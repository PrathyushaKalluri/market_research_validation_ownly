# Metric Dictionary: P0 and P1 KPIs

**Version:** 1.0 · 2026-09-16 · Pairs with `kpi_data_coverage.csv` (IDs match) and `calculation_spec.md` (code-level rules).

**The 13 fields for each metric:**
1. Definition
2. Formula
3. Example
4. Source
5. Evidence level
6. Denominator
7. Cuts
8. Bias
9. High means
10. Low means
11. Decision
12. Panel
13. Priority, shown in the heading

**Examples are illustrative arithmetic, not results.** No primary data exists yet.

**Evidence levels:**
- **Observed:** our audit or experiment measured it.
- **Self-reported behaviour:** survey counts of past actions.
- **Stated:** a hypothetical choice or intent.
- **Association:** a cross-tab; not causal.
- **External:** reported by a third party.

**Eligible respondent:** aged 20–30, city Hyderabad or Bengaluru, and passed the age screen.

---

## Layer 0 · Outcome

### K00 · Repeat-active Ownly customers per 100 delivery users ★ project north-star proxy · P0
- **Definition:** out of every 100 young people who order food online, how many used Ownly in the last 4 weeks *and* have ordered on it at least twice in 8 weeks.
- **Formula:** `count(S4-Q3 ≥ 1 AND S4-Q3 + S12-Q4 ≥ 2) ÷ count(eligible AND S3-Q3 = Yes) × 100`
- **Example:** 11 qualifying respondents out of 92 recent orderers = **12.0 per 100** (Wilson 95% CI 6.8–20.1).
- **Source:** survey v6: S3-Q3, S4-Q3, S12-Q4.
- **Evidence level:** self-reported behaviour.
- **Denominator:** eligible respondents who ordered food online in the last 4 weeks.
- **Cuts:** city, student/professional, Rapido user (A1), member.
- **Bias:** a convenience sample skewed towards food-app users inflates it; recall error on counts; Hyderabad is only ~1 month old, which caps it.
- **High means:** Ownly converts reach into habit in this segment.
- **Low means:** either trial is low (check K01) or repeat is low (check K30). The two cases need different fixes.
- **Decision:** the overall transferability call, always read against guardrails G1–G4.
- **Panel:** Page 1 hero tile; Page 4.

### K01 · Trial penetration · P0
- **Definition:** share of eligible respondents who have ever ordered on Ownly (course: brand penetration).
- **Formula:** `count(S8-Q1 = "I've ordered on Ownly") ÷ count(eligible)`
- **Example:** 22 / 110 = **20.0%** (CI 13.6–28.4).
- **Source:** S8-Q1.
- **Evidence level:** self-reported behaviour.
- **Denominator:** all eligible respondents.
- **Cuts:** city, occupation, Rapido user, member.
- **Bias:** the sample over-represents food-app-engaged people. Report Poll A's unscreened figure next to it; never merge the two.
- **High means:** the acquisition engine works.
- **Low means:** there is a reach or first-order barrier (check K10, K11).
- **Decision:** whether to invest in acquisition or conversion.
- **Panel:** Page 1 card; Page 3 funnel.

---

## Layer 1 · Acquisition

### K10 · Awareness · P0
- **Definition:** share who had heard of Ownly before taking the survey.
- **Formula:** `count(S8-Q1 ≠ "I hadn't heard of Ownly") ÷ count(eligible)`
- **Example:** 64 / 110 = **58.2%**.
- **Source:** S8-Q1.
- **Evidence level:** self-reported.
- **Denominator:** eligible.
- **Cuts:** city, Rapido user, occupation.
- **Bias:** people who open a food survey are more aware than the population. The gap to Poll A is itself a finding.
- **High means:** reach is not the constraint.
- **Low means:** GTM must buy reach before optimising the message.
- **Decision:** the reach vs conversion budget split.
- **Panel:** Page 1 card; Page 3 funnel; Page 7.

### K11 · Awareness → trial conversion · P0
- **Definition:** of those who know Ownly, share who have ordered.
- **Formula:** `count(ordered) ÷ count(aware)`
- **Example:** 22 / 64 = **34.4%** (CI 24.0–46.5).
- **Source:** S8-Q1.
- **Evidence level:** self-reported.
- **Denominator:** aware respondents.
- **Cuts:** city, Rapido user, occupation.
- **Bias:** in Hyderabad, recently aware people have had little time to try it.
- **High means:** the proposition converts once seen.
- **Low means:** a barrier sits between awareness and trial (K16).
- **Decision:** fix the barriers first, or scale awareness.
- **Panel:** Page 3 funnel; Page 4.

