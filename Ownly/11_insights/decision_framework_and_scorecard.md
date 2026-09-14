# Final Decision Framework, Market-Fit Scorecard & Triangulation Rules

**Version:** 2026-09-14. Pre-registered **before** data collection.

Anchors and weights marked *(A)* are editable assumptions. Any change after data is seen is logged in `decisions.md` together with the result of the sensitivity analysis.

---

## 1. Five decision dimensions

Each dimension is scored 0–100 from **named metrics** using **linear anchors**:
- score = 0 at the "weak" anchor
- score = 100 at the "strong" anchor
- values in between are clipped to the 0–100 range

Every score carries an **evidence-strength badge** (HIGH / MEDIUM / LOW, §5) and the n of each input. Scores are computed for **pooled Hyderabad**, **students** and **working professionals** separately.

| # | Dimension | Question | Metric inputs (weight within dimension) | Weak anchor → Strong anchor *(A)* | Source |
|---|---|---|---|---|---|
| D1 | **Need intensity** | Is the problem painful and frequent enough? | a) PPI median (40%) | 25 → 65 | HYD survey |
| | | | b) % abandoned a cart after seeing the final amount in last 4 weeks (30%) | 10% → 50% | HYD survey |
| | | | c) % reporting fee reconsideration "sometimes+" (30%) | 20% → 70% | HYD survey |
| D2 | **Switching potential** | Will people actually move? | a) SRI median (35%) | 30 → 70 | HYD survey |
| | | | b) % whose required savings ≤ audit median Ownly saving (35%) | 10% → 60% | Survey × audit |
| | | | c) Multi-homing rate (15%) | 30% → 80% | HYD survey |
| | | | d) % *without* an active incumbent subscription (15%) | 40% → 90% | HYD survey |
| D3 | **Economic / price attractiveness** | Does the price advantage exist at checkout and clear the bar? | a) Ownly audit win rate in matched pairs (40%) | 30% → 80% | Audit |
| | | | b) Audit median saving as a % of median basket (30%) | 0% → 15% | Audit |
| | | | c) Fee-ladder acceptance at Ownly's actual fee (30%) | 30% → 75% | HYD survey |
| D4 | **Experience / operational acceptability** | Is the experience good enough that low price matters? | a) ETA acceptability: 100 × min(1, median stated tolerance margin / audit median ETA gap), where tolerance margin = median(`exp_eta_max_dinner`) − incumbent median shown ETA; if the Ownly gap ≤ 0 → 100 (30%) | as formula | Survey × audit |
| | | | b) Coverage adequacy: audit Ownly coverage of frame (%) relative to the share of users with ADI < 75 (30%) — score = 100 × min(1, coverage / (1 − share ADI≥75 × 0.5)) *(A)* | as formula | Audit × survey |
| | | | c) Hyderabad + Bengaluru Ownly users reporting "on time most of the time" (25%) | 50% → 85% | Surveys |
| | | | d) Reviews: 100 − severity-weighted share of reliability/support/refund themes among all coded reviews (15%) — lowest weight because reviews are not representative | 50% share → 0, 10% share → 100 | Reviews/social |
| D5 | **Behavioural validation** | Does interest show up in action? | a) Aware→tried conversion among Hyderabad respondents aware ≥ 2 weeks (40%) | 10% → 50% | HYD survey |
| | | | b) Repeat rate among Hyderabad + Bengaluru Ownly users (`own_repeat`) (35%) | 20% → 60% | Surveys |
| | | | c) Fake-door best-variant higher-intent conversion ÷ survey top-2 intent (intent-to-action ratio) (25%) | 0.05 → 0.30 | Fake door × survey |

**Rules for missing inputs:**
- If an input metric is **NOT TESTABLE** (n below minimum), the dimension is computed from the remaining inputs with re-normalised weights.
- The evidence badge drops one level for each missing input.
- If more than half of a dimension's weight is missing, the dimension is shown as "INSUFFICIENT EVIDENCE" and no score is given.

## 2. Weights (recommended defaults; editable in the dashboard)

