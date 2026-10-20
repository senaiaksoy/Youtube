"""Build yt_metadata fixes for the two EN Shorts from SHORTS-EN.md. Usage: py -3.12 build_shorts_fixes.py <idA> <idB>"""
import json, re, sys, pathlib
sys.stdout.reconfigure(encoding='utf-8')
O = pathlib.Path(__file__).parent
t = (O / 'SHORTS-EN.md').read_text(encoding='utf-8')
blocks = re.split(r'\n## glp1-short-', t)[1:]
slots = {'A': '2026-10-29T16:00:00Z', 'B': '2026-10-31T16:00:00Z'}
fixes = []
for vid, b in zip(sys.argv[1:3], blocks):
    key = b[0]
    title = re.search(r'\*\*Title:\*\* (.+)', b).group(1).strip()
    desc = b.split('**Title:**', 1)[1].split('\n', 1)[1].split('\n\nTags:')[0].strip()
    tags = [x.strip() for x in re.search(r'\nTags: (.+)', b).group(1).split(',')]
    fixes.append({'video_id': vid, 'title': title, 'description': desc, 'tags': tags, 'categoryId': '27',
                  'defaultLanguage': 'en-US', 'defaultAudioLanguage': 'en-US',
                  'localizations': {'en-US': {'title': title, 'description': desc}},
                  'status': {'privacyStatus': 'private', 'publishAt': slots[key]}})
    print(key, vid, len(title), 'chars title |', len(desc), 'chars desc |', len(tags), 'tags |', slots[key])
    print('  ', title)
json.dump(fixes, open(O / 'fixes-en-shorts.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
