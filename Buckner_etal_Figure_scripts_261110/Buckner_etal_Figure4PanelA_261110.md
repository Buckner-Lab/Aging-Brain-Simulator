# Buckner et al., Figure 4A: individual lives and the population mean for four phenotypes

Simulator: `AgingBrain_Simulator_261023.html` (version 99; default world: seed 7, 120,000 lives, study year 2026)
Run: `node run_panel_261110.mjs Buckner_etal_Figure4PanelA_261110.md`
The World page's sample of 240 of the 120,000 lives (its seeded draw) from 40 to death, for amyloid PET (positive at 20 CL), hippocampal
volume, episodic memory and semantic memory; the black line is the mean of everyone alive at each age. Lines turn red after dementia.

```js
const S = state.run.S, keys = ['amy', 'hip', 'mem', 'sem'], lives = state.sample;        // the app's 240 sampled lives (E.trace of each)
const at = (t, k, a) => (a - E.AGE0 < t.n ? t.tr[E.IX[k] * t.n + (a - E.AGE0)] : NaN);
return { lives_plotted: `${lives.length} of ${state.run.p.N}`, develop_dementia: lives.filter((t) => t.demAge < 999).length,
  first_life_ids: lives.slice(0, 10).map((t) => t.i + 1).join(', '),
  mean_of_everyone_alive: [40, 50, 60, 70, 80, 90, 100].map((a) => Object.fromEntries([['age', a], ...keys.map((k) => [k, +S.mean[E.IX[k]][a - E.AGE0].toFixed(2)])])),
  sample_at_80_mean: Object.fromEntries(keys.map((k) => { const v = lives.map((t) => at(t, k, 80)).filter(Number.isFinite); return [k, +(v.reduce((s, x) => s + x, 0) / v.length).toFixed(2)]; })) };
```
