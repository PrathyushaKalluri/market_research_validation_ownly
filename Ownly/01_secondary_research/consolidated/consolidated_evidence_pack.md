# Consolidated Evidence Pack (pre-fieldwork)

**Built:** 2026-09-16 by Claude (execution lead), from the project's own coded datasets.
**Inputs:** `01_secondary_research/evidence_table.csv` (68 claims), `ownly_segments_evidence.csv` (60 rows),
`05_review_mining/app_stores/reviews_coded.csv` (n=37), `05_review_mining/social/social_coded.csv` (n=524).
**Nothing here is Hyderabad customer data.** Every number below is a count inside a self-selected, mostly
Bengaluru, publicly-posted sample. Labels: CONSUMER-GENERATED unless stated.

---

## 1. The one exhibit that carries the whole secondary story

Theme families, counted two ways. Columns are **share of items in that column's base**, not population incidence.

| Theme family | All public discussion<br>(n=260 items with a mapped theme) | People describing their **own** Ownly order<br>(n=79 first-hand items) | App-store reviews<br>(n=32 with a mapped theme) |
|---|---:|---:|---:|
| **PRICE_DOUBT** — "the low price won't last", fee creep, incumbent coupons erase the gap, menu inflation | **92 (35%)** | 13 (16%) | 0 |
| **PRICE_ADVANTAGE** — observed saving, bill comparison, no-fee praise | 41 (16%) | 22 (28%) | 5 (16%) |
| **FULFILMENT_FAIL** — non-delivery, false "delivered", late, cancelled, missing items | 38 (15%) | **37 (47%)** | **23 (72%)** |
| **SUPPORT_REFUND** — unreachable/scripted support, money deducted, refund stuck | 28 (11%) | **22 (28%)** | **23 (72%)** |
| **COMPETITION** — Toing, incumbent context, low platform loyalty | 36 (14%) | 3 (4%) | 0 |
| **ASSORTMENT** — city/area availability, restaurant not listed, menu accuracy | 24 (9%) | 3 (4%) | 7 (22%) |
| **DISTRIBUTION** — Rapido ecosystem, trial curiosity, launch relay | 25 (10%) | — | 0 |
| **TRUST_QUALITY** — food quality/hygiene, veg trust, rider conduct, astroturf suspicion | 8 (3%) | 1 (1%) | 14 (44%) |

Items can carry more than one theme, so columns sum to more than 100%.

### How to read it (this is the line for the deck)

> **What people *argue about* is price. What people who actually ordered *report* is fulfilment.**
> Price-doubt is the single largest theme in open discussion (35%), yet it nearly vanishes among
> first-hand accounts (16%). Fulfilment failure runs the opposite way: 15% of all discussion but
> **47% of first-hand accounts** and **72% of app-store reviews**. Support/refund failure behaves
> identically (11% → 28% → 72%).

This is the sharpest available pre-fieldwork support for the project's diagnostic proposition —
**price may acquire, reliability may retain** — and it is the reason our primary instrument must
measure *both* a price hook and a reliability hook rather than assuming price wins.

**Caveat that must appear next to this exhibit:** app-store reviews and complaint posts are
self-selected toward failure. The right conclusion is *"failure is the dominant thing dissatisfied
users talk about"*, not *"47% of Ownly orders fail."* We cannot estimate a failure rate from this data,
and we will not try to.

---

## 2. Secondary-source quality audit (from `evidence_table.csv`, n=68)

| Verification status | Count |
|---|---:|
| Partially verified | 29 |
| Unverified | 18 |
| Verified | 16 |
| **Contradicted** | **5** |

| Evidence type | Count |
|---|---:|
| MEDIA REPORT | 50 |
| COMPANY CLAIM | 10 |
| FACT | 5 |
| CONSUMER-GENERATED | 3 |

**Implication:** 74% of our secondary base is media reporting or company claim, and only 24% is verified.
Slide 2 of the deck should be a *fact-vs-claim* table, not a findings table. The three headline numbers
everyone repeats — "50,000 orders/day", "₹30 flat fee", "~15% cheaper" — are respectively
single-upstream-source, contradicted, and pilot-era positioning. **The Gachibowli price audit is the only
thing in this project that can settle the price question with observed data.**

On the segments file (n=60): 31 COMPANY CLAIM, 28 MEDIA REPORT, 1 CONSUMER-GENERATED — i.e. there is
**no independent evidence about who Ownly's users actually are**. Our survey is the first such evidence.

---

## 3. Other counts worth quoting

| Measure | Value |
|---|---|
| Social items judged relevant | 420 / 524 |
| First-hand Ownly experience | 123 / 524 (23%) |
| Sentiment (social) | neutral 184 · negative 152 · positive 60 · mixed 24 |
| Severity 3 or 4 (social, where coded) | 54 / 79 coded |
| App-store star distribution | 1★ 26 · 2★ 1 · 3★ 1 · 4★ 2 · 5★ 7 |
| City mentioned (social, where stated) | Bengaluru 35 · **Hyderabad 4** · Mumbai 4 · Delhi 3 · others 5 |

**Hyderabad appears 4 times in 524 items.** That is the evidence gap this project exists to close.

---

## 4. What each theme family converts into, in our instruments

| Theme family | Survey item | Audit column | Interview probe |
|---|---|---|---|
| PRICE_DOUBT | `beh_switch_savings_required`, `pain_menu_markup_belief`, `prop_durability_doubt` (new) | `discount_amount` with/without coupon; repeat slots | "Do you expect these prices to last? What makes you say that?" |
| PRICE_ADVANTAGE | `beh_last_order_total`, bill-gap module | `final_payable` gap, win rate | "Walk me through the last bill that felt like a good deal." |
| FULFILMENT_FAIL | `pain_late_freq`, `pain_cancel_freq`, `tradeoff_rel` | test orders: promised vs actual | "Tell me about the last order that went wrong." |
| SUPPORT_REFUND | `pain_top_frustrations` (support option) | — | "What happened when you asked for help?" |
| ASSORTMENT | `exp_fav_restaurant_needed`, `tradeoff_rest` | `restaurant_listed`, coverage count | "Which places would have to be on it?" |
| DISTRIBUTION | `br_rapido_effect`, `own_aware_aided` | — | Rapido-screen first-tap task |
| COMPETITION | `beh_platforms_used_4wk`, `beh_subscriptions` | Toing presence check | "What else have you tried?" |

---

## 5. Reproducing these numbers

The rollup is a theme-family mapping over the `themes` column of both coded files.
The mapping and the counting script are in `01_secondary_research/consolidated/rollup_themes.py`.
Run from the project root: `python3 01_secondary_research/consolidated/rollup_themes.py`.
