"""Step 3: split interim rows into CLEANED / EXCLUDED using flags + adjudication log.

* hard flag -> excluded
* borderline flag -> excluded only if adjudication_log.csv says decision=exclude for that
  (resp_id, flag); otherwise kept with EX_borderline=1 and listed in pending_adjudication.csv
* exclusion_reason = first flag in config.EXCLUSION_PRECEDENCE; all flags kept in exclusion_flags_all
Outputs: CLEAN_DIR/{city}_survey_cleaned.csv, EXCL_DIR/{city}_survey_excluded.csv,
         DATA_ROOT/pending_adjudication.csv, OUT_ROOT/sample_flow.csv
"""
from __future__ import annotations

import pandas as pd

import config as C
import utils_io as io


def main():
    df = io.read_csv(C.INTERIM_DIR / "survey_combined.csv", low_memory=False)
    F = io.read_csv(C.FLAGS_FILE)
    adj = io.read_csv(C.ADJ_FILE, required=False)
    adj_ex = set()
    adj_any = set()
    if adj is not None and len(adj):
        adj_any = set(zip(adj.resp_id, adj.flag))
        adj_ex = set(zip(adj.loc[adj.decision.str.lower().eq("exclude"), "resp_id"],
                         adj.loc[adj.decision.str.lower().eq("exclude"), "flag"]))
    reasons, all_flags, border, pending = [], [], [], []
    for _, r in F.iterrows():
        hard = [ex for ex in C.EXCLUSION_PRECEDENCE if r[ex] == "hard"]
        bl = [ex for ex in C.EXCLUSION_PRECEDENCE if r[ex] == "borderline"]
        bl_ex = [ex for ex in bl if (r.resp_id, ex) in adj_ex]
        bl_pending = [ex for ex in bl if (r.resp_id, ex) not in adj_any]
        exclude = [ex for ex in C.EXCLUSION_PRECEDENCE if ex in hard or ex in bl_ex]
        reasons.append(exclude[0] if exclude else "")
        all_flags.append(";".join(f"{ex}:{r[ex]}" for ex in C.EXCLUSION_PRECEDENCE if r[ex]))
        border.append(int(bool(bl) and not exclude))
        pending += [{"resp_id": r.resp_id, "flag": ex, "reviewer_1": "", "reviewer_2": "",
                     "decision": "", "rationale": "", "date": ""} for ex in bl_pending]
    F["exclusion_reason"] = reasons
    F["exclusion_flags_all"] = all_flags
    F["EX_borderline"] = border
    keep_cols = ["resp_id", "exclusion_reason", "exclusion_flags_all", "EX_borderline"] + \
        [c for c in F.columns if c.startswith("FLAG_")]
    m = df.merge(F[keep_cols], on="resp_id", how="left")
    for city, g in m.groupby("city"):
        io.write_csv(g[g.exclusion_reason.eq("")], C.CLEAN_DIR / f"{city}_survey_cleaned.csv")
        io.write_csv(g[g.exclusion_reason.ne("")], C.EXCL_DIR / f"{city}_survey_excluded.csv")
    io.write_csv(pd.DataFrame(pending, columns=["resp_id", "flag", "reviewer_1", "reviewer_2", "decision",
                                                "rationale", "date"]),
                 C.DATA_ROOT / "pending_adjudication.csv")
    if pending:
        print(f"  NOTE: {len(pending)} borderline flags await two-person adjudication (kept, EX_borderline=1)")

    src = m["meta_source"].fillna("(none)") if "meta_source" in m else "(none)"
    m = m.assign(meta_source_f=src)
    flow = []
    for keys, g in m.groupby(["city", "meta_form_version", "meta_source_f"], dropna=False):
        row = dict(zip(["city", "meta_form_version", "meta_source"], keys))
        row["starts"] = len(g)
        row["screen_outs"] = int(g.exclusion_reason.eq("EX01_screen_fail").sum())
        row["completes"] = row["starts"] - row["screen_outs"]
        for ex in C.EXCLUSION_PRECEDENCE[1:]:
            row[f"excluded_{ex}"] = int(g.exclusion_reason.eq(ex).sum())
        row["valid"] = int(g.exclusion_reason.eq("").sum())
        row["valid_borderline_kept"] = int((g.exclusion_reason.eq("") & g.EX_borderline.eq(1)).sum())
        flow.append(row)
    io.write_csv(io.stamp(pd.DataFrame(flow)), C.OUT_ROOT / "sample_flow.csv")


if __name__ == "__main__":
    main()
