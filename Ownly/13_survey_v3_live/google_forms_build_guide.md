# Google Forms Build Guide — Survey v3 (LIVE)

**Owner: Person 1. Time: ~55 min build + 20 min pilot. Do it in one sitting.**
Source of truth for wording: `survey_questions.md`. Branch map: `survey_logic.md`.
**Do not share the link before written ethics approval.**

---

## 0. Before you start (2 min)
1. Sign into the **team** Google account, not a personal one.
2. Open `survey_questions.md` in a second window. **Copy-paste every string — do not retype.**
3. Fill the four brackets in the Section 1 description first: `[University name]`, `[team email]`,
   `[instructor name]`, `[date]`. A consent text with visible brackets fails ethics.

## 1. Create the form and set options (4 min)
1. forms.google.com → **Blank form**.
2. Title: **`Food delivery in your city — 7-minute student survey`**
3. Form description: leave blank (the consent text is Section 1's description).
4. **Settings** tab → *Responses*: Collect email addresses **OFF**; Limit to 1 response **OFF**.
5. **Settings** → *Presentation*: Show progress bar **ON**; Shuffle question order **OFF**.
6. **Settings** → *Presentation* → Confirmation message:
   `Thank you — your answers are anonymous. Please pass this on to anyone aged 20–30 who orders food delivery.`
7. Theme → header colour: anything neutral. **No Ownly or Rapido logo, name or colour anywhere on the form.**

## 2. Build the sections shell FIRST (10 min)

This is the step people get wrong. **Create all 17 sections empty, in this exact order, before adding any
question.** Forms' "Go to section" dropdown only lists sections that already exist.

Click the **"Add section"** icon (⊟, bottom of the right-hand toolbar) 16 times, then rename each by
clicking its title. Order and names, top to bottom:

| # | Section title |
|---|---|
| 1 | About this survey |
| 2 | Quick check |
| 3 | Quick check (2) |
| 4 | Quick check (3) |
| 5 | About you |
| 6 | Your last order |
| 7 | Your habits |
| 8 | Quick choices |
| 9 | Two services |
| 10 | One more thing |
| 11 | If you have used Ownly |
| 12 | If you have not used Ownly |
| 13 | Ownly in Bengaluru |
| 14 | Bengaluru — Ownly users |
| 15 | Bengaluru — never used Ownly |
| 16 | Other city |
| 17 | Last question |
| 18 | Not eligible |

> Sections 2, 3 and 4 are three separate pages holding **one screener question each**. Forms can only
> branch from the **last question on a page**, so age, orders and city each need their own page.

**Now set every section's default "After section" dropdown** (the grey bar at the bottom of each section).
Leave it on *Continue to next section* except:

| Section | After section →|
|---|---|
| 12 · If you have not used Ownly | **Go to section 17 (Last question)** |
| 11 · If you have used Ownly | **Go to section 17 (Last question)** |
| 14 · Bengaluru — Ownly users | **Go to section 17 (Last question)** |
| 15 · Bengaluru — never used Ownly | **Go to section 17 (Last question)** |
| 16 · Other city | **Go to section 17 (Last question)** |
| 10 · One more thing | *Continue to next section* (Q27 overrides per answer) |

## 3. Section 1 — consent (3 min)
1. Paste the consent paragraph into the **section description** (the grey line under the title).
2. Add question → **Multiple choice** → paste Q1 wording → options `Yes, I agree to take part` / `No`.
3. Toggle **Required ON**.
4. Three-dot menu (bottom-right of the question) → **Go to section based on answer**:
   - `Yes, I agree to take part` → **Continue to next section**
   - `No` → **Section 18 (Not eligible)**

## 4. Sections 2–4 — the screener (6 min)

| Section | Question | Branch rules to set (three-dot → Go to section based on answer) |
|---|---|---|
| 2 | Q2 `scr_age_band` | Under 20 → **18** · Over 30 → **18** · all others → Continue |
| 3 | Q3 `scr_orders_4wk` | None → **18** · all others → Continue |
| 4 | **Q4 `scr_city`** | Hyderabad → **Section 5** · Bengaluru → **Section 13** · Other city → **Section 16** |

**Q4 is the single most important click in the form. Check it twice.**

## 5. Sections 5–8 — the Hyderabad body (12 min)
Straight copy-paste, no branching. Watch these four settings:

| Where | Setting |
|---|---|
| Q9, Q10 | three-dot → **Response validation** → Number → *Between* → `0` and `10000` → error text `Please enter the amount in rupees, numbers only.` |
| Q14 | Question type **Multiple-choice grid**. Columns: Never, Rarely, Sometimes, Often, Very often. Rows: the 7 row texts in order. three-dot → **Require a response in each row ON**, **Shuffle row order ON** |
| Q15, Q35, Q52, Q43, Q56 | three-dot → **Shuffle option order ON** |
| Q15, Q35 | three-dot → **Response validation** → Checkbox → *Select at most* → `3` |
| Q16, Q17, Q18 | three-dot → **Shuffle option order ON** (so the cheap option isn't always second) |

## 6. Section 9 — Two services ★ (8 min)

This section decides the project's headline result. Build it carefully.

1. Paste the section description from `survey_questions.md` §7.
2. Add a **Title and description** block (the `Tt` icon) → Title `SERVICE P` → description = P's headline + 3 bullets.
3. Add a second **Title and description** block → Title `SERVICE Q` → description = Q's headline + 4 bullets.
4. Add Q20 (`prop_P_intent`), Q21 (`prop_Q_intent`), Q22 (`prop_forced_choice`), Q23, Q24.
5. **Q22: Shuffle option order ON.** (Q20 and Q21 keep their natural Definitely-not→Definitely order — never shuffle a scale.)
6. Q23 is the **only** optional question in this section.

**Formatting rule:** P and Q must *look* identical — same font size, same bullet style, same block type.
If you make P an image, make Q an image too, at the same width. Any visual difference becomes a confound
and invalidates the comparison.

**Before you build this section, check with Person 2 whether the pilot interviews changed Service Q's
bullets** (see `survey_questions.md` §7 warning). It is far cheaper to change now than after launch.

## 7. Section 10 — brand reveal (3 min)
1. Section description: the two lines revealing Ownly/Rapido.
2. Q25 `own_aware_aided` — three-dot → **Go to section based on answer**:
   `Yes, clearly` → Continue · `I think so` → Continue · **`No` → Section 17 (Last question)**
3. Q26 — no branching.
4. Q27 `own_tried` — three-dot → **Go to section based on answer**:
   `Yes` → **Section 11** · `No, but I've opened or browsed it` → **Section 12** · `No` → **Section 12**

> Q25 and Q27 both branch but sit on the same page. Forms applies the branch of the **last** question
> with a rule, so **Q25's "No" branch will not fire from this page**. Fix: put Q25 alone on its own page.
> **Add one more section between 10 and 11**, titled `Ownly` — Q25 stays in section 10, Q26 + Q27 move to
> the new page. Renumber the later sections in your head; the dropdown shows names, so go by name.

## 8. Sections 13–16 — Bengaluru and Other City (7 min)
- Section 13, Q41 `blr_own_tried` → three-dot → `Yes` → **Bengaluru — Ownly users**, `No` → **Bengaluru — never used Ownly**.
- Sections 14, 15, 16 already point to **Last question** from step 2.
- Q48, Q50 are optional. Everything else required.

## 9. Pilot — 20 minutes, 3 people, before any real sharing

Send the link to **3 people who are not on the team**: 1 Hyderabad student, 1 Hyderabad working
professional, 1 person who will pick "Other city". Ask each to **time themselves** and to say out loud
anything they had to re-read.

**Run these 6 test cases yourself in Preview (👁 icon) first — every one must land where stated:**

| # | Answers | Must land on |
|---|---|---|
| 1 | Consent **No** | Not eligible → Submit |
| 2 | Yes · **Under 20** | Not eligible |
| 3 | Yes · 23–25 · **None** in last 4 weeks | Not eligible |
| 4 | Yes · 23–25 · 4–7 · **Hyderabad** · … · aware **No** | jumps straight to Last question |
| 5 | Yes · 26–28 · 8–15 · **Hyderabad** · … · aware Yes · tried **Yes** | *If you have used Ownly*, then Last question |
| 6 | Yes · 20–22 · 1–3 · **Bengaluru** · tried **No** | *Bengaluru — never used Ownly*, then Last question |
| 7 | Yes · 29–30 · 16+ · **Other city** | Other city, then Last question |

**What to look for in the pilot (not just "did it work"):**
- Total time > 9 minutes → cut Q12 and Q24 in that order.
- Anyone asks what Service P and Service Q "are" → the section description isn't clear enough; do not
  change the bullets, change the description.
- Anyone answers Q10 (food-only amount) with the same number as Q9 → add `(before fees)` in bold.
- Anyone picks "I genuinely can't choose" on Q22 at pilot → fine, that option stays; it is real data.
- Check the response sheet: one row per pilot, all columns populated, grid columns readable.

**Then delete the pilot responses** (Responses tab → three-dot → *Delete all responses*) **and record in
`progress.md` that you did.** Do this before the first real share, never after.

## 10. Frozen after the first real response — do not edit

| Safe to change any time | **NEVER change once responses exist** |
|---|---|
| Typos in section *descriptions* | Any **answer option** text or order |
| Confirmation message | Any **question wording** |
| Theme colour | **Service P / Service Q copy** |
| Adding a new question **at the end** | Any **branch rule** |
| — | Required ↔ optional |
| — | Response validation limits |

Changing an option after responses exist silently merges two different questions into one column and
there is no way to tell them apart afterwards. If something is genuinely broken, **close the form, fix it,
and log the break point in `decisions.md`** so the two waves can be analysed separately.

## 11. Publish and hand over
1. **Send** → 🔗 link → **Shorten URL ON** → copy.
2. Paste the link into `_ops/task_board.md` and into `07_fake_door/prototype/index.html` → `CONFIG.SURVEY_URL`.
3. Responses tab → green Sheets icon → **Create new spreadsheet** → name it `ownly_v3_survey_responses`.
4. Share that sheet with all three team members (Editor).
5. At close: File → Download → **CSV** → save as `08_clean_data/raw/survey_v3_raw.csv`. **Never edit that file.**
