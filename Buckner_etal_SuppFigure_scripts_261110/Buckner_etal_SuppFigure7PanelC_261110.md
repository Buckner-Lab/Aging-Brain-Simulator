# Supplementary Figure 7, panel C: Deaths before 18, from records

```python
# Supplementary Figure 7C: mortality by 18 by year of birth (sexes averaged), the World's Mortality by age 18 curve (Social
# Security Area cohort life tables), split into the stage's four kinds by the share of deaths before 5 and external causes'
# share at each age. Prints the share for the births of 1936-46 (aged 80-90 in 2026) and saves the stacked plot.
# Run: python Buckner_etal_SuppFigure7PanelC_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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

JS = r'''(() => { const p = state.run.p;
  // the four kinds of death before 18 (the stage's data): the share before 5 (Social Security Area cohort life tables) and external causes'
  // share before 5 and at 5-17 (%; Children's Bureau 1939-41, NCHS 1960-2019), by birth year every 5 years from 1926, girls (w) and boys (m)
  const U5 = { w: [0.844, 0.856, 0.87, 0.884, 0.872, 0.857, 0.853, 0.849, 0.848, 0.844, 0.828, 0.808, 0.8, 0.789, 0.779, 0.767, 0.757, 0.747, 0.741, 0.735, 0.735],
    m: [0.835, 0.839, 0.846, 0.851, 0.833, 0.81, 0.804, 0.799, 0.798, 0.793, 0.768, 0.739, 0.74, 0.738, 0.725, 0.709, 0.694, 0.679, 0.671, 0.663, 0.663] };
  const EXT = { u5: { w: [6.1, 5.8, 5.4, 5.6, 6.4, 6.7, 7, 7.4, 7.9, 8.1, 8.6, 8.8, 8.9, 9.4, 9.8, 9.9, 10.1, 10.5, 11, 11.4, 11.4],
      m: [6.2, 6, 5.5, 5.7, 6.5, 6.8, 7.1, 7.6, 8.2, 8.6, 9.2, 9.5, 9.6, 10.1, 10.6, 11.1, 11.6, 12.1, 12.6, 13.1, 13.1] },
    o5: { w: [19.4, 23, 28.3, 34.4, 39.7, 44.4, 49.2, 53.4, 56.4, 57.9, 58, 57, 55.8, 54, 52.1, 51.3, 51.5, 51.8, 51.9, 51.9, 51.9],
      m: [39.1, 41.4, 45.8, 51.7, 56.5, 60.9, 65, 68.4, 70.5, 71.4, 70.6, 68.8, 67, 65.2, 64, 64.3, 64.8, 65.1, 65.2, 65.2, 65.2] } };
  const shares = (b, f) => { const x = f ? 'w' : 'm', at = (a) => Math.min(1, Math.max(0, E.curveAt(a, 1926, 5, b)));   // before 5 internal, external; 5-17 internal, external
    const u = at(U5[x]), e0 = at(EXT.u5[x].map((v) => v / 100)), e1 = at(EXT.o5[x].map((v) => v / 100)); return [u * (1 - e0), u * e0, (1 - u) * (1 - e1), (1 - u) * e1]; };
  const KIND = [['Before 5, internal', 0.94, 0.75, 0], ['Before 5, external', 0.77, 0.95, 1], ['5-17, internal', 0.96, 0.80, 0], ['5-17, external', 0.91, 0.78, 1]];   // ties per SD: SES, ability
  return Array.from({ length: 83 }, (_, j) => { const b = 1926 + j, out = [0, 0, 0, 0];
    for (const f of [0, 1]) { const q = E.childQ(p, f, b), s = shares(b, f); for (let k = 0; k < 4; k++) out[k] += 0.5 * q * s[k]; }
    return { b, kinds: out }; });   // % of births dying before 18, by kind
})()'''
R = run(JS); B = np.array([r['b'] for r in R]); S = np.array([r['kinds'] for r in R]).T
print(f'births of 1936-46: {S.sum(0)[(B >= 1936) & (B <= 1946)].mean():.1f}% died before 18; 1926: {S.sum(0)[0]:.1f}%, 2008: {S.sum(0)[-1]:.2f}%')
plt.figure(figsize=(4, 2.6)); plt.stackplot(B, S, labels=['Before 5, internal', 'Before 5, external', '5-17, internal', '5-17, external'],
  colors=['#c98500', '#f3d28c', '#2a78d6', '#a9c8f0']); plt.axvspan(1936, 1946, color='k', alpha=0.08)
plt.xlabel('Year of birth'); plt.ylabel('Died before 18 (%)'); plt.legend(frameon=False, fontsize=7); plt.tight_layout(); plt.savefig('Buckner_etal_SuppFigure7PanelC_261110.png', dpi=150)
```
