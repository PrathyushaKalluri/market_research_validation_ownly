"""
01_clean_survey.py — Ownly Gachibowli study
Harmonise the 3-branch Google Form export into a tidy respondent-level frame.

RAW is never modified. Outputs RAW manifest, CLEANED and EXCLUDED with exclusion_reason.
No imputation. No fabrication. Missing stays missing.
"""
import hashlib, os
import numpy as np
import pandas as pd

ROOT = "/Users/klprathyusha/Sem 3/Project/Ownly"
RAW = "/tmp/ownly_extract/Ownly Survey.csv"
OUT = f"{ROOT}/final_dashboard/data"
os.makedirs(OUT, exist_ok=True)

raw = pd.read_csv(RAW)
C = list(raw.columns)

# ---------------------------------------------------------------- raw manifest
with open(RAW, "rb") as fh:
    sha = hashlib.sha256(fh.read()).hexdigest()
pd.DataFrame([{
    "file": "Ownly Survey.csv", "source_zip": "Ownly Survey.csv.zip",
    "sha256": sha, "rows": len(raw), "cols": raw.shape[1],
    "collected_through": str(raw["Timestamp"].max()),
    "evidence_type": "SURVEY — PRIMARY (self-reported)",
    "note": "Google Forms export, 3 branched paths (Hyderabad / Bengaluru / Other city)",
}]).to_csv(f"{OUT}/raw_manifest.csv", index=False)

# --------------------------------------------- branch → harmonised column map
# (hyderabad_idx, bengaluru_idx, othercity_idx); None = not asked on that branch
MAP = {
    "area":             (2, 41, 79),
    "age_band":         (3, 42, 80),
    "occupation":       (4, 43, 81),
    "memberships":      (5, 44, 82),
    "rapido_freq":      (6, 45, None),
    "ordered_4wk":      (8, 46, 83),
    "n_swiggy":         (9, 47, 84),
    "n_zomato":         (10, 48, 85),
    "n_ownly":          (11, 49, 86),
    "n_other":          (12, 50, 87),
    "last_app":         (13, 51, 88),
    "last_amount":      (14, 52, 89),
    "last_people":      (15, 53, 90),
    "bill_fairness":    (16, 54, 91),
    "tradeoff_eta":     (17, 55, None),
    "tradeoff_rel":     (18, 56, None),
    "tradeoff_rest":    (19, 57, None),
    "switch_savings":   (20, 58, None),
    "prop_P_intent":    (21, 59, None),
    "prop_Q_intent":    (22, 60, None),
    "prop_forced":      (23, 61, None),
    "prop_reason":      (24, 62, None),
    "repeat_no_promo":  (25, 63, None),
    "durability_doubt": (26, 64, None),
    "rapido_food_seen": (27, 65, 92),
    "ownly_status":     (28, 66, 93),
    "ownly_trigger":    (29, 67, 94),
}

city_col = raw[C[1]]
BRANCH = {"Hyderabad": 0, "Bengaluru": 1, "Another city": 2}

rows = []
for i in range(len(raw)):
    city = city_col.iloc[i]
    b = BRANCH.get(city)
    if b is None:
        continue
    rec = {"resp_id": f"R{i+1:03d}", "timestamp": raw["Timestamp"].iloc[i], "city": city}
    for var, idxs in MAP.items():
        ci = idxs[b]
        rec[var] = raw[C[ci]].iloc[i] if ci is not None else np.nan
    # col 7 is a duplicate Rapido-frequency item on the Hyderabad branch
    if b == 0 and pd.isna(rec["rapido_freq"]):
        rec["rapido_freq"] = raw[C[7]].iloc[i]
    rows.append(rec)

df = pd.DataFrame(rows)

# ----------------------------------------------------------------- recoding
INTENT5 = {"Definitely not": 1, "Probably not": 2, "Not sure": 3, "Probably": 4, "Definitely": 5}
AGREE5 = {"Strongly disagree": 1, "Disagree": 2, "Neither": 3, "Agree": 4, "Strongly agree": 5}
SAVINGS = {"₹10": 10, "₹20": 20, "₹30": 30, "₹50": 50, "₹75": 75, "₹100 or more": 100}

df["prop_P_intent_n"] = df["prop_P_intent"].map(INTENT5)
df["prop_Q_intent_n"] = df["prop_Q_intent"].map(INTENT5)
df["repeat_no_promo_n"] = df["repeat_no_promo"].map(INTENT5)
df["durability_doubt_n"] = df["durability_doubt"].map(AGREE5)
df["switch_savings_rs"] = df["switch_savings"].map(SAVINGS)
df["switch_never"] = df["switch_savings"].eq("No amount, price alone wouldn't make me switch")
df["switch_dk"] = df["switch_savings"].eq("Don't know")

