# Bill-Comparison Scenarios (synthetic research stimuli)

**Version:** 2026-09-14. **Hypotheses:** H2.2 (transparency), H2.4 (discount framing), H2 total-price value, H3/H2 (price vs ETA and rating).

All ₹ values are **PROVISIONAL**. They are calibrated to the national/Bengaluru fee anchors in `01_secondary_research/market_price_anchors.md` §2 and §5.3. Replace them with Gachibowli audit medians before fielding, keeping the arithmetic identities below. No scenario states or implies any real app's fees, and none mentions Ownly or a savings %.

## 1. Placement & rendering

- **Position in survey:** after pain and expectation items, **before** the choice tasks and before any concept. All respondents see the same scenarios; only the option order changes by version.
- **Header on every scenario (mandatory):** **"Hypothetical example — not a real bill from any app."**
- **Rendering in Google Forms:** each scenario is one multiple-choice question.
  - Build the two bills side by side as one image in Google Slides: the same font, the same row order, a light border, no logos or app colours.
  - Name the bills **"Bill 1"** (first shown: left on desktop, top on mobile) and **"Bill 2"**.
  - Put the plain-text version below into the question description as an accessibility fallback.
- **Option order:** **Order 1** (V1, V3, B1) shows the options as listed. **Order 2** (V2, V4, B2) swaps Bill 1 and Bill 2.
- **Codes:** `1` = Bill 1 (first shown), `2` = Bill 2, `3` = "No real difference to me" (bill_s1 and bill_s2 only).
- **Derived analysis variables** (computed in cleaning from code + version): `bill_s1_simple_chosen`, `bill_s2_nodiscount_chosen`, `bill_s3_newapp_chosen`, `bill_s4_newapp_chosen` (1/0; NA if code 3).
- **Why a "no difference" option on s1/s2:** the totals are identical, so forcing a choice would manufacture preferences. Indifference is itself a finding: transparency or framing does not matter. It is reported as a share, and the H2.2/H2.4 binomial tests use respondents who expressed a preference, alongside the indifferent share.
- **All amounts include taxes.** This avoids mixed GST rates (5% food, 18% delivery) in a stimulus. The stem states it explicitly.

## 2. Scenario bill_s1 — transparency at identical totals (H2.2)

**Stem:** "Hypothetical example — not a real bill from any app. Both bills are for the **same dinner from the same restaurant**, arriving in the **same time**. All amounts include taxes. Which bill would you rather order with?"

| | **Simple bill** | **Itemised bill** |
|---|---|---|
| Food (menu price) | ₹210 | ₹210 |
| Packaging charge | — | ₹20 |
| Platform fee | — | ₹15 |
| Delivery fee | ₹35 | ₹30 |
| Discount | — | −₹30 |
| **Amount to pay** | **₹245** | **₹245** |

Arithmetic: simple 210 + 35 = 245; itemised 210 + 20 + 15 + 30 − 30 = 245.

| Version order | Bill 1 | Bill 2 | Options |
|---|---|---|---|
| Order 1 | Simple | Itemised | Bill 1 / Bill 2 / No real difference to me |
| Order 2 | Itemised | Simple | Bill 1 / Bill 2 / No real difference to me |

**Analysis:**
- Share choosing simple among those with a preference: exact binomial test vs 50%, Wilson CI; threshold ≥ 60% (H2.2).
- Indifferent share with CI.
- Order effect: chi-square of choice × order (should be null).
- Exploratory split by `seg_occupation` and PPI band.

## 3. Scenario bill_s2 — discount framing at identical totals (H2.4)

**Stem:** "Hypothetical example — not a real bill from any app. Both bills are for the **same dish from the same restaurant**, arriving in the **same time**. All amounts include taxes. Which bill would you rather order with?"

| | **Discount bill** | **No-discount bill** |
|---|---|---|
| Food (menu price) | ₹260 | ₹210 |
| Delivery fee | ₹25 | ₹25 |
| Discount | −₹50 ("Offer applied") | — |
| **Amount to pay** | **₹235** | **₹235** |

Arithmetic: 260 + 25 − 50 = 235; 210 + 25 = 235.

| Version order | Bill 1 | Bill 2 |
|---|---|---|
| Order 1 | Discount | No-discount |
| Order 2 | No-discount | Discount |

Options: Bill 1 / Bill 2 / No real difference to me.

**Analysis:**
- Share choosing the discount bill among those with a preference: binomial vs 50%.
- Cross-tab with `beh_offer_dependency` (chi-square/Fisher, Cramér's V) → H1.5/H2.4.

## 4. Scenario bill_s3 — lower total on an app you haven't used (H2)

**Stem:** "Hypothetical example — not a real bill from any app. You want this dinner tonight. **Bill 1 / Bill 2** below: one is on **the app you use most**, the other is on **an app you have not used before**. Same restaurant, same dish, same delivery time (30 minutes), same restaurant rating (4.3★). All amounts include taxes. Where would you order?"

| | **Your usual app** | **App you haven't used before** |
|---|---|---|
| Food (menu price) | ₹230 | ₹210 |
| Packaging charge | ₹15 | — |
| Platform fee | ₹15 | — |
| Delivery fee | ₹30 | ₹30 |
| Discount | −₹20 | — |
| **Amount to pay** | **₹270** | **₹240** |
| Delivery time | 30 min | 30 min |
| Restaurant rating shown | 4.3★ | 4.3★ |

Arithmetic: 230 + 15 + 15 + 30 − 20 = 270; 210 + 30 = 240 (difference ₹30).

| Version order | Bill 1 | Bill 2 |
|---|---|---|
| Order 1 | Usual app | New app |
| Order 2 | New app | Usual app |

Options: Bill 1 / Bill 2 (no indifference option: totals differ).

**Analysis:** share choosing the new app (Wilson CI), by segment. It serves as the baseline for bill_s4.

## 5. Scenario bill_s4 — lower total, but slower and a lower rating (H3 / H2)

**Stem:** as bill_s3, except: "The app you haven't used before shows a **longer delivery time** and a **slightly lower restaurant rating**."

| | **Your usual app** | **App you haven't used before** |
|---|---|---|
| Amount to pay (same line items as the previous example) | **₹270** | **₹240** |
| Delivery time | 30 min | **45 min** |
| Restaurant rating shown | 4.3★ | **4.1★** |

(Show the full line items identical to bill_s3, so the only changes are ETA and rating.)

| Version order | Bill 1 | Bill 2 |
|---|---|---|
| Order 1 | Usual app | New app |
| Order 2 | New app | Usual app |

**Analysis:**
- **Within-subject contrast s3 → s4:** McNemar test on `bill_s3_newapp_chosen` vs `bill_s4_newapp_chosen`. The drop in the new-app share (paired difference with CI) is the combined penalty of +15 min and −0.2★ against a ₹30 saving.
- Segment split (students vs professionals) is exploratory. The difference in paired drops uses a two-proportion comparison of switchers and is **directional only**.
- **Limitation:** ETA and rating change together. Separating them is the choice experiment's job (H3.1); the bill scenario gives an intuitive, respondent-friendly check that should **converge** with the choice-experiment ETA estimate.

## 6. Quality notes

- Keep the image row order identical across all 4 scenarios: food → packaging → platform → delivery → discount → amount → time → rating.
- Choice identity must not depend on layout: pilot respondents must correctly say which bill has the lower total (comprehension probe, pilot protocol §3).
- If the audit shows incumbent non-food charges well above or below ₹50–60 on a ₹210 dish, rescale packaging/platform/delivery lines **proportionally** and re-check that s1 and s2 totals remain identical.
