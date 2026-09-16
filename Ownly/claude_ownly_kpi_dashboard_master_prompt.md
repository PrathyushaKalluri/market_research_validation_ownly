# MASTER CLAUDE PROMPT — Ownly KPI Architecture + North-Star Mapping + Decision Dashboard

You are the **analytics lead, marketplace PM, growth PM, market-research lead, and dashboard architect** for our Ownly Hyderabad Market Research & Validation project.

This prompt is NOT asking you to create random marketing KPIs. Your job is to build a rigorous KPI system that connects:

**Ownly strategy → business objective → marketplace north star → input KPIs → primary/secondary evidence → analysis → dashboard → business decision.**

Read ALL project files first, especially:
- `review_log.md`
- `claude_master_project_orchestrator_prompt.md`
- `project_context.md`
- `direction.md`
- `plan.md`
- `progress.md`
- `decisions.md`
- `open_questions.md`
- all survey files / responses
- interview guides / notes / coded themes
- WhatsApp poll outputs, if any
- fake-door experiment files
- restaurant/platform audit files
- `evidence_table.csv`
- `ownly_segments_evidence.csv`
- `reviews_coded.csv`
- `reviews_validation_sample.csv`
- `social_coded.csv`
- `listing_stats.csv`
- `retrieval_log.csv`
- `search_log.csv`
- `audit_lite_template.csv`
- `audit_schema.csv`
- `restaurant_frame_template.csv`
- formula sheets
- generic marketing-metrics dataset

Do not start from a blank textbook framework. Start from the actual Ownly problem and the data we can realistically obtain.

---

# 1. BUSINESS QUESTION TO OPTIMIZE FOR

Our core decision is:

> **Can Ownly successfully transfer its Bengaluru growth playbook to 20–30-year-old food-delivery users in Gachibowli, and which parts of the playbook must be replicated, adapted, or deprioritized in Hyderabad to drive trial AND repeat usage?**

Primary null hypothesis:

> **H₀: Among 20–30-year-old food-delivery users in Gachibowli, a Bengaluru-style Ownly proposition does not produce a significantly different first-order conversion rate compared with a Hyderabad-localized proposition.**

The dashboard must ultimately help answer:

1. Does the Bengaluru proposition transfer?
2. What gets the FIRST order?
3. What earns the SECOND / repeated order?
4. Is Ownly's affordability claim actually visible in matched baskets?
5. Does Ownly have enough restaurant assortment / availability to support adoption?
6. Does Rapido integration materially improve discovery / trial?
7. Does gamification / ₹50–₹100 reward create durable users or only promo-driven trial?
8. How do students and working professionals differ?
9. What should Ownly KEEP, ADAPT, or DROP for Hyderabad?
10. What evidence is strong, weak, directional, or unavailable?

---

# 2. FIRST: DETERMINE OWNLY'S REAL STRATEGIC METRIC LOGIC

Search current, credible public sources and inspect existing secondary research.

Do NOT invent an “official Ownly North Star Metric.”

Create three distinct labels:

### A. PUBLICLY STATED COMPANY PRIORITIES
Metrics / outcomes explicitly stated by Rapido / Ownly leadership or strong official/primary sources.

### B. REPORTED EXTERNAL BUSINESS METRICS
Examples:
- orders/day
- restaurant partners
- city order share
- app integration
- price structure
- reported marketplace scale

These must include source + date + caveat.

### C. PROJECT-RECOMMENDED NORTH-STAR / PROXY METRICS
Metrics we recommend because they best capture value creation but are NOT publicly confirmed as Ownly's official NSM.

Never blur these three.

---

# 3. NORTH-STAR DESIGN RULE

Evaluate at least these candidate NSM families:

### Candidate 1 — Monthly Transacting Food Customers
Useful because Ownly/Rapido's strategic thesis is expanding the number of people ordering food online.

### Candidate 2 — Monthly Repeat Fulfilled Orders
Useful because it combines:
- actual transaction,
- fulfillment,
- repeated customer value,
- restaurant demand,
- logistics success.

### Candidate 3 — Fulfilled Orders per Active Customer
Useful because affordability should theoretically increase:
- frequency,
- repeat purchases,
- retention.

