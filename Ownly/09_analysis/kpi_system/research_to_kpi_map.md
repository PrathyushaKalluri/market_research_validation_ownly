# Research → KPI Map

**Version:** 1.0 · 2026-09-16. Every workstream feeds named KPIs. If a question feeds no KPI, the table says why it's kept.

## 1. Survey v6 (+ additions A1–A3)

| Question | Short | KPIs fed | Dashboard page |
|---|---|---|---|
| S1-Q1 | City | Geography cut (all) | All |
| S2-Q1 | Area | Gachibowli core vs nearby cut | 3, 9 |
| S2-Q2 | Age | Eligibility screen (all denominators) | — |
| S3-Q1 | Occupation | Student/professional cut (all) | 3, 9 |
| S3-Q2 | Memberships | Member cut; K16 context | 3, 9 |
| **A1 (new)** | Rapido usage | K60, K61; Rapido user cut | 7, 9 |
| S3-Q3 | Ordered online in 4 weeks | K94; K00 denominator | 1, 3 |
| S4-Q1..Q4 | Orders by app | K33, K37, K92; K00, K30 (Ownly count); frequent/light cut | 1, 3, 4 |
| S5-Q1 | Last-order app | Platform context | 3 |
| S5-Q2 | Last bill ₹ | High/low basket cut | 3, 9 |
| S5-Q3 | People on order | Per-person bill (P2 context) | 3 |
| S5-Q4 | Bill fairness | K25 | 3, 5 |
| S6-Q1..Q3 | ₹30 trade-offs | K24; price-first/speed-first cut | 3, 4, 9 |
| S6-Q4 | Switching threshold | K23 | 5 |
| S7-Q1, Q2 | Try P / try Q | K15 | 1, 4 |
| **S7-Q3** | **Forced choice** | **K14 (H₀)** | **1** |
| S7-Q4 | Why (open text) | Coded into interview themes → Transferability Matrix evidence | 1, 10 |
| S7-Q5 | Repeat after ₹100 offer | K32 | 1, 8 |
| S7-Q6 | Low prices go up | Price-durability doubt; feeds the "transparent lower price" row (P2) | 10 |
| S8-Q1 | Ownly status | K01, K10, K11, K12; trier cut | 1, 3, 4, 7 |
| S9-Q1 | Trigger (unaware) | K17, K72 | 4, 8 |
| S10/S11/S12-Q1 | Where first heard | K62 | 7 |
| S10-Q2 | Why never opened | K16 | 4 |
| S11-Q2 | What stopped ordering | K16, K43 | 4, 6 |
| S12-Q2 | Where ordered (HYD) | Cleans Hyderabad triers who only ordered in Bengaluru | 3 |
| S12-Q3 | First order timing | K31 | 2 |
| **A2 (new)** | Offer on first order | K70, K71 | 8 |
| S12-Q4 | Orders 5–8 weeks ago | K00, K30 | 1, 4 |
| S12-Q5 | If Ownly didn't exist | K35 | 4 |
| S12-Q6 | Disappointment | K34 | 4 |
| **A3 (new)** | Fulfilment failures | K51, K52 | 4, 6 |
| S12-Q7 | One change | K36 | 4 |
| S23 order-less (BLR) | Drop-off reason | K36 | 2, 4 |
| S31-Q1 | Interview volunteer | Interview recruitment only | — |

## 2. Interviews (8, `04_interviews/RAPID_15min_guide_v3.md`), explanatory only

**Rule:** report coded **counts** ("5 of 8"), never percentages. Each block explains *why* a KPI moved.

