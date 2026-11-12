# Supplementary Figure 2, panel G: The world by ability

```python
# Supplementary Figure 2G: everyone in the default world in three groups of childhood ability (below -1, -1 to +1, above +1 SD):
# how many are alive at 40, their mean SES and schooling, mean global cognition among the living by age, and the share of those
# alive at 40 with dementia by each age. Prints the numbers and saves the plot. Lives every life again (about 15 s).
# Run: python Buckner_etal_SuppFigure2PanelG_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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

JS = r'''(() => { const run = state.run, p = run.p, k = run.k, z = new Float64Array(E.NZ), P = {};
  const G = [0, 1, 2].map(() => ({ n40: 0, ses: 0, edu: 0, gS: new Array(61).fill(0), gN: new Array(61).fill(0), dem: new Array(61).fill(0) }));   // ages 40-100
  for (let i = 0; i < p.N; i++) {
    E.setup(i, p, k, z, P); const g = G[P.abil < -1 ? 0 : P.abil > 1 ? 2 : 1]; let fD = 999, at40 = false;
    E.live(P, p, k, (a, v, dem) => { if (a < 40 || a > 100) return; if (a === 40) at40 = true; g.gS[a - 40] += (v[E.IX.mem] + v[E.IX.spd] + v[E.IX.exe]) / 3; g.gN[a - 40]++; if (dem && fD === 999) fD = a; });
    if (at40) { g.n40++; g.ses += P.ses; g.edu += P.eduY; if (fD <= 100) for (let a = fD; a <= 100; a++) g.dem[a - 40]++; }
  }
  return G; })()'''
G = run(JS); age = np.arange(40, 101); fig, ax = plt.subplots(2, 1, figsize=(4, 4.4), sharex=True)
for g, lab, col in zip(G, ['below -1 SD', '-1 to +1 SD', 'above +1 SD'], ['#e377c2', '0.5', '#2a78d6']):
    gm = np.array(g['gS']) / np.maximum(1, g['gN']); dem = np.array(g['dem']) / g['n40']
    print(f"ability {lab}: {g['n40']:,} alive at 40; SES {g['ses'] / g['n40']:+.2f}, schooling {g['edu'] / g['n40']:.1f} years; dementia by 85 {100 * dem[45]:.1f}%")
    ax[0].plot(age, gm, color=col, label=lab); ax[1].plot(age, 100 * dem, color=col)
ax[0].set_ylabel('Global cognition (SD)'); ax[1].set_ylabel('Dementia (%)'); ax[1].set_xlabel('Age'); ax[0].legend(frameon=False, fontsize=7)
plt.tight_layout(); plt.savefig('Buckner_etal_SuppFigure2PanelG_261110.png', dpi=150)
```
