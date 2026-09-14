# Ownly App-Store Review Codebook (inductive, v1 — AI first pass, needs human validation)

**Created:** 2026-09-14 by Agent B1. **Applies to:** `reviews_coded.csv` (n = 37).
**Status:** `coder = ai_first_pass`. No code is final until a human has checked `reviews_validation_sample.csv`.

---

## 1. How the taxonomy was built (and where we departed from the plan)

| Planned step | What actually happened | Why |
|---|---|---|
| Open-code a random sample of ~150 reviews | **All 37 accessible reviews were open-coded.** No sampling was needed or possible. | Robots-compliant retrieval returned only 37 unique reviews (see `methodology.md`). |
| Group open codes into themes; write inclusion/exclusion rules | Done. First-pass open codes (e.g., "rider went home", "chat stuck connecting", "₹216 not refunded") were grouped into the 25 codes below. The groups follow what reviewers **described**, not the brief's hypothesis list. | Keeps the taxonomy grounded in the data. Brief hypotheses are mapped afterwards in `analysis.md` §7. |
| Apply codes to all reviews | Done. Multi-label: a review can carry several `themes` and has exactly one `primary_theme`. | — |
| Blind re-code of a 10% subsample for self-agreement | **Not reported as a reliability statistic.** A re-code by the same AI coder in the same session is not independent, so any agreement figure would be misleadingly high. Instead, 7 of 37 primary-theme decisions (19%) are marked `AMBIGUOUS` in `coding_note`. | Honest reliability needs a second, independent coder (see §5). |
| Human validation sample of 50 rows | n < 50, so **all 37 rows** are in `reviews_validation_sample.csv`, with blank human columns. | — |

---

## 2. Theme codes

Codes are grouped for readability only; the groups are not analytic categories.

### A. Order fulfilment failures

| Code | Include when the review… | Exclude / use instead | Example review_ids |
|---|---|---|---|
| `NOT_DELIVERED_OR_FALSE_DELIVERED` | says food never arrived, or the order was marked "delivered" but not received | Delay where food eventually arrived → `LATE_DELIVERY_ETA_BREACH` | GO_a98eb27a20, AP_71e29404ff, AP_e74289b325 |
| `LATE_DELIVERY_ETA_BREACH` | describes a wait well beyond the promised ETA, a frozen or changing ETA, or waits of 45+ minutes | Order cancelled before dispatch with no long wait → `PLATFORM_RESTAURANT_CANCELLATION` | GO_3e282db9cd, AP_dc1c041a4b, GO_274cd3c567 |
| `PLATFORM_RESTAURANT_CANCELLATION` | says the order was cancelled by the platform or restaurant (auto-cancel, out of stock after acceptance, closed restaurant) | Customer asks to cancel and is refused → `CANCELLATION_BLOCKED` | GO_1b0e540633, GO_f66c0135bb, GO_a1c03f1646 |
| `CANCELLATION_BLOCKED` | says the customer tried to cancel a delayed order and could not (refused, option disabled) | — | GO_3e282db9cd, AP_dc1c041a4b |
| `PAYMENT_DEDUCTED_ORDER_FAILED` | says money was debited but no order was created or accepted | Money taken for a delivered-but-bad order → `REFUND_DELAY_OR_DENIAL` | GO_ef0cf51810, GO_6650009b66, GO_b68eea83bc |
| `RIDER_CONDUCT_OR_UNREACHABLE` | describes rider behaviour: unreachable, left, took another job, refused doorstep delivery, ignored instructions | Delay with no rider behaviour described → `LATE_DELIVERY_ETA_BREACH` | AP_adaff63850, GO_cb084c8b76, AP_43838c271d |
| `MISSING_OR_WRONG_ITEMS` | says items were missing or different from what was ordered | A veg/non-veg swap also gets `DIETARY_VEG_TRUST` | GO_46c3a579b3, GO_137c34ee72 |
| `DIETARY_VEG_TRUST` | describes a vegetarian or dietary expectation broken (wrong dish type, misleading Veg filter) | — | AP_6da397d1eb, GO_42d4fd7489 |
| `FOOD_QUALITY_HYGIENE` | describes stale, spoiled, contaminated (e.g., hair) or unacceptably prepared food | Wrong item only → `MISSING_OR_WRONG_ITEMS` | AP_717e816e40, GO_28e36312ca, GO_0b940e34ce |

### B. Service recovery

| Code | Include when | Exclude | Examples |
|---|---|---|---|
| `SUPPORT_UNRESPONSIVE_OR_SCRIPTED` | support is unreachable, bot-looping, scripted, closes tickets without resolving, or there is no phone channel | Support eventually fixed the problem → add `SUPPORT_RECOVERY_POSITIVE` | GO_a9b74f4c4f, AP_45ca8ef886 |
| `REFUND_DELAY_OR_DENIAL` | a refund is pending, slow (e.g., "4-7 days"), not credited, or refused | — | GO_1da47a1e4b, AP_71e29404ff, GO_3e282db9cd |
| `SUPPORT_RECOVERY_POSITIVE` | the problem was eventually resolved in a way the reviewer credits | — | AP_48f7c14d14 |

### C. Catalogue, app and payment

| Code | Include when | Examples |
|---|---|---|
| `LISTING_MENU_ACCURACY` | the listing does not match reality: closed restaurant shown, items out of stock after ordering, restaurant not delivering, offer paused, alleged duplicate or fake restaurant names | GO_a9b74f4c4f, GO_70f2ad2a7d, GO_0b940e34ce |
| `APP_CHECKOUT_BUG` | a checkout or order-placement function does not work | GO_38f94a509d, GO_28e36312ca |
| `NO_CASH_ON_DELIVERY` | explicitly asks for, or complains about the absence of, cash on delivery | GO_137c34ee72, GO_a1c03f1646 |

