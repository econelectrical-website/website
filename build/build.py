"""Static site generator for econelectrical.co.uk (version 2, premium design).

python3 build.py  ->  dist/site     the real website: clean URLs, Netlify form, Google map, analytics
                      dist/preview  the same pages with file links for the private preview
"""
import datetime
import hashlib
import html
import json
import math
import os
import re
import shutil
import subprocess

import markdown
from PIL import Image

from illustration import home_energy_svg
from landing_pages import LANDING, LANDING_ORDER, OFFER_LINKS, PROJECT_SERVICE, RESIDENTIAL
from site_content import (ABOUT_PARAS, AREAS, CATEGORIES, CTA_DEFAULT, FEATURED_PROJECTS, HOME, POSTS, PRIVACY,
                          PROJECT_ORDER, PROJECTS, RETIRED_POSTS, SERVICE_ORDER, SERVICES, SITE, TEAM)

HERE = os.path.dirname(os.path.abspath(__file__))
ASSET_SRC = os.path.join(HERE, '_assets')
MANIFEST = json.load(open(os.path.join(ASSET_SRC, 'media.json')))
MAP = json.load(open(os.path.join(ASSET_SRC, 'map.json')))
ICONS = json.load(open(os.path.join(HERE, 'icons.json')))
ICONS['plus'] = '<path d="M5 12h14" /> <path d="M12 5v14" />'
YEAR = datetime.date.today().year
BUILD_DATE = datetime.date.today().isoformat()
FONTS = 'https://fonts.googleapis.com/css2?family=Manrope:wght@200..800&family=Outfit:wght@100..900&display=swap'
GMAP = ('https://www.google.com/maps?q=Econ%20Electrical%2C%20The%20Courtyard%2C%20225%20Denby%20Dale%20Road%2C'
        '%20Wakefield%20WF2%207AJ&z=15&output=embed')
CONTACT = '/contact-us-wakefield-electricians/'

# ---------------------------------------------------------------- design data
SERVICE_ICON = {'electrical-installation': 'zap', 'renewables': 'sun', 'compliance': 'shield-check'}
SERVICE_BLURB = {
    'electrical-installation': 'Turnkey projects, subcontract support and planned and reactive maintenance.',
    'renewables': 'Solar PV, battery storage and EV charging, designed and installed under one roof.',
    'compliance': 'EICR and fixed wire testing, thermal imaging, PAT testing and emergency lighting.',
}
SERVICE_CHIPS = {
    'renewables': ['Solar PV', 'Battery Storage', 'EV Charging'],
    'electrical-installation': ['Installations', 'Maintenance', 'Subcontract'],
    'compliance': ['EICR Testing', 'Thermal Imaging', 'PAT Testing'],
}
FEATURE_ICON = {
    'Turnkey Delivery': 'layers', 'Commercial Experience': 'building-2', 'Maintenance Support': 'wrench',
    'Fully Compliant': 'shield-check', 'Commercial Specialists': 'factory', 'Highly Certified': 'badge-check',
    'Futureproof Systems': 'leaf', 'Complete Project Delivery': 'route', 'NICEIC Approved': 'badge-check',
    'Detailed Reporting': 'file-text', 'Risk Reduction': 'shield-check',
}
OFFER_ICON = {
    'Turnkey Electrical Solutions': 'layers', 'Sub Contract Partnership': 'handshake',
    'Planned Preventative Maintenance (PPM)': 'calendar-check', 'Reactive Maintenance': 'timer',
    'Solar PV Installation': 'sun', 'Battery Storage': 'battery-charging', 'EV Charging Installation': 'plug-zap',
    'Electrical Testing': 'clipboard-check', 'Thermal Imaging': 'thermometer', 'PAT Testing': 'plug',
    'Emergency Lighting': 'lightbulb',
}
PROCESS_ICON = {'Consult': 'users', 'Design': 'circuit-board', 'Install': 'hard-hat', 'Support': 'shield-check',
                'Inspect': 'scan-search', 'Report': 'file-text'}
HERO_SHORT = {'Planned Preventative Maintenance (PPM)': 'PPM'}
CTA_IMAGE = {'home': 'renewables-hero', 'electrical-installation': 'home-about-site', 'renewables': 'renewables-ev',
             'compliance': 'installation-ppm', 'about': 'renewables-hero', 'projects': 'home-about-site',
             'blog': 'renewables-solar', 'industrial-electrical-contractors': 'card-swan',
             'commercial-ev-charging-installation': 'busdepot-2', 'commercial-solar-pv-installation': 'renewables-hero',
             'eicr-fixed-wire-testing': 'compliance-hero', 'commercial-led-lighting': 'home-cta-warehouse',
             'home-solar-battery-installation': 'home-energy-art'}
TRUST = [
    ('badge-check', 'NICEIC Approved', 'Approved contractor, with MCS and SafeContractor accreditation.'),
    ('factory', 'Commercial & Industrial Focus', 'Electrical solutions tailored to commercial, industrial and public sector environments.'),
    ('shield-check', 'Compliance Assured', 'Testing, certification and installations delivered to recognised industry standards.'),
    ('navigation', 'Nationwide Capability', 'Yorkshire based, providing reliable electrical solutions for projects nationwide.'),
]
SECTORS = [
    ('factory', 'Manufacturing', 'Machine power, production line installations and factory lighting, planned around your shifts.',
     'Cummins Turbo Technologies', '/cummins-turbo-technologies/'),
    ('warehouse', 'Warehousing & Distribution', 'High bay LED lighting, power and containment for large, busy buildings.',
     'Saint Flooring Group', '/saint-flooring-group/'),
    ('hard-hat', 'Industrial Units & Workshops', 'Complete fit outs for new and refurbished units, from design through to certification.',
     'Swan Civil Engineering', '/swan-civil-engineering/'),
    ('landmark', 'Public Sector', 'Councils, schools and public buildings, with work planned around the people using them.',
     'Schools and councils', '/electrical-contractors-for-schools-councils-and-public-buildings/'),
    ('building-2', 'Offices & Commercial', 'Testing, maintenance, lighting and power upgrades for working offices and commercial premises.',
     'Compliance services', '/compliance/'),
    ('handshake', 'Main Contractors', 'Dependable electrical subcontract support on commercial and industrial builds.',
     'Subcontract partnership', '/electrical-installation/#sub-contract-partnership'),
]
# Derived, not hand listed: the menus show the featured projects, so the thumbnails
# follow whatever FEATURED_PROJECTS holds and cannot fall out of step with it.
MENU_THUMBS = (['installation-turnkey', 'renewables-solar', 'compliance-testing']
               + [PROJECTS[s]['card'] for s in FEATURED_PROJECTS])
SERVICE_THUMB = {'electrical-installation': 'installation-turnkey', 'renewables': 'renewables-solar',
                 'compliance': 'compliance-testing'}


def e(s):
    return html.escape(str(s), quote=True)


def icon(name, cls='i'):
    return ('<svg class="%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>') % (cls, ICONS[name])


def arrow():
    return icon('arrow-right')


class Ctx:
    def __init__(self, mode, path):
        self.mode = mode
        self.path = path
        self.depth = 0 if path == '/' else path.strip('/').count('/') + 1
        # Filled in by crumbs() while the body is built, read back by document() to
        # emit the matching BreadcrumbList. Kept here rather than passed around so the
        # markup can never describe a different trail from the one on the page.
        self.trail = None

    def u(self, target):
        if target.startswith(('http', 'tel:', 'mailto:')):
            return target
        frag = ''
        if '#' in target:
            target, frag = target.split('#', 1)
            frag = '#' + frag
        if self.mode == 'site':
            return target + frag
        prefix = '../' * self.depth
        if target in ('', '/'):
            return prefix + 'index.html' + frag
        return prefix + target.strip('/') + '/index.html' + frag

    def a(self, asset):
        return '/' + asset if self.mode == 'site' else '../' * self.depth + asset

    def current(self, target):
        return ' aria-current="page"' if target == self.path else ''


def img(ctx, key, alt, sizes='100vw', cls='', eager=False):
    vs = MANIFEST['images'][key]['variants']
    big = vs[-1]
    attrs = ['src="%s"' % ctx.a(vs[0]['path'])]
    if len(vs) > 1:
        attrs.append('srcset="%s"' % ', '.join('%s %dw' % (ctx.a(v['path']), v['w']) for v in vs))
        attrs.append('sizes="%s"' % sizes)
    attrs.append('width="%d" height="%d"' % (big['w'], big['h']))
    attrs.append('alt="%s"' % e(alt))
    if cls:
        attrs.append('class="%s"' % cls)
    attrs.append('loading="eager" fetchpriority="high"' if eager else 'loading="lazy"')
    attrs.append('decoding="async"')
    return '<img %s>' % ' '.join(attrs)


def thumb(ctx, key, alt):
    return '<img src="%s" width="480" height="%d" alt="%s" loading="lazy" decoding="async">' % (
        ctx.a('assets/img/thumbs/%s-480.webp' % key), THUMB_H[key], e(alt))


def logo_img(ctx, key, alt):
    v = MANIFEST['images'][key]['variants'][0]
    return '<img src="%s" width="%d" height="%d" alt="%s" loading="lazy" decoding="async">' % (
        ctx.a(v['path']), v['w'], v['h'], e(alt))


def full_src(ctx, key):
    return ctx.a(MANIFEST['images'][key]['variants'][-1]['path'])


_HASHED = {}


def hashed_asset(rel):
    """Published path for an asset, with a hash of its contents in the filename.

    A video keeps the same name from one encode to the next and is cached hard, so a
    better cut published under the old name is invisible to anyone holding the old
    one. That is not hypothetical: after the hero was re-encoded, everyone who had
    visited that week carried on being shown the superseded file, Jonathan included.

    Eight characters of the content hash make a changed file a different address, so
    a stale copy cannot be served at all, and the cache lifetime can safely go up to
    a year instead of a week. Applied to the video folder, which holds the clips and
    their poster frames: those are the files that get replaced in place.
    """
    if rel not in _HASHED:
        with open(os.path.join(ASSET_SRC, rel), 'rb') as f:
            h = hashlib.sha256(f.read()).hexdigest()[:8]
        stem, ext = os.path.splitext(rel)
        _HASHED[rel] = '%s.%s%s' % (stem, h, ext)
    return _HASHED[rel]


def hash_video_assets():
    """Hash every file in the video folder up front, before anything is copied."""
    d = os.path.join(ASSET_SRC, 'assets', 'video')
    for f in sorted(os.listdir(d)):
        if not f.startswith('.'):
            hashed_asset('assets/video/' + f)


def video_tag(ctx, name, alt):
    """A background video that loads the cut suited to the screen it is on.

    The source is handed over in data attributes rather than a src, and site.js picks
    between the desktop and phone files once it knows the viewport. The obvious markup
    for this, two sources with a media attribute, does not work: Chromium ignores
    media on a video source and serves the desktop file to a 390px phone, which was
    verified rather than assumed. Script is the only thing that actually decides.

    preload="none" so nothing is fetched before that choice is made. With JavaScript
    off the poster simply stays, which is the video's own first frame, so the hero
    still looks right; it just does not move.
    """
    w, h = video_dims(name)
    mobile = 'assets/video/%s-m.mp4' % name
    attrs = ['data-src="%s"' % ctx.a(hashed_asset('assets/video/%s.mp4' % name))]
    if os.path.exists(os.path.join(ASSET_SRC, mobile)):
        attrs.append('data-src-mobile="%s"' % ctx.a(hashed_asset(mobile)))
    return ('<video autoplay muted loop playsinline preload="none" width="%d" height="%d" '
            'poster="%s" %s aria-label="%s"></video>') % (
        w, h, ctx.a(hashed_asset('assets/video/%s-poster.webp' % name)), ' '.join(attrs), e(alt))


_VIDEO_DIMS = {}


def video_dims(name):
    """Real pixel size of a clip, read from the file rather than written out here.

    These two numbers set the box the browser reserves before the video has loaded.
    Hard coded, they go stale the moment a clip is re-encoded at another size, and
    the page then reserves the wrong shape and shifts as the video arrives. That had
    already happened once: the hero was still declared 1280x960 after it was cropped
    to 1280x916. Reading the file keeps the markup honest for free.
    """
    if name not in _VIDEO_DIMS:
        path = os.path.join(ASSET_SRC, 'assets', 'video', name + '.mp4')
        try:
            out = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                                  '-show_entries', 'stream=width,height,sample_aspect_ratio',
                                  '-of', 'csv=p=0:s=,', path],
                                 capture_output=True, text=True, check=True).stdout.strip()
            parts = out.split(',')
            w, h = int(parts[0]), int(parts[1])
            # Honour a non-square pixel aspect. Our own encodes square the pixels, so
            # this is normally 1:1, but a file dropped in from elsewhere may not be,
            # and declaring its stored size would then reserve the wrong shape.
            sar = parts[2] if len(parts) > 2 else ''
            if ':' in sar and sar != 'N/A':
                num, den = (int(x) for x in sar.split(':'))
                if num and den:
                    w = round(w * num / den)
        except Exception:
            # No ffmpeg on this machine, or the clip is missing. 16:9 is a safer guess
            # than nothing: the box is reserved, and a wrong ratio only costs a shift.
            w, h = 1280, 720
        _VIDEO_DIMS[name] = (w, h)
    return _VIDEO_DIMS[name]


