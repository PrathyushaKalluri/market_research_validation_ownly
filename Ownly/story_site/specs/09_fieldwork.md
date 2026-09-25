# 09 · We went outside

**Purpose:** the primary, physical work — we ordered the food, met the rider, fought support, and priced
every restaurant by hand across three apps.

> **How to use this file.** It defines *what information the screen carries and how that information
> should be drawn* — not the final look. Visual styling is decided separately (see `../research/
> design_system_references.md`). Every fact below is already verified against a file in this repo;
> the source is named next to it. If a number has no source line, it is not allowed on screen.


## What the viewer leaves with
- This team left the building. The evidence is photographic.
- The price audit is real observation, not a scrape.

## Part A — the order we placed
| Element | Content | Asset |
|---|---|---|
| The handover | Photo with the rider, Gachibowli, night | `assets/firsthand/07_field_team_delivery_handover.png` |
| The receipt | La Pino'z via Ownly, 23 Sep 2026, ₹765 | `02_order_receipt_lapinoz_23sep.png` |
| What went wrong | Ordered a 22cm giant slice, received a fraction of it; food cold; cutlery missing | `01_complaint_small_pizza.png` |
| Support | 21:54 complaint → 22:20 first reply (26 min) → 22:27 25% refund offered on one item → 22:29 "since we haven't heard from you, we'll close this chat" → 22:37 we reopen → 22:55 refund confirmed | `03`, `04`, `05`, `06_*.png` |
| Our rating | 1 star | `04_support_refund_offer_1star.png` |

Ties to: **79% of app-store reviews mention support/refund failure** (29 coded reviews, 70% are 1-star) —
`final_dashboard/data/review_theme_summary.csv`, `review_star_distribution.csv`.

## Part B — the price audit (task 3.3)
| Element | Content | Source |
|---|---|---|
| Method | One address (DP1), one evening slot, three apps within minutes of each other, same basket | `06_competitor_audit/audit_slot1_results.md` |
| Scale | 79 captures · 37 priced · 4 matched baskets · 10-restaurant frame | `audit_data_slot1.csv` |
| Result | Ownly cheapest 4 of 4 on list+fees, median ₹114.50 cheaper; 3 of 4 after membership; **2 of 4 after coupons, −₹28 median** | `audit_pairs.csv` |
| Fees | Ownly 5.2% of bill vs incumbent median 23.4% | `audit_clean.csv` |
| Speed | Ownly 39.5 min vs Swiggy 22.5, Zomato 17.5 → +17 min | `eta_gap_by_restaurant.csv` |
| Coverage | 9 of 10 frame restaurants on Ownly; Pizza Hut missing; Aanimuthyalu Ownly-only | `audit_coverage.csv` |

## Visuals
1. **The photo cluster → sorted bins** (the user's request): photos enter scattered and rotated, then on
   scroll they sort themselves into three labelled bins — *the order*, *the support*, *the field*.
2. **A receipt-as-chart**: the real bill redrawn as a stacked bar (food / fees / tax) beside the same
   basket on Swiggy and Zomato. The receipt image sits next to it as proof.
3. **Audit matrix**: restaurant × app grid, cells coloured by who was cheapest, with the coupon view as a
   second state the viewer can toggle — the cells flip and the winner changes. This is the single best
   demonstration of the whole price story.
4. **ETA dumbbell**: Ownly vs cheapest incumbent per restaurant.

## Motion
- Cluster→bins uses FLIP (measure scattered positions, animate to grid).
- The audit matrix flip is a 3D card flip per cell with a 40ms stagger, so the reversal reads as an event.

## Honesty rules
- One order is one order. Never state it as a rate; it illustrates the 79%, it does not measure it.
- The audit is one address, one slot, 4 matched baskets — "directional" badge stays on.

## Acceptance
- [ ] Every photo has a caption naming date and place
- [ ] The coupon-flip state is clearly a different view, not an animation flourish
