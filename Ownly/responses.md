# responses.md — Claude's responses log (Ownly Gachibowli project)

**Purpose:** a durable, copy-pasteable record of every operational response Claude (4th team member /
execution lead) has given on this project, so nothing is lost if the chat session is lost.

**How this file works**
- One `## RESPONSE N` block per response, newest at the bottom.
- Each block is reproduced **verbatim** as it was given in chat.
- The artefacts referenced in each response are real files in this repo — see the
  "Files created" table inside each block, and `_ops/file_manifest.md` for the full map.
- If you lose the chat: give Claude this file plus `claude_master_project_orchestrator_prompt.md`
  and `_ops/` (the seven tracking files), and it can resume with full continuity.

**Sharing with the team:** each response block is followed by a `📲 WHATSAPP SHARE BLOCKS` section —
plain-text messages, pre-chunked per person, ready to copy straight into WhatsApp.

**Project brain (always read these first on resume):**
`_ops/project_context.md` · `_ops/direction.md` · `_ops/plan.md` · `_ops/progress.md` ·
`_ops/decisions.md` · `_ops/open_questions.md` · `_ops/task_board.md`

---

# RESPONSE 1 — 2026-09-16 — IMMEDIATE WORK BLOCK (first block as execution lead)

**Context of the request:** Claude was asked to read all uploaded files (review_log.md,
claude_master_project_orchestrator_prompt.md, all Ownly research CSVs, audit templates, formula sheets,
evidence/review/social/listing files), act as the 4th team member and execution lead, and issue only the
immediate next 2–3 hour work block in execution order — doing everything itself that doesn't require a
human.

**Files created/patched in this response:** 31 artefacts. Full list in the table at the end of this block.

---

All 31 artifacts written and verified.

## IMMEDIATE WORK BLOCK

**First, the thing you need to know.** The project has a genuinely excellent research design and **zero primary data**. Last file change was Sep 14, 22:46. `08_clean_data/raw/` is empty. No survey responses, no audit captures, no interviews, no fake-door events. Two days gone against a 3-day plan. Design quality is not the constraint — nothing has been put in front of a human.

So this block does one thing: **get instruments live.** Everything that doesn't collect data today is deferred.

### Claude — what I will do

**Done in the last two hours** (31 files, all written and verified):

**1. Consolidated every coded dataset into one exhibit** — `01_secondary_research/consolidated/`. The strongest pre-fieldwork result you have:

| Theme | All public discussion (n=260) | People describing their **own** order (n=79) | App reviews (n=32) |
|---|---:|---:|---:|
| Price-doubt | **35%** | 16% | 0% |
| Price advantage | 16% | 28% | 16% |
| Fulfilment failure | 15% | **47%** | **72%** |
| Support/refund | 11% | **28%** | **72%** |

> **What people argue about is price. What people who actually ordered report is fulfilment.**

Reproducible via `rollup_themes.py`. Also: 74% of your secondary base is media report or company claim, only 24% verified, and **Hyderabad appears in 4 of 524 social items.** That gap is the project.

**2. Rebuilt the survey** with the canonical 3-city routing your brief mandates (the existing short survey was Hyderabad-only) — `13_survey_v3_live/`: branch map, all 59 questions with exact wording + variable names + KPI mapping, and a click-by-click Forms build guide with 7 preview test cases and post-launch freeze rules.

**3. Collapsed the fake door 3 arms → 2 and patched the HTML myself.** A = Bengaluru playbook, B = Hyderabad-localized. 3 arms on ~130 visitors gives 40 each and resolves nothing; 2 gives ~65 each. Version bumped, 3-arm original archived.

**4. Pre-registered the H₀ primacy rule — before any data exists** (`_ops/decisions.md` D3). Fake door ≥80 visitors with ≥30/arm → it's primary. Otherwise survey Section 7 is primary and the fake door is directional. Both always reported. Picking the primary test after seeing the p-values is how a student project fabricates a result.

