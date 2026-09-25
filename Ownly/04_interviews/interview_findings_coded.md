# Interview Findings — coded

**Status change: interviews WERE conducted.** This supersedes the earlier repository state, in which
`participant_tracker_v3.csv` was header-only and the study recorded interviews as NOT CONDUCTED.

**Evidence label: INTERVIEW (primary, qualitative).**

---

## 1. What exists, and at what grade

| Source | Grade | n | Detail |
|---|---|---|---|
| **I-01 — documented transcript** | **A** — AI-transcribed notes with timestamps | 1 | Manichandhana Kondeboina, interviewer K Anil, 2026-09-17 12:25 IST, ~12 min. Source: `Meeting started 2026_09_17 12_25 IST - Notes by Gemini.pdf` |
| **Team-reported aggregate insights** | **B** — team synthesis, no transcript seen | **UNKNOWN** | Supplied by the team 2026-09-18 as "the main insights from our interviews". Participant count, dates and segments not recorded |

> ⚠ **Open item — must be closed before the deck is presented.** The total number of interviews, and
> the segment split, are **UNKNOWN**. The PDF was described as "some of the interviews", so more were
> conducted than the one documented here. Until the count is confirmed, no interview finding is given
> a prevalence figure — the prevalence rule in PAP §9 ("N of M interviewees") cannot be applied.
> **Nothing below is reported as a percentage or a count of interviewees.**

Also note the transcript is **Gemini's automatic notes, not a verified verbatim transcript**. PAP §9
requires human verification of every quote used in an output. Quotes below are marked accordingly.

---

## 2. I-01 — coded findings (documented transcript)

**Participant profile.** Student. Orders online **very rarely — ~2× per semester**; had not ordered at
all in the current semester. Default behaviour is **eating out**, because food is hot and freshly
served and the environment can be inspected.

