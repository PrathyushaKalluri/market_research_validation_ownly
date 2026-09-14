"""Hypothesis tests H6-H12 (split from 06_hypothesis_tests.py to keep files small)."""
from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

import config as C
import utils_stats as st

ORDERS_MID = {1: 2, 2: 5.5, 3: 11.5, 4: 18}


def ownly_tests(rec, prop_vs, mw, df, hyd, dce_get, A, transfer, wtp):
    stu, pro = hyd[hyd.seg_occupation == "student"], hyd[hyd.seg_occupation == "working_professional"]
    mw("H6.1", True, "Students have higher PPI", stu.ppi, pro.ppi, "student vs professional")
    adj = hyd[hyd.seg_occupation.isin(C.H6_GROUPS)][["ppi", "seg_occupation", "seg_freq", "dem_living"]].dropna()
    if len(adj) >= 2 * C.MIN_N_GROUP:
        X = pd.get_dummies(adj[["seg_freq", "dem_living"]].astype(str), drop_first=True).astype(float)
        X["student"] = (adj.seg_occupation == "student").astype(float)
        ols = sm.OLS(adj.ppi, sm.add_constant(X)).fit(cov_type="HC3")
        R_last = f"adjusted student coef={ols.params['student']:.2f} [{ols.conf_int().loc['student', 0]:.2f}, {ols.conf_int().loc['student', 1]:.2f}] (exploratory)"
        rec("H6.1-adj", False, "Students higher PPI, adjusted for frequency & living", "OLS HC3", ols.params["student"],
            ols.conf_int().loc["student", 0], ols.conf_int().loc["student", 1], len(adj), ols.pvalues["student"],
            threshold="> 0", verdict=st.verdict_ci(ols.conf_int().loc["student", 0], ols.conf_int().loc["student", 1], 0, "greater", len(adj), 2 * C.MIN_N_GROUP),
            notes=R_last)
    mw("H6.2", False, "Students have lower fee WTP", stu.wtp_max_fee, pro.wtp_max_fee, "student vs professional", expect_positive=False)
    g = dce_get("wtp_reliability_1in10_vs_3in10_inr", "prof_minus_student")
    if g is not None:
        rec("H6.3", True, "Professionals value reliability more (WTP diff > 0)", "Segment-interacted CL, KR CI of difference",
            g.value, g.ci_low, g.ci_high, g.n_resp, np.nan, g.value, "> 0",
            st.verdict_ci(g.ci_low, g.ci_high, 0, "greater", g.n_resp, 2 * C.MIN_N_GROUP), "fact_dce_long", str(g.status))
    else:
        rec("H6.3", True, "Professionals value reliability more", "Segment-interacted CL", dataset="fact_dce_long")
    val = {}
    for name, s in (("student", stu), ("working_professional", pro)):
        val[name] = s.scr_orders_4wk.map(ORDERS_MID).median() * s.beh_last_order_total.median() if len(s) else np.nan
    ratio = val["working_professional"] / val["student"] if val["student"] else np.nan
    rec("H6.4", False, "Commercial value ratio professional/student (orders x AOV, medians)", "Descriptive", ratio,
        n=len(stu) + len(pro), threshold=">= 1.3 or <= 1/1.3", verdict="INCONCLUSIVE" if pd.notna(ratio) else "NOT TESTABLE",
        notes="descriptive; no inferential claim")

    first = hyd[hyd.meta_brand_arm.notna()]
    for scope, d in (("all", first), ("unaware", first[first.own_aware_any == 0])):
        b, u = d[d.meta_brand_arm == "branded"], d[d.meta_brand_arm == "blind"]
        m = st.mann_whitney(b.bt_trial_intent, u.bt_trial_intent)
        kb, nb = int(b.bt_t2b.sum()), int(b.bt_t2b.notna().sum())
        ku, nu = int(u.bt_t2b.sum()), int(u.bt_t2b.notna().sum())
        diff = st.newcombe_diff(kb, nb, ku, nu) if nb and nu else (np.nan,) * 3
        verdict = "NOT TESTABLE" if min(nb, nu) < C.MIN_N_GROUP else ("SUPPORTED" if m["p"] < C.ALPHA else "INCONCLUSIVE")
        rec("H7.1" if scope == "all" else "H7.1-unaware", scope == "all", f"Branding changes trial intent ({scope}; two-sided)",
            "Mann-Whitney + top-2 diff (Newcombe)", diff[0], diff[1], diff[2], nb + nu, m["p"], m["r_rb"],
            "two-sided; floor 10pp", verdict, notes="null = no large effect detected (MDD ~20pp at 100/arm)")
    rel = lambda s: s.replace(98, np.nan)
    m = st.mann_whitney(rel(first[first.meta_brand_arm == "branded"].bt_expected_reliability),
                        rel(first[first.meta_brand_arm == "blind"].bt_expected_reliability))
    rec("H7.2", False, "Branding changes expected reliability (two-sided)", "Mann-Whitney", np.nan, n=m["n1"] + m["n2"],
        p=m["p"], effect=m["r_rb"], verdict="INCONCLUSIVE" if m["n1"] >= C.MIN_N_GROUP else "NOT TESTABLE")
    blind = first[first.meta_brand_arm == "blind"]
    w = st.wilcoxon_paired(blind.br_trial_intent, blind.bt_trial_intent)
    rec("H7.4", False, "Within-subject reveal shift (blind arm)", "Wilcoxon signed-rank", np.nan, n=w["n"], p=w["p"],
        effect=w["r_mp"], verdict="INCONCLUSIVE" if w["n"] >= C.MIN_N_GROUP else "NOT TESTABLE", notes="secondary; demand effects")

    fee = C.OWNLY_OBSERVED_FEE_INR
    if fee is None and A is not None and "ownly_observed_delivery_fee_inr" in A.index:
        fee = A.loc["ownly_observed_delivery_fee_inr", "value"]
    if fee is not None and pd.notna(fee) and wtp is not None:
        grid = int(np.clip(round(fee / 10) * 10, 0, 60))
        s = wtp[(wtp.city == "hyd") & (wtp.wtp_status == "ok") & (wtp.fee_inr == grid)].accept_imputed
        prop_vs("H8.1", True, f"Acceptance at observed Ownly fee (grid ₹{grid}) >= 50%", s, 0.5)
    else:
        rec("H8.1", True, "Acceptance at observed Ownly fee >= 50%", "needs audit-observed fee", dataset="fact_wtp_long")

    if transfer is not None:
        t = transfer[(transfer.population == "non_users") & (transfer.metric == "ppi")]
        if len(t):
            t = t.iloc[0]
            rec("H9.2", True, "Hyderabad PPI not materially weaker than Bengaluru (non-users, weighted)",
                "Weighted difference, bootstrap CI, non-inferiority", t.diff_weighted, t.ci_low, t.ci_high, t.hyd_n + t.blr_n,
                threshold="lower CI > -10", verdict=st.verdict_ci(t.ci_low, t.ci_high, C.NONINF_MARGIN_INDEX, "greater",
                                                                  min(t.hyd_n, t.blr_n), C.MIN_N_GROUP),
                dataset="transfer_metrics", notes=f"robust sign={t.robust_sign}; collapsed={t.cells_collapsed_2x2}")
    else:
        rec("H9.2", True, "Hyderabad PPI not materially weaker", "needs both cities", dataset="transfer_metrics")

    prop_vs("H10.1", True, "ADI>=75 share >= 40%", hyd.adi_high, 0.4)
    if A is not None and "ownly_listing_coverage_of_frame" in A.index:
        a = A.loc["ownly_listing_coverage_of_frame"]
        rec("H10.4", False, "Ownly coverage of audit frame >= 60%", "Wilson", a.value, a.ci_low, a.ci_high, a.n,
            threshold=">= 0.60", verdict=st.verdict_ci(a.ci_low, a.ci_high, 0.6, "greater", a.n, 10), dataset="fact_audit_obs")

    aware = hyd[hyd.aware_2wk_plus == 1].own_tried_bin.dropna()
    intent = hyd[hyd.meta_brand_arm == "blind"].bt_t2b.dropna()
    if len(aware) and len(intent):
        d = st.newcombe_diff(int(aware.sum()), len(aware), int(intent.sum()), len(intent))
        _, p = st.two_prop_test(int(aware.sum()), len(aware), int(intent.sum()), len(intent))
        rec("H11.3", True, "Aware(>=2wk)->tried share lower than blind top-2 intent", "Two proportions (descriptive calibration)",
            d[0], d[1], d[2], len(aware) + len(intent), p, d[0], "< 0",
            st.verdict_ci(d[1], d[2], 0, "less", min(len(aware), len(intent)), C.MIN_N_GROUP))
    else:
        rec("H11.3", True, "Aware->tried lower than intent", "Two proportions")

    own = df[df.own_repeat.notna()].copy()
    preds = ["own_perceived_savings", "own_reliability_rating", "own_found_restaurants", "own_order_accuracy", "own_trust"]
    own["own_perceived_savings"] = own.own_perceived_savings.replace(98, np.nan)
    own["city_hyd"] = (own.city == "hyd").astype(float)
    d = own[preds + ["city_hyd", "own_repeat"]].dropna()
    events = min(d.own_repeat.sum(), len(d) - d.own_repeat.sum()) if len(d) else 0
    use = preds if events / (len(preds) + 1) >= C.MIN_EPV else ["own_reliability_rating", "own_perceived_savings", "own_found_restaurants"]
    if len(d) and events / (len(use) + 1) >= C.MIN_EPV:
        Z = (d[use] - d[use].mean()) / d[use].std(ddof=0)
        X = sm.add_constant(pd.concat([Z, d[["city_hyd"]]], axis=1))
        fit = sm.Logit(d.own_repeat, X).fit(disp=0)
        g = st.rng(1212)
        diffs = []
        for _ in range(500):
            s = d.iloc[g.integers(0, len(d), len(d))]
            Zs = (s[use] - s[use].mean()) / s[use].std(ddof=0)
            try:
                fs = sm.Logit(s.own_repeat, sm.add_constant(pd.concat([Zs, s[["city_hyd"]]], axis=1))).fit(disp=0)
                diffs.append(fs.params["own_reliability_rating"] - fs.params["own_perceived_savings"])
            except Exception:
                continue
        lo, hi = np.percentile(diffs, [2.5, 97.5]) if diffs else (np.nan, np.nan)
        est = fit.params["own_reliability_rating"] - fit.params["own_perceived_savings"]
        rec("H12.1", True, "Reliability predicts repeat more than savings (std. log-odds diff > 0)",
            "Logistic (standardised), bootstrap CI of coefficient difference", est, lo, hi, len(d),
            fit.pvalues["own_reliability_rating"], est, "> 0", st.verdict_ci(lo, hi, 0, "greater", len(d), 30),
            "OWNLY_POOLED", f"events={events}; EPV={events / (len(use) + 1):.1f}; predictors={use}; associations, not causes")
    else:
        rec("H12.1", True, "Reliability predicts repeat more than savings", "Logistic", n=len(d),
            dataset="OWNLY_POOLED", notes=f"EPV too low (events={events}) -> bivariate only")
    t = pd.crosstab(own.unresolved_issue, own.own_lapsed)
    if t.shape == (2, 2):
        p = stats.fisher_exact(t.values)[1]
        rr = (t.loc[1, 1] / t.loc[1].sum()) / (t.loc[0, 1] / t.loc[0].sum()) if t.loc[0, 1] else np.nan
        rec("H12.2", False, "Unresolved issue -> lapse", "Fisher exact; risk ratio", rr, n=int(t.values.sum()), p=p, effect=rr,
            threshold="RR > 1", verdict="SUPPORTED" if p < C.ALPHA and rr > 1 else "INCONCLUSIVE", dataset="OWNLY_POOLED")
    s = st.spearman_boot(own.own_found_restaurants, own.own_share_of_orders, seed_offset=123)
    rec("H12.3", False, "Found restaurants ~ share of orders", "Spearman bootstrap", s["rho"], s["ci_low"], s["ci_high"], s["n"],
        s["p"], s["rho"], "> 0", st.verdict_ci(s["ci_low"], s["ci_high"], 0, "greater", s["n"], 30), "OWNLY_POOLED")
    h = own[own.city == "hyd"]
    t = pd.crosstab(h.offer_trigger, h.own_lapsed)
    if t.shape == (2, 2):
        rec("H12.4", False, "Offer-driven trial -> lapse (Hyderabad)", "Fisher exact", n=int(t.values.sum()),
            p=stats.fisher_exact(t.values)[1], verdict="INCONCLUSIVE", dataset="HYD_OWNLY", notes="small n expected")
