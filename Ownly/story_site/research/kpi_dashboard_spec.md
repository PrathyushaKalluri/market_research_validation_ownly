# Screen 06 — KPI system: visualisation spec

## 0. Four things to fix before any pixels

**0.1 The tree we called the standard is drawn on superseded numbers.** `final_dashboard/index.html`
renders an older n=46 base. Bind everything to **`kpi_table.csv`** and nothing else.

| Tree shows | `kpi_table.csv` says |
|---|---|
| Awareness 37% (n=46) | **42.5%**, 17 of 40 |
| Median saving ₹50 (n=35) | **₹30**, n=33 named |
| Coverage 91.7% (11/12) | **90.0%**, 9 of 10 |
| Lock-in 82.6% | **82.5%**, 33 of 40 |
| Trade-offs 84.8 / 67.4 / 32.6 | **92.5 / 72.5 / 35.0** |
| Fee load 5.2 / 28.3 / 18.0 | **4.8 / 27.4 / 15.1** |

Keep the tree's **row grammar** (it is genuinely excellent); regenerate its **values**.
`metric_dictionary.csv` gets stamped SUPERSEDED.

**0.2 Only 2 of 8 headline KPIs carry a confidence interval.** The repo's intervals are 95% Wilson and
reproduce exactly. Back-fill from `evidence.csv`: **K4 90% → CI 59.6–98.2**, K5 88.9% → 56.5–98.0.
"90%" and "90%, but it could be 60%" are different claims; the second is the true one.

**0.3 K17 is contradictory** — `PARTIALLY UNAVAILABLE` in the KPI table, "0 of 326 orders" in the chart
data. Show the counted fact, name the contradiction, and **never draw a zero-height bar**: the zero
measures the four-week question window, which predates Ownly's Hyderabad go-live.

**0.4 A naming trap.** Family 4 is called *Preferred-Restaurant Coverage*, but its headline is K4
*Audit-frame* coverage. The metric the family is named after, K6, is NOT COMPUTABLE. Put K6 in the card
as a hatched row, or rename the family.

## 1. Architecture — one screen, 1920×1080 canvas scaled to fit

```
HEADER          y   0–96
TREE            y 112–740
INSTRUMENT RAIL y 764–836
FOOTER          y 860–900
```

| Band | x | w | Contents |
|---|---|---|---|
| A — input drivers | 0 | 620 | 5 family cards (price · switching bar · assortment · service · distribution) |
| B — spine | 644 | 168 | `DRIVES` → ACQUISITION box → RETENTION box |
| C — output | 836 | 344 | family 7 card + funnel strip + ₹30 strip |
| D — north star | 1204 | 396 | NS ghost panel + K23 guardrail ghost panel |

**A constant 132px value gutter across all four bands.** That single alignment is what makes 26 numbers
scannable — the frame never moves, so the eye compares values instead of layouts.

**Projector type floor: nothing below 13px in the canvas.** The current tree sets source and CI lines at
9.5px, which is sub-legible from the back of a room.

Connectors: 2px beziers, no arrowheads on the guardrail (a T-bar — a guardrail gates, it does not drive).
ACQUISITION ← cards 2, 3, 6. RETENTION ← cards 4, 5.

**The operator rule (the opinionated one).** Real metric trees join parent to child with `×` or `+`
because they decompose. **Ours does not** — you cannot multiply coverage by ETA gap to get retained
orders. So **no operators anywhere on the tree**. Exactly one `×` appears on the screen, inside the north
star panel, because it is the CSV's own formula: `D30 repeat rate × avg 30-day order frequency`.
That asymmetry is informative: the one place the arithmetic is real is the one place we have no data.

**The instrument rail** (72px, full width, 5 equal segments):
`SURVEY 124→40` · `PRICE AUDIT 79 captures / 4 baskets` · `FAKE DOOR 70 sessions` ·
`REVIEW MINING 836 coded` · `OWNLY / RAPIDO ✕ no access` (greyed, hatched).
Thin ticks rise from each segment to the families it feeds. **The fifth segment being visibly empty, in
the same rail as four full ones, is the most honest object on the screen** — the whole study in 72px.

## 2. Per-KPI chart forms

Two project rules govern everything: 30+ = fine · 10–29 = direction · **under 10 = a count, never a %**.
So **K1a (n=4) and K4 (n=10) may never be drawn as percentage bars.** A 100% bar at n=4 would be the most
dishonest object in the deck.

