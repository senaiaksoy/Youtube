"""EP01 v2 'IVF supplements' thumbnails in the EP02 series style (maroon panel + portrait, cream right side,
large maroon Bodoni word + dark sans question). Base = EP02 variant A with its right-side text erased."""
from PIL import Image, ImageDraw, ImageFont
import numpy as np
SRC = 'ep02-dhea-thumb-EN-A.jpg'
CREAM, INK, MAROON = (251, 247, 238), (36, 35, 33), (110, 22, 38)
base = np.array(Image.open(SRC).convert('RGB'))
# erase the old text row by row: start right of the doctor/gold edge (first long cream run), keep the suit
for y in range(120, 490):
    x = 520
    while x < 900:
        if (base[y, x:x + 12].astype(int).sum(axis=1) > 700).all(): break
        x += 1
    base[y, x + 8:1280] = CREAM
# sample the maroon used in the old serif word for an exact series match
def fit(d, text, font, maxw, size):
    while True:
        f = ImageFont.truetype(font, size); bb = d.textbbox((0, 0), text, font=f)
        if bb[2] - bb[0] <= maxw: return f, bb
        size -= 2
def make(big, small, out, big_size=230, small_size=86):
    im = Image.fromarray(base.copy()); d = ImageDraw.Draw(im)
    fb, bb = fit(d, big, r'C:\Windows\Fonts\BOD_B.TTF', 640, big_size)
    fs, sb = fit(d, small, r'C:\Windows\Fonts\arialbd.ttf', 600, small_size)
    cx = 912
    d.text((cx - (bb[2] - bb[0]) / 2 - bb[0], 345 - bb[3]), big, font=fb, fill=MAROON)
    d.text((cx - (sb[2] - sb[0]) / 2 - sb[0], 392 - sb[1]), small, font=fs, fill=INK)
    im.save(out, quality=92); print(out, fb.size, fs.size)
make('SUPPLEMENTS', 'What really helps?', 'ep01v2-supplements-thumb-EN-A.jpg')
make('BOTTLES', 'Did they count babies?', 'ep01v2-supplements-thumb-EN-B.jpg')
