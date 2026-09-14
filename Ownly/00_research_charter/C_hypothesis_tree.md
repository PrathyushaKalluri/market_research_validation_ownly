# C. Hypothesis Tree (pre-registered)

**Version:** 2026-09-14. Every entry is a **HYPOTHESIS**. Thresholds marked *(A)* are team-editable **ASSUMPTIONS** about business significance. They must be frozen **before** data collection closes; any later change is logged in `decisions.md` together with the reason.

**Variable names** follow `03_hyderabad_survey/survey_variable_dictionary.csv` (authoritative once Agent C finishes). Names below use the shared conventions and are reconciled in `08_clean_data/master_data_dictionary.csv`.

---

## 0. Universal decision rule for a hypothesis

For a pre-registered threshold T and a 95% CI around the estimate:

| Verdict | Rule |
|---|---|
| **SUPPORTED** | The whole CI lies on the hypothesised side of T |
| **REJECTED** | The whole CI lies on the other side of T |
| **INCONCLUSIVE** | The CI contains T. Report the point estimate, CI and n, and do not call it either way. |
| **NOT TESTABLE** | n is below the minimum in `F_sample_plan.md`. Use qualitative evidence only, labelled. |

**Significance testing:**
- **Confirmatory** hypotheses (marked ★) use α = 0.05 with **Holm correction across the ★ set**.
- All other sub-hypotheses are **exploratory**. They are reported with CIs and effect sizes and labelled exploratory. They are never promoted to headline findings without triangulation.

**Business-significance floors *(A)*.** Below these, even a "significant" difference is reported as "not practically meaningful":
- difference in proportions ≥ 10 pp
- rank-biserial r ≥ 0.20
- Cohen's d ≥ 0.30
- a ₹ trade-off of ≥ ₹10 per order

---

## 1. Tree structure (MECE logic)

Root question: **Does Ownly's Bengaluru proposition fit Gachibowli, and for whom, under what conditions?**

The tree splits the root into six mutually exclusive branches along the adoption chain: **need → value → trust → who → transfer/retention → behaviour**.

```
ROOT: Ownly early market fit in Gachibowli
│
├── B1 NEED — Is there a painful, switch-creating problem?
│     ├── H1  Problem intensity (fees, total price, abandonment, promo dependency)
│     └── H10 Assortment threshold (which restaurants must be present)
│
├── B2 VALUE — Does the proposition win choices, and at what trade-off?
│     ├── H2  Total-price & transparency value
│     ├── H3  Price vs ETA
│     ├── H4  Price vs reliability / refund assurance
│     ├── H5  Price vs restaurant choice
│     └── H8  WTP for a transparent delivery fee
│
├── B3 TRUST — Does the brand help or hurt?
│     └── H7  Rapido/Ownly brand effect
│
├── B4 WHO — Do segments differ in ways that change targeting?
│     └── H6  Students vs working professionals
│
├── B5 TRANSFER & RETENTION — Do Bengaluru drivers hold, and what sustains use?
│     ├── H9  Bengaluru → Hyderabad transferability
│     └── H12 Repeat-use drivers
│
└── B6 BEHAVIOURAL VALIDATION — Does stated interest show up in action?
      └── H11 Intent vs behaviour
```

**Why each branch has a clear boundary:**
- **H10 vs H5.** H10 asks *which* restaurants are required and whether their absence blocks trial (a need). H5 asks how much *price* compensates for a loss of selection (a trade-off).
- **H6.** H6 owns segment *differences*. Other families test pooled effects and only reference H6 for splits.
- **H9 vs H1–H8.** H9 owns *cross-city comparison* only; within-Hyderabad tests sit in H1–H8.
- **H12.** H12 owns *post-trial* behaviour. Pre-trial intent belongs to H2 and H7.
- **H11.** H11 owns *say–do calibration* only.

---

## 2. Hypotheses in full

Every sub-hypothesis uses these fields:
- **Statement**
- **Rationale**
- **IV** (independent variable) → **DV** (dependent variable)
- **Segment**
- **Method**
- **Threshold**
- **Dataset**
- **Test**
- **If validated** / **If rejected**

### H1 — PROBLEM INTENSITY
Family question: do users feel enough dissatisfaction with incumbent pricing and fees to create a switching opportunity?

