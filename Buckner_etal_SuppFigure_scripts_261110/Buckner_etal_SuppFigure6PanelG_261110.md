# Supplementary Figure 6, panel G: Hippocampal volume

```python
# Supplementary Figure 6G: hippocampal volume (mL) of the 30 drawn by Biomarker timelines, from 20 years before to 20 after
# turning amyloid positive (true values), with the average course (mean of those alive, where 5 or more are). Prints the stage's
# table and saves the plot.
# Run: python Buckner_etal_SuppFigure6PanelG_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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

JS = r'''(() => {
  const w = state.run.agg.w26, run = state.run, R = runSelection();   // Selection's sample (random 400, ages 18-100, world 7, 2026)
  const T = new Map(R.sel.map((r) => [r, E.trace(w.id[r], run.p, run.k, run.S.saRef)]));   // each participant's whole simulated life
  const pos = R.sel.filter((r) => T.get(r).aPos < 999);   // amyloid positive: t.aPos, the first year of age at 20 CL or more
  const drawn = pos.slice().sort((a, b) => u01(8301, w.id[a]) - u01(8301, w.id[b])).slice(0, 30);   // the stage's key, u01(8300 + seed 1, life)
  return drawn.map((r) => { const t = T.get(r), a0 = t.aPos, j = E.IX['hip'];   // values from 20 years before positivity to 20 after; null before 18 or after death
    return { a0, v: Array.from({ length: 41 }, (_, x) => { const i = a0 + x - 20 - E.AGE0; return i >= 0 && i < t.n ? t.tr[j * t.n + i] : null; }) }; });
})()'''
V = np.array([[np.nan if x is None else x for x in p['v']] for p in run(JS)])   # 30 participants x 41 years
X = np.arange(-20, 21); alive = np.isfinite(V).sum(0); mean = np.where(alive >= 5, np.nanmean(V, 0), np.nan)
for d in (-20, -10, 0, 10, 20): print(f'{d:+d} years: average {mean[d + 20]:.2f} mL, alive {alive[d + 20]}')
plt.figure(figsize=(4, 2.8)); plt.plot(X, V.T, color='#1baf7a', lw=0.7, alpha=0.5); plt.plot(X, mean, 'k', lw=2)
plt.axvline(0, color='k', ls=':', lw=0.8)
plt.xlabel('Years from amyloid positivity'); plt.ylabel('Hippocampal volume (mL)'); plt.tight_layout(); plt.savefig('Buckner_etal_SuppFigure6PanelG_261110.png', dpi=150)
```
