'use client';

import { useState, useEffect, useCallback } from 'react';
import {
  Search,
  Edit2,
  Eye,
  Globe,
  Lock,
  EyeOff,
  ChevronDown,
  Save,
  X,
  Loader2,
} from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'sonner';
import Image from 'next/image';

interface VideoItem {
  id: string;
  title: string;
  description: string;
  thumbnail: string;
  publishedAt: string;
  viewCount: number;
  likeCount: number;
  commentCount: number;
  localizations: Record<string, unknown>;
  privacyStatus: string;
  tags: string[];
  categoryId: string;
}

const privacyOptions = [
  { value: 'public', label: 'Herkese Açık', icon: Globe, color: 'text-green-500' },
  { value: 'unlisted', label: 'Liste Dışı', icon: EyeOff, color: 'text-yellow-500' },
  { value: 'private', label: 'Özel', icon: Lock, color: 'text-red-500' },
];

export function VideosTab() {
  const [videos, setVideos] = useState<VideoItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editForm, setEditForm] = useState({ title: '', description: '', privacyStatus: '' });
  const [saving, setSaving] = useState(false);
  const [nextPageToken, setNextPageToken] = useState<string | null>(null);
  const [searchTimeout, setSearchTimeout] = useState<NodeJS.Timeout | null>(null);

  const fetchVideos = useCallback(async (query?: string, pageToken?: string) => {
    setLoading(true);
    try {
      let url = '/api/youtube/videos?';
      if (query) url += `q=${encodeURIComponent(query)}&`;
      if (pageToken) url += `pageToken=${pageToken}&`;
      const res = await fetch(url);
      const data = await res.json();
      if (data?.error) {
        toast.error(data.error);
      } else {
        setVideos(pageToken ? (prev) => [...prev, ...(data?.videos ?? [])] : (data?.videos ?? []));
        setNextPageToken(data?.nextPageToken ?? null);
      }
    } catch (err: any) {
      toast.error(err?.message ?? 'Videolar yüklenemedi');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchVideos();
  }, [fetchVideos]);

  const handleSearch = (value: string) => {
    setSearchQuery(value);
    if (searchTimeout) clearTimeout(searchTimeout);
    const timeout = setTimeout(() => {
      fetchVideos(value);
    }, 500);
    setSearchTimeout(timeout);
  };

  const startEdit = (video: VideoItem) => {
    setEditingId(video?.id ?? null);
    setEditForm({
      title: video?.title ?? '',
      description: video?.description ?? '',
      privacyStatus: video?.privacyStatus ?? 'private',
    });
  };

  const saveEdit = async () => {
    if (!editingId) return;
    setSaving(true);
    try {
      const res = await fetch(`/api/youtube/video/${editingId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(editForm),
      });
      const data = await res.json();
      if (data?.error) {
        toast.error(data.error);
      } else {
        toast.success('Video güncellendi!');
        setEditingId(null);
        fetchVideos(searchQuery);
      }
    } catch (err: any) {
      toast.error(err?.message ?? 'Güncelleme başarısız');
    } finally {
      setSaving(false);
    }
  };

  const getPrivacyIcon = (status: string) => {
    const option = privacyOptions.find((item) => item.value === status);
    if (!option) return null;
    const Icon = option.icon;
    return <Icon className={`h-4 w-4 ${option.color}`} />;
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="font-display text-2xl font-bold tracking-tight">Video Yönetimi</h2>
        <p className="mt-1 text-sm text-muted-foreground">
          Kanalda bulunan videoları görüntüleyin ve düzenleyin
        </p>
      </div>

      <div className="relative">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <Input
          placeholder="Video ara..."
          value={searchQuery}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleSearch(e.target.value)}
          className="pl-10"
        />
      </div>

      {loading && videos.length === 0 ? (
        <div className="flex items-center justify-center py-20">
          <div className="h-8 w-8 animate-spin rounded-full border-b-2 border-primary" />
        </div>
      ) : (
        <div className="space-y-3">
          <AnimatePresence mode="popLayout">
            {(videos ?? []).map((video, index) => (
              <motion.div
                key={video?.id ?? index}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ delay: index * 0.03 }}
              >
                <Card className="overflow-hidden transition-all hover:shadow-lg">
                  <CardContent className="p-0">
                    {editingId === video?.id ? (
                      <div className="space-y-4 p-4">
                        <div className="flex items-center justify-between">
                          <h3 className="text-sm font-medium">Video Düzenleme</h3>
                          <button onClick={() => setEditingId(null)} className="text-muted-foreground hover:text-foreground">
                            <X className="h-4 w-4" />
                          </button>
                        </div>
                        <div className="space-y-3">
                          <div>
                            <label className="mb-1 block text-xs text-muted-foreground">Başlık</label>
                            <Input
                              value={editForm.title}
                              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                                setEditForm((prev) => ({ ...prev, title: e.target.value }))
                              }
                            />
                          </div>
                          <div>
                            <label className="mb-1 block text-xs text-muted-foreground">Açıklama</label>
                            <textarea
                              value={editForm.description}
                              onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) =>
                                setEditForm((prev) => ({ ...prev, description: e.target.value }))
                              }
                              className="min-h-[100px] w-full resize-y rounded-md border border-input bg-background px-3 py-2 text-sm"
                            />
                          </div>
                          <div>
                            <label className="mb-1 block text-xs text-muted-foreground">Gizlilik</label>
                            <div className="flex gap-2">
                              {privacyOptions.map((option) => {
                                const Icon = option.icon;
                                return (
                                  <button
                                    key={option.value}
                                    onClick={() => setEditForm((prev) => ({ ...prev, privacyStatus: option.value }))}
                                    className={`flex items-center gap-2 rounded-lg border px-3 py-2 text-sm transition-all ${
                                      editForm.privacyStatus === option.value
                                        ? 'border-primary bg-primary/10 text-foreground'
                                        : 'border-border text-muted-foreground hover:border-primary/50'
                                    }`}
                                  >
                                    <Icon className={`h-4 w-4 ${option.color}`} />
                                    {option.label}
                                  </button>
                                );
                              })}
                            </div>
                          </div>
                        </div>
                        <div className="flex justify-end gap-2">
                          <Button variant="outline" size="sm" onClick={() => setEditingId(null)}>
                            İptal
                          </Button>
                          <Button size="sm" onClick={saveEdit} disabled={saving}>
                            {saving ? <Loader2 className="mr-1 h-4 w-4 animate-spin" /> : <Save className="mr-1 h-4 w-4" />}
                            Kaydet
                          </Button>
                        </div>
                      </div>
                    ) : (
                      <div className="flex gap-4 p-4">
                        <div className="relative aspect-video w-40 flex-shrink-0 overflow-hidden rounded bg-muted">
                          {video?.thumbnail ? (
                            <Image src={video.thumbnail} alt={video?.title ?? 'Video'} fill className="object-cover" />
                          ) : (
                            <div className="flex h-full items-center justify-center">
                              <Eye className="h-5 w-5 text-muted-foreground" />
                            </div>
                          )}
                        </div>
                        <div className="min-w-0 flex-1">
                          <div className="flex items-start justify-between gap-2">
                            <div className="min-w-0">
                              <h3 className="truncate text-sm font-medium">{video?.title ?? 'Başlıksız'}</h3>
                              <p className="mt-1 line-clamp-2 text-xs text-muted-foreground">
                                {video?.description?.slice(0, 150) ?? ''}
                              </p>
                            </div>
                            <Button variant="ghost" size="sm" onClick={() => startEdit(video)} className="flex-shrink-0">
                              <Edit2 className="h-4 w-4" />
                            </Button>
                          </div>
                          <div className="mt-3 flex items-center gap-4 text-xs text-muted-foreground">
                            <span className="flex items-center gap-1">
                              {getPrivacyIcon(video?.privacyStatus ?? 'private')}
                              {privacyOptions.find((item) => item.value === video?.privacyStatus)?.label ?? 'Bilinmiyor'}
                            </span>
                            <span className="flex items-center gap-1">
                              <Eye className="h-3 w-3" />
                              {(video?.viewCount ?? 0).toLocaleString('tr-TR')}
                            </span>
                            <span>
                              {video?.publishedAt ? new Date(video.publishedAt).toLocaleDateString('tr-TR') : ''}
                            </span>
                            {Object.keys(video?.localizations ?? {}).length > 0 && (
                              <span className="flex items-center gap-1 text-primary">
                                <Globe className="h-3 w-3" />
                                {Object.keys(video?.localizations ?? {}).length} dil
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                    )}
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </AnimatePresence>

          {videos.length === 0 && !loading && (
            <p className="py-12 text-center text-muted-foreground">Video bulunamadı</p>
          )}

          {nextPageToken && (
            <div className="flex justify-center pt-4">
              <Button variant="outline" onClick={() => fetchVideos(searchQuery, nextPageToken)} disabled={loading}>
                {loading ? (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                ) : (
                  <ChevronDown className="mr-2 h-4 w-4" />
                )}
                Daha Fazla Yükle
              </Button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
