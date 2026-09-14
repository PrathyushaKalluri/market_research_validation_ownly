# F. Sample Strategy, Quotas, Recruitment & Data-Quality Controls

**Version:** 2026-09-14.

All samples are **non-probability quota samples**. Margins of error below are *precision under a simple-random-sample assumption*. They do not guarantee the sample represents the population. Calculations: two-sided α = 0.05, power 0.80, p = 0.5 (conservative). They were computed with Python stdlib, and the code is reproducible in `09_analysis/`.

## 1. Why these numbers (power reality check)

| n (valid) | MOE for a proportion | Min. detectable difference between two groups of this size (50% base) | Min. detectable Cohen's d |
|---|---|---|---|
| 50 | ±13.9 pp | 28 pp | 0.56 |
| 60 | ±12.7 pp | 26 pp | 0.51 |
| 80 | ±11.0 pp | 22 pp | 0.44 |
| 100 | ±9.8 pp | 20 pp | 0.40 |
| 125 | ±8.8 pp | 18 pp | 0.35 |
| 200 | ±6.9 pp | — | — |
| 250 | ±6.2 pp | — | — |

**What this means honestly:**

- **Students vs professionals** with ~100 each: we can detect *large* differences (~20 pp, d ≈ 0.4). A 10 pp difference (our business-significance floor) would need ~400 per group. So a null H6 result means "no large difference detected", **never** "no difference".
- **Brand arms (H7)** with ~100 per arm: the same limit applies. Only large brand effects are detectable.
- **Choice experiment:** Orme's rule of thumb is n ≥ 500·c / (t·a). With c = 3 (max levels), t = 6 tasks and a = 2 alternatives, that gives **n ≥ 125 per model**. The pooled Hyderabad model is fine at 220. Segment-specific models are **directional** unless a segment reaches ≥ 125. Otherwise use a pooled model with segment interactions.
- **Repeat-use regression (H12):** ~6–7 predictors × ≥ 10 events in the smaller outcome class needs roughly **≥ 80–100 Ownly users** (Bengaluru + Hyderabad pooled, with a city control). Below that, report bivariate results only.

## 2. Hyderabad / Gachibowli sample

**Target: 220 valid** (acceptable range 180–250). **Minimum defensible: 120 valid** (§5).

### 2.1 Quota table

| Quota dimension | Cell | Target (valid) | Hard minimum | Hard maximum | Rationale |
|---|---|---|---|---|---|
| Occupation | Student (UG/PG/PhD) | 100 | 80 | 125 | H6 power |
| | Working professional | 100 | 80 | 125 | H6 power |
| | Working student | ≤ 20 | — | 25 | Analysed separately / sensitivity; excluded from the binary H6 test |
| Ordering frequency (orders, last 4 weeks) | Frequent (8+) | 70 | 55 | — | H1.6, commercial value |
| | Regular (4–7) | 80 | 55 | — | |
| | Occasional (1–3) | 70 | 50 | — | Needed to test whether pain/switching is only a heavy-user phenomenon |
| Cross-quota (soft) | Each occupation × {frequent+regular, occasional} | ≥ 30 per cell | 25 | — | Prevents occupation being confounded with frequency |
| Locality | Gachibowli core (incl. Financial District/Nanakramguda) | ≥ 50% | 40% | — | Target-market focus |
| | Surrounding (Kondapur, Madhapur/HITEC City, Manikonda, Narsingi/Kokapet, Serilingampally, Tellapur/Nallagandla) | ≤ 50% | — | 60% | |
| Recruitment channel | Any single channel | — | — | 35% of total | Limits channel homogeneity |
| | IIIT-H | — | — | 45 respondents (≈ 45% of students) | v1 rule: IIIT-H ≠ Hyderabad students |
| | Any single employer | — | — | 15% of professionals | |
| Brand arm (randomised) | Blind / Branded | 50% / 50% (±5 pp) | — | — | H7; balance check on awareness, segment, frequency |
| Choice-experiment block (randomised) | Block 1 / Block 2 | 50% / 50% | — | — | Design balance |
| Ownly status (natural fall-out, tracked) | Tried Ownly in Hyderabad | Aim ≥ 30 | — | — | H12 Hyderabad; if < 30, qualitative only |

### 2.2 Starts needed

