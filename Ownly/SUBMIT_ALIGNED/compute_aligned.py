#!/usr/bin/env python3
"""
Ownly Gachibowli — pre-registration-aligned computation.

Computes the KPI set defined in 09_analysis/kpi_system/metric_dictionary.md
(K00–K94), then applies the threshold rules in
09_analysis/kpi_system/decision_rules.md v1.0 (fixed 2026-09-16, before data)
to produce:

  * the six-element Transferability Matrix verdicts   (decision_rules §2)
  * the four guardrail states G1–G4                   (decision_rules §3.1)
  * the Overall Hyderabad call                        (decision_rules §3)

Every output row carries FULL PROVENANCE: the pre-registered formula verbatim,
the calculation actually applied with its numbers, the source file and columns,
the evidence label, and — where a KPI could not be computed — the reason.

Nothing is imputed. A KPI with no source question is NOT COMPUTABLE, and a rule
that depends on it returns INSUFFICIENT EVIDENCE rather than a guess.

Run:  python3 compute_aligned.py
"""

import csv, json, math, os, random, re, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FD = os.path.join(ROOT, "final_dashboard", "data")
KS = os.path.join(ROOT, "09_analysis", "kpi_system")
OUT = os.path.join(HERE, "Data")
os.makedirs(OUT, exist_ok=True)

def rd(p):
    with open(p, encoding="utf-8", errors="replace") as f:
        return list(csv.DictReader(f))

def num(v, d=None):
    try:
        if v is None or str(v).strip() == "": return d
        return float(str(v).replace(",", "").replace("₹", "").replace("%", "").strip())
    except Exception:
        return d

def truthy(v): return str(v).strip().lower() in ("true", "1", "yes", "y")

def median(xs):
    s = sorted(x for x in xs if x is not None)
    if not s: return None
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2

def wilson(k, n, z=1.959963985):
    if not n: return (None, None, None)
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(100 * p, 1), round(100 * max(0, c - h), 1), round(100 * min(1, c + h), 1))

def boot_median_ci(xs, iters=10000, seed=20260921):
    """Percentile bootstrap CI for a median. Deterministic seed so reruns match."""
    s = [x for x in xs if x is not None]
    if len(s) < 2: return (None, None)
    rng = random.Random(seed)
    meds = []
    for _ in range(iters):
        meds.append(median([s[rng.randrange(len(s))] for _ in range(len(s))]))
    meds.sort()
    return (round(meds[int(.025 * iters)], 2), round(meds[int(.975 * iters)], 2))

# ── load ────────────────────────────────────────────────────────────
clean = rd(os.path.join(FD, "cleaned_survey.csv"))
cat = [r for r in clean if truthy(r.get("in_catchment"))]
audit = rd(os.path.join(FD, "audit_clean.csv"))
pairs = rd(os.path.join(FD, "audit_pairs.csv"))
cover = rd(os.path.join(FD, "audit_coverage.csv"))
prereg = rd(os.path.join(OUT, "00_kpi_dictionary_prereg.csv"))
PR = {r["kpi_id"]: r for r in prereg}

N = len(cat)
print(f"catchment n = {N}")

# ── KPI results collector ───────────────────────────────────────────
K = {}
ROWS = []

def emit(kid, value, unit, n, status, applied, src_file, src_cols,
         ci=(None, None), why=""):
    d = PR.get(kid, {})
    K[kid] = {"value": value, "n": n, "status": status, "ci_lo": ci[0], "ci_hi": ci[1]}
    ROWS.append({
        "KPI ID": kid,
        "Name": d.get("name", ""),
        "Layer": d.get("layer", ""),
        "Priority": d.get("priority", ""),
        "Guardrail": d.get("guardrail", ""),
        "North Star": d.get("north_star", "No"),
        "Status": status,
        "Value": "" if value is None else value,
        "Unit": unit,
        "N": "" if n is None else n,
        "CI Low": "" if ci[0] is None else ci[0],
        "CI High": "" if ci[1] is None else ci[1],
        "Pre-registered formula": d.get("formula", ""),
        "Calculation applied": applied,
        "Source file": src_file,
        "Source columns": src_cols,
        "Evidence label": d.get("evidence_level", ""),
        "Pre-registered source": d.get("source", ""),
        "Why not computable": why,
        "Decision it serves": d.get("decision", ""),
    })

