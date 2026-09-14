#!/usr/bin/env bash
# End-to-end pipeline test on DEMO_SYNTHETIC fixtures. All inputs/outputs live in the scratchpad.
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
D="${DEMO_DIR:-/private/tmp/claude-501/-Users-klprathyusha-Sem-3-Project/90a9dd4b-778d-4cbd-b419-3747da65abb9/scratchpad/demo_synthetic}"
export PYTHON="${PYTHON:-python3}"
export OWNLY_DEMO_MODE=1
export OWNLY_DATA_ROOT="$D/data"
export OWNLY_OUT_ROOT="$D/out"
export OWNLY_FORM_MAP="$D/form_column_map_DEMO_SYNTHETIC.csv"
export OWNLY_AUDIT_FILE="$D/audit_obs_DEMO_SYNTHETIC.csv"
export OWNLY_FAKEDOOR_FILE="$D/events_DEMO_SYNTHETIC.csv"
export OWNLY_N_BOOT="${OWNLY_N_BOOT:-500}"
export OWNLY_N_BOOT_AUDIT="${OWNLY_N_BOOT_AUDIT:-300}"
rm -rf "$D"
cd "$HERE"
"$PYTHON" tests/make_demo_synthetic.py --out "$D"
bash run_all.sh
