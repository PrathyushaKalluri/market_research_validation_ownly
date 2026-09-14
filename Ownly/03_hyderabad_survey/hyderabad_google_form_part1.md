# Hyderabad Survey — Google Form Build Spec, Part 1 (Settings, S0–S3, Screen-out)

**Source of truth:** `survey_variable_dictionary.csv`. The variable name in `[brackets]` is for the analysts. **Do not type it into the form.** Part 1b covers S4–S6, Part 2 covers S7–S14 and the version build checklist.

**Conventions**
- **Type** = the Google Forms question type.
- **Req** = the Required toggle.
- **Shuffle** = "Shuffle option order" (⋮ menu).
- **→** = "Go to section based on answer" (⋮ menu → enable).
- Sections are named exactly as below, e.g. `S1b Area`. Google shows them as "Section n of N".

**Why many screener pages have one question each:** Google Forms uses only one branching question per section reliably. So every question that branches sits last, or alone, in its own section.

---

## Form settings

| Setting | Value |
|---|---|
| Title | Food delivery in Hyderabad — a short student research survey |
| Settings → Responses → Collect email addresses | **Do not collect** |
| Limit to 1 response | **OFF** (it would force Google sign-in) |
| Allow response editing | OFF |
| Presentation → Show progress bar | **ON** |
| Shuffle question order | **OFF** |
| Confirmation message | "Thank you! Your answers have been recorded. Your completion code is **[VERSION CODE, e.g. HV1-26]**. If you'd like to enter the lucky draw or volunteer for an interview, use the links on the previous page — they are separate forms, so your survey answers stay anonymous." |
| Default for all questions | Required ON unless stated |
| Linked sheet | Create one per version: `HYD_V1_responses`, …; export daily to `08_clean_data/raw/` |

**Section order in the editor**

1. S0 Intro
2. S1a Age
3. S1b Area
4. S1c Orders
5. S1d Work conflict
6. S1e Repeat
7. S2a Occupation
8. S2b Student
9. S2c Working student
10. S2e Work
11. S2d Living
12. S3 Last order
13. S4a Habits
14. S4b Switch story
15. S5 Frustrations
16. S6 Expectations
17. S7 Bill scenarios
18. S8 Choice tasks
19. S9 New service
20. S10 Fee sections
21. S11a Reveal (V1/V2 only)
22. S11b Rapido
23. S12a Awareness
24. S12b Awareness detail
25. S12c Not tried
26. S13a Ownly first
27. S13c Lapse reasons
28. S13b Ownly experience
29. S14 Wrap-up
30. **SO Not eligible** (last section; "After section SO → Submit form")

---

## S0 Intro (Section 1)

**Section description (paste):**

> **Hi! Thanks for helping with our research.**
> We are an independent university student research team studying how young people in and around Gachibowli order food delivery. We are **not** working for, paid by or affiliated with any food-delivery company or restaurant.
> • Takes about **12–14 minutes**. • **Anonymous** — we do not ask for your name, phone number or email. • **Voluntary** — skip the survey or stop at any time; unfinished answers are not submitted. • Answers are used only for our course project, reported in summary form, and deleted within 12 months after the project ends. • Questions? Contact **[TEAM EMAIL PLACEHOLDER]**.
> Please answer about **your own real experience** — there are no right or wrong answers.

**Pre-filled fields** (Short answer, Req OFF; description: "Filled in automatically — please don't change"):

