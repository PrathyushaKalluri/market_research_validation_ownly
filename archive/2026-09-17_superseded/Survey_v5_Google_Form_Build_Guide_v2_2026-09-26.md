# Build Guide: Survey v5 in Google Forms (copy-paste edition)

**What you're building:** one Google Form with three city paths (Hyderabad, Bengaluru, Other city), 28 sections in total.
**Time:** about 75–90 minutes to build, plus 15 minutes to test.
**You need:** a Google account, a laptop, and this file open next to Google Forms.

---

## How to use this guide

Every piece of text you need is in a **grey box**. Hover over a box and click the copy icon (or select it and press Ctrl/Cmd + C), then paste into Google Forms.

| Grey box labelled | Paste it into |
|---|---|
| **Form title** / **Form description** | The top card of the form |
| **Section title** / **Section description** | The header of a section (the bar that says "Section 3 of 28") |
| **Question** | The question text box ("Untitled Question") |
| **Question description** | ⋮ (three dots, bottom right of the question) → **Description** → the small box under the title |
| **Options** | Click the **first option box** ("Option 1") and paste **all lines at once**. Google Forms turns each line into its own option. If they land as one option, paste line by line. |
| **Error text** | ⋮ → **Response validation** → the "Custom error text" box |

> **Golden rule:** paste text **exactly**. The dashboard (`10_dashboard/ownly_transfer_scorecard.html`) finds questions and answers by their wording. If you reword them, those KPIs show "Not in this form".

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
| 3 | Hyderabad path (sections 1–10), full copy-paste text | 30 min |
| 4 | Bengaluru path (sections 11–19): duplicate, then paste the changes | 15 min |
| 5 | Other-city path (sections 20–26): duplicate, then paste the changes | 10 min |
| 6 | Last two pages (sections 27–28) | 3 min |
| 7 | Set every branch | 10 min |
| 8 | Connect Google Sheets | 2 min |
| 9 | Test all 10 paths, then delete test responses | 15 min |
| 10 | Share: link and copy-paste messages | 5 min |
| 11 | Close the survey and load the dashboard | 5 min |
| A | Final checklist and exact wording the dashboard needs | — |

---

## Part 0 · The form at a glance
    
### 0A. All sections and questions

| # | Section title | Questions (short) |
|---|---|---|
| 1 | *(form title card)* | Which city do you live, study or work in on most days? |
| **Hyderabad** | | |
| 2 | Hyderabad · Your area | Which area? · How old are you? |
| 3 | Hyderabad · About you | Which best describes you right now? · Ordered food online in the last 4 weeks? |
| 4 | Hyderabad · Your orders | Swiggy / Zomato / Ownly / Any other way: how many orders in the last 4 weeks? (4 numbers) |
| 5 | Hyderabad · Your last order | Which app? · Total amount paid? · How many people? |
| 6 | Hyderabad · Ownly | Before today, which of these is true for you? (4 options) |
| 7 | Hyderabad · About Ownly | Which ONE thing would most make you try Ownly? |
| 8 | Hyderabad · A bit more about Ownly | Where did you first hear about Ownly? · MAIN reason you haven't opened it? |
| 9 | Hyderabad · A bit more about Ownly (2) | Where did you first hear about Ownly? · What MAINLY stopped you from ordering? |
| 10 | Hyderabad · Ownly users | Where first heard · Where have you ordered · FIRST order (2 options) · Orders 5–8 weeks ago · If Ownly didn't exist · How would you feel without Ownly · ONE change |
| **Bengaluru** | | |
| 11 | Bengaluru · Your area | Which area? (**Bengaluru areas**) · How old are you? |
| 12 | Bengaluru · About you | same as 3 |
| 13 | Bengaluru · Your orders | same as 4 |
| 14 | Bengaluru · Your last order | same as 5 |
| 15 | Bengaluru · Ownly | same as 6 |
| 16 | Bengaluru · About Ownly | same as 7 (**Bengaluru description**) |
| 17 | Bengaluru · A bit more about Ownly | same as 8 |
| 18 | Bengaluru · A bit more about Ownly (2) | same as 9 |
| 19 | Bengaluru · Ownly users | Where first heard · FIRST order (**4 options**) · Orders 5–8 weeks ago · If Ownly didn't exist · How would you feel without Ownly · **Why you order less** · ONE change *(no "Where have you ordered")* |
| **Other city** | | |
| 20 | Other city · Your city | **Which city?** · How old are you? |
| 21 | Other city · About you | same as 3 |
| 22 | Other city · Your orders | same as 4 |
| 23 | Other city · Your last order | same as 5 |
| 24 | Other city · Ownly | Before today, which of these is true for you? (**3 options**) |
| 25 | Other city · About Ownly | **If Ownly launched in your city**, which ONE thing would most make you try it? |
| 26 | Other city · Ownly users | **Where did you order on Ownly?** · How would you feel without Ownly |
| **Closing** | | |
| 27 | Last question | Optional: WhatsApp number for a 10-minute chat |
| 28 | Thank you! | *(not-eligible page, no questions)* |

