# Long-Video Thumbnails — Channel Variety & Rotation System (FR · TR · EN)

Master specs stay in `youtube-content/10-thumbnail-production-library.md` (1280×720, ≤ 2 MB, 120×68
mobile proof) and compliance F13 (`youtube-content/02-compliance-checklist.md`).

## Why Variety Is Mandatory (2026-10-20 Rule)
When GLP-1 (`U-ophcWNOro`, `Q7aCrXhG_E8`, `8ZtwHFtF0Io`) and Spermogramme (`pUaFBOSrAO8`, `TluWIqqgQiw`)
all used the same recipe (`classic-gold` + Dr. Aksoy right in navy scrubs + blurred blue cells/molecules),
every thumbnail started looking identical. Looking across `@SenaiAksoy` (FR), `@DocentDrSenaiAksoy` (TR),
and `@DrAksoyFertility` (EN), the channel's best-performing thumbnails actually rotate across **5 visual
axes** while keeping Dr. Aksoy's face 99 % recognizable.

---

## 1. Preflight Before Designing Any Thumbnail

1. Run the rotation status check first:
   ```powershell
   py -3.12 D:\A-klasör\Youtube\.claude\skills\yt-pipeline\scripts\yt_thumb_compose.py --channel <fr|tr|en> --status
   ```
2. Read the last entries in `references/thumb-log.json` and pick a combination of
   `(--template, --side, --outfit, --pose, --backdrop)` that **does not repeat** the previous video on
   that channel.
3. Verify your planned combination before calling Higgsfield:
   ```powershell
   py -3.12 D:\A-klasör\Youtube\.claude\skills\yt-pipeline\scripts\yt_thumb_compose.py --channel <fr|tr|en> --template <T> --side <left|right> --outfit <O> --pose <P> --backdrop <B> --check-variety
   ```

---

## 2. The 5 Rotation Axes (Learned from FR / TR / EN Channels)

### Axis A — Typography & Color Template (`--template`)
| Template | Visual Style | Channel Reference Examples |
|---|---|---|
| `classic-gold` | White condensed line 1 + Gold (`#F0BE50`) line 2 + Gold rounded pill | `pUq5UJ3PEH4` (*Bêta-hCG après FIV*), `SD3CKpN6VS0` (*Quels compléments ?*) |
| `yellow-focus` | Heavy yellow (`#FFD600`) hook lines with dark stroke + White pill at bottom corner | FR `pqc9UgCIqo0` (*Mieux choisir le sperme ?*), `Uw2xfxw7N48` (*Endomètre : trop fin ?*), TR `U8vAciGqvSU` (*Hangisi İşe Yarar?*) |
| `coral-contrast` | White line 1 + Warm Coral/Terracotta (`#E86850`) line 2 + Coral badge + optional `--chip "10 → ?"` | FR `2QpLE_wST1s` (*FIV après 40 ans · 10 → ? · Réalités & Choix*) |
| `amber-eyebrow` | Top eyebrow pill badge + 2 or 3 stacked White/Amber (`#F5B841`) lines with crisp dark outline | FR `MoApIs3-WwE` (*Le cœur bat-il déjà ?*), EN `queLygimeS8` (*Is the Heart Beating?*), TR `za6o781xbWw` |
| `light-card` | Warm cream/clinical split backdrop on text side + Deep Navy (`#142640`) & Burgundy (`#9C2A3A`) type | FR `Ks0Cwpy_a4A` (*AMH basse*), `x8VzlUmEQEw` (*Dossier embryonnaire*), TR `P7CdnSIAOFI` (*İkiye Katlanmadı · 100→150*) |

