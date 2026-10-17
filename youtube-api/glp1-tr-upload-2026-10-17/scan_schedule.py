"""Salt-okunur: 3 kanalın son yüklemelerinde gizlilik, publishAt ve süre (Shorts ayrımı) → schedule-scan.txt.
Run: py -3.12 scan_schedule.py"""
import sys, pathlib
sys.path.insert(0, r'D:\A-klasör\Youtube\.claude\skills\yt-pipeline\scripts')
sys.stdout.reconfigure(encoding='utf-8')
from yt_common import get_service   # canlı mine=True kanal doğrulamasını yapar
D = pathlib.Path(__file__).parent
out = []
for ch in ('tr', 'fr', 'en'):
    yt = get_service(ch)
    me = yt.channels().list(part='contentDetails', mine=True).execute()['items'][0]
    up = me['contentDetails']['relatedPlaylists']['uploads']
    ids = [i['contentDetails']['videoId'] for i in yt.playlistItems().list(part='contentDetails', playlistId=up, maxResults=30).execute()['items']]
    vs = yt.videos().list(part='snippet,status,contentDetails', id=','.join(ids)).execute()['items']
    out.append(f'===== {ch}')
    for v in vs:
        st, sn = v['status'], v['snippet']
        when = st.get('publishAt') or sn['publishedAt']
        out.append(f"{ch} {v['id']} {st['privacyStatus']:8s} publishAt={st.get('publishAt', '-'):24s} published={sn['publishedAt']} dur={v['contentDetails']['duration']:10s} {sn['title'][:70]}")
(D / 'schedule-scan.txt').write_text('\n'.join(out), encoding='utf-8')
print('\n'.join(out))
