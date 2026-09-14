# Analysis-Mart Dataset Schema (feeds the dashboard)

**Owner:** Agent F · **Drafted:** 2026-09-14 · **Revised:** 2026-09-14, aligned to the final lead specs.

Header-only CSVs live in `schema/` and are generated from the canonical sources, so every column name matches exactly.

**Canonical sources (authoritative over this file where they disagree):**

| Topic | File |
|---|---|
| Survey variables | `03_hyderabad_survey/survey_variable_dictionary.csv` (`fact_survey_respondent` has one column per `variable_name`, plus the dictionary's `derived_formula` outputs) |
| Choice design | `03_hyderabad_survey/dce_design_matrix.csv` |
| Audit | `06_competitor_audit/audit_schema.csv`, `audit_data_dictionary.md`, `audit_calculations.md` |
| Reviews / social | `05_review_mining/app_stores/reviews_coded.csv`, `05_review_mining/social/social_coded.csv` |
| Fake door | `07_fake_door/events_schema.json`, `07_fake_door/analyze_fakedoor.py` |
| Derived metrics and scorecard | `09_analysis/M_pre_analysis_plan.md` §4 and §12; `11_insights/decision_framework_and_scorecard.md` §1–§3 |
| Evidence and transfer matrices | `11_insights/insight_evidence_matrix_template.csv`, `11_insights/transfer_matrix_template.csv` (headers copied verbatim) |

**Pipeline:** script names follow the PAP §12 code plan.

| Step | Script | Produces |
|---|---|---|
| P0 | `00_manifest_and_hash.py` | `08_clean_data/raw/MANIFEST.csv` |
| P1 | `01_ingest_and_harmonise.py` → `02_quality_flags.py` → `03_split_clean_excluded.py` | `08_clean_data/cleaned/`, `excluded/` (with `exclusion_reason`), `flags.csv` |
| P2 | `04_derive_metrics.py` | `fact_survey_respondent`, `fact_dce_long`, `fact_wtp_long`, `fact_bill_choice_long` |
| P3 | `06_hypothesis_tests.py` | `outputs/hypothesis_results.csv` → `dim_hypothesis` |
| P4 | `07_dce_models.py` | `outputs/dce_coefficients.csv`, `outputs/dce_wtp.csv` |
| P5 | `08_wtp_curves.py` | `outputs/wtp_curve.csv` |
| P6 | `09_city_transfer.py` | `outputs/transfer_metrics.csv` |
| P7 | `10_audit_analysis.py` | `fact_audit_obs` (from `06_competitor_audit/data/audit_obs.csv`), `fact_audit_pairs`, `outputs/audit_summary.csv` |
| P8 | `11_reviews_merge.py` | `fact_reviews` |
| P9 | `12_fakedoor.py` / `analyze_fakedoor.py` | `fakedoor_summary`, `agg_fakedoor_variant` |
| P10 | `13_scorecard.py` | `fact_scorecard` (all scopes × weight sets) |
| P11 | human synthesis | `fact_interview_segments`, `fact_evidence_matrix`, `bridge_insight_hypothesis`, `dim_chart` |

**Conventions:**
- snake_case names.
- `city` ∈ {`hyderabad`, `bengaluru`}.
- **Enum codes are stored decoded** as snake_case labels (e.g. `scr_orders_4wk` keeps its numeric code 1–4 because it is ordinal, but `beh_platform_primary` = `swiggy`). Code ↔ label maps come from `values_codes` in the dictionary.
- Multi-select (`checkboxes`) variables are stored twice: a pipe-list column under the variable name, and one 0/1 column per option, named `<variable>__<option>`, as the dictionary specifies.
- "Don't know" codes (98) become empty, with a separate flag where the dictionary asks for one.
- Money in whole ₹. Timestamps in IST ISO-8601.
- Every table carries `data_status` ∈ {`real`, `demo`}. The dashboard never mixes the two in one chart.

---

## 1. `fact_survey_respondent` (168 columns; see `schema/fact_survey_respondent.csv`)

**Grain:** one row per cleaned, valid respondent, both cities. **Key:** `resp_id`.

| Column group | Canonical columns (from the dictionary) |
|---|---|
| Meta / QC | `meta_form_version`, `meta_brand_arm` (blind / branded; HYD only), `meta_dce_block` (1/2), `meta_session_token`, `meta_start_ts`, `meta_source` (utm_source), `meta_submit_ts`, `meta_duration_sec`, `meta_consent`, `meta_found_survey`, `meta_comments`, `att_check_1` |
| Screener | `scr_age_band`, `scr_area`, `scr_orders_4wk` (1=1–3, 2=4–7, 3=8–15, 4=16+), `scr_coi`, `scr_repeat` |
| Segments | `seg_occupation_raw` → **`seg_occupation`** (1,2 = student · 3 = working_professional · 4 = working_student · 5 = other); **`seg_freq`** (from `scr_orders_4wk`: 1 = occasional · 2 = regular · 3/4 = frequent) |
| Demographics | `dem_institution` (→ `FLAG_iiith`), `dem_work_sector`, `dem_living`, `dem_delivery_spend_month`, `dem_gender`, `dem_rapido_ride_use`, `dem_rapido_ride_experience` (→ `rapido_exp_group`) |
| Last order | `beh_unaided_apps` (→ `own_aware_unaided`), `beh_last_order_when`, `beh_last_platform`, `beh_last_meal` (1 breakfast … 5 late night; also the time-of-day proxy that replaces the former `beh_last_time`), `beh_last_people`, `beh_last_food`, `beh_last_restaurant_type`, `beh_last_order_total`, `beh_last_total_recall`, `beh_last_discount`, `beh_last_fees_noticed`, `dec_last_reasons` |
| Habits | `beh_weekday_weekend`, `beh_meal_occasions`, **`beh_platforms_used_4wk`** (→ `beh_platform_count`, `beh_multihome`, `multihome5`), **`beh_platform_primary`**, **`beh_subscriptions`** (→ `beh_any_subscription`), **`beh_offer_dependency`** (→ `high_offer_dependency`), **`dec_habit_lock`**, `beh_compare_freq`, `beh_switched_primary_12m`, `beh_switch_reason` |
| Pain | `pain_unaided_frustration`; grid: **`pain_fee_reconsider_freq`, `pain_bill_unreasonable_freq`, `beh_abandon_price_freq`, `pain_late_freq`, `pain_cancel_freq`, `pain_wrong_item_freq`, `pain_restaurant_unavailable_freq`, `pain_quality_freq`**; `pain_menu_markup_belief`; **`pain_top_frustrations`** (→ `price_set`, `reliability_set`); `pain_incidents_3m` (→ `pain_incident_any_3m`); `pain_refund_outcome` |
| Expectations | **`exp_eta_max_lunch`, `exp_eta_max_dinner`**, `exp_late_tolerance`, **`exp_fav_restaurant_needed`**, **`exp_restaurant_types_needed`**, `exp_refund_expectation`, `exp_instructions_importance`, `exp_quality_concern_cheap`, **`beh_switch_savings_required`** (→ `switch_price_never`) |
| Experiments | `bill_s1`…`bill_s4`; `dce_t1`…`dce_t6`, `dce_dom` (→ `FLAG_dominance_fail`); `wtp_start`, **`wtp_accept_0`…`wtp_accept_60`** (→ **`wtp_max_fee`**, empty if non-monotone) |
| Concept (first exposure, both arms) | **`bt_appeal`, `bt_trial_intent`, `bt_trust`, `bt_expected_reliability`, `bt_expected_price`, `bt_concern`, `bt_framing_pref`** (→ `bt_t2b`, `bt_top_box`) |
| Brand reveal (blind arms only) | **`br_trial_intent`, `br_trust`, `br_expected_reliability`**; `br_rapido_effect`, `br_rapido_effect_why` (all HYD) |
| Ownly awareness / use | `own_aware_aided`, `own_aware_duration` (→ `aware_2wk_plus`), `own_aware_source`, `own_tried` (→ `own_tried_bin`), `own_not_tried_reason`, `own_trust`, `own_first_order_month` (→ `tenure_band`), `own_first_trial_trigger` (→ `offer_trigger`), `own_choose_reasons`, **`own_orders_4wk`** (→ `own_repeat` = ≥ 2, `own_lapsed` = 0), `own_share_of_orders`, `own_last_total`, `own_perceived_savings`, `own_known_savings`, `own_reliability_rating` (→ `on_time_most`), `own_found_restaurants`, `own_order_accuracy`, `own_eta_vs_other`, `own_issues_3m`, `own_support_issue_resolved` (→ `unresolved`), **`churn_reduced_reasons`**, `own_competitor_when`, `own_continue_intent` |
| Derived indices (PAP §4) | `ppi`, `sri`, `rss`, `adi` |
| **Dashboard-derived (proposed, not in the dictionary)** | `own_status` (user_repeat / user_not_repeat / aware_never_tried / unaware, from `own_tried` + `own_repeat` + `own_aware_any`); `wtp_nonmonotone` (flag behind `wtp_max_fee` = NA); `bt_concern_coded` (from `bt_concern`: "coded open text — requires human coding"), `beh_switch_reason_coded` and `pain_unaided_coded` (same label); `w_match_hyd` (post-stratification weight for CITY_MATCHED); `exclusion_flags` |

> **Second-pass dictionary changes:**
> - `beh_last_daytype`, `beh_last_location` and `own_nps` were removed.
> - `beh_weekday_weekend` is HYD-only.
> - `bill_s1`/`bill_s2` are asked in both cities with codes 1 = Bill 1, 2 = Bill 2 and 3 = "No real difference". `fact_bill_choice_long.chose_focal_option` is empty for code 3, and a `no_difference` flag is added.
> - `dce_*` columns and `rss` are Hyderabad-only (empty for Bengaluru).
>
> Table-name differences with Agent G's `09_analysis` scripts are listed in `dashboard_blueprint.md` §6 O1.
>
> **Lead mapping for former dashboard fields with no survey item:**
> - `beh_last_time` → use `beh_last_meal`.
> - `beh_abandon_freq` → `beh_abandon_price_freq`.
> - `beh_abandon_reason` → dropped.
> - `dec_trial_trigger_coded` → `own_first_trial_trigger` (Ownly users) + coded `beh_switch_reason` (non-users who switched).
> - `bt_concern_coded` → kept as a human-coded derived field.
>
> None of the removed names appear in the schema CSVs or the prototype.

## 2. `fact_dce_long` (Hyderabad only)
**Grain:** respondent × task × alternative. **Key:** (`resp_id`, `task`, `alt`).
Columns: `resp_id, city, data_status, seg_occupation, seg_freq, meta_brand_arm, meta_dce_block, task (t1…t6, dom), position, purpose_tag (price_vs_eta / price_vs_reliability / price_vs_assortment / price_vs_refund / multi / dominance_check), alt (A/B), price, eta_min, late_in_10, restaurants (few/some/most), refund (auto_24h/case_by_case), chosen, FLAG_dominance_fail`. Attribute columns and levels are joined from `dce_design_matrix.csv` by (`meta_dce_block`, `task`, `alt`).

## 3. `fact_wtp_long`
**Grain:** respondent × fee point. **Key:** (`resp_id`, `fee`).
Columns: `resp_id, city, data_status, seg_occupation, seg_freq, beh_any_subscription, wtp_start (20/40), fee (0…60, PROVISIONAL points), asked, accept, accept_implied (by monotone ladder), wtp_max_fee`.

## 4. `fact_bill_choice_long`
**Grain:** respondent × scenario. **Key:** (`resp_id`, `scenario`).
Columns: `…, scenario (bill_s1…bill_s4), option_order (per version), choice_code, chose_focal_option, focal_option_label (simple bill / discount-framed bill / lower total), is_synthetic_scenario (TRUE)`.

## 5. Model outputs (PAP §12 file names)
- `dce_coefficients`: `model, segment, term, estimate, std_error, ci_low, ci_high, p_value, n_resp, n_obs, log_likelihood, pseudo_r2, run_ts, code_ref, data_status`.
- `dce_wtp`: `model, segment, attribute, unit, wtp_inr, ci_low, ci_high, ci_method (krinsky_robb_5000), price_coef_significant, identifiable, data_status`.
- `wtp_curve`: `segment, fee, accept_share, ci_low, ci_high, n, median_acceptable_fee, median_fee_ci_low, median_fee_ci_high, arc_elasticity_to_next, ladder_status (provisional/final), data_status`.
- `transfer_metrics`: header copied from `11_insights/transfer_matrix_template.csv` (`row_id` BA1…BA10, `non_inferiority_margin`, `verdict_TRANSFERABLE_NEEDS_ADAPTATION_NON_TRANSFERABLE_UNKNOWN`, …).
- `dim_hypothesis` ← `outputs/hypothesis_results.csv`: `hyp_id, family, statement, …, status, result_summary, effect_size, ci, n, evidence_ids, …`.

## 6. `fact_reviews` (harmonised union of app-store and social coded files)
**Grain:** coded item. **Key:** `item_id`.

| Mart column | App-store source column | Social source column |
|---|---|---|
| item_id | review_id | item_id |
| source | platform_source | platform |
| community / item_kind | — | community / item_kind |
| app_context | app_context | — |
| url | source_url | url |
| item_date | review_date | post_date |
| access_date | retrieved_at | access_date |
| star_rating | star_rating | — |
| author_type | — | author_type |
| city_mentioned, sentiment, themes, primary_theme, severity (1–4), order_stage, switching_trigger_flag, churn_signal, repeat_use_signal, price_value_comment, delivery_eta_comment, assortment_comment, support_comment, trust_safety_quality_comment, coder, human_verified | same names | same names |
| quote_excerpt (≤ 25 words, verbatim) | from review_text | from text_excerpt |
| evidence_label | — (CONSUMER-GENERATED) | evidence_label |
| hypotheses_linked | — | hypotheses_linked |
| **theme_family** (dashboard-derived) | mapping of `primary_theme` → `reliability_support_refund` / `price_value` / `assortment_coverage` / `quality_accuracy` / `app_payment` / `business_commentary`; feeds scorecard input D4d | same |

Rows with `human_verified` ≠ TRUE are not displayed.

## 7. `fact_interview_segments`
**Grain:** coded excerpt. Columns as in the schema CSV. `layer` ∈ OBSERVATION / USER_QUOTE / INTERPRETATION / INSIGHT / OPPORTUNITY. USER_QUOTE rows must be verbatim.

## 8. `fact_audit_obs`
**Grain:** one audit row (platform × restaurant × basket × drop point × account state × capture moment). **Key:** `audit_id`.

Columns: all 39 `audit_schema.csv` columns (`audit_id … notes`) plus derived columns from `audit_calculations.md`:
- `price_tier` (joined from the restaurant frame)
- `capture_date`
- `eta_mid_shown`
- `fee_stack`
- `arithmetic_flag`
- `valid_row`
- `valid_for_pairwise` (listed = y AND open = y AND `item_match_quality` ∈ {exact, close} AND `arithmetic_flag` = 0 AND timing gap ≤ 10 min)
- `match_key`

Enum values:
- `slot` ∈ lunch_peak / off_peak / dinner_peak / weekend_dinner / late_night
- `drop_point_id` ∈ DP1_CAMPUS / DP2_OFFICE / DP3_RESIDENTIAL
- `platform` ∈ ownly / ownly_in_rapido / swiggy / zomato / magicpin / other_*

## 9. `fact_audit_pairs`
**Grain:** match_key × comparator. **Key:** (`match_key`, `comparator`).

Columns: `match_key, restaurant_id, price_tier, basket_id, drop_point_id, slot, capture_date, account_state, subscription_active, comparator (swiggy / zomato / cheapest), ownly_total, c_total, gap_rs, gap_pct, dt_min, eta_gap_min, menu_gap_rs, fee_gap_rs, tax_gap, discount_gap, winner, data_status`.

Sign convention (from `audit_calculations.md`): **`gap_rs` = Ownly − comparator**, so a negative value means Ownly is cheaper. `winner` uses a ₹5 tie tolerance across the platforms captured for the key.

`audit_summary`: `scope, slot, drop_point_id, price_tier, comparator, metric (win_rate / median_gap_rs / gap_pct_of_basket / listing_coverage / availability_coverage / median_eta_gap), value, ci_low, ci_high, n_keys, n_restaurants, data_status`.

The dashboard never displays an Ownly delivery-fee constant. The fee is **audit-observed (TBD)**.

## 10. Fake door
- `fact_fakedoor_events`: flattened `events_schema.json`. Columns: `received_at, experiment_id, page_version, variant_id, variant_key (A_total_price / B_transparent_bill / C_reliable_value), anon_visitor_id (unit of analysis), anon_session_id, event_name (page_view / vp_view / scroll_50 / cta_click / disclosure_view / secondary_intent / secondary_skip / mini_survey_submit / mini_survey_skip / survey_link_click / exit), ts, time_since_load_ms, utm_*, referrer_domain, device_type, is_qa, is_bot_suspect, payload_json`.
- `fakedoor_summary`: exactly what `analyze_fakedoor.py` writes. Columns: `scope, group, variant, metric (vp_view_rate / cta_ctr [primary] / secondary_rate / bounce_rate / secondary_given_cta …), x, n, rate, ci_low, ci_high`. `fakedoor_pairwise` and `fakedoor_exclusions` are kept as written by the script.
- `agg_fakedoor_variant` (PAP name): a wide pivot of `fakedoor_summary` where scope = overall, plus `mde_at_80_power` and `directional_only`.

## 11. `fact_scorecard` (framework §1–§3)
**Grain:** scope × weight_set × dimension × input. **Key:** (`scope`, `weight_set`, `dimension`, `input_id`).

Columns: `scope (pooled_hyd / student / working_professional / frequent), n_scope, n_users (HYD + BLR Ownly users used by D4c and D5b), weight_set (default / equal / behaviour_first / price_thesis / custom), dimension (D1…D5), input_id (D1a…D5c), input_label, input_value, input_n, weak_anchor, strong_anchor (empty for the formula inputs D4a/D4b), input_score, input_weight, testable, not_testable_reason, source_types, dimension_score (empty if INSUFFICIENT EVIDENCE), dimension_ci_low, dimension_ci_high, evidence_badge (HIGH / MEDIUM / LOW / INSUFFICIENT EVIDENCE), missing_inputs, dimension_weight, weighted_total, dimensions_scored, recommendation (SCALE / TARGET SELECTIVELY / ADAPT / RETHINK PROPOSITION), rule_applied, provisional, data_status`.

## 12. Evidence
- `fact_evidence_matrix`: header copied verbatim from `11_insights/insight_evidence_matrix_template.csv`.
- `bridge_insight_hypothesis` (`insight_id`, `hyp_id`).
- `dim_chart` (title control).

## Relationships
- `fact_survey_respondent.resp_id` 1—* `fact_dce_long`, `fact_wtp_long`, `fact_bill_choice_long`.
- `fact_audit_obs.match_key` *—* `fact_audit_pairs.match_key`.
- `fact_fakedoor_events.variant_id` *—1 `agg_fakedoor_variant`.
- `dim_hypothesis.hyp_id` 1—* `bridge_insight_hypothesis` *—1 `fact_evidence_matrix`.
- Shared lookup dimensions for slicers: `dim_city`, `dim_segment` (`seg_occupation` × `seg_freq`).

---

## Lead decision (2026-09-14): pipeline table names are authoritative

The analysis pipeline (`09_analysis/`, steps 00–13) produces the tables. Where dashboard names differ, **use the pipeline name** and read this schema's table as an alias:

| Dashboard schema name (alias) | Pipeline output (authoritative) |
|---|---|
| `dce_coefficients`, `dce_wtp` | `fact_model_dce` (+ `dce_task_shares`) |
| — (new in pipeline) | `composition_check` → View 2 composition panel |
| — | `audit_coverage` → View 9 coverage chart |
| — | `review_summary_metrics`, `review_theme_summary` → View 7 |
| `wtp_curve` | `wtp_curve` (+ `wtp_summary`, `wtp_elasticity`) → View 5 |
| — | `decision` → View 1 / View 10 recommendation card |

When the Looker Studio build starts, connect to the pipeline outputs directly. Any field mismatch goes into `09_analysis/README.md`, not into manual renames.
