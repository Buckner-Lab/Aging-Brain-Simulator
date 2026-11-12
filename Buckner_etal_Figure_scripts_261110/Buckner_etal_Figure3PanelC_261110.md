# Buckner et al., Figure 3C: level at 40 against change from 75 to 85, by selection rule

Simulator: `AgingBrain_Simulator_261023.html` (version 99; default world: seed 7, 120,000 lives, study year 2026)
Run: `node run_panel_261110.mjs Buckner_etal_Figure3PanelC_261110.md`
Each woman's true memory at 40 against her true change from 75 to 85; high = above the median at 40 of the dementia-free women, stable = a loss
of no more than 0.3 SD. Corner shares are of each group's own members (first row: all women free of dementia at 85).
Paper: 31,702 women, 27,059 dementia-free; MCI 6,894, NW 6,294, Josefsson 4,445 (cut +0.48), slope 5,730; median at 40 +0.68.

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
const med40 = (() => { const s = free.map((o) => o.m40).sort((a, b) => a - b), h = s.length >> 1; return s.length % 2 ? s[h] : (s[h - 1] + s[h]) / 2; })();
const corner = (rows) => { const n = rows.length, c = (hi, st) => (100 * rows.filter((o) => (o.m40 > med40) === hi && (o.m85 - o.m75 >= -0.3) === st).length / n);
  return { n, 'top left (low, stable)': +c(false, true).toFixed(1), 'top right (high, stable)': +c(true, true).toFixed(1), 'bottom left (low, decline)': +c(false, false).toFixed(1), 'bottom right (high, decline)': +c(true, false).toFixed(1) }; };
return { women_at_85: W.length, dementia_free: free.length, median_memory_at_40: +med40.toFixed(2), josefsson_cut: +cut.jos.toFixed(2),
  corner_shares_percent: [Object.assign({ group: 'all dementia-free' }, corner(free)), ...Object.entries(RULES).map(([g, f]) => Object.assign({ group: g }, corner(W.filter(f))))] };
```
