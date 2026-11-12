# Buckner et al., Figure 3D: the same rules applied to measured values

Simulator: `AgingBrain_Simulator_261023.html` (version 99; default world: seed 7, 120,000 lives, study year 2026)
Run: `node run_panel_261110.mjs Buckner_etal_Figure3PanelD_261110.md`
Memory at 40, 70, 75, 80 and 85 and executive function, semantic memory and CDR-SB at 85 measured once with the app's default errors (memory
and executive 0.40 SD, semantic 0.30, CDR-SB 0.5 points rounded to half points); cutoffs as in panel C; dementia status known.
Paper: measured groups 11,822, 6,337, 4,785, 8,206; incorrectly included 6,261, 1,072, 1,043, 4,558; missed 1,333, 1,029, 703, 2,082; Jaccard 42, 71, 68, 35%.

```js
// every woman who reaches 85 (whatever her birth year), true values from the engine
const run = state.run, IX = E.IX, z = new Float64Array(E.NZ), W = [], np = E.MPARTS.length;
for (let i = 0; i < run.p.N; i++) {
  const P = {}; E.setup(i, run.p, run.k, z, P); if (!P.female) continue;
  const o = { i }, T = { parts: new Float64Array(np), each: (a, y, c) => { if (a === 85) o.c = Array.from(c); } };   // memory's parts at 85
  E.live(P, run.p, run.k, (a, v, dem) => { if ([40, 70, 75, 80].includes(a)) o['m' + a] = v[IX.mem];
    if (a === 85) Object.assign(o, { m85: v[IX.mem], exe85: v[IX.exe], sem85: v[IX.sem], cdr85: v[IX.cdr], dem }); });
  if (o.m85 !== undefined) W.push(o);
}
// the four rules at 85, in true values; NW norms from 2026 (dementia-free 56-66 for memory, 85-89 for the other limits)
const w = run.agg.w26, mean = (a) => a.reduce((s, v) => s + v, 0) / a.length, psd = (a) => { const m = mean(a); return Math.sqrt(mean(a.map((v) => (v - m) ** 2))); };
const ages = (lo, hi, k) => { const x = []; for (let r = 0; r < w.n; r++) if (!w.dem[r] && w.age[r] >= lo && w.age[r] <= hi) x.push(wv(w, r, k)); return x; };
const e = ages(85, 89, 'exe'), s = ages(85, 89, 'sem'), cut = { mem: mean(ages(56, 66, 'mem')), exe: mean(e) - psd(e), sem: mean(s) - psd(s) };
const jos = (o) => { const y = [o.m70, o.m75, o.m80, o.m85], my = mean(y); return o.m70 + 15 * ((-7.5) * (y[0] - my) + (-2.5) * (y[1] - my) + 2.5 * (y[2] - my) + 7.5 * (y[3] - my)) / 125; };
const free = W.filter((o) => !o.dem), js = free.map(jos); cut.jos = mean(js) + psd(js);
const RULES = { MCI: (o) => !o.dem && o.cdr85 >= 0.5 && o.cdr85 <= 2.5, 'NW SuperAger': (o) => !o.dem && o.m85 >= cut.mem && o.exe85 >= cut.exe && o.sem85 >= cut.sem,
  'Josefsson maintainer': (o) => !o.dem && jos(o) >= cut.jos, 'slope maintainer': (o) => !o.dem && o.m85 - o.m75 >= -0.3 };
// one measurement of each value, as the app measures at its defaults; each error fixed by person, measure and occasion (months from 40)
const ms = (k, t, o, age) => msAt(k, t, o.i, 1, age, 0, 12 * (age - 40), 0);
const M = W.map((o) => ({ i: o.i, dem: o.dem, m40: ms('mem', o.m40, o, 40), m70: ms('mem', o.m70, o, 70), m75: ms('mem', o.m75, o, 75), m80: ms('mem', o.m80, o, 80),
  m85: ms('mem', o.m85, o, 85), exe85: ms('exe', o.exe85, o, 85), sem85: ms('sem', o.sem85, o, 85), cdr85: ms('cdr', o.cdr85, o, 85) }));
const med40 = (() => { const s = free.map((o) => o.m40).sort((a, b) => a - b), h = s.length >> 1; return s.length % 2 ? s[h] : (s[h - 1] + s[h]) / 2; })();
const corner = (rows) => { const n = rows.length, c = (hi, st) => +(100 * rows.filter((o) => (o.m40 > med40) === hi && (o.m85 - o.m75 >= -0.3) === st).length / n).toFixed(1);
  return [c(false, true), c(true, true), c(false, false), c(true, false)].join(' / '); };
const out = Object.entries(RULES).map(([g, f]) => {
  const T = new Set(W.filter(f).map((o) => o.i)), Mg = M.filter(f), both = Mg.filter((o) => T.has(o.i)).length;
  return { group: g, true: T.size, measured: Mg.length, incorrectly_included: Mg.length - both, missed: T.size - both,
    jaccard: (100 * both / (T.size + Mg.length - both)).toFixed(0) + '%', measured_corners_TL_TR_BL_BR: corner(Mg) };
});
return { cdr0_measured_05_or_more: (100 * M.filter((o, n) => !W[n].dem && W[n].cdr85 === 0 && o.cdr85 >= 0.5).length / free.filter((o) => o.cdr85 === 0).length).toFixed(0) + '%',
  all_dementia_free_corners: corner(M.filter((o) => !o.dem)), selection_on_measured_values: out };
```
