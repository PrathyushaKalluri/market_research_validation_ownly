# Ownly Gachibowli — Fake-Door Experiment Design

**Version 7.0 · 2026-09-23 · pre-registration draft**

**v12 change.** Every typed query is now logged on a pause, so **abandoned searches survive** — until
now a word was only kept if the participant selected something from it (§6.0). A missing **dish** now
gets the same treatment a missing place already had: an explicit ask, its own event, and its own
question, because a missing dish is a menu problem while a missing place is an onboarding problem
(§6.1).

**v11 change.** The restaurant search moved to the **front of the journey**, alongside the dish
search, as a second box with its own event stream (§6). It had been buried after the debrief as a
post-hoc demand list — wrong place for the thing the study exists to measure. Every selection now
carries its **type** (cuisine, and local vs chain), because the finding is what *kind* of food and
place people reach for, not which exact ones (§6.1). The four-screen ending collapsed to **one
118-word screen with a deletion code** (§6.2).

**v10 change.** The payment section is rebuilt on verified evidence (§7.4), and an earlier claim in
this document is corrected: bill transparency is **not** settled — `bill_s1` was designed and never
fielded — so it is scoped out deliberately rather than dismissed. Order Protection's price is now
**randomised**, making the #2 stated trial trigger in the survey the subject of a willingness-to-pay
curve for the first time.

**v9 change.** The payment section was rebuilt (§7.4). v7 pitted an "itemised bill" against a
"single price" that was ₹10 cheaper — a decided choice, testing a screen no app shows, for a question
the survey had already answered (22 of 59 said their last bill's extra charges were too much). It now
asks the open question instead: Ownly charges nothing today, so **what will people accept being
charged for** — a per-order fee, a third subscription, or a refund guarantee that survey Q26 ranked
second among reasons to try Ownly and that nothing has tested behaviourally.

**v8 change.** The coupons were rebuilt (§7.3). v7's *"every 5th order free"* and *"₹75 off your next
3 orders"* asked people to bet on future orders from an app they had never used and then remember
doing so — not offers anyone would want, and rigged toward "cash wins" before anyone tapped. They are
replaced by three offers real apps actually run, one of which is a **randomised wallet amount** that
applies itself, so the point where money-later beats money-now is measured rather than assumed.

**v7 changes.** Three behaviours — delivery, offer, payment — are now measured **independently**
(§7.1): delivery moves to its own screen before any total is visible, no coupon touches delivery, and
all three payment models charge the same delivery fee. The fast-delivery price is **randomised per
participant** so take-up traces a demand curve instead of yielding one uninterpretable number (§7.2).
Offers are four promotional *logics*, food-discount only (§7.3). The payment choice became a
transparency test with the cheaper option being the opaque one (§7.4). And **all internal
justification text was removed from the participant-facing UI** (§7.5) — v6 printed audit provenance
under the delivery options, which told participants what was being measured.

**v6 changes.** Delivery now comes **before** the pricing choice, so the fee is a real consequence
the pricing models handle rather than a number that vanishes (§7.3). The bill opens as an
**accordion under the selected pricing option** instead of sitting at the foot of the page (§7.2).
The bundled option's **markup is no longer itemised** — no real app shows it, and showing it killed
the choice (§7.2). And **every delivery fee and ETA is now traced to `task 3.3.xlsx`** (§7.3): v5's
₹10-for-14-minutes was invented and was not a trade-off anyone would weigh.

**v5 change.** The offer question moved from the home screen to the cart (§7.1). v4 asked which
offer you noticed — meaningless once all four were visible in a grid — and asked it on a tap nobody
makes, mid-task. Offers are now four priced coupons against the participant's own basket, one of
which is worth ₹0 today and unlocks a local kitchen instead. The home grid stays as the arm
manipulation and fires no question at all.

**v4 changes, in one line each.** The journey now runs to a real cart and a real bill (§6) — a fake
door that stops at "I'd like this" only ever measures interest. Three **pricing models** are offered
over the same basket as a within-subject discrete choice, one of which is the fielded survey's
Service P made payable instead of imagined (§7.2). A **Rapido-linked delivery option** is tested —
the one thing Ownly could build that Swiggy and Zomato structurally cannot (§7.3). Offers moved from
a carousel to a **2×2 grid**, because v3 asked which offer you saw while three of the four were off
screen. The offer follow-up is now **arm-aware**: v3 offered "the food it was about" as a reason for
tapping "₹100 OFF". The **filter tabs work** — v3's decorative "See all" did nothing, and dead
affordances teach participants the prototype is fake. Delivery time is now a **white box bottom-right
of the restaurant image**, the shape a Swiggy user reads without thinking.

**v3 changes, in one line each.** The goal narrowed to dish and restaurant preference discovery (§3).
The end-of-session questionnaire was deleted and replaced by eight questions that fire in the moment
of each choice (§13). Ethics-check and segment questions left the instrument — the protections stay,
the segment items move to the screening sheet (§13.2, §13.4). The home screen now carries loud,
number-led offers and delivery-time badges, so a question about an offer is answerable (§6).
Source of truth: `CASE_STUDY_Ownly_Hyderabad.md`. No finding in this document extends beyond what
that file supports.

**Evidence labels used throughout**
`[GACH]` our Gachibowli sample, n = 40 · `[BLR]` our Bengaluru sample, n = 16 ·
`[PUBLIC]` public reviews / social / video · `[CLAIM]` company or media claim ·
`[ASSUMPTION]` not yet validated.

---

## 1 · Executive recommendation

**Run the fake door, but not the one that was proposed, and not for the reason usually given.**

Three changes to the brief's structure, each with a reason:

1. **Two arms, not three.** At n = 40 a three-arm test gives 13 per arm. Even a 38-percentage-point
   gap returns Fisher p = 0.115 — not significant, and a gap that large is implausible. The
   everyday-no-fee proposition moves out of the between-subjects test and into a within-subject
   within-subject question asked in the moment, where a small sample is not wasted.
2. **The primary metric is a named restaurant request, not a click.** A click costs nothing and
   `[GACH]` already tells us curiosity is cheap. Typing the name of a restaurant you actually order
   from costs recall, specificity and effort — and it produces an artifact with standalone
   operational value: a ranked list of the restaurants Gachibowli wants.
3. **Do not mock Rapido's interface.** Test the *mechanism* (does a food entry get noticed inside a
   mobility context) on a clearly-labelled generic mobility mock. This is both the ethical choice and
   the better science — it removes Rapido's brand recognition as a confound. It also under-states
   real-world notice, which is stated as a limitation rather than hidden.

**The honest framing of why this experiment is worth running.** Our survey already established the
restaurants-versus-price result at `[GACH]` McNemar exact p = 1.5 × 10⁻⁶. A fake door that merely
re-tests that would be a weaker replication of a stronger result. Its marginal value is three things
the survey could not do:

- convert a **hypothetical** trade-off into a **behavioural** one that carries a real cost;
- produce the **specific restaurant names** Gachibowli demands, which the survey never asked for and
  which the case study identifies as the binding constraint;
- test the Rapido discovery channel **prospectively**, where `[GACH]` measured it only by recall
  ("had you noticed food in the app"), a notoriously weak instrument.

That is a defensible reason to run it. "Validating demand" is not.

---

## 2 · Critical evaluation: is a fake door the right method?

### 2.1 What it can validly measure

| Can measure | Why |
|---|---|
| **Relative** preference between framings, between-subjects | Random assignment makes the arms exchangeable; the only systematic difference is the message |
| Behaviour at a genuine cost point | Naming a restaurant requires recall and typing — not a reflex tap |
| Where interest dies in a funnel | Drop-off shape is observable per step |
| Whether a discovery surface is noticed | Prospective, unlike the retrospective recall item in `[GACH]` |
| A ranked list of demanded restaurants | An operational artifact, valid regardless of the experiment's outcome |

### 2.2 What it cannot prove

| Cannot prove | Why not |
|---|---|
| Anyone will place a real paid order | No transaction exists. Intent ≠ purchase |
| Anyone will order a **second** time | Retention needs a cohort over time. This is the actual business risk and the fake door is blind to it |
| The saving survives a real checkout | `[GACH]` a rival coupon already makes Ownly ₹28 dearer; a prototype cannot reproduce a live membership and coupon stack |
| Restaurants will agree to join | Entirely supply-side. Untouched by this design |
| Delivery will be reliable | `[PUBLIC]` 72% of 37 reviews mention a failed delivery — the identified churn driver, and unobservable here |
| Hyderabad-wide demand | Convenience sample in one catchment |
| Willingness to accept a longer ETA | **Not testable by this design.** See §5.4 — ETA is held constant, so it cannot also be an independent variable |

### 2.3 The structural problem with the method, stated plainly

The case study's two load-bearing findings are that **assortment is the constraint** and **retention
is the risk**. A fake door measures **acquisition interest**. It can speak to the first and is
completely silent on the second.

So this experiment tests the part of the funnel we are *least* uncertain about, and cannot touch the
part that decides whether the business works. That is not a reason to skip it — the restaurant-demand
artifact and the channel test are genuinely new — but it is a reason not to over-claim from it, and
it is why §16 exists.

**v4 narrows the gap without closing it.** Carrying the journey through a menu, a cart and an
itemised bill (§6.1) reaches two things the earlier builds could not: a **basket** the participant
assembled, and a **pricing choice** made against that basket rather than against a hypothetical
₹230 scenario. That speaks to assortment far more directly than an expression of interest does.

