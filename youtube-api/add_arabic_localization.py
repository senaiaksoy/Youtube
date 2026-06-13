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

AR_TITLE = "IMSI, PICSI, MACS: كيف تختار الحيوانات المنوية بشكل أفضل؟"

AR_DESCRIPTION = """IMSI, PICSI, MACS : كيف يختار العلم الحيوانات المنوية في التلقيح الاصطناعي (FIV)؟ وهل هي مفيدة لكم؟ الدكتور سيناي أكسوي يستعرض الأدلة السريرية ودواعي الاستخدام في عام 2026.

🎧 هذا المحتوى متوفر أيضاً بالدبلجة والترجمة إلى اللغتين الإنجليزية والعربية. (قم بتفعيل المسار الصوتي/الترجمة في إعدادات الفيديو)
🎧 Ce contenu est également disponible en doublage et sous-titres Anglais (EN) et Arabe (AR). (Activez la piste audio/sous-titres dans les paramètres de la vidéo)
🎧 This video is also available with English (EN) and Arabic (AR) dubbing and subtitles. (Enable audio track/subtitles in video settings)

📌 المقال بالتفصيل والمصادر:
👉 https://draksoyivf.com/fr/selection-spermatique-avancee?utm_source=youtube&utm_medium=description&utm_campaign=spermogramme-advanced

⏱ الفهرس الزمني للفيديو:
00:00 مقدمة
00:48 حدود تقنية الحقن المجهري (ICSI) الكلاسيكية
02:00 الاختلافات التقنية: IMSI و PICSI و MACS
05:15 ماذا يقول العلم؟ (بيانات Cochrane و HABSelect)
08:45 من يجب أن يستخدم هذه التقنيات المتقدمة؟ (دواعي الاستخدام)
11:15 الرأي السريري للدكتور أكسوي
12:45 مصادر ومراجع مفيدة

📚 المصادر العلمية المذكورة:
- Cochrane Database of Systematic Reviews (2020) : Morphologically selected sperm injection for ICSI.
- The Lancet (2019) : Physiological alternative to ICSI (HABSelect trial).
- ESHRE Guidelines on Male Infertility.

ℹ️ نبذة عن الدكتور سيناي أكسوي:
الدكتور سيناي أكسوي هو أخصائي أمراض النساء والتوليد، وخبير في الخصوبة والتلقيح الاصطناعي (FIV) في إسطنبول، مع أكثر من 30 عاماً من الخبرة السريرية. وهو خريج جامعة باريس رينيه ديكارت، ويرافق الأزواج في رحلة الإنجاب.

⚠️ هذا المحتوى ذو طابع إرشادي ومعلوماتي فقط. ولا يغني عن التقييم الطبي الفردي من قبل طبيبك.

#سائل_منوي #حيوانات_منوية #IMSI #PICSI #MACS #تلقيح_اصطناعي #حقن_مجهري #العقم_عند_الرجال #دكتور_سيناي_أكسوي"""

def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Apply changes live to YouTube")
    args = parser.parse_args()
    dry_run = not args.apply

    print("=" * 60)
    print("  YouTube Video Localization Tool (Arabic)")
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
        vid_resp = yt.videos().list(part="snippet,localizations", id=VIDEO_ID).execute()
        items = vid_resp.get("items", [])
        if not items:
            print(f"❌ Video not found on YouTube: {VIDEO_ID}")
            sys.exit(1)
        video = items[0]
        snippet = video["snippet"]
        localizations = video.get("localizations", {})
        
        print(f"Current Default Language: {snippet.get('defaultLanguage')}")
        print(f"Current Title (Default): {snippet.get('title')}")
        print(f"Available Localizations: {list(localizations.keys())}")
    except HttpError as e:
        print(f"❌ API Error fetching video: {e}")
        sys.exit(1)

    # 2. Prepare localization changes
    localizations["ar"] = {
        "title": AR_TITLE,
        "description": AR_DESCRIPTION
    }

    # Make sure defaultLanguage is set to "fr" (the original language of the video)
    if not snippet.get("defaultLanguage"):
        snippet["defaultLanguage"] = "fr"

    print("\nProposed Arabic Title:")
    print(AR_TITLE)
    print("\nProposed Arabic Description Length:", len(AR_DESCRIPTION))

    if not dry_run:
        # Update video using videos().update
        try:
            update_body = {
                "id": VIDEO_ID,
                "snippet": snippet,
                "localizations": localizations
            }
            update_resp = yt.videos().update(
                part="snippet,localizations",
                body=update_body
            ).execute()
            print("✅ Video localizations updated successfully!")
            print(f"Updated Available Localizations: {list(update_resp.get('localizations', {}).keys())}")
        except HttpError as e:
            print(f"❌ API Error updating video localizations: {e}")
            sys.exit(1)
    else:
        print("\n🔍 [Dry Run] Video localization update skipped. Use --apply to execute.")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
