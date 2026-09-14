"""Step 5: pre-specified descriptives (PAP section 3), by city x {all, seg_occupation, seg_freq}.

Every row carries n and a 95% CI (Wilson for shares, bootstrap percentile for medians).
Outputs (OUT_ROOT/descriptives/): desc_categorical.csv, desc_multiselect.csv, desc_numeric.csv
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import config as C
import utils_io as io
import utils_stats as st

CATEGORICAL = ["scr_orders_4wk", "seg_freq", "seg_occupation", "dem_living", "scr_area", "beh_last_meal",
               "beh_last_people", "beh_last_food", "beh_last_restaurant_type", "beh_last_platform",
               "beh_platform_primary", "beh_offer_dependency", "dec_habit_lock", "beh_compare_freq",
               "beh_switched_primary_12m", "pain_fee_reconsider_freq", "pain_bill_unreasonable_freq",
               "beh_abandon_price_freq", "pain_late_freq", "pain_cancel_freq", "pain_wrong_item_freq",
               "pain_restaurant_unavailable_freq", "pain_quality_freq", "pain_menu_markup_belief",
               "exp_late_tolerance", "exp_fav_restaurant_needed", "exp_refund_expectation",
               "beh_switch_savings_required", "bt_trial_intent", "bt_framing_pref", "br_rapido_effect",
               "own_aware_aided", "own_tried", "own_status", "own_first_trial_trigger", "own_orders_4wk",
               "own_perceived_savings", "own_reliability_rating", "own_continue_intent"]
NUMERIC = ["beh_last_order_total", "ppi", "sri", "sri_no_intent", "rss", "adi", "wtp_max_fee",
           "exp_eta_max_lunch_min", "exp_eta_max_dinner_min", "dec_switch_threshold_inr", "own_last_total",
           "own_known_savings", "meta_duration_sec"]
BINARY = ["fee_reconsider_ge3", "abandon_price_ge2", "markup_top2", "price_set", "reliability_set",
          "pain_incident_any_3m", "beh_multihome", "beh_any_subscription", "high_offer_dependency", "adi_high",
          "bt_t2b", "bt_topbox", "own_aware_any", "own_tried_bin", "own_repeat", "own_lapsed", "on_time_most",
          "dec_switch_no_amount"]


def scopes(df):
    for city, g in df.groupby("city"):
        yield city, "all", "all", g
        for dim in ("seg_occupation", "seg_freq"):
            for val, gg in g.groupby(dim):
                yield city, dim, val, gg


def main():
    df = io.read_csv(C.OUT_ROOT / "survey_respondent_full.csv", low_memory=False)
    cat, multi, num = [], [], []
    multi_cols = [k for k in df.columns if "__" in k and not k.endswith(("__n_selected", "__other_text", "__num_parsed_range"))]
    for city, dim, val, g in scopes(df):
        base = {"city": city, "scope_dim": dim, "scope_value": val}
        for v in [x for x in CATEGORICAL if x in g.columns]:
            s = g[v].dropna()
            for level, k in s.value_counts().sort_index().items():
                p, lo, hi = st.wilson(k, len(s))
                cat.append({**base, "variable": v, "level": level, "k": int(k), "n": len(s),
                            "share": p, "ci_low": lo, "ci_high": hi})
        for v in [x for x in BINARY if x in g.columns]:
            s = g[v].dropna()
            p, lo, hi = st.wilson(s.sum(), len(s))
            cat.append({**base, "variable": v, "level": 1, "k": int(s.sum()), "n": len(s),
                        "share": p, "ci_low": lo, "ci_high": hi})
        for v in multi_cols:
            s = g[v].dropna()
            if len(s) == 0:
                continue
            p, lo, hi = st.wilson(s.sum(), len(s))
            q, opt = v.split("__", 1)
            multi.append({**base, "question": q, "option": opt, "k": int(s.sum()), "n": len(s),
                          "share": p, "ci_low": lo, "ci_high": hi})
        for v in [x for x in NUMERIC if x in g.columns]:
            s = pd.to_numeric(g[v], errors="coerce").dropna()
            if len(s) == 0:
                continue
            med, lo, hi = st.boot_median_ci(s, n_boot=min(C.N_BOOT, 2000))
            num.append({**base, "variable": v, "n": len(s), "median": med, "median_ci_low": lo, "median_ci_high": hi,
                        "q1": s.quantile(.25), "q3": s.quantile(.75), "mean": s.mean(), "sd": s.std(ddof=1)})
    out = C.OUT_ROOT / "descriptives"
    io.write_csv(io.stamp(pd.DataFrame(cat)), out / "desc_categorical.csv")
    io.write_csv(io.stamp(pd.DataFrame(multi)), out / "desc_multiselect.csv")
    io.write_csv(io.stamp(pd.DataFrame(num)), out / "desc_numeric.csv")


if __name__ == "__main__":
    main()
