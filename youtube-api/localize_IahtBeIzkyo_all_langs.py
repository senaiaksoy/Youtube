"""Translate IahtBeIzkyo to all channel languages: title, description, captions.

Skips FR (source). Reuses existing EN/AR SRTs if present.
Does NOT rewrite snippet.tags (YouTube rejects invalid tag updates on this video).
"""
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

# Standard channel language pack (+ Persian, used on this channel)
LANGUAGES = {
    "en": "English",
    "ar": "Arabic",
    "tr": "Turkish",
    "de": "German",
    "sq": "Albanian",
    "az": "Azerbaijani",
    "bg": "Bulgarian",
    "es": "Spanish",
    "ro": "Romanian",
    "ru": "Russian",
    "it": "Italian",
    "bs": "Bosnian",
    "uk": "Ukrainian",
    "mk": "Macedonian",
    "sr": "Serbian",
    "fa": "Persian",
}

# High-quality overrides already prepared
OVERRIDES = {
    "en": {
        "title": "IVF supplements: science or marketing? What is actually proven",
        "description": None,  # filled below if file exists / keep previous
    },
    "ar": {
        "title": "مكملات التلقيح الاصطناعي: علم أم تسويق؟ ما المُثبت حقًا",
        "description": None,
    },
}


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


def chunked_translate(texts: list[str], target: str, label: str) -> list[str]:
    translator = GoogleTranslator(source="fr", target=target)
    out: list[str] = []
    batch_size = 35
    total = (len(texts) - 1) // batch_size + 1
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        n = i // batch_size + 1
        print(f"    {label} {target} batch {n}/{total}...")
        try:
            out.extend(translator.translate_batch(batch))
        except Exception as e:
            print(f"    batch fail ({e}), per-line fallback")
            for t in batch:
                try:
                    out.append(translator.translate(t))
                    time.sleep(0.04)
                except Exception:
                    out.append(t)
        time.sleep(0.25)
    return out


def translate_blocks(blocks: list[dict], target: str) -> list[dict]:
    texts = [b["text"] for b in blocks]
    translated = chunked_translate(texts, target, "captions")
    return [
        {"id": b["id"], "time": b["time"], "text": tr or b["text"]}
        for b, tr in zip(blocks, translated)
    ]


def translate_long_text(text: str, target: str) -> str:
    """Translate long description in chunks under Google translate limits."""
    if not text:
        return ""
    translator = GoogleTranslator(source="fr", target=target)
    # Split by paragraphs to stay under 4500 chars
    parts = text.split("\n\n")
    out_parts: list[str] = []
    buf = ""
    for p in parts:
        candidate = (buf + "\n\n" + p).strip() if buf else p
        if len(candidate) > 4000 and buf:
            out_parts.append(translator.translate(buf))
            time.sleep(0.15)
            buf = p
        else:
            buf = candidate
    if buf:
        out_parts.append(translator.translate(buf))
        time.sleep(0.15)
    return "\n\n".join(out_parts)


def delete_existing_caption(yt, language_code: str) -> None:
    resp = yt.captions().list(part="snippet", videoId=VIDEO_ID).execute()
    for item in resp.get("items", []):
        sn = item["snippet"]
        if sn.get("language") == language_code and sn.get("trackKind") == "standard":
            print(f"    delete existing {language_code} caption")
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
    print(f"    ✅ caption {language_code}")


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
    print(f"Kanal: {ch['snippet']['title']} ({ch['id']})")
    if ch["id"] != EXPECTED_CHANNEL:
        print("DUR: wrong channel")
        sys.exit(1)

    vid = yt.videos().list(part="snippet,localizations", id=VIDEO_ID).execute()["items"][0]
    snippet = vid["snippet"]
    localizations = vid.get("localizations") or {}
    fr_title = snippet["title"]
    fr_desc = snippet["description"]

    # Keep FR mirror
    localizations["fr"] = {"title": fr_title, "description": fr_desc}

    # Pull existing EN/AR descriptions if present
    if "en" in localizations:
        OVERRIDES["en"]["description"] = localizations["en"].get("description")
        OVERRIDES["en"]["title"] = localizations["en"].get("title") or OVERRIDES["en"]["title"]
    if "ar" in localizations:
        OVERRIDES["ar"]["description"] = localizations["ar"].get("description")
        OVERRIDES["ar"]["title"] = localizations["ar"].get("title") or OVERRIDES["ar"]["title"]

    blocks = parse_srt(FR_SRT)
    print(f"FR cues: {len(blocks)}")
    print(f"Languages: {', '.join(LANGUAGES)}")

    for lang, name in LANGUAGES.items():
        print(f"\n=== {name} ({lang}) ===")
        srt_path = BASE / f"IahtBeIzkyo-{lang}.srt"

        # Captions
        if srt_path.exists() and srt_path.stat().st_size > 500:
            print(f"  reuse existing {srt_path.name}")
        else:
            print("  translating captions...")
            lang_blocks = translate_blocks(blocks, lang)
            write_srt(lang_blocks, srt_path)
            print(f"  saved {srt_path.name}")

        # Metadata
        if lang in OVERRIDES and OVERRIDES[lang].get("title") and OVERRIDES[lang].get("description"):
            title = OVERRIDES[lang]["title"]
            desc = OVERRIDES[lang]["description"]
            print("  metadata: override")
        else:
            print("  translating metadata...")
            title = GoogleTranslator(source="fr", target=lang).translate(fr_title)
            time.sleep(0.1)
            desc = translate_long_text(fr_desc, lang)
            print(f"  title: {title}")

        localizations[lang] = {"title": title, "description": desc}
        # Mirror English to en-US for clients that prefer region codes
        if lang == "en":
            localizations["en-US"] = {"title": title, "description": desc}

        # Upload caption
        try:
            delete_existing_caption(yt, lang)
            upload_caption(yt, srt_path, lang, name)
        except HttpError as e:
            print(f"  ERROR caption: {e}")
            # continue other languages

    print("\n=== Applying all localizations ===")
    try:
        yt.videos().update(
            part="localizations",
            body={"id": VIDEO_ID, "localizations": localizations},
        ).execute()
        print("SUCCESS: localizations updated")
    except HttpError as e:
        print(f"ERROR localizations: {e}")
        sys.exit(1)

    # Verify
    check = yt.videos().list(part="localizations", id=VIDEO_ID).execute()["items"][0]
    locs = list((check.get("localizations") or {}).keys())
    print("Localizations now:", sorted(locs))
    caps = yt.captions().list(part="snippet", videoId=VIDEO_ID).execute()
    std = sorted(
        {
            c["snippet"]["language"]
            for c in caps.get("items", [])
            if c["snippet"].get("trackKind") == "standard" and not c["snippet"].get("isDraft")
        }
    )
    print("Standard captions:", std)
    print(f"\nStudio: https://studio.youtube.com/video/{VIDEO_ID}/translations")


if __name__ == "__main__":
    main()
