# KPI Tree: Ownly Hyderabad (Gachibowli) transfer decision

**Version:** 1.0 · 2026-09-16 · Owner: Claude (analytics lead)
**Folder note:** the master prompt asks for `05_analysis/`, `06_dashboard/` and `01_plan_tracking/`. Those prefixes are
already taken in this repo (`05_review_mining`, `06_competitor_audit`, `01_secondary_research`), so the equivalents are
`09_analysis/kpi_system/`, `10_dashboard/decision_dashboard/` and `_ops/`.
**Survey basis:** v6 (`Survey_v6_Google_Form_Build_Guide.md`), **plus the 3 minimal additions in `data_gap_map.md` §3**.
If v7 is fielded instead, see `data_gap_map.md` §4.

> **Standard:** no vanity metrics, no false precision, no invented Ownly metrics. Every KPI names the decision it enables.
> **Status on 2026-09-16:** no primary data has been collected yet (survey 0, fake door not deployed, audit fields empty,
> interviews 0). Every primary-data KPI below is **designed and calculable once data arrives**. None has a value yet.
---

## 1. Ownly's real strategic metric logic

Three separate labels, never merged. Full source list: the research hand-back logged in `_ops/decisions.md` D12, and
`01_secondary_research/evidence_table.csv`.

### A. Publicly stated company priorities
**No official north-star metric has been published by Rapido or Ownly.** These are stated goals, not KPIs.

| Stated priority | Evidence | Who | Source · date |
|---|---|---|---|
| Grow the number of people ordering food online, not just take share | "If the number of people ordering food online doesn't reach 100 million in three years, there is no reason for Rapido to exist" | Aravind Sanka, CEO | Storyboard18 citing Moneycontrol · 2026-07-06 |
| Affordability | "We have to solve for affordability. That is the biggest deterrent for consumers today." | Sanka | same · 2026-07-06 |
| Logistics-led model | "Delivery companies are logistics companies… We solve logistics." | Sanka | same · 2026-07-06 |
| Convert Rapido transport users who have never ordered food | Integration aimed at people who "already use its transport services but have not previously ordered food through an app" | Sanka | Indian Startup News · 2026-07-28 |
| Better restaurant economics | "no commissions… no marketing fees… no subscription fees" | Vivek Vashishta | MediaNama · 2026-03-05 |
| Local and regional restaurants | Incumbents "built only for nationalised chains… Not for the local/regional ones" | Sanka | Startuppedia · 2026-07-06 |
| Customer promise in Hyderabad | No platform, packaging or surge fees; "no inflated prices" | Company | ownly.food/hyd · checked 2026-09-16 |

### B. Reported external business metrics (context only, never our observed values)

| Metric | Value | Geo | Source · date | Caveat |
|---|---|---|---|---|
| Orders/day | ~5,000 | BLR | Upstox citing Inc42/HT · ~2026-03-26 | Secondary citation |
| Orders/day | 40k+ (Jul) → 50k+ (Aug) | BLR | Storyboard18 citing Moneycontrol · 2026-08-21 | One upstream report |
| City order share | "nearly 10%" | BLR | Inc42 · 2026-07-30 | Company claim; derived from an estimated 500–600k city orders/day |
| Restaurant partners | ~20,000 (Mar, Jul); 22,000 (site) | BLR | MediaNama; Business Today; ownly.food | Figures conflict |
| App rating | Play 4.48★ (44,485 ratings, 1M+ installs); iOS 4.5★ (10,466) | India | `05_review_mining/app_stores/listing_stats.csv` · 2026-09-14 | Self-selected raters |
| Rapido integration | Ownly inside the Rapido app | **BLR only** | Business Today · 2026-07-28 | No public source on tab or bottom-nav placement |
| First-order offer | 50% off, capped at ₹100 | BLR | Indian Startup News · 2026-07-28 | **No public source for any ₹50/₹100 game** |
| Hyderabad live | "officially LIVE" after "a month of building supply" | HYD | Employee post, StartupTalky · ~2026-09-11 | Not a press release |
| Customer fee model | ~₹30 delivery, no platform fee (Mar 2026 on) | BLR | MediaNama; Upstox | Described inconsistently: flat, +GST, distance-based |
| Restaurant fee model | Per-order fee in the pilot (Aug–Nov 2025) → ₹0 (Mar 2026 on) | BLR | MediaNama; Storyboard18 | Jul 2026: Angel One says there is a "subscription" fee, contradicting other sources |
| Competitor fees | Zomato ₹14.90 + GST; Swiggy ₹17.58 incl. GST platform fee | India | MediaNama · Mar 2026 | National |
| Toing | 33M weekly active users; ~50 cities | India | Storyboard18 citing CLSA · 2026-09-09 | App-intelligence estimate |
| Burn/order | **Not public** | — | — | The repo's "₹150–170" figure is unverified: do not use it |