### 0B. Branching

**Answer-based** (tick ⋮ → **Go to section based on answer** on these questions):

| Section | Question | Answer → go to section |
|---|---|---|
| 1 | Which city… | Hyderabad → **2** · Bengaluru → **11** · Another city → **20** |
| 2 | How old are you? | Under 20 → **28** · 20–22 / 23–25 / 26–28 / 29–30 → **3** · Over 30 → **28** |
| 3 | Ordered online in last 4 weeks? | Yes → **4** · No → **6** |
| 6 | Ownly status | Hadn't heard → **7** · Heard, never opened → **8** · Opened, didn't order → **9** · Ordered → **10** |
| 11 | How old are you? | Under 20 → **28** · 20–30 bands → **12** · Over 30 → **28** |
| 12 | Ordered online in last 4 weeks? | Yes → **13** · No → **15** |
| 15 | Ownly status | Hadn't heard → **16** · Heard, never opened → **17** · Opened, didn't order → **18** · Ordered → **19** |
| 20 | How old are you? | Under 20 → **28** · 20–30 bands → **21** · Over 30 → **28** |
| 21 | Ordered online in last 4 weeks? | Yes → **22** · No → **24** |
| 24 | Ownly status (3 options) | Hadn't heard → **25** · Heard of it → **25** · Ordered → **26** |

**Page-based** (the **After section** dropdown at the bottom of a section):

| After section | Go to |
|---|---|
| 4 → 5 · 5 → 6 · 13 → 14 · 14 → 15 · 22 → 23 · 23 → 24 | the next section |
| 7, 8, 9, 10, 16, 17, 18, 19, 25, 26 | **27 Last question** |
| 27 and 28 | **Submit form** |

**Paths through the form:**
```
1 City
├─ Hyderabad → 2 Area+Age ─(under 20 / over 30)→ 28 Thank you → Submit
│              └→ 3 About you ─ Yes → 4 Orders → 5 Last order → 6 Ownly
│                             └ No ─────────────────────────────→ 6 Ownly
│              6 Ownly ─ hadn't heard → 7  ─┐
│                      ├ heard ────→ 8  ─┤
│                      ├ opened ───→ 9  ─┼→ 27 Last question → Submit
│                      └ ordered ──→ 10 ─┘
├─ Bengaluru → 11 → 12 → (13 → 14) → 15 → 16 / 17 / 18 / 19 → 27 → Submit
└─ Another city → 20 → 21 → (22 → 23) → 24 → 25 or 26 → 27 → Submit
```

---

## Part 1 · Create the form (5 min)

1. Go to **forms.google.com** and click **Blank form**.
2. Click "Untitled form" at the **top left** (the file name) and paste:

**File name**
```
Ownly Food Delivery Survey v5
```

3. Click "Untitled form" inside the **top card** and paste:

