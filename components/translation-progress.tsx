'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle2, XCircle, Loader2, Globe, Sparkles, X as XIcon } from 'lucide-react';
import { Button } from '@/components/ui/button';

export type ProgressItem = {
  videoId: string;
  videoTitle?: string;
  status: 'pending' | 'processing' | 'success' | 'error' | 'skipped' | 'partial';
  error?: string;
  addedLanguages?: string[];
  skippedLanguages?: string[];
};

type Props = {
  open: boolean;
  items: ProgressItem[];
  languages: string[];
  total: number;
  processed: number;
  done: boolean;
  successCount: number;
  failCount: number;
  onClose: () => void;
};

export function TranslationProgress({
  open,
  items,
  languages,
  total,
  processed,
  done,
  successCount,
  failCount,
  onClose,
}: Props) {
  const percent = total > 0 ? Math.round((processed / total) * 100) : 0;

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 p-4 backdrop-blur-sm"
          onClick={done ? onClose : undefined}
        >
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            onClick={(e) => e.stopPropagation()}
            className="flex max-h-[85vh] w-full max-w-2xl flex-col overflow-hidden rounded-2xl border border-border bg-background shadow-2xl"
          >
            <div className="flex items-center justify-between border-b border-border px-6 py-5">
              <div className="flex items-center gap-3">
                <div
                  className={`flex h-10 w-10 items-center justify-center rounded-xl ${
                    done
                      ? failCount > 0
                        ? 'bg-amber-500/15 text-amber-600 dark:text-amber-400'
                        : 'bg-emerald-500/15 text-emerald-600 dark:text-emerald-400'
                      : 'bg-primary/15 text-primary'
                  }`}
                >
                  {done ? (
                    failCount > 0 ? (
                      <Sparkles className="h-5 w-5" />
                    ) : (
                      <CheckCircle2 className="h-5 w-5" />
                    )
                  ) : (
                    <Loader2 className="h-5 w-5 animate-spin" />
                  )}
                </div>
                <div>
                  <h3 className="font-display text-lg font-semibold">
                    {done
                      ? failCount > 0
                        ? 'Tamamlandı (bazı hatalarla)'
                        : 'Çeviriler başarıyla eklendi'
                      : 'Çeviriler ekleniyor...'}
                  </h3>
                  <p className="mt-0.5 text-xs text-muted-foreground">
                    {done
                      ? `${successCount} başarılı · ${failCount} başarısız · ${languages.length} dil`
                      : `${processed} / ${total} video işleniyor · ${languages.length} dil`}
                  </p>
                </div>
              </div>
              {done && (
                <button
                  onClick={onClose}
                  className="rounded-lg p-2 text-muted-foreground transition-colors hover:bg-accent hover:text-foreground"
                >
                  <XIcon className="h-4 w-4" />
                </button>
              )}
            </div>

            <div className="px-6 pt-4">
              <div className="mb-2 flex items-center justify-between text-xs text-muted-foreground">
                <span className="font-medium">
                  {processed} / {total} video
                </span>
                <span className="font-mono">{percent}%</span>
              </div>
              <div className="h-2 overflow-hidden rounded-full bg-muted">
                <motion.div
                  className={`h-full rounded-full ${
                    done
                      ? failCount > 0
                        ? 'bg-amber-500'
                        : 'bg-emerald-500'
                      : 'bg-primary'
                  }`}
                  initial={{ width: 0 }}
                  animate={{ width: `${percent}%` }}
                  transition={{ duration: 0.3 }}
                />
              </div>
            </div>

            <div className="px-6 pb-2 pt-3">
              <div className="flex flex-wrap items-center gap-2">
                <span className="flex items-center gap-1 text-xs text-muted-foreground">
                  <Globe className="h-3 w-3" />
                  Seçilen diller:
                </span>
                {languages.map((language) => (
                  <span
                    key={language}
                    className="rounded bg-primary/10 px-1.5 py-0.5 font-mono text-xs text-primary"
                  >
                    {language}
                  </span>
                ))}
              </div>
            </div>

            <div className="min-h-[120px] flex-1 space-y-1.5 overflow-y-auto px-6 py-3">
              <AnimatePresence initial={false}>
                {items.map((item) => (
                  <motion.div
                    key={item.videoId}
                    layout
                    initial={{ opacity: 0, y: -5 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0 }}
                    className={`flex items-center gap-3 rounded-lg border px-3 py-2 text-sm ${
                      item.status === 'processing'
                        ? 'border-primary/30 bg-primary/5'
                        : item.status === 'success'
                        ? 'border-emerald-500/20 bg-emerald-500/5'
                        : item.status === 'partial'
                        ? 'border-amber-500/20 bg-amber-500/5'
                        : item.status === 'skipped'
                        ? 'border-border bg-muted/50'
                        : item.status === 'error'
                        ? 'border-red-500/20 bg-red-500/5'
                        : 'border-border'
                    }`}
                  >
                    <div className="flex-shrink-0">
                      {item.status === 'processing' && (
                        <Loader2 className="h-4 w-4 animate-spin text-primary" />
                      )}
                      {item.status === 'success' && (
                        <CheckCircle2 className="h-4 w-4 text-emerald-600 dark:text-emerald-400" />
                      )}
                      {item.status === 'partial' && (
                        <Sparkles className="h-4 w-4 text-amber-600 dark:text-amber-400" />
                      )}
                      {item.status === 'skipped' && (
                        <CheckCircle2 className="h-4 w-4 text-muted-foreground" />
                      )}
                      {item.status === 'error' && (
                        <XCircle className="h-4 w-4 text-red-600 dark:text-red-400" />
                      )}
                      {item.status === 'pending' && (
                        <div className="h-4 w-4 rounded-full border-2 border-muted-foreground/30" />
                      )}
                    </div>
                    <div className="min-w-0 flex-1">
                      <p className="truncate text-sm font-medium">{item.videoTitle ?? item.videoId}</p>
                      {item.status === 'success' && (item.addedLanguages?.length ?? 0) > 0 && (
                        <p className="mt-0.5 text-xs text-emerald-600 dark:text-emerald-400">
                          +{item.addedLanguages!.length} dil eklendi
                          {(item.skippedLanguages?.length ?? 0) > 0 && (
                            <span className="text-muted-foreground">
                              {' · '}
                              {item.skippedLanguages!.length} zaten mevcut
                            </span>
                          )}
                        </p>
                      )}
                      {item.status === 'partial' && (
                        <p className="mt-0.5 text-xs text-amber-600 dark:text-amber-400">
                          +{item.addedLanguages?.length ?? 0} dil eklendi
                          {(item.skippedLanguages?.length ?? 0) > 0 && (
                            <span className="text-muted-foreground">
                              {' · '}
                              {item.skippedLanguages!.length} zaten mevcut
                            </span>
                          )}
                          {item.error && (
                            <span className="text-muted-foreground">
                              {' · '}
                              {item.error}
                            </span>
                          )}
                        </p>
                      )}
                      {item.status === 'skipped' && (
                        <p className="mt-0.5 text-xs text-muted-foreground">
                          Tüm diller zaten mevcut, atlandı
                        </p>
                      )}
                      {item.status === 'processing' && (
                        <p className="mt-0.5 text-xs text-primary">İşleniyor...</p>
                      )}
                      {item.status === 'error' && (
                        <p className="mt-0.5 truncate text-xs text-red-600 dark:text-red-400">
                          {item.error ?? 'Bilinmeyen hata'}
                        </p>
                      )}
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>
            </div>

            {done && (
              <div className="flex items-center justify-between border-t border-border bg-muted/30 px-6 py-4">
                <div className="flex items-center gap-4 text-sm">
                  <span className="flex items-center gap-1.5 text-emerald-600 dark:text-emerald-400">
                    <CheckCircle2 className="h-4 w-4" />
                    <span className="font-medium">{successCount} başarılı</span>
                  </span>
                  {failCount > 0 && (
                    <span className="flex items-center gap-1.5 text-red-600 dark:text-red-400">
                      <XCircle className="h-4 w-4" />
                      <span className="font-medium">{failCount} başarısız</span>
                    </span>
                  )}
                </div>
                <Button onClick={onClose}>Bitti</Button>
              </div>
            )}
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