Assumptions *(A)*: ~25% screen-out (age, locality, no recent order) and ~12% quality exclusions. That gives **≈ 220 / (0.75 × 0.88) ≈ 335 starts**. Plan for **350–380 starts** and monitor daily.

## 3. Bengaluru sample

**Target: 150 valid** (acceptable range 120–180). **Minimum defensible: 70 valid** (40 Ownly users + 30 non-users).

| Quota dimension | Cell | Target | Hard minimum | Note |
|---|---|---|---|---|
| Ownly status | Current Ownly user (ordered Ownly in last 4 weeks) | 55 | 30 | Main benchmark group |
| | Lapsed Ownly user (tried in last 6 months, none in last 4 weeks) | 20 | 10 | **Survivorship control; do not skip** |
| | Aware, never tried | 45 | 20 | Barriers, lock-in |
| | Unaware | 30 | 10 | Cap at 40 — least useful group for this study |
| Occupation | Student / working professional | ≥ 50 / ≥ 70 | 35 / 45 | Needed for reweighting to Hyderabad composition |
| Frequency | Occasional (1–3) | ≥ 30 | 20 | Reweighting cell coverage |
| Locality | Record; flag Ownly pilot areas (Koramangala, HSR Layout, BTM Layout) | — | — | Longer-tenure users |
| Channel | Any single channel | ≤ 40% | — | Ownly-topic channels flagged for sensitivity analysis |

**Why so much effort on Ownly users:** H9 and H12 depend on them. Ownly users + lapsed = **75 target**. Pooled with Hyderabad early users, this approaches the ~80–100 needed for the H12 regression.

## 4. Recruitment plan

### 4.1 Hyderabad / Gachibowli

| Channel | Segment | Tactic | Permission / ethics | Expected valid |
|---|---|---|---|---|
| IIIT-H student groups | Students | Class/hostel groups via known contacts | Group admin OK; cap 45 | 40–45 |
| University of Hyderabad (Gachibowli campus) student groups | Students | Friends-of-friends, department/hostel WhatsApp groups | Admin permission | 25–35 |
| ISB (Gachibowli) & other nearby institutions | Students (note: ISB skews older/higher income — record and flag) | Personal referrals | Admin permission | 10–20 |
| Gachibowli/Kondapur PG & co-living groups | Students + young professionals | WhatsApp/Telegram community posts | Admin permission; no cold DMs to strangers | 25–40 |
| LinkedIn (location: Hyderabad; employers in Financial District/HITEC City) | Professionals | Team posts + personal-network outreach + alumni | No mass automated messaging | 30–50 |
| Employee communities / office clubs (via friends at IT firms/GCCs) | Professionals | Internal-group shares by an insider | Only through members; respect company policies | 25–40 |
| Co-working spaces (Financial District/HITEC City) | Professionals | Poster with QR on notice boards | Venue permission | 5–15 |
| r/hyderabad | Mixed | One post, per subreddit rules | Moderator approval if required | 10–25 |
| Snowball | Mixed | End-of-survey share link; each person refers ≤ 3 | Referral cap limits clustering | 20–40 |

### 4.2 Bengaluru (Ownly-user focus)

