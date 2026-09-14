# Market Price Anchors for Survey & Choice-Experiment Design

**Workstream:** Agent A · **Access date:** 2026-09-14 · Evidence IDs refer to `evidence_table.csv`.

> **Read this first.** No source gave us **Hyderabad-specific** incumbent fees, ETAs or AOVs. Almost every anchor below is **national** or a **single Bengaluru bill**. The recommended levels at the end are **design ASSUMPTIONS**. Before the survey goes live, re-confirm or replace them with numbers from the team's own Gachibowli competitor audit (06_competitor_audit).

---

## 1. Order-value (AOV / basket) anchors

| Anchor | Value | Geography | Label | Evidence |
|---|---|---|---|---|
| Ownly's Hyderabad price-page dishes (Ownly price) | ₹150–₹429 per dish | Hyderabad | COMPANY CLAIM | E26 |
| Same dishes, "other apps" price | ₹180–₹479 per dish | Hyderabad | COMPANY CLAIM | E26 |
| Budget single-item order used in a public price check | ₹119 item → ₹125 (Ownly), ~₹180 (Swiggy after ₹50 discount), ₹191.37 (Zomato) | Bengaluru | CONSUMER-GENERATED (n=1) | E29, E30 |
| Toing budget menus | Items "starting at ₹49"; meals "under ₹250" | National (Hyderabad not listed) | MEDIA REPORT | E46, E47 |
| Subscription free-delivery threshold | Orders above ₹199 | National | MEDIA REPORT (2024, stale) | E40 |
| Restaurant payout example | ₹400 dish with packaging → restaurant receives ~₹220 | Bengaluru | MEDIA REPORT (association figure) | E48 |
| **Platform AOV, age 20–30, Hyderabad** | **UNKNOWN** | — | — | — |

**Design implication (INTERPRETATION):** a realistic **single-person meal basket for this segment is roughly ₹150–₹300 in food value**. That covers a mini biryani from a well-known outlet up to a mid-range main. For Gachibowli, **biryani is the natural stimulus dish** (E57, E26). The survey's own "total bill of last order" question will replace this range with real data.

---

## 2. Incumbent customer fee anchors

| Fee line | Value | Geography | Label | Evidence | Confidence |
|---|---|---|---|---|---|
| Platform fee | ₹17.58 incl. GST (Swiggy); ₹14.90 + GST (Zomato) | National, from March 2026 | MEDIA REPORT | E33–E35 | High (as of Mar 2026; changes often) |
| Delivery fee (non-member) | "₹25–60 depending on distance and demand" | National | MEDIA REPORT (blog) | E41 | Low |
| Delivery partner fee on a real bill | ₹19 | Bengaluru, Mar 2026 | CONSUMER-GENERATED | E29 | Low (n=1) |
| Packaging fee on a real bill | ₹25 | Bengaluru, Mar 2026 | CONSUMER-GENERATED | E29 | Low (n=1) |
| GST on delivery charges | 18% (since 2025-09-22) | National | MEDIA REPORT (policy) | E36 | High |
| GST on food | ₹5.95 on ₹119 = 5.0% on the Ownly bill (arithmetic from the bill) | Bengaluru | CONSUMER-GENERATED | E29 | Medium |
| Rain surcharge | "₹15–35", now also charged to subscribers | National | MEDIA REPORT | E38 (policy), E39 (amount, unverified) | Low for amount |
| Donation add-on | ₹3 | Bengaluru (Zomato) | CONSUMER-GENERATED | E29 | Low |
| **Total non-food charges on one Zomato order** | **₹72.37** on a ₹119 item (₹191.37 − ₹119) | Bengaluru | CONSUMER-GENERATED | E29 | Low (n=1) but concrete |
| Small-cart / long-distance fees | **UNKNOWN** | — | — | — | — |
| **Any of the above specifically in Hyderabad** | **UNKNOWN** | — | — | — | — |

## 3. Subscription anchors

