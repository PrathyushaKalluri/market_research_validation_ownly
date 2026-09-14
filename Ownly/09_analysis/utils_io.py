from __future__ import annotations

"""I/O helpers with the DEMO_SYNTHETIC guard.

Rules enforced here (see 09_analysis/README.md):
* In demo mode (OWNLY_DEMO_MODE=1) every file name gets a `__DEMO_SYNTHETIC` tag and
  writing anywhere inside the project folder is refused.
* Outside demo mode, any dataframe whose data_status contains DEMO_SYNTHETIC, or any
  path containing DEMO_SYNTHETIC, is refused if the target is inside the project
  (and always refused inside 08_clean_data/).
"""
from pathlib import Path
import csv
import sys

import pandas as pd

import config as C


class SyntheticDataGuardError(RuntimeError):
    pass


def _inside(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def tag(path) -> Path:
    """Return the path actually used on disk (adds __DEMO_SYNTHETIC in demo mode)."""
    path = Path(path)
    if C.DEMO_MODE and "DEMO_SYNTHETIC" not in path.name:
        return path.with_name(f"{path.stem}__DEMO_SYNTHETIC{path.suffix}")
    return path


def guard_path(path: Path, df: pd.DataFrame | None = None) -> None:
    path = Path(path)
    synthetic = C.DEMO_MODE or "DEMO_SYNTHETIC" in str(path)
    if df is not None and "data_status" in df.columns:
        synthetic = synthetic or df["data_status"].astype(str).str.contains("DEMO_SYNTHETIC").any()
    if not synthetic:
        return
    if _inside(path, C.PROJECT_ROOT / "08_clean_data"):
        raise SyntheticDataGuardError(f"Refusing to write synthetic data into 08_clean_data: {path}")
    if _inside(path, C.PROJECT_ROOT):
        raise SyntheticDataGuardError(f"Refusing to write synthetic data inside the project: {path}")


def write_csv(df: pd.DataFrame, path, index=False) -> Path:
    out = tag(path)
    guard_path(out, df)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=index, quoting=csv.QUOTE_MINIMAL)
    print(f"  wrote {out} ({len(df)} rows)")
    return out


def write_text(text: str, path) -> Path:
    out = tag(path)
    guard_path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(f"  wrote {out}")
    return out


def read_csv(path, required=True, **kw) -> pd.DataFrame | None:
    p = tag(path)
    if not p.exists():
        p = Path(path)            # fall back to untagged (e.g. project reference files)
    if not p.exists():
        if required:
            sys.exit(f"Missing input: {tag(path)}")
        print(f"  (optional input not found: {tag(path)})")
        return None
    return pd.read_csv(p, **kw)


def stamp(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["data_status"] = C.DATA_STATUS
    return df


def load_dictionary() -> pd.DataFrame:
    return pd.read_csv(C.DICT_FILE, dtype=str).fillna("")