# ══════════════════ LAYER 0–1 ══════════════════
aware = sum(1 for r in cat if truthy(r.get("ownly_aware")))
opened = sum(1 for r in cat if truthy(r.get("ownly_opened")))
tried = sum(1 for r in cat if truthy(r.get("ownly_says_ordered")))

p, lo, hi = wilson(aware, N)
emit("K10", p, "%", N, "COMPUTED",
     f"count(ownly_aware = True) / catchment = {aware}/{N}; Wilson 95% CI",
     "final_dashboard/data/cleaned_survey.csv", "ownly_aware, in_catchment", (lo, hi))

p, lo, hi = wilson(tried, N)
emit("K01", p, "%", N, "COMPUTED (LOW BASE)",
     f"count(ownly_says_ordered = True) / catchment = {tried}/{N}",
     "final_dashboard/data/cleaned_survey.csv", "ownly_says_ordered, in_catchment", (lo, hi),
     "Base is 2 respondents; interval spans 1.4–16.5%. Directional only.")

p, lo, hi = wilson(tried, aware) if aware else (None, None, None)
emit("K11", p, "%", aware, "COMPUTED (LOW BASE)",
     f"count(tried) / count(aware) = {tried}/{aware}",
     "final_dashboard/data/cleaned_survey.csv", "ownly_says_ordered, ownly_aware", (lo, hi),
     "Numerator is 2. Not interpretable as a conversion rate.")

p, lo, hi = wilson(tried, opened) if opened else (None, None, None)
emit("K12", p, "%", opened, "COMPUTED (LOW BASE)",
     f"count(tried) / count(opened) = {tried}/{opened}",
     "final_dashboard/data/cleaned_survey.csv", "ownly_says_ordered, ownly_opened", (lo, hi),
     "Numerator is 2.")

emit("K00", None, "per 100", None, "NOT COMPUTABLE",
     "—", "—", "—", (None, None),
     "North-star proxy needs repeat-active Ownly customers. Only 2 catchment respondents report "
     "any Ownly order and their order counts contradict their own other answers (see anomalies.csv). "
     "No survey question substitutes for observed repeat behaviour.")

# ── H0 tests (decision_rules §1) ──
emit("K13", None, "%", 0, "NOT FIELDED",
     "—", "07_fake_door/prototype/index.html (built, collector verified)", "—", (None, None),
     "Fake-door experiment was designed, built and powered but never given traffic. Event log has 0 rows. "
     "decision_rules §1 therefore makes K14 the primary H0 test.")

fp = [r for r in cat if (r.get("prop_forced") or "").strip()]
def _pq(v):
    """Live instrument stores 'Service P' / 'Service Q' / "I genuinely can't choose between them"."""
    t = (v or "").strip().lower()
    if t.endswith("service p") or t == "p": return "P"
    if t.endswith("service q") or t == "q": return "Q"
    return "CANT"
cP = sum(1 for r in fp if _pq(r.get("prop_forced")) == "P")
cQ = sum(1 for r in fp if _pq(r.get("prop_forced")) == "Q")
cCant = len(fp) - cP - cQ
denomPQ = cP + cQ
p, lo, hi = wilson(cQ, denomPQ) if denomPQ else (None, None, None)
emit("K14", p, "%", denomPQ, "COMPUTED",
     f"count(prop_forced = Q) / count(prop_forced in P,Q) = {cQ}/{denomPQ}. "
     f"'Can't choose' = {cCant} of {len(fp)} = {round(100*cCant/len(fp),1) if fp else 0}%, reported separately per the pre-registered formula",
     "final_dashboard/data/cleaned_survey.csv", "prop_forced", (lo, hi))

