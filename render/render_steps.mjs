// Render every step of every section in build/instructions/steps.json -> build/instructions/img/<key>_<n>.png
// plus a thumbnail of every part lot -> build/instructions/img/part_<part>_<color>.png.
import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';
import { serve } from './render.mjs';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const INS = path.join(ROOT, process.env.INS || 'build/instructions'), IMG = path.join(INS, 'img');
fs.mkdirSync(IMG, { recursive: true });
const book = JSON.parse(fs.readFileSync(path.join(INS, 'steps.json')));
const only = process.argv[2];

const srv = await serve(); const port = srv.address().port;
const browser = await chromium.launch({ args: ['--use-gl=angle', '--enable-unsafe-swiftshader'] });
const page = await browser.newPage();
page.on('pageerror', e => console.error('[pageerror]', e.message));

const VIEW = { base: { zoom: 1.05 }, gajo: { az: 30, el: 28, zoom: 1.15 }, anillo: { az: 200, el: 30, zoom: 1.05 },
  anillo_base: { az: 200, el: 30, zoom: 1.05 }, pilares: { az: 200, el: 35, zoom: 1.1 }, plaza: { az: 200, el: 40, zoom: 1.3 },
  plaza_place: { az: 200, el: 35, zoom: 1.05 }, cupula: { az: 200, el: 35, zoom: 1.05 }, entrada: { az: 200, el: 22, zoom: 1.05 } };

async function load(model, opts, w = 900, h = 820) {
  await page.setViewportSize({ width: w, height: h });
  const qs = new URLSearchParams({ model: '/' + model, w, h, bg: '#ffffff', ...opts });
  await page.goto(`http://127.0.0.1:${port}/render/steps.html?${qs}`);
  await page.waitForFunction(() => window.READY, null, { timeout: 900000 });
}

for (const sec of book.sections) {
  if (only && sec.key !== only && only !== 'sections') continue;
  const t0 = Date.now();
  await load((process.env.INS || 'build/instructions') + '/' + sec.ldr, VIEW[sec.key] || {});
  const n = await page.evaluate(() => window.nSteps);
  for (let k = sec.context_steps; k < n; k++) {
    await page.evaluate(k => window.setStep(k), k);
    await page.locator('canvas').screenshot({ path: path.join(IMG, `${sec.key}_${k - sec.context_steps + 1}.png`) });
  }
  // final view of the section (no fading)
  await page.evaluate(k => window.setStep(k, false, false), n - 1);
  await page.locator('canvas').screenshot({ path: path.join(IMG, `${sec.key}_final.png`) });
  console.log(sec.key, n - sec.context_steps, 'steps', ((Date.now() - t0) / 1000).toFixed(1) + 's');
}

if (!only || only === 'parts') {
  // part thumbnails
  const lots = new Map();
  for (const b of book.bom) lots.set(`${b.part}_${b.color}`, b);
  for (const [k, b] of lots) {
    const f = path.join(INS, 'tmp_part.ldr');
    fs.writeFileSync(f, `0 part\n0 STEP\n1 ${b.color} 0 0 0 1 0 0 0 1 0 0 0 1 ${b.part}\n0 STEP\n`);
    await load((process.env.INS || 'build/instructions') + '/tmp_part.ldr', { az: 35, el: 30, zoom: 1.0, bg: '#ffffff', hot: '0' }, 200, 160);
    await page.evaluate(() => window.setStep(1, false));
    await page.locator('canvas').screenshot({ path: path.join(IMG, `part_${b.part.replace('.dat', '')}_${b.color}.png`) });
  }
  console.log('parts', lots.size);
}
await browser.close(); srv.close();
