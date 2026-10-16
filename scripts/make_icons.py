"""Regenerate the PWA / favicon icons from the official crest.

usage: python scripts/make_icons.py [static/img/logo-mark.png]
Writes static/img/icon-192.png and icon-512.png (crest centred on ivory)."""
import os
import sys

from PIL import Image

HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static', 'img')
src = sys.argv[1] if len(sys.argv) > 1 else next(
    (os.path.join(HERE, n) for n in ('logo-mark.png', 'logo-crest.png', 'crest.png') if os.path.exists(os.path.join(HERE, n))))
mark = Image.open(src).convert('RGBA')
for size in (192, 512):
    canvas = Image.new('RGBA', (size, size), (251, 248, 241, 255))
    m = mark.copy()
    m.thumbnail((int(size * .78), int(size * .78)), Image.LANCZOS)
    canvas.paste(m, ((size - m.width) // 2, (size - m.height) // 2), m)
    canvas.save(os.path.join(HERE, f'icon-{size}.png'))
print('icons written from', src)
