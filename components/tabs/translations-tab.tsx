'use client';

import { useState, useEffect, useCallback } from 'react';
import { Languages, Check, Trash2, Plus, Loader2, Search, Globe, ChevronDown, ChevronUp, X, CheckSquare, Square } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
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

  // Progress modal state
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
      if (data?.error) toast.error(data.error);
      else setVideos(data?.videos ?? []);
    } catch (err: any) {
      toast.error(err?.message ?? 'Videolar yüklenemedi');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchVideos(); }, [fetchVideos]);

  const toggleVideo = (id: string) => {
    setSelectedVideos(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const selectAllVideos = () => {
    if (selectedVideos.size === filteredVideos.length) {
      setSelectedVideos(new Set());
    } else {
      setSelectedVideos(new Set(filteredVideos.map(v => v?.id).filter(Boolean)));
    }
  };

  const toggleLanguage = (code: string) => {
    setSelectedLanguages(prev => {
      const next = new Set(prev);
      if (next.has(code)) next.delete(code);
      else next.add(code);
      return next;
    });
  };

  const addTranslations = async () => {
    if (selectedVideos.size === 0 || selectedLanguages.size === 0) {
      toast.error('Lütfen video ve dil seçin');
      return;
    }

    const videoIds = Array.from(selectedVideos);
    const languages = Array.from(selectedLanguages);

    // Build a title lookup from current video list for display
    const titleMap = new Map<string, string>();
    videos.forEach((v) => {
      if (v?.id) titleMap.set(v.id, v.title ?? v.id);
    });

    // Open progress modal with initial pending state
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
                  item.videoId === event.videoId
                    ? { ...item, status: 'processing' as const }
                    : item
                )
              );
            } else if (event.type === 'result') {
              setProgressProcessed(event.index);
              setProgressItems((prev) =>
                prev.map((item) => {
                  if (item.videoId !== event.videoId) return item;
                  const newTitle = event.videoTitle ?? item.videoTitle;
                  if (event.success) {
                    if (event.skipped || (event.addedLanguages?.length ?? 0) === 0) {
                      return {
                        ...item,
                        videoTitle: newTitle,
                        status: 'skipped' as const,
                        skippedLanguages: event.skippedLanguages ?? [],
                      };
                    }
                    return {
                      ...item,
                      videoTitle: newTitle,
                      status: 'success' as const,
                      addedLanguages: event.addedLanguages ?? [],
                      skippedLanguages: event.skippedLanguages ?? [],
                    };
                  }
                  return {
                    ...item,
                    videoTitle: newTitle,
                    status: 'error' as const,
                    error: event.error,
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
                toast.warning(
                  `${event.successCount} başarılı, ${event.failCount} başarısız`
                );
              }
            }
          } catch {
            /* ignore malformed line */
          }
        }
      }

      // Clear selections after completion
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
      if (data?.error) toast.error(data.error);
      else {
        toast.success('Çeviri silindi');
        fetchVideos(searchQuery);
      }
    } catch (err: any) {
      toast.error(err?.message ?? 'Silme başarısız');
    } finally {
      setDeleting(null);
    }
  };

  const filteredVideos = (videos ?? []).filter((v: VideoItem) =>
    !searchQuery || (v?.title ?? '').toLowerCase().includes(searchQuery.toLowerCase())
  );

  const filteredLanguages = (SUPPORTED_LANGUAGES ?? []).filter((l: Language) =>
    !langSearch ||
    (l?.name ?? '').toLowerCase().includes(langSearch.toLowerCase()) ||
    (l?.nativeName ?? '').toLowerCase().includes(langSearch.toLowerCase()) ||
    (l?.code ?? '').toLowerCase().includes(langSearch.toLowerCase())
  );

  const getLangName = (code: string) => {
    return SUPPORTED_LANGUAGES.find(l => l?.code === code)?.name ?? code;
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="font-display text-2xl font-bold tracking-tight">Çeviri Yönetimi</h2>
        <p className="text-muted-foreground text-sm mt-1">Videolarınıza çoklu dil çevirisi ekleyin veya mevcut çevirileri yönetin</p>
      </div>

      {/* Action Bar */}
      <Card>
        <CardContent className="pt-6">
          <div className="space-y-4">
            {/* Language Picker */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-sm font-medium flex items-center gap-2">
                  <Languages className="w-4 h-4 text-primary" />
                  Hedef Diller
                  {selectedLanguages.size > 0 && (
                    <span className="bg-primary text-primary-foreground text-xs px-2 py-0.5 rounded-full">
                      {selectedLanguages.size} seçili
                    </span>
                  )}
                </label>
                <Button variant="ghost" size="sm" onClick={() => setShowLangPicker(!showLangPicker)}>
                  {showLangPicker ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                </Button>
              </div>

              {/* Selected Languages Tags */}
              {selectedLanguages.size > 0 && (
                <div className="flex flex-wrap gap-2 mb-3">
                  {Array.from(selectedLanguages).map(code => (
                    <span
                      key={code}
                      className="inline-flex items-center gap-1 px-2 py-1 rounded-md bg-primary/10 text-primary text-xs font-medium"
                    >
                      {getLangName(code)}
                      <button onClick={() => toggleLanguage(code)} className="hover:text-destructive">
                        <X className="w-3 h-3" />
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
                    <div className="border border-border rounded-lg p-3">
                      <div className="relative mb-3">
                        <Search className="absolute left-2 top-1/2 -translate-y-1/2 w-3 h-3 text-muted-foreground" />
                        <Input
                          placeholder="Dil ara..."
                          value={langSearch}
                          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setLangSearch(e.target.value)}
                          className="h-8 pl-7 text-xs"
                        />
                      </div>
                      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-1.5 max-h-[200px] overflow-y-auto">
                        {filteredLanguages.map((lang: Language) => (
                          <button
                            key={lang.code}
                            onClick={() => toggleLanguage(lang.code)}
                            className={`flex items-center gap-2 px-2 py-1.5 rounded text-xs transition-all text-left ${
                              selectedLanguages.has(lang.code)
                                ? 'bg-primary/15 text-primary font-medium'
                                : 'hover:bg-accent text-foreground'
                            }`}
                          >
                            {selectedLanguages.has(lang.code) ? (
                              <Check className="w-3 h-3 flex-shrink-0" />
                            ) : (
                              <div className="w-3 h-3 flex-shrink-0" />
                            )}
                            <span className="truncate">{lang.name}</span>
                            <span className="text-muted-foreground ml-auto">({lang.code})</span>
                          </button>
                        ))}
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            {/* Add Button */}
            <div className="flex items-center gap-3">
              <Button
                onClick={addTranslations}
                disabled={adding || selectedVideos.size === 0 || selectedLanguages.size === 0}
                className="flex-shrink-0"
              >
                {adding ? (
                  <Loader2 className="w-4 h-4 animate-spin mr-2" />
                ) : (
                  <Plus className="w-4 h-4 mr-2" />
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

      {/* Search & Select All */}
      <div className="flex items-center gap-3">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <Input
            placeholder="Video ara..."
            value={searchQuery}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setSearchQuery(e.target.value)}
            className="pl-10"
          />
        </div>
        <Button variant="outline" size="sm" onClick={selectAllVideos}>
          {selectedVideos.size === filteredVideos.length && filteredVideos.length > 0 ? (
            <CheckSquare className="w-4 h-4 mr-1" />
          ) : (
            <Square className="w-4 h-4 mr-1" />
          )}
          Tümünü Seç
        </Button>
      </div>

      {/* Video List */}
      {loading ? (
        <div className="flex items-center justify-center py-20">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
        </div>
      ) : (
        <div className="space-y-2">
          {filteredVideos.map((video: VideoItem, i: number) => {
            const locKeys = Object.keys(video?.localizations ?? {});
            const isExpanded = expandedVideo === video?.id;
            const isSelected = selectedVideos.has(video?.id ?? '');

            return (
              <motion.div
                key={video?.id ?? i}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.02 }}
              >
                <Card className={`overflow-hidden transition-all ${
                  isSelected ? 'ring-2 ring-primary shadow-md' : 'hover:shadow-md'
                }`}>
                  <CardContent className="p-0">
                    <div className="flex items-center gap-3 p-3">
                      {/* Checkbox */}
                      <button
                        onClick={() => toggleVideo(video?.id ?? '')}
                        className="flex-shrink-0 p-1"
                      >
                        {isSelected ? (
                          <CheckSquare className="w-5 h-5 text-primary" />
                        ) : (
                          <Square className="w-5 h-5 text-muted-foreground" />
                        )}
                      </button>

                      {/* Thumbnail */}
                      <div className="relative w-24 aspect-video rounded overflow-hidden bg-muted flex-shrink-0">
                        {video?.thumbnail ? (
                          <Image src={video.thumbnail} alt={video?.title ?? 'Video'} fill className="object-cover" />
                        ) : null}
                      </div>

                      {/* Info */}
                      <div className="flex-1 min-w-0">
                        <h3 className="font-medium text-sm truncate">{video?.title ?? 'Başlıksız'}</h3>
                        <div className="flex items-center gap-3 mt-1 text-xs text-muted-foreground">
                          <span>{video?.publishedAt ? new Date(video.publishedAt).toLocaleDateString('tr-TR') : ''}</span>
                          <span>{(video?.viewCount ?? 0).toLocaleString('tr-TR')} görüntüleme</span>
                        </div>
                      </div>

                      {/* Translations badge & expand */}
                      <div className="flex items-center gap-2 flex-shrink-0">
                        {locKeys.length > 0 && (
                          <span className="bg-primary/10 text-primary text-xs px-2 py-1 rounded-full flex items-center gap-1">
                            <Globe className="w-3 h-3" />
                            {locKeys.length}
                          </span>
                        )}
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => setExpandedVideo(isExpanded ? null : (video?.id ?? null))}
                        >
                          {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                        </Button>
                      </div>
                    </div>

                    {/* Expanded Translations */}
                    <AnimatePresence>
                      {isExpanded && (
                        <motion.div
                          initial={{ height: 0, opacity: 0 }}
                          animate={{ height: 'auto', opacity: 1 }}
                          exit={{ height: 0, opacity: 0 }}
                          className="overflow-hidden"
                        >
                          <div className="px-4 pb-4 pt-1 border-t border-border">
                            <h4 className="text-xs font-medium text-muted-foreground mb-2 mt-2">Mevcut Çeviriler</h4>
                            {locKeys.length === 0 ? (
                              <p className="text-xs text-muted-foreground italic">Henüz çeviri yok</p>
                            ) : (
                              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                                {locKeys.map(langCode => {
                                  const loc = video?.localizations?.[langCode];
                                  const langName = getLangName(langCode);
                                  const isDeleting = deleting === `${video?.id}-${langCode}`;
                                  return (
                                    <div
                                      key={langCode}
                                      className="flex items-center justify-between p-2 rounded-md bg-muted/50 text-sm"
                                    >
                                      <div className="min-w-0 flex-1">
                                        <div className="flex items-center gap-2">
                                          <span className="font-mono text-xs bg-background px-1.5 py-0.5 rounded">{langCode}</span>
                                          <span className="text-xs font-medium">{langName}</span>
                                        </div>
                                        <p className="text-xs text-muted-foreground truncate mt-0.5">{loc?.title ?? ''}</p>
                                      </div>
                                      <button
                                        onClick={() => deleteTranslation(video?.id ?? '', langCode)}
                                        disabled={isDeleting}
                                        className="ml-2 p-1 text-muted-foreground hover:text-destructive transition-colors flex-shrink-0"
                                      >
                                        {isDeleting ? (
                                          <Loader2 className="w-3 h-3 animate-spin" />
                                        ) : (
                                          <Trash2 className="w-3 h-3" />
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
            <p className="text-center text-muted-foreground py-12">Video bulunamadı</p>
          )}
        </div>
      )}

      {/* Translation Progress Modal */}
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
