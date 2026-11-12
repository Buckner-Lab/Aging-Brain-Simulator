# Buckner et al., Figure 2D: Selection stage, who seeks to enroll, meets the criterion and is selected

Simulator: `AgingBrain_Simulator_261023.html` (version 99; default world: seed 7, 120,000 lives, study year 2026)
Run: `node run_panel_261110.mjs Buckner_etal_Figure2PanelD_261110.md`
The example study of panels C–H: the Nondemented strategy (MMSE ≥ 24, true values), ages 60–90 in 2026, 400 people (55% women), the app's
first draw; enrollment at its defaults (everyone alive may seek to enroll). The plot shows MMSE against age for each group (gray and light amber
thinned evenly for drawing, as the app does).

```js
Object.assign(state.sel, { strat: 'nondem', seed: 1 });
Object.assign(state.sel.q.nondem, { lo: 60, hi: 90, n: 400, women: 55, by: 'mmse', mmse: 24 });
const R = runSelection(), w = state.run.agg.w26, fem = R.sel.filter((r) => w.fem[r]).length;
const inM = new Set(R.meet), inS = new Set(R.sel), thin = (a, k) => (a.length <= k ? a : a.filter((_, j) => (j * k) % a.length < k));
return { alive_60_90_in_2026: R.world.length, seek_to_enroll: R.elig.length, meet_the_criterion: R.meet.length,
  selected: `${R.sel.length} (${fem} women, ${R.sel.length - fem} men)`,
  points_drawn: `seek only ${thin(R.elig.filter((r) => !inM.has(r)), 2200).length}, meet only ${thin(R.meet.filter((r) => !inS.has(r)), 1600).length}, selected ${R.sel.length}` };
```
