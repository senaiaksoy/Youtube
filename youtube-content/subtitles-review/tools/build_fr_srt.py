"""Build review-ready French SRT: ASR word timings (what was said) + spelling aligned to the verified script."""
import difflib, json, re, sys, unicodedata
from pathlib import Path

SP = Path(r"C:\Users\KC3\AppData\Local\Temp\claude\D--A-klas-r-Youtube\698f879a-3ef4-4b5e-b7f2-8e5a23e113ee\scratchpad")
SCRIPT = Path(r"D:\A-klasör\Youtube\youtube-content\video-script-premiere-echographie-fiv-fr-2026-10-07.txt")
ASR = Path(sys.argv[2]) if len(sys.argv) > 2 else SP / "sub" / "fr_medium.words.json"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else SP / "sub" / "fr.srt"
MAXCH, MAXLINES, MAXDUR = 40, 2, 6.0


def key(t):
    t = unicodedata.normalize("NFKD", t.lower())
    return "".join(c for c in t if c.isalnum() and not unicodedata.combining(c))


# ---- ASR words (merge continuation pieces that have no leading space)
raw = json.loads(ASR.read_text(encoding="utf-8-sig"))
aw = []
for w, a, b, p in raw:
    if aw and not w.startswith(" ") and not re.match(r"^[A-Za-zÀ-ÿ0-9«]", w) or (aw and not w.startswith(" ") and w.startswith("'")):
        aw[-1][0] += w; aw[-1][2] = b; aw[-1][3] = min(aw[-1][3], p)
    else:
        aw.append([w.strip(), a, b, p])
aw = [x for x in aw if x[0]]
_m = []
for x in aw:  # lone punctuation from ASR (e.g. "?") belongs to the previous word
    if _m and not any(c.isalnum() for c in x[0]):
        _m[-1][0] += " " + x[0]; _m[-1][2] = x[2]
    else:
        _m.append(x)
aw = _m

# ---- script words
stext = SCRIPT.read_text(encoding="utf-8")
_tok = [m.group().replace("'", "’") for m in re.finditer(r"\S+", stext)]
sw, _pre = [], ""
for t in _tok:
    if not any(c.isalnum() for c in t):
        if t in ("«", "“"):
            _pre = t + " "
        elif sw:
            sw[-1] += " " + t
        continue
    sw.append(_pre + t); _pre = ""
skeys = [key(w) for w in sw]
akeys = [key(w[0]) for w in aw]
sm = difflib.SequenceMatcher(a=skeys, b=akeys, autojunk=False)

final, log = [], []  # final: [text, start, end, src]
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    A = aw[j1:j2]
    if tag == "equal":
        for k in range(j2 - j1):
            final.append([sw[i1 + k], aw[j1 + k][1], aw[j1 + k][2], "script"])
    elif tag == "replace":
        sa, sb = "".join(skeys[i1:i2]), "".join(akeys[j1:j2])
        r = difflib.SequenceMatcher(a=sa, b=sb).ratio() if sa and sb else 0
        NUMS = {"un": "1", "deux": "2", "trois": "3", "quatre": "4", "cinq": "5", "six": "6", "sept": "7", "huit": "8", "neuf": "9", "dix": "10",
                "douze": "12", "seize": "16", "deuxmille": "2000", "deuxmillecinqcents": "2500"}
        numeq = NUMS.get("".join(skeys[i1:i2]).replace("sa", "")) == re.sub(r"\D", "", sb)
        forced = bool(set(skeys[i1:i2]) & {"fiv", "sa", "sg", "hcg"}) or numeq
        if (i2 - i1) <= 4 and (j2 - j1) <= 4 and (r >= 0.4 or forced):
            ns, t0, t1 = i2 - i1, A[0][1], A[-1][2]
            for k in range(ns):
                final.append([sw[i1 + k], t0 + (t1 - t0) * k / ns, t0 + (t1 - t0) * (k + 1) / ns, "script~"])
            log.append((A[0][1], "FIXED", " ".join(sw[i1:i2]), " ".join(x[0] for x in A), round(r, 2)))
        else:
            for x in A:
                final.append([x[0], x[1], x[2], "asr"])
            log.append((A[0][1], "KEPT-ASR", " ".join(sw[i1:i2]), " ".join(x[0] for x in A), round(r, 2)))
    elif tag == "insert":
        for x in A:
            final.append([x[0], x[1], x[2], "asr"])
        log.append((A[0][1], "SAID-EXTRA", "", " ".join(x[0] for x in A), 0))
    elif tag == "delete":
        if i2 - i1 == 1 and skeys[i1] in {"la", "le", "les", "de", "du", "en", "et", "a", "un", "une", "des"} and final:
            final.append([sw[i1], final[-1][2], final[-1][2] + 0.08, "script+"])
        log.append((aw[j1][1] if j1 < len(aw) else 999, "NOT-SAID", " ".join(sw[i1:i2]), "", 0))