| Dimension | Default weight | Why |
|---|---|---|
| D1 Need intensity | **20%** | Necessary but not sufficient. Pain without switching or economics doesn't create fit. |
| D2 Switching potential | **20%** | Incumbent habits and subscriptions are the main barrier in a two-player market. |
| D3 Economic / price attractiveness | **20%** | The core of Ownly's proposition, and the most *verifiable* dimension (audit). |
| D4 Experience / operational acceptability | **25%** | The **guardrail**. The brief's own logic ("fair prices are useful only when dinner arrives") and the H4/H5 trade-offs imply that a price advantage is worthless below an experience floor. Weighted highest because failures here also destroy repeat use (H12). |
| D5 Behavioural validation | **15%** | Conceptually the strongest evidence type, but *our* behavioural instruments are the lowest-powered and noisiest (small fake-door traffic; a small Ownly-user base in Hyderabad). So it gets a lower weight *and* acts as a confidence gate (§3). |

**Alternative weight sets for the sensitivity check** (always report whether the recommendation changes):
- **Equal:** 20/20/20/20/20
- **Behaviour-first:** 15/15/20/20/30
- **Price-thesis:** 20/20/30/20/10

## 3. Pre-registered decision rule

Compute, in order:

1. **Gate — RETHINK:** D1 < 40 **or** D2 < 40 (pooled **and** in both segments) → **RETHINK PROPOSITION**.
2. **SCALE:** weighted total ≥ 70 **and** no dimension < 50 **and** D5 evidence badge ≥ MEDIUM → **SCALE** in Gachibowli for the pooled target.
3. **TARGET SELECTIVELY:** pooled fails SCALE, **but** one pre-defined segment (students, professionals, frequent users) meets the SCALE conditions with segment n ≥ 60 → **TARGET SELECTIVELY** (name the segment).
4. **ADAPT:** D1 ≥ 50 **and** D2 ≥ 50, **but** D3 < 50 **or** D4 < 50 → **ADAPT** (name the dimension to fix: price architecture vs experience/supply).
5. **Otherwise → ADAPT**, with the weakest dimension named.

**Non-compensatory principle:** any dimension < 40 blocks SCALE regardless of the weighted total.

**Confidence overlay:** if ≥ 2 dimensions carry a LOW evidence badge, the recommendation is labelled "**PROVISIONAL — evidence insufficient**", and the next experiment becomes the primary recommendation.

## 4. Final conclusion template (filled in only after analysis)

| Element | Answer | Evidence IDs | Confidence |
|---|---|---|---|
| Recommendation (SCALE / ADAPT / TARGET SELECTIVELY / RETHINK) | | | |
| Strongest opportunity | | | |
| Strongest risk | | | |
| Best initial segment | | | |
| Primary switching trigger | | | |
| Non-negotiable guardrail (e.g. ETA ceiling, reliability floor, coverage floor) | | | |
| Expected pricing/value condition (e.g. "saving ≥ ₹X vs discounted incumbent total at fee ≤ ₹Y") | | | |
| What Ownly should NOT compete on | | | |
| Evidence still missing | | | |
| Next experiment | | | |
| Weight sensitivity: does the recommendation change under alternative weights? | | | |

## 5. Triangulation & insight-confidence rules

| Confidence | Rule |
|---|---|
| **HIGH** | Supported by ≥ 2 independent evidence *types*, including ≥ 1 quantitative source (survey test meeting its threshold, audit, or fake door meeting its MDE); ≥ 3 interviews across ≥ 2 segments *or* consistent review/social signal; no unexplained strong contradiction |
| **MEDIUM** | One quantitative source meeting its threshold **plus** qualitative support; **or** ≥ 2 qualitative types + a directional quantitative signal; contradictions present but explained |
| **LOW** | Single source type; **or** directional/underpowered only; **or** unexplained contradicting evidence. Presented as a "signal", never as a market truth |

**Special rules:**
- A single interview can never support more than LOW.
- Reviews and social data alone can never support more than LOW for *prevalence* claims. They can support MEDIUM for *existence and severity of an issue* when combined with interviews.
- Any price-advantage insight requires audit evidence to reach HIGH.

Templates:
- `11_insights/insight_evidence_matrix_template.csv`
- `11_insights/transfer_matrix_template.csv`