### Candidate 4 — Active Repeat Customers
Useful for separating promo-driven first orders from durable adoption.

For each candidate:
- strategic alignment,
- user value,
- restaurant value,
- controllability,
- measurability,
- susceptibility to gaming,
- whether our project can actually estimate it.

Then recommend:
- **1 primary project north-star proxy**
- **2–4 guardrail metrics**

Do not force one if a dual-sided marketplace requires a north-star + marketplace health guardrails.

---

# 4. BUILD A COMPLETE KPI TREE

Build the KPI system in layers.

## LAYER 0 — BUSINESS OUTCOME
Examples to evaluate:
- transacting customer growth
- fulfilled order growth
- repeat fulfilled orders
- sustainable marketplace growth

## LAYER 1 — CUSTOMER ACQUISITION
Potential metrics:
- Ownly awareness
- aided awareness
- trial penetration
- awareness → trial conversion
- fake-door CTR / intent conversion
- Bengaluru proposition conversion
- Hyderabad proposition conversion
- A/B conversion lift
- Rapido-user → Ownly trial propensity
- app-placement discovery rate
- first-order incentive conversion
- incentive dependency rate
- first-order barrier rate

## LAYER 2 — VALUE / AFFORDABILITY
Potential metrics:
- matched-basket savings ₹
- matched-basket savings %
- final payable price index
- fee load %
- online/offline menu parity rate
- Ownly vs Swiggy price gap
- Ownly vs Zomato price gap
- minimum meaningful saving needed to switch
- price-vs-ETA trade-off threshold
- stated price elasticity / switching threshold
- proportion choosing Ownly at ₹20 / ₹50 / ₹80 savings

Create new metrics if they are more decision-useful.

## LAYER 3 — RETENTION / ENGAGEMENT
Potential metrics:
- repeat-without-promo intent
- trial → repeat-intent conversion
- intended order frequency
- next-10-orders Ownly allocation
- share of requirements
- stated share of wallet / value-share proxy
- promo-dependent repeat rate
- drop-off reason incidence among triers
- reliability-driven churn proxy
- “second-order readiness” if justified

## LAYER 4 — ASSORTMENT / SUPPLY
Potential metrics:
- restaurant availability overlap
- target-restaurant coverage
- local-favourite coverage
- chain coverage
- cuisine coverage
- menu parity
- restaurant partner growth from secondary sources
- supply sufficiency perception
- restaurant-side value proposition evidence
- zero-commission / 100% order value retention claim where verified

Do not pretend we have restaurant economics data if we do not.

## LAYER 5 — FULFILLMENT / EXPERIENCE
Potential metrics:
- ETA gap
- estimated vs observed delivery gap, if observable
- cancellation incidence among sampled Ownly triers
- non-delivery incidence among sampled Ownly triers
- support-resolution experience
- missing-item incidence
- sample failure incidence
- reliability importance
- reliability satisfaction
- “fulfilled experience rate” only if denominator and data are defensible

Review/social data should be used as issue discovery unless the sample is demonstrably representative.

## LAYER 6 — DISTRIBUTION / RAPIDO ECOSYSTEM
Potential metrics:
- Rapido usage penetration within target segment
- Ownly awareness among Rapido users vs non-users
- Ownly trial among Rapido users vs non-users
- discovery through Rapido %
- first-tap success in app-navigation test
- Ownly tile/nav salience
- cross-sell propensity
- conversion lift associated with Rapido usage

Do not claim causality from observational survey associations.

## LAYER 7 — PROMOTION / GTM
Potential metrics:
- reward-triggered trial intent
- no-reward repeat intent
- promo dependency gap
- game awareness
- game participation
- game → CTA conversion if trackable
- fake-door conversion
- landing-page conversion by proposition
- WhatsApp poll directional response
- referral / share intent only if useful

## LAYER 8 — SEGMENTATION
Compare:
- Hyderabad vs Bengaluru
- student vs working professional
- Ownly trier vs non-trier
- Rapido user vs non-user
- frequent vs light food-delivery user
- high vs low basket value
- price-sensitive vs time-sensitive
- Gachibowli core catchment vs nearby
- high-promo dependence vs low-promo dependence

