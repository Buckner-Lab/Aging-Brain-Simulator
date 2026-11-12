# Buckner et al., Figure 6F: median correlation of 100 samples per strategy at four ages

Simulator: `AgingBrain_Simulator_261023.html` (version 99; default world: seed 7, 120,000 lives, study year 2026)
Run: `node run_panel_261110.mjs Buckner_etal_Figure6PanelF_261110.md`
For each 5-year band in 2026 (70–74 to 85–89) and each strategy, draws samples 1–100 of 400 (seeds 1–100), measures once with the
default errors, and gives the median and 2.5th–97.5th percentiles of the adjusted hippocampus–memory correlation (as in Figure 6A–E).
At 85–89, every NW SuperAger and biomarker-negative sample holds the same people (too few qualify).

```js
const w = state.run.agg.w26, m = (r, k) => anObs(w, r, k), mean = (a) => a.reduce((s, v) => s + v, 0) / a.length;
const resid = (y, X) => { const b = olsFit(X, y); return y.map((v, i) => v - X[i].reduce((s, x, j) => s + x * b[j], 0)); };
const adjR = (rows) => pearson(resid(rows.map((r) => m(r, 'hip')), rows.map((r) => [1, m(r, 'tiv'), w.fem[r]])),   // hip ~ head size + sex
                               resid(rows.map((r) => m(r, 'mem')), rows.map((r) => [1, w.fem[r]])));                 // memory ~ sex
// Northwestern rule in true values: memory >= mean of dementia-free 56-66; executive function and semantic memory no more
// than 1 SD (population SD) below the mean of dementia-free people of the same 5-year group; drawn as the app draws SuperAgers.
function nwSample(lo, hi, seed) {
  const free = (a, b) => { const x = []; for (let r = 0; r < w.n; r++) if (!w.dem[r] && w.age[r] >= a && w.age[r] <= b) x.push(r); return x; };
  const mu = (rows, k) => mean(rows.map((r) => wv(w, r, k))), sd = (rows, k) => { const u = mu(rows, k); return Math.sqrt(mean(rows.map((r) => (wv(w, r, k) - u) ** 2))); };
  const nrm = free(56, 66), grp = free(lo, hi), memCut = mu(nrm, 'mem'), exeCut = mu(grp, 'exe') - sd(grp, 'exe'), semCut = mu(grp, 'sem') - sd(grp, 'sem');
  const meet = grp.filter((r) => wv(w, r, 'mem') >= memCut && wv(w, r, 'exe') >= exeCut && wv(w, r, 'sem') >= semCut);
  const s = (seed * 2654435761 + SEL_SEEDK.indexOf('super') * 97 + state.run.p.seed) >>> 0;
  return { meet, sel: seededShuffle(meet.filter((r) => w.fem[r]), s).slice(0, 240).concat(seededShuffle(meet.filter((r) => !w.fem[r]), s ^ 0x5bd1e995).slice(0, 160)) };
}
// draw sample `seed` of a strategy at ages lo-hi, as the app's Selection stage does (55% women; SuperAgers 60%)
function draw(name, lo, hi, seed) {
  if (name === 'NW SuperAger') return nwSample(lo, hi, seed).sel;
  const S = {
    'Random': ['random', { n: 400, women: 55 }],
    'Nondemented': ['nondem', { n: 400, women: 55, by: 'mmse', mmse: 24, bneg: false }],
    'Biomarker negative': ['nondem', { n: 400, women: 55, by: 'mmse', mmse: 24, bneg: true, bAmy: 12, bTau: 1.25 }],
    'MCI': ['mci', { n: 400, women: 55, def: 'bands', cdrLo: 0.5, cdrHi: 2.5, mmLo: 24, mmHi: 30, bpos: false, e4: 'any' }],
  }[name];
  Object.assign(state.sel, { strat: S[0], seed }); Object.assign(state.sel.q[S[0]], S[1], { lo, hi });
  return runSelection().sel;
}
const q = (a, p) => { const s = [...a].sort((x, y) => x - y), h = (s.length - 1) * p, i = Math.floor(h); return s[i] + (h - i) * ((s[i + 1] ?? s[i]) - s[i]); };
const out = [];
for (const lo of [70, 75, 80, 85]) for (const name of ['Random', 'Nondemented', 'Biomarker negative', 'NW SuperAger', 'MCI']) {
  const rs = []; for (let seed = 1; seed <= 100; seed++) rs.push(adjR(draw(name, lo, lo + 4, seed)));
  out.push({ ages: `${lo}-${lo + 4}`, strategy: name, median_r: +q(rs, 0.5).toFixed(3), p2_5: +q(rs, 0.025).toFixed(3), p97_5: +q(rs, 0.975).toFixed(3) });
}
return { medians: out };
```
