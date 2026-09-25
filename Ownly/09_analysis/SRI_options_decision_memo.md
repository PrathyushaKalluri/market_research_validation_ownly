# SRI — three options for a human decision

**Raised:** 2026-09-18, while pre-registering P1–P5 (PAP §6.7, decision D16).
**Decide before:** freezing the PAP. **Blocks:** D2 of `11_insights/decision_framework_and_scorecard.md`.
**Still pre-data** — response tracker is header-only, so whichever option is picked is an *amendment*,
not a *deviation*.

---

## 1. The problem is bigger than first reported

My first note said *one* SRI component was missing. That was wrong. **Two of the three are missing.**

SRI as defined in PAP §4:

```
SRI = mean( r(bt_trial_intent), r(multihome5), r(6 − dec_habit_lock) )
      where r(x) = (x−1)/4 × 100 ,  multihome5 = 5 if beh_platforms_used_4wk ≥ 2 else 1
```

| Component | In live v3 form? | Note |
|---|---|---|
| `bt_trial_intent` | ❌ **Absent** | No `bt_` variable exists anywhere in v3 |
| `dec_habit_lock` | ❌ **Absent** | No `dec_` variable exists anywhere in v3. Habit is only an *answer option* in `oth_choice_driver`, which is the **other-city module** — not asked of Hyderabad respondents |
| `multihome5` ← `beh_platforms_used_4wk` | ✅ Present | Binary by construction (≥2 platforms → 5, else 1) |

**So SRI currently reduces to a single binary item.** That is not an index, and PAP §4's own rule —
*"an index is used as a composite only if Cronbach's α ≥ 0.60… otherwise report the components
separately and drop the composite"* — already points at dropping it.

**Correction to PAP §11:** it currently says an option is to *"redefine SRI on the two remaining
components."* There is only **one** remaining component. That sentence is wrong and is superseded by
this memo.

## 2. The constraint that rules out most fixes: double-counting inside D2

D2 (Switching potential) has four inputs, and three of them already consume the obvious variables:

| D2 input | Weight | Variable it uses |
|---|---:|---|
| **(a) SRI median** | **35%** | ← the broken one |
| (b) % whose required savings ≤ audit median saving | 35% | `beh_switch_savings_required` |
| (c) Multi-homing rate | 15% | `beh_platforms_used_4wk` |
| (d) % without an incumbent subscription | 15% | `beh_subscriptions` |

**Any rebuilt SRI that uses `beh_switch_savings_required`, `beh_platforms_used_4wk` or
`beh_subscriptions` double-counts a variable D2 already scores separately.** Rebuilding SRI on
multi-homing alone would put **35% + 15% = 50% of D2 on one binary item.**

