# M. Pre-Analysis Plan (PAP)

**Version:** 2026-09-14, drafted before any data collection.
**Amended 2026-09-18 (A1)** — added §6.7 challenger-pattern predictions P1–P5, two cross-tab cuts and a
second multiplicity family. Still **pre-data**: the response tracker was header-only at the time. See §11.

**Freeze rule.** Freeze this file (commit a dated copy to `09_analysis/PAP_frozen_YYYYMMDD.md`) **before the first survey response is analysed**. Any deviation afterwards goes into §11 "Deviations log", with the reason and the date.

> ⚠ **The freeze has not happened yet.** No `PAP_frozen_*.md` exists. Freeze this file now that A1 is in —
> the pre-registration claim for P1–P5 rests on a dated artefact, not on this sentence.

**Companion files:**
- `00_research_charter/C_hypothesis_tree.md` — hypotheses, thresholds, tests
- `08_clean_data/cleaning_protocol.md` — cleaning rules
- `10_dashboard/dataset_schema.md` — output tables

---

## 1. Principles

1. Tests are tied to hypotheses. No fishing expeditions. Exploratory findings are labelled **EXPLORATORY** and require triangulation before appearing in headlines.
2. Every estimate is reported with **n, a 95% CI and an effect size**, plus a business-significance judgement against the floors in `C_hypothesis_tree.md` §0.
3. Medians and distributions come first for skewed or ordinal data. Means are used only where meaningful (e.g. index scores with acceptable reliability) and always shown alongside medians.
4. Unweighted results are primary for within-Hyderabad analysis (quota sample). **Weighted** results are used only for city comparisons (post-stratification, see E §3). Both are shown.
5. "Don't know / not applicable" is treated as missing for scale statistics, but its share is reported.
6. No imputation for primary hypothesis tests. Complete-case analysis only, with the item missingness rate reported. If missingness on a critical item is > 10%, run a sensitivity check comparing completers and non-completers on segment and frequency.

## 2. Analysis populations

| Population | Definition | Used for |
|---|---|---|
| `HYD_ALL` | Hyderabad CLEANED rows | H1–H8, H10, H11 |
| `HYD_UNAWARE` | `HYD_ALL` with no unaided **and** no aided prior Ownly awareness | H7 primary interpretation |
| `HYD_OWNLY` | `HYD_ALL` who have ordered on Ownly | H12 (Hyderabad), H11.3 |
| `BLR_OWNLY` | Bengaluru current + lapsed Ownly users | H9.1, H12 |
| `BLR_NONUSER` | Bengaluru aware-never-tried + unaware | H9.4 |
| `CITY_MATCHED` | Both cities, core comparable items, Bengaluru reweighted | H9.2–H9.5 |
| `OWNLY_POOLED` | `BLR_OWNLY` ∪ `HYD_OWNLY` with a city indicator | H12.1 regression |

**Sensitivity populations** (run for every ★ hypothesis):
- excluding IIIT-H respondents
- excluding working students
- excluding Ownly-topic recruitment channels (Bengaluru)
- including borderline-excluded rows (flag `EX_borderline`)

## 3. Descriptive analysis (Hyderabad and Bengaluru separately, then matched comparison)

| Block | Variables | Statistics | Chart (dashboard view) |
|---|---|---|---|
| Sample | Screener flow, segment, frequency, locality, channel, arm/block balance | Counts, % ; CONSORT-style flow | Flow diagram (V1) |
| Ordering intensity | `scr_orders_4wk`, weekday/weekend, occasions, time of day | Distribution, median band | Sorted bars, heatmap occasion × time (V3) |
| Spend | `beh_last_order_total`, basket size | Median, IQR, bootstrap 95% CI; box plot by segment | Box plot (V3) |
| Platforms | Used in last 4 weeks, primary, multi-homing, subscriptions | % with Wilson CI | Sorted bars (V3) |
| Pain | 4 PPI items + incident items | Item distributions (diverging Likert); PPI median + CI | Diverging Likert, distribution (V3) |
| Decision criteria | Top-3 selection | % selected with CI, sorted | Sorted bars (V3/V4) |
| Expectations | ETA max (lunch/dinner), ADI, restaurant types, refund expectation | Median + CI; % | Dot/CI plots (V5) |
| Awareness | Unaided/aided Ownly awareness, trial, repeat | % with CI; funnel | Funnel (V1/V4) |

