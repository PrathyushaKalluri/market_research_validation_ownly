# Survey v3 (LIVE) — Section & Branch Map

**Status:** build-ready, 2026-09-16. Supersedes `03_hyderabad_survey/SHORT_survey_7min_google_form.md`
(which was Hyderabad-only and predates the canonical 3-city routing in the orchestrator prompt §T).
**One Google Form.** Everything below is implemented with Forms' native "Go to section based on answer".

## Respondent burden
| Path | Sections seen | Questions | Target time |
|---|---|---:|---:|
| Hyderabad (deepest) | S1→S2→S3→S4→S5→S6→**S7**→S8→S9 or S10→S13 | 26–28 | **~8 min** |
| Bengaluru (benchmark) | S1→S2→S11→S11a or S11b→S13 | 12–14 | ~4 min |
| Other city (exploratory) | S1→S2→S12→S13 | 6 | ~2 min |
| Screened out | S1→S2→S0 | 3 | <1 min |

## Branch map

```
S1  Consent ─── No ──────────────────────────────────────────────► S0 Not eligible (END)
 │ Yes
 ▼
S2  UNIVERSAL SCREENER
    Q2 age ──── Under 20 / Over 30 ─────────────────────────────► S0 Not eligible (END)
    Q3 orders in last 4 weeks ──── None ────────────────────────► S0 Not eligible (END)
    Q4 CITY ──┬── Hyderabad ────────────────────────────────────► S3   (PRIMARY VALIDATION)
              ├── Bengaluru ────────────────────────────────────► S11  (BENCHMARK)
              └── Other city ───────────────────────────────────► S12  (EXPLORATORY, short)

┌─ HYDERABAD PATH ───────────────────────────────────────────────────────────────┐
│ S3  Catchment + segment   Q5 area ── "Somewhere else in Hyderabad" → stays in   │
│                            (flagged out_of_catchment, NOT screened out)         │
│ S4  Your last order                                                             │
│ S5  Ordering habits + pain                                                      │
│ S6  Trade-offs (3 forced choices)                                               │
│ S7  ★ PAIRED PROPOSITION TEST  ← the H₀ instrument                              │
│ S8  Brand reveal + Ownly awareness                                              │
│      Q_own_aware ── "No" ──────────────────────────────────────► S13 (END)      │
│      Q_own_tried ─┬─ Yes ──────────────────────────────────────► S9  triers     │
│                   └─ No / browsed only ───────────────────────► S10 non-triers  │
│ S9  Ownly triers ─────────────────────────────────────────────► S13             │
│ S10 Ownly non-triers ─────────────────────────────────────────► S13             │
└────────────────────────────────────────────────────────────────────────────────┘

┌─ BENGALURU PATH (benchmark) ───────────────────────────────────────────────────┐
│ S11 Ownly trial split                                                           │
│      Q_blr_tried ─┬─ Yes ─────────────────────────────────────► S11a users      │
│                   └─ No ───────────────────────────────────────► S11b non-users │
│ S11a / S11b ──────────────────────────────────────────────────► S13             │
└────────────────────────────────────────────────────────────────────────────────┘

┌─ OTHER CITY (exploratory) ─────────────────────────────────────────────────────┐
│ S12  6 questions ─────────────────────────────────────────────► S13             │
└────────────────────────────────────────────────────────────────────────────────┘

S13 Source question → SUBMIT
```

## Why S7 is built the way it is

The primary H₀ compares a **Bengaluru-style** proposition against a **Hyderabad-localized** proposition.
There are two ways to test it and we are running **both**, because each covers the other's weakness:

| | Fake-door landing page | Survey Section 7 |
|---|---|---|
| Design | **Between-subjects**, random A or B | **Within-subject**, both shown, order randomised |
| Outcome | CTA click (behavioural, costless) | Stated first-order intent + forced choice |
| Test | Two-proportion z / Fisher's exact | **McNemar** on discordant pairs + forced-choice binomial |
| Strength | Real action, not self-report | Very high power at small n; guaranteed sample |
| Weakness | Needs ≥80 visitors or it says nothing | Stated intent inflates; order/demand effects |

**Pre-registered primacy rule (fixed 2026-09-16, before any data):**
- If the fake door reaches **≥ 80 unique eligible visitors with ≥ 30 per arm**, it is the **primary** H₀ test
  and Section 7 is confirmatory.
- Otherwise Section 7's McNemar test is the **primary** test and the fake door is reported as
  **directional only**, with its n stated on the slide.
- Whichever is primary, **both results are shown.** If they disagree, that disagreement is the finding
  (a gap between what people say and what they do) and neither is suppressed.

Order within S7 is randomised by **Shuffle option order OFF, but the two proposition blocks are presented
in a fixed order with a counterbalance question** — see `google_forms_build_guide.md` §7 for the exact
one-form implementation (we do **not** build two form copies; that splits the sample and loses the pairing).

## Analysis segments preserved end to end
`city` (never blended) · `seg_occupation` (student / professional) · `scr_area` (in-catchment / out) ·
`rapido_user` (yes / no) · `own_tried` (trier / non-trier) · `seg_freq` (light / regular / heavy).

## Screen-out policy
Screen-outs still submit (they hit S0 → Submit) so we can compute the recruitment funnel:
starts → eligible → complete, per `meta_found_survey` channel. Do **not** delete these rows.
