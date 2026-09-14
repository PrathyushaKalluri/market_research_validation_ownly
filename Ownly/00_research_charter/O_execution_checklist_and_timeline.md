# O. Timeline & Project Execution Checklist

**Version:** 2026-09-14.

**Roles** (placeholders until names are supplied):
- **P1** — Bengaluru + Competitor Audit + Secondary
- **P2** — Hyderabad Survey + Interviews
- **P3** — Fake Door + Data/Analysis + Dashboard + Synthesis

## ⚠ Timeline reality check

The v1 plan assumed 14 days from 2026-09-03, which ends **2026-09-17**. Today is 2026-09-14. This v2 scope cannot be completed with real primary data in 3 days. Two options:

| Plan | Fieldwork | Final delivery | What's cut |
|---|---|---|---|
| **Recommended — 5 weeks** | 2026-09-17 → 2026-10-06 | **2026-10-19** | Nothing |
| **Compressed — 3 weeks** | 2026-09-16 → 2026-09-28 | **2026-10-05** | Bengaluru survey at minimum (70); 10 Hyderabad interviews; 1-week audit (3 slots); fake door 7 days (directional); no Bengaluru interviews; mixed logit dropped |

**→ The team must confirm the real submission date.** The plan below uses the recommended 5-week timeline.

## Week-by-week plan (recommended)

| Week | Dates | Milestones | Gate to pass |
|---|---|---|---|
| W0 — Finalise | Sep 14–16 | Review all Phase 0/1/2 documents; freeze hypotheses and thresholds; finalise fee/price levels from `market_price_anchors.md`; build 4 Hyderabad forms + Bengaluru form + randomiser; build fake door; pick audit restaurants and drop points; ethics/consent check (ask the course instructor whether institutional approval is needed) | Instruments reviewed by all 3 |
| W1 — Pilot + launch | Sep 17–23 | Pilot 6–8 per city (timing, comprehension) → fix → freeze PAP; launch surveys; audit wave 1 (5 slots); interviews 1–6; fake-door launch (fixed 14-day window) | Pilot go/no-go; PAP frozen before the first real response |
| W2 — Field | Sep 24–30 | Daily quota monitoring; mid-field quota rebalance (Sep 27); audit wave 2; interviews 7–12; first-pass coding; Bengaluru Ownly-user push | ≥ 60% of quotas filled by Sep 27 |
| W3 — Close + clean | Oct 1–7 | Interviews 13–16 (+ Bengaluru optional); survey close Oct 5; fake door closes Oct 1; cleaning pipeline; double-coding + κ; refresh review/social data | Sample flow table; κ ≥ 0.6 |
| W4 — Analyse | Oct 8–13 | Hypothesis tests, choice models, fee WTP, city transfer, audit pairs, scorecard + sensitivity; insight evidence matrix; contradictions list | All ★ hypotheses have a verdict |
| W5 — Synthesise + deliver | Oct 14–19 | Dashboard with real data; transfer slide; recommendation workshop (joint human decision); final deck + limitations + next research; professor dry-run | Every headline traced to evidence IDs |

## Master checklist

### Phase 0 — Charter (lead)
- [x] A Research charter — `00_research_charter/A_research_charter.md`
- [x] B Assumption map — `B_assumption_map.md`
- [x] C Hypothesis tree — `C_hypothesis_tree.md`
- [x] D Evidence matrix + data-source map — `D_evidence_collection_matrix.md`
- [x] E Bengaluru vs Hyderabad design — `E_research_design_blr_vs_hyd.md`
- [x] F Sample plan — `F_sample_plan.md`
- [ ] **Team review of thresholds marked *(A)* — P1, P2, P3 (Sep 16)**
- [ ] Confirm submission date; confirm whether ethics approval is required
- [ ] Insert real names into roles

### Phase 1 — Instruments
- [ ] Bengaluru Google Form (`02_bangalore_survey/`) — built by P1 from the copy-paste spec
- [ ] Hyderabad Google Forms × 4 versions + link randomiser (`03_hyderabad_survey/`) — P2
- [ ] Variable dictionary reconciled into `08_clean_data/master_data_dictionary.csv` — P3
- [ ] Interview screener, consent, guides, note template, coding framework (`04_interviews/`) — P2
- [ ] Review-mining dataset validated by a human on a 50-row sample (`05_review_mining/`) — P1
- [ ] Audit schema in Google Sheets; restaurant frame; drop points; field sheet (`06_competitor_audit/`) — P1
- [ ] Pilot test both surveys (6–8 each); log edits — P1/P2

### Phase 2 — Fake door
- [ ] Final copy updated with audit-verified ₹ examples (or "illustrative" label) — P3
- [ ] Host on GitHub Pages/Netlify; Apps Script collector live; QA with `?v=` override and `is_qa` — P3
- [ ] UTM links per channel; identical post text; fixed window — P3

### Phase 3 — Fieldwork & data
- [ ] Daily exports to `08_clean_data/raw/` with hashes — P3
- [ ] Daily quota and quality monitor — P2 (Hyderabad), P1 (Bengaluru)
- [ ] Audit waves 1–2, 10% double entry — P1 + P3
- [ ] 14–16 Hyderabad interviews; de-identified transcripts; 20% double-coded — P2 + P3
- [ ] Cleaning pipeline; RAW / CLEANED / EXCLUDED + adjudication log — P3

### Phase 4 — Analysis & dashboard
- [ ] PAP scripts `09_analysis/00–13` — P3
- [ ] All hypotheses → `dim_hypothesis` with verdict, n, CI — P3
- [ ] Qualitative synthesis ladder, JTBD, switch forces — P2
- [ ] Insight evidence matrix + contradictions — all
- [ ] Transfer matrix — P1 + P3
- [ ] Scorecard + weight sensitivity — P3
- [ ] Dashboard with real data (replace the DEMO data entirely; remove the banner only when no synthetic row remains) — P3

### Phase 5 — Decision & presentation
- [ ] Recommendation workshop (all 3; AI not the decider)
- [ ] Final deck storyline (`12_final_presentation/`)
- [ ] Limitations & next research
- [ ] Re-check secondary facts (Ownly Hyderabad status, fees) within 3 days of submission — P1
- [ ] Update `context.md`, `plan.md`, `progress.md`, `decisions.md`

## Risk register (top 6)

| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| Deadline shorter than the plan | High | High | Confirm date; switch to the compressed plan; protect audit + Hyderabad survey first | All |
| Too few Bengaluru Ownly users | High | High | Referral chain from every confirmed user; lapsed quota; minimum-defensible fallback; label limitation | P1 |
| Hyderabad professionals under-recruited | Medium | High | Insider shares in employee groups by W1; co-working posters; LinkedIn | P2 |
| Audit offers personalised / apps block | Medium | Medium | Record account state; multiple team accounts; stop before payment | P1 |
| Fake-door traffic too low | High | Low–Med | Pre-declared DIRECTIONAL; don't over-interpret | P3 |
| Choice experiment misunderstood by respondents | Medium | Medium | Pilot comprehension probes; worked example task; dominance check | P2 |
