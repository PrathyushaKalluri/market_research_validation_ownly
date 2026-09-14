# Competitor Audit — Auditor Field Sheet (phone checklist)

**Version:** v1, 2026-09-14. Carry this on your phone during every session. Rules are in `audit_methodology.md`; column definitions are in `audit_data_dictionary.md`.

## Hard rules (read before every session)
- ❌ Never tap **Pay / Place order** (unless this row is a pre-approved test order).
- ❌ No scraping, auto-clickers or scripts. Manual only.
- ❌ No fake/new throwaway accounts, no coupon abuse, no false complaints.
- ✅ Same drop-point **map pin** in every app.
- ✅ Captures for the same restaurant across platforms **within 10 minutes** (target ≤5).
- ✅ Remove optional donations/tips before capture.
- ✅ Screenshot every checkout with the bill details **expanded**.
- ✅ Blank ≠ 0: "FREE"/₹0 → `0`; not shown → blank.

## Before the session (5 min)
- [ ] Check the schedule grid: session ID, slot, drop point(s), restaurant subset, platform order (pre-generated random order).
- [ ] Sync the clock with auditor partner (phone network time). Agree the start minute.
- [ ] Note account state per app: logged-in account, subscription on/off (Swiggy One/Lite, Zomato Gold), any wallet/bank offer auto-applied.
- [ ] Empty all carts in all apps.
- [ ] Set the delivery pin to the drop point in all apps. Screenshot the address screen once (`..._address.png`, and blur it before sharing).
- [ ] Note weather (rain?) and special events → notes.
- [ ] Open the sheet row template: auditor_id, session_id, slot, drop_point_id pre-filled.

## Per restaurant × platform (≈4–6 min each)
1. **Search** the restaurant (use the frame name). Found? → `restaurant_listed` y/n. Not found → check spelling and one alternate name, then log `n` and move on.
2. **Open?** Accepting orders now? → `restaurant_open` y/n. Closed → log and move on.
3. On the restaurant page: note `distance_km_shown` and ETA shown. **Screenshot** (`..._store.png`).
4. **Add the frozen basket** (`basket_id` items, same variant/size/qty). Not identical? Pick the closest and write the difference in `item_list`, `item_match_quality` = close. No equivalent → `none`.
5. Go to **cart/checkout**. Remove donations/tips. Do **not** manually apply coupons for the primary view (auto offers are fine; note them).
6. **Expand bill details.** Record each line:
   - menu_subtotal ₹____
   - packaging_fee ₹____
   - platform_fee ₹____
   - delivery_fee ₹____ (struck-through original → notes)
   - small_cart_fee ₹____
   - surge_rain_fee ₹____ (label → notes)
   - other_fees ₹____ (label → notes)
   - taxes_gst ₹____ (or "included in fees" → notes)
   - discount_amount ₹____ / discount_type ____
   - subscription_saving_shown ₹____
   - **final_payable ₹____**
   - eta_min_shown ____ / eta_max_shown ____ (checkout ETA)
7. **Screenshot** the checkout with everything expanded (`..._checkout.png`). Scroll-capture if needed.
8. Visible promo banner/offer text? → `promo_banner_text` (short).
9. Quick arithmetic check: subtotal + fees + taxes − discounts ≈ final (±₹2)? If not, re-check the screen now and write "arith mismatch: reason" in notes.
10. **Empty the cart.** Next platform (follow the randomised order).
11. Optional secondary view (only if planned for this session): apply the best available coupon, capture again as a **separate row** with `discount_type = coupon_applied`.

## Screenshot naming
`{YYYYMMDD}_{HHMM}_{slot}_{drop_point_id}_{platform}_{restaurant_id}_{basket_id}_{auditor_id}_{page}.png`
e.g. `20260918_2034_dinner_peak_DP2_OFFICE_ownly_R07_R07_B1_A1_checkout.png`

## Test order rows only (pre-approved in the schedule)
- [ ] Place the order at the scheduled time (paired platform placed within 2 minutes by the partner).
- [ ] Note the order-placed time and ETA shown after placing.
- [ ] Note the handoff time → `actual_delivery_min`.
- [ ] Check items against the basket → `order_accurate` y/n (note what was wrong).
- [ ] `test_order_placed = y`. Keep the receipt screenshot (blur personal data).

