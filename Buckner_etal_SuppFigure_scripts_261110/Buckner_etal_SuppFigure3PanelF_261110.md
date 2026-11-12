# Supplementary Figure 3, panel F: Where each trait acts

```python
# Supplementary Figure 3F: what the cascade has taken by 90 from the reference person's hippocampus and episodic memory (amyloid
# positive at 65 minus never), with one trait at +1 or -1 SD (resistance R, resilience Q, reserve), two e4 alleles, or as a man.
# Prints the table and saves the plot.
# Run: python Buckner_etal_SuppFigure3PanelF_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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
  const at90 = (over) => { const on = life({ aOn: 65, ...over }), off = life({ aOn: 999, ...over }), i = on.age.indexOf(90);
    return { hip: off.hip[i] - on.hip[i], mem: off.mem[i] - on.mem[i] }; };
  return Object.fromEntries([['Reference woman', {}], ['Resistance +1', { R: 1 }], ['Resistance -1', { R: -1 }], ['Resilience +1', { Q: 1 }], ['Resilience -1', { Q: -1 }],
    ['Reserve +1', { crz: 1 }], ['Reserve -1', { crz: -1 }], ['Two e4 alleles', { n4: 2 }], ['Man', { female: 0 }]].map(([k, o]) => [k, at90(o)])); })()'''
c = run(JS)
for k, v in c.items(): print(f"{k:<16} hippocampus {v['hip']:.2f} mL, episodic memory {v['mem']:.2f} SD taken by 90")
fig, ax = plt.subplots(1, 2, figsize=(7, 2.8), sharey=True); y = np.arange(len(c))[::-1]
for a, m, lab in zip(ax, ['hip', 'mem'], ['Hippocampus taken by 90 (mL)', 'Memory taken by 90 (SD)']):
    a.plot([v[m] for v in c.values()], y, 'ko'); a.axvline(c['Reference woman'][m], color='k', ls='--', lw=0.8); a.set_xlabel(lab)
ax[0].set_yticks(y, list(c)); plt.tight_layout(); plt.savefig('Buckner_etal_SuppFigure3PanelF_261110.png', dpi=150)
```
