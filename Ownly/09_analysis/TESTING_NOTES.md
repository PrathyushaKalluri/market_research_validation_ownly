# Testing Notes — 2026-09-14

## Environment
- Python 3.9 in a venv in the session scratchpad (not in the project).
- `pip install` succeeded: pandas 2.3.3, numpy 2.0.2, scipy 1.13.1, statsmodels 0.14.6.

## What ran
`PYTHON=<venv>/bin/python bash tests/run_demo_test.sh`:
1. `tests/make_demo_synthetic.py` writes DEMO_SYNTHETIC fixtures to the scratchpad only:
   - 4 Hyderabad form exports (60 rows each) and 2 Bengaluru exports (70 rows each), with Google-Forms-style question headers and label answers. Includes screen-outs, speeders, attention fails, 2 injected token duplicates per file, and planted choice-task utilities and fee-ladder values.
   - A 3,600-row audit file and a 2,271-event fake-door file.
2. `run_all.sh`, steps 00–13, finished end to end with **exit 0**. All tables were written to `scratchpad/demo_synthetic/out/`.

## What passed
- **Ingest:** 0 unmapped columns and 0 unmatched answer labels in the last run. The attention-check grid row maps via the grid scale.
- **Flags:** screen-outs, speeders, token duplicates and incoherence flags all triggered. Borderline rows went to `pending_adjudication`. Sample-flow table written.
- **Choice-task model:** recovered the planted ordering (professionals value time and reliability more than students). The segment models are correctly labelled "segment_n_below_125_directional".
- **Fee ladder:** staircase reconstruction ran; acceptance curves, median fee, elasticities and the start-effect model were produced.
- **City comparison:** weights and non-inferiority verdicts produced. The 2×2 cell-collapse path runs.
- **Audit:** matched pairs, cluster-bootstrap medians, win rate and coverage.
- **Fake door:** funnel per variant, Wilson CIs, Holm-adjusted pairwise tests, P(best), DIRECTIONAL flag.
- **Hypothesis tests:** 33 hypothesis rows with verdicts. H12.1 was correctly NOT TESTABLE because too few events per predictor (n = 57 Ownly users).
- **Scorecard:** default weights plus 3 alternative weight sets, with the decision rule applied.
- **Guards:**
  - Writing synthetic rows into `08_clean_data/` is refused in demo and non-demo mode.
  - The generator refuses any output folder inside the project.
  - A `find` for `*DEMO_SYNTHETIC*` inside the project returns nothing.

## Bugs found and fixed during testing
- f-string backslash (Py 3.9)
- post-stratification cell-collapse crash
- duplicate and gibberish heuristics over-flagging normal short text
- attention-check label mapping
- spurious numpy matmul warnings in the Krinsky-Robb draws (now Cholesky, with a finite-value check)

## Known limitations / not tested
- **Synthetic data tests the code, not the statistics.** The fixture numbers are meaningless, and no synthetic output is to be copied or cited.
- **Real exports are untested.** Real Google Forms headers depend on how the team builds the forms, so `form_column_map.csv` must be filled in and one pilot export run first. Checkbox answers are split by substring matching, so options containing commas are matched as whole labels; check `recode_unmatched.csv`.
- **Duration** needs `meta_start_ts` pre-filled by the link randomiser. Without it, EX02 cannot be computed and `FLAG_no_duration` = 1.
- **Duplicate text similarity** is O(n²) — fine up to ~1,000 rows.
- **Bootstrap counts** are reduced in the test (500/300); production defaults are 10,000/5,000.
- **H12.1 bootstrap** uses 500 resamples; small samples may cause separation. Firth regression is not implemented (optional dependency).
- **Interview segments and the evidence matrix** are filled by hand and not produced by the pipeline.
- **Several mart fields are left blank** because the survey has no matching item: `beh_last_time`, `beh_abandon_freq`, `beh_abandon_reason`, `dec_trial_trigger_coded`, `bt_concern_coded`. They need a schema/dictionary reconciliation by the lead or dashboard owner.
