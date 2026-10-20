"""i18n/<lang>.json -> i18n/srt/glp1-fertilite-fr-recut.<lang>.srt (FR timings, 2×42 wrap) + QA + localizations fixes.
Usage: py -3.12 -I build_i18n.py   (writes qa.json and fixes-localizations.json; never uploads)"""
import json, re, sys, pathlib
sys.stdout.reconfigure(encoding='utf-8')
P = pathlib.Path(__file__).parent
LANGS = ['ar', 'az', 'bg', 'bs', 'de', 'en', 'es', 'fa', 'it', 'mk', 'ro', 'ru', 'sq', 'sr', 'tr', 'uk']
src = json.load(open(P / 'source.json', encoding='utf-8'))
tim = json.load(open(P / 'timings.json', encoding='utf-8'))
fr_by_i = {c['i']: c['fr'] for c in src['cues']}
stamps = re.findall(r'^(\d\d:\d\d) ', src['description_fr'], re.M)
BRANDS = re.compile(r'ozempic|wegovy|mounjaro|saxenda|zepbound|victoza|rybelsus|trulicity', re.I)
WORDNUM = {'2': ['deux'], '4': ['quatre'], '8': ['huit'], '1': ['un', 'une']}

def wrap(t, n=42):
    t = ' '.join(t.split())
    if len(t) <= n: return t
    w = t.split(' ')
    i = min(range(1, len(w)), key=lambda i: (max(len(' '.join(w[:i])), len(' '.join(w[i:]))), abs(len(' '.join(w[:i])) - len(' '.join(w[i:])))))
    return ' '.join(w[:i]) + '\n' + ' '.join(w[i:])

qa, locs = {}, {}
(P / 'srt').mkdir(exist_ok=True)
for L in LANGS:
    f = P / f'{L}.json'
    if not f.exists(): qa[L] = {'missing': True}; continue
    d = json.load(open(f, encoding='utf-8'))
    cues = d['cues']; issues = []
    if [c['i'] for c in cues] != [c['i'] for c in tim]: issues.append('cue index/order mismatch')
    for c in cues:
        t = c['text'].strip()
        tn = t.translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789'))
        if not t: issues.append(f"empty cue {c['i']}")
        if BRANDS.search(t): issues.append(f"brand in cue {c['i']}")
        if len(t) > 96: issues.append(f"long cue {c['i']} ({len(t)})")
        for num in re.findall(r'\d+', fr_by_i[c['i']].replace('\u202f', '')):
            if num not in re.sub(r'[^0-9]', ' ', tn).split() and num not in ('1', '2', '3', '4', '8'):
                issues.append(f"number {num} missing in cue {c['i']}")
    title, desc = d['title'].strip(), d['description'].strip()
    if len(title) > 100: issues.append(f'title too long ({len(title)})')
    if len(desc) > 5000: issues.append(f'description too long ({len(desc)})')
    miss = [s for s in stamps if s not in desc]
    if miss: issues.append(f'missing timestamps {miss}')
    if BRANDS.search(title + desc): issues.append('brand in title/description')
    out = []
    for c, t in zip(cues, tim):
        out.append(f"{t['i']}\n{t['t']}\n{wrap(c['text'])}\n")
    (P / 'srt' / f'glp1-fertilite-fr-recut.{L}.srt').write_text('\n'.join(out), encoding='utf-8')
    longest = max(len(l) for c in cues for l in wrap(c['text']).split('\n'))
    qa[L] = {'cues': len(cues), 'title': title, 'title_len': len(title), 'desc_len': len(desc), 'longest_line': longest, 'issues': issues}
    locs[L] = {'title': title, 'description': desc}
json.dump(qa, open(P / 'qa.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump({'video_id': 'U-ophcWNOro', 'localizations': locs}, open(P / 'fixes-localizations.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for L, q in qa.items(): print(L, q if q.get('missing') else f"{q['cues']} cues | title {q['title_len']} | desc {q['desc_len']} | longest line {q['longest_line']} | issues {len(q['issues'])}")
