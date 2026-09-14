"""Step 1: Google Forms exports -> one harmonised interim table with canonical variable names.

Inputs : RAW_DIR/hyd_survey_v{1-4}_raw_*.csv, RAW_DIR/blr_survey_b{1,2}_raw_*.csv
         FORM_MAP_FILE (copy of form_column_map_TEMPLATE.csv with exact export headers)
Outputs: INTERIM_DIR/survey_combined.csv, unmapped_columns.csv, recode_unmatched.csv
"""
from __future__ import annotations

import os
import re
import warnings

import numpy as np
import pandas as pd

warnings.simplefilter("ignore", pd.errors.PerformanceWarning)

import config as C
import utils_io as io
import utils_survey as us

TS_DAYFIRST = os.environ.get("OWNLY_FORMS_TS_DAYFIRST", "1") == "1"   # en-IN sheet locale
VERSION_RE = re.compile(r"_(v[1-4]|b[12])_", re.I)
DCE_CODES = {"app a": 1, "app b": 2, "1": 1, "2": 2}
BILL_CODES = {"bill 1": 1, "bill 2": 2, "no real difference to me": 3, "1": 1, "2": 2, "3": 3}
WTP_CODES = {"yes, i would order": 1, "yes": 1, "no": 0, "1": 1, "0": 0}


def fixed_codes(series, table, var, unmatched):
    out = []
    for v in series:
        if pd.isna(v) or str(v).strip() == "":
            out.append(np.nan)
            continue
        key = us.norm(v)
        hit = table.get(key)
        if hit is None:
            hit = next((c for k, c in table.items() if key.startswith(k)), None)
        if hit is None:
            unmatched.append((var, str(v)))
        out.append(np.nan if hit is None else hit)
    return pd.Series(out, index=series.index, dtype="float")


def parse_number(series, var):
    s = series.astype(str).str.replace("₹", "", regex=False).str.replace(",", "", regex=False).str.strip()
    rng_mask = s.str.fullmatch(r"\d+(\.\d+)?\s*-\s*\d+(\.\d+)?")
    val = pd.to_numeric(s, errors="coerce")
    if rng_mask.any():
        parts = s[rng_mask].str.split("-", expand=True).astype(float)
        val[rng_mask] = parts.mean(axis=1)
    return val, rng_mask.fillna(False).astype(int).rename(f"{var}__num_parsed_range")


def main():
    dic = io.load_dictionary()
    codes_src = dict(zip(dic.variable_name, dic.values_codes))
    fmap = pd.read_csv(C.FORM_MAP_FILE, dtype=str).fillna("")
    fmap["key"] = fmap.expected_header.map(us.norm)
    files = sorted(C.RAW_DIR.glob("*_survey_*raw*.csv"))
    if not files:
        raise SystemExit(f"No raw survey exports found in {C.RAW_DIR}")
    frames, unmapped, unmatched = [], [], []
    for f in files:
        city = "hyd" if f.name.lower().startswith("hyd") else "blr"
        vm = VERSION_RE.search(f.name)
        version = vm.group(1).upper() if vm else ""
        raw = pd.read_csv(f, dtype=str)
        out = pd.DataFrame(index=raw.index)
        for col in raw.columns:
            cand = fmap[(fmap.key == us.norm(col)) & fmap.form_family.isin(["both", city, version])]
            if cand.empty:
                unmapped.append({"file": f.name, "header": col})
                continue
            spec = cand.sort_values("form_family", key=lambda s: s.map({version: 0, city: 1, "both": 2})).iloc[0]
            var, kind = spec.variable_name, spec.kind
            s = raw[col]
            if kind == "single":
                cl = us.parse_codes(codes_src.get(var, ""), city)
                if not any(code is not None and label != str(code) for code, label in cl):
                    cl = us.parse_codes(codes_src.get("pain_fee_reconsider_freq", ""), city)   # grid rows (e.g. att_check_1) share the grid scale
                out[var], um = us.recode_single(s, cl, var)
                unmatched += um
            elif kind == "checkbox":
                cb, um = us.split_checkbox(s, us.parse_codes(codes_src.get(var, ""), city), var)
                out = pd.concat([out, cb], axis=1)
                unmatched += um
            elif kind == "number":
                out[var], flag = parse_number(s, var)
                out[flag.name] = flag
            elif kind == "dce":
                out[var] = fixed_codes(s, DCE_CODES, var, unmatched)
            elif kind == "bill":
                out[var] = fixed_codes(s, BILL_CODES, var, unmatched)
            elif kind == "wtp":
                out[var] = fixed_codes(s, WTP_CODES, var, unmatched)
            elif kind == "timestamp":
                out["meta_submit_ts"] = pd.to_datetime(s, dayfirst=TS_DAYFIRST, errors="coerce")
            else:                                          # text / prefill
                out[var] = s.fillna("").str.strip()
        out.insert(0, "city", city)
        if "meta_form_version" not in out or out["meta_form_version"].eq("").all():
            out["meta_form_version"] = version
        out["meta_form_version"] = out["meta_form_version"].replace("", version).str.upper()
        out["source_file"] = f.name
        out["row_in_file"] = np.arange(1, len(out) + 1)
        frames.append(out)

    df = pd.concat(frames, ignore_index=True)
    df.insert(0, "resp_id", [f"{c}_{v}_{i:04d}" for c, v, i in zip(df.city, df.meta_form_version, df.row_in_file)])
    if "meta_start_ts" in df:
        start = pd.to_datetime(pd.to_numeric(df.meta_start_ts, errors="coerce"), unit="ms", utc=True)
        df["meta_start_dt"] = start.dt.tz_convert("Asia/Kolkata").dt.tz_localize(None)
        df["meta_duration_sec"] = (df.meta_submit_ts - df.meta_start_dt).dt.total_seconds()
        df.loc[df.meta_duration_sec < 0, "meta_duration_sec"] = np.nan
    df["meta_brand_arm"] = df.meta_form_version.map(us.ARM_OF)
    df["meta_dce_block"] = df.meta_form_version.map(us.BLOCK_OF)
    df["wtp_start"] = df.meta_form_version.map(us.WTP_START_OF)
    df["bill_order"] = np.where(df.meta_form_version.isin(us.VERSION_ORDER1), 1, 2)
    df["data_status"] = C.DATA_STATUS

    io.write_csv(df, C.INTERIM_DIR / "survey_combined.csv")
    io.write_csv(pd.DataFrame(unmapped, columns=["file", "header"]), C.INTERIM_DIR / "unmapped_columns.csv")
    um = pd.DataFrame(unmatched, columns=["variable", "value"]).value_counts().reset_index(name="count")
    io.write_csv(um, C.INTERIM_DIR / "recode_unmatched.csv")
    if unmapped:
        print(f"  WARNING: {len(unmapped)} unmapped columns — update form_column_map.csv")


if __name__ == "__main__":
    main()
