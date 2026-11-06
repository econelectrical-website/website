"""Turn the original WordPress uploads into web ready images for the new site.
Writes assets/img/... into build/_assets and a manifest (build/_assets/media.json)."""
import json, os, subprocess
from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'src', 'media-orig')
OUT = os.path.join(HERE, '_assets')

# key: (source path under uploads, output folder, kind)
# kind: photo (webp, 720/1440), wide (webp, 960/1920), team (square webp 640), logo (png, keep alpha)
P = 'photo'
MEDIA = {
    # home
    'home-about-site': ('2026/06/Econ-Electrical-About-Us-scaled.jpg', 'home', 'wide'),
    'home-cta-warehouse': ('2026/06/Econ-Electrical-Turnkey-Electrical-Solutions.png', 'home', P),
    'card-cummins': ('2026/08/Cummins-Turbo-Technologies.png', 'projects', P),
    'card-swan': ('2026/08/Swan-Civil-Engineering.png', 'projects', P),
    'card-saint': ('2026/08/Saint-Flooring-Group.png', 'projects', P),
    # services
    'installation-hero': ('2026/06/Econ-Electrical-Electrical-Installation.png', 'services', 'wide'),
    'installation-turnkey': ('2026/06/Econ-Electrical-Turnkey-Electrical-Solutions.png', 'services', P),
    'installation-subcontract': ('2026/06/Econ-Electrical-Sub-Contract-Partnership.png', 'services', P),
    'installation-ppm': ('2026/06/Econ-Electrical-PPM.png', 'services', P),
    'installation-reactive': ('2026/06/Econ-Electrical-Reactive-Maintenance.png', 'services', P),
    'areas-uk': ('2026/06/Econ-Electrical-Areas-We-Cover-2.png', 'services', P),
    'renewables-hero': ('2026/06/Econ-Electrical-Renewables.png', 'services', 'wide'),
    'renewables-solar': ('2026/06/Econ-Electrical-Solar-PV-Installation.png', 'services', P),
    'renewables-battery': ('2026/06/Econ-Electrical-Energy-Storage.png', 'services', P),
    'renewables-ev': ('2026/06/Econ-Electrical-EV-Charger-Installation.png', 'services', P),
    'compliance-hero': ('2026/06/Econ-Electrical-Compliance.png', 'services', 'wide'),
    'compliance-testing': ('2026/06/Econ-Electrical-Electrical-Testing.png', 'services', P),
    'compliance-thermal': ('2026/06/Econ-Electrical-Thermal-Imagin.png', 'services', P),
    'compliance-pat': ('2026/06/Econ-Electrical-PAT-Testing.png', 'services', P),
    'compliance-emergency': ('2026/06/Econ-Electrical-Emergency-Lighting.png', 'services', P),
    # about
    'about-vans': ('2026/10/Econ-Electrical-Vans.png', 'about', P),
    # team
    'team-jonathan': ('2024/07/Econ-Electrical-Team-Jonathan-e1720947206191.jpeg', 'team', 'team'),
    'team-robert': ('2024/07/Econ-Electrical-Team-Robert-e1720947629549.jpeg', 'team', 'team'),
    'team-ashley': ('2024/09/Econ-Electrical-Ash-e1726748149702.jpg', 'team', 'team'),
    'team-matthew': ('2024/11/Matt-finan-pic-e1730544215359.jpeg', 'team', 'team'),
    'team-max': ('2024/09/Econ-Electrical-Max-e1726748314170.jpg', 'team', 'team'),
    'team-cameron': ('2024/09/Econ-Electrical-Cam-e1726748420817.jpg', 'team', 'team'),
    # blog
    'blog-school-led': ('2024/02/responsive-led-lowers-energy-costs-theme.webp', 'blog', P),
    'blog-ev-chargers': ('2024/09/Econ-Electrical-EV-Chargers-8.jpg', 'blog', P),
    'blog-eicr': ('2024/09/Econ-Electrical-Electrical-Testing-and-inspection-5.jpg', 'blog', P),
    'blog-cctv': ('2024/11/CCTV-BLOG-PHOTO.jpeg', 'blog', P),
    'blog-led-wakefield': ('2025/02/Econ-Electrical-LED-Lighting-Wakefield.jpg', 'blog', P),
    'blog-thermal': ('2026/03/Thermal-Imaging.png', 'blog', P),
    'blog-solar': ('2026/03/Solar-Panels.png', 'blog', P),
    'blog-three-phase': ('2026/03/3-Phase-Upgrade.png', 'blog', P),
    'blog-surge': ('2026/03/Surge-Protection.png', 'blog', P),
    # partners and accreditations (white versions for dark backgrounds)
    'logo-solax': ('2026/09/Econ-Electrical-Solax-Power_white.png', 'logos', 'logo'),
    'logo-schneider': ('2026/09/Econ-Electrical-Schneider-Logo-White.png', 'logos', 'logo'),
    'logo-niceic': ('2026/09/NIC-LOGO-White-.png', 'logos', 'logo'),
    'logo-mcs': ('2026/09/MCS-White.png', 'logos', 'logo'),
    'logo-safecontractor': ('2026/09/Safe-Contractor-White.png', 'logos', 'logo'),
    # The Wakefield council car park project page was retired when the London bus
    # depot replaced it on /ev-installation/. One photo is still used by the schools
    # and councils article, so it is kept here on its own, under its original key so
    # the article does not need changing. The other four are no longer published.
    'ev-council-5': ('2024/09/Econ-Electrical-EV-Local-Council-1.jpg', 'projects/ev-council', P),
}
PROJECTS = {
    'cummins': ['2024/09/Econ-Electrical-Cummins-Project-%s.jpg' % n for n in ['1', '7', '2', '4', '5', '6']],
    'bm-packaging': ['2024/09/Econ-Electrical-Factory-Lighting-%s.png' % n for n in ['1', '2', '3']],
    'swan': ['2024/09/Econ-Electrical-Industrial-Unit-Install-%s.png' % n for n in ['3', '1', '11', '10', '9', '8', '7', '6', '5', '4', '2']],
    'saint': ['2024/09/Econ-Electrical-Saint-Group-Flooring-%s' % n for n in ['4.png', '6.png', '1.png', '8.jpg', '5.png', '3.png', '2.png']],
}
for proj, files in PROJECTS.items():
    for i, f in enumerate(files, 1):
        MEDIA['%s-%d' % (proj, i)] = (f, 'projects/' + proj, P)

