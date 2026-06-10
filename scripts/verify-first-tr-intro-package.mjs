import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";

const root = process.cwd();
const packagePath = "youtube-content/edit-packages/2026-06-09-tr-short-1-embriyo-kalitesi-intro-package.md";
const manifestPath = "youtube-content/motion/intro-pilot/MANIFEST.json";

const requiredPackageTokens = [
  "channel: tr",
  "intro-render: youtube-content/motion/intro-pilot/renders/intro-pilot-tr.mp4",
  "tupbebek.com",
  "3BB Embriyo Düşük Kalite mi? Panik Yapma",
  "scripted-intro-selected",
  "No guarantee language",
  "No success-rate promise",
];

const bannedPackagePatterns = [
  { label: "FR intro render", pattern: /intro-pilot-fr\.mp4/i },
  { label: "draksoyivf.com", pattern: /draksoyivf\.com/i },
  { label: "guaranteed", pattern: /\bguaranteed\b/i },
  { label: "miracle", pattern: /\bmiracle\b/i },
  { label: "burgundy palette", pattern: /#6B2D3E/i },
  { label: "gold palette", pattern: /#C9A96E/i },
  { label: "cream palette", pattern: /#FAF6EE/i },
];

const errors = [];

for (const file of [packagePath, manifestPath]) {
  if (!existsSync(join(root, file))) {
    errors.push(`${file} does not exist`);
  }
}

if (errors.length === 0) {
  const editPackage = readFileSync(join(root, packagePath), "utf8");
  const manifest = JSON.parse(readFileSync(join(root, manifestPath), "utf8"));
  const trMp4 = manifest.channels?.tr?.renders?.mp4;

  if (!trMp4) {
    errors.push("TR MP4 render is missing from MANIFEST.json");
  } else if (!existsSync(join(root, trMp4))) {
    errors.push(`${trMp4} does not exist`);
  }

  for (const token of requiredPackageTokens) {
    if (!editPackage.includes(token)) {
      errors.push(`Missing package token: ${token}`);
    }
  }

  for (const { label, pattern } of bannedPackagePatterns) {
    if (pattern.test(editPackage)) {
      errors.push(`Banned package content found: ${label}`);
    }
  }
}

if (errors.length > 0) {
  console.error("First TR intro edit package verification failed.");
  for (const error of errors) {
    console.error(`- ${error}`);
  }
  process.exit(1);
}

console.log("First TR intro edit package verification passed.");
