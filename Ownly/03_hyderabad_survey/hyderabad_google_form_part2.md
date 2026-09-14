# Hyderabad Survey — Google Form Build Spec, Part 2 (S7–S10)

Conventions as in `hyderabad_google_form_part1.md`. This file is rendered from C2's design files:
- `bill_comparison_scenarios.md`
- `dce_design_matrix.csv`
- `wtp_gabor_granger_design.md`
- `randomization_and_versions.md`

**If those files change, they win.** Update this file to match.

**Version matrix:**

| Version | Concept | Choice-task block | Bill order | Fee-ladder start |
|---|---|---|---|---|
| V1 | Blind | 1 | Order 1 | ₹20 |
| V2 | Blind | 2 | Order 2 | ₹40 |
| V3 | Branded | 1 | Order 1 | ₹40 |
| V4 | Branded | 2 | Order 2 | ₹20 |

---

## S7 Bill scenarios (Section 17) — after section → *S8 Choice tasks*

**Section description:** "Next, 4 **made-up** examples of food-delivery bills. They are not real bills from any app. There are no right answers — tell us what you would really do."

**Rendering (all 4 questions):**
- Question type: Multiple choice · Req · Shuffle OFF.
- Add an image (⋮ → Add image) of the two bills side by side, built in Google Slides: same font, same row order (food → packaging → platform → delivery → discount → amount → time → rating), no logos or app colours. Label them "Bill 1" and "Bill 2".
- Paste the plain-text bill into the **question description** as the accessibility fallback.
- **Order 1 (V1, V3):** bills as listed below. **Order 2 (V2, V4):** swap Bill 1 and Bill 2 in the image and the description.
- The option labels themselves never change.

**Q52 `[bill_s1]`** — question title:
"Hypothetical example — not a real bill from any app. Both bills are for the same dinner from the same restaurant, arriving in the same time. All amounts include taxes. Which bill would you rather order with?"
- Description, Order 1: *Bill 1 — Food ₹210 · Delivery fee ₹35 · Amount to pay ₹245. Bill 2 — Food ₹210 · Packaging ₹20 · Platform fee ₹15 · Delivery fee ₹30 · Discount −₹30 · Amount to pay ₹245.*
- Options: Bill 1 (code 1) · Bill 2 (code 2) · No real difference to me (code 3)

**Q53 `[bill_s2]`** — title:
"Hypothetical example — not a real bill from any app. Both bills are for the same dish from the same restaurant, arriving in the same time. All amounts include taxes. Which bill would you rather order with?"
- Description, Order 1: *Bill 1 — Food ₹260 · Delivery fee ₹25 · Discount −₹50 ("Offer applied") · Amount to pay ₹235. Bill 2 — Food ₹210 · Delivery fee ₹25 · Amount to pay ₹235.*
- Options: Bill 1 · Bill 2 · No real difference to me

