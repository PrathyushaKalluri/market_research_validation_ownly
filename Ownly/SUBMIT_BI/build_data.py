#!/usr/bin/env python3
"""
Ownly Gachibowli — BI data engine.

Reads every canonical source in the project, runs the analytics layers
(descriptive / diagnostic / predictive / prescriptive / text) and emits
`bi_data.js`, a single JavaScript file assigning `window.BI`.

Pure standard library: numpy / pandas / scipy / sklearn are not installed
on this machine, so every statistic below is implemented from scratch.

Run:  python3 build_data.py
"""

import csv, json, math, os, re, sys
from collections import Counter, defaultdict
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "final_dashboard", "data")
MINE = os.path.join(ROOT, "05_review_mining")

def rd(path):
    """Read a CSV into a list of dicts. Returns [] if the file is missing."""
    p = path if os.path.isabs(path) else os.path.join(DATA, path)
    if not os.path.exists(p):
        sys.stderr.write(f"  ! missing: {p}\n")
        return []
    with open(p, encoding="utf-8", errors="replace") as f:
        return list(csv.DictReader(f))

def num(v, default=None):
    try:
        if v is None or str(v).strip() == "": return default
        return float(str(v).replace(",", "").replace("₹", "").strip())
    except Exception:
        return default

def truthy(v):
    return str(v).strip().lower() in ("true", "1", "yes", "y")

# ════════════════════════════════════════════════════════════════════
# STATISTICS — implemented from scratch
# ════════════════════════════════════════════════════════════════════

def wilson(k, n, z=1.959963985):
    """Wilson score interval for a binomial proportion."""
    if n == 0: return (0.0, 0.0, 0.0)
    p = k / n
    d = 1 + z*z/n
    c = (p + z*z/(2*n)) / d
    h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return (round(100*p, 1), round(100*max(0, c-h), 1), round(100*min(1, c+h), 1))

def median(xs):
    s = sorted(xs)
    n = len(s)
    if n == 0: return None
    return s[n//2] if n % 2 else (s[n//2 - 1] + s[n//2]) / 2

def quantile(xs, q):
    s = sorted(xs)
    if not s: return None
    i = (len(s)-1) * q
    lo, hi = int(math.floor(i)), int(math.ceil(i))
    return s[lo] if lo == hi else s[lo] + (s[hi]-s[lo]) * (i-lo)

def boxstats(xs):
    """Five-number summary plus Tukey-fence outliers."""
    s = sorted(xs)
    if not s: return None
    q1, q2, q3 = quantile(s, .25), quantile(s, .5), quantile(s, .75)
    iqr = q3 - q1
    lo_f, hi_f = q1 - 1.5*iqr, q3 + 1.5*iqr
    inl = [x for x in s if lo_f <= x <= hi_f]
    out = [x for x in s if x < lo_f or x > hi_f]
    return {"min": min(inl) if inl else s[0], "q1": q1, "med": q2, "q3": q3,
            "max": max(inl) if inl else s[-1], "outliers": out, "n": len(s)}

def ranks(xs):
    """Average ranks, ties shared."""
    idx = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0]*len(xs)
    i = 0
    while i < len(idx):
        j = i
        while j+1 < len(idx) and xs[idx[j+1]] == xs[idx[i]]: j += 1
        avg = (i + j)/2 + 1
        for k in range(i, j+1): r[idx[k]] = avg
        i = j+1
    return r

def spearman(xs, ys):
    """Spearman rho with a t-approximation p-value."""
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    n = len(pairs)
    if n < 4: return None
    rx, ry = ranks([p[0] for p in pairs]), ranks([p[1] for p in pairs])
    mx, my = sum(rx)/n, sum(ry)/n
    sxy = sum((a-mx)*(b-my) for a, b in zip(rx, ry))
    sxx = sum((a-mx)**2 for a in rx); syy = sum((b-my)**2 for b in ry)
    if sxx == 0 or syy == 0: return None
    rho = sxy/math.sqrt(sxx*syy)
    p = None
    if abs(rho) < 1 and n > 2:
        t = rho*math.sqrt((n-2)/(1-rho*rho))
        p = 2*(1 - _t_cdf(abs(t), n-2))
    return {"rho": round(rho, 3), "n": n, "p": round(p, 4) if p is not None else None}

def _t_cdf(t, df):
    """Student-t CDF via the regularised incomplete beta function."""
    x = df/(df + t*t)
    return 1 - 0.5*_betainc(df/2, 0.5, x)

def _betainc(a, b, x):
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    lbeta = math.lgamma(a) + math.lgamma(b) - math.lgamma(a+b)
    front = math.exp(a*math.log(x) + b*math.log(1-x) - lbeta)
    if x < (a+1)/(a+b+2):
        return front*_betacf(a, b, x)/a
    return 1 - front*_betacf(b, a, 1-x)/b

def _betacf(a, b, x, it=200, eps=1e-12):
    qab, qap, qam = a+b, a+1, a-1
    c, d = 1.0, 1 - qab*x/qap
    if abs(d) < 1e-30: d = 1e-30
    d = 1/d; h = d
    for m in range(1, it+1):
        m2 = 2*m
        aa = m*(b-m)*x/((qam+m2)*(a+m2))
        d = 1 + aa*d; c = 1 + aa/c
        if abs(d) < 1e-30: d = 1e-30
        if abs(c) < 1e-30: c = 1e-30
        d = 1/d; h *= d*c
        aa = -(a+m)*(qab+m)*x/((a+m2)*(qap+m2))
        d = 1 + aa*d; c = 1 + aa/c
        if abs(d) < 1e-30: d = 1e-30
        if abs(c) < 1e-30: c = 1e-30
        d = 1/d; de = d*c; h *= de
        if abs(de-1) < eps: break
    return h

def fisher_exact(a, b, c, d):
    """Two-sided Fisher exact test on a 2x2 table."""
    n = a+b+c+d
    if n == 0: return None
    C = math.comb
    def pr(A):
        B, Cc, D = (a+b)-A, (a+c)-A, d-(a-A)
        if B < 0 or Cc < 0 or D < 0: return 0.0
        return C(a+b, A)*C(c+d, Cc)/C(n, a+c)
    obs = pr(a); tot = 0.0
    for A in range(0, min(a+b, a+c)+1):
        p = pr(A)
        if p <= obs + 1e-12: tot += p
    return round(min(1.0, tot), 4)

