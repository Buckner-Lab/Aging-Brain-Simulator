# Buckner et al., Figure 7D: the course of dementia (MMSE) after onset at 80–89

Simulator: `AgingBrain_Simulator_261014.html` (version 88; default world: seed 7, 120,000 lives)
Run: `node run_panel_261110.mjs Buckner_etal_Figure7PanelD_261110.md`
For dementia that begins at 80–89, the mean change in MMSE since onset, chained from each year's mean change among those alive in both years,
with falling resilience or late-rising aging; the dashed reference is 1.5 points a year for Alzheimer dementia in the Cache County study.
Paper: with falling resilience, dementia beginning in the 80s progresses three to four times as fast as that reference; late-rising aging is closer.

```js
// the version-88 worlds: the original model (no late rise in aging, resilience constant) and one change to it in each variant
const d = E.DEFAULTS, ORIGINAL = { mem70: 0, spd70: 0, exe70: 0, resFallDbl: 0 };
const V = { 'original model': {}, 'more AD risk': { aPos70: 45 },
  'faster AD cascade': { lag: d.lag / 2, nLag: d.nLag / 2, cLag: d.cLag / 2, tauK: 2 * d.tauK },                  // every lag halved, tau's rise doubled
  'stronger LATE': { late85: 30, lateMem: 2 * d.lateMem, lateSpd: 2 * d.lateSpd, lateExe: 2 * d.lateExe },
  'late-rising aging': { mem70: d.mem70, spd70: d.spd70, exe70: d.exe70, cogDbl: d.cogDbl },                    // version 88's default
  'falling resilience': { resFallAge: 78, resFallDbl: 5 } };                                                      // default in versions 75-87
const world = (name) => { const p = Object.assign(simParams(), ORIGINAL, V[name]), k = E.prep(p), agg = E.newAgg(p); E.runChunk(agg, k, 0, p.N); return { p, k, agg, S: E.finish(agg) }; };
// every life traced in a world: phenotypes by age (t.tr), onsets of amyloid and tau positivity, LATE (lOn), lesions (wOn) and dementia
const each = (W, f) => { for (let i = 0; i < W.p.N; i++) f(E.trace(i, W.p, W.k, W.S.refMean)); };
const val = (t, k, a) => (a - E.AGE0 < t.n ? t.tr[E.IX[k] * t.n + (a - E.AGE0)] : NaN);
const out = [];
for (const name of ['falling resilience', 'late-rising aging']) {
  const W = world(name), ch = Array.from({ length: 11 }, () => [0, 0]);
  each(W, (t) => { if (t.demAge < 80 || t.demAge > 89) return;
    for (let y = 0; y < 11; y++) { const a = val(t, 'mmse', t.demAge + y), b = val(t, 'mmse', t.demAge + y + 1); if (!Number.isFinite(b)) break; ch[y][0] += b - a; ch[y][1]++; } });
  let c = 0; const row = { world: name, people_at_onset: ch[0][1] };
  ch.forEach(([s, n], y) => { if (n >= 30) { c += s / n; row[`year ${y + 1}`] = +c.toFixed(1); } });
  out.push(row);
}
return { mmse_change_since_onset_chained: out, reference: 'Cache County Alzheimer dementia: about -1.5 points a year (Tschanz et al., 2011)' };
```
