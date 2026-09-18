# Ownly Food Delivery Survey v5: One Form for Bengaluru, Hyderabad and Other Cities (FINAL)

**Version:** 2026-09-16. **Replaces** `03_hyderabad_survey/hyderabad_survey_v4_final.md` and `02_bangalore_survey/` for fieldwork.
**Built for:** the 9 KPIs in `KPI_Framework_and_Survey_Validation.md`. Every question either feeds one of those KPIs or explains one; nothing else is asked.

**Problem statement:** Will Ownly's Bengaluru pitch ("pay the restaurant's price, no hidden fees") pull 20–30-year-old students and working professionals in and around Gachibowli (Hyderabad) away from Swiggy/Zomato? If not, what must Ownly change?

**Why one form with three city paths:**

| City path | Role in the problem statement | What it gives the dashboard |
|---|---|---|
| **Bengaluru** | **Benchmark.** Ownly has been live citywide since March 2026 (pilot Aug 2025), so this is where the pitch is known to have worked. | Full KPI values for a mature Ownly market, including retention and repeat use |
| **Hyderabad** | **Target.** Ownly has been live only weeks; Gachibowli is the focus. | The same KPIs, so every Hyderabad number can be read against Bengaluru (transfer view) |
| **Other city** | **Baseline.** Ownly isn't available in most other cities. | How 20–30s use Swiggy/Zomato where Ownly doesn't exist, and what would make them try it |

**Length (confirm in the pilot):**

| Respondent | Questions | Time |
|---|---|---|
| Doesn't order online | ~8 | 2 min |
| Orders online, not an Ownly user | ~14 | 3–4 min |
| Ownly user | ~20 | 5 min |

---

## 1. What changed from v4 and the 24-response pilot

| Pilot problem (24 responses, 15–16 Sep) | Fix in v5 |
|---|---|
| Only 11 of 24 were eligible, and "Not eligible" routing wasn't set | Age screen on each city's first page with explicit routing; build checklist step 3 tests every path |
| No per-app order counts, so share, SoR, penetration and BDI couldn't be computed | Four number questions (Swiggy, Zomato, Ownly, other) on every city path |
| The placeholder "CURRENT OFFER, e.g. ₹100 off" was left in, and 9 people picked it | No placeholders anywhere. Options are written in final form. |
| "Pick up to 2" had no limit (7 people picked 3+) | Removed. Every driver question is single-choice. |
| Two questions had blank titles | Every question has a title (§3 checklist) |
| Hyderabad-only, so there was no benchmark | City-first branching: Bengaluru / Hyderabad / Other |
| v4 had ~34 questions for Ownly users and fed 20 KPIs, many not collectable | ~20 questions max, feeding 9 collectable KPIs |

**Removed from v4 because they fed no KPI in the final 9:** average ₹ per order, discount on last order, apps used in 3 months, membership, biggest annoyance, app-vs-restaurant price, max delivery fee, first-order discount, offers on recent orders, first-order trigger and outcome, "where did you get the link", non-orderer reasons.

---

## 2. Question → KPI map

Question IDs are the same on every city path. The response sheet gets one column per path; cleaning merges them by ID (§5).