### D. Expectations and trust

| Code | Include when | Examples |
|---|---|---|
| `MARKETING_EXPECTATION_GAP` | contrasts ads, offers or promised ETA with the experience received | GO_ef0cf51810, AP_adaff63850 |
| `TRUST_LOSS_SCAM_FRAMING` | uses "scam", "loot", "cheated", "do not trust", or equivalent | GO_cb084c8b76, AP_e74289b325 |
| `EARLY_GOOD_THEN_DECLINE` | says early orders went well, then the experience worsened | GO_0b940e34ce, GO_ef0cf51810, AP_e74289b325 |

### E. Value and experience positives

| Code | Include when | Examples |
|---|---|---|
| `LOWER_PRICE_VALUE_POSITIVE` | praises lower or affordable prices or total cost | AP_eacd4d8693, GO_f66c0135bb, GO_46c3a579b3 |
| `NO_HIDDEN_FEES_POSITIVE` | praises the absence of platform, delivery, packaging or "miscellaneous" charges | GO_33ef06c9ab, AP_eacd4d8693, GO_0b940e34ce |
| `ON_TIME_DELIVERY_POSITIVE` | praises punctual delivery | GO_33ef06c9ab |
| `APP_UX_GENERAL_POSITIVE` | gives generic praise ("nice", "super", "simple, easy") | GO_ebd88deedd, GO_2ecb312b65 |

### F. Requests

| Code | Include when | Examples |
|---|---|---|
| `ASSORTMENT_MORE_RESTAURANTS` | asks for more, or more popular, restaurants | AP_eacd4d8693, GO_33ef06c9ab |
| `SERVICE_RADIUS_LIMIT` | mentions a delivery-distance cap blocking orders | AP_eacd4d8693 |
| `CITY_EXPANSION_REQUEST` | asks for service in a city where Ownly is not available | GO_81becd057e (Jabalpur), GO_9dc9ee308f (Chennai) |

---

## 3. Other coded fields

### Severity (1–4), scored per review for the worst issue described

| Score | Meaning |
|---|---|
| (blank) | No issue described (pure praise) |
| 1 | Cosmetic, request or suggestion |
| 2 | Inconvenience with no failed order or money at risk, or an issue already resolved |
| 3 | Failed or incorrect order, or money at risk (refund pending) |
| 4 | Safety, hygiene or dietary breach; fraud-like conduct; or money described as lost with the refund refused or unresolved after contacting support |

**Pending vs. denied refunds:** a refund described as "not received yet" scores 3. A refund refused, or described as lost after support contact, scores 4.

**Theme severity caveat:** mean severity for a theme uses the review's severity, so positive themes appearing inside negative reviews inherit that review's severity.

### Order stage

`order_stage` records where the primary failure (or praise) occurred: discovery_onboarding, browse_menu, pricing_checkout, payment, dispatch_eta, delivery_handoff, food_quality_accuracy, post_order_support_refund, app_account, or unspecified (generic praise).

### Sentiment rule

| Stars | Sentiment |
|---|---|
| 1–2 | `neg`, unless the text explicitly praises some part of Ownly → `mixed` |
| 3 | `mixed` |
| 4–5 | `pos`, unless the text contains a complaint → `mixed`. Suggestions or requests alone do not make it mixed. No evaluative content (e.g., only "please come to Chennai") → `neutral` |

### Behavioural flags

- **`switching_trigger_flag`:** 1 if the review states a reason for moving to Ownly or away from it. The direction is recorded in `switching_trigger_text` as `to_ownly:` or `away_from_ownly:`.
- **`churn_signal`:** 1 only for an explicit statement that the reviewer has stopped, uninstalled or will never use Ownly again. "Would not recommend" alone does not count.
- **`repeat_use_signal`:** 1 if the review gives evidence of more than one completed order or ongoing use. Where this is inferred from phrasing such as "really enjoying", the inference is noted in `coding_note`. Repeated failed attempts do not count.
- **`city_mentioned`:** set only when a city is explicitly named as the reviewer's location or service area.
  - Dish names such as "Hyderabadi biryani" do not count.
  - Restaurant names are not used to infer a city.

### Comment fields

`price_value_comment`, `delivery_eta_comment`, `assortment_comment`, `support_comment` and `trust_safety_quality_comment` hold **coder summaries, not quotes**. Text inside single quotes in these fields is verbatim.

---

## 4. Evidence label

All codes describe **CONSUMER-GENERATED** claims. The following are unverified allegations by single reviewers and must not be reported as facts:

- riders taking other apps' jobs (AP_adaff63850)
- "fake/duplicate restaurant names" (GO_0b940e34ce)
- a "15–20 of 50 orders delayed" rate (AP_dc1c041a4b)

---

## 5. Required human validation (before any of this goes into the dashboard)

1. Two team members independently fill the `human_*` columns in `reviews_validation_sample.csv` (all 37 rows) without looking at each other's work.
2. Compute Cohen's κ for `primary_theme` and `severity`, and % agreement per theme (present/absent).
3. Resolve disagreements by discussion. Record decisions in `human_notes` and update this codebook version (v1 → v2).
4. Set `human_verified = 1` in `reviews_coded.csv` for every reconciled row.
5. If κ < 0.6 for `primary_theme`, report theme counts at group level (A–F) only.
