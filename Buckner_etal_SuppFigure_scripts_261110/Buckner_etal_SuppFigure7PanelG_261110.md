# Supplementary Figure 7, panel G: If SES and ability were tied

```python
# Supplementary Figure 7G: the change in dementia at 80-90 with both ties swept at once (SES and ability, each x0.4 to x1.5 per
# SD, holding the other). Prints its range and each tie alone at its setting, and saves the map.
# Run: python Buckner_etal_SuppFigure7PanelG_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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
  const run = state.run, p = run.p, w = run.agg.w26, Y = SY(), r0 = p.rSesAbility, P = [];   // the default world (Childhood mortality off)
  for (let r = 0; r < w.n; r++) if (w.age[r] >= 80 && w.age[r] <= 90)   // everyone alive in 2026 at 80-90, with the hazard of dying before 18
    P.push({ s: w.ses[r], a: w.abil[r], d: w.dem[r], f: w.fem[r], b: Y - w.age[r], H: -Math.log(1 - E.childQ(p, w.fem[r], Y - w.age[r]) / 100) });   // their birth year and sex carry
  // a tie per SD (SES holding ability, ability holding SES) as log coefficients, normalized to keep the mean hazard over births
  const coef = (sHR, aHR) => { const bs = Math.log(sHR), ba = Math.log(aHR); return { bs, ba, h: 0.5 * (bs * bs + ba * ba + 2 * r0 * bs * ba) }; };
  // the change childhood deaths make to dementia at 80-90 (points): the survivors, each weighted by their chance of reaching 18, minus everyone
  const change = (K, lvl = 1) => { let D = 0, WA = 0, DA = 0;
    for (const x of P) { const sv = Math.exp(-lvl * x.H * Math.exp(K.bs * x.s + K.ba * x.a - K.h)); D += x.d; WA += sv; DA += sv * x.d; }
    return 100 * (DA / WA - D / P.length); };
  const gx = Array.from({ length: 45 }, (_, i) => 0.4 * Math.pow(1.5 / 0.4, i / 44));
  return { gx, grid: gx.map((a) => gx.map((s) => change(coef(s, a)))), sesAlone: change(coef(p.chSesHR, 1)), abilAlone: change(coef(1, p.chAbilHR)) };
})()'''
c = run(JS); G = np.array(c['grid'])   # rows: ability tie, columns: SES tie
print(f"both ties: {G.min():+.2f} to {G.max():+.2f} points; SES alone (x0.87) {c['sesAlone']:+.2f}, ability alone (x0.81) {c['abilAlone']:+.2f}")
plt.figure(figsize=(3.6, 3)); plt.pcolormesh(c['gx'], c['gx'], G, cmap='RdBu', vmin=-0.8, vmax=0.8, shading='auto'); plt.colorbar(label='Change (points)')
plt.contour(c['gx'], c['gx'], G, [0], colors='k', linestyles='--'); plt.xscale('log'); plt.yscale('log')
plt.xlabel('SES tie (x per SD)'); plt.ylabel('Ability tie (x per SD)'); plt.tight_layout(); plt.savefig('Buckner_etal_SuppFigure7PanelG_261110.png', dpi=150)
```
