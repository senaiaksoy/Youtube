# YouTube Intro Pilot FRAME.md

## Purpose
This document defines the 15-second motion structure for the reusable
YouTube/Shorts intro pilot.

## Canvas
- Aspect ratio: 16:9
- Design size: 1920 x 1080
- Safe text area: keep all visible text inside the central 80% width and 70% height
- Mobile check: title must remain readable when previewed at small player size

## Inputs
- `channel`: `tr` or `fr`
- `title`: per-video title, defaulting to the skin title
- `identityLine`: skin-specific Dr. Aksoy identity line
- `siteCue`: linked site cue

## Timeline

### Beat 1: Brand Field, 0.0s-3.0s
The frame opens on a clean brand field.

Motion:
- background fades in from white or near-white over 0.4s
- fine line motif draws from left to right between 0.4s and 2.0s
- two or three small dots appear with 0.15s stagger
- no text should dominate this beat

TR skin:
- base: `#f0f7ff`
- line: `#2563a8`
- micro-accent: `#3a8a66`

FR skin:
- base: `#ffffff`
- line: `#094183`
- micro-accent: `#e8578a`

### Beat 2: Main Title, 3.0s-8.0s
The main title becomes the visual focus.

Motion:
- title enters at 3.0s with a soft upward fade
- title reaches final position by 3.8s
- accent line settles under the title by 4.3s
- line motif remains subtle in the background
- title holds from 4.3s to 8.0s

Text rules:
- maximum recommended title length: 42 characters
- if title is longer than 42 characters, split into two lines
- never use all caps for full title
- preserve TR/FR diacritics unless a renderer cannot support them

Default TR title:
`Tüp Bebekte Doğru Bilgi`

Default FR title:
`Comprendre la FIV avec clarté`

### Beat 3: Identity Line, 8.0s-12.0s
The title reduces slightly and the identity line appears.

Motion:
- title scales down to 92% between 8.0s and 8.4s
- identity line fades in between 8.3s and 9.0s
- site cue appears between 9.1s and 9.5s
- hold the full composition until 12.0s

Default TR identity:
`Dr. Senai Aksoy | Üreme Sağlığı`

Default FR identity:
`Dr. Senai Aksoy | FIV à Istanbul`

### Beat 4: Transition Out, 12.0s-15.0s
The frame resolves into a usable title-card end state, then exits.

Motion:
- background accent panel wipes gently from right to left between 12.0s and 13.0s
- title and identity hold readable until 14.2s
- final fade or wipe begins at 14.2s
- final frame reaches transition-ready state by 15.0s

## Channel Skin Mapping

### TR
- `channel`: `tr`
- `title`: `Tüp Bebekte Doğru Bilgi`
- `identityLine`: `Dr. Senai Aksoy | Üreme Sağlığı`
- `siteCue`: `tupbebek.com`
- primary: `#2563a8`
- secondary: `#1a4d7a`
- accent: `#3a8a66`
- surface: `#f0f7ff`
- white: `#ffffff`
- text: `#0f2b4b`

### FR
- `channel`: `fr`
- `title`: `Comprendre la FIV avec clarté`
- `identityLine`: `Dr. Senai Aksoy | FIV à Istanbul`
- `siteCue`: `draksoyivf.com`
- primary: `#094183`
- secondary: `#dce9f3`
- accent: `#e8578a`
- surface: `#ffffff`
- soft-grey: `#efefef`
- text: `#222222`

## Motion Guardrails
- no shake
- no bounce
- no flashing
- no warning iconography
- no red circle emphasis
- no baby imagery
- no pregnant belly imagery
- no patient faces
- no before/after visuals
- no arrows or red circles
- no exaggerated reactions
- no prices or discounts
- no clinic address
- no patient stories
- no success-rate claim
- no promotional medical claims
- no guarantee language
- no miracle, secret, shocking, or guaranteed language
- no burgundy/gold/cream palette

## Preview Requirements
- preview both TR and FR skins
- check desktop 16:9 composition
- check mobile readability
- capture final-frame screenshot for both skins
- capture readable hold screenshots before 14.2s and transition-ready screenshots at 15.0s for both skins
- confirm the rejected burgundy/gold/cream palette is not used
