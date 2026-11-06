"""Team portraits.

The van shoot replaces four of the six headshots. media.py cannot do this job
because it rebuilds from the old WordPress library, and these photos never went
near WordPress, so the crops live here where they are recorded and survive a
rebuild rather than sitting in an edited file somewhere.

FACE holds the centre of each man's face in pixels of his own frame, measured off
the originals. Everything else is derived from it, so the framing stays consistent
across the six tiles: same head size, same amount of head room, eyes on the same
line. That consistency is the only reason a grid of portraits looks deliberate
rather than like six photos that happen to be next to each other.

Matthew is a separate case. The photo on the page is one the lads are not happy
with and there is no replacement yet, so his tile is blurred back to a dark card
instead: he stays listed, his face is not on show, and the tile reads as a
deliberate placeholder rather than a mistake. Swap in a real photo when there is
one and delete the BLUR block.
"""
import json
import os
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
# The camera originals, straight off Jonathan's machine, rather than the copies that
# came through the chat: same four photographs, but 3000x4000 instead of 1932x2576
# and without a second round of compression. His own file names are what confirmed
# which man is which, so the mapping below is his, not a guess from the faces.
UP = '/mnt/user-data/uploads/Downloads'
OUT = os.path.join(HERE, '_assets')
TEAM_DIR = 'assets/img/team'

# key -> (source file, face centre x, face centre y) in pixels of the 3000x4000 frame,
# after EXIF rotation is applied. The files are stored landscape with a rotate flag,
# so anything that reads them without honouring it measures the wrong axis.
FACE = {
    'ashley':  ('Ash.jpg', 1543, 1314),
    'robert':  ('Rob.jpg', 1467, 1579),
    'cameron': ('Cam.jpg', 1500, 1346),
    'max':     ('Max.jpg', 1416, 1613),
}

# Square side, and where down that square the face centre sits. 0.44 leaves head
# room above and brings the shoulders and the branded polo into the bottom of the
# frame; much higher and the chin crowds the lower edge. 900 is as tight as the
# crop goes before the Econ badge on the polo drops out of shot, which is worth
# keeping: it is the only thing in these four tiles that says who they work for.
SIDE = 1398
FACE_Y = 0.44

# Two variants. The tile is about 30vw on a wide screen, so on a retina display it
# is asked for roughly 900 device pixels and a lone 640 looks soft. The crop is the
# ceiling, so the large variant is whatever SIDE allows rather than a fixed number.
WIDTHS = (640, 1280)


def square(im, cx, cy, side):
    """Crop a square around a face, nudged back inside the frame if it overhangs."""
    left, top = cx - side // 2, cy - round(side * FACE_Y)
    left = max(0, min(left, im.width - side))
    top = max(0, min(top, im.height - side))
    return im.crop((left, top, left + side, top + side))


def write(im, key):
    variants = []
    # never upscale, and skip a second variant that would sit on top of the first
    widths = sorted({min(w, im.width) for w in WIDTHS})
    if len(widths) == 2 and widths[1] < widths[0] * 1.3:
        widths = widths[1:]
    for w in widths:
        v = im.resize((w, w), Image.LANCZOS)
        rel = '%s/team-%s%s.webp' % (TEAM_DIR, key, '' if w == widths[0] else '-%d' % w)
        v.save(os.path.join(OUT, rel), 'WEBP', quality=86, method=6)
        variants.append({'path': rel, 'w': w, 'h': w})
    return variants


def blurred_card(src, side=640):
    """Matthew's tile: his photo blurred past recognition and sunk into black.

    The blur is done on a downscale and then enlarged, which destroys the detail
    rather than merely smearing it, so nothing comes back by sharpening the file.
    """
    im = Image.open(src).convert('RGB')
    s = min(im.size)
    im = im.crop(((im.width - s) // 2, 0, (im.width - s) // 2 + s, s)).resize((side, side), Image.LANCZOS)
    small = im.resize((side // 26, side // 26), Image.LANCZOS)
    im = small.resize((side, side), Image.BICUBIC).filter(ImageFilter.GaussianBlur(18))
    # Sink the edges into the panel colour so the tile has no hard border, but leave
    # the middle alone: the grid sits on a near black page, and a tile darkened all
    # over disappears into it and reads as an image that failed to load.
    dark = Image.new('RGB', (side, side), (12, 14, 12))
    mask = Image.new('L', (side, side), 0)
    for i in range(side // 2):
        v = int(255 * (i / (side / 2)) ** 0.8)
        mask.paste(v, (i, i, side - i, side - i))
    im = Image.composite(im, dark, mask.filter(ImageFilter.GaussianBlur(40)))

    # Finally match the brightness of the photographed tiles, which average about 62
    # once the grid's greyscale filter is applied. Matching it is what makes this read
    # as a deliberately soft portrait sitting among five sharp ones, rather than a hole
    # in the grid. Measured, not guessed, so it stays right if the blur above is retuned.
    g = ImageOps.grayscale(im)
    px = list(g.resize((80, 80)).tobytes())
    mean = sum(px) / len(px)
    if mean > 1:
        im = ImageEnhance.Brightness(im).enhance(min(3.0, 62.0 / mean))
    return im


def main():
    man = json.load(open(os.path.join(OUT, 'media.json')))
    os.makedirs(os.path.join(OUT, TEAM_DIR), exist_ok=True)

    for key, (fn, cx, cy) in FACE.items():
        im = ImageOps.exif_transpose(Image.open(os.path.join(UP, fn))).convert('RGB')
        variants = write(square(im, cx, cy, SIDE), key)
        entry = man['images'].setdefault('team-' + key, {})
        entry['variants'] = variants
        entry.pop('src_old', None)          # no longer a WordPress image
        print('team-%-8s %s' % (key, [v['w'] for v in variants]))

    # Always blur from the untouched original, never from the published tile, or a
    # second run blurs an already blurred image and the file degrades a step each time.
    # The original lives in originals/, deliberately outside _assets: everything under
    # _assets/assets is copied wholesale to the live site, so an unblurred copy left
    # there would be served to anyone who asked for it and the blur would be pointless.
    src = os.path.join(OUT, TEAM_DIR, 'team-matthew.webp')
    card = blurred_card(os.path.join(HERE, 'originals', 'team-matthew.webp'))
    card.save(src, 'WEBP', quality=84, method=6)
    man['images']['team-matthew'] = {'variants': [{'path': '%s/team-matthew.webp' % TEAM_DIR,
                                                   'w': card.width, 'h': card.height}]}
    print('team-matthew blurred to a dark card')

    json.dump(man, open(os.path.join(OUT, 'media.json'), 'w'), indent=1, sort_keys=True)


if __name__ == '__main__':
    main()
