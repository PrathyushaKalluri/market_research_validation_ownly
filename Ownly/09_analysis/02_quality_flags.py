"""Step 2: compute every quality flag (08_clean_data/cleaning_protocol.md section 3). No rows removed.

Flag values: "" (clear) | "borderline" | "hard". FLAG_* columns are 0/1 (sensitivity only).
Output: FLAGS_FILE
"""
from __future__ import annotations

import difflib
import re

import numpy as np
import pandas as pd

import config as C
import utils_io as io
import utils_survey as us

OPEN_TEXT = ["beh_unaided_apps", "beh_switch_reason", "pain_unaided_frustration", "bt_concern",
             "br_rapido_effect_why", "own_disappointment", "meta_comments"]
SIGNATURE = ["scr_age_band", "seg_occupation_raw", "scr_area", "scr_orders_4wk", "beh_last_platform",
             "beh_last_order_total"]


def col(df, name):
    return df[name] if name in df.columns else pd.Series(np.nan, index=df.index)


def gibberish(t: str) -> bool:
    t = str(t).strip()
    if len(t) < 4:
        return False
    letters = sum(ch.isalpha() for ch in t) / len(t)
    no_vowel = not re.search(r"[aeiou]", t.lower()) and len(t) > 6
    runs = re.search(r"(.)\1{4,}", t) is not None
    return letters < 0.5 or no_vowel or runs


