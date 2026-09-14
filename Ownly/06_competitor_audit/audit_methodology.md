# Competitor Basket Audit — Methodology (Gachibowli)

**Version:** v1, 2026-09-14. Owner: Person 1 (with a second auditor for same-minute captures).
**Status:** DESIGN. No audit data exists yet. All platform fee/price claims in the project remain COMPANY CLAIM / MEDIA REPORT until this audit produces observations.

## 0. What → why → how → analysis → decision
| What we collect | Why | How | How we analyse | Decision it enables |
|---|---|---|---|---|
| Checkout-screen totals, fee lines, discounts, ETA, distance and listing/open status for matched restaurant × basket × time slot × drop point × account state across Ownly, Swiggy, Zomato (+ Magicpin if relevant) | Survey answers about "cheaper" and app-review complaints are perceptions. The core proposition ("lower transparent total price") is only credible if the **actual payable totals** are lower, **consistently**, **for restaurants people want**, **without an ETA penalty**. | Manual capture on team members' own phones and real accounts, stopping before payment. Two auditors capture simultaneously. Screenshot evidence for every row. Optional small set of real test orders for actual ETA/accuracy. | Matched pairwise gaps (median + bootstrap 95% CI), win rates, fee-stack decomposition, coverage rates, ETA gap, consistency by slot/day (`audit_calculations.md`) | Is the price advantage real, how large, and how consistent (H2)? Is it bought with longer ETA (H3)? Is coverage adequate (H5/H10)? Do Bengaluru claims hold in Gachibowli (H9)? Calibrates realistic ₹ and minute levels for survey choice tasks and bill scenarios, and feeds dashboard View 9. |

**Hypotheses served:** H2 (total price advantage), H3 (price vs ETA), H5 & H10 (restaurant choice/coverage threshold), H9 (Bengaluru claims transfer to Gachibowli). Secondary: H8 (observed delivery-fee levels anchor the WTP ladder).

---

## 1. Platforms
| Platform | Access path | Notes |
|---|---|---|
| Ownly | Standalone Ownly app **and/or** the Ownly tab inside the Rapido app, whichever serves Gachibowli at audit time (record in `notes` and keep constant; if both exist, capture both in the pilot day and check whether totals differ) | Verify Hyderabad service availability at each drop point on Day 0 |
| Swiggy | Swiggy app (food) | Record Swiggy One status |
| Zomato | Zomato app (food delivery) | Record Zomato Gold status |
| Magicpin / other (optional) | Magicpin app food delivery or other relevant entrant (e.g. an ONDC buyer app) | Include only if ≥30% of frame restaurants are listed in the pilot; otherwise note "not audited" |

## 2. Drop-point design (3 fixed delivery addresses)
The team picks exact addresses, records them **privately** (not in shared files), and uses only IDs in the dataset.

| drop_point_id | Type | Selection guidance |
|---|---|---|
| DP1_CAMPUS | Student campus gate area | A main gate/delivery point used by students near Gachibowli (e.g. a university gate area). Use a public gate location, not a private hostel room. |
| DP2_OFFICE | Financial District / Nanakramguda office area | A public entrance of a large office campus/tech park used for food drop-offs |
| DP3_RESIDENTIAL | PG / shared-flat residential cluster | A residential lane with PGs/shared flats in Gachibowli (e.g. Telecom Nagar / Indira Nagar-type cluster) |

Rules: use the **same pin location** in every app (set by map pin, not typed text alone); note the distance each app shows. The three points should be within the Gachibowli service area of all audited platforms. If one platform doesn't serve a point, that is a coverage finding: record the row with `restaurant_listed = n` and note "area not serviceable".

## 3. Restaurant sampling frame (20–25 restaurants)
**Purpose:** compare like-for-like **and** measure coverage. It is not a random sample of Hyderabad restaurants, so results generalise only to this frame (state this in every chart note).

### 3.1 Build the frame (Day 0)
1. From each drop point, open each platform and note the restaurants shown under broad searches ("biryani", "south indian", "north indian", "pizza/burger", "cafe", "dessert"). Also include restaurants participants mentioned in pilot interviews/survey pilot (if available).
2. Build a **candidate list of ~40** restaurants, recording on_ownly / on_swiggy / on_zomato / on_other (`restaurant_frame_template.csv`).
3. Select **20–25** using the stratified quota below. **Include ~5 restaurants that are on Swiggy/Zomato but NOT on Ownly** (coverage measurement) and, if any exist, 1–2 on Ownly but not on the others.

### 3.2 Stratification quota (target 24)
| Dimension | Target distribution |
|---|---|
| Price tier (per-person menu cost): budget <₹200 / mid ₹200–400 / premium >₹400 | 9 / 10 / 5 |
| Chain (national/regional, ≥3 outlets) vs local independent | ~10 chain / ~14 local |
| Cuisine | biryani/Hyderabadi 5; South Indian 4; North Indian/thali 4; fast food (burger/pizza/rolls) 5; cafe/beverages 3; desserts 3 |
| Listing overlap | ≥16 listed on Ownly + ≥1 incumbent (matched comparisons); ~5 on incumbents only; remaining as found |
| Late-night availability | ≥5 restaurants that typically open after 23:00 (for the late-night slot) |

