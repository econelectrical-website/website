"""Screenshots plus behaviour tests for round 3: scroll position on new pages, anchors, blog filters, overflow on every page."""
import asyncio
import re
import sys

from playwright.async_api import async_playwright

S = sys.argv[1]
BASE = 'http://localhost:8765'
SHOTS = [
    ('home-d', '/', 1440), ('home-m', '/', 390),
    ('blog-d', '/blog/', 1440), ('blog-m', '/blog/', 390),
    ('post-d', '/workplace-and-fleet-ev-charging-installation/', 1440), ('post-m', '/how-often-does-a-commercial-building-need-an-eicr/', 390),
    ('contact-d', '/contact-us-wakefield-electricians/', 1440), ('school-d', '/school-led-grants/', 1440),
]

HARNESS = '''<!doctype html><html><body style="margin:0;background:#222">
<div style="height:120px;background:#444;color:#fff;font:16px sans-serif;padding:20px">Viewer bar</div>
<iframe id="f" src="/projects/" style="width:100%;border:0;display:block" scrolling="no"></iframe>
<script>
var f=document.getElementById('f');
function size(){ try { f.style.height=f.contentDocument.documentElement.scrollHeight+'px'; } catch(e){} }
f.addEventListener('load',function(){ size(); setTimeout(size,400); setTimeout(size,1200); });
</script></body></html>'''


async def settle(page):
    h = await page.evaluate('document.documentElement.scrollHeight')
    y = 0
    while y < h:
        await page.evaluate(f'window.scrollTo(0,{y})')
        await page.wait_for_timeout(50)
        y += 600
        h = await page.evaluate('document.documentElement.scrollHeight')
    await page.evaluate('window.scrollTo(0,0)')
    await page.wait_for_timeout(300)