**Model changes over time:** pilot restaurant-paid delivery fee (Aug 2025) → flat ₹25 + GST per order from restaurants,
nothing charged to customers (Nov 2025) → ₹0 restaurant charges plus a ~₹30 customer delivery fee (Mar 2026 onward).
**Never compare a pilot-era fee with a current one.**

### C. Project-recommended north-star proxy (our recommendation, not Ownly's metric)
See §2. It is always labelled **"project proxy"** on the dashboard.

---

## 2. North-star evaluation

Scores run from 1 (weak) to 3 (strong). "Can we estimate it" refers to *our* data, not Ownly's internal data.

| Criterion | C1 Monthly transacting food customers | C2 Monthly repeat fulfilled orders | C3 Fulfilled orders per active customer | **C4 Active repeat customers** |
|---|---|---|---|---|
| Strategic alignment | 3: matches "100M people ordering online" | 3 | 2: a frequency metric, weaker on reach | **3: reach and durability together** |
| User value | 2: counts promo-driven one-offs | 3 | 3 | **3** |
| Restaurant value | 2 | 3: repeat demand | 2 | **3** |
| Controllability (for a GTM team) | 2 | 2 | 2 | **2** |
| Measurability for Ownly | 3 | 3 | 3 | **3** |
| Gaming risk | **1: first-order discounts inflate it** | 2: heavy users can dominate | 2: churning light users *raises* it | **3: needs a second order after the promo** |
| **Can our project estimate it?** | Partly: trial penetration only | **No**: no fulfilment or order-level data | Partly: self-reported counts, no fulfilment flag | **Yes, as a sample proxy** (S4-Q3 + S12-Q4) |

### Recommendation

**Primary project north-star proxy: K00 Repeat-active Ownly customers per 100 food-delivery users.**
- **Formula:** respondents with **≥1 Ownly order in the last 4 weeks AND ≥2 Ownly orders in the last 8 weeks**
  (S4-Q3 + S12-Q4) ÷ eligible respondents (20–30, in the target geography) who ordered food online in the last 4 weeks (S3-Q3).
- **Why this one:**
  - It captures both halves of the business question: reaching new orderers, and earning the second order.
  - It resists promo-only trial.
  - We can estimate it in Hyderabad now: the 8-week window works even though Ownly launched there around September.
  - It maps to Candidate 4, the only candidate our data supports.
- **What it is not:** a fulfilled-order metric (it is self-reported), a market-share figure, or Ownly's own KPI.

**Guardrails.** The north star can rise while these fall; any guardrail breach blocks a KEEP decision.

| # | Guardrail | Why |
|---|---|---|
| G1 | **K20** Median matched-basket saving % (audit) | Affordability is the promise. Repeat growth bought with a price gap that doesn't exist is not transferable |
| G2 | **K51** Fulfilment failure incidence among triers (new survey item) | Repeat demand cannot survive failed deliveries (review mining: fulfilment failures are 72% of app-store complaints) |
| G3 | **K40** Target-restaurant coverage (audit frame) | Supply side of a two-sided marketplace |
| G4 | **K71** Promo-dependency gap (new survey item) | Tells durable adoption apart from subsidised trial |

