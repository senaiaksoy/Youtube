'use client';

import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
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
    try {
      if (window.top && window.top !== window.self) {
        window.top.location.href = `${window.location.origin}/api/auth/google`;
        return;
      }
    } catch {
      window.open(`${window.location.origin}/api/auth/google`, '_blank', 'noopener,noreferrer');
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

  if (!status?.connected) {
    return (
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="mb-6">
        <div className="rounded-xl border border-amber-500/30 bg-gradient-to-r from-amber-500/10 to-orange-500/10 p-5 shadow-sm">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center">
            <div className="flex flex-1 items-start gap-3">
              <div className="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-lg bg-amber-500/20">
                <AlertCircle className="h-5 w-5 text-amber-600 dark:text-amber-400" />
              </div>
              <div>
                <h3 className="font-semibold text-foreground">YouTube hesabı bağlı değil</h3>
                <p className="mt-1 text-sm text-muted-foreground">
                  Uygulamayı kullanabilmek için Google hesabınızla giriş yapın. Bir kez bağlandıktan sonra token
                  otomatik yenilenir.
                </p>
              </div>
            </div>
            <Button onClick={handleConnect} size="lg" className="flex-shrink-0 gap-2">
              <LogIn className="h-4 w-4" />
              Google ile Bağlan
            </Button>
          </div>
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div initial={{ opacity: 0, y: -5 }} animate={{ opacity: 1, y: 0 }} className="mb-6">
      <div className="flex items-center justify-between gap-3 rounded-lg border border-emerald-500/20 bg-emerald-500/5 px-4 py-2.5">
        <div className="flex items-center gap-2 text-sm">
          <CheckCircle2 className="h-4 w-4 text-emerald-600 dark:text-emerald-400" />
          <span className="font-medium text-foreground">YouTube hesabı bağlı</span>
          {status.hasRefreshToken ? (
            <span className="hidden text-xs text-muted-foreground sm:inline">• Otomatik token yenileme aktif</span>
          ) : (
            <span className="hidden text-xs text-amber-600 dark:text-amber-400 sm:inline">
              • Refresh token yok, yeniden bağlanmanız önerilir
            </span>
          )}
        </div>
        <div className="flex items-center gap-2">
          {!status.hasRefreshToken && (
            <Button onClick={handleConnect} size="sm" variant="outline" className="h-8 gap-1.5">
              <LogIn className="h-3.5 w-3.5" />
              Yeniden Bağlan
            </Button>
          )}
          <Button
            onClick={handleDisconnect}
            size="sm"
            variant="ghost"
            disabled={disconnecting}
            className="h-8 gap-1.5 text-muted-foreground hover:text-foreground"
          >
            {disconnecting ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <LogOut className="h-3.5 w-3.5" />}
            <span className="hidden sm:inline">Bağlantıyı Kes</span>
          </Button>
        </div>
      </div>
    </motion.div>
  );
}
