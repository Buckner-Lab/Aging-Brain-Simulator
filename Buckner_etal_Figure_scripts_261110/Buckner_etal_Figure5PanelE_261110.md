# Buckner et al., Figure 5E: five published SuperAger definitions applied to the same simulated people

Simulator: `AgingBrain_Simulator_261023.html` (version 99; default world: seed 7, 120,000 lives, study year 2026)
Run: `node run_panel_261110.mjs Buckner_etal_Figure5PanelE_261110.md`
Dementia-free people aged 70–90 in 2026 with measured MMSE ≥ 24, tested as the app measures (retests with new errors and practice). Norms come
from the same lives in 2006 (dementia-free, 18+), each test measured once with default-size errors drawn here (seed 12345).
Paper: 14,405 of 14,822; H 6.4% (20% of those 80+), D 19.9%, S 15.7%, M 6.0%, B 27.8%; 5,598 classified by any (MAS: 8.4, 18.5, 19.4, 1.5, 6.5%; H 21% of 80+).
The norm errors here come from this script's own generator, not the paper's, so D, S, M and B can differ by a few tenths of a point.

```js
const w = state.run.agg.w26, run = state.run, IX = E.IX, mean = (a) => a.reduce((s, v) => s + v, 0) / a.length;
const sd = (a) => { const m = mean(a); return Math.sqrt(mean(a.map((v) => (v - m) ** 2))); }, median = (a) => { const s = [...a].sort((x, y) => x - y), h = s.length >> 1; return s.length % 2 ? s[h] : (s[h - 1] + s[h]) / 2; };
// 2006 norms: every life alive, 18+ and free of dementia in 2006, each test measured once (error SD as the app's defaults)
let s32 = 12345; const rnd = () => { s32 = (s32 + 0x6d2b79f5) | 0; let t = Math.imul(s32 ^ (s32 >>> 15), 1 | s32); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
const gauss = () => Math.sqrt(-2 * Math.log(1 - rnd())) * Math.cos(2 * Math.PI * rnd());
const N = [];
for (let i = 0; i < run.p.N; i++) {
  const t = E.trace(i, run.p, run.k, run.S.refMean), a = 2006 - t.b;
  if (a < 18 || !(t.death > a) || !(a < t.demAge)) continue;
  const v = (k) => t.tr[IX[k] * t.n + (a - E.AGE0)] + state.ms[k].err * gauss();
  N.push({ a, f: t.female, mem: v('mem'), exe: v('exe'), sem: v('sem'), spd: v('spd') });
}
const at = (lo, hi, f) => N.filter((x) => x.a >= lo && x.a <= hi && (f === undefined || !!x.f === !!f));
const cut = { H: mean(at(50, 65).map((x) => x.mem)), D: mean(at(30, 40).map((x) => x.mem)), S: [0, 1].map((f) => mean(at(18, 32, f).map((x) => x.mem))),
  M: [0, 1].map((f) => median(at(20, 29, f).map((x) => x.mem))), B: mean(at(20, 29).map((x) => x.spd)) - 1.25 * sd(at(20, 29).map((x) => x.spd)) };
const lim = (age, k) => { const g = age >= 80 ? at(80, 80) : at(5 * Math.floor(age / 5), 5 * Math.floor(age / 5) + 4); const x = g.map((y) => y[k]); return mean(x) - sd(x); };
// 2026 sample: dementia-free, 70-90, measured MMSE >= 24; definitions on measured values
const pop = []; for (let r = 0; r < w.n; r++) if (!w.dem[r] && w.age[r] >= 70 && w.age[r] <= 90) pop.push(r);
const S = pop.filter((r) => anObs(w, r, 'mmse') >= 24), o = (r, k) => anObs(w, r, k), ok = (r, k) => o(r, k) >= lim(w.age[r], k);
const M3 = new Map(['mem', 'mmse'].map((k) => [k, new Map(anRecs(w, S, [0, 2, 4], IX[k], true, fuOf, true).map((p) => [p.r, p.pts]))]));
const B2 = new Map(anRecs(w, S, [0, 2.5], IX.spd, true, fuOf, true).map((p) => [p.r, p.pts]));
const def = {
  H: (r) => w.age[r] >= 80 && o(r, 'mem') >= cut.H && ok(r, 'exe') && ok(r, 'sem'),
  D: (r) => o(r, 'mem') >= cut.D && ok(r, 'spd') && ok(r, 'exe'),
  S: (r) => o(r, 'mem') >= cut.S[w.fem[r]] && ok(r, 'exe'),
  M: (r) => { const m = M3.get('mem').get(r), s = M3.get('mmse').get(r); return m.length === 3 && m.every((p) => p[1] >= cut.M[w.fem[r]]) && s.every((p) => p[1] >= 29); },
  B: (r) => { const p = B2.get(r); return p.length === 2 && p[0][1] >= cut.B && p[0][1] - p[1][1] < 0.5; } };
const who = Object.fromEntries(Object.entries(def).map(([k, f]) => [k, new Set(S.filter(f))]));
const any = S.filter((r) => Object.values(who).some((s) => s.has(r))), combo = {};
for (const r of any) { const c = Object.keys(who).filter((k) => who[k].has(r)).join(''); combo[c] = (combo[c] || 0) + 1; }
const n80 = S.filter((r) => w.age[r] >= 80).length;
return { norm_people_2006: N.length, people_2026: `${S.length} of ${pop.length}`,
  shares: Object.keys(def).map((k) => ({ definition: k, qualify: who[k].size, share: `${(100 * who[k].size / S.length).toFixed(1)}%` })),
  H_among_80_plus: `${(100 * who.H.size / n80).toFixed(1)}%`, classified_by_any: any.length,
  overlap: Object.entries(combo).filter(([, n]) => n >= 45).sort((a, b) => b[1] - a[1]).map(([c, n]) => ({ combination: c, share_of_any: `${(100 * n / any.length).toFixed(1)}%` })) };
```
