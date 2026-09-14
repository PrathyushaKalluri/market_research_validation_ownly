# E. Research Design: Bengaluru (reference) vs Hyderabad/Gachibowli (target)

**Version:** 2026-09-14.

## 1. Design logic: a market-transfer test, not a city popularity contest

```
BENGALURU (reference market)                  HYDERABAD / GACHIBOWLI (target market)
───────────────────────────                   ──────────────────────────────────────
What Ownly users say drove trial/repeat  ──►  Is the same NEED present? (H1, H10, H9.1-9.2)
What frictions caused churn              ──►  Would the same FRICTION hurt more? (H9.3)
Incumbent lock-in among non-users        ──►  Is lock-in stronger? (H9.4)
Company-claimed proposition              ──►  Does it exist at checkout here? (audit, H2.3)
                                              What will users TRADE for it? (H3-H5, H8)
                                              Does the BRAND help here? (H7)
                                              Does intent show up in BEHAVIOUR? (H11)
                         ▼
        TRANSFER MATRIX: Bengaluru assumption → Hyderabad evidence →
        TRANSFERABLE / NEEDS ADAPTATION / NON-TRANSFERABLE / UNKNOWN
```

## 2. Instrument architecture

| Module | Bengaluru survey | Hyderabad survey | Comparable? |
|---|---|---|---|
| Consent, screener (age 20–30, locality, ordered in last 4 weeks) | ✔ (Bengaluru localities) | ✔ (Gachibowli-area localities) | Structure identical; locality lists differ |
| Segment & demographics (`seg_occupation`, `dem_living`) | ✔ | ✔ | **Yes** |
| Recent behaviour (last order, frequency, platforms, subscriptions) | ✔ | ✔ | **Yes** |
| Unaided awareness (before any Ownly mention) | ✔ | ✔ | **Yes** |
| Pain frequencies (PPI items), decision criteria | ✔ | ✔ | **Yes** |
| Expectations (ETA, reliability, ADI) | ✔ | ✔ | **Yes** |
| Choice tasks | ✘ (cut for length, 2026-09-14) | ✔ | **No.** Trade-off analyses (H3–H5) are Hyderabad-only. H9 comparisons rely on identical expectation, pain and fee-ladder items instead. |
| Fee ladder | ✔ (non-users; Ownly users on the same ladder) | ✔ | **Yes** |
| Brand-blind concept → reveal | Unaware only (short) | Full, with randomised arms | Partial — Hyderabad only for H7 |
| Ownly user module (acquisition, reasons, savings, reliability, support, repeat/churn) | ✔ **main branch** | ✔ early-user branch | **Yes**, on shared `own_` items; tenure differs (see §4) |
| Aware-never-tried barriers | ✔ | ✔ | **Yes** |

## 3. Comparison protocol (pre-registered)

1. **Only identical items are compared.** Same wording, options and position relative to the concept exposure. Items after concept exposure are compared only within the same exposure condition.
2. **Composition check first.** Tabulate both samples on `seg_occupation × seg_freq × dem_living × age band`. Report the standardised mean difference per variable; SMD > 0.2 flags imbalance.
3. **Reweight Bengaluru to Hyderabad composition.** Use post-stratification (cell weights on `seg_occupation × seg_freq`, 3 × 3 cells collapsed to 2 × 2 if any cell n < 10). Report both weighted and unweighted results. If they disagree in direction, the finding is **not robust**.
4. **Within-cell comparisons** for key metrics, for example students-frequent in Bengaluru vs students-frequent in Hyderabad.
5. **Non-inferiority framing for transfer.** A driver "transfers" if the Hyderabad metric is not worse than Bengaluru by more than the pre-set margin *(A)*: −10 index points or −10 pp (see H9.2).
6. **Never compare** Bengaluru Ownly users with the Hyderabad general population. Compare Ownly users with Ownly users, and non-users with non-users.
7. **Don't compare cities on metrics driven by recruitment channel.** For example, if Bengaluru Ownly users were recruited from Reddit threads about Ownly, their awareness is inflated by design.

## 4. Known confounds and how we handle them

| Confound | Why it matters | Mitigation |
|---|---|---|
| **Tenure / market maturity** | Bengaluru users have months of experience; Hyderabad users are in launch weeks, with offers and novelty | Record `own_first_order_month`. Compare Hyderabad users against Bengaluru users with ≤ 3 months tenure where n allows. Otherwise label the comparison "maturity-confounded". |
| **Recruitment channel** | Ownly-specific channels in Bengaluru inflate Ownly users' positivity | Record `meta_source`; sensitivity analysis excluding Ownly-topic channels |
| **Survivorship** | Easy-to-reach Ownly users are retained | Lapsed-user quota (≥ 15); analyse separately |
| **Price level differences** | Identical ₹ levels may mean different things in each city | Use the same absolute levels for comparability; interpret with the audit and anchors |
| **Brand exposure** | Ownly marketing in Hyderabad contaminates blind tests | Unaided awareness first; primary H7 analysis on the unaware subgroup |
| **Micro-market vs city** | Gachibowli ≠ Hyderabad; Bengaluru respondents come from many areas | Conclusions scoped to "Gachibowli-area 20–30s"; Bengaluru locality recorded, with a pilot-area flag |

## 5. The transfer matrix (final slide / dashboard View 2)

Template: `11_insights/transfer_matrix_template.csv`.

**Pre-registered verdict rules:**

| Verdict | Rule |
|---|---|
| **TRANSFERABLE** | The Hyderabad need/condition meets the H-threshold **and** is non-inferior to matched Bengaluru **and** no severe friction is identified |
| **NEEDS ADAPTATION** | The need exists (threshold met) **but** at least one enabling condition is materially worse in Hyderabad (ETA expectation, coverage, lock-in, trust) **or** the lead benefit differs |
| **NON-TRANSFERABLE** | The need or behaviour is absent (threshold rejected) **or** materially inferior to Bengaluru |
| **UNKNOWN** | Not testable with the n / evidence collected — never silently dropped |

**Starter rows.** These are Bengaluru assumptions to test, not findings:
- BA1: Total-price savings trigger trial
- BA2: No hidden fees / menu parity is noticed and valued
- BA3: A flat fee at Ownly's level is acceptable
- BA4: ETA gap is tolerated
- BA5: Reliability is good enough to repeat
- BA6: Restaurant coverage is sufficient
- BA7: Rapido distribution and brand drive awareness and trust
- BA8: Users multi-home, so switching is low-friction
- BA9: Support and refunds don't cause churn
- BA10: Trial converts to repeat after offers
