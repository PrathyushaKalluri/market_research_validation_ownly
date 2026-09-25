# SOURCE_MAP — every headline traced to its calculation

Each entry gives the finding, the source file, the exact variable or rows, the calculation, the
population, the evidence label and the caveat that must travel with it.

Recompute everything: `scripts/01_clean_survey.py` → `02_audit.py` → `03_kpis_metrics_hypotheses.py`
→ `04_themes_evidence_dictionary.py` → `07_youtube_comments.py` → `05_build_dashboard.py` → `06_export.py`.

---

## Tab 01 — Business problem

**"37% had heard of Ownly, 4% had ever ordered."**
Source `Ownly Survey.csv`, item *"Ownly is a food delivery app by Rapido… which of these is true for
you?"* → `ownly_status` → `ownly_stage`. Aware = stage ≥ 1 (17/46); ordered = stage ≥ 3 (2/46).
Population `HYD_ELIGIBLE` n=46. **SURVEY — STATED BEHAVIOUR.** Caveat: trial base is 2 respondents —
DIRECTIONAL, LOW BASE.

**"Zero Ownly orders in the last four weeks."**
Item *"Ownly … how many orders in the last 4 weeks?"* → `n_ownly`. All 40 Hyderabad respondents who
ordered food reported 0. **SURVEY — STATED BEHAVIOUR.** Caveat: self-reported recall, 4-week window.

**"83% hold a Swiggy One / Zomato Gold membership."**
Item *"Which food delivery memberships do you have right now?"* → `has_membership` = any of Swiggy
One / Zomato Gold / other. 38/46. Wilson 95% CI 69.3–90.9%. **SURVEY — STATED BEHAVIOUR.** Caveat:
membership held, not necessarily actively used. Blank = none selected.

## Tab 03 / 05 / 06 — Price

**"Ownly cheapest in 4 of 4 baskets; median saving ₹114 (30.5%)."**
Source `06_competitor_audit/audit_data_slot1.csv`, rows where `discount_type = 'none'`, grouped
restaurant × basket × platform. Per DQ3, `LIST+FEES` takes `MAX(final_payable)` within `none`.
Saving = cheapest incumbent − Ownly. Win = Ownly lower by > ₹5. n=4 matched baskets.
**PRIMARY OBSERVED DATA.** Caveat: one dinner slot, one address, Ownly on a new account with a ₹50
intro offer, incumbents on subscribed accounts.

**"Offer Reversal Rate 50%; Membership Erosion Rate 25%."**
`audit_pairs.csv`. Reversal = baskets won in `LIST+FEES` but lost in `AFTER OFFER` ÷ matched baskets
(2/4). Erosion = won in `LIST+FEES` but lost in `MEMBER` ÷ matched baskets (1/4). **PRIMARY OBSERVED.**
Caveat: n=4. Membership erosion isolates a *standing* benefit; coupon reversal is episodic.

**"Non-food charges: Ownly 5.2%, Swiggy 28.3%, Zomato 18.0%."**
`(packaging + platform + delivery + small_cart + surge + GST) ÷ final_payable`, median over priced
captures (Ownly 8, Swiggy 15, Zomato 14). **PRIMARY OBSERVED DATA.**

**"Ownly quoted ETA +17 min."**
`eta_mid = (eta_min_shown + eta_max_shown) / 2`. Medians: Ownly 39.5, Swiggy 22.5, Zomato 17.5.
Gap = Ownly median − incumbent pooled median. **PRIMARY OBSERVED DATA.** Caveat: **quoted** ETA, not
delivery time. No test orders were placed.

**"Median required saving ₹50; the observed ₹114 clears 100% of stated thresholds."**
Item *"How much lower would the final amount need to be, every time, for you to make a different app
your main one?"* → `switch_savings_rs` (₹10–₹100+). Denominator = 35 who named a rupee figure.
**Held out of the denominator: 5 "no amount", 6 "don't know"** — reported separately, never as zero.
MM5 = share with threshold ≤ ₹114. **SURVEY — STATED PREFERENCE × PRIMARY OBSERVED.** Caveat: a
stated threshold is not observed switching.

## Tab 04 — The ₹30 equation *(the headline chart)*

**"85% trade speed, 67% trade reliability, 33% trade restaurants."**
Three forced binary items, ₹260 vs ₹230 held constant:

| Variable | Item | Chose ₹230 |
|---|---|---|
| `tradeoff_eta` | 30 min vs 45 min | 39/46 = 84.8% (CI 71.8–92.4) |
| `tradeoff_rel` | late 1-in-10 vs 3-in-10 | 31/46 = 67.4% (CI 53.0–79.1) |
| `tradeoff_rest` | most usual restaurants vs only a few | 15/46 = 32.6% (CI 20.9–47.0) |

Population `HYD_ELIGIBLE` n=46, all three answered by the same respondents.
**SURVEY — STATED PREFERENCE.** Test: McNemar exact, paired, assortment vs speed, **p = 8×10⁻⁶**.
Caveat: constructed pairs, not observed behaviour; the ₹30 level is fixed by the instrument and does
not vary.

## Tab 07 — Assortment

**"90.9% cross-platform overlap; 1 Ownly-only; 1 missing from Ownly."**
`audit_coverage.csv`, `restaurant_listed = 'y'` per platform, after the DQ4 name merge. Denominator =
11 restaurants listed on ≥ 1 incumbent; 10 also on Ownly. Ownly-only = Aanimuthyalu Unlimited.
Missing from Ownly = Pizza Hut. **PRIMARY OBSERVED DATA.** Caveat: 12 restaurants at one address.

**"67% will not give up their usual restaurants for ₹30."**
`tradeoff_rest`, complement of the above. **SURVEY — STATED PREFERENCE.**