**It still cannot touch retention**, and no amount of prototype fidelity will change that. Retention
needs a cohort observed over weeks. `[PUBLIC]` 72% of 37 reviews mention a failed delivery, and that
is the identified churn driver. A participant who picks Rapido Link on a prototype has told us the
idea appeals; they have told us nothing about what happens the first time it arrives cold.

### 2.4 Mock Ownly, Rapido, or both?

**Name Ownly. Mock neither interface. Build a generic mobility mock for the channel test.**

- **Name Ownly in the proposition.** Hiding the brand makes results uninterpretable: `[GACH]` 87.5%
  expect a new app's prices to rise, and that scepticism is attached to *this category*, not to an
  anonymous app. An unbranded test would measure a proposition nobody will ever be offered.
- **Do not reproduce Ownly's interface.** A visually identical clone risks misleading participants
  into thinking it is an official service, which is both an ethics failure and a trademark problem.
  The prototype uses an original layout and a distinct colour system, and is marked as a research
  prototype.
- **Do not reproduce Rapido's interface.** Same reasons, plus a scientific one: a convincing Rapido
  clone confounds *placement* with *brand recognition*. The generic mobility mock isolates placement.
  **Limitation, stated up front:** this under-estimates real-world notice, because real Rapido users
  have habituated scan patterns a mock cannot reproduce. The channel result is therefore a **lower
  bound**.

### 2.5 Landing page, app prototype, ad, or combined funnel?

**A combined short funnel — ad/entry → proposition → restaurant step → intent → disclosure.**

Not a full app prototype: fidelity beyond what the hypotheses need adds deception risk without adding
measurement. Not a static landing page: there would be no costly action, and a click alone is the
thing we are specifically trying to avoid treating as demand.

### 2.6 Commitment ladder — what is stronger than a click

| Level | Action | Cost to participant | Use here |
|---|---|---|---|
| 1 | Tap a card | Near zero | Secondary (CTR) |
| 2 | Scroll / dwell | Near zero | Diagnostic only |
| 3 | Start a search | Small | Secondary |
| 4 | **Type a specific restaurant they currently use** | Recall + effort + specificity | **PRIMARY** |
| 5 | Submit that request | Commitment to a stated want | Primary (same event) |
| 6 | Consent to follow-up contact | Privacy cost | Secondary — introduces selection bias |
| 7 | Pre-pay or deposit | Financial | **Excluded — unethical with no service** |

Level 4–5 is the sweet spot: costly enough to discriminate, ethical because nothing is promised.

### 2.7 Ethical protections

| Requirement | Implementation |
|---|---|
| No payment instruments | No card, UPI, or payment screen anywhere |
| No false order confirmation | The funnel ends at intent. No "order placed" state exists |
| No false availability | Restaurants are only ever **requested**, never shown as available. Results say "Added to the request list", never "Available" |
| Timely disclosure | Fires immediately after the intent action, before any contact field is shown |
| Nothing irreversible pre-disclosure | No contact captured, no external call made, before the disclosure screen |
| Explicit consent for contact | Unticked opt-in, with the purpose stated and fulfillable |
| No PII by default | Anonymous participant ID; contact only if consented |
| No impersonation | Visible research-prototype marker; original visual system; no official logos or screenshots |
| Withdrawal | Contact route on the disclosure screen to delete a submission |
| Minimal deception | The false impression lasts at most one screen and concerns availability only |

**The residual ethical cost, named:** a participant briefly believes Ownly may be launching with their
restaurant. That is the irreducible cost of the method. It is justified only because the disclosure is
immediate, nothing is collected before it, and no promise is made that we cannot keep.

### 2.8 If n = 40

Do not run three arms. The arithmetic (baseline 30% assumed `[ASSUMPTION]`, 80% power, α = .05):

| Per arm | Smallest detectable gap |
|---|---|
| 13 (3 arms at n=40) | **52 pp** |
| 20 (2 arms at n=40) | **43 pp** |
| 100 | 19 pp |
| 250 | 12 pp |

Even a 38-point gap at 13 per arm returns Fisher p = 0.115.

**Recommended n = 40 design:** two arms (Discount vs Restaurants), ~20 each, **explicitly
directional**, every participant answering 5–8 single-tap questions inside the journey, and a
**subset of 8–12**
moderated follow-up interviews**. At this size the qualitative layer carries more weight than the
quantitative one, and should be resourced accordingly.

### 2.9 If n = 200–300 or paid traffic

- **Three arms** (Discount / Everyday-no-fee / Restaurants), ~100 each → detects ~19 pp.
- **Add a neutral control arm** ("Ownly is coming to Gachibowli", no value claim) if n ≥ 400. This is
  what makes §5.3's congruence confound resolvable rather than merely declared.
- Keep the **channel test separate**, not factorial. A 3 × 2 design at n = 300 gives 50 per cell and
  cannot detect an interaction; spending power on an undetectable interaction is waste.
- With paid traffic: pre-register before spend, add bot filtering (`is_bot_suspect`), cap one session
  per device, and set a stopping rule in advance.

---

## 3 · Primary research question

**Revised 2026-09-22 (v3).** The question below is narrower than the v1 framing, and deliberately so.
The v1 question made the framing contrast primary, which put the whole study's weight on a
between-arms comparison that n = 40 cannot resolve (§2.8). The revision makes the *preference
discovery* primary and the framing contrast secondary, which is the right way round: the discovery
output is valid at any sample size, and the framing contrast is not.

> **What do Gachibowli food-delivery users aged 20–35 actually want to eat, which places do they want
> it from, and what happens to the order when the place they want is not on the app?**

Three sub-questions, each answered by a specific measure:

| Sub-question | Measure | Why nothing we already have answers it |
|---|---|---|
| What do they want to **eat**? | Free-text dish query + dish selected | None of the 37 fielded survey questions asks about food at all |
| Where do they want it **from**? | Restaurant chosen, plus every name typed that we do not stock | The survey asks about *apps* and *prices*, never about named restaurants |
| What does a **missing** place cost? | `missing_action` — the substitution question | Nothing in the project prices an assortment gap. This is the only measure that does |

**Secondary, and labelled as such:** does an assortment framing produce more qualified interaction
than a discount framing (H1)? Reported with its interval, never as a conclusion — §2.8 shows why.

---

## 4 · Hypothesis table

| ID | Behavioural hypothesis | Independent variable | Dependent variable | Controls | Supports if | Disproves if | Business decision | Cannot conclude |
|---|---|---|---|---|---|---|---|---|
| **H1** | Restaurant-access framing produces a higher named-restaurant request rate than first-order-discount framing | Proposition (Restaurants / Discount) | Restaurant Request Rate (RRR) | Layout, typography, restaurant count, images, ETA, CTA wording, device, entry channel | RRR higher in Restaurants arm, difference exceeds the pre-set practical threshold (§11) | RRR equal or higher in Discount arm | Whether to spend on local restaurant onboarding before discounting | That requests convert to orders; that the effect is causal outside the prototype |
| **H2** | *Withdrawn in v3.* The forced ranking of three framings lived in an end-of-session questionnaire, which v3 removed — see §13. Framing preference is now read from `first_meaningful_tap` and `offer_recall`, both measured in the moment | — | — | — | — | — | — | **No stated ranking is collected.** Do not report one |
| **H3** | *Withdrawn.* See §5.4 | — | — | — | — | — | — | **This design cannot test ETA tolerance.** ETA is a held constant; it cannot simultaneously be an independent variable |
| **H4** | A food entry inside a mobility-app context is noticed and opened at a low rate | Entry-card prominence (Control / Prominent) | Entry-card notice rate and CTR | Same home-screen mock, same session, same device | Notice and CTR materially below a normal in-app banner benchmark | High notice and CTR | Whether Rapido placement alone can serve as an acquisition channel | Real Rapido performance — the mock lacks Rapido's brand and habituated scan patterns. Result is a **lower bound** |
| **H5** | A tap overstates interest: a large share of people who tap never complete a costly action | None — within-funnel | Ratio of `first_meaningful_tap` to `restaurant_request_submitted` | Same funnel for all arms | Tap-to-request ratio is low across arms | Most tappers complete the costly action | Whether taps may be used as a demand signal in future tests | Which individuals would have ordered |
| **H6** | *(new in v3)* When a wanted restaurant is absent, a material share of demand leaves the app rather than substituting inside it | Absence of the named place (naturally occurring, not manipulated) | `missing_action` answer, asked at the moment the gap is hit | Same funnel, same prompt wording for everyone | A material share answer "go back to my usual app" or "not order at all" | Nearly everyone substitutes within the app | Whether assortment gaps cost orders or merely cost choice | Anything about the size of that loss in revenue, or whether it persists |

**H3 is deliberately withdrawn rather than weakened.** Testing ETA tolerance requires ETA to vary,
which breaks the control needed for H1. In v3 it is not asked as a question at all: delivery-time
influence is read from the `why_rest` option "it is the fastest or the nearest", which is a choice
made in the moment rather than a stated tolerance.

---

## 5 · Experiment design

### 5.1 Structure

- **Between-subjects** on proposition. Within-subject would expose a participant to both framings and
  make the second reading contaminated by the first.
