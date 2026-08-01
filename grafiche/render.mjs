// Esporta i PNG delle grafiche a partire da ferie-agosto-2026.html
// Uso: node grafiche/render.mjs      (richiede playwright + Chromium)
import { chromium } from 'playwright';
import { fileURLToPath } from 'url';
import path from 'path';

const dir = path.dirname(fileURLToPath(import.meta.url));
const targets = [
  { id: 'post',   file: 'innova-ferie-agosto-2026-post.png'   },
  { id: 'story',  file: 'innova-ferie-agosto-2026-story.png'  },
  { id: 'square', file: 'innova-ferie-agosto-2026-quadrato.png'},
];

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1400, height: 1000 }, deviceScaleFactor: 2 });
await page.goto('file://' + path.join(dir, 'ferie-agosto-2026.html'));
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(300);

for (const t of targets) {
  await page.locator('#' + t.id).screenshot({ path: path.join(dir, t.file) });
  console.log('✓', t.file);
}
await browser.close();
