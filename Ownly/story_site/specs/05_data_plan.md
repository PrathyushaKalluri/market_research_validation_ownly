# 05 · What data we needed, and how we got it

**Purpose:** show the instrument design — that each piece of evidence was chosen to answer a specific
question, and that we knew what each could not do.

> **How to use this file.** It defines *what information the screen carries and how that information
> should be drawn* — not the final look. Visual styling is decided separately (see `../research/
> design_system_references.md`). Every fact below is already verified against a file in this repo;
> the source is named next to it. If a number has no source line, it is not allowed on screen.


## What the viewer leaves with
- Six instruments, six jobs, six sample sizes.
- The research funnel: 124 responses → 40 analysable.

## Content inventory
| Instrument | n | What it produces | Source |
|---|---|---|---|
| Survey (Google Form, Hyd + Blr) | **124** received · 78 Hyderabad · 52 age-eligible · **40 catchment** (34 in Gachibowli proper) | Stated preference, switching price, funnel, trade-offs | `final_dashboard/data/survey_all_rows_with_flags.csv`, `funnel_research.csv` |
| Price audit at one address | 79 captures · 37 priced · **4 matched three-app baskets** · 10-restaurant frame | Observed price, fees, ETA, coverage | `06_competitor_audit/audit_data_slot1.csv` |
| Fake door (working app) | **70 sessions** · 34 direct · 36 from inside a ride app | Revealed choices under randomised prices | `FINAL_STORY/data/evidence.csv` F0 |
| Review mining | **836 coded**: 37 app-store · 524 social · 275 YouTube | Public voice, failure themes | `05_review_mining/` |
| Interviews | **1 documented transcript** (+ team-reported themes, count unknown) | Mechanism only — never a percentage | `04_interviews/interview_findings_coded.md` |
| Our own order | 1 order, 1 complaint, 1 refund | Lived service evidence | `assets/firsthand/` |

Also state: **Kondapur and Madhapur were options on the form and nobody chose them**
(`survey_all_rows_with_flags.csv`).

## Visuals
1. **Instrument cards** in a 3×2 grid; each card is a tiny diagram of the method (a form, a price tag,
   a phone, a speech bubble, a transcript, a receipt), with its n as the hero number.
2. **The research funnel** 124 → 78 → 52 → 40 as a four-step descending bar, each step labelled with
   what was removed.
3. **A coverage matrix** (instrument × question) showing which instrument answers which question —
   the honest version of "triangulation". Source: `final_dashboard/data/evidence_matrix.csv` (15 × 7).

## Motion
- Cards deal in like playing cards (stagger 80ms, slight rotation to 0).
- Funnel bars wipe down in order; the removed counts fly out sideways.
- Matrix cells fill in a diagonal sweep.

## Acceptance
- [ ] Every n matches the source file exactly
- [ ] The interview card visibly carries its weakness (count unknown)
