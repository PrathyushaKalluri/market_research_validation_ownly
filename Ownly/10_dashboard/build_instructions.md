# Dashboard Build Instructions

**Owner:** Agent F · **Drafted:** 2026-09-14 · Read `dashboard_blueprint.md` (what to build) and `dataset_schema.md` (tables) first.

---

## A. Recommended stack: Python → Google Sheets → Looker Studio

### A1. Pipeline (run after each data refresh)
1. **Export raw.** Download Google Forms responses (Sheets → File → Download → CSV) into `08_clean_data/raw/<city>_survey_<YYYYMMDD>.csv`. Never edit raw files.
2. **Run the PAP §12 pipeline** (`09_analysis/run_all.sh`, fixed seeds):
   - `00_manifest_and_hash.py` → `01_ingest_and_harmonise.py` (renames every column to `survey_variable_dictionary.csv` names) → `02_quality_flags.py` → `03_split_clean_excluded.py` (`cleaned/`, `excluded/` + `exclusion_reason`).
   - `04_derive_metrics.py` → `fact_survey_respondent`, `fact_dce_long`, `fact_wtp_long`, `fact_bill_choice_long`. This step computes `seg_occupation`, `seg_freq`, `beh_multihome`, `beh_any_subscription`, `own_repeat`, `wtp_max_fee`, `ppi`, `sri`, `rss`, `adi`, and the dashboard-derived `own_status`.
3. **Model and summarise.**
   - `06_hypothesis_tests.py` → `hypothesis_results.csv`
   - `07_dce_models.py` → `dce_coefficients.csv`, `dce_wtp.csv` (conditional logit; Krinsky-Robb CIs)
   - `08_wtp_curves.py` → `wtp_curve.csv`
   - `09_city_transfer.py` → `transfer_metrics.csv` (BA1–BA10, non-inferiority)
4. **Audit, reviews and fake door.**
   - `10_audit_analysis.py` → `fact_audit_obs`, `fact_audit_pairs` (`gap_rs` = Ownly − comparator), `audit_summary.csv`
   - `11_reviews_merge.py` → `fact_reviews`
   - `12_fakedoor.py` / `07_fake_door/analyze_fakedoor.py` → `fakedoor_summary.csv`, `agg_fakedoor_variant.csv`
5. **Scorecard.** `13_scorecard.py` → `fact_scorecard` (scopes × weight sets, computed exactly per `11_insights/decision_framework_and_scorecard.md` §1–§3).
6. **Publish mart.** Copy the outputs to `10_dashboard/mart/<table>.csv` **and** push each to a tab of one Google Sheet named `OWNLY_MART_<data_status>`. Use `gspread` with a service account, or upload manually via File → Import → Replace current sheet.
   - Keep separate Sheets for `demo` and `real`. Never put both in one sheet.
7. **Freeze a snapshot** for the final report: copy `mart/` to `mart_snapshots/<date>/` and record the git hash/date in `fact_model_coefs.code_ref`.

### A2. Looker Studio build
1. **Create → Report → Add data → Google Sheets →** `OWNLY_MART_real`. Add each tab as its own data source: `fact_survey_respondent`, `fact_dce_long`, `fact_wtp_long`, `fact_bill_choice_long`, `fact_model_dce`, `fact_model_coefs`, `fact_reviews`, `fact_interview_segments`, `fact_audit_obs`, `fact_audit_pairs`, `agg_fakedoor_variant`, `fact_fakedoor_events`, `dim_hypothesis`, `fact_evidence_matrix`, `fact_scorecard`, `dim_chart`.
   - In each source, set field types: `_inr` = Currency (INR) or Number; `_ts` = Date & Time; enums = Text; booleans = Boolean.
2. **Pages.** Create 10 pages named `1 Scorecard`, `2 BLR→HYD Transfer`, `3 Behaviour`, `4 Switching`, `5 Price×Reliability×ETA`, `6 Segments`, `7 Voice of Customer`, `8 Fake-door`, `9 Market reality`, `10 Recommendation`. Theme: custom, using the palette in blueprint §3.6.
3. **Global filter row.** Put controls on a report-level layer (Arrange → Make report-level):
   - Drop-down list on `city`, `seg_occupation`, `seg_freq`, `scr_locality`, `beh_platform_primary`, `beh_subscription`, `own_status`, `meta_brand_arm`, `meta_channel`.
   - Looker Studio filters apply only to sources that share the field name. Keep names identical across tables (`city`, `seg_occupation`, `seg_freq` are denormalised into long tables for this reason).
   - For tables without the field (audit, reviews), add a text box "filter not applied: occupation".
