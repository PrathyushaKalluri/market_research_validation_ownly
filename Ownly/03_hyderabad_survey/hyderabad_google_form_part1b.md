# Hyderabad Survey — Google Form Build Spec, Part 1b (S4–S6)

Conventions as in `hyderabad_google_form_part1.md`.

---

## S4a Habits (Section 13)

**Q27 `[beh_weekday_weekend]`** · Multiple choice · Req
"Are most of your delivery orders on weekdays or weekends?"
- Mostly weekdays
- About equal
- Mostly weekends

**Q28 `[beh_meal_occasions]`** · Checkboxes · Req · Shuffle OFF
"For which meals do you usually order delivery? Select all that apply."
- Breakfast
- Lunch
- Evening snacks
- Dinner
- Late night

**Q29 `[beh_platforms_used_4wk]`** · Checkboxes · Req · Shuffle OFF
"Which apps or channels have you ordered food delivery from in the last 4 weeks? Select all that apply."
- Swiggy
- Zomato
- Ownly app
- Rapido app (food section)
- Toing
- Magicpin
- EatSure
- Restaurant direct
- Other

**Q30 `[beh_platform_primary]`** · Multiple choice · Req · Shuffle OFF
"Which one do you use most?"
- Swiggy
- Zomato
- Ownly app
- Rapido app (food section)
- Toing
- Magicpin
- EatSure
- Restaurant direct
- Other

**Q31 `[beh_subscriptions]`** · Checkboxes · Req · Shuffle OFF
"Which food-delivery memberships do you have right now? Select all that apply."
- Swiggy One (any plan)
- Zomato Gold
- Another food-delivery membership
- None
- Not sure

**Q32 `[beh_offer_dependency]`** · Multiple choice · Req
"Think about your last 10 delivery orders. Roughly how many used a coupon, offer or membership discount?"
- 0–1
- 2–4
- 5–7
- 8–10
- Don't know

**Q33 `[dec_habit_lock]`** · Linear scale 1–5 · Req · labels: 1 = "Strongly disagree", 5 = "Strongly agree"
"How much do you agree: "I usually open the same app and order, without checking other apps.""

**Q34 `[beh_compare_freq]`** · Multiple choice · Req
"In the last 4 weeks, how often did you compare the price of the same order on two or more apps?"
- Never
- Rarely
- Sometimes
- Often
- Very often

**Q35 `[beh_switched_primary_12m]`** · Multiple choice · Req · **→ ON** · *must be the last question on this page*
"In the last 12 months, did you change which app you use most for food delivery?"
- Yes → *S4b Switch story*
- No → *S5 Frustrations*
- Not sure → *S5 Frustrations*

## S4b Switch story (Section 14) — after section → *S5 Frustrations*

**Q36 `[beh_switch_reason]`** · Paragraph · **Req OFF**
"What made you change? What happened?"

---

## S5 Frustrations (Section 15) — after section → *S6 Expectations*

**Q37 `[pain_unaided_frustration]`** · Paragraph · **Req OFF** · *keep first on the page, before the grid and list*
"In a sentence or two: what is the most annoying thing about ordering food delivery for you right now?"

**Q38** · **Multiple-choice grid** · Req ON ("Require a response in each row") · Shuffle **row** order ON (⋮ menu). Column order never changes.

- **Question title:** "In the last 4 weeks, how often did each of these happen to you?"
- **Columns:** Never | Rarely | Sometimes | Often | Very often

| Row # | Row text (paste exactly) | Variable |
|---|---|---|
| 38.1 | The charges added at checkout (fees, packaging, etc.) made me reconsider or change my order | `[pain_fee_reconsider_freq]` |
| 38.2 | The final amount felt unreasonable for the food I ordered | `[pain_bill_unreasonable_freq]` |
| 38.3 | I left without placing an order after seeing the final amount | `[beh_abandon_price_freq]` |
| 38.4 | My order arrived noticeably later than the time shown | `[pain_late_freq]` |
| 38.5 | My order was cancelled by the app or the restaurant | `[pain_cancel_freq]` |
| 38.6 | To show you are reading carefully, please select "Rarely" for this row | `[att_check_1]` (correct = Rarely) |
| 38.7 | Items were missing or wrong | `[pain_wrong_item_freq]` |
| 38.8 | A restaurant I wanted was closed, unavailable or not listed | `[pain_restaurant_unavailable_freq]` |
| 38.9 | There was a problem with food quality or hygiene | `[pain_quality_freq]` |

*Sheet columns appear as `Q38 [row text]`; rename them to the variables in ingest. Do not enable "Limit to one response per column."*

