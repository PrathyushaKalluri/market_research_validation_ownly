"""
00_consolidate_survey.py  —  AUTHORITATIVE survey cleaner (live Google Sheet)

Replaces the earlier positional mapping, which broke when the live sheet's column
ORDER changed. Columns are now matched by QUESTION TEXT + BRANCH, so the pipeline
survives further edits to the form.

Structure of the export: 44 canonical questions x 3 city branches = 99 raw columns.
Google Forms suffixes repeats as ' 2' / ' 3'; pandas suffixes as '.1' / '.2'.
Branch order within each question group is: Hyderabad, Bengaluru, Another city
(verified against the city column: n = [78, 20, 26]).

RAW is never modified. Every correction is flagged, never silently applied.
"""
import hashlib
import os
import re
import collections

import numpy as np
import pandas as pd

ROOT = "/Users/klprathyusha/Sem 3/Project/Ownly"
SRC = "/tmp/ownly_live/live.xlsx"
OUT = f"{ROOT}/final_dashboard/data"
os.makedirs(OUT, exist_ok=True)

raw = pd.read_excel(SRC)
CITY_COL = raw.columns[1]
BRANCH_ORDER = ["Hyderabad", "Bengaluru", "Another city"]


def canon(c):
    c = str(c).strip()
    c = re.sub(r"\.\d+$", "", c)
    c = re.sub(r"\s+\d+$", "", c)
    return c.strip()


groups = collections.OrderedDict()
for col in raw.columns:
    groups.setdefault(canon(col), []).append(col)


def pick(question_fragment, branch):
    """Return the column for `question_fragment` belonging to `branch`.
    Branch variants are assigned by which city's rows actually populate them."""
    frag = question_fragment.lower()
    hits = [(b, cols) for b, cols in groups.items() if frag in b.lower()]
    if not hits:
        return None
    _, cols = max(hits, key=lambda kv: len(kv[1]))
    best, best_n = None, -1
    for c in cols:
        n = int((raw[c].notna() & raw[CITY_COL].eq(branch)).sum())
        if n > best_n:
            best, best_n = c, n
    return best if best_n > 0 else None


QUESTIONS = {
    "area": "which area?",
    "city_other": "which city?",
    "age_band": "how old are you?",
    "occupation": "which best describes you right now?",
    "memberships": "which food delivery memberships",
    "rapido_freq": "how often did you use rapido",
    "ordered_4wk": "did you order food online for delivery at least once",
    "n_swiggy": "swiggy: how many orders",
    "n_zomato": "zomato: how many orders",
    "n_ownly": "ownly (rapido's food app, or food inside the rapido app): how many orders",
    "n_other": "any other way (toing, magicpin",
    "last_app": "which app did you use for your most recent",
    "last_amount": "what was the total amount you paid for it",
    "last_people": "how many people was that order for",
    "bill_fairness": "did it feel fair for what you got",
    "tradeoff_eta": "same restaurant, same food. which would you choose",
    "tradeoff_rel": "same restaurant, same food, same delivery time",
    "tradeoff_rest": "same food price level and delivery time",
    "switch_savings": "how much lower would the final amount need to be",
    "prop_P_intent": "if service p were available",
    "prop_Q_intent": "and if service q were available",
    "prop_forced": "if only one of them existed where you live",
    "prop_reason": "in one line, what made you pick that one",
    "repeat_no_promo": "once that offer ended, would you keep using it",
    "durability_doubt": "a new app's low prices usually go up",
    "rapido_food_seen": "have you seen an option to order food inside the rapido app",
    "ownly_status": "before today, which of these is true for you",
    "ownly_trigger": "which one thing would most make you try ownly",
    "ownly_heard_where": "where did you first hear about ownly",
    "not_opened_reason": "what's the main reason you haven't opened it",
    "stopped_ordering": "when you looked, what mainly stopped you from ordering",
    "first_order_when": "when did you place your first ownly order",
    "prev_4wk_orders": "how many ownly orders did you place in the 4 weeks before",
    "counterfactual": "if ownly didn't exist, what would you most likely have done",
    "ownly_loss_feel": "how would you feel if you could no longer use ownly",
    "ownly_less_reason": "if you order on ownly less than you used to",
    "ownly_change": "what one change would make you order more on ownly",
}

