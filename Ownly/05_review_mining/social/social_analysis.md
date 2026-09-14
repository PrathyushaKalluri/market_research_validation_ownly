# Ownly — Social & Community Voice Analysis (Reddit, LinkedIn, X, forums)

**Agent B2 · collected and first-pass coded 2026-09-14 · status: AI first pass, NOT human-verified**
Data in this folder: `social_raw.csv` (524 items), `social_coded.csv`, `search_log.csv`, `codebook_social.md`. Every claim below cites `item_id`s that can be traced to a URL in `social_raw.csv`.

> **Mandatory caveat — read before using any number here.** This is **self-selected public content**. People post when something went very wrong, very right, or went viral. Counts describe *this corpus only*. They are not rates, shares, or estimates for Ownly users, Bengaluru, or Hyderabad. Use this material to generate and sharpen hypotheses, write survey and interview probes, design the competitor audit, and surface contradictions — **never to size a problem or declare a hypothesis validated.** Negative experiences are almost certainly over-represented.

---

## 0. What was collected and how

| Source | Access route | Items | Relevant after exclusions | Notes |
|---|---|---|---|---|
| Reddit | Public RSS feeds (search + per-thread), no login, 12 s spacing with back-off | 471 (34 threads: 34 posts + 437 comments) | 367 | 104 excluded (`relevant = 0`): banter, bots, memes, off-topic side debates, verbatim cross-posts |
| LinkedIn | Individual public post URLs found by web search, viewed logged-out (~22 fetches) | 45 (19 posts, 1 article, 25 visible comments) | 45 | Only comments shown logged-out; some texts are fetch-tool summaries (`verbatim_status`) |
| X / Twitter | Search-engine snippets only (site is login-walled) | 7 | 7 | Snippet text, often truncated |
| Public forums | StartupTalky community (consumercomplaints.in: 0 Ownly items) | 1 | 1 | Ownly staff Hyderabad launch post |
| **Total** | | **524** | **420** | |

- **Reddit communities:** r/Zomato 151 items, r/BangaloreSocial 138, r/swiggy 115, r/indiranagar 29, r/electronic_city 10, r/Ownly 8 (an *unofficial* sub created by a cloud-kitchen co-owner, RD-1sko63h), others ≤ 5.
- **Dates:** April 2025 – 12 September 2026. **55 of 108 de-duplicated first-hand incidents are from August 2026**, when several comparison threads went viral. This reflects posting and search-feed recency, **not a trend in service quality**.
- **De-duplication:** 15 items tagged `[SAME_INCIDENT:…]`; 9 verbatim or same-incident cross-posts excluded. One user posted the same failed order in three threads (RD-1qcrc1f-o6kcml5, confirmed by RD-1nclzlx-o6kcxtm). Same-author links are inferred from content, since RSS has no author field.
- **Not possible / not done:** Reddit JSON API (HTTP 403) and old-Reddit search (login redirect) were not worked around. Reddit's robots.txt could not be read from the script (block page) — logged as a limitation. Facebook, Instagram, YouTube comments and Quora were inaccessible or had no results. The main pass stopped after 32 threads (all Ownly-titled candidates); ~38 broader 2025 "Rapido enters food delivery" speculation threads were not fetched. A follow-up pass requested by the lead added 2 threads (RD-1w9qa1f, RD-1w0k0bk). It ran 8 queries: `toing ownly`, `ownly delivery fee`, `ownly free delivery`, `ownly gachibowli`, `ownly kondapur`, r/hyderabad `toing`, r/hyderabad `zero commission food delivery`, r/BangaloreSocial `toing`. **The Gachibowli and Kondapur queries returned nothing relevant.** RSS returns ≤ 100 entries per thread, so the two largest threads (RD-1vu5s4x 93, RD-1k2w5wi 96) may be truncated.
- **Privacy:** no usernames or profile links stored. Rider phone numbers and names of private individuals in complaint text are redacted automatically in the build script.

---

## 1. Headline findings (each is a HYPOTHESIS-generating observation, not a validated finding)

