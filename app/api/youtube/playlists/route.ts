export const dynamic = 'force-dynamic';

import { NextRequest, NextResponse } from 'next/server';
import { youtubeApiFetch } from '@/lib/youtube-token';

/**
 * POST /api/youtube/playlists
 *
 * Body: { playlists: PlaylistDef[], dryRun?: boolean }
 *
 * PlaylistDef = {
 *   title: string;
 *   description: string;
 *   videoIds: string[];
 *   privacyStatus?: 'public' | 'unlisted' | 'private';
 * }
 */

type PlaylistDef = {
  title: string;
  description: string;
  videoIds: string[];
  privacyStatus?: 'public' | 'unlisted' | 'private';
};

type PlaylistResult = {
  title: string;
  status: 'created' | 'dry_run' | 'error';
  playlistId?: string;
  videosAdded?: number;
  error?: string;
};

async function createPlaylist(def: PlaylistDef, dryRun: boolean): Promise<PlaylistResult> {
  try {
    if (dryRun) {
      return {
        title: def.title,
        status: 'dry_run',
        videosAdded: def.videoIds.length,
      };
    }

    // 1. Create playlist
    const createUrl = 'https://www.googleapis.com/youtube/v3/playlists?part=snippet,status';
    const playlist = await youtubeApiFetch(createUrl, {
      method: 'POST',
      body: JSON.stringify({
        snippet: {
          title: def.title,
          description: def.description,
          defaultLanguage: 'tr',
        },
        status: {
          privacyStatus: def.privacyStatus ?? 'public',
        },
      }),
    });

    const playlistId = playlist.id;

    // 2. Add videos to playlist
    let added = 0;
    for (const videoId of def.videoIds) {
      const itemUrl = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet';
      await youtubeApiFetch(itemUrl, {
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
      added++;
      // Rate limit
      await new Promise((r) => setTimeout(r, 500));
    }

    return {
      title: def.title,
      status: 'created',
      playlistId,
      videosAdded: added,
    };
  } catch (err: any) {
    return {
      title: def.title,
      status: 'error',
      error: err?.message ?? String(err),
    };
  }
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const playlists: PlaylistDef[] = body?.playlists ?? [];
    const dryRun: boolean = body?.dryRun ?? true;

    if (!playlists.length) {
      return NextResponse.json({ error: 'No playlists provided' }, { status: 400 });
    }

    const results: PlaylistResult[] = [];
    for (const def of playlists) {
      const result = await createPlaylist(def, dryRun);
      results.push(result);
    }

    return NextResponse.json({ results });
  } catch (err: any) {
    return NextResponse.json({ error: err?.message ?? 'Playlist creation failed' }, { status: 500 });
  }
}
