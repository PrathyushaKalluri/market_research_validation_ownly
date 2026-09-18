# Hyderabad (Gachibowli) Survey v3: FINAL, Ready to Build

> ⚠️ **SUPERSEDED on 2026-09-15 by `hyderabad_survey_v4_final.md`.** v4 is redesigned so every question feeds a formula-sheet metric. Keep this file for reference only; do not build from it.

**Version:** 2026-09-15 (final iteration). This replaces `hyderabad_google_form_part1/1b/2/2b.md` (103 questions) and `SHORT_survey_7min_google_form.md` (36 questions) for fieldwork. The old files stay in the repo as the "full design" reference.

**Problem statement (agreed):** Will Ownly's Bengaluru pitch ("pay the restaurant's price, no hidden fees") pull 20–30-year-old students and working professionals in and around Gachibowli away from Swiggy/Zomato? If not, what must Ownly change?

**What the survey must deliver:**
1. How strong the pain is with today's apps
2. What locks people in
3. What they'd trade for a lower bill
4. **Where each person sits in Ownly's funnel, and what Ownly should do about it:** what to lead with, what to fix, which first order to target, and what brings people back

**Length:**
- Everyone: 22 required questions (3 are one-tap eligibility checks), about **4 minutes** on a phone
- Ownly users: 8–9 more questions, about 5–6 minutes
- Confirm timings in the pilot (§6)

---

## 1. How this survey was designed (research → decisions)

| Principle | Source | What we did |
|---|---|---|
| The longer a survey says it will take, the fewer people start and finish it. Answer quality also falls late in long forms. | Galesic & Bosnjak (2009), *Public Opinion Quarterly* | 22 core questions. The most important items come early; optional text is kept to one question. |
| Even paid panel members call 10–15 min "ideal". Unpaid WhatsApp respondents tolerate far less. | Revilla & Höhne (2020) | Target is about 4 minutes, and the messages state it honestly. |
| Ask about **specific past behaviour**, not "would you" or opinions. "I would definitely buy that" is the most dangerous fluff. | *The Mom Test* (Fitzpatrick) | Anchored on **your last order** and **counts in the last 4 weeks**. Ownly users are asked about their **first order and what actually happened**. |
| Asking "would you use it?" about a product people don't understand produces noise. People are bad at predicting their own use. | *The Right It* (Savoia), "Thoughtland"; your feedback on v3 | **No "how likely are you to order" question.** People who haven't used Ownly first read a short factual description. Then they choose **one trigger, one worry and one first-order type**, which are forced choices Ownly can act on. |
| Stated willingness-to-pay overstates real payment (median 1.35×). Choice formats reduce the bias. | Murphy et al. (2005) meta-analysis | Trade-offs are A-vs-B choices. The fee answer is treated as an upper bound. |
| Vague frequency words ("often") mean different things to different people. | Schwarz, on response alternatives | Counts (0 / 1 / 2–3 / 4+) instead of "rarely/often". |
| One idea per question; wording and order effects are real. | Pew Research Center | No double-barrelled items. Ownly is **not named until Q23**, so the brand can't colour earlier answers. Unordered options are shuffled. |
| About 10–12% of respondents answer carelessly. Use several detection methods. | Meade & Craig (2012), *Psychological Methods* | 2 traps plus 4 consistency checks (§4). |
| A fake brand among real ones catches over-claiming. | Paulhus over-claiming technique | "Biteway" (not a real food app) sits in the app list. |
| Branch by **funnel stage** (never heard / heard / looked / ordered). Each stage has a different drop-off reason. | Funnel logic from the course syllabus (Unit 4–6); `11_insights/decision_framework_and_scorecard.md` | Q23 routes to 4 different Ownly paths. Ownly users branch again on whether their first order went wrong. |
| Product–market fit: if ≥ 40% of users would be "very disappointed" to lose the product, that's a strong signal. | Sean Ellis test (*Testing Business Ideas*, validation survey card) | D8, asked to Ownly users. |

*"Behavioral Research and Experimental Design" was not in the project folder. The survey-methods sources above were used instead.*

### What the Ownly questions are built on (evidence, not guesses)

| Evidence (CONSUMER-GENERATED unless stated; Bengaluru-heavy, self-selected) | Where it appears in this form |
|---|---|
| Loudest harm is **after the order**: 46 fulfilment failures and 29 support/refund failures, vs 19 price wins, among 108 first-hand incidents. Support (21/37) and refunds (16/37) dominate app reviews. | A2/B4 worry options; D4 first-order outcome → D5 whether it was fixed |
| The saving depends on the restaurant and on coupons: 6 bill comparisons favour Ownly, 7 say Swiggy/Zomato coupons or card offers erase the gap. | C2 "a coupon on my usual app made it cheaper"; D6 size of saving; D7 "better coupon elsewhere" |
| **Price-durability doubt:** 37 items expect prices or fees to rise later ("enjoy while it lasts"). | Q22 (everyone); A2/B4 "low prices won't last" |
| First-order experience looks pivotal: several first-order failures led to deleting the app. | D4 → D5 branch |
| "Small orders Ownly, large orders Swiggy with card offers". Large orders feel riskier; small carts get cancelled. | Q7 people on the order; A3 first order type; D7 "bigger or group orders" |
| Late-night false "delivered" reports | D4 option; D7 "late at night"; A3 |
| **No cash on delivery, no meal-card (Pluxee) payment** — relevant for salaried users | Trigger option (A1/B3/C3); C2 "couldn't pay the way I wanted"; D9 |
| Many prefer a clearly labelled fee over "free delivery" with inflated menus (9 items) | Q21 bill style |
| Rapido brand cuts both ways ("Rapido DNA… don't expect help" vs "does ok without excessive charges") | A2/B4 "trusting a Rapido service with my food" |
| Hyderabad: an Ownly staff post says "officially LIVE in Hyderabad" (≈ 11 Sep 2026). A festival "Mooshak on Wheels" van campaign is on Hyderabad roads (MEDIA REPORT, Sep 2026). Current first-order offer: "up to ₹100 off" (referral post, Sep 2026). | B1/C1 where heard; trigger "₹100 off"; **verify in the app before launch (§6)** |

