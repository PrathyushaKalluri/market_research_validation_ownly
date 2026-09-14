# Interview Coding Framework and Qualitative Synthesis Method

**Version:** v2, 2026-09-14. Replaces root `14_ownly_research_design.md` §8.
**Approach:** hybrid (abductive) thematic analysis. We start from **deductive seed codes** tied to H1–H12, then add **inductive codes** that emerge from the transcripts. Coding sheet: `coded_segments_template.csv`. AI first pass (optional): `transcript_analysis_prompt.md`. Every AI-coded row must be human-reviewed.

**What → why → how → analysis → decision**
Coded transcript segments → turn 14–16 conversations into traceable, countable evidence without losing context → hybrid codebook, two coders on ≥20% → code frequency by segment, JTBD, switch forces, synthesis ladder → insight evidence matrix rows (interview column) and dashboard View 7.

---

## 1. Unit of coding
- **Coding unit = one "meaning segment":** the smallest stretch of talk (usually 1–5 sentences) that describes **one incident, one reason, or one reaction**. A segment may carry several codes.
- Every segment keeps an `interview_id`, `segment_id` (`HYD-07-012`), `timestamp` and `speaker` (P = participant, I = interviewer).
- **Interviewer speech is coded only** to flag leading questions (`META-LED-QUESTION`), which lets us discount the answer that follows.
- Code **incidents** (things that happened) separately from **opinions/intent** (evaluative or hypothetical statements) using the `evidence_kind` tag (§3). This is the main defence against treating talk as behaviour.

## 2. Coding-sheet columns (`coded_segments_template.csv`)
| Column | Content | Rule |
|---|---|---|
| interview_id | HYD-## / BLR-## | |
| segment_id | interview_id + 3-digit sequence | |
| timestamp | mm:ss in the recording/transcript | Required for any quote |
| speaker | P / I | |
| verbatim_quote | Exact redacted words | **Copied from the transcript, never retyped from memory.** No quote → leave blank. |
| observation | What happened, stated as fact **as reported** (e.g. "Abandoned a ₹310 Zomato cart at checkout on a weekday dinner after seeing the fee total") | No adjectives or explanations |
| interpretation | Analyst reading, prefixed `INTERPRETATION:` | Optional. Never merged into observation/quote. |
| codes | Semicolon-separated codebook codes | ≥1 |
| hypothesis_link | H1…H12 (semicolon-separated) or `none` | |
| incident_type | From the §3 list or `n/a` | |
| evidence_kind | past_incident / habitual_behaviour / show_me_observed / opinion / stated_intent / hearsay | |
| recency | this_week / this_month / 1-3_months / older / unclear | Incidents only |
| stated_frequency | e.g. "2–3×/month" as said, or blank | |
| severity | 1–4 (§4) | Pains/incidents only |
| behavioural_consequence | none / changed_order / abandoned / switched_app_once / reduced_use / stopped_platform / complained / recommended / other | |
| seg_occupation, seg_freq, dem_living, primary_platform, ownly_status | Copied from the log | Enables segment roll-ups |
| coder | Initials (or `AI-draft`) | |
| reviewed_by | Human initials | Required before synthesis |
| memo_ref | Link to memo ID | Optional |

## 3. Deductive seed codebook (tied to H1–H12)
Format: **CODE**: definition. *Include*: … *Exclude*: … (→ use instead).

### H1 — Problem intensity (fees/pricing pain)
- **PRICE-FEE-PAIN**: participant reports a specific charge (platform, packaging, delivery, small-cart, surge/rain, GST) as unreasonable or as causing an action. *Include:* noticing a fee at checkout, removing items, complaining. *Exclude:* the general food price being high (→ PRICE-MENU-LEVEL); fee mentioned neutrally (→ FEE-AWARE-NEUTRAL).
- **PRICE-MENU-MARKUP**: belief or observation that the in-app menu price is higher than at the restaurant. *Include:* compared prices, saw a difference. *Exclude:* the restaurant is simply expensive (→ PRICE-MENU-LEVEL). Tag `evidence_kind` = opinion if the belief was never checked.
- **PRICE-MENU-LEVEL**: food itself is expensive, independent of the platform.
- **FEE-AWARE-NEUTRAL**: knows the fee lines but reports no pain.
- **BILL-SURPRISE**: final total higher than expected when reaching checkout.
- **PROMO-DEPENDENCY**: orders only or mainly with a coupon/offer; waits for offers. *Exclude:* one-off use of a coupon (→ PROMO-USE).
- **PROMO-FATIGUE**: distrust of or annoyance with offers (e.g. "discount is fake", inflated strike-through prices).
- **PROMO-USE**: used an offer without it being decisive.
- **ABANDON-CART**: started and did not complete an order. Sub-tag the reason in `interpretation` only if the participant did not state it; otherwise put it in the observation.

