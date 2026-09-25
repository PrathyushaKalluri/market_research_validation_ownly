"""
04_themes_evidence_dictionary.py
Aggregates coded review/social themes, builds the evidence triangulation matrix,
the metric dictionary, and the interview placeholder (interviews were NOT conducted).

Review/social counts are SHARES OF CODED ITEMS MENTIONING A THEME.
They are NOT order failure rates and must never be presented as such.
"""
import os
import numpy as np
import pandas as pd

ROOT = "/Users/klprathyusha/Sem 3/Project/Ownly"
D = f"{ROOT}/final_dashboard/data"

REV = pd.read_csv(f"{ROOT}/05_review_mining/app_stores/reviews_coded.csv")
SOC = pd.read_csv(f"{ROOT}/05_review_mining/social/social_coded.csv")

FAMILY = {
    "PRICE_ADVANTAGE": ["PRICE_SAVINGS_OBSERVED", "USER_BILL_COMPARISON", "NO_HIDDEN_FEES",
                        "PRICE_ADVANTAGE", "CHEAPER", "FEE_MODEL_DESCRIPTION"],
    "PRICE_DOUBT": ["FUTURE_FEE_CREEP_EXPECTED", "SUSTAINABILITY_SKEPTICISM",
                    "HISTORICAL_PRICE_CONVERGENCE", "MENU_PRICE_INFLATION_ON_OWNLY",
                    "INCUMBENT_CHEAPER_AFTER_OFFERS", "OWNLY_PRICIER_OBSERVED",
                    "PRICE_PARITY_OBSERVED", "ASTROTURF_SUSPICION"],
    "FULFILMENT_FAIL": ["NON_DELIVERY", "LATE_DELIVERY", "PLATFORM_RESTAURANT_CANCELLATION",
                        "MISSING_WRONG_ITEMS", "RIDER_CONDUCT", "LATE_NIGHT_RELIABILITY_RISK",
                        "LARGE_ORDER_TRUST_RISK", "RIDER_MULTI_APP_OBSERVED"],
    "SUPPORT_REFUND": ["SUPPORT_UNRESPONSIVE", "SUPPORT_SLOW", "REFUND_ISSUE",
                       "TRUST_LOSS_SCAM_FRAMING"],
    "ASSORTMENT": ["ASSORTMENT_LIMITED", "SERVICE_AREA_LIMITED", "CITY_AVAILABILITY_QUESTION"],
    "TRUST_QUALITY": ["FOOD_QUALITY", "HYGIENE", "TRUST_QUALITY"],
    "COMPETITION": ["TOING_VS_OWNLY", "COMPETITION", "LOW_PLATFORM_LOYALTY"],
    "DISTRIBUTION": ["RAPIDO_ECOSYSTEM", "LAUNCH_CLAIM_RELAY", "DISTRIBUTION"],
}


def fam_of(theme_str):
    out = set()
    if pd.isna(theme_str):
        return out
    for t in str(theme_str).replace("|", ";").split(";"):
        t = t.strip().upper()
        if not t:
            continue
        for fam, keys in FAMILY.items():
            if t in keys or any(t.startswith(k) for k in keys):
                out.add(fam)
    return out


rows = []
# these coded flags are stored as strings ('0'/'1'/'ambiguous'), not integers
SOC["_rel"] = SOC["relevant"].astype(str).str.strip()
SOC["_fh"] = SOC["first_hand_ownly_use"].astype(str).str.strip()
soc_rel = SOC[SOC["_rel"] == "1"]
soc_fh = soc_rel[soc_rel["_fh"] == "1"]
assert len(soc_rel) > 0 and len(soc_fh) > 0, "theme bases resolved empty - check flag encoding"

bases = {
    "Public discussion (social, relevant)": soc_rel,
    "First-hand Ownly accounts (social)": soc_fh,
    "App-store reviews": REV,
}
for base_name, frame in bases.items():
    fams = frame["themes"].apply(fam_of)
    n_with = int(fams.apply(lambda s: len(s) > 0).sum())
    for fam in FAMILY:
        k = int(fams.apply(lambda s: fam in s).sum())
        rows.append({"base": base_name, "theme_family": fam, "items_mentioning": k,
                     "base_n_with_any_theme": n_with, "base_n_total": len(frame),
                     "share_of_coded_items_pct": round(k / n_with * 100, 1) if n_with else np.nan})
T = pd.DataFrame(rows)
T["measure_definition"] = "share of coded items mentioning this theme family - NOT an order failure rate"
T.to_csv(f"{D}/review_theme_summary.csv", index=False)

# star distribution + severity
REV["star_rating"].value_counts().sort_index().rename_axis("star_rating") \
    .reset_index(name="n").to_csv(f"{D}/review_star_distribution.csv", index=False)

