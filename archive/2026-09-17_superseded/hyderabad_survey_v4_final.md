# Hyderabad (Gachibowli) Survey v4: FINAL, KPI-Complete

> ⚠️ **SUPERSEDED on 2026-09-16 by `../Survey_v5_All_Cities.md`** (one form for Bengaluru, Hyderabad and other cities; 9 KPIs). Reference only.

**Version:** 2026-09-15. **Replaces v3** (`hyderabad_survey_v3_final.md`).
**Why v4:** every question now feeds a metric **from the course formula sheets** (`Formulae Sheet (1).docx`, `Formulae Sheet 2.pdf`, `Marketing Metrics 1000 Records.csv`). How each metric is calculated from these questions is in `../KPI_Framework_and_Survey_Validation.md`.

**Problem statement:** Will Ownly's Bengaluru pitch ("pay the restaurant's price, no hidden fees") pull 20–30-year-old students and working professionals in and around Gachibowli away from Swiggy/Zomato? If not, what must Ownly change?

**Length (confirm in the pilot):**

| Path | Questions | Time |
|---|---|---|
| Doesn't order food online | ~14 | ~3 min |
| Orders food, not an Ownly user | ~22 | ~5 min |
| Ownly user | ~34 | ~7 min |

---

## 1. What changed from v3, and why

| Change | Why (metric it enables) |
|---|---|
| **People who didn't order in the last 4 weeks are no longer screened out.** They answer 2 short questions and the Ownly block. | **Market Penetration** needs the whole population in the denominator, not only buyers. **CDI/BDI** also need non-buyers. |
| **Order counts per app** (Swiggy, Zomato, Ownly, other) in the last 4 weeks, as numbers | **Unit Market Share, Unit Share of Requirements, Usage Index, BDI, CDI, Relative Market Share**. Bands were too coarse. |
| **Average ₹ per order** (everyone) and **average ₹ per Ownly order** (users) | **Average Price per Unit, Revenue Market Share, Revenue Share of Requirements** |
| **Last order: amount + number of people** | **Price per Statistical Unit** (one solo meal) and **Unit Price per Statistical Unit** (₹ per person) |
| **App price vs restaurant price** question | **Margin %** via Customer Selling Price vs Supplier Selling Price (channel margin) |
| Ownly users: **first order timing + orders in the previous 4 weeks** | **Retention Rate** (customers at start, at end, new) and **period growth** (YoY formula applied to 4-week periods) |
| Ownly users: **discount on first order** | **Average Acquisition Cost** and **CPA** |
| Ownly users: **offers on recent orders** | **Average Retention Cost** |
| Ownly users: **"if Ownly didn't exist, what would you have done?"** | **Cannibalization Rate** (source of volume) |
| **Where people first heard of Ownly** (all aware paths) | **CTR / Conversion Rate** of Ownly's funnel by channel |
| **Where people got the survey link** | CTR / Conversion Rate / CPA of our own recruitment |
| Removed the price-vs-speed/reliability/restaurant trade-offs, the switching threshold, the bill-style and price-durability questions, "why that app", and the logic trap | They didn't feed a formula-sheet metric. The quality trap is replaced by 6 consistency checks that the new numbers make possible (§4). |
| Kept: membership, biggest annoyance, trigger/worry/leak/one-change, first-order outcome, Sean Ellis | **Driver questions.** They aren't KPIs; they explain *why* a KPI is high or low, which is the "what must Ownly change" half of the problem. |

---

## 2. Question → metric map (one line each)