### K12 · Browse → order conversion · P1
- **Definition:** of those who opened Ownly, share who ordered.
- **Formula:** `count(ordered) ÷ count(opened OR ordered)`
- **Example:** 22 / 35 = **62.9%**.
- **Source:** S8-Q1.
- **Evidence level:** self-reported.
- **Denominator:** respondents who opened or ordered.
- **Cuts:** city.
- **Bias:** small base.
- **High means:** the in-app experience converts.
- **Low means:** in-app barriers (see K16, S11-Q2).
- **Decision:** whether to fix what users see inside the app first.
- **Panel:** Page 3 funnel.

### K13 · H₀ fake-door CTA conversion by arm · P0
- **Definition:** share of unique visitors who tapped the call to action, for Variant A (Bengaluru-style total price) and Variant B (Hyderabad local + reliable).
- **Formula:** `visitors with cta_click ÷ unique visitors`, per arm. Lift = `B − A` in pp, and `B/A − 1` relative.
- **Example:** A 18/52 = 34.6%; B 24/50 = 48.0%. Lift **+13.4pp** (relative +38.7%); Fisher p = 0.23.
- **Source:** fake-door events (`variant_id`, `event_name`), excluding `is_qa` and `is_bot_suspect`.
- **Evidence level:** observed intent (a click, not an order).
- **Denominator:** unique eligible visitors per arm.
- **Cuts:** utm_source; mini-survey occupation.
- **Bias:**
  - Channel mix may differ by arm, so run a sample-ratio check.
  - Every visitor sees the research disclosure only after the click.
  - Low traffic.
- **High means:** that proposition wins first-order intent.
- **Low means:** no winner, or the other arm wins.
- **Decision:** reject or fail to reject H₀, and choose the lead proposition. Primary **only if ≥ 80 visitors and ≥ 30 per arm** (D3).
- **Panel:** Page 1 banner.

### K14 · H₀ survey forced choice: Service Q share · P0
- **Definition:** share choosing Service Q (localized: regulars + reliability) among people who chose P or Q.
- **Formula:** `count(S7-Q3 = Q) ÷ count(S7-Q3 ∈ {P, Q})`. "Can't choose" is reported separately.
- **Example:** 49 / 86 = **57.0%** (CI 46.4–66.9); exact binomial p = 0.24, so **H₀ is not rejected**.
- **Source:** S7-Q3.
- **Evidence level:** stated preference.
- **Denominator:** people who chose P or Q.
- **Cuts:** occupation, member, Rapido user, price-first (K24).
- **Bias:** Forms cannot randomise section order, so P is always read first. The shuffled options mitigate order effects only partly.
- **High means:** the localized proposition is preferred.
- **Low means:** the Bengaluru-style price proposition is preferred.
- **Decision:** the H₀ call when the fake door is under-powered; the lead message for Hyderabad.
- **Panel:** Page 1 banner.

### K15 · Stated trial intent, P vs Q (top-2 box) · P1
- **Definition:** share answering Probably or Definitely for trying each service.
- **Formula:** `share(S7-Q1 ∈ top-2)` vs `share(S7-Q2 ∈ top-2)`
- **Example:** P 61% vs Q 68%; McNemar exact p = 0.19.
- **Source:** S7-Q1, S7-Q2.
- **Evidence level:** stated.
- **Denominator:** respondents answering both.
- **Cuts:** occupation.
- **Bias:** intent overstates action.
- **High means:** broad appeal.
- **Low means:** weak pull.
- **Decision:** confidence in the direction of the H₀ result.
- **Panel:** Page 1 drill-down; Page 4.

### K16 · First-order barrier incidence by stage · P1
- **Definition:** main reason for not opening (S10-Q2), or for not ordering after opening (S11-Q2).
- **Formula:** `share per option` within each stage.
- **Example:** "Happy with my current app or membership" 31% of never-opened.
- **Source:** S10-Q2, S11-Q2.
- **Evidence level:** stated.
- **Denominator:** respondents at that stage.
- **Cuts:** city, occupation.
- **Bias:** only one main reason is captured.
- **High means (for an option):** that barrier dominates.
- **Low means:** no single blocker.
- **Decision:** which acquisition barrier to attack.
- **Panel:** Page 3; Page 4 left.