| Guide block | Explains | Hypothesis |
|---|---|---|
| §1 Last order, surprise at checkout | K25 fee pain, K22 fee load | Fees drive switching intent |
| §2 Last bad order, how many before quitting | K51, K52, K30 | Reliability earns the second order |
| §3 ₹30 trade-offs, switching threshold in ₹ | K24, K23 (verbatim reasons behind the numbers) | Price gets the first order |
| §4 Brand-blind cards (pick, why, what's missing, do prices last) | K14 direction; S7-Q6 durability doubt | H₀ proposition preference |
| §5 Ownly reveal: awareness source, Rapido relevance, repeat without discount (next 3 orders), barrier | K62, K61, K32, K16 | Rapido distribution; promo dependency |
| §6 What would make them switch | K17, K36 | First vs second order drivers |
| Tracker `rapido_user` column | Count context for K60 | — |
| Optional add-on: Rapido home screenshot, "where would you tap to order food?" | K63 (counts and seconds) | App discoverability (P2 hypothesis) |

## 3. Person 3: price audit (`06_competitor_audit/`)

| Audit input | KPI |
|---|---|
| Matched basket final_payable (Ownly vs Swiggy vs Zomato, same slot/restaurant/basket) | K20 saving ₹ and %, K21 win rate |
| menu_subtotal, packaging, platform, delivery, small_cart, surge, taxes, discount | K22 fee load; Page 5 waterfall decomposition |
| restaurant_listed, restaurant_open by platform | K42 availability overlap |
| Restaurant frame on_ownly / on_swiggy / on_zomato, chain_or_local | K40 coverage, K41 local vs chain |
| eta_min_shown, eta_max_shown | K50 ETA gap; savings-vs-ETA scatter |
| Screenshots | Evidence panels (Pages 5, 6); verification of any game (K73) |
| Test orders (if ₹900 approved) | K54 anecdotal actual vs promised |

## 4. Person 3: fake door (`07_fake_door/`)

| Event / field | KPI |
|---|---|
| Unique `anon_visitor_id` per `variant_id` (excluding QA and bots) | K13 denominator; sample-ratio mismatch check |
| `cta_click` | K13 conversion, pp lift and relative lift |
| `secondary_intent` | K74 bill-compare rate |
| `utm_source` (plus `experiment_tracker.csv` reach) | Channel conversion; reach → visitor rate (pattern from the generic marketing file) |
| `mini_survey_submit` seg_occupation / orders_4wk | Segment mix of visitors (Page 7 / Page 9 context) |
| Spend | ₹0, so **experiment CAC is not calculable** |

## 5. App-placement test
Not built. **K63** is an optional add-on to the interviews only. Treat bottom-nav placement as a hypothesis: public sources
confirm Rapido-app integration in **Bengaluru only** (Business Today, 2026-07-28).

## 6. Game / promotion
- **Observable now:** K32 (S7-Q5), K70 and K71 (A2), K72 (S9-Q1).
- **₹50/₹100 game:** no public evidence it exists (research check, 2026-09-16). K73 stays ⛔ until P3 captures a dated screenshot.
  Public sources show only a 50%-off first-order offer capped at ₹100, in Bengaluru.

## 7. Secondary research, reviews and social

| Source | KPI / use | Rule |
|---|---|---|
| Strategy timeline (pilot Aug 2025 → BLR citywide Mar 2026 → Rapido integration Jul 2026 → HYD ~Sep 2026) | Page 2 timeline | Dated, sourced |
| Reported orders/day (5k Mar → 50k Aug) | K90 CMGR | Labelled external |
| Reported share "nearly 10%" | K91 | Company claim |
| Restaurant partners 20k–25k | K44 | Conflicting figures; show a range |
| Zero-commission claim, and the Jul 2026 "subscription" contradiction | Page 2 claims-vs-evidence table | Flag the conflict |
| Fee model by period | Page 2 model-change strip | Never mix periods |
| App ratings | K93 | Context |
| Reviews (37) and social (524; 123 first-hand) | K53 theme map; hypotheses for Pages 4 and 6 | **Issue discovery, never prevalence**; AI-coded, human validation pending |
| Toing (33M WAU), Swiggy/Zomato fee hikes | Page 2 / Page 10 competitive context | External |
| Foodpanda (Ola) 2019, Uber Eats 2020 exits | Appendix only | Doesn't change the Hyderabad decision |
| Poll A (unscreened awareness) | Shown next to K10 | Never merged |
