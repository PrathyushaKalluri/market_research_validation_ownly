# Data-Quality Notes

Issues found during cleaning. **None of these was silently fixed.** Each is recorded with what was
done and what remains unresolved.

---

## DQ1 — Target-population scope conflict: 20–30 vs 20–35 *(unresolved, affects every survey figure)*

**The conflict.**

| Source | Stated scope |
|---|---|
| `_ops/project_context.md` (canonical) | "**20–30**-year-old students and working professionals" |
| `context.md`, charter, hypothesis tree | 20–30 |
| **The live v3 instrument** | Screens in **20–35**; bands are `20–24`, `25–29`, `30–35` |

**Why it cannot be silently fixed.** The form collected a `30–35` band. Respondents aged exactly 30
are inside the pre-registered 20–30 scope but are **trapped inside the 30–35 band and cannot be
separated from 31–35-year-olds.** The strict pre-registered population is therefore **not
recoverable** from this data.

**What was done.** Two populations are carried, never blended:

| Population | Definition | n |
|---|---|---|
| `HYD_ELIGIBLE` (**primary, used throughout the dashboard**) | all age-eligible Hyderabad respondents, 20–35 | **46** |
| `HYD_STRICT_20_30` (exploratory) | bands `20–24` + `25–29` only — **excludes all 30-year-olds** | **39** |

Every dashboard figure uses `HYD_ELIGIBLE` (n=46) and says so. The strict population is available in
`data/cleaned_survey.csv` via the `pop_HYD_STRICT_20_30` flag.

**Residual limitation, to state on any slide:** *"Results are reported for ages 20–35. The
pre-registered 20–30 scope cannot be isolated because the instrument banded 30–35 together; 6 of 46
respondents (13%) fall in that band."*

## DQ2 — An inconsistent age band appeared mid-collection

One respondent selected **`18–24`**, a band that exists in neither the v3 instrument's documented
option set nor the other responses (which use `Under 20` / `20–24`). It overlaps two documented bands.

**Treatment:** counted as eligible (it cannot be below 18 and the midpoint sits inside scope), and
flagged as `age_band_ambiguous = True`. n=1, so no result turns on it. **Likely cause:** a form edit
during collection — worth confirming with whoever edited the form.

## DQ3 — Zomato list prices were captured twice *(resolved, and it changes a headline)*

**Every** Zomato `discount_type = 'none'` capture exists twice: once with `delivery_fee = 0` and once
with the fee charged. These are not duplicates — they are the **member** and **non-member** prices of
the same basket (the audit account had Gold active).

**Treatment — documented rule in `scripts/02_audit.py`:**

| View | Rule | Meaning |
|---|---|---|
| `LIST+FEES` | `MAX(final_payable)` within `none` | non-member structural price |
| `MEMBER` | `MIN(final_payable)` within `none` | membership benefit, no coupon |
| `AFTER OFFER` | `MIN` within coupon rows | actual wallet price |

**Why it matters.** Taking the minimum indiscriminately would have reported Ownly winning **3 of 4**
baskets at a 21.0% median saving. The correct structural view is **4 of 4 at 30.5%** — matching the
project's earlier audit note. The middle view is new and is the one most respondents actually
experience, since 82.6% hold a membership.

## DQ4 — A duplicate restaurant name *(resolved)*

`Aanimuthyalu unlimited` and `Aanimuthyualu unlimited` are the same restaurant, entered with a typo.
Left unmerged they would have double-counted the coverage denominator and reported contradictory
Swiggy/Zomato listing status. Normalised in `02_audit.py`; the correction is noted on the dashboard.

## DQ5 — Two audit rows do not reconcile *(flagged, not altered)*

Two priced captures have line items that do not sum to `final_payable` (>₹1 discrepancy). They are
flagged as `recon_flag` in `data/audit_clean.csv` and **left as captured**. Both are immaterial to the
matched-basket comparisons.

## DQ6 — One implausible bill value *(field voided, respondent kept)*

One respondent reported a most-recent order total of **₹0**. The field is voided
(`amount_flag = amount_zero_implausible_field_excluded`) and excluded from spend statistics; the
respondent is retained for every other item. No value was imputed.

## DQ7 — An outlier basket excluded from one chart only *(documented)*

