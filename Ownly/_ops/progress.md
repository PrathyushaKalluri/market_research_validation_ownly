# progress.md — execution log

Earlier history (to 2026-09-14) is at `../../progress.md`.

---

## 2026-09-16, ~12:30 — Claude joins as execution lead. State assessment.

**Finding: the project has a complete research design and zero primary data.**
The last substantive file change was 2026-09-14 22:46. `08_clean_data/raw/` is empty. No audit captures,
no survey responses, no fake-door events, no interviews. Two calendar days have passed against a
three-day plan whose deadline was recorded as 17 September.

| Stream | Designed | Fielded | Data |
|---|---|---|---|
| Survey | ✅ | ❌ | 0 |
| Interviews | ✅ | ❌ | 0 |
| Price audit | ✅ | ❌ | 0 |
| Fake door | ✅ (then dropped) | ❌ | 0 |
| Secondary + review mining | ✅ | ✅ | 68 claims · 37 reviews · 524 social items |

**Read:** the binding constraint is not design quality — it is that no instrument has been put in front
of a human. Work Block 1 does nothing but fix that.

## 2026-09-16 — Claude's output this block

| Done | Artefact |
|---|---|
| Read all ~150 project files, both governing documents, all evidence CSVs | — |
| **Consolidated all coded evidence into one exhibit** + reproducible script | `01_secondary_research/consolidated/consolidated_evidence_pack.md`, `rollup_themes.py` |
| Rebuilt the survey: canonical 3-city routing, trier/non-trier branch, paired proposition test | `13_survey_v3_live/survey_logic.md`, `survey_questions.md`, `google_forms_build_guide.md` |
| Collapsed the fake door 3 arms → 2, rewrote both variants, **patched the prototype HTML** | `07_fake_door/AB_LAUNCH_RUNSHEET_v2.md`, `prototype/index.html` (v `2026-09-16.1`) |
| Compressed the interview kit to 15 min; wrote proposition cards, notes template, tracker, outreach scripts, ranked recruitment sources | `04_interviews/*_v3.*` |
| **Pre-filled 60 audit rows** (slot/platform/restaurant/basket/screenshot name) + restaurant frame + runsheet | `06_competitor_audit/AUDIT_RUNSHEET_v3.md`, `audit_captures_PREFILLED.csv`, `restaurant_frame_PREFILLED.csv` |
| Wrote 3 polls with exact copy, contamination rule, tracker | `14_quick_polls/` |
| Stood up the seven tracking files | `_ops/` |
| **Pre-registered the H₀ primacy rule before any data exists** | `_ops/decisions.md` D3 |

**Headline from the consolidation — the strongest pre-fieldwork result we have:**
> Price-doubt is **35%** of all public discussion but only **16%** of first-hand accounts.
> Fulfilment failure is **15%** of discussion but **47%** of first-hand accounts and **72%** of app
> reviews. Support/refund runs the same way: 11% → 28% → 72%.
> **What people argue about is price. What people who actually ordered report is fulfilment.**
> (Self-selected complaint sample — this says failure dominates *complaints*, not that 47% of orders fail.)

Also established: 74% of the secondary base is media report or company claim, only 24% verified, and
**Hyderabad is mentioned in 4 of 524 social items.** That gap is the project.

## 2026-09-16 — Person 3 report: serviceability answered, frame named, audit sheet live

**Task 3.1 — Ownly serviceability at DP1 (Gachibowli). ANSWERED. Q3 closed.**

| Question | Answer | What it means |
|---|---|---|
| Does Ownly deliver to DP1? | **Yes** | The audit runs in Gachibowli itself. No substitute area, no caveat on the slide. |
| Standalone app, inside Rapido, or both? | **Both** | The Rapido-distribution hypothesis is testable: survey Q7 × Q25/Q28 now has a real mechanism behind it. |
| Restaurants shown at DP1 | **221** | First observed Hyderabad supply number in the project. Compare with Bengaluru's claimed ~20–25k (company claim) — that is a **live, city-level assortment gap**, and it is ours, not a media figure. |
| Is Toing live at DP1? | **Yes** | Swiggy's budget app is already in the market Ownly is entering. The "only affordable option" framing is not available in Hyderabad. |