**5. Compressed the interview kit to 15 min**, wrote the two proposition cards, notes template, tracker, 10 outreach scripts, ranked recruitment sources.

**6. Pre-filled 60 audit rows** — slot, platform, restaurant, basket and screenshot filename already filled. Person 3 types numbers only.

**7. Wrote 3 WhatsApp polls** with exact copy and a contamination rule.

**8. Stood up all seven tracking files** in `_ops/`.

**Next, when you report back:** clean to protocol, run the H₀ test, compute every audit metric and KPI, build the charts and the transferability matrix, update all trackers, issue block 2.

---

### Person 1 — Data / Research (owns the survey instrument)

Open `13_survey_v3_live/google_forms_build_guide.md` and work top to bottom.

#### Task 1.1 — Build the sections shell FIRST (10 min)
Create all 18 sections **empty** before adding any question. Forms' "Go to section" dropdown only lists sections that already exist — build questions first and you'll rebuild the whole thing. Names are in §2 of the guide.

#### Task 1.2 — Paste every question (25 min)
Copy-paste from `survey_questions.md`, never retype. Watch four settings: number validation on Q9/Q10, the 7-row grid on Q14, shuffle-on for Q15/Q16/Q17/Q18/Q22/Q35, "select at most 3" on Q15/Q35.

#### Task 1.3 — Set every branch rule (10 min)
**Q4 (city router) is the single most important click in the form. Check it twice.** Hyderabad → S5, Bengaluru → S13, Other → S16. Also note the guide's §7 warning: Q25 needs its own page or its branch won't fire.

#### Task 1.4 — HOLD Section 9 ⛔
Do not finalise Service P / Service Q copy until Person 2 sends the pilot verdict. Build everything else around it.

#### Task 1.5 — Run the 7 preview test cases (10 min)
Listed in §9. All 7 must land where stated.

#### Task 1.6 — Pilot with 3 non-team people, timed (20 min)
1 Hyderabad student, 1 professional, 1 "other city". If median >9 min, cut Q12 then Q24.

#### Task 1.7 — Fix, **delete pilot responses**, link the response sheet
Delete them before the first real share, never after.

#### Task 1.8 — Publish, paste the link into `_ops/task_board.md`, send to Person 3

#### Task 1.9 — 15 personal DMs (script I)

**Produces:** live form link · response sheet link · 7-case test log · 3 pilot timings · wording changes made.

---

### Person 2 — User Research (owns the respondents)

#### Task 2.1 — Chase written ethics approval. Right now, before anything else. ⛔
This blocks every human-facing task on this page. If it hasn't arrived, get a stated ETA.

#### Task 2.2 — Two pilot interviews (45 min) ⛔ **critical path**
`04_interviews/RAPID_15min_guide_v3.md`. Print `proposition_card_v3.md` (two sides). One student, one working professional. Card 1 first for interview 1, Card 2 first for interview 2.

**The question that matters most is §4 Q14: "which line on that card made you pick it?"** — write it verbatim. And for these two only, also ask: *"If you were writing the second card for someone in Hyderabad, what would you put on it that isn't there?"*

#### Task 2.3 — Send Person 1 the Service Q verdict ⛔
Either "keep as written" or the exact replacement text. Person 1 is blocked until this lands. Service Q's bullets are v0 desk-derived; your brief requires them to come from interviews. Cash-on-delivery and meal cards are the live candidates from the social data.

#### Task 2.4 — Book 6 more interviews into actual time slots
Quota: 4 students, 4 professionals. **Professionals are the bottleneck — they schedule days out. Ask now.**

#### Task 2.5 — Get admin permission in 6 groups, then split them into two named lists ⛔
**Poll groups** and **survey groups** must be disjoint. Someone who just voted in Poll 1 answers Section 7 differently, and Poll 2 names Ownly, which destroys the brand-blind sequencing.

#### Task 2.6 — Post Polls 1 and 2 in poll-list groups only
`14_quick_polls/exact_poll_copy.md`, verbatim. Log in `poll_tracker.csv` at post time.

