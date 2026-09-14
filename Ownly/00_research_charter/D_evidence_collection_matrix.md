# D. Evidence & Data-Collection Matrix + Data-Source Map

**Version:** 2026-09-14.

**Legend:** **P** = primary evidence for the hypothesis; **S** = supporting / triangulating; blank = not used.

## 1. Hypothesis × method matrix

| Hypothesis | HYD survey | BLR survey | HYD interviews | BLR interviews (optional) | App reviews | Reddit / LinkedIn / social | Competitor audit | Fake door | Secondary |
|---|---|---|---|---|---|---|---|---|---|
| H1 Problem intensity | **P** pain frequencies, abandonment, offer dependency | S (matched comparison) | **P** bill-shock & abandonment incidents | | S complaint themes | S | S verified markup | | S fee landscape |
| H2 Price value | **P** choice tasks, bill comparison, switching threshold | S Ownly users' perceived savings | S | S | S price/value comments | S user-posted bill comparisons | **P** actual total gaps | S framing | S company claims (labelled) |
| H3 Price vs ETA | **P** choice tasks, ETA expectations | S | **P** trade-off incidents | | S ETA complaints | S | **P** ETA shown | | |
| H4 Price vs reliability | **P** choice tasks, RSS, incidents | S Ownly incidents | **P** late/cancel/refund incidents | S | **P** reliability/refund severity | S | S optional test orders | S reliability framing variant | |
| H5 Price vs restaurant choice | **P** choice tasks | S | S restaurant-missing incidents | | S assortment comments | S | **P** coverage | | S restaurant-count claims |
| H6 Students vs professionals | **P** all items by segment | S | **P** segment contrast | | | | | S mini-survey segment | |
| H7 Brand effect | **P** randomised arms | S Bengaluru trust items | S brand reactions | | S Rapido spillover mentions | **P**-qual Rapido trust narratives | | | S Rapido reputation media |
| H8 Fee WTP | **P** fee ladder | S | S | | S fee complaints | S | **P** actual fees | | S fee anchors |
| H9 Transferability | **P** matched items | **P** Ownly drivers, churn | S | **P** | **P** city-tagged themes | **P** city-tagged themes | S HYD conditions | | S context differences |
| H10 Assortment threshold | **P** ADI, types needed | S | S | S | S | S | **P** coverage | | |
| H11 Intent vs behaviour | **P** aware→tried; framing preference | S | S | | | | | **P** CTR, higher-intent | |
| H12 Repeat use | S Hyderabad Ownly users | **P** Ownly users (regression) | S Ownly users | **P** | **P** churn/repeat signals | S | | | |

## 2. Research question × evidence convergence requirement

A conclusion is **HIGH confidence** only if it is supported by at least two *independent* source types, one of which is quantitative (survey, audit or fake door), and no strong contradicting evidence is left unexplained. Details are in `11_insights/decision_framework_and_scorecard.md` §5.

| RQ | Minimum evidence for a HIGH-confidence answer |
|---|---|
| RQ1 pain | Hyderabad survey prevalence + interviews (≥ 3 interviews, ≥ 2 segments) |
| RQ2 why incumbents | Hyderabad survey criteria + interviews |
| RQ3 switch triggers | Survey threshold / choice tasks + interviews on past real switches (+ fake door directional) |
| RQ4 price proposition | **Audit (mandatory)** + choice tasks/threshold |
| RQ5 trade-offs | Choice tasks + interviews or reviews |
| RQ6 fee WTP | Fee ladder + audit fee context |
| RQ7 brand | Randomised arms + interviews/social |
| RQ8 Bengaluru drivers | Bengaluru Ownly-user survey + reviews/social (+ Bengaluru interviews if run) |
| RQ9 transfer frictions | Reviews/social themes + Hyderabad expectations/audit |
| RQ10 segments | Survey tests with controls + interviews |
| RQ11/12 | Scorecard with no dimension scored on LOW evidence alone |

## 3. Data-source map

| Source | Owner (role) | Access method | Raw format → location | Cadence | Unit of analysis | Evidence label | Known limitations |
|---|---|---|---|---|---|---|---|
| Secondary / web | Person 1 (Agent A support) | Public web; URL + date + exact claim | `01_secondary_research/evidence_table.csv` | One-time + re-check before final | Claim | FACT / COMPANY CLAIM / MEDIA REPORT | Company PR repeated by media; stale dates |
| Bengaluru survey | Person 1 | Google Form (sheet export) | CSV → `08_clean_data/raw/blr_survey_raw_YYYYMMDD.csv` (read-only) | Daily export during field | Respondent | Primary (stated/recalled) | Convenience sample; Ownly-user survivorship |
| Hyderabad survey (4 versions) | Person 2 | 4 Google Forms + link randomiser | CSVs → `08_clean_data/raw/hyd_survey_v{1-4}_raw_YYYYMMDD.csv` | Daily export | Respondent; long tables for choice tasks / fee ladder | Primary | Quota sample; awareness contamination |
| Interview screener | Person 2 | Google Form (separate, contains contact info) | Private team drive only; **never** in the project repo | Rolling | Candidate | PII — restricted | Self-selection |
| Interviews | Person 2 (+ Person 3 second coder) | Zoom/Meet/in-person, recorded with consent | Transcripts (de-identified) → `04_interviews/transcripts/` ; coded → `04_interviews/coded_segments.csv` | Rolling | Coded segment / incident | Primary qualitative | Not prevalence; interviewer effects |
| App-store reviews | Agent B1 → Person 1 validates | Public endpoints | `05_review_mining/app_stores/reviews_raw.csv`, `reviews_coded.csv` | One pull + refresh before final | Review | CONSUMER-GENERATED | Self-selected; extreme skew |
| Reddit / LinkedIn / social | Agent B2 → Person 1 validates | Public pages via search; no logins | `05_review_mining/social/social_raw.csv`, `social_coded.csv`, `search_log.csv` | One pull + refresh | Post / comment | CONSUMER-GENERATED / COMPANY CLAIM (execs) | LinkedIn PR skew; small n |
| Competitor audit | Person 1 + Person 3 | Manual app capture, synced clocks; screenshots | `06_competitor_audit/data/audit_obs.csv` + `screenshots/` | 2 weeks × 5 slots | Observation (restaurant × basket × platform × slot × drop point × account state) | FACT (observed at timestamp) | Personalised offers; not realised prices |
| Fake door | Person 3 | Static page + Apps Script → Google Sheet | `07_fake_door/data/events_raw.csv` | Fixed window (e.g. 10 days) | Session / event | Behavioural (low stakes) | Low traffic; channel mix; no purchase |
| Analysis mart | Person 3 | Python pipeline | `08_clean_data/cleaned/*.csv`, `09_analysis/outputs/` | After field close | Per `10_dashboard/dataset_schema.md` | Derived | Inherits all of the above |

## 4. Traceability rules

1. Every number in the dashboard or slides has a `source_id`: a dataset + filter + script, or an `evidence_id` from the secondary table.
2. Raw exports are immutable. Record a SHA-256 hash per raw file in `08_clean_data/raw/MANIFEST.csv`.
3. Every derived table is produced by a script in `09_analysis/`. No manual spreadsheet edits to cleaned data.
4. Qualitative insights cite `interview_id` + `segment_id`, or `review_id` / `item_id`.
