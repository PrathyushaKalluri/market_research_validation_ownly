# Competitor Audit — Calculations and Analysis Plan

**Version:** v1, 2026-09-14. Input: `audit_data.csv` (schema `audit_schema.csv`). All metrics below are **pre-registered**. Report every number with n (matched comparisons), the view (primary / coupon / subscription), date range and slots included.

---

## 1. Row-level derived fields

### Google Sheets (data in a sheet named `audit`, headers in row 1; column letters follow `audit_schema.csv` order)
Column map: R=menu_subtotal, S=offline_subtotal_verified, T=offline_price_source, U=packaging_fee, V=platform_fee, W=delivery_fee, X=small_cart_fee, Y=surge_rain_fee, Z=other_fees, AA=taxes_gst, AB=discount_amount, AC=discount_type, AD=subscription_saving_shown, AE=final_payable, AF=eta_min_shown, AG=eta_max_shown, H=account_state, I=subscription_active, L=restaurant_listed, M=restaurant_open, Q=item_match_quality.

| Derived column | Formula (row 2) |
|---|---|
| AN `fee_stack` | `=SUM(U2:Z2)` |
| AO `eta_mid_shown` | `=IF(AND(ISNUMBER(AF2),ISNUMBER(AG2)),(AF2+AG2)/2,"")` |
| AP `arith_gap` | `=IF(ISNUMBER(AE2),R2+AN2+N(AA2)-N(AB2)-AE2,"")` *(if the app lists subscription savings separately from discounts, subtract N(AD2) as well; document per platform)* |
| AQ `arithmetic_flag` | `=IF(AP2="","",IF(ABS(AP2)>2,1,0))` |
| AR `premium_vs_offline_rs` | `=IF(AND(ISNUMBER(S2),T2<>"unverified"),AE2-S2,"")` |
| AS `premium_vs_offline_pct` | `=IF(ISNUMBER(AR2),AR2/S2,"")` |
| AT `menu_markup_vs_offline_pct` | `=IF(AND(ISNUMBER(S2),T2<>"unverified"),(R2-S2)/S2,"")` |
| AU `fees_share_of_total` | `=IF(AE2>0,AN2/AE2,"")` |
| AV `primary_view` | `=AND(H2="existing",I2="n",OR(AC2="none",AC2="auto_offer",AC2="restaurant_offer"))` |
| AW `valid_row` | `=AND(L2="y",M2="y",Q2<>"none",AQ2=0)` |
| AX `match_key` | `=J2&"|"&O2&"|"&F2&"|"&D2&"|"&TEXT(B2,"yyyy-mm-dd")&"|"&H2&"|"&I2` *(add a session_id if two sessions happen in one slot on one day)* |

**Interpretation rule for offline comparisons:** `premium_vs_offline` is computed **only** where a verified offline price exists. Never label an unverified number an "offline price".

### pandas equivalent
```python
import pandas as pd, numpy as np
df = pd.read_csv("audit_data.csv", parse_dates=["capture_ts"])
fee_cols = ["packaging_fee","platform_fee","delivery_fee","small_cart_fee","surge_rain_fee","other_fees"]
df["fee_stack"] = df[fee_cols].fillna(0).sum(axis=1)
df["eta_mid_shown"] = (df.eta_min_shown + df.eta_max_shown) / 2
df["arith_gap"] = df.menu_subtotal + df.fee_stack + df.taxes_gst.fillna(0) - df.discount_amount.fillna(0) - df.final_payable
df["arithmetic_flag"] = (df.arith_gap.abs() > 2).astype(int)
verified = df.offline_price_source.ne("unverified") & df.offline_subtotal_verified.notna()
df.loc[verified, "premium_vs_offline_rs"]  = df.final_payable - df.offline_subtotal_verified
df.loc[verified, "premium_vs_offline_pct"] = df.premium_vs_offline_rs / df.offline_subtotal_verified
df["primary_view"] = (df.account_state.eq("existing") & df.subscription_active.eq("n")
                      & df.discount_type.isin(["none","auto_offer","restaurant_offer"]))
df["valid_row"] = (df.restaurant_listed.eq("y") & df.restaurant_open.eq("y")
                   & df.item_match_quality.ne("none") & df.arithmetic_flag.eq(0))
df["capture_date"] = df.capture_ts.dt.date
key = ["restaurant_id","basket_id","drop_point_id","slot","capture_date","account_state","subscription_active"]
```

