#!/usr/bin/env python3
"""
Fake-door value-proposition experiment analysis — hyd_vp_fakedoor_v1
Standard library only (Python 3.8+). Reproducible: fixed random seed.

Usage
  Analyse real data (CSV exported from the Google Sheet "events" tab):
    python3 analyze_fakedoor.py analyse --events 08_clean_data/raw/fakedoor_events_raw.csv \
        --out 09_analysis/fakedoor --page-version 2026-09-14.1 [--start 2026-09-16 --end 2026-09-26]

  Generate a SYNTHETIC fixture to test this code (never real, never in 08_clean_data):
    python3 analyze_fakedoor.py make-demo --path <scratch>/DEMO_SYNTHETIC_fakedoor_events.csv

Outputs (in --out)
  fakedoor_summary.csv      long table: scope, group, variant, metric, x, n, rate, ci_low, ci_high
  fakedoor_pairwise.csv     pairwise variant tests with Holm-adjusted p-values and effect sizes
  fakedoor_exclusions.csv   one row per excluded visitor with exclusion_reason (never silently dropped)
  fakedoor_report.md        human-readable report incl. DIRECTIONAL / CONFIRMATORY label
Pre-registered rules live in analysis_framework.md; do not change thresholds after seeing results.
"""
import argparse
import csv
import json
import math
import os
import random
import sys
import uuid
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from statistics import NormalDist, median

EXPERIMENT_ID = "hyd_vp_fakedoor_v1"
VARIANTS = ["A", "B", "C"]
VARIANT_KEYS = {"A": "A_total_price", "B": "B_transparent_bill", "C": "C_reliable_value"}

# ---- Pre-registered constants (see analysis_framework.md) ----
ALPHA = 0.05
POWER = 0.80
PLANNING_DELTA = 0.10          # +10 percentage points: smallest effect the team treats as decision-relevant
MIN_CTA_MS = 1000              # CTA faster than 1 s after load = not a reading human -> excluded
BOUNCE_DWELL_MS = 10000        # no scroll/CTA and < 10 s dwell = bounce
MIN_SUBGROUP_N = 30            # subgroup cells below this are shown but flagged "n<30, do not interpret"
SRM_ALPHA = 0.01               # sample-ratio-mismatch alarm
PBEST_DRAWS = 20000
SEED = 20260914

ORDERS_TO_FREQ = {"0": "none", "1_3": "occasional", "4_7": "regular", "8_plus": "frequent",
                  "not_sure": "unknown", "no_answer": "unknown"}

ND = NormalDist()


# ============================== statistics ==============================
def wilson(x, n, conf=0.95):
    if n == 0:
        return float("nan"), float("nan")
    z = ND.inv_cdf(1 - (1 - conf) / 2)
    p = x / n
    denom = 1 + z * z / n
    centre = p + z * z / (2 * n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return max(0.0, (centre - half) / denom), min(1.0, (centre + half) / denom)


def newcombe_diff_ci(x1, n1, x2, n2):
    """95% CI for p2 - p1 (Newcombe hybrid score, method 10)."""
    p1, p2 = x1 / n1, x2 / n2
    l1, u1 = wilson(x1, n1)
    l2, u2 = wilson(x2, n2)
    d = p2 - p1
    return d - math.sqrt((p2 - l2) ** 2 + (u1 - p1) ** 2), d + math.sqrt((u2 - p2) ** 2 + (p1 - l1) ** 2)


def two_prop_z(x1, n1, x2, n2):
    p = (x1 + x2) / (n1 + n2)
    se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    if se == 0:
        return 0.0, 1.0
    z = (x2 / n2 - x1 / n1) / se
    return z, 2 * (1 - ND.cdf(abs(z)))


def _log_comb(n, k):
    return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)


