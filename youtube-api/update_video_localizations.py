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

TR_TITLE = "IMSI, PICSI, MACS: Sperm Seçimi Nasıl Daha İyi Yapılır?"
TR_DESCRIPTION = """IMSI, PICSI, MACS: IVF (Tüp Bebek) tedavisinde bilim spermleri nasıl seçiyor? Sizin için faydalı mı? Doç. Dr. Senai Aksoy 2026 yılındaki güncel klinik kanıtları ve kullanım alanlarını özetliyor.

🎧 Bu içerik İngilizce (EN) ve Arapça (AR) seslendirme ve altyazı seçenekleriyle de sunulmaktadır. (Video ayarlarından ses kanalı/altyazıyı etkinleştirin)
🎧 Ce contenu est également disponible en doublage et sous-titres Anglais (EN) et Arabe (AR). (Activez la piste audio/sous-titres dans les paramètres de la vidéo)
🎧 This video is also available with English (EN) and Arabic (AR) dubbing and subtitles. (Enable audio track/subtitles in video settings)

📌 Detaylı makale ve kaynaklar:
👉 https://draksoyivf.com/fr/selection-spermatique-avancee?utm_source=youtube&utm_medium=description&utm_campaign=spermogramme-advanced

⏱ Video İçeriği:
00:00 Giriş
00:48 Klasik ICSI'nin Sınırları
02:00 Teknik Farklar: IMSI, PICSI ve MACS
05:15 Bilim Ne Diyor? (Cochrane & HABSelect Verileri)
08:45 Bu Gelişmiş Teknikleri Kimler Kullanmalı? (Endikasyonlar)
11:15 Dr. Aksoy'un Klinik Görüşü
12:45 Yararlı Kaynaklar ve Referanslar

📚 Atıfta Bulunulan Bilimsel Kaynaklar:
- Cochrane Database of Systematic Reviews (2020) : Morphologically selected sperm injection for ICSI.
- The Lancet (2019) : Physiological alternative to ICSI (HABSelect trial).
- ESHRE Guidelines on Male Infertility.

ℹ️ Doç. Dr. Senai Aksoy Hakkında:
Doç. Dr. Senai Aksoy, İstanbul'da 30 yılı aşkın klinik deneyime sahip, kadın hastalıkları, doğum ve tüp bebek (IVF) uzmanıdır. Paris René Descartes Üniversitesi mezunu olup, anne-baba olma yolculuğundaki çiftlere rehberlik etmektedir.

⚠️ Bu içerik bilgilendirme amaçlıdır. Bireysel tıbbi değerlendirmenin yerini alamaz.

#sperm #IMSI #PICSI #MACS #tüpbebek #IVF #erkekkısırlığı #drsenaiaksoy"""

SQ_TITLE = "IMSI, PICSI, MACS: Si të përzgjidhen më mirë spermatozoidet?"
SQ_DESCRIPTION = """IMSI, PICSI, MACS: Si i përzgjedh shkenca spermatozoidet në IVF? A është e dobishme për ju? Dr. Senai Aksoy përmbledh provat klinike dhe indikacionet në vitin 2026.

🎧 Ky përmbajtje është gjithashtu e disponueshme me dublim dhe titra në anglisht (EN) dhe arabisht (AR). (Aktivizoni gjurmët audio/titrat në cilësimet e videos)
🎧 Ce contenu est également disponible en doublage et sous-titres Anglais (EN) et Arabe (AR). (Activez la piste audio/sous-titres dans les paramètres de la vidéo)
🎧 This video is also available with English (EN) and Arabic (AR) dubbing and subtitles. (Enable audio track/subtitles in video settings)

📌 Artikulli i detajuar dhe burimet:
👉 https://draksoyivf.com/fr/selection-spermatique-avancee?utm_source=youtube&utm_medium=description&utm_campaign=spermogramme-advanced

⏱ Përmbledhja e videos:
00:00 Hyrje
00:48 Kufizimet e ICSI-së klasike
02:00 Ndryshimet teknike: IMSI, PICSI dhe MACS
05:15 Çfarë thotë shkenca? (Të dhënat Cochrane & HABSelect)
08:45 Kush duhet t'i përdorë këto teknika të avancuara? (Indikacionet)
11:15 Opinioni klinik i Dr. Aksoy
12:45 Burime dhe referenca të dobishme

📚 Burimet shkencore të cituara:
- Cochrane Database of Systematic Reviews (2020) : Morphologically selected sperm injection for ICSI.
- The Lancet (2019) : Physiological alternative to ICSI (HABSelect trial).
- ESHRE Guidelines on Male Infertility.

ℹ️ Rreth Dr. Senai Aksoy:
Dr. Senai Aksoy është gjinekolog-obstetër, specialist i fertilitetit dhe IVF-së në Stamboll, met mbi 30 vjet përvojë klinike. I diplomuar në Universitetin Paris René Descartes, ai ndihmon çiftet në rrugëtimin e tyre prindëror.

⚠️ Kjo përmbajtje është vetëm informative. Ajo nuk zëvendëson një vlerësim mjekësor individual.

#spermatozoidet #IMSI #PICSI #MACS #IVF #PMA #infertilitetimashkullor #drsenaiaksoy"""

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
    print("  YouTube Video Localization Tool (TR & SQ)")
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

    # 2. Add localizations
    localizations["tr"] = {
        "title": TR_TITLE,
        "description": TR_DESCRIPTION
    }
    localizations["sq"] = {
        "title": SQ_TITLE,
        "description": SQ_DESCRIPTION
    }

    if not snippet.get("defaultLanguage"):
        snippet["defaultLanguage"] = "fr"

    print(f"\nAdding Turkish Title: {TR_TITLE}")
    print(f"Adding Albanian Title: {SQ_TITLE}")

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
