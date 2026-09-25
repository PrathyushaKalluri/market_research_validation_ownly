# 03 · What the secondary research said

**Purpose:** show that we did not start from opinion — we started from what happened to every other
price-led challenger, and to platforms that entered delivery on top of existing infrastructure.

> **How to use this file.** It defines *what information the screen carries and how that information
> should be drawn* — not the final look. Visual styling is decided separately (see `../research/
> design_system_references.md`). Every fact below is already verified against a file in this repo;
> the source is named next to it. If a number has no source line, it is not allowed on screen.


## What the viewer leaves with
- Price-led entry has a documented failure pattern.
- That pattern is what made our hypothesis falsifiable rather than a hunch.

## Content inventory
| Claim | Evidence | Source |
|---|---|---|
| Discount-led growth collapses when the discount stops | Foodpanda India fell from ~200,000 to ~5,000 orders a day once discounts stopped | `FINAL_STORY/data/evidence.csv` R-rows; challenger dossiers in `01_secondary_research/` |
| Delivery economics do not forgive a thin fee | Uber Eats lost ~$2.55 on a ~$2.45 average order at exit | `final_dashboard/data/kpi_table.csv` K23 rationale |
| A rival's discount play beat Ownly over 3 months | JP Morgan on Swiggy's **Toing** being "materially more successful" | `07_fake_door/FAKE_DOOR_REDESIGN_v3.md` §2 |
| Ownly's own stated model | "Everyday low prices rather than discount-led growth"; "We don't force discounts" | Storyboard18, Inc42 (quoted in the same file) |
| Evidence quality | 5 dossiers, ~230 sources, 68 catalogued claims: 50 media report, 10 company claim, 5 fact, 5 contradicted | `01_secondary_research/evidence_table.csv` |

## Visuals
1. **The challenger graveyard** — a small-multiples row: one sparkline per challenger, each ending in a
   drop, Ownly's left deliberately blank ("not written yet"). *This is the emotional beat of the screen.*
2. **Claim-quality bar** — one stacked bar of the 68 claims by evidence type, showing how little is fact
   and how much is company claim. Teaches the audience to distrust the press coverage.
3. **Two pull-quotes** — Ownly's own words, set as evidence, not decoration.

## Motion
- Sparklines draw left→right in sequence, 300ms apart; the drop at the end of each is emphasised by a
  dot that falls and a faint red trail.
- The empty Ownly panel gets a blinking cursor — the story we are about to write.

## Honesty rules
- Foodpanda/Uber Eats figures are **media-reported**, not ours; they carry a "media report" badge.
- Never present a secondary figure in the same visual style as our own measured data.

## Acceptance
- [ ] Every secondary claim badged by evidence type
- [ ] Ownly's own claims quoted verbatim with publication and date
