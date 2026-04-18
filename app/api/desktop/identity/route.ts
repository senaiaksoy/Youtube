import { NextResponse } from 'next/server';

export const dynamic = 'force-dynamic';

export async function GET() {
  return NextResponse.json({
    app: 'youtube-manager',
    ok: true,
  });
}
