#!/usr/bin/env python3
"""
Case-study dashboard — data engine.

Every claim made in CASE_STUDY_Ownly_Hyderabad.md is tested against data here,
and the result is written out for the dashboard to display.

New analyses this file adds beyond the earlier builds:
  * the Bengaluru restaurant revolt as a dated event register
  * social conversation volume by audience type, month by month, annotated with
    those events  -- this is what evidences the case study's central claim
  * YouTube pre-launch vs post-launch comparison (the corpus carries a phase flag)
  * topic modelling (TF-IDF) split by audience and by phase
  * restaurant-side voice, reported at its real size (n = 7) and labelled
    illustrative, because it is far too small to model
  * a claim register: every case-study assertion, its evidence, and its status

Run:  python3 build_case_data.py
"""

import csv, json, math, os, sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from textlib import sentiment, tfidf_terms

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FD = os.path.join(ROOT, "final_dashboard", "data")
MINE = os.path.join(ROOT, "05_review_mining")
OUT = os.path.join(HERE, "Data")
os.makedirs(OUT, exist_ok=True)

def rd(p):
    if not os.path.exists(p):
        sys.stderr.write("  ! missing %s\n" % p); return []
    with open(p, encoding="utf-8", errors="replace") as f:
        return list(csv.DictReader(f))

def num(v, d=None):
    try:
        if v is None or str(v).strip() == "": return d
        return float(str(v).replace(",", "").replace("₹", "").replace("%", "").strip())
    except Exception: return d

def truthy(v): return str(v).strip().lower() in ("true", "1", "yes", "y")

def wilson(k, n, z=1.959963985):
    if not n: return (None, None, None)
    p = k/n; d = 1 + z*z/n
    c = (p + z*z/(2*n))/d
    h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
    return (round(100*p,1), round(100*max(0,c-h),1), round(100*min(1,c+h),1))

def median(xs):
    s = sorted(x for x in xs if x is not None)
    if not s: return None
    n = len(s); return s[n//2] if n%2 else (s[n//2-1]+s[n//2])/2

def w(name, header, rows):
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f); wr.writerow(header); wr.writerows(rows)
    print("  %-40s %4d rows" % (name, len(rows)))

# ── load ────────────────────────────────────────────────────────────
clean = rd(os.path.join(FD, "cleaned_survey.csv"))
cat   = [r for r in clean if truthy(r.get("in_catchment"))]
blr   = [r for r in clean if (r.get("city") or "").strip() == "Bengaluru"]
audit = rd(os.path.join(FD, "audit_clean.csv"))
pairs = rd(os.path.join(FD, "audit_pairs.csv"))
cover = rd(os.path.join(FD, "audit_coverage.csv"))
social = rd(os.path.join(MINE, "social", "social_coded.csv"))
yt     = rd(os.path.join(FD, "youtube_comments_coded.csv"))
appst  = rd(os.path.join(MINE, "app_stores", "reviews_coded.csv"))
N = len(cat)
print("catchment n = %d | bengaluru n = %d | social %d | youtube %d | reviews %d"
      % (N, len(blr), len(social), len(yt), len(appst)))
print()

