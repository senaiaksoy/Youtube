'use client';

import { useCallback, useEffect, useState } from 'react';
import { AlertTriangle, BarChart3, CheckCircle2, ExternalLink, RefreshCw, ShieldCheck, Sparkles } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';

type AuditIssue = {
  severity: 'high' | 'medium' | 'low';
  title: string;
  detail: string;
};

type AuditVideo = {
  id: string;
  title: string;
  score: number;
  grade: 'A' | 'B' | 'C' | 'D';
  viewCount: number;
  likeCount: number;
  commentCount: number;
  engagementRate: number;
  privacyStatus: string;
  localizationCount: number;
  issues: AuditIssue[];
};

type AuditData = {
  error?: string;
  generatedAt: string;
  score: number;
  grade: 'A' | 'B' | 'C' | 'D';
  channel: {
    title: string;
    subscriberCount: number;
    totalViews: number;
    videoCount: number;
    avgViews: number;
  };
  summary: {
    high: number;
    medium: number;
    low: number;
    publishedVideos: number;
    privateOrUnlistedVideos: number;
    averageVideoScore: number;
  };
  priorities: AuditIssue[];
  videos: AuditVideo[];
  references: Array<{ name: string; url: string; reason: string }>;
};

const severityLabels = {
  high: 'Yuksek',
  medium: 'Orta',
  low: 'Dusuk',
};

const severityClasses = {
  high: 'border-red-200 bg-red-50 text-red-700 dark:border-red-900 dark:bg-red-950/40 dark:text-red-300',
  medium: 'border-amber-200 bg-amber-50 text-amber-700 dark:border-amber-900 dark:bg-amber-950/40 dark:text-amber-300',
  low: 'border-sky-200 bg-sky-50 text-sky-700 dark:border-sky-900 dark:bg-sky-950/40 dark:text-sky-300',
};

function formatNumber(value: number) {
  return (value ?? 0).toLocaleString('tr-TR');
}

function gradeClass(grade: string) {
  if (grade === 'A') return 'text-emerald-600';
  if (grade === 'B') return 'text-sky-600';
  if (grade === 'C') return 'text-amber-600';
  return 'text-red-600';
}

