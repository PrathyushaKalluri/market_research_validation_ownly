# Ownly Gachibowli — Fake-Door Experiment

Everything needed to run, log and analyse one defensible fake-door study.
Full design and pre-registration: **`EXPERIMENT_DESIGN.md`** — read that first.

**What this study is for, in one sentence:** find out what Gachibowli actually wants to eat, which
places they want it from, how they want to be charged for it, and what happens to the order when the
place they want is not on the app.

| File | What it is |
|---|---|
| `EXPERIMENT_DESIGN.md` | The design. Critique of the method, hypotheses, metrics, decision rules, ethics, claims matrix, slides |
| `fake_door.html` | The prototype. Open it in any browser — no server, no internet |
| `mobility_entry.html` | The H4 discovery mock (generic ride app, **not** a Rapido replica) |
| `apps_script_collector.gs` | Optional Google Sheets backend |
| `analyse_results.py` | Funnel, primary metric, Fisher exact, Newcombe CI, decision rules, every in-journey answer |
| `STORAGE_SETUP.md` | **Start here for setup.** Every step, in order, no coding |
| `fake_door_v2_ARCHIVE.html` · `fake_door_v3_ARCHIVE.html` | Previous builds, kept for comparison. **Do not field them** |

---

## Quick start

```
open fake_door.html                          # random arm, as a participant sees it
open "fake_door.html?variant=discount&qa=1"  # force an arm + facilitator panel
open "fake_door.html?variant=restaurants&qa=1"
open "mobility_entry.html?placement=prominent&qa=1"
python3 analyse_results.py --demo            # pipeline on fabricated data
```

`?variant=` or `?qa=1` marks the session **`is_qa = true`** and the analysis script drops it.
That is how you preview arms without polluting the data.

**URL parameters**

| Parameter | Values | Effect |
|---|---|---|
| `variant` | `discount` · `restaurants` · `everyday` | Forces the proposition arm (QA only) |
| `source` | `rapido` · `instagram` · `whatsapp` · anything | Recorded as the entry channel |
| `qa` | `1` | Shows the facilitator panel |
| `placement` | `control` · `prominent` | Entry-card arm in the mobility mock |

Without a parameter, a participant is assigned by coin flip on first load and **keeps that arm on
every reload and every later visit** (stored in `localStorage`).

---

## The journey

```
HOME            2×2 offer grid · working filter tabs · ETA boxed on each card
  ↓             no question here — the grid is the arm, not a quiz
SEARCH          TWO BOXES, recorded separately:
  ↓               "What do you feel like eating?"  → dish + cuisine type
  ↓               "Or go straight to a place"      → restaurant + local/chain
  ↓             → why that dish? · when do you order it?
  ↓             → why that place? · can you get it on your app today?
  ↓             → not on here? what would you actually do?
MENU            real items, prices, ADD buttons
  ↓             → why that item?
DELIVERY        its own screen · no totals visible · price randomised
  ↓             → why that one? · what would worry you? (Rapido Link only)
CART            offers — food discounts only, never delivery
  ↓             → why that one?
                how you pay — the bill opens under the option you pick
  ↓             → why that one?
PLACE ORDER     ✋ no confirmation. Ever.
  ↓
DEBRIEF         ONE screen, 118 words, your deletion code
  ↓             primary CTA: "Yes — I'll answer a few more questions"
SURVEY          QR they scan with their own phone + the link → Done
```

### The two searches are the point

The study exists to learn what **kind** of food and what **kind** of place Gachibowli reaches for —
not which exact ones. So they are two boxes, on the first screen after home, recorded as two
separate streams:

| Recorded | On what |
|---|---|
| `category` | The dish's cuisine, and the restaurant's category |
| `rest_kind` | **`local` or `chain`** — the case study's central question, read off behaviour |
| `query` | The raw string. A name we don't stock is kept verbatim, because a gap is a finding |
| `tap_kind` | Which box they reached for first — place-first or dish-first thinking |

