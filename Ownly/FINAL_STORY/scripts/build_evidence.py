#!/usr/bin/env python3
"""
build_evidence.py - every number on the Ownly story dashboard is computed here.

Reads the project's source files directly, computes each figure, and writes:
  data/evidence.csv        one row per number shown anywhere on the dashboard
  data/<chart>.csv         one tidy table per chart (Tableau and the HTML read these)

Standard library only (no pandas), so anyone can re-run it:  python3 build_evidence.py

Sample rule, applied to every percentage:
  n >= 30        -> "OK"            report the %, with its 95% Wilson interval
  10 <= n < 30   -> "Small"         report the % and interval, label it directional
  n < 10         -> "Too small"     report "k of n" only, never a %
Figures taken from outside sources (media, company filings) are not computed here;
they are listed with their source and evidence grade, and marked "Reported".
"""
import csv, math, os, statistics, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "..", "data")
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, HERE)
from xlsx_reader import read as read_xlsx

SRC = {
    "survey":  "final_dashboard/data/cleaned_survey.csv",
    "audit":   "final_dashboard/data/audit_clean.csv",
    "pairs":   "final_dashboard/data/audit_pairs.csv",
    "cover":   "final_dashboard/data/audit_coverage.csv",
    "eta":     "final_dashboard/data/eta_gap_by_restaurant.csv",
    "reviews": "05_review_mining/app_stores/reviews_coded.csv",
    "social":  "05_review_mining/social/social_coded.csv",
    "youtube": "final_dashboard/data/youtube_comments_coded.csv",
    "fd_direct": "ownly_direct.xlsx",
    "fd_rapido": "ownly_rapido.xlsx",
}


def rows(key):
    with open(os.path.join(ROOT, SRC[key]), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write(name, header, data):
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(data)


def wilson(k, n, z=1.96):
    if n == 0:
        return (None, None)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(100 * max(0, c - h), 1), round(100 * min(1, c + h), 1))


def check(n):
    if n >= 30:
        return "OK"
    if n >= 10:
        return "Small - directional"
    return "Too small - count only"


EVID = []   # the evidence page


def pct(eid, screen, claim, k, n, source, method):
    """Register a computed proportion and return its display string."""
    lo, hi = wilson(k, n)
    v = round(100 * k / n, 1) if n else None
    verdict = check(n)
    shown = f"{k} of {n}" if verdict.startswith("Too small") else f"{v:g}%"
    EVID.append([eid, screen, claim, shown, k, n, v, lo, hi, verdict, method, SRC.get(source, source), "Computed"])
    return v


def num(eid, screen, claim, value, n, source, method, unit=""):
    """Register a computed non-proportion (median, count, rupees, minutes)."""
    shown = f"{value:g}{unit}" + (f" (n={n})" if n and n < 10 else "")
    EVID.append([eid, screen, claim, shown, "", n, value, "", "", check(n).replace("count only", "shown with its n") if n else "",
                 method, SRC.get(source, source), "Computed"])
    return value


def reported(eid, screen, claim, shown, grade, source):
    EVID.append([eid, screen, claim, shown, "", "", "", "", "", "Not a sample", grade, source, "Reported"])


def yes(v):
    return str(v).strip().lower() in ("true", "1", "yes")


# ════════════════════════════════════════════════════════════════════
# 1. SURVEY  (Gachibowli catchment, n = 40; Bengaluru, n = 16)
# ════════════════════════════════════════════════════════════════════
SV = rows("survey")
H = [r for r in SV if yes(r["pop_HYD_CATCHMENT"])]
B = [r for r in SV if yes(r["pop_BLR_ELIGIBLE"])]
nH, nB = len(H), len(B)
assert nH == 40 and nB == 16, (nH, nB)


def count(R, col, fn=yes):
    return sum(1 for r in R if fn(r[col]))


# --- behaviour (screen 2)
S2 = "2 Hyderabad users"
mem = count(H, "has_membership")
pct("B1", S2, "Hold Swiggy One and/or Zomato Gold", mem, nH, "survey", "has_membership = True / catchment")
both = sum(1 for r in H if "Swiggy One" in r["memberships"] and "Zomato Gold" in r["memberships"])
pct("B2", S2, "Hold BOTH memberships", both, nH, "survey", "memberships contains both / catchment")
mh = count(H, "multihoming")
pct("B3", S2, "Use two or more delivery apps", mh, nH, "survey", "multihoming = True / catchment")
orders = Counter()
for r in H:
    for app, col in [("Swiggy", "n_swiggy"), ("Zomato", "n_zomato"), ("Ownly", "n_ownly"), ("Other", "n_other")]:
        try:
            orders[app] += float(r[col] or 0) if not (app == "Ownly" and yes(r["ownly_order_conflict"])) else 0
        except ValueError:
            pass
