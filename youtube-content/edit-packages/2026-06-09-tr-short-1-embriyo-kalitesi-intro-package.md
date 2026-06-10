---
type: edit-package
domain: youtube-content-production
channel: tr
source: youtube-content/shorts-scripts-batch-01-2026-04-29.md
script: Short 1 - Embriyo Kalitesi
status: scripted-intro-selected
created: 2026-06-09
intro-manifest: youtube-content/motion/intro-pilot/MANIFEST.json
intro-render: youtube-content/motion/intro-pilot/renders/intro-pilot-tr.mp4
---

# TR Short 1 Edit Package - Embriyo Kalitesi

## Production Target

- Channel: TR
- Site cue: `tupbebek.com`
- Format: K1 Shorts, 50-60 seconds
- Working title: `3BB Embriyo Düşük Kalite mi? Panik Yapma`
- Source script: [shorts-scripts-batch-01-2026-04-29.md](../shorts-scripts-batch-01-2026-04-29.md), Short 1
- Current production state: script ready, intro asset selected, raw shoot/edit pending

## Intro Asset

- Approved intro manifest: [MANIFEST.json](../motion/intro-pilot/MANIFEST.json)
- Primary intro render: [intro-pilot-tr.mp4](../motion/intro-pilot/renders/intro-pilot-tr.mp4)
- Review render: [intro-pilot-tr.webm](../motion/intro-pilot/renders/intro-pilot-tr.webm)
- Brand skin: TR / `tupbebek.com`
- Required colors: `#2563a8`, `#1a4d7a`, `#3a8a66`, `#f0f7ff`

## Timeline Assembly

| Timecode | Segment | Asset / instruction |
|---|---|---|
| 00:00-00:15 | Intro | Use `intro-pilot-tr.mp4`; do not crop text-safe area |
| 00:15-01:10 | Short body | Insert recorded Short 1 script; keep K1 pacing |
| Final 3-5s | CTA | Use neutral CTA from source script; no promotional language |

If the final short must stay under 60 seconds, use the intro as a pre-roll for long-form or YouTube upload package review, not as part of the published Shorts runtime.

## Source Script Summary

Hook:

`Laboratuvar raporunda "3BB" yazıyor ve Google'a mı koştunuz? Durun.`

Core answer:

- Gardner grading separates expansion stage from ICM and trophectoderm grades.
- `3BB` does not mean there is no chance.
- The embryo grade alone does not determine outcome; endometrium, timing, and clinical context also matter.

CTA:

`Detaylı anlatım tam videoda - açıklamadaki linke bak.`

## Studio Metadata

Title:

`3BB Embriyo Düşük Kalite mi? Panik Yapma`

Description source:

Use the Short 1 description from [shorts-scripts-batch-01-2026-04-29.md](../shorts-scripts-batch-01-2026-04-29.md). Keep the `tupbebek.com` UTM link and informational disclaimer.

Pinned comment source:

Use the Short 1 pinned comment from [shorts-scripts-batch-01-2026-04-29.md](../shorts-scripts-batch-01-2026-04-29.md). Keep the evidence reference and the `tupbebek.com` source cue.

## Compliance Gate

- [ ] No guarantee language
- [ ] No success-rate promise
- [ ] No price, discount, or clinic promotion
- [ ] No patient story
- [ ] No baby/pregnancy emotional imagery
- [ ] No red circle, arrow, warning, or exaggerated reaction visual
- [ ] TR diacritics preserved in on-screen text
- [ ] `node scripts/verify-first-tr-intro-package.mjs` passes before Studio upload
