# How to Fill the Lite Audit Sheets (3-day plan)

Import `audit_lite_template.csv` and `test_orders_template.csv` into Google Sheets. **One row per app screen captured.**

| Column | How to fill |
|---|---|
| `capture_ts` | `2026-09-15T13:05`. Sync both auditors' clocks; capture all platforms within 10 minutes of each other. |
| `slot` | `tue_lunch`, `tue_dinner` or `wed_dinner` |
| `auditor_id` | A / B |
| `drop_point_id` | DP1 (keep the real address private, out of the sheet) |
| `platform` | `ownly`, `swiggy`, `zomato` or `toing` — lowercase, exactly these words |
| `account_state` | `existing` or `new` |
| `subscription_active` | y/n (Swiggy One / Zomato Gold on this account) |
| `restaurant_name` | Spell it **identically** on every platform (the script matches on this) |
| `restaurant_listed`, `restaurant_open` | y/n. If not listed, fill only the columns up to here. |
| `basket_id` | B1 = the same single-person item(s) on every app |
| `item_match_quality` | exact / close / none |
| `menu_subtotal` … `taxes_gst` | Numbers only, no ₹. Blank = 0. Enter the delivery fee exactly as charged; if the app shows "FREE", enter 0 and write "shown as FREE" in `notes`. |
| `discount_amount`, `discount_type` | Auto-applied coupon or offer. **If a coupon is applied, add a second row for the same capture with the coupon removed** (discount_amount = 0, discount_type = none). |
| `final_payable` | The "To pay" amount |
| `eta_min_shown`, `eta_max_shown` | e.g. 30 and 35 for "30–35 min"; the same number twice if one value is shown |
| `screenshot_file` | `DP1_tue_lunch_ownly_paradise.png` |

**Test orders sheet:**
- One row per real order.
- Timestamps as `2026-09-16T20:05`: order placed, rider picked up, delivered.
- `order_accurate` = y/n.

**Run on Thursday morning** (from the project folder):

```
python3 09_analysis/short_plan/analyze_audit_lite.py audit_captures.csv test_orders.csv --out 09_analysis/short_plan/audit_outputs
python3 09_analysis/short_plan/analyze_short_survey.py survey_export.csv --out 09_analysis/short_plan/survey_outputs
```
