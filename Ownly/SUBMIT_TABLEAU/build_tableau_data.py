#!/usr/bin/env python3
"""
Ownly Gachibowli — Tableau extract builder.

Reads the analysis output produced by ../SUBMIT_BI/build_data.py and reshapes it
into tidy, Tableau-friendly CSVs in ./Data/.

Design rules applied throughout:
  * LONG format wherever a chart needs a colour/shape dimension
    (Tableau wants one row per mark, not one column per series).
  * Every modelled value Python computed — fitted curve, sentiment scores,
    p-values, confidence intervals, lift — is materialised as a COLUMN so that
    Tableau can draw it natively without TabPy.
  * Sort orders are pre-baked as integer columns so Tableau does not sort
    alphabetically.
  * No pivots, no merged cells, no blank header rows.

Run:  python3 build_tableau_data.py
"""

import csv, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "Data")
BIJS = os.path.join(ROOT, "SUBMIT_BI", "bi_data.js")

if not os.path.exists(BIJS):
    sys.exit("Missing ../SUBMIT_BI/bi_data.js — run SUBMIT_BI/build_data.py first.")

raw = open(BIJS, encoding="utf-8").read()
B = json.loads(raw[raw.index("=") + 1: raw.rstrip().rstrip(";").rindex("}") + 1])

os.makedirs(OUT, exist_ok=True)
written = []