export function AuditTab() {
  const [data, setData] = useState<AuditData | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchAudit = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/youtube/audit');
      const audit = await res.json();
      setData(audit);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchAudit();
  }, [fetchAudit]);

  if (loading && !data) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="h-8 w-8 animate-spin rounded-full border-b-2 border-primary" />
      </div>
    );
  }

  const summary = data?.summary;
  const videos = data?.videos ?? [];
  const priorities = data?.priorities ?? [];

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <h2 className="font-display text-2xl font-bold tracking-tight">Kanal Audit</h2>
          <p className="mt-1 text-sm text-muted-foreground">
            Son 25 video icin SEO, medikal uyum, CTA, etiket ve yerellestirme kontrolu
          </p>
        </div>
        <Button variant="outline" onClick={fetchAudit} disabled={loading}>
          <RefreshCw className={`mr-2 h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
          Yenile
        </Button>
      </div>

      {data?.error && (
        <div className="flex items-center gap-3 rounded-lg bg-destructive/10 p-4 text-sm text-destructive">
          <AlertTriangle className="h-5 w-5 flex-shrink-0" />
          <div>
            <p className="font-medium">Audit verisi alinamadi</p>
            <p className="mt-0.5 text-xs opacity-80">{data.error}</p>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-[1.2fr_2fr]">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <ShieldCheck className="h-5 w-5 text-primary" />
              Genel Skor
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-5">
            <div className="flex items-end gap-3">
              <span className={`text-6xl font-bold ${gradeClass(data?.grade ?? 'D')}`}>{data?.grade ?? 'D'}</span>
              <div className="pb-2">
                <p className="text-2xl font-semibold">{data?.score ?? 0}/100</p>
                <p className="text-xs text-muted-foreground">Ortalama video skoru: {summary?.averageVideoScore ?? 0}</p>
              </div>
            </div>
            <Progress value={data?.score ?? 0} />
            <div className="grid grid-cols-3 gap-2 text-center text-sm">
              <div className="rounded-md border p-3">
                <p className="font-semibold text-red-600">{summary?.high ?? 0}</p>
                <p className="text-xs text-muted-foreground">Yuksek</p>
              </div>
              <div className="rounded-md border p-3">
                <p className="font-semibold text-amber-600">{summary?.medium ?? 0}</p>
                <p className="text-xs text-muted-foreground">Orta</p>
              </div>
              <div className="rounded-md border p-3">
                <p className="font-semibold text-sky-600">{summary?.low ?? 0}</p>
                <p className="text-xs text-muted-foreground">Dusuk</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BarChart3 className="h-5 w-5 text-primary" />
              Kanal Ozeti
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
              <div className="rounded-md border p-3">
                <p className="text-xs text-muted-foreground">Video</p>
                <p className="mt-1 text-lg font-semibold">{formatNumber(data?.channel.videoCount ?? 0)}</p>
              </div>
              <div className="rounded-md border p-3">
                <p className="text-xs text-muted-foreground">Goruntuleme</p>
                <p className="mt-1 text-lg font-semibold">{formatNumber(data?.channel.totalViews ?? 0)}</p>
              </div>
              <div className="rounded-md border p-3">
                <p className="text-xs text-muted-foreground">Ortalama</p>
                <p className="mt-1 text-lg font-semibold">{formatNumber(data?.channel.avgViews ?? 0)}</p>
              </div>
              <div className="rounded-md border p-3">
                <p className="text-xs text-muted-foreground">Abone</p>
                <p className="mt-1 text-lg font-semibold">{formatNumber(data?.channel.subscriberCount ?? 0)}</p>
              </div>
            </div>
            <div className="mt-4 rounded-md border p-3 text-sm text-muted-foreground">
              {summary?.publishedVideos ?? 0} herkese acik video incelendi; {summary?.privateOrUnlistedVideos ?? 0} video
              ozel veya liste disi gorunuyor.
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <AlertTriangle className="h-5 w-5 text-primary" />
            Oncelikli Duzeltmeler
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {priorities.map((issue, index) => (
              <div key={`${issue.title}-${index}`} className="rounded-md border p-3">
                <div className="flex flex-wrap items-center gap-2">
                  <Badge variant="outline" className={severityClasses[issue.severity]}>
                    {severityLabels[issue.severity]}
                  </Badge>
                  <p className="font-medium">{issue.title}</p>
                </div>
                <p className="mt-2 text-sm text-muted-foreground">{issue.detail}</p>
              </div>
            ))}
            {priorities.length === 0 && (
              <div className="flex items-center gap-2 rounded-md border p-4 text-sm text-muted-foreground">
                <CheckCircle2 className="h-4 w-4 text-emerald-600" />
                Kritik duzeltme bulunmadi.
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-primary" />
            Video Skorlari
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {videos.map((video) => (
              <div key={video.id} className="rounded-md border p-3">
                <div className="flex flex-col gap-3 lg:flex-row lg:items-start lg:justify-between">
                  <div className="min-w-0">
                    <div className="flex items-center gap-2">
                      <span className={`text-xl font-bold ${gradeClass(video.grade)}`}>{video.grade}</span>
                      <p className="truncate font-medium">{video.title || video.id}</p>
                    </div>
                    <p className="mt-1 text-xs text-muted-foreground">
                      {formatNumber(video.viewCount)} izlenme, %{video.engagementRate} etkilesim, {video.localizationCount} dil
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    <Badge variant="secondary">{video.score}/100</Badge>
                    <Badge variant="outline">{video.privacyStatus}</Badge>
                  </div>
                </div>
                {video.issues.length > 0 && (
                  <div className="mt-3 flex flex-wrap gap-2">
                    {video.issues.slice(0, 4).map((issue, index) => (
                      <Badge key={`${issue.title}-${index}`} variant="outline" className={severityClasses[issue.severity]}>
                        {issue.title}
                      </Badge>
                    ))}
                  </div>
                )}
              </div>
            ))}
            {videos.length === 0 && (
              <p className="py-8 text-center text-muted-foreground">Audit icin video verisi yok</p>
            )}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Kaynak Alinan Acik Kaynak Fikirleri</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-3 md:grid-cols-2">
            {(data?.references ?? []).map((reference) => (
              <a
                key={reference.url}
                href={reference.url}
                target="_blank"
                rel="noreferrer"
                className="rounded-md border p-3 transition-colors hover:bg-accent"
              >
                <div className="flex items-center justify-between gap-2">
                  <p className="font-medium">{reference.name}</p>
                  <ExternalLink className="h-4 w-4 text-muted-foreground" />
                </div>
                <p className="mt-1 text-sm text-muted-foreground">{reference.reason}</p>
              </a>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