### K17 · Trial-trigger ranking among the unaware · P1
- **Definition:** the single thing that would most make a non-aware person try Ownly.
- **Formula:** `share per option, S9-Q1`
- **Example:** "Seeing it's cheaper than Swiggy/Zomato" 26%.
- **Source:** S9-Q1.
- **Evidence level:** stated.
- **Denominator:** unaware respondents.
- **Cuts:** occupation.
- **Bias:** stated; a description of Ownly is shown just before the question.
- **High means:** that lever should lead first-order messaging.
- **Low means:** that lever is not what gets the first order.
- **Decision:** first-order message.
- **Panel:** Page 4 left.

---

## Layer 2 · Value / affordability

### K20 · Median matched-basket saving % vs the cheaper incumbent · P0 · Guardrail G1
- **Definition:** for the same restaurant, basket and time slot, how much less the Ownly final bill is than the cheaper of Swiggy and Zomato.
- **Formula:** for each matched set, `(min(Swiggy, Zomato final_payable) − Ownly final_payable) ÷ min(Swiggy, Zomato)`; take the median across sets.
- **Example:** Swiggy ₹412, Zomato ₹398, Ownly ₹341, so the saving is ₹57 (**14.3%**). Median across 20 sets 11.8%, bootstrap CI 6.1–16.4.
- **Source:** audit captures (`final_payable`, matched on slot + restaurant_name + basket_id).
- **Evidence level:** observed.
- **Denominator:** matched sets where all three platforms list the restaurant.
- **Cuts:** slot, chain/local.
- **Bias:**
  - Single drop point.
  - Account state and coupons vary.
  - n ≤ 20 sets.
  - A negative value means Ownly is dearer.
- **High means:** affordability is a real, repeatable advantage.
- **Low means:** the price claim is messaging, not reality.
- **Decision:** KEEP/ADAPT/DROP price as the lead claim.
- **Panel:** Page 1 card; Page 5 waterfall.

### K21 · Ownly win rate · P1
- **Definition:** share of matched sets where Ownly is cheapest by more than ₹5.
- **Formula:** `count(Ownly < cheaper incumbent − 5) ÷ matched sets`
- **Example:** 15 / 20 = **75%**.
- **Source:** audit.
- **Evidence level:** observed.
- **Denominator:** matched sets.
- **Cuts:** slot.
- **Bias:** small n.
- **High means:** the advantage is consistent.
- **Low means:** it is occasional.
- **Decision:** whether the price claim can be repeated.
- **Panel:** Page 5.

### K22 · Fee load % · P1
- **Definition:** fees as a share of the final bill.
- **Formula:** `(packaging + platform + delivery + small_cart + surge) ÷ final_payable`, median per platform.
- **Example:** Swiggy 17%, Zomato 15%, Ownly 8%.
- **Source:** audit.
- **Evidence level:** observed.
- **Denominator:** captures with a final payable.
- **Cuts:** platform, slot.
- **Bias:** taxes excluded; discounts are shown separately.
- **High means (on incumbents):** the no-fee message has substance.
- **Low means:** there is little fee gap to promise.
- **Decision:** KEEP/ADAPT the "no fees" message.
- **Panel:** Page 5 fee stack.

### K23 · Switching-threshold coverage · P1
- **Definition:** share whose stated required saving is at or below the saving Ownly actually delivers.
- **Formula:** `count(S6-Q4 ₹ ≤ K20 median ₹) ÷ count(S6-Q4 numeric)`. "No amount" and "don't know" are shown separately.
- **Example:** median saving ₹48, so thresholds of ₹10/20/30 count; 38 / 70 = **54%**.
- **Source:** S6-Q4 × audit.
- **Evidence level:** stated × observed.
- **Denominator:** numeric answers.
- **Cuts:** occupation.
- **Bias:** stated threshold.
- **High means:** the real saving is enough to switch most people.
- **Low means:** the saving alone won't move people.
- **Decision:** whether price can lead.
- **Panel:** Page 5.

