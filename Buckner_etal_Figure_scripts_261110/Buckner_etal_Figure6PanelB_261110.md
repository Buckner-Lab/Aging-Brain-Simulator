# Buckner et al., Figure 6B: Nondemented sample, hippocampal volume and episodic memory at 80–84

Simulator: `AgingBrain_Simulator_261023.html` (version 99; default world: seed 7, 120,000 lives, study year 2026)
Run: `node run_panel_261110.mjs Buckner_etal_Figure6PanelB_261110.md`
Draws the first sample of 400 people aged 80–84 in 2026 by the Nondemented criterion, measures each once with the default errors,
and correlates hippocampal volume (adjusted for intracranial volume and sex) with episodic memory (adjusted for sex).
Paper: r = 0.31; everyone alive at 80–84, r = 0.46.

```js
const w = state.run.agg.w26, m = (r, k) => anObs(w, r, k), mean = (a) => a.reduce((s, v) => s + v, 0) / a.length;
const resid = (y, X) => { const b = olsFit(X, y); return y.map((v, i) => v - X[i].reduce((s, x, j) => s + x * b[j], 0)); };
const adjR = (rows) => pearson(resid(rows.map((r) => m(r, 'hip')), rows.map((r) => [1, m(r, 'tiv'), w.fem[r]])),   // hip ~ head size + sex
                               resid(rows.map((r) => m(r, 'mem')), rows.map((r) => [1, w.fem[r]])));                 // memory ~ sex
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
const sel = draw('Nondemented', 80, 84, 1), band = [];
for (let r = 0; r < w.n; r++) if (w.age[r] >= 80 && w.age[r] <= 84) band.push(r);        // everyone alive at 80-84 (reference)
return { strategy: 'Nondemented', n: sel.length, r: +adjR(sel).toFixed(2), mean_hippocampus_mL: +mean(sel.map((r) => m(r, 'hip'))).toFixed(2),
         reference_n: band.length, reference_r: +adjR(band).toFixed(2) };
```
