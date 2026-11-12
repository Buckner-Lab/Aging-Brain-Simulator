# Supplementary Figure 7, panel B: Two worlds, the same births

```python
# Supplementary Figure 7B: the two worlds the stage compares, made of the same births. Everyone alive in 2026 at 80-90 in the
# default world (no childhood deaths) counts once there and, in the world with childhood deaths, by their chance of reaching 18
# as the World's Childhood mortality sets it; nothing is simulated again. Prints both worlds' numbers and dementia.
# Run: python Buckner_etal_SuppFigure7PanelB_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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
  const K = coef(p.chSesHR, p.chAbilHR); let A = 0, DA = 0, D = 0;
  for (const x of P) { const sv = Math.exp(-x.H * Math.exp(K.bs * x.s + K.ba * x.a - K.h)); A += sv; DA += sv * x.d; D += x.d; }
  return { n: P.length, dem: D, survivors: A, demSurvivors: DA };
})()'''
c = run(JS)
print(f"world without childhood deaths: {c['n']} people at 80-90 in 2026, {100 * c['dem'] / c['n']:.2f}% with dementia")
print(f"world with them: {c['survivors']:.1f} survivors of the same births, {100 * c['demSurvivors'] / c['survivors']:.2f}% with dementia; "
      f"{c['n'] - c['survivors']:.1f} would have died before 18")
plt.figure(figsize=(3.6, 2.6)); plt.bar(['Without childhood deaths', 'With them'], [c['n'], c['survivors']], color=['#dcdad3', '#8a877f'])
plt.bar(['Without childhood deaths', 'With them'], [c['dem'], c['demSurvivors']], color='#c23b3b', label='With dementia')
plt.ylabel('People at 80-90'); plt.legend(frameon=False); plt.tight_layout(); plt.savefig('Buckner_etal_SuppFigure7PanelB_261110.png', dpi=150)
```