def abs_img(key):
    return SITE['domain'] + '/' + MANIFEST['images'][key]['variants'][-1]['path']


def brand_logo(ctx, height, cls=''):
    w = round(MANIFEST['logo']['w'] * height / MANIFEST['logo']['h'])
    return '<img%s src="%s" srcset="%s 1x, %s 2x" width="%d" height="%d" alt="Econ Electrical">' % (
        ' class="%s"' % cls if cls else '', ctx.a('assets/img/brand/econ-logo-160.png'),
        ctx.a('assets/img/brand/econ-logo-160.png'), ctx.a('assets/img/brand/econ-logo-320.png'), w, height)


def ext(href, inner, cls='', label=None):
    return '<a%s href="%s" target="_blank" rel="noopener"%s>%s</a>' % (
        ' class="%s"' % cls if cls else '', e(href), ' aria-label="%s"' % e(label) if label else '', inner)


def btn(href, text, kind='primary', size='', icon_name='arrow-right', attrs=''):
    cls = 'btn btn-%s%s' % (kind, ' btn-' + size if size else '')
    return '<a class="%s" href="%s"%s>%s<span class="btn-ico">%s</span></a>' % (cls, href, attrs, e(text), icon(icon_name))


def eyebrow(text):
    return '<p class="eyebrow">%s</p>' % e(text)


def words(text, start=0):
    out = []
    for i, w in enumerate(text.split()):
        out.append('<span class="w"><span style="--i:%d">%s</span></span>' % (start + i, e(w)))
    return ' '.join(out), start + len(text.split())


def initials(name):
    return ''.join(p[0] for p in name.split()[:2]).upper()


def read_time(md):
    return max(2, math.ceil(len(re.findall(r'\w+', md)) / 220))


def nice_date(iso):
    d = datetime.date.fromisoformat(iso)
    return '%d %s %d' % (d.day, d.strftime('%B'), d.year)


def project_key(slug, i):
    return '%s-%d' % (PROJECTS[slug]['media'], i)


SECTOR_ICON = {'Industrial': 'factory', 'Public Sector': 'landmark', 'Commercial': 'building-2',
               'Transport': 'route'}


def sector_icon(p):
    return SECTOR_ICON.get(p['type'], 'building-2')


def project_card_alt(p):
    if p['card'].startswith(p['media'] + '-'):
        return p['alts'][int(p['card'].rsplit('-', 1)[1]) - 1]
    return '%s project by Econ Electrical' % p['name']


# ---------------------------------------------------------------- layout

def header(ctx):
    in_services = ctx.path.strip('/') in SERVICE_ORDER or ctx.path.strip('/') in LANDING
    in_projects = ctx.path.strip('/') in PROJECT_ORDER or ctx.path.startswith('/projects/')
    in_blog = ctx.path == '/blog/' or ctx.path.strip('/') in [p['slug'] for p in POSTS]
    svc_cards = ''.join('''
          <a class="mega-card" href="{href}"{cur}>
            <span class="ph">{img}</span>
            <span class="body"><h4>{name}</h4><p>{blurb}</p></span>
          </a>'''.format(href=ctx.u('/%s/' % k), cur=ctx.current('/%s/' % k),
                         img=thumb(ctx, SERVICE_THUMB[k], SERVICES[k]['name']), name=e(SERVICES[k]['name']),
                         blurb=e(SERVICE_BLURB[k])) for k in SERVICE_ORDER)
    proj_cards = ''.join('''
          <a class="mega-card" href="{href}"{cur}>
            <span class="ph">{img}</span>
            <span class="body"><h4>{name}</h4><span class="meta">{pin}{loc} &middot; {type}</span></span>
          </a>'''.format(href=ctx.u('/%s/' % k), cur=ctx.current('/%s/' % k),
                         img=thumb(ctx, PROJECTS[k]['card'], PROJECTS[k]['name']), name=e(PROJECTS[k]['name']),
                         pin=icon('map-pin'), loc=e(PROJECTS[k].get('location') or PROJECTS[k]['type']),
                         type=e(PROJECTS[k]['type']))
        for k in FEATURED_PROJECTS)
    # A fifth tile the same size as the four above it, rather than the small text link
    # that used to sit in the foot. The menu shows the pick of the work, and the way
    # through to the rest should look like one of the choices, not like a footnote.
    proj_cards += '''
          <a class="mega-card more" href="{href}"{cur}>
            <span class="ph"><span class="more-ph">{icon}</span></span>
            <span class="body"><h4>More Projects</h4><span class="meta">All {n} projects &middot; filter by sector</span></span>
          </a>'''.format(href=ctx.u('/projects/'), cur=ctx.current('/projects/'),
                         icon=icon('layers'), n=len(PROJECT_ORDER))
    m_services = ''.join('<a href="%s">%s<span>%s</span></a>' % (ctx.u('/%s/' % k), e(SERVICES[k]['name']), e(', '.join(SERVICE_CHIPS[k])))
                         for k in SERVICE_ORDER)
    m_projects = ''.join('<a href="%s">%s<span>%s</span></a>' % (ctx.u('/%s/' % k), e(PROJECTS[k]['name']),
                                                                 e(PROJECTS[k].get('location') or PROJECTS[k]['type']))
                         for k in FEATURED_PROJECTS)
    m_projects += '<a href="%s">More Projects<span>All %d projects</span></a>' % (ctx.u('/projects/'), len(PROJECT_ORDER))
    return f'''
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="topbar">
    <div class="container topbar-inner">
      <div class="topbar-group">
        <a href="tel:{SITE['phone_href']}">{icon('phone')}{SITE['phone']}</a>
        <a href="mailto:{SITE['email']}">{icon('mail')}{SITE['email']}</a>
        <span>{icon('map-pin')}Wakefield, West Yorkshire</span>
      </div>
      <div class="topbar-group">
        <span>{icon('badge-check')}NICEIC Approved Contractor</span>
        {ext(SITE['linkedin'], 'LinkedIn')}{ext(SITE['instagram'], 'Instagram')}{ext(SITE['facebook'], 'Facebook')}
      </div>
    </div>
  </div>
  <div class="mainbar">
    <div class="container mainbar-inner">
      <a class="brand" href="{ctx.u('/')}" aria-label="Econ Electrical home">{brand_logo(ctx, 112)}</a>
      <nav class="nav" aria-label="Main">
        <ul class="nav-list">
          <li class="nav-item"><a class="nav-link" href="{ctx.u('/about-us/')}"{ctx.current('/about-us/')}>About Us</a></li>
          <li class="nav-item has-mega{' is-current' if in_services else ''}">
            <button class="nav-link" type="button" aria-expanded="false" aria-controls="mega-services">Services {icon('chevron-down')}</button>
            <div class="mega" id="mega-services">
              <div class="container mega-inner mega-services">{svc_cards}
                <div class="mega-aside">
                  <div class="copy"><p class="eyebrow">Project enquiries</p><p>Not sure what you need? Talk it through with our team and we&rsquo;ll point you in the right direction.</p></div>
                  <a class="big" href="tel:{SITE['phone_href']}">{SITE['phone']}</a>
                  {btn(ctx.u(CONTACT), 'Enquire Now', size='sm')}
                </div>
              </div>
            </div>
          </li>
          <li class="nav-item has-mega{' is-current' if in_projects else ''}">
            <button class="nav-link" type="button" aria-expanded="false" aria-controls="mega-projects">Projects {icon('chevron-down')}</button>
            <div class="mega" id="mega-projects">
              <div class="container mega-inner mega-projects">{proj_cards}
                <div class="mega-foot"><span>Commercial and industrial installations across the North and beyond.</span></div>
              </div>
            </div>
          </li>
          <li class="nav-item"><a class="nav-link" href="{ctx.u('/blog/')}"{' aria-current="page"' if in_blog else ''}>Blog</a></li>
          <li class="nav-item"><a class="nav-link" href="{ctx.u(CONTACT)}"{ctx.current(CONTACT)}>Contact Us</a></li>
        </ul>
      </nav>
      <div class="header-actions">
        <a class="header-call" href="tel:{SITE['phone_href']}" aria-label="Call {SITE['phone']}"><span class="ring">{icon('phone')}</span><span class="txt"><small>Call us</small><b>{SITE['phone']}</b></span></a>
        {btn(ctx.u(CONTACT), 'Enquire Now', size='sm')}
        <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="mobile-nav"><span class="bars" aria-hidden="true"><span></span></span>Menu</button>
      </div>
    </div>
  </div>
  <div class="mobile-nav" id="mobile-nav">
    <a class="m-link m-anim" style="--i:0" href="{ctx.u('/')}">Home {arrow()}</a>
    <a class="m-link m-anim" style="--i:1" href="{ctx.u('/about-us/')}">About Us {arrow()}</a>
    <div class="m-group m-anim" style="--i:2"><p class="label">Services</p>{m_services}</div>
    <div class="m-group m-anim" style="--i:3"><p class="label">Projects</p>{m_projects}<a href="{ctx.u('/projects/')}">All Projects<span>{icon('arrow-right')}</span></a></div>
    <a class="m-link m-anim" style="--i:4" href="{ctx.u('/blog/')}">Blog {arrow()}</a>
    <a class="m-link m-anim" style="--i:5" href="{ctx.u(CONTACT)}">Contact Us {arrow()}</a>
    <div class="m-actions m-anim" style="--i:6">
      {btn(ctx.u(CONTACT), 'Enquire Now')}
      {btn('tel:' + SITE['phone_href'], 'Call ' + SITE['phone'], 'glass', icon_name='phone')}
    </div>
    <div class="m-contact m-anim" style="--i:7"><span>Email <a href="mailto:{SITE['email']}">{SITE['email']}</a></span><span>The Courtyard, 225 Denby Dale Road, Wakefield, WF2 7AJ</span></div>
  </div>
</header>'''


def footer(ctx):
    svc = ''.join('<li><a href="%s">%s</a></li>' % (ctx.u('/%s/' % k), e(SERVICES[k]['name'])) for k in SERVICE_ORDER)
    svc += ''.join('<li class="sub"><a href="%s">%s</a></li>' % (ctx.u('/%s/' % k), e(LANDING[k]['name'])) for k in LANDING_ORDER)
    svc += '<li class="sub"><a href="%s">%s</a></li>' % (ctx.u('/%s/' % RESIDENTIAL['slug']), e(RESIDENTIAL['name']))
    return f'''
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-brand">
      <a href="{ctx.u('/')}" aria-label="Econ Electrical home">{brand_logo(ctx, 104, 'logo')}</a>
      <p>{e(SITE['tagline'])} Commercial electrical installation, renewables and compliance from Wakefield, across the UK.</p>
      <div class="footer-accred">{logo_img(ctx, 'logo-niceic', 'NICEIC Approved Contractor')}{logo_img(ctx, 'logo-mcs', 'MCS certified')}{logo_img(ctx, 'logo-safecontractor', 'SafeContractor approved')}</div>
    </div>
    <div class="footer-col">
      <h4>Services</h4>
      <ul>{svc}</ul>
    </div>
    <div class="footer-col">
      <h4>Company</h4>
      <ul>
        <li><a href="{ctx.u('/about-us/')}">About Us</a></li>
        <li><a href="{ctx.u('/projects/')}">Projects</a></li>
        <li><a href="{ctx.u('/blog/')}">Blog</a></li>
        <li><a href="{ctx.u(CONTACT)}">Contact Us</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Contact</h4>
      <ul>
        <li>{icon('map-pin')}<address>{e(SITE['legal'])}<br>{'<br>'.join(e(x) for x in SITE['address'])}</address></li>
        <li>{icon('phone')}<a href="tel:{SITE['phone_href']}">{SITE['phone']}</a></li>
        <li>{icon('mail')}<a href="mailto:{SITE['email']}">{SITE['email']}</a></li>
      </ul>
      <div class="socials" style="margin-top:22px">{ext(SITE['google_profile'], 'Google Reviews')}{ext(SITE['linkedin'], 'LinkedIn')}{ext(SITE['instagram'], 'Instagram')}{ext(SITE['facebook'], 'Facebook')}</div>
    </div>
  </div>
  <div class="container footer-bottom">
    <span>&copy; {YEAR} {e(SITE['legal'])}. All rights reserved.</span>
    <span class="legal"><a href="{ctx.u('/privacy-notice/')}" data-privacy-link>Privacy Notice</a><button type="button" data-cookie-settings>Cookie Settings</button></span>
    <span>{e(SITE['area_line'])}</span>
  </div>
  <img class="footer-mark" src="{ctx.a('assets/img/brand/icon-512.png')}" width="512" height="512" alt="" loading="lazy">
</footer>
{ext(SITE['whatsapp_href'], icon('messages-square') + '<span class="tip" aria-hidden="true">WhatsApp us</span>', 'chat-float', 'Message us on WhatsApp')}'''


