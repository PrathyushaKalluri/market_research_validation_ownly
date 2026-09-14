# Hyderabad Survey — Bias Audit

**Scope:** every respondent-facing item in `survey_variable_dictionary.csv`, as built in `hyderabad_google_form_part1/1b/2/2b.md`.

**Risks checked:**
- L = leading
- DB = double-barrelled
- PO = priming / order effect
- US = unbalanced scale
- RB = recall burden
- SD = social desirability
- J = jargon
- AQ = acquiescence (agree-statement)
- HY = hypothetical

## 1. Item audit

| q_no / variable | Risk(s) checked | Verdict | Fix applied / mitigation |
|---|---|---|---|
| Q1 `meta_consent` | DB (consent + age 18+) | Acceptable | Standard ethics combination; both are required to continue |
| Q2–Q6 screener | L, PO | OK | No mention of Ownly, price or fees in the screener; COI item combines two disqualifiers with the same action (accepted DB exception) |
| Q7 `seg_occupation_raw` | DB | OK | "Studying and working" is a single state, not two questions |
| Q11 `dem_delivery_spend_month` | SD, RB | Minor risk | Bands + "Prefer not to say"; used only descriptively / as a control |
| Q13 `beh_unaided_apps` | PO | **Critical placement** | First item of S3, before any app list; open text; coded by 2 people |
| Q14–Q24 last order | RB | Moderate RB | Anchored on the *most recent* order; prompt to check order history; Q23 records recall certainty for sensitivity |
| Q15, Q29, Q30 app lists incl. "Ownly app" / "Rapido app (food section)" | PO (brand name seen before the blind concept) | **Accepted risk** | Needed to measure real behaviour. Mitigations: unaided awareness (Q13) is captured first; the list shows only names, never the proposition; the H7 primary analysis uses the unaware subgroup; the arm comparison is randomised, so exposure is equal across arms |
| Q22 `beh_last_order_total` | RB | Moderate | Numeric validation; "approximate is fine"; Q23 certainty |
| Q26 `dec_last_reasons` | Post-hoc rationalisation | Accepted | Tied to a specific order; options shuffled; max 3 |
| Q32 `beh_offer_dependency` | RB | Moderate | "Last 10 orders" framing + "Don't know" |
| Q33 `dec_habit_lock` | AQ | Minor | Single agree-statement retained for SRI comparability; reverse-scored in SRI; interpreted alongside the behavioural Q34 |
| Q35–Q36 switching | RB, SD | OK | Past behaviour; the open follow-up is optional |
| Q37 `pain_unaided_frustration` | PO | OK | Placed before the grid so the prompted list doesn't shape the answer |
| Q38 grid | L (fee wording), US | OK | Frequency of *incidents*, not agreement; balanced by 5 non-price rows (late, cancel, wrong, unavailable, quality) so price is not singled out; 5-point frequency scale; row shuffle ON; attention check embedded |
| Q38.6 attention check | — | OK | Instructed response |
| Q39 `pain_menu_markup_belief` | AQ, L | Moderate | One-directional statement kept (PPI definition). Balanced agree/disagree scale + "Don't know". Reported as **belief**, validated against the audit |
| Q40 `pain_top_frustrations` | L, PO | OK | 4 price, 4 reliability/service, 4 other options; shuffled; "nothing frustrates me" allowed |
| Q41 option "a refund took >3 days or was refused" | DB | Accepted | Both are the same failure class (refund failure); not analysed separately |
| Q42 `pain_refund_outcome` | Branching limit | **Changed** | Skip logic could not be built (checkbox source). Now always shown, with the added option "I haven't asked for a refund in the last 3 months" (code 0). Dictionary updated |
| Q43–Q44 ETA maximums | HY | Accepted | Anchored to specific occasions; used alongside the choice tasks, not alone |
| Q45 `exp_late_tolerance` | HY | Accepted | "Lateness alone wouldn't make me stop" option avoids forcing |
| Q46 `exp_fav_restaurant_needed` | HY, L | OK | Neutral 5-step count scale that includes "None — I'd happily try new places" |
| Q50 `exp_quality_concern_cheap` | AQ, L | Moderate | One-sided statement; exploratory only (no ★ hypothesis); a cut candidate if the survey is too long |
| Q51 `beh_switch_savings_required` | HY, anchoring on ₹ steps | Moderate | Explicit "No amount" and "Don't know" codes (fixes v1). Treated as a stated threshold compared with audit reality, not as behaviour |
| Q52–Q55 bill scenarios | PO (position), L | OK | Every scenario labelled hypothetical; left/right order counterbalanced by version; "No real difference" option on the equal-total scenarios; no brand; all amounts include taxes |
| Q56–Q62 choice tasks | PO, cognitive load | OK | Unbranded App A/B; fixed attribute order; warm-up explanation; dominance check at position 4; blocks by version |
| S9 concept text | L (benefit-only framing) | OK | States one limitation ("delivery time and number of restaurants vary by area"); no ₹ or savings %; identical to the interview card; brand/no-brand is the only difference between arms |
| Q63–Q67 concept reactions | L, SD (politeness) | OK | Balanced 5-point scales; "No idea / Don't know" where expectation may be absent; intent analysed top-box and calibrated against behaviour (H11) |
| Q69 `bt_framing_pref` | PO (comes after the concept) | Accepted | Same exposure for all arms; comparison is relative, against the fake door |
| Q70 fee ladder | Anchoring | OK | Randomised start (₹20/₹40) by version; stop at the first change; "this service" wording in all arms |
| S11a reveal + Q71–Q73 | Demand effect (repeated items) | Accepted | Blind arms only; secondary to the between-arm test (H7.1) |
| Q74 `br_rapido_effect` | L (direct attribution), SD | Moderate | Balanced 5-point scale with "No difference" in the middle; secondary evidence only |
| Q76–Q77 Rapido ride use/experience | PO | **Placement** | Asked only after the brand reveal, so the concept test isn't primed by Rapido |
| Q78 `own_aware_aided` | PO | OK | Asked only after the reveal; unaided awareness already captured in Q13 |
| Q85 `own_first_trial_trigger` | Forced single cause | Accepted | Single choice keeps trigger frequencies interpretable; "Other" available |
| Q91 `own_perceived_savings` | L | OK | Balanced scale from "Much more expensive" to "Much cheaper" + "I didn't compare" |
| Q93–Q95 frequency ratings | US | Minor | "Rarely / Sometimes / About half the time / Mostly / Always" is ordinal but not symmetric. Kept per the dictionary; analysed with rank-based tests |
| Q98 `own_support_issue_resolved` | Branching limit | **Changed** | Always shown, with the added option "I haven't had an Ownly issue that needed a refund or support in the last 3 months" (code 9). Dictionary updated |
| Q101 `own_continue_intent` | SD | Accepted | Secondary outcome; repeat behaviour (`own_orders_4wk`) is primary |

