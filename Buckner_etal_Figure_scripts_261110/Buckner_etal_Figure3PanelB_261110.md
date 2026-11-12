# Buckner et al., Figure 3B: memory split into its level at 40 and each causal chain; the pies

Simulator: `AgingBrain_Simulator_261023.html` (version 99; default world: seed 7, 120,000 lives, study year 2026)
Run: `node run_panel_261110.mjs Buckner_etal_Figure3PanelB_261110.md`
Each woman's episodic memory is split by the engine into the level set at 40 and each chain's contribution (they add up exactly). Each group's pie
divides its mean difference from the dementia-free women in each part by its mean difference in memory at 85 (negative shares set to zero, rest
rescaled); the median woman's pie gives each part's covariance with memory over memory's variance among all women at 85.
Paper: groups are 21.7, 19.9, 14.0 and 18.1% of women at 85, level at 40 −0.78, +0.97, +1.13 and −0.07 SD; the slope pie's level share was −11%.

```js
const EX = { 'median woman': 83854, MCI: 9660, 'NW SuperAger': 49923, 'Josefsson maintainer': 106392, 'slope maintainer': 87872 };   // engine life index (the app shows index + 1)
// every woman who reaches 85 (whatever her birth year), true values from the engine
const run = state.run, IX = E.IX, z = new Float64Array(E.NZ), W = [], np = E.MPARTS.length;
for (let i = 0; i < run.p.N; i++) {
  const P = {}; E.setup(i, run.p, run.k, z, P); if (!P.female) continue;
  const o = { i }, T = { parts: new Float64Array(np), each: (a, y, c) => { if (a === 85) o.c = Array.from(c); } };   // memory's parts at 85
  E.live(P, run.p, run.k, (a, v, dem) => { if ([40, 70, 75, 80].includes(a)) o['m' + a] = v[IX.mem];
    if (a === 85) Object.assign(o, { m85: v[IX.mem], exe85: v[IX.exe], sem85: v[IX.sem], cdr85: v[IX.cdr], dem }); }, T);
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
const lab = E.MPARTS.map((p) => ({ start: 'level at 40', aging: 'aging', eng: 'engagement', cv: 'cardiovascular', sleep: 'sleep', ad: 'AD cascade', late: 'LATE', term: 'terminal decline' })[p]);
const mc = (rows, q) => mean(rows.map((o) => o.c[q])), my = (rows) => mean(rows.map((o) => o.m85));
const clip = (raw) => { const pos = raw.map((v) => Math.max(0, v)), s = pos.reduce((a, b) => a + b, 0); return pos.map((v) => +(100 * v / s).toFixed(1)); };
const pies = Object.entries(RULES).map(([g, f]) => {                                          // group mean difference from dementia-free women, by part
  const G = W.filter(f), raw = lab.map((_, q) => (mc(G, q) - mc(free, q)) / (my(G) - my(free)));
  return Object.assign({ group: g, share_of_women_at_85: (100 * G.length / W.length).toFixed(1) + '%', level_at_40_vs_free: +(mc(G, 0) - mc(free, 0)).toFixed(2),
    raw_level_share: (100 * raw[0]).toFixed(0) + '%' }, Object.fromEntries(clip(raw).map((v, q) => [lab[q], v])));
});
const yW = my(W), vy = mean(W.map((o) => (o.m85 - yW) ** 2)), cov = lab.map((_, q) => { const cq = mc(W, q); return mean(W.map((o) => (o.c[q] - cq) * (o.m85 - yW))) / vy; });
const byId = new Map(W.map((o) => [o.i, o]));
return { women_at_85: W.length, median_woman_pie_all_women: Object.fromEntries(clip(cov).map((v, q) => [lab[q], v])), group_pies_percent: pies,
  example_women_memory_at_85: Object.entries(EX).map(([who, i]) => Object.assign({ woman: who, memory: +byId.get(i).m85.toFixed(2) }, Object.fromEntries(lab.map((l, q) => [l, +byId.get(i).c[q].toFixed(2)])))) };
```