### H2 — Price value proposition (total checkout)
- **TOTAL-PRICE-DRIVER**: chose an option because of the **final payable** amount (compared totals).
- **PRICE-COMPARE-BEHAVIOUR**: actually compared across apps / with the restaurant (past incident).
- **VALUE-NOT-PRICE**: explicitly chose on something other than price despite a known cheaper option.

### H3 — Price vs ETA
- **ETA-EXPECTATION**: stated or implied acceptable wait (record minutes said).
- **ETA-TRADEOFF-SAVE**: waited longer to pay less (incident).
- **ETA-TRADEOFF-PAY**: paid more for faster delivery (incident).
- **ETA-BROKEN-PROMISE**: actual delivery later than shown.

### H4 — Price vs reliability
- **RELIABILITY-FAIL**: late/cancelled/wrong/missing/spilled order (incident).
- **REFUND-EXPERIENCE**: outcome of a refund or credit (positive or negative; put the valence in the observation).
- **SUPPORT-EXPERIENCE**: interaction with customer support.
- **CHEAP-DISAPPOINT**: a cheaper choice led to a worse outcome.
- **RELIABILITY-PREMIUM**: chose or stayed with a more expensive option for dependability.

### H5 / H10 — Restaurant choice / assortment
- **ASSORT-MISSING**: wanted restaurant not available.
- **ASSORT-FAVOURITE-LOCK**: orders repeatedly from specific restaurants; those determine the app.
- **ASSORT-DISCOVERY**: browses to discover new places.
- **ASSORT-TYPE-NEED**: needs a restaurant type (budget, chains, premium, local/biryani, late-night, healthy). Tag the type in the observation.

### H6 — Segment difference
Not a code. Analysed by cross-tabulating all codes by `seg_occupation`/`seg_freq`. Add **CONTEXT-HOSTEL-GATE** (campus delivery constraints), **CONTEXT-OFFICE-DELIVERY**, **CONTEXT-GROUP-ORDER**, **CONTEXT-BUDGET-CYCLE** (month-end, pocket money, salary day) as seed context codes.

### H7 — Brand effect
- **RAPIDO-TRUST-POS / RAPIDO-TRUST-NEG / RAPIDO-NEUTRAL**: reaction to the Rapido affiliation. The observation must note the **specific Rapido experience** cited (or "none cited").
- **BRAND-EXPECT-RELIABILITY / BRAND-EXPECT-SUPPORT / BRAND-EXPECT-SAFETY**: expectations changed by the brand.
- **CONCEPT-COMPREHENSION**: correct / partial / wrong (brand-blind card).
- **CONCEPT-APPEAL-REASON / CONCEPT-OBJECTION**: reasons for the stated reaction (`evidence_kind` = stated_intent).
- **INTENT-SHIFT-REVEAL**: moved placement after the reveal (direction in the observation).

### H8 — WTP for delivery
- **DELIVERY-FEE-ANCHOR**: ₹ amount mentioned as normal/acceptable/too much for delivery (record the figure and whether recalled or hypothetical).
- **SUBSCRIPTION-VALUE**: Swiggy One / Zomato Gold perceived worth (incident-based if possible).
- **SUBSCRIPTION-LOCKIN**: subscription keeps them on a platform.

### H9 — Bengaluru → Hyderabad transferability
- **CITY-CONTEXT**: a local Hyderabad (or Bengaluru) factor affecting ordering (cuisine, traffic, rain, campus rules, area coverage).
- **TRANSFER-DRIVER**: Bengaluru module, reason for adoption/repeat that could apply elsewhere.
- **TRANSFER-RISK**: a friction that could be worse in the Hyderabad context.

### H11 — Behavioural intent
- **SAID-DID-GAP**: contradiction between a stated preference and a reported behaviour within the same interview (e.g. "price matters most" but pays for a subscription and never compares). Always write both halves in the observation.

### H12 — Repeat use (Ownly users)
- **OWNLY-TRIAL-TRIGGER**, **OWNLY-DISCOVERY-SOURCE**, **OWNLY-REPEAT-DRIVER**, **OWNLY-COMPETITOR-OCCASION** (when they still use others), **OWNLY-ISSUE**, **OWNLY-CHURN-REASON**, **OWNLY-SAVING-PERCEIVED** (record ₹ if said, "recalled").

