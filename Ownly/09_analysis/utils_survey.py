"""Survey-specific helpers: value-code parsing, checkbox splitting, fee-ladder
reconstruction, DCE long format, bill-scenario mapping, Ownly status."""
from __future__ import annotations

import re
import unicodedata

import numpy as np
import pandas as pd

import config as C

VERSION_ORDER1 = {"V1", "V3", "B1"}            # bill option order 1
BLOCK_OF = {"V1": 1, "V3": 1, "V2": 2, "V4": 2}   # Bengaluru has no choice tasks (cut 2026-09-14)
WTP_START_OF = {"V1": 20, "V4": 20, "B1": 20, "V2": 40, "V3": 40, "B2": 40}
ARM_OF = {"V1": "blind", "V2": "blind", "V3": "branded", "V4": "branded"}
REST_RANK = {"few": 0, "some": 1, "most": 2}
REFUND_RANK = {"case_by_case": 0, "auto_24h": 1}


def norm(s) -> str:
    s = unicodedata.normalize("NFKC", str(s)).lower()
    s = s.replace("–", "-").replace("—", "-").replace("’", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s).strip()


def slug(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", norm(label)).strip("_")[:40]


# ------------------------------------------------------------ dictionary codes
def city_part(text: str, city: str) -> str:
    t = (text or "").strip()
    if t.upper().startswith("HYD:") and "BLR:" in t:
        hyd, blr = re.split(r";\s*BLR:", t, maxsplit=1)
        return hyd.split(":", 1)[1] if city == "hyd" else blr
    return t


def parse_codes(text: str, city: str):
    """Return list of (code|None, label)."""
    out = []
    for it in [i.strip() for i in city_part(text, city).split(" | ") if i.strip()]:
        m = re.match(r"^(-?\d+)\s*=\s*(.+)$", it)
        if m:
            out.append((int(m.group(1)), m.group(2).strip()))
        elif re.fullmatch(r"-?\d+", it):
            out.append((int(it), it))
        else:
            out.append((None, it))
    return out


def recode_single(series: pd.Series, codes, var: str):
    lookup = {}
    for code, label in codes:
        if code is None:
            continue
        lookup[norm(label)] = code
        lookup[norm(str(code))] = code
    out, unmatched = [], []
    for v in series:
        if pd.isna(v) or str(v).strip() == "":
            out.append(np.nan)
            continue
        key = norm(v)
        if key in lookup:
            out.append(lookup[key])
            continue
        m = re.match(r"^\s*(-?\d+(\.\d+)?)", str(v))     # e.g. "30 minutes" or linear-scale digits
        if m:
            out.append(float(m.group(1)))
        else:
            out.append(np.nan)
            unmatched.append((var, str(v)))
    return pd.Series(out, index=series.index, dtype="float"), unmatched


def split_checkbox(series: pd.Series, options, var: str):
    labels = [lab for _, lab in options]
    cols = {f"{var}__{slug(l)}": np.zeros(len(series), dtype=float) for l in labels}
    other = [""] * len(series)
    unmatched = []
    for i, v in enumerate(series):
        if pd.isna(v) or str(v).strip() == "":
            for c in cols:
                cols[c][i] = np.nan
            continue
        rest = norm(v)
        for lab in sorted(labels, key=len, reverse=True):
            key = norm(lab)
            if key and key in rest:
                cols[f"{var}__{slug(lab)}"][i] = 1
                rest = rest.replace(key, " ", 1)
        leftover = re.sub(r"[,;\s]+", " ", rest).strip()
        if leftover:
            other[i] = leftover
            unmatched.append((var, leftover))
    df = pd.DataFrame(cols, index=series.index)
    df[f"{var}__n_selected"] = df.sum(axis=1, min_count=1)
    df[f"{var}__other_text"] = other
    return df, unmatched


# ------------------------------------------------------------ fee ladder
def reconstruct_ladder(start, answers: dict):
    """Staircase: up on yes / down on no, stop at first reversal (wtp_gabor_granger_design.md)."""
    res = {"wtp_max_fee": np.nan, "wtp_censored_top": 0, "wtp_rejects_all": 0,
           "wtp_path": "", "wtp_status": "ok", "FLAG_wtp_nonmonotone": 0, "FLAG_wtp_orphan_conflict": 0}
    if pd.isna(start):
        res["wtp_status"] = "no_start"
        return res
    fee = int(start)
    path = [fee]
    a0 = answers.get(fee, np.nan)
    if pd.isna(a0):
        res["wtp_status"] = "not_answered" if all(pd.isna(v) for v in answers.values()) else "incomplete"
        res["FLAG_wtp_nonmonotone"] = int(res["wtp_status"] == "incomplete")
        return res
    if a0 == 1:
        mx = fee
        while mx < 60:
            a = answers.get(mx + 10, np.nan)
            if pd.isna(a):
                res.update(wtp_status="incomplete", FLAG_wtp_nonmonotone=1)
                return res
            path.append(mx + 10)
            if a == 1:
                mx += 10
            else:
                break
        res["wtp_max_fee"] = mx
        res["wtp_censored_top"] = int(mx == 60)
    else:
        f = fee
        while True:
            if f == 0:
                res["wtp_rejects_all"] = 1
                break
            a = answers.get(f - 10, np.nan)
            if pd.isna(a):
                res.update(wtp_status="incomplete", FLAG_wtp_nonmonotone=1)
                return res
            path.append(f - 10)
            if a == 1:
                res["wtp_max_fee"] = f - 10
                break
            f -= 10
    res["wtp_path"] = ">".join(map(str, path))
    for fee_pt, a in answers.items():
        if fee_pt in path or pd.isna(a):
            continue
        implied = 0 if res["wtp_rejects_all"] else int(fee_pt <= res["wtp_max_fee"])
        if int(a) != implied:
            res["FLAG_wtp_orphan_conflict"] = 1
    return res


def ladder_frame(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, r in df.iterrows():
        ans = {f: r.get(f"wtp_accept_{f}", np.nan) for f in C.WTP_FEES}
        rows.append(reconstruct_ladder(r.get("wtp_start", np.nan), ans))
    return pd.DataFrame(rows, index=df.index)


# ------------------------------------------------------------ DCE
def load_design() -> pd.DataFrame | None:
    if not C.DCE_DESIGN_FILE.exists():
        return None
    d = pd.read_csv(C.DCE_DESIGN_FILE)
    d["block"] = d["block"].astype(int)
    return d


def dominant_alt(design: pd.DataFrame, block: int, task="dom"):
    t = design[(design.block == block) & (design.task == task)].set_index("alt")
    if t.empty:
        return None
    a, b = t.loc["A"], t.loc["B"]

    def ge(x, y):
        return (x.price <= y.price and x.eta_min <= y.eta_min and x.late_in_10 <= y.late_in_10
                and REST_RANK[x.restaurants] >= REST_RANK[y.restaurants]
                and REFUND_RANK[x.refund] >= REFUND_RANK[y.refund])
    return 1 if ge(a, b) else (2 if ge(b, a) else None)


def dce_long(resp: pd.DataFrame, design: pd.DataFrame, include_dom=False) -> pd.DataFrame:
    tasks = [t for t in design.task.unique() if include_dom or t != "dom"]
    cols = [f"dce_{t}" for t in tasks if f"dce_{t}" in resp.columns]
    base = resp.loc[resp["meta_dce_block"].notna(), ["resp_id", "city", "seg_occupation", "meta_dce_block"] + cols].copy()
    m = base.melt(id_vars=["resp_id", "city", "seg_occupation", "meta_dce_block"],
                  value_vars=cols, var_name="task_var", value_name="choice").dropna(subset=["choice"])
    m["task"] = m.task_var.str.replace("dce_", "", regex=False)
    m = m.rename(columns={"meta_dce_block": "block"})
    m["block"] = m["block"].astype(int)
    long = m.merge(design, on=["block", "task"], how="inner")
    long["chosen"] = (((long.alt == "A") & (long.choice == 1)) | ((long.alt == "B") & (long.choice == 2))).astype(int)
    other = long[["resp_id", "task", "alt", "price", "late_in_10"]].copy()
    other["alt"] = other.alt.map({"A": "B", "B": "A"})
    long = long.merge(other.rename(columns={"price": "price_other", "late_in_10": "late_other"}),
                      on=["resp_id", "task", "alt"], how="left")
    long["is_cheaper_alt"] = (long.price < long.price_other).astype(int)
    long["is_more_reliable_alt"] = (long.late_in_10 < long.late_other).astype(int)
    return long


def rss_from_long(long: pd.DataFrame) -> pd.Series:
    rel = long[(long.purpose_tag == C.DCE_REL_TAG) & (long.is_more_reliable_alt == 1)]
    rel = rel.assign(hit=((rel.chosen == 1) & (rel.price > rel.price_other)).astype(int))
    g = rel.groupby("resp_id").agg(n=("hit", "size"), k=("hit", "sum"))
    return (g.k / g.n * 100).where(g.n >= C.DCE_MIN_REL_TASKS)


# ------------------------------------------------------------ bills
BILL_TARGET = {"bill_s1": ("simple", "bill_s1_simple_chosen"),
               "bill_s2": ("no_discount", "bill_s2_nodiscount_chosen"),
               "bill_s3": ("new_app", "bill_s3_newapp_chosen"),
               "bill_s4": ("new_app", "bill_s4_newapp_chosen")}


def bill_meaning(version: str, scenario: str, code) -> str | None:
    if pd.isna(code):
        return None
    code = int(code)
    if code == 3:
        return "no_difference"
    order1 = version in VERSION_ORDER1
    first, second = {"bill_s1": ("simple", "itemised"), "bill_s2": ("discount", "no_discount"),
                     "bill_s3": ("usual_app", "new_app"), "bill_s4": ("usual_app", "new_app")}[scenario]
    if not order1:
        first, second = second, first
    return first if code == 1 else second


# ------------------------------------------------------------ Ownly status
def ownly_status(r) -> str:
    aware = (r.get("own_aware_aided") in (1, 2)) or (r.get("own_aware_unaided") == 1)
    tried = r.get("own_tried") == 2
    orders = r.get("own_orders_4wk")
    if tried:
        if pd.notna(orders) and orders >= 2:
            return "user_repeat"
        if pd.notna(orders) and orders == 1:
            return "user_single"
        if pd.notna(orders) and orders == 0:
            return "lapsed"
        return "tried_unknown"
    if aware:
        return "aware_not_tried"
    return "unaware" if pd.notna(r.get("own_aware_aided")) else "not_asked"
