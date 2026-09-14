"""Step 0: hash every raw export and maintain raw/MANIFEST.csv (raw files are immutable).

A raw file whose hash changed since it was first registered is reported as an ERROR
(raw exports must never be edited; export a new dated file instead).
"""
from __future__ import annotations

import hashlib
import sys
from datetime import datetime

import pandas as pd

import config as C
import utils_io as io


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    C.RAW_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path = C.RAW_DIR / "MANIFEST.csv"
    old = io.read_csv(manifest_path, required=False)
    old = old if old is not None else pd.DataFrame(columns=["file", "export_ts", "rows", "sha256", "registered_at"])
    rows, errors = [], []
    for p in sorted(C.RAW_DIR.glob("*.csv")):
        if p.name.startswith("MANIFEST"):
            continue
        digest = sha256(p)
        n = sum(1 for _ in open(p, encoding="utf-8", errors="ignore")) - 1
        prev = old[old.file == p.name]
        if len(prev) and prev.sha256.iloc[0] != digest:
            errors.append(p.name)
        rows.append({"file": p.name,
                     "export_ts": datetime.fromtimestamp(p.stat().st_mtime).isoformat(timespec="seconds"),
                     "rows": n, "sha256": digest,
                     "registered_at": prev.registered_at.iloc[0] if len(prev) else datetime.now().isoformat(timespec="seconds")})
    io.write_csv(pd.DataFrame(rows), manifest_path)
    if errors:
        sys.exit(f"ERROR: raw file(s) changed after registration: {errors}")


if __name__ == "__main__":
    main()
