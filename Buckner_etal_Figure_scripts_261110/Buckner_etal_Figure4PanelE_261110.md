# Buckner et al., Figure 4E: the thirteen reality checks, scaled to their accepted ranges

Simulator: `AgingBrain_Simulator_261023.html` (version 99; default world: seed 7, 120,000 lives, study year 2026)
Run: `node run_panel_261110.mjs Buckner_etal_Figure4PanelE_261110.md`
Runs the application's own reality checks (World page, Reality checks) and scales each value to its accepted range (0, low end; 1, high end).
Paper: 12 of 13 within range (Table 1 lists the values).

```js
wpChecks();                                                    // the app computes and renders the table
const num = (s) => parseFloat(s.replace(/−/g, '-'));
const rows = [...document.querySelectorAll('#wp-checks-body tbody tr')].map((tr) => {
  const td = tr.querySelectorAll('td'), v = num(td[1].textContent), m = td[3].textContent.replace(/−/g, '-').match(/(-?[\d.]+)\s*(?:–|to)\s*(-?[\d.]+)/);
  return { check: td[0].childNodes[0].textContent.trim(), model: td[1].textContent, range: td[3].textContent,
    scaled: +((v - +m[1]) / (+m[2] - +m[1])).toFixed(2), status: td[5].textContent.replace(/[✓–▲▼!]/g, '').trim() };
});
return { summary: document.querySelector('#wp-checks-say').textContent, checks: rows };
```
