# AI First-Pass Transcript Coding Prompt (copy-paste)

**Use:** optional acceleration for first-pass coding of **redacted** transcripts. The output is a **draft**. A human coder must review every row, fill `reviewed_by`, and correct it before any synthesis. AI output is never the final coding, and AI may never supply quotes that are not in the transcript.

**Before using:**
- [ ] The transcript is redacted (no names, phone numbers, addresses, employers, order IDs).
- [ ] The tool's data-retention/training settings have been checked, and participants consented to processing (`consent_and_privacy.md` §D).
- [ ] Paste the current codebook (from `coding_framework.md` §3–4) into the prompt where indicated.
- [ ] One transcript per run (keeps timestamps and context accurate).

---

## PROMPT (copy everything below this line)

You are assisting a university research team with FIRST-PASS qualitative coding of one interview transcript about food-delivery behaviour in Hyderabad/Bengaluru. Your output will be checked line-by-line by a human researcher. Accuracy and traceability matter more than completeness.

### Hard rules (follow all)
1. **Verbatim only.** `verbatim_quote` must be copied character-for-character from the transcript below, including any "[redacted]" markers. Never paraphrase inside `verbatim_quote`, never merge sentences from different places, never invent or "clean up" wording. Maximum 40 words per quote. If there is no exact quote, leave it empty.
2. **Timestamps.** Every row must carry the timestamp shown in the transcript at the start of that segment. If the transcript has no timestamps, use the line number prefixed `L` (e.g. `L112`). Never estimate a timestamp.
3. **Separate observation from interpretation.** `observation` = what the participant reported happening or doing, in neutral past tense, with no explanation of why beyond what they said. `interpretation` = your analytic reading, starting with "INTERPRETATION:", and marked uncertain if it is.
4. **Behaviour vs talk.** Set `evidence_kind` to one of: past_incident, habitual_behaviour, show_me_observed, opinion, stated_intent, hearsay. Anything about what they *would* do is `stated_intent`. Reactions to the concept card (Service X / Ownly) are `stated_intent` or `opinion`, never behaviour.
5. **Use only the codebook codes provided.** If a meaningful segment fits no code, use `NEW-<SHORTNAME>` and explain it in `interpretation`. Do not force-fit.
6. **Severity** (1–4) only from a consequence the participant actually reported (1 irritant, 2 changed the order, 3 order/money lost, 4 reduced/stopped using a platform). If no consequence was stated, leave it blank.
7. **Leading questions.** If the interviewer's question suggested the answer, add a row with speaker = I, code `META-LED-QUESTION`, and mention in the next participant row's interpretation that the answer may be primed.
8. **Uncertainty.** If you are unsure about a code, recency, or meaning, append `[UNSURE: reason]` to `interpretation`. Do not guess recency or frequency; leave them blank.
9. **No invented facts.** Do not add amounts, app names, times or reasons not in the transcript. Do not infer demographics; copy the segment fields from the header supplied.
10. **Counter-evidence matters.** Code segments that contradict price-led or Ownly-favourable expectations with the same care as supporting ones (e.g. VALUE-NOT-PRICE, RELIABILITY-PREMIUM, SUBSCRIPTION-LOCKIN, RAPIDO-TRUST-NEG).

### Inputs
- INTERVIEW HEADER (copy from interview log): interview_id=___; seg_occupation=___; seg_freq=___; dem_living=___; primary_platform=___; ownly_status=___; guide_version=___
- CODEBOOK: <<PASTE coding_framework.md §3 codes + definitions + include/exclude, and §4 severity scale>>
- INCIDENT TYPES: bill_unreasonable, abandon, late, cancel, wrong_or_missing_item, spill_quality, refund, support_contact, restaurant_missing, cheaper_disappointed, eta_changed_plan, switch_episode, tradeoff_save, tradeoff_pay, subscription_decision, ownly_trial, ownly_issue, other
- TRANSCRIPT: <<PASTE REDACTED TRANSCRIPT WITH TIMESTAMPS>>

### Output format
**Part 1: CSV** (no commentary inside), with exactly this header, one row per meaning segment (a segment = the smallest stretch describing one incident, reason or reaction; it may carry several codes separated by semicolons). Wrap any field containing commas in double quotes.
```
interview_id,segment_id,timestamp,speaker,verbatim_quote,observation,interpretation,codes,hypothesis_link,incident_type,evidence_kind,recency,stated_frequency,severity,behavioural_consequence,seg_occupation,seg_freq,dem_living,primary_platform,ownly_status,coder,reviewed_by,memo_ref
```
- `segment_id` = interview_id + "-" + 3-digit sequence (001, 002…)
- `hypothesis_link` ∈ H1…H12 (semicolon-separated) or `none`
- `recency` ∈ this_week, this_month, 1-3_months, older, unclear (only if stated)
- `behavioural_consequence` ∈ none, changed_order, abandoned, switched_app_once, reduced_use, stopped_platform, complained, recommended, other
- `coder` = `AI-draft`; `reviewed_by` = empty; `memo_ref` = empty

**Part 2: Coder notes** (after the CSV, max 250 words):
- (a) Candidate NEW codes with a one-line definition and segment_ids
- (b) Say–do contradictions spotted (segment_ids for both halves)
- (c) Segments you were least sure about (segment_ids + why)
- (d) Evidence that cuts against the idea that lower total price drives switching (segment_ids), or "none found"
- (e) Any place the transcript looked incomplete, garbled or unredacted (line/timestamp) so the human can fix it

Do NOT write insights, recommendations, personas, or JTBD statements. The human team does synthesis.

---

## Human review checklist (after AI output)
- [ ] Spot-check 100% of `verbatim_quote` values against the transcript (Ctrl+F each). Delete any row whose quote isn't found exactly.
- [ ] Check that `evidence_kind` for every concept-card segment is not a behaviour category.
- [ ] Re-segment where the AI merged two incidents or split one.
- [ ] Confirm severity is consequence-based; blank it where no consequence was stated.
- [ ] Add missed segments (AI often under-codes brief incumbent-positive remarks).
- [ ] Fill `reviewed_by`. Log the AI-vs-human change rate (rows changed / total) in the memo log as a method note.