### K24 · ₹30 trade-off shares · P0
- **Definition:** share taking ₹30 off in exchange for 15 minutes slower (S6-Q1), 3-in-10 late instead of 1-in-10 (S6-Q2), or few of their usual restaurants (S6-Q3).
- **Formula:** `share choosing ₹230`, per item.
- **Example:** speed 58%, reliability 36%, restaurants 31%.
- **Source:** S6-Q1..Q3.
- **Evidence level:** stated choice.
- **Denominator:** answered.
- **Cuts:** occupation, member, frequent user.
- **Bias:** one price point; hypothetical.
- **High means (above 50%):** price beats that attribute.
- **Low means (below 50%):** that attribute beats ₹30.
- **Decision:** lead with price, or with reliability/supply; tests "price gets the first order, reliability the second".
- **Panel:** Page 3; Page 4.

### K25 · Fee pain on the last bill · P1
- **Definition:** share saying the extra charges on their last order were too much.
- **Formula:** `count(S5-Q4 = "No, the extra charges on top were too much") ÷ answered`
- **Example:** 35%.
- **Source:** S5-Q4.
- **Evidence level:** self-reported perception.
- **Denominator:** recent orderers.
- **Cuts:** member, occupation.
- **Bias:** anchored on one order.
- **High means:** the no-fee promise addresses a felt pain.
- **Low means:** fees are not top of mind.
- **Decision:** how prominent the no-fee message should be.
- **Panel:** Page 3; Page 5.

---

## Layer 3 · Retention

### K30 · Trier repeat rate · P0
- **Definition:** of everyone who has ordered on Ownly, share with at least 2 Ownly orders in the last 8 weeks.
- **Formula:** `count(S4-Q3 + S12-Q4 ≥ 2) ÷ count(ordered)`
- **Example:** 13 / 22 = **59%**.
- **Source:** S4-Q3, S12-Q4, S8-Q1.
- **Evidence level:** self-reported behaviour.
- **Denominator:** triers.
- **Cuts:** offer first order (A2), failure (A3), city.
- **Bias:** an older trier whose first order predates the 8-week window with no recent orders counts as not repeating, which is intended.
- **High means:** the second order is earned.
- **Low means:** trial doesn't stick.
- **Decision:** GTM focus on retention vs acquisition.
- **Panel:** Page 1; Page 4 right.

### K31 · Still-ordering rate, Bengaluru cohort · P1
- **Definition:** of users whose first order was more than 4 weeks ago, share who ordered in the last 4 weeks (course retention rate, as a proxy).
- **Formula:** `count(S12-Q3 = earlier AND S4-Q3 > 0) ÷ count(S12-Q3 = earlier)`
- **Example:** 21 / 34 = 62%.
- **Source:** S12-Q3, S4-Q3.
- **Evidence level:** self-reported.
- **Denominator:** earlier triers.
- **Cuts:** A2, A3.
- **Bias:** in Hyderabad the base is about 0 by construction; survivor bias.
- **High means:** Bengaluru retention holds.
- **Low means:** Bengaluru churn is a warning for Hyderabad.
- **Decision:** the benchmark for what retention looks like where the playbook ran.
- **Panel:** Page 2.

### K32 · Repeat-without-promo intent · P0
- **Definition:** share who'd keep using the service they picked once a ₹100 first-order offer ends.
- **Formula:** `count(S7-Q5 ∈ {Probably, Definitely}) ÷ answered`
- **Example:** 44%.
- **Source:** S7-Q5.
- **Evidence level:** stated.
- **Denominator:** answered.
- **Cuts:** P vs Q choosers, occupation.
- **Bias:** top-2 box inflates.
- **High means:** demand survives the subsidy.
- **Low means:** promo-rented demand.
- **Decision:** promotion KEEP/MODIFY (read against K15).
- **Panel:** Page 1 card; Page 8.

### K33 · Unit share of requirements · P0
- **Definition:** among people who ordered on Ownly in the last 4 weeks, Ownly's share of their delivery orders.
- **Formula:** `Σ S4-Q3 ÷ Σ(S4-Q1..Q4)` over respondents with S4-Q3 > 0.
- **Example:** 58 Ownly orders out of 171 = **33.9%**.
- **Source:** S4.
- **Evidence level:** self-reported behaviour.
- **Denominator:** all orders by Ownly buyers.
- **Cuts:** occupation, member.
- **Bias:** heavy users dominate a ratio of sums; counts are recalled.
- **High means:** Ownly is becoming a main app.
- **Low means:** it is a side app used for occasional deals.
- **Decision:** position Ownly as a main app or an occasional deal app.
- **Panel:** Page 1 card; Page 3.

