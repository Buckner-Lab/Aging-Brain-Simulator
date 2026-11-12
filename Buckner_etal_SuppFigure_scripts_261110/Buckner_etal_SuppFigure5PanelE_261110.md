# Supplementary Figure 5, panel E: Export

```python
# Supplementary Figure 5E: Export writes the selected participants' values in the study year, true and as measured, and their
# values at each Follow-up visit (as set: every 2 years for 6 years), as CSV files with a data dictionary. Version 102 has no
# such stage; this script computes the stage's result with the app's own functions. Writes the three files next to this script.
# Run: python Buckner_etal_SuppFigure5PanelE_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
import sys, tempfile
from pathlib import Path
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from playwright.sync_api import sync_playwright
SIM = Path(sys.argv[1] if len(sys.argv) > 1 else 'AgingBrain_Simulator_v102_261109.html')
READY = "window.__abReady === true && !document.getElementById('status').classList.contains('busy')"
def run(*steps):   # the simulator, headless, with one added line that exposes its app; runs each step there, after any new world is ready
    tmp = Path(tempfile.gettempdir()) / 'ab_sim.html'
    tmp.write_text(SIM.read_text(encoding='utf8').replace('\ninit();\n})();', '\nwindow.__abEval = s => eval(s);\ninit();\n})();', 1), encoding='utf8')
    with sync_playwright() as pw:
        pg = pw.chromium.launch().new_page(); pg.route('http*://**', lambda r: r.abort()); pg.goto(tmp.as_uri())
        for s in steps: pg.wait_for_function(READY, timeout=600_000); out = pg.evaluate('s => __abEval(s)', s)
    return out

import csv
JS = r'''(() => { const w = state.run.agg.w26, R = runSelection(), ys = anVisits(state.an), keys = MS_KEYS;
  const now = R.sel.map((r) => ({ id: w.id[r] + 1, age: w.age[r], female: w.fem[r], ...Object.fromEntries(keys.flatMap((k) => { const t = wv(w, r, k);
    return [[k + '_true', t], [k + '_measured', msAt(k, t, w.id[r], w.fem[r], w.age[r], wv(w, r, 'cdr'), 0)]]; })) }));
  const visits = []; for (const k of keys) anRecs(w, R.sel, ys, E.IX[k], true, fuOf).forEach((p) => p.pts.forEach(([y, m, t]) => visits.push({ id: w.id[p.r] + 1, years: y, variable: k, true: t, measured: m })));
  return { now, visits, dict: keys.map((k) => [k, LD_NAME[k], LD_UNIT[k] || 'points']) }; })()'''
c = run(JS)
for name, rows in (('Buckner_etal_SuppFigure5PanelE_study_year_261110.csv', c['now']), ('Buckner_etal_SuppFigure5PanelE_visits_261110.csv', c['visits'])):
    with open(name, 'w', newline='') as f: wr = csv.DictWriter(f, fieldnames=list(rows[0])); wr.writeheader(); wr.writerows(rows)
    print(f'{name}: {len(rows)} rows, {len(rows[0])} columns')
with open('Buckner_etal_SuppFigure5PanelE_dictionary_261110.csv', 'w', newline='') as f:
    wr = csv.writer(f); wr.writerow(['column', 'meaning', 'unit']); wr.writerows([['id', 'life number (1-based)', ''], ['age', 'age in 2026', 'years'], ['female', '1 for women', ''],
        ['years', 'years from entry (visits file)', 'years'], ['variable', 'phenotype key (visits file)', '']] + [[k + '_true / _measured', n, u] for k, n, u in c['dict']])
print('Buckner_etal_SuppFigure5PanelE_dictionary_261110.csv written')
```