**Wording changes to the dictionary:** none to question stems. Changes made:
- added "not applicable" options to Q42 and Q98, with their skip logic updated
- added `meta_campaign`
- aligned `bill_s1`–`bill_s4` codes to C2's scenarios (code 3 = "No real difference" on s1 and s2)

## 2. v1 items (root `14_ownly_research_design.md`, Survey B) removed or changed

| v1 item | Problem | v2 treatment |
|---|---|---|
| H-S1 "ordered in last 4 weeks? Yes/No" | Binary loses frequency; no segmentation | Q4 `scr_orders_4wk` with frequency bands (0 screens out) → `seg_freq` |
| H-S2 age bands (Under 22 / 22–28 / 29–35 …) | Did not match the 20–30 target; no screen-out | Q2 bands aligned to 20–30, with screen-out |
| H-S3 occupation (incl. homemaker, self-employed) | Not aligned to target segments; no working-student category | Q7 with student UG/PG, working, studying + working, other |
| H-S4 open-text area | Uncodeable; no eligibility control | Q3 fixed Gachibowli-area list with screen-out |
| H-S5 orders per typical week | Vague "typical" recall; overlaps H-S1 | Replaced by last-4-weeks count (Q4) |
| H-S6 single open text (what / which app / occasion) | Triple-barrelled; hard to code | Split into Q14–Q21 structured items |
| H-S7 total bill incl. fees | OK in concept but no recall-quality control | Q22 + Q23 certainty + order-history prompt |
| H-S8 platform used most (Swiggy/Zomato/direct/other) | Missing Ownly, Rapido food, Toing, Magicpin | Q29/Q30 expanded lists |
| H-S9 open "why that platform" | Uncodeable at scale | Q26 structured reasons (max 3, shuffled) |
| H-S10 multi-app use (regularly/occasionally/no) | Attitudinal frequency | Q29 actual apps used in 4 weeks → `beh_multihome` |
| H-S11 "frustrates you most, choose up to 2" | Only 2 picks; price-heavy list; no reliability/assortment balance | Q40 up to 3 with balanced price/reliability/other options + Q38 incident-frequency grid + unaided Q37 |
| H-S12 "have you noticed menu prices are sometimes higher?" | Leading (presupposes it happens) | Q39 neutral agree/disagree belief + "Don't know"; audit tests the fact |
| H-S13 importance of total price 1–5 | Importance ratings inflate everything; no trade-off | Removed; replaced by bill scenarios (Q52–55), choice tasks (Q56–62) and fee ladder (Q70) |
| H-S14 open "what would make you try a new platform" | Hypothetical, unprimed, but uncodeable | Replaced by past switching episodes (Q35–36) + `bt_concern` (Q68) |
| H-S15 concept reveal naming Ownly/Rapido + "no hidden markup" + "₹30" before any blind test | Brand + unverified fee claim revealed together; no blind baseline; biased H7 | Blind "Service X" concept (V1/V2) vs branded (V3/V4), randomised; no ₹ figure; one stated limitation; reveal afterwards |
| H-S16 "willing to try Ownly … if available" | Conditional hypothetical with a brand; yes-bias | `bt_trial_intent` at first exposure (Q64), analysed top-box and calibrated by H11 behavioural checks |
| H-S17 open ₹/% threshold to switch to Ownly | Open numeric with mixed units; branded; no "no amount"/DK codes | Q51 unbranded ₹ ladder with "No amount" and "Don't know" |
| H-S18 open concerns about the concept | OK | Kept as Q68 `bt_concern` |

