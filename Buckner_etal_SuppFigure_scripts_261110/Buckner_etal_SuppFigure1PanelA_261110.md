# Supplementary Figure 1, panel A: Everything in one file

```python
# Supplementary Figure 1A: the file's bytes in order, assigned to roles by landmarks (the two scripts, the pages' markup, the
# app's section comments): the engine, study stages, explaining and checking (guide, model text, checks, history, insights),
# saving and extending, and display. The figure mapped an earlier, smaller version. No browser needed.
# Run: python Buckner_etal_SuppFigure1PanelA_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install numpy matplotlib)
import sys
from pathlib import Path
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
SIM = Path(sys.argv[1] if len(sys.argv) > 1 else 'AgingBrain_Simulator_v102_261109.html')

s = SIM.read_text(encoding='utf8'); B = lambda i: len(s[:i].encode('utf8'))
e0 = s.index('<script data-ab>'); e1 = s.index('</script>', e0) + 9; a0 = s.index('<script data-ab>', e1)
app = lambda t: s.index('/* ---------------- ' + t, a0)
g0 = s.index('<details class="sect detail" id="im-doc">'); g1 = g0; depth = 0   # the developer guide: its whole <details> element
for m in __import__('re').finditer(r'<(/?)details\b', s[g0:]):
    depth += -1 if m.group(1) else 1
    if depth == 0: g1 = g0 + m.end() + 1; break
cuts = [(0, 'shows'), (s.index('<details class="sect wp-sub" id="wp-model"'), 'explains'),   # World page; its model text, checks, history, insights
        (s.index('id="panel-enroll"'), 'studies'), (s.index('id="panel-imagine"'), 'extends'), (g0, 'explains'), (g1, 'extends'),   # stage pages; Imagine, with the guide
        (e0, 'simulates'), (e1, 'shows'), (app('the properties of this simulated world'), 'explains'), (app('enrollment'), 'studies'),   # the engine; the app
        (app('save and load'), 'extends'), (s.rindex('/* ---------------- stages ---------------- */'), 'shows')]
cuts = sorted(set(cuts)); seg = [(B(i), B(j) if j else len(s.encode('utf8')), r) for (i, r), (j, _) in zip(cuts, cuts[1:] + [(None, None)])]
tot = len(s.encode('utf8')); kb = {}
for i, j, r in seg: kb[r] = kb.get(r, 0) + (j - i)
print(f'{tot:,} bytes: ' + ', '.join(f'{r} {v / 1000:.0f} KB ({100 * v / tot:.0f}%)' for r, v in kb.items()))
col = {'simulates': 'k', 'studies': '#2a78d6', 'explains': '#d9622e', 'extends': '#1baf7a', 'shows': '0.7'}
plt.figure(figsize=(6, 1.2))
for i, j, r in seg: plt.barh(0, j - i, left=i, color=col[r], height=0.6)
plt.yticks([]); plt.xlabel('Bytes, in order'); plt.tight_layout(); plt.savefig('Buckner_etal_SuppFigure1PanelA_261110.png', dpi=150)
```
