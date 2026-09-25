# Ownly · Gachibowli — Executive Summary

**Compiled 2026-09-21** · Rebased onto the canonical catchment sample

**Survey n = 40** (Gachibowli catchment, 20–35; 124 responses received) · **Price audit** 4 matched
baskets, 10-restaurant frame, one Gachibowli address, wed_dinner 2026-09-16 · **App-store reviews**
29 coded of 37 · **Social** 264 coded of 420, plus 97 first-hand accounts of 123 · **YouTube** 105
coded of 275 · **Interviews** 1 documented transcript + team-reported (count UNKNOWN) ·
**Fake door** designed and powered, **0 events — not fielded**

> **Note on the base change (read this if you have seen an earlier version).**
> The 2026-09-18 draft of this summary was computed on **n = 46** — respondents who had ordered food
> online in the last four weeks. Every figure below is now computed on **n = 40**, the Gachibowli
> catchment, which is the base the KPI table, the dashboard and the analysis pipeline all use. The two
> bases answer slightly different questions and produced slightly different numbers for the same facts
> (for example membership 82.6% → 82.5%, speed trade-off 84.8% → 92.5%). Nothing was re-collected and
> no conclusion changed direction. **The catchment base is canonical; quote these numbers, not the
> older ones.** Source of record: `data/kpi_table.csv`, built by `scripts/`.

---

## Business problem

How large and durable must Ownly's price advantage be to break Swiggy/Zomato lock-in in Gachibowli,
and what restaurant coverage, discovery and delivery experience are required so that price-led trial
becomes repeat usage?

Ownly is already live at the audited Gachibowli address. The decision is per-tactic —
**KEEP / ADAPT / DEPRIORITISE** on the Bengaluru playbook — not whether to enter.

## What we found

**1. The price advantage is real, structural, and largely invisible to the people who matter.**
On list price plus fees, Ownly was cheapest in **4 of 4** matched baskets, median saving **₹114.50
(30.5%)**. Non-food charges are **5.2%** of an Ownly bill against an incumbent median of **23.4%**
(on zero-discount captures: Ownly 4.8%, Zomato 15.1%, Swiggy 27.4%). Unlike every challenger in the
historical record, this comes from removing fees, not from funding discounts.

But **82.5%** of the catchment holds an incumbent membership <sub>(95% CI 68.0–91.3)</sub>, and a
membership alone — before any coupon — flips **1 of 4** baskets. A coupon flips **2 of 4**. Most
respondents never see the view Ownly wins.

**2. Assortment — not price, speed or reliability — is the binding constraint.**
Holding ₹30 constant across three forced choices with the same 40 respondents:

| Users will trade… | for ₹30 | 95% CI | |
|---|---|---|---|
| **Speed** (15 min slower) | **92.5%** will | 80.1–97.4 | not a constraint |
| **Reliability** (3-in-10 late vs 1-in-10) | **72.5%** will | 57.2–83.9 | not a constraint |
| **Their usual restaurants** | only **35.0%** will | 22.1–50.5 | **the constraint** |

McNemar exact, paired, assortment vs speed: **p = 1.5 × 10⁻⁶** (24 respondents accepted a delay but
refused to lose restaurants; exactly 1 did the reverse). Assortment vs reliability: **p = 0.0026**.

This **falsified our own pre-registered prediction P3**, that Ownly's ~17-minute ETA deficit would
block adoption. It does not.

**3. The advantage erodes to nothing at a real checkout.**
Switch-Threshold Coverage — the share of person × restaurant pairs where Ownly's observed saving meets
what that person said they need to switch (132 pairs; 33 respondents who named a figure × 4 baskets):

| View | Coverage | Median saving |
|---|---|---|
| List price + fees | **81.1%** | +₹114.50 |
| With an incumbent membership | **56.1%** | +₹77.59 |
| After an incumbent coupon | **27.3%** | **−₹28.07** — Ownly is dearer |

The median recurring saving people say they need is **₹30** (n = 33 named a figure; 4 said no amount
would move them, 3 did not know — held out, not coded as zero).