### Cross-cutting
- **SWITCH-PUSH / SWITCH-PULL / SWITCH-ANXIETY / SWITCH-HABIT**: forces-of-progress elements in a real or near switch.
- **HABIT-DEFAULT-APP**: opens one app without considering others.
- **MULTIHOME**: uses more than one app, with the occasion logic.
- **ALT-NON-DELIVERY**: the alternative chosen was not delivery (cook, mess, eat out, skip).
- **TRUST-FOOD-SAFETY**: hygiene/quality/tampering concerns.
- **APP-UX**: usability issues or delights.
- **META-LED-QUESTION**: interviewer led; discount the answer that follows.
- **META-RECALL-WEAK**: participant unsure or reconstructing.

### Incident types (for `incident_type`)
`bill_unreasonable, abandon, late, cancel, wrong_or_missing_item, spill_quality, refund, support_contact, restaurant_missing, cheaper_disappointed, eta_changed_plan, switch_episode, tradeoff_save, tradeoff_pay, subscription_decision, ownly_trial, ownly_issue, other`

## 4. Severity scale (pains/incidents only)
| Score | Label | Definition (based on **consequence**, not tone) |
|---|---|---|
| 1 | Irritant | Noticed/complained, no behaviour change |
| 2 | Order-level impact | Changed that order (removed items, chose another restaurant, used a coupon, waited) |
| 3 | Order lost / money lost | Abandoned the order, cancelled, ate elsewhere, or lost money not fully refunded |
| 4 | Relationship impact | Reduced or stopped using a platform/restaurant, uninstalled, cancelled a subscription, told others not to use it |

Severity comes from the reported consequence. If the consequence is unknown, leave it blank; **don't infer**.

## 5. Inductive coding rules
1. **Open-code the first 3 transcripts line-by-line** (both coders independently) *before* applying the seed codebook heavily, to reduce forcing.
2. A candidate new code is written in the memo log as `NEW-<NAME>` with a definition and 1 example segment ID.
3. **Promotion rule:** a candidate becomes a codebook code when it appears in ≥2 interviews **or** is judged critical (a severity-4 incident). Then re-check earlier transcripts for it (**constant comparison**).
4. **Merge/split rule:** if two codes co-occur in >80% of their segments, consider merging. If one code's segments show clearly different meanings, split it. Record every change in the codebook change log with date and reason.
5. Codebook freeze: after the double-coding reliability round (§6). Changes after that require re-coding the affected codes across all transcripts.

## 6. Memoing
Memo log (a simple doc/sheet): `memo_id, date, author, type (code_definition / emerging_pattern / contradiction / method_note / reflexive), linked_segments, text`. Required memos:
- One **reflexive memo** per interviewer after each session ("what I expected vs heard; where I might have led").
- One **contradiction memo** whenever evidence cuts against a working hypothesis.

## 7. Two-coder reliability (≥20% of transcripts)
- **Sample:** at least 3 of 14–16 transcripts (≥20%), chosen to include ≥1 student, ≥1 professional and ≥1 Ownly user.
- **Procedure:** both coders code the same pre-segmented transcripts independently with the frozen draft codebook. Compare **presence/absence of each code per segment**.
- **Metrics per code and overall:**
  - Percent agreement = agreed segments / total segments.
  - **Cohen's κ** = (p_o − p_e) / (1 − p_e), computed per code on the segment × present/absent 2×2 table. Report κ only for codes applied ≥5 times (κ is unstable on rare codes).
  - Interpretation guide (Landis & Koch style): <0.40 weak, 0.41–0.60 moderate, 0.61–0.80 substantial, >0.80 almost perfect. **Target κ ≥ 0.60** for the codes that feed hypothesis tests.
- **Reconciliation meeting:** walk through disagreements, refine definitions and include/exclude rules, log the changes, then have one coder code the remaining transcripts (with 1 more double-coded transcript as a spot-check if κ was <0.60).
- Pseudocode (Python, no external libs needed):
```python
def kappa(a, b):  # a, b: lists of 0/1 for one code across the same segments
    n = len(a); po = sum(x == y for x, y in zip(a, b)) / n
    pa1, pb1 = sum(a)/n, sum(b)/n
    pe = pa1*pb1 + (1-pa1)*(1-pb1)
    return (po - pe) / (1 - pe) if pe < 1 else float('nan')
```

## 8. Roll-ups and saturation
**Code frequency table (report both counts, never just segments):**
| code | # segments | # interviews (n of N) | students (n/8) | professionals (n/8) | frequent / regular / occasional | Ownly users | mean severity | max severity | past_incident share |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | |

"# interviews" is the headline number. Segment counts inflate talkative participants.