## 4. Derived metrics (exact formulas)

All indices are reported **with their component items**. An index is used as a composite only if Cronbach's α ≥ 0.60 *(A)* (or, for 3-item mixed-format indices, inter-item Spearman correlations are all ≥ 0.15). Otherwise report the components separately and drop the composite. No opaque vanity scores.

| Metric | Formula | Range | Missing rule | Validity check |
|---|---|---|---|---|
| **PPI** — Price Pain Index | `((mean(pain_fee_reconsider_freq, pain_bill_unreasonable_freq, pain_menu_markup_belief, beh_abandon_price_freq)) − 1) / 4 × 100`, items on 1–5 | 0–100 | ≥ 3 of 4 items; else NA | α; item-total correlations; correlation with `beh_last_order_total` reported descriptively |
| **SRI** — Switching Readiness Index | `mean(r(bt_trial_intent), r(multihome5), r(6 − dec_habit_lock))` where `r(x) = (x−1)/4×100`, `multihome5 = 5 if beh_platforms_used_4wk ≥ 2 else 1` | 0–100 | All 3 required | Inter-item correlations; **for H1.7 use SRI without `bt_trial_intent` as a robustness check**. Note: `bt_trial_intent` is measured at first exposure, so for the branded arm SRI includes a brand effect — compute SRI on blind-arm-equivalent terms (first-exposure intent) and include arm as a control in any model |
| **RSS** — Reliability Sensitivity | `# price-vs-reliability choice tasks where the more reliable + more expensive alternative was chosen / # such tasks shown × 100` | 0–100 | Respondent must have seen ≥ 2 such tasks | Correlation with `pain_incident_any_3m` (H4.3) |
| **ADI** — Assortment Dependency | `(exp_fav_restaurant_needed − 1) / 4 × 100` | 0–100 | Single item; NA if DK | Correlation with the "restaurant not available" frustration |
| **ETA tolerance (stated)** | `exp_eta_max_dinner`, `exp_eta_max_lunch` (minutes) | min | — | — |
| **wtp_max_fee** | Highest fee point accepted in the ladder, given monotone answers | ₹ | NA if non-monotone (flag; count reported) | Non-monotone share < 10% expected |
| **Required switching savings** | `beh_switch_savings_required` (₹); the "no amount" option is coded as a separate flag, not as ∞ | ₹ | — | — |
| **Model-based WTP** | `WTP_k = −β_k / β_price` (sign per coding), with a Krinsky-Robb 95% CI (5,000 draws) | ₹ per attribute step | — | Only if β_price is significant (p < 0.05); otherwise "not identifiable" |
| **Audit pair gap** | `final_payable(Ownly) − final_payable(comparator)` on a matched key | ₹ | Matched pairs only | — |
| **Ownly market-fit scorecard** | See `11_insights/decision_framework_and_scorecard.md` | 0–100 per dimension | Evidence-strength badge required | Weight sensitivity |

## 5. Inferential tests (tied to hypotheses)

| Situation | Test | Effect size | Notes |
|---|---|---|---|
| Single proportion vs threshold | Wilson 95% CI; CI-threshold rule | Difference from threshold (pp) | Exact binomial if n < 30 |
| Two independent proportions | Two-proportion z / Fisher exact (expected cell < 5) | Difference (pp) with Newcombe CI; risk ratio | |
| Paired proportions (same respondent) | McNemar | Paired difference with CI | H1.2 |
| Ordinal/skewed, 2 groups | Mann-Whitney U | Rank-biserial r with bootstrap CI | Also report the Hodges-Lehmann shift |
| Paired ordinal | Wilcoxon signed-rank | Matched-pairs r | H3.3, H7.4 |
| Categorical × categorical | Chi-square (Fisher/Monte-Carlo if sparse) | Cramér's V | Collapse sparse levels **as pre-specified**: ≤ 5 expected → merge adjacent ordinal levels |
| Continuous/index, 2 groups | Welch t-test **only if** distribution is roughly symmetric; otherwise Mann-Whitney | Cohen's d / Hedges' g | Report both if uncertain |
| Association | Spearman ρ with bootstrap CI | ρ | |
| Non-inferiority (city transfer) | CI of the weighted difference vs margin | Difference | H9.2 |
| Medians | Bootstrap percentile CI (10,000 resamples, seed = 20260914) | — | Fixed seed for reproducibility |

