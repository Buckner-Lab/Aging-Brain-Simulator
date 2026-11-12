# Supplementary Figure 4, panel E: Missed visits and dropout

```python
# Supplementary Figure 4E: missed visits and dropout set for illustration (10% of visits missed and 5% leaving each year at 70,
# with the application's factors), in the study of Figure 2C-2H visited every 2 years for 10 years. Prints the shares alive,
# still in the study and seen at each visit (mxStatus) and saves the plot.
# Run: python Buckner_etal_SuppFigure4PanelE_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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
  // the study of Figure 2C-2H: Selection's Nondemented strategy, MMSE at least 24, 400 people aged 60-90 in 2026 (55% women)
  state.sel.strat = 'nondem'; Object.assign(state.sel.q.nondem, { lo: 60, hi: 90, n: 400, women: 55, by: 'mmse', mmse: 24 });
  const w = state.run.agg.w26, R = runSelection(), rows = R.sel;
  Object.assign(state.mx, { miss: 10, drop: 5 }); const ys = [0, 2, 4, 6, 8, 10], n = rows.length;
  const S = ys.map(() => [0, 0, 0]);   // alive, still in the study, seen
  for (const r of rows) mxStatus(w, r, fuOf(w, r), ys).forEach((s, i) => { if (s !== 3) S[i][0]++; if (s === 0 || s === 1) S[i][1]++; if (s === 0) S[i][2]++; });
  return { ys, S: S.map((x) => x.map((v) => v / n)) }; })()'''
c = run(JS); S = np.array(c['S'])
for y, (a, i, s) in zip(c['ys'], S): print(f'year {y:>2}: alive {100 * a:.1f}%, still in the study {100 * i:.1f}%, seen {100 * s:.1f}%')
plt.figure(figsize=(3.6, 2.6))
for j, (lab, col) in enumerate([('Alive', '0.5'), ('In the study', '#2a78d6'), ('Seen', '#d9622e')]): plt.plot(c['ys'], 100 * S[:, j], 'o-', color=col, label=lab)
plt.xlabel('Years from entry'); plt.ylabel('% of the sample'); plt.legend(frameon=False); plt.tight_layout(); plt.savefig('Buckner_etal_SuppFigure4PanelE_261110.png', dpi=150)
```