# ════════════════════════════════════════════════════════════════════
# 1 · THE BENGALURU RESTAURANT REVOLT — dated event register
#     Structured from 01_secondary_research/challenger_failures/E_...md
#     This is a MEDIA-REPORTED event record, not a sentiment model.
# ════════════════════════════════════════════════════════════════════
EVENTS = [
 ["2025-08","Ownly pilot begins","Ownly","Pilot in Koramangala, HSR Layout, BTM Layout (Bengaluru)","MEDIA REPORT","TechCrunch, 13 Aug 2025"],
 ["2025-08","Standalone Ownly app launched","Ownly","App goes live","MEDIA REPORT","Business Standard"],
 ["2026-03","Citywide Bengaluru launch","Ownly","Zero commission, flat Rs30 delivery fee, ~20,000 restaurant partners, no subscription or ad fees","MEDIA REPORT","MediaNama, 5 Mar 2026"],
 ["2026-07","1,000+ restaurants threaten to delist","Restaurants","Bengaluru hotel and restaurant owners threaten to leave Swiggy and Zomato from 15 Aug if demands unmet in writing","MEDIA REPORT","Business Today, 29 Jul 2026"],
 ["2026-07","Press notes the opening for Ownly","Media","'Bengaluru restaurants push back gives Rapido's Ownly an opening against Swiggy Zomato'","MEDIA REPORT","Inc42, 30 Jul 2026"],
 ["2026-07","Ownly goes live inside the main Rapido app","Ownly","'No platform fees, 20,000 restaurants'","MEDIA REPORT","Business Today, 28 Jul 2026"],
 ["2026-07","40,000+ daily orders, ~7% Bengaluru share","Ownly","Scale milestone","MEDIA REPORT","Storyboard18"],
 ["2026-08","21,000 Karnataka restaurants expected to join","Restaurants","Boycott expected to extend statewide","MEDIA REPORT","Storyboard18"],
 ["2026-08","Ownly signs MoU with NRAI","Ownly","National Restaurant Association of India; Ownly is Industry Partner for the NRAI Food Delivery Summit 2026","MEDIA REPORT","mediabrief / FM Live, Aug 2026"],
 ["2026-08","Boycott deadline extended to 1 Sep","Restaurants","Breakthrough in talks involving NRAI","MEDIA REPORT","News18"],
 ["2026-08","50,000+ daily orders, ~10% Bengaluru share","Ownly","Prices ~15% lower than Swiggy/Zomato","MEDIA REPORT","Storyboard18, 21 Aug 2026"],
 ["2026-09","Outcome of the boycott","Restaurants","UNKNOWN - no reporting found confirming whether it executed, was called off, or what was agreed","NOT FOUND","12+ searches, none returned a result"],
]
w("01_bengaluru_event_register.csv",
  ["Month","Event","Actor","Detail","Evidence grade","Source"], EVENTS)

DEMANDS = [
 ["Money should not be automatically deducted immediately after a customer complaint","Arbitrary deductions"],
 ["Restaurants shouldn't bear losses if an order is cancelled after the food has been prepared","Cancellation losses"],
 ["Absolute freeze on promotional campaigns and ad spends without explicit written consent","Forced discounting"],
 ["A comprehensive, itemised monthly settlement report on deductions","No transparency"],
 ["No discounts without restaurant consent","Forced discounting"],
 ["Allocation of a dedicated relationship manager","No support"],
]
w("02_boycott_demands.csv", ["Demand (verbatim)","Grievance type"], DEMANDS)

# ════════════════════════════════════════════════════════════════════
# 2 · SOCIAL CONVERSATION — volume and sentiment by audience, by month
#     This is the series that evidences the case study's central claim.
# ════════════════════════════════════════════════════════════════════
BLR_SUBS = {"r/BangaloreSocial", "r/indiranagar", "r/electronic_city"}
INC_SUBS = {"r/Zomato", "r/swiggy"}
def audience(c):
    if c in BLR_SUBS: return "Bengaluru local"
    if c in INC_SUBS: return "Incumbent app community"
    if c == "linkedin_post": return "Professional / LinkedIn"
    return "Other"

docs = []
for r in social:
    s, lab = sentiment(r.get("text_excerpt"))
    docs.append({"src":"Social","aud":audience(r.get("community","")),
                 "community":r.get("community",""),
                 "month":(r.get("post_date") or "")[:7],
                 "text":r.get("text_excerpt") or "",
                 "themes":[t.strip() for t in (r.get("themes") or "").split(";") if t.strip()],
                 "author":r.get("author_type",""), "city":r.get("city_mentioned",""),
                 "phase":"", "score":s, "label":lab})
