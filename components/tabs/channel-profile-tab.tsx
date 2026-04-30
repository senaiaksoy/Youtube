'use client';

import { Copy, Mail, MapPin, Phone, Globe2 } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { toast } from 'sonner';

const bannerLines = ['Tüp Bebek Sürecinde', 'Doğru Kararlar İçin', 'Bilimsel ve Anlaşılır Rehber'] as const;

const aboutText = `Tüp bebek sürecinde doğru kararlar, güvenilir bilgiyle başlar.

Bu kanalda; tüp bebek, embriyo kalitesi, transfer süreci, AMH, yumurta dondurma, PCOS, endometriozis ve erkek infertilitesi gibi konuları bilimsel veriler ışığında sade, net ve anlaşılır biçimde ele alıyorum.

Amacım, karmaşık bilgileri sadeleştirerek süreci daha iyi anlamanıza, daha doğru sorular sormanıza ve doktor görüşmelerinize daha hazırlıklı gitmenize yardımcı olmak.

Ben Doç. Dr. Senai Aksoy. 30 yıllık deneyimle üreme tıbbı alanında çalışıyorum.

Sorularınızı yorumlarda paylaşabilirsiniz.
İletişim: contact@draksoyivf.com
Telefon: +90 533 254 60 40
Web: www.tupbebek.com
Lotus Nişantaşı, Şişli / İstanbul

Bu kanal bilgilendirme amaçlıdır; tanı ve tedavi için doktor değerlendirmesinin yerine geçmez.`;

async function copyText(label: string, text: string) {
  try {
    await navigator.clipboard.writeText(text);
    toast.success(`${label} panoya kopyalandı`);
  } catch {
    toast.error(`${label} kopyalanamadı`);
  }
}

export function ChannelProfileTab() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="font-display text-2xl font-bold tracking-tight">Kanal Profili</h2>
        <p className="mt-1 text-sm text-muted-foreground">
          Banner ve about metinlerinin site içindeki güncel versiyonu
        </p>
      </div>

      <Card className="overflow-hidden border-primary/20 bg-gradient-to-br from-primary/10 via-background to-background">
        <CardHeader className="flex flex-row items-start justify-between gap-4">
          <div>
            <CardTitle className="font-display text-xl">Banner Metni</CardTitle>
            <p className="mt-1 text-sm text-muted-foreground">YouTube banner yerleşimi için kısa satırlar</p>
          </div>
          <Button variant="outline" size="sm" onClick={() => copyText('Banner metni', bannerLines.join('\n'))}>
            <Copy className="mr-2 h-4 w-4" />
            Kopyala
          </Button>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {bannerLines.map((line) => (
              <p key={line} className="font-display text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
                {line}
              </p>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-start justify-between gap-4">
          <div>
            <CardTitle className="font-display text-xl">About Metni</CardTitle>
            <p className="mt-1 text-sm text-muted-foreground">Kanal açıklaması için nihai kopya</p>
          </div>
          <Button variant="outline" size="sm" onClick={() => copyText('About metni', aboutText)}>
            <Copy className="mr-2 h-4 w-4" />
            Kopyala
          </Button>
        </CardHeader>
        <CardContent className="space-y-5">
          <div className="space-y-4 text-sm leading-7 text-muted-foreground">
            {aboutText.split('\n\n').map((paragraph, index) => (
              <p key={`${index}-${paragraph.slice(0, 20)}`} className={index === 0 ? 'text-base font-medium text-foreground' : ''}>
                {paragraph}
              </p>
            ))}
          </div>

          <div className="grid gap-3 rounded-xl border border-border/60 bg-muted/30 p-4 text-sm sm:grid-cols-2">
            <div className="flex items-center gap-2">
              <Mail className="h-4 w-4 text-primary" />
              <span>contact@draksoyivf.com</span>
            </div>
            <div className="flex items-center gap-2">
              <Phone className="h-4 w-4 text-primary" />
              <span>+90 533 254 60 40</span>
            </div>
            <div className="flex items-center gap-2">
              <Globe2 className="h-4 w-4 text-primary" />
              <span>www.tupbebek.com</span>
            </div>
            <div className="flex items-center gap-2">
              <MapPin className="h-4 w-4 text-primary" />
              <span>Lotus Nişantaşı, Şişli / İstanbul</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
