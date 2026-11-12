# Buckner et al., Figure 7B: each version-88 world against its fourteen reality checks

Simulator: `AgingBrain_Simulator_261014.html` (version 88; default world: seed 7, 120,000 lives)
Run: `node run_panel_261110.mjs Buckner_etal_Figure7PanelB_261110.md`
Simulates each of the six worlds of panel A and runs the version-88 application's own reality checks on it (green, within range; red, above
or below).
Paper: late-rising aging passes all 14; falling resilience 13, missing the non-carriers' hippocampus–memory change r (0.17 against 0.16).

```js
// the version-88 worlds: the original model (no late rise in aging, resilience constant) and one change to it in each variant
const d = E.DEFAULTS, ORIGINAL = { mem70: 0, spd70: 0, exe70: 0, resFallDbl: 0 };
const V = { 'original model': {}, 'more AD risk': { aPos70: 45 },
  'faster AD cascade': { lag: d.lag / 2, nLag: d.nLag / 2, cLag: d.cLag / 2, tauK: 2 * d.tauK },                  // every lag halved, tau's rise doubled
  'stronger LATE': { late85: 30, lateMem: 2 * d.lateMem, lateSpd: 2 * d.lateSpd, lateExe: 2 * d.lateExe },
  'late-rising aging': { mem70: d.mem70, spd70: d.spd70, exe70: d.exe70, cogDbl: d.cogDbl },                    // version 88's default
  'falling resilience': { resFallAge: 78, resFallDbl: 5 } };                                                      // default in versions 75-87
const world = (name) => { const p = Object.assign(simParams(), ORIGINAL, V[name]), k = E.prep(p), agg = E.newAgg(p); E.runChunk(agg, k, 0, p.N); return { p, k, agg, S: E.finish(agg) }; };
const keep = state.run, out = [];
for (const name of Object.keys(V)) {
  state.run = world(name); wpChecks();                                   // the version-88 application's own checks on this world
  for (const tr of document.querySelectorAll('#wp-checks-body tbody tr')) { const td = tr.querySelectorAll('td');
    out.push({ world: name, check: td[0].childNodes[0].textContent.trim().slice(0, 60), model: td[1].textContent, range: td[3].textContent, status: td[5].textContent.replace(/[^A-Za-z ]/g, '').trim() }); }
}
state.run = keep;
const sum = Object.keys(V).map((n) => ({ world: n, in_range: out.filter((r) => r.world === n && /In range/.test(r.status)).length + ' of ' + out.filter((r) => r.world === n).length }));
return { summary: sum, checks: out };
```