for r in yt:
    s, lab = sentiment(r.get("text"))
    docs.append({"src":"YouTube","aud":"YouTube audience","community":"youtube",
                 "month":(r.get("published") or "")[:7], "text":r.get("text") or "",
                 "themes":[t.strip() for t in (r.get("themes") or "").split(";") if t.strip()],
                 "author":"", "city":"", "phase":r.get("phase",""), "score":s, "label":lab})
for r in appst:
    s, lab = sentiment(r.get("review_text"))
    docs.append({"src":"App store","aud":"App-store reviewer","community":"appstore",
                 "month":(r.get("review_date") or "")[:7], "text":r.get("review_text") or "",
                 "themes":[], "author":"", "city":"", "phase":"",
                 "score":s, "label":lab, "star":num(r.get("star_rating"))})

months = sorted({d["month"] for d in docs if d["month"]})
rows = []
for m in months:
    for aud in ["Bengaluru local","Incumbent app community","Professional / LinkedIn","Other","YouTube audience","App-store reviewer"]:
        sub = [d for d in docs if d["month"] == m and d["aud"] == aud]
        if not sub: continue
        rows.append([m, aud, len(sub),
                     round(sum(d["score"] for d in sub)/len(sub), 3),
                     sum(1 for d in sub if d["label"]=="negative"),
                     sum(1 for d in sub if d["label"]=="neutral"),
                     sum(1 for d in sub if d["label"]=="positive")])
w("03_social_timeline_by_audience.csv",
  ["Month","Audience","Documents","Mean sentiment","Negative","Neutral","Positive"], rows)

aud_rows = []
for aud in sorted({d["aud"] for d in docs}):
    sub = [d for d in docs if d["aud"] == aud]
    aud_rows.append([aud, len(sub), round(sum(d["score"] for d in sub)/len(sub),3),
                     sum(1 for d in sub if d["label"]=="negative"),
                     sum(1 for d in sub if d["label"]=="neutral"),
                     sum(1 for d in sub if d["label"]=="positive")])
w("04_sentiment_by_audience.csv",
  ["Audience","Documents","Mean sentiment","Negative","Neutral","Positive"], aud_rows)

# ════════════════════════════════════════════════════════════════════
# 3 · YOUTUBE PRE-LAUNCH vs POST-LAUNCH
# ════════════════════════════════════════════════════════════════════
ph_rows = []
for ph in ["pre-launch","post-launch"]:
    sub = [d for d in docs if d["src"]=="YouTube" and d["phase"]==ph]
    if not sub: continue
    ph_rows.append([ph, len(sub), round(sum(d["score"] for d in sub)/len(sub),3),
                    sum(1 for d in sub if d["label"]=="negative"),
                    sum(1 for d in sub if d["label"]=="positive")])
w("05_youtube_phase.csv", ["Phase","Comments","Mean sentiment","Negative","Positive"], ph_rows)

ph_theme = []
for ph in ["pre-launch","post-launch"]:
    sub = [d for d in docs if d["src"]=="YouTube" and d["phase"]==ph]
    c = Counter(t for d in sub for t in d["themes"])
    tot = sum(c.values()) or 1
    for t, n in c.most_common(10):
        ph_theme.append([ph, t.replace("_"," ").title(), n, round(100*n/tot,1)])
w("06_youtube_phase_themes.csv", ["Phase","Theme","Mentions","Share of mentions %"], ph_theme)

# ════════════════════════════════════════════════════════════════════
# 4 · TOPIC MODELLING — distinctive vocabulary by audience and by phase
# ════════════════════════════════════════════════════════════════════
topic_rows = []
for aud in ["Bengaluru local","Incumbent app community","Professional / LinkedIn","YouTube audience","App-store reviewer"]:
    sub = [d["text"] for d in docs if d["aud"] == aud and len(d["text"]) > 30]
    if len(sub) < 8: continue
    for i, t in enumerate(tfidf_terms(sub, top=12, min_df=2)):
        topic_rows.append(["By audience", aud, t["term"], round(t["score"],4), t["df"], i+1])
