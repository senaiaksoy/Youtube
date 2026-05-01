export const dynamic = 'force-dynamic';

import { NextRequest, NextResponse } from 'next/server';
import { youtubeApiFetch } from '@/lib/youtube-token';
import { normalizeYoutubeText, normalizeYoutubeTextList } from '@/lib/youtube-text';

/**
 * POST /api/youtube/batch-update
 *
 * Body: { fixes: VideoFix[] }
 *
 * VideoFix = {
 *   video_id: string;
 *   title?: string | null;          // null → değiştirme
 *   description_hook?: string | null; // açıklama ilk satırlarını değiştir
 *   hashtags?: string[] | null;      // açıklama sonuna ekle
 *   tags?: string[] | null;          // YouTube backend tags (merge)
 *   standardize_disclaimer?: boolean;
 * }
 *
 * Response: { results: UpdateResult[] }
 */

// ── Standart Disclaimer (Format B) ──
const DISCLAIMER = `⚕️ ÖNEMLİ TIBBİ UYARI
Bu videoda sunulan bilgiler yalnızca eğitim ve bilgilendirme amaçlıdır. Bu içerik hiçbir koşulda tıbbi tavsiye, tanı veya kişiselleştirilmiş tedavi önerisi niteliği taşımamaktadır.
Her hastanın tıbbi durumu kendine özgüdür. Bu videoda ele alınan konular; bir hekim, kadın doğum uzmanı veya üreme tıbbı uzmanı ile yapılacak konsültasyonun yerini tutmaz.
Bu videodaki bilgilere dayanarak mevcut tedavinizi değiştirmeyin, yeni bir tedaviye başlamayın veya herhangi bir tıbbi karar almayın. Her türlü tıbbi karar öncesinde mutlaka aile hekiminize veya uzman doktorunuza danışınız.
Üreme sağlığınız veya IVF tedavi sürecinizle ilgili sorularınız için lütfen yetkili bir sağlık profesyoneline başvurunuz.
© Doç. Dr. Senai Aksoy — Tüm hakları saklıdır.`;

type VideoFix = {
  video_id: string;
  title?: string | null;
  description_hook?: string | null;
  hashtags?: string[] | null;
  tags?: string[] | null;
  standardize_disclaimer?: boolean;
};

type UpdateResult = {
  video_id: string;
  status: 'updated' | 'skipped' | 'error' | 'dry_run';
  changes?: Record<string, { old: string; new: string }>;
  error?: string;
};

function normalizeFix(fix: VideoFix): VideoFix {
  return {
    ...fix,
    title: typeof fix.title === 'string' ? normalizeYoutubeText(fix.title) : fix.title,
    description_hook:
      typeof fix.description_hook === 'string'
        ? normalizeYoutubeText(fix.description_hook)
        : fix.description_hook,
    hashtags: normalizeYoutubeTextList(fix.hashtags),
    tags: normalizeYoutubeTextList(fix.tags),
  };
}

// ── Açıklama hook'u değiştir ──
function replaceHook(desc: string, hook: string): string {
  const lines = desc.split('\n');
  let tsStart: number | null = null;

  for (let i = 0; i < lines.length; i++) {
    const s = lines[i].trim();
    if (
      s.length > 2 &&
      (/^\d+:\d\d/.test(s) || s.startsWith('⏱') || s.startsWith('00:') || s.startsWith('0:'))
    ) {
      tsStart = i;
      break;
    }
  }

  if (tsStart !== null && tsStart > 0) {
    const remaining = lines.slice(tsStart).join('\n');
    return hook.trimEnd() + '\n\n' + remaining;
  } else if (tsStart === 0) {
    return hook.trimEnd() + '\n\n' + desc;
  } else {
    const parts = desc.split('\n\n');
    if (parts.length > 1) {
      return hook.trimEnd() + '\n\n' + parts.slice(1).join('\n\n');
    }
    return hook.trimEnd() + '\n\n' + desc;
  }
}

// ── Hashtag ekle (disclaimer'dan önce) ──
function ensureHashtags(desc: string, hashtags: string[]): string {
  const existingTags = desc.split(/\s+/).filter((w) => w.startsWith('#'));
  if (existingTags.length >= 3) return desc;

  const tagLine = hashtags.join(' ');
  const markers = ['⚕️ ÖNEMLİ', 'TIBBİ UYARI', '*Bu videodaki bilgiler'];

  for (const marker of markers) {
    const idx = desc.indexOf(marker);
    if (idx > 0) {
      const before = desc.slice(0, idx).trimEnd();
      const after = desc.slice(idx);
      return before + '\n\n' + tagLine + '\n\n' + after;
    }
  }

  return desc.trimEnd() + '\n\n' + tagLine;
}

