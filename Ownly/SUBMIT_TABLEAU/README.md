# Ownly Gachibowli — Tableau Workbook

**Open `Ownly_Gachibowli_BI.twbx`.** It was built and verified against
Tableau Desktop 2026.2 on this machine — it opens with no errors and the data
connects automatically, because all 28 CSVs are packaged inside the `.twbx`.

---

## What is here

Two renderings of the same analysis, from the same data.

| File | What it is |
|---|---|
| **`consolidated_dashboard.html`** | **The consolidated dashboard** — all five sections in one page: every Tableau visualisation *plus* the Python-only ones. Open in any browser, no internet needed |
| `Ownly_Gachibowli_BI.twbx` | **The Tableau workbook** — 31 worksheets, 5 dashboards, data packaged inside |
| `Ownly_Gachibowli_BI.twb` | The same workbook unpackaged (XML), if you want to inspect it |
| `Data/` | 46 tidy CSVs — the single source both renderings read |
| `build_tableau_data.py` | Reshapes the analysis output into the CSVs in `Data/` |
| `build_workbook.py` | Declares every Tableau worksheet and dashboard |
| `twb_gen.py` | Generates the Tableau XML and packages the `.twbx` |
| `build_consolidated.py` | Bundles `Data/*.csv` into `consolidated_data.js` for the HTML |
| `consolidated_app.js`, `lib.js` | The HTML dashboard's rendering code and chart library |

**The two cannot drift apart.** The HTML reads `consolidated_data.js`, which is generated
from the identical CSVs the `.twbx` is built on. Change the data and rebuild — both update.

To regenerate everything after the underlying data changes:

```
cd ../SUBMIT_BI  && python3 build_data.py        # re-runs the analysis
cd ../SUBMIT_TABLEAU
python3 build_tableau_data.py                    # rebuilds Data/*.csv
python3 build_workbook.py                        # rebuilds the .twbx
python3 build_consolidated.py                    # rebuilds the HTML's data
```

---

## The consolidated dashboard

Five sections, exactly as briefed — **Problem Statement · KPIs · Marketing Metrics ·
Analytics · Propositions** — holding **46 cards, 30 charts and 14 tables**.

Every card carries a badge saying where that visual lives:

| Badge | Meaning |
|---|---|
| **Tableau 4.6** | This exact chart is worksheet 4.6 in the `.twbx` |
| **Tableau 4.1 · Python-computed** | The chart is in Tableau, but a value on it (a p-value, a confidence interval, a fitted curve) was computed in Python |
| **Python only** | Not in the Tableau workbook — the data is in `Data/`, so you can build it there if you want it |

24 cards are Tableau visualisations; 22 are Python-only analyses that extend the workbook
(correlation matrix, associations, theme co-occurrence, verbatims, profiling tests,
hypothesis register, data-quality register, full audit table, unit-economics provenance,
sentiment mix by month, theme volume-vs-sentiment).

---

## The five dashboards

Exactly the structure asked for — nothing else is on them.

| # | Dashboard | Worksheets |
|---|---|---|
| 1 | **Problem Statement** | Business problem · research funnel · analytics applied |
| 2 | **KPIs** | Headline KPIs · adoption funnel · KPI coverage · KPI detail |
| 3 | **Marketing Metrics** | 10 computed metrics · 10 marked NOT ESTIMABLE |
| 4 | **Analytics** | ₹30 trade-off · price erosion · demand curve · theme families · sentiment by source · sentiment over time · evidence triangulation · switcher profiling |
| 5 | **Propositions** | KEEP/ADAPT/DEPRIORITISE · lever sensitivity · break-even · why challengers fail |

A further 13 worksheets (price by platform, bill composition, TF-IDF terms,
city benchmark, restaurant coverage, delivery gap, review ratings, segment
scorecard, paired tests, sentiment validation and others) are built and ready —
drag any of them onto a dashboard if you want it there.

---

## The honest split: what Tableau does, and what it cannot

This is the answer to give if you are asked.

**Tableau draws every single chart in this workbook natively.** No images, no
screenshots, no extensions.

