# Build Guide: Survey v7 in Google Forms (lean edition)

**What you're building:** one Google Form, **one path for every city**, **8 sections**.
**Time:** about 30 minutes to build, plus 10 minutes to test.
**Respondent time:** about 3–4 minutes (longest path: 20 questions on 7 pages; most people see 12–15).

> **v7 = v6 with the load removed.** Testers found v6 overwhelming: 32 sections, up to 33 questions, and
> lists of 7–8 options. v7 keeps **what people actually do** (how often they order, what they paid, where
> they are in the Ownly funnel, whether they came back) plus the one H₀ question. It cuts questions that ask
> the same thing twice and questions that ask people to guess about imaginary futures.
> See "What v7 cut, and why" at the end, and `_ops/decisions.md` D11.

**Build rules:** paste text exactly as written, because the analysis matches on wording. **Required: ON** for
every question unless it says otherwise. Settings (Part 2) are the same as v6.

---

## Part 0 · The form at a glance

| # | Section | Questions | Goes to |
|---|---|---|---|
| 1 | *(title card)* | How old are you? | Under 20 / Over 30 → **8** · 20–25 / 26–30 → **2** |
| 2 | About you | Where you live · What you do · Membership · **Ordered in last 4 weeks?** | Yes → **3** · No → **4** |
| 3 | Your recent orders | Orders per app (one grid) · Amount paid last time · Did it feel fair? | → **4** |
| 4 | A few quick choices | 3 either-or trade-offs · *Two services* text block · **If only one existed, which?** · Why *(optional)* | → **5** |
| 5 | Ownly | **Before today, which is true?** | Hadn't heard → **7** · Heard / opened → **6** · Ordered → **6b** |
| 6 | What's holding you back | Main reason (1 question) | → **7** |
| 6b | Ownly users | First order · Orders 5–8 weeks ago · If Ownly didn't exist · Disappointment · One change | → **7** |
| 7 | Last question | WhatsApp number *(optional)* | Submit |
| 8 | Thank you! | *(not eligible, no questions)* | Submit |

> Section **6b** is just the 7th section in the editor. The real numbering is 1, 2, 3, 4, 5, 6, **7 = Ownly users**,
> **8 = Last question**, **9 = Thank you!** In Part 4, always **pick branch targets by name**, never by number.

**What each respondent sees:**

| Who | Pages | Questions |
|---|---|---|
| Hasn't ordered in 4 weeks, hasn't heard of Ownly | 5 | 12 |
| Orders online, hasn't heard of Ownly | 6 | 15 |
| Orders online, heard of Ownly but hasn't ordered | 7 | 16 |
| Ownly user | 7 | 20 |

---

## Part 1 · Create the form

**Form title**
```
How young India orders food: 4-minute student survey
```

**Form description**
```
Hi! Thanks for opening this 🙂
We're Product Management students studying how people aged 20–30 order food online.

⏱ About 4 minutes, mostly taps · 🔒 Anonymous · 🎓 Independent student research, not linked to any food app or restaurant.

Please answer based on what you actually do. A good guess is fine.
```

## Part 2 · Settings

Same as v6: quiz OFF · don't collect emails · limit to 1 response OFF · progress bar ON · shuffle question
order OFF · required by default ON.

**Confirmation message**
```
Done! Thank you 🙏 Please forward the link to friends aged 20–30 in any city, whether they order food online or not.
```

---

## Part 3 · Build the sections

### SECTION 1 · Title card

#### Q1 · Age
- **Multiple choice** · **Go to section based on answer: ON**

**Question**
```
How old are you?
```
**Options**
```
Under 20
20–25
26–30
Over 30
```

---

### SECTION 2 · About you

**Section title**
```
About you
```

#### Q2 · Where
- **Dropdown**. A dropdown looks short even with many entries, and people just scroll to their city.
- This single question replaces v6's separate city, area and "which city" questions, **and the three duplicated city paths**.

