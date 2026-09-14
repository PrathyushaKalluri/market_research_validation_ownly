# Ownly Gachibowli Market-Fit Dashboard — Blueprint

**Owner:** Agent F (dashboard workstream) · **Drafted:** 2026-09-14 · **Revised:** 2026-09-14, aligned to the final lead specs (see §6).

**Status:** blueprint plus demo prototype. No real data has been collected yet.

> **Evidence rule for this whole dashboard:** every number on screen traces back to three things: (a) a hypothesis ID (H1–H12), (b) a mart table and field, and (c) a base size. The prototype in `prototype/dashboard_demo.html` uses **synthetic data only** and shows "DEMO DATA — REPLACE WITH REAL DATA" on every view and card. Never screenshot demo views into a report.

**Authoritative inputs** (this blueprint follows them; where they conflict, they win):

| Topic | File |
|---|---|
| Survey variables | `03_hyderabad_survey/survey_variable_dictionary.csv` |
| Choice design | `03_hyderabad_survey/dce_design_matrix.csv` |
| Scorecard dimensions, anchors, weights, gates, decision rule, confidence overlay, alternative weight sets, triangulation rules | `11_insights/decision_framework_and_scorecard.md` (§1–§3, §5) |
| Metric formulas, tests, script and output names | `09_analysis/M_pre_analysis_plan.md` (PAP) |
| Audit | `06_competitor_audit/audit_schema.csv` + `audit_calculations.md` |
| Fake door | `07_fake_door/events_schema.json` + `analyze_fakedoor.py` |
| Reviews / social | `05_review_mining/*/…_coded.csv` |

Companion files:
- `dataset_schema.md` + `schema/*.csv`: mart tables, with headers generated from those sources.
- `build_instructions.md`: build steps.
- `prototype/dashboard_demo.html`: the demo.

---

## 1. Audience and the decisions it supports

| Audience | What they do with it | Views used most |
|---|---|---|
| Professors / examiners | Check bases, matched comparisons, uncertainty, whether conclusions follow from evidence | 1, 2, 5, 8, the evidence-trace drawer |
| Product managers (Ownly/Rapido-style reader) | Choose the target segment, lead proposition, must-fix guardrail | 1, 4, 5, 6, 10 |
| Business leadership | SCALE / TARGET SELECTIVELY / ADAPT / RETHINK PROPOSITION for Gachibowli | 1, 2, 10 |
| The research team | Monitor quotas, spot weak evidence, write insight titles honestly | 3, 6, 7, 9 |

## 2. Tool recommendation

**Constraints:**
- 3-person student team.
- Google Forms → Sheets for the survey; Apps Script → Sheet for fake-door events.
- Budget ≈ ₹0.
- Professors must open it with no licence.
- The statistics are not spreadsheet-friendly: conditional logit, WTP curves, Wilson and bootstrap CIs, post-stratified city comparison, logistic regression, and the framework scorecard with NOT TESTABLE handling.
- Everything must be reproducible.

| Criterion | Tableau | Power BI | Looker Studio | Python + Plotly | Hand-built HTML |
|---|---|---|---|---|---|
| Cost / access | Public = data public; Desktop needs a licence | Sharing needs Pro or a public embed | **Free, view-only link** | Free, file | Free, file / Artifact |
| Sheets connection | Brittle | CSV | **Native** | via CSV | via CSV |
| DCE / WTP / CIs / scorecard | Precomputed only | Partly | Precomputed only | **Native** | Precomputed or in-page |
| Reproducibility | Low | Medium | Low | **High** | High if generated |
| Build effort | Med–high | Med–high | **Low** | Medium | High |

**Recommendation:** run the PAP §12 Python pipeline and write the mart CSVs to a Google Sheet, then build the shared dashboard in **Looker Studio**. Export Plotly HTML for the hero charts (Views 2, 5, 8) as the reproducible appendix.

Why:
1. All maths lives in code the professor can audit. The BI layer only displays it.
2. Looker Studio is free, reads Sheets natively and shares with a view-only link.
3. Tableau Public would publish respondent-level data.

The HTML prototype is the layout and interaction spec, and can be regenerated from real mart CSVs if Looker's chart types prove too limited.

---

## 3. Global rules

### 3.1 Global filters (one row above all charts; every chart re-renders against the same slice)

