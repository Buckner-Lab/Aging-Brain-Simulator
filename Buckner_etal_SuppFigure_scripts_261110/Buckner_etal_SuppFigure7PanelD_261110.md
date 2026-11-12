# Supplementary Figure 7, panel D: Who died is assumed

```python
# Supplementary Figure 7D: the ties of dying before 18 to SES and ability (hazard ratios per SD, each holding the other) for the
# World's one kind and the stage's four, SES alone (SES x ability^0.5), and how much more often the lowest SES fifth dies than
# the highest. The literature spans (bars) are not computed.
# Run: python Buckner_etal_SuppFigure7PanelD_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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

JS = r'''(() => { const p = state.run.p, r0 = p.rSesAbility;
  const Phi = (x) => { const t = 1 / (1 + 0.2316419 * Math.abs(x)), y = Math.exp(-0.5 * x * x) / 2.5066282746310002;   // the normal CDF
    const c = y * t * (0.319381530 + t * (-0.356563782 + t * (1.781477937 + t * (-1.821255978 + t * 1.330274429)))); return x >= 0 ? 1 - c : c; };
  const fifths = (g) => Phi(-0.8416212 - g) / Phi(g - 0.8416212);   // SES alone scales the hazard by e^(g SES - g^2/2): lowest fifth / highest fifth
  return [['One kind (the World)', p.chSesHR, p.chAbilHR], ['Before 5, internal', 0.94, 0.75], ['Before 5, external', 0.77, 0.95],
    ['5-17, internal', 0.96, 0.80], ['5-17, external', 0.91, 0.78]].map(([k, s, a]) =>
    ({ k, s, a, alone: s * Math.pow(a, r0), fifths: fifths(Math.log(s) + r0 * Math.log(a)) }));
})()'''
T = run(JS)
for t in T: print(f"{t['k']:<22} SES x{t['s']:.2f} (alone x{t['alone']:.2f}; lowest fifth {t['fifths']:.1f} times the highest), ability x{t['a']:.2f}")
plt.figure(figsize=(4, 2.4)); y = np.arange(len(T))[::-1]
plt.plot([t['alone'] for t in T], y, 'o', color='k', label='SES alone'); plt.plot([t['a'] for t in T], y, 'o', mfc='none', color='k', label='Ability')
plt.axvline(1, color='k', ls='--', lw=0.8); plt.yticks(y, [t['k'] for t in T]); plt.xlabel('Hazard ratio per SD'); plt.legend(frameon=False)
plt.tight_layout(); plt.savefig('Buckner_etal_SuppFigure7PanelD_261110.png', dpi=150)
```
