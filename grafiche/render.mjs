// Esporta i PNG delle grafiche.
// Uso: npm i playwright && node grafiche/render.mjs
import { chromium } from 'playwright';
import { fileURLToPath } from 'url';
import path from 'path';

const dir = path.dirname(fileURLToPath(import.meta.url));

// scale 1 = 1080 px di larghezza (nativo social), 2 = doppia risoluzione.
// Le grafiche sulla baia di Mondello restano a 1x: la foto sorgente è
// piccola e ingrandirla oltre non aggiunge dettaglio.
const pages = [
  { file: 'ferie-agosto-2026-foto.html', targets: [
      { id: 'post',       out: 'innova-ferie-agosto-2026-post.png',        scale: 1 },
      { id: 'story',      out: 'innova-ferie-agosto-2026-story.png',       scale: 1 },
      { id: 'post-luna',  out: 'innova-ferie-agosto-2026-luna-post.png',   scale: 2 },
      { id: 'story-volo', out: 'innova-ferie-agosto-2026-volo-story.png',  scale: 2 },
  ]},
  { file: 'ferie-agosto-2026.html', targets: [
      { id: 'post',   out: 'innova-ferie-agosto-2026-illustrata-post.png',     scale: 2 },
      { id: 'story',  out: 'innova-ferie-agosto-2026-illustrata-story.png',    scale: 2 },
      { id: 'square', out: 'innova-ferie-agosto-2026-illustrata-quadrato.png', scale: 2 },
  ]},
];

const browser = await chromium.launch();
for (const p of pages) {
  for (const scale of [...new Set(p.targets.map(t => t.scale))]) {
    const page = await browser.newPage({ viewport: { width: 1400, height: 1000 }, deviceScaleFactor: scale });
    await page.goto('file://' + path.join(dir, p.file));
    await page.evaluate(() => document.fonts.ready);
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(300);
    for (const t of p.targets.filter(t => t.scale === scale)) {
      await page.locator('#' + t.id).screenshot({ path: path.join(dir, t.out) });
      console.log('✓', t.out, `(${scale}x)`);
    }
    await page.close();
  }
}
await browser.close();
