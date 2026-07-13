#!/usr/bin/env python3
"""Parse OrderZ_*_Page_Copy.docx files into structured page dicts."""
import re
import json
import pathlib
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph

SRC = pathlib.Path(__file__).parent.parent  # OrderZ folder

SKIP_TABLE_PAT = re.compile(r'\[DEV NOTE|Pre-Launch|☐|✓ ?☐|ACTION REQUIRED|\[CONFIRM|word count|Word Count|QC / |Quality Check|LOGO GRID|logo grid|Insert confirmed|\[Owner Name|\[Client|STRESS TEST', re.I)
CTA_TABLE_PAT = re.compile(r'^\s*>?\s*(▶\s*)?Book a Free Demo', re.I)
DIVIDER = re.compile(r'^─+$')
MARKER = re.compile(r'^\[\s*(.+?)\s*\]$')

def iter_blocks(doc):
    from docx.oxml.ns import qn
    body = doc.element.body
    for child in body.iterchildren():
        if child.tag == qn('w:p'):
            yield ('p', Paragraph(child, doc).text.strip())
        elif child.tag == qn('w:tbl'):
            t = Table(child, doc)
            rows = []
            for row in t.rows:
                cells = []
                for c in row.cells:
                    txt = c.text.strip()
                    if not cells or cells[-1] != txt:
                        cells.append(txt)
                rows.append(cells)
            yield ('t', rows)

def table_text(rows):
    return "\n".join(" | ".join(r) for r in rows)

def classify_table(rows):
    txt = table_text(rows)
    if re.search(r'META TITLE|Title Tag\s*\|', txt): return ('meta', txt)
    if SKIP_TABLE_PAT.search(txt): return ('skip', None)
    if CTA_TABLE_PAT.search(txt.strip()): return ('cta', None)
    # multi-row pipe tables (e.g. business types, differentiators)
    if len(rows) > 2 and all(len(r) >= 2 for r in rows):
        return ('rowcards', [(r[0], r[1]) for r in rows if len(r) >= 2 and r[0] and r[1]])
    lines = []
    for r in rows:
        for c in r:
            for l in c.split("\n"):
                if l.strip(): lines.append(l.strip())
    if not lines: return ('skip', None)
    head = lines[0]
    if re.fullmatch(r'\d+', head) and len(lines) >= 2:
        title = lines[1]; body = " ".join(lines[2:])
        return ('step', (head, title, body))
    body = " ".join(lines[1:]) if len(lines) > 1 else ""
    m = re.match(r'^(\d+)\s*\|\s*(.+)$', head)
    if m: return ('step', (m.group(1), m.group(2), body))
    if head.startswith('+'): return ('outcome', (head.lstrip('+ ').strip(), body))
    if re.search(r'\[(Insert|Client|Owner|X\]|PRICE\b)|NOTE TO EDITOR|EDITOR:', head + ' ' + body):
        if 'PRICE' not in head + body: return ('skip', None)
    if 'NOTE TO EDITOR' in head or head.startswith('EDITOR'): return ('skip', None)
    if head.startswith('"') or head.startswith('> "'):
        if '[' in head: return ('skip', None)
        return ('quote', (head.lstrip('> '), body))
    if body: return ('card', (head, body))
    return ('para', head)

def parse_meta(txt):
    meta = {}
    # row style: "Title Tag | X" / "META TITLE (50 chars) | X"
    for line in txt.split("\n"):
        parts = [x.strip() for x in line.split("|")]
        if len(parts) >= 2:
            key = re.sub(r'\s*\(.*?\)', '', parts[0]).strip().upper()
            if key in ('TITLE TAG', 'META TITLE'): meta['title'] = " | ".join(p for p in parts[1:] if p)
            if key in ('META DESCRIPTION', 'META DESC'): meta['description'] = parts[1]
    if meta.get('title'): return meta
    def grab(pat):
        m = re.search(pat, txt, re.S)
        return re.sub(r'\s+', ' ', m.group(1)).strip() if m else None
    stop = r'(?=\n\s*(?:META DESC|H1 TAG|CANONICAL|SCHEMA|PRIMARY|SECONDARY|OG |OLD URL|PHASE|Sub-category|Title Tag|URL )|\n\s*\n|\Z)'
    meta['title'] = grab(r'(?:META TITLE|Title Tag)[^\n]*[\n|](.+?)' + stop)
    meta['description'] = grab(r'META DESC(?:RIPTION)?[^\n]*[\n|](.+?)' + stop)
    return meta

