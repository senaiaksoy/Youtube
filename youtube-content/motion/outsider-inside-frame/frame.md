---
version: 1.0
name: Outsider Inside — Frame (video / frame layer)
description: >
  Frame-scale design system for Dr. Senai Aksoy's French-language YouTube channel "Outsider Inside".
  Register: the evidence-critical second opinion — a clinician reading the literature with a red pen.
  Warm paper ground, blue-black ink voice, ONE red "correcteur" accent used only for marking up
  claims (strike, circle, underline, stamp). Literata display + IBM Plex Sans body + IBM Plex Mono
  for references and chrome. Real footage over invented decoration. No glow, no gradient, no
  breathing ambience.
unit: the frame — 1920×1080 primary; 9:16 (Shorts) documented
principle: atoms are sacred · composition is free · every number has a reference
language: on-screen text follows the channel — fr (@SenaiAksoy, default), tr (@DocentDrSenaiAksoy), en (@DrAksoyFertility); fonts must render French and Turkish (ğ ş ı İ ç ö ü)
scope: applies to HyperFrames projects started on or after 2026-10-15; earlier projects keep their own frame.md / DESIGN.md untouched

colors:
  paper: "#F4F0E6"        # default ground — warm, never pure white
  paper-deep: "#E8E1D0"   # half-step surface for cards / reference slips
  ink: "#1B2230"          # blue-black — headlines, body, rules
  ink-soft: "#4A5263"     # secondary text, captions
  graphite: "#8C877A"     # hairlines on paper, footnote numerals, disabled
  correcteur: "#C4301C"   # the red pen — markup ONLY (strike, circle, underline, stamp, § mark)
  lab: "#121820"          # dark surface — footage frames, microscope / ultrasound panels
  lab-elev: "#1D252E"     # caption tab / title bar on lab surface

borders: { hairline: "1px solid ink@14%", hairline-strong: "1px solid ink@28%", lab: "1px solid paper@16% (on lab)" }
shadows: { none: "none", slip: "0 1px 0 ink@10%" }   # paper does not cast shadows; a slip may sit 1px proud

typography:
  # PHONE FLOOR (2026-10-16): no visible text below 40 px at 1080 px short side = 2.1cqw on 16:9.
  # Enforced by tools/legibility.mjs before every render. Px values are @1920×1080.
  # — reading + chrome ramp —
  body:      { fontFamily: "IBM Plex Sans", cqw: 2.3,  weight: 400, lineHeight: 1.3 }       # 44px
  lead:      { fontFamily: "IBM Plex Sans", cqw: 2.6,  weight: 400, lineHeight: 1.3 }       # 50px
  label:     { fontFamily: "IBM Plex Sans", cqw: 2.3,  weight: 600, lineHeight: 1.15, tracking: "0.01em" }  # 44px
  kicker:    { fontFamily: "IBM Plex Mono", cqw: 2.1,  weight: 500, tracking: "0.12em", upper: true }        # 40px
  ref:       { fontFamily: "IBM Plex Mono", cqw: 2.1,  weight: 400, lineHeight: 1.32 }      # 40px — citations, footnotes
  stamp:     { fontFamily: "IBM Plex Mono", cqw: 3.6,  weight: 700, tracking: "0.08em", upper: true }        # 70px (TR long words 3.1)
  # — display ramp (Literata, sentence case, opsz high) —
  headline:  { fontFamily: "Literata", cqw: 4.4, weight: 500, lineHeight: 1.08, tracking: "-0.015em" }   # 84px
  evidence:  { fontFamily: "Literata", cqw: 3.3, weight: 500, lineHeight: 1.12, tracking: "-0.012em" }   # 64px
  claim:     { fontFamily: "Literata", cqw: 5.2, weight: 400, lineHeight: 1.1,  tracking: "-0.015em", italic: true }  # 100px
  display:   { fontFamily: "Literata", cqw: 7.2, weight: 600, lineHeight: 1.02, tracking: "-0.022em" }  # 138px
  number-hero: { fontFamily: "Literata", cqw: 8.3, weight: 600, lineHeight: 0.95, tracking: "-0.03em", numerals: "lining tabular" }  # 160px
  number-unit: { fontFamily: "IBM Plex Mono", cqw: 2.3, weight: 500 }

spacing:
  frame-pad: "4.6cqw"     # ~88px @1920
  gap-sm: "0.8cqw"
  gap-md: "1.8cqw"
  gap-lg: "3.6cqw"
  hairline: "1px"
  radius: "2px"           # paper is cut, not rounded
  pen-stroke: "0.42cqw"   # ~8px @1920 — every red-pen mark uses this weight

