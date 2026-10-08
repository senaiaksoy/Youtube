#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
YouTube Subtitle & Video Metadata Automator

This tool automates:
  1. Multi-lingual subtitle translation (SRT) and upload.
  2. Video title and description translation and metadata localization.
  3. Bulk subtitle text search and replace corrections.
  4. Video playlist checking and mapping.
  5. Regulatory disclaimer insertion.

Requires:
  pip install google-api-python-client google-auth-oauthlib deep-translator
"""

import argparse
import sys
import os
import json
import time
from pathlib import Path
from deep_translator import GoogleTranslator

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaFileUpload
except ImportError:
    print("❌ Gerekli paketler yuklu degil. Sunu calistirin:")
    print("   pip install google-api-python-client google-auth-oauthlib deep-translator")
    sys.exit(1)

# ---------------------------------------------------------------------------
# CONSTANTS & CONFIGURATION
# ---------------------------------------------------------------------------
SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]
API_SERVICE = "youtube"
API_VERSION = "v3"

BASE_DIR = Path(__file__).resolve().parent
TOKEN_FILE = BASE_DIR / "token.json"
CLIENT_SECRET = BASE_DIR / "client_secret.json"

DEFAULT_LANGUAGES = {
    "en": "English",
    "ar": "Arabic",
    "de": "German",
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

# ---------------------------------------------------------------------------
# LOCALIZED MEDICAL DISCLAIMERS (Turkish Health Compliance Regulation)
# ---------------------------------------------------------------------------
DISCLAIMERS = {
    "tr": """⚕️ ÖNEMLİ TIBBİ UYARI
Bu videoda sunulan bilgiler yalnızca eğitim ve bilgilendirme amaçlıdır. Bu içerik hiçbir koşulda tıbbi tavsiye, tanı veya kişiselleştirilmiş tedavi önerisi niteliği taşımamaktadır.
Her hastanın tıbbi durumu kendine özgüdür. Bu videoda ele alınan konular; bir hekim, kadın doğum uzmanı veya üreme tıbbı uzmanı ile yapılacak konsültasyonun yerini tutmaz.
Bu videodaki bilgilere dayanarak mevcut tedavinizi değiştirmeyin, yeni bir tedaviye başlamayın veya herhangi bir tıbbi karar almayın. Her türlü tıbbi karar öncesinde mutlaka aile hekiminize veya uzman doktorunuza danışınız.
Üreme sağlığınız veya IVF tedavi sürecinizle ilgili sorularınız için lütfen yetkili bir sağlık profesyoneline başvurunuz.
© Doç. Dr. Senai Aksoy — Tüm hakları saklıdır.""",

    "fr": """⚕️ AVERTISSEMENT MÉDICAL IMPORTANT
Les informations présentées dans cette vidéo sont fournies uniquement à des fins éducatives et informatives. Ce contenu ne constitue en aucun cas un avis médical, un diagnostic ou une suggestion de traitement personnalisé.
La situation médicale de chaque patient est unique. Les sujets abordés dans cette vidéo ne remplacent pas une consultation avec un médecin, un gynécologue-obstétricien ou un spécialiste de la médecine de la reproduction.
Ne modifiez pas votre traitement actuel, ne commencez pas de nouveau traitement et ne prenez aucune décision médicale sur la base des informations contenues dans cette vidéo. Pour toute décision médicale, consultez toujours votre médecin de famille ou votre médecin spécialiste.
Pour toute question concernant votre santé reproductive ou votre parcours de FIV, veuillez contacter un professionnel de la santé agréé.
© Doç. Dr. Senai Aksoy — Tous droits réservés.""",

    "en": """⚕️ IMPORTANT MEDICAL DISCLAIMER
The information presented in this video is for educational and informational purposes only. This content does not under any circumstances constitute medical advice, diagnosis, or personalized treatment recommendations.
Each patient's medical condition is unique. The topics discussed in this video do not replace a consultation with a physician, obstetrician-gynecologist, or reproductive medicine specialist.
Do not change your current treatment, start a new treatment, or make any medical decisions based on the information in this video. Always consult your family doctor or specialist physician before making any medical decisions.
For questions regarding your reproductive health or IVF treatment process, please consult a licensed healthcare professional.
© Doç. Dr. Senai Aksoy — All rights reserved.""",

    "ar": """⚕️ تحذير طبي هام
