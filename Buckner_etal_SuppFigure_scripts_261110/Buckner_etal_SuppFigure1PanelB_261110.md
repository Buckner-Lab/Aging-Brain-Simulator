# Supplementary Figure 1, panel B: Reads itself

```python
# Supplementary Figure 1B: the file's first lines, which point any reader to the developer guide inside it, and the guide's
# sections; section 10 sets the rules for recording insights and puzzles. No browser needed.
# Run: python Buckner_etal_SuppFigure1PanelB_261110.py AgingBrain_Simulator_v102_261109.html   (needs: pip install numpy matplotlib)
import sys
from pathlib import Path
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
SIM = Path(sys.argv[1] if len(sys.argv) > 1 else 'AgingBrain_Simulator_v102_261109.html')

import re, html
s = SIM.read_text(encoding='utf8')
print(s[s.index('<!--'):s.index('-->') + 3])
g = s[s.index('<details class="sect detail" id="im-doc">'):s.index('<script data-ab>')]   # the guide, inside the Imagine page
heads = [html.unescape(re.sub('<[^>]+>', '', h)).strip() for h in re.findall(r'<h[3-6][^>]*>(\d+\..*?)</h[3-6]>', g)]
print(f'the guide has {len(heads)} sections:'); print('\n'.join(heads))
```