- **Within-subject** for `first_meaningful_tap` and for `miss_most`, both read from behaviour and
  from a forced choice inside the participant's own set — not from a stated ranking.
- **Separate study** for the channel test (H4) — different participants or a clearly separated
  session, never the same exposure.

### 5.2 Assignment

- Coin flip on first load via `crypto.getRandomValues`, persisted in `localStorage` under
  `fd_variant`. Same browser always sees the same arm, on every reload and every later visit.
- Not alternating, not blocked: each participant is an independent draw, so the split approaches even
  without being exactly even.
- `?variant=` in the URL **overrides** assignment and marks the session `is_qa = true`, excluded from
  analysis. This is how the facilitator previews arms without polluting data.

### 5.3 The congruence confound — the biggest threat to validity

If the primary metric is a restaurant request and one arm's headline is about restaurants, that arm
**primes the exact action being measured**. A difference could mean "restaurant access is a stronger
proposition" or merely "priming an action increases that action."

This cannot be eliminated at n = 40. It is handled three ways:

1. **Identical funnel.** The restaurant step is byte-identical in position, prominence and wording in
   every arm. Only the headline block differs.
2. **Pre-registered congruence check.** Post-test Q1 asks, unprompted, what made them continue. If
   the Restaurants arm's advantage is priming, participants will cite the message; if it is genuine,
   they will cite their own restaurant need. This is a qualitative adjudication and is stated as such.
3. **Neutral control arm** at n ≥ 400 (§2.9), which is the only clean resolution.

**This limitation must appear on any slide reporting H1.**

### 5.4 Held constant across arms

Layout · typography · colour system · number of restaurants shown (6) · restaurant images
(illustrative, non-branded) · **ETA (fixed at 38–45 min, drawn from our own audit: `[GACH]` Ownly's
quoted ETA ran ~17 min above incumbents)** · CTA wording · button placement · device viewport ·
entry channel within a run.

### 5.5 Participants

| Criterion | Rule |
|---|---|
| **Include** | Age 20–35; ordered food online ≥ once in the last 4 weeks; lives, works or studies in the Gachibowli catchment; owns a smartphone |
| **Exclude** | Works for Ownly, Rapido, Swiggy or Zomato, or for a restaurant on a delivery platform; **took part in the Gachibowli survey** (that instrument primes the restaurants-vs-price trade-off directly); has taken part in an earlier wave of this study; cannot give informed consent |
| **Recruit via** | Fresh recruitment only — no overlap with the surveyed 40. University and co-working noticeboards; Gachibowli-area WhatsApp and Telegram groups; on-campus intercept; snowball from earlier participants — each channel logged in `utm_source` so recruitment-channel bias is visible |
| **Duration** | 10–14 days, or until the stopping rule is met, whichever is first |
| **Screening capture** | Facilitator records on the recruitment sheet: age band, area, occupation, orders in the last 4 weeks. These are inclusion criteria anyway, so they are never asked twice |
| **Device** | Participant's own smartphone, own network. No facilitator device — it changes behaviour |
| **Environment** | Unmoderated for the behavioural funnel; moderated only for the follow-up interview subset |

### 5.6 Integrity controls

| Risk | Control |
|---|---|
| One participant, several variants | Arm persisted in `localStorage`; one session per device; `anon_visitor_id` deduplicates |
| Duplicate participation | `anon_visitor_id` + a one-per-person recruitment code; duplicates flagged, not silently dropped |
| Facilitator previews polluting data | `?variant=` or `?qa=1` sets `is_qa = true`; excluded by the analysis script |
| Bots / automation | `is_bot_suspect` from `navigator.webdriver` and UA patterns; relevant only for paid traffic |
| Order effects in `offer_recall` | The four cards, including the never-shown control, are shuffled per participant |

### 5.7 Should participants know Ownly is the brand?

**Yes, from the proposition screen onward.** `[GACH]` scepticism about durability (87.5%) is
category-specific and brand-attached; an unbranded test would measure a proposition that will never
exist. They should **not** be told which hypothesis is being tested, nor that other variants exist,
until the debrief.

### 5.8 Pre-stratification

**Do not stratify at assignment with n = 40** — it creates cells too small to fill. Capture the
segment variables **at screening** (§13.4) and analyse post-hoc, with the minimum cell sizes in §12.

Segments to capture: membership (Swiggy One / Zomato Gold / both / neither); Rapido use; prior Ownly
awareness; prior Ownly trial; student vs working; single-app vs multi-app; order frequency.

**Prior Ownly users are analysed separately and never pooled** — `[GACH]` only 5% had ordered, so any
such participant is both rare and qualitatively different.

---

## 6 · Screen-by-screen flow  (v11)

**The two searches come first, because they are the reason the study exists.** The question is what
*kind* of food and what *kind* of place Gachibowli reaches for. Those are two different questions, so
they get **two boxes on one screen, recorded as two separate event streams** — a dish query never
lands in the restaurant column and vice versa. Both fire before anything reaches a cart.

| # | Screen | Choice made | Question fired immediately | Events |
|---|---|---|---|---|
| 1 | **Home** — 2×2 offer grid, working filter tabs, ETA boxed on each card | First meaningful tap | — (the grid is the arm, not a probe) | `landing_page_view`, `first_meaningful_tap`, `offer_card_click`, `filter_tab_click`, `category_chip_click` |
| 2 | **Search — two boxes** · *"What do you feel like eating?"* and *"Or go straight to a place"* | A dish **or** a restaurant | dish → **`why_dish`**, **`meal_slot`** · place → **`why_rest`**, **`app_gap`** · a place we don't stock → **`missing_action`** | `dish_search_started`, `dish_selected`, `restaurant_search_started`, `restaurant_search_selected`, `restaurant_added_custom` |
| 3 | **Places for that dish** (dish route only) | Which restaurant | **`why_rest`**, **`app_gap`** | `restaurant_search_view`, `restaurant_search_selected` |
| 4 | **Restaurant menu** | Which item | **`why_item`** | `menu_view`, `item_added`, `item_qty_changed` |
| 5 | **Delivery** — its own screen, no totals visible | Speed, at a randomised price | **`why_delivery`** (+ **`rapido_link_trust`**) | `delivery_screen_view`, `delivery_option_chosen`, `delivery_confirmed` |
| 6 | **Cart** — offers, then how you pay | Coupon, then charging model | **`why_offer`**, **`why_bill`** | `cart_view`, `offer_applied`, `bill_option_chosen` |
| 7 | **Place Order** | — | — | `place_order_click` |
| 8 | **The debrief** — one screen | — | — | `honest_stop_view`, `research_disclosure_view`, `followup_consent_given`, `prototype_exit` |

### 6.0 Every query is logged, not only the ones that end in a tap

**This was the largest data loss in the build and it went unnoticed until v11.** Until now a query
was only recorded if the participant *selected* something from it. Someone who typed *"pulihora"*,
found nothing, and settled for biryani left no trace of the word — and that word is the single most
valuable thing they could have given us.

`search_query` now fires **on a 700 ms pause**, once per distinct string of two or more characters,
carrying `query`, `results_count` and `source_screen`. One word is one row, not eight. Abandoned
searches survive; so does the order in which someone tried things.

| Captured | Why it matters |
|---|---|
| The query itself | The demand, in the participant's own words |
| `results_count` | **A zero is a supply gap.** The zero-result list is the operational output of the study |
| `source_screen` | `dish` or `restaurant` — the two streams never merge |

### 6.1 A missing DISH and a missing PLACE are different gaps

v11 handled a missing restaurant properly — explicit ask, event, question — and handled a missing
dish not at all. Typing a dish we did not have dropped the participant into a restaurant list with
**no record that the thing they came for did not exist**, and no question about it.

Both paths are now symmetrical:

| | Dish we don't have | Place we don't have |
|---|---|---|
| Empty state | "We do not have *X* in Gachibowli yet." | same |
| Primary action | **Ask for *X*** | **Ask for *X*** |
| Secondary action | "Show me places that might make it" | — |
| Event | `dish_added_custom` | `restaurant_added_custom` |
| Question | **`missing_dish`** | **`missing_action`** |
| After answering | Box clears, stays on search | Stays on search |

**They are asked separately because they are different business problems.** A dish nobody can find is
a **menu** problem — the restaurant is on the platform but the item is not listed. A place nobody can
find is an **onboarding** problem. Pooling them would hide which one actually costs an order.

`missing_dish` also carries an option the place version does not need: *"I only wanted it today —
normally I would not."* A one-off craving is not a gap worth funding, and without that option it
would be indistinguishable from real unmet demand.

**Neither path is a dead end.** In both cases the participant stays on the search screen with the box
cleared, free to keep looking — so a miss costs us a data point rather than the whole session.

### 6.2 Every selection carries its TYPE, not just its name

The operational output is not a list of names — it is a distribution over kinds.

| Recorded | On what |
|---|---|
| `category` | The dish's cuisine (Biryani, South Indian, …) and the restaurant's category |
| `rest_kind` | **`local` or `chain`** — the case study's central question, read off behaviour rather than asked |
| `query` | The raw string, scrubbed. A name we do not stock is kept verbatim, because a gap is a finding |
| `source_screen` | Which box it came from, so the two streams never merge |
| `tap_kind` on `first_meaningful_tap` | Which box they reached for first — place-first or dish-first thinking |

