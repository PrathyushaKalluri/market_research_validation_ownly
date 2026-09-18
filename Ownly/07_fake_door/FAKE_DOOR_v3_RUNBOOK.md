# Fake Door v3 — Runbook (build, admin view, Meta ads, stop rule, precedents)

**Written:** 2026-09-17 · **Page:** `prototype/index.html` (copy in `gachibowli-food-study/index.html` for Netlify Drop)
**Page version:** `2026-09-17.v3b` · **Experiment ID:** `hyd_vp_fakedoor_v1` (unchanged, so the collector needs no redeploy)
**Design:** `FAKE_DOOR_REDESIGN_v3.md` · **Distribution chosen:** Option B, ₹1,000 Meta ads over 2 days (D15)

---

## 1. What was built

| Part | v2 (old) | v3 (now) |
|---|---|---|
| Arms | A Bengaluru total price · B Hyderabad local + reliable (3 ideas bundled) | **A `A_everyday_low_price`** · **B `B_discount_led`** — one variable: *why* dinner is cheaper |
| Above the button | 131 words, bill table, 3 bullet points | Headline, one sub line, one real-price proof line (~40 words) |
| After the tap | Disclosure → bill calculator (2 inputs) → 3-question mini-survey → survey | **"Coming soon — not taking orders in Gachibowli yet" → one tap question → survey button** (no research disclosure, v3b) |
| Personal data | None | None (the spec's WhatsApp-number idea was dropped, see §6) |

**The two arms, as a visitor sees them:**

| | Arm A — everyday low price | Arm B — discount-led |
|---|---|---|
| Headline | Dinner costs less here. Every day, not just today. | ₹100 off your first three dinners. |
| Sub | Restaurants list their own menu prices. No delivery, platform or packaging fees. | A new food delivery app for Gachibowli. Get ₹100 off each of your first three orders. |
| Proof | A real Gachibowli order on 16 Sep: ₹188 here, ₹259 on the usual app. | A real Gachibowli order on 16 Sep: ₹259 on the usual app, ₹159 with the offer. |
| Button, note, coming-soon panel, question, survey | identical | identical |

The ₹259 and ₹188 are real (Cream Stone, slot 1, `audit_data_slot1.csv`). Arm B's ₹100 offer is hypothetical;
the post-tap panel says only that the service is not taking orders yet.

**The post-tap question:** *"When it launches, would you try it for your next dinner order?"*
`Yes, even without an offer` · `Only with a first-order offer` · `Not for me` · Skip.
This is the costly-action replacement and it answers the v3 question directly: if Arm A still produces lots of
"only with an offer", the everyday-low-price story is not carrying the first order by itself.

---

## 2. How a visitor gets an arm (your question)

**Neither alternating nor in blocks.** Each new browser that opens the link gets an **independent 50/50 coin
flip** (`crypto.getRandomValues`), and the result is **saved in that browser** (`localStorage`).

| Situation | What they see |
|---|---|
| Person 1 opens the link | Coin flip → say B. Saved. |
| Person 2 opens the same link | A fresh, independent flip → could be A or B. **Not** forced to be A. |
| Person 1 reloads, or comes back tomorrow | B again — the saved arm wins. They are counted once. |
| Person 1 opens it in a different browser (e.g. Instagram's in-app browser, then Chrome) | A new flip. Unavoidable without logins; small, and equal across arms. |

**Why not strict alternation (A, B, A, B)?** Alternation is predictable and can line up with patterns in traffic
(two friends opening it one after another always split). **Why not blocks (first 10% A)?** Early visitors differ
from late visitors — time of day, which group posted — so blocks mix time into the arm comparison. An independent
coin flip is the only one of the three where nothing about *who* or *when* can predict the arm.

**The cost:** the split is close to 50/50 but never exact. With 80 visitors, 35/45 is normal. That is why the
analysis runs a **sample-ratio check** (chi-square on visitors per arm) *before* reading any rate: p < 0.01 means
the assignment or the tracking is broken, not that one arm is more popular.

---

## 3. Admin: seeing both arms

| URL | What it does | Data sent |
|---|---|---|
| `https://gachibowli-food-study.netlify.app/?admin` | **Both arms side by side** in two phone-sized frames, tap-through works; shows this browser's own saved arm; "Clear this browser's arm" to re-flip; "Simulate 1,000 visitors" to see the split | **Nothing** |
| `…/?v=A` or `…/?v=B` | One arm full-size with a dark QA bar (Arm A / Arm B / Both) | Rows sent **flagged `is_qa = true`**, excluded from analysis. Use this to check the sheet end to end |
| `…/?utm_source=…` (plain link) | What real visitors get: random, sticky, no bar | Real rows |

Never share a `?v=` or `?admin` link. Rows from them are thrown away, and the person sees one arm by choice, not chance.

---

## 4. The ₹1,000 Meta ads plan (2 days)

### 4.1 The one design rule: the ad must not carry either message

The page does the randomisation. The ad is **one neutral ad** that sends everyone to the **same plain link**.
If the ad said "₹100 off", only discount-seekers would click, and Arm A would be judged on an audience the
Arm B message recruited. A neutral ad means both arms receive the same kind of stranger.

*(The alternative — two ads, each with its arm's headline, run as a Meta A/B test — tests the ad instead of the
page, lets Meta's delivery algorithm shape each arm's audience, and needs two budgets from ₹1,000. Not recommended here.)*

### 4.2 Setup, step by step

1. **Facebook Page.** Ads need one. Create a neutral page, e.g. "Gachibowli Dinner Delivery". **No Ownly / Rapido
   name, logo or colours anywhere** (same rule as the site name).
2. **Ads Manager → Create → Objective: Traffic.** Conversion location: **Website**. Performance goal:
   **Maximise number of landing page views** (counts people whose page actually loaded, not accidental taps).
3. **Budget and schedule:** ₹500/day, **fixed start and end** — default **Sat 19 Sep 2026 00:00 → Mon 21 Sep
   2026 00:00 IST**. Meta adds **18% GST** in India, so expect ~₹1,180 charged. Ads go through review (often
   minutes, can be up to 24 h), so submit on **Fri 18 Sep**.
4. **Audience:** Location → drop a pin on Gachibowli, smallest radius that covers Gachibowli, Kondapur,
   HITEC City and Financial District (~5 km). Choose "people living in or recently in this location". **Age
   20–30**, all genders. If Ads Manager offers *Advantage+ audience*, set age as a **hard control** (not a
   suggestion), otherwise Meta may deliver outside 20–30. No interest targeting (it would narrow the audience
   towards food enthusiasts). Special ad category: none.
5. **Placements:** Advantage+ placements is fine (Facebook + Instagram feeds, Stories, Reels).
6. **The ad (single image, 1080×1080 or 1080×1350):**
   - Image: a plain photo of a dinner plate or delivery bag. No logos, no prices, no "₹100 off".
   - Primary text: *"A new food delivery idea for Gachibowli. Would you use it? Take a 10-second look."*
   - Headline: *"Dinner delivery in Gachibowli"*
   - Button: **Learn more**
7. **Website URL (paste exactly):**
   ```
   https://gachibowli-food-study.netlify.app/?utm_source=meta&utm_medium=paid_social&utm_campaign=hyd_vp_fakedoor_v1&utm_content=neutral_ad_1
   ```
   Meta appends `fbclid=…` — harmless. Meta's link-preview crawler (`facebookexternalhit`) is auto-flagged as a bot.
8. **Before publishing:** open the URL on your own phone *from Chrome*, confirm the page loads, then **Clear this
   browser's arm** via `?admin` so your own visit is not in the data. (Or just use `?v=A` for your checks.)

### 4.3 What ₹1,000 realistically buys

| Assumption | Landing-page views | Per arm |
|---|---|---|
| ₹25 per view (pessimistic) | ~40 | ~20 |
| ₹10 per view (optimistic) | ~100 | ~50 |

That is **below the ≥30-per-arm floor in D3 in the pessimistic case, and far below the ~291 per arm needed to
detect a 10-point gap.** It is still worth running — it is the only *strangers, same time, randomised* evidence
in the project — but it is pre-registered as **directional**, and **K14 (survey forced choice) stays primary**.

**To add sample without breaking the design:** during the same 48 hours, the team may also post the **same plain
link** in groups, with its own `utm_source` (e.g. `whatsapp_iiit`). The page randomises these visitors too, so arms
stay comparable. Report paid and organic **separately first**, and pool them only if both pass the sample-ratio check.

---

## 5. Stopping rule (pre-registered, replaces the 30 Sep / 300 rule for v3)

| Item | Rule |
|---|---|
| Window | **Sat 19 Sep 2026 00:00 IST → Mon 21 Sep 2026 00:00 IST** (48 h), matching the ad schedule |
| If Meta review delays the start | Shift **both** dates by whole days, and write the new dates here **before** the first ad impression |
| Early stop | **None.** Not for a "clear winner", not for a slow start |
| Allowed peeking during the window | Total rows arriving; visitors per arm (sample-ratio check). **Not** CTA or answer rates per arm |
| Analysis filter | `page_version = 2026-09-17.v3b`, `is_qa = false`, not bot, window above |
| Primary read | K13 CTA rate per arm, **directional**; K74 (v3) = "yes" or "offer-only" answers per arm; survey hand-off per arm |

**Analysis command** (after exporting the sheet to `08_clean_data/raw/fakedoor_events_raw.csv`):
```
python3 07_fake_door/analyze_fakedoor.py analyse --events 08_clean_data/raw/fakedoor_events_raw.csv \
  --out 09_analysis/fakedoor --page-version 2026-09-17.v3b --start 2026-09-19 --end 2026-09-21
```
The script now also reports `try_yes_rate`, `try_offer_only_rate` and `try_offer_only_given_cta` per arm.

---

## 6. Why no phone number

The redesign spec suggested "leave a WhatsApp number" as the costly action. It was dropped because the collector,
the privacy note on the page and QA check "no personal data anywhere in the sheet" all promise no personal data,
and adding a phone field would break all three and need consent wording. The one-tap question keeps the page
personal-data-free, needs **no collector change** (it reuses the whitelisted `action` field), and asks something
more useful for v3 than a number would: *does the saving need an offer attached to earn the first order?*
Its weakness: it is asked after the disclosure, so it is stated intent, not behaviour — say so on the slide.

---

## 7. Precedents: Dropbox, Zappos, Buffer

None of the three ran a *two-arm message test*. All three are single-door **demand** tests, which is why they are
precedents for the *method*, not for our comparison.

| | Dropbox (2007–08) | Zappos (1999) | Buffer (2010) |
|---|---|---|---|
| **The question** | Will people want file sync badly enough to wait for it? | Will people buy shoes online without trying them on? | Will people pay for scheduled social posts, and how much? |
| **The door** | A short screencast demo of a product that was not publicly usable, posted to Hacker News and later Digg, with in-jokes aimed at that audience | A website with photos of shoes taken at local shoe shops. No inventory: when an order came in, the founder bought the pair at retail and shipped it | A landing page describing the product with a "Plans and pricing" button. Tapping it said, in effect, *you caught us before we're ready*, and asked for an email |
| **Second step** | Join the beta waitlist (email) | Pay the real price | Added later: a pricing page with free and paid tiers **between** the button and the email field |
| **The input it produced** | Waitlist sign-ups — widely reported as jumping from ~5,000 to ~75,000 overnight after the second video (Eric Ries, *The Lean Startup*) | **Real paid orders** — proof that the behaviour existed, at a loss on every order | Emails, and **which price tier people tapped** — willingness to pay before any code was written |
| **Test type** (see `fake-door-design` skill) | Demand / waitlist | Wizard of Oz (manual behind the scenes) | Two-step pricing smoke test |

**What we copy from each:**

| From | Lesson | Where it is in v3 |
|---|---|---|
| Dropbox | The door must speak to the audience it is shown to; a signal costlier than a view (the waitlist) | Real Gachibowli prices in the proof line; the post-tap question |
| Zappos | Money is the only signal that is not an opinion | **Not** the page — that is the 3 test orders (₹900) in the audit plan. Keep them |
| Buffer | **Tap → a second, costlier step** separates curiosity from intent; the second step can reveal *how* people want it | Exactly our structure: tap → "coming soon" → "without an offer / only with an offer" |

**Disclosure (changed 2026-09-17, v3b, user decision):** like Buffer's *"you caught us before we're ready"*, the
page does not say it is a study. After the tap it says only *"We're not taking orders in Gachibowli yet"*, which is
true. No payment and no personal data are ever collected, and the page is unbranded. The main survey, if they open
it, is where the research context appears. **If your course or ethics sign-off requires a debrief, add it there.**

**Honest note (unchanged from the redesign spec):** there is no well-documented fake-door case study from an
Indian consumer app. Cite these three as method precedents, not as market evidence.

---

## 8. Your checklist, in order

| # | Step | Done when |
|---|---|---|
| 1 | Drag the `gachibowli-food-study` folder onto the existing site in Netlify (Deploys → drag and drop) | `…netlify.app/?admin` shows both arms |
| 2 | Open `?v=A`, tap through, answer; repeat for `?v=B`; check rows in the sheet say `2026-09-17.v3b`, `is_qa = true`, `action = try_…` | Both arms' rows visible |
| 3 | Build the Facebook Page + ad (§4.2), schedule Sat 19 Sep 00:00 → Mon 21 Sep 00:00 IST, submit Fri 18 Sep | Ad status "Active"/"Scheduled" |
| 4 | Optional: post the plain link with its own `utm_source` in groups during the same window | Logged in `experiment_tracker.csv` |
| 5 | Mon 21 Sep: export the sheet, run the §5 command | `09_analysis/fakedoor/fakedoor_report.md` |