| # | Theme | Finding | Timestamp |
|---|---|---|---|
| I-01.1 | **PRICE_TRANSPARENCY** | Core concern is **unexpected charges** — delivery fees, platform fees, charges appearing at checkout, order-value thresholds. Wants to understand *how much she is actually paying* | 00:00:00 |
| I-01.2 | **TRUST_HYGIENE** | **Ratings measure taste, not hygiene.** Cannot verify restaurant cleanliness through an app; eating out allows visual inspection | 00:00:00 |
| I-01.3 | **FOOD_CONDITION** | Packaging condensation makes food oily and soft on arrival | — |
| I-01.4 | **SPEED_vs_PRICE, hunger-conditional** | Prefers **shorter delivery** because a long wait "defeats the purpose of ordering" and would push her to eat out instead — **but this flips with hunger.** When very hungry, speed wins; when not, the cheaper option wins | 00:01:50, 00:03:06 |
| I-01.5 | **CHECKOUT_PREFERENCE (stimulus test)** | Shown the **same item from the same restaurant on two apps**, she chose the one showing **₹150 with free delivery** over **₹272 with extra charges** — for lower total *and* cost transparency | 00:04:53 |
| I-01.6 | **SEGMENTATION (respondent's own)** | Splits the market herself: **premium customers value time over money**; **students, middle-class families and frequent orderers prioritise price**. Predicted the cheaper app would become more popular | 00:06:00 |
| I-01.7 | **GROUP_ORDERING** | Students **pool orders** — one friend holds Zomato Gold, another uses Swiggy; they compare final totals and order on whichever gives the better deal (₹100 off, % discounts) | 00:07:41 |
| I-01.8 | **LOW_PLATFORM_LOYALTY** | No loyalty to a platform; compares on the deal available **at the moment of ordering** | 00:07:41 |
| I-01.9 | **AWARENESS — word of mouth** | Heard about Ownly **from her brother**. Had not used it; **not available at her location** | 00:07:41 |
| I-01.10 | **TOO_CHEAP_SIGNAL** | A very low price raises a **food-quality doubt** — "if biryani is ₹100, is the quality good?" | 00:09:08 |
| I-01.11 | **SPEED tolerance** | For a student, **30 vs 40 minutes is not a major concern**; price matters far more | 00:09:08 |

**I-01 core insight (as recorded):** *food delivery is mainly a value-driven decision — she compares
platforms on final price and available discounts, while food quality and hygiene determine whether she
trusts the service; delivery speed matters mainly when she is very hungry.*

## 3. Team-reported aggregate insights (grade B, no transcript)

| # | Theme | Insight as reported |
|---|---|---|
| T-1 | **TRADE-OFF HIERARCHY** | General: **hunger, time ≫ money.** Students: **hunger, money ≫ time** |
| T-2 | **PRICE_DURABILITY_DOUBT** | On Ownly's offers — *"what if they increase later"* |
| T-3 | **PRICE ANCHOR** | **₹10 per km** is the reference point for delivery pricing |
| T-4 | **TRIAL TRIGGER** | Switching to a new app comes from a **friend's recommendation**; also **Instagram and YouTube reviews, and regular advertising** |
| T-5 | **CHURN TRIGGER** | People leave an app after **frequent bad orders** |
| T-6 | **TRUST SOURCE** | Trust comes from **influencers and word of mouth** |

## 4. Triangulation against our own survey and audit

| Interview finding | Survey / audit evidence | Verdict |
|---|---|---|
| I-01.1, T-2 — hidden charges are the core pain; doubt that low prices last | Survey: **89.1%** agree a new app's low prices rise once popular (n=46). Audit: Ownly non-food load **5.2%** vs Swiggy **28.3%** | **CONVERGES — strongly** |
| I-01.5 — chose the transparent, lower-total option in a two-app stimulus | Audit: Ownly wins **4/4** baskets on list+fees, median **₹114**. Survey: observed saving clears **100%** of stated thresholds | **CONVERGES.** Note I-01.5 is a *constructed stimulus*, structurally like our survey trade-offs — treat as stated preference, not behaviour |
| I-01.11, T-1 (students) — 30 vs 40 min is not a major concern | Survey: **84.8%** took ₹230/45-min over ₹260/30-min (n=46) | **CONVERGES — strongly.** Both independently falsify pre-registered prediction P3 |
| **T-1 — general users weight time over money; students weight money over time** | Survey by segment: students **87.5%** (28/32) vs working professionals **81.8%** (9/11) chose cheaper+slower; **Fisher p = 0.637 — no detectable difference.** But switching threshold differs directionally: **students ₹30 vs professionals ₹50** (medians) | **PARTIALLY SUPPORTED / UNDERPOWERED.** The segment split is **not confirmed** on the speed trade-off — but n=11 professionals cannot detect anything short of a very large effect. The threshold difference is consistent with the interview's direction. **Do not present T-1 as validated** |
| I-01.7, I-01.8 — group ordering, no loyalty, compares deals at order time | Survey: **82.6%** hold a membership, **58.7%** multi-home. Audit: incumbent coupons erase Ownly's advantage in **50%** of baskets; membership alone in **25%** | **CONVERGES — and supplies the mechanism.** The audit showed coupons erase the gap; the interview explains *how* — students deliberately route orders through whoever holds the subscription |
| I-01.9, T-4, T-6 — trial comes from friends, influencers, Instagram/YouTube | Survey: **84.6%** of Rapido users had not noticed food inside the Rapido app; Ownly trial **4.3%**; the most-cited trial trigger after price was *"a friend telling me it works well"* | **CONVERGES — and reframes the discovery problem** (see §5) |
| **T-5 — churn comes from frequent bad orders** | Survey: **67.4%** accept worse reliability for ₹30. Reviews: fulfilment failure in **72.4%** of coded app-store reviews, **49.5%** of first-hand accounts | **RESOLVES AN APPARENT CONTRADICTION** (see §5) |
| I-01.2, I-01.10 — hygiene unverifiable; a very low price signals low quality | **No survey item measures either.** Not in the instrument | **UNIQUE TO INTERVIEWS — an evidence gap the survey cannot fill** |
| I-01 — orders ~2×/semester, prefers eating out | Survey: all 40 Hyderabad orderers ordered in the last 4 weeks (screened in) | **DIVERGES — by design.** The survey screens *in* recent orderers, so it structurally cannot see the light/non-user segment I-01 represents. **A real coverage gap** |
| T-3 — ₹10/km delivery anchor | Audit observed Ownly delivery fee **₹0** in 8 of 8 rows; no distance data captured | **NOT TESTABLE** with current data |

## 5. The two findings that change the analysis

### 5.1 Reliability is a **churn** driver, not a **trial** blocker

The study carried an unresolved contradiction: the survey said **67.4% would accept worse reliability
for ₹30**, while **72.4% of coded app-store reviews** are about fulfilment failure. T-5 resolves it:

> People will *accept* a reliability risk when choosing an app. They *leave* after **frequent bad
> orders** actually happen.

These are different decision moments — a prospective trade-off versus a retrospective pattern. Both
findings can be true at once. This directly supports the project's diagnostic proposition
(*price may acquire; execution may retain*) and gives it a mechanism rather than an assumption.
**Consequence:** reliability belongs in the retention guardrail, not the acquisition hook — which is
where tab 12 already placed it, now with interview support rather than inference.

### 5.2 Discovery runs on word of mouth, not on in-app placement

The dashboard measured an **84.6% Rapido discovery gap** and treated in-app placement as the lever.
T-4, T-6 and I-01.9 point somewhere else: trial comes from **a friend's recommendation, influencers,
Instagram and YouTube**. I-01 heard about Ownly **from her brother** — not from the Rapido app she
may already use.

**Consequence:** "fix the placement inside Rapido" is probably the *wrong* first experiment. The
higher-value test is a **referral / creator-led trial mechanism**. This changes a recommendation on
tab 13 and reorders the test list.

## 6. What the interviews still cannot support

- **No prevalence.** Interview count is UNKNOWN; nothing here is a percentage.
- **No Ownly experience.** I-01 had never used Ownly (unavailable at her location). Consistent with
  the survey, where zero of 40 recent orderers had ordered on Ownly in four weeks.
- **Not verbatim-verified.** The transcript is Gemini's automatic notes. PAP §9 requires human
  verification before any quote goes in an output.
- **No double-coding.** PAP §9 requires ≥20% double-coded with Cohen's κ. This is an AI first pass on
  one transcript and a team summary — **κ cannot be computed**.

## 7. Actions required

1. **Confirm how many interviews were conducted**, with dates and segments. Until then the INTERVIEW
   column of the evidence matrix carries findings but no prevalence.
2. **Human-verify I-01's quotes** against the recording before any appears on a slide.
3. **Add a hygiene / food-quality item** to the instrument — interviews surfaced it as a first-order
   trust concern and the survey is blind to it.
4. **Add a "too cheap to trust" probe.** I-01.10 and T-2 both suggest Ownly's low price carries a
   quality-doubt cost that the price-advantage framing does not capture.
5. **Reconsider the light-user segment.** The survey screens in recent orderers; I-01 orders twice a
   semester and prefers eating out. That segment is invisible to our survey by construction.