# ══════════════════ LAYER 2 · VALUE ══════════════════
lf = [r for r in pairs if r.get("view") == "LIST+FEES"]
sav_pct = [num(r.get("saving_pct")) for r in lf]
sav_rs = [num(r.get("saving_rs")) for r in lf]
k20 = median(sav_pct)
k20_rs = median(sav_rs)
ci20 = boot_median_ci(sav_pct)
emit("K20", round(k20, 1), "%", len(lf), "COMPUTED (n=4)",
     f"(min(Swiggy,Zomato final_payable) − Ownly final_payable) / min(...) per matched set; "
     f"median of {[round(x,1) for x in sav_pct]} = {round(k20,1)}%. "
     f"Median in rupees = ₹{k20_rs:.2f}. 95% CI by percentile bootstrap, 10,000 resamples, seed 20260921",
     "final_dashboard/data/audit_pairs.csv", "view=LIST+FEES, saving_pct, saving_rs", ci20,
     "")

winr = sum(1 for r in lf if (num(r.get("saving_rs")) or 0) > 5)
p, lo, hi = wilson(winr, len(lf))
emit("K21", p, "%", len(lf), "COMPUTED (n=4)",
     f"count(Ownly cheapest by more than ₹5) / matched sets = {winr}/{len(lf)}",
     "final_dashboard/data/audit_pairs.csv", "view=LIST+FEES, saving_rs", (lo, hi))

feeshare = {}
for a in audit:
    if a.get("priced") != "True": continue
    if (num(a.get("discount_amount"), 0) or 0) != 0: continue
    s = num(a.get("non_food_share"))
    if s is None: continue
    feeshare.setdefault(a.get("platform"), []).append(100 * s)
own_fee = median(feeshare.get("ownly", []))
inc_fee = median([v for p2 in ("swiggy", "zomato") for v in feeshare.get(p2, [])])
emit("K22", round(own_fee, 1), "%", len(feeshare.get("ownly", [])), "COMPUTED",
     f"non-food charges / final_payable, median across zero-discount priced captures. "
     f"Ownly = {own_fee:.1f}% (n={len(feeshare.get('ownly',[]))}); "
     f"incumbent pooled median = {inc_fee:.1f}% "
     f"(swiggy n={len(feeshare.get('swiggy',[]))}, zomato n={len(feeshare.get('zomato',[]))}). "
     f"Fee-load gap = {inc_fee-own_fee:.1f} pp",
     "final_dashboard/data/audit_clean.csv",
     "platform, non_food_share, discount_amount=0, priced=True")
K["K22_gap"] = {"value": round(inc_fee - own_fee, 1)}
K["K22_incumbent"] = {"value": round(inc_fee, 1)}

thr = [num(r.get("switch_savings_rs")) for r in cat if num(r.get("switch_savings_rs")) is not None]
never = sum(1 for r in cat if truthy(r.get("switch_never")))
dk = sum(1 for r in cat if truthy(r.get("switch_dk")))
k23_k = sum(1 for t in thr if t <= k20_rs)
p, lo, hi = wilson(k23_k, len(thr))
emit("K23", p, "%", len(thr), "COMPUTED",
     f"count(stated required saving ≤ K20 median of ₹{k20_rs:.2f}) / count(numeric answers) = {k23_k}/{len(thr)}. "
     f"Held out and reported separately per the pre-registered formula: 'no amount' = {never}, \"don't know\" = {dk}",
     "final_dashboard/data/cleaned_survey.csv",
     "switch_savings_rs, switch_never, switch_dk × audit_pairs.saving_rs", (lo, hi))

td = {}
for key, col in [("speed", "eta_chose_cheap"), ("reliability", "rel_chose_cheap"), ("restaurants", "rest_chose_cheap")]:
    k = sum(1 for r in cat if truthy(r.get(col)))
    td[key] = wilson(k, N) + (k,)