def logistic_fit(xs, ys):
    """
    Fit y = 1/(1+exp(-(b0 + b1*x))) to observed proportions by coarse-then-fine
    grid search on SSE. With 6 points a grid beats hand-rolled gradient descent
    for robustness, and it is fully deterministic.
    """
    best = None
    b0_rng = (-8.0, 4.0); b1_rng = (0.0001, 0.5)
    for depth in range(5):
        steps = 60
        s0 = (b0_rng[1]-b0_rng[0])/steps
        s1 = (b1_rng[1]-b1_rng[0])/steps
        for i in range(steps+1):
            b0 = b0_rng[0] + i*s0
            for j in range(steps+1):
                b1 = b1_rng[0] + j*s1
                sse = 0.0
                for x, y in zip(xs, ys):
                    yh = 1/(1+math.exp(-(b0 + b1*x))) if -700 < (b0+b1*x) < 700 else (0.0 if b0+b1*x < 0 else 1.0)
                    sse += (y-yh)**2
                if best is None or sse < best[2]:
                    best = (b0, b1, sse)
        b0_rng = (best[0]-3*s0, best[0]+3*s0)
        b1_rng = (max(1e-6, best[1]-3*s1), best[1]+3*s1)
    b0, b1, sse = best
    ybar = sum(ys)/len(ys)
    sst = sum((y-ybar)**2 for y in ys)
    r2 = 1 - sse/sst if sst > 0 else None
    return {"b0": round(b0, 4), "b1": round(b1, 5), "sse": round(sse, 5),
            "r2": round(r2, 4) if r2 is not None else None}

def logistic_at(fit, x):
    z = fit["b0"] + fit["b1"]*x
    if z < -700: return 0.0
    if z > 700: return 1.0
    return 1/(1+math.exp(-z))

# ════════════════════════════════════════════════════════════════════
# SENTIMENT — domain lexicon, negation-aware
# ════════════════════════════════════════════════════════════════════

POS = {
 "good":1,"great":2,"excellent":2,"amazing":2,"awesome":2,"love":2,"loved":2,"best":2,
 "nice":1,"happy":1.5,"cheap":1,"cheaper":1,"affordable":1.5,"reasonable":1,"fast":1.5,
 "quick":1.5,"quickly":1.5,"fresh":1.5,"hot":1,"tasty":1.5,"delicious":2,"smooth":1.5,
 "easy":1,"helpful":1.5,"support":0.5,"refund":0.5,"genuine":1.5,"transparent":2,
 "honest":1.5,"save":1.5,"saving":1.5,"saved":1.5,"discount":1,"free":1,"zero":0.5,
 "recommend":2,"recommended":2,"better":1.5,"improve":0.5,"improved":1.5,"perfect":2,
 "satisfied":2,"reliable":1.5,"working":1,"works":1,"worth":1.5,"superb":2,"thanks":1,
 "convenient":1.5,"sustainable":1,"support":0.5,"welcome":1,"win":1.5,"benefit":1.5,
}
NEG = {
 "bad":-1.5,"worst":-2.5,"terrible":-2.5,"awful":-2.5,"horrible":-2.5,"pathetic":-2.5,
 "poor":-1.5,"hate":-2,"scam":-2.5,"fraud":-2.5,"cheat":-2.5,"cheating":-2.5,"fake":-2,
 "late":-1.5,"delay":-1.5,"delayed":-1.5,"slow":-1.5,"waiting":-1,"wait":-0.8,
 "cancel":-1.5,"cancelled":-1.8,"cancellation":-1.5,"missing":-2,"wrong":-1.8,
 "cold":-1.5,"stale":-2,"spoiled":-2,"rotten":-2.5,"disgusting":-2.5,
 "expensive":-1.5,"costly":-1.5,"overpriced":-2,"charge":-0.5,"charges":-0.8,"fee":-0.5,
 "fees":-0.8,"hidden":-1.5,"surge":-1,"increase":-0.8,"increased":-1,"rise":-0.8,
 "never":-1,"nothing":-0.8,"nobody":-1,"useless":-2,"waste":-2,"wasted":-2,
 "refuse":-1.5,"refused":-1.5,"complaint":-1.5,"issue":-1,"issues":-1.2,"problem":-1.2,
 "problems":-1.5,"error":-1.2,"bug":-1.2,"crash":-1.5,"stuck":-1.5,"failed":-1.8,
 "fail":-1.5,"unavailable":-1.2,"unprofessional":-2,"rude":-2,"ignore":-1.5,
 "ignored":-1.8,"disappointed":-2,"disappointing":-2,"frustrating":-2,"annoying":-1.5,
 "loss":-1.2,"lose":-1.2,"losing":-1.2,"burn":-1,"unsustainable":-1.5,"doubt":-1,
 "risky":-1.2,"exploit":-2,"exploitation":-2,"underpaid":-2,"struggle":-1.5,
}
NEGATORS = {"not","no","never","dont","don't","doesnt","doesn't","didnt","didn't",
            "cant","can't","wont","won't","isnt","isn't","without","hardly","nor"}
INTENS = {"very":1.5,"really":1.4,"extremely":1.8,"totally":1.5,"absolutely":1.7,
          "completely":1.6,"so":1.3,"too":1.3,"highly":1.4,"super":1.4}

TOKEN = re.compile(r"[a-z']+")

def sentiment(text):
    """Return (score in [-1,1], label). Lexicon + negation + intensifiers."""
    if not text: return 0.0, "neutral"
    toks = TOKEN.findall(text.lower())
    if not toks: return 0.0, "neutral"
    total, hits = 0.0, 0
    for i, t in enumerate(toks):
        w = POS.get(t, 0) or NEG.get(t, 0)
        if w == 0: continue
        mult = 1.0
        for k in (1, 2):
            if i-k >= 0:
                prev = toks[i-k]
                if prev in NEGATORS: mult *= -0.85
                elif prev in INTENS and k == 1: mult *= INTENS[prev]
        total += w*mult; hits += 1
    if hits == 0: return 0.0, "neutral"
    raw = total/math.sqrt(hits)          # dampen long-text accumulation
    score = max(-1.0, min(1.0, raw/3.0))
    label = "positive" if score > 0.12 else ("negative" if score < -0.12 else "neutral")
    return round(score, 3), label

