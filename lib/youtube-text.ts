const MOJIBAKE_PATTERN = /[ÃÅÄâ]/;

function countSuspiciousChars(value: string): number {
  return (value.match(/[ÃÅÄâ�]/g) ?? []).length;
}

function repairMojibakeOnce(value: string): string {
  return Buffer.from(value, 'latin1').toString('utf8');
}

export function normalizeYoutubeText(value: string): string {
  let current = value.normalize('NFC');

  for (let i = 0; i < 2; i += 1) {
    if (!MOJIBAKE_PATTERN.test(current)) break;

    const repaired = repairMojibakeOnce(current).normalize('NFC');
    if (countSuspiciousChars(repaired) >= countSuspiciousChars(current)) break;
    current = repaired;
  }

  return current;
}

export function normalizeYoutubeTextList(values: string[] | null | undefined): string[] | null | undefined {
  if (!values) return values;
  return values.map((value) => normalizeYoutubeText(value));
}