**Q39 `[pain_menu_markup_belief]`** · **Multiple choice** (not Linear scale, because a "Don't know" option is needed) · Req · Shuffle OFF
"How much do you agree: "Menu prices on delivery apps are usually higher than the price at the restaurant itself.""
- Strongly disagree
- Disagree
- Neither agree nor disagree
- Agree
- Strongly agree
- Don't know

**Q40 `[pain_top_frustrations]`** · Checkboxes · Req · **Shuffle ON** · **Validation: Select at most → 3**
"Which of these frustrate you most about food delivery today? Select up to 3."
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
- Problems with the delivery partner (handover, calls, directions)
- Nothing really frustrates me

*Shuffle also moves the last option; accepted. Cleaning: if "Nothing really frustrates me" is ticked with other options, keep the others and flag.*

**Q41 `[pain_incidents_3m]`** · Checkboxes · Req · Shuffle OFF
"In the last 3 months, did any of these happen to you? Select all that apply."
- An order arrived more than 20 minutes late
- An order was cancelled after I paid
- I asked for a refund
- A refund took more than 3 days or was refused
- A support issue was not resolved
- None of these

**Q42 `[pain_refund_outcome]`** · Multiple choice · Req · Shuffle OFF
"How was your most recent refund request resolved?"
- Full refund within 24 hours
- Full refund, but slower
- Partial refund or coupon only
- Refused or no resolution
- Still pending
- **I haven't asked for a refund in the last 3 months** *(added; see note)*

> **Build note (deviation from the dictionary's skip logic):** Google Forms cannot branch on a Checkboxes answer (Q41). So Q42 is always shown, with an added option: "I haven't asked for a refund in the last 3 months" (code 0). Cleaning checks consistency with Q41 "I asked for a refund". This is recorded in `bias_audit.md` and in the dictionary.

---

## S6 Expectations (Section 16) — after section → *S7 Bill scenarios*

**Q43 `[exp_eta_max_lunch]`** · Multiple choice · Req · Shuffle OFF
"For a weekday LUNCH order, what is the longest delivery time you would normally accept before choosing something else?"
- 15 minutes
- 20 minutes
- 30 minutes
- 40 minutes
- 50 minutes
- 60 minutes
- More than 60 minutes
- I don't order lunch

**Q44 `[exp_eta_max_dinner]`** · Multiple choice · Req · Shuffle OFF
"For a weekday DINNER order, what is the longest delivery time you would normally accept before choosing something else?"
- 15 minutes
- 20 minutes
- 30 minutes
- 40 minutes
- 50 minutes
- 60 minutes
- More than 60 minutes
- I don't order dinner

**Q45 `[exp_late_tolerance]`** · Multiple choice · Req · Shuffle OFF
"Out of 10 orders on an app, how many arriving 15+ minutes late would make you stop using that app?"
- 1
- 2
- 3
- 4
- 5 or more
- Lateness alone wouldn't make me stop

**Q46 `[exp_fav_restaurant_needed]`** · Multiple choice · Req · Shuffle OFF
"Before trying a new food-delivery app, how many of your usual restaurants would need to be on it?"
- None — I'd happily try new places
- A few
- About half
- Most
- All or nearly all

**Q47 `[exp_restaurant_types_needed]`** · Checkboxes · Req · **Shuffle ON**
"Which kinds of restaurants would a new app need to have for you to use it? Select all that apply."
- My specific favourite restaurants
- Well-known chains
- Good local restaurants near me
- Budget options (meals under ₹200)
- Premium restaurants
- Healthy options
- Late-night options
- None of these matter much

**Q48 `[exp_refund_expectation]`** · Multiple choice · Req · Shuffle OFF
"If a delivery order goes wrong, which is closest to what you expect?"
- Automatic refund within 24 hours, without having to argue
- A refund within 2–3 days after I raise a complaint
- A credit or coupon is fine
- I don't expect much

**Q49 `[exp_instructions_importance]`** · Linear scale 1–5 · Req · labels: 1 = "Not important", 5 = "Extremely important"
"How important is it that the delivery partner follows your delivery instructions (e.g. gate, hostel desk, calling first)?"

**Q50 `[exp_quality_concern_cheap]`** · Linear scale 1–5 · Req · labels: 1 = "Strongly disagree", 5 = "Strongly agree"
"How much do you agree: "I worry about food quality or hygiene when a delivery option is cheaper than usual.""

**Q51 `[beh_switch_savings_required]`** · Multiple choice · Req · Shuffle OFF
"Think of a typical order of yours. How much lower would the final amount need to be, every time, for you to make a different app your main one?"
- ₹10
- ₹20
- ₹30
- ₹50
- ₹75
- ₹100 or more
- No amount — price alone wouldn't make me switch
- Don't know
