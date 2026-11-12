# Supplementary Figure 7, panel F: If SES were tied more or less

```python
# Supplementary Figure 7F: the change in dementia at 80-90 as the SES tie (holding ability) sweeps from x0.4 to x1.5 per SD,
# with ability's tie as set (x0.81) or none (x1), and the band of ten worlds of different seeds (1-10) with ability as set.
# Prints the ends and the band at the setting (x0.87) and saves the plot.
# Run: python Buckner_etal_SuppFigure7PanelF_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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

SWEEP = r'''(() => {
  const run = state.run, p = run.p, w = run.agg.w26, Y = SY(), r0 = p.rSesAbility, P = [];   // the default world (Childhood mortality off)
  for (let r = 0; r < w.n; r++) if (w.age[r] >= 80 && w.age[r] <= 90)   // everyone alive in 2026 at 80-90, with the hazard of dying before 18
    P.push({ s: w.ses[r], a: w.abil[r], d: w.dem[r], f: w.fem[r], b: Y - w.age[r], H: -Math.log(1 - E.childQ(p, w.fem[r], Y - w.age[r]) / 100) });   // their birth year and sex carry
  // a tie per SD (SES holding ability, ability holding SES) as log coefficients, normalized to keep the mean hazard over births
  const coef = (sHR, aHR) => { const bs = Math.log(sHR), ba = Math.log(aHR); return { bs, ba, h: 0.5 * (bs * bs + ba * ba + 2 * r0 * bs * ba) }; };
  // the change childhood deaths make to dementia at 80-90 (points): the survivors, each weighted by their chance of reaching 18, minus everyone
  const change = (K, lvl = 1) => { let D = 0, WA = 0, DA = 0;
    for (const x of P) { const sv = Math.exp(-lvl * x.H * Math.exp(K.bs * x.s + K.ba * x.a - K.h)); D += x.d; WA += sv; DA += sv * x.d; }
    return 100 * (DA / WA - D / P.length); };
  const xs = Array.from({ length: 61 }, (_, i) => 0.4 * Math.pow(1.5 / 0.4, i / 60));
  (window.OUT = window.OUT || []).push({ seed: p.seed, xs, at: change(coef(p.chSesHR, p.chAbilHR)), set: xs.map((x) => change(coef(x, p.chAbilHR))), none: xs.map((x) => change(coef(x, 1))) });
  return window.OUT;
})()'''
steps = [SWEEP]
for seed in [1, 2, 3, 4, 5, 6, 8, 9, 10]: steps += [f'state.p.seed = {seed}; simulate(); 0', SWEEP]   # nine more worlds
O = run(*steps); xs = np.array(O[0]['xs']); band = np.array([o['set'] for o in O]); w7 = O[0]
at = [o['at'] for o in O]
print(f"ability as set: {w7['set'][0]:+.2f} points at x0.4, {w7['at']:+.2f} at x0.87 (as set), {w7['set'][-1]:+.2f} at x1.5; with no ability tie {w7['none'][0]:+.2f} to {w7['none'][-1]:+.2f}")
print(f'ten worlds at the setting: {min(at):+.2f} to {max(at):+.2f}')
plt.figure(figsize=(4, 2.8)); plt.fill_between(xs, band.min(0), band.max(0), color='#c98500', alpha=0.25, lw=0)
plt.plot(xs, w7['set'], color='#c98500', label='Ability x0.81'); plt.plot(xs, w7['none'], color='k', ls='--', label='No ability tie')
plt.xscale('log'); plt.axhline(0, color='k', lw=0.6); plt.xlabel('Childhood mortality per SD higher SES (x)'); plt.ylabel('Change (points)')
plt.legend(frameon=False); plt.tight_layout(); plt.savefig('Buckner_etal_SuppFigure7PanelF_261110.png', dpi=150)
```
