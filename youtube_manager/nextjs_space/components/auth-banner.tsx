'use client';

import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AlertCircle, CheckCircle2, LogIn, LogOut, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { toast } from 'sonner';

type AuthStatus = {
  connected: boolean;
  hasRefreshToken: boolean;
  expiresAt: number | null;
};

export function AuthBanner() {
  const [status, setStatus] = useState<AuthStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [disconnecting, setDisconnecting] = useState(false);

  async function fetchStatus() {
    try {
      const res = await fetch('/api/auth/status');
      const data = await res.json();
      setStatus(data);
    } catch {
      setStatus({ connected: false, hasRefreshToken: false, expiresAt: null });
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchStatus();

    // Check URL params for auth result
    if (typeof window !== 'undefined') {
      const params = new URLSearchParams(window.location.search);
      if (params.get('auth') === 'success') {
        toast.success('Google hesabınız başarıyla bağlandı!');
        window.history.replaceState({}, '', window.location.pathname);
      } else if (params.get('auth_error')) {
        toast.error(`Bağlantı hatası: ${params.get('auth_error')}`);
        window.history.replaceState({}, '', window.location.pathname);
      }
    }
  }, []);

  const handleConnect = () => {
    // If we're in an iframe (like Abacus AI preview panel), break out to top window
    // Google OAuth refuses to run inside iframes for security reasons.
    try {
      if (window.top && window.top !== window.self) {
        window.top.location.href = window.location.origin + '/api/auth/google';
        return;
      }
    } catch {
      // Cross-origin iframe: top is inaccessible. Open in new tab.
      const fullUrl = window.location.origin + '/api/auth/google';
      window.open(fullUrl, '_blank', 'noopener,noreferrer');
      return;
    }
    window.location.href = '/api/auth/google';
  };

  const handleDisconnect = async () => {
    setDisconnecting(true);
    try {
      await fetch('/api/auth/disconnect', { method: 'POST' });
      toast.success('Bağlantı kesildi');
      await fetchStatus();
    } catch {
      toast.error('Bağlantı kesme başarısız');
    } finally {
      setDisconnecting(false);
    }
  };

  if (loading) return null;

  // Not connected - show full-width warning banner
  if (!status?.connected) {
    return (
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-6"
      >
        <div className="rounded-xl border border-amber-500/30 bg-gradient-to-r from-amber-500/10 to-orange-500/10 p-5 shadow-sm">
          <div className="flex flex-col sm:flex-row sm:items-center gap-4">
            <div className="flex items-start gap-3 flex-1">
              <div className="w-10 h-10 rounded-lg bg-amber-500/20 flex items-center justify-center flex-shrink-0">
                <AlertCircle className="w-5 h-5 text-amber-600 dark:text-amber-400" />
              </div>
              <div>
                <h3 className="font-semibold text-foreground">YouTube hesabı bağlı değil</h3>
                <p className="text-sm text-muted-foreground mt-1">
                  Uygulamayı kullanabilmek için Google hesabınızla giriş yapın. Bir kez bağlandıktan sonra token otomatik yenilenir.
                </p>
              </div>
            </div>
            <Button onClick={handleConnect} size="lg" className="flex-shrink-0 gap-2">
              <LogIn className="w-4 h-4" />
              Google ile Bağlan
            </Button>
          </div>
        </div>
      </motion.div>
    );
  }

  // Connected - show compact success bar
  return (
    <motion.div
      initial={{ opacity: 0, y: -5 }}
      animate={{ opacity: 1, y: 0 }}
      className="mb-6"
    >
      <div className="flex items-center justify-between gap-3 rounded-lg border border-emerald-500/20 bg-emerald-500/5 px-4 py-2.5">
        <div className="flex items-center gap-2 text-sm">
          <CheckCircle2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
          <span className="text-foreground font-medium">YouTube hesabı bağlı</span>
          {status.hasRefreshToken ? (
            <span className="text-xs text-muted-foreground hidden sm:inline">• Otomatik token yenileme aktif</span>
          ) : (
            <span className="text-xs text-amber-600 dark:text-amber-400 hidden sm:inline">• Refresh token yok - yeniden bağlanmanız önerilir</span>
          )}
        </div>
        <div className="flex items-center gap-2">
          {!status.hasRefreshToken && (
            <Button onClick={handleConnect} size="sm" variant="outline" className="gap-1.5 h-8">
              <LogIn className="w-3.5 h-3.5" />
              Yeniden Bağlan
            </Button>
          )}
          <Button
            onClick={handleDisconnect}
            size="sm"
            variant="ghost"
            disabled={disconnecting}
            className="gap-1.5 h-8 text-muted-foreground hover:text-foreground"
          >
            {disconnecting ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <LogOut className="w-3.5 h-3.5" />}
            <span className="hidden sm:inline">Bağlantıyı Kes</span>
          </Button>
        </div>
      </div>
    </motion.div>
  );
}
