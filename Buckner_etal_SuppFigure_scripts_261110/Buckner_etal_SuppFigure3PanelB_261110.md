# Supplementary Figure 3, panel B: One life, amyloid positive at 65

```python
# Supplementary Figure 3B: the engine's reference person (a woman born in 1950, APOE e3/e3, average traits and draws, no
# vascular risk or LATE) amyloid positive at 65 or never. Prints when tau PET turns positive (1.30 SUVR), MCI (CDR-SB 0.5) and
# dementia (CDR-SB 3, the diagnosis) come with and without the cascade, and what the cascade has taken by 90; saves the plot.
# Run: python Buckner_etal_SuppFigure3PanelB_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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
  const p = state.run.p, K = ['amy', 'ptau', 'tau', 'hip', 'mem', 'cdr'];   // the engine's reference person: a woman born in 1950, APOE e3/e3,
  const life = (over) => { const o = E.prototype(p, over, 100, 40);           // average traits and draws, no vascular risk or LATE; aOn: amyloid positive at
    return { age: o.age, ...Object.fromEntries(K.map((k) => [k, o.v.map((v) => v[E.IX[k]])])) }; };   // that age (999: never). From 40 to 100
  return { on: life({ aOn: 65 }), off: life({ aOn: 999 }) }; })()'''
c = run(JS); age = np.array(c['on']['age'])
first = lambda x, thr: next((a for a, v in zip(age, x) if v >= thr), None)
for w in ('on', 'off'): L = c[w]; print(f"{'amyloid positive at 65' if w == 'on' else 'never'}: tau positive at {first(L['tau'], 1.30)}, "
                                        f"CDR-SB 0.5 at {first(L['cdr'], 0.5)}, dementia at {first(L['cdr'], 3)}")
i90 = list(age).index(90)
print(f"by 90 the cascade has taken {c['off']['hip'][i90] - c['on']['hip'][i90]:.2f} mL of hippocampus and {c['off']['mem'][i90] - c['on']['mem'][i90]:.2f} SD of episodic memory")
fig, ax = plt.subplots(1, 3, figsize=(8, 2.6))
for a, k, lab in zip(ax, ['tau', 'hip', 'mem'], ['Tau PET (SUVR)', 'Hippocampus (mL)', 'Episodic memory (SD)']):
    a.plot(age, c['on'][k], 'k'); a.plot(age, c['off'][k], 'k--'); a.fill_between(age, c['on'][k], c['off'][k], color='#c98500', alpha=0.3); a.set_xlabel('Age'); a.set_ylabel(lab)
plt.tight_layout(); plt.savefig('Buckner_etal_SuppFigure3PanelB_261110.png', dpi=150)
```