Checking the full v3 variable list, the **only** switching-relevant items not already used by (b), (c)
or (d) are **`prop_P_intent`** and **`prop_Q_intent`** (Q20/Q21 — *"how likely are you to try it for one
of your next few orders?"*, 5-point Definitely-not → Definitely). These are the same construct and the
same scale as the missing `bt_trial_intent`.

That single fact drives all three options below.

---

## 3. The three options

### Option 1 — DROP SRI (the already-pre-registered default)

Drop the composite. D2 computes from (b), (c), (d) with re-normalised weights:

| D2 input | Was | Becomes |
|---|---:|---:|
| (b) required savings ≤ audit saving | 35% | **53.8%** |
| (c) Multi-homing rate | 15% | **23.1%** |
| (d) No incumbent subscription | 15% | **23.1%** |

- **Requires no new decision.** The decision framework §1 already says: *"If an input metric is NOT
  TESTABLE, the dimension is computed from the remaining inputs with re-normalised weights. The
  evidence badge drops one level for each missing input."* This option is simply that rule firing.
- **Researcher degrees of freedom: zero.** Nothing is constructed after seeing the instrument.
- **Cost:** D2 badge drops one level (max MEDIUM). Switching potential then rests mostly on a single
  ₹-threshold question (53.8%), which is narrow — it measures *price-triggered* switching only, and
  says nothing about willingness to move for non-price reasons.
- **Defensibility: highest.** If challenged in a viva, the answer is "the pre-registered missing-input
  rule applied itself."

### Option 2 — SUBSTITUTE a single-item measure, renamed *(recommended)*

Replace SRI with an honestly-named single-item measure and keep D2's designed weights:

```
PTI  (Proposition Trial Intent)  =  r( max(prop_P_intent, prop_Q_intent) )
     r(x) = (x−1)/4 × 100 ,  x on the 5-point Definitely-not → Definitely scale
     Missing rule: both items required (both are mandatory questions)
```

- **`max(P, Q)`** = readiness to try *whichever* new proposition suits the respondent better. That is
  nearer the original "switching readiness" construct than either arm alone, and it avoids baking the
  P-vs-Q contrast (the primary H₀ test) into the scorecard as a level effect.
- **Non-redundant** — uses the only D2-relevant variables not already consumed by (b), (c) or (d).
- **Renamed on purpose.** Calling it SRI would imply the 14 Sep 3-item index survived. It didn't.
  Report it as a **single item, not an index**: no Cronbach's α, no composite claim.
- **D2 weights stay 35/35/15/15**, so the dimension keeps its designed shape.
- **Costs, stated plainly:**
  1. It is **concept-anchored**, measured right after Section 7 exposure — not a standing disposition.
  2. **Service Q's copy is flagged v0** and must be re-checked against the pilot interviews. **If Q's
     wording changes, PTI changes.** So PTI must be frozen *after* Q's copy is final, or it isn't
     really pre-registered.
  3. It creates a dependency between D2 and the Section 7 block that also produces the primary H₀
     test. Not fatal — `max()` is symmetric and ignores which concept won — but it must be disclosed.
- **Badge:** still drops one level (a 3-item index became a 1-item measure). Be honest about that.

### Option 3 — REBUILD a 2-item composite

```
SRI-v3 = mean( r(max(prop_P_intent, prop_Q_intent)), r(multihome5) )
```

- Structurally closest to the original 3-item design, and keeps D2 at 35/35/15/15.
- **Known defect: it double-counts multi-homing.** Multi-homing would carry
  (35% × ½) + 15% ≈ **32.5% of D2**, on a **binary** item. A 2-item composite mixing a 5-point scale
  with a binary is also weak psychometrically — no meaningful α (report Spearman ρ instead).
- **Only choose this if** you specifically want multi-homing weighted heavily in switching potential,
  and are willing to say so out loud on the slide.

---

## 4. Comparison

| | **Option 1 — Drop** | **Option 2 — PTI (rec.)** | **Option 3 — Rebuild** |
|---|---|---|---|
| New construction after seeing the form | None | One item, renamed | One composite |
| Double-counting | None | None | **Yes — multi-homing ≈32.5% of D2** |
| D2 weights | Re-normalised 53.8/23.1/23.1 | Unchanged 35/35/15/15 | Unchanged |
| Information retained | Least | Most | Middle |
| Depends on Service Q copy being frozen | No | **Yes** | **Yes** |
| Defensibility under challenge | **Highest** | High, if disclosed | Lowest |
| Evidence badge for D2 | Drops one | Drops one | Drops one |

**Recommendation: Option 2**, because Option 1 discards the only usable switching signal the
instrument actually collected, and Option 3 has a real double-counting defect. **Option 1 is the right
choice if you want maximum methodological safety** and are content for D2 to rest largely on the
₹-threshold question.

**If you pick Option 2, one sequencing rule is mandatory:** finalise Service Q's copy against the pilot
interviews **first**, then freeze the PAP. PTI is defined on Q20/Q21, so freezing before Q's wording is
settled would make the pre-registration hollow.

---

## 5. What happens after you pick

1. Amend PAP §4 (metric table) and §11 (amendment **A2**), and correct the wrong
   *"two remaining components"* sentence in §11.
2. Amend `11_insights/decision_framework_and_scorecard.md` D2 — either the re-normalised weights
   (Option 1) or the renamed input (Options 2/3) — and note the badge drop.
3. Update `08_clean_data/master_data_dictionary.csv` and `09_analysis/04_derive_metrics.py`'s spec.
4. Log the choice in `_ops/decisions.md` as **D17**.
5. **Then** freeze: `09_analysis/PAP_frozen_YYYYMMDD.md`.

**None of this is done yet — all three options are still open.**
