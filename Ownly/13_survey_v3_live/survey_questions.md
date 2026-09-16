# Survey v3 (LIVE) — Every Question, Exact Wording

**Build target:** one Google Form. **Do not start sharing before written ethics approval.**
Variable names match `03_hyderabad_survey/survey_variable_dictionary.csv` where the item is unchanged;
items marked **NEW-v3** must be appended to the dictionary.

**Form settings:** Collect email OFF · Limit to 1 response OFF · Progress bar ON ·
Shuffle question order OFF (per-question shuffle is set individually below) ·
Confirmation message: *"Thank you — your answers are anonymous. Please pass this on to anyone aged 20–30 who orders food delivery."*

---

# SECTION 1 — About this survey

**Section description (paste exactly, filling the four brackets):**
> We are a student research team at **[University name]** studying how people aged 20–30 choose food-delivery apps. This is independent university coursework. We are not paid by, and do not work with, any food-delivery company. It takes about **7 minutes** and is anonymous — we do not ask for your name, phone number or email. Taking part is voluntary, you can stop at any time, and you may skip optional questions. Answers are used only for our course project and are deleted after grading. Questions: **[team email]**. Approved by **[instructor name]** on **[date]**.

| # | Var | Question | Type | Options | Req | Branch |
|---|---|---|---|---|---|---|
| Q1 | `meta_consent` | I have read the above and agree to take part. | Multiple choice | Yes, I agree · No | Yes | Yes→S2 · No→S0 |

*Purpose:* ethics requirement. *Feeds:* exclusion flag.

---

# SECTION 2 — Quick check *(universal screener)*

| # | Var | Question | Type | Options | Req | Branch |
|---|---|---|---|---|---|---|
| Q2 | `scr_age_band` | How old are you? | MC | Under 20 · 20–22 · 23–25 · 26–28 · 29–30 · Over 30 | Yes | Under 20→S0 · Over 30→S0 · else next |
| Q3 | `scr_orders_4wk` | In the last 4 weeks, about how many times did you order food for delivery through any app? | MC | None · 1–3 · 4–7 · 8–15 · 16 or more | Yes | None→S0 · else next |
| Q4 | `scr_city` | **Where do you currently live and primarily order food?** | MC | Hyderabad · Bengaluru · Other city | Yes | **Hyderabad→S3 · Bengaluru→S11 · Other city→S12** |

*Purpose:* Q2/Q3 enforce the target frame (20–30, recent category behaviour). Q4 is the canonical
geography router — it decides the respondent's **research role**, not just a demographic field.
*Feeds:* eligibility, `seg_freq` (1–3 light / 4–7 regular / 8+ heavy), city segmentation (never blended).
*Build note:* put Q2, Q3 and Q4 on **three separate sections** (2a, 2b, 2c) — Forms can only branch from
the last question on a page.

---

# ══ HYDERABAD PATH — PRIMARY VALIDATION ══

# SECTION 3 — About you

| # | Var | Question | Type | Options | Req |
|---|---|---|---|---|---|
| Q5 | `scr_area` | Which area do you live, study or work in on most days? | MC | Gachibowli · Financial District / Nanakramguda · Kondapur · Madhapur / HITEC City · Manikonda · Narsingi / Kokapet · Serilingampally / Chandanagar · Tellapur / Nallagandla · Somewhere else in Hyderabad | Yes |
| Q6 | `seg_occupation_raw` | Which best describes you right now? | MC | Full-time student (undergraduate) · Full-time student (postgraduate / PhD) · Working full-time · Studying and working (incl. internships / part-time) · Other / between jobs | Yes |
| Q7 | `beh_rapido_freq` | How often do you use the **Rapido** app (bike taxi / auto / cab)? | MC | Never · Tried it once or twice · A few times a month · Weekly · Almost daily | Yes |

*Q5 purpose:* catchment. **"Somewhere else in Hyderabad" is NOT screened out** — it is flagged
`out_of_catchment` and reported separately. Screening it out would shrink an already small sample and
throw away a useful contrast. *Q7 purpose:* the distribution hypothesis (does an existing Rapido habit
predict Ownly awareness/trial?). *Feeds:* H-distribution, BDI by segment, `rapido_user` split.

---

# SECTION 4 — Your last order

