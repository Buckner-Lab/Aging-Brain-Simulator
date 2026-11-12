# Supplementary Figure 5, panel H: Alternative worlds

```python
# Supplementary Figure 5H: Alternative worlds: dementia among people 65+ in 2026 in the default world, with AD cured (AD cascade
# off) and with AD prevented in a fixed random half of lives. The stage's pandemic world was its own construction and is not
# reproduced.
# Run: python Buckner_etal_SuppFigure5PanelH_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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

WORLD = r'''(() => { const w = state.run.agg.w26, o = {}; for (let r = 0; r < w.n; r++) if (w.age[r] >= 65) o[w.id[r]] = w.dem[r]; return o; })()'''
d0 = run(WORLD); d1 = run('state.p.ad = false; simulate(); 0', WORLD)   # life number -> dementia, for everyone 65+ in 2026
mix = {}
for i in set(d0) | set(d1):
    src = d1 if (int(i) * 2654435761 % 2**32) / 2**32 < 0.5 else d0   # a fixed draw puts each life in the cured half or not
    if i in src: mix[i] = src[i]
for name, d in (('default world', d0), ('AD cured', d1), ('AD prevented in half', mix)):
    print(f'{name}: {100 * sum(d.values()) / len(d):.1f}% of {len(d):,} people 65 and older have dementia')
```