STOP = set("""a an the and or but if then than that this these those is are was were be been being am
of to in on at by for with from as it its it's i you he she they we me my our your their them his her
not no do does did doing done have has had having will would can could should may might must shall
so such very too also just only more most much many other some any each every all both few own same
there here what which who whom when where why how about into over under again further once now then
get got go going one two three s t re ve ll d m ain don didn doesn isn aren wasn weren won t
they're you're we're i'm i've don't can't won't it's he's she's that's there's what's let's
food order orders app apps delivery deliver delivered swiggy zomato ownly rapido rs inr
""".split())

def tfidf_terms(docs, top=14, min_df=2):
    """Top distinctive terms by mean TF-IDF. `docs` is a list of strings."""
    tok_docs = []
    for d in docs:
        ts = [t for t in TOKEN.findall((d or "").lower()) if len(t) > 2 and t not in STOP]
        tok_docs.append(ts)
    N = len(tok_docs)
    if N == 0: return []
    df = Counter()
    for ts in tok_docs: df.update(set(ts))
    scores = defaultdict(float)
    for ts in tok_docs:
        if not ts: continue
        tf = Counter(ts); L = len(ts)
        for t, c in tf.items():
            if df[t] < min_df: continue
            scores[t] += (c/L) * math.log(N/(1+df[t]) + 1)
    out = sorted(scores.items(), key=lambda kv: -kv[1])[:top]
    return [{"term": t, "score": round(s, 4), "df": df[t]} for t, s in out]

def month_of(datestr):
    if not datestr: return None
    s = str(datestr).strip()[:10]
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d"):
        try: return datetime.strptime(s, fmt).strftime("%Y-%m")
        except Exception: pass
    m = re.match(r"^(\d{4})-(\d{2})", s)
    return f"{m.group(1)}-{m.group(2)}" if m else None

# ════════════════════════════════════════════════════════════════════
# LOAD
# ════════════════════════════════════════════════════════════════════
print("Loading sources…")
survey_all = rd("survey_all_rows_with_flags.csv")
clean      = rd("cleaned_survey.csv")
cat        = [r for r in clean if truthy(r.get("in_catchment"))]
audit      = rd("audit_clean.csv")
pairs      = rd("audit_pairs.csv")
platprice  = rd("audit_platform_prices.csv")
coverage   = rd("audit_coverage.csv")
etagap     = rd("eta_gap_by_restaurant.csv")
stair      = rd("switching_staircase.csv")
thresh     = rd("switch_threshold_coverage.csv")
tradeoff   = rd("tradeoff_summary.csv")
tradetests = rd("tradeoff_tests.csv")
segtrade   = rd("segment_tradeoffs.csv")
segcuts    = rd("segment_cuts.csv")
kpi        = rd("kpi_table.csv")
mmet       = rd("marketing_metrics.csv")
notest     = rd("not_estimable.csv")
hyp        = rd("hypothesis_results.csv")
assoc      = rd("associations.csv")
evmat      = rd("evidence_matrix.csv")
blr        = rd("bengaluru_benchmark.csv")
stars      = rd("review_star_distribution.csv")
revtheme   = rd("review_theme_summary.csv")
yttheme    = rd("youtube_theme_summary.csv")
ytraw      = rd("youtube_comments_coded.csv")
anomalies  = rd("anomalies.csv")
funnel_res = rd("research_funnel.csv")
appstore   = rd(os.path.join(MINE, "app_stores", "reviews_coded.csv"))
social     = rd(os.path.join(MINE, "social", "social_coded.csv"))

print(f"  survey all={len(survey_all)} clean={len(clean)} catchment={len(cat)}")
print(f"  audit captures={len(audit)} pairs={len(pairs)}")
print(f"  text: social={len(social)} youtube={len(ytraw)} appstore={len(appstore)}")

BI = {}

# ════════════════════════════════════════════════════════════════════
# 0 · META
# ════════════════════════════════════════════════════════════════════
BI["meta"] = {
    "built": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "n_catchment": len(cat),
    "n_clean": len(clean),
    "n_received": len(survey_all),
    "n_audit_captures": len(audit),
    "n_text": len(social) + len(ytraw) + len(appstore),
    "audit_slot": "wed_dinner, DP1 Gachibowli, 2026-09-16",
}

# ════════════════════════════════════════════════════════════════════
# 1 · RESPONDENT-LEVEL TABLE  (drives all cross-filtering in the UI)
# ════════════════════════════════════════════════════════════════════
def seg_occ(r):
    o = (r.get("occupation") or "").strip()
    if o.startswith("Student"): return "Student"
    if o.startswith("Working"): return "Working professional"
    return "Other"

rows = []
for r in cat:
    rows.append({
        "id": r.get("resp_id"),
        "occ": seg_occ(r),
        "member": truthy(r.get("has_membership")),
        "n_mem": int(num(r.get("n_memberships"), 0) or 0),
        "multi": truthy(r.get("multihoming")),
        "rapido": (r.get("rapido_freq") or "").strip() not in ("", "Never"),
        "rapido_seen": (r.get("rapido_food_seen") or "").strip(),
        "aware": truthy(r.get("ownly_aware")),
        "opened": truthy(r.get("ownly_opened")),
        "ordered": truthy(r.get("ownly_says_ordered")),
        "eta_cheap": truthy(r.get("eta_chose_cheap")),
        "rel_cheap": truthy(r.get("rel_chose_cheap")),
        "rest_cheap": truthy(r.get("rest_chose_cheap")),
        "switch_rs": num(r.get("switch_savings_rs")),
        "switch_never": truthy(r.get("switch_never")),
        "switch_dk": truthy(r.get("switch_dk")),
        "orders_4wk": num(r.get("total_orders_4wk")),
        "n_swiggy": num(r.get("n_swiggy"), 0),
        "n_zomato": num(r.get("n_zomato"), 0),
        "n_ownly": num(r.get("n_ownly"), 0),
        "n_other": num(r.get("n_other"), 0),
        "last_amount": num(r.get("last_amount")),
        "amount_pp": num(r.get("amount_pp")),
        "repeat_n": num(r.get("repeat_no_promo_n")),
        "doubt_n": num(r.get("durability_doubt_n")),
        "P_int": num(r.get("prop_P_intent_n")),
        "Q_int": num(r.get("prop_Q_intent_n")),
        "bill_fair": (r.get("bill_fairness") or "").strip(),
        "gachi": truthy(r.get("is_gachibowli_proper")),
    })
BI["rows"] = rows

