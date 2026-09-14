# Bengaluru Survey: Experimental Modules Note

**Version:** 2026-09-14 v2 (lead length cuts: choice tasks removed from Bengaluru). **Companion files:** `03_hyderabad_survey/randomization_and_versions.md`, `bill_comparison_scenarios.md`, `wtp_gabor_granger_design.md`.

## 1. Versions

| Version | Fee-ladder start (experimental factor) | Bill order (position counterbalancing only) |
|---|---|---|
| **B1** | ₹20 | Order 1 |
| **B2** | ₹40 | Order 2 |

Assignment is 50/50 via `link_randomizer.html?city=blr`, with the same technical fields as Hyderabad (`meta_form_version`, `meta_session_token`, `meta_start_ts`, `meta_source`, `meta_campaign`).

**Change from v1:** the choice experiment is removed from Bengaluru. B1/B2 therefore differ experimentally **only in the ladder start**. The earlier block/start confound is gone, and the start (anchoring) effect is estimable in Bengaluru. Bill order also alternates, but only as position counterbalancing; the bills come before the ladder and are not expected to affect fee acceptance, and this is checked by including order as a covariate.

## 2. What is identical to Hyderabad (for H9 matched comparisons)

- **Fee ladder:** same framing screen (₹220 dinner for one; "this service"), same fee points, same two start points in the same 50/50 split, same derived variables.
- **Bill scenarios bill_s1 and bill_s2:** same stimuli, same order counterbalancing.
- **Variable names:** `wtp_start`, `wtp_accept_*`, `wtp_max_fee`, `bill_s1`, `bill_s2`.

## 3. What differs

| Module | Bengaluru | Reason |
|---|---|---|
| Choice tasks (DCE) | **Not included** (lead decision, 2026-09-14) | Survey length. H3–H5 are Hyderabad-only confirmatory tests, so no Bengaluru DCE comparison is made. **Cost:** there are no cross-city choice-model WTP comparisons for ETA, reliability or assortment. H9.3 uses stated expectations (`exp_eta_max_*`, ADI) instead. |
| Brand-arm experiment (H7) | **Not included** | H7 is a Hyderabad question. Most Bengaluru respondents are recruited *because* they know Ownly, so a blind arm is impossible for the key group. |
| Blind concept | Short version for **unaware** respondents only | Barriers and attractiveness for non-users |
| Bill scenarios | **bill_s1 and bill_s2 only** | Both test whether transparency and discount framing are valued at *identical totals* (transfer row BA2). bill_s3/bill_s4's "usual app vs new app" framing is ambiguous for Ownly users. |

## 4. Placement in the Bengaluru form

1. Consent → screener → segment → recent behaviour → unaided awareness → pain → expectations
2. **bill_s1, bill_s2**
3. **Fee ladder**
4. Ownly-status branch: current/lapsed user module, aware-never-tried module, or unaware short concept
5. Rapido ride use → wrap-up

Placing the experimental modules **before** the Ownly-user branch keeps them uncontaminated by Ownly-specific questions. The module sequence (bills → ladder) matches Hyderabad.

## 5. Analysis note

- City comparisons of fee acceptance and bill shares use the **reweighted** Bengaluru sample (post-stratified to Hyderabad on `seg_occupation × seg_freq`). Bengaluru Ownly users and non-users are analysed separately.
- The Bengaluru start effect: `acc ~ fee + start40 + fee×start40 (+ bill_order)`, with respondent-clustered SEs.
