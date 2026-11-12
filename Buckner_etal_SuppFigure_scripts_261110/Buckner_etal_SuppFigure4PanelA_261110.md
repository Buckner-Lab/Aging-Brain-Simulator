# Supplementary Figure 4, panel A: The measurement process

```python
# Supplementary Figure 4A: the Measurement process as the application starts: each variable's error at 70 with its factors (age,
# CDR-SB, women), validity, and practice model (first gain, ceiling, half-life); and missed visits and dropout, off to start,
# with their factors.
# Run: python Buckner_etal_SuppFigure4PanelA_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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

c = run("({ ms: state.ms, mx: MX_DEF, keys: MS_KEYS })")
print('variable  error@70  x/decade  x/CDR-SB  x women  validity  practice: first, ceiling, half-life (y)')
for k in c['keys']:
    s = c['ms'][k]; pr = f"{s['p1']:g}, {s['pc']:g}, {s['ph']:g}" if s['p1'] or s['pc'] else 'none'
    print(f"{k:<9} {s['err']:<9g} {s['age']:<9g} {s['cdr']:<9g} {s['sex']:<8g} {s['val']:<9g} {pr}")
m = c['mx']; print(f"missed visits {m['miss']}% and dropout {m['drop']}% a year at 70 (none to start); factors per decade of age x{m['missAge']} and x{m['dropAge']}, "
                   f"per SD lower SES x{m['missSes']} and x{m['dropSes']}, per SD of decline x{m['missDec']} and x{m['dropDec']}, once dementia begins x{m['missDem']} and x{m['dropDem']}")
```
