# Fake door — map of the LIVE build (fakedoorownly.netlify.app)

**Method:** static analysis of the deployed build — HTML shells, 8 JS chunks and the CSS were fetched
and read. One read-only `GET /api/admin/sessions`. **No POST was sent; no test event was written.**

## 0. The live app is not any file in this repo

It is a **Next.js / React app on Netlify** that impersonates Rapido (`<title>Rapido</title>`). It is a
*re-implementation* of `SUBMIT_EXPERIMENT/fake_door.html`, not a copy: same arms, same price ladders,
same 12 questions, same screens — different tech and a different backend.

| Route | What it is |
|---|---|
| `/login` | Role chooser: **Start Rapido** · **Start Ownly (direct)** · Admin |
| `/app` | A working fake **Rapido ride app** (destination → vehicle → captain → ride → complete) |
| `/ownly` | **The fake door** (food ordering) |
| `/admin` | Live analytics, polls every 3s |
| `/api/sessions`, `/api/events`, `/api/mark-explored` | POST-only writes |
| `/api/admin/sessions` | GET, **no authentication** |

## 1. Two entry paths

| | Direct | From Rapido |
|---|---|---|
| Route | `/ownly?source=direct` | 7 ride screens, then `/ownly?from=<touchpoint>&session=<id>` |
| Header inside Ownly | `Direct Ownly · @direct` | `From Rapido · @username` |
| Touchpoints | — | `top_banner` 7 · `bottom_nav` 17 · `ride_complete_ad` 18 (+ 4 legacy slots since removed) |
| Guard | `/app` bounces direct users out | `/ownly` bounces provenance-less visitors back to `/app` — the door cannot be reached by typing the URL |
| Live visits | 45 | 52 |

## 2. The Ownly flow, screen by screen

1. **Home** — location, fake search bar, filter chips (ALL/OFFERS/FAST/RATED 4+), **the A/B tile block**, category chips, 14 real Gachibowli restaurants. Fires `experiment_view`, `landing_page_view`.
2. **Search** — "What do you feel like eating?" + "Or go straight to a place". Every keystroke from 2 chars logs `search_query`. **A typed miss is a designed trap:** "We don't have *shawarma*. Tell us what you would do." → `dish_added_custom` + the `missing_dish` question.
3. **Places list** — restaurants for that dish.
4. **Menu** — real dish names, invented prices with struck-through "was" prices. ADD → `item_added` + `why_item`.
5. **Delivery** — Standard 42 min free **vs Rapido Link 25 min +₹X** (randomised). Choosing Rapido Link also asks the trust question.
6. **Cart** — live bill, three offers (₹100 now / ₹X wallet / 10% for 30 days) and three pay models (₹15 per order / ₹99 a month / ₹15 + ₹X cover), each showing its own recomputed total. CTA **Place Order**.
7. **Honest stop** — ✋ "We can't place this order. Nothing was charged. No restaurant was contacted."
8. **End** — back to Rapido, or log out.

**The 12 micro-questions** fire *at the moment of the choice*, as a bottom sheet, before the next screen paints: `why_filter, why_dish, meal_slot, missing_dish, why_rest, app_gap, missing_action, why_item, why_delivery, rapido_link_trust, why_offer, why_bill`. Each is 4–6 tappable options plus Skip — **they are not free text**, and the spreadsheet stores the human-readable label.

## 3. The four randomisations (drawn on `/ownly` mount, stored in localStorage)

| What | Levels | Measures |
|---|---|---|
| Message arm `fd_variant` | `discount` \| `restaurants` | Money-off framing vs supply framing |
| Rapido Link fee `fd_rlprice` | ₹15 / ₹25 / ₹35 / ₹49 | WTP for 17 minutes |
| Wallet `fd_wallet` | ₹120 / ₹150 / ₹200 / ₹250 | Deferred vs ₹100 now — the implied discount rate |
| Cover `fd_protect` | ₹9 / ₹19 / ₹29 / ₹39 | WTP for reliability |

## 4. The data model