#### Task 2.7 — Post the survey in survey-list groups (script F)

#### Task 2.8 — 15 personal DMs (script I)

**Produces:** 2 interview note sheets · the Service Q verdict · 6 booked slots · 2 named group lists · poll vote counts.

---

### Person 3 — Experiment / GTM (owns the observed evidence)

You start immediately and independently — nothing you do waits on ethics or interviews.

#### Task 3.1 — Ownly serviceability check. 10 minutes. Do it now. ⛔
Open Ownly (standalone **and** inside Rapido) with a real Gachibowli address. Send me four answers: does it deliver? standalone/in-Rapido/both? how many restaurants? is Toing live?

**If Ownly doesn't serve Gachibowli, that's a headline finding, not a failure.** Audit the nearest served area and say so.

#### Task 3.2 — Name the 4 Group B restaurants
`restaurant_frame_PREFILLED.csv` has 6 named. Fill 4 local tiffin/meals places from what Ownly actually lists — that's the segment Ownly *says* it targets, versus the chains it *showcases*. Testing both is the point.

#### Task 3.3 — Import `audit_captures_PREFILLED.csv` into Sheets, share with the team
60 rows already structured. You only type numbers.

#### Task 3.4 — Fake-door collector (Apps Script + Sheet), paste `/exec` into `CONFIG.ENDPOINT`
`deploy_instructions.md` §2.

#### Task 3.5 — Host the page. **Neutral site name** — nothing with "ownly" or "rapido" in it.

#### Task 3.6 — Paste the survey link into `CONFIG.SURVEY_URL`

#### Task 3.7 — 10-point QA with `?qa=1`
Check 3 hardest: A and B pixel-identical apart from headline/subhead/bullets · disclosure fires first after CTA · no Ownly/Rapido anywhere.

#### Task 3.8 — Post with per-channel UTMs, log each in `experiment_tracker.csv`
One neutral post text everywhere. Variant never in the link.

#### Task 3.9 — Audit slot 1 (`wed_dinner`), 19:30–21:30 — 30 captures
All 3 apps within 10 minutes of each other. **Coupon auto-applies → capture a second row with it removed.** Delivery fee exactly as shown. Screenshots named per the pre-filled column. Plus the coverage count: of 10 restaurants you'd normally order from, how many are missing on Ownly.

**Produces:** 4 serviceability answers · live fake-door URL · live audit sheet · 30 rows + 30 PNGs · coverage count.

---

### Parallel work

Three independent tracks, only one dependency between them:

- **P3 runs fully parallel from minute zero** — the audit and fake-door build need no ethics approval and no interview input. This is deliberate: it keeps the observed-evidence stream alive even if the ethics chain stalls.
- **P2's ethics chase and P1's form shell run in parallel** — P1 can build 95% of the form before Service Q is settled.
- **Polls (P2) and fake-door posting (P3) run parallel** on disjoint channels.
- **All three distribute** once the link is live.
- The only true serialisation: **pilot interviews → Service Q copy → form publish → distribution.**

### Dependencies

| Blocked | Waits on | Why |
|---|---|---|
| Everything involving people | Written ethics approval (P2) | Hard rule |
| P1 task 1.4 (Section 9 copy) | P2 task 2.3 (pilot verdict) | Service Q is v0; your brief requires interview-derived copy |
| P1 1.5–1.8 | 1.4 | Can't test branches through an unfinished section |
| P3 3.6 (survey button) | P1 1.8 (live link) | Non-blocking — deploy without it, paste later |
| P2 2.6/2.7 (posting) | P2 2.5 (two group lists) | Contamination rule |
| P3 3.2 onwards | P3 3.1 (serviceability) | The frame depends on what's actually listed |
| Audit metrics | Slot 1 complete | Also unblocks replacing the landing page's placeholder bill |

### What we must send back to Claude

Use `_ops/report_back_template.md` — copy it, fill it, paste it back. **Send it even if half is blank.** A half-filled report tells me what to re-plan; silence costs us the next block.