| KPI | Value | Form | x | y |
|---|---|---|---|---|
| **NS** retained order rate | NOT COMPUTABLE | **Empty frame** | days since first order 0–30 | cumulative repeat rate |
| **K1a** price win rate | 4 of 4 | **Slopegraph**, 4 baskets across 3 price views | *what the customer has* | saving ₹, zero rule |
| **K13** switching price | ₹30 (n=33) | **Staircase / ECDF** | ₹10·20·30·50·75·100 | cumulative % who'd switch |
| **K4** coverage | 9 of 10 | **Unit grid**, 10 named restaurants × 3 apps | platform | restaurant |
| **K7** ETA gap | +17 min | **Dumbbell**, 4 restaurants | quoted minutes 0–50 | restaurant |
| **K9** Rapido discovery | 15.2%, CI 6.7–30.9 | **CI dot plot**, 3 rows | % 0–100 | the three rows |
| **K18** repeat intent | 25% (10/40) | **Two 40-dot unit arrays** + CI | — | — |
| **K23** margin | NOT COMPUTABLE | **Empty ledger** (T-account) | — | — |

**K1a slopegraph:** four matched baskets crossing three views — ₹114.50 → ₹77.59 → **−₹28.07**; lines
that cross below the ₹0 rule turn red. The crossing *is* the finding; a 100% bar hides three numbers.

**K13 staircase:** the median line drops at ₹30, and **the 7 held-out respondents (4 "no amount",
3 "don't know") get their own grey block outside the curve** — coding them as zero would inflate it,
coding them as infinity would flatten it, and the data explicitly refuses both.

**K4 unit grid:** ten named restaurants, plus a fully hatched row for **K6 — never measured**, quoting
the reason: *"the live instrument never asks respondents to name their usual restaurants."*

**K7 dumbbell:** the connector *is* the metric. Across four restaurants the gap is flat (+17.5 to +24.0)
— the signature of a supply-density problem, not a logistics one. Title block carries
**QUOTED ETA, NOT DELIVERY PERFORMANCE** — no test orders were placed.

**K9 CI dot plot:** three rows — noticed food 15.2% (5/33) · aware among Rapido users 33.3% (8/24) ·
aware among non-users 56.2% (9/16). **The two awareness intervals overlap heavily; annotate that.**
Resisting the tempting "Rapido users are *less* aware!" headline is the most credibility-earning
annotation in the deck.

**K18 unit arrays:** 40 dots per row, one per respondent — 35 filled for price-durability doubt,
10 filled for repeat intent. At n=40 a dot array is a census of the sample. Nobody argues with a count.

### The two we could not measure

**NS — the empty frame.** Draw the *complete* chart: both axes, ticks, labels, gridlines — and leave the
plot region empty under a 45° hatch, with a centred plate: the formula, `0 rows available`, **NEEDS:**
Ownly cohort export, **WHY NOT:** stated intent is not behaviour. Then a small inset showing K18 (25%)
joined by a **dashed** connector labelled *closest available proxy*.

> A greyed-out "no data" card is an absence. A fully drawn, fully labelled instrument with nothing in it
> is an **accusation** — it shows the exact shape of what is missing and names who holds it.

**Forbidden in that frame:** any dotted "projected" curve, plausible range, industry benchmark or
comparison curve "for shape". Any curve there is a fabricated north star.

**K23 — the empty ledger.** A T-account where the observed cells are real (delivery fee ₹0, platform fee
₹0, packaging ₹0, commission 0%) and the cost cells are hatched (rider payout, payments, support — not
disclosed). Below a heavy rule, **fenced** and labelled *ANOTHER COMPANY, ANOTHER YEAR*: Uber Eats India
Q1 2019, −$2.55 on a ~$2.45 order. The fence is non-negotiable or it becomes an implied Ownly number.

## 3. The provenance rail — one object, repeated for all 26 KPIs

```
INSTRUMENT ──── BASE ──── FORMULA ──── VALUE ──── CONFIDENCE
```
Identical width and stop positions for every KPI **including the two that cannot be computed** — the
break is legible only because the frame never moves.

- Baseline stroke encodes evidence type: solid blue = primary observed · solid ink = stated behaviour ·
  **dashed = stated preference** (*stated is not done*) · **physically broken = no data**.
- The break is two slashes across the baseline right after the stage that failed, with later stops
  hollow and their **labels still present**: NS and K23 break at BASE (no rows exist); K6 breaks at
  INSTRUMENT (the question was never asked). Different failures, visibly different.
