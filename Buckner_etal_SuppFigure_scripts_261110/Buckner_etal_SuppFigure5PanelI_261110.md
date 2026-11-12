# Supplementary Figure 5, panel I: Diagnosis by decline

```python
# Supplementary Figure 5I: Diagnosis by decline contrasts the default rule (global cognition at or below -2.3 SD after a fall of
# 1.2 SD since 40) with the fall alone, set so as many people 65+ have dementia. Prints the matching fall and dementia by
# ability under each rule. About 2 min.
# Run: python Buckner_etal_SuppFigure5PanelI_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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

STATS = r'''(() => { const w = state.run.agg.w26; let n = 0, d = 0; const g = [[0, 0], [0, 0], [0, 0]];
  for (let r = 0; r < w.n; r++) if (w.age[r] >= 65) { n++; d += w.dem[r]; const x = g[w.abil[r] < -0.43 ? 0 : w.abil[r] > 0.43 ? 2 : 1]; x[0]++; x[1] += w.dem[r]; }
  return { prev: d / n, byAbility: g.map(([m, k]) => k / m) }; })()'''
base = run(STATS); lo, hi = 1.2, 4.0
for _ in range(7):   # the fall alone that gives the same prevalence at 65+
    mid = (lo + hi) / 2; s = run(f'state.p.demThresh = 99; state.p.demDecline = {mid}; simulate(); 0', STATS)
    lo, hi = (mid, hi) if s['prev'] > base['prev'] else (lo, mid)
print(f"default rule: {100 * base['prev']:.1f}% of people 65+ have dementia; by childhood ability (lowest, middle, highest third): " + ', '.join(f'{100 * x:.1f}%' for x in base['byAbility']))
print(f"fall alone ({mid:.2f} SD since 40): {100 * s['prev']:.1f}%; by ability: " + ', '.join(f'{100 * x:.1f}%' for x in s['byAbility']))
```
