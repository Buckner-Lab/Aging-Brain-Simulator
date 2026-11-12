# Supplementary Figure 7, panel E: Who is missing at 80-90

```python
# Supplementary Figure 7E: as set (the World's Childhood mortality: SES x0.87, ability x0.81 per SD), the share of people at
# 80-90 in the world without childhood deaths who would have died as children, their dementia against the survivors', how they
# differ in SES and ability, and the change: -f x (dementia among the missing - among the survivors), with its 95% CI.
# Run: python Buckner_etal_SuppFigure7PanelE_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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
  const K = coef(p.chSesHR, p.chAbilHR), sv = P.map((x) => Math.exp(-x.H * Math.exp(K.bs * x.s + K.ba * x.a - K.h)));
  const g = (wt) => { let W = 0, d = 0, s = 0, a = 0; P.forEach((x, i) => { const v = wt(i); W += v; d += v * x.d; s += v * x.s; a += v * x.a; }); return { W, d: d / W, s: s / W, a: a / W }; };
  const B = g(() => 1), A = g((i) => sv[i]), M = g((i) => 1 - sv[i]);   // everyone, the survivors, the missing
  let v = 0; P.forEach((x, i) => { const gA = sv[i] * (x.d - A.d) / A.W, gB = (x.d - B.d) / B.W; v += (gA - gB) ** 2; });   // each person a draw
  return { n: P.length, B, A, M, se: Math.sqrt(v) };
})()'''
c = run(JS); f = c['M']['W'] / c['B']['W']; dl = 100 * (c['A']['d'] - c['B']['d']); se = 100 * c['se']
print(f"{c['n']} people at 80-90; {100 * f:.1f}% would have died as children; dementia {100 * c['M']['d']:.1f}% among them, {100 * c['A']['d']:.1f}% among the survivors")
print(f"the missing are lower in ability by {c['A']['a'] - c['M']['a']:.2f} SD and in SES by {c['A']['s'] - c['M']['s']:.2f} SD")
print(f"change {dl:.2f} points (95% CI {dl - 1.96 * se:.2f} to {dl + 1.96 * se:.2f}): {100 * c['A']['d']:.2f}% rather than {100 * c['B']['d']:.2f}%")
plt.figure(figsize=(3.4, 2.6)); plt.bar(['Survivors', 'Missing'], [100 * c['A']['d'], 100 * c['M']['d']], width=[0.6, 0.6 * f / 0.2], color=['#8a877f', '#c98500'])
plt.ylabel('Dementia at 80-90 (%)'); plt.tight_layout(); plt.savefig('Buckner_etal_SuppFigure7PanelE_261110.png', dpi=150)
```