## LAYER 9 — MARKET / COMPETITIVE CONTEXT
Potential metrics:
- reported Bengaluru orders/day
- reported Bengaluru volume share
- restaurant count
- market growth indicators
- app downloads / ratings
- sample volume-share proxy
- sample value-share proxy
- category ordering frequency

Never convert external estimates into “official Ownly metrics.”

## LAYER 10 — ECONOMICS
Evaluate whether we can defensibly calculate:
- CAC
- CPA
- retention cost
- CLV
- ROAS
- contribution margin
- GOV/GMV
- EBITDA
- burn/order

If required inputs do not exist, mark:
**NOT CALCULABLE FROM OUR DATA**

If we run paid acquisition ourselves:
- Experimental CAC = experiment spend / acquired intent conversions
- clearly label it as experiment CAC, NOT Ownly CAC.

If secondary research reports burn/order or economics:
- show as external reported estimate with source/date,
- never mix into primary-data calculations as if it were our observed value.

---

# 5. COURSE METRICS

Inspect the uploaded formula sheets.

Map course metrics such as:
- retention rate
- customer lifetime value
- average acquisition cost
- average retention cost
- YoY growth
- CAGR
- cannibalization where relevant
- value share
- volume share
- penetration
- any other metrics contained in the sheets

For each metric, decide:

### USE
We have valid inputs.

### USE AS PROXY
We can estimate a clearly labeled sample/stated/experimental proxy.

### REFERENCE ONLY
Relevant theoretically but cannot calculate.

### NOT RELEVANT
Does not help the Ownly Hyderabad decision.

Do not include a metric simply because it appears in the course formula sheet.

---

# 6. GENERIC MARKETING-METRICS FILE

The generic marketing dataset includes fields like:
- impressions
- clicks
- CTR
- spend
- qualified leads
- conversions
- conversion rate
- revenue
- ROAS
- CPA

Treat it as a **metric-calculation / dashboard-pattern reference only** unless there is explicit evidence that it contains Ownly data.

Do not mix those records into Ownly empirical analysis.

Use the useful logic for our fake-door experiment:
**reach/impressions → visitors → CTA clicks → intent conversions → possible acquisition cost if spend exists.**

---

# 7. CREATE A KPI DATA-COVERAGE MATRIX

Create `05_analysis/kpi_data_coverage.csv`.

Required columns:

- KPI_ID
- KPI_Name
- KPI_Layer
- Business_Question
- Why_It_Matters
- Exact_Formula
- Numerator
- Denominator
- Unit
- Primary_or_Guardrail
- Actual_Company_Metric_or_Proxy
- Data_Source
- Source_File
- Source_Field_or_Question
- Geography
- Segment
- Can_Calculate_Now
- Data_Gap
- Collection_Action
- Owner
- Statistical_Test
- Dashboard_Visual
- Caveat
- Decision_Enabled
- Priority_P0_P1_P2

Every metric must have a denominator where applicable.

---

# 8. CREATE A KPI DICTIONARY

Create `05_analysis/metric_dictionary.md`.

For EVERY P0/P1 metric include:

1. name
2. plain-English definition
3. exact formula
4. example calculation
5. data source
6. level of evidence
7. denominator
8. segment cuts
9. bias / limitation
10. what a high value means
11. what a low value means
12. which business decision it affects
13. which dashboard panel it belongs to

---

# 9. MAP EVERY RESEARCH TASK TO KPIs

Do not let survey, interview and Person-3 workstreams operate separately.

Create:

`05_analysis/research_to_kpi_map.md`

Map:

## Survey
Which exact question feeds which KPI?

## Interviews
Which hypothesis / KPI does each question explain?

Interviews are primarily explanatory.
Do not turn 8 interviews into population percentages unless explicitly presented as coded qualitative counts.

## Person 3 — platform audit
Map:
- matched basket → savings / price index / fee load
- restaurant availability → assortment coverage
- ETA → ETA gap
- screenshots → evidence panels

## Person 3 — fake door
Map:
- visitors
- CTA clicks
- conversion
- A/B lift
- segment / channel if trackable

