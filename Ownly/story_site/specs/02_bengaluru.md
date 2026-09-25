# 02 · What happened in Bengaluru

**Purpose:** show the playbook being copied into Hyderabad, and that it worked *on the restaurant side*.

> **How to use this file.** It defines *what information the screen carries and how that information
> should be drawn* — not the final look. Visual styling is decided separately (see `../research/
> design_system_references.md`). Every fact below is already verified against a file in this repo;
> the source is named next to it. If a number has no source line, it is not allowed on screen.


## What the viewer leaves with
- Ownly's Bengaluru run in six beats.
- The restaurant revolt is the engine of the story: supply came first, demand was assumed.

## Content inventory (all from `FINAL_STORY/data/s1_timeline.csv`)
| When | Event |
|---|---|
| Aug 2025 | Pilot in 3 Bengaluru areas |
| Mar 2026 | Citywide launch, ~20,000 restaurants, zero commission |
| Jul 2026 | 1,000+ restaurants threaten to quit Swiggy/Zomato |
| Jul 2026 | Ownly goes live inside the Rapido app |
| Aug 2026 | MoU with NRAI; 50,000+ orders a day |
| Sep 2026 | Live in Gachibowli, Hyderabad — no restaurant revolt |

Supporting: **221 restaurants** already listed on Ownly at our Gachibowli address
(`final_dashboard/data/market_context.csv`, first-hand check).

## Visuals
1. **Horizontal scroll timeline** — the six beats as stations on a line that moves as you scroll; the
   Hyderabad station is the only coloured one.
2. **Supply-vs-demand split** at the end of the line: 221 restaurants listed (supply, full) against
   0 of 326 orders in our sample (demand, empty). Two columns, same scale, one full one empty.

## Motion
- The timeline line draws left→right, scrubbed to scroll (pinned section, ~150vh of scroll).
- Each station pops when the line reaches it; its label fades up.
- The supply/demand columns fill on entry: supply fills fast, demand stays at zero for a beat too long.

## Tech notes
- Pinned horizontal scroll: GSAP ScrollTrigger `pin + scrub`, or CSS `animation-timeline: view()` for the simple version.
- Keep the whole line in one SVG so the draw is a single `stroke-dashoffset` tween.

## Acceptance
- [ ] Six beats, verbatim from the CSV
- [ ] The Hyderabad beat is visually distinct
- [ ] Works without scroll-jacking on a trackpad
