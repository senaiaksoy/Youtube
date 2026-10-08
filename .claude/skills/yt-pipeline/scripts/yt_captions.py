# -*- coding: utf-8 -*-
"""Caption track list, download, upload, replace, delete, and offline translate."""

from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

from yt_common import get_service, parse_srt, write_json, write_srt


def cmd_list(yt, video_id: str, out: str | None) -> None:
    resp = yt.captions().list(part="snippet", videoId=video_id).execute()
    items = resp.get("items", [])
    rows = []
    for item in items:
        sn = item["snippet"]
        row = {
            "id": item["id"],
            "language": sn.get("language"),
            "name": sn.get("name"),
            "trackKind": sn.get("trackKind"),
            "status": sn.get("status"),
            "isDraft": sn.get("isDraft"),
        }
        rows.append(row)
        print(f"{row['id']}  lang={row['language']} name={row['name']!r} status={row['status']}")
    if out:
        print(f"wrote: {write_json(out, rows)}")


def cmd_download(yt, caption_id: str, out: str) -> None:
    req = yt.captions().download(id=caption_id, tfmt="srt")
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, req)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_bytes(fh.getvalue())
    print(f"downloaded: {caption_id} -> {out}")


def cmd_upload(yt, video_id: str, file: str, lang: str, name: str, go: bool) -> None:
    if not Path(file).exists():
        sys.stderr.write(f"ERROR: file not found: {file}\n")
        sys.exit(2)
    if not go:
        print(f"dry-run: would upload {file} to video={video_id} lang={lang} name={name!r}")
        return
    media = MediaFileUpload(file, mimetype="*/*", resumable=True)
    resp = yt.captions().insert(
        part="snippet",
        body={"snippet": {"videoId": video_id, "language": lang, "name": name, "isDraft": False}},
        media_body=media,
    ).execute()
    print(f"uploaded caption: {resp['id']} lang={lang}")


def cmd_replace(yt, caption_id: str, file: str, go: bool) -> None:
    if not Path(file).exists():
        sys.stderr.write(f"ERROR: file not found: {file}\n")
        sys.exit(2)
    if not go:
        print(f"dry-run: would replace caption={caption_id} with {file}")
        return
    media = MediaFileUpload(file, mimetype="*/*", resumable=True)
    yt.captions().update(part="id", body={"id": caption_id}, media_body=media).execute()
    print(f"replaced caption: {caption_id}")


def cmd_delete(yt, caption_id: str, go: bool) -> None:
    if not go:
        print(f"dry-run: would delete caption={caption_id}")
        return
    yt.captions().delete(id=caption_id).execute()
    print(f"deleted caption: {caption_id}")


def cmd_translate(file: str, src: str, targets: str, out_dir: str) -> None:
    try:
        from deep_translator import GoogleTranslator
    except ImportError:
        sys.stderr.write("ERROR: deep-translator missing. Run: py -3.12 -m pip install deep-translator\n")
        sys.exit(2)

    blocks = parse_srt(file)
    out_root = Path(out_dir)
    out_root.mkdir(parents=True, exist_ok=True)
    stem = Path(file).stem

    for target in [t.strip() for t in targets.split(",") if t.strip()]:
        translator = GoogleTranslator(source=src, target=target)
        translated = []
        for block in blocks:
            text = block["text"]
            translated.append({**block, "text": translator.translate(text) if text.strip() else text})
        path = write_srt(translated, out_root / f"{stem}.{target}.srt")
        print(f"translated {src}->{target}: {path}")
    print("review required before publishing generated subtitle text")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--channel", choices=["fr", "tr"], help="Required for YouTube API commands; unused for translate.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("list")
    p.add_argument("--video", required=True)
    p.add_argument("--out")
    p = sub.add_parser("download")
    p.add_argument("--caption-id", required=True)
    p.add_argument("--out", required=True)
    p = sub.add_parser("upload")
    p.add_argument("--video", required=True)
    p.add_argument("--file", required=True)
    p.add_argument("--lang", required=True)
    p.add_argument("--name", default="")
    p.add_argument("--go", action="store_true")
    p = sub.add_parser("replace")
    p.add_argument("--caption-id", required=True)
    p.add_argument("--file", required=True)
    p.add_argument("--go", action="store_true")
    p = sub.add_parser("delete")
    p.add_argument("--caption-id", required=True)
    p.add_argument("--go", action="store_true")
    p = sub.add_parser("translate")
    p.add_argument("--file", required=True)
    p.add_argument("--src", required=True)
    p.add_argument("--targets", required=True)
    p.add_argument("--out-dir", default=".")
    args = ap.parse_args()

    if args.cmd == "translate":
        cmd_translate(args.file, args.src, args.targets, args.out_dir)
        return

    if not args.channel:
        sys.stderr.write("ERROR: --channel is required for YouTube API commands.\n")
        sys.exit(2)

    yt = get_service(args.channel)
    try:
        if args.cmd == "list":
            cmd_list(yt, args.video, args.out)
        elif args.cmd == "download":
            cmd_download(yt, args.caption_id, args.out)
        elif args.cmd == "upload":
            cmd_upload(yt, args.video, args.file, args.lang, args.name, args.go)
        elif args.cmd == "replace":
            cmd_replace(yt, args.caption_id, args.file, args.go)
        elif args.cmd == "delete":
            cmd_delete(yt, args.caption_id, args.go)
    except HttpError as exc:
        sys.stderr.write(f"API ERROR: {exc}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
