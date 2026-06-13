export const dynamic = 'force-dynamic';

import { NextResponse } from 'next/server';
import { youtubeApiFetch } from '@/lib/youtube-token';

async function fetchAllPlaylists() {
  const items: any[] = [];
  let pageToken = '';

  while (true) {
    const url = `https://www.googleapis.com/youtube/v3/playlists?part=id,snippet,status&mine=true&maxResults=50${
      pageToken ? `&pageToken=${pageToken}` : ''
    }`;
    const data = await youtubeApiFetch(url);
    items.push(...(data?.items ?? []));
    pageToken = data?.nextPageToken ?? '';
    if (!pageToken) return items;
  }
}

export async function GET(request: Request, { params }: { params: { id: string } }) {
  try {
    const videoId = params?.id;
    if (!videoId) return NextResponse.json({ error: 'Video ID required' }, { status: 400 });

    const playlists = await fetchAllPlaylists();

    const playlistsWithStatus = await Promise.all(
      playlists.map(async (playlist: any) => {
        try {
          const playlistId = playlist.id;
          const itemsUrl = `https://www.googleapis.com/youtube/v3/playlistItems?part=id&playlistId=${playlistId}&videoId=${videoId}&maxResults=1`;
          const itemsData = await youtubeApiFetch(itemsUrl);
          const hasVideo = (itemsData?.items ?? []).length > 0;
          const playlistItemId = hasVideo ? itemsData.items[0].id : null;
          return {
            id: playlistId,
            title: playlist?.snippet?.title ?? '',
            description: playlist?.snippet?.description ?? '',
            hasVideo,
            playlistItemId,
          };
        } catch (err) {
          return {
            id: playlist.id,
            title: playlist?.snippet?.title ?? '',
            description: playlist?.snippet?.description ?? '',
            hasVideo: false,
            playlistItemId: null,
          };
        }
      })
    );

    return NextResponse.json({ playlists: playlistsWithStatus });
  } catch (err: any) {
    return NextResponse.json({ error: err?.message ?? 'Failed to fetch video playlists' }, { status: 500 });
  }
}

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
    if (body?.tags !== undefined) updateBody.snippet.tags = body.tags;
    if (body?.privacyStatus !== undefined) updateBody.status.privacyStatus = body.privacyStatus;

    const updateUrl = 'https://www.googleapis.com/youtube/v3/videos?part=snippet,status';
    const result = await youtubeApiFetch(updateUrl, {
      method: 'PUT',
      body: JSON.stringify(updateBody),
    });

    // Handle playlist additions
    if (body?.addPlaylists && Array.isArray(body.addPlaylists)) {
      for (const playlistId of body.addPlaylists) {
        const addUrl = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet';
        await youtubeApiFetch(addUrl, {
          method: 'POST',
          body: JSON.stringify({
            snippet: {
              playlistId,
              resourceId: {
                kind: 'youtube#video',
                videoId,
              },
            },
          }),
        });
        await new Promise((resolve) => setTimeout(resolve, 200));
      }
    }

    // Handle playlist removals
    if (body?.removePlaylists && Array.isArray(body.removePlaylists)) {
      for (const playlistItemId of body.removePlaylists) {
        const deleteUrl = `https://www.googleapis.com/youtube/v3/playlistItems?id=${playlistItemId}`;
        await youtubeApiFetch(deleteUrl, {
          method: 'DELETE',
        });
        await new Promise((resolve) => setTimeout(resolve, 200));
      }
    }

    return NextResponse.json({ success: true, video: result });
  } catch (err: any) {
    return NextResponse.json({ error: err?.message ?? 'Failed to update video' }, { status: 500 });
  }
}