**Question**
```
Where do you live, study or work on most days?
```
**Options**
```
Hyderabad · Gachibowli / Financial District
Hyderabad · Kondapur / Madhapur / HITEC City
Hyderabad · Manikonda / Narsingi / Kokapet
Hyderabad · Another area
Bengaluru · Koramangala / HSR / BTM
Bengaluru · Indiranagar / Domlur
Bengaluru · Whitefield / Marathahalli / Bellandur
Bengaluru · Another area
Chennai
Pune
Mumbai
Delhi NCR
Another city
```

#### Q3 · Occupation
- **Multiple choice**

**Question**
```
Which best describes you right now?
```
**Options**
```
Student
Working full-time
Studying and working (internship / part-time)
Other
```

#### Q4 · Membership
- **Multiple choice** (not checkboxes; "Both" covers the overlap)

**Question**
```
Do you have a paid food delivery membership right now?
```
**Options**
```
Swiggy One
Zomato Gold
Both
Neither
```

#### Q5 · Ordered recently (keep this LAST in the section)
- **Multiple choice** · **Go to section based on answer: ON**

**Question**
```
In the last 4 weeks, did you order food online for delivery at least once (any app, or directly from a restaurant)?
```
**Options**
```
Yes
No
```

---

### SECTION 3 · Your recent orders

**Section title**
```
Your recent orders
```

#### Q6 · Orders per app
- **Multiple choice grid** · ⋮ → **Require a response in each row: ON**
- One grid replaces v6's four typed number questions. Tapping bands is quicker than typing, and still measures real behaviour.

**Question**
```
In the last 4 weeks, roughly how many orders did you place on each?
```
**Rows**
```
Swiggy
Zomato
Ownly (or food in the Rapido app)
Other apps or directly from a restaurant
```
**Columns**
```
0
1–2
3–5
6+
```

#### Q7 · Amount paid
- **Short answer** · ⋮ → **Response validation**: Number → Between → `0` and `10000`
- Error text: `Please type the amount as a number, e.g. 280`

**Question**
```
Your most recent order: what was the total amount you paid?
```
**Question description**
```
₹, final amount after discounts, including all fees.
```

#### Q8 · Did it feel fair
- **Multiple choice**

**Question**
```
Did that amount feel fair for what you got?
```
**Options**
```
Yes, it felt fair
No, the extra charges on top were too much
No, the food itself was overpriced
I didn't really check
```

---

### SECTION 4 · A few quick choices

**Section title**
```
A few quick choices
```
**Section description**
```
Made-up examples, not real offers. Assume everything else is the same.
```

#### Q9 · Price vs speed
- **Multiple choice** · ⋮ → **Shuffle option order: ON**

**Question**
```
Same restaurant, same food. Which would you choose?
```
**Options**
```
₹260 total, arrives in 30 minutes
₹230 total, arrives in 45 minutes
```

#### Q10 · Price vs reliability
- **Multiple choice** · **Shuffle: ON**

**Question**
```
Same restaurant, same food, same delivery time. Which would you choose?
```
**Options**
```
₹260 total, late in about 1 of every 10 orders
₹230 total, late in about 3 of every 10 orders
```

#### Q11 · Price vs restaurants
- **Multiple choice** · **Shuffle: ON**

**Question**
```
Same delivery time. Which would you choose?
```
**Options**
```
₹260 total, has most of your usual restaurants
₹230 total, has only a few of your usual restaurants
```

#### Text block · Two services
- ⊕ toolbar → **Tt (Add title and description)**, placed **after Q11**.
- P and Q must look identical: same number of bullets, same format.

**Title**
```
Two services
```
**Description**
```
Neither exists exactly as described. Please read both.

SERVICE P — "Same food. Smaller final bill."
• Menu prices are the restaurant's own prices, not marked up
• No platform, packaging or surge fee, just one flat delivery fee
• The total you see is the total you pay

SERVICE Q — "Your local regulars, and dinner that actually turns up."
• The local biryani, tiffin and meals places you already order from
• The delivery time shown is the time it actually takes
• If an order goes wrong, your money back fast
```

#### Q12 · Forced choice ⭐ THE H₀ QUESTION
- **Multiple choice** · **Shuffle: ON**

