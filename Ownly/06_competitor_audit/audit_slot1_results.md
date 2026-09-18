# Gachibowli Price Audit — Slot 1 Results (`wed_dinner`, 2026-09-16)

**Data:** `audit_data_slot1.csv` (78 rows, **37 priced**), captured by P3 at **DP1** (one fixed Gachibowli address),
19:45–22:00 on 2026-09-16. Published sheet mirrored into the repo on 2026-09-17.
**Status:** task 3.3 complete · task 3.9 partially complete (4 full three-app comparisons, plus coverage on all 10).
**Evidence label: FACT (observed by us).** Everything below is our own checkout observation, not a claim.

---

## 1. The headline: the answer flips on coupons

| View | Ownly cheapest | Median gap vs the cheapest incumbent | Range |
|---|---|---|---|
| **List price + fees, no offers** | **4 of 4** | **−30.5%** (Ownly cheaper) | −16.9% to −52.6% |
| **With each app's auto-applied offer** | 2 of 4 | **+13.9%** (Ownly dearer) | −44.9% to +246% |

Per restaurant (₹, final payable at checkout):

| Restaurant | View | Ownly | Swiggy | Zomato | Gap vs cheapest |
|---|---|---:|---:|---:|---:|
| Paradise Biryani | no offers | **313.95** | 471.76 | 484.76 | −157.81 (−33.5%) |
| Bawarchi | no offers | **205.80** | 249.35 | 247.64 | −41.84 (−16.9%) |
| Cream Stone | no offers | **187.95** | 277.80 | 259.14 | −71.19 (−27.5%) |
| Shah Ghouse | no offers | **157.50** | 332.00 | 332.49 | −174.50 (−52.6%) |
| Paradise Biryani | with offers | 263.95 | **187.76** | — | +76.19 (+40.6%) |
| Bawarchi | with offers | 155.80 | **45.00** | — | +110.80 (+246%) |
| Cream Stone | with offers | **137.95** | 158.00 | — | −20.05 (−12.7%) |
| Shah Ghouse | with offers | **107.50** | 195.00 | — | −87.50 (−44.9%) |

**Reading it.** Ownly's structural price advantage is real and large: on list price plus fees it won every
comparison, by a median of 30%. But incumbent coupons erase it. A ₹156 Swiggy coupon at Bawarchi turned a
₹205.80 Ownly order into a ₹45 Swiggy order. This is precisely the pattern the Bengaluru social corpus
predicted (18 posts: "coupons make Swiggy/Zomato equal or cheaper"), now observed first-hand in Gachibowli.

**What it means for the survey:** the decisive question is no longer "is Ownly cheaper?" but **"how often do
people actually order with a coupon?"** — survey `beh_offer_dependency` (Q13) and `beh_subscriptions` (Q12).
Offer-dependent users see the right-hand column; everyone else sees the left.

---

## 2. Where the saving comes from: menu price, not just fees

| Restaurant | Ownly menu | Incumbent menu | Menu gap |
|---|---:|---:|---:|
| Shah Ghouse | 150 | 254 | **−40.9%** |
| Paradise Biryani | 299 | 375 | **−20.3%** |
| Cream Stone | 179 | 189 | −5.3% |
| Bawarchi | 196 | 179 | **+9.5%** (Ownly dearer) |

Ownly's menu prices were lower on 3 of 4 restaurants, which supports the "restaurant's own prices, not marked
up" claim — **but not universally**: at Bawarchi the same veg biryani was ₹17 *more* on Ownly. The claim is
restaurant-dependent, exactly as the desk research warned.

## 3. Fee stack: the clearest structural difference

| Platform | Non-food share of the bill (median) | Delivery fee |
|---|---:|---|
| **Ownly** | **4.8%** (tax only) | **₹0 in 8 of 8 rows** |
| Zomato | 15.1% | median ₹21, up to ₹85 |
| Swiggy | 27.4% | median ₹42, up to ₹57 |

Ownly charged **no delivery fee, no platform fee and no packaging fee** in every captured row. Its only
addition was GST. On Swiggy, more than a quarter of the bill was non-food.

## 4. Speed is the trade-off

| Platform | Median ETA shown | Range |
|---|---:|---|
| Ownly | **39.5 min** | 30–46 |
| Swiggy | 22.5 min | 8–35 |
| Zomato | 17.5 min | 12–32 |

**Ownly is ~17 minutes slower than the incumbent median.** Survey Q16 asks exactly this trade (₹30 cheaper
vs 15 minutes slower), so the observed gap and the stated tolerance can be compared directly.

## 5. Coverage at DP1

