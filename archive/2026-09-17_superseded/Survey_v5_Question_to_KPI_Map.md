# Question → KPI Map: Survey v5

**Survey:** `Survey_v5_All_Cities.md` (built with `Survey_v5_Google_Form_Build_Guide.md`)
**KPIs:** `KPI_Framework_and_Survey_Validation.md` (K1–K9)
**Version:** 2026-09-16

Every question in the survey is listed once. For each: what it feeds, and exactly how it enters the formula. Questions that feed no KPI are marked **No KPI** with the job they do instead.

**The 9 KPIs, for reference**

| ID | KPI | Source |
|---|---|---|
| K1 | Penetration Share | Formulae Sheet 1 |
| K2 | Cannibalization Rate | Formulae Sheet 2 |
| K3 | Unit Market Share | Formulae Sheet 1 |
| K4 | Unit Share of Requirements | Formulae Sheet 1 |
| K5 | Retention Rate | Formulae Sheet 2 |
| K6 | Sean Ellis PMF score | Syllabus Unit 6 |
| K7 | Conversion Rate | Marketing Metrics dataset |
| K8 | Price per Statistical Unit | Formulae Sheet 1 |
| K9 | Brand Development Index | Formulae Sheet 1 |

---

## 1. Every question, mapped

The same question ID appears on all three city paths (Hyderabad, Bengaluru, Other city). In the export they arrive as separate columns and are merged back into one field during cleaning.

### Screening and structure

| ID | Question (exact) | Asked on | Feeds | Exactly how it is used |
|---|---|---|---|---|
| **CITY** | Which city do you live, study or work in on most days? | All | **Every KPI** | Splits every KPI into the three columns of the scorecard: Bengaluru (benchmark), Hyderabad (target), Other cities (baseline). Without it, no transfer comparison exists. |
| **LOC** | Which area? / Which city? | All | **K9** | Group variable for the area version of BDI (Gachibowli area vs rest of Hyderabad; Koramangala/HSR/BTM vs rest of Bengaluru). Also powers the "Focus areas" filter on the dashboard. |
| **AGE** | How old are you? | All | **No KPI** | **Screening.** Keeps the sample to 20–30, the group in the problem statement. Under 20 and over 30 are routed out, so their answers never enter a KPI. Without it, share and penetration would mix age groups that behave differently. |
| **OCC** | Which best describes you right now? | All | **K9** | Group variable for the segment version of BDI (students vs working professionals), and the "Segment" filter that re-computes every KPI. |

### The order counts (the engine behind five KPIs)

