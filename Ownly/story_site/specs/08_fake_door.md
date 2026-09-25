# 08 · The fake door  ★ key screen

**Purpose:** show that we built a working food-delivery app that could not take an order, put 70 people
through it, and recorded what they *chose* rather than what they *said*.
**Owner:** fake-door forensics agent → `../research/fakedoor_event_map.md` — **LANDED**. That document is
the source of truth for this screen: the live app is a Next.js re-implementation with a full fake Rapido
ride simulator in front of the food flow, not the single-file prototype in `SUBMIT_EXPERIMENT/`.
Live build: https://fakedoorownly.netlify.app/app · session data: `07_fake_door/ownly_direct.xlsx`, `ownly_rapido.xlsx`

> **How to use this file.** It defines *what information the screen carries and how that information
> should be drawn* — not the final look. Visual styling is decided separately (see `../research/
> design_system_references.md`). Every fact below is already verified against a file in this repo;
> the source is named next to it. If a number has no source line, it is not allowed on screen.


## What the viewer leaves with
- What the app was, in 20 seconds, without clicking anything.
- Why a fake door was needed *in addition to* the survey.
- The three results the survey could never have produced.

## The auto-playing walkthrough (the centrepiece)
- Plays **on section entry**, no controls, ~20 seconds, loops.
- Built from real captured frames of the live app, not a mock-up.
- **Frame list is fixed: the 12 frames in `../research/fakedoor_event_map.md` §8** — it starts in the
  fake Rapido ride app (banner → destination → vehicle → captain → ride → ride-complete ad) and only
  then enters Ownly, because the Rapido handoff is half the experiment.
- Each frame carries a one-line caption and, where a question fired, a small tag showing the question.

## Why a fake door as well as a survey (state this explicitly on screen)
| The survey can | The fake door can |
|---|---|
| Ask what people would do | Watch what they do when a button is in front of them |
| Measure stated switching price | Randomise a real price and see take-up |
| Reach 124 people | Reach 70, but with revealed preference |

## Content inventory (verified; sources in `FINAL_STORY/data/`)
| Result | Number | File |
|---|---|---|
| Sessions | 70 (34 direct · 36 inside a ride app); 96 raw − 25 test rows − 1 duplicate | `evidence.csv` F0 |
| Funnel, direct | 34 → 25 → 18 → 18 → **16 placed (47.1%)** | `s8_fd_funnel.csv` |
| Funnel, inside Rapido | 36 → 33 → 26 → 24 → **13 placed (36.1%)** | `s8_fd_funnel.csv` |
| Entry points | food tab 8 of 14 · ride-end ad 4 of 16 · top banner 1 of 5 | `s8_fd_entry.csv` |
| Missing restaurant | 16 of 30 left for their usual app | `s6_fd_missing.csv` |
| Why that restaurant | 62.5% trust/loyalty · 12.5% price | `s6_fd_why_restaurant.csv` |
| Rapido Link ladder | ₹15 25% · ₹25 33.3% · ₹35 53.8% · ₹49 63.6% · overall 20 of 44 = 45.5% | `s8_fd_speed.csv` |
| Payment model | ₹15/order 26 of 42 (21 placed) · Order Protection 8 of 42 · ₹99/month 8 of 42 (3 placed) | `s8_fd_pay.csv` |
| Offer reasoning | 18 of 34 = 53% chose cash-now for "may not order again"/"don't trust later offers" | `s7_fd_offer_why.csv` |

**Corrections already applied** (the terminal screenshot circulating in the team is wrong on three):
₹49 take-up is **63.6%**, not 58%; Order Protection cover was randomised **₹9–39**, so there is no
"₹39 held steady" claim; the wallet was **₹120–250** randomised, so 35% is the whole-range rate.

## Visuals besides the walkthrough
1. **Two funnels side by side** — direct vs inside-Rapido, same five steps.
2. **The price ladder** — four columns rising with price, the opposite of what a demand curve should do.
3. **Payment models** — chose vs then-placed, paired bars.

## Motion
- Walkthrough autoplays; the funnels draw as the walkthrough finishes its loop.
- The ladder's fourth column overshoots slightly — the surprise is the point.

## Honesty rules
- "Placed" means the button was pressed. **No money changed hands.** Put it on the screen, not in a footnote.
- The A/B home-screen arms are **not reportable** (phones were shared; the split was 58 vs 12). Show both
  screens, claim no winner.
- Every price cell is under 15 people: show the shape, label the counts.

## Live-build facts that must appear on this screen
- **Two doors, not one:** a direct link, and three touchpoints inside a working fake ride app
  (top banner · Ownly tab · ride-complete ad). Live: 45 direct visits, 52 from Rapido.
- **Questions fire at the moment of choice**, as a bottom sheet, before the next screen paints — 12 of them.
- **Four randomised prices**, not one: the message arm, the Rapido Link fee (₹15–49), the wallet
  (₹120–250) and the cover (₹9–39).
- **The honest stop** is part of the product: "We can't place this order. Nothing was charged."

## Open items
- Live click-through testing needs the browser extension connected. The map was read from the deployed
  code instead. **Do not post test events to the live backend** — it would pollute the session table.
- The live table now holds **97 Ownly visits / 42 placed**, against the 96 rows in the two xlsx exports.
  Decide before building: present the frozen export, or re-export first.
- **The message A/B is not reportable** (71:26 split; `fd_variant` survives logout on a shared phone).
  Show both home screens, claim no winner.

## Acceptance
- [ ] Walkthrough plays automatically within 300ms of the section entering
- [ ] Both entry paths shown
- [ ] The three corrected numbers used everywhere