emit("K24", td["speed"][0], "%", N, "COMPUTED",
     f"share choosing the ₹230 option at a constant ₹30 saving, by attribute sacrificed. "
     f"speed {td['speed'][3]}/{N} = {td['speed'][0]}%; reliability {td['reliability'][3]}/{N} = {td['reliability'][0]}%; "
     f"restaurants {td['restaurants'][3]}/{N} = {td['restaurants'][0]}%",
     "final_dashboard/data/cleaned_survey.csv",
     "eta_chose_cheap, rel_chose_cheap, rest_chose_cheap", (td["speed"][1], td["speed"][2]))
K["K24_speed"] = {"value": td["speed"][0]}
K["K24_rel"] = {"value": td["reliability"][0]}
K["K24_rest"] = {"value": td["restaurants"][0]}

bf = [(r.get("bill_fairness") or "").strip() for r in cat if (r.get("bill_fairness") or "").strip()]
k25_k = sum(1 for v in bf if v.startswith("No, the extra charges"))
p, lo, hi = wilson(k25_k, len(bf))
emit("K25", p, "%", len(bf), "COMPUTED",
     f'count(bill_fairness = "No, the extra charges on top were too much") / answered = {k25_k}/{len(bf)}',
     "final_dashboard/data/cleaned_survey.csv", "bill_fairness", (lo, hi))

# ══════════════════ LAYER 3 · RETENTION ══════════════════
rep = [num(r.get("repeat_no_promo_n")) for r in cat if num(r.get("repeat_no_promo_n")) is not None]
k32_k = sum(1 for v in rep if v >= 4)
p, lo, hi = wilson(k32_k, len(rep))
emit("K32", p, "%", len(rep), "COMPUTED",
     f"top-2 box on repeat-without-promo (score ≥ 4 of 5) / answered = {k32_k}/{len(rep)}",
     "final_dashboard/data/cleaned_survey.csv", "repeat_no_promo_n", (lo, hi))

pi = [num(r.get("prop_P_intent_n")) for r in cat if num(r.get("prop_P_intent_n")) is not None]
qi = [num(r.get("prop_Q_intent_n")) for r in cat if num(r.get("prop_Q_intent_n")) is not None]
best = [max(a, b) for a, b in zip(pi, qi)] if len(pi) == len(qi) else pi
k15_k = sum(1 for v in best if v >= 4)
p, lo, hi = wilson(k15_k, len(best))
emit("K15", p, "%", len(best), "COMPUTED",
     f"top-2 box trial intent on the better of Service P / Service Q per respondent = {k15_k}/{len(best)}",
     "final_dashboard/data/cleaned_survey.csv", "prop_P_intent_n, prop_Q_intent_n", (lo, hi))

emit("K30", None, "%", tried, "NOT COMPUTABLE",
     "—", "final_dashboard/data/cleaned_survey.csv", "n_ownly, first_order_when", (None, None),
     f"Trier repeat rate needs repeat behaviour among triers. Only {tried} catchment respondents report an Ownly "
     "order, and one of those gives contradictory order counts. Base too small and internally inconsistent.")

emit("K33", None, "%", None, "NOT COMPUTABLE",
     "—", "final_dashboard/data/cleaned_survey.csv", "n_ownly, total_orders_4wk", (None, None),
     "Unit share of requirements among Ownly users requires a usable Ownly order count; the only two are unusable.")

# ══════════════════ LAYER 4 · SUPPLY ══════════════════
on_ownly = sum(1 for r in cover if str(r.get("on_ownly", "")).strip().lower() in ("true", "y", "yes"))
p, lo, hi = wilson(on_ownly, len(cover))
emit("K40", p, "%", len(cover), "COMPUTED",
     f"count(on_ownly = yes) / 10 audit-frame restaurants = {on_ownly}/{len(cover)}",
     "final_dashboard/data/audit_coverage.csv", "restaurant_display, on_ownly", (lo, hi))

