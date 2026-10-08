"""Add EN + AR localizations and captions for video IahtBeIzkyo (FR source)."""
from __future__ import annotations

import sys
import time
from pathlib import Path

from deep_translator import GoogleTranslator
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

BASE = Path(__file__).resolve().parent
TOKEN = BASE / "token.senaiaksoy.20260510-193158.json"
VIDEO_ID = "IahtBeIzkyo"
FR_SRT = BASE / "IahtBeIzkyo-fr.srt"
EXPECTED_CHANNEL = "UC51eCoXFnN1DiBd1dWcJpPQ"
SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",
]

EN_TITLE = "IVF supplements: science or marketing? What is actually proven"

EN_DESCRIPTION = """CoQ10, DHEA, melatonin, NAC, growth hormone, ovarian PRP… In fertility care, “miracle” products and add-ons are everywhere. But which ones are actually backed by solid scientific evidence?

In this video, I explain simply:

✅ What an IVF “add-on” really is
✅ Why a promising lab result does not always mean more live births
✅ What scientific recommendations say — especially ESHRE
✅ The differences between CoQ10, DHEA, growth hormone, PRP and stem cells
✅ The three questions to ask before paying for a supplement or extra treatment

An individual testimonial can be sincere without being scientific proof. Before buying, always ask whether serious clinical trials exist, whether the benefit is about live births, and what international consensus says.

📌 Find my detailed videos on CoQ10 and DHEA in the description and pinned comment.

🌐 Articles and resources: https://www.draksoyivf.com/fr/

And you — which supplement or treatment were you offered during your ART journey? Share your experience in the comments.

For more information:
📱 WhatsApp: +90 507 380 28 05
🌐 Website: www.draksoyivf.com

⚕️ IMPORTANT MEDICAL DISCLAIMER

The information in this video is provided for educational and informational purposes only. It does not constitute medical advice, diagnosis, or a personalized treatment recommendation.

Every medical situation is unique. This content does not replace a consultation with a qualified doctor, gynecologist, or reproductive medicine specialist.

Never change your current treatment, start a new treatment, or make medical decisions based on this video without first consulting your treating physician or specialist.

If you have questions about your reproductive health or IVF care, please consult a qualified healthcare professional.

© Assoc. Prof. Dr. Senai Aksoy — All rights reserved."""

AR_TITLE = "مكملات التلقيح الاصطناعي: علم أم تسويق؟ ما المُثبت حقًا"

AR_DESCRIPTION = """CoQ10، DHEA، الميلاتونين، NAC، هرمون النمو، PRP المبيضي… في مجال الخصوبة، المنتجات والعلاجات التي تُقدَّم كـ«معجزات» موجودة في كل مكان. لكن أيّها يستند فعلًا إلى أدلة علمية؟

في هذا الفيديو أشرح ببساطة:

✅ ما المقصود بـ«الإضافة» (add-on) في التلقيح الاصطناعي
✅ لماذا لا تعني نتيجة مخبرية واعدة بالضرورة مزيدًا من الولادات الحية
✅ ماذا تقول التوصيات العلمية، لا سيما توصيات ESHRE
✅ الفروق بين CoQ10 وDHEA وهرمون النمو وPRP والخلايا الجذعية
✅ الأسئلة الثلاثة التي يجب طرحها قبل دفع ثمن مكمل أو علاج إضافي

قد تكون الشهادة الفردية صادقة دون أن تشكّل دليلًا علميًا. قبل الشراء، اسألي دائمًا إن وُجدت تجارب سريرية جادّة، وهل الفائدة تتعلق فعلًا بالولادات الحية، وماذا تقول التوافقات الدولية.

📌 ستجدين فيديوهاتي التفصيلية عن CoQ10 وDHEA في الوصف والتعليق المثبت.

🌐 مقالات ومعلومات: https://www.draksoyivf.com/fr/

وأنتِ، أي مكمل أو علاج عُرض عليكِ خلال مسار المساعدة على الإنجاب؟ شاركي تجربتك في التعليقات.

لمزيد من المعلومات:
📱 واتساب: +90 507 380 28 05
🌐 الموقع: www.draksoyivf.com

⚕️ تحذير طبي هام

المعلومات الواردة في هذا الفيديو لأغراض تعليمية وإعلامية فقط. وهي لا تشكّل بأي حال نصيحة طبية أو تشخيصًا أو توصية بعلاج شخصي.

كل حالة طبية فريدة. المحتوى هنا لا يغني عن استشارة طبيب مؤهل أو أخصائي نساء أو طب الإنجاب.

لا تعدّلي علاجك الحالي، ولا تبدئي علاجًا جديدًا، ولا تتخذي أي قرار طبي بناءً على هذا الفيديو دون استشارة طبيبك المعالج أولًا.

إذا كانت لديك أسئلة حول صحتك الإنجابية أو مسار التلقيح الاصطناعي، يُرجى استشارة مختص رعاية صحية مؤهل.

© أ. د. سيناي أكسوي — جميع الحقوق محفوظة."""

