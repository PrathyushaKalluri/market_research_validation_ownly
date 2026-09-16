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