Sources: `05_review_mining/voc_synthesis_pre_fieldwork.md`, `05_review_mining/social/social_analysis.md`, `05_review_mining/app_stores/analysis_tables.md`, `01_secondary_research/`.

---

## 2. What each question is for

| Q | Measures | Decision it feeds | Hypothesis |
|---|---|---|---|
| 1–4 | Eligibility; student vs professional; order frequency | Target segment | H6, H1.6 |
| 5–9 | Last order: app, amount, group size, discount, why that app | Lock-in; basket size; small-vs-group occasion | H1.5, H6.4, RQ2 |
| 10 | Apps used in 3 months (multi-homing) + **trap** | Is switching low-friction? | H9.4, H11.3 |
| 11 | Membership | Lock-in | H9.4, AS14 |
| 12 | Times the checkout total made them change or drop an order | Is price pain real behaviour? | H1.1, H1.4 |
| 13 | Single biggest annoyance | Lead with price, reliability or selection? | H1.2 |
| 14 | Last annoying experience (optional) | Stories for the deck; interview leads | — |
| 15 | Saving needed to make a new app your main one | Is Ownly's real saving big enough? (vs the audit) | **H2.3** |
| 16–19 | ₹30 cheaper vs slower / less reliable / fewer restaurants, + **trap** | Guardrails Ownly can't break | H3.1, H4.1, H5.1 |
| 20 | Max delivery fee on a no-extra-fees app | Fee level | H8.1 |
| 21 | "Free delivery + higher menu" vs "restaurant price + clear fee" | How Ownly should show its price | H2.2 |
| 22 | Expect a new app's low prices to last? | Does Ownly need a "price promise"? | AS24 |
| 23 | **Ownly funnel stage** (4 paths) | Where the funnel leaks | H11.3 |
| A1–A3 | Never heard: trigger, worry, first order type | What to lead with; first occasion to target | H2.5 (replaced), H10 |
| B1–B4 | Heard, never opened: channel, reason, trigger, worry | Awareness isn't converting: why? | AS12, H11.3 |
| C1–C3 | Looked, didn't order: channel, what stopped them, trigger | Conversion leak at browse/checkout | AS9, AS25 |
| D1–D9 | Ordered: city, repeat, first-order trigger, first-order outcome → fixed?, saving, when they still use incumbents, Sean Ellis, one change | Retention levers; PMF signal | H12.1, H12.2, H12.4, H9 |
| 24 | Interview volunteer (optional) | Qualitative follow-up | — |

---

## 3. The form: copy-paste build spec

### Form settings

| Setting | Value |
|---|---|
| Form title | **How young Hyderabad orders food: 4-minute student survey** |
| Form description (top of form) | *Leave blank. The intro is on Page 1, so it shows as the first screen on phones.* |
| Collect email addresses | OFF |
| Limit to 1 response | OFF (turning it on forces Google sign-in, and people drop off) |
| Show progress bar | ON |
| Shuffle question order | OFF |
| All questions | Required unless marked *Optional* |
| Confirmation message | "Done! Thank you 🙏 Your answers really help our research. If you know someone aged 20–30 who orders food around Gachibowli, HITEC City or Financial District, please forward them the link. More answers make the results fairer." |

**Branching rule:** Google Forms reliably uses only **one** "Go to section based on answer" question per page. It must be the **last** question on that page. The layout below follows this.

**Page map:**
```
P1 Age ─► P2 Area ─► P3 About you ─► P4 Last order ─► P5 Your apps ─► P6 Quick choices ─► P7 Pricing ─► P8 Ownly
                                                                                                         │
             ┌──────────────────────────┬──────────────────────────────┬────────────────────────────┤
             ▼                          ▼                              ▼                            ▼
       P9A Never heard           P9B Heard, not opened         P9C Looked, didn't order       P9D Ordered
             │                          │                              │                     D4 first order?
             │                          │                              │                   ┌────────┴────────┐
             │                          │                              │               problem           smooth
             │                          │                              │                   ▼                 │
             │                          │                              │             P9D-fix (D5)            │
             │                          │                              │                   └───────┬─────────┘
             │                          │                              │                           ▼
             │                          │                              │                     P9D-more (D6–D9)
             └──────────────────────────┴──────────────┬───────────────┴───────────────────────────┘
                                                        ▼
                                                P10 Last one ─► Submit
(P1, P2, P3 "not eligible" answers ─► PX Not eligible ─► Submit)
```

