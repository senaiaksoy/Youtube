"""Vertical FR Shorts from the final 4K talking-head video: face crop 9:16, burned-in captions (approved FR cues), hook title.
usage: py -3.12 make_shorts.py [clip_id ...]   (default: all)
"""
import json, re, shutil, subprocess, sys
from pathlib import Path

R = Path(r"D:\A-klasör\Youtube\youtube-content\subtitles-review")
W = R / "work"
OUT = Path(r"D:\A-klasör\openmontage\projects\premiere-echographie-fr-motion-2026-10-09\shorts")
TMP = W / "shorts_tmp"
SRC = r"C:\Users\KC3\Downloads\ilk ultrason fr - final 4K.mp4"
OUT.mkdir(exist_ok=True); TMP.mkdir(exist_ok=True)
(TMP / "fonts").mkdir(exist_ok=True)
for f in ("ariblk.ttf", "arialbd.ttf"):
    shutil.copy(Path(r"C:\Windows\Fonts") / f, TMP / "fonts" / f)

cues = json.loads((W / "cues.json").read_text(encoding="utf-8"))
units = {u["id"]: u for u in json.loads((W / "units.json").read_text(encoding="utf-8"))}
CUE = {c["n"]: c for c in cues}

# id, unit range, on-screen hook, face-centre x in the 4K frame
CLIPS = [
    ("s1-signes-alerte", 113, 118, "4 SIGNES À NE\\NJAMAIS IGNORER", 1930),
    ("s2-silence-medecin", 9, 12, "LE SILENCE\\NDU MÉDECIN…", 1930),
    ("s3-coeur-pas-visible", 16, 20, "PAS DE CŒUR\\NVISIBLE ?", 1930),
    ("s4-combien-continuent", 93, 98, "COMBIEN DE GROSSESSES\\NCONTINUENT ?", 1930),
    ("s5-pourquoi-5-sa", 27, 35, "POURQUOI\\N« 5 SA » ?", 1930),
    ("s6-trois-reperes", 54, 63, "LES 3 REPÈRES\\NDE L'ÉCHO", 1930),
    ("s7-echo-5-sa", 124, 129, "ÉCHO À 5 SA :\\NUTILE ?", 1930),
]
CAPFONT, CAPSIZE, MAXCH = "Arial Black", 82, 17


def ass_time(t):
    cs = int(round(t * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


def chunks(text, s, e):
    words = text.split()
    out, cur = [], []
    for w in words:
        if cur and len(" ".join(cur + [w])) > MAXCH:
            out.append(cur); cur = []
        cur.append(w)
    if cur:
        out.append(cur)
    # avoid orphan one-word chunk of punctuation/short word
    if len(out) > 1 and len(" ".join(out[-1])) < 5:
        out[-2] += out.pop()
    tot = sum(len(" ".join(c)) for c in out)
    res, t = [], s
    for c in out:
        d = (e - s) * len(" ".join(c)) / tot
        res.append((t, t + d, " ".join(c)))
        t += d
    return res


def build(cid, ua, ub, hook, fx):
    t0 = CUE[units[ua]["cues"][0]]["s"] - 0.10
    t1 = CUE[units[ub]["cues"][-1]]["e"] + 0.05
    dur = t1 - t0
    ev = []
    for n in range(units[ua]["cues"][0], units[ub]["cues"][-1] + 1):
        c = CUE[n]
        txt = c["text"].replace("\u00a0", " ").upper()
        for a, b, tx in chunks(txt, max(c["s"] - t0, 0), min(c["e"] - t0, dur)):
            ev.append(f"Dialogue: 0,{ass_time(a)},{ass_time(b)},Cap,,0,0,0,,{tx}")
    ev.append(f"Dialogue: 1,{ass_time(0.15)},{ass_time(3.4)},Hook,,0,0,0,,{hook}")
    ev.append(f"Dialogue: 1,{ass_time(dur - 2.4)},{ass_time(dur - 0.1)},Hook,,0,0,0,,VIDÉO COMPLÈTE\\NEN DESCRIPTION")
    ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,{CAPFONT},{CAPSIZE},&H00F7F3E8,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,8,3,2,50,50,430,1
Style: Hook,{CAPFONT},70,&H00271808,&H000000FF,&H0072BEF2,&H00000000,-1,0,0,0,100,100,0,0,3,22,0,8,40,40,1110,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(ev) + "\n"
    (TMP / f"{cid}.ass").write_text(ass, encoding="utf-8")
    x0 = fx - 607
    vf = (f"crop=1215:2160:{x0}:0,scale=1080:1920:flags=lanczos,eq=contrast=1.04:saturation=1.08,"
          f"subtitles={cid}.ass:fontsdir=fonts,fade=t=in:d=0.12,fade=t=out:st={dur - 0.2:.2f}:d=0.2")
    out = OUT / f"{cid}.mp4"
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{t0:.3f}", "-t", f"{dur:.3f}", "-i", SRC,
           "-vf", vf, "-af", f"afade=t=in:d=0.05,afade=t=out:st={dur - 0.2:.2f}:d=0.2", "-r", "30",
           "-c:v", "libx264", "-crf", "19", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
           "-movflags", "+faststart", str(out)]
    r = subprocess.run(cmd, cwd=TMP, capture_output=True, text=True, encoding="utf-8")
    if r.returncode:
        print(cid, "FAILED", r.stderr[-600:]); return None
    print(f"{cid}: {dur:.1f}s  {out.stat().st_size // 1024 // 1024} MB")
    return out


want = set(sys.argv[1:])
for c in CLIPS:
    if not want or c[0] in want:
        build(*c)
