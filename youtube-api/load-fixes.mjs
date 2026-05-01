import fs from 'fs';

const MOJIBAKE_PATTERN = /[ÃÅÄâ]/;

function countSuspiciousChars(value) {
  return (value.match(/[ÃÅÄâ�]/g) ?? []).length;
}

function normalizeText(value) {
  let current = value.normalize('NFC');

  for (let i = 0; i < 2; i += 1) {
    if (!MOJIBAKE_PATTERN.test(current)) break;

    const repaired = Buffer.from(current, 'latin1').toString('utf8').normalize('NFC');
    if (countSuspiciousChars(repaired) >= countSuspiciousChars(current)) break;
    current = repaired;
  }

  return current;
}

function normalizeValue(value) {
  if (typeof value === 'string') return normalizeText(value);
  if (Array.isArray(value)) return value.map((item) => normalizeValue(item));
  if (value && typeof value === 'object') {
    return Object.fromEntries(
      Object.entries(value).map(([key, item]) => [key, normalizeValue(item)])
    );
  }
  return value;
}

export function loadFixes(filePath) {
  const raw = JSON.parse(fs.readFileSync(filePath, 'utf8'));
  return normalizeValue(raw);
}