OUTRO = 925.0
final = [f for f in final if f[1] < OUTRO] + [[x[0], x[1], x[2], "asr"] for x in aw if x[1] >= OUTRO]
# ---- ASR-only cleanups
for f in final:
    if f[3] == "asr":
        f[0] = f[0].replace("'", "’")
        f[0] = re.sub(r"\bS\s?\.?\s?A\.?\b", "SA", f[0])
for f in final:
    if f[3] == "asr":
        f[0] = re.sub(r"(?<=[^\s ])([?!:;])$", lambda m: " " + m.group(1), f[0])
LOWER = {"ce", "cette", "ces", "le", "la", "les", "un", "une", "et", "mais", "si", "je", "on", "vous", "c’est", "ça"}
for k in range(1, len(final)):
    if final[k - 1][0].endswith((",", ";")) and final[k][0][:1].isupper() and key(final[k][0]) in {key(x) for x in LOWER}:
        final[k][0] = final[k][0][0].lower() + final[k][0][1:]

# ---- cue segmentation
END = re.compile(r"[.!?…»]$")
SOFT = re.compile(r"[,;:—–)]$")
CONJ = {"et", "mais", "que", "qui", "où", "donc", "car", "ou", "quand", "parce", "puis", "avec", "pour", "dans"}


def length(ws):
    return len(" ".join(w[0] for w in ws))


cues, cur = [], []
for idx, w in enumerate(final):
    if cur and (w[1] - cur[-1][2] > 0.7 or END.search(cur[-1][0].rstrip("»\"”")) and length(cur) >= 18):
        cues.append(cur); cur = []
    cur.append(w)
    if length(cur) > MAXCH * MAXLINES or cur[-1][2] - cur[0][1] > MAXDUR:
        # split at best point in the last 60% of the cue
        lo = max(1, int(len(cur) * 0.4))
        best, score = None, -1
        for s in range(lo, len(cur)):
            sc = (3 if END.search(cur[s - 1][0]) else 2 if SOFT.search(cur[s - 1][0]) else 1 if key(cur[s][0]) in CONJ else 0)
            sc = sc * 10 + s * 0.01
            if sc > score and length(cur[:s]) <= MAXCH * MAXLINES:
                best, score = s, sc
        best = best or len(cur) - 1
        cues.append(cur[:best]); cur = cur[best:]
if cur:
    cues.append(cur)


def wrap(ws):
    t = " ".join(w[0] for w in ws)
    if len(t) <= MAXCH:
        return t
    mid, best, bs = len(t) / 2, None, 1e9
    pos = 0
    for k, w in enumerate(ws[:-1]):
        pos += len(w[0]) + 1
        pen = abs(pos - mid) - (6 if SOFT.search(w[0]) or END.search(w[0]) else 0)
        if pen < bs:
            best, bs = k, pen
    return " ".join(w[0] for w in ws[:best + 1]) + "\n" + " ".join(w[0] for w in ws[best + 1:])


def ts(t):
    t = max(t, 0)
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


rows = []
for k, c in enumerate(cues):
    s, e = c[0][1], c[-1][2]
    nxt = cues[k + 1][0][1] if k + 1 < len(cues) else 1e9
    e = min(max(e + 0.2, s + 1.0), nxt - 0.04)
    if e <= s:
        e = s + 0.5
    rows.append((s, e, wrap(c)))
srt = "\n\n".join(f"{i + 1}\n{ts(s)} --> {ts(e)}\n{t}" for i, (s, e, t) in enumerate(rows)) + "\n"
OUT.write_text(srt, encoding="utf-8")
(SP / "sub" / "fr_srt_log.txt").write_text("\n".join(f"{a:7.1f} {b:10s} r={r:<4} SCRIPT:{s!r} SAID:{h!r}" for a, b, s, h, r in sorted(log)), encoding="utf-8")
fast = [(i + 1, round(len(t.replace("\n", "")) / (e - s), 1)) for i, (s, e, t) in enumerate(rows) if len(t.replace("\n", "")) / (e - s) > 21]
from collections import Counter
print("cues", len(rows), "| src", dict(Counter(f[3] for f in final)), "| log", dict(Counter(l[1] for l in log)))
print("longest cue", round(max(e - s for s, e, _ in rows), 1), "s | cues >21 cps:", len(fast), fast[:12])
