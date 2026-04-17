import { NextResponse } from 'next/server';
import { clearTokens } from '@/lib/youtube-token';

export const dynamic = 'force-dynamic';

export async function POST() {
  clearTokens();
  return NextResponse.json({ success: true });
}
