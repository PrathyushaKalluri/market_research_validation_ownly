# Bengaluru Survey — Google Form Build Spec, Part 2 (Sections 19–37, 39 + build checklist + QA personas)

Continues from `bengaluru_google_form_part1.md`, which ends at Section 18. The screen-out section is **Section 38**; the optional quota-full section is **Section 39**. Wording source: `03_hyderabad_survey/survey_variable_dictionary.csv`. Module order: `bengaluru_experimental_modules_note.md`.

**v2 (2026-09-14, lead length cuts):** no choice tasks in Bengaluru. own_nps is removed. B1 and B2 differ experimentally **only in the fee-ladder start** (B1 ₹20, B2 ₹40).

---

## Section 19 — Bill examples (bill_s1, bill_s2)

Build both bills as **one side-by-side image per question** (Google Slides → PNG): same font and row order, no logos, no app colours. Paste the plain-text table into the question description as a fallback. Full spec: `03_hyderabad_survey/bill_comparison_scenarios.md` §1–3.

| # | Variable | Question text (exact) | Type | Options | Req |
|---|---|---|---|---|---|
| 19.1 | bill_s1 | Hypothetical example — not a real bill from any app. Both bills are for the **same dinner from the same restaurant**, arriving in the **same time**. All amounts include taxes. Which bill would you rather order with? | Multiple choice + image | Bill 1 / Bill 2 / No real difference to me | Yes |
| 19.2 | bill_s2 | Hypothetical example — not a real bill from any app. Both bills are for the **same dish from the same restaurant**, arriving in the **same time**. All amounts include taxes. Which bill would you rather order with? | Multiple choice + image | Bill 1 / Bill 2 / No real difference to me | Yes |

| Copy | 19.1 Bill 1 / Bill 2 | 19.2 Bill 1 / Bill 2 |
|---|---|---|
| **B1** (Order 1) | Simple (Food ₹210, Delivery ₹35 → **₹245**) / Itemised (Food ₹210, Packaging ₹20, Platform ₹15, Delivery ₹30, Discount −₹30 → **₹245**) | Discount (Food ₹260, Delivery ₹25, Discount −₹50 "Offer applied" → **₹235**) / No-discount (Food ₹210, Delivery ₹25 → **₹235**) |
| **B2** (Order 2) | Itemised / Simple | No-discount / Discount |

⚠ ₹ values are **PROVISIONAL**. Replace them from the audit, keeping the totals identical (design file §6). After section → Section 20.

---

## Section 20 — Delivery-charge framing (text only)

**Description (exact, from `wtp_gabor_granger_design.md` §2):**
> **Imagine a food-delivery service that works like this:**
> • Food is charged at the restaurant's own menu prices.
> • There are no platform charges and no packaging charges.
> • The **only** amount added to your food is **one delivery charge**, shown to you before you order.
> • All amounts include taxes.
> Think about a dinner for one that you would normally order, where **the food costs ₹220**. On the next screens we'll show different delivery charges. For each one, tell us whether you would place this order through **this service**.

After section → **B1: Section 23 (₹20)** · **B2: Section 25 (₹40)**.

## Sections 21–27 — Fee ladder (one question per section)

**Question in each:** "For this ₹220 dinner, the delivery charge is **₹[FEE]**. Would you place this order through this service?"
- Type: Multiple choice. Options: **Yes, I would order / No, not at this delivery charge**. Required: Yes.
- Set go-to on **both** options in every section.

| Section | Variable | Fee | **B1 (start ₹20)** Yes → / No → | **B2 (start ₹40)** Yes → / No → |
|---|---|---|---|---|
| 21 | wtp_accept_0 | ₹0 | S28 / S28 | S28 / S28 |
| 22 | wtp_accept_10 | ₹10 | S28 / S21 | S28 / S21 |
| 23 | wtp_accept_20 | ₹20 | S24 / S22 | S28 / S22 |
| 24 | wtp_accept_30 | ₹30 | S25 / S28 | S28 / S23 |
| 25 | wtp_accept_40 | ₹40 | S26 / S28 | S26 / S24 |
| 26 | wtp_accept_50 | ₹50 | S27 / S28 | S27 / S28 |
| 27 | wtp_accept_60 | ₹60 | S28 / S28 | S28 / S28 |