| # | Label | Variable |
|---|---|---|
| M1 | Version code (pre-filled — please don't change) | `[meta_form_version]` |
| M4 | Session code (pre-filled — please don't change) | `[meta_session_token]` |
| M5 | Start code (pre-filled — please don't change) | `[meta_start_ts]` |
| M6 | Source code (pre-filled — please don't change) | `[meta_source]` |
| M6b | Campaign code (pre-filled — please don't change) | `[meta_campaign]` — added because `link_randomizer.html` passes it |

M1: in each version copy, set the **pre-filled** link value. For direct QA links, type the version code manually. Response validation: Regular expression → matches → `^V[1-4]$`.

**Q1 `[meta_consent]`** · Multiple choice · Req · Shuffle OFF · **→ branching ON**
"I have read the information above, I am 18 or older, and I agree to take part."
- Yes, I agree → *Continue to next section*
- No → *SO Not eligible*

---

## S1a Age (Section 2)

**Q2 `[scr_age_band]`** · Multiple choice · Req · Shuffle OFF · → ON
"How old are you?"
- Under 20 → *SO Not eligible*
- 20–22 → *Continue*
- 23–25 → *Continue*
- 26–28 → *Continue*
- 29–30 → *Continue*
- Over 30 → *SO Not eligible*

## S1b Area (Section 3)

**Q3 `[scr_area]`** · Multiple choice · Req · Shuffle OFF · → ON
"Which area do you live, study or work in on most days? If more than one, choose where you usually get food delivered."
- Gachibowli → *Continue*
- Financial District / Nanakramguda → *Continue*
- Kondapur → *Continue*
- Madhapur / HITEC City → *Continue*
- Manikonda → *Continue*
- Narsingi / Kokapet → *Continue*
- Serilingampally / Chandanagar → *Continue*
- Tellapur / Nallagandla → *Continue*
- Somewhere else in Hyderabad → *SO Not eligible*
- I don't live, study or work in Hyderabad → *SO Not eligible*

## S1c Orders (Section 4)

**Q4 `[scr_orders_4wk]`** · Multiple choice · Req · Shuffle OFF · → ON
"In the last 4 weeks, about how many times did you order food for delivery through any app? Count each order once."
- None → *SO Not eligible*
- 1–3 times → *Continue*
- 4–7 times → *Continue*
- 8–15 times → *Continue*
- 16 or more times → *Continue*

## S1d Work conflict (Section 5)

**Q5 `[scr_coi]`** · Multiple choice · Req · → ON
"Do you work for a food-delivery, quick-commerce or restaurant-aggregator company, or in market research?"
- Yes → *SO Not eligible*
- No → *Continue*

## S1e Repeat (Section 6)

**Q6 `[scr_repeat]`** · Multiple choice · Req · → ON
"Have you already filled in this survey before (any version)?"
- Yes → *SO Not eligible*
- No → *Continue*

---

## S2a Occupation (Section 7)

**Q7 `[seg_occupation_raw]`** · Multiple choice · Req · Shuffle OFF · → ON
"Which best describes you right now?"
- Full-time student (undergraduate) → *S2b Student*
- Full-time student (postgraduate / PhD) → *S2b Student*
- Working full-time → *S2e Work*
- Studying and working (incl. internships / part-time jobs) → *S2c Working student*
- Other / between jobs → *S2d Living*

## S2b Student (Section 8) — after section → *S2d Living*

**Q8 `[dem_institution]`** · Multiple choice · Req · Shuffle OFF
"Where do you study?"
- IIIT Hyderabad
- University of Hyderabad
- ISB
- Another college near Gachibowli
- Elsewhere / online

## S2c Working student (Section 9) — after section → *S2e Work*

**Q8b `[dem_institution]`** — identical copy of Q8. It is duplicated so that working students can continue to the work question. It appears as a second column in the Sheet; merge both in cleaning.

## S2e Work (Section 10) — after section → *S2d Living*

**Q9 `[dem_work_sector]`** · Multiple choice · Req · Shuffle OFF
"Which best describes where you work?"
- IT / software product or services
- Global capability centre, consulting or finance
- Other corporate
- Startup
- Government / PSU
- Other

## S2d Living (Section 11) — after section → *S3 Last order*

**Q10 `[dem_living]`** · Multiple choice · Req
"Where do you currently live?"
- Hostel
- PG / co-living
- Shared flat with friends or flatmates
- With family
- Alone in a rented place
- Other

**Q11 `[dem_delivery_spend_month]`** · Multiple choice · Req
"Roughly how much do you personally spend on food delivery in a typical month?"
- Less than ₹1,000
- ₹1,000–2,499
- ₹2,500–4,999
- ₹5,000–9,999
- ₹10,000 or more
- Prefer not to say

**Q12 `[dem_gender]`** · Multiple choice · **Req OFF**
"What is your gender?"
- Woman
- Man
- Non-binary / other
- Prefer not to say

---

## S3 Last order (Section 12) — after section → *S4a Habits*

**Section description:** "A few questions about **your most recent** food-delivery order. If you can, open your order history to check."

**Q13 `[beh_unaided_apps]`** · Paragraph · Req
"Which food-delivery apps can you think of, even ones you don't use? Type as many as come to mind."
*Keep this question first on the page, before any app list appears.*

**Q14 `[beh_last_order_when]`** · Multiple choice · Req
"When did you place your most recent food-delivery order? If you can, check your order history."
- Today
- Yesterday
- 2–3 days ago
- 4–7 days ago
- 1–2 weeks ago
- 2–4 weeks ago
- More than 4 weeks ago

**Q15 `[beh_last_platform]`** · Multiple choice · Req · Shuffle OFF
"Which app or channel did you use for that order?"
- Swiggy
- Zomato
- Ownly app
- Rapido app (food section)
- Toing
- Magicpin
- EatSure
- Restaurant's own app / website / phone
- Other

**Q16 `[beh_last_meal]`** · Multiple choice · Req
"Which meal was it?"
- Breakfast
- Lunch
- Evening snack
- Dinner
- Late night (after 11 pm)

*Q17 `beh_last_daytype` and Q18 `beh_last_location` were **removed for length** (lead decision, 2026-09-14). Weekday/weekend is still measured by Q27. The question numbers are kept, so later numbers match the spec.*

**Q19 `[beh_last_people]`** · Multiple choice · Req
"How many people was that order for?"
- Just me
- 2 people
- 3–4 people
- 5 or more

**Q20 `[beh_last_food]`** · Multiple choice · Req
"What kind of food was it mainly?"
- Biryani
- South Indian
- North Indian
- Chinese / Asian
- Pizza / burgers / fast food
- Healthy / salads / bowls
- Desserts / beverages / cafe
- Other

**Q21 `[beh_last_restaurant_type]`** · Multiple choice · Req
"Which best describes the restaurant?"
- Well-known chain
- Local / independent restaurant
- Delivery-only brand / cloud kitchen
- Not sure

**Q22 `[beh_last_order_total]`** · Short answer · Req · **Response validation: Number → Between → 0 and 10000** · error text "Please enter the amount in rupees as a number, e.g. 280"
"What was the final amount you paid for that order, including all charges and after any discount? (₹, approximate is fine)"

**Q23 `[beh_last_total_recall]`** · Multiple choice · Req
"How sure are you about that amount?"
- I checked the app
- Fairly sure
- It's a rough guess

**Q24 `[beh_last_discount]`** · Multiple choice · Req
"Did that order use a discount or membership benefit?"
- Yes, a coupon or offer
- Yes, a membership benefit (e.g. free delivery)
- Both
- No
- Not sure

**Q25 `[beh_last_fees_noticed]`** · Checkboxes · Req · Shuffle OFF
"Which charges do you remember seeing on that bill? Select all that apply."
- Delivery fee
- Platform fee
- Packaging charge
- Small-order fee
- Rain / surge fee
- Taxes / GST
- Tip
- Donation
- None of these
- Don't remember

*Cleaning:* if "None of these" or "Don't remember" is ticked together with a charge, keep the charges and flag.

**Q26 `[dec_last_reasons]`** · Checkboxes · Req · **Shuffle ON** · **Response validation: Select at most → 3**
"Why did you use that app for that order? Select up to 3."
- Had the restaurant or dish I wanted
- Lowest final price
- A discount or offer
- Fastest delivery time
- It's the app I always use
- My membership benefits
- Reliable in my experience
- Easy to use
- Better support or refunds
- Good ratings / reviews
- Other

*Shuffle moves "Other" too. This is accepted: Forms cannot pin an option.*

---

## SO Not eligible (last section) — after section → **Submit form**

**Section description (paste):**

> **Thank you for your time!**
> This survey is for people aged **20–30** who live, study or work **in or around Gachibowli**, have ordered food delivery in the **last 4 weeks**, and don't work in food delivery or market research — or you've told us you have already taken part. Based on your answers, we don't need to ask you more questions. Please press **Submit** to finish. We really appreciate your help.

*Screen-out submissions are recorded, with blanks after the screener, and counted in the sample-flow table (`EX01_screen_fail`).*