---

### Page 1: Welcome

**Page description (paste exactly):**
> **Hi! Thanks for opening this 🙂**
> We're Product Management students studying **how people aged 20–30 around Gachibowli choose food delivery apps**: what they like, what annoys them, and what would make them switch.
>
> **What to expect**
> • About **4 minutes**, almost all taps. One optional question lets you type.
> • **Anonymous**: we don't ask your name or email.
> • This is independent student research. We don't work for any food app or restaurant.
>
> **One request:** please answer based on **what you actually do**, not what sounds right. There are no right or wrong answers. "I don't know" and "none" are useful answers too.

**Q1. How old are you?** · Multiple choice · Go to section based on answer
- Under 20 → *PX Not eligible*
- 20–22 → Continue
- 23–25 → Continue
- 26–28 → Continue
- 29–30 → Continue
- Over 30 → *PX Not eligible*

---

### Page 2

**Q2. Where do you live, work or study on most days?** · Multiple choice · Go to section based on answer
*(Description: "If more than one, pick where you usually get food delivered.")*
- Gachibowli
- Financial District / Nanakramguda
- Kondapur
- Madhapur / HITEC City
- Manikonda
- Narsingi / Kokapet
- Serilingampally / Nallagandla / Tellapur
- Another part of Hyderabad → *PX Not eligible*
- Not in Hyderabad → *PX Not eligible*

---

### Page 3: About you

**Q3. Which best describes you right now?** · Multiple choice
- Student (undergraduate)
- Student (postgraduate / PhD)
- Working full-time
- Studying and working (internship / part-time)
- Looking for a job
- Other

**Q4. In the last 4 weeks, how many times did you order food online for delivery?** · Multiple choice · Go to section based on answer
*(Description: "Any app. Count each order once.")*
- None → *PX Not eligible*
- 1–3 times → Continue
- 4–7 times → Continue
- 8–15 times → Continue
- 16 or more times → Continue

---

### Page 4: Your last order

**Page description:** "Think about the **last time** you ordered food online. Opening your order history for 10 seconds makes your answers much more accurate."

**Q5. Which app did you use for that order?** · Multiple choice
- Swiggy
- Zomato
- Ownly (or food inside the Rapido app)
- Toing
- Magicpin
- EatSure
- Directly from the restaurant (call / WhatsApp / its own app)
- Other

**Q6. Roughly how much did you pay in total?** · Multiple choice
*(Description: "Final amount after discounts, including all fees.")*
- Under ₹150
- ₹150–249
- ₹250–399
- ₹400–599
- ₹600 or more
- Don't remember

**Q7. How many people was that order for?** · Multiple choice
- Just me
- 2 people
- 3 or more people

**Q8. Did that order use a discount?** · Multiple choice
*(Description: "A coupon, an offer, a bank/card offer, or a membership benefit like free delivery.")*
- Yes, a coupon, offer or card offer
- Yes, a membership benefit
- Both
- No
- Not sure

**Q9. Why did you use that app for that order? Pick up to 2.** · Checkboxes · Shuffle options ON · Response validation: *Select at most 2*
- It had the restaurant or dish I wanted
- Lowest total price
- A coupon or offer
- My membership (free delivery etc.)
- Fastest delivery
- It's the app I always use
- It's usually on time
- Other

---

### Page 5: Your food apps

**Q10. Which of these have you ordered food from in the last 3 months? Select all that apply.** · Checkboxes · Shuffle options ON
- Swiggy
- Zomato
- Ownly (or food inside the Rapido app)
- Toing
- Magicpin
- EatSure
- Biteway ⚠️ *TRAP: not a real app. Don't remove it or explain it to anyone.*
- Directly from a restaurant

**Q11. Do you have a food delivery membership right now?** · Multiple choice
- Swiggy One
- Zomato Gold
- Both
- Neither
- Not sure

**Q12. In the last 4 weeks, how many times did the final amount at checkout make you change your order or not order at all?** · Multiple choice
- 0 times
- Once
- 2–3 times
- 4 or more times
- Don't remember

**Q13. Which ONE of these bothers you most when ordering food online?** · Multiple choice · Shuffle options ON
- Extra charges (delivery, platform, packaging fees)
- Food costs more on the app than at the restaurant
- Late delivery
- Orders getting cancelled
- Wrong or missing items
- Food quality
- Getting a refund or help from support
- The restaurant I want isn't on the app
- Offers that don't really save money
- Nothing really bothers me

**Q14. *Optional:* Think of the last time ordering food online annoyed you. What happened?** · Paragraph · Not required
*(Description: "One or two lines is perfect. Example: 'Paid ₹90 in fees on a ₹200 biryani, so I cancelled.' or 'Order was 40 min late and support just closed the chat.'")*

---

### Page 6: Quick choices

**Page description (paste):**
> These are **made-up examples**. In each one, **everything else is the same**: same restaurant, same food, same quality. Only what's shown is different.
> Pick what you would **really** do on a normal day, not what sounds smart.
> "Late" means 15+ minutes later than promised.

