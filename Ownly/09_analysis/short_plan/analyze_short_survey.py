#!/usr/bin/env python3
"""Analyse the SHORT 7-minute Hyderabad survey (Google Forms CSV export).

Standard library only.

Usage:
    python3 analyze_short_survey.py path/to/export.csv [--out OUTDIR]

Outputs (OUTDIR, default ./short_survey_outputs/):
    sample_flow.csv, cleaned.csv, excluded.csv, kpis.csv, report.md

Rules follow 08_clean_data/cleaning_protocol.md and 00_research_charter/P_3day_plan_ethics_budget_kpis.md §5.
Every estimate is reported with n and a Wilson 95% CI. Nothing is invented: if a column is missing, the KPI is
reported as NOT AVAILABLE.
"""
import csv, math, os, re, sys, statistics as st
from collections import Counter

# ---------- column mapping: distinctive header substrings -> variable ----------
HEADERS = {
    "meta_consent": "agree to take part",
    "scr_age_band": "How old are you",
    "scr_area": "live, study or work in on most days",
    "scr_orders_4wk": "how many times did you order food for delivery",
    "seg_occupation_raw": "best describes you right now",
    "dem_living": "currently live",
    "beh_unaided_apps": "food-delivery apps can you think of",
    "beh_last_platform": "most recent food-delivery order",
    "beh_last_order_total": "final amount you paid for that order",
    "beh_last_meal": "Which meal was it",
    "beh_platforms_used_4wk": "ordered food delivery from in the last 4 weeks",
    "beh_subscriptions": "memberships do you have",
    "beh_offer_dependency": "last 10 delivery orders",
    "pain_fee_reconsider_freq": "made me reconsider or change my order",
    "pain_bill_unreasonable_freq": "felt unreasonable for the food",
    "beh_abandon_price_freq": "left without placing an order",
    "pain_late_freq": "noticeably later than the time shown",
    "pain_cancel_freq": "cancelled by the app or the restaurant",
    "att_check_1": "please select \"Rarely\"",
    "pain_menu_markup_belief": "Menu prices on delivery apps are usually higher",
    "pain_top_frustrations": "frustrate you most",
    "exp_eta_max_dinner": "longest delivery time",
    "exp_fav_restaurant_needed": "how many of your usual restaurants would need",
    "beh_switch_savings_required": "How much lower would the final amount need to be",
    "bill_s1": "Which bill would you rather pay",
    "tradeoff_eta": "arrives in 30 minutes",
    "tradeoff_rel": "1 of every 10 orders",
    "tradeoff_rest": "most of your usual restaurants",
    "bt_trial_intent": "how likely are you to try Service X",
    "wtp_max_fee_direct": "highest delivery fee you would pay",
    "bt_concern": "would stop you from trying it",
    "br_trial_intent": "Now that you know it is Ownly",
    "br_rapido_effect": "being from Rapido make you",
    "own_aware_aided": "had you heard of Ownly",
    "own_tried": "ever placed an order on Ownly",
    "own_orders_4wk": "How many Ownly orders",
    "own_reliability_rating": "Ownly orders arrived on time",
    "own_perceived_savings": "your most recent Ownly order was",
    "own_disappointment": "disappointed you about Ownly",
    "own_not_tried_reason": "reasons you haven't ordered on it",
    "meta_found_survey": "Where did you find this survey",
}
# Trade-off questions: the Forms header is the question stem, so match on the stem too.
TRADEOFF_STEMS = {
    "tradeoff_eta": "same restaurant, same food. Which would you choose",
    "tradeoff_rel": "same restaurant, same food, same delivery time",
    "tradeoff_rest": "same food price level and delivery time",
}

FREQ5 = {"never": 1, "rarely": 2, "sometimes": 3, "often": 4, "very often": 5}
AGREE5 = {"strongly disagree": 1, "disagree": 2, "neither": 3, "agree": 4, "strongly agree": 5}
LIKELY5 = {"definitely not": 1, "probably not": 2, "not sure": 3, "probably": 4, "definitely": 5}
ORDERS4WK = {"none": 0, "1–3 times": 2, "4–7 times": 5.5, "8–15 times": 11.5, "16 or more times": 18}  # midpoints for index maths
SEGFREQ = {"1–3 times": "occasional", "4–7 times": "regular", "8–15 times": "frequent", "16 or more times": "frequent"}
OWN4WK = {"none": 0, "1": 1, "2–3": 2.5, "4–7": 5.5, "8 or more": 9}
ADI = {"none — i'd happily try new places": 1, "a few": 2, "about half": 3, "most": 4, "all or nearly all": 5}
FREQ_RATING = {"rarely": 1, "sometimes": 2, "about half the time": 3, "mostly": 4, "always": 5}