| Filter | Field (canonical) | Applies to | Default |
|---|---|---|---|
| City | `city` | Survey tables; audit is HYD-only; reviews not filtered | Hyderabad |
| Occupation | `seg_occupation` (from `seg_occupation_raw`) | Survey, interviews | All |
| Delivery frequency | `seg_freq` (from `scr_orders_4wk` codes) | Survey, interviews | All |
| Area | `scr_area` | Survey (city-specific codes) | All |
| Primary platform | `beh_platform_primary` | Survey | All |
| Membership | `beh_any_subscription` (from `beh_subscriptions`) | Survey | All |
| Ownly status | `own_status`: dashboard-derived from `own_tried`, `own_repeat`, `own_aware_any` | Survey | All |
| Brand arm | `meta_brand_arm` (blind / branded; HYD only) | Concept and brand charts | All |
| Where found | `meta_found_survey` (`meta_source` = utm in QC) | Survey | All |

When a filter does not apply to a chart's source, the chart shows a muted "filter not applied: …" chip. It never silently ignores the filter.

### 3.2 Base size
| Unweighted n | Display |
|---|---|
| ≥ 60 | Normal, `n = …` |
| 30–59 | "Low base" chip; CI mandatory; no insight title |
| < 30 | Suppressed: "n < 30, not shown" (audit cells use a lower display floor, labelled directional; interviews are qualitative) |

Weighted comparisons also show `n_eff`. Every proportion carries a Wilson 95% CI. Medians carry bootstrap CIs, and medians come first for skewed or ordinal data (PAP §1.3).

### 3.3 Insight-title rule
Titles are descriptive by default. An insight title is allowed only when all of these hold:
- the pre-registered test for the linked H# is complete
- the CI clears the threshold
- n ≥ 60 per compared group
- the claim sits in `fact_evidence_matrix` at MEDIUM or HIGH confidence

`dim_chart.title_mode` controls this, and a reviewer (not the builder) flips it. The demo shows `[Insight title goes here once data supports it]` on every chart.

### 3.4 Evidence trace
Every KPI and chart carries a chip `H# · table.field · strength`. It opens a drawer with:
- the hypothesis statement
- source table and field
- filters in force
- the §5 confidence rule
- test and result (from `dim_hypothesis`)
- linked insights and contradictions (from `fact_evidence_matrix`)

### 3.5 Evidence badges
- **Scorecard badges** follow framework §1 (below).
- **Insight confidence** follows framework §5:
  - **HIGH:** ≥ 2 independent evidence types, including ≥ 1 quantitative source that meets its threshold, AND ≥ 3 interviews across ≥ 2 segments or a consistent review signal, AND no unexplained contradiction.
  - **MEDIUM:** one quantitative source that meets its threshold, plus qualitative support.
  - **LOW:** a single source type, directional-only evidence, or an unexplained contradiction.
  - Special rules: a single interview never exceeds LOW; reviews and social data alone never exceed LOW for prevalence; price-advantage insights need audit evidence to reach HIGH.
- **Chart chips** use a simple base-size proxy: LOW if n < 60, MEDIUM for one source with n ≥ 60, HIGH only where ≥ 2 source types feed the chart.

