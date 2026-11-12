# Supplementary Figure 4, panel C: Error at a cut point

```python
# Supplementary Figure 4C: amyloid PET measured once (error 4 CL) against its true value in the study of Figure 2C-2H,
# classified at 20 Centiloid. Prints who is called positive in error, who is missed and their true values; saves the plot (-10
# to 60 CL shown).
# Run: python Buckner_etal_SuppFigure4PanelC_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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
  return rows.map((r) => { const t = wv(w, r, 'amy'); return [t, msAt('amy', t, w.id[r], w.fem[r], w.age[r], wv(w, r, 'cdr'), 0)]; }); })()'''
A = np.array(run(JS)); t, m = A[:, 0], A[:, 1]
fp, fn = (t < 20) & (m >= 20), (t >= 20) & (m < 20); wrong = t[fp | fn]
print(f'{len(t)} people; {(t >= 20).sum()} truly positive; {fp.sum()} called positive in error, {fn.sum()} of the truly positive missed; '
      f'their true values {wrong.min():.0f} to {wrong.max():.0f} CL')
sh = (t >= -10) & (t <= 60) & (m >= -10) & (m <= 60); print(f'{sh.sum()} people with both values between -10 and 60 CL are shown')
plt.figure(figsize=(3.4, 3.2)); plt.plot(t[sh], m[sh], 'o', ms=2.5, color='0.6'); plt.plot(t[fp | fn], m[fp | fn], 'o', ms=4, color='#c23b3b')
plt.axvline(20, color='k', ls='--', lw=0.8); plt.axhline(20, color='k', ls='--', lw=0.8); plt.xlabel('True amyloid PET (CL)'); plt.ylabel('Measured (CL)')
plt.tight_layout(); plt.savefig('Buckner_etal_SuppFigure4PanelC_261110.png', dpi=150)
```
