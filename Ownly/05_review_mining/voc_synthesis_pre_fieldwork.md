# Voice of Customer: Pre-Fieldwork Synthesis (App Stores + Reddit/LinkedIn/X)

**Written by:** lead, 2026-09-14.

**Sources:**
- `05_review_mining/app_stores/` — 37 reviews
- `05_review_mining/social/` — 524 items; 108 de-duplicated first-hand incidents; 45 LinkedIn items

> **Status: CONSUMER-GENERATED signals, not findings.**
> - Everything here is self-selected, negatively skewed, Bengaluru-only, and AI first-pass coded (human validation pending).
> - It is used to **shape hypotheses and instruments**, not to estimate prevalence.
> - Counts are counts *within these corpora*.
> - No Hyderabad consumer voice exists yet.

## 1. Convergent signals (both corpora point the same way)

| # | Signal | App stores (n=37) | Social (108 first-hand) | Label | Instrument response |
|---|---|---|---|---|---|
| V1 | **Post-order failure is the loudest harm.** Support, refunds, non-delivery and rider problems cause more high-severity complaints than price. | Support unresponsive 21 (mean sev 3.2); refund delay/denial 16; cancellation 11; late 10 | Fulfilment failure 46 (38 at sev ≥ 3); support/refund failure 29 (27 at sev ≥ 3) | CONSUMER-GENERATED; convergent | Reliability + refund assurance are choice-experiment attributes; D4 Experience weighted highest (25%); H4, H12.1, H12.2 are ★ |
| V2 | **Price is praised before ordering; harm occurs after dispatch.** | Positive reviews praise price and no fees; failures follow payment | Order stage: pricing/checkout 32 incidents vs post-dispatch stages ~48 | INTERPRETATION | Supports the "price attracts, reliability retains" hypothesis (H12.1) — to be tested, not assumed |
| V3 | **Early good experience then decline** | 3 reviews | First-order failure → account deletion (several) | CONSUMER-GENERATED | H12: first-order outcome matters; interview probe added |

## 2. Contested signals (keep both sides visible)

| # | Topic | One side | Other side | Implication |
|---|---|---|---|---|
| C1 | Is Ownly actually cheaper? | 6 user bill comparisons all show Ownly cheaper (some ₹100–170) | Incumbent coupons/card offers equal or beat it (7); area parity (4); pricier listings (3); menu above in-store (7) | **Saving appears restaurant-dependent and offer-dependent.** The audit must record totals with and without coupons, card offers and subscriptions (H2.3; AS3/AS4/AS14). |
| C2 | Is the saving worth reliability risk? | "Accept wait/hassle for savings" (4) | "Reliability over price / would pay ₹20–30 more" (6) | Real heterogeneity; choice-experiment segment interactions (H4.1, H6.3) |
| C3 | Delivery fee | Free / ₹0 / "+₹5" / ₹15 | ₹30 flat (media/company); ~₹40 fees (ambiguous) | Fee is taken from the **audit**, not sources (H8.1 edit) |
| C4 | Rapido brand | "does ok without excessive charges" | "Rapido DNA… don't expect help"; ride complaints on launch posts | H7 tests are **two-sided** (already specified) |
| C5 | Incumbent recovery | Swiggy/Zomato recover failed orders better (3) | Incumbent support also "horrendous"; one Swiggy churner | Don't assume incumbents are reliable; measure incumbent pain (PPI + reliability items) |

## 3. New signals not in the v2 design, and what was changed

| # | Signal | Evidence | Change made (2026-09-14) |
|---|---|---|---|
| N1 | **Price-durability scepticism.** Users expect fees and prices to rise once Ownly gains share ("enjoy while it lasts"); Toing reportedly added fees after launching fee-free. | 37 social items + 28 on sustainability | Added **AS24** to the assumption map. Interview probe added (`04_interviews/interview_guide_45min.md`, addendum). `bt_concern` / `own_disappointment` coding frame includes "price won't last". **No survey item added**, to protect survey length. Candidate item if the pilot runs short: "In 12 months, I expect this app's prices to be: higher / same / lower / don't know". |
| N2 | **Payment gaps:** no cash on delivery, no meal-card (e.g. Pluxee) payment — potentially material for salaried professionals | 3 COD + 2 meal-card items | Added **AS25**. New option "the payment method I use (e.g. cash on delivery or a meal card) isn't accepted" in `own_not_tried_reason` (dictionary + both forms/specs); interview probe |
| N3 | **Small carts (< ₹150) cancelled by restaurants; large orders (₹1–2k) feel riskier** | 2 + 3 items | Audit addendum: add a small-cart basket and a large group basket where feasible (`06_competitor_audit/audit_addendum_from_social.md`) |
| N4 | **Late-night false "delivered"** | One thread with ≥ 12 "same happened" replies | Late-night slot already in the audit; `beh_last_meal` includes late night; interview probe |
| N5 | **Preference for an explicit, labelled fee** over "free delivery" with inflated menus | 9 items | Consistent with the H2.2 bill-transparency test (already fielded) |
| N6 | **Swiggy Toing seen as the like-for-like rival** | 23 mentions | Toing already in platform lists; audit adds Toing where it operates |
| N7 | **Hyderabad launch timing:** "Not available in Hyderabad!" (2026-08-21) → Ownly staff "officially LIVE in Hyderabad" (≈ 2026-09-11) | 3 dated items | `context.md` §2: launch *likely* between late August and ~11 September 2026 (INTERPRETATION, unconfirmed). Hyderabad users are therefore at most weeks old, which strengthens the tenure-confound warning (E §4). |

## 4. What this means for the hypotheses (signals only)

| H | Direction of signal | Strength |
|---|---|---|
| H1 Problem intensity | Incumbent fee pain exists (fee stacks, DIY workarounds) | Weak |
| H2 Price value | **Mixed** — real but inconsistent savings | Weak |
| H4 Price vs reliability | **Contested**; failures dominate first-hand posts | Weak–moderate (convergent across corpora) |
| H7 Brand | Two-sided | Weak |
| H8 Fee WTP | Fee confusion; labelled-fee preference | Weak |
| H9 Transfer | Bengaluru failure modes are operational and could transfer; no Hyderabad data | None for Hyderabad |
| H12 Repeat | First-order experience looks pivotal; durability scepticism may cap commitment | Weak |

## 5. Validation still required before any dashboard use

1. Two team members blind-code the 37 app reviews and a 50-item social sample, then compute Cohen's κ per theme family.
2. Open every URL behind any quote before using it. Never quote rows marked as tool summaries.
3. Team members hand-log 150–300 "most recent" Play Store reviews from a phone to reduce the "most relevant" sorting bias.
