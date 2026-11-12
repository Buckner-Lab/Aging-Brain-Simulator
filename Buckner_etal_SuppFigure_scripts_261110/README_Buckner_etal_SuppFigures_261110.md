# Analysis scripts for the Supplementary Figures: Buckner et al., the AgingBrain Simulator

## What these are

These are the analysis scripts for Supplementary Figures 1-8. There is one script for every panel, 54 files in all. Supplementary Figure 8 is a single table, so its file is filed as panel A. Each file is Markdown named `Buckner_etal_SuppFigureXPanelY_261110.md` and holds one Python block. The block opens with a few comment lines saying what the panel shows and the command to run it, followed by the code. When run, a script prints the numbers that its panel and legend report and saves a plain plot of the panel. The plot is named like the script (`..._261110.png`).

## How they reproduce the figures

The figures were made from the simulated world, and so are the scripts. Each one opens the simulator file (`AgingBrain_Simulator_v102_261109.html`, version 102) in a headless browser. It waits for the default world to be simulated: 120,000 lives in world 7, study year 2026. It then computes the panel with the application's own code:

- the engine (`E`): each life traced, the reference person, every life lived again from its fixed draws
- Selection's sample (`runSelection`)
- the Measurement process (`msAt`, `msStats`, `msPrac`)
- Follow-up and Intervention (`anRecs`, `ivArms`)
- the reality checks and model description (`wpChecks`, `wpModelHtml`)

To reach that code, a script adds one line to its in-memory copy of the page (`window.__abEval = s => eval(s)`, placed just before the application starts). The file on disk is never changed, and nothing is computed differently. Where a panel needs a different world (a setting switched off, another seed or another sample), the script changes the setting and simulates the world again, as a user would in the application.

Three groups of panels come from stages that version 102 does not contain: Biomarker timelines (Supplementary Figure 6), Childhood mortality worlds (Supplementary Figure 7) and the example stages of Supplementary Figure 5. For these, the script writes out the steps the stage takes and runs them with the same functions.

Every script was run on version 102, as extracted from its Markdown file, and its printout compared with the figure's legend. The last column of the index gives the result.

## Where they cannot, and why

- **An earlier file.** 1A maps the bytes of version 102 (879,317 bytes). The panel mapped the earlier, smaller file it shows, so the totals and shares differ.
- **Stages built on version 95** (Supplementary Figure 5A-I). These builds are not part of version 102. Their own choices (who was drawn, which random seeds, how a group was defined) live only in those builds. The scripts compute each stage's result with version 102's world and functions, so numbers in 5A, 5B, 5C, 5D and 5H differ from the legend:
  - 5A: the world and sample differ from the build's.
  - 5B: the trials use different random seeds.
  - 5C: the build drew its own 30 participants.
  - 5D: version 102 changed the maintainers' rule.
  - 5H: the default world has 7.9% with dementia, against the build's 7.7%.
- **Analyses made only inside a build.** 5G's analysis of the Fjell et al. (2026) preprint and 5H's pandemic world were constructed within those version 95 stages and are not reproduced. The 5G script shows instead what the preprint's anchors would change (the world's cohort settings and memory at 70 by decade of birth). The 5H script leaves the pandemic world out.
- **Content that is not computed.** 7D's bars are spans of published estimates. Supplementary Figure 8's prompts and interpretations come from the development conversations, so its script prints the file's version-history line for each version in the table. The "Built from one prompt" panels (6A, 7A) print the prompt that Imagine gives for each example. The builds' own copies of their prompts are kept in those builds (v102_BT, v101_CMW).
- **One engine change, as in the figure.** 2F's brain path needs the reference person's hippocampal loss to follow ability. Version 102's reference person holds hers at the mean, so the script uses an in-memory copy of the engine with that one line changed, as the figure did.
- **Small differences.** The 75-84 group in 3E counts 19,667 lives, one more than the legend's 19,666.

## Running them

You need Python 3 with `pip install playwright numpy matplotlib` and `playwright install chromium`. Scripts 1A, 1B and 8A need only numpy and matplotlib.

To run one, save its code block as a `.py` file named like the Markdown file. Put the simulator file in the same folder and run, for example:

`python Buckner_etal_SuppFigure6PanelE_261110.py AgingBrain_Simulator_v102_261109.html`

How long they take:

- most scripts: about 10 seconds (1A, 1B and 8A, which need no browser: a second or two)
- 1C, 2G, 3D, 3E, 5F, 5G and 5H, which simulate a second world or live every life again: 15-25 seconds
- 5B, which runs 800 trials, and 7F, which simulates ten worlds: about 1.5 minutes each
- 5I, which simulates several worlds: about 2 minutes

Besides their plots, 1D writes the settings file and 5E writes three CSV files, all dated `_261110`.

## Index

| Script | Panel | What it computes | Against the legend |
|---|---|---|---|
| `Buckner_etal_SuppFigure1PanelA_261110.md` | 1A Everything in one file | The file's bytes in order, assigned to roles by landmarks in the file | Differs: maps version 102's file (879,317 bytes); the panel mapped the earlier file it shows (831,208) |
| `Buckner_etal_SuppFigure1PanelB_261110.md` | 1B Reads itself | The file's first lines and the developer guide's 13 sections | Matches |
| `Buckner_etal_SuppFigure1PanelC_261110.md` | 1C Describes and checks itself | The model description and the 13 reality checks, with aging's late rise and without it | Matches: 12 of 13 checks in range; three more fail without the late rise |
| `Buckner_etal_SuppFigure1PanelD_261110.md` | 1D Saves and copies itself | The saved settings (writes the file) and the size of the page's own copy | Matches |
| `Buckner_etal_SuppFigure2PanelA_261110.md` | 2A Childhood ability as implemented | Ability's paths as set: SES, schooling, level at 40, reserve, engagement, brain, the dementia criterion | Matches |
| `Buckner_etal_SuppFigure2PanelB_261110.md` | 2B How the cohort works | People alive at 18-100 in 2026, the cohort settings, the early-cohort ability check; a Lexis plot of 150 lives | Matches (89,554; r = 0.64) |
| `Buckner_etal_SuppFigure2PanelC_261110.md` | 2C Birth year and ability | Expected schooling and the level at 40 by year of birth, at ability -1, 0 and +1 SD | Matches (about 2.2 years; 0.65 against 0.16 SD per decade) |
| `Buckner_etal_SuppFigure2PanelD_261110.md` | 2D Ranking the determinants | Shapley shares of R2 for 11 determinants and five outcomes, over every life | Matches (85%, 77%, 56%, 18%, 9%; the leading determinants) |
| `Buckner_etal_SuppFigure2PanelE_261110.md` | 2E One life by ability | The reference woman at ability -1, 0 and +1 SD: the start at 40 and dementia with and without the cascade | Matches (87, 91, 95; 92, 98, not by 100) |
| `Buckner_etal_SuppFigure2PanelF_261110.md` | 2F Where ability acts | Each of ability's five paths: its share of the gap in cognition at 85, dementia, the hippocampus | Matches; the brain path uses an in-memory copy of the engine with one line changed, as the figure did |
| `Buckner_etal_SuppFigure2PanelG_261110.md` | 2G The world by ability | Three ability groups: alive at 40, SES, schooling, cognition by age, dementia by age | Matches (18,730, 80,375, 18,618; 39.4%, 14.3%, 3.8% by 85) |
| `Buckner_etal_SuppFigure3PanelA_261110.md` | 3A The AD cascade as implemented | The cascade's settings in the legend's order; the onset anchor counted across the world | Matches (24% is set for an e3/e3 carrier of average traits; 23.2% across the e3/e3 carriers with their traits) |
| `Buckner_etal_SuppFigure3PanelB_261110.md` | 3B One life, amyloid positive at 65 | The reference person: tau positivity, MCI and dementia with and without the cascade; its toll by 90 | Matches (80, 86, 91; 91, 98; 0.85 mL, 1.08 SD) |
| `Buckner_etal_SuppFigure3PanelC_261110.md` | 3C Order of change | Years after positivity at which each change is halfway | Matches (7, 9, 22, 24-25, 27) |
| `Buckner_etal_SuppFigure3PanelD_261110.md` | 3D Onset by APOE | Share amyloid positive by each age if they lived, by e4 alleles; share positive before death | Matches (22%, 59%, 85%; medians 81, 68, 60; 62%) |
| `Buckner_etal_SuppFigure3PanelE_261110.md` | 3E After amyloid positivity | Everyone positive at 60-69 or 75-84, followed by years since positivity | Matches, except the 75-84 group: 19,667 (legend 19,666) |
| `Buckner_etal_SuppFigure3PanelF_261110.md` | 3F Where each trait acts | The cascade's toll by 90 with one trait changed at a time | Matches the legend's statements |
| `Buckner_etal_SuppFigure4PanelA_261110.md` | 4A The measurement process | Each variable's error, factors, validity and practice model; the attrition settings | Matches |
| `Buckner_etal_SuppFigure4PanelB_261110.md` | 4B Reliability | Retest r and r with the true value in the study of Figure 2C-2H | Matches |
| `Buckner_etal_SuppFigure4PanelC_261110.md` | 4C Error at a cut point | Amyloid PET measured once against its true value, classified at 20 CL | Matches (5 called positive in error; 4 of 134 missed; 316 shown) |
| `Buckner_etal_SuppFigure4PanelD_261110.md` | 4D Practice effects | The expected practice gain at each of eight tests, at four spacings | Matches |
| `Buckner_etal_SuppFigure4PanelE_261110.md` | 4E Missed visits and dropout | Shares alive, still in the study and seen at each visit | Matches (alive 66.5%, given as 67%; 32%; 29%) |
| `Buckner_etal_SuppFigure4PanelF_261110.md` | 4F What the study records | Mean change in memory under error, practice and attrition, and what each hides | Matches |
| `Buckner_etal_SuppFigure5PanelA_261110.md` | 5A Distributions | Episodic memory in the sample against everyone alive at the same ages | Differs: 0.00 SD (legend 0.12), from the version 95 build's own world and sample |
| `Buckner_etal_SuppFigure5PanelB_261110.md` | 5B Power | Share of 200 repeated Intervention trials finding the effect, by sample size | Differs: 18% at 2,000 (legend 23%); the trials' random seeds differ |
| `Buckner_etal_SuppFigure5PanelC_261110.md` | 5C Biomarker timelines | Median years from amyloid to tau positivity and to dementia among the 30 drawn | Differs: 11 and 13 (legend 9 and 15); the version 95 build drew its own 30 |
| `Buckner_etal_SuppFigure5PanelD_261110.md` | 5D Compare definitions | Three Selection strategies: memory above age peers and dementia within 10 years | Differs: 1.50, 1.31, 1.27 SD and 6%, 6%, 14% (legend 1.55, 0.64, 1.19 and 3%, 16%, 13%); version 102 changed the maintainers' rule |
| `Buckner_etal_SuppFigure5PanelE_261110.md` | 5E Export | Writes the study-year and visit values as CSV files, with a dictionary | No numbers in the legend |
| `Buckner_etal_SuppFigure5PanelF_261110.md` | 5F Life map | 2,000 lives' memory trails up to each calendar year, 1990-2040 | No numbers in the legend |
| `Buckner_etal_SuppFigure5PanelG_261110.md` | 5G Generational anchors | The world's cohort settings and memory at 70 by decade of birth | Not reproduced: the stage's analysis of the Fjell et al. (2026) preprint was made inside the version 95 build |
| `Buckner_etal_SuppFigure5PanelH_261110.md` | 5H Alternative worlds | Dementia at 65 and older in the default world, with AD cured and with AD prevented in half | Partly: 5.7% and 6.8% match; default 7.9% (legend 7.7%); the pandemic world was the build's own and is not reproduced |
| `Buckner_etal_SuppFigure5PanelI_261110.md` | 5I Diagnosis by decline | The default dementia rule against diagnosis by the fall alone, by childhood ability | No numbers in the legend |
| `Buckner_etal_SuppFigure5PanelJ_261110.md` | 5J Childhood mortality worlds | Share at 80-90 who would have died as children; dementia among them and among the survivors | Matches (5.5%, 22.6%, 18.0%) |
| `Buckner_etal_SuppFigure6PanelA_261110.md` | 6A Built from one prompt | The prompt Imagine's Copy prompt gives for the example | Matches (the v102_BT build kept it word for word) |
| `Buckner_etal_SuppFigure6PanelB_261110.md` | 6B Who is lined up | Who became amyloid positive, and the 30 drawn | Matches (277: 51 by 2026, 226 later; 123 never; 5 and 25 drawn) |
| `Buckner_etal_SuppFigure6PanelC_261110.md` | 6C Positive at different ages | Ages at positivity, how many after 2026, deaths within 20 years | Matches (51-96, median 66; 25; 15) |
| `Buckner_etal_SuppFigure6PanelD_261110.md` | 6D Lined up, with what followed | Tau positivity, dementia and death within 20 years of amyloid positivity | Matches (21, median 11; 11, median 13; 15) |
| `Buckner_etal_SuppFigure6PanelE_261110.md` | 6E Amyloid PET | Amyloid PET's lines and average course; the stage's table | Matches |
| `Buckner_etal_SuppFigure6PanelF_261110.md` | 6F Tau PET | Tau PET's lines and average course; the stage's table | Matches |
| `Buckner_etal_SuppFigure6PanelG_261110.md` | 6G Hippocampal volume | Hippocampal volume's lines and average course; the stage's table | Matches |
| `Buckner_etal_SuppFigure6PanelH_261110.md` | 6H Episodic memory | Episodic memory's lines and average course; the stage's table | Matches |
| `Buckner_etal_SuppFigure6PanelI_261110.md` | 6I CDR-SB | CDR-SB's lines and average course; the stage's table | Matches |
| `Buckner_etal_SuppFigure6PanelJ_261110.md` | 6J If the settings changed | The average memory course with 200 drawn, or only those positive by 2026 | Matches (-1.79, -1.65, -1.59 SD at +20) |
| `Buckner_etal_SuppFigure7PanelA_261110.md` | 7A Built from one prompt | The prompt Imagine gives for the example in version 102 | The v101_CMW build's own prompt is kept in that build's banner |
| `Buckner_etal_SuppFigure7PanelB_261110.md` | 7B Two worlds, the same births | Both worlds' people at 80-90 and their dementia | Matches (5,858; 18.30% and 18.05%) |
| `Buckner_etal_SuppFigure7PanelC_261110.md` | 7C Deaths before 18, from records | Mortality by 18 by year of birth, in four kinds | Matches (6.4% for the births of 1936-46) |
| `Buckner_etal_SuppFigure7PanelD_261110.md` | 7D Who died is assumed | The ties to SES and ability for each kind; SES alone; lowest against highest fifth | Matches (x0.78 alone; twice as often); the bars, published spans, are not computed |
| `Buckner_etal_SuppFigure7PanelE_261110.md` | 7E Who is missing at 80-90 | The missing share, their dementia, SES and ability; the change with its CI | Matches (5.5%; 22.6% and 18.0%; -0.25, -0.28 to -0.23) |
| `Buckner_etal_SuppFigure7PanelF_261110.md` | 7F If SES were tied more or less | The change across the SES tie, and ten worlds of different seeds | Matches (-0.52 to +0.02; -0.27 to -0.23) |
| `Buckner_etal_SuppFigure7PanelG_261110.md` | 7G If SES and ability were tied | The change across both ties at once | Matches (-0.72 to +0.46; -0.10 and -0.19) |
| `Buckner_etal_SuppFigure7PanelH_261110.md` | 7H If more children had died | The change across the level of childhood mortality | Matches (-0.25, -0.03; -1.45, given as -1.5, and -2.80) |
| `Buckner_etal_SuppFigure7PanelI_261110.md` | 7I Four kinds of death | Each kind's share of the deaths and its part of the change | Matches (81%, 85%; -0.26 and -0.25) |
| `Buckner_etal_SuppFigure7PanelJ_261110.md` | 7J If internal deaths took the frailer | The change with internal deaths also tied to maintenance | Matches (-0.62) |
| `Buckner_etal_SuppFigure8PanelA_261110.md` | 8A Consequential prompts | The file's version-history line for each version in the table | Not computed: the prompts and interpretations come from the development conversations |