### 3.6 Colour and form (validated with the dataviz palette validator)
- Hyderabad = blue `#2a78d6` / `#3987e5`; Bengaluru = orange `#eb6834` / `#d95926`.
- Students = aqua `#1baf7a` / `#199e70`; working professionals = violet `#4a3aa7` / `#9085e9`; working students = magenta (composition chart only).
- **Platforms (Ownly, Swiggy, Zomato, …) never use brand colours.** They use the neutral palette (ink / mid-grey / light-grey, filled vs ring) with names as labels, or small multiples headed by the platform name.
- Fee components use ordered blue steps, in bill order.
- Status colours are used only for verdicts and gates (always with an icon and a label): good = TRANSFERABLE / SCALE; warning = NEEDS ADAPTATION / ADAPT / low base; critical = NON-TRANSFERABLE / RETHINK / gate failed; muted = UNKNOWN / INSUFFICIENT EVIDENCE / PROVISIONAL.
- Diverging Likert: red ↔ grey midpoint ↔ blue.
- No pie charts. No dual axes. Every chart has a table view (it's also the relief path for sub-3:1 hues).
- **Ownly delivery fee:** never drawn as a constant or a reference line. It is shown as the text "Ownly fee: audit-observed (TBD)" (the fee is contested: ₹30+GST vs free vs distance-based). Fee-ladder points are labelled **provisional**.

---

## 4. Information architecture: 10 views

Order: verdict → transfer → behaviour → switching → trade-offs → segments → voice → behaviour test → market reality → recommendation.

### VIEW 1 — Executive Market-Fit Scorecard
**Decision question:** Across the five decision dimensions, does the evidence support SCALE, TARGET SELECTIVELY, ADAPT or RETHINK PROPOSITION for Gachibowli, and is the call robust to the weights?

**Scorecard = framework §1–§3, implemented exactly.**

Scopes: pooled Hyderabad, students, working professionals, frequent users. D4c and D5b pool Hyderabad + Bengaluru Ownly users, as the framework specifies.

| Dim | Inputs (weight within dimension) | Weak → strong anchor |
|---|---|---|
| D1 Need (20%) | a) PPI median (40%) | 25 → 65 |
| | b) % abandoned after seeing the final amount, `beh_abandon_price_freq` ≥ 2 (30%) | 10% → 50% |
| | c) % `pain_fee_reconsider_freq` ≥ 3 (30%) | 20% → 70% |
| D2 Switching (20%) | a) SRI median (35%) | 30 → 70 |
| | b) % whose `beh_switch_savings_required` ≤ audit median Ownly saving (35%) | 10% → 60% |
| | c) `beh_multihome` (15%) | 30% → 80% |
| | d) % without an incumbent membership (15%) | 40% → 90% |
| D3 Economic (20%) | a) audit win rate (40%) | 30% → 80% |
| | b) audit median saving as % of median basket (30%) | 0 → 15% |
| | c) fee-ladder acceptance at Ownly's actual fee (30%). **NOT TESTABLE until the audit confirms the fee** | 30% → 75% |
| D4 Experience (25%) | a) ETA acceptability: 100 × min(1, (median `exp_eta_max_dinner` − incumbent median shown ETA) / audit median ETA gap); 100 if gap ≤ 0 (30%) | formula |
| | b) Coverage adequacy: 100 × min(1, coverage / (1 − share ADI≥75 × 0.5)) (30%) | formula |
| | c) % Ownly users on time most of the time, `own_reliability_rating` ≥ 4 (25%) | 50% → 85% |
| | d) 100 − severity-weighted share of reliability/support/refund review themes (15%) | 50% → 0, 10% → 100 |
| D5 Behavioural (15%) | a) aware ≥ 2 weeks → tried, HYD (40%) | 10% → 50% |
| | b) `own_repeat` among HYD + BLR users (35%) | 20% → 60% |
| | c) fake-door best higher-intent rate ÷ survey top-2 intent (25%) | 0.05 → 0.30 |

- **Missing inputs:** an input is NOT TESTABLE when n < 30 (or its source is unconfirmed). It is dropped and the remaining weights are re-normalised. The badge drops one level per missing input. If more than half of a dimension's weight is missing, the dimension shows **INSUFFICIENT EVIDENCE** with no score.
- **Badge operationalisation (for the lead to confirm):** start at LOW if scope n < 60; otherwise HIGH if the testable inputs span ≥ 2 source types (survey / audit / reviews / fake door), else MEDIUM. D5 is capped at MEDIUM while the fake-door result is directional. Then apply the per-missing-input drop.
- **Weights:** default 20/20/20/25/15, editable. Alternative sets are always reported: Equal 20×5 · Behaviour-first 15/15/20/20/30 · Price-thesis 20/20/30/20/10.
- **Decision rule, in order:**
  1. **RETHINK PROPOSITION** if D1 < 40 or D2 < 40, pooled **and** in both segments.
  2. **SCALE** if the total is ≥ 70, no dimension is < 50, and the D5 badge is ≥ MEDIUM (all five dimensions must be scored).
  3. **TARGET SELECTIVELY** if a segment (students / professionals / frequent users, n ≥ 60) meets SCALE.
  4. **ADAPT** if D1 ≥ 50 and D2 ≥ 50 but D3 or D4 < 50 (name the fix: price architecture vs experience/supply).
  5. Otherwise **ADAPT**, naming the weakest dimension.

  Any dimension < 40 blocks SCALE. **Confidence overlay:** if ≥ 2 dimensions are LOW or INSUFFICIENT, label the call "PROVISIONAL — evidence insufficient" and make the next experiment the primary recommendation.

