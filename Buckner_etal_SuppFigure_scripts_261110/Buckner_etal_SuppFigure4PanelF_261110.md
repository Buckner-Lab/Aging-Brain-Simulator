# Supplementary Figure 4, panel F: What the study records

```python
# Supplementary Figure 4F: mean change in episodic memory from entry (visits every 2 years for 10; attrition as in E): true
# among everyone alive, measured with error, with error and practice, true among those seen, and measured with practice among
# those seen; then, without error, what practice and attrition hide.
# Run: python Buckner_etal_SuppFigure4PanelF_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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
  Object.assign(state.mx, { miss: 10, drop: 5 }); const ys = [0, 2, 4, 6, 8, 10], out = {};
  const mean = (meas, prac, mx) => { const P = anRecs(w, rows, ys, E.IX.mem, meas, fuOf, prac, mx);   // each visit's mean change from entry, among those seen there
    return ys.map((_, k) => { let s = 0, n = 0; for (const p of P) { const i = anAt(p, k), i0 = anAt(p, 0); if (i >= 0 && i0 >= 0) { s += p.pts[i][1] - p.pts[i0][1]; n++; } } return s / n; }); };
  for (const [name, meas, prac, mx] of [['true, everyone alive', 0, 0, 0], ['measured with error', 1, 0, 0], ['measured with error and practice', 1, 1, 0],
    ['true, those still seen', 0, 0, 1], ['measured with practice, those still seen', 1, 1, 1], ['true with practice (no error)', 0, 1, 0], ['true with practice, those still seen', 0, 1, 1]])
    out[name] = mean(!!meas, !!prac, !!mx);
  return { ys, out }; })()'''
c = run(JS); O = {k: np.array(v) for k, v in c['out'].items()}; T = O['true, everyone alive']
for k in list(O)[:5]: print(f'{k}: {O[k][-1]:+.2f} SD by year 10 (year 2: {O[k][1]:+.2f})')
print(f"error moves the 10-year change by {O['measured with error'][-1] - T[-1]:+.2f} SD; without it, practice hides "
      f"{100 * (O['true with practice (no error)'][1] - T[1]) / -T[1]:.0f}% of the decline by year 2 and {100 * (O['true with practice (no error)'][-1] - T[-1]) / -T[-1]:.0f}% by 10, "
      f"attrition {100 * (O['true, those still seen'][-1] - T[-1]) / -T[-1]:.0f}%, both {100 * (O['true with practice, those still seen'][-1] - T[-1]) / -T[-1]:.0f}%")
plt.figure(figsize=(4, 2.8))
for k in list(O)[:5]: plt.plot(c['ys'], O[k], 'o-', label=k)
plt.axhline(0, color='k', lw=0.6); plt.xlabel('Years from entry'); plt.ylabel('Change in episodic memory (SD)'); plt.legend(frameon=False, fontsize=6)
plt.tight_layout(); plt.savefig('Buckner_etal_SuppFigure4PanelF_261110.png', dpi=150)
```
