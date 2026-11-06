"""Rebuild _assets/media.json from already processed files.

The original WordPress uploads are no longer on disk, but every processed
image from the last deploy is. This walks those files and reconstructs the
manifest that build.py reads, using the same key to path rules as media.py.
"""
import json, os, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '_assets')
sys.path.insert(0, HERE)
from media import MEDIA  # noqa: E402

manifest = {'images': {}, 'old_paths': {}}
missing = []

for key, (src, folder, kind) in MEDIA.items():
    name = key.split('-', 1)[1] if folder.startswith('projects/') else key
    base = 'assets/img/%s/%s' % (folder, name)
    entry = {'variants': [], 'src_old': src}
    # Always scan the folder rather than guessing filenames. media.py clamps the
    # largest width to the source image, so plenty of variants are odd sizes like
    # 1200 or 1174 and would be missed by looking only for 720/1440. Dropping one
    # that way is silent: the page still builds, it just serves the small file to
    # everyone and looks soft on a retina screen.
    d = os.path.dirname(base)
    stem = os.path.basename(base)
    full = os.path.join(OUT, d)
    found = []
    if os.path.isdir(full):
        for f in sorted(os.listdir(full)):
            fbase, ext = os.path.splitext(f)
            if ext.lower() not in ('.webp', '.png', '.jpg', '.jpeg'):
                continue
            if fbase == stem or (fbase.startswith(stem + '-') and fbase[len(stem) + 1:].isdigit()):
                p = os.path.join(full, f)
                with Image.open(p) as im:
                    found.append({'path': '%s/%s' % (d, f), 'w': im.width, 'h': im.height})
    if not found:
        missing.append(key)
        continue
    found.sort(key=lambda v: v['w'])
    entry['variants'] = found
    manifest['images'][key] = entry
    manifest['old_paths']['/wp-content/uploads/' + src] = found[-1]['path']

# generated artwork, normally registered by render_art.py
for key, paths in (('home-energy-art', ['assets/img/residential/home-energy-art-960.webp',
                                        'assets/img/residential/home-energy-art-1920.webp']),
                   ('home-energy-og', ['assets/img/residential/home-energy-og.jpg'])):
    vs = []
    for p in paths:
        f = os.path.join(OUT, p)
        if os.path.exists(f):
            with Image.open(f) as im:
                vs.append({'path': p, 'w': im.width, 'h': im.height})
    if vs:
        manifest['images'][key] = {'variants': vs, 'src_old': 'illustration.py'}

logo = os.path.join(OUT, 'assets/img/brand/econ-logo-320.png')
with Image.open(logo) as im:
    manifest['logo'] = {'w': im.width, 'h': im.height}

json.dump(manifest, open(os.path.join(OUT, 'media.json'), 'w'), indent=1)
print('images:', len(manifest['images']), 'missing:', missing or 'none')