// ── Kısa disclaimer → uzun ──
function standardizeDisclaimer(desc: string): string {
  const shortMarker = '*Bu videodaki bilgiler yalnızca genel bilgilendirme amaçlıdır';
  if (desc.includes(shortMarker)) {
    const idx = desc.indexOf(shortMarker);
    let end = desc.indexOf('\n---', idx);
    if (end === -1) end = desc.length;
    else end += 4;
    const oldBlock = desc.slice(idx, end);
    return desc.replace(oldBlock, DISCLAIMER);
  }
  return desc;
}

async function fetchVideo(videoId: string) {
  const url = `https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=${videoId}`;
  const data = await youtubeApiFetch(url);
  return data?.items?.[0] ?? null;
}

async function applyFix(
  fix: VideoFix,
  dryRun: boolean
): Promise<UpdateResult> {
  try {
    const normalizedFix = normalizeFix(fix);
    const video = await fetchVideo(fix.video_id);
    if (!video) return { video_id: fix.video_id, status: 'error', error: 'Video not found' };

    const snippet = { ...video.snippet };
    const changes: Record<string, { old: string; new: string }> = {};

    // ── Başlık ──
    if (normalizedFix.title && normalizedFix.title !== snippet.title) {
      changes.title = { old: snippet.title, new: normalizedFix.title };
      snippet.title = normalizedFix.title;
    }

    // ── Açıklama ──
    let desc = snippet.description ?? '';
    const origDesc = desc;

    if (normalizedFix.description_hook) {
      desc = replaceHook(desc, normalizedFix.description_hook);
    }
    if (normalizedFix.hashtags && normalizedFix.hashtags.length > 0) {
      desc = ensureHashtags(desc, normalizedFix.hashtags);
    }
    if (normalizedFix.standardize_disclaimer) {
      desc = standardizeDisclaimer(desc);
    }

    if (desc !== origDesc) {
      changes.description = {
        old: origDesc.slice(0, 150) + '…',
        new: desc.slice(0, 150) + '…',
      };
      snippet.description = desc;
    }

    // ── Tags ──
    if (normalizedFix.tags && normalizedFix.tags.length > 0) {
      const oldTags: string[] = normalizeYoutubeTextList(snippet.tags ?? []) ?? [];
      const merged = [...new Set([...oldTags, ...normalizedFix.tags])];
      if (JSON.stringify(merged) !== JSON.stringify(oldTags)) {
        changes.tags = { old: oldTags.join(', '), new: merged.join(', ') };
        snippet.tags = merged;
      }
    }

    if (Object.keys(changes).length === 0) {
      return { video_id: fix.video_id, status: 'skipped', changes };
    }

    if (dryRun) {
      return { video_id: fix.video_id, status: 'dry_run', changes };
    }

    // ── Tag temizliği: boş, çok uzun veya geçersiz tag'leri filtrele ──
    const cleanTags = (snippet.tags ?? [])
      .map((t: string) => t.trim())
      .filter((t: string) => t.length > 0 && t.length < 500 && !t.includes('<') && !t.includes('>'));

    // ── Gerçek güncelleme (sadece yazılabilir alanlar) ──
    const updateUrl = 'https://www.googleapis.com/youtube/v3/videos?part=snippet';
    await youtubeApiFetch(updateUrl, {
      method: 'PUT',
      body: JSON.stringify({
        id: fix.video_id,
        snippet: {
          title: snippet.title,
          description: snippet.description,
          tags: cleanTags,
          categoryId: snippet.categoryId ?? '26',
          defaultLanguage: snippet.defaultLanguage || 'tr',
          defaultAudioLanguage: snippet.defaultAudioLanguage || 'tr',
        },
      }),
    });

    return { video_id: fix.video_id, status: 'updated', changes };
  } catch (err: any) {
    return { video_id: fix.video_id, status: 'error', error: err?.message ?? String(err) };
  }
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const fixes: VideoFix[] = body?.fixes ?? [];
    const dryRun: boolean = body?.dryRun ?? true; // default: dry run

    if (!fixes.length) {
      return NextResponse.json({ error: 'No fixes provided' }, { status: 400 });
    }

    const results: UpdateResult[] = [];
    for (const fix of fixes) {
      const result = await applyFix(fix, dryRun);
      results.push(result);
      // Rate limit: 1 saniye bekle (gerçek güncellemelerde)
      if (!dryRun && result.status === 'updated') {
        await new Promise((r) => setTimeout(r, 1000));
      }
    }

    const summary = {
      total: results.length,
      updated: results.filter((r) => r.status === 'updated').length,
      dry_run: results.filter((r) => r.status === 'dry_run').length,
      skipped: results.filter((r) => r.status === 'skipped').length,
      errors: results.filter((r) => r.status === 'error').length,
    };

    return NextResponse.json({ summary, results });
  } catch (err: any) {
    return NextResponse.json({ error: err?.message ?? 'Batch update failed' }, { status: 500 });
  }
}
