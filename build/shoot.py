import asyncio, sys
from playwright.async_api import async_playwright
from PIL import Image
S = sys.argv[1]
BASE = 'http://localhost:8765'
JOBS = [
    ('home-d', '/', 1440), ('home-m', '/', 390),
    ('renew-d', '/renewables/', 1440), ('led-d', '/led-lighting/', 1440), ('led-m', '/led-lighting/', 390),
    ('about-d', '/about-us/', 1440), ('contact-m', '/contact-us-wakefield-electricians/', 390),
    ('blog-d', '/blog/', 1440), ('post-m', '/thermal-imaging-how-commercial-electricians-in-yorkshire-prevent-costly-downtime/', 390),
]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        problems = []
        for name, path, w in JOBS:
            ctx = await b.new_context(viewport={'width': w, 'height': 900}, device_scale_factor=1, reduced_motion='reduce')
            page = await ctx.new_page()
            msgs = []
            page.on('console', lambda m: msgs.append(m.type + ': ' + m.text) if m.type in ('error', 'warning') else None)
            page.on('pageerror', lambda e: msgs.append('pageerror: ' + str(e)))
            await page.goto(BASE + path, wait_until='networkidle')
            await page.evaluate('document.fonts.ready')
            # widest element check for horizontal overflow
            ov = await page.evaluate('''() => { const W = document.documentElement.clientWidth; const out = [];
              for (const el of document.querySelectorAll('body *')) { const r = el.getBoundingClientRect(); if (r.right > W + 1 && r.width > 0) out.push(el.tagName + '.' + (el.className||'').toString().slice(0,40) + ' ' + Math.round(r.right)); }
              return {sw: document.documentElement.scrollWidth, W, out: out.slice(0,8)}; }''')
            fonts = await page.evaluate('[...document.fonts].filter(f=>f.status==="loaded").map(f=>f.family+" "+f.weight).join(", ")')
            if ov['sw'] > ov['W'] or msgs: problems.append((name, ov, msgs))
            await page.screenshot(path=f'{S}/{name}.png', full_page=True)
            print(name, 'height', (await page.evaluate('document.documentElement.scrollHeight')), 'overflow', ov['sw'] - ov['W'], 'fonts:', fonts[:80])
            await ctx.close()
        await b.close()
        print('PROBLEMS', problems)
asyncio.run(main())