**Every query is logged, not just the ones you tap through.** `search_query` fires on a 700 ms pause
with the string and its result count — so someone who types *"pulihora"*, finds nothing and settles
for biryani leaves that word behind. A **zero result is a supply gap**, and the zero-result list is
the operational output of the whole study.

**A missing dish and a missing place are different problems**, so they're handled separately:

| | Dish we don't have | Place we don't have |
|---|---|---|
| Action | **Ask for it** · or "show me places that might make it" | **Ask for it** |
| Event | `dish_added_custom` | `restaurant_added_custom` |
| Question | `missing_dish` | `missing_action` |

A dish nobody can find is a **menu** problem — the restaurant is on the platform, the item isn't
listed. A place nobody can find is an **onboarding** problem. Pooling them would hide which one
actually costs an order.

Neither is a dead end: the box clears and you stay on search, free to keep looking.



### Three behaviours, kept apart

The study measures three decisions. On one screen they cancel each other out — take the expensive
fast delivery, kill its cost with a free-delivery coupon, then pick the payment model that zeroes
fees anyway. Three rules stop that:

| Rule | What it prevents |
|---|---|
| Delivery is decided **on its own screen**, before any total is visible | Picking speed because a coupon will cover it |
| **No coupon touches delivery** — every offer discounts food only | Cancelling the delivery decision with the offer decision |
| **All three payment models charge the same delivery fee** | A payment choice rewriting a delivery choice already made |

Verified: delivery is ₹35 under *Itemised*, *Single price* and *Ownly Plus* alike.

**1 · Will they pay for time?** Two options. The fast one's price is **randomised per participant**
(₹15 / ₹25 / ₹35 / ₹49), so take-up across the sample traces a demand curve for the same 17-minute
saving rather than giving one uninterpretable number.

| | ETA | Fee | Trade-off they're told about |
|---|---|---|---|
| Standard | 42 min | free | "Can wait longer at busy times." |
| Rapido Link | 25 min | randomised | "They may drop a passenger first. Live tracking starts once they have your order." |

The trade-off isn't only money — a speed option with no downside isn't a decision.

**2 · How steeply do they discount a reward that isn't today?** Three offers real apps actually run.
None asks you to remember anything or predict your own future.

| Coupon | Structure | On a ₹640 basket |
|---|---|---|
| ₹100 off this order | Cash now, certain | −₹105 now |
| **₹X in Ownly Money** — lands in your balance, **applies itself** next order, valid 30 days | More cash, one order away | +₹X next order |
| 10% off every order for 30 days | Recurring, self-applying | −₹67 now, and again all month |

**₹X is randomised per participant (₹120 / ₹150 / ₹200 / ₹250)** against a fixed ₹100 now. Where
people start choosing it is the discount rate — what one order of delay costs Ownly.

Only 25% of the surveyed 40 said they'd stay once an intro offer ended. If nothing in that range
beats ₹100 today, Ownly has to buy every order outright, forever.

**3 · What will they accept being charged for?** The audit found Ownly charges **nothing** — 0 of 8
captures carried any fee; fee load 5.2% vs an incumbent median of 23.4%. That can't hold.

| Option | Cost | Evidence it rests on |
|---|---|---|
| Pay per order | ₹15/order | ₹15 is Zomato's audited platform fee — ₹14.99 on 14 of 14 captures |
| Ownly Plus | ₹99/month | 82.5% (33/40) already hold Swiggy One and/or Gold — the largest barrier in the study |
| **Order Protection** | **₹9/₹19/₹29/₹39 — randomised** | A refund promise is the **#2 stated reason** people would try Ownly (6 of 23), **3× the first-order discount (2)** |

**Order Protection is what this screen exists for.** It's the second strongest trial trigger in the
whole survey and **nobody has ever been asked to pay for it.** Randomising the price turns take-up
into a willingness-to-pay curve.

