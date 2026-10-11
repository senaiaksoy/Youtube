"""Diff Whisper words (what was said) against the FR script (intended text); write diff list to a UTF-8 file."""
import difflib, json, re, unicodedata
from pathlib import Path

SP = Path(r"C:\Users\KC3\AppData\Local\Temp\claude\D--A-klas-r-Youtube\698f879a-3ef4-4b5e-b7f2-8e5a23e113ee\scratchpad")
script = Path(r"D:\A-klasör\Youtube\youtube-content\video-script-premiere-echographie-fiv-fr-2026-10-07.txt").read_text(encoding="utf-8")
words = json.loads((SP / "tx" / "seq_mix_limited2.words.json").read_text(encoding="utf-8-sig"))


def norm(t):
    t = unicodedata.normalize("NFKD", t.lower().replace("’", "'"))
    return re.findall(r"[a-z0-9]+", "".join(c for c in t if not unicodedata.combining(c)))


st, sraw = [], []
for m in re.finditer(r"\S+", script):
    for t in norm(m.group()):
        st.append(t); sraw.append(m.group())
ht, hraw, htime = [], [], []
for w, a, b in words:
    for t in norm(w):
        ht.append(t); hraw.append(w); htime.append(a)
sm = difflib.SequenceMatcher(a=st, b=ht, autojunk=False)
print("ratio", round(sm.ratio(), 3), "script tokens", len(st), "speech tokens", len(ht))
out = []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        continue
    out.append(f"{htime[j1] if j1 < len(htime) else 999:7.1f} {tag:7s} SCRIPT: {' '.join(sraw[i1:i2])!r:60.60s} SAID: {' '.join(hraw[j1:j2])!r}")
(SP / "fr_sub_diff.txt").write_text("\n".join(out), encoding="utf-8")
print(len(out), "diffs")