The nine highest-value fields:
1. **The deadline** — still Sep 17, or has the 3-day box reset?
2. Ethics approved, yes/no, in writing
3. The 4 serviceability answers
4. **The Service Q verdict** — keep, or exact replacement text
5. Card 1 vs Card 2 counts from the 2 interviews, plus the two best "why did you pick it" verbatims
6. Response counts split: Hyderabad / Bengaluru / Other, and students vs professionals
7. First three matched price comparisons: Ownly / Swiggy / Zomato final payable
8. Of 10 restaurants, how many listed on Ownly + the coverage count
9. Poll 1 vote split

**Do not send me fake-door conversion by arm before the stopping rule fires.** Peeking and stopping on a good-looking split turns a null result into a fake positive.

### Completion criteria

This block is done when all seven are true:

1. ☐ Written ethics approval in hand, or a stated ETA
2. ☐ Google Form **live**, all 7 preview cases passing, piloted with 3 people, pilot responses deleted
3. ☐ Two pilot interviews complete and Service Q's copy confirmed or revised
4. ☐ Fake-door page live, QA 10/10, posted to ≥4 channels
5. ☐ Survey posted to ≥4 channels + 45 personal DMs sent
6. ☐ Audit slot 1 complete — 30 rows, 30 screenshots, coverage count recorded
7. ☐ Polls 1 and 2 posted in poll-list groups, logged

**Minimum viable version if you're short on time:** items 1, 2, 3, 6. A live survey plus one audit slot keeps the project alive. Everything else can slip a block.

### Do not do yet

- **Any more secondary research, scraping or Reddit mining.** You have 68 claims, 37 reviews and 524 social items — and 4 of them mention Hyderabad. The marginal row is worth roughly nothing.
- **Any dashboard or deck work.** No data exists to put in it. The blueprint and the draft deck are already built and waiting.
- **Test orders (₹900).** Slot 1 first — it may change which restaurant you order from.
- **Looking at fake-door results by variant.** Stopping rule only.
- **Analysis, cleaning, or statistics.** Mine, and I need the exports first.
- **Replacing the landing page's illustrative bill.** Needs audit medians — after slot 1.
- **Chasing Other City respondents.** Take them if they arrive, spend zero minutes recruiting them.
- **Building the `ownly_hyd_market_validation/` tree from the brief.** I deliberately didn't (`decisions.md` D7) — it would create two of everything one day before a deadline and break every relative path in the analysis pipeline. `_ops/file_manifest.md` maps the brief's structure to where each thing actually lives.

---

**One open question, and it doesn't block you** (`_ops/open_questions.md` Q1): **is the deadline still Sep 17, or did the new 3-day time box reset it?** This work block is correct either way — collect data now regardless. It only changes whether tomorrow is analysis day or day 2 of fieldwork, and how long the survey stays open. Answer it in your first report back.

---

---

# 📲 WHATSAPP SHARE BLOCKS — Response 1

**How to use:** each block below is plain text, formatted for WhatsApp (`*bold*` renders as bold there).
Copy everything between the lines and paste straight into the chat. No tables, no markdown — it will
render correctly on a phone. Send MSG 0 to the group, then MSG 1/2/3 to each person individually.

---

## MSG 0 — to the group (send first)

```
*OWNLY PROJECT — WORK BLOCK 1* 🚨

Status check: we have a great research design and *ZERO primary data*. Nothing has moved since Sun 14 Sep. No survey responses, no interviews, no price audit, no landing page traffic.

Design isn't the problem. Nothing has been put in front of a human yet.

So this block does ONE thing: *get the instruments live today.*

Everything is already built and waiting in the project folder:
• Survey - every question written, click-by-click Google Forms guide
• Interview guide - 15 min version + the 2 cards to print
• Price audit - 60 rows already pre-filled, you only type numbers
• Landing page A/B - ready to host
• 3 WhatsApp polls - exact wording written

Your individual task list is coming in a separate message.

*The one thing that blocks everything:* written ethics approval. P2 is chasing it now.

*What I need back from everyone:* fill the report template in _ops/report_back_template.md and paste it back. Send it even if half of it is blank.

Also - is the deadline still 17 Sep, or has it moved? Please confirm.
```

