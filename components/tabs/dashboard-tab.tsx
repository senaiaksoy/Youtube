'use client';

import { useState, useEffect } from 'react';
import { Eye, Video, TrendingUp, Users, BarChart3, Play } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { motion } from 'framer-motion';
import Image from 'next/image';

interface AnalyticsData {
  channel: {
    title: string;
    subscriberCount: number;
    totalViews: number;
    videoCount: number;
    thumbnail: string;
  };
  topVideos: Array<{
    id: string;
    title: string;
    thumbnail: string;
    viewCount: number;
    likeCount: number;
  }>;
  avgViews: number;
}

function AnimatedCounter({ value, duration = 2000 }: { value: number; duration?: number }) {
  const [count, setCount] = useState(0);

  useEffect(() => {
    let start = 0;
    const end = value ?? 0;
    if (end === 0) return;

    const increment = Math.max(Math.ceil(end / (duration / 16)), 1);
    const timer = setInterval(() => {
      start += increment;
      if (start >= end) {
        setCount(end);
        clearInterval(timer);
      } else {
        setCount(start);
      }
    }, 16);

    return () => clearInterval(timer);
  }, [value, duration]);

  return <span className="font-mono">{(count ?? 0).toLocaleString('tr-TR')}</span>;
}

export function DashboardTab() {
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch('/api/youtube/analytics')
      .then((res) => res.json())
      .then((response) => {
        if (response?.error) setError(response.error);
        setData(response);
      })
      .catch((err) => setError(err?.message ?? 'Veri alınamadı'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="h-8 w-8 animate-spin rounded-full border-b-2 border-primary" />
      </div>
    );
  }

  const channel = data?.channel;
  const topVideos = data?.topVideos ?? [];
  const avgViews = data?.avgViews ?? 0;

  const stats = [
    { label: 'Toplam Video', value: channel?.videoCount ?? 0, icon: Video, color: 'text-blue-500' },
    { label: 'Toplam Görüntüleme', value: channel?.totalViews ?? 0, icon: Eye, color: 'text-green-500' },
    { label: 'Ortalama Görüntüleme', value: avgViews, icon: TrendingUp, color: 'text-orange-500' },
    { label: 'Abone Sayısı', value: channel?.subscriberCount ?? 0, icon: Users, color: 'text-purple-500' },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="font-display text-2xl font-bold tracking-tight">Kanal Özeti</h2>
        <p className="mt-1 text-sm text-muted-foreground">{channel?.title ?? 'Kanal'} için analitik verileri</p>
      </div>

      {error && (
        <div className="flex items-center gap-3 rounded-lg bg-destructive/10 p-4 text-sm text-destructive">
          <BarChart3 className="h-5 w-5 flex-shrink-0" />
          <div>
            <p className="font-medium">YouTube API Bağlantı Hatası</p>
            <p className="mt-0.5 text-xs opacity-80">
              Token süresi dolmuş olabilir. Lütfen OAuth bağlantısını yenileyin.
            </p>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <Card className="transition-shadow hover:shadow-lg">
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-xs uppercase tracking-wide text-muted-foreground">{stat.label}</p>
                      <p className="mt-1 text-2xl font-bold">
                        <AnimatedCounter value={stat.value} />
                      </p>
                    </div>
                    <div className={`rounded-lg bg-muted p-3 ${stat.color}`}>
                      <Icon className="h-5 w-5" />
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          );
        })}
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5 text-primary" />
            En Çok İzlenen Videolar
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {topVideos.map((video, index) => (
              <motion.div
                key={video?.id ?? index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
                className="flex items-center gap-4 rounded-lg p-3 transition-colors hover:bg-accent"
              >
                <span className="w-6 text-right font-mono text-sm text-muted-foreground">{index + 1}</span>
                <div className="relative aspect-video w-20 flex-shrink-0 overflow-hidden rounded bg-muted">
                  {video?.thumbnail ? (
                    <Image src={video.thumbnail} alt={video?.title ?? 'Video'} fill className="object-cover" />
                  ) : (
                    <div className="flex h-full items-center justify-center">
                      <Play className="h-5 w-5 text-muted-foreground" />
                    </div>
                  )}
                </div>
                <div className="min-w-0 flex-1">
                  <p className="truncate text-sm font-medium">{video?.title ?? 'Başlıksız'}</p>
                  <p className="mt-0.5 text-xs text-muted-foreground">
                    {(video?.viewCount ?? 0).toLocaleString('tr-TR')} görüntüleme
                  </p>
                </div>
                <div className="text-right">
                  <span className="font-mono text-sm font-medium">
                    {(video?.viewCount ?? 0).toLocaleString('tr-TR')}
                  </span>
                </div>
              </motion.div>
            ))}
            {topVideos.length === 0 && (
              <p className="py-8 text-center text-muted-foreground">Henüz video verisi yok</p>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
