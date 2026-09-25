# final_dashboard — Ownly Gachibowli Market-Fit

A 14-tab executive dashboard built from the project's real primary data. Every number is computed by
the scripts in `scripts/` and read from `data/` at build time — nothing on the page is hand-typed.

**Start here:** `index.html` (open in any browser) · `EXECUTIVE_SUMMARY.md` (2 pages) ·
`Ownly_Gachibowli_GTM_Dashboard.pdf` (all tabs, print layout).

---

## 1. What was built

| Deliverable | Path |
|---|---|
| Interactive dashboard, 14 tabs | `index.html` (self-contained, no server, no CDN) |
| Print/PDF version | `Ownly_Gachibowli_GTM_Dashboard.pdf` |
| Per-tab images | `exports/01…14_*.png` |
| Repository audit | `00_repo_inventory.md` |
| Data-quality register | `DATA_QUALITY_NOTES.md` |
| Headline traceability | `SOURCE_MAP.md` |
| Executive summary | `EXECUTIVE_SUMMARY.md` |
| Analysis pipeline | `scripts/01…06` |
| Datasets | `data/*.csv` (21 files) |
| Interview coding | `../04_interviews/interview_findings_coded.md` |

## 2. Dashboard structure

| # | Tab | Answers |
|---|---|---|
| 01 | Business problem | What is the problem, in 30 seconds |
| 02 | KPI driver tree | Input → behaviour → output, grouped by what Ownly controls |
| 03 | Marketing metrics | 10 derived metrics + what is *not* estimable |
| 04 | The ₹30 equation | What users will and will not trade for ₹30 |
| 05 | Price-to-switch fit | Required saving vs observed saving |
| 06 | Market reality | Price vs ETA, bill composition, the two-step erosion |
| 07 | Assortment & availability | Coverage, overlap, exclusives, dayparts |
| 08 | Awareness → trial | Funnel, and distribution vs discovery |
| 09 | Trial vs retention risk | Intent gap, coded themes, the reliability reconciliation, respondent voice |
| 10 | Why challengers fail | 5 mechanisms scored against our own evidence |
| 11 | Evidence triangulation | 14 dimensions × 7 evidence types |
| 12 | Propositions | 5 GTM territories with evidence for and against |
| 13 | GTM decision | KEEP / ADAPT / DEPRIORITISE + what to test next |
| 14 | Hypothesis decision | H₀, the stated-preference proxy, and P1–P5 |

Keyboard: ← → move between tabs. Tab state is kept in the URL hash.

## 3. How to run

```bash
python3 -m venv .venv && ./.venv/bin/pip install pandas numpy scipy Pillow

cd final_dashboard/scripts
../../.venv/bin/python 01_clean_survey.py              # raw -> cleaned / excluded
../../.venv/bin/python 02_audit.py                     # audit -> 3 price views, matched pairs
../../.venv/bin/python 03_kpis_metrics_hypotheses.py   # KPIs, metrics, H0, P1-P5
../../.venv/bin/python 04_themes_evidence_dictionary.py# themes, evidence matrix, dictionary
../../.venv/bin/python 07_youtube_comments.py          # code YouTube comments into themes
../../.venv/bin/python 05_build_dashboard.py           # -> ../index.html
../../.venv/bin/python 06_export.py                    # -> ../exports/*.png + PDF (needs Chrome)
```

Scripts 01–05 need only pandas/numpy/scipy. 06 needs Pillow and Google Chrome.

## 4. Source datasets