المعلومات الواردة في هذا الفيديو هي لأغراض تعليمية وإرشادية فقط. لا يشكل هذا المحتوى بأي حال من الأحوال نصيحة طبية أو تشخيصاً أو توصية بعلاج شخصي.
الحالة الطبية لكل مريض فريدة من نوعها. المواضيع التي تمت مناقشتها في هذا الفيديو لا تغني عن استشارة الطبيب، أو أخصائي التوليد وأمراض النساء، أو أخصائي طب التناسل.
لا تغير علاجك الحالي، أو تبدأ علاجاً جديداً، أو تتخذ أي قرارات طبية بناءً على المعلومات الواردة في هذا الفيديو. استشر دائماً طبيب العائلة أو الطبيب المختص قبل اتخاذ أي قرار طبي.
للأسئلة المتعلقة بصحتك الإنجابية أو عملية علاج أطفال الأنابيب (FIV)، يرجى مراجعة أخصائي رعاية صحية مرخص.
© Doç. Dr. Senai Aksoy — جميع الحقوق محفوظة."""
}

# ---------------------------------------------------------------------------
# CORE HELPER FUNCTIONS
# ---------------------------------------------------------------------------
def setup_encoding():
    """Ensure standard input and output streams are using UTF-8 encoding."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

def authenticate():
    """Authenticate with YouTube Data API using OAuth 2.0."""
    creds = None
    # Check for existing token
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired credentials token...")
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"⚠️ Token refresh failed: {e}. Initiating full OAuth flow...")
                creds = None
        
        if not creds:
            if not CLIENT_SECRET.exists():
                print(f"❌ ERROR: Client secret file not found at: {CLIENT_SECRET}")
                print("Please download client_secret.json from Google Cloud Console.")
                sys.exit(1)
            
            print("🔐 Launching local server for browser OAuth login...")
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
            creds = flow.run_local_server(port=8090, open_browser=True)
        
        TOKEN_FILE.write_text(creds.to_json())
        print(f"✅ Credentials token saved to: {TOKEN_FILE}")
        
    return build(API_SERVICE, API_VERSION, credentials=creds)

