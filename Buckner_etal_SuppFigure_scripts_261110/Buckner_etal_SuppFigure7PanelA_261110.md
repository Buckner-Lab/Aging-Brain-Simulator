# Supplementary Figure 7, panel A: Built from one prompt

```python
# Supplementary Figure 7A: the prompt for the Childhood mortality worlds stage as Imagine's Copy prompt gives it in version 102:
# the opening every example shares, then the example. The build in the figure (v101_CMW, on version 101) kept its prompt word
# for word in the stage's banner.
# Run: python Buckner_etal_SuppFigure7PanelA_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install playwright numpy matplotlib; playwright install chromium)
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

print(run("IM_PRE + '\\n\\n' + IM_PROMPTS.find((x) => x.t === 'Childhood mortality worlds').p"))
```
