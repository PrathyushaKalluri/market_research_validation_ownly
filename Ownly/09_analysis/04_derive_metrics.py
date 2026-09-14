"""Step 4: derived metrics (PAP section 4) + long tables for models + dashboard mart tables.

Outputs (OUT_ROOT): survey_respondent_full.csv, dce_long_full.csv, index_reliability.csv
Mart (MART_DIR): fact_survey_respondent.csv, fact_dce_long.csv, fact_wtp_long.csv, fact_bill_choice_long.csv
"""
from __future__ import annotations

import re

import numpy as np
import pandas as pd

import config as C
import utils_io as io
import utils_stats as st
import utils_survey as us


def c(df, name):
    return df[name] if name in df.columns else pd.Series(np.nan, index=df.index)


def selected(df, var, label):
    return c(df, f"{var}__{us.slug(label)}").eq(1)


def joined(df, var):
    cols = [k for k in df.columns if k.startswith(f"{var}__") and not k.endswith(("__n_selected", "__other_text", "__num_parsed_range"))]
    return df[cols].apply(lambda r: ";".join(k.split("__", 1)[1] for k, v in r.items() if v == 1), axis=1) if cols else np.nan


def main():
    frames = [io.read_csv(C.CLEAN_DIR / f"{city}_survey_cleaned.csv", required=False, low_memory=False)
              for city in ("hyd", "blr")]
    df = pd.concat([f for f in frames if f is not None], ignore_index=True)
    d = pd.DataFrame(index=df.index)

    df["seg_occupation"] = c(df, "seg_occupation_raw").map(C.OCC_MAP)
    df["seg_freq"] = c(df, "scr_orders_4wk").map(C.FREQ_MAP)
    df["blr_pilot_area"] = (df.city.eq("blr") & c(df, "scr_area").isin([1, 2, 3])).astype(int)

    # awareness: human-coded column wins; regex is only a provisional first pass
    auto = c(df, "beh_unaided_apps").fillna("").str.contains(r"own\s*-?\s*l[yi]|rapido\s*food", flags=re.I, regex=True)
    df["own_aware_unaided_auto"] = auto.astype(int)
    if "own_aware_unaided" not in df.columns:
        df["own_aware_unaided"] = df["own_aware_unaided_auto"]
        df["own_aware_unaided_source"] = "regex_first_pass_NEEDS_HUMAN_CODING"

    n_plat = c(df, "beh_platforms_used_4wk__n_selected")
    df["beh_platform_count"] = n_plat
    df["beh_multihome"] = np.where(n_plat.notna(), (n_plat >= 2).astype(int), np.nan)
    df["multihome5"] = np.where(n_plat.notna(), np.where(n_plat >= 2, 5, 1), np.nan)
    df["beh_any_subscription"] = (selected(df, "beh_subscriptions", "Swiggy One (any plan)") |
                                  selected(df, "beh_subscriptions", "Zomato Gold") |
                                  selected(df, "beh_subscriptions", "another food-delivery membership")).astype(int)
    df["high_offer_dependency"] = c(df, "beh_offer_dependency").replace(98, np.nan).isin([3, 4]).astype(float) \
        .where(c(df, "beh_offer_dependency").replace(98, np.nan).notna())

    # ---- indices
    items = df[[k for k in C.PPI_ITEMS if k in df.columns]].replace(list(C.DK_CODES), np.nan)
    n_ok = items.notna().sum(axis=1)
    df["ppi"] = ((items.mean(axis=1) - 1) / 4 * 100).where(n_ok >= C.PPI_MIN_ITEMS)
    sri_parts = pd.DataFrame({"intent": st.rescale_1_5(c(df, "bt_trial_intent")),
                              "multi": st.rescale_1_5(df["multihome5"]),
                              "habit_rev": st.rescale_1_5(6 - c(df, "dec_habit_lock"))})
    df["sri"] = sri_parts.mean(axis=1).where(sri_parts.notna().all(axis=1))
    df["sri_no_intent"] = sri_parts[["multi", "habit_rev"]].mean(axis=1).where(sri_parts[["multi", "habit_rev"]].notna().all(axis=1))
    df["adi"] = st.rescale_1_5(c(df, "exp_fav_restaurant_needed"))
    df["adi_high"] = (df.adi >= 75).astype(float).where(df.adi.notna())

    thr = c(df, "beh_switch_savings_required")
    df["dec_switch_threshold_inr"] = thr.where(thr.isin([10, 20, 30, 50, 75, 100]))
    df["dec_switch_no_amount"] = thr.eq(0).astype(float).where(thr.notna())
    df["dec_switch_dk"] = thr.eq(98).astype(float).where(thr.notna())
    for k in ("exp_eta_max_lunch", "exp_eta_max_dinner"):
        df[f"{k}_min"] = c(df, k).where(~c(df, k).isin(list(C.DK_CODES)))

    df["fee_reconsider_ge3"] = (c(df, "pain_fee_reconsider_freq") >= 3).astype(float).where(c(df, "pain_fee_reconsider_freq").notna())
    df["abandon_price_ge2"] = (c(df, "beh_abandon_price_freq") >= 2).astype(float).where(c(df, "beh_abandon_price_freq").notna())
    mk = c(df, "pain_menu_markup_belief").replace(98, np.nan)
    df["markup_top2"] = (mk >= 4).astype(float).where(mk.notna())
    tf = "pain_top_frustrations"
    has_tf = c(df, f"{tf}__n_selected").notna()
    price_labels = ["delivery fees", "platform, packaging or other charges",
                    "menu prices higher than at the restaurant", "offers that don't really save money"]
    df["price_set"] = pd.concat([selected(df, tf, l) for l in price_labels], axis=1).any(axis=1).astype(float).where(has_tf)
    df["reliability_set"] = (selected(df, tf, "late delivery") | selected(df, tf, "cancelled orders")).astype(float).where(has_tf)
    inc_none = selected(df, "pain_incidents_3m", "none of these")
    df["pain_incident_any_3m"] = ((c(df, "pain_incidents_3m__n_selected") > 0) & ~inc_none).astype(float) \
        .where(c(df, "pain_incidents_3m__n_selected").notna())
    for pre in ("bt", "br"):
        ti = c(df, f"{pre}_trial_intent")
        df[f"{pre}_t2b"] = (ti >= 4).astype(float).where(ti.notna())
        df[f"{pre}_topbox"] = (ti == 5).astype(float).where(ti.notna())
    rx = c(df, "dem_rapido_ride_experience")
    df["rapido_exp_group"] = np.select([c(df, "dem_rapido_ride_use").eq(0), rx <= 2, rx == 3, rx >= 4],
                                       ["none", "negative", "neutral", "positive"], default="unknown")

    # ---- Ownly
    df["own_aware_any"] = (c(df, "own_aware_aided").isin([1, 2]) | df.own_aware_unaided.eq(1)).astype(int)
    df["aware_2wk_plus"] = c(df, "own_aware_duration").isin([2, 3, 4]).astype(float).where(c(df, "own_aware_duration").notna())
    df["own_tried_bin"] = c(df, "own_tried").eq(2).astype(float).where(c(df, "own_tried").notna())
    tried = df.own_tried_bin.eq(1)
    o4 = c(df, "own_orders_4wk")
    df["own_repeat"] = (o4 >= 2).astype(float).where(tried & o4.notna())
    df["own_lapsed"] = (o4 == 0).astype(float).where(tried & o4.notna())
    df["own_status"] = df.apply(us.ownly_status, axis=1)
    df["tenure_band"] = c(df, "own_first_order_month").map({1: "le_1m", 2: "le_1m", 3: "2_3m", 4: "gt_3m", 5: "gt_3m"})
    rel = c(df, "own_reliability_rating")
    df["on_time_most"] = (rel >= 4).astype(float).where(rel.notna())
    res = c(df, "own_support_issue_resolved").replace(9, np.nan)
    df["unresolved_issue"] = res.isin([0, 3]).astype(float).where(res.notna())
    df["offer_trigger"] = c(df, "own_first_trial_trigger").eq(1).astype(float).where(c(df, "own_first_trial_trigger").notna())

    # ---- fee ladder
    lad = us.ladder_frame(df)
    df = pd.concat([df, lad.drop(columns=[k for k in lad.columns if k in df.columns and k.startswith("FLAG_")])], axis=1)
    df["wtp_inconsistent"] = lad.FLAG_wtp_nonmonotone
    wtp_rows = []
    for _, r in df.iterrows():
        path = [int(x) for x in str(r.wtp_path).split(">") if x not in ("", "nan")]
        for f in C.WTP_FEES:
            asked = int(f in path)
            imp = np.nan
            if r.wtp_status == "ok":
                imp = 0 if r.wtp_rejects_all == 1 else int(f <= r.wtp_max_fee)
            wtp_rows.append({"resp_id": r.resp_id, "city": r.city, "seg_occupation": r.seg_occupation,
                             "seg_freq": r.seg_freq, "fee_inr": f, "asked": asked,
                             "accept": r.get(f"wtp_accept_{f}") if asked else np.nan,
                             "accept_imputed": imp, "wtp_inconsistent": r.wtp_inconsistent,
                             "wtp_start": r.get("wtp_start"), "meta_brand_arm": r.get("meta_brand_arm"),
                             "wtp_rejects_all": r.wtp_rejects_all, "wtp_status": r.wtp_status})
    wtp_long = io.stamp(pd.DataFrame(wtp_rows))

    # ---- bills
    bmap = pd.read_csv(C.BILL_MAP_FILE)
    bill_rows = []
    for _, s in bmap.iterrows():
        if s.scenario_id not in df.columns:
            continue
        meaning = [us.bill_meaning(v, s.scenario_id, code) for v, code in zip(df.meta_form_version, df[s.scenario_id])]
        mser = pd.Series(meaning, index=df.index)
        df[s.derived_var] = np.where(mser.isna() | mser.eq("no_difference"), np.nan, (mser == s.target_meaning).astype(float))
        df[f"{s.scenario_id}_indifferent"] = np.where(mser.isna(), np.nan, mser.eq("no_difference").astype(float))
        for i in df.index[mser.notna()]:
            bill_rows.append({"resp_id": df.at[i, "resp_id"], "city": df.at[i, "city"], "scenario_id": s.scenario_id,
                              "scenario_label": s.scenario_label, "is_synthetic_scenario": s.is_synthetic_scenario,
                              "source_audit_pair_id": s.source_audit_pair_id, "saving_inr": s.saving_inr,
                              "eta_diff_min": s.eta_diff_min, "rating_diff": s.rating_diff,
                              "ontime_diff_pct": s.ontime_diff_pct, "choice_meaning": mser[i],
                              "chose_target": df.at[i, s.derived_var],
                              "chose_lower_total": df.at[i, s.derived_var] if s.saving_inr > 0 else np.nan,
                              "seg_occupation": df.at[i, "seg_occupation"]})
    bill_long = io.stamp(pd.DataFrame(bill_rows))

    # ---- DCE + RSS (Hyderabad only)
    design = us.load_design()
    df["rss"] = np.nan
    dce_mart = pd.DataFrame()
    if design is not None and df.get("meta_dce_block", pd.Series(dtype=float)).notna().any():
        long = us.dce_long(df, design)
        df["rss"] = df.resp_id.map(us.rss_from_long(long))
        io.write_csv(io.stamp(long), C.OUT_ROOT / "dce_long_full.csv")
        dce_mart = io.stamp(pd.DataFrame({
            "resp_id": long.resp_id, "city": long.city, "block": long.block, "task_id": long.task,
            "task_display_order": long.position, "task_type": long.purpose_tag, "alt_id": long.alt,
            "price_total_inr": long.price, "eta_min": long.eta_min, "ontime_pct": (10 - long.late_in_10) * 10,
            "selection_level": long.restaurants, "refund_assurance": long.refund, "chosen": long.chosen,
            "is_cheaper_alt": long.is_cheaper_alt, "is_more_reliable_alt": long.is_more_reliable_alt}))

    # ---- reliability of indices
    rel_rows = [{"index": "ppi", "cronbach_alpha": st.cronbach_alpha(items), "n": int(items.dropna().shape[0]),
                 "use_composite": st.cronbach_alpha(items) >= C.ALPHA_MIN}]
    corr = sri_parts.corr(method="spearman")
    rel_rows.append({"index": "sri", "min_interitem_spearman": float(corr.where(~np.eye(3, dtype=bool)).min().min()),
                     "n": int(sri_parts.dropna().shape[0])})
    io.write_csv(io.stamp(pd.DataFrame(rel_rows)), C.OUT_ROOT / "index_reliability.csv")

    df = io.stamp(df)
    io.write_csv(df, C.OUT_ROOT / "survey_respondent_full.csv")
    mart = pd.DataFrame({
        "resp_id": df.resp_id, "city": df.city, "data_status": df.data_status,
        "meta_start_ts": c(df, "meta_start_dt"), "meta_submit_ts": c(df, "meta_submit_ts"),
        "meta_duration_sec": c(df, "meta_duration_sec"), "meta_channel": c(df, "meta_source"),
        "meta_form_version": df.meta_form_version, "meta_brand_arm": c(df, "meta_brand_arm"),
        "meta_dce_block": c(df, "meta_dce_block"), "meta_quality_flags": c(df, "exclusion_flags_all"),
        "scr_age": c(df, "scr_age_band"), "scr_locality": c(df, "scr_area"), "scr_orders_4wk": c(df, "scr_orders_4wk"),
        "seg_occupation": df.seg_occupation, "seg_freq": df.seg_freq, "dem_living": c(df, "dem_living"),
        "beh_platform_primary": c(df, "beh_platform_primary"), "beh_platforms_used_4wk": joined(df, "beh_platforms_used_4wk"),
        "beh_multihome": df.beh_multihome, "beh_last_order_total_inr": c(df, "beh_last_order_total"),
        "beh_last_occasion": c(df, "beh_last_meal"), "beh_last_time": np.nan,
        "beh_subscription": df.beh_any_subscription, "beh_abandon_freq": np.nan,
        "beh_abandon_price_freq": c(df, "beh_abandon_price_freq"), "beh_abandon_reason": np.nan,
        "pain_fee_reconsider_freq": c(df, "pain_fee_reconsider_freq"),
        "pain_bill_unreasonable_freq": c(df, "pain_bill_unreasonable_freq"),
        "pain_menu_markup_belief": c(df, "pain_menu_markup_belief"), "pain_top_frustrations": joined(df, tf),
        "exp_eta_max_min": df.exp_eta_max_dinner_min, "exp_fav_restaurant_needed": c(df, "exp_fav_restaurant_needed"),
        "dec_habit_lock": c(df, "dec_habit_lock"), "dec_trial_trigger_coded": np.nan,
        "dec_switch_threshold_inr": df.dec_switch_threshold_inr, "dec_switch_no_amount": df.dec_switch_no_amount,
        "bt_appeal": c(df, "bt_appeal"), "bt_trial_intent": c(df, "bt_trial_intent"), "bt_trust": c(df, "bt_trust"),
        "bt_expected_reliability": c(df, "bt_expected_reliability"), "bt_benefit_top": c(df, "bt_framing_pref"),
        "bt_concern_coded": np.nan, "br_aware_ownly": c(df, "own_aware_aided"), "br_trial_intent": c(df, "br_trial_intent"),
        "br_trust": c(df, "br_trust"), "br_expected_reliability": c(df, "br_expected_reliability"),
        "br_rapido_effect": c(df, "br_rapido_effect"), "own_status": df.own_status,
        "own_orders_total": c(df, "own_orders_4wk"), "own_discovery_source": c(df, "own_first_trial_trigger"),
        "own_perceived_saving_inr": c(df, "own_known_savings"), "own_continue_intent": c(df, "own_continue_intent"),
        "churn_reason_coded": joined(df, "churn_reduced_reasons"), "wtp_max_fee_inr": df.wtp_max_fee,
        "wtp_inconsistent": df.wtp_inconsistent, "ppi": df.ppi, "sri": df.sri, "rss": df.rss, "adi": df.adi,
        "bt_t2b": df.bt_t2b, "w_match_hyd": np.nan})
    io.write_csv(mart, C.MART_DIR / "fact_survey_respondent.csv")
    io.write_csv(dce_mart, C.MART_DIR / "fact_dce_long.csv")
    io.write_csv(wtp_long, C.MART_DIR / "fact_wtp_long.csv")
    io.write_csv(bill_long, C.MART_DIR / "fact_bill_choice_long.csv")


if __name__ == "__main__":
    main()
