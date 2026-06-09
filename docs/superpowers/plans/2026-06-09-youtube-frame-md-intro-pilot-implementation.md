# YouTube Frame.md Intro Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first reusable 15-second intro pilot package with `DESIGN.md`, `FRAME.md`, a static TR/FR HTML preview, and a lightweight verification script.

**Architecture:** Keep the pilot isolated under `youtube-content/motion/intro-pilot/` so it does not affect the Next.js app or YouTube API tooling. The Markdown files are the source of truth; the HTML/CSS/JS preview is a visual prototype that reads like the future HyperFrames composition but stays dependency-free for the first pass.

**Tech Stack:** Markdown, static HTML/CSS/vanilla JavaScript, Node.js filesystem checks, optional in-app Browser visual review.

---

## Scope Check

The approved design covers one subsystem: a reusable YouTube intro motion pilot. It does not include long-form editing, upload automation, voiceover, thumbnail redesign, or a full HyperFrames render pipeline. No decomposition into separate plans is needed.

## File Structure

- Create: `youtube-content/motion/intro-pilot/DESIGN.md`
  - Brand and visual system source of truth for the pilot.
- Create: `youtube-content/motion/intro-pilot/FRAME.md`
  - Motion timing, composition, copy slots, and skin mapping source of truth.
- Create: `youtube-content/motion/intro-pilot/prototype/index.html`
  - Static visual preview with TR/FR skin toggle and animated 15-second sequence.
- Create: `youtube-content/motion/intro-pilot/prototype/styles.css`
  - Prototype styling, color tokens, responsive text rules, and animation keyframes.
- Create: `youtube-content/motion/intro-pilot/prototype/intro.js`
  - Small controller for skin switching, replay, and timeline labels.
- Create: `scripts/verify-frame-intro-pilot.mjs`
  - Dependency-free verification script for required files, required tokens, and banned language.
- Modify: none outside the new script and isolated pilot folder.

## Task 1: Create The Pilot Brand Spec

**Files:**
- Create: `youtube-content/motion/intro-pilot/DESIGN.md`

- [ ] **Step 1: Create the directory**

Run:

```powershell
New-Item -ItemType Directory -Force -Path "D:\A-klasör\Youtube\youtube-content\motion\intro-pilot"
```

Expected: directory exists with no error.

- [ ] **Step 2: Add `DESIGN.md`**

Create `youtube-content/motion/intro-pilot/DESIGN.md` with this content:

```markdown
# YouTube Intro Pilot DESIGN.md

## Purpose
This document defines the visual identity for the 15-second YouTube/Shorts intro
pilot. It is the brand reference for both channel skins:

- TR skin: connected to `tupbebek.com`
- FR skin: connected to `draksoyivf.com`

The motion system is shared. Color, identity line, and language change by skin.

## Shared Identity
The intro should feel calm, clinical, educational, and precise. It should have
enough motion energy for Shorts, but it must not feel like clickbait.

Core qualities:
- evidence-oriented
- readable on mobile
- calm but not static
- medical without being cold
- human without using emotional leverage

## TR Skin: tupbebek.com

### Role
The TR variant supports an educational fertility information portal. It should
feel like a structured guide to correct information.

### Colors
- Primary blue: `#2563a8`
- Deep blue: `#1a4d7a`
- Support green: `#3a8a66`
- Light blue surface: `#f0f7ff`
- White: `#ffffff`
- Text dark: `#0f2b4b`

### Typography
- Primary title: Inter or Manrope, bold, clear, sentence case.
- Identity line: Inter or Manrope, medium weight.
- Micro labels: Inter or Manrope, uppercase only when short.

### Surfaces
- Light blue or white base.
- Fine blue line motifs.
- Small green accent only for secondary emphasis.

### Default Copy
- Main title: `Tup Bebekte Dogru Bilgi`
- Identity line: `Dr. Senai Aksoy | Ureme Sagligi`
- Site cue: `tupbebek.com`

## FR Skin: draksoyivf.com

### Role
The FR variant supports an international IVF clinic and patient-care context. It
should feel clinical, calm, and reassuring.