**Q15. Your usual order costs ₹250 in total on your usual app. Another app has the same restaurant, same food and same delivery time. How much cheaper would it need to be, every time, for you to make it your main food app?** · Multiple choice · Keep this order
- ₹10–20 cheaper
- ₹30–40 cheaper
- ₹50–70 cheaper
- ₹80 or more cheaper
- Price alone wouldn't make me switch

**Q16. Which would you order from?** · Multiple choice · Shuffle options ON
- ₹260 · arrives in 30 min
- ₹230 · arrives in 45 min

**Q17. Which would you order from?** · Multiple choice · Shuffle options ON
- ₹260 · late about 1 in 10 orders
- ₹230 · late about 3 in 10 orders

**Q18. Which would you order from?** · Multiple choice · Shuffle options ON ⚠️ *TRAP: one option is better on both counts*
- ₹230 · arrives in 30 min
- ₹260 · arrives in 45 min

**Q19. For your everyday orders, which app would you rather use?** · Multiple choice · Shuffle options ON
- ₹260 · has most of your usual restaurants
- ₹230 · has only a few of your usual restaurants

---

### Page 7: How prices are shown

**Q20. Imagine an app where food costs the same as at the restaurant, with no platform or packaging fees, only a delivery fee. For a ₹220 meal, what's the highest delivery fee you'd pay before ordering elsewhere?** · Multiple choice · Keep this order
- ₹0 (only if delivery is free)
- ₹10
- ₹20
- ₹30
- ₹40
- ₹50 or more

**Q21. Two apps. Same food, and the total you pay is exactly the same. Which way of showing the price would you trust more?** · Multiple choice · Shuffle the first two options ON
- "Free delivery", but menu prices are higher than at the restaurant
- Menu at the restaurant's own price, plus a clearly shown delivery fee
- No difference to me

**Q22. When a new food app starts with lower prices than the big apps, what do you think usually happens within a year?** · Multiple choice
- Prices stay low
- Prices slowly rise to match the big apps
- The app shuts down or gets worse
- Hard to say

---

### Page 8: One app in particular

**Q23. Ownly is a food delivery app by Rapido (the bike-taxi and auto app). Before today, which of these is true for you?** · Multiple choice · Go to section based on answer
- I hadn't heard of Ownly → *P9A*
- I'd heard of it, but never opened it → *P9B*
- I opened or browsed it, but didn't order → *P9C*
- I've ordered on Ownly → *P9D*

---

### P9A: New to Ownly (after section → *P10 Last one*)

**Page description (paste exactly; neutral and factual, no selling):**
> **About Ownly (so you know what we mean):**
> • A food delivery app from Rapido, available in Hyderabad since around September 2026 and also inside the Rapido app.
> • Restaurants pay Ownly no commission, so menu prices are meant to match the restaurant's own prices.
> • No platform fee, packaging fee or surge fee. [DELIVERY FEE LINE — fill in after the in-app check, e.g. "A delivery fee is shown before you pay" or "Delivery is currently free"]
> • It's new in Hyderabad, so the list of restaurants is still growing.
>
> There are no right answers. We want to know what would matter **to you**.

**A1. Which ONE thing would most make you try Ownly for an order?** · Multiple choice · Shuffle options ON
- [CURRENT OFFER, e.g. "₹100 off my first order"]
- My usual restaurants being on it
- Seeing it's cheaper than Swiggy/Zomato for the same order
- A promise of a quick refund if an order goes wrong
- A friend telling me it works well
- Paying by cash on delivery or meal card (Pluxee / Zeta)
- Nothing, I'm happy with my current app

**A2. Which ONE worry would most stop you from trying it?** · Multiple choice · Shuffle options ON
- Late or failed deliveries
- Getting a refund or help if something goes wrong
- My usual restaurants not being there
- The low prices won't last
- Food quality
- Trusting a Rapido service with my food
- No real worry

**A3. If you did try it, what would your first order most likely be?** · Multiple choice
- A quick, cheap meal just for me
- Lunch at college or work
- Dinner at home
- Late-night food (after 11 pm)
- A bigger order for friends or family
- I wouldn't try it

---

### P9B: Heard of Ownly, never opened it (after section → *P10 Last one*)

**B1. Where did you first hear about Ownly?** · Multiple choice
- Inside the Rapido app
- Instagram / YouTube
- Friends, classmates or colleagues
- Hoardings, posters or the festival van campaign
- News, LinkedIn or Reddit
- Don't remember

**B2. What's the MAIN reason you haven't opened it yet?** · Multiple choice · Shuffle options ON
- I'm happy with my current app or membership
- I don't trust a new app yet
- I heard bad things about its delivery or support
- I don't think it's really cheaper
- Not sure it delivers to my area
- I don't want another app on my phone
- Just haven't got around to it

**B3. Which ONE thing would most make you try Ownly for an order?** · Multiple choice · Shuffle options ON
*(Same options as A1. Copy the question exactly.)*

**B4. Which ONE worry would most stop you from trying it?** · Multiple choice · Shuffle options ON
*(Same options as A2. Copy the question exactly.)*

---

### P9C: Looked at Ownly, didn't order (after section → *P10 Last one*)

**C1. Where did you first hear about Ownly?** · Multiple choice
*(Same options as B1.)*

