'use client';

import { useState } from 'react';
import { LayoutDashboard, Video, Languages, Settings } from 'lucide-react';
import { DashboardTab } from '@/components/tabs/dashboard-tab';
import { VideosTab } from '@/components/tabs/videos-tab';
import { TranslationsTab } from '@/components/tabs/translations-tab';
import { AuthBanner } from '@/components/auth-banner';
import { cn } from '@/lib/utils';

const TABS = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { id: 'videos', label: 'Videolar', icon: Video },
  { id: 'translations', label: 'Çeviriler', icon: Languages },
] as const;

type TabId = typeof TABS[number]['id'];

export function AppShell() {
  const [activeTab, setActiveTab] = useState<TabId>('dashboard');

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-background/80 backdrop-blur-md border-b border-border">
        <div className="max-w-[1200px] mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-primary flex items-center justify-center">
              <Video className="w-5 h-5 text-primary-foreground" />
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
                    'flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200',
                    activeTab === tab.id
                      ? 'bg-primary text-primary-foreground shadow-md'
                      : 'text-muted-foreground hover:text-foreground hover:bg-accent'
                  )}
                >
                  <Icon className="w-4 h-4" />
                  <span className="hidden sm:inline">{tab.label}</span>
                </button>
              );
            })}
          </nav>
        </div>
      </header>

      {/* Content */}
      <main className="max-w-[1200px] mx-auto px-4 py-6">
        <AuthBanner />
        {activeTab === 'dashboard' && <DashboardTab />}
        {activeTab === 'videos' && <VideosTab />}
        {activeTab === 'translations' && <TranslationsTab />}
      </main>
    </div>
  );
}