| Source | Type | n | Used for |
|---|---|---|---|
| `Ownly Survey.csv` (from the supplied zip) | SURVEY — primary | 113 raw → 75 cleaned | Tabs 1, 3–5, 8, 9, 13, 14 |
| `06_competitor_audit/audit_data_slot1.csv` | PRIMARY OBSERVED | 79 rows, 37 priced | Tabs 3, 5–7 |
| `05_review_mining/app_stores/reviews_coded.csv` | CONSUMER-GENERATED | 37 | Tab 9 |
| `05_review_mining/social/social_coded.csv` | CONSUMER-GENERATED | 524 | Tab 9 |
| `04_interviews/interview_findings_coded.md` | INTERVIEW (primary) | 1 documented + team-reported | Tabs 8, 9, 11, 13 |
| `05_review_mining/youtube/*_comments.json` | CONSUMER-GENERATED (verbatim) | 275 comments | Tabs 9, 10 |
| `01_secondary_research/challenger_failures/` | Secondary, 5 dossiers | ~230 sources | Tabs 1, 10 |

**Not used:** `Marketing Metrics 1000 Records.csv` (generic campaign data, not Ownly);
the two existing dashboard prototypes (they carry DEMO DATA); archived v1/v2 material.

## 5. Analysis population

| Population | Definition | n |
|---|---|---|
| **`HYD_ELIGIBLE`** — primary | Hyderabad, age-eligible (20–35) | **46** |
| `HYD_CATCHMENT` | of those, inside the Gachibowli catchment | 37 |
| `HYD_STRICT_20_30` | bands 20–24 + 25–29 only | 39 |
| `BLR_ELIGIBLE` | Bengaluru | 12 — context only |
| `OTHER` | other cities | 17 — context only |

**Hyderabad and Bengaluru are never blended.** See `DATA_QUALITY_NOTES.md` DQ1 on the 20–30 vs 20–35
scope conflict — it is unresolved and every figure is labelled 20–35 for that reason.

## 6. Cleaning performed

RAW is never modified. 113 raw → **75 cleaned**, **38 excluded** (all screened out by the instrument's
own age routing; `exclusion_reason` recorded per row in `data/excluded_survey.csv`).
The three branched question blocks were harmonised to one respondent-level frame.
No imputation anywhere; missing stays missing. Documented interventions: DQ3 (Zomato dual capture),
DQ4 (duplicate restaurant name), DQ6 (one ₹0 bill field voided, respondent retained),
DQ7 (₹1,200 cake basket excluded from one chart). All in `DATA_QUALITY_NOTES.md`.

## 7. KPI definitions

32 KPIs across INPUT (price, assortment, service, distribution, lock-in) and OUTPUT (funnel,
retention, trade-off) layers. Full definitions — business question, formula, numerator, denominator,
source, population, sample size, evidence type, limitations, interpretation rule — in
`data/metric_dictionary.csv` (43 rows). **No KPI appears on the dashboard without an entry there.**

## 8. Marketing metrics

Ten derived metrics in `data/marketing_metrics.csv`. Eight are standard; **two are our own**:

- **MM4 Membership Erosion Rate (25%)** — baskets Ownly wins on list price but loses once the
  incumbent *membership benefit alone* applies, before any coupon. Good indicator because a
  membership is a **standing** benefit applying to every order, whereas a coupon is episodic — so
  this isolates the durable half of the erosion. Directly actionable: it is the part of the gap that
  Ownly cannot out-wait.
- **MM10 Fee Load Advantage (18.2pp)** — median incumbent non-food share of bill minus Ownly's. Good
  indicator because it is the one advantage Ownly controls outright: it survives without subsidy
  (unlike a discount) and it is invisible unless stated — which ties the metric to the communication
  problem the dashboard identifies.

## 9. Statistical methods

Wilson score intervals for proportions · exact binomial for the H₀ forced choice · McNemar exact for
paired binary comparisons (the ₹30 trade-offs, P-vs-Q intent) · Spearman ρ for ordinal association ·
medians with the distribution shown for skewed data. Segmentation is limited to pre-specified cuts;
no fishing. Small bases are labelled **DIRECTIONAL — LOW BASE** rather than given false precision.
No ML models — none would be defensible at n=46.

## 10. H₀ result

