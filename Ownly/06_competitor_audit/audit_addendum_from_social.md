# Audit Addendum: Additions Motivated by Review and Social Signals (lead, 2026-09-14)

Source: `05_review_mining/voc_synthesis_pre_fieldwork.md`. These signals are self-selected (CONSUMER-GENERATED) and serve only as reasons to **measure**, not as findings.

| # | Addition | Why | How to record, using existing schema columns where possible |
|---|---|---|---|
| A1 | **Capture each checkout twice when an offer exists:** (a) as shown with the best auto-applied offer/coupon, (b) without the coupon, where the app allows removing it. Record card offers shown but not applied. | Social posts report incumbent coupons and card offers erasing Ownly's gap; H2.3 must compare against the *discounted* total | Two rows per capture: `discount_type` = none / coupon / card_offer / subscription; `notes` = "paired_capture_id=…" |
| A2 | **Small-cart basket (< ₹150)** for 4–6 frame restaurants | Reports of small carts being cancelled or carrying small-order fees | New `basket_id` B4_smallcart; record `small_cart_fee` and whether checkout is allowed |
| A3 | **Large group basket (≥ ₹1,000)** for 3–4 restaurants, one dinner slot per week | Reports that large orders feel riskier; incumbent card offers often need higher totals | New `basket_id` B5_group |
| A4 | **Strike-through / "MRP" price vs listed price** on Ownly and incumbents | Disputed "inflated MRP" claims | Put the strike-through value in `notes` as "mrp_shown=₹…"; never treat it as a verified offline price |
| A5 | **Listed but not accepting orders** | Social reports of listings that fail at checkout | `restaurant_open` = n, with `notes` = "listed_not_accepting" |
| A6 | **Delivery fee exactly as displayed**, including "₹0", "free" or struck-through fees, and any distance note | Fee is contested across sources | `delivery_fee` + `notes` with the verbatim fee text |
| A7 | **Swiggy Toing** where it serves the drop point | Seen as the like-for-like affordability rival | `platform` = toing |
| A8 | **New-user / referral offers** (e.g. "up to ₹100 off first order") recorded but analysed separately | Launch offers inflate first-order savings | `account_state` = new; `promo_banner_text` |

All additions are optional if the audit is running in its reduced 1-week fallback, except **A1 and A6, which are mandatory**.