**4. Ownly sells the same restaurants, more slowly.**
**88.9%** cross-platform overlap; audit-frame coverage **90%** (9 of 10). One Ownly-only restaurant
observed, one missing. This is the "no new use case" pattern the incumbents named publicly, and our
own audit confirms both premises independently. Median quoted-ETA gap **+17 min**, flat across all
four restaurants — the signature of supply density rather than logistics, though the audit did not
record outlet distances, so the mechanism is inferred and not shown.

**5. Rapido is access, not discovery.**
**24 of 40** used Rapido in the last four weeks. Of the **33** who answered the in-app question, only
**5 (15.2%)** had noticed food inside the app <sub>(95% CI 6.7–30.9)</sub> — roughly an **85%
discovery gap**. Funnel: awareness **42.5%** → browse **17.5%** → trial **5.0%** (2 of 40; interval
1.4–16.5%, effectively uninformative, and the 4-week window mostly predates the Hyderabad rollout).

**6. Nobody believes the prices will last.**
**87.5%** agree a new app's low prices rise once it becomes popular <sub>(95% CI 73.9–94.5)</sub>.
Stated continuation after a ₹100 intro offer ends is **25.0%** <sub>(95% CI 14.2–40.2)</sub>.

## Why it matters

Ownly has escaped the mechanism that killed Foodpanda and Uber Eats India — its saving is structural,
not rented. But it has inherited two others: it attacks the side of the market that was never scarce
(restaurants already multi-home), and it offers no new use case. The price advantage it does have is
being **communicated as a comparison that any incumbent coupon can falsify**, to an audience that is
83% membership-holding and 88% sceptical.

## KEEP

- **Zero platform, packaging and surge fees.** The structural advantage, and it survives without subsidy.
- **Transparent everyday pricing.** The observed saving clears the stated switching bar of every
  respondent who named one.

## ADAPT

- **The "cheaper than Swiggy/Zomato" claim** → reframe on the everyday bill. Against members, the
  comparison is often false at their checkout.
- **Restaurant breadth** → named local depth. Breadth reproduces the incumbent catalogue.
- **Rapido as a channel** → build and measure discovery; access alone is not producing trial.

## DEPRIORITISE

- **Speed / ETA parity investment.** 92.5% accept 15 minutes slower for ₹30. Our own prediction that
  this blocked adoption was falsified.
- **Deeper first-order discounts.** They buy the trial the historical record says does not stick, and
  only 25% say they would stay once the offer ends.

## H₀ result

| | |
|---|---|
| **Behavioural H₀** (first-order conversion) | **NOT DIRECTLY TESTED** — the fake-door experiment was designed, built and powered but never fielded (0 events). No substitute is claimed. |
| **Stated-preference analogue** | Service P 18 vs Service Q 11 (11 could not choose). Among the 29 expressing a preference, P share **62.1%**, exact binomial **p = 0.2649**, 95% CI 42.3–79.3% → **FAIL TO REJECT H₀**. |
| **Paired analogue** | Top-2-box trial intent, McNemar exact: 6 discordant each way, **p = 1.00**, n = 40 → **FAIL TO REJECT H₀**. |

The two *bundled* propositions did not separate — and **11 of 40 (28%) could not choose between them
at all**, which is itself a finding about how distinct they are. **The attributes inside them separated
sharply**, which is the more informative result and the one the GTM decision rests on.

## What the interviews added

Interviews were conducted after the first build of this dashboard. They did two things the survey
could not.

**1. They resolved a contradiction.** The survey says **72.5% will accept worse reliability for ₹30**;
the app-store record says fulfilment failure is **72.4%** of coded reviews (29 coded of 37), and among
first-hand Ownly accounts on social it is **49.5%** against **18.9%** in general discussion.
Interviews report that people leave an app after **frequent bad orders**. Users *accept* a reliability
risk when choosing and *leave* after it repeats — different decision moments, both true.
**Reliability is a churn driver, not a trial blocker.**

