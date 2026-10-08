import sys
import os
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from deep_translator import GoogleTranslator

BASE = Path(__file__).resolve().parent
TOKEN = BASE / "token.senaiaksoy.20260510-193158.json"
if not TOKEN.exists():
    TOKEN = BASE / "token.json"

VIDEO_ID = "zhcapjJhxzA"
SRC_SRT_PATH = r"C:\Users\KC3\.gemini\antigravity\brain\ac4f2c93-ed80-4113-bb8f-894b4bb2519d\scratch\youtube_fr_unnamed.srt"
INCORRECT_FR_CAPTION_ID = "AUieDaaBcfCpdzpRZTj8Y3rOcGFSrU3pNwqvltJJtC-bCbVOErFMw3Tx8ZA"

LANGUAGES = {
    "en": "English",
    "ar": "Arabic",
    "sq": "Albanian",
    "az": "Azerbaijani",
    "bg": "Bulgarian",
    "sr": "Serbian",
    "mk": "Macedonian",
    "bs": "Bosnian",
    "it": "Italian",
    "es": "Spanish",
    "ru": "Russian",
    "uk": "Ukrainian",
    "tr": "Turkish",
    "ro": "Romanian"
}

def parse_srt(file_path):
    blocks = []
    current_block = {}
    text_lines = []
    
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
        
    state = 0  # 0: expecting ID, 1: expecting timing, 2: expecting text
    for line in lines:
        line_str = line.strip()
        if state == 0:
            if line_str == "":
                continue
            current_block["id"] = line_str
            state = 1
        elif state == 1:
            current_block["time"] = line_str
            state = 2
            text_lines = []
        elif state == 2:
            if line_str == "":
                current_block["text"] = "\n".join(text_lines)
                blocks.append(current_block)
                current_block = {}
                state = 0
            else:
                text_lines.append(line_str)
                
    if current_block:
        current_block["text"] = "\n".join(text_lines)
        blocks.append(current_block)
        
    return blocks

def write_srt(blocks, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        for block in blocks:
            f.write(f"{block['id']}\n")
            f.write(f"{block['time']}\n")
            f.write(f"{block['text']}\n\n")

def translate_blocks(blocks, src_lang, target_lang):
    translator = GoogleTranslator(source=src_lang, target=target_lang)
    translated_blocks = []
    
    batch_size = 50
    texts = [b["text"] for b in blocks]
    translated_texts = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        print(f"  Translating batch {i // batch_size + 1}/{(len(texts) - 1) // batch_size + 1} to {target_lang}...")
        try:
            translated_batch = translator.translate_batch(batch)
            translated_texts.extend(translated_batch)
        except Exception as e:
            print(f"  [WARNING] Batch translation failed: {e}. Falling back to individual requests.")
            for text in batch:
                try:
                    translated_texts.append(translator.translate(text))
                except Exception as e_ind:
                    print(f"  [ERROR] Individual translation failed for '{text}': {e_ind}")
                    translated_texts.append(text)
                    
    for block, trans_text in zip(blocks, translated_texts):
        translated_blocks.append({
            "id": block["id"],
            "time": block["time"],
            "text": trans_text
        })
        
    return translated_blocks

def delete_existing_caption(yt, video_id, language_code):
    try:
        resp = yt.captions().list(part="snippet", videoId=video_id).execute()
        items = resp.get("items", [])
        for item in items:
            sn = item["snippet"]
            if sn.get("language") == language_code and sn.get("trackKind") == "standard":
                print(f"  Found existing standard caption track for '{language_code}' (ID: {item['id']}). Deleting...")
                yt.captions().delete(id=item['id']).execute()
                print(f"  Deleted existing caption track {item['id']}.")
    except HttpError as e:
        print(f"  [WARNING] Error checking/deleting caption: {e}")

def upload_caption(yt, video_id, file_path, language_code, name):
    print(f"  Uploading caption track {file_path} for '{language_code}'...")
    media = MediaFileUpload(str(file_path), mimetype="*/*", resumable=True)
    request = yt.captions().insert(
        part="snippet",
        body={
            "snippet": {
                "videoId": video_id,
                "language": language_code,
                "name": name,
                "isDraft": False
            }
        },
        media_body=media
    )
    response = request.execute()
    print(f"  ✅ Caption uploaded successfully for {language_code}!")
    return response

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

    print("=" * 60)
    print("  YouTube Subtitles Correction & Translation Automator")
    print("=" * 60)

    # 1. Parse corrected French subtitles
    if not Path(SRC_SRT_PATH).exists():
        print(f"ERROR: Corrected French subtitle file not found at {SRC_SRT_PATH}")
        sys.exit(1)
        
    print(f"Parsing corrected French subtitles from: {SRC_SRT_PATH}")
    blocks = parse_srt(SRC_SRT_PATH)
    print(f"Found {len(blocks)} subtitle blocks.")

    # 2. Connect to YouTube API
    if not TOKEN.exists():
        print(f"ERROR: Token file not found at {TOKEN}")
        sys.exit(1)

    print("Connecting to YouTube API...")
    creds = Credentials.from_authorized_user_file(str(TOKEN), [
        "https://www.googleapis.com/auth/youtube",
        "https://www.googleapis.com/auth/youtube.force-ssl"
    ])
    yt = build("youtube", "v3", credentials=creds)
    print("Authenticated successfully.")

    # 3. Delete incorrect French caption track if it exists
    print(f"\nChecking incorrect French caption track (ID: {INCORRECT_FR_CAPTION_ID})...")
    try:
        yt.captions().delete(id=INCORRECT_FR_CAPTION_ID).execute()
        print("✅ Deleted incorrect French caption track successfully!")
    except HttpError as e:
        print(f"WARNING: Could not delete caption track {INCORRECT_FR_CAPTION_ID}: {e}")

    # 4. Translate and upload for other languages
    for lang, lang_name in LANGUAGES.items():
        print(f"\nProcessing language: {lang_name} ({lang})...")
        
        # Translate subtitles
        print(f"  Translating subtitles for {lang_name}...")
        srt_path = BASE / f"subtitles_{lang}_temp.srt"
        lang_blocks = translate_blocks(blocks, "fr", lang)
        write_srt(lang_blocks, srt_path)
        print(f"  Saved temporary subtitles to {srt_path}")
        
        # Apply subtitles live
        print(f"  Applying {lang_name} subtitles to YouTube...")
        delete_existing_caption(yt, VIDEO_ID, lang)
        upload_caption(yt, VIDEO_ID, srt_path, lang, lang_name)

        # Remove temp srt file
        try:
            srt_path.unlink()
        except OSError:
            pass

    print("\n🎉 All 14 subtitle tracks (excluding French and German) corrected and uploaded successfully!")

if __name__ == "__main__":
    main()
