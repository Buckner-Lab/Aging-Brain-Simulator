# Supplementary Figure 3, panel A: The AD cascade as implemented

```python
# Supplementary Figure 3A: the AD cascade's links as the engine sets them (E.DEFAULTS), in the legend's order, and its anchor
# checked in the world: 24% amyloid positive by 70 is set for an e3/e3 carrier of average traits; the script also counts it
# across the world's e3/e3 carriers.
# Run: python Buckner_etal_SuppFigure3PanelA_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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

JS = r'''(() => { const run = state.run, p = run.p, k = run.k, z = new Float64Array(E.NZ), P = {}; let n = 0, by70 = 0;
  for (let i = 0; i < p.N; i++) { E.setup(i, p, k, z, P); if (P.n4 === 0 && P.n2 === 0) { n++; if (P.aOn <= 70) by70++; } }
  return { p, e33: n, by70 }; })()'''
c = run(JS); p = c['p']
for label, keys in [('amyloid onset: share of e3/e3 positive by 70 (%), doubling of risk (years), from age', ['aPos70', 'amyDbl', 'amyFrom']),
                    ('  x per e4 allele, two alleles, per e2 allele, per SD polygenic, per SD poor sleep', ['e4HR', 'e44HR', 'e2HR', 'prsHR', 'sleepAmy']),
                    ('  resistance R: e^(-x R), with x =', ['resistSD']),
                    ('amyloid PET S-curve: rate, shape, rise above baseline (CL), baseline mean and SD', ['amyK', 'amyNu', 'amyMax', 'amyBase', 'amyBaseSD']),
                    ('AD tau: lag to positivity (years), rate, x per e4, x in women, rise (SUVR), resistance on rate e^(-0.2R)', ['lag', 'tauK', 'tauE4', 'tauFem', 'tauMax']),
                    ('  baseline SUVR mean and SD, age-related tau a year from 50 and its log SD', ['tauBase', 'tauBaseSD', 'partRate', 'partSD']),
                    ('pTau217: baseline (pg/mL), x at full plaque, plaque scale (CL), x at full tau', ['ptauBase', 'pAmyX', 'pAmyK', 'pTauX']),
                    ('atrophy per SUVR (% a year): hippocampus, cortex, whole brain; plaque terms', ['tauHipp', 'tauCtx', 'tauWB', 'amyHipp', 'amyCtx', 'amyWB']),
                    ('cognition per SUVR-year: memory, executive, speed; cap of tau-years', ['tauMem', 'tauExe', 'tauSpd', 'cogCap']),
                    ('resilience Q (e^(-x Q - x^2/2)), reserve (% less cognitive toll per SD)', ['resilSD', 'buffer']),
                    ('dementia: global cognition at or below, after a fall since 40 of', ['demThresh', 'demDecline']),
                    ('other chains: sleep disruption per SUVR, x LATE risk, x lesion risk', ['sleepAD', 'lateAD', 'amyWMH'])]:
    print(label + ': ' + ', '.join(f'{p[k]:g}' for k in keys))
print(f"check: the 24% is set for an e3/e3 carrier of average traits; across the world's {c['e33']} e3/e3 carriers, with their genes and traits, "
      f"{100 * c['by70'] / c['e33']:.1f}% have amyloid onset by 70 if they lived")
```
