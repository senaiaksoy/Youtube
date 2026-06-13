import json
import sys
import argparse
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

BASE = Path(__file__).resolve().parent
TOKEN = BASE / "token.senaiaksoy.20260510-193158.json"
if not TOKEN.exists():
    TOKEN = BASE / "token.json"

VIDEO_ID = "pqc9UgCIqo0"
PLAYLIST_TITLE = "Infertilité masculine : sperme, varicocèle, azoospermie"

TITLE = "IMSI, PICSI, MACS : comment mieux choisir les spermatozoïdes ?"

DESCRIPTION = """IMSI, PICSI, MACS : comment la science sélectionne-t-elle les spermatozoïdes en FIV ? Est-ce utile pour vous ? Le Dr. Senai Aksoy fait le point sur les preuves cliniques et les indications en 2026.

🎧 Ce contenu est également disponible en doublage et sous-titres Anglais (EN) et Arabe (AR). (Activez la piste audio/sous-titres dans les paramètres de la vidéo)
🎧 This video is also available with English (EN) and Arabic (AR) dubbing and subtitles. (Enable audio track/subtitles in video settings)
🎧 هذا المحتوى متوفر أيضاً بالدبلجة والترجمة إلى اللغتين الإنجليزية والعربية. (قم بتفعيل المسار الصوتي/الترجمة في إعدادات الفيديو)

📌 Article détaillé et ressources :
👉 https://draksoyivf.com/fr/selection-spermatique-avancee?utm_source=youtube&utm_medium=description&utm_campaign=spermogramme-advanced

⏱ Sommaire de la vidéo :
00:00 Introduction
00:48 Les limites de l'ICSI classique
02:00 Différences techniques : IMSI, PICSI et MACS
05:15 Que dit la science ? (Données Cochrane & HABSelect)
08:45 Qui doit utiliser ces techniques avancées ? (Indications)
11:15 L'avis clinique du Dr. Aksoy
12:45 Sources et ressources utiles

📚 Sources scientifiques citées :
- Cochrane Database of Systematic Reviews (2020) : Morphologically selected sperm injection for ICSI.
- The Lancet (2019) : Physiological alternative to ICSI (HABSelect trial).
- ESHRE Guidelines on Male Infertility.

ℹ️ À propos du Dr. Senai Aksoy :
Le Dr. Senai Aksoy est gynécologue-obstétricien, spécialiste de la fertilité et de la FIV à Istanbul, avec plus de 30 ans d'expérience clinique. Diplômé de l'Université Paris René Descartes, il accompagne les couples francophones dans leur projet parental.

⚠️ Ce contenu est informatif. Il ne remplace pas une évaluation médicale individuelle.

#sperme #IMSI #PICSI #MACS #FIV #PMA #infertilitemasculine #drsenaiaksoy"""

TAGS = [
    "IMSI", "PICSI", "MACS", "sélection spermatique", "spermatozoïdes", "FIV", 
    "PMA", "facteur masculin", "infertilité masculine", "Dr Senai Aksoy", 
    "HABSelect", "Cochrane", "fragmentation ADN spermatique", "triage sperme"
]

def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass # Fallback for older python versions
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Apply changes live to YouTube")
    args = parser.parse_args()
    dry_run = not args.apply

    print("=" * 60)
    print("  YouTube Specific Video Update Tool")
    print("=" * 60)
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print(f"Video ID: {VIDEO_ID}")
    
    if not TOKEN.exists():
        print(f"ERROR: Token file not found at {TOKEN}")
        sys.exit(1)

    creds = Credentials.from_authorized_user_file(str(TOKEN), ["https://www.googleapis.com/auth/youtube"])
    yt = build("youtube", "v3", credentials=creds)
    print("✅ Authenticated with YouTube API successfully.")

    # 1. Fetch current video details
    try:
        vid_resp = yt.videos().list(part="snippet", id=VIDEO_ID).execute()
        items = vid_resp.get("items", [])
        if not items:
            print(f"❌ Video not found on YouTube: {VIDEO_ID}")
            sys.exit(1)
        video = items[0]
        snippet = video["snippet"]
        print(f"Current Title: {snippet.get('title')}")
    except HttpError as e:
        print(f"❌ API Error fetching video: {e}")
        sys.exit(1)

    # 2. Update Video Snippet
    print("\nProposed Changes:")
    print(f"Title: {TITLE}")
    print("Description length:", len(DESCRIPTION))
    print(f"Tags: {', '.join(TAGS)}")

    if not dry_run:
        # Update snippet
        snippet["title"] = TITLE
        snippet["description"] = DESCRIPTION
        snippet["tags"] = TAGS
        snippet["categoryId"] = snippet.get("categoryId", "26") # Keep existing or default to 26

        try:
            update_resp = yt.videos().update(
                part="snippet",
                body={
                    "id": VIDEO_ID,
                    "snippet": {
                        "title": snippet["title"],
                        "description": snippet["description"],
                        "tags": snippet["tags"],
                        "categoryId": snippet["categoryId"],
                        "defaultLanguage": "fr"
                    }
                }
            ).execute()
            print("✅ Video metadata updated successfully!")
        except HttpError as e:
            print(f"❌ API Error updating video metadata: {e}")
            sys.exit(1)
    else:
        print("🔍 [Dry Run] Video metadata update skipped.")

    # 3. Add to Playlist
    print(f"\nTarget Playlist: {PLAYLIST_TITLE}")
    playlist_id = None
    try:
        pl_resp = yt.playlists().list(part="id,snippet", mine=True, maxResults=50).execute()
        for pl in pl_resp.get("items", []):
            if pl["snippet"]["title"].strip() == PLAYLIST_TITLE.strip():
                playlist_id = pl["id"]
                break
        
        if not playlist_id:
            print(f"❌ Playlist not found by title: {PLAYLIST_TITLE}")
        else:
            print(f"Found Playlist ID: {playlist_id}")
            # Check if video already in playlist
            items_resp = yt.playlistItems().list(part="id,contentDetails", playlistId=playlist_id, maxResults=50).execute()
            already_in = False
            for item in items_resp.get("items", []):
                if item["contentDetails"]["videoId"] == VIDEO_ID:
                    already_in = True
                    break
            
            if already_in:
                print("ℹ️ Video is already in the playlist.")
            else:
                if not dry_run:
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
                    print("✅ Added video to playlist successfully!")
                else:
                    print("🔍 [Dry Run] Playlist insertion skipped.")
    except HttpError as e:
        print(f"❌ API Error during playlist operations: {e}")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
