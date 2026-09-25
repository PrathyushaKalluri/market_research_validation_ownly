"""
02_audit.py — Gachibowli competitor price audit (PRIMARY OBSERVED DATA, 2026-09-16, DP1)

THREE price views, kept strictly separate. This matters: the answer to "is Ownly cheaper?"
flips between them, and 82.6% of our Hyderabad sample holds an incumbent membership.

  1 LIST+FEES    non-member, no coupon      -> the STRUCTURAL price position
  2 MEMBER       membership benefit applied -> what a Swiggy One / Zomato Gold holder sees
  3 AFTER OFFER  coupons/auto offers applied-> the ACTUAL WALLET price

DOCUMENTED CLEANING RULE (audit_dedup_rule):
Every Zomato LIST+FEES capture in this slot exists TWICE - once with delivery_fee = 0
(Gold free delivery) and once with the delivery fee charged. These are not duplicates;
they are the member and non-member prices of the same basket. Therefore, within
discount_type == 'none': MAX(final_payable) = LIST+FEES (view 1)
                         MIN(final_payable) = MEMBER    (view 2)
Where only one 'none' capture exists, it serves both views.
Ownly was a NEW account (no membership exists on Ownly), so Ownly's view 1 == view 2.
"""
import os
import numpy as np
import pandas as pd

ROOT = "/Users/klprathyusha/Sem 3/Project/Ownly"
OUT = f"{ROOT}/final_dashboard/data"
os.makedirs(OUT, exist_ok=True)

a = pd.read_csv(f"{ROOT}/06_competitor_audit/audit_data_slot1.csv")

num = ["menu_subtotal", "packaging_fee", "platform_fee", "delivery_fee", "small_cart_fee",
       "surge_rain_fee", "taxes_gst", "discount_amount", "final_payable",
       "eta_min_shown", "eta_max_shown"]
for c in num:
    a[c] = pd.to_numeric(a[c], errors="coerce")

# name normalisation - 'Aanimuthyalu' / 'Aanimuthyualu' are one restaurant (typo in capture)
a["restaurant_name"] = (a["restaurant_name"].str.strip()
                        .replace({"Aanimuthyualu unlimited": "Aanimuthyalu unlimited"}))

a["eta_mid"] = (a["eta_min_shown"] + a["eta_max_shown"]) / 2
a["fees_total"] = a[["packaging_fee", "platform_fee", "delivery_fee",
                     "small_cart_fee", "surge_rain_fee"]].sum(axis=1, min_count=1)
a["non_food_total"] = a["fees_total"] + a["taxes_gst"]
a["non_food_share"] = a["non_food_total"] / a["final_payable"]
a["priced"] = a["final_payable"].notna()
a["recon_delta"] = ((a["menu_subtotal"].fillna(0) + a["fees_total"].fillna(0)
                     + a["taxes_gst"].fillna(0) - a["discount_amount"].fillna(0))
                    - a["final_payable"]).round(2)
a["recon_flag"] = np.where(a["priced"] & (a["recon_delta"].abs() > 1.0),
                           "line items do not reconcile to final_payable", "")
a.to_csv(f"{OUT}/audit_clean.csv", index=False)

# ------------------------------------------------- platform price per view
priced = a[a["priced"]].copy()
recs = []
for (rest, basket, plat), g in priced.groupby(["restaurant_name", "basket_id", "platform"]):
    none_g = g[g["discount_type"].eq("none")]
    off_g = g[~g["discount_type"].eq("none")]
    rec = {"restaurant_name": rest, "basket_id": basket, "platform": plat,
           "eta_mid": g["eta_mid"].mean()}
    if len(none_g):
        rec["LIST+FEES"] = none_g["final_payable"].max()
        rec["MEMBER"] = none_g["final_payable"].min()
    if len(off_g):
        rec["AFTER OFFER"] = off_g["final_payable"].min()
    elif len(none_g):                       # no coupon seen -> wallet price = member price
        rec["AFTER OFFER"] = none_g["final_payable"].min()
    recs.append(rec)
PP = pd.DataFrame(recs)
PP.to_csv(f"{OUT}/audit_platform_prices.csv", index=False)

# ----------------------------------------------------------- matched pairs
VIEWS = ["LIST+FEES", "MEMBER", "AFTER OFFER"]
pairs = []
for (rest, basket), g in PP.groupby(["restaurant_name", "basket_id"]):
    if "ownly" not in set(g["platform"]):
        continue
    own_row = g[g["platform"].eq("ownly")].iloc[0]
    inc = g[~g["platform"].eq("ownly")]
    if inc.empty:
        continue
    for v in VIEWS:
        if v not in g.columns:
            continue
        own = own_row.get(v, np.nan)
        iv = inc[["platform", v]].dropna()
        if pd.isna(own) or iv.empty:
            continue
        best = iv.loc[iv[v].idxmin()]
        pairs.append({
            "restaurant_name": rest, "basket_id": basket, "view": v,
            "ownly_payable": own, "cheapest_incumbent": best["platform"],
            "incumbent_payable": best[v],
            "saving_rs": best[v] - own,
            "saving_pct": (best[v] - own) / best[v] * 100,
            "ownly_wins": bool(own < best[v] - 5),
            "ownly_eta_mid": own_row["eta_mid"],
            "incumbent_eta_mid": inc["eta_mid"].min(),
        })

P = pd.DataFrame(pairs)
P["view"] = pd.Categorical(P["view"], VIEWS, ordered=True)
P = P.sort_values(["view", "restaurant_name"])
P.to_csv(f"{OUT}/audit_pairs.csv", index=False)

# ------------------------------------------------------------------ report
print("AUDIT ROWS:", len(a), "| priced:", int(a["priced"].sum()),
      "| recon flags:", int((a["recon_flag"] != "").sum()))
print("\nNon-food share of final payable, median % (priced rows):")
print(priced.groupby("platform")["non_food_share"].median().mul(100).round(1).to_string())
print("\nQuoted ETA midpoint, median minutes:")
print(a.groupby("platform")["eta_mid"].median().to_string())
for v in VIEWS:
    g = P[P["view"].eq(v)]
    if not len(g):
        continue
    print(f"\n=== {v} ===  n={len(g)} matched baskets | Ownly cheapest {int(g.ownly_wins.sum())}/{len(g)}")
    print(f"    median saving ₹{g.saving_rs.median():.2f}  ({g.saving_pct.median():.1f}%)")
    print(g[["restaurant_name", "ownly_payable", "cheapest_incumbent",
             "incumbent_payable", "saving_rs", "saving_pct", "ownly_wins"]]
          .round(2).to_string(index=False))

cov = (a.drop_duplicates(["restaurant_name", "platform"])
       .pivot_table(index="restaurant_name", columns="platform",
                    values="restaurant_listed", aggfunc="first"))
cov.to_csv(f"{OUT}/audit_coverage.csv")
print("\nCOVERAGE (y = listed at DP1):")
print(cov.fillna("-").to_string())
