#!/usr/bin/env bash
# Full pipeline with fixed seeds. Run from anywhere:  bash 09_analysis/run_all.sh
# Order: 06 (hypothesis tests) runs after 07-12 because it consumes their outputs.
set -euo pipefail
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"
for step in 00_manifest_and_hash 01_ingest_and_harmonise 02_quality_flags 03_split_clean_excluded \
            04_derive_metrics 05_descriptives 07_dce_models 08_wtp_curves 09_city_transfer \
            10_audit_analysis 11_reviews_merge 12_fakedoor 06_hypothesis_tests 13_scorecard; do
  echo "=== ${step} ==="
  "$PY" "${step}.py"
done
echo "Pipeline finished. Review pending_adjudication.csv and recode_unmatched.csv before reporting."