**C2. When you looked, what MAINLY stopped you from ordering?** · Multiple choice · Shuffle options ON
- My restaurants weren't there
- Prices weren't lower than my usual app
- A coupon on my usual app made that cheaper
- It didn't deliver to my address
- The delivery time looked too long
- I couldn't pay the way I wanted
- I was just looking around
- Other

**C3. Which ONE thing would most make you order on Ownly next time?** · Multiple choice · Shuffle options ON
*(Same options as A1.)*

---

### P9D: Ownly users (page 1 of 3)

**D1. Where have you ordered on Ownly?** · Multiple choice
- Hyderabad only
- Bengaluru only
- Both

**D2. How many times have you ordered on Ownly in the last 4 weeks?** · Multiple choice
- 0 times
- Once
- 2–3 times
- 4 or more times

**D3. What MAINLY made you place your first Ownly order?** · Multiple choice · Shuffle options ON
- A first-order offer or referral discount
- It showed a lower price than my usual app
- No platform or packaging fees
- A friend recommended it
- I saw it inside the Rapido app
- A restaurant I like was on it
- Just curious

**D4. How did your FIRST Ownly order go?** · Multiple choice · Go to section based on answer
- Smooth, no problems → *P9D-more*
- Arrived late → *P9D-fix*
- Got cancelled → *P9D-fix*
- Wrong or missing items → *P9D-fix*
- Marked "delivered" but never reached me → *P9D-fix*
- Food quality problem → *P9D-fix*

### P9D-fix: When the first order went wrong (after section → *P9D-more*)

**D5. Did it get sorted?** · Multiple choice
- Yes, a full refund or fix within a day
- Sorted, but slowly or only partly
- No, it wasn't sorted
- I didn't contact support

### P9D-more: Ownly users, continued (after section → *P10 Last one*)

**D6. Compared with Swiggy/Zomato, your most recent Ownly order was:** · Multiple choice
- Cheaper by ₹50 or more
- Cheaper by less than ₹50
- About the same
- More expensive
- I didn't compare

**D7. When do you still choose Swiggy/Zomato instead of Ownly? Pick the MAIN one.** · Multiple choice · Shuffle options ON
- The restaurant isn't on Ownly
- A better coupon or card offer there
- I need it faster
- Bigger or group orders
- Late at night
- After a bad Ownly experience
- Out of habit
- I don't. I use Ownly for all my orders

**D8. How would you feel if you could no longer use Ownly?** · Multiple choice
- Very disappointed
- Somewhat disappointed
- Not disappointed

**D9. What ONE change would make you order more on Ownly?** · Multiple choice · Shuffle options ON
- More restaurants
- Faster delivery
- More reliable, on-time delivery
- Quicker refunds and support
- A bigger price gap vs other apps
- More offers and coupons
- Cash on delivery or meal-card payment
- A membership with extra benefits

---

### P10: Last one (after section → *Submit*)

**Page description:** "That's it, thank you! 🙏 One last optional question."

**Q24. *Optional:* Can we message you for a 10-minute chat about how you order food?** · Short answer · Not required
*(Description: "Leave your WhatsApp number if yes. It's only used to contact you for the chat and is kept separately from your answers.")*

---

### PX: Not eligible (last page; after section → *Submit*)

**Page description:**
> Thanks so much for your time! 🙏 This survey is only for people **aged 20–30** who live, work or study **around Gachibowli** and **ordered food online in the last 4 weeks**. Please press **Submit**.
> If you know someone who fits, please forward them the link. It really helps.

---

## 4. False-positive checks (fix these rules BEFORE seeing results)

| Check | Flag rule | Points |
|---|---|---|
| **T1 Fake app** | Ticked "Biteway" in Q10 | **2** |
| **T2 Logic trap** | Q18 = "₹260 · arrives in 45 min" | 1 |
| **C1 Last app mismatch** | Q5 app not ticked in Q10 (ignore "Other"; "Directly from the restaurant" = "Directly from a restaurant") | 1 |
| **C2 Ownly mismatch** | Any of: Q5 or Q10 includes Ownly but Q23 ≠ "ordered"; **or** Q23 = "ordered" and D1 ≠ "Bengaluru only" and D2 ≠ "0 times" but Q10 has no Ownly | 1 |
| **C3 Impossible count** | D2 = "4 or more" but Q4 = "1–3 times" | 1 |
| **C4 Contradiction** | A3 = "I wouldn't try it" but A1 ≠ "Nothing, I'm happy…" **and** A2 = "No real worry" | 1 |
| **C5 Junk text** | Q14 is gibberish or copy-pasted nonsense | 1 |
| **D1 Duplicate** | Identical answers on every required question, submitted within 10 minutes | keep first only |

**Exclusion rule:** exclude responses with **2 or more points**. Report headline numbers **with and without** 1-point responses. If a conclusion flips, call it "not robust".

**Honest limit:** Google Forms doesn't record time taken, so speeders can't be caught directly. The traps and consistency checks are the substitute.

---

## 5. Analysis key: from answers to "what Ownly should do"

### 5a. Core metrics

