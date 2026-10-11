"""Side-by-side review file: FR + EN/TR/AR per sentence unit."""
import json
from pathlib import Path

R = Path(r"D:\A-klasör\Youtube\youtube-content\subtitles-review")
W = R / "work"
u = json.loads((W / "units.json").read_text(encoding="utf-8"))
cues = {c["n"]: c for c in json.loads((W / "cues.json").read_text(encoding="utf-8"))}
LANGS = ("es", "ru", "de")  # new batch only; EN/TR/AR were reviewed and uploaded earlier
L = {k: json.loads((W / f"tr_{k}.json").read_text(encoding="utf-8")) for k in LANGS}


def mmss(t):
    return f"{int(t // 60):02d}:{int(t % 60):02d}"


out = ["# Première échographie — altyazı çevirileri (FR → ES / RU / DE)", "",
       "Her blok: birim no, başlangıç zamanı, Fransızca asıl metin ve üç çeviri. Düzeltmek istediğin birimin numarasını yaz (ör. “036 TR”).", ""]
for x in u:
    k = str(x["id"])
    out += [f"### {x['id']:03d} · {mmss(cues[x['cues'][0]]['s'])}", f"- **FR:** {x['fr']}"] + [f"- **{g.upper()}:** {L[g][k]}" for g in LANGS] + [""]
(R / "ceviriler-es-ru-de.md").write_text("\n".join(out), encoding="utf-8")
print(len(u), "units written")