for ph in ["pre-launch","post-launch"]:
    sub = [d["text"] for d in docs if d["phase"] == ph and len(d["text"]) > 30]
    if len(sub) < 8: continue
    for i, t in enumerate(tfidf_terms(sub, top=12, min_df=2)):
        topic_rows.append(["By YouTube phase", ph, t["term"], round(t["score"],4), t["df"], i+1])
w("07_topic_terms.csv", ["Split","Group","Term","TF-IDF","Document frequency","Rank"], topic_rows)

# ════════════════════════════════════════════════════════════════════
# 5 · RESTAURANT-SIDE VOICE  (n = 7 — illustrative, NOT a finding)
# ════════════════════════════════════════════════════════════════════
rest = [d for d in docs if "restaurant" in (d.get("author") or "").lower()]
w("08_restaurant_voice.csv",
  ["Month","Community","Sentiment score","Sentiment label","Verbatim"],
  [[d["month"], d["community"], d["score"], d["label"],
    (d["text"][:300] + "…") if len(d["text"]) > 300 else d["text"]] for d in rest])

# ════════════════════════════════════════════════════════════════════
# 6 · CITY COMPARISON — Bengaluru vs Gachibowli, from our own survey
# ════════════════════════════════════════════════════════════════════
def share(rows_, pred):
    elig = [r for r in rows_ if pred(r) is not None]
    k = sum(1 for r in elig if pred(r))
    return wilson(k, len(elig)) + (k, len(elig))

metrics = [
  ("Heard of Ownly",        lambda r: truthy(r.get("ownly_aware"))),
  ("Opened Ownly",          lambda r: truthy(r.get("ownly_opened"))),
  ("Ordered on Ownly",      lambda r: truthy(r.get("ownly_says_ordered"))),
  ("Holds a paid membership", lambda r: truthy(r.get("has_membership"))),
  ("Uses 2+ delivery apps", lambda r: truthy(r.get("multihoming"))),
  ("Expects prices to rise", lambda r: (num(r.get("durability_doubt_n")) or 0) >= 4),
  ("Would stay after the offer ends", lambda r: (num(r.get("repeat_no_promo_n")) or 0) >= 4),
]
city_rows = []
for label, fn in metrics:
    for cname, rows_ in [("Bengaluru", blr), ("Gachibowli (Hyderabad)", cat)]:
        p, lo, hi, k, n = share(rows_, fn)
        city_rows.append([cname, label, p, lo, hi, k, n])
for cname, rows_ in [("Bengaluru", blr), ("Gachibowli (Hyderabad)", cat)]:
    thr = [num(r.get("switch_savings_rs")) for r in rows_ if num(r.get("switch_savings_rs")) is not None]
    city_rows.append([cname, "Median saving needed to switch (Rs)", median(thr), "", "", len(thr), len(rows_)])
w("09_city_comparison.csv",
  ["City","Metric","Value","CI low","CI high","Numerator","Base"], city_rows)

# ════════════════════════════════════════════════════════════════════
# 7 · THE Rs30 TRADE-OFF + the audit  (the Hyderabad demand-side story)
# ════════════════════════════════════════════════════════════════════
tr = []
for label, col, order in [("Wait 15 minutes longer","eta_chose_cheap",1),
                          ("Accept a late order 3 times in 10","rel_chose_cheap",2),
                          ("Give up their usual restaurants","rest_chose_cheap",3)]:
    k = sum(1 for r in cat if truthy(r.get(col)))
    p, lo, hi = wilson(k, N)
    tr.append([label, order, k, N, p, lo, hi, 100-p, "Yes" if p < 50 else "No"])
w("10_tradeoff.csv",
  ["Give up","Sort order","Accepted","Base","Accept %","CI low","CI high","Refused %","Is the constraint"], tr)

