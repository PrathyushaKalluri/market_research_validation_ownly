# Fake Door v3 — Redesign Spec

**Written:** 2026-09-17, after external research on fake-door practice and on Ownly's own strategy statements.
**Supersedes:** the A/B design in `AB_LAUNCH_RUNSHEET_v2.md` §arms. Mechanics, collector and ethics flow are unchanged.
**Status:** **built 2026-09-17, Option B chosen (D15).** Build, admin view, Meta plan and stop rule: `FAKE_DOOR_v3_RUNBOOK.md`.
Two changes from this spec at build time: the proof lines say "on 16 Sep" (not "last week"), and the WhatsApp-number step became a one-tap question (runbook §6).

---

## 1. What was wrong with v2

| Problem | Evidence |
|---|---|
| **It was specified as a hypothesis test it can never pass.** K13 is marked P0 and "primary if ≥80 visitors". To detect a 10-point difference at a 20% baseline you need **≈291 visitors per arm (≈582 total)**. 80 visitors detects only a ~20–25 point gap — implausible between two reasonable messages. | Two-proportion z, α=0.05, power 80% |
| **Arm B is confounded.** A tests one idea (price). B bundles three (local restaurants + honest ETA + refunds). If B wins, we cannot say which of the three won. | Practitioner rule: a message test varies exactly one thing |
| **The page is too heavy for cold traffic.** Hero is 131 words (~36 s of reading) before the button; the post-click flow adds 204 words across 19 inputs and 10 buttons. | Users decide in <5 s; ~80% of attention is above the fold; every extra form field costs conversion |
| **Organic sharing is not randomisation.** Who forwards what, and when, is mixed into the result — there is no random split, so "A beat B" can just mean "A's groups were livelier". | Message tests need simultaneous, evenly-split exposure |
| **It duplicated the survey.** Survey §7 already tests the Bengaluru price pitch (P) against the localized pitch (Q) as K14. Running the same contrast twice spends traffic without adding a new question. | `13_survey_v3_live/survey_questions.md` S7 |

**What v2 got right and v3 keeps:** immediate disclosure at the click (this matches IRB guidance on
deception and practitioner norms), a sticky per-browser assignment, QA rows excluded by flag, and a
pre-registered stopping rule.

---

## 2. The new goal, in one sentence

> **Does Ownly's stated growth model — everyday low prices instead of discount-led growth — actually pull
> people, or does it still need a discount to get the first order?**

That is a question the survey cannot answer behaviourally, it is Ownly's own stated bet, and it is exactly
what a fake door is good at: two headlines, one button, count the taps.

### Why this question and not the old one

Sanka's public position is explicit and testable:

| Ownly's claim | Source |
|---|---|
| "We have to solve for affordability. That is the biggest deterrent for consumers today." | Storyboard18, 2026-07-06 |
| "Ownly is not a discount platform… We don't force discounts." | Inc42 |
| "Ownly will focus on **everyday low prices rather than discount-led growth**." | Storyboard18, 2026-03-04 |
| "It is a gap not of demand, but of **affordability and trust**." | Sanka, Inc42 |

Meanwhile JP Morgan reports that Swiggy's **Toing** — a discount-and-performance-marketing play — was
"materially more successful" than Ownly over three months. So the company's central strategic bet is
contested by an analyst, and no instrument in this project tests it. That is the gap v3 fills.

**And it generalises to new markets,** which is what the project ultimately needs: if everyday-low-price
pulls on its own, Ownly can enter a new city without buying demand. If it only works with a discount
attached, every new city costs money and the model's economics are the constraint — which matters, because
analysts estimate ₹50–60 delivery cost against a ₹30 fee.

---

## 3. The two arms

Identical page, identical bill table, identical button. **One variable: whether the saving is permanent or promotional.**

### Arm A — `A_everyday_low_price` (Ownly's stated model)
> **Headline:** Dinner costs less here. Every day, not just today.
> **Sub:** Restaurants list their own menu prices. No delivery, platform or packaging fees.
> **Proof line:** On a real Gachibowli order last week: ₹188 here, ₹259 on the app it came from.

### Arm B — `B_discount_led` (the incumbent/Toing model)
> **Headline:** ₹100 off your first three dinners.
> **Sub:** A new food delivery app for Gachibowli. Get ₹100 off each of your first three orders.
> **Proof line:** On a real Gachibowli order last week: ₹259 on the app it came from — ₹159 with the offer.

Both arms show the same ₹259 reference bill, so the *amount saved is comparable* and only the **reason for
the saving** changes: structural versus promotional.

**What each result means:**

