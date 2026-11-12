# Buckner et al., Figure 2E: Measurement process stage, measured against true episodic memory

Simulator: `AgingBrain_Simulator_261023.html` (version 99; default world: seed 7, 120,000 lives, study year 2026)
Run: `node run_panel_261110.mjs Buckner_etal_Figure2PanelE_261110.md`
The 400 participants of panel D, episodic memory measured once in 2026 with the default error (SD 0.4, validity 1), against its true value;
the fitted line is least squares, measured on true. Also the application's retest r and MDC95 for the same participants.

```js
Object.assign(state.sel, { strat: 'nondem', seed: 1 });
Object.assign(state.sel.q.nondem, { lo: 60, hi: 90, n: 400, women: 55, by: 'mmse', mmse: 24 });
const R = runSelection(), w = state.run.agg.w26, st = msStats(w, R.sel, 'mem');
const fit = anFitG(R.sel, (r) => anVal(w, r, 'mem'), (r) => anObs(w, r, 'mem'), []);
return { participants: R.sel.length, error_SD: state.ms.mem.err, validity: state.ms.mem.val, fitted_slope: +fit.slope.toFixed(3), intercept: +fit.b[0].toFixed(3),
  r_with_true: +st.rv.toFixed(3), retest_r: +st.rt.toFixed(3), MDC95_SD: +st.mdc.toFixed(2) };
```
