# Survey Distribution Plan

**Owner: all three.** Scripts: `04_interviews/outreach_scripts_v3.md`. Log: `survey_response_tracker.csv`.
**Nothing goes out before written ethics approval.**

## Targets
| Sample | Target | Why that number |
|---|---:|---|
| Hyderabad, in-catchment, 20–30 | **80–100** | The H₀ sample. Below ~60 the segment cuts stop meaning anything |
| — of which working professionals | **≥ 35** | The half that always under-fills. Watch it hourly |
| — of which students | ≥ 35 | Will over-fill on its own; cap the effort spent here |
| Bengaluru benchmark | **15–30** | Enough for counts. Never pooled into the Hyderabad test |
| Other city | opportunistic | Do not spend a minute recruiting these |

**Margin of error at n=80 is roughly ±11 points.** That is a directional, exploratory sample and every
slide says so. Getting to 100 does not make it representative — it makes the cuts less noisy.

## Channel plan
| # | Channel | Who | Expected | Script |
|---|---|---|---:|---|
| 1 | **Personal DMs, 15 each** | P1 P2 P3 | 25–30 | I |
| 2 | Hostel / PG / co-living groups | P2 | 20–30 | F (after J) |
| 3 | Classmates and course cohort | P1 | 20–25 | F / I |
| 4 | Office and intern colleagues in Gachibowli / Fin District / HITEC City | P3 | 15–20 | C / I |
| 5 | Apartment & society groups (Manikonda, Narsingi, Kondapur, Tellapur) | P2 | 10–15 | F (after J) |
| 6 | LinkedIn post | P3 | 10–15 | G |
| 7 | Alumni / seniors working in Hyderabad | P1 | 10 | I |
| 8 | **Friends in Bengaluru — the benchmark** | All | **15–30** | I, adapted |
| 9 | Instagram story | P2 | 5–10 | H |
| 10 | Fake-door thank-you page | — | 5–15 | automatic, tagged `src=fakedoor_A/B` |

## Rules
- **Ask a group admin before posting in any group you don't own.** Screenshot the permission.
- **Never post the survey in a group that received a poll**, and never post a poll in a survey group — see `_ops/decisions.md` D8.
- One post per group. One reminder at most, and only after 12+ hours.
- No incentives, no payment, no promises. We have no budget for them and an unpayable promise is an ethics problem.
- Never say the survey is by, for, or about Ownly. It is a university study of food-delivery choice.
- **Do not let any single campus exceed ~40% of the Hyderabad sample.** `meta_found_survey` is how we check.

## Quota watch — check at every report back
| Trigger | Do this |
|---|---|
| Professionals < 40% of Hyderabad responses | Stop student channels. Everyone works channels 4, 6 and 7 only |
| Bengaluru < 10 after the first wave | Each person personally messages 5 Bengaluru contacts. It will not happen passively |
| One campus > 40% of Hyderabad | Push channels 4, 5, 6, 7 hard; stop posting to that campus |
| Screen-out rate > 40% | Check where those people came from — a channel is reaching the wrong age or city |
| Median completion time > 9 min | Cut Q12 then Q24. Log the cut and the timestamp in `_ops/decisions.md` |

## Closing
- Close the form when the deadline requires, and record the exact close time in `_ops/progress.md`.
- Export: Responses → ⋮ → Download CSV → `08_clean_data/raw/survey_v3_raw.csv`. **Never edit that file.**
- Keep screen-outs in the export — they are the denominator of the recruitment funnel.