tot = sum(orders.values())
for app in ["Swiggy", "Zomato", "Ownly", "Other"]:
    num("B4-" + app, S2, f"Share of last-4-week orders placed on {app}", round(100 * orders[app] / tot, 1), nH,
        "survey", f"sum(n_{app.lower()}) / sum(all orders), catchment; {int(tot)} orders", "%")
fee_base = [r for r in H if r["bill_fairness"]]
fee_pain = sum(1 for r in fee_base if "extra charges" in r["bill_fairness"])
pct("B5", S2, "Last bill felt unfair because of the extra charges", fee_pain, len(fee_base), "survey",
    "bill_fairness = 'extra charges on top were too much' / answered")
stud = sum(1 for r in H if r["occupation"].startswith("Student"))
pct("B6", S2, "Students in the sample", stud, nH, "survey", "occupation starts 'Student' / catchment")
a2024 = sum(1 for r in H if r["age_band"] == "20–24")
pct("B7", S2, "Aged 20-24", a2024, nH, "survey", "age_band = 20-24 / catchment")
thr = [float(r["switch_savings_rs"]) for r in H if r["switch_savings_rs"]]
num("B8", S2, "Median saving per order needed to switch apps (Rs)", statistics.median(thr), len(thr), "survey",
    "median(switch_savings_rs) among those who named a figure", " Rs")
never = count(H, "switch_never")
num("B9", S2, "Said no saving would make them switch", never, nH, "survey", "switch_never = True (count)")

write("s2_order_share.csv", ["App", "Orders", "Share_pct", "Sort"],
      [[a, int(orders[a]), round(100 * orders[a] / tot, 1), i] for i, a in enumerate(["Swiggy", "Zomato", "Other", "Ownly"])])
write("s2_behaviour.csv", ["Measure", "Yes", "Base", "Pct", "CI_low", "CI_high", "Sample", "Sort"],
      [[m, k, n, round(100 * k / n, 1), *wilson(k, n), check(n), i] for i, (m, k, n) in enumerate([
          ("Pay for a Swiggy/Zomato membership", mem, nH),
          ("Use 2+ delivery apps", mh, nH),
          ("Felt the extra charges were too much", fee_pain, len(fee_base)),
      ])])

# --- funnel and barriers (screen 3, KPIs)
S3 = "3 KPIs"
aw, op, od = count(H, "ownly_aware"), count(H, "ownly_opened"), count(H, "ownly_says_ordered")
pct("K1", S3, "Awareness: heard of Ownly", aw, nH, "survey", "ownly_aware = True / catchment")
pct("K2", S3, "Browse: opened Ownly", op, nH, "survey", "ownly_opened = True / catchment")
pct("K3", S3, "Trial: ordered on Ownly", od, nH, "survey", "ownly_says_ordered = True / catchment")
rap_users = [r for r in H if r["rapido_freq"] and r["rapido_freq"] != "Never"]
pct("K4", S3, "Use Rapido (any frequency, last 4 weeks)", len(rap_users), nH, "survey", "rapido_freq not in (Never, blank) / catchment")
seen_base = [r for r in H if r["rapido_food_seen"] in ("Yes", "No", "Not sure")]
seen = sum(1 for r in seen_base if r["rapido_food_seen"] == "Yes")
pct("K5", S3, "Noticed food inside the Rapido app", seen, len(seen_base), "survey",
    "rapido_food_seen = Yes / (Yes + No + Not sure)")
dd = sum(1 for r in H if r["durability_doubt_n"] and float(r["durability_doubt_n"]) >= 4)
pct("K6", S3, "Expect a new app's low prices to rise", dd, nH, "survey", "durability_doubt_n >= 4 (agree) / catchment")
rp = sum(1 for r in H if r["repeat_no_promo_n"] and float(r["repeat_no_promo_n"]) >= 4)
pct("K7", S3, "Would keep ordering after the Rs100 offer ends", rp, nH, "survey", "repeat_no_promo_n >= 4 (likely) / catchment")
aw_rap = sum(1 for r in rap_users if yes(r["ownly_aware"]))
non_rap = [r for r in H if r not in rap_users]
aw_non = sum(1 for r in non_rap if yes(r["ownly_aware"]))
pct("K8", S3, "Aware of Ownly - Rapido users", aw_rap, len(rap_users), "survey", "ownly_aware among Rapido users")
pct("K9", S3, "Aware of Ownly - non-Rapido users", aw_non, len(non_rap), "survey", "ownly_aware among non-users")

write("s3_funnel.csv", ["Stage", "People", "Base", "Pct", "CI_low", "CI_high", "Sample", "Sort"],
      [[s, k, nH, round(100 * k / nH, 1), *wilson(k, nH), check(nH), i] for i, (s, k) in enumerate([
          ("Heard of Ownly", aw), ("Opened Ownly", op), ("Ordered on Ownly", od)])])