def org_jsonld():
    return {
        '@context': 'https://schema.org', '@type': 'Electrician', '@id': SITE['domain'] + '/#business',
        'name': SITE['legal'], 'url': SITE['domain'] + '/',
        'logo': SITE['domain'] + '/assets/img/brand/econ-logo-320.png',
        'image': SITE['domain'] + '/assets/img/brand/econ-social-card.jpg',
        'telephone': '+44 1924 677085', 'email': SITE['email'],
        'address': {'@type': 'PostalAddress', 'streetAddress': 'The Courtyard, 225 Denby Dale Road',
                    'addressLocality': 'Wakefield', 'addressRegion': 'West Yorkshire', 'postalCode': 'WF2 7AJ',
                    'addressCountry': 'GB'},
        'geo': {'@type': 'GeoCoordinates', 'latitude': MAP['lat'], 'longitude': MAP['lon']},
        'areaServed': ['Wakefield', 'West Yorkshire', 'United Kingdom'],
        'hasMap': SITE['google_profile'],
        'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': SITE['hours']['days'],
                                       'opens': SITE['hours']['opens'], 'closes': SITE['hours']['closes']}],
        'sameAs': [SITE['google_profile'], SITE['facebook'], SITE['instagram'], SITE['linkedin']],
    }


def document(ctx, meta, body, preview_main=False):
    canonical = SITE['domain'] + meta['path']
    og_image = meta.get('image') or SITE['domain'] + '/assets/img/brand/econ-social-card.jpg'
    robots = 'noindex, follow' if meta.get('noindex') else 'index, follow, max-image-preview:large'
    head = [
        '<meta name="description" content="%s">' % e(meta['description']),
        '<link rel="canonical" href="%s">' % canonical,
        '<meta name="robots" content="%s">' % robots,
        '<meta property="og:locale" content="en_GB">',
        '<meta property="og:site_name" content="Econ Electrical">',
        '<meta property="og:type" content="%s">' % meta.get('og_type', 'website'),
        '<meta property="og:title" content="%s">' % e(meta['title']),
        '<meta property="og:description" content="%s">' % e(meta['description']),
        '<meta property="og:url" content="%s">' % canonical,
        '<meta property="og:image" content="%s">' % og_image,
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="theme-color" content="#000000">',
        '<link rel="icon" type="image/png" sizes="32x32" href="%s">' % ctx.a('assets/img/brand/favicon-32.png'),
        '<link rel="apple-touch-icon" href="%s">' % ctx.a('assets/img/brand/apple-touch-icon.png'),
        '<link rel="preload" href="%s" as="font" type="font/woff2" crossorigin>' % ctx.a('assets/fonts/outfit-latin-wght.woff2'),
        '<link rel="preload" href="%s" as="font" type="font/woff2" crossorigin>' % ctx.a('assets/fonts/manrope-latin-wght.woff2'),
    ]
    if ctx.mode == 'preview':
        head.append('<link rel="stylesheet" href="%s">' % FONTS)
    head.append('<link rel="stylesheet" href="%s">' % ctx.a('assets/site.css'))
    head.append('<script>document.documentElement.classList.add("js");setTimeout(function(){if(!window.__econReady)document.documentElement.classList.remove("js")},2500)</script>')
    if meta['path'] == '/':
        head.append('<meta name="google-site-verification" content="%s">' % SITE['google_verification'])
    blocks = list(meta.get('jsonld', []))
    crumb = breadcrumb_ld(ctx)
    if crumb:
        blocks.append(crumb)
    for block in blocks:
        head.append('<script type="application/ld+json">%s</script>' % json.dumps(block, ensure_ascii=False))
    if ctx.mode == 'site':
        # Google Analytics only loads once the visitor has accepted cookies (see the cookie bar in site.js)
        head.append(("<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
                     "window.econAnalytics=function(){if(window.__econGA)return;window.__econGA=1;"
                     "var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id=%s';"
                     "document.head.appendChild(s);gtag('js',new Date());gtag('config','%s');};"
                     "try{if(localStorage.getItem('econ:consent')==='granted')window.econAnalytics();}catch(e){}</script>") % (SITE['ga4'], SITE['ga4']))
    page = '<span class="top-marker" aria-hidden="true"></span>' + header(ctx) + '\n<main id="main">\n' + body + '\n</main>\n' + footer(ctx) + \
        '\n<script src="%s" defer></script>\n' % ctx.a('assets/site.js')
    if preview_main:
        return '<title>Econ Electrical Website</title>\n' + '\n'.join(head) + '\n' + page
    return ('<!doctype html>\n<html lang="en-GB">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<title>%s</title>\n%s\n</head>\n<body>\n%s</body>\n</html>\n') % (e(meta['title']), '\n'.join(head), page)


# ---------------------------------------------------------------- shared blocks

def crumbs(ctx, trail):
    ctx.trail = trail
    items = []
    for label, href in trail:
        items.append('<li><a href="%s">%s</a></li>' % (ctx.u(href), e(label)) if href else '<li>%s</li>' % e(label))
    return '<ol class="crumbs" aria-label="Breadcrumb">%s</ol>' % ''.join(items)


def breadcrumb_ld(ctx):
    """The visible trail, repeated for Google so it can show it under the result.

    Built from whatever crumbs() was handed, so there is nothing to keep in step by
    hand. The last crumb has no href, which is the current page, so it gets the
    canonical URL rather than being left without one.
    """
    if not ctx.trail:
        return None
    items = []
    for i, (label, href) in enumerate(ctx.trail, 1):
        items.append({'@type': 'ListItem', 'position': i, 'name': label,
                      'item': SITE['domain'] + (href if href else ctx.path)})
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': items}


def cta_band(ctx, key, kicker, heading, text, button='Get in Touch'):
    return f'''
<section class="section tight">
  <div class="container">
    <div class="cta-band" data-reveal>
      {img(ctx, CTA_IMAGE[key], '', '100vw')}
      <div class="inner">
        {eyebrow(kicker)}
        <h2>{e(heading)}</h2>
        <p>{e(text)}</p>
        <div class="btn-row">{btn(ctx.u(CONTACT), button)}<a class="btn btn-glass plain" href="tel:{SITE['phone_href']}">{icon('phone')}&nbsp;{SITE['phone']}</a></div>
      </div>
    </div>
  </div>
</section>'''


def logos_section(ctx, alt=False):
    return f'''
<section class="section tight{' section-alt' if alt else ''}">
  <div class="container">
    <div class="section-head center" data-reveal>
      {eyebrow('Partners & Accreditations')}
      <h2>Trusted by Leading Partners. Certified by Industry Experts.</h2>
    </div>
    <div class="logo-groups" data-reveal>
      <div class="logo-group"><p class="label">Technology Partners</p>
        <div class="logo-tiles" style="--n:2"><div class="logo-tile">{logo_img(ctx, 'logo-solax', 'Solax Power')}</div><div class="logo-tile">{logo_img(ctx, 'logo-schneider', 'Schneider Electric')}</div></div>
      </div>
      <div class="logo-group"><p class="label">Accreditations</p>
        <div class="logo-tiles" style="--n:3"><div class="logo-tile">{logo_img(ctx, 'logo-niceic', 'NICEIC Approved Contractor')}</div><div class="logo-tile">{logo_img(ctx, 'logo-mcs', 'MCS certified')}</div><div class="logo-tile">{logo_img(ctx, 'logo-safecontractor', 'SafeContractor approved')}</div></div>
      </div>
    </div>
  </div>
</section>'''


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


# A headline figure is written the way it reads ('55%', '50kW', '110'). The
# leading number is what counts up; whatever follows is the unit and is held
# back until the count lands, so it does not jitter while the digits change.
STAT = re.compile(r'^([\d.,]+)(.*)$')


def stat_block(results, style=''):
    if not results:
        return ''
    cells = []
    for value, label in results:
        m = STAT.match(value.strip())
        num, suffix = (m.group(1).replace(',', ''), m.group(2)) if m else ('', '')
        count = ' data-count="%s" data-suffix="%s"' % (num, e(suffix)) if num else ''
        cells.append('<div class="stat"><strong%s>%s</strong><span>%s</span></div>' % (count, e(value), e(label)))
    cls = 'stats n3' if len(cells) == 3 else 'stats'
    return '<div class="%s"%s>%s</div>' % (cls, style, ''.join(cells))


def project_card(ctx, slug, sizes='(max-width: 760px) 90vw, 33vw', heading='h3', cat=None, cls=''):
    p = PROJECTS[slug]
    return f'''<a class="proj-card{(' ' + cls) if cls else ''}"{' data-cat="%s"' % cat if cat else ''} href="{ctx.u('/%s/' % slug)}">
  {img(ctx, p['card'], project_card_alt(p), sizes)}
  <span class="go"><span class="svc-go">{icon('arrow-up-right')}</span></span>
  <span class="body">
    <{heading}>{e(p['name'])}</{heading}>
    <span class="chips">{'<span class="chip">%s%s</span>' % (icon('map-pin'), e(p['location'])) if p.get('location') else ''}<span class="chip">{icon(sector_icon(p))}{e(p['type'])}</span></span>
  </span>
</a>'''


def testimonials(ctx, heading_kicker='Customer Testimonials', heading='What Our Clients Say', alt=True):
    cards = ''.join(f'''
      <figure class="t-card">
        {icon('quote', 'i q')}
        <blockquote><p>{e(PROJECTS[s]['quote'])}</p></blockquote>
        <figcaption class="who"><span class="avatar" aria-hidden="true">{initials(PROJECTS[s]['quote_name'])}</span><span><strong>{e(PROJECTS[s]['quote_name'])}</strong><span>{e(PROJECTS[s]['quote_role'])}</span></span></figcaption>
      </figure>''' for s in PROJECT_ORDER if PROJECTS[s].get('quote'))
    return f'''
<section class="section{' section-alt' if alt else ''}" style="overflow:hidden;overflow:clip">
  <div class="glow" style="left:-20%;top:-30%"></div>
  <div class="container">
    <div class="section-head row" data-reveal>
      <div>{eyebrow(heading_kicker)}<h2>{e(heading)}</h2></div>
      {ext(SITE['google_profile'], 'Read Our Google Reviews <span class="circle">%s</span>' % icon('arrow-up-right'), 'link-arrow')}
    </div>
  </div>
  <div data-carousel data-reveal>
    <div class="carousel-track quotes-track">{cards}
    </div>
    <div class="container"><div class="head-tools" style="margin-top:28px"><button class="round-btn" type="button" data-prev aria-label="Previous testimonial">{icon('arrow-left')}</button><button class="round-btn" type="button" data-next aria-label="Next testimonial">{icon('arrow-right')}</button></div></div>
  </div>
</section>'''


def process_section(ctx, steps, alt=False):
    items = ''.join(f'''
      <li class="step">
        <span class="num">0{i}</span>
        <span class="ico-box">{icon(PROCESS_ICON.get(h, 'check'))}</span>
        <h3>{e(h)}</h3>
        <p>{e(p)}</p>
      </li>''' for i, (h, p) in enumerate(steps, 1))
    return f'''
<section class="section{' section-alt' if alt else ''}">
  <div class="container">
    <div class="section-head center" data-reveal>
      {eyebrow('Our Process')}
      <h2>A Straightforward Process from Start to Finish</h2>
    </div>
    <ol class="steps" data-stagger>{items}
    </ol>
  </div>
</section>'''


# ---------------------------------------------------------------- pages