A participant who searches *"Chutneys"* and gets nothing is not a dead end: `restaurant_added_custom`
fires, `missing_action` asks what they would actually do, and they stay on the search screen to keep
looking. That path is the supply gap, named by the person who has it.

### 6.3 The debrief is one screen

Earlier builds ran **stop → disclosure → demand list → end**: four screens and a multi-select after
the behavioural data was already complete. It added one to two minutes to every session for no
measurement gain, and the demand list duplicated what the restaurant search now captures properly,
at the right moment, in the right place.

It is now **one screen, 118 words**, reached the instant Place Order is tapped:

- we can't place this order, and we won't pretend we did — nothing charged, no order, no restaurant
  contacted;
- Ownly is real but this page isn't run by them; everything shown was illustrative;
- what was recorded, and what was not;
- **a short code, with one line: quote it to have your answers deleted.**

Then **Done**. An optional follow-up consent sits below it as a ghost button. The code is repeated on
the closing screen so it survives a screenshot.

---

## 7 · Exact copy

### 7.1 Three behaviours in one experiment, without them contaminating each other

The study measures three separate decisions. Put naively on one screen they destroy one another:
**take the expensive fast delivery, then cancel its cost with a free-delivery coupon, then pick the
payment model that zeroes fees anyway.** Nothing measured under those conditions means anything.

Three rules keep them independent.

| Rule | What it prevents |
|---|---|
| **Delivery is decided on its own screen, before any total is visible** | Choosing speed because you expect a coupon to cover it |
| **No offer touches delivery.** Every coupon discounts the food only | Cancelling the delivery decision with the offer decision |
| **All three payment models charge the same delivery fee** | A payment choice retroactively rewriting a delivery choice already made |

The result: delivery costs the same rupees whatever offer and whatever payment model are chosen, so
each of the three can be read on its own.

**Order of decisions:** menu → **delivery (own screen)** → cart → offer → payment. Each is made
without knowing what the next one will offer. Changing delivery later is allowed but fires
`delivery_revisited`, so re-optimisation is visible in the data rather than silent.

### 7.2 Behaviour 1 — will they pay for time, and how much?

**v6's ladder was unusable.** It offered 42 min free, 25 min for ₹30, and 20 min for ₹55 — asking
₹25 for five minutes. Nobody weighs that; it is simply refused, so the top rung was a dead option.

**v7 uses two options and randomises the price of the fast one.**

| Option | ETA | Fee | Trade-off shown to the participant |
|---|---|---|---|
| Standard | 42 min | free | "Can wait longer at busy times." |
| Rapido Link | 25 min | **₹15 / ₹25 / ₹35 / ₹49** — randomly assigned per participant | "They may drop a passenger first. Live tracking starts once they have your order." |

Everyone faces the same **17-minute saving at a different price**, so take-up across the sample
traces a demand curve for time rather than yielding one meaningless take-up number. This is a
Gabor-Granger design, and it is the only way a fixed-menu prototype produces a rate.

The price is drawn from `crypto.getRandomValues`, persisted in `localStorage` so a reload cannot
re-roll it into a better deal, and carried on every relevant event as `rl_price`.

**The trade-off is not only money.** Rapido Link's cost includes a passenger detour and delayed
tracking — real consequences of piggybacking on a passenger fleet. A speed option with no downside
is not a decision. `rapido_link_trust` then asks what specifically worries them.

**Why ₹25–₹35 is the interesting region.** `[GACH]` the survey's `tradeoff_eta` found **92.5% would
wait 15 minutes longer to save ₹30**. If take-up stays high at ₹35 here, the two measures disagree —
and the behavioural one cost something.

### 7.3 Behaviour 2 — how steeply do they discount a reward that is not today?

**v7's coupons were unusable, and the fault was the same as the audit text: they were designed for
what we wanted to measure rather than for someone who might want them.** *"Every 5th order free"* and
*"₹75 off your next 3 orders from a kitchen you haven't tried"* both asked a person who has never
used this app to bet on four or five future orders — **and then to remember they had done so.** No
real app runs either. Neither is tempting.

They also rigged the result. A ₹0-today reward from an unfamiliar brand loses to ₹100 in hand every
single time, so "cash wins" was guaranteed before anyone tapped, and it would have proved nothing
about assortment or loyalty. Measuring which of four unappealing things is least bad is not measuring
preference.

**The three that replaced them.** All are offer types Indian delivery apps actually run. All are
legible on first read. **None requires the participant to remember anything or to predict their own
future behaviour.**

| Coupon | Structure | On a ₹640 basket |
|---|---|---|
| **₹100 off this order** | Cash now, certain | −₹105 off this bill |
| **₹X in Ownly Money** — lands in your balance when this order is placed, **applies itself** to your next order, valid 30 days | More cash, one order away, self-enforcing | +₹X next order |
| **10% off every order for 30 days** | Recurring, applies itself | −₹67 off this bill, and again all month |

**The wallet amount is randomised per participant: ₹120 / ₹150 / ₹200 / ₹250**, against a fixed ₹100
now. The amount at which people start choosing it **is the discount rate**, and the crossing point is
what one order of delay costs Ownly in rupees.

**Why the wallet mechanic and not a promise.** Swiggy already runs exactly this as "Free Cash", with
the balance visible in the app and applied automatically. It answers the objection that killed v7's
coupons — *"how would I even remember I picked that?"* — because there is nothing to remember. That
credibility is what makes the deferred option a fair comparator rather than a straw man.

**What it tells us.** `[GACH]` only 25% of the surveyed 40 said they would stay once an intro offer
ended. This is that finding priced. If nothing in the ₹120–₹250 range beats ₹100 today, Ownly cannot
wean anyone off discounts and has to buy every single order outright — which is the retention risk
the case study names, expressed in rupees instead of on a five-point scale.

**`why_offer` separates the reasons**, including the one that matters most: *"I am not sure I would
order here again."* Someone who takes cash now because they doubt they will return is a different
finding from someone who takes it because ₹100 is simply more than they discount ₹200 to.

### 7.4 Behaviour 3 — what will people accept being charged for?

**v7's version tested nothing.** It offered *"itemised bill"* against *"single price"* with the
single price **₹10 cheaper**. Nobody pays ₹10 to look at a list, so the answer was fixed before the
screen was read — and "single price, no breakdown" is not a screen any delivery app shows.

**Correction to an earlier claim in this document.** A previous revision said the transparency
question was "already answered by survey Q14". That was wrong, and the record matters:

- Q14 (`bill_fairness`) measures **fee pain**, not a preference between presentations.
  `[GACH]` catchment n = 40, 36 answered: **14 "the extra charges on top were too much"**, 7 "the food
  itself was overpriced", 12 "it felt fair", 3 "I didn't really look at the breakdown". Pre-registered
  as **K25 = 38.9%, 95% CI 24.8–55.1**. Fees outrank food price as the reason a bill felt unfair.
- The presentation question has its own designed instrument — `bill_s1` in
  `03_hyderabad_survey/bill_comparison_scenarios.md`: two bills at an **identical ₹245**, one simple,
  one itemised. **It was never fielded.** No `bill_s1` column exists in `cleaned_survey.csv`.
- `[PUBLIC]` 9 social items state a preference for *"a flat platform fee that is clearly labelled"*
  over free delivery with hidden menu inflation. Fake-door variant `B_transparent_bill` was written
  around it and got zero traffic.

So transparency is **an open question, deliberately scoped out of this screen** — at equal totals it
belongs in that instrument, not bolted onto a list of paid options where the cheaper one always wins.

#### The question this screen does ask

`[AUDIT]` Ownly charged **zero** on 8 of 8 Gachibowli captures — no delivery, platform, packaging,
small-cart or surge fee, only GST. Fee load **5.2%** of the bill against an incumbent median of
**23.4%**. *(On the record: those captures came from a new account carrying a ₹50 intro discount, so
₹0 is observed, not guaranteed.)* That cannot hold — so what will people accept instead?

| Option | Cost | What it tests | Evidence it rests on |
|---|---|---|---|
| **Pay per order** | ₹15/order | Will they accept *any* fee on an app that charges none? | ₹15 is Zomato's audited platform fee — **₹14.99 on every one of 14 captures** |
| **Ownly Plus** | ₹99/month | Room for a **third** subscription? | `[GACH]` **82.5% (33/40)** hold Swiggy One and/or Zomato Gold — the largest barrier measured in the study. A membership alone flips **1 of 4** audited baskets away from Ownly before any coupon. Two social users say a subscription would be acceptable; one names ₹200/month |
| **Order Protection** | **₹9 / ₹19 / ₹29 / ₹39 — randomised** | Will they *pay* for a refund guarantee? | `[GACH]` Q26 "what would most make you try Ownly": a quick refund promise came **2nd — 6 of 23**, behind price (8) and at **three times a first-order discount (2)**. `[PUBLIC]` refund delay or denial appears in **43% of 37 app reviews at mean severity 3.31**; support/refund failure is the largest review family at **79%** |

**Order Protection is the one this experiment exists to settle.** A refund promise is the second
strongest stated trial trigger in the whole survey and **nobody has ever been asked to pay for it**.
Randomising the cover price turns take-up into a willingness-to-pay curve, the same treatment the
delivery saving and the wallet amount get.