| # | Var | Question | Type | Options | Req |
|---|---|---|---|---|---|
| Q8 | `beh_last_platform` | Which app did you use for your **most recent** food-delivery order? | MC | Swiggy · Zomato · Ownly app · Rapido app (food section) · Toing · Magicpin · Restaurant's own app / phone · Other | Yes |
| Q9 | `beh_last_order_total` | What was the **final amount you paid** for that order — including all charges, after discounts? (₹) | Short answer · **Number, between 0 and 10000** | — | Yes |
| Q10 | `beh_last_food_only` | **NEW-v3** And roughly what was the **food itself** worth on that order, before any fees, taxes or discounts? (₹ — your best estimate is fine) | Short answer · **Number, between 0 and 10000** | — | Yes |

*Purpose:* Q9 − Q10 gives a **self-reported fee gap** per respondent, which we compare directly against
the **observed** fee gap from the Gachibowli audit. That comparison — *what people think they pay in fees
vs what they actually pay* — is a genuine finding either way and costs one extra question.
*Feeds:* fee share of bill; calibration of survey self-report against audit observation.
*Ask before the brand reveal* so the answer is not primed.

---

# SECTION 5 — Your habits and what annoys you

| # | Var | Question | Type | Options | Req |
|---|---|---|---|---|---|
| Q11 | `beh_platforms_used_4wk` | Which apps have you ordered food delivery from in the last 4 weeks? *Select all.* | Checkboxes | Swiggy · Zomato · Ownly app · Rapido app (food section) · Toing · Magicpin · Restaurant direct · Other | Yes |
| Q12 | `beh_subscriptions` | Which food-delivery memberships do you have right now? | Checkboxes | Swiggy One (any plan) · Zomato Gold · Another food-delivery membership · None · Not sure | Yes |
| Q13 | `beh_offer_dependency` | Of your last 10 delivery orders, roughly how many used a coupon, offer or membership discount? | MC | 0–1 · 2–4 · 5–7 · 8–10 · Don't know | Yes |

**Q14 — grid.** *"In the last 4 weeks, how often did each of these happen to you?"*
Multiple-choice **grid** · require a response in each row · **shuffle rows ON**
Columns: `Never · Rarely · Sometimes · Often · Very often`

| Row var | Row text |
|---|---|
| `pain_fee_reconsider_freq` | The charges added at checkout (fees, packaging, taxes) made me reconsider or change my order |
| `pain_bill_unreasonable_freq` | The final amount felt unreasonable for the food I ordered |
| `beh_abandon_price_freq` | I left without placing an order after seeing the final amount |
| `pain_late_freq` | My order arrived noticeably later than the time shown |
| `pain_cancel_freq` | My order was cancelled by the app or the restaurant |
| `pain_support_freq` | **NEW-v3** I had to contact support, or chase a refund, about an order |
| `att_check_1` | To show you are reading carefully, please select "Rarely" for this row |

| # | Var | Question | Type | Options | Req |
|---|---|---|---|---|---|
| Q15 | `pain_top_frustrations` | Which of these frustrate you most about food delivery today? *Select up to 3.* | Checkboxes · validation **Select at most 3** · **shuffle ON** | Delivery fees · Platform, packaging or other charges · Menu prices higher than at the restaurant · Offers that don't really save money · Late delivery · Cancelled orders · Wrong or missing items · Getting refunds or help from support · The restaurant I want isn't available · Food quality or hygiene · Nothing really frustrates me | Yes |

*Purpose:* Q12/Q13 test the **"incumbent coupons erase the gap"** theme (18 social posts). Q14 rows map
1:1 onto the two theme families that dominate first-hand accounts (fulfilment 47%, support 28%).
`att_check_1` is the data-quality gate in `08_clean_data/cleaning_protocol.md`.

---

# SECTION 6 — Quick choices

**Section description:** *"These are made-up examples, not real offers from any app. Assume everything else about the two apps is the same."*
**Shuffle option order ON for all three** — so the cheaper option is not always listed second.

| # | Var | Question | Option A | Option B |
|---|---|---|---|---|
| Q16 | `tradeoff_eta` | Same restaurant, same food. Which would you choose? | ₹260 total, arrives in **30 minutes** | ₹230 total, arrives in **45 minutes** |
| Q17 | `tradeoff_rel` | Same restaurant, same food, same delivery time. | ₹260 total, late by 15+ min in about **1 of every 10** orders | ₹230 total, late by 15+ min in about **3 of every 10** orders |
| Q18 | `tradeoff_rest` | Same food price level and delivery time. | ₹260 total, has **most** of your usual restaurants | ₹230 total, has **only a few** of your usual restaurants |

