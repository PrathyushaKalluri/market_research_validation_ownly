# Decision Dashboard Blueprint (v6 + A1–A3)

**Version:** 1.0 · 2026-09-17 · Replaces the 2026-09-14 blueprint (`10_dashboard/dashboard_blueprint.md`, built for the retired
choice-experiment survey). The old file stays as history.
**Build:** `ownly_decision_dashboard.html`, a single file. It runs in the browser and loads 4 CSVs (survey, audit, frame,
fake-door events). It shows **labelled demo data** until real files are loaded.
**Why HTML rather than Looker Studio:** no licence or login; the CSV → KPI logic lives in one auditable place; it works
offline for the viva. The Looker route in the old `build_instructions.md` still works if the team prefers it.

## Global rules
1. Every chart shows: **question answered · source · n · segment · interpretation · implication**.
2. Every number carries an evidence label: Observed / Self-reported / Stated / Association / External / Project proxy.
3. The demo-data badge sits on every page until real data is loaded for that dataset. Each dataset has its own status.
4. Values with n < 10 are hidden; n < 30 is flagged "low base".
5. External figures always show source and date, and are never styled like our primary KPIs.
6. Filters (city, occupation, Rapido user) sit in one row and apply to every survey chart. Audit and fake-door charts say
   when a filter doesn't apply.

## Pages

| # | Page | Question answered | Main data |
|---|---|---|---|
| 1 | Executive Decision Cockpit | Replicate or adapt the Bengaluru playbook in Gachibowli? | All |
| 2 | Bengaluru Playbook | What exactly are we trying to transfer? | External + Bengaluru survey |
| 3 | Hyderabad Market | Who will switch and why? | Survey (Hyderabad) |
| 4 | First Order vs Second Order | Does price get the first order and reliability earn the second? | Survey |
| 5 | Is Ownly Actually Cheaper? | Is affordability real and repeatable? | Audit |
| 6 | Can the Marketplace Deliver? | Can supply and fulfilment support repeat use? | Frame, audit, survey A3, reviews |
| 7 | Rapido Distribution Advantage | Does Rapido lower Ownly's discovery barrier? | Survey A1, S10–12-Q1, fake door |
| 8 | Promotion: Growth or Rented Demand? | Do offers create retained demand? | Survey S7-Q5, A2, S9-Q1 |
| 9 | Segment Prioritization | Which segment should Hyderabad GTM enter through? | Survey |
| 10 | Final Proposition / GTM Decision | KEEP / ADAPT / DROP, H₀ call, next validation | All + decision rules |

Chart-level detail: `chart_specifications.md`. Data contract: `dashboard_data_schema.csv`. Narrative: `dashboard_storyline.md`.
KPI definitions: `09_analysis/kpi_system/`.