components:
  kicker-section:
    typography: "{typography.kicker}"
    mark: "§ in {colors.correcteur}, then episode number and topic — e.g. § 03 · VARICOCÈLE"
    description: "The eyebrow. Mono uppercase, 2–5 words, always opened with a red §. Never a full sentence."
  pen-strike:
    stroke: "{colors.correcteur}, {spacing.pen-stroke}, round caps"
    description: >
      The signature mark. A real hand-drawn marker stroke from assets/pen/ (strike-01/02 for body and
      claim sizes, wide-strike-01/02 for display ≥ 7cqw) drawn THROUGH a claim at x-height, ±1–3° tilt,
      mix-blend-mode multiply. Never a CSS text-decoration, never a generated or perfectly straight line.
  pen-circle:
    stroke: "{colors.correcteur}, {spacing.pen-stroke}"
    description: "A real hand-drawn loop (assets/pen loop-01 / oval-01, wide-loop-01 / wide-oval-01) around ONE word or number; class pen--loop."
  pen-underline:
    stroke: "{colors.correcteur}, {spacing.pen-stroke}"
    description: "A real hand-drawn underline (assets/pen underline-01, wide-underline-01) under the word that carries the argument. Max one per frame."
  verdict-stamp:
    typography: "{typography.stamp}"
    border: "0.25cqw solid {colors.correcteur}"
    rounded: "{spacing.radius}"
    rotation: "-4° to -7°"
    texture: "assets/textures/stamp-mask.png as mask-image (100% 100%), mix-blend-mode multiply"
    description: >
      The evidence verdict. Fixed vocabulary only: PREUVE SOLIDE · PREUVE FAIBLE · NON PROUVÉ ·
      NON RECOMMANDÉ · ÇA DÉPEND. TR: GÜÇLÜ KANIT · ZAYIF KANIT · KANITLANMADI · ÖNERİLMEZ · DURUMA GÖRE.
      EN: STRONG EVIDENCE · WEAK EVIDENCE · NOT PROVEN · NOT RECOMMENDED · IT DEPENDS. At most once per scene.
  reference-slip:
    backgroundColor: "{colors.paper-deep}"
    border: "{borders.hairline}"
    rounded: "{spacing.radius}"
    typography: "{typography.ref}"
    description: >
      The citation card — authors · journal · year · design (RCT, méta-analyse, cohorte, n=). Looks
      like an index card from a bibliography drawer. Every number-hero and every verdict-stamp has one.
  footnote-marker:
    typography: "{typography.ref} inline (not superscript — a sup shrinks below the phone floor)"
    description: "[1] [2] beside a claim or figure, linking to the reference-slip on screen or in the description."
  lower-third:
    backgroundColor: "{colors.paper}"
    border: "top 1px {colors.ink}"
    typography: "{typography.label} name + {typography.ref} role"
    description: >
      Talking-head identifier: 'Dr Senai Aksoy' / 'Médecine de la reproduction · Istanbul'. A paper
      tab that slides in from the left edge, flush to frame-pad; no blur, no glass, no logo animation.
  footage-tab:
    backgroundColor: "{colors.lab-elev}"
    typography: "{typography.ref} in paper"
    description: >
      Caption tab on real footage (lab, microscope, ultrasound): what we are looking at + source
      ('Time-lapse embryonnaire · J1→J5 · archive clinique'). Bottom-left, inside frame-pad.
  illustration-tab:
    backgroundColor: "{colors.lab-elev}"
    typography: "{typography.kicker} in paper"
    text: "fr ILLUSTRATION · tr TEMSİLİ ÇİZİM · en ILLUSTRATION"
    description: >
      Mandatory, always visible, on every AI-generated or stock clip (top-left, inside frame-pad) for its whole duration.
      Tells the viewer the image is a representation, not a recording. Never removed, never faded out early.
  signature-line:
    typography: "{typography.claim}"
    description: >
      The channel's closing line: « Les garanties, c'est pour les réfrigérateurs, pas pour la
      biologie. » TR: « Garantiler buzdolabı içindir, biyoloji için değil. » Literata italic, ink on paper;
      'garanties' / 'Garantiler' carries the single pen-circle.
---

# Outsider Inside — Frame (video / frame layer)

## Overview

