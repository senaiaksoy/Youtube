import argparse
import json
import sys
import time
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/youtube"]
BASE_DIR = Path(__file__).resolve().parent
TOKEN_FILE = BASE_DIR / "token.json"
CONFIG_FILE = BASE_DIR / "homepage-config-fr.json"


def youtube_client():
    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    return build("youtube", "v3", credentials=creds)


def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def list_playlists(youtube):
    items = []
    req = youtube.playlists().list(part="id,snippet,status", mine=True, maxResults=50)
    while req:
        resp = req.execute()
        items.extend(resp.get("items", []))
        req = youtube.playlists().list_next(req, resp)
    return items


def list_playlist_items(youtube, playlist_id):
    items = []
    req = youtube.playlistItems().list(
        part="id,contentDetails", playlistId=playlist_id, maxResults=50
    )
    while req:
        resp = req.execute()
        for item in resp.get("items", []):
            items.append(
                {
                    "id": item["id"],
                    "video_id": item["contentDetails"]["videoId"],
                }
            )
        req = youtube.playlistItems().list_next(req, resp)
    return items


def find_playlist(existing, title, aliases):
    candidates = [title, *aliases]
    for candidate in candidates:
        for item in existing:
            if item["snippet"].get("title", "").strip() == candidate.strip():
                return item
    return None


def same_order(current_items, desired_video_ids):
    return [item["video_id"] for item in current_items] == desired_video_ids


def update_playlist_metadata(youtube, playlist, definition):
    youtube.playlists().update(
        part="snippet,status",
        body={
            "id": playlist["id"],
            "snippet": {
                "title": definition["title"],
                "description": definition["description"],
                "defaultLanguage": "fr",
            },
            "status": {
                "privacyStatus": definition.get("privacyStatus", "public"),
            },
        },
    ).execute()


def create_playlist(youtube, definition):
    created = (
        youtube.playlists()
        .insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": definition["title"],
                    "description": definition["description"],
                    "defaultLanguage": "fr",
                },
                "status": {
                    "privacyStatus": definition.get("privacyStatus", "public"),
                },
            },
        )
        .execute()
    )
    return created


def clear_playlist(youtube, current_items):
    for item in current_items:
        youtube.playlistItems().delete(id=item["id"]).execute()
        time.sleep(0.15)


def add_videos(youtube, playlist_id, video_ids):
    for video_id in video_ids:
        youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id,
                    },
                }
            },
        ).execute()
        time.sleep(0.15)


def sync_playlists(youtube, config, dry_run):
    existing = list_playlists(youtube)
    results = []

    for definition in config["playlists"]:
        found = find_playlist(existing, definition["title"], definition.get("matchTitles", []))
        desired_ids = definition["videoIds"]

        if not found:
            if dry_run:
                results.append(
                    {
                        "title": definition["title"],
                        "status": "would_create",
                        "playlist_id": None,
                        "videos": len(desired_ids),
                    }
                )
                continue
            found = create_playlist(youtube, definition)
            existing.append(found)
            add_videos(youtube, found["id"], desired_ids)
            results.append(
                {
                    "title": definition["title"],
                    "status": "created",
                    "playlist_id": found["id"],
                    "videos": len(desired_ids),
                }
            )
            continue

        current_items = list_playlist_items(youtube, found["id"])
        needs_metadata = (
            found["snippet"].get("title") != definition["title"]
            or found["snippet"].get("description", "") != definition["description"]
            or found.get("status", {}).get("privacyStatus") != definition.get("privacyStatus", "public")
        )
        needs_videos = not same_order(current_items, desired_ids)
        status = "unchanged"
        if needs_metadata or needs_videos:
            status = "would_update" if dry_run else "updated"

        if not dry_run and (needs_metadata or needs_videos):
            if needs_metadata:
                update_playlist_metadata(youtube, found, definition)
            if needs_videos:
                clear_playlist(youtube, current_items)
                add_videos(youtube, found["id"], desired_ids)

        results.append(
            {
                "title": definition["title"],
                "status": status,
                "playlist_id": found["id"],
                "videos": len(desired_ids),
                "metadata": needs_metadata,
                "video_order": needs_videos,
            }
        )

    return results


def list_sections(youtube):
    try:
        resp = youtube.channelSections().list(
            part="id,snippet,contentDetails", mine=True
        ).execute()
        return resp.get("items", [])
    except HttpError as error:
        print(f"Section list error: {error}", file=sys.stderr)
        return []


def replace_sections(youtube, config, playlist_results, dry_run):
    title_to_id = {
        result["title"]: result["playlist_id"]
        for result in playlist_results
        if result.get("playlist_id")
    }
    desired = [
        {"title": title, "playlist_id": title_to_id.get(title)}
        for title in config["homepageOrder"]
    ]
    missing = [item["title"] for item in desired if not item["playlist_id"]]
    if missing:
        return {"status": "error", "missing": missing}

    existing_sections = list_sections(youtube)

    if dry_run:
        return {
            "status": "would_replace",
            "delete_count": len(existing_sections),
            "create": desired,
        }

    deleted = []
    for section in existing_sections:
        youtube.channelSections().delete(id=section["id"]).execute()
        deleted.append(section["id"])
        time.sleep(0.25)

    created = []
    for index, item in enumerate(desired):
        section = (
            youtube.channelSections()
            .insert(
                part="snippet,contentDetails",
                body={
                    "snippet": {
                        "type": "singlePlaylist",
                        "position": index,
                    },
                    "contentDetails": {
                        "playlists": [item["playlist_id"]],
                    },
                },
            )
            .execute()
        )
        created.append({"title": item["title"], "section_id": section.get("id")})
        time.sleep(0.25)

    return {"status": "replaced", "deleted": deleted, "created": created}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Apply changes to YouTube")
    args = parser.parse_args()
    dry_run = not args.apply

    config = load_config()
    youtube = youtube_client()
    print("=" * 64)
    print("YouTube Homepage Sync - FR channel")
    print("=" * 64)
    print("Mode:", "DRY RUN" if dry_run else "LIVE")

    playlist_results = sync_playlists(youtube, config, dry_run)
    print("\nPlaylists:")
    for result in playlist_results:
        print(
            f"  [{result['status']}] {result['title']} "
            f"({result.get('videos', 0)} videos)"
        )
        if result.get("playlist_id"):
            print(f"     ID: {result['playlist_id']}")
        if "metadata" in result:
            print(
                f"     metadata={result['metadata']} video_order={result['video_order']}"
            )

    section_result = replace_sections(youtube, config, playlist_results, dry_run)
    print("\nHomepage sections:")
    print(json.dumps(section_result, ensure_ascii=False, indent=2))
    print("=" * 64)


if __name__ == "__main__":
    main()