**2. They redirected a recommendation.** We measured an ~85% discovery gap inside Rapido and were about
to recommend fixing the in-app placement. Interviews say trial comes from **a friend's recommendation,
influencers, Instagram and YouTube** — the documented interviewee heard about Ownly **from her
brother**. The higher-value experiment is a **referral or creator-led trial mechanism**, not a
placement change.

**One interview claim we could not confirm.** Interviews report that students weight money over time
while general users weight time over money. In the catchment, non-students took the cheaper, slower
option **100% (8 of 8)** against students' **90.6% (29 of 32)** — the opposite direction, and
**Fisher exact p = 1.00**, i.e. no detectable difference at this base. The switching *threshold* does
differ directionally (**students ₹30 vs working professionals ₹50**, n = 7 professionals). Reported as
partially supported and underpowered, not as validated. *(An earlier draft quoted p = 0.637; that was
computed on the superseded n = 46 base and is withdrawn.)*

**Two things only the interviews see.** Hygiene cannot be judged through an app ("ratings measure
taste, not hygiene"), and a **very low price itself raises a quality doubt** — "if biryani is ₹100, is
it good?" The survey instrument is blind to both, and both are costs of a price-led claim.

## What the public argument is actually about

275 verbatim YouTube comments were retrieved from two Rapido/Ownly explainer videos; 105 were coded.
The single largest theme is one this study had not examined at all: **rider economics — 27.6% of coded
comments and 1,167 likes**, repeatedly arguing riders earn more per hour from bike taxi than from food
delivery. That is a **supply-side** version of the thin-economics risk, and neither our survey nor our
audit can see it.

Only **3 of 275** commenters claim first-hand Ownly use. One independently reproduces our audit's
central finding: *"Ownly is not that cheap .. they have no discount on any restaurant .. same menu
available in Swiggy with lesser cost after discount."* Another names the assortment constraint:
*"The number of restaurant need to improve."*

Caveat: these are self-selected viewers of Rapido-favourable videos, national rather than Gachibowli,
and the counts are **shares of coded comments — not failure rates and not population incidence**.

## What we still do not know

- **Whether any of this converts.** Every switching, trial and repeat figure is stated intent. The
  fake door is built and the collector is live; it has not been run.
- **How many people we actually spoke to.** Interviews were conducted, but only one transcript is
  documented and the total count is **UNKNOWN**. No interview finding carries a prevalence figure.
- **Whether the price gap holds** beyond one dinner slot at one address with n = 4 matched baskets.
- **Whether Ownly's quoted ETA is honest** — no test orders were placed.
- **Whether the business model works.** Ownly charged ₹0 to the customer and takes 0% commission in
  every captured row. Observed revenue per order in Gachibowli was **₹0**. CAC, CLV, retention,
  market share and contribution margin per order are **NOT ESTIMABLE** from any evidence in this
  repository, and no value has been imputed for them.

## Test next, in order of decision value

1. **Run the fake door.** It is the only instrument that yields behavioural first-order conversion —
   what H₀ is actually about. Powered for a ~20pp effect at 200 visitors; see
   `07_fake_door/FAKE_DOOR_v3_RUNBOOK.md`.
2. **Audit named local restaurants, not showcase chains.** The strategy the evidence points to depends
   on depth we have not measured. Ownly lists 221 restaurants at the audited address; we sampled 10.
3. **Place the 3 test orders.** Quoted ETA is not delivery time.
4. **Document the interviews already done** — confirm the count, back-fill the tracker, human-verify
   quotes — then run the remaining ones to quota.
5. **Re-audit from a membership-holding account** — that is what 82.5% of the target actually sees.

---

*Every figure above is computed from `data/*.csv` by `scripts/`. Where a figure could not be computed
from the evidence held, it is marked NOT ESTIMABLE rather than estimated. Pre-analysis plan frozen at
`09_analysis/PAP_frozen_2026-09-21.md`; deviations logged in `_ops/decisions.md` (D17, D18).*
