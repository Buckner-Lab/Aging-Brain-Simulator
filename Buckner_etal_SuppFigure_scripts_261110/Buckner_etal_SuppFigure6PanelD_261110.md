# Supplementary Figure 6, panel D: Lined up, with what followed

```python
# Supplementary Figure 6D: the 30 lined up on the year they became amyloid positive (0), with when each became tau positive
# (1.30 SUVR), developed dementia and died within the 20 years after, as the stage's caption counts them (tau positivity before
# amyloid counts). Prints the counts and medians and saves the plot.
# Run: python Buckner_etal_SuppFigure6PanelD_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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
  return drawn.map((r) => { const t = T.get(r); return { a0: t.aPos, tau: t.tPos, dem: t.demAge, last: E.AGE0 + t.n - 1 }; });   // 999: never
})()'''
L = sorted(run(JS), key=lambda p: p['a0'])
tau = [p['tau'] - p['a0'] for p in L if p['tau'] < 999 and p['tau'] - p['a0'] <= 20]
dem = [p['dem'] - p['a0'] for p in L if p['dem'] < 999 and p['dem'] - p['a0'] <= 20]
died = [p for p in L if p['last'] < p['a0'] + 20]
print(f'within 20 years: {len(tau)} tau positive (median {np.median(tau):g} years after; {sum(x < 0 for x in tau)} before amyloid), '
      f'{len(dem)} dementia (median {np.median(dem):g}), {len(died)} died')
plt.figure(figsize=(4, 3.6))
for i, p in enumerate(L):
    plt.plot([max(18, p['a0'] - 20) - p['a0'], min(p['last'], p['a0'] + 20) - p['a0']], [i, i], color='0.6', lw=1)
    if p['tau'] < 999 and p['tau'] - p['a0'] <= 20: plt.plot(p['tau'] - p['a0'], i, 'D', color='#c98500', ms=3)
    if p['dem'] < 999 and p['dem'] - p['a0'] <= 20: plt.plot(p['dem'] - p['a0'], i, 'o', color='#c23b3b', ms=4)
    if p['last'] < p['a0'] + 20: plt.plot(p['last'] - p['a0'], i, 'ko', ms=3)
plt.axvline(0, color='k', ls=':', lw=0.8); plt.yticks([]); plt.xlabel('Years from amyloid positivity'); plt.tight_layout(); plt.savefig('Buckner_etal_SuppFigure6PanelD_261110.png', dpi=150)
```
