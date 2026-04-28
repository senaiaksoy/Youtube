export type AuditSeverity = 'high' | 'medium' | 'low';

export type AuditIssue = {
  severity: AuditSeverity;
  title: string;
  detail: string;
};

export type VideoAuditInput = {
  id: string;
  title: string;
  description: string;
  tags: string[];
  thumbnail: string;
  privacyStatus: string;
  publishedAt: string;
  viewCount: number;
  likeCount: number;
  commentCount: number;
  localizationCount: number;
};

export type VideoAuditResult = VideoAuditInput & {
  score: number;
  grade: 'A' | 'B' | 'C' | 'D';
  issues: AuditIssue[];
  wins: string[];
  engagementRate: number;
};

export type ChannelAuditInput = {
  title: string;
  subscriberCount: number;
  totalViews: number;
  videoCount: number;
  recentVideos: VideoAuditInput[];
};

export type ChannelAuditResult = {
  generatedAt: string;
  score: number;
  grade: 'A' | 'B' | 'C' | 'D';
  channel: {
    title: string;
    subscriberCount: number;
    totalViews: number;
    videoCount: number;
    avgViews: number;
  };
  summary: {
    high: number;
    medium: number;
    low: number;
    publishedVideos: number;
    privateOrUnlistedVideos: number;
    averageVideoScore: number;
  };
  priorities: AuditIssue[];
  videos: VideoAuditResult[];
  references: Array<{
    name: string;
    url: string;
    reason: string;
  }>;
};

const MEDICAL_TERMS = [
  'tedavi',
  'tup bebek',
  'ivf',
  'gebelik',
  'hamile',
  'embriyo',
  'amh',
  'pcos',
  'endometriozis',
  'infertilite',
];

const DISCLAIMER_TERMS = [
  'doktorunuza',
  'hekiminize',
  'muayene',
  'tani',
  'tedavi plani',
  'kisisel degerlendirme',
  'bilgilendirme',
];

const CTA_TERMS = [
  'abone',
  'yorum',
  'randevu',
  'iletisim',
  'web',
  'instagram',
  'soru',
  'paylas',
];

function normalizeText(value: string) {
  return value
    .toLocaleLowerCase('tr-TR')
    .replace(/ı/g, 'i')
    .replace(/ğ/g, 'g')
    .replace(/ü/g, 'u')
    .replace(/ş/g, 's')
    .replace(/ö/g, 'o')
    .replace(/ç/g, 'c');
}

function hasAny(text: string, terms: string[]) {
  const normalized = normalizeText(text);
  return terms.some((term) => normalized.includes(normalizeText(term)));
}

function clampScore(score: number) {
  return Math.max(0, Math.min(100, Math.round(score)));
}

function gradeFromScore(score: number): 'A' | 'B' | 'C' | 'D' {
  if (score >= 85) return 'A';
  if (score >= 70) return 'B';
  if (score >= 55) return 'C';
  return 'D';
}

function issuePenalty(severity: AuditSeverity) {
  if (severity === 'high') return 12;
  if (severity === 'medium') return 7;
  return 3;
}

function countIssues(videos: VideoAuditResult[], severity: AuditSeverity) {
  return videos.reduce((total, video) => total + video.issues.filter((issue) => issue.severity === severity).length, 0);
}