def page_home(ctx):
    h1a, n = words(HOME['h1'])
    h1b, _ = words(HOME['h1_accent'], n)
    trust = ''.join(f'''
      <div class="trust-item"><span class="ico-box">{icon(ic)}</span><div><h3>{e(t)}</h3><p>{e(d)}</p></div></div>'''
                    for ic, t, d in TRUST)
    services = ''.join(f'''
      <a class="svc-card" href="{ctx.u('/%s/' % slug)}">
        {img(ctx, key, SERVICES[slug]['offers'][0]['alt'], '(max-width: 1000px) 100vw, 33vw')}
        <span class="svc-top"><span class="glass-ico">{icon(SERVICE_ICON[slug])}</span><span class="svc-go">{icon('arrow-up-right')}</span></span>
        <span class="svc-body">
          <h3>{e(name)}</h3>
          <p>{e(text)}</p>
          <span class="chips">{''.join('<span class="chip">%s</span>' % e(c) for c in SERVICE_CHIPS[slug])}</span>
        </span>
      </a>''' for slug, name, key, text, link in HOME['services'])
    sectors = ''.join(f'''
      <article class="sector">
        <span class="num">{i:02d}</span>
        <span class="ico-box">{icon(ic)}</span>
        <h3>{e(name)}</h3>
        <p>{e(text)}</p>
        <a class="sector-link" href="{ctx.u(href)}">{e(label)}{arrow()}</a>
      </article>''' for i, (ic, name, text, label, href) in enumerate(SECTORS, 1))
    statement_words = ('From initial advice to full project delivery, Econ Electrical is your trusted partner '
                       'for efficient and future proof electrical systems.').split()
    accent_from = statement_words.index('trusted')
    stmt = ' '.join('<span class="wd%s">%s</span>' % (' acc' if accent_from <= i <= accent_from + 1 else '', e(w))
                    for i, w in enumerate(statement_words))
    projects = ''.join(project_card(ctx, s) for s in FEATURED_PROJECTS)
    led = PROJECTS['led-lighting']
    body = f'''
<section class="hero" data-video>
  <div class="hero-media">
    {video_tag(ctx, 'econ-team-on-site', 'The Econ Electrical team at work on site')}
  </div>
  <div class="hero-shade"></div>
  <div class="grain"></div>
  <div class="container hero-inner">
    <div class="hero-copy">
      <p class="kicker fade-up" style="--d:.05s"><span class="pulse"></span>{e(HOME['eyebrow'])}</p>
      <h1 class="display words">{h1a} <span class="accent" style="display:block">{h1b}</span></h1>
      <p class="lead fade-up" style="--d:.75s">{e(HOME['lede'])}</p>
      <div class="btn-row fade-up" style="--d:.9s">{btn(ctx.u(CONTACT), 'Enquire Now')}{btn(ctx.u('/#services'), 'Explore Our Services', 'glass', icon_name='arrow-right')}</div>
    </div>
    <div class="hero-side fade-up" style="--d:1.1s">
      <button class="video-toggle" type="button" aria-label="Pause background video">{icon('pause', 'i i-pause')}{icon('play', 'i i-play')}<span class="txt">Pause</span></button>
      <a class="scroll-cue" href="{ctx.u('/#intro')}"><span class="rail"></span>Scroll</a>
    </div>
  </div>
</section>

<section class="trust" id="intro" aria-label="Why Econ Electrical">
  <div class="container trust-grid" data-stagger>{trust}
  </div>
</section>

<section class="section">
  <div class="container about-grid">
    <div class="about-media" data-reveal>
      <figure class="am-main">{img(ctx, 'home-about-site', 'Econ Electrical engineer installing new switchgear on site', '(max-width: 960px) 100vw, 45vw')}</figure>
      <figure class="am-sub">{img(ctx, 'about-vans', 'Econ Electrical branded electric vans', '(max-width: 960px) 50vw, 22vw')}</figure>
      <div class="am-badge"><span class="ico-box">{icon('users')}</span><strong>One team, start to finish</strong><span>Design, installation, testing and certification, all handled in house.</span></div>
    </div>
    <div class="about-copy" data-reveal>
      {eyebrow('About Econ Electrical')}
      <h2>Powering Businesses for a <span class="accent">Better Future</span></h2>
      <div class="copy">{''.join('<p>%s</p>' % e(p) for p in ABOUT_PARAS[:2])}</div>
      <div class="mini-logos">{logo_img(ctx, 'logo-niceic', 'NICEIC Approved Contractor')}{logo_img(ctx, 'logo-mcs', 'MCS certified')}{logo_img(ctx, 'logo-safecontractor', 'SafeContractor approved')}</div>
      <div class="btn-row">{btn(ctx.u('/about-us/'), 'Learn More About Us')}</div>
    </div>
  </div>
</section>

<section class="section section-alt tight">
  <div class="container">
    <p class="statement statement-xl" data-highlight>{stmt}</p>
  </div>
</section>

<section class="section" id="services">
  <div class="container">
    <div class="section-head row" data-reveal>
      <div>{eyebrow('Our Services')}<h2>Complete Electrical &amp; Renewable Solutions</h2><p>{e(HOME['services_intro'])}</p></div>
      <a class="link-arrow" href="{ctx.u(CONTACT)}">Discuss Your Project <span class="circle">{arrow()}</span></a>
    </div>
    <div class="svc-grid" data-stagger>{services}
    </div>
  </div>
</section>

<section class="section section-alt" id="sectors">
  <div class="container">
    <div class="section-head row" data-reveal>
      <div>{eyebrow('Sectors We Serve')}<h2>Built for Commercial and Industrial Sites</h2><p>From single units to multi site operations, we keep businesses powered, compliant and running, wherever the work takes us.</p></div>
      <a class="link-arrow" href="{ctx.u('/projects/')}">View Our Projects <span class="circle">{arrow()}</span></a>
    </div>
    <div class="sector-grid" data-stagger>{sectors}
    </div>
  </div>
</section>

<section class="section">
  <div class="container proof-grid">
    <div class="proof-media" data-reveal>
      {img(ctx, 'bm-packaging-2', led['alts'][1], '(max-width: 960px) 90vw, 50vw')}
      <span class="media-tag">{icon('map-pin')}BM Packaging Ltd, Huddersfield</span>
    </div>
    <div class="stack" data-reveal style="display:grid;gap:24px">
      {eyebrow('Proven Results')}
      <h2>Lower Energy Costs. Brighter Workplaces.</h2>
      <p class="lead">Our high bay LED lighting upgrade at BM Packaging Ltd was installed out of hours, so the factory never had to stop, and the results speak for themselves.</p>
      <div class="stats">
        <div class="stat"><strong data-count="55" data-suffix="%">55%</strong><span>reduction in energy costs</span></div>
        <div class="stat"><strong data-count="40" data-suffix="%">40%</strong><span>increase in lux levels</span></div>
      </div>
      <a class="link-arrow" href="{ctx.u('/led-lighting/')}">See the Project <span class="circle">{arrow()}</span></a>
    </div>
  </div>
</section>

<section class="section section-alt" style="overflow:hidden;overflow:clip">
  <div class="container">
    <div class="section-head row" data-reveal>
      <div>{eyebrow('Recent Projects')}<h2>Commercial Electrical Projects Across the North</h2></div>
      <a class="link-arrow" href="{ctx.u('/projects/')}">View All Projects <span class="circle">{arrow()}</span></a>
    </div>
  </div>
  <div data-carousel data-reveal>
    <div class="carousel-track projects-track">{projects}
    </div>
    <div class="container"><div class="head-tools" style="margin-top:28px"><button class="round-btn" type="button" data-prev aria-label="Previous project">{icon('arrow-left')}</button><button class="round-btn" type="button" data-next aria-label="Next project">{icon('arrow-right')}</button></div></div>
  </div>
</section>
{testimonials(ctx, alt=False)}
{logos_section(ctx, alt=True)}
{cta_band(ctx, 'home', 'Ready to Start Your Project?', 'Let’s Build a Smarter, Greener Tomorrow', CTA_DEFAULT)}'''
    meta = {'title': HOME['title'], 'description': HOME['description'], 'path': '/', 'jsonld': [org_jsonld()]}
    return meta, body


def page_service(ctx, slug):
    s = SERVICES[slug]
    anchors = []
    offers = []
    for o in s['offers']:
        anchor = re.sub(r'[^a-z0-9]+', '-', o['h'].lower()).strip('-')
        anchors.append('<a class="chip" href="#%s">%s%s</a>' % (anchor, icon(OFFER_ICON[o['h']]), e(HERO_SHORT.get(o['h'], o['h']))))
        offers.append(f'''
    <article class="offer" id="{anchor}">
      <div class="offer-media" data-reveal>
        {img(ctx, o['img'], o['alt'], '(max-width: 960px) 90vw, 50vw')}
        <span class="media-tag">{icon(OFFER_ICON[o['h']])}{e(s['name'])}</span>
      </div>
      <div class="offer-copy" data-reveal>
        <span class="ico-box">{icon(OFFER_ICON[o['h']])}</span>
        <h2>{e(o['h'])}</h2>
        <div class="copy">{''.join('<p>%s</p>' % e(p) for p in o['p'])}</div>
        <ul class="ticks">{''.join('<li>%s%s</li>' % (icon('circle-check'), e(x)) for x in o['items'])}</ul>
        {('<a class="link-arrow" href="%s">Learn More <span class="circle">%s</span></a>' % (ctx.u(OFFER_LINKS[o['h']]), arrow())) if o['h'] in OFFER_LINKS else ''}
      </div>
    </article>''')
    features = ''.join(f'''
        <div class="feature"><span class="ico-box">{icon(FEATURE_ICON.get(h, 'check'))}</span><h3>{e(h)}</h3><p>{e(p)}</p></div>''' for h, p in s['features'])
    faqs = ''.join(f'''
        <details><summary>{e(q)}<span class="pm">{icon('plus')}</span></summary><p class="ans">{e(a)}</p></details>''' for q, a in s['faqs'])
    places = ''.join('<span class="chip">%s%s</span>' % (icon('map-pin'), e(x)) for x in AREAS['items'])
    body = f'''
<section class="page-hero">
  {img(ctx, s['hero'], s['hero_alt'], '100vw', eager=True)}
  <div class="grain"></div>
  <div class="container page-hero-inner">
    {crumbs(ctx, [('Home', '/'), ('Services', None), (s['name'], None)])}
    <p class="kicker fade-up" style="--d:.05s"><span class="pulse"></span>Our Services</p>
    <h1 class="words">{words(s['name'])[0]}</h1>
    <p class="lead fade-up" style="--d:.45s">{e(s['lede'])}</p>
    <div class="btn-row fade-up" style="--d:.6s">{btn(ctx.u(CONTACT), 'Enquire Now')}<a class="btn btn-glass plain" href="tel:{SITE['phone_href']}">{icon('phone')}&nbsp;{SITE['phone']}</a></div>
    <div class="hero-chips fade-up" style="--d:.75s">{''.join(anchors)}</div>
  </div>
</section>

<section class="section">
  <div class="container intro-grid">
    <div class="intro-copy" data-reveal>
      {eyebrow('What We Do')}
      <h2>{e(s['intro_h2'])}</h2>
      <div class="copy">{''.join('<p>%s</p>' % e(p) for p in s['intro'])}</div>
      <div class="mini-logos">{logo_img(ctx, 'logo-niceic', 'NICEIC Approved Contractor')}{logo_img(ctx, 'logo-mcs', 'MCS certified')}{logo_img(ctx, 'logo-safecontractor', 'SafeContractor approved')}</div>
    </div>
    <div class="feature-grid" data-stagger>{features}
    </div>
  </div>
</section>

<section class="section-alt" aria-label="{e(s['name'])} services">
  <div class="container">{''.join(offers)}
  </div>
</section>
{process_section(ctx, s['process'])}
<section class="section section-alt">
  <div class="container duo">
    <div class="panel" data-reveal>
      {eyebrow('Areas We Cover')}
      <h2 style="font-size:clamp(1.8rem,1.3rem + 1.6vw,2.6rem)">{e(AREAS['h2'])}</h2>
      <p>{e(AREAS['p'])}</p>
      <div class="places">{places}</div>
      <div class="coverage-map">{img(ctx, 'areas-uk', 'Map of the UK showing Econ Electrical’s nationwide coverage from Yorkshire', '(max-width: 960px) 90vw, 40vw')}</div>
    </div>
    <div class="panel" data-reveal>
      {eyebrow('Frequently Asked Questions')}
      <h2 style="font-size:clamp(1.8rem,1.3rem + 1.6vw,2.6rem)">Got Questions?</h2>
      <div class="faq">{faqs}</div>
      <a class="link-arrow" href="{ctx.u(CONTACT)}">Ask Our Team <span class="circle">{arrow()}</span></a>
    </div>
  </div>
</section>
{cta_band(ctx, slug, 'Get in Touch', s['cta_h'], s['cta_p'])}'''
    faq_ld = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in s['faqs']]}
    meta = {'title': s['title'], 'description': s['description'], 'path': '/%s/' % slug, 'image': abs_img(s['hero']),
            'jsonld': [faq_ld]}
    return meta, body


def business_ref():
    """Point at the full business record on the home page instead of repeating it."""
    return {'@type': 'Electrician', '@id': SITE['domain'] + '/#business',
            'name': SITE['legal'], 'url': SITE['domain'] + '/'}


def project_jsonld(ctx, slug, keys):
    """A project page described as what it is: a write-up about a job we did.

    Article carries the write-up itself, which is what Google can show as a result.
    The 'about' Service is the part that earns its keep commercially: it ties the work
    to the service and the place, so an EV depot job in London reads as evidence that
    we install EV charging in London, rather than as an untyped page with photos on it.
    Nothing here is asserted that the page does not already say in words.
    """
    p = PROJECTS[slug]
    # Name the service by the service page this job belongs to, not by the job's own
    # title, so ten projects across four services say four consistent things rather
    # than ten unique ones. PROJECT_SERVICE already holds that mapping for the page's
    # own "related service" link, so there is nothing new to keep in step.
    svc = PROJECT_SERVICE.get(slug)
    service = {'@type': 'Service',
               'serviceType': SERVICES[svc]['name'] if svc in SERVICES else p['type'],
               'provider': business_ref()}
    if svc:
        service['url'] = SITE['domain'] + '/%s/' % svc
    if p.get('location'):
        service['areaServed'] = {'@type': 'Place', 'name': p['location']}
    return {
        '@context': 'https://schema.org', '@type': 'Article',
        'headline': p['name'],
        'description': p['description'],
        'image': [abs_img(k) for k in keys[:6]],
        'author': business_ref(),
        'publisher': {'@type': 'Organization', 'name': SITE['legal'],
                      'logo': {'@type': 'ImageObject',
                               'url': SITE['domain'] + '/assets/img/brand/econ-logo-320.png'}},
        'mainEntityOfPage': {'@type': 'WebPage', '@id': SITE['domain'] + '/%s/' % slug},
        'about': service,
    }


