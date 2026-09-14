# Choice Experiment (DCE-lite): Price × ETA × Reliability × Assortment × Refund

**Version:** 2026-09-14.
**Hypotheses:** H2.1, H3.1–H3.2, H4.1–H4.2, H5.1–H5.2, H6.3; RSS metric.
**Files:** `dce_design_matrix.csv` (design), `dce_check.py` (validation).
**Status:** all levels are **PROVISIONAL** until the Gachibowli audit (`01_secondary_research/market_price_anchors.md` §5.2).

## 1. Attributes & levels

Every task shows two unbranded options, **App A** and **App B**, for the **same dinner for one (food ≈ ₹210)**. Attributes always appear in this order:

| # | Attribute (respondent wording) | Levels | Variable | Rationale |
|---|---|---|---|---|
| 1 | **Total amount to pay** (food + all charges + taxes) | ₹235 · ₹260 · ₹285 · ₹310 | `price` | ₹235 ≈ food + a low single-fee structure; ₹285–310 ≈ food + the ~₹72 non-food stack seen on one incumbent bill (E29). ₹25 steps make "₹25 ↔ Y minutes" statements readable. Total checkout price only, never "cheapness". |
| 2 | **Delivery time shown** | 25 · 35 · 45 · 55 min | `eta_min` | 25 = lowest plausible standard delivery; 45 = the brief's example; 55 tests the ceiling (H3.2). Four levels so non-linearity can be checked. Quick-commerce ~10-min delivery is excluded as a different product. |
| 3 | **How often it's late** | "15+ min late in **1 of every 10** orders" · "**3 of every 10** orders" | `late_in_10` | A frequency format ("x in 10") is understood better than percentages. There are no public on-time rates, so the levels are an ASSUMPTION. |
| 4 | **Your usual restaurants on the app** | **Most** · **Some** · **Few** | `restaurants` | Relative to the respondent's *own* usual restaurants (H5/H10). Restaurant counts mean little to respondents. |
| 5 | **If something goes wrong** | "**Automatic refund within 24 hours**" · "Refund after you raise a complaint, **case by case**" | `refund` | Refund and support failures are the top-severity review themes (`05_review_mining/app_stores/analysis_tables.md`) → H4.2. |

**No brand, no Ownly fee, no savings %** anywhere in the module. Every task is labelled "Hypothetical apps".

## 2. Design

- **2 blocks × 6 paired tasks + 1 dominance-check task** (`dce_dom`, identical in both blocks, at position 4 of 7).
- Block 1 runs in V1, V3 and B1; block 2 in V2, V4 and B2 (`randomization_and_versions.md`).
- **No opt-out ("neither").** The module estimates *relative* trade-offs between two apps for an order the respondent has already decided to place. An opt-out would mix market-participation with trade-off preference and add a third response mode on a small mobile form. Switching from the respondent's *current* app is measured separately (`beh_switch_savings_required`, bill_s3/s4). Codes: `dce_t1…dce_t6`, `dce_dom` → 1 = App A, 2 = App B.

### 2.1 Construction method

A small hand-built, constraint-based design, not a full or fractional factorial. The goal is **readable trade-offs** at a sample of ≈ 220, not maximum statistical efficiency.

1. **Pure two-attribute tasks** (`price_vs_eta`, `price_vs_reliability`, `price_vs_assortment`, `price_vs_refund`): only price and one attribute differ. The cheaper option is always worse on that attribute, so no pair is dominated. Each can be read directly as a choice share even if the full model is underpowered (fallback in PAP §6.1).
2. **Multi-attribute task** per block: all 5 attributes differ, with each option better on 2–3 attributes. This identifies the attributes jointly and reduces the "spot the one difference" heuristic.
3. **Price gaps varied across tasks** so the choice data bracket the business thresholds in the hypothesis tree:

| Trade-off | Block 1 | Block 2 | Brackets |
|---|---|---|---|
| ETA | ₹50 for 20 min (₹25 per 10 min) | ₹75 for 20 min (₹37.5 per 10 min) | H3.1 threshold ₹30 per 10 min |
| Reliability (3→1 late in 10) | ₹25 and ₹75 | ₹25 and ₹50 | H4.1 threshold ₹30 |
| Assortment | few→most for ₹50 | some→most for ₹25 | H5.1 vs audit saving |
| Refund assurance | ₹25 | ₹50 | H4.2 threshold ₹15 |

4. **Position balance:** the cheaper option is App A in 3 tasks and App B in 3 tasks per block (block 1: A, B, A, B, A, B; block 2: B, A, B, A, B, A).
5. **Constraints:** no dominated pair except `dce_dom`. The implausible "super-profile" (₹235 / 25 min / 1 late in 10 / most / auto-24h) is excluded. At least 2 `price_vs_reliability` tasks per block, because RSS needs ≥ 2.
6. **Task order is fixed within block**, since Google Forms cannot shuffle sections while keeping images attached reliably. Order effects are partly offset by the two blocks having different sequences. Position is recorded, so order can be checked as a covariate.

### 2.2 Validation results (`python3 dce_check.py`, run 2026-09-14)

```
block 1 pos 1 t1   price_vs_eta           varies=price,eta_min            gap=Rs50  dominated=no  [ok]
block 1 pos 2 t2   price_vs_reliability   varies=price,late_in_10         gap=Rs25  dominated=no  [ok]
block 1 pos 3 t3   price_vs_assortment    varies=price,restaurants        gap=Rs50  dominated=no  [ok]
block 1 pos 4 dom  dominance_check        varies=all 5                    gap=Rs25  dominated=A>B [ok]
block 1 pos 5 t4   price_vs_reliability   varies=price,late_in_10         gap=Rs75  dominated=no  [ok]
block 1 pos 6 t5   price_vs_refund        varies=price,refund             gap=Rs25  dominated=no  [ok]
block 1 pos 7 t6   multi                  varies=all 5                    gap=Rs50  dominated=no  [ok]
block 2 pos 1 t1   price_vs_eta           varies=price,eta_min            gap=Rs75  dominated=no  [ok]
block 2 pos 2 t2   price_vs_reliability   varies=price,late_in_10         gap=Rs25  dominated=no  [ok]
block 2 pos 3 t3   price_vs_assortment    varies=price,restaurants        gap=Rs25  dominated=no  [ok]
block 2 pos 4 dom  dominance_check        varies=all 5                    gap=Rs25  dominated=A>B [ok]
block 2 pos 5 t4   price_vs_reliability   varies=price,late_in_10         gap=Rs50  dominated=no  [ok]
block 2 pos 6 t5   price_vs_refund        varies=price,refund             gap=Rs50  dominated=no  [ok]
block 2 pos 7 t6   multi                  varies=all 5                    gap=Rs50  dominated=no  [ok]
Tag counts per block: price_vs_eta 1, price_vs_reliability 2, price_vs_assortment 1, price_vs_refund 1, multi 1, dominance_check 1
Level appearances (both blocks, dominance excluded):
  price {235:7, 260:6, 285:7, 310:4}   eta {25:5, 35:7, 45:8, 55:4}
  late_in_10 {1:18, 3:6}   restaurants {few:4, some:10, most:10}   refund {auto_24h:12, case_by_case:12}
Cheaper option shown as A/B: block 1 3/3, block 2 3/3
All hard checks passed.
```

**Balance interpretation.** The imbalances (`late_in_10` 18:6; `few` 4) come from **attributes held constant** inside pure tasks. In a conditional logit, an attribute that is identical in both options contributes nothing to the likelihood, so these constant appearances neither help nor bias identification. What matters is the number of tasks where each attribute **differs**:

| Attribute | Tasks where it differs (both blocks) |
|---|---|
| Price | 12 |
| ETA | 4 |
| Reliability | 6 |
| Assortment | 4 |
| Refund | 4 |

