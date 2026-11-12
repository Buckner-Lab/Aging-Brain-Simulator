# Buckner et al., Figure 5C: one measurement misclassifies SuperAgers, and a retest regresses to the mean

Simulator: `AgingBrain_Simulator_261023.html` (version 99; default world: seed 7, 120,000 lives, study year 2026)
Run: `node run_panel_261110.mjs Buckner_etal_Figure5PanelC_261110.md`
Dementia-free people aged 80–89 in 2026. Northwestern rule with 2026 norms from true values, applied to true values and to one measurement
of each test (Visit 1); Visit 2 measures all three again in the same year with new errors and no practice gain.
Paper: 4,587 people; 713 true SuperAgers; 712 labeled at Visit 1, 81% true, 72% labeled again; memory above threshold 0.70 → 0.52 (true 0.53).

```js
const w = state.run.agg.w26, mean = (a) => a.reduce((s, v) => s + v, 0) / a.length;
const free = (a, b) => { const x = []; for (let r = 0; r < w.n; r++) if (!w.dem[r] && w.age[r] >= a && w.age[r] <= b) x.push(r); return x; };
const mu = (rows, k) => mean(rows.map((r) => wv(w, r, k))), sd = (rows, k) => { const u = mu(rows, k); return Math.sqrt(mean(rows.map((r) => (wv(w, r, k) - u) ** 2))); };
const norm = free(56, 66), memCut = mu(norm, 'mem'), lim = {};
for (const [a, b] of [[80, 84], [85, 89]]) { const g = free(a, b); lim[a] = { exe: mu(g, 'exe') - sd(g, 'exe'), sem: mu(g, 'sem') - sd(g, 'sem') }; }
const pop = free(80, 89), L = (r) => lim[w.age[r] >= 85 ? 85 : 80];
const nw = (r, v) => v('mem') >= memCut && v('exe') >= L(r).exe && v('sem') >= L(r).sem;          // the rule, on any set of values
const tru = (r) => (k) => wv(w, r, k), v1 = (r) => (k) => anObs(w, r, k);                         // true; Visit 1 (occasion 0)
const v2 = (r) => (k) => msAt(k, wv(w, r, k), w.id[r], w.fem[r], w.age[r], wv(w, r, 'cdr'), MS_RETEST, 0);   // new error, no practice
const T = pop.filter((r) => nw(r, tru(r))), L1 = pop.filter((r) => nw(r, v1(r))), L12 = L1.filter((r) => nw(r, v2(r)));
const inT = new Set(T), half = pop.filter((_, i) => i % 2 === 0);
const cat = (rows) => ({ correct: rows.filter((r) => inT.has(r) && nw(r, v1(r))).length, wrongly_labeled: rows.filter((r) => !inT.has(r) && nw(r, v1(r))).length,
  missed: rows.filter((r) => inT.has(r) && !nw(r, v1(r))).length });
return { people_80_89: pop.length, norm_people_56_66: norm.length, memory_threshold_SD: +memCut.toFixed(2), true_SuperAgers: T.length,
  labeled_visit1: L1.length, labeled_who_are_true: `${(100 * L1.filter((r) => inT.has(r)).length / L1.length).toFixed(0)}%`,
  labeled_again_visit2: `${(100 * L12.length / L1.length).toFixed(0)}%`,
  labeled_memory_above_threshold: { visit1: +mean(L1.map((r) => anObs(w, r, 'mem') - memCut)).toFixed(2),
    visit2: +mean(L1.map((r) => v2(r)('mem') - memCut)).toFixed(2), true: +mean(L1.map((r) => wv(w, r, 'mem') - memCut)).toFixed(2) },
  left_plot_every_second_person: half.length, left_plot_counts_all: cat(pop), left_plot_counts_plotted: cat(half) };
```
