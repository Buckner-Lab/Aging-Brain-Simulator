# Supplementary Figure 1, panel D: Saves and copies itself

```python
# Supplementary Figure 1D: every setting is saved as a versioned file (keepSnapshot; the format's version, KEEP_V) that later
# versions can load, and "Download this version of the html application" saves a copy of the page itself (PAGE_SRC). Prints an
# excerpt of the saved settings and the size of the copy, and writes the settings file.
# Run: python Buckner_etal_SuppFigure1PanelD_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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

import json
c = run("({ v: KEEP_V, snap: keepSnapshot(), copy: PAGE_SRC.length })")
snap = c['snap']; Path('Buckner_etal_SuppFigure1PanelD_settings_261110.json').write_text(json.dumps(snap, indent=1), encoding='utf8')
print(f"settings file format version {c['v']}; sections: {', '.join(snap)}")
print('\n'.join(json.dumps(snap, indent=1).split('\n')[:12]) + '\n ...')
print(f"Download this version of the html application saves a copy of {c['copy']:,} characters")
```