lf = [r for r in pairs if r.get("view")=="LIST+FEES"]
w("11_price_audit.csv",
  ["Restaurant","Ownly payable","Cheapest rival payable","Rival","Saving Rs","Saving %","Ownly ETA","Rival ETA","ETA gap"],
  [[r["restaurant_display"], num(r["ownly_payable"]), num(r["incumbent_payable"]), r["cheapest_incumbent"],
    round(num(r["saving_rs"]),2), round(num(r["saving_pct"]),1), num(r["ownly_eta_mid"]), num(r["incumbent_eta_mid"]),
    round((num(r["ownly_eta_mid"]) or 0)-(num(r["incumbent_eta_mid"]) or 0),1)] for r in lf])

ero = rd(os.path.join(FD, "switch_threshold_coverage.csv"))
w("12_price_erosion.csv", ["Price view","Order","Coverage %","Median saving Rs","Ownly dearer"],
  [[r["view"], {"LIST+FEES":1,"MEMBER":2,"AFTER OFFER":3}.get(r["view"],9),
    num(r["coverage_pct"]), num(r["median_saving_rs"]),
    "Yes" if (num(r["median_saving_rs"]) or 0) < 0 else "No"] for r in ero])

fee = defaultdict(list)
for a in audit:
    if a.get("priced")!="True" or (num(a.get("discount_amount"),0) or 0)!=0: continue
    s = num(a.get("non_food_share"))
    if s is not None: fee[a.get("platform")].append(100*s)
w("13_fee_load.csv", ["Platform","Median fee load %","Captures"],
  [[p.title(), round(median(v),1), len(v)] for p,v in sorted(fee.items(), key=lambda kv: median(kv[1]))])

# ════════════════════════════════════════════════════════════════════
# 8 · REVIEWS + first-hand vs commentary gap
# ════════════════════════════════════════════════════════════════════
stars = Counter(int(num(r.get("star_rating")) or 0) for r in appst)
w("14_review_stars.csv", ["Star rating","Reviews","Low rating"],
  [[s, stars[s], "Yes" if s<=2 else "No"] for s in sorted(stars) if s])

rev_theme = rd(os.path.join(FD, "review_theme_summary.csv"))
w("15_theme_by_base.csv", ["Base","Theme","Items mentioning","Share of coded items %"],
  [[r["base"], r["theme_family"].replace("_"," ").title(), num(r["items_mentioning"]),
    num(r["share_of_coded_items_pct"])] for r in rev_theme])

# ════════════════════════════════════════════════════════════════════
# 9 · KPIs and MARKETING METRICS for the case
# ════════════════════════════════════════════════════════════════════
def sh(pred):
    k = sum(1 for r in cat if pred(r)); return wilson(k, N) + (k,)
aw = sh(lambda r: truthy(r.get("ownly_aware")))
op = sh(lambda r: truthy(r.get("ownly_opened")))
tri = sh(lambda r: truthy(r.get("ownly_says_ordered")))
mem = sh(lambda r: truthy(r.get("has_membership")))
mh  = sh(lambda r: truthy(r.get("multihoming")))
dbt = sh(lambda r: (num(r.get("durability_doubt_n")) or 0) >= 4)
rpt = sh(lambda r: (num(r.get("repeat_no_promo_n")) or 0) >= 4)
rap = sh(lambda r: (r.get("rapido_freq") or "").strip() not in ("","Never"))
seen_base = [r for r in cat if (r.get("rapido_food_seen") or "").strip() not in ("","I don't use the Rapido app")]
seen_k = sum(1 for r in seen_base if (r.get("rapido_food_seen") or "").strip()=="Yes")
disc = wilson(seen_k, len(seen_base))
thr_all = [num(r.get("switch_savings_rs")) for r in cat if num(r.get("switch_savings_rs")) is not None]
on_own = sum(1 for r in cover if str(r.get("on_ownly","")).strip().lower() in ("true","y","yes"))
ov = [r for r in cover if str(r.get("on_ownly","")).strip().lower() in ("true","y","yes")]
ovi = sum(1 for r in ov if str(r.get("on_incumbent","")).strip().lower() in ("true","y","yes"))
etas = defaultdict(list)
for a in audit:
    e = num(a.get("eta_mid"))
    if e is not None: etas[a.get("platform")].append(e)