| Metric | Formula | Threshold (hypothesis tree) |
|---|---|---|
| Price-pain prevalence | % Q12 ≥ "Once" | H1.1: ≥ 50% |
| Price vs reliability pain | % Q13 in {extra charges, food costs more, offers don't save} vs % in {late, cancelled} | H1.2: price ≥ reliability |
| Offer dependency | % Q8 = any "Yes" | H1.5: ≥ 40% = high |
| Multi-homing | % ticking ≥ 2 real apps in Q10 | H9.4 |
| Switching threshold | Median band of Q15; % "price alone wouldn't" | H2.3: vs the audit's median Ownly saving |
| Guardrails | % choosing ₹230 in Q16, Q17, Q19 (Wilson 95% CI) | > 50% (CI lower bound) = ₹30 "buys" that compromise |
| Fee ceiling | % with Q20 ≥ each level | H8.1: ≥ 50% at the audit-observed Ownly fee |
| Price display | Q21 split | H2.2: ≥ 60% prefer "restaurant price + clear fee" |
| Durability doubt | % Q22 = "rise" or "shuts down / gets worse" | AS24: ≥ 50% = Ownly needs a price promise |
| **Ownly funnel** | Heard = Q23 ≠ "hadn't heard"; Looked = looked + ordered; Ordered; Repeat = D2 ≥ "2–3" (Hyderabad users) | H11.3; stage-to-stage conversion % |
| PMF signal | % D8 = "Very disappointed" | ≥ 40% (Sean Ellis). **Report only if ≥ 20 Ownly users; otherwise label "anecdotal".** |

**Every metric is split by Q3 (students vs working). Report a split only when each group has n ≥ 20.**

### 5b. Ownly action map (pre-registered reading of results)

| If the data show… | …then Ownly should… |
|---|---|
| A1/B3/C3 top trigger = **"usual restaurants"** | Build supply first: onboard the restaurants Gachibowli users already order from before spending on ads |
| Top trigger = **"seeing it's cheaper"** | Put a side-by-side "you saved ₹X vs other apps" on the menu or receipt |
| Top trigger = **first-order offer** | Keep the offer, **but** check D2/D3: if offer-driven triers don't repeat (H12.4), the offer buys trial, not customers |
| Top trigger = **"refund promise"**, or A2/B4 top worry = delivery or refunds | Launch a visible service guarantee (e.g. automatic refund if not delivered) before scaling |
| Trigger or C2/D9 = **cash on delivery / meal card** (especially working professionals) | Add Pluxee/Zeta and COD; target office clusters in Financial District and HITEC City |
| A2/B4 worry = **"low prices won't last"**, or Q22 ≥ 50% expect rises | Communicate a price-lock or "honest pricing" promise; don't rely on launch discounts |
| A2/B4 worry = **"trusting a Rapido service"** | Lead with the Ownly brand; play down Rapido in food marketing |
| A3 = **quick meal for me / lunch** | Position as the everyday solo-meal app ("Meals for One", under ₹200) |
| A3 or D7 = **group / late night** | Fix large-order and late-night reliability before promoting these occasions |
| B2 = **"heard bad things"** | Reputation repair: public reliability stats, fast social-media support |
| B1/C1 channel mix | Double down on the channel that produces the most **opened/ordered** users, not the most aware |
| C2 leak = **restaurants / area / delivery time / coupon** | That is the conversion fix: supply, serviceability, ETA, or price-matching incumbent coupons |
| D4 problem + D5 "not sorted" + D2 = 0 | **Recovery is the retention lever**: a first-order failure that isn't fixed loses the customer |
| D7 top reason | The competitive gap to close first |
| D9 top change | The single product priority named by actual users |
| Q16/Q17/Q19 majority won't trade | These are **guardrails**: cheaper must not mean slower, flakier or thinner selection |
| Q21 prefers clear fee | Keep showing the delivery fee openly; don't copy "free delivery + higher menu" |

**Qualitative:** code Q14 into themes (fees, late, cancel, quality, support, selection). Contact Q24 volunteers using `04_interviews/interview_guide_30min.md` §1–§6, prioritising Ownly users whose first order went wrong (D4 ≠ smooth). About 10% of respondents volunteering is healthy (*Testing Business Ideas*).

---

## 6. Before launch: 45-minute checklist

1. **In-app fact check (Ownly, with a Gachibowli address), then update P9A:**
   - Delivery fee shown at checkout → fill the [DELIVERY FEE LINE]
   - Current first-order offer → fill [CURRENT OFFER] in A1/B3/C3
   - Whether cash on delivery or meal cards are accepted (if they now are, keep the option anyway; it tells us whether people *know*)
   - Whether it delivers to Gachibowli at all. If not, that's a finding. Change the P9A line "available in Hyderabad" to name the served areas.
2. Search the Play Store and App Store for **"Biteway"**. If a real food app appears, rename the trap (e.g. "Khanaway") and re-check.
3. Fill in the form yourself along **every path**: P9A, P9B, P9C, P9D smooth, P9D problem, and Not eligible. Confirm every "Go to section" arrow and every "After section" setting.
4. Pilot with **5 target people** (2 students, 3 working; at least 1 Ownly user if possible). Time them.
   - Target: **median ≤ 4½ min** for non-users.
   - If it runs over, cut in this order: Q22 → Q20 → Q7 → B4.
5. Ask each pilot person:
   - "Which question made you pause?"
   - "In your own words, what was Q15 asking?"
   - "Did anything in Q16–Q19 feel confusing?"
   - "Did the Ownly description feel like an ad?"
6. Fix the wording, **delete the pilot rows** from the response sheet, then launch.

---

## 7. Sharing: messages and rules

### 7a. Rules for every message (read before sending anything)

**Why this matters:** the message decides *who* answers and *what they think the survey wants*. A leading message quietly ruins the data before anyone opens the form.

| ❌ Never write | Why it damages the data | ✅ Write instead |
|---|---|---|
| "Ownly", "Rapido", "zero commission", "new app" | Attracts Ownly fans and critics; primes brand answers before Q23 | "how people choose food delivery apps" |
| "Are you tired of Swiggy/Zomato charges?" / "hidden fees" / "apps overcharge" | Tells people the "right" answer; inflates price pain (Q12–Q13) | "what you like and what annoys you" |
| "Help us prove…" / "We think…" / "Our hypothesis is…" | People answer to please you (acquiescence) | "we want to understand" |
| "It's for a startup" / "for a company" | People suspect marketing and answer strategically or skip | "independent student research" |
| "Takes 1 minute" | It doesn't; people quit halfway and feel misled | "about 4 minutes" (honest) |
| "Win a prize / lucky draw" (unless you truly have one) | Attracts people outside the target who click through for rewards | Thank people; ask them to forward |
| "Just fill anything" / "fill it fast" | Invites careless answers | "please answer what you actually do" |
| Posting only in one college group | The sample becomes one campus; results aren't about Gachibowli | Mix college, PG/co-living, office and friend groups |
| Explaining the "Biteway" question to anyone | Breaks the quality check | Say nothing about individual questions |

**Also:**
- Send **personal messages first**. A 1:1 message gets far more responses than a group post.
- Post in groups **between 12:30–2 pm or 7–9:30 pm**, when people are on their phones.
- If someone asks "is this for Swiggy/Ownly?", use the reply templates in §7g. Never reveal the brand focus.

### 7b. WhatsApp group message (college, PG/co-living, apartment, community groups)

> Hi everyone! 👋 Sorry for the group message, and thank you for reading.
>
> I'm a Product Management student, and for our Market Research project we're studying **how people aged 20–30 around Gachibowli choose food delivery apps**: what they like, what annoys them, and what would make them switch apps.
>
> We'd be really grateful if you could fill in our short survey:
> 👉 [FORM LINK]
>
> ⏱ **About 4 minutes**, almost all taps (one optional typing question)
> 🔒 **Anonymous**: no name, no email
> 🎓 Independent student research. We don't work for any food app or restaurant.
>
> **Who can fill it:** anyone **aged 20–30** who lives, works or studies around **Gachibowli, Financial District, Kondapur, HITEC City/Madhapur, Manikonda, Narsingi/Kokapet or Nallagandla/Tellapur**, and has ordered food online at least once in the last month.
>
> **One request:** please answer based on **what you actually do**, not what sounds right. There are no right or wrong answers, and "none" or "don't know" are perfectly useful answers. If you can, open your food app's order history while filling it. It makes the answers much more accurate.
>
> If it's not for you, please **forward it** to a friend or colleague it fits. That helps us just as much 🙏
>
> We're collecting answers until **[DAY, DATE, TIME]**. Thank you so much!

### 7c. Personal WhatsApp message (friends, classmates, colleagues; send these first)

> Hey [Name]! Hope you're doing well 🙂
>
> Small favour: I'm doing a market research project for my PDM course on **how people around Gachibowli choose food delivery apps**. Could you fill in a quick survey? It's about **4 minutes**, mostly taps, and completely anonymous.
>
> 👉 [FORM LINK]
>
> Just answer based on what you actually do. There are no right answers. And if you have friends, flatmates or colleagues aged 20–30 around Gachibowli/HITEC City who order food, could you forward it to 2–3 of them? That would help a lot.
>
> Thanks a ton! 🙏

### 7d. Office / colleague group (Financial District, HITEC City, Nanakramguda)

> Hi all, a quick non-work request 🙂
>
> I'm doing a Product Management course alongside work, and our project studies **how working professionals and students in West Hyderabad choose food delivery apps** (what matters, what's frustrating, what would make you switch).
>
> If you're **20–30** and order food online around office or home, I'd really appreciate **4 minutes** of your time:
> 👉 [FORM LINK]
>
> It's anonymous, mostly taps, and not linked to any company. Please answer based on your real ordering, not what sounds right. Forwarding to friends in the area is very welcome.
>
> Thank you!