# ════════════════════════════════════════════════════════════════════
# 2 · DESCRIPTIVE
# ════════════════════════════════════════════════════════════════════
BI["kpis"] = [
    {k: r.get(k) for k in ("kpi_id","kpi_name","layer","driver","status","value","unit",
                           "numerator","denominator","base","formula","data_source",
                           "evidence_type","evidence_strength","limitation","ci_lo","ci_hi",
                           "family","is_headline")}
    for r in kpi
]
BI["funnel_research"] = [{"stage": r["stage"], "n": int(num(r["n"], 0))} for r in funnel_res]

BI["adoption_funnel"] = [
    {"stage": "Heard of Ownly", "k": sum(1 for r in rows if r["aware"]), "n": len(rows)},
    {"stage": "Opened / browsed", "k": sum(1 for r in rows if r["opened"]), "n": len(rows)},
    {"stage": "Ordered", "k": sum(1 for r in rows if r["ordered"]), "n": len(rows)},
]
for s in BI["adoption_funnel"]:
    s["pct"], s["lo"], s["hi"] = wilson(s["k"], s["n"])

BI["tradeoffs"] = [
    {"dim": r["dimension"], "label": r["description"],
     "k": int(num(r["chose_cheaper_k"], 0)), "n": int(num(r["n"], 0)),
     "pct": num(r["chose_cheaper_pct"]), "lo": num(r["ci_lo"]), "hi": num(r["ci_hi"]),
     "premium": num(r["paid_premium_pct"])}
    for r in tradeoff
]
BI["tradeoff_tests"] = [
    {"cmp": r["comparison"], "n": int(num(r["n"],0)), "b": int(num(r["b"],0)),
     "c": int(num(r["c"],0)), "p": num(r["p_value"]), "test": r["test"]}
    for r in tradetests
]
BI["segment_cuts"] = segcuts
BI["segment_tradeoffs"] = [
    {"dim": r["dimension"], "seg": r["segment"], "k": int(num(r["k"],0)), "n": int(num(r["n"],0)),
     "pct": num(r["chose_cheaper_pct"]), "lo": num(r["ci_lo"]), "hi": num(r["ci_hi"]),
     "p": num(r["fisher_p"])}
    for r in segtrade
]

# platform order share within the sample
plat = {"Swiggy": 0.0, "Zomato": 0.0, "Ownly": 0.0, "Other": 0.0}
for r in rows:
    plat["Swiggy"] += r["n_swiggy"] or 0; plat["Zomato"] += r["n_zomato"] or 0
    plat["Ownly"]  += r["n_ownly"]  or 0; plat["Other"]  += r["n_other"]  or 0
tot = sum(plat.values()) or 1
BI["platform_share"] = [{"platform": k, "orders": v, "pct": round(100*v/tot, 1)}
                        for k, v in sorted(plat.items(), key=lambda kv: -kv[1])]

# distributions for histogram / box plot
amts = [r["last_amount"] for r in rows if r["last_amount"]]
ords_ = [r["orders_4wk"] for r in rows if r["orders_4wk"] is not None]
BI["dist"] = {
    "last_amount": {"values": amts, "box": boxstats(amts)},
    "orders_4wk": {"values": ords_, "box": boxstats(ords_)},
    "switch_rs": {"values": [r["switch_rs"] for r in rows if r["switch_rs"] is not None],
                  "box": boxstats([r["switch_rs"] for r in rows if r["switch_rs"] is not None])},
}
BI["stars"] = [{"star": int(num(r["star_rating"],0)), "n": int(num(r["n"],0))} for r in stars]

# ════════════════════════════════════════════════════════════════════
# 3 · DIAGNOSTIC — price erosion, audit, correlations
# ════════════════════════════════════════════════════════════════════
BI["erosion"] = [
    {"view": r["view"], "clearing": int(num(r["pairs_clearing"],0)),
     "total": int(num(r["pairs_total"],0)), "pct": num(r["coverage_pct"]),
     "median_saving": num(r["median_saving_rs"])}
    for r in thresh
]
BI["pairs"] = [
    {"restaurant": r["restaurant_display"], "view": r["view"],
     "ownly": num(r["ownly_payable"]), "rival": num(r["incumbent_payable"]),
     "rival_name": r["cheapest_incumbent"], "saving": num(r["saving_rs"]),
     "saving_pct": num(r["saving_pct"]), "wins": truthy(r["ownly_wins"]),
     "ownly_eta": num(r["ownly_eta_mid"]), "rival_eta": num(r["incumbent_eta_mid"])}
    for r in pairs
]
BI["coverage"] = coverage
BI["eta_gap"] = [{"restaurant": r["restaurant_display"], "ownly": num(r["ownly"]),
                  "swiggy": num(r["swiggy"]), "zomato": num(r["zomato"]),
                  "best": num(r["best_incumbent"]), "gap": num(r["gap"])} for r in etagap]

# fee-load decomposition by platform (zero-discount captures only)
fee = defaultdict(lambda: defaultdict(list))
for a in audit:
    if a.get("priced") != "True": continue
    if num(a.get("discount_amount"), 0) not in (0, 0.0): continue
    p = a.get("platform")
    fp = num(a.get("final_payable"))
    if not fp: continue
    for comp, key in [("menu_subtotal","Food"),("delivery_fee","Delivery"),
                      ("platform_fee","Platform"),("packaging_fee","Packaging"),
                      ("small_cart_fee","Small cart"),("surge_rain_fee","Surge"),
                      ("taxes_gst","GST")]:
        fee[p][key].append(100*(num(a.get(comp), 0) or 0)/fp)
BI["fee_decomp"] = [
    {"platform": p, "parts": [{"part": k, "pct": round(median(v) or 0, 1)} for k, v in comps.items()]}
    for p, comps in fee.items()
]

# correlation matrix (Spearman) over the modelling variables
corr_vars = [
    ("switch_rs", "Saving required (₹)"),
    ("orders_4wk", "Orders / 4wk"),
    ("n_mem", "Memberships held"),
    ("last_amount", "Last bill (₹)"),
    ("repeat_n", "Post-offer repeat intent"),
    ("doubt_n", "Price-durability doubt"),
    ("P_int", "Proposition P intent"),
    ("Q_int", "Proposition Q intent"),
]
cm = []
for i, (ka, la) in enumerate(corr_vars):
    for j, (kb, lb) in enumerate(corr_vars):
        if j < i: continue
        xs = [r[ka] for r in rows]; ys = [r[kb] for r in rows]
        sp = spearman(xs, ys) if ka != kb else {"rho": 1.0, "n": len(rows), "p": 0.0}
        if sp:
            cm.append({"a": la, "b": lb, "rho": sp["rho"], "p": sp["p"], "n": sp["n"]})