- `POST /api/sessions` creates the row; `POST /api/events` once per interaction; `POST /api/mark-explored` at the handoff.
- Events are **double-encoded**: every field appears flattened *and* inside `payload`.
- The server folds events into one **`ownly_visits` row per session** — that row is exactly the 30 columns in `07_fake_door/ownly_direct.xlsx` and `ownly_rapido.xlsx` (45 + 51 = 96 rows; the live table now holds 97).
- Key columns: `source`, `variant`, `dish`, `restaurant_name`, `delivery_id`, `bill_id`, `offer_id`, `filter`, `rl_price`, `wallet_amt`, `protect_price`, `item_count`, `bill_total`, **`placed_order`**, plus the 12 "why" answer columns.
- **Only free text in the whole study:** the Rapido destination query, the Ownly dish/restaurant query, and a typed miss (which is how *Momos* and *Shawarma* got into the dish column).

## 5. Live totals (read-only, as of this session)

194 sessions · 97 Ownly visits · 3,166 events · **48 `place_order_click` events, 42 sessions flagged `placed_order`**.
Funnel: 106 restaurant-card clicks → 60 menu views → 44 delivery screens → 40 carts → 42 placed.

## 6. What it can and cannot prove

**Can:** a behavioural conversion at a fully priced bill (42 of 97 ≈ 43%); relative preference among options shown side by side (`per_order` 35 / `membership` 11 / `protected` 10; standard 35 / rapido_link 26; flat100 20 / wallet 15 / recur10 10); directional WTP curves; reasons captured at the moment of the act; where attention dies; which touchpoint pulls people out of a ride app.

**Cannot:** anything about the message A/B — the split is **71 discount : 26 restaurants** against a 50/50 design because `fd_variant` survives logout on a shared phone, so the arm is confounded with the device. Also cannot prove real demand (nobody paid, nobody was hungry), a real Rapido partnership (the ride app is a mock), absolute price points, population estimates, or retention (the live build dropped the visitor id).

## 7. Defects found in the live build — fix before presenting

1. **`GET /api/admin/sessions` is world-readable.** Anyone with the URL can download all 194 sessions, including every typed search term and self-chosen username.
2. **Admin credentials are hardcoded in a public JS chunk** (`admin@gmail.com` / `Admin@123`), and the admin gate is only a localStorage check.
3. **The participant code is the same for everyone.** It is `sessionId.slice(0,8)` and every id starts `sess_<13-digit ms>`, so every participant is shown `SESS_179` — sessions cannot be reconciled with any survey response.
4. **Randomisation is sticky across logout.** Clear `fd_variant` / `fd_rlprice` / `fd_wallet` / `fd_protect` on logout, or key them to the session id.
5. **The survey screen was removed** from this build, yet `followup_consent_given {contact_channel:'survey'}` is still logged.

## 8. Frame list for the ~20-second auto-playing walkthrough (12 frames, ~1.7s each)

1. Yellow login, "rapido / Ownly Research Prototype", three buttons — *every participant picks one of two doors*
2. Rapido home, pink banner sliding in: "Food delivery is here! Zero fees · 2,847 orders in Gachibowli"
3. Destination list, tapping "Inorbit Mall · HITEC City · 5.8 km" — *every keystroke is recorded*
4. Vehicle cards, Bike selected, "Book Bike · ₹71"
5. "Finding your captain…" → captain card ⭐4.7 TS 09 4821
6. Green progress bar sweeping to 100%, "Ride in progress…"
7. "Ride Complete!" + the pink card "Perfect timing! … zero fees" → **the door**
8. Ownly home, amber strip "Research prototype · not a live order", the four A/B tiles
9. Menu open, bottom sheet: "QUICK ONE — Why add Chicken Dum Biryani?"
10. Delivery: Standard 42 min free vs **Rapido Link 25 min +₹35** — *the price is randomised*
11. Cart: bill, three pay models, "Place Order · ₹310"
12. The stop: ✋ "We can't place this order. Nothing was charged."