### Axis B — Layout & Side (`--side`)
- `left` (Doctor on RIGHT third, text on LEFT 55 %) — standard, max 2 times in a row with the same outfit.
- `right` (Doctor on LEFT third, text on RIGHT 55 %) — FR `zhcapjJhxzA` (*FIV à l'étranger ?*), `x8VzlUmEQEw` (*Dossier embryonnaire*). Use every 2nd–3rd video to break grid monotony.

### Axis C — Doctor Outfit (`--outfit`) & Identity References on Disk
Never use the same outfit + pose twice in a row. Pick reference images from disk matching the target outfit:
- `white-coat`: Crisp white doctor's lab coat over shirt & tie (classic specialist look across 80 % of FR catalog).
  - Disk refs (`D:\A-klasör\Youtube\thumbs_fr_scan\thumbs\`): `001_pqc9UgCIqo0.jpg`, `002_Uw2xfxw7N48.jpg`, `004_brJ1PiPP1fc.jpg`, `052_YfOz7V4dqYs.jpg`
- `scrubs`: Navy V-neck medical scrubs.
  - Disk refs (`D:\A-klasör\Youtube\youtube-api\glp1-recut-2026-10-16\channel-thumbs\`): `2026-09-22-pUq5UJ3PEH4.jpg`, `2026-10-06-SD3CKpN6VS0.jpg`, `2026-06-29-zhcapjJhxzA.jpg`
- `shirt`: Crisp white or light-blue button-down shirt, no coat, warm clinical office feel.
  - Disk refs: `2026-09-01-Ks0Cwpy_a4A.jpg` (*AMH basse*), `2026-08-20-2QpLE_wST1s.jpg` (*FIV après 40 ans*)
- `coat-blue-shirt`: White doctor's coat over open-collar royal/light blue shirt (no tie).
  - Disk ref: `.tmp\en-tr-thumbs\tr-za6o781xbWw.jpg` (*Düşükten Sonra Ne Kadar Beklemeli?*)

### Axis D — Pose & Hand Gesture (`--pose`)
Do not repeat `chin` (hand on chin) in consecutive videos:
- `open-hands`: Both hands or one hand open at chest level in a calm explaining gesture (`YfOz7V4dqYs`, `U8vAciGqvSU`, `P7CdnSIAOFI`).
- `pointing`: One index finger raised or pointing calmly toward the topic/text (`TfjN2BKxqyw`, `fNIy0xFmQsg`, `3ntGxfx0gFs`).
- `calm-clasped`: Hands clasped in front or arms relaxed, reassuring slight smile (`brJ1PiPP1fc`, `Ks0Cwpy_a4A`, `za6o781xbWw`).
- `chin`: Hand resting thoughtfully on chin (`pUq5UJ3PEH4` — use at most once every 4 videos).

### Axis E — Topic-Specific Medical Backdrop (`--backdrop`)
**Hard rule:** Generic floating blue cells + ball-and-stick molecules (`cells-molecules`) must NOT be used as a default filler. Every video's backdrop must depict the concrete medical subject of that video:
- `ultrasound`: High-contrast grayscale ultrasound fan cone with a warm amber highlight on the follicle/sac/endometrium (`MoApIs3-WwE`, `Uw2xfxw7N48`, `FlVV8qNhJXU`).
- `embryo-microscope`: Embryology microscope view — blastocyst (`0xafaN3UJsM`), ICSI micropipette + single sperm (`pqc9UgCIqo0`), or oocyte (`aX4XIEcjxVg`) in emerald/teal/amber tones.
- `clinic-warm`: Softly blurred warm clinical consultation room or embryology lab with microscope/incubators and warm tungsten/daylight bokeh (`brJ1PiPP1fc`, `pN8HNmPnfXg`, `zhcapjJhxzA`).
- `bottles-props`: Clean, **unlabeled** white or amber supplement/medication bottles or lab tubes on a counter (`SD3CKpN6VS0`, `U8vAciGqvSU`).
- `chart-data`: Subtle rising hormone curve, calendar grid, or age-decline line behind the text (`pUq5UJ3PEH4`, `2QpLE_wST1s`, `za6o781xbWw`).
- `light-editorial`: Bright warm ivory/cream clinical backdrop with soft medical line-art or clean consultation room (`Ks0Cwpy_a4A`, `x8VzlUmEQEw`, `P7CdnSIAOFI`).
- `anatomy-3d`: Clean, tasteful 3D medical illustration of uterus/fallopian tubes/ovary (`gBrcdndP5XI`, `y6B43MrIvAk`).

---

## 3. Rejected Patterns (Never Reuse)
- **Identical A/B variants:** Variant A and Variant B for Studio "Test & Compare" must NOT be the exact same image with only 2 words changed. Vary the `--template` (e.g. Variant A `yellow-focus` vs Variant B `amber-eyebrow`) or generate 2 distinct base compositions.
- **DHEA dark-suit cut-out on flat burgundy/cream:** Rejected by Dr. Aksoy ("seçtiğin Dr Aksoy fotosu güzel değil").
- **Frames grabbed from talking-head video:** Mouth open mid-word, webcam lighting.
- **F13 / Compliance hard no:** Red circles, arrows, ⚠ signs, "%" claims, shocked faces, syringes/injection pens close-up, pregnant belly, baby, drug brand names, clinic logo/name, red-pen strikes/stamps from Outsider Inside.

---

## 4. Production Workflow

1. **Check status & pick rotation:**
   `py -3.12 scripts\yt_thumb_compose.py --channel fr --status`
2. **Generate base image (Higgsfield `gpt_image_2_5`):**
   - Upload 1–2 approved disk references matching the chosen `--outfit`.
   - Prompt for the chosen `--side` (`RIGHT third` if `--side left`, `LEFT third` if `--side right`), `--outfit`, `--pose`, and concrete `--backdrop`.
   - Keep the text side (`LEFT 55%` or `RIGHT 55%`) clean and uncluttered.
   - STRICTLY no text, letters, numbers, or logos in the AI generation.
3. **Compose type & log variety:**
   ```powershell
   py -3.12 scripts\yt_thumb_compose.py --base base.png --out fr-thumb-00-slug-A.jpg `
     --channel fr --video VIDEO_ID --slug slug `
     --template yellow-focus --side left --outfit white-coat --pose open-hands --backdrop clinic-warm `
     --line1 "KEYWORD" --line2 "QUESTION ?" --pill "LABEL" `
     --check-variety --log-variety
   ```
4. **Verify:** Check `*-mobile.png` (120×68 proof), face fidelity, hands/glasses, file size ≤ 2 MB, and side-by-side contrast against the last 3 channel thumbnails.
