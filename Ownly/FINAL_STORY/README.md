# FINAL_STORY — Ownly in Hyderabad (final dashboard)

| File | What it is |
|---|---|
| `Ownly_Hyderabad_Story.twbx` | **Tableau Story**, 11 story points (one per screen). Open in Tableau Desktop 2026.2 and click through with the arrows. |
| `Ownly_Hyderabad_Story.html` | The same 11 screens as a web page. Open in any browser; arrow keys move one screen. Print to PDF for a handout (A4 landscape). |
| `PRESENTER_SCRIPT.md` | What to say on each screen, about 7 minutes in total. |
| `data/evidence.csv` | Every number shown, with numerator, denominator, 95% interval, sample check, method and source file. |
| `data/*.csv` | One table per chart. |

## Rebuild everything

```
cd scripts
python3 build_evidence.py     # computes every number from the source files
python3 build_html.py         # writes the HTML page
python3 build_tableau.py      # writes the Tableau workbook
```
Standard library only. No pandas, and no chart libraries: charts are plain SVG written by Python (`charts.py`) and native Tableau worksheets.

## Sources read by `build_evidence.py`

Survey `final_dashboard/data/cleaned_survey.csv` (Gachibowli catchment n=40, Bengaluru n=16) · price audit
`final_dashboard/data/audit_*.csv` · app reviews and social posts `05_review_mining/...coded.csv` · YouTube
`final_dashboard/data/youtube_comments_coded.csv` · fake door `ownly_direct.xlsx`, `ownly_rapido.xlsx`. Media and filing
figures (Bengaluru orders, restaurant revolt, Foodpanda, Uber Eats, Zomato quote, rider cost) are cited, not computed.

## Rules applied

- Sample check on every percentage: 30+ = OK · 10–29 = Small (direction only) · under 10 = count only, never a %.
- Fake door: 25 `sess_natural_*` test rows and 1 duplicate session removed, leaving 70 live sessions.
- The home-screen A/B test (discount vs restaurants) is **not reported**: the app kept one arm per phone, so shared phones gave 58 vs 12.
- The fake door's restaurant list was fixed (14 places, Paradise Biryani first with a badge), so restaurant *picks* reflect list position as well as preference. Picks are not used as a demand ranking.
- Review and social figures are the share of posts that mention a theme. They are not failure rates.

## Checks run

- All survey, audit and review figures match the case study (e.g. 82.5%, 92.5/72.5/35%, 81.1→56.1→27.3%, 72.4%, 79.3%).
- The Tableau workbook was opened in Tableau Desktop 2026.2 on this machine. The log shows no schema errors, and all dashboards and the story laid out. **Look through it once by eye before presenting.**
- The HTML was rendered in headless Chrome at 1440×900 and every screen was checked for overlaps.
