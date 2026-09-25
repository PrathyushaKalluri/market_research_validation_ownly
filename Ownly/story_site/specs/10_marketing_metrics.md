# 10 · Marketing metrics  ★ key screen — dashboard only, no prose

**Purpose:** the ten marketing metrics as a pure instrument panel.
**Owner:** marketing-metrics agent → `../research/marketing_metrics_spec.md` — **LANDED (514 lines).
That document is the build spec for this screen.** The notes below are the summary.

> **Blocking finding:** `final_dashboard/index.html` tab 03 is also on superseded numbers — six of its
> nine cards contradict `marketing_metrics.csv` (n=46 vs n=40; trial-to-repeat shown as 44pp against the
> canonical 52.5pp; two of its "marketing metrics" are no longer marketing metrics at all).

> **How to use this file.** It defines *what information the screen carries and how that information
> should be drawn* — not the final look. Visual styling is decided separately (see `../research/
> design_system_references.md`). Every fact below is already verified against a file in this repo;
> the source is named next to it. If a number has no source line, it is not allowed on screen.


## Hard rules for this screen
1. **No sentences.** Chart titles, axis labels, direct labels and legends only.
2. **Six or more different chart families** across the ten metrics — never ten bars.
3. Every tile shows its base (n) inside the chart frame.
4. The not-estimable metrics are present as **ghost tiles**, not omitted.

## Content inventory — source of record `final_dashboard/data/marketing_metrics.csv`
| ID | Metric | Value | Base |
|---|---|---|---|
| MM1 | Switch-threshold coverage | **81.1% → 56.1% → 27.3%** | 107/74/36 of 132 pairs |
| MM2 | Offer reversal rate | 50.0% | 2 of 4 baskets |
| MM3 | Membership erosion rate | 25.0% | 1 of 4 baskets |
| MM4 | Sample volume share | **0.0%** | 0 of 326 orders — sample only, a lower bound |
| MM5 | Penetration share | 5.6% | 2 of 36 |
| MM6 | Unit share of requirements | 18.8% | 3 of 16 — very low base |
| MM7 | Assortment barrier rate | 65.0% | 26 of 40 |
| MM8 | Rapido discovery gap | 84.8% | 28 of 33 |
| MM9 | Trial-to-repeat intent gap | **52.5 pp** | 78% try vs 25% continue, n=40 |
| MM10 | Fee-load advantage | 18.2 pp | 37 priced captures |

Plus the 10 **not estimable** business metrics (CLV, CAC, retention, EBITDA, YoY…) from
`final_dashboard/data/not_estimable.csv`, shown as a single ghost row with the reason encoded visually.

## Architecture (from the spec)
1440×900, 12 columns, three rows of tiles (240 / 240 / 192) plus a 32px source strip.
**MM1 is the only 6-column tile and the only one with three panels** — the eye enters top-left at the
largest object. Reading order is established without prose by five devices: size, evidence-glyph
clustering by row, shared axis domains across neighbouring tiles, titles set *inside* the plot, and direct
labels instead of legends (exactly one legend on the whole screen).

**Eleven chart families, no two adjacent tiles alike, and only two bar-family tiles out of eleven.**
Form varies by job; **scale is unified by subject** — MM2/MM3 share a signed-₹ axis, MM7/MM9/MM10 share a
0–100% domain across row 3, MM1's three panels share one x-domain.

**The honesty layer, all wordless and defined once in a 28px key:**
- **Base-size badge** = a strip of dots, one per unit of base. MM2 and MM3 literally show **four dots** —
  far stronger than "n=4", because four dots is read, not parsed.
- **Evidence glyph by shape, never colour:** ● observed · ◐ stated behaviour · ○ stated preference · ◑● both.
- **Fill grammar:** solid = measured · 45° hatch = stated/proxy · outline only = not estimable or a lower
  bound · 135° hatch = excluded/unusable.
- **Low-base scrim:** any tile under n=20 (MM2, MM3, MM6) gets a hairline hatch and a dashed warn border,
  so the reader perceives "this one is thin" *before* reading the number.
- **Intervals never sit on top of bars** (the within-bar bias): bars get a hatched range overlay, dots get
  whiskers. MM2's interval is 15.0–85.0 and MM3's is 4.6–69.9 — **that enormity is the honesty**.
- **MM4's zero is a lower bound, not a measurement:** an outlined stub with a `^` caret, plus a separate
  hatched ghost cell for the one unusable response. Measured zero and unusable data must look different.
- Every tile emits a visually-hidden table; hover enhances, never gates.

## Chart assignment (superseded by the spec's per-metric section — kept as the index)
| Metric | Form | x | y |
|---|---|---|---|
| MM1 | Slope / three-state bar | price view | % of respondent × basket pairs cleared |
| MM2, MM3 | Paired win/loss dot strip over 4 baskets | basket | cheaper app |
| MM4 | Donut with an empty outlined wedge | — | share of 326 orders |
| MM5, MM6 | Nested-square (part-of-whole) | — | triers / orderers |
| MM7 | Diverging stacked bar | — | paid premium vs took the ₹30 |
| MM8 | Waffle, 33 squares, 28 filled | — | Rapido users |
| MM9 | Dumbbell, trial vs continue | % | — |
| MM10 | Stacked bill composition, 3 apps | app | share of bill |

## Motion
- Tiles reveal in reading order, 60ms stagger; each chart's marks animate from zero.
- MM4's empty wedge is the last thing to resolve, and it resolves to nothing.
- Hover: the tile lifts 2px and reveals its formula in a mono line. Hover is enhancement only.

## Python pipeline
- One script generates all ten as SVG at fixed tile dimensions, from the CSVs, with stable element ids.
- No chart library in the page; animation is CSS classes applied to the generated SVG.

## Act on before building
1. **MM6 needs recomputing** — its base (3/16, n=2 users, all cities) differs from every other row-2
   metric (catchment n=40). Two bases cannot share a mark style without lying.
2. **Two MM10 components exist in no summary file** and must be computed at build time from
   `audit_clean.csv`: Ownly median non-food share 5.2% (n=8), pooled incumbent 23.4% (n=29).
3. **The current chart palette fails validation** on our own surface — the green/coral pair is
   indistinguishable under protanopia. Replacement specified in the research doc §3.6.4.

## Acceptance
- [ ] Zero prose on the screen
- [ ] ≥ 6 distinct chart families
- [ ] Sample-only and proxy metrics visually marked
- [ ] Every value matches `marketing_metrics.csv`