def fisher_exact_two_sided(x1, n1, x2, n2):
    k = x1 + x2
    total = n1 + n2
    lo, hi = max(0, k - n2), min(k, n1)

    def prob(a):
        return math.exp(_log_comb(n1, a) + _log_comb(n2, k - a) - _log_comb(total, k))

    p_obs = prob(x1)
    return min(1.0, sum(prob(a) for a in range(lo, hi + 1) if prob(a) <= p_obs * (1 + 1e-7)))


def cohens_h(p1, p2):
    return 2 * math.asin(math.sqrt(p2)) - 2 * math.asin(math.sqrt(p1))


def holm(pvals):
    m = len(pvals)
    order = sorted(range(m), key=lambda i: pvals[i])
    adj = [0.0] * m
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (m - rank) * pvals[i]))
        adj[i] = running
    return adj


def n_required(p1, delta, alpha, power=POWER):
    p2 = min(0.999, p1 + delta)
    za, zb = ND.inv_cdf(1 - alpha / 2), ND.inv_cdf(power)
    pb = (p1 + p2) / 2
    return math.ceil((za * math.sqrt(2 * pb * (1 - pb)) + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 / (p2 - p1) ** 2)


def srm_pvalue(counts):
    """Chi-square goodness of fit vs equal allocation. df = k-1 (closed form for df=2; normal approx otherwise)."""
    k, total = len(counts), sum(counts)
    if total == 0:
        return float("nan"), float("nan")
    exp = total / k
    chi2 = sum((c - exp) ** 2 / exp for c in counts)
    if k == 3:
        return chi2, math.exp(-chi2 / 2)
    df = k - 1  # Wilson-Hilferty approximation
    z = ((chi2 / df) ** (1 / 3) - (1 - 2 / (9 * df))) / math.sqrt(2 / (9 * df))
    return chi2, 1 - ND.cdf(z)


def p_best(successes, trials, draws=PBEST_DRAWS, seed=SEED):
    rng = random.Random(seed)
    wins = Counter()
    keys = list(successes)
    for _ in range(draws):
        samples = {v: rng.betavariate(1 + successes[v], 1 + trials[v] - successes[v]) for v in keys}
        wins[max(samples, key=samples.get)] += 1
    return {v: wins[v] / draws for v in keys}


# ============================== loading & cleaning ==============================
def truthy(v):
    return str(v).strip().lower() in ("true", "1", "yes", "y")


def parse_ts(s):
    try:
        return datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except ValueError:
        return None


def load_events(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        raw = r.get("payload_json", r.get("payload", "")) or "{}"
        try:
            r["_payload"] = json.loads(raw)
        except json.JSONDecodeError:
            r["_payload"] = {}
        r["_ts"] = parse_ts(r.get("ts", ""))
        try:
            r["_tsl"] = int(float(r.get("time_since_load_ms") or 0))
        except ValueError:
            r["_tsl"] = 0
    return rows


def build_visitors(rows, page_version=None, start=None, end=None):
    log = {"raw_events": len(rows)}
    rows = [r for r in rows if r.get("experiment_id") == EXPERIMENT_ID]
    log["events_this_experiment"] = len(rows)
    versions = Counter(r.get("page_version", "") for r in rows)
    if page_version:
        rows = [r for r in rows if r.get("page_version") == page_version]
    elif len(versions) > 1:
        sys.exit(f"Multiple page_version values found {dict(versions)}. Re-run with --page-version (copy changed mid-test).")
    log["events_this_version"] = len(rows)

    seen, dedup = set(), []
    for r in rows:
        key = (r.get("anon_session_id"), r.get("event_name"), r.get("ts"), r.get("payload_json", ""))
        if key in seen:
            continue
        seen.add(key)
        dedup.append(r)
    log["exact_duplicate_events_removed"] = len(rows) - len(dedup)

    by_visitor = defaultdict(list)
    for r in dedup:
        by_visitor[r.get("anon_visitor_id", "")].append(r)

    visitors, exclusions = [], []
    for vid, evs in by_visitor.items():
        evs.sort(key=lambda r: (r["_ts"] or datetime.min.replace(tzinfo=timezone.utc)))
        variants = {r.get("variant_id") for r in evs}
        first = evs[0]
        reason = None
        if not vid:
            reason = "missing_visitor_id"
        elif any(truthy(r.get("is_qa")) for r in evs):
            reason = "qa_traffic"
        elif any(truthy(r.get("is_bot_suspect")) for r in evs):
            reason = "bot_suspect"
        elif len(variants) > 1 or not variants <= set(VARIANTS):
            reason = "multiple_or_invalid_variant"
        elif start and first["_ts"] and first["_ts"] < start:
            reason = "outside_test_window"
        elif end and first["_ts"] and first["_ts"] >= end:
            reason = "outside_test_window"
        else:
            ctas = [r["_tsl"] for r in evs if r.get("event_name") == "cta_click"]
            if ctas and min(ctas) < MIN_CTA_MS:
                reason = "cta_faster_than_1s"
        if reason:
            exclusions.append({"anon_visitor_id": vid, "variant_id": "|".join(sorted(v for v in variants if v)), "exclusion_reason": reason, "n_events": len(evs)})
            continue

        names = Counter(r.get("event_name") for r in evs)
        exit_dwell = max([int(r["_payload"].get("dwell_ms", 0) or 0) for r in evs if r.get("event_name") == "exit"] or [0])
        cta_times = [r["_tsl"] for r in evs if r.get("event_name") == "cta_click"]
        mini = [r["_payload"] for r in evs if r.get("event_name") == "mini_survey_submit"]
        seg = mini[-1] if mini else {}
        bills = [r["_payload"] for r in evs if r.get("event_name") == "secondary_intent"]
        src = (first.get("utm_source") or "").strip().lower()
        if not src:
            src = ("ref:" + first["referrer_domain"]) if first.get("referrer_domain") else "(direct/none)"
        visitors.append({
            "visitor": vid,
            "variant": first.get("variant_id"),
            "source": src,
            "device": first.get("device_type", ""),
            "first_ts": first["_ts"],
            "vp": names["vp_view"] > 0 or names["cta_click"] > 0,
            "scroll": names["scroll_50"] > 0,
            "cta": names["cta_click"] > 0,
            "secondary": names["secondary_intent"] > 0,
            "mini": names["mini_survey_submit"] > 0,
            "survey_click": names["survey_link_click"] > 0,
            "bounce": names["cta_click"] == 0 and names["scroll_50"] == 0 and exit_dwell < BOUNCE_DWELL_MS,
            "time_to_cta": min(cta_times) if cta_times else None,
            "seg_occupation": seg.get("seg_occupation", "unknown") if seg else "not_asked",
            "seg_freq": ORDERS_TO_FREQ.get(seg.get("orders_4wk", ""), "unknown") if seg else "not_asked",
            "locality": seg.get("locality", "unknown") if seg else "not_asked",
            "bill_gap_pct": bills[-1].get("bill_gap_pct") if bills else None,
        })
    log["visitors_total"] = len(by_visitor)
    log["visitors_excluded"] = len(exclusions)
    log["visitors_analysed"] = len(visitors)
    log["exclusions_by_reason"] = dict(Counter(e["exclusion_reason"] for e in exclusions))
    return visitors, exclusions, log


# ============================== analysis ==============================
METRICS = [
    # (metric, numerator flag, denominator flag or None=all visitors, label)
    ("vp_view_rate", "vp", None, "Value-proposition view / visitors"),
    ("cta_ctr", "cta", None, "CTA click / visitors  [PRIMARY]"),
    ("cta_given_vp", "cta", "vp", "CTA click / VP viewers"),
    ("secondary_rate", "secondary", None, "Bill-compare completed / visitors  [KEY SECONDARY]"),
    ("secondary_given_cta", "secondary", "cta", "Bill-compare completed / CTA clickers"),
    ("mini_given_cta", "mini", "cta", "Mini-survey submitted / CTA clickers"),
    ("survey_click_given_cta", "survey_click", "cta", "Main-survey link click / CTA clickers"),
    ("bounce_rate", "bounce", None, "Bounce / visitors"),
]


def rate_rows(scope, group, subset):
    out = []
    for v in VARIANTS:
        vs = [x for x in subset if x["variant"] == v]
        for metric, num, den, _ in METRICS:
            base = vs if den is None else [x for x in vs if x[den]]
            n = len(base)
            x = sum(1 for b in base if b[num])
            lo, hi = wilson(x, n) if n else (float("nan"), float("nan"))
            out.append({"scope": scope, "group": group, "variant": v, "metric": metric, "x": x, "n": n,
                        "rate": round(x / n, 4) if n else "", "ci_low": round(lo, 4) if n else "", "ci_high": round(hi, 4) if n else "",
                        "flag": "n<30, do not interpret" if n < MIN_SUBGROUP_N else ""})
    return out


def pairwise(visitors, metric, num):
    counts = {v: (sum(1 for x in visitors if x["variant"] == v and x[num]), sum(1 for x in visitors if x["variant"] == v)) for v in VARIANTS}
    pairs = [("A", "B"), ("A", "C"), ("B", "C")]
    res = []
    for a, b in pairs:
        x1, n1 = counts[a]
        x2, n2 = counts[b]
        if n1 == 0 or n2 == 0:
            res.append({"metric": metric, "pair": f"{b}-{a}", "test": "n/a", "p_raw": 1.0})
            continue
        pool = (x1 + x2) / (n1 + n2)
        min_expected = min(n1 * pool, n1 * (1 - pool), n2 * pool, n2 * (1 - pool))
        if min_expected < 5:
            test, p = "fisher_exact", fisher_exact_two_sided(x1, n1, x2, n2)
            z = ""
        else:
            test = "two_prop_z"
            z, p = two_prop_z(x1, n1, x2, n2)
            z = round(z, 3)
        lo, hi = newcombe_diff_ci(x1, n1, x2, n2)
        res.append({"metric": metric, "pair": f"{b}-{a}", "rate_first": round(x1 / n1, 4), "rate_second": round(x2 / n2, 4),
                    "diff_pp": round((x2 / n2 - x1 / n1) * 100, 2), "diff_ci_low_pp": round(lo * 100, 2), "diff_ci_high_pp": round(hi * 100, 2),
                    "cohens_h": round(cohens_h(x1 / n1, x2 / n2), 3), "test": test, "z": z, "p_raw": p})
    adj = holm([r["p_raw"] for r in res])
    for r, pa in zip(res, adj):
        r["p_raw"] = round(r["p_raw"], 4)
        r["p_holm"] = round(pa, 4)
        r["significant_holm_0.05"] = pa < ALPHA
    return res, counts


def fmt_pct(v):
    return "—" if v in ("", None) or (isinstance(v, float) and math.isnan(v)) else f"{float(v) * 100:.1f}%"


def analyse(args):
    rows = load_events(args.events)
    start = parse_ts(args.start + "T00:00:00+05:30") if args.start else None
    end = parse_ts(args.end + "T00:00:00+05:30") if args.end else None
    visitors, exclusions, log = build_visitors(rows, args.page_version, start, end)
    os.makedirs(args.out, exist_ok=True)
    demo = "DEMO_SYNTHETIC" in os.path.basename(args.events)

    summary = rate_rows("overall", "all", visitors)
    for src in sorted({x["source"] for x in visitors}):
        summary += rate_rows("source", src, [x for x in visitors if x["source"] == src])
    for dev in sorted({x["device"] for x in visitors}):
        summary += rate_rows("device", dev, [x for x in visitors if x["device"] == dev])
    # Segment is only known for CTA clickers who answered the mini-survey -> composition + downstream rates only.
    for field in ("seg_occupation", "seg_freq", "locality"):
        clickers = [x for x in visitors if x["cta"] and x["mini"]]
        for g in sorted({x[field] for x in clickers}):
            summary += [r for r in rate_rows(field, g, [x for x in clickers if x[field] == g]) if r["metric"] in ("secondary_given_cta", "survey_click_given_cta")]

    with open(os.path.join(args.out, "fakedoor_summary.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(summary[0].keys()) if summary else ["scope"])
        w.writeheader()
        w.writerows(summary)

    pw_ctr, counts = pairwise(visitors, "cta_ctr", "cta")
    pw_sec, sec_counts = pairwise(visitors, "secondary_rate", "secondary")
    pw_all = pw_ctr + pw_sec
    fields = ["metric", "pair", "rate_first", "rate_second", "diff_pp", "diff_ci_low_pp", "diff_ci_high_pp", "cohens_h", "test", "z", "p_raw", "p_holm", "significant_holm_0.05"]
    with open(os.path.join(args.out, "fakedoor_pairwise.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(pw_all)

    with open(os.path.join(args.out, "fakedoor_exclusions.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["anon_visitor_id", "variant_id", "exclusion_reason", "n_events"])
        w.writeheader()
        w.writerows(exclusions)

    # Evidence-strength label
    arm_n = [counts[v][1] for v in VARIANTS]
    total_cta = sum(counts[v][0] for v in VARIANTS)
    pooled = total_cta / sum(arm_n) if sum(arm_n) else 0.0
    base = min(max(pooled, 0.02), 0.85)
    need = n_required(base, PLANNING_DELTA, ALPHA / 3)
    label = "CONFIRMATORY" if min(arm_n) >= need else "DIRECTIONAL"
    chi2, srm_p = srm_pvalue(arm_n)
    pb_ctr = p_best({v: counts[v][0] for v in VARIANTS}, {v: counts[v][1] for v in VARIANTS})
    pb_sec = p_best({v: sec_counts[v][0] for v in VARIANTS}, {v: sec_counts[v][1] for v in VARIANTS})

    def overall(metric, v):
        return next(r for r in summary if r["scope"] == "overall" and r["metric"] == metric and r["variant"] == v)

    lines = []
    if demo:
        lines += ["> **DEMO SYNTHETIC DATA — CODE TEST ONLY. These numbers are simulated and must never be reported as findings.**", ""]
    lines += [f"# Fake-door results — {EXPERIMENT_ID}", "",
              f"Input: `{os.path.basename(args.events)}` · page_version: {args.page_version or 'single version'} · generated {datetime.now().strftime('%Y-%m-%d %H:%M')}", "",
              f"## Evidence label: **{label}**", "",
              f"Smallest arm n = {min(arm_n)}; pre-registered requirement to detect +{PLANNING_DELTA * 100:.0f} pp from the pooled CTR of {pooled * 100:.1f}% "
              f"at α = 0.05/3 (Holm first step), power 0.80 = **{need} visitors per arm**. "
              + ("Differences below may be real but this test cannot distinguish them from noise; report as relative behavioural signal only." if label == "DIRECTIONAL" else "Sample meets the pre-registered requirement."), "",
              "## Data quality", "",
              "| Check | Value |", "|---|---|"]
    for k, v in log.items():
        lines.append(f"| {k} | {v} |")
    lines += [f"| Sample-ratio mismatch χ² (df=2) | {chi2:.2f}, p = {srm_p:.4f} {'⚠ INVESTIGATE assignment/tracking before interpreting' if srm_p < SRM_ALPHA else '(ok)'} |", "",
              "## Funnel by variant (unique visitors; Wilson 95% CI)", "",
              "| Metric | " + " | ".join(f"{v} · {VARIANT_KEYS[v]}" for v in VARIANTS) + " |", "|---|" + "---|" * len(VARIANTS)]
    for metric, _, _, lab in METRICS:
        cells = []
        for v in VARIANTS:
            r = overall(metric, v)
            cells.append(f"{fmt_pct(r['rate'])} ({r['x']}/{r['n']}) [{fmt_pct(r['ci_low'])}–{fmt_pct(r['ci_high'])}]")
        lines.append(f"| {lab} | " + " | ".join(cells) + " |")
    ttc = {v: sorted(x["time_to_cta"] for x in visitors if x["variant"] == v and x["time_to_cta"] is not None) for v in VARIANTS}
    lines.append("| Median time to CTA (s) | " + " | ".join(f"{median(ttc[v]) / 1000:.1f} (n={len(ttc[v])})" if ttc[v] else "—" for v in VARIANTS) + " |")
    gaps = {v: [x["bill_gap_pct"] for x in visitors if x["variant"] == v and isinstance(x["bill_gap_pct"], (int, float))] for v in VARIANTS}
    lines.append("| Self-reported last-bill gap, median % (bill-compare users) | " + " | ".join(f"{median(gaps[v]):.0f}% (n={len(gaps[v])})" if gaps[v] else "—" for v in VARIANTS) + " |")
    lines += ["", "## Pairwise comparisons (Holm-adjusted within each metric)", "",
              "| Metric | Pair | Diff (pp) | 95% CI (pp) | Cohen's h | Test | p raw | p Holm |", "|---|---|---|---|---|---|---|---|"]
    for r in pw_all:
        if r.get("test") == "n/a":
            continue
        lines.append(f"| {r['metric']} | {r['pair']} | {r['diff_pp']:+.1f} | {r['diff_ci_low_pp']:+.1f} to {r['diff_ci_high_pp']:+.1f} | {r['cohens_h']:+.2f} | {r['test']} | {r['p_raw']} | {r['p_holm']} |")
    lines += ["", "## Probability each variant is best (Beta(1,1) prior, descriptive only — not a decision rule)", "",
              "| Metric | " + " | ".join(VARIANTS) + " |", "|---|" + "---|" * len(VARIANTS),
              "| CTA CTR | " + " | ".join(f"{pb_ctr[v] * 100:.0f}%" for v in VARIANTS) + " |",
              "| Bill-compare rate | " + " | ".join(f"{pb_sec[v] * 100:.0f}%" for v in VARIANTS) + " |", "",
              "## Reading rules (pre-registered)", "",
              "- Declare a *winner* only if Holm-adjusted p < 0.05 on CTA CTR **and** the label is CONFIRMATORY. Otherwise say \"Variant X led directionally\".",
              "- Business relevance requires ≥ +5 pp absolute CTR difference even when significant.",
              "- Segment cuts use mini-survey answers, which exist only for CTA clickers who opted in: they describe *who clicked*, not segment-level CTR.",
              "- Source-level rows with n < 30 per arm are descriptive only.",
              "- Behavioural intent here ≠ adoption or purchase. Triangulate with survey (brand-blind concept, framing item) and interviews before using in the market-fit scorecard."]
    with open(os.path.join(args.out, "fakedoor_report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines[:12]))
    print(f"\nWrote outputs to {args.out}")


# ============================== synthetic fixture (code test only) ==============================
def make_demo(args):
    path = os.path.abspath(args.path)
    if "DEMO_SYNTHETIC" not in os.path.basename(path):
        sys.exit("Refusing: synthetic fixture file name must contain 'DEMO_SYNTHETIC'.")
    if "08_clean_data" in path:
        sys.exit("Refusing: synthetic data must never be written inside 08_clean_data.")
    rng = random.Random(SEED)
    true_ctr = {"A": 0.14, "B": 0.17, "C": 0.12}  # arbitrary test values, meaningless
    cols = ["received_at", "experiment_id", "page_version", "variant_id", "variant_key", "anon_visitor_id", "anon_session_id", "event_name", "ts",
            "time_since_load_ms", "utm_source", "utm_medium", "utm_campaign", "utm_content", "referrer_domain", "device_type", "is_qa", "is_bot_suspect", "payload_json"]
    sources = [("whatsapp", "community_group"), ("linkedin", "post"), ("instagram", "story"), ("qr_poster", "offline"), ("", "")]
    t_start = datetime(2026, 9, 16, 6, 0, tzinfo=timezone.utc)
    out = []
    for i in range(args.visitors):
        vid, sid = str(uuid.UUID(int=rng.getrandbits(128))), str(uuid.UUID(int=rng.getrandbits(128)))
        v = rng.choice(VARIANTS)
        src, med = rng.choice(sources)
        qa = i < 6
        bot = 6 <= i < 10
        t = t_start + timedelta(minutes=rng.randint(0, 60 * 24 * 9))
        base = {"experiment_id": EXPERIMENT_ID, "page_version": "2026-09-14.1", "variant_id": v, "variant_key": VARIANT_KEYS[v], "anon_visitor_id": vid,
                "anon_session_id": sid, "utm_source": src, "utm_medium": med, "utm_campaign": EXPERIMENT_ID if src else "", "utm_content": "",
                "referrer_domain": "", "device_type": rng.choice(["mobile"] * 8 + ["desktop", "tablet"]), "is_qa": str(qa).lower(), "is_bot_suspect": str(bot).lower()}

        def emit(name, ms, payload=None):
            ts = (t + timedelta(milliseconds=ms)).isoformat().replace("+00:00", "Z")
            out.append({**base, "received_at": ts, "event_name": name, "ts": ts, "time_since_load_ms": ms, "payload_json": json.dumps(payload or {})})

        emit("page_view", 0, {"viewport_w": 390})
        dwell = rng.randint(2000, 90000)
        if dwell > 3500:
            emit("vp_view", 3200, {"trigger": "hero_visible_3s"})
        if rng.random() < 0.45:
            emit("scroll_50", rng.randint(4000, 20000), {"pct": 55})
        if rng.random() < true_ctr[v]:
            ms = 600 if i % 97 == 0 else rng.randint(4000, 60000)
            emit("cta_click", ms, {"cta_position": rng.choice(["hero", "bottom"])})
            emit("disclosure_view", ms + 50, {"from": "hero"})
            if rng.random() < 0.35:
                food = rng.randint(150, 600)
                fin = int(food * rng.uniform(1.05, 1.45))
                emit("secondary_intent", ms + 20000, {"action": "bill_compare", "bill_food": food, "bill_final": fin, "bill_gap_inr": fin - food, "bill_gap_pct": round((fin - food) / food * 100)})
            else:
                emit("secondary_skip", ms + 5000)
            if rng.random() < 0.6:
                emit("mini_survey_submit", ms + 40000, {"seg_occupation": rng.choice(["student", "working_professional", "working_student"]),
                                                        "locality": rng.choice(["gachibowli", "kondapur", "hitec_city_madhapur"]),
                                                        "orders_4wk": rng.choice(["1_3", "4_7", "8_plus"])})
        emit("exit", dwell, {"dwell_ms": dwell, "max_scroll_pct": 60, "furthest_step": "landing"})
    out += out[:5]  # a few exact duplicates to exercise dedup
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(out)
    print(f"Wrote {len(out)} SYNTHETIC events for {args.visitors} fake visitors to {path} (code test only).")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("analyse")
    a.add_argument("--events", required=True)
    a.add_argument("--out", required=True)
    a.add_argument("--page-version")
    a.add_argument("--start", help="YYYY-MM-DD (IST) inclusive")
    a.add_argument("--end", help="YYYY-MM-DD (IST) exclusive")
    d = sub.add_parser("make-demo")
    d.add_argument("--path", required=True)
    d.add_argument("--visitors", type=int, default=600)
    args = ap.parse_args()
    analyse(args) if args.cmd == "analyse" else make_demo(args)


if __name__ == "__main__":
    main()
