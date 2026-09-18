# Fake-Door Value-Proposition Experiment — Plan

**Experiment ID:** `hyd_vp_fakedoor_v1` · **Owner:** Growth/experimentation workstream · **Drafted:** 2026-09-14 · **Status:** designed, not launched
**Serves:** H11 (behavioural intent vs stated intent), primarily. Directional input to H2 (price value proposition), H4 (price vs reliability) and H6 (segment differences). It does **not** test H7 (brand effect): the page is deliberately unbranded.

> Every section follows: **What we collect → Why → How → How we analyse → What decision it enables.**

---

## 1. Objective

**What we collect:** anonymous on-page behaviour from 20–30-year-old food-delivery users around Gachibowli who see one of three value-proposition framings of the same delivery concept.

**Why:** survey intent ("I would probably try it") is systematically inflated. A tap costs a respondent attention and a bill comparison costs effort; they are weak but real behavioural signals. The market-fit scorecard's *Behavioural validation* dimension needs at least one source that is not self-report.

**Decision it enables:** which framing Ownly-style positioning in Gachibowli should lead with (total price, transparent bill, or reliable value), and whether behavioural interest converges with or contradicts the survey and interviews.

## 2. Hypotheses (pre-registered)

| ID | Hypothesis | Label | Metric | Test |
|---|---|---|---|---|
| H11.FD1 | At least one framing produces a CTA click-through rate whose 95% CI lower bound exceeds 5% among eligible visitors | HYPOTHESIS | CTA CTR (clicks / unique visitors) | Wilson CI |
| H11.FD2 | The three framings differ in CTA CTR | HYPOTHESIS | CTA CTR | 3 pairwise two-proportion z tests (Fisher exact if any expected cell < 5), Holm-adjusted |
| H11.FD3 | Framings differ in *effortful* intent (completing the bill comparison) more than in clicks | HYPOTHESIS | Bill-compare completion / visitors | Same as FD2 |
| H4.FD | The reliability-value framing (C) converts at least as well as pure price framings (A, B) — i.e. price alone is not the stronger hook | HYPOTHESIS | CTR, C vs A and C vs B | Difference + 95% CI; non-inferiority read at −5 pp, descriptive only |
| H6.FD | Composition of clickers by occupation differs by variant (students over-represented in A; professionals in C) | HYPOTHESIS (weak test) | Share of mini-survey respondents by `seg_occupation` per variant | Descriptive; chi-square only if every cell ≥ 5 |

Thresholds above were set before data collection. The 5% floor in FD1 is **not** a universal benchmark; it only separates "some people act" from "essentially nobody acts" for a free, no-commitment tap. The main read is **relative** (variant vs variant) and **convergence** with other evidence.

## 3. Why fake-door evidence is not purchase evidence

- A tap is costless; ordering food involves money, habit, restaurant availability and a real ETA. Expect a large gap between click and adoption.
- The page is unbranded, so it tests the *proposition framing*, not Ownly's brand or its actual operations in Hyderabad.
- The audience is whoever our channels reach (community groups, LinkedIn, posters). It is a convenience sample, not a representative Gachibowli estimate.
- Therefore results are reported as **relative behavioural signal** and fed into the scorecard with a lower weight than survey/audit evidence unless the sample meets the confirmatory threshold (Section 8).

## 4. The three variants

All three describe the **same concept**: menu prices close to the restaurant's own, one flat delivery fee, visible pricing. What changes is the **lead framing** only. Full copy: `landing_page_copy.md`.

| Variant | `variant_key` | Lead framing | Hero headline | What it bets on |
|---|---|---|---|---|
| A | `A_total_price` | Lower **total checkout** price | "Same dinner. Smaller final bill." | Price pain is about the final amount (H1/H2) |
| B | `B_transparent_bill` | **Transparency** of the bill | "See the real price. Pay that price." | Pain is surprise/unfairness of fee lines, not the amount |
| C | `C_reliable_value` | Value **conditional on reliability** | "A fair price only counts if dinner arrives." | Low price is discounted unless delivery is trusted (H4) |