| # | Var | Question | Type | Options | Req |
|---|---|---|---|---|---|
| Q19 | `beh_switch_savings_required` | Think of a typical order of yours. How much lower would the final amount need to be, **every time**, for you to make a different app your main one? | MC | ₹10 · ₹20 · ₹30 · ₹50 · ₹75 · ₹100 or more · No amount — price alone wouldn't make me switch · Don't know | Yes |

*Purpose:* each trade-off holds ₹30 constant and varies **what ₹30 buys**. Directly tests
*"price may acquire, reliability may retain"*. Q19 is the switching threshold we compare against the
**observed** median saving from the audit — if the audit gap is below the modal threshold, the price
proposition does not clear the bar in Gachibowli, and that is a headline result.
*Analysis:* % choosing cheaper option with Wilson CI; student vs professional; heavy vs light.
*Interpretation rule (pre-registered):* ₹30 "buys" that compromise only if the **lower CI bound > 50%**.

---

# ★ SECTION 7 — Two services *(the H₀ instrument)*

**Section description (paste exactly):**
> Below are two different food-delivery services being considered for Hyderabad. Neither exists exactly as described. Please read both before answering.

**Then two image-or-text blocks, in this fixed order. Keep them the same length and format.**

**SERVICE P**
> **Same food. Smaller final bill.**
> • Menu prices are the restaurant's own prices, not marked up for the app
> • One flat delivery fee — no platform fee, no packaging fee, no surge charge
> • The total you see is the total you pay

**SERVICE Q**
> **Your Hyderabad regulars, and dinner that actually turns up.**
> • The local biryani, tiffin and meals places you already order from — not only the big chains
> • The delivery time shown is the time it actually takes
> • If an order goes wrong, a clear answer and your money back fast
> • Fair prices with every charge visible before you pay

| # | Var | Question | Type | Options | Req |
|---|---|---|---|---|---|
| Q20 | `prop_P_intent` | If **Service P** were available where you are, how likely are you to try it for one of your next few orders? | MC | Definitely not · Probably not · Not sure · Probably · Definitely | Yes |
| Q21 | `prop_Q_intent` | And if **Service Q** were available, how likely are you to try **it** for one of your next few orders? | MC | *(same five)* | Yes |
| Q22 | `prop_forced_choice` | **If only one of them existed where you live, which would you start using?** | MC · **shuffle ON** | Service P · Service Q · I genuinely can't choose between them | Yes |
| Q23 | `prop_reason` | In one line — what made you pick that one? | Short answer | — | **No** (optional) |
| Q24 | `prop_durability_doubt` | **NEW-v3** How much do you agree: *"A new app's low prices usually go up once it becomes popular."* | MC | Strongly disagree · Disagree · Neither · Agree · Strongly agree | Yes |

### Why these two, and what changes between them
Both describe the **same category** of service and both mention price — so the manipulation is
**emphasis**, not a price-vs-no-price confound.
- **Service P = the Bengaluru playbook**, stated as the review log defines it: lower final bill,
  no hidden fees, transparent pricing.
- **Service Q = the Hyderabad-localized alternative**, built from this project's own consolidated
  evidence: local assortment + fulfilment reliability + support/refund + visible pricing.

> ⚠ **Service Q's copy is v0 and MUST be re-checked against the first two pilot interviews before the
> form is shared.** The orchestrator brief requires the localized variant to be derived from interviews,
> not from desk research. If the pilots surface a different dominant local concern (e.g. cash-on-delivery
> or meal cards, which appear in the social data), swap the weakest bullet and log it in `decisions.md`.
> After responses begin, Section 7 copy is **frozen** — see `google_forms_build_guide.md` §10.

### Analysis (pre-registered 2026-09-16, before any data)
| Outcome | Test | Rule |
|---|---|---|
| `prop_forced_choice` (P vs Q, excluding "can't choose") | **Exact binomial vs 50%**, Wilson CI | **Primary within-survey H₀ test** |
| `prop_P_intent` vs `prop_Q_intent`, dichotomised at *Probably/Definitely* | **McNemar** on discordant pairs | Secondary; report b, c and n |
| Both, split by `seg_occupation`, `beh_rapido_freq`, `seg_freq` | Descriptive + Fisher if cells ≥5 | Exploratory, labelled as such |

