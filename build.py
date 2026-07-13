#!/usr/bin/env python3
"""OrderZ static site builder.
Renders templates/*.html (Jinja2) into dist/ with per-page meta + JSON-LD.
Usage: python3 build.py
"""
import json
import re
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).parent
DIST = ROOT / "dist"

ORG_SCHEMA = json.dumps({
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "OrderZ",
    "url": "https://orderz.sg",
    "telephone": "+65 8011 6009",
    "email": "sales@zaroid.com",
    "areaServed": "Singapore",
    "description": "All-in-one business management platform for restaurants, salons, spas, and wellness clinics in Singapore.",
})


def faq_schema(faqs):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    })


PAGES = {
    "index.html": {
        "out": "index.html",
        "canonical": "/",
        "meta_title": "OrderZ - Business Management System for Restaurants, Salons & Clinics | Singapore",
        "meta_description": "OrderZ helps restaurants, spas, salons, and wellness clinics in Singapore manage orders, billing, bookings, and operations in one system. Book a free demo.",
        "og_title": "OrderZ - One System for Restaurants, Salons & Clinics in Singapore",
        "og_description": "Manage orders, billing, bookings and operations from one platform.",
        "faqs": [
            ("What is OrderZ?", "OrderZ is a business operations platform for restaurants, spas, salons, and wellness clinics in Singapore. It combines POS billing, QR ordering, appointment booking, customer management, inventory tracking, and multi-outlet reporting in one system - replacing fragmented tools and reducing operational dependency on staff."),
            ("What industries does OrderZ serve?", "OrderZ serves restaurants, cafes, hawker stalls, food courts, spas, hair salons, beauty salons, nail studios, aesthetic clinics, wellness centres, and therapy practices. It is designed for service and transaction-driven businesses operating with high daily volume across Singapore."),
            ("Is OrderZ suitable for small businesses in Singapore?", "Yes. OrderZ is built for businesses with 1 to 5 outlets and 6 to 30 staff. Small restaurants, cafes, salons, and clinics use OrderZ to reduce manual errors, speed up billing and booking, and give owners real-time visibility without hiring additional administrative staff."),
            ("Does OrderZ support multi-outlet businesses?", "Yes. OrderZ includes multi-outlet management, allowing founders and operations managers to monitor revenue, orders, appointments, and staff performance across all locations from one real-time dashboard - without needing to visit each outlet or consolidate separate reports."),
            ("Is OrderZ GST-ready?", "Yes. OrderZ generates GST-compliant invoices automatically on every transaction. The correct GST rate is applied, itemised on each receipt, and reflected in daily and monthly sales reports - reducing manual tax calculation and keeping your records audit-ready."),
            ("What is the best business management software for F&B in Singapore?", "OrderZ is used by restaurants, cafes, hawker stalls, and food courts across Singapore for POS billing, QR ordering, kitchen workflow, and reporting. It is built for Singapore operations with GST-ready invoicing, local payment support, and a Singapore-based support team."),
            ("How do I book a demo of OrderZ?", "Book a free 30-minute demo at orderz.sg or WhatsApp the OrderZ team directly at +65 8011 6009. The demo is tailored to your business type - restaurant, salon, or clinic - and covers exactly the modules relevant to your operation. No commitment required."),
        ],
    },
    "fnb.html": {
        "out": "fnb/index.html",
        "canonical": "/fnb",
        "meta_title": "FnB Management System Singapore | OrderZ",
        "meta_description": "Singapore all-in-one FnB management system. POS, QR ordering, kitchen display, inventory, and reporting - built for every food and beverage business type. Setup in days.",
        "faqs": [
            ("What types of FnB businesses does OrderZ support?", "OrderZ supports the full range of Singapore FnB business types - restaurants, hawker stalls, cafes, food courts, QSR operations, casual dining, small chains, and bars and pubs. The platform handles both counter service and full table service, and scales from a single-stall hawker setup to a multi-outlet chain."),
            ("Can OrderZ handle dine-in and takeaway orders on the same system?", "Yes. OrderZ manages dine-in table orders, takeaway counter orders, and delivery orders in one unified platform. All three order types flow to the same kitchen display and are captured in the same reporting dashboard."),
            ("Does OrderZ work for hawker stalls that do not have table service?", "Yes. OrderZ is designed for single-person counter operations as much as for full restaurant setups. For hawker stalls, the system supports fast counter POS with QR payment, receipt printing, and real-time sales reporting. Most single-operator stalls are live within one working day."),
            ("How quickly can an FnB business be set up on OrderZ?", "Most FnB businesses are live on OrderZ within one to three working days. Setup includes menu configuration, POS terminal setup, kitchen display installation where required, and full staff training - all completed by the local Singapore support team."),
            ("Can I run QR table ordering and a counter POS at the same time?", "Yes. QR table ordering and counter POS operate simultaneously on OrderZ - all orders from both channels fire to the same kitchen display and are tracked in the same live dashboard."),
            ("Does OrderZ integrate with GrabFood and Foodpanda?", "OrderZ includes a direct online ordering channel for delivery and takeaway - commission-free, through your own branded page, synced to your POS. For integration with third-party delivery platforms such as GrabFood or Foodpanda, speak to the OrderZ team about integration options."),
            ("Can I manage multiple FnB outlets from one dashboard?", "Yes. OrderZ multi-outlet management lets you view revenue, menu performance, staff activity, and stock levels across all locations from a single login."),
            ("Is OrderZ billing GST-compliant?", "Yes. OrderZ generates GST-inclusive receipts automatically for every transaction. Tax rates are configurable, and all billing records are stored and exportable for accounting purposes."),
            ("Does OrderZ support kitchen display screens?", "Yes. Kitchen display screens are a core component of OrderZ. Every order placed fires to the kitchen display the instant it is submitted. Screens can be configured by station."),
            ("What happens to my data if I expand from one outlet to multiple outlets?", "Your data is centralised in OrderZ from the moment you open your first outlet. When additional locations are added, your existing menu, customer, and reporting data carries across automatically."),
        ],
    },
    "cafes.html": {
        "out": "cafes/index.html",
        "canonical": "/cafes",
        "meta_title": "Cafe POS System Singapore | OrderZ",
        "meta_description": "OrderZ helps Singapore cafes manage QR orders, customise drinks, track inventory, and run loyalty programmes from one connected system. Book a free demo.",
        "faqs": [
            ("Does OrderZ work for cafes and coffee shops in Singapore?", "Yes. OrderZ is designed for cafes and coffee shops that need QR ordering with drink customisation, bar display integration, inventory tracking, and loyalty management. It handles both walk-in counter orders and QR table or counter ordering from the same connected system."),
            ("Can customers customise their drinks when ordering via QR?", "Yes. Your QR menu includes full customisation options - milk type, syrup, shot count, temperature, and any modifier you define. The customisation appears on your bar display the moment the order is placed."),
            ("Does OrderZ help cafes track milk and ingredient inventory?", "Yes. OrderZ deducts inventory automatically as items are sold. When oat milk or a key ingredient reaches a low-stock threshold, you receive an alert before you run out mid-shift."),
            ("Can OrderZ run a loyalty programme for my cafe?", "Yes. OrderZ tracks customer visits and purchases automatically. You can set up a stamp card, a points-based rewards programme, or a custom loyalty structure. Rewards apply without any staff effort."),
            ("How does OrderZ speed up the morning rush at my cafe?", "Customers can order from your QR menu before they reach the counter. Orders go directly to your bar display. Your baristas start making drinks while other customers are still in the queue."),
            ("Does OrderZ support PayNow and contactless payment for cafes?", "Yes. OrderZ accepts PayNow, NETS, contactless card, and cash from one integrated system. End-of-day reconciliation is generated automatically."),
            ("How much does cafe management software cost in Singapore?", "Costs vary by provider, modules, and outlet count. OrderZ offers packages suited to single-outlet cafes and multi-branch coffee shop groups. Book a free demo for the right configuration and pricing."),
        ],
    },
    "solutions-qr-ordering.html": {
        "out": "solutions/qr-ordering-system/index.html",
        "canonical": "/solutions/qr-ordering-system",
        "meta_title": "QR Ordering System Singapore for F&B & Salons | OrderZ",
        "meta_description": "QR code ordering system for Singapore restaurants, salons, and clinics. Table ordering, digital menus, PayNow payment, real-time order routing. No commission fees. Book a free demo today.",
        "faqs": [
            ("What is the best QR ordering system for restaurants in Singapore?", "The best QR ordering system for Singapore restaurants lets customers scan a table QR code, browse a live menu with photos, place their order, and pay via PayNow or card - without a waiter. OrderZ does all of this natively, with direct kitchen routing, GST-compliant receipts, and a live menu you can update in seconds."),
            ("Can salons and clinics use QR ordering with OrderZ?", "Yes. Salons, spas, nail studios, and clinics use OrderZ QR codes at reception and waiting areas - a live service menu, digital walk-in check-in, and waitlist sign-up."),
            ("Does OrderZ QR ordering connect to the kitchen and the POS?", "Yes. Every QR order goes directly to your kitchen display or kitchen printer, and is simultaneously recorded in the OrderZ POS as a live transaction."),
            ("Can customers pay via PayNow or NETS through the QR code?", "Yes. OrderZ QR ordering includes built-in payment - PayNow, NETS, Visa, and Mastercard are all supported. A GST-compliant receipt is sent automatically by WhatsApp or email."),
            ("How is OrderZ QR ordering different from GrabFood or Foodpanda?", "GrabFood and Foodpanda charge 25-30% commission on every order. OrderZ QR ordering is own-channel - the customer orders from your branded menu and pays you directly with zero commission."),
            ("Can I update my menu in real time - including sold-out items?", "Yes. Update your menu instantly from any device - change a price, mark an item as sold out, add a daily special. The change appears on every QR code immediately."),
            ("Does OrderZ QR ordering work across multiple restaurant outlets?", "Yes. OrderZ manages QR menus for all your outlets from one account, with outlet-specific pricing where needed and consolidated revenue reporting."),
            ("Does the customer need to download an app to use QR ordering?", "No. Customers scan the QR code with any standard phone camera - no app download, no account creation, and no login required."),
        ],
    },
    "reduce-manpower.html": {
        "out": "reduce-manpower/index.html",
        "canonical": "/reduce-manpower",
        "meta_title": "Reduce Manpower Singapore - F&B, Salons & Clinics | OrderZ",
        "meta_description": "Reduce your dependence on frontline staff in Singapore - without reducing service quality. OrderZ automates order-taking, billing, and appointment booking for restaurants, salons, and clinics. Book a demo.",
    },
}


