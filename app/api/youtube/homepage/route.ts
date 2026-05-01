export const dynamic = 'force-dynamic';

import fs from 'fs';
import path from 'path';
import { NextRequest, NextResponse } from 'next/server';
import { getValidAccessToken } from '@/lib/youtube-token';

type PlaylistDef = {
  title: string;
  description: string;
  videoIds: string[];
  privacyStatus?: 'public' | 'unlisted' | 'private';
  showOnHomepage?: boolean;
};

type HomepageConfig = {
  playlists: PlaylistDef[];
  homepageOrder: string[];
};

type PlaylistItemRef = {
  id: string;
  videoId: string;
};

type PlaylistSyncResult = {
  title: string;
  playlistId?: string;
  status: 'created' | 'updated' | 'unchanged' | 'dry_run' | 'error';
  videosSet?: number;
  error?: string;
};

type SectionSyncResult = {
  status: 'updated' | 'dry_run' | 'error';
  desiredTitles?: string[];
  deletedSectionIds?: string[];
  createdSectionIds?: string[];
  error?: string;
};

const CONFIG_PATH = path.join(process.cwd(), 'youtube-api', 'homepage-config.json');

function readHomepageConfig(): HomepageConfig {
  const raw = fs.readFileSync(CONFIG_PATH, 'utf-8');
  return JSON.parse(raw) as HomepageConfig;
}

async function youtubeRequest(url: string, init?: RequestInit) {
  const token = await getValidAccessToken();
  const res = await fetch(url, {
    ...init,
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
      ...(init?.headers ?? {}),
    },
  });

  const text = await res.text().catch(() => '');
  let parsed: any = null;
  if (text) {
    try {
      parsed = JSON.parse(text);
    } catch {
      parsed = text;
    }
  }

  if (!res.ok) {
    const message =
      typeof parsed === 'object' && parsed?.error?.message
        ? parsed.error.message
        : typeof parsed === 'string' && parsed
          ? parsed
          : `YouTube API ${res.status}`;
    throw new Error(message);
  }

  return parsed;
}

async function listAllPlaylists() {
  const items: any[] = [];
  let pageToken = '';

  while (true) {
    const url = `https://www.googleapis.com/youtube/v3/playlists?part=id,snippet,status&mine=true&maxResults=50${
      pageToken ? `&pageToken=${pageToken}` : ''
    }`;
    const data = await youtubeRequest(url);
    items.push(...(data?.items ?? []));
    pageToken = data?.nextPageToken ?? '';
    if (!pageToken) return items;
  }
}

async function listPlaylistItems(playlistId: string): Promise<PlaylistItemRef[]> {
  const items: PlaylistItemRef[] = [];
  let pageToken = '';

  while (true) {
    const url =
      `https://www.googleapis.com/youtube/v3/playlistItems?part=id,contentDetails&playlistId=${playlistId}&maxResults=50` +
      (pageToken ? `&pageToken=${pageToken}` : '');
    const data = await youtubeRequest(url);

    for (const item of data?.items ?? []) {
      items.push({
        id: item.id,
        videoId: item?.contentDetails?.videoId,
      });
    }

    pageToken = data?.nextPageToken ?? '';
    if (!pageToken) return items;
  }
}

async function clearPlaylistItems(items: PlaylistItemRef[]) {
  for (const item of items) {
    await youtubeRequest(`https://www.googleapis.com/youtube/v3/playlistItems?id=${item.id}`, {
      method: 'DELETE',
    });
    await new Promise((resolve) => setTimeout(resolve, 250));
  }
}

