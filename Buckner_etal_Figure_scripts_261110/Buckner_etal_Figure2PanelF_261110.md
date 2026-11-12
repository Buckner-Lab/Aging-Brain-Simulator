# Buckner et al., Figure 2F: Analysis stage, memory in two age groups by biomarker status

Simulator: `AgingBrain_Simulator_261023.html` (version 99; default world: seed 7, 120,000 lives, study year 2026)
Run: `node run_panel_261110.mjs Buckner_etal_Figure2PanelF_261110.md`
The second sample: panel D's study drawn again (the app's draw 282, chosen for its clear biomarker difference at 80–89), groups 60–69 and
80–89. Measured episodic memory adjusted for sex and head size; biomarker+ means measured amyloid PET ≥ 20 CL or tau PET ≥ 1.30 SUVR.
Bars are means with 95% CIs, dashed lines the means in everyone alive at those ages. Read from the application's own Analysis tables.
Figure: Biomarker− 166, Biomarker+ 85; n = 177 (60–69) and 74 (80–89).

```js
Object.assign(state.sel, { strat: 'nondem', seed: 282 });
Object.assign(state.sel.q.nondem, { lo: 60, hi: 90, n: 400, women: 55, by: 'mmse', mmse: 24 });
Object.assign(state.an, { mode: 'split', y: 'mem', meas: true, color: 'bio', sep: false, fit: true, truth: true, adjSex: true, adjTiv: true, adjE4: false, gA: [60, 69], gB: [80, 89] });
showPanel('analysis'); renderAnalysis();
const txt = (s) => document.querySelector(s).textContent.replace(/\s+/g, ' ').trim();
const lg = (s) => [...document.querySelector(s).children].map((c) => c.textContent.trim()).filter(Boolean).join(' · ');
const tables = (s) => [...document.querySelectorAll(s + ' table')].map((t) => { let last = '';   // a repeated header (95% CI, p) is named for its column
  const h = [...t.querySelectorAll('thead th')].map((x) => x.textContent.trim()).map((x, i, a) => { if (a.indexOf(x) < i) return `${x}, ${last}`; if (x && !/^(95% CI|p|SD|n)$/.test(x)) last = x.toLowerCase(); return x || 'row'; });
  return [...t.querySelectorAll('tbody tr')].map((tr) => Object.fromEntries([...tr.children].map((td, i) => [h[i], td.textContent.trim()]))); });
const [means, diff] = tables('#an-table');
return { legend: lg('#an-lg'), groups: [...document.querySelectorAll('#an-plot text.an-cn')].map((t) => `${t.previousElementSibling.textContent} ${t.textContent}`).join(', '),
  group_means_adjusted: means, difference_80_89_minus_60_69: diff, app_says: txt('#an-say') };
```
