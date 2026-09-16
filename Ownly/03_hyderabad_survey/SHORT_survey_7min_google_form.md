> ⚠ **SUPERSEDED 2026-09-16 by `13_survey_v3_live/`.** This spec is Hyderabad-only and predates the canonical three-city routing. Reason: `_ops/decisions.md` D4. Kept for reference.

# SHORT Hyderabad Survey (~7 minutes): Google Forms Copy-Paste Spec

**Version:** 2026-09-14, for the 17 September deadline. Variable names match `survey_variable_dictionary.csv` where the item is the same. New items are marked **NEW**.

**Start sharing only after written ethics approval.**

## Form settings
- Collect email addresses: **OFF**
- Limit to 1 response: **OFF**
- Show progress bar: **ON**
- Shuffle question order: **OFF**
- Confirmation message: "Thank you! Your answers are anonymous. Please share this survey with friends aged 20–30 who order food in or around Gachibowli."

---

## Section 1: About this survey

**Description text:**
> We are a student research team at [University name] studying how people aged 20–30 in and around Gachibowli order food delivery. This is independent university research. We are not paid by or working with any food-delivery company. The survey takes about 7 minutes and is anonymous: we do not ask for your name, phone number or email. Taking part is voluntary, you can stop at any time, and you can skip optional questions. Answers are used only for our course project and deleted after grading. Questions: [team email]. This study was approved by [instructor name] on [date].

**Q1 `meta_consent`** — Multiple choice, required
- Yes, I agree to take part → *Continue to next section*
- No → *Go to section "Not eligible"*

## Section 2: Quick check

**Q2 `scr_age_band`** How old are you? — Multiple choice, required
- Under 20 → Not eligible
- 20–22
- 23–25
- 26–28
- 29–30
- Over 30 → Not eligible

**Q3 `scr_area`** Which area do you live, study or work in on most days? — Multiple choice, required
- Gachibowli
- Financial District / Nanakramguda
- Kondapur
- Madhapur / HITEC City
- Manikonda
- Narsingi / Kokapet
- Serilingampally / Chandanagar
- Tellapur / Nallagandla
- Somewhere else in Hyderabad → Not eligible
- I don't live, study or work in Hyderabad → Not eligible

**Q4 `scr_orders_4wk`** In the last 4 weeks, about how many times did you order food for delivery through any app? — Multiple choice, required
- None → Not eligible
- 1–3 times
- 4–7 times
- 8–15 times
- 16 or more times

*(Turn on "Go to section based on answer" for Q1–Q4. Put each on its own page: Section 2a, 2b, 2c.)*

## Section 3: About you

**Q5 `seg_occupation_raw`** Which best describes you right now? — Multiple choice, required
- Full-time student (undergraduate)
- Full-time student (postgraduate / PhD)
- Working full-time
- Studying and working (incl. internships / part-time jobs)
- Other / between jobs

**Q6 `dem_living`** Where do you currently live? — Multiple choice, required
- Hostel
- PG / co-living
- Shared flat with friends or flatmates
- With family
- Alone in a rented place
- Other

**Q7 `beh_unaided_apps`** Which food-delivery apps can you think of, even ones you don't use? — Short answer, required

## Section 4: Your last order

**Q8 `beh_last_platform`** Which app did you use for your most recent food-delivery order? — Multiple choice, required
- Swiggy
- Zomato
- Ownly app
- Rapido app (food section)
- Toing
- Magicpin
- Restaurant's own app / phone
- Other

**Q9 `beh_last_order_total`** What was the final amount you paid for that order, including all charges and after discounts? (₹; check your order history if you can) — Short answer, required
- Response validation: Number, between 0 and 10000

**Q10 `beh_last_meal`** Which meal was it? — Multiple choice, required
- Breakfast
- Lunch
- Evening snack
- Dinner
- Late night (after 11 pm)

## Section 5: Your ordering habits

**Q11 `beh_platforms_used_4wk`** Which apps have you ordered food delivery from in the last 4 weeks? Select all. — Checkboxes, required
- Swiggy
- Zomato
- Ownly app
- Rapido app (food section)
- Toing
- Magicpin
- Restaurant direct
- Other

**Q12 `beh_subscriptions`** Which food-delivery memberships do you have now? — Checkboxes, required
- Swiggy One (any plan)
- Zomato Gold
- Another food-delivery membership
- None
- Not sure