## 6. Models

### 6.1 Choice experiment (H2.1, H3.1, H4.1, H4.2, H5.1, H5.2, H6.3)

- **Data:** long format, `resp_id × task × alternative` (+ opt-out if included).
- **Coding:**
  - price: linear (₹)
  - ETA: linear minutes, plus a dummy-coded check for H3.2
  - reliability: dummy
  - assortment: dummy (most/some/few, with "most" as reference)
  - refund assurance: dummy
- **Model 1 (primary):** pooled conditional logit with respondent-clustered SEs.
- **Model 2:** Model 1 + segment × attribute interactions (students vs professionals).
- **Model 3 (exploratory, only if n ≥ 200 and it converges):** mixed logit with random price and ETA coefficients, used to show heterogeneity.
- **Diagnostics:**
  - failing a pre-included dominance check → sensitivity analysis excluding those respondents
  - always choosing the left or right option (≥ all tasks) → flag
  - McFadden pseudo-R², hit rate on held-out tasks if a holdout task is included
- **Fallback if n < 125** or price is not significant: task-level choice shares with Wilson CIs and descriptive trade-off statements only ("in task T, X% chose the ₹40-cheaper-but-15-minutes-slower option").
- **Claim discipline:** statements like "₹X compensates for Y minutes for segment A but not B" require (a) a significant price coefficient, (b) a WTP CI for each segment, and (c) the segment difference CI excluding 0. Otherwise the statement is **not made**.
- **Library:** Python `statsmodels` (`ConditionalLogit`) or `pylogit`/`xlogit`; the choice is recorded in `requirements.txt`.

### 6.2 Gabor-Granger fee ladder (H8, H6.2)

- **Acceptance curve:** `P(accept | fee)` with a Wilson CI per point, pooled and per segment.
- **Median acceptable fee:** linear interpolation where acceptance crosses 50%, with a bootstrap CI.
- **Arc elasticity** between adjacent points, with bootstrap CIs.
- **Segment comparison:** logistic regression `accept ~ fee + segment + fee×segment`, respondent-clustered SEs.
- **Revenue-proxy curve** `fee × P(accept)` is shown **only** as an illustration of the trade-off. It is not a pricing recommendation, because it ignores basket size, frequency, cost and competitive response.

### 6.3 Brand experiment (H7)

- **Primary:** between-arm comparison at first exposure (Mann-Whitney + top-2-box difference), in `HYD_ALL` and `HYD_UNAWARE`.
- **Balance table:** arm × segment, frequency, awareness, Rapido ride use (SMDs).
- **Exploratory:** ordinal logistic `intent ~ arm + aware + arm×rapido_experience + seg_occupation + seg_freq`.

### 6.4 Switching intent / repeat-use models

- **H1.7 / exploratory switching driver model** (`HYD_ALL`):
  - Outcome: `high_switch_intent` = `bt_trial_intent` top-2 at first exposure.
  - Predictors: PPI, RSS, ETA tolerance, ADI, `dec_habit_lock`, `beh_multihome`, subscription, `seg_freq`, `seg_occupation`, arm.
  - ≤ 10 predictors, EPV ≥ 10.
  - Logistic regression with standardised continuous predictors; report ORs with 95% CIs, VIF, AUC with bootstrap optimism correction.
  - **Interpretation:** associations, not causes.
