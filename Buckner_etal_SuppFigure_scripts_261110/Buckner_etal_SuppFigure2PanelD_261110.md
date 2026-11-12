# Supplementary Figure 2, panel D: Ranking the determinants

```python
# Supplementary Figure 2D: each of the eleven baseline determinants' share of the variance they explain together (Shapley
# decomposition of R2) in global cognition at 40, 70 and 85, dementia by 90 (alive at 65) and age at death (alive at 40). The
# browser sums cross-products over every life; Python decomposes.
# Run: python Buckner_etal_SuppFigure2PanelD_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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

JS = r'''(() => { const run = state.run, p = run.p, k = run.k, z = new Float64Array(E.NZ), P = {}, NC = 15;
  const out = Object.fromEntries(['g40', 'g70', 'g85', 'dem90', 'death'].map((o) => [o, { n: 0, s: new Float64Array(NC), cp: new Float64Array(NC * NC) }]));
  const add = (o, x) => { const A = out[o]; A.n++; for (let i = 0; i < NC; i++) { A.s[i] += x[i]; for (let j = 0; j < NC; j++) A.cp[i * NC + j] += x[i] * x[j]; } };
  for (let i = 0; i < p.N; i++) {
    E.setup(i, p, k, z, P); const g = {}; let fD = 999;
    const death = E.live(P, p, k, (a, v, dem) => { if (a === 40 || a === 65 || a === 70 || a === 85) g[a] = (v[E.IX.mem] + v[E.IX.spd] + v[E.IX.exe]) / 3; if (dem && fD === 999) fD = a; });
    const c = (P.b - 1950) / 10, x = [c, c * c, P.female, P.n4, P.n4 === 2 ? 1 : 0, P.n2, P.prs, P.ses, P.abil, P.eduY, P.R, P.Q, P.sT, P.eT, 0];
    for (const a of [40, 70, 85]) if (a in g) { x[14] = g[a]; add('g' + a, x); }
    if (65 in g) { x[14] = fD <= 90 ? 1 : 0; add('dem90', x); }
    if (40 in g) { x[14] = death; add('death', x); }
  }
  return Object.fromEntries(Object.entries(out).map(([o, A]) => [o, { n: A.n, s: Array.from(A.s), cp: Array.from(A.cp) }])); })()'''
from itertools import combinations
from math import factorial
GROUPS = {'Birth year': [0, 1], 'Sex': [2], 'APOE': [3, 4, 5], 'Polygenic score': [6], 'SES': [7], 'Childhood ability': [8], 'Schooling': [9],
          'Resistance': [10], 'Resilience': [11], 'Sleep trait': [12], 'Engagement trait': [13]}
names = list(GROUPS); NG = len(names)
for o, A in run(JS).items():
    n = A['n']; m = np.array(A['s']) / n; C = np.array(A['cp']).reshape(15, 15) / n - np.outer(m, m)   # covariance of the 14 columns and the outcome
    cache = {}
    def r2(S):   # R2 of the outcome on the columns of the groups in S, from the covariance
        if S not in cache:
            cols = [c for j in S for c in GROUPS[names[j]]]
            cache[S] = 0.0 if not cols else float(C[14, cols] @ np.linalg.solve(C[np.ix_(cols, cols)], C[cols, 14]) / C[14, 14])
        return cache[S]
    phi = np.zeros(NG)
    for j in range(NG):
        rest = [i for i in range(NG) if i != j]
        for r in range(NG):
            wt = factorial(r) * factorial(NG - r - 1) / factorial(NG)
            for S in combinations(rest, r): phi[j] += wt * (r2(tuple(sorted(S + (j,)))) - r2(S))
    tot = r2(tuple(range(NG))); top = np.argsort(-phi)[:3]
    print(f"{o} ({n:,} lives): R2 {100 * tot:.0f}%; " + ', '.join(f'{names[j]} {100 * phi[j] / tot:.0f}%' for j in top))
```