**Form title**
```
How young India orders food: 4-minute student survey
```

4. Click "Form description" and paste:

**Form description**
```
Hi! Thanks for opening this 🙂
We're Product Management students studying how people aged 20–30 order food online: which apps they use, what they pay, and what makes them try a new app.

⏱ About 4 minutes, mostly taps and a few numbers · 🔒 Anonymous · 🎓 Independent student research, not linked to any food app or restaurant.

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

## Part 3 · Hyderabad path (sections 1–10)

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

#### S3-Q2 · Ordered online recently (keep it last)
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

---

### SECTION 6 · Hyderabad · Ownly

**Section title**
```
Hyderabad · Ownly
```
**Section description:** leave empty

#### S6-Q1 · Ownly status
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

### SECTION 7 · Hyderabad · About Ownly

**Section title**
```
Hyderabad · About Ownly
```
**Section description**
```
About Ownly: a food delivery app from Rapido. Restaurants pay Ownly no commission, so menu prices are meant to match the restaurant's own prices. There's no platform, packaging or surge fee; you pay for the food plus delivery. It started in Hyderabad in September 2026.
```

#### S7-Q1 · What would make you try it
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

### SECTION 8 · Hyderabad · A bit more about Ownly

**Section title**
```
Hyderabad · A bit more about Ownly
```
**Section description:** leave empty

#### S8-Q1 · Where first heard
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

#### S8-Q2 · Why not opened
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

### SECTION 9 · Hyderabad · A bit more about Ownly (2)

**Section title**
```
Hyderabad · A bit more about Ownly (2)
```
**Section description:** leave empty

#### S9-Q1 · Where first heard
- **Type:** Multiple choice · **Required:** ON
- Paste the same question and options as **S8-Q1**:

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

#### S9-Q2 · What stopped ordering
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

### SECTION 10 · Hyderabad · Ownly users

**Section title**
```
Hyderabad · Ownly users
```
**Section description**
```
A few questions about Ownly. Your answers are the most valuable part of this survey 🙏
```

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

#### S10-Q2 · Where ordered
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

#### S10-Q3 · First order
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

#### S10-Q4 · Orders 5–8 weeks ago
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

#### S10-Q5 · If Ownly didn't exist
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

#### S10-Q6 · Disappointment (Sean Ellis)
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

#### S10-Q7 · One change
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

✅ **Checkpoint:** the last section header reads **"Section 10 of 10"**.

---

## Part 4 · Bengaluru path (sections 11–19)

### 4a. Duplicate sections 2–10

Do these 4 steps for **Hyderabad sections 2, 3, 4, 5, 6, 7, 8, 9, 10**, in that order:
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
| 6 | `Bengaluru · Ownly` |
| 7 | `Bengaluru · About Ownly` |
| 8 | `Bengaluru · A bit more about Ownly` |
| 9 | `Bengaluru · A bit more about Ownly (2)` |
| 10 | `Bengaluru · Ownly users` |

✅ **Checkpoint:** sections 11–19 are the Bengaluru pages, in the order above.

### 4b. Paste the Bengaluru changes

#### SECTION 11 · Bengaluru · Your area → replace the area options
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

#### SECTION 16 · Bengaluru · About Ownly → replace the section description

**Section description**
```
About Ownly: a food delivery app from Rapido. Restaurants pay Ownly no commission, so menu prices are meant to match the restaurant's own prices. There's no platform, packaging or surge fee; you pay for the food plus delivery. It has been available across Bengaluru since March 2026.
```

#### SECTION 19 · Bengaluru · Ownly users → 3 changes

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

✅ **Checkpoint:** section 19 now has 7 questions: where first heard · FIRST order (4 options) · orders 5–8 weeks ago · if Ownly didn't exist · how would you feel · order less reason · ONE change.

---

## Part 5 · Other-city path (sections 20–26)

### 5a. Duplicate 7 sections

Same 4 steps as Part 4a, but only for **Hyderabad sections 2, 3, 4, 5, 6, 7, 10** (skip 8 and 9). Paste these titles:

| Copy of section | New section title (copy) |
|---|---|
| 2 | `Other city · Your city` |
| 3 | `Other city · About you` |
| 4 | `Other city · Your orders` |
| 5 | `Other city · Your last order` |
| 6 | `Other city · Ownly` |
| 7 | `Other city · About Ownly` |
| 10 | `Other city · Ownly users` |

✅ **Checkpoint:** sections 20–26 are the Other-city pages, in the order above.

### 5b. Paste the Other-city changes

#### SECTION 20 · Other city · Your city
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

#### SECTION 24 · Other city · Ownly
Replace the question text with:

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

#### SECTION 25 · Other city · About Ownly
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

#### SECTION 26 · Other city · Ownly users
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

✅ **Checkpoint:** section 26 has 2 questions.

---

## Part 6 · Last two pages (sections 27–28)

Click inside section 26, then **Add section**.

### SECTION 27 · Last question

**Section title**
```
Last question
```
**Section description**
```
That's it, thank you! 🙏
```

#### S27-Q1 · Interview volunteer
- **Type:** Short answer · **Required:** **OFF** ← the only optional question in the form

**Question**
```
Optional: Can we message you for a 10-minute chat about how you order food?
```
**Question description**
```
Leave your WhatsApp number if yes. It's only used for the chat and kept separately from your answers.
```

Click inside section 27, then **Add section** again.

### SECTION 28 · Not eligible

**Section title**
```
Thank you!
```
**Section description**
```
Thanks so much for your time! 🙏 This survey is for people aged 20–30. Please press Submit, and forward the link to friends in that age group.
```
No questions in this section.

✅ **Checkpoint:** "Section 28 of 28".

---

## Part 7 · Set every branch (10 min)

> Duplicated sections still point to the Hyderabad pages. **Set every row below**, even ones that look right.

### 7a. Answer-based branching
On each question below, each option now has a dropdown on its right. Pick the section:

| Section | Question | Option → Go to section |
|---|---|---|
| 1 | Which city do you live, study or work in on most days? | Hyderabad → **2** · Bengaluru → **11** · Another city → **20** |
| 2 | How old are you? | Under 20 → **28** · 20–22 → **3** · 23–25 → **3** · 26–28 → **3** · 29–30 → **3** · Over 30 → **28** |
| 3 | In the last 4 weeks, did you order food online… | Yes → **4** · No → **6** |
| 6 | Ownly is a food delivery app by Rapido… | I hadn't heard of Ownly → **7** · I'd heard of it, but never opened it → **8** · I opened or browsed it, but didn't order → **9** · I've ordered on Ownly → **10** |
| 11 | How old are you? | Under 20 → **28** · 20–22 → **12** · 23–25 → **12** · 26–28 → **12** · 29–30 → **12** · Over 30 → **28** |
| 12 | In the last 4 weeks, did you order food online… | Yes → **13** · No → **15** |
| 15 | Ownly is a food delivery app by Rapido… | I hadn't heard of Ownly → **16** · I'd heard of it, but never opened it → **17** · I opened or browsed it, but didn't order → **18** · I've ordered on Ownly → **19** |
| 20 | How old are you? | Under 20 → **28** · 20–22 → **21** · 23–25 → **21** · 26–28 → **21** · 29–30 → **21** · Over 30 → **28** |
| 21 | In the last 4 weeks, did you order food online… | Yes → **22** · No → **24** |
| 24 | Ownly is a food delivery app by Rapido, available in… | I hadn't heard of Ownly → **25** · I'd heard of it → **25** · I've ordered on Ownly (e.g. …) → **26** |

### 7b. Page-based branching
At the **bottom** of each section, set **After section X**:

| Section | After section → |
|---|---|
| 4 Hyderabad · Your orders | Go to section **5** |
| 5 Hyderabad · Your last order | Go to section **6** |
| 7 Hyderabad · About Ownly | Go to section **27** |
| 8 Hyderabad · A bit more about Ownly | Go to section **27** |
| 9 Hyderabad · A bit more about Ownly (2) | Go to section **27** |
| 10 Hyderabad · Ownly users | Go to section **27** |
| 13 Bengaluru · Your orders | Go to section **14** |
| 14 Bengaluru · Your last order | Go to section **15** |
| 16 Bengaluru · About Ownly | Go to section **27** |
| 17 Bengaluru · A bit more about Ownly | Go to section **27** |
| 18 Bengaluru · A bit more about Ownly (2) | Go to section **27** |
| 19 Bengaluru · Ownly users | Go to section **27** |
| 22 Other city · Your orders | Go to section **23** |
| 23 Other city · Your last order | Go to section **24** |
| 25 Other city · About Ownly | Go to section **27** |
| 26 Other city · Ownly users | Go to section **27** |
| 27 Last question | **Submit form** |
| 28 Thank you! | **Submit form** |

Sections 1, 2, 3, 6, 11, 12, 15, 20, 21 and 24 contain an answer-based question, so their "After section" dropdown is ignored. That's normal.

---

## Part 8 · Connect Google Sheets (2 min)

1. **Responses** tab → **Link to Sheets** (green icon) → **Create a new spreadsheet**.
2. Paste the name:

**Spreadsheet name**
```
Ownly Survey v5 responses
```
3. Click **Create**. Don't edit this sheet by hand; copy data to another tab if you need to work on it.

---

## Part 9 · Test all 10 paths, then delete them (15 min)

Click **👁 Preview** and submit each test.

| # | Answer like this | You should end up on | Check |
|---|---|---|---|
| 1 | Hyderabad · Under 20 | Thank you! page | Submit works |
| 2 | Hyderabad · 23–25 · Student · ordered **No** · hadn't heard | Ownly → About Ownly (Hyderabad description) → Last question | No order questions shown |
| 3 | Hyderabad · Yes · counts 3/1/0/0 · Swiggy ₹250 Just me · heard, never opened | Orders → Last order → Ownly → A bit more (where heard + reason) → Last question | Typing `abc` in a count shows the error |
| 4 | Hyderabad · Yes · opened, didn't order | … → A bit more (2) (where heard + what stopped) → Last question | |
| 5 | Hyderabad · Yes · Ownly count 2 · ordered | … → Ownly users (7 questions incl. "Where have you ordered") → Last question | |
| 6 | Bengaluru · 26–28 · Yes · hadn't heard | Bengaluru pages → About Ownly with "since March 2026" → Last question | Bengaluru areas shown |
| 7 | Bengaluru · Yes · Ownly count 4 · ordered | Bengaluru Ownly users: 4 first-order options, "order less" question, no "Where have you ordered" | |
| 8 | Another city · Pune · 20–22 · Yes · hadn't heard | City list → orders → last order → 3-option Ownly question → "If Ownly launched in your city…" | |
| 9 | Another city · 23–25 · No · ordered on Ownly | 3-option Ownly question → Ownly users (2 questions) → Last question | |
| 10 | Bengaluru · Over 30 | Thank you! page | |

Also:
- **Search for leftovers** with Ctrl/Cmd + F in the editor: `Copy of`, `Option 1`, `[`. None should appear.
- **Check on a phone** by opening the Preview link once.

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

⏱ About 4 minutes, mostly taps and a few numbers
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
Hey! Hope you're doing well 🙂 Small favour: I'm doing a market research project for my PDM course on how people our age order food online. Could you fill in a quick survey? About 4 minutes, anonymous.

👉 [FORM LINK]

If you order food online, keep your order history handy (it asks how many orders you placed). And if you can, forward it to 2–3 friends aged 20–30, in any city. Thanks a ton! 🙏
```

**LinkedIn post**
```
Aged 20–30 and living in Bengaluru, Hyderabad or anywhere in India? I'd value 4 minutes of your time.

For my Product Management programme, our team is researching how young professionals and students choose food delivery apps: how often they order, what they pay, and what makes them try something new.

🕒 About 4 minutes · 🔒 Anonymous · 📱 Built for your phone
👉 [FORM LINK]

Everyone counts, including people who rarely order online. I'll share a summary of what we learn. Reposts are hugely appreciated 🙌

#ProductManagement #MarketResearch #Bengaluru #Hyderabad
```

**Reminder message**
```
Thank you to everyone who filled in the food delivery survey! 🙏 We still need more answers from [Hyderabad / Bengaluru / working professionals / people who rarely order online]. If you're 20–30 and haven't filled it yet: 👉 [FORM LINK] (about 4 min). Already did it? Forwarding it is the best help!
```

---

## Part 11 · Close the survey and load the dashboard (5 min)

**While collecting:** Responses tab → **Summary** → check the count per city. Targets: **≥ 80 Hyderabad**, **≥ 80 Bengaluru** (with ≥ 30 Ownly users), **≥ 40 other cities**.

**To close:** Responses tab → switch **Accepting responses** OFF → paste:

**Closed message**
```
This survey is now closed. Thank you for your help!
```

**To load the dashboard:**
1. Responses tab → **⋮** → **Download responses (.csv)**. It downloads a **.zip**.
2. Unzip it to get the `.csv`.
3. Open `Ownly/10_dashboard/ownly_transfer_scorecard.html` (or the published link) → **Upload survey CSV** → choose the `.csv`.
4. Scroll to **Data and quality**: **Missing** should say **none**. If a field is listed, a question title was changed; fix it using Appendix A1.

---

## Appendix A · Final checklist

### A1. Phrases the dashboard looks for in question titles
Don't change these phrases:

| Question | Title must contain |
|---|---|
| City | `Which city do you live` |
| Area / city | whole title exactly `Which area?` or `Which city?` |
| Age | `How old are you` |
| Occupation | `best describes you` |
| Ordered recently | `order food online for delivery at least once` |
| Counts | starts with `Swiggy: how many` · `Zomato: how many` · `Ownly (Rapido` · `Any other way` |
| Last order | `Which app did you use for your most recent` · `total amount you paid` · `How many people was that order for` |
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
- age bands `20–22` `23–25` `26–28` `29–30`
- status options starting `I hadn't heard` / `I'd heard` / `I opened` / `I've ordered`

### A3. Before you share
- [ ] 28 sections, in the order in Part 0A
- [ ] Only the WhatsApp question is optional
- [ ] All 5 number questions per city (4 counts + amount) and the 5–8-weeks question have number validation
- [ ] Every branch in Part 7a and 7b is set; Ownly pages go to 27; sections 27 and 28 go to Submit
- [ ] Settings: no emails · limit-1 OFF · progress bar ON · question shuffle OFF · confirmation message set
- [ ] No `Copy of`, `Option 1` or `[` anywhere
- [ ] Linked to a Google Sheet
- [ ] All 10 test paths passed, plus one check on a phone
- [ ] Test responses deleted from the form **and** the sheet

### A4. Common mistakes

| What you see | Cause | Fix |
|---|---|---|
| Bengaluru people land on Hyderabad pages | Duplicated branches still point to Hyderabad | Redo Part 7 for sections 11–26 |
| After an Ownly page, people see the next city's pages | "After section" left as "Continue to next section" | Set sections 7–10, 16–19, 25–26 to go to 27 |
| Under-20s can finish the survey | Age branches not set | Sections 2 / 11 / 20: Under 20 and Over 30 → 28 |
| People hit a Google sign-in | "Limit to 1 response" is ON | Settings → Responses → OFF |
| Pasted options became one long option | Paste didn't split into lines | Delete it and paste one line per option |
| "Other" shows a text box | Used "add 'Other'" | Delete it and paste `Other` as a normal option |
| Dashboard shows a field as "Missing" | A question title was reworded | Match Appendix A1 and re-download the CSV |
