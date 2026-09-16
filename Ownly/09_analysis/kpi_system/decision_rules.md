# Decision Rules: KEEP / ADAPT / DROP

**Version:** 1.0 · **Fixed 2026-09-16, before any data exists.** Changing a rule after data arrives requires a dated
`_ops/decisions.md` entry explaining why.

## 0. Principles behind every threshold
- **Practical floors come from the research charter** (`00_research_charter/C_hypothesis_tree.md`): **10pp** for proportions
  and **₹10** for money. A difference smaller than these would not change a GTM plan even if statistically significant.
- **Uncertainty decides the verdict:**
  - "Supported" needs the whole 95% CI on the hypothesised side of the threshold.
  - "Contradicted" needs it wholly on the other side.
  - Otherwise the result is **inconclusive**.
  - n < 30 is **not testable**.
  - This is the existing project verdict rule, reused.
- **Majority rules (50%)** are used only where the decision is about the *lead* message for the segment. A lead message has
  to serve more than half of the people it addresses.
- **₹30** is the design constant from the survey trade-offs (S6) and roughly one incumbent delivery + platform fee, so it is
  the natural yardstick for "a saving people notice".
- **Confidence:**
  - **HIGH** = ≥2 evidence types agree, including one observed (audit or fake door).
  - **MEDIUM** = one quantitative source with n ≥ 30, plus qualitative support.
  - **LOW** = stated only, n < 30, or reviews only.
  - Price claims cannot be HIGH without the audit.

## 1. H₀: Bengaluru-style vs Hyderabad-localized proposition

**Which test is primary (D3):** the fake door (K13) if ≥ 80 eligible visitors and ≥ 30 per arm. Otherwise the survey
forced choice (K14). Both are always shown.

| Result | H₀ call | Proposition decision |
|---|---|---|
| Primary test p < 0.05 **and** \|difference\| ≥ 10pp (K13), or CI wholly outside 40–60% (K14) | **Reject H₀** | The winner leads Hyderabad messaging |
| p < 0.05 but difference < 10pp | Reject H₀ statistically, **no practical difference** | Don't lead with either; combine P and Q proof points |
| p ≥ 0.05 | **Fail to reject H₀** | *"No evidence the two differ"*. This is **not** "the two are equal". Treat the Bengaluru proposition as transferable *as is*, pending retention checks |
| "Can't choose" > 35% (K14) | Report as a finding | The framings don't read as different; framing is not the lever |

**What a rejection does NOT mean:**
- It doesn't prove actual first orders will differ, because the survey measures stated choice and the fake door measures clicks.
- It doesn't say anything about retention.
- It doesn't generalise beyond 20–30-year-olds in our sample.

## 2. Transferability Matrix (six playbook elements)