**H1.1 ★ Fee friction is common**
- **Statement:** Most target users had checkout charges make them reconsider or change an order in the last 4 weeks.
- **Rationale:** A cost proposition needs felt, recent, repeated pain, not just a general belief that apps are expensive.
- **IV:** none (prevalence).
- **DV:** `pain_fee_reconsider_freq` ≥ 3 ("sometimes" or more) — binary.
- **Segment:** pooled Hyderabad; then students and professionals.
- **Method:** Hyderabad survey.
- **Threshold *(A)*:** ≥ 50% of respondents.
- **Dataset:** `fact_survey_respondent` (city = hyd).
- **Test:** proportion with Wilson 95% CI; decision rule §0.
- **If validated:** fee pain is a legitimate lead message.
- **If rejected:** do not lead with fees; look to other pains (reliability/assortment) or a different job.

**H1.2 ★ Price/fee pain ranks at least as high as reliability pain**
- **Statement:** The share selecting price/fee frustrations among their top frustrations is ≥ the share selecting lateness/cancellation frustrations.
- **Rationale:** Tests AS2. A cheaper app that competes against a mainly reliability-driven market would lose.
- **IV:** frustration category.
- **DV:** selected (0/1), per respondent.
- **Segment:** pooled; students and professionals.
- **Method:** survey (prompted multi-select) + coded unaided open text.
- **Threshold:** difference (price − reliability) ≥ 0, with a business floor of 10 pp for "clearly higher".
- **Dataset:** respondent table.
- **Test:** McNemar test for paired proportions; paired difference with CI. The open-text coding serves as a robustness check.
- **If validated:** price can lead, and reliability becomes the guardrail.
- **If rejected:** lead with reliability or a mixed "value you can count on" message; the price message is secondary.

**H1.3 Menu-inflation belief is widespread (belief, not fact)**
- **Statement:** ≥ 50% agree that app menu prices exceed restaurant prices.
- **Rationale:** Ownly's "menu parity" message only lands if users believe there is a markup. The audit tests whether the markup is real.
- **DV:** `pain_menu_markup_belief` top-2 box.
- **Segment:** pooled.
- **Method:** survey + audit (verified offline prices where available).
- **Threshold *(A)*:** 50%.
- **Test:** Wilson CI; compare belief with the audit-verified markup share, descriptively.
- **If validated:** the parity message is credible if the audit also shows a markup.
- **If rejected:** parity is not a salient benefit; lead with the total instead.

**H1.4 Price-driven cart abandonment is common**
- **Statement:** ≥ 30% abandoned at least one cart after seeing the final amount in the last 4 weeks.
- **Rationale:** Abandonment is recalled behaviour, stronger evidence than attitudes.
- **DV:** `beh_abandon_price_freq` ≥ 2.
- **Threshold *(A)*:** 30%.
- **Test:** Wilson CI; split by segment is exploratory.
- **If validated:** checkout price visibly costs incumbents orders, which Ownly can capture.
- **If rejected:** pain is tolerated and switching energy is low.

**H1.5 Promotion dependency competes with everyday low price (falsification test)**
- **Statement:** A large share of users mainly order when a discount is available.
- **Rationale:** If orders are offer-triggered, a no-coupon everyday price may look *less* attractive even when it is cheaper.
- **DV:** `beh_offer_dependency` (share of orders placed with an offer; 5-point frequency).
- **Segment:** students and professionals.
- **Test:** proportion + CI; cross-tab with the H2.4 choice.
- **If high (≥ 40% "most/all orders")** *(A)*: the design must show savings versus the *discounted* incumbent total, and Ownly may need launch offers.
- **If low:** everyday pricing is viable.

**H1.6 Pain concentrates in frequent users**
- **Statement:** PPI is higher among frequent users (8+ orders per 4 weeks) than occasional users (1–3).
- **Rationale:** Cumulative exposure; frequent users are also more valuable.
- **IV:** `seg_freq`. **DV:** PPI.
- **Test:** Mann-Whitney U + rank-biserial r; ordinal trend check with Jonckheere-Terpstra or Spearman.
- **Threshold:** r ≥ 0.20.
- **If validated:** target the frequent segment.
- **If rejected:** pain is broad; segment on other variables.