| ID | Question (short) | Feeds KPI |
|---|---|---|
| CITY | Which city | Splits every KPI by city |
| LOC | Locality / which other city | **K9 BDI** by area; Gachibowli-area filter |
| AGE | Age band | Eligibility (20–30) |
| OCC | Student / working / etc. | **K9 BDI** by segment |
| ORD | Ordered online in the last 4 weeks? | **K1 Penetration Share** (denominator) |
| N_SW, N_ZO, N_OW, N_OT | Orders on Swiggy / Zomato / Ownly / other in the last 4 weeks | **K1, K3 Unit Market Share, K4 Share of Requirements, K5 Retention (end), K9 BDI** |
| LO_APP, LO_AMT, LO_PPL | Last order: app, ₹ amount, people served | **K8 Price per Statistical Unit** |
| OW_STATUS | Ownly: never heard / heard / opened / ordered | **K7 Conversion Rate** |
| NH_TRIGGER | (Never heard) what would make you try | Driver for K1 |
| SRC | (Aware) where you first heard of Ownly | Splits K7 by channel |
| HD_REASON | (Heard, never opened) main reason | Driver for K7 |
| OP_STOP | (Opened, didn't order) what stopped you | Driver for K7 |
| US_WHERE | (User, Hyderabad & Other paths) where you ordered | City attribution for user KPIs |
| US_FIRST | (User) when was your first order | **K5 Retention** (new customers) |
| US_PRIOR | (User) Ownly orders 5–8 weeks ago | **K5 Retention** (customers at start) |
| US_ALT | (User) if Ownly didn't exist, what would you have done | **K2 Cannibalization Rate** |
| US_PMF | (User) how disappointed without Ownly | **K6 Sean Ellis PMF score** |
| US_LAPSE | (User, Bengaluru) main reason for ordering less | Driver for K5 |
| US_CHANGE | (User) one change to order more | Driver for K4, K5 |
| INTERVIEW | Optional WhatsApp for a 10-min chat | Qualitative follow-up |

---

## 3. Build instructions (Google Forms)

### 3a. How to build the three paths

Google Forms can't "remember" an earlier answer for later branching. So each city gets **its own chain of sections**, and all chains end on the same last page.

1. Build **Page 0** and the **Hyderabad chain (H1–H7)** exactly as in §4.
2. For the Bengaluru chain, use ⋮ → **Duplicate section** on H1…H7. Rename the copies B1…B7 and edit only the items marked **[BLR]** in §4.
3. Duplicate again for the Other chain (O1…O7) and edit the items marked **[OTHER]**.
4. Set every "Go to section" and "After section" arrow as written. **Duplicated sections keep pointing to the Hyderabad sections**, so re-point every arrow in the copies.
5. **Keep question titles identical across chains.** Only locality and the Ownly-user page differ. This makes merging easy (§5).

### 3b. Form settings

| Setting | Value |
|---|---|
| Form title | **How young India orders food: 4-minute student survey** |
| Collect email addresses | OFF |
| Limit to 1 response | OFF |
| Show progress bar | ON |
| All questions | Required unless marked *Optional* · **every question has a title** |
| Number questions | Short answer → ⋮ Response validation → **Number → Between 0 and 60** (₹ amount: 0 and 10000) · error text "Please type a number, e.g. 3" |
| Confirmation message | "Done! Thank you 🙏 Please forward the link to friends aged 20–30 in any city, whether they order food online or not." |

### 3c. Build checklist (do all before sharing)

1. Search for "[" and "e.g." in the form. **No placeholder text may remain.**
2. Every question has a title, and every number field has validation.
3. **Walk 10 test paths** and check where each ends, then delete the test rows:
   - HYD under 20 → Not eligible
   - HYD non-orderer → never heard
   - HYD orderer → heard
   - HYD orderer → opened
   - HYD Ownly user
   - BLR non-user
   - BLR Ownly user
   - OTHER never heard
   - OTHER Ownly user
   - Age over 30 → Not eligible
4. Pilot with 5 people (at least 1 per city, and 1 Ownly user). Median time must be ≤ 4 min for non-users.

---

## 4. The form

### Page 0: Welcome (branch)

**Page description (paste exactly):**
> **Hi! Thanks for opening this 🙂**
> We're Product Management students studying **how people aged 20–30 order food online**: which apps they use, what they pay, and what makes them try a new app.
>
> ⏱ About **4 minutes**, mostly taps and a few numbers · 🔒 **Anonymous** · 🎓 Independent student research, not linked to any food app or restaurant.
>
> **Please answer based on what you actually do.** If you order food online, keep your food app's **order history** open. A couple of questions ask how many orders you placed. A good guess is fine.

**CITY. Which city do you live, study or work in on most days?** · Multiple choice · Go to section based on answer
- Hyderabad → *H1*
- Bengaluru → *B1*
- Another city → *O1*

---

### H1 [HYD] / B1 [BLR] / O1 [OTHER]: Where exactly

**LOC. [HYD] Which area?** · Multiple choice
- Gachibowli
- Financial District / Nanakramguda
- Kondapur
- Madhapur / HITEC City
- Manikonda
- Narsingi / Kokapet
- Serilingampally / Nallagandla / Tellapur
- Another part of Hyderabad

**LOC. [BLR] Which area?** · Multiple choice
- Koramangala / HSR Layout / BTM Layout
- Indiranagar / Domlur / Old Airport Road
- Whitefield / Marathahalli / Bellandur / Sarjapur Road
- Electronic City / Bommanahalli
- Jayanagar / JP Nagar / Banashankari
- Hebbal / Yelahanka / North Bengaluru
- Another part of Bengaluru

*(Koramangala/HSR/BTM are grouped because they were Ownly's 2025 pilot areas. That lets the dashboard compare pilot areas with the rest.)*

**LOC. [OTHER] Which city?** · Multiple choice
- Chennai
- Pune
- Mumbai
- Delhi NCR
- Kolkata
- Another Indian city
- Outside India

**AGE. How old are you?** · Multiple choice · Go to section based on answer *(last on the page)*
- Under 20 → *Not eligible*
- 20–22 → *H2 / B2 / O2 (same chain)*
- 23–25 → *same chain*
- 26–28 → *same chain*
- 29–30 → *same chain*
- Over 30 → *Not eligible*

---

### H2 / B2 / O2: About you

**OCC. Which best describes you right now?** · Multiple choice
- Student (undergraduate)
- Student (postgraduate / PhD)
- Working full-time
- Studying and working (internship / part-time)
- Looking for a job
- Other

**ORD. In the last 4 weeks, did you order food online for delivery at least once (any app, or directly from a restaurant)?** · Multiple choice · Go to section based on answer
- Yes → *H3 / B3 / O3*
- No → *H5 / B5 / O5 (Ownly page of the same chain)*

---

### H3 / B3 / O3: Your orders in the last 4 weeks (after section → next)

**Page description:** "Count **orders**, not items. Open each app → **Orders** to check. Type **0** if you didn't use that app."

**N_SW. Swiggy: how many orders in the last 4 weeks?** · Short answer · Number 0–60
**N_ZO. Zomato: how many orders in the last 4 weeks?** · Short answer · Number 0–60
**N_OW. Ownly (Rapido's food app, or food inside the Rapido app): how many orders in the last 4 weeks?** · Short answer · Number 0–60
**N_OT. Any other way (Toing, Magicpin, EatSure, or directly from a restaurant): how many orders in the last 4 weeks?** · Short answer · Number 0–60

---

### H4 / B4 / O4: Your most recent order (after section → H5 / B5 / O5)

**LO_APP. Which app did you use for your most recent food delivery order?** · Multiple choice
- Swiggy
- Zomato
- Ownly (or food inside the Rapido app)
- Toing
- Magicpin
- EatSure
- Directly from the restaurant
- Other

**LO_AMT. What was the total amount you paid for it?** · Short answer · Number 0–10000
*(Description: "₹, final amount after discounts, including all fees.")*

**LO_PPL. How many people was that order for?** · Multiple choice
- Just me
- 2 people
- 3–4 people
- 5 or more people

---

### H5 / B5: Ownly (branch)

**OW_STATUS. Ownly is a food delivery app by Rapido (the bike-taxi and auto app). Before today, which of these is true for you?** · Multiple choice · Go to section based on answer
- I hadn't heard of Ownly → *H6a / B6a*
- I'd heard of it, but never opened it → *H6b / B6b*
- I opened or browsed it, but didn't order → *H6c / B6c*
- I've ordered on Ownly → *H7 / B7*

### O5 [OTHER]: Ownly (branch)

**OW_STATUS. Ownly is a food delivery app by Rapido (the bike-taxi and auto app), available in Bengaluru and Hyderabad. Before today, which of these is true for you?** · Multiple choice · Go to section based on answer
- I hadn't heard of Ownly → *O6a*
- I'd heard of it → *O6a*
- I've ordered on Ownly (e.g. while in Bengaluru or Hyderabad) → *O7*

---

### H6a / B6a / O6a: Never heard (after section → *Last page*)

**Page description (neutral, factual):**
> **About Ownly:** a food delivery app from Rapido. Restaurants pay Ownly no commission, so menu prices are meant to match the restaurant's own prices. There's no platform, packaging or surge fee; you pay for the food plus delivery. **[HYD]** It started in Hyderabad in September 2026. **[BLR]** It has been available across Bengaluru since March 2026. **[OTHER]** It isn't available in most other cities yet.

**NH_TRIGGER. [HYD/BLR] Which ONE thing would most make you try Ownly for an order?** · **[OTHER] If Ownly launched in your city, which ONE thing would most make you try it?** · Multiple choice · Shuffle options ON
- A discount on my first order
- My usual restaurants being on it
- Seeing it's cheaper than Swiggy/Zomato for the same order
- A promise of a quick refund if an order goes wrong
- A friend telling me it works well
- Paying by cash on delivery or meal card (Pluxee / Zeta)
- Nothing, I'm happy with how I order now

---

### H6b / B6b: Heard, never opened (after section → *Last page*)

**SRC. Where did you first hear about Ownly?** · Multiple choice
- Inside the Rapido app
- Instagram / YouTube
- Friends, classmates or colleagues
- Hoardings, posters or street campaigns
- News, LinkedIn or Reddit
- Don't remember

**HD_REASON. What's the MAIN reason you haven't opened it?** · Multiple choice · Shuffle options ON
- I'm happy with my current app or membership
- I don't trust a new app yet
- I heard bad things about its delivery or support
- I don't think it's really cheaper
- Not sure it delivers to my area
- I don't want another app on my phone
- Just haven't got around to it

---

### H6c / B6c: Opened, didn't order (after section → *Last page*)

**SRC.** *(Same as H6b.)*

**OP_STOP. When you looked, what MAINLY stopped you from ordering?** · Multiple choice · Shuffle options ON
- My restaurants weren't there
- Prices weren't lower than my usual app
- A coupon on my usual app made that cheaper
- It didn't deliver to my address
- The delivery time looked too long
- I couldn't pay the way I wanted
- I was just looking around

---

### H7 [HYD] / B7 [BLR]: Ownly users (after section → *Last page*)

**Page description:** "A few questions about Ownly. Your answers are the most valuable part of this survey 🙏"

**SRC.** *(Same as H6b.)*

**US_WHERE. [HYD only] Where have you ordered on Ownly?** · Multiple choice
- Hyderabad only
- Bengaluru only
- Both

**US_FIRST. When did you place your FIRST Ownly order?** · Multiple choice
- **[HYD]** In the last 4 weeks · More than 4 weeks ago
- **[BLR]** In the last 4 weeks · 1–3 months ago · 3–6 months ago · More than 6 months ago

**US_PRIOR. How many Ownly orders did you place in the 4 weeks BEFORE the last 4 weeks (roughly 5–8 weeks ago)?** · Short answer · Number 0–60
*(Description: "Type 0 if none, or if your first Ownly order was in the last 4 weeks.")*

**US_ALT. Think of your most recent Ownly order. If Ownly didn't exist, what would you most likely have done instead?** · Multiple choice · Shuffle options ON
- Ordered the same on Swiggy or Zomato
- Ordered on another app (Toing, Magicpin, etc.)
- Ordered directly from the restaurant
- Cooked, or eaten at home / mess / hostel
- Gone out to eat
- Skipped it or had a snack

**US_PMF. How would you feel if you could no longer use Ownly?** · Multiple choice
- Very disappointed
- Somewhat disappointed
- Not disappointed

**US_LAPSE. [BLR only] If you order on Ownly less than you used to, what's the MAIN reason?** · Multiple choice · Shuffle options ON (keep the first option first if your form allows; otherwise accept shuffle)
- I don't order less than before
- The restaurants I want aren't there
- Late or failed deliveries
- Refund or support problems
- Prices are no longer clearly lower
- Offers ended
- Went back to my Swiggy One / Zomato Gold membership

**US_CHANGE. What ONE change would make you order more on Ownly?** · Multiple choice · Shuffle options ON
- More restaurants
- Faster delivery
- More reliable, on-time delivery
- Quicker refunds and support
- A bigger price gap vs other apps
- More offers and coupons
- Cash on delivery or meal-card payment

### O7 [OTHER]: Ownly users from other cities (after section → *Last page*)

**US_WHERE. Where did you order on Ownly?** · Multiple choice · Bengaluru · Hyderabad · Both
**US_PMF.** *(Same as H7.)*

---

### Last page (all chains; after section → *Submit*)

**Page description:** "That's it, thank you! 🙏"

**INTERVIEW. *Optional:* Can we message you for a 10-minute chat about how you order food?** · Short answer · Not required
*(Description: "Leave your WhatsApp number if yes. It's only used for the chat and kept separately from your answers.")*

### Not eligible (after section → *Submit*)

**Page description:** "Thanks so much for your time! 🙏 This survey is for people aged **20–30**. Please press **Submit**, and forward the link to friends in that age group."

---

## 5. Cleaning: merge, derive, check

### 5a. Merge the three chains
The sheet has one column per chain for each repeated question (e.g. three "Swiggy: how many orders" columns). For each ID, take the **first non-empty value** across its chain columns. Set `city` from the CITY answer.

### 5b. Derived fields

| Field | Rule |
|---|---|
| `tot` | N_SW + N_ZO + N_OW + N_OT (0 if ORD = No) |
| `ownly_user_4wk` | N_OW ≥ 1 |
| `gachibowli_area` | CITY = Hyderabad and LOC ≠ "Another part of Hyderabad" |
| `blr_pilot_area` | CITY = Bengaluru and LOC = "Koramangala / HSR Layout / BTM Layout" |
| `segment` | OCC → student (UG, PG) · working (full-time) · working student · job seeker / other |
| `ownly_city` | Hyderabad path: US_WHERE; Bengaluru path: "Bengaluru"; Other path: US_WHERE |

### 5c. Quality checks (1 point each; exclude a response with ≥ 2 points)

| # | Flag |
|---|---|
| C1 | LO_APP = Swiggy but N_SW = 0 (same for Zomato → N_ZO, Ownly → N_OW) |
| C2 | N_OW ≥ 1 but OW_STATUS ≠ "I've ordered on Ownly" |
| C3 | ORD = Yes but `tot` = 0; or `tot` > 60 |
| C4 | US_FIRST = "In the last 4 weeks" but US_PRIOR ≥ 1 |
| C5 | Hyderabad path, US_WHERE = "Hyderabad only", US_FIRST = "More than 4 weeks ago" (before the Hyderabad launch) |
| C6 | LO_PPL = "Just me" and LO_AMT > 1500 |
| D | Identical answers submitted within 10 minutes → keep the first |

---

## 6. Sampling targets (so the dashboard has something to show)

| City | Target eligible responses | Of which Ownly users | Where to share |
|---|---|---|---|
| **Hyderabad** | **≥ 80** (≥ 60 in the Gachibowli area) | As many as possible; expect few | IIIT-H, UoH, ISB groups; PG/co-living groups in Gachibowli/Kondapur; office groups in Financial District/HITEC City |
| **Bengaluru** | **≥ 80** | **≥ 30** (needed for the loyalty KPIs) | Koramangala/HSR/BTM and Whitefield/ORR apartment, PG and office groups; college groups (Christ, IIIT-B, PES, RVCE) |
| **Other** | **≥ 40** | — | Friends and classmates in other cities |

**Dashboard display rule:** a KPI tile shows a value only when its base n ≥ 30. Between 10 and 29 it shows "directional (n = …)". Below 10 it shows "not enough data".

---

## 7. Sharing messages

### 7a. Rules

| ❌ Never write | Why | ✅ Write instead |
|---|---|---|
| "Ownly", "Rapido", "zero commission", "new app" | Attracts fans and critics, which inflates or deflates Ownly KPIs | "how people choose and use food delivery apps" |
| "hidden fees", "Swiggy/Zomato overcharge" | Leads the answers | "which apps you use and what you pay" |
| "only if you order food online" | Removes non-orderers, which breaks Penetration Share | "whether you order often, rarely or never" |
| "only for Hyderabad" | We need Bengaluru and other cities too | "20–30, in any city" |
| "takes 1 minute" | Untrue; people quit | "about 4 minutes" |
| Explaining questions to people | Biases answers | Just share the link |

### 7b. WhatsApp group message

> Hi everyone! 👋 Sorry for the group message, and thank you for reading.
>
> I'm a Product Management student, and for our Market Research project we're studying **how people aged 20–30 order food online**: which apps they use, how often, what they pay, and what makes them try a new app.
>
> 👉 [FORM LINK]
>
> ⏱ **About 4 minutes**, mostly taps and a few numbers
> 🔒 **Anonymous**: no name, no email
> 🎓 Independent student research, not linked to any food app or restaurant
>
> **Who can fill it:** anyone **aged 20–30**, in **Bengaluru, Hyderabad or any other city**, **whether you order food online often, rarely or never.**
>
> **Two small requests:**
> 1️⃣ Answer based on **what you actually do**. There are no right or wrong answers.
> 2️⃣ If you order food online, **keep your app's order history open**. A couple of questions ask how many orders you placed.
>
> Please **forward it** to friends and colleagues aged 20–30 🙏 We're collecting answers until **[DAY, DATE, TIME]**. Thank you!

### 7c. Personal message

> Hey [Name]! Hope you're doing well 🙂 Small favour: I'm doing a market research project for my PDM course on **how people our age order food online**. Could you fill in a quick survey? About **4 minutes**, anonymous.
> 👉 [FORM LINK]
> If you order food online, keep your order history handy (it asks how many orders you placed). And if you can, forward it to 2–3 friends aged 20–30, in any city. Thanks a ton! 🙏

### 7d. LinkedIn post

> **Aged 20–30 and living in Bengaluru, Hyderabad or anywhere in India? I'd value 4 minutes of your time.**
>
> For my Product Management programme, our team is researching **how young professionals and students choose food delivery apps**: how often they order, what they pay, and what makes them try something new.
>
> 🕒 About 4 minutes · 🔒 Anonymous · 📱 Built for your phone
> 👉 [FORM LINK]
>
> Everyone counts, including people who rarely order online. I'll share a summary of what we learn. Reposts are hugely appreciated 🙌
> #ProductManagement #MarketResearch #Bengaluru #Hyderabad

### 7e. Reminder

> Thank you to everyone who filled in the food delivery survey! 🙏 We still need more answers from **[Hyderabad / Bengaluru / working professionals / people who rarely order online]**. If you're 20–30 and haven't filled it yet: 👉 [FORM LINK] (about 4 min). Already did it? Forwarding it is the best help!

### 7f. Reply templates

| If someone asks… | Reply |
|---|---|
| "Is this for Swiggy / Zomato / some app?" | "No, it's independent student research for our course, about how people choose food apps in general." |
| "I don't order food online, should I fill it?" | "Yes please! It's even shorter for you, and those answers matter just as much." |
| "I don't remember how many orders" | "A good guess is fine, or check your app's order history. It takes a few seconds." |
| "I'm 31 / 19" | "Thanks for offering! It's only for 20–30, but please forward it to someone in that range." |
| "Why do you want my number?" | "It's optional, only if you're happy to chat for 10 minutes later." |
