# Deploy, QA and Export — `hyd_vp_fakedoor_v1`

Time needed: ~45 minutes. Cost: ₹0. Nothing here needs a paid account.

## 1. Before you deploy

1. Replace the illustrative bill numbers in `prototype/index.html` (the `<tbody>` under the comment "ILLUSTRATIVE numbers") with medians from `06_competitor_audit`, or delete the "Difference in this example" block if the audit shows no consistent advantage. Mirror the change in `landing_page_copy.md`.
2. Set `CONFIG.PAGE_VERSION` to today's date + revision, e.g. `2026-09-18.1`.
3. Keep `CONFIG.ENDPOINT` empty until step 2 is done; while empty, the page is in review mode (switcher bar, console logging, all events QA).

## 2. Create the event collector (Google Sheet + Apps Script)

1. Create a Google Sheet named `hyd_vp_fakedoor_v1_events` in a team-owned Google account (not a personal one you will lose access to).
2. Extensions → Apps Script. Delete the sample code, paste `apps_script_collector.gs`, save.
3. Run the `setup` function once (authorise when asked). A tab `events` with a header row appears.
4. Deploy → New deployment → type **Web app** → Execute as **Me** → Who has access **Anyone** → Deploy. Copy the Web app URL (ends in `/exec`).
5. Open that URL in a browser: it should say `collector alive: hyd_vp_fakedoor_v1`.
6. Paste the URL into `CONFIG.ENDPOINT` in `prototype/index.html`. The review bar disappears.
7. Set `CONFIG.SURVEY_URL` to the Hyderabad Google Form link (or leave empty to hide the button).

If you edit the script later: Deploy → Manage deployments → edit → **New version**; the URL stays the same.

## 3. Host the page (pick one)

**GitHub Pages**
1. Create a public repo, e.g. `gachibowli-food-concept-study` (neutral name; do not use Ownly/Rapido in repo name or URL).
2. Upload `prototype/index.html` to the repo root.
3. Settings → Pages → Deploy from branch → `main` / root. URL: `https://<user>.github.io/gachibowli-food-concept-study/`.

**Netlify Drop**
1. Go to app.netlify.com/drop, drag the `prototype` folder.
2. Site settings → change site name to something neutral. URL: `https://<name>.netlify.app/`.

## 4. QA checklist (run with `?qa=1` so rows are flagged and excluded)

| # | Check | Pass |
|---|---|---|
| 1 | Page loads < 3 s on 4G on Android Chrome, iOS Safari, desktop Chrome | ☐ |
| 2 | Open `?qa=1&v=A`, `?qa=1&v=B`, `?qa=1&v=C` — correct headline/subhead/points; everything else identical | ☐ |
| 3 | Open without `v` in a private window 6+ times: variants appear roughly evenly; reloading the same window keeps the same variant | ☐ |
| 4 | Sheet receives `page_view`, `vp_view` (wait 3 s), `scroll_50`, `cta_click`, `disclosure_view`, `secondary_intent`, `mini_survey_submit`, `exit` (close tab) — all `is_qa = TRUE` | ☐ |
| 5 | `utm_*` columns populated from a test UTM link | ☐ |
| 6 | Bill check: blank → error; ₹20 → range error; ₹240/₹310 → "₹70 more … 29% on top" | ☐ |
| 7 | Disclosure is the first thing visible after either CTA | ☐ |
| 8 | No personal data anywhere in the sheet | ☐ |
| 9 | Footer and "What this page records" visible; no Ownly/Rapido name or logo anywhere | ☐ |
| 10 | Dark mode and light mode both readable | ☐ |
| 11 | Delete QA rows? **No** — keep them; the analysis script excludes them and logs the count | ☐ |

## 5. Launch

- Build one UTM link per channel/group (see `event_schema.md` → UTM convention) and log each in a channel register sheet: `utm_content`, group/venue, admin permission (Y/date), posted at.
- Record the launch date and stopping date in `experiment_plan.md` §9 **before** posting.
- Mid-point: open the sheet only to confirm events arrive and variant counts are roughly equal. Do not compute CTR by variant.

## 6. Export and analyse at the stopping point

1. Sheet → File → Download → CSV (the `events` tab) → save as `08_clean_data/raw/fakedoor_events_raw.csv`. Never edit this file.
2. Run from the project root:
   ```
   python3 07_fake_door/analyze_fakedoor.py analyse \
     --events 08_clean_data/raw/fakedoor_events_raw.csv \
     --out 09_analysis/fakedoor \
     --page-version 2026-09-18.1 --start 2026-09-18 --end 2026-09-28
   ```
3. Move `09_analysis/fakedoor/fakedoor_exclusions.csv` copy into `08_clean_data/excluded/`.
4. Paste the evidence label (DIRECTIONAL / CONFIRMATORY) into the dashboard View 8 title and the insight evidence matrix.

## 7. After the project

Delete the Google Sheet and take down the page (GitHub: delete repo or disable Pages; Netlify: delete site). Keep only the aggregate outputs in `09_analysis/fakedoor/`.