**KPI tiles** (each with an H# chip and n):
- valid sample
- slice
- ordering intensity (`scr_orders_4wk` midpoints)
- PPI median [CI]
- `bt_trial_intent` T2B [CI]
- best CTA CTR (flagged if directional)
- median `wtp_max_fee` (ladder provisional)
- **Ownly fee: audit-observed (TBD)**
- audit win rate
- mean RSS
- % ADI ≥ 75

**Charts:**
1. Dimension bars (0–100, bootstrap CI, lines at 40 / 50 / 70; INSUFFICIENT rows labelled).
2. Weights inputs plus a sensitivity table (current + 3 pre-registered sets → total, recommendation, PROVISIONAL flag).
3. Scope × dimension heatmap (greyed if n < 60 or INSUFFICIENT).
4. Inputs table: ID, metric, value, anchors, input score, weight, n, status (OK / NOT TESTABLE + reason), source.

```
┌ DEMO DATA — REPLACE WITH REAL DATA ──────────────────────────────────────────┐
│ ◎ TARGET SELECTIVELY  [PROVISIONAL]   total 64/100 (5 of 5 scored)           │
│ Why: rule 3 … · ✕ gate D4 38 < 40 · 2 LOW badges → next experiment primary   │
├ KPIs: n · slice · orders · PPI · T2B · CTR · WTP · Ownly fee TBD · win · RSS ┤
├───────────────────────────────────────┬──────────────────────────────────────┤
│ Dimension bars (CI, 40/50/70)          │ Weights [20][20][20][25][15]         │
│ D3 ▇▇▇▇▇▇ 58  LOW (1 NOT TESTABLE)     │ Current / Equal / Behav / Price → ◎ !│
├───────────────────────────────────────┴──────────────────────────────────────┤
│ Scope × dimension heatmap: Pooled | Students | Professionals | Frequent      │
│ Inputs table: D1a … D5c · value · anchors · score · weight · n · status       │
└──────────────────────────────────────────────────────────────────────────────┘
```

### VIEW 2 — Bengaluru → Hyderabad Transfer (the Starbucks-Australia view)
**Decision question:** Which Bengaluru assumptions hold in Gachibowli once respondent mix is equalised?

**Method** (PAP `CITY_MATCHED`, `09_city_transfer.py`):
- Post-stratify Bengaluru to Hyderabad's `seg_occupation × seg_freq` cells (collapse cells with < 5 BLR respondents to occupation; cap weights at 5).
- Show the composition check first.
- Use comparable items only (`comparable_blr_hyd = yes`).
- **Verdict = non-inferiority on the weighted difference** (oriented so + favours HYD), with margins from `transfer_matrix_template.csv`:
  - TRANSFERABLE: CI lower ≥ −margin
  - NON-TRANSFERABLE: CI upper < −margin
  - NEEDS ADAPTATION: CI crosses the margin
  - UNKNOWN: n < 30 or not testable

| Row | Bengaluru assumption | Comparable metric (both cities) | Margin | H# |
|---|---|---|---|---|
| BA1 | Total-price savings trigger trial | % `beh_switch_savings_required` ≤ ₹30 (survey code) | −10pp | H2; H9.1 |
| BA2 | No hidden fees / menu parity noticed and valued | % `pain_menu_markup_belief` ≥ 4 | −10pp | H1.3; H2.2 |
| BA3 | Flat fee at Ownly's level acceptable | Fee-ladder acceptance at Ownly's fee: **UNKNOWN until audit-observed** | −10pp | H8.1 |
| BA4 | ETA gap tolerated | `exp_eta_max_dinner` (median in final; demo uses mean) | −5 min | H3; H9.3 |
| BA5 | Reliability sustains repeat | % users `own_reliability_rating` ≥ 4 | −10pp | H4; H12.1 |
| BA6 | Coverage sufficient | % ADI ≥ 75 (lower is better) | −10pp | H5; H10; H9.3 |
| BA7 | Rapido distribution drives awareness/trust | % of aware who heard via Rapido app (`own_aware_source`) | −10pp | H7; H9 |
| BA8 | Multi-homing lowers friction | `beh_multihome` | −10pp | H9.4 |
| BA9 | Support/refund doesn't cause churn | % users with an unresolved issue (`own_support_issue_resolved` ∈ {0, 3}; lower is better) | −10pp | H12.2 |
| BA10 | Trial converts to repeat | `own_repeat` among users | −10pp | H12.4; H11.3 |

**Panels:**
- Composition 100%-stacked bars (BLR raw / weighted / HYD; `n_eff`).
- Transfer table with the template's columns (assumption, BLR observed, HYD observed, Δ with CI, margin, verdict, rule applied, implication, H#).
- Dumbbell of percentage rows (BLR orange ↔ HYD blue, ±margin band).
- Tenure caveat on BA5, BA9 and BA10.

### VIEW 3 — Current Food-Delivery Behaviour
**Decision question:** How intense and habitual is delivery use, and where does friction show up in behaviour?

| # | Chart | Fields |
|---|---|---|
| 3.1 | Grouped columns: order bands by segment | `scr_orders_4wk`, `seg_occupation` |
| 3.2 | Box plot: last-order final amount | `beh_last_order_total` (sensitivity: `beh_last_total_recall` = checked) |
| 3.3 | Sorted bars + CI: primary platform (neutral colour) + multi-homing note | `beh_platform_primary`, `beh_multihome` |
| 3.4 | Heatmap: last-order meal by segment (meal is the time-of-day proxy) | `beh_last_meal` × `seg_occupation` |
| 3.5 | Sorted bars + CI: top frustrations (≤ 3) | `pain_top_frustrations` (McNemar `price_set` vs `reliability_set` in PAP) |
| 3.6 | Diverging Likert: 8-item pain grid + tile "% left without ordering after seeing the total" | `pain_*_freq`, `beh_abandon_price_freq` ≥ 2 |
| 3.7 | Bars: memberships (multi-select) | `beh_subscriptions` |
| 3.8 | Ordered bars: offer dependency | `beh_offer_dependency` (`high_offer_dependency`) |

### VIEW 4 — Switching Engine
**Decision question:** Which need → trigger → benefit → barrier chain is associated with high trial intent?

| # | Chart | Fields |
|---|---|---|
| 4.1 | Chain columns, each with its own base: Unmet need → Real past switch trigger → Expected benefit → Barrier → Intent | `pain_top_frustrations` → trigger: `own_first_trial_trigger` (Ownly users) + coded `beh_switch_reason` (non-users with `beh_switched_primary_12m` = 1) → `bt_expected_price` → `bt_concern` (coded) → `bt_trial_intent` T2B |
| 4.2 | Forest plot (log OR + CI) for `bt_trial_intent` ≥ 4 | Predictors per PAP §6: PPI, RSS, `exp_eta_max_dinner`, ADI, `dec_habit_lock`, `beh_multihome`, `beh_any_subscription`, `seg_freq`, `seg_occupation`, `meta_brand_arm` (HYD only). Not SRI (circular). EPV shown; "associational, not causal" |
| 4.3 | Diverging Likert: trial intent by primary platform | `bt_trial_intent` × `beh_platform_primary` |
| 4.4 | Ordered bars: saving needed to switch, incl. "No amount" (DK excluded), with the audit median saving noted | `beh_switch_savings_required` |

### VIEW 5 — Price × Reliability × ETA (hero)
**Decision question:** What does a rupee of savings buy in waiting time, reliability, restaurant choice and refund assurance, by segment? A low-price proposition is validated only if users trade something for it.

| # | Chart | Source |
|---|---|---|
| 5.1 | Fee-acceptance curve by segment (Wilson band); **ladder points labelled provisional; no Ownly fee marker** ("Ownly fee: audit-observed (TBD)"); median acceptable fee = interpolated 50% crossing | `fact_wtp_long` → `wtp_curve` |
| 5.2 | Arc elasticity per fee step (dumbbell by segment) | `wtp_curve` |
| 5.3 | Model-based WTP per attribute step (₹ per minute faster, per 1-in-10 fewer late orders, per coverage step, for an automatic 24-h refund), pooled + by segment, CI | `dce_wtp` (conditional logit, Krinsky-Robb). A claim is made only if β_price is significant and the segment-difference CI excludes 0 |
| 5.4 | Task-level shares choosing the cheaper alternative for each designed task (block × t1–t6, dominance task excluded), by segment. This is the PAP fallback wording | `fact_dce_long` + `dce_design_matrix.csv` |
| 5.5 | RSS distribution (0 / 50 / 100) by segment | `rss` |
| 5.6 | Median lunch vs dinner ETA tolerance by segment, with audit incumbent ETA and Ownly gap noted | `exp_eta_max_lunch`, `exp_eta_max_dinner`, `audit_summary` |
| 5.7 | Bill scenarios S1 (simple bill at identical total) · S2 (discount framing at identical total) · S3 (lower total vs usual) · S4 (lower total but slower / lower rating): share choosing the focal option, vs 50%. **Labelled SYNTHETIC research scenarios** | `fact_bill_choice_long` |

### VIEW 6 — Segments
**Decision question:** Do students and working professionals differ meaningfully, and which is the better initial target?

- **No personas.** Optional data-driven clusters only if silhouette ≥ 0.25 and each cluster has n ≥ 40; they are labelled by measured profile.
- **6.1** Medians dumbbell (PPI, SRI, RSS, ADI, T2B%).
- **6.2** H6 test-family table: Mann-Whitney + bootstrap median-difference CI (two-proportion z for T2B), effect sizes r / h, Holm-adjusted. Measures: PPI, SRI, RSS, ADI, T2B, `wtp_max_fee`, orders, `beh_last_order_total`, `exp_eta_max_dinner`.
- **6.3** PPI × RSS scatter (jittered).
- **6.4** Framework dimension scores for the student and professional scopes.

### VIEW 7 — Voice of Customer
Permanent caveat: reviews and social data support issue existence and severity, not prevalence.

- **7.1** `primary_theme` share × mean severity (1–4). The reliability/support/refund family (scorecard input D4d) is shown in ink; everything else in grey.
- **7.2** `primary_theme` × `order_stage` heatmap.
- **7.3** Theme share by `source` (google_play / apple_app_store / reddit / linkedin), as small multiples.
- **7.4** Monthly negative share with n.
- **7.5** Interview theme matrix (k of N by segment).
- **7.6** Quote wall: verbatim ≤ 25 words from `human_verified` items only, with the interpretation shown separately. The demo shows placeholders, never quotes.

### VIEW 8 — Fake-Door Experiment
Unit: `anon_visitor_id`; `is_qa` and `is_bot_suspect` excluded.

- **8.1** Funnel per variant (`A_total_price` / `B_transparent_bill` / `C_reliable_value`): page_view → vp_view → cta_click → disclosure_view → secondary_intent.
- **8.2** `cta_ctr` (primary) and `secondary_rate` with Wilson CIs (`fakedoor_summary`).
- **8.3** Power / MDE panel and winner rule ("Winner" only if p < 0.05 and the lead exceeds the MDE; otherwise DIRECTIONAL). A directional result caps the D5 badge at MEDIUM.
- **8.4** `utm_source` × variant balance table.
- **8.5** Time to CTA (`time_since_load_ms`).
- **8.6** Say-do: survey T2B vs best `cta_ctr` and vs best `secondary_rate` (= D5c), pooled only. A visitor's segment is known only after the mini-survey, so segment-level say-do needs segment-specific `utm_campaign` links.

### VIEW 9 — Market Reality: Competitor Basket Audit
Fields follow `audit_schema.csv` and `audit_calculations.md`. Neutral platform colours throughout.

- **9.1** Dumbbell per restaurant × basket: Ownly `final_payable` (filled ink) vs cheapest comparator (grey ring); `gap_rs` = Ownly − comparator.
- **9.2** Median fee stack (`packaging_fee`, `platform_fee`, `delivery_fee`, `small_cart_fee`, `surge_rain_fee`, `taxes_gst`; `discount_amount` left of zero) by platform, plus the gap decomposition.
- **9.3** `gap_rs` distribution with median and cluster-bootstrap CI; win rate (tie ≤ ₹5); saving % of basket.
- **9.4** Ownly win rate by `slot` × `drop_point_id`.
- **9.5** `eta_gap_min` (from `eta_mid_shown`) by slot.
- **9.6** Listing coverage (`listed_y / frame_n`) and availability (listed AND open) by `price_tier`, as small multiples per platform.
- **9.7** Offline-verified premium, shown only where `offline_subtotal_verified` is present.
- The observed Ownly `delivery_fee` is shown as captured and is never assumed.

### VIEW 10 — Recommendation
**Cards follow the framework §4 conclusion template:**
- recommendation
- strongest opportunity
- strongest risk
- best initial segment
- primary switching trigger
- non-negotiable guardrail
- expected pricing/value condition
- what not to compete on
- evidence still missing
- next experiment
- weight sensitivity

Each card has an answer field (blank until analysed), evidence IDs, a confidence badge and contradicting evidence. A **triangulation strip** (insight × evidence type, supports ■ / contradicts ✕ / absent □) applies the §5 confidence rules.

---

## 5. Calculated metrics (single definitions)

| Metric | Definition (source) |
|---|---|
| `ppi` | ((mean of `pain_fee_reconsider_freq`, `pain_bill_unreasonable_freq`, `pain_menu_markup_belief`, `beh_abandon_price_freq`) − 1)/4 × 100; needs ≥ 3 of 4 items; composite used only if α ≥ 0.60 (PAP §4) |
| `sri` | mean(r(`bt_trial_intent`), r(`multihome5`), r(6 − `dec_habit_lock`)), where r(x) = (x−1)/4×100; all 3 required; uses first-exposure intent, with arm as a control (PAP §4) |
| `rss` | % of `price_vs_reliability` tasks where the more reliable, more expensive alternative was chosen; ≥ 2 tasks |
| `adi` | (`exp_fav_restaurant_needed` − 1)/4 × 100 |
| `wtp_max_fee` | Highest accepted ladder fee given monotone answers; NA if non-monotone (dashboard flag `wtp_nonmonotone`) |
| Median acceptable fee | Linear interpolation at the 50% acceptance crossing, bootstrap CI (PAP §6) |
| Model WTP | −β_k / β_price, Krinsky-Robb 95% CI; "not identifiable" if β_price is not significant |
| `own_repeat` / `own_lapsed` | `own_orders_4wk` ≥ 2 / = 0 |
| `own_status` (dashboard-derived) | `user_repeat` (`own_tried` = 2 and `own_repeat`) · `user_not_repeat` · `aware_never_tried` (`own_aware_any`) · `unaware` |
| Wilson CI | centre = (p̂ + z²/2n)/(1 + z²/n); half = z·√(p̂(1−p̂)/n + z²/4n²)/(1 + z²/n) |
| Arc elasticity | ((A₂−A₁)/mean(A)) / ((F₂−F₁)/mean(F)), skipping F = 0 |
| Audit `gap_rs`, `eta_gap_min`, `winner`, coverage | As in `audit_calculations.md` (Ownly − comparator; tie ≤ ₹5; listed_y / frame_n) |
| `n_eff` | (Σw)² / Σw² |
| Dimension scores / badges / decision / overlay | Framework §1–§3, exactly (View 1) |

---

## 6. Reconciliation log

### Resolved (2026-09-14, lead reconciliation request)
| # | Item | Resolution |
|---|---|---|
| R1 | Assumed survey names | Replaced with `survey_variable_dictionary.csv` names everywhere (schema CSVs regenerated from the dictionary; 168 respondent columns; prototype generator rebuilt on them). Key renames: `scr_locality` → `scr_area`; `beh_last_order_total_inr` → `beh_last_order_total`; `beh_subscription` → `beh_subscriptions` (+ `beh_any_subscription`); `beh_abandon_freq`/`beh_abandon_reason` → pain grid `beh_abandon_price_freq`; `dec_switch_threshold_inr` → `beh_switch_savings_required`; `exp_eta_max_min` → `exp_eta_max_lunch`/`dinner`; `meta_channel` → `meta_found_survey`/`meta_source`; `wtp_fee_<x>`/`wtp_max_fee_inr` → `wtp_accept_<x>`/`wtp_max_fee`; `dce_t<k>` (now t1–t6 + dom from the real design); `bill_s<k>` → `bill_s1…s4`; `churn_reason_coded` → `churn_reduced_reasons`; `own_discovery_source` → `own_aware_source`; brand arm values → blind/branded; `br_*` blind arms only; added `bt_framing_pref`, `beh_offer_dependency`, `exp_restaurant_types_needed`, `dem_rapido_ride_use`/`_experience` |
| R2 | Scorecard formulas | The proposed formulas were removed. Framework §1–§3 is now implemented exactly (anchors, NOT TESTABLE, INSUFFICIENT EVIDENCE, badge drop, D5 badge in SCALE, frequent-users scope, RETHINK pooled + both segments, PROVISIONAL overlay, 3 alternative weight sets). PAP path corrected to `09_analysis/M_pre_analysis_plan.md` |
| R3 | ₹30 Ownly fee | All fee constants and markers removed. The text is "Ownly fee: audit-observed (TBD)". D3c and BA3 are NOT TESTABLE / UNKNOWN until the audit confirms the fee. Ladder points are labelled provisional |
| R4 | Competitor brand colours | Removed. Neutral palette with labels and small multiples |
| R5 | Table / output names | Aligned to PAP §12: `dce_coefficients`, `dce_wtp`, `wtp_curve`, `transfer_metrics`, `audit_summary`, `hypothesis_results → dim_hypothesis`, `fakedoor_summary`. The earlier `fact_model_dce`/`fact_model_coefs` were dropped. `fact_evidence_matrix` and `transfer_metrics` headers are copied verbatim from the 11_insights templates. Audit, review and fake-door fields are aligned to their source files |

### Open (for the lead)
| # | Item |
|---|---|
| O1 | **Table-name diffs vs Agent G's `09_analysis` scripts.** The dashboard schema keeps its own names; the lead decides which set wins. **Same name in both:** `fact_survey_respondent`, `fact_wtp_long`, `wtp_curve`, `transfer_metrics`, `fact_audit_obs`, `fact_audit_pairs`, `audit_summary`, `fact_reviews`, `agg_fakedoor_variant`, `fact_scorecard`. **Named differently:** dashboard `dce_coefficients` + `dce_wtp` ↔ G `fact_model_dce` (+ `dce_hypothesis_inputs`). **G only (not yet in the dashboard schema):** `dce_task_shares` (= View 5 task chart), `dce_long_full`, `survey_respondent_full`, `composition_check` (= View 2 composition panel), `audit_coverage` (= View 9 coverage), `review_summary_metrics` + `review_theme_summary` (= View 7 and D4d), `wtp_summary`, `wtp_elasticity`, `wtp_model_coefs`, `decision` (= View 1 verdict + sensitivity). **Dashboard only:** `fakedoor_summary` (the `analyze_fakedoor.py` output), `dim_chart`, `bridge_insight_hypothesis`. Recommendation: adopt G's names for these outputs and point the listed views at them; headers to be copied from G's outputs once run. |
| O8 | **Dictionary changes applied (2026-09-14, second pass):** `beh_last_daytype`, `beh_last_location` and `own_nps` removed (View 3.4 is now `beh_last_meal` × segment; `beh_weekday_weekend` is HYD-only). Choice tasks are Hyderabad-only, so every DCE chart, RSS and the scorecard's RSS-based inputs use HYD rows only, and View 2 has no DCE rows (BA1–BA10 are all non-DCE). `bill_s1`/`bill_s2` now run in both cities and include code 3 "No real difference", shown as its own row next to the focal-option share; `bill_s3`/`bill_s4` stay HYD-only. |
| O2 | Dashboard-derived fields not in the dictionary: `own_status`, `wtp_nonmonotone`, `bt_concern_coded`, `beh_switch_reason_coded`, `pain_unaided_coded`, `w_match_hyd`, `theme_family`. Confirm, or name them in the master dictionary. |
| O3 | Badge operationalisation (the base level from scope n and source-type count; D5 capped while the fake door is directional) and MIN_N = 30 for NOT TESTABLE are my reading of framework §1/§5. The framework doesn't give a numeric minimum. |
| O4 | RETHINK "in both segments" when a segment has n < 60: the demo treats unscorable segments as not blocking the pooled gate. Confirm. |
| O5 | D4d "reliability/support/refund themes" needs an agreed `primary_theme` → family map across the app-store and social codebooks (the codes differ, e.g. `LATE_DELIVERY_ETA_BREACH` vs `LATE_DELIVERY`). |
| O6 | Dictionary R1–R3 say `br_*` is shown to blind arms only, but `randomization_and_versions.md` step 3 says V3/V4 keep the post-reveal questions. The dashboard follows the dictionary and coordinator (blind only). Agent C should fix the doc. |
| O7 | `agg_fakedoor_variant` (PAP name) vs `fakedoor_summary.csv` (script output): both are kept, with the pivot defined in `dataset_schema.md` §10. |
