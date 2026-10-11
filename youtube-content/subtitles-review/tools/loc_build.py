"""Validate localized title/description JSONs and build the yt_metadata fixes file.
usage: py -3.12 loc_build.py   (reads work/loc_<lang>.json, writes youtube-api/loc-fixes-MoApIs3-WwE.json)
"""
import json, re, sys
from pathlib import Path

W = Path(r"D:\A-klasör\Youtube\youtube-content\subtitles-review\work")
OUT = Path(r"D:\A-klasör\Youtube\youtube-api\loc-fixes-MoApIs3-WwE.json")
LANGS = "ar az bg bs de es fa it mk ro ru sq sr tr uk".split()
src = json.loads((W / "loc_source_fr.json").read_text(encoding="utf-8-sig"))
TS = re.compile(r"^(\d\d:\d\d)\s", re.M)
src_ts = TS.findall(src["description"])
problems, loc = [], {}
for lang in LANGS:
    p = W / f"loc_{lang}.json"
    if not p.exists():
        problems.append((lang, "missing file")); continue
    try:
        d = json.loads(p.read_text(encoding="utf-8-sig"))
    except Exception as e:
        problems.append((lang, f"invalid json {e}")); continue
    t, desc = d.get("title", "").strip(), d.get("description", "").strip()
    errs = []
    if not t or len(t) > 100:
        errs.append(f"title len {len(t)}")
    if len(desc.encode("utf-8")) >= 5000:
        errs.append(f"desc bytes {len(desc.encode('utf-8'))}")
    if TS.findall(desc) != src_ts:
        errs.append(f"chapters mismatch {len(TS.findall(desc))}/{len(src_ts)}")
    for must in ("+90 507 380 28 05", "www.draksoyivf.com", "NICE NG126", "Mortimer"):
        if must not in desc:
            errs.append(f"missing '{must}'")
    if "AVERTISSEMENT" in desc or "Première échographie" in t:
        errs.append("French leftover")
    if not re.search(r"#\S+ #\S+ #\S+\s*$", desc):
        errs.append("hashtags not last")
    if desc.count("#") < 3:
        errs.append("hashtags")
    if errs:
        problems.append((lang, "; ".join(errs)))
    loc[lang] = {"title": t, "description": desc}
for lang in LANGS:
    if lang in loc:
        print(f"{lang}: {len(loc[lang]['title']):>3} ch | {len(loc[lang]['description'].encode('utf-8')):>4} B | {loc[lang]['title']}")
print("PROBLEMS:", problems or "none")
if not problems:
    fix = [{"video_id": "MoApIs3-WwE", "localizations": loc}]
    OUT.write_text(json.dumps(fix, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", OUT)
