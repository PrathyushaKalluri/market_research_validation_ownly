"""Step 7: choice-experiment models (PAP 6.1) — Hyderabad only.

With 2 forced-choice alternatives and no opt-out, the conditional logit is exactly a
no-intercept binary logit on attribute differences (A - B); this lets us use
respondent-clustered SEs directly (statsmodels Logit, cov_type='cluster').
WTP = beta_attr / beta_price (sign conventions below), CIs by Krinsky-Robb (5,000 draws).
WTP is reported only if the price coefficient is significant (p < 0.05).

Outputs: OUT_ROOT/dce_task_shares.csv, MART_DIR/fact_model_dce.csv, OUT_ROOT/dce_hypothesis_inputs.csv
"""
from __future__ import annotations

from datetime import datetime

import numpy as np
import pandas as pd
import statsmodels.api as sm

import config as C
import utils_io as io
import utils_stats as st

ATTRS = ["price", "eta_min", "late3", "rest_some", "rest_few", "refund_case"]
WTP_DEF = {  # metric: (attribute, multiplier) ; ₹ a respondent would give up to obtain the better level
    "wtp_10min_faster_inr": ("eta_min", 10),
    "wtp_reliability_1in10_vs_3in10_inr": ("late3", 1),
    "wtp_most_vs_few_restaurants_inr": ("rest_few", 1),
    "wtp_most_vs_some_restaurants_inr": ("rest_some", 1),
    "wtp_auto_refund_inr": ("refund_case", 1),
}


def diff_frame(long):
    L = long.copy()
    L["late3"] = (L.late_in_10 == L.late_in_10.max()).astype(int)
    L["rest_some"] = (L.restaurants == "some").astype(int)
    L["rest_few"] = (L.restaurants == "few").astype(int)
    L["refund_case"] = (L.refund == "case_by_case").astype(int)
    a = L[L.alt == "A"].set_index(["resp_id", "task"])
    b = L[L.alt == "B"].set_index(["resp_id", "task"])
    X = a[ATTRS] - b[ATTRS]
    out = X.assign(y=a.chosen, seg_occupation=a.seg_occupation).reset_index()
    return out


def kr_wtp(params, cov, names, attr, mult, rng, draws=C.N_KRINSKY_ROBB, price="price"):
    beta = np.asarray(params)
    V = np.asarray(cov)
    with np.errstate(all="ignore"):          # numpy 2.0 + Accelerate emits spurious matmul warnings
        sims = rng.multivariate_normal(beta, V, size=draws, method="cholesky")
    if not np.isfinite(sims).all():
        raise FloatingPointError("non-finite Krinsky-Robb draws")
    i_a, i_p = names.index(attr), names.index(price)
    point = mult * beta[i_a] / beta[i_p]
    s = mult * sims[:, i_a] / sims[:, i_p]
    return point, *np.percentile(s, [2.5, 97.5])


def fit(d, names):
    res = sm.Logit(d.y, d[names]).fit(disp=0, cov_type="cluster", cov_kwds={"groups": pd.factorize(d.resp_id)[0]})
    return res


def model_rows(model_id, segment, res, d, names, extra_wtp):
    rows, ts = [], datetime.now().isoformat(timespec="seconds")
    ci = res.conf_int()
    base = {"model_id": model_id, "model_type": "conditional_logit_pairwise_diff", "outcome": "chosen",
            "segment": segment, "n_resp": d.resp_id.nunique(), "n_obs": len(d), "events": int(d.y.sum()),
            "epv": np.nan, "pseudo_r2": res.prsquared, "run_ts": ts, "code_ref": "09_analysis/07_dce_models.py",
            "ci_method": "cluster_robust_resp", "data_status": C.DATA_STATUS}
    for t in names:
        rows.append({**base, "term": t, "estimate": res.params[t], "std_error": res.bse[t],
                     "ci_low": ci.loc[t, 0], "ci_high": ci.loc[t, 1], "p_value": res.pvalues[t]})
    for metric, (val, lo, hi, note) in extra_wtp.items():
        rows.append({**base, "term": "", "derived_metric": metric, "derived_value": val,
                     "derived_ci_low": lo, "derived_ci_high": hi, "ci_method": f"krinsky_robb_{C.N_KRINSKY_ROBB}",
                     "notes": note})
    return rows