def w(name, header, rows):
    p = os.path.join(OUT, name)
    with open(p, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(header)
        wr.writerows(rows)
    written.append((name, len(rows), len(header)))

def yn(v): return "Yes" if v else "No"
def f1(v):
    """Tolerant numeric coercion — blanks, None and non-numeric strings become ''."""
    if v is None: return ""
    if isinstance(v, (int, float)): return round(float(v), 4)
    t = str(v).strip().replace("\u20b9", "").replace(",", "").replace("%", "")
    if t == "" or t.lower() in ("nan", "none", "-", "—"): return ""
    try: return round(float(t), 4)
    except ValueError: return ""

# ─────────────────────────────────────────────────────────────
# 1 · KPI SUMMARY
# ─────────────────────────────────────────────────────────────
rows = []
for k in B["kpis"]:
    rows.append([
        k.get("kpi_id"), k.get("kpi_name"), k.get("layer"), k.get("driver"),
        k.get("family"), k.get("status"),
        f1(k.get("value")) if k.get("value") not in ("", None) else "",
        k.get("unit"), f1(k.get("ci_lo")), f1(k.get("ci_hi")),
        k.get("numerator"), k.get("denominator"), k.get("base"),
        "Yes" if str(k.get("is_headline")).lower() == "true" else "No",
        k.get("evidence_type"), k.get("evidence_strength"),
        "Yes" if "NOT COMPUTABLE" in str(k.get("status")).upper() or "UNAVAILABLE" in str(k.get("status")).upper() else "No",
        k.get("limitation"),
    ])
w("01_kpi_summary.csv",
  ["KPI ID","KPI Name","Layer","Driver","Family","Status","Value","Unit","CI Low","CI High",
   "Numerator","Denominator","Base","Is Headline","Evidence Type","Evidence Strength",
   "Not Computable","Limitation"], rows)

# ─────────────────────────────────────────────────────────────
# 2 · MARKETING METRICS  (+ 3 · not estimable)
# ─────────────────────────────────────────────────────────────
w("02_marketing_metrics.csv",
  ["Metric ID","Metric Name","Value","Unit","Basis","Our Own Definition","Formula","Interpretation","Caveat"],
  [[m["metric_id"], m["metric_name"], f1(m.get("value")), m.get("unit"),
    m.get("formula_sheet_reference"),
    yn(m.get("formula_sheet_reference","").startswith(("custom","derived"))),
    m.get("formula"), m.get("interpretation"), m.get("caveat")]
   for m in B["marketing_metrics"]])

w("03_not_estimable.csv",
  ["Metric","Formula Sheet","Why Not Computable","Status","Where It Would Come From"],
  [[n["metric"], n["formula_sheet"], n["why_not_computable"], n["status"], n["where_it_would_come_from"]]
   for n in B["not_estimable"]])

# ─────────────────────────────────────────────────────────────
# 4 · TRADE-OFFS  (+ 5 · paired tests)
# ─────────────────────────────────────────────────────────────
order = {"speed": 1, "reliability": 2, "usual restaurants": 3}
w("04_tradeoffs.csv",
  ["Dimension","Sort Order","Description","Accepted K","Base N","Accept Pct","CI Low","CI High","Paid Premium Pct","Is Constraint"],
  [[t["dim"], order.get(t["dim"], 9), t["label"], t["k"], t["n"], f1(t["pct"]),
    f1(t["lo"]), f1(t["hi"]), f1(t["premium"]), yn(t["pct"] < 50)]
   for t in B["tradeoffs"]])

w("05_tradeoff_tests.csv",
  ["Comparison","Test","Base N","Discordant A Only","Discordant B Only","P Value","Significant at 0.05","Neg Log10 P"],
  [[t["cmp"], t["test"], t["n"], t["b"], t["c"], t["p"],
    yn(t["p"] < 0.05), round(-__import__("math").log10(max(t["p"], 1e-12)), 2)]
   for t in B["tradeoff_tests"]])

# ─────────────────────────────────────────────────────────────
# 6 · RESPONDENT LEVEL  (the cross-filter spine)
# ─────────────────────────────────────────────────────────────
rows = []
for r in B["rows"]:
    rows.append([
        r["id"], r["occ"], yn(r["member"]), r["n_mem"], yn(r["multi"]), yn(r["rapido"]),
        r["rapido_seen"], yn(r["aware"]), yn(r["opened"]), yn(r["ordered"]),
        yn(r["eta_cheap"]), yn(r["rel_cheap"]), yn(r["rest_cheap"]),
        f1(r["switch_rs"]), yn(r["switch_never"]), yn(r["switch_dk"]),
        f1(r["orders_4wk"]), f1(r["n_swiggy"]), f1(r["n_zomato"]), f1(r["n_ownly"]), f1(r["n_other"]),
        f1(r["last_amount"]), f1(r["amount_pp"]), f1(r["repeat_n"]), f1(r["doubt_n"]),
        f1(r["P_int"]), f1(r["Q_int"]), r["bill_fair"], yn(r["gachi"]),
    ])
w("06_survey_respondents.csv",
  ["Respondent ID","Occupation Segment","Holds Membership","Memberships Held","Multi Homing","Uses Rapido",
   "Rapido Food Seen","Aware Of Ownly","Opened Ownly","Ordered On Ownly",
   "Trades Speed","Trades Reliability","Trades Restaurants",
   "Saving Required Rs","No Amount Would Switch","Does Not Know",
   "Orders 4wk","Swiggy Orders","Zomato Orders","Ownly Orders","Other Orders",
   "Last Bill Rs","Amount Per Person","Repeat Intent Score","Durability Doubt Score",
   "Proposition P Intent","Proposition Q Intent","Bill Fairness","Gachibowli Proper"], rows)

# Long version of the four platform order counts, for share-of-wallet charts
rows = []
for r in B["rows"]:
    for plat, key in [("Swiggy","n_swiggy"),("Zomato","n_zomato"),("Ownly","n_ownly"),("Other","n_other")]:
        rows.append([r["id"], r["occ"], yn(r["member"]), plat, f1(r[key]) or 0])
w("06b_orders_by_platform_long.csv",
  ["Respondent ID","Occupation Segment","Holds Membership","Platform","Orders 4wk"], rows)

# ─────────────────────────────────────────────────────────────
# 7 · PRICE AUDIT
# ─────────────────────────────────────────────────────────────
vorder = {"LIST+FEES": 1, "MEMBER": 2, "AFTER OFFER": 3}
w("07_price_audit_pairs.csv",
  ["Restaurant","Price View","View Order","Ownly Payable","Cheapest Rival Payable","Cheapest Rival",
   "Saving Rs","Saving Pct","Ownly Wins","Ownly ETA Min","Rival ETA Min","ETA Gap Min"],
  [[p["restaurant"], p["view"], vorder.get(p["view"], 9), f1(p["ownly"]), f1(p["rival"]),
    p["rival_name"], f1(p["saving"]), f1(p["saving_pct"]), yn(p["wins"]),
    f1(p["ownly_eta"]), f1(p["rival_eta"]),
    f1((p["ownly_eta"] or 0) - (p["rival_eta"] or 0))]
   for p in B["pairs"]])

# LONG: one row per restaurant × platform × view — for grouped bars
rows = []
for p in B["pairs"]:
    rows.append([p["restaurant"], p["view"], vorder.get(p["view"],9), "Ownly", f1(p["ownly"]), f1(p["ownly_eta"])])
    rows.append([p["restaurant"], p["view"], vorder.get(p["view"],9), p["rival_name"].title(), f1(p["rival"]), f1(p["rival_eta"])])
w("07b_price_by_platform_long.csv",
  ["Restaurant","Price View","View Order","Platform","Final Payable Rs","Quoted ETA Min"], rows)

# 8 · bill composition — LONG, drives the 100% stacked bar
rows = []
for f in B["fee_decomp"]:
    for part in f["parts"]:
        if part["pct"] > 0:
            rows.append([f["platform"].title(), part["part"],
                         "Food" if part["part"] == "Food" else "Fees & tax", f1(part["pct"])])
w("08_bill_composition_long.csv",
  ["Platform","Component","Component Group","Pct Of Bill"], rows)

# 9 · erosion
w("09_price_erosion.csv",
  ["Price View","View Order","Pairs Clearing","Pairs Total","Coverage Pct","Median Saving Rs","Ownly Is Dearer"],
  [[e["view"], vorder.get(e["view"],9), e["clearing"], e["total"], f1(e["pct"]),
    f1(e["median_saving"]), yn((e["median_saving"] or 0) < 0)]
   for e in B["erosion"]])

# ─────────────────────────────────────────────────────────────
# 10 · FUNNELS
# ─────────────────────────────────────────────────────────────
rows = []
for i, s in enumerate(B["funnel_research"]):
    rows.append(["Research sample", s["stage"], i + 1, s["n"],
                 f1(100 * s["n"] / B["funnel_research"][0]["n"]), "", ""])
for i, s in enumerate(B["adoption_funnel"]):
    rows.append(["Ownly adoption", s["stage"], i + 1, s["k"], f1(s["pct"]), f1(s["lo"]), f1(s["hi"])])
w("10_funnels.csv", ["Funnel","Stage","Stage Order","N","Pct","CI Low","CI High"], rows)

# ─────────────────────────────────────────────────────────────
# 11 · DEMAND CURVE  — Python-fitted, drawn natively by Tableau
# ─────────────────────────────────────────────────────────────
dc = B["demand_curve"]
maxobs = dc.get("max_observed_x") or 100
rows = []
for p in dc["observed"]:
    rows.append([f1(p["x"]), "Observed", f1(p["y"]), "In range"])
for p in dc["curve"]:
    rows.append([f1(p["x"]), "Fitted logistic", f1(p["y"]),
                 "In range" if p["x"] <= maxobs else "Extrapolated"])
for m in dc["markers"]:
    rows.append([f1(m["x"]), "Observed saving at checkout: " + m["label"], f1(m["y"]),
                 "In range" if m["x"] <= maxobs else "Extrapolated"])
w("11_demand_curve.csv", ["Saving Rs","Series","Pct Would Switch","Range Status"], rows)

w("11b_demand_curve_fit.csv",
  ["Parameter","Value","Note"],
  [["b0 (intercept)", dc["fit"]["b0"], "logit(p) = b0 + b1 * saving"],
   ["b1 (slope)", dc["fit"]["b1"], "per rupee of recurring saving"],
   ["R squared", dc["fit"]["r2"], "fit against 6 observed staircase points"],
   ["SSE", dc["fit"]["sse"], "sum of squared error"],
   ["Base n", dc["n_named"], "respondents who named a rupee figure"],
   ["Excluded - no amount", dc["excluded_never"], "said no saving would move them"],
   ["Excluded - don't know", dc["excluded_dk"], "could not name a figure"],
   ["Max observed saving", maxobs, "anything above this is extrapolation"]])

# ─────────────────────────────────────────────────────────────
# 12-17 · TEXT ANALYTICS  (all Python-computed, Tableau-drawable)
# ─────────────────────────────────────────────────────────────
w("14_theme_families.csv",
  ["Theme Family","Documents","Mean Sentiment","Sentiment Direction"],
  [[t["family"], t["n"], f1(t["sentiment"]),
    "Negative" if t["sentiment"] < -0.08 else ("Positive" if t["sentiment"] > 0.05 else "Neutral")]
   for t in B["theme_families"]])

w("14b_themes_detail.csv",
  ["Theme Code","Theme Label","Theme Family","Documents","Mean Sentiment","Engagement Total","Engagement Docs"],
  [[t["raw"], t["theme"], t["family"], t["n"], f1(t["sentiment"]),
    t.get("eng"), t.get("eng_n")] for t in B["themes"]])

w("15_text_trend_monthly.csv",
  ["Month","Documents","Mean Sentiment","Positive","Neutral","Negative","Engagement"],
  [[t["month"], t["n"], f1(t["mean"]), t["pos"], t["neu"], t["neg"], f1(t["eng"])]
   for t in B["text_trend"]])

# long version for a 100% stacked sentiment-over-time chart
rows = []
for t in B["text_trend"]:
    for lab, key in [("Negative","neg"),("Neutral","neu"),("Positive","pos")]:
        rows.append([t["month"], lab, t[key], f1(100 * t[key] / t["n"]) if t["n"] else 0])
w("15b_text_trend_long.csv", ["Month","Sentiment Label","Documents","Pct Of Month"], rows)

w("16_sentiment_by_source.csv",
  ["Source","Documents","Positive","Neutral","Negative","Mean Sentiment"],
  [[s["src"], s["n"], s["positive"], s["neutral"], s["negative"], f1(s["mean"])]
   for s in B["sentiment_by_source"]])

rows = []
for s in B["sentiment_by_source"]:
    for lab, key in [("Negative","negative"),("Neutral","neutral"),("Positive","positive")]:
        rows.append([s["src"], lab, s[key], f1(100 * s[key] / s["n"])])
w("16b_sentiment_by_source_long.csv", ["Source","Sentiment Label","Documents","Pct Of Source"], rows)

sv = B["sentiment_vs_star"]
w("17_sentiment_validation.csv",
  ["Star Rating","Reviews","Mean Sentiment Score"],
  [[r["star"], r["n"], f1(r["mean"])] for r in sv["by_star"]])
w("17b_sentiment_validation_stat.csv",
  ["Statistic","Value","Note"],
  [["Spearman rho", sv["spearman"]["rho"], "lexicon score vs star rating"],
   ["n", sv["spearman"]["n"], "app-store reviews carrying a star rating"],
   ["p value", sv["spearman"]["p"], "two-sided"],
   ["Interpretation", "Validated", "lexicon written blind to the star ratings"]])

w("18_tfidf_terms.csv",
  ["Scope","Theme","Term","TFIDF Score","Document Frequency","Rank"],
  [["Overall","All documents", t["term"], f1(t["score"]), t["df"], i + 1]
   for i, t in enumerate(B["terms_overall"])] +
  [["By theme", th["theme"], t["term"], f1(t["score"]), t["df"], i + 1]
   for th in B["terms_by_theme"] for i, t in enumerate(th["terms"])])

w("19_theme_cooccurrence.csv",
  ["Theme A","Theme B","Pair Label","Documents"],
  [[c["a"], c["b"], c["a"] + " + " + c["b"], c["n"]] for c in B["cooccur"]])

w("20_verbatims.csv",
  ["Source","Month","Engagement","Sentiment Score","Sentiment Label","Star Rating","Themes","Verbatim"],
  [[v["src"], v["date"], v["eng"], f1(v["score"]), v["label"], v["star"],
    "; ".join(v["themes"]), v["text"]] for v in B["verbatims"]])

w("21_review_stars.csv", ["Star Rating","Reviews","Is Low Rating"],
  [[s["star"], s["n"], yn(s["star"] <= 2)] for s in B["stars"]])

# ─────────────────────────────────────────────────────────────
# 22-25 · COMPETITIVE
# ─────────────────────────────────────────────────────────────
rows = []
for c in B["coverage"]:
    for plat in ("ownly", "swiggy", "zomato"):
        v = str(c.get(plat, "")).strip().lower()
        rows.append([c["restaurant_display"], plat.title(),
                     "Listed" if v in ("y","true","yes") else "Not listed",
                     1 if v in ("y","true","yes") else 0])
w("22_coverage_long.csv", ["Restaurant","Platform","Listing Status","Listed Flag"], rows)

rows = []
for e in B["eta_gap"]:
    for plat, key in [("Ownly","ownly"),("Swiggy","swiggy"),("Zomato","zomato")]:
        if e.get(key) is not None:
            rows.append([e["restaurant"], plat, f1(e[key]), f1(e["gap"])])
w("23_eta_by_platform_long.csv", ["Restaurant","Platform","Quoted ETA Min","Ownly Gap Min"], rows)

bl = B["blr_vs_hyd"]
metrics = [("Awareness","aware_pct"),("Trial","tried_pct"),("Membership","membership_pct"),
           ("Multi-homing","multihoming_pct"),("Median switch Rs","median_switch_rs"),
           ("Price doubt","durability_doubt_pct")]
rows = []
for b in bl:
    for label, key in metrics:
        rows.append([b["base"], int(float(b["n"])), label, f1(b[key])])
w("24_city_benchmark_long.csv", ["City Base","Base N","Metric","Value"], rows)

w("25_challenger_failure_modes.csv",
  ["Failure Mechanism","Ownly Status","Status Order","Our Evidence"],
  [["Rented demand — price funded by subsidy","Escaped",1,
    "Saving is structural: fee load 5.2% vs 23.4%. Does not require funding to persist."],
   ["No new use case — same catalogue","Exposed",3,
    "88.9% catalogue overlap. Same restaurants, +17 min slower."],
   ["Attacking a side that was not scarce","Exposed",3,
    "Restaurants already multi-home. Zero commission buys supply that was never constrained."],
   ["Thin unit economics","Exposed",3,
    "Rs 30 revenue against Rs 56.01 industry rider payout = -Rs 26.01 per order."],
   ["Distribution assumed to convert","At risk",2,
    "Uber Eats had the same amortised-fleet logic. Only 5 of 33 noticed food inside Rapido."]])

# ─────────────────────────────────────────────────────────────
# 26-29 · DIAGNOSTIC / PREDICTIVE
# ─────────────────────────────────────────────────────────────
w("26_correlations_long.csv", ["Variable A","Variable B","Spearman Rho","P Value","N","Significant"],
  [[c["a"], c["b"], f1(c["rho"]), f1(c["p"]), c["n"],
    yn(c["p"] is not None and c["p"] < 0.05 and c["a"] != c["b"])]
   for c in B["corr"]["cells"]])

w("26b_associations.csv", ["Question","N","Spearman Rho","P Value","CI Low","CI High","Verdict"],
  [[a["q"], a["n"], f1(a["rho"]), f1(a["p"]), f1(a["lo"]), f1(a["hi"]), a["verdict"]]
   for a in B["associations"]])

rows = []
for t in B["profiling"]["targets"]:
    for r in t["rows"]:
        rows.append([t["target"], f1(t["base_pct"]), r["feature"], r["k"], r["n"],
                     f1(r["pct"]), f1(r["lo"]), f1(r["hi"]), f1(r["lift"]),
                     "Above base" if (r["lift"] or 0) > 1.05 else ("Below base" if (r["lift"] or 0) < 0.95 else "At base")])
w("27_switcher_profiling.csv",
  ["Target","Base Pct","Feature","K","N","Pct","CI Low","CI High","Lift","Lift Direction"], rows)

w("27b_profiling_tests.csv", ["Target","Feature","In Yes","In No","Out Yes","Out No","Fisher P","Detectable"],
  [[t["target"], t["feature"], t["a"], t["b"], t["c"], t["d"], f1(t["p"]),
    yn(t["p"] is not None and t["p"] < 0.05)] for t in B["profiling"]["tests"]])

w("28_segment_cuts_long.csv", ["Segment","Base N","Metric","Value"],
  [[s["segment"], int(float(s["n"])), k, f1(float(str(s[k]).replace("₹","")))]
   for s in B["segment_cuts"]
   for k in s if k not in ("segment", "n") and str(s[k]).strip() != ""])

w("28b_segment_tradeoffs.csv", ["Dimension","Segment","K","N","Accept Pct","CI Low","CI High","Fisher P"],
  [[s["dim"], s["seg"], s["k"], s["n"], f1(s["pct"]), f1(s["lo"]), f1(s["hi"]), f1(s["p"])]
   for s in B["segment_tradeoffs"]])

# ─────────────────────────────────────────────────────────────
# 30-33 · ECONOMICS / PRESCRIPTIVE
# ─────────────────────────────────────────────────────────────
w("30_econ_benchmarks.csv",
  ["Metric","Value","Unit","Evidence Grade","Entity","Series","Source","Why Domain Wide"],
  [[e["metric"], f1(e["value"]), e["unit"], e["grade"], e["entity"], e["series"],
    e["source"], e["why_domain_wide"]] for e in B["econ_benchmarks"]])

rows = []
for g in B["breakeven_grid"]:
    for scen, key in [("Rider Rs 45","contrib_at_45"),("Rider Rs 56.01 (industry FACT)","contrib"),("Rider Rs 65","contrib_at_65")]:
        rows.append([g["rev"], scen, f1(g[key]), yn(g[key] >= 0)])
w("31_breakeven_grid_long.csv",
  ["Revenue Per Order Rs","Rider Cost Scenario","Contribution Per Order Rs","Is Profitable"], rows)

be = B["breakeven"]
w("31b_breakeven_summary.csv", ["Item","Value","Note"],
  [["Revenue per order (reported)", be["rev_per_order"], "MEDIA, contested across three outlets"],
   ["Rider payout per order", be["rider_cost"], "Swiggy FY24 disclosed, FACT"],
   ["Contribution per order", be["contrib_per_order"], "revenue minus rider payout"],
   ["Break-even revenue per order", be["breakeven_rev"], "revenue needed to reach zero"],
   ["Uplift needed pct", be["uplift_needed_pct"], "increase required on reported revenue"]])

w("32_lever_sensitivity.csv",
  ["Lever","Low Outcome","High Outcome","Swing","Range Low","Range High","Lever Type"],
  [[t["lever"], f1(t["low"]), f1(t["high"]), f1(t["swing"]), t["lo_val"], t["hi_val"],
    "Can change the sign" if ("Revenue" in t["lever"] or "Rider" in t["lever"]) else "Volume lever"]
   for t in B["tornado"]])

# ─────────────────────────────────────────────────────────────
# 34-36 · METHOD
# ─────────────────────────────────────────────────────────────
srcs = ["survey","interviews","price_audit","app_reviews","social","secondary_research","challenger_history"]
rows = []
for e in B["evidence_matrix"]:
    for s in srcs:
        v = str(e.get(s, "")).strip()
        if v and v != "—":
            up = v.upper()
            strength = ("Strong" if "STRONG" in up else "Contradicted" if "CONTRADICT" in up
                        else "Moderate" if "MODERATE" in up else "Directional" if ("WEAK" in up or "DIRECTIONAL" in up)
                        else "Present")
            score = {"Strong":4,"Moderate":3,"Directional":2,"Present":1,"Contradicted":0}[strength]
            rows.append([e["dimension"], s.replace("_"," ").title(), strength, score, v])
w("34_evidence_matrix_long.csv",
  ["Dimension","Evidence Source","Strength","Strength Score","Assessment"], rows)

w("35_hypotheses.csv", ["Hypothesis ID","Statement","Test","N","Statistic","P Value","CI","Verdict","Evidence Type"],
  [[h.get("id"), h.get("statement"), h.get("test"), h.get("n"), h.get("statistic"),
    h.get("p_value"), h.get("ci"), h.get("verdict"), h.get("evidence_type")]
   for h in B["hypotheses"]])

w("36_data_quality.csv", ["Anomaly","What We Found","How It Was Handled","Source"],
  [[a.get("anomaly"), a.get("what_we_found"), a.get("how_it_was_handled"), a.get("source")]
   for a in B["anomalies"]])

w("37_analytics_layers.csv",
  ["Analytics Layer","Technique","Applied To","Computed In","Drawn In Tableau","Confidence"],
  [["Descriptive","Proportions with Wilson 95% intervals","Survey n=40","Python","Yes","High"],
   ["Descriptive","Funnels, distributions, box plots, share of wallet","Survey, audit","Tableau-native","Yes","High"],
   ["Diagnostic","McNemar exact test (paired)","Survey n=40","Python","Yes - as a column","High"],
   ["Diagnostic","Fisher exact test","Survey subgroups","Python","Yes - as a column","Underpowered"],
   ["Diagnostic","Spearman rank correlation","Survey n=40","Python","Yes - heatmap","Null results"],
   ["Diagnostic","Waterfall decomposition of price erosion","Audit x survey","Python","Yes","High"],
   ["Predictive","Logistic price-response curve (Gabor-Granger)","6 staircase points","Python","Yes - line + scatter","R2 = 0.964"],
   ["Predictive","Switcher profiling by lift","Survey n=40","Python","Yes - bar","Exploratory only"],
   ["Predictive","Sentiment and volume trend, 16 months","836 documents","Python","Yes - dual line","Descriptive trend"],
   ["Prescriptive","Break-even solve","Benchmarks","Python","Yes - line","Assumption-driven"],
   ["Prescriptive","Scenario simulator","Fitted curve + benchmarks","Tableau parameters","Yes - native","Assumption-driven"],
   ["Prescriptive","Tornado sensitivity","Scenario model","Python","Yes - diverging bar","Assumption-driven"],
   ["Cognitive / text","Lexicon sentiment, negation-aware","836 documents","Python","Yes - as a column","Validated rho = 0.648"],
   ["Cognitive / text","TF-IDF term salience","836 documents","Python","Yes - bar","Light topic modelling"],
   ["Cognitive / text","Theme roll-up and co-occurrence","119 codes","Python","Yes - treemap, bar","Light topic modelling"]])

w("38_propositions.csv",
  ["Bengaluru Tactic","Call","Call Order","Evidence","Key Metric","Key Value"],
  [["Charge no platform, packaging or surge fee","KEEP",1,
    "Fee load 5.2% vs incumbent median 23.4%. Structural, needs no subsidy.","K3 Fee load","5.2%"],
   ["Transparent everyday pricing - total you see is total you pay","KEEP",1,
    "Cheapest in 4 of 4 baskets; median saving Rs 114.50 against a stated Rs 30 bar.","K1a Price win rate","100%"],
   ["Headline claim: cheaper than Swiggy and Zomato","ADAPT",2,
    "82.5% hold a membership; after one coupon Ownly is Rs 28 dearer. Claim is falsifiable.","K11 Membership lock-in","82.5%"],
   ["Stock the same big chains","ADAPT",2,
    "88.9% catalogue overlap, +17 min slower. Only 35% will give up their restaurants.","K5 Assortment overlap","88.9%"],
   ["Rely on Rapido placement for growth","ADAPT",2,
    "Only 5 of 33 answering had noticed food inside Rapido - an 84.8% discovery gap.","K9 Rapido discovery","15.2%"],
   ["Rs 100 off the first order","DEPRIORITISE",3,
    "25% post-offer repeat intent; 87.5% expect prices to rise. Rented demand.","K18 Post-promo repeat","25.0%"],
   ["Spend to match delivery speed","DEPRIORITISE",3,
    "92.5% accept 15 min slower. Pre-registered prediction P3 was falsified.","K20 Trades speed","92.5%"]])

w("39_problem_statement.csv", ["Section","Order","Content"],
  [["Business problem",1,
    "Ownly is a food-delivery platform backed by Rapido. It charges restaurants no commission and adds no platform, packaging or surge fees, so the customer's bill is lower. It launched in Bengaluru and is now live in Hyderabad."],
   ["Why the obvious question is wrong",2,
    "Discounts reliably produce trial. Foodpanda, Uber Eats India and Amazon Food each bought early volume and then exited. Foodpanda fell from roughly 200,000 daily orders to about 5,000 once discounting stopped. No challenger in the Indian record has demonstrated post-subsidy retention."],
   ["Research question",3,
    "How large and durable must Ownly's price advantage be to break Swiggy/Zomato lock-in in Gachibowli, and what restaurant coverage, discovery and delivery experience are required so that price-led trial becomes repeat usage?"],
   ["Decision this serves",4,
    "Per-tactic KEEP / ADAPT / DEPRIORITISE on the Bengaluru playbook. Not whether to enter - Ownly is already live at the audited address."],
   ["Evidence base",5,
    "Survey n=40 in catchment (124 received). Price audit: 4 matched baskets across a 10-restaurant frame, one address, one dinner slot. 836 public documents across 16 months. Interviews: 1 documented transcript plus team-reported. Fake-door experiment designed, powered, not fielded."],
   ["Population and limits",6,
    "Adults 20-35 ordering into the Gachibowli catchment. Convenience sample, not probability. Results describe this sample and are directional for the catchment. Every proportion carries a 95% Wilson interval."]])

print("Tableau extracts written to ./Data\n")
print(f"{'FILE':42s} {'ROWS':>6s} {'COLS':>5s}")
print("-"*58)
for n, r, c in written:
    print(f"{n:42s} {r:>6d} {c:>5d}")
print("-"*58)
print(f"{len(written)} files · {sum(r for _,r,_ in written)} rows total")