write("s3_barriers.csv", ["KPI", "Yes", "Base", "Pct", "CI_low", "CI_high", "Sample", "Why_it_matters", "Sort"],
      [[m, k, n, round(100 * k / n, 1), *wilson(k, n), check(n), why, i] for i, (m, k, n, why) in enumerate([
          ("Already pay a rival membership", mem, nH, "A membership cancels much of Ownly's list-price saving"),
          ("Expect the low prices to rise", dd, nH, "A price promise only works if it is believed"),
          ("Would stay after the intro offer", rp, nH, "Closest thing to retention the survey can see"),
          ("Noticed food inside Rapido", seen, len(seen_base), "Rapido reaches people; it is not making them notice Ownly"),
      ])])

# --- city comparison (screen 1)
S1 = "1 Problem"
city = []
for label, colfn in [("Heard of Ownly", lambda R: count(R, "ownly_aware")),
                     ("Opened Ownly", lambda R: count(R, "ownly_opened")),
                     ("Ordered on Ownly", lambda R: count(R, "ownly_says_ordered")),
                     ("Pay a rival membership", lambda R: count(R, "has_membership"))]:
    for cname, R in [("Bengaluru", B), ("Gachibowli", H)]:
        k = colfn(R)
        city.append([label, cname, k, len(R), round(100 * k / len(R), 1), *wilson(k, len(R)), check(len(R))])
        pct(f"C-{cname[:3]}-{label[:6]}", S1, f"{cname}: {label}", k, len(R), "survey", f"{label} / {cname} sample")
write("s1_city.csv", ["Measure", "City", "Yes", "Base", "Pct", "CI_low", "CI_high", "Sample"], city)
bthr = [float(r["switch_savings_rs"]) for r in B if r["switch_savings_rs"]]
num("C-BLR-thr", S1, "Bengaluru: median saving needed to switch (Rs)", statistics.median(bthr), len(bthr), "survey",
    "median(switch_savings_rs), Bengaluru", " Rs")

# --- trade-offs (screen 6)
S6 = "6 Customers"
eta = count(H, "eta_chose_cheap")
rel = count(H, "rel_chose_cheap")
rest = count(H, "rest_chose_cheap")
pct("T1", S6, "Take Rs30 off to wait 15 min longer", eta, nH, "survey", "eta_chose_cheap / catchment")
pct("T2", S6, "Take Rs30 off to accept 3-in-10 late orders", rel, nH, "survey", "rel_chose_cheap / catchment")
pct("T3", S6, "Take Rs30 off to give up their usual restaurants", rest, nH, "survey", "rest_chose_cheap / catchment")
# McNemar exact, restaurants vs speed (paired)
b_ = sum(1 for r in H if yes(r["eta_chose_cheap"]) and not yes(r["rest_chose_cheap"]))
c_ = sum(1 for r in H if not yes(r["eta_chose_cheap"]) and yes(r["rest_chose_cheap"]))
m = b_ + c_
p_mc = min(1.0, 2 * sum(math.comb(m, i) for i in range(0, min(b_, c_) + 1)) / 2 ** m)
num("T4", S6, f"Accepted the wait but refused to lose restaurants ({b_}) vs the reverse ({c_}); McNemar exact p",
    float(f"{p_mc:.2g}"), nH, "survey", "exact binomial on discordant pairs")
write("s6_tradeoff.csv", ["Give_up", "Accept", "Base", "Accept_pct", "CI_low", "CI_high", "Sample", "Sort"],
      [[g, k, nH, round(100 * k / nH, 1), *wilson(k, nH), check(nH), i] for i, (g, k) in enumerate([
          ("Wait 15 min longer", eta), ("3-in-10 orders late", rel), ("Lose my usual restaurants", rest)])])

trig_base = [r for r in H if r["ownly_trigger"]]
trig = Counter(r["ownly_trigger"] for r in trig_base)
write("s6_trigger.csv", ["Trigger", "People", "Base", "Sort"],
      [[t, k, len(trig_base), i] for i, (t, k) in enumerate(trig.most_common())])
for t, k in trig.most_common(3):
    pct("T5-" + t[:10], S6, f"What would most make you try Ownly: '{t}'", k, len(trig_base), "survey", "ownly_trigger / answered")