| # | Observation from this corpus | Evidence (item_ids) | Strength |
|---|---|---|---|
| F1 | **The loudest first-hand theme is service failure and recovery, not price.** Of 108 de-duplicated first-hand incidents, **46 describe a fulfilment failure** (38 at severity ≥ 3) and **29 a support/refund failure** (27 at severity ≥ 3). Price wins: 19. Price non-wins: 18. | §2.2–2.3 | Directional only; negative self-selection |
| F2 | **The price advantage is real for some baskets but not consistent.** All 6 user-posted bill comparisons show Ownly cheaper, some by a lot. But 18 first-hand incidents report no win: incumbent cheaper after coupons/card offers, identical listings, Ownly listing pricier, or menu prices inflated versus in-store. | §2.4 | Mixed, contradictory |
| F3 | **Whether the saving is worth lower reliability is openly contested, in users' own words.** "Accept wait/hassle/hiccups for savings": 4 statements. "Reliability over price" / "would pay more for reliability": 6 statements, one quantified at ₹20–30 per order. | §2.5 | Very small n; valuable for question design |
| F4 | **Durability distrust is the dominant narrative reaction.** 37 items expect fees or prices to rise once Ownly has market share; 28 question sustainability. Users frame use as "enjoy while it lasts". Two users say Swiggy Toing started fee-free and later added fees. | §2.7, §3.4 | Consistent across LinkedIn and Reddit |
| F5 | **Users disagree on what Ownly's delivery fee is.** Described as free (3 items), "+5 rupees" (1), ₹15 on one order (1), and GST + platform fee ≈ ₹40 (2, platform ambiguous). Media and company sources say ₹30 flat. | §2.6 | Contradictory — needs the live audit |
| F6 | **The Rapido brand cuts both ways.** Negative: "Rapido DNA", the Rapido pricing playbook, ride complaints posted on the Ownly launch post, and a "Swiggy's child" association. Positive: "rapido seems to do ok without excessive charges", plus fleet/super-app framing (mostly from commentators). | §2.8, §3.5 | Two-sided; H7 must test both directions |
| F7 | **Specific operational risk patterns repeat** (each from few users; hypotheses only): late-night false "delivered" (a thread with ≥ 12 "same happened" replies); large (₹1k–2k) orders more exposed; small carts (< ₹150) cancelled by restaurants; riders batching 4–5 orders; riders shared with Swiggy; no cash-on-delivery; **no meal-card (Pluxee) payment**. | §2.9 | Hypotheses for survey/audit |
| F8 | **There is no public consumer voice about Ownly in Hyderabad yet** — searches for Gachibowli and Kondapur also returned nothing. Found only: "Not available in Hyderabad!" (2026-08-21), "Can't wait for it to come to Hyderabad. Tired of zomato monopoly" (2026-08-24), and an Ownly staff "officially LIVE in Hyderabad" post (≈ 2026-09-11). **INTERPRETATION:** launch most likely between 24 Aug and ~11 Sep 2026 — inferred, not confirmed. | §5 | Very weak, but dated |
| F9 | **Incumbents show pain and strength in the same corpus.** Pain: fee stacks and opacity, "3–5x" delivered prices, 7 DIY workarounds (call the restaurant + Rapido parcel/Porter), bad incumbent support incl. one Swiggy churner. Strength: in **3 direct comparisons, users say Swiggy/Zomato recovered failed orders better**. | §2.8 | Directional |

---

## 2. Reddit and cross-source consumer evidence

### 2.1 Composition of first-hand evidence
| Measure (all sources, de-duplicated) | Count |
|---|---|
| First-hand Ownly usage items | 123 (108 unique incidents/authors) — Reddit 102, LinkedIn 5, X 1 |
| Sentiment of the 108 | negative 64 · positive 19 · mixed 16 · neutral 9 |
| Stated switching reason (all relevant items, de-dup) | **away from Ownly 18** · **to Ownly 14** (incl. 2 conditional, 1 planned) |
| Explicit "moved completely to Ownly" | 4 (RD-1vn73gn, RD-1vq18l9-p4cbzrc, RD-1vu5s4x, RD-1vw5429-p5e3vp2) |
| Explicit churn ("deleted/never again") | 3 (plus 2 urging others to delete) |
| Evidence of repeat use | 18 |
| Severity of the 108 | 4 = 15 · 3 = 29 · 2 = 20 · 1 = 4 · none (praise/neutral) = 40 |

### 2.2 Theme frequency × severity — first-hand, de-duplicated incidents (n = 108)
Severity: 1 cosmetic · 2 inconvenience · 3 failed order or money at risk · 4 safety/hygiene, fraud-like conduct, or money lost after contacting support.

