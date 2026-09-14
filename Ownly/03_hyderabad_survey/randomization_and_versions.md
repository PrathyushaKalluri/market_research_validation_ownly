# Randomisation & Form Versions

**Version:** 2026-09-14. **Serves:** H7 (brand arms), the H2–H5 choice experiment (blocks), H8 (fee-ladder start), and position-bias control for the bill scenarios.

**Why versions instead of in-form randomisation.** Google Forms cannot randomise which *section* a respondent sees, and it cannot store a random assignment. So each experimental cell is a separate **copy of the same form**. A static link randomiser (`link_randomizer.html`) sends each respondent to one copy and pre-fills technical fields.

## 1. Version matrix

| Version | City | Concept exposure (H7) | Choice-experiment block | Bill scenario option order | Fee-ladder start (`wtp_start`) |
|---|---|---|---|---|---|
| **V1** | Hyderabad | BLIND → reveal | Block 1 | Order 1 | ₹20 |
| **V2** | Hyderabad | BLIND → reveal | Block 2 | Order 2 (swapped) | ₹40 |
| **V3** | Hyderabad | BRANDED from first exposure | Block 1 | Order 1 | ₹40 |
| **V4** | Hyderabad | BRANDED from first exposure | Block 2 | Order 2 (swapped) | ₹20 |
| **B1** | Bengaluru | (no brand-arm experiment) | Block 1 | Order 1 (bill_s1, bill_s2 only) | ₹20 |
| **B2** | Bengaluru | (no brand-arm experiment) | Block 2 | Order 2 | ₹40 |

**Balance properties (Hyderabad):**
- Each brand arm contains both choice-experiment blocks and both ladder starts.
- Each block contains both arms and both ladder starts.
- Arm is therefore orthogonal to block and start, so the H7 comparison is not confounded with either.
- Bill-scenario order is tied to block (V1/V3 vs V2/V4). This is harmless: the bill module comes **before** the choice tasks, so the block's content cannot influence bill answers. Bill order is orthogonal to arm.

**Bengaluru:** ladder start is tied to block (B1 = ₹20, B2 = ₹40). This is an accepted limitation, since the choice tasks precede the ladder. The ₹20/₹40 split is 50/50, as in Hyderabad, so pooled city comparisons of fee acceptance use the same start mix.

## 2. Build procedure (do in this order)

1. Build **V1 completely** as the master form. Include all sections, the choice tasks for block 1, bill Order 1, the ladder with start ₹20, and the blind concept → reveal.
2. Freeze V1 wording after the pilot (`pilot_and_cognitive_test_protocol.md`).
3. For each other version: **Form ⋮ → Make a copy**, then edit ONLY these modules:
   - V2: swap choice tasks to block 2 (`dce_design_matrix.csv`); swap bill order; rebuild ladder branching for start ₹40 (`wtp_gabor_granger_design.md` §3, graph B).
   - V3: replace the blind concept section with the branded concept (same text + brand line); rebuild ladder branching for start ₹40; delete the whole S11a reveal section, **including** the post-reveal items `br_trial_intent`, `br_trust`, `br_expected_reliability`. These are asked in V1/V2 only. V3/V4 already saw the brand at first exposure, so repeating the items is redundant and adds demand effects. `br_rapido_effect`, `dem_rapido_ride_use` and `dem_rapido_ride_experience` stay in all versions. *(Changed by lead decision 2026-09-14.)*
   - V4: as V3, plus block 2 and bill Order 2; ladder start ₹20.
4. **Settings in every copy:**
   - Collect emails OFF
   - Limit to 1 response OFF (it would require sign-in)
   - Progress bar ON
   - Shuffle question order OFF
   - Response sheet: each copy links to its **own** tab in one shared Google Sheet (Responses → Link to Sheets → *Select existing spreadsheet*)
