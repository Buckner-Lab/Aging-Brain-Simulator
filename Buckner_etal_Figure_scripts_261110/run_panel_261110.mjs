// run_panel_261110.mjs: runs the code block of one Buckner_etal_FigureXPanelY_261110.md inside the simulator file it names, and prints the result.
// Usage: node run_panel_261110.mjs Buckner_etal_Figure6PanelF_261110.md [folder holding the simulator .html files; default: the .md's folder]
// Needs Node 18+ and Playwright (npm i playwright && npx playwright install chromium).
// The only change to the simulator is one added line that lets the panel's code run inside the application's own scope,
// so it can use state, E (the engine), wv, anObs, runSelection and every other internal the developer guide describes.
import { readFileSync, writeFileSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve, dirname } from 'node:path';
import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)('playwright');

const md = process.argv[2];
if (!md) { console.error('usage: node run_panel_261110.mjs <panel .md> [simulator folder]'); process.exit(1); }
const dir = process.argv[3] || dirname(resolve(md));
const text = readFileSync(md, 'utf8');
const file = (text.match(/^Simulator: `([^`]+)`/m) || [])[1];
const code = [...text.matchAll(/```js\n([\s\S]*?)```/g)].map((m) => m[1]).join('\n');
if (!file || !code) { console.log('This panel has no analysis to run (see its notes).'); process.exit(0); }
let html = readFileSync(join(dir, file), 'utf8');
// optional source edits a panel declares (Figure 5F carries the v91 branch's generational settings into version 99)
for (const m of text.matchAll(/```patch\n([\s\S]*?)\n=>\n([\s\S]*?)\n```/g)) {
  if (!html.includes(m[1])) throw new Error('patch target not found:\n' + m[1]);
  html = html.replace(m[1], () => m[2]);
}
const tail = /init\(\);\s*\}\)\(\);\s*<\/script>/;
if (!tail.test(html)) throw new Error('unexpected file layout');
html = html.replace(tail, (m) => 'window.__run = (src) => eval(src);\n' + m);
const tmp = join(mkdtempSync(join(tmpdir(), 'ab-')), file);
writeFileSync(tmp, html);

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1400, height: 900 } });
page.on('pageerror', (e) => console.error('page error:', e.message));
await page.goto('file://' + tmp);
await page.waitForFunction(() => window.__abReady === true, null, { timeout: 0 });
const t0 = Date.now();
const out = await page.evaluate((src) => window.__run(`(async () => {\n${src}\n})()`), code);
await browser.close();

// print: a table for a list of rows, an indented list for an object of values, one line for everything else
const cell = (v) => (v === undefined || v === null ? '' : typeof v === 'string' ? v : JSON.stringify(v));
function table(rows) {
  const cols = [...new Set(rows.flatMap((r) => Object.keys(r)))], txt = rows.map((r) => cols.map((c) => cell(r[c])));
  const wd = cols.map((c, i) => Math.max(c.length, ...txt.map((t) => t[i].length)));
  const num = cols.map((c) => rows.every((r) => r[c] == null || typeof r[c] === 'number'));
  const line = (t) => t.map((s, i) => (num[i] ? s.padStart(wd[i]) : s.padEnd(wd[i]))).join('  ').trimEnd();
  console.log(line(cols)); console.log(wd.map((n) => '-'.repeat(n)).join('  ')); txt.forEach((t) => console.log(line(t)));
}
for (const [k, v] of Object.entries(out || {})) {
  if (Array.isArray(v) && v.length && typeof v[0] === 'object' && !Array.isArray(v[0])) { console.log(`\n${k}`); table(v); console.log(''); }
  else if (v && typeof v === 'object' && !Array.isArray(v)) { console.log(`${k}:`); for (const [a, b] of Object.entries(v)) console.log(`  ${a}: ${cell(b)}`); }
  else console.log(`${k}: ${cell(v)}`);
}
console.log(`\n(${file}; analysis ${((Date.now() - t0) / 1000).toFixed(1)} s)`);