# ════════════════════════════════════════════════════════════════════
# 2. PRICE AUDIT  (4 matched baskets, wed_dinner, one Gachibowli address)
# ════════════════════════════════════════════════════════════════════
S5 = "5 Market"
PA = rows("pairs")
views = ["LIST+FEES", "MEMBER", "AFTER OFFER"]
view_label = {"LIST+FEES": "Menu price + fees", "MEMBER": "With a rival membership", "AFTER OFFER": "After a rival coupon"}
er = []
for i, v in enumerate(views):
    P = [p for p in PA if p["view"] == v]
    wins = sum(1 for p in P if yes(p["ownly_wins"]))
    med = statistics.median(float(p["saving_rs"]) for p in P)
    er.append([view_label[v], wins, len(P), round(med, 2), i])
    num(f"A-win-{i}", S5, f"Ownly cheapest - {view_label[v]} ({wins} of {len(P)} baskets); median saving Rs",
        round(med, 2), len(P), "pairs", "median(saving_rs) over 4 matched baskets", " Rs")
write("s5_price_views.csv", ["View", "Ownly_cheaper", "Baskets", "Median_saving_rs", "Sort"], er)

# switch-threshold coverage: person x basket pairs where saving >= that person's threshold
people = [float(r["switch_savings_rs"]) for r in H if r["switch_savings_rs"]]
cov = []
for i, v in enumerate(views):
    sav = [float(p["saving_rs"]) for p in PA if p["view"] == v]
    k = sum(1 for t in people for s in sav if s >= t)
    n = len(people) * len(sav)
    cov.append([view_label[v], k, n, round(100 * k / n, 1), i])
    pct(f"MM1-{i}", "4 Metrics", f"Switch-threshold coverage - {view_label[v]}", k, n, "pairs",
        "person x basket pairs where Ownly's saving >= that person's stated switching figure")
write("s4_coverage.csv", ["View", "Pairs_clearing", "Pairs", "Coverage_pct", "Sort"], cov)


AU = rows("audit")
priced = [r for r in AU if yes(r["priced"])]
fee = []
for plat in ["ownly", "zomato", "swiggy"]:
    zero = [float(r["non_food_share"]) * 100 for r in priced if r["platform"] == plat and float(r["discount_amount"] or 0) == 0]
    fee.append([plat.capitalize(), round(statistics.median(zero), 1), len(zero)])
    num(f"A-fee-{plat}", S5, f"Median non-food share of the bill (fees+tax) - {plat.capitalize()}, no-discount captures",
        round(statistics.median(zero), 1), len(zero), "audit", "median(non_food_total / final bill)", "%")
write("s5_fee_load.csv", ["Platform", "Fee_share_pct", "Captures"], fee)

CV = rows("cover")
on_inc = [r for r in CV if yes(r["on_incumbent"])]
on_own = [r for r in CV if yes(r["on_ownly"])]
overlap = sum(1 for r in on_own if yes(r["on_incumbent"]))
pct("A-cov", S5, "Audit restaurants that are on Ownly", len(on_own), len(CV), "cover", "on_ownly / restaurant frame")
pct("A-ovl", S5, "Ownly restaurants also on Swiggy or Zomato", overlap, len(on_own), "cover", "on both / on Ownly")
ET = rows("eta")
etas = [r for r in AU if r["eta_mid"]]
own_eta = statistics.median(float(r["eta_mid"]) for r in etas if r["platform"] == "ownly")
inc_eta = statistics.median(float(r["eta_mid"]) for r in etas if r["platform"] != "ownly")
num("A-eta", S5, f"Extra wait quoted on Ownly (median {own_eta:g} min vs rivals {inc_eta:g} min)", round(own_eta - inc_eta, 1),
    len(etas), "audit", "median(Ownly quoted ETA midpoint) - median(Swiggy+Zomato quoted ETA midpoint), all captures with an ETA", " min")
write("s5_eta.csv", ["Restaurant", "Ownly_min", "Fastest_rival_min", "Gap_min"],
      [[r["restaurant_display"], float(r["ownly"]), float(r["best_incumbent"]), float(r["gap"])] for r in ET])

# formula-sheet metrics that the data can support, and the ones it cannot
S4 = "4 Metrics"
cat_buyers = [r for r in H if r["total_orders_4wk"] and float(r["total_orders_4wk"]) > 0]
pen = pct("MM2", S4, "Penetration share: tried Ownly / ordered food at all (last 4 weeks)", od, len(cat_buyers), "survey",
          "Brand penetration / market penetration = Ownly triers / category orderers, within the sample")