5. Put the 5 technical short-answer questions **on page 1 (S0 Intro)**, below the intro text and before consent. Mark them not required, with the description "Filled in automatically — please don't change":
   `meta_form_version`, `meta_session_token`, `meta_start_ts`, `meta_source`, `meta_campaign`.
   **Why page 1:** Google Forms saves only the pages a respondent actually visits. Respondents screened out early never reach a last section, so their token and source would be lost, and the sample-flow table and channel screen-out rates need them. *(Changed by lead decision 2026-09-14; previously a final section.)*
6. Get pre-filled entry IDs **from each copy separately**: ⋮ → *Get pre-filled link* → type dummy values → *Get link*. Copying a form changes entry IDs.

## 3. Pre-fill URL construction

```
https://docs.google.com/forms/d/e/<FORM_ID>/viewform?usp=pp_url
  &entry.<ID_version>=V2
  &entry.<ID_token>=3f0c…-uuid
  &entry.<ID_start>=1758612345678        (epoch ms at redirect)
  &entry.<ID_source>=linkedin
  &entry.<ID_campaign>=hyd_wave1
```

- The randomiser builds this automatically. Put the base URL and entry IDs into its `FORMS` constant.
- **Duration** = Google Forms `Timestamp` (submit time, IST) − `meta_start_ts` (convert epoch ms → IST). This duration includes screen-out time before the first page and is used for the speeder rule (`08_clean_data/cleaning_protocol.md` EX02).

## 4. Distribution rules

- **Share only the randomiser URL**, one per channel with UTM:
  `…/link_randomizer.html?utm_source=iiith&utm_campaign=hyd_w1`
  `…/link_randomizer.html?city=blr&utm_source=reddit_blr&utm_campaign=blr_w1`
- A response with an empty `meta_session_token` means someone opened a form URL directly. It is **flagged** (`FLAG_no_token`), kept, and analysed for sensitivity; its arm is still known from which sheet tab it arrived in.
- Never post the raw Google Form links. If a form link leaks, rotate: Form ⋮ → *Make a copy* is **not** needed; just watch the flag rate.

## 5. Balance monitoring (daily, Person 3)

| Check | Computation | Action threshold |
|---|---|---|
| Version counts (Hyderabad) | Completes per V1–V4 from `meta_form_version` | Any version < 20% or > 30% of completes after n ≥ 80 → switch to `apps_script_randomizer_alternative.gs` (counter-based cycling) |
| Arm balance | (V1+V2) vs (V3+V4) | Outside 45/55 → same action |
| Block balance | (V1+V3) vs (V2+V4) | Outside 45/55 → same action |
| Differential drop-off | Starts → completes per version. Starts = randomiser opens, only if logged; otherwise compare screen-in → complete in the sheet | Completion rate differs by > 10 pp between arms → inspect the branded concept section for a technical problem |
| Direct-link responses | Share with empty token | > 5% → find and remove the leaked link |
| Covariate balance (post-close) | SMD of `seg_occupation`, `seg_freq`, unaided Ownly awareness by arm | SMD > 0.2 → include as covariate (pre-declared in the pre-analysis plan) |

Test for imbalance with a chi-square goodness-of-fit test against equal shares, as a diagnostic only. Do **not** re-randomise completed respondents.

## 6. QA before launch (record in the pilot edit log)

1. Open the randomiser 20× with `?utm_source=qa`. All 4 versions (2 for `?city=blr`) should appear, and the technical fields must be pre-filled.
2. For **each** version, submit test responses that cover:
   - a screen-out path
   - the ladder paths: start ₹20 → yes, yes, yes, yes (to ₹60); start ₹20 → no, no, no (to ₹0); start ₹40 → no then yes at ₹30
   - each Ownly-status branch
3. Confirm in the sheet: correct variable columns; skipped ladder sections are blank (not stale answers after using *Back*); `meta_*` fields populated.
4. **Never delete test rows.** They carry `meta_source = qa` / `qa_override` and are excluded by rule in cleaning.
5. Confirm the choice-task images match the matrix row for row (a second person checks every task against `dce_design_matrix.csv`).