**Q13 `beh_offer_dependency`** Of your last 10 delivery orders, roughly how many used a coupon, offer or membership discount? — Multiple choice, required
- 0–1
- 2–4
- 5–7
- 8–10
- Don't know

**Q14 (grid)** In the last 4 weeks, how often did each of these happen to you? — Multiple-choice grid, require a response in each row; shuffle rows **ON**
- Columns: Never · Rarely · Sometimes · Often · Very often
- Rows:
  - `pain_fee_reconsider_freq` The charges added at checkout (fees, packaging, etc.) made me reconsider or change my order
  - `pain_bill_unreasonable_freq` The final amount felt unreasonable for the food I ordered
  - `beh_abandon_price_freq` I left without placing an order after seeing the final amount
  - `pain_late_freq` My order arrived noticeably later than the time shown
  - `pain_cancel_freq` My order was cancelled by the app or the restaurant
  - `att_check_1` To show you are reading carefully, please select "Rarely" for this row

**Q15 `pain_menu_markup_belief`** How much do you agree: "Menu prices on delivery apps are usually higher than the price at the restaurant itself." — Multiple choice, required
- Strongly disagree
- Disagree
- Neither
- Agree
- Strongly agree
- Don't know

**Q16 `pain_top_frustrations`** Which of these frustrate you most about food delivery today? Select up to 3. — Checkboxes, required; validation: *Select at most 3*; shuffle options **ON**
- Delivery fees
- Platform, packaging or other charges
- Menu prices higher than at the restaurant
- Offers that don't really save money
- Late delivery
- Cancelled orders
- Wrong or missing items
- Getting refunds or help from support
- The restaurant I want isn't available
- Food quality or hygiene
- Nothing really frustrates me

## Section 6: What matters to you

**Q17 `exp_eta_max_dinner`** For a weekday dinner order, what is the longest delivery time you'd normally accept? — Multiple choice, required
- 15 min
- 20 min
- 30 min
- 40 min
- 50 min
- 60 min
- More than 60 min
- I don't order dinner

**Q18 `exp_fav_restaurant_needed`** Before trying a new food-delivery app, how many of your usual restaurants would need to be on it? — Multiple choice, required
- None — I'd happily try new places
- A few
- About half
- Most
- All or nearly all

**Q19 `beh_switch_savings_required`** Think of a typical order of yours. How much lower would the final amount need to be, every time, for you to make a different app your main one? — Multiple choice, required
- ₹10
- ₹20
- ₹30
- ₹50
- ₹75
- ₹100 or more
- No amount — price alone wouldn't make me switch
- Don't know

## Section 7: Quick choices (hypothetical examples)

**Section description:** "These are made-up examples, not real bills from any app. Imagine everything else about the two apps is the same."

**Q20 `bill_s1`** Hypothetical example. Which bill would you rather pay? — Multiple choice, required

| | Bill 1 | Bill 2 |
|---|---|---|
| Food | ₹210 | ₹190 |
| Delivery fee | ₹35 | ₹25 |
| Platform fee | — | ₹15 |
| Packaging | — | ₹25 |
| Discount | — | −₹10 |
| **Total (incl. taxes)** | **₹245** | **₹245** |

- Bill 1
- Bill 2
- No real difference to me

*(Add the table as an image, or type it into the question description. Both totals are ₹245 on purpose.)*

**Q21 NEW `tradeoff_eta`** Hypothetical: same restaurant, same food. Which would you choose? — Multiple choice, required
- App A: ₹260 total, arrives in 30 minutes
- App B: ₹230 total, arrives in 45 minutes

**Q22 NEW `tradeoff_rel`** Hypothetical: same restaurant, same food, same delivery time. — Multiple choice, required
- App A: ₹260 total, late by 15+ minutes in about 1 of every 10 orders
- App B: ₹230 total, late by 15+ minutes in about 3 of every 10 orders

**Q23 NEW `tradeoff_rest`** Hypothetical: same food price level and delivery time. — Multiple choice, required
- App A: ₹260 total, has most of your usual restaurants
- App B: ₹230 total, has only a few of your usual restaurants

