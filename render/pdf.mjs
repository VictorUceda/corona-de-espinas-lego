// build/instructions/book.html -> dist/instrucciones.pdf (Playwright page.pdf)
import path from 'node:path';
import { chromium } from 'playwright';
import { serve } from './render.mjs';
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const srv = await serve();
const b = await chromium.launch(); const p = await b.newPage();
await p.goto('http://127.0.0.1:' + srv.address().port + '/' + (process.env.INS || 'build/instructions') + '/book.html', { waitUntil: 'networkidle' });
await p.pdf({ path: path.join(ROOT, (process.env.PDF || 'dist/instrucciones.pdf')), format: 'A4', landscape: true, printBackground: true, preferCSSPageSize: true });
await b.close(); srv.close(); console.log((process.env.PDF || 'dist/instrucciones.pdf'));
