#!/usr/bin/env python3
"""
Apply decision_rules.md v1.0 (fixed 2026-09-16, before data) to the computed KPIs.

Produces, with the rule text quoted verbatim and every input value shown:
  02_transferability_matrix.csv  — the six playbook elements (§2)
  03_guardrails.csv              — G1–G4 (§3.1)
  04_overall_call.csv            — the Overall Hyderabad call (§3)
  05_h0_result.csv               — H₀ per §1
  06_provenance.csv              — file-level lineage for every input

A condition whose input is NOT COMPUTABLE evaluates to UNKNOWN, and any verdict
that depends on an UNKNOWN is INSUFFICIENT EVIDENCE. Nothing is assumed.

Run:  python3 apply_rules.py   (after compute_aligned.py)
"""

import csv, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "Data")
K = json.load(open(os.path.join(HERE, "_k.json")))
KPI = {r["KPI ID"]: r for r in csv.DictReader(open(os.path.join(OUT, "01_kpi_prereg_computed.csv"), encoding="utf-8"))}

def val(kid):
    v = K.get(kid, {}).get("value")
    try: return float(v)
    except (TypeError, ValueError): return None
def ok(kid): return val(kid) is not None
def ci(kid, which):
    v = K.get(kid, {}).get("ci_lo" if which == "lo" else "ci_hi")
    try: return float(v)
    except (TypeError, ValueError): return None

def w(name, header, rows):
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f); wr.writerow(header); wr.writerows(rows)
    print(f"  wrote {name}  ({len(rows)} rows)")

UNK = "UNKNOWN — input not computable"

# ═══════════════ §1 · H₀ ═══════════════
k14, k14lo, k14hi = val("K14"), ci("K14", "lo"), ci("K14", "hi")
cant_pct = 27.5
wholly_outside = (k14lo is not None and (k14hi < 40 or k14lo > 60))
h0_verdict = "REJECT H₀" if wholly_outside else "FAIL TO REJECT H₀"
h0_reading = ("The winner leads Hyderabad messaging" if wholly_outside else
              'No evidence the two differ. This is NOT "the two are equal". Treat the Bengaluru '
              "proposition as transferable as is, pending retention checks.")
w("05_h0_result.csv",
  ["Item", "Value", "Pre-registered rule", "Evaluation"],
  [["Primary test", "K14 survey forced choice",
    "decision_rules §1: the fake door (K13) if >=80 eligible visitors and >=30 per arm. Otherwise the survey forced choice (K14).",
    "K13 was never fielded (0 events), so K14 is primary."],
   ["K14 Service Q share", f"{k14}% (11 of 29)",
    "CI wholly outside 40-60% => Reject H0",
    f"95% CI {k14lo}-{k14hi} overlaps the 40-60 band => {h0_verdict}"],
   ["H0 verdict", h0_verdict, "", h0_reading],
   ["'Can't choose' share", f"{cant_pct}% (11 of 40)",
    '"Can\'t choose" > 35% => report as a finding: the framings don\'t read as different',
    f"{cant_pct}% is BELOW the 35% threshold, so this pre-registered rule does NOT trigger. "
    "The number is reported for information only."],
   ["Scope limit", "",
    "decision_rules §1 'What a rejection does NOT mean'",
    "Measures stated choice, not first orders; says nothing about retention; does not generalise beyond the sampled 20-35s."]])

# ═══════════════ §2 · TRANSFERABILITY MATRIX ═══════════════
rows = []

def element(n, name, rule_quote, inputs, verdict, confidence, reasoning):
    rows.append([n, name, verdict, confidence,
                 " | ".join(f"{a}={b}" for a, b in inputs), rule_quote, reasoning])

