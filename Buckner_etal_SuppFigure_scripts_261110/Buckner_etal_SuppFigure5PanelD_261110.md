# Supplementary Figure 5, panel D: Compare definitions

```python
# Supplementary Figure 5D: Compare definitions applies three Selection strategies as set: SuperAgers, maintainers (Josefsson's
# rule from version 102) and the resilient. Prints how far each group's memory exceeds everyone alive at its ages (in their SD)
# and its 10-year dementia against dementia-free peers, with the app's own functions.
# Run: python Buckner_etal_SuppFigure5PanelD_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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

JS = r'''(() => { const w = state.run.agg.w26, run = state.run, out = {};
  const peer = {}; for (let r = 0; r < w.n; r++) { const a = w.age[r]; (peer[a] = peer[a] || []).push(r); }   // everyone alive at each age
  const memAt = Object.fromEntries(Object.entries(peer).map(([a, rows]) => { const x = rows.map((r) => wv(w, r, 'mem')), m = x.reduce((s, v) => s + v, 0) / x.length;
    return [a, { m, sd: Math.sqrt(x.reduce((s, v) => s + (v - m) ** 2, 0) / (x.length - 1)) }]; }));
  const dem10 = (rows) => rows.filter((r) => { const t = E.trace(w.id[r], run.p, run.k, run.S.saRef); return t.demAge <= w.age[r] + 10; }).length / rows.length;
  for (const id of ['super', 'maint', 'resil']) {
    state.sel.strat = id; const R = runSelection(), sel = R.sel;
    const peers = R.world.filter((r) => !w.dem[r]).filter((_, i) => i % 10 === 0);   // a tenth of the dementia-free at the same ages
    out[SEL_BY[id].title] = { n: sel.length, ages: [R.lo, R.hi], above: sel.reduce((s, r) => s + (wv(w, r, 'mem') - memAt[w.age[r]].m) / memAt[w.age[r]].sd, 0) / sel.length, dem: dem10(sel), peers: dem10(peers) };
  }
  return out; })()'''
for k, v in run(JS).items():
    print(f"{k} ({v['n']}, ages {v['ages'][0]}-{v['ages'][1]}): memory {v['above']:+.2f} SD above everyone alive at their ages (in their SD); "
          f"dementia within 10 years {100 * v['dem']:.0f}% (dementia-free peers {100 * v['peers']:.0f}%)")
```