**Changes from the brief's draft lines, and why**
- A: the brief's "Your ₹250 meal shouldn't become ₹330 at checkout" states a specific markup as if typical. No verified Gachibowli basket premium exists yet (secondary research found only one consumer bill and no verified savings %). The ₹ story moved into a clearly labelled *illustrative* bill that is identical across variants, so the headline does not smuggle in an unverified number.
- B: kept the idea; "Pay that price" is honest about what the concept controls (no added fee lines) without promising the lowest price.
- C: app-review mining shows support/refund failures and late or cancelled orders as the highest-severity themes, so this framing is well motivated. Copy avoids "guarantee" or "on time, every time", because nobody in the market verifiably offers that and the page must not promise it.

**Illustrative bill (identical on all variants):** numbers are calibrated to national fee anchors (`01_secondary_research/market_price_anchors.md` §2: platform fee ≈ ₹17.58 incl. GST, 5% GST on food, 18% GST on delivery). They are labelled "Illustrative example only" on the page. **Before launch, replace them with medians from the Gachibowli competitor audit (`06_competitor_audit`) and bump `PAGE_VERSION`.** If the audit shows no consistent total-price advantage, remove the "Difference" stamp rather than keep a number the market does not support.

## 5. What is held constant

| Element | Constant value |
|---|---|
| Layout and order of sections | Strip → hero → CTA → illustrative bill → 3 points → CTA → footer |
| Imagery | None (typography + receipt only), so no image confound |
| CTA label | "See how this would work" (both positions) |
| CTA positions | Under hero and after the 3 points |
| Page length | Same structure; headline/subhead/point lengths kept within ±15 characters where possible |
| Eyebrow | "Food delivery around Gachibowli" |
| Bill module | Identical numbers and caption |
| Post-click flow | Identical disclosure, bill check, mini-survey, thank-you |
| Load speed | One file, same fonts, no variant-specific assets |
| Distribution text | One neutral post text for all channels (Section 7), no variant named in the link |

## 6. Randomisation and assignment

- **Single entry URL** for all channels. Variant is not in the link, so channel and variant cannot correlate.
- On first load the page draws A/B/C uniformly using `crypto.getRandomValues` and stores it in `localStorage` → a returning visitor sees the same variant (sticky).
- `?v=A|B|C` forces a variant for QA and marks every event `is_qa=true`; `?qa=1` does the same without forcing. QA traffic is always excluded.
- If the page has no `ENDPOINT` configured it is in **review mode**: shows a variant switcher, logs only to the console, flags events QA.
- **Sample-ratio mismatch check:** chi-square on visitors per arm; p < 0.01 means assignment or tracking is broken → fix before interpreting.
- Known leak: a person opening the link on two devices gets two IDs and possibly two variants. Accepted and disclosed; not fingerprinted by design.

## 7. Distribution plan

**One neutral post text (all channels):**
> "We're a university student team studying food delivery around Gachibowli. We've put a short concept page online and would value your honest reaction. It takes under a minute, and there's nothing to buy or sign up for: [link]"

| Channel | Where | Permission rule | `utm_source` | `utm_medium` | `utm_content` |
|---|---|---|---|---|---|
| WhatsApp groups | PG/hostel/apartment and campus community groups in Gachibowli, Telecom Nagar, Kondapur, Nanakramguda | Ask the admin first; post once, no DMs to members | `whatsapp` | `community_group` | group code, e.g. `pg_telecomnagar_01` |
| Telegram groups | Same logic | Admin permission | `telegram` | `community_group` | group code |
| LinkedIn | Team members' posts; Hyderabad tech/community groups | Group rules | `linkedin` | `post` | `member1`, `group_hydtech` |
| Instagram | Story from team/club accounts | Account owner | `instagram` | `story` | account code |
| QR posters | Campus notice boards, cafés, co-working spaces | Written/verbal permission from the venue | `qr_poster` | `offline` | venue code |