The copy answers the documented complaints, not a generic promise — reviews name *"refund initiated…
5 to 7 days"*, *"bots that loop endlessly"*, *"they make you cry if you want to cancel"*. So it reads:
*"Late, cold or wrong — tap once and the full amount is back the same day. No photographs, no chat
bot, no five-day wait."*

`why_bill` separates *"I'd want the cover"* from *"I don't believe the refund would happen"* — the
first means the product is wanted, the second means a trust problem no price fixes.

**Not tested here: bill transparency.** A proper test exists (`bill_s1` — two bills at an *identical*
₹245, simple vs itemised) and was never fielded. It belongs there, at equal totals, not on a list of
paid options where the cheaper one always wins.

**Not tested here: payment method.** COD/meal-card was chosen by 0 of 23 catchment respondents.

### Nothing internal is visible to participants

v6 printed justification under the delivery options — *"Audited: 0 of 8 Ownly captures carried any
fee"*, *"Priced at ₹30 for the 17 min saved — the exact trade the survey asked about"*. That's
research documentation, and it tells participants exactly what's being measured. All of it is gone.

Participant copy names the product and its trade-off, never the evidence behind it. A check renders
every screen and sheet and scans for audit language, competitor names, sample sizes and survey
references — currently zero hits.

## How the questions work

**There is no questionnaire at the end.** Every question is a bottom sheet that appears the instant a
choice is made, on the screen where it happened, naming the thing just chosen — "Why **chicken
biryani**, right now?", "Why **Paradise Biryani** for that?". The gap between the behaviour and the
question is under a second, so what comes back is recall, not reconstruction.

Twelve questions exist; a typical participant sees seven or eight. None fires on the home screen. Each is one tap from four or five
options. Nothing is typed except the two search boxes, where the typed string is itself the finding.

| Fires after | Question | What it gives us that nothing else does |
|---|---|---|
| Applying a coupon | Why that one? | **Which shape of offer wins when it costs something** — biggest now, fee removal, one that lasts, or ₹0 today for a new local place |
| Choosing a dish | Why that, right now? | The project has no food data at all |
| Choosing a place | Why there for it? | "Only place that makes it right" vs "habit" — identical in a survey, different businesses |
| Choosing a place | Can you get it on the app you use today? | The assortment gap at the level of **their own** restaurant, not the catalogue |
| Naming a place we do not have | What would you actually do? | **The most valuable item here.** Whether a missing restaurant costs an order or just costs choice |
| Submitting the list | Which would you miss most? | A forced ranking inside their own set — impossible in a survey |
| Tapping a filter tab | What were you hoping to find? | Price vs speed vs trust, before a single restaurant is seen |
| Adding to the cart | Why that item? | Nothing asked what a person would actually put in a basket |
| Choosing a pricing model | Why that one? | **Q22 asked people to imagine Service P. This asks them to pay it** |
| Choosing a delivery option | Why that one? | Speed was previously a hypothetical at a fixed ₹30; here it is priced against their own bill |
| Choosing Rapido Link | What would worry you? | Whether the one asset no competitor has is actually acceptable |
| Submitting the list | When do you order it? | Catchment hours. Nothing else in the project touches it |

**What this costs.** Interrupting a journey to ask about it changes the journey — someone asked "why
that dish?" now knows the app cares about reasons. That is a real limitation and it is stated in the
design (§13.1) rather than hidden. The alternative, asking at the end, trades a known reactivity cost
for an unknown recall cost.

**What was removed, and why.** The v1 build ended with six questions after the disclosure, including
"what did you think this page was?". All gone. That question was a report card on the ethics, not a
safeguard — the safeguards are the permanent banner, the absence of any order state, and the
disclosure itself. The segment tick-boxes (membership, Rapido use, Ownly awareness) moved to the
facilitator's screening sheet, where they belong.

---

## Will the results be saved?