rows = []
for i in range(len(raw)):
    city = raw[CITY_COL].iloc[i]
    if city not in BRANCH_ORDER:
        continue
    rec = {"resp_id": f"R{i+2:03d}", "timestamp": raw["Timestamp"].iloc[i], "city": city}
    for var, frag in QUESTIONS.items():
        col = pick(frag, city)
        rec[var] = raw[col].iloc[i] if col is not None else np.nan
    rows.append(rec)

df = pd.DataFrame(rows)

# ------------------------------------------------------------------ recoding
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

for c in ["eta", "rel", "rest"]:
    df[f"{c}_chose_cheap"] = df[f"tradeoff_{c}"].astype(str).str.startswith("₹230").where(
        df[f"tradeoff_{c}"].notna())

for c in ["n_swiggy", "n_zomato", "n_ownly", "n_other", "last_amount", "last_people",
          "prev_4wk_orders"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")

# ------------------------------------------------- age scope (see DQ1 / DQ15)
# The instrument routes out 'Under 20' and 'Over 35'. It therefore collected 20-35,
# even though the stated target scope is 18-35. Three respondents sit in a later
# '18-24' band whose exact age is unknown.
ROUTED_OUT = {"Under 20", "Over 35"}
df["age_routed_out"] = df["age_band"].isin(ROUTED_OUT)
df["age_eligible"] = df["age_band"].notna() & ~df["age_routed_out"]
df["age_band_ambiguous"] = df["age_band"].eq("18–24")

CATCH = {"Gachibowli", "Financial District / Nanakramguda", "Manikonda",
         "Narsingi / Kokapet", "Serilingampally / Nallagandla / Tellapur"}
df["in_catchment"] = df["area"].isin(CATCH)
df["is_gachibowli_proper"] = df["area"].eq("Gachibowli")

m = df["memberships"].fillna("")
df["has_membership"] = m.str.contains("Swiggy One|Zomato Gold|Another food delivery membership",
                                      regex=True)
df["n_memberships"] = m.apply(lambda s: 0 if not s else len([x for x in s.split(";") if x.strip()]))

ST = {"I hadn't heard of Ownly": 0, "I'd heard of it, but never opened it": 1,
      "I opened or browsed it, but didn't order": 2, "I've ordered on Ownly": 3}
df["ownly_stage"] = df["ownly_status"].map(ST)
df["ownly_aware"] = df["ownly_stage"] >= 1
df["ownly_opened"] = df["ownly_stage"] >= 2
df["ownly_says_ordered"] = df["ownly_stage"] >= 3

plat = df[["n_swiggy", "n_zomato", "n_ownly", "n_other"]]
df["n_platforms_used"] = (plat > 0).sum(axis=1).where(plat.notna().any(axis=1))
df["multihoming"] = df["n_platforms_used"] >= 2
df["total_orders_4wk"] = plat.sum(axis=1, min_count=1)
df["recent_orderer"] = df["ordered_4wk"].eq("Yes")

# =====================================================================
# DQ16 — the Ownly recent-order contradiction. NOT silently corrected.
# =====================================================================
says_ordered = df["ownly_says_ordered"].fillna(False)
first_recent = df["first_order_when"].eq("In the last 4 weeks")
zero_recent = df["n_ownly"].eq(0)

df["ownly_order_conflict"] = says_ordered & first_recent & zero_recent
df["ownly_lapsed_consistent"] = (says_ordered & ~first_recent & zero_recent
                                 & df["prev_4wk_orders"].fillna(0).gt(0))

# usable recent-order count: blanked where the respondent contradicts themselves
df["n_ownly_usable"] = df["n_ownly"].where(~df["ownly_order_conflict"])
df["ownly_recent_status"] = np.select(
    [df["ownly_order_conflict"],
     says_ordered & df["n_ownly"].gt(0),
     df["ownly_lapsed_consistent"],
     says_ordered & zero_recent,
     ~says_ordered & df["recent_orderer"]],
    ["CONFLICTING - recent count unavailable",
     "Ordered on Ownly in last 4 weeks",
     "Lapsed - ordered earlier, none in last 4 weeks",
     "Says ordered, reports 0 recent (unexplained)",
     "Never ordered on Ownly"],
    default="Not asked / not applicable")

# other data-quality flags
df["amount_flag"] = np.where(df["last_amount"].eq(0), "amount_zero_implausible_voided", "")
df.loc[df["last_amount"].eq(0), "last_amount"] = np.nan
df["amount_pp"] = df["last_amount"] / df["last_people"].replace(0, np.nan)

# ------------------------------------------------------------------ populations
df["exclusion_reason"] = np.where(
    df["age_band"].isna(), "Abandoned before the age item",
    np.where(df["age_routed_out"],
             "SCREENED OUT by instrument: age band 'Under 20' or 'Over 35'", ""))

cleaned = df[df["exclusion_reason"] == ""].copy()
excluded = df[df["exclusion_reason"] != ""].copy()

cleaned["pop_HYD_ELIGIBLE"] = cleaned["city"].eq("Hyderabad")
cleaned["pop_HYD_CATCHMENT"] = cleaned["pop_HYD_ELIGIBLE"] & cleaned["in_catchment"]
cleaned["pop_HYD_GACHIBOWLI"] = cleaned["pop_HYD_ELIGIBLE"] & cleaned["is_gachibowli_proper"]
cleaned["pop_HYD_RECENT_ORDERER"] = cleaned["pop_HYD_ELIGIBLE"] & cleaned["recent_orderer"]
cleaned["pop_BLR_ELIGIBLE"] = cleaned["city"].eq("Bengaluru")
cleaned["pop_OTHER"] = cleaned["city"].eq("Another city")

with open(SRC, "rb") as fh:
    sha = hashlib.sha256(fh.read()).hexdigest()
pd.DataFrame([{
    "source": "Google Sheet (live) — Form Responses 1",
    "sheet_id": "1YWjzxcGNsEWhM_OT1PHFhGa9Eb2b0EegY63qz5q-7G8",
    "downloaded": pd.Timestamp.now().isoformat(timespec="seconds"),
    "sha256_of_xlsx": sha, "raw_rows": len(raw), "raw_cols": raw.shape[1],
    "canonical_questions": len(groups),
    "first_response": str(raw["Timestamp"].min()), "last_response": str(raw["Timestamp"].max()),
    "supersedes": "Ownly Survey.csv.zip (113 rows) — column ORDER differs, do not reuse",
}]).to_csv(f"{OUT}/raw_manifest.csv", index=False)

df.to_csv(f"{OUT}/survey_all_rows_with_flags.csv", index=False)
cleaned.to_csv(f"{OUT}/cleaned_survey.csv", index=False)
excluded.to_csv(f"{OUT}/excluded_survey.csv", index=False)

# ------------------------------------------------------------------ funnel
H = cleaned[cleaned["pop_HYD_ELIGIBLE"]]
funnel = [
    ("All responses received", len(raw)),
    ("Hyderabad branch", int((raw[CITY_COL] == "Hyderabad").sum())),
    ("Passed the age screen (20–35 as collected)", len(H)),
    ("In the Gachibowli catchment", int(H["in_catchment"].sum())),
    ("Gachibowli proper", int(H["is_gachibowli_proper"].sum())),
    ("Ordered food online in the last 4 weeks", int(H["recent_orderer"].sum())),
]
pd.DataFrame(funnel, columns=["stage", "n"]).to_csv(f"{OUT}/research_funnel.csv", index=False)

print("RAW rows:", len(raw), "| canonical questions:", len(groups))
print("CLEANED:", len(cleaned), "| EXCLUDED:", len(excluded))
print(excluded["exclusion_reason"].value_counts().to_string())
print("\nRESEARCH SAMPLE FUNNEL (not a market funnel)")
for s, n in funnel:
    print(f"  {n:>4}   {s}")
print("\nAge bands, Hyderabad eligible:")
print(H["age_band"].value_counts().to_string())
print("\nOwnly recent-order status (all cities, those asked):")
print(df[df["ownly_says_ordered"].fillna(False)]["ownly_recent_status"].value_counts().to_string())
print("\nSwitching threshold, Hyderabad eligible:")
t = H["switch_savings_rs"].dropna()
print(t.value_counts().sort_index().to_string())
print(f"  median ₹{t.median():.0f} | mode ₹{t.mode().tolist()} | n={len(t)} "
      f"(+{int(H['switch_never'].sum())} 'no amount', +{int(H['switch_dk'].sum())} 'don't know')")
print("\n₹30 trade-offs, Hyderabad eligible:")
for c, lab in [("eta_chose_cheap", "speed"), ("rel_chose_cheap", "reliability"),
               ("rest_chose_cheap", "usual restaurants")]:
    s = H[c].dropna().astype(bool)
    print(f"  {lab:18s} chose cheaper {int(s.sum())}/{len(s)} = {s.mean()*100:.1f}%"
          f"  | paid premium {100-s.mean()*100:.1f}%")
