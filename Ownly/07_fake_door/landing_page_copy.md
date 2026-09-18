> **Superseded for the live page on 2026-09-17 (D15):** the page now runs the v3 arms. See `FAKE_DOOR_v3_RUNBOOK.md`. This file documents v2.

# Landing-Page Copy — `hyd_vp_fakedoor_v1`

Source of truth for all on-page text. `prototype/index.html` implements it verbatim. Any change → bump `PAGE_VERSION` and log it.

**Rules applied**
- Unbranded concept. No Ownly/Rapido names, marks or colours. No "coming soon", no "order now".
- ₹ amounts appear only inside the illustrative bill, which is labelled and identical across variants.
- No verified-savings claims, no guarantees, no testimonials, no user counts.
- Only headline, subhead and the three supporting points change between variants.

---

## 1. Constant elements (all variants)

| Slot | Copy |
|---|---|
| Top strip, left | Food-delivery concept |
| Top strip, right (tag) | Research study |
| Eyebrow | Food delivery around Gachibowli |
| CTA (hero and bottom) | See how this would work → |
| Bill module title | Checkout, side by side |
| Bill module tag | Real price check · Gachibowli, 16 Sep |
| Bill caption | From a real price check we ran in Gachibowli on 16 September 2026: the same item, same address, two apps, within ten minutes, with no coupons applied. Prices change daily, and a coupon on either app can reverse this. Not a promise of savings on your order. |
| Footer | Independent university research prototype by a student team studying food delivery in Hyderabad. Not affiliated with any food-delivery company or restaurant. There is no app, no ordering and no payment on this page. |

### Bill module (REAL — our own Gachibowli audit, slot 1, 2026-09-16)

| Line | Typical app | This idea |
|---|---|---|
| Food item | ₹189 | ₹179 |
| Packaging | — | — |
| Platform fee | ₹15 | — |
| Delivery | ₹43 | ₹0 |
| Taxes | ₹12 | ₹9 |
| **You pay** | **₹259** | **₹188** |
| Difference in this example | | ₹71 |

Source (replaces the earlier assumption-based bill, 2026-09-17): one observed pair from our own price audit — the same dessert item at the same Gachibowli address (DP1), captured on both apps within ten minutes on 2026-09-16, with **no coupons applied on either side**. Row: `06_competitor_audit/audit_data_slot1.csv` (Cream Stone). This is the **mid-case** of our four comparisons, chosen deliberately: the largest observed gap ran to −52.6%, and printing that would overstate the typical case. Full analysis and caveats: `06_competitor_audit/audit_slot1_results.md`. **With each app's auto-offer applied the ranking flips in 2 of 4 comparisons**, which is why the caption says a coupon can reverse it. The bill is identical on both arms, so it cannot bias A vs B.

---

## 2. Variant copy

### Variant A — `A_total_price`

**Headline:** Same dinner. Smaller final bill.
**Subhead:** A delivery idea built around what you pay at the end: menu prices close to the restaurant's own, and one flat delivery fee.

| # | Point title | Point text |
|---|---|---|
| 1 | Judge the order by its total | Compare what actually leaves your account, not the discount banner. |
| 2 | Menu prices close to the restaurant's | Restaurants list their own prices instead of raising them for the app. |
| 3 | One flat delivery fee | The same fee for a small snack or a big dinner. |

### Variant B — `B_transparent_bill`

**Headline:** See the real price. Pay that price.
**Subhead:** A delivery idea with no surprise lines at checkout: the food price and one flat delivery fee, shown before you add anything to your cart.

| # | Point title | Point text |
|---|---|---|
| 1 | Every charge up front | The delivery fee is shown on the menu screen, not revealed at the last step. |
| 2 | No extra fee lines | No separate platform fee or small-cart fee added at checkout. |
| 3 | A bill you can check in five seconds | Food, delivery, taxes. That's the whole list. |

### Variant C — `C_reliable_value`

**Headline:** A fair price only counts if dinner arrives.
**Subhead:** A delivery idea that pairs visible, low-fee pricing with honest delivery times and a clear answer when an order goes wrong.

| # | Point title | Point text |
|---|---|---|
| 1 | Honest delivery times | The time shown is the time the order is planned around, not the most hopeful guess. |
| 2 | Fair, visible pricing | The food price and one flat delivery fee, shown before checkout. |
| 3 | Clear help when something goes wrong | Missing or very late orders get a named next step, not a long chat. |

Copy notes: C deliberately includes pricing (point 2) so it remains the same concept; its manipulation is *emphasis* on reliability. C avoids "guarantee", "always on time" and specific refund promises because no verified market offer supports them (app-review evidence shows refund and lateness failures are the most severe complaints, which motivates the framing but not a promise).

---

## 3. After the CTA (identical for all variants)

### Step 1 — Disclosure (shown immediately)
- **Badge:** Research prototype
- **Heading:** No app, no order, no payment.
- **Body:** We're a university student team studying how people around Gachibowli choose food delivery. This page is one of the ideas we're testing, and your tap is the signal we measure. Nothing was ordered and nothing will be charged.

