# Supplementary Figure 2, panel C: Birth year and ability

```python
# Supplementary Figure 2C: for women of average SES at ability -1, 0 and +1 SD, the expected years of schooling by year of birth
# and the level at 40: the cohort gain plus ability's direct part plus schooling's part. Prints the schooling gap between +1 and
# -1 SD and what one SD of ability and one decade of birth are worth at 40; saves the plot.
# Run: python Buckner_etal_SuppFigure2PanelC_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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
  const B = Array.from({ length: 83 }, (_, j) => 1926 + j), lvl = (a, b) => p.cohortCog * (b - 1950) / 10 + k.aCd * a + k.eduB * (school(a, 0, 1, b) - E.EDU_REF);
  return { B, yrs: [-1, 0, 1].map((a) => B.map((b) => school(a, 0, 1, b))), lvl: [-1, 0, 1].map((a) => B.map((b) => lvl(a, b))) }; })()'''
c = run(JS); B = np.array(c['B']); Y = np.array(c['yrs']); L = np.array(c['lvl'])
gap = Y[2] - Y[0]; per_dec = np.diff(L[1])[(B[:-1] >= 1926) & (B[:-1] < 2008)].mean() * 10
print(f'+1 rather than -1 SD: {gap.min():.1f} to {gap.max():.1f} more years of schooling across cohorts (mean {gap.mean():.1f})')
print(f'at 40, one SD of ability is worth {(L[2] - L[0]).mean() / 2:.2f} SD and a decade of birth {per_dec:.2f} SD (cohort gain plus schooling)')
fig, ax = plt.subplots(2, 1, figsize=(4, 4.4), sharex=True)
for j, (a, col) in enumerate(zip([-1, 0, 1], ['#e377c2', '0.5', '#2a78d6'])): ax[0].plot(B, Y[j], color=col, label=f'{a:+d} SD'); ax[1].plot(B, L[j], color=col)
ax[0].set_ylabel('Schooling (years)'); ax[1].set_ylabel('Level at 40 (SD)'); ax[1].set_xlabel('Year of birth'); ax[0].legend(frameon=False)
plt.tight_layout(); plt.savefig('Buckner_etal_SuppFigure2PanelC_261110.png', dpi=150)
```
