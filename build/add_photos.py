"""Process new project photography into web assets and register it.

The original WordPress uploads that media.py works from are long gone, so any
project added from here on is processed through this script instead. Output
matches media.py's 'photo' kind exactly: webp at 720 and 1440 wide.

To add a project: drop its photos somewhere readable, add an entry to SHOOTS
keyed by the project's `media` prefix, listing the files in gallery order, then
run this script and rebuild. The first photo is usually the card image too.
"""
import json, os, sys
from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '_assets')
ATT = '/mnt/user-data/attachments/5a2101c9-8fdc-5e88-b6dc-469f7e45ed42'
UP = '/mnt/user-data/uploads'

# A value is either a list of (directory, filename) in gallery order, or a dict
# with 'start' and 'files' when the photos are being added to a project that
# already has some, so the numbering carries on rather than overwriting.
#
# An entry may carry a third item, a crop as fractions of the frame
# (left, top, right, bottom). That is how a client's signage is kept out of a
# photo on a job we have agreed not to name, done here so the crop is recorded
# and survives a rebuild rather than living in an edited file somewhere.
SHOOTS = {
    # extra photos added to the original Cummins set, which runs 1 to 6
    'cummins': {'start': 7, 'files': [
        (UP + '/Cummins', '20241227_115128.jpg'),   # assembly line framework under build
        (UP + '/Cummins', '20241228_094138.jpg'),   # control panel internals, pneumatics and terminals
        (UP + '/Cummins', '20241228_111819.jpg'),   # terminal rails wired out in a station enclosure
    ]},
    # Scotland bus depot, same client as the London depot and not named
    'scotdepot': [
        (UP + '/Scotland DC chargers Project', '20250717_095341.jpg'),   # engineer fixing containment to the wall
        (UP + '/Scotland DC chargers Project', '20250715_152640.jpg'),   # setting out with the laser level
        (UP + '/Scotland DC chargers Project', '20250717_095345.jpg'),   # team working the containment run
        (UP + '/Scotland DC chargers Project', '20250723_093732.jpg'),   # completed run with cable drums on site
        (UP + '/Scotland DC chargers Project', '20250723_093750.jpg'),   # containment the length of the depot wall
        # cropped off the right hand side: the operator's building sign and a
        # branded coach and van sat in the original frame
        (UP + '/Scotland DC chargers Project', '20250729_130608 (1).jpg', (0.09, 0.10, 0.76, 1.0)),
        (UP + '/Scotland DC chargers Project', '20250729_130609.jpg', (0.09, 0.10, 0.76, 1.0)),
        (UP + '/Scotland DC chargers Project', 'PHOTO-2025-10-31-10-34-05.jpg'),  # LV panel, ways labelled
        (UP + '/Scotland DC chargers Project', 'PHOTO-2025-10-31-10-40-28.jpg'),  # terminating inside the cabinet
        # cropped in from the left, away from the lettering painted on the wall
        (UP + '/Scotland DC chargers Project', 'PHOTO-2025-10-31-10-40-29.jpg', (0.28, 0.0, 1.0, 1.0)),
    ],
    # Saint Flooring Group, Nottingham: fluorescent stripped out, UFO LED retrofit
    'highbaynotts': [
        (UP + '/High Bay Lighting Project', 'DJI_20241024145423_0099_D.JPG'),
        (UP + '/High Bay Lighting Project', 'DJI_20241021134335_0078_D.JPG'),
        (UP + '/High Bay Lighting Project', 'DJI_20241021134348_0079_D.JPG'),
        (UP + '/High Bay Lighting Project', 'DJI_20241021134317_0077_D (2).JPG'),
        (UP + '/High Bay Lighting Project', 'DJI_20241024145438_0100_D.JPG'),
    ],
    # London bus depot EV fleet charging
    'busdepot': [
        (ATT, 'd736aae8-image.png'),                  # two engineers terminating the chargers
        (ATT, '7116dfe3-image.jpg'),                  # finished chargers, green status, bollards
        (ATT, 'aab67c83-image.jpg'),                  # power cabinets behind the crash barrier
        (UP, '20250708_113258.jpg'),                  # LV switchboard with the riser up to roof level
        (UP, '20250708_113405.jpg'),                  # LV cable bundle running the length of the tray
        (UP, 'DJI_20250708135611_0289_D__1_.JPG'),    # bus alongside the wall mounted chargers
        (ATT, '89e7bd7e-image.jpg'),                  # wide bay, containment the length of the wall
        (ATT, 'b652e940-image.jpg'),                  # charger bay with bollards and containment
    ],
    # Devitech: DC charger for the truck fleet at the rear, four AC chargers at the front
    'devitechdcac': [
        (UP + '/Devitech DC & AC Project', 'D6.jpeg'),    # the installed DC charger
        (UP + '/Devitech DC & AC Project', 'd15.jpeg'),   # DC charger craned into position
        (UP + '/Devitech DC & AC Project', 'WhatsApp Image 2026-11-04 at 11.27.21.jpeg'),
        (UP + '/Devitech DC & AC Project', 'D4.jpeg'),    # labelled board: DC EVSE rear, front EVSE 1-4
        (UP + '/Devitech DC & AC Project', 'D10.jpeg'),   # high level containment from the panel board
        (UP + '/Devitech DC & AC Project', 'D11.jpeg'),   # isolator and containment drop
        (UP + '/Devitech DC & AC Project', 'D13.jpeg'),   # panel board and switchgear
        (UP + '/Devitech DC & AC Project', 'D14.jpeg'),   # AC charger at the front
        (UP + '/Devitech DC & AC Project', 'd12.jpeg'),   # front of the building, staff car charging
    ],
    # Devitech, Reading: four DC chargers, supply cabling and containment
    'dcreading': [
        (UP + '/DC Chargers Reading Project', 'f10.jpeg'),  # engineer working in the panel
        (UP + '/DC Chargers Reading Project', 'f3.jpeg'),   # main board locked off for the shutdown
        (UP + '/DC Chargers Reading Project', 'f1.jpeg'),   # new cables into the plant room panels
        (UP + '/DC Chargers Reading Project', 'f5.jpeg'),   # four supply cables glanded into the enclosure
        (UP + '/DC Chargers Reading Project', 'f6.jpeg'),   # glands and earthing detail
        (UP + '/DC Chargers Reading Project', 'f7.jpeg'),   # containment with fire stopping
        (UP + '/DC Chargers Reading Project', 'f2.jpeg'),   # containment run through the plant room
        (UP + '/DC Chargers Reading Project', 'f4.jpeg'),   # distribution board
        (UP + '/DC Chargers Reading Project', 'f8.jpeg'),   # external duct route to the charger positions
    ],
    # Manningham Concrete, Bradford: 50 kW commercial roof mounted solar PV
    'solarbradford': [
        (UP + '/Solar Bradford Project', 'MAIN SOLAR.jpeg'),
        (UP + '/Solar Bradford Project', 'Solar1.jpeg'),
        (UP + '/Solar Bradford Project', 'SOLAR.jpeg'),
        (UP + '/Solar Bradford Project', '20260729_131036.jpg'),
        (UP + '/Solar Bradford Project', 'IMG_20260729_124728_10_132_PureShot.jpg'),
        (UP + '/Solar Bradford Project', '20260729_125812.jpg'),
        (UP + '/Solar Bradford Project', 'Solar pic.jpeg'),
        (UP + '/Solar Bradford Project', '20260729_125826.jpg'),
    ],
}