**Implications logged:** (a) coverage denominator for the audit is 221 listed restaurants at DP1;
(b) Toing belongs in the competitive set — record its presence per restaurant in `on_other`, and capture
Toing prices for the Group B baskets if slot 1 finishes early (not a blocker, not part of the 60-row grid).

**Task 3.2 — Group B named. ✅** R5 Murgan Tiffins · R6 Aanimuthyualu Unlimited · R7 Mehfil ·
R8 Karachi Bakery. Frame is now 10 named restaurants (4 showcase chains, 4 local, 2 national QSR).
*Fix applied:* the file had been saved with Rainbow CSV column padding (123 of 124 cells carried spaces),
which would have broken `analyze_audit_lite.py`. Padding stripped; names preserved.

**Task 3.3 — Audit sheet imported and shared. ✅** Link in `task_board.md`.

## 2026-09-17 — FIRST PRIMARY DATA: price audit slot 1 analysed

**Source:** P3 captured 37 priced checkout rows at DP1 on Wed 16 Sep, 19:45–22:00, published the sheet, and it
is mirrored into the repo as `06_competitor_audit/audit_data_slot1.csv`. Full write-up:
`06_competitor_audit/audit_slot1_results.md`. **Evidence label: FACT — observed by us.**

**The headline, and it is a better finding than "Ownly is cheaper":**

| View | Ownly cheapest | Median gap vs cheapest incumbent |
|---|---|---|
| List price + fees, **no offers** | **4 of 4** | **−30.5%** |
| **With each app's auto-offer** | 2 of 4 | **+13.9%** (Ownly dearer) |

A ₹156 Swiggy coupon turned a ₹205.80 Ownly order at Bawarchi into a ₹45 Swiggy order. The Bengaluru social
corpus predicted exactly this (18 posts: coupons erase the gap); we have now observed it in Gachibowli.
**The decisive survey variable is therefore `beh_offer_dependency` (Q13) and `beh_subscriptions` (Q12)** —
how often people actually order with a coupon decides which column they live in.

**Supporting observations (all first-party):**
- **Menu parity is real but not universal:** Ownly's menu price was lower at Shah Ghouse (−40.9%), Paradise
  (−20.3%) and Cream Stone (−5.3%), but **higher at Bawarchi (+9.5%)**.
- **Fee stack:** non-food share of the bill — Ownly **4.8%** (tax only, ₹0 delivery in 8 of 8 rows) ·
  Zomato 15.1% · Swiggy 27.4%.
- **Speed is the trade:** Ownly median ETA **39.5 min** vs Swiggy 22.5 and Zomato 17.5 → **+17 min**. This maps
  straight onto survey Q16 (₹30 cheaper vs 15 min slower).
- **Coverage:** 9 of 10 frame restaurants listed on Ownly; **Pizza Hut absent from Ownly**;
  **Aanimuthyalu Unlimited is on Ownly only**, absent from both incumbents. Ownly lists 221 restaurants at DP1.

**Caveats carried forward:** n=4 comparisons · Ownly was a **new** account (₹50 first-order offer) while
Swiggy/Zomato were **existing accounts with memberships** · Ownly's ₹0 delivery fee may be a launch condition ·
Murgan Tiffins and Mehfil have no Ownly price yet (app closed at midnight), so **every Ownly price we hold is a
showcase chain, not the under-₹150 local segment Ownly says it targets**. That gap is the first thing the
`thu_lunch` slot should close.

