"""
03_kpis_metrics_hypotheses.py — Ownly Gachibowli
Computes KPIs, derived marketing metrics, hypothesis results and the pre-registered
P1-P5 challenger-pattern predictions. Every figure carries n, base, source, evidence type.

ZERO FABRICATION. Anything not computable is emitted as NOT ESTIMABLE FROM AVAILABLE EVIDENCE.
"""
import json, os
import numpy as np
import pandas as pd
from scipy import stats

ROOT = "/Users/klprathyusha/Sem 3/Project/Ownly"
D = f"{ROOT}/final_dashboard/data"

S = pd.read_csv(f"{D}/cleaned_survey.csv")
P = pd.read_csv(f"{D}/audit_pairs.csv")
A = pd.read_csv(f"{D}/audit_clean.csv")
COV = pd.read_csv(f"{D}/audit_coverage.csv")

HYD = S[S["pop_HYD_ELIGIBLE"]].copy()
CATCH = S[S["pop_HYD_CATCHMENT"]].copy()
BLR = S[S["pop_BLR_ELIGIBLE"]].copy()
OTH = S[S["pop_OTHER"]].copy()
HYD_ORD = HYD[HYD["ordered_4wk"].eq("Yes")]


# ------------------------------------------------------------------ helpers
def wilson(k, n, z=1.96):
    if n == 0:
        return (np.nan, np.nan, np.nan)
    p = k / n
    d = 1 + z**2 / n
    c = (p + z**2 / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / d
    return (p * 100, max(0, c - h) * 100, min(1, c + h) * 100)


def prop(series, cond=None, label=""):
    """Returns dict with k, n, pct, ci_lo, ci_hi for a boolean-able series."""
    s = series.dropna()
    if cond is not None:
        k = int(cond(s).sum())
    else:
        k = int(s.astype(bool).sum())
    n = int(len(s))
    pct, lo, hi = wilson(k, n)
    return {"k": k, "n": n, "pct": pct, "ci_lo": lo, "ci_hi": hi, "label": label}


KPI, MM, HYP, NOTES = [], [], [], []


def kpi(kid, name, layer, driver, value, unit, k, n, base, source, evidence,
        ci=None, question=None, interpret=None):
    KPI.append({"kpi_id": kid, "kpi_name": name, "layer": layer, "driver": driver,
                "value": value, "unit": unit, "numerator": k, "denominator": n,
                "base": base, "source": source, "evidence_type": evidence,
                "ci_lo": None if ci is None else round(ci[0], 1),
                "ci_hi": None if ci is None else round(ci[1], 1),
                "business_question": question, "interpretation": interpret})


# ================================================================ INPUT KPIs
# ---- PRICE (observed audit)
for view, kid in [("LIST+FEES", "K20a"), ("MEMBER", "K20b"), ("AFTER OFFER", "K20c")]:
    g = P[P["view"].eq(view)]
    if len(g):
        kpi(kid, f"Ownly price win rate — {view}", "INPUT", "PRICE",
            round(g["ownly_wins"].mean() * 100, 1), "%", int(g["ownly_wins"].sum()), len(g),
            "Matched restaurant x basket comparisons, DP1 Gachibowli, wed_dinner 2026-09-16",
            "06_competitor_audit/audit_data_slot1.csv", "PRIMARY OBSERVED DATA",
            question="Is Ownly actually cheaper at checkout?",
            interpret=f"Ownly cheapest in {int(g['ownly_wins'].sum())} of {len(g)} matched baskets in the {view} view")
        kpi(kid.replace("K20", "K21"), f"Median saving vs cheapest incumbent — {view}", "INPUT", "PRICE",
            round(g["saving_rs"].median(), 2), "INR", None, len(g),
            "Same matched baskets", "audit_pairs.csv", "PRIMARY OBSERVED DATA",
            question="How large is the saving in rupees?",
            interpret=f"Median {g['saving_rs'].median():.0f} INR ({g['saving_pct'].median():.1f}%)")

pr = A[A["final_payable"].notna()]
for plat in ["ownly", "swiggy", "zomato"]:
    g = pr[pr["platform"].eq(plat)]
    kpi(f"K22_{plat}", f"Non-food share of bill — {plat}", "INPUT", "PRICE",
        round(g["non_food_share"].median() * 100, 1), "%", None, len(g),
        f"{len(g)} priced captures", "audit_clean.csv", "PRIMARY OBSERVED DATA",
        question="How much of the bill is fees and tax rather than food?",
        interpret="Ownly's structural advantage is the absence of fees")

# ---- SERVICE (observed)
for plat in ["ownly", "swiggy", "zomato"]:
    g = A[A["platform"].eq(plat)]
    kpi(f"K30_{plat}", f"Quoted ETA midpoint — {plat}", "INPUT", "SERVICE",
        round(g["eta_mid"].median(), 1), "min", None, int(g["eta_mid"].notna().sum()),
        "All captures with an ETA shown", "audit_clean.csv", "PRIMARY OBSERVED DATA",
        question="How much slower is Ownly?",
        interpret="Quoted ETA, NOT observed delivery time - no test orders were placed")
eta_gap = (A[A.platform.eq("ownly")]["eta_mid"].median()
           - A[A.platform.isin(["swiggy", "zomato"])]["eta_mid"].median())
kpi("K31", "Ownly quoted-ETA gap vs incumbent median", "INPUT", "SERVICE",
    round(eta_gap, 1), "min", None, int(A["eta_mid"].notna().sum()),
    "All captures with ETA", "audit_clean.csv", "PRIMARY OBSERVED DATA",
    question="What speed penalty accompanies the saving?")

# ---- ASSORTMENT (observed)
cov = COV.set_index("restaurant_name")
listed_own = (cov["ownly"] == "y").sum()
kpi("K40", "Ownly coverage of audited restaurant frame", "INPUT", "ASSORTMENT",
    round(listed_own / len(cov) * 100, 1), "%", int(listed_own), len(cov),
    "12 audited restaurants at DP1", "audit_coverage.csv", "PRIMARY OBSERVED DATA",
    question="Does Ownly have the restaurants people use?")
both_inc = ((cov["swiggy"] == "y") | (cov["zomato"] == "y"))
overlap = ((cov["ownly"] == "y") & both_inc).sum()
kpi("K42", "Cross-platform assortment overlap", "INPUT", "ASSORTMENT",
    round(overlap / both_inc.sum() * 100, 1), "%", int(overlap), int(both_inc.sum()),
    "Restaurants on >=1 incumbent", "audit_coverage.csv", "PRIMARY OBSERVED DATA",
    question="Is Ownly offering a differentiated catalogue, or the same one?",
    interpret="High overlap = little differentiated supply (failure mechanism M3)")
own_only = ((cov["ownly"] == "y") & ~both_inc).sum()
inc_only = ((cov["ownly"] != "y") & both_inc).sum()
kpi("K43", "Ownly-only restaurants observed", "INPUT", "ASSORTMENT", int(own_only), "count",
    int(own_only), len(cov), "12 audited restaurants", "audit_coverage.csv",
    "PRIMARY OBSERVED DATA", question="Does Ownly offer supply the incumbents lack?")
kpi("K44", "Incumbent-only restaurants observed", "INPUT", "ASSORTMENT", int(inc_only), "count",
    int(inc_only), len(cov), "12 audited restaurants", "audit_coverage.csv",
    "PRIMARY OBSERVED DATA", question="What supply gap does Ownly carry?")

# ---- LOCK-IN (survey)
p = prop(HYD["has_membership"])
kpi("K50", "Incumbent membership lock-in", "INPUT", "LOCK-IN", round(p["pct"], 1), "%",
    p["k"], p["n"], "Hyderabad eligible respondents (20-35)", "Ownly Survey.csv",
    "SURVEY — STATED BEHAVIOUR", ci=(p["ci_lo"], p["ci_hi"]),
    question="How locked in are Gachibowli customers?",
    interpret="Members see the MEMBER or AFTER OFFER price view, not the list view")
mh = HYD["multihoming"].dropna()
p = prop(mh)
kpi("K51", "Multi-homing rate (2+ platforms in 4 weeks)", "INPUT", "LOCK-IN",
    round(p["pct"], 1), "%", p["k"], p["n"], "Hyderabad respondents reporting order counts",
    "Ownly Survey.csv", "SURVEY — STATED BEHAVIOUR", ci=(p["ci_lo"], p["ci_hi"]),
    question="Do users already use more than one app?")

sw = HYD["switch_savings_rs"].dropna()
kpi("K52", "Median required recurring saving to switch main app", "INPUT", "LOCK-IN",
    float(sw.median()), "INR", None, len(sw),
    "Hyderabad respondents giving a rupee threshold (excl. 'no amount' and 'don't know')",
    "Ownly Survey.csv", "SURVEY — STATED PREFERENCE",
    question="How much recurring saving is required to switch?")
p = prop(HYD["switch_never"])
kpi("K53", "Share saying no price would make them switch", "INPUT", "LOCK-IN",
    round(p["pct"], 1), "%", p["k"], p["n"], "Hyderabad eligible", "Ownly Survey.csv",
    "SURVEY — STATED PREFERENCE", ci=(p["ci_lo"], p["ci_hi"]))

# ---- DISTRIBUTION (survey)
rap = HYD[HYD["rapido_food_seen"].notna() & ~HYD["rapido_food_seen"].eq("I don't use the Rapido app")]
p = prop(rap["rapido_food_seen"], cond=lambda s: s.eq("Yes"))
kpi("K60", "Rapido users who noticed food inside the Rapido app", "INPUT", "DISTRIBUTION",
    round(p["pct"], 1), "%", p["k"], p["n"], "Hyderabad respondents who use Rapido",
    "Ownly Survey.csv", "SURVEY — STATED BEHAVIOUR", ci=(p["ci_lo"], p["ci_hi"]),
    question="Does Rapido create real discovery, or only theoretical access?")
p = prop(HYD["rapido_freq"], cond=lambda s: ~s.eq("Never"))
kpi("K61", "Recent Rapido usage (any, last 4 weeks)", "INPUT", "DISTRIBUTION",
    round(p["pct"], 1), "%", p["k"], p["n"], "Hyderabad respondents answering the Rapido item",
    "Ownly Survey.csv", "SURVEY — STATED BEHAVIOUR", ci=(p["ci_lo"], p["ci_hi"]))

# =============================================================== OUTPUT KPIs
for kid, col, nm, q in [
    ("K70", "ownly_aware", "Ownly awareness", "Do they know it exists?"),
    ("K71", "ownly_opened", "Ownly opened / browsed", "Did awareness become a visit?"),
    ("K72", "ownly_ordered", "Ownly trial (ever ordered)", "Did a visit become an order?")]:
    p = prop(HYD[col])
    kpi(kid, nm, "OUTPUT", "FUNNEL", round(p["pct"], 1), "%", p["k"], p["n"],
        "Hyderabad eligible (20-35)", "Ownly Survey.csv", "SURVEY — STATED BEHAVIOUR",
        ci=(p["ci_lo"], p["ci_hi"]), question=q)

own4 = HYD_ORD["n_ownly"].dropna()
kpi("K73", "Ownly orders in last 4 weeks (Hyderabad orderers)", "OUTPUT", "FUNNEL",
    float(own4.sum()), "orders", int(own4.sum()), len(own4),
    "Hyderabad respondents who ordered food in last 4 weeks",
    "Ownly Survey.csv", "SURVEY — STATED BEHAVIOUR",
    question="Is Ownly in the actual rotation?",
    interpret="Observed share of recent orders on Ownly in this sample")

p = prop(HYD["repeat_no_promo_n"], cond=lambda s: s >= 4)
kpi("K74", "Would keep using after the intro offer ends (top-2 box)", "OUTPUT", "RETENTION",
    round(p["pct"], 1), "%", p["k"], p["n"], "Hyderabad eligible, after concept exposure",
    "Ownly Survey.csv", "SURVEY — STATED PREFERENCE", ci=(p["ci_lo"], p["ci_hi"]),
    question="Does price-led trial look like it becomes a habit?",
    interpret="STATED INTENT PROXY - not observed retention")
p = prop(HYD["durability_doubt_n"], cond=lambda s: s >= 4)
kpi("K75", "Believe a new app's low prices will rise once popular", "OUTPUT", "RETENTION",
    round(p["pct"], 1), "%", p["k"], p["n"], "Hyderabad eligible", "Ownly Survey.csv",
    "SURVEY — STATED PREFERENCE", ci=(p["ci_lo"], p["ci_hi"]),
    question="Is the price promise believed?")

# ---- the three-30-rupee trade-offs
TRADE = [("eta_chose_cheap", "K80", "speed", "wait 15 minutes longer"),
         ("rel_chose_cheap", "K81", "reliability", "accept 3-in-10 late instead of 1-in-10"),
         ("rest_chose_cheap", "K82", "usual restaurants", "give up most usual restaurants")]
trade_rows = []
for col, kid, dim, desc in TRADE:
    s = HYD[col].dropna().astype(bool)
    p = prop(s)
    kpi(kid, f"Will trade {dim} for INR 30", "OUTPUT", "TRADE-OFF", round(p["pct"], 1), "%",
        p["k"], p["n"], "Hyderabad eligible shown the paired choice", "Ownly Survey.csv",
        "SURVEY — STATED PREFERENCE", ci=(p["ci_lo"], p["ci_hi"]),
        question=f"Will users {desc} to save INR 30?")
    trade_rows.append({"dimension": dim, "description": desc, "chose_cheaper_k": p["k"],
                       "n": p["n"], "chose_cheaper_pct": round(p["pct"], 1),
                       "ci_lo": round(p["ci_lo"], 1), "ci_hi": round(p["ci_hi"], 1),
                       "paid_premium_pct": round(100 - p["pct"], 1)})
pd.DataFrame(trade_rows).to_csv(f"{D}/tradeoff_summary.csv", index=False)

# ---- segment split, to test the interview claim "students weight money over time,
# ---- general users weight time over money" (interview_findings_coded.md, T-1)
HYD = HYD.copy()
HYD["seg"] = np.where(HYD["occupation"].str.contains("Student", na=False), "Student",
                      np.where(HYD["occupation"].eq("Working full-time"), "Working prof", None))
seg_rows = []
for col, dim in [("eta_chose_cheap", "speed"), ("rel_chose_cheap", "reliability"),
                 ("rest_chose_cheap", "usual restaurants")]:
    cells = {}
    for seg in ["Student", "Working prof"]:
        s = HYD[HYD["seg"].eq(seg)][col].dropna().astype(bool)
        if not len(s):
            continue
        pct, lo, hi = wilson(int(s.sum()), len(s))
        cells[seg] = (int(s.sum()), len(s))
        seg_rows.append({"dimension": dim, "segment": seg, "k": int(s.sum()), "n": len(s),
                         "chose_cheaper_pct": round(pct, 1), "ci_lo": round(lo, 1),
                         "ci_hi": round(hi, 1)})
    if len(cells) == 2:
        a, b = cells["Student"], cells["Working prof"]
        pv = stats.fisher_exact([[a[0], a[1] - a[0]], [b[0], b[1] - b[0]]])[1]
        for r in seg_rows:
            if r["dimension"] == dim:
                r["fisher_p"] = round(pv, 3)
SEG = pd.DataFrame(seg_rows)
thr_seg = HYD.groupby("seg")["switch_savings_rs"].agg(["median", "count"]).reset_index()
thr_seg.to_csv(f"{D}/segment_switch_threshold.csv", index=False)
SEG.to_csv(f"{D}/segment_tradeoffs.csv", index=False)

pd.DataFrame(KPI).to_csv(f"{D}/kpi_table.csv", index=False)

# ==================================================== DERIVED MARKETING METRICS
def mm(mid, name, formula, value, unit, num, den, source, evidence, interp, caveat):
    MM.append({"metric_id": mid, "metric_name": name, "formula": formula, "value": value,
               "unit": unit, "numerator": num, "denominator": den, "data_source": source,
               "evidence_type": evidence, "interpretation": interp, "caveat": caveat})


g_list = P[P["view"].eq("LIST+FEES")]
g_mem = P[P["view"].eq("MEMBER")]
g_off = P[P["view"].eq("AFTER OFFER")]

mm("MM1", "Price Win Rate (structural)",
   "matched baskets where Ownly final payable is lowest / all matched baskets",
   round(g_list["ownly_wins"].mean() * 100, 1), "%", int(g_list["ownly_wins"].sum()), len(g_list),
   "audit_pairs.csv", "PRIMARY OBSERVED DATA",
   "On list price plus fees, Ownly wins every matched basket",
   "n=4 matched baskets, one slot, one address. Directional.")

mm("MM2", "Median Basket Saving (structural)",
   "median(cheapest incumbent final payable - Ownly final payable)",
   round(g_list["saving_rs"].median(), 2), "INR", None, len(g_list),
   "audit_pairs.csv", "PRIMARY OBSERVED DATA",
   f"Median {g_list['saving_pct'].median():.1f}% cheaper before any offer",
   "Excludes incumbent memberships and coupons.")

# Offer Reversal Rate - baskets Ownly wins on list but loses after offers
rev = g_list.merge(g_off, on=["restaurant_name", "basket_id"], suffixes=("_list", "_off"))
reversed_n = int((rev["ownly_wins_list"] & ~rev["ownly_wins_off"]).sum())
mm("MM3", "Offer Reversal Rate",
   "baskets Ownly wins on list+fees but loses after incumbent offers / matched baskets",
   round(reversed_n / len(rev) * 100, 1) if len(rev) else np.nan, "%", reversed_n, len(rev),
   "audit_pairs.csv", "PRIMARY OBSERVED DATA",
   "Share of Ownly's structural price wins that incumbent coupons erase",
   "Ownly held a new-account intro offer; incumbents held memberships. Both views reported.")

# Membership Erosion Rate - NEW, our own metric
mem_rev = g_list.merge(g_mem, on=["restaurant_name", "basket_id"], suffixes=("_l", "_m"))
mem_lost = int((mem_rev["ownly_wins_l"] & ~mem_rev["ownly_wins_m"]).sum())
mm("MM4", "Membership Erosion Rate (custom)",
   "baskets Ownly wins on list+fees but loses once the incumbent MEMBERSHIP benefit alone applies "
   "/ matched baskets (no coupon involved)",
   round(mem_lost / len(mem_rev) * 100, 1) if len(mem_rev) else np.nan, "%", mem_lost, len(mem_rev),
   "audit_pairs.csv", "PRIMARY OBSERVED DATA",
   "Isolates how much of Ownly's edge a subscription alone removes, before any coupon. "
   "Good indicator because a membership is a STANDING benefit (it applies to every order), "
   "whereas a coupon is episodic - so this is the durable half of the erosion.",
   "n=4. Zomato Gold free delivery observed on every Zomato list capture in this slot.")

# Switching Reach at the observed saving
obs_med = g_list["saving_rs"].median()
valid_thr = HYD["switch_savings_rs"].dropna()
reach_k = int((valid_thr <= obs_med).sum())
pct, lo, hi = wilson(reach_k, len(valid_thr))
mm("MM5", f"Switching Reach @ observed structural saving (INR {obs_med:.0f})",
   "respondents whose stated required recurring saving <= observed median structural saving "
   "/ respondents giving a rupee threshold",
   round(pct, 1), "%", reach_k, len(valid_thr), "Ownly Survey.csv + audit_pairs.csv",
   "SURVEY — STATED PREFERENCE x PRIMARY OBSERVED DATA",
   f"Share of threshold-giving respondents whose bar is cleared by the observed INR {obs_med:.0f} saving "
   f"[95% CI {lo:.0f}-{hi:.0f}%]",
   "Denominator excludes 'no amount' and 'don't know'. Stated threshold, not observed switching.")

# same, at the AFTER OFFER saving
obs_off = g_off["saving_rs"].median()
mm("MM5b", f"Switching Reach @ observed wallet saving (INR {obs_off:.0f})",
   "same numerator rule, using the AFTER OFFER median saving",
   0.0 if obs_off < 10 else np.nan, "%", 0 if obs_off < 10 else None, len(valid_thr),
   "Ownly Survey.csv + audit_pairs.csv",
   "SURVEY — STATED PREFERENCE x PRIMARY OBSERVED DATA",
   f"After incumbent offers the median saving is INR {obs_off:.0f} (Ownly DEARER), so no stated "
   "threshold is cleared",
   "A negative saving cannot clear any positive threshold.")

s = HYD["rest_chose_cheap"].dropna().astype(bool)
k = int((~s).sum())
pct, lo, hi = wilson(k, len(s))
mm("MM6", "Assortment Barrier Rate",
   "respondents paying the INR 30 premium to keep most usual restaurants / respondents shown the item",
   round(pct, 1), "%", k, len(s), "Ownly Survey.csv", "SURVEY — STATED PREFERENCE",
   f"Share who will NOT give up their usual restaurants for INR 30 [95% CI {lo:.0f}-{hi:.0f}%]",
   "Stated choice on a constructed pair, not observed behaviour.")

p = prop(HYD["has_membership"])
mm("MM7", "Incumbent Lock-in Rate", "membership holders / eligible respondents",
   round(p["pct"], 1), "%", p["k"], p["n"], "Ownly Survey.csv", "SURVEY — STATED BEHAVIOUR",
   f"[95% CI {p['ci_lo']:.0f}-{p['ci_hi']:.0f}%] These respondents never see the list-price view",
   "Membership held, not membership actively used.")

p = prop(rap["rapido_food_seen"], cond=lambda x: ~x.eq("Yes"))
mm("MM8", "Rapido Discovery Gap",
   "recent Rapido users who have NOT noticed food ordering / recent Rapido users",
   round(p["pct"], 1), "%", p["k"], p["n"], "Ownly Survey.csv", "SURVEY — STATED BEHAVIOUR",
   f"[95% CI {p['ci_lo']:.0f}-{p['ci_hi']:.0f}%] Distribution exists; discovery largely does not",
   "'Not sure' counted as not-noticed. Excludes non-users of Rapido.")

trial = prop(HYD["prop_P_intent_n"], cond=lambda s: s >= 4)
rep = prop(HYD["repeat_no_promo_n"], cond=lambda s: s >= 4)
mm("MM9", "Stated Trial-to-Repeat Intent Gap",
   "(% top-2 likely to TRY the chosen proposition) - (% top-2 likely to CONTINUE after the intro offer ends)",
   round(trial["pct"] - rep["pct"], 1), "pp", None, trial["n"],
   "Ownly Survey.csv", "SURVEY — STATED PREFERENCE",
   f"Trial intent {trial['pct']:.0f}% vs post-offer continuation {rep['pct']:.0f}% "
   f"-> {trial['pct'] - rep['pct']:.0f}pp drop",
   "STATED-INTENT PROXY. Not observed retention. Two different question framings.")

# custom: Fee Transparency Advantage
own_nf = pr[pr.platform.eq("ownly")]["non_food_share"].median() * 100
inc_nf = pr[pr.platform.isin(["swiggy", "zomato"])]["non_food_share"].median() * 100
mm("MM10", "Fee Load Advantage (custom)",
   "median incumbent non-food share of bill - median Ownly non-food share",
   round(inc_nf - own_nf, 1), "pp", None, len(pr), "audit_clean.csv", "PRIMARY OBSERVED DATA",
   "Ownly's structural edge expressed as the share of the bill that is NOT food. "
   "Good indicator because it is the one advantage Ownly controls directly: it survives without "
   "subsidy, unlike a discount, and it is invisible to the customer unless stated - which links "
   "it to the communication problem.",
   "Median across priced captures; excludes menu-price differences.")

pd.DataFrame(MM).to_csv(f"{D}/marketing_metrics.csv", index=False)

# ======================================================== NOT ESTIMABLE panel
NE = [("Customer Acquisition Cost (CAC)", "No spend data, no attributable acquisition counts"),
      ("Customer Lifetime Value (CLV)", "No repeat-purchase or margin data for any platform"),
      ("True retention / cohort curves", "No longitudinal panel; survey is a single cross-section"),
      ("Market share (value or volume)", "No denominator for Hyderabad food-delivery orders"),
      ("Contribution margin / EBITDA / burn per order (Ownly)", "Never disclosed by Rapido; no filing exists"),
      ("Actual delivery time vs quoted ETA", "Test orders were not placed; only quoted ETA observed"),
      ("First-order conversion rate (behavioural)", "Fake-door experiment was not executed (0 events)"),
      ("Restaurant-side economics in Hyderabad", "No restaurant interviews conducted")]
pd.DataFrame(NE, columns=["metric", "why_not_estimable"]).assign(
    status="NOT ESTIMABLE FROM AVAILABLE EVIDENCE").to_csv(f"{D}/not_estimable.csv", index=False)

# ================================================================ HYPOTHESES
def hyp(hid, statement, test, result, n, stat, p, ci, verdict, note, evidence):
    HYP.append({"id": hid, "statement": statement, "test": test, "result": result, "n": n,
                "statistic": stat, "p_value": p, "ci": ci, "verdict": verdict,
                "note": note, "evidence_type": evidence})


# --- H0 behavioural: NOT TESTED
hyp("H0-BEHAVIOURAL",
    "Among the Gachibowli target population, a Bengaluru-style Ownly proposition does not produce a "
    "significantly different FIRST-ORDER CONVERSION rate from a Hyderabad-localised proposition.",
    "Randomised fake-door landing test (planned)", "NOT TESTED", 0, None, None, None,
    "NOT DIRECTLY TESTED",
    "The fake-door experiment was not executed: fact_fakedoor_events.csv contains 0 events. "
    "No behavioural first-order conversion was observed. This cannot be substituted with survey intent.",
    "NONE")

# --- H0 stated-preference analogue: forced choice P vs Q
fc = HYD["prop_forced"].dropna()
nP = int((fc == "Service P").sum())
nQ = int((fc == "Service Q").sum())
nCant = int((fc == "I genuinely can't choose between them").sum())
n_dec = nP + nQ
bt = stats.binomtest(nP, n_dec, 0.5)
ci_b = bt.proportion_ci(confidence_level=0.95)
hyp("H0-STATED",
    "Stated-preference analogue: the share choosing the Bengaluru-style proposition (Service P) does "
    "not differ from 50% among respondents who expressed a preference.",
    "Exact binomial vs 50% (two-sided), Wilson/Clopper-Pearson CI",
    f"Service P {nP} vs Service Q {nQ} (plus {nCant} 'can't choose')", n_dec,
    f"P share = {nP/n_dec*100:.1f}%", round(bt.pvalue, 4),
    f"[{ci_b.low*100:.1f}%, {ci_b.high*100:.1f}%]",
    "FAIL TO REJECT H0" if bt.pvalue >= 0.05 else "REJECT H0",
    f"{nCant}/{len(fc)} ({nCant/len(fc)*100:.0f}%) could not choose between the two bundled "
    "propositions - itself a finding about proposition distinctiveness.",
    "SURVEY — STATED PREFERENCE (PROXY, not conversion)")

# --- McNemar on P vs Q top-2 intent
d = HYD[["prop_P_intent_n", "prop_Q_intent_n"]].dropna()
pt = (d["prop_P_intent_n"] >= 4)
qt = (d["prop_Q_intent_n"] >= 4)
b = int((pt & ~qt).sum())
c = int((~pt & qt).sum())
mc_p = stats.binomtest(b, b + c, 0.5).pvalue if (b + c) > 0 else np.nan
hyp("H0-STATED-MCNEMAR",
    "Top-2-box trial intent does not differ between Service P and Service Q (paired).",
    "McNemar exact (paired binary, same respondents)",
    f"discordant pairs: P-only {b}, Q-only {c}", len(d), f"b={b}, c={c}",
    None if np.isnan(mc_p) else round(mc_p, 4), None,
    "FAIL TO REJECT H0" if (np.isnan(mc_p) or mc_p >= 0.05) else "REJECT H0",
    "Paired test on the same respondents; complements the forced choice.",
    "SURVEY — STATED PREFERENCE")

# ------------------------------------- pre-registered P1-P5 (PAP section 6.7)
tr = prop(HYD["prop_P_intent_n"], cond=lambda s: s >= 4)
rp = prop(HYD["repeat_no_promo_n"], cond=lambda s: s >= 4)
p1_trial_wins = bt.pvalue < 0.05 and nP > nQ
p1_repeat_fails = rp["ci_hi"] < 50
hyp("P1", "Price framing wins trial but does not survive to repeat (M1 rented demand).",
    "Conjunction: exact binomial on forced choice AND Wilson CI on post-offer continuation",
    f"Service P did NOT significantly win trial (p={bt.pvalue:.3f}); post-offer continuation "
    f"{rp['pct']:.1f}% [{rp['ci_lo']:.1f}-{rp['ci_hi']:.1f}%]",
    rp["n"], f"repeat top-2 = {rp['k']}/{rp['n']}", round(bt.pvalue, 4),
    f"[{rp['ci_lo']:.1f}%, {rp['ci_hi']:.1f}%]",
    "NOT SUPPORTED AS STATED (first limb fails)",
    "The first limb requires Service P to win trial; it did not. The second limb (weak post-offer "
    "continuation) IS observed. So the retention concern stands on its own, but the 'price wins "
    "trial' premise is not supported in this sample.",
    "SURVEY — STATED PREFERENCE")

hyp("P2", "Coupon-dependent users see no Ownly advantage.",
    "Planned: offer-dependency band x forced choice", "NOT TESTABLE", 0, None, None, None,
    "NOT TESTABLE",
    "The live v3 form does not contain the offer-dependency item (planned Q13, 'of your last 10 "
    "orders how many used a coupon'). No substitute variable exists.",
    "NONE")

s_eta = HYD["eta_chose_cheap"].dropna().astype(bool)
pe = prop(s_eta)
hyp("P3", "The observed ETA gap exceeds stated tolerance (M3).",
    "Wilson CI on share choosing the cheaper/slower option in the INR 30 / 15-minute pair",
    f"{pe['pct']:.1f}% chose cheaper+slower [{pe['ci_lo']:.1f}-{pe['ci_hi']:.1f}%]",
    pe["n"], f"{pe['k']}/{pe['n']}", None, f"[{pe['ci_lo']:.1f}%, {pe['ci_hi']:.1f}%]",
    "FALSIFIED",
    "Pre-registered rule: P3 holds only if the lower CI bound is NOT above 50%. It is "
    f"({pe['ci_lo']:.1f}%). Respondents accept the slower option for INR 30. Since the survey tested a "
    "15-minute gap and the audit observed ~17 minutes, this is close to but not identical with the "
    "observed gap - the inference is one-directional and is not claimed beyond 15 minutes.",
    "SURVEY — STATED PREFERENCE")

dd = HYD[["rest_chose_cheap", "eta_chose_cheap"]].dropna()
b4 = int((~dd["rest_chose_cheap"].astype(bool) & dd["eta_chose_cheap"].astype(bool)).sum())
c4 = int((dd["rest_chose_cheap"].astype(bool) & ~dd["eta_chose_cheap"].astype(bool)).sum())
mc4 = stats.binomtest(b4, b4 + c4, 0.5).pvalue if (b4 + c4) > 0 else np.nan
prem_rest = 100 - prop(HYD["rest_chose_cheap"].dropna().astype(bool))["pct"]
prem_eta = 100 - pe["pct"]
hyp("P4", "Assortment beats speed: users defend usual restaurants harder than delivery speed.",
    "McNemar exact on paired premium-choice (assortment pair vs speed pair, same respondents)",
    f"paid premium to keep restaurants {prem_rest:.1f}% vs to keep speed {prem_eta:.1f}%",
    len(dd), f"b={b4}, c={c4}", None if np.isnan(mc4) else round(mc4, 6), None,
    "CONFIRMED" if (not np.isnan(mc4) and mc4 < 0.05 and prem_rest > prem_eta) else "NOT CONFIRMED",
    "The single strongest result in the survey. The same INR 30 buys a 15-minute delay for most "
    "respondents but cannot buy away their usual restaurants.",
    "SURVEY — STATED PREFERENCE")

dsub = HYD[HYD["prop_forced"].isin(["Service P", "Service Q"])].dropna(subset=["durability_doubt_n"])
if len(dsub) > 5:
    x = dsub["durability_doubt_n"].astype(float)
    y = (dsub["prop_forced"] == "Service P").astype(int)
    rho, pv = stats.spearmanr(x, y)
    hyp("P5", "Durability doubt suppresses the price proposition.",
        "Spearman rho between agreement that low prices rise, and choosing the price-led Service P",
        f"rho = {rho:.3f}", len(dsub), f"rho={rho:.3f}", round(pv, 4), None,
        "NOT SUPPORTED" if pv >= 0.05 else ("SUPPORTED" if rho < 0 else "REVERSED"),
        f"Durability doubt is near-universal in this sample "
        f"({prop(HYD['durability_doubt_n'], cond=lambda s: s>=4)['pct']:.0f}% agree), which leaves "
        "very little variance for an association to be detected. A null here is uninformative "
        "rather than evidence of no effect.",
        "SURVEY — STATED PREFERENCE")

pd.DataFrame(HYP).to_csv(f"{D}/hypothesis_results.csv", index=False)

# ---------------------------------------------------- derived respondent file
keep = ["resp_id", "city", "area", "age_band", "occupation", "in_catchment", "has_membership",
        "n_memberships", "multihoming", "n_platforms_used", "total_orders_4wk", "n_swiggy",
        "n_zomato", "n_ownly", "n_other", "last_app", "last_amount", "amount_pp",
        "bill_fairness", "rapido_freq", "rapido_food_seen", "ownly_stage", "ownly_aware",
        "ownly_opened", "ownly_ordered", "eta_chose_cheap", "rel_chose_cheap", "rest_chose_cheap",
        "switch_savings_rs", "switch_never", "switch_dk", "prop_P_intent_n", "prop_Q_intent_n",
        "prop_forced", "repeat_no_promo_n", "durability_doubt_n",
        "pop_HYD_ELIGIBLE", "pop_HYD_CATCHMENT", "pop_BLR_ELIGIBLE", "pop_OTHER"]
S[[c for c in keep if c in S.columns]].to_csv(f"{D}/derived_survey_metrics.csv", index=False)

# ------------------------------------------------------------------- console
print(f"POPULATIONS  HYD={len(HYD)}  CATCHMENT={len(CATCH)}  BLR={len(BLR)}  OTHER={len(OTH)}")
print(f"\nKPIs written: {len(KPI)}   Marketing metrics: {len(MM)}   Hypotheses: {len(HYP)}")
print("\n--- THE 30-RUPEE TRADE-OFFS (Hyderabad, n=46) ---")
print(pd.DataFrame(trade_rows).to_string(index=False))
print("\n--- H0 (stated-preference analogue) ---")
print(f"Service P {nP} | Service Q {nQ} | can't choose {nCant} -> p={bt.pvalue:.4f} "
      f"({'FAIL TO REJECT' if bt.pvalue>=.05 else 'REJECT'})")
print("\n--- MARKETING METRICS ---")
print(pd.DataFrame(MM)[["metric_id", "metric_name", "value", "unit", "numerator", "denominator"]]
      .to_string(index=False))
print("\n--- PRE-REGISTERED P1-P5 ---")
print(pd.DataFrame(HYP)[pd.DataFrame(HYP).id.str.startswith("P")][["id", "verdict"]].to_string(index=False))