BI["corr"] = {"vars": [l for _, l in corr_vars], "cells": cm}
BI["associations"] = [
    {"q": r["question"], "n": int(num(r["n"],0)), "rho": num(r["rho"]),
     "p": num(r["p_value"]), "lo": num(r["ci_lo"]), "hi": num(r["ci_hi"]), "verdict": r["verdict"]}
    for r in assoc
]
BI["evidence_matrix"] = evmat
BI["hypotheses"] = hyp
BI["anomalies"] = anomalies

# ════════════════════════════════════════════════════════════════════
# 4 · PREDICTIVE (a) — price-response / adoption curve
# ════════════════════════════════════════════════════════════════════
sx = [num(r["level_rs"]) for r in stair]
sy = [num(r["pct_of_named"])/100.0 for r in stair]
fit = logistic_fit(sx, sy)
curve = [{"x": x, "y": round(100*logistic_at(fit, x), 1)} for x in range(0, 201, 2)]
obs_savings = {e["view"]: e["median_saving"] for e in BI["erosion"]}
BI["demand_curve"] = {
    "fit": fit,
    "observed": [{"x": x, "y": round(100*y, 1)} for x, y in zip(sx, sy)],
    "curve": curve,
    "n_named": int(num(stair[0]["n_named"], 0)) if stair else 0,
    "excluded_never": int(num(stair[0]["excluded_no_amount"], 0)) if stair else 0,
    "excluded_dk": int(num(stair[0]["excluded_dont_know"], 0)) if stair else 0,
    "max_observed_x": max(sx) if sx else None,
    "extrapolation_warning": "The staircase was measured at \u20b910\u2013\u20b9100. Anything the curve says above \u20b9100 is extrapolation from a fitted function, not observation, and is drawn dashed.",
    "markers": [
        {"label": v, "x": s, "y": round(100*logistic_at(fit, s), 1)}
        for v, s in obs_savings.items() if s is not None and s > 0
    ],
}

# ════════════════════════════════════════════════════════════════════
# 5 · PREDICTIVE (b) — switcher profiling  [EXPLORATORY, n=40]
# ════════════════════════════════════════════════════════════════════
def lift_table(target_key, target_name):
    base_k = sum(1 for r in rows if r[target_key])
    base = base_k/len(rows) if rows else 0
    feats = [
        ("Holds a membership", lambda r: r["member"]),
        ("No membership", lambda r: not r["member"]),
        ("Multi-homes (2+ apps)", lambda r: r["multi"]),
        ("Single-app user", lambda r: not r["multi"]),
        ("Student", lambda r: r["occ"] == "Student"),
        ("Working professional", lambda r: r["occ"] == "Working professional"),
        ("Uses Rapido", lambda r: r["rapido"]),
        ("Aware of Ownly", lambda r: r["aware"]),
        ("Low switch bar (≤₹30)", lambda r: r["switch_rs"] is not None and r["switch_rs"] <= 30),
        ("High switch bar (>₹30)", lambda r: r["switch_rs"] is not None and r["switch_rs"] > 30),
        ("Orders 5+ / 4wk", lambda r: (r["orders_4wk"] or 0) >= 5),
        ("Doubts price durability", lambda r: (r["doubt_n"] or 0) >= 4),
    ]
    out = []
    for name, fn in feats:
        sub = [r for r in rows if fn(r)]
        if len(sub) < 3: continue
        k = sum(1 for r in sub if r[target_key])
        p, lo, hi = wilson(k, len(sub))
        out.append({"feature": name, "k": k, "n": len(sub), "pct": p, "lo": lo, "hi": hi,
                    "lift": round((p/100)/base, 2) if base > 0 else None})
    return {"target": target_name, "base_pct": round(100*base, 1),
            "base_k": base_k, "base_n": len(rows),
            "rows": sorted(out, key=lambda d: -(d["lift"] or 0))}

BI["profiling"] = {
    "note": "EXPLORATORY ONLY. n=40 — subgroup cells are small and every interval is wide. "
            "Lift = subgroup rate ÷ overall rate. Not a fitted classifier; no out-of-sample validation.",
    "targets": [
        lift_table("rest_cheap", "Will give up usual restaurants for ₹30"),
        lift_table("aware", "Aware of Ownly"),
    ],
}

# Fisher tests on the strongest contrasts
prof_tests = []
for tk, tn in [("rest_cheap","Trades restaurants"), ("eta_cheap","Trades speed"), ("aware","Aware")]:
    for fname, fn in [("Membership", lambda r: r["member"]),
                      ("Student", lambda r: r["occ"] == "Student"),
                      ("Multi-homes", lambda r: r["multi"])]:
        a = sum(1 for r in rows if fn(r) and r[tk]); b = sum(1 for r in rows if fn(r) and not r[tk])
        c = sum(1 for r in rows if not fn(r) and r[tk]); d = sum(1 for r in rows if not fn(r) and not r[tk])
        if min(a+b, c+d) < 3: continue
        prof_tests.append({"target": tn, "feature": fname, "a": a, "b": b, "c": c, "d": d,
                           "p": fisher_exact(a, b, c, d)})
BI["profiling"]["tests"] = prof_tests

# ════════════════════════════════════════════════════════════════════
# 6 · TEXT ANALYTICS — sentiment, topics, trend
# ════════════════════════════════════════════════════════════════════
def social_eng(v):
    """Social engagement is mostly the literal string 'not exposed by RSS'.
    Parse a leading integer where one exists; otherwise the value is UNAVAILABLE."""
    m = re.match(r"^\s*(\d+)", str(v or ""))
    return float(m.group(1)) if m else None

docs = []
for r in social:
    s, lab = sentiment(r.get("text_excerpt"))
    docs.append({"src": "Social", "platform": r.get("platform") or "social",
                 "date": month_of(r.get("post_date")), "text": r.get("text_excerpt") or "",
                 "themes": [t.strip() for t in (r.get("themes") or "").split(";") if t.strip()],
                 "eng": social_eng(r.get("engagement")), "score": s, "label": lab, "star": None})
for r in ytraw:
    s, lab = sentiment(r.get("text"))
    docs.append({"src": "YouTube", "platform": "youtube",
                 "date": month_of(r.get("published")), "text": r.get("text") or "",
                 "themes": [t.strip() for t in (r.get("themes") or "").split(";") if t.strip()],
                 "eng": num(r.get("likes"), 0) or 0, "score": s, "label": lab, "star": None})