## After the session (10 min)
- [ ] Upload screenshots to `06_competitor_audit/screenshots/YYYY-MM-DD/`.
- [ ] Finish the sheet rows; check that each listed & open row has a screenshot file name.
- [ ] Mark the session complete in the schedule grid; note skipped restaurants and why.
- [ ] Flag anything odd for the team (new fee type, app outage, restaurant delisted).

---

## Schedule grid template (fill before the audit; do not enter results here)

Legend: DP1 = campus gate, DP2 = office, DP3 = residential. Restaurant subsets S1–S3 rotate so every restaurant is captured in ≥3 slots over the period. Platform order: randomise per session (e.g. O-S-Z, Z-O-S…).

| session_id | Date | Day | Slot | Window | Drop point(s) | Restaurant subset | Baskets | Platform order | Auditors | Test orders? (y/n, which) | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S01 (pilot) | | | off_peak | 16:00–18:00 | DP1 | 5 pilot restaurants | B1 | | | n | | Time per capture: __ min |
| S02 (pilot) | | | dinner_peak | 20:00–22:00 | DP2 | 5 pilot restaurants | B1 | | | n | | |
| S03 | | Wk1 Mon–Fri | lunch_peak | 12:30–14:00 | DP2 | S1 | B1, B2 | | | | | |
| S04 | | Wk1 Mon–Fri | dinner_peak | 20:00–22:00 | DP1 | S2 | B1, B3 | | | | | |
| S05 | | Wk1 Mon–Fri | dinner_peak | 20:00–22:00 | DP3 | S3 | B1, B2 | | | | | |
| S06 | | Wk1 Mon–Fri | off_peak | 16:00–18:00 | DP2 | S1 | B1 | | | | | |
| S07 | | Wk1 Mon–Fri | lunch_peak | 12:30–14:00 | DP1 | S2 | B1 | | | | | |
| S08 | | Wk1 Mon–Fri | dinner_peak | 20:00–22:00 | DP2 | S3 | B1, B2 | | | | | |
| S09 | | Wk1 Sat/Sun | weekend_dinner | 20:00–22:00 | DP3 | S1 | B1, B2 | | | | | |
| S10 | | Wk1 any | late_night | 23:00–00:30 | DP1 | late-night set | B1, B3 | | | | | |
| S11 | | Wk2 Mon–Fri | lunch_peak | 12:30–14:00 | DP1 | S3 | B1, B2 | | | | | |
| S12 | | Wk2 Mon–Fri | dinner_peak | 20:00–22:00 | DP2 | S1 | B1, B3 | | | | | |
| S13 | | Wk2 Mon–Fri | dinner_peak | 20:00–22:00 | DP1 | S2 | B1, B2 | | | | | |
| S14 | | Wk2 Mon–Fri | off_peak | 16:00–18:00 | DP3 | S3 | B1 | | | | | |
| S15 | | Wk2 Mon–Fri | lunch_peak | 12:30–14:00 | DP3 | S1 | B1 | | | | | |
| S16 | | Wk2 Mon–Fri | dinner_peak | 20:00–22:00 | DP3 | S2 | B1, B2 | | | | | |
| S17 | | Wk2 Sat/Sun | weekend_dinner | 20:00–22:00 | DP2 | S2/S3 | B1, B2 | | | | | |
| S18 | | Wk2 any | late_night | 23:00–00:30 | DP3 | late-night set | B1, B3 | | | | | |

**Capacity check:** ~8 restaurants × 3 platforms × ~5 min ≈ 2 hours per session for one auditor, or ~1 hour with two auditors splitting platforms. If the pilot shows a longer time per capture, cut the subset to 5–6 restaurants per session rather than widening the 10-minute matching window.

**1-week fallback:** keep S03, S04, S05, S08, S09, S10, S12, S13 (compressed into one week), B1 only, DP1 + DP2. Label outputs directional.
