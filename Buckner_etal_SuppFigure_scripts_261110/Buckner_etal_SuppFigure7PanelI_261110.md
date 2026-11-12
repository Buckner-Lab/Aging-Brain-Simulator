# Supplementary Figure 7, panel I: Four kinds of death

```python
# Supplementary Figure 7I: the same mortality split into four kinds (before 5 or at 5-17; internal or external causes), each
# with its own ties to SES and ability. Prints each kind's share of the deaths and its part of the change, which add up to the
# whole, against the one kind's change.
# Run: python Buckner_etal_SuppFigure7PanelI_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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
  const run = state.run, p = run.p, w = run.agg.w26, Y = SY(), r0 = p.rSesAbility, P = [];   // the default world (Childhood mortality off)
  for (let r = 0; r < w.n; r++) if (w.age[r] >= 80 && w.age[r] <= 90)   // everyone alive in 2026 at 80-90, with the hazard of dying before 18
    P.push({ s: w.ses[r], a: w.abil[r], d: w.dem[r], f: w.fem[r], b: Y - w.age[r], H: -Math.log(1 - E.childQ(p, w.fem[r], Y - w.age[r]) / 100) });   // their birth year and sex carry
  // a tie per SD (SES holding ability, ability holding SES) as log coefficients, normalized to keep the mean hazard over births
  const coef = (sHR, aHR) => { const bs = Math.log(sHR), ba = Math.log(aHR); return { bs, ba, h: 0.5 * (bs * bs + ba * ba + 2 * r0 * bs * ba) }; };
  // the change childhood deaths make to dementia at 80-90 (points): the survivors, each weighted by their chance of reaching 18, minus everyone
  const change = (K, lvl = 1) => { let D = 0, WA = 0, DA = 0;
    for (const x of P) { const sv = Math.exp(-lvl * x.H * Math.exp(K.bs * x.s + K.ba * x.a - K.h)); D += x.d; WA += sv; DA += sv * x.d; }
    return 100 * (DA / WA - D / P.length); };
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
  const KS = KIND.map(([, s, a]) => coef(s, a)), n = P.length;
  let WA = 0, DA = 0, D = 0; const W = [0, 0, 0, 0], Dk = [0, 0, 0, 0];
  for (const x of P) { const sh = shares(x.b, x.f), hk = KS.map((K, j) => x.H * sh[j] * Math.exp(K.bs * x.s + K.ba * x.a - K.h)), h = hk.reduce((a, b) => a + b, 0), sv = Math.exp(-h);
    WA += sv; DA += sv * x.d; D += x.d; hk.forEach((v, j) => { const m = h > 0 ? (1 - sv) * v / h : 0; W[j] += m; Dk[j] += m * x.d; }); }   // each death split by kind
  const pa = DA / WA;
  return { one: change(coef(p.chSesHR, p.chAbilHR)), all: 100 * (pa - D / n), kinds: KIND.map(([k], j) => ({ k, share: W[j] / W.reduce((a, b) => a + b, 0), part: -100 * (W[j] / n) * (Dk[j] / W[j] - pa) })) };
})()'''
c = run(JS)
for k in c['kinds']: print(f"{k['k']:<20} {100 * k['share']:.0f}% of the deaths, part of the change {k['part']:+.3f} points ({100 * k['part'] / c['all']:.0f}%)")
print(f"four kinds together {c['all']:+.2f} points (sum of parts {sum(k['part'] for k in c['kinds']):+.2f}); one kind {c['one']:+.2f}")
plt.figure(figsize=(4, 2.4)); names = [k['k'] for k in c['kinds']]
plt.barh(names, [k['part'] for k in c['kinds']], color=['#c98500', '#f3d28c', '#2a78d6', '#a9c8f0']); plt.gca().invert_yaxis()
plt.xlabel('Part of the change (points)'); plt.tight_layout(); plt.savefig('Buckner_etal_SuppFigure7PanelI_261110.png', dpi=150)
```
