---
name: fake-door-design
description: Design or critique a fake-door, painted-door, smoke test or landing-page A/B test. Use when someone wants to test demand for a product that doesn't exist, test which value proposition/message wins, or asks whether a fake door is the right instrument. Covers the demand-vs-message distinction, sample-size reality, randomisation, page structure, ethics and what the result can and cannot claim.
---

# Fake-door and message-test design

## Step 1 — Decide which test this actually is

Most bad fake doors are the wrong instrument, not a bad page.

| Question being asked | Instrument | Outcome measured |
|---|---|---|
| Will anyone want this at all? | **Fake door** — a button where the feature would live, → "coming soon" + capture | Click rate on one door |
| Which *story* about it wins? | **Message test** — two near-identical pages/ads differing in headline only | Click rate per arm, compared |
| Will they pay, and how much? | **Pricing smoke test** — pricing page with tiers, capture on click | Tier clicked |
| What should the product even be? | **Concierge** (human visible) or **Wizard of Oz** (human hidden) | What people ask for, qualitatively |
| Will they commit? | **Pre-order / waitlist** | Money, email, phone — a costly action |

**If the arms differ in copy, it is a message test, not a demand test.** A message test cannot tell you
whether demand exists in absolute terms; a single fake door's CTR cannot tell you which message is better.
Say which one you are running, in writing, before building.

## Step 2 — Do the sample maths before writing a word of copy

Two-proportion z, α = 0.05, power 80%, baseline 20% CTR:

| Detect | n per arm | Total |
|---|---|---|
| +10 pp (20→30%) | ~291 | ~582 |
| +5 pp | ~1,090 | ~2,180 |
| +3 pp | ~2,937 | ~5,874 |

Then compare with realistically achievable traffic. If the honest answer is 80 visitors, the test detects
only ~20–25 pp differences — so **pre-register it as directional and name the instrument that carries the
hypothesis instead.** Deciding this after seeing the numbers is how a null becomes a fake positive.

## Step 3 — Randomise, or admit you didn't

- **Sticky, per-user assignment** (localStorage/cookie), never per-session or per-visit.
- **Organic sharing is not randomisation.** Who forwards what, and when, is confounded with the arm.
  It can still be run — label it a convenience sample in the method section.
- **A small paid budget buys randomisation**, which is usually worth more than the extra clicks: both
  variants run simultaneously to one audience with the budget split evenly.
- **Check sample ratio mismatch before reading any metric** (chi-square on visitors per arm). ~6% of
  experiments show SRM; it usually means the randomiser or tracking is broken.
- **No peeking.** Uncorrected optional stopping can push the false-positive rate from 5% to over 25%.
  Fix the stop (date or n) in writing before launch.
- **Two-tailed** unless there is a strong reason an effect can only go one way.

## Step 4 — Build the page for a 5-second decision

- Visitors decide in under 5 seconds; roughly 80% of attention is above the fold.
- **Under ~40 words before the CTA.** Headline ≤10 words, sub ≤20, one proof line.
- **Specific beats vague.** Real numbers, a named place, a concrete price. Generic value-speak
  underperforms badly.
- **One CTA**, no competing links or navigation.
- **Vary exactly one thing between arms.** If arm B bundles three ideas and wins, you have learned nothing
  about which idea won.
- **Minimise fields after the click.** Every field costs conversion; ask for one costly thing, not four
  cheap ones.
- Mobile first: most cold social traffic is a phone on mobile data.

## Step 5 — Measure a funnel, not a tap

A tap conflates curiosity with intent. Always pair it with one costly action:

| Signal | What it means |
|---|---|
| CTA click | Curiosity — cheap, noisy, but the headline outcome |
| Phone/email left, bill typed, quiz completed | Intent — effortful, far better discriminator |
| Hand-off click (to a survey or waitlist) | Depth of interest by arm |

## Step 6 — Ethics: disclose at the click

- Reveal immediately on the CTA, before any effortful step: *"No app, no order, no payment — we're testing
  which idea people respond to."* Not a delayed debrief.
- Never collect payment you cannot honour; never invent urgency or scarcity; never imply a real company
  exists if it does not.
- For student research this is light-touch deception: the click happens before disclosure, which is exactly
  what makes it measurable — and the disclosure is what makes it defensible.
- Fake-dooring *inside* a live product carries reputational risk with existing users; a standalone page does not.

## Step 7 — Write down what it cannot claim

Put these on the slide, next to the result:
1. A click is not a purchase.
2. The audience is whoever your channels reached, not the market.
3. It measures the **message**, not the product.
4. It says nothing about retention.

## Reference points worth citing

Dropbox's explainer-video waitlist (demand), Zappos' manual fulfilment (Wizard of Oz), Buffer's two-page
pricing smoke test (willingness to pay), Netflix's unavailable-title autocomplete (content demand, blog-sourced).
**There is no well-documented fake-door case study from an Indian consumer app** — say so rather than implying one.

## Red flags when critiquing an existing design

- The primary KPI needs 10× the traffic the team can get.
- Arms differ in more than one dimension.
- The page takes longer to read than the decision it asks for.
- Distribution is organic but the write-up says "randomised".
- The same contrast is already being tested by the survey.
- The disclosure comes after the effortful step instead of before it.
