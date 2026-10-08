# -*- coding: utf-8 -*-
"""Shared YouTube API helpers for the yt-pipeline skill."""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from typing import Any


def configure_output() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


configure_output()

if sys.version_info[:2] != (3, 12):
    sys.stderr.write(
        "ERROR: use Python 3.12 for this pipeline. Run with: py -3.12 <script>.py\n"
    )
    sys.exit(2)

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
except ImportError:
    sys.stderr.write(
        "ERROR: Google API packages are missing for this interpreter.\n"
        "Run scripts with py -3.12. If needed:\n"
        "  py -3.12 -m pip install google-api-python-client google-auth-oauthlib\n"
    )
    sys.exit(2)


SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",
]

CHANNELS: dict[str, dict[str, str]] = {
    "fr": {
        "id": "UC51eCoXFnN1DiBd1dWcJpPQ",
        "handle": "@SenaiAksoy",
        "title_hint": "Dr. Senai Aksoy",
        "token": "token.senaiaksoy.20260510-193158.json",
    },
    "tr": {
        "id": "UCbO5qpAnmaQPBJlGMM9ITiw",
        "handle": "@DocentDrSenaiAksoy",
        "title_hint": "Docent Dr Senai Aksoy",
        "token": "token.json",
    },
}


def find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        if (parent / "youtube-api").is_dir() and (parent / "CLAUDE.md").exists():
            return parent
    env_root = os.environ.get("YT_REPO_ROOT")
    if env_root:
        return Path(env_root)
    sys.stderr.write("ERROR: could not find D:/A-klasor/Youtube repo root. Set YT_REPO_ROOT.\n")
    sys.exit(2)


def find_api_dir() -> Path:
    env = os.environ.get("YT_API_DIR")
    if env:
        api_dir = Path(env)
    else:
        api_dir = find_repo_root() / "youtube-api"
    if not api_dir.is_dir():
        sys.stderr.write(f"ERROR: youtube-api directory not found: {api_dir}\n")
        sys.exit(2)
    return api_dir


REPO_ROOT = find_repo_root()
API_DIR = find_api_dir()


def channel_config(channel_key: str) -> dict[str, str]:
    if channel_key not in CHANNELS:
        choices = ", ".join(sorted(CHANNELS))
        sys.stderr.write(f"ERROR: unknown channel '{channel_key}'. Choices: {choices}\n")
        sys.exit(2)
    return CHANNELS[channel_key]


def canonical_token_path(channel_key: str) -> Path:
    return API_DIR / channel_config(channel_key)["token"]


def read_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write_json(path: str | Path, data: Any) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return p


def backup_json(prefix: str, data: Any) -> Path:
    return write_json(API_DIR / f"backup_{prefix}_{int(time.time())}.json", data)


def load_credentials(channel_key: str) -> Credentials:
    token_file = canonical_token_path(channel_key)
    if not token_file.exists():
        ch = channel_config(channel_key)
        sys.stderr.write(
            f"ERROR: canonical token missing: {token_file}\n"
            f"Create it once with:\n"
            f"  py -3.12 {Path(__file__).with_name('yt_oauth.py')} --channel {channel_key}\n"
            f"Expected live channel: {ch['handle']} ({ch['id']})\n"
        )
        sys.exit(2)

    creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            token_file.write_text(creds.to_json(), encoding="utf-8")
        else:
            sys.stderr.write(
                f"ERROR: token cannot be refreshed: {token_file}\n"
                f"Recreate it with: py -3.12 {Path(__file__).with_name('yt_oauth.py')} --channel {channel_key}\n"
            )
            sys.exit(2)
    return creds


def build_youtube(creds: Credentials):
    return build("youtube", "v3", credentials=creds)


def verify_channel(yt, channel_key: str, quiet: bool = False) -> dict[str, Any]:
    expected = channel_config(channel_key)
    resp = yt.channels().list(part="snippet,statistics,contentDetails", mine=True).execute()
    items = resp.get("items", [])
    if not items:
        sys.stderr.write("ERROR: token has no accessible mine=True channel.\n")
        sys.exit(3)
    live = items[0]
    if live["id"] != expected["id"]:
        sys.stderr.write(
            "ERROR: LIVE CHANNEL MISMATCH. No operation was performed.\n"
            f"  token channel: {live['snippet'].get('title')} ({live['id']})\n"
            f"  expected     : {expected['handle']} ({expected['id']})\n"
        )
        sys.exit(3)
    if not quiet:
        print(f"verified channel: {expected['handle']} ({live['id']})")
    return live


def get_service(channel_key: str, quiet: bool = False):
    creds = load_credentials(channel_key)
    yt = build_youtube(creds)
    verify_channel(yt, channel_key, quiet=quiet)
    return yt


def parse_srt(path: str | Path) -> list[dict[str, str]]:
    blocks: list[dict[str, str]] = []
    current: dict[str, str] = {}
    text_lines: list[str] = []
    state = 0

    for raw in Path(path).read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if state == 0:
            if not line:
                continue
            current = {"id": line}
            state = 1
        elif state == 1:
            current["time"] = line
            text_lines = []
            state = 2
        else:
            if not line:
                current["text"] = "\n".join(text_lines)
                blocks.append(current)
                current = {}
                state = 0
            else:
                text_lines.append(line)

    if state == 2 and current:
        current["text"] = "\n".join(text_lines)
        blocks.append(current)
    return blocks


def write_srt(blocks: list[dict[str, str]], path: str | Path) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8", newline="\n") as f:
        for block in blocks:
            f.write(f"{block['id']}\n{block['time']}\n{block['text']}\n\n")
    return p