### Step 1b — Higher-intent action (optional)
- **Label:** Optional
- **Heading:** Check your own last bill
- **Body:** Open your most recent food-delivery order and type two numbers. We'll show how far the final bill moved from the food price.
- **Field 1:** Food items total (₹) · placeholder "e.g. 240"
- **Field 2:** Final amount you paid (₹) · placeholder "e.g. 310"
- **Button:** Compare my bill (after first result: Compare again)
- **Secondary:** Skip this · Continue (after result)
- **Result (gap > 0):** Your final bill was ₹{gap} more than the food itself, {pct}% on top.
- **Result (gap < 0):** Your final bill was ₹{gap} less than the food price. Discounts outweighed the fees.
- **Result (gap = 0):** Your final bill matched the food price exactly.
- **Error (missing):** Enter both amounts, in rupees, from the same order.
- **Error (range):** Use amounts between ₹50 and ₹5,000, the range this check is built for.
- **Note:** Only these two numbers are recorded, with no name, phone, email or location.

### Step 2 — Mini-survey (optional)
- **Label:** Optional · 3 questions
- **Heading:** Help us read the results

| Variable | Question | Options (value) |
|---|---|---|
| `seg_occupation` | Which describes you best? | Student (`student`) · Working professional (`working_professional`) · Working and studying (`working_student`) · Other (`other`) · Prefer not to say (`prefer_not`) |
| `locality` | Where do you usually order food to? | Gachibowli · Financial District / Nanakramguda · HITEC City / Madhapur · Kondapur · Manikonda / Narsingi · Elsewhere in Hyderabad · Outside Hyderabad |
| `orders_4wk` | Food-delivery orders you placed in the last 4 weeks | None (`0`) · 1–3 (`1_3`) · 4–7 (`4_7`) · 8 or more (`8_plus`) · Not sure (`not_sure`) |

- **Buttons:** Send answers · Skip
- `orders_4wk` → `seg_freq`: 1–3 occasional, 4–7 regular, 8+ frequent (matches project convention; main survey's finer bands collapse into these).

### Step 3 — Thank you
- **Heading:** Thank you. That's everything.
- **Body (only if survey link set):** If you have about 10 minutes, our main survey on food delivery in Hyderabad helps the study even more.
- **Button:** Take the 10-minute survey (appends `src=fakedoor_{variant}`)
- **Close line:** You can close this page now.

---

## 4. Privacy notice ("What this page records", expandable in footer)

- Anonymous interaction events: page opened, scrolled, buttons tapped, and how long before a tap.
- A random ID stored in your browser so repeat visits aren't double-counted. No cookies from ad networks, no fingerprinting.
- The campaign tag in the link you opened (for example, which group shared it) and the referring website's domain.
- Only if you choose to answer: two bill amounts and three multiple-choice answers.
- Never recorded: your name, phone number, email, exact location or IP address.
- Data is used only for this university project, reported in aggregate, and deleted after the project ends.

---

## 5. Wireframe (mobile-first, 360–430 px; desktop centres a 460 px column)

```
┌───────────────────────────────────────┐
│ FOOD-DELIVERY CONCEPT   (Research study)│  ← constant strip
│                                         │
│ FOOD DELIVERY AROUND GACHIBOWLI         │  ← constant eyebrow
│ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
│ ┃ HEADLINE (varies A/B/C)            ┃ │
│ ┃ 2 lines max at 390 px              ┃ │
│ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ │
│ Subhead (varies), ≤ 3 lines             │
│ ┌─────────────────────────────────────┐ │
│ │     See how this would work  →      │ │  ← CTA #1 (constant)
│ └─────────────────────────────────────┘ │
│                                         │
│ ╭◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦╮ │  ← receipt, perforated edges
│ │ CHECKOUT, SIDE BY SIDE   REAL CHECK │ │
│ │ LINE          TYPICAL APP  THIS IDEA│ │
│ │ Food item           ₹189      ₹179  │ │
│ │ Packaging             —         —   │ │
│ │ Platform fee         ₹15        —   │ │
│ │ Delivery             ₹43       ₹0   │ │
│ │ Taxes                ₹12       ₹9   │ │
│ │ ─────────────────────────────────── │ │
│ │ You pay             ₹259      ₹188  │ │
│ │ Difference in this example   [₹71]  │ │
│ │ Real price check, Gachibowli 16 Sep…│ │
│ ╰◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦◦╯ │
│                                         │
│ [✓] Point 1 title (varies)              │
│     Point 1 text                        │
│ [✓] Point 2 title                       │
│     Point 2 text                        │
│ [✓] Point 3 title                       │
│     Point 3 text                        │
│ ┌─────────────────────────────────────┐ │
│ │     See how this would work  →      │ │  ← CTA #2 (constant)
│ └─────────────────────────────────────┘ │
│ ─────────────────────────────────────── │
│ Independent university research …       │
│ ▸ What this page records                │
└───────────────────────────────────────┘

After tap (same for all variants):
┌───────────────────────────────────────┐
│ ┌ (RESEARCH PROTOTYPE) ───────────────┐ │
│ │ No app, no order, no payment.       │ │
│ │ We're a university student team …   │ │
│ └─────────────────────────────────────┘ │
│ ┌ OPTIONAL ───────────────────────────┐ │
│ │ Check your own last bill            │ │
│ │ [₹ Food items total] [₹ Final paid] │ │
│ │ [ Compare my bill ]   Skip this     │ │
│ │ → "Your final bill was ₹70 more…"   │ │
│ │ [ Continue ]                        │ │
│ └─────────────────────────────────────┘ │
└───────────────────────────────────────┘
        ↓
┌ OPTIONAL · 3 QUESTIONS ────────────────┐
│ Which describes you best?  (chips)     │
│ Where do you usually order food to?    │
│ Orders in the last 4 weeks             │
│ [ Send answers ]   Skip                │
└────────────────────────────────────────┘
        ↓
┌ Thank you. That's everything. ─────────┐
│ [ Take the 10-minute survey ] (if set) │
└────────────────────────────────────────┘
```