vol = round(100 * orders["Ownly"] / tot, 1)
metrics = [
    ["Unit (volume) share", "Ownly orders / all delivery orders", f"{vol:g}% of {int(tot)} orders", "MKT 24604 formula sheet",
     "In-sample only. Ownly has been live for weeks, so this is a floor, not a verdict"],
    ["Penetration share", "Ownly triers / people who order food", f"{od} of {len(cat_buyers)} ({pen:g}%)", "MKT 24604 formula sheet",
     "Small base - the interval runs to 18%"],
    ["Switch-threshold coverage", "Pairs where Ownly's saving >= the person's switching figure", f"{cov[0][3]:g}% -> {cov[1][3]:g}% -> {cov[2][3]:g}%",
     "Our own", "Falls as rival memberships and coupons are applied"],
    ["Fee-load gap", "Rival median non-food share - Ownly's", f"{fee[1][1]:g}% / {fee[2][1]:g}% vs {fee[0][1]:g}%", "Our own",
     "Structural: needs no subsidy. Small capture counts"],
    ["Offer-reversal", "Baskets Ownly wins before, loses after a rival coupon", f"{er[0][1] - er[2][1]} of {er[0][2]} baskets", "Our own",
     "4 baskets - count only"],
]
write("s4_metrics.csv", ["Metric", "Formula", "Result", "Source", "Read_it_as", "Sort"], [m + [i] for i, m in enumerate(metrics)])
write("s4_not_estimable.csv", ["Metric", "Why we cannot compute it"], [
    ["Retention rate", "Needs customers at start and end of a period; the survey is one snapshot"],
    ["Customer lifetime value", "Needs margin and retention - Ownly publishes neither"],
    ["Acquisition cost (CAC)", "Needs Ownly's marketing spend and new-customer count"],
    ["YoY growth / CAGR", "Ownly has been in Hyderabad for weeks - no prior period"],
    ["Revenue market share", "Needs total Gachibowli food-delivery revenue - not published"],
])

# ════════════════════════════════════════════════════════════════════
# 3. REVIEWS, SOCIAL, YOUTUBE  (share of coded items - NOT failure rates)
# ════════════════════════════════════════════════════════════════════
S7 = "7 After the order"
FAMILY = {
    "Price is cheaper": ["PRICE_SAVINGS_OBSERVED", "USER_BILL_COMPARISON", "NO_HIDDEN_FEES", "PRICE_ADVANTAGE", "CHEAPER", "FEE_MODEL_DESCRIPTION"],
    "Doubt the price": ["FUTURE_FEE_CREEP_EXPECTED", "SUSTAINABILITY_SKEPTICISM", "HISTORICAL_PRICE_CONVERGENCE", "MENU_PRICE_INFLATION_ON_OWNLY",
                        "INCUMBENT_CHEAPER_AFTER_OFFERS", "OWNLY_PRICIER_OBSERVED", "PRICE_PARITY_OBSERVED", "ASTROTURF_SUSPICION"],
    "Order went wrong": ["NON_DELIVERY", "LATE_DELIVERY", "PLATFORM_RESTAURANT_CANCELLATION", "MISSING_WRONG_ITEMS", "RIDER_CONDUCT",
                         "LATE_NIGHT_RELIABILITY_RISK", "LARGE_ORDER_TRUST_RISK", "RIDER_MULTI_APP_OBSERVED"],
    "Support / refund failed": ["SUPPORT_UNRESPONSIVE", "SUPPORT_SLOW", "REFUND_ISSUE", "TRUST_LOSS_SCAM_FRAMING"],
    "Restaurants missing": ["ASSORTMENT_LIMITED", "SERVICE_AREA_LIMITED", "CITY_AVAILABILITY_QUESTION"],
}


def fams(s):
    out = set()
    for t in (s or "").replace("|", ";").split(";"):
        t = t.strip().upper()
        for f, keys in FAMILY.items():
            if t and (t in keys or any(t.startswith(k) for k in keys)):
                out.add(f)
    return out


RV = rows("reviews")
SO = rows("social")
so_fh = [r for r in SO if r["relevant"].strip() == "1" and r["first_hand_ownly_use"].strip() == "1"]
so_rel = [r for r in SO if r["relevant"].strip() == "1"]
voice = []
for base, R, key in [("App-store reviews", RV, "reviews"), ("People who ordered (social)", so_fh, "social"),
                     ("General discussion (social)", so_rel, "social")]:
    F = [fams(r["themes"]) for r in R]
    coded = [f for f in F if f]
    for i, fam in enumerate(FAMILY):
        k = sum(1 for f in coded if fam in f)
        voice.append([base, fam, k, len(coded), round(100 * k / len(coded), 1), *wilson(k, len(coded)), check(len(coded)), i])
        if fam in ("Order went wrong", "Support / refund failed", "Doubt the price"):
            pct(f"V-{base[:6]}-{fam[:6]}", S7, f"{base}: mention '{fam}'", k, len(coded), key,
                "items mentioning the theme / items with any coded theme (NOT an order failure rate)")
write("s7_voice.csv", ["Source", "Theme", "Items", "Coded_items", "Pct", "CI_low", "CI_high", "Sample", "Sort"], voice)
one_star = sum(1 for r in RV if r["star_rating"] == "1")
pct("V-1star", S7, "App-store reviews that are 1-star", one_star, len(RV), "reviews", "star_rating = 1 / all reviews")

