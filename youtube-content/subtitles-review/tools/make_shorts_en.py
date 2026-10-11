"""Vertical EN Shorts from the EN talking-head 4K (same 702 s timeline as the motion master): face crop 9:16,
burned-in captions from the approved EN SRT (queLygimeS8), hook title.
usage: py -3.12 make_shorts_en.py [clip_id ...]   (default: all)
"""
import json, re, shutil, subprocess, sys
from pathlib import Path

R = Path(r"D:\A-klasör\Youtube\youtube-content\subtitles-review")
W = R / "work"
OUT = Path(r"D:\A-klasör\openmontage\projects\premiere-echographie-en-motion-2026-10-09\shorts")
TMP = W / "shorts_en_tmp"
SRC = r"C:\Users\KC3\Downloads\ilk ultrason EN - paragraf hizali 4K.mp4"
SRT = R / "en-first-ultrasound" / "queLygimeS8.en.srt"
OUT.mkdir(exist_ok=True); TMP.mkdir(exist_ok=True)
(TMP / "fonts").mkdir(exist_ok=True)
for f in ("ariblk.ttf", "arialbd.ttf"):
    shutil.copy(Path(r"C:\Windows\Fonts") / f, TMP / "fonts" / f)


def srt_time(x):
    h, m, rest = x.split(":")
    sec, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000


CUE = {}
for blk in SRT.read_text(encoding="utf-8").strip().split("\n\n"):
    ln = blk.split("\n")
    a, b = ln[1].split(" --> ")
    CUE[int(ln[0])] = {"s": srt_time(a), "e": srt_time(b), "text": " ".join(ln[2:])}

# id, first cue, last cue, on-screen hook, face-centre x in the 4K frame
CLIPS = [
    ("en-s1-warning-signs", 153, 161, "4 SIGNS YOU\\NMUST NEVER IGNORE", 1930),
    ("en-s2-how-many-continue", 119, 130, "HEARTBEAT SEEN:\\NHOW MANY CONTINUE?", 1930),
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
    t0 = CUE[ua]["s"] - 0.10
    t1 = CUE[ub]["e"] + 0.05
    dur = t1 - t0
    ev = []
    for n in range(ua, ub + 1):
        c = CUE[n]
        txt = c["text"].replace("\u00a0", " ").upper()
        for a, b, tx in chunks(txt, max(c["s"] - t0, 0), min(c["e"] - t0, dur)):
            ev.append(f"Dialogue: 0,{ass_time(a)},{ass_time(b)},Cap,,0,0,0,,{tx}")
    ev.append(f"Dialogue: 1,{ass_time(0.15)},{ass_time(3.4)},Hook,,0,0,0,,{hook}")
    ev.append(f"Dialogue: 1,{ass_time(dur - 2.4)},{ass_time(dur - 0.1)},Hook,,0,0,0,,FULL VIDEO\\NIN DESCRIPTION")
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
