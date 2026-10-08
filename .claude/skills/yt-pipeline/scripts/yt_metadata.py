# -*- coding: utf-8 -*-
"""Video metadata read and dry-run/apply update helpers."""

from __future__ import annotations

import argparse
import sys

from googleapiclient.errors import HttpError

from yt_common import backup_json, get_service, read_json, write_json


def get_video(yt, video_id: str) -> dict:
    items = yt.videos().list(part="snippet,status,localizations,statistics", id=video_id).execute().get("items", [])
    if not items:
        sys.stderr.write(f"ERROR: video not found: {video_id}\n")
        sys.exit(1)
    return items[0]


def cmd_get(yt, video_id: str, out: str | None) -> None:
    video = get_video(yt, video_id)
    sn = video["snippet"]
    loc = video.get("localizations", {})
    print(f"{video_id}  {sn.get('title')}")
    print(f"defaultLanguage={sn.get('defaultLanguage')} localizations={','.join(sorted(loc))}")
    print(f"descriptionLength={len(sn.get('description', ''))} tags={len(sn.get('tags', []))}")
    if out:
        print(f"wrote: {write_json(out, video)}")


def apply_fix(snippet: dict, localizations: dict, status: dict, fix: dict) -> tuple[dict, dict, dict, list[str]]:
    new_sn = dict(snippet)
    new_loc = dict(localizations)
    new_st = dict(status)
    changes: list[str] = []

    for field in ("title", "description", "tags", "categoryId", "defaultLanguage"):
        if field in fix and fix[field] is not None and fix[field] != snippet.get(field):
            new_sn[field] = fix[field]
            changes.append(field)

    if "localizations" in fix and fix["localizations"] is not None:
        for lang, payload in fix["localizations"].items():
            if payload != new_loc.get(lang):
                new_loc[lang] = payload
                changes.append(f"localizations.{lang}")

    if "status" in fix and fix["status"] is not None:
        for field in ("privacyStatus", "publishAt"):
            if field in fix["status"] and fix["status"][field] != status.get(field):
                new_st[field] = fix["status"][field]
                changes.append(f"status.{field}")

    return new_sn, new_loc, new_st, changes


def cmd_update(yt, fixes_path: str, go: bool) -> None:
    fixes = read_json(fixes_path)
    if isinstance(fixes, dict):
        fixes = [fixes]

    originals = []
    for fix in fixes:
        video_id = fix["video_id"]
        video = get_video(yt, video_id)
        snippet = video["snippet"]
        localizations = video.get("localizations", {})
        status = video.get("status", {})
        originals.append({"video_id": video_id, "snippet": snippet, "localizations": localizations, "status": status})
        new_sn, new_loc, new_st, changes = apply_fix(snippet, localizations, status, fix)

        if not changes:
            print(f"no-change: {video_id}  {snippet.get('title')}")
            continue

        print(f"{'apply' if go else 'dry-run'}: {video_id}  {snippet.get('title')}")
        for change in changes:
            print(f"  change: {change}")

        if go:
            body = {"id": video_id, "snippet": new_sn, "localizations": new_loc}
            body["snippet"].setdefault("categoryId", snippet.get("categoryId", "27"))
            parts = ["snippet", "localizations"]
            if any(c.startswith("status.") for c in changes):
                parts.append("status")
                body["status"] = new_st
            yt.videos().update(part=",".join(parts), body=body).execute()
            print("  updated")

    if go and originals:
        print(f"backup: {backup_json('meta', originals)}")
    if not go:
        print("dry-run only. Re-run with --go after explicit user approval.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--channel", required=True, choices=["fr", "tr"])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("get")
    p.add_argument("--video", required=True)
    p.add_argument("--out")
    p = sub.add_parser("update")
    p.add_argument("--fixes", required=True)
    p.add_argument("--go", action="store_true")
    args = ap.parse_args()

    yt = get_service(args.channel)
    try:
        if args.cmd == "get":
            cmd_get(yt, args.video, args.out)
        elif args.cmd == "update":
            cmd_update(yt, args.fixes, args.go)
    except HttpError as exc:
        sys.stderr.write(f"API ERROR: {exc}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
