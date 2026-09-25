# 01 · Problem statement

**Purpose:** the question, and why this question. **Nothing else on this screen.**
**Status:** content locked, motion to design.

> **How to use this file.** It defines *what information the screen carries and how that information
> should be drawn* — not the final look. Visual styling is decided separately (see `../research/
> design_system_references.md`). Every fact below is already verified against a file in this repo;
> the source is named next to it. If a number has no source line, it is not allowed on screen.


## What the viewer leaves with
- One sentence they could repeat back.
- One reason it is worth three weeks of work.

## Content inventory
| Element | Exact content | Source |
|---|---|---|
| **The problem statement** | "Will Ownly's Bengaluru value proposition transfer to Gachibowli — and what do 20–35 year-old students and professionals need before they switch and stay?" | `FINAL_STORY/Ownly_Hyderabad_Story.html` §1 |
| **Why this problem** (three supporting facts, shown as marks, not prose) | ① Ownly reached **50,000+ orders a day, ~10% share**, in Bengaluru within a year. ② It went live in **Gachibowli ~2 weeks before we fielded**, so the question is live, not hypothetical. ③ **No internal data exists** for a two-week-old market, so it has to be answered from outside. | `FINAL_STORY/data/s1_timeline.csv`; `_ops/decisions.md`; `final_dashboard/data/not_estimable.csv` |

## Visuals
- **Type as the visual.** The statement is set large; the three reasons appear as three small marks
  around it (a share ring at 10%, a two-week clock, a locked database glyph).
- No chart on this screen. The next screen carries the first chart.

## Motion
- Statement types on in two beats: the question first, then "— and what do they need before they switch **and stay**" emphasised.
- The three marks draw in sequence (SVG stroke draw, 400ms each, 120ms gap) as the eye travels down.
- Scroll out: the statement shrinks and pins to the top-left as a persistent breadcrumb for screens 02–05.

## Layout
- Statement max 18 words per line, never more than 3 lines.
- Reasons sit on a 3-column baseline grid beneath, each ≤ 12 words.

## Tech notes
- Marks are inline SVG with `stroke-dasharray` draw-on; no library needed.
- The pin uses `position: sticky` rather than a scroll library, so it survives reduced-motion.

## Acceptance
- [ ] Exactly two things on screen: the statement and why
- [ ] Zero numbers without a source
- [ ] Readable in 5 seconds