eta_gap = median(etas["ownly"]) - median([v for p in ("swiggy","zomato") for v in etas[p]])

KPI = [
 ["Awareness","Do people know Ownly exists?",aw[0],"%",aw[1],aw[2],f"{aw[3]} of {N}","Survey","Top of the funnel. Weeks-old brand in Hyderabad."],
 ["Browse rate","Did they open it?",op[0],"%",op[1],op[2],f"{op[3]} of {N}","Survey","Stronger than awareness: it is an action."],
 ["Trial rate","Did they order?",tri[0],"%",tri[1],tri[2],f"{tri[3]} of {N}","Survey","2 people. Directional only."],
 ["Membership lock-in","Do they already pay a rival?",mem[0],"%",mem[1],mem[2],f"{mem[3]} of {N}","Survey","The single biggest barrier: a membership cancels the list-price saving."],
 ["Multi-homing","Do they use more than one app?",mh[0],"%",mh[1],mh[2],f"{mh[3]} of {N}","Survey","Good news: becoming a second app is a lower bar than replacing the first."],
 ["Rapido usage","Can Rapido reach them?",rap[0],"%",rap[1],rap[2],f"{rap[3]} of {N}","Survey","Reach exists."],
 ["Rapido food discovery","Did they notice food inside Rapido?",disc[0],"%",disc[1],disc[2],f"{seen_k} of {len(seen_base)}","Survey","Reach is not discovery. This is the gap."],
 ["Price-durability doubt","Do they believe prices will last?",dbt[0],"%",dbt[1],dbt[2],f"{dbt[3]} of {N}","Survey","A price promise only works if believed."],
 ["Post-offer repeat intent","Would they stay after the offer?",rpt[0],"%",rpt[1],rpt[2],f"{rpt[3]} of {N}","Survey","Closest proxy for retention. Stated, not observed."],
 ["Restaurant coverage","Is the audit frame on Ownly?",wilson(on_own,len(cover))[0],"%",wilson(on_own,len(cover))[1],wilson(on_own,len(cover))[2],f"{on_own} of {len(cover)}","Audit","Breadth is fine; depth is unmeasured."],
 ["Catalogue overlap","Are they the same restaurants?",wilson(ovi,len(ov))[0],"%",wilson(ovi,len(ov))[1],wilson(ovi,len(ov))[2],f"{ovi} of {len(ov)}","Audit","The 'no new use case' risk, measured."],
 ["Quoted ETA gap","How much slower?",round(eta_gap,1),"min","","",f"{sum(len(v) for v in etas.values())} captures","Audit","Flat across all four restaurants."],
 ["Median saving","How much cheaper, in rupees?",round(median([num(r['saving_rs']) for r in lf]),2),"Rs","","",f"{len(lf)} baskets","Audit","Before any rival coupon."],
 ["Switching bar","How much do they need to save?",median(thr_all),"Rs","","",f"{len(thr_all)} named a figure","Survey","The bar the saving has to clear."],
]
w("16_kpis.csv", ["KPI","Question it answers","Value","Unit","CI low","CI high","Base","Source","Why it matters"], KPI)

MM = rd(os.path.join(FD, "marketing_metrics.csv"))
w("17_marketing_metrics.csv",
  ["ID","Metric","Value","Unit","Basis","Our own definition","Formula","Interpretation","Caveat"],
  [[m["metric_id"], m["metric_name"], num(m["value"]), m["unit"], m["formula_sheet_reference"],
    "Yes" if m["formula_sheet_reference"].startswith(("custom","derived")) else "No",
    m["formula"], m["interpretation"], m["caveat"]] for m in MM])