**H1.7 ★ Pain links to switching readiness**
- **Statement:** PPI is positively associated with SRI.
- **Rationale:** Pain that doesn't relate to readiness to switch isn't an opportunity.
- **IV:** PPI. **DV:** SRI (`bt_trial_intent` component analysed separately to avoid overlap).
- **Test:** Spearman ρ with bootstrap CI. Partial correlation controlling for `seg_freq` is exploratory.
- **Threshold *(A)*:** ρ ≥ 0.20.
- **If validated:** a pain-led acquisition message is justified.
- **If rejected:** switching is driven by something else (habit, assortment); investigate in interviews.

### H2 — PRICE VALUE PROPOSITION (TOTAL CHECKOUT PRICE, not "cheapness")

**H2.1 ★ Total checkout price materially shifts choice**
- **Statement:** In the choice tasks, a lower total checkout raises choice probability. The coefficient is negative and significant, and the marginal effect of ₹30 lower is ≥ 10 pp in choice share.
- **IV:** `dce_price` (total ₹). **DV:** `dce_chosen`.
- **Segment:** pooled; students/professionals as a price × segment interaction.
- **Method:** choice experiment.
- **Threshold *(A)*:** ₹30 → ≥ 10 pp.
- **Dataset:** `fact_dce_long`.
- **Test:** conditional logit with respondent-clustered SEs. Marginal effects are simulated. If n < 125, fall back to task-level choice shares with Wilson CIs.
- **If validated:** price is a real lever.
- **If rejected:** price differences at realistic levels don't move choice; reposition.

**H2.2 Transparency has value beyond the total**
- **Statement:** At *identical* final payable, a simple bill (food + delivery) is preferred over an itemised bill with fees and a discount line.
- **Rationale:** Separates "no hidden fees" from "lower total" (AS5).
- **IV:** bill format. **DV:** `bill_s1_simple_chosen` (code 3, "no real difference", is reported separately and is not counted as either choice).
- **Method:** bill comparison (labelled hypothetical scenarios).
- **Threshold *(A)*:** ≥ 60% prefer simple.
- **Test:** exact binomial vs 50% + Wilson CI.
- **If validated:** "see the real price" messaging has standalone value.
- **If ≈ 50%:** lead with the total amount, not transparency.

**H2.3 ★ Achievable savings clear the switching threshold**
- **Statement:** The median savings respondents say they need to make a new app their default for a typical order is ≤ the audit-observed median Ownly saving in Gachibowli.
- **Rationale:** This is the single most important economic test: needed vs actually available.
- **IV:** none (two distributions). **DV:** `beh_switch_savings_required` (₹) vs `audit_pair_gap`.
- **Segment:** students, professionals, frequent users.
- **Method:** survey + competitor audit.
- **Threshold:** the audit median saving CI lower bound ≥ the survey required-savings median. Also report the share of respondents whose threshold ≤ the audit median saving.
- **Dataset:** respondent + `fact_audit_pairs`.
- **Test:** bootstrap CIs on both medians; share with Wilson CI. "No amount would make me switch" responses are reported separately, not dropped.
- **If validated:** the savings message is economically defensible.
- **If rejected:** savings alone won't convert; bundle with reliability or assortment, or target only the segment whose threshold is met.

**H2.4 Discount framing vs everyday price**
- **Statement:** At equal totals, users prefer "higher base price − visible discount" over "lower price, no discount".
- **Rationale:** Falsification check for Ownly's everyday-pricing model (links to H1.5).
- **Method:** bill comparison.
- **Test:** binomial vs 50%; cross-tab with offer dependency (chi-square / Fisher).
- **If discount framing is preferred:** Ownly must communicate savings versus the discounted incumbent total, or use selective offers.
- **If not:** everyday price works as a message.

**H2.5 Brand-blind concept interest (relative, not absolute)**
- **Statement:** The blind concept's "definitely would try" (top-box) share ≥ 20% *(A)* and is higher in the target segment than in others.
- **Rationale:** Top-2-box intent is inflated. Top-box is used for relative comparison and calibrated by H11.
- **DV:** `bt_trial_intent` = 5.
- **Test:** Wilson CI; segment difference via two-proportion z-test.
- **If validated:** a starting concept signal exists, pending H11.
- **If rejected:** weak concept pull even before trade-offs.

### H3 — PRICE vs ETA