Each row gets **KEEP** (replicate as in Bengaluru), **ADAPT** (keep with localisation or operational change) or
**DROP/DEPRIORITIZE** (don't lead Hyderabad GTM with it).

### 2.1 Transparent lower price
| Condition | Verdict | Reason |
|---|---|---|
| K20 median saving CI lower bound > 0 **and** median saving ≥ ₹30, **and** K23 ≥ 50%, **and** K24 speed share ≥ 50% | **KEEP** as core positioning | The advantage is real, noticeable, above most people's switching threshold, and worth more than 15 minutes |
| Saving CI > 0 but median < ₹30, **or** K23 < 50% | **ADAPT**: supporting proof, not the headline | Real but too small to switch most people |
| Saving CI includes 0, **or** K21 win rate < 50% | **DROP** as a lead claim | An affordability claim that fails half the time damages trust (reviews already show FUTURE_FEE_CREEP / SUSTAINABILITY scepticism) |
| Audit incomplete | **INSUFFICIENT EVIDENCE** | Price claims need observed data |

### 2.2 No / low fees
| Condition | Verdict |
|---|---|
| Incumbent fee load (K22) − Ownly fee load ≥ 5pp of the bill **and** K25 fee pain ≥ 30% | **KEEP** |
| Fee gap ≥ 5pp but K25 < 30% | **ADAPT**: fold into the "final bill" message; fees aren't a felt pain |
| Fee gap < 5pp | **DROP** the fee message |

*Why 5pp and 30%:* 5pp of a ~₹350 bill is about ₹18, close to one incumbent platform fee (₹14.90–₹17.58), the smallest
fee a customer can see. 30% is the level at which a pain is shared by roughly one in three orderers, enough to anchor a
message but not a majority.

### 2.3 Rapido cross-sell
| Condition | Verdict |
|---|---|
| K61 awareness gap (Rapido users − non-users) CI lower bound ≥ 10pp **and** K62 Rapido discovery is a top-2 source **and** K60 ≥ 40% | **KEEP**. Label it association, not causation |
| K61 gap positive but CI includes 10pp, or K60 < 40% | **ADAPT**: use Rapido as one channel, not the engine |
| K61 gap ≤ 0 | **DEPRIORITIZE** |

*Why 40%:* if fewer than 4 in 10 target users ride Rapido, cross-sell cannot reach the majority of the segment on its own.
**Caveat on the page:** public sources confirm in-app integration in Bengaluru only.

### 2.4 Game / first-order reward
| Condition | Verdict |
|---|---|
| K71 promo-dependency gap < 10pp **and** K32 ≥ ½ × K15 top-2 trial intent | **KEEP**: offers acquire users who stay |
| K71 ≥ 10pp **and** K70 ≥ 50% | **MODIFY**: keep a smaller first-order offer, add a second-order incentive or reliability guarantee |
| Gap concentrated in one segment (≥ 10pp difference between students and professionals) | **TARGET TO SEGMENT** |
| K32 < ½ × K15 **and** K71 ≥ 10pp | **DEPRIORITIZE** heavy discounting |
| A ₹50/₹100 *game* not verified by screenshot | Game-specific verdict = **NOT TESTABLE** |

*Why ½:* if less than half of the people who'd try would stay once the subsidy ends, most acquired demand is rented.

### 2.5 Local restaurant supply
| Condition | Verdict |
|---|---|
| K40 coverage ≥ 60% **and** K41 local − chain gap ≥ −10pp **and** K24 restaurant-choice share < 50% | **KEEP** supply approach |
| K40 ≥ 60% but local coverage trails chains by > 10pp | **ADAPT**: onboard local favourites before the Service Q message |
| K40 < 60% **or** K43 ≥ 30% | **Fix supply before acquisition spend** (ADAPT, blocking) |

*Why 60%:* the charter's H10.4 threshold. Below it, users meet a missing favourite on almost every other search.

### 2.6 Delivery reliability proposition
| Condition | Verdict |
|---|---|
| K51 failure incidence < 20% **and** K50 ETA gap ≤ +5 min | **KEEP** current operations; reliability is not a differentiator to lead with |
| K24 reliability share < 50% (people pay for reliability) **and** K52 gap ≥ 10pp | **ADAPT: lead with reliability** (Service Q) and fix operations first |
| K51 ≥ 40% | **Operations blocker**: no acquisition scale-up until fixed |

*Why 20% / 40% / +5 min:*
- 20% ≈ one in five triers, the point at which word-of-mouth risk becomes visible in reviews.
- 40% means failures are the norm for a large minority.
- +5 min is the charter's ETA transfer margin.

## 3. Overall Hyderabad call
1. **Any guardrail breach blocks KEEP overall:** K20 saving CI includes 0; K51 ≥ 40%; K40 < 60%; K71 ≥ 20pp.
2. **REPLICATE** the playbook if ≥ 4 of 6 rows are KEEP, no row is a blocker, and K00 (Hyderabad) CI overlaps K00 (Bengaluru).
3. **ADAPT** if the proposition transfers (H₀ not rejected, or P wins) but ≥ 1 row is ADAPT/blocking. Name the rows.
4. **LOCALIZE** if Q wins H₀ **and** the supply/reliability rows are ADAPT. The Hyderabad-localized proposition leads.
5. **INSUFFICIENT EVIDENCE** if the audit is incomplete **or** the survey has < 30 Hyderabad respondents. The dashboard
   says this rather than guessing.

The call is labelled **PROVISIONAL** when ≥ 2 rows are LOW confidence.

## 4. "Price gets the first order; reliability earns the second"
Supported only if **all three** hold:
- K24 speed share ≥ 50% **and** K17 "cheaper" is the top trigger (price wins first-order choices)
- K24 reliability share < 50% (people won't trade reliability for ₹30)
- K52 repeat gap (no failure − failure) ≥ 10pp

Otherwise report which parts hold. Never state the hypothesis as fact.
