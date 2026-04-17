'use client';

import { useState, useEffect, useCallback } from 'react';
import { Search, Filter, Edit2, Eye, Globe, Lock, EyeOff, ChevronDown, Save, X, Loader2 } from 'lucide-react';
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
  localizations: Record<string, any>;
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
    const opt = privacyOptions.find(o => o.value === status);
    if (!opt) return null;
    const Icon = opt.icon;
    return <Icon className={`w-4 h-4 ${opt.color}`} />;
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="font-display text-2xl font-bold tracking-tight">Video Yönetimi</h2>
        <p className="text-muted-foreground text-sm mt-1">Kanalda bulunan videoları görüntüleyin ve düzenleyin</p>
      </div>

      {/* Search Bar */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
        <Input
          placeholder="Video ara..."
          value={searchQuery}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleSearch(e.target.value)}
          className="pl-10"
        />
      </div>

      {/* Video List */}
      {loading && videos.length === 0 ? (
        <div className="flex items-center justify-center py-20">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
        </div>
      ) : (
        <div className="space-y-3">
          <AnimatePresence mode="popLayout">
            {(videos ?? []).map((video: VideoItem, i: number) => (
              <motion.div
                key={video?.id ?? i}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ delay: i * 0.03 }}
              >
                <Card className="overflow-hidden hover:shadow-lg transition-all">
                  <CardContent className="p-0">
                    {editingId === video?.id ? (
                      /* Edit Mode */
                      <div className="p-4 space-y-4">
                        <div className="flex items-center justify-between">
                          <h3 className="font-medium text-sm">Video Düzenleme</h3>
                          <button onClick={() => setEditingId(null)} className="text-muted-foreground hover:text-foreground">
                            <X className="w-4 h-4" />
                          </button>
                        </div>
                        <div className="space-y-3">
                          <div>
                            <label className="text-xs text-muted-foreground mb-1 block">Başlık</label>
                            <Input
                              value={editForm.title}
                              onChange={(e: React.ChangeEvent<HTMLInputElement>) => setEditForm(prev => ({ ...prev, title: e.target.value }))}
                            />
                          </div>
                          <div>
                            <label className="text-xs text-muted-foreground mb-1 block">Açıklama</label>
                            <textarea
                              value={editForm.description}
                              onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setEditForm(prev => ({ ...prev, description: e.target.value }))}
                              className="w-full min-h-[100px] px-3 py-2 rounded-md border border-input bg-background text-sm resize-y"
                            />
                          </div>
                          <div>
                            <label className="text-xs text-muted-foreground mb-1 block">Gizlilik</label>
                            <div className="flex gap-2">
                              {privacyOptions.map(opt => {
                                const Icon = opt.icon;
                                return (
                                  <button
                                    key={opt.value}
                                    onClick={() => setEditForm(prev => ({ ...prev, privacyStatus: opt.value }))}
                                    className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm border transition-all ${
                                      editForm.privacyStatus === opt.value
                                        ? 'border-primary bg-primary/10 text-foreground'
                                        : 'border-border text-muted-foreground hover:border-primary/50'
                                    }`}
                                  >
                                    <Icon className={`w-4 h-4 ${opt.color}`} />
                                    {opt.label}
                                  </button>
                                );
                              })}
                            </div>
                          </div>
                        </div>
                        <div className="flex justify-end gap-2">
                          <Button variant="outline" size="sm" onClick={() => setEditingId(null)}>İptal</Button>
                          <Button size="sm" onClick={saveEdit} disabled={saving}>
                            {saving ? <Loader2 className="w-4 h-4 animate-spin mr-1" /> : <Save className="w-4 h-4 mr-1" />}
                            Kaydet
                          </Button>
                        </div>
                      </div>
                    ) : (
                      /* View Mode */
                      <div className="flex gap-4 p-4">
                        <div className="relative w-40 aspect-video rounded overflow-hidden bg-muted flex-shrink-0">
                          {video?.thumbnail ? (
                            <Image src={video.thumbnail} alt={video?.title ?? 'Video'} fill className="object-cover" />
                          ) : (
                            <div className="flex items-center justify-center h-full">
                              <Eye className="w-5 h-5 text-muted-foreground" />
                            </div>
                          )}
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-start justify-between gap-2">
                            <div className="min-w-0">
                              <h3 className="font-medium text-sm truncate">{video?.title ?? 'Başlıksız'}</h3>
                              <p className="text-xs text-muted-foreground mt-1 line-clamp-2">
                                {video?.description?.slice(0, 150) ?? ''}
                              </p>
                            </div>
                            <Button variant="ghost" size="sm" onClick={() => startEdit(video)} className="flex-shrink-0">
                              <Edit2 className="w-4 h-4" />
                            </Button>
                          </div>
                          <div className="flex items-center gap-4 mt-3 text-xs text-muted-foreground">
                            <span className="flex items-center gap-1">
                              {getPrivacyIcon(video?.privacyStatus ?? 'private')}
                              {privacyOptions.find(o => o.value === video?.privacyStatus)?.label ?? 'Bilinmiyor'}
                            </span>
                            <span className="flex items-center gap-1">
                              <Eye className="w-3 h-3" />
                              {(video?.viewCount ?? 0).toLocaleString('tr-TR')}
                            </span>
                            <span>
                              {video?.publishedAt ? new Date(video.publishedAt).toLocaleDateString('tr-TR') : ''}
                            </span>
                            {Object.keys(video?.localizations ?? {}).length > 0 && (
                              <span className="flex items-center gap-1 text-primary">
                                <Globe className="w-3 h-3" />
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
            <p className="text-center text-muted-foreground py-12">Video bulunamadı</p>
          )}

          {nextPageToken && (
            <div className="flex justify-center pt-4">
              <Button
                variant="outline"
                onClick={() => fetchVideos(searchQuery, nextPageToken)}
                disabled={loading}
              >
                {loading ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : <ChevronDown className="w-4 h-4 mr-2" />}
                Daha Fazla Yükle
              </Button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
