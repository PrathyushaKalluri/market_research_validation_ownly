# Ownly Marketing Metrics — Pure-Visual Dashboard Specification

**Scope:** one screen, 1440×900, ten metrics (MM1–MM10) plus the not-estimable set, zero body prose. Python-generated SVG, animated in page.

---

## STEP 1 — What we actually have

### 1.1 Canonical source: `final_dashboard/data/marketing_metrics.csv`

| ID | Metric | Value | Num/Den | Base | Evidence | Status flag |
|---|---|---|---|---|---|---|
| MM1 | Switch-Threshold Coverage | **81.1% → 56.1% → 27.3%** | 107/132, 74/132, 36/132 | 33 threshold-givers × 4 baskets | STATED PREF × OBSERVED | COMPUTED |
| MM2 | Offer Reversal Rate | **50.0%** | 2/4 | 4 matched baskets | PRIMARY OBSERVED | COMPUTED |
| MM3 | Membership Erosion Rate | **25.0%** | 1/4 | 4 matched baskets | PRIMARY OBSERVED | COMPUTED |
| MM4 | Sample Volume Share | **0.0%** | 0/326 | catchment n=40, 1 count unusable | STATED BEHAVIOUR | SAMPLE ONLY — **LOWER BOUND** |
| MM5 | Penetration Share | **5.6%** | 2/36 | catchment n=40 | STATED BEHAVIOUR | SAMPLE ONLY |
| MM6 | Unit Share of Requirements | **18.8%** | 3/16 | n=2 Ownly users, all cities | STATED BEHAVIOUR | **VERY LOW BASE** |
| MM7 | Assortment Barrier Rate | **65.0%** | 26/40 | catchment n=40 | STATED PREFERENCE | COMPUTED |
| MM8 | Rapido Discovery Gap | **84.8%** | 28/33 | Rapido users n=33 | STATED BEHAVIOUR | COMPUTED |
| MM9 | Trial-to-Repeat Intent Gap | **52.5pp** | 77.5% − 25.0% | catchment n=40 | STATED PREFERENCE | **PROXY** |
| MM10 | Fee Load Advantage | **18.2pp** | 23.4% − 5.2% | 37 priced captures | PRIMARY OBSERVED | COMPUTED |

I recomputed every one from source and all reconcile exactly. Wilson 95% intervals (computed, not in the CSV): MM1 73.5–86.8 / 47.5–64.2 / 20.4–35.4 · MM2 15.0–85.0 · MM3 4.6–69.9 · MM5 1.5–18.1 · MM6 6.6–43.0 · MM7 49.5–77.9 · MM8 69.1–93.3 · MM9 endpoints 62.5–87.7 and 14.2–40.2.

**MM1's internal structure is the most chartable thing in the whole dataset.** It is a 33 × 4 matrix: 33 stated rupee thresholds crossed with 4 observed per-basket savings. Threshold distribution (n=33 who named an amount): ₹10 : 3 · ₹20 : 5 · ₹30 : 9 · ₹50 : 7 · ₹75 : 4 · ₹100 : 5. Per-basket savings:

| Basket | LIST+FEES | MEMBER | AFTER OFFER |
|---|---|---|---|
| Bawarchi | +₹41.84 | **−₹0.16** | **−₹110.80** |
| Cream Stone | +₹71.19 | +₹28.19 | +₹20.05 |
| Paradise Biryani | +₹157.81 | +₹127.81 | **−₹76.19** |
| Shah Ghouse | +₹174.50 | +₹126.99 | +₹87.50 |
| **median** | **₹114.50** | **₹77.59** | **−₹28.07** |

Counting thresholds cleared per basket gives 17+24+33+33 = 107, 0+8+33+33 = 74, 0+8+0+28 = 36 — i.e. MM1, MM2 and MM3 are all readable off one picture.

### 1.2 `metric_dictionary.csv` — superseded, and materially different

43 rows on an **n=46 Hyderabad-eligible** base, not the n=40 catchment base. Differences that matter:

- **The MM numbering is completely reassigned.** Old MM1/MM2 (Price Win Rate 100%, Median Basket Saving ₹114) are no longer marketing metrics at all — they live as KPIs K20a/K21a. Old MM3/MM4 (offer reversal, membership erosion) became new MM2/MM3. Old MM5/MM5b (Switching Reach @ ₹114 = 100%, @ −₹28 = 0%) were **replaced** by new MM1, which is a far better metric: it crosses every threshold with every basket instead of collapsing to the median.
- **Three formula-sheet share metrics were added** at MM4/MM5/MM6 (volume share, penetration, share-of-requirements). None existed in the old file.
- **Old MM7 Incumbent Lock-in (83%, 38/46) was dropped** from the MM set entirely.
- **Values moved with the base change:** assortment barrier 67% → 65.0%; Rapido gap 85% → 84.8%; trial-to-repeat gap **43pp → 52.5pp** (post-offer continuation fell 35% → 25%).
- Only MM10 Fee Load Advantage (18.2pp, n=37) is unchanged.

**Live defect:** `index.html` tab 03 renders the *superseded* set — its nine cards read 100% / ₹114 / 50% / 25% / 67% / 83% / 85% / 44pp / 18pp on an n=46 base. Six of those nine contradict `marketing_metrics.csv`. The new dashboard must be built from the canonical CSV, and tab 03 should be regenerated or retired, or the site contradicts its own data folder.

### 1.3 The current house standard in tab 03 (to be kept)

Headline + subhead, then `.cards` — `grid-template-columns: repeat(auto-fit, minmax(168px, 1fr))`, `gap:1px` with the gap filled by `var(--rule)` so the grid reads as a hairline table; `.cval` Georgia 29px, `.clab` 11.5px, `.csub` 10px muted carrying `n=`. Risk cards get `.warn` (value in `#B4552F`). Tokens: `--cream #F2EBDD · --panel #FBF8F1 · --rule #D5C9B4 · --dark #443533 · --muted #8C7F78 · --blue #2F6094 · --coral #EF7259`. Wrap max-width 1180px.

**What to keep:** the hairline 1px-gap grid, the cream/panel/rule surfaces, the value-then-label-then-base hierarchy, and the `.warn` distinction. **What to change:** Georgia on in-chart numerals (§3.6.3), the palette (§3.6.4), and the fact that there is no chart at all — nine cards is a KPI row, not a dashboard.

### 1.4 Everything in `data/` that feeds a marketing metric

