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

# Translations definitions
LOCALIZATIONS = {
    "bs": {
        "title": "IMSI, PICSI, MACS: Kako bolje odabrati spermatozoide?",
        "description": """IMSI, PICSI, MACS: Kako nauka odabire spermatozoide u IVF-u? Da li je to korisno za vas? Doc. dr Senai Aksoy sumira kliničke dokaze i indikacije u 2026. godini.

🎧 Ovaj sadržaj je takođe dostupan sa engleskim (EN) i arapskim (AR) sinhronizacijama i titlovima. (Aktivirajte audio traku/titlove u postavkama videa)
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
11:15 Kliničko mišljenje dr. Aksoya
12:45 Korisni izvori i reference

📚 Citirani naučni izvori:
- Cochrane Database of Systematic Reviews (2020) : Morphologically selected sperm injection for ICSI.
- The Lancet (2019) : Physiological alternative to ICSI (HABSelect trial).
- ESHRE Guidelines on Male Infertility.

ℹ️ O dr. Senai Aksoyu:
Doc. dr Senai Aksoy je specijalista ginekologije, akušerstva i IVF-a u Istanbulu, sa preko 30 godina kliničkog iskustva. Diplomirao je na Univerzitetu Paris René Descartes i vodi parove na njihovom putu ka roditeljstvu.

⚠️ Ovaj sadržaj je informativnog karaktera. Ne zamjenjuje individualnu medicinsku procjenu.

#spermatozoidi #IMSI #PICSI #MACS #IVF #potpomognutaoplodnja #muskinfertilitet #drsenaiaksoy"""
    },
    "it": {
        "title": "IMSI, PICSI, MACS: come scegliere al meglio gli spermatozoi?",
        "description": """IMSI, PICSI, MACS: in che modo la scienza seleziona gli spermatozoi nella FIVET? È utile per voi? Il Dr. Senai Aksoy fa il punto sulle prove cliniche e sulle indicazioni nel 2026.

🎧 Questo contenuto è disponibile anche con doppiaggio e sottotitoli in inglese (EN) e arabo (AR). (Attiva la traccia audio/sottotitoli nelle impostazioni del video)
🎧 Ce contenu est également disponible en doublage et sous-titres Anglais (EN) et Arabe (AR). (Activez la piste audio/sous-titres dans les paramètres de la vidéo)
🎧 This video is also available with English (EN) and Arabic (AR) dubbing and subtitles. (Enable audio track/subtitles in video settings)

📌 Articolo dettagliato e risorse:
👉 https://draksoyivf.com/fr/selection-spermatique-avancee?utm_source=youtube&utm_medium=description&utm_campaign=spermogramme-advanced

⏱ Sommario del video:
00:00 Introduzione
00:48 I limiti della ICSI classica
02:00 Differenze tecniche: IMSI, PICSI e MACS
05:15 Cosa dice la scienza? (Dati Cochrane e HABSelect)
08:45 Chi dovrebbe usare queste tecniche avanzate? (Indicazioni)
11:15 L'opinione clinica del Dr. Aksoy
12:45 Fonti e risorse utili

📚 Fonti scientifiche citate:
- Cochrane Database of Systematic Reviews (2020) : Morphologically selected sperm injection for ICSI.
- The Lancet (2019) : Physiological alternative to ICSI (HABSelect trial).
- ESHRE Guidelines on Male Infertility.

ℹ️ Informazioni sul Dr. Senai Aksoy:
Il Dr. Senai Aksoy è un ginecologo-ostetrico, specialista in fertilità e FIVET a Istanbul, con oltre 30 anni di esperienza clinica. Laureato presso l'Università Paris René Descartes, accompagna le coppie nel loro percorso genitoriale.

⚠️ Questo contenuto è puramente informativo. Non sostituisce una valutazione medica individuale.

#spermatozoi #IMSI #PICSI #MACS #FIVET #PMA #infertilitamaschile #drsenaiaksoy"""
    },
    "es": {
        "title": "IMSI, PICSI, MACS: ¿cómo elegir mejor los espermatozoides?",
        "description": """IMSI, PICSI, MACS: ¿cómo selecciona la ciencia los espermatozoides en la FIV? ¿Es útil para usted? El Dr. Senai Aksoy repasa las pruebas clínicas y las indicaciones en 2026.

🎧 Este contenido también está disponible con doblaje y subtítulos en inglés (EN) y árabe (AR). (Active la pista de audio/subtítulos en la configuración del video)
🎧 Ce contenu est également disponible en doublage et sous-titres Anglais (EN) et Arabe (AR). (Activez la piste audio/sous-titres dans les paramètres de la vidéo)
🎧 This video is also available with English (EN) and Arabic (AR) dubbing and subtitles. (Enable audio track/subtitles in video settings)

📌 Artículo detallado y recursos:
👉 https://draksoyivf.com/fr/selection-spermatique-avancee?utm_source=youtube&utm_medium=description&utm_campaign=spermogramme-advanced

⏱ Resumen del video:
00:00 Introducción
00:48 Los límites de la ICSI clásica
02:00 Diferencias técnicas: IMSI, PICSI y MACS
05:15 ¿Qué dice la ciencia? (Datos de Cochrane y HABSelect)
08:45 ¿Quién debería usar estas técnicas avanzadas? (Indicaciones)
11:15 La opinión clínica del Dr. Aksoy
12:45 Fuentes y recursos útiles

📚 Fuentes científicas citadas:
- Cochrane Database of Systematic Reviews (2020) : Morphologically selected sperm injection for ICSI.
- The Lancet (2019) : Physiological alternative to ICSI (HABSelect trial).
- ESHRE Guidelines on Male Infertility.

ℹ️ Acerca del Dr. Senai Aksoy:
El Dr. Senai Aksoy es ginecólogo obstetra, especialista en fertilidad y FIV en Estambul, con más de 30 años de experiencia clínica. Graduado de la Universidad París René Descartes, acompaña a las parejas en su proyecto parental.

⚠️ Este contenido es meramente informativo. No reemplaza una evaluación médica individual.

#espermatozoides #IMSI #PICSI #MACS #FIV #reproduccionasistida #infertilidadmasculina #drsenaiaksoy"""
    },
    "ro": {
        "title": "IMSI, PICSI, MACS: cum să alegem mai bine spermatozoizii?",
        "description": """IMSI, PICSI, MACS: cum selectează știința spermatozoizii în FIV? Este util pentru dumneavoastră? Dr. Senai Aksoy prezintă dovezile clinice și indicațiile în 2026.

🎧 Acest conținut este disponibil și cu dublare și subtitrări în engleză (EN) și arabă (AR). (Activați piesa audio/subtitrările în setările video)
🎧 Ce contenu est également disponible en doublage et sous-titres Anglais (EN) et Arabe (AR). (Activez la piste audio/sous-titres dans les paramètres de la vidéo)
🎧 This video is also available with English (EN) and Arabic (AR) dubbing and subtitles. (Enable audio track/subtitles in video settings)

📌 Articol detaliat și resurse:
👉 https://draksoyivf.com/fr/selection-spermatique-avancee?utm_source=youtube&utm_medium=description&utm_campaign=spermogramme-advanced

⏱ Rezumatul videoclipului:
00:00 Introducere
00:48 Limitele ICSI-ului clasic
02:00 Diferențe tehnice: IMSI, PICSI și MACS
05:15 Ce spune știința? (Date Cochrane și HABSelect)
08:45 Cine ar trebui să folosească aceste tehnici avansate? (Indicații)
11:15 Opinia clinică a Dr. Aksoy
12:45 Surse și resurse utile

📚 Surse științifice citate:
- Cochrane Database of Systematic Reviews (2020) : Morphologically selected sperm injection for ICSI.
- The Lancet (2019) : Physiological alternative to ICSI (HABSelect trial).
- ESHRE Guidelines on Male Infertility.

ℹ️ Despre Dr. Senai Aksoy:
Dr. Senai Aksoy este medic ginecolog-obstetrician, specialist în fertilitate și FIV în Istanbul, cu peste 30 de ani de experiență clinică. Absolvent al Universității Paris René Descartes, el însoțește cuplurile în proiectul lor parental.

⚠️ Acest conținut este pur informativ. Nu înlocuiește o evaluare medicală individuală.

#spermatozoizi #IMSI #PICSI #MACS #FIV #reproducereasistata #infertilitatemasculina #drsenaiaksoy"""
    },
    "az": {
        "title": "IMSI, PICSI, MACS: Sperm seçimi necə daha yaxşı aparılır?",
        "description": """IMSI, PICSI, MACS: IVF (Süni Mayalanma) müalicəsində elm spermləri necə seçir? Sizin üçün faydalıdır? Dos. Dr. Senai Aksoy 2026-cı ildəki ən son klinik sübutları və göstərişləri təqdim edir.

🎧 Bu məzmun həmçinin İngilis (EN) və Ərəb (AR) dillərində səsləndirmə və altyazı ilə mövcuddur. (Video parametrlərindən səs kanalını/altyazını aktiv edin)
🎧 Ce contenu est également disponible en doublage et sous-titres Anglais (EN) et Arabe (AR). (Activez la piste audio/sous-titres dans les paramètres de la vidéo)
🎧 This video is also available with English (EN) and Arabic (AR) dubbing and subtitles. (Enable audio track/subtitles in video settings)

📌 Ətraflı məqalə və mənbələr:
👉 https://draksoyivf.com/fr/selection-spermatique-avancee?utm_source=youtube&utm_medium=description&utm_campaign=spermogramme-advanced

⏱ Video məzmunu:
00:00 Giriş
00:48 Klasik ICSI-nin sərhədləri
02:00 Texniki fərqlər: IMSI, PICSI və MACS
05:15 Elm nə deyir? (Cochrane və HABSelect məlumatları)
08:45 Bu inkişaf etmiş texnikaları kimlər istifadə etməlidir? (Göstərişlər)
11:15 Dr. Aksoyun klinik fikri
12:45 Faydalı mənbələr və istinadlar

📚 İstinad edilən elmi mənbələr:
- Cochrane Database of Systematic Reviews (2020) : Morphologically selected sperm injection for ICSI.
- The Lancet (2019) : Physiological alternative to ICSI (HABSelect trial).
- ESHRE Guidelines on Male Infertility.

ℹ️ Dos. Dr. Senai Aksoy haqqında:
Dos. Dr. Senai Aksoy İstanbulda 30 ildən çox klinik təcrübəyə malik mama-ginekoloq və süni mayalanma (IVF) mütəxəssisidir. Paris René Descartes Universitetinin məzunudur və valideyn olmaq yolundakı cütlüklərə bələdçilik edir.

⚠️ Bu məzmun məlumat xarakterlidir. Fərdi tibbi qiymətləndirməni əvəz etmir.

#sperm #IMSI #PICSI #MACS #sunimayalanma #IVF #kisikişiliyi #drsenaiaksoy"""
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
    print("  YouTube Video Localization Tool (5 More Languages)")
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
