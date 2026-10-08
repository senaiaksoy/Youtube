import sys
import argparse
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from deep_translator import GoogleTranslator

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

BASE = Path(__file__).resolve().parent
TOKEN = BASE / "token.json"
VIDEO_ID = "ibyu5gWtfQY"

LANGUAGES = {
    "en": "English",
    "ar": "Arabic",
    "de": "German",
    "sq": "Albanian",
    "az": "Azerbaijani",
    "bg": "Bulgarian",
    "bs": "Bosnian",
    "mk": "Macedonian",
    "sr": "Serbian",
    "ru": "Russian",
    "uk": "Ukrainian",
    "fa": "Persian",
    "ro": "Romanian",
    "it": "Italian",
    "es": "Spanish",
    "tr": "Turkish"
}

# Pre-translated high-quality overrides for English and Arabic
EN_DESCRIPTION = """DHEA and growth hormone are often proposed to patients undergoing IVF, especially in cases of low ovarian reserve or poor ovarian response. But what do the studies really say?

In this video, Dr. Senai Aksoy explains what is proven, what is not, why these treatments remain off-label in many contexts, and how to avoid confusing hope, marketing, and evidence-based medicine.

Topics covered:
- DHEA before IVF
- Growth hormone and ovarian response
- Quality of available evidence
- Cost, lost time, and difficult decisions
- How to make an informed choice with your doctor

This video does not replace a personalized medical consultation. Each situation must be evaluated individually.

#IVF #DHEA #Fertility #ART #DrSenaiAksoy

For more information:  
📱 WhatsApp: +90 507 380 28 05  
🌐 Website: www.draksoyivf.com

⚕️ IMPORTANT MEDICAL DISCLAIMER

The information presented in this video is provided for educational and informational purposes only. Under no circumstances does it constitute medical advice, diagnosis, or a personalized treatment recommendation.

Each medical situation is unique. The topics discussed here do not replace a consultation with a qualified doctor, gynecologist, or reproductive medicine specialist.

Never modify your current medical treatment, start a new treatment, or make any medical decisions based on the information contained in this video without first consulting your treating doctor or specialist.

If you have questions regarding your reproductive health or IVF management, please consult a qualified healthcare professional.

© Assoc. Prof. Dr. Senai Aksoy — All rights reserved."""

AR_DESCRIPTION = """غالباً ما تُقترح DHEA وهرمون النمو للمريضات اللواتي يخضعن لعمليات التلقيح الاصطناعي (FIV)، خاصة في حالات ضعف مخزون المبيض أو الاستجابة غير الكافية للمبيض. ولكن ماذا تقول الدراسات حقاً؟

في هذا الفيديو، يشرح الدكتور سيناي أكسوي ما تم إثباته وما لم يتم إثباته، ولماذا تظل هذه العلاجات غير مرخصة في العديد من السياقات، وكيفية تجنب الخلط بين الأمل والتسويق والطب القائم على الأدلة.

النقاط التي تمت مناقشتها:
- DHEA قبل التلقيح الاصطناعي (FIV)
- هرمون النمو واستجابة المبيض
- جودة الأدلة المتاحة
- التكلفة والوقت الضائع والقرارات الصعبة
- كيف تتخذين قراراً مستنيراً مع طبيبكِ

هذا الفيديو لا يغني عن الاستشارة الطبية الشخصية. يجب تقييم كل حالة على حدة.

#التلقيح_الاصطناعي #DHEA #الخصوبة #PMA #الدكتور_سيناي_أكسوي

لمزيد من المعلومات:
📱 واتساب: 05 28 380 507 90+
🌐 الموقع الإلكتروني: www.draksoyivf.com

⚕️ تحذير طبي هام

المعلومات الواردة في هذا الفيديو هي لأغراض تعليمية وإعلامية فقط. ولا تشكل بأي حال من الأحوال نصيحة طبية أو تشخيصاً أو توصية بعلاج شخصي.

كل حالة طبية فريدة من نوعها. المواضيع التي تمت مناقشتها هنا لا تغني عن استشارة طبيب مؤهل، أو أخصائي أمراض نساء وتوليد، أو أخصائي في طب الإنجاب.

لا تقومي أبداً بتعديل علاجك الطبي الحالي، ولا تبدأي علاجاً جديداً، ولا تتخذي أي قرار طبي بناءً على المعلومات الواردة في هذا الفيديو دون استشارة طبيبك المعالج أو الأخصائي أولاً.

إذا كان لديك أي أسئلة تتعلق بصحتك الإنجابية أو بروتوكول التلقيح الاصطناعي الخاص بك، يرجى استشارة أخصائي رعاية صحية مؤهل.

© أ. د. سيناي أكسوي — جميع الحقوق محفوظة."""