for r in appstore:
    s, lab = sentiment(r.get("review_text"))
    st = num(r.get("star_rating"))
    docs.append({"src": "App store", "platform": r.get("platform_source") or "appstore",
                 "date": month_of(r.get("review_date")), "text": r.get("review_text") or "",
                 "themes": [], "eng": num(r.get("thumbs_up_count"), 0) or 0,
                 "score": s, "label": lab, "star": st})

BI["text_meta"] = {"n": len(docs),
                   "by_source": dict(Counter(d["src"] for d in docs))}

# sentiment distribution, by source
sent_by_src = []
for src in ("Social", "YouTube", "App store"):
    sub = [d for d in docs if d["src"] == src]
    if not sub: continue
    c = Counter(d["label"] for d in sub)
    sent_by_src.append({"src": src, "n": len(sub),
                        "positive": c["positive"], "neutral": c["neutral"], "negative": c["negative"],
                        "mean": round(sum(d["score"] for d in sub)/len(sub), 3)})
BI["sentiment_by_source"] = sent_by_src
BI["sentiment_hist"] = [
    {"bin": round(b/10, 1),
     "n": sum(1 for d in docs if b/10 <= d["score"] < (b+1)/10 or (b == 10 and d["score"] == 1.0))}
    for b in range(-10, 11)
]

# sentiment + volume over time
by_month = defaultdict(list)
for d in docs:
    if d["date"]: by_month[d["date"]].append(d)
months = sorted(by_month)
BI["text_trend"] = [
    {"month": m, "n": len(by_month[m]),
     "mean": round(sum(x["score"] for x in by_month[m])/len(by_month[m]), 3),
     "pos": sum(1 for x in by_month[m] if x["label"] == "positive"),
     "neu": sum(1 for x in by_month[m] if x["label"] == "neutral"),
     "neg": sum(1 for x in by_month[m] if x["label"] == "negative"),
     "eng": sum(x["eng"] for x in by_month[m] if x["eng"] is not None)}
    for m in months
]

# Engagement is only published by YouTube. Social exposes "not exposed by RSS"
# for 471 of 524 items, so any engagement-weighted view is YouTube-only and says so.
eng_docs = [d for d in docs if d["eng"] is not None]
BI["engagement_note"] = {
    "available_n": len(eng_docs),
    "total_n": len(docs),
    "by_source": dict(Counter(d["src"] for d in eng_docs)),
    "warning": "Engagement (likes/reactions) is published by YouTube and a handful of social posts only. "
               "471 of 524 social items return 'not exposed by RSS'. Engagement-weighted views are "
               "therefore YouTube-dominated and are labelled as such — they are NOT a full-corpus measure.",
}

# Roll the 119 granular sub-codes up into families for the treemap, keeping the raw
# code on every document for drill-down. Ordered keyword rules rather than an
# enumerated lookup, so new codes in a later coding pass still land somewhere sensible.
FAMILY_RULES = [
    ("Support & refunds",      ("SUPPORT", "REFUND", "COMPLAINT", "ESCALAT")),
    ("Fulfilment failure",     ("NON_DELIVERY", "LATE", "MISSING", "WRONG_ITEM", "CANCELL",
                                "CANCEL", "SPOIL", "COLD_FOOD", "QUALITY_ISSUE", "RIDER_CONDUCT")),
    ("Rider economics",        ("RIDER_ECON", "RIDER_EARN", "RIDER_PAY", "GIG_", "DELIVERY_PARTNER")),
    ("Trust & credibility",    ("TRUST", "SCAM", "ASTROTURF", "FAKE", "SHILL", "DISTRUST")),
    ("Price — doubt",          ("FEE_CREEP", "INFLATION", "SKEPTIC", "CONVERGENCE", "PRICE_DOUBT",
                                "SUSTAINABILITY", "UNSUSTAIN", "BURN", "EARLY_LAUNCH_TRUST")),
    ("Price — advantage",      ("PRICE", "FEE", "CHEAP", "SAVING", "COMMISSION", "BILL",
                                "MARKUP", "DISCOUNT", "OFFER", "COST")),
    ("Assortment & coverage",  ("ASSORTMENT", "RESTAURANT", "MENU", "SERVICE_AREA", "CITY_",
                                "AVAILAB", "COVERAGE", "OUTLET")),
    ("Competitive framing",    ("COMPETIT", "INCUMBENT", "TOING", "SWIGGY", "ZOMATO",
                                "AGGREGATOR", "RIVAL", "MULTI_HOMING", "LOYALTY")),
    ("Regulation & policy",    ("REGULAT", "ONDC", "POLICY", "GOVT", "LAW", "TAX")),
    ("App & payments",         ("APP_UX", "UX", "GLITCH", "CRASH", "PAYMENT", "COD", "CASH", "LOGIN")),
    ("Speed & ETA",            ("SPEED", "ETA", "FAST", "SLOW_DELIVERY")),
    ("Distribution & ecosystem",("RAPIDO", "ECOSYSTEM", "DISINTERMEDIATION", "DISTRIBUTION",
                                "DIRECT_ORDER")),
    ("Buzz & advocacy",        ("LAUNCH", "SLOGAN", "RELAY", "CURIOSITY", "WORD_OF_MOUTH",
                                "WELCOME", "GENERAL_SUPPORT", "ADVOCA", "TRIAL_")),
]
def fam(t):
    u = (t or "").upper()
    for name, keys in FAMILY_RULES:
        if any(k in u for k in keys): return name
    return "Other"

# themes: volume, engagement, sentiment  (treemap + bubble)
theme_agg = defaultdict(lambda: {"n": 0, "eng": 0.0, "eng_n": 0, "scores": []})
for d in docs:
    for t in d["themes"]:
        a = theme_agg[t]; a["n"] += 1; a["scores"].append(d["score"])
        if d["eng"] is not None: a["eng"] += d["eng"]; a["eng_n"] += 1
BI["themes"] = sorted([
    {"theme": t.replace("_", " ").title(), "raw": t, "family": fam(t), "n": a["n"],
     "eng": round(a["eng"]), "eng_n": a["eng_n"],
     "sentiment": round(sum(a["scores"])/len(a["scores"]), 3) if a["scores"] else 0,
     "eng_per": round(a["eng"]/a["eng_n"], 1) if a["eng_n"] else None}
    for t, a in theme_agg.items() if a["n"] >= 2
], key=lambda d: -d["n"])