## Counts
| | Target | Now |
|---|---:|---:|
| Hyderabad survey responses | 80–100 | **0** |
| Bengaluru survey responses | 15–30 | **0** |
| Interviews | 8 | **0** |
| Audit captures | 60 | **37 priced rows · 4 complete 3-app comparisons · coverage on all 10** |
| Test orders | 3 | **0** |
| Fake-door visitors | 80+ | **0** |
| Poll votes | 170+ | **0** |

## Blocked on
Written ethics approval (Q2) · Ownly serviceability at DP1 (Q3) · pilot-interview verdict on Service Q (Q6)
· **the actual deadline (Q1)**.

## Next action
Work Block 1 in `task_board.md`. Report back per `_ops/report_back_template.md`.

---

## Update · 2026-09-17 — KPI architecture and decision dashboard

**Done (Claude):**
- `09_analysis/kpi_system/`:
  - `kpi_tree.md` (public-metric logic A/B/C, north-star evaluation, 10-layer tree, course-metric verdicts)
  - `kpi_data_coverage.csv` (58 rows)
  - `metric_dictionary.md` (all P0/P1)
  - `research_to_kpi_map.md`
  - `data_gap_map.md`
  - `calculation_spec.md`
  - `decision_rules.md`
- `10_dashboard/decision_dashboard/`: `dashboard_blueprint.md`, `chart_specifications.md`, `dashboard_data_schema.csv`,
  `dashboard_storyline.md`, `ownly_decision_dashboard.html` (10 pages, loads the 4 CSVs, demo data until loaded).

**P0 KPIs that cannot be computed yet:**
- K51 and K71: need survey additions A2 and A3.
- K13: fake door not deployed.
- K20, K40, K50: audit fields empty.

**Human decisions needed now:**
1. v6 or v7 goes live?
2. Add A1–A3?
3. Deploy the fake door, or declare it directional?
4. P3: complete the audit and restaurant frame.

Counts unchanged: all **0**.

---

## Update · 2026-09-18 — Challenger-failure research (why Uber Eats / Foodpanda / ONDC et al. failed)

**Done (Claude):** new folder `01_secondary_research/challenger_failures/`
- `A_ubereats_foodpanda.md` — 580 lines, 63 sources. Uber Eats India **operating loss per order
  $2.55/$2.05/$1.65 vs AOV $2.45–2.78** (SEC 8-K Ex. 99.1, FACT-grade, rarely cited). Foodpanda FY19
  RoC: revenue ₹82 Cr, loss ₹756 Cr, discounts 1.67× revenue; orders **200k/day → 5k/day (−97.5%)**.
- `B_other_challengers.md` — 692 lines, 92 sources. Amazon Food, the 2015-16 shakeout, Dunzo, ONDC,
  magicpin, Thrive, DotPe, Toing, Zepto Café. **No challenger in the Indian record has demonstrated
  post-subsidy retention.**
- `C_unit_economics_and_structure.md` — 980 lines, 75 sources, **5 primary filings extracted in full**
  (Swiggy + Eternal Q1FY27/Q4FY26). Incumbents name Ownly and Toing on the record.
- `D_synthesis_why_challengers_fail.md` — five failure mechanisms, Ownly scored against each using
  **our own audit data**, plus 5 falsifiable predictions (P1–P5) mapped to our instruments.

**The finding that matters:** our Gachibowli audit independently confirms Goyal's public diagnosis of
Ownly — *"same restaurants, similar or longer delivery times"*: **89% cross-platform overlap (K42) and
~17 min slower ETA**, measured by us. Ownly escapes the historical failure pattern on **M1 only**
(its price gap is structural, not discount-funded: non-food share 4.8% vs 15.1%/27.4%).

