"""Build the definitive French-AUDIO video list (defaultAudioLanguage starts with 'fr').
READ-ONLY. Writes fr_audio_videos.json + a human-readable .txt for review."""
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

BASE = Path(__file__).resolve().parent
TOKEN = BASE / "token.senaiaksoy.20260510-193158.json"
if not TOKEN.exists():
    TOKEN = BASE / "token.json"
CH = "UC51eCoXFnN1DiBd1dWcJpPQ"; UP = "UU" + CH[2:]

creds = Credentials.from_authorized_user_file(str(TOKEN), ["https://www.googleapis.com/auth/youtube"])
yt = build("youtube", "v3", credentials=creds)

ids, page = [], None
while True:
    r = yt.playlistItems().list(playlistId=UP, part="contentDetails", maxResults=50, pageToken=page).execute()
    ids += [i["contentDetails"]["videoId"] for i in r["items"]]
    page = r.get("nextPageToken")
    if not page:
        break

fr = []
for i in range(0, len(ids), 50):
    r = yt.videos().list(part="snippet", id=",".join(ids[i:i+50])).execute()
    for it in r["items"]:
        sn = it["snippet"]
        dal = sn.get("defaultAudioLanguage") or ""
        if dal.startswith("fr"):
            fr.append({"id": it["id"], "title": sn["title"],
                       "dal": dal, "publishedAt": sn.get("publishedAt")})

fr.sort(key=lambda v: v["publishedAt"] or "", reverse=True)
(BASE / "fr_audio_videos.json").write_text(json.dumps(fr, ensure_ascii=False, indent=2), encoding="utf-8")
lines = [f"{n+1:3}. [{v['id']}] {v['title']}" for n, v in enumerate(fr)]
(BASE / "fr_audio_videos.txt").write_text("\n".join(lines), encoding="utf-8")
print(f"FR-audio videos: {len(fr)}")
print(f"WROTE fr_audio_videos.json + fr_audio_videos.txt")