def render():
    env = Environment(loader=FileSystemLoader(ROOT / "templates"))
    DIST.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT / "assets", DIST / "assets", dirs_exist_ok=True)

    for template_name, cfg in PAGES.items():
        out_path = DIST / cfg["out"]
        out_path.parent.mkdir(parents=True, exist_ok=True)
        depth = cfg["out"].count("/")
        rel_root = "../" * depth if depth else "./"
        schema_blocks = [ORG_SCHEMA]
        if cfg.get("faqs"):
            schema_blocks.append(faq_schema(cfg["faqs"]))
        html = env.get_template(template_name).render(
            root=rel_root,
            canonical=cfg["canonical"],
            meta_title=cfg["meta_title"],
            meta_description=cfg["meta_description"],
            og_title=cfg.get("og_title"),
            og_description=cfg.get("og_description"),
            schema_blocks=schema_blocks,
        )
        out_path.write_text(html, encoding="utf-8")
        print(f"built {cfg['out']}")


if __name__ == "__main__":
    render()
    print("done ->", DIST)


# ================= AUTO-GENERATED PAGES =================
import sys as _sys
_sys.path.insert(0, str(ROOT))
from generator import parse_docx
from pages_map import PAGES_MAP, REDIRECTS

ICONS = ["⬚", "▦", "📅", "👥", "📦", "📊", "🖥", "💳", "🎁", "📈", "🏬", "📝"]
SRC_DOCX = ROOT.parent

