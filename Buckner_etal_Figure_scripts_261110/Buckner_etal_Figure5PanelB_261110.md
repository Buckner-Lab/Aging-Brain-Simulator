# Buckner et al., Figure 5B: cross-sectional and longitudinal estimates of memory decline, with and without practice

Simulator: `AgingBrain_Simulator_261023.html` (version 99; default world: seed 7, 120,000 lives, study year 2026)
Run: `node run_panel_261110.mjs Buckner_etal_Figure5PanelB_261110.md`
Everyone alive in 2026 aged 33–87 with true MMSE ≥ 24 is measured in 2026 and, if alive, five years later (new error; a retest's practice
gain, then the same with the gain removed). Groups by age at entry (centered on 35, 40, …, 85); five-year changes chained from 35.
Paper: 64,615 people; cross-sectional −0.49 SD at 60, −1.47 at 80 and −1.74 at 85; true −0.12 by 60 and −1.78 by 85; longitudinal by 85, −0.77 with practice, −1.78 without.

```js
const w = state.run.agg.w26, mean = (a) => (a.length ? a.reduce((s, v) => s + v, 0) / a.length : NaN);
const rows = []; for (let r = 0; r < w.n; r++) if (w.age[r] >= 33 && w.age[r] <= 87 && wv(w, r, 'mmse') >= 24) rows.push(r);
const withP = anRecs(w, rows, [0, 5], E.IX.mem, true, fuOf, true), noP = anRecs(w, rows, [0, 5], E.IX.mem, true, fuOf, false);  // pts: [year, measured, true]
const G = [35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85], grp = (r) => 5 * Math.round(w.age[r] / 5);
const at = (recs, g, f) => recs.filter((p) => grp(p.r) === g).map(f);
const cross = Object.fromEntries(G.map((g) => [g, mean(at(withP, g, (p) => p.pts[0][1]))]));
const chain = (recs, i) => { let s = 0; const out = { 35: 0 };                                  // sum of mean 5-year changes of successive groups
  for (const g of G.slice(0, -1)) { s += mean(at(recs, g, (p) => p.pts[1] ? p.pts[1][i] - p.pts[0][i] : NaN).filter(Number.isFinite)); out[g + 5] = s; } return out; };
const L = chain(withP, 1), Lnp = chain(noP, 1), Tr = chain(withP, 2);
return { people: rows.length, measured_twice: withP.filter((p) => p.pts.length === 2).length,
  curves: [40, 45, 50, 55, 60, 65, 70, 75, 80, 85].map((a) => ({ age: a, cross_sectional: +(cross[a] - cross[35]).toFixed(2),
    longitudinal_with_practice: +L[a].toFixed(2), longitudinal_practice_removed: +Lnp[a].toFixed(2), true_change: +Tr[a].toFixed(2) })) };
```