# family roll-up (what the treemap actually shows)
fam_agg = defaultdict(lambda: {"n": 0, "scores": []})
for d in docs:
    for t in set(fam(x) for x in d["themes"]):
        fam_agg[t]["n"] += 1
    for x in d["themes"]:
        fam_agg[fam(x)]["scores"].append(d["score"])
BI["theme_families"] = sorted([
    {"family": k, "n": v["n"],
     "sentiment": round(sum(v["scores"])/len(v["scores"]), 3) if v["scores"] else 0}
    for k, v in fam_agg.items()], key=lambda d: -d["n"])

# theme co-occurrence (network / heatmap)
co = Counter()
for d in docs:
    ts = sorted(set(d["themes"]))
    for i in range(len(ts)):
        for j in range(i+1, len(ts)):
            co[(ts[i], ts[j])] += 1
BI["cooccur"] = [{"a": a.replace("_"," ").title(), "b": b.replace("_"," ").title(), "n": n}
                 for (a, b), n in co.most_common(28)]

# topic modelling (light): distinctive terms overall and per top theme
BI["terms_overall"] = tfidf_terms([d["text"] for d in docs], top=20, min_df=3)
BI["terms_by_theme"] = []
for th in BI["themes"][:8]:
    sub = [d["text"] for d in docs if th["raw"] in d["themes"]]
    if len(sub) >= 4:
        BI["terms_by_theme"].append({"theme": th["theme"], "n": len(sub),
                                     "terms": tfidf_terms(sub, top=10, min_df=2)})

# sentiment vs star (validation of the lexicon against a labelled signal)
sv = [d for d in docs if d["star"] is not None]
BI["sentiment_vs_star"] = {
    "points": [{"star": d["star"], "score": d["score"]} for d in sv],
    "by_star": [
        {"star": s,
         "n": sum(1 for d in sv if d["star"] == s),
         "mean": round(sum(d["score"] for d in sv if d["star"] == s) /
                       max(1, sum(1 for d in sv if d["star"] == s)), 3)}
        for s in (1, 2, 3, 4, 5) if any(d["star"] == s for d in sv)
    ],
    "spearman": spearman([d["star"] for d in sv], [d["score"] for d in sv]),
}
BI["review_themes"] = revtheme
BI["youtube_themes"] = yttheme

# most engaged verbatims, for the drill-down panel
BI["verbatims"] = sorted(
    [{"src": d["src"], "date": d["date"], "eng": d["eng"], "score": d["score"],
      "label": d["label"], "star": d["star"],
      "text": (d["text"][:260] + "…") if len(d["text"]) > 260 else d["text"],
      "themes": [t.replace("_"," ").title() for t in d["themes"]]}
     for d in docs if len(d["text"]) > 40],
    key=lambda d: -(d["eng"] or 0))[:60]

# ════════════════════════════════════════════════════════════════════
# 7 · COMPETITIVE / BENCHMARK
# ════════════════════════════════════════════════════════════════════
BI["blr_vs_hyd"] = blr
BI["marketing_metrics"] = mmet
BI["not_estimable"] = notest
BI["market_context"] = rd("market_context.csv")

# ════════════════════════════════════════════════════════════════════
# 8 · PRESCRIPTIVE — unit economics benchmarks + scenario defaults
# Every constant below is FACT-grade and domain-wide. Sources recorded.
# ════════════════════════════════════════════════════════════════════
BI["econ_benchmarks"] = [
    {"metric": "Rider payout per order", "value": 56.01, "unit": "₹",
     "grade": "FACT", "entity": "Swiggy FY24",
     "series": "₹59.23 (FY22) → ₹58.99 (FY23) → ₹56.01 (FY24)",
     "source": "Swiggy Corporate Deck FY24-25",
     "why_domain_wide": "What a delivery partner is paid per order. Ownly uses the same rider pool as Rapido and competes for the same labour, so this is the floor on its variable cost."},
    {"metric": "Food-delivery AOV", "value": 458.0, "unit": "₹",
     "grade": "FACT", "entity": "Swiggy FY25",
     "series": "₹407 (FY22) → ₹416 (FY23) → ₹428 (FY24) → ₹458 (FY25)",
     "source": "Swiggy Corporate Deck FY24-25",
     "why_domain_wide": "Industry basket size. Our own Gachibowli audit observed a much smaller median Ownly basket — the gap is itself a finding."},
    {"metric": "A&SP per order (CAC proxy)", "value": 33.20, "unit": "₹",
     "grade": "CALCULATED", "entity": "Zomato FY20",
     "series": "₹26.51 (FY18) → ₹64.71 (FY19) → ₹33.20 (FY20)",
     "source": "Zomato DRHP, advertising & sales promotion ÷ orders",
     "why_domain_wide": "No credible public CAC exists for Indian food delivery — neither DRHP discloses it. A&SP per order is the defensible proxy named in our own secondary research."},
    {"metric": "Steady-state margin ceiling", "value": 5.5, "unit": "% of NOV",
     "grade": "FACT", "entity": "Eternal guidance 5–6%; Swiggy 5% of GOV",
     "series": "Actuals: Eternal 5.6%, Swiggy 3.1% (Q1FY27)",
     "source": "Eternal & Swiggy shareholder letters",
     "why_domain_wide": "Both incumbents guide to the same ceiling. It is the realistic best case for any player in this category, challenger included."},
    {"metric": "Years to EBITDA break-even", "value": 16, "unit": "years",
     "grade": "FACT", "entity": "Eternal (Zomato)",
     "series": "16 years to adjusted-EBITDA break-even; 18 to $10bn NOV",
     "source": "Eternal disclosures",
     "why_domain_wide": "The category's demonstrated time-to-profit, by the only Indian player that has got there."},
    {"metric": "Ownly revenue per order", "value": 30.0, "unit": "₹",
     "grade": "MEDIA — CONTESTED", "entity": "Ownly, Bengaluru launch",
     "series": "Reported variously as 8–15% commission, zero + subscription, or zero + ₹30 flat fee",
     "source": "MediaNama, 5 Mar 2026",
     "why_domain_wide": "NOT domain-wide — Ownly-specific and contested. Our own Gachibowli audit observed ₹0 charged to the customer. Used only as the optimistic bound in the simulator."},
    {"metric": "Uber Eats India loss per order", "value": -2.55, "unit": "$",
     "grade": "DERIVED from SEC filings", "entity": "Uber Eats India, Q1 2019",
     "series": "Operating loss $2.55/order against AOV $2.45",
     "source": "Uber SEC filings",
     "why_domain_wide": "The cautionary benchmark: a challenger losing more than 100% of gross bookings per order."},
]