| File | Feeds |
|---|---|
| `switch_threshold_coverage.csv` | MM1 — the three coverage values + median savings |
| `switching_staircase.csv` | MM1 — the threshold distribution forming the x-axis mass (and the 4 "no amount" + 3 "don't know" exclusions) |
| `audit_pairs.csv` | MM1 (per-basket savings), MM2, MM3 — 12 rows = 4 baskets × 3 views |
| `audit_platform_prices.csv` | MM2/MM3 — per-platform payable in each view; the waterfall's step components |
| `sample_volume_share.csv` | MM4 — all three bases (Gachibowli 326, Hyderabad 398, Bengaluru 146) |
| `bengaluru_benchmark.csv` | MM4/MM5 — reference row (aware 75%, tried 25%, n=16) |
| `funnel_research.csv` | MM5 — the five funnel stages with step-retention |
| `cleaned_survey.csv` / `derived_survey_metrics.csv` | MM5–MM9 respondent-level marks |
| `tradeoff_summary.csv` | MM7 + its two siblings, with CIs (speed 7.5%, reliability 27.5%, restaurants 65.0% refuse) |
| `audit_clean.csv` | MM10 — 37 priced captures, `non_food_share` per row |
| `not_estimable.csv` | Tile 11 — exactly 10 rows |
| `evidence_matrix.csv` | the evidence-glyph grouping by row |
| `segment_cuts.csv`, `segment_tradeoffs.csv`, `segment_switch_threshold.csv` | hover layer only — segment splits |
| `audit_coverage.csv`, `eta_gap_by_restaurant.csv`, `market_context.csv`, `audit_slot_quality.csv` | context, **not** MM feeders |
| `kpi_table.csv`, `hypothesis_results.csv`, `associations.csv`, `anomalies.csv`, `review_*`, `youtube_*`, `interview_*` | other layers — no MM feeds them |

Two numbers I had to recompute from `audit_clean.csv` because they are in no summary file: **Ownly median non-food share 5.2% (n=8 priced), Swiggy 28.3% (n=15), Zomato 18.0% (n=14), pooled incumbent 23.4% (n=29) → 18.19pp.** Also median quoted ETA Ownly 39.5 vs Swiggy 22.5 / Zomato 17.5 min, per-restaurant gap 17.5–24.0, median 19.5.

---

## STEP 2 — Professional standard, with sources

### 2.1 Penetration / share-of-requirements (Ehrenberg-Bass)

- **Ehrenberg-Bass Institute — "The Double Jeopardy Law in B2B shows the way to grow"** (marketingscience.info/news-and-insights/the-double-jeopardy-law-in-b2b-shows-the-way-to-grow). Readable because the canonical form is an **ordered table sorted by penetration descending**, with loyalty columns beside it — the sort *is* the analysis; the eye runs down penetration and watches loyalty decay in step. Their "Average" bottom row is a built-in benchmark that tells you whether a brand is a deviation.
- **Rungie, *Marketing Bulletin* 15** (marketing-bulletin.massey.ac.nz/V15/MB_V15_T2_Rungie.pdf) and **Bassi, *Marketing Bulletin* 22**. Readable because of the **observed-vs-theoretical paired row** — `O` directly above `T` for each brand, so deviation is a vertical gap, not a computed column.
- **Anesbury et al., *J. Consumer Behaviour* 2022** (duplication of purchase). Readable because the brand×brand matrix is **ordered by penetration on both axes and carries an "average duplication" row at the foot** — the expected gradient runs diagonally, and partitions show as blocks breaking it.
- **Kantar Worldpanel Brand Footprint.** Readable because Consumer Reach Points = penetration × frequency × households is **decomposed on the page into its two drivers side by side** — you see the score and which component moved.
- **CPG Data Insights, "The Panel Data Chart Every CPG Analyst Should Understand"**. Readable because the **decomposition tree makes the arithmetic identity the layout** — Sales splits to Penetration × Buy Rate, Buy Rate to Frequency × Spend.
- *Honest caveat:* the penetration-vs-frequency **scatter** is widely reproduced but Ehrenberg-Bass's own public pages present Double Jeopardy as tables, not scatters. No first-party citable scatter figure exists. I use the scatter below because a table is text, and I say so.

### 2.2 Funnel and switching

- **Amplitude, "Interpret your funnel analysis"**. Readable because each step is **one bar split into a solid converted region and a lighter/striped dropped region** — the loss is drawn at the same scale as the survival instead of inferred from shrinking widths. A dropdown reframes the same data as "largest drop-off step", so the chart names the worst step rather than making you hunt.
- **Amplitude's three companion views** (Conversion over Time / Time to Convert / Frequency) — the funnel answers "how many", the histogram answers "how long", the question a plain funnel silently drops.
- **GA4 funnel exploration** (support.google.com/analytics/answer/9327974). Readable because the **open-funnel toggle splits each bar into new vs continuing entries** — closed-vs-open becomes a stated, switchable assumption instead of a hidden one.
- **Ashok Charan (NUS), "Gain–loss, Brand Switching Analytics"** (ashokcharan.com/Marketing-Analytics/~cp-consumer-panel-gain-loss.php). Readable because gains and losses split to **opposite sides of a zero axis**, broken into new/lost/increased/decreased/switched, with an **Interaction Index normed to 100** (>115 above expected, <85 below) putting every competitor on one comparable scale.
- **Greenbook, "Correspondence Analysis of Brand Switching and Other Square Tables"**. Readable because **rows and columns are ordered identically**, so retention is a visible diagonal ridge and switching is everything off it.
- **Flourish Sankey docs.** source/target/value is the entire data contract — and their own rule: collapse small ribbons into "Other" before drawing.

### 2.3 Price thresholds, elasticity, coverage

- **Conjointly, Van Westendorp PSM**. Readable because **the four intersections are named on the plot itself (PMC, OPP, IPP, PME)** — the chart delivers four numbers, not four lines — and the acceptable range is **shaded**, converting an intersection puzzle into a band you can point at. They also disclose an analytic choice (no curve inversion) next to the chart — the model for our honesty layer.
- **Sawtooth, Van Westendorp.** All four series share **one cumulative-% y-axis and one price x-axis**, and curves are labelled **at the line ends** rather than in a legend, so four crossing lines need no colour lookup.
- **Conjointly / Sawtooth, Gabor-Granger.** **Two stacked panels over a shared price axis** — demand above, revenue below, revenue peak marked — putting the decision directly beneath its cause. Direct precedent for MM1.
- **Storytelling with Data, "#SWDchallenge: the waterfall chart"**. The first and last bars are **anchored to the baseline while the middle bars float**, increases and decreases coloured differently, each floating bar labelled with its delta — exactly the list → fees → membership → coupon structure.
- **Storytelling with Data, "more on slopegraphs"**. Two labelled value columns joined by lines make **rank change and magnitude change visible at once**, direction carrying the message, no delta column.
- **Cleveland & McGill, JASA 79(387), 1984.** The empirical ranking — position on a common scale > non-aligned position > length > angle > area — is *why* dumbbells and dot plots beat paired bars for price comparison. Position judgements ~1.4–2.5× more accurate than length.
- **Tornado charts.** Bars extend left/right from a **base-case vertical line, sorted longest-at-top** — the sort order is the finding.

### 2.4 Competitive-share dashboard layout

