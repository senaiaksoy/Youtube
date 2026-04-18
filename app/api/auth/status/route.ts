import { NextResponse } from 'next/server';
import { readTokens, validateYouTubeConnection } from '@/lib/youtube-token';

export const dynamic = 'force-dynamic';

export async function GET() {
  const tokens = readTokens();
  const connected = await validateYouTubeConnection();
  const latestTokens = connected ? readTokens() : null;

  return NextResponse.json({
    connected,
    hasRefreshToken: !!latestTokens?.refresh_token,
    expiresAt: latestTokens?.expires_at ?? null,
  });
}
