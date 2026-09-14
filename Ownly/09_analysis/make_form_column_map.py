"""Generate form_column_map_TEMPLATE.csv from the canonical survey dictionary.

The team copies the template to form_column_map.csv and replaces `expected_header`
with the EXACT column headers of each Google Forms export (especially the DCE, bill
and fee-ladder placeholders, which are version-specific).

usage: python make_form_column_map.py [--out PATH]
"""
from __future__ import annotations

import argparse
import re

import pandas as pd

import config as C

GRID_STEM = "In the last 4 weeks, how often did each of these happen to you?"
KIND = {"multiple_choice": "single", "linear_scale_1_5": "single", "linear_scale_1_5_plus_dk": "single",
        "linear_scale_0_10": "single", "grid_row": "single", "checkboxes": "checkbox",
        "checkboxes_max3": "checkbox", "short_answer_number": "number", "paragraph": "text",
        "short_answer_prefilled": "prefill", "google_forms_timestamp": "timestamp"}


def split_city_text(text):
    if text.startswith("HYD:") and "| BLR:" in text:
        hyd, blr = text.split("| BLR:", 1)
        return {"hyd": hyd[4:].strip(), "blr": blr.strip()}
    return None


def build():
    d = pd.read_csv(C.DICT_FILE, dtype=str).fillna("")
    rows = []
    for _, r in d.iterrows():
        var, rt, scope = r.variable_name, r.response_type, r.city_scope
        fam = "hyd" if scope.startswith("hyd") else ("blr" if scope.startswith("blr") else "both")
        if var.startswith("dce_t1"):
            for t in ["t1", "t2", "t3", "t4", "t5", "t6"]:
                rows.append((fam, f"[DCE {t} — paste exact question title of this version]", f"dce_{t}", "dce", "version-specific; Hyderabad only"))
            continue
        if var.startswith("wtp_start"):
            for f in C.WTP_FEES:
                rows.append(("both", f"[FEE LADDER ₹{f} — paste exact question title]", f"wtp_accept_{f}", "wtp", "one section per fee"))
            continue
        if var == "dce_dom":
            rows.append((fam, "[DCE dominance task — paste exact question title]", "dce_dom", "dce", "Hyderabad only"))
            continue
        if var.startswith("bill_s"):
            rows.append((fam, f"[BILL {var[-2:]} — paste exact question title]", var, "bill", "codes: Bill 1 / Bill 2 / No real difference to me (s1, s2 only)"))
            continue
        if rt == "google_forms_timestamp":
            rows.append(("both", "Timestamp", var, "timestamp", "Google Forms system column"))
            continue
        if rt not in KIND:
            continue                                   # derived / text blocks
        text = r.question_text
        if rt == "grid_row":
            row_text = re.sub(r"^\[[^\]]*\]\s*", "", text)
            text = f"{GRID_STEM} [{row_text}]"
        parts = split_city_text(text)
        if parts:
            rows.append(("hyd", parts["hyd"], var, KIND[rt], ""))
            rows.append(("blr", parts["blr"], var, KIND[rt], ""))
        else:
            rows.append((fam, text, var, KIND[rt], ""))
    return pd.DataFrame(rows, columns=["form_family", "expected_header", "variable_name", "kind", "notes"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(C.ANALYSIS_DIR / "form_column_map_TEMPLATE.csv"))
    out = ap.parse_args().out
    m = build()
    m.to_csv(out, index=False)
    print(f"wrote {out} ({len(m)} rows)")
