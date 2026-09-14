# P. 3-Day Plan (deadline 17 Sep 2026): Feasible Data, Ethics, ₹900 Budget, KPIs

**Version:** 2026-09-14.

**Real constraints (confirmed by the user today):**
- Deadline: **17 September**
- Instructor ethics approval is required for **every** data-collection activity
- Budget: **₹900**
- No team time for manual review copying

This replaces the 5-week plan in `O_execution_checklist_and_timeline.md` for the actual submission. The full design stays in the project as the "what we would do with more time" appendix.

---

## 1. What we can honestly conclude today (before any survey)

**Evidence base:**
- Secondary research: 68 claims (`01_secondary_research/`)
- 37 app-store reviews
- 524 Reddit/LinkedIn/X items, of which 108 are first-hand experiences (`05_review_mining/`)

**None of this is Hyderabad customer data.** So these are **provisional, desk-based conclusions**, not validated findings.

| # | Provisional conclusion | Evidence type | Confidence |
|---|---|---|---|
| 1 | **Ownly's Bengaluru pull is price, but its biggest risk is service reliability.** First-hand public posts describe 46 failed deliveries and 29 support/refund failures, against 19 price wins. App reviews show the same pattern (support 21 of 37, refunds 16). | CONSUMER-GENERATED (two independent sources agree) | LOW–MEDIUM (self-selected, Bengaluru only) |
| 2 | **The price advantage is real but not guaranteed.** Every user-posted bill comparison favoured Ownly, yet 18 posts say Swiggy/Zomato coupons or card offers erased the gap, or restaurants priced the same. | CONSUMER-GENERATED | LOW |
| 3 | **Key "facts" are weaker than they look.** "50,000 orders/day" is one media source copied by others. The "₹30 flat fee" is contradicted (free / ₹15 / distance-based). "15% cheaper" is pilot-era company positioning. | MEDIA REPORT / COMPANY CLAIM | HIGH (that these claims are unverified) |
| 4 | **Hyderabad is only weeks old for Ownly.** Dated posts suggest a launch between late August and ~11 September. There is no Hyderabad customer voice online yet. | INTERPRETATION | LOW |
| 5 | **Competition is not just Swiggy and Zomato.** Swiggy's budget app Toing targets the same 20–30 students and young professionals. | MEDIA REPORT | MEDIUM |
| 6 | **Users doubt the low prices will last** (37 posts), and payment gaps (no cash on delivery, no meal cards) may block salaried users. | CONSUMER-GENERATED | LOW |

**Provisional strategic position (a HYPOTHESIS to test in the next 3 days, not a recommendation):**

> **ADAPT, don't copy Bengaluru.**
> - In Gachibowli, don't lead with "cheapest". Lead with a *fair total price you can rely on*.
> - Fix support and refunds before scaling.
> - Start with small, frequent solo orders from students and young professionals. A Reddit user put it as "small orders Ownly, large orders Swiggy with card offers".

The 3-day data collection below tests the three things this position depends on:
1. **Is there a real price gap in Gachibowli after coupons?** → competitor audit
2. **Do Gachibowli 20–30s feel fee pain, and how big a saving would make them switch?** → short survey
3. **Does reliability outweigh a ₹30 saving?** → three trade-off questions in the short survey

---

## 2. Ethics approval — do this first (today)

1. Send the instructor the application: `00_research_charter/ethics_application_draft.md` (covers survey, interviews, app price audit, test orders, public review analysis).
2. Ask for a same-day or next-morning decision, since the deadline is 17 September.
3. **Nothing involving people (survey, interviews) starts before written approval.**
4. The **fake-door landing page is dropped.** There is no time to get traffic, and a page that shows a disclosure only after the click is harder to approve quickly.

**If approval has not arrived by Tuesday 15 September, 2 pm:** submit a **desk-based study**, made up of:
- secondary evidence
- public customer-voice analysis
- the complete validated research design (already built)
- the competitor price audit, if the instructor approves that part separately (it involves no participants)