| Theme | Incidents | With severity | ≥ 3 | = 4 | Mean severity |
|---|---|---|---|---|---|
| NON_DELIVERY (incl. marked delivered, not received) | 20 | 20 | 16 | 6 | 3.10 |
| SUPPORT_UNRESPONSIVE | 19 | 19 | 17 | 6 | 3.21 |
| PRICE_SAVINGS_OBSERVED | 18 | 4 | 1 | 0 | 2.00 |
| RIDER_CONDUCT | 12 | 12 | 12 | 6 | 3.50 |
| LATE_DELIVERY | 9 | 9 | 6 | 0 | 2.67 |
| TRUST_LOSS_SCAM_FRAMING | 9 | 9 | 8 | 5 | 3.44 |
| PLATFORM_RESTAURANT_CANCELLATION | 7 | 7 | 7 | 3 | 3.43 |
| MISSING_WRONG_ITEMS | 6 | 6 | 6 | 4 | 3.67 |
| REFUND_ISSUE | 6 | 6 | 6 | 5 | 3.83 |
| MENU_PRICE_INFLATION_ON_OWNLY | 6 | 2 | 0 | 0 | 2.00 |
| ASSORTMENT_LIMITED | 6 | 3 | 2 | 0 | 2.33 |
| USER_BILL_COMPARISON | 6 | — | — | — | — |
| SUPPORT_RECOVERY_POSITIVE | 6 | 4 | 0 | 0 | 2.00 |
| INCUMBENT_CHEAPER_AFTER_OFFERS | 5 | 2 | 1 | 0 | 2.50 |
| RELIABLE_EXPERIENCE_POSITIVE | 5 | 1 | 0 | 0 | 1.00 |
| SUPPORT_SLOW | 4 | 4 | 4 | 0 | 3.00 |
| APP_UX_SLOW_GLITCHY | 4 | 4 | 2 | 0 | 2.50 |
| FULL_SWITCH_TO_OWNLY | 4 | — | — | — | — |
| LATE_NIGHT_RELIABILITY_RISK · LARGE_ORDER_TRUST_RISK · OWNLY_PRICIER_OBSERVED · PRICE_PARITY_OBSERVED · NO_CASH_ON_DELIVERY · SERVICE_AREA_LIMITED · RIDER_MULTI_APP_OBSERVED | 3 each | | | | |

### 2.3 Rolled-up families (same 108 incidents; one incident can sit in several families)
| Family | Incidents | Severity ≥ 3 | Severity 4 |
|---|---|---|---|
| Fulfilment failure (non-delivery, late, rider conduct, cancellation, wrong/missing, stale, payment deducted) | **46** | 38 | 13 |
| Support / refund failure | **29** | 27 | 10 |
| Price win (savings, no hidden fees, simple pricing) | 19 | 1 | 0 |
| Price non-win (incumbent cheaper after offers, parity, pricier listing, inflated MRP, fees observed, price creep) | 18 | 1 | 0 |
| App / payment friction (UX, forced rating, no COD, no meal card) | 13 | 4 | 0 |
| Assortment / coverage | 8 | 2 | 0 |
| Support recovered well | 7 | 1 | 0 |
| Reliable experience praised | 7 | 0 | 0 |

**Order stage of first-hand incidents:** pricing/checkout 32 · delivery hand-off 18 · post-order support/refund 17 · dispatch/ETA 13 · app/account 5 · payment 5 · browse/menu 4 · food quality 3 · discovery 1 · general 10.
**INTERPRETATION:** price is discussed *before* the order; the severe harm happens *after* dispatch. That is where a low-price proposition is most exposed.

### 2.4 Price evidence — both directions
**User-posted comparisons (all CONSUMER-GENERATED, unverified, screenshots not retrievable via RSS):**
| Item | Date | What the user reports |
|---|---|---|
| X-01 | 2026-03-04 | Corn pizza: Ownly ≈ ₹124.95 vs Swiggy ≈ ₹180 (after ₹50 discount + charges) vs Zomato ₹191.37 — as reported by Oneindia |
| RD-1vn73gn | 2026-08-13 | Same restaurant/food: Swiggy ₹367; dish price alone ₹100 higher on Swiggy; "switching to Ownly and delete Swiggy" |
| RD-1vp2t3m / -p3z47ie | 2026-08-15/16 | ~₹300 on Ownly (incl. a first-order extra discount) vs ~₹450 on Zomato/Swiggy |
| RD-1vq18l9 | 2026-08-16 | "Same place, same items, but ₹392 on Zomato vs ₹220 on Ownly." |
| RD-1vu5s4x | 2026-08-21 | "Even with the Swiggy Card discount + Swiggy One it still is off by ~120-150 rupees." |
| RD-1vpxbyr | 2026-08-16 | Direction disputed in the replies (item-size mismatch) — ambiguous |