**The copy answers the documented complaints, not a generic promise.** App-store verbatims name the
specific failures: *"refund initiated… you will receive money 5 to 7 days"*, *"automated bots that
loop endlessly"*, *"they make you cry if you want to cancel"*. So the cover reads: **"Late, cold or
wrong — tap once and the full amount is back the same day. No photographs, no chat bot, no five-day
wait."** There is also a structural objection on record worth testing against: a marketplace-only
model creates a refund accountability gap, because the platform is only a delivery partner.

On a ₹640 basket with free standard delivery and ₹29 cover: **₹688 / ₹771 (then ₹672) / ₹702**.

**Every option itemises in full**, and all three charge the same delivery fee — so this cannot rewrite
the delivery decision made on the previous screen. Verified at ₹35: the delivery line reads ₹35 in
all three bills.

**`why_bill` separates the two readings that matter**: *"orders go wrong often enough that I would
want the cover"* against *"I do not believe the refund would actually happen"*. The first says the
product is wanted; the second says Ownly has a trust problem no price will fix.

**What is deliberately absent: payment method.** `[GACH]` cash-on-delivery / meal-card was chosen by
**0 of 23** catchment respondents as a trial trigger and **0 of 7** as a change that would increase
ordering. The assumption it was added to test (AS25) does not meet its kill criterion. Adding a
payment step would also breach the no-payment-instrument rule for nothing.

### 7.5 What the participant is never shown

**The prototype contains no internal reasoning, and this was a real defect in v6.** That build printed
justification lines under the delivery options — *"Audited: 0 of 8 Ownly captures carried any fee"*,
*"Matches Swiggy's audited 25 min. Priced at ₹30 for the 17 min saved — the exact trade the survey
asked about"*. That is research documentation, and putting it in front of a participant tells them
exactly what is being measured. Every such line is gone.

The rule: **participant-facing copy names the product and its trade-off, never the evidence behind
it.** Provenance belongs in this document. A check renders every screen and sheet and scans the
visible text for audit language, competitor names, sample sizes, survey references and experiment
vocabulary; it currently returns no hits.

### Constant copy

- Location header: "Gachibowli · DLF Cyber City Road, Hyderabad"
- Search placeholder, rotating: *Search "biryani"* · *Search "Paradise"* · *Search "dosa"* …
- Dish search: **"What do you feel like eating?"**
- Place search: **"Search a place you order from"**
- Regulars step: **"Which places do you actually order from?"** · "My place isn't listed — add it"
- Request confirm: **"Added to the Gachibowli request list."** — *never* "Available", and followed by
  "It does **not** mean these places are available, or that they are joining anything."
- Intent CTA: **"Tell us you want this in Gachibowli"** — not "Notify me when we launch", which would
  promise a notification we may not be able to send.
- Banner, sticky on every screen: "RESEARCH PROTOTYPE · not a live service · you cannot order food here"
- Footer, on every screen: "not affiliated with Ownly, Rapido or any delivery company. Restaurants,
  ratings, delivery times, prices and offers shown here are illustrative."

### Question copy — the rule every sheet follows

Every sheet names the participant's own choice in the question text, and every option is a complete
thought they could have had themselves.

| Wrong | Right |
|---|---|
| "Why did you select that restaurant?" | "**Why Paradise Biryani for that?**" |
| "Rate the importance of consistency" | "It is consistent — it never disappoints" |
| "Would you order elsewhere if unavailable?" | "**“Chutneys” is not on here. What would you actually do?**" |

The hint line under `missing_action` reads *"what you would genuinely do — not what sounds
reasonable"*, because the flattering answer ("I'd find something else here") is also the easy one.

### Screen 5 — research disclosure (verbatim)

> **This was a research prototype, not a live service.**
> You can't order food here, and nothing you did placed an order.
> We're a student research team studying how people in Gachibowli choose food-delivery apps. We showed
> you one of two versions of a message to see which one people respond to.
> **Ownly is a real app, but this page is not run by Ownly or Rapido, and they did not ask us to build
> it.** The restaurants shown are illustrative. Nothing here means a restaurant is joining any app.
> We recorded which buttons you tapped and how long you took. We did **not** record your name, phone
> number, email or location.
> If you'd like to tell us more, the next step is optional.

---

## 8 · Event schema

Every event carries: `event_id`, `experiment_id`, `page_version`, `variant_id`, `variant_key`,
`source`, `anon_visitor_id`, `anon_session_id`, `event_name`, `ts_iso`, `time_since_load_ms`,
`time_since_prev_ms`, `device_type`, `viewport_w`, `is_qa`, `is_bot_suspect`, `payload`.

| Event | Fires when | Extra properties | Signal | PII |
|---|---|---|---|---|
| `experiment_view` | Any prototype screen first renders | `entry_screen`, `storage_ok` | Denominator | No |
| `entry_card_view` | Entry card enters viewport ≥ 1s (IntersectionObserver) | `card_position`, `placement` | Secondary (H4) | No |
| `entry_card_click` | Entry card tapped | `card_position`, `dwell_ms` | Secondary (H4) | No |
| `landing_page_view` | Home screen renders | `variant_key`, `n_offers` | Denominator for H1 | No |
| `first_meaningful_tap` | The first tap that goes anywhere | `tap_kind`, `detail`, `ms_to_first_tap` | **Entry route — dish-first vs place-first** | No |
| `offer_card_click` | An offer card is tapped (filters the feed; no question) | `offer`, `detail`, `position` | Diagnostic — the card is the arm, not a probe | No |
| `offer_applied` | A coupon is applied at the cart | `offer`, `offer_worth`, `bill_id`, `delivery_id`, `bill_total`, `item_price`, `detail` (previous) | **PRIMARY — the priced offer choice** | No |
| `offer_removed` | An applied coupon is tapped off | `offer` | Diagnostic | No |
| `category_chip_click` | A category circle is tapped | `category` | Cuisine gravity | No |
| `restaurant_card_click` | A feed card is tapped | `restaurant_name` | Place-first route | No |
| `bottom_nav_click` | Bottom nav tapped | `detail` | Diagnostic | No |
| `micro_shown` | A question sheet opens | `q_id`, `subject`, `screen` | Denominator for that question | No |
| `micro_answer` | An option in the sheet is tapped | `q_id`, `answer`, `subject`, `detail`, `ms_to_answer` | **The in-journey evidence** | No |
| `dish_search_view` | Dish search opens | `detail` (place, if place-first), `tap_kind` | Funnel | No |
| `dish_search_started` | First keystroke in the dish box | `ms_to_start` | Separates browsing from intent | No |
| `dish_selected` | A dish is chosen or typed | `dish`, `query`, `typed`, `from_list` | **What they want to eat** | No* |
| `restaurant_search_view` | Places-for-that-dish opens | `dish` | Funnel | No |
| `restaurant_search_selected` | A place is chosen or typed | `restaurant_name`, `query`, `dish`, `from_list`, `typed` | **Where they want it from** | No* |
| `restaurant_added_custom` | A place we do not stock is named | `restaurant_name`, `source_screen`, `dish` | **The supply gap** | No* |
| `restaurant_request_submitted` | The list is confirmed | `restaurant_name` (pipe-joined), `n_requests`, `n_custom`, both queries, `tap_kind` | **PRIMARY** | No* |
| `notify_me_click` | Intent CTA tapped | `step_reached`, `n_requests` | Secondary | No |
| `research_disclosure_view` | Disclosure screen renders | `n_requests` | Compliance | No |
| `followup_consent_given` | Follow-up agreed on the disclosure screen | `contact_channel` | Secondary | **Channel only** |
| `filter_tab_click` | ALL / OFFERS / FAST / RATED 4+ tapped | `detail`, `category` | Price vs speed vs trust, before any restaurant is seen | No |
| `menu_view` | A restaurant's menu opens | `restaurant_name`, `dish` | Funnel | No |
| `item_added` | ADD tapped on a menu item | `item_name`, `item_price`, `restaurant_name`, `detail` (bestseller) | **What they would actually eat, at a price** | No |
| `item_qty_changed` | +/− on an item | `item_name`, `n_selected`, `detail` | Basket building | No |
| `cart_view` | Cart opens | `restaurant_name`, `n_selected`, `item_price` | Funnel | No |
| `bill_option_chosen` | A pricing model is selected | `bill_id`, `bill_total`, `delivery_id`, `item_price`, `detail` (previous) | **PRIMARY — the within-subject pricing choice** | No |
| `delivery_option_chosen` | A delivery option is selected | `delivery_id`, `mins`, `bill_total`, `bill_id`, `detail` (previous) | **Rapido Link take-up** | No |
| `place_order_click` | Place Order tapped | `bill_id`, `delivery_id`, `bill_total`, `mins`, `item_price`, `n_selected`, `restaurant_name`, `dish`, `bill_touched`, `delivery_touched` | Completed basket | No |
| `honest_stop_view` | The no-confirmation screen renders | `furthest_step` | Compliance | No |
| `wishlist_view` | Post-disclosure demand list opens | `n_requests` | Funnel | No |
| `prototype_exit` | `visibilitychange` / `pagehide` / finish | `furthest_step`, `dwell_ms`, `tap_kind`, `bill_id`, `delivery_id` | Diagnostic | No |

\* These fields are free text. They are *business* and *food* names, not personal data, but the
browser strips anything resembling a phone number or email before storage and the collector strips it
again. Single fields cap at 60 characters in the page and 80 in the collector; `restaurant_name` on
submission carries the whole pipe-joined list and caps at 500, so a long list is not silently
truncated.