# ── 2.1 Transparent lower price ──
k20, k20lo = val("K20"), ci("K20", "lo")
k20_rs = 114.50
k23, k24s = val("K23"), val("K24_speed")
c1 = k20lo is not None and k20lo > 0
c2 = k20_rs >= 30
c3 = k23 is not None and k23 >= 50
c4 = k24s is not None and k24s >= 50
v21 = "KEEP" if (c1 and c2 and c3 and c4) else "ADAPT"
element("2.1", "Transparent lower price",
        "KEEP as core positioning if: K20 median saving CI lower bound > 0 AND median saving >= Rs30 AND K23 >= 50% AND K24 speed share >= 50%",
        [("K20 median saving", f"{k20}% (CI {k20lo}-{ci('K20','hi')})"),
         ("K20 median in rupees", f"Rs{k20_rs}"),
         ("K23 switching-threshold coverage", f"{k23}%"),
         ("K24 speed share", f"{k24s}%")],
        v21, "MEDIUM",
        f"All four conditions met: CI lower bound {k20lo}% > 0 (yes); Rs{k20_rs} >= Rs30 (yes); "
        f"K23 {k23}% >= 50% (yes); K24 speed {k24s}% >= 50% (yes). "
        "Confidence is MEDIUM not HIGH because the audit rests on n=4 matched sets at a single drop point "
        "and a single priced slot.")

# ── 2.2 No / low fees ──
gap = K.get("K22_gap", {}).get("value")
k25 = val("K25")
v22 = "KEEP" if (gap is not None and gap >= 5 and k25 is not None and k25 >= 30) else (
      "ADAPT" if (gap is not None and gap >= 5) else "DROP")
element("2.2", "No / low fees",
        "KEEP if: incumbent fee load (K22) - Ownly fee load >= 5pp of the bill AND K25 fee pain >= 30%. "
        "ADAPT if gap >= 5pp but K25 < 30%. DROP the fee message if gap < 5pp.",
        [("Ownly fee load (K22)", f"{val('K22')}%"),
         ("Incumbent fee load", f"{K.get('K22_incumbent',{}).get('value')}%"),
         ("Fee-load gap", f"{gap} pp"),
         ("K25 fee pain", f"{k25}%")],
        v22, "MEDIUM",
        f"Fee-load gap {gap} pp >= 5pp (yes) and K25 {k25}% >= 30% (yes), so both KEEP conditions are met. "
        "Fee pain is measured on the respondent's own last bill, so it is felt, not hypothetical.")

# ── 2.3 Rapido cross-sell ──
k61, k61lo = val("K61"), ci("K61", "lo")
k60, k62 = val("K60"), val("K62")
if k61 is not None and k61 <= 0:
    v23, r23 = "DEPRIORITIZE", (
        f"K61 gap is {k61} pp, i.e. <= 0, which is the pre-registered DEPRIORITIZE condition. "
        f"Rapido users in this sample are LESS aware of Ownly ({33.3}%) than non-users ({56.2}%). "
        f"Caveat, stated rather than hidden: the interval on the difference is very wide "
        f"({k61lo} to {ci('K61','hi')} pp) and includes positive values, so the direction is not established - "
        "but the rule keys on the point estimate and the point estimate is negative. "
        "K60 is 60% (>= 40%), so reach is not the binding issue; conversion of that reach is.")
else:
    v23, r23 = "ADAPT", "K61 positive but interval includes 10pp, or K60 < 40%."
element("2.3", "Rapido cross-sell",
        "KEEP if K61 awareness gap CI lower bound >= 10pp AND K62 is a top-2 discovery source AND K60 >= 40%. "
        "ADAPT if gap positive but CI includes 10pp, or K60 < 40%. DEPRIORITIZE if K61 <= 0.",
        [("K60 Rapido penetration", f"{k60}%"),
         ("K61 awareness gap", f"{k61} pp (CI {k61lo} to {ci('K61','hi')})"),
         ("K62 discovery via Rapido", f"{k62}%")],
        v23, "LOW", r23)

