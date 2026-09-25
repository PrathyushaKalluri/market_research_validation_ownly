# 07 · What 124 people told us

**Purpose:** the survey, visualised — Hyderabad *and* Bengaluru, because Bengaluru is our control group.

> **How to use this file.** It defines *what information the screen carries and how that information
> should be drawn* — not the final look. Visual styling is decided separately (see `../research/
> design_system_references.md`). Every fact below is already verified against a file in this repo;
> the source is named next to it. If a number has no source line, it is not allowed on screen.


## What the viewer leaves with
- Who answered, and the four findings that matter.
- That Bengaluru — 18 months ahead — looks worse than you would expect.

## Content inventory (base: 40 catchment unless stated; source `survey_all_rows_with_flags.csv`)
| Finding | Number |
|---|---|
| Already pay a rival membership | 33 of 40 = 82.5% (19 pay both) |
| Median saving needed to switch | ₹30 (33 named a figure; 4 said no amount; 3 don't know) |
| Trade speed for ₹30 | 37 of 40 = 92.5% |
| Trade reliability for ₹30 | 29 of 40 = 72.5% |
| Trade usual restaurants for ₹30 | 14 of 40 = 35.0% (McNemar vs speed p = 1.5e-06) |
| Expect low prices to rise | 35 of 40 = 87.5% |
| Would stay after the intro offer | 10 of 40 = 25.0% |
| Noticed food inside Rapido | 5 of 33 Rapido users = 15.2% |
| Ownly funnel | aware 42.5% · opened 17.5% · ordered 5.0% |
| Orders in 4 weeks | 326 total: Swiggy 178 · Zomato 120 · other 28 · **Ownly 0** |

**Bengaluru panel (n=16 eligible, 20 responses):** aware 75% · opened 37.5% · ordered 25% ·
Ownly 3 of 146 orders = 2.1% · median switch ₹50 · would stay after offer 46.7% · expect prices to rise
80% · noticed food in Rapido 41.7% · of the 4 who tried it, 3 would be "not disappointed" if it vanished,
and they stopped because offers ended (2), late deliveries (1), went back to their membership (1).

## Visuals
1. **Who answered** — a unit chart: 124 dots, coloured by city, with the 40 analysed highlighted.
2. **The ₹30 panel** — three horizontal bars with intervals (92.5 / 72.5 / 35.0), the third in red.
3. **The staircase** — cumulative share switching at ₹10…₹100.
4. **Two-city funnel** — dumbbell, Gachibowli vs Bengaluru, three stages.
5. **The four Bengaluru triers** — four small portraits-as-cards, each with why they stopped.
6. **Orders donut** — 326 orders by app, with Ownly's 0 as an empty wedge outline.

## Motion
- The 124 dots scatter in, then sort themselves into city columns, then the 40 light up.
- Bars grow left→right; intervals draw after.
- The donut's empty Ownly wedge stays outlined and never fills — hold it for a beat.

## Honesty rules
- Bengaluru panels carry "16 people — direction, not size" permanently, not on hover.
- The 4 triers are counts, never percentages.

## Acceptance
- [ ] Every number matches the source CSV
- [ ] Bengaluru is visually distinct from Hyderabad everywhere
