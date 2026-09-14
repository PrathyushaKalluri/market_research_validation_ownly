# Hyderabad Survey — Google Form Build Spec, Part 2b (S11–S14, build checklist, QA)

---

## S11a Reveal (Section 21) — **V1 and V2 only**; after section → *S11b Rapido*

**Section description:** "**The service you just read about is Ownly, a food-delivery service from Rapido (the bike-taxi and auto app).**"

**Q71 `[br_trial_intent]`** · Multiple choice · Req · Shuffle OFF
"Now that you know it is Ownly from Rapido: if it were available where you are, how likely are you to try it for one of your next few orders?"
- Definitely not · Probably not · Not sure · Probably · Definitely

**Q72 `[br_trust]`** · Linear scale 1–5 · Req · 1 = "Not at all", 5 = "Completely"
"Now that you know it is Ownly from Rapido: how much would you trust it with your order and payment?"

**Q73 `[br_expected_reliability]`** · Multiple choice · Req
"Now that you know it is Ownly from Rapido: how often would you expect orders to arrive on time?"
- Rarely · Sometimes · About half the time · Mostly · Almost always · No idea

**V3/V4:** delete S11a entirely, including Q71–Q73. The last fee sections' END routing points to S11b. *(Lead decision 2026-09-14: post-reveal items are asked in V1/V2 only; `randomization_and_versions.md` is aligned.)*

## S11b Rapido (Section 22)

**Section description:**
- V1/V2: none.
- V3/V4: "As mentioned, this service is Ownly from Rapido."

**Q74 `[br_rapido_effect]`** · Multiple choice · Req · Shuffle OFF
"Does it being from Rapido make you more or less likely to try it?"
- Much less likely · Somewhat less likely · No difference · Somewhat more likely · Much more likely

**Q75 `[br_rapido_effect_why]`** · Paragraph · Req OFF
"Why? (optional)"

**Q76 `[dem_rapido_ride_use]`** · Multiple choice · Req · **→ ON (last on page)**
"In the last 3 months, how often have you taken a Rapido ride (bike, auto or cab)?"
- Never used Rapido → *S12a Awareness*
- Used before, but not in the last 3 months → *S11c Rapido experience*
- 1–3 times → *S11c*
- 4–10 times → *S11c*
- More than 10 times → *S11c*

## S11c Rapido experience (Section 22b) — after section → *S12a Awareness*

**Q77 `[dem_rapido_ride_experience]`** · Linear scale 1–5 · Req · 1 = "Very poor", 5 = "Very good"
"Overall, how has your experience with Rapido rides been?"

---

## S12a Awareness (Section 23)

**Q78 `[own_aware_aided]`** · Multiple choice · Req · → ON
"Before today, had you heard of Ownly (the food-delivery service from Rapido)?"
- Yes, clearly → *S12b*
- I think so → *S12b*
- No → *S14 Wrap-up*

## S12b Awareness detail (Section 24)

**Q79 `[own_aware_duration]`** · Multiple choice · Req
"When did you first hear about it?"
- In the last 2 weeks · 2–4 weeks ago · 1–3 months ago · More than 3 months ago · Don't remember

**Q80 `[own_aware_source]`** · Checkboxes · Req · Shuffle OFF
"Where did you hear about it? Select all that apply."
- Rapido app · Instagram / YouTube · Friends or colleagues · Posters / outdoor ads · News / LinkedIn · A restaurant · A delivery partner · Other

**Q81 `[own_tried]`** · Multiple choice · Req · → ON (last on page)
"Have you ever placed an order on Ownly (in the Ownly app or inside the Rapido app)?"
- Yes → *S13a Ownly first*
- No, but I've opened or browsed it → *S12c Not tried*
- No → *S12c Not tried*

## S12c Not tried (Section 25) — after section → *S14 Wrap-up*

**Q82 `[own_not_tried_reason]`** · Checkboxes · Req · Shuffle ON · Validation: select at most 3
"What are the main reasons you haven't ordered on it? Select up to 3."
- Happy with my current app · My usual restaurants weren't on it · Not available at my location · Didn't trust a new app yet · Expected slow delivery · Didn't see real savings · No offers or discounts · Didn't know how to access it · The payment method I use (e.g. cash on delivery or a meal card) isn't accepted · Haven't got round to it · Other

**Q83 `[own_trust]`** · Linear scale 1–5 · Req · 1 = "Not at all", 5 = "Completely"
"From what you know or have experienced, how much do you trust Ownly with your orders and payments?"

---