- **H12.1** (`OWNLY_POOLED`):
  - Outcome: `own_repeat`.
  - Predictors: perceived savings, reliability rating, found restaurants, support-issue resolved, order accuracy, trust.
  - Controls: city, tenure band, `seg_occupation`.
  - If EPV < 10: reduce to the 3 pre-specified key predictors (reliability, savings, restaurants). If still < 10: bivariate tests only.
  - Firth-penalised logistic if separation occurs. **Open item (2026-09-14):** Firth is not yet implemented in `09_analysis/`. Before the PAP is frozen, implement it (e.g. with `firthlogist`), or pre-register the fallback: exact/Fisher bivariate tests only. The choice must be made before the data is seen.
  - The difference between the standardised reliability and savings coefficients uses a bootstrap CI.

### 6.5 Competitor audit (H2.3, H3, H5, H10.4)

- **Matched key:** `restaurant_id × basket_id × slot × capture date × drop_point_id × account_state`. Platforms are captured within ±10 minutes.
- **Pair gap:**
  - median and bootstrap CI (cluster bootstrap by restaurant, to account for repeated restaurants)
  - distribution (box/strip)
  - win rate (ties within ₹5)
  - by slot and subscription state
- **Coverage:** listed and open, by platform and slot.
- **ETA:** shown-ETA midpoint gap, median and CI.
- **Offline premium:** only on rows where `offline_subtotal_verified` is present.
- **Consistency:** share of restaurants where Ownly is the cheapest in ≥ 75% of their captures.

### 6.6 Fake door (H11)

As per `07_fake_door/experiment_plan.md`:
- funnel per variant
- Wilson CIs
- pairwise two-proportion / Fisher tests with Holm correction
- descriptive Bayesian P(best)
- **DIRECTIONAL** label if below the pre-computed per-arm n

### 6.7 Challenger-pattern predictions P1–P5 (SECONDARY, pre-registered 2026-09-18)

**Provenance.** Derived from `01_secondary_research/challenger_failures/D_synthesis_why_challengers_fail.md`
§6 — five failure mechanisms common to Uber Eats India, Foodpanda, Amazon Food, ONDC, Thrive and DotPe.
**Added 2026-09-18, before the first survey response** (`13_survey_v3_live/survey_response_tracker.csv`
was header-only at the time of writing; see §11 amendment A1). Registered here so the pattern cannot be
fitted to the data after the fact.

**Status and limits.**
- This is a **SECONDARY family**. It does **not** join the ★ confirmatory set (§8) and **never**
  overrides it or the decision rule in `11_insights/decision_framework_and_scorecard.md` §3.
- Most tests below **re-use analyses already planned** in §5–§6 under a new interpretive frame. Only
  the two cuts marked **[NEW CUT]** add analyses the PAP did not previously contain.
- Every threshold marked *(A)* is an editable assumption, fixed now, changeable only via §11.
- These are **stated-preference** measures. A prediction "holding" is evidence about intent, not behaviour.

