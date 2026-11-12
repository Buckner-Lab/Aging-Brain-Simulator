# Buckner et al., Figure 5D: 100 A4-like trials of slowing the AD cascade, analyzed at 2 to 10 years

Simulator: `AgingBrain_Simulator_261023.html` (version 99; default world: seed 7, 120,000 lives, study year 2026)
Run: `node run_panel_261110.mjs Buckner_etal_Figure5PanelD_261110.md`
The app's A4 strategy at 33 Centiloid (ages 65–85, CDR-SB 0; 720 women, 480 men), trials 1–100 (selection seed = allocation seed), half treated
with the AD cascade 50% slower; memory measured every 6 months with error and practice; Welch's t on the participants' slopes.
Paper: 4,801 eligible; about 1,180 analyzed per trial; significant benefit in 4% of trials at 2 years rising to 28% at 10; one significant harm (at 4 years).

```js
const w = state.run.agg.w26, mean = (a) => a.reduce((s, v) => s + v, 0) / a.length, j = E.IX.mem;
Object.assign(state.sel, { strat: 'a4' }); Object.assign(state.sel.q.a4, { lo: 65, hi: 85, n: 1200, women: 60, amy: 33, cdr: 0, e4: 'any' });
Object.assign(state.iv, { kind: 'ad', x: 50, share: 50, y: 'mem', step: 6, meas: true, prac: true });
const res = { 2: [], 4: [], 6: [], 8: [], 10: [] };
for (let seed = 1; seed <= 100; seed++) {
  state.sel.seed = seed; state.iv.seed = seed;
  const R = runSelection(), { T, C } = ivArms(R);
  for (const yrs of [2, 4, 6, 8, 10]) {
    const ys = anVisits({ yrs, step: 6 }), sl = (recs) => recs.map((p) => p.slope).filter(Number.isFinite);
    const rT = anRecs(w, T, ys, j, true, ivOf, true), rC = anRecs(w, C, ys, j, true, fuOf, true);       // what the trial sees
    const eff = ivDiff(anMean(sl(rT)), anMean(sl(rC)));                                                 // treated minus control, Welch's t
    const all = T.concat(C), on = anRecs(w, all, ys, j, false, ivOf), off = anRecs(w, all, ys, j, false, fuOf);   // true values, both ways
    const tru = mean(on.map((p, i) => p.slope - off[i].slope).filter(Number.isFinite));
    res[yrs].push({ d: eff.d, p: eff.p, tru, n: sl(rT).length + sl(rC).length });
  }
}
return { eligible: runSelection().meet.length, trials: Object.entries(res).map(([yrs, a]) => ({ years: +yrs,
  significant_benefit: `${a.filter((t) => t.p < 0.05 && t.d > 0).length}%`, significant_harm: a.filter((t) => t.p < 0.05 && t.d < 0).length,
  mean_estimate_SD_per_yr: +mean(a.map((t) => t.d)).toFixed(4), mean_true_effect: +mean(a.map((t) => t.tru)).toFixed(4),
  analyzed_per_trial: Math.round(mean(a.map((t) => t.n))) })) };
```