- Evidence strength becomes a 4-segment meter: STRONG ▮▮▮▮ · MODERATE ▮▮▮▯ · DIRECTIONAL ▮▮▯▯ ·
  PROXY ▮▯▯▯ · N/A hatched.

**Three non-negotiables:** the limitation always renders (never hover-only — a tooltip is a caveat you
can avoid reading); the base is always a fraction, never only a percentage; every interval says
**95% Wilson**, stated once per screen.

## 4. Movement — legitimate versus fabrication

There is **no time series anywhere in this project**. Every movement visual must run along a
*non-temporal ordered axis*, and say so.

**Legitimate:** the three price views (axis reads *what the customer has*, never "time") · switch-threshold
coverage 81.1 → 56.1 → 27.3 · the switching staircase · the fake-door funnel, where Direct
(100→73.5→52.9→52.9→**47.1**) and Inside-Rapido (100→91.7→72.2→66.7→**36.1**) cross — Rapido starts
better and finishes worse, which is the best story in the deck · the research funnel, drawn as nested
bases, never labelled "conversion" · the Rapido Link price ladder, because the price was randomised.

**Fabrication — forbidden:**
- Any date axis on a survey KPI. One snapshot.
- **Bengaluru → Gachibowli as a trajectory.** Two samples collected simultaneously, not two time points.
  Draw a paired dot plot with both intervals — with n=16, Bengaluru's awareness CI is 50.5–89.8 against
  Gachibowli's 28.5–57.8, and they nearly touch.
- **The Bengaluru orders/day ramp as a curve.** 5k → 40k → 50k are three press citations with conflicting
  upstream counts. Three dated dots, no connecting line.
- A zero bar for K17. Any projection in the NS frame. Count-up animation on n<30.

## 5. Choreography

Trigger on `IntersectionObserver` at 0.4, play once. **Hard cap: nothing moves after 2,500ms** — the
presenter's first sentence lands around 4s. `prefers-reduced-motion` → all durations 0, final state only.

| T | What |
|---|---|
| 0 | Instrument rail draws left→right, 60ms stagger |
| 320 | Family cards fade + rise 12px |
| 700 | Connectors draw |
| 1000 | Headline numerals resolve |
| 1300 | **CI bars grow outward from the point estimate, both directions** |
| 1500 | NOT-COMPUTABLE hatch sweeps in, 900ms — the slowest thing on screen |
| 1900 | Rail break glyph snaps, no easing |

Three doctrines: **value first, then the interval** (a CI that shrinks onto a value animates precision
arriving from nowhere; one that grows outward animates honest uncertainty) · **absence arrives last and
slowly**, after every measured value has settled · **a break is not a smooth event, it snaps**.

**The count-up rule, tied to our own evidence discipline: a value counts up only if n ≥ 30. Below that it
snaps in as a fraction.** K13, K9, K18, K7 count. K1a snaps to `4 of 4`. K4 snaps to `9 of 10`.
Use `tabular-nums` during the count, proportional on settle.

Per chart: staircase draws, then the median line drops, then the held-out block fades in last · dumbbell
draws rival dot, Ownly dot, *then* the connector, so the gap is seen being created · slopegraph draws the
₹0 rule first, then all four lines simultaneously (staggering would rank baskets that are not ranked) ·
funnel bars wipe **down**, not along · **hollow dots never animate — absence does not get to perform**.

## 6. Python pipeline

**Keep plain SVG written by Python. Do not introduce matplotlib.** Four repo-specific reasons: CSS-variable
theming survives a light/dark flip; animation needs addressable nodes (matplotlib emits `<g id="patch_3">`
and sometimes rasterises text); provenance — CSV → SVG → HTML in one stdlib call; zero dependencies.

**Consolidate three chart kits into one.** `final_dashboard/scripts/charts.py` has the function set
(`staircase`, `forest`, `coverage_grid`, `erosion`, `funnel_steps`, `dotplot`, `matrix`, `hbar`);
`FINAL_STORY/scripts/charts.py` has the CSS-variable colouring; `build_story_v2.py` has a third inline kit
with `dumbbell`. Nine of eleven charts already exist. Only three are new: `ghost()`, `rail()`, `slope()`.