Present the survey and interviews as the next phase. Say this openly in the limitations; it is a legitimate outcome.

---

## 3. What data to collect in 3 days (feasible, ₹900)

| # | Data | Why | How | Feasible size in 3 days | Cost | Needs approval? |
|---|---|---|---|---|---|---|
| D1 | **Competitor price audit** (checkout screen captured, stopped before payment) | The only way to prove or disprove the price claim in Gachibowli | 2 people, same address, same minute, same dish on Ownly / Swiggy / Zomato (+ Toing if present). Record food price, every fee, discount, final payable, ETA. Screenshot everything. Use schema `06_competitor_audit/audit_schema.csv` (fill only the columns in §3a below). | **10 restaurants × 3 apps × 3 slots** (Tue lunch, Tue dinner, Wed dinner) ≈ **90 captures**, ~30 matched comparisons | ₹0 | Yes (quick, no participants) |
| D2 | **3 real test orders** (same dish, same restaurant, same time, ordered to the same Gachibowli address on Ownly, Swiggy, Zomato) | Promised vs actual delivery time, actual fees charged, order accuracy | Order a cheap single item (~₹150–200 food) on Wednesday dinner. Record the timestamp at order, pickup and delivery. | 3 orders | **≈ ₹750–900** (the whole budget) | Yes |
| D3 | **Short Hyderabad survey (~7 min)** | Fee pain, switching threshold, trade-offs, Ownly awareness/trial | `03_hyderabad_survey/SHORT_survey_7min_google_form.md`. Share via IIIT-H, University of Hyderabad, PG/co-living groups (with admin permission) and LinkedIn contacts in Gachibowli/Financial District. Open ~36 hours. | Realistic **50–80 valid**. Label as exploratory; margin of error ±11–14 pp. | ₹0 (no incentives) | Yes |
| D4 | **4–6 short interviews (15 min)** | The "why" behind survey numbers: last order, last bill shock, last failed order | Use the 30-minute guide, keeping §1–§6 plus the brand-blind card. Notes, not recordings, unless consent is given. | 4–6 (2–3 students, 2–3 professionals) | ₹0 | Yes |
| D5 | **Public customer voice (already collected)** | Bengaluru benchmark evidence in place of a Bengaluru survey | Use `05_review_mining/voc_synthesis_pre_fieldwork.md` | 561 items, 145 first-hand | ₹0 | Include in application |
| ✘ | Bengaluru survey | **Dropped:** reaching real Ownly users in 36 hours isn't feasible | Public VoC serves as the Bengaluru evidence | — | — | — |
| ✘ | Fake door, full choice experiment (needs n ≥ 125), fee staircase, brand-arm randomisation | **Dropped:** the sample is too small and time too short | Replaced by 3 simple trade-off questions and a direct max-fee question | — | — | — |

### 3a. Audit columns to fill (lite version)

`capture_ts, slot, auditor_id, drop_point_id, platform, account_state, subscription_active, restaurant_name, restaurant_listed, restaurant_open, basket_id, item_list, item_match_quality, menu_subtotal, packaging_fee, platform_fee, delivery_fee, small_cart_fee, surge_rain_fee, taxes_gst, discount_amount, discount_type, final_payable, eta_min_shown, eta_max_shown, screenshot_file, notes`

**Mandatory capture rules:**
- Where a coupon is auto-applied, capture the total **with and without** the coupon.
- Type the delivery fee **exactly as shown** (including "free").

**Restaurant choice (updated 2026-09-14 from `01_secondary_research/ownly_restaurant_and_user_segments.md`):** pick 10 that serve the drop point, in three groups that mirror what Ownly says it targets.