# trade-offs: 1 = took the CHEAPER (₹230) option, 0 = paid the ₹30 premium (₹260)
df["eta_chose_cheap"] = df["tradeoff_eta"].str.startswith("₹230").astype("boolean")
df["rel_chose_cheap"] = df["tradeoff_rel"].str.startswith("₹230").astype("boolean")
df["rest_chose_cheap"] = df["tradeoff_rest"].str.startswith("₹230").astype("boolean")

# age eligibility — see the data-quality note on the 20–30 vs 20–35 scope conflict
ELIGIBLE_BANDS = {"20–24", "25–29", "30–35", "18–24"}
df["age_eligible"] = df["age_band"].isin(ELIGIBLE_BANDS)
df["age_strict_20_30"] = df["age_band"].isin({"20–24", "25–29"})
df["age_band_ambiguous"] = df["age_band"].eq("18–24")

# Gachibowli catchment (per project scope)
CATCH = {"Gachibowli", "Financial District / Nanakramguda", "Manikonda",
         "Narsingi / Kokapet", "Serilingampally / Nallagandla / Tellapur"}
df["in_catchment"] = df["area"].isin(CATCH)

# memberships
m = df["memberships"].fillna("")
df["has_membership"] = m.str.contains("Swiggy One|Zomato Gold|Another food delivery membership", regex=True)
df["n_memberships"] = m.apply(lambda s: 0 if not s else len([x for x in s.split(";") if x.strip()]))

# Ownly funnel status
ST = {"I hadn't heard of Ownly": 0, "I'd heard of it, but never opened it": 1,
      "I opened or browsed it, but didn't order": 2, "I've ordered on Ownly": 3}
df["ownly_stage"] = df["ownly_status"].map(ST)
df["ownly_aware"] = df["ownly_stage"] >= 1
df["ownly_opened"] = df["ownly_stage"] >= 2
df["ownly_ordered"] = df["ownly_stage"] >= 3

# multi-homing
for c in ["n_swiggy", "n_zomato", "n_ownly", "n_other"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")
plat = df[["n_swiggy", "n_zomato", "n_ownly", "n_other"]]
df["n_platforms_used"] = (plat > 0).sum(axis=1).where(plat.notna().any(axis=1))
df["multihoming"] = df["n_platforms_used"] >= 2
df["total_orders_4wk"] = plat.sum(axis=1, min_count=1)

df["last_amount"] = pd.to_numeric(df["last_amount"], errors="coerce")
df["last_people"] = pd.to_numeric(df["last_people"], errors="coerce")
df["amount_pp"] = df["last_amount"] / df["last_people"].replace(0, np.nan)

# ------------------------------------------------------- exclusions (logged)
df["exclusion_reason"] = ""
df.loc[~df["age_eligible"] & df["age_band"].notna(), "exclusion_reason"] = \
    "SCREENED OUT by instrument: age outside 20–35 (form routed to end)"
df.loc[df["age_band"].isna(), "exclusion_reason"] = "Did not pass city/area screen or abandoned before age item"
# a ₹0 'amount paid' is not a usable bill value; flag the field, keep the respondent
df.loc[df["last_amount"].eq(0), "amount_flag"] = "amount_zero_implausible_field_excluded"
df.loc[df["last_amount"].eq(0), "last_amount"] = np.nan
df.loc[df["last_amount"].isna(), "amount_pp"] = np.nan

cleaned = df[df["exclusion_reason"] == ""].copy()
excluded = df[df["exclusion_reason"] != ""].copy()

# analysis populations
cleaned["pop_HYD_ELIGIBLE"] = cleaned["city"].eq("Hyderabad")
cleaned["pop_HYD_CATCHMENT"] = cleaned["pop_HYD_ELIGIBLE"] & cleaned["in_catchment"]
cleaned["pop_BLR_ELIGIBLE"] = cleaned["city"].eq("Bengaluru")
cleaned["pop_OTHER"] = cleaned["city"].eq("Another city")
cleaned["pop_HYD_STRICT_20_30"] = cleaned["pop_HYD_ELIGIBLE"] & cleaned["age_strict_20_30"]

df.to_csv(f"{OUT}/survey_all_rows_with_flags.csv", index=False)
cleaned.to_csv(f"{OUT}/cleaned_survey.csv", index=False)
excluded.to_csv(f"{OUT}/excluded_survey.csv", index=False)

print(f"RAW rows          : {len(raw)}")
print(f"CLEANED           : {len(cleaned)}")
print(f"EXCLUDED          : {len(excluded)}")
print(excluded["exclusion_reason"].value_counts().to_string())
print("\nPopulations:")
for p in ["pop_HYD_ELIGIBLE", "pop_HYD_CATCHMENT", "pop_HYD_STRICT_20_30",
          "pop_BLR_ELIGIBLE", "pop_OTHER"]:
    print(f"  {p:24s} n = {int(cleaned[p].sum())}")
print("\nAge bands (cleaned, Hyderabad):")
print(cleaned[cleaned.pop_HYD_ELIGIBLE]["age_band"].value_counts().to_string())