**Palette — validated.** The cream/coral set **fails** the lightness band and chroma floor. The
`story.css` tokens **pass all checks in both modes**: `#2a78d6, #eb6834, #1baf7a` for Ownly / Swiggy /
Zomato. Reserved and never a series colour: absence = neutral grey at 12% + 45° hatch.
One deliberate deviation from general dataviz doctrine: **the hero figure stays Georgia serif** — this is
a research report, not a SaaS dashboard, and the serif numeral signals *ledger*.

**Dimensions:** author every chart on a **620 × H viewBox**, `preserveAspectRatio="xMinYMin meet"`,
`width:100%`. Bars ≤24px, lines 2px, markers r≥4 with a surface ring. **Gridlines solid, not dashed** —
dashing reads as "projection", which is expensive on a deck about a company with no projections. Keep the
dash for exactly two things: the K13 median line and the NS→K18 proxy connector, both of which genuinely
mean *inferred*.

**Animation hookup, ~40 lines total:** emit `pathLength="1"` so one CSS rule animates a 40px connector and
a 600px staircase identically (no `getTotalLength()`); emit counters as
`<text class="count" data-to data-dp data-n>` and have the runtime skip any node with `data-n < 30`.

**Two export fixes:** `final_dashboard/scripts/06_export.py` has a **hardcoded path to a different
machine** (`/Users/klprathyusha/…`) so it cannot run here — derive from `__file__`. And it exports
1500×3600 portrait, which is handout geometry; add a 16:9 path driving the existing `?shot=N` param with
headless Chrome at 1920×1080.

## Sources
Amplitude *North Star Playbook* · KPI Tree, *North Star Framework vs Metric Trees* · Hyperbots *Driver Tree*
· Wilke, *Fundamentals of Data Visualization* ch.16 (graded error bars, deterministic construal error) ·
Brown/Cai/DasGupta 2001 and Agresti & Coull 1998 on Wilson intervals · NN/g *Designing Empty States*
(an empty state per widget, not per page) · Carbon Design System empty-states pattern · Tufte, *Visual
Display* (small multiples, graphical integrity) · Stephen Few, *Common Pitfalls in Dashboard Design*
(the authority against HUD glitz) · Scrollama / The Pudding on IntersectionObserver · web.dev
*Animation and motion* (WCAG 2.3.3, and the caveat that in dataviz the motion may be the information) ·
FT Visual Vocabulary.

---

# ADDENDUM — one correction, four upgrades (verified against primary sources)

## CORRECTION — strike §1.6

The claim that Amplitude's North Star Framework prescribes **"3–6 input metrics"** is wrong — **that rule
does not exist** in the Playbook. (Its "three to six" on p.38 refers to *essential actions where customers
derive value*, a different construct.) So "we have 7 inputs instead of 5" was never a real problem.

The defensible rule comes from the metric-tree literature instead: *"A metric tree should funnel, not fan
out… A metric tree with 200 nodes is not a tree. It is a maze. Start with 20 to 30 nodes."*
**Our system is 26 nodes — precisely inside the recommended range. Say that on the screen.**

Two things worth adopting from the actual Playbook:
- Its canonical diagram runs **top-to-bottom with a LEADING → LAGGING axis**. Our left-to-right layout is
  the metric-tree convention, which is fine — but **add a 13px `LEADING → LAGGING` axis label along the
  bottom of the tree band**. It costs nothing and explains why the north star sits on the far right.
- *"Never try to influence the North Star directly… the goal of the North Star is to be one level out of
  reach."* **That is the caption for our empty NS frame** — it reframes the absence from an apology into
  the design intent.

## UPGRADE 1 — drop the caps on every interval

Our `hbar()` and `forest()` draw I-beams with end ticks. Remove them: caps *"draw attention to the error
bars' endpoints, which are generally not important at all"* (Gelman) — the same deterministic-construal
failure Wilke names, where readers read the endpoint as a hard min/max.

**Use a graded confidence strip:** a 6px band whose alpha falls from 0.35 at the estimate to 0.05 at each
bound. It says *this fades out*, which is true; an I-beam says *it stops here*, which is false. This also
matches the "grow outward from the estimate" animation.

The form to avoid outright now has a name: **"dynamite plots must die"** — a bar with an error bar on top
is *"a graphical representation of a grand total of 4 numbers, regardless of the sample size."* Exactly
why K18 is a 40-dot array.

## UPGRADE 2 — our n≥30 rule has federal backing, and there is a second threshold to adopt