---

## MSG 1 — to PERSON 1 (Data / Research — owns the survey)

```
*PERSON 1 - YOUR TASKS (next 2-3 hrs)* 📊

Open: 13_survey_v3_live/google_forms_build_guide.md
Work top to bottom. Everything is written - copy paste, don't retype.

*1.1 Build the 18 sections EMPTY first (10 min)*
Create all sections before adding any question. Google Forms' "go to section" dropdown only shows sections that already exist. Build questions first and you'll redo the whole form. Section names are in §2.

*1.2 Paste every question (25 min)*
4 settings to watch:
• Q9, Q10 - number validation 0 to 10000
• Q14 - multiple choice GRID, 7 rows, shuffle rows ON
• Q15 Q16 Q17 Q18 Q22 Q35 - shuffle options ON
• Q15, Q35 - "select at most 3"

*1.3 Set the branch rules (10 min)*
⚠️ *Q4 (the city question) is the most important click in the form. Check it twice.*
Hyderabad → Section 5
Bengaluru → Section 13
Other city → Section 16
Also read §7 - Q25 needs its own page or its branch won't work.

*1.4 ⛔ HOLD Section 9 (the two services)*
Don't finalise that copy until P2 sends the pilot interview verdict. Build everything else around it.

*1.5 Run the 7 preview test cases (10 min)*
Listed in §9. All 7 must land where stated.

*1.6 Pilot with 3 people who aren't on the team (20 min)*
1 Hyd student, 1 working professional, 1 "other city". Time them. If median is over 9 min, cut Q12 then Q24.

*1.7 Fix wording, DELETE the pilot responses, link the response sheet*
Delete them before the first real share, never after.

*1.8 Publish. Send the link to the group + to P3.*

*1.9 Send 15 personal DMs* (script I in outreach_scripts_v3.md)

*Send back:* form link, response sheet link, which of the 7 tests passed, the 3 pilot timings, any wording you changed.
```

---

## MSG 2 — to PERSON 2 (User Research — owns the respondents)

```
*PERSON 2 - YOUR TASKS (next 2-3 hrs)* 🎤

*2.1 ⛔ CHASE THE ETHICS APPROVAL. Right now, before anything else.*
In writing. This blocks every human-facing task in the project. If it hasn't come, get a stated ETA.

*2.2 ⛔ TWO PILOT INTERVIEWS (45 min) - this is the critical path*
Guide: 04_interviews/RAPID_15min_guide_v3.md
Print: 04_interviews/proposition_card_v3.md (2 sides)
One student, one working professional.
Show Card 1 first in interview 1, Card 2 first in interview 2.

⭐ The single most important question is §4 Q14:
"Which line on that card made you pick it?"
*Write their answer word for word.*

And for these 2 interviews only, also ask:
"If you were writing the second card for someone in Hyderabad, what would you put on it that isn't there?"

*2.3 ⛔ Send P1 the Service Q verdict*
Either "keep as written" or the exact replacement wording. *P1 is blocked until this lands.*
Service Q's bullets are currently based on desk research. Our brief says they must come from interviews. Watch out for cash-on-delivery and meal cards - those came up in the social data.

*2.4 Book 6 more interviews into actual time slots*
Quota: 4 students, 4 working professionals.
⚠️ Professionals are the bottleneck - they schedule days ahead. Ask NOW.

*2.5 ⛔ Get admin permission in 6 groups, then split them into 2 written lists*
POLL groups and SURVEY groups must be completely separate.
Why: someone who just voted in Poll 1 will answer the survey differently. And Poll 2 says the word "Ownly", which ruins the blind test.

*2.6 Post Polls 1 and 2 - in POLL groups only*
Exact wording: 14_quick_polls/exact_poll_copy.md. Don't reword it. Log in poll_tracker.csv as you post.

*2.7 Post the survey in SURVEY groups* (script F)

*2.8 Send 15 personal DMs* (script I)

*Send back:* 2 interview notes, the Service Q verdict, 6 booked slots, your 2 group lists, poll vote counts.
```

