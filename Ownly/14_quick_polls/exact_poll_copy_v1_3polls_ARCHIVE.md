# WhatsApp / Instagram Polls — exact copy

**Owner: Person 2. Cost: ₹0. Time: 5 minutes to post, results by evening.**

## What polls are for, and what they are not for
A poll is a **fast, single-variable sanity check on a large, cheap sample** — useful for one blunt
question where a nuanced answer isn't needed. It is **not** a substitute for the survey and must never
be used for a trade-off question, because a poll strips away the thing being traded.

## Contamination rule — this matters
**Never post a poll and the survey link in the same group.** A poll primes the respondent: someone who
has just voted "reliability" will answer the survey's Section 7 differently.

- **Poll groups** and **survey groups** are two disjoint lists. Write them down in `poll_tracker.csv`
  before posting anything.
- Use polls in groups where a full survey ask would be unwelcome or wouldn't convert (large, loose,
  low-engagement groups) and save the survey for groups where you can actually ask for 7 minutes.
- Poll results are reported **separately**, never merged into survey counts, never added to any n.

---

## Poll 1 — the diagnostic that maps straight to H₀ ★ *(post this one first)*

> **Quick one for a college project 🙏 Your food-delivery app is ₹30 cheaper than the other one on a typical order. Which would make you actually switch to it?**
>
> 1️⃣ ₹30 cheaper, every time
> 2️⃣ It actually arrives when it says it will
> 3️⃣ It has the restaurants I actually want
> 4️⃣ Honestly, I'd just stay where I am

- **Multiple answers: OFF** (forcing one choice is the entire point)
- **Target: 60+ votes**
- **Decision it informs:** the relative weight of price / reliability / assortment in a single blunt
  read, as a cross-check on survey Q16–Q18 and on the fake-door A-vs-B result. If option 1 dominates
  here but Service Q wins the survey, that gap is worth a slide on its own.

## Poll 2 — awareness, in one tap

> **Have you heard of "Ownly", the food-delivery service from Rapido? (college project, 1 tap)**
>
> 1️⃣ Yes, and I've ordered on it
> 2️⃣ Yes, but never ordered
> 3️⃣ Never heard of it

- **Multiple answers: OFF** · **Target: 60+ votes**
- **Decision it informs:** an independent read on awareness and the awareness→trial gap, on a much
  larger n than the survey will reach. Post this in the **largest** groups available.
- ⚠ This poll names Ownly, so any group receiving it is **permanently disqualified from the survey**.
  Choose those groups deliberately.

## Poll 3 — fee pain *(only if 1 and 2 are already out)*

> **Last time you ordered food: did the final amount feel fair for what you got? (1 tap, college project)**
>
> 1️⃣ Yes, felt fair
> 2️⃣ No — the extra charges were too much
> 3️⃣ No — the food itself was overpriced
> 4️⃣ Didn't really look

- **Multiple answers: OFF** · **Target: 50+ votes**
- **Decision it informs:** separates *fee* pain from *price* pain — which is exactly the difference
  between Service P's second bullet and its first.

---

## Posting rules
- **Ask the admin first** in any group you don't own (script J in `04_interviews/outreach_scripts_v3.md`).
- Post between **12:30–13:30** or **20:00–22:00** — the two windows when people are on their phones
  thinking about food.
- One poll per group. Never two.
- Do not comment under your own poll to nudge it. Let it sit.
- **Close the poll and screenshot it** when you log the result. WhatsApp poll results move; the
  screenshot is the record.

## Logging
Fill `poll_tracker.csv` the moment you post, not afterwards. Save each screenshot as
`poll<N>_<groupname>_<date>.png` in this folder.

## How these get reported
> "Three WhatsApp polls in [N] groups returned [n] votes. Polls are a convenience sample with no
> screener — no age check, no catchment check, no category-usage check — so they are used only as a
> directional cross-check on the survey, and are never pooled with it."

Never write a poll percentage without that sentence nearby.
