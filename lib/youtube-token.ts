import fs from 'fs';
import path from 'path';

const TOKENS_FILE = process.env.YOUTUBE_TOKENS_FILE ?? path.join(process.cwd(), 'data', 'google-tokens.json');
const LEGACY_FILE = process.env.YOUTUBE_LEGACY_FILE ?? path.join(process.cwd(), 'data', 'auth-secrets.json');

export const CHANNEL_ID = process.env.YOUTUBE_CHANNEL_ID ?? 'UC51eCoXFnN1DiBd1dWcJpPQ';

export const OAUTH_SCOPES = [
  'https://www.googleapis.com/auth/youtube',
  'https://www.googleapis.com/auth/youtube.force-ssl',
  'https://www.googleapis.com/auth/yt-analytics.readonly',
].join(' ');

export type StoredTokens = {
  access_token: string;
  refresh_token?: string;
  expires_at: number; // epoch ms
  scope?: string;
  token_type?: string;
};

function ensureDataDir() {
  const dir = path.dirname(TOKENS_FILE);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

export function readTokens(): StoredTokens | null {
  try {
    if (fs.existsSync(TOKENS_FILE)) {
      const raw = fs.readFileSync(TOKENS_FILE, 'utf-8');
      return JSON.parse(raw) as StoredTokens;
    }
  } catch {
    /* ignore */
  }

  // Legacy fallback: support old auth-secrets.json format (no refresh token)
  try {
    if (fs.existsSync(LEGACY_FILE)) {
      const raw = fs.readFileSync(LEGACY_FILE, 'utf-8');
      const data = JSON.parse(raw);
      const t = data?.youtube?.secrets?.access_token;
      if (t?.value) {
        const expires = t.expires_at ? Date.parse(t.expires_at) : 0;
        return { access_token: t.value, expires_at: expires };
      }
    }
  } catch {
    /* ignore */
  }

  return null;
}

export function writeTokens(tokens: StoredTokens) {
  ensureDataDir();
  fs.writeFileSync(TOKENS_FILE, JSON.stringify(tokens, null, 2), 'utf-8');
}

export function clearTokens() {
  try {
    if (fs.existsSync(TOKENS_FILE)) fs.unlinkSync(TOKENS_FILE);
  } catch {
    /* ignore */
  }
}

export function isConnected(): boolean {
  const t = readTokens();
  return !!(t?.access_token || t?.refresh_token);
}

export function isAuthErrorMessage(message: string | undefined | null): boolean {
  if (!message) return false;

  const normalized = message.toLowerCase();
  return (
    normalized.includes('invalid authentication credentials') ||
    normalized.includes('expected oauth 2 access token') ||
    normalized.includes('refresh failed') ||
    normalized.includes('invalid_grant') ||
    normalized.includes('unauthorized') ||
    normalized.includes('login required') ||
    normalized.includes('request had invalid authentication credentials')
  );
}

async function refreshAccessToken(refreshToken: string): Promise<StoredTokens> {
  const clientId = process.env.GOOGLE_CLIENT_ID;
  const clientSecret = process.env.GOOGLE_CLIENT_SECRET;
  if (!clientId || !clientSecret) {
    throw new Error('GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET not set');
  }

  const params = new URLSearchParams({
    client_id: clientId,
    client_secret: clientSecret,
    refresh_token: refreshToken,
    grant_type: 'refresh_token',
  });

  const res = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: params.toString(),
  });

  if (!res.ok) {
    const errTxt = await res.text().catch(() => '');
    throw new Error(`Refresh failed: ${res.status} ${errTxt}`);
  }

  const data = await res.json();
  const now = Date.now();
  const stored: StoredTokens = {
    access_token: data.access_token,
    refresh_token: refreshToken, // Google may not return refresh_token on refresh; keep old
    expires_at: now + (data.expires_in ?? 3600) * 1000,
    scope: data.scope,
    token_type: data.token_type,
  };
  writeTokens(stored);
  return stored;
}

export async function getValidAccessToken(): Promise<string> {
  let tokens = readTokens();
  if (!tokens) {
    throw new Error('NOT_CONNECTED');
  }

  // If access token is valid for at least 60 more seconds, use it
  if (tokens.access_token && tokens.expires_at > Date.now() + 60 * 1000) {
    return tokens.access_token;
  }

  // Otherwise, try refreshing
  if (tokens.refresh_token) {
    tokens = await refreshAccessToken(tokens.refresh_token);
    return tokens.access_token;
  }

  // Legacy tokens without refresh: fall back to existing access_token (may fail)
  if (tokens.access_token) return tokens.access_token;

  throw new Error('NOT_CONNECTED');
}

export async function youtubeApiFetch(url: string, options?: RequestInit) {
  const token = await getValidAccessToken();
  const res = await fetch(url, {
    ...options,
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
      ...(options?.headers ?? {}),
    },
  });
  if (!res.ok) {
    const errorBody = await res.text().catch(() => '');
    let message = `YouTube API ${res.status}`;
    try {
      const parsed = JSON.parse(errorBody);
      message = parsed?.error?.message ?? message;
    } catch { /* use default */ }
    throw new Error(message);
  }
  return res.json();
}

export async function validateYouTubeConnection(): Promise<boolean> {
  if (!isConnected()) return false;

  try {
    await youtubeApiFetch('https://www.googleapis.com/youtube/v3/channels?part=id&mine=true&maxResults=1');
    return true;
  } catch (error: any) {
    if (isAuthErrorMessage(error?.message)) {
      clearTokens();
    }
    return false;
  }
}