---

## MSG 3 — to PERSON 3 (Experiment / GTM — owns the observed evidence)

```
*PERSON 3 - YOUR TASKS (next 2-3 hrs)* 📱

You start immediately. *Nothing you do waits on ethics or interviews.*

*3.1 ⛔ OWNLY SERVICEABILITY CHECK - 10 minutes, do this first*
Open Ownly (both the standalone app AND the food section inside Rapido) with a real Gachibowli address.
Send me 4 answers:
1. Does Ownly deliver there? Y/N
2. Is it standalone, inside Rapido, or both?
3. How many restaurants does it show?
4. Is Toing (Swiggy's budget app) live there? Y/N

⚠️ If Ownly does NOT serve Gachibowli, that's a *headline finding*, not a failure. Then audit the nearest area it does serve (Madhapur/Kondapur) and we say so openly.

*3.2 Name the 4 "Group B" restaurants*
File: 06_competitor_audit/restaurant_frame_PREFILLED.csv - 6 are already named, you fill 4.
Pick local tiffin / meals places that Ownly actually lists. That's the segment Ownly SAYS it targets, vs the big chains it SHOWCASES. Testing both is the whole point.

*3.3 Import audit_captures_PREFILLED.csv into Google Sheets, share with the team*
60 rows already structured - slot, platform, restaurant, basket, screenshot filename all pre-filled. *You only type numbers.*

*3.4 Build the landing page collector* (Apps Script + Sheet), paste the /exec URL into CONFIG.ENDPOINT
See 07_fake_door/deploy_instructions.md §2

*3.5 Host the page* - GitHub Pages or Netlify Drop
⚠️ *Neutral site name.* Nothing with "ownly" or "rapido" in the URL.

*3.6 Paste the survey link into CONFIG.SURVEY_URL* (once P1 sends it)

*3.7 Run the 10-point QA with ?qa=1*
The 3 that matter most:
• A and B look identical apart from the headline and 3 bullets
• The disclosure shows immediately after the CTA
• No Ownly/Rapido name or logo anywhere

*3.8 Post the link with a UTM per channel*, log each one in experiment_tracker.csv
Same neutral post text everywhere. The variant is never in the link.

*3.9 AUDIT SLOT 1 tonight, 19:30-21:30 - 30 captures*
Rules that make the numbers defensible:
• All 3 apps within 10 minutes of each other
• Same address every time (call it DP1, keep the real address out of the sheet)
• *If a coupon auto-applies, take a 2nd row with the coupon removed*
• Type the delivery fee exactly as shown - if it says FREE, enter 0 and note it
• Stop at checkout. Never place an order.
• Screenshot everything, names are already in the sheet
• Count: of 10 restaurants you'd normally order from, how many are MISSING on Ownly?

*Send back:* the 4 serviceability answers, live page URL, audit sheet link, 30 rows + screenshots, the coverage count.
```

---

## MSG 4 — to the group (dependencies + what to send back)