OVERRIDES = {
    "en": {
        "title": "DHEA and Growth Hormone in IVF: Evidence, Limits, and Real Risks",
        "description": EN_DESCRIPTION
    },
    "ar": {
        "title": "DHEA وهرمون النمو في التلقيح الاصطناعي: الأدلة والحدود والمخاطر الحقيقية",
        "description": AR_DESCRIPTION
    }
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

def translate_text(text, target_lang):
    if not text:
        return ""
    try:
        translator = GoogleTranslator(source="fr", target=target_lang)
        # Use translate which handles up to 5000 chars
        return translator.translate(text)
    except Exception as e:
        print(f"  [ERROR] Failed to translate metadata to {target_lang}: {e}")
        return text

def get_service():
    if not TOKEN.exists():
        print(f"ERROR: Token file not found at {TOKEN}")
        sys.exit(1)
    creds = Credentials.from_authorized_user_file(str(TOKEN), [
        "https://www.googleapis.com/auth/youtube",
        "https://www.googleapis.com/auth/youtube.force-ssl"
    ])
    return build("youtube", "v3", credentials=creds)

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
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Apply changes live to YouTube")
    args = parser.parse_args()
    dry_run = not args.apply
    
    print("=" * 60)
    print("  YouTube Multi-Language Translation & Localization Automator")
    print("=" * 60)
    print(f"Mode: {'DRY RUN (Preview)' if dry_run else 'LIVE (Apply)'}")
    print(f"Video ID: {VIDEO_ID}")
    print("=" * 60)

    # 1. Parse French subtitles
    fr_srt_path = BASE / "subtitles_fr.srt"
    if not fr_srt_path.exists():
        print(f"ERROR: French subtitle file not found at {fr_srt_path}")
        sys.exit(1)
        
    print(f"Parsing French subtitles from: {fr_srt_path}")
    blocks = parse_srt(fr_srt_path)
    print(f"Found {len(blocks)} subtitle blocks.")

    # 2. Process translations for each language
    yt = None
    if not dry_run:
        print("\nConnecting to YouTube API...")
        yt = get_service()

        # Fetch default metadata (French)
        print("Fetching French video metadata to use as translation source...")
        vid_resp = yt.videos().list(part="snippet,localizations", id=VIDEO_ID).execute()
        video = vid_resp["items"][0]
        snippet = video["snippet"]
        localizations = video.get("localizations", {})
        
        fr_title = snippet.get("title", "")
        fr_desc = snippet.get("description", "")
        
        if not snippet.get("defaultLanguage"):
            snippet["defaultLanguage"] = "fr"
    else:
        # Dry-run placeholder
        fr_title = "DHEA et hormone de croissance en FIV : preuves, limites et vrais risques"
        fr_desc = "DHEA et hormone de croissance sont souvent proposées..."
        localizations = {}

    for lang, lang_name in LANGUAGES.items():
        print(f"\nProcessing language: {lang_name} ({lang})...")
        
        # Translate subtitles
        print(f"  Translating subtitles for {lang_name}...")
        srt_path = BASE / f"subtitles_{lang}.srt"
        
        # Avoid re-translating if the file already exists locally to save API requests and time
        if srt_path.exists():
            print(f"  [INFO] Local subtitle file subtitles_{lang}.srt already exists. Skipping translation step.")
        else:
            lang_blocks = translate_blocks(blocks, "fr", lang)
            write_srt(lang_blocks, srt_path)
            print(f"  Saved subtitles to {srt_path}")

        # Translate metadata
        print(f"  Translating metadata for {lang_name}...")
        if lang in OVERRIDES:
            title = OVERRIDES[lang]["title"]
            desc = OVERRIDES[lang]["description"]
            print("  [INFO] Using manual override for title/description.")
        else:
            title = translate_text(fr_title, lang)
            desc = translate_text(fr_desc, lang)
            print(f"  [SUCCESS] Translated title: '{title}'")
            
        localizations[lang] = {
            "title": title,
            "description": desc
        }
        
        # Apply subtitles live
        if not dry_run:
            print(f"  Applying {lang_name} subtitles to YouTube...")
            delete_existing_caption(yt, VIDEO_ID, lang)
            upload_caption(yt, VIDEO_ID, srt_path, lang, lang_name)

    # 3. Apply Localizations live
    if not dry_run:
        print("\nApplying Title and Description localizations for all languages on YouTube...")
        update_body = {
            "id": VIDEO_ID,
            "snippet": snippet,
            "localizations": localizations
        }
        yt.videos().update(
            part="snippet,localizations",
            body=update_body
        ).execute()
        print("✅ All video localizations updated successfully!")
        print("\n🎉 Multi-language Localization and Translation Completed Successfully!")
    else:
        print("\n🔍 [Dry Run] Subtitles generated locally. No updates were made on YouTube.")
        print("  - To apply changes, run:")
        print(f"    python {__file__} --apply")
        
    print("=" * 60)

if __name__ == "__main__":
    main()
