"""Step 6 (run after 07-12): hypothesis tests tied to C_hypothesis_tree.md; Holm across the ★ set.

Each test returns estimate, CI, n, p (if applicable), effect size, threshold, verdict.
Verdicts: SUPPORTED / REJECTED / INCONCLUSIVE / NOT TESTABLE (universal rule, section 0).
Outputs: OUT_ROOT/hypothesis_results.csv, MART_DIR/dim_hypothesis.csv
"""
from __future__ import annotations

from datetime import date

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

import config as C
import utils_io as io
import utils_stats as st
from hyp_tests_ownly import ownly_tests

R = []


def rec(hyp, star, statement, test, est=np.nan, lo=np.nan, hi=np.nan, n=np.nan, p=np.nan, effect=np.nan,
        threshold="", verdict="NOT TESTABLE", dataset="fact_survey_respondent", notes=""):
    R.append(dict(hyp_id=hyp, confirmatory=star, statement=statement, test=test, estimate=est, ci_low=lo, ci_high=hi,
                  n=n, p_value=p, effect_size=effect, threshold=threshold, verdict_rule=verdict, dataset=dataset, notes=notes))


def prop_vs(hyp, star, stmt, s, thr, direction="greater"):
    s = s.dropna()
    n, k = len(s), int(s.sum())
    p_hat, lo, hi = st.wilson(k, n)
    alt = "greater" if direction == "greater" else "less"
    p = stats.binomtest(k, n, thr, alternative=alt).pvalue if n else np.nan
    rec(hyp, star, stmt, "Wilson CI vs threshold; exact binomial", p_hat, lo, hi, n, p, p_hat - thr if n else np.nan,
        f"{direction} {thr}", st.verdict_ci(lo, hi, thr, direction, n, C.MIN_N_PROP))


def mw(hyp, star, stmt, x, y, label, floor=C.FLOOR_R, expect_positive=True):
    m = st.mann_whitney(x, y)
    n = m["n1"] + m["n2"]
    if min(m["n1"], m["n2"]) < C.MIN_N_GROUP:
        verdict = "NOT TESTABLE"
    elif m["p"] < C.ALPHA and ((m["r_rb"] >= floor) if expect_positive else (m["r_rb"] <= -floor)):
        verdict = "SUPPORTED"
    elif m["p"] < C.ALPHA:
        verdict = "INCONCLUSIVE"      # significant but below business floor or wrong direction -> see notes
    else:
        verdict = "INCONCLUSIVE"
    rec(hyp, star, stmt, f"Mann-Whitney ({label}); rank-biserial r", m["hl_shift"], np.nan, np.nan, n, m["p"],
        m["r_rb"], f"r {'>=' if expect_positive else '<='} {'' if expect_positive else '-'}{floor}", verdict,
        notes=f"n1={m['n1']}, n2={m['n2']}; null = no LARGE difference detected, not 'no difference'")