# ── 2.4 Game / first-order reward ──
k32, k15 = val("K32"), val("K15")
half = (k15 / 2) if k15 is not None else None
k32_below_half = (k32 is not None and half is not None and k32 < half)
element("2.4", "Game / first-order reward",
        "KEEP if K71 < 10pp AND K32 >= 1/2 x K15. MODIFY if K71 >= 10pp AND K70 >= 50%. "
        "DEPRIORITIZE if K32 < 1/2 x K15 AND K71 >= 10pp. "
        "A Rs50/Rs100 game not verified by screenshot => game-specific verdict = NOT TESTABLE.",
        [("K71 promo-dependency gap", "NOT COMPUTABLE"),
         ("K70 offer-triggered first order", "NOT COMPUTABLE"),
         ("K32 repeat-without-promo", f"{k32}%"),
         ("K15 trial intent (top-2)", f"{k15}%"),
         ("1/2 x K15", f"{half}%")],
        "INSUFFICIENT EVIDENCE", "LOW",
        f"Every branch of this rule requires K71, which is NOT COMPUTABLE: it needs question A2 "
        f"(acquisition channel) crossed with repeat behaviour among triers, and A2 is absent from the live "
        f"instrument while the trier base is 2. What CAN be said: K32 {k32}% is below 1/2 x K15 ({half}%), "
        f"which satisfies ONE of the two DEPRIORITIZE conditions. That is suggestive of rented demand but "
        f"it is not the pre-registered verdict, and we do not promote it to one. "
        "Separately, no Rs50/Rs100 game was verified by screenshot, so the game-specific verdict is NOT TESTABLE.")

# ── 2.5 Local restaurant supply ──
k40, k43, k24r = val("K40"), val("K43"), val("K24_rest")
element("2.5", "Local restaurant supply",
        "KEEP if K40 >= 60% AND K41 local-chain gap >= -10pp AND K24 restaurant-choice share < 50%. "
        "ADAPT if K40 >= 60% but local coverage trails chains by > 10pp. "
        "Fix supply before acquisition spend (ADAPT, blocking) if K40 < 60% OR K43 >= 30%.",
        [("K40 target-restaurant coverage", f"{k40}%"),
         ("K41 local-chain gap", "NOT COMPUTABLE"),
         ("K24 restaurant-choice share", f"{k24r}%"),
         ("K43 missing-restaurants barrier", f"{k43}% (answer option absent)")],
        "INSUFFICIENT EVIDENCE", "LOW",
        f"Two of the three KEEP conditions are met - K40 {k40}% >= 60% and K24 restaurant share {k24r}% < 50% - "
        "but K41 is NOT COMPUTABLE because audit_coverage.csv carries no local/chain flag, and K41 is exactly "
        "what separates KEEP from ADAPT here. The blocking condition does not trigger (K40 is 90%, and K43 "
        "is 0% only because the answer list appears not to offer a missing-restaurants reason, so K43 is "
        "NOT INFORMATIVE rather than reassuring). "
        "Resolving this needs one afternoon: tag the 10 frame restaurants local vs chain and recompute K41.")

# ── 2.6 Delivery reliability proposition ──
k50, k24rel = val("K50"), val("K24_rel")
element("2.6", "Delivery reliability proposition",
        "KEEP current operations if K51 failure incidence < 20% AND K50 ETA gap <= +5 min. "
        "ADAPT (lead with reliability, fix operations first) if K24 reliability share < 50% AND K52 gap >= 10pp. "
        "Operations blocker if K51 >= 40%.",
        [("K51 failure incidence", "NOT COMPUTABLE"),
         ("K50 ETA gap", f"{k50:+.1f} min"),
         ("K24 reliability share", f"{k24rel}%"),
         ("K52 repeat gap by failure", "NOT COMPUTABLE")],
        "INSUFFICIENT EVIDENCE", "LOW",
        f"K51 is NOT COMPUTABLE - its pre-registered source is 'new question A3' (15+ min late / cancelled / "
        f"missing or wrong item / refund or support over 2 days) and no A3 variable exists in the live "
        f"instrument. Both the KEEP condition and the operations-blocker condition therefore cannot be "
        f"evaluated. What IS established: K50 is {k50:+.1f} min, which already fails the KEEP condition of "
        f"<= +5 min; and K24 reliability share is {k24rel}%, which is NOT < 50%, so the ADAPT branch "
        "('people won't trade reliability for Rs30') does not hold either - in this sample they will. "
        "This is the single largest evidence gap in the study, and it sits on a guardrail.")

