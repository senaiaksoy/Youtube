export const dynamic = 'force-dynamic';

import { NextResponse } from 'next/server';
import { youtubeApiFetch } from '@/lib/youtube-token';

export async function PUT(request: Request, { params }: { params: { id: string } }) {
  try {
    const body = await request.json();
    const videoId = params?.id;
    if (!videoId) return NextResponse.json({ error: 'Video ID required' }, { status: 400 });

    // First fetch current video data
    const currentUrl = `https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=${videoId}`;
    const currentData = await youtubeApiFetch(currentUrl);
    const current = currentData?.items?.[0];
    if (!current) return NextResponse.json({ error: 'Video not found' }, { status: 404 });

    const updateBody: any = {
      id: videoId,
      snippet: {
        ...(current?.snippet ?? {}),
        categoryId: current?.snippet?.categoryId ?? '22',
      },
      status: { ...(current?.status ?? {}) },
    };

    if (body?.title !== undefined) updateBody.snippet.title = body.title;
    if (body?.description !== undefined) updateBody.snippet.description = body.description;
    if (body?.privacyStatus !== undefined) updateBody.status.privacyStatus = body.privacyStatus;

    const updateUrl = 'https://www.googleapis.com/youtube/v3/videos?part=snippet,status';
    const result = await youtubeApiFetch(updateUrl, {
      method: 'PUT',
      body: JSON.stringify(updateBody),
    });

    return NextResponse.json({ success: true, video: result });
  } catch (err: any) {
    // Graceful error handling
    return NextResponse.json({ error: err?.message ?? 'Failed to update video' }, { status: 500 });
  }
}
