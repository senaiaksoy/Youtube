# -*- coding: utf-8 -*-
"""Playlist list, item list, and idempotent add operations."""

from __future__ import annotations

import argparse
import sys

from googleapiclient.errors import HttpError

from yt_common import get_service, write_json


def cmd_list(yt, out: str | None) -> None:
    rows = []
    page = None
    while True:
        resp = yt.playlists().list(part="snippet,contentDetails", mine=True, maxResults=50, pageToken=page).execute()
        for item in resp.get("items", []):
            row = {
                "id": item["id"],
                "title": item["snippet"]["title"],
                "itemCount": item["contentDetails"]["itemCount"],
            }
            rows.append(row)
            print(f"{row['id']}  ({row['itemCount']})  {row['title']}")
        page = resp.get("nextPageToken")
        if not page:
            break
    if out:
        print(f"wrote: {write_json(out, rows)}")


def playlist_items(yt, playlist_id: str) -> list[dict]:
    rows = []
    page = None
    while True:
        resp = yt.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=page,
        ).execute()
        for item in resp.get("items", []):
            rows.append(
                {
                    "playlistItemId": item["id"],
                    "videoId": item["contentDetails"]["videoId"],
                    "title": item["snippet"]["title"],
                }
            )
        page = resp.get("nextPageToken")
        if not page:
            return rows


def cmd_items(yt, playlist_id: str, out: str | None) -> None:
    rows = playlist_items(yt, playlist_id)
    for row in rows:
        print(f"{row['videoId']}  {row['title']}")
    if out:
        print(f"wrote: {write_json(out, rows)}")


def cmd_add(yt, video_id: str, playlist_ids: str, go: bool) -> None:
    for playlist_id in [p.strip() for p in playlist_ids.split(",") if p.strip()]:
        existing = {row["videoId"] for row in playlist_items(yt, playlist_id)}
        if video_id in existing:
            print(f"already-present: {video_id} -> {playlist_id}")
            continue
        if not go:
            print(f"dry-run: would add {video_id} -> {playlist_id}")
            continue
        yt.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {"kind": "youtube#video", "videoId": video_id},
                }
            },
        ).execute()
        print(f"added: {video_id} -> {playlist_id}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--channel", required=True, choices=["fr", "tr"])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("list")
    p.add_argument("--out")
    p = sub.add_parser("items")
    p.add_argument("--playlist", required=True)
    p.add_argument("--out")
    p = sub.add_parser("add")
    p.add_argument("--video", required=True)
    p.add_argument("--playlists", required=True)
    p.add_argument("--go", action="store_true")
    args = ap.parse_args()

    yt = get_service(args.channel)
    try:
        if args.cmd == "list":
            cmd_list(yt, args.out)
        elif args.cmd == "items":
            cmd_items(yt, args.playlist, args.out)
        elif args.cmd == "add":
            cmd_add(yt, args.video, args.playlists, args.go)
    except HttpError as exc:
        sys.stderr.write(f"API ERROR: {exc}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
