# Supplementary Figure 3, panel E: After amyloid positivity

```python
# Supplementary Figure 3E: everyone in the default world who turned amyloid positive at 60-69 or 75-84, followed by years since:
# amyloid positive only, tau positive, with dementia (any cause) or dead. Prints the group sizes and the shares who ever become
# tau positive, develop dementia and die without dementia; saves the stacked plot. Lives every life again (about 20 s).
# Run: python Buckner_etal_SuppFigure3PanelE_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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
  const run = state.run, p = run.p, k = run.k, z = new Float64Array(E.NZ), P = {}, out = [];   // every life of the default world, lived again
  for (let i = 0; i < p.N; i++) {                                                                  // year by year from its fixed draws
    E.setup(i, p, k, z, P); let fA = 999, fT = 999, fD = 999;
    const death = E.live(P, p, k, (a, v, dem) => { if (fA === 999 && v[E.IX.amy] >= E.A_POS) fA = a; if (fT === 999 && v[E.IX.tau] >= E.T_POS) fT = a; if (fD === 999 && dem) fD = a; });
    out.push([P.n4, P.aOn, fA, fT, fD, death]);   // e4 alleles, amyloid onset if they lived, first ages amyloid+ / tau+ / dementia while alive, death
  }
  return out;
})()'''
W = np.array(run(JS), float); fA, fT, fD, death = W[:, 2], W[:, 3], W[:, 4], W[:, 5]
fig, ax = plt.subplots(1, 2, figsize=(7, 2.6), sharey=True); t = np.arange(0, 31)
for a, (lo, hi) in zip(ax, [(60, 69), (75, 84)]):
    g = (fA >= lo) & (fA <= hi); a0, T, Dm, Dt = fA[g], fT[g], fD[g], death[g]
    print(f'positive at {lo}-{hi}: {g.sum()} lives; {100 * (T < 999).mean():.0f}% become tau positive, {100 * (Dm < 999).mean():.0f}% develop dementia, '
          f'{100 * (Dm == 999).mean():.0f}% die without dementia')
    dead = np.array([(Dt <= a0 + y).mean() for y in t]); dem = np.array([((Dm <= a0 + y) & (Dt > a0 + y)).mean() for y in t])
    tau = np.array([((T <= a0 + y) & (Dm > a0 + y) & (Dt > a0 + y)).mean() for y in t])
    a.stackplot(t, 1 - dead - dem - tau, tau, dem, dead, colors=['#f3d28c', '#c98500', '#c23b3b', '#8a877f'], labels=['Amyloid+ only', 'Tau+', 'Dementia', 'Died'])
    a.set_title(f'Positive at {lo}-{hi}'); a.set_xlabel('Years since amyloid positivity')
ax[0].set_ylabel('Share'); ax[1].legend(frameon=False, fontsize=7); plt.tight_layout(); plt.savefig('Buckner_etal_SuppFigure3PanelE_261110.png', dpi=150)
```