`utm_campaign` is always `hyd_vp_fakedoor_v1`. **No paid boosting** unless the same budget and targeting apply to the single URL (the variant is randomised on the page, so a boost cannot favour one variant, but it does change audience mix, so log it as its own `utm_source`).

Do not post in Ownly/Rapido-branded communities or reply threads, and do not tag either company.

## 8. Sample size, power and the DIRECTIONAL rule

Per-arm sample size for a two-sided two-proportion test, power 0.80:

n = [ z₁₋α/₂·√(2·p̄(1−p̄)) + z₁₋β·√(p₁(1−p₁) + p₂(1−p₂)) ]² / (p₂ − p₁)²,  with p̄ = (p₁+p₂)/2, z₀.₈ = 0.842.

| Baseline CTR p₁ | Detect | n per arm, α = 0.05 (z = 1.960) | n per arm, α = 0.05/3 Holm first step (z = 2.394) |
|---|---|---|---|
| 5% | +5 pp | 435 | 580 |
| 5% | +10 pp | 141 | 188 |
| 10% | +5 pp | 686 | 915 |
| 10% | +10 pp | 199 | 266 |
| 20% | +5 pp | 1,094 | 1,460 |
| 20% | +10 pp | 294 | 392 |
| 30% | +10 pp | 356 | 475 |

**Minimum detectable effect at realistic traffic** (α = 0.05 unadjusted / Holm first step):

| Visitors per arm | Baseline 10% | Baseline 20% |
|---|---|---|
| 50 | +22.7 / +27.1 pp | +26.1 / +30.5 pp |
| 100 | +15.0 / +17.8 pp | +17.9 / +21.0 pp |
| 150 | +11.8 / +14.0 pp | +14.4 / +16.8 pp |
| 250 | +8.8 / +10.4 pp | +10.9 / +12.8 pp |
| 400 | +6.8 / +8.0 pp | +8.5 / +9.9 pp |

**Reality check (INTERPRETATION):** a student team using community groups and posters will plausibly reach a few hundred eligible visitors in total, i.e. roughly 50–200 per arm. At that size only very large differences (≥ 12–27 pp) are detectable. **The pre-registered rule:** if the smallest arm is below the requirement for +10 pp at α = 0.05/3 using the observed pooled CTR as baseline, the result is labelled **DIRECTIONAL** everywhere it appears (report, dashboard View 8, scorecard). `analyze_fakedoor.py` applies this automatically.

**Target:** 300 eligible visitors per arm (900 total). **Floor for reporting at all:** 50 per arm.

## 9. Stopping rule

- **SUPERSEDED 2026-09-17 by the 2-arm runsheet** (`AB_LAUNCH_RUNSHEET_v2.md`), which is the live rule:
  **launch 2026-09-17 · stop Tue 30 Sep 2026, 10:00 IST, or 300 unique non-QA visitors, whichever comes first.**
  The 300 figure replaces the 900 below because the design collapsed from 3 arms to 2 (decision D2) and
  900 was never reachable through student channels. Fixed before any traffic; it does not move again.
- ~~Fixed window: **10 consecutive days** from launch, or **900 eligible visitors**, whichever comes first.~~
- One mid-point **data-quality** check only (events arriving, SRM, QA exclusion working). Conversion by variant is **not** looked at before the end.
- No early stopping for a "winner"; no extending the test because a result is "almost significant".
- If copy must change mid-test (e.g. audit numbers arrive), bump `PAGE_VERSION`, and analyse versions separately; never pool.

## 10. Metrics

| Metric | Definition | Role |
|---|---|---|
| Unique visitors | Distinct `anon_visitor_id` after exclusions | Denominator |
| VP view rate | Visitors with `vp_view` (hero ≥ 60% visible for 3 s, or scroll ≥ 50%, or CTA) / visitors | Exposure check |
| **CTA CTR** | Visitors with ≥ 1 `cta_click` / visitors | **Primary** |
| CTA given VP view | CTA clickers / VP viewers | Diagnostic |
| **Bill-compare rate** | Visitors with `secondary_intent` / visitors | **Key secondary (higher intent)** |
| Bill-compare given CTA | `secondary_intent` / CTA clickers | Diagnostic |
| Mini-survey completion | `mini_survey_submit` / CTA clickers | Data coverage |
| Main-survey click | `survey_link_click` / CTA clickers | Extra intent signal |
| Bounce rate | No CTA, no scroll_50 and dwell < 10 s / visitors | Page quality |
| Time to CTA | Median `time_since_load_ms` of first CTA | Friction/clarity |
| Breakdowns | By `utm_source`, device; clicker composition by `seg_occupation`, `seg_freq`, locality | Descriptive only |