Record `selection_reason` for every restaurant (e.g. "budget biryani, local, on all 3").

## 4. Basket definitions
Define baskets **per restaurant** on Day 0 and freeze them. Use the **identical items and variants** across platforms. Where an identical item doesn't exist, use the closest equivalent, set `item_match_quality = close` and document the difference in `item_list`. If there is no reasonable equivalent → `none`, excluded from pairwise comparison but kept for coverage.

| basket_id suffix | Basket type | Target menu subtotal | Purpose |
|---|---|---|---|
| `_B1` | Single-person meal (1 main + 1 side/drink) | ~₹150–300 | Core weekday use case for 20–30 users |
| `_B2` | Two-person meal (2 mains + 1–2 sides) | ~₹400–600 | Shared-flat/couple/group ordering |
| `_B3` | Small cart: snack/beverage only | ~₹80–150 (below typical minimum-order/small-cart thresholds) | Triggers small-cart fees and minimum-order rules |

Rules: no customisations or add-ons unless needed for a match; the same quantity; note size/portion. Basket IDs: `R07_B1`. Not every restaurant needs all three baskets: B1 is required for all; B2 for ≥12 restaurants; B3 for the ~8 cafe/dessert/fast-food restaurants.

## 5. Time slots and schedule
| slot | Window | Why |
|---|---|---|
| lunch_peak | Weekday 12:30–14:00 | Office/campus lunch; peak fees/ETA |
| off_peak | Weekday 16:00–18:00 | Baseline conditions |
| dinner_peak | Weekday 20:00–22:00 | Main delivery occasion |
| weekend_dinner | Sat/Sun 20:00–22:00 | Weekend demand, offers |
| late_night | Any day 23:00–00:30 | Coverage thins; students' late orders |

**Minimum feasible plan:** 2 weeks × (weekday lunch ×2, weekday dinner ×3, off-peak ×1, weekend dinner ×1, late-night ×1) per week = 16 sessions. In each session, audit a **rotating subset** of ~8 restaurants × B1 (+ B2/B3 where defined) × 1–2 drop points so that, over 2 weeks, every restaurant is captured in ≥3 slots and every drop point in ≥4 sessions. Use the schedule grid in `audit_field_sheet.md`.
**Reduced fallback (1 week):** 8 sessions, B1 only, DP1 + DP2, 20 restaurants. Label all outputs **directional**.

Record weather (rain → possible surge/rain fees) and special days (festival, cricket match, sale events) in `notes`, and never pool rain sessions with dry sessions without flagging.

## 6. Same-minute capture protocol
Prices, fees and ETAs change minute to minute, so the comparison is valid only if captured together.
- Two auditors (A and B), clocks synced to phone network time. Each captures one platform, or one auditor captures all platforms in sequence **within 5 minutes**. Record the exact `capture_ts` per row.
- Matched comparisons are valid only when captures for the same restaurant × basket × drop point × account state are **≤10 minutes apart** (flag 5–10 min as `timing_gap_flag` in notes; exclude >10 min from pairwise analysis).
- Randomise the **platform order** within a session (e.g. by die roll or a pre-generated order), so no platform is always captured first.

## 7. Account-state controls
Offers depend on the account (new-user coupons, targeted discounts, subscriptions), so account state is a recorded variable, not noise.
- Use **team members' own real, existing accounts only.** **Do not create fake, duplicate or throwaway accounts**, do not use others' accounts without permission, and do not abuse new-user offers. This keeps the audit within platform terms.
- Record `account_state`: `existing` (normal) or `new` (only if a team member genuinely has no prior account on that platform and legitimately signs up once; record it and never repeat it).
- Record `subscription_active` (y/n) and `subscription_saving_shown` (₹ shown by the app). Where a team member has Swiggy One/Zomato Gold, capture that account **and** a non-subscribed teammate's account in the same slot where possible, to produce both "list" and "member" views.
- **Primary comparison = existing account, no subscription, no manually applied coupon, automatic discounts included as shown.** Secondary views: best available coupon applied; subscription on.
- Keep a private `auditor_accounts.md` (not shared) mapping auditor_id → which platform accounts, their subscription state, and when it changed.

## 8. Capture procedure (stop before payment)
1. Set the drop-point pin. Search the restaurant. Record listed/open, distance and ETA shown on the restaurant page.
2. Add the frozen basket items. Go to cart/checkout. **Do not tap Pay / Place order.**
3. Expand all bill details ("bill details", "i" icons) and record every line: item subtotal, packaging, platform fee, delivery fee, small-cart fee, surge/rain/late-night fee, other fees (e.g. donation defaults — **remove optional donations/tips before capture** and note it), taxes, discounts (auto vs coupon), subscription savings, final payable, checkout ETA.
4. Screenshot the checkout (bill expanded) and the restaurant page (ETA/distance). Name the files per §9.
5. Empty the cart after capture so carts don't carry over.
6. Log any promo banners visible on the home screen/restaurant page (`promo_banner_text`).

