# Project Map & File Architecture (v2)

**Updated:** 2026-09-14. One line per deliverable, mapped to the brief's deliverable numbers (#1–#50) and start-list letters (A–O).

| Folder | File | Brief item | Status |
|---|---|---|---|
| `00_research_charter/` | `A_research_charter.md` | #1–3, #7, A | Draft |
| | `B_assumption_map.md` | #4, B | Draft |
| | `C_hypothesis_tree.md` | #5, C | Draft — thresholds *(A)* need team review |
| | `D_evidence_collection_matrix.md` | #6, #10, D | Draft |
| | `E_research_design_blr_vs_hyd.md` | E | Draft |
| | `F_sample_plan.md` | #8, F | Draft |
| | `O_execution_checklist_and_timeline.md` | #9, O | Draft |
| `01_secondary_research/` | `evidence_table.csv`, `secondary_research_report.md`, `market_price_anchors.md` | Agent A, Ownly evidence table | Done (68 claims) |
| `02_bangalore_survey/` | `bengaluru_google_form.md`, `bengaluru_question_spec.csv`, `bengaluru_survey_logic.md` | #11, #13, G | Done (spec split into `bengaluru_google_form_part1.md` / `part2.md`; `bengaluru_experimental_modules_note.md`) — pilot pending |
| `03_hyderabad_survey/` | `hyderabad_google_form.md`, `hyderabad_question_spec.csv`, `hyderabad_survey_logic.md`, `randomization_and_versions.md`, `choice_experiment_design.md`, `dce_design_matrix.csv`, `bill_comparison_scenarios.md`, `wtp_gabor_granger_design.md`, `survey_variable_dictionary.csv`, `pilot_and_cognitive_test_protocol.md`, `bias_audit.md` | #12–14, H | Done (form split into part1/part1b/part2/part2b; `link_randomizer.html`, `dce_check.py`) — pilot pending |
| `04_interviews/` | `recruitment_plan_and_quota.md`, `screener.md`, `consent_and_privacy.md`, `interview_guide_45min.md`, `interview_guide_30min.md`, `note_taking_template.md`, `interview_log_template.csv`, `coding_framework.md`, `coded_segments_template.csv`, `transcript_analysis_prompt.md` | #15–17, I | Done |
| `05_review_mining/app_stores/` | `reviews_raw.csv`, `reviews_coded.csv`, `codebook.md`, `analysis_tables.md`, `methodology.md`, `collect_and_code.py`, `reviews_validation_sample.csv` | #18, J | Done (n=37; human κ pending) |
| `05_review_mining/social/` | `social_raw.csv`, `social_coded.csv`, `codebook_social.md`, `social_analysis.md`, `search_log.csv` | #18, J (Reddit/LinkedIn) | Done (524 items) + `05_review_mining/voc_synthesis_pre_fieldwork.md` |
| `06_competitor_audit/` | `audit_methodology.md`, `audit_schema.csv`, `audit_data_dictionary.md`, `restaurant_frame_template.csv`, `audit_calculations.md`, `audit_field_sheet.md` | #19, K | Done + `audit_addendum_from_social.md` |
| `07_fake_door/` | `experiment_plan.md`, `landing_page_copy.md`, `event_schema.md`, `events_schema.json`, `prototype/index.html`, `apps_script_collector.gs`, `deploy_instructions.md`, `analysis_framework.md`, `analyze_fakedoor.py` | #20–25, L | Done; preview artifact published |
| `08_clean_data/` | `cleaning_protocol.md`, `raw/`, `cleaned/`, `excluded/`, `master_data_dictionary.csv` (after surveys) | #26 | Protocol done; `master_data_dictionary.csv` (843 variables, rebuilt by `09_analysis/make_master_dictionary.py`) |
| `09_analysis/` | `M_pre_analysis_plan.md`, pipeline scripts (after surveys) | #27–29, M | PAP done; pipeline 00–13 runs end-to-end on synthetic test fixtures (kept outside project); `README.md`, `TESTING_NOTES.md`; needs `form_column_map.csv` from a pilot export |
| `10_dashboard/` | `dashboard_blueprint.md`, `dataset_schema.md`, `build_instructions.md`, `prototype/dashboard_demo.html` | #31–37, N | Done — demo prototype v2 published (DEMO DATA); pipeline table names authoritative |
| `11_insights/` | `decision_framework_and_scorecard.md`, `insight_evidence_matrix_template.csv`, `transfer_matrix_template.csv` | #30, #37, final decision framework | Draft |
| `12_final_presentation/` | `storyline_skeleton.md`, `build_deck.py`, `Ownly_Gachibowli_deck_DRAFT.pptx`, `charts/` | #49 | Draft deck (evidence slides filled; data slides TO FILL) |
| **3-day plan (active)** | `00_research_charter/P_3day_plan_ethics_budget_kpis.md`, `ethics_application_draft.md`, `03_hyderabad_survey/SHORT_survey_7min_google_form.md`, `06_competitor_audit/audit_lite_template.csv`, `test_orders_template.csv`, `audit_lite_how_to_fill.md`, `09_analysis/short_plan/` (2 scripts + `scenario_kpis.md`) | Submission 17 Sep | Ready for fieldwork |
| Root | `context.md`, `plan.md`, `progress.md`, `decisions.md` | Tracking | Updated |
| Root (v1) | `13_`–`17_*.md`, `ownly_project_context.md` | Superseded reference | Banner added |

**Phase 5 (#38–50)** starts only after real data exists in `08_clean_data/raw/`.
