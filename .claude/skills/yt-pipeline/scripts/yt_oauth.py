# -*- coding: utf-8 -*-
"""Create one canonical OAuth token for a channel after live verification."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from yt_common import API_DIR, SCOPES, build_youtube, canonical_token_path, channel_config, write_json

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
except ImportError:
    sys.stderr.write("ERROR: google-auth-oauthlib missing. Run: py -3.12 -m pip install google-auth-oauthlib\n")
    sys.exit(2)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--channel", required=True, choices=["fr", "tr"])
    ap.add_argument("--port", type=int, default=8090)
    ap.add_argument("--no-browser", action="store_true")
    args = ap.parse_args()

    ch = channel_config(args.channel)
    client_secret = API_DIR / "client_secret.json"
    if not client_secret.exists():
        sys.stderr.write(f"ERROR: client secret missing: {client_secret}\n")
        sys.exit(2)

    os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"
    flow = InstalledAppFlow.from_client_secrets_file(str(client_secret), SCOPES)
    creds = flow.run_local_server(port=args.port, open_browser=not args.no_browser)

    yt = build_youtube(creds)
    live = yt.channels().list(part="snippet,statistics", mine=True).execute()["items"][0]
    result = {
        "requestedChannel": args.channel,
        "expectedId": ch["id"],
        "expectedHandle": ch["handle"],
        "liveChannelId": live["id"],
        "liveTitle": live["snippet"].get("title"),
    }
    write_json(API_DIR / "oauth-result.json", result)

    if live["id"] != ch["id"]:
        sys.stderr.write(
            "ERROR: selected account is the wrong channel. Token was not saved.\n"
            f"Expected {ch['handle']} ({ch['id']}), got {live['snippet'].get('title')} ({live['id']}).\n"
            f"Details written to {API_DIR / 'oauth-result.json'}\n"
        )
        sys.exit(3)

    token_path = canonical_token_path(args.channel)
    token_path.write_text(creds.to_json(), encoding="utf-8")
    print(f"saved canonical token: {token_path}")
    print(f"verified channel: {ch['handle']} ({ch['id']})")


if __name__ == "__main__":
    main()