**Not automatically, as shipped.** `CONFIG.ENDPOINT` is empty, so nothing is sent anywhere. Events
are written to the participant's own browser storage and **only exist on that phone**.

| Situation | Is the data saved? |
|---|---|
| Participant reloads or comes back later | **Yes** — browser storage persists, same arm, events append |
| Facilitator downloads before the tab closes | **Yes** — JSON or CSV on your machine |
| Participant closes the tab before you download | **Lost** |
| Private / incognito browsing | **Lost when the window closes** |
| Participant clears site data | **Lost** |
| You set `CONFIG.ENDPOINT` to an Apps Script URL | **Yes — saved centrally, automatically, per event** |

**The prototype now tells you when storage is unavailable.** It probes `localStorage` at startup with
a real write-read-delete test. If that fails, a red facilitator alert appears at the top of the
screen, `storage_ok: false` is recorded on the first event, and the QA panel shows
`storage=BLOCKED · endpoint=OFF`. Events continue to accumulate **in memory** so the download still
works — but only until that tab closes.

This matters because the earlier build failed silently: with storage blocked it ran perfectly, looked
fine, and recorded nothing. You would only have discovered it at analysis time.

**Recommendation.** For anything beyond a handful of supervised sessions, set up Option 2. Manual
download per participant is a single point of failure, and the failure is invisible until too late.

### Option 1 · No backend (recommended for n = 40)

Events are written to `localStorage` as structured JSON. Nothing leaves the device.

1. Run the session on the participant's phone.
2. Before they leave, append `&qa=1` to the URL and press **Download JSON** (or CSV).
3. Save as `p01.json`, `p02.json`, … one file per participant.
4. Combine: `python3 analyse_results.py p*.csv`

**Combining logs.** Every event carries `anon_visitor_id`, so concatenating the CSVs is safe — the
analysis script deduplicates by participant. If a participant reloads, their events append to the
same log; no double-counting occurs. A participant who clears their browser is a new ID — this is
why the one-per-person **recruitment code** in §5.6 of the design exists.

Trade-off, stated: if the participant closes the tab before you download, that session is lost.
For n = 40 with a facilitator present this is acceptable and keeps the privacy surface at zero.

### Option 2 · Google Sheets (recommended for 200+ or unattended)

1. Create a Sheet with two tabs named exactly **`events`** and **`contacts`**.
2. Extensions → Apps Script → paste `apps_script_collector.gs` → Save.
3. Run `setupSheets()` once from the editor to write the headers.
4. Deploy → New deployment → **Web app**, Execute as **Me**, Access **Anyone**. Copy the `/exec` URL.
5. Open that URL in a browser — it should print `collector alive: …`.
6. Paste it into `CONFIG.ENDPOINT` in both HTML files.

**Recommended `events` columns**

```
received_at · event_id · experiment_id · page_version · variant_id · variant_key · source
anon_visitor_id · anon_session_id · event_name · ts_iso · time_since_load_ms
time_since_prev_ms · device_type · viewport_w · is_qa · is_bot_suspect · payload_json
```

**Why no credential appears in the HTML.** The `/exec` URL is write-only: it appends a row and
returns `ok`. It cannot read the sheet, cannot list rows, and carries no API key. The sheet stays
private to your Google account. There is nothing in the published HTML that can be used to read data.

**Privacy precautions built in**

- Apps Script never exposes the sender's IP, so no IP is stored.
- Only whitelisted payload keys are written; everything else is discarded server-side.
- Free text is scrubbed of anything resembling an email or phone **twice** — once in the browser,
  once in the collector.
- **Contact details never reach the events tab.** `followup_consent_given` logs only the *channel*
  (email/phone). The contact string itself stays in the participant's own browser and is collected
  by the facilitator under the consent flow, so the behavioural dataset can be shared and analysed
  without ever touching personal data.
- Timestamps are ISO-8601 UTC, written server-side (`received_at`) as well as client-side (`ts_iso`),
  so clock-skew on a participant's phone cannot corrupt ordering.
