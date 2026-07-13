# OrderZ Website — orderz.sg

Complete static site: **78 pages**, built from the page copy docs and the Figma design base (navy #0D2B5E / orange #F4722B, Poppins + Inter).

## Deploy

Upload the **`dist/`** folder to any static host (Netlify, Vercel, cPanel, S3). Includes `sitemap.xml`, `robots.txt`, and 301 redirects in both `_redirects` (Netlify) and `.htaccess` (Apache) formats.

## Rebuild

```
pip install jinja2 python-docx
python3 build.py
```

- `build.py` — renders the 5 handcrafted pages (Home, FnB hub, Cafes, QR Ordering, Reduce Manpower) + auto-generates 73 pages from the docx copy files + sitemap/redirects
- `generator.py` — parses `OrderZ_*_Page_Copy.docx` into structured sections (pains, steps, tiles, outcomes, FAQs, CTAs)
- `pages_map.py` — URL map (nav v4) + 301 redirect list
- `templates/` — `base.html` (header/footer/nav), `generic.html` (universal page renderer), plus the 5 handcrafted page templates
- `assets/` — design system CSS + optimized images (official logo, client logos, photos)
- `figma-assets/` — full image library pulled from Figma + live site (112 files) for future use

## Page inventory (78)

- Home + 4 industry hubs (fnb, beautycare, wellness, retail) + eCommerce Builder hub
- 15 sub-category 360 pages (restaurants, hawker-stalls, cafes, ... aesthetic-clinics)
- 20 POS entry pages (/fnb/cafes-pos ... /retail/multi-branch-retail-pos)
- 11 solution pages (/solutions/...)
- 10 use-case pages (reduce-manpower, peak-hours, ...)
- 4 eCommerce sub-pages
- 11 core pages (platform, how-it-works, pricing, why-orderz, book-demo, contact, support, faq, help, onboarding, success-stories)

## Before launch — action items

1. **Pricing page**: copy contained `[PRICE]` placeholders — rendered as "flat monthly rate" wording. Insert real prices when confirmed.
2. **Testimonials**: all placeholder quotes were stripped per the copy docs' instructions. Success Stories page shows client logos with a "stories being collected" note — replace with verified quotes when available.
3. **Book Demo page**: needs the actual demo booking form wired in (currently CTA buttons link to WhatsApp).
4. **Help page**: guide categories are stubs — link each to full articles when written.
5. QC status: all 78 pages pass automated checks — no placeholder leaks, valid FAQ JSON-LD, all internal links and images resolve.