| Result | Read | Consequence for the Hyderabad GTM |
|---|---|---|
| A ≥ B | The structural story pulls on its own | Ownly's stated model transfers; enter new cities on the price-structure message |
| B > A by a wide margin | Demand is bought, not earned | The claim "we don't force discounts" is not how this market behaves; entry cost per city is real and recurring |
| No separation | Framing is not the lever at this stage of awareness | Distribution and supply matter more than message; spend on restaurants and the Rapido app, not on copy |

Any of the three is a finding. None of them is a null result.

---

## 4. The page (rebuild spec)

**Above the fold, nothing else:** headline (≤10 words) · sub (≤20 words) · the proof line · one button.
Target: **under 40 words before the CTA**, down from 131.

Below the fold, optional scroll: the bill table (unchanged, real numbers), then the same button again.

**After the tap — in this order:**
1. **Disclosure, immediately.** "No app, no order, no payment. We're students testing which idea people
   respond to. Nothing was ordered and nothing will be charged." *(unchanged from v2 — this is the ethical core)*
2. **One costly action, not four.** "Want to know when something like this reaches your area? Leave a
   WhatsApp number." One field. A phone number is effortful, so it separates curiosity from intent far
   better than a tap.
3. **The survey button.** Unchanged, tagged `src=fakedoor_A` / `_B`.

**Cut entirely:** the bill-comparison calculator (2 inputs + validation), the 3-question mini-survey
(11 radio inputs). They cost roughly 15 of the 19 inputs and sit between the tap and the signal we want.
Occupation and locality now come from the survey, which is where they belong.

---

## 5. Metrics (revised)

| KPI | Definition | Role |
|---|---|---|
| **K13** CTA rate per arm | unique visitors with `cta_click` ÷ unique visitors | Primary outcome of *this instrument*, **reported as directional** |
| **K74** (redefined) Leave-a-number rate | unique visitors with `secondary_intent` ÷ unique visitors, per arm | **The stronger signal.** Costly action, not a tap |
| **K13b** (new) Survey hand-off rate | `survey_link_click` ÷ visitors, per arm | Whether the framing sends people deeper |

**Pre-registered, before traffic:** K13 is **directional** unless the test reaches ≥291 visitors per arm.
It is *not* the primary H₀ test; **K14 (survey forced choice) is primary**, exactly as D3's fallback says.
This is written down now so nobody promotes a p-value after seeing it.

**Sample maths, stated honestly on the slide:**

| Visitors per arm | Smallest difference detectable |
|---|---|
| 30 | ~25 pp — not a test |
| 100 | ~17 pp |
| 291 | 10 pp |
| 1,090 | 5 pp |

---

## 6. Randomisation

| Route | Method | Quality |
|---|---|---|
| **₹0** | Same single link everywhere; the page splits A/B itself. Non-random exposure (who forwards, when). | Directional only. Must be labelled a convenience sample in the method section. |
| **₹500–1,000** | Meta ads, both variants running simultaneously, budget split 50/50, one audience: 20–30, Gachibowli/HITEC City radius. At ₹10–25 per click that is ~40–100 clicks. | **Randomised and simultaneous.** Still underpowered, but a real experiment with a defensible method. |

**Recommendation: spend the ₹1,000 here rather than on a third test order.** It converts the fake door from
"a page we shared" into "a controlled message test", which is a materially better method section — and the
₹900 test-order budget already buys promised-vs-actual delivery evidence that nothing else can.

**Sample-ratio check before reading anything:** chi-square on visitors per arm; p < 0.01 means assignment or
tracking is broken — fix and discard rather than interpret.

---

## 7. Decision needed

- **Option A (₹0):** rebuild the page, run organic, report K13/K74 as directional, K14 stays primary.
- **Option B (₹1,000):** rebuild the page, run Meta ads for 3–4 days, report the same KPIs as a randomised
  but underpowered experiment, K14 still primary.

Both need the same rebuild. Only the distribution differs.

---

## 8. What this instrument still cannot answer

1. Whether anyone would actually **order** — a tap is not a purchase.
2. Whether Ownly **specifically** wins — the page is unbranded by design.
3. Anything about **retention** — that is K30/K32 in the survey.
4. Whether first-time online orderers exist in the numbers Ownly claims — that needs order-level data
   nobody outside the company has.

These four sentences belong on the fake-door slide, next to the result.

---

## 9. Honest note on precedent

There is **no documented fake-door case study from any Indian consumer app** — not Swiggy, Zomato, Ola,
Flipkart, Meesho or Zepto. Rapido's own Bengaluru launch was a real soft launch, not an instrumented demand
test. The citable precedents are Dropbox's explainer-video waitlist, Zappos' manual fulfilment, and Buffer's
two-page pricing smoke test. Say that plainly rather than implying an Indian precedent exists.
