# KPI Framework: Ownly Market-Transfer Study (v3, FINAL)

**Version:** 2026-09-16 (v3). Replaces v1 and v2 (20 KPIs).
**Survey:** `Survey_v5_All_Cities.md`, one form with Bengaluru / Hyderabad / Other city paths. Question IDs below refer to v5.
**Problem statement:** Will Ownly's Bengaluru pitch pull 20–30-year-old students and working professionals in and around Gachibowli (Hyderabad) away from Swiggy/Zomato? If not, what must Ownly change?

---

## 0. Answers to the two questions asked

**Were all 20 KPIs dashboard-worthy? No.** A KPI is only worth a dashboard tile if we can actually collect it at a usable sample size, and a reader learns something different from it than from the other tiles. Of the previous 20:

| Problem with the previous 20 | Examples | Count |
|---|---|---|
| **Not collectable by us.** They need Ownly's internal costs, spend or a year of history. The survey could only give one side of the formula, so the tile would show an assumption, not data. | Contribution per Unit, Break-Even, CLV, Average Acquisition Cost / CPA, Average Retention Cost, YoY Growth / CAGR | 6 |
| **Redundant.** Same inputs, same story as a KPI we keep. | Brand Penetration, Market Penetration, Relative Market Share, Revenue SoR, Revenue Market Share, Usage Index, CDI | 7 |
| **Weak data.** Customers can't observe the input. | Margin % (restaurant in-store price), Average Price per Unit (distorted by basket size), CTR (awareness inflated by who we recruit) | 3 |