emit("K41", None, "pp", None, "NOT COMPUTABLE",
     "—", "final_dashboard/data/audit_coverage.csv", "—", (None, None),
     "coverage(local) − coverage(chain) requires a local/chain flag on the restaurant frame. "
     "audit_coverage.csv carries no such column, so the gap cannot be computed without re-coding the frame.")

ov = [r for r in cover if str(r.get("on_ownly", "")).strip().lower() in ("true", "y", "yes")]
ovi = sum(1 for r in ov if str(r.get("on_incumbent", "")).strip().lower() in ("true", "y", "yes"))
p, lo, hi = wilson(ovi, len(ov))
emit("K42", p, "%", len(ov), "COMPUTED",
     f"count(on Ownly AND on ≥1 incumbent) / count(on Ownly) = {ovi}/{len(ov)}",
     "final_dashboard/data/audit_coverage.csv", "on_ownly, on_incumbent", (lo, hi))

nor = [(r.get("not_opened_reason") or "").strip() for r in cat if (r.get("not_opened_reason") or "").strip()]
k43_k = sum(1 for v in nor if "restaurant" in v.lower())
p, lo, hi = wilson(k43_k, len(nor))
emit("K43", p, "%", len(nor), "COMPUTED (OPTION ABSENT)",
     f'count(reason mentions restaurants) / answered = {k43_k}/{len(nor)}',
     "final_dashboard/data/cleaned_survey.csv", "not_opened_reason", (lo, hi),
     'No respondent selected a missing-restaurants reason. The live instrument\'s answer list for this '
     'question does not appear to offer "My restaurants weren\'t there", so a 0% here measures the option '
     'list, not the barrier. Treated as NOT INFORMATIVE for the rule.')

# ══════════════════ LAYER 5 · FULFILMENT ══════════════════
etas = {}
for a in audit:
    e = num(a.get("eta_mid"))
    if e is None: continue
    etas.setdefault(a.get("platform"), []).append(e)
own_eta = median(etas.get("ownly", []))
inc_eta = median([v for p2 in ("swiggy", "zomato") for v in etas.get(p2, [])])
emit("K50", round(own_eta - inc_eta, 1), "min", sum(len(v) for v in etas.values()), "COMPUTED",
     f"median(Ownly shown ETA) − median(incumbent shown ETA) = {own_eta:.1f} − {inc_eta:.1f} = "
     f"{own_eta-inc_eta:+.1f} min",
     "final_dashboard/data/audit_clean.csv", "platform, eta_mid")

emit("K51", None, "%", None, "NOT COMPUTABLE",
     "—", "—", "—", (None, None),
     "The pre-registered source is 'new question A3' (15+ min late / cancelled / missing or wrong item / "
     "refund or support over 2 days). No such question exists in the live v3 instrument — there is no A3 "
     "variable in cleaned_survey.csv. Guardrail G2 therefore cannot be evaluated.")

emit("K52", None, "pp", None, "NOT COMPUTABLE",
     "—", "—", "—", (None, None),
     "Repeat rate by failure experience depends on K51 (absent) and on a usable trier base (n=2).")

# ══════════════════ LAYER 6 · DISTRIBUTION ══════════════════
rap = sum(1 for r in cat if (r.get("rapido_freq") or "").strip() not in ("", "Never"))
p, lo, hi = wilson(rap, N)
emit("K60", p, "%", N, "COMPUTED",
     f"count(rapido_freq not in blank/Never) / catchment = {rap}/{N}",
     "final_dashboard/data/cleaned_survey.csv", "rapido_freq", (lo, hi))

