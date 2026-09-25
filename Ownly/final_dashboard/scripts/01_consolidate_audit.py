"""
01_consolidate_audit.py — AUTHORITATIVE price/coverage audit
Source: 06_competitor_audit/task 3.3.xlsx  (supersedes audit_data_slot1.csv)

Three cleaning rules, all documented, none silent:

R1  CASE NORMALISATION. The workbook mixes 'Zomato'/'zomato', 'Y'/'y', 'N'/'n',
    'Auto offer'/'auto offer'. Left as-is these fork into separate platforms,
    listing states and price views. Everything is lower-cased before grouping.

R2  NAME NORMALISATION. 'Aanimuthyualu unlimited' is a typo for
    'Aanimuthyalu unlimited'. Merged.

R3  LISTED vs OPEN ARE DIFFERENT THINGS. A restaurant absent from a platform is
    not the same as one listed but shut at that hour. Closure is reported separately.

R4  THE thu_lunch PASS IS EXCLUDED FROM COVERAGE. All 30 of its rows record
    restaurant_listed = 'y' with no variation, no restaurant_open value, no
    timestamp and no prices. A coverage pass in which every cell is 'y' carries no
    information and is consistent with default-filling rather than observation.
    It is retained in audit_clean.csv, flagged, and excluded from coverage counts.
    Cross-check: a first-hand Ownly user in Gachibowli (2026-09-19) confirms
    Aanimuthyalu Unlimited IS Ownly-only, which matches the wed_dinner pass and
    contradicts thu_lunch.

Price views (as before): LIST+FEES (non-member) / MEMBER (benefit, no coupon) /
AFTER OFFER (coupon applied). Within discount_type == 'none', MAX = non-member and
MIN = member, because incumbent list captures were taken twice.
"""
import os
import numpy as np
import pandas as pd

ROOT = "/Users/klprathyusha/Sem 3/Project/Ownly"
SRC = f"{ROOT}/06_competitor_audit/task 3.3.xlsx"
OUT = f"{ROOT}/final_dashboard/data"
os.makedirs(OUT, exist_ok=True)

a = pd.read_excel(SRC)

# R1 — case normalisation
for c in ["platform", "restaurant_listed", "restaurant_open", "discount_type",
          "restaurant_name", "slot", "drop_point_id", "account_state",
          "subscription_active", "item_match_quality", "notes"]:
    if c in a.columns:
        a[c] = a[c].astype(str).str.strip().str.lower().replace({"nan": np.nan})

# R2 — name normalisation
a["restaurant_name"] = a["restaurant_name"].replace(
    {"aanimuthyualu unlimited": "aanimuthyalu unlimited"})
a["restaurant_display"] = a["restaurant_name"].str.title().str.replace("'S", "'s", regex=False)

NUM = ["menu_subtotal", "packaging_fee", "platform_fee", "delivery_fee", "small_cart_fee",
       "surge_rain_fee", "taxes_gst", "discount_amount", "final_payable",
       "eta_min_shown", "eta_max_shown"]
for c in NUM:
    a[c] = pd.to_numeric(a[c], errors="coerce")

a["eta_mid"] = (a["eta_min_shown"] + a["eta_max_shown"]) / 2
a["fees_total"] = a[["packaging_fee", "platform_fee", "delivery_fee",
                     "small_cart_fee", "surge_rain_fee"]].sum(axis=1, min_count=1)
a["non_food_total"] = a["fees_total"] + a["taxes_gst"]
a["non_food_share"] = a["non_food_total"] / a["final_payable"]
a["priced"] = a["final_payable"].notna()
a["is_listed"] = a["restaurant_listed"].eq("y")
a["is_open"] = a["restaurant_open"].eq("y")
a["recon_delta"] = ((a["menu_subtotal"].fillna(0) + a["fees_total"].fillna(0)
                     + a["taxes_gst"].fillna(0) - a["discount_amount"].fillna(0))
                    - a["final_payable"]).round(2)
a["recon_flag"] = np.where(a["priced"] & (a["recon_delta"].abs() > 1.0),
                           "line items do not reconcile", "")
a.to_csv(f"{OUT}/audit_clean.csv", index=False)

# ----------------------------------------- R4: flag and exclude the thu_lunch pass
slot_q = (a.groupby("slot")
          .agg(rows=("is_listed", "size"), listed_y=("is_listed", "sum"),
               open_recorded=("restaurant_open", lambda s: int(s.notna().sum())),
               priced=("priced", "sum"))
          .reset_index())
slot_q["all_listed_y"] = slot_q["listed_y"] == slot_q["rows"]
slot_q["usable_for_coverage"] = ~(slot_q["all_listed_y"] & slot_q["open_recorded"].eq(0))
slot_q.to_csv(f"{OUT}/audit_slot_quality.csv", index=False)
USABLE = set(slot_q.loc[slot_q["usable_for_coverage"], "slot"])
a["slot_usable_for_coverage"] = a["slot"].isin(USABLE)

cov_src = a[a["slot_usable_for_coverage"]]

# ------------------------------------------------- coverage (usable slots only)
cov = (cov_src.groupby(["restaurant_display", "platform"])
       .agg(listed_any=("is_listed", "max"),
            open_any=("is_open", "max"),
            slots=("slot", "nunique"))
       .reset_index())