| Plan | Value | Label | Evidence | Status |
|---|---|---|---|---|
| Zomato Gold | ₹99/month; free delivery on orders >₹199 within 7 km | MEDIA REPORT | E40 | **Stale (June 2024)**; 2026 blogs quote ₹999/yr, conflicting |
| Swiggy One | ₹99/month; orders >₹199 within 7 km | MEDIA REPORT | E40 | **Stale**; 2026 blogs quote ₹1,299/3 months and "One Lite" ₹99/3 months, conflicting |
| Rain surcharge for subscribers | Exemption withdrawn May 2025 | MEDIA REPORT | E38 | Current |

→ **Capture current prices and terms in-app on audit day. Don't show any subscription price to respondents from this table.**

## 4. Ownly anchors

| Item | Value | Label | Evidence |
|---|---|---|---|
| Hyderabad platform / packaging / surge fee | ₹0 (claimed) | COMPANY CLAIM | E23 |
| **Hyderabad delivery fee** | **Not published — UNKNOWN** | — | E22, E23 |
| Bengaluru delivery fee | "around ₹30, along with GST" | MEDIA REPORT, **contradicted** | E13 |
| Contradicting signals | App Store says "Free delivery"; ₹0 delivery on a launch-week bill; "distance-based" (vendor blog) | COMPANY / CONSUMER / MEDIA | E28, E29, E31 |
| ETA | "25-minute ETA" mentioned in a review summary; no official commitment | CONSUMER-GENERATED, unverified | E65 |
| Incumbent fast-delivery benchmark | Swiggy Bolt (~10 min); Hyderabad 2nd-highest Bolt orders in 2025 | COMPANY CLAIM (Swiggy) | E58 |
| Incumbent standard ETAs in Gachibowli | **UNKNOWN** | — | — |

---

## 5. RECOMMENDED design values (ASSUMPTIONS, to confirm with the audit)

### 5.1 Gabor-Granger delivery-fee ladder (H8)

**Recommended price points:** **₹0 · ₹10 · ₹20 · ₹30 · ₹40 · ₹50 · ₹60** (7 points, ₹10 steps).

**Rationale**
- **₹30** is the most-reported Ownly Bengaluru fee [E13], so it sits in the middle of the ladder and the acceptance curve can be read on both sides of Ownly's likely price.
- **₹20** sits just above the incumbent platform fee alone (₹17.58) [E33]. **₹10–20** covers the "token fee" range.
- **₹50–60** spans the low-confidence ₹25–60 incumbent delivery range [E41] and the upper part of the ₹72 total non-food stack seen on one bill [E29]. Going above ₹60 for a single-person ₹150–300 basket would push fee-to-food ratios above 20–40%. **INTERPRETATION:** that is unlikely to be informative for this segment.
- **₹0** is needed as the reference point, and because "free delivery" messaging exists [E28].