def page_project(ctx, slug):
    p = PROJECTS[slug]
    nxt = PROJECT_ORDER[(PROJECT_ORDER.index(slug) + 1) % len(PROJECT_ORDER)]
    keys = [project_key(slug, i) for i in range(1, p['count'] + 1)]
    gallery = ''.join('<a href="%s">%s<span class="zoom">%s</span></a>' % (
        full_src(ctx, k), img(ctx, k, p['alts'][i], '(max-width: 600px) 90vw, 33vw'), icon('maximize-2')) for i, k in enumerate(keys))
    results = stat_block(p.get('results'))
    extra = ''.join('<p>%s</p>' % e(x) for x in p['summary'][1:])
    quote_block = f'''
<section class="section" style="overflow:hidden;overflow:clip">
  <div class="glow" style="left:50%;top:50%;transform:translate(-50%,-50%)"></div>
  <div class="container">
    <figure class="big-quote" data-reveal>
      {icon('quote', 'i q')}
      <blockquote><p>{e(p.get('quote', ''))}</p></blockquote>
      <figcaption><strong>{e(p.get('quote_name', ''))}</strong><span>{e(p.get('quote_role', ''))}</span></figcaption>
    </figure>
  </div>
</section>''' if p.get('quote') else ''
    # Location is optional: some work is published without naming the site.
    spec = [('building-2', p.get('client_label', 'Client'), p['client'])]
    if p.get('location'):
        spec.append(('map-pin', 'Location', p['location']))
    spec += [(sector_icon(p), 'Sector', p['type']),
             ('badge-check', 'Certification', p.get('cert', 'NICEIC certificate'))]
    kicker = p.get('kicker') or ' · '.join(x for x in (p['client'], p.get('location')) if x)
    # A project can lead with footage instead of a still. The card image stays as the
    # poster, so the hero looks right before the video has loaded and if it never does.
    if p.get('video'):
        vid, vid_alt = p['video']
        hero_media = '<div class="hero-media">%s</div>' % video_tag(ctx, vid, vid_alt)
    else:
        hero_media = img(ctx, p['card'], project_card_alt(p), '100vw', eager=True)
    body = f'''
<section class="page-hero project"{' data-video' if p.get('video') else ''}{' style="--focus:%s"' % p['hero_focus'] if p.get('hero_focus') else ''}>
  {hero_media}
  <div class="grain"></div>
  <div class="container page-hero-inner">
    {crumbs(ctx, [('Home', '/'), ('Projects', '/projects/'), (p['name'], None)])}
    <p class="kicker fade-up" style="--d:.05s"><span class="pulse"></span>{e(kicker)}</p>
    <h1 class="words">{words(p['name'])[0]}</h1>
    <p class="lead fade-up" style="--d:.45s">{e(p['summary'][0])}</p>
  </div>
</section>

<div class="spec-bar">
  <div class="container">
    <div class="spec-inner fade-up" style="--d:.6s;--n:{len(spec)}">{''.join('<div class="spec-item"><span class="ico-box">%s</span><div><span class="k">%s</span><strong>%s</strong></div></div>' % (icon(ic), e(k), e(v)) for ic, k, v in spec)}</div>
  </div>
</div>

<section class="section">
  <div class="container proj-body">
    <div class="proj-main" data-reveal>
      {eyebrow('About the Project')}
      <h2>How We Helped</h2>
      {'<div class="copy">%s</div>' % extra if extra else ''}
      {results}
      <ul class="ticks">{''.join('<li>%s%s</li>' % (icon('circle-check'), e(x)) for x in p['scope'])}</ul>
      {('<a class="link-arrow" href="%s">More on %s <span class="circle">%s</span></a>' % (ctx.u('/%s/' % PROJECT_SERVICE[slug]), e(LANDING[PROJECT_SERVICE[slug]]['name']), arrow())) if slug in PROJECT_SERVICE else ''}
    </div>
    <aside class="side-card" data-reveal>
      {eyebrow('Planning Something Similar?')}
      <h3>Talk to the team that delivered it.</h3>
      <p>{e(CTA_DEFAULT)}</p>
      {btn(ctx.u(CONTACT), 'Discuss Your Project')}
      <a class="cta-phone" href="tel:{SITE['phone_href']}">{icon('phone')}{SITE['phone']}</a>
    </aside>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <div class="section-head row" data-reveal>
      <div>{eyebrow('See Our Work')}<h2>Project Gallery</h2></div>
      <p class="muted">{len(keys)} photos from site</p>
    </div>
    <div class="gallery" data-gallery data-reveal>{gallery}</div>
  </div>
</section>

{quote_block}

<section class="section flush-top">
  <div class="container">
    <a class="next-card" href="{ctx.u('/%s/' % nxt)}" data-reveal>
      {img(ctx, PROJECTS[nxt]['card'], project_card_alt(PROJECTS[nxt]), '100vw')}
      <span class="t">{eyebrow('Next Project')}<h2>{e(PROJECTS[nxt]['name'])}</h2><span class="chips">{'<span class="chip">%s%s</span>' % (icon('map-pin'), e(PROJECTS[nxt]['location'])) if PROJECTS[nxt].get('location') else ''}<span class="chip">{e(PROJECTS[nxt]['type'])}</span></span></span>
      <span class="svc-go">{icon('arrow-up-right')}</span>
    </a>
  </div>
</section>'''
    meta = {'title': p['title'], 'description': p['description'], 'path': '/%s/' % slug, 'image': abs_img(keys[0]),
            'og_type': 'article', 'jsonld': [project_jsonld(ctx, slug, keys)]}
    return meta, body


def landing_proof(ctx, d):
    if not d['proof'] and not d.get('results'):
        return ''
    stats = stat_block(d.get('results'), style=' style="margin-bottom:24px"')
    n = len(d['proof'])
    cards = ''.join(project_card(ctx, s, '(max-width: 760px) 90vw, %dvw' % (100 // max(n, 1))) for s in d['proof'])
    return f"""
<section class="section">
  <div class="container">
    <div class="section-head row" data-reveal>
      <div>{eyebrow('Proven Results')}<h2>{e(d['proof_h2'] or 'Recent Projects')}</h2></div>
      <a class="link-arrow" href="{ctx.u('/projects/')}">View All Projects <span class="circle">{arrow()}</span></a>
    </div>
    {stats}
    <div class="proof-cards n{n}" data-stagger>{cards}</div>
  </div>
</section>"""


def posts_in(cat, n=3):
    return [p for p in POSTS if p['cat'] == cat][:n]


def page_landing(ctx, slug):
    d = LANDING[slug]
    parent = SERVICES[d['parent']]
    chips = ''.join('<span class="chip">%s%s</span>' % (icon('circle-check'), e(c)) for c in d['chips'])
    points = ''.join(f"""
        <div class="feature"><span class="ico-box">{icon(ic)}</span><h3>{e(h)}</h3><p>{e(t)}</p></div>""" for ic, h, t in d['points'])
    faqs = ''.join(f"""
        <details><summary>{e(q)}<span class="pm">{icon('plus')}</span></summary><p class="ans">{e(a)}</p></details>""" for q, a in d['faqs'])
    places = ''.join('<span class="chip">%s%s</span>' % (icon('map-pin'), e(x)) for x in AREAS['items'])
    by_slug = {p['slug']: p for p in POSTS}
    reading = [by_slug[x] for x in d.get('reading', [])] or posts_in(d['cat'])
    body = f"""
<section class="page-hero">
  {img(ctx, d['hero'], d['hero_alt'], '100vw', eager=True)}
  <div class="grain"></div>
  <div class="container page-hero-inner">
    {crumbs(ctx, [('Home', '/'), (parent['name'], '/%s/' % d['parent']), (d['name'], None)])}
    <p class="kicker fade-up" style="--d:.05s"><span class="pulse"></span>{e(d['kicker'])}</p>
    <h1 class="words">{words(d['h1'])[0]}</h1>
    <p class="lead fade-up" style="--d:.45s">{e(d['lede'])}</p>
    <div class="btn-row fade-up" style="--d:.6s">{btn(ctx.u(CONTACT), 'Enquire Now')}<a class="btn btn-glass plain" href="tel:{SITE['phone_href']}">{icon('phone')}&nbsp;{SITE['phone']}</a></div>
    <div class="hero-chips fade-up" style="--d:.75s">{chips}</div>
  </div>
</section>

<section class="section">
  <div class="container intro-grid">
    <div class="intro-copy" data-reveal>
      {eyebrow('Overview')}
      <h2>{e(d['intro_h2'])}</h2>
      <div class="copy">{''.join('<p>%s</p>' % e(p) for p in d['intro'])}</div>
      <div class="mini-logos">{logo_img(ctx, 'logo-niceic', 'NICEIC Approved Contractor')}{logo_img(ctx, 'logo-mcs', 'MCS certified')}{logo_img(ctx, 'logo-safecontractor', 'SafeContractor approved')}</div>
      {('<p class="cross-link">%s <a href="%s">%s %s</a></p>' % (e(d['cross_link'][0]), ctx.u(d['cross_link'][1]), e(d['cross_link'][2]), arrow())) if d.get('cross_link') else ''}
    </div>
    <div class="feature-grid" data-stagger>{points}
    </div>
  </div>
</section>

<section class="section-alt" aria-label="{e(d['includes_h2'])}">
  <div class="container">
    <article class="offer">
      <div class="offer-media" data-reveal>
        {img(ctx, d['includes_img'], d['includes_alt'], '(max-width: 960px) 90vw, 50vw')}
        <span class="media-tag">{icon('badge-check')}NICEIC Approved</span>
      </div>
      <div class="offer-copy" data-reveal>
        <span class="ico-box">{icon('list-checks')}</span>
        <h2>{e(d['includes_h2'])}</h2>
        <div class="copy"><p>{e(d['includes_intro'])}</p></div>
        <ul class="ticks">{''.join('<li>%s%s</li>' % (icon('circle-check'), e(x)) for x in d['includes'])}</ul>
        <a class="link-arrow" href="{ctx.u('/%s/' % d['parent'])}">All {e(parent['name'])} Services <span class="circle">{arrow()}</span></a>
      </div>
    </article>
  </div>
</section>
{landing_proof(ctx, d)}
{process_section(ctx, d['process'], alt=not d['proof'])}
<section class="section{' section-alt' if d['proof'] else ''}">
  <div class="container duo">
    <div class="panel" data-reveal>
      {eyebrow('Frequently Asked Questions')}
      <h2 style="font-size:clamp(1.8rem,1.3rem + 1.6vw,2.6rem)">Got Questions?</h2>
      <div class="faq">{faqs}</div>
      <a class="link-arrow" href="{ctx.u(CONTACT)}">Ask Our Team <span class="circle">{arrow()}</span></a>
    </div>
    <div class="panel" data-reveal>
      {eyebrow('Areas We Cover')}
      <h2 style="font-size:clamp(1.8rem,1.3rem + 1.6vw,2.6rem)">{e(AREAS['h2'])}</h2>
      <p>{e(AREAS['p'])}</p>
      <div class="places">{places}</div>
      <div class="coverage-map">{img(ctx, 'areas-uk', 'Map of the UK showing Econ Electrical’s nationwide coverage from Yorkshire', '(max-width: 960px) 90vw, 40vw')}</div>
    </div>
  </div>
</section>
<section class="section{'' if d['proof'] else ' section-alt'}">
  <div class="container">
    <div class="section-head row" data-reveal>
      <div>{eyebrow('Guidance')}<h2>Helpful Reading</h2></div>
      <a class="link-arrow" href="{ctx.u('/blog/#' + cat_slug(d['cat']))}">More Articles <span class="circle">{arrow()}</span></a>
    </div>
    <div class="post-grid{' three' if len(reading) == 3 else ''}" data-stagger>{''.join(post_card(ctx, p) for p in reading)}</div>
  </div>
</section>
{cta_band(ctx, slug, 'Get in Touch', d['cta_h'], d['cta_p'], 'Enquire Now')}"""
    url = SITE['domain'] + '/%s/' % slug
    faq_ld = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in d['faqs']]}
    svc_ld = {'@context': 'https://schema.org', '@type': 'Service', 'name': d['h1'], 'serviceType': d['name'],
              'description': d['description'], 'url': url, 'areaServed': ['Yorkshire', 'United Kingdom'],
              'provider': {'@type': 'Electrician', '@id': SITE['domain'] + '/#business', 'name': SITE['legal'], 'url': SITE['domain'] + '/'}}
    meta = {'title': d['title'], 'description': d['description'], 'path': '/%s/' % slug, 'image': abs_img(d['hero']),
            'jsonld': [svc_ld, faq_ld]}
    return meta, body


def app_mockup():
    """A simple phone showing the kind of live view the app gives (illustrative figures)."""
    ring = ('<svg viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="50" fill="none" stroke="rgba(255,255,255,.08)" stroke-width="10"/>'
            '<circle cx="60" cy="60" r="50" fill="none" stroke="#9eca84" stroke-width="10" stroke-linecap="round" '
            'stroke-dasharray="289 314" transform="rotate(-90 60 60)"/></svg>')
    tiles = [('sun', 'Solar', '6.4 kW'), ('battery-charging', 'Battery', '86%'), ('house', 'Home', '1.2 kW'),
             ('thermometer', 'Heat pump', '0.8 kW')]
    cells = ''.join('<div class="ph-tile">%s<span>%s</span><b>%s</b></div>' % (icon(ic), e(k), e(v)) for ic, k, v in tiles)
    bars = ''.join('<i style="--h:%d%%"></i>' % h for h in (8, 14, 26, 44, 62, 78, 90, 96, 88, 70, 46, 22))
    return f"""<div class="phone" aria-hidden="true">
  <div class="phone-screen">
    <div class="ph-bar"><span></span></div>
    <div class="ph-head"><div><small>Good evening</small><strong>My Home</strong></div><span class="ph-live"><i></i>Live</span></div>
    <div class="ph-ring">{ring}<div><strong>92%</strong><span>self powered today</span></div></div>
    <div class="ph-tiles">{cells}</div>
    <div class="ph-chart"><span>Today</span><div>{bars}</div></div>
    <div class="ph-ev">{icon('plug-zap')}<div><span>EV charging</span><b>Charging from solar</b></div></div>
  </div>
</div>"""


def page_residential(ctx):
    r = RESIDENTIAL
    eco = ''.join(f"""
        <div class="eco-card"><span class="ico-box">{icon(ic)}</span><h3>{e(h)}</h3><p>{e(t)}</p></div>""" for ic, h, t in r['eco'])
    pillars = ''.join(f"""
      <div class="pillar"><span class="ico-box">{icon(ic)}</span><h3>{e(h)}</h3><p>{e(t)}</p></div>""" for ic, h, t in r['pillars'])
    tiers = ''.join(f"""
      <article class="tier{' featured' if i == 1 else ''}">
        <span class="tier-num">0{i + 1}</span>
        <h3>{e(name)}</h3>
        <p>{e(text)}</p>
        <ul class="ticks">{''.join('<li>%s%s</li>' % (icon('circle-check'), e(x)) for x in items)}</ul>
      </article>""" for i, (name, text, items) in enumerate(r['tiers']))
    support = ''.join(f"""
        <div class="feature"><span class="ico-box">{icon(ic)}</span><h3>{e(h)}</h3><p>{e(t)}</p></div>""" for ic, h, t in r['support'])
    faqs = ''.join(f"""
        <details><summary>{e(q)}<span class="pm">{icon('plus')}</span></summary><p class="ans">{e(a)}</p></details>""" for q, a in r['faqs'])
    body = f"""
<section class="page-hero plain res-hero">
  <div class="container page-hero-inner">
    {crumbs(ctx, [('Home', '/'), ('Renewables', '/renewables/'), (r['name'], None)])}
    <p class="kicker fade-up" style="--d:.05s"><span class="pulse"></span>{e(r['kicker'])}</p>
    <h1 class="words">{words(r['h1'])[0]}</h1>
    <p class="lead fade-up" style="--d:.45s">{e(r['lede'])}</p>
    <div class="btn-row fade-up" style="--d:.6s">{btn(ctx.u(CONTACT), 'Book a Design Consultation')}<a class="btn btn-glass plain" href="tel:{SITE['phone_href']}">{icon('phone')}&nbsp;{SITE['phone']}</a></div>
    <div class="hero-chips fade-up" style="--d:.75s"><span class="chip">{icon('badge-check')}MCS Certified</span><span class="chip">{icon('shield-check')}NICEIC Approved</span>{ext(SITE['google_profile'], icon('sparkles') + 'Rated 4.9 on Google', 'chip')}</div>
  </div>
</section>
<section class="res-showcase">
  <div class="container">
    <figure class="res-art fade-up" style="--d:.5s"><div class="art-scroll" data-art-scroll>{home_energy_svg()}</div><p class="swipe-hint" aria-hidden="true">{icon('arrow-left')}Swipe to explore{icon('arrow-right')}</p></figure>
  </div>
</section>

<section class="section eco-section" style="overflow:hidden;overflow:clip">
  <div class="container eco-grid">
    <div class="eco-copy" data-reveal>
      {eyebrow('The SolaX Ecosystem')}
      <h2>{e(r['eco_h2'])}</h2>
      <div class="copy">{''.join('<p>%s</p>' % e(p) for p in r['eco_intro'])}</div>
      <div class="eco-cards" data-stagger>{eco}
      </div>
    </div>
    <div class="eco-phone" data-reveal>
      <div class="glow" style="left:50%;top:50%;transform:translate(-50%,-50%)"></div>
      {app_mockup()}
      <p class="phone-cap">{icon('activity')}Your solar, battery, heat pump and car, all in one app</p>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <div class="section-head center" data-reveal>{eyebrow('Why Homeowners Choose Econ')}<h2>{e(r['pillars_h2'])}</h2></div>
    <div class="pillar-grid" data-stagger>{pillars}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head row" data-reveal>
      <div>{eyebrow('Your Options')}<h2>{e(r['tiers_h2'])}</h2><p>Every home is different, so every system is designed from scratch, usually starting from one of these three.</p></div>
      <a class="link-arrow" href="{ctx.u(CONTACT)}">Talk It Through <span class="circle">{arrow()}</span></a>
    </div>
    <div class="tier-grid" data-stagger>{tiers}
    </div>
  </div>
</section>

<section class="section-alt" aria-label="{e(r['turnkey_h2'])}">
  <div class="container">
    <article class="offer">
      <div class="offer-media" data-reveal>
        {img(ctx, 'about-vans', 'Econ Electrical branded electric vans', '(max-width: 960px) 90vw, 50vw')}
        <span class="media-tag">{icon('badge-check')}One team, start to finish</span>
      </div>
      <div class="offer-copy" data-reveal>
        <span class="ico-box">{icon('layers')}</span>
        <h2>{e(r['turnkey_h2'])}</h2>
        <div class="copy">{''.join('<p>%s</p>' % e(p) for p in r['turnkey'])}</div>
        <ul class="ticks">{''.join('<li>%s%s</li>' % (icon('circle-check'), e(x)) for x in r['turnkey_items'])}</ul>
      </div>
    </article>
  </div>
</section>

<section class="section">
  <div class="container intro-grid">
    <div class="intro-copy" data-reveal>
      {eyebrow('Aftercare')}
      <h2>{e(r['support_h2'])}</h2>
      <div class="copy"><p>Your system should look after you for decades, and so should we. Our team stays on hand long after the scaffold comes down.</p></div>
      <div class="mini-logos">{logo_img(ctx, 'logo-solax', 'SolaX Power')}{logo_img(ctx, 'logo-mcs', 'MCS certified')}{logo_img(ctx, 'logo-niceic', 'NICEIC Approved Contractor')}</div>
    </div>
    <div class="feature-grid" data-stagger>{support}
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container duo">
    <div class="panel" data-reveal>
      {eyebrow('Frequently Asked Questions')}
      <h2 style="font-size:clamp(1.8rem,1.3rem + 1.6vw,2.6rem)">Got Questions?</h2>
      <div class="faq">{faqs}</div>
    </div>
    <div class="panel res-reviews" data-reveal>
      {eyebrow('Trusted Locally')}
      <h2 style="font-size:clamp(1.8rem,1.3rem + 1.6vw,2.6rem)">Rated 4.9 on Google</h2>
      <p>Homeowners across Yorkshire trust our team with their homes. Read what they say about our work, our tidiness and our communication.</p>
      {ext(SITE['google_profile'], 'Read Our Google Reviews <span class="btn-ico">%s</span>' % icon('arrow-up-right'), 'btn btn-primary')}
      <div class="res-contact">
        <a href="tel:{SITE['phone_href']}">{icon('phone')}{SITE['phone']}</a>
        <a href="mailto:{SITE['email']}">{icon('mail')}{SITE['email']}</a>
      </div>
    </div>
  </div>
</section>
{cta_band(ctx, r['slug'], 'Get Started', r['cta_h'], r['cta_p'], 'Book a Consultation')}"""
    url = SITE['domain'] + '/%s/' % r['slug']
    faq_ld = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in r['faqs']]}
    svc_ld = {'@context': 'https://schema.org', '@type': 'Service', 'name': 'Home solar panels and battery storage',
              'serviceType': 'Residential solar PV and battery storage installation', 'description': r['description'], 'url': url,
              'areaServed': ['Yorkshire', 'United Kingdom'],
              'provider': {'@type': 'Electrician', '@id': SITE['domain'] + '/#business', 'name': SITE['legal'], 'url': SITE['domain'] + '/'}}
    meta = {'title': r['title'], 'description': r['description'], 'path': '/%s/' % r['slug'],
            'image': abs_img('home-energy-og'), 'jsonld': [svc_ld, faq_ld]}
    return meta, body


