# -*- coding: utf-8 -*-
"""Offline bulk typo correction for SRT files."""

from __future__ import annotations

import argparse

from yt_common import parse_srt, read_json, write_srt


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--file", required=True)
    ap.add_argument("--fixes", required=True, help='JSON object such as {"wrong": "right"}')
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    fixes = read_json(args.fixes)
    blocks = parse_srt(args.file)
    total = 0
    for block in blocks:
        for wrong, right in fixes.items():
            count = block["text"].count(wrong)
            if count:
                block["text"] = block["text"].replace(wrong, right)
                total += count
    path = write_srt(blocks, args.out)
    print(f"changed={total} out={path}")
    print("review required before replacing any live caption track")


if __name__ == "__main__":
    main()