4. **Calculated fields** (in `fact_survey_respondent` unless noted):
   - `PPI` (if not precomputed in Python):
     ```
     ( ( (IFNULL(pain_fee_reconsider_freq,0)+IFNULL(pain_bill_unreasonable_freq,0)+IFNULL(pain_menu_markup_belief,0)+IFNULL(beh_abandon_price_freq,0))
         / ( (CASE WHEN pain_fee_reconsider_freq IS NULL THEN 0 ELSE 1 END)+(CASE WHEN pain_bill_unreasonable_freq IS NULL THEN 0 ELSE 1 END)+(CASE WHEN pain_menu_markup_belief IS NULL THEN 0 ELSE 1 END)+(CASE WHEN beh_abandon_price_freq IS NULL THEN 0 ELSE 1 END) ) ) - 1 ) / 4 * 100
     ```
     Wrap it in a CASE that returns NULL when fewer than 3 items are present. Precomputing in Python is strongly preferred.
   - `T2B trial` = `CASE WHEN bt_trial_intent >= 4 THEN 1 ELSE 0 END`. Chart metric = `AVG(T2B trial)`.
   - `n` = `COUNT_DISTINCT(resp_id)`
   - Wilson CI (for proportion `p` = AVG of a 0/1 field, `n` = COUNT):
     - `wilson_center` = `(AVG(x) + 1.9208/COUNT(resp_id)) / (1 + 3.8416/COUNT(resp_id))`
     - `wilson_half` = `1.96 * SQRT( AVG(x)*(1-AVG(x))/COUNT(resp_id) + 0.9604/POWER(COUNT(resp_id),2) ) / (1 + 3.8416/COUNT(resp_id))`
     - `ci_low` = `wilson_center - wilson_half`; `ci_high` = `wilson_center + wilson_half`
   - `Base-size flag` = `CASE WHEN COUNT_DISTINCT(resp_id) < 30 THEN "suppressed" WHEN COUNT_DISTINCT(resp_id) < 60 THEN "low base" ELSE "ok" END`
   - **n-suppression:** create a metric `PPI_shown` = `CASE WHEN COUNT_DISTINCT(resp_id) >= 30 THEN AVG(ppi) ELSE NULL END` and chart that instead of `AVG(ppi)`. Add the `Base-size flag` as a table column or scorecard subtitle.
