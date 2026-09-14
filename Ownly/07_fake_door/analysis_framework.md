# Fake-Door Analysis Framework (index)

**Written by:** lead, 2026-09-14. This file indexes the analysis rules. The authoritative detail is in `experiment_plan.md` §8–13, and `analyze_fakedoor.py` applies it.

## Funnel (per variant; overall and per `utm_source`)
VISITOR (unique `anon_session_id`) → VALUE-PROPOSITION VIEW → CTA CLICK → HIGHER-INTENT ACTION ("Check your own last bill" calculator completed) → DISCLOSURE VIEW → MINI-SURVEY SUBMIT / SURVEY-LINK CLICK

## Primary metrics
| Metric | Numerator / denominator |
|---|---|
| CTA CTR (primary) | CTA-click sessions ÷ unique visitors |
| Higher-intent conversion | Calculator-completion sessions ÷ unique visitors (also ÷ CTA clickers) |
| Bounce | Sessions with only `page_view` ÷ unique visitors |
| Time-to-CTA | Median ms from load to first `cta_click`, with IQR |
| Mini-survey completion | Submits ÷ disclosure views |

## Pre-registered tests
- **Per-variant proportions:** Wilson 95% CIs.
- **Pairwise (A–B, A–C, B–C):** two-proportion z-test, or Fisher exact when any expected cell < 5. Holm correction across the 3 comparisons.
- **Effect size:** difference in pp with a Newcombe CI; relative lift.
- **Bayesian P(best):** beta-binomial with a Beta(1,1) prior and 20,000 draws. Descriptive only; never used as a stopping rule.

## DIRECTIONAL rule
Detecting +10 pp needs **199 visitors per arm** from a 10% CTR baseline (266 with Holm), or 294/392 from a 20% baseline. If the per-arm n is below the requirement for the observed baseline, every output is labelled **DIRECTIONAL**. The report then shows relative ordering, CIs and convergence with other evidence, and no "winner" claim is made.

## Segments
The segment (student / professional, frequency) is known only for people who click the CTA (mini-survey). So segment-level CTR **cannot** be computed; only the composition of clickers can be compared. Traffic-source splits use UTM.

## Exclusions
`is_qa`, `?v=` / `?qa` overrides, sessions with no endpoint set, bot heuristics (`08_clean_data/cleaning_protocol.md` §7), and duplicate sessions (the first assignment wins). All exclusions are logged with a reason.

## Triangulation (H11)
- H11.1: fake-door CTR ranking vs survey `bt_framing_pref` ranking.
- H11.2: higher-intent conversion ÷ survey top-2 trial intent. Descriptive calibration only, since the populations differ.
- Interview theme support for the leading framing.

## Stopping rule
A fixed window (see `experiment_plan.md` §9). No peeking-based stopping.