def main():
    df = io.read_csv(C.OUT_ROOT / "survey_respondent_full.csv", low_memory=False)
    hyd = df[df.city == "hyd"]
    dce = io.read_csv(C.OUT_ROOT / "dce_hypothesis_inputs.csv", required=False)
    audit = io.read_csv(C.OUT_ROOT / "audit_summary.csv", required=False)
    transfer = io.read_csv(C.OUT_ROOT / "transfer_metrics.csv", required=False)
    wtp = io.read_csv(C.MART_DIR / "fact_wtp_long.csv", required=False)
    A = audit.set_index("metric") if audit is not None else None

    prop_vs("H1.1", True, "Fee friction common (>=50% sometimes+)", hyd.fee_reconsider_ge3, 0.5)
    sub = hyd[["price_set", "reliability_set"]].dropna()
    if len(sub) >= C.MIN_N_PROP:
        m = st.mcnemar_paired(sub.price_set, sub.reliability_set)
        rec("H1.2", True, "Price pain share >= reliability pain share", "McNemar exact; Agresti-Min CI", m["diff"],
            m["ci_low"], m["ci_high"], m["n"], m["p"], m["diff"], ">= 0 (floor 10pp)",
            st.verdict_ci(m["ci_low"], m["ci_high"], 0, "greater", m["n"], C.MIN_N_PROP))
    else:
        rec("H1.2", True, "Price pain share >= reliability pain share", "McNemar", n=len(sub))
    prop_vs("H1.3", False, "Menu-markup belief >=50% (belief, not fact)", hyd.markup_top2, 0.5)
    prop_vs("H1.4", False, "Price-driven abandonment >=30%", hyd.abandon_price_ge2, 0.3)
    prop_vs("H1.5", False, "High offer dependency (>=40% 'most/all')", hyd.high_offer_dependency, 0.4)
    mw("H1.6", False, "PPI higher in frequent vs occasional", hyd.ppi[hyd.seg_freq == "frequent"],
       hyd.ppi[hyd.seg_freq == "occasional"], "frequent vs occasional")
    s = st.spearman_boot(hyd.ppi, hyd.sri, seed_offset=61)
    s2 = st.spearman_boot(hyd.ppi, hyd.sri_no_intent, seed_offset=62)
    rec("H1.7", True, "PPI associated with SRI (rho>=0.20)", "Spearman, bootstrap CI", s["rho"], s["ci_low"],
        s["ci_high"], s["n"], s["p"], s["rho"], ">= 0.20", st.verdict_ci(s["ci_low"], s["ci_high"], 0.2, "greater", s["n"], C.MIN_N_PROP),
        notes=f"robustness without intent component: rho={s2['rho']:.3f} [{s2['ci_low']:.3f},{s2['ci_high']:.3f}]")

    def dce_get(metric, seg="all"):
        if dce is None:
            return None
        r = dce[(dce.metric == metric) & (dce.segment == seg)]
        return r.iloc[0] if len(r) else None

    g = dce_get("choice_prob_gain_30inr")
    if g is not None:
        verdict = "NOT TESTABLE" if "below_min_n" in str(g.status) else (
            "SUPPORTED" if g.p_price < C.ALPHA and g.value >= 0.10 else "REJECTED")
        rec("H2.1", True, "₹30 lower total -> >=10pp choice gain", "Conditional logit (pairwise diff), clustered", g.value,
            n=g.n_resp, p=g.p_price, effect=g.value, threshold=">= 0.10", verdict=verdict, dataset="fact_dce_long", notes=g.status)
    else:
        rec("H2.1", True, "₹30 lower total -> >=10pp choice gain", "Conditional logit", dataset="fact_dce_long")
    prop_vs("H2.2", False, "Simple bill preferred at equal totals (>=60% of those with a preference)",
            hyd.get("bill_s1_simple_chosen", pd.Series(dtype=float)), 0.6)
    med_thr = st.boot_median_ci(hyd.dec_switch_threshold_inr, seed_offset=63)
    if A is not None and "median_saving_vs_cheapest_inr" in A.index:
        a = A.loc["median_saving_vs_cheapest_inr"]
        verdict = "SUPPORTED" if a.ci_low >= med_thr[0] else ("REJECTED" if a.ci_high < med_thr[1] else "INCONCLUSIVE")
        met = (hyd.dec_switch_threshold_inr <= a.value).astype(float).where(hyd.dec_switch_threshold_inr.notna() | hyd.dec_switch_no_amount.eq(1))
        met = met.fillna(0).where(hyd.dec_switch_threshold_inr.notna() | hyd.dec_switch_no_amount.eq(1))
        rec("H2.3", True, "Audit median saving >= survey required saving", "Bootstrap medians (audit clustered by restaurant)",
            a.value, a.ci_low, a.ci_high, a.n, effect=a.value - med_thr[0], threshold=f"survey median ₹{med_thr[0]}",
            verdict=verdict, dataset="fact_audit_pairs + survey",
            notes=f"survey median [{med_thr[1]},{med_thr[2]}]; share threshold met = {met.mean():.3f} (n={met.notna().sum()})")
    else:
        rec("H2.3", True, "Audit median saving >= survey required saving", "needs audit", dataset="fact_audit_pairs")
    nd = hyd.get("bill_s2_nodiscount_chosen", pd.Series(dtype=float)).dropna()
    disc = 1 - nd
    if len(disc):
        p_hat, lo, hi = st.wilson(int(disc.sum()), len(disc))
        rec("H2.4", False, "Discount framing preferred at equal totals", "Exact binomial vs 50% (two-sided)", p_hat, lo, hi,
            len(disc), stats.binomtest(int(disc.sum()), len(disc), 0.5).pvalue, p_hat - 0.5, "!= 0.5",
            st.verdict_ci(lo, hi, 0.5, "greater", len(disc), C.MIN_N_PROP))
    prop_vs("H2.5", False, "Blind-concept top-box >=20% (first exposure)", hyd.bt_topbox, 0.2)

    for hyp, metric, thr, direction, stmt in [
            ("H3.1", "wtp_10min_faster_inr", 30, "less", "Value of 10 min < ₹30"),
            ("H4.1", "wtp_reliability_1in10_vs_3in10_inr", 30, "greater", "Reliability step worth > ₹30")]:
        g = dce_get(metric)
        if g is not None and pd.notna(g.value):
            rec(hyp, True, stmt, "Conditional logit WTP, Krinsky-Robb", g.value, g.ci_low, g.ci_high, g.n_resp, g.p_price,
                g.value, f"{direction} ₹{thr}", st.verdict_ci(g.ci_low, g.ci_high, thr, direction, g.n_resp, C.MIN_N_DCE),
                "fact_dce_long", str(g.status))
        else:
            rec(hyp, True, stmt, "Conditional logit WTP", dataset="fact_dce_long", notes="no model or price not significant")
    rss = st.boot_median_ci(hyd.rss, seed_offset=64)
    rec("H4.1b", False, "Median RSS >= 50", "Bootstrap median", *rss, int(hyd.rss.notna().sum()), threshold=">= 50",
        verdict=st.verdict_ci(rss[1], rss[2], 50, "greater", int(hyd.rss.notna().sum()), C.MIN_N_PROP))
    mw("H4.3", False, "RSS higher after incidents", hyd.rss[hyd.pain_incident_any_3m == 1], hyd.rss[hyd.pain_incident_any_3m == 0], "incident vs none")
    g = dce_get("wtp_most_vs_few_restaurants_inr")
    if g is not None and pd.notna(g.value) and A is not None and "median_saving_vs_cheapest_inr" in A.index:
        thr = A.loc["median_saving_vs_cheapest_inr", "value"]
        rec("H5.1", True, "Selection loss worth more than audit median saving", "WTP KR CI vs audit median", g.value, g.ci_low,
            g.ci_high, g.n_resp, g.p_price, g.value - thr, f"> ₹{thr:.1f}", st.verdict_ci(g.ci_low, g.ci_high, thr, "greater", g.n_resp, C.MIN_N_DCE),
            "fact_dce_long + fact_audit_pairs")
    else:
        rec("H5.1", True, "Selection loss worth more than audit median saving", "needs DCE WTP + audit")
    ownly_tests(rec, prop_vs, mw, df, hyd, dce_get, A, transfer, wtp)

    res = pd.DataFrame(R)
    star = res.confirmatory & res.p_value.notna()
    res["p_holm_confirmatory"] = np.nan
    res.loc[star, "p_holm_confirmatory"] = st.holm(res.loc[star, "p_value"].tolist())
    res["verdict"] = res.verdict_rule
    res["data_status"] = C.DATA_STATUS
    io.write_csv(res, C.OUT_ROOT / "hypothesis_results.csv")
    dim = pd.DataFrame({"hyp_id": res.hyp_id, "family": res.hyp_id.str.extract(r"^(H\d+)")[0], "statement": res.statement,
                        "independent_var": "", "dependent_var": "", "segment": "", "method": res.dataset, "test": res.test,
                        "threshold": res.threshold, "required_dataset": res.dataset, "status": res.verdict,
                        "result_summary": res.apply(lambda r: f"est={r.estimate:.3g} [{r.ci_low:.3g}, {r.ci_high:.3g}], p={r.p_value:.3g}, p_holm={r.p_holm_confirmatory:.3g}", axis=1),
                        "effect_size": res.effect_size, "ci": res.apply(lambda r: f"[{r.ci_low:.3g}, {r.ci_high:.3g}]", axis=1),
                        "n": res.n, "evidence_ids": res.dataset, "implication_if_validated": "see C_hypothesis_tree.md",
                        "implication_if_rejected": "see C_hypothesis_tree.md", "last_updated": str(date.today()),
                        "data_status": C.DATA_STATUS})
    io.write_csv(dim, C.MART_DIR / "dim_hypothesis.csv")
    print(res[["hyp_id", "confirmatory", "estimate", "ci_low", "ci_high", "n", "verdict"]].to_string())


if __name__ == "__main__":
    main()
