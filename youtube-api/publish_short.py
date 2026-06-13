"""Publish and update metadata for the IMSI Shorts video."""
import sys
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

BASE = Path(__file__).resolve().parent
TOKEN = BASE / "token.senaiaksoy.20260510-193158.json"
if not TOKEN.exists():
    TOKEN = BASE / "token.json"

VIDEO_ID = "oCVZ8johrR0"
LONG_FORM_VIDEO_ID = "pqc9UgCIqo0"

TITLE = "Grossissement 6000x en FIV : Pourquoi l'IMSI ?"
DESCRIPTION = (
    "Pourquoi l'IMSI à un grossissement de 6000x peut-elle être supérieure à l'ICSI classique ? "
    "Le Dr. Senai Aksoy vous explique la détection des vacuoles spermatiques en 55 secondes.\n\n"
    f"📖 Vidéo complète : https://www.youtube.com/watch?v={LONG_FORM_VIDEO_ID}\n"
    "📖 Article de référence : https://draksoyivf.com/fr/selection-spermatique-avancee?utm_source=youtube&utm_medium=short&utm_campaign=imsi-short\n\n"
    "📌 Ce contenu est informatif. Il ne remplace pas une évaluation médicale individuelle.\n\n"
    "#IMSI #ICSI #FIV #sperme #infertilitémasculine #drsenaiaksoy"
)
TAGS = ["IMSI", "ICSI", "FIV", "sperme", "infertilité masculine", "Dr. Senai Aksoy"]

def main():
    # Force stdout to use UTF-8 to prevent any encoding issues in Windows shell
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

    if not TOKEN.exists():
        print(f"ERROR: Token file not found: {TOKEN}")
        sys.exit(1)
        
    creds = Credentials.from_authorized_user_file(str(TOKEN), ["https://www.googleapis.com/auth/youtube"])
    yt = build("youtube", "v3", credentials=creds)
    
    # 1. Fetch current video details to preserve category or other values if needed
    print(f"INFO: Fetching current details for video: {VIDEO_ID}...")
    try:
        current_res = yt.videos().list(part="snippet", id=VIDEO_ID).execute()
        items = current_res.get("items", [])
        if not items:
            print(f"ERROR: Video {VIDEO_ID} not found in the channel uploads.")
            sys.exit(1)
        current_snippet = items[0]["snippet"]
        category_id = current_snippet.get("categoryId", "26")
    except HttpError as e:
        print(f"ERROR: API Error: {e}")
        sys.exit(1)
        
    # 2. Update metadata (snippet) and make it public (status)
    print("INFO: Updating metadata and publishing the video...")
    try:
        update_body = {
            "id": VIDEO_ID,
            "snippet": {
                "title": TITLE,
                "description": DESCRIPTION,
                "tags": TAGS,
                "categoryId": category_id
            },
            "status": {
                "privacyStatus": "public"
            }
        }
        update_res = yt.videos().update(part="snippet,status", body=update_body).execute()
        print("SUCCESS: Video metadata updated and privacy status set to PUBLIC!")
        print(f"SUCCESS: Public URL: https://youtube.com/shorts/{VIDEO_ID}")
    except HttpError as e:
        print(f"ERROR: Failed to update video: {e}")
        sys.exit(1)
        
    # 3. Insert the top-level comment
    print("INFO: Posting the pinned comment...")
    try:
        comment_text = (
            "Votre conjoint a-t-il effectué un test de fragmentation de l'ADN spermatique ? "
            "Vous a-t-on proposé l'IMSI, la PICSI ou le MACS lors de votre parcours FIV ? "
            "Partagez votre expérience en commentaire, je ferai mon possible pour répondre à vos questions.\n\n"
            "🔬 Sources de référence : Cochrane Review. Détails sur draksoyivf.com"
        )
        comment_body = {
            "snippet": {
                "videoId": VIDEO_ID,
                "topLevelComment": {
                    "snippet": {
                        "textOriginal": comment_text
                    }
                }
            }
        }
        comment_res = yt.commentThreads().insert(part="snippet", body=comment_body).execute()
        print("SUCCESS: Comment posted successfully!")
    except HttpError as e:
        print(f"WARNING: Could not post comment: {e}")

if __name__ == "__main__":
    main()
