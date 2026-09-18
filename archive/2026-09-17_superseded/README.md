# Archived 2026-09-17 — superseded instruments and analysis

These files are **not live**. They are kept for provenance: they show how the final design was reached,
which an examiner may reasonably ask about. Nothing in the active project reads from this folder.

**The live set, as of 2026-09-17 (decision D14):**

| Thing | Live file |
|---|---|
| Survey | `Ownly/Survey_v6_Google_Form_Build_Guide.md` + the two Rapido questions (D13) |
| KPI framework | `Ownly/09_analysis/kpi_system/` |
| Dashboard | `Ownly/10_dashboard/decision_dashboard/` |
| Fake door | `Ownly/07_fake_door/` (page live, 2 arms) |
| Price audit | `Ownly/06_competitor_audit/audit_data_slot1.csv` + `audit_slot1_results.md` |

## What is in here, and why it was superseded

| File | What it was | Superseded by |
|---|---|---|
| `Survey_v5_All_Cities.md` | The 3-city survey (25 questions) that introduced city routing, per-app order counts and the Ownly funnel | **v6**, which keeps every v5 question and adds the H₀ instrument (decision D9) |
| `Survey_v5_Google_Form_Build_Guide.md` | Click-by-click build guide for v5 | `Survey_v6_Google_Form_Build_Guide.md` |
| `Survey_v5_Question_to_KPI_Map.md` / `.docx` | Mapped every v5 question to the 9-KPI set | `09_analysis/kpi_system/research_to_kpi_map.md` |
| `KPI_Framework_and_Survey_Validation.md` | The 9-KPI framework (K1–K9), chosen for collectability from the survey alone | The 58-row KPI system in `09_analysis/kpi_system/` (decision D12) |
| `ownly_transfer_scorecard.html` | Dashboard reading a v5 CSV export: 9 KPIs × 3 cities, with example/pilot/upload modes | `10_dashboard/decision_dashboard/ownly_decision_dashboard.html` |
| `hyderabad_survey_v3_final.md` | Hyderabad-only survey, 17 core questions | v5, then v6 |
| `hyderabad_survey_v4_final.md` | Hyderabad-only survey rebuilt around formula-sheet metrics | v5, then v6 |
| `Survey_v7_Questions.md`, `Survey_v7_Google_Form_Build_Guide.md`, `Survey_v6_to_v7_Conversion_Guide.md` | A leaner 8-section rewrite of v6 (decision D11) | **Not fielded.** D13 and D14: v6 is the live form. v7's cuts removed questions the KPI system depends on. |

## Two things worth keeping from the archived work

1. **The v5 pilot readout.** The 24-response pilot (15–16 Sep) is analysed inside
   `KPI_Framework_and_Survey_Validation.md` §7: only 11 of 24 respondents were in scope, there were no
   per-app order counts, and an unfilled placeholder was shown to respondents. Those findings are why the
   live form screens on age and city and asks for order counts.
2. **The v6 guide builds on v5.** `Survey_v6_Google_Form_Build_Guide.md` states "v6 = v5 + the H₀ instrument"
   and contains a "Part 12: upgrading an existing v5 form". If anyone needs the original v5 wording for that
   upgrade path, it is in this folder.