## App-placement test
Map:
- Rapido usage
- Ownly awareness
- first tap
- time to find food
- Ownly discoverability

## Game / promotion
Map:
- reward-triggered first order
- no-reward repeat
- promo dependency

## Secondary research
Map:
- strategy timeline
- reported orders/day
- restaurant scale
- zero-commission claim
- app integration
- review/social themes
- competitor / historical cautionary evidence

---

# 10. IDENTIFY MISSING DATA BEFORE IT IS TOO LATE

After creating the KPI tree, determine:

> **Which P0 metrics cannot be computed from our current survey / interview / Person-3 plan?**

If a crucial metric is missing:

- propose the smallest possible survey question addition,
- or smallest audit addition,
- or smallest experiment event to track.

Do NOT bloat the survey.

For every proposed new question state:
- metric enabled,
- why current questions cannot calculate it,
- exact wording,
- answer type,
- where to insert it,
- whether it is worth respondent burden.

---

# 11. BUILD THE DASHBOARD AS A DECISION STORY

Do NOT create a generic Tableau/Power BI page full of unrelated charts.

Design a dashboard system with a **main executive dashboard + drill-down pages/tabs**.

# PAGE 1 — EXECUTIVE DECISION COCKPIT

Purpose:
> **Should Ownly replicate or adapt Bengaluru's playbook for Gachibowli?**

Top banner:
- primary H₀ result
- current decision: KEEP / ADAPT / DROP
- one-sentence evidence-based answer

KPI cards, depending on available data:
- awareness
- trial penetration
- A/B fake-door conversion
- median basket savings %
- repeat-without-promo intent
- sample share of requirements
- restaurant coverage
- ETA gap

Core visual:
**Transferability Matrix**

Rows:
- transparent lower price
- no/low fees
- Rapido cross-sell
- game/reward
- local restaurant supply
- delivery/reliability proposition

Columns:
- Bengaluru evidence
- Hyderabad evidence
- supporting KPI
- confidence
- KEEP / ADAPT / DROP

---

# PAGE 2 — BENGALURU PLAYBOOK: WHAT ACTUALLY WORKED?

Explain the originating strategy before comparing Hyderabad.

Visuals:
1. strategy timeline
2. reported orders/day over time, only where sourced
3. reported restaurant growth / scale
4. Bengaluru user benchmark:
   - discovery
   - first-order triggers
   - repeat/drop-off drivers
5. claims-vs-evidence table

This page should answer:
> **What exactly are we trying to transfer?**

Also show model changes over time so early fee structures are not mixed with current strategy.

---

# PAGE 3 — HYDERABAD MARKET: WHO WILL SWITCH AND WHY?

Use Hyderabad primary survey.

Visuals:
1. student vs professional profile
2. order-frequency distribution
3. primary platform
4. awareness → trial funnel
5. switching-driver ranking
6. price-vs-ETA trade-off curve
7. Rapido users vs non-users
8. Ownly triers vs non-triers
9. next-10-orders allocation / share-of-requirements proxy

This page answers:
> **Who is the highest-potential entry segment and what causes switching?**

---

# PAGE 4 — FIRST ORDER VS SECOND ORDER

This is a critical narrative page.

Left side:
## FIRST ORDER / ACQUISITION
Potential drivers:
- price
- no hidden fees
- game/reward
- Rapido discovery
- first-order offer
- curiosity

Right side:
## SECOND ORDER / RETENTION
Potential drivers:
- successful fulfillment
- ETA
- reliability
- restaurant availability
- support
- consistent savings
- repeat without promo

Visual ideas:
- paired driver bars
- acquisition-to-retention funnel
- trier cohort split
- promo dependency gap

Test the hypothesis:
> **Price gets the first order; reliability earns the second.**

Do not state it as truth unless the data supports it.

---

# PAGE 5 — IS OWNLY ACTUALLY CHEAPER?

Use Person-3 matched-basket audit.

Primary visual:
**Matched Basket Waterfall / Price Decomposition**

For Ownly vs Swiggy vs Zomato:
- menu price
- packaging
- platform fee
- delivery
- surge
- discounts
- final payable