**Known limitation, stated on the slide:** Google Forms cannot randomise *section* order, so every
respondent sees P before Q. The forced choice (Q22, with shuffled options) is the primary outcome
precisely because it is less order-sensitive than two sequential ratings. The **fake-door page is the
properly randomised between-subjects version of this same test.**

---

# SECTION 8 — One more thing

**Section description:** *"Service P and Service Q are both descriptions of ideas. Now a real one:"*
> **Ownly** is the food-delivery service from **Rapido**, the bike-taxi and auto app.

| # | Var | Question | Type | Options | Req | Branch |
|---|---|---|---|---|---|---|
| Q25 | `own_aware_aided` | Before today, had you heard of Ownly? | MC | Yes, clearly · I think so · No | Yes | **No→S13** · else next |
| Q26 | `br_rapido_effect` | Does it being from **Rapido** make you more or less likely to try it? | MC | Much less likely · Somewhat less likely · No difference · Somewhat more likely · Much more likely | Yes | — |
| Q27 | `own_tried` | Have you ever placed an order on Ownly (Ownly app, or inside the Rapido app)? | MC | Yes → **S9** · No, but I've opened or browsed it → **S10** · No → **S10** | Yes | as shown |

*Purpose:* brand reveal comes **after** the blind proposition test so the brand cannot contaminate Q20–Q22.
Q25 gives awareness; Q25→Q27 gives the **awareness→trial conversion** (the say–do gap);
Q26 tests the Rapido distribution hypothesis directly.

---

# SECTION 9 — If you have used Ownly

| # | Var | Question | Type | Options | Req |
|---|---|---|---|---|---|
| Q28 | `own_discovery` | **NEW-v3** How did you first come across Ownly? | MC | Saw it inside the Rapido app · A friend or colleague told me · Social media · Advertising / poster / offer message · Search or app store · Can't remember | Yes |
| Q29 | `own_orders_4wk` | How many Ownly orders have you placed in the last 4 weeks? | MC | None · 1 · 2–3 · 4–7 · 8 or more | Yes |
| Q30 | `own_reliability_rating` | How often have your Ownly orders arrived on time? | MC | Rarely · Sometimes · About half the time · Mostly · Always | Yes |
| Q31 | `own_perceived_savings` | Compared with ordering the same thing on the app you'd otherwise use, your most recent Ownly order was: | MC | Much more expensive · A bit more expensive · About the same · A bit cheaper · Much cheaper · I didn't compare | Yes |
| Q32 | `own_repeat_no_promo` | **NEW-v3** If Ownly gave you **no discount, cashback or reward** on your next three orders, would you still use it? | MC | Definitely not · Probably not · Not sure · Probably · Definitely | Yes |
| Q33 | `own_next10_alloc` | **NEW-v3** Of your **next 10** delivery orders, roughly how many would be on Ownly? | MC | 0 · 1–2 · 3–4 · 5–6 · 7–8 · 9–10 | Yes |
| Q34 | `own_disappointment` | What, if anything, has disappointed you about Ownly? | Paragraph | — | **No** |

→ then **S13**.

*Purpose:* Q32 is the **retention-intent proxy** — the single most important question for the
*"price acquires, reliability retains"* proposition. Q33 gives **share of requirements**.
Q28 tests Rapido as a discovery channel with revealed rather than hypothetical data.

---

# SECTION 10 — If you have not used Ownly

| # | Var | Question | Type | Options | Req |
|---|---|---|---|---|---|
| Q35 | `own_not_tried_reason` | What are the main reasons you haven't ordered on it? *Select up to 3.* | Checkboxes · validation **at most 3** · **shuffle ON** | Happy with my current app · My usual restaurants weren't on it · Not available at my location · Didn't trust a new app yet · Expected slow or unreliable delivery · Didn't see real savings · No offers or discounts · The payment method I use (cash on delivery, meal card) isn't accepted · Didn't know how to access it · Haven't got round to it · Other | Yes |
| Q36 | `own_trigger_reward` | **NEW-v3** Would **₹100 off your first order** be enough to make you place one order on Ownly? | MC | No · Maybe · Yes | Yes |
| Q37 | `own_repeat_no_promo` | **NEW-v3** And if the three orders after that had **no discount or reward at all**, would you keep using it? | MC | Definitely not · Probably not · Not sure · Probably · Definitely | Yes |
| Q38 | `own_next10_alloc` | Of your **next 10** delivery orders, roughly how many would be on Ownly if it worked as described? | MC | 0 · 1–2 · 3–4 · 5–6 · 7–8 · 9–10 | Yes |

