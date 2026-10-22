# -*- coding: utf-8 -*-
"""ASR (large-v3, kesim sonrasi ses) + onayli script -> FR SRT + inceleme raporu.
py -3.12 -I build_srt.py   (calisma klasorunde)
Kural: ASR zamanlari esas; metin, script ile eslesen yerde script yazimina duzeltilir; scriptte karsiligi olmayan
(dogaclama: 'Allez, ciao !') ASR metni korunur; ASR'de karsiligi olmayan script kelimeleri (kesilen/soylenmeyen) atilir.
"""
import difflib, io, json, re, sys, unicodedata

W = r"C:\Users\KC3\clomid-blur4k\v2_words.json"
SCRIPT = r"D:\A-klasör\Youtube\youtube-content\video-script-clomid-humour-fr-2026-10-21.txt"
OUT_SRT = r"D:\A-klasör\Youtube\youtube-api\clomid-fr-v2\subtitles_fr.srt"
OUT_REP = r"D:\A-klasör\Youtube\youtube-api\clomid-fr-v2\subtitles_review.md"

def norm(t):
    t = unicodedata.normalize("NFKC", t).lower()
    t = t.replace("œ", "oe").replace("’", "'")
    return re.sub(r"[^0-9a-zàâäçéèêëîïôöùûüÿ]+", "", t)

# --- ASR kelimeleri
d = json.load(open(W, encoding="utf-8"))
asr = []
for sg in d["segments"]:
    for w in sg["words"]:
        t = w["w"].strip()
        if t:
            asr.append({"t": t, "s": float(w["s"]), "e": float(w["e"])})
# noktalama-only ASR kelimelerini onceki kelimeye ekle
_m=[]
for a in asr:
    if not norm(a["t"]) and _m:
        _m[-1]["t"] += a["t"]; _m[-1]["e"] = max(_m[-1]["e"], a["e"])
    else:
        _m.append(a)
asr=_m
# sifir/negatif sureli kelimeleri komsu araliga yay
for i, a in enumerate(asr):
    if a["e"] <= a["s"]:
        nxt = asr[i + 1]["s"] if i + 1 < len(asr) else a["s"] + 0.3
        a["e"] = max(a["s"] + 0.12, min(nxt, a["s"] + 0.4))

# --- script kelimeleri
raw = open(SCRIPT, encoding="utf-8").read()
lines = []
for ln in raw.splitlines():
    ln = ln.strip()
    if not ln or ln.startswith("("):
        continue
    ln = re.sub(r"^\d+\.\s+", "", ln)
    lines.append(ln)
_raw = " ".join(lines).split()
stoks = []; _pend = ""
for tk in _raw:
    if norm(tk):
        stoks.append((_pend + tk)); _pend = ""
    elif tk in ("«", "“", "(", "[") or tk == "—" and not stoks:
        _pend = tk + " "
    elif stoks:
        stoks[-1] += " " + tk if tk not in ("?", "!", ":", ";", "»", "”", ")", ".", ",") else tk
    else:
        _pend = tk + " "
sn = [norm(t) for t in stoks]
an = [norm(a["t"]) for a in asr]

sm = difflib.SequenceMatcher(None, an, sn, autojunk=False)
out = []      # (text, s, e)
review = []   # (kind, asr_text, script_text, t)
for op, i1, i2, j1, j2 in sm.get_opcodes():
    A = asr[i1:i2]; S = stoks[j1:j2]
    if op == "equal":
        for a, s in zip(A, S):
            out.append((s, a["s"], a["e"]))
    elif op == "replace":
        t0, t1 = A[0]["s"], A[-1]["e"]
        simil = difflib.SequenceMatcher(None, " ".join(an[i1:i2]), " ".join(sn[j1:j2])).ratio()
        if len(A) == len(S):
            for a, s in zip(A, S):
                out.append((s, a["s"], a["e"]))
        else:
            n = len(S); step = (t1 - t0) / n
            for k, s in enumerate(S):
                out.append((s, t0 + k * step, t0 + (k + 1) * step))
        review.append(("remplacé" if simil >= 0.5 else "REMPLACÉ (faible similarité)", " ".join(a["t"] for a in A), " ".join(S), t0))
    elif op == "delete":   # ASR'de var, scriptte yok: dogaclama/ASR gurultusu -> korunur
        for a in A:
            out.append((a["t"], a["s"], a["e"]))
        review.append(("ajout oral (ASR conservé)", " ".join(a["t"] for a in A), "", A[0]["s"]))
    # insert: scriptte var, soylenmemis -> atilir
    if op == "insert":
        review.append(("script non prononcé (ignoré)", "", " ".join(S), out[-1][2] if out else 0))