Additional:
- median savings ₹
- median savings %
- price-index distribution
- number of baskets where Ownly is cheapest
- savings by basket value
- savings vs ETA trade-off

This page answers:
> **Is affordability a real, repeatable advantage or only messaging?**

---

# PAGE 6 — CAN THE MARKETPLACE DELIVER THE PROMISE?

Marketplace health / supply / operations.

Visuals:
- restaurant availability overlap
- local-favourite coverage
- chain coverage
- cuisine coverage
- ETA gap
- sampled Ownly trier failure themes
- review/social issue theme map
- positive vs negative themes ONLY with proper sampling caveat

This page answers:
> **Even if consumers want Ownly, can supply and fulfillment support repeat usage?**

Do not claim scraped-review percentages represent all customers.

---

# PAGE 7 — RAPIDO DISTRIBUTION ADVANTAGE

Test the strategic idea that Rapido's existing ecosystem reduces acquisition friction.

Visuals:
- Rapido usage penetration in target audience
- Ownly awareness: Rapido users vs non-users
- Ownly trial: Rapido users vs non-users
- discovery source
- app first-tap / discoverability test
- fake-door traffic/channel conversion if available

Treat bottom-nav placement as a hypothesis unless internal evidence explains the design decision.

Possible question:
> **Does Rapido already own enough user attention to lower Ownly's discovery barrier?**

Do not equate association with causal acquisition-cost reduction.

---

# PAGE 8 — PROMOTION: GROWTH OR RENTED DEMAND?

Evaluate the ₹50 / ₹100 game and similar incentives.

Visuals:
- % saying reward causes first order
- % saying they repeat without reward
- promo-dependency gap
- student vs professional difference
- high-frequency vs light-user difference

Decision:
- KEEP
- MODIFY
- TARGET TO SEGMENT
- DEPRIORITIZE

This page answers:
> **Does gamification create retained demand or only subsidized trial?**

---

# PAGE 9 — SEGMENT PRIORITIZATION

Create a practical segment matrix.

Rows may include:
- students
- working professionals
- frequent food-delivery users
- existing Rapido users
- high price-sensitive users
- high reliability-sensitive users

Columns:
- category frequency
- Ownly awareness
- trial
- price sensitivity
- repeat intent
- promo dependence
- expected share of requirements
- fit with Ownly proposition

Do not produce a fake “market attractiveness score” unless the weighting is explicitly justified.

Prefer transparent evidence over arbitrary composite scores.

---

# PAGE 10 — FINAL PROPOSITION / GO-TO-MARKET DECISION

Create:

## KEEP
Bengaluru tactics supported in Hyderabad

## ADAPT
Tactics that work only with localization / operational changes

## DROP / DEPRIORITIZE
Tactics not supported by evidence

For every proposition show:
- supporting metric
- supporting qualitative insight
- confidence level
- source
- implementation implication

Also include:
- reject / fail-to-reject H₀
- what the result DOES mean
- what it DOES NOT mean
- next validation needed before citywide scale

---

# 12. WHERE THE ORIGINAL BRAIN-DUMP QUESTIONS BELONG

Map all our earlier thoughts into the dashboard / analysis instead of losing them.

### “Will Bengaluru strategy work in Hyderabad?”
→ Page 1 + H₀ + Transferability Matrix

### “Understand Bengaluru people's behavior / how market was captured”
→ Page 2

### “Understand Hyderabad behavior / entry point / GTM”
→ Page 3

### “How do we use claims/reviews/social research?”
→ Pages 2, 4, 6 as hypothesis/evidence, not fake population statistics

### “When was Ownly embedded in Rapido?”
→ Strategy timeline + Page 7

### “Why did Rapido start Ownly?”
→ Strategy context, based on sourced leadership thesis around affordability + shared logistics network

### “Foodpanda / Uber Eats / Toing failures?”
→ Appendix / cautionary benchmark ONLY if evidence materially changes a decision

### “Batching / rider behavior?”
→ Operations appendix unless we have real evidence

### “Extra verticals?”
→ OUT OF CURRENT SCOPE; future opportunities appendix only

