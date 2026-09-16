# Build Guide: Survey v6 in Google Forms (copy-paste edition)

**What you're building:** one Google Form, three city paths (Hyderabad, Bengaluru, Other city), **32 sections**.
**Time:** about 90–105 minutes to build, plus 15 minutes to test.
**You need:** a Google account, a laptop, and this file open next to Google Forms.

> **v6 = v5 + the H₀ instrument.** v5 measured the Ownly funnel well but had no way to test the project's
> primary hypothesis. v6 keeps every v5 question and adds two brand-blind sections per city: **Quick choices**
> (three price trade-offs + the switching threshold) and **Two services** (the Bengaluru-style vs
> Hyderabad-localized proposition test). Full rationale in `_ops/decisions.md` D9.
> If you already built v5, **don't rebuild** — jump to **Part 12: upgrading an existing v5 form**.
>
> **🆕 Rapido add-on (2026-09-17):** two one-tap questions: **S3-Q3 Rapido usage** and **S8-Q1 food inside the Rapido app**.
> No new sections and no branching changes. **Already built v6?** Add S3-Q3 to all three *About you* sections
> (above "ordered online recently") and S8-Q1 to all three *Ownly* sections (above "Before today…"). The Other-city
> Ownly section gets the same question. Then re-run test paths 3, 7 and 9.

---

## How to use this guide

Every piece of text you need is in a **grey box**. Hover over a box and click the copy icon (or select it and press Ctrl/Cmd + C), then paste into Google Forms.

| Grey box labelled | Paste it into |
|---|---|
| **Form title** / **Form description** | The top card of the form |
| **Section title** / **Section description** | The header of a section (the bar that says "Section 3 of 32") |
| **Question** | The question text box ("Untitled Question") |
| **Question description** | ⋮ (three dots, bottom right of the question) → **Description** → the small box under the title |
| **Options** | Click the **first option box** ("Option 1") and paste **all lines at once**. Google Forms turns each line into its own option. If they land as one option, paste line by line. |
| **Error text** | ⋮ → **Response validation** → the "Custom error text" box |

> **Golden rule:** paste text **exactly**. The analysis scripts and the dashboard find questions and answers by their wording. If you reword them, those KPIs show "Not in this form".

**Where things are in the editor:**

| You need | Where to click |
|---|---|
| Add a question | **⊕** in the floating toolbar on the right |
| Add a section (new page) | The **two-rectangle icon** at the bottom of the floating toolbar |
| Question type | Dropdown at the top right of each question |
| Required | Toggle at the bottom right of each question |
| Description / Response validation / Go to section based on answer / Shuffle option order | **⋮** at the bottom right of each question |
| Duplicate / Move / Delete a section | **⋮** at the top right of the section header |
| Where a page goes next | **After section X** dropdown at the bottom of each section |
| Preview | **👁** at the top of the page |

---

## Contents

| Part | What you do | Time |
|---|---|---|
| 0 | The form at a glance: every section and question, then the branching | read first |
| 1 | Create the form, title and welcome text | 5 min |
| 2 | Settings | 5 min |
| 3 | Hyderabad path (sections 1–12), full copy-paste text | 40 min |
| 4 | Bengaluru path (sections 13–23): duplicate, then paste the changes | 15 min |
| 5 | Other-city path (sections 24–30): duplicate, then paste the changes | 10 min |
| 6 | Last two pages (sections 31–32) | 3 min |
| 7 | Set every branch | 12 min |
| 8 | Connect Google Sheets | 2 min |
| 9 | Test all 11 paths, then delete test responses | 15 min |
| 10 | Share: link and copy-paste messages | 5 min |
| 11 | Close the survey and analyse | 5 min |
| 12 | **Upgrading an existing v5 form to v6** (skip Parts 3–6 if you do this) | 25 min |
| A | Final checklist and exact wording the analysis needs | — |

---

## Part 0 · The form at a glance

### 0A. All sections and questions

🆕 = new in v6.

| # | Section title | Questions (short) |
|---|---|---|
| 1 | *(form title card)* | Which city do you live, study or work in on most days? |
| **Hyderabad** | | |
| 2 | Hyderabad · Your area | Which area? · How old are you? |
| 3 | Hyderabad · About you | Which best describes you right now? · 🆕 Which memberships do you have? · 🆕 How often did you use Rapido? · Ordered food online in the last 4 weeks? |
| 4 | Hyderabad · Your orders | Swiggy / Zomato / Ownly / Any other way: how many orders in the last 4 weeks? (4 numbers) |
| 5 | Hyderabad · Your last order | Which app? · Total amount paid? · How many people? · 🆕 Did the bill feel fair? |
| 6 🆕 | Hyderabad · Quick choices | 3 either-or trade-offs · How much cheaper before you'd switch? |
| 7 🆕 | Hyderabad · Two services | Try P? · Try Q? · **If only one existed, which?** · Why? · Would you stay after the offer ends? · Do low prices last? |
| 8 | Hyderabad · Ownly | 🆕 Seen a food option inside the Rapido app? · Before today, which of these is true for you? (4 options) |
| 9 | Hyderabad · About Ownly | Which ONE thing would most make you try Ownly? |
| 10 | Hyderabad · A bit more about Ownly | Where did you first hear about Ownly? · MAIN reason you haven't opened it? |
| 11 | Hyderabad · A bit more about Ownly (2) | Where did you first hear about Ownly? · What MAINLY stopped you from ordering? |
| 12 | Hyderabad · Ownly users | Where first heard · Where have you ordered · FIRST order (2 options) · Orders 5–8 weeks ago · If Ownly didn't exist · How would you feel without Ownly · ONE change |
| **Bengaluru** | | |
| 13 | Bengaluru · Your area | same as 2 (**Bengaluru areas**) |
| 14 | Bengaluru · About you | same as 3 |
| 15 | Bengaluru · Your orders | same as 4 |
| 16 | Bengaluru · Your last order | same as 5 |
| 17 🆕 | Bengaluru · Quick choices | same as 6 |
| 18 🆕 | Bengaluru · Two services | same as 7 |
| 19 | Bengaluru · Ownly | same as 8 |
| 20 | Bengaluru · About Ownly | same as 9 (**Bengaluru description**) |
| 21 | Bengaluru · A bit more about Ownly | same as 10 |
| 22 | Bengaluru · A bit more about Ownly (2) | same as 11 |
| 23 | Bengaluru · Ownly users | Where first heard · FIRST order (**4 options**) · Orders 5–8 weeks ago · If Ownly didn't exist · How would you feel without Ownly · **Why you order less** · ONE change *(no "Where have you ordered")* |
| **Other city** | | |
| 24 | Other city · Your city | **Which city?** · How old are you? |
| 25 | Other city · About you | same as 3 |
| 26 | Other city · Your orders | same as 4 |
| 27 | Other city · Your last order | same as 5 |
| 28 | Other city · Ownly | Before today, which of these is true for you? (**3 options**) |
| 29 | Other city · About Ownly | **If Ownly launched in your city**, which ONE thing would most make you try it? |
| 30 | Other city · Ownly users | **Where did you order on Ownly?** · How would you feel without Ownly |
| **Closing** | | |
| 31 | Last question | Optional: WhatsApp number for a 10-minute chat |
| 32 | Thank you! | *(not-eligible page, no questions)* |

> **Other city deliberately skips sections 6 and 7.** It is appendix-only context, never used for the
> Hyderabad hypothesis, so it stays short. Hyderabad and Bengaluru both get the proposition test — Bengaluru
> is the benchmark, and seeing whether people who have actually used Ownly choose differently is worth the
> two extra pages.

