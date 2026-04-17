'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle2, XCircle, Loader2, Globe, Sparkles, X as XIcon } from 'lucide-react';
import { Button } from '@/components/ui/button';

export type ProgressItem = {
  videoId: string;
  videoTitle?: string;
  status: 'pending' | 'processing' | 'success' | 'error' | 'skipped';
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
          className="fixed inset-0 z-[100] bg-black/60 backdrop-blur-sm flex items-center justify-center p-4"
          onClick={done ? onClose : undefined}
        >
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            onClick={(e) => e.stopPropagation()}
            className="bg-background border border-border rounded-2xl shadow-2xl w-full max-w-2xl max-h-[85vh] flex flex-col overflow-hidden"
          >
            {/* Header */}
            <div className="px-6 py-5 border-b border-border flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div
                  className={`w-10 h-10 rounded-xl flex items-center justify-center ${
                    done
                      ? failCount > 0
                        ? 'bg-amber-500/15 text-amber-600 dark:text-amber-400'
                        : 'bg-emerald-500/15 text-emerald-600 dark:text-emerald-400'
                      : 'bg-primary/15 text-primary'
                  }`}
                >
                  {done ? (
                    failCount > 0 ? (
                      <Sparkles className="w-5 h-5" />
                    ) : (
                      <CheckCircle2 className="w-5 h-5" />
                    )
                  ) : (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  )}
                </div>
                <div>
                  <h3 className="font-display text-lg font-semibold">
                    {done
                      ? failCount > 0
                        ? 'Tamamlandı (bazı hatalarla)'
                        : 'Çeviriler Başarıyla Eklendi'
                      : 'Çeviriler Ekleniyor...'}
                  </h3>
                  <p className="text-xs text-muted-foreground mt-0.5">
                    {done
                      ? `${successCount} başarılı · ${failCount} başarısız · ${languages.length} dil`
                      : `${processed} / ${total} video işleniyor · ${languages.length} dil`}
                  </p>
                </div>
              </div>
              {done && (
                <button
                  onClick={onClose}
                  className="p-2 rounded-lg hover:bg-accent text-muted-foreground hover:text-foreground transition-colors"
                >
                  <XIcon className="w-4 h-4" />
                </button>
              )}
            </div>

            {/* Progress Bar */}
            <div className="px-6 pt-4">
              <div className="flex items-center justify-between text-xs text-muted-foreground mb-2">
                <span className="font-medium">
                  {processed} / {total} video
                </span>
                <span className="font-mono">{percent}%</span>
              </div>
              <div className="h-2 bg-muted rounded-full overflow-hidden">
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

            {/* Language Chips */}
            <div className="px-6 pt-3 pb-2">
              <div className="flex items-center gap-2 flex-wrap">
                <span className="text-xs text-muted-foreground flex items-center gap-1">
                  <Globe className="w-3 h-3" />
                  Eklenen diller:
                </span>
                {languages.map((l) => (
                  <span
                    key={l}
                    className="font-mono text-xs bg-primary/10 text-primary px-1.5 py-0.5 rounded"
                  >
                    {l}
                  </span>
                ))}
              </div>
            </div>

            {/* Items List */}
            <div className="flex-1 overflow-y-auto px-6 py-3 space-y-1.5 min-h-[120px]">
              <AnimatePresence initial={false}>
                {items.map((item) => (
                  <motion.div
                    key={item.videoId}
                    layout
                    initial={{ opacity: 0, y: -5 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0 }}
                    className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm border ${
                      item.status === 'processing'
                        ? 'bg-primary/5 border-primary/30'
                        : item.status === 'success'
                        ? 'bg-emerald-500/5 border-emerald-500/20'
                        : item.status === 'skipped'
                        ? 'bg-muted/50 border-border'
                        : item.status === 'error'
                        ? 'bg-red-500/5 border-red-500/20'
                        : 'border-border'
                    }`}
                  >
                    <div className="flex-shrink-0">
                      {item.status === 'processing' && (
                        <Loader2 className="w-4 h-4 text-primary animate-spin" />
                      )}
                      {item.status === 'success' && (
                        <CheckCircle2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                      )}
                      {item.status === 'skipped' && (
                        <CheckCircle2 className="w-4 h-4 text-muted-foreground" />
                      )}
                      {item.status === 'error' && (
                        <XCircle className="w-4 h-4 text-red-600 dark:text-red-400" />
                      )}
                      {item.status === 'pending' && (
                        <div className="w-4 h-4 rounded-full border-2 border-muted-foreground/30" />
                      )}
                    </div>
                    <div className="min-w-0 flex-1">
                      <p className="truncate font-medium text-sm">
                        {item.videoTitle ?? item.videoId}
                      </p>
                      {item.status === 'success' && (item.addedLanguages?.length ?? 0) > 0 && (
                        <p className="text-xs text-emerald-600 dark:text-emerald-400 mt-0.5">
                          +{item.addedLanguages!.length} dil eklendi
                          {(item.skippedLanguages?.length ?? 0) > 0 && (
                            <span className="text-muted-foreground">
                              {' · '}
                              {item.skippedLanguages!.length} zaten mevcut
                            </span>
                          )}
                        </p>
                      )}
                      {item.status === 'skipped' && (
                        <p className="text-xs text-muted-foreground mt-0.5">
                          Tüm diller zaten mevcut, atlandı
                        </p>
                      )}
                      {item.status === 'processing' && (
                        <p className="text-xs text-primary mt-0.5">İşleniyor...</p>
                      )}
                      {item.status === 'error' && (
                        <p className="text-xs text-red-600 dark:text-red-400 mt-0.5 truncate">
                          {item.error ?? 'Bilinmeyen hata'}
                        </p>
                      )}
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>
            </div>

            {/* Footer */}
            {done && (
              <div className="px-6 py-4 border-t border-border bg-muted/30 flex items-center justify-between">
                <div className="flex items-center gap-4 text-sm">
                  <span className="flex items-center gap-1.5 text-emerald-600 dark:text-emerald-400">
                    <CheckCircle2 className="w-4 h-4" />
                    <span className="font-medium">{successCount} başarılı</span>
                  </span>
                  {failCount > 0 && (
                    <span className="flex items-center gap-1.5 text-red-600 dark:text-red-400">
                      <XCircle className="w-4 h-4" />
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
