"""EN first-ultrasound thumbnail in the FR channel style (MoApIs3-WwE cover A): ultrasound background + doctor cutout,
cream/gold Arial Black stacked question on the left, gold pill subtitle. Base = text-free FR base (thumb_ar_base.py)."""
from PIL import Image, ImageDraw, ImageFont
BASE = r"D:\A-klasör\Youtube\youtube-content\subtitles-review\work\thumb_ar\base.jpg"
FONT = r"C:\Windows\Fonts\ariblk.ttf"
CREAM, GOLD, INK = (247, 243, 233), (236, 189, 112), (24, 24, 30)

def make(lines, pill, out, size=170, maxw=900):
    im = Image.open(BASE).convert("RGB"); d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, size)
    while max(d.textlength(t, font=f) for t, _ in lines) > maxw:
        size -= 4; f = ImageFont.truetype(FONT, size)
    x, y, lh = 80, 120, int(size * 1.2)
    for t, col in lines:
        d.text((x + 6, y + 6), t, font=f, fill=(0, 0, 0))  # hard drop shadow as in FR cover
        d.text((x, y), t, font=f, fill=col); y += lh
    pf = ImageFont.truetype(FONT, 62)
    pw = d.textlength(pill, font=pf); bb = d.textbbox((0, 0), pill, font=pf)
    py = y + 20
    d.rounded_rectangle((x - 10, py, x + pw + 50, py + 100), radius=22, fill=GOLD)
    d.text((x + 20, py + 50 - (bb[1] + bb[3]) / 2), pill, font=pf, fill=INK)
    im.save(out, quality=92); print(out, size)

make([("IS THE", CREAM), ("HEART", CREAM), ("BEATING?", GOLD)], "FIRST IVF SCAN", "echo-heartbeat-thumb-EN-FRstyle-A.jpg")
make([("HEARTBEAT", CREAM), ("AT 6", CREAM), ("WEEKS?", GOLD)], "FIRST IVF SCAN", "echo-heartbeat-thumb-EN-FRstyle-B.jpg")