| ID | Prediction | Population | Variables | Test + effect size | Pre-registered decision rule | Falsified if |
|---|---|---|---|---|---|---|
| **P1** | **Price framing wins trial but does not survive to repeat** (mechanism M1: rented demand). The conjunction is the point — either half alone is uninformative. | `HYD_ALL` for trial; `HYD_ALL` post-concept (Q37) and `HYD_OWNLY` (Q32) for repeat, reported separately, never pooled | `prop_forced_choice` (Q22); `own_repeat_no_promo` (Q32/Q37); `own_next10_alloc` (Q33/Q38) as support | Trial: exact binomial vs 50% on P-vs-Q excluding "can't choose", Wilson CI (this is the existing primary within-survey test). Repeat: Wilson CI on top-2-box (*Probably* + *Definitely*) | **P1 holds** if Service P's lower CI bound > 50% **AND** `own_repeat_no_promo` top-2 **upper** CI bound < 50% *(A)*. Report the "can't choose" share alongside — a large share weakens both halves | Service P wins trial **and** repeat top-2 **lower** CI > 50% → **Case A. The price proposition retains, and the failure pattern does not apply.** Record this as the headline |
| **P2** | **Coupon-dependent users see no Ownly advantage.** Audit: Ownly cheapest 4/4 on list+fees but only 2/4 after each app's auto-applied offer. So the structural saving should be worth less to people who always order on a coupon | `HYD_ALL`, `Don't know` excluded (share reported) | `beh_offer_dependency` (Q13) banded **LOW = 0–1, 2–4** vs **HIGH = 5–7, 8–10**; outcomes `prop_forced_choice`, `beh_switch_savings_required` (Q19) | Two-proportion z (Fisher if any expected cell < 5), Newcombe CI on the pp difference; Mann-Whitney + Hodges-Lehmann shift on required savings **[NEW CUT]** | **P2 holds** if HIGH-dependency respondents choose Service P at a **lower** rate (Newcombe CI excludes 0) **or** require a **larger** switching saving (HL shift CI excludes 0) | CI includes 0, **or the direction reverses**. ⚠ **A reversal is genuinely plausible and must not be explained away:** heavy coupon users may simply be more price-motivated, in which case HIGH-dependency respondents choose P *more*. That result falsifies P2 and is itself a finding |
| **P3** | **The observed ETA gap exceeds stated tolerance** (mechanism M3: same restaurants, slower). Audit medians: Ownly 39.5 min vs Swiggy 22.5, Zomato 17.5 — **a ~17 min gap.** Q16 tests a **15 min** gap for the same ₹30, so the survey **understates** the real trade | `HYD_ALL` | `tradeoff_eta` (Q16); `exp_eta_max_dinner` (Q20) | % choosing ₹230/45-min with Wilson CI (existing pre-registered rule: ₹30 "buys" 15 min only if **lower CI > 50%**). Separately: % whose `exp_eta_max_dinner` < **39.5 min**, Wilson CI | **P3 holds** if the ₹230/45-min lower CI bound is **not** > 50%, **or** a majority state a dinner ETA ceiling below 39.5 min (lower CI > 50%). **One-directional inference to state explicitly:** because Q16 tests 15 min and the observed gap is ~17 min, failing at 15 min implies failing at 17 min *a fortiori*. The converse does **not** hold | Lower CI > 50% on Q16 **and** median `exp_eta_max_dinner` ≥ 39.5 min → the speed deficit is tolerable and M3 does not bind here |
| **P4** | **Assortment people cannot get elsewhere beats "same restaurants, cheaper."** Audit: 89% cross-platform overlap (K42), local coverage 100% vs chain 80% (K41), and exactly one Ownly-only restaurant observed | `HYD_ALL` | `tradeoff_eta` (Q16), `tradeoff_rel` (Q17), `tradeoff_rest` (Q18) — all three hold ₹30 constant and vary what ₹30 buys; `prop_reason` (Q23) free text; fake-door arms | Paired design (same respondents answer all three) → **McNemar** on premium-option choice between Q18 and Q16, and Q18 vs Q17; matched-pairs effect size, Holm within P4. `prop_reason` coded for spontaneous assortment mentions (§9 rules, double-coded) | **P4 holds** if the premium-option share is **higher for `tradeoff_rest` than for `tradeoff_eta`** (McNemar CI on the paired difference excludes 0) — i.e. people defend assortment harder than speed | Premium share for `tradeoff_eta` ≥ `tradeoff_rest` → speed matters more than assortment, and the §4.1 recommendation in file D is wrong |
| **P5** | **Durability doubt suppresses the price proposition independently of the observed gap** (37 social items expect fee creep; two cite Toing adding fees after launching free) | `HYD_ALL` | `prop_durability_doubt` (Q24, 5-pt) × `prop_forced_choice`; support: `own_tried` | Spearman ρ (doubt vs P-choice coded 1/0) with bootstrap CI; and banded *Agree+Strongly agree* vs rest, two-proportion z with Newcombe CI **[NEW CUT]** | **P5 holds** if higher durability doubt is associated with **lower** Service P choice (CI excludes 0) | CI includes 0 → the fee-creep narrative is loud in public discussion but does not move stated choice. Given 92 PRICE_DOUBT items in the corpus, **a null here is a substantive finding about the gap between discourse and decision**, not a failed test |

**Reporting rule.** P1–P5 are reported in one table with the ★ set clearly separated, each labelled
**SECONDARY — PRE-REGISTERED (challenger-pattern)**. Any P that is not computable at the achieved n is
reported as **NOT TESTABLE**, never silently dropped. Because these predictions were generated from a
pattern in six *other* companies' histories, a confirmation is corroboration by analogy — it raises
confidence, it does not establish the mechanism in Gachibowli.

## 7. Cross-tab plan (only these pre-specified cuts)

| Cut | Applied to |
|---|---|
| Student vs working professional | All H1–H8, H10 metrics |
| Frequent vs regular vs occasional | PPI, SRI, spend, fee WTP, choice shares |
| Ownly user vs aware-never-tried vs unaware | Pain, trust, lock-in, barriers |
| High vs low price pain (PPI ≥ 50 vs < 50) | Choice-experiment WTP, fee acceptance, SRI |
| Brand arm | H7 outcomes only |
| City (matched items, weighted) | H9 only |
| Subscription holder vs not | Fee WTP, habit lock, audit subscription-state gaps |
| **Offer dependency: LOW (0–1, 2–4) vs HIGH (5–7, 8–10)** — added 2026-09-18 | `prop_forced_choice`, `beh_switch_savings_required` (**P2 only**) |
| **Durability doubt: Agree+Strongly agree vs rest** — added 2026-09-18 | `prop_forced_choice` (**P5 only**) |

Any cut not in this table is **exploratory** and labelled as such.

## 8. Multiplicity

- The ★ confirmatory set (16) uses Holm-Bonferroni on p-values (family-wise α = 0.05).
- **The challenger-pattern set P1–P5 (§6.7) is a separate family** with its own Holm-Bonferroni correction at family-wise α = 0.05. It is deliberately **not** merged into the ★ family: adding 5 tests to the confirmatory family would raise the correction burden on the 16 primary hypotheses, weakening the tests the study exists to run. The cost of separating them is that the *overall* study-wide error rate is not controlled across both families — this is stated openly rather than hidden, and is the reason P1–P5 can support a recommendation but never drive one on their own.
- Within P4, the two McNemar comparisons (Q18 vs Q16, Q18 vs Q17) are Holm-corrected inside P4 before P4 enters the family correction.
- Exploratory tests are reported with unadjusted p-values, marked "exploratory, unadjusted", and **never** used alone for a recommendation.

## 9. Qualitative synthesis methodology

1. **Transcription:** de-identify (names, employers, addresses → `[REDACTED-TYPE]`).
2. **Familiarisation:** two coders read 3 transcripts each and write memos.
3. **Codebook:** start from the deductive seed codes (`04_interviews/coding_framework.md`) and add inductive codes. Codebook v1 is frozen after 4 transcripts.
4. **Double-coding:** ≥ 20% of transcripts (≥ 3). Compute percent agreement and Cohen's κ per code family, then reconcile. κ < 0.6 → refine the definition and re-code.
5. **Synthesis ladder** per theme: OBSERVATION → USER QUOTE (verbatim, with `interview_id` and timestamp) → INTERPRETATION (labelled) → INSIGHT → OPPORTUNITY.
6. **Prevalence language rule:** "N of M interviewees (segments …)". Never "most users". An insight requires ≥ 3 interviews across ≥ 2 segments; otherwise it is labelled "single-source signal".
7. **JTBD and switch forces** (push / pull / anxiety / habit) are built only from coded incidents, with counts and counter-evidence.
8. **Reviews/social:** inductive taxonomy with frequency × severity. Human validation of a 50-row sample, with agreement reported.
9. **AI assistance:** first-pass coding only. Human review of 100% of quotes used in outputs; verbatim quotes are checked against transcripts.

## 10. Triangulation

Handled in `11_insights/insight_evidence_matrix_template.csv` and the confidence rules in `11_insights/decision_framework_and_scorecard.md` §5. Contradictions get their own column and are discussed in the final report.

## 11. Amendments and deviations log

**Amendments** are changes made *before* any data was collected. **Deviations** are changes made after.
The distinction is recorded because only the second damages pre-registration.

### Amendments (pre-data)

| # | Date | Section | Amendment | Reason | Evidence that no data existed yet |
|---|---|---|---|---|---|
| **A1** | 2026-09-18 | **New §6.7**; §7 (2 cuts added); §8 (second family) | Added challenger-pattern predictions **P1–P5** as a separate pre-registered SECONDARY family, with two new cross-tab cuts (offer dependency; durability doubt) and a separate Holm family | New secondary research (`01_secondary_research/challenger_failures/`, 5 dossiers, ~230 sources) established a repeated failure pattern across six challengers. Registering the predictions **before** data prevents the pattern being fitted to results afterwards | `13_survey_v3_live/survey_response_tracker.csv` was **header-only (zero rows)** on 2026-09-18; `_ops/progress.md` records counts "all 0" through 2026-09-17 |

### Deviations (post-data)

| Date | Section | Deviation | Reason | Impact on interpretation |
|---|---|---|---|---|
| | | | | |

### Known pre-existing inconsistency (flagged 2026-09-18, not resolved here)

§4's **SRI** formula is **not computable** from the live v3 form. **Two of its three components are
absent** from `13_survey_v3_live/survey_questions.md`: `bt_trial_intent` and `dec_habit_lock` (no `bt_`
or `dec_` variable exists in v3 at all; "habit" survives only as an answer option in
`oth_choice_driver`, which is the *other-city* module and is not asked of Hyderabad respondents). Only
`multihome5` ← `beh_platforms_used_4wk` remains, so **SRI currently reduces to a single binary item** —
which PAP §4's own composite rule already says should be dropped rather than reported as an index.

> ⚠ **Correction (2026-09-18):** an earlier version of this entry said a human could *"redefine SRI on
> the two remaining components."* There is only **one** remaining component. That sentence was wrong
> and is superseded by the memo below.

This is a pre-existing mismatch between the 14 Sep PAP and the 16 Sep instrument, found while
registering P1–P5. It is **not** silently patched. Three costed options — constrained by the fact that
any rebuild using `beh_switch_savings_required`, `beh_platforms_used_4wk` or `beh_subscriptions` would
**double-count** a variable D2 already scores separately — are set out in
**`09_analysis/SRI_options_decision_memo.md`**. A human picks one; it is logged here as amendment **A2**
and in `_ops/decisions.md` as **D17**.

**SRI feeds D2 (35%) of the decision scorecard**, so this blocks a scored dimension and must be
resolved **before** the PAP is frozen.

## 12. Code plan (to be implemented in `09_analysis/`)

| Script | Input | Output |
|---|---|---|
| `00_manifest_and_hash.py` | `08_clean_data/raw/*` | `raw/MANIFEST.csv` with SHA-256 |
| `01_ingest_and_harmonise.py` | Raw form exports (4 Hyderabad versions + Bengaluru) | `interim/combined_long_names.csv` (variables renamed per dictionary) |
| `02_quality_flags.py` | interim | `08_clean_data/flags.csv` (all `EX` codes, per row) |
| `03_split_clean_excluded.py` | interim + flags + adjudication log | `cleaned/*.csv`, `excluded/*.csv` with `exclusion_reason` |
| `04_derive_metrics.py` | cleaned | `fact_survey_respondent.csv`, `fact_dce_long.csv`, `fact_wtp_long.csv`, `fact_bill_choice_long.csv` |
| `05_descriptives.py` | facts | `outputs/descriptives/*.csv` |
| `06_hypothesis_tests.py` | facts | `outputs/hypothesis_results.csv` → `dim_hypothesis` |
| `07_dce_models.py` | `fact_dce_long` | `outputs/dce_coefficients.csv`, `dce_wtp.csv` |
| `08_wtp_curves.py` | `fact_wtp_long` | `outputs/wtp_curve.csv` |
| `09_city_transfer.py` | `CITY_MATCHED` | `outputs/transfer_metrics.csv` |
| `10_audit_analysis.py` | `06_competitor_audit/data/audit_obs.csv` | `fact_audit_pairs.csv`, `outputs/audit_summary.csv` |
| `11_reviews_merge.py` | `05_review_mining/*_coded.csv` | `fact_reviews.csv` |
| `12_fakedoor.py` | `07_fake_door` events | `agg_fakedoor_variant.csv` |
| `13_scorecard.py` | all outputs + weights config | `fact_scorecard.csv` + sensitivity |
| `run_all.sh` | — | Full pipeline, fixed seeds |
