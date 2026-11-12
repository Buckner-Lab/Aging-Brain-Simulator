# Supplementary Figure 4, panel B: Reliability

```python
# Supplementary Figure 4B: in the study of Figure 2C-2H (400 people aged 60-90 in 2026 with MMSE 24 or more), with the default
# errors, each variable's correlation of one test with a retest in the same year and with its true value, as the Measurement
# page computes them (msStats). Prints them and saves the plot.
# Run: python Buckner_etal_SuppFigure4PanelB_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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
  // the study of Figure 2C-2H: Selection's Nondemented strategy, MMSE at least 24, 400 people aged 60-90 in 2026 (55% women)
  state.sel.strat = 'nondem'; Object.assign(state.sel.q.nondem, { lo: 60, hi: 90, n: 400, women: 55, by: 'mmse', mmse: 24 });
  const w = state.run.agg.w26, R = runSelection(), rows = R.sel;
  return MS_KEYS.map((k) => ({ k, ...msStats(w, rows, k) })); })()'''
T = run(JS)
for t in T: print(f"{t['k']:<5} retest r {t['rt']:.2f}, r with true {t['rv']:.2f}")
plt.figure(figsize=(3.6, 3.6)); y = np.arange(len(T))[::-1]
plt.plot([t['rt'] for t in T], y, 'ko', label='Retest'); plt.plot([t['rv'] for t in T], y, 'o', mfc='none', color='k', label='True value')
plt.yticks(y, [t['k'] for t in T]); plt.xlabel('Correlation'); plt.legend(frameon=False); plt.tight_layout(); plt.savefig('Buckner_etal_SuppFigure4PanelB_261110.png', dpi=150)
```
