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

LOCALIZATIONS = {
    "mk": {
        "title": "IMSI, PICSI, MACS: како подобро да се изберат сперматозоидите?",
        "description": """IMSI, PICSI, MACS: Како науката ги избира сперматозоидите при ин витро (IVF)? Дали е ова корисно за вас? Доц. д-р Сенаи Аксој ги сумира клиничките докази и индикации во 2026 година.

🎧 Оваа содржина е исто така достапна со синхронизација и титлови на англиски (EN) и арапски (AR). (Активирајте ја аудио лентата/титловите во поставките на видеото)
🎧 Ce contenu est également disponible en doublage et sous-titres Anglais (EN) et Arabe (AR). (Activez la piste audio/sous-titres dans les paramètres de la vidéo)
🎧 This video is also available with English (EN) and Arabic (AR) dubbing and subtitles. (Enable audio track/subtitles in video settings)

📌 Детален напис и ресурси:
👉 https://draksoyivf.com/fr/selection-spermatique-avancee?utm_source=youtube&utm_medium=description&utm_campaign=spermogramme-advanced

⏱ Содржина на видеото:
00:00 Вовед
00:48 Ограничувања на класичното ICSI
02:00 Технички разлики: IMSI, PICSI и MACS
05:15 Што вели науката? (Податоци од Cochrane и HABSelect)
08:45 Кој треба да ги користи овие напредни техники? (Индикации)
11:15 Клиничко мислење на д-р Аксој
12:45 Корисни извори и референци

📚 Цитирани научни извори:
- Cochrane Database of Systematic Reviews (2020) : Morphologically selected sperm injection for ICSI.
- The Lancet (2019) : Physiological alternative to ICSI (HABSelect trial).
- ESHRE Guidelines on Male Infertility.

ℹ️ За д-р Сенаи Аксој:
Доц. д-р Сенаи Аксој е специјалист по гинекологија, акушерство и ин витро (IVF) во Истанбул, со над 30 години клиничко искуство. Дипломирал на Универзитетот Paris René Descartes и ги води паровите на нивниот пат кон родителството.

⚠️ Оваа содржина е само од информативен карактер. Не ја заменува индивидуалната медицинска проценка.

#сперматозоиди #IMSI #PICSI #MACS #IVF #инвитро #машкобесплодие #drsenaiaksoy"""
    },
    "uk": {
        "title": "IMSI, PICSI, MACS: як краще вибирати сперматозоїди?",
        "description": """IMSI, PICSI, MACS: як наука вибирає сперматозоїди при ЕКО? Чи корисно це для вас? Доц. д-р Сенаї Аксой резюмує клінічні докази та показання у 2026 році.

🎧 Цей контент також доступний з англійським (EN) та арабським (AR) дубляжем і субтитрами. (Активуйте аудіодоріжку/субтитри в налаштуваннях відео)
🎧 Ce contenu est également disponible en doublage et sous-titres Anglais (EN) et Arabe (AR). (Activez la piste audio/sous-titres dans les paramètres de la vidéo)
🎧 This video is also available with English (EN) and Arabic (AR) dubbing and subtitles. (Enable audio track/subtitles in video settings)

📌 Детальна стаття та ресурси:
👉 https://draksoyivf.com/fr/selection-spermatique-avancee?utm_source=youtube&utm_medium=description&utm_campaign=spermogramme-advanced

⏱ Зміст відео:
00:00 Вступ
00:48 Обмеження класичного ICSI
02:00 Технічні відмінності: IMSI, PICSI та MACS
05:15 Що говорить наука? (Дані Cochrane та HABSelect)
08:45 Кому слід використовувати ці передові методи? (Показання)
11:15 Клінічна думка доктора Аксоя
12:45 Корисні джерела та посилання

📚 Цитовані наукові джерела:
- Cochrane Database of Systematic Reviews (2020) : Morphologically selected sperm injection for ICSI.
- The Lancet (2019) : Physiological alternative to ICSI (HABSelect trial).
- ESHRE Guidelines on Male Infertility.

ℹ️ Про доктора Сенаї Аксоя:
Доцент, д-р Сенаї Аксой — акушер-гінеколог, спеціаліст з лікування безпліддя та ЕКО в Стамбулі з понад 30-річним клінічним досвідом. Випускник Університету Париж Рене Декарт, він допомагає франкомовним парам на шляху до батьківства.

⚠️ Цей контент має виключно інформаційний характер. Він не замінює індивідуальну медичну консультацію.

#сперматозоїди #IMSI #PICSI #MACS #ЕКО #ДРТ #чоловічебезпліддя #drsenaiaksoy"""
    },
    "sr": {
        "title": "IMSI, PICSI, MACS: kako bolje odabrati spermatozoide?",
        "description": """IMSI, PICSI, MACS: Kako nauka bira spermatozoide u IVF-u? Da li je to korisno za vas? Doc. dr Senai Aksoj sumira kliničke dokaze i indikacije u 2026. godini.

🎧 Ovaj sadržaj je takođe dostupan sa engleskim (EN) i arapskim (AR) prevodom i titlovima. (Aktivirajte audio traku/titlove u podešavanjima videa)
🎧 Ce contenu est également disponible en doublage et sous-titres Anglais (EN) et Arabe (AR). (Activez la piste audio/sous-titres dans les paramètres de la vidéo)
🎧 This video is also available with English (EN) and Arabic (AR) dubbing and subtitles. (Enable audio track/subtitles in video settings)

📌 Detaljan članak i resursi:
👉 https://draksoyivf.com/fr/selection-spermatique-avancee?utm_source=youtube&utm_medium=description&utm_campaign=spermogramme-advanced

⏱ Sadržaj videa:
00:00 Uvod
00:48 Ograničenja klasičnog ICSI-ja
02:00 Tehničke razlike: IMSI, PICSI i MACS
05:15 Šta kaže nauka? (Cochrane i HABSelect podaci)
08:45 Ko bi trebao koristiti ove napredne tehnike? (Indikacije)
11:15 Kliničko mišljenje dr. Aksoja
12:45 Korisni izvori i reference

📚 Citirani naučni izvori:
- Cochrane Database of Systematic Reviews (2020) : Morphologically selected sperm injection for ICSI.
- The Lancet (2019) : Physiological alternative to ICSI (HABSelect trial).
- ESHRE Guidelines on Male Infertility.

ℹ️ O dr. Senai Aksoju:
Doc. dr Senai Aksoj je specijalista ginekologije, akušerstva i IVF-a u Istanbulu, sa preko 30 godina kliničkog iskustva. Diplomirao je na Univerzitetu Paris René Descartes i vodi parove na njihovom putu ka roditeljstvu.

⚠️ Ovaj sadržaj je informativnog karaktera. Ne zamenjuje individualnu medicinsku procenu.

#spermatozoidi #IMSI #PICSI #MACS #IVF #vto #muskiinfertilitet #drsenaiaksoy"""
    },
    "fa": {
        "title": "IMSI, PICSI, MACS: چگونه اسپرم‌ها را بهتر انتخاب کنیم؟",
        "description": """IMSI، PICSI، MACS: علم چگونه اسپرم‌ها را در لقاح مصنوعی (FIV) انتخاب می‌کند؟ آیا این برای شما مفید است؟ دکتر سنایی آکسوی شواهد بالینی و موارد مصرف را در سال 2026 بررسی می‌کند.

🎧 این محتوا همچنین با دوبله و زیرنویس انگلیسی (EN) و عربی (AR) در دسترس است. (باند صوتی/زیرنویس را در تنظیمات ویدیو فعال کنید)
🎧 Ce contenu est également disponible en doublage et sous-titres Anglais (EN) et Arabe (AR). (Activez la piste audio/sous-titres dans les paramètres de la vidéo)
🎧 This video is also available with English (EN) and Arabic (AR) dubbing and subtitles. (Enable audio track/subtitles in video settings)

📌 مقاله دقیق و منابع:
👉 https://draksoyivf.com/fr/selection-spermatique-avancee?utm_source=youtube&utm_medium=description&utm_campaign=spermogramme-advanced

⏱ خلاصه ویدیو:
00:00 مقدمه
00:48 محدودیت‌های روش ICSI کلاسیک
02:00 تفاوت‌های فنی: IMSI، PICSI و MACS
05:15 علم چه می‌گوید؟ (داده‌های Cochrane و HABSelect)
08:45 چه کسانی باید از این تکنیک‌های پیشرفته استفاده کنند؟ (موارد مصرف)
11:15 نظر بالینی دکتر آکسوی
12:45 منابع و مراجع مفید

📚 منابع علمی ذکر شده:
- Cochrane Database of Systematic Reviews (2020) : Morphologically selected sperm injection for ICSI.
- The Lancet (2019) : Physiological alternative to ICSI (HABSelect trial).
- ESHRE Guidelines on Male Infertility.

ℹ️ درباره دکتر سنایی آکسوی:
دکتر سنایی آکسوی متخصص زنان و زایمان، فلوشیپ نازایی و آی‌وی‌اف در استانبول با بیش از ۳۰ سال تجربه بالینی است. او فارغ‌التحصیل دانشگاه پاریس دکارت بوده و زوج‌ها را در مسیر بچه‌دار شدن همراهی می‌کند.

⚠️ این محتوا صرفاً جنبه اطلاع‌رسانی دارد و جایگزین ارزیابی پزشکی فردی نمی‌شود.

#اسپرم #IMSI #PICSI #MACS #ناباروری #آی_وی_اف #ناباروری_مردان #دکتر_سنایی_آکسوی"""
    }
}

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
    print("  YouTube Video Localization Tool (4 More Languages)")
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
    for lang, data in LOCALIZATIONS.items():
        localizations[lang] = data
        print(f"Adding {lang.upper()} Title: {data['title']}")

    if not snippet.get("defaultLanguage"):
        snippet["defaultLanguage"] = "fr"

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
