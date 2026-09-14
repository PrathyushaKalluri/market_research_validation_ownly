#!/usr/bin/env python3
"""Analyse the 3-day LITE competitor price audit + test orders.

Standard library only.

Usage:
    python3 analyze_audit_lite.py audit_captures.csv [test_orders.csv] [--out OUTDIR]

audit_captures.csv columns (see 06_competitor_audit/audit_lite_template.csv):
    capture_ts, slot, auditor_id, drop_point_id, platform, account_state, subscription_active, restaurant_name,
    restaurant_listed, restaurant_open, basket_id, item_list, item_match_quality, menu_subtotal, packaging_fee,
    platform_fee, delivery_fee, small_cart_fee, surge_rain_fee, taxes_gst, discount_amount, discount_type,
    final_payable, eta_min_shown, eta_max_shown, screenshot_file, notes

test_orders.csv columns (06_competitor_audit/test_orders_template.csv):
    order_id, platform, restaurant_name, item_list, order_ts, eta_min_shown, eta_max_shown, pickup_ts,
    delivered_ts, final_payable, delivery_fee_charged, other_fees_charged, order_accurate, issue_notes

Matching key: restaurant × basket × slot × date × drop point × coupon state.
Ownly is compared with each other platform. Ties are within ₹5.
"""
import csv, math, os, random, statistics as st, sys
from collections import defaultdict
from datetime import datetime


def num(x):
    try:
        return float(str(x).replace("₹", "").replace(",", "").strip())
    except ValueError:
        return None


def boot_median(vals, clusters, reps=5000, seed=20260914):
    """Cluster bootstrap by restaurant."""
    if not vals:
        return (float("nan"),) * 3
    rnd = random.Random(seed)
    by = defaultdict(list)
    for v, c in zip(vals, clusters):
        by[c].append(v)
    keys = list(by)
    meds = []
    for _ in range(reps):
        sample = []
        for _k in keys:
            sample += by[rnd.choice(keys)]
        meds.append(st.median(sample))
    meds.sort()
    return (st.median(vals), meds[int(.025 * reps)], meds[int(.975 * reps)])


