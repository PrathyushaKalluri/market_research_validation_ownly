"""Step 9: Bengaluru -> Hyderabad matched comparison (E section 3; H9.2, H9.4).

* Populations: 'non_users' (PRIMARY: own_status in unaware / aware_not_tried / not_asked) and 'all'
  (secondary; confounded by the Bengaluru Ownly-user quota).
* Post-stratification: Bengaluru reweighted to Hyderabad composition on seg_occupation (student,
  working_professional) x seg_freq (3 levels), collapsed to 2x2 (occasional vs regular+frequent)
  if any cell has n < POSTSTRAT_MIN_CELL in either city. Weights are fixed at full-sample values
  during the bootstrap (stated simplification).
* Verdicts: need metrics use non-inferiority (HYD - BLR lower CI > margin); lock-in metrics test
  "not stronger" (HYD - BLR upper CI < +margin).
Outputs: OUT_ROOT/transfer_metrics.csv, composition_check.csv; updates w_match_hyd in the mart.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import config as C
import utils_io as io
import utils_stats as st

NON_USER = {"unaware", "aware_not_tried", "not_asked"}
METRICS = [  # variable, kind, direction ('need' = higher in HYD is good for transfer; 'lock' = higher is bad)
    ("ppi", "index", "need"), ("sri_no_intent", "index", "need"), ("fee_reconsider_ge3", "prop", "need"),
    ("abandon_price_ge2", "prop", "need"), ("markup_top2", "prop", "need"), ("beh_multihome", "prop", "need"),
    ("beh_any_subscription", "prop", "lock"), ("habit_lock_top2", "prop", "lock"), ("adi_high", "prop", "lock"),
    ("exp_eta_max_dinner_min", "minutes", "need")]


def cells(df, collapse):
    f = df.seg_freq.replace({"frequent": "regular_plus", "regular": "regular_plus"}) if collapse else df.seg_freq
    return df.seg_occupation + "|" + f


def wmean(x, w):
    m = x.notna() & w.notna()
    return np.average(x[m], weights=w[m]) if m.any() and w[m].sum() > 0 else np.nan


def main():
    df = io.read_csv(C.OUT_ROOT / "survey_respondent_full.csv", low_memory=False)
    if set(df.city.unique()) != {"hyd", "blr"}:
        print("  both cities required — skipping")
        return
    df["habit_lock_top2"] = (df.dec_habit_lock >= 4).astype(float).where(df.dec_habit_lock.notna())
    df = df[df.seg_occupation.isin(C.H6_GROUPS) & df.seg_freq.notna()].copy()
    rows, comp, weights = [], [], []
    for pop in ("non_users", "all"):
        d = df[df.own_status.isin(NON_USER)] if pop == "non_users" else df
        counts = pd.crosstab(d.seg_occupation + "|" + d.seg_freq, d.city)
        collapse = bool((counts.reindex(columns=["hyd", "blr"]).fillna(0) < C.POSTSTRAT_MIN_CELL).any().any())
        d = d.assign(cell=cells(d, collapse))
        share = pd.crosstab(d.cell, d.city, normalize="columns")
        ratio = (share["hyd"] / share["blr"]).replace([np.inf], np.nan)
        d["w"] = np.where(d.city == "hyd", 1.0, d.cell.map(ratio))
        uncovered = float(share.loc[share["blr"] == 0, "hyd"].sum()) if (share["blr"] == 0).any() else 0.0
        if pop == "non_users":
            weights.append(d[["resp_id", "w"]])
        for var in ["seg_occupation", "seg_freq", "dem_living", "scr_age_band"]:
            if var not in d:
                continue
            for lvl in d[var].dropna().unique():
                x = (d[var] == lvl).astype(float)
                ph, pb = x[d.city == "hyd"].mean(), x[d.city == "blr"].mean()
                sd = np.sqrt((ph * (1 - ph) + pb * (1 - pb)) / 2)
                comp.append({"population": pop, "variable": var, "level": lvl, "hyd_share": ph, "blr_share": pb,
                             "smd": (ph - pb) / sd if sd > 0 else 0.0, "imbalanced_smd_gt_0_2": abs((ph - pb) / sd) > 0.2 if sd > 0 else False})
        g = st.rng(900)
        H, B = d[d.city == "hyd"], d[d.city == "blr"]
        for var, kind, direction in METRICS:
            if var not in d:
                continue
            est_w = wmean(H[var], H.w) - wmean(B[var], B.w)
            est_u = H[var].mean() - B[var].mean()
            boots = []
            for _ in range(min(C.N_BOOT, 2000)):
                hh = H.iloc[g.integers(0, len(H), len(H))]
                bb = B.iloc[g.integers(0, len(B), len(B))]
                boots.append(wmean(hh[var], hh.w) - wmean(bb[var], bb.w))
            lo, hi = np.nanpercentile(boots, [2.5, 97.5])
            margin = C.NONINF_MARGIN_INDEX if kind == "index" else (-5.0 if kind == "minutes" else C.NONINF_MARGIN_PP)
            if direction == "need":
                verdict = "NON_INFERIOR" if lo > margin else ("INFERIOR" if hi < margin else "INCONCLUSIVE")
            else:
                verdict = "NOT_STRONGER" if hi < -margin else ("STRONGER" if lo > -margin else "INCONCLUSIVE")
            rows.append({"population": pop, "metric": var, "kind": kind, "direction": direction,
                         "hyd_n": int(H[var].notna().sum()), "blr_n": int(B[var].notna().sum()),
                         "hyd_value": H[var].mean(), "blr_value_weighted": wmean(B[var], B.w),
                         "blr_value_unweighted": B[var].mean(), "diff_weighted": est_w, "ci_low": lo, "ci_high": hi,
                         "diff_unweighted": est_u, "robust_sign": np.sign(est_w) == np.sign(est_u),
                         "margin": margin, "verdict": verdict, "cells_collapsed_2x2": collapse,
                         "hyd_share_in_cells_absent_in_blr": uncovered})
    io.write_csv(io.stamp(pd.DataFrame(rows)), C.OUT_ROOT / "transfer_metrics.csv")
    io.write_csv(io.stamp(pd.DataFrame(comp)), C.OUT_ROOT / "composition_check.csv")
    mart = io.read_csv(C.MART_DIR / "fact_survey_respondent.csv", low_memory=False)
    wmap = pd.concat(weights).set_index("resp_id").w
    mart["w_match_hyd"] = mart.resp_id.map(wmap)
    io.write_csv(mart, C.MART_DIR / "fact_survey_respondent.csv")


if __name__ == "__main__":
    main()