YT = rows("youtube")
yt_theme = Counter(t for r in YT for t in r["themes"].split(";") if t)
yt_coded = sum(1 for r in YT if r["themes"])
rider = yt_theme["RIDER_ECONOMICS"]
pct("V-yt-rider", S7, "YouTube comments (coded) about rider pay", rider, yt_coded, "youtube", "RIDER_ECONOMICS / comments with a theme")

# ════════════════════════════════════════════════════════════════════
# 4. FAKE DOOR  (live app sessions only)
# ════════════════════════════════════════════════════════════════════
S8 = "6 Customers"
FD = []
excluded = Counter()
for key, ch in [("fd_direct", "Direct link"), ("fd_rapido", "Inside Rapido")]:
    sheet = read_xlsx(os.path.join(ROOT, SRC[key]))
    raw = next(iter(sheet.values()))
    hdr = raw[0]
    seen_sess = set()
    for r in raw[1:]:
        d = {hdr[c]: r.get(c, "") for c in hdr}
        if d["session_id"].startswith("sess_natural"):
            excluded["test / seeded rows (sess_natural_*)"] += 1
            continue
        if d["session_id"] in seen_sess:
            excluded["duplicate session id"] += 1
            continue
        seen_sess.add(d["session_id"])
        d["channel"] = ch
        FD.append(d)
nF = len(FD)
num("F0", S8, "Live fake-door sessions analysed", nF, nF, "fd_direct",
    "all rows minus " + "; ".join(f"{v} {k}" for k, v in excluded.items()))
for k, v in excluded.items():
    num("F0-" + k[:4], S8, f"Excluded: {k}", v, 0, "fd_direct", "count")

filled = lambda d, c: d[c] not in ("", "Skip")


def placed(d):
    return d["placed_order"] == "true"


# funnel per channel
fun = []
for ch in ["Direct link", "Inside Rapido"]:
    R = [d for d in FD if d["channel"] == ch]
    steps = [("Opened Ownly", len(R)),
             ("Picked a dish or place", sum(1 for d in R if d["dish"] or d["restaurant_name"])),
             ("Added food to cart", sum(1 for d in R if int(d["item_count"] or 0) > 0)),
             ("Chose how to pay", sum(1 for d in R if d["bill_id"])),
             ("Pressed Place order", sum(1 for d in R if placed(d)))]
    for i, (s, k) in enumerate(steps):
        fun.append([ch, s, k, len(R), round(100 * k / len(R), 1), i])
    pct(f"F1-{ch[:6]}", S8, f"{ch}: sessions that pressed Place order", steps[-1][1], len(R), "fd_direct", "placed_order = true / sessions")
write("s8_fd_funnel.csv", ["Channel", "Step", "Sessions", "Base", "Pct", "Sort"], fun)

# entry points inside Rapido
ent = []
src_label = {"ride_complete_ad": "Ad after the ride ends", "bottom_nav": "Food tab in bottom bar",
             "top_banner": "Banner at top", "in_app": "Other in-app link"}
for s, lab in src_label.items():
    R = [d for d in FD if d["channel"] == "Inside Rapido" and d["source"] == s]
    if R:
        k = sum(1 for d in R if placed(d))
        ent.append([lab, k, len(R), round(100 * k / len(R), 1), check(len(R))])
        pct(f"F2-{s}", S8, f"Rapido entry '{lab}': placed order", k, len(R), "fd_rapido", "placed / sessions from that entry")
write("s8_fd_entry.csv", ["Entry_point", "Placed", "Sessions", "Pct", "Sample"], ent)

# restaurant reasons
why = Counter(d["why_this_restaurant"] for d in FD if filled(d, "why_this_restaurant"))
nw = sum(why.values())
group = {"It's always good": "Trust / loyalty", "They make it best": "Trust / loyalty", "I always pick them": "Trust / loyalty",
         "Closest / fastest": "Closest / fastest", "Good price": "Good price"}
g = Counter()
for k, v in why.items():
    g[group.get(k, k)] += v
write("s6_fd_why_restaurant.csv", ["Reason", "Answers", "Base", "Pct", "Sort"],
      [[k, v, nw, round(100 * v / nw, 1), i] for i, (k, v) in enumerate(g.most_common())])
for k, v in g.items():
    pct("F3-" + k[:6], S6, f"Why this restaurant: {k}", v, nw, "fd_direct", "grouped why_this_restaurant / answered")

# missing place / missing dish
LOST = ("Open the app I use most", "Don't order")
miss = []
for col, lab in [("not_here_what_next", "Wanted place not on Ownly"), ("no_such_dish_what_next", "Wanted dish not on Ownly")]:
    A = [d[col] for d in FD if filled(d, col)]
    lost = sum(1 for a in A if a in LOST)
    miss.append([lab, "Order lost (usual app / no order)", lost, len(A), round(100 * lost / len(A), 1), *wilson(lost, len(A)), check(len(A))])
    miss.append([lab, "Stayed on Ownly", len(A) - lost, len(A), round(100 * (len(A) - lost) / len(A), 1), *wilson(len(A) - lost, len(A)), check(len(A))])
    pct("F4-" + col[:6], S6, f"{lab}: order lost to usual app or not placed", lost, len(A), "fd_direct",
        "answer in (Open the app I use most, Don't order) / answered")