### Colors
- Deep clinic blue: `#094183`
- Rose accent: `#e8578a`
- Pale blue-grey: `#dce9f3`
- White: `#ffffff`
- Soft grey: `#efefef`
- Text dark: `#222222`

### Typography
- Primary title: Inter or Manrope, bold, clear, sentence case.
- Identity line: Inter or Manrope, medium weight.
- Micro labels: Inter or Manrope, restrained and sparse.

### Surfaces
- White or deep-blue base depending on contrast.
- Rose accent used sparingly, never as a warning signal.
- Fine clinical line motifs and soft panel transitions.

### Default Copy
- Main title: `Comprendre la FIV avec clarte`
- Identity line: `Dr. Senai Aksoy | FIV a Istanbul`
- Site cue: `draksoyivf.com`

## Motifs
Allowed motifs:
- abstract cellular arcs
- fine lab-grid lines
- soft path drawing
- measured wipe transitions
- small dots used as data or timeline points

Forbidden motifs:
- baby imagery
- pregnant belly imagery
- patient faces
- before/after visuals
- warning icons
- red circles or arrows
- exaggerated reactions

## Motion Tone
- calm clinical editorial
- one small Shorts-energy lift during the title entrance
- no bouncing, shaking, flashing, or alarm-like movement
- final frame must hold long enough to read

## Reusable Slots
- `{{channel}}`: `tr` or `fr`
- `{{title}}`: per-video title
- `{{identityLine}}`: Dr. Aksoy line for the chosen skin
- `{{siteCue}}`: linked site

## Compliance Guardrails
Do not include:
- success-rate claims
- guarantee language
- prices or discounts
- clinic address
- patient stories
- miracle, secret, shocking, guaranteed, or similar words
- promotional medical claims
```

- [ ] **Step 3: Review the file**

Run:

```powershell
Get-Content "D:\A-klasör\Youtube\youtube-content\motion\intro-pilot\DESIGN.md"
```

Expected: the file prints with both TR and FR skin sections, and no burgundy/gold/cream palette appears.

- [ ] **Step 4: Commit Task 1**

Run:

```powershell
git add -- "youtube-content/motion/intro-pilot/DESIGN.md"
git commit -m "Add intro pilot design spec" -- "youtube-content/motion/intro-pilot/DESIGN.md"
```

Expected: a commit containing only `DESIGN.md`.

## Task 2: Create The Frame Motion Spec

**Files:**
- Create: `youtube-content/motion/intro-pilot/FRAME.md`

- [ ] **Step 1: Add `FRAME.md`**

Create `youtube-content/motion/intro-pilot/FRAME.md` with this content:

```markdown
# YouTube Intro Pilot FRAME.md

## Purpose
This document defines the 15-second motion structure for the reusable
YouTube/Shorts intro pilot.

## Canvas
- Aspect ratio: 16:9
- Design size: 1920 x 1080
- Safe text area: keep primary text inside the central 80% width and 70% height
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

Default TR title:
`Tup Bebekte Dogru Bilgi`

Default FR title:
`Comprendre la FIV avec clarte`

### Beat 3: Identity Line, 8.0s-12.0s
The title reduces slightly and the identity line appears.

Motion:
- title scales down to 92% between 8.0s and 8.4s
- identity line fades in between 8.3s and 9.0s
- site cue appears between 9.1s and 9.5s
- hold the full composition until 12.0s

Default TR identity:
`Dr. Senai Aksoy | Ureme Sagligi`

Default FR identity:
`Dr. Senai Aksoy | FIV a Istanbul`

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
- `title`: `Tup Bebekte Dogru Bilgi`
- `identityLine`: `Dr. Senai Aksoy | Ureme Sagligi`
- `siteCue`: `tupbebek.com`
- primary: `#2563a8`
- secondary: `#1a4d7a`
- accent: `#3a8a66`
- surface: `#f0f7ff`

### FR
- `channel`: `fr`
- `title`: `Comprendre la FIV avec clarte`
- `identityLine`: `Dr. Senai Aksoy | FIV a Istanbul`
- `siteCue`: `draksoyivf.com`
- primary: `#094183`
- secondary: `#dce9f3`
- accent: `#e8578a`
- surface: `#ffffff`

