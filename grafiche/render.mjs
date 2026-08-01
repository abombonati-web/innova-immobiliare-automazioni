// Esporta i PNG delle grafiche a 2x.
// Uso: npm i playwright && node grafiche/render.mjs
import { chromium } from 'playwright';
import { fileURLToPath } from 'url';
import path from 'path';

const dir = path.dirname(fileURLToPath(import.meta.url));

const pages = [
  { file: 'ferie-agosto-2026-foto.html', targets: [
      { id: 'post',   out: 'innova-ferie-agosto-2026-foto-post.png'  },
      { id: 'story',  out: 'innova-ferie-agosto-2026-foto-story.png' },
  ]},
  { file: 'ferie-agosto-2026.html', targets: [
      { id: 'post',   out: 'innova-ferie-agosto-2026-post.png'      },
      { id: 'story',  out: 'innova-ferie-agosto-2026-story.png'     },
      { id: 'square', out: 'innova-ferie-agosto-2026-quadrato.png'  },
  ]},
];

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1400, height: 1000 }, deviceScaleFactor: 2 });

for (const p of pages) {
  await page.goto('file://' + path.join(dir, p.file));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(300);
  for (const t of p.targets) {
    await page.locator('#' + t.id).screenshot({ path: path.join(dir, t.out) });
    console.log('✓', t.out);
  }
}
await browser.close();
