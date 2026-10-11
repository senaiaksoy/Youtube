"""Group the reviewed FR SRT into sentence units for translation. -> units.json + units.txt (UTF-8)"""
import json, re, sys
from pathlib import Path

SRT = Path(r"D:\A-klasör\Youtube\youtube-content\subtitles-review\premiere-echographie-fr.srt")
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else SRT.parent / "work"
OUT.mkdir(parents=True, exist_ok=True)


def sec(s):
    h, m, r = s.split(":"); a, b = r.split(",")
    return int(h) * 3600 + int(m) * 60 + int(a) + int(b) / 1000


cues = []
for blk in SRT.read_text(encoding="utf-8").strip().split("\n\n"):
    l = blk.split("\n")
    s, e = [sec(x) for x in l[1].split(" --> ")]
    cues.append(dict(n=int(l[0]), s=s, e=e, text=" ".join(l[2:]).replace("\u00a0", " ")))

END = re.compile(r"[.!?…»]\s*$")
units, cur = [], []
for c in cues:
    cur.append(c)
    if END.search(c["text"]):
        units.append(cur); cur = []
if cur:
    units.append(cur)

data = [dict(id=i + 1, cues=[c["n"] for c in u], fr=" ".join(c["text"] for c in u)) for i, u in enumerate(units)]
(OUT / "units.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
(OUT / "cues.json").write_text(json.dumps(cues, ensure_ascii=False), encoding="utf-8")
with open(OUT / "units.txt", "w", encoding="utf-8") as f:
    for d in data:
        f.write(f"{d['id']:03d} [{d['cues'][0]}-{d['cues'][-1]}] {d['fr']}\n")
print(len(cues), "cues ->", len(data), "units; longest unit", max(len(d["cues"]) for d in data), "cues")