**Method rules**
1. **Define the fee precisely in the question:** *"a single delivery charge that is the only amount added to the menu price (taxes shown separately)."* Otherwise respondents mentally add platform and packaging fees and the answers mix different things.
2. **Fix the basket context** (e.g., "a ₹220 dinner for one") so the fee is judged relative to a stated food value. Consider a split-sample second context (₹450 order for two) to test fee-to-basket sensitivity.
3. **Randomise the starting price** (start at ₹20, ₹30 or ₹40), then go up after "yes" and down after "no." This reduces anchoring on the first price. Record the start point as a variable.
4. Ask "Would you place this order at this delivery charge?" with a binary answer. Use **acceptance share per price point** to build the demand curve. **Median acceptable fee** = highest price where ≥50% still accept. **Arc elasticity** between adjacent points = %Δacceptance / %Δprice (don't compute it from ₹0).
5. **Confirm the ladder with the audit.** If the observed Ownly Gachibowli fee is ₹0 or ₹40+, re-centre the ladder on it before fielding.

### 5.2 Choice-experiment attribute levels (H3, H4, H5)

**Stimulus basket (ASSUMPTION):** a single-person Hyderabadi biryani dinner, **food value ₹210** (inside the ₹150–300 range [E26]). Use the same basket in every task.

| Attribute | Recommended levels | Rationale / source | Confidence |
|---|---|---|---|
| **Total checkout price** (all fees + taxes, shown as one number, with an optional expandable breakdown) | **₹235 · ₹260 · ₹285 · ₹310** | ₹235 ≈ food + ~₹25 (low-fee structure, like Ownly's reported ₹30 [E13]); ₹285 ≈ food + ~₹75, close to the ₹72 non-food stack on one incumbent bill [E29]. ₹25 steps make "₹25 saved ↔ Y minutes" statements easy | Medium (structure) / Low (Hyderabad values) |
| **ETA (quoted)** | **25 · 35 · 45 · 55 min** | 25 min = reported Ownly ETA mention [E65]; 45 min matches the brief's example; 55 min tests the tolerance limit. Bolt-style ~10 min NOT included (it's a separate product) | Low — **replace with audited quoted ETAs** |
| **Delivery reliability** | "Usually on time: **9 in 10** orders" · "**7 in 10** orders" | ASSUMPTION. No public on-time rates found. Frequency format ("x in 10") is easier to understand than percentages | Assumption |
| **Restaurant selection** | "**Most** of the restaurants you usually order from" · "**About half**" · "**Only a few** — mostly local places" | ASSUMPTION, tied to H5/H10. Qualitative levels because restaurant counts mean little to respondents | Assumption |
| **Refund / support assurance** | "Automatic refund within **24 hours** if order is missing/wrong" · "Refund after contacting **chat support**, no time commitment" | ASSUMPTION, tied to H4. Review evidence suggests refund delays are a real pain [E28] | Assumption |

**Design guidance**
- **Size:** 5–8 paired tasks (A vs B, plus an optional "neither/I'd cook or go out" opt-out), **brand-blind** ("Platform A / Platform B").
- **Constraints:** avoid dominated pairs (cheaper AND faster AND more reliable). Include 2 "pure trade-off" tasks that vary only price and ETA (H3), one that varies only price and reliability (H4), and one that varies only price and selection (H5), so each can be read directly even if the full model is under-powered.
- **Implausible combinations to exclude (ASSUMPTION):** ₹235 + 25 min + 9/10 reliability + "most restaurants" + 24h refund. That profile looks like an impossible platform and will dominate every choice.
- **Randomise** task order and left/right position; record the version shown.
- **Analysis:** conditional logit (or simple logit on the paired choice) with price as a linear term. Implied **minutes per ₹** = β_ETA / β_price. Report by segment (student vs professional) with confidence intervals. Only make a claim if the interval excludes zero.

### 5.3 Bill-comparison experiment (synthetic scenarios, must be labelled as such)

Use the **line-item structure** of the documented Bengaluru bill [E29] (item / packaging / platform / delivery / donation / taxes / discount / total) but **Hyderabad-plausible values from the audit**. Label every stimulus: *"Illustrative scenario created for research — not an actual bill from any platform."* Never present the E29 numbers as a Hyderabad bill.

---

## 6. Must be re-confirmed by the live Gachibowli competitor audit

1. Ownly's actual delivery fee (and whether it varies by distance, time, basket or promo).
2. Whether Ownly serves the team's audit addresses in Gachibowli, and how many restaurants are available.
3. Swiggy and Zomato platform fee as displayed in Hyderabad at audit time.
4. Incumbent delivery fee, packaging fee, small-cart and long-distance fees for the audit baskets.
5. Quoted ETAs on each platform at lunch, dinner and a weekend slot.
6. Current Swiggy One / Zomato Gold price, free-delivery threshold and radius.
7. Whether Swiggy Toing (and Flipkart food) is available in Gachibowli.
8. Prices of the 12 dishes Ownly shows on its Hyderabad page [E26], on every platform, at the same outlets.
9. Verified offline menu prices, only from an in-store menu or receipt photo.
10. GST treatment shown on each checkout.