| ID | Question (exact) | Feeds | Exactly how it is used |
|---|---|---|---|
| **ORD** | In the last 4 weeks, did you order food online for delivery at least once (any app, or directly from a restaurant)? | **K1** | **Denominator of K1:** people who ordered food online in the last 4 weeks. Also routes non-orderers past the order questions. |
| **N_OW** | Ownly (Rapido's food app, or food inside the Rapido app): how many orders in the last 4 weeks? | **K1, K3, K4, K5, K9** | K1 numerator (respondents with ≥ 1 Ownly order) · K3 numerator (total Ownly orders) · K4 numerator · K5 "customers at end" · K9 the per-respondent Ownly orders that the index compares. Also weights K2. |
| **N_SW** | Swiggy: how many orders in the last 4 weeks? | **K3, K4** | Part of the denominator: all food orders. Also gives Swiggy's own market share on the K3 chart. |
| **N_ZO** | Zomato: how many orders in the last 4 weeks? | **K3, K4** | Same as N_SW, for Zomato. |
| **N_OT** | Any other way (Toing, Magicpin, EatSure, or directly from a restaurant): how many orders in the last 4 weeks? | **K3, K4** | Completes the denominator so shares add to 100%. Shows the "other apps & direct" slice. |

> These four numbers are why the survey asks for counts instead of bands. Share, share of requirements, retention and BDI are all ratios of orders, so they need real counts.

### The last order (price)

| ID | Question (exact) | Feeds | Exactly how it is used |
|---|---|---|---|
| **LO_APP** | Which app did you use for your most recent food delivery order? | **K8** | Splits the price by app: Ownly vs Swiggy vs Zomato vs other. Also used in quality check C1 (a last order on an app the respondent says they used 0 times). |
| **LO_AMT** | What was the total amount you paid for it? | **K8** | The value itself: the median of these amounts is the price per statistical unit. |
| **LO_PPL** | How many people was that order for? | **K8** | Defines the statistical unit. Only orders for "Just me" count, so a group order doesn't inflate the price. Also used in quality check C6. |

### The Ownly funnel

| ID | Question (exact) | Feeds | Exactly how it is used |
|---|---|---|---|
| **OW_STATUS** | Ownly is a food delivery app by Rapido… Before today, which of these is true for you? | **K7** | Builds the whole funnel: "heard" = aware, "opened or ordered" = clicks, "ordered" = conversions. **K7 = ordered ÷ (opened + ordered).** Also routes people to the right follow-up page, and cross-checks N_OW (quality check C2). |
| **SRC** | Where did you first hear about Ownly? | **K7 (split)** | Splits the conversion rate by channel: Rapido app, Instagram/YouTube, friends, hoardings, news. Shows which channel brings people who actually order, not just people who have heard. |

### Ownly users

| ID | Question (exact) | Feeds | Exactly how it is used |
|---|---|---|---|
| **US_WHERE** | Where have you ordered on Ownly? *(Hyderabad path)* / Where did you order on Ownly? *(Other city)* | **K2, K4, K5, K6 (filter)** | Keeps city KPIs honest: a Hyderabad respondent who only ordered in Bengaluru is excluded from Hyderabad's user KPIs. Also quality check C5. |
| **US_FIRST** | When did you place your FIRST Ownly order? | **K5** | The "new customers" term of the retention formula: first order inside the last 4 weeks = a new customer, not a retained one. Also quality checks C4 and C5. |
| **US_PRIOR** | How many Ownly orders did you place in the 4 weeks BEFORE the last 4 weeks (roughly 5–8 weeks ago)? | **K5** | The "customers at start" term: ≥ 1 order in the earlier period. Without it, retention has no starting cohort. |
| **US_ALT** | Think of your most recent Ownly order. If Ownly didn't exist, what would you most likely have done instead? | **K2** | The whole KPI: the share of Ownly orders that would otherwise have gone to Swiggy/Zomato, weighted by N_OW. The other answers split into "other channels" and "new orders". |
| **US_PMF** | How would you feel if you could no longer use Ownly? | **K6** | "Very disappointed" ÷ all Ownly users who answered, against the 40% benchmark. |

### Driver questions (no KPI of their own)

These explain *why* a KPI is high or low. They're the "what must Ownly change" half of the problem statement.

| ID | Question (exact) | Asked on | Purpose | Explains |
|---|---|---|---|---|
| **NH_TRIGGER** | Which ONE thing would most make you try Ownly for an order? *(Other city: If Ownly launched in your city…)* | People who never heard of Ownly | Says which lever would raise trial: first-order discount, restaurants, proof it's cheaper, refund promise, word of mouth, payment method, or nothing | **K1** |
| **HD_REASON** | What's the MAIN reason you haven't opened it? | Heard, never opened | Names the block between awareness and curiosity: trust, "not really cheaper", "doesn't reach my area", app fatigue | **K7** (top of funnel) |
| **OP_STOP** | When you looked, what MAINLY stopped you from ordering? | Opened, didn't order | Names the block at the moment of buying: restaurants missing, price not lower, coupon elsewhere, no delivery to the address, delivery time, payment | **K7** (the conversion step) |
| **US_LAPSE** | If you order on Ownly less than you used to, what's the MAIN reason? | Bengaluru Ownly users | Says what breaks loyalty in the mature market: restaurants, failed deliveries, refunds, prices no longer lower, offers ended, went back to a membership | **K5** |
| **US_CHANGE** | What ONE change would make you order more on Ownly? | Ownly users | The single product priority named by real users | **K4, K5** |

### Follow-up

| ID | Question (exact) | Feeds | Purpose |
|---|---|---|---|
| **INTERVIEW** | Optional: Can we message you for a 10-minute chat about how you order food? | **No KPI** | **Recruitment.** Supplies interviewees for the "why" behind the numbers, and the 14-day follow-up that measures true retention (the second time point K5 can't get from one survey). The only optional question. |

---

## 2. The reverse view: what each KPI is built from

| KPI | Numerator | Denominator | Splits and filters |
|---|---|---|---|
| **K1 Penetration Share** | Respondents with N_OW ≥ 1 | Respondents with ORD = Yes | CITY · OCC · LOC |
| **K2 Cannibalization Rate** | Ownly orders (N_OW) whose US_ALT = "Ordered the same on Swiggy or Zomato" | All Ownly orders of users who answered US_ALT | CITY · US_WHERE filter |
| **K3 Unit Market Share** | N_OW (and N_SW, N_ZO, N_OT for the other slices) | N_SW + N_ZO + N_OW + N_OT | CITY · OCC |
| **K4 Share of Requirements** | N_OW, among users with N_OW ≥ 1 | Their total orders | CITY · US_WHERE filter |
| **K5 Retention Rate** | (Users with N_OW ≥ 1) − (users with US_FIRST = "In the last 4 weeks") | Users with US_PRIOR ≥ 1 | CITY · US_WHERE filter |
| **K6 Sean Ellis PMF** | US_PMF = "Very disappointed" | Users who answered US_PMF | CITY · OCC |
| **K7 Conversion Rate** | OW_STATUS = "I've ordered on Ownly" | OW_STATUS = opened or ordered | CITY · SRC (channel) |
| **K8 Price per Statistical Unit** | Median LO_AMT where LO_PPL = "Just me" | — (a median, by LO_APP) | CITY · LO_APP |
| **K9 BDI** | Ownly orders per respondent in a group (N_OW) | Ownly orders per respondent in the city | Group = OCC or LOC |

---

## 3. Questions that feed no KPI, and why they stay

| Question | Why it's in the survey | What we'd lose without it | Could it be cut? |
|---|---|---|---|
| **AGE** | Screening: keeps the sample at 20–30 | KPIs would mix ages with different ordering behaviour, and the sample would no longer match the problem statement | No |
| **CITY** | Structure: routes to the right path and labels the row | The transfer comparison, which is the whole study | No |
| **NH_TRIGGER** | Driver for K1 | We'd know trial is low but not what would lift it | No: it's the main action question for non-users |
| **HD_REASON** | Driver for K7 | A leak between "heard" and "opened" with no explanation | No |
| **OP_STOP** | Driver for K7 | The most actionable answer in the survey: why people who wanted to order didn't | No |
| **US_LAPSE** | Driver for K5 | Retention without a reason; Bengaluru's warnings for Hyderabad would be lost | No |
| **US_CHANGE** | Driver for K4 and K5 | No user-voted priority for what to fix first | Could be cut if the form runs long |
| **INTERVIEW** | Recruitment for interviews and the 14-day follow-up | No second time point for true retention, and no interviewees | Could be cut, at the cost of the follow-up |

**Nothing else is asked.** Every other question feeds at least one KPI. Questions from earlier drafts that fed nothing (membership, biggest annoyance, app-vs-restaurant price, maximum delivery fee, trade-offs, switching threshold, price-display preference, price durability, first-order discount, offers on recent orders, first-order outcome) were removed in v5.

---

## 4. Double duty: questions used by the quality checks

| Check | Flag when | Questions used |
|---|---|---|
| C1 | The last order is on an app the respondent says they used 0 times | LO_APP + N_SW / N_ZO / N_OW |
| C2 | Ownly orders ≥ 1 but the status isn't "I've ordered on Ownly" | N_OW + OW_STATUS |
| C3 | "Yes, I ordered" but all counts are 0, or the total is above 60 | ORD + the four counts |
| C4 | First order in the last 4 weeks, yet orders 5–8 weeks ago | US_FIRST + US_PRIOR |
| C5 | Hyderabad-only user whose first order is older than the Hyderabad launch | CITY + US_WHERE + US_FIRST |
| C6 | A meal for one costing more than ₹1,500 | LO_PPL + LO_AMT |

A response with 2 or more flags is excluded before any KPI is computed.

---

## 5. Coverage by city path

| KPI | Hyderabad | Bengaluru | Other city | Why |
|---|---|---|---|---|
| K1, K3 | Yes | Yes | Yes | Counts asked on every path |
| K8 | Yes | Yes | Yes (no Ownly) | Ownly rarely appears as the last order outside its two cities |
| K7 | Yes | Yes | — | The Other-city path has no "opened it" option, since Ownly isn't available |
| K2, K4, K6, K9 | Likely directional | Yes | — | They need Ownly users; Hyderabad has few so far |
| K5 | Not yet | Yes | — | Retention needs an earlier 4-week period; Ownly launched in Hyderabad in September 2026 |

**What this means for the report:** Bengaluru carries the loyalty KPIs (K4, K5, K6) and is the benchmark. Hyderabad carries adoption and funnel KPIs (K1, K3, K7) plus price (K8). The gap between the two is the transfer finding.

---

## 6. Field names in the CSV export

The dashboard renames each question to a short field. Useful when reading the Google Sheet.

| Field | Question |
|---|---|
| `city`, `loc`, `age`, `occ` | CITY, LOC, AGE, OCC |
| `ord` | ORD |
| `n_sw`, `n_zo`, `n_ow`, `n_ot` | The four order counts |
| `lo_app`, `lo_amt`, `lo_ppl` | The last-order questions |
| `ow` | OW_STATUS |
| `trig`, `src`, `hd`, `stop` | NH_TRIGGER, SRC, HD_REASON, OP_STOP |
| `where`, `first`, `prior`, `alt`, `pmf`, `lapse`, `change` | The Ownly-user questions |

If the dashboard's **Data and quality** panel lists a field as missing, that question's title was reworded in the form. Appendix A1 of the build guide lists the wording each field needs.
