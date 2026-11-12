# Supplementary Figure 4, panel D: Practice effects

```python
# Supplementary Figure 4D: the practice model for episodic memory (gain at the first retest 0.25 SD, ceiling 0.45 SD, half-life
# 3 years): the expected gain over the first test at each of eight tests a month, six months, a year or two years apart, from
# the application's own functions (msExpo, msPrac). Prints the gains and saves the plot.
# Run: python Buckner_etal_SuppFigure4PanelD_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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

JS = r'''([1, 6, 12, 24].map((mo) => { const ys = Array.from({ length: 8 }, (_, i) => i * mo / 12);
  return { mo, gain: ys.map((_, i) => msPrac('mem', msExpo(ys, i, state.ms.mem.ph))) }; }))'''
plt.figure(figsize=(3.6, 2.6))
for d in run(JS):
    print(f"every {d['mo']} months: " + ', '.join(f'{g:.2f}' for g in d['gain'])); plt.plot(range(1, 9), d['gain'], 'o-', label=f"{d['mo']} months")
plt.xlabel('Test'); plt.ylabel('Practice gain (SD)'); plt.legend(frameon=False); plt.tight_layout(); plt.savefig('Buckner_etal_SuppFigure4PanelD_261110.png', dpi=150)
```