At frame scale Outsider Inside is **a clinician's annotated reading copy**. The viewer is looking
over the doctor's shoulder at the literature, the brochure, the clinic's promise — and watching it
get marked up. The thesis is three colors: **paper is the ground, ink is the voice, red is the
pen**. The red never decorates; it only ever *judges* — it strikes, circles, underlines or stamps.
If a red element is not making a judgment, it should not be red.

The channel's authority comes from evidence, not from production gloss. So the visual system
deliberately refuses the vocabulary of AI-generated motion graphics (glows, gradients, glass,
particles, breathing backgrounds, neon on dark). It borrows instead from physical objects that
carry credibility: printed journals, index cards, rubber stamps, a red correcting pen, real
laboratory footage.

Three voices, each in its own face: **Literata** (display) speaks the claims and the conclusions;
**IBM Plex Sans** (body) explains; **IBM Plex Mono** (reference) cites. Swapping a voice's face
collapses the register.

**Key characteristics at frame scale:**

- **Paper / ink / red pen** + a dark **lab** surface used only for real footage and imaging.
- **The strike is the signature move** — a claim is set in Literata italic, then struck through by hand.
- **Every figure has a reference-slip.** No naked numbers, ever.
- **Real media first** — lab, microscope, ultrasound, the clinic — before any typographic frame.
- **Stillness is allowed.** Paper does not breathe. A frame may hold perfectly still while the voice carries it.

## The Frame

### Frame Craft Bar

Eyeball tests that gate every frame:

- **Squint** — one Literata moment (claim, display or number) dominates at 3–6× its neighbour.
- **Pen** — red appears only as a mark of judgment (strike / circle / underline / stamp / §). One mark per frame, a strike + stamp pair at most.
- **Proof** — any number or verdict on screen has its reference-slip or footnote-marker visible in the same frame.
- **Not-AI** — no glow, no gradient, no glass, no particles, no neon, no 3D tilt, no ambient drift.

- **Primary:** 1920×1080 (16:9). Author sizes in **`cqw`** (`px ÷ 1920 × 100`).
- **Vertical:** 1080×1920 (9:16) for Shorts; **Square:** 1080×1080 only if asked.
- **Safe area:** `frame-pad` 4.6cqw; captions and lower-thirds sit inside it. On 9:16, keep the bottom 18% clear for platform UI.
- **9:16 sizing:** keep the same **pixel** sizes as 16:9 (cqw token × 1.78 on a 1080-wide frame); the 40 px floor is the same.
- **One source, two aspects (2026-10-17):** a scene is written once, in `index.html` at 1920×1080. Its portrait layout lives in
  the same file under `:root[data-aspect="9x16"] …` rules (helpers `.only-169` / `.only-916`; sizes via `--W` / `--H`).
  `node tools/aspect.mjs <project>` writes the Shorts twin to `<project>/shorts/` (1080×1920, same facts, assets linked);
  check, legibility, facts verify and render run on it unchanged. Never hand-edit `shorts/index.html`.
- **Shorts UI zone:** YouTube draws title/channel/music over the **bottom 18 %** and the action icons over the **right
  120 px of the lower 55 %**. No text there (`legibility.mjs` fails it); footage and paper may run under it.
- **Portrait moves that work:** claims and headlines wrap with `text-wrap: balance`; a strike over a two-line claim becomes
  one diagonal stroke corner to corner; uppercase mono labels that would wrap become sentence-case Plex Sans; figure pairs
  stay side by side at 110–130 px; the slip spans the column and wraps to four lines.

**Container law.** Every frame ground sets `container-type: size`; frame-relative units are `cqw`/`cqh`, never `vw`.

## Colors

Default ground `{colors.paper}`; cards and slips on `{colors.paper-deep}` — a half-step, never a hard
contrast. Text is `{colors.ink}` / `{colors.ink-soft}`; hairlines `{colors.graphite}` or ink at low alpha.

`{colors.correcteur}` is the pen. It is never a background fill, never a headline colour, never a
button, never a gradient stop. Its only jobs: pen-strike, pen-circle, pen-underline, verdict-stamp,
the § in kickers.

`{colors.lab}` / `{colors.lab-elev}` are the dark surfaces for real footage, microscope and
ultrasound panels. On lab, text is paper; the pen keeps the same red.

No pure white, no pure black, no cool grey, no fourth hue. No traffic-light green/amber/red for
evidence levels — evidence strength is expressed by the **stamp vocabulary**, not by colour.

## Typography