Karachi Bakery's captured basket is a **~₹1,200 cake**, not the single-portion basket the audit
protocol defines — the project's own audit note says to exclude it from basket-level averages. It is
excluded from the price-vs-ETA scatter (tab 6) where it compressed the axis, and it never entered the
matched-pair comparisons (no Ownly price was captured). It remains in `audit_clean.csv`.

## DQ8 — Planned survey items that do not exist in the live form *(affects one pre-registered test)*

| Planned variable | Status | Consequence |
|---|---|---|
| `beh_offer_dependency` (Q13, "of your last 10 orders, how many used a coupon") | **Absent** | **Pre-registered prediction P2 is NOT TESTABLE.** No substitute exists |
| `exp_eta_max_dinner` (stated ETA ceiling) | **Absent** | P3 tested on its `tradeoff_eta` limb only |
| `bt_trial_intent`, `dec_habit_lock` | **Absent** | See DQ9 |

## DQ9 — SRI is not computable *(open decision, blocks a scorecard dimension)*

Two of the three components of the pre-registered Switching Readiness Index are missing from the live
form. SRI reduces to a single binary item. **SRI is input (a) of D2 in the decision scorecard, at 35%
weight.**

Three costed options are in `09_analysis/SRI_options_decision_memo.md`. **No option has been chosen,
so no scorecard total is displayed anywhere in this dashboard** — showing one would require silently
picking an option. Tab 13 gives the KEEP/ADAPT/DEPRIORITISE decision from named observations instead.

## DQ10 — Base sizes that require a "DIRECTIONAL" label

| Figure | Base | Label used |
|---|---|---|
| Ownly trial | 2 of 46 | **DIRECTIONAL — LOW BASE** |
| Matched price baskets | 4 | **Directional, not a market estimate** |
| Bengaluru respondents | 12 | Context only; no inference drawn |
| Other-city respondents | 17 | Context only; excluded from all Hyderabad figures |
| App-store reviews | 37 | Self-selected; shares of coded items only |

## DQ11 — What this data structurally cannot support

Not a defect — a boundary. The following appear on the dashboard as
**NOT ESTIMABLE FROM AVAILABLE EVIDENCE** and no proxy is substituted:
CAC · CLV · true retention · market share (value or volume) · contribution margin, EBITDA or burn per
order for Ownly · actual delivery time versus quoted ETA · behavioural first-order conversion ·
restaurant-side economics in Hyderabad.

## DQ12 — Interviews exist but are undercounted and unverified *(open)*

An earlier build of this dashboard recorded **interviews = 0**, because
`04_interviews/participant_tracker_v3.csv` is header-only. That was wrong: interviews were conducted
and held outside the repository.

| Issue | State |
|---|---|
| Documented transcripts | **1** (Manichandhana Kondeboina, 2026-09-17, ~12 min) |
| Total interviews conducted | **UNKNOWN** — the PDF was supplied as "some of the interviews" |
| Verbatim verification | **None.** Gemini auto-notes; PAP §9 requires human verification before any quote is used |
| Double-coding / Cohen's κ | **Not done.** PAP §9 requires ≥20% double-coded; κ cannot be computed |
| Tracker | Still 0 rows — the repo does not reflect fieldwork that happened |

**Treatment:** findings are carried as INTERVIEW evidence and triangulated, but **no interview
finding is given a percentage or an "N of M interviewees" figure**, because the denominator is
unknown. No interview quote is placed on a dashboard slide until it is human-verified.

**Actions:** confirm the interview count, dates and segments; back-fill the tracker; verify quotes
against recordings.

## DQ13 — The survey structurally cannot see the light-user segment *(coverage gap)*

The documented interviewee orders online **~2× per semester** and prefers eating out. The survey
screens *in* people who ordered in the last 4 weeks, so this segment is **invisible to the survey by
construction**. Any statement about "Gachibowli food-delivery users" excludes the people who have
largely opted out of delivery — which is exactly the population a cheaper app might convert.

## DQ14 — Two first-order concerns the instrument does not measure *(gap)*

Interviews surfaced **hygiene/food-quality trust** ("ratings measure taste, not hygiene") and a
**"too cheap to trust" signal** ("if biryani is ₹100, is the quality good?"). Neither has a survey
item. Both are potential costs of a price-led proposition, and both are currently supported by
interview evidence alone.
