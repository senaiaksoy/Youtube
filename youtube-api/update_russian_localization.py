import json
import sys
import argparse
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

BASE = Path(__file__).resolve().parent
TOKEN = BASE / "token.json"

VIDEO_ID = "pqc9UgCIqo0"

RU_TITLE = "IMSI, PICSI, MACS: как лучше выбирать сперматозоиды?"
RU_DESCRIPTION = """IMSI, PICSI, MACS: как наука выбирает сперматозоиды при ЭКО? Полезно ли это для вас? Доц. д-р Сенаи Аксой резюмирует клинические данные и показания в 2026 году.

🎧 Этот контент также доступен с английским (EN) и арабским (AR) дубляжом и субтитрами. (Активируйте аудиодорожку/субтитры в настройках видео)
🎧 Ce contenu est également disponible en doublage et sous-titres Anglais (EN) et Arabe (AR). (Activez la piste audio/sous-titres dans les paramètres de la vidéo)
🎧 This video is also available with English (EN) and Arabic (AR) dubbing and subtitles. (Enable audio track/subtitles in video settings)

📌 Подробная статья и ресурсы:
👉 https://draksoyivf.com/fr/selection-spermatique-avancee?utm_source=youtube&utm_medium=description&utm_campaign=spermogramme-advanced

⏱ Содержание видео:
00:00 Введение
00:48 Ограничения классического ИКСИ
02:00 Технические различия: IMSI, PICSI и MACS
05:15 Что говорит наука? (Данные Cochrane и HABSelect)
08:45 Кому следует использовать эти передовые методы? (Показания)
11:15 Клиническое мнение доктора Аксоя
12:45 Полезные источники и ресурсы

📚 Цитируемые научные источники:
- Cochrane Database of Systematic Reviews (2020) : Morphologically selected sperm injection for ICSI.
- The Lancet (2019) : Physiological alternative to ICSI (HABSelect trial).
- ESHRE Guidelines on Male Infertility.

ℹ️ О докторе Сенаи Аксое:
Доцент, д-р Сенаи Аксой — акушер-гинеколог, специалист по лечению бесплодия и ЭКО в Стамбуле с более чем 30-летним клиническим опытом. Выпускник Университета Париж Декарт, он помогает франкоязычным парам на пути к родительству.

⚠️ Этот контент носит исключительно информационный характер. Он не заменяет индивидуальную медицинскую консультацию.

#сперматозоиды #IMSI #PICSI #MACS #ЭКО #ВРТ #мужскоебесплодие #drsenaiaksoy"""

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
    print("  YouTube Video Localization Tool (Russian)")
    print("=" * 60)
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print(f"Video ID: {VIDEO_ID}")

    if not TOKEN.exists():
        print(f"ERROR: Token file not found at {TOKEN}")
        sys.exit(1)

    creds = Credentials.from_authorized_user_file(str(TOKEN), ["https://www.googleapis.com/auth/youtube"])
    yt = build("youtube", "v3", credentials=creds)
    print("✅ Authenticated successfully.")

    # 1. Fetch current video details
    try:
        vid_resp = yt.videos().list(part="snippet,localizations", id=VIDEO_ID).execute()
        items = vid_resp.get("items", [])
        if not items:
            print(f"❌ Video not found: {VIDEO_ID}")
            sys.exit(1)
        video = items[0]
        snippet = video["snippet"]
        localizations = video.get("localizations", {})
        
        print(f"Current Default Language: {snippet.get('defaultLanguage')}")
        print(f"Available Localizations: {list(localizations.keys())}")
    except HttpError as e:
        print(f"❌ API Error: {e}")
        sys.exit(1)

    # 2. Add localization
    localizations["ru"] = {
        "title": RU_TITLE,
        "description": RU_DESCRIPTION
    }

    if not snippet.get("defaultLanguage"):
        snippet["defaultLanguage"] = "fr"

    print(f"\nAdding Russian Title: {RU_TITLE}")

    if not dry_run:
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
            print(f"❌ API Error: {e}")
            sys.exit(1)
    else:
        print("\n🔍 [Dry Run] Localization update skipped. Use --apply to execute.")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