# ------------------------------------------------- interviews: CONDUCTED
# Source: 04_interviews/interview_findings_coded.md
# I-01 = documented transcript (Gemini notes, 2026-09-17). T-n = team-reported aggregate insights
# from an UNKNOWN number of further interviews -> no prevalence figures are emitted.
IV = [
    ("I-01.1", "PRICE_TRANSPARENCY", "documented transcript",
     "Core pain is unexpected charges at checkout; wants to know what she is actually paying",
     "CONVERGES with survey (89.1% expect prices to rise) and audit (5.2% vs 28.3% fee load)"),
    ("I-01.2", "TRUST_HYGIENE", "documented transcript",
     "Ratings measure taste, not hygiene; cannot inspect a kitchen through an app",
     "UNIQUE TO INTERVIEWS - no survey item measures this"),
    ("I-01.4", "SPEED_VS_PRICE_HUNGER", "documented transcript",
     "Speed preference flips with hunger: very hungry -> speed; otherwise -> price",
     "CONVERGES with survey (84.8% took cheaper+slower)"),
    ("I-01.5", "CHECKOUT_TRANSPARENCY", "documented transcript",
     "Chose Rs150 free-delivery app over Rs272 with extra charges, same item same restaurant",
     "CONVERGES with audit (Ownly 4/4 on list+fees)"),
    ("I-01.6", "SELF_SEGMENTATION", "documented transcript",
     "Premium customers value time over money; students and middle-class prioritise price",
     "PARTIALLY SUPPORTED - survey cannot detect the split (Fisher p=0.637, n=11 professionals)"),
    ("I-01.7", "GROUP_ORDERING", "documented transcript",
     "Students pool orders through whoever holds Zomato Gold / Swiggy One and compare totals",
     "CONVERGES - supplies the mechanism behind the 50% coupon reversal in the audit"),
    ("I-01.9", "WORD_OF_MOUTH_AWARENESS", "documented transcript",
     "Heard about Ownly from her brother; had not used it; unavailable at her location",
     "CONVERGES with 84.6% Rapido discovery gap - and reframes the lever"),
    ("I-01.10", "TOO_CHEAP_SIGNAL", "documented transcript",
     "A very low price raises a food-quality doubt ('if biryani is Rs100, is it good?')",
     "UNIQUE TO INTERVIEWS - a cost of the price-led claim the survey does not capture"),
    ("T-1", "TRADEOFF_HIERARCHY", "team-reported",
     "General: hunger, time >> money. Students: hunger, money >> time",
     "PARTIALLY SUPPORTED / UNDERPOWERED - threshold differs (Rs30 vs Rs50) but speed trade-off does not"),
    ("T-2", "PRICE_DURABILITY_DOUBT", "team-reported",
     "On Ownly's offers - 'what if they increase later'",
     "CONVERGES - 89.1% of survey agrees"),
    ("T-3", "PRICE_ANCHOR_PER_KM", "team-reported", "Rs10 per km is the reference for delivery pricing",
     "NOT TESTABLE - no distance data captured in the audit"),
    ("T-4", "TRIAL_TRIGGER_WOM", "team-reported",
     "Switching to a new app comes from a friend's recommendation, Instagram/YouTube reviews, ads",
     "CONVERGES - reframes discovery away from in-app placement"),
    ("T-5", "CHURN_TRIGGER_BAD_ORDERS", "team-reported",
     "People leave an app after frequent bad orders",
     "RESOLVES the survey-vs-reviews contradiction on reliability"),
    ("T-6", "TRUST_SOURCE", "team-reported", "Trust comes from influencers and word of mouth",
     "CONVERGES with T-4 and I-01.9"),
]
pd.DataFrame(IV, columns=["ref", "theme", "grade", "finding", "triangulation"]).assign(
    status="CONDUCTED",
    documented_transcripts=1,
    total_interviews="UNKNOWN - team reported further interviews; count not recorded",
    evidence_type="INTERVIEW (primary, qualitative)",
    prevalence_rule="NO percentages or interviewee counts reported - denominator unknown",
    verification="Gemini auto-notes; NOT human-verified verbatim; no double-coding, no Cohen's kappa",
).to_csv(f"{D}/interview_theme_summary.csv", index=False)

# ------------------------------------------------------- evidence matrix
def cell(v):
    return v


