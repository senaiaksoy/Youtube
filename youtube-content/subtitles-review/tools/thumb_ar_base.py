"""Text-free base image (ultrasound background + doctor cutout + left readability gradient) for the Arabic thumbnail."""
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter

SC = Path(r"C:\Users\KC3\AppData\Local\Temp\claude\D--A-klas-r-Youtube\698f879a-3ef4-4b5e-b7f2-8e5a23e113ee\scratchpad")
OUT = Path(r"D:\A-klasör\Youtube\youtube-content\subtitles-review\work\thumb_ar")
OUT.mkdir(exist_ok=True)
W, H = 1920, 1080

bg = Image.open(SC / "bg" / "bg1.png").convert("RGB")
bw = 2300
bg = bg.resize((bw, int(bw * bg.height / bg.width)), Image.LANCZOS)
x0 = max(0, min(bg.width - W, int(0.72 * bw) - 1060))
y0 = max(0, min(bg.height - H, int(0.45 * bg.height) - 520))
im = bg.crop((x0, y0, x0 + W, y0 + H)).convert("RGBA")

c = Image.open(SC / "cut_12.5.png")
scale = 1080 / c.height * 1.18
c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
rgb = ImageEnhance.Brightness(ImageEnhance.Contrast(ImageEnhance.Color(c.convert("RGB")).enhance(1.08)).enhance(1.10)).enhance(1.18)
c = Image.merge("RGBA", (*rgb.split(), c.split()[3]))
x, y = W - c.width + 230, -55
a = c.split()[3]
glow = Image.new("RGBA", c.size, (60, 200, 200, 0))
glow.putalpha(a.filter(ImageFilter.GaussianBlur(38)).point(lambda v: int(v * 0.55)))
im.alpha_composite(glow, (x, y))
im.alpha_composite(c, (x, y))

ov = Image.new("RGBA", (W, H))
px = ov.load()
for xx in range(W):
    al = max(0.0, 1 - xx / 1000) ** 1.3
    for yy in range(H):
        px[xx, yy] = (6, 22, 34, int(215 * al))
im = Image.alpha_composite(im, ov)
im.convert("RGB").save(OUT / "base.jpg", quality=95)
print("base saved", (OUT / "base.jpg").stat().st_size // 1024, "KB")