**Counter-evidence (price advantage absent or reversed):**
- **Incumbent cheaper once offers apply (7 items):** LI-19 (card and platform offers), RD-1nclzlx-ntzggfd ("Swiggy and Zomato offer discounts to reduce the prices. Ownly doesn't."), RD-1vpxbyr-p41atep (2 weeks of daily comparisons: pre-coupon Zomato never cheaper, but coupons made totals "equal to or 15-20rs less than Ownly"), RD-1vkoo9i-p308quz, RD-1vq18l9-p420vqm (₹120 off on Zomato), RD-1vu5s4x-p4zlg8f (₹0.41 difference), RD-1vq18l9-p4d4532 (Toing vs Swiggy).
- **Parity (4):** "In our area, already most shops have same price between Swiggy and Ownly" (RD-1vu5s4x-p52p0z4); savings limited to absent fees (RD-1w8qx26-p87mci1).
- **Menu price above in-store (7 items):** 2 idlis ₹40 in store vs ₹68 on Ownly, and the poster would accept ₹50–55 (RD-1vs9ut4, with three "noticed the same" replies). An alleged strike-through MRP on a biryani chain (RD-1szs0vx) is disputed in replies.
- **Specific listings pricier on Ownly (3):** RD-1vpxbyr-p40z0hq, RD-1vpxbyr-p41g7mi, RD-1vkoo9i-p30cdmr.
- **Perceived price creep after repeat orders (1):** RD-1vu5s4x-p5gszsr.

**Mechanism clues (INTERPRETATION):** restaurants, not Ownly, set menu prices. One cloud-kitchen owner says "We have kept our prices there much much lower than Swiggy/ Zomato" (RD-1vo68qd-p3nf2wm — seller claim). Others say restaurants list the same prices everywhere, so "No point of flat fee if restaurants prices are same" (RD-1nclzlx-nzb4quo). **The Ownly saving is therefore restaurant-dependent**, and incumbents' coupons can erase it.
**Segmentation clue:** "For small orders ownly For large orders with credit card offers Swiggy" (RD-1vq18l9-p471knv).

### 2.5 Price vs reliability / time — stated trade-offs (H3, H4)
| Stance | Items | Short verbatim quote |
|---|---|---|
| Accepts longer wait for saving | RD-1vp2t3m-p3z47ie | "I don't mind waiting an extra 10-15mins to save 150es" |
| Accepts hassle for saving | RD-1qcrc1f-owap5ff | "There can be little hassle sometimes, but I'll discount that for the money I am saving" |
| Tolerate a challenger's early problems | RD-1w8qx26-p85x98w, -p87jkgc | argues users should accept "a few initial hiccups" (paraphrase + fragment) |
| **Reliability over price** | RD-1vw5429; RD-1w8qx26; RD-1w8qx26-p85079n | "They can't compete on reliability with swiggy and zomato. The lower price is not worth it" |
| **Would pay more for reliability/resolution** | RD-1vp2t3m-p3zl4ah; RD-1vs9ut4-p75exe7; RD-1w8qx26-p85z4gw | "Swiggy has charged me say 20-30rs extra every order but provided proper customer service and delivered properly" |
| Mechanism for slower delivery | RD-1vu5s4x-p55u3l2 | "They pick 4-5 orders at once and deliver your order after roaming over the city" |

**INTERPRETATION:** both sides exist and the counts are too small to say which is more common. For the choice experiment, this means reliability and refund assurance must be real attributes alongside price and ETA. A price-only test would miss what a large share of these posts are about.

### 2.6 What users say the delivery fee is (H8) — inconsistent
| Claim | Item | Date |
|---|---|---|
| ₹40 order → ₹45 final "after delivery" (pilot) | RD-1qcrc1f-nzkh0ra | 2026-01-14 |
| "minimal fees like +5 rupees" | RD-1u4t85s-orqjidr | 2026-06-15 |
| "how are they providing free delivery" | RD-1vq18l9-p46udk0 | 2026-08-17 |
| "95 + 15(delivery) = 110 total" | RD-1vs9ut4-p4kl9av | 2026-08-19 |
| "no platform fee/ packing charge/ delivery fee" | RD-1vs9ut4-p5et377 | 2026-08-23 |
| "Not worth the no delivery prices and no platform fee" | RD-1w8qx26 | 2026-09-06 |
| "charged me gst and platform fee...abt 40 rs extra" (platform ambiguous) | RD-1vkoo9i-p2yvz60 | 2026-08-11 |
| Company/media: ₹30 flat (LI-08); earlier tiers ₹10–₹50 (LI-04, LI-13, X-02) | — | 2025–2026 |

