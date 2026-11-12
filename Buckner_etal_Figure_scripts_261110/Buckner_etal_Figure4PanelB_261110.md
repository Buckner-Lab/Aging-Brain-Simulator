# Buckner et al., Figure 4B: two average lives, never demented and dementia at 80

Simulator: `AgingBrain_Simulator_261023.html` (version 99; default world: seed 7, 120,000 lives, study year 2026)
Run: `node run_panel_261110.mjs Buckner_etal_Figure4PanelB_261110.md`
The mean of each phenotype among lives that never develop dementia and those whose dementia begins at 80, as change from 40 in SD of
85-year-olds ((10th–90th percentile)/2.563; log scale for skewed measures), worse upward; ages shown while at least 30 lives remain.
Paper: 78,451 and 1,467 lives.

```js
const S = state.run.S, sd = dgPopSD(), NV = E.NV, i40 = 40 - E.AGE0, rows = [];
for (const [g, L] of S.lm.entries()) for (const a of [50, 60, 70, 75, 80, 85, 90, 95, 100]) {
  const ai = a - E.AGE0; if (L.n[ai] < LM_MINN) continue;
  rows.push(Object.fromEntries([['life', g ? 'dementia at ' + S.lmDem : 'never'], ['age', a], ['lives', L.n[ai]], ...LM_KEYS.map((k) => {
    const j = E.IX[k], T = E.VARS[j].log ? (v) => Math.log(Math.max(v, 1e-6)) : (v) => v;
    return [k, +(DROW[k].up * (T(L.mean[ai * NV + j]) - T(L.mean[i40 * NV + j])) / sd[k]).toFixed(2)]; })]));
}
return { never_dementia_lives: S.lm[0].lives, dementia_at_80_lives: S.lm[1].lives, change_from_40_SD_worse_up: rows };
```