def page_projects(ctx):
    """Every project, once, in one grid.

    This page has been through two shapes that both split the work up: first a
    featured page with the rest behind a link, then one page with a featured block
    above a smaller filterable list. Both showed the best jobs twice and dropped to a
    meaner card halfway down, so the page lost its nerve exactly where someone
    scrolling is deciding whether to get in touch.

    So: one grid, one card treatment, each project once, in PROJECT_ORDER so the
    strongest work leads. Every fifth card runs the full width, which gives the page
    a rhythm instead of an unbroken ladder of pairs and keeps working at any count.
    """
    sectors = []
    for s in PROJECT_ORDER:
        t = PROJECTS[s]['type']
        if t not in sectors:
            sectors.append(t)
    filters = '<button type="button" class="filter" data-filter="all" aria-pressed="true">All Projects<span>%d</span></button>' % len(PROJECT_ORDER)
    filters += ''.join('<button type="button" class="filter" data-filter="%s" aria-pressed="false">%s<span>%d</span></button>' % (
        slug(t), e(t), sum(1 for s in PROJECT_ORDER if PROJECTS[s]['type'] == t)) for t in sectors)
    # The wide cards are marked here as well as re-marked by the filter script, so the
    # rhythm is right in the HTML itself and does not depend on JavaScript running.
    cards = ''.join(project_card(ctx, s,
                                 '(max-width: 760px) 90vw, 100vw' if i % 5 == 0 else '(max-width: 760px) 90vw, 50vw',
                                 'h2', cat=slug(PROJECTS[s]['type']), cls='wide' if i % 5 == 0 else '')
                    for i, s in enumerate(PROJECT_ORDER))
    body = f'''
<section class="page-hero short">
  {img(ctx, 'solarbradford-1', 'Roof mounted commercial solar array installed by Econ Electrical in Bradford', '100vw', eager=True)}
  <div class="grain"></div>
  <div class="container page-hero-inner">
    {crumbs(ctx, [('Home', '/'), ('Projects', None)])}
    <p class="kicker fade-up" style="--d:.05s"><span class="pulse"></span>{len(PROJECT_ORDER)} Projects</p>
    <h1 class="words">{words('Our Projects')[0]}</h1>
    <p class="lead fade-up" style="--d:.45s">Commercial and industrial installations delivered by our team, from factory lighting upgrades to EV charging and full workshop fit outs. Filter by sector to find work like yours.</p>
  </div>
</section>
<section class="section">
  <div class="container" data-filterable>
    <div class="post-filters" role="group" aria-label="Filter projects by sector">{filters}</div>
    <div class="proj-grid" data-stagger>{cards}</div>
    <p class="filter-status sr-only" role="status" aria-live="polite"></p>
  </div>
</section>
{testimonials(ctx)}
{cta_band(ctx, 'projects', 'Planning a Similar Project?', 'Let’s Talk About Your Site', CTA_DEFAULT)}'''
    # The list in the order it appears on the page, so the markup and the page agree.
    listing = {'@context': 'https://schema.org', '@type': 'CollectionPage',
               'name': 'Econ Electrical Projects', 'url': SITE['domain'] + '/projects/',
               'mainEntity': {'@type': 'ItemList', 'numberOfItems': len(PROJECT_ORDER),
                              'itemListElement': [
                                  {'@type': 'ListItem', 'position': i, 'url': SITE['domain'] + '/%s/' % s,
                                   'name': PROJECTS[s]['name']}
                                  for i, s in enumerate(PROJECT_ORDER, 1)]}}
    meta = {'title': 'Commercial Electrical Projects in Yorkshire | Econ Electrical',
            'description': 'Commercial and industrial electrical projects by Econ Electrical, including LED lighting, EV charging, solar PV and full workshop fit outs across Yorkshire and the UK.',
            'path': '/projects/', 'jsonld': [listing]}
    return meta, body


