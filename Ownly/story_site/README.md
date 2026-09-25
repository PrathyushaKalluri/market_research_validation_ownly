# Ownly · Story Site

A scroll-driven story website that presents the whole study: who we are, the problem, why we chose it,
what we read, what we built to test it, what the data said, and what Ownly should do.

**Status:** specs being written. No site code yet. Analysis and Propositions screens are deliberately
left as stubs until the earlier screens are locked.

---

## 1. The flow (decided)

The order follows what we actually did, because that is the story that earns each number.

| # | Screen | The one thing it does | Spec |
|---|---|---|---|
| 00 | Opening | Who we are, what this is | `specs/00_opening.md` |
| 01 | Problem statement | The question, and why this question — nothing else | `specs/01_problem.md` |
| 02 | What happened in Bengaluru | The playbook that is being copied here | `specs/02_bengaluru.md` |
| 03 | Secondary research | What history says about price-led challengers | `specs/03_secondary_research.md` |
| 04 | From question to hypothesis | Narrowing to a falsifiable claim and a demographic | `specs/04_hypothesis.md` |
| 05 | The data plan | What to collect, why, and with which instrument | `specs/05_data_plan.md` |
| 06 | **KPI system** | The tree, and how each KPI was actually measured | `specs/06_kpi_dashboard.md` |
| 07 | Survey results | 124 responses, visualised | `specs/07_survey.md` |
| 08 | **Fake door** | A working fake app, auto-playing, and what it recorded | `specs/08_fake_door.md` |
| 09 | We went outside | Rider, food, support chat, and the price audit | `specs/09_fieldwork.md` |
| 10 | **Marketing metrics** | Pure dashboard, no prose | `specs/10_marketing_metrics.md` |
| 11 | Analysis | *stub — write after 01–10 are locked* | `specs/11_analysis.md` |
| 12 | Propositions | *stub* | `specs/12_propositions.md` |

---

## 2. The central decision: KPIs versus marketing metrics

They are drawn differently **because they answer different kinds of question**, and making them look the
same is the mistake most decks make.

| | KPI screen (06) | Marketing-metrics screen (10) |
|---|---|---|
| The question it answers | *What causes what?* | *What is the level?* |
| Form | **A driver tree.** One north star, seven drivers, each node carrying value + interval + the instrument badge | **A dashboard grid of small multiples.** Ten metrics, ten tiles, six different chart families |
| Why that form | Our KPIs are a causal argument about a business, and a tree is the only form that shows an argument | Our marketing metrics are levels and shares with no causal claim; a grid invites comparison, which is the point |
| Text | A short rationale line per KPI is allowed | **None.** Titles, axes and direct labels only |
| Movement | Only where movement genuinely exists: the three price views, the switching staircase, the funnel. Never a fabricated trend line | Same rule — no invented time series |
| Honesty | Two KPIs are **not computable** without Rapido's data; they appear as ghost nodes stating what data would unlock them | Sample-only, n=4 directional and proxy metrics carry visual conventions (hatch, ghost tile, badge) |

**Why we can't show most KPIs "moving":** Ownly launched in Hyderabad ~2 weeks before fielding and we
have no internal data, so almost every figure is one snapshot. Drawing a trend would be fabrication.
What we *can* show moving is a value under different conditions — which is what the price views, the
staircase and the funnels are.

---

## 3. Folders

```
story_site/
  README.md          this file
  specs/             one brief per screen (the working documents)
  research/          agent output: design references, KPI viz, marketing viz, fake-door map
  assets/            images used by the site
    team/            headshots (TO SHOOT)
    firsthand/       food, receipt, support chat, rider  (have: FINAL_STORY/images/firsthand)
    prototype/       fake-door screens (have: FINAL_STORY/images/prototype; more to capture)
    survey/          exported survey charts
    audit/           price-audit visuals
    secondary/       case-study marks and logos
  data/              CSV extracts that feed the charts (copied from final_dashboard/data)
  src/               the site itself (not started)
```

## 4. Agent assignment

| Agent | Owns | Writes to |
|---|---|---|
| Design & motion | Reference sites, scroll techniques, stack, type system | `research/design_system_references.md` |
| KPI visualisation | Screen 06 in full | `research/kpi_dashboard_spec.md` **LANDED** |
| Marketing metrics | Screen 10 in full | `research/marketing_metrics_spec.md` **LANDED** |
| Fake-door forensics | Screen 08: every screen, event and field in the live app | `research/fakedoor_event_map.md` |
| Per-screen agents | One agent per remaining screen, once its spec is locked | the screen's own folder in `src/` |

## 4b. The build stack (locked — see `research/design_system_references.md`)

**GSAP 3.15.0 UMD (gsap + ScrollTrigger + Flip) + IntersectionObserver for media + native
`animation-timeline: view()` behind `@supports`.** Lenis optional, with a `?nosmooth=1` kill switch.
No build step, no framework, no ES modules (they break on `file://`). Everything vendored into
`src/vendor/` before demo day.

**The spine of the story is one pattern:** a sticky chart with captions scrolling past it, each caption
setting the chart to state *N* via one idempotent `renderChart(state)`. Three "wow" moments only:
the hero scroll-scrub, the scattered→sorted photos on screen 09, and one count-up wall.

**Type:** Instrument Serif (display, with italic for verbatims) + Inter Tight (UI) + JetBrains Mono (data).
**Palette:** ink `#1A1614` · cream `#FBF4EC` · coral `#FF4438` (fills) · brick `#B3261E` (text on cream) ·
deep teal `#0F6E6B` (the comparison series) · warm grey `#A79C92` (context). A mono-red palette cannot
encode two series — that is what the teal is for.

## 5. Rules that apply to every screen

1. **Every number names its instrument and its base.** No bare percentages.
2. **Charts are generated by Python**, as SVG, and animated in the page — never hand-typed numbers in HTML.
3. **Small bases are labelled**, not hidden: 30+ = fine, 10–29 = direction, under 10 = a count.
4. **One idea per screen.** If a screen needs a second idea, it is two screens.
5. **Nothing moves that did not move in reality.**
6. **It must survive a projector**: 1440×900, no dark mode, no dependency on hover to understand a chart.

## 6. Open items

- **Survey export.** Everything is currently built on **124 responses** (frozen 19 Sep). The live form
  reportedly shows 136. Share the sheet or drop a CSV in `data/` and every figure re-derives.
- **Fake-door live testing.** Driving the live app needs the Claude browser extension connected; it is
  not. The fake-door map is being produced by reading the deployed code instead.
- **Team headshots** for screen 00 do not exist yet.
