# AgingBrain Simulator

Every published version of the AgingBrain Simulator, from version 1 to version 103, together with the scripts that reproduce each panel of
the paper's figures and supplementary figures.

> Buckner RL, …, Nyberg L. *Synthesizing and Predicting Brain and Cognitive Aging Data Patterns Using an Evolving Simulator Enabled by
> Agentic Artificial Intelligence.* bioRxiv (forthcoming).

The simulator generates worlds of 120,000 individual lives. Each life starts from baseline parameters (genetic risk, birth year, childhood
ability, …) and changes with age through explicit causal cascades (aging, cardiovascular, the AD cascade, sleep, engagement, LATE). The
simulator then runs studies on those worlds through selection, measurement, follow-up and intervention stages. Each version is a single,
self-contained HTML file. Nothing needs to be installed.

**Open the simulators:** download or clone this repository and open
[`HistoricalSimulatorVersions/000_AgingBrain_Simulator_VersionList_000_261110.html`](HistoricalSimulatorVersions/000_AgingBrain_Simulator_VersionList_000_261110.html)
in a browser. Every version opens from that list. (GitHub shows HTML files as source code, so open them from a local copy.)

## What is here

| Folder | Contents |
|---|---|
| [`HistoricalSimulatorVersions/`](HistoricalSimulatorVersions/) | 103 simulator files, one per version, and the version list [`000_AgingBrain_Simulator_VersionList_000_261110.html`](HistoricalSimulatorVersions/000_AgingBrain_Simulator_VersionList_000_261110.html). The list says what changed in each version and how each copy was obtained. |
| [`Buckner_etal_Figure_scripts_261110/`](Buckner_etal_Figure_scripts_261110/) | One script per panel of Figures 1–8 (40 in all), a runner, and the expected output. See its [README](Buckner_etal_Figure_scripts_261110/README_261110.md) for what each script reproduces and where it cannot. |
| [`Buckner_etal_SuppFigure_scripts_261110/`](Buckner_etal_SuppFigure_scripts_261110/) | One script per panel of Supplementary Figures 1–8 (54 in all). See its [README](Buckner_etal_SuppFigure_scripts_261110/README_Buckner_etal_SuppFigures_261110.md), which compares each script with the figure legend. |

The simulator was named Parallax for versions 1–77, LifeBrain Simulator for 78–86 and AgingBrain Simulator for 87–103. Each file name
ends in the version's date (YYMMDD).

## Using a simulator

Open any file from the [version list](HistoricalSimulatorVersions/000_AgingBrain_Simulator_VersionList_000_261110.html) in a local copy of
the repository, or download a single file and open it. It runs entirely in the browser. The default world (seed 7, 120,000 lives born 1926–2008, study year
2026) takes a few seconds to simulate. Every world and draw is seeded, so a given version with given settings gives the same numbers on
any computer.

Each file carries its own documentation: a developer guide, a model description, reality checks and a version history.

## Reproducing the figures

The scripts do not re-implement the model. Each one opens the simulator file the paper used in a headless browser and calls the same
functions the application's buttons call.

**Main figures** (JavaScript, Node 18 or later):

```sh
cd Buckner_etal_Figure_scripts_261110
npm i playwright && npx playwright install chromium     # once
node run_panel_261110.mjs Buckner_etal_Figure6PanelF_261110.md
```

Compare the output with [`expected_output_261110.txt`](Buckner_etal_Figure_scripts_261110/expected_output_261110.txt).

**Supplementary figures** (Python 3): each Markdown file holds one Python block. Save it as a `.py` file of the same name and run it
with the simulator file:

```sh
cd Buckner_etal_SuppFigure_scripts_261110
pip install playwright numpy matplotlib && playwright install chromium   # once
python Buckner_etal_SuppFigure6PanelE_261110.py AgingBrain_Simulator_v102_261109.html
```

### Which simulator file each set of scripts uses

The scripts name their simulator files as the paper's analyses did. Those names differ from the names in `HistoricalSimulatorVersions/`.
So both script folders work as they stand, each one holds a copy of the files it needs under the name its scripts expect. Each copy is
byte-for-byte identical to the historical file:

| Name used by the scripts | Version | Identical to |
|---|---|---|
| `Buckner_etal_Figure_scripts_261110/AgingBrain_Simulator_261023.html` | 99 (Figures 1–6, 8) | `HistoricalSimulatorVersions/AgingBrain_Simulator_v99_261023.html` |
| `Buckner_etal_Figure_scripts_261110/AgingBrain_Simulator_261014.html` | 88 (Figure 7) | `HistoricalSimulatorVersions/AgingBrain_Simulator_v88_261014.html` |
| `Buckner_etal_Figure_scripts_261110/AgingBrain_Simulator_v91_261018.html` | 91 branch (source of Figure 5F's generational settings; not run itself) | a working branch, not one of the published versions |
| `Buckner_etal_SuppFigure_scripts_261110/AgingBrain_Simulator_v102_261109.html` | 102 (all supplementary figures) | `HistoricalSimulatorVersions/AgingBrain_Simulator_v102_261104.html` |

### Checked in this repository

The repository's own files were rerun on 2026-11-10 (Node 24, Python 3.12, Playwright 1.65, headless Chromium):

- **Figures 1–8:** all 40 scripts ran. Each output matches `expected_output_261110.txt` line for line, apart from the timing lines.
- **Supplementary Figures 1–8:** all 54 scripts ran without error against version 102. The printed values checked against the "Against
  the legend" column of the supplementary README agree with it.

Where a panel cannot be reproduced exactly, and why, is set out in each folder's README.

## Citation

If you use the simulator or these scripts, please cite the paper above. A full reference will be added when the preprint is posted.

Correspondence: Randy L. Buckner (randy_buckner@harvard.edu)

## License

Released under the [MIT License](LICENSE).
