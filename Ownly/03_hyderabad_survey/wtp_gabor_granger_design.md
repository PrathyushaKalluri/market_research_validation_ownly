# Delivery-Fee Willingness to Pay: Gabor-Granger Ladder (H8, H6.2)

**Version:** 2026-09-14. The fee points are **PROVISIONAL** until the Gachibowli audit (`01_secondary_research/market_price_anchors.md` §5.1). If the audit shows Ownly's actual delivery fee is ₹0 or ≥ ₹40, re-centre the ladder before fielding and log a deviation.

## 1. Why this design

| Option considered | Verdict |
|---|---|
| Van Westendorp price-sensitivity meter | Not used. It asks for price *perceptions* ("too cheap", "too expensive") on an open scale. A delivery fee is a small add-on judged against a basket, and the method gives no acceptance curve for specific fee points. Not justified here. |
| Pure descending ladder (start high, go down) | Anchors respondents on the first high price and inflates acceptance of lower fees. |
| Split-sample monadic (each person sees one fee) | Cleanest, but needs about 7 × 30+ respondents per point per segment. Not feasible at n ≈ 220. |
| **Randomised-start adaptive ladder (chosen)** | Each respondent answers 2–5 binary questions. The start is ₹20 or ₹40, balanced by form version: V1/V4/B1 = ₹20, V2/V3/B2 = ₹40. The ladder moves up after "yes" and down after "no", and stops at the first change of answer. The anchoring direction differs between the two starts, so the pooled curve averages opposite anchoring biases, and the start effect is estimated explicitly. It works in Google Forms via "Go to section based on answer". |

## 2. Framing screen (shown once, before the first fee section)

> **Imagine a food-delivery service that works like this:**
> - Food is charged at the restaurant's own menu prices.
> - There are no platform charges and no packaging charges.
> - The **only** amount added to your food is **one delivery charge**, shown to you before you order.
> - All amounts include taxes.
>
> Think about a dinner for one that you would normally order, where **the food costs ₹220**.
> On the next screens we'll show different delivery charges. For each one, tell us whether you would place this order through **this service**.

Rules:
- Always say "this service", in every version. Never name a brand in the ladder, not even in branded versions (V3/V4 have already seen the brand in the concept section; the arm is a covariate).
- Do not mention any other app's fees, Ownly's fee, or savings.

## 3. Section graphs (one section per fee point; each section has one required question)

**Question text in every section:** "For this ₹220 dinner, the delivery charge is **₹[FEE]**. Would you place this order through this service?"
**Options:** "Yes, I would order" (code 1) · "No, not at this delivery charge" (code 0)
**Variable:** `wtp_accept_[FEE]`. The start fee goes into `wtp_start`, which is a constant per version and is added in cleaning from `meta_form_version`.

### Graph A — start ₹20 (V1, V4, B1)

```
[Framing] → [₹20]
[₹20]  Yes → [₹30]        No → [₹10]
[₹30]  Yes → [₹40]        No → END
[₹40]  Yes → [₹50]        No → END
[₹50]  Yes → [₹60]        No → END
[₹60]  Yes → END          No → END
[₹10]  Yes → END          No → [₹0]
[₹0]   Yes → END          No → END
END = the section after the ladder (next survey module)
```

### Graph B — start ₹40 (V2, V3, B2)

```
[Framing] → [₹40]
[₹40]  Yes → [₹50]        No → [₹30]
[₹50]  Yes → [₹60]        No → END
[₹60]  Yes → END          No → END
[₹30]  Yes → END          No → [₹20]
[₹20]  Yes → END          No → [₹10]
[₹10]  Yes → END          No → [₹0]
[₹0]   Yes → END          No → END
```

**Implementation note:** a section's "After section" routing must point to END for sections that are only reached terminally. Because routing is set per question option, set both options explicitly in every section. QA must walk every path (§6).

## 4. Derived variables

| Variable | Rule |
|---|---|
| `wtp_max_fee` | The highest fee answered "Yes" on the respondent's path. Examples: start ₹20 with Yes at ₹20 and No at ₹30 → **20**. Start ₹40 with No at ₹40 and Yes at ₹30 → **30**. |
| `wtp_censored_top` | 1 if "Yes" at ₹60 (true maximum ≥ ₹60; right-censored) |
| `wtp_rejects_all` | 1 if "No" at ₹0. The respondent would not order this dinner through this service **even with free delivery**, so the reason is not the fee. `wtp_max_fee` = NA; reported as a separate share, never coded as ₹0. |
| Imputed acceptance per fee point `acc_f` | 1 if `wtp_max_fee` ≥ f, else 0 (monotonicity assumption; standard for Gabor-Granger). `wtp_rejects_all` respondents are 0 at every point and are shown in a sensitivity curve with and without them. |

**Non-monotone answers.** The stop-at-first-change rule makes non-monotone paths impossible by construction. They can only appear from Google Forms *Back*-button edits that leave orphan answers in skipped sections. Cleaning rule: reconstruct the path from `wtp_start` using the routing graph and keep only the answers on that path. If the path is inconsistent (e.g. "Yes" at ₹50 but "No" at ₹40 both on-path), set `wtp_max_fee` = NA and flag `FLAG_wtp_nonmonotone`. The count of such rows is reported.

## 5. Analysis (per `09_analysis/M_pre_analysis_plan.md` §6.2)

1. **Acceptance curve:** share with `acc_f = 1` at f ∈ {0, 10, 20, 30, 40, 50, 60}, with Wilson 95% CIs. Pooled; by `seg_occupation`; by brand arm (V1+V2 vs V3+V4); by `wtp_start`.
2. **Start (anchoring) effect:** logistic regression `acc ~ fee + start40 + fee×start40` on the long table (`fact_wtp_long`, respondent × fee point), with respondent-clustered SEs. If the start effect is material (≥ 10 pp at any point), report the start-specific curves alongside the pooled curve. The pooled curve remains primary because the design is balanced.
3. **Median acceptable fee:** the fee at which pooled acceptance crosses 50%, by linear interpolation between the two adjacent points: `f* = f1 + (0.5 − a1)·(f2 − f1)/(a2 − a1)`. Bootstrap percentile CI (10,000 resamples of respondents, seed 20260914). Also report the **highest fee point with acceptance ≥ 50%** (the discrete version).
4. **H8.1:** Wilson CI on acceptance at the fee point closest to the audit-observed Ownly Gachibowli fee vs the 50% threshold.
5. **Arc elasticity** between adjacent points, excluding ₹0 (undefined percentage change):
   `E = ((a2 − a1)/((a1 + a2)/2)) / ((f2 − f1)/((f1 + f2)/2))`, with a bootstrap CI. The largest |E| identifies the kink (H8.2).
6. **Segment comparison (H6.2):**
   - Mann-Whitney on `wtp_max_fee`. Censored values at ₹60 are treated as 60, and the censored share per segment is reported.
   - Logistic `acc ~ fee × segment + start40 + arm`, clustered.
7. **Illustrative revenue-proxy curve** `fee × acceptance`. Clearly labelled **not a pricing recommendation**: it ignores basket size, order frequency, costs and competitor response.

## 6. QA paths to test in every version

- Start ₹20: YYYYY (ends at ₹60, censored) · YN (max 20) · NY (max 10) · NNN (rejects all)
- Start ₹40: YYY (censored) · YN (max 50) · NY (max 30) · NNNNN (rejects all)
- Check in the sheet that skipped fee columns are blank.
