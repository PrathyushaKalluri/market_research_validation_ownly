# progress.md — execution log

Earlier history (to 2026-09-14) is at `../../progress.md`.

---

## 2026-09-16, ~12:30 — Claude joins as execution lead. State assessment.

**Finding: the project has a complete research design and zero primary data.**
The last substantive file change was 2026-09-14 22:46. `08_clean_data/raw/` is empty. No audit captures,
no survey responses, no fake-door events, no interviews. Two calendar days have passed against a
three-day plan whose deadline was recorded as 17 September.

| Stream | Designed | Fielded | Data |
|---|---|---|---|
| Survey | ✅ | ❌ | 0 |
| Interviews | ✅ | ❌ | 0 |
| Price audit | ✅ | ❌ | 0 |
| Fake door | ✅ (then dropped) | ❌ | 0 |
| Secondary + review mining | ✅ | ✅ | 68 claims · 37 reviews · 524 social items |

**Read:** the binding constraint is not design quality — it is that no instrument has been put in front
of a human. Work Block 1 does nothing but fix that.

## 2026-09-16 — Claude's output this block

| Done | Artefact |
|---|---|
| Read all ~150 project files, both governing documents, all evidence CSVs | — |
| **Consolidated all coded evidence into one exhibit** + reproducible script | `01_secondary_research/consolidated/consolidated_evidence_pack.md`, `rollup_themes.py` |
| Rebuilt the survey: canonical 3-city routing, trier/non-trier branch, paired proposition test | `13_survey_v3_live/survey_logic.md`, `survey_questions.md`, `google_forms_build_guide.md` |
| Collapsed the fake door 3 arms → 2, rewrote both variants, **patched the prototype HTML** | `07_fake_door/AB_LAUNCH_RUNSHEET_v2.md`, `prototype/index.html` (v `2026-09-16.1`) |
| Compressed the interview kit to 15 min; wrote proposition cards, notes template, tracker, outreach scripts, ranked recruitment sources | `04_interviews/*_v3.*` |
| **Pre-filled 60 audit rows** (slot/platform/restaurant/basket/screenshot name) + restaurant frame + runsheet | `06_competitor_audit/AUDIT_RUNSHEET_v3.md`, `audit_captures_PREFILLED.csv`, `restaurant_frame_PREFILLED.csv` |
| Wrote 3 polls with exact copy, contamination rule, tracker | `14_quick_polls/` |
| Stood up the seven tracking files | `_ops/` |
| **Pre-registered the H₀ primacy rule before any data exists** | `_ops/decisions.md` D3 |

**Headline from the consolidation — the strongest pre-fieldwork result we have:**
> Price-doubt is **35%** of all public discussion but only **16%** of first-hand accounts.
> Fulfilment failure is **15%** of discussion but **47%** of first-hand accounts and **72%** of app
> reviews. Support/refund runs the same way: 11% → 28% → 72%.
> **What people argue about is price. What people who actually ordered report is fulfilment.**
> (Self-selected complaint sample — this says failure dominates *complaints*, not that 47% of orders fail.)

Also established: 74% of the secondary base is media report or company claim, only 24% verified, and
**Hyderabad is mentioned in 4 of 524 social items.** That gap is the project.

## Counts
| | Target | Now |
|---|---:|---:|
| Hyderabad survey responses | 80–100 | **0** |
| Bengaluru survey responses | 15–30 | **0** |
| Interviews | 8 | **0** |
| Audit captures | 60 | **0** |
| Test orders | 3 | **0** |
| Fake-door visitors | 80+ | **0** |
| Poll votes | 170+ | **0** |

## Blocked on
Written ethics approval (Q2) · Ownly serviceability at DP1 (Q3) · pilot-interview verdict on Service Q (Q6)
· **the actual deadline (Q1)**.

## Next action
Work Block 1 in `task_board.md`. Report back per `_ops/report_back_template.md`.