### 7e. LinkedIn post

> **Working or studying around Gachibowli, Financial District or HITEC City? I'd value 4 minutes of your time.**
>
> As part of my Product Management programme, our team is running market research on **how 20–30-year-olds in West Hyderabad choose food delivery apps**: what drives the choice, what frustrates people, and what trade-offs they'd accept for a better experience.
>
> 🕒 About 4 minutes · 🔒 Anonymous · 📱 Built for your phone
> 👉 [FORM LINK]
>
> There are no right answers. We want to understand real ordering behaviour, so honest "I don't know" answers are just as valuable.
>
> I'll share a short summary of what we learn once the project is complete. If you have colleagues or juniors in the area, a repost or forward would help us reach a fairer mix of people. Thank you! 🙌
>
> #Hyderabad #Gachibowli #HITECCity #ProductManagement #MarketResearch #ConsumerResearch

### 7f. Reminders

**Reminder 1 (next day, same groups):**
> Thank you so much to everyone who filled in the food delivery survey yesterday! 🙏
>
> We still need more answers from **[working professionals / students / people in Kondapur & Financial District]**, so the results reflect everyone and not just one group.
>
> If you're 20–30, order food around Gachibowli, and haven't filled it yet, it's about 4 minutes: 👉 [FORM LINK]
> (If you've already filled it, please don't fill it again. Forwarding it is the best help!)

