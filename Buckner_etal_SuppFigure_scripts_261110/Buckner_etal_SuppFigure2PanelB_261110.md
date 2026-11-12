# Supplementary Figure 2, panel B: How the cohort works

```python
# Supplementary Figure 2B: every life is simulated from 18 to death whatever the study year; the study year picks who is alive
# and at what age. Prints how many are alive at 18-100 in 2026, the cohort settings, and the early-cohort ability check (the
# world's ten earliest birth years at 77-81, standing in for the Lothian Birth Cohort 1921); saves a Lexis plot of 150 lives.
# Run: python Buckner_etal_SuppFigure2PanelB_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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

JS = r'''(() => { const run = state.run, w = run.agg.w26, p = run.p; let n = 0; for (let r = 0; r < w.n; r++) if (w.age[r] <= 100) n++;
  const lives = Array.from({ length: 150 }, (_, j) => { const t = E.trace(j * 800, p, run.k, run.S.saRef); return { b: t.b, death: t.death, dem: t.demAge }; });
  return { alive: n, cohortCog: p.cohortCog, mortImprove: p.mortImprove, r: run.S.chk.rAbil * Math.sqrt(0.85 * 0.80), lives }; })()'''
c = run(JS)
print(f"alive in 2026 at 18-100: {c['alive']:,}; later births: +{c['cohortCog']:g} SD at 40 per decade (besides schooling), mortality {c['mortImprove']:g}% lower per decade")
print(f"early-cohort check: ability vs global cognition at 77-81, r = {c['r']:.2f} allowing for test reliabilities (Gow et al. 2011: 0.66)")
plt.figure(figsize=(4, 3))
for L in c['lives']:
    end = L['death']; plt.plot([L['b']] * 2, [18, min(end, L['dem']) if L['dem'] < 999 else end], color='0.4', lw=0.6)
    if L['dem'] < 999: plt.plot([L['b']] * 2, [L['dem'], end], color='#c23b3b', lw=0.8)
b = np.array([1926, 2008]); plt.plot(b, 2026 - b, 'k'); plt.plot(b, 1990 - b, 'k--'); plt.axhline(40, color='k', ls=':', lw=0.8)
plt.ylim(18, 105); plt.xlabel('Year of birth'); plt.ylabel('Age'); plt.tight_layout(); plt.savefig('Buckner_etal_SuppFigure2PanelB_261110.png', dpi=150)
```