### 0B. Branching

**Answer-based** (⋮ → **Go to section based on answer** on these questions):

| Section | Question | Answer → go to section |
|---|---|---|
| 1 | Which city… | Hyderabad → **2** · Bengaluru → **13** · Another city → **24** |
| 2 | How old are you? | Under 20 → **32** · 20–22 / 23–25 / 26–28 / 29–30 → **3** · Over 30 → **32** |
| 3 | Ordered online in last 4 weeks? | Yes → **4** · No → **6** |
| 8 | Ownly status | Hadn't heard → **9** · Heard, never opened → **10** · Opened, didn't order → **11** · Ordered → **12** |
| 13 | How old are you? | Under 20 → **32** · 20–30 bands → **14** · Over 30 → **32** |
| 14 | Ordered online in last 4 weeks? | Yes → **15** · No → **17** |
| 19 | Ownly status | Hadn't heard → **20** · Heard, never opened → **21** · Opened, didn't order → **22** · Ordered → **23** |
| 24 | How old are you? | Under 20 → **32** · 20–30 bands → **25** · Over 30 → **32** |
| 25 | Ordered online in last 4 weeks? | Yes → **26** · No → **28** |
| 28 | Ownly status (3 options) | Hadn't heard → **29** · Heard of it → **29** · Ordered → **30** |

**Page-based** (the **After section** dropdown at the bottom of a section):

