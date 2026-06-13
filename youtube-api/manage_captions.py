import sys
import argparse
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import io

BASE = Path(__file__).resolve().parent
TOKEN = BASE / "token.json"  # Force using the newly generated token.json with force-ssl scope

VIDEO_ID = "pqc9UgCIqo0"

def get_service():
    if not TOKEN.exists():
        print(f"ERROR: Token file not found at {TOKEN}")
        sys.exit(1)
    creds = Credentials.from_authorized_user_file(str(TOKEN), [
        "https://www.googleapis.com/auth/youtube",
        "https://www.googleapis.com/auth/youtube.force-ssl"
    ])
    return build("youtube", "v3", credentials=creds)

def list_captions(yt):
    print(f"Fetching caption tracks for video: {VIDEO_ID}...")
    try:
        resp = yt.captions().list(part="snippet", videoId=VIDEO_ID).execute()
        items = resp.get("items", [])
        print(f"Found {len(items)} caption tracks:")
        for idx, item in enumerate(items):
            sn = item["snippet"]
            print(f"  [{idx}] ID: {item['id']}")
            print(f"      Language: {sn.get('language')}")
            print(f"      Name: {sn.get('name')}")
            print(f"      TrackKind: {sn.get('trackKind')}")
            print(f"      Status: {sn.get('status')}")
        return items
    except HttpError as e:
        print(f"❌ API Error listing captions: {e}")
        sys.exit(1)

def download_caption(yt, caption_id, output_path):
    print(f"Downloading caption track {caption_id} to {output_path}...")
    try:
        request = yt.captions().download(id=caption_id, tfmt="srt")
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            if status:
                print(f"  Download progress: {int(status.progress() * 100)}%")
        
        with open(output_path, "wb") as f:
            f.write(fh.getvalue())
        print(f"✅ Caption downloaded successfully to {output_path}")
    except HttpError as e:
        print(f"❌ API Error downloading caption: {e}")
        sys.exit(1)

def upload_caption(yt, file_path, language_code, name):
    print(f"Uploading caption track {file_path} for language '{language_code}'...")
    if not Path(file_path).exists():
        print(f"ERROR: File not found: {file_path}")
        sys.exit(1)
        
    try:
        media = MediaFileUpload(file_path, mimetype="*/*", resumable=True)
        request = yt.captions().insert(
            part="snippet",
            body={
                "snippet": {
                    "videoId": VIDEO_ID,
                    "language": language_code,
                    "name": name,
                    "isDraft": False
                }
            },
            media_body=media
        )
        response = request.execute()
        print("✅ Caption uploaded successfully!")
        print(json.dumps(response, ensure_ascii=False, indent=2))
    except HttpError as e:
        print(f"❌ API Error uploading caption: {e}")
        sys.exit(1)

def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store_true", help="List caption tracks")
    parser.add_argument("--download", type=str, help="Caption ID to download")
    parser.add_argument("--output", type=str, default="subtitles_fr.srt", help="Output file path for download")
    parser.add_argument("--upload", type=str, help="File path to upload")
    parser.add_argument("--lang", type=str, default="ar", help="Language code for upload (default: ar)")
    parser.add_argument("--name", type=str, default="Arabic", help="Name of the subtitle track (default: Arabic)")
    args = parser.parse_args()

    yt = get_service()

    if args.list:
        list_captions(yt)
    elif args.download:
        download_caption(yt, args.download, args.output)
    elif args.upload:
        upload_caption(yt, args.upload, args.lang, args.name)
    else:
        # Default action: list captions
        list_captions(yt)

if __name__ == "__main__":
    main()
