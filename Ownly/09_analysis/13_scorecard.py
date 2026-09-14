"""Step 13: market-fit scorecard + pre-registered decision rule (11_insights/decision_framework_and_scorecard.md).

Scopes: hyd pooled, students, working professionals. Inputs are linear-anchored to 0-100
(config.SCORE_INPUTS); missing inputs re-normalise weights and drop the evidence badge one level;
>50% weight missing -> INSUFFICIENT. Decision computed for default + 3 alternative weight sets.
Outputs: MART_DIR/fact_scorecard.csv, OUT_ROOT/decision.csv
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import config as C
import utils_io as io

LEVELS = ["LOW", "MEDIUM", "HIGH"]


def lin(v, weak, strong):
    return float(np.clip((v - weak) / (strong - weak) * 100, 0, 100)) if pd.notna(v) else np.nan


def get(tbl, metric, col="value"):
    if tbl is None or metric not in tbl.index:
        return np.nan
    return tbl.loc[metric, col]


def inputs_for(scope, df, audit, wtp, reviews, fake):
    h = df[df.city == "hyd"]
    if scope != "hyd_pooled":
        h = h[h.seg_occupation == scope]
    own = df[df.own_tried_bin == 1]
    if scope != "hyd_pooled":
        own = own[own.seg_occupation == scope]
    v = {}
    v["ppi_median"] = (h.ppi.median(), h.ppi.notna().sum())
    v["abandon_price_share"] = (h.abandon_price_ge2.mean(), h.abandon_price_ge2.notna().sum())
    v["fee_reconsider_share"] = (h.fee_reconsider_ge3.mean(), h.fee_reconsider_ge3.notna().sum())
    v["sri_median"] = (h.sri.median(), h.sri.notna().sum())
    sav = get(audit, "median_saving_vs_cheapest_inr")
    base = h[h.dec_switch_threshold_inr.notna() | h.dec_switch_no_amount.eq(1)]
    v["threshold_met_share"] = ((base.dec_switch_threshold_inr <= sav).mean(), len(base)) if pd.notna(sav) else (np.nan, 0)
    v["multihome_share"] = (h.beh_multihome.mean(), h.beh_multihome.notna().sum())
    v["no_subscription_share"] = (1 - h.beh_any_subscription.mean(), h.beh_any_subscription.notna().sum())
    v["audit_win_rate"] = (get(audit, "ownly_win_rate"), get(audit, "ownly_win_rate", "n"))
    v["audit_saving_pct_basket"] = (get(audit, "audit_saving_pct_basket"), get(audit, "audit_saving_pct_basket", "n"))
    fee = C.OWNLY_OBSERVED_FEE_INR if C.OWNLY_OBSERVED_FEE_INR is not None else get(audit, "ownly_observed_delivery_fee_inr")
    if pd.notna(fee) and wtp is not None:
        grid = int(np.clip(round(fee / 10) * 10, 0, 60))
        w = wtp[(wtp.city == "hyd") & (wtp.wtp_status == "ok") & (wtp.fee_inr == grid)]
        if scope != "hyd_pooled":
            w = w[w.seg_occupation == scope]
        v["fee_accept_at_ownly_fee"] = (w.accept_imputed.mean(), len(w))
    else:
        v["fee_accept_at_ownly_fee"] = (np.nan, 0)
    gap, inc_eta = get(audit, "median_eta_diff_min"), get(audit, "median_incumbent_eta_shown_min")
    margin = h.exp_eta_max_dinner_min.median() - inc_eta
    eta_score = np.nan if pd.isna(gap) or pd.isna(margin) else (100.0 if gap <= 0 else float(np.clip(100 * margin / gap, 0, 100)))
    v["eta_acceptability"] = (eta_score, h.exp_eta_max_dinner_min.notna().sum(), "formula")
    cov = get(audit, "ownly_listing_coverage_of_frame")
    need = 1 - h.adi_high.mean() * 0.5
    v["coverage_adequacy"] = (float(np.clip(100 * min(1, cov / need), 0, 100)) if pd.notna(cov) and need > 0 else np.nan,
                              get(audit, "ownly_listing_coverage_of_frame", "n"), "formula")
    v["ontime_most_share"] = (own.on_time_most.mean(), own.on_time_most.notna().sum())
    v["review_reliability_score"] = (get(reviews, "review_reliability_score"), get(reviews, "review_reliability_score", "n"), "formula")
    aw = h[h.aware_2wk_plus == 1].own_tried_bin
    v["aware_to_tried"] = (aw.mean(), aw.notna().sum())
    v["repeat_rate"] = (own.own_repeat.mean(), own.own_repeat.notna().sum())
    if fake is not None and len(fake):
        best = fake[fake.utm_source == "all"].sort_values("hi_conv", ascending=False).iloc[0]
        t2b = h[h.meta_brand_arm == "blind"].bt_t2b.mean()
        v["intent_action_ratio"] = (best.hi_conv / t2b if t2b else np.nan, best.unique_sessions, bool(best.directional_only))
    else:
        v["intent_action_ratio"] = (np.nan, 0)
    return v, len(h)


def main():
    df = io.read_csv(C.OUT_ROOT / "survey_respondent_full.csv", low_memory=False)
    audit = io.read_csv(C.OUT_ROOT / "audit_summary.csv", required=False)
    audit = audit.set_index("metric") if audit is not None else None
    reviews = io.read_csv(C.OUT_ROOT / "review_summary_metrics.csv", required=False)
    reviews = reviews.set_index("metric") if reviews is not None else None
    wtp = io.read_csv(C.MART_DIR / "fact_wtp_long.csv", required=False)
    fake = io.read_csv(C.MART_DIR / "agg_fakedoor_variant.csv", required=False)
    rows, dims = [], {}
    for scope in ("hyd_pooled",) + C.H6_GROUPS:
        vals, n_scope = inputs_for(scope, df, audit, wtp, reviews, fake)
        for dim in ["D1", "D2", "D3", "D4", "D5"]:
            keys = [k for k, s in C.SCORE_INPUTS.items() if s[0] == dim]
            scored, wsum, missing_w, badge, small = [], 0.0, 0.0, 2, False
            for k in keys:
                _, wt, weak, strong = C.SCORE_INPUTS[k]
                val, n = vals[k][0], vals[k][1]
                sc = val if weak is None else lin(val, weak, strong)
                if pd.isna(sc):
                    missing_w += wt
                    badge -= 1
                else:
                    scored.append((sc, wt))
                    small |= (pd.notna(n) and n < C.MIN_SEGMENT_N_TARGET)
                    if k == "intent_action_ratio" and len(vals[k]) > 2 and vals[k][2]:
                        badge -= 1
                rows.append({"scope": scope, "n_scope": n_scope, "dimension": dim, "input_metric": k, "input_value": val,
                             "input_ci_low": np.nan, "input_ci_high": np.nan, "input_n": n, "input_score": sc,
                             "input_weight_within_dimension": wt})
            badge -= int(small)
            score = np.nan if missing_w > 0.5 or not scored else sum(s * w for s, w in scored) / sum(w for _, w in scored)
            strength = "INSUFFICIENT" if pd.isna(score) else LEVELS[max(badge, 0)]
            dims[(scope, dim)] = (score, strength)
            for r in rows:
                if r["scope"] == scope and r["dimension"] == dim:
                    r.update(dimension_score=score, evidence_strength=strength, default_weight=C.DEFAULT_WEIGHTS[dim],
                             gate_fail=bool(pd.notna(score) and score < C.GATE_BLOCK_SCALE))
    fact = io.stamp(pd.DataFrame(rows))
    fact["dimension_ci_low"] = np.nan
    fact["dimension_ci_high"] = np.nan
    io.write_csv(fact, C.MART_DIR / "fact_scorecard.csv")

    def meets_scale(scope, weights):
        sc = {d: dims[(scope, d)] for d in weights}
        if any(pd.isna(s) for s, _ in sc.values()):
            return False, np.nan
        total = sum(weights[d] * sc[d][0] for d in weights)
        ok = total >= C.SCALE_TOTAL and all(s >= C.SCALE_MIN_DIM for s, _ in sc.values()) and sc["D5"][1] in ("MEDIUM", "HIGH")
        return ok, total

    decisions = []
    for wname, weights in [("default", C.DEFAULT_WEIGHTS)] + list(C.ALT_WEIGHT_SETS.items()):
        ok, total = meets_scale("hyd_pooled", weights)
        D = {d: dims[("hyd_pooled", d)][0] for d in weights}
        lows = sum(dims[("hyd_pooled", d)][1] in ("LOW", "INSUFFICIENT") for d in weights)
        rethink = all((pd.notna(dims[(s, "D1")][0]) and dims[(s, "D1")][0] < C.GATE_RETHINK) or
                      (pd.notna(dims[(s, "D2")][0]) and dims[(s, "D2")][0] < C.GATE_RETHINK) for s in ("hyd_pooled",) + C.H6_GROUPS)
        seg_ok = [s for s in C.H6_GROUPS if meets_scale(s, weights)[0] and (df[(df.city == "hyd") & (df.seg_occupation == s)].shape[0] >= C.MIN_SEGMENT_N_TARGET)]
        if rethink:
            rec = "RETHINK PROPOSITION"
        elif ok:
            rec = "SCALE"
        elif seg_ok:
            rec = f"TARGET SELECTIVELY: {', '.join(seg_ok)}"
        elif pd.notna(D["D1"]) and pd.notna(D["D2"]) and D["D1"] >= C.ADAPT_MIN and D["D2"] >= C.ADAPT_MIN and \
                ((pd.notna(D["D3"]) and D["D3"] < C.ADAPT_MIN) or (pd.notna(D["D4"]) and D["D4"] < C.ADAPT_MIN)):
            rec = "ADAPT: fix " + " & ".join(d for d in ("D3", "D4") if pd.notna(D[d]) and D[d] < C.ADAPT_MIN)
        else:
            avail = {d: s for d, s in D.items() if pd.notna(s)}
            rec = f"ADAPT: weakest = {min(avail, key=avail.get)}" if avail else "INSUFFICIENT EVIDENCE"
        if lows >= 2:
            rec = "PROVISIONAL — evidence insufficient | " + rec
        decisions.append({"weight_set": wname, "weighted_total": total, **{f"{d}_score": D[d] for d in D},
                          "recommendation_by_rule": rec, "n_low_or_insufficient_dimensions": lows,
                          "note": "Rule output is an INPUT to the team's joint human decision, never the decision itself."})
    io.write_csv(io.stamp(pd.DataFrame(decisions)), C.OUT_ROOT / "decision.csv")
    print(pd.DataFrame(decisions)[["weight_set", "weighted_total", "recommendation_by_rule"]].to_string())


if __name__ == "__main__":
    main()
