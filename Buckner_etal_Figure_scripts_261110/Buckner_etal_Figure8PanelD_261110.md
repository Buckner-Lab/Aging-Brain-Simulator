# Buckner et al., Figure 8D: milestones from version 1 to version 76

Simulator: `AgingBrain_Simulator_261023.html` (version 99)
Run: `node run_panel_261110.mjs Buckner_etal_Figure8PanelD_261110.md`
The milestones are entries of the version history kept inside the file (World → AgingBrain Simulator version history); the icons are the stages'.
The script lists those entries with their dates.

```js
const keep = [1, 33, 35, 41, 52, 59, 61, 63, 75, 76];
const all = [...document.querySelectorAll('#wp-versions li.vh')].map((li) => ({ version: li.querySelector('.vh-v').textContent, date: li.querySelector('.vh-d').textContent,
  entry: (li.querySelector('.vh-t b') || li.querySelector('.vh-t')).textContent.trim() }));
return { versions_recorded: all.length, milestones: all.filter((r) => keep.includes(+r.version.slice(1))).reverse() };
```