### K34 · PMF score · P1
- **Definition:** share of users who'd be very disappointed without Ownly.
- **Formula:** `count(S12-Q6 = Very disappointed) ÷ answered`
- **Example:** 31%.
- **Source:** S12-Q6.
- **Evidence level:** stated.
- **Denominator:** Ownly users.
- **Cuts:** city.
- **Bias:** the 40% bar is a rule of thumb.
- **High means:** strong product-market fit.
- **Low means:** users could live without it.
- **Decision:** confidence in the proposition.
- **Panel:** Page 4.

### K35 · Incumbent substitution · P1
- **Definition:** share of Ownly orders that would otherwise have gone to Swiggy or Zomato.
- **Formula:** `count(S12-Q5 = "Ordered the same on Swiggy or Zomato") ÷ answered`
- **Example:** 55%.
- **Source:** S12-Q5.
- **Evidence level:** stated counterfactual.
- **Denominator:** users.
- **Cuts:** occupation.
- **Bias:** recall.
- **High means:** Ownly is taking share from incumbents.
- **Low means:** Ownly creates new ordering occasions, which fits Rapido's "100M people" thesis.
- **Decision:** the expansion vs share-steal narrative.
- **Panel:** Page 4.

### K36 · One-change and drop-off drivers · P1
- **Definition:** the single change that would increase ordering (S12-Q7); the Bengaluru reason for ordering less (S23).
- **Formula:** `share per option`
- **Example:** "More reliable, on-time delivery" 24%.
- **Source:** S12-Q7, S23.
- **Evidence level:** stated.
- **Denominator:** users.
- **Cuts:** city.
- **Bias:** single choice.
- **High means (for an option):** that is the main retention lever.
- **Low means:** the retention levers are diffuse.
- **Decision:** the retention roadmap.
- **Panel:** Page 4 right.

---

## Layer 4 · Supply

### K40 · Target-restaurant coverage · P0 · Guardrail G3
- **Definition:** share of the 10 audit-frame restaurants that are listed on Ownly.
- **Formula:** `count(on_ownly = yes) ÷ 10`
- **Example:** 6 / 10 = **60%**. Report it as k/n; a CI is too wide to be useful.
- **Source:** restaurant frame.
- **Evidence level:** observed.
- **Denominator:** the frame.
- **Cuts:** chain/local.
- **Bias:** the frame was chosen by us; n = 10.
- **High means:** supply supports trial.
- **Low means:** fix supply before buying acquisition.
- **Decision:** supply-first vs demand-first.
- **Panel:** Page 1 card; Page 6.

### K41 · Local vs chain coverage gap · P1
- **Definition:** local coverage minus chain coverage.
- **Formula:** `coverage(local) − coverage(chain)`
- **Example:** local 2/4 − chain 4/6 = −17pp.
- **Source:** frame.
- **Evidence level:** observed.
- **Denominator:** frame by type.
- **Cuts:** none.
- **Bias:** n = 10.
- **High (positive) means:** the localisation premise is already met.
- **Low (negative) means:** local supply must be built first.
- **Decision:** Service Q feasibility.
- **Panel:** Page 6.

### K42 · Cross-platform availability overlap · P1
- **Definition:** when a restaurant is listed and open on an incumbent, share of the time it is also listed and open on Ownly.
- **Formula:** `count(open on Ownly AND on ≥1 incumbent) ÷ count(open on ≥1 incumbent)`
- **Example:** 14 / 20 = 70%.
- **Source:** audit `restaurant_listed`, `restaurant_open`.
- **Evidence level:** observed.
- **Denominator:** captures open on an incumbent.
- **Cuts:** slot.
- **Bias:** snapshot at two slots.
- **High means:** listings translate into real availability.
- **Low means:** listed restaurants are often closed or offline on Ownly.
- **Decision:** operational supply fix.
- **Panel:** Page 6.

