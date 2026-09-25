# 00 — Repository Inventory

**Audited 2026-09-18.** Every artefact below was opened and inspected. Files not relevant to the
Gachibowli market-fit question are excluded rather than listed for completeness.

Legend — **Quality:** A = primary/observed or filing-grade · B = coded primary with known bias ·
C = single-source or self-selected · D = template/empty.

---

## 1. Survey data

| Path | Type | Geography | Date | n | State | Quality | Answers | Does NOT answer |
|---|---|---|---|---|---|---|---|---|
| `Ownly Survey.csv.zip` → `Ownly Survey.csv` | SURVEY — primary | Hyderabad / Bengaluru / other | to 2026-09-18 | **113 raw** | RAW | A | Stated behaviour, stated preference, ₹30 trade-offs, P-vs-Q concept choice, Ownly funnel | Actual conversion, actual retention, actual spend |
| → `final_dashboard/data/cleaned_survey.csv` | derived | as above | 2026-09-18 | **75 cleaned** | CLEANED | A | Analysis populations | — |
| → `final_dashboard/data/excluded_survey.csv` | derived | — | — | **38 excluded** | EXCLUDED | A | Screen-out audit trail | — |

**Branch structure.** The Google Form routes to three parallel question blocks. Branch 1 = Hyderabad
(72 reached the age item), branch 2 = Bengaluru (16), branch 3 = other city (25). Column suffixes
`.1` / `.2` in the export are the Bengaluru and other-city copies of the same questions, **not**
duplicate responses.

**Analysis populations:** `HYD_ELIGIBLE` n=46 · `HYD_CATCHMENT` n=37 · `BLR_ELIGIBLE` n=12 ·
`OTHER` n=17. Bengaluru and other-city bases are too small for inference and are used for context only.

## 2. Survey instruments

| Path | Purpose | Note |
|---|---|---|
| `13_survey_v3_live/survey_questions.md` | The live v3 instrument | **Authoritative.** Matched against the export column-by-column |
| `13_survey_v3_live/survey_logic.md` | Branching and screen-out logic | Confirms the age screen |
| `03_hyderabad_survey/`, `02_bangalore_survey/` | Earlier v1–v2 designs | Superseded; not used |
| `archive/2026-09-17_superseded/` | v4–v7 drafts | Superseded; not used |

## 3. Price / competitor audit

| Path | Type | Geography | Date | n | Quality | Answers | Does NOT answer |
|---|---|---|---|---|---|---|---|
| `06_competitor_audit/audit_data_slot1.csv` | **PRIMARY OBSERVED** | Gachibowli DP1 | 2026-09-16 19:45–22:00 | 79 rows, **37 priced** | A | Final payable, fee stack, quoted ETA, listing coverage | Actual delivery time, lunch/late-night slots, other addresses |
| `06_competitor_audit/audit_slot1_results.md` | Prior analysis | " | 2026-09-17 | — | A | Reproduced and extended here | — |
| `06_competitor_audit/test_orders_template.csv` | Template | — | — | **0** | D | — | Promised-vs-actual delivery time |

**Matched comparisons: 4** complete three-platform baskets. Directional, not a market estimate.

## 4. Review and social data

| Path | Type | n | Quality | Answers | Does NOT answer |
|---|---|---|---|---|---|
| `05_review_mining/app_stores/reviews_coded.csv` | CONSUMER-GENERATED, coded | **37** | C | What dissatisfied users complain about | Failure **rates**; anything about Hyderabad |
| `05_review_mining/social/social_coded.csv` | CONSUMER-GENERATED, coded | **524** (420 relevant, 123 first-hand) | C | Themes, durability scepticism, Toing comparisons | Population incidence; Hyderabad (4 mentions only) |
| `05_review_mining/social/social_analysis.md` | Prior synthesis | — | C | Theme families | — |

**Both are self-selected toward complaint.** Counts are shares of coded items mentioning a theme.

## 4b. YouTube — audience comments *(new, 2026-09-18)*

| Path | Type | n | Quality | Answers | Does NOT answer |
|---|---|---|---|---|---|
| `05_review_mining/youtube/h6PJ_QB4CiQ_comments.json` | CONSUMER-GENERATED, verbatim | **77** of 81 | C | Post-launch audience reaction (Mar 2026) | Population incidence |
| `05_review_mining/youtube/2EI51Z7WQ3o_comments.json` | CONSUMER-GENERATED, verbatim | **199** of 250 | C | Pre-launch reaction (Jun 2025) | Population incidence |
| `05_review_mining/youtube/youtube_findings.md` | Agent dossier | — | C | Video content, coding, provenance | — |
| `final_dashboard/data/youtube_comments_coded.csv` | Coded output | 275 | C | Theme shares weighted by likes | — |

Both videos are from **Backstage with Millionaires**. Transcripts **could not be retrieved**
(`timedtext` requires a PO-token; mirrors returned 403/bot-checks), so the creator-written
descriptions were used and are labelled as such. **National, not Gachibowli.** Self-selected viewers
of Rapido-favourable explainers — treat as a map of public argument, not of user experience.

## 5. Interviews — CONDUCTED *(corrected 2026-09-18)*

An earlier version of this inventory recorded interviews as NOT CONDUCTED, because the repository's
tracker was empty. **That was wrong** — interviews were run and held outside the repo.

