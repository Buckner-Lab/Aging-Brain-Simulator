# Supplementary Figure 5, panel A: Distributions

```python
# Supplementary Figure 5A: Distributions compares a phenotype in the sample with everyone alive at the same ages: here episodic
# memory in Selection's random 400 (world 7, 2026), with the difference in means, its 95% CI and standardized size, from the
# app's own functions.
# Run: python Buckner_etal_SuppFigure5PanelA_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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

JS = r'''(() => { const w = state.run.agg.w26, R = runSelection();
  return { s: R.sel.map((r) => wv(w, r, 'mem')), a: R.world.map((r) => wv(w, r, 'mem')) }; })()'''
c = run(JS); s, a = np.array(c['s']), np.array(c['a'])
d = s.mean() - a.mean(); se = np.sqrt(s.var(ddof=1) / len(s) + a.var(ddof=1) / len(a))
print(f'sample {len(s)}: mean {s.mean():.2f} SD (SD {s.std(ddof=1):.2f}); everyone alive at those ages {len(a):,}: mean {a.mean():.2f} (SD {a.std(ddof=1):.2f})')
print(f'difference {d:+.2f} SD (95% CI {d - 1.96 * se:+.2f} to {d + 1.96 * se:+.2f}); standardized {d / a.std(ddof=1):+.2f}')
plt.figure(figsize=(4, 2.6)); bins = np.linspace(-5, 4, 46)
plt.hist(a, bins, density=True, color='0.8', label='Everyone alive'); plt.hist(s, bins, density=True, histtype='step', color='#d9622e', lw=1.5, label='Sample')
plt.xlabel('Episodic memory (SD)'); plt.legend(frameon=False); plt.tight_layout(); plt.savefig('Buckner_etal_SuppFigure5PanelA_261110.png', dpi=150)
```