seen = [(r.get("rapido_food_seen") or "").strip() for r in cat if (r.get("rapido_food_seen") or "").strip()]
seen = [v for v in seen if v != "I don't use the Rapido app"]
k62_k = sum(1 for v in seen if v == "Yes")
p, lo, hi = wilson(k62_k, len(seen))
emit("K62", p, "%", len(seen), "COMPUTED",
     f'count(rapido_food_seen = "Yes") / answered excluding "I don\'t use the Rapido app" = {k62_k}/{len(seen)}. '
     f'"Not sure" counted as not noticed, per the project convention',
     "final_dashboard/data/cleaned_survey.csv", "rapido_food_seen", (lo, hi))

ru = [r for r in cat if (r.get("rapido_freq") or "").strip() not in ("", "Never")]
nu = [r for r in cat if (r.get("rapido_freq") or "").strip() in ("", "Never")]
aw_r = sum(1 for r in ru if truthy(r.get("ownly_aware")))
aw_n = sum(1 for r in nu if truthy(r.get("ownly_aware")))
pr_, lr, hr = wilson(aw_r, len(ru))
pn_, ln, hn = wilson(aw_n, len(nu))
gap = round(pr_ - pn_, 1) if (pr_ is not None and pn_ is not None) else None
gap_lo = round(lr - hn, 1) if None not in (lr, hn) else None
gap_hi = round(hr - ln, 1) if None not in (hr, ln) else None
emit("K61", gap, "pp", N, "COMPUTED (WIDE)",
     f"awareness(Rapido users) − awareness(non-users) = {pr_}% ({aw_r}/{len(ru)}) − {pn_}% ({aw_n}/{len(nu)}) "
     f"= {gap:+.1f} pp. Conservative interval from the difference of the two Wilson bounds",
     "final_dashboard/data/cleaned_survey.csv", "rapido_freq, ownly_aware", (gap_lo, gap_hi),
     "Association, not causation. Both subgroups are small, so the interval on the difference is very wide.")

# ══════════════════ LAYER 7 · PROMO ══════════════════
trig = [(r.get("ownly_trigger") or "").strip() for r in cat if (r.get("ownly_trigger") or "").strip()]
k72_k = sum(1 for v in trig if "discount" in v.lower())
cheaper_k = sum(1 for v in trig if "cheaper" in v.lower())
p, lo, hi = wilson(k72_k, len(trig))
emit("K72", p, "%", len(trig), "COMPUTED",
     f'count(trigger = "A discount on my first order") / answered = {k72_k}/{len(trig)}. '
     f'For comparison, "Seeing it\'s cheaper than Swiggy/Zomato" = {cheaper_k}/{len(trig)} '
     f'= {round(100*cheaper_k/len(trig),1)}% and is the top trigger',
     "final_dashboard/data/cleaned_survey.csv", "ownly_trigger", (lo, hi))
K["K17_top_is_cheaper"] = {"value": cheaper_k / len(trig) if trig else 0}

emit("K70", None, "%", tried, "NOT COMPUTABLE",
     "—", "final_dashboard/data/cleaned_survey.csv", "ownly_trigger among triers", (None, None),
     f"Offer-triggered FIRST ORDER is defined among triers. Only {tried} catchment respondents ordered; "
     "ownly_trigger is answered by non-triers as a hypothetical, so it cannot stand in.")

emit("K71", None, "pp", None, "NOT COMPUTABLE",
     "—", "—", "—", (None, None),
     "Promo-dependency gap = repeat rate of organic triers − repeat rate of offer-acquired triers. "
     "Requires question A2 (acquisition channel) crossed with repeat behaviour among triers. A2 is absent "
     "from the live instrument and the trier base is 2. Guardrail G4 cannot be evaluated.")

# ══════════════════ write KPI table ══════════════════
with open(os.path.join(OUT, "01_kpi_prereg_computed.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(ROWS[0].keys()))
    w.writeheader(); w.writerows(ROWS)

comp = sum(1 for r in ROWS if r["Status"].startswith("COMPUTED"))
print(f"KPIs evaluated: {len(ROWS)}  |  computed: {comp}  |  not computable: {len(ROWS)-comp}")
json.dump(K, open(os.path.join(HERE, "_k.json"), "w"), default=str)
