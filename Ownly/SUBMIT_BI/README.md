# Ownly Gachibowli — BI Workbook

An interactive, Tableau-style analytics workbook built from the project's primary data.
**Open `index.html` in any browser.** No server, no internet, no install.

---

## The four files

| File | What it is |
|---|---|
| `index.html` | The application — open this |
| `app.js` | Worksheets, filters, scenario model |
| `lib.js` | Charting library (19 chart types, hand-rolled SVG) |
| `bi_data.js` | All analysis output, generated — **do not edit by hand** |
| `build_data.py` | The analysis engine. Re-run it to regenerate `bi_data.js` |

To rebuild after the underlying CSVs change:

```
python3 build_data.py
```

It needs no packages — numpy, pandas, scipy and sklearn are not installed on this
machine, so every statistic is implemented from scratch in the standard library.

---

## How to drive it

- **Seven worksheets** in the left rail.
- **Five global filters** (segment, membership, multi-homing, Rapido use, awareness).
  They cross-filter every survey-based chart at once. Audit, text and benchmark charts
  are not respondent-level and deliberately do not filter — each card says so.
- **Hover any mark** for a tooltip with the underlying numbers.
- **Click a column header** to sort that table.
- **Predictive & Scenarios** has eight live sliders; every output recomputes as you drag.
- **Print** (Cmd/Ctrl-P) hides the sidebar and lays the cards out for PDF.

---

## What is in each worksheet

| # | Worksheet | Answers |
|---|---|---|
| 1 | Executive overview | The decision, the evidence, the constraint underneath it |
| 2 | Price & value | What Ownly charges, how the advantage is built, where it erodes |
| 3 | Demand & segments | What the catchment will trade, and how subgroups differ |
| 4 | Voice of customer | 836 documents, 16 months — sentiment, themes, vocabulary, verbatims |
| 5 | Competitive position | Assortment overlap, Bengaluru benchmark, challenger failure record |
| 6 | Predictive & scenarios | Fitted demand curve, profiling, break-even, live simulator |
| 7 | Method & evidence | Triangulation, hypothesis register, not-estimable, confidence grading |

---

## Analytics layers, and the honest confidence on each

| Layer | Technique | Confidence |
|---|---|---|
| **Descriptive** | Proportions with Wilson intervals, funnels, distributions, box plots, share of wallet | High |
| **Diagnostic** | McNemar exact (paired), Fisher exact, Spearman correlation, waterfall decomposition, fee attribution | High on the headline result; null elsewhere and reported as such |
| **Predictive** | Logistic price-response curve (Gabor-Granger), **R² = 0.964** on 6 observed points | Good inside ₹10–₹100; extrapolation above ₹100 drawn dashed |
| **Predictive** | Switcher profiling by lift + Fisher tests | **Exploratory only** — n = 40 cannot support a classifier |
| **Predictive** | Sentiment and volume trend across 16 months | Descriptive trend; no forecast claimed |
| **Prescriptive** | Scenario simulator, tornado sensitivity, break-even solve | Assumption-driven and user-adjustable by design |
| **Text / cognitive** | Lexicon sentiment, negation- and intensifier-aware | **Validated: ρ = 0.648 against star ratings, p < 0.001** |
| **Text / cognitive** | TF-IDF term salience, rule-based theme roll-up, co-occurrence | Light topic modelling |

**Deliberately not attempted:** time-series forecasting (no transactional history exists),
classification with a train/test split (n = 40 cannot support it), market-share modelling
(no credible market-size denominator exists for Gachibowli food delivery). Claiming any of
these would have been decoration rather than analysis.

---

## Chart types implemented

KPI cards · horizontal bar with confidence whiskers · grouped bar · 100% stacked bar ·
waterfall · funnel with drop-off · line · area · scatter with fitted curve · bubble ·
heatmap (correlation, matrix, categorical) · treemap · box plot with Tukey outliers ·
histogram · donut · slope chart · tornado · dumbbell/lollipop · bullet with target marker ·
sortable tables.

*No map:* the audit covers a single delivery address, so there is no geography to plot.
*No dual-axis:* two y-scales on one frame is a known misreading hazard; paired charts are
used instead.

---

## Unit economics — the boundary

Every **observed** number in this workbook comes from the project's own data and is sourced
on the card that displays it.

The unit-economics layer is different, and is labelled wherever it appears. Only figures
that are **FACT-grade and common across the domain** were adopted:

| Benchmark | Value | Grade | Source |
|---|---|---|---|
| Rider payout per order | ₹56.01 | FACT | Swiggy Corporate Deck FY24-25 |
| Food-delivery AOV | ₹458 (FY25) | FACT | Swiggy Corporate Deck FY24-25 |
| A&SP per order (CAC proxy) | ₹33.20 | CALCULATED | Zomato DRHP |
| Steady-state margin ceiling | 5–6% of NOV | FACT | Eternal & Swiggy shareholder letters |
| Years to EBITDA break-even | 16 | FACT | Eternal disclosures |
| Uber Eats India loss per order | −$2.55 on $2.45 AOV | DERIVED from SEC filings | Uber SEC filings |

**CAC was deliberately excluded.** The project's own secondary research concludes there is
no credible, dated, primary-sourced CAC figure for Indian food delivery in the public
domain — neither DRHP discloses it. Advertising & sales promotion per order is used as the
named defensible proxy instead.

**Ownly's own ₹30 revenue per order is MEDIA-reported and contested** across three outlets,
and our own Gachibowli audit observed ₹0 charged to the customer. It is used only as the
optimistic bound in the simulator.

---

## The finding the economics layer surfaces

At the only revenue figure ever reported for Ownly (**₹30 per order**) and the industry's
disclosed rider payout (**₹56.01**), contribution is **−₹26.01 per order** before any
marketing, support or overhead. Revenue per order must rise **~87%** simply to reach zero.

While contribution per order is negative, **growth makes losses larger, not smaller** —
every volume lever in the simulator moves monthly contribution down. Only the revenue and
cost levers can change the sign. This is the mechanism that ended Uber Eats India.

---

*Built 2026-09-21. Survey n = 40 in catchment (124 received) · price audit 4 matched baskets
across a 10-restaurant frame · 836 public documents across 16 months · fake-door experiment
designed, powered and not fielded.*