## Motion Guardrails
- no shake
- no bounce
- no flashing
- no warning iconography
- no red circle emphasis
- no success-rate claim
- no guarantee language

## Preview Requirements
- preview both TR and FR skins
- check desktop 16:9 composition
- check mobile readability
- capture final-frame screenshot for both skins
- confirm the rejected burgundy/gold/cream palette is not used
```

- [ ] **Step 2: Review the file**

Run:

```powershell
Get-Content "D:\A-klasör\Youtube\youtube-content\motion\intro-pilot\FRAME.md"
```

Expected: the file prints the four beats, TR mapping, FR mapping, and preview requirements.

- [ ] **Step 3: Commit Task 2**

Run:

```powershell
git add -- "youtube-content/motion/intro-pilot/FRAME.md"
git commit -m "Add intro pilot frame spec" -- "youtube-content/motion/intro-pilot/FRAME.md"
```

Expected: a commit containing only `FRAME.md`.

## Task 3: Build The Static Prototype

**Files:**
- Create: `youtube-content/motion/intro-pilot/prototype/index.html`
- Create: `youtube-content/motion/intro-pilot/prototype/styles.css`
- Create: `youtube-content/motion/intro-pilot/prototype/intro.js`

- [ ] **Step 1: Create the prototype directory**

Run:

```powershell
New-Item -ItemType Directory -Force -Path "D:\A-klasör\Youtube\youtube-content\motion\intro-pilot\prototype"
```

Expected: directory exists with no error.

- [ ] **Step 2: Add `index.html`**

Create `youtube-content/motion/intro-pilot/prototype/index.html` with this content:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>YouTube Intro Pilot</title>
    <link rel="stylesheet" href="./styles.css">
  </head>
  <body data-skin="tr">
    <main class="page-shell">
      <section class="preview-toolbar" aria-label="Preview controls">
        <div>
          <p class="eyebrow">Frame.md intro pilot</p>
          <h1>15-second shared intro with TR/FR skins</h1>
        </div>
        <div class="toolbar-actions">
          <button type="button" data-skin-button="tr" aria-pressed="true">TR</button>
          <button type="button" data-skin-button="fr" aria-pressed="false">FR</button>
          <button type="button" data-replay>Replay</button>
        </div>
      </section>

      <section class="stage-wrap" aria-label="Intro preview">
        <div class="stage" data-stage>
          <div class="motif motif-a"></div>
          <div class="motif motif-b"></div>
          <div class="dot dot-one"></div>
          <div class="dot dot-two"></div>
          <div class="dot dot-three"></div>

          <div class="title-group">
            <p class="site-cue" data-site-cue>tupbebek.com</p>
            <h2 data-title>Tup Bebekte Dogru Bilgi</h2>
            <div class="accent-line"></div>
            <p class="identity" data-identity>Dr. Senai Aksoy | Ureme Sagligi</p>
          </div>

          <div class="transition-panel"></div>
          <div class="time-label" data-time-label>0-3s Brand field</div>
        </div>
      </section>
    </main>

    <script src="./intro.js"></script>
  </body>
</html>
```

- [ ] **Step 3: Add `styles.css`**

Create `youtube-content/motion/intro-pilot/prototype/styles.css` with this content:

```css
:root {
  --page-bg: #f7f9fc;
  --ink: #0f172a;
  --muted: #64748b;
  --stage-surface: #f0f7ff;
  --primary: #2563a8;
  --secondary: #1a4d7a;
  --accent: #3a8a66;
  --soft: #ffffff;
}

body[data-skin="fr"] {
  --stage-surface: #ffffff;
  --primary: #094183;
  --secondary: #dce9f3;
  --accent: #e8578a;
  --ink: #222222;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  min-height: 100vh;
  background: var(--page-bg);
  color: var(--ink);
  font-family: Inter, Manrope, Arial, sans-serif;
}

.page-shell {
  width: min(1180px, calc(100vw - 32px));
  margin: 0 auto;
  padding: 28px 0;
}

.preview-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  margin-bottom: 18px;
}

.eyebrow {
  margin: 0 0 4px;
  color: var(--muted);
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
}

h1 {
  margin: 0;
  font-size: 24px;
  line-height: 1.2;
}

.toolbar-actions {
  display: flex;
  gap: 8px;
}

button {
  border: 1px solid rgba(15, 23, 42, 0.16);
  border-radius: 8px;
  background: #ffffff;
  color: var(--ink);
  cursor: pointer;
  font: inherit;
  font-weight: 700;
  padding: 9px 12px;
}

button[aria-pressed="true"] {
  background: var(--primary);
  border-color: var(--primary);
  color: #ffffff;
}

.stage-wrap {
  width: 100%;
}

.stage {
  position: relative;
  aspect-ratio: 16 / 9;
  overflow: hidden;
  background:
    linear-gradient(135deg, color-mix(in srgb, var(--stage-surface), #ffffff 18%), var(--stage-surface)),
    var(--stage-surface);
  border: 1px solid rgba(15, 23, 42, 0.12);
  border-radius: 8px;
  box-shadow: 0 18px 50px rgba(15, 23, 42, 0.12);
}

.stage::before {
  content: "";
  position: absolute;
  inset: 9%;
  border: 1px solid color-mix(in srgb, var(--primary), transparent 78%);
  opacity: 0;
  animation: fieldIn 15s linear forwards;
}

.motif {
  position: absolute;
  border: 2px solid color-mix(in srgb, var(--primary), transparent 35%);
  border-left-color: transparent;
  border-bottom-color: transparent;
  border-radius: 999px;
  opacity: 0;
  transform: rotate(-18deg) scale(0.86);
  animation: motifDraw 15s ease forwards;
}

.motif-a {
  width: 44%;
  height: 68%;
  left: -10%;
  top: 12%;
}

.motif-b {
  width: 34%;
  height: 52%;
  right: -8%;
  bottom: 7%;
  animation-delay: 0.18s;
}

.dot {
  position: absolute;
  width: 12px;
  height: 12px;
  border-radius: 999px;
  background: var(--accent);
  opacity: 0;
  animation: dotIn 15s ease forwards;
}

.dot-one {
  left: 18%;
  top: 24%;
  animation-delay: 0.4s;
}

.dot-two {
  left: 26%;
  bottom: 24%;
  animation-delay: 0.58s;
}

.dot-three {
  right: 23%;
  top: 30%;
  animation-delay: 0.76s;
}

.title-group {
  position: absolute;
  left: 10%;
  right: 10%;
  top: 50%;
  transform: translateY(-42%);
  z-index: 2;
}

.site-cue {
  margin: 0 0 14px;
  color: var(--accent);
  font-size: clamp(14px, 1.8vw, 24px);
  font-weight: 800;
  opacity: 0;
  animation: siteCue 15s ease forwards;
}

h2 {
  max-width: 980px;
  margin: 0;
  color: var(--primary);
  font-size: clamp(38px, 7vw, 104px);
  line-height: 1.02;
  letter-spacing: 0;
  opacity: 0;
  transform: translateY(28px);
  animation: titleIn 15s cubic-bezier(.2, .8, .2, 1) forwards;
}

.accent-line {
  width: 0;
  height: 5px;
  margin-top: 24px;
  background: var(--accent);
  border-radius: 999px;
  animation: accentLine 15s ease forwards;
}

.identity {
  margin: 24px 0 0;
  color: var(--ink);
  font-size: clamp(17px, 2.2vw, 30px);
  font-weight: 700;
  opacity: 0;
  animation: identityIn 15s ease forwards;
}

.transition-panel {
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent, color-mix(in srgb, var(--primary), transparent 88%));
  transform: translateX(100%);
  animation: transitionPanel 15s ease forwards;
}

.time-label {
  position: absolute;
  right: 24px;
  bottom: 20px;
  z-index: 3;
  color: color-mix(in srgb, var(--ink), transparent 30%);
  font-size: 13px;
  font-weight: 800;
}

.stage.replay,
.stage.replay * {
  animation: none !important;
}

@keyframes fieldIn {
  0%, 2% { opacity: 0; transform: scale(0.98); }
  7%, 100% { opacity: 1; transform: scale(1); }
}

@keyframes motifDraw {
  0%, 3% { opacity: 0; transform: rotate(-18deg) scale(0.86); }
  14%, 100% { opacity: 0.7; transform: rotate(-18deg) scale(1); }
}

@keyframes dotIn {
  0%, 4% { opacity: 0; transform: scale(0.4); }
  11%, 100% { opacity: 0.85; transform: scale(1); }
}

@keyframes titleIn {
  0%, 20% { opacity: 0; transform: translateY(28px) scale(1); }
  25%, 53% { opacity: 1; transform: translateY(0) scale(1); }
  56%, 100% { opacity: 1; transform: translateY(0) scale(0.92); }
}

@keyframes accentLine {
  0%, 26% { width: 0; opacity: 0; }
  30%, 100% { width: min(320px, 52%); opacity: 1; }
}

@keyframes identityIn {
  0%, 54% { opacity: 0; transform: translateY(12px); }
  60%, 100% { opacity: 1; transform: translateY(0); }
}

@keyframes siteCue {
  0%, 58% { opacity: 0; transform: translateY(8px); }
  64%, 100% { opacity: 1; transform: translateY(0); }
}

@keyframes transitionPanel {
  0%, 80% { transform: translateX(100%); opacity: 0; }
  88% { transform: translateX(0); opacity: 1; }
  96%, 100% { transform: translateX(-100%); opacity: 0.45; }
}

@media (max-width: 720px) {
  .preview-toolbar {
    align-items: flex-start;
    flex-direction: column;
  }

  .toolbar-actions {
    width: 100%;
  }

  button {
    flex: 1;
  }

  .title-group {
    left: 8%;
    right: 8%;
  }
}
```

