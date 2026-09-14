"""Central configuration for the Ownly Gachibowli analysis pipeline.

All thresholds mirror 00_research_charter/C_hypothesis_tree.md and
11_insights/decision_framework_and_scorecard.md (pre-registered 2026-09-14).
Change a value here ONLY before the PAP is frozen; otherwise log a deviation in
09_analysis/M_pre_analysis_plan.md section 11 and in decisions.md.

Paths can be redirected with environment variables (used by the synthetic test):
  OWNLY_DATA_ROOT, OWNLY_OUT_ROOT, OWNLY_FORM_MAP, OWNLY_BILL_MAP, OWNLY_AUDIT_FILE,
  OWNLY_FAKEDOOR_FILE, OWNLY_DEMO_MODE=1, OWNLY_N_BOOT, OWNLY_OBSERVED_FEE_INR
"""
from pathlib import Path
import os

ANALYSIS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = ANALYSIS_DIR.parent

DATA_ROOT = Path(os.environ.get("OWNLY_DATA_ROOT", PROJECT_ROOT / "08_clean_data"))
OUT_ROOT = Path(os.environ.get("OWNLY_OUT_ROOT", ANALYSIS_DIR / "outputs"))
RAW_DIR = DATA_ROOT / "raw"
INTERIM_DIR = DATA_ROOT / "interim"
CLEAN_DIR = DATA_ROOT / "cleaned"
EXCL_DIR = DATA_ROOT / "excluded"
FLAGS_FILE = DATA_ROOT / "flags.csv"
ADJ_FILE = DATA_ROOT / "adjudication_log.csv"
LOCALITY_RECODE_FILE = DATA_ROOT / "locality_recode_log.csv"
MART_DIR = OUT_ROOT / "mart"          # dashboard-ready tables (10_dashboard/dataset_schema.md)

DICT_FILE = PROJECT_ROOT / "03_hyderabad_survey" / "survey_variable_dictionary.csv"
DCE_DESIGN_FILE = PROJECT_ROOT / "03_hyderabad_survey" / "dce_design_matrix.csv"
FORM_MAP_FILE = Path(os.environ.get("OWNLY_FORM_MAP", ANALYSIS_DIR / "form_column_map.csv"))
BILL_MAP_FILE = Path(os.environ.get("OWNLY_BILL_MAP", ANALYSIS_DIR / "bill_scenario_map.csv"))
AUDIT_FILE = Path(os.environ.get("OWNLY_AUDIT_FILE",
                                 PROJECT_ROOT / "06_competitor_audit" / "data" / "audit_obs.csv"))
FAKEDOOR_FILE = Path(os.environ.get("OWNLY_FAKEDOOR_FILE",
                                    PROJECT_ROOT / "07_fake_door" / "data" / "events_raw.csv"))
REVIEWS_APP_FILE = PROJECT_ROOT / "05_review_mining" / "app_stores" / "reviews_coded.csv"
REVIEWS_SOCIAL_FILE = PROJECT_ROOT / "05_review_mining" / "social" / "social_coded.csv"

DEMO_MODE = os.environ.get("OWNLY_DEMO_MODE", "0") == "1"
DATA_STATUS = "DEMO_SYNTHETIC" if DEMO_MODE else "REAL"

# ---- reproducibility ------------------------------------------------------
SEED = 20260914
N_BOOT = int(os.environ.get("OWNLY_N_BOOT", "10000"))
N_BOOT_AUDIT = int(os.environ.get("OWNLY_N_BOOT_AUDIT", "5000"))
N_KRINSKY_ROBB = 5000
ALPHA = 0.05

# Ownly's delivery fee as OBSERVED in the Gachibowli audit (secondary sources conflict).
# Leave None until the audit exists; 10_audit_analysis.py writes the observed median.
_fee = os.environ.get("OWNLY_OBSERVED_FEE_INR")
OWNLY_OBSERVED_FEE_INR = float(_fee) if _fee not in (None, "") else None

# ---- segments ---------------------------------------------------------------
OCC_MAP = {1: "student", 2: "student", 3: "working_professional", 4: "working_student", 5: "other"}
FREQ_MAP = {1: "occasional", 2: "regular", 3: "frequent", 4: "frequent"}
H6_GROUPS = ("student", "working_professional")

# ---- derived-metric item lists (PAP section 4) -----------------------------
PPI_ITEMS = ["pain_fee_reconsider_freq", "pain_bill_unreasonable_freq",
             "pain_menu_markup_belief", "beh_abandon_price_freq"]