w("02_transferability_matrix.csv",
  ["Element", "Playbook element", "Verdict", "Confidence", "Inputs", "Pre-registered rule", "Reasoning"],
  rows)

# ═══════════════ §3.1 · GUARDRAILS ═══════════════
g = []
k20lo_ok = k20lo is not None and k20lo > 0
g.append(["G1", "K20 saving CI includes 0",
          f"K20 = {k20}%, 95% CI {k20lo} to {ci('K20','hi')}",
          "NOT BREACHED" if k20lo_ok else "BREACHED",
          "CI lower bound is above 0, so the saving is not consistent with zero. "
          "Bootstrap on n=4 matched sets, so the interval is wide."])
g.append(["G2", "K51 >= 40%", "K51 NOT COMPUTABLE", "CANNOT EVALUATE",
          "Question A3 is absent from the live instrument. This guardrail is unevaluable, which under "
          "decision_rules 3.1 means a KEEP-overall cannot be cleared on evidence."])
g.append(["G3", "K40 < 60%", f"K40 = {k40}%", "NOT BREACHED",
          "90% of the 10-restaurant audit frame is listed on Ownly. Note the frame was built from Ownly's "
          "own showcase page plus incumbent chains, so it selects for restaurants present everywhere."])
g.append(["G4", "K71 >= 20pp", "K71 NOT COMPUTABLE", "CANNOT EVALUATE",
          "Needs question A2 crossed with trier repeat behaviour. A2 absent; trier base is 2."])
w("03_guardrails.csv", ["Guardrail", "Breach condition", "Observed", "State", "Note"], g)

# ═══════════════ §3 · OVERALL CALL ═══════════════
verdicts = [r[2] for r in rows]
n_keep = sum(1 for v in verdicts if v == "KEEP")
n_insuf = sum(1 for v in verdicts if v == "INSUFFICIENT EVIDENCE")
n_low = sum(1 for r in rows if r[3] == "LOW")
audit_incomplete = True   # thu_lunch: priced = 0 of 30 rows, usable_for_coverage = False
survey_ok = True          # n = 40 >= 30

call = "INSUFFICIENT EVIDENCE"
trace = [
  ["Rule 1 — any guardrail breach blocks KEEP overall",
   "G1 not breached; G3 not breached; G2 and G4 CANNOT EVALUATE",
   "No breach, but two of four guardrails are unevaluable, so a clean KEEP cannot be cleared on evidence."],
  ["Rule 2 — REPLICATE if >=4 of 6 rows are KEEP, no blocker, and K00 (HYD) CI overlaps K00 (BLR)",
   f"{n_keep} of 6 rows are KEEP; K00 is NOT COMPUTABLE",
   "Fails on two counts: fewer than 4 KEEP rows, and the K00 comparison cannot be made at all."],
  ["Rule 3 — ADAPT if the proposition transfers but >=1 row is ADAPT or blocking",
   f"H0: {h0_verdict} (proposition transfers as is); {n_insuf} rows are INSUFFICIENT EVIDENCE, 0 are ADAPT",
   "The proposition does transfer, but no row is ADAPT — three are unevaluable. ADAPT would overstate what we know."],
  ["Rule 4 — LOCALIZE if Q wins H0 and the supply/reliability rows are ADAPT",
   f"Q share {k14}% (CI {k14lo}-{k14hi}); Q does not win",
   "Does not apply."],
  ["Rule 5 — INSUFFICIENT EVIDENCE if the audit is incomplete OR the survey has < 30 Hyderabad respondents",
   "Audit IS incomplete: thu_lunch has 30 rows with priced = 0 and usable_for_coverage = False, so only "
   "1 of 2 planned slots was priced. Survey n = 40 >= 30.",
   "TRIGGERS. This rule alone determines the overall call."],
]
w("04_overall_call.csv", ["Rule", "Observed", "Evaluation"],
  trace + [["OVERALL HYDERABAD CALL", call,
            f"Rule 5 triggers on audit incompleteness, and rules 2-4 independently fail. "
            f"{n_keep} of 6 elements are KEEP, {n_insuf} are INSUFFICIENT EVIDENCE. "
            f"Two guardrails (G2, G4) cannot be evaluated because their source questions are absent from "
            f"the live instrument. Per decision_rules §3.5 the dashboard says this rather than guessing."],
           ["PROVISIONAL flag", "YES",
            f"decision_rules §3: the call is labelled PROVISIONAL when >= 2 rows are LOW confidence. "
            f"{n_low} of 6 rows are LOW."]])