**Tableau cannot *compute* five things**, so Python computed them and they are
stored as ordinary columns in the CSVs:

| Computed in Python | Why Tableau cannot | Where it lands |
|---|---|---|
| Logistic demand curve, R² = 0.964 | Tableau trend lines are linear, log, exponential, polynomial, power — **there is no logistic option** | `11_demand_curve.csv` → sheet 4.6 |
| Sentiment scores on 836 documents | Tableau has no NLP of any kind | `15`, `16b`, `17` → sheets 4.7, 4.8, 4.10 |
| TF-IDF term salience | Same | `18_tfidf_terms.csv` → sheet 4.11 |
| McNemar exact, Fisher exact p-values | Require combinatorics; not expressible in Tableau's calculation language | `05`, `27b` → sheets 4.2, 4.15 |
| Wilson confidence intervals | *Could* be a calculated field — it is only algebra — but pre-computing keeps one source of truth | `01`, `04`, `10` |

That division — **Python models, Tableau visualises** — is how BI teams
actually work. Tableau connects to a prepared extract; the modelling happens
upstream. `build_tableau_data.py` is that upstream layer.

**One thing Tableau does better than the HTML workbook:** dashboard actions.
Add a filter action on any dashboard and clicking a bar will cross-filter the
others natively.

---

## Two minutes of polish worth doing

The generator sets sensible default marks. Four sheets look noticeably better
after a couple of clicks:

| Sheet | Do this |
|---|---|
| **4.9 Theme Families** | Marks card → change **Bar** to **Square**, drag `Documents` to **Size** → it becomes a treemap |
| **4.7 Sentiment by Source** | Right-click the `Pct Of Source` axis → Add Table Calculation → **Percent of Total** → a clean 100% stacked bar |
| **4.12 Evidence Triangulation** | Marks card → **Square**; click Colour → edit colours → red-green diverging |
| **4.5 Bill Composition** | Same percent-of-total table calc as 4.7 |

Everything else renders correctly as generated.

---

## If a chart ever loses its data

The CSVs live inside the `.twbx`. If you unpack it or move files, point the
connection at the `Data/` folder in this directory — every file is there.

---

## Data dictionary

46 CSVs in `Data/`, all long-format where a chart needs a colour dimension, with
sort orders pre-baked as integer columns so Tableau does not sort alphabetically.

| Group | Files |
|---|---|
| Problem & method | `39_problem_statement`, `10_funnels`, `37_analytics_layers`, `34_evidence_matrix_long`, `35_hypotheses`, `36_data_quality` |
| KPIs & metrics | `01_kpi_summary`, `02_marketing_metrics`, `03_not_estimable` |
| Survey | `06_survey_respondents`, `06b_orders_by_platform_long`, `04_tradeoffs`, `05_tradeoff_tests`, `28_segment_cuts_long`, `28b_segment_tradeoffs`, `26_correlations_long`, `26b_associations` |
| Price audit | `07_price_audit_pairs`, `07b_price_by_platform_long`, `08_bill_composition_long`, `09_price_erosion`, `22_coverage_long`, `23_eta_by_platform_long` |
| Predictive | `11_demand_curve`, `11b_demand_curve_fit`, `27_switcher_profiling`, `27b_profiling_tests` |
| Text analytics | `14_theme_families`, `14b_themes_detail`, `15_text_trend_monthly`, `15b_text_trend_long`, `16_sentiment_by_source`, `16b_..._long`, `17_sentiment_validation`, `17b_..._stat`, `18_tfidf_terms`, `19_theme_cooccurrence`, `20_verbatims`, `21_review_stars` |
| Economics | `30_econ_benchmarks`, `31_breakeven_grid_long`, `31b_breakeven_summary`, `32_lever_sensitivity` |
| Competitive & output | `24_city_benchmark_long`, `25_challenger_failure_modes`, `38_propositions` |

---

*Built 2026-09-21 · verified against Tableau Desktop 2026.2 · 28 datasources ·
31 worksheets · 5 dashboards · all field and filter references validated.*
