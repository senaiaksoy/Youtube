"""Re-apply title/description localizations in batches (captions already done)."""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from deep_translator import GoogleTranslator
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

sys.stdout.reconfigure(encoding="utf-8")

BASE = Path(__file__).resolve().parent
TOKEN = BASE / "token.senaiaksoy.20260510-193158.json"
VIDEO_ID = "IahtBeIzkyo"
CACHE = BASE / "IahtBeIzkyo_localizations_cache.json"
SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",
]

LANGS = [
    "tr", "de", "sq", "az", "bg", "es", "ro", "ru",
    "it", "bs", "uk", "mk", "sr", "fa", "en", "ar",
]


def translate_long(text: str, target: str) -> str:
    translator = GoogleTranslator(source="fr", target=target)
    parts = text.split("\n\n")
    out: list[str] = []
    buf = ""
    for p in parts:
        candidate = (buf + "\n\n" + p).strip() if buf else p
        if len(candidate) > 4000 and buf:
            out.append(translator.translate(buf))
            time.sleep(0.12)
            buf = p
        else:
            buf = candidate
    if buf:
        out.append(translator.translate(buf))
        time.sleep(0.12)
    return "\n\n".join(out)


def main() -> None:
    creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
    yt = build("youtube", "v3", credentials=creds)

    vid = yt.videos().list(part="snippet,localizations", id=VIDEO_ID).execute()["items"][0]
    existing = vid.get("localizations") or {}
    fr_title = vid["snippet"]["title"]
    fr_desc = vid["snippet"]["description"]
    print("NOW:", sorted(existing.keys()))
    print("FR title:", fr_title)
    print("FR desc len:", len(fr_desc))

    if CACHE.exists():
        meta = json.loads(CACHE.read_text(encoding="utf-8"))
        print(f"Loaded cache with {len(meta)} langs")
    else:
        meta = {}

    for lang in LANGS:
        if lang in meta and meta[lang].get("title") and meta[lang].get("description"):
            print(f"  cache hit {lang}")
            continue
        if (
            lang in ("en", "ar")
            and lang in existing
            and existing[lang].get("title")
            and existing[lang].get("description")
        ):
            meta[lang] = existing[lang]
            print(f"  reuse live {lang}")
            continue
        print(f"  translating {lang}...")
        title = GoogleTranslator(source="fr", target=lang).translate(fr_title)
        time.sleep(0.12)
        desc = translate_long(fr_desc, lang)
        meta[lang] = {"title": title, "description": desc}
        print(f"  {lang}: {title}")
        CACHE.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    CACHE.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    locs = {"fr": {"title": fr_title, "description": fr_desc}}
    # Keep any existing good entries
    for k, v in existing.items():
        if v.get("title") and v.get("description"):
            locs[k] = v

    batches = [LANGS[i : i + 3] for i in range(0, len(LANGS), 3)]
    for batch in batches:
        for lang in batch:
            locs[lang] = meta[lang]
        if "en" in locs:
            locs["en-US"] = locs["en"]
        print("\nUpdate batch", batch, "→ keys", sorted(locs.keys()))
        try:
            yt.videos().update(
                part="localizations",
                body={"id": VIDEO_ID, "localizations": locs},
            ).execute()
            check = yt.videos().list(part="localizations", id=VIDEO_ID).execute()["items"][0]
            got = check.get("localizations") or {}
            print("  after:", sorted(got.keys()))
            locs = got
            missing = [x for x in batch if x not in got]
            if missing:
                print("  MISSING after batch:", missing)
                for lang in missing:
                    try:
                        one = dict(locs)
                        one[lang] = meta[lang]
                        yt.videos().update(
                            part="localizations",
                            body={"id": VIDEO_ID, "localizations": one},
                        ).execute()
                        check = yt.videos().list(part="localizations", id=VIDEO_ID).execute()["items"][0]
                        locs = check.get("localizations") or one
                        print(f"  single {lang}:", sorted(locs.keys()))
                    except HttpError as e:
                        print(f"  FAIL {lang}: {e}")
        except HttpError as e:
            print("  BATCH ERROR:", e)
            for lang in batch:
                try:
                    one = dict(locs)
                    one[lang] = meta[lang]
                    yt.videos().update(
                        part="localizations",
                        body={"id": VIDEO_ID, "localizations": one},
                    ).execute()
                    check = yt.videos().list(part="localizations", id=VIDEO_ID).execute()["items"][0]
                    locs = check.get("localizations") or one
                    print(f"  single {lang}:", sorted(locs.keys()))
                except HttpError as e2:
                    print(f"  FAIL {lang}: {e2}")

    final = yt.videos().list(part="localizations", id=VIDEO_ID).execute()["items"][0]
    final_locs = final.get("localizations") or {}
    print("\nFINAL:", sorted(final_locs.keys()))
    for k in sorted(final_locs.keys()):
        title = final_locs[k].get("title", "")
        print(f"  {k}: {title[:90]}")


if __name__ == "__main__":
    main()