| Group | Count | Candidates (check in-app first) | Why |
|---|---|---|---|
| A. Ownly's Hyderabad showcase chains | 4 | Paradise Biryani, Bawarchi, Cream Stone, 100N, Vivaha Bhojanambu, Punjabi Affair (whichever outlets serve Gachibowli) | Tests Ownly's own published price claims, e.g. ₹249 vs ₹420 (COMPANY CLAIM) |
| B. Local independents / budget meals near tech parks and PG clusters | 4 | Tiffin centres, meals/thali places, local biryani joints listed on Ownly | Ownly's *stated* core target (local/regional eateries; ≥4 meals under ₹150) |
| C. National QSR / cloud-kitchen brands | 2 | KFC, McDonald's, Domino's, Burger King, Faasos/EatSure, Wow! Momo | Record whether they are on Ownly at all (KFC and McDonald's went offline in Bengaluru in May 2026, MEDIA REPORT) |

Group B uses a "Meals for One" item under ₹150 where available.

Also note how many of 10 popular Swiggy/Zomato restaurants you search for are **missing** on Ownly (coverage).

**Day 0 check (tonight):** open Ownly with the Gachibowli address. If Ownly doesn't deliver there, **that is itself a key finding**. Then audit the nearest served area (e.g. Madhapur/Kondapur) and say so.

---

## 4. Day-by-day (Sep 14–17)

| When | Task | Owner |
|---|---|---|
| **Mon 14, evening** | Send ethics application. Build the short Google Form (copy-paste spec). Build the audit Google Sheet. Check Ownly serviceability at 1–2 Gachibowli addresses. Pick 10 audit restaurants. | P1 form · P2 ethics + sheet · P3 serviceability + restaurants |
| **Tue 15, morning** | On approval: pilot the survey with 3 friends (fix wording), then launch. Message group admins. | P1 |
| **Tue 15, 12:30–14:00** | Audit slot 1 (lunch) | P2 + P3 |
| **Tue 15, 20:00–22:00** | Audit slot 2 (dinner); 2 interviews | P2 + P3; P1 |
| **Wed 16, day** | Survey reminders; 2–4 interviews; code the interview notes | P1 |
| **Wed 16, 20:00–21:30** | Audit slot 3 + **3 test orders** (₹900) | P2 + P3 |
| **Wed 16, 22:00** | **Close survey.** Export CSV to `08_clean_data/raw/`. | P1 |
| **Thu 17, morning** | Clean data (rules in `08_clean_data/cleaning_protocol.md`: screen-outs, speeders, attention check). Compute KPIs (§5). | P1 + P3 |
| **Thu 17, afternoon** | Transfer slide, scorecard (only the dimensions with evidence), slides, limitations. Submit. | All |

---

## 5. Which KPIs from your three files to use

### 5.1 File verdicts

| File | What it is | Verdict for this project |
|---|---|---|
| `Formulae Sheet (1).docx` (MKT 24604) | Contribution & break-even, margins and channel margins, average price & price per statistical unit, market share, penetration, share of requirements, usage/heavy-usage index, development indices, relative market share | **Useful.** Several formulas map directly onto our survey and audit data (§5.2) |
| `Formulae Sheet 2.pdf` (Ch. 4 & 5) | YoY growth, CAGR, cannibalisation rate, retention rate, customer lifetime value (CLV), average acquisition cost, average retention cost | **Partly useful.** Growth rate (on media-reported numbers), a retention proxy and CLV as a labelled scenario. The rest needs company data we don't have |
| `Marketing Metrics 1000 Records.csv` | 1,000 rows of generic digital-campaign data (2024-01 to 2025-05, USD, channels such as Google Ads/LinkedIn/Email, regions North/South/East/West) with impressions, clicks, CTR, spend, leads, conversions, revenue, ROAS, CPA | **Not Ownly or food-delivery data. Don't use it as evidence about Ownly.** Its formulas are internally consistent: CTR, conversion rate, ROAS and CPA match 1000/1000 rows. But in 325 rows conversions exceed qualified leads, and all 8 channels have near-identical ROAS (7.8–10.4), which suggests a practice/synthetic dataset. Use it only to **demonstrate** digital funnel KPIs, and apply the same KPI definitions to our own survey-recruitment funnel (§5.4). |

### 5.2 KPIs to compute from our data (Tier 1)

"Survey" means the short survey. "Audit" means D1/D2.

| KPI (from the sheets) | Formula | Our version | Data | Hypothesis / question answered |
|---|---|---|---|---|
| **Price per statistical unit** (docx) | Total price of the bundle that forms one "unit" | Statistical unit = one single-person meal basket. **Price per basket = final payable** on each app | Audit | H2: which app's basket is cheaper? |
| **Average price per unit** (docx) | Revenue ÷ units | Median final payable per app across restaurants and slots | Audit | H2 |
| *(Price gap and win rate — research metrics)* | Ownly final payable − Swiggy/Zomato final payable, same restaurant/slot; win rate = % comparisons where Ownly is cheapest (tie ≤ ₹5) | Median gap (₹) and % wins, with and without coupons | Audit | **H2.3: is there a real saving after coupons?** |
| **Channel margin / customer selling price** (docx: Customer selling price = Supplier price ÷ (1 − customer margin %)) | Margin % = (selling price − supplier price) ÷ selling price | "App markup %" = (app menu price − verified in-restaurant price) ÷ app menu price. Only where a dated menu photo exists; otherwise don't compute | Audit (+ menu photo) | H1.3: is menu inflation real? |
| *(Fee share of bill — research metric)* | (Final payable − food subtotal) ÷ final payable | Non-food charges as % of what you pay, per app | Audit + test orders | H1 fee pain; H8 |
| **Market penetration %** (docx) | Category buyers ÷ population | % of people who started the survey and ordered delivery in the last 4 weeks (from screen-out counts). **Only "among reached 20–30s", never Hyderabad population.** | Survey screener | Context |
| **Brand penetration %** (docx) | Brand buyers ÷ population | % of all started respondents who have ever ordered on Ownly | Survey | H11 / early traction |
| **Penetration share %** (docx) | Brand penetration ÷ market penetration | % of delivery users who have tried Ownly | Survey (`own_tried`) | Early adoption in Gachibowli |
| *(Awareness → trial conversion)* | Tried ÷ aware | Of those aware of Ownly, % who ordered | Survey | **H11.3: say–do gap** |
| **Share of requirements %** (docx) | Brand purchases ÷ total category purchases by brand buyers | Ownly orders (4 weeks) ÷ all delivery orders (4 weeks), among Ownly triers | Survey | H12; **only if ≥ 10 Ownly triers** |
| **Heavy usage / weight index** (docx) | Avg category purchases by brand customers ÷ avg by all category customers | Mean orders in 4 weeks of Ownly triers ÷ mean of all respondents | Survey | Are Ownly triers heavy users? |
| **Market share decomposition** (docx: Share = Penetration share × Share of requirements × Usage index) | — | Ownly's order share **within our sample**, decomposed into "how many try" × "how much of their ordering" × "how heavy they are". Shows *which lever is weak*. | Survey | Strategy: fix trial, loyalty or target heavier users? |
| **Brand development index** (docx) | (Brand sales in group ÷ group size) ÷ (total brand sales ÷ total size) | Ownly trial rate among students vs professionals, relative to overall. BDI > 100 = over-indexes | Survey | H6 segment (directional; each group ≥ 20) |
| **Retention rate** (pdf) | (Customers at end − new) ÷ customers at start | **We can't observe start/end cohorts.** Proxy: repeat rate = % of Ownly triers with ≥ 2 Ownly orders in last 4 weeks; lapse = tried but 0 in last 4 weeks. **Label as proxy.** | Survey | H12 |

### 5.3 KPIs as clearly labelled scenarios (Tier 2 — illustrative, not findings)

| KPI | Formula | How to use honestly |
|---|---|---|
| **CAGR → compound monthly growth rate** (pdf) | (Final ÷ Start)^(1/N) − 1 | Bengaluru daily orders, as reported by media: ~5,000 (Mar 2026) → ~50,000 (Aug 2026), N = 5 months → (50,000 ÷ 5,000)^(1/5) − 1 ≈ **58% per month**. Label **MEDIA REPORT, single upstream source**; months approximate. **YoY is not applicable** (less than 1 year of history). |
| **Contribution per unit & break-even volume** (docx) | Contribution = Price − Variable cost; Break-even volume = Fixed costs ÷ Contribution | Ownly's revenue per order ≈ delivery fee (restaurants pay zero commission). Variable cost ≈ rider payout per order (**UNKNOWN**). Show a table for fee ₹0/₹15/₹30 × rider cost ₹30/₹45/₹60 → contribution per order. Shows that zero-commission + low fee likely means **negative contribution per order**, which supports users' "prices won't last" scepticism. All inputs are ASSUMPTIONS. |
| **Customer lifetime value** (pdf) | CLV = Margin × r ÷ (1 + d − r) | Scenario: margin per customer per month (assumed) × retention r (use the survey repeat-rate proxy as r, if n allows) at d = 1%/month. Point: **CLV collapses when retention is low**, so reliability (which drives retention) is worth more than extra discounts. |
| **Relative market share** (docx) | Brand share ÷ largest competitor's share | Only if a source gives Bengaluru shares for both Ownly and the leader. We have Ownly ~10% (media) but no verified leader share, so **don't compute**; mention as a data gap. |
| **Average acquisition cost** (pdf) | Acquisition spend ÷ new customers | Not computable. Note the observed **₹100-off first-order referral offer** as a per-customer acquisition incentive (CONSUMER-GENERATED). |

### 5.4 Digital funnel KPIs (the CSV's metric set) applied to our recruitment

| CSV KPI | Our equivalent (survey recruitment by channel) |
|---|---|
| Impressions | Group members reached, per post (estimate from group size) |
| CTR = clicks ÷ impressions | Survey link opens ÷ people reached (Google Forms doesn't count opens; use screen-out + completes as "starts") |
| Conversion rate = conversions ÷ clicks | Valid completes ÷ starts, per channel (from `meta_source`) |
| CPA = spend ÷ conversions | Cost per valid complete = ₹0 ÷ completes → ₹0. The **test-order** cost per observation is ₹900 ÷ 3 = ₹300 |
| ROAS = revenue ÷ spend | Not applicable (no revenue) |

In the report, use the CSV only in a short "metrics toolkit" appendix: compute channel-level CTR, conversion rate, CPA and ROAS, and show you'd use exactly these for Ownly's Gachibowli launch campaigns (which we cannot observe). **Flag the data-quality issue** (conversions > qualified leads in 325 rows).

### 5.5 KPIs NOT suitable (and why)

| KPI | Why not |
|---|---|
| Cannibalisation rate | Needs Rapido/Swiggy internal sales before and after a launch |
| Average retention cost | Needs company retention spend |
| YoY growth | Less than 1 year of Ownly history |
| Category development index by households | No household-level sales data |
| Total selling / marketing costs, target volume/revenue | Company cost data not available |
| Unit/revenue market share for Hyderabad | No Hyderabad order data exists publicly |

---

## 6. Final deliverable storyline for 17 September (12 slides)

1. The question, and the Starbucks Australia lesson (analogy only)
2. What Ownly claims vs what is verified (fact vs claim table)
3. Method, what we could and couldn't collect in 3 days, and why (ethics, time, ₹900)
4. Bengaluru benchmark from public customer voice: price attracts, reliability hurts (frequency × severity)
5. **Gachibowli price audit:** price per basket, gap after coupons, win rate, fee share, ETA, coverage
6. Test orders: promised vs actual (n = 3, anecdotal, labelled)
7. Survey: fee pain (PPI), switching threshold vs audit saving
8. Trade-offs: does ₹30 buy 15 minutes? Reliability? Restaurant choice? (shares with CIs)
9. Ownly funnel in Gachibowli: awareness → trial → repeat; market-share decomposition; students vs professionals BDI
10. **Bengaluru assumption → Gachibowli evidence → Transferable / Adapt / Unknown**
11. Recommendation (SCALE / ADAPT / TARGET SELECTIVELY) with confidence level, guardrails, what not to compete on
12. Limitations (n, convenience sample, 3 days, no Bengaluru survey) + next research (the full design already built)