---

## 2. Matched pairwise platform gap (headline metric for H2)
**Definition:** for each match key (the same restaurant × basket × drop point × slot × date/session × account state × subscription state), with both platforms valid and captures ≤10 minutes apart:
`gap_rs = final_payable(platform P) − final_payable(comparator C)`, and `gap_pct = gap_rs / final_payable(C)`.
Negative gap → P is cheaper. Primary pairs: **Ownly vs Swiggy**, **Ownly vs Zomato**, and **Ownly vs cheapest incumbent** (`min(Swiggy, Zomato)` at that key, requiring both valid).

```python
v = df[df.valid_row & df.primary_view]
wide = v.pivot_table(index=key, columns="platform",
                     values=["final_payable","capture_ts","eta_mid_shown","fee_stack","menu_subtotal"],
                     aggfunc="first")
def pair(wide, p, c):
    t = pd.DataFrame({
        "p_total": wide[("final_payable", p)], "c_total": wide[("final_payable", c)],
        "dt_min": (wide[("capture_ts", p)] - wide[("capture_ts", c)]).abs().dt.total_seconds()/60,
        "p_eta": wide[("eta_mid_shown", p)], "c_eta": wide[("eta_mid_shown", c)],
        "p_menu": wide[("menu_subtotal", p)], "c_menu": wide[("menu_subtotal", c)],
        "p_fees": wide[("fee_stack", p)], "c_fees": wide[("fee_stack", c)]}).dropna(subset=["p_total","c_total"])
    t = t[t.dt_min <= 10]
    t["gap_rs"] = t.p_total - t.c_total
    t["gap_pct"] = t.gap_rs / t.c_total
    t["eta_gap_min"] = t.p_eta - t.c_eta
    t["menu_gap_rs"] = t.p_menu - t.c_menu     # decomposition
    t["fee_gap_rs"] = t.p_fees - t.c_fees
    return t.reset_index()
ow_sw = pair(wide, "ownly", "swiggy"); ow_zo = pair(wide, "ownly", "zomato")
```

**Gap decomposition** (answers *where* savings come from): `gap_rs ≈ menu_gap_rs + fee_gap_rs + tax_gap − discount_gap`. Report the median of each component, which shows whether any advantage comes from menu prices, fees or discounts. Discount-driven advantages are fragile.

Google Sheets (paired sheet with one row per match key and columns `ownly_total`, `swiggy_total`): `gap_rs = ownly_total − swiggy_total`; median `=MEDIAN(FILTER(gap_rs, ISNUMBER(gap_rs)))`.

## 3. Median gap with bootstrap 95% CI
**Clustering caveat:** repeated captures of the same restaurant are not independent. Use a **cluster bootstrap by restaurant_id** (resample restaurants, keep all their comparisons).

```python
rng = np.random.default_rng(20260914)
def cluster_boot_median(t, col="gap_rs", cluster="restaurant_id", B=5000):
    groups = {k: g[col].values for k, g in t.groupby(cluster)}
    ids = list(groups); stats = []
    for _ in range(B):
        sample = rng.choice(ids, size=len(ids), replace=True)
        stats.append(np.median(np.concatenate([groups[i] for i in sample])))
    return np.median(t[col]), np.percentile(stats, [2.5, 97.5])
```
Report: `median gap = ₹X (95% CI ₹a to ₹b), n = __ matched comparisons across __ restaurants, __ sessions, [date range], primary view`.
Also report the mean and IQR, plus `gap_pct` in the same format.
Google Sheets approximation (no clustering): percentile CI is not native. Use the Python cell above, or an Apps Script bootstrap; in Sheets show `QUARTILE` values only.