def main():
    df = io.read_csv(C.INTERIM_DIR / "survey_combined.csv", low_memory=False, parse_dates=["meta_submit_ts"])
    F = df[["resp_id", "city", "meta_form_version"]].copy()
    for ex in C.EXCLUSION_PRECEDENCE:
        F[ex] = ""

    def mark(ex, mask, level):
        mask = mask.fillna(False)
        if level == "hard":
            F.loc[mask, ex] = "hard"
        else:
            F.loc[mask & (F[ex] != "hard"), ex] = "borderline"

    hyd, blr = df.city.eq("hyd"), df.city.eq("blr")
    area = col(df, "scr_area")
    ex01 = (col(df, "meta_consent").eq(0) | col(df, "scr_age_band").isin([1, 6])
            | (hyd & area.isin([90, 99])) | (blr & area.eq(99))
            | col(df, "scr_orders_4wk").eq(0) | col(df, "scr_coi").eq(1))
    mark("EX01_screen_fail", ex01, "hard")
    completes = ~ex01

    # EX02 speeder: ratio to version median among completes
    dur = col(df, "meta_duration_sec")
    med = dur[completes].groupby(df.meta_form_version[completes]).median()
    ratio = dur / df.meta_form_version.map(med)
    F["duration_ratio"] = ratio.round(3)
    mark("EX02_speeder", completes & (ratio < C.SPEEDER_HARD), "hard")
    mark("EX02_speeder", completes & (ratio >= C.SPEEDER_HARD) & (ratio < C.SPEEDER_BORDER), "borderline")
    F["FLAG_no_duration"] = (completes & dur.isna()).astype(int)

    # EX03 attention
    att = col(df, "att_check_1")
    mark("EX03_attention_fail", completes & att.notna() & att.ne(2), "hard")

    # EX04 straightline on the pain grid (all rows answered, SD = 0)
    grid = df[[c for c in C.PAIN_GRID if c in df.columns]]
    sl = completes & grid.notna().all(axis=1) & grid.nunique(axis=1).eq(1)
    speed_any = F["EX02_speeder"].ne("")
    mark("EX04_straightline", sl & ~speed_any, "borderline")
    mark("EX04_straightline", sl & speed_any, "hard")

    # EX05 duplicates
    mark("EX05_duplicate", col(df, "scr_repeat").eq(1), "hard")
    tok = col(df, "meta_session_token").replace("", np.nan)
    F["FLAG_no_token"] = tok.isna().astype(int)
    order = df.sort_values("meta_submit_ts").index
    dup_tok = tok.loc[order].duplicated(keep="first") & tok.loc[order].notna()
    mark("EX05_duplicate", dup_tok.reindex(df.index), "hard")
    sig_cols = [c for c in SIGNATURE if c in df.columns]
    s = df.loc[order, sig_cols + ["meta_submit_ts"]].copy()
    s["sig"] = s[sig_cols].astype(str).agg("|".join, axis=1)
    prev_ts = s.groupby("sig").meta_submit_ts.shift(1)
    near = (s.meta_submit_ts - prev_ts).dt.total_seconds() / 60 <= C.DUP_WINDOW_MIN
    mark("EX05_duplicate", near.reindex(df.index) & completes, "borderline")
    texts = df[[c for c in OPEN_TEXT if c in df.columns]].fillna("").astype(str).apply(lambda s: s.map(us.norm))
    sim_hits = pd.Series(0, index=df.index)
    idx = list(order)
    for i_pos, i in enumerate(idx):
        for j in idx[:i_pos]:
            n_sim = 0
            for c in texts.columns:
                a, b = texts.at[i, c], texts.at[j, c]
                if len(a) >= 25 and len(b) >= 25 and difflib.SequenceMatcher(None, a, b).ratio() > C.TEXT_SIM_THRESHOLD:
                    n_sim += 1
            if n_sim >= 2:
                sim_hits[i] = 1
                break
    mark("EX05_duplicate", sim_hits.eq(1) & completes, "borderline")

    # EX06 incoherence count
    plat_own = col(df, "beh_platforms_used_4wk__ownly_app").eq(1) | col(df, "beh_platforms_used_4wk__rapido_app_food_section").eq(1)
    total = col(df, "beh_last_order_total")
    inco = pd.concat([
        col(df, "beh_last_order_when").eq(7) & col(df, "scr_orders_4wk").ge(1),
        total.notna() & ((total < C.TOTAL_MIN_INR) | (total > C.TOTAL_MAX_INR)),
        col(df, "own_aware_aided").eq(0) & (col(df, "beh_last_platform").isin([3, 4]) | plat_own),
        col(df, "own_aware_aided").eq(0) & col(df, "own_tried").eq(2),
    ], axis=1).fillna(False).sum(axis=1)
    F["incoherence_count"] = inco
    mark("EX06_incoherent", completes & inco.eq(1), "borderline")
    mark("EX06_incoherent", completes & inco.ge(2), "hard")

    # EX07 gibberish / copy-paste
    gib = texts.apply(lambda s: s.map(gibberish)).any(axis=1)
    rep = pd.Series(False, index=df.index)
    for c in [k for k in texts.columns if k != "beh_unaided_apps"]:   # app-name lists are legitimately identical
        t = texts[c]
        counts = t[t.str.len() >= 25].value_counts()
        rep |= t.isin(counts[counts >= 3].index)
    mark("EX07_bot_or_gibberish", completes & (gib | rep), "borderline")

    # EX08 missing critical
    ppi_missing = df[[c for c in C.PPI_ITEMS if c in df.columns]].replace(list(C.DK_CODES), np.nan).isna().sum(axis=1)
    miss = col(df, "seg_occupation_raw").isna() | col(df, "scr_orders_4wk").isna() | ppi_missing.ge(2)
    mark("EX08_missing_critical", completes & miss, "hard")

    # EX09 locality recode (team-maintained log)
    rec = io.read_csv(C.LOCALITY_RECODE_FILE, required=False)
    if rec is not None and "recoded_outside" in rec:
        outside = df.resp_id.isin(rec.loc[rec.recoded_outside == 1, "resp_id"])
        mark("EX09_outside_target_after_recode", outside, "hard")

    # sensitivity flags
    dce_cols = [f"dce_t{i}" for i in range(1, 7) if f"dce_t{i}" in df.columns]
    if dce_cols:
        d = df[dce_cols]
        F["FLAG_choice_left_right"] = (d.notna().sum(axis=1).eq(len(dce_cols)) & d.nunique(axis=1).eq(1)).astype(int)
    design = us.load_design()
    if design is not None and "dce_dom" in df:
        dom = df.meta_dce_block.map(lambda b: us.dominant_alt(design, int(b)) if pd.notna(b) else None)
        F["FLAG_dominance_fail"] = (df.dce_dom.notna() & dom.notna() & df.dce_dom.ne(dom)).astype(int)
    F["FLAG_iiith"] = (hyd & col(df, "dem_institution").eq(1)).astype(int)
    lad = us.ladder_frame(df)
    F["FLAG_wtp_nonmonotone"] = lad.FLAG_wtp_nonmonotone
    F["FLAG_wtp_orphan_conflict"] = lad.FLAG_wtp_orphan_conflict
    F["data_status"] = C.DATA_STATUS
    io.write_csv(F, C.FLAGS_FILE)
    print(F[C.EXCLUSION_PRECEDENCE].apply(lambda s: s.value_counts()).fillna(0).astype(int).to_string())


if __name__ == "__main__":
    main()