async def main():
    results = []
    async with async_playwright() as p:
        b = await p.chromium.launch()

        # 1. screenshots
        for name, path, w in SHOTS:
            ctx = await b.new_context(viewport={'width': w, 'height': 900}, device_scale_factor=1, reduced_motion='reduce')
            await ctx.add_init_script("try{localStorage.setItem('econ:consent','denied')}catch(e){}")
            page = await ctx.new_page()
            errs = []
            page.on('pageerror', lambda err: errs.append(str(err)))
            await page.goto(BASE + path, wait_until='networkidle')
            await settle(page)
            await page.screenshot(path=f'{S}/{name}.png', full_page=True)
            results.append((name, 'errors', errs))
            await ctx.close()

        # 2. overflow on every page at phone width
        sm = open('dist/site/sitemap.xml').read()
        paths = [re.sub(r'^https://econelectrical\.co\.uk', '', u) for u in re.findall(r'<loc>([^<]+)</loc>', sm)]
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, reduced_motion='reduce')
        await ctx.add_init_script("try{localStorage.setItem('econ:consent','denied')}catch(e){}")
        page = await ctx.new_page()
        over = []
        for path in paths:
            await page.goto(BASE + path, wait_until='load')
            ov = await page.evaluate('document.documentElement.scrollWidth - document.documentElement.clientWidth')
            if ov > 0:
                over.append((path, ov))
        results.append(('overflow at 390px', len(paths), 'pages', over))
        await ctx.close()

        # 3. normal navigation: card clicked half way down the projects page opens the project at the top
        ctx = await b.new_context(viewport={'width': 1440, 'height': 900})
        await ctx.add_init_script("try{localStorage.setItem('econ:consent','denied')}catch(e){}")
        page = await ctx.new_page()
        await page.goto(BASE + '/projects/', wait_until='networkidle')
        await page.evaluate('window.scrollTo(0, 1400)')
        await page.wait_for_timeout(600)
        await page.click('.proj-grid .proj-card:nth-child(4)')
        await page.wait_for_load_state('networkidle')
        await page.wait_for_timeout(500)
        results.append(('project from list', page.url, 'scrollY', await page.evaluate('scrollY')))
        # next project card at the bottom of a project page
        await page.evaluate('window.scrollTo(0, document.documentElement.scrollHeight)')
        await page.wait_for_timeout(900)
        await page.click('a.next-card')
        await page.wait_for_load_state('networkidle')
        await page.wait_for_timeout(500)
        results.append(('next project', page.url, 'scrollY', await page.evaluate('scrollY')))
        # back button still returns to where you were
        await page.go_back()
        await page.wait_for_load_state('networkidle')
        await page.wait_for_timeout(700)
        results.append(('back button', page.url, 'scrollY (should be near the bottom)', await page.evaluate('scrollY')))
        await ctx.close()

        # 4. a viewer that keeps the old scroll position when a new page loads
        ctx = await b.new_context(viewport={'width': 1440, 'height': 900})
        await ctx.add_init_script("try{localStorage.setItem('econ:consent','denied')}catch(e){}")
        await ctx.add_init_script('''document.addEventListener('readystatechange', function () {
            if (document.readyState === 'interactive' && location.pathname !== '/projects/') window.scrollTo(0, 2200); });''')
        page = await ctx.new_page()
        await page.goto(BASE + '/projects/', wait_until='networkidle')
        await page.click('.proj-grid .proj-card:nth-child(2)')
        await page.wait_for_load_state('networkidle')
        await page.wait_for_timeout(700)
        results.append(('kept scroll simulated', page.url, 'scrollY', await page.evaluate('scrollY')))
        await ctx.close()

        # 5. the site shown inside a taller page (the outer page scrolls, not the site)
        ctx = await b.new_context(viewport={'width': 1280, 'height': 860})
        await ctx.add_init_script("try{localStorage.setItem('econ:consent','denied')}catch(e){}")
        page = await ctx.new_page()
        await page.route(BASE + '/__harness.html', lambda r: r.fulfill(status=200, content_type='text/html', body=HARNESS))
        await page.goto(BASE + '/__harness.html', wait_until='networkidle')
        await page.wait_for_timeout(1500)
        await page.evaluate('window.scrollTo(0, 2600)')
        await page.wait_for_timeout(500)
        before = await page.evaluate('scrollY')
        frame = page.frame_locator('#f')
        await frame.locator('.proj-grid .proj-card:nth-child(3)').click()
        await page.wait_for_timeout(2500)
        results.append(('inside a taller page', 'outer scrollY before', before, 'after', await page.evaluate('scrollY')))
        await page.screenshot(path=f'{S}/harness.png')
        await ctx.close()

        # 6. same page anchor glides and keeps the hash; blog filters
        ctx = await b.new_context(viewport={'width': 1440, 'height': 900})
        await ctx.add_init_script("try{localStorage.setItem('econ:consent','denied')}catch(e){}")
        page = await ctx.new_page()
        await page.goto(BASE + '/', wait_until='networkidle')
        await page.click('.hero .btn-glass')
        await page.wait_for_timeout(1500)
        top = await page.evaluate("Math.round(document.getElementById('services').getBoundingClientRect().top)")
        results.append(('explore services', page.url, 'services top in viewport', top))
        await page.goto(BASE + '/blog/', wait_until='networkidle')
        await page.click('.filter[data-filter="compliance"]')
        await page.wait_for_timeout(400)
        vis = await page.evaluate("[...document.querySelectorAll('.post-grid .post-card')].filter(c => getComputedStyle(c).display !== 'none').length")
        feat = await page.evaluate("getComputedStyle(document.querySelector('.featured-post')).display")
        results.append(('blog filter compliance', 'cards shown', vis, 'featured', feat, page.url))
        await page.screenshot(path=f'{S}/blog-filter.png')
        await page.goto(BASE + '/blog/#renewables', wait_until='networkidle')
        await page.wait_for_timeout(300)
        vis = await page.evaluate("[...document.querySelectorAll('.post-grid .post-card')].filter(c => getComputedStyle(c).display !== 'none').length")
        results.append(('blog hash renewables', 'cards shown', vis))
        await page.click('.filter[data-filter="all"]')
        await page.wait_for_timeout(300)
        vis = await page.evaluate("[...document.querySelectorAll('.post-grid .post-card')].filter(c => getComputedStyle(c).display !== 'none').length")
        results.append(('blog all', 'cards shown (latest is featured above)', vis, page.url))
        # WhatsApp tip on hover
        await page.hover('.chat-float')
        await page.wait_for_timeout(500)
        await page.screenshot(path=f'{S}/whatsapp.png', clip={'x': 1100, 'y': 760, 'width': 340, 'height': 140})
        await ctx.close()

        # 7. hero and menu on a phone
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
        await ctx.add_init_script("try{localStorage.setItem('econ:consent','denied')}catch(e){}")
        page = await ctx.new_page()
        await page.goto(BASE + '/', wait_until='networkidle')
        await page.wait_for_timeout(1600)
        await page.screenshot(path=f'{S}/m-hero.png')
        await page.click('.menu-toggle')
        await page.wait_for_timeout(900)
        await page.screenshot(path=f'{S}/m-menu.png')
        await ctx.close()
        await b.close()
    for r in results:
        print(*r)

asyncio.run(main())
