# Buckner et al., Figure 4D: what makes episodic memory differ between people, by age

Simulator: `AgingBrain_Simulator_261023.html` (version 99; default world: seed 7, 120,000 lives, study year 2026)
Run: `node run_panel_261110.mjs Buckner_etal_Figure4PanelD_261110.md`
The engine's breakdown of between-person differences in episodic memory (each part's covariance with memory over memory's variance) among
the living every 5 years, from a 30,000-life sample; negative shares set to zero and the rest rescaled (as the Figure 3B pies, for everyone alive).

```js
const M = E.memoryShares(state.run.p, state.run.k, WP_LIVES, WP_AGES), lab = { start: 'level at 40', aging: 'aging', eng: 'engagement',
  cv: 'cardiovascular', sleep: 'sleep', ad: 'AD cascade', late: 'LATE', term: 'terminal decline' };
return { lives: M.lives, share_percent: M.all.filter((x) => x.n >= WP_MINN).map((x) => {
  const pos = x.raw.map((v) => Math.max(0, v)), s = pos.reduce((a, b) => a + b, 0);
  return Object.fromEntries([['age', x.age], ['n', x.n], ...M.parts.map((p, i) => [lab[p] || p, +(100 * pos[i] / s).toFixed(1)])]); }) };
```