- **IBCS, SUCCESS framework** (ibcs.com/standards/). **SAY** — every exhibit carries an explicit message, the title states the finding; **CONDENSE** — raise density rather than spreading thin; **UNIFY** — the same meaning always takes the same visual form, which is what makes a multi-chart dashboard scannable rather than re-learned chart by chart.
- **Gene Zelazny, *Say It With Charts*** (McKinsey's Director of Visual Communications). The chart form is chosen **from the comparison being made** after the message is written. Origin of the "action title" convention: read a deck's titles alone and you get the argument. Cite Zelazny — McKinsey and BCG do not publish exhibit style guides.
- **Dona M. Wong, *The WSJ Guide to Information Graphics***. Structured as paired **dos and don'ts at the level of individual mechanics** — gridline weight, label placement, colour count, axis breaks — and the source strip at the foot of every exhibit is a WSJ-lineage convention, not decoration.
- **Tufte's small multiples.** "Once viewers understand the design of one chart, they have immediate access to the data in all the other charts" — a 12-panel comparison costs the reader one chart-reading, not twelve.
- **Datawrapper Academy, line-chart customizing / "why no axis labels"**. **Direct line labelling with connector lines, label coloured to line**, replacing the legend; and dropping axis labels whose content is already in the title. Both remove a lookup step between mark and name.
- **Microsoft, "Competitive Marketing Analysis sample for Power BI"**. Organised as **named single-screen pages by question**, with drill-through and report-page tooltips so density lives in the hover layer. Microsoft explicitly warns a large tooltip obscures the report — the hover layer has a size budget too.

### 2.5 Honesty and uncertainty inside a chart

- **IBCS semantic notation** (via Zebra BI / Inforiver — normative text is behind the paid Standards 2.0). **Actual = solid dark fill; previous period = lighter solid; plan/budget = outlined hollow; forecast = hatched**, with scenario codes in the axis labels and green/red reserved for variance. The transferable idea: **hatching means "not measured"; outline means "target, not outcome"** — consistently, so an estimate never looks like a fact.
- **FT Visual Vocabulary**. Charts grouped by **communicative intent — Deviation, Correlation, Ranking, Distribution, Change over Time, Part-to-whole, Magnitude, Flow** — form follows message, not habit. Its Uncertainty section is marked under development; cite FT for intent grouping, not as a finished uncertainty spec.
- **Datawrapper Academy, "How to show confidence intervals in bar charts"**. A **range overlay** from lower/upper-bound columns; **striped/hatched patterns for a look-through effect**; the option to make the bar transparent; the rule to **put the interval definition in the title**. The reason it matters is **within-the-bar bias** — readers judge values inside a bar as more likely than values outside it, so an error bar drawn over a solid bar is systematically misread. This directly dictates §3.4E.
- **Padilla, Kay & Hullman, "Uncertainty Visualization" (Wiley 2022)**. **Frequency-framed and discrete-outcome encodings (quantile dotplots, HOPs) are read more accurately than continuous error bars**, because readers count objects instead of estimating a smear. The citation for the unit charts and dot strips below.
- **Hullman, "Why Authors Don't Visualize Uncertainty"** (arxiv.org/pdf/1908.01697). Authors omit uncertainty for identifiable reasons — fear of undermining credibility, no good default encoding. The citation for building the convention deliberately.
- **BBC `bbplot` / R cookbook**. The honesty mechanic is structural: `finalise_plot()` **stamps the source strip as part of the export step, not the design step** — it cannot be forgotten. Our build script does the same.
- *Honest caveat:* **there is no published standard for an in-chart "n=" badge.** Present ours as our own convention, defined once in a key. Also: no verified Kantar switching Sankey, no nameable Tableau market-share Viz of the Day, no public Reuters graphics guide — do not cite those.

---

## STEP 3 — The specification

### 3.1 Dashboard architecture

**Canvas.** 1440 × 900, light only (projected). Outer margin 40px → content 1360 × 820. Header band 64px. Source strip 32px. Tile band = 900 − 40 − 64 − 24 − 32 − 28 = **712px**.

**Grid.** 12 columns, 20px gutter, content 1360 → column = (1360 − 220)/12 = **95px**. An *n*-column tile is `115n − 20` wide: 2col = 210 · 3col = 325 · 4col = 440 · 5col = 555 · 6col = 670.

**Rows.** Three, heights **240 / 240 / 192**, 20px gaps (240+20+240+20+192 = 712 ✓).

**Layout.**

```
┌──────────── 6col ────────────┬──── 3col ────┬──── 3col ────┐  240
│ MM1  Switch-Threshold        │ MM2  Offer   │ MM3  Member- │
│      Coverage (3 panels)     │    Reversal  │  ship Erosion│
├────── 4col ──────┬───── 4col ─────┬───── 4col ─────────────┤  240
│ MM4 Volume Share │ MM5 Penetration│ MM6 Share of Reqts     │
├── 3col ───┬─2col─┬─── 3col ───┬─2col─┬────── 2col ─────────┤  192
│ MM7 Trades│ MM8  │ MM9 Trial→ │ MM10 │  NOT ESTIMABLE (10) │
│           │Rapido│    Repeat  │ Fees │                     │
└───────────┴──────┴────────────┴──────┴─────────────────────┘
        source strip — 10 evidence glyphs + slot + date       32
```

Row 3 sums 3+2+3+2+2 = 12 ✓.

**Reading order, established without prose — five devices:**

1. **Size.** MM1 is the only 6-column tile and the only one with three panels. The eye enters top-left at the largest object.
2. **Evidence-glyph clustering by row.** Row 1 is all price evidence (● and ◑●), Row 2 all stated-behaviour share (◐), Row 3 mixed. The glyph column teaches the dashboard's structure without a heading. (IBCS **UNIFY**.)
3. **Shared domains across tiles.** MM2/MM3 share the signed-₹ y-axis. MM7/MM9/MM10 share the 0–100 %-of-respondents x-domain across row 3, so bar lengths are comparable *between* tiles. MM1's three panels share one x-domain.
4. **Titles set inside the plot**, top-left, 12.5px/600, ink — never above the tile, so the title travels with the chart when exported alone (Zelazny/IBCS **SAY**: title states the metric, annotation states the finding).
5. **Direct labels, not legend boxes.** Exactly one legend on the whole dashboard — MM4's 4-swatch strip. Every other tile is single-series-plus-emphasis or ≤3 series with end labels.

**The one negotiated text exception:** the 32px source strip — 10 evidence glyphs in tile order, the audit slot (`wed_dinner`), capture date (`2026-09-16`), survey window. Stamped by the export step, not the design step, so it cannot be forgotten.

---

### 3.2 Per-metric chart specification

#### **MM1 — Switch-Threshold Coverage** · 6col × 240 · `viewBox="0 0 642 212"`

**Form:** three-panel small multiple of an **inverse-cumulative (step/survival) curve with observed-saving reference rules and a shaded cleared region**.

- **x (all three panels, identical domain):** *stated required recurring saving to switch main app, ₹ per order*. Linear 0 → 200. Ticks 0/25/50/75/100/125/150/175/200, tabular-nums, 10px.
- **y:** *cumulative % of the 33 threshold-giving respondents whose stated bar is ≤ x*. 0 → 100, ticks 0/25/50/75/100.
- **Step curve:** 2px ink step line rising 9.1 → 24.2 → 51.5 → 72.7 → 84.8 → 100.0 at ₹10/20/30/50/75/100.
- **Reference rules:** four 1px vertical hairlines per panel at that view's per-basket savings, each capped with a 7px dot at its intercept on the curve. Panel 1 at ₹41.84/71.19/157.81/174.50; panel 2 at −0.16/28.19/127.81/126.99; panel 3 at −110.80/20.05/−76.19/87.50.
- **Negative savings** push two rules off the left edge in panel 3 — drawn as a coral wedge in the 12px left margin. Reads as "below zero" wordlessly.
- **Shaded region:** area under the curve left of that panel's median saving, coral at 12%.
- **Panel condition labels** (inside plot, top-left, 11px/500 muted, .06em): `LIST + FEES` · `+ MEMBERSHIP` · `+ COUPON`.
- **Direct labels:** the four basket names at the top of each rule — `Bawarchi · Cream Stone · Paradise · Shah Ghouse` — **in panel 1 only**, inherited by position (label once, small-multiples discipline).
- **Hero numerals:** `81.1%` · `56.1%` · `27.3%`, 30px/600 sans, coral, top-left of each panel, proportional figures.
- **The annotation that carries the insight:** a single 2px coral polyline drawn *across the three panel hero numerals*, descending left to right, filled arrowhead at `27.3%`. That line is the finding. It animates last.
- **Honesty:** a 135°-hatched strip in the left margin, height proportional to 7/40, marks the 7 respondents excluded (4 "no amount", 3 "don't know"). Median-saving tick labels `₹114.50 · ₹77.59 · −₹28.07` sit on each x-axis.
- **Why:** the Gabor-Granger cumulative-demand form. It is the only form that shows *why* coverage falls rather than *that* it falls — the reader sees the observed savings slide left past the mass of the threshold distribution. A 3-bar chart of 81/56/27 hides the mechanism. Fixing the x-domain across panels makes the fall a visual fact (Tufte).

#### **MM2 — Offer Reversal Rate, 50%** · 3col × 240 · `viewBox="0 0 297 212"`

**Form:** **slope chart** over a signed-saving axis.

- **x:** two ordered categorical positions — `LIST + FEES` → `AFTER COUPON`.
- **y:** *Ownly saving vs cheapest incumbent, ₹, signed*. Domain −125 → +200. **Zero line 1.5px ink**; everything else hairline.
- **Marks:** four 2px lines. The two crossing zero downward in coral `#D64A2E`; the two staying positive in de-emphasis `#B9AE9E`. Endpoint dots r=5, 2px surface ring.
- **Direct labels at right endpoint only:** `Bawarchi −₹111` · `Paradise −₹76` · `Cream Stone +₹20` · `Shah Ghouse +₹88`.
- **The annotation:** the region below y=0 filled with a coral wash at 10%, `2 of 4` set inside it at 24px/600. Reversal is a region you fall into, not a percentage.
- **Why:** reversal is a before→after change per item, and the reader must see *which* baskets flip and *by how much*. The slope chart is the canonical before/after form (Knaflic) and puts the zero crossing — the event being measured — at a fixed readable y. A 50% bar hides that one basket flips by ₹111.

#### **MM3 — Membership Erosion Rate, 25%** · 3col × 240 · `viewBox="0 0 297 212"`

**Form:** **waterfall / bridge** on the median saving.

- **x:** five ordered positions — `LIST + FEES` (anchored) → `− membership` (floating) → `+ MEMBERSHIP` (anchored) → `− coupon` (floating) → `AFTER OFFER` (anchored).
- **y:** *median Ownly saving vs cheapest incumbent, ₹*. Domain −60 → +130, zero line 1.5px.
- **Marks:** anchors at ₹114.50, ₹77.59, −₹28.07 in `#17518F`; floating deductions −₹36.91 (membership) and −₹105.66 (coupon) in coral. 4px rounded data-end, square at baseline, 2px surface gaps, 1px solid connector rules between step tops.
- **Direct labels:** the delta on each floating bar; the value on each anchor.
- **The annotation:** under each anchor, a micro 4-cell unit strip of baskets won — `■■■■` (4/4) → `■■■□` (3/4) → `■■□□` (2/4). The 25% and 50% rates are *counted*, not read.
- **Hero numeral:** `25.0%` with Wilson **4.6–69.9** as a hatched range overlay beneath — never a whisker over a bar (within-the-bar bias).
- **Why:** begin-quantity / deductions / end-quantity is exactly what a waterfall is for (SWD), and it separates the *durable* deduction (membership, a standing benefit) from the *episodic* one (coupon) as two physically different steps. A different family from MM2 also stops the reader mistaking the two metrics for one measurement.

#### **MM4 — Sample Volume Share, 0 of 326** · 4col × 240 · `viewBox="0 0 412 212"`

**Form:** **100% stacked horizontal bar, small multiple by base (3 rows)**.

- **x:** *share of self-reported delivery orders, last 4 weeks*, 0–100%.
- **y:** Gachibowli catchment (326 orders) · Hyderabad eligible (398) · Bengaluru benchmark (146).
- **Segments, fixed order, never re-sorted:** Ownly `#D64A2E` | Swiggy `#17518F` | Zomato `#3E8FD6` | Other `#8A7A6E` (neutral residual, direct-labelled, never a fourth identity). 2px surface gaps, bar height 22px. Row 1: 0.0/54.6/36.8/8.6. Row 2: 0.0/50.8/37.4/11.8. Row 3: **2.05**/27.4/63.0/7.5.
- **The lower-bound mark:** rows 1–2 have a zero-width Ownly segment. Draw a **3px-wide coral outlined stub at x=0, no fill, with a `^` caret above it** — the statistical "at least this" convention. Beside it, one 135°-hatched ghost cell per unusable count (1 on row 1, 2 on row 2). Absence is drawn, not omitted.
- **Legend:** the only one on the dashboard — 4-swatch strip above row 1, in segment order.
- **Direct labels:** `54.6` and `36.8` inside their segments (they fit); `8.6` outside the bar end; `2.05%` outside on row 3.
- **The annotation:** a 1px coral leader from the zero-width stub on row 1 down to the 2.05% fill on row 3. One connector that says *this is what a non-zero looks like*.
- **Honesty:** the plot is **fenced** — visible open brackets on both ends. Each row's y-label is a **micro unit strip of dots**, one per respondent (40/46/16). Row 3 sits below a 1px rule at 75% chroma — a reference, not a peer.
- **Why:** 100% stacked bar is the part-to-whole form for ≤6 segments, and three as small multiples let the reader compare Ownly's sliver against a market where Ownly demonstrably exists. The outlined stub + caret is IBCS's outline-means-not-outcome grammar doing the work of "this is a lower bound, not a measured zero".

#### **MM5 — Penetration Share, 5.6%** · 4col × 240 · `viewBox="0 0 412 212"`

**Form:** **stepped funnel on a true count axis, each bar split converted / dropped** (Amplitude's device), *not* a tapering trapezoid.

- **x:** *respondents*, linear 0–40. Bar length is literally a count.
- **y:** five ordered stages — in catchment (40) → ordered online in 4 wks (36) → aware of Ownly (17) → browsed Ownly (7) → ever ordered (2).
- **Marks:** five bars, each a solid `#17518F` converted region plus a **135°-hatched continuation to the previous stage's length** showing who dropped. Loss drawn at the same scale as survival. Final bar coral.
- **Step-retention arcs:** 1px arcs between bars labelled `90%` · `47%` · `41%` · `29%`.
- **Direct labels:** count at each bar end — 40 · 36 · 17 · 7 · 2.
- **The n=2 treatment:** the last bar is **two discrete unit squares**, not a continuous bar. Two people, not a rate (Padilla/Kay/Hullman: discrete outcomes read more accurately).
- **The annotation:** a coral bracket tying bar 2 (36 orderers) to bar 5 (2 triers), carrying `5.6%` at 26px — because 5.6% is 2/36, not 2/40, and the bracket says which denominator without saying it.
- **Comparison mark:** 1px hatched ghost outlines at Bengaluru's rates (75%/25%, n=16) over the "aware" and "ever ordered" bars, 40% opacity.
- **Honesty:** fenced plot box (research sample, not a market funnel) + ◐ glyph.
- **Why:** funnels are the form for sequential attrition; a true count axis keeps areas honest, and the split converted/dropped bar makes the drop legible rather than inferred.

#### **MM6 — Unit Share of Requirements, 18.8%** · 4col × 240 · `viewBox="0 0 412 212"`

**Form:** **penetration × purchase-frequency scatter** — the Double Jeopardy plane.

- **x:** *brand penetration within the sample* — % of catchment orderers using the brand in 4 weeks. 0–100.
- **y:** *average orders per user, 4 weeks*. 0–8.
- **Marks:** four dots r=6, 2px surface ring. Catchment recompute: Swiggy (75.8, 6.5) · Zomato (72.7, 4.5) · Other (33.3, 2.1) · **Ownly (0, 0)** as an open coral ring pinned to the origin.
- **Second, visually distinct mark:** the all-cities Ownly-user point carrying the canonical SOR 18.8% — **hatched**, because it rests on a different base (2 users, 16 orders). Two bases must never share one mark style.
- **Direct labels:** `Swiggy 69% · Zomato 47% · Other 23% · Ownly 0%` beside each dot.
- **The annotation:** a 1px muted Double-Jeopardy trend line through the three observed brands, plus a coral arrow from Ownly's origin ring to the nearest point on it. The arrow is the finding: small brands have fewer buyers *and* those buyers buy less often, so Ownly's problem is on both axes at once.
- **Hero numeral:** `18.8%` with Wilson **6.6–43.0** as a hatched range bar beneath. An interval that wide *is* the honest statement about n=2.
- **Why:** an SOR figure alone has no reference frame; the penetration × frequency plane is the discipline's standard frame, and it makes 18.8% at 0% penetration read as a directional reading from two people rather than a market position. *Scatter, not the canonical ordered table, because a table is text — see §2.1 caveat.*
- **Build requirement:** the catchment recompute (n=33 orderers) and the canonical MM6 base (n=2, all cities) must be regenerated on the canonical n=40 base before publishing, or the two marks are not comparable.

#### **MM7 — Assortment Barrier Rate, 65%** · 3col × 192 · `viewBox="0 0 297 164"`

**Form:** **diverging stacked bar centred on the choice midpoint**.

- **x:** *% of 40 respondents*, −100 (took the ₹30 cheaper option) ← 0 → +100 (paid the ₹30 premium to keep the attribute). Centre line 1.5px ink.
- **y:** three ₹30 trades, sorted by refusal descending — usual restaurants (65.0%) · reliability (27.5%) · speed (7.5%).
- **Marks:** premium side coral `#D64A2E`, cheaper side `#B9AE9E`, 2px surface gap at the centre, neutral grey midpoint `#CFC6B6` (never a hue at a diverging midpoint).
- **CIs:** hatched range overlay on the coral side — 49.5–77.9 · 16.1–42.8 · 2.6–19.9 — as a look-through overlay, not a whisker over a solid bar.
- **Direct labels** at each premium-side bar end.
- **The annotation:** a single 1px coral rule at the 50% mark on the premium side. Only the restaurants bar crosses it. The crossing is the finding — the one thing money could not buy.
- **Why:** the three trades are one ordered choice scale, and diverging-stacked centred on the decision point is the canonical form. Sorting longest-at-top makes the chart simultaneously a magnitude chart and a priority list (tornado convention). One shared baseline turns three percentages into one length comparison.

#### **MM8 — Rapido Discovery Gap, 84.8%** · 2col × 192 · `viewBox="0 0 182 164"`

**Form:** **waffle / unit chart, exactly 33 cells**.

- **Grid:** 11 × 3 = 33. No blanks, no rounding. The grid *is* the base. Cells 11×11px, 2px surface gaps.
- **Marks:** 28 cells `#B9AE9E` (have NOT noticed food in Rapido), 5 coral `#D64A2E` (have).
- **Direct labels:** `5` beside the coral block; the 11×3 dimensions readable off the edge.
- **The annotation:** a coral bracket around the 5 filled cells with `84.8%` at 26px outside it, Wilson 69.1–93.3 as a 1px hatched rule under the numeral.
- **Why:** at n=33 a percentage bar invites over-reading. A unit chart with exactly 33 cells makes the base countable — the frequency framing Padilla/Kay/Hullman show is read more accurately than a continuous encoding. It also separates the two halves of the finding: 33 people are *in* the Rapido app (distribution exists) and 28 never saw the food tab (discovery does not).

#### **MM9 — Trial-to-Repeat Intent Gap, 52.5pp** · 3col × 192 · `viewBox="0 0 297 164"`

**Form:** **dumbbell**.

- **x:** *% top-2 box*, 0–100.
- **y:** one row, two points — "would try" **77.5%**, "would continue after the intro offer ends" **25.0%**.
- **Marks:** two r=6 dots, 2px surface rings. Try dot `#17518F` solid. **Continue dot 45°-hatched coral** — a stated-intent proxy, and hatch is the dashboard's proxy grammar. Connector **3px**, the only 3px stroke on the entire dashboard, because the gap *is* the metric.
- **Direct labels** at both dots.
- **The annotation:** `52.5pp` at 26px above the connector, centred on it.
- **Honesty:** Wilson whiskers on both dots — 62.5–87.7 and 14.2–40.2. They do not overlap. The gap survives sampling error, and that can only be *shown* in a wordless dashboard. Whiskers are legitimate here because the marks are dots, not bars.
- **Why:** a dumbbell encodes the gap as physical distance rather than asking the reader to subtract two bar lengths. Cleveland & McGill's position-on-a-common-scale ranking is the empirical reason it beats paired bars.

#### **MM10 — Fee Load Advantage, 18.2pp** · 2col × 192 · `viewBox="0 0 182 164"`

**Form:** **dumbbell over a per-capture dot strip**.

- **x (shared by both layers):** *non-food share of the bill, %*, 0–40.
- **Upper layer:** Ownly **5.2%** ↔ incumbent pooled median **23.4%**, 3px coral connector labelled `18.2pp`.
- **Lower layer** (below a 1px hairline): all **37 priced captures** as r=2.5 dots on the same x axis, 3px vertical jitter, 55% opacity, coloured by platform, 2px surface rings. Ownly n=8 · Swiggy n=15 · Zomato n=14.
- **Direct labels:** `5.2%` / `23.4%` at the dumbbell ends; `Swiggy 28.3` and `Zomato 18.0` as 1px tick rules on the strip.
- **The annotation:** a 1px leader from the coral connector down into the strip, showing the two clouds barely overlap — the gap is not an artefact of one capture.
- **Why:** a pp gap between two medians is a dumbbell. Putting the raw captures underneath is the "distribution under the summary" convention that stops a median computed on n=8 from being read as a fact about every order, and encodes the sample size as something countable.

#### **Tile 11 — NOT ESTIMABLE (10)** · 2col × 192 · `viewBox="0 0 182 164"`

**Form:** **2 × 5 ghost grid of chart silhouettes.**

- Ten cells, each a 1px **dashed** frame on cream at 30% opacity — the only dashing permitted anywhere, and on a tile frame, never a gridline.
- Each cell holds, at 10% ink, the silhouette of the chart that metric *would* have received: Value Share → ghost stacked bar · Relative Market Share → ghost dumbbell · BDI/CDI → ghost scatter · Contribution margin / break-even → ghost crossing lines · Retention Rate → ghost decay curve · CLV → ghost area · CAC → ghost column · CRC → ghost column · EBITDA → ghost waterfall · YoY / CAGR → ghost slope.
- **Nothing labelled at rest.** Hover reveals the name and the "why not computable" line from `not_estimable.csv`.
- **Why:** ten empty frames of the right shape read as "ten measurements missing" in under a second, and they are *countable*. A ten-row prose table breaks the no-text rule; blank space would read as a layout gap rather than a finding.

---

### 3.3 Variety with discipline — the family allocation

Ten chart families across eleven tiles. No two adjacent tiles share a form.

| # | Chart family | Metric | Why this metric earns this family |
|---|---|---|---|
| 1 | **Inverse-cumulative step curve + reference rules** (Gabor-Granger) | **MM1** | the only metric that is a crossing of two distributions |
| 2 | **Slope / bump chart** | **MM2** | before→after per item; the zero crossing is the event |
| 3 | **Waterfall / bridge** | **MM3** | begin → deduct → deduct → end; separates durable from episodic |
| 4 | **100% stacked bar, small multiple** | **MM4** | part-to-whole, ≤6 segments, three comparable bases |
| 5 | **Stepped funnel, split converted/dropped** | **MM5** | sequential attrition on a true count axis |
| 6 | **Scatter in the penetration × frequency plane** | **MM6** | a loyalty figure needs a two-axis reference frame |
| 7 | **Diverging stacked bar** | **MM7** | one ordered choice scale, three items, one decision midpoint |
| 8 | **Waffle / unit chart** | **MM8** | n=33 — make the base countable |
| 9 | **Dumbbell** | **MM9** | the gap is the metric; encode it as distance |
| 10 | **Dumbbell + dot strip (beeswarm)** | **MM10** | a median on n=8 must show its distribution |
| 11 | **Ghost-silhouette grid** | **NOT ESTIMABLE ×10** | absence made countable |

**Exactly two bar-family tiles** (MM4 stacked, MM7 diverging) out of eleven, on different geometries and different axes. No wall of identical bars anywhere.

**The discipline that stops variety becoming chaos:** MM2 and MM3 both plot signed rupee savings and share a y-domain though their forms differ; MM7/MM9/MM10 share the 0–100 x-domain across row 3; MM1's three panels share one x-domain. **Form varies by job; scale is unified by subject** — IBCS UNIFY applied at the axis level rather than the chart-type level.

---

### 3.4 The honesty layer — conventions for a wordless dashboard

Every convention is **defined once in a 28px key** at the right end of the header band, and never explained again. (Per §2.5: the "n=" badge has no industry standard, so it is presented as our own convention, defined once.)

**A. Base-size badge — top-right of every tile.** A micro unit strip of dots, one per unit of base, capped at 40 with a `40+` terminator. MM2 and MM3 literally show **four dots** — far stronger than the text "n=4", because four dots is self-evidently thin and is read, not parsed.

**B. Evidence-type glyph — shape, never colour alone.**
- **●** solid disc — PRIMARY OBSERVED DATA → MM2, MM3, MM10
- **◐** half disc — SURVEY, STATED BEHAVIOUR → MM4, MM5, MM6, MM8
- **○** open ring — SURVEY, STATED PREFERENCE → MM7, MM9
- **◑●** paired — STATED PREFERENCE × PRIMARY OBSERVED → MM1

These cluster by row, so they double as the structural wayfinder.

**C. Fill grammar — our local dialect of IBCS semantic notation,** stated in the key:
- **Solid fill** = measured on observed data
- **45° hatch**, 3px pitch, 1px stroke = **stated preference / proxy** → MM9's continuation dot, MM7's premium overlay, MM6's all-cities dot
- **Outline only**, 1.5px, no fill = **not estimable / lower bound** → MM4's Ownly stub, Tile 11
- **135° hatch** = **excluded / unusable** → MM1's 7-of-40 margin strip, MM4's unusable-count ghost cells, MM5's drop-off regions

IBCS uses hatch for forecast and outline for plan; ours means "not measured" and "not an outcome" — the same logic, declared rather than borrowed silently.

**D. Low-base scrim.** Any tile with base under n=20 — **MM2 (n=4), MM3 (n=4), MM6 (n=2 users / 16 orders)** — gets a 135° hairline hatch across the whole plot at 6% opacity plus a 1.5px dashed tile border in `--warn #B4552F`. The reader perceives "this one is thin" *before* reading the number. Only use of the status colour; never a series colour.

**E. Confidence intervals — overlay, never whisker-over-bar.** Datawrapper's within-the-bar-bias finding is binding:
- **Bar forms** (MM3, MM7) → a **hatched range overlay** with look-through, drawn from the Wilson bounds.
- **Dot forms** (MM9, MM10, MM6) → 1px whiskers with 5px caps at 45% opacity, legitimate because there is no bar to bias the reading.
- MM2's interval (15.0–85.0) and MM3's (4.6–69.9) are enormous. That *is* the honesty, and it is wordless.

**F. "Sample only — not market share" for MM4/MM5/MM6.** Three simultaneous devices: (i) the plot box carries **visible open brackets** on both ends — a fenced, bounded sample; (ii) the y-axis label is a **unit strip of respondent dots** (40/46/16), not an `n=` string; (iii) benchmark rows sit **below a 1px rule at 75% chroma** — a reference, not a peer.

**G. Lower-bound caret.** MM4's Ownly value is 0.0% but flagged LOWER BOUND: a zero-width outlined stub pinned at the baseline with a `^` caret above it, plus a 135°-hatched ghost cell for the unusable response. *Measured zero* and *unusable data* become two visibly different marks.

**H. The ten missing metrics.** Tile 11 as specified — ghost frames holding the silhouette of each metric's would-be chart. Countable absence.

**I. Table-view twin.** Every tile emits a visually-hidden `<table class="sr">` with every mark's label, value, base and evidence type. Tooltips enhance; they never gate. Keyboard focus produces the identical state to hover.

---

### 3.5 Animation choreography

**Section entry** — `IntersectionObserver`, threshold 0.35, fires once. Total ≈ 1.45s.

| t | Element | Motion | Duration / easing |
|---|---|---|---|
| 0 | tile frames | opacity 0→1 | 180ms, stagger **28ms** row-major |
| +120 | axis rules + gridlines | `stroke-dashoffset` → 0 | 240ms ease-out |
| +240 | **bars / columns** | `scaleX`/`scaleY` from the axis, `transform-origin` pinned to the baseline | 420ms `cubic-bezier(.22,.61,.36,1)`, stagger 40ms within tile |
| +240 | **step curves / slopes / connectors** | `stroke-dashoffset` from `pathLength` → 0 | 620ms ease-out |
| +240 | **dots** | `r` 0→6, surface ring after | 180ms, stagger 30ms |
| +240 | **waffle / unit cells** | opacity 0→1 | 120ms, stagger **12ms** — MM8's 33 cells fill in ~0.5s, so the count is *felt* |
| +700 | direct labels + hero numerals | opacity 0→1, translateY 6px→0 | 260ms |
| +700 | hero numerals | **count up from 0**, ease-out, rounded to stated precision (81.1, 56.1, 27.3, 52.5) | 520ms |
| +900 | **the annotation** — coral descent polyline, brackets, reference rules, arrows | draws last | 320ms |
| +1100 | honesty badges, CI overlays, hatch fills | fade to 0.75 opacity | 200ms |

**Two rules that matter more than the timings:**

1. **The annotation lands after the data, never before.** MM1's coral descent, MM2's "2 of 4" wash, MM7's 50% rule, MM6's arrow — an insight that appears before its evidence reads as an assertion.
2. **MM1's three panels animate left → right with 180ms between panels**, so 81.1 → 56.1 → 27.3 is experienced as a fall, not read as three numbers. The single most important motion decision on the screen.

**`prefers-reduced-motion: reduce`** → every duration 0, final state only, no count-up. Non-negotiable.

**Hover / focus** (identical states; Tab order = reading order):

| Element | Behaviour |
|---|---|
| hovered mark | 2px surface ring; fill lightens one ramp step — 120ms |
| siblings in the same tile | drop to 0.35 opacity — 120ms (emphasis-on-hover) |
| tooltip | 140ms delay, anchored to the mark, 11px sans: label · value · base *n* · evidence glyph |
| hit target | ≥24px, includes the 2px surface gap; MM10's dense strip uses a nearest-point layer |
| honesty badge | expands from glyph to a one-line caveat chip from `marketing_metrics.csv:caveat` — **the only prose on the page**, behind hover, so the resting dashboard stays wordless |
| MM1 panels | vertical crosshair follows the pointer on the ₹ axis, both ends labelled; hovering panel 1's curve highlights the same y-position in panels 2 and 3 |
| MM2 / MM3 | hovering a basket in one tile highlights the same basket in the other — same four baskets, so the tiles are linked |
| Tile 11 ghost cell | reveals the metric name and the "why not computable" line |

No filters, no per-chart controls. A presentation dashboard, not an exploration tool — density lives entirely in the hover layer (Power BI convention), and that layer has a size budget: one chip, one line.

---

### 3.6 Python pipeline

#### 3.6.1 Renderer: hand-rolled SVG, **not** matplotlib

Extend the existing stdlib chart kit in `FINAL_STORY/scripts/build_story_v2.py` (`_svg`, `_bar`, `_vbar`, `hbars`, `grouped`, `dumbbell`, `columns`, `staircase`, `waterfall`, `tiles`, `fig`) into a sibling `build_mm_dashboard.py`. Three reasons, in order of weight:

1. **Animation requires stable, targetable elements.** Every mark needs a class and id so CSS can reach it. Matplotlib's SVG backend emits anonymous `<path>` soup; the only way in is `Artist.set_gid()` one artist at a time, it does not survive every backend, and it still gives no per-segment `transform-origin` — bar-grow animation would need a post-processing pass over the emitted XML anyway.
2. **The repo already guarantees** "every chart is SVG written by Python: no chart library, no CDN, no external request", with figures read from the CSVs so a number cannot drift from its source. Matplotlib breaks that guarantee and adds a dependency to a deliverable that currently has none.
3. **Nothing in the ten forms needs a statistical renderer.** Every mark is a `rect`, `path`, `circle` or `text`.

*If matplotlib were mandated anyway:* `rcParams['svg.fonttype']='none'` (text stays text so the page font applies), `rcParams['svg.hashsalt']='ownly'` (deterministic, diffable ids), `figure.dpi=100`, `savefig(transparent=True, bbox_inches='tight')`, `artist.set_gid('mm1-step-3')` on every animatable artist, plus a post-process pass to inject `transform-origin`. Strictly more work for a worse result.

**New primitives to add:** `steps()` (MM1) · `slope()` (MM2) · `waterfall_signed()` (MM3) · `stacked100()` (MM4) · `funnel_split()` (MM5) · `scatter_dj()` (MM6) · `diverging_stack()` (MM7) · `waffle()` (MM8) · `strip()` (MM10) · `ghost_grid()` (Tile 11). Shared helpers: `whisker()`, `range_overlay()`, `badge()`, `hatch_defs()`.

#### 3.6.2 Exact figure sizes for a 1440 × 900 projector

SVG has no DPI. Author every tile in a **1:1 pixel viewBox matching its rendered box**, so one user unit = one CSS pixel at 1440 width; scale with `width:100%; height:auto`.

| Tile | Columns × row height | `viewBox` | Plot area (after 14px tile padding) |
|---|---|---|---|
| MM1 | 6 × 240 | `0 0 642 212` | 3 panels 198w × 142h, 24px gutters, plot y 34→176 |
| MM2, MM3 | 3 × 240 | `0 0 297 212` | 269 × 142, plot y 34→176 |
| MM4, MM5, MM6 | 4 × 240 | `0 0 412 212` | 384 × 142, plot y 34→176 |
| MM7, MM9 | 3 × 192 | `0 0 297 164` | 269 × 108, plot y 30→138 |
| MM8, MM10, Tile 11 | 2 × 192 | `0 0 182 164` | 154 × 108, plot y 30→138 |

Add `preserveAspectRatio="xMinYMin meet"` and `overflow: visible` (already in `story.css`) so labels outside the plot box are never clipped. Reserve the x-axis band *inside* the container height — a fixed-height card that excludes it produces a nested scrollbar.

At 1440 × 900 projected, 1 SVG unit = 1 real pixel, so a 10px tick is 10 real px — legible at 3m on a 100-inch screen. The same file prints losslessly.

#### 3.6.3 Fonts

**One sans everywhere inside a chart:** `-apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif`.

**Change from the current house style:** drop Georgia from in-chart numerals. The existing `.cval{font-family:Georgia,serif}` puts a serif display face on the hero figure, which reads as off-brand decoration at chart scale. Keep Georgia for **page identity only** — `.pgttl`, `.headline .hl` — so the house voice survives in the chrome and disappears in the data.

| Role | Size / weight | Notes |
|---|---|---|
| tile title (inside plot, top-left) | 12.5 / 600 | ink `#443533`, .01em |
| panel condition label | 11 / 500 | muted, .06em tracking, caps |
| hero numeral | 26–30 / 600 | **proportional figures** — `tabular-nums` makes `121` look loose at display size |
| direct label | 11 / 500 | ink-2 |
| axis tick | 10 / 400 | ink-3, **`tabular-nums`** (they align vertically) |
| badge glyph | 9 | ink-3 |

Text never wears a data colour; identity comes from the coloured mark beside it. Single exception: a label inside a coloured stacked segment (MM4's `54.6`), where contrast against the fill governs.

#### 3.6.4 Colour tokens — validated, not eyeballed

I ran the palette validator. **The current chart colours FAIL on the panel surface `#FBF8F1`:** coral `#EF7259` contrast 2.74:1 (below 3:1); tan `#C9B79A` lightness 0.787 (outside band) and chroma 0.045 (reads grey); blue `#2F6094` chroma 0.100; green `#3F7A5E` chroma 0.077. Green and coral additionally collide under protanopia (ΔE 5.2, below floor).

**Validated replacement — all five checks PASS under `--pairs all` on surface `#FBF8F1`:**

```
--c-ownly   #D64A2E     Ownly
--c-swiggy  #17518F     Swiggy
--c-zomato  #3E8FD6     Zomato
--c-other   #8A7A6E     "Other" residual — neutral, always direct-labelled,
                        never a fourth identity (folded, not a series)
--mute      #B9AE9E     de-emphasis for non-story marks
```

Validator: lightness band PASS · chroma floor PASS · CVD separation worst all-pairs ΔE **19.3** (protan) / 19.9 (tritan) PASS · normal-vision floor ΔE **20.1** PASS · contrast vs surface all ≥3:1 PASS.

**Diverging** (MM2/MM3 signed saving, MM7 choice): poles `#D64A2E` ↔ `#17518F`, neutral grey midpoint `#CFC6B6` (never a hue at the midpoint). Validator: all checks PASS, ΔE 20.0 protan / 32.7 normal.

**Surfaces & ink** — unchanged: page `--cream #F2EBDD` · tile/plot `--panel #FBF8F1` · hairline `--rule #D5C9B4` · `--ink #443533` · `--ink-2 #6F625C` · `--ink-3 #8C7F78`.

**Status, reserved, never a series:** `--warn #B4552F`, used only on the low-base scrim border.

**Brand continuity:** keep `#EF7259` as the Ownly accent in page chrome — headline rules, tab underline, header band — where it carries no data. Use `#D64A2E` for every data mark. The brand still reads; the charts become legible.

**Texture:** exactly two pattern defs — `hatch45` and `hatch135`, 3px pitch, 1px stroke in `--ink-3`, emitted once in `<defs>`. Opt-in only where the honesty grammar calls for it. Never decorative.

#### 3.6.5 Export format

**Inline `<svg>` written directly into the HTML by the build script** — not `<img src="chart.svg">`, not PNG. Inline is the only form where the page's CSS can reach an individual mark to animate it and drive the hover layer, and it preserves the no-external-request property. Each mark carries:

```html
<rect class="mark mm4-seg" data-metric="MM4" data-series="swiggy"
      data-v="54.6" data-n="326" data-ev="stated-behaviour" .../>
```

so the entry animation, the tooltip, the honesty badge and the generated table-view twin all read from the same attributes — one source, four consumers, no drift. The same pass emits the visually-hidden `<table class="sr">` per tile.

#### 3.6.6 Build-time honesty assertion

`build_mm_dashboard.py` reads `final_dashboard/data/marketing_metrics.csv` as the single source of truth for every hero numeral, with the supporting CSVs (§1.4) supplying per-mark detail. Before writing output it asserts that **every hero numeral rendered equals the `value` column for that `metric_id`**, and fails the build otherwise. The source strip is stamped in the same export step, not the design step (BBC `finalise_plot()` discipline), so provenance cannot be forgotten.

That assertion is what keeps the dashboard honest without a person checking it — and it is exactly the check that `index.html` tab 03 currently fails (§1.2).

---

## Key findings the caller should act on

1. **`index.html` tab 03 is showing superseded numbers.** Six of its nine cards contradict `marketing_metrics.csv` (different base: n=46 vs n=40; trial-to-repeat gap shown as 44pp vs the canonical 52.5pp; "Incumbent Lock-in 83%" and "Price Win Rate 100%" are no longer marketing metrics at all). Fix or retire it.
2. **The current chart palette fails accessibility validation** on the site's own surface — four of four hues fail at least one check, and the green/coral pair is indistinguishable under protanopia. A validated replacement is specified in §3.6.4.
3. **MM1 has far richer structure than its three headline numbers** — it is a 33 × 4 matrix, and the coverage figures 107/132, 74/132, 36/132 reconcile exactly from the threshold distribution crossed with per-basket savings. This makes the Gabor-Granger step-curve form possible and turns the metric from an assertion into a mechanism.
4. **MM6 needs recomputing before publishing.** Its canonical numerator/denominator (3/16, n=2 users, all cities) sits on a different base from every other Row-2 metric (catchment n=40), and the two cannot share a mark style without lying.
5. **Two MM10 components exist in no summary file** and must be computed at build time from `audit_clean.csv`: Ownly median non-food share 5.2% (n=8), pooled incumbent 23.4% (n=29).
6. No files were created or edited. This is specification only.