- **9 of 10** frame restaurants were listed on Ownly.
- **Pizza Hut**: on Swiggy and Zomato, **not on Ownly** (national QSR gap, consistent with the Bengaluru KFC/McDonald's delisting).
- **Aanimuthyalu Unlimited**: on **Ownly only**, absent from both incumbents — a local place Ownly has that the incumbents don't.
- Ownly listed **221 restaurants** in total at DP1 (serviceability check, task 3.1).

---

## 6. Caveats (these belong on the slide)

1. **n = 4 complete three-app comparisons.** Directional, not a precise market estimate.
2. **Account states differ.** Ownly was a **new** account (a ₹50 first-order offer applied); Swiggy and Zomato
   were **existing** accounts **with memberships**. The "with offers" column therefore compares Ownly's
   acquisition offer against incumbent coupons and member benefits. Both views are reported for this reason.
3. **Ownly's ₹0 delivery fee may be a launch condition**, not a steady state. Bengaluru users report ₹15–₹30.
4. **Not captured:** Murgan Tiffins (listed and open, prices not captured before the app closed at midnight),
   Wendy's Burgers, and Aanimuthyalu (Ownly-only, so no comparison is possible).
5. **Karachi Bakery, Mehfil and Pizza Hut** have incumbent-only prices (Ownly closed for the night), so they
   contribute to coverage but not to the price comparison. Karachi Bakery's basket was a **₹1,200 cake**, which
   is not the single-portion B2 basket; exclude it from any basket-level average.
6. One row (Karachi Bakery, Zomato) is ₹2.75 off its line items — a rounding or a missed line; immaterial.

## 7. What would strengthen this, in order

1. **Murgan Tiffins and Mehfil on Ownly** (tomorrow's `thu_lunch` slot) — these are the under-₹150 local
   eateries Ownly *says* it targets, and right now every Ownly price we hold is a showcase chain.
2. **A second slot** to show whether the gap is stable or peak-dependent.
3. **The 3 test orders** (₹900) for promised-vs-actual delivery time, which is the only way to test whether
   the 40-minute ETA is honest.

## 7b. These results against the live KPI system (`09_analysis/kpi_system/`)

Recomputed using the **exact formulas** in `kpi_data_coverage.csv`, not my earlier working. Six KPIs that the
KPI system lists as "cannot be computed yet" are now computed from slot 1.

| KPI | Formula as defined | Slot-1 value | Priority |
|---|---|---|---|
| **K20** Median matched-basket saving % | median of (cheaper incumbent − Ownly) ÷ cheaper incumbent | **+30.5% no offers · −13.9% with offers** | P0 |
| **K21** Ownly win rate | Ownly cheapest by > ₹5, over matched sets | **4/4 no offers · 2/4 with offers** | P1 |
| **K22** Fee load % of final payable | (packaging + platform + delivery + small cart + surge) ÷ final payable | **Ownly 0.0% · Swiggy 3.3% · Zomato 12.7%** | P1 |
| **K40** Target-restaurant coverage on Ownly | frame restaurants listed on Ownly ÷ frame restaurants | **9/10 = 90%** | P0 |
| **K41** Local vs chain coverage gap | coverage(local) − coverage(chain) | **+20 pp** (local 3/3 = 100%, chain 4/5 = 80%) | P1 |
| **K42** Cross-platform availability overlap | usable on Ownly **and** ≥ 1 incumbent ÷ usable on ≥ 1 incumbent | **8/9 = 89%** | P1 |

**Note on K22.** This is the *fee-only* definition, so Ownly reads 0.0%: it charged no packaging, platform,
delivery, small-cart or surge fee in any captured row. The 4.8% figure in §3 is a different measure —
non-food share **including GST**. Both are true; the KPI system's definition is the one to quote as K22.

**Note on K20's sign.** The KPI system defines saving as positive when Ownly is cheaper, so the same data
that reads "−30.5% gap" in §1 reads "+30.5% saving" here. Same number, opposite convention.

**K26** (online/offline menu parity) stays uncomputed: the audit-lite schema has no verified offline-price
field. It needs a dated in-store menu photo, which is the cheapest remaining evidence to collect.

**K13** (fake-door CTA conversion by arm) stays uncomputed until the page has traffic.

**Two findings the KPI grid surfaces that §1 did not:**
- **K41 is positive**, meaning Ownly's coverage is *better* on local eateries (3/3) than on chains (4/5).
  That supports Service Q's localisation premise, though n = 10 restaurants.
- **K42's exceptions are the interesting rows**: Pizza Hut is on both incumbents but not on Ownly, and
  **Aanimuthyalu Unlimited is on Ownly and on neither incumbent** — a local place Ownly has exclusively.

## 8. Reproduce

```
python3 09_analysis/short_plan/analyze_audit_lite.py 06_competitor_audit/audit_data_slot1.csv --out 09_analysis/short_plan/audit_outputs
```
Published source sheet: `task_board.md` → shared links.