**Question**
```
If only one of them existed where you live, which would you start using?
```
**Options**
```
Service P
Service Q
I genuinely can't choose between them
```

#### Q13 · Why
- **Short answer** · **Required: OFF**

**Question**
```
In one line, what made you pick that one?
```

---

### SECTION 5 · Ownly

**Section title**
```
Ownly
```

#### Q14 · Ownly status
- **Multiple choice** · **Go to section based on answer: ON**

**Question**
```
Ownly is a food delivery app by Rapido (the bike-taxi app). Before today, which of these is true for you?
```
**Options**
```
I hadn't heard of Ownly
I'd heard of it, but never opened it
I opened or browsed it, but didn't order
I've ordered on Ownly
```

---

### SECTION 6 · What's holding you back

**Section title**
```
What's holding you back
```

#### Q15 · Main barrier
- **Multiple choice** · **Shuffle: ON**
- One question for both "never opened" and "opened but didn't order". v6 asked these on two separate pages with 7 options each.

**Question**
```
What's the MAIN reason you haven't ordered on Ownly?
```
**Options**
```
I'm happy with my current app or membership
I don't think it's really cheaper
My usual restaurants aren't on it
I don't trust a new app with delivery or refunds yet
It doesn't deliver to my area, or I'm not sure it does
I just haven't got around to it
```

---

### SECTION 7 · Ownly users

**Section title**
```
Ownly users
```
**Section description**
```
Your answers here are the most valuable part of this survey 🙏
```

#### Q16 · First order
- **Multiple choice**

**Question**
```
When did you place your FIRST Ownly order?
```
**Options**
```
In the last 4 weeks
1–3 months ago
More than 3 months ago
```

#### Q17 · Orders 5–8 weeks ago
- **Multiple choice**

**Question**
```
How many Ownly orders did you place in the 4 weeks BEFORE the last 4 weeks (roughly 5–8 weeks ago)?
```
**Options**
```
0
1–2
3–5
6+
```

#### Q18 · If Ownly didn't exist
- **Multiple choice** · **Shuffle: ON**

**Question**
```
Think of your most recent Ownly order. If Ownly didn't exist, what would you have done instead?
```
**Options**
```
Ordered the same on Swiggy or Zomato
Ordered another way (other app or directly from the restaurant)
Cooked, or eaten at home / mess / hostel
Gone out to eat
Skipped it or had a snack
```

#### Q19 · Disappointment
- **Multiple choice** · Shuffle OFF

**Question**
```
How would you feel if you could no longer use Ownly?
```
**Options**
```
Very disappointed
Somewhat disappointed
Not disappointed
```

#### Q20 · One change
- **Multiple choice** · **Shuffle: ON**

**Question**
```
What ONE change would make you order more on Ownly?
```
**Options**
```
More of my restaurants
More reliable, on-time delivery
Quicker refunds and support
A bigger price gap vs other apps
More offers and coupons
```

---

### SECTION 8 · Last question

**Section title**
```
Last question
```

#### Q21 · Interview volunteer
- **Short answer** · **Required: OFF**

**Question**
```
Optional: Can we message you for a 10-minute chat about how you order food?
```
**Question description**
```
Leave your WhatsApp number if yes. It's only used for the chat and kept separately from your answers.
```

---

### SECTION 9 · Thank you!

**Section title**
```
Thank you!
```
**Section description**
```
Thanks so much for your time! 🙏 This survey is for people aged 20–30. Please press Submit, and forward the link to friends in that age group.
```

---

## Part 4 · Branching (pick targets by NAME)

**Answer-based** (⋮ → Go to section based on answer):

| Question | Answer → section |
|---|---|
| Q1 How old are you? | Under 20 → **Thank you!** · 20–25 → **About you** · 26–30 → **About you** · Over 30 → **Thank you!** |
| Q5 Ordered in last 4 weeks | Yes → **Your recent orders** · No → **A few quick choices** |
| Q14 Ownly status | Hadn't heard → **Last question** · Heard, never opened → **What's holding you back** · Opened, didn't order → **What's holding you back** · Ordered → **Ownly users** |