**Removed across v3/v4:** `proposition_view`, `posttest_submitted`, `explore_restaurants_click`,
`picker_view`, `restaurant_search_skipped`, `notify_me_click`, `intent_declined`. Their payload keys
went with them.

**Both lists are checked against the prototype mechanically before every run.** A whitelist that has
drifted from the page fails *silently* — the collector answers `rejected: event_name` and the row is
simply never written. The check reports four things and all four must be clean: events the page emits
that the collector rejects, payload keys the collector drops, whitelist entries nothing emits any
more, and keys nothing sends. v3 shipped with `detail` missing from the whitelist, which would have
recorded *that* someone tapped an offer but not *which* offer.

### 8.0 · The micro-question events, and why they are two events not one

`micro_shown` and `micro_answer` are separate so that a question that was *asked and skipped* is
distinguishable from one that was *never asked*. Without the pair, a skipped question and an
unreached question look identical in the log, and every denominator becomes a guess.

| `q_id` | Fires after | Subject recorded | Answers |
|---|---|---|---|
| `why_offer` | Applying a coupon at the cart | the coupon | biggest on this bill · delivery fees annoy me · it lasts · want to try somewhere new · don't trust future promises |
| `why_dish` | Choosing a dish | the dish | craving · usual · time of day · sharing · safest |
| `why_rest` | Choosing a place | the place | only place · consistent · value · fastest · habit |
| `app_gap` | Choosing a place | the place | on my app · on it but expensive · **not on it** · never checked |
| `missing_action` | Naming a place we do not stock | the place | another place here · **back to my usual app** · other food · would not order |
| `miss_most` | Submitting a list of 2+ places | — | **their own picks**, as the options |
| `meal_slot` | Submitting a list | the dish | breakfast · lunch · evening · dinner · late night |

`ms_to_answer` is recorded on every one. It is a data-quality control, not a finding: a median under
roughly 1.5 seconds across a participant's answers means they were tapping to get past the sheet, and
that session should be flagged before analysis, not after.

### 8.1 · Two searches, and why both are recorded

The funnel now runs **dish search → restaurant search**, and both free-text queries are stored.

| Event | Fires when | Stored | Why it earns its place |
|---|---|---|---|
| `dish_search_started` | First keystroke in the dish box | `ms_to_start` | Separates browsing from intent |
| `dish_selected` | A dish is chosen or typed | `dish`, `query`, `typed`, `from_list` | **Nothing in the 37 fielded survey questions asks what people want to *eat*.** This is new evidence, not a replication |
| `restaurant_search_started` | First keystroke in the restaurant box | `dish`, `ms_to_start` | Intent to find a *specific* place |
| `restaurant_search_selected` | A place is chosen or typed | `restaurant_name`, `query`, `dish`, `from_list`, `typed` | The costly action. A typed name absent from our frame is kept and flagged `from_list: false` — those are the **real supply gaps** |
| `restaurant_request_submitted` | The list is confirmed | both queries carried forward | Joins dish demand to place demand on one row |

**Why the dish search is worth a screen of its own.** It asks what a person wants *before* they have
seen which restaurants exist, so the answer is not anchored to our list. The restaurant search that
follows is then anchored — deliberately — because that is how a real app works.

**A typed restaurant we do not stock is the most valuable single output of this study.** It is a
named business, wanted by a named participant type, that Ownly does not currently list. `[GACH]` the
audit found 88.9% catalogue overlap; these entries are the other 11%, identified by the people who
actually want them.

**Privacy.** Both queries are free text, so both are scrubbed of anything resembling an email or phone
number in the browser, capped at 60 characters, and scrubbed again in the collector. They are business
and food names, not personal data — but the defence is applied twice regardless.

**Where typing is and is not allowed.** Search boxes accept typing, because that is how search works
and because the query itself is data. **Every question in the journey accepts no typing at all** —
every answer is a tap. That distinction is deliberate: a search query is evidence, a typed
questionnaire answer is friction.


---

## 9 · Metric definitions  (v4)

### Primary — the discovery outputs

These are valid at any sample size, because they are *lists and distributions*, not comparisons.

| # | Output | Definition | Why it is the primary output |
|---|---|---|---|
| P1 | **Demanded dish list** | Every `dish_selected`, plus every raw `query` typed | The project has no food data at all. This is the whole gap |
| P2 | **Demanded restaurant list** | Every name in `restaurant_request_submitted`, ranked by count and by share of participants | The operational artifact: who to onboard, in order |
| P3 | **Off-frame request list** | Every `restaurant_added_custom` with `from_list: false` | `[GACH]` the audit found 88.9% catalogue overlap. These are the other 11%, named by the people who want them |
| P4 | **Assortment gap rate** | `app_gap` ∈ {not on my app, on it but expensive} ÷ answered | Whether the gap is real at the level of the individual's own restaurant, not at frame level |
| P5 | **Order-loss rate** | `missing_action` ∈ {back to my usual app, would not order} ÷ answered | The only measure in the project that prices a missing restaurant |
| P6 | **Pricing-model split** | final `bill_id` ÷ participants who chose one | Service P made payable instead of imagined. Every cart-reacher answers it |
| P7 | **Rapido Link take-up** | `delivery_id = rapido_link` ÷ participants who chose one | The one option no competitor can copy. It is also the priciest on screen, so price cannot explain it |
| P8 | **Offer-structure split** | final `offer_applied` ÷ those who applied one, with `offer_worth` | Which promotional shape wins when it is priced against the person's own basket. `local3` is worth ₹0 today, so picking it is a direct assortment-over-cash statement |
| P9 | **Basket composition** | `item_added` names and prices, median `bill_total` | What people would actually eat, at a price they assembled themselves |

### Secondary — the framing contrast

> **Restaurant Request Rate (RRR)** = participants who submit at least one **named** restaurant ÷
> participants who reached the home screen (`landing_page_view`, `is_qa = false`).

> **Gap-qualified RRR** = as above, *and* they said at the moment of choosing that they cannot get
> that place on the app they use today, or can only get it expensively.

The gap-qualified form replaces v1's "do you order from here now?" filter, which came from a question
the v3 journey removed. It is a stronger filter, not a weaker one: it requires a named place, a
completed submission, and a stated gap.

| Metric | Formula |
|---|---|
| Entry-card CTR / notice rate (H4) | `entry_card_click` ÷ `entry_card_view` · `entry_card_view` ÷ `experiment_view` |
| Dish-reach rate | `dish_search_view` ÷ `landing_page_view` |
| Dish-selection rate | `dish_selected` ÷ `dish_search_view` |
| Place-selection rate | `restaurant_search_selected` ÷ `restaurant_search_view` |
| Off-frame request rate | participants with ≥1 `restaurant_added_custom` ÷ participants |
| Notify-me intent | `notify_me_click` ÷ `landing_page_view` |
| Tap-to-request ratio (H5) | `restaurant_request_submitted` ÷ `first_meaningful_tap` |
| Offer-structure split | final `offer_applied.offer` ÷ participants who applied one |
| Cash-forgone rate | share choosing a coupon worth strictly less than the best available to them |
| Drop-off by step | 1 − (step *n* ÷ step *n−1*) |
| Time to action | Median `time_since_load_ms` at `restaurant_request_submitted` |
| Menu-to-cart rate | `item_added` ÷ `menu_view` |
| Cart-to-order rate | `place_order_click` ÷ `cart_view` |
| Pricing-choice engagement | `bill_option_chosen` ÷ `cart_view` |

**Pricing-choice engagement must be reported before the pricing split itself.** If few people touched
the control, the split describes a default, not a preference — and that is a finding about the screen,
not about pricing. The analysis script prints it in that order for exactly this reason.

**Offer take-up must be read against what the coupon was worth.** Every `offer_applied` carries
`offer_worth` in rupees for that participant's basket and pricing model, so "chose the ₹100 coupon"
is never reported without the fact that it was the largest number on their screen. The reading that
matters is the **minority who did not** take the largest number — and `why_offer` says whether that
was fee-annoyance, durability, or assortment.

### The interest ladder — what each level does and does not mean

| Level | Measured by | Means | Does **not** mean |
|---|---|---|---|
| Curiosity | `first_meaningful_tap` | Something caught the eye | Any intent |
| Consideration | `dish_selected` | Willing to say what they want | Willing to act |
| Selection | `item_added` | Put specific food at a specific price in a basket | They would pay for it |
| **Priced choice** | `bill_option_chosen` | Chose how to be charged for **their own** basket | They would accept that price in the real world |
| **Completed basket** | `place_order_click` | Carried a real order to the last screen | A purchase. No money moved and none was ever asked for |
| **Qualified interest** | `restaurant_request_submitted` | Named a real place they use | They will order |
| **Gap-qualified interest** | the above + `app_gap` = not available | Named a real place they *cannot currently get* | They will order, or that Ownly can get that place |
| Purchase | — | **Not measurable here** | — |
| Repeat | — | **Not measurable here** | — |

**`place_order_click` is the strongest signal this design can produce, and it is still not a
purchase.** It says someone assembled a basket, chose how to pay for it, chose how to receive it, and
pressed the button. It does not say they would have done so with their own money on a live app, and
no write-up may describe it as a conversion, an order, or validated demand.

---

## 10 · Analysis methodology

### Tests, by sample size

