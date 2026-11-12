# Supplementary Figure 5, panel F: Life map

```python
# Supplementary Figure 5F: Life map: 2,000 lives (every 60th), each a faint trail of episodic memory by age up to a calendar
# year from 1990 to 2040. Prints how many are alive in each year shown and saves maps for 1990, 2015 and 2040.
# Run: python Buckner_etal_SuppFigure5PanelF_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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

JS = r'''(() => { const run = state.run, j = E.IX.mem;
  return Array.from({ length: 2000 }, (_, i) => { const t = E.trace(i * 60, run.p, run.k, run.S.saRef); return { b: t.b, mem: Array.from({ length: t.n }, (_, a) => t.tr[j * t.n + a]) }; }); })()'''
L = run(JS); fig, ax = plt.subplots(1, 3, figsize=(9, 2.8), sharey=True)
for a, year in zip(ax, (1990, 2015, 2040)):
    alive = 0
    for p in L:
        age = np.arange(18, 18 + len(p['mem'])); keep = p['b'] + age <= year
        if keep.any(): a.plot(age[keep], np.array(p['mem'])[keep], color='k', lw=0.2, alpha=0.15)
        if p['b'] + 18 <= year < p['b'] + 18 + len(p['mem']): alive += 1
    print(f'{year}: {alive} of the 2,000 alive'); a.set_title(str(year)); a.set_xlabel('Age')
ax[0].set_ylabel('Episodic memory (SD)'); plt.tight_layout(); plt.savefig('Buckner_etal_SuppFigure5PanelF_261110.png', dpi=150)
```