FRUSTRATION_OPTS = ["Delivery fees", "Platform, packaging or other charges", "Menu prices higher than at the restaurant",
                    "Offers that don't really save money", "Late delivery", "Cancelled orders", "Wrong or missing items",
                    "Getting refunds or help from support", "The restaurant I want isn't available",
                    "Food quality or hygiene", "Nothing really frustrates me"]
PRICE_SET = FRUSTRATION_OPTS[:4]
RELIAB_SET = ["Late delivery", "Cancelled orders"]
PLATFORM_OPTS = ["Swiggy", "Zomato", "Ownly app", "Rapido app (food section)", "Toing", "Magicpin", "Restaurant direct", "Other"]
NOT_TRIED_OPTS = ["Happy with my current app", "My usual restaurants weren't on it", "Not available at my location",
                  "Didn't trust a new app yet", "Expected slow delivery", "Didn't see real savings", "No offers or discounts",
                  "The payment method I use (e.g. cash on delivery or a meal card) isn't accepted",
                  "Didn't know how to access it", "Haven't got round to it", "Other"]
FEE_LEVELS = [0, 10, 20, 30, 40, 50, 60]


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"), float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (p, max(0, c - h), min(1, c + h))


def fmt_prop(k, n):
    p, lo, hi = wilson(k, n)
    if n == 0:
        return "NOT AVAILABLE (n=0)"
    return f"{p*100:.1f}% (95% CI {lo*100:.1f}–{hi*100:.1f}; {k}/{n})"


def norm(s):
    return (s or "").strip().lower()


def map_columns(header):
    colmap = {}
    for var, key in HEADERS.items():
        for h in header:
            if key.lower() in h.lower():
                colmap.setdefault(var, h)
    for var, stem in TRADEOFF_STEMS.items():
        for h in header:
            if stem.lower() in h.lower():
                colmap[var] = h
    return colmap


def has(opt, cell):
    return opt.lower() in (cell or "").lower()


def median_boot_ci(vals, reps=5000, seed=20260914):
    import random
    if not vals:
        return (float("nan"),) * 3
    rnd = random.Random(seed)
    meds = sorted(st.median([rnd.choice(vals) for _ in vals]) for _ in range(reps))
    return (st.median(vals), meds[int(0.025 * reps)], meds[int(0.975 * reps)])


