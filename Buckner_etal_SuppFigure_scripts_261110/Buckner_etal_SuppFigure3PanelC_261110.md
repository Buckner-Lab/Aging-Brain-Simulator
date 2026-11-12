# Supplementary Figure 3, panel C: Order of change

```python
# Supplementary Figure 3C: the reference person's changes from the cascade (amyloid positive at 65 minus never), each as a share
# of where it stands 30 years after positivity (pTau217 on its log scale, as the World page draws it). Prints when each is
# halfway and saves the plot.
# Run: python Buckner_etal_SuppFigure3PanelC_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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
  const p = state.run.p, K = ['amy', 'ptau', 'tau', 'hip', 'mem', 'cdr'];   // the engine's reference person: a woman born in 1950, APOE e3/e3,
  const life = (over) => { const o = E.prototype(p, over, 100, 40);           // average traits and draws, no vascular risk or LATE; aOn: amyloid positive at
    return { age: o.age, ...Object.fromEntries(K.map((k) => [k, o.v.map((v) => v[E.IX[k]])])) }; };   // that age (999: never). From 40 to 100
  return { on: life({ aOn: 65 }), off: life({ aOn: 999 }) }; })()'''
c = run(JS); age = np.array(c['on']['age']); yrs = age - 65; keep = (yrs >= 0) & (yrs <= 30)
plt.figure(figsize=(4, 2.8))
for k, lab in [('ptau', 'pTau217'), ('amy', 'Amyloid PET'), ('tau', 'Tau PET'), ('hip', 'Hippocampus'), ('mem', 'Episodic memory'), ('cdr', 'CDR-SB')]:
    on, off = np.array(c['on'][k]), np.array(c['off'][k]); d = np.log(on / off) if k == 'ptau' else on - off   # pTau217 on its log scale
    d = (d / d[age == 95])[keep]   # the cascade's change, as a share of where it stands 30 years after positivity
    print(f'{lab}: halfway after {np.interp(0.5, d[d < 1], yrs[keep][d < 1]):.0f} years'); plt.plot(yrs[keep], d, label=lab)
plt.xlabel('Years after amyloid positivity'); plt.ylabel('Share of change at 30 years'); plt.legend(frameon=False, fontsize=7); plt.tight_layout(); plt.savefig('Buckner_etal_SuppFigure3PanelC_261110.png', dpi=150)
```
