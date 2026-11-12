# Supplementary Figure 2, panel F: Where ability acts

```python
# Supplementary Figure 2F: the same woman, amyloid positive at 65, at +1 or -1 SD of ability through one path at a time (direct
# level at 40, schooling, reserve, engagement, brain) or all five. Prints how much of the gap in global cognition at 85 each
# path carries, when dementia comes, and the brain path's effect on the hippocampus at 85.
# Run: python Buckner_etal_SuppFigure2PanelF_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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
  return Object.fromEntries([['all', ALL], ...ALL.map((q) => [q, [q]])].map(([nm, on]) => [nm, { hi: life({ aOn: 65, ...path(1, on) }), lo: life({ aOn: 65, ...path(-1, on) }) }])); })()'''
c = run(JS); i85 = c['all']['hi']['age'].index(85)
for nm, d in c.items():
    print(f"{nm:<8} gap at 85 {d['hi']['g'][i85] - d['lo']['g'][i85]:.2f} SD in global cognition, {d['hi']['hip'][i85] - d['lo']['hip'][i85]:.2f} mL in the hippocampus; "
          f"dementia at {d['lo']['dem']} (-1 SD) and {d['hi']['dem']} (+1 SD)")
fig, ax = plt.subplots(figsize=(4, 2.6)); y = np.arange(len(c))[::-1]
ax.plot([d['hi']['g'][i85] for d in c.values()], y, 'ko'); ax.plot([d['lo']['g'][i85] for d in c.values()], y, 'o', mfc='none', color='k')
ax.set_yticks(y, list(c)); ax.set_xlabel('Global cognition at 85 (SD)'); plt.tight_layout(); plt.savefig('Buckner_etal_SuppFigure2PanelF_261110.png', dpi=150)
```