- **Display (Literata):** sentence case always. `claim` (italic) is the voice of the thing being
  examined — the brochure line, the add-on's promise. `display` / `headline` (roman) is the doctor's
  conclusion. Italic = what *they* say; roman = what the *evidence* says.
- **Body (IBM Plex Sans):** 400, sentence case. Explanatory lines only; ≤ 2 lines per frame.
- **Reference (IBM Plex Mono):** kickers, citations, footnotes, footage tabs, stamps.
- **Phone legibility floor (hard rule):** every visible piece of text — kicker, label, citation, footnote marker, footage tab, lower-third — is **≥ 40 px at 1080 px on the short side** (2.1cqw on 16:9; 3.7cqw on 9:16). Most viewers watch on a phone; a line that can't be read there doesn't exist. No exceptions for "small print": if a citation doesn't fit at 40 px, shorten it (authors · journal · year · design · n) or split it over two lines. Only text that is part of real footage may opt out, with `data-legibility-exempt="reason"`. Check: `node tools/legibility.mjs <project>` (fails the render on any run below the floor, measured after transforms at 24+ points of the timeline).
- **Fewer words, not smaller words:** when a frame doesn't fit, cut text or split the frame — never shrink below the floor.
- **Fit to measure:** headline block ≤ 82cqw wide. ≤ 3 words → `display`; 4–8 → `claim`/`headline`; longer → it's a voice-over line, not an on-screen line.
- **French typography (fr channel):** non-breaking thin space before « ? ! : ; » and inside « guillemets »; use real « » not "".
- **Numerals:** lining, tabular (`font-variant-numeric: lining-nums tabular-nums`) for figures and percentages.

## Depth & Surface

Paper is flat. Elevation is a **1px hairline** or a half-step `paper-deep` slip sitting 1px proud
(`{shadows.slip}`). The only texture is a **single static paper grain** from a real photographed A4 sheet
(`assets/textures/paper-grain-16x9.png` / `-9x16.png`: neutral-grey, lighting flattened) laid over
`{colors.paper}` with `mix-blend-mode: soft-light; opacity: 0.35` — never animated noise. On lab surfaces, footage provides all the depth needed.