**Final reminder (a few hours before closing):**
> Last call 🙂 Our food delivery survey closes **tonight at [TIME]**. If you've been meaning to fill it, now's the time (about 4 min, anonymous): 👉 [FORM LINK]
> Huge thanks to everyone who already did. You made this project possible 🙏

### 7g. Reply templates (when people ask questions)

| If someone asks… | Reply |
|---|---|
| "Is this for Swiggy / Zomato / some app?" | "No, it's independent student research for our course. We're studying how people choose between apps in general." |
| "What's the right answer for the price questions?" | "There isn't one. We genuinely want to know what you'd do, and different people choose differently." |
| "I don't live in Gachibowli, can I still fill it?" | "Thank you! It's only for people around Gachibowli and nearby areas, but forwarding it to someone there would really help." |
| "I'm 31 / 19, can I fill it?" | "Thanks for offering! This one is only for 20–30, but please forward it if you know someone in that range." |
| "Why do you want my number?" (Q24) | "It's optional. Only if you're happy to have a 10-minute chat later. Skip it otherwise." |
| "I filled it twice by mistake" | "No problem, thanks for telling me! We remove duplicates when cleaning the data." |
| "What will you do with the results?" | "It's for our course project. We report only overall patterns, never individual answers. I'm happy to share the summary later." |

---

## 8. What was removed from the old 103-question form, and why

| Removed | Why | Where that evidence comes from instead |
|---|---|---|
| Consent page, repeat check, work-conflict check, institution, work sector, gender, monthly spend | Don't help answer the problem; add screens | Q6 order amount stands in for spend; duplicate rule D1 |
| Three separate "which platform" questions | Same thing asked three ways | Q5 last app + Q10 multi-select |
| 9-row frequency grid | Breaks on phones; vague "often/rarely" | Q12 behavioural count + Q13 single biggest annoyance |
| 7 choice tasks, 4 bill scenarios, fee ladder, 4 randomised versions | Need 125+ responses and complex builds | Q16/Q17/Q19 trade-offs, Q20 fee, Q21 bill style |
| "How likely are you to try Service X / Ownly" (intent) | Hypothetical intent without real understanding; no action follows from it | Factual card + trigger (A1), worry (A2), first order type (A3) |
| Brand-blind vs branded arms | Needs ~100 per arm | A2/B4 "Rapido trust" option + interviews |
| 20+ generic Ownly-user questions | Few users this early; many didn't lead to a decision | 4 funnel paths, first-order branch, Sean Ellis, one-change question |

---

## Sources

- Galesic, M. & Bosnjak, M. (2009). Effects of questionnaire length on participation and indicators of response quality in a web survey. *Public Opinion Quarterly* 73(2). https://academic.oup.com/poq/article-abstract/73/2/349/1939196
- Revilla, M. & Höhne, J. K. (2020). How long do respondents think online surveys should be? https://journals.sagepub.com/doi/abs/10.1177/1470785320943049
- Meade, A. W. & Craig, S. B. (2012). Identifying careless responses in survey data. *Psychological Methods* 17(3). https://pubmed.ncbi.nlm.nih.gov/22506584/
- Murphy, J. J. et al. (2005). A meta-analysis of hypothetical bias in stated preference valuation. https://link.springer.com/article/10.1007/s10640-004-3332-z
- Pew Research Center. Writing Survey Questions. https://www.pewresearch.org/writing-survey-questions/
- Response alternatives and frequency reports (Schwarz; review in PLOS One 2022). https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0263552
- Paulhus Lab, Over-claiming technique. https://paulhuslab.psych.ubc.ca/research/overclaiming/ ; Quirk's, "When fake brands are used to get real data". https://www.quirks.com/articles/when-fake-brands-are-used-to-get-real-data
- Ownly Hyderabad festival campaign (MEDIA REPORT, Sep 2026). https://businessnewsthisweek.com/business/ownly-puts-bappas-delivery-partner-on-hyderabads-roads-with-mooshak-on-wheels/
- Ownly app listings: https://play.google.com/store/apps/details?id=com.ownly.customer&hl=en_IN ; https://apps.apple.com/in/app/ownly-food-delivery-app/id6747476494
- Project evidence: `05_review_mining/voc_synthesis_pre_fieldwork.md`, `05_review_mining/social/social_analysis.md`, `05_review_mining/app_stores/analysis_tables.md`, `01_secondary_research/secondary_research_report.md`
- Fitzpatrick, R. (2013). *The Mom Test*. Bland, D. J. & Osterwalder, A. (2019). *Testing Business Ideas* (Discovery Survey; Sean Ellis Test). Savoia, A. (2019). *The Right It*.
