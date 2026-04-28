'use client';

import { useState } from 'react';
import { LayoutDashboard, Video, Languages, ShieldCheck } from 'lucide-react';
import { DashboardTab } from '@/components/tabs/dashboard-tab';
import { VideosTab } from '@/components/tabs/videos-tab';
import { TranslationsTab } from '@/components/tabs/translations-tab';
import { AuditTab } from '@/components/tabs/audit-tab';
import { AuthBanner } from '@/components/auth-banner';
import { cn } from '@/lib/utils';

const TABS = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { id: 'videos', label: 'Videolar', icon: Video },
  { id: 'audit', label: 'Audit', icon: ShieldCheck },
  { id: 'translations', label: 'Çeviriler', icon: Languages },
] as const;

type TabId = (typeof TABS)[number]['id'];

export function AppShell() {
  const [activeTab, setActiveTab] = useState<TabId>('dashboard');

  return (
    <div className="min-h-screen bg-background">
      <header className="sticky top-0 z-50 border-b border-border bg-background/80 backdrop-blur-md">
        <div className="mx-auto flex h-16 max-w-[1200px] items-center justify-between px-4">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary">
              <Video className="h-5 w-5 text-primary-foreground" />
            </div>
            <h1 className="font-display text-xl font-bold tracking-tight">YouTube Yönetim</h1>
          </div>
          <nav className="flex items-center gap-1">
            {TABS.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={cn(
                    'flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-medium transition-all duration-200',
                    activeTab === tab.id
                      ? 'bg-primary text-primary-foreground shadow-md'
                      : 'text-muted-foreground hover:bg-accent hover:text-foreground'
                  )}
                >
                  <Icon className="h-4 w-4" />
                  <span className="hidden sm:inline">{tab.label}</span>
                </button>
              );
            })}
          </nav>
        </div>
      </header>

      <main className="mx-auto max-w-[1200px] px-4 py-6">
        <AuthBanner />
        {activeTab === 'dashboard' && <DashboardTab />}
        {activeTab === 'videos' && <VideosTab />}
        {activeTab === 'audit' && <AuditTab />}
        {activeTab === 'translations' && <TranslationsTab />}
      </main>
    </div>
  );
}