Routing reproduces Graphs A/B in the design file §3 (END = S28); QA paths are in design §6. `wtp_start` is added in cleaning (B1 = 20, B2 = 40). ⚠ Fee points are PROVISIONAL.

---

## Section 28 — Ownly awareness
| 28.1 | own_aware_aided | Before today, had you heard of Ownly (the food-delivery service from Rapido)? | Multiple choice | Yes, clearly / I think so / No | Yes | **Go to:** Yes, clearly → S29; I think so → S29; No → **S34** |
|---|---|---|---|---|---|---|

## Section 29 — About Ownly
| # | Variable | Text | Type | Options | Req | Go to |
|---|---|---|---|---|---|---|
| 29.1 | own_aware_duration | When did you first hear about it? | Multiple choice | In the last 2 weeks / 2–4 weeks ago / 1–3 months ago / More than 3 months ago / Don't remember | Yes | — |
| 29.2 | own_aware_source | Where did you hear about it? Select all that apply. | Checkboxes | Rapido app / Instagram / YouTube / Friends or colleagues / Posters / outdoor ads / News / LinkedIn / A restaurant / A delivery partner / Other | Yes | — |
| 29.3 | own_tried | Have you ever placed an order on Ownly (in the Ownly app or inside the Rapido app)? | Multiple choice | Yes / No, but I've opened or browsed it / No | Yes | Yes → **S30**; the other two → **S33** |

## Section 30 — Your Ownly use (1)
| # | Variable | Text | Type | Options | Req | Go to |
|---|---|---|---|---|---|---|
| 30.1 | own_first_order_month | When did you place your first Ownly order? | Multiple choice | This month / Last month / 2–3 months ago / 4–6 months ago / More than 6 months ago | Yes | — |
| 30.2 | own_first_trial_trigger | What made you place your first Ownly order? | Multiple choice | A launch offer or discount / I saw lower prices than other apps / No platform or packaging charges / A friend or colleague recommended it / I found it in the Rapido app / A restaurant I like was on it / Curiosity / My usual app had a problem / Other | Yes | — |
| 30.3 | own_choose_reasons | Why do you choose Ownly when you do? Select up to 3. | Checkboxes (at most 3; shuffle On) | Lower final price / No extra charges / A restaurant I wanted / Delivery speed / Reliability / Offers / I already use Rapido / Easy app / Other | Yes | — |
| 30.4 | own_orders_4wk | How many Ownly orders have you placed in the last 4 weeks? | Multiple choice | None / 1 / 2–3 / 4–7 / 8 or more | Yes | None → **S31**; others → **S32** |

## Section 31 — Why not recently (lapsed)
| 31.1 | churn_reduced_reasons | Why haven't you ordered on Ownly recently? Select up to 3. | Checkboxes (at most 3; shuffle On) | Restaurants I wanted weren't there / Late or unreliable deliveries / Cancelled orders / A refund or support problem / The savings weren't worth it / Launch offers ended / Went back to my usual app or membership / Food quality / App problems / My location isn't served / Other | Yes |
|---|---|---|---|---|---|

After section → S32.

