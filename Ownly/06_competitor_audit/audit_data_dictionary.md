# Competitor Audit — Data Dictionary

**Version:** v1, 2026-09-14. Applies to `audit_schema.csv` (one row = one platform × restaurant × basket × drop point × account state × capture moment) and `restaurant_frame_template.csv`.
**General conventions:** money in ₹ as numbers with no symbol (e.g. `249` or `249.5`). A charge **shown as ₹0 or "FREE"** → `0`. A charge **not shown at all** → blank (not 0) plus a note if relevant. Timestamps are local IST in ISO format `YYYY-MM-DD HH:MM`. y/n fields are lowercase `y` / `n`. **No fabricated or "example" rows in the data file.**

## A. Audit dataset (`audit_schema.csv`)

| # | Column | Type | Definition | Allowed values / format | Validation rule |
|---|---|---|---|---|---|
| 1 | audit_id | string | Unique row ID | `AUD-YYYYMMDD-####` | Unique; not blank |
| 2 | capture_ts | datetime | Time the checkout screen was captured | `YYYY-MM-DD HH:MM` (IST) | Must fall inside the slot window (§slot); not in the future |
| 3 | day_of_week | category | Day of capture | Mon, Tue, Wed, Thu, Fri, Sat, Sun | Must match capture_ts |
| 4 | slot | category | Time slot | lunch_peak (weekday 12:30–14:00), off_peak (weekday 16:00–18:00), dinner_peak (weekday 20:00–22:00), weekend_dinner (Sat/Sun 20:00–22:00), late_night (23:00–00:30) | Consistent with capture_ts and day_of_week |
| 5 | auditor_id | category | Team member code | A1, A2, A3 | Not blank |
| 6 | drop_point_id | category | Fixed delivery pin | DP1_CAMPUS, DP2_OFFICE, DP3_RESIDENTIAL | Not blank |
| 7 | platform | category | Platform audited | ownly, ownly_in_rapido, swiggy, zomato, magicpin, other_<name> | Not blank |
| 8 | account_state | category | Account type used | existing, new | `new` at most once per auditor×platform |
| 9 | subscription_active | y/n | Paid membership active on this account (Swiggy One/Lite, Zomato Gold, other) | y, n | If y → note the plan name in notes |
| 10 | restaurant_id | string | Frame ID | `R01`–`R40` | Must exist in restaurant_frame |
| 11 | restaurant_name | string | Name as shown in the app | text | Should match the frame name (minor spelling differences allowed) |
| 12 | restaurant_listed | y/n | Restaurant found on this platform for this drop point | y, n | If n → rows 13–38 blank except notes |
| 13 | restaurant_open | y/n | Accepting orders at capture time | y, n | If n → money fields blank |
| 14 | distance_km_shown | number | Distance shown by the app | ≥0, 1 decimal | Blank if not shown; flag >15 |
| 15 | basket_id | string | Frozen basket | `R##_B1` / `_B2` / `_B3` | Restaurant prefix must equal restaurant_id |
| 16 | item_list | string | Items × qty × variant actually added; differences from the frozen basket | e.g. `Chicken Dum Biryani (Full) x1; Coke 250ml x1` | Not blank when listed & open |
| 17 | item_match_quality | category | Match to the frozen basket | exact, close, none | `none` → excluded from pairwise comparisons |
| 18 | menu_subtotal | number | Sum of item prices shown in the cart before fees, taxes and discounts | ≥0 | Required when listed & open & match ≠ none |
| 19 | offline_subtotal_verified | number | Same basket priced from a verified offline source | ≥0 or blank | Blank unless offline_price_source ≠ unverified; source date within 30 days |
| 20 | offline_price_source | category | Verification source | menu_photo, dine_in_bill, takeaway_bill, official_website, unverified | Default `unverified` |
| 21 | packaging_fee | number | Restaurant packaging/container charge shown | ≥0 or blank | — |
| 22 | platform_fee | number | Platform/convenience/service fee | ≥0 or blank | — |
| 23 | delivery_fee | number | Delivery partner fee **after** any shown free-delivery waiver (enter the payable delivery amount; put the struck-through amount in notes) | ≥0 or blank | — |
| 24 | small_cart_fee | number | Small order / minimum-order surcharge | ≥0 or blank | Expected mainly for B3 baskets |
| 25 | surge_rain_fee | number | Rain, surge, high-demand, late-night or long-distance fee | ≥0 or blank | If >0 → note the fee label in notes |
| 26 | other_fees | number | Any other charge (e.g. restaurant service charge); **exclude optional donations/tips (remove before capture)** | ≥0 or blank | If >0 → describe in notes |
| 27 | taxes_gst | number | Taxes shown separately (GST on food/fees). If the app merges taxes into fees, leave blank and note "taxes included in fees". | ≥0 or blank | — |
| 28 | discount_amount | number | Total discounts applied at checkout, as a **positive** number (auto offers + any coupon) | ≥0 | Must be ≤ menu_subtotal + fees |
| 29 | discount_type | category | Discount source | none, auto_offer, coupon_applied, restaurant_offer, bank_or_wallet_offer, multiple | Primary comparison uses none/auto_offer/restaurant_offer only |
| 30 | subscription_saving_shown | number | Saving the app attributes to the membership on this cart (₹) | ≥0 or blank | Blank if subscription_active = n |
| 31 | final_payable | number | Final "To pay" amount on checkout | >0 | Arithmetic check: abs(menu_subtotal + fee_stack + taxes_gst − discount_amount − [subscription savings not already in discount] − final_payable) ≤ 2, else flag |
| 32 | eta_min_shown | integer | Lower bound of ETA at checkout (minutes) | 5–120 | If a single ETA value is shown → same value in both min and max |
| 33 | eta_max_shown | integer | Upper bound of ETA at checkout | ≥ eta_min_shown, ≤180 | — |
| 34 | promo_banner_text | string | Short text of visible promo banners/offer labels (≤25 words) | text or blank | — |
| 35 | screenshot_file | string | Checkout screenshot file name | naming convention in methodology §9 | Required when listed & open; file must exist |
| 36 | test_order_placed | y/n | A real order was placed for this row | y, n | Default n |
| 37 | actual_delivery_min | integer | Minutes from order placed to handoff | ≥1 or blank | Only if test_order_placed = y |
| 38 | order_accurate | category | All items correct and complete | y, n, NA | NA unless test_order_placed = y |
| 39 | notes | string | Anything unusual: rain, festival, timing gap to paired capture, fee label wording, struck-through fees, taxes merged, area unserviceable, app used (standalone vs in-Rapido) | text | Required if any flag condition applies |