## S13a Ownly first (Section 26)

**Q84 `[own_first_order_month]`** · Multiple choice · Req
"When did you place your first Ownly order?"
- This month · Last month · 2–3 months ago · 4–6 months ago · More than 6 months ago

**Q85 `[own_first_trial_trigger]`** · Multiple choice · Req · Shuffle OFF
"What made you place your first Ownly order?"
- A launch offer or discount · I saw lower prices than other apps · No platform or packaging charges · A friend or colleague recommended it · I found it in the Rapido app · A restaurant I like was on it · Curiosity · My usual app had a problem · Other

**Q86 `[own_choose_reasons]`** · Checkboxes · Req · Shuffle ON · Validation: select at most 3
"Why do you choose Ownly when you do? Select up to 3."
- Lower final price · No extra charges · A restaurant I wanted · Delivery speed · Reliability · Offers · I already use Rapido · Easy app · Other

**Q87 `[own_orders_4wk]`** · Multiple choice · Req · → ON (last on page)
"How many Ownly orders have you placed in the last 4 weeks?"
- None → *S13c Lapse reasons*
- 1 → *S13b*
- 2–3 → *S13b*
- 4–7 → *S13b*
- 8 or more → *S13b*

## S13c Lapse reasons (Section 27) — after section → *S13b Ownly experience*

**Q88 `[churn_reduced_reasons]`** · Checkboxes · Req · Shuffle ON · Validation: select at most 3
"Why haven't you ordered on Ownly recently? Select up to 3."
- Restaurants I wanted weren't there · Late or unreliable deliveries · Cancelled orders · A refund or support problem · The savings weren't worth it · Launch offers ended · Went back to my usual app or membership · Food quality · App problems · My location isn't served · Other

## S13b Ownly experience (Section 28) — after section → *S14 Wrap-up*

**Q89 `[own_share_of_orders]`** · Multiple choice · Req
"Of all your food-delivery orders in the last 4 weeks, how many were on Ownly?"
- None · A few · About half · Most · All

**Q90 `[own_last_total]`** · Short answer · Req OFF · Validation: Number between 0 and 10000
"What was the final amount of your most recent Ownly order? (₹, approximate is fine)"

**Q91 `[own_perceived_savings]`** · Multiple choice · Req
"Compared with ordering the same thing on the app you'd otherwise use, your most recent Ownly order was:"
- Much more expensive · A bit more expensive · About the same · A bit cheaper · Much cheaper · I didn't compare

**Q92 `[own_known_savings]`** · Short answer · Req OFF · Validation: Number between −2000 and 2000
"If you did compare: roughly how many rupees did you save? Type a negative number if Ownly was more expensive. Leave blank if you didn't compare."

**Q93 `[own_reliability_rating]`** · Multiple choice · Req
"How often have your Ownly orders arrived on time?"
- Rarely · Sometimes · About half the time · Mostly · Always

**Q94 `[own_found_restaurants]`** · Multiple choice · Req
"How often did you find the restaurant you wanted on Ownly?"
- (same 5 options as Q93)

**Q95 `[own_order_accuracy]`** · Multiple choice · Req
"How often were your Ownly orders complete and correct?"
- (same 5 options as Q93)

**Q96 `[own_eta_vs_other]`** · Multiple choice · Req
"Compared with the other app you use, Ownly delivery is usually:"
- Much slower · A bit slower · About the same · A bit faster · Much faster · Don't know

**Q97 `[own_issues_3m]`** · Checkboxes · Req · Shuffle OFF
"In the last 3 months, did any of these happen with Ownly? Select all that apply."
- A late order · A cancelled order · Wrong or missing items · A food quality problem · I needed a refund · I contacted support · None of these