## Section 32 — Your Ownly use (2)
| # | Variable | Text | Type | Options | Req |
|---|---|---|---|---|---|
| 32.1 | own_share_of_orders | Of all your food-delivery orders in the last 4 weeks, how many were on Ownly? | Multiple choice | None / A few / About half / Most / All | Yes |
| 32.2 | own_last_total | What was the final amount of your most recent Ownly order? (₹, approximate is fine) | Short answer (Number, 0–10000) | — | No |
| 32.3 | own_perceived_savings | Compared with ordering the same thing on the app you'd otherwise use, your most recent Ownly order was: | Multiple choice | Much more expensive / A bit more expensive / About the same / A bit cheaper / Much cheaper / I didn't compare | Yes |
| 32.4 | own_known_savings | If you did compare: roughly how many rupees did you save? Type a negative number if Ownly was more expensive. Leave blank if you didn't compare. | Short answer (Number, −2000 to 2000) | — | No |
| 32.5 | own_reliability_rating | How often have your Ownly orders arrived on time? | Multiple choice | Rarely / Sometimes / About half the time / Mostly / Always | Yes |
| 32.6 | own_found_restaurants | How often did you find the restaurant you wanted on Ownly? | Multiple choice | Rarely / Sometimes / About half the time / Mostly / Always | Yes |
| 32.7 | own_order_accuracy | How often were your Ownly orders complete and correct? | Multiple choice | Rarely / Sometimes / About half the time / Mostly / Always | Yes |
| 32.8 | own_eta_vs_other | Compared with the other app you use, Ownly delivery is usually: | Multiple choice | Much slower / A bit slower / About the same / A bit faster / Much faster / Don't know | Yes |
| 32.9 | own_issues_3m | In the last 3 months, did any of these happen with Ownly? Select all that apply. | Checkboxes | A late order / A cancelled order / Wrong or missing items / A food quality problem / I needed a refund / I contacted support / None of these | Yes |
| 32.10 | own_support_issue_resolved | Was your most recent Ownly issue resolved to your satisfaction? | Multiple choice | Yes, fully / Partly / No / Still pending / I haven't had an Ownly issue that needed a refund or support in the last 3 months | Yes |
| 32.11 | own_trust | From what you know or have experienced, how much do you trust Ownly with your orders and payments? | Linear scale 1–5 (1 Not at all, 5 Completely) | — | Yes |
| 32.12 | own_competitor_when | When do you still order on another app instead of Ownly? Select up to 3. | Checkboxes (at most 3; shuffle On) | The restaurant isn't on Ownly / I need it faster / A better offer elsewhere / Ownly isn't available at that location or time / After a bad Ownly experience / Group or large orders / Late at night / Habit / I don't use other apps / Other | Yes |
| 32.13 | own_continue_intent | How likely are you to keep ordering on Ownly over the next month? | Multiple choice | Definitely not / Probably not / Not sure / Probably / Definitely | Yes |
| 32.14 | own_disappointment | What, if anything, has disappointed you about Ownly? | Paragraph | — | No |

After section → **S35**.

## Section 33 — Not tried yet (aware)
| 33.1 | own_not_tried_reason | What are the main reasons you haven't ordered on it? Select up to 3. | Checkboxes (at most 3; shuffle On) | Happy with my current app / My usual restaurants weren't on it / Not available at my location / Didn't trust a new app yet / Expected slow delivery / Didn't see real savings / No offers or discounts / Didn't know how to access it / The payment method I use (e.g. cash on delivery or a meal card) isn't accepted / Haven't got round to it / Other | Yes |
|---|---|---|---|---|---|
| 33.2 | own_trust | From what you know or have experienced, how much do you trust Ownly with your orders and payments? | Linear scale 1–5 | 1 Not at all … 5 Completely | Yes |

After section → **S35**. In cleaning, merge 32.11 and 33.2 into one `own_trust` column.

## Section 34 — A new service (unaware only; blind)
**Description (exact K0 blind text):**
> Service X is a food-delivery app where the food prices shown are the restaurant's own prices, and the checkout shows a single delivery charge instead of separate platform, packaging or other fees. Restaurants on it do not pay the app a commission on each order. The delivery time and the number of restaurants available vary by area.

| # | Variable | Text | Type | Options | Req |
|---|---|---|---|---|---|
| 34.1 | bt_appeal | How appealing is this for your own food orders? | Linear scale 1–5 | 1 Not at all appealing … 5 Extremely appealing | Yes |
| 34.2 | bt_trial_intent | If it were available where you are, how likely are you to try it for one of your next few orders? | Multiple choice | Definitely not / Probably not / Not sure / Probably / Definitely | Yes |
| 34.3 | bt_trust | How much would you trust it with your order and payment? | Linear scale 1–5 | 1 Not at all … 5 Completely | Yes |
| 34.4 | bt_expected_reliability | How often would you expect orders from it to arrive on time? | Multiple choice | Rarely / Sometimes / About half the time / Mostly / Almost always / No idea | Yes |
| 34.5 | bt_expected_price | Compared with the app you use most, what would you expect the final amount for the same order to be? | Multiple choice | Much higher / A bit higher / About the same / A bit lower / Much lower / Don't know | Yes |
| 34.6 | bt_concern | What, if anything, would stop you from trying it? | Paragraph | — | No |

After section → S35. (Quota-full: O1 = No routes to S39; see `bengaluru_survey_logic.md` §6.)