- Participant IDs are random UUIDs generated with `crypto.getRandomValues`. They contain nothing
  derived from the device or the person.

**Duplicate handling.** `anon_visitor_id` is stable per browser. The analysis script collapses all
events for one ID into a single participant record. Same-person-different-device is caught by the
recruitment code, not by the software — flag it, do not silently drop it.

---

## Running a session

1. Screen against the inclusion/exclusion criteria (design §5.5). Record the recruitment code.
2. Hand them their own phone with the link. **Do not watch the screen** — observation changes behaviour.
3. Say only: *"Have a look at this and do whatever you'd normally do. There's no right answer."*
4. Let them reach the disclosure themselves. Do not explain it in advance.
5. Let the question sheets appear on their own. **Do not explain them** — if a participant asks
   what they are for, say "just tap whatever's closest" and debrief properly afterwards.
6. Debrief verbally at the end and answer questions.
7. Download the log with `&qa=1`.
8. For the 8–12 interview subset, run the follow-up immediately while it is fresh.

**Do not** tell participants there are other versions until the debrief.

---

## What this study can and cannot say

Full matrix in design §14. The short version:

**Can:** which dishes people want and which places they want them from *in this sample*; what they
would put in a basket and at what price; **which of three pricing models they choose for their own
basket**; whether anyone wants a Rapido-linked delivery when it is the dearest option on screen; how
often the place they want is not on the app they use today; what they say they would do when it is
missing; whether a food entry gets noticed inside a mobility context (a **lower bound**).

**Cannot:** that anyone will place a real order — **no money moved and none was ever requested**;
that anyone will order twice; that Ownly will be profitable; that Hyderabad-wide demand exists; that
delivery is reliable; that restaurants will join. `place_order_click` is the strongest signal here
and it is still not a conversion. Do not write it up as one.

**At n = 40 the between-arms comparison detects roughly a 43-percentage-point difference.** Anything
smaller will not reach significance, and a 43-point difference is implausible — so that comparison is
**directional only**, and it is not what this study is for.

**The discovery outputs do not have this problem.** A ranked list of demanded dishes and restaurants,
a list of names we do not stock, and the distribution of in-journey answers are valid at any sample
size, because they are lists and distributions rather than comparisons. They are the primary output
(design §9); the framing contrast is secondary.

---

## Ethics summary

No payment collected · no card or UPI field anywhere · no fake order confirmation · no restaurant ever
shown as available · disclosure fires within one screen of the intent action · nothing captured before
the disclosure · contact only on explicit opt-in with a fulfillable purpose · visible research-prototype
marker on every screen · original visual system, no official logos or screenshots · withdrawal route
and anonymous code given on the final screen.

**There is no ethics question in the instrument any more,** and that is deliberate: a question about
whether the prototype misled someone is a report card, not a protection. The protections are the
sticky research banner on every screen, the fact that no order state exists to reach, no restaurant is
ever shown as available, and a disclosure that fires within one screen of the intent action.

The facilitator debriefs verbally at the end and records any participant who says they thought it was
a live app. Report that count in the write-up.

---

## Accessibility

Semantic landmarks and headings · every input labelled · visible 3px focus ring · minimum 44×44px
touch targets · `aria-live` announcements on screen change · focus moves to the new heading on each
step · respects `prefers-reduced-motion` · text contrast meets WCAG AA · works keyboard-only ·
16px inputs to prevent iOS zoom-on-focus.

---

*Design v11.0 · 2026-09-23 · grounded in `CASE_STUDY_Ownly_Hyderabad.md`. Every statistic in the
design document carries an evidence label: `[GACH]` our Gachibowli sample, `[BLR]` our Bengaluru
sample, `[PUBLIC]` public reviews and social, `[CLAIM]` company or media claim, `[ASSUMPTION]`
not yet validated.*
