# 04 · From a question to a hypothesis

**Purpose:** show the funnel of thinking — broad question → market → segment → falsifiable H₀ — and what
would prove us wrong.

> **How to use this file.** It defines *what information the screen carries and how that information
> should be drawn* — not the final look. Visual styling is decided separately (see `../research/
> design_system_references.md`). Every fact below is already verified against a file in this repo;
> the source is named next to it. If a number has no source line, it is not allowed on screen.


## What the viewer leaves with
- We narrowed deliberately, and we wrote down in advance what would falsify us.

## Content inventory
| Stage | Content | Source |
|---|---|---|
| Broad question | Does a zero-commission, no-platform-fee model transfer to a new city? | `00_research_charter/` |
| Market | Hyderabad, because Ownly launched here ~2 weeks before fielding | `_ops/decisions.md` |
| Place | The Gachibowli catchment — one delivery address (DP1) for every price capture | `06_competitor_audit/audit_data_slot1.csv` |
| People | 20–35, students and working professionals | survey screen, `final_dashboard/data/survey_all_rows_with_flags.csv` |
| H₀ | The Bengaluru proposition (P) and a Hyderabad-localised proposition (Q) are equally preferred | `09_analysis/kpi_system/decision_rules.md` §1 |
| Primary test | Survey forced choice (K14); the fake door reports as directional | same file, decision D3 |
| Result | P 18 · Q 11 · can't choose 11 → **fail to reject H₀**, p = 0.2649 | `final_dashboard/data/hypothesis_results.csv` |
| Pre-registration | Analysis plan frozen with a SHA-256 before analysis | `_ops/decisions.md` D18 |

## Visuals
1. **A narrowing funnel drawn as a physical funnel**, four stages, each stage labelled with what was
   excluded and why. Not a bar chart — a shape that literally narrows.
2. **The H₀ card**: P / Q / can't choose as three columns, with the p-value and the verdict stamped
   across them. Design the "fail to reject" stamp carefully — it is a real finding, not a failure.
3. **The freeze**: the PAP SHA-256 shown as a small monospace seal with its date.

## Motion
- The funnel narrows as you scroll (each stage's width tweened, scrubbed).
- The H₀ columns rise, then the stamp lands with a short overshoot.

## Honesty rules
- "Fail to reject" must never be written as "the two are the same". Use the decision-rules wording:
  *"no evidence the two differ"*.

## Acceptance
- [ ] Every exclusion at each funnel stage is stated with its n
- [ ] The p-value appears with its test name