# Extra EN discoverability tags only (YouTube tag budget ~500 chars total;
# Arabic tags often rejected / blow the budget — put Arabic keywords in description instead)
EN_TAGS = [
    "IVF supplements",
    "fertility supplements",
    "IVF add-ons",
    "CoQ10 fertility",
    "DHEA IVF",
    "evidence-based fertility",
]


def parse_srt(file_path: Path) -> list[dict]:
    blocks: list[dict] = []
    current: dict = {}
    text_lines: list[str] = []
    state = 0
    with file_path.open("r", encoding="utf-8-sig") as f:
        for line in f:
            line_str = line.strip()
            if state == 0:
                if not line_str:
                    continue
                current["id"] = line_str
                state = 1
            elif state == 1:
                current["time"] = line_str
                state = 2
                text_lines = []
            elif state == 2:
                if line_str == "":
                    current["text"] = "\n".join(text_lines)
                    blocks.append(current)
                    current = {}
                    state = 0
                else:
                    text_lines.append(line_str)
    if current:
        current["text"] = "\n".join(text_lines)
        blocks.append(current)
    return blocks


def write_srt(blocks: list[dict], file_path: Path) -> None:
    with file_path.open("w", encoding="utf-8") as f:
        for block in blocks:
            f.write(f"{block['id']}\n{block['time']}\n{block['text']}\n\n")


def translate_blocks(blocks: list[dict], target_lang: str) -> list[dict]:
    translator = GoogleTranslator(source="fr", target=target_lang)
    texts = [b["text"] for b in blocks]
    translated: list[str] = []
    batch_size = 40
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        n = i // batch_size + 1
        total = (len(texts) - 1) // batch_size + 1
        print(f"  Translating captions {target_lang} batch {n}/{total}...")
        try:
            translated.extend(translator.translate_batch(batch))
        except Exception as e:
            print(f"  batch failed ({e}), falling back per line")
            for text in batch:
                try:
                    translated.append(translator.translate(text))
                    time.sleep(0.05)
                except Exception:
                    translated.append(text)
        time.sleep(0.2)
    out = []
    for block, text in zip(blocks, translated):
        out.append({"id": block["id"], "time": block["time"], "text": text or block["text"]})
    return out


def delete_existing_caption(yt, language_code: str) -> None:
    resp = yt.captions().list(part="snippet", videoId=VIDEO_ID).execute()
    for item in resp.get("items", []):
        sn = item["snippet"]
        if sn.get("language") == language_code and sn.get("trackKind") == "standard":
            print(f"  Deleting existing {language_code} caption {item['id']}...")
            yt.captions().delete(id=item["id"]).execute()


def upload_caption(yt, file_path: Path, language_code: str, name: str) -> None:
    media = MediaFileUpload(str(file_path), mimetype="*/*", resumable=True)
    yt.captions().insert(
        part="snippet",
        body={
            "snippet": {
                "videoId": VIDEO_ID,
                "language": language_code,
                "name": name,
                "isDraft": False,
            }
        },
        media_body=media,
    ).execute()
    print(f"  ✅ Caption uploaded: {language_code}")


