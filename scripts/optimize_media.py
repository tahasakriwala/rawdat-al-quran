"""Copy downloaded wp-content/uploads media into static/media, resized for the web.

usage: python scripts/optimize_media.py <downloaded_uploads_dir> [static/media]
Skips anything that isn't a real image/audio file (e.g. an HTML error page)."""
import os
import shutil
import sys

from PIL import Image, ImageOps

SRC = sys.argv[1]
DST = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(__file__), '..', 'static', 'media')


def limit_for(rel):
    r = rel.lower()
    if '/2019/05/' in r:                 # student portraits
        return 640
    if 'newsletter' in r or 'page-0' in r or 'presentation' in r:
        return 1800                      # keep newsletter pages readable
    return 1600


ok = bad = 0
for root, _, files in os.walk(SRC):
    for f in files:
        src = os.path.join(root, f)
        rel = os.path.relpath(src, SRC)
        out = os.path.join(DST, rel)
        if os.path.exists(out) and '--force' not in sys.argv:
            continue
        os.makedirs(os.path.dirname(out), exist_ok=True)
        ext = f.lower().rsplit('.', 1)[-1]
        if ext == 'mp3':
            with open(src, 'rb') as fh:
                head = fh.read(3)
            if head[:3] == b'ID3' or head[:2] in (b'\xff\xfb', b'\xff\xf3', b'\xff\xf2'):
                shutil.copyfile(src, out); ok += 1
            else:
                bad += 1
            continue
        try:
            im = Image.open(src)
            im = ImageOps.exif_transpose(im)
            m = limit_for(rel)
            if max(im.size) > m:
                im.thumbnail((m, m), Image.LANCZOS)
            if ext in ('jpg', 'jpeg'):
                im.convert('RGB').save(out, 'JPEG', quality=78, optimize=True, progressive=True)
            else:
                im.save(out, optimize=True)
            ok += 1
        except Exception as e:  # not an image
            bad += 1
            print('skip', rel, e.__class__.__name__)
print('ok', ok, 'skipped', bad)