def wilson(k, n, z=1.96):
    if n == 0:
        return "n=0"
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return f"{p*100:.0f}% (95% CI {max(0, c-h)*100:.0f}–{min(1, c+h)*100:.0f}; {k}/{n})"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "audit_outputs"
    if "--out" in sys.argv:
        args = [a for a in args if a != out]
    os.makedirs(out, exist_ok=True)
    rows = list(csv.DictReader(open(args[0], encoding="utf-8-sig")))
    lines = ["# Lite audit results (auto-generated)\n", f"Captures: {len(rows)}\n"]

    # arithmetic check
    bad = []
    for r in rows:
        parts = [num(r.get(k)) or 0 for k in ["menu_subtotal", "packaging_fee", "platform_fee", "delivery_fee", "small_cart_fee", "surge_rain_fee", "taxes_gst"]]
        fp = num(r.get("final_payable"))
        if fp is not None and r.get("restaurant_open", "y").lower().startswith("y"):
            calc = sum(parts) - (num(r.get("discount_amount")) or 0)
            if abs(calc - fp) > 2:
                r["EXA1_arith"] = "1"
                bad.append(r)
    lines.append(f"Arithmetic mismatches > ₹2 (recheck screenshots; excluded from pairs): {len(bad)}\n")

    # per-platform summaries
    plat = defaultdict(list)
    for r in rows:
        if r.get("EXA1_arith") or not (r.get("restaurant_open", "").lower().startswith("y")):
            continue
        plat[r["platform"].strip().lower()].append(r)
    lines.append("\n## Price per basket (price per statistical unit) and fee share, by platform\n\n| platform | n | median final payable ₹ | median non-food charges ₹ | median fee share of bill | median ETA midpoint (min) |\n|---|---|---|---|---|---|\n")
    for p, rs in sorted(plat.items()):
        fps = [num(r["final_payable"]) for r in rs if num(r["final_payable"])]
        nonfood = [num(r["final_payable"]) - (num(r["menu_subtotal"]) or 0) for r in rs if num(r["final_payable"]) and num(r["menu_subtotal"])]
        share = [(num(r["final_payable"]) - num(r["menu_subtotal"])) / num(r["final_payable"]) for r in rs if num(r["final_payable"]) and num(r["menu_subtotal"])]
        eta = [(num(r["eta_min_shown"]) + num(r["eta_max_shown"])) / 2 for r in rs if num(r.get("eta_min_shown")) and num(r.get("eta_max_shown"))]
        f = lambda v, pct=False: (f"{st.median(v)*100:.0f}%" if pct else f"{st.median(v):.0f}") if v else "—"
        lines.append(f"| {p} | {len(rs)} | {f(fps)} | {f(nonfood)} | {f(share, True)} | {f(eta)} |\n")

    # coverage
    lines.append("\n## Coverage (listed and open), by platform and slot\n\n| platform | slot | listed & open | \n|---|---|---|\n")
    cov = defaultdict(lambda: [0, 0])
    for r in rows:
        key = (r["platform"].strip().lower(), r.get("slot", ""))
        cov[key][1] += 1
        if r.get("restaurant_listed", "").lower().startswith("y") and r.get("restaurant_open", "").lower().startswith("y"):
            cov[key][0] += 1
    for (p, s), (k, n) in sorted(cov.items()):
        lines.append(f"| {p} | {s} | {wilson(k, n)} |\n")

    # matched pairs: Ownly vs each competitor
    def key(r):
        d = (r.get("capture_ts", "")[:10])
        return (r["restaurant_name"].strip().lower(), r.get("basket_id", ""), r.get("slot", ""), d, r.get("drop_point_id", ""))

    def cstate(r):
        return "with_coupon" if (num(r.get("discount_amount")) or 0) > 0 else "no_coupon"
    # idx[key][platform][coupon_state] = row
    idx = defaultdict(lambda: defaultdict(dict))
    for p, rs in plat.items():
        for r in rs:
            if r.get("item_match_quality", "exact").lower() in ("none",) or num(r.get("final_payable")) is None:
                continue
            idx[key(r)][p][cstate(r)] = r
    pair_rows = []
    for k, byp in idx.items():
        if "ownly" not in byp:
            continue
        own = byp["ownly"]
        own_list = own.get("no_coupon") or own.get("with_coupon")          # Ownly list price
        own_best = min(own.values(), key=lambda x: num(x["final_payable"]))  # Ownly best available
        for comp, states in byp.items():
            if comp == "ownly":
                continue
            comparisons = []
            if "no_coupon" in states:
                comparisons.append(("no_coupon (both without coupons)", own_list, states["no_coupon"]))
            if "with_coupon" in states:
                comparisons.append(("after_coupons (best available on each app)", own_best, states["with_coupon"]))
            elif "no_coupon" in states:
                # no coupon offered by the competitor: best-available comparison equals the list comparison
                comparisons.append(("after_coupons (best available on each app)", own_best, states["no_coupon"]))
            for label, ro, rc in comparisons:
                gap = num(ro["final_payable"]) - num(rc["final_payable"])
                eg = None
                if all(num(x.get(c)) for x in (ro, rc) for c in ("eta_min_shown", "eta_max_shown")):
                    eg = (num(ro["eta_min_shown"]) + num(ro["eta_max_shown"])) / 2 - (num(rc["eta_min_shown"]) + num(rc["eta_max_shown"])) / 2
                pair_rows.append({"restaurant": k[0], "basket_id": k[1], "slot": k[2], "date": k[3], "drop_point": k[4], "coupon_state": label,
                                  "comparator": comp, "ownly_final": ro["final_payable"], "comp_final": rc["final_payable"],
                                  "gap_ownly_minus_comp": round(gap, 2), "eta_gap_min": "" if eg is None else round(eg, 1)})
    with open(os.path.join(out, "audit_pairs.csv"), "w", newline="", encoding="utf-8") as f:
        if pair_rows:
            w = csv.DictWriter(f, fieldnames=list(pair_rows[0].keys()))
            w.writeheader()
            w.writerows(pair_rows)
    lines.append("\n## Matched comparisons: Ownly minus competitor (negative = Ownly cheaper)\n\n| comparator | coupon state | pairs | median gap ₹ (95% cluster-bootstrap CI) | Ownly cheaper (win rate, tie ≤ ₹5) | median ETA gap (min, + = Ownly slower) |\n|---|---|---|---|---|---|\n")
    grp = defaultdict(list)
    for pr in pair_rows:
        grp[(pr["comparator"], pr["coupon_state"])].append(pr)
    for (c, cs), prs in sorted(grp.items()):
        gaps = [p["gap_ownly_minus_comp"] for p in prs]
        md, lo, hi = boot_median(gaps, [p["restaurant"] for p in prs])
        wins = sum(1 for x in gaps if x < -5)
        etas = [p["eta_gap_min"] for p in prs if p["eta_gap_min"] != ""]
        label = "DIRECTIONAL (<20 pairs)" if len(prs) < 20 else ""
        lines.append(f"| {c} | {cs} | {len(prs)} {label} | {md:.0f} ({lo:.0f} to {hi:.0f}) | {wilson(wins, len(prs))} | {st.median(etas):.0f} |\n" if etas else f"| {c} | {cs} | {len(prs)} {label} | {md:.0f} ({lo:.0f} to {hi:.0f}) | {wilson(wins, len(prs))} | — |\n")

    # test orders
    if len(args) > 1 and os.path.exists(args[1]):
        to = list(csv.DictReader(open(args[1], encoding="utf-8-sig")))
        lines.append("\n## Test orders (n = %d; anecdotal — do not generalise)\n\n| platform | promised ETA (min) | actual (min) | late vs max promise (min) | final payable ₹ | delivery fee ₹ | accurate |\n|---|---|---|---|---|---|---|\n" % len(to))
        for t in to:
            try:
                o = datetime.fromisoformat(t["order_ts"])
                dlv = datetime.fromisoformat(t["delivered_ts"])
                actual = (dlv - o).total_seconds() / 60
                late = actual - (num(t["eta_max_shown"]) or 0)
                a, l = f"{actual:.0f}", f"{late:+.0f}"
            except Exception:
                a, l = "—", "—"
            lines.append(f"| {t['platform']} | {t.get('eta_min_shown','')}–{t.get('eta_max_shown','')} | {a} | {l} | {t.get('final_payable','')} | {t.get('delivery_fee_charged','')} | {t.get('order_accurate','')} |\n")
    lines.append("\n**Caveats:** prices shown are for the team's own accounts at capture time (offers are personalised); captures stopped before payment; small number of restaurants and slots.\n")
    open(os.path.join(out, "audit_report.md"), "w", encoding="utf-8").write("".join(lines))
    print("".join(lines))


if __name__ == "__main__":
    main()
