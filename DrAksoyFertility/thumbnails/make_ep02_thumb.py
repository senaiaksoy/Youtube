from PIL import Image, ImageDraw, ImageFont
import numpy as np, sys
SRC = r'D:\A-klasör\openmontage\projects\dhea-fr-recut-2026-10-04-v3\artifacts\dhea-thumbnail-fr-premium-v2.jpg'
CREAM, INK = (251, 247, 238), (36, 35, 33)
base = np.array(Image.open(SRC).convert('RGB'))
# erase the French subtitle line, row by row, stopping short of the suit edge
for y in range(384, 480):
    x = 560
    while x < 760 and base[y, x].astype(int).sum() < 400: x += 1
    base[y, max(x + 6, 630):1270] = CREAM
def make(text, out, font='arialbd.ttf'):
    im = Image.fromarray(base.copy()); d = ImageDraw.Draw(im)
    # size so cap height ~ the original (~79 px) but never wider than 610 px
    size = 108
    while True:
        f = ImageFont.truetype(font, size); bb = d.textbbox((0, 0), text, font=f)
        if bb[2] - bb[0] <= 610: break
        size -= 2
    w = bb[2] - bb[0]; cx = 942
    cap = d.textbbox((0, 0), 'H', font=f)
    y = 391 - cap[1]   # align cap top with the original line
    d.text((cx - w / 2 - bb[0], y), text, font=f, fill=INK)
    im.save(out, quality=92); print(out, 'font size', size, 'width', w)
make('Help or hype?', 'ep02-dhea-thumb-EN-A.jpg')
make('Worth it for IVF?', 'ep02-dhea-thumb-EN-B.jpg')
