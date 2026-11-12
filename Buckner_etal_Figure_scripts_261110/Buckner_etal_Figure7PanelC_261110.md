# Buckner et al., Figure 7C: memory by age, free of pathology and in everyone, under the two hypotheses

Simulator: `AgingBrain_Simulator_261014.html` (version 88; default world: seed 7, 120,000 lives)
Run: `node run_panel_261110.mjs Buckner_etal_Figure7PanelC_261110.md`
Mean true episodic memory by age (every 5 years, pooled over every life) among people free of pathology (amyloid PET < 20 CL, tau PET < 1.30 SUVR,
before the onsets of LATE and white matter lesions, without dementia) and among everyone alive, with falling resilience or late-rising aging (and, for reference, neither repair).
Paper: pathology-free 90-year-olds average −0.86 SD with late-rising aging, −0.35 with falling resilience and −0.34 with neither.

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
for (const name of ['falling resilience', 'late-rising aging', 'original model']) {
  const W = world(name), s = {}, add = (key, a, v) => { const o = (s[key] = s[key] || {})[a] = s[key][a] || [0, 0]; o[0] += v; o[1]++; };
  each(W, (t) => { for (let a = 40; a <= 100; a += 5) { const m = val(t, 'mem', a); if (!Number.isFinite(m)) break; add('everyone', a, m);
    if (val(t, 'amy', a) < 20 && val(t, 'tau', a) < 1.3 && a < t.lOn && a < t.wOn && a < t.demAge) add('free of pathology', a, m); } });
  for (const key of ['free of pathology', 'everyone']) out.push(Object.assign({ world: name, group: key }, Object.fromEntries(Object.entries(s[key]).map(([a, [x, n]]) => ['age ' + a, +(x / n).toFixed(2)]))));
}
return { mean_episodic_memory_by_age: out };
```
