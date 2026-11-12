# Supplementary Figure 6, panel B: Who is lined up

```python
# Supplementary Figure 6B: of Selection's random sample of 400 (ages 18-100, world 7, study year 2026), who became amyloid
# positive (20 Centiloid) at some age of their simulated lives, who did by 2026, and the 30 that Biomarker timelines draws with
# its own random key. Prints the counts and saves a bar chart.
# Run: python Buckner_etal_SuppFigure6PanelB_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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
  const by = (r) => T.get(r).aPos <= w.age[r];   // positive by 2026: at or before their age in the study year
  return { sample: R.sel.length, positive: pos.length, by2026: pos.filter(by).length, drawn: drawn.length, drawnBy2026: drawn.filter(by).length };
})()'''
c = run(JS); later, never = c['positive'] - c['by2026'], c['sample'] - c['positive']
print(f"sample {c['sample']}: amyloid positive at some age {c['positive']} (by 2026 {c['by2026']}, later {later}); never {never}")
print(f"drawn {c['drawn']}: {c['drawnBy2026']} positive by 2026, {c['drawn'] - c['drawnBy2026']} later")
plt.figure(figsize=(4, 2.6)); plt.bar(['Positive by 2026', 'Positive later', 'Never'], [c['by2026'], later, never], color=['#c98500', '#f3d28c', '#dcdad3'])
plt.bar(['Positive by 2026', 'Positive later'], [c['drawnBy2026'], c['drawn'] - c['drawnBy2026']], fill=False, edgecolor='k', label='Drawn')
plt.ylabel('Participants'); plt.legend(frameon=False); plt.tight_layout(); plt.savefig('Buckner_etal_SuppFigure6PanelB_261110.png', dpi=150)
```