| Channel | Tactic | Note |
|---|---|---|
| Personal/alumni networks in Bengaluru | Ask specifically: "do you or your flatmates order on Ownly?" | Highest yield |
| LinkedIn (Bengaluru, 20–30) | Team posts with the screener in the text | |
| r/bangalore, r/bengaluru, Ownly-related threads found by Agent B2 | Post per rules; **no unsolicited DMs to commenters** | Flag Ownly-topic channel (sensitivity analysis) |
| College groups in Bengaluru (friends' institutions) | Admin-approved posts | Students |
| Snowball from confirmed Ownly users | Referral link; cap 3 | Clustered — track `meta_referrer_code` |
| Ownly/Rapido outreach (research help request) | Email/LinkedIn to company | Upside only; if they help, label that sample "company-facilitated" |

**Incentive** *(A)*: a lucky draw (e.g. 5 × ₹500 vouchers per city), entered through a **separate** form linked by a random completion code shown at the end of the survey. The survey itself stays anonymous. Interviews: ₹200–300 voucher each, if budget allows.

## 5. Minimum defensible sample (if targets fail)

| Component | Target | Minimum defensible | What is lost at minimum |
|---|---|---|---|
| Hyderabad survey | 220 | **120** (≥ 50 students, ≥ 50 professionals, ≥ 40 occasional) | Segment choice models; H7 detects only very large effects (~26–28 pp); H6 is directional |
| Bengaluru survey | 150 | **70** (≥ 40 current+lapsed Ownly users, ≥ 30 non-users) | H12 regression → bivariate only; reweighting uses 2 × 2 cells or unweighted with caveat |
| Hyderabad interviews | 14–16 | **10** (≥ 4 students, ≥ 4 professionals, ≥ 2 Ownly users/lapsed) | Saturation claims limited; JTBD with fewer segments |
| Bengaluru Ownly interviews | 5–6 (optional) | 3 | H9 mechanism evidence thinner |
| Competitor audit | 20–25 restaurants × 3 platforms × 5 slots × 2 weeks | **12 overlapping restaurants × 3 slots × 2 days × 1 drop point** (≥ 60 matched pairs) | Slot/day consistency claims |
| Fake door | Per-arm n from the MDE table (`07_fake_door/experiment_plan.md`) | Any n, **reported as DIRECTIONAL** | Winner claims |

**Rule:** if any component is below minimum, its hypotheses are **NOT TESTABLE** and are shown as such in the dashboard. They are not dropped silently.

## 6. Screening rules

| Rule | Hyderabad | Bengaluru | Action |
|---|---|---|---|
| Consent not given | ✔ | ✔ | End survey |
| Age outside 20–30 (numeric) | ✔ | ✔ | End survey; logged as screen-out |
| Doesn't live/study/work in the listed localities | ✔ (Gachibowli-area list) | ✔ (Bengaluru city) | End survey |
| No food delivery order in last 4 weeks (any app) | ✔ | ✔ — "lapsed Ownly user" means tried Ownly but no Ownly order in the last 4 weeks, while still ordering on other apps | End survey |
| Works for a food-delivery/quick-commerce/aggregator company or in market research | ✔ | ✔ | End survey (conflict of interest) |
| Already completed this survey | ✔ | ✔ | Self-report item + duplicate checks |

## 7. Exclusion rules (post-collection; details in `08_clean_data/cleaning_protocol.md`)

Rows are flagged, never silently deleted. Exclusion codes:

- `EX01_screen_fail`
- `EX02_speeder` (duration < 40% of median for that form version)
- `EX03_attention_fail`
- `EX04_straightline` (identical answers across the pain grid including a reverse-keyed item)
- `EX05_duplicate`
- `EX06_incoherent` (e.g. 0 orders but a last-order date within 4 weeks; last order total < ₹50 or > ₹5,000 without explanation)
- `EX07_bot_or_gibberish` (nonsense or copy-pasted open texts across rows)
- `EX08_missing_critical` (segment, frequency or all PPI items missing)
- `EX09_outside_target_after_recode` (locality "Other" free text recoded outside the area)

Borderline cases are adjudicated by two team members, with the decision logged.

## 8. Duplicate-response controls (Google Forms without mandatory sign-in)

Mandatory Google sign-in reduces completion and deters non-Gmail users, so it is **not** required. Instead:

1. The link randomiser appends a random `meta_session_token` in a pre-filled hidden-style field. Repeated tokens = same link session.
2. An end-of-survey completion code is shown. The lucky-draw form records the email and the code in a **separate** sheet; duplicate emails → both codes flagged (email hashed; the raw email never enters the analysis data).
3. Pattern matching: identical (age, occupation, locality, frequency, last-order total, platform) with submissions < 30 min apart → review.
4. Open-text similarity: normalised Levenshtein ratio > 0.9 on ≥ 2 open texts across rows → review.
5. Self-report: "Have you already filled this survey (any version)?"

## 9. In-field data-quality monitoring (daily, 10 minutes)

| Check | Owner | Trigger → action |
|---|---|---|
| Starts, completes, screen-out rate by channel | Person 2 / Person 1 | Screen-out > 40% in a channel → review the targeting message |
| Quota fill vs target | Person 2 / Person 1 | Cell < 50% of target at mid-field → redirect recruitment |
| Median duration by version | Person 3 | Median < 7 min (Hyderabad) → check for skip-logic errors |
| Arm/block balance | Person 3 | Imbalance > 55/45 → check the randomiser |
| Speeders / attention fails | Person 3 | > 15% → review channel quality; pause that channel |
| Open-text quality sample (10 rows) | Person 2 | Gibberish cluster → flag channel |