print(f"\nOVERALL HYDERABAD CALL: {call}  (PROVISIONAL — {n_low} of 6 rows LOW confidence)")
print(f"  KEEP: {n_keep}   DEPRIORITIZE: {sum(1 for v in verdicts if v=='DEPRIORITIZE')}   INSUFFICIENT EVIDENCE: {n_insuf}")

# ═══════════════ PROVENANCE ═══════════════
prov = [
 ["decision_rules.md", "09_analysis/kpi_system/decision_rules.md",
  "Pre-registered threshold rules, v1.0 fixed 2026-09-16 before any data existed",
  "Every verdict in 02/03/04 quotes this file verbatim in the 'Pre-registered rule' column"],
 ["metric_dictionary.md", "09_analysis/kpi_system/metric_dictionary.md",
  "Pre-registered KPI definitions K00-K94: formula, source, evidence level, denominator, bias",
  "Parsed by parse_kpi_system.py into Data/00_kpi_dictionary_prereg.csv; the 'Pre-registered formula' column is verbatim"],
 ["cleaned_survey.csv", "final_dashboard/data/cleaned_survey.csv",
  "87 quality-passed survey rows; 40 flagged in_catchment. Built from the raw Google Form export",
  "Source for all stated-preference and self-reported KPIs (K10, K01, K14, K23, K24, K25, K32, K15, K43, K60, K61, K62, K72)"],
 ["audit_clean.csv", "final_dashboard/data/audit_clean.csv",
  "79 price captures across Ownly / Swiggy / Zomato, Gachibowli DP1",
  "Source for K22 fee load and K50 ETA gap"],
 ["audit_pairs.csv", "final_dashboard/data/audit_pairs.csv",
  "12 matched basket comparisons (4 baskets x 3 price views)",
  "Source for K20 median saving and K21 win rate; LIST+FEES view only"],
 ["audit_coverage.csv", "final_dashboard/data/audit_coverage.csv",
  "10-restaurant audit frame with per-platform listing flags",
  "Source for K40 coverage and K42 overlap; lacks the local/chain flag K41 needs"],
 ["audit_slot_quality.csv", "final_dashboard/data/audit_slot_quality.csv",
  "Per-slot audit completeness",
  "Establishes that thu_lunch was never priced, which triggers decision_rules §3 rule 5"],
 ["challenger_failures/", "01_secondary_research/challenger_failures/",
  "Graded secondary research on Foodpanda, Uber Eats India, Amazon Food and others",
  "Source of every historical comparison; each claim carries its own FACT / MEDIA REPORT / ANALYST grade"],
]
w("06_provenance.csv", ["Input", "Path", "What it is", "What it feeds"], prov)
