"""Compose a channel-style FR long-video thumbnail (offline, no API).

Base image: AI-generated (Higgsfield gpt_image_2_5) with Dr. Aksoy on the RIGHT third, navy/teal
science backdrop, and NO text. This script adds the type deterministically (correct accents):
white condensed caps keyword, gold accent line, gold pill label — the channel's recent style.
F13 / thumbnail library: no arrows, no red, no warning signs, no pen strikes or stamps, no %, no brands.

Usage:
  py -3.12 yt_thumb_compose.py --base base.png --out fr-thumb-00-slug-A.jpg \
     --line1 "GLP-1" --line2 "ET GROSSESSE ?" --pill "CE QUE DISENT LES ÉTUDES"
Writes the 1280×720 JPG (< 2 MB) and <out>-mobile.png (120×68 proof, ×4 enlarged).
"""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

W, H = 1280, 720
WHITE, GOLD, NAVY = (250, 248, 242), (240, 190, 80), (14, 30, 54)
FONT = "C:/Windows/Fonts/bahnschrift.ttf"  # variable: condensed width + bold weight


def cond(size: int, wght: int = 700, wdth: int = 75) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(FONT, size)
    try:
        vals = []
        for a in f.get_variation_axes():
            n = a["name"] if isinstance(a["name"], str) else a["name"].decode()
            vals.append(wght if "eight" in n else wdth if "idth" in n else a["default"])
        f.set_variation_by_axes(vals)
    except Exception as e:  # static font fallback
        print("variation fallback:", e)
    return f


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--line1", required=True, help="keyword, white, largest (e.g. GLP-1)")
    ap.add_argument("--line2", required=True, help="accent question, gold (e.g. ET GROSSESSE ?)")
    ap.add_argument("--pill", default="", help="gold label (e.g. CE QUE DISENT LES ÉTUDES)")
    ap.add_argument("--maxw", type=int, default=640, help="text column width in px")
    a = ap.parse_args()
    nb = lambda s: s.replace(" ?", "\u00a0?").replace(" !", "\u00a0!").replace(" :", "\u00a0:")

    img = Image.open(a.base).convert("RGB")
    img = img.resize((W, int(img.height * W / img.width)))
    top = (img.height - H) // 2
    img = img.crop((0, top, W, top + H))
    shade = Image.new("L", (W, H), 0)
    ds = ImageDraw.Draw(shade)
    for x in range(W):  # gentle wide falloff on the left so type reads on any backdrop
        ds.line([(x, 0), (x, H)], fill=int(150 * max(0.0, 1 - x / (W * 0.62)) ** 1.4))
    img = Image.composite(Image.new("RGB", (W, H), NAVY), img, shade)
    d = ImageDraw.Draw(img)

    def fit(text, maxw, start, wght=700):
        for s in range(start, 30, -2):
            f = cond(s, wght)
            b = d.textbbox((0, 0), text, font=f)
            if b[2] - b[0] <= maxw:
                return f, b
        return f, b

    def shadow_text(xy, text, font, fill):
        sh = Image.new("L", (W, H), 0)
        ImageDraw.Draw(sh).text(xy, text, font=font, fill=200)
        sh = sh.filter(ImageFilter.GaussianBlur(6))
        img.paste((0, 0, 0), (0, 0), sh.point(lambda v: int(v * 0.55)))
        ImageDraw.Draw(img).text(xy, text, font=font, fill=fill)

    X, y = 64, 70
    f1, b1 = fit(nb(a.line1), a.maxw, 230)
    shadow_text((X - b1[0], y - b1[1]), nb(a.line1), f1, WHITE)
    y += (b1[3] - b1[1]) + 26
    f2, b2 = fit(nb(a.line2), a.maxw, 120)
    shadow_text((X - b2[0], y - b2[1]), nb(a.line2), f2, GOLD)
    y += (b2[3] - b2[1]) + 40
    if a.pill:
        f3, b3 = fit(a.pill, a.maxw - 80, 52, 600)
        pw, ph = (b3[2] - b3[0]) + 44, (b3[3] - b3[1]) + 28
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((X, y, X + pw, y + ph), radius=10, fill=GOLD)
        d.text((X + 22 - b3[0], y + 14 - b3[1]), a.pill, font=f3, fill=NAVY)

    out = Path(a.out)
    img.save(out, quality=92)
    img.resize((120, 68), Image.LANCZOS).resize((480, 272), Image.NEAREST).save(out.with_name(out.stem + "-mobile.png"))
    kb = out.stat().st_size // 1024
    print(f"wrote {out} {kb} KB" + ("  WARNING: over 2 MB" if kb > 2048 else ""))


if __name__ == "__main__":
    main()
