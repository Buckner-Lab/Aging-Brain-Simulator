# Buckner et al., Figure 2C: World stage, episodic memory of 240 lives

Simulator: `AgingBrain_Simulator_261023.html` (version 99; default world: seed 7, 120,000 lives, study year 2026)
Run: `node run_panel_261110.mjs Buckner_etal_Figure2PanelC_261110.md`
The World page's episodic memory plot: its seeded sample of 240 lives (gray, red after dementia), the mean of everyone alive at each age with
the 10th–90th percentile band, and each sampled life's value at its age in 2026 (dots).

```js
const S = state.run.S, agg = state.run.agg, j = E.IX.mem, lives = state.sample, SY = state.run.p.studyYear;
const dots = lives.filter((t) => SY - t.b >= 40 && SY - t.b - E.AGE0 < t.n);            // alive in 2026, at 40 or older
return { lives_plotted: `${lives.length} of ${state.run.p.N}`, develop_dementia: lives.filter((t) => t.demAge < 999).length,
  dots_in_2026: `${dots.length} (${dots.filter((t) => SY - t.b >= t.demAge).length} with dementia)`,
  everyone_alive: [40, 50, 60, 70, 80, 85, 90, 100].map((a) => { const i = a - E.AGE0;
    return { age: a, alive: agg.alive[i], mean: +S.mean[j][i].toFixed(2), p10: +S.q[j].q10[i].toFixed(2), p90: +S.q[j].q90[i].toFixed(2) }; }) };
```
