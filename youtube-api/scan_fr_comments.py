"""READ-ONLY. For each FR video, find top-level comments authored by the channel.
Detect likely-old-pinned WhatsApp comment. No writes."""
import json, re
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

BASE = Path(__file__).resolve().parent
TOKEN = BASE / "token.senaiaksoy.20260510-193158.json"
if not TOKEN.exists():
    TOKEN = BASE / "token.json"
CHANNEL_ID = "UC51eCoXFnN1DiBd1dWcJpPQ"

creds = Credentials.from_authorized_user_file(str(TOKEN), ["https://www.googleapis.com/auth/youtube"])
yt = build("youtube", "v3", credentials=creds)

scan = json.loads((BASE / "scan_fr_result.json").read_text(encoding="utf-8"))
fr = scan["fr_ids"]

has_channel_comment = []   # video has a top-level comment authored by channel
has_whatsapp = []          # that comment looks like old WhatsApp pin
no_channel_comment = []
errors = []

for vid in fr:
    try:
        resp = yt.commentThreads().list(
            part="snippet", videoId=vid, maxResults=100,
            textFormat="plainText", order="relevance").execute()
    except HttpError as e:
        errors.append((vid, str(e.status_code)))
        continue
    found = None
    for it in resp.get("items", []):
        top = it["snippet"]["topLevelComment"]["snippet"]
        acid = (top.get("authorChannelId") or {}).get("value")
        if acid == CHANNEL_ID:
            found = top["textDisplay"]
            break
    if found is None:
        no_channel_comment.append(vid)
    else:
        has_channel_comment.append(vid)
        if re.search(r"wa\.me|whatsapp|WhatsApp", found, re.I):
            has_whatsapp.append(vid)

print(f"FR videos scanned: {len(fr)}")
print(f"  with a channel top-level comment: {len(has_channel_comment)}")
print(f"    of those, looks like WhatsApp pin: {len(has_whatsapp)}")
print(f"  with NO channel comment: {len(no_channel_comment)}")
print(f"  errors (comments disabled etc): {len(errors)}")

(BASE / "scan_fr_comments_result.json").write_text(json.dumps({
    "has_channel_comment": has_channel_comment,
    "has_whatsapp": has_whatsapp,
    "no_channel_comment": no_channel_comment,
    "errors": errors,
}, ensure_ascii=False, indent=2), encoding="utf-8")
print("WROTE scan_fr_comments_result.json")
