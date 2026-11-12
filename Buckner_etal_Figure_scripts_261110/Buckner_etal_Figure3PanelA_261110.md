# Buckner et al., Figure 3A: five example women at 85, plotted as change from 40

Simulator: `AgingBrain_Simulator_261023.html` (version 99; default world: seed 7, 120,000 lives, study year 2026)
Run: `node run_panel_261110.mjs Buckner_etal_Figure3PanelA_261110.md`
The five women of Figure 3A–B (the median woman is at the median of memory among the 31,702 women who reach 85). For each: the ages of amyloid
and tau positivity, MCI (first CDR-SB ≥ 0.5 before dementia), dementia, a terminal phase and death, and each phenotype's change from 40 at 85.
Paper: the median woman has MCI from 84, is amyloid positive at 86, never tau positive, and dies at 89; the MCI woman converted at 82.

```js
const EX = { 'median woman': 83854, MCI: 9660, 'NW SuperAger': 49923, 'Josefsson maintainer': 106392, 'slope maintainer': 87872 };   // engine life index (the app shows index + 1)
const run = state.run, sd = dgPopSD(), keys = ['amy', 'tau', 'wmh', 'hip', 'mem', 'cdr'];   // SD of 85-year-olds: (10th-90th)/2.563, WMH on a log scale
const out = Object.entries(EX).map(([who, i]) => {
  const t = E.trace(i, run.p, run.k, run.S.refMean), at = (k, a) => t.tr[E.IX[k] * t.n + (a - E.AGE0)], L = (k, v) => (E.VARS[E.IX[k]].log ? Math.log(v) : v);
  let mci = 999; for (let a = 40; a < Math.min(t.demAge, 18 + t.n); a++) if (at('cdr', a) >= 0.5) { mci = a; break; }
  const ev = (a) => (a >= 999 ? 'never' : Math.floor(a));
  return Object.assign({ woman: who, life: i + 1, born: t.b, amyloid_pos: ev(t.aPos), tau_pos: ev(t.tPos), MCI: mci < t.demAge ? ev(mci) : 'never', dementia: ev(t.demAge),
    terminal: ev(t.termAt), death: +t.death.toFixed(1) }, Object.fromEntries(keys.map((k) => [k + '_at_85', +(DROW[k].up * (L(k, at(k, 85)) - L(k, at(k, 40))) / sd[k]).toFixed(2)])));
});
return { example_women: out, note: 'phenotype columns: change from 40 at 85 in SD of 85-year-olds, worse positive' };
```
