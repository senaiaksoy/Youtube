const GOOGLE_TRANSLATE_API_KEY = process.env.GOOGLE_TRANSLATE_API_KEY || '';

interface TranslateResult {
  translatedText: string;
}

/**
 * Google Cloud Translation API v2 ile metin çevirisi yapar.
 * Kaynak dil otomatik algılanır.
 */
export async function translateText(
  text: string,
  targetLang: string
): Promise<string> {
  if (!text.trim()) return text;
  if (!GOOGLE_TRANSLATE_API_KEY) {
    console.warn('GOOGLE_TRANSLATE_API_KEY not set — returning original text');
    return text;
  }

  const url = `https://translation.googleapis.com/language/translate/v2?key=${GOOGLE_TRANSLATE_API_KEY}`;

  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      q: text,
      target: targetLang,
      format: 'text',
    }),
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Translation API error (${res.status}): ${err}`);
  }

  const data = await res.json();
  const translations: TranslateResult[] = data?.data?.translations ?? [];
  return translations[0]?.translatedText ?? text;
}

/**
 * Birden fazla metni tek seferde çevirir (batch).
 */
export async function translateBatch(
  texts: string[],
  targetLang: string
): Promise<string[]> {
  if (!GOOGLE_TRANSLATE_API_KEY) return texts;

  const nonEmpty = texts.filter((t) => t.trim());
  if (nonEmpty.length === 0) return texts;

  const url = `https://translation.googleapis.com/language/translate/v2?key=${GOOGLE_TRANSLATE_API_KEY}`;

  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      q: texts,
      target: targetLang,
      format: 'text',
    }),
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Translation API error (${res.status}): ${err}`);
  }

  const data = await res.json();
  const translations: TranslateResult[] = data?.data?.translations ?? [];
  return translations.map((t, i) => t?.translatedText ?? texts[i]);
}
