---
name: yt-pipeline
description: Safe reusable YouTube Data API pipeline for Dr. Senai Aksoy channels. Use when working on YouTube captions/subtitles, subtitle translation or upload, adding languages (localized titles/descriptions + caption tracks), thumbnails, video metadata titles/descriptions/tags/localizations, playlists, channel verification, bulk subtitle typo fixes, or any YouTube API task in D:\A-klasör\Youtube. Do not write throwaway Python scripts; use the bundled scripts with pinned Python 3.12, UTF-8 output, canonical OAuth tokens, and live channel verification.
---

# yt-pipeline

Use these scripts instead of creating one-off YouTube Python files. They wrap the
working patterns from `youtube-api/youtube_automator.py`,
`manage_captions.py`, `add_video_to_playlists.py`,
`translate_and_update_foreign_fiv.py`, `correct_all_subtitles.py`, and
`update_metadata.py`.

## Hard Rules

1. Run with Python 3.12 only:
   `py -3.12 D:\A-klasör\Youtube\.claude\skills\yt-pipeline\scripts\<script>.py ...`
   The Google API packages are installed for Python 3.12, not the default
   interpreter.
2. Never trust Windows console encoding. The scripts force UTF-8 streams, but
   intermediate data must still be written to explicit UTF-8 files with `--out`
   or `--out-dir`.
3. Keep the channels separate:
   - `--channel fr` = `@SenaiAksoy`, `UC51eCoXFnN1DiBd1dWcJpPQ`, French channel,
     canonical token `youtube-api/token.senaiaksoy.20260510-193158.json`.
   - `--channel tr` = `@DocentDrSenaiAksoy`, `UCbO5qpAnmaQPBJlGMM9ITiw`,
     Turkish channel, canonical token `youtube-api/token.json`.
   - `--channel en` = `@DrAksoyFertility` ("Dr. Aksoy — Fertility, No Hype"),
     `UCo3ZeBXk0ng-OigXd9jqJqQ`, English channel, canonical token
     `youtube-api/token.draksoyfertility.json`.
   Never consolidate channels. Before any mutation, run a live read command and
   confirm the token's `mine=True` channel matches the intended channel.
4. Mutations are dry-run by default. Upload, replace, delete, update, and add
   operations require `--go`. Show the dry-run output to the user and ask for
   explicit approval before re-running with `--go`.
5. FR copy review: if subtitles, descriptions, titles, or other French medical
   text are generated or changed, show the text to Dr. Aksoy before publishing.
6. Medical text gate: if new medical/article-style text is drafted, follow the
   draksoyivf `CLAUDE.md` style-guide preflight before drafting.
