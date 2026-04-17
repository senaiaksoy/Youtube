export const dynamic = 'force-dynamic';

import { NextResponse } from 'next/server';
import { youtubeApiFetch, CHANNEL_ID } from '@/lib/youtube-token';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const pageToken = searchParams.get('pageToken') ?? '';
    const q = searchParams.get('q') ?? '';

    // First get all video IDs from channel
    let searchUrl = `https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=${CHANNEL_ID}&type=video&maxResults=50&order=date`;
    if (pageToken) searchUrl += `&pageToken=${pageToken}`;
    if (q) searchUrl += `&q=${encodeURIComponent(q)}`;

    const searchData = await youtubeApiFetch(searchUrl);
    const videoIds = (searchData?.items ?? []).map((item: any) => item?.id?.videoId).filter(Boolean).join(',');

    if (!videoIds) {
      return NextResponse.json({ videos: [], nextPageToken: null, totalResults: 0 });
    }

    // Get detailed info including stats and localizations
    const detailsUrl = `https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,localizations,status&id=${videoIds}`;
    const detailsData = await youtubeApiFetch(detailsUrl);

    const videos = (detailsData?.items ?? []).map((v: any) => ({
      id: v?.id ?? '',
      title: v?.snippet?.title ?? '',
      description: v?.snippet?.description ?? '',
      thumbnail: v?.snippet?.thumbnails?.medium?.url ?? v?.snippet?.thumbnails?.default?.url ?? '',
      publishedAt: v?.snippet?.publishedAt ?? '',
      viewCount: parseInt(v?.statistics?.viewCount ?? '0', 10),
      likeCount: parseInt(v?.statistics?.likeCount ?? '0', 10),
      commentCount: parseInt(v?.statistics?.commentCount ?? '0', 10),
      localizations: v?.localizations ?? {},
      defaultLanguage: v?.snippet?.defaultLanguage ?? '',
      privacyStatus: v?.status?.privacyStatus ?? 'private',
      tags: v?.snippet?.tags ?? [],
      categoryId: v?.snippet?.categoryId ?? '',
    }));

    return NextResponse.json({
      videos,
      nextPageToken: searchData?.nextPageToken ?? null,
      totalResults: searchData?.pageInfo?.totalResults ?? 0,
    });
  } catch (err: any) {
    // Graceful error handling
    return NextResponse.json({ error: err?.message ?? 'Failed to fetch videos', videos: [], nextPageToken: null, totalResults: 0 });
  }
}
