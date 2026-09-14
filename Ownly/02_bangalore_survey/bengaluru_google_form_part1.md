# Bengaluru Survey — Google Form Build Spec, Part 1 (settings + Sections 1–18, 38)

Canonical wording: `03_hyderabad_survey/survey_variable_dictionary.csv`. Every item scoped `both` is copied verbatim; **don't reword it**, or city comparisons break. Part 2 (`bengaluru_google_form_part2.md`) covers editor Sections 19–37: bill examples, fee ladder, the Ownly-status branch, Rapido and wrap-up. **No choice tasks in Bengaluru** (lead decision 2026-09-14, length). **Option separator:** in these tables " / " separates options. Where an option label itself contains " / " (e.g. "PG / co-living", "Chinese / Asian"), copy it from the dictionary, where options are separated by " | ".

**Copies:** build **B1** (DCE block 1) and finish it fully, then *Make a copy* → **B2**, The only experimental difference is the **fee-ladder start (B1 ₹20, B2 ₹40)**. Position counterbalancing (bill-image order, 17.3 option order) and the completion code also change; see Part 2's build checklist. The link randomiser (`03_hyderabad_survey/link_randomizer.html?city=blr`) assigns B1/B2 and pre-fills the meta fields.

---

## Form settings (Settings tab)

| Setting | Value | Why |
|---|---|---|
| Collect email addresses | **Off** | Anonymous survey |
| Restrict to users in org / require sign-in | **Off** | Sign-in reduces completion (see F_sample_plan §8) |
| Limit to 1 response | **Off** | Needs sign-in; duplicates are handled by token + checks |
| Allow response editing | Off | Data integrity |
| Show progress bar | On | Completion |
| Shuffle question order | **Off** (form-level) | Order is part of the design (unaided before prompted) |
| Confirmation message | "Thank you — your response has been recorded." (the completion code is on the last section instead) | — |
| Show link to submit another response | Off | Duplicates |
| Presentation → "View results summary" | Off | Avoids priming others |
| Responses → Link to Sheets | On — one sheet per copy (`BLR_B1_responses`, `BLR_B2_responses`) | Export to `08_clean_data/raw/` |

**Conventions below:**
- **Type** uses Google Forms names.
- **Req** = Required toggle.
- **Go to** = "Go to section based on answer" (⋮ menu on the question; only works for Multiple choice/Dropdown).
- **After section** = the section footer's "After section N" dropdown.
- Each branching question is placed **last in its own section** so its branch always applies.

---

## Section 1 — S0 Intro & consent

**Section title:** Food delivery in Bengaluru — a short student survey

**Section description (paste):**
> We are a team of university students running an independent research project on how people aged 20–30 order food delivery in Bengaluru. **This project is not run by, funded by or affiliated with any food-delivery or ride-hailing company.**
> • It takes about 12 minutes.
> • It is anonymous: we don't ask for your name, phone number or email.
> • Taking part is voluntary. You can stop at any time; unfinished responses are not submitted.
> • Answers are used only for our course project, reported in summary form, and stored by the research team until the project is graded (then deleted).
> • Questions? Contact: [TEAM CONTACT EMAIL — placeholder].
> There are no right or wrong answers. Please answer about what you actually do.

