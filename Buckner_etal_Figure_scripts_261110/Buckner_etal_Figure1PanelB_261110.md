# Buckner et al., Figure 1B: the simulator's loop

Simulator: `AgingBrain_Simulator_261023.html` (version 99; default world: seed 7, 120,000 lives, study year 2026)
Run: `node run_panel_261110.mjs Buckner_etal_Figure1PanelB_261110.md`
A diagram; its lives are illustrative. The script checks the facts it depicts: the dementia rule behind the red lines (and the MMSE when
dementia begins, about 24), the reality checks in the compare box (12 of 13 in range, as in Figure 4E) and the versions in the file (v1 to v99).

```js
const { p, k, S } = state.run, j = E.IX.mmse, at = [];
for (let i = 0; i < 20000; i++) { const t = E.trace(i, p, k, S.refMean); if (t.demAge < 999) at.push(t.tr[j * t.n + (t.demAge - E.AGE0)]); }
at.sort((a, b) => a - b); wpChecks();
return { dementia_rule: `global cognition at or below ${p.demThresh} SD after a fall of at least ${p.demDecline} SD from its level at 40`,
  mmse_when_dementia_begins: `median ${at[at.length >> 1].toFixed(1)}, middle half ${at[at.length >> 2].toFixed(1)}–${at[(3 * at.length) >> 2].toFixed(1)} (${at.length} onsets in lives 1–20,000)`,
  reality_checks: document.querySelector('#wp-checks-say').textContent,
  versions_in_file: [...document.querySelectorAll('#wp-versions li.vh .vh-v')].map((x) => x.textContent).reverse().filter((v, i, a) => i === 0 || i === a.length - 1).join(' to ') };
```
