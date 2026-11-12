# Supplementary Figure 6, panel C: Positive at different ages

```python
# Supplementary Figure 6C: the 30 drawn by Biomarker timelines, by the age they became amyloid positive, each with the 20 years
# before and after (cut at death). Prints the ages at positivity, how many lie after 2026 and how many died within 20 years, and
# saves the plot.
# Run: python Buckner_etal_SuppFigure6PanelC_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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
  return drawn.map((r) => ({ a0: T.get(r).aPos, age26: w.age[r], last: E.AGE0 + T.get(r).n - 1 }));   // last: the last year of life
})()'''
L = sorted(run(JS), key=lambda p: p['a0']); a0 = np.array([p['a0'] for p in L])
print(f"positive at ages {a0.min()} to {a0.max()} (median {np.median(a0):g}); after 2026: {sum(p['a0'] > p['age26'] for p in L)}; "
      f"died within 20 years: {sum(p['last'] < p['a0'] + 20 for p in L)}")
plt.figure(figsize=(4, 3.6))
for i, p in enumerate(L):
    lo, hi = max(18, p['a0'] - 20), min(p['last'], p['a0'] + 20)
    plt.plot([lo, hi], [i, i], color='0.6', lw=1); plt.plot(p['a0'], i, 'o', color='#c98500', ms=4)
    if p['last'] < p['a0'] + 20: plt.plot(hi, i, 'ko', ms=3)
plt.yticks([]); plt.xlabel('Age (years)'); plt.tight_layout(); plt.savefig('Buckner_etal_SuppFigure6PanelC_261110.png', dpi=150)
```
