#!/usr/bin/env python3
"""Build the case-study Tableau workbook from ./Data using the verified generator."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "SUBMIT_TABLEAU"))
import twb_gen as G
HERE = os.path.dirname(os.path.abspath(__file__))
G.HERE = HERE
G.DATA = os.path.join(HERE, "Data_tableau")   # sanitised headers: Tableau rejects %, #, (), - in field names

DS = [
 ("federated.timeline", "03_social_timeline_by_audience.csv", "Social timeline"),
 ("federated.events",   "01_bengaluru_event_register.csv",    "Bengaluru events"),
 ("federated.demands",  "02_boycott_demands.csv",             "Boycott demands"),
 ("federated.city",     "09_city_comparison.csv",             "City comparison"),
 ("federated.trade",    "10_tradeoff.csv",                    "Rs30 trade-off"),
 ("federated.price",    "11_price_audit.csv",                 "Price audit"),
 ("federated.erosion",  "12_price_erosion.csv",               "Price erosion"),
 ("federated.fee",      "13_fee_load.csv",                    "Fee load"),
 ("federated.stars",    "14_review_stars.csv",                "Review stars"),
 ("federated.themes",   "15_theme_by_base.csv",               "Themes by base"),
 ("federated.kpi",      "16_kpis.csv",                        "KPIs"),
 ("federated.mm",       "17_marketing_metrics.csv",           "Marketing metrics"),
 ("federated.ne",       "18_not_estimable.csv",               "Not estimable"),
 ("federated.sol",      "19_solutions.csv",                   "Solutions"),
 ("federated.kad",      "20_keep_adapt_deprioritise.csv",     "Keep Adapt Deprioritise"),
 ("federated.sent",     "04_sentiment_by_audience.csv",       "Sentiment by audience"),
 ("federated.phase",    "05_youtube_phase.csv",               "YouTube phase"),
 ("federated.terms",    "07_topic_terms.csv",                 "Topic terms"),
]
W = [
 {"name":"1.1 Conversation by month","ds":"federated.timeline","rows":"Documents","cols":"Month","mark":"Line","color":"Audience"},
 {"name":"1.2 Bengaluru event register","ds":"federated.events","rows":["Month","Event","Detail"],"cols":None,"mark":"Text","color":"Actor"},
 {"name":"1.3 Boycott demands","ds":"federated.demands","rows":["Grievance type","Demand verbatim"],"cols":None,"mark":"Text"},
 {"name":"1.4 Bengaluru vs Hyderabad","ds":"federated.city","rows":"Metric","cols":"Value","mark":"Bar","color":"City"},
 {"name":"2.1 KPI overview","ds":"federated.kpi","rows":"KPI","cols":"Value","mark":"Bar","label":"Value","color":"Source"},
 {"name":"2.2 KPI detail","ds":"federated.kpi","rows":["KPI","Question it answers","Why it matters"],"cols":None,"mark":"Text","label":"Value"},
 {"name":"3.1 Marketing metrics","ds":"federated.mm","rows":"Metric","cols":"Value","mark":"Bar","label":"Value","color":"Our own definition"},
 {"name":"3.2 Not estimable","ds":"federated.ne","rows":["Metric","Why not computable"],"cols":None,"mark":"Text"},
 {"name":"4.1 The Rs30 trade-off","ds":"federated.trade","rows":"Give up","cols":"Accept Pct","mark":"Bar","label":"Accept Pct","color":"Is the constraint"},
 {"name":"4.2 Price by restaurant","ds":"federated.price","rows":"Restaurant","cols":"Ownly payable","mark":"Bar","label":"Saving Rs"},
 {"name":"4.3 Price erosion","ds":"federated.erosion","rows":"Price view","cols":"Coverage Pct","mark":"Bar","label":"Median saving Rs","color":"Ownly dearer"},
 {"name":"4.4 Fee load","ds":"federated.fee","rows":"Platform","cols":"Median fee load Pct","mark":"Bar","label":"Median fee load Pct"},
 {"name":"4.5 Review ratings","ds":"federated.stars","rows":"Star rating","cols":"Reviews","mark":"Bar","label":"Reviews","color":"Low rating"},
 {"name":"4.6 Themes by who is speaking","ds":"federated.themes","rows":"Theme","cols":"Share of coded items Pct","mark":"Bar","color":"Base"},
 {"name":"4.7 Sentiment by audience","ds":"federated.sent","rows":"Audience","cols":"Mean sentiment","mark":"Bar","label":"Documents"},
 {"name":"4.8 YouTube pre vs post launch","ds":"federated.phase","rows":"Phase","cols":"Mean sentiment","mark":"Bar","label":"Comments"},
 {"name":"4.9 Topic terms","ds":"federated.terms","rows":["Group","Term"],"cols":"TF IDF","mark":"Bar"},
 {"name":"5.1 Keep Adapt Deprioritise","ds":"federated.kad","rows":["Call","Playbook element","Why"],"cols":None,"mark":"Text","color":"Call"},
 {"name":"5.2 Solutions","ds":"federated.sol","rows":["Solution","What to do","Evidence"],"cols":None,"mark":"Text"},
]
D = [
 {"name":"1 The case","sheets":["1.1 Conversation by month","1.4 Bengaluru vs Hyderabad","1.2 Bengaluru event register","1.3 Boycott demands"],"cols":2,"w":1500,"h":1000},
 {"name":"2 KPIs","sheets":["2.1 KPI overview","2.2 KPI detail"],"cols":2,"w":1500,"h":950},
 {"name":"3 Marketing metrics","sheets":["3.1 Marketing metrics","3.2 Not estimable"],"cols":2,"w":1500,"h":950},
 {"name":"4 Analysis","sheets":["4.1 The Rs30 trade-off","4.3 Price erosion","4.2 Price by restaurant","4.4 Fee load","4.6 Themes by who is speaking","4.5 Review ratings","4.7 Sentiment by audience","4.9 Topic terms"],"cols":3,"w":1700,"h":1100},
 {"name":"5 Solutions","sheets":["5.1 Keep Adapt Deprioritise","5.2 Solutions"],"cols":1,"w":1500,"h":1000},
]
if __name__ == "__main__":
    twb  = os.path.join(HERE, "Ownly_Case_Study.twb")
    twbx = os.path.join(HERE, "Ownly_Case_Study.twbx")
    xml, files = G.build(twb, twbx, DS, W, D)
    import xml.etree.ElementTree as ET; ET.fromstring(xml)
    names = {x["name"] for x in W}
    missing = [(d["name"], s) for d in D for s in d["sheets"] if s not in names]
    if missing: sys.exit("unknown sheet(s): %s" % missing)
    print("Built Ownly_Case_Study.twbx")
    print("  datasources %d | worksheets %d | dashboards %d | %.0f KB"
          % (len(DS), len(W), len(D), os.path.getsize(twbx)/1024))
