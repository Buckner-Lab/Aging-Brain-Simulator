# Buckner et al., Figure 2G: Follow-up stage, six years of measured memory from 81–90

Simulator: `AgingBrain_Simulator_261023.html` (version 99; default world: seed 7, 120,000 lives, study year 2026)
Run: `node run_panel_261110.mjs Buckner_etal_Figure2PanelG_261110.md`
Panel D's participants aged 81–90 at entry in 2026, seen every 2 years for 6 years, episodic memory measured with error and practice effects,
by age. Black: mean course by 5-year age at entry (81–85, 86–90; visits with 5 or more seen); dashed: the same for everyone alive at 81–90 in
2026, at true values. The application's Follow-up code (anLong) run on the 81–90 part of the sample. Figure: Biomarker− 18, Biomarker+ 47.

```js
Object.assign(state.sel, { strat: 'nondem', seed: 1 });
Object.assign(state.sel.q.nondem, { lo: 60, hi: 90, n: 400, women: 55, by: 'mmse', mmse: 24 });
Object.assign(state.an, { ly: 'mem', yrs: 6, step: 24, lmeas: true, lprac: true, lview: 'traj', ltime: 'age', lmean: true, ltruth: true, color: 'bio', sep: false });
const R0 = runSelection(), w = state.run.agg.w26, in8190 = (r) => w.age[r] >= 81 && w.age[r] <= 90;
const R = Object.assign({}, R0, { lo: 81, hi: 90, sel: R0.sel.filter(in8190), world: R0.world.filter(in8190) });
showPanel('follow'); ANP = 'fu'; anLong(R);
const ys = anVisits(state.an), j = E.IX.mem, recs = anRecs(w, R.sel, ys, j, true, fuOf, true, mxOn('fu')), T = anRecs(w, anTruthRows(R), ys, j);
const course = (who, list) => anCourses(w, list, ys, true, R).flatMap((c, b) => c.map(([age, m, n]) => ({ who, entry: ['81–85', '86–90'][b], age: +age.toFixed(1), mean: +m.toFixed(2), n })));
const txt = (s) => document.querySelector(s).textContent.replace(/\s+/g, ' ').trim();
const lg = (s) => [...document.querySelector(s).children].map((c) => c.textContent.trim()).filter(Boolean).join(' · ');
const tables = (s) => [...document.querySelectorAll(s + ' table')].map((t) => { let last = '';   // a repeated header (95% CI, p) is named for its column
  const h = [...t.querySelectorAll('thead th')].map((x) => x.textContent.trim()).map((x, i, a) => { if (a.indexOf(x) < i) return `${x}, ${last}`; if (x && !/^(95% CI|p|SD|n)$/.test(x)) last = x.toLowerCase(); return x || 'row'; });
  return [...t.querySelectorAll('tbody tr')].map((tr) => Object.fromEntries([...tr.children].map((td, i) => [h[i], td.textContent.trim()]))); });
return { participants: R.sel.length, legend: lg('#fu-lg'), mean_courses: course('sample', recs).concat(course('everyone 81–90', T)),
  change_per_year: tables('#fu-table')[0], app_says: txt('#fu-say') };
```