5. **Weights parameters (View 1).** In `fact_scorecard`, create 5 parameters: `w_need` (default 20), `w_switch` (20), `w_econ` (20), `w_exp` (25), `w_beh` (15), each Number, 0–100, with an input-box control.
   - `weighted_contrib` = `CASE dimension WHEN "need" THEN dimension_score*w_need WHEN "switching" THEN dimension_score*w_switch WHEN "economic" THEN dimension_score*w_econ WHEN "experience" THEN dimension_score*w_exp WHEN "behavioural" THEN dimension_score*w_beh END / (w_need+w_switch+w_econ+w_exp+w_beh)`
   - Scorecard tile = `SUM(weighted_contrib)` filtered to `scope = pooled_hyd`, one row per dimension. Ensure `fact_scorecard` has one row per dimension per scope for the dimension-score view (use `input_metric = "_dimension"` rows).
   - **Dimension scores are never computed in Looker Studio.** `13_scorecard.py` computes them per framework §1:
     - linear anchors, clipped 0–100
     - NOT TESTABLE inputs (n < 30, or Ownly fee not audit-confirmed) dropped with weights re-normalised
     - badge drops one level per missing input
     - "INSUFFICIENT EVIDENCE" (empty score) when more than half of a dimension's weight is missing

     Weights only re-weight the scored dimensions: `weighted_contrib` must divide by the sum of weights of **non-empty** `dimension_score` rows.
   - The decision rule (framework §3) needs row-wise mins, segment scopes and badges. Precompute `recommendation`, `rule_applied` and `provisional` in Python for the four pre-registered weight sets (default 20/20/20/25/15, equal, behaviour-first 15/15/20/20/30, price-thesis 20/20/30/20/10), and show them as a sensitivity table. For custom weights, use a Sheets tab driven by weight cells:
     ```
     Sheets (weights B2:B6; pooled scores C2:C6, blank = INSUFFICIENT; D5 badge in E6;
             RETHINK condition in each scorable segment G2 (students), G3 (professionals) = TRUE/FALSE/blank if n<60;
             SCALE conditions met by a segment (students/professionals/frequent, n≥60) in G5 = TRUE/FALSE;
             count of LOW or INSUFFICIENT badges in E8)
     Weighted total  H2: =SUMPRODUCT(B2:B6,N(+C2:C6))/SUMIF(C2:C6,"<>",B2:B6)
     Decision        H3: =IF(AND(OR(AND(C2<>"",C2<40),AND(C3<>"",C3<40)),AND(OR(G2="",G2),OR(G3="",G3))),"RETHINK PROPOSITION",
                          IF(AND(COUNT(C2:C6)=5,H2>=70,MIN(C2:C6)>=50,OR(E6="HIGH",E6="MEDIUM")),"SCALE",
                          IF(G5,"TARGET SELECTIVELY","ADAPT")))
     Overlay         H4: =IF(E8>=2,"PROVISIONAL — evidence insufficient","")
     ```
     (ADAPT's sub-reason is "fix price architecture (D3) and/or experience/supply (D4)" when D1 ≥ 50, D2 ≥ 50 and D3 or D4 < 50; otherwise it names the weakest dimension. Write it as text from `rule_applied`.)
   - **Ownly fee:** never add a fee constant or reference line. Show the text "Ownly fee: audit-observed (TBD)" until `audit_summary` holds a confirmed observed fee. Scorecard input D3c stays NOT TESTABLE until then. Label the fee-ladder points "provisional".
   - **Competitor colours:** Swiggy, Zomato and Ownly use the neutral palette (ink / mid-grey / light-grey) with names as labels or small multiples. Never use brand colours.
6. **Chart mapping in Looker Studio** (where native charts fall short, embed the Plotly HTML export via the URL-embed component or a static image with a link):
   | Blueprint chart | Looker Studio component |
   |---|---|
   | Sorted bars, grouped columns | Bar chart (sort by metric, descending) |
   | Diverging Likert | Stacked 100% bar with negative categories pre-signed in Python (`share_signed`) |
   | Box plots, dumbbells, CI whiskers, forest plot, heatmap with suppression | Precompute in Python → Plotly HTML → URL embed (or a pivot table with heatmap conditional formatting for heatmaps) |
   | WTP curve | Line chart on `agg_wtp_curve` (precomputed: fee, segment, share, ci_low, ci_high) + a second series for CI bounds as lighter lines |
   | Funnel | Bar chart on `agg_fakedoor_variant` stage counts |
   | Transfer table | Table with conditional formatting on `verdict` (and a text icon column ✓ ! ✕ ?) |
   | Evidence matrix | Table from `fact_evidence_matrix` |
7. **Evidence trace.** Under each chart add a text box, `H# · table.field · n = {n} · strength`, or a small table bound to `dim_chart` filtered by `chart_id`.
8. **Sharing.** Share → Manage access → "Anyone with the link can view". The underlying Sheet stays restricted: set data credentials to **Owner's credentials** so viewers don't need Sheet access. Do not expose respondent-level free text on shared pages unless it has been reviewed for identifiability.

### A3. Plotly exports (hero charts)
In `09_analysis/09_charts.py`, build Views 2, 5, 8 with `plotly.graph_objects`:
- Use the blueprint palette. Titles are read from `dim_chart.title_mode`.
- Every figure has a subtitle `n = …`.
- Export with `fig.write_html(path, include_plotlyjs="cdn")` into `10_dashboard/exports/`.

---

## B. Power BI (if a licence is available)

**Data model**
- Import mart CSVs from a SharePoint/OneDrive folder, so refresh works.
- Relationships:
  - `fact_survey_respondent[resp_id]` 1→* `fact_dce_long`, `fact_wtp_long`, `fact_bill_choice_long` (single direction, filter from respondent).
  - `dim_segment` (seg_occupation × seg_freq, key `seg_key`) and `dim_city` → all fact tables with those fields.
  - `bridge_insight_hypothesis` between `fact_evidence_matrix` and `dim_hypothesis` (both directions on the bridge only).
- Mark `fact_audit_*`, `fact_reviews` and `agg_fakedoor_variant` as not related to `dim_segment`. Show "filter not applied" with a card using `ISFILTERED(dim_segment[seg_occupation])`.

**Key DAX**
```DAX
N Resp = DISTINCTCOUNT ( fact_survey_respondent[resp_id] )

PPI Mean =
VAR n = CALCULATE ( [N Resp], NOT ISBLANK ( fact_survey_respondent[ppi] ) )
RETURN IF ( n < 30, BLANK (), AVERAGE ( fact_survey_respondent[ppi] ) )

PPI CI Half =
VAR n = CALCULATE ( [N Resp], NOT ISBLANK ( fact_survey_respondent[ppi] ) )
RETURN IF ( n < 30, BLANK (), 1.96 * STDEV.S ( fact_survey_respondent[ppi] ) / SQRT ( n ) )

SRI Mean = IF ( [N Resp] < 30, BLANK (), AVERAGE ( fact_survey_respondent[sri] ) )

T2B Trial = DIVIDE ( CALCULATE ( [N Resp], fact_survey_respondent[bt_trial_intent] >= 4 ),
                     CALCULATE ( [N Resp], NOT ISBLANK ( fact_survey_respondent[bt_trial_intent] ) ) )

Wilson Low =
VAR n = CALCULATE ( [N Resp], NOT ISBLANK ( fact_survey_respondent[bt_trial_intent] ) )
VAR p = [T2B Trial]  VAR z = 1.96
VAR c = ( p + z*z / ( 2*n ) ) / ( 1 + z*z / n )
VAR h = z * SQRT ( p*(1-p)/n + z*z/(4*n*n) ) / ( 1 + z*z / n )
RETURN IF ( n < 30, BLANK (), c - h )
-- Wilson High: same with c + h

Base Flag = SWITCH ( TRUE (), [N Resp] < 30, "n<30 suppressed", [N Resp] < 60, "Low base", "n = " & [N Resp] )
```

**Weights and decision** (the dimension scores, badges and INSUFFICIENT EVIDENCE flags come precomputed in `fact_scorecard`; `BLANK()` scores are skipped and weights re-normalised. The measures below are simplified. Framework §3 also requires: RETHINK only if the D1/D2 gate holds pooled **and** in both scorable segments; SCALE also needs a D5 badge ≥ MEDIUM and all 5 dimensions scored; TARGET SELECTIVELY checks students, professionals **and frequent users**; ≥ 2 LOW/INSUFFICIENT badges → "PROVISIONAL — evidence insufficient". Implement these as extra conditions on `Decision` using `fact_scorecard[evidence_badge]`.)
- Modeling → New parameter → Numeric range (0–100, step 5) × 5: `W Need`, `W Switch`, `W Econ`, `W Exp`, `W Beh`.
- Dimension scores as measures, e.g. `Score Need = CALCULATE(MAX(fact_scorecard[dimension_score]), fact_scorecard[dimension]="need", fact_scorecard[input_metric]="_dimension", fact_scorecard[scope]="pooled_hyd")`.

```DAX
Weighted Total =
DIVIDE ( [Score Need]*[W Need Value] + [Score Switch]*[W Switch Value] + [Score Econ]*[W Econ Value]
       + [Score Exp]*[W Exp Value] + [Score Beh]*[W Beh Value],
         [W Need Value]+[W Switch Value]+[W Econ Value]+[W Exp Value]+[W Beh Value] )

Min Dimension = MINX ( { [Score Need], [Score Switch], [Score Econ], [Score Exp], [Score Beh] }, [Value] )

Segment Meets Scale = -- precomputed boolean per segment in fact_scorecard (n>=60 and SCALE criteria) 
  CALCULATE ( MAX ( fact_scorecard[segment_scale_flag] ), fact_scorecard[scope] IN { "student", "working_professional" } )

Decision =
SWITCH ( TRUE (),
  [Score Need] < 40 || [Score Switch] < 40, "RETHINK",
  [Weighted Total] >= 70 && [Min Dimension] >= 50, "SCALE",
  [Segment Meets Scale] = TRUE (), "TARGET SELECTIVELY",
  [Score Need] >= 50 && [Score Switch] >= 50 && ( [Score Econ] < 50 || [Score Exp] < 50 ), "ADAPT",
  "ADAPT" )
```
Note: `segment_scale_flag` must be computed with the **same weights**. If weights change, compute segment totals with the same `Weighted Total` pattern over segment-scoped score measures, rather than trusting a precomputed flag.

**Visuals:** error bars (Analytics pane → Error bars, bound to CI low/high measures) on bar/line charts. Deneb (Vega-Lite custom visual) for dumbbells, box plots and forest plots. Matrix with conditional formatting for heatmaps and the transfer table.

---

## C. Tableau (Desktop/Public; do not publish respondent-level data to Tableau Public)

**Data model:** Relationships canvas, with `fact_survey_respondent` as the root.
- Related tables: `fact_dce_long`, `fact_wtp_long` and `fact_bill_choice_long` on `resp_id`.
- Separate data sources for audit, reviews, fake-door and evidence matrix. Use **cross-data-source filters** on `city` (Filter → Apply to worksheets → All using related data sources, with `city` blended/defined as a related field).

**Calculated fields**
```
// N
COUNTD([resp_id])

// PPI shown
IF COUNTD([resp_id]) >= 30 THEN AVG([ppi]) END

// T2B trial (row-level)
IIF([bt_trial_intent] >= 4, 1, 0)

// Wilson low (aggregate)
( AVG([T2B trial]) + 1.9208/COUNTD([resp_id]) ) / ( 1 + 3.8416/COUNTD([resp_id]) )
- 1.96*SQRT( AVG([T2B trial])*(1-AVG([T2B trial]))/COUNTD([resp_id]) + 0.9604/SQUARE(COUNTD([resp_id])) ) / ( 1 + 3.8416/COUNTD([resp_id]) )

// Base flag
IF COUNTD([resp_id]) < 30 THEN "n<30 suppressed" ELSEIF COUNTD([resp_id]) < 60 THEN "Low base" ELSE "n = " + STR(COUNTD([resp_id])) END
```
- **Weights:** 5 parameters (Integer 0–100), shown as parameter controls.
  - `Weighted total` = `SUM(IIF([dimension]="need",[dimension_score]*[W Need],0)) + … ) / ([W Need]+[W Switch]+[W Econ]+[W Exp]+[W Beh])`, on `fact_scorecard` filtered to `scope="pooled_hyd"` and `input_metric="_dimension"`.
  - Min dimension: `WINDOW_MIN(SUM([dimension_score]))` as a table calculation, or precomputed per scope.
  - Decision: the same IF/ELSEIF chain as the DAX `SWITCH`.
- **Charts:**
  - Dumbbell: dual-*mark* (not dual-axis on different scales). Put `MIN(value)` circles and a line on the same measure axis via Measure Values with a synchronised axis, which gives the same scale.
  - Box plot: Analytics → Box plot.
  - CI whiskers: Gantt bar from `ci_low`, size `ci_high − ci_low`.
  - Heatmap: square marks + colour, with suppressed cells given a grey colour via `IF [n] < 30 THEN "suppressed"`.
- **Sharing:** Tableau Public only for **aggregated** tabs (agg tables, model outputs, audit pairs). Otherwise share a packaged workbook (.twbx) with professors.

---

## D. The HTML version (`prototype/dashboard_demo.html`)

- The prototype generates synthetic data in-page (seeded PRNG, `DEMO_SEED = 20260914`), then computes every metric, CI and the decision rule client-side.
- It uses the canonical names throughout: `survey_variable_dictionary.csv`, the real choice-experiment blocks from `dce_design_matrix.csv`, `audit_schema.csv` fields, and review and fake-door event names. The scorecard implements framework §1–§3 exactly, including NOT TESTABLE inputs, INSUFFICIENT EVIDENCE, badges, the PROVISIONAL overlay and the three alternative weight sets. The Ownly fee input D3c is NOT TESTABLE by design until the audit confirms the fee.
- **To switch it to real data** (only once the mart is final):
  1. Replace `generateDemoData()` with a loader that reads `mart/*.csv` embedded as JSON (the Artifact CSP blocks fetch to external hosts, so inline the JSON or publish the CSVs as supporting files and fetch them by relative path).
  2. Set `DATA_STATUS = "real"`. This removes the DEMO banner and enables insight titles from `dim_chart.title_insight` where `title_mode = "insight"`.
  3. Replace the DCE/driver panels' in-page approximations with `fact_model_dce` / `fact_model_coefs` values produced by Python (the in-page logistic regression is for layout demonstration only).
  4. Never keep any synthetic generator code path reachable when `DATA_STATUS = "real"`.
