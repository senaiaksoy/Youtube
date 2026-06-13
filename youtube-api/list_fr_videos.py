"""List all FR channel video titles via YouTube Data API."""
import json
import sys
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

BASE = Path(__file__).resolve().parent
TOKEN = BASE / "token.senaiaksoy.20260510-193158.json"
if not TOKEN.exists():
    TOKEN = BASE / "token.json"

CHANNEL_ID = "UC51eCoXFnN1DiBd1dWcJpPQ"
UPLOADS = "UU" + CHANNEL_ID[2:]

creds = Credentials.from_authorized_user_file(str(TOKEN), ["https://www.googleapis.com/auth/youtube"])
yt = build("youtube", "v3", credentials=creds)

videos = []
page = None
while True:
    resp = yt.playlistItems().list(
        playlistId=UPLOADS,
        part="snippet,contentDetails",
        maxResults=50,
        pageToken=page,
    ).execute()
    for it in resp.get("items", []):
        sn = it["snippet"]
        videos.append({
            "id": it["contentDetails"]["videoId"],
            "title": sn["title"],
            "publishedAt": sn.get("publishedAt"),
        })
    page = resp.get("nextPageToken")
    if not page:
        break

out = BASE / "fr_video_titles.json"
out.write_text(json.dumps(videos, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"TOTAL {len(videos)}")
print(f"WROTE {out}")