**H3.1 ★ Savings buy waiting time, within limits**
- **Statement:** For the pooled sample, the implied value of 10 minutes of ETA is < ₹30. So ₹30 in savings compensates for ~10 extra minutes.
- **IV:** `dce_eta`, `dce_price`. **DV:** choice.
- **Segment:** pooled; students/professionals via interaction.
- **Method:** choice experiment.
- **Threshold *(A)*:** ₹30 per 10 min.
- **Test:** conditional logit. WTP = β_ETA/β_price × 10, with delta-method or Krinsky-Robb CI. Supported if the CI upper bound is < ₹30.
- **If validated:** a moderate ETA gap is acceptable when savings are real.
- **If rejected:** ETA parity is a guardrail; don't compete on price at the expense of speed.

**H3.2 A tolerance ceiling exists**
- **Statement:** Choice share drops non-linearly at the longest ETA level. Separately, a majority report a maximum acceptable dinner ETA ≤ 45 min *(A)*.
- **Method:** choice experiment with ETA as dummies + `exp_eta_max_dinner`.
- **Test:** compare dummy coefficients (Wald test of linearity); distribution and median of the stated maximum.
- **If validated:** set an operational ETA ceiling.
- **If rejected:** tolerance is roughly linear.

**H3.3 Occasion moderates tolerance**
- **Statement:** Tolerated ETA is lower for weekday lunch than for weekday dinner.
- **IV:** occasion (within-subject). **DV:** `exp_eta_max_lunch` vs `exp_eta_max_dinner`.
- **Test:** Wilcoxon signed-rank + matched-pairs r.
- **If validated:** position Ownly for occasions with more slack; don't lead at lunch peaks.
- **If rejected:** a single ETA standard applies.

### H4 — PRICE vs RELIABILITY

**H4.1 ★ Users will not trade reliability for realistic savings**
- **Statement:** The implied WTP to move from "late in 3 of 10 orders" to "late in 1 of 10" exceeds ₹30. Supporting check: median RSS ≥ 50%.
- **IV:** `dce_reliability`, `dce_price`. **DV:** choice.
- **Segment:** pooled; students/professionals.
- **Test:** conditional logit WTP with CI; RSS distribution (median, bootstrap CI).
- **If validated:** reliability is a non-negotiable guardrail, and cheaper-but-flakier fails.
- **If rejected:** some segments will accept lower reliability for price, so a value tier is possible.

**H4.2 Refund assurance offsets reliability risk**
- **Statement:** Automatic refund within 24h has a WTP ≥ ₹15 *(A)* and reduces the reliability penalty (reliability × refund interaction).
- **Test:** conditional logit with interaction (exploratory; power is limited).
- **If validated:** a service guarantee can be part of the proposition.
- **If rejected:** reliability itself must improve.

**H4.3 Past incidents raise reliability sensitivity**
- **Statement:** Respondents with a late, cancelled or refund-problem order in the last 3 months have higher RSS.
- **IV:** `pain_incident_any_3m`. **DV:** RSS.
- **Test:** Mann-Whitney + r.
- **If validated:** incident-experienced users are receptive to a reliability promise.
- **If rejected:** sensitivity is a general trait.

### H5 — PRICE vs RESTAURANT CHOICE

**H5.1 ★ Selection loss costs more than achievable savings**
- **Statement:** The implied WTP to move from "few of your usual restaurants available" to "most available" exceeds the audit median Ownly saving.
- **IV:** `dce_assortment`, `dce_price`. **DV:** choice.
- **Segment:** pooled; students/professionals.
- **Test:** conditional logit WTP CI vs the audit median saving with its bootstrap CI.
- **If validated:** assortment is a gating condition, and supply build-out comes before demand spend.
- **If rejected:** savings can compensate for a thinner catalogue.

**H5.2 Assortment matters more than ₹20 for professionals**
- **Statement:** For professionals, the "most vs few" assortment WTP is > ₹20. For students it is ≤ ₹20.
- **Test:** segment-interacted logit; this is a directional claim unless each segment has n ≥ 125.
- **If validated:** a segment-specific supply strategy.
- **If rejected:** a uniform strategy.

### H6 — STUDENTS vs WORKING PROFESSIONALS (tested, not assumed)

All H6 tests report:
- the raw difference, and
- an adjusted model controlling for `seg_freq`, `beh_last_order_total` band and `dem_living`,