**Was survey v4 good enough? No, for two reasons:**
1. **It only covered Hyderabad.** The problem is a *transfer* question (does Bengaluru's success carry over?), so the same KPIs must be measured in Bengaluru as the benchmark.
2. **The 24-response pilot (15–16 Sep) could not produce a single KPI reliably.** Only 11 respondents were eligible; there were no per-app order counts and no Hyderabad Ownly users; and build errors (an unfilled placeholder, missing validation, blank titles) crept in.

Survey v5 fixes both. It has a city-first branch, and every question feeds or explains one of **9 KPIs**.

---

## 1. How the 9 were chosen

A metric became a KPI only if it passed **all four** tests:

| Test | Question |
|---|---|
| **T1 Course metric** | Is it a standard formula from the course materials (Formulae Sheet 1, Sheet 2, Marketing Metrics dataset), or, for one exception, the Sean Ellis test named in the syllabus? |
| **T2 Actually collectable** | Can survey v5 supply **every input** of the formula, from real respondents, at n ≥ 30 in at least Bengaluru and Hyderabad? |
| **T3 Insight** | Would a reader make a different call depending on its value, especially **Hyderabad vs Bengaluru**? |
| **T4 Not redundant** | Does it say something no other chosen KPI says? |

**Priority order** = how directly the KPI answers "is Ownly pulling customers away, and will it last?"

---

## 2. The 9 KPIs

| # | KPI | Source | The question it answers | Survey inputs | Bengaluru | Hyderabad | Other city |
|---|---|---|---|---|---|---|---|
| **K1** | **Penetration Share** | Formulae Sheet 1 | Of people who order food online, how many use Ownly? | ORD, N_OW | ✅ | ✅ | ✅ (≈ 0, baseline) |
| **K2** | **Cannibalization Rate** | Formulae Sheet 2 (Ch. 4) | Are Ownly's orders taken from Swiggy/Zomato, or are they new orders? | US_ALT, N_OW | ✅ | ◐ few users | — |
| **K3** | **Unit Market Share** | Formulae Sheet 1 | What share of all food orders goes to Ownly vs Swiggy vs Zomato? | N_SW, N_ZO, N_OW, N_OT | ✅ | ✅ | ✅ (no Ownly) |
| **K4** | **Unit Share of Requirements** | Formulae Sheet 1 | Do Ownly users give it a real share of their ordering? | N_OW, tot (users) | ✅ | ◐ few users | — |
| **K5** | **Retention Rate** | Formulae Sheet 2 (Ch. 5) | Do Ownly customers keep ordering from one month to the next? | US_PRIOR, N_OW, US_FIRST | ✅ | ✗ not yet (launched < 5 weeks ago) | — |
| **K6** | **Sean Ellis PMF score** | External (syllabus Unit 6) | Has Ownly become essential to its users? | US_PMF | ✅ | ◐ few users | ◐ |
| **K7** | **Conversion Rate** | Marketing Metrics dataset | Of people who opened Ownly, how many ordered? | OW_STATUS | ✅ | ✅ | — |
| **K8** | **Price per Statistical Unit** | Formulae Sheet 1 | What does one solo meal actually cost on each app? | LO_APP, LO_AMT, LO_PPL | ✅ | ✅ (Ownly ◐) | ✅ (no Ownly) |
| **K9** | **Brand Development Index (BDI)** | Formulae Sheet 1 | In which segment and area is Ownly strongest? | OCC, LOC, N_OW | ✅ | ◐ trial-based | — |

✅ = measurable at the target sample · ◐ = measurable but likely n < 30 (shown as "directional") · ✗ = not measurable yet · — = not applicable

**Five come from Formulae Sheet 1** (K1, K3, K4, K8, K9). Four come from elsewhere because Sheet 1 has no measure of where volume comes from (K2), whether customers stay (K5), where the funnel leaks (K7), or whether a product is essential (K6). Each is explained in its card.

---

## 3. KPI cards

### K1 · Penetration Share (Formulae Sheet 1)
- **Formula:** customers who purchased the brand ÷ customers who purchased a product in the category.
- **How we measure it:** `n(N_OW ≥ 1) ÷ n(ORD = Yes)`, by city.
- **Why chosen:** it's the first proof of "pull". Ownly can't take customers from Swiggy/Zomato unless people who already order online start using it. It's collectable in all three cities, with no assumptions.
- **Insight it produces:** **the transfer gap.** Hyderabad's penetration share next to Bengaluru's, allowing for Hyderabad being weeks old, shows how far Hyderabad is from the benchmark. The Other-city value (≈ 0) confirms the baseline.
- **Dashboard visual:** 3 KPI tiles (Bengaluru · Hyderabad · Other) with n and 95% CI; Hyderabad also split Gachibowli area vs rest.

### K2 · Cannibalization Rate (Formulae Sheet 2, Chapter 4)
- **Formula:** sales lost from existing products ÷ sales of the new product.
- **How we measure it:** among Ownly users, the share of Ownly orders that would otherwise have gone to Swiggy/Zomato: `Σ max(N_OW,1) × [US_ALT = "Ordered the same on Swiggy or Zomato"] ÷ Σ max(N_OW,1)`. The remainder splits into "new to delivery" (cook / eat out / skip) and "other channels".
- **How we apply the formula:** Rapido had no earlier food product, so "existing products" are the incumbent apps the customer already used. The formula is unchanged.
- **Why chosen:** it's the problem statement in one number. "Pulling customers away from Swiggy/Zomato" literally means Ownly orders that used to be Swiggy/Zomato orders. It also tests Ownly's own claim that it is *expanding* online ordering.
- **Insight it produces:** high → a head-on switching play, so expect incumbent retaliation. Low, with a high "new to delivery" share → market expansion.
- **Dashboard visual:** 100% stacked bar per city: from Swiggy/Zomato · from other channels · new orders.
- **Collectability:** Bengaluru ✅; Hyderabad directional until Ownly users reach n ≥ 30.

### K3 · Unit Market Share (Formulae Sheet 1)
- **Formula:** unit sales ÷ total market unit sales.
- **How we measure it:** `Σ N_OW ÷ Σ tot` (and the same for Swiggy, Zomato and other), by city.
- **Why chosen:** it is the overall result of adoption (K1) and depth (K4). It's the one number that shows Ownly's standing against Swiggy and Zomato in each city.
- **Insight it produces:** the Bengaluru vs Hyderabad share gap. The Other-city split shows the incumbents' "normal" share without Ownly.
- **Dashboard visual:** stacked bar of order share by app × city.
- **Check:** on the Formulae Sheet, Share = Penetration Share × Share of Requirements × Usage Index. We don't track the usage index as a KPI, but the dashboard uses this identity as a data-quality check.

### K4 · Unit Share of Requirements (Formulae Sheet 1)
- **Formula:** brand purchases ÷ total category purchases by brand buyers.
- **How we measure it:** `Σ N_OW ÷ Σ tot` over respondents with `N_OW ≥ 1`, by city.
- **Why chosen:** trial isn't switching. SoR shows whether Ownly users moved a real share of their orders or use Ownly as a side app. Bengaluru social posts suggest "small orders Ownly, large orders Swiggy", which SoR can confirm or reject.
- **Insight it produces:** high penetration + low SoR → people try Ownly but don't rely on it (look at US_CHANGE for why). High SoR → Ownly wins its users; growth then depends on penetration.
- **Dashboard visual:** gauge per city with SoR of Swiggy and Zomato among the same users for contrast.

### K5 · Retention Rate (Formulae Sheet 2, Chapter 5)
- **Formula:** (customers at end − new customers) ÷ customers at start × 100.
- **How we measure it:** among Ownly users:

| Formula term | Survey definition |
|---|---|
| Customers at start | US_PRIOR ≥ 1 (ordered 5–8 weeks ago) |
| Customers at end | N_OW ≥ 1 |
| New customers | US_FIRST = "In the last 4 weeks" |

  Report the cohort check alongside: `n(US_PRIOR ≥ 1 and N_OW ≥ 1) ÷ n(US_PRIOR ≥ 1)`.
- **Why chosen:** launch offers buy trial; retention shows whether the pitch holds after the first orders. It is the strongest "will it last?" metric we can collect.
- **Insight it produces:** Bengaluru retention is the **benchmark Hyderabad must reach**. US_LAPSE (Bengaluru) names what breaks retention, e.g. restaurants missing, failed deliveries, offers ended. Those are exactly the risks to fix before scaling in Hyderabad.
- **Collectability:** Bengaluru ✅. **Hyderabad ✗ for now:** Ownly launched there < 5 weeks ago, so almost nobody has a "start" period. The dashboard shows "not measurable yet (launched Sep 2026)", which is honest and itself a finding, rather than a misleading number.
- **Dashboard visual:** Bengaluru tile + a lapse-reason bar chart.

### K6 · Sean Ellis PMF score (external; course syllabus Unit 6)
- **Formula:** % of users who would be "very disappointed" if they could no longer use the product. ≥ 40% = product–market fit signal.
- **How we measure it:** `n(US_PMF = "Very disappointed") ÷ n(US_PMF answered)`, by city.
- **What it measures, and why it's needed although it's not on the formula sheets:** none of the course formulas measure whether a product is *essential* to its users. Retention can be propped up by offers or habit. For a SCALE vs ADAPT decision on a new entrant, product–market fit is the central question, and the syllabus names this test.
- **Insight it produces:** Bengaluru ≥ 40% → the proposition has real fit where it matured. Read with K5: high PMF + low retention = an operations problem, not a proposition problem.
- **Dashboard visual:** tile per city with the 40% benchmark line.

### K7 · Conversion Rate (Marketing Metrics dataset)
- **Formula (dataset):** conversions ÷ clicks.
- **How we measure it:** clicks = opened or ordered Ownly; conversions = ordered. `n(OW_STATUS = ordered) ÷ n(OW_STATUS ∈ {opened, ordered})`, by city.
- **What it measures, and why it's needed although it's not on Formulae Sheet 1:** Sheet 1 has no funnel metric. Conversion Rate isolates the step where a **curious** customer decides not to buy, which is where Ownly's product (restaurants, price, serviceability) is judged. OP_STOP names the exact blocker.
- **Why not CTR as well:** awareness counts depend heavily on who we recruit, so CTR would mostly measure our sharing channels. Conversion among people who opened the app is far less affected.
- **Insight it produces:** low Hyderabad conversion with "it didn't deliver to my address" or "my restaurants weren't there" → **supply/serviceability must come before marketing**. By channel (SRC): which source brings people who actually order.
- **Dashboard visual:** funnel (heard → opened → ordered) per city with the conversion rate labelled, plus a bar of OP_STOP reasons.

### K8 · Price per Statistical Unit (Formulae Sheet 1)
- **Formula:** total price of the bundle of SKUs comprising one statistical unit.
- **Statistical unit (our definition):** **one delivered meal for one person.**
- **How we measure it:** median LO_AMT where LO_PPL = "Just me", by LO_APP and city.
- **Why chosen:** Ownly's pitch is a lower price. This is the course metric that compares **like with like**: a solo meal, on real bills respondents paid. Average price per order was dropped because group orders distort it.
- **Insight it produces:** whether a solo meal on Ownly is actually cheaper than on Swiggy/Zomato in the same city. The Other-city value shows what incumbents charge where Ownly isn't present.
- **Dashboard visual:** dot/box plot of solo-meal price by app × city.
- **Collectability:** Swiggy/Zomato ✅ in every city; Ownly ✅ in Bengaluru, directional in Hyderabad. (If the team runs the competitor price audit, it can be shown alongside as the same-basket check, but the KPI itself comes from the survey.)

### K9 · Brand Development Index (BDI) (Formulae Sheet 1)
- **Formula:** (brand sales to group ÷ households in group) ÷ (total brand sales ÷ total households). We use respondents instead of households, which the formula allows.
- **How we measure it:** for each group g, `BDI_g = (Σ N_OW in g ÷ n_g) ÷ (Σ N_OW ÷ n) × 100`, by city. Groups:
  - **segment** (OCC: students vs working professionals)
  - **area** (LOC: e.g. Bengaluru pilot areas vs rest; Gachibowli area vs rest of Hyderabad)

  If a group has < 10 Ownly users, use trial BDI: `(% ordered on Ownly in g) ÷ (% overall) × 100`.
- **Why chosen:** the problem statement names two segments, and the decision includes TARGET SELECTIVELY. BDI is the course metric for where a brand over-performs (> 120) or under-performs (< 80).
- **Insight it produces:** "In Bengaluru, Ownly over-indexes with [segment] in [area]." That tells Hyderabad which group and area to target first.
- **Dashboard visual:** heatmap, segments × areas, per city.

---

## 4. Driver questions (not KPIs; they explain the KPIs)

| Driver | Asked to | Explains |
|---|---|---|
| NH_TRIGGER | Never heard of Ownly | What would lift K1 among the unaware |
| SRC | Anyone aware of Ownly | K7 by channel |
| HD_REASON | Heard, never opened | Why awareness doesn't become interest (K1) |
| OP_STOP | Opened, didn't order | Why interest doesn't convert (K7) |
| US_LAPSE (Bengaluru) | Ownly users | Why retention drops (K5) |
| US_CHANGE | Ownly users | What would raise SoR and retention (K4, K5) |

---

## 5. Metrics considered and dropped

| Metric (source) | Why dropped |
|---|---|
| Brand Penetration, Market Penetration (Sheet 1) | Same inputs as Penetration Share; the Market Penetration base is only the "orders online?" count, shown as context on K1's tile |
| Relative Market Share (Sheet 1) | Visible directly on the K3 market-share chart; a separate tile adds nothing |
| Revenue Market Share, Revenue SoR (Sheet 1) | Need recalled average ₹ per order per app, which the pilot showed is too noisy; unit versions are kept |
| Usage Index, CDI (Sheet 1) | Diagnostic; used only as the K3 identity check and the BDI context, with too few Ownly users for stable values |
| Average Price per Unit, Unit Price per Stat. Unit (Sheet 1) | Distorted by basket size; K8 (solo meal) answers the same question cleanly |
| Margin %, Supplier/Customer Selling Price (Sheet 1) | Customers can't observe the restaurant's in-store price; only a perception would be collected |
| Contribution per Unit, Contribution Margin, Break-Even, Unit Margin, Target Volume/Revenue, cost totals (Sheet 1) | Need Ownly's costs; not collectable |
| CLV, Average Acquisition Cost, Average Retention Cost (Sheet 2) | Need company margin or spend; the survey could only give assumptions |
| YoY Growth, CAGR (Sheet 2) | Ownly is < 1 year old, and Hyderabad has no prior period |
| CTR, CPA, ROAS (Marketing Metrics dataset) | CTR reflects our recruitment; CPA/ROAS need ad spend and revenue |

---

## 6. Dashboard vision (what the 9 KPIs turn into)

**Principle:** every page answers one problem-statement question, always showing **Bengaluru (benchmark) · Hyderabad (target) · Other (baseline)** side by side, with n on every tile.

| Page | Question | KPIs and visuals | Example insight title (filled only when data supports it) |
|---|---|---|---|
| **1. Overview** | Is Ownly pulling people away, and does it transfer? | 9 KPI tiles × 3 city columns; traffic-light "Hyderabad vs Bengaluru" column | "Hyderabad has reached X% of Bengaluru's penetration share in its first weeks" |
| **2. Pull** | Where do Ownly's orders come from? | K1 tiles, K3 stacked share bars, K2 source-of-volume bars | "Y% of Ownly orders in Bengaluru came from Swiggy/Zomato" |
| **3. Loyalty** | Do the users it wins stay? | K4 gauge, K5 Bengaluru tile + US_LAPSE reasons, K6 with 40% line | "Bengaluru users give Ownly Z% of their orders, but lapse because of …" |
| **4. Funnel** | Where does interest leak? | Heard → opened → ordered funnel by city with K7; OP_STOP and HD_REASON bars; K7 by SRC | "In Hyderabad, most people who open Ownly don't order because …" |
| **5. Price** | Is the price pitch visible in real bills? | K8 solo-meal price by app × city | "A solo meal on Ownly costs ₹A vs ₹B on Swiggy in Bengaluru" |
| **6. Target** | Who should Ownly target first in Hyderabad? | K9 heatmap (segment × area), Bengaluru vs Hyderabad | "In Bengaluru, Ownly over-indexes with working professionals in pilot areas (BDI 140)" |

**Display rules:**
- **Value shown** when n ≥ 30.
- **"Directional (n = …)"**, greyed, when n is 10–29.
- **"Not enough data yet"** when n < 10.
- **"Not measurable yet"** for Hyderabad Retention.
- Every % carries a 95% Wilson CI.

---

## 7. What the 24-response pilot showed

The pilot used an earlier form: v3 main questions plus the v4 Ownly block. **All 24 responses, pilot only, not findings:**

| KPI | Pilot result | Why it can't be used |
|---|---|---|
| K1 Penetration Share | 1 of 24 had ordered on Ownly (in Bengaluru) | No per-app order counts; 13 of 24 were out of scope (age or city) |
| K3, K4, K9 | Not computable | No per-app order counts |
| K5 Retention | Not computable | 1 Ownly user |
| K2 Cannibalization | 1 answer ("gone out to eat") | n = 1 |
| K6 Sean Ellis | Not asked | Question missing from the built form |
| K7 Conversion Rate | Funnel 17 never heard → 5 heard → 1 opened → 1 ordered | n = 2 at the "opened" step |
| K8 Price per Stat. Unit | 15 solo orders, but amounts in bands and app answered by only 12 | Bands, and the app question added mid-way |

**Lessons built into v5:**
- Ask for order counts as numbers.
- Branch by city and include Bengaluru.
- Set routing and validation; use no placeholders.
- Actively recruit Ownly users in Bengaluru.

---

## 8. Google Sheets formulas (clean tab; `keep` = passed quality checks)

| KPI | Formula (add `city,"Bengaluru"` etc. to each COUNTIFS/SUMIFS for the city split) |
|---|---|
| K1 Penetration Share | `=COUNTIFS(keep,TRUE,n_ow,">=1")/COUNTIFS(keep,TRUE,ord,"Yes")` |
| K2 Cannibalization Rate | `=SUMPRODUCT((keep=TRUE)*(ow_status="I've ordered on Ownly")*(us_alt="Ordered the same on Swiggy or Zomato")*IF(n_ow>=1,n_ow,1))/SUMPRODUCT((keep=TRUE)*(ow_status="I've ordered on Ownly")*(us_alt<>"")*IF(n_ow>=1,n_ow,1))` (enter as array formula) |
| K3 Unit Market Share (Ownly) | `=SUMIFS(n_ow,keep,TRUE)/SUMIFS(tot,keep,TRUE)` |
| K4 Unit SoR | `=SUMIFS(n_ow,keep,TRUE,n_ow,">=1")/SUMIFS(tot,keep,TRUE,n_ow,">=1")` |
| K5 Retention Rate | `=(COUNTIFS(keep,TRUE,ow_status,"I've ordered on Ownly",n_ow,">=1")-COUNTIFS(keep,TRUE,us_first,"In the last 4 weeks"))/COUNTIFS(keep,TRUE,us_prior,">=1")*100` |
| K6 Sean Ellis | `=COUNTIFS(keep,TRUE,us_pmf,"Very disappointed")/COUNTIFS(keep,TRUE,us_pmf,"<>")` |
| K7 Conversion Rate | `=COUNTIFS(keep,TRUE,ow_status,"I've ordered*")/(COUNTIFS(keep,TRUE,ow_status,"I opened*")+COUNTIFS(keep,TRUE,ow_status,"I've ordered*"))` |
| K8 Price per Stat. Unit (Swiggy) | `=MEDIAN(FILTER(lo_amt,keep=TRUE,lo_ppl="Just me",lo_app="Swiggy"))` |
| K9 BDI (students) | `=(SUMIFS(n_ow,keep,TRUE,segment,"student")/COUNTIFS(keep,TRUE,segment,"student"))/(SUMIFS(n_ow,keep,TRUE)/COUNTIFS(keep,TRUE))*100` |
| Wilson 95% CI (k in B1, n in B2) | Low `=((B1/B2)+1.96^2/(2*B2)-1.96*SQRT((B1/B2)*(1-B1/B2)/B2+1.96^2/(4*B2^2)))/(1+1.96^2/B2)` · High: `+1.96*SQRT` |

---

## 9. Limits (for the limitations slide)

1. **Sample, not market.** All KPIs describe our respondents in each city, not city-wide figures.
2. **Recall.** Order counts rely on memory. The order-history prompt and consistency checks C1–C6 limit this.
3. **Hyderabad is weeks old.** Retention isn't measurable there yet, and user-based KPIs (K2, K4, K6) may stay directional. Bengaluru is the benchmark for what "good" looks like.
4. **Stated answers.** K2 (what they would have done) and K6 (disappointment) are stated, not observed.
5. **Recruitment.** Messages never mention Ownly, but Bengaluru Ownly users must be actively found. Report where they were recruited.
