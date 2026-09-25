// Usage: node render/render.mjs <model path rel. to project root> <out.png> [key=value ...]  (keys passed to scene.html)
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json' };

export function serve() {
  const srv = http.createServer((req, res) => {
    const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
    if (!p.startsWith(ROOT)) { res.writeHead(403); return res.end(); }
    // LDraw lookups are case-insensitive on real systems; try lower-case fallback
    let f = p;
    if (!fs.existsSync(f)) f = path.join(path.dirname(p), path.basename(p).toLowerCase());
    if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'text/plain' });
    fs.createReadStream(f).pipe(res);
  });
  return new Promise(r => srv.listen(0, '127.0.0.1', () => r(srv)));
}

export async function render(page, port, model, out, opts = {}) {
  const qs = new URLSearchParams({ model: '/' + model, ...opts });
  await page.setViewportSize({ width: +(opts.w || 1200), height: +(opts.h || 900) });
  await page.goto(`http://127.0.0.1:${port}/render/scene.html?${qs}`);
  await page.waitForFunction(() => window.RENDER_DONE, null, { timeout: 600000 });
  await page.locator('canvas').screenshot({ path: out });
  return page.evaluate(() => window.RENDER_DONE);
}

if (process.argv[1] && import.meta.url.endsWith(path.basename(process.argv[1]))) {
  const [model, out, ...kv] = process.argv.slice(2);
  const opts = Object.fromEntries(kv.map(s => s.split('=')));
  const srv = await serve();
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--enable-unsafe-swiftshader'] });
  const page = await browser.newPage();
  page.on('console', m => { if (m.type() === 'error' && !m.text().includes('Failed to load resource')) console.error('[page]', m.text()); });
  const info = await render(page, srv.address().port, model, out, opts);
  console.log(JSON.stringify(info));
  await browser.close(); srv.close();
}
