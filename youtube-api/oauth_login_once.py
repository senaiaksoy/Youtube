from pathlib import Path
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json

SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]
BASE = Path(__file__).resolve().parent
TOKEN_FILE = BASE / "token.json"
CLIENT_SECRET = BASE / "client_secret.json"

flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
port = int(os.environ.get("YOUTUBE_OAUTH_PORT", "8091"))
creds = flow.run_local_server(
    port=port,
    open_browser=True,
    prompt="select_account consent",
)
TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")

youtube = build("youtube", "v3", credentials=creds)
channel = youtube.channels().list(part="snippet", mine=True).execute()["items"][0]
print(json.dumps({
    "channelId": channel["id"],
    "title": channel["snippet"]["title"],
    "customUrl": channel["snippet"].get("customUrl"),
}, ensure_ascii=True, indent=2), flush=True)