## 4. Distribution
- Box plot (or strip + box) of `gap_rs` by comparator pair, split by basket type (B1/B2/B3). Show individual points (n is small).
- Histogram of `gap_pct` with a reference line at 0.
- Sheets: `=QUARTILE(range,0..4)` for the box elements.

## 5. Win rate
For each match key with ≥2 valid platforms: the **cheapest platform wins**. If the lowest two totals are within **₹5**, the key is a **tie** (both flagged tie).
```python
tot = v.pivot_table(index=key, columns="platform", values="final_payable", aggfunc="first")
def winner(row, tol=5):
    r = row.dropna().sort_values()
    if len(r) < 2: return None
    return "tie" if r.iloc[1] - r.iloc[0] <= tol else r.index[0]
tot["winner"] = tot.apply(winner, axis=1)
win_rate = tot.winner.value_counts(normalize=True)     # share of keys won by each platform / tie
```
Report the win rate for Ownly with a **Wilson 95% CI** (n = keys where Ownly was valid alongside ≥1 incumbent):
```python
from math import sqrt
def wilson(k, n, z=1.96):
    if n == 0: return (np.nan, np.nan)
    p = k/n; d = 1 + z*z/n; c = p + z*z/(2*n); m = z*sqrt(p*(1-p)/n + z*z/(4*n*n))
    return ((c-m)/d, (c+m)/d)
```
Sheets: win flag per key `=IF(SMALL(range,2)-SMALL(range,1)<=5,"tie",INDEX(headers,MATCH(MIN(range),range,0)))`; win rate `=COUNTIF(winner_col,"ownly")/COUNTA(winner_col)`.

## 6. Coverage
- **Listing coverage** = share of frame restaurants listed on a platform (per drop point): `listed_y / frame_n`.
- **Availability coverage** = share of frame restaurants **listed AND open** at capture, **by slot** (late-night matters).
- **Overlap coverage** = among restaurants on ≥1 incumbent, the share also on Ownly.
```python
cov = (df.groupby(["platform","drop_point_id","slot","restaurant_id"])
         .agg(listed=("restaurant_listed", lambda s: (s=="y").any()),
              open_=("restaurant_open",  lambda s: (s=="y").any()))
         .groupby(["platform","drop_point_id","slot"]).mean())
```
Always pair coverage with frame composition (tier/cuisine), because coverage of budget biryani ≠ coverage of premium. Report by `price_tier` and `cuisine` too (join the frame). Sheets: `=COUNTIFS(platform,"ownly",restaurant_listed,"y",slot,"late_night")/COUNTIFS(platform,"ownly",slot,"late_night")` (at restaurant level after de-duplication).

**Caveat:** the frame was built to include ~5 non-Ownly restaurants, so listing coverage is **frame-relative**, not a citywide share. Report it as "of the __ frame restaurants…".

## 7. ETA difference (shown/promised)
`eta_gap_min = eta_mid_shown(P) − eta_mid_shown(C)` for matched keys. Report the median with a cluster-bootstrap 95% CI, and by slot.
**Joint view:** scatter of `gap_rs` (x) vs `eta_gap_min` (y), one point per matched comparison. The quadrants show cheaper-and-slower, cheaper-and-faster, etc. This shows whether the price advantage is paired with an ETA penalty (H3).
**Implied ₹ per minute (descriptive only):** for comparisons where P is cheaper and slower, `saving_per_extra_min = −gap_rs / eta_gap_min`. Report the median and the share of comparisons. This describes the market offer, not user preference. User trade-off tolerance comes from the survey choice tasks.
Test orders (if any): `actual_delivery_min − eta_max_shown` per order, **listed individually, labelled anecdotal (n = __)**.

## 8. Consistency by slot / day
- Median `gap_rs` (and Ownly win rate) by `slot`, by weekday vs weekend, by drop point, by basket type. Show as a heatmap with cell n.
- **Consistency index (descriptive):** the share of restaurants where Ownly is cheaper (or tied) in **≥80%** of that restaurant's matched comparisons. Report n restaurants with ≥3 comparisons.
- Check whether the gap differs by slot using a **Kruskal–Wallis** test on `gap_rs` across slots (only if each slot has ≥10 comparisons). Otherwise present descriptively. Hypothesis-driven, not a fishing test.
- Flag sessions with rain/surge fees separately and show the results with and without them.