→ then **S13**.

*Purpose:* Q36 → Q37 is the **promotion diagnostic**: high Q36 with low Q37 means the reward buys trial,
not adoption — exactly the *"promotional acquisition, not durable product pull"* pattern.
`own_repeat_no_promo` and `own_next10_alloc` deliberately use the **same variable names** as S9 so triers
and non-triers pool into one retention-intent column with a `trier` flag.

---

# ══ BENGALURU PATH — BENCHMARK ══

# SECTION 11 — Ownly in Bengaluru

**Section description:** *"A few quick questions — Bengaluru is our reference market for this study."*

| # | Var | Question | Type | Options | Req | Branch |
|---|---|---|---|---|---|---|
| Q39 | `blr_occupation` | Which best describes you right now? | MC | Student · Working full-time · Studying and working · Other | Yes | — |
| Q40 | `blr_primary_app` | Which app do you use most for food delivery? | MC | Swiggy · Zomato · Ownly · Rapido app (food section) · Other | Yes | — |
| Q41 | `blr_own_tried` | **Have you ever ordered from Ownly?** | MC | Yes → **S11a** · No → **S11b** | Yes | as shown |

## SECTION 11a — Bengaluru, Ownly users

| # | Var | Question | Type | Options | Req |
|---|---|---|---|---|---|
| Q42 | `blr_discovery` | How did you first come across Ownly? | MC | Saw it inside the Rapido app · Friend or colleague · Social media · Advertising / offer message · Search or app store · Can't remember | Yes |
| Q43 | `blr_first_order_trigger` | What actually made you place that **first** order? | MC · shuffle ON | It looked cheaper overall · A discount or first-order offer · Curiosity about a new app · A friend recommended it · It was already there in Rapido · Something else | Yes |
| Q44 | `blr_savings_real` | Was the saving meaningful in practice? | MC | No — it worked out the same or more · Slightly cheaper · Clearly cheaper · It varied a lot · I never compared | Yes |
| Q45 | `blr_reliability_vs` | Compared with the app you'd otherwise use, Ownly's delivery has been: | MC | Much less reliable · Somewhat less reliable · About the same · Somewhat more reliable · Much more reliable | Yes |
| Q46 | `blr_assortment` | Were the restaurants you wanted available on it? | MC | Hardly any · A few · About half · Most · Nearly all | Yes |
| Q47 | `blr_status` | Which is true for you now? | MC | I use it as my main app · I use it alongside others · I've cut down a lot · I've stopped using it | Yes |
| Q48 | `blr_stop_reason` | If you cut down or stopped — why? | Short answer | — | **No** |
| Q49 | `blr_next10_alloc` | Of your **next 10** delivery orders, roughly how many would be on Ownly? | MC | 0 · 1–2 · 3–4 · 5–6 · 7–8 · 9–10 | Yes |
| Q50 | `blr_improve` | What would Ownly need to improve for you to use it more? | Short answer | — | **No** |

→ **S13**.

## SECTION 11b — Bengaluru, never used Ownly

| # | Var | Question | Type | Options | Req |
|---|---|---|---|---|---|
| Q51 | `blr_aware` | Before today, had you heard of Ownly? | MC | Yes, clearly · I think so · No | Yes |
| Q52 | `blr_not_tried_reason` | What's the main reason you haven't tried it? | MC · shuffle ON | Happy with my current app · My restaurants aren't on it · Didn't trust a new app · Expected unreliable delivery · Didn't see real savings · Payment method not accepted · Haven't got round to it · Other | Yes |
| Q53 | `blr_prop_reaction` | *"Same food, smaller final bill — the restaurant's own menu prices and one flat delivery fee, with no platform or packaging charges."* How likely would that make you try it? | MC | Definitely not · Probably not · Not sure · Probably · Definitely | Yes |

→ **S13**.

*Role of this branch:* it answers **"is our written definition of the Bengaluru playbook the one that
actually acquired and retained people there?"** Q43 vs Q47/Q49 is the Bengaluru version of
acquisition-vs-retention. **This branch is never pooled into the Hyderabad H₀.** With a realistic
n of 15–30 it is reported as **qualitative benchmark counts (raw n, no percentages under n=20)**.