| Path | Type | Date | n | Quality | Answers | Does NOT answer |
|---|---|---|---|---|---|---|
| `~/Downloads/Meeting started 2026_09_17 12_25 IST - Notes by Gemini.pdf` | **INTERVIEW — documented transcript** | 2026-09-17 | **1** (Manichandhana Kondeboina, ~12 min) | A | Mechanism: hunger-conditional speed preference, checkout transparency, group ordering, word-of-mouth awareness, hygiene distrust, "too cheap" signal | Prevalence of anything |
| Team-reported aggregate insights | **INTERVIEW — team synthesis** | 2026-09-18 | **UNKNOWN** | B | Trade-off hierarchy by segment, ₹10/km anchor, trial and churn triggers, trust sources | Prevalence; no transcript seen |
| `04_interviews/interview_findings_coded.md` | **Coded output (new)** | 2026-09-18 | 14 coded findings | B | Triangulation against survey and audit | — |
| `04_interviews/participant_tracker_v3.csv` | Tracker | — | **still 0 rows** | D | — | — |

**Open item:** the **total interview count is UNKNOWN** — the PDF was supplied as "some of the
interviews". Until it is confirmed, no interview finding is given a percentage or an "N of M" figure,
per PAP §9. The transcript is **Gemini auto-notes, not human-verified verbatim**, and there is no
double-coding, so Cohen's κ cannot be computed.

**Two findings changed the analysis** (see `04_interviews/interview_findings_coded.md` §5):
reliability is a **churn** driver rather than a trial blocker, and discovery runs on **word of mouth**
rather than in-app placement.

## 6. Fake door — NOT EXECUTED

| Path | State |
|---|---|
| `10_dashboard/schema/fact_fakedoor_events.csv` | **Header only, 0 events** |
| `07_fake_door/FAKE_DOOR_v3_RUNBOOK.md`, `experiment_plan.md`, `landing_page_copy.md`, `prototype/` | Design complete, never fielded — D |

**Consequence:** the behavioural H₀ (first-order conversion) is **NOT DIRECTLY TESTED**. No substitute
is claimed.

## 7. Secondary research

| Path | Type | Claims | Quality |
|---|---|---|---|
| `01_secondary_research/evidence_table.csv` | 68 labelled claims | 50 MEDIA REPORT, 10 COMPANY CLAIM, 5 FACT, 5 contradicted | B/C |
| `01_secondary_research/secondary_research_report.md` | Synthesis + corrections | — | B |
| `01_secondary_research/market_price_anchors.md` | Fee/price anchors | — | C |
| `01_secondary_research/ownly_restaurant_and_user_segments.md` | Segment claims | 31 COMPANY CLAIM of 60 | C |
| `01_secondary_research/consolidated/consolidated_evidence_pack.md` | Cross-source rollup | — | B |

## 8. Challenger-failure research

| Path | Content | Sources | Quality |
|---|---|---|---|
| `01_secondary_research/challenger_failures/A_ubereats_foodpanda.md` | Uber Eats India SEC 8-K per-order economics; Foodpanda RoC filings | 63 | **A** (filings) |
| `.../B_other_challengers.md` | Amazon Food, TinyOwl, Dunzo, ONDC, magicpin, Thrive, DotPe, Toing, Zepto Café | 92 | B |
| `.../C_unit_economics_and_structure.md` | Swiggy/Eternal filings, take rates, platform fee, cohort retention, CCI | 75 | **A** (filings) |
| `.../D_synthesis_why_challengers_fail.md` | 5 mechanisms scored against our own data; P1–P5 | — | B |
| `.../E_restaurant_economics_and_cac.md` | Commission evidence, CCI record, #Logout, CAC | — | B |

## 9. Hypotheses, plans and logs

| Path | Content |
|---|---|
| `_ops/project_context.md` | **Authoritative** business question and H₀ |
| `00_research_charter/C_hypothesis_tree.md` | H1–H12 with thresholds |
| `09_analysis/M_pre_analysis_plan.md` | PAP, incl. **§6.7 pre-registered P1–P5** and §11 amendment log |
| `09_analysis/SRI_options_decision_memo.md` | Open decision: SRI is not computable |
| `11_insights/decision_framework_and_scorecard.md` | Pre-registered 5-dimension scorecard |
| `_ops/decisions.md`, `_ops/progress.md`, `_ops/open_questions.md` | Decision and state logs |
| `08_clean_data/cleaning_protocol.md`, `master_data_dictionary.csv` | Cleaning rules |

## 10. Existing dashboard assets

| Path | State | Used? |
|---|---|---|
| `10_dashboard/ownly_v6_dashboard.html`, `decision_dashboard/ownly_decision_dashboard.html` | Prototypes carrying **DEMO DATA** | **No** — superseded by `final_dashboard/` on real data |
| `10_dashboard/schema/*.csv` | Schema stubs, mostly empty | Schema reference only |
| `09_analysis/kpi_system/` | KPI tree, coverage, formulas | **Yes** — KPI ids (K20/K21/K22/K40/K42) reused |
| Tableau files | **None found** | — |
| `06_competitor_audit/screenshots/` | Audit screenshots | Provenance only |

## 11. Explicitly excluded from analysis

| Path | Why |
|---|---|
| `Marketing Metrics 1000 Records.csv` | Generic digital-campaign data, **not Ownly data**. Method illustration only |
| `Formulae Sheet*.docx/.pdf`, `Team02_A6.docx` | Course reference material |
| `archive/food_beverages_and_ordershield_track/` | Retired project track |
| Root `13_`–`17_` files | Superseded v1 framing |

---

## What the inventory establishes

1. **Two of four planned primary streams do not exist.** Interviews (0) and fake door (0).
2. **The survey is the only population-level primary evidence**, at n=46 for Hyderabad.
3. **The audit is observed but thin** — one slot, one address, 4 matched baskets.
4. **Secondary research is 74% media/company claim**, which is why it frames rather than decides.
5. **No file in the repository contains Ownly CAC, CLV, retention, burn or market share.** These are
   not computed anywhere in this dashboard.
