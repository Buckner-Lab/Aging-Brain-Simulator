# Buckner et al., Figure 2H: Intervention stage, a trial that slows the AD cascade by half

Simulator: `AgingBrain_Simulator_261023.html` (version 99; default world: seed 7, 120,000 lives, study year 2026)
Run: `node run_panel_261110.mjs Buckner_etal_Figure2PanelH_261110.md`
Panel D's 400 participants randomized at entry in 2026 (half treated: amyloid and tau build up 50% slower), seen yearly for 10 years; each
participant's change per year in true episodic memory (no error, no practice). Dashed: the treated participants' own lives without the
intervention. Read from the application's own Intervention tables. Figure: Treated 200, Controls 200; n = 195 and 197 seen twice or more.

```js
Object.assign(state.sel, { strat: 'nondem', seed: 1 });
Object.assign(state.sel.q.nondem, { lo: 60, hi: 90, n: 400, women: 55, by: 'mmse', mmse: 24 });
Object.assign(state.iv, { kind: 'ad', x: 50, share: 50, seed: 1, y: 'mem', yrs: 10, step: 12, view: 'chg', meas: false, prac: false, cf: true });
showPanel('interv'); renderInterv();
const txt = (s) => document.querySelector(s).textContent.replace(/\s+/g, ' ').trim();
const lg = (s) => [...document.querySelector(s).children].map((c) => c.textContent.trim()).filter(Boolean).join(' · ');
const tables = (s) => [...document.querySelectorAll(s + ' table')].map((t) => { let last = '';   // a repeated header (95% CI, p) is named for its column
  const h = [...t.querySelectorAll('thead th')].map((x) => x.textContent.trim()).map((x, i, a) => { if (a.indexOf(x) < i) return `${x}, ${last}`; if (x && !/^(95% CI|p|SD|n)$/.test(x)) last = x.toLowerCase(); return x || 'row'; });
  return [...t.querySelectorAll('tbody tr')].map((tr) => Object.fromEntries([...tr.children].map((td, i) => [h[i], td.textContent.trim()]))); });
const [arms, effect] = tables('#iv-table');
return { legend: lg('#iv-lg'), bars: [...document.querySelectorAll('#iv-plot text.an-cn')].map((t) => `${t.previousElementSibling.textContent} ${t.textContent}`).join(', '),
  each_arm: arms, effect_treated_minus_controls: effect, app_says: txt('#iv-say') };
```