**Late-night.** Only the `wed_dinner` slot was captured. Lunch and post-midnight are **not audited**,
so the daypart heatmap shows *captured / not captured* — it does not claim a late-night gap.

## Tab 08 — Discovery

**"Rapido Discovery Gap 84.6%."**
Item *"Have you seen an option to order food inside the Rapido app?"* → `rapido_food_seen`.
Denominator excludes *"I don't use the Rapido app"* → 39 Rapido users. Numerator = not "Yes"
(No 26 + Not sure 7) = 33. **"Not sure" is counted as not-noticed** — a deliberate, stated choice.
Wilson CI 70.3–92.8%. **SURVEY — STATED BEHAVIOUR.**

## Tab 09 — Trial vs retention

**"Trial-to-repeat intent gap 43.5pp."**
`prop_P_intent` top-2 (Probably/Definitely) = 78.3% minus `repeat_no_promo` top-2 = 34.8%.
Item: *"Imagine you tried the one you picked because of a ₹100 off first-order offer. Once that offer
ended, would you keep using it?"* **SURVEY — STATED PREFERENCE.**
Caveat: **STATED-INTENT PROXY, not retention.** The two items use different framings and the gap is
partly a framing artefact — it is a signal, not a measurement.

**"Price is 37.5% of discussion but 0% of app reviews; fulfilment is 18.9% vs 72.4%."**
`05_review_mining/social/social_coded.csv` (`relevant='1'`, first-hand `first_hand_ownly_use='1'`)
and `app_stores/reviews_coded.csv`. Themes mapped to families in `04_themes_evidence_dictionary.py`;
denominator = items carrying any mapped theme. **CONSUMER-GENERATED.**
Caveat: **share of coded items mentioning a theme — NOT an order failure rate.** All bases are
self-selected toward complaint.

**Quotes.** Verbatim from `prop_reason` ("In one line, what made you pick that one?"), 24 Hyderabad
respondents answered. Interview quotes exist but are **Gemini auto-notes, not human-verified
verbatim**, so none is placed on a slide; see `04_interviews/interview_findings_coded.md`.
No quote anywhere in this deck is invented.

**YouTube audience themes.** `05_review_mining/youtube/*_comments.json` — 275 verbatim comments
(77 + 199, minus one pinned self-promo comment) retrieved via the YouTube InnerTube API. Coded by
regex rules in `scripts/07_youtube_comments.py`; denominator = the **105** comments carrying at least
one theme. Likes parsed from strings. **CONSUMER-GENERATED.**
Caveat: shares of coded comments, **not** failure rates, **not** population incidence; viewers of two
Rapido-favourable explainer videos; national, not Gachibowli. Only **3** commenters claim first-hand
Ownly use — all three are shown verbatim rather than summarised.

**Interview findings.** `04_interviews/interview_findings_coded.md` — 1 documented transcript
(Gemini auto-notes, 2026-09-17) plus team-reported aggregate insights from an **UNKNOWN** number of
further interviews. **INTERVIEW (primary, qualitative).**
Caveat: no prevalence figures are derived because the denominator is unknown; notes are not
human-verified verbatim; no double-coding, so Cohen's κ is not computed.

**Segment split (interview claim T-1 tested).** `data/segment_tradeoffs.csv` — `tradeoff_eta` by
occupation: students 28/32 = 87.5%, working professionals 9/11 = 81.8%, **Fisher exact p = 0.637**.
Switching threshold medians: students ₹30 (n=26), professionals ₹50 (n=7).
**SURVEY — STATED PREFERENCE.** Caveat: n=11 professionals is underpowered; reported as partially
supported, not validated.

## Tab 10 — Challenger mechanisms

Historical evidence from `01_secondary_research/challenger_failures/` (5 dossiers, ~230 sources).
Strongest items: Uber Eats India per-order operating loss (**FACT** — SEC Form 8-K, Ex. 99.1,
21 Jan 2020); Foodpanda order collapse and FY19 RoC figures (**MEDIA REPORT / filings**); ONDC volume
decline (**MEDIA REPORT, single upstream**); Eternal Q1FY27 shareholder letter quote (**FACT** —
primary filing). Ownly-side evidence is our own audit and survey.
Caveat: **analogy, not causal proof.** No status asserts that Ownly will fail.

## Tab 14 — Hypothesis

**"Fail to reject H₀ (stated-preference analogue)."**
`prop_forced` — *"If only one of them existed where you live, which would you start using?"*
Service P 18, Service Q 15, "can't choose" 13. Exact binomial 18/33 vs 0.5 → **p = 0.7283**,
95% CI 36.1–71.7%. Paired check: McNemar on top-2 intent, b=3, c=2, p=1.0.
Population `HYD_ELIGIBLE` n=46; 33 expressed a preference. **SURVEY — STATED PREFERENCE (PROXY).**
Caveat: this is **not** first-order conversion. The behavioural H₀ is NOT DIRECTLY TESTED because the
fake door was never fielded (0 events).

**P1–P5 verdicts.** Pre-registered in `09_analysis/M_pre_analysis_plan.md §6.7` on 2026-09-18, before
any response was collected (tracker header-only; amendment A1). Computed in
`03_kpis_metrics_hypotheses.py`; results in `data/hypothesis_results.csv`.
**P3 was falsified and P1's first limb failed — both reported as they came out.**

---

## Figures that appear nowhere, by design

CAC · CLV · retention rate · market share · EBITDA · contribution margin · burn per order ·
restaurant counts beyond the 12 audited · actual delivery time · first-order conversion.
Listed in `data/not_estimable.csv` and shown on tab 03.