export function auditVideo(video: VideoAuditInput): VideoAuditResult {
  const issues: AuditIssue[] = [];
  const wins: string[] = [];
  const titleLength = video.title.trim().length;
  const descriptionLength = video.description.trim().length;
  const combinedText = `${video.title} ${video.description}`;
  const isMedical = hasAny(combinedText, MEDICAL_TERMS);

  if (titleLength < 35) {
    issues.push({
      severity: 'medium',
      title: 'Baslik kisa',
      detail: 'Baslik arama niyetini ve ana faydayi daha net anlatacak kadar acilmali.',
    });
  } else if (titleLength > 90) {
    issues.push({
      severity: 'medium',
      title: 'Baslik uzun',
      detail: 'Baslik mobil ekranda kesilebilir; ilk 60 karakterde ana vaadi netlestirin.',
    });
  } else {
    wins.push('Baslik uzunlugu iyi aralikta.');
  }

  if (descriptionLength < 250) {
    issues.push({
      severity: 'high',
      title: 'Aciklama zayif',
      detail: 'Aciklama bolumu konu ozeti, izleyici faydasi, kaynak/uyari ve CTA icin genisletilmeli.',
    });
  } else {
    wins.push('Aciklama temel SEO icin yeterli uzunlukta.');
  }

  if (!hasAny(combinedText, CTA_TERMS)) {
    issues.push({
      severity: 'medium',
      title: 'CTA eksik',
      detail: 'Aciklamaya abonelik, yorum, randevu veya iletisim yonlendirmesi eklenmeli.',
    });
  } else {
    wins.push('Aciklamada veya baslikta aksiyon sinyali var.');
  }

  if (isMedical && !hasAny(video.description, DISCLAIMER_TERMS)) {
    issues.push({
      severity: 'high',
      title: 'Medikal uyari eksik',
      detail: 'Saglik iceriginde bilgilendirme amaci ve kisisel muayene gerekliligi net belirtilmeli.',
    });
  }

  if (!video.thumbnail) {
    issues.push({
      severity: 'medium',
      title: 'Thumbnail okunamadi',
      detail: 'Video icin ayirt edici thumbnail varligi kontrol edilmeli.',
    });
  }

  if (video.tags.length < 5) {
    issues.push({
      severity: 'low',
      title: 'Etiket sayisi dusuk',
      detail: 'Birincil konu, semptom/soru varyasyonlari ve kanal kategori etiketleri eklenebilir.',
    });
  } else {
    wins.push('Etiket kapsami temel seviyede iyi.');
  }

  if (video.localizationCount === 0) {
    issues.push({
      severity: 'low',
      title: 'Yerellestirme yok',
      detail: 'Onemli videolara en azindan baslik/aciklama cevirileri eklenebilir.',
    });
  }

  if (video.privacyStatus !== 'public') {
    issues.push({
      severity: 'low',
      title: 'Yayin durumu herkese acik degil',
      detail: 'Audit puanlamasinda gorunurluk dusuk sayildi; bu bilincli bir tercihse sorun degil.',
    });
  }

  const engagementRate = video.viewCount > 0
    ? ((video.likeCount + video.commentCount) / video.viewCount) * 100
    : 0;

  if (video.viewCount >= 100 && engagementRate < 0.5) {
    issues.push({
      severity: 'low',
      title: 'Etkilesim orani dusuk',
      detail: 'Video sonunda soru sorma ve yorum daveti daha belirgin hale getirilebilir.',
    });
  }

  const penalty = issues.reduce((total, issue) => total + issuePenalty(issue.severity), 0);
  const score = clampScore(100 - penalty);

  return {
    ...video,
    score,
    grade: gradeFromScore(score),
    issues,
    wins,
    engagementRate: Number(engagementRate.toFixed(2)),
  };
}

export function auditChannel(input: ChannelAuditInput): ChannelAuditResult {
  const videos = input.recentVideos.map(auditVideo).sort((a, b) => a.score - b.score);
  const averageVideoScore = videos.length > 0
    ? Math.round(videos.reduce((total, video) => total + video.score, 0) / videos.length)
    : 0;
  const privateOrUnlistedVideos = videos.filter((video) => video.privacyStatus !== 'public').length;
  const priorities = videos
    .flatMap((video) => video.issues.map((issue) => ({ ...issue, title: `${video.title || video.id}: ${issue.title}` })))
    .sort((a, b) => issuePenalty(b.severity) - issuePenalty(a.severity))
    .slice(0, 8);

  const score = clampScore(
    averageVideoScore
    - Math.min(10, privateOrUnlistedVideos * 2)
    - Math.min(8, countIssues(videos, 'high') * 2)
  );

  return {
    generatedAt: new Date().toISOString(),
    score,
    grade: gradeFromScore(score),
    channel: {
      title: input.title,
      subscriberCount: input.subscriberCount,
      totalViews: input.totalViews,
      videoCount: input.videoCount,
      avgViews: input.videoCount > 0 ? Math.round(input.totalViews / input.videoCount) : 0,
    },
    summary: {
      high: countIssues(videos, 'high'),
      medium: countIssues(videos, 'medium'),
      low: countIssues(videos, 'low'),
      publishedVideos: videos.filter((video) => video.privacyStatus === 'public').length,
      privateOrUnlistedVideos,
      averageVideoScore,
    },
    priorities,
    videos,
    references: [
      {
        name: 'youtube/api-samples',
        url: 'https://github.com/youtube/api-samples',
        reason: 'YouTube Data API ve Analytics API icin resmi ornek desenleri.',
      },
      {
        name: 'AgriciDaniel/claude-youtube',
        url: 'https://github.com/AgriciDaniel/claude-youtube',
        reason: 'Kanal audit, video SEO, thumbnail ve retention kontrol listeleri icin metodoloji.',
      },
      {
        name: 'eat-pray-ai/yutu',
        url: 'https://github.com/eat-pray-ai/yutu',
        reason: 'YouTube otomasyon ve MCP mimarisi icin fikir kaynagi.',
      },
      {
        name: 'madEffort/youtube-trend-dashboard',
        url: 'https://github.com/madEffort/youtube-trend-dashboard',
        reason: 'Trend, tag, yorum sentiment ve video karsilastirma fikirleri.',
      },
    ],
  };
}