*(Shuffle option order **ON** for Q21–Q23, so the cheaper app isn't always shown second.)*

## Section 8: A food-delivery service

**Section description:**
> **Service X** is a food-delivery app where the food prices shown are the restaurant's own prices, and the checkout shows a single delivery charge instead of separate platform, packaging or other fees. Restaurants on it do not pay the app a commission on each order. The delivery time and the number of restaurants available vary by area.

**Q24 `bt_trial_intent`** If it were available where you are, how likely are you to try Service X for one of your next few orders? — Multiple choice, required
- Definitely not
- Probably not
- Not sure
- Probably
- Definitely

**Q25 NEW `wtp_max_fee_direct`** What is the highest delivery fee you would pay per order on Service X for a typical order of yours? — Multiple choice, required
- ₹0 — I'd only use it with free delivery
- ₹10
- ₹20
- ₹30
- ₹40
- ₹50
- ₹60 or more

**Q26 `bt_concern`** What, if anything, would stop you from trying it? — Paragraph, optional

## Section 9: About Ownly

**Section description:** "Service X describes **Ownly**, the food-delivery service from **Rapido** (the bike-taxi and auto app)."

**Q27 `br_trial_intent`** Now that you know it is Ownly from Rapido: how likely are you to try it for one of your next few orders? — Multiple choice, required
- Definitely not
- Probably not
- Not sure
- Probably
- Definitely

**Q28 `br_rapido_effect`** Does it being from Rapido make you more or less likely to try it? — Multiple choice, required
- Much less likely
- Somewhat less likely
- No difference
- Somewhat more likely
- Much more likely

**Q29 `own_aware_aided`** Before today, had you heard of Ownly? — Multiple choice, required
- Yes, clearly
- I think so
- No → *go to Section 12 (end)*

**Q30 `own_tried`** Have you ever placed an order on Ownly (Ownly app or inside the Rapido app)? — Multiple choice, required
- Yes → *Section 10*
- No, but I've opened or browsed it → *Section 11*
- No → *Section 11*

## Section 10: Ownly users

**Q31 `own_orders_4wk`** How many Ownly orders have you placed in the last 4 weeks? — Multiple choice, required
- None
- 1
- 2–3
- 4–7
- 8 or more

**Q32 `own_reliability_rating`** How often have your Ownly orders arrived on time? — Multiple choice, required
- Rarely
- Sometimes
- About half the time
- Mostly
- Always

**Q33 `own_perceived_savings`** Compared with ordering the same thing on the app you'd otherwise use, your most recent Ownly order was: — Multiple choice, required
- Much more expensive
- A bit more expensive
- About the same
- A bit cheaper
- Much cheaper
- I didn't compare

**Q34 `own_disappointment`** What, if anything, has disappointed you about Ownly? — Paragraph, optional

*→ After this section go to Section 12.*

## Section 11: Not tried yet

**Q35 `own_not_tried_reason`** What are the main reasons you haven't ordered on it? Select up to 3. — Checkboxes, required; validation: *Select at most 3*; shuffle **ON**
- Happy with my current app
- My usual restaurants weren't on it
- Not available at my location
- Didn't trust a new app yet
- Expected slow delivery
- Didn't see real savings
- No offers or discounts
- The payment method I use (e.g. cash on delivery or a meal card) isn't accepted
- Didn't know how to access it
- Haven't got round to it
- Other

## Section 12: Last question

**Q36 `meta_found_survey`** Where did you find this survey? — Multiple choice, required
- WhatsApp / Telegram group
- LinkedIn
- Reddit
- Instagram
- A friend or colleague sent it
- College or office group
- Other

→ Submit

## Section "Not eligible" (ends the form)

**Description:** "Thank you for your time! This survey is only for people aged 20–30 who live, study or work in or around Gachibowli and ordered food delivery in the last 4 weeks." → Submit

---

## New variables (add to the dictionary after the deadline)

| Variable | Codes | Hypothesis | Analysis |
|---|---|---|---|
| `tradeoff_eta` | 1 = App A (faster, ₹30 more) · 2 = App B (cheaper, 15 min slower) | H3.1 (simplified) | % choosing cheaper, with Wilson CI; students vs professionals |
| `tradeoff_rel` | 1 = more reliable, ₹30 more · 2 = cheaper, less reliable | H4.1 (simplified) | same |
| `tradeoff_rest` | 1 = most restaurants, ₹30 more · 2 = cheaper, few restaurants | H5.1 (simplified) | same |
| `wtp_max_fee_direct` | 0/10/20/30/40/50/60 | H8 (direct question; less rigorous than a ladder — say so) | Acceptance curve = % with max fee ≥ each level; median |

**Interpretation rule:** if > 50% (CI lower bound) choose the cheaper option in a trade-off, then ₹30 "buys" that compromise *in this hypothetical, for this sample*. Anything else is inconclusive or rejected. This is stated preference, not behaviour.
