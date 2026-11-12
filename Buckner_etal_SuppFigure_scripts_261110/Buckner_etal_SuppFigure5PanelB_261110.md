# Supplementary Figure 5, panel B: Power

```python
# Supplementary Figure 5B: Power repeats the Intervention trial as set (aging slowed 30%, half treated, memory yearly for 6
# years, Welch's t on slopes) 200 times per sample size, with a new sample and randomization each time, and counts trials with p
# < 0.05. Its own seeds, so shares differ by chance from the stage's. About 1.5 min.
# Run: python Buckner_etal_SuppFigure5PanelB_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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

JS = r'''(() => { const w = state.run.agg.w26, q = state.iv, ys = [0, 1, 2, 3, 4, 5, 6], j = E.IX.mem, out = {};
  const st = (x) => { const n = x.length, m = x.reduce((a, b) => a + b, 0) / n; return { n, m, sd: Math.sqrt(x.reduce((a, b) => a + (b - m) ** 2, 0) / (n - 1)) }; };
  const slopes = (recs) => recs.map((p) => p.slope).filter(Number.isFinite);
  for (const N of [250, 500, 1000, 2000]) { let hit = 0, eff = 0;
    for (let t = 1; t <= 200; t++) {
      state.sel.seed = 1000 + t; state.sel.q.random.n = N; q.seed = 1000 + t;   // a new sample and a new randomization each time
      const R = runSelection(), { T, C } = ivArms(R), d = ivDiff(st(slopes(anRecs(w, T, ys, j, false, ivOf))), st(slopes(anRecs(w, C, ys, j, false, fuOf))));
      if (d && d.p < 0.05 && d.d > 0) hit++;
      eff += st(slopes(anRecs(w, T, ys, j, false, ivOf))).m - st(slopes(anRecs(w, T, ys, j, false, fuOf))).m;   // the true effect in the treated
    }
    out[N] = { power: hit / 200, effect: eff / 200 }; }
  return out; })()'''
P = run(JS)
for N, v in P.items(): print(f"{int(N):>5} participants: effect found by {100 * v['power']:.0f}% of 200 trials (true effect {v['effect']:+.4f} SD a year)")
plt.figure(figsize=(3.6, 2.6)); plt.plot([int(n) for n in P], [100 * v['power'] for v in P.values()], 'o-', color='#2a78d6'); plt.axhline(80, color='k', ls='--', lw=0.8)
plt.xlabel('Participants'); plt.ylabel('Trials finding the effect (%)'); plt.tight_layout(); plt.savefig('Buckner_etal_SuppFigure5PanelB_261110.png', dpi=150)
```
