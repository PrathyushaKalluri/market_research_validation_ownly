"""Step 12: fake-door funnel per variant (07_fake_door/experiment_plan.md sections 8-13; H11).

Unit of analysis: anon_visitor_id (first variant assignment wins). Excluded: is_qa, is_bot_suspect,
time-to-CTA < 500 ms (EXF1_bot). Wilson CIs; pairwise two-proportion/Fisher with Holm; Beta(1,1)
P(best) by simulation (descriptive only). DIRECTIONAL if per-arm n is below the n needed to detect
+10 pp at the observed pooled baseline with alpha = 0.05/3 and power 0.80.
Outputs: MART_DIR/fact_fakedoor_events.csv, agg_fakedoor_variant.csv; OUT_ROOT/fakedoor_pairwise.csv
"""
from __future__ import annotations

import itertools
import json
from math import ceil, sqrt

import numpy as np
import pandas as pd
from scipy import stats

import config as C
import utils_io as io
import utils_stats as st


def n_required(p1, d, alpha=0.05 / 3, power=0.8):
    p2 = min(p1 + d, 0.999)
    za, zb = stats.norm.ppf(1 - alpha / 2), stats.norm.ppf(power)
    pbar = (p1 + p2) / 2
    return ceil((za * sqrt(2 * pbar * (1 - pbar)) + zb * sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 / (p2 - p1) ** 2)


def mde(n, p1):
    for d in np.arange(0.01, 0.6, 0.005):
        if n_required(p1, d) <= n:
            return round(float(d), 3)
    return np.nan


def truthy(s):
    return s.astype(str).str.lower().isin(["true", "1", "yes"])


def main():
    if not C.FAKEDOOR_FILE.exists() and not io.tag(C.FAKEDOOR_FILE).exists():
        print(f"  no fake-door events at {C.FAKEDOOR_FILE} — skipping")
        return
    ev = io.read_csv(C.FAKEDOOR_FILE)
    ev["is_qa"] = truthy(ev.get("is_qa", pd.Series(False, index=ev.index)))
    ev["is_bot_suspect"] = truthy(ev.get("is_bot_suspect", pd.Series(False, index=ev.index)))
    ev["time_since_load_ms"] = pd.to_numeric(ev.time_since_load_ms, errors="coerce")
    if "payload" in ev:
        pl = ev.payload.fillna("{}").map(lambda s: json.loads(s) if str(s).startswith("{") else {})
        for k in ("seg_occupation", "locality", "orders_4wk"):
            ev[f"mini_{k}"] = pl.map(lambda d: d.get(k))
    first_variant = ev.sort_values("ts").groupby("anon_visitor_id").variant_id.first()
    ev["variant_id"] = ev.anon_visitor_id.map(first_variant)
    ttc = ev[ev.event_name == "cta_click"].groupby("anon_visitor_id").time_since_load_ms.min()
    bots = set(ttc[ttc < 500].index)
    ev["excluded_reason"] = np.select([ev.is_qa, ev.is_bot_suspect, ev.anon_visitor_id.isin(bots)],
                                      ["EXF0_qa", "EXF1_bot", "EXF1_bot"], default="")
    io.write_csv(io.stamp(pd.DataFrame({
        "event_id": range(1, len(ev) + 1), "event_ts": ev.ts, "experiment_id": ev.experiment_id,
        "variant_id": ev.variant_id, "session_id": ev.anon_visitor_id, "event_name": ev.event_name,
        "utm_source": ev.get("utm_source"), "utm_medium": ev.get("utm_medium"), "utm_campaign": ev.get("utm_campaign"),
        "utm_content": ev.get("utm_content"), "referrer_domain": ev.get("referrer_domain"),
        "device_type": ev.get("device_type"), "ms_since_page_view": ev.time_since_load_ms,
        "mini_q_seg_occupation": ev.get("mini_seg_occupation"), "mini_q_locality": ev.get("mini_locality"),
        "mini_q_orders_4wk": ev.get("mini_orders_4wk"), "is_bot_suspect": ev.is_bot_suspect,
        "is_internal": ev.is_qa, "excluded_reason": ev.excluded_reason})), C.MART_DIR / "fact_fakedoor_events.csv")

    e = ev[ev.excluded_reason == ""]
    vis = e.groupby("anon_visitor_id").agg(
        experiment_id=("experiment_id", "first"), variant_id=("variant_id", "first"),
        vp=("event_name", lambda s: s.isin(["vp_view", "cta_click"]).any()),
        cta=("event_name", lambda s: (s == "cta_click").any()),
        secondary=("event_name", lambda s: (s == "secondary_intent").any()),
        disclosure=("event_name", lambda s: (s == "disclosure_view").any()),
        scroll=("event_name", lambda s: (s == "scroll_50").any()),
        utm_source=("utm_source", "first"))
    vis["time_to_cta"] = ttc.reindex(vis.index)
    vis["bounce"] = ~vis.cta & ~vis.scroll
    base_p = max(vis.cta.mean(), 0.01)
    agg = []
    for (vid, src), g in pd.concat([vis.assign(src="all"), vis.assign(src=vis.utm_source.fillna("(direct/none)"))]).groupby(["variant_id", "src"]):
        n = len(g)
        ctr, clo, chi = st.wilson(int(g.cta.sum()), n)
        hc, hlo, hhi = st.wilson(int(g.secondary.sum()), n)
        need = n_required(base_p, 0.10)
        agg.append({"experiment_id": g.experiment_id.iloc[0], "variant_id": vid, "utm_source": src, "unique_sessions": n,
                    "proposition_views": int(g.vp.sum()), "cta_clicks": int(g.cta.sum()),
                    "high_intent_actions": int(g.secondary.sum()), "disclosure_views": int(g.disclosure.sum()),
                    "bounces": int(g.bounce.sum()), "ctr": ctr, "ctr_ci_low": clo, "ctr_ci_high": chi,
                    "hi_conv": hc, "hi_conv_ci_low": hlo, "hi_conv_ci_high": hhi, "bounce_rate": g.bounce.mean(),
                    "median_time_to_cta_ms": g.time_to_cta.median(), "mde_at_80_power": mde(n, base_p),
                    "n_required_for_10pp": need, "directional_only": n < need})
    io.write_csv(io.stamp(pd.DataFrame(agg)), C.MART_DIR / "agg_fakedoor_variant.csv")

    pw = []
    arms = {v: g for v, g in vis.groupby("variant_id")}
    for metric in ("cta", "secondary"):
        tmp = []
        for a, b in itertools.combinations(sorted(arms), 2):
            ga, gb = arms[a], arms[b]
            test, p = st.two_prop_test(int(ga[metric].sum()), len(ga), int(gb[metric].sum()), len(gb))
            d, lo, hi = st.newcombe_diff(int(ga[metric].sum()), len(ga), int(gb[metric].sum()), len(gb))
            tmp.append({"metric": metric, "arm_a": a, "arm_b": b, "diff_pp": d, "ci_low": lo, "ci_high": hi,
                        "test": test, "p": p})
        for row, ph in zip(tmp, st.holm([t["p"] for t in tmp])):
            row["p_holm"] = ph
            pw.append(row)
        g = st.rng(1200)
        draws = np.column_stack([g.beta(1 + arms[v][metric].sum(), 1 + len(arms[v]) - arms[v][metric].sum(), 20000) for v in sorted(arms)])
        best = np.bincount(draws.argmax(axis=1), minlength=len(arms)) / 20000
        for v, pb in zip(sorted(arms), best):
            pw.append({"metric": metric, "arm_a": v, "arm_b": "P(best)", "diff_pp": pb, "test": "beta_binomial_descriptive"})
    io.write_csv(io.stamp(pd.DataFrame(pw)), C.OUT_ROOT / "fakedoor_pairwise.csv")


if __name__ == "__main__":
    main()