7. Secrets stay in `D:\A-klasör\Youtube\youtube-api\`. Never print or commit
   `client_secret.json`, `token.json`, `token.tr.json`, or legacy token files.

## Scripts

Run `--help` on each script for exact parameters.

- `yt_channel.py`: read-only `whoami` and upload-list smoke tests.
- `yt_oauth.py`: one-time OAuth token creation for the canonical per-channel
  token file. Use only when a token is missing or cannot refresh.
- `yt_captions.py`: caption list, download, upload, replace, delete, and offline
  SRT translation (GoogleTranslator: drafts only; not for published FR-channel tracks).
- `yt_metadata.py`: read video snippet/status/localizations and dry-run or apply
  title, description, tags, and localization updates from JSON.
- `yt_playlists.py`: list playlists, list items, and idempotently add videos.
- `yt_thumbnail.py`: set a custom thumbnail (JPG/PNG, max 2 MB; dry-run default, `--go` uploads). Test & Compare is Studio-only.
- `yt_subfix.py`: offline bulk typo correction for SRT files.
- `yt_thumb_compose.py`: offline; adds the channel-style title type (white keyword, gold line, gold pill)
  to an AI base image and writes the 120×68 mobile proof. See `references/thumbnails.md`.
- `yt_i18n.py`: offline; `prep` builds the translation workspace from the FR SRT/title/description,
  `build` QA-checks translator output and writes per-language SRTs + `fixes-localizations.json`.
  See `references/localization.md`.

## Thumbnails and languages (read before doing either)

- Thumbnail for a FR long video: copy the channel's current style (doctor right, navy science backdrop,
  white/gold condensed text, gold pill), base image from Higgsfield `gpt_image_2_5` with approved channel
  thumbnails as identity references, text added by `yt_thumb_compose.py`, never by the image model.
  No talking-head frames, no DHEA premium suit cut-out, nothing from F13. Full recipe:
  `references/thumbnails.md`.
- Languages for a FR long video: the DHEA set of 15 (ar, az, bg, bs, de, es, fa, it, mk, ro, ru, sq, sr,
  tr, uk), each with localized title + description AND a caption track; English only when Dr. Aksoy asks.
  FR SRT from large-v3 ASR + manual correction; translations by Claude subagents (not GoogleTranslator),
  QA with `yt_i18n.py build`, dry-run → `--go`. Full rules: `references/localization.md`.

## Common Flows

Read-only smoke test:

```powershell
cd D:\A-klasör\Youtube\.claude\skills\yt-pipeline\scripts
py -3.12 .\yt_channel.py --channel fr whoami --out D:\A-klasör\Youtube\youtube-api\smoke-fr-channel.json
py -3.12 .\yt_channel.py --channel fr list --max 5 --out D:\A-klasör\Youtube\youtube-api\smoke-fr-videos.json
```

Caption download, translation, review, and upload:

```powershell
py -3.12 .\yt_captions.py --channel fr list --video VIDEO_ID --out captions.json
py -3.12 .\yt_captions.py --channel fr download --caption-id CAPTION_ID --out subtitles_fr.srt
py -3.12 .\yt_captions.py --channel fr translate --file subtitles_fr.srt --src fr --targets ar,en --out-dir review
```

Stop here for human review. After approval:

```powershell
py -3.12 .\yt_captions.py --channel fr upload --video VIDEO_ID --file review\subtitles_fr.ar.srt --lang ar --name Arabic
py -3.12 .\yt_captions.py --channel fr upload --video VIDEO_ID --file review\subtitles_fr.ar.srt --lang ar --name Arabic --go
```

Metadata update:

```powershell
py -3.12 .\yt_metadata.py --channel fr get --video VIDEO_ID --out before.json
py -3.12 .\yt_metadata.py --channel fr update --fixes fixes.json
```

Show the dry-run. Only after explicit approval:

```powershell
py -3.12 .\yt_metadata.py --channel fr update --fixes fixes.json --go
```

Playlist add:

```powershell
py -3.12 .\yt_playlists.py --channel fr add --video VIDEO_ID --playlists PLAYLIST_ID_1,PLAYLIST_ID_2
py -3.12 .\yt_playlists.py --channel fr add --video VIDEO_ID --playlists PLAYLIST_ID_1,PLAYLIST_ID_2 --go
```

Bulk subtitle typo fix:

```powershell
py -3.12 .\yt_subfix.py --file subtitles_fr.srt --fixes typo-fixes.json --out subtitles_fr.fixed.srt
py -3.12 .\yt_captions.py --channel fr replace --caption-id CAPTION_ID --file subtitles_fr.fixed.srt
```

## Notes from the old scripts

- Legacy scripts often guessed between token files. This skill uses the
  channel registry in `yt_common.py` as the only source of truth and never
  falls back automatically.
- `update_metadata.py` mixed a Turkish `CHANNEL_ID` with the French token in
  some paths. The new scripts verify the live token channel every time.
- YouTube Data API cannot pin comments. It can update comment text with
  `youtube.force-ssl`, but pinning itself remains a Studio UI action.
- Caption upload/update is quota-expensive. Prefer read-only list/download and
  offline review before any `--go`.
