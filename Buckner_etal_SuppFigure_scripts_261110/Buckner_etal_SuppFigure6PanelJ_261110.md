# Supplementary Figure 6, panel J: If the settings changed

```python
# Supplementary Figure 6J: the average course of episodic memory as the stage is set (30 drawn, positive at any age), with 200
# drawn, and with 30 drawn only from those positive by 2026. Prints each at -20, 0 and +20 years from positivity and saves the
# plot.
# Run: python Buckner_etal_SuppFigure6PanelJ_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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

JS = r'''(() => { const out = {};
  for (const [name, NDRAW, BY2026] of [['as set (30)', 30, false], ['200 participants', 200, false], ['positive by 2026', 30, true]]) {
    const w = state.run.agg.w26, run = state.run, R = runSelection();
    const T = new Map(R.sel.map((r) => [r, E.trace(w.id[r], run.p, run.k, run.S.saRef)]));
    const pos = R.sel.filter((r) => T.get(r).aPos < 999 && (!BY2026 || T.get(r).aPos <= w.age[r]));
    const drawn = pos.slice().sort((a, b) => u01(8301, w.id[a]) - u01(8301, w.id[b])).slice(0, NDRAW);   // the stage's key
    out[name] = drawn.map((r) => { const t = T.get(r), a0 = t.aPos, j = E.IX.mem;
      return Array.from({ length: 41 }, (_, x) => { const i = a0 + x - 20 - E.AGE0; return i >= 0 && i < t.n ? t.tr[j * t.n + i] : null; }); });
  }
  return out; })()'''
X = np.arange(-20, 21); plt.figure(figsize=(4, 2.8))
for (name, V), col in zip(run(JS).items(), ['k', '#2a78d6', '#d9622e']):
    V = np.array([[np.nan if x is None else x for x in v] for v in V]); alive = np.isfinite(V).sum(0)
    mean = np.where(alive >= 5, np.nanmean(V, 0), np.nan)   # the average course: those alive each year, where 5 or more are
    print(f'{name}: {len(V)} drawn; memory {mean[0]:.2f} SD at -20, {mean[20]:.2f} at 0, {mean[40]:.2f} at +20')
    plt.plot(X, mean, color=col, lw=1.6, label=name)
plt.axvline(0, color='k', ls=':', lw=0.8); plt.xlabel('Years from amyloid positivity'); plt.ylabel('Memory, average (SD)')
plt.legend(frameon=False); plt.tight_layout(); plt.savefig('Buckner_etal_SuppFigure6PanelJ_261110.png', dpi=150)
```
