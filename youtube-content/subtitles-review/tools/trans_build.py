"""Re-time sentence-level translations onto the approved FR cue timings -> <lang>.srt (+ report).
usage: py -3.12 trans_build.py <lang en|tr|ar>
"""
import json, re, sys
from pathlib import Path

lang = sys.argv[1]
W = Path(r"D:\A-klasör\Youtube\youtube-content\subtitles-review\work")
units = json.loads((W / "units.json").read_text(encoding="utf-8"))
cues = {c["n"]: c for c in json.loads((W / "cues.json").read_text(encoding="utf-8"))}
tr = json.loads((W / f"tr_{lang}.json").read_text(encoding="utf-8-sig"))
MAXCH = {"en": 42, "tr": 42, "ar": 38, "fa": 38, "es": 42, "ru": 42, "de": 42}.get(lang, 42)
CPS = {"en": 20, "tr": 17, "ar": 17, "fa": 17, "es": 19, "ru": 17, "de": 18}.get(lang, 17)
GOOD = re.compile(r"[,.;:?!…»”—،؟]$")
assert set(tr) == {str(u["id"]) for u in units}, (set(str(u["id"]) for u in units) ^ set(tr))


def split_unit(u):
    words = tr[str(u["id"])].split()
    ns = u["cues"]
    if len(ns) == 1:
        return [words]
    dur = [cues[n]["e"] - cues[n]["s"] for n in ns]
    tot, cum, bounds = sum(dur), 0, []
    for d in dur[:-1]:
        cum += d
        bounds.append(round(len(words) * cum / tot))
    snapped = []
    for b in bounds:
        best, bs = b, 99
        for c in range(max(1, b - 2), min(len(words) - 1, b + 2) + 1):
            if GOOD.search(words[c - 1]) and not re.fullmatch(r"\d+\.", words[c - 1]):
                sc = abs(c - b)
                if sc < bs:
                    best, bs = c, sc
        snapped.append(best)
    out, prev = [], 0
    for b in snapped + [len(words)]:
        b = max(b, prev + 1)
        out.append(words[prev:b]); prev = b
    return out


def fix_overflow(chunks):
    for _ in range(40):
        moved = False
        for i, ch in enumerate(chunks):
            if len(" ".join(ch)) > 2 * MAXCH and len(ch) > 1:
                if i + 1 < len(chunks):
                    chunks[i + 1].insert(0, ch.pop()); moved = True
                elif i > 0:
                    chunks[i - 1].append(ch.pop(0)); moved = True
        if not moved:
            break
    return chunks


def wrap(ws):
    t = " ".join(ws)
    if len(t) <= MAXCH:
        return t
    mid, best, bs, pos = len(t) / 2, 0, 1e9, 0
    for k, w in enumerate(ws[:-1]):
        pos += len(w) + 1
        pen = abs(pos - mid) - (5 if GOOD.search(w) else 0)
        if pen < bs:
            best, bs = k, pen
    return " ".join(ws[:best + 1]) + "\n" + " ".join(ws[best + 1:])


def ts(t):
    ms = int(round(max(t, 0) * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def srt_time(n):
    return ts(cues[n]["s"]) + " --> " + ts(cues[n]["e"])


blocks, slow, long_lines = [], [], []
for u in units:
    chunks = fix_overflow(split_unit(u))
    for n, ch in zip(u["cues"], chunks):
        txt = wrap(ch)
        if lang in ("ar", "fa"):
            txt = "\n".join("\u200f" + ln for ln in txt.split("\n"))
        dur = cues[n]["e"] - cues[n]["s"]
        cps = len(txt.replace("\n", "")) / dur
        if cps > CPS:
            slow.append((n, round(cps, 1)))
        if any(len(ln.replace("\u200f", "")) > MAXCH + 4 for ln in txt.split("\n")):
            long_lines.append(n)
        blocks.append((n, txt))
blocks.sort()
out = "\n\n".join(f"{n}\n{srt_time(n)}\n{t}" for n, t in blocks) + "\n"
(W / f"premiere-echographie-{lang}.srt").write_text(out, encoding="utf-8")
print(lang, "cues", len(blocks), "| > %d cps:" % CPS, len(slow), slow[:15], "| long lines:", long_lines[:10])
