import fs from 'node:fs/promises';

const selectedPath = 'D:/A-klasör/Youtube/selected_french_thumbnail_videos.json';
const statusPath = 'D:/A-klasör/Youtube/pin_status.jsonl';

const desiredComment = `Vos questions sont les bienvenues en commentaire — j'y réponds personnellement, une par une.

Ce canal reste gratuit et informatif. Si vous souhaitez être suivie/accompagné par notre équipe pour un traitement (FIV, laparoscopie, bilan de fertilité), c'est ici :

WhatsApp : https://wa.me/905073802805?text=Bonjour%2C%20je%20souhaite%20commencer%20un%20suivi%20avec%20le%20Dr%20Senai%20Aksoy.%0A%0ARef%3A%20yt-fr-pin

www.draksoyivf.com

🇬🇧 To start a treatment with our team (IVF, laparoscopy, fertility check-up), message us on WhatsApp (link above). For questions, just comment below.

🇸🇦 لبدء العلاج مع فريقنا (أطفال الأنابيب، تنظير البطن، تقييم الخصوبة)، راسلونا على واتساب (الرابط أعلاه). وللأسئلة، اكتبوا في التعليقات.

️ Ce canal est informatif et ne remplace pas une consultation personnalisée.`;

async function writeStatus(obj) {
  try {
    await fs.appendFile(statusPath, JSON.stringify({ ...obj, at: new Date().toISOString() }) + '\n', 'utf8');
  } catch (e) {
    obj.statusWriteError = String(e?.message ?? e);
  }
}

async function okIdsFromStatus() {
  let txt = '';
  try {
    txt = await fs.readFile(statusPath, 'utf8');
  } catch {}
  const ok = new Set();
  for (const line of txt.split(/\r?\n/)) {
    if (!line.trim()) continue;
    try {
      const j = JSON.parse(line.replace(/^\uFEFF/, ''));
      if (j.ok === true) ok.add(j.id);
    } catch {}
  }
  return ok;
}

