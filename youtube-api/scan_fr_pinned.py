"""READ-ONLY diagnostic.
Classify FR videos and detect whether the channel already has a top-level comment.
No writes. No pin changes."""
import json
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

# 1) gather all upload video ids
ids = []
page = None
while True:
    resp = yt.playlistItems().list(playlistId=UPLOADS, part="contentDetails",
                                   maxResults=50, pageToken=page).execute()
    for it in resp.get("items", []):
        ids.append(it["contentDetails"]["videoId"])
    page = resp.get("nextPageToken")
    if not page:
        break

# 2) pull language metadata in batches of 50
meta = {}
for i in range(0, len(ids), 50):
    chunk = ids[i:i+50]
    resp = yt.videos().list(part="snippet", id=",".join(chunk)).execute()
    for it in resp.get("items", []):
        sn = it["snippet"]
        meta[it["id"]] = {
            "title": sn["title"],
            "dl": sn.get("defaultLanguage"),
            "dal": sn.get("defaultAudioLanguage"),
        }

def is_fr(m):
    return (m["dl"] or "").startswith("fr") or (m["dal"] or "").startswith("fr")

fr = [vid for vid in ids if vid in meta and is_fr(meta[vid])]
unknown = [vid for vid in ids if vid in meta and not meta[vid]["dl"] and not meta[vid]["dal"]]

print(f"TOTAL uploads: {len(ids)}")
print(f"FR (by lang tag): {len(fr)}")
print(f"No lang tag at all: {len(unknown)}")

out = {"fr_ids": fr, "unknown_ids": unknown,
       "meta": {k: meta[k] for k in fr + unknown}}
(BASE / "scan_fr_result.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print("WROTE scan_fr_result.json")