def _clean(s):
    if not isinstance(s, str): return s
    s = s.replace(" -- ", " — ").replace("--", "—")
    s = re.sub(r'\[PRICE\]\s*SGD per month', 'a flat monthly fee', s)
    s = re.sub(r'\[PRICE\]\s*SGD per outlet', 'a flat monthly fee per outlet', s)
    s = re.sub(r'\[PRICE\]\s*/ month per outlet', 'Flat monthly rate per outlet', s)
    s = re.sub(r'\[PRICE\]', 'a flat monthly rate', s)
    return s.strip()

def _clean_page(page):
    page['h1'] = _clean(page['h1'])
    page['sub'] = _clean(page['sub'])
    page['tagline'] = [_clean(t) for t in page['tagline']]
    page['faqs'] = [(_clean(q), _clean(a)) for q, a in page['faqs']]
    for k in ('heading', 'sub', 'trust'):
        if page['final'].get(k): page['final'][k] = _clean(page['final'][k])
    for s in page['sections']:
        s['heading'] = _clean(s['heading'])
        s['lead'] = _clean(s['lead'])
        for b in s['blocks']:
            d = b.get('data')
            if isinstance(d, tuple): b['data'] = tuple(_clean(x) for x in d)
            elif isinstance(d, list): b['data'] = [tuple(_clean(x) for x in i) if isinstance(i, tuple) else _clean(i) for i in d]
            elif isinstance(d, str): b['data'] = _clean(d)
    return page