ETA and assortment are the thinnest. Re-run `dce_check.py` after any level change.

## 3. Respondent-facing screens (Google Forms)

### 3.1 Warm-up / instruction section (one section, no question, then task sections)

> **Choosing between two apps (7 quick questions)**
> Imagine you're ordering **the same dinner for one** tonight, from a restaurant you like. Two *hypothetical* apps can deliver it. They differ in:
> - **Total amount to pay:** food + every charge + taxes, all in one number
> - **Delivery time shown**
> - **How often it's late:** e.g. "3 of every 10 orders arrive 15+ minutes late"
> - **Your usual restaurants on the app:** most / some / few of the places you normally order from
> - **If something goes wrong:** automatic refund in 24 hours, or a refund only after you complain, case by case
>
> There are no right answers. Pick the app you would **actually** order from. If both seem similar, go with your first instinct.
>
> *Example (not a question):* App A costs ₹25 more but arrives 10 minutes sooner. App B is cheaper but slower. Choosing App A means the time mattered more to you than ₹25 here.

### 3.2 Each task

- **Rendering:** one multiple-choice question per task, each task in its own section so it fits the screen.
- **Question title:** "Task [k] of 7 — which app would you order from?"
- **Image:** a two-column table made in Google Slides (same template for all 14 images; no colours implying good/bad; ₹ in bold). Header "Hypothetical apps".
- **Description (text fallback for accessibility)**, e.g. block 1, task 1:
  ```
  App A — ₹235 | 45 min | late in 1 of 10 | some of your usual restaurants | automatic refund within 24h
  App B — ₹285 | 25 min | late in 1 of 10 | some of your usual restaurants | automatic refund within 24h
  ```
- **Options (never shuffled):** "App A" · "App B". Required.
- **Variable:** by position → `dce_t1`, `dce_t2`, `dce_t3`, `dce_dom`, `dce_t4`, `dce_t5`, `dce_t6`.

## 4. Analysis summary (details: `09_analysis/M_pre_analysis_plan.md` §6.1)

- **Long table** `fact_dce_long`: resp_id × task × alt, with the attributes joined from the matrix using `meta_form_version` → block.
- **Coding:** price linear (₹); ETA linear (minutes), with a dummy-coded check for H3.2; `late3` dummy; `restaurants_some`, `restaurants_few` dummies (ref = most); `refund_case` dummy; ASC_A for position.
- **Model 1:** pooled conditional logit, respondent-clustered SEs.
- **Model 2:** Model 1 + segment × attribute interactions (H5.2, H6.3).
- **WTP:** `WTP_k = β_k / (−β_price)` with a Krinsky-Robb 95% CI; ₹ per 10 min = 10 × β_eta / (−β_price).
- **RSS** (per respondent) = % of the 2 `price_vs_reliability` tasks in which the reliable-but-pricier option was chosen (possible values 0 / 50 / 100).
- **Quality flags:**
  - `FLAG_dominance_fail` (chose B in `dce_dom`)
  - `FLAG_choice_left_right` (the same letter in all 7 tasks)
  - Both are kept in the primary analysis and dropped in the sensitivity analysis.
- **Fallback** if n < 125 or β_price is not significant: pure-task choice shares with Wilson CIs, e.g. "in block 1 task 1, X% (CI) chose paying ₹50 more to save 20 minutes".

## 5. Claim discipline

- A statement like "₹X compensates for Y minutes for segment A but not segment B" requires: a significant price coefficient, a WTP CI for **each** segment, and a between-segment difference CI that excludes 0. Otherwise the statement is not made.
- Stated choices between hypothetical apps remove habit, subscriptions and real offers. WTP values are **upper-bound preference signals**, to be read alongside the audit (actual gaps) and interviews (real trade-off episodes).
- The levels are provisional. If the audit changes them, re-run `dce_check.py` and record the change in the pilot edit log **before** fielding. Never after data collection.
