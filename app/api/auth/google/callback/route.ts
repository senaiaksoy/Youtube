import { NextRequest, NextResponse } from 'next/server';
import { writeTokens } from '@/lib/youtube-token';

export const dynamic = 'force-dynamic';

function getBaseUrl(req: NextRequest): string {
  const forwardedHost = req.headers.get('x-forwarded-host');
  const forwardedProto = req.headers.get('x-forwarded-proto') ?? 'https';
  if (forwardedHost) return `${forwardedProto}://${forwardedHost}`;
  if (process.env.NEXTAUTH_URL) return process.env.NEXTAUTH_URL;
  const host = req.headers.get('host') ?? 'localhost:3000';
  const proto = host.startsWith('localhost') ? 'http' : 'https';
  return `${proto}://${host}`;
}

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const code = searchParams.get('code');
  const error = searchParams.get('error');
  const baseUrl = getBaseUrl(req);

  if (error) {
    return NextResponse.redirect(`${baseUrl}/?auth_error=${encodeURIComponent(error)}`);
  }

  if (!code) {
    return NextResponse.redirect(`${baseUrl}/?auth_error=missing_code`);
  }

  const clientId = process.env.GOOGLE_CLIENT_ID;
  const clientSecret = process.env.GOOGLE_CLIENT_SECRET;

  if (!clientId || !clientSecret) {
    return NextResponse.redirect(`${baseUrl}/?auth_error=missing_config`);
  }

  const redirectUri = `${baseUrl}/api/auth/google/callback`;

  try {
    const tokenRes = await fetch('https://oauth2.googleapis.com/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        code,
        client_id: clientId,
        client_secret: clientSecret,
        redirect_uri: redirectUri,
        grant_type: 'authorization_code',
      }).toString(),
    });

    if (!tokenRes.ok) {
      const msg = await tokenRes.text().catch(() => '');
      console.error('Token exchange failed:', tokenRes.status, msg);
      return NextResponse.redirect(`${baseUrl}/?auth_error=token_exchange_failed`);
    }

    const data = await tokenRes.json();
    const now = Date.now();

    writeTokens({
      access_token: data.access_token,
      refresh_token: data.refresh_token,
      expires_at: now + (data.expires_in ?? 3600) * 1000,
      scope: data.scope,
      token_type: data.token_type,
    });

    return NextResponse.redirect(`${baseUrl}/?auth=success`);
  } catch (e: any) {
    console.error('OAuth callback error:', e);
    return NextResponse.redirect(`${baseUrl}/?auth_error=${encodeURIComponent(e.message ?? 'unknown')}`);
  }
}