**Saturation table:** `interview_order, interview_id, new_codes_added, cumulative_codes`. Stop rule is in `recruitment_plan_and_quota.md` §1.

## 9. Synthesis ladder (OBSERVATION → USER QUOTE → INTERPRETATION → INSIGHT → OPPORTUNITY)
Build one ladder per candidate insight. **Each rung must reference segment IDs.**

| Rung | Content | Rule |
|---|---|---|
| OBSERVATION | Factual pattern across incidents: "In 6 of 16 interviews (4 prof., 2 students), participants reported abandoning a cart after seeing the checkout total." | Counts + segment breakdown; past incidents only unless stated |
| USER QUOTE | 1–3 verbatim quotes with `segment_id` + timestamp | Exact transcript text only, ≤25 words each, redacted |
| INTERPRETATION | "INTERPRETATION: the pain is triggered at checkout, not at menu browsing, suggesting…" | Labelled as the analyst's view |
| INSIGHT | A non-obvious, decision-relevant statement about users: "For professionals, reliability failures, not fees, trigger platform-level changes (severity 4); fees trigger order-level changes (severity 2)." | Must pass the evidence rule below |
| OPPORTUNITY | "Lead Gachibowli professional messaging with dependable arrival; test price transparency as a secondary message." | Framed as a hypothesis to test (fake door, survey, pilot) |

**Evidence-strength rule for an INSIGHT:**
- **≥3 interviews across ≥2 segments** (segments = student/professional, or frequency bands) **and** ≥1 past incident (not only opinion/intent) → eligible as a qualitative insight.
- Otherwise it is flagged **"single-source signal"** (or "narrow signal": ≥3 interviews in one segment only) and cannot appear as a headline insight in the deck/dashboard without that label.
- Insights built mainly on `stated_intent` segments are labelled **"stated-intent insight — needs behavioural validation"**.
- Always record **counter-evidence** (interview count + segment IDs).
- An interview-only insight is at most **MEDIUM** confidence in the triangulation matrix. HIGH requires convergence with survey/audit/fake-door/review evidence.

Ladder template:
```
INSIGHT ID: QI-__
Hypothesis link: H__
OBSERVATION: __ of __ interviews (students __/__, professionals __/__); incident types: __ ; segment IDs: __
USER QUOTES: "__" (HYD-__-___, mm:ss) | "__" (HYD-__-___, mm:ss)
INTERPRETATION: __
INSIGHT: __
COUNTER-EVIDENCE: __ interviews (IDs) — __
EVIDENCE STATUS: qualitative insight / narrow signal / single-source signal / stated-intent insight
OPPORTUNITY (to test): __  → test via: survey Q__ / audit / fake door / pilot
```

## 10. JTBD template (evidence-based only)
A job statement is written **only** from coded incidents (`evidence_kind` ∈ past_incident, habitual_behaviour, show_me_observed).

| Field | Content |
|---|---|
| JTBD ID | J-__ |
| Situation (When…) | e.g. "When I finish late at the office and the cafeteria is closed…" (from observations) |
| Motivation (I want to…) | |
| Expected outcome (so I can…) | |
| Current solution(s) used | apps / mess / cook / eat out (counts) |
| What "hired" means here (success criteria seen in incidents) | e.g. arrives before 21:30; total under the budget they mention |
| Evidence: interview IDs + segment IDs | |
| # interviews / segments represented | __ / __ (students __, professionals __) |
| Counter-evidence (interviews where the same situation produced a different job) | |
| Status | supported (≥3 interviews, ≥2 segments) / narrow / single-source |

## 11. Switch-forces template (per switching or near-switching episode, then aggregated)
| Force | Coded content (short) | # episodes | # interviews | Segments | Example segment IDs | Counter-evidence |
|---|---|---|---|---|---|---|
| PUSH (problem with current solution) | | | | | | |
| PULL (attraction of new solution) | | | | | | |
| ANXIETY (fear about new solution) | | | | | | |
| HABIT (attachment to current) | | | | | | |

Rule: a switch happens when push + pull > anxiety + habit **in the observed episodes**. Report which forces appear in **completed** switches vs **near-switches that didn't happen**, as the contrast is the evidence.

## 12. Outputs of qualitative synthesis
1. `coded_segments.csv` (filled template, human-reviewed)
2. Codebook with change log + reliability table (κ per code)
3. Code frequency × segment table + severity table
4. Saturation table
5. Synthesis ladders (QI-01…)
6. JTBD table + switch-forces table
7. Rows for the triangulation / insight evidence matrix (interview-evidence column), each with confidence ≤ MEDIUM unless triangulated
