# Supplementary Figure 2, panel E: One life by ability

```python
# Supplementary Figure 2E: the reference woman (born 1950, APOE e3/e3, average SES and traits) at ability -1, 0 and +1 SD with
# all five of ability's paths, amyloid positive at 65 or never. Prints where global cognition starts at 40 and when dementia
# begins (CDR-SB 3) with and without the cascade; saves the plot.
# Run: python Buckner_etal_SuppFigure2PanelE_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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
  const run = state.run, p = run.p, k = run.k;
  const Phi = (x) => { const t = 1 / (1 + 0.3275911 * Math.abs(x) / Math.SQRT2), y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x / 2); return x >= 0 ? 0.5 * (1 + y) : 0.5 * (1 - y); };
  // expected years of schooling: a propensity eS*SES + eA*ability + eduRes*e is cut where the census shares fall for the birth year and sex
  const school = (a, s, f, b) => { const t = ((f ? 0 : 1) * k.eduNB + Math.max(0, Math.min(k.eduNB - 1, b - p.birthMin))) * 3, mu = k.eS * s + k.eA * a;
    const c = [0, 1, 2].map((j) => Phi((k.eduT[t + j] - mu) / k.eduRes)); return [c[0], c[1] - c[0], c[2] - c[1], 1 - c[2]].reduce((y, q, j) => y + q * E.EDU.years[j], 0); };
  // a copy of the engine whose reference person can take ability's tie to hippocampal loss (version 102 holds hers at the mean)
  const EX = new Function(document.querySelector('script[data-ab]').textContent.replace('P.hipRate = k.agingOn * p.hipLoss;', 'P.hipRate = k.agingOn * p.hipLoss - (ov.hipAdj || 0);') + '; return ENGINE;')();
  // ability a's five paths in the reference woman (born 1950, SES 0, everything else average), relative to her at a = 0
  const e0 = school(0, 0, 1, 1950), path = (a, on) => { const o = { lvl: 0 };
    if (on.includes('direct')) o.lvl += k.aCd * a;                                   // the level at 40, directly
    if (on.includes('school')) o.lvl += k.eduB * (school(a, 0, 1, 1950) - e0);       // the level at 40, through the schooling it brings
    if (on.includes('reserve')) o.crz = k.aC * a / k.crNorm;                          // reserve, (aC ability + sC SES) / its SD
    if (on.includes('engage')) o.eT = p.engAbil * a;                                  // the engagement trait
    if (on.includes('brain')) { const zh = p.hipAbil * a; o.hipAdj = k.agingOn * p.hipLossSD * zh; o.ctx0 = p.ctxMean + p.ctxSD * p.ctxHipR * zh; }   // brain from 20
    return o; };
  const ALL = ['direct', 'school', 'reserve', 'engage', 'brain'];
  const life = (over) => { const o = EX.prototype(p, over, 100, 40), g = o.v.map((v) => (v[E.IX.mem] + v[E.IX.spd] + v[E.IX.exe]) / 3), cdr = o.v.map((v) => v[E.IX.cdr]);
    const d = cdr.findIndex((c) => c >= 3); return { age: o.age, g, hip: o.v.map((v) => v[E.IX.hip]), dem: d < 0 ? null : o.age[d] }; };   // dementia: CDR-SB 3
  return Object.fromEntries([-1, 0, 1].flatMap((a) => [65, 999].map((aOn) => [`${a} ${aOn}`, life({ aOn, ...path(a, ALL) })]))); })()'''
c = run(JS); plt.figure(figsize=(4, 2.8))
for a, col in zip([-1, 0, 1], ['#e377c2', '0.5', '#2a78d6']):
    on, off = c[f'{a} 65'], c[f'{a} 999']
    print(f"ability {a:+d} SD: global cognition at 40 {on['g'][0] - c['0 65']['g'][0]:+.2f} SD from the reference woman's; "
          f"dementia at {on['dem']} with the cascade, {off['dem'] or 'not by 100'} without")
    plt.plot(on['age'], on['g'], color=col, label=f'{a:+d} SD'); plt.plot(off['age'], off['g'], color=col, ls='--')
plt.axhline(-2.3, color='k', ls=':', lw=0.8); plt.xlabel('Age'); plt.ylabel('Global cognition (SD)'); plt.legend(frameon=False); plt.tight_layout(); plt.savefig('Buckner_etal_SuppFigure2PanelE_261110.png', dpi=150)
```
