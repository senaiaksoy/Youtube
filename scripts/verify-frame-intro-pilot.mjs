import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";

const root = process.cwd();

const requiredFiles = [
  "youtube-content/motion/intro-pilot/DESIGN.md",
  "youtube-content/motion/intro-pilot/FRAME.md",
  "youtube-content/motion/intro-pilot/MANIFEST.json",
  "youtube-content/motion/intro-pilot/prototype/index.html",
  "youtube-content/motion/intro-pilot/prototype/styles.css",
  "youtube-content/motion/intro-pilot/prototype/intro.js",
  "youtube-content/motion/intro-pilot/renders/intro-pilot-tr.mp4",
  "youtube-content/motion/intro-pilot/renders/intro-pilot-tr.webm",
  "youtube-content/motion/intro-pilot/renders/intro-pilot-fr.mp4",
  "youtube-content/motion/intro-pilot/renders/intro-pilot-fr.webm",
];

const renderedFiles = [
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
  "#efefef",
  "#0f2b4b",
  "#222222",
  "tupbebek.com",
  "draksoyivf.com",
  "Tüp Bebekte Doğru Bilgi",
  "Dr. Senai Aksoy | Üreme Sağlığı",
  "Comprendre la FIV avec clarté",
  "Dr. Senai Aksoy | FIV à Istanbul",
  "no promotional medical claims",
  "no burgundy/gold/cream palette",
  "edited-to-scheduled",
  "youtube-content/motion/intro-pilot/renders/intro-pilot-tr.mp4",
  "youtube-content/motion/intro-pilot/renders/intro-pilot-fr.mp4",
];

const bannedRenderedPatterns = [
  { label: "#6B2D3E", pattern: /#6B2D3E/i },
  { label: "#C9A96E", pattern: /#C9A96E/i },
  { label: "#FAF6EE", pattern: /#FAF6EE/i },
  { label: "border-radius: 50%", pattern: /border-radius\s*:\s*50%/i },
  { label: "% 15", pattern: /% 15/ },
  { label: "miracle", pattern: /\bmiracle\b/i },
  { label: "secret", pattern: /\bsecret\b/i },
  { label: "shocking", pattern: /\bshocking\b/i },
  { label: "guaranteed", pattern: /\bguaranteed\b/i },
  { label: "success rate", pattern: /\bsuccess rate\b/i },
];

const errors = [];
const missingFiles = requiredFiles.filter((file) => !existsSync(join(root, file)));

if (missingFiles.length > 0) {
  errors.push({
    title: "Missing required files",
    items: missingFiles,
  });
}

const readableFiles = requiredFiles.filter((file) => !missingFiles.includes(file));
const allCorpus = readableFiles
  .map((file) => readFileSync(join(root, file), "utf8"))
  .join("\n");

const missingTokens = requiredTokens.filter((token) => !allCorpus.includes(token));

if (missingTokens.length > 0) {
  errors.push({
    title: "Missing required package tokens",
    items: missingTokens,
  });
}

const renderedCorpus = renderedFiles
  .filter((file) => !missingFiles.includes(file))
  .map((file) => readFileSync(join(root, file), "utf8"))
  .join("\n");

const bannedMatches = bannedRenderedPatterns
  .filter(({ pattern }) => pattern.test(renderedCorpus))
  .map(({ label }) => label);

if (bannedMatches.length > 0) {
  errors.push({
    title: "Banned prototype content found",
    items: bannedMatches,
  });
}

const manifestPath = join(root, "youtube-content/motion/intro-pilot/MANIFEST.json");

if (existsSync(manifestPath)) {
  let manifest;

  try {
    manifest = JSON.parse(readFileSync(manifestPath, "utf8"));
  } catch (error) {
    errors.push({
      title: "Invalid intro manifest JSON",
      items: [error.message],
    });
  }

  if (manifest) {
    const manifestErrors = [];

    if (manifest.productionUse?.pipelineStage !== "edited-to-scheduled") {
      manifestErrors.push("productionUse.pipelineStage must be edited-to-scheduled");
    }

    for (const channel of ["tr", "fr"]) {
      const config = manifest.channels?.[channel];

      if (!config) {
        manifestErrors.push(`channels.${channel} is missing`);
        continue;
      }

      for (const format of ["mp4", "webm"]) {
        const renderPath = config.renders?.[format];

        if (!renderPath) {
          manifestErrors.push(`channels.${channel}.renders.${format} is missing`);
          continue;
        }

        if (!existsSync(join(root, renderPath))) {
          manifestErrors.push(`${renderPath} does not exist`);
        }
      }
    }

    if (manifestErrors.length > 0) {
      errors.push({
        title: "Intro manifest verification failed",
        items: manifestErrors,
      });
    }
  }
}

if (errors.length > 0) {
  console.error("Frame intro pilot verification failed.");
  for (const group of errors) {
    console.error(`\n${group.title}:`);
    for (const item of group.items) {
      console.error(`- ${item}`);
    }
  }
  process.exit(1);
}

console.log("Frame intro pilot verification passed.");