**Why the higher-intent action is a bill comparison, not a waitlist:** it needs no personal data, takes real effort (finding the last order and typing two numbers), and yields useful self-reported data on the bill gap (H1). It is labelled as self-reported and non-representative wherever used.

**Limitation to state:** segment is known only for clickers who answer the mini-survey, so **segment-level CTR cannot be computed**. We can only compare *who clicked* across variants.

## 11. Exclusions (visitor level, logged with reason, never silently dropped)

`qa_traffic` · `bot_suspect` (webdriver/crawler UA) · `multiple_or_invalid_variant` · `outside_test_window` · `cta_faster_than_1s` · `missing_visitor_id`. Exact duplicate events are removed before aggregation and counted. Exclusion file: `fakedoor_exclusions.csv`.

## 12. Ethics and privacy

- **No impersonation.** The page does not use Ownly's or Rapido's name, logo, colours or trade dress and states it is not affiliated with any food-delivery company.
- **No false availability.** It never says "coming soon" or implies ordering is possible. The CTA reads "See how this would work", not "Order" or "Check availability".
- **Immediate debrief.** The first screen after a tap says: "Research prototype — No app, no order, no payment." Everything after that is optional.
- **No personal data.** No name, phone, email, location or IP is collected. A random ID in local storage prevents double-counting. Bill amounts and mini-survey answers are optional and anonymous.
- **Visible notice.** Footer identifies the page as a university research prototype and links an expandable "What this page records" notice.
- **Institutional check (ACTION for the team):** confirm with the course instructor whether the university's ethics committee requires review for online behavioural studies with deception-by-omission. Record the answer in `decisions.md`.
- **Data retention:** raw events deleted after the project ends; only aggregate tables go into the report.

## 13. Convergence checks (triangulation)

| Question | Fake-door evidence | Compare against | Converges if |
|---|---|---|---|
| Which framing pulls hardest? | CTR and bill-compare rate ranking A/B/C | Survey: matched item showing the three headlines (randomised order) asking which would most make them look at a new delivery app | Same top framing, or overlapping CIs in both |
| Is price the hook, or reliability? | C vs A/B difference | DCE price-vs-reliability trade-offs (H4); review severity of late/cancel/refund themes; interview codes on reliability | C ≥ A/B behaviourally **and** reliability outweighs ₹ savings in DCE |
| Is bill pain real? | Self-reported bill gap % (bill-compare users) | Survey `beh_last_order_total` vs food subtotal; competitor audit basket premium | Medians within ~10 pp of each other |
| Who responds? | Clicker composition by occupation/frequency | Survey segment differences in brand-blind trial intent | Same segment leads |

Contradictions are reported, not resolved away, in the insight evidence matrix.

## 14. Launch checklist

1. Replace illustrative bill numbers with audit medians (or remove the stamp) → bump `PAGE_VERSION`.
2. Create Google Sheet + Apps Script collector (`apps_script_collector.gs`), deploy, paste URL into `CONFIG.ENDPOINT`.
3. Set `CONFIG.SURVEY_URL` to the Hyderabad survey link.
4. Host on GitHub Pages or Netlify (`deploy_instructions.md`).
5. QA with `?qa=1` on Android Chrome, iOS Safari and desktop; confirm rows arrive flagged `is_qa=true`.
6. Generate UTM links per channel; record launch date and stopping date in Section 9.
7. Get admin/venue permissions logged.
8. Launch; mid-point data-quality check only; analyse at stop with `analyze_fakedoor.py`.