- [ ] **Step 4: Add `intro.js`**

Create `youtube-content/motion/intro-pilot/prototype/intro.js` with this content:

```javascript
const skins = {
  tr: {
    title: "Tup Bebekte Dogru Bilgi",
    identity: "Dr. Senai Aksoy | Ureme Sagligi",
    siteCue: "tupbebek.com",
  },
  fr: {
    title: "Comprendre la FIV avec clarte",
    identity: "Dr. Senai Aksoy | FIV a Istanbul",
    siteCue: "draksoyivf.com",
  },
};

const body = document.body;
const stage = document.querySelector("[data-stage]");
const title = document.querySelector("[data-title]");
const identity = document.querySelector("[data-identity]");
const siteCue = document.querySelector("[data-site-cue]");
const timeLabel = document.querySelector("[data-time-label]");
const skinButtons = document.querySelectorAll("[data-skin-button]");
const replayButton = document.querySelector("[data-replay]");

function applySkin(skin) {
  const copy = skins[skin];
  body.dataset.skin = skin;
  title.textContent = copy.title;
  identity.textContent = copy.identity;
  siteCue.textContent = copy.siteCue;

  skinButtons.forEach((button) => {
    button.setAttribute("aria-pressed", String(button.dataset.skinButton === skin));
  });

  replay();
}

function replay() {
  stage.classList.add("replay");
  window.requestAnimationFrame(() => {
    window.requestAnimationFrame(() => {
      stage.classList.remove("replay");
    });
  });
}

function updateTimeLabel() {
  const seconds = Math.floor((performance.now() / 1000) % 15);

  if (seconds < 3) {
    timeLabel.textContent = "0-3s Brand field";
  } else if (seconds < 8) {
    timeLabel.textContent = "3-8s Main title";
  } else if (seconds < 12) {
    timeLabel.textContent = "8-12s Identity line";
  } else {
    timeLabel.textContent = "12-15s Transition out";
  }

  window.requestAnimationFrame(updateTimeLabel);
}

skinButtons.forEach((button) => {
  button.addEventListener("click", () => applySkin(button.dataset.skinButton));
});

replayButton.addEventListener("click", replay);
updateTimeLabel();
```

- [ ] **Step 5: Open the prototype manually**

Open this local file in a browser:

```text
D:\A-klasör\Youtube\youtube-content\motion\intro-pilot\prototype\index.html
```

Expected:
- TR skin loads first.
- TR button is active.
- FR button switches title, identity, site cue, and colors.
- Replay restarts the animation.
- Text does not overflow the 16:9 stage.

