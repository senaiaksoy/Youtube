"""TR GLP-1 Shorts metadata + planlama → fixes-tr-shorts.json (SHORTS-METADATA-TR.md metinleri). Run: py -3.12 -I build_shorts_fixes.py"""
import json, re, pathlib
D = pathlib.Path(__file__).parent
md = pathlib.Path(r'D:/A-klasör/openmontage/projects/2026-10-17-glp1-infertilite-tr-shorts/SHORTS-METADATA-TR.md').read_text(encoding='utf-8')
IDS = {'A': ('521shfez8kU', '2026-10-22T14:00:00Z'), 'B': ('W1vSQ4OzgbI', '2026-10-24T14:00:00Z')}
fixes = []
for k, (vid, when) in IDS.items():
    sec = md.split(f'## glp1-tr-short-{k}.mp4')[1].split('\n## ')[0]
    title = re.search(r'\*\*Başlık:\*\* (.+)', sec).group(1).strip()
    tags = [t.strip() for t in re.search(r'Etiketler: (.+)', sec).group(1).split(',')]
    body = sec.split(title, 1)[1].split('\nEtiketler:')[0].strip()
    assert len(title) <= 100 and len(body) < 5000 and '#Shorts' in title
    fixes.append({'video_id': vid, 'title': title, 'description': body, 'tags': tags, 'categoryId': '27',
                  'defaultLanguage': 'tr', 'defaultAudioLanguage': 'tr', 'status': {'privacyStatus': 'private', 'publishAt': when}})
    print(k, vid, when, '|', title, '|', len(body), 'karakter |', len(tags), 'etiket')
json.dump(fixes, open(D / 'fixes-tr-shorts.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
