import { NextRequest, NextResponse } from 'next/server';
import { OAUTH_SCOPES } from '@/lib/youtube-token';
import { createOAuthState } from '@/lib/oauth-state';

export const dynamic = 'force-dynamic';

function getBaseUrl(req: NextRequest): string {
  // Prefer forwarded host if present (production behind proxy)
  const forwardedHost = req.headers.get('x-forwarded-host');
  const forwardedProto = req.headers.get('x-forwarded-proto') ?? 'https';
  if (forwardedHost) return `${forwardedProto}://${forwardedHost}`;

  if (process.env.NEXTAUTH_URL) return process.env.NEXTAUTH_URL;

  const host = req.headers.get('host') ?? 'localhost:3000';
  const proto = host.startsWith('localhost') ? 'http' : 'https';
  return `${proto}://${host}`;
}

export async function GET(req: NextRequest) {
  const clientId = process.env.GOOGLE_CLIENT_ID;
  if (!clientId) {
    return NextResponse.json({ error: 'GOOGLE_CLIENT_ID not configured' }, { status: 500 });
  }

  const baseUrl = getBaseUrl(req);
  const redirectUri = `${baseUrl}/api/auth/google/callback`;
  const { state, hashedState, maxAge } = createOAuthState();

  const params = new URLSearchParams({
    client_id: clientId,
    redirect_uri: redirectUri,
    response_type: 'code',
    scope: OAUTH_SCOPES,
    access_type: 'offline',
    prompt: 'consent', // ensure refresh_token is returned
    include_granted_scopes: 'true',
    state,
  });

  const authUrl = `https://accounts.google.com/o/oauth2/v2/auth?${params.toString()}`;
  const response = NextResponse.redirect(authUrl);
  response.cookies.set('google_oauth_state', hashedState, {
    httpOnly: true,
    sameSite: 'lax',
    secure: baseUrl.startsWith('https://'),
    path: '/',
    maxAge,
  });
  return response;
}