**Ceiling:** no drop shadows beyond `slip`, no blur, no glow, no gradient, no glassmorphism, no tilt
(the verdict-stamp's −4°…−7° rotation is the single exception).

## Shapes

Paper is cut, not rounded: **2px** radius everywhere. Pen marks are the only curves. No pills, no
circles as containers, no blobs.

## Components

- **kicker-section** — red § + mono uppercase topic. Opens every chapter.
- **pen-strike / pen-circle / pen-underline** — the red-pen family; real marker strokes from `assets/pen/`, revealed by `--p` (see Assets).
- **verdict-stamp** — fixed five-word vocabulary; ink-starved edges.
- **reference-slip** + **footnote-marker** — the proof layer.
- **lower-third** — paper tab for the talking head.
- **footage-tab** — caption tab on real footage.
- **illustration-tab** — mandatory ILLUSTRATION / TEMSİLİ ÇİZİM tag on every AI-generated or stock clip, whole duration.
- **signature-line** — the closing fridge line.

## Frame Treatments

> Recipe: ground · composes · focal · chrome · pen · Fixed/Free · density.

### 1 · Cover — Titre d'épisode
**Ground** paper. **Composes** kicker-section, display title, lead (one-line hook), ref line (episode n° · date).
**Focal** a 1–2 line Literata `display` title, flush left. **Chrome** mono episode line at top.
**Pen** the red § only — or one pen-underline under the word that carries the question.
**Fixed** paper ground, Literata sentence case, flush-left. **Free** title, hook, layout. **Density** sparse.

### 2 · La promesse barrée — Claim → Strike (signature treatment)
**Ground** paper. **Composes** kicker-section, `claim` in Literata italic (the promise, quoted with « »), pen-strike, then `headline` in roman beneath (what the evidence actually says), footnote-marker.
**Beat order** claim lands and holds (≥ 1.2s, long enough to read) → strike draws through at pen speed → correction line appears below. Never strike before the viewer has read the claim.
**Fixed** italic-for-claim / roman-for-evidence, one strike. **Free** the wording, vertical rhythm. **Density** medium.

### 3 · Le verdict — Stamp
**Ground** paper (or the previous frame held). **Composes** headline (the add-on / test / practice named), verdict-stamp, reference-slip.
**Focal** the stamp, landing on a hard cut (no scale bounce): frame N absent, frame N+1 present at final rotation, with a 2-frame ink-spread on the edges.
**Fixed** stamp vocabulary, one stamp per scene, reference-slip present. **Free** placement (it may overlap the headline). **Density** sparse.

### 4 · Le chiffre — Number with proof
**Ground** paper. **Composes** kicker-section, number-hero + number-unit, one body line of context, reference-slip (bottom-left, full measure, 40 px mono, ≤ 2 lines).
**Focal** the Literata figure. **Pen** optional pen-circle around the figure when the number contradicts the claim.
**Fixed** reference-slip always present; figure comes from the script with its source. **Free** layout. **Density** sparse.
Comparisons (e.g. avec / sans) are **two figures side by side with one hairline between** — not a bar chart unless there are ≥ 4 data points.

### 5 · Le labo — Real footage (and labelled illustration)
**Ground** lab, footage full-bleed. **Composes** footage, footage-tab, optional single pen-circle on the structure being discussed (drawn on top of the footage, red stays red).
**Fixed** embryos, gametes, ultrasound and the lab are **real footage only** (`assets/footage/`, EmbryoScope exports); footage-tab names the source. Hormone, cellular and molecular **mechanisms** may be AI-generated (Higgsfield) or schematic, always with the **illustration-tab** for the whole clip, checked for anatomical and biological correctness before use (Dr. Aksoy decision, 2026-10-16). **Free** crop, duration. **Density** footage-led.

### 6 · La référence — Citation focus
**Ground** paper. **Composes** a large reference-slip (title in Literata `headline`, authors · journal · year · design · n= in mono), optional one-line pen-underline on the key phrase of the conclusion.
**Fixed** quote at most one short phrase from the paper (≤ 15 words), always attributed; paraphrase the rest. **Free** layout. **Density** medium.

### 7 · Talking head — Lower-third & side note
**Ground** camera footage. **Composes** lower-third (first appearance only), optional side note: a paper-deep slip on the right third with ONE key term or figure + footnote-marker.
**Fixed** max one overlay element besides the lower-third at a time; never cover the face. **Free** timing. **Density** sparse.

### 8 · Clôture — Signature
**Ground** paper. **Composes** signature-line, pen-circle around « garanties », small ref line (channel / site).
**Fixed** the line verbatim, Literata italic, the one circle. **Free** hold duration. **Density** sparse.

## Motion Register (prose guidance for hyperframes-animation)

Motion should feel like **a hand and a page**, not like software.

- **Pen marks** draw on by tweening the CSS variable `--p` 0→1 (`tl.fromTo(el,{'--p':0},{'--p':1,duration:.55,ease:'power2.inOut'},t)`), 0.45–0.7s — the speed of a real hand. Loops 0.6–0.8s. Easing bounce never.
- **Text** arrives by a short fade + 6–10px rise (0.35–0.5s, `power3.out`), or simply cuts in. No per-letter cascades, no blur-in, no scale-from-zero.
- **Stamps** cut in (see treatment 3). Never scale, never spin.
- **Paper slips** slide in along one axis, as if pushed by a hand (0.5s, `power3.out`), and stop dead.
- **Scene changes:** hard cuts by default; cross-dissolve ≤ 0.3s for time passing; chapter breaks may use a paper-slide (the next sheet slides over the previous). **No** flash-through-white, glitch, zoom-blur, light-leak or shader-wipe transitions.
- **Sound (installed):** every pen mark and stamp carries its real foley from `assets/sfx/` (recorded by Dr. Aksoy: marker on paper, rubber stamp on desk). Pen sound starts with the reveal; stamp sound starts 0.03 s before the stamp frame. No stock whooshes, risers, swooshes or impacts — ever. See `assets/sfx/README.md`.
- **Ambient motion: none.** No breathing glows, no drifting ghost text, no floating shapes. A still frame with a strong voice-over is correct.
- **Counters:** a number may count up only if the voice-over is talking about growth or accumulation; otherwise it cuts in at its final value.

## Composition Rules

### Do
- Start from **real material**: the actual brochure line, the actual paper, the actual lab footage.
- Lead each frame with **one focal**, flush left by default; let the frame be mostly paper.
- Use **italic for the claim, roman for the evidence** — consistently, across the whole channel.
- Put the **reference on screen** whenever a number or verdict is on screen.
- Ration the red pen to **one judgment per frame**.
- Size every text for a **phone** first (≥ 40 px @1080, see Typography); cut words before shrinking type.

### Don't
- No glow, gradient, glass, particles, neon, lens flares, light leaks, 3D tilt, bouncing or elastic easing.
- No radial "breathing" backgrounds, ghost text, floating orbs or decorative grids (overrides house-style background layer).
- No banned fonts (Inter, Roboto, Poppins, Playfair Display, EB Garamond, Syne…), no gradient text, no left-edge accent stripes.
- No identical card grids, no icon rows, no emoji, no stock "doctor", "patient" or "happy baby" imagery.
- No AI-generated or stock embryos, gametes, ultrasound, microscope views or clinical/patient scenes. AI is allowed only for mechanisms (hormones, cells, molecules) and only with the illustration-tab; stock only for non-medical atmosphere (hands, calendar, city), also tagged.
- No traffic-light evidence colours; no red outside of judgment.
- Pen marks, stamps and pen arrows live **inside** the video only, always next to their evidence — never in thumbnails (F13).
- No title case, no all-caps Literata.
- No channel intro / logo sting / animated bumper — not at the start, not after the hook. Videos open on Dr. Aksoy and go straight into content (decision 2026-10-16).

## Editorial Hard Rules (on-screen text)

- **Numbers & claims:** never invent figures, percentages, success rates or study names. Every on-screen figure traces to a cited source supplied in the script; otherwise render `— chiffre —` and flag it.
- **Source → scene (enforced):** every on-screen number, finding, verdict and citation is bound to `scene-facts.json` (`data-fact` / `data-ref`), each entry tied to a claim ID in the script's fact-checked `-sources.md` and, for papers, to a PMID. Citations are generated from PubMed, never typed. Run `node tools/facts.mjs all <project> --lang <fr|tr|en>` before `hyperframes check`; no render while `verify` fails. See `tools/README.md`.
- **No guarantees language** anywhere on screen (garanti, 100 %, assuré, miracle) except when it is the claim being struck.
- **Out of scope topics:** no PGT-A content, no gamete/embryo donation content.
- **No other clinics** named or recommended; no competitor logos.
- **Patient privacy (KVKK/GDPR):** footage and imaging carry no patient name, ID, date of birth or face unless documented consent exists; crop or blur scanner overlays.
- **Quotations from papers:** one short phrase (≤ 15 words) at most, attributed; paraphrase the rest.

## Aspect-Ratio Behaviour

| Treatment          | 16:9                                   | 9:16 (Shorts)                                  |
| ------------------ | -------------------------------------- | ---------------------------------------------- |
| Cover              | title flush left, kicker top-left      | title upper third, kicker above                |
| La promesse barrée | claim top, correction below, left-aligned | claim centred-left, correction below, larger |
| Le verdict         | stamp overlaps headline right          | stamp centred over headline                    |
| Le chiffre         | figure left, slip bottom-left          | figure centred, slip below (above UI zone)     |
| Le labo            | footage full-bleed, tab bottom-left    | footage cropped to subject, tab above UI zone  |
| Talking head       | lower-third left, side note right third | lower-third above UI zone, no side note       |
| Clôture            | line centred-left                      | line stacked, 3–4 lines                        |

## Assets

- **Objects (installed, 2026-10-17):** `assets/objects/` — two paper clips cut from a top-down photo of Dr. Aksoy's desk (see its README). Branded objects (calculator, glue) and red objects (scissors) are not used.
- **Fonts (installed):** `assets/fonts/` holds Literata variable (wght 200–900 + opsz 7–72, roman + italic) and IBM Plex Sans 400/600 as WOFF2, split into latin + latin-ext subsets (FR + TR verified). Link `assets/fonts/fonts.css` in index.html (or paste its @font-face block); family names are exactly 'Literata' and 'IBM Plex Sans'. IBM Plex Mono is renderer-bundled. Licence: SIL OFL 1.1 (OFL-*.txt beside the files). Fallbacks: Literata → Source Serif 4 → Georgia (never a sans); Plex Sans → system-ui. Proof: `test/font-testcard.png`.
- **Paper grain (installed):** `assets/textures/paper-grain-16x9.png` (1920×1080) and `paper-grain-9x16.png` (1080×1920) — neutral grey (mean 128) from a real A4 photo, lighting gradient removed. Use as a full-frame static layer: `mix-blend-mode: soft-light; opacity: .35` over `{colors.paper}`; never on lab surfaces, never moving. Preview: `test/paper-preview.png`.
- **Stamp mask (installed):** `assets/textures/stamp-mask.png` (1400×560, white + alpha). Ink-pressure variation calibrated to a real rubber-stamp impression (in-stroke density CV ≈ 0.22, ~5 % ink-starved specks, drier right edge), built from the real paper-fibre texture. Apply to the whole verdict-stamp box: `mask-image: url(assets/textures/stamp-mask.png); mask-size: 100% 100%;` plus `mix-blend-mode: multiply`. Flip it (`transform: scaleX(-1)` on a wrapper, or `mask-position`) when two stamps share a video so they don't look identical. CSS masks need the page served over http (HyperFrames preview/render do this) — they silently fail on file://. Reference: `test/stamp-test.png`.
- **Pen marks (installed):** `assets/pen/` — 14 real strokes drawn by Dr. Aksoy with markers, recoloured to `{colors.correcteur}` with the original ink density kept as alpha (2× resolution). `pen-library.json` lists id, type (strike / underline / loop / arrow / question), tool (round marker = 7 marks for body/claim sizes; chisel `wide-*` = 7 marks for display sizes) and reveal. Use as `<img class="pen">` (+ `pen--loop` or `pen--question`) with `assets/pen/pen.css`; position and size per frame, stretch strikes horizontally up to ~1.8× to fit the text. Never reuse the same mark id twice in a row within one video. Masks need http. Reference: `test/pen-test.png`. Do not generate pen marks programmatically.
- **Papers (installed, 2026-10-17):** `assets/papers/<paper>/ground-16x9.png` + `ground-9x16.png` for `recete`, `cizgili`, `lab-spiral`, `kareli`; geometry in `papers.json`; CSS in `papers.css`. Rebuilt from Dr. Aksoy's photographed papers by `tools/make_papers.py` (measured colours/rules; only the spiral binding is photographic). Use under the paper-grain layer (`opacity .30`). See § Series & Variety.
- **Footage (installed):** `assets/footage/lab/` (15 real lab stills, sensitive papers/labels already blurred) and `assets/footage/embryo/` (5 anonymous embryo stills, 1080×1080). Read `assets/footage/INDEX.md` first: it gives each file's content, best use and status (✅ ready / ⚠️ check / ⛔ do not publish). Stills get at most one slow push-in (scale 1.00→1.04 over the shot). Never use ⛔ files.

## Series & Variety (2026-10-17)

Every video shares the **identity** — red pen as judgment, verdict stamp, reference slip, Literata + Plex, the
phone floor, real assets only. What changes from video to video is the **material**: each video belongs to one
series, and each series has its own paper, photographed by Dr. Aksoy and rebuilt from measurements
(`tools/make_papers.py`; colours, rule pitch, weights and dash patterns measured from his prescription pad, ruled
notebook, spiral lab notebook and squared notebook; printed text, logo, contact details, handwriting and
show-through writing never copied — only the spiral binding is photographic).

| Series (FR · TR · EN) | Paper | Use it for | Reference scene |
|---|---|---|---|
| **mythe** — Le mythe · Mit avcısı · The myth | `a4` plain paper-grain | a claim, add-on or promise examined: strike + stamp | `example-era/` |
| **labo** — Au labo · Laboratuvardan · From the lab | `lab-spiral` | embryology / lab technique; real footage is the hero, laid on the page as a print | `example-series/labo/` |
| **questions** — Vos questions · Sorularınız · Your questions | `cizgili` | one patient question (generic wording, never an identifiable patient) | `example-series/questions/` |
| **chiffres** — Les chiffres · Rakamlar · The numbers | `kareli` | a study or rate; hand-ruled ledger snapped to the grid | `example-series/chiffres/` |
| **conseils** — Ce que je retiens · Aklınızda kalsın · What to remember | `recete` | practical take-aways / closing summary | `example-series/conseils/` |

**Rules**
- One **main paper** per video (= the series paper) + at most **one contrast paper** for a single segment (e.g. a
  `kareli` ledger inside a `mythe` video). Never three.
- Paper rules are **material**: low contrast, never red, never carry meaning, never used as text colour. They do not
  count as a palette hue.
- Text **sits on the rules**: use `assets/papers/papers.css` `.on-rule` (`--y` rule y, `--fs`, `--lh` = pitch);
  rule geometry per ground in `assets/papers/papers.json`. On `kareli`, every box snaps to the 54 px grid.
- `recete` is the stock of the prescription pad **without** its letterhead: never a patient name/diagnosis field,
  never a drug name or dose, never presented as a real prescription.
- Every project has a `look.json` (series, papers, first_graphic, layouts, pen_marks, stamp_flip). Layout variant
  ids live in `series.json` (built / spec). `node tools/variety.mjs check <project>` must pass before render; after
  the final render `node tools/variety.mjs log <project> --lang <fr|tr|en>` records it in
  `youtube-content/motion/look-log.json`.
- The gate fails when: the first graphic after Dr. Aksoy's hook repeats the previous video's; the pen-mark set is
  identical to the previous video's; or same series **and** identical layout set as one of the last 3 videos.
  It warns on the same series 3 times in a row. `node tools/variety.mjs status` lists series and built layouts not
  used lately — start there when choosing.
- A "spec" layout may be used once it is built; then set it to "built" in `series.json` with its example path.
- Built so far (2026-10-17): promesse-A/B, chiffre-A/B/C, verdict-A/B, labo-A/B, question-A, retenir-A — reference scenes in
  `example-era/`, `example-series/`, `example-layouts/`, each with its Shorts twin.

## Built Components (2026-10-17)

Every overlay the edit needs has a built, checked reference in `example-components/` (16:9 + `shorts/`), styled by
`assets/components/components.css` (link it after `papers.css`; put `class="oi-c"` on `#root`):

| Component | Reference | Rules that matter |
|---|---|---|
| lower-third | `talking-head` | first appearance of Dr. Aksoy only; slides in from the left edge, holds ~4 s, slides out; name + role per channel (TR: « Doç. Dr. » + « Kadın Hastalıkları, Doğum ve Üreme Tıbbı Uzmanı ») |
| side note | `talking-head` | ONE term or figure on the right third (portrait: top), never over the face; a figure carries its citation |
| CTA | `cta` | paper tab, ink thumb + bell + subscribe; one axis in, outline→filled state changes (real ink-tap foley), one axis out; never during the opening hook; no YouTube logo |
| chapter sheet | `chapitre` | the next sheet slides over the previous one in 0.6 s (power2.inOut); the covered sheet is dropped once hidden |
| signature line | `cloture` | the channel's closing sentence verbatim, Literata italic, one pen circle on « garanties / Garantiler / Guarantees »; channel handle under it |
| footage-tab / illustration-tab | `etiquettes` | footage-tab on real footage (what + source); illustration-tab on every AI / stock clip from its first to its last frame |
| paper clip | `example-series/conseils` | real clip from Dr. Aksoy's desk (`assets/objects/`) holding a card; never over text (`.clipped-left` / `.clipped` make room); max one object per frame |

The talking-head stills in these references are stand-ins: in a real edit `.foot` is Dr. Aksoy's camera clip.

## Reference Composition

`example-era/index.html` is the approved reference scene (claim → pen-strike → evidence → two figures + reference-slip → verdict-stamp, 10 s). Copy its structure, timings and CSS patterns for new scenes; change only the content.

## Pre-Render Self-Audit

- **Squint** — one Literata moment dominates each frame.
- **Pen** — red only as judgment; ≤ 1 mark per frame (strike + stamp pair max); § in every kicker.
- **Proof** — every figure and stamp has a reference on screen; no invented numbers.
- **Not-AI** — zero glow / gradient / glass / particle / ambient drift / bounce; no banned fonts.
- **Type** — italic = claim, roman = evidence; French spacing and « » correct.
- **Shorts** — `node tools/aspect.mjs <project>` then legibility/check on `<project>/shorts` (no text under the Shorts UI).
- **Phone** — `node tools/legibility.mjs <project>` passes (every visible text ≥ 40 px @1080); look at one frame scaled to 640×360 — everything still reads.
- **Privacy & scope** — no patient identifiers; no PGT-A / donation / competitor content.

## Known Gaps

- Pen library is small (14 marks). If a video needs more variety, ask Dr. Aksoy for another sheet rather than generating strokes.
- Turkish and Arabic cut-downs: Literata covers Turkish; Arabic would need a separate display face (e.g. a Naskh) and a mirrored layout — not specified here.
- Thumbnails are out of scope, and they must **not** borrow the pen/stamp vocabulary: compliance rule F13 (`youtube-content/02-compliance-checklist.md`) bans visual clickbait in thumbnails — red strikes/crosses, stamps, arrows, shocked faces. Thumbnails follow `10-thumbnail-production-library.md`; at most they share the palette and Literata.
