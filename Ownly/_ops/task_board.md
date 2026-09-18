# task_board.md — WORK BLOCK 1 (2026-09-16, next 2–3 hours)

Update the Status column as you go. `→` means blocked on the thing named.

## Shared links — fill these in the moment they exist
| Thing | Link | Owner | Status |
|---|---|---|---|
| Ethics approval (written) | | P2 | ☐ |
| Google Form (live link) | | P1 | ☐ |
| Form response sheet | | P1 | ☐ |
| Fake-door page URL | | P3 | ☐ |
| Fake-door event sheet | | P3 | ☐ |
| Audit sheet (Google Sheets) | https://docs.google.com/spreadsheets/d/1JYRpagnFkq5KFvmpPPWop87dZ-yLqTPOVnV5Ekcz5Nk/edit | P3 | ✅ |

---

## PERSON 1 — Data / Research · *own the survey instrument*
| # | Task | Depends on | Output | Status |
|---|---|---|---|---|
| 1.1 | Build the Google Form, sections shell first | `13_survey_v3_live/google_forms_build_guide.md` §2 | Form exists, 18 sections | ☐ |
| 1.2 | Paste all questions, set validation / shuffle / grid | 1.1 | All Q1–Q59 in | ☐ |
| 1.3 | Set every branch rule; **Q4 city router twice** | 1.2 | Branching complete | ☐ |
| 1.4 | Hold Section 9 (Two services) copy | → P2 task 2.2 | Confirmed or revised bullets | ☐ |
| 1.5 | Run the 7 preview test cases | 1.3, 1.4 | All 7 land correctly | ☐ |
| 1.6 | Pilot with 3 non-team people, timed | 1.5 | 3 timings + wording notes | ☐ |
| 1.7 | Fix wording, **delete pilot responses**, link the response sheet | 1.6 | Clean sheet, 0 rows | ☐ |
| 1.8 | Publish link → `task_board.md` + send to P3 for the fake door | 1.7 | Live short link | ☐ |
| 1.9 | Send 15 personal DMs (script I) | 1.8 | 15 sent | ☐ |

## PERSON 2 — User Research · *own the respondents*
| # | Task | Depends on | Output | Status |
|---|---|---|---|---|
| 2.1 | **Chase ethics approval in writing. Do this first, now.** | — | Written approval or a stated ETA | ☐ |
| 2.2 | **2 pilot interviews** (1 student, 1 professional) using `RAPID_15min_guide_v3.md` + printed `proposition_card_v3.md` | 2.1 | 2 filled note templates + **the Card 2 rewrite answer** | ☐ |
| 2.3 | Send P1 the verdict on Service Q's bullets | 2.2 | "keep" or exact replacement text | ☐ |
| 2.4 | Book 6 more interviews into slots | 2.1 | 6 confirmed times in the tracker | ☐ |
| 2.5 | Get admin permission in 6 groups; split them into **poll groups** vs **survey groups** | 2.1 | 6 permissions, 2 named lists | ☐ |
| 2.6 | Post **Poll A (awareness) only** in one written-off group | 2.5 | Posted, logged in `poll_tracker.csv` | ☐ |
| 2.7 | Post the survey in **survey-list groups** (script F) | 2.5, 1.8 | Posted + logged | ☐ |
| 2.8 | Send 15 personal DMs (script I) | 1.8 | 15 sent | ☐ |

## PERSON 3 — Experiment / GTM · *own the observed evidence*
| # | Task | Depends on | Output | Status |
|---|---|---|---|---|
| 3.1 | **Ownly serviceability check at a Gachibowli address — 10 min, do this first** | — | 4 answers to Claude | ✅ Yes · both · **221 restaurants** · Toing live |
| 3.2 | Fill the 4 Group B restaurant names in `restaurant_frame_PREFILLED.csv` | 3.1 | 10 named restaurants | ✅ Murgan Tiffins · Aanimuthyualu · Mehfil · Karachi Bakery |
| 3.3 | Import `audit_captures_PREFILLED.csv` into Sheets, share with team | 3.2 | Live audit sheet | ✅ link above |
| 3.4 | Create the fake-door collector sheet + Apps Script, deploy, paste `/exec` into `CONFIG.ENDPOINT` | — | Collector alive | ✅ verified: GET returns `collector alive: hyd_vp_fakedoor_v1`; endpoint pasted; `PAGE_VERSION 2026-09-17.1` |
| 3.5 | Host the page (GitHub Pages or Netlify Drop), **neutral name** | 3.4 | Live URL | ☐ |
| 3.6 | Paste the survey link into `CONFIG.SURVEY_URL` | 3.5, 1.8 | Survey button live | ✅ `forms.gle/wAUBsGtwN5GjHPZaA` verified live (200, "How young India orders food: 6-minute survey") and pasted. Button carries `src=fakedoor_A` / `_B`. |
| 3.7 | Run the 10-point QA with `?qa=1` | 3.5 | 10/10 pass | ☐ **v3 rebuilt 2026-09-17** (D15): re-drag `gachibowli-food-study/`, check `?admin`, `?v=A`, `?v=B` — see `07_fake_door/FAKE_DOOR_v3_RUNBOOK.md` §8 |
| 3.8 | Post the fake-door link with per-channel UTMs; log each in `experiment_tracker.csv` | 3.7, 2.5 | ≥4 channels posted | ☐ **Now: ₹1,000 Meta ad, Sat 19 → Mon 21 Sep** (runbook §4), plus optional organic posts in the same window |
| 3.9 | **Audit slot 1 (`wed_dinner`), 19:30–21:30** — 30 captures + screenshots | 3.3 | 30 rows + 30 PNGs | 🟡 **37 priced rows · 4 full comparisons · coverage 9/10 on Ownly** — analysed in `audit_slot1_results.md`. Missing: Ownly prices for the local eateries (Murgan Tiffins, Mehfil) → do in `thu_lunch` |

## CLAUDE — done this block
| # | Task | Output | Status |
|---|---|---|---|
| C.1 | Read every project file; establish true state | This board | ✅ |
| C.2 | Consolidate all coded evidence into one exhibit | `01_secondary_research/consolidated/` + reproducible script | ✅ |
| C.3 | Rebuild the survey with canonical 3-city routing + paired proposition test | `13_survey_v3_live/` ×3 | ✅ |
| C.4 | Collapse the fake door 3 arms → 2, rewrite both variants, patch the HTML | `07_fake_door/` | ✅ |
| C.5 | Compress the interview kit to 15 min + proposition cards + trackers | `04_interviews/*_v3.*` | ✅ |
| C.6 | Pre-fill 60 audit rows + the restaurant frame + write the runsheet | `06_competitor_audit/` | ✅ |
| C.7 | Write poll copy, plan and tracker | `14_quick_polls/` | ✅ |
| C.8 | Stand up the seven tracking files | `_ops/` | ✅ |
| C.9 | **Pre-register the H₀ primacy rule before any data exists** | `decisions.md` D3 | ✅ |
| C.10 | Log every response verbatim to `../responses.md` for session recovery | `responses.md` | ✅ |
| C.11 | On your results: clean, compute, test, build charts, update all trackers, issue block 2 | — | ⏳ waiting |
