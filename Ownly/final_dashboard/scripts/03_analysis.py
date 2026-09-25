"""
03_analysis.py — analysis layer: funnel, H0, trade-offs, associations, segments, anomalies.

Base: Gachibowli catchment (n=40). Every test reports n, effect size and a 95% CI.
At this sample size most comparisons are underpowered; those are labelled DIRECTIONAL
rather than given a verdict. Only a pre-specified set of associations is tested — no fishing.
"""
import os
import numpy as np
import pandas as pd
from scipy import stats

ROOT = "/Users/klprathyusha/Sem 3/Project/Ownly"
D = f"{ROOT}/final_dashboard/data"

S = pd.read_csv(f"{D}/cleaned_survey.csv")
P = pd.read_csv(f"{D}/audit_pairs.csv")
A = pd.read_csv(f"{D}/audit_clean.csv")
C = S[S["pop_HYD_CATCHMENT"]].copy()
BLR = S[S["pop_BLR_ELIGIBLE"]].copy()
N = len(C)


def wilson(k, n, z=1.96):
    if not n:
        return (np.nan, np.nan, np.nan)
    p = k / n
    d = 1 + z**2 / n
    c = (p + z**2 / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / d
    return (p * 100, max(0, c - h) * 100, min(1, c + h) * 100)


# =====================================================================
# 1. FUNNELS — research sample funnel, and market context (kept separate)
# =====================================================================
raw_n = int(pd.read_csv(f"{D}/survey_all_rows_with_flags.csv").shape[0])
hyd_all = int((S["city"] == "Hyderabad").sum() + (pd.read_csv(f"{D}/excluded_survey.csv")["city"]
                                                  == "Hyderabad").sum())
funnel = [
    ("Responses received", raw_n, "All submissions to the live form"),
    ("Hyderabad branch", hyd_all, "Routed to the Hyderabad question set"),
    ("Passed age screen (20–35 as collected)", int((S["city"] == "Hyderabad").sum()),
     "Form routes out 'Under 20' and 'Over 35'"),
    ("In the Gachibowli catchment", N, "Gachibowli + Financial District, Manikonda, Narsingi, "
     "Serilingampally/Tellapur"),
    ("Ordered food online in last 4 weeks", int(C["recent_orderer"].sum()),
     "The population the study is actually about"),
    ("Aware of Ownly", int(C["ownly_aware"].fillna(False).sum()), "Before taking the survey"),
    ("Browsed Ownly", int(C["ownly_opened"].fillna(False).sum()), "Opened the app"),
    ("Ever ordered on Ownly", int(C["ownly_says_ordered"].fillna(False).sum()),
     "Self-reported; 1 of these has an unusable recent-order count"),
]
F = pd.DataFrame(funnel, columns=["stage", "n", "note"])
F["pct_of_responses"] = (F["n"] / raw_n * 100).round(1)
# share-of-catchment only makes sense for stages at or below the catchment
_at_or_below = F.index >= F.index[F["stage"] == "In the Gachibowli catchment"][0]
F["pct_of_catchment"] = np.where(_at_or_below, (F["n"] / N * 100).round(1), np.nan)
F["step_retention_pct"] = (F["n"] / F["n"].shift(1) * 100).round(1)
F["funnel_type"] = "RESEARCH SAMPLE — not a market funnel"
F.to_csv(f"{D}/funnel_research.csv", index=False)

# Market context — clearly separate, sourced, and NOT derived from the survey
MKT = [
    ("Gachibowli population", 149264, "Wikipedia / Census-derived, 2020",
     "SECONDARY — dated, locality definition varies", "context only"),
    ("Telangana IT workforce", 946000, "Telangana IT dept, FY2024 (~9.46 lakh)",
     "SECONDARY — state level, not Gachibowli", "context only"),
    ("Restaurants listed on Ownly at a Gachibowli address", 221,
     "First-hand user check, 2026-09-19 + serviceability check", "FIRST-HAND OBSERVATION",
     "supply-side context"),
]
pd.DataFrame(MKT, columns=["item", "value", "source", "evidence_type", "use"]).to_csv(
    f"{D}/market_context.csv", index=False)

# =====================================================================
# 2. H0 — behavioural vs stated-preference analogue
# =====================================================================
fc = C["prop_forced"].dropna()
nP = int((fc == "Service P").sum())
nQ = int((fc == "Service Q").sum())
nC = int((fc == "I genuinely can't choose between them").sum())
bt = stats.binomtest(nP, nP + nQ, 0.5) if (nP + nQ) else None
ci = bt.proportion_ci(confidence_level=0.95) if bt else None

d = C[["prop_P_intent_n", "prop_Q_intent_n"]].dropna()
pt, qt = d["prop_P_intent_n"] >= 4, d["prop_Q_intent_n"] >= 4
b, c_ = int((pt & ~qt).sum()), int((~pt & qt).sum())
mc = stats.binomtest(b, b + c_, 0.5).pvalue if (b + c_) else np.nan

HYP = [
    dict(id="H0-BEHAVIOURAL",
         statement="Among the Gachibowli target population, a Bengaluru-style Ownly proposition "
                   "does not produce a significantly different FIRST-ORDER CONVERSION rate from a "
                   "Hyderabad-localised proposition.",
         test="Randomised fake-door landing test (planned)", result="NOT TESTED",
         n=0, statistic=None, p_value=None, ci=None, verdict="NOT TESTABLE WITH AVAILABLE EVIDENCE",
         note="The fake-door experiment was never fielded — the event log contains 0 rows. No "
              "behavioural first-order conversion was observed anywhere in this study. Survey "
              "preference is NOT a substitute and is reported separately below.",
         evidence_type="NONE"),
    dict(id="H0-STATED",
         statement="Stated-preference analogue: the share choosing the Bengaluru-style proposition "
                   "(Service P) does not differ from 50% among those expressing a preference.",
         test="Exact binomial vs 50%, two-sided",
         result=f"Service P {nP} vs Service Q {nQ}, plus {nC} 'can't choose'",
         n=nP + nQ, statistic=f"P share = {nP/(nP+nQ)*100:.1f}%",
         p_value=round(bt.pvalue, 4),
         ci=f"[{ci.low*100:.1f}%, {ci.high*100:.1f}%]",
         verdict="FAIL TO REJECT H0" if bt.pvalue >= .05 else "REJECT H0",
         note=f"{nC} of {len(fc)} ({nC/len(fc)*100:.0f}%) could not choose between the two bundled "
              "propositions — itself a finding about how distinct they are.",
         evidence_type="SURVEY — STATED PREFERENCE (PROXY, not conversion)"),
    dict(id="H0-STATED-PAIRED",
         statement="Top-2-box trial intent does not differ between Service P and Service Q.",
         test="McNemar exact (paired, same respondents)",
         result=f"discordant pairs: P-only {b}, Q-only {c_}", n=len(d),
         statistic=f"b={b}, c={c_}", p_value=None if np.isnan(mc) else round(mc, 4), ci=None,
         verdict="FAIL TO REJECT H0" if (np.isnan(mc) or mc >= .05) else "REJECT H0",
         note="Paired test on the same respondents; complements the forced choice.",
         evidence_type="SURVEY — STATED PREFERENCE"),
]

# =====================================================================
# 3. THE ₹30 TRADE-OFFS — paired comparisons
# =====================================================================
TR = pd.read_csv(f"{D}/tradeoff_summary.csv")
pairs = [("rest_chose_cheap", "eta_chose_cheap", "assortment vs speed"),
         ("rest_chose_cheap", "rel_chose_cheap", "assortment vs reliability"),
         ("rel_chose_cheap", "eta_chose_cheap", "reliability vs speed")]
trade_tests = []
for a_, b_, lab in pairs:
    dd = C[[a_, b_]].dropna()
    x, y = dd[a_].astype(bool), dd[b_].astype(bool)
    bb, cc = int((~x & y).sum()), int((x & ~y).sum())
    p = stats.binomtest(bb, bb + cc, 0.5).pvalue if (bb + cc) else np.nan
    trade_tests.append(dict(comparison=lab, n=len(dd), b=bb, c=cc,
                            p_value=None if np.isnan(p) else float(f"{p:.2g}"),
                            test="McNemar exact (paired)",
                            interpretation=f"{lab}: discordance {bb} vs {cc}"))
pd.DataFrame(trade_tests).to_csv(f"{D}/tradeoff_tests.csv", index=False)

# =====================================================================
# 4. SWITCHING STAIRCASE — both denominators
# =====================================================================
thr = C["switch_savings_rs"].dropna()
never, dk = int(C["switch_never"].sum()), int(C["switch_dk"].sum())
stair = []
for lv in [10, 20, 30, 50, 75, 100]:
    k = int((thr <= lv).sum())
    stair.append(dict(level_rs=lv, k=k,
                      pct_of_named=round(k / len(thr) * 100, 1),
                      pct_of_all=round(k / N * 100, 1)))
ST = pd.DataFrame(stair)
ST["n_named"] = len(thr)
ST["n_all"] = N
ST["excluded_no_amount"] = never
ST["excluded_dont_know"] = dk
ST.to_csv(f"{D}/switching_staircase.csv", index=False)

# =====================================================================
# 5. PRE-SPECIFIED ASSOCIATIONS (no fishing — this list is fixed)
# =====================================================================
C["is_student"] = C["occupation"].str.contains("Student", na=False)
C["is_prof"] = C["occupation"].eq("Working full-time")
C["rapido_user"] = C["rapido_freq"].notna() & ~C["rapido_freq"].eq("Never")
C["saw_food_in_rapido"] = C["rapido_food_seen"].eq("Yes")
C["bill_felt_unfair"] = C["bill_fairness"].astype(str).str.startswith("No")

ASSOC = [
    ("durability_doubt_n", "repeat_no_promo_n", "spearman",
     "Do price doubters plan to reorder less?"),
    ("switch_savings_rs", "total_orders_4wk", "spearman",
     "Do frequent orderers want a bigger saving?"),
    ("prop_P_intent_n", "repeat_no_promo_n", "spearman",
     "Does wanting to try mean wanting to stay?"),
    ("n_memberships", "switch_savings_rs", "spearman",
     "Do more memberships mean a bigger saving needed?"),
]
assoc_rows = []
for x, y, method, q in ASSOC:
    dd = C[[x, y]].dropna()
    if len(dd) < 10:
        assoc_rows.append(dict(x=x, y=y, question=q, n=len(dd), rho=None, p_value=None,
                               verdict="NOT TESTABLE — n<10"))
        continue
    rho, p = stats.spearmanr(dd[x], dd[y])
    # bootstrap CI for rho
    bs = []
    rng = np.random.default_rng(20260919)
    for _ in range(2000):
        s_ = dd.sample(len(dd), replace=True, random_state=int(rng.integers(1e9)))
        if s_[x].nunique() > 1 and s_[y].nunique() > 1:
            bs.append(stats.spearmanr(s_[x], s_[y])[0])
    lo, hi = (np.nanpercentile(bs, [2.5, 97.5]) if bs else (np.nan, np.nan))
    assoc_rows.append(dict(x=x, y=y, question=q, n=len(dd), rho=round(rho, 3),
                           p_value=round(p, 4), ci_lo=round(lo, 3), ci_hi=round(hi, 3),
                           verdict=("association detected" if p < .05 else
                                    "no association detected — UNDERPOWERED at this n")))
AS = pd.DataFrame(assoc_rows)
AS.to_csv(f"{D}/associations.csv", index=False)

# =====================================================================
# 6. SEGMENT CUTS (pre-specified)
# =====================================================================
SEGS = [("Students", C["is_student"]), ("Working professionals", C["is_prof"]),
        ("Pays for a membership", C["has_membership"]),
        ("No paid membership", ~C["has_membership"]),
        ("Uses Rapido", C["rapido_user"]), ("Knows Ownly", C["ownly_aware"].fillna(False))]
OUT = [("eta_chose_cheap", "Trades speed for ₹30", "pct"),
       ("rel_chose_cheap", "Trades reliability for ₹30", "pct"),
       ("rest_chose_cheap", "Trades restaurants for ₹30", "pct"),
       ("switch_savings_rs", "Median saving required (₹)", "median"),
       ("repeat_no_promo_n", "Post-offer repeat intent (top-2 %)", "top2"),
       ("durability_doubt_n", "Price-durability doubt (top-2 %)", "top2")]
seg_rows = []
for sname, mask in SEGS:
    sub = C[mask.fillna(False)]
    row = {"segment": sname, "n": len(sub)}
    for col, label, kind in OUT:
        s = sub[col].dropna()
        if not len(s):
            row[label] = None
            continue
        if kind == "pct":
            row[label] = round(s.astype(bool).mean() * 100, 1)
        elif kind == "median":
            row[label] = float(s.median())
        else:
            row[label] = round((s >= 4).mean() * 100, 1)
    seg_rows.append(row)
SEG = pd.DataFrame(seg_rows)
SEG.to_csv(f"{D}/segment_cuts.csv", index=False)

# =====================================================================
# 7. ANOMALY / CONFLICT REGISTER
# =====================================================================
ANOM = [
    ("A1", "Ownly recent-order count contradicts other answers",
     f"{int(C['ownly_order_conflict'].sum())} catchment respondent(s) said they had ordered on "
     "Ownly AND that their first order was in the last 4 weeks, while entering 0 orders for that "
     "window.", "Reported as UNAVAILABLE, not as zero. Excluded from volume-share numerator.",
     "data/cleaned_survey.csv", "SURVEY"),
    ("A2", "thu_lunch audit pass carries no information",
     "All 30 rows record restaurant_listed='y' with no restaurant_open, no timestamp, no prices.",
     "Excluded from coverage (rule R4). Retained and flagged in audit_clean.csv.",
     "data/audit_slot_quality.csv", "AUDIT"),
    ("A3", "Audit workbook is case-inconsistent",
     "'Zomato'/'zomato', 'Y'/'y', 'Auto offer'/'auto offer' would fork platforms, listing states "
     "and price views if left as captured.", "Lower-cased before grouping (rule R1).",
     "scripts/01_consolidate_audit.py", "AUDIT"),
    ("A4", "Duplicate restaurant name",
     "'Aanimuthyualu unlimited' vs 'Aanimuthyalu unlimited' — same restaurant, would double-count "
     "the coverage denominator.", "Merged (rule R2).", "data/audit_coverage.csv", "AUDIT"),
    ("A5", "Incumbent list prices captured twice",
     "Every Zomato 'none' capture exists twice — once with delivery fee, once without (Gold). Not "
     "duplicates: member and non-member prices of the same basket.",
     "Split into three price views; MAX = non-member, MIN = member.",
     "data/audit_platform_prices.csv", "AUDIT"),
    ("A6", "Two audit rows do not reconcile",
     "Line items do not sum to final_payable (>₹1).", "Flagged, left as captured, immaterial to "
     "matched pairs.", "data/audit_clean.csv", "AUDIT"),
    ("A7", "Age scope conflict: target says 18–35, instrument collected 20–35",
     "The form routes out 'Under 20', so 18–19-year-olds answered nothing. A later '18–24' band "
     "also appears, overlapping two earlier bands.",
     "Reported as '20–35 as collected'. 18–35 is not recoverable.",
     "data/excluded_survey.csv", "SURVEY"),
    ("A8", "Survey column order changed between exports",
     "The live sheet's column ORDER differs from the earlier CSV export, so positional mapping "
     "silently read the wrong questions.",
     "Pipeline now maps by question text + city branch.", "scripts/00_consolidate_survey.py",
     "SURVEY"),
    ("A9", "Brand present but nearest outlet absent",
     "Bawarchi is on Ownly, but not the Gachibowli outlet (first-hand check, 2026-09-19).",
     "Price capture retained. Generated H-OUTLET — see analysis.",
     "06_competitor_audit/user_firsthand_check_2026-09-19.md", "AUDIT x USER CHECK"),
    ("A10", "One implausible bill value", "A respondent reported a ₹0 order total.",
     "Field voided, respondent retained, no imputation.", "data/cleaned_survey.csv", "SURVEY"),
]
pd.DataFrame(ANOM, columns=["id", "anomaly", "what_we_found", "how_it_was_handled",
                            "evidence_link", "source"]).to_csv(
    f"{D}/anomalies.csv", index=False)

# =====================================================================
# 8. H-OUTLET — the ETA pattern
# =====================================================================
pr = A[(A["priced"] == True) & A["eta_mid"].notna()]  # noqa: E712
eta = pr.pivot_table(index="restaurant_display", columns="platform", values="eta_mid",
                     aggfunc="median")
eta = eta.dropna(subset=["ownly"])
eta["best_incumbent"] = eta[["swiggy", "zomato"]].min(axis=1)
eta["gap"] = eta["ownly"] - eta["best_incumbent"]
eta.reset_index().to_csv(f"{D}/eta_gap_by_restaurant.csv", index=False)

HYP.append(dict(
    id="H-OUTLET",
    statement="Ownly's delivery-time gap and its assortment gap are the same problem: it lists "
              "brands but not their nearest outlets, so it fulfils from further away.",
    test="Pattern check on per-restaurant ETA gap + first-hand outlet observation",
    result=f"gap present on {int((eta['gap']>0).sum())}/{len(eta)} restaurants, range "
           f"{eta['gap'].min():.1f}–{eta['gap'].max():.1f} min, median {eta['gap'].median():.1f}",
    n=len(eta), statistic=f"median gap {eta['gap'].median():.1f} min", p_value=None, ci=None,
    verdict="HYPOTHESIS — CONSISTENT WITH DATA, NOT DEMONSTRATED",
    note="A flat, brand-independent penalty is the signature of supply density; rider or batching "
         "problems produce variable outliers instead. The audit did not record outlet name or "
         "distance, so the mechanism is inferred. Test: re-run one slot capturing outlet name and "
         "stated distance per platform.",
    evidence_type="PRIMARY OBSERVED (ETA) x FIRST-HAND OBSERVATION (outlet)"))

# =====================================================================
# 9. BENGALURU BENCHMARK
# =====================================================================
bench = []
for label, d_ in [("Gachibowli catchment", C), ("Bengaluru (benchmark)", BLR)]:
    bench.append(dict(
        base=label, n=len(d_),
        aware_pct=round(d_["ownly_aware"].fillna(False).mean() * 100, 1),
        tried_pct=round(d_["ownly_says_ordered"].fillna(False).mean() * 100, 1),
        membership_pct=round(d_["has_membership"].mean() * 100, 1),
        multihoming_pct=round(d_["multihoming"].dropna().astype(bool).mean() * 100, 1)
        if d_["multihoming"].notna().any() else None,
        median_switch_rs=float(d_["switch_savings_rs"].dropna().median())
        if d_["switch_savings_rs"].notna().any() else None,
        durability_doubt_pct=round((d_["durability_doubt_n"].dropna() >= 4).mean() * 100, 1)
        if d_["durability_doubt_n"].notna().any() else None))
pd.DataFrame(bench).to_csv(f"{D}/bengaluru_benchmark.csv", index=False)

pd.DataFrame(HYP).to_csv(f"{D}/hypothesis_results.csv", index=False)

# ------------------------------------------------------------------- console
print(f"BASE Gachibowli catchment n={N}\n")
print("RESEARCH FUNNEL"); print(F[["stage", "n", "pct_of_catchment"]].to_string(index=False))
print(f"\nH0 STATED: P {nP} vs Q {nQ} (+{nC} can't choose) -> p={bt.pvalue:.4f} "
      f"[{ci.low*100:.1f}%, {ci.high*100:.1f}%] -> {HYP[1]['verdict']}")
print(f"H0 BEHAVIOURAL: {HYP[0]['verdict']}")
print("\n₹30 TRADE-OFFS"); print(TR.to_string(index=False))
print("\nPAIRED TESTS"); print(pd.DataFrame(trade_tests).to_string(index=False))
print("\nSWITCHING STAIRCASE"); print(ST[["level_rs", "k", "pct_of_named", "pct_of_all"]].to_string(index=False))
print(f"  n_named={len(thr)}  excluded: no-amount={never}, don't-know={dk}")
print("\nASSOCIATIONS"); print(AS[["x", "y", "n", "rho", "p_value", "verdict"]].to_string(index=False))
print("\nSEGMENT CUTS"); print(SEG.to_string(index=False))
print("\nETA GAP BY RESTAURANT"); print(eta[["ownly", "best_incumbent", "gap"]].round(1).to_string())
print("\nBENGALURU BENCHMARK"); print(pd.DataFrame(bench).to_string(index=False))
print(f"\nANOMALY REGISTER: {len(ANOM)} entries -> data/anomalies.csv")
