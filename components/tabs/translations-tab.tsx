'use client';

import { useState, useEffect, useCallback } from 'react';
import {
  Languages,
  Check,
  Trash2,
  Plus,
  Loader2,
  Search,
  Globe,
  ChevronDown,
  ChevronUp,
  X,
  CheckSquare,
  Square,
} from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'sonner';
import { SUPPORTED_LANGUAGES, type Language } from '@/lib/languages';
import Image from 'next/image';
import { TranslationProgress, type ProgressItem } from '@/components/translation-progress';

interface VideoItem {
  id: string;
  title: string;
  thumbnail: string;
  publishedAt: string;
  viewCount: number;
  localizations: Record<string, { title: string; description: string }>;
}

export function TranslationsTab() {
  const [videos, setVideos] = useState<VideoItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedVideos, setSelectedVideos] = useState<Set<string>>(new Set());
  const [selectedLanguages, setSelectedLanguages] = useState<Set<string>>(new Set());
  const [searchQuery, setSearchQuery] = useState('');
  const [adding, setAdding] = useState(false);
  const [deleting, setDeleting] = useState<string | null>(null);
  const [expandedVideo, setExpandedVideo] = useState<string | null>(null);
  const [showLangPicker, setShowLangPicker] = useState(false);
  const [langSearch, setLangSearch] = useState('');

  const [progressOpen, setProgressOpen] = useState(false);
  const [progressItems, setProgressItems] = useState<ProgressItem[]>([]);
  const [progressLanguages, setProgressLanguages] = useState<string[]>([]);
  const [progressTotal, setProgressTotal] = useState(0);
  const [progressProcessed, setProgressProcessed] = useState(0);
  const [progressDone, setProgressDone] = useState(false);
  const [progressSuccess, setProgressSuccess] = useState(0);
  const [progressFail, setProgressFail] = useState(0);

  const fetchVideos = useCallback(async (query?: string) => {
    setLoading(true);
    try {
      let url = '/api/youtube/videos?';
      if (query) url += `q=${encodeURIComponent(query)}&`;
      const res = await fetch(url);
      const data = await res.json();
      if (data?.error) {
        toast.error(data.error);
      } else {
        setVideos(data?.videos ?? []);
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

  const toggleVideo = (id: string) => {
    setSelectedVideos((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const toggleLanguage = (code: string) => {
    setSelectedLanguages((prev) => {
      const next = new Set(prev);
      if (next.has(code)) next.delete(code);
      else next.add(code);
      return next;
    });
  };

  const filteredVideos = (videos ?? []).filter(
    (video) => !searchQuery || (video?.title ?? '').toLowerCase().includes(searchQuery.toLowerCase())
  );

  const filteredLanguages = (SUPPORTED_LANGUAGES ?? []).filter(
    (language) =>
      !langSearch ||
      (language?.name ?? '').toLowerCase().includes(langSearch.toLowerCase()) ||
      (language?.nativeName ?? '').toLowerCase().includes(langSearch.toLowerCase()) ||
      (language?.code ?? '').toLowerCase().includes(langSearch.toLowerCase())
  );

  const selectAllVideos = () => {
    if (selectedVideos.size === filteredVideos.length) {
      setSelectedVideos(new Set());
      return;
    }

    setSelectedVideos(new Set(filteredVideos.map((video) => video?.id).filter(Boolean)));
  };

  const getLangName = (code: string) => {
    return SUPPORTED_LANGUAGES.find((language) => language?.code === code)?.name ?? code;
  };

  const addTranslations = async () => {
    if (selectedVideos.size === 0 || selectedLanguages.size === 0) {
      toast.error('Lütfen video ve dil seçin');
      return;
    }

    const videoIds = Array.from(selectedVideos);
    const languages = Array.from(selectedLanguages);

    const titleMap = new Map<string, string>();
    videos.forEach((video) => {
      if (video?.id) titleMap.set(video.id, video.title ?? video.id);
    });

    setProgressItems(
      videoIds.map((id) => ({
        videoId: id,
        videoTitle: titleMap.get(id) ?? id,
        status: 'pending' as const,
      }))
    );
    setProgressLanguages(languages);
    setProgressTotal(videoIds.length);
    setProgressProcessed(0);
    setProgressDone(false);
    setProgressSuccess(0);
    setProgressFail(0);
    setProgressOpen(true);
    setAdding(true);

    try {
      const res = await fetch('/api/youtube/translations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ videoIds, languages }),
      });

      if (!res.ok || !res.body) {
        const errData = await res.json().catch(() => ({}));
        toast.error(errData?.error ?? 'Çeviri eklenemedi');
        setProgressDone(true);
        return;
      }

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() ?? '';

        for (const line of lines) {
          if (!line.trim()) continue;

          try {
            const event = JSON.parse(line);

            if (event.type === 'processing') {
              setProgressItems((prev) =>
                prev.map((item) =>
                  item.videoId === event.videoId ? { ...item, status: 'processing' as const } : item
                )
              );
            } else if (event.type === 'result') {
              setProgressProcessed(event.index);
              setProgressItems((prev) =>
                prev.map((item) => {
                  if (item.videoId !== event.videoId) return item;

                  const nextTitle = event.videoTitle ?? item.videoTitle;
                  const hasAdded = (event.addedLanguages?.length ?? 0) > 0;
                  const hasSkipped = (event.skippedLanguages?.length ?? 0) > 0;

                  if (event.success) {
                    if (event.skipped || (!hasAdded && hasSkipped)) {
                      return {
                        ...item,
                        videoTitle: nextTitle,
                        status: 'skipped' as const,
                        skippedLanguages: event.skippedLanguages ?? [],
                      };
                    }

                    return {
                      ...item,
                      videoTitle: nextTitle,
                      status: 'success' as const,
                      addedLanguages: event.addedLanguages ?? [],
                      skippedLanguages: event.skippedLanguages ?? [],
                    };
                  }

                  if (hasAdded || hasSkipped) {
                    return {
                      ...item,
                      videoTitle: nextTitle,
                      status: 'partial' as const,
                      addedLanguages: event.addedLanguages ?? [],
                      skippedLanguages: event.skippedLanguages ?? [],
                      error: event.error,
                    };
                  }

                  return {
                    ...item,
                    videoTitle: nextTitle,
                    status: 'error' as const,
                    error: event.error,
                    skippedLanguages: event.skippedLanguages ?? [],
                  };
                })
              );
            } else if (event.type === 'done') {
              setProgressSuccess(event.successCount ?? 0);
              setProgressFail(event.failCount ?? 0);
              setProgressDone(true);

              if ((event.failCount ?? 0) === 0) {
                toast.success(`${event.successCount} video için çeviriler eklendi`);
              } else {
                toast.warning(`${event.successCount} başarılı, ${event.failCount} başarısız`);
              }
            }
          } catch {
            // Ignore malformed NDJSON rows.
          }
        }
      }

      setSelectedVideos(new Set());
      setSelectedLanguages(new Set());
      fetchVideos(searchQuery);
    } catch (err: any) {
      toast.error(err?.message ?? 'Çeviri eklenemedi');
      setProgressDone(true);
    } finally {
      setAdding(false);
    }
  };

  const closeProgress = () => {
    if (!adding) {
      setProgressOpen(false);
    }
  };

  const deleteTranslation = async (videoId: string, langCode: string) => {
    const key = `${videoId}-${langCode}`;
    setDeleting(key);

    try {
      const res = await fetch('/api/youtube/translations', {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ videoId, language: langCode }),
      });
      const data = await res.json();

      if (data?.error) {
        toast.error(data.error);
      } else {
        toast.success('Çeviri silindi');
        fetchVideos(searchQuery);
      }
    } catch (err: any) {
      toast.error(err?.message ?? 'Silme başarısız');
    } finally {
      setDeleting(null);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="font-display text-2xl font-bold tracking-tight">Çeviri Yönetimi</h2>
        <p className="mt-1 text-sm text-muted-foreground">
          Videolarınıza çoklu dil çevirisi ekleyin veya mevcut çevirileri yönetin
        </p>
      </div>

      <Card>
        <CardContent className="pt-6">
          <div className="space-y-4">
            <div>
              <div className="mb-2 flex items-center justify-between">
                <label className="flex items-center gap-2 text-sm font-medium">
                  <Languages className="h-4 w-4 text-primary" />
                  Hedef Diller
                  {selectedLanguages.size > 0 && (
                    <span className="rounded-full bg-primary px-2 py-0.5 text-xs text-primary-foreground">
                      {selectedLanguages.size} seçili
                    </span>
                  )}
                </label>
                <Button variant="ghost" size="sm" onClick={() => setShowLangPicker(!showLangPicker)}>
                  {showLangPicker ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                </Button>
              </div>

              {selectedLanguages.size > 0 && (
                <div className="mb-3 flex flex-wrap gap-2">
                  {Array.from(selectedLanguages).map((code) => (
                    <span
                      key={code}
                      className="inline-flex items-center gap-1 rounded-md bg-primary/10 px-2 py-1 text-xs font-medium text-primary"
                    >
                      {getLangName(code)}
                      <button onClick={() => toggleLanguage(code)} className="hover:text-destructive">
                        <X className="h-3 w-3" />
                      </button>
                    </span>
                  ))}
                </div>
              )}

              <AnimatePresence>
                {showLangPicker && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    className="overflow-hidden"
                  >
                    <div className="rounded-lg border border-border p-3">
                      <div className="relative mb-3">
                        <Search className="absolute left-2 top-1/2 h-3 w-3 -translate-y-1/2 text-muted-foreground" />
                        <Input
                          placeholder="Dil ara..."
                          value={langSearch}
                          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setLangSearch(e.target.value)}
                          className="h-8 pl-7 text-xs"
                        />
                      </div>
                      <div className="grid max-h-[200px] grid-cols-2 gap-1.5 overflow-y-auto sm:grid-cols-3 md:grid-cols-4">
                        {filteredLanguages.map((language) => (
                          <button
                            key={language.code}
                            onClick={() => toggleLanguage(language.code)}
                            className={`flex items-center gap-2 rounded px-2 py-1.5 text-left text-xs transition-all ${
                              selectedLanguages.has(language.code)
                                ? 'bg-primary/15 font-medium text-primary'
                                : 'text-foreground hover:bg-accent'
                            }`}
                          >
                            {selectedLanguages.has(language.code) ? (
                              <Check className="h-3 w-3 flex-shrink-0" />
                            ) : (
                              <div className="h-3 w-3 flex-shrink-0" />
                            )}
                            <span className="truncate">{language.name}</span>
                            <span className="ml-auto text-muted-foreground">({language.code})</span>
                          </button>
                        ))}
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            <div className="flex items-center gap-3">
              <Button
                onClick={addTranslations}
                disabled={adding || selectedVideos.size === 0 || selectedLanguages.size === 0}
                className="flex-shrink-0"
              >
                {adding ? (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                ) : (
                  <Plus className="mr-2 h-4 w-4" />
                )}
                Çeviri Ekle
                {selectedVideos.size > 0 && selectedLanguages.size > 0 && (
                  <span className="ml-1 text-xs opacity-80">
                    ({selectedVideos.size} video × {selectedLanguages.size} dil)
                  </span>
                )}
              </Button>
              <p className="text-xs text-muted-foreground">
                Seçili videolara seçili dillerdeki çevirileri ekler
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="flex items-center gap-3">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Video ara..."
            value={searchQuery}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setSearchQuery(e.target.value)}
            className="pl-10"
          />
        </div>
        <Button variant="outline" size="sm" onClick={selectAllVideos}>
          {selectedVideos.size === filteredVideos.length && filteredVideos.length > 0 ? (
            <CheckSquare className="mr-1 h-4 w-4" />
          ) : (
            <Square className="mr-1 h-4 w-4" />
          )}
          Tümünü Seç
        </Button>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-20">
          <div className="h-8 w-8 animate-spin rounded-full border-b-2 border-primary" />
        </div>
      ) : (
        <div className="space-y-2">
          {filteredVideos.map((video, index) => {
            const localizationKeys = Object.keys(video?.localizations ?? {});
            const isExpanded = expandedVideo === video?.id;
            const isSelected = selectedVideos.has(video?.id ?? '');

            return (
              <motion.div
                key={video?.id ?? index}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.02 }}
              >
                <Card
                  className={`overflow-hidden transition-all ${
                    isSelected ? 'ring-2 ring-primary shadow-md' : 'hover:shadow-md'
                  }`}
                >
                  <CardContent className="p-0">
                    <div className="flex items-center gap-3 p-3">
                      <button onClick={() => toggleVideo(video?.id ?? '')} className="flex-shrink-0 p-1">
                        {isSelected ? (
                          <CheckSquare className="h-5 w-5 text-primary" />
                        ) : (
                          <Square className="h-5 w-5 text-muted-foreground" />
                        )}
                      </button>

                      <div className="relative aspect-video w-24 flex-shrink-0 overflow-hidden rounded bg-muted">
                        {video?.thumbnail ? (
                          <Image src={video.thumbnail} alt={video?.title ?? 'Video'} fill className="object-cover" />
                        ) : null}
                      </div>

                      <div className="min-w-0 flex-1">
                        <h3 className="truncate text-sm font-medium">{video?.title ?? 'Başlıksız'}</h3>
                        <div className="mt-1 flex items-center gap-3 text-xs text-muted-foreground">
                          <span>
                            {video?.publishedAt ? new Date(video.publishedAt).toLocaleDateString('tr-TR') : ''}
                          </span>
                          <span>{(video?.viewCount ?? 0).toLocaleString('tr-TR')} görüntüleme</span>
                        </div>
                      </div>

                      <div className="flex flex-shrink-0 items-center gap-2">
                        {localizationKeys.length > 0 && (
                          <span className="flex items-center gap-1 rounded-full bg-primary/10 px-2 py-1 text-xs text-primary">
                            <Globe className="h-3 w-3" />
                            {localizationKeys.length}
                          </span>
                        )}
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => setExpandedVideo(isExpanded ? null : (video?.id ?? null))}
                        >
                          {isExpanded ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                        </Button>
                      </div>
                    </div>

                    <AnimatePresence>
                      {isExpanded && (
                        <motion.div
                          initial={{ height: 0, opacity: 0 }}
                          animate={{ height: 'auto', opacity: 1 }}
                          exit={{ height: 0, opacity: 0 }}
                          className="overflow-hidden"
                        >
                          <div className="border-t border-border px-4 pb-4 pt-1">
                            <h4 className="mb-2 mt-2 text-xs font-medium text-muted-foreground">Mevcut Çeviriler</h4>
                            {localizationKeys.length === 0 ? (
                              <p className="text-xs italic text-muted-foreground">Henüz çeviri yok</p>
                            ) : (
                              <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
                                {localizationKeys.map((langCode) => {
                                  const localization = video?.localizations?.[langCode];
                                  const langName = getLangName(langCode);
                                  const isDeleting = deleting === `${video?.id}-${langCode}`;

                                  return (
                                    <div
                                      key={langCode}
                                      className="flex items-center justify-between rounded-md bg-muted/50 p-2 text-sm"
                                    >
                                      <div className="min-w-0 flex-1">
                                        <div className="flex items-center gap-2">
                                          <span className="rounded bg-background px-1.5 py-0.5 font-mono text-xs">
                                            {langCode}
                                          </span>
                                          <span className="text-xs font-medium">{langName}</span>
                                        </div>
                                        <p className="mt-0.5 truncate text-xs text-muted-foreground">
                                          {localization?.title ?? ''}
                                        </p>
                                      </div>
                                      <button
                                        onClick={() => deleteTranslation(video?.id ?? '', langCode)}
                                        disabled={isDeleting}
                                        className="ml-2 flex-shrink-0 p-1 text-muted-foreground transition-colors hover:text-destructive"
                                      >
                                        {isDeleting ? (
                                          <Loader2 className="h-3 w-3 animate-spin" />
                                        ) : (
                                          <Trash2 className="h-3 w-3" />
                                        )}
                                      </button>
                                    </div>
                                  );
                                })}
                              </div>
                            )}
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </CardContent>
                </Card>
              </motion.div>
            );
          })}

          {filteredVideos.length === 0 && (
            <p className="py-12 text-center text-muted-foreground">Video bulunamadı</p>
          )}
        </div>
      )}

      <TranslationProgress
        open={progressOpen}
        items={progressItems}
        languages={progressLanguages}
        total={progressTotal}
        processed={progressProcessed}
        done={progressDone}
        successCount={progressSuccess}
        failCount={progressFail}
        onClose={closeProgress}
      />
    </div>
  );
}