def parse_srt(file_path):
    """Parse SRT subtitle file into structured blocks."""
    blocks = []
    current_block = {}
    text_lines = []
    
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
        
    state = 0  # 0: ID, 1: Timing, 2: Text
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
    """Write blocks into an SRT subtitle file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        for block in blocks:
            f.write(f"{block['id']}\n")
            f.write(f"{block['time']}\n")
            f.write(f"{block['text']}\n\n")

def get_disclaimer(lang_code):
    """Get the localized medical disclaimer for a language code."""
    if lang_code in DISCLAIMERS:
        return DISCLAIMERS[lang_code]
    
    # Fallback to translating the English disclaimer to the target language
    english_disclaimer = DISCLAIMERS["en"]
    try:
        print(f"  [INFO] Generating dynamic disclaimer translation for '{lang_code}'...")
        translator = GoogleTranslator(source="en", target=lang_code)
        return translator.translate(english_disclaimer)
    except Exception as e:
        print(f"  [WARNING] Disclaimer translation failed: {e}. Using English disclaimer.")
        return english_disclaimer

def translate_blocks(blocks, src_lang, target_lang):
    """Translate SRT subtitle text blocks into a target language."""
    translator = GoogleTranslator(source=src_lang, target=target_lang)
    translated_blocks = []
    
    batch_size = 50
    texts = [b["text"] for b in blocks]
    translated_texts = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        print(f"  Translating subtitles batch {i // batch_size + 1}/{(len(texts) - 1) // batch_size + 1} to {target_lang}...")
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

def translate_text(text, src_lang, target_lang):
    """Translate plain text into target language."""
    if not text:
        return ""
    try:
        translator = GoogleTranslator(source=src_lang, target=target_lang)
        return translator.translate(text)
    except Exception as e:
        print(f"  [ERROR] Failed to translate text to {target_lang}: {e}")
        return text

# ---------------------------------------------------------------------------
# YOUTUBE API OPERATIONS
# ---------------------------------------------------------------------------
def list_recent_videos(yt, max_results=10):
    """List recent videos uploaded to the channel."""
    print(f"INFO: Fetching last {max_results} videos...")
    try:
        resp = yt.search().list(
            part="snippet",
            type="video",
            maxResults=max_results,
            order="date"
        ).execute()
        
        items = resp.get("items", [])
        if not items:
            print("No videos found.")
            return
            
        print("\n" + "=" * 80)
        print(f"{'Video ID':<15} | {'Publish Date':<20} | {'Title'}")
        print("=" * 80)
        for item in items:
            snippet = item["snippet"]
            vid_id = item["id"]["videoId"]
            title = snippet["title"]
            pub_date = snippet["publishedAt"]
            print(f"{vid_id:<15} | {pub_date:<20} | {title}")
        print("=" * 80 + "\n")
        
    except HttpError as e:
        print(f"❌ YouTube API Error listing videos: {e}")

def print_video_info(yt, video_id):
    """Print detailed video metadata, localizations, and caption tracks."""
    print(f"INFO: Fetching details for video ID: {video_id}...")
    try:
        # Fetch video metadata
        vid_resp = yt.videos().list(part="snippet,status,localizations", id=video_id).execute()
        items = vid_resp.get("items", [])
        if not items:
            print(f"❌ ERROR: Video {video_id} not found.")
            return
            
        video = items[0]
        snippet = video["snippet"]
        status = video["status"]
        localizations = video.get("localizations", {})
        
        print("\n" + "=" * 80)
        print(f"VIDEO DETAILS: {video_id}")
        print("=" * 80)
        print(f"Title (Default):      {snippet.get('title')}")
        print(f"Default Language:     {snippet.get('defaultLanguage', 'Not Set (Usually inherits channel default)')}")
        print(f"Privacy Status:       {status.get('privacyStatus')}")
        print(f"Scheduled Publish:    {status.get('publishAt', 'Not scheduled')}")
        print(f"Tags:                 {', '.join(snippet.get('tags', []))}")
        print(f"Active Localizations: {', '.join(localizations.keys())}")
        
        # Fetch caption tracks
        print("-" * 80)
        print("CAPTION TRACKS:")
        cap_resp = yt.captions().list(part="snippet", videoId=video_id).execute()
        cap_items = cap_resp.get("items", [])
        if not cap_items:
            print("  No caption tracks found.")
        else:
            print(f"  {'Caption ID':<65} | {'Lang':<5} | {'Name':<20} | {'Status'}")
            print(f"  {'-' * 65}-+-{'-' * 5}-+-{'-' * 20}-+-{'-' * 10}")
            for cap in cap_items:
                sn = cap["snippet"]
                status_str = "Draft" if sn.get("isDraft") else "Public"
                print(f"  {cap['id']:<65} | {sn.get('language'):<5} | {sn.get('name'):<20} | {status_str}")
        print("=" * 80 + "\n")
        
    except HttpError as e:
        print(f"❌ YouTube API Error fetching video info: {e}")

def delete_existing_caption(yt, video_id, language_code):
    """Delete standard standard caption track for a language code if it exists."""
    try:
        resp = yt.captions().list(part="snippet", videoId=video_id).execute()
        items = resp.get("items", [])
        for item in items:
            sn = item["snippet"]
            if sn.get("language") == language_code and sn.get("trackKind") == "standard":
                print(f"  Found existing standard caption track for '{language_code}' (ID: {item['id']}). Deleting...")
                yt.captions().delete(id=item['id']).execute()
                print(f"  Deleted existing caption track: {item['id']}")
                return True
    except HttpError as e:
        print(f"  [WARNING] Error deleting caption: {e}")
    return False

def upload_caption(yt, video_id, file_path, language_code, name):
    """Upload caption file to YouTube."""
    print(f"  Uploading subtitle file {file_path} for '{language_code}'...")
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
    print(f"  ✅ Subtitle uploaded successfully for {language_code}!")
    return response

def list_playlists(yt):
    """List available playlists on the channel."""
    print("INFO: Fetching channel playlists...")
    try:
        resp = yt.playlists().list(
            part="snippet",
            mine=True,
            maxResults=50
        ).execute()
        
        items = resp.get("items", [])
        if not items:
            print("No playlists found on this channel.")
            return []
            
        print("\n" + "=" * 80)
        print(f"{'Playlist ID':<35} | {'Title'}")
        print("=" * 80)
        for item in items:
            print(f"{item['id']:<35} | {item['snippet']['title']}")
        print("=" * 80 + "\n")
        return items
    except HttpError as e:
        print(f"❌ YouTube API Error listing playlists: {e}")
        return []

def add_video_to_playlist(yt, video_id, playlist_id):
    """Insert video into a playlist."""
    print(f"INFO: Inserting video {video_id} into playlist {playlist_id}...")
    try:
        yt.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        ).execute()
        print("✅ Video added to playlist successfully!")
    except HttpError as e:
        print(f"❌ YouTube API Error adding to playlist: {e}")

# ---------------------------------------------------------------------------
# REUSABLE PIPELINES
# ---------------------------------------------------------------------------
def run_localization_pipeline(yt, video_id, srt_path, source_lang, target_langs, execute=False):
    """Translate metadata and subtitles and update YouTube."""
    print("\n" + "=" * 80)
    print(f"RUNNING TRANSLATION & LOCALIZATION PIPELINE")
    print(f"Video ID:        {video_id}")
    print(f"Source SRT:      {srt_path}")
    print(f"Source Lang:     {source_lang}")
    print(f"Target Langs:    {', '.join(target_langs)}")
    print(f"Mode:            {'LIVE EXECUTE' if execute else 'DRY RUN (Preview)'}")
    print("=" * 80)
    
    # 1. Check SRT file
    if not Path(srt_path).exists():
        print(f"❌ ERROR: Subtitle file not found at: {srt_path}")
        return
        
    print(f"Parsing source subtitles from: {srt_path}...")
    blocks = parse_srt(srt_path)
    print(f"Parsed {len(blocks)} subtitle blocks.")
    
    # 2. Fetch video metadata
    try:
        vid_resp = yt.videos().list(part="snippet,localizations", id=video_id).execute()
        video = vid_resp["items"][0]
        snippet = video["snippet"]
        localizations = video.get("localizations", {})
    except HttpError as e:
        print(f"❌ ERROR: Failed to retrieve video: {e}")
        return
        
    fr_title = snippet.get("title", "")
    fr_desc = snippet.get("description", "")
    
    if not snippet.get("defaultLanguage"):
        snippet["defaultLanguage"] = source_lang

    # 3. Translate and apply for each target language
    for lang in target_langs:
        lang_name = DEFAULT_LANGUAGES.get(lang, lang.upper())
        print(f"\n➡️ Processing: {lang_name} ({lang})")
        
        # Translate subtitles
        print(f"  Translating subtitles...")
        temp_srt = BASE_DIR / f"subtitles_{lang}_temp.srt"
        lang_blocks = translate_blocks(blocks, source_lang, lang)
        write_srt(lang_blocks, temp_srt)
        print(f"  Saved temporary subtitles to: {temp_srt}")
        
        # Translate metadata
        print(f"  Translating metadata...")
        title = translate_text(fr_title, source_lang, lang)
        desc = translate_text(fr_desc, source_lang, lang)
        
        # Append medical disclaimer warning
        disclaimer = get_disclaimer(lang)
        if disclaimer and disclaimer not in desc:
            desc = desc.strip() + "\n\n" + disclaimer
            
        print(f"  Translated title: '{title}'")
        
        localizations[lang] = {
            "title": title,
            "description": desc
        }
        
        # Action execution
        if execute:
            delete_existing_caption(yt, video_id, lang)
            upload_caption(yt, video_id, temp_srt, lang, lang_name)
        else:
            print(f"  [DRY RUN] Would delete existing caption track and upload {temp_srt} on YouTube.")
            
        # Clean temp file
        try:
            temp_srt.unlink()
        except OSError:
            pass
            
    # Apply localizations
    if execute:
        print("\nUpdating localizations on YouTube...")
        update_body = {
            "id": video_id,
            "snippet": snippet,
            "localizations": localizations
        }
        yt.videos().update(
            part="snippet,localizations",
            body=update_body
        ).execute()
        print("✅ Localized titles and descriptions updated successfully on YouTube!")
    else:
        print("\n[DRY RUN] Would update localized metadata on YouTube.")
        
    print("\n🎉 Localization Pipeline Finished!")

def run_corrections_pipeline(yt, video_id, target_langs, find_str, replace_str, srt_path=None, execute=False):
    """Perform bulk corrections on translated subtitles and update YouTube."""
    print("\n" + "=" * 80)
    print(f"RUNNING SUBTITLES SEARCH & REPLACE CORRECTIONS")
    print(f"Video ID:     {video_id}")
    print(f"Languages:    {', '.join(target_langs)}")
    print(f"Search Query: '{find_str}'")
    print(f"Replacement:  '{replace_str}'")
    print(f"Mode:         {'LIVE EXECUTE' if execute else 'DRY RUN (Preview)'}")
    print("=" * 80)
    
    # Check source file or download
    if not srt_path or not Path(srt_path).exists():
        print("❌ ERROR: A valid local source SRT subtitle file must be provided to re-translate and correct.")
        return
        
    blocks = parse_srt(srt_path)
    print(f"Parsed {len(blocks)} subtitle blocks from source file.")
    
    for lang in target_langs:
        lang_name = DEFAULT_LANGUAGES.get(lang, lang.upper())
        print(f"\n➡️ Correcting subtitles for: {lang_name} ({lang})")
        
        # Translate subtitles
        print(f"  Translating subtitles...")
        temp_srt = BASE_DIR / f"subtitles_{lang}_temp.srt"
        lang_blocks = translate_blocks(blocks, "fr", lang)
        
        # Apply corrections
        corrected_count = 0
        for block in lang_blocks:
            if find_str in block["text"]:
                block["text"] = block["text"].replace(find_str, replace_str)
                corrected_count += 1
                
        print(f"  Applied {corrected_count} search & replace corrections.")
        write_srt(lang_blocks, temp_srt)
        print(f"  Saved temporary corrected subtitles to: {temp_srt}")
        
        if execute:
            delete_existing_caption(yt, video_id, lang)
            upload_caption(yt, video_id, temp_srt, lang, lang_name)
        else:
            print(f"  [DRY RUN] Would delete existing caption track and upload corrected subtitle file on YouTube.")
            
        try:
            temp_srt.unlink()
        except OSError:
            pass
            
    print("\n🎉 Corrections Pipeline Finished!")

# ---------------------------------------------------------------------------
# MAIN ENTRYPOINT
# ---------------------------------------------------------------------------
def main():
    setup_encoding()
    
    parser = argparse.ArgumentParser(
        description="YouTube Subtitle & Video Metadata Automator - localized management tool."
    )
    parser.add_argument(
        "--action", 
        required=True, 
        choices=["list", "info", "localize", "correct", "playlists"],
        help="Action to perform: list, info, localize, correct, or playlists."
    )
    parser.add_argument("--video", help="YouTube Video ID to target.")
    parser.add_argument("--srt", help="Path to source SRT subtitle file.")
    parser.add_argument("--source-lang", default="fr", help="Source language code (default: fr).")
    parser.add_argument(
        "--target-langs", 
        help="Comma-separated list of target language codes (e.g. en,ar,tr)."
    )
    parser.add_argument("--find", help="Search term/string for corrections.")
    parser.add_argument("--replace", help="Replacement string for corrections.")
    parser.add_argument("--playlist", help="Playlist ID to insert the video into.")
    parser.add_argument(
        "--execute", 
        action="store_true", 
        help="Execute the live changes. Default is dry-run mode."
    )
    
    args = parser.parse_args()
    
    # 1. Parse target languages
    if args.target_langs:
        langs = [l.strip() for l in args.target_langs.split(",") if l.strip()]
    else:
        # Default excludes source_lang if localizing
        langs = [l for l in DEFAULT_LANGUAGES.keys() if l != args.source_lang]
        
    # 2. Authenticate
    yt = authenticate()
    
    # 3. Dispatch Action
    if args.action == "list":
        list_recent_videos(yt)
        
    elif args.action == "info":
        if not args.video:
            print("❌ ERROR: --video ID must be provided for info action.")
            sys.exit(1)
        print_video_info(yt, args.video)
        
    elif args.action == "playlists":
        list_playlists(yt)
        if args.video and args.playlist:
            if args.execute:
                add_video_to_playlist(yt, args.video, args.playlist)
            else:
                print(f"[DRY RUN] Would insert video {args.video} into playlist {args.playlist}.")
                
    elif args.action == "localize":
        if not args.video or not args.srt:
            print("❌ ERROR: --video ID and --srt file path must be provided for localize action.")
            sys.exit(1)
        run_localization_pipeline(
            yt=yt,
            video_id=args.video,
            srt_path=args.srt,
            source_lang=args.source_lang,
            target_langs=langs,
            execute=args.execute
        )
        
    elif args.action == "correct":
        if not args.video or not args.find or not args.replace:
            print("❌ ERROR: --video ID, --find string, and --replace string must be provided for correct action.")
            sys.exit(1)
        run_corrections_pipeline(
            yt=yt,
            video_id=args.video,
            target_langs=langs,
            find_str=args.find,
            replace_str=args.replace,
            srt_path=args.srt,
            execute=args.execute
        )

if __name__ == "__main__":
    main()