PPI_MIN_ITEMS = 3
PAIN_GRID = ["pain_fee_reconsider_freq", "pain_bill_unreasonable_freq", "beh_abandon_price_freq",
             "pain_late_freq", "pain_cancel_freq", "pain_wrong_item_freq",
             "pain_restaurant_unavailable_freq", "pain_quality_freq"]
DK_CODES = {98, 99}
ALPHA_MIN = 0.60
WTP_FEES = [0, 10, 20, 30, 40, 50, 60]
DCE_REL_TAG = "price_vs_reliability"
DCE_MIN_REL_TASKS = 2

# ---- business-significance floors (hypothesis tree section 0) --------------
FLOOR_PP = 0.10
FLOOR_R = 0.20
FLOOR_D = 0.30
FLOOR_INR = 10

# ---- minimum n before a test is attempted (NOT TESTABLE below) -------------
MIN_N_PROP = 30
MIN_N_GROUP = 30
MIN_N_DCE = 125          # Orme rule for a pooled model; fallback to task shares below
MIN_EPV = 10
MIN_SEGMENT_N_TARGET = 60

# ---- cleaning (08_clean_data/cleaning_protocol.md) -------------------------
SPEEDER_HARD = 0.40
SPEEDER_BORDER = 0.50
DUP_WINDOW_MIN = 30
TEXT_SIM_THRESHOLD = 0.90
TOTAL_MIN_INR, TOTAL_MAX_INR = 50, 5000
EXCLUSION_PRECEDENCE = ["EX01_screen_fail", "EX08_missing_critical", "EX05_duplicate",
                        "EX07_bot_or_gibberish", "EX03_attention_fail", "EX02_speeder",
                        "EX09_outside_target_after_recode", "EX06_incoherent", "EX04_straightline"]

# ---- city transfer ----------------------------------------------------------
NONINF_MARGIN_INDEX = -10.0
NONINF_MARGIN_PP = -0.10
POSTSTRAT_MIN_CELL = 10

# ---- scorecard (11_insights/decision_framework_and_scorecard.md) -----------
DEFAULT_WEIGHTS = {"D1": 0.20, "D2": 0.20, "D3": 0.20, "D4": 0.25, "D5": 0.15}
ALT_WEIGHT_SETS = {
    "equal": {"D1": 0.20, "D2": 0.20, "D3": 0.20, "D4": 0.20, "D5": 0.20},
    "behaviour_first": {"D1": 0.15, "D2": 0.15, "D3": 0.20, "D4": 0.20, "D5": 0.30},
    "price_thesis": {"D1": 0.20, "D2": 0.20, "D3": 0.30, "D4": 0.20, "D5": 0.10},
}
# metric_key: (dimension, weight within dimension, weak anchor, strong anchor). None anchors = formula-based.
SCORE_INPUTS = {
    "ppi_median": ("D1", 0.40, 25, 65),
    "abandon_price_share": ("D1", 0.30, 0.10, 0.50),
    "fee_reconsider_share": ("D1", 0.30, 0.20, 0.70),
    "sri_median": ("D2", 0.35, 30, 70),
    "threshold_met_share": ("D2", 0.35, 0.10, 0.60),
    "multihome_share": ("D2", 0.15, 0.30, 0.80),
    "no_subscription_share": ("D2", 0.15, 0.40, 0.90),
    "audit_win_rate": ("D3", 0.40, 0.30, 0.80),
    "audit_saving_pct_basket": ("D3", 0.30, 0.00, 0.15),
    "fee_accept_at_ownly_fee": ("D3", 0.30, 0.30, 0.75),
    "eta_acceptability": ("D4", 0.30, None, None),
    "coverage_adequacy": ("D4", 0.30, None, None),
    "ontime_most_share": ("D4", 0.25, 0.50, 0.85),
    "review_reliability_score": ("D4", 0.15, None, None),
    "aware_to_tried": ("D5", 0.40, 0.10, 0.50),
    "repeat_rate": ("D5", 0.35, 0.20, 0.60),
    "intent_action_ratio": ("D5", 0.25, 0.05, 0.30),
}
GATE_RETHINK = 40
GATE_BLOCK_SCALE = 40
SCALE_TOTAL = 70
SCALE_MIN_DIM = 50
ADAPT_MIN = 50
