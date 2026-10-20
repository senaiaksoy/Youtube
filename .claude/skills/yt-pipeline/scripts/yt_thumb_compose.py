# -*- coding: utf-8 -*-
"""Compose diversified channel-style long-video thumbnails (offline, no API).

Supports 5 visual templates learned from @SenaiAksoy (FR), @DocentDrSenaiAksoy (TR),
and @DrAksoyFertility (EN), plus left/right text placement, optional 3rd line,
optional numeric comparison chip (e.g. '10 -> ?'), and automatic rotation checking
against references/thumb-log.json so consecutive thumbnails never look identical.

Templates (--template):
  1. classic-gold   : White line1 + Gold line2 + Gold pill (dark backdrop)
  2. yellow-focus   : Heavy yellow outlined hook lines + White pill bottom/top (FR pqc9UgCIqo0 / TR U8vAciGqvSU)
  3. coral-contrast : White line1 + Coral/terracotta line2 + Coral pill + optional numeric chip (FR 2QpLE_wST1s)
  4. amber-eyebrow  : Top eyebrow badge + White/Amber 2-3 line stack with strong stroke (FR MoApIs3-WwE / SD3CKpN6VS0)
  5. light-card     : Light cream/clinical split backdrop with deep Navy + Burgundy/Coral type (FR Ks0Cwpy_a4A / TR P7CdnSIAOFI)

Text side (--side):
  - left  : Doctor on RIGHT third, text on LEFT (default)
  - right : Doctor on LEFT third, text on RIGHT (FR zhcapjJhxzA / x8VzlUmEQEw)

Variety gate:
  Pass --check-variety (with --channel, --outfit, --pose, --backdrop) to verify against
  references/thumb-log.json before finalizing, and --log-variety to record the chosen design.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

W, H = 1280, 720
FONT = "C:/Windows/Fonts/bahnschrift.ttf"
LOG_PATH = Path(__file__).resolve().parent.parent / "references" / "thumb-log.json"

PALETTES = {
    "classic-gold": {
        "shade": (14, 30, 54),
        "shade_alpha": 150,
        "line1": (250, 248, 242),
        "line2": (240, 190, 80),
        "line3": (240, 190, 80),
        "stroke": None,
        "stroke_w": 0,
        "pill_bg": (240, 190, 80),
        "pill_fg": (14, 30, 54),
        "pill_pos": "bottom-stack",
        "wdth": 75,
    },
    "yellow-focus": {
        "shade": (10, 24, 44),
        "shade_alpha": 145,
        "line1": (255, 214, 0),
        "line2": (255, 214, 0),
        "line3": (250, 248, 242),
        "stroke": (15, 15, 15),
        "stroke_w": 5,
        "pill_bg": (250, 248, 242),
        "pill_fg": (17, 17, 17),
        "pill_pos": "corner-bottom",
        "wdth": 88,
    },
    "coral-contrast": {
        "shade": (18, 34, 48),
        "shade_alpha": 155,
        "line1": (250, 248, 242),
        "line2": (232, 104, 80),
        "line3": (250, 248, 242),
        "stroke": (14, 22, 32),
        "stroke_w": 3,
        "pill_bg": (214, 86, 64),
        "pill_fg": (250, 248, 242),
        "pill_pos": "bottom-stack",
        "wdth": 82,
    },
    "amber-eyebrow": {
        "shade": (12, 28, 48),
        "shade_alpha": 150,
        "line1": (250, 248, 242),
        "line2": (245, 184, 65),
        "line3": (245, 184, 65),
        "stroke": (12, 20, 32),
        "stroke_w": 4,
        "pill_bg": (245, 184, 65),
        "pill_fg": (14, 26, 44),
        "pill_pos": "eyebrow",
        "wdth": 80,
    },
    "light-card": {
        "shade": (246, 242, 234),
        "shade_alpha": 225,
        "line1": (20, 38, 64),
        "line2": (156, 42, 58),
        "line3": (20, 38, 64),
        "stroke": None,
        "stroke_w": 0,
        "pill_bg": (20, 38, 64),
        "pill_fg": (250, 248, 242),
        "pill_pos": "bottom-stack",
        "wdth": 80,
    },
}

OUTFITS = ("scrubs", "white-coat", "shirt", "coat-blue-shirt")
POSES = ("chin", "open-hands", "pointing", "calm-clasped")
BACKDROPS = (
    "ultrasound",
    "embryo-microscope",
    "clinic-warm",
    "bottles-props",
    "chart-data",
    "light-editorial",
    "anatomy-3d",
    "cells-molecules",
)


def cond(size: int, wght: int = 700, wdth: int = 75) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(FONT, size)
    try:
        vals = []
        for a in f.get_variation_axes():
            n = a["name"] if isinstance(a["name"], str) else a["name"].decode()
            vals.append(wght if "eight" in n else wdth if "idth" in n else a["default"])
        f.set_variation_by_axes(vals)
    except Exception:
        pass
    return f


def load_log() -> list[dict]:
    if not LOG_PATH.exists():
        return []
    return json.loads(LOG_PATH.read_text(encoding="utf-8"))


def check_variety(
    entries: list[dict],
    channel: str,
    template: str,
    side: str,
    outfit: str | None,
    pose: str | None,
    backdrop: str | None,
) -> list[str]:
    """Return a list of variety violations against the most recent entries."""
    issues: list[str] = []
    if not entries:
        return issues

    ch_entries = [e for e in entries if e.get("channel") == channel]
    recent_any = entries[-1]
    recent_ch = ch_entries[-1] if ch_entries else recent_any

    if recent_ch.get("template") == template:
        issues.append(
            f"template '{template}' was just used on {channel} ({recent_ch.get('video') or recent_ch.get('slug')}); pick a different --template."
        )
    if outfit and recent_ch.get("outfit") == outfit and recent_ch.get("pose") == pose:
        issues.append(
            f"same outfit+pose ({outfit} + {pose}) as the previous {channel} video; rotate outfit or pose."
        )
    if pose and recent_ch.get("pose") == pose:
        issues.append(
            f"pose '{pose}' was used in the previous {channel} thumbnail ({recent_ch.get('slug')}); rotate pose."
        )
    if backdrop and recent_ch.get("backdrop") == backdrop:
        issues.append(
            f"backdrop '{backdrop}' was used in the previous {channel} thumbnail ({recent_ch.get('slug')}); pick a topic-specific backdrop."
        )
    if backdrop == "cells-molecules":
        last_two = [e.get("backdrop") for e in entries[-2:]]
        if "cells-molecules" in last_two:
            issues.append(
                "backdrop 'cells-molecules' was used recently; use a concrete medical visual (ultrasound, embryo-microscope, clinic-warm, chart-data, bottles-props, light-editorial)."
            )
    if len(ch_entries) >= 2:
        if ch_entries[-1].get("side") == side and ch_entries[-2].get("side") == side:
            if outfit and ch_entries[-1].get("outfit") == outfit:
                issues.append(
                    f"last 2 {channel} thumbnails already used side='{side}' with outfit='{outfit}'; switch --side right or change outfit."
                )
    return issues


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", help="Path to AI/photo base image (16:9, no text)")
    ap.add_argument("--out", help="Output .jpg path")
    ap.add_argument("--line1", help="First headline line")
    ap.add_argument("--line2", help="Second headline line")
    ap.add_argument("--line3", default="", help="Optional third headline line")
    ap.add_argument("--pill", default="", help="Badge/pill text")
    ap.add_argument("--chip", default="", help="Optional comparison chip (e.g. '10 → ?')")
    ap.add_argument("--maxw", type=int, default=640, help="Text column width in px")
    ap.add_argument(
        "--template",
        choices=list(PALETTES.keys()),
        default=None,
        help="Typography/color template (classic-gold, yellow-focus, coral-contrast, amber-eyebrow, light-card)",
    )
    ap.add_argument(
        "--style",
        choices=["fr", "tr"],
        default="fr",
        help="Legacy alias: 'tr' defaults to yellow-focus if --template is not set",
    )
    ap.add_argument("--side", choices=["left", "right"], default="left", help="Which side the text block sits on")
    ap.add_argument("--channel", choices=["fr", "tr", "en"], default="fr")
    ap.add_argument("--video", default="", help="YouTube video ID (for variety log)")
    ap.add_argument("--slug", default="", help="Short topic slug (for variety log)")
    ap.add_argument("--outfit", choices=OUTFITS, default=None)
    ap.add_argument("--pose", choices=POSES, default=None)
    ap.add_argument("--backdrop", choices=BACKDROPS, default=None)
    ap.add_argument("--check-variety", action="store_true", help="Check variety rules against thumb-log.json and fail on repeats")
    ap.add_argument("--log-variety", action="store_true", help="Append this thumbnail's metadata to thumb-log.json")
    ap.add_argument("--status", action="store_true", help="Print recent thumb-log.json entries and recommended next options")
    a = ap.parse_args()

    entries = load_log()
    if a.status:
        print(f"thumb-log ({len(entries)} entries):")
        for e in entries[-6:]:
            print(
                f"  {e.get('date')} [{e.get('channel')}] {e.get('video') or '-':11s} {e.get('slug',''):24s} "
                f"template={e.get('template')} side={e.get('side')} outfit={e.get('outfit')} pose={e.get('pose')} backdrop={e.get('backdrop')}"
            )
        ch_entries = [e for e in entries if e.get("channel") == a.channel]
        last = ch_entries[-1] if ch_entries else (entries[-1] if entries else {})
        avail_t = [t for t in PALETTES if t != last.get("template")]
        avail_o = [o for o in OUTFITS if o != last.get("outfit")]
        avail_p = [p for p in POSES if p != last.get("pose")]
        avail_b = [b for b in BACKDROPS if b not in (last.get("backdrop"), "cells-molecules")]
        print(f"\nNext recommended for --channel {a.channel}:")
        print(f"  --template : {', '.join(avail_t)}")
        print(f"  --outfit   : {', '.join(avail_o)}")
        print(f"  --pose     : {', '.join(avail_p)}")
        print(f"  --backdrop : {', '.join(avail_b)}")
        return

    template = a.template or ("yellow-focus" if a.style == "tr" else "classic-gold")

    if a.check_variety:
        issues = check_variety(entries, a.channel, template, a.side, a.outfit, a.pose, a.backdrop)
        if issues:
            sys.stderr.write("VARIETY CHECK FAILED:\n")
            for iss in issues:
                sys.stderr.write(f"  - {iss}\n")
            sys.exit(2)
        print("variety check: OK")

    if not a.base or not a.out or not a.line1 or not a.line2:
        if a.check_variety:
            return
        ap.error("--base, --out, --line1, and --line2 are required when composing an image.")

    pal = PALETTES[template]
    nb = lambda s: s.replace(" ?", "\u00a0?").replace(" !", "\u00a0!").replace(" :", "\u00a0:")

    img = Image.open(a.base).convert("RGB")
    img = img.resize((W, int(img.height * W / img.width)))
    top = (img.height - H) // 2
    img = img.crop((0, top, W, top + H))

    # Directional contrast shade on the text side
    shade = Image.new("L", (W, H), 0)
    ds = ImageDraw.Draw(shade)
    alpha_max = pal["shade_alpha"]
    for x in range(W):
        rel = (x / (W * 0.64)) if a.side == "left" else ((W - 1 - x) / (W * 0.64))
        val = int(alpha_max * max(0.0, 1.0 - rel) ** 1.35)
        ds.line([(x, 0), (x, H)], fill=val)
    img = Image.composite(Image.new("RGB", (W, H), pal["shade"]), img, shade)
    d = ImageDraw.Draw(img)

    wdth = pal["wdth"]

    def fit(text: str, maxw: int, start: int, wght: int = 750) -> tuple[ImageFont.FreeTypeFont, tuple[int, int, int, int]]:
        for s in range(start, 30, -2):
            f = cond(s, wght, wdth)
            b = d.textbbox((0, 0), text, font=f)
            if b[2] - b[0] <= maxw:
                return f, b
        return f, b

    def draw_line(xy: tuple[int, int], text: str, font: ImageFont.FreeTypeFont, fill: tuple[int, int, int]) -> None:
        if template != "light-card":
            sh = Image.new("L", (W, H), 0)
            ImageDraw.Draw(sh).text(xy, text, font=font, fill=210)
            sh = sh.filter(ImageFilter.GaussianBlur(6))
            img.paste((0, 0, 0), (0, 0), sh.point(lambda v: int(v * 0.58)))
        stroke_w = pal["stroke_w"]
        if stroke_w and pal["stroke"]:
            ImageDraw.Draw(img).text(xy, text, font=font, fill=fill, stroke_width=stroke_w, stroke_fill=pal["stroke"])
        else:
            ImageDraw.Draw(img).text(xy, text, font=font, fill=fill)

    X = 64 if a.side == "left" else (W - a.maxw - 64)
    y = 64 if not a.line3 else 52

    # Optional eyebrow pill at top
    if a.pill and pal["pill_pos"] == "eyebrow":
        fp, bp = fit(a.pill, a.maxw - 80, 44, 650)
        pw, ph = (bp[2] - bp[0]) + 36, (bp[3] - bp[1]) + 22
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((X, y, X + pw, y + ph), radius=8, fill=pal["pill_bg"])
        d.text((X + 18 - bp[0], y + 11 - bp[1]), a.pill, font=fp, fill=pal["pill_fg"])
        y += ph + 24

    l1_start = 210 if not a.line3 else 165
    f1, b1 = fit(nb(a.line1), a.maxw, l1_start, 800)
    draw_line((X - b1[0], y - b1[1]), nb(a.line1), f1, pal["line1"])
    y += (b1[3] - b1[1]) + 22

    l2_start = 130 if not a.line3 else 135
    f2, b2 = fit(nb(a.line2), a.maxw, l2_start, 750)
    draw_line((X - b2[0], y - b2[1]), nb(a.line2), f2, pal["line2"])
    y += (b2[3] - b2[1]) + 24

    if a.line3:
        f3_line, b3_line = fit(nb(a.line3), a.maxw, 120, 750)
        draw_line((X - b3_line[0], y - b3_line[1]), nb(a.line3), f3_line, pal["line3"])
        y += (b3_line[3] - b3_line[1]) + 28

    # Optional numeric/comparison chip (e.g. "10 → ?")
    if a.chip:
        fc, bc = fit(a.chip, 280, 58, 750)
        cw, ch = (bc[2] - bc[0]) + 40, (bc[3] - bc[1]) + 24
        d = ImageDraw.Draw(img)
        chip_bg = (36, 56, 76) if template != "light-card" else (156, 42, 58)
        d.rounded_rectangle((X, y, X + cw, y + ch), radius=ch // 2, fill=chip_bg, outline=pal["line1"], width=2)
        d.text((X + 20 - bc[0], y + 12 - bc[1]), a.chip, font=fc, fill=(250, 248, 242))
        y += ch + 22

    # Bottom or corner pill
    if a.pill and pal["pill_pos"] != "eyebrow":
        fp, bp = fit(a.pill, a.maxw - 80, 50, 650)
        pw, ph = (bp[2] - bp[0]) + 44, (bp[3] - bp[1]) + 28
        d = ImageDraw.Draw(img)
        px, py = X, y + 8
        radius = 10
        if pal["pill_pos"] == "corner-bottom":
            px = 36 if a.side == "left" else (W - pw - 36)
            py = H - ph - 34
            radius = ph // 2
        d.rounded_rectangle((px, py, px + pw, py + ph), radius=radius, fill=pal["pill_bg"])
        d.text((px + 22 - bp[0], py + 14 - bp[1]), a.pill, font=fp, fill=pal["pill_fg"])

    out = Path(a.out)
    img.save(out, quality=92)
    img.resize((120, 68), Image.LANCZOS).resize((480, 272), Image.NEAREST).save(out.with_name(out.stem + "-mobile.png"))
    kb = out.stat().st_size // 1024
    print(f"wrote {out} ({template}, side={a.side}) {kb} KB" + ("  WARNING: over 2 MB" if kb > 2048 else ""))

    if a.log_variety:
        entries.append(
            {
                "date": str(date.today()),
                "channel": a.channel,
                "video": a.video,
                "slug": a.slug or out.stem,
                "template": template,
                "side": a.side,
                "outfit": a.outfit or "unknown",
                "pose": a.pose or "unknown",
                "backdrop": a.backdrop or "unknown",
            }
        )
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        LOG_PATH.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"logged variety -> {LOG_PATH}")


if __name__ == "__main__":
    main()