so that "student" is not a proxy for "low spend".

**H6.1 ★ Students have higher price pain**
- **IV:** `seg_occupation`. **DV:** PPI.
- **Test:** Mann-Whitney + r; OLS on PPI with controls (robust SE) is exploratory.
- **Threshold:** r ≥ 0.20.
- **If validated:** students respond to price-led messaging.
- **If rejected (including if professionals score higher):** the price message is not student-specific.

**H6.2 Students have lower fee WTP**
- **DV:** `wtp_max_fee`; acceptance at each fee point.
- **Test:** Mann-Whitney on max fee; logistic regression of acceptance on fee × segment, with respondent-clustered SEs.
- **If validated:** a fee strategy differentiated by segment and occasion.
- **If rejected:** uniform fee.

**H6.3 ★ Professionals value reliability and time more**
- **Statement:** WTP for reliability and ETA is higher for professionals than for students.
- **Test:** segment-interacted conditional logit; difference in WTP with Krinsky-Robb CI. RSS and ETA tolerance via Mann-Whitney as a robustness check.
- **If validated:** reliability-led positioning for professionals.
- **If rejected:** do not segment messaging on this axis.

**H6.4 Segments differ in commercial value**
- **DV:** `scr_orders_4wk`, `beh_last_order_total`, occasion mix.
- **Test:** chi-square with Cramér's V; Mann-Whitney for spend.
- **If one segment is ≥ 1.3×** *(A)* the other in orders × AOV: it is the stronger commercial beachhead, other things equal.

### H7 — BRAND EFFECT (randomised between-subjects + within-subject)

**H7.1 ★ Rapido/Ownly branding changes trial intent**
- **Statement:** Two-sided: branded-arm `bt_trial_intent` at first exposure differs from the blind arm.
- **IV:** `meta_brand_arm` (randomised). **DV:** trial intent (5-point) at first exposure.
- **Segment:** pooled; the **unaware-of-Ownly subgroup is primary for interpretation**.
- **Method:** Hyderabad survey arms.
- **Threshold:** top-2-box difference ≥ 10 pp for business relevance. Note that n ≈ 100/arm only detects about 20 pp.
- **Test:** Mann-Whitney + r; top-2-box difference with Newcombe CI; ordinal logit with arm + awareness is exploratory.
- **If positive:** use Rapido endorsement prominently.
- **If negative:** lead with the Ownly brand and proposition; de-emphasise Rapido.
- **If null:** report "no large effect detected", not "no effect".

**H7.2 Branding changes expected reliability (two-sided)**
- **DV:** `bt_expected_reliability` at first exposure, compared between arms (`meta_brand_arm`). `br_expected_reliability` is the post-reveal measure, asked in blind arms only, and is used for H7.4.
- **Rationale:** ride-hailing familiarity could raise trust in riders, *or* import cancellation perceptions.
- **Test:** as H7.1.
- **If negative:** reliability messaging must specifically counter the spillover.

**H7.3 Rapido ride experience moderates the brand effect**
- **IV:** arm × `dem_rapido_ride_experience` (positive / negative / none).
- **Test:** ordinal logit interaction (exploratory, low power) + interviews.
- **If validated:** target Rapido riders with positive experience first.

**H7.4 Within-subject reveal shift**
- **Statement:** In the blind arm, trust and intent change after the brand is revealed.
- **Test:** Wilcoxon signed-rank. This is secondary because of demand effects, and is interpreted only alongside H7.1.

### H8 — WTP FOR DELIVERY FEE (Gabor-Granger; final fee points from `01_secondary_research/market_price_anchors.md` + audit)

**H8.1 ★ Ownly's fee is within acceptable range**
- **Statement:** Acceptance at the fee point closest to Ownly's **audit-observed** Gachibowli delivery fee is ≥ 50%. Secondary sources conflict on this fee (₹30 + GST vs free vs distance-based; see `01_secondary_research/market_price_anchors.md` §4), so the fee is taken from the audit, not from media. If the audit observes ₹0, H8.1 is re-framed as acceptance of the fee Ownly would need after launch offers. That re-framing is logged as a deviation.
- **DV:** `wtp_accept_fee_X`.
- **Segment:** pooled; students/professionals.
- **Method:** fee ladder.
- **Threshold *(A)*:** 50%.
- **Test:** Wilson CI on acceptance; acceptance curve with CIs; median acceptable fee (the fee at which acceptance crosses 50%, interpolated, with bootstrap CI).
- **If validated:** the fee is not a barrier.
- **If rejected:** fee is a trial barrier; test a lower fee or a fee waiver above a basket threshold.

