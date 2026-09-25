"""
02_kpis_and_metrics.py — KPI register + derived marketing metrics

Primary base: HYD CATCHMENT (Gachibowli + Financial District/Nanakramguda, Manikonda,
Narsingi/Kokapet, Serilingampally/Nallagandla/Tellapur), n=40. Gachibowli-proper and the
wider Hyderabad base are computed alongside as cuts, never blended.

Every metric carries: formula, numerator, denominator, base, source, evidence type,
evidence strength, why it is a good indicator, its limitation, and what would upgrade it.
Anything not computable is emitted with status NOT COMPUTABLE and the reason — never a proxy.
"""
import json
import os

import numpy as np
import pandas as pd
from scipy import stats

ROOT = "/Users/klprathyusha/Sem 3/Project/Ownly"
D = f"{ROOT}/final_dashboard/data"

S = pd.read_csv(f"{D}/cleaned_survey.csv")
P = pd.read_csv(f"{D}/audit_pairs.csv")
A = pd.read_csv(f"{D}/audit_clean.csv")
COV = pd.read_csv(f"{D}/audit_coverage.csv")

CATCH = S[S["pop_HYD_CATCHMENT"]].copy()
GACH = S[S["pop_HYD_GACHIBOWLI"]].copy()
HYD = S[S["pop_HYD_ELIGIBLE"]].copy()
BLR = S[S["pop_BLR_ELIGIBLE"]].copy()
BASE, NB = CATCH, len(CATCH)


