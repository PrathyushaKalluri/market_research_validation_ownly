# file_manifest.md

## The brief's specified structure → where it actually lives
Per decision **D7**, no duplicate tree was created. Mapping:

| Brief path | Actual location |
|---|---|
| `00_context/project_context.md` | `_ops/project_context.md` |
| `00_context/research_question.md`, `hypotheses.md` | `_ops/project_context.md` §§ business question, hypothesis · `00_research_charter/C_hypothesis_tree.md` |
| `00_context/assumptions_constraints.md` | `00_research_charter/B_assumption_map.md` |
| `00_context/file_manifest.md` | **this file** |
| `01_plan_tracking/*` | `_ops/` (all seven) |
| `02_secondary_research/secondary_findings.md` | `01_secondary_research/secondary_research_report.md` |
| `02_secondary_research/evidence_map.csv` | `01_secondary_research/evidence_table.csv` (68 claims) |
| `02_secondary_research/claims_vs_evidence.md` | `01_secondary_research/consolidated/consolidated_evidence_pack.md` §2 |
| `03_primary_research/survey/*` | **`13_survey_v3_live/`** |
| `03_primary_research/interviews/*` | `04_interviews/` (`*_v3.*` are live) |
| `03_primary_research/whatsapp_polls/*` | **`14_quick_polls/`** |
| `03_primary_research/fake_door/*` | `07_fake_door/` (`AB_LAUNCH_RUNSHEET_v2.md` is live) |
| `04_market_audit/*` | `06_competitor_audit/` (`*_PREFILLED.csv` are live) |
| `05_analysis/*` | `09_analysis/` (+ `short_plan/`), `08_clean_data/` |
| `06_dashboard/*` | `10_dashboard/` |
| `07_final_submission/*` | `11_insights/`, `12_final_presentation/` |
| `98_reference_only/` | `Marketing Metrics 1000 Records.csv`, `Formulae Sheet (1).docx`, `Formulae Sheet 2.pdf` — see below |
| `99_archive/` | `../archive/` |

## Session recovery

`../responses.md` holds every operational response Claude has given, verbatim, newest at the bottom.
**If the chat session is lost:** hand Claude `responses.md` + `claude_master_project_orchestrator_prompt.md`
+ the seven `_ops/` files, and it resumes with full continuity.

## Live artefacts created 2026-09-16
| File | Purpose | Owner |
|---|---|---|
| `_ops/*.md` (7 + this + report template) | Project brain | Claude |
| `01_secondary_research/consolidated/consolidated_evidence_pack.md` | The one secondary exhibit | Claude |
| `01_secondary_research/consolidated/rollup_themes.py` | Reproduces it | Claude |
| `13_survey_v3_live/survey_logic.md` | Branch map + H₀ primacy rule | Claude |
| `13_survey_v3_live/survey_questions.md` | Every question, exact wording, KPI map | Claude |
| `13_survey_v3_live/google_forms_build_guide.md` | Click-by-click build + 7 test cases + freeze rules | **P1 executes** |
| `13_survey_v3_live/survey_distribution_plan.md` | Channel plan and quota watch | **All** |
| `13_survey_v3_live/survey_response_tracker.csv` | Running counts by channel and quota | **P1** |
| `07_fake_door/AB_LAUNCH_RUNSHEET_v2.md` | 2-arm launch, QA, stopping rule, reading rule | **P3 executes** |
| `07_fake_door/prototype/index.html` | Patched to 2 arms, v `2026-09-16.1` | Claude |
| `07_fake_door/prototype/index_v1_3arm_ARCHIVE.html` | The 3-arm original, kept | — |
| `07_fake_door/experiment_tracker.csv` | Channel register | **P3** |
| `04_interviews/RAPID_15min_guide_v3.md` | 15-min behavioural guide | **P2 executes** |
| `04_interviews/proposition_card_v3.md` | The two cards to print | **P2** |
| `04_interviews/interview_notes_v3_template.md` | Note template | **P2** |
| `04_interviews/participant_tracker_v3.csv` | Participant log | **P2** |
| `04_interviews/outreach_scripts_v3.md` | 10 scripts + ranked recruitment sources + quotas | **All** |
| `06_competitor_audit/AUDIT_RUNSHEET_v3.md` | Day-0 check, frame, capture rules, metrics | **P3 executes** |
| `06_competitor_audit/audit_captures_PREFILLED.csv` | **60 rows pre-filled — type numbers only** | **P3** |
| `06_competitor_audit/restaurant_frame_PREFILLED.csv` | 10 restaurants, 6 named, 4 to fill | **P3** |
| `14_quick_polls/exact_poll_copy.md` | 3 polls, verbatim + contamination rule | **P2 executes** |
| `14_quick_polls/poll_plan.md`, `poll_tracker.csv` | Plan and log | **P2** |

## Source files — never overwritten
| File | Status |
|---|---|
| `Marketing Metrics 1000 Records.csv` | **REFERENCE ONLY.** Generic 2024–25 USD campaign data, not Ownly and not food delivery. Used **only** to demonstrate digital-funnel KPI definitions in an appendix. 325 rows have conversions > qualified leads — flag it when shown. **Never mixed with Ownly evidence.** |
| `Formulae Sheet (1).docx`, `Formulae Sheet 2.pdf` | Course formula sheets. Mapped to our data in `00_research_charter/P_3day_plan_ethics_budget_kpis.md` §5. Reference only. |
| `evidence_table.csv`, `ownly_segments_evidence.csv`, `reviews_coded.csv`, `social_coded.csv`, `listing_stats.csv`, `retrieval_log.csv`, `search_log.csv`, `reviews_validation_sample.csv` | Original coded datasets. Read-only. The consolidation writes to a **new** folder and never edits these. |
| `claude_master_project_orchestrator_prompt.md`, `review_log.md` | Governing documents. Read-only. |

## Superseded, kept for reference
| File | Superseded by | Why kept |
|---|---|---|
| `03_hyderabad_survey/SHORT_survey_7min_google_form.md` | `13_survey_v3_live/` | Hyderabad-only; predates the 3-city routing (D4) |
| `07_fake_door/experiment_plan.md` §4 (3 arms) | `AB_LAUNCH_RUNSHEET_v2.md` | Everything except §4 still applies |
| `04_interviews/interview_guide_30min.md`, `_45min.md` | `RAPID_15min_guide_v3.md` | The full design, for the "more time" appendix |
| `../13_`–`17_*.md` (v1) | v2 framing | SUPERSEDED banners already in place |
| `00_research_charter/O_execution_checklist_and_timeline.md` | `_ops/plan.md` | The 5-week next-phase appendix |