- [ ] **Step 6: Commit Task 3**

Run:

```powershell
git add -- "youtube-content/motion/intro-pilot/prototype/index.html" "youtube-content/motion/intro-pilot/prototype/styles.css" "youtube-content/motion/intro-pilot/prototype/intro.js"
git commit -m "Add intro pilot static prototype" -- "youtube-content/motion/intro-pilot/prototype/index.html" "youtube-content/motion/intro-pilot/prototype/styles.css" "youtube-content/motion/intro-pilot/prototype/intro.js"
```

Expected: a commit containing only the three prototype files.

## Task 4: Add Dependency-Free Verification

**Files:**
- Create: `scripts/verify-frame-intro-pilot.mjs`

- [ ] **Step 1: Add the verification script**

Create `scripts/verify-frame-intro-pilot.mjs` with this content:

```javascript
import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";

const root = process.cwd();

const requiredFiles = [
  "youtube-content/motion/intro-pilot/DESIGN.md",
  "youtube-content/motion/intro-pilot/FRAME.md",
  "youtube-content/motion/intro-pilot/prototype/index.html",
  "youtube-content/motion/intro-pilot/prototype/styles.css",
  "youtube-content/motion/intro-pilot/prototype/intro.js",
];

const requiredTokens = [
  "#2563a8",
  "#1a4d7a",
  "#3a8a66",
  "#f0f7ff",
  "#094183",
  "#e8578a",
  "tupbebek.com",
  "draksoyivf.com",
  "Tup Bebekte Dogru Bilgi",
  "Comprendre la FIV avec clarte",
];

const bannedPatterns = [
  /\bmiracle\b/i,
  /\bsecret\b/i,
  /\bshocking\b/i,
  /\bguaranteed\b/i,
  /\bsuccess rate\b/i,
  /#6B2D3E/i,
  /#C9A96E/i,
  /#FAF6EE/i,
];

const missingFiles = requiredFiles.filter((file) => !existsSync(join(root, file)));
if (missingFiles.length > 0) {
  console.error("Missing required files:");
  for (const file of missingFiles) console.error(`- ${file}`);
  process.exit(1);
}

const allCorpus = requiredFiles
  .map((file) => readFileSync(join(root, file), "utf8"))
  .join("\n");

const missingTokens = requiredTokens.filter((token) => !allCorpus.includes(token));
if (missingTokens.length > 0) {
  console.error("Missing required tokens:");
  for (const token of missingTokens) console.error(`- ${token}`);
  process.exit(1);
}

const renderedFiles = [
  "youtube-content/motion/intro-pilot/prototype/index.html",
  "youtube-content/motion/intro-pilot/prototype/styles.css",
  "youtube-content/motion/intro-pilot/prototype/intro.js",
];

const renderedCorpus = renderedFiles
  .map((file) => readFileSync(join(root, file), "utf8"))
  .join("\n");

const bannedHits = bannedPatterns.filter((pattern) => pattern.test(renderedCorpus));
if (bannedHits.length > 0) {
  console.error("Banned language or rejected palette found:");
  for (const pattern of bannedHits) console.error(`- ${pattern}`);
  process.exit(1);
}

console.log("Frame intro pilot verification passed.");
```

- [ ] **Step 2: Run verification**

Run:

```powershell
node scripts/verify-frame-intro-pilot.mjs
```

Expected:

```text
Frame intro pilot verification passed.
```

- [ ] **Step 3: Commit Task 4**

Run:

```powershell
git add -- "scripts/verify-frame-intro-pilot.mjs"
git commit -m "Add intro pilot verification script" -- "scripts/verify-frame-intro-pilot.mjs"
```

Expected: a commit containing only the verification script.

## Task 5: Visual Review And Final Adjustments

**Files:**
- Modify if needed: `youtube-content/motion/intro-pilot/prototype/styles.css`
- Modify if needed: `youtube-content/motion/intro-pilot/prototype/intro.js`
- Modify if needed: `youtube-content/motion/intro-pilot/DESIGN.md`
- Modify if needed: `youtube-content/motion/intro-pilot/FRAME.md`

- [ ] **Step 1: Use Browser or a local browser to inspect the prototype**