write("s6_fd_missing.csv", ["Situation", "Outcome", "Answers", "Base", "Pct", "CI_low", "CI_high", "Sample"], miss)

# restaurant picks (catalogue of 14, Paradise listed first)
picks = Counter(d["restaurant_name"] for d in FD if d["restaurant_name"])
npk = sum(picks.values())
write("s6_fd_picks.csv", ["Restaurant", "Sessions", "Base", "Pct"],
      [[k, v, npk, round(100 * v / npk, 1)] for k, v in picks.most_common()])
top, topk = picks.most_common(1)[0]
pct("F5", S6, f"Sessions that picked {top} (listed first, with a badge)", topk, npk, "fd_direct", "restaurant_name / sessions with a pick")

# delivery: Rapido Link take-up by randomised price
S9 = "8 Propositions"
dl = [d for d in FD if d["delivery_id"]]
rl = sum(1 for d in dl if d["delivery_id"] == "rapido_link")
pct("F6", S9, "Paid extra for Rapido Link (25 min vs 42 min)", rl, len(dl), "fd_direct", "delivery_id = rapido_link / chose a delivery")
curve = []
for p in ["15", "25", "35", "49"]:
    R = [d for d in dl if d["rl_price"] == p]
    k = sum(1 for d in R if d["delivery_id"] == "rapido_link")
    curve.append([f"Rs {p}", int(p), k, len(R), round(100 * k / len(R), 1), check(len(R))])
    pct(f"F6-{p}", S9, f"Rapido Link take-up at Rs{p}", k, len(R), "fd_direct", "rapido_link / chose delivery, at that randomised price")
write("s8_fd_speed.csv", ["Price", "Price_rs", "Took_Rapido_Link", "Chose_delivery", "Pct", "Sample"], curve)
worry = Counter(d["worry_if_rapido_brings_food"] for d in FD if filled(d, "worry_if_rapido_brings_food"))
nwo = sum(worry.values())
write("s8_fd_worry.csv", ["Worry", "Answers", "Base", "Pct", "Sort"],
      [[k, v, nwo, round(100 * v / nwo, 1), i] for i, (k, v) in enumerate(worry.most_common())])
pct("F7", S9, "Top worry about Rapido bringing food: 'drop a passenger first'", worry["They might drop a passenger first"], nwo,
    "fd_direct", "worry answer / answered")

# how to pay
bl = [d for d in FD if d["bill_id"]]
bc = Counter(d["bill_id"] for d in bl)
lab_b = {"per_order": "Pay Rs15 per order", "protected": "Order Protection (Rs15 + cover)", "membership": "Ownly Plus Rs99/month"}
pay = []
for i, b in enumerate(["per_order", "protected", "membership"]):
    R = [d for d in bl if d["bill_id"] == b]
    pl = sum(1 for d in R if placed(d))
    pay.append([lab_b[b], len(R), len(bl), round(100 * len(R) / len(bl), 1), pl, i])
    pct(f"F8-{b}", S9, f"Chose '{lab_b[b]}'", len(R), len(bl), "fd_direct", "bill_id / chose a payment model")
    pct(f"F8p-{b}", S9, f"Of those choosing '{lab_b[b]}', pressed Place order", pl, len(R), "fd_direct", "placed / chose that model")
write("s8_fd_pay.csv", ["Model", "Chose", "Base", "Pct", "Then_placed", "Sort"], pay)
wp = Counter(d["why_this_way_to_pay"] for d in FD if filled(d, "why_this_way_to_pay"))
write("s8_fd_pay_why.csv", ["Reason", "Answers", "Base"], [[k, v, sum(wp.values())] for k, v in wp.most_common()])
pct("F9", S9, "Top reason behind the payment choice: 'I want a refund if it goes wrong'", wp["I want a refund if it goes wrong"],
    sum(wp.values()), "fd_direct", "why_this_way_to_pay / answered")

# offers: now vs later
of = [d for d in FD if d["offer_id"] in ("flat100", "wallet", "recur10")]
oc = Counter(d["offer_id"] for d in of)
pct("F10", S7, "Picked Ownly Money (Rs120-250 on the NEXT order) over Rs100 off now", oc["wallet"], len(of), "fd_direct",
    "offer_id = wallet / chose one of the three offers")
wo = Counter(d["why_this_offer"] for d in FD if filled(d, "why_this_offer"))
distrust = wo["I may not order here again"] + wo["I don't trust later offers"]
pct("F11", S7, "Reason for the offer: 'may not order here again' or 'don't trust later offers'", distrust, sum(wo.values()),
    "fd_direct", "those two answers / answered")
