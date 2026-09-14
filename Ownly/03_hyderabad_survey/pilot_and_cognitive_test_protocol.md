# Pilot & Cognitive-Testing Protocol (both surveys)

**Version:** 2026-09-14.

**Rule: pilot data is never analysed as study data.** Pilot responses carry `meta_source = pilot` and are excluded. If the instrument changes materially after the pilot, re-pilot 2–3 people.

## 1. Who and how many

| City | Pilots | Composition | Mode |
|---|---|---|---|
| Hyderabad | 6–8 | ≥ 3 students (≥ 1 outside IIIT-H), ≥ 3 professionals; ≥ 2 occasional users; ≥ 1 with low English comfort (tests plain wording); ≥ 1 on a small phone | 4–5 **think-aloud** (video call with screen share or in person) + 2–3 **silent timed** runs on their own phone |
| Bengaluru | 6–8 | ≥ 3 current/lapsed Ownly users, ≥ 2 non-users, both occupations | 3–4 think-aloud + 3–4 silent timed |

- Pilots must meet the screener but must **not** later take the live survey. Record their initials in a private pilot sheet so they can be excluded.
- Each pilot is assigned a version; together the pilots must cover **every version** (V1–V4, B1–B2) at least once, so all routing is exercised by real people.

## 2. Timing targets

| City | Median completion target | Hard ceiling | If exceeded |
|---|---|---|---|
| Hyderabad | ≤ 14 min | 18 min for any silent pilot | Cut in this order: optional open-texts → one bill scenario (bill_s4 kept, bill_s3 folded into its stem) → one choice task per block (never a price_vs_reliability task) |
| Bengaluru | ≤ 12 min | 16 min | Cut optional open-texts → bill_s2 → one Ownly-user attitude item |

Also record the time spent on the choice-task module, the bill module and the ladder separately (think-aloud facilitator uses a stopwatch).

## 3. Think-aloud script and probes

**Opening:** "Please say out loud whatever you are thinking as you answer: what you read, what you're unsure about, why you pick an answer. There are no right answers. We're testing the questionnaire, not you."

**General probes** (use when the participant hesitates or goes silent):
- "What is this question asking you, in your own words?"
- "How did you arrive at that answer?"
- "Was any option missing for you?"
- "Was anything confusing, repetitive or uncomfortable?"

**Module-specific probes (mandatory):**

| Module | Probe | Pass criterion |
|---|---|---|
| Last-order reconstruction | "How sure are you about that amount? Did you check your app?" | Participant can recall or look up the total; the numeric format is accepted |
| Pain frequency items | "What does 'sometimes' mean to you here — how many times in 4 weeks?" | Consistent interpretation across pilots (note the ranges) |
| **Bill scenarios** | After bill_s1: "Which bill costs more in total?" (correct: neither). After bill_s2: "What is different between the two bills?" After bill_s4: "What changed compared with the previous example?" | ≥ 80% of pilots answer correctly without help. "Hypothetical" label noticed |
| **Choice-task warm-up + tasks** | After task 1: "Tell me what App A offers and what App B offers." "What made you pick that one?" After the dominance task: "Was that one easy? Why?" | ≥ 80% can restate both apps correctly; the dominance task is recognised as easy; no one reads "late in 3 of 10" as "3 minutes late" |
| **Fee ladder** | "What exactly would you be paying on top of your food here?" "Did the charge include packaging or platform fees?" | Understands one delivery charge only; taxes included; ₹220 food fixed |
| Blind concept | "In your own words, what is this service?" "What's good or bad about it?" | Paraphrase matches the card; the stated limitation (delivery time and restaurants vary) is noticed |
| Brand reveal (V1/V2) / branded concept (V3/V4) | "Did anything change for you when you saw who runs it?" | Participant understands the brand line; no confusion with Rapido rides |
| Ownly awareness (unaided) | "Did any earlier question make you think of a particular app?" | Nothing before the concept names Ownly (priming check) |

## 4. Technical checks during pilots

- Randomiser → correct version; technical fields pre-filled.
- Routing: screen-outs end correctly; Ownly-status branches; every ladder path taken by at least one pilot or by a QA tester (`wtp_gabor_granger_design.md` §6).
- Images readable on a 5.5" phone without zooming (choice-task table, bills).
- Response sheet: columns land under the expected variable names; blank where skipped.

## 5. Go / no-go criteria for launch

| Criterion | Go if |
|---|---|
| Silent-run median time | Within target (§2) |
| Comprehension of bills / choice tasks / ladder | ≥ 80% pass on each module's probe |
| Dominance task | All think-aloud pilots choose the dominant option (if any pilot fails, rework the table layout) |
| Routing errors | Zero outstanding |
| Priming | No pilot reports Ownly/Rapido being suggested before the concept section |
| Sensitive or uncomfortable items | None flagged by ≥ 2 pilots without a fix |
| Team sign-off | All 3 members approve the edit log |

## 6. Edit log template (`03_hyderabad_survey/pilot_edit_log.csv` — create when piloting)

```
edit_id,date,city,version,pilot_id,module,variable_name,issue_observed,evidence (quote/timing),change_made,old_text,new_text,affects_comparability_with_other_city (y/n),approved_by
```

- Any edit to a **core comparable item** must be applied identically to both city surveys; mark `affects_comparability_with_other_city = y` and confirm both forms are updated.
- Freeze the forms and the pre-analysis plan after the last approved edit, **before** the first live response.