---

# ══ OTHER CITY — SHORT EXPLORATORY ══

# SECTION 12

| # | Var | Question | Type | Options | Req |
|---|---|---|---|---|---|
| Q54 | `oth_city` | Which city? | Short answer | — | Yes |
| Q55 | `oth_primary_app` | Which app do you use most for food delivery? | MC | Swiggy · Zomato · Ownly · Rapido app (food section) · Magicpin · Other | Yes |
| Q56 | `oth_choice_driver` | What matters most in choosing it? | MC · shuffle ON | Lowest total price · Offers and discounts · Speed of delivery · Reliability — it turns up · Restaurant choice · Habit | Yes |
| Q57 | `oth_own_aware` | Before today, had you heard of Ownly? | MC | Yes, clearly · I think so · No | Yes |
| Q58 | `oth_prop_reaction` | *"Same food, smaller final bill — the restaurant's own menu prices and one flat delivery fee, no platform or packaging charges."* How likely would that make you try it? | MC | Definitely not · Probably not · Not sure · Probably · Definitely | Yes |

→ **S13**. *Role:* appendix context only. **Never** used for Hyderabad validation, Hyderabad demand,
or Bengaluru benchmarking. If recruitment time is tight, do not chase these respondents.

---

# SECTION 13 — Last question *(all paths)*

| # | Var | Question | Type | Options | Req |
|---|---|---|---|---|---|
| Q59 | `meta_found_survey` | Where did you find this survey? | MC | WhatsApp / Telegram group · LinkedIn · Instagram · Reddit · A friend or colleague sent it · College or office group · Other | Yes |

→ **SUBMIT.** *Purpose:* channel-level recruitment funnel (starts → eligible → complete per channel),
which is how we apply the course's digital-funnel KPI definitions to our own data honestly.

---

# SECTION 0 — Not eligible *(END)*

**Description:** *"Thank you for your time. This survey is for people aged 20–30 who ordered food delivery through an app in the last 4 weeks."* → **Submit.**
**Do not delete these responses** — they are the denominator of the recruitment funnel.

---

# Question → KPI / hypothesis map

| KPI or metric | Built from |
|---|---|
| Ownly awareness (Hyderabad) | Q25 |
| Ownly trial penetration | Q27 |
| **Awareness → trial conversion (say–do gap)** | Q27 ÷ Q25 |
| **First-order intent, P vs Q** — *primary H₀* | **Q22**, supported by Q20/Q21 |
| Repeat-without-promo intent *(retention proxy)* | Q32 / Q37 pooled, with `trier` flag |
| Share of requirements | Q33 / Q38 |
| Self-reported fee share of bill | (Q9 − Q10) ÷ Q9 |
| Switching threshold vs observed audit saving | Q19 vs audit median gap |
| Price-vs-reliability trade-off | Q17 |
| Price-vs-assortment trade-off | Q18 |
| Price-vs-speed trade-off | Q16 |
| Rapido distribution effect | Q7 × Q25, Q26, Q28 |
| Promotion diagnostic (trial vs durable pull) | Q36 → Q37 |
| Price-durability scepticism | Q24 |
| Offer dependency | Q13, Q12 |
| Segment comparison (student vs professional) | Q6 × everything |
| Bengaluru benchmark: what acquired vs what retained | Q43 vs Q47/Q49 |

# Items deliberately cut from the v2 short survey, and why
| Cut | Reason |
|---|---|
| `beh_unaided_apps` (open text) | Needs human coding we have no time for |
| `dem_living`, `beh_last_meal` | Nice-to-have; no hypothesis depends on them |
| `bill_s1` (equal-total bill pair) | Superseded by Section 7, which tests the same transparency-vs-amount idea with a decision attached |
| `exp_eta_max_dinner`, `exp_fav_restaurant_needed` | The Q16/Q18 trade-offs measure the same thing with a real trade attached |
| `pain_menu_markup_belief` | The audit measures markup with observed data; belief adds little |
| `wtp_max_fee_direct` | Q19 (switching threshold) is the decision-relevant version |
| Full choice experiment, fee staircase, brand-arm randomisation | Need n ≥ 125 (decision of 2026-09-14, unchanged) |
