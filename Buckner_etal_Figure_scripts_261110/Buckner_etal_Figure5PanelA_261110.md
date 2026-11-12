# Buckner et al., Figure 5A: selection changes the cross-sectional decline of episodic memory with age

Simulator: `AgingBrain_Simulator_261023.html` (version 99; default world: seed 7, 120,000 lives, study year 2026)
Run: `node run_panel_261110.mjs Buckner_etal_Figure5PanelA_261110.md`
Ages 60–90 in 2026, three criteria in true values (none; MMSE ≥ 24; MMSE ≥ 24 with amyloid < 12 CL and tau < 1.25 SUVR). Each is sampled
100 times (seeds 1–100; 220 women, 180 men), memory is measured once, and memory is regressed on age (slope × 10 = SD per decade).
Paper: samples average −0.68, −0.51 and −0.49 SD per decade; everyone alive, −0.68. Left plot: true mean by year of age (3-year running mean).

```js
const w = state.run.agg.w26, mean = (a) => a.reduce((s, v) => s + v, 0) / a.length;
const slope10 = (rows, f) => { const x = rows.map((r) => w.age[r]), y = rows.map(f), mx = mean(x), my = mean(y);
  let sxy = 0, sxx = 0; x.forEach((v, i) => { sxy += (v - mx) * (y[i] - my); sxx += (v - mx) ** 2; }); return 10 * sxy / sxx; };
const crit = { 'Everyone': ['random', {}], 'MMSE >= 24': ['nondem', { by: 'mmse', mmse: 24, bneg: false }],
  'MMSE >= 24, amyloid < 12 CL, tau < 1.25 SUVR': ['nondem', { by: 'mmse', mmse: 24, bneg: true, bAmy: 12, bTau: 1.25 }] };
const slopes = [], curve = [];
for (const [name, [strat, q]] of Object.entries(crit)) {
  const sl = [];
  for (let seed = 1; seed <= 100; seed++) {
    Object.assign(state.sel, { strat, seed }); Object.assign(state.sel.q[strat], q, { lo: 60, hi: 90, n: 400, women: 55 });
    sl.push(slope10(runSelection().sel, (r) => anObs(w, r, 'mem')));        // measured once, default error
  }
  const all = runSelection().meet;                                           // everyone alive at 60-90 who qualifies
  slopes.push({ criterion: name, qualified: all.length, mean_of_100_sample_slopes: +mean(sl).toFixed(2),
    range: `${Math.min(...sl).toFixed(2)} to ${Math.max(...sl).toFixed(2)}`, all_qualified_true: +slope10(all, (r) => wv(w, r, 'mem')).toFixed(2) });
  const byAge = (a) => all.filter((r) => Math.abs(w.age[r] - a) <= 1).map((r) => wv(w, r, 'mem'));   // centered 3-year window
  curve.push(Object.fromEntries([['criterion', name], ...[61, 65, 70, 75, 80, 85, 89].map((a) => [`age ${a}`, +mean(byAge(a)).toFixed(2)])]));
}
return { slopes_SD_per_decade: slopes, left_plot_true_mean_memory: curve };
```