## Section 35 — Rapido rides
| 35.1 | dem_rapido_ride_use | In the last 3 months, how often have you taken a Rapido ride (bike, auto or cab)? | Multiple choice | Never used Rapido / Used before, but not in the last 3 months / 1–3 times / 4–10 times / More than 10 times | Yes | Never used Rapido → **S37**; others → **S36** |
|---|---|---|---|---|---|---|

## Section 36 — Rapido experience
| 36.1 | dem_rapido_ride_experience | Overall, how has your experience with Rapido rides been? | Linear scale 1–5 | 1 Very poor … 5 Very good | Yes |
|---|---|---|---|---|---|

## Section 37 — Wrap-up
| # | Variable | Text | Type | Options | Req |
|---|---|---|---|---|---|
| 37.1 | meta_found_survey | Where did you find this survey? | Multiple choice | WhatsApp / Telegram group / LinkedIn / Reddit / Instagram / A friend or colleague sent it / Poster / QR code / College or office group / Other | Yes |
| 37.2 | meta_comments | Anything else you'd like to tell us about food delivery? (optional) | Paragraph | — | No |

**Section description (end text):**
> "Thank you! Your completion code is **BLR-B1-7Q** (B2 copy: **BLR-B2-4K**). If you'd like to enter the lucky draw, open [LUCKY-DRAW FORM LINK — separate form] and paste this code. If you're open to a 30–45 minute interview, sign up at [INTERVIEW SIGN-UP LINK — separate form]. This survey did not collect your name, phone number or email."

After section → **Submit form**.

## Section 39 — Thank you (quota full) — create at build time and leave unused until needed
Text: "Thank you — we have enough responses from people in your situation. Your answers have been recorded." After section → **Submit form**.

---

## Build checklist (B1 → B2)

1. Build B1 in editor order: Sections 1–37, then 38 (screen-out) and 39 (quota-full). Set every go-to exactly as specified. Check that "After section" footers don't override option-level routing.
2. Add the bill images for 19.1 and 19.2 (Order 1), with a text fallback in each description.
3. Get the pre-filled link and record the entry IDs for meta_form_version, meta_session_token, meta_start_ts, meta_source and meta_campaign in `link_randomizer.html`.
4. **Make a copy → B2.** Change only:
   - **Experimental factor:** Section 20 footer → S25, plus the ladder go-tos per the B2 column (start ₹40).
   - **Position counterbalancing, not an experimental factor:** swap the bill images in 19.1/19.2 (Order 2) and reverse the order of options 1–11 in 17.3.
   - Completion code.
5. Link each copy to its own response sheet. Add a combined tab (`=QUERY({B1!A:ZZ;B2!A:ZZ},…)`) for the quota counters.
6. Run all QA personas in **both** copies with `utm_source=blr_qa`. Export RAW, then exclude QA rows via `blr_qa`; never delete them from RAW.
7. Freeze: no edits after launch except the pre-planned unaware-quota switch. Log any change in `decisions.md`.

## QA test personas (walk each path; confirm expected sections appear and skipped columns stay blank)

| Persona | Key answers | Expected path |
|---|---|---|
| P1 Current user, professional | 24 yrs, HSR Layout, 8–15 orders, Working full-time, O1 Yes clearly, O4 Yes, U4 2–3, Rapido 1–3 times | 1→…→7→10→11→12→13→14→16→17→18→19→20→ladder→28→29→30→32→35→36→37 |
| P2 Lapsed user, student | 21 yrs, Koramangala, 1–3 orders, UG student, O1 Yes, O4 Yes, U4 None | …7→8→11…→28→29→30→**31**→32→35… |
| P3 Aware, never tried | 27 yrs, Whitefield, 4–7 orders, O1 I think so, O4 browsed | …28→29→**33**→35… |
| P4 Unaware, working student | 23 yrs, Electronic City, O1 No | …7→**9→10**→11…→28→**34**→35… |
| P5 Screen-outs | Separately: age Over 30; Not in Bengaluru; 0 orders; COI Yes; already filled | Each → S38 → submit |
| P6 Ladder paths | B1: YYYYY, YN, NY, NNN · B2: YYY, YN, NY, NNNNN | Matches `wtp_gabor_granger_design.md` §6; skipped fee columns blank; all paths end at S28 |
| P7 Never used Rapido | 35.1 Never | 35→37 (36 skipped) |
| P8 Switch story | 14.7 Yes | 14→15→16 |
| P9 Quota-full test (after switch) | O1 No | 28→39→submit |