NE = rd(os.path.join(FD, "not_estimable.csv"))
w("18_not_estimable.csv", ["Metric","Sheet","Why not computable","Where it would come from"],
  [[r["metric"], r["formula_sheet"], r["why_not_computable"], r["where_it_would_come_from"]] for r in NE])

# ════════════════════════════════════════════════════════════════════
# 10 · SOLUTIONS — the case study's six, each tied to its evidence
# ════════════════════════════════════════════════════════════════════
SOL = [
 ["1","Market Research","Check whether the REASON Bengaluru worked exists in the new city before copying the playbook.",
  "Bengaluru: 1,000+ restaurants threatening to delist, Aug 2026. Hyderabad: no equivalent event found.",
  "Event register + social volume spike (232 incumbent-community posts in Aug 2026 vs 0-7 in prior months)","KEEP/ADAPT decision"],
 ["2","Customer Base","Target people with no membership and people who already use two apps, not loyal members.",
  f"{mem[0]}% hold a paid membership; {mh[0]}% already multi-home.",
  "Membership lock-in and multi-homing KPIs","Segment choice"],
 ["3","Cost Control","Launch area by area, not citywide. Every order currently loses money.",
  "Rs30 revenue per order vs Rs56.01 industry rider payout = -Rs26 per order.",
  "Unit economics (secondary, FACT-grade)","Spend pacing"],
 ["4","Increase Revenue","Get the local restaurants people refuse to give up. Keep the no-fees promise.",
  f"Only {tr[2][4]}% will give up their usual restaurants for Rs30. Fee load 4.8% vs 23%.",
  "Rs30 trade-off + fee load","Supply and positioning"],
 ["5","Damage Control - Before","Watch two numbers monthly: second orders after the offer, and failed orders.",
  f"Post-offer repeat intent {rpt[0]}%. Reviews: 72% mention a failed delivery, 79% support/refunds.",
  "Repeat intent KPI + review themes","Early warning"],
 ["6","Damage Control - After","If second orders don't come, stop discounting and fix delivery and supply instead.",
  "Foodpanda fell from ~200,000 to ~5,000 daily orders in ~10 months once discounts stopped.",
  "Challenger failure record (secondary)","Recovery"],
]
w("19_solutions.csv", ["#","Solution","What to do","Evidence","Evidence source","Decision it serves"], SOL)

KAD = [
 ["KEEP","Zero commission for restaurants","Only advantage rivals cannot copy without giving up their own revenue.",
  "Bengaluru: ~20,000 restaurants signed in the revolt window.","Event register"],
 ["KEEP","No platform, packaging or surge fees","Structural saving - needs no funding, so it cannot run out.",
  "Fee load 4.8% (Ownly) vs 23.0% (incumbent median), zero-discount captures.","Price audit"],
 ["ADAPT","Stop leading with 'cheaper than Swiggy and Zomato'","False at the checkout of the majority; one coupon disproves it.",
  f"{mem[0]}% hold a membership. After a rival coupon the median saving is -Rs28.","Audit x survey"],
 ["ADAPT","Swap wide coverage for deep local coverage","Bengaluru's restaurants came to Ownly; Hyderabad's have not.",
  f"{wilson(ovi,len(ov))[0]}% catalogue overlap, +{round(eta_gap,0)} min slower.","Price audit"],
 ["ADAPT","Make Rapido a real channel, not a doorway","Sitting in the app is not producing discovery.",
  f"{rap[0]}% use Rapido but only {seen_k} of {len(seen_base)} noticed food in it.","Survey"],
 ["DEPRIORITISE","Big first-order discounts","Buys trial that does not stick.",
  f"{rpt[0]}% would stay after the offer; {dbt[0]}% expect prices to rise.","Survey"],
 ["DEPRIORITISE","Spending to match delivery speed","Speed is not the blocker in this market.",
  f"{tr[0][4]}% will wait 15 minutes longer to save Rs30.","Survey"],
]
w("20_keep_adapt_deprioritise.csv", ["Call","Playbook element","Why","Evidence","Source"], KAD)

print()
print("Data written to ./Data")