### Derived fields (computed in analysis, not entered)
| Field | Formula |
|---|---|
| fee_stack | sum of packaging_fee, platform_fee, delivery_fee, small_cart_fee, surge_rain_fee, other_fees (blank treated as 0 **only after** confirming "not shown" ≠ "not captured") |
| eta_mid_shown | (eta_min_shown + eta_max_shown) / 2 |
| capture_date | date part of capture_ts |
| match_key | restaurant_id \| basket_id \| drop_point_id \| slot \| capture_date \| session_id \| account_state \| subscription_active |
| arithmetic_flag | 1 if the final_payable check fails |
| valid_for_pairwise | listed = y AND open = y AND item_match_quality ∈ {exact, close} AND arithmetic_flag = 0 AND timing gap to comparator ≤ 10 min |
| primary_view | account_state = existing AND subscription_active = n AND discount_type ∈ {none, auto_offer, restaurant_offer} |

## B. Restaurant frame (`restaurant_frame_template.csv`)
| Column | Type | Allowed values | Rule |
|---|---|---|---|
| restaurant_id | string | R01–R40 | Unique |
| name | string | as shown on most platforms | — |
| locality | category | Gachibowli, Financial District/Nanakramguda, Kondapur, HITEC City/Madhapur, Manikonda/Narsingi, Other | Outlet locality |
| cuisine | category | biryani_hyderabadi, south_indian, north_indian_thali, fast_food, cafe_beverages, desserts, other | One primary |
| price_tier | category | budget (<₹200/person), mid (₹200–400), premium (>₹400) | Based on a typical single main + side |
| chain_or_local | category | chain (≥3 outlets), local | — |
| on_ownly / on_swiggy / on_zomato | category | y, n, unknown | Checked from DP1 on Day 0; update if changed (note date) |
| on_other | string | platform name(s) or blank | — |
| selection_reason | string | short text | Required |

## C. Missing-value codes summary
| Situation | Entry |
|---|---|
| Charge shown as ₹0 / FREE | 0 |
| Charge not displayed at all | blank |
| Could not capture (app error, screen closed) | blank + notes "not captured: reason" |
| Restaurant not listed / closed | listed/open = n; money fields blank |
| Offline price unverified | offline_subtotal_verified blank, source = unverified |