**Q98 `[own_support_issue_resolved]`** · Multiple choice · Req · **always shown** (Forms cannot branch on Q97's checkboxes)
"Was your most recent Ownly issue resolved to your satisfaction?"
- Yes, fully · Partly · No · Still pending · I haven't had an Ownly issue that needed a refund or support in the last 3 months

**Q99 `[own_competitor_when]`** · Checkboxes · Req · Shuffle ON · Validation: select at most 3
"When do you still order on another app instead of Ownly? Select up to 3."
- The restaurant isn't on Ownly · I need it faster · A better offer elsewhere · Ownly isn't available at that location or time · After a bad Ownly experience · Group or large orders · Late at night · Habit · I don't use other apps · Other

**Q100 `[own_trust]`** · Linear scale 1–5 · Req — identical to Q83.

- **Why a single variable works:** Q83 (S12c, aware non-triers) and Q100 (S13b, triers) sit on mutually exclusive branches of Q81. Routing never takes a respondent through both S12c and S13b.
- **Merge rule:** `own_trust` = Q100 if `own_tried` = Yes, else Q83.
- **Back-button edge case:** if Back-button navigation leaves an orphan answer in the other column, keep the one consistent with the final `own_tried` answer and flag `FLAG_own_trust_orphan`.

**Q101 `[own_continue_intent]`** · Multiple choice · Req
"How likely are you to keep ordering on Ownly over the next month?"
- Definitely not · Probably not · Not sure · Probably · Definitely

**Q102 `[own_disappointment]`** · Paragraph · Req OFF
"What, if anything, has disappointed you about Ownly?"

---

## S14 Wrap-up (Section 29) — after section → **Submit form**

**Q103 `[meta_found_survey]`** · Multiple choice · Req · Shuffle OFF
"Where did you find this survey?"
- WhatsApp / Telegram group · LinkedIn · Reddit · Instagram · A friend or colleague sent it · Poster / QR code · College or office group · Other

**Q104 `[meta_comments]`** · Paragraph · Req OFF
"Anything else you'd like to tell us about food delivery? (optional)"

**Section description (end-page text):**
> "Almost done — press **Submit**. After submitting you'll see a completion code.
> Optional: **Lucky draw** → [LUCKY DRAW FORM LINK] (asks for your email and the completion code; kept separately from your answers).
> **Interview volunteers** (30–45 min, voucher) → [INTERVIEW SIGN-UP LINK]. Please share the survey with friends in Gachibowli: [RANDOMISER LINK]."

---

## Build checklist for the 4 versions

1. **Build V1 as the master:** blind concept, Block 1, bill Order 1, ladder Graph A (start ₹20), S11a present.
2. **Pilot V1** (`pilot_and_cognitive_test_protocol.md`), then freeze the wording.
3. **Make copies** (Form ⋮ → Make a copy) and change ONLY these:

| Change | V2 | V3 | V4 |
|---|---|---|---|
| S7 bill images + descriptions → Order 2 | ✔ | — | ✔ |
| S8 task images/tables → Block 2 | ✔ | — | ✔ |
| S9 concept text → branded | — | ✔ | ✔ |
| S10 routing → Graph B (start ₹40) | ✔ | ✔ | — |
| Delete S11a; END routing → S11b; add S11b "As mentioned…" description | — | ✔ | ✔ |
| Confirmation code text (HV2 / HV3 / HV4) | ✔ | ✔ | ✔ |

4. **In every copy:**
   - Link the response sheet to its own tab.
   - Fetch the pre-fill entry IDs separately (copying changes them) and send them to the `link_randomizer.html` constants.
   - Re-check that "Go to section" targets still point to the right sections; copying keeps them, but section deletion in V3/V4 can reset targets to "Continue".
5. **Final setting check:** emails OFF, limit-1 OFF, progress bar ON.

## QA test personas (run in EVERY version; mark Sheet rows with `meta_source = qa`)

| # | Persona | Path to verify |
|---|---|---|
| P1 | Age 32 | Q2 → SO → submit; row blank after screener |
| P2 | Lives in Kukatpally | Q3 "Somewhere else" → SO |
| P3 | UG student at IIIT-H, frequent, switched app last year, asked for a refund; not aware of Ownly; Rapido never | S2a → S2b → S2d; S4b shown; Q42 answered; ladder Yes-Yes-No; Q76 Never → S12a; Q78 No → S14 |
| P4 | Working student, aware of Ownly, browsed not tried | S2c → S2e → S2d; Q81 → S12c → S14; ladder No-No-No (rejects all) |
| P5 | Working professional, Ownly user, 0 Ownly orders last 4 weeks, had an issue | S2e; Q81 Yes → S13a → Q87 None → S13c → S13b → S14; Q98 answered |
| P6 | Other/between jobs, active Ownly user (4–7 orders), no issues, Rapido rider (bad experience) | S2a → S2d; Q76 → S11c; Q87 → S13b; Q98 = "haven't had an issue" |
| P7 (V1/V2 vs V3/V4) | Any complete path | S11a appears only in V1/V2; branded text only in V3/V4; fee start ₹20 (V1/V4) vs ₹40 (V2/V3) |
| P8 | Uses Back button inside the ladder, then changes an answer | Sheet: orphan fee answers → cleaning `FLAG_wtp_nonmonotone` rule works |
