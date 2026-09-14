"""DEMO_SYNTHETIC survey-export generator (test fixture ONLY — never real data, never in project folders).

Builds Google-Forms-like exports (question-text headers, label answers) from the canonical
dictionary + form_column_map template so that 01_ingest_and_harmonise.py is exercised end-to-end.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd

import utils_survey as us

IST = timezone(timedelta(hours=5, minutes=30))
BETA = {"student": dict(price=-0.035, eta=-0.03, late3=-0.7, rest_few=-0.9, rest_some=-0.35, refund_case=-0.25),
        "working_professional": dict(price=-0.025, eta=-0.05, late3=-1.1, rest_few=-1.2, rest_some=-0.45, refund_case=-0.35)}


def clip5(x):
    return int(np.clip(round(x), 1, 5))


def gen_city(city, versions, n_per_version, fmap, dic, design, g, start_index=0):
    codes = {r.variable_name: us.parse_codes(r.values_codes, city) for _, r in dic.iterrows()}
    rows = []
    for version in versions:
        cols = fmap[fmap.form_family.isin(["both", city, version])]
        if city == "blr":
            cols = cols[~cols.kind.eq("dce")]
        for i in range(n_per_version):
            a = latent(city, version, g)
            row = {}
            for _, spec in cols.iterrows():
                row[spec.expected_header] = answer(spec, a, codes, design, g)
            rows.append(row)
    df = pd.DataFrame(rows)
    # inject 2 exact duplicates (same token) to exercise EX05
    if len(df) > 10:
        df = pd.concat([df, df.iloc[[3, 7]]], ignore_index=True)
    return df


def latent(city, version, g):
    occ = g.choice([1, 2, 3, 4, 5], p=[.25, .2, .45, .07, .03])
    seg = "student" if occ in (1, 2, 4) else "working_professional"
    screened_out = g.random() < 0.06
    aware = g.random() < (0.55 if city == "blr" else 0.4)
    tried = aware and g.random() < (0.6 if city == "blr" else 0.3)
    submit = datetime(2026, 9, 17, 9, tzinfo=IST) + timedelta(minutes=int(g.integers(0, 14 * 24 * 60)))
    dur = float(np.exp(g.normal(np.log(620), 0.35))) if g.random() > 0.05 else float(g.uniform(90, 180))
    return dict(city=city, version=version, occ=occ, seg=seg, z=g.normal(0.35 if seg == "student" else 0, 1),
                rel_z=g.normal(0, 1), out=screened_out, aware=aware, tried=tried,
                wtp=g.normal(25 if seg == "student" else 35, 15), submit=submit, dur=dur, token=str(uuid.uuid4()),
                branded=us.ARM_OF.get(version) == "branded", block=us.BLOCK_OF.get(version),
                start=us.WTP_START_OF[version], orders=int(g.choice([1, 2, 3, 4], p=[.25, .35, .3, .1])))


def label_for(codes, code):
    for c, lab in codes:
        if c == code:
            return lab
    return str(code)


def answer(spec, a, codes, design, g):
    var, kind = spec.variable_name, spec.kind
    cl = codes.get(var, [])
    screener = var in ("meta_consent", "scr_age_band", "scr_area", "scr_orders_4wk", "scr_coi", "scr_repeat")
    if kind == "timestamp":
        return a["submit"].strftime("%d/%m/%Y %H:%M:%S")
    if var == "meta_form_version":
        return a["version"]
    if var == "meta_session_token":
        return a["token"]
    if var == "meta_start_ts":
        return str(int((a["submit"].timestamp() - a["dur"]) * 1000))
    if var in ("meta_source", "meta_campaign"):
        return g.choice(["whatsapp", "linkedin", "reddit", "campus_group"])
    if a["out"] and not screener:
        return ""
    if screener:
        return label_for(cl, {"meta_consent": 1, "scr_age_band": 6 if a["out"] else int(g.integers(2, 6)),
                              "scr_area": int(g.integers(1, 9)) if a["city"] == "hyd" else int(g.integers(1, 11)),
                              "scr_orders_4wk": a["orders"], "scr_coi": 0, "scr_repeat": 0}[var])
    z, rz = a["z"], a["rel_z"]
    likert = {"pain_fee_reconsider_freq": 3 + z, "pain_bill_unreasonable_freq": 3 + 0.9 * z,
              "beh_abandon_price_freq": 2.4 + 0.8 * z, "pain_menu_markup_belief": 3.4 + 0.6 * z,
              "pain_late_freq": 2.6 + rz, "pain_cancel_freq": 2 + 0.6 * rz, "pain_wrong_item_freq": 2 + 0.5 * rz,
              "pain_restaurant_unavailable_freq": 2.5, "pain_quality_freq": 2.2, "dec_habit_lock": 3.2 - 0.5 * z,
              "bt_trial_intent": 3 + 0.5 * z + 0.3 * a["branded"], "br_trial_intent": 3.2 + 0.5 * z,
              "exp_fav_restaurant_needed": 3 + 0.3 * rz, "bt_appeal": 3.3 + 0.4 * z, "bt_trust": 3,
              "own_reliability_rating": 3.4 - 0.6 * rz, "own_found_restaurants": 3.5, "own_order_accuracy": 4,
              "own_trust": 3.5, "own_continue_intent": 3.5, "own_perceived_savings": 3.8}
    if var == "att_check_1":
        return label_for(cl, 2) if g.random() > 0.04 else "Often"
    if var in likert:
        return label_for(cl, clip5(likert[var] + g.normal(0, 0.8)))
    if var == "seg_occupation_raw":
        return label_for(cl, a["occ"])
    if var == "dem_institution" and a["occ"] not in (1, 2, 4):
        return ""
    if var == "dem_work_sector" and a["occ"] not in (3, 4):
        return ""
    if var.startswith("br_") and a["branded"]:
        return ""
    if var == "own_aware_aided":
        return label_for(cl, 2 if a["aware"] else 0)
    if var == "own_tried":
        return "" if not a["aware"] else label_for(cl, 2 if a["tried"] else 0)
    if var in ("own_aware_duration", "own_aware_source") and not a["aware"]:
        return ""
    if var == "own_not_tried_reason" and (not a["aware"] or a["tried"]):
        return ""
    if var.startswith(("own_", "churn_")) and var not in ("own_aware_aided", "own_tried", "own_aware_duration",
                                                          "own_aware_source", "own_not_tried_reason", "own_trust") and not a["tried"]:
        return ""
    if kind == "dce":
        return dce_answer(var, a, design, g)
    if kind == "wtp":
        return wtp_answer(int(var.split("_")[-1]), a)
    if kind == "bill":
        return g.choice(["Bill 1", "Bill 2", "No real difference to me"], p=[.4, .4, .2]) if var in ("bill_s1", "bill_s2") \
            else g.choice(["Bill 1", "Bill 2"])
    if kind == "number":
        if var in ("beh_last_order_total", "own_last_total"):
            return str(int(np.exp(g.normal(np.log(290), 0.45))))
        return str(int(g.normal(25, 30))) if g.random() > 0.4 else ""
    if kind == "text":
        if var == "beh_unaided_apps":
            return "Swiggy, Zomato" + (", Ownly" if a["aware"] and g.random() < .5 else "")
        return g.choice(["", "", "fees keep going up", "late delivery again", "restaurant not available", "asdfgh"], p=[.35, .25, .15, .15, .09, .01])
    if kind == "checkbox":
        opts = [lab for _, lab in cl]
        if not opts:
            return ""
        k = int(g.integers(1, 4))
        return ", ".join(g.choice(opts, size=min(k, len(opts)), replace=False))
    numeric = [c for c, _ in cl if c is not None and c not in (98, 99)]
    return label_for(cl, int(g.choice(numeric))) if numeric else ""


def dce_answer(var, a, design, g):
    if a["block"] is None:
        return ""
    task = var.replace("dce_", "")
    t = design[(design.block == a["block"]) & (design.task == task)].set_index("alt")
    if t.empty:
        return ""
    b = BETA[a["seg"]]

    def u(r):
        return (b["price"] * r.price + b["eta"] * r.eta_min + b["late3"] * (r.late_in_10 == 3)
                + b["rest_few"] * (r.restaurants == "few") + b["rest_some"] * (r.restaurants == "some")
                + b["refund_case"] * (r.refund == "case_by_case"))
    pa = 1 / (1 + np.exp(-(u(t.loc["A"]) - u(t.loc["B"]))))
    return "App A" if g.random() < pa else "App B"


def wtp_answer(fee, a):
    wtp, start = a["wtp"], a["start"]
    path, f = [start], start
    if start <= wtp:
        while f < 60 and f + 10 <= wtp:
            f += 10
            path.append(f)
        if f < 60:
            path.append(f + 10)
    else:
        while f > 0 and f - 10 > wtp:
            f -= 10
            path.append(f)
        if f > 0:
            path.append(f - 10)
    if fee not in path:
        return ""
    return "Yes, I would order" if fee <= wtp else "No"
