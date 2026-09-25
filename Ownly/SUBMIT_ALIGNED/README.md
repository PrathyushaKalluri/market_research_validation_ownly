# Ownly Gachibowli — Pre-Registered Dashboard

**Open `aligned_dashboard.html`.** Plain local HTML, no internet needed.

This folder rebuilds the study's conclusions on the project's **own pre-registered
framework**, instead of the ad-hoc framing used in `SUBMIT_TABLEAU/` and `SUBMIT_BI/`.
Every number shows where it came from and how it was calculated.

`SUBMIT/`, `SUBMIT_BI/` and `SUBMIT_TABLEAU/` are untouched.

---

## Why this folder exists

The earlier dashboards presented a **seven-tactic KEEP / ADAPT / DEPRIORITISE table**.
That framing was taken from the junior's executive summary. It is not what the project
pre-registered.

`09_analysis/kpi_system/decision_rules.md` **v1.0 — fixed 2026-09-16, before any data
existed** — defines two decision levels:

| Level | Decision | Options |
|---|---|---|
| **§2 Transferability Matrix** | Per playbook element — **six**, named in advance | KEEP · ADAPT · DROP/DEPRIORITIZE |
| **§3 Overall Hyderabad call** | The study's primary output | REPLICATE · ADAPT · LOCALIZE · INSUFFICIENT EVIDENCE |

Three specific errors in the earlier build:

1. **Seven tactics against a pre-registered six**, and they did not map. "Headline cheaper
   than Swiggy & Zomato" is messaging inside element 2.1, so it double-counted the price row.
   "Spend to match delivery speed" replaced element **2.6 Delivery reliability**, which is a
   different construct with its own thresholds. "Stock the same big chains" inverted element
   **2.5 Local restaurant supply**.
2. **The overall call was never made at all.**
3. **No evidence labels**, though `A_research_charter.md §5` makes them mandatory on every
   claim in every deliverable.

---

## What the pre-registered rules actually return

| Element | Verdict | Confidence |
|---|---|---|
| 2.1 Transparent lower price | **KEEP** | MEDIUM |
| 2.2 No / low fees | **KEEP** | MEDIUM |
| 2.3 Rapido cross-sell | **DEPRIORITIZE** | LOW |
| 2.4 Game / first-order reward | **INSUFFICIENT EVIDENCE** | LOW |
| 2.5 Local restaurant supply | **INSUFFICIENT EVIDENCE** | LOW |
| 2.6 Delivery reliability proposition | **INSUFFICIENT EVIDENCE** | LOW |

**Overall Hyderabad call: INSUFFICIENT EVIDENCE, flagged PROVISIONAL.**

| Guardrail | Breach condition | State |
|---|---|---|
| G1 | K20 saving CI includes 0 | NOT BREACHED — CI 16.9–52.6%, lower bound above 0 |
| G2 | K51 ≥ 40% | **CANNOT EVALUATE** — question A3 absent from the live instrument |
| G3 | K40 < 60% | NOT BREACHED — coverage is 90% |
| G4 | K71 ≥ 20pp | **CANNOT EVALUATE** — question A2 absent; trier base is 2 |

The call is INSUFFICIENT EVIDENCE because **§3 rule 5** triggers: the audit priced only
**one of two planned slots** (`audit_slot_quality.csv` shows `thu_lunch` with `priced = 0`),
and rules 2–4 independently fail. `decision_rules §3.5` anticipated this and says the
dashboard should report it rather than guess.

**This is the correct answer, not a failure.** Three verdicts do not depend on the missing
inputs and stand on evidence: the price advantage is real and clears its threshold, the fee
advantage is real and felt, and Rapido cross-sell is not earning its place in this sample.

---

## Two findings the earlier framing missed

**K61 — Rapido users are *less* aware of Ownly than non-users.** 33.3% (8 of 24) against
56.2% (9 of 16), a gap of **−22.9 pp**. The pre-registered rule says DEPRIORITIZE if
K61 ≤ 0, and it is. Stated plainly on the card: the interval runs −58.9 to +20.1 pp and
includes positive values, so the *direction* is not established — but the rule keys on the
point estimate, and it is applied as written rather than reinterpreted after seeing data.

**K23 = 100%, not the 81.1% reported as MM1.** They are different calculations. MM1 counts
person × basket *pairs* (107 of 132). Pre-registered K23 counts *respondents* whose stated
bar is at or below the median saving: 33 of 33, because ₹114.50 exceeds every rupee figure
anyone named. MM1 is the more conservative and more informative number — but §2.1's threshold
is written against K23, so K23 is what the verdict uses. Both are shown.

---

## A correction carried forward

The "**28% could not choose** between the two propositions" line, repeated in earlier
deliverables, is **27.5%** and sits **below** the pre-registered 35% threshold. It does not
trigger the rule it was presented as meeting. It is now reported for information only.

---

## How to rebuild

```
python3 parse_kpi_system.py     # metric_dictionary.md -> Data/00_kpi_dictionary_prereg.csv
python3 compute_aligned.py      # computes K00-K94 with full provenance
python3 apply_rules.py          # applies decision_rules.md thresholds
python3 build_aligned_data.py   # bundles everything for the HTML
```

---

## Provenance — the point of this folder

Every KPI row in section 2 expands to show:

| Field | What it gives you |
|---|---|
| **Pre-registered formula** | Quoted verbatim from `metric_dictionary.md` |
| **Calculation applied** | What was actually computed, with the numbers substituted in |
| **Source file** | Exact path, e.g. `final_dashboard/data/cleaned_survey.csv` |
| **Source columns** | Which columns were read |
| **Pre-registered source** | The survey question or instrument the dictionary names |
| **Evidence label** | observed / stated / self-reported / association |
| **Why not computable** | For the nine that return nothing — the specific missing question or base |

Every element in section 5 shows the **rule text verbatim**, the **inputs with their values**,
and the reasoning. Every problem-statement block in section 1 carries an **evidence label** and
a **source path**.

Statistical methods: Wilson score intervals on proportions; percentile bootstrap
(10,000 resamples, seed `20260921`, so reruns reproduce) on the audit median.

| File | What it is |
|---|---|
| `Data/00_kpi_dictionary_prereg.csv` | The 39 pre-registered KPI definitions, parsed from source |
| `Data/01_kpi_prereg_computed.csv` | 30 evaluated KPIs with value, interval, derivation, source |
| `Data/02_transferability_matrix.csv` | The six elements with verdict, inputs, rule and reasoning |
| `Data/03_guardrails.csv` | G1–G4 with observed values and state |
| `Data/04_overall_call.csv` | Rule-by-rule trace to the overall call |
| `Data/05_h0_result.csv` | Which H₀ test was primary and what it returned |
| `Data/06_provenance.csv` | File-level lineage for every input |
| `Data/07_problem_statement_aligned.csv` | Corrected problem statement with evidence labels |

---

## What this folder does *not* claim

Text analytics (sentiment, themes, TF-IDF) appear in section 4 as **supporting context and
are labelled as such**. They sit outside `metric_dictionary.md` and inform **no verdict** on
this page. The earlier dashboards let them read as evidence for strategic calls; here they
do not.

---

*Built 2026-09-21 · aligned to decision_rules.md v1.0 (fixed 2026-09-16, before data) ·
survey n = 40 in catchment · 30 pre-registered KPIs evaluated, 21 computed, 9 not computable.*