**Stated preferences:** 9 items prefer an **explicit, labelled fee** over "free delivery" paired with hidden menu inflation — e.g. "I'd much rather see a flat platform fee that is clearly labelled" (RD-1vkoo9i-p36kc9g). Two suggest a subscription would be acceptable (one names ₹200/month, RD-1vu5s4x-p66sylu). Users report **no Ownly subscription** as of Aug 2026 (RD-1vu5s4x-p4zgv23). Deep promotions also exist — a "FIFA offer" order for ₹60 (RD-1v0w2lx, 2026-07-19) — so "everyday pricing" and promotions coexist. A referral post (RD-1w9qa1f, 2026-09-07; the poster benefits from referrals, so this is not an organic review) repeats the current acquisition offer: "upto ₹100 off on your first order" and "No surge fee. No platform fee. No packaging charges."

### 2.7 Durability, loyalty and competition
- `FUTURE_FEE_CREEP_EXPECTED` 37 items; `SUSTAINABILITY_SKEPTICISM` 28; `HISTORICAL_PRICE_CONVERGENCE` 9 (nostalgia for early Zomato/Swiggy/Uber Eats discounts that later disappeared). Two of these recall living on discounted delivery as interns or students.
- "Use it while it lasts": 4 (`SWITCH_DESPITE_TEMPORARY_PRICING`). "Just keep switching" / no loyalty: 5.
- **Swiggy Toing** mentioned in 23 items: seen as the like-for-like competitor with a similar UI and prices. Two users report Toing **added delivery fees after launching fee-free** (RD-1vkoo9i-p2vhimd, RD-1vu5s4x-p5348vu). One user says Toing is "the only legit one" on price (RD-1vkoo9i-p30cdmr). Also named: Swish, Directoo, ONDC/Digihaat, Flipkart.
- `ASTROTURF_SUSPICION` in 8 items, accusing posters of being paid by Ownly **and** by Zomato/Swiggy. Community trust in comparisons is itself low.

### 2.8 Brand and incumbent contrast (H7)
- **Negative Rapido transfer:** "Don't expect any help from any of the rapido's ventures" (RD-1w8qx26-p84qr61). The Rapido playbook is expected to follow: raise prices slowly, tipping, pay more to get a partner assigned (RD-1vkoo9i-p37z1cu). Three ride-related complaints appear on the Ownly launch post (LI-09-C1, -C4, -C5). "Swiggy's child" association (RD-1vkoo9i-p3aaig4).
- **Positive:** "rapido seems to do ok without excessive charges still" (RD-1vu5s4x-p599njy). Fleet/super-app framing in 9 items, mostly from commentators.
- **Awareness is uneven:** "What platform is this?" (RD-1vkoo9i-p3l6wvy); "Is this the one by Rapido?" (RD-1vw5429-p5e3mm2); "no one seems to know about them" (RD-1qcrc1f-ocrvht0).
- **Incumbents recover better** in 3 direct comparisons — e.g. Swiggy "immediately took the rider on conference call" (LI-19-C2). **But incumbents fail too:** Zomato support "horrendous" (RD-1vq18l9-p46crht); a user stopped using Swiggy after an unresolved missing-item complaint (RD-1vu5s4x-p6a3nog).

