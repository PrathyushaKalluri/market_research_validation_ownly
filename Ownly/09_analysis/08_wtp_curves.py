"""Step 8: Gabor-Granger delivery-fee analysis (PAP 6.2, H8, H6.2).

ESTIMATOR NOTE (interval censoring). The staircase (up on yes / down on no, stop at first
reversal, ₹10 grid) brackets each respondent's WTP within one ₹10 grid cell, e.g. yes at ₹30 and
no at ₹40 -> WTP in [30, 40). Under the standard Gabor-Granger monotonicity assumption,
acceptance at every GRID fee is therefore fully determined (accept_imputed = 1[wtp_max_fee >= f]);
the NPMLE/Turnbull estimator on this grid reduces to these empirical shares. Between grid points
we interpolate linearly, which assumes WTP is uniform within a ₹10 cell. Right-censoring at ₹60
(wtp_censored_top) only affects fees above the grid and is reported as a share. wtp_rejects_all
respondents are 0 at every fee in the primary curve and removed in a sensitivity curve.
Only wtp_status == 'ok' respondents enter the curves (incomplete paths reported separately).

Outputs: OUT_ROOT/wtp_curve.csv, wtp_summary.csv, wtp_elasticity.csv, wtp_model_coefs.csv
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

import config as C
import utils_io as io
import utils_stats as st

FEES = np.array(C.WTP_FEES, dtype=float)


def curve(wide):
    return wide.mean(axis=0).reindex(C.WTP_FEES).to_numpy(dtype=float)


def median_fee(acc):
    if acc[0] < 0.5:
        return -np.inf
    if acc[-1] >= 0.5:
        return np.inf
    for i in range(len(FEES) - 1):
        if acc[i] >= 0.5 > acc[i + 1]:
            return FEES[i] + (acc[i] - 0.5) / (acc[i] - acc[i + 1]) * (FEES[i + 1] - FEES[i])
    return np.nan


def arc(acc):
    out = []
    for i in range(len(FEES) - 1):
        q1, q2, p1, p2 = acc[i], acc[i + 1], FEES[i], FEES[i + 1]
        denom_q = (q1 + q2) / 2
        out.append(((q2 - q1) / denom_q) / ((p2 - p1) / ((p1 + p2) / 2)) if denom_q > 0 else np.nan)
    return np.array(out)


def boot(wide, func, n_boot, seed):
    arr = wide.to_numpy(dtype=float)
    g = st.rng(seed)
    vals = [func(np.nanmean(arr[g.integers(0, len(arr), len(arr))], axis=0)) for _ in range(n_boot)]
    return np.array(vals)


def main():
    long = io.read_csv(C.MART_DIR / "fact_wtp_long.csv")
    ok = long[long.wtp_status == "ok"].copy()
    resp = ok.drop_duplicates("resp_id").set_index("resp_id")
    wide = ok.pivot_table(index="resp_id", columns="fee_inr", values="accept_imputed")
    n_boot = min(C.N_BOOT, 2000)
    scopes = [("city", c) for c in resp.city.unique()]
    scopes += [("seg_occupation", s) for s in C.H6_GROUPS]
    scopes += [("wtp_start", s) for s in sorted(resp.wtp_start.dropna().unique())]
    scopes += [("meta_brand_arm", a) for a in resp.meta_brand_arm.dropna().unique()]
    curve_rows, summ_rows, el_rows = [], [], []
    for variant in ("primary", "excl_rejects_all"):
        for dim, val in scopes:
            ids = resp.index[(resp[dim] == val) & (resp.city == "hyd" if dim != "city" else True)]
            if variant == "excl_rejects_all":
                ids = ids[resp.loc[ids, "wtp_rejects_all"] != 1]
            w = wide.loc[wide.index.intersection(ids)]
            n = len(w)
            if n == 0:
                continue
            acc = curve(w)
            for f, a in zip(C.WTP_FEES, acc):
                k = int(round(a * n))
                p, lo, hi = st.wilson(k, n)
                curve_rows.append({"variant": variant, "scope_dim": dim, "scope_value": val, "fee_inr": f,
                                   "n": n, "accept_share": a, "ci_low": lo, "ci_high": hi})
            b_med = boot(w, median_fee, n_boot, 800)
            finite = b_med[np.isfinite(b_med)]
            summ_rows.append({"variant": variant, "scope_dim": dim, "scope_value": val, "n": n,
                              "median_acceptable_fee_inr": median_fee(acc),
                              "median_ci_low": np.percentile(finite, 2.5) if len(finite) else np.nan,
                              "median_ci_high": np.percentile(finite, 97.5) if len(finite) else np.nan,
                              "share_boot_nonfinite": 1 - len(finite) / len(b_med),
                              "censored_top_share": resp.loc[w.index, "wtp_rejects_all"].pipe(lambda _: (w[60] == 1).mean()),
                              "rejects_all_share": resp.loc[w.index, "wtp_rejects_all"].mean()})
            b_el = boot(w, arc, n_boot, 801)
            for i, e in enumerate(arc(acc)):
                el_rows.append({"variant": variant, "scope_dim": dim, "scope_value": val,
                                "fee_from": C.WTP_FEES[i], "fee_to": C.WTP_FEES[i + 1], "n": n, "arc_elasticity": e,
                                "ci_low": np.nanpercentile(b_el[:, i], 2.5), "ci_high": np.nanpercentile(b_el[:, i], 97.5)})
    io.write_csv(io.stamp(pd.DataFrame(curve_rows)), C.OUT_ROOT / "wtp_curve.csv")
    io.write_csv(io.stamp(pd.DataFrame(summ_rows)), C.OUT_ROOT / "wtp_summary.csv")
    io.write_csv(io.stamp(pd.DataFrame(el_rows)), C.OUT_ROOT / "wtp_elasticity.csv")

    # models: start (anchoring) effect and segment x fee (clustered by respondent)
    coef_rows = []
    hyd = ok[ok.city == "hyd"].copy()
    hyd["start40"] = (hyd.wtp_start == 40).astype(int)
    specs = {"wtp_start_effect": ("accept_imputed ~ fee_inr * start40", hyd)}
    seg = hyd[hyd.seg_occupation.isin(C.H6_GROUPS)].copy()
    seg["prof"] = (seg.seg_occupation == "working_professional").astype(int)
    if seg.resp_id.nunique() >= 2 * C.MIN_N_GROUP:
        specs["wtp_fee_x_segment"] = ("accept_imputed ~ fee_inr * prof + start40", seg)
    for mid, (formula, data) in specs.items():
        try:
            r = smf.logit(formula, data=data).fit(disp=0, cov_type="cluster",
                                                  cov_kwds={"groups": pd.factorize(data.resp_id)[0]})
        except Exception as e:                          # perfect separation etc.
            coef_rows.append({"model_id": mid, "term": "", "notes": f"fit_failed: {e}"})
            continue
        ci = r.conf_int()
        for t in r.params.index:
            coef_rows.append({"model_id": mid, "model_type": "logit_clustered", "outcome": "accept_imputed",
                              "segment": "hyd", "term": t, "estimate": r.params[t], "std_error": r.bse[t],
                              "ci_low": ci.loc[t, 0], "ci_high": ci.loc[t, 1], "odds_ratio": np.exp(r.params[t]),
                              "or_ci_low": np.exp(ci.loc[t, 0]), "or_ci_high": np.exp(ci.loc[t, 1]),
                              "p_value": r.pvalues[t], "n_resp": data.resp_id.nunique(), "n_obs": len(data),
                              "ci_method": "cluster_robust_resp", "code_ref": "09_analysis/08_wtp_curves.py"})
    io.write_csv(io.stamp(pd.DataFrame(coef_rows)), C.OUT_ROOT / "wtp_model_coefs.csv")


if __name__ == "__main__":
    main()
