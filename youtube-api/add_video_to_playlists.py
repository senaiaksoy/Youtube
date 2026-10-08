import sys
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

BASE = Path(__file__).resolve().parent
TOKEN = BASE / "token.senaiaksoy.20260510-193158.json"
if not TOKEN.exists():
    TOKEN = BASE / "token.json"

VIDEO_ID = "zhcapjJhxzA"
PLAYLIST_IDS = [
    "PL21Sr5bmkPJVnapVaNbfq5Yyp8l8LbkHl",  # Patients internationaux : Votre parcours FIV à Istanbul
    "PL21Sr5bmkPJUqGpLW3_Zxzre7pJ4klZTe",  # Débuter la FIV : parcours, examens et décisions
    "PL21Sr5bmkPJXmf7cJMbIW8p_VQ910IWf2"   # Tout comprendre sur la fécondation in vitro (FIV)
]

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

    if not TOKEN.exists():
        print(f"ERROR: Token file not found: {TOKEN}")
        sys.exit(1)

    creds = Credentials.from_authorized_user_file(str(TOKEN), [
        "https://www.googleapis.com/auth/youtube"
    ])
    yt = build("youtube", "v3", credentials=creds)

    for playlist_id in PLAYLIST_IDS:
        print(f"INFO: Checking playlist {playlist_id}...")
        # Check if already exists in playlist to avoid duplicates
        try:
            exists = False
            page = None
            while True:
                resp = yt.playlistItems().list(
                    part="snippet,contentDetails",
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=page
                ).execute()
                for item in resp.get("items", []):
                    if item["contentDetails"]["videoId"] == VIDEO_ID:
                        exists = True
                        break
                page = resp.get("nextPageToken")
                if exists or not page:
                    break
            
            if exists:
                print(f"INFO: Video already exists in playlist {playlist_id}.")
                continue
            
            # Insert video into playlist
            print(f"INFO: Adding video to playlist {playlist_id}...")
            yt.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": VIDEO_ID
                        }
                    }
                }
            ).execute()
            print(f"SUCCESS: Added to playlist {playlist_id}!")
        except HttpError as e:
            print(f"ERROR: Failed for playlist {playlist_id}: {e}")

if __name__ == "__main__":
    main()