def save_webp(im, path, q=76):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path, 'WEBP', quality=q, method=6)


def main(only=None):
    m = json.load(open(os.path.join(OUT, 'media.json')))
    for prefix, shots in SHOOTS.items():
        if only and prefix != only:
            continue
        start, shots = (shots['start'], shots['files']) if isinstance(shots, dict) else (1, shots)
        for i, shot in enumerate(shots, start):
            d, fn, crop = shot if len(shot) == 3 else (shot[0], shot[1], None)
            src = os.path.join(d, fn)
            if not os.path.exists(src):
                print('  MISSING', src)
                continue
            im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
            if crop:
                w, h = im.size
                l, t, r, b = crop
                im = im.crop((round(w * l), round(h * t), round(w * r), round(h * b)))
            key = '%s-%d' % (prefix, i)
            base = 'assets/img/projects/%s/%d' % (prefix, i)
            # never upscale, and skip a second variant that would sit on top of the first
            widths = sorted({w for w in (720, 1440) if w < im.width} | {min(im.width, 1440)})
            if len(widths) == 2 and widths[1] < widths[0] * 1.3:
                widths = widths[1:]
            variants = []
            for w in widths:
                h = round(im.height * w / im.width)
                v = im.resize((w, h), Image.LANCZOS) if w != im.width else im
                p = '%s-%d.webp' % (base, w)
                save_webp(v, os.path.join(OUT, p))
                variants.append({'path': p, 'w': w, 'h': h})
            m['images'][key] = {'variants': variants, 'src_old': fn}
            print(key, im.size, '->', [v['w'] for v in variants])
    json.dump(m, open(os.path.join(OUT, 'media.json'), 'w'), indent=1)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else None)