**NCHS/CDC** suppresses a proportion entirely if n < 30, **or** the 95% CI width ≥ 0.30, **or** relative CI
width exceeds 130% of the estimate. Run our headlines against it:

| KPI | Interval | Width | Verdict |
|---|---|---|---|
| K18 repeat intent | 14.2–40.2 | 0.260 | passes, barely |
| K9 Rapido discovery | 6.7–30.9 | 0.242 | passes |
| **K4 coverage** | 59.6–98.2 | **0.386** | **fails — a federal agency would not publish it** |
| K16 Ownly trial | 1.4–16.5 | 0.151 | passes width, **fails relative width (302%)** |

Not a reason to hide K4 — a reason the unit grid is the **only** defensible form. Annotate it exactly so:
*"9 of 10. The interval runs 60–98. This is a count, not a rate."*

**Adopt a second threshold (UK ONS/GSS):** estimates on a base ≤ 25 are **shaded** with a standing note.
Our repo has three bands but no visual token for the middle one. **Add one: any KPI row with n ≤ 25 gets
its value gutter tinted 20%.** Bengaluru (n=16), the fake-door entry points (n=5, 14, 16) and the trigger
question (n=23) all light up — the correct result, currently invisible.

## UPGRADE 3 — the "not measurable" grammar, with precedent and one fix

**Mixpanel's empty metric card** is the vendor precedent: *"Every metric card starts blank… No data
required."* A node with no data is a first-class citizen, not an error state — so the NS and K23 panels are
**the same size and chrome** as measured ones, differing only in fill.

**The rule I got wrong:** a fixed-grey hatch is fragile across backgrounds. Define the hatch as
**`currentColor` at 18% inside a `<pattern>`**, with `color` set on the parent `<g>` from the CSS token, so
it auto-contrasts — darker on bright fills, brighter on dark ones — and stays legible over the Uber Eats
comparator bar in the K23 ledger.

**The hard rule, stated explicitly:** whatever token means *no data* must **not** be a valid member of the
value legend's colour family — not the lightest step of a sequential ramp (reads as "low"), not white
(reads as background or zero).

Three rules that harden §4 (movement):
- **Never interpolate across missing periods; label both ends of the gap** (Carbon).
- **Missing and zero are different.** Highcharts' `connectNulls: true` silently reads nulls as 0 in stacked
  areas — which is exactly the K17 trap: reporting "0 orders" where the field is contradictory.
- **Keep the missing point in the scale domain** so the axis doesn't silently compress (Vega-Lite's
  default) — the formal version of "the NS empty frame keeps its full 0–30 day axis".
- **Solid = measured, dashed = inferred** (Datawrapper). Our NS→K18 proxy connector is already dashed;
  it is now a convention rather than a one-off.

## UPGRADE 4 — no operators: right call, corrected lineage

**No major analytics vendor draws operator glyphs between children.** Mixpanel puts a *correlation
coefficient* on the edge with an explicit "does not imply causation" disclaimer; Power BI's decomposition
tree is a filter drill with no operator; Tableau has no metric tree at all. The operator grammar lives in
the **consulting/finance lineage** — DuPont (ROE = margin × turnover × leverage) and MECE value-driver
trees.

Driver trees come in three types: multiplicative, additive, and **influencing** — *"the child affects the
parent, but the relationship is not a clean formula."* **Ours is entirely the third type.** So the edges
stay bare, and the single `×` in the NS panel is honest because that one edge is genuinely multiplicative.
The framing line for the screen: *"Mathematical decompositions are the strongest form because they are
deterministic: if you know the children, you can calculate the parent exactly."* **We cannot — and saying
so is the point of the tree.**

Rejected option: labelling the influence edges with correlations, Mixpanel-style. We have no correlation
estimates between families, and inventing them would be worse than silence.

## MINOR — two for the choreography

- **No scroll-jacking** (Bostock): keep scrolling *"rapid, incremental, and reversible"*, and note that
  *"making everything position-fixed so nothing moves reads as broken."* Our `scroll-snap: proximity` plus
  keyboard paging is compliant — **do not tighten it to `mandatory`.**
- **Archie Tse, NYT:** *"If you make the reader click or do anything other than scroll, something
  spectacular has to happen."* The KPI screen has no interaction at all, which is right for a projected
  deck — and this is the authority for refusing hover tooltips as the primary read path.

*Nothing in this addendum changes the band geometry, the chart-form table, the movement rules or the pipeline.*
