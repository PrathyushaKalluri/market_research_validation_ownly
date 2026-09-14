# 09_analysis — Reproducible Analysis Pipeline

The pipeline implements `M_pre_analysis_plan.md` (PAP) and `08_clean_data/cleaning_protocol.md`. Hypotheses and thresholds come from `00_research_charter/C_hypothesis_tree.md`. Scorecard anchors and weights come from `11_insights/decision_framework_and_scorecard.md`. Every constant lives in `config.py`, seed 20260914.

## Setup
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r 09_analysis/requirements.txt
```

## Before the first export
1. `python make_form_column_map.py` → `form_column_map_TEMPLATE.csv`.
2. Copy it to `form_column_map.csv`.
3. For each row, replace `expected_header` with the **exact** column header in the Google Forms export. Headers for choice tasks, bills and fee ladder are placeholders and differ by version. `form_family` = both / hyd / blr / V1…V4 / B1, B2.
4. Name raw exports `hyd_survey_v1_raw_YYYYMMDD.csv` … `blr_survey_b2_raw_YYYYMMDD.csv`. Save them in `08_clean_data/raw/` and never edit them.
5. Audit data goes to `06_competitor_audit/data/audit_obs.csv` (schema `audit_schema.csv`). Fake-door events go to `07_fake_door/data/events_raw.csv`.

## Run
```bash
bash 09_analysis/run_all.sh          # PYTHON=.venv/bin/python bash ... to pick an interpreter
```

| Step | Reads | Writes |
|---|---|---|
| 00 manifest | raw/*.csv | raw/MANIFEST.csv (SHA-256; stops if a raw file changed) |
| 01 ingest | raw exports + form_column_map.csv + survey dictionary | interim/survey_combined.csv, unmapped_columns.csv, recode_unmatched.csv |
| 02 flags | interim | flags.csv (EX01–EX09 as ''/borderline/hard; FLAG_* sensitivity) |
| 03 split | flags + adjudication_log.csv | cleaned/, excluded/ (with exclusion_reason), pending_adjudication.csv, outputs/sample_flow.csv |
| 04 derive | cleaned | outputs/survey_respondent_full.csv, dce_long_full.csv, index_reliability.csv; mart fact_survey_respondent, fact_dce_long, fact_wtp_long, fact_bill_choice_long |
| 05 descriptives | derived | outputs/descriptives/*.csv (n + CIs) |
| 07 DCE (Hyderabad only) | dce_long_full | dce_task_shares, dce_hypothesis_inputs, mart fact_model_dce |
| 08 fee WTP | fact_wtp_long | wtp_curve, wtp_summary, wtp_elasticity, wtp_model_coefs |
| 09 city transfer | derived | transfer_metrics, composition_check; w_match_hyd in mart |
| 10 audit | audit_obs.csv | mart fact_audit_obs, fact_audit_pairs; audit_summary, audit_coverage |
| 11 reviews | 05_review_mining/*/*_coded.csv | mart fact_reviews; review_theme_summary, review_summary_metrics |
| 12 fake door | events_raw.csv | mart fact_fakedoor_events, agg_fakedoor_variant; fakedoor_pairwise |
| 06 hypothesis tests (runs after 07–12) | all of the above | hypothesis_results.csv, mart dim_hypothesis |
| 13 scorecard | all of the above | mart fact_scorecard; decision.csv (default + 3 alternative weight sets) |

Mart tables follow `10_dashboard/dataset_schema.md`. Tables that are filled by hand, not by the pipeline: `fact_interview_segments`, `fact_evidence_matrix`, `dim_chart`.

## Human steps the code cannot replace
- **Borderline flags:** two team members fill in `adjudication_log.csv` (resp_id, flag, reviewer_1, reviewer_2, decision = keep/exclude, rationale, date). Then rerun step 03.
- **Locality recodes:** "Other" localities go in `locality_recode_log.csv` (resp_id, raw_text, recoded_area, recoded_outside 0/1).
- **Unaided awareness:** two people code Ownly mentions into an `own_aware_unaided` column. Until then, a regex first pass is used and labelled as such.
- **Unmatched answers:** check `recode_unmatched.csv` and `unmapped_columns.csv` after every run. A label that doesn't match the dictionary becomes NA.
- **Audit fee:** `OWNLY_OBSERVED_FEE_INR` is taken from the audit median unless you override it with that environment variable.
- **Final recommendation:** `decision.csv` is an *input* to the joint human recommendation, never the decision itself.

## Freezing the PAP and logging deviations
1. Before the first real response is analysed, copy `M_pre_analysis_plan.md` to `PAP_frozen_YYYYMMDD.md`. Also record the SHA-256 of `config.py` in that file.
2. After freezing, any change to `config.py` thresholds or weights, or to test logic, gets a row in PAP §11 (date, section, deviation, reason, impact). It also gets an entry in `decisions.md`.
3. Report analyses added after freezing as **EXPLORATORY**.

## Synthetic test data
`tests/run_demo_test.sh` generates **DEMO_SYNTHETIC** fixtures and runs the full pipeline. Everything goes to the scratchpad only. `utils_io.guard_path` refuses to write synthetic data inside the project, and always inside `08_clean_data/`. See `TESTING_NOTES.md`.

## Master data dictionary
`python make_master_dictionary.py` regenerates `08_clean_data/master_data_dictionary.csv` from: the survey dictionary, derived-variable definitions, mart schemas, the audit schema, review/interview headers and fake-door events. Rerun it whenever any of those change.