audit_aov = median([p["ownly"] for p in BI["pairs"] if p["view"] == "LIST+FEES" and p["ownly"]])
BI["econ_defaults"] = {
    "aov": round(audit_aov or 196, 0),
    "aov_industry": 458,
    "rev_per_order": 30,
    "rider_cost": 56.01,
    "cac": 33.20,
    "margin_ceiling_pct": 5.5,
    "catchment_pop": 149264,
    "target_share_pct": 5,
    "orders_per_user_month": 4,
    "note": "AOV defaults to the median Ownly basket observed in our own Gachibowli audit, not the industry figure. Every other default is the FACT-grade benchmark listed above.",
}

# prescriptive: lever sensitivity (tornado)
def scenario(saving, coverage_pct, discovery_pct, rev, rider, cac, pop, share, opm):
    """Simplified funnel → contribution model. Deterministic, fully transparent."""
    adopt = logistic_at(fit, saving)                       # willing at this saving
    reach = (discovery_pct/100.0)                          # of those, reached
    fitpct = (coverage_pct/100.0)                          # assortment acceptable
    users  = pop * (share/100.0) * adopt * reach * fitpct
    orders = users * opm
    contrib_per = rev - rider
    return {"adopt": round(100*adopt,1), "users": round(users),
            "orders": round(orders), "contrib_per": round(contrib_per,2),
            "monthly_contrib": round(orders*contrib_per),
            "cac_total": round(users*cac),
            "payback_months": round((cac/contrib_per)/max(opm,0.01),1) if contrib_per > 0 else None}

d = BI["econ_defaults"]
base_args = dict(saving=114.5, coverage_pct=35.0, discovery_pct=15.2,
                 rev=d["rev_per_order"], rider=d["rider_cost"], cac=d["cac"],
                 pop=d["catchment_pop"], share=d["target_share_pct"],
                 opm=d["orders_per_user_month"])
BI["scenario_base"] = scenario(**base_args)
tornado = []
for key, lo, hi, label in [
    ("saving", 30, 150, "Recurring saving held (₹)"),
    ("coverage_pct", 20, 80, "Usual-restaurant coverage (%)"),
    ("discovery_pct", 10, 60, "Discovery rate (%)"),
    ("rev", 0, 45, "Revenue per order (₹)"),
    ("rider", 40, 70, "Rider cost per order (₹)"),
]:
    a = dict(base_args); a[key] = lo; low = scenario(**a)["monthly_contrib"]
    a = dict(base_args); a[key] = hi; high = scenario(**a)["monthly_contrib"]
    tornado.append({"lever": label, "low": low, "high": high,
                    "swing": abs(high-low), "lo_val": lo, "hi_val": hi})
BI["tornado"] = sorted(tornado, key=lambda t: -t["swing"])

# ── Break-even: the single most consequential number in the model ──
rev, rider, cac = d["rev_per_order"], d["rider_cost"], d["cac"]
contrib = rev - rider
BI["breakeven"] = {
    "rev_per_order": rev,
    "rider_cost": rider,
    "contrib_per_order": round(contrib, 2),
    "breakeven_rev": round(rider, 2),
    "uplift_needed_pct": round(100*(rider-rev)/rev, 1) if rev else None,
    "sign": "negative" if contrib < 0 else "positive",
    "headline": (
        "At the only revenue figure ever reported for Ownly (₹30 per order) and the industry's "
        "disclosed rider payout (₹56.01), every order destroys ₹26.01 of contribution before a "
        "single rupee of marketing, support or overhead. Revenue per order must rise ~87% simply "
        "to reach zero."),
    "consequence": (
        "While contribution per order is negative, growth makes losses larger, not smaller. "
        "Every volume lever in the simulator — discovery, coverage, saving held — moves monthly "
        "contribution DOWN. Only the revenue and cost levers can change the sign. This is the "
        "mechanism that ended Uber Eats India, which lost $2.55 per order on a $2.45 order."),
    "caveats": [
        "Ownly's ₹30 revenue per order is MEDIA-reported and contested across three outlets "
        "(8–15% commission vs zero+subscription vs zero+₹30 fee). Our own Gachibowli audit observed "
        "₹0 charged to the customer, which would make contribution worse, not better.",
        "₹56.01 is Swiggy's FY24 disclosed rider payout, used as a domain-wide proxy. Ownly's own "
        "delivery cost is not disclosed by anyone. If Rapido's amortised fleet genuinely lowers it, "
        "the gap narrows — but no public figure supports or refutes that.",
        "This is a contribution model, not a P&L. Fixed costs, technology, support and overhead are "
        "excluded entirely, so true break-even is strictly worse than shown.",
    ],
}

# Sensitivity of contribution per order to the two levers that can change its sign
BI["breakeven_grid"] = [
    {"rev": r,
     "contrib": round(r - rider, 2),
     "contrib_at_45": round(r - 45, 2),
     "contrib_at_65": round(r - 65, 2)}
    for r in range(0, 91, 5)
]

# ════════════════════════════════════════════════════════════════════
# WRITE
# ════════════════════════════════════════════════════════════════════
out = os.path.join(HERE, "bi_data.js")
with open(out, "w", encoding="utf-8") as f:
    f.write("/* Generated by build_data.py — do not edit by hand. */\n")
    f.write("window.BI = ")
    json.dump(BI, f, ensure_ascii=False, separators=(",", ":"), default=str)
    f.write(";\n")

size = os.path.getsize(out)/1024
print(f"\nWrote {out}  ({size:.0f} KB)")
print(f"  respondents      : {len(BI['rows'])}")
print(f"  text documents   : {BI['text_meta']['n']}  {BI['text_meta']['by_source']}")
print(f"  months of text   : {len(BI['text_trend'])}  ({months[0] if months else '-'} → {months[-1] if months else '-'})")
print(f"  demand curve fit : b0={fit['b0']} b1={fit['b1']} R²={fit['r2']}")
print(f"  themes           : {len(BI['themes'])}   co-occurrence pairs: {len(BI['cooccur'])}")
print(f"  sentiment×star ρ : {BI['sentiment_vs_star']['spearman']}")