---

## 3. KPI tree

Legend: **P0** = decides the call · P1 = explains why P0 moved · P2 = context · ⛔ = not calculable from our data.
Data: SV = survey v6 (+ additions A1–A3) · FD = fake door · AU = price audit and restaurant frame ·
IV = interviews (qualitative counts only) · RM = review/social mining (issue discovery only) · EX = external/secondary.

```
LAYER 0 · BUSINESS OUTCOME
└── K00 ★ Repeat-active Ownly customers per 100 delivery users (P0, SV, project proxy)
    ├── K01 Trial penetration (brand penetration) (P0, SV)
    └── K30 Trier repeat rate (P0, SV)

LAYER 1 · ACQUISITION: what gets the FIRST order?
├── K10 Awareness (P0, SV) · cross-check: Poll A unscreened awareness (P2)
├── K11 Awareness → trial conversion (P0, SV)
├── K12 Browse → order conversion (P1, SV)
├── K13 H₀ fake-door CTA conversion A vs B, pp and relative lift (P0, FD)
├── K14 H₀ survey forced choice: Service Q share (P0, SV; primary if FD < 80 visitors, per D3)
├── K15 Stated trial intent P vs Q, top-2 box, McNemar (P1, SV)
├── K16 First-order barrier incidence by funnel stage (P1, SV)
└── K17 Trial-trigger ranking among the unaware (P1, SV)

LAYER 2 · VALUE / AFFORDABILITY: is "cheaper" real and does it move people?
├── K20 Median matched-basket saving % vs cheaper incumbent (P0, AU) [G1]
├── K21 Ownly win rate, ₹5 tie rule (P1, AU)
├── K22 Fee load % of final payable, by platform (P1, AU)
├── K23 Switching-threshold coverage: % whose required saving ≤ observed median ₹ saving (P1, SV × AU)
├── K24 ₹30 trade-off shares: price vs speed / reliability / restaurant choice (P0, SV)
├── K25 Fee pain on last bill (P1, SV)
└── K26 Online/offline menu parity (⛔ P2: audit-lite has no offline price field)

LAYER 3 · RETENTION: what earns the SECOND order?
├── K30 Trier repeat rate: ≥2 Ownly orders in 8 weeks ÷ triers (P0, SV)
├── K31 Still-ordering rate, first order 4+ weeks ago (P1, SV; Bengaluru cohort, Hyderabad too young)
├── K32 Repeat-without-promo intent, S7-Q5 top-2 (P0, SV)
├── K33 Unit share of requirements among Ownly buyers (P0, SV; course metric)
├── K34 PMF: very disappointed (P1, SV)
├── K35 Incumbent substitution (P1, SV)
├── K36 Drop-off / "one change" drivers (P1, SV)
└── K37 Heavy-usage index (P2, SV; course metric)

LAYER 4 · ASSORTMENT / SUPPLY
├── K40 Target-restaurant coverage on Ownly (P0, AU) [G3]
├── K41 Local vs chain coverage gap (P1, AU)
├── K42 Cross-platform availability overlap (P1, AU)
├── K43 "My restaurants weren't there" barrier share (P1, SV)
└── K44 Reported restaurant partners (P2, EX, Bengaluru)

LAYER 5 · FULFILMENT / EXPERIENCE
├── K50 ETA gap: Ownly minus cheaper incumbent, minutes (P0, AU)
├── K51 Fulfilment failure incidence among triers (P0, SV addition A3) [G2]
├── K52 Repeat rate: triers with vs without a failure (P1, SV; the "reliability earns the second order" test)
├── K53 Fulfilment/support theme share in reviews (P2, RM, issue discovery only)
└── K54 Test orders: actual vs promised minutes (P2, AU, n = 3, anecdotal)

LAYER 6 · DISTRIBUTION / RAPIDO ECOSYSTEM
├── K60 Rapido usage penetration (P1, SV addition A1)
├── K61 Awareness and trial: Rapido users vs non-users, pp gap (P1, SV; association only)
├── K62 Discovery via the Rapido app % (P1, SV)
└── K63 App-placement first-tap success (P2, IV optional add-on; ⛔ in survey)

LAYER 7 · PROMOTION / GTM
├── K70 Offer-triggered first order % (P1, SV addition A2)
├── K71 Promo-dependency gap: repeat rate for no-offer minus offer first orders, pp (P0, SV) [G4]
├── K72 "Discount" as top trial trigger among the unaware (P1, SV)
├── K73 Game awareness / participation (⛔ P2: no public evidence a game exists; P3 to screenshot)
└── K74 Fake-door bill-compare rate by arm (P1, FD)

LAYER 8 · SEGMENTATION (cuts applied to the P0/P1 KPIs, not KPIs themselves)
    city (HYD/BLR) · student/professional · trier/non-trier · Rapido user/non-user (A1) ·
    frequent (≥6 orders in 4 weeks)/light · basket above/below the median last bill · price-first/speed-first (K24) ·
    Gachibowli core/nearby (S2 area) · offer/no-offer first order (A2) · delivery member/non-member

LAYER 9 · MARKET / COMPETITIVE CONTEXT (EX; always labelled external)
├── K90 Reported BLR orders/day and CMGR: 5k (Mar) → 50k (Aug) ≈ 58% a month (P2)
├── K91 Reported BLR city share "nearly 10%" (P2, company claim)
├── K92 Sample volume-share proxy: Ownly orders ÷ all orders, all orderers (P1, SV)
├── K93 App-store ratings (P2)
└── K94 Market penetration: ordered online in 4 weeks ÷ eligible respondents (P1, SV; course metric)

LAYER 10 · ECONOMICS: all ⛔ NOT CALCULABLE FROM OUR DATA
    CAC · CPA · retention cost · CLV · ROAS · contribution margin · GOV/GMV · EBITDA · burn/order
    (No spend, cost, margin or company sales data. Fake-door spend = ₹0, so even an experiment CAC is undefined.)
```