## 3. Cut for length

| Date | Item | Scope | Decision by | Reason | What still covers it |
|---|---|---|---|---|---|
| 2026-09-14 | B4 / Q17 `beh_last_daytype` | Removed from both cities | Lead | Survey length (main path ≈ 16 min before cuts) | Q27 `beh_weekday_weekend` (brief-mandated weekday/weekend measure) |
| 2026-09-14 | B5 / Q18 `beh_last_location` | Removed from both cities | Lead | Length; no hypothesis test depended on it | `dem_living` (Q10) gives the delivery context by living type |
| 2026-09-14 | U19 `own_nps` | Removed (Bengaluru) | Lead | Length; NPS was secondary per the brief ("only if useful") | `own_continue_intent`, `own_orders_4wk` |
| 2026-09-14 | `dce_t1`–`dce_t6`, `dce_dom` | Hyderabad only (Bengaluru has no choice tasks) | Lead | Bengaluru survey length | Bengaluru ↔ Hyderabad trade-off comparison no longer possible from choice tasks; H9 uses other comparable items |
| 2026-09-14 | `beh_weekday_weekend`, `beh_meal_occasions`, `exp_instructions_importance`, `exp_quality_concern_cheap`, `dem_gender` | Kept in Hyderabad, removed from Bengaluru (`comparable_blr_hyd` = no) | Lead | Bengaluru length | Hyderabad-only descriptives |

**Proposed but NOT applied** (ranked list in `hyderabad_survey_logic.md` §2): Q25, Q75, Q34, Q21, Q67, Q12, Q36, saving about 1.1 min. The pilot median decides.
