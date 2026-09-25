// node render/record.mjs <mode> <w> <h> <outdir> [extra query] -> PNG frames of build/viewer.html?record=1 (deterministic clock)
import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';
import { serve } from './render.mjs';
const [mode, w, h, out, extra = ''] = process.argv.slice(2);
fs.mkdirSync(out, { recursive: true });
const srv = await serve();
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: +w, height: +h } });
p.on('pageerror', e => console.log('ERR', e.message));
await p.goto(`http://127.0.0.1:${srv.address().port}/${process.env.VIEWER || 'build/viewer.html'}?record=1&mode=${mode}&w=${w}&h=${h}${extra}`);
await p.waitForFunction(() => window.__ready, null, { timeout: 600000 });
const n = await p.evaluate(() => window.__frames);
const cv = p.locator('canvas'); const t0 = Date.now();
for (let f = 0; f < n; f++) {
  await p.evaluate(f => window.__frame(f), f);
  await cv.screenshot({ path: path.join(out, `f_${String(f).padStart(5, '0')}.png`) });
  if (f % 100 === 0) console.log(mode, f, '/', n, ((Date.now() - t0) / 1000).toFixed(0) + 's');
}
await b.close(); srv.close(); console.log('done', n);