---

## 4. Course formula-sheet metrics

| Course metric (sheet) | Verdict | How it's used |
|---|---|---|
| Brand penetration | **USE** | K01 (sample-based) |
| Market penetration | **USE** | K94 (sample-based) |
| Penetration share | **USE** | K01 ÷ K94 |
| Unit share of requirements | **USE AS PROXY** | K33 (self-reported 4-week counts) |
| Revenue share of requirements | REFERENCE ONLY | No spend per app; only the last-order amount |
| Heavy-usage index | **USE AS PROXY** | K37 (P2) |
| Volume share | **USE AS PROXY** | K92 (sample volume share, not market share) |
| Value share | REFERENCE ONLY | No revenue per app |
| Retention rate | **USE AS PROXY** | K31 (Bengaluru cohort, self-reported) |
| CLV | REFERENCE ONLY | No margin or discount-rate inputs |
| Average acquisition cost / retention cost | NOT CALCULABLE | No spend |
| YoY growth / CAGR | **USE AS PROXY (external)** | K90 CMGR on reported orders/day, labelled external |
| Cannibalization rate | **USE AS PROXY, reframed** | K35 measures substitution *from incumbents*, not cannibalisation of Rapido's own products |
| CDI / BDI | USE AS PROXY (P2) | Only as in-sample segment indices; no household denominators |
| Relative market share | NOT RELEVANT | No competitor share data |
| Contribution, margin, break-even, target volume/revenue, supplier/customer price, price per statistical unit | NOT RELEVANT | Unit economics not observable; the decision is proposition transfer, not pricing a P&L |
| Average price per unit | REFERENCE ONLY | The audit's final payable already covers it |

The generic `Marketing Metrics 1000 Records.csv` is a **pattern reference only** (funnel: impressions → clicks → conversions → CPA).
It is never mixed into Ownly analysis. Its funnel logic is reused for the fake door: reach (tracker) → visitors → CTA → bill compare.