```
*WHO'S WAITING ON WHOM* ⛓️

Only one real dependency chain:
P2's ethics approval → P2's 2 pilot interviews → Service Q wording → P1 publishes the form → everyone distributes

*P3 runs completely in parallel from minute zero.* The price audit and the landing page need no ethics approval and no interview input. That's deliberate - it keeps one evidence stream alive even if ethics stalls.

Other blocks:
• P1 can build 95% of the form before Service Q is settled
• P3 can deploy the page before the survey link exists - paste it in later
• P2 can't post anything until the 2 group lists are written
• P3 can't pick restaurants until the serviceability check is done

*WHAT TO SEND BACK*
Use _ops/report_back_template.md - copy, fill, paste back. *Send it even if half is blank.* A half-filled report tells me what to re-plan. Silence costs us the next block.

The 9 things I need most:
1. The deadline - still 17 Sep or reset?
2. Ethics approved Y/N, in writing
3. The 4 serviceability answers
4. The Service Q verdict - keep or replace
5. Card 1 vs Card 2 counts + the 2 best "why did you pick it" quotes
6. Response counts: Hyderabad / Bengaluru / Other, students vs professionals
7. First 3 price comparisons - Ownly / Swiggy / Zomato final amount
8. How many of the 10 restaurants are on Ownly + the coverage count
9. Poll 1 vote split

⚠️ *Do NOT send me landing page conversion by variant before the stopping rule fires.* Looking early and stopping on a good-looking split is how a real result turns into a fake one.
```

---

## MSG 5 — to the group (done criteria + what NOT to do)

```
*WHEN IS THIS BLOCK DONE* ✅

All 7 true:
1. Ethics approval in writing (or a stated ETA)
2. Google Form LIVE, 7 preview tests passing, piloted with 3 people, pilot responses deleted
3. 2 pilot interviews done + Service Q wording confirmed
4. Landing page live, QA 10/10, posted to 4+ channels
5. Survey posted to 4+ channels + 45 personal DMs sent
6. Audit slot 1 done - 30 rows, 30 screenshots, coverage count
7. Polls 1 and 2 posted and logged

*If you're short on time, the minimum is 1, 2, 3 and 6.* A live survey plus one audit slot keeps the project alive. The rest can slip a block.

*DO NOT DO ANY OF THIS YET* 🛑

❌ More secondary research, scraping or Reddit. We have 68 claims, 37 reviews, 524 social posts - and only 4 of them even mention Hyderabad. Another row is worth nothing.
❌ Dashboard or deck work. There's no data to put in it. Both are already built and waiting.
❌ The 3 test orders (Rs 900). Do audit slot 1 first - it may change which restaurant you order from.
❌ Looking at landing page results by variant. Stopping rule only.
❌ Any analysis, cleaning or stats. That's mine - I need your exports first.
❌ Updating the illustrative bill on the landing page. Needs audit medians, so after slot 1.
❌ Chasing "other city" survey respondents. Take them if they arrive, spend zero minutes recruiting them.

*One open question that does NOT block you:* is the deadline still 17 Sep, or has the 3-day clock reset? Today's work is the same either way - collect data now. It only changes whether tomorrow is analysis day or a second fieldwork day. Answer it in your first report back.
```

---

## Files created / patched in Response 1 (31 artefacts, all verified)