**H8.2 Fee elasticity has a kink**
- **Statement:** Arc elasticity of acceptance is largest between two adjacent points around current market fees.
- **Test:** descriptive arc elasticities `((q2−q1)/((q1+q2)/2)) / ((p2−p1)/((p1+p2)/2))`, with bootstrap CIs.
- **Use:** identifies a psychological fee ceiling.

**H8.3 Segment fee curves differ** — tested under H6.2 (cross-reference, not re-tested).

### H9 — BENGALURU → HYDERABAD TRANSFERABILITY (matched comparisons only)

Comparison rules:
- Compare cities only on identical items.
- Reweight Bengaluru to the Hyderabad composition on `seg_occupation × seg_freq` (post-stratification), and also report within-cell comparisons.
- **Non-inferiority margins *(A)*:** PPI and SRI −10 points; proportions −10 pp.

**H9.1 Bengaluru adoption drivers match Hyderabad's top unmet needs**
- **Statement:** The ranking of Bengaluru Ownly users' reasons for choosing Ownly correlates with the ranking of Hyderabad pain categories, on the shared categories.
- **Test:** Spearman rank correlation across categories (few categories, so descriptive) + qualitative comparison.
- **If aligned:** the proposition transfers on need.
- **If misaligned:** adapt the lead benefit.

**H9.2 ★ Hyderabad pain is not materially weaker**
- **Statement:** Weighted Hyderabad PPI − Bengaluru PPI ≥ −10.
- **Test:** difference in means/medians with bootstrap CI (TOST-style non-inferiority: lower CI bound > −10).
- **If validated:** the need transfers.
- **If rejected:** the need is weaker, so ADAPT or TARGET SELECTIVELY.

**H9.3 Bengaluru frictions are more damaging in Hyderabad**
- **Statement:** For the top-3 friction themes in Bengaluru reviews and churn reasons (e.g. ETA, assortment, refunds — to be confirmed from data), the matched Hyderabad expectation is stricter *or* audit conditions are worse. Examples:
  - Hyderabad `exp_eta_max` lower
  - Hyderabad ADI higher
  - Hyderabad Ownly coverage lower
- **Test:** per theme, matched difference with CI; audit coverage by city is only possible if a small Bengaluru audit is run (optional).
- **Output:** the transfer matrix rows.

**H9.4 Incumbent lock-in is not stronger in Hyderabad**
- **DV:** subscription penetration, `dec_habit_lock`, multi-homing.
- **Test:** weighted proportion difference with CI.
- **If lock-in is stronger:** trial needs stronger triggers.

**H9.5 Local assortment needs differ**
- **Statement:** Hyderabad users' most-ordered cuisines and restaurant types differ from Bengaluru's.
- **Test:** chi-square on the coded cuisine/restaurant type of the last order, with Cramér's V; audit coverage of the top categories.
- **Guardrail:** this is tested with data, not cultural stereotypes.

### H10 — ASSORTMENT THRESHOLD

**H10.1 ★ Missing usual restaurants blocks trial for a large share**
- **Statement:** ≥ 40% *(A)* have ADI ≥ 75, meaning they would need most of their usual restaurants available before trying a new app.
- **Test:** Wilson CI.
- **If validated:** supply coverage is a gate.
- **If rejected:** users are willing to explore.

**H10.2 Required restaurant types differ by segment**
- **DV:** `exp_restaurant_types_needed` (favourite known / local / chains / premium / budget).
- **Test:** proportions per type per segment; chi-square with Cramér's V.
- **Use:** prioritises which restaurants to onboard first.

**H10.3 Assortment gaps drive competitor use among Ownly users**
- **Statement:** "Restaurant not available" is among the top-3 reasons Ownly users chose a competitor or reduced use (Bengaluru; Hyderabad if n allows).
- **Test:** ranked proportions with CIs.