def main():
    long = io.read_csv(C.OUT_ROOT / "dce_long_full.csv", required=False)
    if long is None or long.empty:
        print("  no DCE data (Hyderabad only) — skipping")
        return
    rng = st.rng(700)
    # fallback / descriptive task shares
    shares = []
    ch = long[long.chosen == 1]
    for (tag, seg), g in pd.concat([ch.assign(seg="all"), ch.assign(seg=ch.seg_occupation)]).groupby(["purpose_tag", "seg"]):
        k, n = int(g.is_cheaper_alt.sum()), len(g)
        p, lo, hi = st.wilson(k, n)
        shares.append({"task_type": tag, "segment": seg, "chose_cheaper_k": k, "n_choices": n,
                       "share_chose_cheaper": p, "ci_low": lo, "ci_high": hi, "data_status": C.DATA_STATUS})
    io.write_csv(pd.DataFrame(shares), C.OUT_ROOT / "dce_task_shares.csv")

    d = diff_frame(long)
    rows, hyp = [], []
    n_resp = d.resp_id.nunique()
    status = "ok" if n_resp >= C.MIN_N_DCE else f"below_min_n_{C.MIN_N_DCE}_directional"
    res = fit(d, ATTRS)
    price_sig = res.pvalues["price"] < C.ALPHA and res.params["price"] < 0
    wtp = {}
    for metric, (attr, mult) in WTP_DEF.items():
        if price_sig:
            val, lo, hi = kr_wtp(res.params, res.cov_params(), ATTRS, attr, mult, rng)
            wtp[metric] = (val, lo, hi, status)
        else:
            wtp[metric] = (np.nan, np.nan, np.nan, "price_not_significant_wtp_not_identifiable")
        hyp.append({"metric": metric, "segment": "all", "value": wtp[metric][0], "ci_low": wtp[metric][1],
                    "ci_high": wtp[metric][2], "n_resp": n_resp, "status": wtp[metric][3],
                    "p_price": res.pvalues["price"]})
    # marginal effect of ₹30 lower price on choice probability at the sample mean (H2.1)
    me = 1 / (1 + np.exp(-(-30 * res.params["price"]))) - 0.5
    hyp.append({"metric": "choice_prob_gain_30inr", "segment": "all", "value": me, "ci_low": np.nan,
                "ci_high": np.nan, "n_resp": n_resp, "status": status, "p_price": res.pvalues["price"]})
    rows += model_rows("dce_m1_pooled", "all", res, d, ATTRS, wtp)

    # Model 2: student vs professional interactions (H5.2, H6.3)
    s = d[d.seg_occupation.isin(C.H6_GROUPS)].copy()
    if s.resp_id.nunique() >= 2 * C.MIN_N_GROUP and s.seg_occupation.nunique() == 2:
        s["prof"] = (s.seg_occupation == "working_professional").astype(int)
        inter = []
        for a in ATTRS:
            s[f"{a}_x_prof"] = s[a] * s.prof
            inter.append(f"{a}_x_prof")
        names = ATTRS + inter
        r2 = fit(s, names)
        with np.errstate(all="ignore"):
            sims = rng.multivariate_normal(r2.params.values, r2.cov_params().values, size=C.N_KRINSKY_ROBB, method="cholesky")
        if not np.isfinite(sims).all():
            raise FloatingPointError("non-finite Krinsky-Robb draws (model 2)")
        idx = {n: i for i, n in enumerate(names)}
        wtp2 = {}
        for metric, (attr, mult) in WTP_DEF.items():
            stu = mult * sims[:, idx[attr]] / sims[:, idx["price"]]
            pro = mult * (sims[:, idx[attr]] + sims[:, idx[f"{attr}_x_prof"]]) / (sims[:, idx["price"]] + sims[:, idx["price_x_prof"]])
            b = r2.params
            p_stu = mult * b[attr] / b["price"]
            p_pro = mult * (b[attr] + b[f"{attr}_x_prof"]) / (b["price"] + b["price_x_prof"])
            seg_status = "ok" if min(s[s.prof == 1].resp_id.nunique(), s[s.prof == 0].resp_id.nunique()) >= C.MIN_N_DCE \
                else "segment_n_below_125_directional"
            for label, pt, arr in (("student", p_stu, stu), ("working_professional", p_pro, pro), ("prof_minus_student", p_pro - p_stu, pro - stu)):
                wtp2[f"{metric}__{label}"] = (pt, *np.percentile(arr, [2.5, 97.5]), seg_status)
                hyp.append({"metric": metric, "segment": label, "value": pt,
                            "ci_low": np.percentile(arr, 2.5), "ci_high": np.percentile(arr, 97.5),
                            "n_resp": s.resp_id.nunique(), "status": seg_status, "p_price": r2.pvalues["price"]})
        rows += model_rows("dce_m2_segment_interaction", "student_vs_professional", r2, s, names, wtp2)
    io.write_csv(pd.DataFrame(rows), C.MART_DIR / "fact_model_dce.csv")
    io.write_csv(pd.DataFrame(hyp).assign(data_status=C.DATA_STATUS), C.OUT_ROOT / "dce_hypothesis_inputs.csv")


if __name__ == "__main__":
    main()
