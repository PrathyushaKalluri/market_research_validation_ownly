> **Superseded for the live page on 2026-09-17 (D15):** the page now runs the v3 arms. See `FAKE_DOOR_v3_RUNBOOK.md`. This file documents v2.

# Fake-Door A/B — Launch Runsheet (2-arm, v2)

**Owner: Person 3. Time: ~45 min. Cost: ₹0.**
Supersedes the 3-arm design in `experiment_plan.md` §4. Mechanics, QA and export are unchanged —
follow `deploy_instructions.md` for steps 2–6, with the differences below.

## What changed today and why

| | Was (v1) | Now (v2) |
|---|---|---|
| Arms | 3 (A total price · B transparent bill · C reliable value) | **2** |
| A | `A_total_price` | **`A_blr_total_price`** — the Bengaluru playbook: smaller final bill, restaurant's own menu prices, one flat fee |
| B | `B_transparent_bill` | **`B_hyd_local_reliable`** — the Hyderabad-localized alternative: local regulars, honest ETA, clear answer when it goes wrong, fair visible price |
| C | `C_reliable_value` | **removed** (its reliability idea is now inside B) |
| Page version | `2026-09-14.1` | **`2026-09-16.1`** |

**Why 2 arms, not 3:** the primary H₀ is *Bengaluru-style vs Hyderabad-localized*. Three arms split a
small traffic pool three ways; with a realistic 100–150 visitors, 3 arms give ~40 each and no test can
resolve anything. Two arms give ~55–75 each, which is the minimum where a 15-point difference is
detectable. A vs B now maps **exactly** onto the hypothesis instead of approximately onto three of them.
Logged in `_ops/decisions.md`.

**The page stays unbranded.** No Ownly or Rapido name, mark or colour, and the disclosure fires
immediately after the CTA. This is a research concept page, not an Ownly page. That decision is unchanged.

## Pre-launch, in order

1. `prototype/index.html` is already patched to 2 arms — **do not re-edit the COPY block.**
2. **Illustrative bill:** the table at line ~264 still holds placeholder numbers. If the Tuesday audit is
   done, replace them with audit medians and note it here. **If the audit shows no consistent Ownly
   advantage, delete the "Difference in this example" row rather than print a number the market
   doesn't support.** The bill is identical on both arms either way, so it cannot bias A vs B.
3. Create the collector: `deploy_instructions.md` §2. Paste the `/exec` URL into `CONFIG.ENDPOINT`.
4. Paste the live Google Form link into `CONFIG.SURVEY_URL` (this turns the fake door into a survey
   recruitment channel — every clicker is offered the survey, tagged `src=fakedoor_A` / `_B`).
5. Host it: `deploy_instructions.md` §3. **Neutral repo/site name** — nothing containing "ownly" or "rapido".

## QA — 10 minutes, all with `?qa=1` so the rows are excluded

| # | Check | ✓ |
|---|---|---|
| 1 | `?qa=1&v=A` shows "Same dinner. Smaller final bill." | ☐ |
| 2 | `?qa=1&v=B` shows "Your Hyderabad regulars, and dinner that actually turns up." | ☐ |
| 3 | **Everything else is pixel-identical between A and B** — same bill table, same CTA text and position, same footer | ☐ |
| 4 | 6 private-window opens with no `?v=` → roughly 3 A and 3 B; reloading keeps the same one | ☐ |
| 5 | Sheet receives `page_view`, `cta_click`, `disclosure_view`, `mini_survey_submit`, all `is_qa=TRUE` | ☐ |
| 6 | Disclosure is the first thing on screen after either CTA | ☐ |
| 7 | No Ownly/Rapido name or logo anywhere | ☐ |
| 8 | Survey button appears and carries `src=fakedoor_A` / `_B` | ☐ |
| 9 | Loads under 3 s on 4G, readable in dark and light mode | ☐ |
| 10 | **Keep the QA rows** — the analysis script excludes and counts them | ☐ |

## Distribution — one neutral post, one link

Use the **same single URL everywhere**. The variant is never in the link, so channel and variant cannot
correlate. Build one UTM per channel so we can read channel quality:

`https://<site>/?utm_source=<channel>&utm_medium=post&utm_campaign=gachi_concept&utm_content=<group_name>`

**Post text (identical on every channel — do not customise per group):**
> We're students researching how people around Gachibowli pick food-delivery apps. One page, about 30 seconds, nothing to sign up for: <link>

Log every post in `experiment_tracker.csv` (created alongside this file): channel, group name, approx.
group size, admin permission Y/N + date, posted-at timestamp, `utm_content`.

**Ask admin permission before posting in any group you do not own.** No paid promotion, no DM blasting,
no posting the same link twice in one group.

## Stopping rule — fix it now, before any traffic

- **Stop at:** **Tue 30 Sep 2026, 10:00 IST**, **or** 300 unique non-QA visitors, whichever comes first.
  *(Re-set on 2026-09-17: the original stop, Wed 16 Sep 22:00, passed before the page went live. This new
  rule is fixed before any traffic arrives, and does not move again.)*
- **Do not look at conversion by variant before the stop.** Mid-run, open the sheet only to confirm that
  events are arriving and that A and B counts are roughly equal. Peeking and stopping on a good-looking
  split is how a null result becomes a fake positive.
- **Sample-ratio mismatch check** at the stop: chi-square on visitors per arm. p < 0.01 means assignment
  or tracking is broken → fix and discard, do not interpret.

## Reading the result — pre-registered 2026-09-16, before any data

| Unique eligible visitors | Status of this experiment |
|---|---|
| **≥ 80, with ≥ 30 per arm** | **Primary H₀ test.** Two-proportion z on CTA CTR; Fisher's exact if any expected cell < 5. Report n per arm, CTR per arm, difference in percentage points, 95% CI on the difference, p, and the practical read. |
| **< 80, or < 30 in either arm** | **Directional only.** Report the raw counts and the CI, state the n on the slide, and make the survey's Section 7 the primary H₀ test. Do not report a p-value as if it decided anything. |

Secondary outcome: **bill-compare completions ÷ visitors** — a costlier action than a tap, so a better
intent signal. Same test, reported with the same n caveat.

**In every case:** this measures which *framing* makes people act. It is not purchase evidence, it is not
Ownly-branded, and the audience is whoever our channels reached. Those three sentences go on the slide.

## Export at the stop
1. Sheet → File → Download → CSV → `08_clean_data/raw/fakedoor_events_raw.csv`. **Never edit it.**
2. `python3 07_fake_door/analyze_fakedoor.py analyse --events 08_clean_data/raw/fakedoor_events_raw.csv --out 09_analysis/fakedoor --page-version 2026-09-16.1 --start 2026-09-16 --end 2026-09-16`
3. Send Claude: the two arm counts, the two CTR numbers, and the exclusions count.