def _split_trust(s):
    if not s: return []
    parts = re.split(r'\s*[·|]\s*', s)
    return [p.strip() for p in parts if p.strip() and len(p) < 60][:5]

def _card_group_type(sec_name):
    n = sec_name.lower()
    if 'pain' in n or 'problem' in n: return 'pains'
    if 'outcome' in n or 'change' in n: return 'outcomes'
    if 'solution' in n or 'tile' in n or 'include' in n or 'feature' in n: return 'tiles'
    return 'cards'

def _prepare_sections(page):
    out = []
    soft = True
    for sec in page['sections']:
        name = sec['name']
        nl = name.lower()
        if nl in ('_hero',) or nl.startswith('hero'):
            continue
        if 'faq' in nl:
            continue
        groups = []
        cur_grp = None
        def flush():
            nonlocal cur_grp
            if cur_grp and cur_grp.get('cards'): groups.append(cur_grp)
            cur_grp = None
        if 'social proof' in nl or 'trusted by' in (sec['heading'] or '').lower():
            groups.append({'type': 'logos'})
            out.append({'heading': sec['heading'], 'lead': sec['lead'], 'groups': groups, 'soft': soft, 'name': name})
            soft = not soft
            continue
        gmap = {'quote': 'quotes', 'card': None, 'step': 'steps', 'outcome': 'outcomes'}
        for b in sec['blocks']:
            bt = b['type']
            if bt == 'cta':
                flush()
                if not groups or groups[-1].get('type') != 'cta':
                    groups.append({'type': 'cta'})
                continue
            if bt == 'para':
                flush(); groups.append({'type': 'para', 'text': b['data']}); continue
            if bt == 'rowcards':
                flush()
                items = [(t, d) for t, d in b['data']
                         if not re.match(r'^(Differentiator|FnB Business Type|Business Type|✓|Item)', t)]
                if items: groups.append({'type': _card_group_type(name), 'cards': items})
                continue
            gt = gmap.get(bt)
            if gt is None:  # card → context type
                gt = _card_group_type(name)
            if cur_grp and cur_grp['type'] == gt:
                cur_grp['cards'].append(b['data'])
            else:
                flush()
                cur_grp = {'type': gt, 'cards': [b['data']]}
        flush()
        # drop trailing duplicate ctas
        while len(groups) > 1 and groups[-1].get('type') == 'cta' and groups[-2].get('type') == 'cta':
            groups.pop()
        if not groups and not sec['heading']:
            continue
        out.append({'heading': sec['heading'], 'lead': sec['lead'], 'groups': groups, 'soft': soft, 'name': name})
        soft = not soft
    return out

