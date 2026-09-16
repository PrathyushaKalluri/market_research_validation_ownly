# WhatsApp Polls — exact copy (v2, 2026-09-16)

**Owner: Person 2. Cost: ₹0. Time: 5 minutes to post.**
**Down from 3 polls to 1.** Two of the three original polls were folded into Survey v6 instead. The
reasoning is in §1 — read it before asking for a poll to be added back.

---

## 1. The rule we now use: what belongs in a poll, and what doesn't

A poll gives you **one unlinked number from a large, unscreened crowd, today.**
A survey gives you **one row per person**, which you can cut, cross-tabulate and screen.

> **Decisive test: if you would ever want to say "…among students" or "…among people with a membership",
> the question belongs in the survey.** Poll answers cannot be joined to anything — you get a bar chart
> and nothing else. That single constraint settles almost every case.

There is also a real, non-obvious cost. `_ops/decisions.md` D8 requires poll groups and survey groups to
be **disjoint**, because a poll primes the very frame the survey is trying to measure. So:

> **Every group you spend on a poll is a group you cannot use for the survey.**

With a target of 80 Hyderabad responses and only a handful of group permissions, polls are now expensive.
Spend one only where it buys something the survey genuinely cannot.

### What happened to the original three polls

| Original poll | Verdict | Why |
|---|---|---|
| **Poll 1** — "₹30 cheaper vs arrives on time vs restaurants vs stay put" | ❌ **Dropped** | Redundant. Survey **S9-Q1** already asks this ranking with 7 options on a screened sample, and **Section 6** tests the same three levers properly — one variable at a time, with ₹30 held constant. The poll version forced a single choice between four unlike things, which is a weaker question, not a faster one. |
| **Poll 2** — "Have you heard of Ownly?" | ✅ **Kept** (now Poll A) | The one case where a poll genuinely beats the survey. See §2. |
| **Poll 3** — "Did the final amount feel fair?" | ➡️ **Moved into the survey** as **S5-Q4** | It was a real gap — v6 had no fee-pain question at all. In the survey it sits straight after the amount question, so it's anchored to a bill the respondent just recalled, and it can be cut by segment and crossed against the trade-offs. As a poll it would have been a lone percentage. |

Also promoted into the survey while we were at it: **memberships** (new **S3-Q2**). Swiggy One / Zomato
Gold is the strongest single predictor of *not* switching apps, and it was appearing only as an answer
option buried in two other questions. It is now a segment we can cut everything else by.

---

## 2. Poll A — Ownly awareness ⭐ *the only poll we run*

> **Post this in large groups you have already written off for the survey.**

```
Have you heard of "Ownly", the food delivery app from Rapido? (college project, 1 tap 🙏)

1️⃣ Yes, and I've ordered on it
2️⃣ Yes, but never ordered
3️⃣ Never heard of it
```

- **Multiple answers: OFF** · **Target: 80+ votes** · **Post at 12:30–13:30 or 20:00–22:00**
- ⚠️ This poll says the word "Ownly", so **any group that receives it is permanently disqualified from the
  survey.** Choose those groups deliberately and write them down before posting.

### Why this one survives the test in §1

Three reasons, and it needs all three:

1. **The survey's awareness number is biased upward and we can't fix it from inside the survey.** People
   who click a food-delivery survey are more interested in food apps than people who don't. So v6's
   awareness estimate (S8-Q1) is measured on a self-selected sample that over-represents exactly the
   people most likely to have heard of Ownly. A one-tap poll in a general group catches people who would
   never open a 6-minute form. **The gap between the two numbers is itself the finding** — and it is the
   only honest way we have to show the direction of our own sampling bias.
2. **Awareness is a bare prevalence question.** It's the rare case where we don't need to cut by anything.
   "What share of 20–30s around here have heard of it" is a complete answer on its own.
3. **n.** The survey will give roughly 80 Hyderabad responses (±11 points). A poll can plausibly return
   200+. For a single headline percentage on slide 9, that difference is real.

### How it gets reported
Poll and survey awareness numbers go **side by side, never merged**, with this sentence attached:

> "The poll has no screener — no age check, no area check, no category-usage check — and no denominator we
> control. It is shown only as a directional cross-check on the survey's awareness figure, and the gap
> between the two is a read on our own sampling bias, not a population estimate."

---

## 3. Posting rules
- **Ask the admin first** in any group you don't own (script J in `04_interviews/outreach_scripts_v3.md`).
- Post between **12:30–13:30** or **20:00–22:00** — when people are on their phones thinking about food.
- One poll per group. Never two.
- Do not comment under your own poll to nudge it. Let it sit.
- **Close the poll and screenshot it** when you log the result. WhatsApp poll results move; the screenshot
  is the record.
- Log in `poll_tracker.csv` the moment you post, not afterwards. Save screenshots as
  `pollA_<groupname>_<date>.png` in this folder.

## 4. If you have spare groups after the survey is saturated

Only then, and only if someone asks for a second number, the next-best poll-shaped question is:

```
Roughly how many times did you order food delivery last month? (college project, 1 tap)

1️⃣ None
2️⃣ 1–3
3️⃣ 4–7
4️⃣ 8 or more
```

- Doesn't name any brand, so it does **not** disqualify the group from the survey.
- Use it as a **category-usage sanity check**: if the poll's order-frequency distribution looks very
  different from the survey's, our respondents are heavier users than the population we're describing,
  and the limitations slide should say so.
- **Do not run this before the survey is distributed.** It is a spare-capacity check, not a priority.
