import asyncio
import sys

from playwright.async_api import async_playwright

S = sys.argv[1]
BASE = 'http://localhost:8765'
JOBS = [
    ('home-d', '/', 1440), ('home-m', '/', 390),
    ('renew-d', '/renewables/', 1440), ('cummins-d', '/cummins-turbo-technologies/', 1440), ('led-m', '/led-lighting/', 390),
    ('about-d', '/about-us/', 1440), ('contact-d', '/contact-us-wakefield-electricians/', 1440),
    ('contact-m', '/contact-us-wakefield-electricians/', 390), ('blog-d', '/blog/', 1440), ('projects-d', '/projects/', 1440),
]


async def settle(page):
    h = await page.evaluate('document.documentElement.scrollHeight')
    y = 0
    while y < h:
        await page.evaluate(f'window.scrollTo(0,{y})')
        await page.wait_for_timeout(60)
        y += 500
        h = await page.evaluate('document.documentElement.scrollHeight')
    await page.evaluate('window.scrollTo(0,0)')
    await page.wait_for_timeout(400)
    await page.wait_for_load_state('networkidle')


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        probs = []
        for name, path, w in JOBS:
            ctx = await b.new_context(viewport={'width': w, 'height': 900}, device_scale_factor=1, reduced_motion='reduce')
            page = await ctx.new_page()
            msgs = []
            page.on('console', lambda m: msgs.append(m.type + ': ' + m.text) if m.type == 'error' and 'TUNNEL' not in m.text else None)
            page.on('pageerror', lambda err: msgs.append('pageerror: ' + str(err)))
            await page.goto(BASE + path, wait_until='networkidle')
            await settle(page)
            ov = await page.evaluate('''() => { const W = document.documentElement.clientWidth; const out = [];
              for (const el of document.querySelectorAll('body *')) { const r = el.getBoundingClientRect();
                if (r.right > W + 1 && r.width > 0 && getComputedStyle(el).position !== 'fixed') out.push(el.tagName + '.' + (el.className||'').toString().slice(0,30) + ' ' + Math.round(r.right)); }
              return {sw: document.documentElement.scrollWidth, W, out: out.slice(0,6)}; }''')
            if ov['sw'] > ov['W'] or msgs:
                probs.append((name, ov, msgs[:4]))
            await page.screenshot(path=f'{S}/{name}.png', full_page=True)
            print(name, await page.evaluate('document.documentElement.scrollHeight'), 'overflow', ov['sw'] - ov['W'])
            await ctx.close()
        ctx = await b.new_context(viewport={'width': 1440, 'height': 820}, device_scale_factor=1)
        page = await ctx.new_page()
        await page.goto(BASE + '/', wait_until='networkidle')
        await page.wait_for_timeout(1800)
        await page.screenshot(path=f'{S}/hero-anim.png')
        await page.hover('button.nav-link[aria-controls="mega-services"]')
        await page.wait_for_timeout(700)
        await page.screenshot(path=f'{S}/mega.png')
        await page.mouse.move(10, 600)
        await page.wait_for_timeout(500)
        await page.evaluate('window.scrollTo(0, 1250)')
        await page.wait_for_timeout(1600)
        await page.screenshot(path=f'{S}/scrolled.png')
        await ctx.close()
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
        page = await ctx.new_page()
        await page.goto(BASE + '/', wait_until='networkidle')
        await page.wait_for_timeout(1500)
        await page.screenshot(path=f'{S}/m-hero.png')
        await page.click('.menu-toggle')
        await page.wait_for_timeout(900)
        await page.screenshot(path=f'{S}/m-menu.png')
        await ctx.close()
        await b.close()
        print('PROBLEMS', probs)

asyncio.run(main())