| Q | Feeds (formula-sheet metric unless marked) |
|---|---|
| Q1, Q2 | Population definition (denominator for all penetration and index metrics) |
| Q3 | Groups for **BDI / CDI**; every metric split by segment |
| Q4 | **Market Penetration** |
| N1, N2 | Market Penetration context (lapsed vs never) · driver |
| Q5–Q8 | **Unit Market Share, Relative Market Share, Unit SoR, Usage Index, BDI, CDI, Brand Penetration, Penetration Share, Retention (customers at end), Growth** |
| Q9 | **Average Price per Unit** (category), **Revenue Market Share, Revenue SoR** |
| Q10, Q11, Q12 | **Average Price per Unit by app, Price per Statistical Unit, Unit Price per Statistical Unit** |
| Q13 | Driver (discount-dependence of price per unit) |
| Q14 | Quality trap · multi-homing driver · Brand Penetration (3-month) |
| Q15 | Driver (membership lock-in explains SoR) |
| Q16 | Driver (pain) |
| Q17 | **Margin %** (Customer vs Supplier Selling Price) |
| Q18 | **Contribution per Unit** (price side: acceptable fee per order) |
| Q19 | Qualitative (optional) |
| Q20 | **CTR / Conversion Rate** funnel stages (impressions → clicks → conversions); **Brand Penetration (ever)** |
| A1–A3, B2–B4, C2–C3 | Drivers of CTR and Conversion Rate |
| B1, C1, D1 | Funnel by channel (**CTR / Conversion Rate** per channel) |
| D2 | Hyderabad vs Bengaluru filter |
| D3 | **Retention Rate** (new customers) · Average Acquisition Cost cohort |
| D4 | **Retention Rate** (customers at start) · **Growth rate** |
| D5 | **Average Price per Unit** (Ownly) · **Revenue SoR / Revenue Market Share** · CLV margin |
| D6 | Driver (why acquired) |
| D7 | **Average Acquisition Cost, CPA** (+ ROAS scenario) |
| D8 | **Average Retention Cost** |
| D9 | **Cannibalization Rate** |
| D10, D11 | Driver of Retention Rate (first-order failure and recovery) |
| D12 | Sean Ellis PMF score (the one addition outside the sheets) |
| D13 | Driver (top fix) |
| Q21 | **CTR / Conversion Rate / CPA** of survey recruitment |
| Q22 | Interview recruitment (optional) |

---

## 3. The form: copy-paste build spec

### Form settings

| Setting | Value |
|---|---|
| Form title | **How young Hyderabad orders food: 5-minute student survey** |
| Collect email addresses | OFF |
| Limit to 1 response | OFF (turning it on forces Google sign-in, and people drop off) |
| Show progress bar | ON |
| Shuffle question order | OFF |
| All questions | Required unless marked *Optional* |
| Number fields | Short answer → ⋮ → Response validation → **Number → Between** (limits given per question) → error text: "Please type a number, e.g. 3" |
| Confirmation message | "Done! Thank you 🙏 Your answers really help our research. If you know someone aged 20–30 around Gachibowli, HITEC City or Financial District, please forward them the link, whether or not they order food online." |

**Branching rule:** Google Forms reliably uses only **one** "Go to section based on answer" question per page, and it must be the **last** question on that page.

**Page map:**
```
P1 Age ─► P2 Area ─► P3 About you (Q4 ordered in 4 weeks?)
                          │ No                          │ Yes
                          ▼                             ▼
                    P3N Not ordering            P4 Orders by app ─► P5 Last order ─► P6 Your apps
                          │                                                              │
                          └──────────────────────────────┬───────────────────────────────┘
                                                         ▼
                                              P7 Ownly (Q20, 4 paths)
             ┌───────────────────────┬───────────────────┼───────────────────────┐
             ▼                       ▼                   ▼                       ▼
       P8A Never heard       P8B Heard, not opened  P8C Looked, no order    P8D Ordered (D1–D10)
             │                       │                   │                 D10 problem? ─► P8D-fix (D11)
             │                       │                   │                       ▼
             │                       │                   │                 P8D-more (D12–D13)
             └───────────────────────┴─────────┬─────────┴───────────────────────┘
                                                ▼
                                         P9 Last page ─► Submit
(P1 / P2 not-eligible answers ─► PX Not eligible ─► Submit)
```

---

### Page 1: Welcome

**Page description (paste exactly):**
> **Hi! Thanks for opening this 🙂**
> We're Product Management students studying **how people aged 20–30 around Gachibowli choose and use food delivery apps**, including people who rarely or never order.
>
> **What to expect**
> • About **5 minutes**, mostly taps. A few questions ask you to type a number.
> • **Anonymous**: we don't ask your name or email.
> • Independent student research. We don't work for any food app or restaurant.
>
> **One request:** answer based on **what you actually do**. Opening your food app's order history for a minute makes your answers much more accurate. A good guess is fine; there are no right or wrong answers.

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
*(Description: "If more than one, pick where you'd usually get food delivered.")*
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