piv = cov.pivot(index="restaurant_display", columns="platform", values="listed_any").fillna(False)
piv["on_incumbent"] = piv.get("swiggy", False) | piv.get("zomato", False)
piv["on_ownly"] = piv.get("ownly", False)
piv["status"] = np.select(
    [piv["on_ownly"] & ~piv["on_incumbent"],
     ~piv["on_ownly"] & piv["on_incumbent"],
     piv["on_ownly"] & piv["on_incumbent"]],
    ["Ownly only", "Missing from Ownly", "On Ownly and incumbents"], default="Neither")
piv.reset_index().to_csv(f"{OUT}/audit_coverage.csv", index=False)

n_frame = len(piv)
n_own = int(piv["on_ownly"].sum())
n_inc = int(piv["on_incumbent"].sum())
n_both = int((piv["on_ownly"] & piv["on_incumbent"]).sum())
n_own_only = int((piv["on_ownly"] & ~piv["on_incumbent"]).sum())
n_inc_only = int((~piv["on_ownly"] & piv["on_incumbent"]).sum())

# closure (distinct from coverage)
closed = cov_src[cov_src["is_listed"] & ~cov_src["is_open"] & cov_src["restaurant_open"].notna()]
closed_summary = (closed.groupby(["restaurant_display", "platform", "slot"]).size()
                  .reset_index(name="n"))
closed_summary.to_csv(f"{OUT}/audit_closures.csv", index=False)

# ------------------------------------------------- price views + matched pairs
priced = a[a["priced"]].copy()
recs = []
for (rest, basket, plat, slot), g in priced.groupby(
        ["restaurant_display", "basket_id", "platform", "slot"]):
    none_g = g[g["discount_type"].eq("none")]
    off_g = g[g["discount_type"].notna() & ~g["discount_type"].eq("none")]
    rec = {"restaurant_display": rest, "basket_id": basket, "platform": plat, "slot": slot,
           "eta_mid": g["eta_mid"].mean()}
    if len(none_g):
        rec["LIST+FEES"] = none_g["final_payable"].max()
        rec["MEMBER"] = none_g["final_payable"].min()
    if len(off_g):
        rec["AFTER OFFER"] = off_g["final_payable"].min()
    elif len(none_g):
        rec["AFTER OFFER"] = none_g["final_payable"].min()
    recs.append(rec)
PP = pd.DataFrame(recs)
PP.to_csv(f"{OUT}/audit_platform_prices.csv", index=False)

VIEWS = ["LIST+FEES", "MEMBER", "AFTER OFFER"]
pairs = []
for (rest, basket, slot), g in PP.groupby(["restaurant_display", "basket_id", "slot"]):
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
            "restaurant_display": rest, "basket_id": basket, "slot": slot, "view": v,
            "ownly_payable": own, "cheapest_incumbent": best["platform"],
            "incumbent_payable": best[v],
            "saving_rs": best[v] - own,
            "saving_pct": (best[v] - own) / best[v] * 100,
            "ownly_wins": bool(own < best[v] - 5),
            "ownly_eta_mid": own_row["eta_mid"], "incumbent_eta_mid": inc["eta_mid"].min(),
        })
P = pd.DataFrame(pairs)
P["view"] = pd.Categorical(P["view"], VIEWS, ordered=True)
P = P.sort_values(["view", "restaurant_display"])
P.to_csv(f"{OUT}/audit_pairs.csv", index=False)

# ------------------------------------------------------------------- report
print(f"AUDIT rows {len(a)} | priced {int(a['priced'].sum())} | recon flags "
      f"{int((a['recon_flag']!='').sum())}")
print(f"slots: {sorted(a['slot'].dropna().unique())} | drop points: "
      f"{sorted(a['drop_point_id'].dropna().unique())}")
print("\nPriced captures by slot x platform:")
print(pd.crosstab(priced["slot"], priced["platform"], margins=True).to_string())

print("\nSLOT QUALITY:"); print(slot_q.to_string(index=False))
print(f"\nCOVERAGE (usable slots only: {sorted(USABLE)}), frame = {n_frame} restaurants")
print(f"  on Ownly            {n_own}/{n_frame} = {n_own/n_frame*100:.1f}%")
print(f"  on >=1 incumbent    {n_inc}/{n_frame} = {n_inc/n_frame*100:.1f}%")
print(f"  on BOTH (overlap)   {n_both}/{n_own} of Ownly's list = {n_both/n_own*100:.1f}%")
print(f"  Ownly only          {n_own_only}")
print(f"  Missing from Ownly  {n_inc_only}")
print(piv[["on_ownly", "on_incumbent", "status"]].to_string())

print("\nCLOSURES (listed but shut at that slot) — NOT a coverage gap:")
print(closed_summary.to_string(index=False) if len(closed_summary) else "  none")

print("\nNon-food share of bill, median %:")
print(priced.groupby("platform")["non_food_share"].median().mul(100).round(1).to_string())
print("\nQuoted ETA midpoint, median min:")
print(a.groupby("platform")["eta_mid"].median().to_string())

for v in VIEWS:
    g = P[P["view"].eq(v)]
    if not len(g):
        continue
    print(f"\n=== {v} === n={len(g)} matched baskets | Ownly cheapest "
          f"{int(g.ownly_wins.sum())}/{len(g)} | median saving ₹{g.saving_rs.median():.2f} "
          f"({g.saving_pct.median():.1f}%)")
    print(g[["restaurant_display", "slot", "ownly_payable", "cheapest_incumbent",
             "incumbent_payable", "saving_rs", "saving_pct", "ownly_wins"]]
          .round(2).to_string(index=False))
