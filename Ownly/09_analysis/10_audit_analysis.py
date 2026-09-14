"""Step 10: competitor basket audit (06_competitor_audit/audit_calculations.md; H2.3, H3, H5.1, H10.4).

Sign convention in this pipeline: saving_* = incumbent final_payable - Ownly final_payable
(positive = Ownly cheaper). Ties: |gap| <= ₹5. Only valid rows (listed, open, item match not
'none', arithmetic within ₹2) in the PRIMARY view (existing account, no subscription, no manual
coupon) enter price pairs; captures more than 10 minutes apart are not paired.
Outputs: MART_DIR/fact_audit_obs.csv, fact_audit_pairs.csv; OUT_ROOT/audit_summary.csv, audit_coverage.csv
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import config as C
import utils_io as io
import utils_stats as st

NUM = ["distance_km_shown", "menu_subtotal", "offline_subtotal_verified", "packaging_fee", "platform_fee",
       "delivery_fee", "small_cart_fee", "surge_rain_fee", "other_fees", "taxes_gst", "discount_amount",
       "subscription_saving_shown", "final_payable", "eta_min_shown", "eta_max_shown", "actual_delivery_min"]
FEES = ["packaging_fee", "platform_fee", "delivery_fee", "small_cart_fee", "surge_rain_fee", "other_fees"]
KEY = ["restaurant_id", "basket_id", "drop_point_id", "slot", "capture_date", "account_state", "subscription_active"]
INCUMBENTS = ["swiggy", "zomato"]


def main():
    if not C.AUDIT_FILE.exists() and not io.tag(C.AUDIT_FILE).exists():
        print(f"  no audit data at {C.AUDIT_FILE} — skipping")
        return
    df = io.read_csv(C.AUDIT_FILE, parse_dates=["capture_ts"])
    for k in NUM:
        df[k] = pd.to_numeric(df.get(k), errors="coerce")
    for k in ["platform", "account_state", "subscription_active", "restaurant_listed", "restaurant_open",
              "item_match_quality", "discount_type", "offline_price_source", "slot"]:
        df[k] = df[k].astype(str).str.strip().str.lower()
    df["fee_stack"] = df[FEES].fillna(0).sum(axis=1)
    df["eta_mid_shown"] = (df.eta_min_shown + df.eta_max_shown) / 2
    df["arith_gap"] = df.menu_subtotal + df.fee_stack + df.taxes_gst.fillna(0) - df.discount_amount.fillna(0) - df.final_payable
    df["arithmetic_flag"] = (df.arith_gap.abs() > 2).astype(int)
    verified = df.offline_price_source.ne("unverified") & df.offline_subtotal_verified.notna()
    df["premium_vs_offline_rs"] = np.where(verified, df.final_payable - df.offline_subtotal_verified, np.nan)
    df["primary_view"] = (df.account_state.eq("existing") & df.subscription_active.eq("n")
                          & df.discount_type.isin(["none", "auto_offer", "restaurant_offer", "nan"]))
    df["valid_row"] = (df.restaurant_listed.eq("y") & df.restaurant_open.eq("y")
                       & df.item_match_quality.ne("none") & df.arithmetic_flag.eq(0))
    df["capture_date"] = df.capture_ts.dt.date.astype(str)
    df["day_type"] = np.where(df.capture_ts.dt.dayofweek >= 5, "weekend", "weekday")

    v = df[df.valid_row & df.primary_view]
    pairs = []
    for key, g in v.groupby(KEY):
        own = g[g.platform == "ownly"]
        if own.empty:
            continue
        o = own.iloc[0]
        rec = dict(zip(KEY, key))
        inc = {}
        for p in INCUMBENTS:
            gp = g[g.platform == p]
            if gp.empty:
                continue
            r = gp.iloc[0]
            if abs((r.capture_ts - o.capture_ts).total_seconds()) / 60 <= 10:
                inc[p] = r
        cheapest = min(inc, key=lambda p: inc[p].final_payable) if inc else None
        rec.update({
            "pair_id": f"P{len(pairs) + 1:05d}", "capture_window_id": "|".join(map(str, key)),
            "day_type": o.day_type, "daypart": o.slot, "ownly_obs_id": o.audit_id, "ownly_final_inr": o.final_payable,
            "swiggy_final_inr": inc["swiggy"].final_payable if "swiggy" in inc else np.nan,
            "zomato_final_inr": inc["zomato"].final_payable if "zomato" in inc else np.nan,
            "cheapest_incumbent_platform": cheapest,
            "cheapest_incumbent_final_inr": inc[cheapest].final_payable if cheapest else np.nan,
            "eta_ownly_min": o.eta_mid_shown,
            "eta_cheapest_incumbent_min": inc[cheapest].eta_mid_shown if cheapest else np.nan,
            "menu_subtotal_diff_inr": o.menu_subtotal - inc[cheapest].menu_subtotal if cheapest else np.nan,
            "fee_diff_inr": o.fee_stack - inc[cheapest].fee_stack if cheapest else np.nan,
            "offline_premium_inr": o.premium_vs_offline_rs, "ownly_delivery_fee_inr": o.delivery_fee,
            "valid_pair": int(bool(inc)), "invalid_reason": "" if inc else "no_incumbent_within_10min"})
        pairs.append(rec)
    P = pd.DataFrame(pairs)
    if P.empty:
        print("  no matched pairs")
        return
    P["saving_vs_cheapest_inr"] = P.cheapest_incumbent_final_inr - P.ownly_final_inr
    P["saving_vs_swiggy_inr"] = P.swiggy_final_inr - P.ownly_final_inr
    P["saving_vs_zomato_inr"] = P.zomato_final_inr - P.ownly_final_inr
    P["saving_pct_vs_cheapest"] = P.saving_vs_cheapest_inr / P.cheapest_incumbent_final_inr
    P["ownly_tie"] = (P.saving_vs_cheapest_inr.abs() <= 5).astype(int)
    P["ownly_wins"] = (P.saving_vs_cheapest_inr > 5).astype(int)
    P["eta_diff_min"] = P.eta_ownly_min - P.eta_cheapest_incumbent_min
    io.write_csv(io.stamp(P), C.MART_DIR / "fact_audit_pairs.csv")

    VP = P[P.valid_pair == 1]
    summ = []

    def add(metric, val, lo=np.nan, hi=np.nan, n=np.nan, note=""):
        summ.append({"metric": metric, "value": val, "ci_low": lo, "ci_high": hi, "n": n, "note": note})

    n_rest = VP.restaurant_id.nunique()
    for col in ["saving_vs_cheapest_inr", "saving_vs_swiggy_inr", "saving_vs_zomato_inr", "saving_pct_vs_cheapest",
                "eta_diff_min", "menu_subtotal_diff_inr", "fee_diff_inr"]:
        m, lo, hi = st.cluster_boot_stat(VP, col, "restaurant_id", seed_offset=1000)
        add(f"median_{col}", m, lo, hi, int(VP[col].notna().sum()), f"cluster bootstrap by restaurant; {n_rest} restaurants")
    k, n = int(VP.ownly_wins.sum()), len(VP)
    p, lo, hi = st.wilson(k, n)
    add("ownly_win_rate", p, lo, hi, n, f"ties (<=₹5) share = {VP.ownly_tie.mean():.3f}")
    add("median_cheapest_incumbent_basket_inr", VP.cheapest_incumbent_final_inr.median(), n=n)
    add("audit_saving_pct_basket", VP.saving_vs_cheapest_inr.median() / VP.cheapest_incumbent_final_inr.median(), n=n,
        note="median saving / median cheapest-incumbent basket")
    add("ownly_observed_delivery_fee_inr", v.loc[v.platform == "ownly", "delivery_fee"].median(),
        n=int((v.platform == "ownly").sum()), note="median over valid primary-view Ownly rows")
    add("median_incumbent_eta_shown_min", v.loc[v.platform.isin(INCUMBENTS), "eta_mid_shown"].median())
    per_rest = VP.assign(ok=(VP.saving_vs_cheapest_inr >= -5).astype(int)).groupby("restaurant_id").ok.agg(["mean", "size"])
    per_rest = per_rest[per_rest["size"] >= 3]
    add("consistency_share_restaurants_ownly_cheaper_or_tied_80pct", (per_rest["mean"] >= .8).mean(), n=len(per_rest))
    verified = VP.offline_premium_inr.dropna()
    add("median_ownly_premium_vs_verified_offline_inr", verified.median() if len(verified) else np.nan, n=len(verified),
        note="only rows with verified offline price")

    cov = (df.groupby(["platform", "slot", "restaurant_id"])
             .agg(listed=("restaurant_listed", lambda s: (s == "y").any()), open_=("restaurant_open", lambda s: (s == "y").any()))
             .reset_index())
    cov_rows = []
    for (plat, slot), g in cov.groupby(["platform", "slot"]):
        for what in ("listed", "open_"):
            kk = int((g.listed & g.open_).sum()) if what == "open_" else int(g.listed.sum())
            pp, l2, h2 = st.wilson(kk, len(g))
            cov_rows.append({"platform": plat, "slot": slot, "coverage_type": "listed" if what == "listed" else "listed_and_open",
                             "k": kk, "n_frame_restaurants": len(g), "share": pp, "ci_low": l2, "ci_high": h2})
    rest_level = cov.groupby(["platform", "restaurant_id"]).listed.any().reset_index()
    own_cov = rest_level[rest_level.platform == "ownly"]
    kk = int(own_cov.listed.sum())
    pp, l2, h2 = st.wilson(kk, len(own_cov))
    add("ownly_listing_coverage_of_frame", pp, l2, h2, len(own_cov), "frame-relative, not citywide")
    io.write_csv(io.stamp(pd.DataFrame(summ)), C.OUT_ROOT / "audit_summary.csv")
    io.write_csv(io.stamp(pd.DataFrame(cov_rows)), C.OUT_ROOT / "audit_coverage.csv")

    obs = pd.DataFrame({
        "obs_id": df.audit_id, "capture_ts": df.capture_ts, "capture_window_id": df[KEY].astype(str).agg("|".join, axis=1),
        "day_type": df.day_type, "daypart": df.slot, "drop_point_id": df.drop_point_id, "restaurant_id": df.restaurant_id,
        "restaurant_name": df.restaurant_name, "restaurant_type": np.nan, "basket_id": df.basket_id, "platform": df.platform,
        "available": df.restaurant_listed.eq("y") & df.restaurant_open.eq("y"),
        "items_all_available": df.item_match_quality.ne("none"), "item_subtotal_inr": df.menu_subtotal,
        "packaging_fee_inr": df.packaging_fee, "platform_fee_inr": df.platform_fee, "delivery_fee_inr": df.delivery_fee,
        "other_fees_inr": df[["small_cart_fee", "surge_rain_fee", "other_fees"]].fillna(0).sum(axis=1),
        "taxes_inr": df.taxes_gst, "discount_inr": df.discount_amount, "subscription_applied": df.subscription_active,
        "account_type": df.account_state, "final_payable_inr": df.final_payable,
        "final_payable_check_inr": df.final_payable + df.arith_gap, "eta_min_displayed": df.eta_mid_shown,
        "distance_km_displayed": df.distance_km_shown, "promo_text": df.promo_banner_text,
        "offline_price_inr": df.offline_subtotal_verified, "offline_price_verified": verified,
        "offline_evidence_ref": df.offline_price_source, "screenshot_ref": df.screenshot_file, "auditor_id": df.auditor_id})
    io.write_csv(io.stamp(obs), C.MART_DIR / "fact_audit_obs.csv")


if __name__ == "__main__":
    main()