### 2.9 Operational patterns worth testing (few users each — hypotheses only)
| Pattern | Items | Why it matters for Gachibowli |
|---|---|---|
| Late-night false "delivered" | RD-1tmgwrf (≥ 12 "same happened" replies, alleged repeat-offender rider), RD-1vspuva-p4ooll8 ("it happens only when you order late at night"), RD-1tmgwrf-p4p288t (1:24 am) | Students and shift-working professionals order late — survey should capture time of day |
| Large orders riskier | RD-1vpxbyr-p4n9d1n ("if ur ordering for more items don't trust ownly"), RD-1w8qx26 (₹2k), RD-1w8qx26-p854g39 (fine under ₹1,000) | Group or hostel orders |
| Small carts cancelled by restaurants | RD-1rme2x8-o92gcb5, -oo7yi8v ("small orders (under rs 150)") | Conflicts with low-AOV value story |
| Rider batching / shared riders | RD-1vu5s4x-p55u3l2; RD-1vp2t3m-p3z5k7n (Ownly helmet, Swiggy bag); RD-1qcrc1f-ocrvht0 | Rider supply is not exclusive — Hyderabad peak capacity is a question |
| Listings not accepting orders | RD-1rme2x8-o925ag6; RD-1nclyuy-odj5wgc | First-order failure drives deletion (RD-1rme2x8, RD-1w8qx26-p850abw, RD-1vspuva-p4rcb95) |
| No cash on delivery | RD-1qcrc1f-oo7vwmt, RD-1nclyuy-oganv2f, RD-1w8qx26-p8b3uuc; COD suggested as a trust safeguard (RD-1tmgwrf-onmte5s) | Trust for first-time users |
| **No meal-card (Pluxee) payment** | RD-1vp2t3m-p3z0kqj; RD-1vu5s4x-p4zqore ("implement pluxee card payment then I would ordee food from them") | **Directly relevant to salaried professionals in Gachibowli** |
| Rider earnings doubts | RD-1nk2ror-nf7kcb2, RD-1vs9ut4-p4qrquq | Supply sustainability |

---

## 3. LinkedIn — narrative and claims landscape (n = 45)

**Read as a map of what is being *said*, not a measure of experience.** Only logged-out-visible comments were captured.

### 3.1 Composition
| Measure | Count |
|---|---|
| Business/launch commentary | 39 of 45 |
| First-hand Ownly order accounts | 5 (LI-09-C2, LI-09-C8, LI-10, LI-19, LI-19-C2) + 1 ambiguous (LI-09-C3, probably a Rapido parcel) |
| Timing | Pre-launch/pilot wave Jun–Nov 2025; citywide-launch wave Mar 2026; 4 posts after April 2026 |

### 3.2 What the company says (COMPANY CLAIM)
- Rapido co-founder's launch post (LI-09, 2026-03-06): "Transparency", "Honest pricing", "Zero commission for restaurants"; "Bangalore is just the beginning."
- Ownly team member (FO-01, ≈ 2026-09-11): "After a month of building supply… Ownly is officially LIVE in Hyderabad!" No localities, offers, fee or restaurant count given.

### 3.3 Claims in circulation — several conflict
| Claim | Items | Status |
|---|---|---|
| Zero commission for restaurants | 10+ | Consistent; company claim |
| "Up to 15% cheaper"; meals capped at ₹100–₹150 / "sub-₹250" | LI-01, LI-03, LI-06, LI-11, LI-13 | Pre-launch promises |
| Customer delivery fee ₹10–₹25 / ₹20–₹50 tiers / free ≥ ₹100 / ₹30 flat | LI-13, LI-04, LI-05, X-02, LI-08 | **Contradictory over time** (see §2.6) |
| Restaurants pay a per-order fee (₹25 / ₹29.50, pilot) or a monthly listing fee | LI-05, X-02; Reddit beliefs | Unverified — for Agent A |
| JP Morgan: Swiggy Toing "materially more successful" than Ownly, helped by marketing spend | LI-21 (Moneycontrol, 2026-06) | Media relay of analyst view |
| Brokerage: short-term price pressure, limited long-term impact unless Ownly scales | LI-12 | Attribution unverified |

### 3.4 Dominant reaction: durability scepticism
The most-reacted visible comment on the highest-engagement post (LI-01, 1,150 reactions) calls zero fees "just a carrot dangling to capture the market". A Hinglish comment (LI-17-C2) says cash will burn only while investor money lasts. The same belief dominates Reddit (§2.7).

### 3.5 Brand spillover
On the co-founder's post, 3 of 9 visible comments are Rapido **ride** grievances: an unanswered driver complaint, a women's-safety allegation (unverified), and "I don't see Transparency, Honest pricing and customer support" (LI-09-C5).

### 3.6 First-hand accounts (n = 5)
- LI-10 (2026-05-15): "The pricing is consistently 35% lower than the giants… But support is almost non-existent and delivery is consistently delayed."
- LI-19 (2026-03-07): "the final price on Zomato was cheaper… Because of platform offers and credit card discounts"; limited restaurants; wrong order; slow support.
- LI-19-C2 (≈ Aug 2026): non-delivery, the rider refused handover, support "cannot do anything"; Swiggy handled a similar case better.
- LI-09-C8, LI-09-C2: delays, missing items, a support chat closed unresolved.