**Behavioural H₀: NOT DIRECTLY TESTED** — the fake door was never fielded (0 events).
**Stated-preference analogue: FAIL TO REJECT** — Service P 18 vs Q 15, exact binomial p = 0.7283,
95% CI 36.1–71.7%; McNemar on paired top-2 intent p = 1.0. 13 of 46 could not choose between the
bundled propositions. The attribute-level trade-offs inside the propositions *did* separate
(assortment vs speed, p = 8×10⁻⁶), which is where the decision value lies.

## 11. Key insights

1. The price advantage is structural (fee removal), not rented — genuinely different from Foodpanda.
2. It erodes in two steps: membership alone flips 25% of baskets, coupons flip 50%.
3. **Assortment is the binding constraint.** ₹30 buys speed and reliability; it cannot buy restaurants.
4. 90.9% assortment overlap — Ownly sells the same catalogue, ~17 minutes slower.
5. Rapido delivers access, not discovery: 84.6% gap.
6. 89.1% expect the low prices to rise; stated post-offer continuation is 34.8%.
7. **Rider economics is the single largest theme in public comment** (27.6% of coded YouTube
   comments, 1,167 likes) — a supply-side sustainability risk the survey and audit cannot see.
8. Interviews reframe two conclusions: reliability is a **churn** driver not a trial blocker, and
   discovery runs on **word of mouth**, not in-app placement.

## 12. GTM recommendation

**KEEP** the fee architecture and transparent everyday pricing.
**ADAPT** the price claim (away from a comparison coupons can falsify), the supply goal (breadth →
named local depth) and Rapido's role (access → measured discovery).
**DEPRIORITISE** ETA-parity spending and deeper first-order discounts.
Full reasoning on tab 13.

## 13. Limitations

Interviews: only **one** documented transcript, total count **UNKNOWN**, Gemini auto-notes not
human-verified, no double-coding — so no interview finding carries a prevalence figure.
Survey n=46 from a self-selected distribution, not a probability sample — **no result generalises to
Gachibowli or Hyderabad**. Audit is n=4 matched baskets, one slot, one address, with Ownly on a new
account and incumbents on subscribed accounts. Review and social bases are self-selected toward
complaint and are reported as shares of coded items, never as failure rates. All switching, trial and
repeat figures are **stated intent**. Secondary research is ~74% media report or company claim.
Historical challenger cases are **analogies, not causal proof**.

## 14. Unresolved unknowns

CAC · CLV · true retention · market share · EBITDA / contribution margin / burn per order for Ownly ·
actual delivery time vs quoted ETA · behavioural first-order conversion · restaurant-side economics in
Hyderabad · whether the ₹0 delivery fee is a launch condition or steady state.
Listed on tab 03 and in `data/not_estimable.csv`. **No proxy was substituted for any of them.**

**One open decision blocks a scorecard dimension:** SRI is not computable from the live form (two of
three components absent). Options in `../09_analysis/SRI_options_decision_memo.md`. Because no option
has been chosen, **no composite scorecard total is shown anywhere in this dashboard** — displaying one
would mean silently picking an option.

## 15. What a real company would test next

1. **The fake door** — the only route to behavioural first-order conversion, which is what H₀ asks.
2. **A named-local-restaurant audit**, not showcase chains — the strategy depends on depth we have not
   measured.
3. **Test orders** for promised-vs-actual delivery time.
4. **Document and complete the interviews.** Some were conducted; the count is UNKNOWN, the tracker
   is empty and no quote is human-verified yet.
5. **A membership-account re-audit** — 83% of the target sees that view, not the list-price view.
6. **A held-out pricing cell**: does removing the intro offer change trial? That is the M1 question,
   and nothing in this study answers it.

---

### A note on fabrication

No respondent data, traffic, conversion, order, price, ETA or business metric was simulated,
imputed or fabricated at any point. Where a figure could not be computed it is shown as
**NOT ESTIMABLE FROM AVAILABLE EVIDENCE**. The dashboard contains no scenario modelling.
