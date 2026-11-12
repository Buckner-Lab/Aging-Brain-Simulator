# Buckner et al., Figure 7A: new dementia per year by age in six version-88 worlds

Simulator: `AgingBrain_Simulator_261014.html` (version 88; default world: seed 7, 120,000 lives)
Run: `node run_panel_261110.mjs Buckner_etal_Figure7PanelA_261110.md`
Each world simulates all 120,000 lives with one setting of the original model changed; new dementia per year is the share of those without
dementia at one age who have it at the next, pooled over every year of every life, by 5-year age group.
Paper: amyloid+ at 70 rises from 32% to 49% with more AD risk; published rates (Corrada et al., 2010) at 90–94 (11.9%, range 9–17%), 95–99 and 100+.

```js
// the version-88 worlds: the original model (no late rise in aging, resilience constant) and one change to it in each variant
const d = E.DEFAULTS, ORIGINAL = { mem70: 0, spd70: 0, exe70: 0, resFallDbl: 0 };
const V = { 'original model': {}, 'more AD risk': { aPos70: 45 },
  'faster AD cascade': { lag: d.lag / 2, nLag: d.nLag / 2, cLag: d.cLag / 2, tauK: 2 * d.tauK },                  // every lag halved, tau's rise doubled
  'stronger LATE': { late85: 30, lateMem: 2 * d.lateMem, lateSpd: 2 * d.lateSpd, lateExe: 2 * d.lateExe },
  'late-rising aging': { mem70: d.mem70, spd70: d.spd70, exe70: d.exe70, cogDbl: d.cogDbl },                    // version 88's default
  'falling resilience': { resFallAge: 78, resFallDbl: 5 } };                                                      // default in versions 75-87
const world = (name) => { const p = Object.assign(simParams(), ORIGINAL, V[name]), k = E.prep(p), agg = E.newAgg(p); E.runChunk(agg, k, 0, p.N); return { p, k, agg, S: E.finish(agg) }; };
const rows = [], G = [[65, 69], [70, 74], [75, 79], [80, 84], [85, 89], [90, 94], [95, 99], [100, 110]];
for (const name of Object.keys(V)) {
  const { agg } = world(name), inc = ([a, b]) => { let n = 0, r = 0; for (let x = a; x <= b; x++) { n += agg.demNew[x - E.AGE0]; r += agg.demRisk[x - E.AGE0]; } return +(100 * n / r).toFixed(1); };
  let ap = 0; const i70 = 70 - E.AGE0; if (agg.aPosD) for (let s = 0; s < 3; s++) ap += agg.aPosD[s * E.NA + i70];
  rows.push(Object.assign({ world: name, 'amyloid+ at 70 (realized)': agg.aPosD ? +(100 * ap / agg.alive[i70]).toFixed(0) + '%' : '' },
    Object.fromEntries(G.map((g) => [g[1] > 100 ? '100+' : `${g[0]}-${g[1]}`, inc(g)]))));
}
return { new_dementia_percent_per_year: rows };
```