| After section | Go to |
|---|---|
| 4 → 5 · 5 → 6 · **6 → 7** · **7 → 8** | the next section |
| 15 → 16 · 16 → 17 · **17 → 18** · **18 → 19** | the next section |
| 26 → 27 · 27 → 28 | the next section |
| 9, 10, 11, 12, 20, 21, 22, 23, 29, 30 | **31 Last question** |
| 31 | **Submit form** |
| 32 | *(no dropdown — it's the last section, so it submits automatically)* |

> Note the one non-obvious route: someone who says **No** to "ordered in the last 4 weeks" skips the order
> counts and the last-order page, but **still sees Quick choices and Two services**. That is deliberate —
> people who rarely order are exactly the ones a new app has to win, and the proposition test is the only
> question we have for them.

---

## Part 1 · Create the form (5 min)

1. Go to **forms.google.com** → **Blank form**.
2. Sign in with the **team** Google account, not a personal one you'll lose access to.
3. Click "Untitled form" and paste:

**Form title**
```
How young India orders food: 6-minute student survey
```

4. Click "Form description" and paste:

**Form description**
```
Hi! Thanks for opening this 🙂
We're Product Management students studying how people aged 20–30 order food online: which apps they use, what they pay, and what makes them try a new app.

⏱ About 6 minutes, mostly taps and a few numbers · 🔒 Anonymous · 🎓 Independent student research, not linked to any food app or restaurant.

Please answer based on what you actually do. If you order food online, keep your food app's order history open. A couple of questions ask how many orders you placed. A good guess is fine.
```

5. Leave the empty sample question for now. You'll turn it into the first question in Part 3.

---

## Part 2 · Settings (5 min)

Click the **Settings** tab (top centre).

| Area | Setting | Set to |
|---|---|---|
| Quizzes | Make this a quiz | **OFF** |
| Responses | Collect email addresses | **Do not collect** |
| Responses | Allow response editing | **OFF** |
| Responses | Limit to 1 response | **OFF** (ON forces a Google sign-in) |
| Presentation | Show progress bar | **ON** |
| Presentation | Shuffle question order | **OFF** |
| Presentation | Show link to submit another response | **OFF** |
| Presentation | View results summary | **OFF** |
| Defaults | Collect email addresses by default | **OFF** |
| Defaults | Make questions required by default | **ON** |

Presentation → **Confirmation message** → **Edit** → paste:

**Confirmation message**
```
Done! Thank you 🙏 Please forward the link to friends aged 20–30 in any city, whether they order food online or not.
```

Go back to the **Questions** tab.

---

## Part 3 · Hyderabad path (sections 1–12)

> Build in this order. Where a question says **Branching: ON**, only tick **Go to section based on answer** now. You'll pick the target sections in Part 7, once they all exist.

---

### SECTION 1 · Welcome (the top card)

#### S1-Q1 · City
- **Type:** Multiple choice · **Required:** ON · **Branching:** ON

**Question**
```
Which city do you live, study or work in on most days?
```
**Options**
```
Hyderabad
Bengaluru
Another city
```

---

### SECTION 2 · Hyderabad · Your area

Click **Add section** (two-rectangle icon).

**Section title**
```
Hyderabad · Your area
```
**Section description:** leave empty

#### S2-Q1 · Area
- **Type:** Multiple choice · **Required:** ON

**Question**
```
Which area?
```
**Options**
```
Gachibowli
Financial District / Nanakramguda
Kondapur
Madhapur / HITEC City
Manikonda
Narsingi / Kokapet
Serilingampally / Nallagandla / Tellapur
Another part of Hyderabad
```

#### S2-Q2 · Age (keep it last in this section)
- **Type:** Multiple choice · **Required:** ON · **Branching:** ON

**Question**
```
How old are you?
```
**Options**
```
Under 20
20–22
23–25
26–28
29–30
Over 30
```

---

### SECTION 3 · Hyderabad · About you

**Section title**
```
Hyderabad · About you
```
**Section description:** leave empty

#### S3-Q1 · Occupation
- **Type:** Multiple choice · **Required:** ON

**Question**
```
Which best describes you right now?
```
**Options**
```
Student (undergraduate)
Student (postgraduate / PhD)
Working full-time
Studying and working (internship / part-time)
Looking for a job
Other
```

#### 🆕 S3-Q2 · Memberships
- **Type:** Checkboxes · **Required:** ON · Shuffle **OFF**

**Question**
```
Which food delivery memberships do you have right now?
```
**Question description**
```
Tick all that apply.
```
**Options**
```
Swiggy One (any plan)
Zomato Gold
Another food delivery membership
None
Not sure
```

> **Why this is here:** a paid membership is the strongest reason not to switch apps — it shows up in this
> survey twice already, as "happy with my current app or membership" and "went back to my Swiggy One /
> Zomato Gold membership". Asking it directly turns that from an anecdote into a segment you can cut every
> other answer by: do members choose Service P less often? Do they need a bigger saving to switch?

#### 🆕 S3-Q3 · Rapido usage
- **Type:** Multiple choice · **Required:** ON · Shuffle **OFF**

**Question**
```
In the last 4 weeks, how often did you use Rapido (bike, auto or cab)?
```
**Options**
```
Never
1–3 times
About once a week
Several times a week
```

> **Why this is here:** Ownly's growth thesis is converting people who already ride with Rapido. This one tap lets
> the dashboard compare Ownly awareness and trial for Rapido users vs non-users (Page 7). Keep it **above** the
> "ordered online recently" question, which must stay last because it branches.

#### S3-Q4 · Ordered online recently (keep it last)
- **Type:** Multiple choice · **Required:** ON · **Branching:** ON

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

### SECTION 4 · Hyderabad · Your orders

**Section title**
```
Hyderabad · Your orders
```
**Section description**
```
Count orders, not items. Open each app → Orders to check. Type 0 if you didn't use that app.
```

All four questions use the same settings:
- **Type:** Short answer · **Required:** ON
- **⋮ → Response validation:** `Number` → `Between` → `0` and `60`

**Error text** (same for all four)
```
Please type a number, e.g. 3
```

> Shortcut: build S4-Q1 completely, click **Duplicate** (⧉) three times, then paste the new titles. The validation copies too.

#### S4-Q1 · Swiggy orders
**Question**
```
Swiggy: how many orders in the last 4 weeks?
```

#### S4-Q2 · Zomato orders
**Question**
```
Zomato: how many orders in the last 4 weeks?
```

#### S4-Q3 · Ownly orders
**Question**
```
Ownly (Rapido's food app, or food inside the Rapido app): how many orders in the last 4 weeks?
```

#### S4-Q4 · Other orders
**Question**
```
Any other way (Toing, Magicpin, EatSure, or directly from a restaurant): how many orders in the last 4 weeks?
```

---

### SECTION 5 · Hyderabad · Your last order

**Section title**
```
Hyderabad · Your last order
```
**Section description**
```
Now just your most recent order.
```

#### S5-Q1 · Last order app
- **Type:** Multiple choice · **Required:** ON
- Add "Other" as a **normal option** by pasting it. Don't click "add 'Other'", which adds a text box.

**Question**
```
Which app did you use for your most recent food delivery order?
```
**Options**
```
Swiggy
Zomato
Ownly (or food inside the Rapido app)
Toing
Magicpin
EatSure
Directly from the restaurant
Other
```

#### S5-Q2 · Amount paid
- **Type:** Short answer · **Required:** ON
- **⋮ → Response validation:** `Number` → `Between` → `0` and `10000`

**Question**
```
What was the total amount you paid for it?
```
**Question description**
```
₹, final amount after discounts, including all fees.
```
**Error text**
```
Please type the amount as a number, e.g. 280
```

#### S5-Q3 · People on the order
- **Type:** Multiple choice · **Required:** ON

**Question**
```
How many people was that order for?
```
**Options**
```
Just me
2 people
3–4 people
5 or more people
```

#### 🆕 S5-Q4 · Did the bill feel fair
- **Type:** Multiple choice · **Required:** ON · Shuffle **OFF**

**Question**
```
Thinking about that amount: did it feel fair for what you got?
```
**Options**
```
Yes, it felt fair
No, the extra charges on top were too much
No, the food itself was overpriced
I didn't really look at the breakdown
```

> **Why this is here and not in a WhatsApp poll:** it separates *fee* pain from *price* pain, which is
> exactly the difference between Service P's first bullet and its second. It sits immediately after the
> amount question because the respondent has just recalled the number, so the answer is anchored to a real
> bill rather than a general mood. Asking it here also lets us cut it by segment and cross it against the
> Section 6 trade-offs — a poll would only give a prevalence number with nothing to join it to.

---

### 🆕 SECTION 6 · Hyderabad · Quick choices

> **Why this section exists:** every trade-off below holds the saving at **₹30** and changes only what the
> ₹30 costs you — speed, reliability, or restaurant choice. That is how we find out whether price is really
> the lever, or whether people only say it is. Do not reword the amounts.

**Section title**
```
Hyderabad · Quick choices
```
**Section description**
```
Four quick either-or questions. These are made-up examples, not real offers from any app. Assume everything else about the two apps is the same.
```

#### S6-Q1 · Price vs speed
- **Type:** Multiple choice · **Required:** ON · **⋮ → Shuffle option order:** ON

**Question**
```
Same restaurant, same food. Which would you choose?
```
**Options**
```
₹260 total, arrives in 30 minutes
₹230 total, arrives in 45 minutes
```

#### S6-Q2 · Price vs reliability
- **Type:** Multiple choice · **Required:** ON · **⋮ → Shuffle option order:** ON

**Question**
```
Same restaurant, same food, same delivery time. Which would you choose?
```
**Options**
```
₹260 total, late by 15+ minutes in about 1 of every 10 orders
₹230 total, late by 15+ minutes in about 3 of every 10 orders
```

#### S6-Q3 · Price vs restaurant choice
- **Type:** Multiple choice · **Required:** ON · **⋮ → Shuffle option order:** ON

**Question**
```
Same food price level and delivery time. Which would you choose?
```
**Options**
```
₹260 total, has most of your usual restaurants
₹230 total, has only a few of your usual restaurants
```

#### S6-Q4 · Switching threshold
- **Type:** Multiple choice · **Required:** ON · Shuffle **OFF**

**Question**
```
Think of a typical order of yours. How much lower would the final amount need to be, every time, for you to make a different app your main one?
```
**Options**
```
₹10
₹20
₹30
₹50
₹75
₹100 or more
No amount, price alone wouldn't make me switch
Don't know
```

---

### 🆕 SECTION 7 · Hyderabad · Two services

> **This is the section the whole project turns on.** It is the primary test of H₀ whenever the landing-page
> experiment draws fewer than 80 visitors (`_ops/decisions.md` D3). Two rules when you build it:
> **1.** Service P and Service Q must *look* identical — same block type, same font size, same bullet style.
> Any visual difference becomes a confound. **2.** It must come **before** the Ownly reveal in section 8, so
> nobody is answering about a brand.

**Section title**
```
Hyderabad · Two services
```
**Section description**
```
Two different food delivery services are being considered for Hyderabad. Neither exists exactly as described. Please read both before answering.

SERVICE P — "Same food. Smaller final bill."
• Menu prices are the restaurant's own prices, not marked up for the app
• One flat delivery fee: no platform fee, no packaging fee, no surge charge
• The total you see is the total you pay

SERVICE Q — "Your Hyderabad regulars, and dinner that actually turns up."
• The local biryani, tiffin and meals places you already order from, not only the big chains
• The delivery time shown is the time it actually takes
• If an order goes wrong, a clear answer and your money back fast
• Fair prices with every charge visible before you pay
```

#### S7-Q1 · Try P?
- **Type:** Multiple choice · **Required:** ON · Shuffle **OFF** (never shuffle a scale)

**Question**
```
If SERVICE P were available where you are, how likely are you to try it for one of your next few orders?
```
**Options**
```
Definitely not
Probably not
Not sure
Probably
Definitely
```

#### S7-Q2 · Try Q?
- **Type:** Multiple choice · **Required:** ON · Shuffle **OFF**

**Question**
```
And if SERVICE Q were available, how likely are you to try it for one of your next few orders?
```
**Options**
```
Definitely not
Probably not
Not sure
Probably
Definitely
```

#### S7-Q3 · Forced choice ⭐ THE H₀ QUESTION
- **Type:** Multiple choice · **Required:** ON · **⋮ → Shuffle option order:** ON

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

#### S7-Q4 · Why (the only optional question in this section)
- **Type:** Short answer · **Required:** **OFF**

**Question**
```
In one line, what made you pick that one?
```

#### S7-Q5 · Repeat without the offer
- **Type:** Multiple choice · **Required:** ON · Shuffle **OFF**

**Question**
```
Imagine you tried the one you picked because of a ₹100 off first-order offer. Once that offer ended, would you keep using it?
```
**Options**
```
Definitely not
Probably not
Not sure
Probably
Definitely
```

#### S7-Q6 · Price durability
- **Type:** Multiple choice · **Required:** ON · Shuffle **OFF**

**Question**
```
How much do you agree: "A new app's low prices usually go up once it becomes popular."
```
**Options**
```
Strongly disagree
Disagree
Neither
Agree
Strongly agree
```

---

### SECTION 8 · Hyderabad · Ownly

**Section title**
```
Hyderabad · Ownly
```
**Section description:** leave empty

#### 🆕 S8-Q1 · Food inside the Rapido app
- **Type:** Multiple choice · **Required:** ON · Shuffle **OFF**
- It sits here, after the two brand-blind sections, so it can't influence the Service P / Q answers.

**Question**
```
Have you seen an option to order food inside the Rapido app?
```
**Options**
```
Yes
No
Not sure
I don't use the Rapido app
```

#### S8-Q2 · Ownly status (keep it last: it branches)
- **Type:** Multiple choice · **Required:** ON · **Branching:** ON

**Question**
```
Ownly is a food delivery app by Rapido (the bike-taxi and auto app). Before today, which of these is true for you?
```
**Options**
```
I hadn't heard of Ownly
I'd heard of it, but never opened it
I opened or browsed it, but didn't order
I've ordered on Ownly
```

---

### SECTION 9 · Hyderabad · About Ownly

**Section title**
```
Hyderabad · About Ownly
```
**Section description**
```
About Ownly: a food delivery app from Rapido. Restaurants pay Ownly no commission, so menu prices are meant to match the restaurant's own prices. There's no platform, packaging or surge fee; you pay for the food plus delivery. It started in Hyderabad in September 2026.
```

#### S9-Q1 · What would make you try it
- **Type:** Multiple choice · **Required:** ON · **⋮ → Shuffle option order:** ON

**Question**
```
Which ONE thing would most make you try Ownly for an order?
```
**Options**
```
A discount on my first order
My usual restaurants being on it
Seeing it's cheaper than Swiggy/Zomato for the same order
A promise of a quick refund if an order goes wrong
A friend telling me it works well
Paying by cash on delivery or meal card (Pluxee / Zeta)
Nothing, I'm happy with how I order now
```

---

### SECTION 10 · Hyderabad · A bit more about Ownly

**Section title**
```
Hyderabad · A bit more about Ownly
```
**Section description:** leave empty

#### S10-Q1 · Where first heard
- **Type:** Multiple choice · **Required:** ON

**Question**
```
Where did you first hear about Ownly?
```
**Options**
```
Inside the Rapido app
Instagram / YouTube
Friends, classmates or colleagues
Hoardings, posters or street campaigns
News, LinkedIn or Reddit
Don't remember
```

#### S10-Q2 · Why not opened
- **Type:** Multiple choice · **Required:** ON · **⋮ → Shuffle option order:** ON

**Question**
```
What's the MAIN reason you haven't opened it?
```
**Options**
```
I'm happy with my current app or membership
I don't trust a new app yet
I heard bad things about its delivery or support
I don't think it's really cheaper
Not sure it delivers to my area
I don't want another app on my phone
Just haven't got around to it
```

---

### SECTION 11 · Hyderabad · A bit more about Ownly (2)

**Section title**
```
Hyderabad · A bit more about Ownly (2)
```
**Section description:** leave empty

#### S11-Q1 · Where first heard
- **Type:** Multiple choice · **Required:** ON
- Same question and options as **S10-Q1**:

**Question**
```
Where did you first hear about Ownly?
```
**Options**
```
Inside the Rapido app
Instagram / YouTube
Friends, classmates or colleagues
Hoardings, posters or street campaigns
News, LinkedIn or Reddit
Don't remember
```

#### S11-Q2 · What stopped ordering
- **Type:** Multiple choice · **Required:** ON · **⋮ → Shuffle option order:** ON

**Question**
```
When you looked, what MAINLY stopped you from ordering?
```
**Options**
```
My restaurants weren't there
Prices weren't lower than my usual app
A coupon on my usual app made that cheaper
It didn't deliver to my address
The delivery time looked too long
I couldn't pay the way I wanted
I was just looking around
```

---

### SECTION 12 · Hyderabad · Ownly users

**Section title**
```
Hyderabad · Ownly users
```
**Section description**
```
A few questions about Ownly. Your answers are the most valuable part of this survey 🙏
```

#### S12-Q1 · Where first heard
- **Type:** Multiple choice · **Required:** ON

**Question**
```
Where did you first hear about Ownly?
```
**Options**
```
Inside the Rapido app
Instagram / YouTube
Friends, classmates or colleagues
Hoardings, posters or street campaigns
News, LinkedIn or Reddit
Don't remember
```

#### S12-Q2 · Where ordered
- **Type:** Multiple choice · **Required:** ON

**Question**
```
Where have you ordered on Ownly?
```
**Options**
```
Hyderabad only
Bengaluru only
Both
```

#### S12-Q3 · First order
- **Type:** Multiple choice · **Required:** ON

**Question**
```
When did you place your FIRST Ownly order?
```
**Options**
```
In the last 4 weeks
More than 4 weeks ago
```

#### S12-Q4 · Orders 5–8 weeks ago
- **Type:** Short answer · **Required:** ON
- **⋮ → Response validation:** `Number` → `Between` → `0` and `60`

**Question**
```
How many Ownly orders did you place in the 4 weeks BEFORE the last 4 weeks (roughly 5–8 weeks ago)?
```
**Question description**
```
Type 0 if none, or if your first Ownly order was in the last 4 weeks.
```
**Error text**
```
Please type a number, e.g. 2
```

#### S12-Q5 · If Ownly didn't exist
- **Type:** Multiple choice · **Required:** ON · **⋮ → Shuffle option order:** ON

**Question**
```
Think of your most recent Ownly order. If Ownly didn't exist, what would you most likely have done instead?
```
**Options**
```
Ordered the same on Swiggy or Zomato
Ordered on another app (Toing, Magicpin, etc.)
Ordered directly from the restaurant
Cooked, or eaten at home / mess / hostel
Gone out to eat
Skipped it or had a snack
```

#### S12-Q6 · Disappointment (Sean Ellis)
- **Type:** Multiple choice · **Required:** ON · Shuffle **OFF**

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

#### S12-Q7 · One change
- **Type:** Multiple choice · **Required:** ON · **⋮ → Shuffle option order:** ON

**Question**
```
What ONE change would make you order more on Ownly?
```
**Options**
```
More restaurants
Faster delivery
More reliable, on-time delivery
Quicker refunds and support
A bigger price gap vs other apps
More offers and coupons
Cash on delivery or meal-card payment
```

✅ **Checkpoint:** the last section header reads **"Section 12 of 12"**.

---
## Part 4 · Bengaluru path (sections 13–23)

### 4a. Duplicate sections 2–12

Do these 4 steps for **Hyderabad sections 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12**, in that order:
1. On the Hyderabad section header: **⋮ → Duplicate section** (the copy appears right below).
2. On the copy: **⋮ → Move section** → click **⌄** until the copy is **last** → **Save**.
3. Select the copy's section title and paste the Bengaluru title from the table below.
4. Move on to the next Hyderabad section.

Paste these titles onto the copies:

| Copy of section | New section title (copy) |
|---|---|
| 2 | `Bengaluru · Your area` |
| 3 | `Bengaluru · About you` |
| 4 | `Bengaluru · Your orders` |
| 5 | `Bengaluru · Your last order` |
| 6 | `Bengaluru · Quick choices` |
| 7 | `Bengaluru · Two services` |
| 8 | `Bengaluru · Ownly` |
| 9 | `Bengaluru · About Ownly` |
| 10 | `Bengaluru · A bit more about Ownly` |
| 11 | `Bengaluru · A bit more about Ownly (2)` |
| 12 | `Bengaluru · Ownly users` |

✅ **Checkpoint:** sections 13–23 are the Bengaluru pages, in the order above.

### 4b. Paste the Bengaluru changes

Only **four** sections change. Everything else is correct as duplicated.

#### SECTION 13 · Bengaluru · Your area → replace the area options
Delete all 8 old options (✕ next to each). Then paste into the first option box:

**Options**
```
Koramangala / HSR Layout / BTM Layout
Indiranagar / Domlur / Old Airport Road
Whitefield / Marathahalli / Bellandur / Sarjapur Road
Electronic City / Bommanahalli
Jayanagar / JP Nagar / Banashankari
Hebbal / Yelahanka / North Bengaluru
Another part of Bengaluru
```

#### SECTION 18 · Bengaluru · Two services → replace the section description
Only the Service Q headline changes (Hyderabad → Bengaluru). Everything else stays identical, so the
two cities stay comparable.

**Section description**
```
Two different food delivery services are being considered for Bengaluru. Neither exists exactly as described. Please read both before answering.

SERVICE P — "Same food. Smaller final bill."
• Menu prices are the restaurant's own prices, not marked up for the app
• One flat delivery fee: no platform fee, no packaging fee, no surge charge
• The total you see is the total you pay

SERVICE Q — "Your local regulars, and dinner that actually turns up."
• The local places you already order from, not only the big chains
• The delivery time shown is the time it actually takes
• If an order goes wrong, a clear answer and your money back fast
• Fair prices with every charge visible before you pay
```

#### SECTION 20 · Bengaluru · About Ownly → replace the section description

**Section description**
```
About Ownly: a food delivery app from Rapido. Restaurants pay Ownly no commission, so menu prices are meant to match the restaurant's own prices. There's no platform, packaging or surge fee; you pay for the food plus delivery. It has been available across Bengaluru since March 2026.
```

#### SECTION 23 · Bengaluru · Ownly users → 3 changes

**Change 1:** delete the question "Where have you ordered on Ownly?" (🗑).

**Change 2:** on "When did you place your FIRST Ownly order?", delete both options and paste:

**Options**
```
In the last 4 weeks
1–3 months ago
3–6 months ago
More than 6 months ago
```

**Change 3:** add a new question **below** "How would you feel if you could no longer use Ownly?". Click that question, then ⊕.
- **Type:** Multiple choice · **Required:** ON · Shuffle **OFF**

**Question**
```
If you order on Ownly less than you used to, what's the MAIN reason?
```
**Options**
```
I don't order less than before
The restaurants I want aren't there
Late or failed deliveries
Refund or support problems
Prices are no longer clearly lower
Offers ended
Went back to my Swiggy One / Zomato Gold membership
```

✅ **Checkpoint:** section 23 now has 7 questions: where first heard · FIRST order (4 options) · orders 5–8 weeks ago · if Ownly didn't exist · how would you feel · order less reason · ONE change.

---

## Part 5 · Other-city path (sections 24–30)

### 5a. Duplicate 7 sections

Same 4 steps as Part 4a, but only for **Hyderabad sections 2, 3, 4, 5, 8, 9, 12**.
**Skip sections 6, 7, 10 and 11.** Paste these titles:

| Copy of section | New section title (copy) |
|---|---|
| 2 | `Other city · Your city` |
| 3 | `Other city · About you` |
| 4 | `Other city · Your orders` |
| 5 | `Other city · Your last order` |
| 8 | `Other city · Ownly` |
| 9 | `Other city · About Ownly` |
| 12 | `Other city · Ownly users` |

✅ **Checkpoint:** sections 24–30 are the Other-city pages, in the order above.

### 5b. Paste the Other-city changes

#### SECTION 24 · Other city · Your city
Replace the question "Which area?" with:

**Question**
```
Which city?
```
Delete all old options, then paste:

**Options**
```
Chennai
Pune
Mumbai
Delhi NCR
Kolkata
Another Indian city
Outside India
```

#### SECTION 28 · Other city · Ownly
Leave the Rapido food question as it is. On the **last** question (Ownly status), replace the question text with:

**Question**
```
Ownly is a food delivery app by Rapido (the bike-taxi and auto app), available in Bengaluru and Hyderabad. Before today, which of these is true for you?
```
Delete all 4 old options, then paste these **3**:

**Options**
```
I hadn't heard of Ownly
I'd heard of it
I've ordered on Ownly (e.g. while in Bengaluru or Hyderabad)
```

#### SECTION 29 · Other city · About Ownly
Replace the section description:

**Section description**
```
About Ownly: a food delivery app from Rapido. Restaurants pay Ownly no commission, so menu prices are meant to match the restaurant's own prices. There's no platform, packaging or surge fee; you pay for the food plus delivery. It isn't available in most other cities yet.
```
Replace the question text (options stay the same):

**Question**
```
If Ownly launched in your city, which ONE thing would most make you try it?
```

#### SECTION 30 · Other city · Ownly users
**Delete** these 5 questions (🗑):
- Where did you first hear about Ownly?
- When did you place your FIRST Ownly order?
- How many Ownly orders did you place in the 4 weeks BEFORE…
- Think of your most recent Ownly order. If Ownly didn't exist…
- What ONE change would make you order more on Ownly?

On the remaining "Where have you ordered on Ownly?", replace the question text:

**Question**
```
Where did you order on Ownly?
```
Delete its options, then paste:

**Options**
```
Bengaluru
Hyderabad
Both
```

Keep "How would you feel if you could no longer use Ownly?" unchanged.

Replace the section description:

**Section description**
```
Thanks for trying Ownly. Just two quick questions 🙏
```

✅ **Checkpoint:** section 30 has 2 questions.

---

## Part 6 · Last two pages (sections 31–32)

Click inside section 30, then **Add section**.

### SECTION 31 · Last question

**Section title**
```
Last question
```
**Section description**
```
That's it, thank you! 🙏
```

#### S31-Q1 · Interview volunteer
- **Type:** Short answer · **Required:** **OFF**

**Question**
```
Optional: Can we message you for a 10-minute chat about how you order food?
```
**Question description**
```
Leave your WhatsApp number if yes. It's only used for the chat and kept separately from your answers.
```

Click inside section 31, then **Add section** again.

### SECTION 32 · Not eligible

**Section title**
```
Thank you!
```
**Section description**
```
Thanks so much for your time! 🙏 This survey is for people aged 20–30. Please press Submit, and forward the link to friends in that age group.
```
No questions in this section.

✅ **Checkpoint:** "Section 32 of 32".

---

## Part 7 · Set every branch (12 min)

> Duplicated sections still point to the Hyderabad pages. **Set every row below**, even ones that look right.

### 7a. Answer-based branching
On each question below, each option now has a dropdown on its right. Pick the section:

| Section | Question | Option → Go to section |
|---|---|---|
| 1 | Which city do you live, study or work in on most days? | Hyderabad → **2** · Bengaluru → **13** · Another city → **24** |
| 2 | How old are you? | Under 20 → **32** · 20–22 → **3** · 23–25 → **3** · 26–28 → **3** · 29–30 → **3** · Over 30 → **32** |
| 3 | In the last 4 weeks, did you order food online… | Yes → **4** · No → **6** |
| 8 | Ownly is a food delivery app by Rapido… | I hadn't heard of Ownly → **9** · I'd heard of it, but never opened it → **10** · I opened or browsed it, but didn't order → **11** · I've ordered on Ownly → **12** |
| 13 | How old are you? | Under 20 → **32** · 20–22 → **14** · 23–25 → **14** · 26–28 → **14** · 29–30 → **14** · Over 30 → **32** |
| 14 | In the last 4 weeks, did you order food online… | Yes → **15** · No → **17** |
| 19 | Ownly is a food delivery app by Rapido… | I hadn't heard of Ownly → **20** · I'd heard of it, but never opened it → **21** · I opened or browsed it, but didn't order → **22** · I've ordered on Ownly → **23** |
| 24 | How old are you? | Under 20 → **32** · 20–22 → **25** · 23–25 → **25** · 26–28 → **25** · 29–30 → **25** · Over 30 → **32** |
| 25 | In the last 4 weeks, did you order food online… | Yes → **26** · No → **28** |
| 28 | Ownly is a food delivery app by Rapido, available in… | I hadn't heard of Ownly → **29** · I'd heard of it → **29** · I've ordered on Ownly (e.g. …) → **30** |

### 7b. Page-based branching
At the **bottom** of each section, set **After section X**:

| Section | After section → |
|---|---|
| 4 Hyderabad · Your orders | Go to section **5** |
| 5 Hyderabad · Your last order | Go to section **6** |
| 6 Hyderabad · Quick choices | Go to section **7** |
| 7 Hyderabad · Two services | Go to section **8** |
| 9 Hyderabad · About Ownly | Go to section **31** |
| 10 Hyderabad · A bit more about Ownly | Go to section **31** |
| 11 Hyderabad · A bit more about Ownly (2) | Go to section **31** |
| 12 Hyderabad · Ownly users | Go to section **31** |
| 15 Bengaluru · Your orders | Go to section **16** |
| 16 Bengaluru · Your last order | Go to section **17** |
| 17 Bengaluru · Quick choices | Go to section **18** |
| 18 Bengaluru · Two services | Go to section **19** |
| 20 Bengaluru · About Ownly | Go to section **31** |
| 21 Bengaluru · A bit more about Ownly | Go to section **31** |
| 22 Bengaluru · A bit more about Ownly (2) | Go to section **31** |
| 23 Bengaluru · Ownly users | Go to section **31** |
| 26 Other city · Your orders | Go to section **27** |
| 27 Other city · Your last order | Go to section **28** |
| 29 Other city · About Ownly | Go to section **31** |
| 30 Other city · Ownly users | Go to section **31** |
| 31 Last question | **Submit form** |
| 32 Thank you! | **— nothing to set —** see the note below |

**The last section has no "After section" dropdown, and that is correct.** Google Forms only shows the
dropdown when there is a section after the current one. Section 32 is the final section, so it submits
automatically. Don't go looking for a setting that isn't there.

Sections 1, 2, 3, 8, 13, 14, 19, 24, 25 and 28 contain an answer-based question, so their "After section" dropdown is ignored. That's normal.

---

## Part 8 · Connect Google Sheets (2 min)

1. **Responses** tab → **Link to Sheets** (green icon) → **Create a new spreadsheet**.
2. Paste the name:

**Spreadsheet name**
```
Ownly Survey v6 responses
```
3. Click **Create**. Don't edit this sheet by hand; copy data to another tab if you need to work on it.

---

## Part 9 · Test all 11 paths, then delete them (15 min)

> ### ⚠ Read this first: if **Submit is greyed out**, the form isn't live yet
>
> A disabled Submit button is **not** a branching or validation problem. It means the form is not
> currently accepting responses. Check these three, in order:
>
> | # | Check | Where |
> |---|---|---|
> | 1 | **Is the form published?** Newer Google Forms starts every form as an unpublished draft. An unpublished form previews fine but cannot be submitted. | **Publish** button, top right. Click it, then **Copy responder link** |
> | 2 | **Is "Accepting responses" on?** | **Responses** tab → the *Accepting responses* toggle must be ON |
> | 3 | **Are you on the responder link rather than the editor preview?** | Use the link from step 1, not `/edit` |
>
> Fix whichever applies, then reload the page. A required question you skipped looks different — Forms
> shows a red *"This is a required question"* and the Submit button stays **clickable**.

Click **👁 Preview** and submit each test.

**How to read the table:** the middle column is every answer you give, **in the order the form asks for
them**, each one labelled with the section it belongs to. The right column is the pages you should land on,
in order. If your pages don't match, the branch is wrong — see the diagnostic under the table.

| # | Answer these, in this order | Pages you should see, in order | What to check |
|---|---|---|---|
| 1 | S1 city **Hyderabad** · S2 age **Under 20** | *Thank you!* | Submit works, nothing else shown |
| 2 | S1 **Hyderabad** · S2 age **23–25** · S3 occupation **Student**, memberships **None**, ordered recently **No** | Quick choices → Two services → Ownly → About Ownly *(Hyderabad description)* → Last question | **No Orders page, no Last-order page, no bill-fairness question** — but the two new sections still appear |
| 3 | S1 **Hyderabad** · S2 **23–25** · S3 occupation **Student**, memberships **Swiggy One**, ordered recently **Yes** · S4 counts **3 / 1 / 0 / 0** · S5 app **Swiggy**, amount **250**, people **Just me**, bill felt **fair** · S8 Ownly status **"I'd heard of it, but never opened it"** | Orders → Last order → Quick choices → Two services → Ownly → A bit more about Ownly → Last question | Typing `abc` in a count shows the error · memberships lets you tick more than one · **you reach the Orders page** |
| 4 | Same as 3, but S8 Ownly status **"I opened or browsed it, but didn't order"** | … → A bit more about Ownly **(2)** → Last question | You get the *"what stopped you ordering"* page, not the *"why haven't you opened it"* one |
| 5 | Same as 3, but S4 Ownly count **2** and S8 status **"I've ordered on Ownly"** | … → Ownly users → Last question | 7 questions, including *"Where have you ordered on Ownly?"* |
| 6 | Any path — stop on the **Two services** page and just look | — | P and Q are the same size and style · the forced-choice options swap order when you reload · nothing is cut off on a phone |
| 7 | S1 city **Bengaluru** · S2 age **26–28** · ordered recently **Yes** · S8 status **"I hadn't heard of Ownly"** | Bengaluru pages throughout → Two services saying **"Your local regulars"** → About Ownly saying **"since March 2026"** → Last question | Bengaluru area list, not Hyderabad's |
| 8 | Bengaluru · ordered recently **Yes** · Ownly count **4** · status **"I've ordered on Ownly"** | Bengaluru Ownly users → Last question | 4 first-order options · the *"order less"* question is there · **no** *"Where have you ordered"* |
| 9 | S1 city **Another city** · city **Pune** · age **20–22** · ordered recently **Yes** · status **"I hadn't heard of Ownly"** | City → Orders → Last order → Ownly *(3 options)* → *"If Ownly launched in your city…"* → Last question | **No Quick choices and no Two services** — that's deliberate |
| 10 | Another city · ordered recently **No** · status **"I've ordered on Ownly…"** | Ownly *(3 options)* → Ownly users *(2 questions)* → Last question | Only 2 questions on the last page |
| 11 | S1 **Bengaluru** · S2 age **Over 30** | *Thank you!* | |

### If a page you expected didn't appear

The commonest one: **you answered "Yes" to "did you order food online in the last 4 weeks" but never saw
the Orders page.** That means the branch on that question is pointing at the wrong section.

1. Open the section **Hyderabad · About you**.
2. Find *"In the last 4 weeks, did you order food online for delivery at least once…"*.
3. Check it is the **last question on that page**. If Memberships or Rapido usage sits below it, drag them above it.
   A branching question has to be last, or the page's own "After section" setting can override it.
4. **⋮ → Go to section based on answer**, and set — **by section name, never by number**:
   - `Yes` → **Hyderabad · Your orders**
   - `No` → **Hyderabad · Quick choices**
5. Repeat for **Bengaluru · About you** (`Yes` → *Bengaluru · Your orders*, `No` → *Bengaluru · Quick choices*)
   and **Other city · About you** (`Yes` → *Other city · Your orders*, `No` → *Other city · Ownly*).

> **Always pick branch targets by name.** If your form has even one more section than this guide, every
> number in Part 7 is off, but the names are still right.

Also:
- **Search for leftovers** with Ctrl/Cmd + F in the editor: `Copy of`, `Option 1`, `[`. None should appear.
- **Check on a phone.** The Two services description is the longest text in the form — make sure both
  services are readable without pinch-zooming, and that neither one is cut off.
- **Time yourself** on path 3 (the longest). If it runs over 8 minutes, delete S6-Q4 (switching threshold)
  and S7-Q6 (price durability), in that order, and log the cut in `_ops/decisions.md`.

**Delete all test responses:**
1. **Responses** tab → **⋮** → **Delete all responses** → OK.
2. In the linked sheet, select row 2 down to the last test row → right-click → **Delete rows**.

---

## Part 10 · Share (5 min)

1. Click **Send** → the **🔗** tab → tick **Shorten URL** → **Copy**. In newer Google Forms the button is **Publish**: click **Publish**, then **Copy responder link**.
2. Optional: make one short link per channel at bit.ly, so you can see clicks per channel.
3. Paste one of the messages below and replace `[FORM LINK]` and `[DAY, DATE, TIME]`.

**Don't** mention Ownly, Rapido or "hidden fees" in messages, and don't add people as collaborators (they could edit the form).

**WhatsApp group message**
```
Hi everyone! 👋 Sorry for the group message, and thank you for reading.

I'm a Product Management student, and for our Market Research project we're studying how people aged 20–30 order food online: which apps they use, how often, what they pay, and what makes them try a new app.

👉 [FORM LINK]

⏱ About 6 minutes, mostly taps and a few numbers
🔒 Anonymous: no name, no email
🎓 Independent student research, not linked to any food app or restaurant

Who can fill it: anyone aged 20–30, in Bengaluru, Hyderabad or any other city, whether you order food online often, rarely or never.

Two small requests:
1️⃣ Answer based on what you actually do. There are no right or wrong answers.
2️⃣ If you order food online, keep your app's order history open. A couple of questions ask how many orders you placed.

Please forward it to friends and colleagues aged 20–30 🙏 We're collecting answers until [DAY, DATE, TIME]. Thank you!
```

**Personal WhatsApp message**
```
Hey! Hope you're doing well 🙂 Small favour: I'm doing a market research project for my PDM course on how people our age order food online. Could you fill in a quick survey? About 6 minutes, anonymous.

👉 [FORM LINK]

If you order food online, keep your order history handy (it asks how many orders you placed). And if you can, forward it to 2–3 friends aged 20–30, in any city. Thanks a ton! 🙏
```

**LinkedIn post**
```
Aged 20–30 and living in Bengaluru, Hyderabad or anywhere in India? I'd value 6 minutes of your time.

For my Product Management programme, our team is researching how young professionals and students choose food delivery apps: how often they order, what they pay, and what makes them try something new.

🕒 About 6 minutes · 🔒 Anonymous · 📱 Built for your phone
👉 [FORM LINK]

Everyone counts, including people who rarely order online. I'll share a summary of what we learn. Reposts are hugely appreciated 🙌

#ProductManagement #MarketResearch #Bengaluru #Hyderabad
```

**Reminder message**
```
Thank you to everyone who filled in the food delivery survey! 🙏 We still need more answers from [Hyderabad / Bengaluru / working professionals / people who rarely order online]. If you're 20–30 and haven't filled it yet: 👉 [FORM LINK] (about 6 min). Already did it? Forwarding it is the best help!
```

---

## Part 11 · Close the survey and analyse (5 min)

**While collecting:** Responses tab → **Summary** → check the count per city. Targets: **≥ 80 Hyderabad**, **≥ 80 Bengaluru** (with ≥ 30 Ownly users), **≥ 40 other cities**.

**Watch two things daily:**
- The **student vs working-professional split** in section 3. Students over-fill on their own; professionals don't.
- The **"I genuinely can't choose"** share on S7-Q3. If it goes above ~35%, the two services aren't reading
  as different enough, and that itself is a finding worth reporting.

**To close:** Responses tab → switch **Accepting responses** OFF → paste:

**Closed message**
```
This survey is now closed. Thank you for your help!
```

**To export:**
1. Responses tab → **⋮** → **Download responses (.csv)**. It downloads a **.zip**.
2. Unzip it and save the `.csv` as `08_clean_data/raw/survey_v6_raw.csv`. **Never edit that file.**
3. Send Claude the counts per city and the S7-Q3 split. The H₀ test, the trade-off shares with confidence
   intervals, and the segment cuts are run from there.

**The H₀ test that comes out of section 7** (pre-registered in `_ops/decisions.md` D3, fixed before any data):
- Primary outcome: **S7-Q3 forced choice**, "can't choose" excluded, exact binomial vs 50% with a Wilson CI.
- Secondary: **S7-Q1 vs S7-Q2** dichotomised at *Probably / Definitely*, **McNemar** on the discordant pairs.
- Known limit, stated on the slide rather than buried: Google Forms cannot randomise section order, so every
  respondent sees P before Q. That is exactly why the forced choice, with its options shuffled, is the
  primary outcome, and why the landing-page experiment runs the properly randomised version of the same test.

---

## Part 12 · Upgrading an existing v5 form to v6 (25 min)

If you already built the 28-section v5 form, **do not rebuild it.** Do this instead.

1. **Add the two new Hyderabad sections in the right place.** Click inside v5's section 5
   (*Hyderabad · Your last order*), then **Add section** twice. Two empty sections appear as the new
   sections 6 and 7, and everything after them renumbers automatically (old 6 → 8, old 7 → 9 … old 28 → 30).
2. **Build them** from **SECTION 6** and **SECTION 7** in Part 3 above — titles, descriptions and all
   10 questions.
2b. **Add the two single questions that live inside existing sections:** 🆕 **S3-Q2 Memberships**
   (insert above "Ordered online recently", which must stay last in section 3) and 🆕 **S5-Q4 Did the bill
   feel fair** (add at the end of *Your last order*). Copy both from Part 3 above.
3. **Duplicate both into the Bengaluru path.** For each of the two new sections: **⋮ → Duplicate section**,
   then **⋮ → Move section** until it sits directly after *Bengaluru · Your last order*. Rename them
   `Bengaluru · Quick choices` and `Bengaluru · Two services`, and paste section 18's replacement
   description from Part 4b.
4. **Do not add them to the Other-city path.**
5. **Redo Part 7 completely.** Every branch number has shifted by 2 (Hyderabad), 4 (Bengaluru) or 4
   (Other city / closing). Work through both tables row by row — this is the step where upgrades break.
6. **Re-run all 11 test paths** in Part 9, paying attention to tests 2, 6 and 9.
7. **Delete the test responses** from both the form and the sheet.

> If responses have already come in on v5, **stop.** Adding questions mid-collection creates two
> incompatible waves. Either close v5 and treat what you have as wave 1, or keep v5 running unchanged and
> run the proposition test on the landing page only. Whichever you pick, log it in `_ops/decisions.md`
> with the timestamp of the break.

---

## Appendix A · Final checklist

### A1. Phrases the analysis looks for in question titles
Don't change these phrases:

| Question | Title must contain |
|---|---|
| City | `Which city do you live` |
| Area / city | whole title exactly `Which area?` or `Which city?` |
| Age | `How old are you` |
| Occupation | `best describes you` |
| 🆕 Memberships | `memberships do you have right now` |
| 🆕 Rapido usage | `how often did you use Rapido` |
| 🆕 Food inside Rapido app | `option to order food inside the Rapido app` |
| Ordered recently | `order food online for delivery at least once` |
| Counts | starts with `Swiggy: how many` · `Zomato: how many` · `Ownly (Rapido` · `Any other way` |
| Last order | `Which app did you use for your most recent` · `total amount you paid` · `How many people was that order for` |
| 🆕 Bill fairness | `did it feel fair for what you got` |
| 🆕 Trade-off: speed | `arrives in 30 minutes` (in the options) |
| 🆕 Trade-off: reliability | `1 of every 10 orders` (in the options) |
| 🆕 Trade-off: restaurants | `most of your usual restaurants` (in the options) |
| 🆕 Switching threshold | `make a different app your main one` |
| 🆕 Try P | `If SERVICE P were available` |
| 🆕 Try Q | `And if SERVICE Q were available` |
| 🆕 **Forced choice (H₀)** | `If only one of them existed` |
| 🆕 Why | `what made you pick that one` |
| 🆕 Repeat without offer | `Once that offer ended` |
| 🆕 Price durability | `low prices usually go up` |
| Ownly status | `Before today, which of these is true` |
| Trigger | `would most make you try` |
| Where first heard | `first hear about Ownly` |
| Why not opened | `reason you haven't opened` |
| What stopped | `stopped you from ordering` |
| Where ordered | `Where have you ordered on Ownly` / `Where did you order on Ownly` |
| First order | `FIRST Ownly order` |
| Previous period | `4 weeks BEFORE the last 4 weeks` |
| Counterfactual | `If Ownly didn't exist` |
| Disappointment | `no longer use Ownly` |
| Order less | `less than you used to` |
| One change | `ONE change would make you order more` |

### A2. Answer options the KPIs count
Must be pasted exactly:
- `Yes`
- `Just me`
- `Very disappointed`
- `Ordered the same on Swiggy or Zomato`
- `In the last 4 weeks`
- `More than 4 weeks ago`
- `Hyderabad only`
- `Bengaluru only`
- `Koramangala / HSR Layout / BTM Layout`
- `Another part of Hyderabad`
- `Ownly (or food inside the Rapido app)`
- 🆕 `Service P` · `Service Q` · `I genuinely can't choose between them`
- 🆕 `Swiggy One (any plan)` · `Zomato Gold` · `None`
- 🆕 `Yes, it felt fair` · `No, the extra charges on top were too much` · `No, the food itself was overpriced`
- 🆕 `Definitely` · `Probably` (the two that count as positive intent)
- 🆕 `No amount, price alone wouldn't make me switch`
- age bands `20–22` `23–25` `26–28` `29–30`
- status options starting `I hadn't heard` / `I'd heard` / `I opened` / `I've ordered`

### A3. Before you share
- [ ] 32 sections, in the order in Part 0A
- [ ] Only two questions are optional: the WhatsApp number (S31-Q1) and "what made you pick that one" (S7-Q4)
- [ ] 🆕 Memberships (S3-Q2) is a **Checkboxes** question, not multiple choice — it's the only one in the form
- [ ] 🆕 "Ordered online recently" is still the **last** question in section 3, after memberships and Rapido usage
- [ ] 🆕 "Before today, which of these is true" is still the **last** question in the Ownly section, after the Rapido food question
- [ ] All 5 number questions per city (4 counts + amount) and the 5–8-weeks question have number validation
- [ ] **Shuffle option order is ON for S6-Q1, S6-Q2, S6-Q3 and S7-Q3** — and **OFF** for every 5-point scale
- [ ] **Service P and Service Q are formatted identically** — same block, same size, same bullets
- [ ] **Sections 6 and 7 come BEFORE section 8**, so the proposition test is brand-blind
- [ ] Other city has no Quick choices and no Two services
- [ ] Every branch in Part 7a and 7b is set; Ownly pages go to 31; sections 31 and 32 go to Submit
- [ ] Settings: no emails · limit-1 OFF · progress bar ON · question shuffle OFF · confirmation message set
- [ ] No `Copy of`, `Option 1` or `[` anywhere
- [ ] **Form is Published and "Accepting responses" is ON** — test by submitting once from the responder link
- [ ] Section count matches Part 0A exactly; if it doesn't, Part 7's numbers are wrong
- [ ] Linked to a Google Sheet
- [ ] All 11 test paths passed, plus one check on a phone, plus one timing run
- [ ] Test responses deleted from the form **and** the sheet

### A4. Common mistakes

| What you see | Cause | Fix |
|---|---|---|
| **Submit is greyed out on the last page** | The form is an unpublished draft, or "Accepting responses" is off. Not a branching problem | Click **Publish** (top right), then check **Responses → Accepting responses** is ON |
| **The last section has no "After section" dropdown** | Correct behaviour — there is no section after it | Nothing to fix. The final section submits automatically |
| **Your form has more sections than this guide** | An extra section was added, so every branch target after it is off by one | Recount against Part 0A, then redo **both** tables in Part 7 using section *names*, not numbers |
| Bengaluru people land on Hyderabad pages | Duplicated branches still point to Hyderabad | Redo Part 7 for sections 13–30 |
| After an Ownly page, people see the next city's pages | "After section" left as "Continue to next section" | Set sections 9–12, 20–23, 29–30 to go to 31 |
| **People see Ownly named before the Two services page** | Sections 6 and 7 built after section 8 | Move them: ⋮ → Move section, until they sit between Your last order and Ownly |
| **Everyone picks Service Q** | Q has four bullets to P's three, so it looks like more | Expected and acceptable — but report the bullet-count asymmetry as a limitation |
| **"Can't choose" is over 35%** | The two services read as the same thing | Don't change the form mid-collection. Report it: it means framing isn't the lever |
| Under-20s can finish the survey | Age branches not set | Sections 2 / 13 / 24: Under 20 and Over 30 → 32 |
| People hit a Google sign-in | "Limit to 1 response" is ON | Settings → Responses → OFF |
| Pasted options became one long option | Paste didn't split into lines | Delete it and paste one line per option |
| "Other" shows a text box | Used "add 'Other'" | Delete it and paste `Other` as a normal option |
| Survey takes over 8 minutes | Two new sections added length | Cut S6-Q4, then S7-Q6. Log the cut and the timestamp |

### A5. What v6 deliberately does NOT ask

| Dropped | Why |
|---|---|
| WhatsApp Poll 1 ("which would make you switch?") | Redundant: S9-Q1 already asks the same ranking with 7 options, on a screened sample |
| WhatsApp Poll 3 ("did the bill feel fair?") | Promoted into the survey as S5-Q4, where it can be cut by segment |
| Food-only subtotal of the last order | The Gachibowli price audit measures fee share with observed data, which beats a recalled estimate |
| "Next 10 orders" allocation | The four order-count questions in section 4 give revealed share of requirements, which is better than a stated one |
| Separate ₹100-reward trial question for non-triers | Folded into S7-Q5, which asks everyone once instead of duplicating across three branches |
| Full choice experiment, fee staircase, brand-arm randomisation | Need n ≥ 125 and days of fielding (decision of 2026-09-14, unchanged) |