### “Sentiment analysis?”
→ Page 6 as issue-theme evidence with sampling caveat

### “₹50 / ₹100 game?”
→ Page 8

### “Metro bottom-nav replaced by Ownly?”
→ Page 7 as app-discoverability hypothesis, not claimed motive

### “Landing page analysis?”
→ Page 1 / Page 7 through A/B fake-door conversion

---

# 13. STATISTICAL ANALYSIS REQUIREMENTS

For each quantitative claim define:

- n
- denominator
- geography
- segment
- metric type
- confidence interval if appropriate
- statistical test
- practical effect size
- caveat

Primary experiment:
- A vs B conversion
- Fisher's exact if small cells
- otherwise two-proportion test
- show absolute percentage-point lift AND relative lift
- do not rely only on p-value

Secondary:
- chi-square / Fisher for categorical associations
- Mann-Whitney / ordinal summaries where justified
- simple logistic regression only if sample size and data quality allow

Do not perform statistical theater.

---

# 14. DECISION RULES

Create `05_analysis/decision_rules.md`.

Before looking at final results, define how evidence translates into action.

For example:

### Bengaluru proposition
- materially higher A/B conversion + no retention penalty → KEEP
- acquisition advantage but weak repeat → ADAPT
- no meaningful advantage → do not lead Hyderabad GTM with it

### Promotions
- high first-order lift + low no-reward repeat → acquisition-only tactic
- high trial + high no-reward repeat → stronger scalable tactic

### Price
- meaningful observed basket savings + switching sensitivity → core positioning
- small/inconsistent savings → cannot rely on affordability claim alone

### Assortment
- low coverage of target restaurants → fix supply before heavy acquisition

Do NOT hard-code arbitrary thresholds without explaining them.
Use effect sizes, sample uncertainty and practical business relevance.

---

# 15. REQUIRED OUTPUT FILES

Create/update:

1. `05_analysis/kpi_tree.md`
2. `05_analysis/kpi_data_coverage.csv`
3. `05_analysis/metric_dictionary.md`
4. `05_analysis/research_to_kpi_map.md`
5. `05_analysis/data_gap_map.md`
6. `05_analysis/calculation_spec.md`
7. `05_analysis/decision_rules.md`
8. `06_dashboard/dashboard_blueprint.md`
9. `06_dashboard/chart_specifications.md`
10. `06_dashboard/dashboard_data_schema.csv`
11. `06_dashboard/dashboard_storyline.md`
12. `01_plan_tracking/decisions.md`
13. `01_plan_tracking/progress.md`

Do not overwrite raw source files.

---

# 16. PRIORITIZATION

Categorize every metric:

## P0 — MUST HAVE
Directly determines the Hyderabad decision.

## P1 — IMPORTANT
Explains why P0 moved.

## P2 — NICE TO HAVE
Interesting but not decision-critical.

We have a 3-day deadline.

If a metric requires major new data collection and does not affect the final decision, remove it.

---

# 17. YOUR FIRST RESPONSE TO THIS PROMPT

Do NOT immediately build pretty charts.

Your first response must contain:

# KPI ARCHITECTURE — FIRST PASS

## 1. Ownly's publicly stated strategic metric priorities
Clearly sourced and distinguished from inference.

## 2. Recommended project north-star proxy
One metric + rationale + guardrails.

## 3. KPI tree
Business outcome → acquisition → value → retention → supply → operations → distribution → promotion.

## 4. P0 metric table
For each:
- formula
- exact source
- can we calculate it?
- missing data
- decision enabled

## 5. Data gaps RIGHT NOW
Tell us whether the current survey, interview and Person-3 tasks can calculate all P0 KPIs.

## 6. Minimal changes required BEFORE data collection goes too far
Exact survey question / audit field / experiment event additions only if necessary.

## 7. Dashboard architecture
Pages + exact charts + data source + question answered.

## 8. What Claude will do next
Files Claude will create itself.

## 9. What Person 1 / 2 / 3 must do next
Only human-required tasks.

After that, create the KPI/dataset/dashboard files and maintain them as project context.

Your standard is:
**No vanity metrics. No fake precision. No invented Ownly metrics. Every KPI must enable a decision.**
