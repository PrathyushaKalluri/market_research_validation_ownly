# Data Gap Map

**Version:** 1.0 · 2026-09-16 · **Nothing has been collected yet**, so gaps can still be closed without splitting the sample into waves.

## 1. Can current instruments calculate every P0 KPI?

| P0 KPI | Instrument | Calculable once collected? | Gap |
|---|---|---|---|
| K00 North-star proxy | Survey v6 | ✅ | — |
| K01 Trial penetration | Survey v6 | ✅ | — |
| K10 Awareness | Survey v6 | ✅ | — |
| K11 Awareness → trial | Survey v6 | ✅ | — |
| K13 H₀ fake-door conversion | Fake door | ⚠️ Instrument ready, **not deployed** | D3's stopping date has passed with 0 traffic. Without ≥80 visitors (≥30 per arm), K14 becomes primary |
| K14 H₀ forced choice | Survey v6 | ✅ | Stated, not conversion; noted on the banner |
| K20 Basket saving % | Audit | ⚠️ Template ready, **all price fields empty** | P3 must complete the 60 captures |
| K24 ₹30 trade-offs | Survey v6 | ✅ | — |
| K30 Trier repeat rate | Survey v6 | ✅ | — |
| K32 Repeat without promo | Survey v6 (S7-Q5) | ✅ | **v7 dropped S7-Q5.** It must be restored if v7 is fielded |
| K33 Share of requirements | Survey v6 | ✅ | v7 bands make it approximate |
| K40 Restaurant coverage | Restaurant frame | ⚠️ R5–R8 names and all `on_*` flags empty | P3 fills the frame |
| K50 ETA gap | Audit | ⚠️ ETA fields empty | Collected in the same captures |
| **K51 Fulfilment failure** | — | ❌ **No question exists** | Addition **A3** |
| **K71 Promo-dependency gap** | — | ❌ **No first-order offer question** | Addition **A2** |

Also missing, at P1: **K60/K61 Rapido usage**. No Rapido question exists in v5, v6 or v7, and Page 7 cannot run without
it → addition **A1**.

## 2. Gaps accepted, with no collection

| Gap | Why we accept it |
|---|---|
| Real conversion to a first order, real repeat rates | Needs Ownly's internal data. Survey self-reports and fake-door clicks are labelled proxies |
| Revenue/value share of requirements | Would need spend per app: a burdensome question with high recall error |
| CAC, CLV, retention cost, contribution, GMV, EBITDA, burn/order | No spend, cost or revenue data; the fake door has ₹0 spend |
| Menu parity (K26) | Audit-lite dropped offline prices; re-adding them costs a restaurant visit per item |
| Game awareness/participation (K73) | No evidence a game exists. P3 screenshots the app; if one exists, probe it in interviews only |
| App-placement first tap (K63) | Optional 30-second interview add-on; not worth a survey question |
| Actual delivery reliability rate | 3 test orders give anecdotes only; the survey self-report (A3) is the better proxy |
| Hyderabad retention over 4+ weeks (K31) | Ownly has been in Hyderabad about 1 month. Bengaluru is the benchmark; Hyderabad uses the 8-week K30 and stated K32 |

## 3. Minimal additions to survey v6 (add before sharing the link)

Three questions: one for everyone (one tap), two for Ownly users only (about 20–35% of respondents). Added time is under 20
seconds for most people.

### A1 · Rapido usage
- **Enables:** K60, K61, and the Rapido user/non-user segment (Page 7, Page 9).
- **Why current questions can't:** "Inside the Rapido app" as a discovery source (S10–12-Q1) only covers aware people. It
  can't compare users with non-users.
- **Where:** S3 (and S14, S25), **above** "In the last 4 weeks, did you order food online…", which must stay last.
- **Type:** Multiple choice, required, shuffle OFF.

```
In the last 4 weeks, how often did you use Rapido (bike, auto or cab)?
```
```
Never
1–3 times
About once a week
Several times a week
```
- **Worth the burden?** Yes. One tap for everyone, and it unlocks a whole dashboard page and a master-prompt question.

### A2 · Offer on the first Ownly order
- **Enables:** K70, K71 (P0 guardrail G4, Page 8).
- **Why current questions can't:** S7-Q5 is hypothetical. Nothing asks what actually triggered the real first order.
- **Where:** S12 (HYD) and S23 (BLR), directly **below** "When did you place your FIRST Ownly order?".
- **Type:** Multiple choice, required, shuffle OFF.

```
Did your FIRST Ownly order use a discount or offer?
```
```
Yes, a first-order discount
Yes, another offer or coupon
No
Don't remember
```
- **Worth the burden?** Yes. Ownly users only, one tap, and it turns the promotion question from stated into self-reported behaviour.

### A3 · Fulfilment failures
- **Enables:** K51 (P0 guardrail G2), K52 (the test of "reliability earns the second order").
- **Why current questions can't:** v6 has no reliability-experience question. S12-Q7 asks what should change, not what happened.
- **Where:** S12 (HYD) and S23 (BLR), directly **below** "How would you feel if you could no longer use Ownly?".
- **Type:** **Checkboxes**, required, shuffle OFF.

```
Across your Ownly orders so far, has any of these happened?
```
**Question description:** `Tick all that apply.`
```
An order arrived 15+ minutes later than shown
An order was cancelled or never delivered
An item was missing or wrong
A refund or support reply took more than 2 days
None of these
```
- **Worth the burden?** Yes. It is the only way to test the second-order hypothesis with behaviour rather than stated intent.

**Analysis wording to add to Appendix A1 of the v6 guide:**
- `how often did you use Rapido`
- `FIRST Ownly order use a discount`
- `has any of these happened`

## 4. If the team fields v7 instead of v6

v7 (decision D11) is shorter, but it removes inputs to two P0 KPIs. To keep this KPI system working, v7 needs:
1. **A1** in "About you" (above the ordered-recently question).
2. **A2 and A3** in "Ownly users".
3. **Restore S7-Q5** (repeat after the ₹100 offer), right after the forced choice. It is the only input to P0 K32.
4. Accept that K33 and K00 use band midpoints (0 / 1.5 / 4 / 8), and that K15 (P/Q intent, McNemar) is lost.

**Which form is live is a team decision** (see `_ops/decisions.md` D12). This KPI system and dashboard assume **v6 + A1–A3**.

## 5. Audit and fake-door actions (no new fields)
- **Audit:**
  - P3 completes all 60 captures, including `restaurant_listed`, `restaurant_open`, ETAs and every fee field.
  - Fill R5–R8 names and every `on_*` flag in the restaurant frame.
- **Fake door:**
  - Either deploy tonight with `CONFIG.ENDPOINT` set, and log posts in `experiment_tracker.csv`,
  - or formally record that it is directional only and that K14 is primary (D3 already allows this).
- **Game:** P3 takes one dated screenshot of the Ownly/Rapido Hyderabad home screen and any rewards screen.
