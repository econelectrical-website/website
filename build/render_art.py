"""Renders the home energy illustration to image files (CTA background and social share image)."""
import asyncio
import json
import os

from PIL import Image
from playwright.async_api import async_playwright

from illustration import VIEW, home_energy_svg

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '_assets', 'assets', 'img', 'residential')
FONT = os.path.join(HERE, '_assets', 'assets', 'fonts', 'manrope-latin-wght.woff2')


async def shot(page, svg, w, h, path):
    html = ('<html><head><style>@font-face{font-family:"Manrope Local";src:url("file://%s") format("woff2");font-weight:200 800;}'
            'html,body{margin:0;background:#000}svg{display:block;width:%dpx;height:%dpx}'
            '*{animation:none!important}</style></head><body>%s</body></html>') % (FONT, w, h, svg)
    await page.set_viewport_size({'width': w, 'height': h})
    await page.set_content(html)
    await page.wait_for_timeout(500)
    await page.screenshot(path=path)


async def main():
    os.makedirs(OUT, exist_ok=True)
    art = home_energy_svg(labels=False, pid='ra', cls='ra')
    og = art.replace('<svg ', '<svg preserveAspectRatio="xMidYMid slice" ', 1)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page()
        tmp = os.path.join(OUT, '_art.png')
        await shot(page, art, 1920, round(1920 * VIEW[3] / VIEW[2]), tmp)
        im = Image.open(tmp).convert('RGB')
        variants = []
        for w in (960, 1920):
            h = round(im.height * w / im.width)
            path = 'assets/img/residential/home-energy-art-%d.webp' % w
            (im.resize((w, h), Image.LANCZOS) if w != im.width else im).save(os.path.join(HERE, '_assets', path), 'WEBP', quality=82, method=6)
            variants.append({'path': path, 'w': w, 'h': h})
        os.remove(tmp)
        await shot(page, og, 1200, 630, os.path.join(OUT, '_og.png'))
        Image.open(os.path.join(OUT, '_og.png')).convert('RGB').save(os.path.join(OUT, 'home-energy-og.jpg'), quality=86, optimize=True, progressive=True)
        os.remove(os.path.join(OUT, '_og.png'))
        await b.close()
    m = json.load(open(os.path.join(HERE, '_assets', 'media.json')))
    m['images']['home-energy-art'] = {'variants': variants, 'src_old': 'illustration.py'}
    m['images']['home-energy-og'] = {'variants': [{'path': 'assets/img/residential/home-energy-og.jpg', 'w': 1200, 'h': 630}], 'src_old': 'illustration.py'}
    json.dump(m, open(os.path.join(HERE, '_assets', 'media.json'), 'w'), indent=1)
    print(variants)


if __name__ == '__main__':
    asyncio.run(main())
