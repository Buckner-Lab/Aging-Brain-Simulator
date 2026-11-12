# Buckner et al., Figure 2B: what each causal chain does to each phenotype at 85

Simulator: `AgingBrain_Simulator_261023.html` (version 99; default world: seed 7, 120,000 lives, study year 2026)
Run: `node run_panel_261110.mjs Buckner_etal_Figure2PanelB_261110.md`
The dots on the right: the application's causal diagrams (How the model works) run its reference person, as a woman and as a man, with each
chain on and off (cardiovascular, AD and LATE onsets at 55, 65 and 80 against none; a terminal phase from 82 against none), and give the
difference at 85 in SD of 85-year-olds (10th–90th percentile range / 2.563), worse positive, averaged over the two. Dot area follows the value;
links below 0.02 SD are drawn as open circles. The baseline boxes and arrows on the left are a diagram.

```js
const CH = { aging: 'Aging', cv: 'Cardiovascular', ad: 'AD cascade', sleep: 'Sleep', engage: 'Engagement', late: 'LATE', term: 'Terminal decline' };
const rows = DROW_ORDER.map((k) => Object.assign({ phenotype: DROW[k].label }, Object.fromEntries(Object.values(CH).map((n) => [n, null])))), open = [];
for (const [id, name] of Object.entries(CH)) for (const r of dgCompute(id).rows) {
  rows[DROW_ORDER.indexOf(r.key)][name] = +r.h85.toFixed(2);
  if (Math.abs(r.h85) < 0.02) open.push(`${name} → ${DROW[r.key].label}`);
}
return { effect_at_85_SD: rows, open_circles: open.join('; '), each_chain_compares: Object.entries(CH).map(([id, n]) => `${n}: ${DGM[id].say}`).join('; ') };
```