write("s7_fd_offer_why.csv", ["Reason", "Answers", "Base", "Pct", "Sort"],
      [[k, v, sum(wo.values()), round(100 * v / sum(wo.values()), 1), i] for i, (k, v) in enumerate(wo.most_common())])
arm = Counter(d["variant"] for d in FD)
num("F12", S8, f"A/B arms not comparable: discount {arm['discount']} vs restaurants {arm['restaurants']} sessions", arm["restaurants"], nF,
    "fd_direct", "arm is fixed per phone (localStorage), so shared phones kept one arm - comparison dropped")
bills = [int(d["bill_total"]) for d in FD if placed(d)]
num("F13", S8, "Median basket at Place order (Rs)", statistics.median(bills), len(bills), "fd_direct", "median(bill_total) where placed", " Rs")

# ════════════════════════════════════════════════════════════════════
# 5. REPORTED FIGURES (media, company filings) - not computed, cited
# ════════════════════════════════════════════════════════════════════
REP = [
    ("R1", S1, "Ownly Bengaluru daily orders, Aug 2026", "50,000+ (~10% share)", "Media report", "Storyboard18, 21 Aug 2026"),
    ("R2", S1, "Bengaluru restaurants threatening to quit Swiggy/Zomato, Jul 2026", "1,000+", "Media report", "Business Today, 29 Jul 2026"),
    ("R3", S1, "Restaurants on Ownly in Bengaluru at citywide launch", "~20,000", "Media report", "MediaNama, 5 Mar 2026"),
    ("R4", S1, "Ownly signs MoU with the National Restaurant Association (NRAI)", "Aug 2026", "Media report", "mediabrief / FM Live, Aug 2026"),
    ("R5", S5, "Foodpanda India daily orders after discounts stopped", "~200,000 to ~5,000", "Media report", "01_secondary_research/challenger_failures/A_ubereats_foodpanda.md"),
    ("R6", S5, "Uber Eats India operating loss per order, Q1 2019", "$2.55 on a ~$2.5 order", "Company filing (SEC 8-K)", "Uber Form 8-K Ex. 99.1, 21 Jan 2020"),
    ("R7", S5, "Zomato founder: 'no new use case being unlocked here'", "Quote", "Company filing", "Eternal Q1FY27 shareholders' letter, 22 Jul 2026"),
    ("R8", S5, "Ownly revenue per order vs Swiggy rider payout per order", "Rs30 vs Rs56.01", "Media report / company deck", "C_unit_economics_and_structure.md; Swiggy corporate deck FY24-25"),
    ("R9", S5, "Price-led challengers that failed or shrank (Uber Eats, Foodpanda, Amazon Food, Thrive, DotPe, ONDC buyer apps)", "6 of 6", "Secondary synthesis", "01_secondary_research/challenger_failures/D_synthesis_why_challengers_fail.md"),
]
for r in REP:
    reported(*r)
write("s1_timeline.csv", ["When", "Event", "Who", "Sort"], [
    ["Aug 2025", "Pilot in 3 Bengaluru areas", "Ownly", 0],
    ["Mar 2026", "Citywide launch, ~20,000 restaurants, zero commission", "Ownly", 1],
    ["Jul 2026", "1,000+ restaurants threaten to quit Swiggy/Zomato", "Restaurants", 2],
    ["Jul 2026", "Ownly goes live inside the Rapido app", "Ownly", 3],
    ["Aug 2026", "MoU with NRAI; 50,000+ orders a day", "Ownly", 4],
    ["Sep 2026", "Ownly live in Gachibowli, Hyderabad (no restaurant revolt)", "Ownly", 5],
])

# interviews: qualitative only, count unknown -> no percentages
write("s7_interviews.csv", ["Finding", "Grade"], [
    ["People leave an app after repeated bad orders, not one", "Team-reported, count unknown"],
    ["Speed matters when very hungry; price wins otherwise", "Transcript I-01"],
    ["New apps are tried because a friend or a reel said so", "Team-reported, count unknown"],
    ["'What if they increase prices later'", "Team-reported, count unknown"],
])

# ════════════════════════════════════════════════════════════════════
write("evidence.csv", ["ID", "Screen", "Claim", "Shown_as", "Numerator", "Denominator", "Value", "CI_low", "CI_high",
                       "Sample_check", "Method", "Source_file", "Type"], EVID)
bad = [e for e in EVID if e[9].startswith("Too small")]
print(f"{len(EVID)} evidence rows written; {len(bad)} are too small to show as a percentage:")
for e in bad:
    print("   ", e[0], e[2], e[3])
print("fake door:", nF, "live sessions;", dict(excluded))
