# 00 · Opening

**Purpose:** establish that three real people did this work, and set the tone in under five seconds.
**Status:** blocked on assets (headshots).

> **How to use this file.** It defines *what information the screen carries and how that information
> should be drawn* — not the final look. Visual styling is decided separately (see `../research/
> design_system_references.md`). Every fact below is already verified against a file in this repo;
> the source is named next to it. If a number has no source line, it is not allowed on screen.


## What the viewer leaves with
- Three named researchers, a university project, a named company and city.
- The feeling that this is a designed piece of work, not a class submission.

## Content inventory
| Element | Exact content | Source |
|---|---|---|
| Headshot | The three of us together, shot straight-on, same light | TO SHOOT |
| Title | *Ownly in Gachibowli* | — |
| Subtitle | One line: what the study is. Draft: "Rapido built a food app with no commission and no platform fee. We spent three weeks finding out whether Hyderabad would use it." | — |
| Credits | Three names + roles (survey · audit · experiment) | `_ops/task_board.md` |
| Date | Field window 16–25 Sep 2026 | `final_dashboard/data/raw_manifest.csv` |

## Visuals
1. **Hero portrait**, full-bleed, desaturated slightly so the title holds contrast.
2. **Scroll cue** — a thin line that draws downward on loop.

## Motion
- Portrait scales from 1.06 → 1.00 over 1.2s on load; title words rise with a 60ms stagger.
- On scroll out: portrait parallaxes slower than the text (0.6 ratio) and the next screen's colour bleeds up.

## Assets needed
- `assets/team/headshot_group.jpg` — landscape, 3000px wide, shot at eye level.
- Optional: three individual cut-outs for the credits row.

## Acceptance
- [ ] Readable at 1440×900 with no scrolling
- [ ] Names spelled and ordered as the team agreed
- [ ] Loads in under 1.5s on 4G (portrait ≤ 400KB, AVIF/WebP)
