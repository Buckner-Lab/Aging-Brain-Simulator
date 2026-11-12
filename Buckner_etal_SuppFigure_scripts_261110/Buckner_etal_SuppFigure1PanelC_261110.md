# Supplementary Figure 1, panel C: Describes and checks itself

```python
# Supplementary Figure 1C: the model's description and its 13 reality checks are generated from the current settings
# (wpModelHtml, wpChecks). Prints the description of episodic memory's aging and which checks are in range with aging's late
# rise (as set) and with it switched off (mem70, spd70 and exe70 set to 0, a new world).
# Run: python Buckner_etal_SuppFigure1PanelC_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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

import re, html
JS = r'''(() => { wpChecks();   // writes the checks into the page; read them back with the description of episodic memory's aging
  const t = wpModelHtml().replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' '), i = t.indexOf('episodic memory loss per year');
  return { desc: t.slice(i, i + 190), say: $('#wp-checks-say').textContent,
    checks: [...document.querySelectorAll('#wp-checks-body tbody tr')].map((tr) => [tr.cells[0].firstChild.textContent, tr.cells[1].textContent, tr.cells[3].textContent, tr.cells[5].textContent]) }; })()'''
for name, c in [('with the late rise', run(JS)), ('without it', run('state.p.mem70 = state.p.spd70 = state.p.exe70 = 0; simulate(); 0', JS))]:
    print(f"{name}: {c['say']}\n  description: {html.unescape(c['desc'])}")
    for label, v, rng, status in c['checks']:
        if 'In range' not in status: print(f'  outside: {label}: {v} (range {rng})')
```