**H10.4 Audit coverage vs need**
- **Statement:** Ownly lists and has open ≥ 60% *(A)* of the audit restaurant frame across slots.
- **Test:** coverage proportion with Wilson CI, by slot.
- **If rejected together with H10.1 validated:** a supply-first ADAPT recommendation.

### H11 — BEHAVIOURAL INTENT (say–do)

**H11.1 Framing ranks converge**
- **Statement:** The fake-door CTA-rate ranking of the 3 framings matches the survey's framing preference ranking.
- **Test:** descriptive rank comparison; fake-door pairwise tests with Holm. Labelled DIRECTIONAL unless per-arm n meets the MDE plan (`07_fake_door/experiment_plan.md`).
- **If converged:** higher confidence in the lead message.
- **If diverged:** trust the behaviour, and investigate why.

**H11.2 Intent-to-action ratio**
- **Statement:** The fake-door higher-intent conversion is far below survey top-2 intent.
- **Test:** report the ratio with CIs from both sources. **The sources differ, so this is not a formal test.**
- **Use:** deflate stated intent when projecting.

**H11.3 ★ Aware→tried gap among Hyderabad respondents**
- **Statement:** Among respondents aware of Ownly for ≥ 2 weeks, the share who have ordered is lower than the share who state top-2 intent in the blind arm.
- **Rationale:** A real say–do check that is possible *because* Ownly already operates in Hyderabad.
- **Test:** two proportions with Newcombe CI (different subgroups, so descriptive calibration); logistic regression of `own_tried` on awareness duration, Rapido use and PPI is exploratory.
- **If the gap is large:** the barrier is not awareness but trial friction or trust, so investigate barriers.

### H12 — REPEAT USE (Bengaluru Ownly users + Hyderabad early users)

**Outcome definitions:**
- `own_repeat` = placed ≥ 2 Ownly orders in the last 4 weeks.
- `own_lapsed` = tried Ownly but no order in the last 4 weeks.
- Continue-intent is a secondary outcome.

**H12.1 ★ Reliability predicts repeat more strongly than perceived savings**
- **Statement:** The standardised odds ratio for perceived on-time reliability > the OR for perceived savings.
- **IVs:** `own_perceived_savings`, `own_reliability_rating`, `own_found_restaurants`, `own_support_issue_resolved`, `own_order_accuracy`, `own_trust`; controls: `seg_occupation`, `seg_freq`, tenure, city.
- **DV:** `own_repeat`.
- **Method:** Bengaluru survey (+ Hyderabad users).
- **Minimum n:** ≥ 10 events per predictor (~80–100 Ownly users). Otherwise, bivariate only.
- **Test:** logistic regression (Firth if separation occurs); compare ORs with bootstrap CI of the difference; VIF check.
- **If validated:** operations (on-time delivery) is the retention lever.
- **If rejected (savings is the stronger driver):** price is the retention lever, and reliability is a hygiene factor.

**H12.2 Unresolved incidents predict lapse**
- **Statement:** Users with an unresolved support or refund issue are more likely to be lapsed.
- **Test:** Fisher exact / chi-square; risk ratio with CI.
- **If validated:** fix the support process before scaling.

**H12.3 Assortment predicts share of wallet**
- **Statement:** `own_found_restaurants` correlates with `own_share_of_orders`.
- **Test:** Spearman ρ with CI.

**H12.4 Offer-driven trial predicts lapse (Hyderabad early users)**
- **Statement:** Users whose first-trial trigger was a launch offer are more likely to be lapsed.
- **Test:** Fisher exact. Hyderabad n is likely small, so this is also a qualitative interview theme.

---

## 3. Confirmatory (★) set — Holm-corrected together

H1.1, H1.2, H1.7, H2.1, H2.3, H3.1, H4.1, H5.1, H6.1, H6.3, H7.1, H8.1, H9.2, H10.1, H11.3, H12.1 — **16 tests**.

Holm adjustment applies to the p-value-based tests. CI-threshold decisions for prevalence hypotheses use 95% CIs as specified. The Holm-adjusted equivalent is reported in a sensitivity table.

## 4. Hypothesis → dashboard → evidence trace

Each H# appears in `dim_hypothesis` (see `10_dashboard/dataset_schema.md`) with these fields:
- status: untested / supported / rejected / inconclusive / not testable
- estimate
- CI
- n
- evidence IDs
- contradicting evidence

Each dashboard KPI links to its H#.