export async function createYoutubePinRunner(browser) {
  const selectedItems = JSON.parse(await fs.readFile(selectedPath, 'utf8'));
  const tab = await browser.tabs.new();

  async function wait(ms) {
    await tab.playwright.waitForTimeout(ms);
  }

  async function openWatch(id) {
    await tab.goto(`https://www.youtube.com/watch?v=${id}`);
    await tab.playwright.waitForLoadState({ state: 'domcontentloaded', timeoutMs: 20000 });
    await wait(1200);
  }

  async function scrollToComments() {
    for (let i = 0; i < 4; i++) {
      const placeholderCount = await tab.playwright.locator('#placeholder-area').count();
      const snap = await tab.playwright.domSnapshot();
      if (
        placeholderCount > 0 ||
        snap.includes('Yorumlar devre dışı') ||
        snap.includes('Yorumlar kapalı') ||
        snap.includes('Yorum" [level=2]') ||
        snap.includes('Yorumlar')
      ) {
        return snap;
      }
      await tab.cua.scroll({ x: 600, y: 700, scrollY: 1000, scrollX: 0 });
      await wait(500);
    }
    return await tab.playwright.domSnapshot();
  }

  async function pasteIntoActiveCommentBox(text) {
    await tab.clipboard.writeText(text);
    const box = tab.playwright.locator('#contenteditable-root');
    const count = await box.count();
    if (count < 1) throw new Error('No contenteditable-root');
    await box.nth(0).click({});
    await box.nth(0).press('Control+A', {});
    await box.nth(0).press('Control+V', {});
    await wait(350);
  }

  async function clickTextOption(labels) {
    for (const label of labels) {
      const loc = tab.playwright.getByText(label, { exact: true });
      const c = await loc.count();
      if (c === 1) {
        await loc.click({});
        return label;
      }
      const menuItem = tab.playwright.getByRole('menuitem', { name: label });
      const mc = await menuItem.count();
      if (mc > 0) {
        await menuItem.nth(mc - 1).click({ timeoutMs: 5000 });
        return label;
      }
    }
    return null;
  }

  async function confirmPinIfShown() {
    for (let i = 0; i < 8; i++) {
      const confirm = tab.playwright.getByRole('button', { name: 'Sabitle' });
      const cc = await confirm.count();
      if (cc === 1) {
        await confirm.click({ timeoutMs: 10000 });
        await wait(1500);
        return true;
      }
      await wait(250);
    }
    return false;
  }

  async function editExistingPinned() {
    const menus = tab.playwright.getByRole('button', { name: 'İşlem menüsü' });
    const mc = await menus.count();
    if (mc < 1) throw new Error('No comment action menu');
    await menus.nth(0).click({});
    await wait(400);
    const editLabel = await clickTextOption(['Düzenle', 'Edit']);
    if (!editLabel) {
      try {
        await tab.playwright.locator('body').press('Escape', {});
      } catch {}
      return { edited: false, reason: 'no-edit-option' };
    }
    await wait(500);
    await pasteIntoActiveCommentBox(desiredComment);
    let save = tab.playwright.getByRole('button', { name: 'Kaydet' });
    let sc = await save.count();
    if (sc !== 1) save = tab.playwright.getByRole('button', { name: 'Save' });
    sc = await save.count();
    if (sc !== 1) throw new Error('Save button not found');
    if (await save.isEnabled()) {
      await save.click({ timeoutMs: 10000 });
      await wait(1800);
      return { edited: true, saved: true };
    }
    const cancel = tab.playwright.getByRole('button', { name: 'İptal' });
    if ((await cancel.count()) === 1) await cancel.click({});
    return { edited: true, saved: false, reason: 'already-same' };
  }

  async function postNewCommentAndPin() {
    const placeholder = tab.playwright.locator('#placeholder-area');
    const pc = await placeholder.count();
    if (pc < 1) throw new Error('Comment placeholder not found');
    await placeholder.nth(0).click({});
    await wait(500);
    await pasteIntoActiveCommentBox(desiredComment);
    let submit = tab.playwright.getByRole('button', { name: 'Yorum yap' });
    let subc = await submit.count();
    if (subc !== 1) submit = tab.playwright.getByRole('button', { name: 'Comment' });
    subc = await submit.count();
    if (subc !== 1) throw new Error('Submit comment button not found');
    if (!(await submit.isEnabled())) throw new Error('Submit button disabled');
    await submit.click({ timeoutMs: 10000 });
    await wait(2500);
    const menus = tab.playwright.getByRole('button', { name: 'İşlem menüsü' });
    const mc = await menus.count();
    if (mc < 1) throw new Error('No action menu after posting');
    await menus.nth(0).click({});
    await wait(400);
    const pinLabel = await clickTextOption(['Sabitle', 'Pin']);
    if (!pinLabel) throw new Error('Pin option not found');
    await wait(600);
    const pinButtons = tab.playwright.getByRole('button', { name: 'Sabitle' });
    const pbc = await pinButtons.count();
    if (pbc === 1) {
      await pinButtons.click({ timeoutMs: 10000 });
      await wait(1200);
    } else {
      await confirmPinIfShown();
    }
    const got = (await tab.playwright.domSnapshot()).includes('@SenaiAksoy tarafından sabitlendi');
    return { posted: true, pinned: got };
  }

  async function pinThread(thread) {
    const menu = thread.getByRole('button', { name: 'İşlem menüsü' });
    const mc = await menu.count();
    if (mc !== 1) throw new Error(`Expected one thread action menu, found ${mc}`);
    await menu.click({ timeoutMs: 5000 });
    await wait(500);
    const pinLabel = await clickTextOption(['Sabitle', 'Pin']);
    if (!pinLabel) throw new Error('Pin option not found for existing thread');
    await confirmPinIfShown();
    return (await tab.playwright.domSnapshot()).includes('@SenaiAksoy tarafından sabitlendi');
  }

  async function editExistingOwnContactAndPin() {
    const threads = tab.playwright
      .locator('ytd-comment-thread-renderer')
      .filter({ has: tab.playwright.locator('a[href="/@SenaiAksoy"]') })
      .filter({ has: tab.playwright.locator('a[href*="905073802805"]') });
    const tc = await threads.count();
    if (tc < 1) return { foundExistingContact: false };

    const thread = threads.nth(0);
    const menu = thread.getByRole('button', { name: 'İşlem menüsü' });
    const mc = await menu.count();
    if (mc !== 1) return { foundExistingContact: true, reason: `contact-menu-count-${mc}` };
    await menu.click({ timeoutMs: 5000 });
    await wait(500);
    const editLabel = await clickTextOption(['Düzenle', 'Edit']);
    if (!editLabel) {
      try {
        await tab.playwright.locator('body').press('Escape', {});
      } catch {}
      return { foundExistingContact: true, reason: 'contact-no-edit-option' };
    }
    await wait(500);
    await pasteIntoActiveCommentBox(desiredComment);
    let save = tab.playwright.getByRole('button', { name: 'Kaydet' });
    let sc = await save.count();
    if (sc !== 1) save = tab.playwright.getByRole('button', { name: 'Save' });
    sc = await save.count();
    if (sc !== 1) throw new Error('Save button not found for existing contact');
    if (await save.isEnabled()) {
      await save.click({ timeoutMs: 10000 });
      await wait(1800);
    } else {
      const cancel = tab.playwright.getByRole('button', { name: 'İptal' });
      if ((await cancel.count()) === 1) await cancel.click({});
    }
    const pinned = await pinThread(thread);
    return { foundExistingContact: true, editedExistingContact: true, pinned };
  }

  async function updateOne(item) {
    const result = { id: item.id, type: item.type, index: item.index, ok: false };
    try {
      await openWatch(item.id);
      const snap = await scrollToComments();
      if (snap.includes('Yorumlar devre dışı') || snap.includes('Yorumlar kapalı')) {
        result.skipped = 'comments-disabled';
      } else if (snap.includes('@SenaiAksoy tarafından sabitlendi')) {
        result.action = 'edit-pinned';
        Object.assign(result, await editExistingPinned());
        const verify = await tab.playwright.domSnapshot();
        result.ok =
          verify.includes('@SenaiAksoy tarafından sabitlendi') &&
          verify.includes('Ref%3A%20yt-fr-pin') &&
          verify.includes('www.draksoyivf.com');
      } else {
        const existing = await editExistingOwnContactAndPin();
        if (existing.foundExistingContact && existing.editedExistingContact) {
          result.action = 'edit-existing-contact-pin';
          Object.assign(result, existing);
        } else {
          result.action = 'post-pin';
          Object.assign(result, existing, await postNewCommentAndPin());
        }
        const verify = await tab.playwright.domSnapshot();
        result.ok =
          verify.includes('@SenaiAksoy tarafından sabitlendi') &&
          verify.includes('Ref%3A%20yt-fr-pin') &&
          verify.includes('www.draksoyivf.com');
      }
    } catch (e) {
      result.error = String(e?.message ?? e);
    }
    await writeStatus(result);
    return result;
  }

  async function runNextBatch(n) {
    const ok = await okIdsFromStatus();
    const pending = selectedItems.filter((x) => !ok.has(x.id));
    const todo = pending.slice(0, n);
    const results = [];
    for (const item of todo) results.push(await updateOne(item));
    const ok2 = await okIdsFromStatus();
    return {
      processed: results.map((r) => ({
        index: r.index,
        type: r.type,
        id: r.id,
        ok: r.ok,
        action: r.action,
        error: r.error,
        skipped: r.skipped,
      })),
      done: ok2.size,
      total: selectedItems.length,
      remaining: selectedItems.length - ok2.size,
    };
  }

  return { runNextBatch, selectedItems, tab };
}