## 9. Fee-stack decomposition (View 9 chart data)
For each platform × basket type (primary view, valid rows): median menu_subtotal, packaging, platform, delivery, small-cart, surge, taxes, discount, final_payable. A stacked bar ("waterfall-like") per platform, showing n.
Also: **share of rows with each fee type > 0** per platform (e.g. "platform fee charged in __% of Swiggy captures").

## 10. Offline premium (only verified restaurants)
For restaurants with verified offline prices: median `premium_vs_offline_pct` per platform, with individual points shown (n will be small). The chart title must say "n = __ restaurants with verified offline menus". Also show `menu_markup_vs_offline_pct` separately, which distinguishes menu inflation from fees.

## 11. Sample-size guidance: what we can call the results
| Matched comparisons for a pair (and restaurants) | Label |
|---|---|
| ≥60 comparisons across ≥15 restaurants and ≥4 slots | **Reportable estimate** (still frame-specific; give CI) |
| 30–59 comparisons, or <15 restaurants, or <3 slots | **Directional**: report the median + CI, with "directional" in the chart note |
| <30 comparisons | **Illustrative only**: show the individual comparisons, no headline median claim |

Rationale: with a gap SD of ~₹25–40 (ASSUMPTION; update with pilot data), ~60 comparisons put the half-width of a 95% CI for the median at roughly ₹7–12, which is enough to distinguish a ₹20+ advantage from zero. Clustering by restaurant widens this, hence the restaurant minimum. Recompute after the pilot using the observed SD: `n ≈ (1.96 × 1.25 × SD / target_half_width)²` (the 1.25 factor approximates median inefficiency), then inflate by a design effect for clustering (`1 + (m−1)×ICC`, m = comparisons per restaurant).

**Business-significance threshold (pre-registered for interpretation):** a median saving is treated as **practically meaningful** only if the **lower CI bound ≥ ₹15 per single-person basket (B1)** or ≥ 7% of the comparator total, since smaller gaps are within typical coupon variation (ASSUMPTION; revisit against survey WTP/choice results and Agent A price anchors). A statistically non-zero gap below this is reported as "small".

## 12. How the audit feeds other workstreams
| Output | Destination |
|---|---|
| Median gap + CI, win rate, fee stack, coverage, ETA gap, consistency heatmap | **Dashboard View 9 (Market Reality)** + Executive Scorecard dimension "Economic/price attractiveness" (price advantage evidence) and "Experience/operational acceptability" (ETA gap, coverage) |
| Observed ranges (P10–P90) of final payable, delivery fee, platform/packaging fees and ETA for B1/B2 | **Survey calibration**: choice-experiment price/ETA levels, Gabor-Granger fee ladder check, bill-comparison scenarios. Scenarios remain labelled "scenario (calibrated to audit, dates __)", never presented as real bills. |
| Gap decomposition (menu vs fees vs discounts) | H2 interpretation. Messaging: whether "transparent fees" or "menu prices" is the actual lever. |
| Coverage by tier/cuisine/slot | H5/H10 and the assortment barrier on the scorecard, plus the Bengaluru → Hyderabad transfer slide (coverage claim vs Gachibowli observation) |
| Test-order anecdotes | Illustrative only. Triangulation matrix "audit evidence" column with confidence LOW. |
| Evidence matrix rows | `11_insights` triangulation matrix: audit column, with n, dates and view |

## 13. Output tables (file names)
`audit_pairs_ownly_vs_{swiggy|zomato|cheapest}.csv`, `audit_winrate.csv`, `audit_coverage.csv`, `audit_fee_stack.csv`, `audit_eta_gap.csv`, `audit_consistency_heatmap.csv`, `audit_offline_premium.csv`, `audit_calibration_memo.md`. Save them in `09_analysis/audit/` (the analysis owner decides the final location).