def main() -> None:
    if not FR_SRT.exists():
        print(f"ERROR: missing {FR_SRT}")
        sys.exit(1)
    if not TOKEN.exists():
        print(f"ERROR: missing {TOKEN}")
        sys.exit(1)

    creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
    yt = build("youtube", "v3", credentials=creds)

    ch = yt.channels().list(part="snippet", mine=True).execute()["items"][0]
    print(f"INFO: channel {ch['id']} ({ch['snippet']['title']})")
    if ch["id"] != EXPECTED_CHANNEL:
        print("DUR: wrong channel")
        sys.exit(1)

    vid = yt.videos().list(part="snippet,localizations", id=VIDEO_ID).execute()["items"][0]
    snippet = vid["snippet"]
    localizations = vid.get("localizations") or {}

    # Keep FR localization mirror of default
    localizations["fr"] = {
        "title": snippet["title"],
        "description": snippet["description"],
    }
    localizations["en"] = {"title": EN_TITLE, "description": EN_DESCRIPTION}
    localizations["ar"] = {"title": AR_TITLE, "description": AR_DESCRIPTION}

    print("INFO: updating localizations (fr/en/ar)...")
    try:
        yt.videos().update(
            part="localizations",
            body={"id": VIDEO_ID, "localizations": localizations},
        ).execute()
        print("SUCCESS: localizations updated")
    except HttpError as e:
        print(f"ERROR updating localizations: {e}")
        sys.exit(1)

    # Optional: append a few EN tags without rewriting the full list if budget allows
    existing_tags = list(snippet.get("tags") or [])
    merged = list(dict.fromkeys(existing_tags + EN_TAGS))
    used = sum(len(t) for t in existing_tags) + max(0, len(existing_tags) - 1)
    extra: list[str] = []
    for t in EN_TAGS:
        if t in existing_tags:
            continue
        cost = len(t) + 1
        if used + cost > 480:
            break
        extra.append(t)
        used += cost
    if extra:
        print(f"INFO: trying to add EN tags: {extra}")
        try:
            yt.videos().update(
                part="snippet",
                body={
                    "id": VIDEO_ID,
                    "snippet": {
                        "title": snippet["title"],
                        "description": snippet["description"],
                        "categoryId": snippet.get("categoryId", "27"),
                        "tags": existing_tags + extra,
                        "defaultLanguage": "fr",
                        "defaultAudioLanguage": snippet.get("defaultAudioLanguage") or "fr",
                    },
                },
            ).execute()
            print("SUCCESS: EN tags added")
        except HttpError as e:
            print(f"WARNING: could not add EN tags ({e}); continuing")
    else:
        print("INFO: skipping tag changes (budget full / already present)")

    print("INFO: translating captions from FR...")
    blocks = parse_srt(FR_SRT)
    print(f"  FR cues: {len(blocks)}")

    en_blocks = translate_blocks(blocks, "en")
    ar_blocks = translate_blocks(blocks, "ar")
    en_path = BASE / "IahtBeIzkyo-en.srt"
    ar_path = BASE / "IahtBeIzkyo-ar.srt"
    write_srt(en_blocks, en_path)
    write_srt(ar_blocks, ar_path)
    print(f"  wrote {en_path.name}, {ar_path.name}")

    for lang, path, name in [
        ("en", en_path, "English"),
        ("ar", ar_path, "Arabic"),
    ]:
        try:
            delete_existing_caption(yt, lang)
            upload_caption(yt, path, lang, name)
        except HttpError as e:
            print(f"ERROR caption {lang}: {e}")
            sys.exit(1)

    print("DONE")
    print(f"Studio: https://studio.youtube.com/video/{VIDEO_ID}/translations")
    print(f"Watch:  https://www.youtube.com/watch?v={VIDEO_ID}")


if __name__ == "__main__":
    main()