Open:

```text
D:\A-klasör\Youtube\youtube-content\motion\intro-pilot\prototype\index.html
```

Check:
- TR skin uses blue/light-blue/green, not burgundy/gold/cream.
- FR skin uses deep blue/rose, not burgundy/gold/cream.
- title is readable at desktop size.
- title is readable when the browser window is narrow.
- identity line appears after the title.
- final transition begins after the composition has held long enough to read.

- [ ] **Step 2: If text overflows, tighten the CSS**

If either title overflows, edit the `h2` rule in `styles.css` to this exact rule:

```css
h2 {
  max-width: 980px;
  margin: 0;
  color: var(--primary);
  font-size: clamp(34px, 6.4vw, 96px);
  line-height: 1.04;
  letter-spacing: 0;
  overflow-wrap: anywhere;
  opacity: 0;
  transform: translateY(28px);
  animation: titleIn 15s cubic-bezier(.2, .8, .2, 1) forwards;
}
```

- [ ] **Step 3: If the FR skin feels too stark, tune the stage background**

If FR reads too empty, edit the `.stage` background rule in `styles.css` to this exact rule:

```css
.stage {
  position: relative;
  aspect-ratio: 16 / 9;
  overflow: hidden;
  background:
    radial-gradient(circle at 82% 24%, color-mix(in srgb, var(--accent), transparent 88%), transparent 30%),
    linear-gradient(135deg, color-mix(in srgb, var(--stage-surface), #ffffff 18%), var(--stage-surface)),
    var(--stage-surface);
  border: 1px solid rgba(15, 23, 42, 0.12);
  border-radius: 8px;
  box-shadow: 0 18px 50px rgba(15, 23, 42, 0.12);
}
```

- [ ] **Step 4: Re-run verification**

Run:

```powershell
node scripts/verify-frame-intro-pilot.mjs
```

Expected:

```text
Frame intro pilot verification passed.
```

- [ ] **Step 5: Commit visual adjustments if any were made**

If Step 2 or Step 3 changed files, run:

```powershell
git add -- "youtube-content/motion/intro-pilot"
git commit -m "Refine intro pilot visual preview" -- "youtube-content/motion/intro-pilot"
```

Expected: a commit containing only pilot preview/spec refinements.

## Task 6: Final Verification And Handoff

**Files:**
- Read: `youtube-content/motion/intro-pilot/DESIGN.md`
- Read: `youtube-content/motion/intro-pilot/FRAME.md`
- Read: `youtube-content/motion/intro-pilot/prototype/index.html`
- Read: `scripts/verify-frame-intro-pilot.mjs`

- [ ] **Step 1: Run the verification script**

Run:

```powershell
node scripts/verify-frame-intro-pilot.mjs
```

Expected:

```text
Frame intro pilot verification passed.
```

- [ ] **Step 2: Confirm committed files**

Run:

```powershell
git log --oneline -- "youtube-content/motion/intro-pilot" "scripts/verify-frame-intro-pilot.mjs"
```

Expected: commits for the design spec, frame spec, static prototype, and verification script.

- [ ] **Step 3: Confirm no unrelated files are staged**

Run:

```powershell
git diff --cached --name-only
```

Expected: no output.

- [ ] **Step 4: Report the output paths**

Report these paths to the user:

```text
D:\A-klasör\Youtube\youtube-content\motion\intro-pilot\DESIGN.md
D:\A-klasör\Youtube\youtube-content\motion\intro-pilot\FRAME.md
D:\A-klasör\Youtube\youtube-content\motion\intro-pilot\prototype\index.html
D:\A-klasör\Youtube\scripts\verify-frame-intro-pilot.mjs
```

## Self-Review Checklist

- Spec coverage: tasks create `DESIGN.md`, `FRAME.md`, TR/FR skins, static prototype, verification, and visual review.
- Rejected palette: verification blocks the old burgundy/gold/cream hex values.
- Site linkage: both `tupbebek.com` and `draksoyivf.com` are required tokens.
- Safety: verification blocks common sensational wording and the specs list compliance guardrails.
- Scope: no long-form editing, upload automation, voiceover, or full HyperFrames render is included.
