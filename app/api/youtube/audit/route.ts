export const dynamic = 'force-dynamic';

import { NextResponse } from 'next/server';
import { auditChannel, type VideoAuditInput } from '@/lib/youtube-audit';
import { youtubeApiFetch, CHANNEL_ID } from '@/lib/youtube-token';

function toNumber(value: unknown) {
  const parsed = parseInt(String(value ?? '0'), 10);
  return Number.isFinite(parsed) ? parsed : 0;
}

export async function GET() {
  try {
    const channelUrl = `https://www.googleapis.com/youtube/v3/channels?part=statistics,snippet&id=${CHANNEL_ID}`;
    const channelData = await youtubeApiFetch(channelUrl);
    const channel = channelData?.items?.[0];

    const searchUrl = `https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=${CHANNEL_ID}&type=video&maxResults=25&order=date`;
    const searchData = await youtubeApiFetch(searchUrl);
    const videoIds = (searchData?.items ?? []).map((item: any) => item?.id?.videoId).filter(Boolean).join(',');

    let recentVideos: VideoAuditInput[] = [];
    if (videoIds) {
      const detailsUrl = `https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,localizations,status&id=${videoIds}`;
      const detailsData = await youtubeApiFetch(detailsUrl);
      recentVideos = (detailsData?.items ?? []).map((video: any) => ({
        id: video?.id ?? '',
        title: video?.snippet?.title ?? '',
        description: video?.snippet?.description ?? '',
        tags: video?.snippet?.tags ?? [],
        thumbnail: video?.snippet?.thumbnails?.high?.url
          ?? video?.snippet?.thumbnails?.medium?.url
          ?? video?.snippet?.thumbnails?.default?.url
          ?? '',
        privacyStatus: video?.status?.privacyStatus ?? 'private',
        publishedAt: video?.snippet?.publishedAt ?? '',
        viewCount: toNumber(video?.statistics?.viewCount),
        likeCount: toNumber(video?.statistics?.likeCount),
        commentCount: toNumber(video?.statistics?.commentCount),
        localizationCount: Object.keys(video?.localizations ?? {}).length,
      }));
    }

    const audit = auditChannel({
      title: channel?.snippet?.title ?? 'Kanal',
      subscriberCount: toNumber(channel?.statistics?.subscriberCount),
      totalViews: toNumber(channel?.statistics?.viewCount),
      videoCount: toNumber(channel?.statistics?.videoCount),
      recentVideos,
    });

    return NextResponse.json(audit);
  } catch (err: any) {
    return NextResponse.json(
      {
        error: err?.message ?? 'Audit verisi alinamadi',
        generatedAt: new Date().toISOString(),
        score: 0,
        grade: 'D',
        channel: { title: 'Kanal', subscriberCount: 0, totalViews: 0, videoCount: 0, avgViews: 0 },
        summary: { high: 0, medium: 0, low: 0, publishedVideos: 0, privateOrUnlistedVideos: 0, averageVideoScore: 0 },
        priorities: [],
        videos: [],
        references: [],
      },
      { status: 200 }
    );
  }
}