| # | Variable | Text | Type | Options | Req | Notes |
|---|---|---|---|---|---|---|
| 1.1 | meta_form_version | Version code (pre-filled — please don't change) | Short answer | — | Yes | Pre-filled `B1` / `B2` |
| 1.2 | meta_session_token | Session code (pre-filled — please don't change) | Short answer | — | No | Pre-filled UUID |
| 1.3 | meta_start_ts | Start code (pre-filled — please don't change) | Short answer | — | No | Pre-filled epoch ms |
| 1.4 | meta_source | Source code (pre-filled — please don't change) | Short answer | — | No | Pre-filled utm_source (values in `bengaluru_survey_logic.md` §5) |
| 1.4b | meta_campaign | Campaign code (pre-filled — please don't change) | Short answer | — | No | Pre-filled utm_campaign (e.g. `blr_wave1`) |
| 1.5 | meta_consent | I have read the information above, I am 18 or older, and I agree to take part. | Multiple choice | Yes, I agree / No | Yes | **Go to:** Yes → Section 2; No → **Section 38 (Not eligible / thank you)** |

Tip: get the pre-fill entry IDs via ⋮ → *Get pre-filled link*, fill dummy values, copy the URL, and read the `entry.NNNN` IDs into the randomiser constants.

---

## Section 2 — S1a Age
| # | Variable | Text | Type | Options (in order) | Req | Go to |
|---|---|---|---|---|---|---|
| 2.1 | scr_age_band | How old are you? | Multiple choice | Under 20 / 20–22 / 23–25 / 26–28 / 29–30 / Over 30 | Yes | Under 20 → S38; Over 30 → S38; others → Section 3 |

## Section 3 — S1b Area
| # | Variable | Text | Type | Options (in order) | Req | Go to |
|---|---|---|---|---|---|---|
| 3.1 | scr_area | Which area of Bengaluru do you usually get food delivered to? | Multiple choice | Koramangala / HSR Layout / BTM Layout / Indiranagar / Domlur / Whitefield / Marathahalli / Bellandur / Electronic City / JP Nagar / Jayanagar / Banashankari / Hebbal / Yelahanka / Manyata / Malleshwaram / Rajajinagar / Other area of Bengaluru / Not in Bengaluru | Yes | Not in Bengaluru → S38; others → Section 4 |

Codes: 1 Koramangala, 2 HSR, 3 BTM, 4 Indiranagar/Domlur, 5 Whitefield/Marathahalli/Bellandur, 6 Electronic City, 7 JP Nagar/Jayanagar/Banashankari, 8 Hebbal/Yelahanka/Manyata, 9 Malleshwaram/Rajajinagar, 10 Other, 99 Not in Bengaluru. **Type the option labels exactly as the grouped labels in the dictionary** (e.g. "Indiranagar / Domlur" is one option). Don't shuffle.

## Section 4 — S1c Recent ordering
| # | Variable | Text | Type | Options | Req | Go to |
|---|---|---|---|---|---|---|
| 4.1 | scr_orders_4wk | In the last 4 weeks, about how many times did you order food for delivery through any app? Count each order once. | Multiple choice | None / 1–3 times / 4–7 times / 8–15 times / 16 or more times | Yes | None → S38; others → Section 5 |

## Section 5 — S1d Conflict of interest
| 5.1 | scr_coi | Do you work for a food-delivery, quick-commerce or restaurant-aggregator company, or in market research? | Multiple choice | Yes / No | Yes | Yes → S38; No → Section 6 |
|---|---|---|---|---|---|---|

## Section 6 — S1e Repeat check
| 6.1 | scr_repeat | Have you already filled in this survey before (any version)? | Multiple choice | Yes / No | Yes | Yes → S38; No → Section 7 |
|---|---|---|---|---|---|---|

---

## Section 7 — S2a About you
| # | Variable | Text | Type | Options | Req | Go to |
|---|---|---|---|---|---|---|
| 7.1 | seg_occupation_raw | Which best describes you right now? | Multiple choice | Full-time student (undergraduate) / Full-time student (postgraduate / PhD) / Working full-time / Studying and working (incl. internships / part-time jobs) / Other / between jobs | Yes | UG or PG student → **Section 8**; Working full-time → **Section 10**; Studying and working → **Section 9**; Other → **Section 11** |

## Section 8 — S2b Study (students)
| 8.1 | dem_institution | Where do you study? | Multiple choice | A college/university in Bengaluru / Elsewhere / online | Yes | After section → **Section 11** |
|---|---|---|---|---|---|---|

## Section 9 — S2b' Study (studying and working)
Duplicate of 8.1 (same text, same options). **After section → Section 10.** Both sections map to `dem_institution` during cleaning.

## Section 10 — S2c Work
| 10.1 | dem_work_sector | Which best describes where you work? | Multiple choice | IT / software product or services / Global capability centre, consulting or finance / Other corporate / Startup / Government / PSU / Other | Yes | After section → Section 11 |
|---|---|---|---|---|---|---|

## Section 11 — S2d Living & spend
| # | Variable | Text | Type | Options | Req |
|---|---|---|---|---|---|
| 11.1 | dem_living | Where do you currently live? | Multiple choice | Hostel / PG / co-living / Shared flat with friends or flatmates / With family / Alone in a rented place / Other | Yes |
| 11.2 | dem_delivery_spend_month | Roughly how much do you personally spend on food delivery in a typical month? | Multiple choice | Less than ₹1,000 / ₹1,000–2,499 / ₹2,500–4,999 / ₹5,000–9,999 / ₹10,000 or more / Prefer not to say | Yes |

---

## Section 12 — S3a Apps you know (unaided; **must be its own page**)
| 12.1 | beh_unaided_apps | Which food-delivery apps can you think of, even ones you don't use? Type as many as come to mind. | Paragraph | — | Yes |
|---|---|---|---|---|---|

Section description: "Please answer from memory — don't look anything up." Nothing on this page may name any app.

## Section 13 — S3b Your most recent order
**Description:** "Think about the most recent time you ordered food for delivery."

| # | Variable | Text | Type | Options | Req | Validation / shuffle |
|---|---|---|---|---|---|---|
| 13.1 | beh_last_order_when | When did you place your most recent food-delivery order? If you can, check your order history. | Multiple choice | Today / Yesterday / 2–3 days ago / 4–7 days ago / 1–2 weeks ago / 2–4 weeks ago / More than 4 weeks ago | Yes | No shuffle |
| 13.2 | beh_last_platform | Which app or channel did you use for that order? | Multiple choice | Swiggy / Zomato / Ownly app / Rapido app (food section) / Toing / Magicpin / EatSure / Restaurant's own app / website / phone / Other | Yes | No shuffle |
| 13.3 | beh_last_meal | Which meal was it? | Multiple choice | Breakfast / Lunch / Evening snack / Dinner / Late night (after 11 pm) | Yes | — |
| 13.4 | beh_last_people | How many people was that order for? | Multiple choice | Just me / 2 people / 3–4 people / 5 or more | Yes | — |
| 13.5 | beh_last_food | What kind of food was it mainly? | Multiple choice | Biryani / South Indian / North Indian / Chinese / Asian / Pizza / burgers / fast food / Healthy / salads / bowls / Desserts / beverages / cafe / Other | Yes | — |
| 13.6 | beh_last_restaurant_type | Which best describes the restaurant? | Multiple choice | Well-known chain / Local / independent restaurant / Delivery-only brand / cloud kitchen / Not sure | Yes | — |
| 13.7 | beh_last_order_total | What was the final amount you paid for that order, including all charges and after any discount? (₹, approximate is fine) | Short answer | — | Yes | Response validation: **Number → Between 0 and 10000**; error text "Please enter a number in rupees, e.g. 280" |
| 13.8 | beh_last_total_recall | How sure are you about that amount? | Multiple choice | I checked the app / Fairly sure / It's a rough guess | Yes | — |
| 13.9 | beh_last_discount | Did that order use a discount or membership benefit? | Multiple choice | Yes, a coupon or offer / Yes, a membership benefit (e.g. free delivery) / Both / No / Not sure | Yes | — |
| 13.10 | beh_last_fees_noticed | Which charges do you remember seeing on that bill? Select all that apply. | Checkboxes | Delivery fee / Platform fee / Packaging charge / Small-order fee / Rain / surge fee / Taxes / GST / Tip / Donation / None of these / Don't remember | Yes | No shuffle |
| 13.11 | dec_last_reasons | Why did you use that app for that order? Select up to 3. | Checkboxes | Had the restaurant or dish I wanted / Lowest final price / A discount or offer / Fastest delivery time / It's the app I always use / My membership benefits / Reliable in my experience / Easy to use / Better support or refunds / Good ratings / reviews / Other | Yes | Validation: **Select at most 3**. Shuffle option order **On** ("Other" stays last automatically only if added as the "Other" option — add it as a normal last option and accept the shuffle, or turn shuffle off and rotate between B1/B2; **recommended: shuffle On**) |

---

## Section 14 — S4 Habits and apps
| # | Variable | Text | Type | Options | Req | Notes |
|---|---|---|---|---|---|---|
| 14.1 | beh_platforms_used_4wk | Which apps or channels have you ordered food delivery from in the last 4 weeks? Select all that apply. | Checkboxes | Swiggy / Zomato / Ownly app / Rapido app (food section) / Toing / Magicpin / EatSure / Restaurant direct / Other | Yes | Validation: at least 1 |
| 14.2 | beh_platform_primary | Which one do you use most? | Multiple choice | Swiggy / Zomato / Ownly app / Rapido app (food section) / Toing / Magicpin / EatSure / Restaurant direct / Other | Yes | |
| 14.3 | beh_subscriptions | Which food-delivery memberships do you have right now? Select all that apply. | Checkboxes | Swiggy One (any plan) / Zomato Gold / Another food-delivery membership / None / Not sure | Yes | |
| 14.4 | beh_offer_dependency | Think about your last 10 delivery orders. Roughly how many used a coupon, offer or membership discount? | Multiple choice | 0–1 / 2–4 / 5–7 / 8–10 / Don't know | Yes | |
| 14.5 | dec_habit_lock | How much do you agree: "I usually open the same app and order, without checking other apps." | Linear scale 1–5 | 1 = Strongly disagree … 5 = Strongly agree | Yes | Labels: 1 Strongly disagree, 5 Strongly agree |
| 14.6 | beh_compare_freq | In the last 4 weeks, how often did you compare the price of the same order on two or more apps? | Multiple choice | Never / Rarely / Sometimes / Often / Very often | Yes | |
| 14.7 | beh_switched_primary_12m | In the last 12 months, did you change which app you use most for food delivery? | Multiple choice | Yes / No / Not sure | Yes | **Go to:** Yes → Section 15; No / Not sure → Section 16. **Must be the last question in Section 14.** |

## Section 15 — S4b Switch story
| 15.1 | beh_switch_reason | What made you change? What happened? | Paragraph | — | No |
|---|---|---|---|---|---|

After section → Section 16.

---

## Section 16 — S5a Most annoying thing (unaided; its own page)
| 16.1 | pain_unaided_frustration | In a sentence or two: what is the most annoying thing about ordering food delivery for you right now? | Paragraph | — | No |
|---|---|---|---|---|---|

## Section 17 — S5b Frustrations
| # | Variable(s) | Text | Type | Options | Req | Notes |
|---|---|---|---|---|---|---|
| 17.1 | GRID: pain_fee_reconsider_freq, pain_bill_unreasonable_freq, beh_abandon_price_freq, pain_late_freq, pain_cancel_freq, att_check_1, pain_wrong_item_freq, pain_restaurant_unavailable_freq, pain_quality_freq | **Question title:** In the last 4 weeks, how often did each of these happen to you? | Multiple choice grid | **Columns (in order, never shuffled):** Never / Rarely / Sometimes / Often / Very often. **Rows (exact):** (1) The charges added at checkout (fees, packaging, etc.) made me reconsider or change my order (2) The final amount felt unreasonable for the food I ordered (3) I left without placing an order after seeing the final amount (4) My order arrived noticeably later than the time shown (5) My order was cancelled by the app or the restaurant (6) To show you are reading carefully, please select "Rarely" for this row (7) Items were missing or wrong (8) A restaurant I wanted was closed, unavailable or not listed (9) There was a problem with food quality or hygiene | Yes — **"Require a response in each row" On** | ⋮ → Shuffle row order **On** |
| 17.2 | pain_menu_markup_belief | How much do you agree: "Menu prices on delivery apps are usually higher than the price at the restaurant itself." | Multiple choice | Strongly disagree / Disagree / Neither / Agree / Strongly agree / Don't know | Yes | Use multiple choice (not linear scale) so "Don't know" is possible; no shuffle |
| 17.3 | pain_top_frustrations | Which of these frustrate you most about food delivery today? Select up to 3. | Checkboxes | Delivery fees / Platform, packaging or other charges / Menu prices higher than at the restaurant / Offers that don't really save money / Late delivery / Cancelled orders / Wrong or missing items / Getting refunds or help from support / The restaurant I want isn't available / Food quality or hygiene / Problems with the delivery partner (handover, calls, directions) / Nothing really frustrates me | Yes | Validation: at most 3. Shuffle **Off** in Forms (Forms can't pin the last option) → instead **reverse the order of options 1–11 in B2** to balance order effects; keep "Nothing really…" last in both |
| 17.4 | pain_incidents_3m | In the last 3 months, did any of these happen to you? Select all that apply. | Checkboxes | An order arrived more than 20 minutes late / An order was cancelled after I paid / I asked for a refund / A refund took more than 3 days or was refused / A support issue was not resolved / None of these | Yes | |
| 17.5 | pain_refund_outcome | How was your most recent refund request resolved? | Multiple choice | Full refund within 24 hours / Full refund, but slower / Partial refund or coupon only / Refused or no resolution / Still pending / **I haven't asked for a refund in the last 3 months** | Yes | ⚠ Forms can't branch on checkboxes, so this is shown to all with an added "haven't asked" option (code 0), which is recoded to missing when 17.4 lacks "I asked for a refund" |

---

## Section 18 — S6 Expectations
| # | Variable | Text | Type | Options | Req |
|---|---|---|---|---|---|
| 18.1 | exp_eta_max_lunch | For a weekday LUNCH order, what is the longest delivery time you would normally accept before choosing something else? | Multiple choice | 15 minutes / 20 minutes / 30 minutes / 40 minutes / 50 minutes / 60 minutes / More than 60 minutes / I don't order lunch | Yes |
| 18.2 | exp_eta_max_dinner | For a weekday DINNER order, what is the longest delivery time you would normally accept before choosing something else? | Multiple choice | 15 minutes / 20 minutes / 30 minutes / 40 minutes / 50 minutes / 60 minutes / More than 60 minutes / I don't order dinner | Yes |
| 18.3 | exp_late_tolerance | Out of 10 orders on an app, how many arriving 15+ minutes late would make you stop using that app? | Multiple choice | 1 / 2 / 3 / 4 / 5 or more / Lateness alone wouldn't make me stop | Yes |
| 18.4 | exp_fav_restaurant_needed | Before trying a new food-delivery app, how many of your usual restaurants would need to be on it? | Multiple choice | None — I'd happily try new places / A few / About half / Most / All or nearly all | Yes |
| 18.5 | exp_restaurant_types_needed | Which kinds of restaurants would a new app need to have for you to use it? Select all that apply. | Checkboxes | My specific favourite restaurants / Well-known chains / Good local restaurants near me / Budget options (meals under ₹200) / Premium restaurants / Healthy options / Late-night options / None of these matter much | Yes |
| 18.6 | exp_refund_expectation | If a delivery order goes wrong, which is closest to what you expect? | Multiple choice | Automatic refund within 24 hours, without having to argue / A refund within 2–3 days after I raise a complaint / A credit or coupon is fine / I don't expect much | Yes |
| 18.7 | beh_switch_savings_required | Think of a typical order of yours. How much lower would the final amount need to be, every time, for you to make a different app your main one? | Multiple choice | ₹10 / ₹20 / ₹30 / ₹50 / ₹75 / ₹100 or more / No amount — price alone wouldn't make me switch / Don't know | Yes |

After Section 18 → **Section 19 (Bill scenarios)**, see Part 2. Module order follows `bengaluru_experimental_modules_note.md` §4: the experimental modules (bill_s1/s2, fee ladder) come **before** the Ownly-status branch, so they aren't contaminated by Ownly-specific questions and the sequence matches Hyderabad.

---

## Section 38 — Not eligible / thank you (screen-out end)
**Title:** Thank you!
**Description:** "Thanks for your interest. This survey is for people aged 20–30 in Bengaluru who have ordered food delivery in the last 4 weeks, so we don't need any more answers from you. Your time is appreciated."
**After section → Submit form.** (Place it as the last section in the editor. Screen-out submissions are kept for the sample-flow table.)