| Situation | Test | Why |
|---|---|---|
| Any expected cell < 5 (the n = 40 case) | **Fisher's exact** | Exact; no large-sample approximation |
| All expected cells ≥ 5 | Chi-square | Adequate and conventional |
| Difference in rates | **Newcombe-Wilson interval** on the difference | Behaves correctly near 0 and 1, unlike Wald |
| Effect size | Risk difference (pp) **and** risk ratio | pp drives the decision; RR travels across baselines |
| Funnel shape | Descriptive + Wilson intervals per step | No test; it is a shape, not a comparison |

### Formulas

```
RRR_arm              = requests_arm / exposed_arm
Absolute difference  = RRR_C − RRR_A                      (percentage points)
Relative uplift      = (RRR_C − RRR_A) / RRR_A            (report only if RRR_A ≥ 0.10)
95% CI on difference  = Newcombe-Wilson hybrid score interval
```

**Which comparisons are valid**

- Valid: arm vs arm on the same step; step-to-step drop-off within an arm; segment vs segment where
  both cells meet §12 minimums.
- **Not valid:** comparing a rate from this experiment with `[GACH]` survey percentages — different
  populations, different instruments, different denominators. They are different studies.
- **Not valid:** comparing the mobility-mock CTR with published in-app benchmarks — the mock has no
  brand equity.

### Why p-values are not the decision criterion

At n = 40 the study is powered to detect ~43 pp. A null result therefore carries almost no
information, and a significant result would require an implausibly large effect. Decisions are made
against the **practical thresholds** in §11, with the interval reported alongside. A p-value is
reported for completeness and is explicitly not the trigger.

### Sample results table — **DUMMY DATA, NOT FINDINGS**

> ⚠️ Every number in this table is fabricated for illustration. It must be deleted before any real
> result is entered, and must never appear alongside real data.

| Metric | Arm A · Discount | Arm C · Restaurants | Diff (pp) | 95% CI | Fisher p |
|---|---|---|---|---|---|
| Exposed | 20 | 20 | — | — | — |
| Explore rate | 55.0% (11/20) | 60.0% (12/20) | +5.0 | −25 to +34 | 1.00 |
| **RRR (primary)** | 25.0% (5/20) | 45.0% (9/20) | **+20.0** | −9 to +45 | 0.31 |
| Notify-me intent | 30.0% (6/20) | 35.0% (7/20) | +5.0 | −23 to +32 | 1.00 |
| Qualified interest | 20.0% (4/20) | 35.0% (7/20) | +15.0 | −13 to +40 | 0.48 |

*Read across: even a 20-point gap on the primary metric would not reach significance at this size.
That is the expected outcome and the reason the design is labelled directional.*

---

## 11 · Decision rules — pre-registered

**Threshold types.** `S` statistical · `P` practical business threshold · `D` directional research
rule. At n = 40, **all primary rules are type D or P**; no type-S rule is available.

| # | Result | Type | Interpretation | Decision |
|---|---|---|---|---|
| R1 | RRR(Restaurants) − RRR(Discount) ≥ **+15 pp** | D | Availability is directionally the stronger lever | Prioritise onboarding the requested local restaurants before any discount spend |
| R2 | Difference within **±10 pp** | D | No directional separation at this size | Do not choose between them on this evidence. Escalate to the n ≥ 200 design |
| R3 | RRR(Discount) − RRR(Restaurants) ≥ **+15 pp** | D | Discount is directionally stronger — contradicts `[GACH]` | Treat as a flag, not a finding. Re-examine the survey trade-off before acting |
| R4 | Explore rate high but RRR low in **both** arms (click-to-request < 0.35) | P | Clicks are curiosity, not intent | Do not use CTR as a demand signal in any future Ownly test |
| R5 | RRR < 15% in **both** arms | P | The proposition itself is weak, not the framing | **Do not respond by increasing the discount.** Re-examine the offer |
| R6 | Entry-card notice rate < 40% on the mobility mock | D | Passive placement is a weak discovery channel — consistent with `[GACH]` 5 of 33 | Do not rely on in-app placement alone; test active acquisition |
| R7 | ≥ 60% of requested restaurants are already on Ownly | P | The assortment gap is narrower than assumed | Shift emphasis from onboarding to communicating existing coverage |
| R8 | A single restaurant is requested by ≥ 20% of participants | P | A concentrated supply target exists | Onboard it first; it is the cheapest possible win |

R7 and R8 are the rules that pay for the study regardless of how H1 resolves.

---

## 12 · Segmentation plan

| Segment | Why it matters | Min per cell to interpret |
|---|---|---|
| Membership (any vs none) | `[GACH]` 82.5% hold one; a membership erases the list-price saving | 15 |
| Rapido user vs not | `[GACH]` Rapido users were *less* aware (33% vs 56%) | 15 |
| Student vs working | `[GACH]` differing switching bars (₹30 vs ₹50) | 15 |
| Single-app vs multi-app | `[GACH]` 57.5% multi-home; a second app is a lower bar | 15 |
| Ownly-aware vs not | `[GACH]` 42.5% aware | 15 |
| **Prior Ownly trial** | `[GACH]` 5% — rare and qualitatively different | **Never pooled; report as case notes** |
| Order frequency | Heavier users have more to save | 15 |

**The n = 40 rule:** with 20 per arm, a segment split produces ~10 per cell. **Do not run segment
comparisons at n = 40.** Report segment composition as a descriptive table only, so the reader can see
who was in the sample. Segment *comparisons* require n ≥ 200.

---

## 13 · The question set — asked in the journey, not after it

### 13.1 Why there is no post-test

The v1 design ended with a six-item questionnaire after the disclosure. **That has been removed in
full.** The reason is not length, it is validity.

A question asked at the end of a session asks the participant to *reconstruct* a reason for something
they did several screens ago. Reconstruction is not recall. What comes back is a plausible-sounding
account assembled from the options on offer — which is precisely the failure mode a fake door exists
to avoid. Worse, by the time the questionnaire appears the participant has been told the whole thing
was research, which reframes everything they did before it.

So every question now fires **one tap after the choice it is about**, on the screen where the choice
happened, with the participant's own selection named in the question text: not "why did you pick that
restaurant" but "**Why Paradise Biryani for that?**". The window between the behaviour and the
question is under a second.

**What this costs, stated plainly.** Interrupting a journey to ask about it changes the journey.
Someone asked "why that dish?" now knows the app is interested in their reasons, and may deliberate
more on the next screen than they otherwise would. This is a real cost and it is not avoidable — the
alternative, asking later, trades a known reactivity cost for an unknown recall cost. We take the
known one. It is a limitation to state, not a flaw to hide.

### 13.2 Ethics questions are not in the questionnaire

The v1 post-test asked "before the disclosure, what did you think this page was?" as a manipulation
check. **Removed.** It produced no evidence about food or restaurant preference, and the ethical
protection it was standing in for is better served by the protections themselves: a permanent research
banner on every screen, no order state that can be reached, no restaurant ever shown as available, and
a disclosure that fires within one screen of the intent action. Those are controls. A question about
them was a report card, not a safeguard.

### 13.3 The duplication audit — what is deliberately NOT asked

Every item was checked against the 37 questions actually fielded in the live Hyderabad survey.

**Already measured — never re-asked**

| Already in the survey | What it measures | Value `[GACH]` |
|---|---|---|
| `tradeoff_rest` | Will you give up usual restaurants for ₹30 | 35.0% |
| `tradeoff_eta` | Will you wait 15 min longer for ₹30 | 92.5% |
| `tradeoff_rel` | Will you accept 3-in-10 late for ₹30 | 72.5% |
| `switch_savings` | Recurring saving needed to switch | median ₹30 |
| `durability_doubt` | Do you expect prices to rise | 87.5% |
| `repeat_no_promo` | Would you stay after the intro offer | 25.0% |
| `memberships` / `rapido_freq` / `ownly_status` | Segments | 82.5% / 60% / 42.5% |
| `prop_forced` / `prop_reason` | Proposition P vs Q preference | 18 vs 11, 11 could not choose |

**The eight questions that are asked, and what each one adds that nothing else has**

| `q_id` | Asked at | New because |
|---|---|---|
| `offer_recall` | leaving the home screen | Whether a loud discount registers **at all** with someone whose attention went to food. Carries its own false-recall control |
| `offer_why` | tapping an offer | Which *element* of a discount pulls — the number, free delivery, or the food it names. The survey only ever measured whether a saving was enough |
| `why_dish` | choosing a dish | **Nothing in the project asks about food.** Craving, routine, time of day, group size and risk-aversion are five different demand drivers with five different implications |
| `why_rest` | choosing a place | The assortment mechanism. "Only place that makes it right" and "habit" look identical in a survey and are completely different businesses |
| `app_gap` | choosing a place | The audit measured catalogue overlap at **frame** level (88.9%). This measures it at the level of **the individual's own restaurant**, which is the level at which people actually switch apps |
| `missing_action` | naming a place we do not stock | **The single most valuable item.** Nothing in the project says whether a missing restaurant costs an order or merely costs choice |
| `miss_most` | submitting a list of 2+ | A forced ranking inside the participant's **own** set. A survey cannot do this, because the options do not exist until the participant creates them |
| `why_item` | adding to the cart | Menu-level choice. The survey asked about apps and prices; nothing asked what a person would actually put in a basket |
| `why_bill` | choosing a pricing model | **Q22 asked people to imagine Service P. This asks them to pay it**, on a basket they built, against two live alternatives |
| `why_delivery` | choosing a delivery option | Speed was previously a hypothetical trade at a fixed ₹30. Here it is priced against their own bill |
| `rapido_link_trust` | choosing Rapido Link | Rapido's passenger fleet is the one asset no competitor has. Nothing in the project has asked whether anyone would accept food from it |
| `meal_slot` | submitting a list | *When*, not whether. Drives catchment hours and rider shift planning, and nothing else in the project touches it |