### K43 · "My restaurants weren't there" barrier share · P1
- **Definition:** among people who opened Ownly but didn't order, share naming missing restaurants as the main reason.
- **Formula:** `count(S11-Q2 = "My restaurants weren't there") ÷ answered`
- **Example:** 29%.
- **Source:** S11-Q2.
- **Evidence level:** stated.
- **Denominator:** opened, didn't order.
- **Cuts:** city.
- **Bias:** small base.
- **High means:** users feel the supply gap.
- **Low means:** assortment isn't blocking first orders.
- **Decision:** supply priority.
- **Panel:** Page 6.

---

## Layer 5 · Fulfilment

### K50 · ETA gap · P0
- **Definition:** difference in shown delivery time between Ownly and the cheaper incumbent, for the same set.
- **Formula:** median of `Ownly eta_mid − cheaper incumbent eta_mid`, where `eta_mid = (min + max) ÷ 2`
- **Example:** Ownly 42 vs Zomato 33 = **+9 minutes**.
- **Source:** audit.
- **Evidence level:** observed (*shown* ETA).
- **Denominator:** matched sets with ETAs.
- **Cuts:** slot.
- **Bias:** a shown ETA is not the actual delivery time.
- **High (above 0) means:** Ownly is slower, so the ₹30-for-speed trade (K24) is live.
- **Low (0 or below) means:** there is no speed penalty.
- **Decision:** whether ETA blocks the price proposition.
- **Panel:** Page 1 card; Page 5.

### K51 · Fulfilment failure incidence among triers · P0 · Guardrail G2
- **Definition:** share of Ownly users reporting at least one of: 15+ minutes late, cancelled or not delivered, missing or wrong item, refund or support taking more than 2 days.
- **Formula:** `count(A3 ≠ "None of these") ÷ answered`
- **Example:** 9 / 22 = **41%**.
- **Source:** **new question A3**.
- **Evidence level:** self-reported.
- **Denominator:** Ownly users.
- **Cuts:** city.
- **Bias:** users with more orders have more chances to experience a failure.
- **High means:** reliability is a real risk to repeat use.
- **Low means:** operations support the promise.
- **Decision:** ADAPT (lead with and fix reliability) vs KEEP.
- **Panel:** Page 1 card; Page 6.

### K52 · Repeat rate by failure experience · P1
- **Definition:** K30 among users with no failures minus K30 among users with at least one failure.
- **Formula:** `K30(A3 = none) − K30(A3 = any)`
- **Example:** 75% − 44% = **+31pp**; Fisher p = 0.19.
- **Source:** A3 × S4/S12.
- **Evidence level:** association.
- **Denominator:** users.
- **Cuts:** pooled across cities if cells are small.
- **Bias:** reverse causality: heavy users both repeat more and experience more failures, which *understates* the gap.
- **High means:** reliability earns the second order.
- **Low means:** failures aren't driving churn.
- **Decision:** the retention lever.
- **Panel:** Page 4.

---

## Layer 6 · Distribution

### K60 · Rapido usage penetration · P1
- **Definition:** share who used Rapido in the last 4 weeks.
- **Formula:** `count(A1 ≠ Never) ÷ eligible`
- **Example:** 64%.
- **Source:** **new question A1**.
- **Evidence level:** self-reported.
- **Denominator:** eligible.
- **Cuts:** occupation.
- **Bias:** none beyond sampling.
- **High means:** a large cross-sell base.
- **Low means:** Rapido gives little distribution leverage.
- **Decision:** Rapido cross-sell priority.
- **Panel:** Page 7.

### K61 · Awareness and trial gap, Rapido users vs non-users · P1
- **Definition:** K10 and K01 among Rapido users, minus the same among non-users.
- **Formula:** `K(A1 ≠ Never) − K(A1 = Never)`
- **Example:** awareness 66% vs 44% = **+22pp**.
- **Source:** A1 × S8.
- **Evidence level:** association.
- **Denominator:** each group.
- **Cuts:** city.
- **Bias:** Rapido users may simply be more app-savvy. **Public sources say Rapido-app integration is Bengaluru-only.**
- **High means:** consistent with a distribution advantage.
- **Low means:** no advantage visible.
- **Decision:** KEEP/ADAPT Rapido cross-sell.
- **Panel:** Page 7.

