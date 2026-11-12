# AgingBrain Simulator

Every published version of the AgingBrain Simulator, from version 1 to version 103, together with the scripts that reproduce each panel of
the paper's figures and supplementary figures.

> Buckner RL, …, Nyberg L. *Synthesizing and Predicting Brain and Cognitive Aging Data Patterns Using an Evolving Simulator Enabled by
> Agentic Artificial Intelligence.* bioRxiv (forthcoming).

The simulator generates worlds of 120,000 individual lives. Each life starts from baseline parameters (genetic risk, birth year, childhood
ability, …) and changes with age through explicit causal cascades (aging, cardiovascular, the AD cascade, sleep, engagement, LATE). The
simulator then runs studies on those worlds through selection, measurement, follow-up and intervention stages. Each version is a single HTML file
that opens on its own in a browser.

**Open the simulators:** download or clone this repository and open
[`HistoricalSimulatorVersions/000_AgingBrain_Simulator_VersionList_000_261110.html`](HistoricalSimulatorVersions/000_AgingBrain_Simulator_VersionList_000_261110.html)
in a browser. Every version opens from that list.

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
the repository, or download a single file and open it. It runs entirely in the browser. The default world is seed 7, 120,000 lives born 1926–2008, study year
2026. Every world and draw is seeded, so a given version with given settings gives the same numbers on
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

## Citation

If you use the simulator or these scripts, please cite the paper above.

Correspondence: Randy L. Buckner (randy_buckner@harvard.edu)

## License

Released under the [MIT License](LICENSE).