def page_about(ctx):
    team = ''.join(f'''
      <article class="member">
        <div class="photo">{img(ctx, 'team-' + key, name, '(max-width: 560px) 90vw, (max-width: 960px) 45vw, 30vw')}</div>
        <div class="info">
          <p class="role">{e(role)}</p>
          <h3>{e(name)}</h3>
          <p>{e(bio)}</p>
          {ext(li, 'LinkedIn ' + icon('arrow-up-right'), 'li') if li else ''}
        </div>
      </article>''' for key, name, role, bio, li in TEAM)
    values = ''.join(f'''
        <div class="feature"><span class="ico-box">{icon(ic)}</span><h3>{e(t)}</h3><p>{e(d)}</p></div>''' for ic, t, d in TRUST)
    body = f'''
<section class="page-hero split">
  <div class="container split-inner">
    <div class="split-copy">
      {crumbs(ctx, [('Home', '/'), ('About Us', None)])}
      <p class="kicker fade-up" style="--d:.05s"><span class="pulse"></span>About Us</p>
      <h1 class="words">{words('Yorkshire Roots, Nationwide Reach')[0]}</h1>
      <p class="lead fade-up" style="--d:.45s">Commercial and industrial electrical contractors based in Wakefield, delivering projects for businesses right across the UK.</p>
      <div class="btn-row fade-up" style="--d:.6s">{btn(ctx.u(CONTACT), 'Enquire Now')}{btn(ctx.u('/projects/'), 'See Our Projects', 'glass')}</div>
    </div>
    <figure class="split-media fade-up" style="--d:.35s">
      {img(ctx, 'about-vans', 'Two Econ Electrical branded electric vans parked side by side', '(max-width: 960px) 92vw, 52vw', eager=True)}
      <figcaption class="media-tag">{icon('zap')}Our new electric vans</figcaption>
    </figure>
  </div>
</section>

<section class="section">
  <div class="container story-grid">
    <div class="stack" data-reveal style="display:grid;gap:26px">
      {eyebrow('Who We Are')}
      <p class="statement">Proud of our Yorkshire roots, trusted on large scale projects across the country.</p>
      <div class="mini-logos">{logo_img(ctx, 'logo-niceic', 'NICEIC Approved Contractor')}{logo_img(ctx, 'logo-mcs', 'MCS certified')}{logo_img(ctx, 'logo-safecontractor', 'SafeContractor approved')}</div>
    </div>
    <div class="copy" data-reveal>{''.join('<p>%s</p>' % e(p) for p in ABOUT_PARAS)}</div>
  </div>
  <div class="container" style="margin-top:clamp(56px,7vw,96px)">
    <div class="feature-grid" style="grid-template-columns:repeat(auto-fit,minmax(240px,1fr))" data-stagger>{values}
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <div class="section-head row" data-reveal>
      <div>{eyebrow('Get to Know Us')}<h2>Meet Our Team</h2></div>
      <p class="muted" style="max-width:40ch">The people who plan, install and look after your electrical systems.</p>
    </div>
    <div class="team-grid" data-stagger>{team}
    </div>
  </div>
</section>
{logos_section(ctx)}
{cta_band(ctx, 'about', 'Work With Us', 'Let’s Talk About Your Project', CTA_DEFAULT)}'''
    # Names and roles only. They are already on the page, and nothing else about the
    # lads belongs in machine readable markup.
    about_ld = {'@context': 'https://schema.org', '@type': 'AboutPage',
                'url': SITE['domain'] + '/about-us/',
                'mainEntity': dict(business_ref(), **{
                    'employee': [{'@type': 'Person', 'name': name, 'jobTitle': role}
                                 for _, name, role, _, _ in TEAM]})}
    meta = {'title': 'About Econ Electrical | Wakefield Electrical Contractors',
            'description': 'Based in Wakefield with a nationwide reach, Econ Electrical provides expert electrical contracting for commercial and industrial projects across the UK.',
            'path': '/about-us/', 'image': abs_img('about-vans'), 'jsonld': [about_ld]}
    return meta, body


def page_contact(ctx):
    if ctx.mode == 'site':
        form_open = ('<form class="form" name="contact" method="POST" action="/thank-you/" data-netlify="true" '
                     'netlify-honeypot="bot-field">\n<input type="hidden" name="form-name" value="contact">\n'
                     '<input type="hidden" name="subject" data-remove-prefix value="New website enquiry from econelectrical.co.uk">\n'
                     '<p class="hp"><label>Leave this empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>')
        map_inner = None
    else:
        form_open = '<form class="form" name="contact" method="POST" data-preview data-email="%s">' % SITE['email']
        map_inner = ('<img src="%s" width="%d" height="%d" alt="Map of Denby Dale Road, Wakefield, showing the Econ Electrical office" loading="lazy">'
                     '<div class="map-pin" style="--x:%s%%;--y:%s%%"><span class="dot"></span><span class="lbl">Econ Electrical</span></div>'
                     '<span class="map-credit">&copy; OpenStreetMap contributors</span>'
                     '<span class="map-note">Preview map. The live site shows the interactive Google map here.</span>') % (
            ctx.a('assets/img/contact/econ-office-map.webp'), MAP['w'], MAP['h'], MAP['x'], MAP['y'])
    static_map = ('<img src="%s" width="%d" height="%d" alt="Map of Denby Dale Road, Wakefield, showing the Econ Electrical office" loading="lazy">'
                  '<div class="map-pin" style="--x:%s%%;--y:%s%%"><span class="dot"></span><span class="lbl">Econ Electrical</span></div>'
                  '<span class="map-credit">&copy; OpenStreetMap contributors</span>') % (
        ctx.a('assets/img/contact/econ-office-map.webp'), MAP['w'], MAP['h'], MAP['x'], MAP['y'])
    if ctx.mode == 'site':
        map_attrs = ' data-map-src="%s" data-map-title="Map showing Econ Electrical, The Courtyard, 225 Denby Dale Road, Wakefield"' % e(GMAP)
        map_inner = static_map + ('<button type="button" class="btn btn-glass btn-sm map-load" data-map-load>Show Google Map'
                                  '<span class="btn-ico">%s</span></button>') % icon('map-pin')
    else:
        map_attrs = ''
    addr_line = ', '.join(SITE['address'])
    body = f'''
<section class="page-hero short">
  {img(ctx, 'installation-hero', 'Commercial switch room fitted out by Econ Electrical', '100vw', eager=True)}
  <div class="grain"></div>
  <div class="container page-hero-inner">
    {crumbs(ctx, [('Home', '/'), ('Contact Us', None)])}
    <p class="kicker fade-up" style="--d:.05s"><span class="pulse"></span>Contact Us</p>
    <h1 class="words">{words('Get in Touch With Us')[0]}</h1>
    <p class="lead fade-up" style="--d:.45s">Tell us about your site, project or maintenance requirements and our team will come back to you. Send us a message, give us a call or drop us an email.</p>
    <div class="quick fade-up" style="--d:.6s">
      <a href="tel:{SITE['phone_href']}"><span class="ico-box">{icon('phone')}</span><span><small>Call us</small><b>{SITE['phone']}</b></span></a>
      <a href="mailto:{SITE['email']}"><span class="ico-box">{icon('mail')}</span><span><small>Email us</small><b>{SITE['email']}</b></span></a>
      {ext(SITE['whatsapp_href'], '<span class="ico-box">%s</span><span><small>WhatsApp</small><b>%s</b></span>' % (icon('messages-square'), SITE['whatsapp']))}
    </div>
  </div>
</section>

<section class="section">
  <div class="container contact-grid">
    <div class="form-card" data-reveal>
      <div style="display:grid;gap:14px">{eyebrow('Send Us a Message')}<h2 style="font-size:clamp(1.9rem,1.4rem + 1.6vw,2.8rem)">Tell Us About Your Project</h2></div>
      {form_open}
        <div class="field"><label for="f-name">Name</label><input id="f-name" name="name" type="text" autocomplete="name" placeholder="Your name" required></div>
        <div class="field"><label for="f-company">Company <span class="opt">(optional)</span></label><input id="f-company" name="company" type="text" autocomplete="organization" placeholder="Company name"></div>
        <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" placeholder="you@company.co.uk" required></div>
        <div class="field"><label for="f-phone">Phone <span class="opt">(optional)</span></label><input id="f-phone" name="phone" type="tel" autocomplete="tel" placeholder="Best number to reach you"></div>
        <div class="field full"><label for="f-message">Message</label><textarea id="f-message" name="message" required placeholder="Tell us about your site and what you need"></textarea></div>
        <div class="form-foot">
          <span class="form-note">{icon('shield-check')}<span>We&rsquo;ll only use your details to reply to your enquiry. <a href="{ctx.u('/privacy-notice/')}">Privacy notice</a></span></span>
          <button class="btn btn-primary" type="submit">Send Message<span class="btn-ico">{arrow()}</span></button>
        </div>
        <p class="form-status" role="status" hidden></p>
      </form>
    </div>
    <aside class="info-card" data-reveal>
      {eyebrow('Contact Details')}
      <div class="info-row"><span class="ico-box">{icon('phone')}</span><div><small>Phone</small><a href="tel:{SITE['phone_href']}">{SITE['phone']}</a></div></div>
      <div class="info-row"><span class="ico-box">{icon('mail')}</span><div><small>Email</small><a href="mailto:{SITE['email']}">{SITE['email']}</a></div></div>
      <div class="info-row"><span class="ico-box">{icon('messages-square')}</span><div><small>WhatsApp</small>{ext(SITE['whatsapp_href'], SITE['whatsapp'])}</div></div>
      <div class="info-row"><span class="ico-box">{icon('map-pin')}</span><div><small>Office</small><address>{e(SITE['legal'])}<br>{'<br>'.join(e(x) for x in SITE['address'])}</address></div></div>
      <div class="info-row"><span class="ico-box">{icon('clock')}</span><div><small>Opening hours</small><span>{e(SITE['hours_text'])}</span></div></div>
      <div class="socials">{ext(SITE['google_profile'], 'Google Reviews')}{ext(SITE['linkedin'], 'LinkedIn')}{ext(SITE['instagram'], 'Instagram')}{ext(SITE['facebook'], 'Facebook')}</div>
    </aside>
  </div>
</section>

<section class="section flush-top">
  <div class="container">
    <div class="map-wrap" data-reveal>
      <div class="map-canvas"{map_attrs}>{map_inner}</div>
      <div class="map-card">
        {eyebrow('Find Us')}
        <h3>Econ Electrical Ltd</h3>
        <address>{e(addr_line)}</address>
        {ext(SITE['maps'], 'Get Directions<span class="btn-ico">%s</span>' % icon('navigation'), 'btn btn-primary btn-sm')}
      </div>
    </div>
  </div>
</section>
{logos_section(ctx, alt=True)}'''
    meta = {'title': 'Electricians Wakefield | Contact Us | Econ Electrical',
            'description': 'Commercial and industrial electrical contractors in Wakefield. Get in touch with Econ Electrical to discuss your installation, renewables or compliance project.',
            'path': CONTACT, 'jsonld': [org_jsonld()]}
    return meta, body


def cat_slug(cat):
    return re.sub(r'[^a-z0-9]+', '-', cat.lower()).strip('-')


def post_card(ctx, post, heading='h3', latest=False):
    return f'''<a class="post-card" href="{ctx.u('/%s/' % post['slug'])}" data-cat="{cat_slug(post['cat'])}"{' data-latest' if latest else ''}>
  <span class="media">{img(ctx, post['img'], post['alt'], '(max-width: 600px) 90vw, (max-width: 1100px) 45vw, 25vw')}<span class="cat-tag">{e(post['cat'])}</span></span>
  <span class="body">
    <span class="post-meta"><span>{icon('calendar-check')}<time datetime="{post['date']}">{nice_date(post['date'])}</time></span><span>{icon('clock')}{read_time(post['body'])} min read</span></span>
    <{heading}>{e(post['title'])}</{heading}>
    <p>{e(post['excerpt'])}</p>
  </span>
</a>'''


def related_posts(post, n=3):
    same = [p for p in POSTS if p['slug'] != post['slug'] and p['cat'] == post['cat']]
    rest = [p for p in POSTS if p['slug'] != post['slug'] and p['cat'] != post['cat']]
    return (same + rest)[:n]


def page_blog(ctx):
    first = POSTS[0]
    counts = {c: sum(1 for p in POSTS if p['cat'] == c) for c in CATEGORIES}
    filters = '<button type="button" class="filter" data-filter="all" aria-pressed="true">All Articles<span>%d</span></button>' % len(POSTS)
    filters += ''.join('<button type="button" class="filter" data-filter="%s" aria-pressed="false">%s<span>%d</span></button>' % (
        cat_slug(c), e(c), counts[c]) for c in CATEGORIES if counts[c])
    body = f'''
<section class="page-hero plain">
  <div class="container page-hero-inner">
    {crumbs(ctx, [('Home', '/'), ('Blog', None)])}
    <p class="kicker fade-up" style="--d:.05s"><span class="pulse"></span>News &amp; Insights</p>
    <h1 class="words">{words('Blog')[0]}</h1>
    <p class="lead fade-up" style="--d:.45s">Guidance and insights on commercial electrical installation, renewables and compliance from the Econ Electrical team.</p>
  </div>
</section>
<section class="section flush-top">
  <div class="container blog-wrap" data-blog>
    <a class="featured-post" href="{ctx.u('/%s/' % first['slug'])}" data-reveal>
      <span class="media">{img(ctx, first['img'], first['alt'], '(max-width: 900px) 90vw, 55vw', eager=True)}</span>
      <span class="body">
        <span class="chips"><span class="chip">{icon('sparkles')}Latest Article</span><span class="chip">{icon('tag')}{e(first['cat'])}</span></span>
        <span class="post-meta"><span>{icon('calendar-check')}<time datetime="{first['date']}">{nice_date(first['date'])}</time></span><span>{icon('clock')}{read_time(first['body'])} min read</span></span>
        <h2>{e(first['title'])}</h2>
        <p class="muted">{e(first['excerpt'])}</p>
        <span class="link-arrow">Read Article <span class="circle">{arrow()}</span></span>
      </span>
    </a>
    <div class="post-filters" role="group" aria-label="Filter articles by topic">{filters}</div>
    <div class="post-grid" data-stagger>{''.join(post_card(ctx, p, latest=(i == 0)) for i, p in enumerate(POSTS))}</div>
    <p class="filter-status sr-only" role="status" aria-live="polite"></p>
  </div>
</section>
{cta_band(ctx, 'blog', 'Need Some Advice?', 'Need Reliable Electrical Support?', CTA_DEFAULT)}'''
    blog_ld = {'@context': 'https://schema.org', '@type': 'Blog',
               'name': 'Econ Electrical Blog', 'url': SITE['domain'] + '/blog/',
               'publisher': business_ref(),
               'blogPost': [{'@type': 'BlogPosting', 'headline': p['title'],
                             'url': SITE['domain'] + '/%s/' % p['slug'], 'datePublished': p['date']}
                            for p in POSTS]}
    meta = {'title': 'Commercial Electrical Advice and News | Econ Electrical',
            'description': 'News, guidance and insights on commercial electrical work, renewables and compliance from Econ Electrical in Wakefield.',
            'path': '/blog/', 'jsonld': [blog_ld]}
    return meta, body