def parse_docx(path):
    doc = Document(str(path))
    page = {'h1': None, 'tagline': [], 'sub': None, 'meta_title': None,
            'meta_description': None, 'sections': [], 'faqs': [], 'final': {}, 'trust': None}
    sections = page['sections']
    cur = None            # current section dict
    pending = None        # next paragraph role
    in_faq_q = None
    hero_done = False
    in_appendix = False
    sec_name = ""
    pend_title = None

    def new_section(name):
        nonlocal cur
        cur = {'name': name, 'heading': None, 'lead': None, 'blocks': []}
        sections.append(cur)

    new_section("_hero")

    for kind, data in iter_blocks(doc):
        if kind == 'p':
            t = data
            if not t or DIVIDER.match(t): continue
            if re.search(r'NOTE TO EDITOR|^EDITOR\s*:|^DEVELOPER NOTE|\[Insert|\[Client|\[Owner|^>\s*"?\[', t): continue
            if re.match(r'^Appendix', t, re.I): in_appendix = True
            if in_appendix: continue
            sm = re.match(r'^Section\s+\d+\s*[—-]\s*(.+)$', t, re.I)
            if sm:
                sec_name = sm.group(1).strip()
                new_section(sec_name)
                pending = None; pend_title = None
                continue
            bm = re.match(r'^\[\s*([A-Z][A-Z0-9 &\'/—\-()%,.:]+?)(\(.*)?\s*\]?$', t)
            mk = MARKER.match(t)
            marker = (mk.group(1) if mk else (bm.group(1) if bm and t.startswith('[') else None))
            if marker:
                mu = marker.upper()
                if 'APPENDIX' in mu or 'CHECKLIST' in mu or re.search(r'\bQC\b|STRESS TEST|QUALITY CHECK', mu):
                    in_appendix = True; continue
                if 'H1' in mu: pending = 'h1'
                elif 'TAGLINE' in mu or 'PAIN LINES' in mu: pending = 'tagline'
                elif 'SUBHEADLINE' in mu or 'SUBTEXT' in mu: pending = 'sub'
                elif 'SECTION HEADING' in mu or mu.startswith('HERO SECTION'): pending = 'heading'
                elif 'HERO BAND' in mu: pending = 'h1'
                elif 'FINAL CTA' in mu:
                    new_section('Final CTA'); pending = 'heading'
                elif 'FAQ' in mu:
                    new_section('FAQ'); pending = None
                elif 'REASSURANCE' in mu or 'TRUST LINE' in mu: pending = 'trust'
                elif mu.startswith('HELP CATEGORY'):
                    new_section(marker.split(':',1)[1].strip().title() if ':' in marker else marker.title())
                    pending = None
                elif re.search(r'SECTION|BLOCK|BAND', mu):
                    if 'CTA' in mu:
                        cur['blocks'].append({'type': 'cta'}); pending = None
                    else:
                        new_section(marker.title()); pending = 'heading'
                else: pending = None
                continue
            um = t.upper()
            if um in ('SECTION HEADING', 'CONNECTOR TEXT', 'SUBTEXT', 'SUBHEADLINE', 'REASSURANCE TEXT'):
                pending = {'SECTION HEADING':'heading','CONNECTOR TEXT':'lead','SUBTEXT':'sub2','SUBHEADLINE':'sub','REASSURANCE TEXT':'lead'}[um]
                continue
            if re.match(r'^(H1 TAG|META |CANONICAL|SCHEMA |OG |PRIMARY KEY|SECONDARY|Persona|Page:|Old URL|CTA BUTTON|TRUST LINE|DISPLAY TAGLINE|CLIENT LOGO|TESTIMONIAL|STAT LINE|Meta title|Meta desc|Primary keyword|Secondary keywords|AEO note|OrderZ$|Website Page Copy|orderz\.sg|www\.orderz\.sg|Triple-Purpose|PAGE META|Hand this|Complete every|Verify every)', t, re.I):
                if re.match(r'^Meta title', t, re.I):
                    m = re.search(r':\s*(.+)$', t); page['meta_title'] = m.group(1).strip() if m else None
                if re.match(r'^Meta desc', t, re.I):
                    m = re.search(r':\s*(.+)$', t); page['meta_description'] = m.group(1).strip() if m else None
                if re.match(r'^H1 TAG', t, re.I): pending = 'h1'
                continue
            if t.startswith('Q:'):
                in_faq_q = t[2:].strip(); continue
            if t.startswith('A:') and in_faq_q:
                page['faqs'].append((in_faq_q, t[2:].strip())); in_faq_q = None; continue
            if in_faq_q and len(t) > 80 and not t.startswith('Q:'):
                page['faqs'].append((in_faq_q, t)); in_faq_q = None; continue
            if t.startswith('▶'):
                continue
            # trust line heuristic
            if re.search(r'(·|\|)', t) and re.search(r'No long contracts|Live in|GST|Singapore support|Setup in days|No app download|no commitment', t, re.I) and len(t) < 200:
                if cur['name'] == 'Final CTA': page['final']['trust'] = t
                else: page['trust'] = page['trust'] or t
                continue
            # assign by pending role
            if pending == 'h1' and not page['h1']:
                page['h1'] = t; pending = None; continue
            if pending == 'tagline':
                if len(page['tagline']) < 4 and len(t) < 160: page['tagline'].append(t)
                continue
            if pending == 'sub' and not page['sub'] and not hero_done:
                page['sub'] = t; pending = None; continue
            if pending in ('heading',):
                if cur['name'] == 'Final CTA' and not page['final'].get('heading'):
                    page['final']['heading'] = t
                    pending = 'sub2'
                elif not cur['heading']:
                    cur['heading'] = t; pending = None
                continue
            if pending in ('sub2',):
                if cur['name'] == 'Final CTA': page['final']['sub'] = t
                else: cur['lead'] = cur['lead'] or t
                pending = None; continue
            if pending == 'lead':
                cur['lead'] = cur['lead'] or t; pending = None; continue
            if pending == 'trust':
                if cur['name'] == 'Final CTA': page['final']['trust'] = t
                else: page['trust'] = page['trust'] or t
                pending = None; continue
            # unassigned paragraph
            if cur['name'] == '_hero' and not page['h1'] and 20 < len(t) < 120 and not page['sections'][0]['blocks']:
                page['h1'] = t; continue
            if cur['name'] == '_hero' and page['h1'] and not page['sub'] and len(t) > 80:
                page['sub'] = t; continue
            if cur['name'] == 'Final CTA':
                if not page['final'].get('heading') and len(t) < 120: page['final']['heading'] = t
                elif not page['final'].get('sub'): page['final']['sub'] = t
                continue
            if not cur['heading'] and len(t) < 120 and not cur['blocks']:
                cur['heading'] = t; continue
            # title/body pairing
            if pend_title is not None:
                if len(t) > 130:
                    cur['blocks'].append({'type': 'card', 'data': (pend_title, t)})
                    pend_title = None; continue
                pend_title = t if len(t) < 120 else None
                continue
            if len(t) < 120:
                pend_title = t; continue
            if not cur['lead'] and len(t) > 60:
                cur['lead'] = t; continue
            continue
        else:  # table
            if in_appendix: continue
            ttype, payload = classify_table(data)
            if ttype == 'meta':
                m = parse_meta(payload)
                page['meta_title'] = page['meta_title'] or m.get('title')
                page['meta_description'] = page['meta_description'] or m.get('description')
                # H1 from meta table
                hm = re.search(r'H1 TAG[^\n]*\n\s*(.+)', payload)
                if hm and not page['h1']: page['h1'] = re.sub(r'\s+',' ',hm.group(1)).strip()
            elif ttype == 'skip' or ttype is None:
                continue
            elif ttype == 'cta':
                cur['blocks'].append({'type': 'cta'})
            else:
                cur['blocks'].append({'type': ttype, 'data': payload})
    # h1 fixup: doc-title leak
    hero_secs = [s for s in page['sections'] if s['name'].lower().startswith('hero')]
    if page['h1'] and (page['h1'].startswith('OrderZ') or 'Page Copy' in page['h1']):
        if hero_secs and hero_secs[0]['heading']:
            page['h1'] = hero_secs[0]['heading']; hero_secs[0]['heading'] = None
    # hero section heading that duplicates h1
    for s in hero_secs:
        if s['heading'] == page['h1']: s['heading'] = None
    # cleanup: drop empty sections
    page['sections'] = [s for s in page['sections']
                        if s['blocks'] or (s['heading'] and s['name'] not in ('_hero',))]
    return page

if __name__ == '__main__':
    import sys
    p = parse_docx(SRC / sys.argv[1])
    print(json.dumps(p, indent=1)[:4000])