### K62 · Discovery via the Rapido app · P1
- **Definition:** share of aware respondents who first heard of Ownly inside the Rapido app.
- **Formula:** `count(first heard = "Inside the Rapido app") ÷ answered`
- **Example:** 34%.
- **Source:** S10/S11/S12-Q1.
- **Evidence level:** self-reported.
- **Denominator:** aware.
- **Cuts:** city.
- **Bias:** first-touch recall.
- **High means:** in-app placement is doing the work.
- **Low means:** other channels drive discovery.
- **Decision:** Hyderabad channel mix.
- **Panel:** Page 7.

---

## Layer 7 · Promotion

### K70 · Offer-triggered first order · P1
- **Definition:** share of users whose first Ownly order used a discount or offer.
- **Formula:** `count(A2 ∈ Yes options) ÷ count(A2 answered, excluding "Don't remember")`
- **Example:** 15 / 20 = 75%.
- **Source:** **new question A2**.
- **Evidence level:** self-reported.
- **Denominator:** users.
- **Cuts:** city, occupation.
- **Bias:** recall.
- **High means:** trial is subsidised.
- **Low means:** trial is organic.
- **Decision:** how much trial depends on promotion.
- **Panel:** Page 8.

### K71 · Promo-dependency gap · P0 · Guardrail G4
- **Definition:** repeat rate of organic triers minus repeat rate of offer-acquired triers.
- **Formula:** `K30(A2 = No) − K30(A2 = Yes)` in pp.
- **Example:** 80% − 53% = **+27pp**.
- **Source:** A2 × S4/S12.
- **Evidence level:** association.
- **Denominator:** users with A2 answered.
- **Cuts:** pooled if cells are small.
- **Bias:** offer users may be more price-sensitive, so the gap is not the causal effect of the offer.
- **High means:** promos rent demand that doesn't stay.
- **Low means:** promo-acquired users retain like organic ones.
- **Decision:** promotion KEEP / MODIFY / TARGET / DEPRIORITIZE.
- **Panel:** Page 8.

### K72 · Discount as top trial trigger · P1
- **Definition:** share of unaware respondents picking "A discount on my first order".
- **Formula:** `count ÷ S9-Q1 answered`
- **Example:** 22%.
- **Source:** S9-Q1.
- **Evidence level:** stated.
- **Denominator:** unaware.
- **Cuts:** occupation.
- **Bias:** stated.
- **High means:** promo pull is strong.
- **Low means:** proof of lower prices matters more.
- **Decision:** promo vs price-proof message.
- **Panel:** Page 8.

### K74 · Fake-door bill-compare rate · P1
- **Definition:** share of unique visitors completing the bill comparison.
- **Formula:** `visitors with secondary_intent ÷ unique visitors`, per arm.
- **Example:** A 12%, B 9%.
- **Source:** fake door.
- **Evidence level:** observed intent.
- **Denominator:** visitors per arm.
- **Cuts:** arm.
- **Bias:** low traffic.
- **High means:** price proof engages visitors.
- **Low means:** price proof is ignored.
- **Decision:** whether to use bill-comparison creative.
- **Panel:** Page 1 drill-down; Page 7.

---

## Layer 9 · Context (P1 only)

### K92 · Sample volume-share proxy · P1
- **Definition:** Ownly's share of all delivery orders placed by every recent orderer.
- **Formula:** `Σ S4-Q3 ÷ Σ S4-Q1..Q4`, all orderers.
- **Example:** 58 / 640 = 9.1%.
- **Source:** S4.
- **Evidence level:** self-reported.
- **Denominator:** all orders.
- **Cuts:** city.
- **Bias:** a sample, not the market. **Never compare it directly with the reported Bengaluru "~10%" share.**
- **High means:** early traction in the sample.
- **Low means:** little share in the sample so far.
- **Decision:** context on scale.
- **Panel:** Page 3.

### K94 · Market penetration (sample) · P1
- **Definition:** share of eligible respondents who ordered food online in the last 4 weeks.
- **Formula:** `count(S3-Q3 = Yes) ÷ eligible`
- **Example:** 84%.
- **Source:** S3-Q3.
- **Evidence level:** self-reported.
- **Denominator:** eligible.
- **Cuts:** occupation.
- **Bias:** a food survey attracts people who order food.
- **High means:** the category is mature in this segment.
- **Low means:** room to grow the category itself.
- **Decision:** denominator for K00; context.
- **Panel:** Page 3.