EM = [
    # dimension,            survey, interviews, audit, app reviews, social, secondary, challengers, interpretation
    ("Price advantage exists", "SUPPORTS", "SUPPORTS", "SUPPORTS", "MIXED", "MIXED",
     "MIXED", "SUPPORTS", "STRONG (structural view only)"),
    ("Price advantage survives offers", "NO EVIDENCE", "CONTRADICTS", "CONTRADICTS", "NO EVIDENCE",
     "CONTRADICTS", "MIXED", "CONTRADICTS", "MODERATE — erosion observed"),
    ("Assortment is the binding constraint", "SUPPORTS", "NO EVIDENCE", "SUPPORTS", "MIXED",
     "MIXED", "SUPPORTS", "SUPPORTS", "STRONG (survey + audit; interviews silent)"),
    ("Speed deficit blocks adoption", "CONTRADICTS", "CONTRADICTS", "SUPPORTS", "MIXED",
     "MIXED", "NO EVIDENCE", "SUPPORTS", "CONTRADICTED by survey AND interviews"),
    ("Reliability blocks TRIAL", "CONTRADICTS", "CONTRADICTS", "NO EVIDENCE", "MIXED",
     "MIXED", "NO EVIDENCE", "MIXED", "CONTRADICTED — accepted prospectively for ₹30"),
    ("Bad orders drive CHURN", "NO EVIDENCE", "SUPPORTS", "NO EVIDENCE", "SUPPORTS",
     "SUPPORTS", "NO EVIDENCE", "SUPPORTS", "STRONG — interviews supply the mechanism"),
    ("Support/refund is a risk", "NO EVIDENCE", "NO EVIDENCE", "NO EVIDENCE", "SUPPORTS",
     "SUPPORTS", "NO EVIDENCE", "SUPPORTS", "MODERATE (self-selected sources)"),
    ("Rapido creates real discovery", "CONTRADICTS", "CONTRADICTS", "NO EVIDENCE", "NO EVIDENCE",
     "MIXED", "MIXED", "CONTRADICTS", "STRONG — trial runs on word of mouth instead"),
    ("Membership lock-in is material", "SUPPORTS", "SUPPORTS", "SUPPORTS", "NO EVIDENCE",
     "SUPPORTS", "SUPPORTS", "SUPPORTS", "STRONG — interviews explain the mechanism"),
    ("Price durability is doubted", "SUPPORTS", "SUPPORTS", "NO EVIDENCE", "NO EVIDENCE",
     "SUPPORTS", "SUPPORTS", "SUPPORTS", "STRONG (near-universal in survey)"),
    ("Hygiene / food-quality trust", "NO EVIDENCE", "SUPPORTS", "NO EVIDENCE", "SUPPORTS",
     "MIXED", "NO EVIDENCE", "NO EVIDENCE", "DIRECTIONAL — survey is blind to this"),
    ("Very low price signals low quality", "NO EVIDENCE", "SUPPORTS", "NO EVIDENCE", "NO EVIDENCE",
     "MIXED", "NO EVIDENCE", "NO EVIDENCE", "DIRECTIONAL — a cost of the price-led claim"),
    ("Late-night availability gap", "NO EVIDENCE", "NO EVIDENCE", "MIXED", "NO EVIDENCE",
     "SUPPORTS", "NO EVIDENCE", "NO EVIDENCE", "DIRECTIONAL — supply gap only, demand unvalidated"),
    ("Rider supply is sustainable", "NO EVIDENCE", "NO EVIDENCE", "NO EVIDENCE", "NO EVIDENCE",
     "CONTRADICTS", "NO EVIDENCE", "CONTRADICTS", "DIRECTIONAL — the single largest public-comment theme"),
    ("Sustainable unit economics", "NO EVIDENCE", "NO EVIDENCE", "NO EVIDENCE", "NO EVIDENCE",
     "CONTRADICTS", "CONTRADICTS", "CONTRADICTS", "UNKNOWN for Ownly — not disclosed anywhere"),
]
pd.DataFrame(EM, columns=["dimension", "survey", "interviews", "price_audit", "app_reviews",
                          "social", "secondary_research", "challenger_history",
                          "current_interpretation"]).to_csv(f"{D}/evidence_matrix.csv", index=False)

# ------------------------------------------------------- metric dictionary
K = pd.read_csv(f"{D}/kpi_table.csv")
M = pd.read_csv(f"{D}/marketing_metrics.csv")
dict_rows = []
for _, r in K.iterrows():
    dict_rows.append({
        "metric_name": r["kpi_name"], "metric_id": r["kpi_id"], "kind": "KPI",
        "business_question": r["business_question"],
        "formula": "numerator / denominator" if pd.notna(r["numerator"]) else "median of observed values",
        "numerator": r["numerator"], "denominator": r["denominator"],
        "data_source": r["source"], "population": r["base"], "sample_size": r["denominator"],
        "evidence_type": r["evidence_type"],
        "limitations": "Stated preference is not behaviour; audit is n=4 matched baskets, one slot, "
                       "one address" if "SURVEY" in str(r["evidence_type"]) else
                       "Single slot, single drop point, n=4 complete comparisons",
        "interpretation_rule": r["interpretation"],
    })
for _, r in M.iterrows():
    dict_rows.append({
        "metric_name": r["metric_name"], "metric_id": r["metric_id"], "kind": "MARKETING METRIC",
        "business_question": r["interpretation"], "formula": r["formula"],
        "numerator": r["numerator"], "denominator": r["denominator"],
        "data_source": r["data_source"], "population": r["data_source"],
        "sample_size": r["denominator"], "evidence_type": r["evidence_type"],
        "limitations": r["caveat"], "interpretation_rule": r["interpretation"],
    })
pd.DataFrame(dict_rows).to_csv(f"{D}/metric_dictionary.csv", index=False)

print("review_theme_summary.csv")
print(T.pivot_table(index="theme_family", columns="base", values="share_of_coded_items_pct")
      .round(1).to_string())
print("\nevidence_matrix.csv rows:", len(EM))
print("metric_dictionary.csv rows:", len(dict_rows))
print(f"interview_theme_summary.csv -> CONDUCTED ({len(IV)} coded findings, "
      f"1 documented transcript, total interview count UNKNOWN)")