**Page-based** (the "After section" dropdown at the bottom):

| After section | Go to |
|---|---|
| Your recent orders | A few quick choices |
| A few quick choices | Ownly |
| What's holding you back | **Last question** |
| Ownly users | **Last question** |
| Last question | **Submit form** |

---

## Part 5 · Test 5 paths, then delete the test responses

| # | Answers | Pages you should see |
|---|---|---|
| 1 | Age **Under 20** | Thank you! |
| 2 | 20–25 · ordered **No** · Ownly **hadn't heard** | About you → Quick choices → Ownly → Last question |
| 3 | 26–30 · ordered **Yes** · Ownly **heard, never opened** | About you → Recent orders → Quick choices → Ownly → Holding you back → Last question |
| 4 | Same as 3, Ownly **opened, didn't order** | …same as 3 |
| 5 | Ordered **Yes** · Ownly **I've ordered** | …Ownly → Ownly users (5 questions) → Last question |

Also check: the grid doesn't let you skip a row · on a phone, the grid fits without sideways scrolling and the
Two services text reads without zooming · **time path 5: it should take under 5 minutes.**

Then delete test responses from **Responses → ⋮ → Delete all responses**, and from the linked sheet.
Link the sheet as `Ownly Survey v7 responses`. Sharing messages from v6 Part 10 still work; change
"6 minutes" to **"4 minutes"**.

---

## Appendix · What v7 cut, and why

| Cut from v6 | Why |
|---|---|
| **3 duplicated city paths (32 → 9 sections)** | One "Where do you live" dropdown carries city and area. The analysis gets city from the text before `·` |
| Separate city, area and "which city?" questions | Merged into Q2 |
| 4 typed order counts | One tap grid (Q6). **Trade-off:** bands, not exact counts; share-of-orders uses band midpoints 0 / 1.5 / 4 / 8 |
| Last-order app, people on the order | The grid already shows which apps people use. The price audit measures fees per order better than a recalled headcount does |
| Switching threshold (8 options) | Repeated the three trade-offs, which test price sensitivity one lever at a time |
| **Try P? / Try Q?** (two 5-point scales) | Asked the same thing as the forced choice. **Consequence:** D3's secondary McNemar test goes; the forced-choice binomial test stays as the primary test and is unchanged |
| Would you stay after the offer ends · Do low prices last? | Guesses about imaginary futures, not behaviour. Q17 (orders 5–8 weeks ago) measures real repeat use |
| "Which ONE thing would make you try Ownly" (7 options) | Repeated Q9–Q12, which test the same levers without naming a brand |
| "Where did you first hear about Ownly" (asked on 3 pages) | Marketing attribution, not ordering behaviour. The fake-door channel links give better attribution |
| "Why not opened" + "What stopped you ordering" (2 pages, 7 options each) | Merged into Q15 (6 options) |
| "Where have you ordered on Ownly" · Bengaluru "why you order less" | Q2 already gives city. "Order less" overlapped with Q20 "one change" |
| Service Q's "Your **Hyderabad** regulars" headline | Both cities now see identical wording, which makes the city comparison cleaner. Service Q is now 3 bullets, matching P ("Fair prices" bullet removed), which fixes v6's bullet-count asymmetry |

**Phrases the analysis matches on:** `How old are you` · `Where do you live, study or work` · `best describes you` ·
`paid food delivery membership` · `order food online for delivery at least once` · `how many orders did you place on each` ·
`total amount you paid` · `feel fair` · `arrives in 30 minutes` · `1 of every 10 orders` · `most of your usual restaurants` ·
`If only one of them existed` · `what made you pick that one` · `Before today, which of these is true` ·
`MAIN reason you haven't ordered` · `FIRST Ownly order` · `4 weeks BEFORE the last 4 weeks` · `If Ownly didn't exist` ·
`no longer use Ownly` · `ONE change would make you order more`.

> **If v6 responses have already come in, don't edit that form.** Build v7 as a new form, close v6, and treat
> v6 as wave 1. Log the cut-over time in `_ops/decisions.md`.
