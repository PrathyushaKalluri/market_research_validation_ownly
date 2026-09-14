# Scenario & Illustrative KPIs (computable now; NOT survey/audit findings)
Generated 2026-09-14 by lead. Every input is labelled. Formulas are from the course sheets (`Formulae Sheet (1).docx`, `Formulae Sheet 2.pdf`).

## 1. Growth: compound monthly growth rate of Ownly Bengaluru daily orders
Formula (CAGR adapted to months): (Final ÷ Start)^(1/N) − 1 = (50,000 ÷ 5,000)^(1/5) − 1 = **58.5% per month**.

- Inputs: ~5,000/day (Mar 2026) and ~50,000/day (Aug 2026). **MEDIA REPORT, single upstream source.** Month count approximate.
- YoY growth: **not computable** (less than 12 months of history).
- Sensitivity: if the start figure were 10,000/day, CMGR = 38.0%; if N = 6 months, CMGR = 46.8%.

## 2. Contribution per order and break-even (Ownly platform view) — ASSUMPTION scenario
Formulas: Contribution per unit = Selling price per unit − Variable cost per unit; Break-even volume = Fixed costs ÷ Contribution per unit.

Assumptions (all labelled **ASSUMPTION**, none verified):
- Ownly's revenue per order ≈ the delivery fee paid by the customer, excluding GST. Restaurants pay zero commission (MEDIA REPORT / COMPANY CLAIM).
- Variable cost per order = rider payout + ₹5 (payment gateway, support, other). Rider payout is **UNKNOWN**, so three levels are shown.
- No ad or other revenue is included. If Ownly earns any, contribution rises.

| Delivery fee ₹ \ Rider payout ₹ | ₹30 | ₹45 | ₹60 |
|---|---|---|---|
| ₹0 | -35 | -50 | -65 |
| ₹15 | -20 | -35 | -50 |
| ₹30 | -5 | -20 | -35 |
| ₹45 | +10 | -5 | -20 |

**Reading:** at the reported fee levels (₹0–₹30), contribution per order is negative unless rider payout is under ₹25. Break-even volume therefore doesn't exist (you can't break even by selling more units at a negative contribution).
**INTERPRETATION:** this is consistent with users' scepticism that prices will last (37 social items), and with a second-hand, unverified "₹150–170 cash burn per order" claim. It is a scenario, not a finding.

If contribution were positive, e.g. fee ₹45 with a ₹30 rider payout (+₹10/order): break-even volume = monthly fixed costs ÷ ₹10. For every ₹1 crore of monthly fixed cost, that is 10,00,000 orders a month (~33,000/day).

## 3. Customer lifetime value — ASSUMPTION scenario (why retention matters)
Formula (Formulae Sheet 2): CLV = Margin × r ÷ (1 + d − r), with monthly margin, monthly retention r and monthly discount rate d = 1%.

| Monthly margin per customer ₹ \ Monthly retention r | 40% | 60% | 80% | 90% |
|---|---|---|---|---|
| ₹20 | ₹13 | ₹29 | ₹76 | ₹164 |
| ₹50 | ₹33 | ₹73 | ₹190 | ₹409 |
| ₹100 | ₹66 | ₹146 | ₹381 | ₹818 |

**Reading:** going from 60% to 90% monthly retention multiplies CLV by about 6×, while doubling the margin only doubles it. **INTERPRETATION:** if reliability failures drive churn (as public posts suggest), fixing reliability is worth more than extra discounts. Replace r with the survey's repeat-rate proxy only if there are at least 10 Ownly triers.

## 4. Metrics toolkit appendix — `Marketing Metrics 1000 Records.csv` (NOT Ownly data)
Generic digital-campaign dataset: 2024-01-01 to 2025-05-14, USD, 8 channels, 4 regions, 1,000 rows.

- Formula consistency check: CTR = clicks ÷ impressions, conversion rate = conversions ÷ clicks, ROAS = revenue ÷ spend and CPA = spend ÷ conversions all reproduce in **1000/1000** rows.
- **Data-quality flag:** conversions exceed qualified leads in **325/1000** rows.
- Channel ROAS values are near-identical, which suggests a practice/synthetic dataset.
- Use this table only to demonstrate the KPIs.

| Channel | Rows | CTR % | Conversion rate % | CPC $ | Cost per lead $ | CPA $ | ROAS × |
|---|---|---|---|---|---|---|---|
| Display | 109 | 4.38 | 7.75 | 1.76 | 16.73 | 22.66 | 10.37 |
| Referral | 130 | 4.81 | 8.28 | 1.94 | 16.73 | 23.48 | 9.78 |
| LinkedIn | 132 | 4.25 | 7.83 | 1.76 | 15.72 | 22.43 | 9.48 |
| Meta Ads | 128 | 4.26 | 7.63 | 1.78 | 15.84 | 23.35 | 9.45 |
| Organic Social | 135 | 4.98 | 9.15 | 1.84 | 15.14 | 20.12 | 9.31 |
| Email | 104 | 4.63 | 7.54 | 1.67 | 14.58 | 22.10 | 9.29 |
| Google Ads | 136 | 4.45 | 7.83 | 1.86 | 17.19 | 23.72 | 8.43 |
| Organic Search | 126 | 4.48 | 7.90 | 1.97 | 17.45 | 24.92 | 7.82 |

**How we'd use these for Ownly (not observable by us):**
- CTR and conversion rate for Gachibowli launch ads.
- CPA = acquisition spend ÷ new customers — the Formulae Sheet 2 'average acquisition cost'. The observed ₹100-off first-order offer is one component (CONSUMER-GENERATED).
- Compare CPA with the CLV scenario in §3: acquisition only pays off if CLV > CPA.