### Optional: budgeted real test orders
- Purpose: measure **promised vs actual ETA** and **order accuracy** (reliability), which checkout screens can't show.
- Budget suggestion: 6–12 orders total (e.g. B1 baskets at ₹150–300 = ~₹1,500–3,500), spread across 2 platforms × 3 slots, **ordered in matched pairs** (the same restaurant, basket and slot on two platforms at the same time) where possible.
- Record `test_order_placed = y`, `actual_delivery_min` (from order-placed time to handoff), `order_accurate`. Eat or share the food; don't waste it.
- **Label all test-order findings "anecdotal (n = __)".** With ≤12 orders they illustrate variation and cannot estimate reliability rates.
- Do not file false complaints or refund claims to test support.

## 9. Evidence files
- Folder: `06_competitor_audit/screenshots/YYYY-MM-DD/` (keep outside any public share; blur the account name/phone/address before sharing any screenshot in slides).
- File name: `{YYYYMMDD}_{HHMM}_{slot}_{drop_point_id}_{platform}_{restaurant_id}_{basket_id}_{auditor_id}_{page}.png` where page ∈ `checkout` / `menu` / `store`. Example: `20260918_2034_dinner_peak_DP2_OFFICE_swiggy_R07_R07_B1_A1_checkout.png`
- `screenshot_file` in the dataset holds the checkout file name.

## 10. Offline price verification (never assume)
An "offline price" is used **only if independently verified**:
- **Accepted sources:** (a) in-person photo of the printed/board menu at the outlet, dated; (b) a dine-in or takeaway bill, dated; (c) the restaurant's own official website/menu PDF showing a date or captured with an access date. Record `offline_price_source` = menu_photo / dine_in_bill / takeaway_bill / official_website.
- Verification must be within **30 days** of the audit capture. Record the item prices for the **same basket**.
- If none is available: `offline_subtotal_verified` blank, `offline_price_source = unverified`, and **no premium-vs-offline claim** for that restaurant.
- Do **not** treat a platform's own "strike-through" price, a Google Maps review photo of unknown date, or a third-party menu site as a verified offline price.
- Aim to verify ≥8 restaurants (mix of tiers) near the drop points. Report results as "for the __ restaurants with verified offline menus".
- Takeaway may include packaging charges. Record them separately in `notes` and compare the food subtotal separately from the takeaway total.

## 11. Data-capture ethics and terms
- **Manual capture only.** No scraping, bots, API interception, automated clicking, emulators or screen-recording scripts on any platform.
- Use real, personal accounts as they normally function. No fake accounts, no promo abuse, no orders placed and cancelled to probe fees, no false complaints.
- Do not publish restaurant-identifying fee data in a way that suggests wrongdoing. Report aggregate findings, and name restaurants only if needed and as observed, dated facts.
- Screenshots may contain personal data (name, address, phone), so crop/blur before sharing.
- The audit observes publicly shown checkout information at a point in time. Always state date/time/slot/account state next to any number.

## 12. Quality assurance
- **Double entry of 10% of rows:** a second person re-enters randomly selected rows from screenshots only. Compute the field-level mismatch rate. If >2% on money fields, re-check that auditor's full session.
- **Arithmetic check:** `menu_subtotal + fee_stack + taxes_gst − discount_amount − subscription_saving_applied ≈ final_payable` (tolerance ±₹2). Flag mismatches → recheck the screenshot. Some apps fold taxes into fees; document per platform in `notes`.
- Validation rules per column: `audit_data_dictionary.md`.
- Daily: upload screenshots and the sheet, and record session completion in the schedule grid.
- Pilot (Day 0–1): 2 sessions × 5 restaurants, to test the time per capture (expect ~4–6 min per restaurant × platform), refine fee-line definitions per platform and freeze the schema.

## 13. Limitations (state in every output)
- Purposive frame of 20–25 restaurants in one micro-market over 1–2 weeks. Not representative of Hyderabad and not a market-wide price index.
- Account-level personalisation means a totals gap may differ for other users.
- Checkout screens show **promised** ETA only; reliability requires test orders (anecdotal) or survey/review evidence.
- Platform fees and policies change often, so findings are dated snapshots.
- Offline comparisons only apply where verified.

## 14. Outputs
1. `audit_data.csv` (schema `audit_schema.csv`) + screenshot archive
2. `restaurant_frame.csv` (from template)
3. Analysis outputs per `audit_calculations.md`: matched gap table, win rates, fee-stack chart data, coverage table, ETA gap table, slot consistency table
4. Calibration memo for survey scenarios: observed ranges of final payable, delivery/platform/packaging fees and ETA for B1/B2 baskets → survey/choice-experiment levels. Any synthetic survey scenario remains labelled "scenario" even when calibrated.
