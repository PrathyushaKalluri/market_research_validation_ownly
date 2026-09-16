# project_context.md — stable facts

**Canonical as of 2026-09-16.** This file holds only things that do not change week to week.
Live state: `progress.md` · current direction: `direction.md` · reasoning: `decisions.md`.
Historical v2 context (14 Sep and earlier) stays at `../../context.md`.

## The team
Four members. **Person 1 — Data / Research · Person 2 — User Research · Person 3 — Experiment / GTM ·
Claude — execution lead** (planning, instrument design, analysis, artefacts, tracking).
All three humans distribute the survey. Humans own anything requiring a person: talking to respondents,
building and testing forms, taking platform screenshots, checking live prices and ETAs, distribution.

## The business question
> **Can Ownly transfer its Bengaluru growth playbook to 20–30-year-old food-delivery users in
> Gachibowli, and which parts must be adapted for Hyderabad to drive trial and repeat usage?**

Not "should Ownly enter Hyderabad" — Ownly is already live there. The decision is per-tactic:
**KEEP / ADAPT / DROP.**

## The hypothesis
- **H₀:** Among 20–30-year-old food-delivery users in Gachibowli, a Bengaluru-style Ownly proposition
  does **not** produce a significantly different first-order conversion rate from a Hyderabad-localized
  proposition.
- **H₁:** The first-order conversion rates are different.

**H₀ is never silently changed.** Any proposed change goes to `decisions.md` with its reason first.

## The diagnostic proposition under test
> **Price may acquire the customer; reliability may retain the customer.**

## The Bengaluru playbook — frozen definition (Jul–Aug 2026 framing)
**Consumer:** lower final bill · transparent pricing · no/low platform, packaging and surge fees ·
everyday affordability rather than coupon-led discounting · discovery through Rapido · gamified
first-order incentives.
**Supply:** restaurant-friendly economics · large-scale onboarding · local/regional assortment ·
low/zero commission.
**Distribution:** Ownly inside the Rapido app · leverage Rapido's user base · geographic density first.
*Pilot-era fee structures are never mixed with current positioning without marking the period.*

## Target and scope
20–30-year-old students and working professionals in **Gachibowli** and the surrounding catchment
(Financial District / Nanakramguda, Kondapur, Madhapur / HITEC City, Manikonda, Narsingi / Kokapet,
Serilingampally, Tellapur / Nallagandla). Bengaluru is the **benchmark** market. Other cities are
exploratory context only.

## The three cities' research roles — fixed
| City | Role | Never used for |
|---|---|---|
| **Hyderabad** | Primary validation. Deepest questionnaire. | — |
| **Bengaluru** | Benchmark: what actually acquired and retained in the originating market | The Hyderabad H₀ |
| **Other city** | Short exploratory context | Hyderabad validation, demand estimates, Bengaluru benchmarking |

**Never produce a blended all-city metric.** Geography is preserved as a segmentation field end to end.

## Execution targets (targets, not representativeness claims)
| Instrument | Target |
|---|---|
| Survey — Hyderabad | 80–100 usable |
| Survey — Bengaluru | 15–30 usable |
| Interviews | 8 (4 students, 4 working professionals) |
| Fake door | 80+ unique visitors, 30+ per arm |
| Price audit | 10 restaurants × 3 platforms × 2 slots = 60 captures |
| Test orders | 3 (₹900 budget) |
| Polls | 3 polls, 50–60+ votes each |

## Standing rules (carried forward, unchanged)
- **Evidence labels on every claim:** FACT / COMPANY CLAIM / MEDIA REPORT / CONSUMER-GENERATED /
  HYPOTHESIS / INTERPRETATION / ASSUMPTION / UNKNOWN.
- **Survey order:** unaided behaviour and pain → brand-blind concept → brand reveal. Never the reverse.
- Intent ≠ behaviour. Reviews ≠ population. Bengaluru ≠ Hyderabad. Student ≠ professional.
  Correlation ≠ causation. Statistical significance ≠ business significance.
- A low-price proposition is validated only when people **trade something** for it.
- **Never fabricate** CAC, CLV, EBITDA, market share, retention or profit. Label everything else
  `sample` / `stated` / `proxy` / `experimental`.
- Data handling: RAW / CLEANED / EXCLUDED with an `exclusion_reason`. Nothing deleted silently.
- Contradictions are shown, not hidden.
- Ethics: no data collection from people before written instructor approval. No circumventing logins,
  robots.txt or terms. No impersonation of Ownly or Rapido — the fake door is unbranded.
- AI never generates or simulates respondent data. Synthetic dashboard data is labelled
  **DEMO DATA — REPLACE WITH REAL DATA** and never mixed with real data.
- Pre-registration: thresholds and tests are fixed **before** the data arrives, and any deviation is logged.

## Course deliverable
A dashboard carrying: business problem · KPIs driving business inputs and outputs · 3–7 derived
marketing metrics · analysis through strong visuals · propositions/decisions · the reasoning ·
the **H₀ decision based on evidence**.