**Q54 `[bill_s3]`** — title:
"Hypothetical example — not a real bill from any app. You want this dinner tonight. One bill is on the app you use most; the other is on an app you have not used before. Same restaurant, same dish, same delivery time (30 minutes), same restaurant rating (4.3★). All amounts include taxes. Where would you order?"
- Description, Order 1: *Bill 1 (your usual app) — Food ₹230 · Packaging ₹15 · Platform fee ₹15 · Delivery fee ₹30 · Discount −₹20 · Amount to pay ₹270 · 30 min · 4.3★. Bill 2 (app you haven't used before) — Food ₹210 · Delivery fee ₹30 · Amount to pay ₹240 · 30 min · 4.3★.*
- Options: Bill 1 · Bill 2

**Q55 `[bill_s4]`** — title:
"Hypothetical example — not a real bill from any app. Same situation as the previous example, but this time the app you haven't used before shows a longer delivery time and a slightly lower restaurant rating. All amounts include taxes. Where would you order?"
- Description, Order 1: *Bill 1 (your usual app) — same line items as before · Amount to pay ₹270 · 30 min · 4.3★. Bill 2 (app you haven't used before) — same line items as before · Amount to pay ₹240 · **45 min** · **4.1★**.*
- Options: Bill 1 · Bill 2

*All ₹ values are PROVISIONAL (C2). Replace them with audit medians before fielding, keeping s1/s2 totals identical.*

---

## S8 Choice tasks (Section 18) — after section → *S9 New service*

**S8 Warm-up** is a text-only section. Its description is pasted verbatim from `choice_experiment_design.md` §3.1:

> **Choosing between two apps (7 quick questions)**
> Imagine you're ordering **the same dinner for one** tonight, from a restaurant you like. Two *hypothetical* apps can deliver it. They differ in:
> - **Total amount to pay:** food + every charge + taxes, all in one number
> - **Delivery time shown**
> - **How often it's late:** e.g. "3 of every 10 orders arrive 15+ minutes late"
> - **Your usual restaurants on the app:** most / some / few of the places you normally order from
> - **If something goes wrong:** automatic refund in 24 hours, or a refund only after you complain, case by case
>
> There are no right answers. Pick the app you would **actually** order from. If both seem similar, go with your first instinct.
>
> *Example (not a question):* App A costs ₹25 more but arrives 10 minutes sooner. App B is cheaper but slower. Choosing App A means the time mattered more to you than ₹25 here.

**Rendering** (per `choice_experiment_design.md` §3.2):
- **Sections:** each task is in **its own section** (`S8 Task 1` … `S8 Task 7`), so the table fits one screen. Every section's routing is "Continue to next section"; `S8 Task 7` → *S9 New service*.
- **Question:** one Multiple choice question per section. Required. Options never shuffled.
- **Image:** a two-column table made in Google Slides, using the same template for all 14 images. Header "Hypothetical apps". No colours implying good or bad; ₹ in bold.
- **Text fallback (description),** e.g. `App A — ₹235 | 45 min | late in 1 of 10 | some of your usual restaurants | automatic refund within 24h`.

Question title for every task: **"Task [k] of 7 — which app would you order from?"**
Options: App A (code 1) · App B (code 2). No opt-out.

**Legend for the tables below:** `auto` = "Automatic refund within 24 hours"; `case` = "Refund after you complain, case by case".

### Block 1 (V1, V3)

| Q | Position | Variable | App A | App B |
|---|---|---|---|---|
| Q56 | 1 | `dce_t1` | ₹235 · 45 min · 1 in 10 · Some · auto | ₹285 · 25 min · 1 in 10 · Some · auto |
| Q57 | 2 | `dce_t2` | ₹285 · 35 min · 1 in 10 · Most · case | ₹260 · 35 min · 3 in 10 · Most · case |
| Q58 | 3 | `dce_t3` | ₹235 · 35 min · 1 in 10 · Few · auto | ₹285 · 35 min · 1 in 10 · Most · auto |
| Q59 | 4 | `dce_dom` | ₹260 · 35 min · 1 in 10 · Most · auto | ₹285 · 45 min · 3 in 10 · Some · case |
| Q60 | 5 | `dce_t4` | ₹310 · 45 min · 1 in 10 · Some · case | ₹235 · 45 min · 3 in 10 · Some · case |
| Q61 | 6 | `dce_t5` | ₹260 · 35 min · 1 in 10 · Some · case | ₹285 · 35 min · 1 in 10 · Some · auto |
| Q62 | 7 | `dce_t6` | ₹310 · 25 min · 3 in 10 · Some · auto | ₹260 · 55 min · 1 in 10 · Most · case |

### Block 2 (V2, V4)

| Q | Position | Variable | App A | App B |
|---|---|---|---|---|
| Q56 | 1 | `dce_t1` | ₹310 · 35 min · 1 in 10 · Most · auto | ₹235 · 55 min · 1 in 10 · Most · auto |
| Q57 | 2 | `dce_t2` | ₹235 · 25 min · 3 in 10 · Some · auto | ₹260 · 25 min · 1 in 10 · Some · auto |
| Q58 | 3 | `dce_t3` | ₹285 · 45 min · 1 in 10 · Most · case | ₹260 · 45 min · 1 in 10 · Some · case |
| Q59 | 4 | `dce_dom` | ₹260 · 35 min · 1 in 10 · Most · auto | ₹285 · 45 min · 3 in 10 · Some · case |
| Q60 | 5 | `dce_t4` | ₹260 · 45 min · 3 in 10 · Few · case | ₹310 · 45 min · 1 in 10 · Few · case |
| Q61 | 6 | `dce_t5` | ₹285 · 55 min · 1 in 10 · Most · auto | ₹235 · 55 min · 1 in 10 · Most · case |
| Q62 | 7 | `dce_t6` | ₹235 · 45 min · 1 in 10 · Most · case | ₹285 · 25 min · 3 in 10 · Few · auto |

*QA: a second person checks every image against `dce_design_matrix.csv`, row by row. Choosing App B in `dce_dom` → `FLAG_dominance_fail`.*

---

## S9 New service (Section 19) — after section → *S10 Fee framing*

**Each form copy contains ONLY its own concept text.** Paste it as the section description, in bold.

- **V1, V2 (blind):**
  > "**Service X** is a food-delivery app where the food prices shown are the restaurant's own prices, and the checkout shows a single delivery charge instead of separate platform, packaging or other fees. Restaurants on it do not pay the app a commission on each order. The delivery time and the number of restaurants available vary by area."
- **V3, V4 (branded):** identical text, with "Service X" replaced:
  > "**Ownly, the food-delivery service from Rapido,** is a food-delivery app where the food prices shown are the restaurant's own prices, … vary by area."

Wording must match the interview card (`04_interviews/interview_guide_45min.md` §8.1). Do not add a ₹ figure, a savings %, logos or images.

In V3/V4 the question texts say "it", so they need no change.

**Q63 `[bt_appeal]`** · Linear scale 1–5 · Req · 1 = "Not at all appealing", 5 = "Extremely appealing"
"How appealing is this for your own food orders?"

**Q64 `[bt_trial_intent]`** · Multiple choice · Req · Shuffle OFF
"If it were available where you are, how likely are you to try it for one of your next few orders?"
- Definitely not
- Probably not
- Not sure
- Probably
- Definitely

**Q65 `[bt_trust]`** · Linear scale 1–5 · Req · 1 = "Not at all", 5 = "Completely"
"How much would you trust it with your order and payment?"

**Q66 `[bt_expected_reliability]`** · Multiple choice · Req
"How often would you expect orders from it to arrive on time?"
- Rarely
- Sometimes
- About half the time
- Mostly
- Almost always
- No idea

**Q67 `[bt_expected_price]`** · Multiple choice · Req
"Compared with the app you use most, what would you expect the final amount for the same order to be?"
- Much higher
- A bit higher
- About the same
- A bit lower
- Much lower
- Don't know

**Q68 `[bt_concern]`** · Paragraph · Req OFF
"What, if anything, would stop you from trying it?"

**Q69 `[bt_framing_pref]`** · Multiple choice · Req · **Shuffle ON**
"Which of these messages would most make you take a look at a new food-delivery app?"
- Same dinner. Smaller final bill.
- See the real price. Pay that price.
- A fair price only counts if dinner arrives.
- None of these would

*Shuffle cannot pin "None of these would" last; accepted. The analysis maps the text, not the position.*

---

## S10 Fee ladder (Sections 20a–20h)

**S10 Fee framing (text-only section)** — after section → the start-fee section: **₹20 in V1/V4**, **₹40 in V2/V3**.

Description (paste):

> **Imagine a food-delivery service that works like this:**
> • Food is charged at the restaurant's own menu prices.
> • There are no platform charges and no packaging charges.
> • The **only** amount added to your food is **one delivery charge**, shown to you before you order.
> • All amounts include taxes.
>
> Think about a dinner for one that you would normally order, where **the food costs ₹220**. On the next screens we'll show different delivery charges. For each one, tell us whether you would place this order through **this service**.

**Seven fee sections**, named `S10 Fee ₹0`, `S10 Fee ₹10`, `S10 Fee ₹20`, `S10 Fee ₹30`, `S10 Fee ₹40`, `S10 Fee ₹50`, `S10 Fee ₹60`.

Each section holds one Multiple choice question, Req, branching ON. Always refer to "this service" — never a brand, not even in V3/V4.

- **Title:** "For this ₹220 dinner, the delivery charge is **₹[FEE]**. Would you place this order through this service?"
- **Options:** Yes, I would order (1) · No, not at this delivery charge (0)
- **Variable:** `[wtp_accept_FEE]`

`END` below = the first post-ladder section: **S11a Reveal** in V1/V2, **S11b Rapido** in V3/V4.

**Routing, Graph A — start ₹20 (V1, V4):**

| Section | Yes → | No → |
|---|---|---|
| ₹20 | ₹30 | ₹10 |
| ₹30 | ₹40 | END |
| ₹40 | ₹50 | END |
| ₹50 | ₹60 | END |
| ₹60 | END | END |
| ₹10 | END | ₹0 |
| ₹0 | END | END |

**Routing, Graph B — start ₹40 (V2, V3):**

| Section | Yes → | No → |
|---|---|---|
| ₹40 | ₹50 | ₹30 |
| ₹50 | ₹60 | END |
| ₹60 | END | END |
| ₹30 | END | ₹20 |
| ₹20 | END | ₹10 |
| ₹10 | END | ₹0 |
| ₹0 | END | END |

**Build notes:**
- Set **both** options' routing explicitly in every fee section.
- The editor places fee sections in physical order; routing, not position, decides the path.
- `wtp_start` is **not** a question. It is added in cleaning from `meta_form_version`.
- Continued in `hyderabad_google_form_part2b.md` (S11–S14, build checklist, QA personas).
