"""Site videos: one encode, from an original, recorded here.

Why this file exists. The hero video was re-encoded in place by an ad hoc ffmpeg
command when the videos were brightened, and the original export had been lost
with the container, so that command re-compressed an already compressed file.
It went from 1280x960 at 1320 kbps down to 1024x732 at 523 kbps, which is the
quality drop Jonathan spotted on the main page. The lesson is the whole point of
this script: every clip is encoded ONCE, from a file in originals/, with the crop
and the grade applied in the same pass. Nothing is ever re-encoded from its own
output, and nothing is edited in place from the shell.

If a video needs changing, change the numbers here and run it again. If the file
in originals/ is missing the script says so and stops rather than quietly working
from the published copy and losing another generation.

originals/econ-hero-live.mp4 was recovered from the live site, which was still
serving the good version. It is itself a 1280x960 encode rather than the camera
original, so if the real export ever turns up, drop it in originals/, point SOURCE
at it and rerun: the result will be better again.
"""
import os
import subprocess
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(HERE, 'originals')
VDIR = os.path.join(HERE, '_assets', 'assets', 'video')
UP = '/mnt/user-data/uploads'

# Lift the picture without washing it out. A flat brightness offset raises the
# blacks along with everything else, which on a dark clip at a modest bitrate makes
# the compression blocking in the shadows plainly visible. A gamma curve lifts the
# midtones and shadows while leaving true black alone, and gamma 1.25 lands on the
# same average brightness as the flat +21/255 offset it replaces.
GRADE = 'eq=gamma=1.25:saturation=1.03'

# Square the pixels. The hero export is anamorphic: 1280x960 stored, but with a 4:3
# sample aspect ratio, so it is meant to be shown at 1706x916. A player honours that
# and looks right, but nothing else does. The poster frame came out 1280 wide and so
# appeared 25% squashed next to the video it was standing in for, and the width and
# height written into the page described the stored size rather than the displayed
# one, which reserves the wrong shape and shifts the page as the video arrives.
# Baking the ratio in costs nothing visible and means every tool downstream, now and
# later, can just read the file's dimensions and be right.
SQUARE = "scale='trunc(iw*sar/2)*2':ih,setsar=1"

# crop is width:height:x:y, measured off the source rather than assumed. The hero
# export is letterboxed with a 22px black bar top and bottom at 1280 wide: harmless
# on desktop, where a wide hero is cropped vertically anyway, but on a tall phone
# screen nothing is cropped and the bar sat across the top of the home page as a
# dark line. Taking it out of the file fixes it everywhere at once.
CLIPS = {
    'econ-team-on-site': {
        'source': os.path.join(ORIG, 'econ-hero-live.mp4'),
        'vf': 'crop=1280:916:0:22,%s,%s,fps=25' % (SQUARE, GRADE),
        # Squaring the pixels adds a third more of them, all horizontally interpolated,
        # so they carry no detail the source did not have. 25 rather than the 23 the
        # other two use gives those cheap pixels fewer bits and lands the file back at
        # 5 MB: checked frame by frame against 23 at 4x zoom and indistinguishable.
        # This autoplays on the home page, so the weight is worth caring about.
        'crf': '25',
        'poster_at': '4.2',
    },
    # The two project heroes still have their camera originals, so these are encoded
    # from 1080p and 4K rather than from anything the site has served before. 1280x720
    # rather than the 1152x648 they were: a project hero runs the full width of the
    # page, and the step up costs little from sources this good.
    'bus-depot-charging': {
        'source': os.path.join(UP, 'Copy_of_Final_with_audio.mp4'),
        # the first 26 seconds of a 40 second export, which is the cut that was published
        'trim': ['-t', '26'],
        'vf': 'scale=1280:720,%s,fps=24' % GRADE,
        'crf': '23',
        'poster_at': '2.0',
    },
    'factory-led-nottingham': {
        'source': os.path.join(UP, 'High Bay Lighting Project', 'complete.mp4'),
        # stops at 22.29s because the export ends on an Econ logo card, which looked
        # wrong sitting at the end of a looping background video
        'trim': ['-t', '22.29'],
        'vf': 'scale=1280:720,%s,fps=24' % GRADE,
        'crf': '23',
        'poster_at': '3.0',
    },
}

ENCODE = ['-an', '-c:v', 'libx264', '-preset', 'veryslow', '-profile:v', 'high',
          '-pix_fmt', 'yuv420p', '-movflags', '+faststart']

# A second, much smaller cut of every clip for phones. The desktop files are 3.5 to
# 5 MB each, which is a lot to push down a mobile connection for something playing
# behind a headline, and this is a site people open standing on a job. Half the
# width and a coarser CRF takes each one to roughly a fifth of the size; at the
# physical size a phone shows it, the difference is not visible. The page picks
# between the two in script, because Chromium ignores the media attribute on a
# video source (tested, it serves the desktop file to a 390px viewport).
MOBILE_SUFFIX = '-m'
MOBILE_CRF = '28'


def encode(name, spec):
    src = spec['source']
    if not os.path.exists(src):
        sys.exit('missing original for %s: %s\n'
                 'Put the original back in originals/ rather than re-encoding the '
                 'published file, which loses another generation.' % (name, src))
    out = os.path.join(VDIR, name + '.mp4')
    trim = spec.get('trim', [])
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src] + trim
                   + ['-vf', spec['vf'], '-crf', spec['crf']] + ENCODE + [out], check=True)

    # Poster from the same source and the same filter chain, so the still the page
    # shows before the video loads matches the first frame of the video itself.
    frame = os.path.join(HERE, '_frame.png')
    poster_vf = spec['vf'].replace(',fps=25', '').replace(',fps=24', '')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', spec['poster_at'], '-i', src,
                    '-frames:v', '1', '-vf', poster_vf, frame], check=True)
    Image.open(frame).convert('RGB').save(
        os.path.join(VDIR, name + '-poster.webp'), 'WEBP', quality=78, method=6)
    os.remove(frame)

    # The phone cut, from the same original and the same filter chain with a scale on
    # the end, so it is the identical picture rather than a separate edit that could
    # drift. Width halved and rounded to an even number, which h264 requires.
    mob = os.path.join(VDIR, name + MOBILE_SUFFIX + '.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src] + trim
                   + ['-vf', spec['vf'] + ",scale='trunc(iw/4)*2':-2",
                      '-crf', MOBILE_CRF] + ENCODE + [mob], check=True)

    def describe(path):
        d = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                            '-show_entries', 'stream=width,height', '-of', 'csv=p=0:s=x',
                            path], capture_output=True, text=True).stdout.strip()
        return '%s %5.2f MB' % (d, os.path.getsize(path) / 1048576)

    print('%-24s desktop %-20s phone %s' % (name, describe(out), describe(mob)))


def main():
    os.makedirs(VDIR, exist_ok=True)
    for name, spec in CLIPS.items():
        encode(name, spec)


if __name__ == '__main__':
    main()
