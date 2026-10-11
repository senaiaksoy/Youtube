"""Automatic sanity checks on translation JSONs: completeness, numbers, length ratio, French leakage.
usage: py -3.12 trans_check.py it ro fa ...
"""
import json, re, sys
from pathlib import Path

W = Path(r"D:\A-klasör\Youtube\youtube-content\subtitles-review\work")
en = json.loads((W / "tr_en.json").read_text(encoding="utf-8"))
units = json.loads((W / "units.json").read_text(encoding="utf-8"))
ids = [str(u["id"]) for u in units]
FRENCH = re.compile(r"\b(échographie|grossesse|semaines|médecin|embryon|c’est|n’est|vous|votre|aujourd|avec|dans les)\b", re.I)
NUMS = re.compile(r"\d+")
ok_all = True
for lang in sys.argv[1:]:
    p = W / f"tr_{lang}.json"
    if not p.exists():
        print(lang, "MISSING FILE"); ok_all = False; continue
    try:
        t = json.loads(p.read_text(encoding="utf-8-sig"))
    except Exception as e:
        print(lang, "INVALID JSON:", e); ok_all = False; continue
    miss = [i for i in ids if not str(t.get(i, "")).strip()]
    extra = [k for k in t if k not in ids]
    nummiss, longs, fr = [], [], []
    for i in ids:
        s = t.get(i, "")
        if not s:
            continue
        for n in set(NUMS.findall(en[i])):
            if n not in s:
                nummiss.append((i, n))
        r = len(s) / max(1, len(en[i]))
        if r > 1.45:
            longs.append((i, round(r, 2)))
        if lang not in ("fr",) and FRENCH.search(s):
            fr.append(i)
    print(f"{lang}: ids {len(t)}/{len(ids)} missing={miss[:8]} extra={extra[:5]} | digit-mismatch={nummiss[:8]} | >1.45x EN={longs[:8]} | French-leak={fr[:8]}")
    if miss or extra:
        ok_all = False
print("ALL OK" if ok_all else "PROBLEMS FOUND")
