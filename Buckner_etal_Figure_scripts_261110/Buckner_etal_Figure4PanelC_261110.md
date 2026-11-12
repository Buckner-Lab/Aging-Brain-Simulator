# Buckner et al., Figure 4C: survival, amyloid positivity and dementia by age

Simulator: `AgingBrain_Simulator_261023.html` (version 99; default world: seed 7, 120,000 lives, study year 2026)
Run: `node run_panel_261110.mjs Buckner_etal_Figure4PanelC_261110.md`
Pooling every year of every life: survival from 40, amyloid positivity (≥ 20 CL) among the living, amyloid-positive and unimpaired (CDR-SB 0)
as a share of those without dementia, and dementia among the living (shown where at least 150 are alive). The published markers are
Roberts et al. (2018) and Manly et al. (2022); the checks that count only their people are Figure 4E.

```js
const agg = state.run.agg, N40 = agg.alive[E.ANCHOR - E.AGE0], pc = (x) => (Number.isFinite(x) ? +x.toFixed(1) : null), rows = [];
for (let a = 40; a <= 105; a += 5) {
  const ai = a - E.AGE0, n = agg.alive[ai], nc = agg.aliveCU[ai];
  let ap = 0; for (let d = 0; d < 3; d++) ap += agg.aPosD[d * E.NA + ai];
  rows.push({ age: a, surviving_from_40: pc(100 * n / N40), amyloid_positive: pc(n >= 150 ? 100 * ap / n : NaN),
    amyloid_pos_unimpaired_of_nondemented: pc(nc >= 150 ? 100 * agg.aPosCU[ai] / nc : NaN), dementia: pc(n >= 150 ? 100 * agg.dem[ai] / n : NaN) });
}
return { percent_by_age: rows };
```
