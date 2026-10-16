"""Offline localisation workspace for one video: prepare translation sources, then QA + build SRTs and
the localizations fixes file for yt_metadata.py. Never calls the YouTube API.

  prep   --srt fr.srt --title "..." --desc description-fr.txt --dir i18n
         -> i18n/source.json (title_fr, description_fr, cues [{i, fr}]) + i18n/timings.json
  build  --dir i18n --video VIDEO_ID [--langs ar,az,...] [--stem name]
         reads i18n/<lang>.json ({lang, title, description, cues:[{i,text}]}) written by the translators,
         -> i18n/srt/<stem>.<lang>.srt (FR timings, 2×42 wrap), i18n/qa.json, i18n/fixes-localizations.json

QA (build): same cue count/order as FR, no empty cue, every number of the FR cue present (Persian/Arabic
digits normalised; small counts 1–4 and 8 may be words), no drug brand names, title ≤ 100, description
≤ 5000 with every FR chapter timestamp. Exit code 1 if any language has issues.
"""
import argparse
import json
import re
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

DEFAULT_LANGS = "ar,az,bg,bs,de,es,fa,it,mk,ro,ru,sq,sr,tr,uk"
BRANDS = re.compile(r"ozempic|wegovy|mounjaro|saxenda|zepbound|victoza|rybelsus|trulicity", re.I)
DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")


def parse_srt(path: str) -> list[dict]:
    blocks = re.split(r"\n\s*\n", Path(path).read_text(encoding="utf-8-sig").strip())
    out = []
    for b in blocks:
        lines = b.splitlines()
        out.append({"i": int(lines[0]), "t": lines[1], "fr": " ".join(lines[2:]).replace("\u00a0", " ")})
    return out


def wrap(t: str, n: int = 42) -> str:
    t = " ".join(t.split())
    if len(t) <= n:
        return t
    w = t.split(" ")
    i = min(range(1, len(w)), key=lambda i: (max(len(" ".join(w[:i])), len(" ".join(w[i:]))),
                                            abs(len(" ".join(w[:i])) - len(" ".join(w[i:])))))
    return " ".join(w[:i]) + "\n" + " ".join(w[i:])


def cmd_prep(a) -> None:
    d = Path(a.dir)
    d.mkdir(parents=True, exist_ok=True)
    cues = parse_srt(a.srt)
    desc = Path(a.desc).read_text(encoding="utf-8").strip()
    json.dump({"title_fr": a.title, "description_fr": desc, "cues": [{"i": c["i"], "fr": c["fr"]} for c in cues]},
              open(d / "source.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(cues, open(d / "timings.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(f"wrote {d / 'source.json'} ({len(cues)} cues) and timings.json")


def cmd_build(a) -> None:
    d = Path(a.dir)
    src = json.load(open(d / "source.json", encoding="utf-8"))
    tim = json.load(open(d / "timings.json", encoding="utf-8"))
    fr_by_i = {c["i"]: c["fr"] for c in src["cues"]}
    stamps = re.findall(r"^(\d\d:\d\d) ", src["description_fr"], re.M)
    (d / "srt").mkdir(exist_ok=True)
    qa, locs, bad = {}, {}, False
    for L in [x.strip() for x in a.langs.split(",") if x.strip()]:
        f = d / f"{L}.json"
        if not f.exists():
            qa[L] = {"missing": True}
            bad = True
            continue
        j = json.load(open(f, encoding="utf-8"))
        cues, issues = j["cues"], []
        if [c["i"] for c in cues] != [c["i"] for c in tim]:
            issues.append("cue index/order mismatch")
        for c in cues:
            t = c["text"].strip()
            tn = t.translate(DIGITS)
            if not t:
                issues.append(f"empty cue {c['i']}")
            if BRANDS.search(t):
                issues.append(f"brand in cue {c['i']}")
            if len(t) > 96:
                issues.append(f"long cue {c['i']} ({len(t)})")
            for num in re.findall(r"\d+", fr_by_i.get(c["i"], "").replace("\u202f", "")):
                if num not in re.sub(r"[^0-9]", " ", tn).split() and num not in ("1", "2", "3", "4", "8"):
                    issues.append(f"number {num} missing in cue {c['i']}")
        title, desc = j["title"].strip(), j["description"].strip()
        if len(title) > 100:
            issues.append(f"title too long ({len(title)})")
        if len(desc) > 5000:
            issues.append(f"description too long ({len(desc)})")
        miss = [s for s in stamps if s not in desc]
        if miss:
            issues.append(f"missing timestamps {miss}")
        if BRANDS.search(title + desc):
            issues.append("brand in title/description")
        srt = "\n".join(f"{t['i']}\n{t['t']}\n{wrap(c['text'])}\n" for c, t in zip(cues, tim))
        (d / "srt" / f"{a.stem}.{L}.srt").write_text(srt, encoding="utf-8")
        longest = max(len(line) for c in cues for line in wrap(c["text"]).split("\n"))
        qa[L] = {"cues": len(cues), "title": title, "title_len": len(title), "desc_len": len(desc),
                 "longest_line": longest, "issues": issues}
        locs[L] = {"title": title, "description": desc}
        bad |= bool(issues)
        print(f"{L}: {len(cues)} cues | title {len(title)} | desc {len(desc)} | longest line {longest} | issues {len(issues)}")
    json.dump(qa, open(d / "qa.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({"video_id": a.video, "localizations": locs}, open(d / "fixes-localizations.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"wrote {d / 'qa.json'} and {d / 'fixes-localizations.json'}")
    sys.exit(1 if bad else 0)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prep")
    p.add_argument("--srt", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--desc", required=True)
    p.add_argument("--dir", required=True)
    p = sub.add_parser("build")
    p.add_argument("--dir", required=True)
    p.add_argument("--video", required=True)
    p.add_argument("--langs", default=DEFAULT_LANGS)
    p.add_argument("--stem", default="subtitles")
    a = ap.parse_args()
    cmd_prep(a) if a.cmd == "prep" else cmd_build(a)


if __name__ == "__main__":
    main()
