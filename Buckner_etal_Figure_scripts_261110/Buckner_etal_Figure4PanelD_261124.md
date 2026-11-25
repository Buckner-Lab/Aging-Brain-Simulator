# Buckner et al., Figure 4D: 100 A4-like trials of a therapy that clears 30% of plaque, the effect accumulated over 2 to 10 years

Simulator: `AgingBrain_Simulator_v104_261115.html` (version 104; default world: seed 7, 120,000 lives, study year 2026)
Run: `node run_panel_261110.mjs Buckner_etal_Figure4PanelD_261124.md`
The app's A4 strategy at 33 Centiloid (ages 65–85, CDR-SB 0; 720 women, 480 men; selected on true values), trials 1–100 (selection seed = allocation
seed), half treated with a therapy that clears 30% of plaque from the year after entry, in the AD cascade expanded so that the plaque drives all of tau's
rise and AD's toll comes with that rise (xDrv 100; path weights xwL 0, xwC 1, xwA 0, which leave every untreated life as the world's own); memory
measured every 6 months with error and practice; Welch's t on the participants' slopes. Plotted: each trial's difference in mean slope (treated minus
control) times trial length, orange for benefit and red for harm at p < 0.05; the true effect (each participant's slope with the therapy minus without,
averaged) times trial length; and, above each length, the power to detect the true effect, Φ(μ/σ − 1.96), with μ the mean true effect and σ the SD
(ddof 0) of the 100 estimates.
Paper: 4,801 eligible; about 1,180 analyzed per trial; power 9% at 2 years rising to 25% at 10; one significant harm (at 4 years).
Figure: power 9, 15, 19, 23 and 25%; true effect 0.021, 0.048, 0.080, 0.115 and 0.151 SD; significant benefit in 9, 15, 18, 17 and 19 trials.

```js
const w = state.run.agg.w26, mean = (a) => a.reduce((s, v) => s + v, 0) / a.length, j = E.IX.mem, X = 0.30, LEN = [2, 4, 6, 8, 10];
Object.assign(state.sel, { strat: 'a4', meas: false }); Object.assign(state.sel.q.a4, { lo: 65, hi: 85, n: 1200, women: 60, amy: 33, cdr: 0, e4: 'any' });
Object.assign(state.iv, { kind: 'ad', x: 50, share: 50, y: 'mem', step: 6, meas: true, prac: true }); IVC.run = null;
// the therapy: the AD cascade expanded (plaque drives all of tau's rise, AD's toll comes with that rise), 30% of the plaque cleared from the year after entry
const pX = { ...state.run.p, ad: false, adx: true, xwL: 0, xwC: 1, xwA: 0, xDrv: 100 }, cache = new Map();
const treated = (w2, r) => { const id = w2.id[r];
  if (!cache.has(id)) cache.set(id, fuFrom(E.trace(id, pX, state.run.k, state.run.S.saRef, { a0: w2.age[r], kind: 'amy', x: X }), w2, r));
  return cache.get(id); };
const MX = mxOn('iv'), sl = (recs) => recs.map((p) => p.slope).filter(Number.isFinite), res = Object.fromEntries(LEN.map((y) => [y, []]));
let eligible = 0;
for (let seed = 1; seed <= 100; seed++) {
  state.sel.seed = seed; state.iv.seed = seed;
  const R = runSelection(), { T, C } = ivArms(R); eligible = R.meet.length;
  for (const yrs of LEN) {
    state.iv.yrs = yrs; const ys = anVisits(state.iv);
    const rT = sl(anRecs(w, T, ys, j, true, treated, true, MX)), rC = sl(anRecs(w, C, ys, j, true, fuOf, true, MX));   // what the trial sees
    const eff = ivDiff(anMean(rT), anMean(rC));                                                                          // treated minus control, Welch's t
    const all = T.concat(C), on = anRecs(w, all, ys, j, false, treated), off = anRecs(w, all, ys, j, false, fuOf);      // true values, both ways
    const tru = mean(on.map((p, i) => p.slope - off[i].slope).filter(Number.isFinite));
    res[yrs].push({ seed, d: eff.d, p: eff.p, tru, n: rT.length + rC.length });
  }
}
const Phi = (z) => { const t = 1 / (1 + 0.3275911 * Math.abs(z) / Math.SQRT2);                                          // standard normal CDF
  const e = t * (0.254829592 + t * (-0.284496736 + t * (1.421413741 + t * (-1.453152027 + t * 1.061405429)))) * Math.exp(-z * z / 2);
  return 0.5 * (1 + Math.sign(z) * (1 - e)); };
const sd = (a) => { const m = mean(a); return Math.sqrt(mean(a.map((v) => (v - m) ** 2))); };
const ben = (t) => t.p < 0.05 && t.d > 0, harm = (t) => t.p < 0.05 && t.d < 0;
return { eligible,
  by_length: LEN.map((yrs) => { const a = res[yrs], mu = mean(a.map((t) => t.tru)), s = sd(a.map((t) => t.d));
    return { years: yrs, power: `${Math.round(100 * Phi(mu / s - 1.96))}%`, significant_benefit: a.filter(ben).length, significant_harm: a.filter(harm).length,
      true_effect_SD_per_yr: +mu.toFixed(4), true_effect_accumulated_SD: +(mu * yrs).toFixed(3), sd_of_estimates_SD_per_yr: +s.toFixed(4),
      analyzed_per_trial: Math.round(mean(a.map((t) => t.n))) }; }),
  significant_harm: LEN.flatMap((yrs) => res[yrs].filter(harm).map((t) => ({ trial: t.seed, years: yrs, accumulated_SD: +(t.d * yrs).toFixed(3), p: +t.p.toFixed(4) }))),
  trials_accumulated_SD: res[2].map((_, i) => ({ trial: i + 1, ...Object.fromEntries(LEN.map((yrs) => [`${yrs} y`, +(res[yrs][i].d * yrs).toFixed(3)])),
    benefit_at: LEN.filter((yrs) => ben(res[yrs][i])).join(', '), harm_at: LEN.filter((yrs) => harm(res[yrs][i])).join(', ') })) };
```