def build_auto():
    env = Environment(loader=FileSystemLoader(ROOT / "templates"))
    tpl = env.get_template("generic.html")
    built, issues = 0, []
    for stem, (url, info) in PAGES_MAP.items():
        docx = SRC_DOCX / (stem + ".docx")
        if not docx.exists():
            issues.append((stem, "docx missing")); continue
        try:
            page = _clean_page(parse_docx(docx))
        except Exception as e:
            issues.append((stem, f"parse error: {e}")); continue
        if not page['h1']:
            page['h1'] = info['crumbs'][-1][0] + " — OrderZ"
        if stem == "OrderZ_Success_Stories_Page_Copy":
            for s in page['sections']:
                s['blocks'] = [bl for bl in s['blocks'] if bl['type'] in ('cta',)]
            page['sections'] = [s for s in page['sections'] if s['heading'] or s['blocks']]
            page['sections'].insert(0, {'name': 'Social Proof', 'heading': 'Trusted by F&B, beauty, and wellness businesses across Singapore.',
                'lead': 'Verified customer stories are being collected and will be published here. In the meantime, these are some of the businesses running on OrderZ today.', 'blocks': []})
        page['trust_items'] = _split_trust(page.get('trust'))
        page['final']['trust_items'] = _split_trust(page['final'].get('trust'))
        sections = _prepare_sections(page)
        depth = url.count("/")
        rel_root = "../" * depth if depth else "./"
        canonical = "/" + url.rstrip("/")
        meta_title = page['meta_title'] or (page['h1'][:57] + " | OrderZ" if page['h1'] else "OrderZ")
        meta_desc = page['meta_description'] or (page['sub'][:158] if page['sub'] else "OrderZ — all-in-one business management platform for Singapore.")
        schema_blocks = [ORG_SCHEMA]
        if page['faqs']:
            schema_blocks.append(faq_schema(page['faqs']))
        html = tpl.render(
            root=rel_root, canonical=canonical,
            meta_title=_clean(meta_title), meta_description=_clean(meta_desc),
            og_title=None, og_description=None,
            schema_blocks=schema_blocks,
            page=page, sections=sections,
            eyebrow=info['eyebrow'], crumbs=[{'label': l, 'url': u} for l, u in info['crumbs']],
            icons=ICONS,
            faq_heading="Frequently asked questions.",
        )
        out_path = DIST / url / "index.html"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html, encoding="utf-8")
        built += 1
    print(f"auto-built {built} pages")
    for s, msg in issues: print("  WARN", s, msg)
    # sitemap
    urls = ["/"] + [cfg["canonical"] for cfg in PAGES.values() if cfg["canonical"] != "/"]
    urls += ["/" + u.rstrip("/") for u, _ in PAGES_MAP.values()]
    urls = sorted(set(urls))
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        loc = "https://orderz.sg" + (u if u != "/" else "/")
        sm.append(f"  <url><loc>{loc}</loc></url>")
    sm.append("</urlset>")
    (DIST / "sitemap.xml").write_text("\n".join(sm), encoding="utf-8")
    # redirects (Netlify + Apache)
    (DIST / "_redirects").write_text("\n".join(f"{a} {b} 301!" for a, b in REDIRECTS) + "\n", encoding="utf-8")
    (DIST / ".htaccess").write_text("\n".join(f"Redirect 301 {a} https://orderz.sg{b}" for a, b in REDIRECTS) + "\n", encoding="utf-8")
    (DIST / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://orderz.sg/sitemap.xml\n", encoding="utf-8")
    print("sitemap:", len(urls), "urls; redirects:", len(REDIRECTS))

if __name__ == "__main__":
    build_auto()