def save_webp(im, path, q=76):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path, 'WEBP', quality=q, method=6)

def main():
    manifest = {'images': {}, 'old_paths': {}}
    for key, (src, folder, kind) in MEDIA.items():
        im = Image.open(os.path.join(SRC, src))
        im = ImageOps.exif_transpose(im)
        base = 'assets/img/%s/%s' % (folder, key.split('-', 1)[1] if folder.startswith('projects/') else key)
        entry = {'variants': [], 'src_old': src}
        if kind == 'logo':
            im = im.convert('RGBA')
            bbox = im.getchannel('A').getbbox()
            if bbox: im = im.crop(bbox)
            im.thumbnail((640, 240), Image.LANCZOS)
            out = base + '.png'
            os.makedirs(os.path.dirname(os.path.join(OUT, out)), exist_ok=True)
            im.save(os.path.join(OUT, out), optimize=True)
            entry['variants'].append({'path': out, 'w': im.width, 'h': im.height})
        elif kind == 'team':
            im = im.convert('RGB')
            s = min(im.size)
            im = ImageOps.fit(im, (s, s), Image.LANCZOS, centering=(0.5, 0.35))
            im = im.resize((640, 640), Image.LANCZOS) if s > 640 else im
            out = base + '.webp'
            save_webp(im, os.path.join(OUT, out), 80)
            entry['variants'].append({'path': out, 'w': im.width, 'h': im.height})
        else:
            im = im.convert('RGB')
            widths = (960, 1920) if kind == 'wide' else (720, 1440)
            ws = sorted(set([w for w in widths if w < im.width] + [min(im.width, widths[-1])]))
            for w in ws:
                h = round(im.height * w / im.width)
                v = im.resize((w, h), Image.LANCZOS) if w != im.width else im
                out = '%s-%d.webp' % (base, w)
                save_webp(v, os.path.join(OUT, out))
                entry['variants'].append({'path': out, 'w': w, 'h': h})
        manifest['images'][key] = entry
        manifest['old_paths']['/wp-content/uploads/' + src] = entry['variants'][-1]['path']

    # brand: stacked logo. The source is white on a solid black square, so the black is
    # keyed out (brightness becomes alpha) and the result trimmed, giving a transparent
    # white logo that sits cleanly over the hero video and any dark background.
    logo_src = Image.open(os.path.join(SRC, '2020/11/Econ-Electrical-Logo-e1778259493403.png')).convert('RGB')
    lum = logo_src.convert('L')
    logo = Image.new('RGBA', logo_src.size, (255, 255, 255, 0)); logo.putalpha(lum)
    logo = logo.crop(lum.getbbox())
    flat = Image.new('RGB', logo.size, (0, 0, 0)); flat.paste(logo, mask=logo.getchannel('A'))
    os.makedirs(os.path.join(OUT, 'assets/img/brand'), exist_ok=True)
    for h in (160, 320):
        w = round(logo.width * h / logo.height)
        logo.resize((w, h), Image.LANCZOS).save(os.path.join(OUT, 'assets/img/brand/econ-logo-%d.png' % h), optimize=True)
    manifest['logo'] = {'w': logo.width, 'h': logo.height}
    mark = Image.open(os.path.join(SRC, '2020/11/cropped-Trancparent-logo-1.png')).convert('RGBA')
    a = mark.getchannel('A'); bbox = a.getbbox(); a = a.crop(bbox)
    for size, name in ((32, 'favicon-32.png'), (180, 'apple-touch-icon.png'), (512, 'icon-512.png')):
        tile = Image.new('RGB', (size, size), (0, 0, 0))
        inner = round(size * 0.72)
        m = a.copy(); m.thumbnail((inner, inner), Image.LANCZOS)
        white = Image.new('RGB', m.size, (255, 255, 255))
        tile.paste(white, ((size - m.width) // 2, (size - m.height) // 2), m)
        tile.save(os.path.join(OUT, 'assets/img/brand/' + name), optimize=True)
    # Hero video: shrink, drop audio, add a poster frame.
    # The original export is letterboxed, with a black bar roughly 17px top and bottom
    # once scaled to 1024 wide. Desktop never showed it because object-fit: cover crops
    # the top and bottom off a wide hero, but on a tall phone screen nothing is cropped
    # vertically and the bar sat across the top of the page as a dark line. Crop it here
    # so the file itself is clean, rather than hiding it with CSS.
    vid_src = os.path.join(SRC, '2026/06/Econ-Hero-Video.mp4')
    vdir = os.path.join(OUT, 'assets/video'); os.makedirs(vdir, exist_ok=True)
    VF = 'scale=1024:768,crop=1024:732:0:18,fps=25'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', vid_src, '-an', '-vf', VF,
                    '-c:v', 'libx264', '-preset', 'veryslow', '-crf', '29', '-profile:v', 'high', '-pix_fmt', 'yuv420p',
                    '-movflags', '+faststart', os.path.join(vdir, 'econ-team-on-site.mp4')], check=True)
    frame = os.path.join(HERE, '_frame.png')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '4.2', '-i', vid_src, '-frames:v', '1',
                    '-vf', 'scale=1024:768,crop=1024:732:0:18', frame], check=True)
    pf = Image.open(frame).convert('RGB')
    save_webp(pf, os.path.join(vdir, 'econ-team-on-site-poster.webp'), 78)
    # social share card 1200x630: poster frame with the logo tile
    card = Image.new('RGB', (1200, 630), (0, 0, 0))
    ph = ImageOps.fit(pf, (760, 630), Image.LANCZOS, centering=(0.5, 0.45))
    card.paste(ph, (440, 0))
    lg = flat.resize((round(flat.width * 330 / flat.height), 330), Image.LANCZOS)
    card.paste(lg, ((440 - lg.width) // 2, (630 - lg.height) // 2))
    card.save(os.path.join(OUT, 'assets/img/brand/econ-social-card.jpg'), quality=86, optimize=True, progressive=True)
    os.remove(frame)
    json.dump(manifest, open(os.path.join(OUT, 'media.json'), 'w'), indent=1)
    total = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(OUT) for f in fs)
    print('images:', len(manifest['images']), 'total MB: %.1f' % (total / 1048576),
          'video MB: %.1f' % (os.path.getsize(os.path.join(vdir, 'econ-team-on-site.mp4')) / 1048576))

if __name__ == '__main__':
    main()