Every one is a single tap from 4–6 options. **No typing anywhere except the two search boxes**, where
the typed string is itself the finding.

### 13.4 Sample comparability now sits with the facilitator

The v1 post-test carried four tick-boxes — membership, Rapido use, Ownly awareness, Ownly trial —
whose job was to show that the fake-door sample resembles the surveyed 40 closely enough for survey
findings to be used as interpretive context. Those are not questions about food or restaurants, so
under the v3 rule they do not belong in the journey.

**They have not been dropped. They move to the screening sheet**, collected by the facilitator at
recruitment alongside age band, area and occupation — which were already inclusion criteria (§5.5).
The methodological obligation is unchanged:

| Captured at screening | Surveyed 40 `[GACH]` | Purpose |
|---|---|---|
| Pays for Swiggy One / Zomato Gold | 82.5% | The largest barrier in the case study |
| Used Rapido in the last month | 60% | H4 depends on it |
| Had heard of Ownly before today | 42.5% | Awareness contaminates response |
| Has ordered on Ownly before | 5.0% | Rare and qualitatively different — never pooled |

**Mandatory in the write-up — the comparability table.** Report these four side by side with the
survey values. If any differs by more than roughly 20 percentage points, say so explicitly and stop
using the survey as interpretive context for that dimension. With ~40 participants the interval on
each is about ±15 pp, so only a large divergence is detectable — which is itself worth stating.

**These four characterise the sample. They do not split it.** Segmentation was already ruled out at
this size (§12); with a fresh sample it is doubly so.

### 13.5 A fresh sample, and what that obliges us to do

Participants are recruited **fresh** — none of the surveyed 40 takes part.

- **It avoids priming.** Survey respondents were asked, explicitly, *"would you give up most of your
  usual restaurants to save ₹30?"* Anyone who answered that has been told in advance that
  restaurants-versus-price is the thing under study.
- **It gives an independent sample.** A behavioural result from the same 40 people would be a second
  reading of one group, not new evidence.

**The obligation it creates.** Because there is no overlap, **no survey finding may be assumed to hold
in this sample.** The 82.5% membership rate, the 60% Rapido use, the 42.5% awareness are properties of
the surveyed 40, not of Gachibowli.

**Avoided as leading:** "Did the discount make you want to try Ownly?" · "How much would you pay?" ·
anything of the form "don't you agree…". Note also that `missing_action` is worded *"what would you
actually do"* with the hint *"not what sounds reasonable"*, because the socially acceptable answer
("I'd find something else here") is the one that flatters the app.

---

## 14 · Claims matrix

| Claim | Status | Correct phrasing |
|---|---|---|
| One framing produced more qualified interaction than the other | **Potentially supported** | "In this sample, the restaurant framing directionally outperformed the discount framing by X pp (95% CI …)." |
| Specific restaurants are in demand | **Supported** | "Participants named these restaurants; N of them are not currently on Ownly." |
| A mobility-app entry was or was not noticed | **Potentially supported, lower bound** | "In a non-branded mock, X% noticed the entry card. This under-states real Rapido performance." |
| Some segment showed stronger interest | **Requires n ≥ 200** | "Segment differences are not interpretable at this sample size." |
| Users will place a real paid order | **Not supported** | Do not claim |
| Users will order a second time | **Not supported** | Do not claim |
| Ownly will be profitable in Hyderabad | **Not supported** | Do not claim |
| Hyderabad-wide demand is established | **Not supported** | "Findings describe this Gachibowli convenience sample." |
| Delivery reliability is validated | **Not supported** | Untouched by this design |
| Restaurants will agree to join | **Not supported** | Entirely supply-side |
| Long-term retention is proven | **Not supported** | The design is blind to retention |

Permitted verbs: *supports, does not support, directionally suggests, in this sample, requires further
validation, is consistent with, cannot distinguish.* **"Proves" is not available to this study.**

---

## 15 · Six-slide presentation content

**Slide 1 — Why this experiment**
Evidence we have `[GACH]`: 92.5% trade speed for ₹30, 35% trade restaurants; 89% catalogue overlap;
82.5% hold a membership. What we don't know: whether any of that survives a **behavioural** cost, and
which restaurants specifically are missing. Decision: where the next rupee goes — restaurant
onboarding or discounting.

**Slide 2 — Hypothesis**
Primary H1. Control = first-order discount (the incumbent playbook). Challenger = restaurant access
(what `[GACH]` says people actually refuse to trade). Matters because the two imply opposite budgets.

**Slide 3 — The funnel**
Entry → home → dish → place → regulars → request → intent → disclosure, with a one-tap question
fired at each choice. Mark where the
costly action sits and where the disclosure fires.

**Slide 4 — What is measured**
Primary: Restaurant Request Rate. Secondary: the ladder from CTR to qualified interest. Segments:
descriptive only at n = 40. Decision rules R1–R8, pre-registered.

**Slide 5 — Evidence boundary**

| Can establish | Cannot establish |
|---|---|
| Relative framing preference, in this sample | Real purchase |
| Which restaurants are demanded | Repeat behaviour |
| Whether a mobility entry is noticed (lower bound) | Profitability, supply, reliability |

**Slide 6 — Ethics and limits**
No payment; no fake confirmation; no false availability; disclosure within one screen; contact only on
opt-in. Limits: n = 40 is directional (detects ~43 pp); the congruence confound; intent ≠ behaviour.
**Results slides stay as placeholders until data exists.**

---

## 16 · What this experiment is not

The case study's decisive risk is **retention** — `[PUBLIC]` 72% of 37 reviews mention a failed
delivery, and interviews say people leave after *repeated* failures. This experiment cannot see any of
that. It also cannot see whether `[GACH]` the ₹114 saving survives a real membership and coupon.

If only one further study can be funded, a **cohort study of real Ownly orders over 60 days** answers
a more important question than this one does. This fake door is worth running because it is cheap, it
is ethical, and it produces the restaurant list — not because it settles the business case.

---

## 18 · The survey hand-off, and the QR

The debrief now ends on a **primary** call to action — *"Yes — I'll answer a few more questions"* —
with *"No thanks, I'm done"* as the secondary. Someone who has just carried a basket to checkout is
the most engaged they will ever be; asking then, rather than by email later, is the cheapest sample
we will get.

Tapping it opens a screen with a **QR code they scan with their own phone**, plus the link as
tappable text for anyone already on a phone. Their deletion code is repeated there, so the survey
step never costs them the one thing they might need later.

**The QR is generated inside the page.** A field prototype cannot depend on a CDN or an image host:
it may run from `file://`, on a borrowed phone, on bad hotel wifi. So the file carries a complete
QR encoder — byte mode, ECC level M, versions 1–10, mask chosen by the standard penalty rules, drawn
as inline SVG.

**It was verified rather than trusted.** A hand-rolled QR encoder that is subtly wrong produces a
symbol that looks perfect and scans as nothing, and you find out in the field. The encoder was
checked **module for module against the Python `qrcode` library across 66 URLs spanning versions
2–10**, with the mask forced to match. All 66 are identical.

Two bugs were found that way and would not have been found any other way:

1. **The character count indicator is 16 bits from version 10 up**, not 8. The first build hardcoded
   8, which shifts the entire bit stream. Everything up to a 180-character link scanned fine; longer
   links produced a valid-looking symbol containing nothing.
2. A first comparison against `segno` showed a padding difference. Cross-checking against a *second*
   implementation showed `segno` was the outlier and this encoder matched `qrcode` exactly — a
   reminder that one reference is not a reference.

**If `CONFIG.SURVEY_URL` is empty the whole step disappears** — no dead button for participants, and
a visible facilitator warning in QA mode instead.

---

## 17 · Execution checklist

**Before launch**
☐ Freeze this document with a date; no changes after the first participant
☐ Ethics sign-off; disclosure text approved verbatim
☐ Pilot with 5 people (not counted); check that the question sheets read as part of the app, that
  nobody is confused about what "request" means, and that the disclosure lands
☐ Verify arm assignment persists across reload and across sessions
☐ Verify no PII is stored when consent is not given
☐ Confirm the collector endpoint accepts and stores a QA event end-to-end
☐ Set and write down the stopping rule
☐ Prepare the recruitment code list for duplicate control

**During**
☐ Monitor arm balance daily; do not rebalance mid-flight
☐ Watch `is_bot_suspect` and `is_qa` volumes
☐ Do not look at the primary metric by arm until the stopping rule is met

**After**
☐ Export events; drop `is_qa` and `is_bot_suspect`
☐ Deduplicate on `anon_visitor_id`
☐ Compute the funnel, then the primary metric, then segments **descriptively only**
☐ Apply R1–R8 as written
☐ Write the demanded-restaurant list and check each against Ownly's live catalogue
☐ Run 8–12 follow-up interviews with consenting participants
☐ Debrief all participants; honour deletion requests
☐ Delete contact details once the follow-up window closes
