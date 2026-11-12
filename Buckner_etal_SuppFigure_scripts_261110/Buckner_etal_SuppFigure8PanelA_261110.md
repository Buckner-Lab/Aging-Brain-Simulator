# Supplementary Figure 8, panel A: Consequential prompts

```python
# Supplementary Figure 8 (one table, filed as panel A): its prompts and interpretations come from the development conversations,
# not the file. This prints the file's version-history line for each version in the table (side builds v96_M&S and v101_MT by
# their parent versions). No browser needed.
# Run: python Buckner_etal_SuppFigure8PanelA_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install numpy matplotlib)
import sys
from pathlib import Path
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
SIM = Path(sys.argv[1] if len(sys.argv) > 1 else 'AgingBrain_Simulator_v102_261109.html')

import re, html
s = SIM.read_text(encoding='utf8')
H = {v: (d, html.unescape(re.sub(r'<[^>]+>', ' ', t)).split()) for d, v, t in
     re.findall(r'<li class="vh[^"]*"><span class="vh-d">([^<]*)</span><span class="vh-v">([^<]*)</span><span class="vh-t">(.*?)</li>', s)}
for row in ['v1', 'v15', 'v31', 'v32', 'v63', 'v65', 'v75', 'v76', 'v83', 'v89', 'v96', 'v99', 'v100', 'v101']:
    d, t = H.get(row, ('', ['(not in the history)']))
    print(f"{row:<5} {d:<9} {' '.join(t)[:160]}")
```