## 4. X / Twitter (n = 7 snippets)
Launch and pilot announcements, a fee-tier description (X-02), influencer framing (X-03), Toing matching offline prices (X-04), and the viral corn-pizza comparison (X-01, §2.4). X-01 is a single low-value, launch-week order, when Ownly reportedly charged no delivery fee. It shows how large the gap *can* be, not how large it typically is.

---

## 5. City split — and why Hyderabad cannot be compared yet

| City explicitly mentioned (relevant, de-dup) | Items |
|---|---|
| Bengaluru | 35 (most other items are Bengaluru by context but not stated) |
| Hyderabad | 4 — FO-01 (staff launch post), RD-1vu5s4x-p50728x ("Not available in Hyderabad!", 2026-08-21), RD-1vu5s4x-p5j6tvy ("Can't wait for it to come to Hyderabad. Tired of zomato monopoly", 2026-08-24), RD-1vu5s4x-p5kk204 (speculation) |
| Mumbai 4 · Delhi 3 · Pune 2 · Chennai 1 · Ghaziabad 1 (ride complaint) · West Bengal 1 · "tier-2 city" 1 | availability questions (22 items total) |
| Hyderabad supply side (r/hyderabad; city not named in the text) | 1 — RD-1w0k0bk (2026-08-28): a restaurant owner says Swiggy **Toing** cut its prices "drastically without consent", that Toing's "offline prices" are wrong, and that they cannot delist. About Toing, not Ownly, but it shows Hyderabad restaurants pushing back on offline-price-matching models (H9/H10) |

- r/hyderabad searches for "ownly" returned **0 relevant threads**. No Gachibowli, Kondapur or Financial District mentions of Ownly were found on any source.
- **Implication:** every consumer theme above is **Bengaluru evidence**. Whether it transfers to Hyderabad (H9) must come from the team's primary research and competitor audit, not from social data.

---

## 6. Contradictions to carry forward (do not resolve them by picking a side)

| Topic | Says one thing | Says the opposite |
|---|---|---|
| Is Ownly cheaper? | 6 bill comparisons; "consistently 35% lower" (LI-10); switchers | Coupons/card offers make incumbents equal or cheaper (7); parity by area (4); pricier listings (3); in-store price lower (7) |
| Delivery fee | "free" / "no delivery fee" (3) | ₹5, ₹15, ₹30 flat, ~₹40 fees (ambiguous) |
| Reliability | "Ordered plenty of times but no issues" (RD-1vw5429-p5e5kxh); "10-12 times, and no issues" (RD-1w8qx26-p86x8k1) | 46 fulfilment-failure incidents; "3 times… All 3 were terrible" (RD-1w8qx26-p87mqyk) |
| Support | "refund immediately" (RD-1w8qx26-p854g39); "processed refund without much hassle" (RD-1tmgwrf-onn8bjy) | 29 support/refund failures; refunds only after threatening consumer court (RD-1tmgwrf-oq1lhij) |
| Rapido brand | "does ok without excessive charges" | "Rapido DNA… don't expect any help" |
| App | "Love the UI; very minimal" (RD-1vkoo9i-p31xtqr) | "slow and glitchy" (RD-1qcrc1f-ocrqfj6) |
| Incumbent vs Ownly failures | "same happens with swiggy zomato" (3 items) | "Swiggy… customer service is a million times better" (RD-1w8qx26) |

---

## 7. Hypothesis support table (social evidence only — never sufficient to validate)