# --- cue'lara bol
def ends_sentence(t): return bool(re.search(r"[.?!…]['»”\")]*$", t))
def ends_clause(t): return bool(re.search(r"[,;:—]$", t))
cues = []; cur = []
def flush():
    global cur
    if cur:
        cues.append(cur); cur = []
for k, (t, s, e) in enumerate(out):
    if cur:
        gap = s - cur[-1][2]
        text = " ".join(x[0] for x in cur)
        dur = e - cur[0][1]
        if gap > 0.7 or dur > 6.0 or len(text) + 1 + len(t) > 80:
            # mumkunse son virgulde bol
            idx = max((i for i, x in enumerate(cur) if ends_clause(x[0])), default=None)
            if idx is not None and idx < len(cur) - 1 and len(cur) - idx > 1 and gap <= 0.7:
                head, tail = cur[:idx + 1], cur[idx + 1:]
                cues.append(head); cur = tail
            else:
                flush()
    cur.append((t, s, e))
    text = " ".join(x[0] for x in cur)
    if ends_sentence(t) and (len(text) >= 18 or (cur[-1][2] - cur[0][1]) >= 1.2):
        flush()
flush()
# cok kisa cue'lari komsuyla birlestir (<0.9 s ve birlesince <=80 karakter)
merged = []
for c in cues:
    if merged and (c[-1][2] - c[0][1]) < 0.9 and (c[0][1] - merged[-1][-1][2]) < 0.5:
        txt = " ".join(x[0] for x in merged[-1] + c)
        if len(txt) <= 80:
            merged[-1] = merged[-1] + c; continue
    merged.append(c)
cues = merged

def wrap(text):
    if len(text) <= 42: return text
    mid = len(text) // 2
    best = None
    for m in re.finditer(r" ", text):
        p = m.start()
        sc = abs(p - mid)
        if best is None or sc < best[0]: best = (sc, p)
    p = best[1]
    return text[:p] + "\n" + text[p + 1:]

def ts(x):
    x = max(0.0, x); h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
    return "%02d:%02d:%06.3f" % (h, m, s)

lines = []
prev_end = 0.0
for i, c in enumerate(cues, 1):
    s = max(c[0][1], prev_end)
    e = max(c[-1][2], s + 0.8)
    if i < len(cues): e = min(e, cues[i][0][1] - 0.04) if cues[i][0][1] - 0.04 > s + 0.5 else e
    prev_end = e
    text = " ".join(x[0] for x in c)
    text = re.sub(r"(?<=[^\s ])([?!:;»])", lambda m: " " + m.group(1), text).replace("« ", "« ")
    text = re.sub(r"(Allez, ciao)\s*$", "\1 !", text) if i == len(cues) else text
    text = wrap(text)
    lines.append(f"{i}\n{ts(s).replace('.', ',')} --> {ts(e).replace('.', ',')}\n{text}\n")
open(OUT_SRT, "w", encoding="utf-8", newline="\n").write("\n".join(lines))

rep = [f"# Altyazı inceleme raporu — {len(cues)} cue\n",
       "ASR (Whisper large-v3, v2 sesi) zamanları esas; metin onaylı scripte göre düzeltildi. Aşağıda ASR ile script arasındaki farklar var (düzeltme: ASR → script).\n"]
for kind, a, s, t in review:
    mm = int(t // 60); ss = t % 60
    rep.append(f"- [{mm:02d}:{ss:04.1f}] {kind}: ASR « {a} » → SCRIPT « {s} »" if kind.startswith(("rempl", "REMPL")) else f"- [{mm:02d}:{ss:04.1f}] {kind}: « {a or s} »")
open(OUT_REP, "w", encoding="utf-8", newline="\n").write("\n".join(rep) + "\n")
print("cues", len(cues), "review", len(review))