| Lines | File | Owner / purpose |
|---:|---|---|
| 86 | `_ops/project_context.md` | Stable facts, H₀, frozen Bengaluru playbook, city roles, standing rules |
| 52 | `_ops/direction.md` | What we solve / don't solve / decision sought / why this step exists |
| 56 | `_ops/plan.md` | Block 1–3 workplan, critical path, 3 risks |
| 65 | `_ops/progress.md` | State assessment + this block's output + counts |
| 151 | `_ops/decisions.md` | **D1–D8**, incl. D3 pre-registered H₀ primacy rule |
| 17 | `_ops/open_questions.md` | Q1–Q10, owners, status |
| 67 | `_ops/task_board.md` | Per-person task grid with dependencies + shared-links table |
| 68 | `_ops/file_manifest.md` | Brief's folder spec → actual locations; source files never overwritten |
| 68 | `_ops/report_back_template.md` | **The fill-in-and-paste-back form** |
| 107 | `01_secondary_research/consolidated/consolidated_evidence_pack.md` | The one secondary exhibit + source-quality audit |
| 52 | `01_secondary_research/consolidated/rollup_themes.py` | Reproduces the exhibit (stdlib only) |
| 88 | `13_survey_v3_live/survey_logic.md` | Branch map, burden table, H₀ primacy rule |
| 353 | `13_survey_v3_live/survey_questions.md` | All 59 questions, exact wording, variables, KPI map, cuts justified |
| 183 | `13_survey_v3_live/google_forms_build_guide.md` | **P1 executes** — click-by-click, 7 test cases, freeze rules |
| 52 | `13_survey_v3_live/survey_distribution_plan.md` | Channels, quotas, quota-watch triggers |
| 1 | `13_survey_v3_live/survey_response_tracker.csv` | Running counts by channel/quota |
| 94 | `07_fake_door/AB_LAUNCH_RUNSHEET_v2.md` | **P3 executes** — 2-arm launch, QA, stopping rule, reading rule |
| 1 | `07_fake_door/experiment_tracker.csv` | Channel register |
| 676 | `07_fake_door/prototype/index.html` | **Patched to 2 arms**, v `2026-09-16.1` |
| 687 | `07_fake_door/prototype/index_v1_3arm_ARCHIVE.html` | 3-arm original, preserved |
| 102 | `04_interviews/RAPID_15min_guide_v3.md` | **P2 executes** — 15-min behavioural guide |
| 32 | `04_interviews/proposition_card_v3.md` | The two cards to print |
| 49 | `04_interviews/interview_notes_v3_template.md` | Note template |
| 1 | `04_interviews/participant_tracker_v3.csv` | Participant log |
| 90 | `04_interviews/outreach_scripts_v3.md` | 10 scripts + ranked recruitment sources + quotas |
| 116 | `06_competitor_audit/AUDIT_RUNSHEET_v3.md` | **P3 executes** — day-0 check, frame, capture rules, metrics |
| 61 | `06_competitor_audit/audit_captures_PREFILLED.csv` | **60 rows pre-filled — type numbers only** |
| 11 | `06_competitor_audit/restaurant_frame_PREFILLED.csv` | 10 restaurants, 6 named, 4 to fill |
| 84 | `14_quick_polls/exact_poll_copy.md` | **P2 executes** — 3 polls verbatim + contamination rule |
| 14 | `14_quick_polls/poll_plan.md` | Purpose, sample goals, reporting rule |
| 1 | `14_quick_polls/poll_tracker.csv` | Poll log |

**Also patched:** supersession banners added to `../plan.md`, `../progress.md`, `../decisions.md`,
`../context.md` and `03_hyderabad_survey/SHORT_survey_7min_google_form.md`.

## Key decisions locked in Response 1 (full reasoning in `_ops/decisions.md`)

| ID | Decision |
|---|---|
| **D1** | Fake door reinstated (dropped 14 Sep) and becomes the primary H₀ instrument — build cost is now zero, it was already fully built |
| **D2** | Fake-door arms 3 → 2: `A_blr_total_price` vs `B_hyd_local_reliable`. 3 arms on ~130 visitors resolves nothing |
| **D3** | **H₀ primacy rule pre-registered before any data.** ≥80 visitors & ≥30/arm → fake door primary; else survey Section 7 primary, fake door directional. Both always shown; disagreement is itself the finding |
| **D4** | Survey rebuilt with canonical 3-city routing (Hyderabad deep / Bengaluru benchmark / Other short). Bengaluru never pooled into the Hyderabad H₀ |
| **D5** | Section 7 is **within-subject** (both propositions, forced choice primary, McNemar secondary). Order effect declared on the slide, not hidden; fake door is the randomised counterpart |
| **D6** | Service Q copy is **v0 and provisional** until pilot interviews 1–2 land. Real dependency, not a formality |
| **D7** | **No duplicate `ownly_hyd_market_validation/` tree created** — would break every relative path one day before deadline. Brief's structure satisfied in substance via `file_manifest.md` |
| **D8** | Polls and survey never share a group (priming + brand-blind contamination) |

## Standing instruction for future blocks

Every time the team returns with results, Claude updates `project_context.md`, `direction.md`, `plan.md`,
`progress.md`, `decisions.md`, `open_questions.md` and `task_board.md`, appends the new response to this
file as `## RESPONSE N`, and issues the next work block only.

---
