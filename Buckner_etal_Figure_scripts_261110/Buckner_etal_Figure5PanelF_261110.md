# Buckner et al., Figure 5F: generational change, three worlds with the same lives

Simulator: `AgingBrain_Simulator_261023.html` (version 99, with the generational settings of `AgingBrain_Simulator_v91_261018.html` carried in)
Run: `node run_panel_261110.mjs Buckner_etal_Figure5PanelF_261110.md` (about a minute)
The same 120,000 lives in three worlds: no gains (no cohort gain beyond schooling, no schooling effect); level gains (the default); level and slope
gains (gain beyond schooling 0.10 SD a decade; normal aging and the toll of AD, LATE and white matter lesions × 0.5 per decade of birth after 1935,
births clamped to 1930–1960). True memory at every age reached, as change from 35, for four birth cohorts, everyone alive in 2026 (cross-sectional),
and changes chained across the ages of 2026 (dashed).
Paper: no gains, cross-sectional −1.41 SD by 85 against about −2.0; level gains, cross-sectional −0.49 by 60 while cohorts lose 0.10–0.12;
level and slope gains, by 85 the 1931 cohort −2.37 and the 1961 cohort −0.62, chained −0.97 against −1.50 for the 1941 cohort.

The four edits below carry the v91 branch's generational change in rates into version 99's engine (applied by run_panel_261110.mjs before loading):

```patch
  k.hipAbilE = Math.sqrt(Math.max(0, 1 - p.hipAbil * p.hipAbil));
=>
  k.hipAbilE = Math.sqrt(Math.max(0, 1 - p.hipAbil * p.hipAbil));
  const gr = (v) => 1 - Math.max(-60, Math.min(90, +v || 0)) / 100;
  k.cohOn = p.cohortRate || p.cohAmy || p.cohRes ? 1 : 0;
  k.cohA = Math.min(p.cohFrom === undefined ? 1930 : +p.cohFrom, p.cohTo === undefined ? 1960 : +p.cohTo);
  k.cohB = Math.max(p.cohFrom === undefined ? 1930 : +p.cohFrom, p.cohTo === undefined ? 1960 : +p.cohTo);
  k.cohR = p.cohRef === undefined ? k.cohA : +p.cohRef;
  k.cohFg = gr(p.cohortRate); k.cohFa = gr(p.cohAmy); k.cohFr = gr(p.cohRes);
```

```patch
  P.mfac = Math.exp(-k.sM * P.M - 0.5 * k.sM * k.sM);         // normal-aging rate multiplier
=>
  P.mfac = Math.exp(-k.sM * P.M - 0.5 * k.sM * k.sM);         // normal-aging rate multiplier
  const dG = k.cohOn ? (Math.max(k.cohA, Math.min(k.cohB, P.b)) - k.cohR) / 10 : 0;
  P.gAge = dG ? Math.pow(k.cohFg, dG) : 1; P.gAmy = dG ? Math.pow(k.cohFa, dG) : 1; P.gTol = dG ? Math.pow(k.cohFr, dG) : 1;
  P.mfac *= P.gAge;
```

```patch
  P.bCog = P.bBrain * P.bRes;                                 // pathology → cognition
=>
  P.bCog = P.bBrain * P.bRes * P.gTol;                        // pathology → cognition
```

```patch
    const cvM = wmhMem * lsp * vm, cvS = wmhSpd * lsp * vm, cvE = wmhExe * lsp * vm, cvO = wmhMot * lsp * vm, adO = bC * tauMot * cT;
=>
    const vmL = vm * (P.gTol === undefined ? 1 : P.gTol), cvM = wmhMem * lsp * vmL, cvS = wmhSpd * lsp * vmL, cvE = wmhExe * lsp * vmL, cvO = wmhMot * lsp * vmL, adO = bC * tauMot * cT;
```

```js
const WORLDS = { 'no gains': { cohortCog: 0, eduCog: 0 }, 'level gains (default)': {},
  'level and slope gains': { cohortCog: 0.10, cohortRate: 50, cohRes: 50, cohRef: 1935, cohFrom: 1930, cohTo: 1960 } };
const make = (s) => { const p = Object.assign(simParams(), s), k = E.prep(p), agg = E.newAgg(p); E.runChunk(agg, k, 0, p.N); return { p, k, agg, S: E.finish(agg) }; };
const keep = state.run, SY = 2026, AGES = [40, 50, 60, 70, 80, 85], out = [], checks = {};
for (const [name, s] of Object.entries(WORLDS)) {
  const W = make(s), B0 = W.p.birthMin, NB = W.p.birthMax - B0 + 1, A = 112, I = (b, a) => (b - B0) * A + a;
  state.run = W; wpChecks(); checks[name] = document.querySelector('#wp-checks-say').textContent; state.run = keep;
  const sM = new Float64Array(NB * A), nM = new Float64Array(NB * A), sD = new Float64Array(NB * A), nD = new Float64Array(NB * A);
  for (let i = 0; i < W.p.N; i++) {                                   // every life's true memory at every age it reaches
    const t = E.trace(i, W.p, W.k, W.S.refMean), j = E.IX.mem * t.n;
    for (let y = 1; y < t.n; y++) { const a = E.AGE0 + y, v = t.tr[j + y]; sM[I(t.b, a)] += v; nM[I(t.b, a)]++; sD[I(t.b, a)] += v - t.tr[j + y - 1]; nD[I(t.b, a)]++; }
  }
  const pool = (arr, n, bs, a) => { let x = 0, m = 0; for (const b of bs) if (b >= B0 && b < B0 + NB) { x += arr[I(b, a)]; m += n[I(b, a)]; } return m ? x / m : NaN; };
  const near = (B, h) => Array.from({ length: 2 * h + 1 }, (_, q) => B - h + q);
  const cohort = (B) => { let c = 0; const r = { 35: 0 }; for (let a = 36; a <= 85; a++) { c += pool(sD, nD, near(B, 2), a); r[a] = c; } return r; };
  const csAt = (a) => { let x = 0, m = 0; for (const b of near(SY - a, 1)) { const ag = SY - b; if (b >= B0 && b < B0 + NB) { x += sM[I(b, ag)]; m += nM[I(b, ag)]; } } return x / m; };
  let d = 0; const dash = { 35: 0 }; for (let a = 35; a < 85; a++) { d += pool(sD, nD, near(SY - a, 2), a + 1); dash[a + 1] = d; }
  const C = Object.fromEntries([1931, 1941, 1951, 1961].map((B) => [B, cohort(B)]));
  for (const a of AGES) out.push({ world: name, age: a, cross_sectional_2026: +(csAt(a) - csAt(35)).toFixed(2), chained_2026: +dash[a].toFixed(2),
    born_1931: +C[1931][a].toFixed(2), born_1941: +C[1941][a].toFixed(2), born_1951: +C[1951][a].toFixed(2), born_1961: +C[1961][a].toFixed(2) });
}
return { change_from_35_SD: out, reality_checks: checks };
```
