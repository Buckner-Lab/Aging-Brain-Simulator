# Supplementary Figure 2, panel A: Childhood ability as implemented

```python
# Supplementary Figure 2A: childhood ability's paths as the engine sets them (the world's settings and the constants the engine
# derives from them): SES, schooling, the level at 40, reserve, engagement, the brain at 40 and the dementia criterion.
# Run: python Buckner_etal_SuppFigure2PanelA_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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
  const run = state.run, p = run.p, k = run.k;
  const Phi = (x) => { const t = 1 / (1 + 0.3275911 * Math.abs(x) / Math.SQRT2), y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x / 2); return x >= 0 ? 0.5 * (1 + y) : 0.5 * (1 - y); };
  // expected years of schooling: a propensity eS*SES + eA*ability + eduRes*e is cut where the census shares fall for the birth year and sex
  const school = (a, s, f, b) => { const t = ((f ? 0 : 1) * k.eduNB + Math.max(0, Math.min(k.eduNB - 1, b - p.birthMin))) * 3, mu = k.eS * s + k.eA * a;
    const c = [0, 1, 2].map((j) => Phi((k.eduT[t + j] - mu) / k.eduRes)); return [c[0], c[1] - c[0], c[2] - c[1], 1 - c[2]].reduce((y, q, j) => y + q * E.EDU.years[j], 0); };
  return { p, k: { aC: k.aC, aCd: k.aCd, sC: k.sC, crNorm: k.crNorm, eA: k.eA, eS: k.eS, eduRes: k.eduRes, eduB: k.eduB, engRes: k.engRes },
    years: E.EDU.years, ref: E.EDU_REF, perSD: (school(1, 0, 1, 1950) - school(-1, 0, 1, 1950)) / 2 }; })()'''
c = run(JS); p, k = c['p'], c['k']
print(f"ability = {p['rSesAbility']:g} SES + {(1 - p['rSesAbility'] ** 2) ** 0.5:.2f} u")
print(f"schooling propensity S = {k['eA']:.2f} ability + {k['eS']:.2f} SES + {k['eduRes']:.2f} e; levels {c['years']} years; "
      f"each year above {c['ref']:.1f} adds {k['eduB']:.2f} SD to the level at 40")
print(f"level at 40: ability adds {k['aCd']:.2f} SD directly, {k['aCd'] + k['eduB'] * c['perSD']:.2f} with the schooling it brings "
      f"({c['perSD']:.2f} years per SD, a woman born in 1950); semantic memory {k['aC']:.2f}")
print(f"reserve = ({k['aC']:.2f} ability + {k['sC']:.2f} SES) / {k['crNorm']:.2f}, shrinking the AD cascade's and LATE's toll on cognition by {p['buffer']:g}% per SD")
print(f"engagement = {p['engAbil']:.2f} ability + {p['engSES']:.2f} SES + {k['engRes']:.2f} e: aging's toll on cognition {p['engCog']:g}% and brain {p['engBrain']:g}% less per SD, "
      f"vascular hazard x{p['engCV']:g}, motivation +{p['engMot']:g} SD")
print(f"brain at 40: hippocampal loss from 20 correlates {p['hipAbil']:g} with ability; dementia at global cognition <= {p['demThresh']:g} after a fall of >= {p['demDecline']:g} since 40")
```
