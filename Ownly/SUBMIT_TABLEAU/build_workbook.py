#!/usr/bin/env python3
"""
Ownly Gachibowli — Tableau workbook builder.

Declares every datasource, worksheet and dashboard, then emits
Ownly_Gachibowli_BI.twbx via twb_gen.

Dashboard structure follows the brief exactly — five sections:
  1  Problem Statement
  2  KPIs
  3  Marketing Metrics
  4  Analytics
  5  Propositions

Every worksheet draws NATIVELY in Tableau. Values that Tableau cannot compute
(logistic fit, sentiment scores, exact-test p-values, Wilson intervals, TF-IDF,
lift) were computed in Python and are materialised as columns in ./Data.

Run:  python3 build_workbook.py
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import twb_gen as G

HERE = G.HERE

# ── datasources: (internal name, csv file, caption) ──────────────────
DS = [
    ("federated.problem",   "39_problem_statement.csv",        "Problem Statement"),
    ("federated.funnels",   "10_funnels.csv",                  "Funnels"),
    ("federated.layers",    "37_analytics_layers.csv",         "Analytics Layers"),
    ("federated.kpi",       "01_kpi_summary.csv",              "KPI Summary"),
    ("federated.mm",        "02_marketing_metrics.csv",        "Marketing Metrics"),
    ("federated.ne",        "03_not_estimable.csv",            "Not Estimable"),
    ("federated.trade",     "04_tradeoffs.csv",                "Trade-offs"),
    ("federated.ttest",     "05_tradeoff_tests.csv",           "Paired Tests"),
    ("federated.erosion",   "09_price_erosion.csv",            "Price Erosion"),
    ("federated.priceplat", "07b_price_by_platform_long.csv",  "Price by Platform"),
    ("federated.bill",      "08_bill_composition_long.csv",    "Bill Composition"),
    ("federated.curve",     "11_demand_curve.csv",             "Demand Curve"),
    ("federated.sentsrc",   "16b_sentiment_by_source_long.csv","Sentiment by Source"),
    ("federated.senttrend", "15_text_trend_monthly.csv",       "Sentiment Trend"),
    ("federated.themes",    "14_theme_families.csv",           "Theme Families"),
    ("federated.sentval",   "17_sentiment_validation.csv",     "Sentiment Validation"),
    ("federated.terms",     "18_tfidf_terms.csv",              "TF-IDF Terms"),
    ("federated.evmat",     "34_evidence_matrix_long.csv",     "Evidence Matrix"),
    ("federated.city",      "24_city_benchmark_long.csv",      "City Benchmark"),
    ("federated.coverage",  "22_coverage_long.csv",            "Restaurant Coverage"),
    ("federated.profile",   "27_switcher_profiling.csv",       "Switcher Profiling"),
    ("federated.breakeven", "31_breakeven_grid_long.csv",      "Break-even Grid"),
    ("federated.levers",    "32_lever_sensitivity.csv",        "Lever Sensitivity"),
    ("federated.props",     "38_propositions.csv",             "Propositions"),
    ("federated.failures",  "25_challenger_failure_modes.csv", "Challenger Failures"),
    ("federated.stars",     "21_review_stars.csv",             "Review Stars"),
    ("federated.eta",       "23_eta_by_platform_long.csv",     "ETA by Platform"),
    ("federated.segments",  "28_segment_cuts_long.csv",        "Segment Cuts"),
]

# ── worksheets ───────────────────────────────────────────────────────
W = [
    # ── 1 · PROBLEM STATEMENT ──────────────────────────────────────
    {"name": "1.1 Business Problem", "ds": "federated.problem",
     "rows": ["Section", "Content"], "cols": None, "mark": "Text", "label": "Order"},
    {"name": "1.2 Research Funnel", "ds": "federated.funnels",
     "rows": "Stage", "cols": "N", "mark": "Bar", "label": "N",
     "filters": [("Funnel", ["Research sample"])]},
    {"name": "1.3 Analytics Applied", "ds": "federated.layers",
     "rows": ["Analytics Layer", "Technique"], "cols": None, "mark": "Text",
     "color": "Computed In"},

    # ── 2 · KPIs ───────────────────────────────────────────────────
    {"name": "2.1 Headline KPIs", "ds": "federated.kpi",
     "rows": "KPI Name", "cols": "Value", "mark": "Bar", "label": "Value",
     "color": "Driver", "filters": [("Is Headline", ["Yes"])]},
    {"name": "2.2 KPI Coverage", "ds": "federated.kpi",
     "rows": "Layer", "cols": None, "mark": "Bar", "color": "Not Computable"},
    {"name": "2.3 Adoption Funnel", "ds": "federated.funnels",
     "rows": "Stage", "cols": "Pct", "mark": "Bar", "label": "Pct",
     "filters": [("Funnel", ["Ownly adoption"])]},
    {"name": "2.4 KPI Detail", "ds": "federated.kpi",
     "rows": ["Family", "KPI Name"], "cols": None, "mark": "Text", "label": "Value"},

    # ── 3 · MARKETING METRICS ──────────────────────────────────────
    {"name": "3.1 Marketing Metrics", "ds": "federated.mm",
     "rows": "Metric Name", "cols": "Value", "mark": "Bar", "label": "Value",
     "color": "Our Own Definition"},
    {"name": "3.2 Not Estimable", "ds": "federated.ne",
     "rows": ["Metric", "Why Not Computable"], "cols": None, "mark": "Text"},

    # ── 4 · ANALYTICS ──────────────────────────────────────────────
    {"name": "4.1 The Rs30 Trade-off", "ds": "federated.trade",
     "rows": "Description", "cols": "Accept Pct", "mark": "Bar", "label": "Accept Pct",
     "color": "Is Constraint"},
    {"name": "4.2 Paired Tests", "ds": "federated.ttest",
     "rows": "Comparison", "cols": "Neg Log10 P", "mark": "Bar", "label": "P Value"},
    {"name": "4.3 Price Erosion", "ds": "federated.erosion",
     "rows": "Price View", "cols": "Coverage Pct", "mark": "Bar", "label": "Median Saving Rs",
     "color": "Ownly Is Dearer"},
    {"name": "4.4 Price by Platform", "ds": "federated.priceplat",
     "rows": "Restaurant", "cols": "Final Payable Rs", "mark": "Bar", "color": "Platform",
     "filters": [("Price View", ["LIST+FEES"])]},
    {"name": "4.5 Bill Composition", "ds": "federated.bill",
     "rows": "Platform", "cols": "Pct Of Bill", "mark": "Bar", "color": "Component"},
    {"name": "4.6 Demand Curve", "ds": "federated.curve",
     "rows": "Pct Would Switch", "cols": "Saving Rs", "mark": "Line", "color": "Series"},
    {"name": "4.7 Sentiment by Source", "ds": "federated.sentsrc",
     "rows": "Source", "cols": "Pct Of Source", "mark": "Bar", "color": "Sentiment Label"},
    {"name": "4.8 Sentiment Over Time", "ds": "federated.senttrend",
     "rows": "Mean Sentiment", "cols": "Month", "mark": "Line", "label": "Documents"},
    {"name": "4.9 Theme Families", "ds": "federated.themes",
     "rows": "Theme Family", "cols": "Documents", "mark": "Bar",
     "color": "Mean Sentiment", "label": "Documents"},
    {"name": "4.10 Sentiment Validation", "ds": "federated.sentval",
     "rows": "Star Rating", "cols": "Mean Sentiment Score", "mark": "Bar",
     "label": "Mean Sentiment Score"},
    {"name": "4.11 Distinctive Terms", "ds": "federated.terms",
     "rows": "Term", "cols": "TFIDF Score", "mark": "Bar",
     "filters": [("Scope", ["Overall"])]},
    {"name": "4.12 Evidence Triangulation", "ds": "federated.evmat",
     "rows": "Dimension", "cols": "Evidence Source", "mark": "Square",
     "color": "Strength Score"},
    {"name": "4.13 City Benchmark", "ds": "federated.city",
     "rows": "Value", "cols": "Metric", "mark": "Line", "color": "City Base"},
    {"name": "4.14 Restaurant Coverage", "ds": "federated.coverage",
     "rows": "Restaurant", "cols": "Platform", "mark": "Square", "color": "Listing Status"},
    {"name": "4.15 Switcher Profiling", "ds": "federated.profile",
     "rows": "Feature", "cols": "Lift", "mark": "Bar", "color": "Lift Direction",
     "filters": [("Target", ["Will give up usual restaurants for ₹30"])]},
    {"name": "4.16 Delivery Time Gap", "ds": "federated.eta",
     "rows": "Restaurant", "cols": "Quoted ETA Min", "mark": "Bar", "color": "Platform"},
    {"name": "4.17 Review Ratings", "ds": "federated.stars",
     "rows": "Star Rating", "cols": "Reviews", "mark": "Bar", "color": "Is Low Rating",
     "label": "Reviews"},
    {"name": "4.18 Segment Scorecard", "ds": "federated.segments",
     "rows": "Segment", "cols": "Value", "mark": "Bar", "color": "Metric"},

    # ── 5 · PROPOSITIONS ───────────────────────────────────────────
    {"name": "5.1 Propositions", "ds": "federated.props",
     "rows": ["Call", "Bengaluru Tactic", "Evidence"], "cols": None, "mark": "Text",
     "color": "Call"},
    {"name": "5.2 Break-even", "ds": "federated.breakeven",
     "rows": "Contribution Per Order Rs", "cols": "Revenue Per Order Rs",
     "mark": "Line", "color": "Rider Cost Scenario"},
    {"name": "5.3 Lever Sensitivity", "ds": "federated.levers",
     "rows": "Lever", "cols": "Swing", "mark": "Bar", "color": "Lever Type", "label": "Swing"},
    {"name": "5.4 Why Challengers Fail", "ds": "federated.failures",
     "rows": ["Failure Mechanism", "Ownly Status"], "cols": None, "mark": "Text",
     "color": "Ownly Status"},
]

# ── dashboards: the five sections in the brief ───────────────────────
D = [
    {"name": "1 Problem Statement",
     "sheets": ["1.1 Business Problem", "1.2 Research Funnel", "1.3 Analytics Applied"],
     "cols": 2, "w": 1500, "h": 950},
    {"name": "2 KPIs",
     "sheets": ["2.1 Headline KPIs", "2.3 Adoption Funnel", "2.2 KPI Coverage", "2.4 KPI Detail"],
     "cols": 2, "w": 1500, "h": 950},
    {"name": "3 Marketing Metrics",
     "sheets": ["3.1 Marketing Metrics", "3.2 Not Estimable"],
     "cols": 2, "w": 1500, "h": 950},
    {"name": "4 Analytics",
     "sheets": ["4.1 The Rs30 Trade-off", "4.3 Price Erosion", "4.6 Demand Curve",
                "4.9 Theme Families", "4.7 Sentiment by Source", "4.8 Sentiment Over Time",
                "4.12 Evidence Triangulation", "4.15 Switcher Profiling"],
     "cols": 3, "w": 1700, "h": 1100},
    {"name": "5 Propositions",
     "sheets": ["5.1 Propositions", "5.3 Lever Sensitivity", "5.2 Break-even",
                "5.4 Why Challengers Fail"],
     "cols": 2, "w": 1500, "h": 1000},
]

if __name__ == "__main__":
    twb = os.path.join(HERE, "Ownly_Gachibowli_BI.twb")
    twbx = os.path.join(HERE, "Ownly_Gachibowli_BI.twbx")
    xml, files = G.build(twb, twbx, DS, W, D)

    import xml.etree.ElementTree as ET
    ET.fromstring(xml)

    # every worksheet a dashboard references must exist
    names = {w["name"] for w in W}
    missing = [(d["name"], s) for d in D for s in d["sheets"] if s not in names]
    if missing:
        sys.exit("Dashboard references unknown worksheet(s): %s" % missing)

    print("Built  %s" % os.path.basename(twbx))
    print("  XML well-formed : yes")
    print("  datasources     : %d" % len(DS))
    print("  worksheets      : %d" % len(W))
    print("  dashboards      : %d" % len(D))
    print("  CSVs packaged   : %d" % len(files))
    print("  size            : %.0f KB" % (os.path.getsize(twbx) / 1024))