**Corrections forced on existing files** (see D §5): Amazon Food shut **Dec 2022** not Dec 2023;
Uber Eats deal was **$206M for 9.99%**, not $350M; the **"25–35% commission" range is untraceable to
any primary source** (Swiggy's disclosed blended take rate ~14.8%); Eternal is sunsetting GOV
disclosure, so Swiggy GOV and Eternal NOV are no longer comparable.

**Does NOT change:** H₀, the decision framework, or any KEEP/ADAPT/DROP call. No survey data yet.
Counts unchanged: all **0**.

**New audit priority raised by this work:** every Ownly price we hold is a **showcase chain**, but
Ownly's claimed target and its only defensible differentiation are **local sub-₹150 eateries**
(local coverage 100% vs chain 80%, K41). `thu_lunch` must capture Murgan Tiffins and Mehfil.

**Addendum, same day —** a fifth dossier landed: `E_restaurant_economics_and_cac.md` (641 lines,
restaurant-side economics, CCI/DG record, #Logout, CAC). It **corrected file D**: the "~14.8% blended
take rate" cited in D's first draft could not be traced to a primary filing and has been **withdrawn**.
Replaced with Swiggy's disclosed **Adj.Revenue ÷ GOV = 24.0% (FY22) → 25.6% (FY26)**, with an explicit
warning that HSIE (25.6%), HSBC-Swiggy (21.9%) and HSBC-Zomato (24.4%) use different denominators and
are not comparable. Also added FACT-grade per-order structure from Swiggy's DRHP: **cost of delivery
~14.3% of GOV vs only ~3.1% recovered from users**, contribution margin 6.40%, and the finding that
**Eternal has sunset GOV disclosure**, permanently removing the only public proxy for restaurant-funded
discounting. And: **NRAI's own president says "It's never 30%"** — the 25–35% commission range must not
be stated as fact. **Ownly's own model is contested across three outlets** (8–15% commission vs zero +
subscription vs zero + ₹30 fee); our audit observed ₹0 to the customer.

**Update · 2026-09-18 (later) — P1–P5 pre-registered.** `09_analysis/M_pre_analysis_plan.md` amended:
new **§6.7** (P1–P5 with variables, tests, effect sizes, decision rules, falsification conditions),
**§7** gains two cuts (offer-dependency band; durability-doubt band), **§8** gains a second Holm family,
**§11** restructured into *Amendments (pre-data)* vs *Deviations (post-data)* with amendment **A1**.
Reasoning in `decisions.md` **D16**. Verified pre-data: response tracker header-only, counts still **0**.

**Two blockers surfaced, both needing a human:**
1. **SRI is not computable** — PAP §4 uses `bt_trial_intent`, absent from the live v3 form. **SRI feeds
   D2 of the scorecard.** Three options in PAP §11; not patched silently.
2. **The PAP has never been frozen** (no `PAP_frozen_*.md`). Freeze it now — the pre-registration claim
   for P1–P5 depends on a dated artefact.

**Update · 2026-09-18 (later still) — SRI is worse than reported; three options drafted.**
`09_analysis/SRI_options_decision_memo.md` written. **Correction to the earlier entry: TWO of SRI's
three components are missing, not one** — `bt_trial_intent` *and* `dec_habit_lock` are both absent from
the live v3 form (no `bt_` or `dec_` variable exists in v3). SRI reduces to a **single binary item**.
The binding constraint on any rebuild is **double-counting inside D2**: (b), (c) and (d) already consume
`beh_switch_savings_required`, `beh_platforms_used_4wk` and `beh_subscriptions`, so the only
non-redundant switching items left are `prop_P_intent` / `prop_Q_intent` (Q20/Q21).
Options: **1 Drop** (pre-registered default, re-normalise D2 to 53.8/23.1/23.1) · **2 Substitute PTI =
r(max(prop_P_intent, prop_Q_intent))**, renamed, single item, D2 weights unchanged — **recommended** ·
**3 Rebuild 2-item composite** (double-counts multi-homing to ~32.5% of D2). PAP §11 corrected.
**Awaiting a human pick → D17 → then freeze.** Counts still **0**.
