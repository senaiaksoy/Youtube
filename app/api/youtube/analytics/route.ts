export const dynamic = 'force-dynamic';

import { NextResponse } from 'next/server';
import { youtubeApiFetch, CHANNEL_ID } from '@/lib/youtube-token';

export async function GET() {
  try {
    // Get channel stats
    const channelUrl = `https://www.googleapis.com/youtube/v3/channels?part=statistics,snippet&id=${CHANNEL_ID}`;
    const channelData = await youtubeApiFetch(channelUrl);
    const channel = channelData?.items?.[0];

    const channelStats = {
      title: channel?.snippet?.title ?? 'Kanal',
      subscriberCount: parseInt(channel?.statistics?.subscriberCount ?? '0', 10),
      totalViews: parseInt(channel?.statistics?.viewCount ?? '0', 10),
      videoCount: parseInt(channel?.statistics?.videoCount ?? '0', 10),
      thumbnail: channel?.snippet?.thumbnails?.medium?.url ?? '',
    };

    // Get top videos by view count
    const searchUrl = `https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=${CHANNEL_ID}&type=video&maxResults=10&order=viewCount`;
    const searchData = await youtubeApiFetch(searchUrl);
    const videoIds = (searchData?.items ?? []).map((item: any) => item?.id?.videoId).filter(Boolean).join(',');

    let topVideos: any[] = [];
    if (videoIds) {
      const detailsUrl = `https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id=${videoIds}`;
      const detailsData = await youtubeApiFetch(detailsUrl);
      topVideos = (detailsData?.items ?? [])
        .map((v: any) => ({
          id: v?.id ?? '',
          title: v?.snippet?.title ?? '',
          thumbnail: v?.snippet?.thumbnails?.default?.url ?? '',
          viewCount: parseInt(v?.statistics?.viewCount ?? '0', 10),
          likeCount: parseInt(v?.statistics?.likeCount ?? '0', 10),
        }))
        .sort((a: any, b: any) => (b?.viewCount ?? 0) - (a?.viewCount ?? 0));
    }

    return NextResponse.json({
      channel: channelStats,
      topVideos,
      avgViews: channelStats.videoCount > 0 ? Math.round(channelStats.totalViews / channelStats.videoCount) : 0,
    });
  } catch (err: any) {
    // Token may be expired - graceful degradation
    // Return 200 with fallback data to avoid console errors in browser
    return NextResponse.json({
      error: err?.message ?? 'Failed to fetch analytics',
      channel: { title: 'Kanal', subscriberCount: 0, totalViews: 0, videoCount: 0, thumbnail: '' },
      topVideos: [],
      avgViews: 0,
    });
  }
}
