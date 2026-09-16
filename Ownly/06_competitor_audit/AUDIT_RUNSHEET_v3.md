# Gachibowli Price Audit — Runsheet (v3, LIVE)

**Owner: Person 3, with a second pair of hands. Cost: ₹0 (nothing is paid for).**
**This is the highest-value evidence per hour in the whole project** — it is the only thing that can
settle the price question with *observed* data rather than claims. 74% of our secondary base is media
report or company claim; this is ours.

## Before anything else — the Day-0 serviceability check (10 minutes, do it NOW)

1. Open **Ownly** (standalone app, and the food section inside **Rapido** — check both).
2. Set the delivery address to a real Gachibowli address. Use one address for the whole audit and
   call it **DP1**. **Keep the actual address out of the spreadsheet** — write only `DP1`.
3. Answer these four questions and send them to Claude immediately:
   - Does Ownly deliver to DP1? **Y / N**
   - Is Ownly a standalone app, inside Rapido, or both?
   - How many restaurants does it show for DP1?
   - Is **Toing** (Swiggy's budget app) live at DP1? **Y / N**

> **If Ownly does not serve Gachibowli, that is itself a headline finding — not a failure.** Then:
> audit the nearest served area instead (Madhapur / Kondapur / HITEC City), record which, and say so
> plainly in the deck. Do not quietly substitute an address and present it as Gachibowli.

## The frame — 10 restaurants, three groups

Open `restaurant_frame_PREFILLED.csv`. Groups A and C are named. **Fill in the four Group B names
yourself from what Ownly actually lists near DP1** — pick the cheapest real meals/tiffin places, because
those are the segment Ownly *says* it targets (meals under ₹150), as opposed to the regional chains it
*showcases*. Testing both is the point: if the price advantage only holds on showcase chains, the
proposition is narrower than the company claims.

If a Group A restaurant doesn't serve DP1, substitute another from
`17_ownly_hyderabad_restaurant_onboarding_targets.md` and note the substitution.

## Baskets — fix them before you start, never change mid-audit

| Basket | What | Rule |
|---|---|---|
| **B1** | One biryani / one main, single portion | Same item name and size on all three apps |
| **B2** | One QSR or dessert item, single portion | Same item |
| **B3** | One "meals for one" / thali / tiffin plate under ₹150 | Same item |

**Item match quality** goes in every row: `exact` / `close` / `none`. A `close` match is usable;
`none` means do not compute a price gap from that pair.

## The capture rules — these are what make the numbers defensible

1. **Same minute.** All three apps for one restaurant within **10 minutes** of each other. Two people
   working in parallel is the reliable way; sync your clocks first.
2. **Same address**, DP1, every time.
3. **Same account state.** Record `account_state` (`existing` / `new`) and `subscription_active` (y/n).
   If one of you has Swiggy One and the other doesn't, **that is useful** — capture both and record it.
   Do not "fix" it by cancelling a subscription.
4. **Stop at the checkout screen. Never place an order** during the audit (test orders are separate,
   below, and are deliberate).
5. **Coupons: capture twice.** If a coupon auto-applies, record that row, then remove the coupon and
   record a **second row** with `discount_amount = 0` and `discount_type = none`. The
   coupon-vs-no-coupon gap is exactly what the social data says decides the price question.
6. **Type the delivery fee exactly as shown.** If it says FREE, enter `0` and write `shown as FREE` in
   `notes`. Do not infer a fee that isn't displayed.
7. **Screenshot everything**, named exactly: `DP1_<slot>_<platform>_<restaurantID>.png`
   e.g. `DP1_wed_dinner_ownly_R1.png` — the names are **already pre-filled** in the capture sheet, so
   just match them. Save into `06_competitor_audit/screenshots/`.
8. **Coverage count:** search for **10 restaurants you'd normally order from** on Swiggy/Zomato and
   record how many are **missing on Ownly**. One line, huge finding, two minutes of work.

## Slots

`audit_captures_PREFILLED.csv` already has **60 empty rows** — 10 restaurants × 3 platforms × 2 slots —
with slot, platform, restaurant, basket and screenshot filename pre-filled. **You only type numbers.**

| Slot | When | Why |
|---|---|---|
| `wed_dinner` | Today, 19:30–21:30 | Peak. Surge and fees are at their most honest here. |
| `thu_lunch` | Tomorrow, 12:30–14:00 | Off-peak contrast — is the gap stable or slot-dependent? |

Two slots is the minimum that lets us say anything about stability. If time allows a third, add it —
but a complete two-slot grid beats a patchy three-slot one.

## Test orders — ₹900, only if the budget is approved and ethics covers it

`test_orders_template.csv`. Three real orders, same dish, same restaurant, same evening, one per app,
to DP1. Record: order timestamp, promised ETA, pickup timestamp, delivered timestamp, actual final
charge, whether the order was accurate.

**n=3 is an anecdote and must be labelled as one on the slide.** Its value is that it is the only
*promised-vs-actual* evidence in the project, and promised-vs-actual is the core of the reliability
proposition. Order the **cheapest single item that still makes a real order** — do not spend ₹900 on
three large baskets when three ₹200 orders answer the same question.

## What gets computed (Thursday morning, by Person 1)

```
python3 09_analysis/short_plan/analyze_audit_lite.py \
    06_competitor_audit/audit_captures_PREFILLED.csv \
    06_competitor_audit/test_orders.csv \
    --out 09_analysis/short_plan/audit_outputs
```

| Metric | Formula |
|---|---|
| Basket savings % | (competitor final payable − Ownly final payable) ÷ competitor final payable × 100 |
| **Ownly win rate** | % of matched comparisons where Ownly is cheapest (tie if within ₹5) — **with and without coupons, reported separately** |
| Fee share of bill | (final payable − menu subtotal) ÷ final payable, per platform |
| ETA gap | Ownly ETA midpoint − competitor ETA midpoint |
| Assortment overlap | benchmark restaurants listed on Ownly ÷ benchmark restaurants |
| Promised vs actual | delivered_ts − order_ts, against the ETA shown (test orders only) |

**The number that decides the price story:** median Ownly saving **with incumbent coupons applied**,
compared against the modal switching threshold from survey Q19. If the observed saving is below what
people say they'd need, the Bengaluru price proposition does not clear the bar in Gachibowli —
and that conclusion holds whichever way the fake door goes.

## Send Claude when the first slot is done
Not the whole sheet — just: how many of 10 restaurants were listed on Ownly, the Ownly / Swiggy / Zomato
final payable for the first three restaurants, whether coupons auto-applied on any app, and the
coverage count (how many of your 10 usual restaurants were missing on Ownly).
