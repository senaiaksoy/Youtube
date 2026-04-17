'use client';

import { useState, useEffect, useRef } from 'react';
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
  const ref = useRef<HTMLSpanElement>(null);

  useEffect(() => {
    let start = 0;
    const end = value ?? 0;
    if (end === 0) return;
    const stepTime = Math.max(Math.floor(duration / end), 1);
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

  return <span ref={ref} className="font-mono">{(count ?? 0).toLocaleString('tr-TR')}</span>;
}

export function DashboardTab() {
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch('/api/youtube/analytics')
      .then(res => res.json())
      .then(d => {
        if (d?.error) setError(d.error);
        setData(d);
      })
      .catch(e => setError(e?.message ?? 'Veri alınamadı'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
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
        <p className="text-muted-foreground text-sm mt-1">{channel?.title ?? 'Kanal'} için analitik verileri</p>
      </div>

      {error && (
        <div className="bg-destructive/10 text-destructive rounded-lg p-4 flex items-center gap-3 text-sm">
          <BarChart3 className="w-5 h-5 flex-shrink-0" />
          <div>
            <p className="font-medium">YouTube API Ba&#x11f;lant&#x131; Hatas&#x131;</p>
            <p className="text-xs mt-0.5 opacity-80">Token s&#xfc;resi dolmu&#x15f; olabilir. L&#xfc;tfen OAuth ba&#x11f;lant&#x131;s&#x131;n&#x131; yenileyin.</p>
          </div>
        </div>
      )}

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat, i) => {
          const Icon = stat.icon;
          return (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
            >
              <Card className="hover:shadow-lg transition-shadow">
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-xs text-muted-foreground uppercase tracking-wide">{stat.label}</p>
                      <p className="text-2xl font-bold mt-1">
                        <AnimatedCounter value={stat.value} />
                      </p>
                    </div>
                    <div className={`p-3 rounded-lg bg-muted ${stat.color}`}>
                      <Icon className="w-5 h-5" />
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          );
        })}
      </div>

      {/* Top Videos */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-primary" />
            En Çok İzlenen Videolar
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {topVideos.map((video: any, i: number) => (
              <motion.div
                key={video?.id ?? i}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.05 }}
                className="flex items-center gap-4 p-3 rounded-lg hover:bg-accent transition-colors"
              >
                <span className="font-mono text-sm text-muted-foreground w-6 text-right">{i + 1}</span>
                <div className="relative w-20 aspect-video rounded overflow-hidden bg-muted flex-shrink-0">
                  {video?.thumbnail ? (
                    <Image src={video.thumbnail} alt={video?.title ?? 'Video'} fill className="object-cover" />
                  ) : (
                    <div className="flex items-center justify-center h-full">
                      <Play className="w-5 h-5 text-muted-foreground" />
                    </div>
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-sm truncate">{video?.title ?? 'Başlıksız'}</p>
                  <p className="text-xs text-muted-foreground mt-0.5">
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
              <p className="text-center text-muted-foreground py-8">Henüz video verisi yok</p>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
