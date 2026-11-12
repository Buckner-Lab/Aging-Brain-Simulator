# Supplementary Figure 7, panel H: If more children had died

```python
# Supplementary Figure 7H: the change in dementia at 80-90 as the level of childhood mortality goes from none to six times the
# records, with the ties as set, both at x0.6, or none. Prints the change at the records and where a third of the births of
# 1936-46 (aged 80-90 in 2026) would have died before 18, and saves the plot.
# Run: python Buckner_etal_SuppFigure7PanelH_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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
  const lv = Array.from({ length: 25 }, (_, i) => 0.25 * i);   // the level: times the records; died: the share of the births of 1936-46 (sexes averaged)
  const died = (lvl) => { let t = 0; for (let b = 1936; b <= 1946; b++) for (const f of [0, 1]) t += 1 - Math.pow(1 - E.childQ(p, f, b) / 100, lvl); return 100 * t / 22; };
  return { lv, died: lv.map(died), set: lv.map((l) => change(coef(p.chSesHR, p.chAbilHR), l)), strong: lv.map((l) => change(coef(0.6, 0.6), l)), none: lv.map((l) => change(coef(1, 1), l)) };
})()'''
c = run(JS); died = np.array(c['died'])
print(f"at the records ({died[4]:.1f}% died): {c['set'][4]:+.2f} points as set, {c['strong'][4]:+.2f} with both at x0.6, {c['none'][4]:+.2f} with none")
for k in ('set', 'strong'): print(f"had a third died before 18: {np.interp(100 / 3, died, c[k]):+.2f} points ({k})")
plt.figure(figsize=(4, 2.8))
for k, col, ls in (('set', '#c98500', '-'), ('strong', '#c23b3b', '-'), ('none', 'k', '--')): plt.plot(died, c[k], color=col, ls=ls, label=k)
plt.xlabel('Died before 18 (%)'); plt.ylabel('Change (points)'); plt.legend(frameon=False); plt.tight_layout(); plt.savefig('Buckner_etal_SuppFigure7PanelH_261110.png', dpi=150)
```
