import { NextResponse } from 'next/server';
import { isConnected, readTokens } from '@/lib/youtube-token';

export const dynamic = 'force-dynamic';

export async function GET() {
  const tokens = readTokens();
  return NextResponse.json({
    connected: isConnected(),
    hasRefreshToken: !!tokens?.refresh_token,
    expiresAt: tokens?.expires_at ?? null,
  });
}
