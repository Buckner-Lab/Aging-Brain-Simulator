# Supplementary Figure 5, panel G: Generational anchors

```python
# Supplementary Figure 5G: Generational anchors (version 95) analysed Fjell et al. (2026) and simulated worlds set to its
# anchors; that analysis needs the build and the preprint. What the anchors change is computable: the world's cohort settings
# and episodic memory at 70 by decade of birth.
# Run: python Buckner_etal_SuppFigure5PanelG_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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

JS = r'''(() => { const run = state.run, p = run.p, k = run.k, z = new Float64Array(E.NZ), P = {}, S = {};
  for (let i = 0; i < p.N; i++) { E.setup(i, p, k, z, P); const dec = 10 * Math.floor(P.b / 10);
    E.live(P, p, k, (a, v) => { if (a === 70) { const s = (S[dec] = S[dec] || [0, 0]); s[0] += v[E.IX.mem]; s[1]++; } }); }
  return { cohortCog: p.cohortCog, eduCog: p.eduCog, S }; })()'''
c = run(JS); print(f"cohort gain {c['cohortCog']:g} SD per decade at 40, besides schooling ({c['eduCog']:g} SD a year of it)")
for d, (s, n) in sorted(c['S'].items()): print(f'born {d}s: episodic memory at 70 {s / n:+.2f} SD ({n:,} alive at 70)')
```
