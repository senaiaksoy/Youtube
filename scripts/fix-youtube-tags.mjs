import fs from 'fs';
import path from 'path';

const tokens = JSON.parse(fs.readFileSync(path.join(process.cwd(), 'data', 'google-tokens.json'), 'utf8'));

const updates = {
  '6UwNaQa_di4': [
    'tüp bebek',
    'IVF',
    'infertilite',
    'soğan suyu',
    'akupunktur',
    'bitkisel kür',
    'tüp bebekte akupunktur',
    'tüp bebekte soğan suyu',
    'embriyo transferi sonrası',
    'kanıta dayalı tıp',
    'Cochrane',
    'ESHRE',
    'doç dr senai aksoy',
    'tüp bebekte ek tedaviler',
    'ivf add-ons',
    'gebelik şansı',
    'embriyo tutunması',
    'kadın sağlığı',
  ],
  'DbCrz_VPyC4': [
    'tüp bebek',
    'IVF',
    'infertilite',
    'bağışıklık serumları',
    'intralipid',
    'IVIG',
    'takrolimus',
    'embriyo transferi',
    'embriyo tutunması',
    'ivf add-ons',
    'kanıta dayalı tıp',
    'ESHRE',
    'tekrarlayan tüp bebek başarısızlığı',
    'immünoloji',
    'bağışıklık tedavisi',
    'kısırlık tedavisi',
    'doç dr senai aksoy',
    'gebelik şansı',
  ],
  'wybruaMaIdY': [
    'Embryo Glue',
    'embriyo yapıştırıcısı',
    'tüp bebek',
    'IVF',
    'infertilite',
    'embriyo transferi',
    'embriyo tutunması',
    'hyaluronan',
    'Cochrane',
    'ivf add-ons',
    'kanıta dayalı tıp',
    'blastokist',
    'tüp bebek başarı oranı',
    'doç dr senai aksoy',
    'transfer sonrası',
    'gebelik şansı',
  ],
  'w29IsrwxHWA': [
    'yumurta dondurma',
    'oosit dondurma',
    'fertility preservation',
    'AMH',
    'yumurta rezervi',
    'over rezervi',
    'tüp bebek',
    'IVF',
    'infertilite',
    'vitrifikasyon',
    'ileri yaş gebelik',
    'kaç yumurta gerekir',
    'yumurta kalitesi',
    'gebelik şansı',
    'doç dr senai aksoy',
    'kadın sağlığı',
    'doğurganlık korunması',
  ],
  '1pXII-iRU-U': [
    'azospermi',
    'erkek infertilitesi',
    'Roaccutane',
    'izotretinoin',
    'sperm üretimi',
    'mikroTESE',
    'TESE',
    'non-obstrüktif azospermi',
    'matürasyon aresti',
    'tüp bebek',
    'IVF',
    'infertilite',
    'sperm testi',
    'erkek kısırlığı',
    'doç dr senai aksoy',
    'andrology',
    'retinoik asit',
    'gebelik şansı',
  ],
  'yT2dmjxZ3Qs': [
    'embriyo kalitesi',
    '4AA embriyo',
    '3BB embriyo',
    '5BC embriyo',
    'Gardner sınıflaması',
    'blastokist',
    'embriyo transferi',
    'tüp bebek',
    'IVF',
    'infertilite',
    'embriyo derecelendirme',
    'embriyo raporu',
    'gebelik şansı',
    'doç dr senai aksoy',
    'iyi kalite embriyo',
    'düşük kalite embriyo',
  ],
  'S8xkWrHylTE': [
    'dondurulmuş embriyo transferi',
    'FET',
    'TEC',
    'doğal siklus',
    'yapay siklus',
    'letrozol protokolü',
    'embriyo transferi',
    'tüp bebek',
    'IVF',
    'infertilite',
    'implantasyon penceresi',
    'progesteron',
    'gebelik şansı',
    'preeklampsi',
    'doç dr senai aksoy',
    'rahim hazırlığı',
    'transfer protokolü',
  ],
  '-blY0f_9WCE': [
    'vajinal mikrobiyota',
    'vajinal flora',
    'lactobacillus',
    'tüp bebek',
    'IVF',
    'infertilite',
    'embriyo transferi',
    'probiyotik',
    'vajinal enfeksiyon',
    'klamidya',
    'üreoplazma',
    'tekrarlayan tüp bebek başarısızlığı',
    'endometrium',
    'kadın sağlığı',
    'doç dr senai aksoy',
    'üreme sağlığı',
    'gebelik şansı',
  ],
  '-FxkIwmlO9g': [
    'endometriozis',
    'çikolata kisti',
    'endometrioma',
    'kısırlık',
    'infertilite',
    'tüp bebek',
    'IVF',
    'endometriozis tedavisi',
    'freeze all',
    'skleroterapi',
    'yumurta rezervi',
    'AMH',
    'embriyo transferi',
    'doç dr senai aksoy',
    'kadın sağlığı',
    'gebelik şansı',
    '2025 tedavi stratejileri',
  ],
};

async function api(url, options = {}) {
  const res = await fetch(url, {
    ...options,
    headers: {
      Authorization: `Bearer ${tokens.access_token}`,
      'Content-Type': 'application/json; charset=utf-8',
      ...(options.headers || {}),
    },
  });

  if (!res.ok) {
    throw new Error(`${res.status} ${await res.text()}`);
  }

  return res.json();
}

const ids = Object.keys(updates);
const current = await api(`https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=${ids.join(',')}`);

for (const item of current.items || []) {
  const body = {
    id: item.id,
    snippet: {
      ...item.snippet,
      categoryId: item.snippet?.categoryId || '22',
      tags: updates[item.id],
    },
    status: { ...(item.status || {}) },
  };

  await api('https://www.googleapis.com/youtube/v3/videos?part=snippet,status', {
    method: 'PUT',
    body: JSON.stringify(body),
  });
}

const verify = await api(`https://www.googleapis.com/youtube/v3/videos?part=snippet&id=${ids.join(',')}`);
const report = (verify.items || []).map((item) => {
  const expected = updates[item.id];
  const actual = item.snippet?.tags || [];
  return {
    id: item.id,
    title: item.snippet?.title,
    matches: JSON.stringify(expected) === JSON.stringify(actual),
    badTags: actual.filter((tag) => /[ÃÅÄ]/.test(tag)),
  };
});

console.log(JSON.stringify(report, null, 2));