**Q4. In the last 4 weeks, did you order food online for delivery at least once (any app, or directly from a restaurant)?** · Multiple choice · Go to section based on answer
- Yes → *P4 Orders by app*
- No → *P3N Not ordering*

---

### P3N: Not ordering recently (after section → *P7 Ownly*)

**N1. When did you last order food online for delivery?** · Multiple choice
- 1–3 months ago
- 3–12 months ago
- More than a year ago
- I've never ordered food online

**N2. What's the MAIN reason you haven't ordered food online in the last 4 weeks?** · Multiple choice · Shuffle options ON
- I cook, or eat at home / mess / hostel
- Too expensive once fees are added
- I prefer eating out
- I don't trust the hygiene or quality
- Delivery doesn't reach my hostel / PG / office easily
- I just didn't need to
- Other

---

### Page 4: Your orders in the last 4 weeks

**Page description (paste):**
> Count **orders**, not items. Open each app → **Orders** to check. A good guess is fine. Type **0** if you didn't use that app.

**Q5. Swiggy: how many orders in the last 4 weeks?** · Short answer · Number between 0 and 60

**Q6. Zomato: how many orders in the last 4 weeks?** · Short answer · Number between 0 and 60

**Q7. Ownly (Rapido's food app, or food inside the Rapido app): how many orders in the last 4 weeks?** · Short answer · Number between 0 and 60

**Q8. Any other way (Toing, Magicpin, EatSure, or directly from a restaurant by phone / WhatsApp / its own app): how many orders in the last 4 weeks?** · Short answer · Number between 0 and 60

**Q9. On average, how much do you pay per food delivery order?** · Short answer · Number between 0 and 5000
*(Description: "₹, the final amount including all fees, after discounts. A rough average is fine.")*

---

### Page 5: Your last order

**Page description:** "Now just your **most recent** food delivery order."

**Q10. Which app did you use for it?** · Multiple choice
- Swiggy
- Zomato
- Ownly (or food inside the Rapido app)
- Toing
- Magicpin
- EatSure
- Directly from the restaurant
- Other

**Q11. What was the total amount you paid?** · Short answer · Number between 0 and 10000
*(Description: "₹, final amount after discounts, including all fees. Check the app if you can.")*

**Q12. How many people was that order for?** · Multiple choice
- Just me
- 2 people
- 3–4 people
- 5 or more people

**Q13. Did that order use a discount?** · Multiple choice
*(Description: "A coupon, an offer, a bank/card offer, or a membership benefit like free delivery.")*
- Yes, a coupon, offer or card offer
- Yes, a membership benefit
- Both
- No
- Not sure

---

### Page 6: Your food apps (after section → *P7 Ownly*)

**Q14. Which of these have you ordered food from in the last 3 months? Select all that apply.** · Checkboxes · Shuffle options ON
- Swiggy
- Zomato
- Ownly (or food inside the Rapido app)
- Toing
- Magicpin
- EatSure
- Biteway ⚠️ *TRAP: not a real app. Don't remove it or explain it.*
- Directly from a restaurant

**Q15. Do you have a food delivery membership right now?** · Multiple choice
- Swiggy One
- Zomato Gold
- Both
- Neither
- Not sure

**Q16. Which ONE of these bothers you most when ordering food online?** · Multiple choice · Shuffle options ON
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

**Q17. Think of a dish you've bought both at the restaurant itself and on a delivery app. On the app, the dish price (before delivery and other fees) was usually:** · Multiple choice · Keep this order
- Cheaper on the app
- About the same
- Up to 10% more
- 10–25% more
- 25–50% more
- More than 50% more
- I haven't compared

**Q18. Imagine an app where food costs the same as at the restaurant, with no platform or packaging fees, only a delivery fee. For a ₹220 meal, what's the highest delivery fee you'd pay before ordering elsewhere?** · Multiple choice · Keep this order
- ₹0 (only if delivery is free)
- ₹10
- ₹20
- ₹30
- ₹40
- ₹50 or more

**Q19. *Optional:* Think of the last time ordering food online annoyed you. What happened?** · Paragraph · Not required
*(Description: "One or two lines is perfect. Example: 'Paid ₹90 in fees on a ₹200 biryani, so I cancelled.'")*

---

### Page 7: One app in particular

**Q20. Ownly is a food delivery app by Rapido (the bike-taxi and auto app). Before today, which of these is true for you?** · Multiple choice · Go to section based on answer
- I hadn't heard of Ownly → *P8A*
- I'd heard of it, but never opened it → *P8B*
- I opened or browsed it, but didn't order → *P8C*
- I've ordered on Ownly → *P8D*

---

### P8A: New to Ownly (after section → *P9*)

**Page description (paste exactly; neutral and factual):**
> **About Ownly (so you know what we mean):**
> • A food delivery app from Rapido, available in Hyderabad since around September 2026 and also inside the Rapido app.
> • Restaurants pay Ownly no commission, so menu prices are meant to match the restaurant's own prices.
> • No platform fee, packaging fee or surge fee. [DELIVERY FEE LINE: fill in after the in-app check, e.g. "A delivery fee is shown before you pay" or "Delivery is currently free"]
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
- Nothing, I'm happy with how I order now

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

### P8B: Heard of Ownly, never opened it (after section → *P9*)

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

**B3. Which ONE thing would most make you try Ownly for an order?** · *(Copy A1 exactly.)*

**B4. Which ONE worry would most stop you from trying it?** · *(Copy A2 exactly.)*

---

### P8C: Looked at Ownly, didn't order (after section → *P9*)

**C1. Where did you first hear about Ownly?** · *(Copy B1 exactly.)*

**C2. When you looked, what MAINLY stopped you from ordering?** · Multiple choice · Shuffle options ON
- My restaurants weren't there
- Prices weren't lower than my usual app
- A coupon on my usual app made that cheaper
- It didn't deliver to my address
- The delivery time looked too long
- I couldn't pay the way I wanted
- I was just looking around
- Other

**C3. Which ONE thing would most make you order on Ownly next time?** · *(Copy A1 exactly.)*

---

### P8D: Ownly users (page 1 of 3)

**Page description:** "A few more questions, since you've used Ownly. Your answers are the most valuable part of this survey 🙏"

**D1. Where did you first hear about Ownly?** · *(Copy B1 exactly.)*

**D2. Where have you ordered on Ownly?** · Multiple choice
- Hyderabad only
- Bengaluru only
- Both

**D3. When did you place your FIRST Ownly order?** · Multiple choice
- In the last 4 weeks
- 1–2 months ago
- 2–6 months ago
- More than 6 months ago

**D4. How many Ownly orders did you place in the 4 weeks BEFORE the last 4 weeks (roughly 5–8 weeks ago)?** · Short answer · Number between 0 and 60
*(Description: "Type 0 if none, or if you started using Ownly only in the last 4 weeks.")*

**D5. On average, how much do you pay per Ownly order?** · Short answer · Number between 0 and 5000
*(Description: "₹, final amount including the delivery fee, after discounts.")*

**D6. What MAINLY made you place your first Ownly order?** · Multiple choice · Shuffle options ON
- A first-order offer or referral discount
- It showed a lower price than my usual app
- No platform or packaging fees
- A friend recommended it
- I saw it inside the Rapido app
- A restaurant I like was on it
- Just curious

**D7. How much discount did you get on your FIRST Ownly order?** · Multiple choice
- No discount
- Up to ₹50 off
- ₹51–100 off
- More than ₹100 off
- Don't remember

**D8. In the last 4 weeks, how did offers work on your Ownly orders?** · Multiple choice
- I didn't order on Ownly in the last 4 weeks
- No offers used
- Offers on some orders, usually ₹50 or less off
- Offers on some orders, usually more than ₹50 off
- Offers on most or all orders, usually ₹50 or less off
- Offers on most or all orders, usually more than ₹50 off

**D9. Think of your most recent Ownly order. If Ownly didn't exist, what would you most likely have done instead?** · Multiple choice · Shuffle options ON
- Ordered the same on Swiggy or Zomato
- Ordered on another app (Toing, Magicpin, etc.)
- Ordered directly from the restaurant
- Cooked, or eaten at home / mess / hostel
- Gone out to eat
- Skipped it or had a snack
- Don't know

**D10. How did your FIRST Ownly order go?** · Multiple choice · Go to section based on answer
- Smooth, no problems → *P8D-more*
- Arrived late → *P8D-fix*
- Got cancelled → *P8D-fix*
- Wrong or missing items → *P8D-fix*
- Marked "delivered" but never reached me → *P8D-fix*
- Food quality problem → *P8D-fix*

### P8D-fix: When the first order went wrong (after section → *P8D-more*)

**D11. Did it get sorted?** · Multiple choice
- Yes, a full refund or fix within a day
- Sorted, but slowly or only partly
- No, it wasn't sorted
- I didn't contact support

### P8D-more: Ownly users, continued (after section → *P9*)

**D12. How would you feel if you could no longer use Ownly?** · Multiple choice
- Very disappointed
- Somewhat disappointed
- Not disappointed

**D13. What ONE change would make you order more on Ownly?** · Multiple choice · Shuffle options ON
- More restaurants
- Faster delivery
- More reliable, on-time delivery
- Quicker refunds and support
- A bigger price gap vs other apps
- More offers and coupons
- Cash on delivery or meal-card payment
- A membership with extra benefits

---

### P9: Last page (after section → *Submit*)

**Page description:** "That's it, thank you! 🙏 Two quick last ones."

**Q21. Where did you get the link to this survey?** · Multiple choice
- A WhatsApp group
- A personal WhatsApp message
- LinkedIn
- Instagram
- A college or office group (Slack, Teams, email)
- Other

**Q22. *Optional:* Can we message you for a 10-minute chat about how you order food?** · Short answer · Not required
*(Description: "Leave your WhatsApp number if yes. It's only used to contact you for the chat and is kept separately from your answers.")*

---

### PX: Not eligible (last page; after section → *Submit*)

**Page description:**
> Thanks so much for your time! 🙏 This survey is only for people **aged 20–30** who live, work or study **around Gachibowli**. Please press **Submit**. If you know someone who fits, please forward them the link.

---

## 4. Quality checks (fix these rules BEFORE seeing results)

| Check | Flag rule | Points |
|---|---|---|
| **T1 Fake app** | Ticked "Biteway" in Q14 | **2** |
| **C1 Last order vs counts** | Q10 = Swiggy but Q5 = 0; or Zomato and Q6 = 0; or Ownly and Q7 = 0 (the last order must fall inside the last 4 weeks for Q4 = Yes) | 1 |
| **C2 Ownly vs counts** | Q7 ≥ 1 but Q20 ≠ "ordered"; or Q14 includes Ownly but Q20 = "hadn't heard" | 1 |
| **C3 Impossible totals** | Q4 = Yes but Q5+Q6+Q7+Q8 = 0; or Q5+Q6+Q7+Q8 > 60 | 1 |
| **C4 New but old** | D3 = "In the last 4 weeks" but D4 ≥ 1 | 1 |
| **C5 Before launch** | D2 = "Hyderabad only" and D3 ∈ {2–6 months, More than 6 months} (Ownly went live in Hyderabad ≈ Sep 2026) | 1 |
| **C6 Implausible solo meal** | Q12 = "Just me" and Q11 > ₹1,500 | 1 |
| **C7 Junk text** | Q19 is gibberish | 1 |
| **D1 Duplicate** | Identical answers on every required question, submitted within 10 minutes | keep first only |

**Exclusion rule:** exclude responses with **2 or more points**. Report headline metrics **with and without** 1-point responses.
**Limit:** Google Forms doesn't record time taken. The checks above stand in for a speed check.

---

## 5. Before launch: 45-minute checklist

1. **In-app check (Ownly, with a Gachibowli address).** Fill the [DELIVERY FEE LINE] and [CURRENT OFFER] placeholders. Note the delivery fee, the first-order offer, and whether cash on delivery or meal cards are accepted. This observed fee is also the price input for **Contribution per Unit**.
2. Search the Play Store and App Store for **"Biteway"**. If a real food app appears, rename the trap.
3. Walk every path yourself: not eligible, P3N, P8A, P8B, P8C, P8D smooth, P8D problem. Check every "Go to section" and "After section" setting and every number validation.
4. Pilot with **5 target people**, including 1 non-orderer and 1 Ownly user if possible. Time them.
   - Target median: **≤ 5½ min** for orderers who don't use Ownly.
   - If it runs over, cut **Q16**, then **Q13**, then **B4**. Never cut a question that feeds a metric.
5. Ask each pilot person:
   - "Was counting orders per app (Q5–Q8) easy? Did you open your order history?"
   - "In your own words, what was Q17 asking?"
   - "Was D4 (orders 5–8 weeks ago) clear?"
6. Fix the wording, **delete the pilot rows**, then launch.

---

## 6. Sharing: messages and rules

### 6a. Rules for every message

**Why this matters:** the message decides who answers and what they think we want to hear. A leading message damages the data before the form even opens.

| ❌ Never write | Why it damages the data | ✅ Write instead |
|---|---|---|
| "Ownly", "Rapido", "zero commission", "new app" | Attracts Ownly fans and critics; inflates Ownly penetration | "how people choose and use food delivery apps" |
| "Are you tired of Swiggy/Zomato charges?" / "hidden fees" | Signals the "right" answer; biases pain and markup answers | "what you like and what annoys you" |
| "Only if you order food online" | Removes non-orderers, which **breaks Market Penetration and CDI** | "whether you order often, rarely or never" |
| "Help us prove…" / "We think…" | People answer to please you | "we want to understand" |
| "It's for a startup / company" | People suspect marketing and answer strategically | "independent student research" |
| "Takes 1 minute" | Untrue; people quit halfway | "about 5 minutes" |
| "Just fill anything" | Invites careless answers, and the order counts get wrong | "please check your order history if you can" |
| Posting in only one college group | The sample becomes one campus, which distorts BDI/CDI | Mix college, PG/co-living, office and friend groups |
| Explaining the "Biteway" option | Breaks the quality check | Say nothing about individual questions |

**Also:**
- Send **personal messages first**; they get far more responses than group posts.
- Post in groups **12:30–2 pm or 7–9:30 pm**.
- **Use a separate short link per channel** (e.g. bit.ly/ownly-wa-group, /-dm, /-li). Link clicks by channel plus Q21 give our recruitment **CTR, Conversion Rate and CPA** (KPI file, KPI 17).

### 6b. WhatsApp group message (college, PG/co-living, apartment, community groups)

> Hi everyone! 👋 Sorry for the group message, and thank you for reading.
>
> I'm a Product Management student, and for our Market Research project we're studying **how people aged 20–30 around Gachibowli choose and use food delivery apps**: how often they order, what they pay, what annoys them, and what would make them switch.
>
> We'd be really grateful if you could fill in our short survey:
> 👉 [FORM LINK]
>
> ⏱ **About 5 minutes**, mostly taps and a few numbers
> 🔒 **Anonymous**: no name, no email
> 🎓 Independent student research. We don't work for any food app or restaurant.
>
> **Who can fill it:** anyone **aged 20–30** who lives, works or studies around **Gachibowli, Financial District, Kondapur, HITEC City/Madhapur, Manikonda, Narsingi/Kokapet or Nallagandla/Tellapur**, **whether you order food online often, rarely or never.** Every answer counts.
>
> **Two requests:**
> 1️⃣ Answer based on **what you actually do**, not what sounds right. There are no right or wrong answers.
> 2️⃣ If you order food online, **keep your food app's order history open** while filling it. A couple of questions ask how many orders you placed, and checking makes a huge difference.
>
> If it's not for you, please **forward it** to a friend or colleague it fits 🙏
>
> We're collecting answers until **[DAY, DATE, TIME]**. Thank you so much!

### 6c. Personal WhatsApp message (send these first)

> Hey [Name]! Hope you're doing well 🙂
>
> Small favour: I'm doing a market research project for my PDM course on **how people around Gachibowli use food delivery apps**. Could you fill in a quick survey? It's about **5 minutes** and completely anonymous.
>
> 👉 [FORM LINK]
>
> Just answer what you actually do; there are no right answers. If you order food online, keep your app's order history handy (a couple of questions ask how many orders you placed).
>
> And if you have friends, flatmates or colleagues aged 20–30 around Gachibowli/HITEC City, whether they order food or not, could you forward it to 2–3 of them? That would help a lot. Thanks a ton! 🙏

### 6d. Office / colleague group (Financial District, HITEC City, Nanakramguda)

> Hi all, a quick non-work request 🙂
>
> I'm doing a Product Management course alongside work, and our project studies **how working professionals and students in West Hyderabad use food delivery apps** (how often, how much, what matters, what frustrates).
>
> If you're **20–30**, whether you order food online daily or almost never, I'd really appreciate **5 minutes** of your time:
> 👉 [FORM LINK]
>
> It's anonymous and not linked to any company. Please answer based on your real ordering; checking your order history helps. Forwarding to friends in the area is very welcome. Thank you!

### 6e. LinkedIn post

> **Working or studying around Gachibowli, Financial District or HITEC City? I'd value 5 minutes of your time.**
>
> As part of my Product Management programme, our team is running market research on **how 20–30-year-olds in West Hyderabad use food delivery apps**: how often people order, what they pay, what drives the choice of app, and what makes them switch.
>
> 🕒 About 5 minutes · 🔒 Anonymous · 📱 Built for your phone
> 👉 [FORM LINK]
>
> We want everyone, including people who rarely or never order online, so the picture is complete. Honest "I don't know" answers are just as valuable.
>
> I'll share a short summary of what we learn once the project is complete. A repost or forward to colleagues in the area would help us reach a fairer mix of people. Thank you! 🙌
>
> #Hyderabad #Gachibowli #HITECCity #ProductManagement #MarketResearch #ConsumerResearch

### 6f. Reminders

**Reminder 1 (next day, same groups):**
> Thank you so much to everyone who filled in the food delivery survey yesterday! 🙏
>
> We still need more answers from **[working professionals / students / people who rarely order online / people in Kondapur & Financial District]**, so the results reflect everyone and not just one group.
>
> If you're 20–30 around Gachibowli and haven't filled it yet, it's about 5 minutes: 👉 [FORM LINK]
> (If you've already filled it, please don't fill it again. Forwarding it is the best help!)

**Final reminder (a few hours before closing):**
> Last call 🙂 Our food delivery survey closes **tonight at [TIME]**. About 5 min, anonymous: 👉 [FORM LINK]
> Huge thanks to everyone who already did. You made this project possible 🙏

### 6g. Reply templates

| If someone asks… | Reply |
|---|---|
| "Is this for Swiggy / Zomato / some app?" | "No, it's independent student research for our course. We're studying how people choose and use food apps in general." |
| "I don't order food online, should I still fill it?" | "Yes please! People who rarely or never order are just as important for our results. It's even shorter for you." |
| "I don't remember exactly how many orders" | "A good guess is fine, or check your app's order history. It takes a few seconds." |
| "I don't live in Gachibowli, can I still fill it?" | "Thank you! It's only for people around Gachibowli and nearby areas, but forwarding it to someone there would really help." |
| "I'm 31 / 19, can I fill it?" | "Thanks for offering! This one is only for 20–30, but please forward it if you know someone in that range." |
| "Why do you want my number?" (Q22) | "It's optional. Only if you're happy to chat for 10 minutes later. Skip it otherwise." |
| "I filled it twice by mistake" | "No problem, thanks for telling me! We remove duplicates when cleaning the data." |
| "What will you do with the results?" | "It's for our course project. We report only overall patterns, never individual answers. I'm happy to share the summary later." |

---

## Sources (design)

- Galesic & Bosnjak (2009), survey length and response quality. https://academic.oup.com/poq/article-abstract/73/2/349/1939196
- Meade & Craig (2012), careless responding. https://pubmed.ncbi.nlm.nih.gov/22506584/
- Pew Research Center, Writing Survey Questions. https://www.pewresearch.org/writing-survey-questions/
- Paulhus over-claiming technique. https://paulhuslab.psych.ubc.ca/research/overclaiming/
- Farris et al., *Marketing Metrics* Ch. 2 (penetration, share of requirements, usage index, BDI/CDI). https://ptgmedia.pearsoncmg.com/images/9780131873704/samplechapter/0131873709_CH02.pdf
- Fitzpatrick, *The Mom Test*; Bland & Osterwalder, *Testing Business Ideas* (Sean Ellis test); Savoia, *The Right It*.
- Project evidence: `05_review_mining/voc_synthesis_pre_fieldwork.md`, `05_review_mining/social/social_analysis.md`, `01_secondary_research/secondary_research_report.md`