| H | What this corpus suggests | Direction | Strength | What primary research must do |
|---|---|---|---|---|
| H1 Problem intensity | Incumbent fee stacks and opacity, "3–5x" delivered prices, DIY workarounds (7), incumbent support failures; but also "cost of convenience" acceptance (4) | Supports pain existing | Weak (self-selected) | Measure fee frustration/abandonment frequency (Price Pain Index); don't assume |
| H2 Price proposition | Large gaps on some baskets **and** parity/inversion after offers; restaurant-set prices; durability distrust (37) | **Mixed** | Weak | Compare **total checkout after coupons, card offers and subscriptions**; add a price-durability expectation item |
| H3 Price vs ETA | 1 accepts +10–15 min for ~₹150; batching and 1-hour ETAs reported | Unclear | Very weak | Choice tasks with ETA levels |
| H4 Price vs reliability | Central tension; 4 "accept problems for savings" vs 6 "reliability over price / pay more"; failures dominate first-hand posts | **Contested** | Weak | Include on-time probability and refund assurance as attributes |
| H5 Price vs selection | 1 accepts fewer restaurants for simple pricing; limited assortment (6); unreliable listings | Unclear | Very weak | Assortment attribute; "favourite restaurant available?" item |
| H6 Students vs professionals | Only indirect: Pluxee meal-card gap (salaried), PG/hostel mentions, intern discount nostalgia | Cannot assess | None | Segment comparison in survey |
| H7 Rapido brand | Two-sided spillover; uneven awareness; "Swiggy's child" confusion | **Two-sided** | Weak | Brand-blind vs brand-reveal; measure trust both ways |
| H8 WTP for delivery | Fee confusion; preference for explicit labelled fee (9); ₹20–30 reliability premium (1); ₹200/month subscription idea (1); small-cart cancellations | Suggests explicit fee framing matters | Weak | Gabor-Granger with explicit fee and what it buys; confirm current fee in audit |
| H9 Transferability | No Hyderabad consumer data; Bengaluru failure modes (shared riders, late-night, support) are operational and could transfer; 1 expects price rises in new cities | Risk flagged | None for Hyderabad | Hyderabad survey, interviews, audit |
| H10 Assortment threshold | Limited restaurants early; service radius; listings not accepting orders; merchant-run r/Ownly | Barrier exists in Bengaluru | Weak | Coverage in audit; must-have restaurant item |
| H11 Behavioural intent | Not testable here; astroturf accusations both ways; one prospect deterred by negative posts | — | — | Fake-door test |
| H12 Repeat use | 18 repeat-use and 4 full-switch signals; 3 explicit churns; several first-order failures → account deletion; perceived price creep after repeat orders | Mixed; **first-order experience looks pivotal** | Weak | Ask first-order outcome and its effect on continued use |

---

## 8. Suggested additions for the instruments (for the survey, interview, and audit owners)

- **Survey:**
  - Expected price durability ("in 12 months this app will be…").
  - Usual ordering time, including after 11 pm.
  - Typical order size, and whether the respondent orders for a group.
  - Payment methods needed: COD, UPI, meal cards such as Pluxee.
  - Card offers and subscriptions used.
  - For Ownly users: outcome of the first order, and whether any refund was received and how long it took.
  - A preference item: explicit fee vs "free delivery" with a higher menu price.
- **Choice experiment:** keep refund assurance and on-time reliability as attributes. Price-only framing would miss the main theme of this corpus.
- **Competitor audit:**
  - Record totals **with and without** coupons, card offers and subscriptions.
  - Record the strike-through MRP versus the listed price.
  - Include Swiggy Toing where it operates.
  - Sample late-night slots and two basket sizes (< ₹200 and ≥ ₹1,000).
  - Record Ownly's displayed delivery fee exactly as shown.
  - Check whether listed restaurants actually accept orders.
- **Interviews:** probe the last failed order on any app and how it was resolved. Probe trust in "no hidden charges" claims, and whether price differences were checked before ordering.

---

## 9. Limitations and items for the lead to reconcile

1. **Not representative.** Self-selection, negativity bias and viral-thread concentration (Aug 2026). Bengaluru only.
2. **AI first-pass coding.** Same-author inferences and severity scores need blind human re-coding (`codebook_social.md` §6). Several LinkedIn texts are fetch-tool summaries — never quote those rows.
3. **Access limits.** Reddit via RSS only (no votes/authors; long threads may be truncated). Reddit robots.txt unreadable from the script. LinkedIn's robots notice prohibits automated access without permission; volume was kept to single public-page views. X via snippets only.
4. **Coverage.** ~38 broader 2025 speculation threads were not fetched. The follow-up pass for Toing, fee and Hyderabad-locality queries found 2 new threads and no Gachibowli/Kondapur mentions (queries and hit counts in `search_log.csv`). Reproduction scripts are in `scripts/`. The raw RSS cache is not kept, because it contains usernames.
5. **For Agent A to verify:** restaurant-side fees (per-order vs monthly), the JP Morgan Toing note, the Nirmal Bang view, Ownly's current Hyderabad delivery fee and service areas, the "FIFA offer", and a second-hand "₹150–170 cash burn per order" claim (RD-1vp2t3m-p45k2my).
6. **Merging with app-store data:** equivalent codes are mapped in `codebook_social.md` §5. Social-only codes (durability distrust, brand spillover, trade-off statements) should not be stacked with app-review frequencies.
