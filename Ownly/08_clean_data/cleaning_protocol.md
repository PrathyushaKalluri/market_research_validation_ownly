# Data-Cleaning Protocol (reproducible)

**Version:** 2026-09-14. **Applies to:** Bengaluru survey, the 4 Hyderabad survey versions, audit data and fake-door events.

**Core rule: never silently delete.** Every row that enters RAW ends up in exactly one of CLEANED or EXCLUDED, with an `exclusion_reason`.

## 1. Folder states

```
08_clean_data/
├── raw/        immutable exports (never edited). MANIFEST.csv holds file, export_ts, rows, sha256
├── interim/    renamed/harmonised (script output; regenerable)
├── cleaned/    analysis-eligible rows (script output)
├── excluded/   excluded rows + exclusion_reason + flag detail (script output)
├── flags.csv   every row × every check (0/1) + values used
├── adjudication_log.csv   borderline decisions: resp_id, flag, reviewer_1, reviewer_2, decision, rationale, date
└── master_data_dictionary.csv
```

## 2. Pipeline order (scripted in `09_analysis/01–03_*.py`)

| Step | Action | Output |
|---|---|---|
| 0 | Export each Google Form response sheet to CSV with a date stamp. Hash it and add a row to MANIFEST. | `raw/` |
| 1 | Rename columns from question text to `variable_name` using the dictionary mapping. Add `city`, `meta_form_version`, `meta_brand_arm`, `meta_dce_block`. Generate `resp_id` = `{city}_{version}_{row}`. | `interim/` |
| 2 | Type coercion: numeric ₹ (strip "₹", commas; "250-300" → midpoint, flagged `num_parsed_range`), ages, timestamps (IST). | `interim/` |
| 3 | Recode open "Other" locality text to the locality list (a two-person rule for ambiguous entries). | `interim/` + recode log |
| 4 | Compute all quality flags (§3). No rows removed yet. | `flags.csv` |
| 5 | Adjudicate borderline flags (§4). | `adjudication_log.csv` |
| 6 | Split into CLEANED / EXCLUDED using the precedence order (§5). | `cleaned/`, `excluded/` |
| 7 | Produce a CONSORT-style flow table: starts → screen-outs → completes → exclusions by reason → valid, by city/version/channel. | `09_analysis/outputs/sample_flow.csv` |

## 3. Quality checks (flags)

| Code | Check | Rule (default *(A)*, adjust only before field close) | Hard / borderline |
|---|---|---|---|
| EX01_screen_fail | Consent no / age ∉ [20,30] / locality outside list / no order in last 4 weeks / conflict-of-interest employer | Any true | Hard |
| EX02_speeder | Duration (`meta_submit_ts − meta_start_ts`, if captured; otherwise not computable → note) < 40% of the median for the same form version | < 40% → hard; 40–50% → borderline | Hard/borderline |
| EX03_attention_fail | Instructed-response item answered incorrectly | Wrong | Hard |
| EX04_straightline | All pain and expectation grid items identical (SD = 0) **including** a reverse-keyed item | True → borderline; also a speeder → hard | Borderline |
| EX05_duplicate | Same `meta_session_token`; or same demographic signature + < 30 min apart; or open-text similarity > 0.9 on ≥ 2 fields; or self-reported repeat | Keep the **first complete** submission; exclude later ones | Hard (token/self-report), borderline (pattern) |
| EX06_incoherent | 0 orders in 4 weeks but last order ≤ 4 weeks ago; Ownly "never heard" but Ownly order reported; last order total < ₹50 or > ₹5,000; fee ladder non-monotone (accepts ₹50, rejects ₹20) | Borderline; ≥ 2 incoherences → hard. A non-monotone ladder only sets `wtp_max_fee` = NA (row not excluded) | Borderline |
| EX07_bot_or_gibberish | Open texts random characters, identical across ≥ 3 rows, or irrelevant copy-paste | Hard after review | Borderline → hard |
| EX08_missing_critical | Missing `seg_occupation`, `scr_orders_4wk` or ≥ 2 PPI items | Hard | Hard |
| EX09_outside_target_after_recode | "Other" locality recodes outside the target area | Hard | Hard |
| FLAG_choice_left_right | Chose the same position in all choice tasks | Flag only; sensitivity analysis excludes | — |
| FLAG_dominance_fail | Chose the dominated alternative in a dominance check task | Flag only; sensitivity analysis | — |
| FLAG_iiith | Recruitment channel IIIT-H | Flag only; sensitivity analysis | — |

## 4. Adjudication

- Borderline rows are reviewed independently by 2 team members, blind to the row's answers on hypothesis outcome items where feasible.
- Disagreement → a third member decides.
- Log every decision. Rows kept after adjudication carry `EX_borderline = 1` for sensitivity analysis.

## 5. Exclusion precedence (first match is recorded as the primary `exclusion_reason`; all flags are kept)

EX01 → EX08 → EX05 → EX07 → EX03 → EX02 → EX09 → EX06 → EX04

## 6. Audit data cleaning

- Double-enter 10% of rows. Discrepancy rate > 3% → re-check all rows from that auditor.
- Invalid when: `final_payable` ≠ `menu_subtotal + fees + taxes − discount` beyond ₹2 tolerance → recheck the screenshot. If irreconcilable → `EXA1_arith`.
- Pair eligibility: platforms captured > 10 min apart → `EXA2_time_gap` (kept in observations, excluded from pairs).
- `item_match_quality = none` → excluded from price pairs, kept for coverage.

## 7. Fake-door event cleaning

- Exclude `is_qa = 1` sessions and sessions with a `?v=` override.
- Bot heuristics: user-agent contains bot/crawler; > 20 events within 2 s; time-to-CTA < 500 ms → `EXF1_bot`.
- Deduplicate on `anon_session_id`; first variant assignment wins.

## 8. Reporting

The final report and dashboard show:
- the sample-flow table
- exclusion counts by reason and city
- a sensitivity table (★ hypotheses with and without borderline rows, IIIT-H, working students)
