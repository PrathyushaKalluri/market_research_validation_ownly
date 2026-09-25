# decisions.md — material decisions, with reasoning

Earlier decisions (to 2026-09-14) remain at `../../decisions.md`. Nothing there is overturned except
where stated below.

---

## D1 · 2026-09-16 — The fake door is reinstated, and becomes the primary H₀ instrument

**Decision:** The fake-door landing A/B, dropped on 14 Sep, is back and is the pre-registered primary
test of H₀, subject to the sample rule in **D3**.

**Evidence used:** The orchestrator brief (§J, §R) defines H₀ as a *first-order conversion* comparison
between a Bengaluru-style and a Hyderabad-localized proposition. A survey-only design cannot produce a
conversion rate — only stated intent.

**Alternative rejected:** Keeping it dropped and testing H₀ on survey intent alone. Rejected because
stated intent is systematically inflated and the whole point of the hypothesis is *conversion*.

**Why the 14 Sep reasoning no longer holds:** it was dropped for lack of time to accumulate traffic and
for ethics-approval friction. The page, the collector, the analysis script and the disclosure flow were
all completed on 14 Sep and have sat unused since — the build cost is now zero, and the ethics
application already covers it. What remains is ~45 minutes of hosting work.

**Implication:** Person 3 gains the deploy task. `07_fake_door/AB_LAUNCH_RUNSHEET_v2.md` created.

---

## D2 · 2026-09-16 — Three fake-door arms collapse to two

**Decision:** `A_total_price` / `B_transparent_bill` / `C_reliable_value` → **`A_blr_total_price`**
(Bengaluru playbook) and **`B_hyd_local_reliable`** (Hyderabad-localized). `PAGE_VERSION` → `2026-09-16.1`.

**Evidence used:** realistic traffic is 100–150 visitors. Three arms give ~40 each — too thin for any
test to resolve a difference. Two give ~55–75, the minimum at which a ~15-point gap is detectable.

**Alternative rejected:** keeping all three to also test transparency-vs-amount. That question is
preserved inside survey Section 7's optional `prop_reason` free text, at zero sample cost.

**Implication:** A and B now map **exactly** onto H₀ rather than approximately onto three hypotheses.
`prototype/index.html` patched; the 3-arm version archived as `index_v1_3arm_ARCHIVE.html`.

---

## D3 · 2026-09-16 — H₀ is tested twice, and which one is primary is fixed NOW, before any data

