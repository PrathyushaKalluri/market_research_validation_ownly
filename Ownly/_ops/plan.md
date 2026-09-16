# plan.md — current work plan

**Live from 2026-09-16.** Supersedes `../../plan.md` for execution. ⚠ **Deadline is open question Q1.**
The plan below is written so that Block 1 is correct either way — if the deadline is 17 Sep, Block 3
happens tomorrow morning; if the time box has reset, Block 3 gains a day and the survey stays open longer.

| WS | Task | Owner | Depends on | Status | Due | Output |
|---|---|---|---|---|---|---|
| **BLOCK 1 — go live (next 2–3 hours)** |
| Ethics | Written approval in hand | P2 | — | 🔴 | now | Approval message |
| Survey | Build form: shell → questions → branches | P1 | build guide | 🔴 | +60 min | Live form |
| Survey | Hold Section 9 for pilot verdict | P1 | 2.3 | 🔴 | +90 min | Confirmed copy |
| Survey | 7 preview cases + 3-person timed pilot | P1 | build | 🔴 | +90 min | Test log |
| Survey | Publish, link the response sheet, share the link | P1 | pilot | 🔴 | +2 h | Short link |
| Interviews | 2 pilot interviews + the Card 2 rewrite answer | P2 | ethics | 🔴 | +90 min | 2 note sheets |
| Interviews | Book 6 more into slots | P2 | ethics | 🔴 | +2 h | 6 confirmed times |
| Recruitment | 6 group permissions; poll list vs survey list | P2 | ethics | 🔴 | +2 h | 2 named lists |
| Polls | Post polls 1 and 2 in poll-list groups | P2 | permissions | 🔴 | +2.5 h | Logged rows |
| Audit | Serviceability check at DP1 | P3 | — | 🔴 | +15 min | 4 answers |
| Audit | Name 4 Group B restaurants; import the sheet | P3 | check | 🔴 | +45 min | Live audit sheet |
| Fake door | Collector + host + QA | P3 | — | 🔴 | +90 min | Live URL |
| Fake door | Post with per-channel UTMs | P3 | QA, permissions | 🔴 | +2.5 h | ≥4 channels |
| Distribution | 15 personal DMs each | P1 P2 P3 | live link | 🔴 | +3 h | 45 DMs |
| Audit | **Slot 1 `wed_dinner`, 19:30–21:30** | P3 +1 | sheet | 🔴 | tonight | 30 rows + 30 PNGs |
| **BLOCK 2 — collect (evening → next morning)** |
| Interviews | Interviews 3–8 | P2 | bookings | ⬜ | | 6 note sheets |
| Interviews | Code all 8 into the 8 theme families | P2 | interviews | ⬜ | | `coded_segments` |
| Survey | Reminder wave; watch the professional and Bengaluru quotas | All | launch | ⬜ | | Quota counts |
| Audit | Slot 2 `thu_lunch` | P3 | slot 1 | ⬜ | | 30 rows |
| Audit | 3 test orders (₹900) | P3 | budget + ethics | ⬜ | | 3 rows, promised vs actual |
| Fake door | Hold until the stopping rule fires. **No peeking at conversion by arm.** | P3 | launch | ⬜ | | — |
| Analysis | Illustrative bill on the landing page → audit medians | P3 | slot 1 | ⬜ | | Bumped page version |
| **BLOCK 3 — decide and build (Claude leads)** |
| Analysis | Clean to protocol; RAW / CLEANED / EXCLUDED | Claude + P1 | exports | ⬜ | | Cleaned CSVs |
| Analysis | H₀ test per the D3 primacy rule | Claude | cleaned | ⬜ | | Test output + CIs |
| Analysis | Audit metrics: savings %, win rate w/ and w/o coupons, fee share, ETA gap, coverage | Claude | audit CSV | ⬜ | | Metric tables |
| Analysis | KPI set + derived marketing metrics from the formula sheets | Claude | all | ⬜ | | `metric_dictionary` |
| Analysis | Segment cuts: student vs professional, Rapido vs not, trier vs not, heavy vs light | Claude | cleaned | ⬜ | | Segment tables |
| Synthesis | Triangulation: survey × audit × fake door × interviews, agreements **and** contradictions | Claude | all | ⬜ | | `findings.md` |
| Synthesis | Transferability matrix — KEEP / ADAPT / DROP on all six Bengaluru tactics | Claude + all | findings | ⬜ | | Decision matrix |
| Dashboard | KPI row + 5 charts, each with question / source / n / segment / interpretation / implication | Claude | metrics | ⬜ | | Dashboard |
| Deck | Storyline, H₀ verdict, recommendation, limitations | Claude + all | dashboard | ⬜ | | Final deck |
| QA | Every number traced to a source file; every claim labelled | All | deck | ⬜ | | Submission |

## Critical path
**Ethics approval → pilot interviews → Service Q copy confirmed → form published → distribution.**
Everything on the survey side waits on that chain. The audit and the fake-door build sit **off** it and
must run in parallel — that is why P3 starts immediately and independently.

## The three things most likely to sink this
1. **Ethics approval doesn't arrive.** → Everything involving people stops. The audit (no participants)
   and the desk analysis continue, and the fallback is the desk-based study named in the 14 Sep plan.
2. **Working-professional and Bengaluru quotas never fill.** Students over-fill on their own; these two
   do not. Check them at every report and redirect effort, don't discover it at the end.
3. **Fake-door traffic stays under 80.** → D3 already handles this: Section 7 becomes primary and the
   fake door is reported as directional. No improvisation needed at analysis time.