def wilson(k, n, z=1.96):
    if not n:
        return (np.nan, np.nan, np.nan)
    p = k / n
    d = 1 + z**2 / n
    c = (p + z**2 / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / d
    return (p * 100, max(0, c - h) * 100, min(1, c + h) * 100)


KPI, MM = [], []


def kpi(kid, name, layer, driver, status, value, unit, num, den, base, formula,
        source, link, evidence, strength, why, limitation, upgrade, ci=None):
    KPI.append(dict(kpi_id=kid, kpi_name=name, layer=layer, driver=driver, status=status,
                    value=value, unit=unit, numerator=num, denominator=den, base=base,
                    formula=formula, data_source=source, evidence_link=link,
                    evidence_type=evidence, evidence_strength=strength,
                    why_good_indicator=why, limitation=limitation, what_would_upgrade_it=upgrade,
                    ci_lo=None if ci is None else round(ci[0], 1),
                    ci_hi=None if ci is None else round(ci[1], 1)))


SURVEY_LINK = "data/cleaned_survey.csv"
AUDIT_LINK = "data/audit_pairs.csv"
SHEET = ("https://docs.google.com/spreadsheets/d/"
         "1YWjzxcGNsEWhM_OT1PHFhGa9Eb2b0EegY63qz5q-7G8/edit")

# =====================================================================
# NORTH STAR
# =====================================================================
kpi("NS", "D30 Retained Order Rate", "NORTH STAR", "RETENTION", "NOT COMPUTABLE",
    None, "orders/user/30d", None, None,
    "Would be: Ownly first-time users in Gachibowli",
    "D30 repeat rate (%) x average 30-day order frequency among retained users",
    "Ownly transaction logs — not available to this study",
    "01_secondary_research/challenger_failures/C_unit_economics_and_structure.md",
    "COMPANY DATA REQUIRED", "N/A",
    "It is the only metric that answers the actual question — does a cheaper first order become "
    "a habit. DoorDash reports the same construct publicly (cohort retention x frequency), and "
    "Rapido's own co-founder has said affordability is meant to drive repeat, frequency and "
    "retention rather than GOV. Awareness and trial are upstream proxies; this is the outcome.",
    "Requires per-user transaction history. No survey question can substitute — stated intent "
    "is not behaviour.",
    "Ownly cohort export: first-order date, subsequent order dates, per user.")

# =====================================================================
# INPUT KPIs — computable now
# =====================================================================
for view, kid in [("LIST+FEES", "K1a"), ("MEMBER", "K1b"), ("AFTER OFFER", "K1c")]:
    g = P[P["view"] == view]
    if not len(g):
        continue
    k, n = int(g["ownly_wins"].sum()), len(g)
    kpi(kid, f"Price Win Rate — {view}", "INPUT", "PRICE", "COMPUTED",
        round(k / n * 100, 1), "%", k, n, f"{n} matched restaurant x basket comparisons",
        "baskets where Ownly final payable is lowest / all matched baskets",
        "Price audit, wed_dinner, DP1 Gachibowli, 2026-09-16", AUDIT_LINK,
        "PRIMARY OBSERVED DATA", "DIRECTIONAL (n=4)",
        {"LIST+FEES": "The structural position: what Ownly's price looks like before any "
                      "incumbent benefit applies. This is the version Ownly controls.",
         "MEMBER": "What a Swiggy One or Zomato Gold holder actually sees. Since 82.5% of this "
                   "catchment holds a membership, this is most people's real checkout.",
         "AFTER OFFER": "What happens when a coupon lands. This is the version that decides "
                        "whether the price advantage survives a competitive response."}[view],
        "n=4 matched baskets, one slot, one address. Ownly on a new account with an intro offer; "
        "incumbents on subscribed accounts.",
        "More restaurants, a second slot, and a membership-holding Ownly account.")

g = P[P["view"] == "LIST+FEES"]
kpi("K2", "Median Basket Saving (structural)", "INPUT", "PRICE", "COMPUTED",
    round(g["saving_rs"].median(), 2), "INR", None, len(g), "4 matched baskets",
    "median(cheapest incumbent final payable - Ownly final payable), list+fees view",
    "Price audit", AUDIT_LINK, "PRIMARY OBSERVED DATA", "DIRECTIONAL (n=4)",
    "Converts the price claim into rupees, which is the unit the switching-threshold question "
    "is also measured in — so the two can be compared directly.",
    "Before any incumbent coupon or membership benefit.",
    "Expanded matched-basket audit.")

pr = A[A["priced"] == True]  # noqa: E712
own_nf = pr[pr.platform == "ownly"]["non_food_share"].median() * 100
inc_nf = pr[pr.platform.isin(["swiggy", "zomato"])]["non_food_share"].median() * 100
kpi("K3", "Fee Load — non-food share of bill", "INPUT", "PRICE", "COMPUTED",
    round(own_nf, 1), "%", None, int((pr.platform == "ownly").sum()),
    "Ownly priced captures", "(packaging+platform+delivery+small cart+surge+GST) / final payable",
    "Price audit", "data/audit_clean.csv", "PRIMARY OBSERVED DATA", "MODERATE",
    "The one advantage Ownly controls outright. Unlike a discount it survives without subsidy, "
    f"so it is the durable half of the price story. Incumbent median is {inc_nf:.1f}%.",
    "Median across priced captures; excludes menu-price differences.",
    "Capture across dayparts to confirm no surge is applied at peak.")

# --- assortment
cov = COV.set_index("restaurant_display")
n_frame = len(cov)
n_own = int(cov["on_ownly"].sum())
n_both = int((cov["on_ownly"] & cov["on_incumbent"]).sum())
n_only = int((cov["on_ownly"] & ~cov["on_incumbent"]).sum())
n_miss = int((~cov["on_ownly"] & cov["on_incumbent"]).sum())

kpi("K4", "Audit-frame Restaurant Coverage", "INPUT", "ASSORTMENT", "COMPUTED",
    round(n_own / n_frame * 100, 1), "%", n_own, n_frame,
    f"{n_frame}-restaurant audit frame, usable slots only",
    "restaurants listed on Ownly / restaurants in the audit frame",
    "Price audit (thu_lunch pass excluded, rule R4)", "data/audit_coverage.csv",
    "PRIMARY OBSERVED DATA", "DIRECTIONAL (frame of 10)",
    "Assortment is the attribute respondents refused to trade for money, so coverage is the "
    "constraint most likely to cap adoption.",
    "This is AUDIT-FRAME coverage, NOT Gachibowli market coverage. The frame was built from "
    "Ownly's own showcase page plus incumbent chains, so it selects for restaurants present "
    "everywhere and cannot detect exclusives.",
    "A long-tail pass: 25-30 restaurants sampled from Ownly's own 221-item list, checked on "
    "Swiggy and Zomato.")

kpi("K5", "Cross-platform Assortment Overlap", "INPUT", "ASSORTMENT", "COMPUTED",
    round(n_both / n_own * 100, 1), "%", n_both, n_own, "Restaurants listed on Ownly",
    "restaurants on Ownly AND >=1 incumbent / restaurants on Ownly",
    "Price audit", "data/audit_coverage.csv", "PRIMARY OBSERVED DATA", "DIRECTIONAL",
    "Directly tests the 'no new use case' risk that killed earlier challengers: if the catalogue "
    "is the same, price is the only differentiator left.",
    f"Frame of {n_frame}. {n_only} Ownly-only and {n_miss} missing-from-Ownly observed.",
    "Long-tail coverage pass.")

kpi("K6", "Preferred-Restaurant Coverage", "INPUT", "ASSORTMENT", "NOT COMPUTABLE",
    None, "%", None, None, "Would be: respondents' own most-ordered restaurants",
    "respondents' top/last-used restaurants available on Ownly / their top restaurants",
    "Survey does not capture named restaurants", SURVEY_LINK,
    "INSTRUMENT GAP", "N/A",
    "Generic coverage counts restaurants; this counts the ones a person actually uses. Because "
    "61.8% will not trade their usual restaurants for ₹30, this is the version of coverage that "
    "predicts behaviour.",
    "The live instrument never asks respondents to name their usual restaurants.",
    "Add one question: 'name the 3 places you order from most', then check each on Ownly.")

# --- service
eta_own = A[A.platform == "ownly"]["eta_mid"].median()
eta_inc = A[A.platform.isin(["swiggy", "zomato"])]["eta_mid"].median()
kpi("K7", "Quoted ETA Gap vs incumbents", "INPUT", "SERVICE", "COMPUTED",
    round(eta_own - eta_inc, 1), "min", None, int(A["eta_mid"].notna().sum()),
    "All captures showing an ETA", "median(Ownly quoted ETA) - median(incumbent quoted ETA)",
    "Price audit", "data/audit_clean.csv", "PRIMARY OBSERVED DATA", "MODERATE",
    "Quantifies what the saving costs in time. The gap is flat across all four restaurants "
    "(+17.5 to +24 min), which is the signature of a supply-density problem rather than a "
    "logistics one — see H-OUTLET.",
    "QUOTED ETA, not delivery performance. No test orders were placed, so on-time rate is unknown.",
    "3 test orders recording promised vs actual; and outlet name/distance per platform.")

kpi("K8", "Delivery Experience Parity (on-time, cancellation)", "INPUT", "SERVICE",
    "NOT COMPUTABLE", None, "%", None, None, "Would be: real Ownly orders",
    "orders delivered within promised ETA / total orders; and cancellation rate",
    "Requires placed orders or platform data", "06_competitor_audit/test_orders_template.csv",
    "COMPANY DATA / FIELD WORK REQUIRED", "N/A",
    "Interviews say people leave an app after repeated bad orders, so fulfilment reliability is "
    "the retention guardrail. A quoted ETA cannot measure it.",
    "The 3 budgeted test orders were never placed; template is empty.",
    "Place the 3 test orders; or obtain Ownly's on-time and cancellation rates.")

# --- distribution
rap = BASE[BASE["rapido_food_seen"].notna()
           & ~BASE["rapido_food_seen"].eq("I don't use the Rapido app")]
k = int(rap["rapido_food_seen"].eq("Yes").sum())
pct, lo, hi = wilson(k, len(rap))
kpi("K9", "Rapido Food Discovery Rate", "INPUT", "DISTRIBUTION", "COMPUTED",
    round(pct, 1), "%", k, len(rap), "Catchment respondents who use Rapido",
    "noticed food inside the Rapido app / Rapido users ('Not sure' counted as not noticed)",
    "Survey", SURVEY_LINK, "SURVEY — STATED BEHAVIOUR", "MODERATE",
    "Rapido's user base is the cheapest acquisition asset Ownly has. This separates access "
    "(they are in the app) from discovery (they noticed the product). Interviews say trial "
    "actually comes from friends and creators, not placement — so this tests the assumption.",
    "Self-reported noticing, subject to recall.",
    "In-app exposure-to-first-order analytics from Rapido.", ci=(lo, hi))

kpi("K10", "Rapido -> Ownly Trial Conversion", "INPUT", "DISTRIBUTION", "NOT COMPUTABLE",
    None, "%", None, None, "Would be: Rapido users exposed to the Ownly entry point",
    "Ownly first orders / Rapido users exposed to the Ownly entry point",
    "Requires Rapido funnel analytics", "data/kpi_table.csv",
    "COMPANY DATA REQUIRED", "N/A",
    "Tests whether the distribution advantage converts, which is the single biggest claimed "
    "asset of the Ownly model. Uber Eats had the same amortised-fleet logic and it did not save it.",
    "No exposure or browse data exists outside Rapido.",
    "Rapido: impressions of the food entry point -> browse -> first order.")

# --- lock-in
for kid, col, nm, why, lim in [
    ("K11", "has_membership", "Incumbent Membership Lock-in",
     "Members never see Ownly's list-price advantage — a membership converts a structural saving "
     "into no saving at all. It is the single largest barrier measured in this study.",
     "Membership held, not necessarily used."),
    ("K12", "multihoming", "Multi-homing Rate",
     "A multi-homing market lets Ownly become a secondary app before it becomes a main one, which "
     "is a lower bar than switching. It also means trial does not imply displacement.",
     "Based on self-reported 4-week order counts.")]:
    s = BASE[col].dropna().astype(bool)
    pct, lo, hi = wilson(int(s.sum()), len(s))
    kpi(kid, nm, "INPUT", "LOCK-IN", "COMPUTED", round(pct, 1), "%", int(s.sum()), len(s),
        f"Catchment respondents (n={len(s)})",
        f"{col} = true / respondents answering", "Survey", SURVEY_LINK,
        "SURVEY — STATED BEHAVIOUR", "MODERATE", why, lim,
        "Larger sample; confirm active use of the membership.", ci=(lo, hi))

thr = BASE["switch_savings_rs"].dropna()
kpi("K13", "Required Recurring Saving to Switch (median)", "INPUT", "LOCK-IN", "COMPUTED",
    float(thr.median()), "INR", None, len(thr),
    f"Catchment respondents naming a rupee figure (n={len(thr)}); "
    f"{int(BASE['switch_never'].sum())} said no amount, {int(BASE['switch_dk'].sum())} don't know",
    "median of stated recurring saving needed to change main app",
    "Survey", SURVEY_LINK, "SURVEY — STATED PREFERENCE", "MODERATE",
    "Defines the bar Ownly's price advantage has to clear. Paired with the observed saving it "
    "becomes Switch-Threshold Coverage (MM3), which is the most decision-relevant metric here.",
    "Stated threshold, not observed switching. 'No amount' and 'don't know' are held out of the "
    "median and reported separately rather than coded as zero or infinity.",
    "Behavioural test: vary the discount and observe actual switching.")

# =====================================================================
# OUTPUT KPIs
# =====================================================================
for kid, col, nm, why in [
    ("K14", "ownly_aware", "Ownly Awareness", "Top of funnel. Ownly is weeks old in Hyderabad, so "
     "this is the ceiling on everything downstream."),
    ("K15", "ownly_opened", "Ownly Browse Rate", "Stronger than awareness — it is an action, and "
     "it separates 'heard of it' from 'looked at it'."),
    ("K16", "ownly_says_ordered", "Ownly Trial Rate", "The first behavioural step. Low base, so "
     "reported as directional.")]:
    s = BASE[col].dropna().astype(bool)
    pct, lo, hi = wilson(int(s.sum()), len(s))
    kpi(kid, nm, "OUTPUT", "FUNNEL", "COMPUTED", round(pct, 1), "%", int(s.sum()), len(s),
        f"Catchment respondents (n={len(s)})", f"{col} / all catchment respondents",
        "Survey", SURVEY_LINK, "SURVEY — STATED BEHAVIOUR",
        "DIRECTIONAL — LOW BASE" if col == "ownly_says_ordered" else "MODERATE", why,
        "Self-reported. Trial base is very small.",
        "Larger sample; Ownly's own first-order counts for the pincode.", ci=(lo, hi))

conf = int(BASE["ownly_order_conflict"].sum())
kpi("K17", "Ownly Recent Order Count", "OUTPUT", "FUNNEL", "PARTIALLY UNAVAILABLE",
    None, "orders", None, None, "Catchment respondents",
    "sum of self-reported Ownly orders in the last 4 weeks",
    "Survey — conflicting responses", SURVEY_LINK, "SURVEY — STATED BEHAVIOUR", "UNUSABLE",
    "Would be the cleanest adoption signal available without company data.",
    f"{conf} respondents said they had ordered on Ownly AND that their first order was within the "
    "last 4 weeks, while entering 0 orders for that same window. Those fields contradict each "
    "other, so the count is reported as UNAVAILABLE rather than as zero adoption. The 4-week "
    "window also mostly predates Ownly's Hyderabad go-live (NRAI launch 22 Jul 2026; on-ground "
    "September 2026), so a zero here would measure the question window, not rejection.",
    "Ask recent-order count with an explicit 'since Ownly launched here' anchor.")

s = BASE["repeat_no_promo_n"].dropna()
k = int((s >= 4).sum())
pct, lo, hi = wilson(k, len(s))
kpi("K18", "Post-Promotion Repeat Intent", "OUTPUT", "RETENTION", "COMPUTED (PROXY)",
    round(pct, 1), "%", k, len(s), f"Catchment respondents (n={len(s)})",
    "top-2 box on 'once the ₹100 first-order offer ended, would you keep using it'",
    "Survey", SURVEY_LINK, "SURVEY — STATED PREFERENCE", "PROXY ONLY",
    "The closest available stand-in for the North Star. It asks the rented-demand question "
    "directly: does the behaviour survive the subsidy. Foodpanda went from ~200k to ~5k daily "
    "orders when discounts stopped, so this is the failure mode worth measuring.",
    "STATED INTENT, not retention. People overstate future good behaviour.",
    "Observed second-order rate among promo-acquired users.", ci=(lo, hi))

s = BASE["durability_doubt_n"].dropna()
k = int((s >= 4).sum())
pct, lo, hi = wilson(k, len(s))
kpi("K19", "Price-Durability Doubt", "OUTPUT", "RETENTION", "COMPUTED",
    round(pct, 1), "%", k, len(s), f"Catchment respondents (n={len(s)})",
    "agree + strongly agree that a new app's low prices rise once it becomes popular",
    "Survey", SURVEY_LINK, "SURVEY — STATED PREFERENCE", "STRONG",
    "A price proposition only works if it is believed. This measures whether the market has "
    "already priced in the fee creep it has seen from every previous challenger.",
    "Attitudinal. Does not by itself predict behaviour.",
    "Test whether doubt predicts non-trial in a behavioural experiment.", ci=(lo, hi))

# trade-offs
TRADE = [("eta_chose_cheap", "K20", "speed", "wait 15 minutes longer"),
         ("rel_chose_cheap", "K21", "reliability", "accept 3-in-10 late instead of 1-in-10"),
         ("rest_chose_cheap", "K22", "usual restaurants", "give up most usual restaurants")]
trade_rows = []
for col, kid, dim, desc in TRADE:
    s = BASE[col].dropna().astype(bool)
    pct, lo, hi = wilson(int(s.sum()), len(s))
    kpi(kid, f"Will trade {dim} for ₹30", "OUTPUT", "TRADE-OFF", "COMPUTED",
        round(pct, 1), "%", int(s.sum()), len(s), f"Catchment respondents (n={len(s)})",
        f"chose the ₹230 option over ₹260 / respondents answering",
        "Survey", SURVEY_LINK, "SURVEY — STATED PREFERENCE", "STRONG (paired design)",
        f"Holds ₹30 constant and varies only what is given up, so differences are attributable "
        f"to the attribute rather than to price sensitivity. Tests whether users will {desc}.",
        "Constructed choice at a single price point; not observed behaviour.",
        "Repeat at ₹20/₹50/₹75 to build a trade-off curve.", ci=(lo, hi))
    trade_rows.append(dict(dimension=dim, description=desc, chose_cheaper_k=int(s.sum()),
                           n=len(s), chose_cheaper_pct=round(pct, 1), ci_lo=round(lo, 1),
                           ci_hi=round(hi, 1), paid_premium_pct=round(100 - pct, 1)))
pd.DataFrame(trade_rows).to_csv(f"{D}/tradeoff_summary.csv", index=False)

kpi("K23", "Contribution Margin per Repeat Order", "GUARDRAIL", "ECONOMICS", "NOT COMPUTABLE",
    None, "INR", None, None, "Would be: Ownly per-order P&L",
    "revenue per order - variable delivery, payment and support cost per order",
    "Requires Ownly internal cost data",
    "01_secondary_research/challenger_failures/A_ubereats_foodpanda.md",
    "COMPANY DATA REQUIRED", "N/A",
    "The guardrail that separates growth from burn. Uber Eats India lost $2.55 per order against "
    "a $2.45 average order value — it lost more per order than the order was worth. Any repeat "
    "rate is meaningless without this. Our audit observed Ownly charging ₹0 delivery, ₹0 "
    "platform and ₹0 packaging while taking 0% commission, so observed revenue per order in "
    "Gachibowli was ₹0.",
    "Ownly has never published per-order economics; no figure exists in any source.",
    "Ownly internal: revenue and variable cost per order.")

# ---- map every entry onto the 8-KPI framework so the register and the framework agree
FAMILY = {
    "NS":  (0, "North Star — D30 Retained Order Rate"),
    "K1a": (2, "2 · Recurring Price-Advantage Coverage"),
    "K1b": (2, "2 · Recurring Price-Advantage Coverage"),
    "K1c": (2, "2 · Recurring Price-Advantage Coverage"),
    "K2":  (2, "2 · Recurring Price-Advantage Coverage"),
    "K3":  (2, "2 · Recurring Price-Advantage Coverage"),
    "K13": (3, "3 · Required Recurring Saving to Switch"),
    "K4":  (4, "4 · Preferred-Restaurant Coverage"),
    "K5":  (4, "4 · Preferred-Restaurant Coverage"),
    "K6":  (4, "4 · Preferred-Restaurant Coverage"),
    "K7":  (5, "5 · Delivery Experience Parity"),
    "K8":  (5, "5 · Delivery Experience Parity"),
    "K9":  (6, "6 · Rapido Discovery-to-Trial Conversion"),
    "K10": (6, "6 · Rapido Discovery-to-Trial Conversion"),
    "K18": (7, "7 · Post-Promotion Repeat Rate"),
    "K19": (7, "7 · Post-Promotion Repeat Rate"),
    "K23": (8, "8 · Contribution Margin per Repeat Order"),
}
SUPPORT = (9, "Supporting measures — market conditions and funnel")
_k = pd.DataFrame(KPI)
_k["family_order"] = _k["kpi_id"].map(lambda i: FAMILY.get(i, SUPPORT)[0])
_k["family"] = _k["kpi_id"].map(lambda i: FAMILY.get(i, SUPPORT)[1])
_k["is_headline"] = _k["kpi_id"].isin(["NS", "K1a", "K13", "K4", "K7", "K9", "K18", "K23"])
_k = _k.sort_values(["family_order", "kpi_id"])
_k.to_csv(f"{D}/kpi_table.csv", index=False)

# =====================================================================
# DERIVED MARKETING METRICS
# =====================================================================
def mm(mid, name, sheet_ref, formula, status, value, unit, num, den, base, source, link,
       evidence, interp, caveat):
    MM.append(dict(metric_id=mid, metric_name=name, formula_sheet_reference=sheet_ref,
                   formula=formula, status=status, value=value, unit=unit, numerator=num,
                   denominator=den, base=base, data_source=source, evidence_link=link,
                   evidence_type=evidence, interpretation=interp, caveat=caveat))


gl = P[P["view"] == "LIST+FEES"]
gm = P[P["view"] == "MEMBER"]
go = P[P["view"] == "AFTER OFFER"]

# MM1 Switch-Threshold Coverage (the headline derived metric)
rows = []
for v, g in [("LIST+FEES", gl), ("MEMBER", gm), ("AFTER OFFER", go)]:
    hit = tot = 0
    for _, b in g.iterrows():
        hit += int((thr <= b["saving_rs"]).sum())
        tot += len(thr)
    rows.append(dict(view=v, pairs_clearing=hit, pairs_total=tot,
                     coverage_pct=round(hit / tot * 100, 1) if tot else np.nan,
                     median_saving_rs=round(g["saving_rs"].median(), 2)))
STC = pd.DataFrame(rows)
STC.to_csv(f"{D}/switch_threshold_coverage.csv", index=False)

mm("MM1", "Switch-Threshold Coverage", "derived (combines K13 x K1/K2)",
   "respondent x basket pairs where observed Ownly saving >= that respondent's stated required "
   "recurring saving / all such pairs",
   "COMPUTED", float(STC.loc[STC.view == "LIST+FEES", "coverage_pct"].iloc[0]), "%",
   int(STC.loc[STC.view == "LIST+FEES", "pairs_clearing"].iloc[0]),
   int(STC.loc[STC.view == "LIST+FEES", "pairs_total"].iloc[0]),
   f"{len(thr)} threshold-giving catchment respondents x {len(gl)} matched baskets",
   "Survey x price audit", "data/switch_threshold_coverage.csv",
   "SURVEY — STATED PREFERENCE x PRIMARY OBSERVED DATA",
   f"Falls {STC.coverage_pct.iloc[0]:.0f}% -> {STC.coverage_pct.iloc[1]:.0f}% -> "
   f"{STC.coverage_pct.iloc[2]:.0f}% across the three price views. This is the study's central "
   "number: it answers 'is the saving big enough for these people' rather than 'is Ownly cheaper'.",
   "Cross-product of a stated threshold and an observed price; n=4 baskets. Not a conversion rate.")

# MM2 Offer Reversal / MM3 Membership Erosion
rev = gl.merge(go, on=["restaurant_display", "basket_id"], suffixes=("_l", "_o"))
r_n = int((rev["ownly_wins_l"] & ~rev["ownly_wins_o"]).sum())
mm("MM2", "Offer Reversal Rate", "custom",
   "baskets Ownly wins on list+fees but loses after incumbent coupons / matched baskets",
   "COMPUTED", round(r_n / len(rev) * 100, 1), "%", r_n, len(rev), f"{len(rev)} matched baskets",
   "Price audit", AUDIT_LINK, "PRIMARY OBSERVED DATA",
   "Measures how much of the structural advantage a coupon can erase on any given day.",
   "n=4. Ownly held a new-account intro offer; incumbents held memberships.")

mem = gl.merge(gm, on=["restaurant_display", "basket_id"], suffixes=("_l", "_m"))
m_n = int((mem["ownly_wins_l"] & ~mem["ownly_wins_m"]).sum())
mm("MM3", "Membership Erosion Rate", "custom",
   "baskets Ownly wins on list+fees but loses once the incumbent MEMBERSHIP benefit alone "
   "applies, before any coupon / matched baskets",
   "COMPUTED", round(m_n / len(mem) * 100, 1), "%", m_n, len(mem), f"{len(mem)} matched baskets",
   "Price audit", AUDIT_LINK, "PRIMARY OBSERVED DATA",
   "Isolates the DURABLE half of the erosion. A membership is a standing benefit applying to "
   "every order; a coupon is episodic. Ownly can out-wait a coupon, not a subscription — and "
   f"{round(BASE['has_membership'].mean()*100)}% of this catchment holds one.",
   "n=4 baskets.")

# MM4 Sample Volume Share (Sheet 1: Unit Market Share)
def vol_share(d, label):
    """Uses n_ownly_usable, so respondents whose Ownly count contradicts their own
    other answers are EXCLUDED from the numerator rather than counted as zero."""
    cols = ["n_swiggy", "n_zomato", "n_other"]
    unusable = int(d["ownly_order_conflict"].sum())
    own = d["n_ownly_usable"].sum()
    tot = d[cols].sum().sum() + own
    return dict(base=label, ownly_orders_usable=float(own),
                ownly_counts_unusable=unusable,
                total_orders=float(tot),
                volume_share_pct=round(own / tot * 100, 2) if tot else np.nan,
                bound="LOWER BOUND — unusable counts excluded" if unusable else "complete",
                swiggy_pct=round(d["n_swiggy"].sum() / tot * 100, 1) if tot else np.nan,
                zomato_pct=round(d["n_zomato"].sum() / tot * 100, 1) if tot else np.nan,
                other_pct=round(d["n_other"].sum() / tot * 100, 1) if tot else np.nan)


VS = pd.DataFrame([vol_share(CATCH, "Gachibowli catchment"), vol_share(HYD, "Hyderabad eligible"),
                   vol_share(BLR, "Bengaluru (benchmark)")])
VS.to_csv(f"{D}/sample_volume_share.csv", index=False)
cv = VS.iloc[0]
bv = VS[VS.base == "Bengaluru (benchmark)"].iloc[0]
mm("MM4", "Sample Volume Share (Unit Market Share)", "Sheet 1 — Unit Market Share / Volume Share",
   "Ownly orders in last 4 weeks / all delivery orders in last 4 weeks, WITHIN THE SAMPLE. "
   "Respondents whose Ownly count contradicts their own other answers are excluded from the "
   "numerator, not counted as zero — so the catchment figure is a LOWER BOUND.",
   "COMPUTED (SAMPLE ONLY — LOWER BOUND)", float(cv["volume_share_pct"]), "%",
   float(cv["ownly_orders_usable"]), float(cv["total_orders"]),
   f"Self-reported 4-week order counts, catchment (n={len(CATCH)}); "
   f"{int(cv['ownly_counts_unusable'])} Ownly count excluded as unusable",
   "Survey", "data/sample_volume_share.csv", "SURVEY — STATED BEHAVIOUR",
   f"In this catchment sample Swiggy takes {cv['swiggy_pct']}% and Zomato {cv['zomato_pct']}% of "
   f"reported orders. Ownly's usable count is {cv['ownly_orders_usable']:.0f} orders, with "
   f"{int(cv['ownly_counts_unusable'])} response unusable, so its share is a lower bound rather "
   f"than a measured zero. Bengaluru — live far longer — shows {bv['volume_share_pct']}%, which is "
   "what early traction looks like when it exists.",
   "THIS IS NOT MARKET SHARE. It is share of orders inside a small convenience sample. The "
   "formula-sheet Volume Share needs total market unit sales, which this study does not have. "
   "Ownly has been live in Hyderabad for weeks, so a low share here is expected and is NOT "
   "evidence of rejection.")

# MM5 Penetration Share (Sheet 1)
brand_pen = BASE["ownly_says_ordered"].fillna(False).mean() * 100
mkt_pen = BASE["recent_orderer"].mean() * 100
mm("MM5", "Penetration Share", "Sheet 1 — Penetration Share",
   "Brand Penetration (%) / Market Penetration (%) = Ownly triers / category orderers",
   "COMPUTED (SAMPLE ONLY)", round(brand_pen / mkt_pen * 100, 1), "%",
   int(BASE["ownly_says_ordered"].fillna(False).sum()), int(BASE["recent_orderer"].sum()),
   f"Catchment (n={len(BASE)})", "Survey", SURVEY_LINK, "SURVEY — STATED BEHAVIOUR",
   f"Of the people in this sample who order food delivery at all, "
   f"{brand_pen/mkt_pen*100:.1f}% have ever tried Ownly. The formula-sheet version uses total "
   "population as the denominator; here the denominator is the sample, so it is a within-sample "
   "penetration share.",
   "Sample, not population. 'Ever tried' not 'active user'. Very low base.")

# MM6 Share of Requirements (Sheet 1)
users = S[(S["ownly_says_ordered"].fillna(False)) & (S["n_ownly"].fillna(0) > 0)]
if len(users):
    sor = users["n_ownly"].sum() / users[["n_swiggy", "n_zomato", "n_ownly", "n_other"]].sum().sum()
    mm("MM6", "Unit Share of Requirements", "Sheet 1 — Unit Share of Requirements",
       "Ownly orders / total category orders BY OWNLY USERS",
       "COMPUTED (VERY LOW BASE)", round(sor * 100, 1), "%",
       float(users["n_ownly"].sum()),
       float(users[["n_swiggy", "n_zomato", "n_ownly", "n_other"]].sum().sum()),
       f"Respondents with >0 Ownly orders in 4 weeks (n={len(users)}, all cities)",
       "Survey", SURVEY_LINK, "SURVEY — STATED BEHAVIOUR",
       "Among people who actually use Ownly, what share of their delivery ordering it captures. "
       "This is the closest available proxy for the frequency half of the North Star.",
       f"n={len(users)} users across all cities. Directional only; cannot be reported by city.")

# MM7 Assortment Barrier Rate
s = BASE["rest_chose_cheap"].dropna().astype(bool)
k = int((~s).sum())
pct, lo, hi = wilson(k, len(s))
mm("MM7", "Assortment Barrier Rate", "custom",
   "respondents paying the ₹30 premium to keep most usual restaurants / respondents shown the item",
   "COMPUTED", round(pct, 1), "%", k, len(s), f"Catchment (n={len(s)})",
   "Survey", SURVEY_LINK, "SURVEY — STATED PREFERENCE",
   f"[95% CI {lo:.0f}-{hi:.0f}%] The highest refusal of the three ₹30 trades — the one thing "
   "money could not buy in this sample.",
   "Constructed choice, not observed behaviour.")

# MM8 Rapido Discovery Gap
k = int((~rap["rapido_food_seen"].eq("Yes")).sum())
pct, lo, hi = wilson(k, len(rap))
mm("MM8", "Rapido Discovery Gap", "custom",
   "Rapido users who have NOT noticed food in the app / Rapido users",
   "COMPUTED", round(pct, 1), "%", k, len(rap), f"Catchment Rapido users (n={len(rap)})",
   "Survey", SURVEY_LINK, "SURVEY — STATED BEHAVIOUR",
   f"[95% CI {lo:.0f}-{hi:.0f}%] Distribution exists; discovery largely does not.",
   "'Not sure' counted as not-noticed.")

# MM9 Trial-to-Repeat Intent Gap
ti = BASE["prop_P_intent_n"].dropna()
tk = int((ti >= 4).sum())
ri = BASE["repeat_no_promo_n"].dropna()
rk = int((ri >= 4).sum())
mm("MM9", "Trial-to-Repeat Intent Gap", "custom",
   "(% top-2 likely to TRY) - (% top-2 likely to CONTINUE after the intro offer ends)",
   "COMPUTED (PROXY)", round(tk / len(ti) * 100 - rk / len(ri) * 100, 1), "pp", None, len(BASE),
   f"Catchment (n={len(BASE)})", "Survey", SURVEY_LINK, "SURVEY — STATED PREFERENCE",
   f"Trial intent {tk/len(ti)*100:.0f}% vs post-offer continuation {rk/len(ri)*100:.0f}%. The "
   "size of the drop is the rented-demand risk expressed in this sample's own words.",
   "STATED INTENT PROXY. The two items use different framings, so part of the gap is framing.")

# MM10 Fee Load Advantage
mm("MM10", "Fee Load Advantage", "custom",
   "median incumbent non-food share of bill - median Ownly non-food share",
   "COMPUTED", round(inc_nf - own_nf, 1), "pp", None, int(pr.shape[0]),
   f"{int(pr.shape[0])} priced captures", "Price audit", "data/audit_clean.csv",
   "PRIMARY OBSERVED DATA",
   "Expresses Ownly's structural edge as the share of the bill that is not food. It survives "
   "without subsidy, unlike a discount — and it is invisible to the customer unless stated, "
   "which ties the metric to the communication problem.",
   "Median across priced captures; excludes menu-price differences.")

pd.DataFrame(MM).to_csv(f"{D}/marketing_metrics.csv", index=False)

# ---- formula-sheet metrics we deliberately do NOT compute
NC = [
    ("Value Share / Revenue Market Share", "Sheet 1",
     "Needs total market revenue for Gachibowli food delivery. No such figure exists publicly, "
     "and a 40-person convenience sample cannot stand in for it."),
    ("Relative Market Share", "Sheet 1",
     "Requires a credible market share for Ownly and for the largest competitor. See above."),
    ("Brand / Category Development Index", "Sheet 1",
     "Requires category and brand sales per household by group. Not available at any level."),
    ("Contribution Margin, Break-even, Target Volume", "Sheet 1",
     "Requires Ownly's variable cost and fixed cost per order. Never published."),
    ("Retention Rate", "Sheet 2",
     "Requires customers at start, customers at end and new customers over a period. The survey "
     "is a single cross-section."),
    ("Customer Lifetime Value", "Sheet 2",
     "Requires margin and retention rate. Both unavailable."),
    ("Average Acquisition Cost (CAC)", "Sheet 2",
     "Requires acquisition spending and number of new customers acquired. Circulating ₹400-600 "
     "figures trace only to low-quality blogs and are not used."),
    ("Average Retention Cost (CRC)", "Sheet 2",
     "Requires retention spending and number retained."),
    ("EBITDA", "course list",
     "A company-level P&L measure. Ownly does not report separately from Rapido."),
    ("YoY Growth / CAGR", "Sheet 2",
     "Requires a prior-period value for the same metric and market. Ownly has been live in "
     "Hyderabad for weeks."),
]
pd.DataFrame(NC, columns=["metric", "formula_sheet", "why_not_computable"]).assign(
    status="NOT ESTIMABLE FROM AVAILABLE EVIDENCE",
    where_it_would_come_from="Ownly / Rapido internal data, or a commissioned market study"
).to_csv(f"{D}/not_estimable.csv", index=False)

# ------------------------------------------------------------------- console
K = pd.DataFrame(KPI)
print(f"BASE = Gachibowli catchment, n={NB}  (Gachibowli proper {len(GACH)}, HYD {len(HYD)}, BLR {len(BLR)})")
print(f"\nKPI REGISTER: {len(K)} entries")
print(K["status"].value_counts().to_string())
print("\n--- COMPUTED KPIs ---")
c = K[K["status"].str.startswith("COMPUTED")]
print(c[["kpi_id", "kpi_name", "value", "unit", "numerator", "denominator",
         "evidence_strength"]].to_string(index=False))
print("\n--- NOT COMPUTABLE (need company data / instrument change) ---")
print(K[~K["status"].str.startswith("COMPUTED")][["kpi_id", "kpi_name", "status"]]
      .to_string(index=False))
print("\n--- SWITCH-THRESHOLD COVERAGE ---")
print(STC.to_string(index=False))
print("\n--- SAMPLE VOLUME SHARE ---")
print(VS.to_string(index=False))
print(f"\n--- MARKETING METRICS: {len(MM)} ---")
print(pd.DataFrame(MM)[["metric_id", "metric_name", "status", "value", "unit"]]
      .to_string(index=False))