def exact_binom_two_sided(k, n):
    if n == 0:
        return float("nan")
    p = [math.comb(n, i) * 0.5 ** n for i in range(n + 1)]
    obs = p[k]
    return min(1.0, sum(x for x in p if x <= obs + 1e-12))


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = sys.argv[1]
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "short_survey_outputs"
    if "08_clean_data" in os.path.abspath(out) and "DEMO_SYNTHETIC" in src:
        sys.exit("Refusing to write synthetic demo outputs into 08_clean_data/.")
    os.makedirs(out, exist_ok=True)
    rows = list(csv.DictReader(open(src, encoding="utf-8-sig")))
    header = list(rows[0].keys()) if rows else []
    cm = map_columns(header)
    missing = [v for v in HEADERS if v not in cm]
    g = lambda r, v: r.get(cm.get(v, "__none__"), "")

    # ---------- cleaning (flags, never silent deletion) ----------
    flow = Counter()
    cleaned, excluded = [], []
    grid_vars = ["pain_fee_reconsider_freq", "pain_bill_unreasonable_freq", "beh_abandon_price_freq", "pain_late_freq", "pain_cancel_freq"]
    for i, r in enumerate(rows, 1):
        r["resp_id"] = f"hyd_short_{i:04d}"
        flow["started"] += 1
        reason = ""
        if not norm(g(r, "meta_consent")).startswith("yes"):
            reason = "EX01_screen_fail:no_consent"
        elif norm(g(r, "scr_age_band")) in ("under 20", "over 30", ""):
            reason = "EX01_screen_fail:age"
        elif norm(g(r, "scr_area")).startswith(("somewhere else", "i don't live")) or not g(r, "scr_area"):
            reason = "EX01_screen_fail:area"
        elif norm(g(r, "scr_orders_4wk")) in ("none", ""):
            reason = "EX01_screen_fail:no_recent_order"
        elif cm.get("att_check_1") and norm(g(r, "att_check_1")) != "rarely":
            reason = "EX03_attention_fail"
        else:
            vals = [FREQ5.get(norm(g(r, v))) for v in grid_vars]
            if all(v is not None for v in vals) and len(set(vals)) == 1:
                r["FLAG_straightline_borderline"] = "1"  # borderline: kept, flagged
            tot = g(r, "beh_last_order_total").replace("₹", "").replace(",", "").strip()
            try:
                t = float(tot)
                if t < 50 or t > 5000:
                    r["FLAG_total_out_of_range"] = "1"
            except ValueError:
                r["FLAG_total_unparsed"] = "1"
        if reason:
            r["exclusion_reason"] = reason
            excluded.append(r)
            flow[reason.split(":")[0] + (":" + reason.split(":")[1] if ":" in reason else "")] += 1
        else:
            cleaned.append(r)
    flow["valid"] = len(cleaned)

    def write(path, data):
        if not data:
            open(path, "w").close()
            return
        keys = sorted({k for d in data for k in d.keys()})
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            w.writerows(data)
    write(os.path.join(out, "cleaned.csv"), cleaned)
    write(os.path.join(out, "excluded.csv"), excluded)
    with open(os.path.join(out, "sample_flow.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["stage", "n"])
        for k, v in flow.items():
            w.writerow([k, v])

    C = cleaned
    n = len(C)
    K = []  # (kpi, segment, value_text, n, source_formula)

    def seg_of(r):
        o = norm(g(r, "seg_occupation_raw"))
        if o.startswith("full-time student"):
            return "student"
        if o.startswith("working full-time"):
            return "working_professional"
        if o.startswith("studying and working"):
            return "working_student"
        return "other"

    segs = {"all": C,
            "student": [r for r in C if seg_of(r) == "student"],
            "working_professional": [r for r in C if seg_of(r) == "working_professional"]}

    for sname, S in segs.items():
        m = len(S)
        # PPI (≥3 of 4 items)
        ppis = []
        for r in S:
            items = [FREQ5.get(norm(g(r, "pain_fee_reconsider_freq"))), FREQ5.get(norm(g(r, "pain_bill_unreasonable_freq"))),
                     AGREE5.get(norm(g(r, "pain_menu_markup_belief"))), FREQ5.get(norm(g(r, "beh_abandon_price_freq")))]
            items = [x for x in items if x is not None]
            if len(items) >= 3:
                ppis.append((st.mean(items) - 1) / 4 * 100)
        md, lo, hi = median_boot_ci(ppis)
        K.append(("Price Pain Index (median, 0–100)", sname, f"{md:.1f} (95% CI {lo:.1f}–{hi:.1f})" if ppis else "NOT AVAILABLE", len(ppis), "PPI = (mean of 4 items − 1)/4×100"))
        k = sum(1 for r in S if (FREQ5.get(norm(g(r, "pain_fee_reconsider_freq"))) or 0) >= 3)
        K.append(("H1.1 Checkout charges made me reconsider (sometimes+)", sname, fmt_prop(k, m), m, "freq ≥ 3"))
        k = sum(1 for r in S if (FREQ5.get(norm(g(r, "beh_abandon_price_freq"))) or 0) >= 2)
        K.append(("H1.4 Abandoned a cart after seeing final amount (rarely+)", sname, fmt_prop(k, m), m, "freq ≥ 2"))
        k = sum(1 for r in S if (AGREE5.get(norm(g(r, "pain_menu_markup_belief"))) or 0) >= 4)
        m2 = sum(1 for r in S if norm(g(r, "pain_menu_markup_belief")) in AGREE5)
        K.append(("H1.3 Believe app menu prices are higher (agree)", sname, fmt_prop(k, m2), m2, "top-2 box, DK excluded"))
        kp = sum(1 for r in S if any(has(o, g(r, "pain_top_frustrations")) for o in PRICE_SET))
        kr = sum(1 for r in S if any(has(o, g(r, "pain_top_frustrations")) for o in RELIAB_SET))
        K.append(("H1.2 Price/fee frustration in top-3", sname, fmt_prop(kp, m), m, "any of 4 price options"))
        K.append(("H1.2 Late/cancel frustration in top-3", sname, fmt_prop(kr, m), m, "late or cancelled"))
        for opt in FRUSTRATION_OPTS:
            k = sum(1 for r in S if has(opt, g(r, "pain_top_frustrations")))
            K.append((f"Top frustration: {opt}", sname, fmt_prop(k, m), m, "select up to 3"))
        # switching threshold
        sav = []
        never = 0
        for r in S:
            v = norm(g(r, "beh_switch_savings_required"))
            if v.startswith("no amount"):
                never += 1
            else:
                mm = re.search(r"₹\s*(\d+)", v)
                if mm:
                    sav.append(float(mm.group(1)))
        md, lo, hi = median_boot_ci(sav)
        K.append(("H2.3 Required saving to switch main app (median ₹)", sname, f"{md:.0f} (95% CI {lo:.0f}–{hi:.0f})" if sav else "NOT AVAILABLE", len(sav), "excludes 'no amount' and DK; '₹100 or more' coded 100"))
        K.append(("Price alone would never make me switch", sname, fmt_prop(never, m), m, ""))
        # trade-offs: share choosing the cheaper option (App B)
        for var, label in [("tradeoff_eta", "H3 Chose ₹30 cheaper but 15 min slower"), ("tradeoff_rel", "H4 Chose ₹30 cheaper but late 3/10 vs 1/10"), ("tradeoff_rest", "H5 Chose ₹30 cheaper but only a few usual restaurants")]:
            ans = [norm(g(r, var)) for r in S if g(r, var)]
            k = sum(1 for a in ans if a.startswith("app b"))
            K.append((label, sname, fmt_prop(k, len(ans)), len(ans), "share choosing cheaper App B; >50% with CI lower bound >50% = ₹30 buys the compromise (stated, hypothetical)"))
        # bill transparency
        ans = [norm(g(r, "bill_s1")) for r in S if g(r, "bill_s1")]
        k1 = sum(1 for a in ans if a == "bill 1")
        k2 = sum(1 for a in ans if a == "bill 2")
        K.append(("H2.2 Prefer simple bill (Bill 1) at equal total", sname, fmt_prop(k1, k1 + k2) + f"; exact binomial p={exact_binom_two_sided(k1, k1 + k2):.3f}; 'no difference' {len(ans)-k1-k2}", k1 + k2, "no-difference excluded from denominator"))
        # expectations
        eta = []
        for r in S:
            mm = re.search(r"(\d+)", g(r, "exp_eta_max_dinner"))
            if mm:
                eta.append(75.0 if "more than" in norm(g(r, "exp_eta_max_dinner")) else float(mm.group(1)))
        md, lo, hi = median_boot_ci(eta)
        K.append(("Max acceptable dinner ETA (median minutes)", sname, f"{md:.0f} (95% CI {lo:.0f}–{hi:.0f})" if eta else "NOT AVAILABLE", len(eta), ""))
        adi = [ADI.get(norm(g(r, "exp_fav_restaurant_needed"))) for r in S]
        adi = [a for a in adi if a]
        k = sum(1 for a in adi if a >= 4)
        K.append(("H10.1 Need most/all usual restaurants before trying a new app", sname, fmt_prop(k, len(adi)), len(adi), "ADI ≥ 75"))
        # fee acceptance curve (direct)
        fees = []
        for r in S:
            mm = re.search(r"₹\s*(\d+)", g(r, "wtp_max_fee_direct"))
            if mm:
                fees.append(int(mm.group(1)))
        for lvl in FEE_LEVELS:
            k = sum(1 for x in fees if x >= lvl)
            K.append((f"H8 Would pay delivery fee ≥ ₹{lvl}", sname, fmt_prop(k, len(fees)), len(fees), "direct max-fee question (less rigorous than a ladder)"))
        # brand
        pairs = [(LIKELY5.get(norm(g(r, "bt_trial_intent"))), LIKELY5.get(norm(g(r, "br_trial_intent")))) for r in S]
        pairs = [p for p in pairs if None not in p]
        kb = sum(1 for a, b in pairs if a >= 4)
        ka = sum(1 for a, b in pairs if b >= 4)
        up = sum(1 for a, b in pairs if a < 4 <= b)
        down = sum(1 for a, b in pairs if b < 4 <= a)
        K.append(("Trial intent top-2 BEFORE brand reveal (Service X)", sname, fmt_prop(kb, len(pairs)), len(pairs), "stated intent, not behaviour"))
        K.append(("Trial intent top-2 AFTER reveal (Ownly by Rapido)", sname, fmt_prop(ka, len(pairs)) + f"; moved up {up}, down {down}; exact McNemar p={exact_binom_two_sided(up, up + down):.3f}", len(pairs), "within-subject; demand effects possible"))
        # Ownly funnel & course-sheet KPIs
        aware = [r for r in S if norm(g(r, "own_aware_aided")) in ("yes, clearly", "i think so")]
        tried = [r for r in S if norm(g(r, "own_tried")) == "yes"]
        K.append(("Aided awareness of Ownly", sname, fmt_prop(len(aware), m), m, ""))
        K.append(("Penetration share = tried Ownly ÷ delivery users (in sample)", sname, fmt_prop(len(tried), m), m, "Brand penetration ÷ market penetration; all valid respondents are delivery users"))
        K.append(("H11.3 Aware → tried conversion", sname, fmt_prop(len(tried), len(aware)), len(aware), ""))
        rep = sum(1 for r in tried if (OWN4WK.get(norm(g(r, "own_orders_4wk"))) or 0) >= 2)
        K.append(("Retention proxy: tried users with ≥2 Ownly orders in last 4 weeks", sname, fmt_prop(rep, len(tried)), len(tried), "PROXY for retention rate (no cohort data)"))
        if len(tried) >= 10:
            own = [OWN4WK.get(norm(g(r, "own_orders_4wk"))) for r in tried]
            cat = [ORDERS4WK.get(norm(g(r, "scr_orders_4wk"))) for r in tried]
            pairs2 = [(a, b) for a, b in zip(own, cat) if a is not None and b]
            sor = sum(a for a, b in pairs2) / sum(b for a, b in pairs2) if pairs2 else float("nan")
            allcat = [ORDERS4WK.get(norm(g(r, "scr_orders_4wk"))) for r in S]
            allcat = [x for x in allcat if x]
            ui = (st.mean([b for a, b in pairs2]) / st.mean(allcat)) if pairs2 and allcat else float("nan")
            ps = len(tried) / m
            K.append(("Share of requirements (Ownly orders ÷ all orders of Ownly triers)", sname, f"{sor*100:.1f}%", len(pairs2), "category midpoints; approximate"))
            K.append(("Heavy usage index (orders of triers ÷ orders of all)", sname, f"{ui:.2f}", len(pairs2), ">1 = triers are heavier users"))
            K.append(("Market share decomposition: penetration share × share of req. × usage index", sname, f"{ps*sor*ui*100:.1f}% of sample orders (approx.)", m, "within this sample only"))
        else:
            K.append(("Share of requirements / usage index / share decomposition", sname, f"NOT TESTABLE (only {len(tried)} Ownly triers; need ≥10)", len(tried), ""))
        for opt in NOT_TRIED_OPTS:
            base = [r for r in aware if norm(g(r, "own_tried")) != "yes"]
            k = sum(1 for r in base if has(opt, g(r, "own_not_tried_reason")))
            K.append((f"Not-tried reason: {opt}", sname, fmt_prop(k, len(base)), len(base), "aware non-triers; up to 3"))

    # Brand development index (students vs professionals)
    tr_all = sum(1 for r in C if norm(g(r, "own_tried")) == "yes") / n if n else float("nan")
    for sname in ("student", "working_professional"):
        S = segs[sname]
        if len(S) >= 20 and tr_all and tr_all == tr_all and tr_all > 0:
            rate = sum(1 for r in S if norm(g(r, "own_tried")) == "yes") / len(S)
            K.append(("Brand development index (trial rate vs overall ×100)", sname, f"{rate/tr_all*100:.0f}", len(S), ">100 over-indexes; directional"))
        else:
            K.append(("Brand development index", sname, "NOT TESTABLE (segment n<20 or no triers)", len(S), ""))

    with open(os.path.join(out, "kpis.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["kpi", "segment", "value", "n", "definition"])
        w.writerows(K)

    with open(os.path.join(out, "report.md"), "w", encoding="utf-8") as f:
        f.write("# Short survey results (auto-generated; exploratory, convenience sample)\n\n")
        f.write(f"Source: `{os.path.basename(src)}`. Valid n = {n}. Unmapped columns: {', '.join(missing) or 'none'}.\n\n")
        f.write("## Sample flow\n\n| stage | n |\n|---|---|\n" + "".join(f"| {k} | {v} |\n" for k, v in flow.items()))
        f.write("\n## KPIs\n\n| KPI | segment | value | n |\n|---|---|---|---|\n")
        for kpi, s, v, nn, _ in K:
            f.write(f"| {kpi} | {s} | {v} | {nn} |\n")
        f.write("\n**Caveats:** convenience sample of reached 20–30s around Gachibowli; not representative of Hyderabad. Trade-offs and intent are stated, hypothetical preferences. Segment results with n<30 are directional only.\n")
    print(f"valid n={n}; outputs in {out}; unmapped: {missing}")


if __name__ == "__main__":
    main()
