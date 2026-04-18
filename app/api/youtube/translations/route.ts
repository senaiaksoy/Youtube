export const dynamic = 'force-dynamic';

import { NextResponse } from 'next/server';
import { youtubeApiFetch } from '@/lib/youtube-token';
import { translateBatch } from '@/lib/translate';

// Add translations to videos - STREAMING NDJSON response for live progress
export async function POST(request: Request) {
  let body: any = {};
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: 'Invalid JSON body' }, { status: 400 });
  }

  const { videoIds, languages } = body ?? {};

  if (!videoIds?.length || !languages?.length) {
    return NextResponse.json({ error: 'videoIds and languages are required' }, { status: 400 });
  }

  const encoder = new TextEncoder();

  const stream = new ReadableStream({
    async start(controller) {
      const send = (event: any) => {
        try {
          controller.enqueue(encoder.encode(JSON.stringify(event) + '\n'));
        } catch {
          /* stream closed */
        }
      };

      // Initial event with total count
      send({
        type: 'start',
        total: videoIds.length,
        languages,
      });

      const results: any[] = [];
      let processed = 0;

      for (const videoId of videoIds) {
        processed++;

        // Send "processing" event for current video
        send({
          type: 'processing',
          videoId,
          index: processed,
          total: videoIds.length,
        });

        try {
          // Fetch current video with snippet and localizations
          const url = `https://www.googleapis.com/youtube/v3/videos?part=snippet,localizations&id=${videoId}`;
          const data = await youtubeApiFetch(url);
          const video = data?.items?.[0];
          if (!video) {
            const result = { videoId, success: false, error: 'Video bulunamadı' };
            results.push(result);
            send({ type: 'result', ...result, index: processed, total: videoIds.length });
            continue;
          }

          const currentLocalizations = video?.localizations ?? {};
          const title = video?.snippet?.title ?? '';
          const description = video?.snippet?.description ?? '';
          const videoTitle = title;

          // Add each language localization (with real translation)
          const newLocalizations = { ...currentLocalizations };
          const addedLanguages: string[] = [];
          const skippedLanguages: string[] = [];
          for (const lang of languages) {
            if (!newLocalizations[lang]) {
              addedLanguages.push(lang);
            } else {
              skippedLanguages.push(lang);
            }
          }

          // Translate title and description for each new language
          for (const lang of addedLanguages) {
            try {
              const [translatedTitle, translatedDescription] = await translateBatch(
                [title, description],
                lang
              );
              newLocalizations[lang] = {
                title: translatedTitle,
                description: translatedDescription,
              };
            } catch (translationErr: any) {
              // Fallback: use original text if translation fails
              console.error(`Translation to ${lang} failed:`, translationErr?.message);
              newLocalizations[lang] = { title, description };
            }
          }

          // If nothing new to add, skip the API call
          if (addedLanguages.length === 0) {
            const result = {
              videoId,
              videoTitle,
              success: true,
              skipped: true,
              addedLanguages: [],
              skippedLanguages,
            };
            results.push(result);
            send({ type: 'result', ...result, index: processed, total: videoIds.length });
            continue;
          }

          // Update video with new localizations
          const updateUrl = 'https://www.googleapis.com/youtube/v3/videos?part=snippet,localizations';
          const snippetUpdate: any = {
            title: video?.snippet?.title,
            description: video?.snippet?.description,
            categoryId: video?.snippet?.categoryId ?? '22',
          };
          if (video?.snippet?.defaultLanguage) {
            snippetUpdate.defaultLanguage = video.snippet.defaultLanguage;
          }
          const updateBody = {
            id: videoId,
            snippet: snippetUpdate,
            localizations: newLocalizations,
          };

          await youtubeApiFetch(updateUrl, {
            method: 'PUT',
            body: JSON.stringify(updateBody),
          });

          const result = {
            videoId,
            videoTitle,
            success: true,
            addedLanguages,
            skippedLanguages,
          };
          results.push(result);
          send({ type: 'result', ...result, index: processed, total: videoIds.length });
        } catch (err: any) {
          const result = {
            videoId,
            success: false,
            error: err?.message ?? 'Bilinmeyen hata',
          };
          results.push(result);
          send({ type: 'result', ...result, index: processed, total: videoIds.length });
        }
      }

      // Final completion event
      const successCount = results.filter((r) => r.success).length;
      const failCount = results.length - successCount;
      send({
        type: 'done',
        total: videoIds.length,
        successCount,
        failCount,
        results,
      });

      controller.close();
    },
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'application/x-ndjson; charset=utf-8',
      'Cache-Control': 'no-cache, no-transform',
      'X-Accel-Buffering': 'no',
    },
  });
}

// Delete translation from a video
export async function DELETE(request: Request) {
  try {
    const body = await request.json();
    const { videoId, language } = body ?? {};

    if (!videoId || !language) {
      return NextResponse.json({ error: 'videoId and language are required' }, { status: 400 });
    }

    // Fetch current video
    const url = `https://www.googleapis.com/youtube/v3/videos?part=snippet,localizations&id=${videoId}`;
    const data = await youtubeApiFetch(url);
    const video = data?.items?.[0];
    if (!video) return NextResponse.json({ error: 'Video not found' }, { status: 404 });

    const localizations = { ...(video?.localizations ?? {}) };
    delete localizations[language];

    const updateUrl = 'https://www.googleapis.com/youtube/v3/videos?part=snippet,localizations';
    const snippetUpdate: any = {
      title: video?.snippet?.title,
      description: video?.snippet?.description,
      categoryId: video?.snippet?.categoryId ?? '22',
    };
    if (video?.snippet?.defaultLanguage) {
      snippetUpdate.defaultLanguage = video.snippet.defaultLanguage;
    }
    const updateBody = {
      id: videoId,
      snippet: snippetUpdate,
      localizations,
    };

    await youtubeApiFetch(updateUrl, {
      method: 'PUT',
      body: JSON.stringify(updateBody),
    });

    return NextResponse.json({ success: true });
  } catch (err: any) {
    return NextResponse.json({ error: err?.message ?? 'Failed to delete translation' }, { status: 500 });
  }
}
