# Supplementary Figure 3, panel D: Onset by APOE

```python
# Supplementary Figure 3D: across the 120,000 lives of the default world, the share who would be amyloid positive by each age if
# they lived, by number of APOE e4 alleles, and the share whose amyloid turns positive before death. Prints the shares by 70,
# the median ages and the share before death; saves the plot. Lives every life again (about 20 s).
# Run: python Buckner_etal_SuppFigure3PanelD_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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
  const run = state.run, p = run.p, k = run.k, z = new Float64Array(E.NZ), P = {}, out = [];   // every life of the default world, lived again
  for (let i = 0; i < p.N; i++) {                                                                  // year by year from its fixed draws
    E.setup(i, p, k, z, P); let fA = 999, fT = 999, fD = 999;
    const death = E.live(P, p, k, (a, v, dem) => { if (fA === 999 && v[E.IX.amy] >= E.A_POS) fA = a; if (fT === 999 && v[E.IX.tau] >= E.T_POS) fT = a; if (fD === 999 && dem) fD = a; });
    out.push([P.n4, P.aOn, fA, fT, fD, death]);   // e4 alleles, amyloid onset if they lived, first ages amyloid+ / tau+ / dementia while alive, death
  }
  return out;
})()'''
W = np.array(run(JS), float); n4, aOn, fA, death = W[:, 0], W[:, 1], W[:, 2], W[:, 5]
ages = np.arange(40, 111); plt.figure(figsize=(4, 2.8))
for j in (0, 1, 2):
    a = aOn[n4 == j]; cum = [(a <= x).mean() for x in ages]
    print(f'{j} e4 alleles ({len(a)} lives): {100 * (a <= 70).mean():.0f}% by 70 if they lived, median age {np.median(a):.0f}')
    plt.plot(ages, cum, label=f'{j} e4')
print(f'{100 * (aOn < death).mean():.0f}% of lives turn amyloid positive before death')
plt.xlabel('Age'); plt.ylabel('Amyloid positive if they lived'); plt.legend(frameon=False); plt.tight_layout(); plt.savefig('Buckner_etal_SuppFigure3PanelD_261110.png', dpi=150)
```