**Decision, pre-registered before a single response exists:**
- Fake door reaches **≥ 80 unique eligible visitors with ≥ 30 per arm** → the fake door is the
  **primary** H₀ test (two-proportion z, or Fisher's exact if any expected cell < 5); survey Section 7
  is confirmatory.
- **Otherwise** → survey Section 7 is primary (exact binomial on the forced choice, McNemar on the
  paired intent) and the fake door is reported as **directional only, with its n on the slide.**
- **Both results are always shown.** If they disagree, the disagreement — a gap between stated and
  revealed preference — is reported as a finding, and neither is suppressed.

**Why this is written down today:** choosing the primary test *after* seeing which one gave the nicer
p-value is the most common way a student project fabricates a result. Fixing the rule in advance is the
only thing that makes either number worth printing.

**Implication:** the rule appears identically in `13_survey_v3_live/survey_logic.md`,
`07_fake_door/AB_LAUNCH_RUNSHEET_v2.md` and here. If it changes, it changes in all three with a reason.

---

## D4 · 2026-09-16 — The survey is rebuilt with canonical three-city routing

**Decision:** `03_hyderabad_survey/SHORT_survey_7min_google_form.md` (Hyderabad-only) is superseded by
`13_survey_v3_live/`. One form, routed by `scr_city` into Hyderabad (deep, ~26 Q) / Bengaluru
(benchmark, ~12 Q) / Other city (exploratory, 6 Q), then by Ownly trial status.

**Evidence used:** orchestrator §T declares the three-city routing a fixed project decision. The
14 Sep design dropped Bengaluru entirely for want of recruitment time.

**Alternative rejected:** a separate Bengaluru form. Rejected — it doubles build and distribution work
for a sample we expect to be 15–30, and splits the response sheet.

**Why the 14 Sep reasoning no longer holds:** the objection was to a *full* Bengaluru survey. A 12-question
benchmark branch inside the existing form costs ~7 minutes of extra build time and no extra distribution
channel — friends in Bengaluru get the same link.

**Implication:** the Bengaluru branch is benchmark evidence only. It is **never** pooled into the
Hyderabad H₀, and under n=20 it is reported as raw counts with no percentages.

---

## D5 · 2026-09-16 — Section 7 is within-subject, and the order effect is declared rather than hidden

**Decision:** every Hyderabad respondent sees **both** propositions, rates both, then makes a forced
choice. The **forced choice** (`prop_forced_choice`, options shuffled) is the primary within-survey
outcome; McNemar on the paired intent ratings is secondary.

**Evidence used:** at n≈80 a between-subjects split gives two arms of ~40 — badly underpowered. A
within-subject paired design uses every respondent for both conditions and is far more powerful at
small n. The brief's own Hyderabad question list (§T2) asks each respondent for **both** proposition
reactions, so this matches the canonical design.

**Known weakness, stated on the slide rather than buried:** Google Forms cannot randomise section order,
so P is always shown before Q. This is why the forced choice — less order-sensitive than two sequential
ratings, and with its options shuffled — is the primary outcome, and why the **fake door is the properly
randomised between-subjects version of the same test.** The two designs cover each other's weakness.

**Alternative rejected:** building two form copies to randomise. Rejected — it halves an already small
sample, destroys the pairing, splits the response sheet, and doubles the build.

---

## D6 · 2026-09-16 — Service Q's copy is provisional until the pilot interviews land

**Decision:** the Hyderabad-localized proposition (survey Service Q, fake-door variant B) is **v0**,
derived from this project's consolidated secondary evidence. It must be re-checked against the first
two interviews before the form is shared, and revised if they point elsewhere.

**Evidence used:** the brief requires the localized variant to come from early interviews, not desk
research. v0 is built from the strongest desk signal available — fulfilment failure at 47% of first-hand
accounts and support/refund at 28%, plus assortment — so it is a defensible starting point, not a guess.

**Implication:** this is a real dependency, not a formality — **P1 task 1.4 waits on P2 task 2.3.**
If interviews 1 and 2 surface a different dominant concern (payment methods, cash on delivery and meal
cards are the live candidates in the social data), the weakest bullet is swapped and logged here.

---

## D7 · 2026-09-16 — No duplicate project workspace is created

**Decision:** the `ownly_hyd_market_validation/` folder tree specified in the orchestrator brief §C is
**not** created. The existing `00_`–`12_` structure is kept, and the seven mandated tracking files live
in `_ops/`.

**Evidence used:** the brief's own §B rule 6 — extend an existing file rather than create a
near-duplicate. The existing tree already contains every folder the specified tree calls for, with ~150
populated files in it.

**Alternative rejected:** building the specified tree and copying files across. Rejected — it would
create two of everything one day before a deadline, break every relative path in the analysis pipeline
and the deploy instructions, and produce no research value.

**Implication:** the brief's structure is satisfied in substance. `_ops/file_manifest.md` maps each
specified path to where the thing actually lives.

---

## D8 · 2026-09-16 — Polls and the survey never share a group

**Decision:** poll groups and survey groups are two disjoint, written-down lists. Poll results are
reported separately and never pooled into any survey n.

**Evidence used:** Poll 1 asks the price-vs-reliability-vs-assortment question directly; someone who
has just voted on it would answer Section 7 differently. Poll 2 names Ownly, which destroys the
brand-blind sequencing the whole instrument depends on.

**Implication:** P2 task 2.5 produces both lists **before** anything is posted.

---

## D9 · 2026-09-16 — Surveys v3 and v5 merge into a single v6; v6 is the form we build

**Decision:** `Survey_v6_Google_Form_Build_Guide.md` is the only survey to build. v3's build guide is
replaced by a pointer; v5 is upgraded in place rather than rebuilt (Part 12 of the v6 guide).

**Evidence used:** two complete survey designs existed by this evening. v5 (built 18:17) is a strong
funnel instrument — city routing, per-platform order counts, a four-way Ownly funnel status, Sean Ellis
PMF, trial drivers — and is already written in a copy-paste format the team can work from. But it
contains **no proposition test**: no Service P vs Service Q, nothing that compares a Bengaluru-style
framing against a Hyderabad-localized one. That is the H₀ instrument. Fielding v5 alone would leave the
primary hypothesis resting entirely on the fake-door page, which D3 already says becomes unusable below
80 visitors.

**Alternative rejected:** fielding both forms. This is the one clearly wrong option — it splits an
80-response target into two halves, and neither half answers its own question.

**Alternative rejected:** keeping v3 and discarding v5. v5's revealed order counts are strictly better
than v3's stated "next 10 orders" allocation, and its funnel status is a cleaner awareness→trial
measure than v3's two-question equivalent.

**What v6 is:** all of v5, plus two brand-blind sections inserted between *Your last order* and the
Ownly reveal — **Quick choices** (three ₹30 trade-offs + switching threshold) and **Two services**
(P intent, Q intent, forced choice, why, repeat-without-offer, price durability). Hyderabad and
Bengaluru get both; Other city gets neither, since it is appendix-only context. 28 sections → 32.

**Deliberate cuts from v3, to hold the length at ~6 minutes:** food-only subtotal (the audit measures
fee share by observation, which beats recall), next-10-orders allocation (superseded by v5's actual
order counts), and the separate ₹100-reward question for non-triers (folded into S7-Q5, asked once of
everyone instead of duplicated across three branches).

**Implication:** the brand-blind ordering rule now has a build consequence — sections 6 and 7 **must**
sit before section 8, or the proposition test is contaminated by the Ownly name. It is on the
pre-share checklist and in the common-mistakes table. If v5 responses already exist, the guide says to
stop and log the break rather than add questions mid-collection.

---

## D10 · 2026-09-16 — Poll questions folded into the survey; one poll survives

**Decision:** the three WhatsApp polls become **one**. Poll 3 (bill fairness) moves into Survey v6 as
**S5-Q4**, Poll 1 (which lever makes you switch) is dropped as redundant, and Poll A (Ownly awareness)
is kept. Memberships is added to v6 as **S3-Q2** at the same time. Survey v6 goes from 39 to 41 unique
questions; length stays ≈6 minutes.

**The rule applied:** *if you would ever want to say "…among students" or "…among people with a
membership", the question belongs in the survey.* Poll answers cannot be joined to any other answer —
a poll returns a bar chart and nothing else. Almost every case is settled by that constraint alone.

**Evidence used, question by question:**
- **Poll 1** was redundant. v6's S9-Q1 already ranks the same levers across 7 options on a *screened*
  sample, and Section 6 tests the same three levers properly — one variable at a time with ₹30 held
  constant. The poll forced a single choice between four unlike things, which is a weaker question, not
  a faster one.
- **Poll 3** exposed a real gap: v6 had **no fee-pain question at all**. The v3→v6 merge had dropped
  v3's whole pain grid. Promoted to S5-Q4, placed directly after the amount question so the answer is
  anchored to a bill the respondent has just recalled rather than to a general mood.
- **Memberships** was appearing only as an answer *option* inside two other questions ("happy with my
  current app or membership", "went back to my Swiggy One / Zomato Gold membership"). A paid membership
  is the strongest single reason not to switch apps, so it should be a segment we cut by, not an
  anecdote. Added as S3-Q2, before the branching question, which stays last in that section.

**Why Poll A (awareness) survives:** it needs all three of these to be true, and it is the only question
for which they are. (1) The survey's awareness figure is **biased upward and cannot be fixed from inside
the survey** — people who click a food-delivery survey are more likely to know food apps. A one-tap poll
reaches people who would never open a 6-minute form, and **the gap between the two numbers is itself the
finding**: it is the only honest read we have on the direction of our own sampling bias. (2) Awareness is
a bare prevalence question — it is the rare case needing no cut. (3) The poll can plausibly return 200+
votes against the survey's ~80 (±11 points).

**The cost that made this decision sharp:** D8 requires poll groups and survey groups to be disjoint,
because a poll primes the frame the survey measures. So **every group spent on a poll is a group lost for
the survey.** Against an 80-response target with a handful of group permissions, two redundant polls were
buying nothing and costing real sample.

**Implication:** P2's task 2.6 drops from two polls to one, freeing group permissions for survey
distribution. Poll and survey awareness numbers are reported side by side and **never merged**.
`14_quick_polls/exact_poll_copy_v1_3polls_ARCHIVE.md` keeps the original three.

---

## D11 · 2026-09-16 — v6 is cut down to a lean v7; v7 is the form we build

**Decision:** `Survey_v7_Google_Form_Build_Guide.md` replaces v6. Sections drop from 32 to 9 and the
longest path from 33 questions to 20. Every city follows one path.

**Evidence used:** people testing v6 said it felt overwhelming: too many sections, 7–8-option lists, and
questions that asked the same thing more than once. A form that people quit halfway through loses more
data than it gains from extra questions.

**Rule applied:** keep what people *did* (order frequency by app, amount paid, funnel stage, repeat use,
what they'd have done otherwise) and the single H₀ forced choice. Cut questions that repeat another
question, and hypothetical questions about the future.

**Consequences, stated rather than buried:**
- D3's secondary test (Try P vs Try Q, McNemar) is dropped. The primary forced-choice test is unchanged.
- Order counts become bands (0 / 1–2 / 3–5 / 6+), so share-of-orders uses band midpoints.
- Service Q now has the same wording in both cities and 3 bullets, matching P. This removes v6's
  bullet-count asymmetry, but the Hyderabad test no longer names the city in the headline.
- Channel attribution ("where first heard") moves entirely to the fake-door links.

---

## D12 · 2026-09-17 — KPI system and decision dashboard adopted; project north-star proxy fixed; 3 survey additions proposed

**Decision:**
1. KPI system in `09_analysis/kpi_system/`. The master prompt's `05_analysis/`, `06_dashboard/` and `01_plan_tracking/`
   map to `09_analysis/kpi_system/`, `10_dashboard/decision_dashboard/` and `_ops/`, because those number prefixes are
   already used in this repo.
2. **Project north-star proxy = K00 Repeat-active Ownly customers per 100 food-delivery users.** This is our proxy, not
   Ownly's metric: **no official Ownly/Rapido north-star metric has been published** (public-source check, 2026-09-16).
   Guardrails: K20 basket saving, K51 fulfilment failure, K40 restaurant coverage, K71 promo-dependency gap.
3. Decision rules (`decision_rules.md`) are fixed **before any data exists**.
4. Proposed minimal survey additions to v6: **A1 Rapido usage, A2 offer on first Ownly order, A3 fulfilment failures**
   (`data_gap_map.md` §3).

**Evidence used:** three sweeps: public sources, data instruments, and existing analysis design. Key facts:
- No primary data has been collected on any stream.
- There is no Rapido-usage question in v5, v6 or v7.
- There is no fulfilment-experience or offer-on-first-order question.
- The fake door is not deployed, and its D3 stopping date has passed.
- Public sources confirm Rapido-app integration in **Bengaluru only**, and a 50%-off (≤ ₹100) first-order offer.
- No public source was found for any ₹50/₹100 game, bottom-nav placement, or burn/order. The repo's "₹150–170 burn" and
  "FIFA offer" are unverified: do not cite them.
- A 2026-09-11 employee post places the Hyderabad launch around early September.

**Alternatives rejected:**
- A composite "market attractiveness" score: the weights would be arbitrary.
- Adding next-10-orders back: past counts (S4) are better evidence than stated allocation.
- A survey question on the ₹50/₹100 game: its existence is unverified.

**Open team decision (not Claude's to make):** v6 or v7 goes live. D11 chose v7, but the latest user instruction built on
v6. The KPI system assumes **v6 + A1–A3**. If v7 is fielded, it must also restore S7-Q5 (`data_gap_map.md` §4).

**Supersedes:** `10_dashboard/dashboard_blueprint.md` (2026-09-14, choice-experiment design) as the build spec. It is kept
as history.

---


## D13 · 2026-09-17 — Field survey v6 with two Rapido questions; A2/A3 not added

**Decision (user instruction):** v6 is the live form, which overrides D11 (v7). It gets two one-tap Rapido questions and nothing else:
- **S3-Q3 Rapido usage:** "In the last 4 weeks, how often did you use Rapido (bike, auto or cab)?"
- **S8-Q1 Food inside the Rapido app:** "Have you seen an option to order food inside the Rapido app?" It sits after the
  brand-blind sections, so it doesn't prime P vs Q.

No new sections and no branching changes.

**Not added, to keep the form simple:** A2 (offer on first order) and A3 (fulfilment failures).
**Consequence:** K71 (promo-dependency gap) and K51/K52 (fulfilment failure) show INSUFFICIENT EVIDENCE on the dashboard.
The promotion and reliability rows fall back to K32 (stated repeat without offer), K24 (reliability trade-off), the audit
ETA gap, and interview codes.

---
## D14 · 2026-09-17 — One live set: v6 + 2 Rapido questions, their KPI system, their dashboard. Everything else archived.

**Decision (user instruction, closes the open question left in D12):**

| Thing | Live | Archived |
|---|---|---|
| Survey | **v6 + the two Rapido questions** (D13) | v3, v4, v5 and **all v7 files** |
| KPI framework | **`09_analysis/kpi_system/`** (58 rows, P0/P1/P2) | `KPI_Framework_and_Survey_Validation.md` (the 9-KPI set) |
| Dashboard | **`10_dashboard/decision_dashboard/`** | `ownly_transfer_scorecard.html` |
| Fake door | `07_fake_door/` — unchanged, 2 arms, live page | — |
| Price audit | `06_competitor_audit/audit_data_slot1.csv` + `audit_slot1_results.md` | — |

**Why v7 is archived rather than fielded:** D11 chose v7 for length, but v7's cuts removed questions the
adopted KPI system depends on, and P1 has already published a v6-based form. Two live survey specs in one
repo is how a team builds the wrong instrument the night before a deadline.

**Why the 9-KPI framework is archived rather than merged:** both frameworks are defensible, but a deck can
only tell one story, and the KPI system is the one the dashboard is built against. The audit work already
done feeds it directly — K20, K21, K22, K26, K40, K41 and K42 all draw on `audit_data_slot1.csv`.

**Nothing is deleted.** Everything moved to `archive/2026-09-17_superseded/` with a README explaining what
each file was and what replaced it, because the path from v3 to v6 is part of the method story.

**Supersedes:** D11 (v7 is the form we build). D13 stands.

---

## D15 — Fake door v3 is built and runs on ₹1,000 of Meta ads over 48 hours (2026-09-17)

**Decision (user chose Option B in `07_fake_door/FAKE_DOOR_REDESIGN_v3.md` §7):**
- The live page is rebuilt to v3: **A `A_everyday_low_price`** vs **B `B_discount_led`**, page version `2026-09-17.v3`.
- Distribution: **one neutral Meta ad → the same plain link**; the page randomises (sticky 50/50 per browser).
  No per-arm ads, no `?v=` links in public.
- Stop: **Sat 19 Sep 2026 00:00 → Mon 21 Sep 2026 00:00 IST**, no early stop. Replaces the 30 Sep / 300 rule for v3.
- K13 is **directional**; **K14 stays primary** (expected ~20–50 visitors per arm).
- Post-tap costly action is a **one-tap question** (try without an offer / only with an offer / not for me), not a
  WhatsApp number, so the page and sheet stay personal-data-free and the collector needs no redeploy.

**Details:** `07_fake_door/FAKE_DOOR_v3_RUNBOOK.md`. **Supersedes:** the v2 arms and v2 stopping rule in
`AB_LAUNCH_RUNSHEET_v2.md`.

**D15 amendment (2026-09-17, user instruction):** the research disclosure panel is removed. After the tap the page
shows a Buffer-style "Coming soon — we're not taking orders in Gachibowli yet"; the "Research study" tag, the
university footer and "if this existed" wording are gone. Page version `2026-09-17.v3b`; analyse v3b only.

---

## D16 — Challenger-pattern predictions P1–P5 are pre-registered as a SECONDARY family (2026-09-18)

**Decision:** fold the five predictions from
`01_secondary_research/challenger_failures/D_synthesis_why_challengers_fail.md` §6 into the PAP as a new
**§6.7**, with exact variables, tests, effect sizes, decision rules and falsification conditions.

**Why now, and why this is still legitimate pre-registration.** The predictions were generated from a
pattern in *other companies'* histories (Uber Eats India, Foodpanda, Amazon Food, ONDC, Thrive, DotPe).
If they were written down after our own results arrived, they would be a story fitted to the data.
`13_survey_v3_live/survey_response_tracker.csv` was **header-only (zero rows)** on 2026-09-18 and
`progress.md` records counts "all 0" through 2026-09-17, so registration precedes the data. Logged as
**amendment A1** (pre-data), explicitly distinguished from a **deviation** (post-data) in PAP §11.

**Three judgement calls, with reasons:**

1. **Separate Holm family, not added to the ★16.** Merging 5 tests into the confirmatory family would
   raise the multiplicity burden on the 16 hypotheses the study exists to test. Cost: study-wide error
   is not controlled *across* the two families. That cost is stated in PAP §8 rather than hidden, and is
   the reason P1–P5 may support a recommendation but never drive one.
2. **P2's direction is pre-registered *with* its plausible reversal.** High coupon-dependence could mean
   "the coupon already erases Ownly's gap" (our prediction) **or** simply "more price-motivated" (the
   opposite). Both readings are written down now so a reversal counts as falsification instead of being
   reinterpreted afterwards.
3. **P3 gets a one-directional inference.** Q16 tests a **15-minute** gap; the audit observed **~17 min**
   (Ownly 39.5 vs Swiggy 22.5 / Zomato 17.5). Failing at 15 implies failing at 17; the converse does not
   hold. Stated in §6.7 so the asymmetry is not read backwards.

**What this does NOT change:** H₀, the ★ confirmatory set, the five scorecard dimensions, or any
KEEP/ADAPT/DROP call. No survey data exists.

**Blocking item surfaced while doing this (needs a human decision):** PAP §4's **SRI** formula uses
`bt_trial_intent`, which **does not exist** in the live v3 instrument — a mismatch between the 14 Sep PAP
and the 16 Sep form. **SRI is therefore not computable as written, and SRI feeds D2 of the decision
scorecard.** Options in PAP §11; deliberately not patched silently.

**Also outstanding:** the PAP has **never been frozen** — no `PAP_frozen_*.md` exists. The
pre-registration claim for P1–P5 rests on a dated frozen artefact, so freeze it now.

---

## D17 · SRI — take Option 1 (Drop), the pre-registered default

**Date:** 2026-09-21 · **Status:** DECIDED · **Classification:** Deviation (post-data), not an amendment

**Decision.** Drop SRI. Re-normalise D2 to **53.8 / 23.1 / 23.1** across components (b), (c), (d), exactly
as `M_pre_analysis_plan.md` §11 already specifies as the default. Report **PTI** —
`r(max(prop_P_intent, prop_Q_intent))` — as a **labelled exploratory supplement** that informs no
KEEP/ADAPT/DROP call and enters no scorecard dimension.

**This overturns the recommendation in `09_analysis/SRI_options_decision_memo.md`,** which recommended
Option 2 (substitute PTI into D2 at the designed weights). The reason is the memo's own mandatory
precondition, not a disagreement with its reasoning:

> *"If you pick Option 2, one sequencing rule is mandatory: finalise Service Q's copy against the pilot
> interviews first, then freeze the PAP. PTI is defined on Q20/Q21, so freezing before Q's wording is
> settled would make the pre-registration hollow."*

Service Q's copy is fielded and its responses are collected. That precondition can no longer be met in
either order. Choosing Option 2 now would mean **selecting a scorecard component after seeing the data
it scores** — the precise failure mode pre-registration exists to prevent. Option 1 requires no
post-hoc judgement because the PAP had already named it as the fallback.

**What this costs, stated plainly.** D2 now rests largely on the ₹-threshold question
(`beh_switch_savings_required`). The memo is right that this discards the only other usable switching
signal the instrument collected. We accept a thinner D2 in exchange for a D2 that was not chosen
against the data. PTI still gets reported — it just does not get to move a recommendation.

**Why not Option 3.** Unchanged from the memo: it double-counts multi-homing to roughly 32.5% of D2.

**Reversible?** Yes, and the reversal must be explicit. If a reader prefers Option 2, D2 recomputes
from PTI, which is reported alongside. Nothing is hidden by this choice.

---

## D18 · Freeze the PAP as a tiered retrospective snapshot

**Date:** 2026-09-21 · **Status:** DONE

**Artefact:** `09_analysis/PAP_frozen_2026-09-21.md`
**SHA-256:** `5ada2f3a83bd5337fcef4758e0ca8fb05d786dca0322030fd32020e06f63938f`

The PAP had never been frozen. Freezing it today and dating it today would present a post-data
document as a pre-registration. Instead the freeze carries a provenance block that separates what can
be proved from what is merely asserted:

- **Tier A** — §1–§6.6, §7–§10: committed at `83ff55f`, **2026-09-14 23:42:19 +0530**, before the
  instrument went live (2026-09-16). Git-dated, independently verifiable.
- **Tier B** — §6.7 (P1–P5), the §7 cuts, the §8 second Holm family, the §11 restructure: written
  2026-09-18, uncommitted until now. Pre-data status rests on `_ops/progress.md` self-attestation only;
  the raw survey export is untracked, so nothing corroborates the ordering. **P1–P5 are reported as
  pre-specified but not independently verifiable, and carry no confirmatory claim alone.**
- **Tier C** — D17 above: post-data, logged as a deviation.

**Lesson recorded for the next study:** freeze before fielding, and commit the frozen file, so the
provenance question never has to be argued.
