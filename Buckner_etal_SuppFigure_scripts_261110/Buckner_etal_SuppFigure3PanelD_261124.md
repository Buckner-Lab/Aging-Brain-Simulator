# Supplementary Figure 3, panel D: Onset by APOE

```python
# Supplementary Figure 3D: across the 120,000 lives of the default world, the share who would be amyloid positive by each age if
# they lived, by number of APOE e4 alleles, under the default e4 risks from research cohorts (x3.76 and x8.93, 24% of e3/e3
# positive by 70; solid) and the alternative fitted to the population-based Mayo Clinic Study of Aging (x2.8 and x5.5, 26% of
# e3/e3 positive by 70; dotted), and the share whose amyloid turns positive before death. Prints the shares by 70 and the median
# ages under each and the share before death; saves the plot. Lives every life again (about 10 s).
# Run: python Buckner_etal_SuppFigure3PanelD_261124.py AgingBrain_Simulator_v104_261115.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
import sys, tempfile
from pathlib import Path
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from playwright.sync_api import sync_playwright
SIM = Path(sys.argv[1] if len(sys.argv) > 1 else 'AgingBrain_Simulator_v104_261115.html')
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
  const pA = { ...p, e4HR: 2.8, e44HR: 5.5, aPos70: 26 }, kA = E.prep(pA);                      // the population alternative (Roberts et al., 2018)
  for (let i = 0; i < p.N; i++) {                                                                  // year by year from its fixed draws
    E.setup(i, pA, kA, z, P); const aOnA = P.aOn;                                                  // amyloid onset if they lived, alternative
    E.setup(i, p, k, z, P); const death = E.live(P, p, k, () => {});
    out.push([P.n4, P.aOn, aOnA, death]);   // e4 alleles, amyloid onset if they lived (default, alternative), age at death
  }
  return out;
})()'''
W = np.array(run(JS), float); n4, aOn, aOnA, death = W.T
ages = np.arange(40, 111); plt.figure(figsize=(4, 2.8))
for on, ls, label in [(aOn, '-', 'research cohorts (default; solid)'), (aOnA, ':', 'population, Mayo Clinic Study of Aging (dotted)')]:
    print(label)
    for j in (0, 1, 2):
        a = on[n4 == j]; cum = [(a <= x).mean() for x in ages]
        print(f'  {j} e4 alleles ({len(a)} lives): {100 * (a <= 70).mean():.0f}% by 70 if they lived, median age {np.median(a):.0f}')
        plt.plot(ages, cum, ls, color=f'C{j}', label=f'{j} e4' if ls == '-' else None)
print(f'{100 * (aOn < death).mean():.0f}% of lives turn amyloid positive before death (default)')
plt.xlabel('Age'); plt.ylabel('Amyloid positive if they lived'); plt.legend(frameon=False); plt.tight_layout(); plt.savefig('Buckner_etal_SuppFigure3PanelD_261124.png', dpi=150)
```