async function addVideosToPlaylist(playlistId: string, videoIds: string[]) {
  for (const videoId of videoIds) {
    await youtubeRequest('https://www.googleapis.com/youtube/v3/playlistItems?part=snippet', {
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
    await new Promise((resolve) => setTimeout(resolve, 250));
  }
}

function sameVideoOrder(current: PlaylistItemRef[], desiredVideoIds: string[]) {
  return (
    current.length === desiredVideoIds.length &&
    current.every((item, index) => item.videoId === desiredVideoIds[index])
  );
}

async function syncPlaylist(def: PlaylistDef, existingPlaylists: any[], dryRun: boolean): Promise<PlaylistSyncResult> {
  try {
    const existing = existingPlaylists.find((item) => item?.snippet?.title?.trim() === def.title.trim());
    const desiredPrivacy = def.privacyStatus ?? 'public';

    if (!existing) {
      if (dryRun) {
        return {
          title: def.title,
          status: 'dry_run',
          videosSet: def.videoIds.length,
        };
      }

      const created = await youtubeRequest('https://www.googleapis.com/youtube/v3/playlists?part=snippet,status', {
        method: 'POST',
        body: JSON.stringify({
          snippet: {
            title: def.title,
            description: def.description,
            defaultLanguage: 'tr',
          },
          status: {
            privacyStatus: desiredPrivacy,
          },
        }),
      });

      const playlistId = created?.id;
      await addVideosToPlaylist(playlistId, def.videoIds);

      return {
        title: def.title,
        playlistId,
        status: 'created',
        videosSet: def.videoIds.length,
      };
    }

    const playlistId = existing.id;
    const needsMetadataUpdate =
      existing?.snippet?.description !== def.description ||
      existing?.status?.privacyStatus !== desiredPrivacy;
    const currentItems = await listPlaylistItems(playlistId);
    const needsVideoReset = !sameVideoOrder(currentItems, def.videoIds);

    if (dryRun) {
      return {
        title: def.title,
        playlistId,
        status: needsMetadataUpdate || needsVideoReset ? 'dry_run' : 'unchanged',
        videosSet: def.videoIds.length,
      };
    }

    if (needsMetadataUpdate) {
      await youtubeRequest('https://www.googleapis.com/youtube/v3/playlists?part=snippet,status', {
        method: 'PUT',
        body: JSON.stringify({
          id: playlistId,
          snippet: {
            title: def.title,
            description: def.description,
            defaultLanguage: existing?.snippet?.defaultLanguage || 'tr',
          },
          status: {
            privacyStatus: desiredPrivacy,
          },
        }),
      });
    }

    if (needsVideoReset) {
      await clearPlaylistItems(currentItems);
      await addVideosToPlaylist(playlistId, def.videoIds);
    }

    return {
      title: def.title,
      playlistId,
      status: needsMetadataUpdate || needsVideoReset ? 'updated' : 'unchanged',
      videosSet: def.videoIds.length,
    };
  } catch (error: any) {
    return {
      title: def.title,
      status: 'error',
      error: error?.message ?? String(error),
    };
  }
}

async function listChannelSections() {
  const data = await youtubeRequest(
    'https://www.googleapis.com/youtube/v3/channelSections?part=id,snippet,contentDetails&mine=true'
  );
  return data?.items ?? [];
}

async function replaceHomepageSections(
  homepageOrder: string[],
  playlistResults: PlaylistSyncResult[],
  dryRun: boolean
): Promise<SectionSyncResult> {
  try {
    const titleToPlaylistId = new Map<string, string>();
    for (const item of playlistResults) {
      if (item.playlistId) {
        titleToPlaylistId.set(item.title, item.playlistId);
        continue;
      }
      if (dryRun && item.status === 'dry_run') {
        titleToPlaylistId.set(item.title, `[create:${item.title}]`);
      }
    }

    const desiredTitles = homepageOrder.filter((title) => titleToPlaylistId.has(title));
    if (desiredTitles.length !== homepageOrder.length) {
      const missing = homepageOrder.filter((title) => !titleToPlaylistId.has(title));
      return {
        status: 'error',
        error: `Missing playlist ids for homepage titles: ${missing.join(', ')}`,
      };
    }

    const existingSections = await listChannelSections();
    const deletedSectionIds = existingSections.map((item: any) => item.id);

    if (dryRun) {
      return {
        status: 'dry_run',
        desiredTitles,
        deletedSectionIds,
        createdSectionIds: desiredTitles.map((title) => titleToPlaylistId.get(title) as string),
      };
    }

    for (const section of existingSections) {
      await youtubeRequest(`https://www.googleapis.com/youtube/v3/channelSections?id=${section.id}`, {
        method: 'DELETE',
      });
      await new Promise((resolve) => setTimeout(resolve, 250));
    }

    const createdSectionIds: string[] = [];
    for (let index = 0; index < desiredTitles.length; index++) {
      const playlistId = titleToPlaylistId.get(desiredTitles[index]) as string;
      const created = await youtubeRequest('https://www.googleapis.com/youtube/v3/channelSections?part=snippet,contentDetails', {
        method: 'POST',
        body: JSON.stringify({
          snippet: {
            type: 'singlePlaylist',
            position: index,
          },
          contentDetails: {
            playlists: [playlistId],
          },
        }),
      });
      createdSectionIds.push(created?.id ?? playlistId);
      await new Promise((resolve) => setTimeout(resolve, 250));
    }

    return {
      status: 'updated',
      desiredTitles,
      deletedSectionIds,
      createdSectionIds,
    };
  } catch (error: any) {
    return {
      status: 'error',
      error: error?.message ?? String(error),
    };
  }
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json().catch(() => ({}));
    const dryRun = body?.dryRun ?? true;
    const config = readHomepageConfig();
    const existingPlaylists = await listAllPlaylists();

    const playlistResults: PlaylistSyncResult[] = [];
    for (const playlist of config.playlists) {
      const result = await syncPlaylist(playlist, existingPlaylists, dryRun);
      playlistResults.push(result);
    }

    const sectionResult = await replaceHomepageSections(config.homepageOrder, playlistResults, dryRun);

    return NextResponse.json({
      config,
      dryRun,
      playlistResults,
      sectionResult,
      summary: {
        created: playlistResults.filter((item) => item.status === 'created').length,
        updated: playlistResults.filter((item) => item.status === 'updated').length,
        unchanged: playlistResults.filter((item) => item.status === 'unchanged').length,
        dryRun: playlistResults.filter((item) => item.status === 'dry_run').length,
        errors:
          playlistResults.filter((item) => item.status === 'error').length +
          (sectionResult.status === 'error' ? 1 : 0),
      },
    });
  } catch (error: any) {
    return NextResponse.json(
      { error: error?.message ?? 'Homepage sync failed' },
      { status: 500 }
    );
  }
}
