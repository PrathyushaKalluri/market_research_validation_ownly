# First-hand Ownly user check — Gachibowli, 2026-09-19

**Evidence label: FIRST-HAND USER OBSERVATION (n = 1).**
Source: a team member who is an active Ownly user, checking the live app at a Gachibowli
address on 2026-09-19. Not a measurement, not a sample — one observer, recorded because it is
**live** evidence and the audit workbook is three days old.

---

## What was asked and what came back

| # | Question | Answer |
|---|---|---|
| Q1 | Name restaurants on Ownly that are **not** on Swiggy/Zomato | **"Aanimuthyalu Unlimited is the only restaurant that is there in Ownly and not in Swiggy and Zomato."** |
| Q2 | Roughly how many restaurants does Ownly show at your address? | **221** |
| Q3 | Which well-known restaurants are missing from Ownly? | **"It doesn't have some very famous or very well-rated very high level of restaurants — ITC, Bawarchi, Taj, Domino's, KFC."** |

---

## What this resolved

### 1. It caught a bad pass in the audit workbook

The `thu_lunch` pass records `restaurant_listed = 'y'` for **all 30 rows**, with no
`restaurant_open` value, no timestamp and no prices. Zero variation carries zero information.
On that pass, Aanimuthyalu appears listed on Swiggy and Zomato; on the `wed_dinner` pass
(auditor A, timestamped, priced, with real variation) it is `n`/`n` on both.

**Q1 matches `wed_dinner` and contradicts `thu_lunch`.** The `thu_lunch` pass is therefore
excluded from coverage (rule R4 in `final_dashboard/scripts/01_consolidate_audit.py`) and
retained in `audit_clean.csv` with a flag. **`audit_slot_quality.csv` shows the test.**

An earlier analysis had used `thu_lunch` to "correct" the exclusive count from 1 to 0. That
correction was wrong and is withdrawn. Coverage on usable slots:

| | |
|---|---|
| On Ownly | 9 / 10 = **90.0%** |
| Ownly-only | **1** — Aanimuthyalu Unlimited |
| Missing from Ownly | 1 — Pizza Hut |
| Overlap (Ownly's list also on an incumbent) | 8 / 9 = **88.9%** |

### 2. It sets the size of the exclusivity claim

**1 confirmed exclusive out of ~221 listed restaurants.** H-LOCAL — "zero commission lets
Ownly carry local places the incumbents don't" — is therefore **alive but very small** on
current evidence. One exclusive is not a differentiated catalogue. It is not zero either,
and the audit frame was never built to find exclusives (see below).

### 3. It reframes the assortment gap — this is the substantive finding

Q3 points the gap at the **top end and the national chains**, not the local tail. Four
independent sources agree:

| Source | Evidence |
|---|---|
| **This check** (live, 2026-09-19) | ITC, Taj, Domino's, KFC, Bawarchi reported absent |
| **Price audit** (`wed_dinner`, 2026-09-16) | **Pizza Hut** listed on Swiggy and Zomato, **not on Ownly** |
| **Secondary research** (`01_secondary_research/`) | KFC and McDonald's **went offline on Ownly in Bengaluru, May 2026** |
| **YouTube comments** (n=275, coded) | A first-hand Ownly user: *"The number of restaurant need to improve"* |

**Why it matters:** 61.8% of catchment respondents would pay ₹30 **more** rather than lose
most of their usual restaurants. If the places Ownly is missing are the well-known ones, the
assortment constraint bites exactly where the survey says it hurts.

---

## The Bawarchi conflict — RESOLVED, and it produced the sharpest hypothesis in the study

Re-checked by the same user on 2026-09-19:

> **"Bawarchi is there, I checked wrong earlier — but Gachibowli is not there."**

So the brand **is** on Ownly; the **Gachibowli outlet is not**. Ownly serves a Gachibowli
address from a **further-away branch**. The audit's Ownly price and ETA for Bawarchi are
therefore valid and stay in the matched-basket comparison.

### H-OUTLET (new): the speed gap and the assortment gap may be the same problem

If Ownly lists brands but is missing their **nearest outlets**, it must fulfil from further
away — which should show up as a consistent delivery-time penalty across every restaurant,
not as a few slow outliers. **That is exactly the pattern in the data:**

| Restaurant | Ownly ETA | Best incumbent | Gap |
|---|---:|---:|---:|
| Cream Stone | 30.0 | 12.5 | **+17.5** |
| Shah Ghouse | 40.5 | 22.5 | **+18.0** |
| Bawarchi | 38.5 | 17.5 | **+21.0** |
| Paradise Biryani | 46.5 | 22.5 | **+24.0** |
| | | **median** | **+19.5 min** |

Four of four restaurants, every one penalised, range only 17.5–24 min. A logistics or
rider-supply problem would vary by order and by hour. **A supply-density problem looks like
this** — flat, structural, brand-independent.

**Why this matters strategically.** Assortment depth and delivery speed have been treated as
two separate weaknesses. Under H-OUTLET they are one: **outlet-level coverage**. Adding the
nearby branches would improve both at once. Under the alternative explanation — rider
allocation or batching — adding outlets would fix neither.

**Status: HYPOTHESIS, not a finding.** The audit recorded platform and restaurant name but
**not outlet name or distance**, so the mechanism is inferred from the ETA pattern and one
user's observation. It is consistent with the data; it is not demonstrated by it.

**What would test it:** re-run one price slot recording, for each restaurant and platform,
the **outlet name and stated distance** alongside the ETA. If Ownly's outlets are
systematically further, H-OUTLET holds. This is a cheap addition to an audit already designed.

**A nuance worth keeping.** The same root cause produces one consequence users tolerate and
one they do not: 94% of Gachibowli respondents accept a slower delivery for ₹30, but 61.8%
will **not** give up their usual restaurants for it. So if H-OUTLET is right, the damage is
done through **assortment**, not through speed.

---

## Limits of this evidence

- **n = 1**, and the observer is on the project team. It is used to *check the workbook* and
  to *size a hypothesis*, never to produce a coverage percentage.
- Q3 is recall, not a systematic search — absence of a brand from memory is weaker than the
  audit's observed `listed = n`.
- The audit frame (10 priced restaurants) was drawn from Ownly's own showcase page plus
  incumbent chains. **It selects for restaurants present on every platform and so cannot
  detect exclusives.** Any exclusivity figure from it is a property of the frame.

## What would settle it

A **long-tail coverage pass**: take 25–30 restaurants sampled from Ownly's own 221-item list
at a fixed Gachibowli address — deliberately skipping the showcase names — and check each on
Swiggy and Zomato. That is the only design that can measure exclusivity rather than assume it.
Listed under "test next", not claimed now.