def page_post(ctx, post):
    md = post['body'].replace('{{contact}}', ctx.u(CONTACT))
    md = re.sub(r'\{\{u:([^}]+)\}\}', lambda m: ctx.u(m.group(1)), md)
    content = markdown.markdown(md.strip(), extensions=['sane_lists'], output_format='html')
    others = related_posts(post)
    url = SITE['domain'] + '/%s/' % post['slug']
    updated = post.get('updated')
    updated_meta = ('<span>%sUpdated <time datetime="%s">%s</time></span>' % (icon('circle-check'), updated, nice_date(updated))
                    if updated else '')
    body = f'''
<div class="progress" aria-hidden="true"></div>
<article data-article>
  <section class="article-hero">
    <div class="container">
      <div class="inner">
        {crumbs(ctx, [('Home', '/'), ('Blog', '/blog/')])}
        <span class="post-meta fade-up" style="--d:.05s"><a class="cat-link" href="{ctx.u('/blog/#' + cat_slug(post['cat']))}">{icon('tag')}{e(post['cat'])}</a><span>{icon('calendar-check')}<time datetime="{post['date']}">{nice_date(post['date'])}</time></span>{updated_meta}<span>{icon('clock')}{read_time(post['body'])} min read</span></span>
        <h1 class="fade-up" style="--d:.15s">{e(post['title'])}</h1>
        <p class="lead fade-up" style="--d:.3s">{e(post['excerpt'])}</p>
      </div>
    </div>
  </section>
  <div class="container"><figure class="article-cover fade-up" style="--d:.4s">{img(ctx, post['img'], post['alt'], '100vw', eager=True)}</figure></div>
  <section class="section tight">
    <div class="container">
      <div class="prose">
{content}
      </div>
      <div class="share">
        <span class="label">Share</span>
        {ext('https://www.linkedin.com/sharing/share-offsite/?url=' + url, 'LinkedIn')}
        {ext('https://www.facebook.com/sharer/sharer.php?u=' + url, 'Facebook')}
        <button type="button" data-copy="{url}">{icon('copy')}<span class="txt">Copy link</span></button>
      </div>
    </div>
  </section>
</article>
<section class="section section-alt">
  <div class="container">
    <div class="section-head row" data-reveal>
      <div>{eyebrow('Keep Reading')}<h2>Related Articles</h2></div>
      <a class="link-arrow" href="{ctx.u('/blog/')}">All Articles <span class="circle">{arrow()}</span></a>
    </div>
    <div class="post-grid three" data-stagger>{''.join(post_card(ctx, p) for p in others)}</div>
  </div>
</section>
{cta_band(ctx, 'blog', 'Talk to Our Team', 'Need Reliable Electrical Support?', CTA_DEFAULT)}'''
    image = abs_img(post['img'])
    ld = {'@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': post['title'],
          'description': post['excerpt'], 'articleSection': post['cat'],
          'datePublished': post['date'], 'dateModified': updated or post['date'], 'image': image, 'mainEntityOfPage': url,
          'author': {'@type': 'Organization', 'name': SITE['legal']},
          'publisher': {'@type': 'Organization', 'name': SITE['legal'],
                        'logo': {'@type': 'ImageObject', 'url': SITE['domain'] + '/assets/img/brand/econ-logo-320.png'}}}
    # seo_title is the short form for the browser tab and the search result, where
    # anything past about 60 characters is cut off mid sentence. The headline on the
    # page stays as written: it has room to be a full sentence, a result does not.
    meta = {'title': '%s | Econ Electrical' % (post.get('seo_title') or post['title']),
            'description': post['excerpt'], 'path': '/%s/' % post['slug'],
            'image': image, 'og_type': 'article', 'jsonld': [ld], 'lastmod': updated or post['date']}
    return meta, body


def page_privacy(ctx):
    content = markdown.markdown(PRIVACY['body'].strip(), extensions=['sane_lists'], output_format='html')
    body = f"""
<section class="article-hero">
  <div class="container">
    <div class="inner">
      {crumbs(ctx, [('Home', '/'), ('Privacy Notice', None)])}
      <span class="post-meta fade-up" style="--d:.05s"><span>{icon('shield-check')}Last updated <time datetime="{PRIVACY['updated']}">{nice_date(PRIVACY['updated'])}</time></span></span>
      <h1 class="fade-up" style="--d:.15s">Privacy Notice</h1>
      <p class="lead fade-up" style="--d:.3s">{e(PRIVACY['lede'])}</p>
    </div>
  </div>
</section>
<section class="section tight flush-top">
  <div class="container">
    <div class="prose">
{content}
      <p><button type="button" class="btn btn-glass btn-sm" data-cookie-settings>Change Cookie Settings<span class="btn-ico">{icon('shield-check')}</span></button></p>
    </div>
  </div>
</section>"""
    meta = {'title': 'Privacy Notice | Econ Electrical', 'description': PRIVACY['lede'], 'path': '/privacy-notice/',
            'lastmod': PRIVACY['updated']}
    return meta, body


def page_simple(ctx, path, kicker, h1, lede, title):
    body = f'''
<section class="page-hero plain" style="min-height:clamp(560px,78vh,760px);align-items:center">
  <div class="container page-hero-inner">
    <div class="notice">
      <p class="kicker fade-up" style="--d:.05s"><span class="pulse"></span>{e(kicker)}</p>
      <h1 class="words">{words(h1)[0]}</h1>
      <p class="lead fade-up" style="--d:.45s">{e(lede)}</p>
      <div class="btn-row fade-up" style="--d:.6s">{btn(ctx.u('/'), 'Back to Home')}<a class="btn btn-glass plain" href="tel:{SITE['phone_href']}">{icon('phone')}&nbsp;{SITE['phone']}</a></div>
    </div>
  </div>
</section>'''
    return {'title': title, 'description': lede, 'path': path, 'noindex': True}, body


# ---------------------------------------------------------------- build

THUMB_H = {}


def make_thumbs():
    out_dir = os.path.join(ASSET_SRC, 'assets', 'img', 'thumbs')
    os.makedirs(out_dir, exist_ok=True)
    for key in MENU_THUMBS:
        src = os.path.join(ASSET_SRC, MANIFEST['images'][key]['variants'][-1]['path'])
        im = Image.open(src).convert('RGB')
        h = round(im.height * 480 / im.width)
        dest = os.path.join(out_dir, '%s-480.webp' % key)
        if not os.path.exists(dest):
            im.resize((480, h), Image.LANCZOS).save(dest, 'WEBP', quality=74, method=6)
        THUMB_H[key] = h


def all_pages():
    pages = [('/', page_home), ('/about-us/', page_about), ('/projects/', page_projects),
             (CONTACT, page_contact), ('/blog/', page_blog)]
    pages += [('/%s/' % s, (lambda s: lambda ctx: page_service(ctx, s))(s)) for s in SERVICE_ORDER]
    pages += [('/%s/' % s, (lambda s: lambda ctx: page_landing(ctx, s))(s)) for s in LANDING_ORDER]
    pages += [('/%s/' % RESIDENTIAL['slug'], page_residential)]
    pages += [('/%s/' % s, (lambda s: lambda ctx: page_project(ctx, s))(s)) for s in PROJECT_ORDER]
    pages += [('/%s/' % p['slug'], (lambda p: lambda ctx: page_post(ctx, p))(p)) for p in POSTS]
    pages += [('/privacy-notice/', page_privacy)]
    pages += [('/thank-you/', lambda ctx: page_simple(
        ctx, '/thank-you/', 'Message Sent', 'Thanks for Getting in Touch',
        'We’ll get back to you as soon as we can. If it’s urgent, call us on %s.' % SITE['phone'],
        'Thank You | Econ Electrical'))]
    return pages


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def copy_assets(out, mode):
    shutil.copytree(os.path.join(ASSET_SRC, 'assets'), os.path.join(out, 'assets'), dirs_exist_ok=True)
    # Publish the video folder under hashed names. Renaming rather than copying so a
    # file never ships under both names: the unhashed one would be dead weight in the
    # deploy and, worse, a second address serving the same bytes.
    for rel, hashed in _HASHED.items():
        src, dst = os.path.join(out, rel), os.path.join(out, hashed)
        if os.path.exists(src):
            os.replace(src, dst)
    shutil.copy(os.path.join(HERE, 'static', 'site.css'), os.path.join(out, 'assets', 'site.css'))
    shutil.copy(os.path.join(HERE, 'static', 'site.js'), os.path.join(out, 'assets', 'site.js'))


def build(mode):
    out = os.path.join(HERE, 'dist', mode)
    if os.path.exists(out):
        shutil.rmtree(out)
    copy_assets(out, mode)
    paths = []
    for path, fn in all_pages():
        ctx = Ctx(mode, path)
        meta, body = fn(ctx)
        doc = document(ctx, meta, body, mode == 'preview' and path == '/')
        target = os.path.join(out, 'index.html') if path == '/' else os.path.join(out, path.strip('/'), 'index.html')
        write(target, doc)
        paths.append((path, meta.get('noindex'), meta.get('lastmod')))
    if mode == 'site':
        ctx = Ctx(mode, '/404.html')
        meta, body = page_simple(ctx, '/404.html', 'Error 404', 'Page Not Found',
                                 'The page you’re looking for has moved or no longer exists.', 'Page Not Found | Econ Electrical')
        write(os.path.join(out, '404.html'), document(ctx, meta, body))
        write_site_extras(out, paths)
    return out


def write_site_extras(out, paths):
    urls = ''.join('  <url><loc>%s%s</loc>%s</url>\n' % (SITE['domain'], p, '<lastmod>%s</lastmod>' % lastmod if lastmod else '')
                   for p, noindex, lastmod in paths if not noindex)
    write(os.path.join(out, 'sitemap.xml'),
          '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % urls)
    write(os.path.join(out, 'robots.txt'), 'User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n' % SITE['domain'])
    # Short addresses for print, signage and QR codes. The roadside banner's QR
    # points at /solar, so this block is load bearing once anything is printed.
    redirects = ['# Short addresses for print, signage and QR codes',
                 '/solar  /home-solar-battery-installation/  301',
                 '/commercial-solar  /commercial-solar-pv-installation/  301',
                 '/ev  /commercial-ev-charging-installation/  301',
                 '/eicr  /eicr-fixed-wire-testing/  301',
                 '/led  /commercial-led-lighting/  301',
                 '/industrial  /industrial-electrical-contractors/  301',
                 # The full list used to be its own page before it was folded into
                 # /projects/. Nothing should still point here, but the address was
                 # live in the preview and costs one line to keep working.
                 '/projects/all  /projects/  301',
                 '/projects/all/  /projects/  301',
                 '', '# Posts folded into another that covers the same ground']
    redirects += ['/%s/  /%s/  301' % (old, new) for old, new in sorted(RETIRED_POSTS.items())]
    redirects += [
                 '', '# Old WordPress addresses', '/category/*  /blog/  301', '/feed  /blog/  301', '/feed/  /blog/  301',
                 '/wp-login.php  /  301', '/wp-admin/*  /  301', '/sitemap_index.xml  /sitemap.xml  301',
                 '/page-sitemap.xml  /sitemap.xml  301', '/post-sitemap.xml  /sitemap.xml  301',
                 '/category-sitemap.xml  /sitemap.xml  301', '', '# Old image addresses, so image search results keep working']
    for old, new in sorted(MANIFEST['old_paths'].items()):
        redirects.append('%s  /%s  301' % (old, new))
    write(os.path.join(out, '_redirects'), '\n'.join(redirects) + '\n')
    write(os.path.join(out, 'netlify.toml'), '''[build]
  publish = "."

[[headers]]
  for = "/*"
  [headers.values]
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    X-Frame-Options = "SAMEORIGIN"

[[headers]]
  for = "/assets/img/*"
  [headers.values]
    Cache-Control = "public, max-age=604800"

[[headers]]
  for = "/assets/video/*"
  [headers.values]
    # A year, and immutable, which is only safe because these filenames carry a hash
    # of their contents: a re-encode is published at a different address, so nobody
    # can be handed a stale copy. Under the old shared names this was a week, and a
    # week was still long enough to keep serving a superseded cut of the hero.
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/assets/fonts/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
''')


if __name__ == '__main__':
    make_thumbs()
    # Before anything is copied or rendered, so the pages and the published files
    # agree on the hashed names from the first byte written.
    hash_video_assets()
    for m in ('site', 'preview'):
        o = build(m)
        n = sum(len(fs) for _, _, fs in os.walk(o))
        size = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(o) for f in fs)
        print('%-8s %4d files  %.1f MB  -> %s' % (m, n, size / 1048576, o))
