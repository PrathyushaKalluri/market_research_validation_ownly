# Social & Community Voice — Codebook (v1, AI first pass, needs human validation)

**Created:** 2026-09-14 by Agent B2. **Applies to:** `social_coded.csv`. **Status:** every row `coder = ai_first_pass`, `human_verified` blank.
Companion to the app-store codebook (`../app_stores/codebook.md`, Agent B1). Field definitions for severity, order stage, sentiment and behavioural flags are **deliberately identical** so the two datasets can be stacked.

---

## 1. Collection and access rules actually applied

| Source | Route used | What was *not* done | Consequence |
|---|---|---|---|
| Reddit | Reddit's public Atom/RSS feeds (search feeds + per-thread comment feeds), no login, descriptive User-Agent, 12 s spacing, back-off on HTTP 429 | JSON API returned 403 (network policy) and old.reddit search redirects to login — neither was retried or worked around. `robots.txt` could not be read from the script (blocked page). | RSS exposes no vote/comment counts → `engagement` = "not exposed by RSS". Thread feeds return at most ~100 entries → very long threads are truncated. |
| LinkedIn | Individual public post/article URLs found via web search, viewed logged-out (~21 fetches) | No login, no Chrome session, no feed scrolling, no profile pages. | Only the comments LinkedIn shows logged-out were captured (typically first 2–10). LinkedIn's robots notice prohibits automated access without permission; volume was kept to single-page views, and this tension is logged as a limitation. |
| X / Twitter | Search-engine snippets only (`site:x.com`) | x.com pages are login/JS-walled; not accessed. | X text is the indexed snippet, often truncated (`verbatim_status = search_snippet`). |
| Facebook, Instagram, YouTube comments, Quora | Attempted via search/fetch | Login-walled or no results | Not mined; recorded in `search_log.csv`. |
| Public forums | StartupTalky community (1 item); consumercomplaints.in (0 Ownly items) | — | — |

**Privacy:** no usernames, display names, profile URLs or commenter names are stored. Names of support agents / riders appearing inside complaint text are redacted as `[name redacted]`. Post URLs are kept for traceability (some LinkedIn/X post URLs contain the poster's handle as a URL slug; the dataset does not store it separately and reports never cite it).

**Text fidelity (`verbatim_status`):** `yes` = copied from page; `yes_partial` / `yes_truncated_60w` = verbatim but shortened; `partial_retrieval_summary` / `no_retrieval_summary` = the fetch tool returned a summary — **never quote these rows**; `search_snippet` = search-index text. A human must open the URL before any quote goes into a deck.

---

## 2. Process (inductive)

1. Read every captured item in full before coding.
2. Open-coded each item with short descriptive labels in the author's terms ("carrot dangling", "rider refused handover", "Zomato cheaper after card offer").
3. Grouped open labels into the theme codes below; wrote include/exclude rules; re-applied the final codes to all items (multi-label `themes`, one `primary_theme`).
4. Where a theme already exists in the app-store codebook for the same concept, the social code maps to it (Section 5) rather than inventing a synonym for analysis — separate names are kept only where social data adds a distinction app reviews do not have (e.g., ride-vs-food brand spillover).
5. **Two populations are coded separately and must never be pooled for frequency claims:**
   - **Experience items** — a person describes their own ordering/usage experience (`order_stage` ≠ `NA_business_commentary`).
   - **Narrative items** — commentary on the business model, launches, competition (`order_stage = NA_business_commentary`). LinkedIn is dominated by these.

---

## 3. Theme codes

### A. Consumer experience — fulfilment and recovery (maps to app-store group A/B)
| Code | Include when | Exclude / use instead |
|---|---|---|
| `NON_DELIVERY` | food never arrived or marked delivered but not received | late but arrived → `LATE_DELIVERY` |
| `LATE_DELIVERY` | delay beyond promise, "consistently delayed", long waits | — |
| `RIDER_CONDUCT` | rider unreachable, refused handover, misconduct | ride-hailing captain (not food) → `RAPIDO_RIDE_SPILLOVER_NEGATIVE` |
| `MISSING_WRONG_ITEMS` | wrong or missing items | — |
| `FOOD_QUALITY` | stale/poor/unhygienic food | — |
| `SUPPORT_UNRESPONSIVE` | support unreachable, closes chats unresolved, "cannot do anything" | slow but engaged → `SUPPORT_SLOW` |
| `SUPPORT_SLOW` | support eventually engages but only after a noticeable wait | — |
| `INCUMBENT_BETTER_RECOVERY` / `INCUMBENT_BETTER_EXPERIENCE` | explicitly says Swiggy/Zomato handled the same kind of problem better | — |
| `REFUND_ISSUE` | refund pending/denied | — |
| `RESTAURANT_PREP_GOVERNANCE_GAP` | attributes delays to restaurant prep the platform cannot/does not police | — |

### B. Price and value (maps to app-store group E)
| Code | Include when |
|---|---|
| `PRICE_SAVINGS_OBSERVED` | user reports paying less on Ownly than on an incumbent for their own order(s) |
| `USER_BILL_COMPARISON` | user posts item-level/checkout-level numbers across platforms (always CONSUMER-GENERATED, unverified) |
| `INCUMBENT_CHEAPER_AFTER_OFFERS` | user finds the incumbent's final price lower once discounts, card offers or subscriptions apply |
| `NO_HIDDEN_FEES_POSITIVE` | praises absence of platform/packaging fees or "pay only for food + delivery" |
| `INCUMBENT_PRICE_OBSTACLE` | describes incumbent fee stack/dynamic pricing as the problem |
| `CLEAN_APP_NO_UPSELL` | values absence of ads/clickbait/upsell clutter |
| `AGGREGATOR_MARKUP_WORKAROUND` | describes bypassing aggregators (courier pickup, calling restaurant) to avoid markup |

### C. Assortment and product (maps to app-store groups C/F)
| Code | Include when |
|---|---|
| `ASSORTMENT_LIMITED` | fewer/less popular restaurants than incumbents |
| `DISCOVERY_UX_BASIC` | homepage/search/filtering too basic to find food |
| `CITY_AVAILABILITY_QUESTION` | asks whether Ownly is available / coming to a city |

### D. Trust and brand
| Code | Include when | Note |
|---|---|---|
| `RAPIDO_RIDE_SPILLOVER_NEGATIVE` | complaint about Rapido **rides/captains/ride support** posted in an Ownly context | Evidence for H7 (brand baggage); **excluded** from food-experience frequencies |
| `SAFETY_CONCERN` | personal-safety allegation | Always severity 4; unverified |
| `SLOGAN_THROWN_BACK` | uses Ownly's own values ("transparency", "honest pricing") to criticise Rapido/Ownly | — |
| `TRUST_LOSS_SCAM_FRAMING` | "scam", "cheated", "loot" | Same as app-store code |
| `EARLY_LAUNCH_TRUST_RISK` | argues first bad experiences will stop people returning | — |
| `TRUST_AS_MOAT` | trust framed as the durable competitive advantage | narrative |
| `FUTURE_FEE_CREEP_EXPECTED` | expects low prices/zero fees to disappear after market capture | Consumer-side scepticism about the durability of the proposition — relevant to H2/H7 |
| `LOW_PLATFORM_LOYALTY` | asserts users switch freely / are not loyal | — |

### E. Narrative / business commentary (not consumer demand evidence)
| Code | Include when |
|---|---|
| `LAUNCH_CLAIM_RELAY` | repeats company launch claims (zero commission, meal price caps, "15% cheaper") without own evidence |
| `FEE_MODEL_DESCRIPTION` | states a specific fee structure (tiers, flat ₹30, restaurant fee) |
| `SUSTAINABILITY_SKEPTICISM` | questions whether the model can make money / last |
| `RESTAURANT_ECONOMICS_POSITIVE` | argues restaurants benefit from zero commission |
| `RAPIDO_ECOSYSTEM_ADVANTAGE` | cites rider fleet, app base, super-app as the edge |
| `COMPETITOR_CONTEXT` | Swiggy Toing, Flipkart/ONDC, incumbent responses |
| `MARKET_EXPANSION_FIRST_TIME_USERS` | frames the opportunity as new users, not switching |
| `ANALYST_VIEW` | relays brokerage/analyst opinion |
| `WELCOME_THIRD_COMPETITOR` | welcomes a challenger to the duopoly |
| `RELIABILITY_AT_SCALE_CONCERN` | doubts consistent delivery at scale |
| `HYDERABAD_LAUNCH` / `SUPPLY_BUILDING` | Hyderabad launch statements / restaurant supply build-out |

### F. Codes that emerged from Reddit (added after reading Reddit threads)

**Trade-off and switching statements (most decision-relevant)**
| Code | Include when | Hypothesis |
|---|---|---|
| `ACCEPTS_WAIT_FOR_SAVINGS` | user says a longer delivery time was acceptable because of the saving | H3 |
| `ACCEPTS_HASSLE_FOR_SAVINGS` | user tolerates occasional problems because of the saving | H4 |
| `RELIABILITY_OVER_PRICE` | user says the lower price is not worth unreliability ("the lower price is not worth it") | H4 |
| `WTP_FOR_RELIABILITY` | user says they would pay more (sometimes with an amount) for reliable delivery/resolution | H4, H8 |
| `TOLERATE_CHALLENGER_HICCUPS` | argues users should accept early problems to keep a low-fee challenger alive | H4, H12 |
| `SWITCH_DESPITE_TEMPORARY_PRICING` | would switch now even while expecting prices to rise later | H2, H12 |
| `FULL_SWITCH_TO_OWNLY` | says they now use Ownly exclusively / "completely moved" | H12 |
| `FALLBACK_TO_INCUMBENT` | a failed Ownly order ended with ordering on Swiggy/Zomato | H12 |
| `SEGMENTED_PLATFORM_USE` | uses different apps for different baskets/occasions (e.g., small orders Ownly, large orders with card offers Swiggy) | H2, H8, H10 |
| `PRICE_AS_SWITCH_TRIGGER` | names price as the switching factor | H2 |
| `CHURN_ADVOCACY` | urges others to delete/avoid | H12 |

**Price-comparison nuance**
| Code | Include when |
|---|---|
| `OWNLY_PRICIER_OBSERVED` | user reports a specific listing costing more on Ownly |
| `PRICE_PARITY_OBSERVED` | user finds little difference; savings limited to absent fees |
| `PRICE_COMPARISON_DISPUTE` | users contest a posted comparison (item size mismatch, different restaurant) |
| `RESTAURANT_CAPTURES_SAVINGS` | says restaurants list the same prices as on incumbents, so zero commission benefits the restaurant, not the customer |
| `MENU_PRICE_INFLATION_ON_OWNLY` | alleges inflated MRP with a strike-through discount on Ownly |
| `MENU_MARKUP_EXPECTED_ON_OWNLY` | expects (not observed) restaurants to mark up on Ownly too |
| `NO_DISCOUNTS_ON_OWNLY` | notes Ownly lacks incumbent-style coupons/discounts |
| `INCUMBENT_CHEAPER_CONDITIONAL` / `INCUMBENT_DEFENSIVE_DISCOUNTING` | incumbent wins under conditions (small minimum order) / incumbent coupons read as a response to Ownly |
| `MENU_MARKUP_INCUMBENT`, `INCUMBENT_FEE_OPACITY`, `INCUMBENT_FEE_STACK_FRUSTRATION`, `TRANSPARENT_DELIVERY_FEE_PREFERENCE`, `DELIVERY_PRICE_LEVEL_TOO_HIGH` | incumbent pricing pain (H1) |
| `PORTION_SIZE_DIFFERS_OFFLINE` | offline portion differs from delivery portion — complicates "offline price" comparisons |
| `RESTAURANT_SETS_PRICES`, `RESTAURANT_SETS_DISCOUNTS` | attributes menu price/discount to restaurants |
| `CHECKOUT_PRICE_FOCUS`, `MULTI_HOMING_PRICE_COMPARISON` | compares final checkout across apps |
| `FREE_DELIVERY_PERCEPTION` | user describes Ownly delivery as free / no delivery fee |
| `LAUNCH_DISCOUNT_TEMPORARY`, `LOW_AOV_ORDERING`, `USER_BILL_COMPARISON` | as named |

**Operations and service**
| Code | Include when |
|---|---|
| `RIDER_COORDINATION_FAILURE` | rider not moving to restaurant, wrong direction, confusion about order |
| `RIDER_MULTI_APP_OBSERVED` | rider seen with another platform's bag/packaging (shared rider supply) |
| `RIDER_UNTRAINED` | riders unfamiliar with the app |
| `TRACKING_OPACITY` | no visibility of rider after pickup |
| `ETA_DISPLAY_MISLEADING` | shown ETA far from reality |
| `LATE_NIGHT_RELIABILITY_RISK` | failures tied to late-night ordering |
| `LOCATION_DEPENDENT_RELIABILITY` | experience attributed to locality |
| `LARGE_ORDER_TRUST_RISK` | failures/trust concerns tied to large baskets (e.g., ₹2k orders) |
| `DELIVERY_PROBLEMS_RECURRING`, `PLATFORM_FAULT_ATTRIBUTION`, `OPERATIONS_UNDERSTAFFED` | repeated failures; blames platform not restaurant; attributes to lean ops |
| `COMPENSATION_REVERSED` | offered compensation then withdrawn |
| `SUPPORT_WORKAROUND`, `SUPPORT_RECOVERY_POSITIVE`, `RELIABLE_EXPERIENCE_POSITIVE` | as named |
| `MEAL_CARD_PAYMENT_GAP` | meal cards (e.g., Pluxee) not accepted — relevant to salaried users |
| `NO_CASH_ON_DELIVERY`, `APP_ACCESS_ISSUE`, `SERVICE_AREA_LIMITED`, `APP_UX_SLOW_GLITCHY`, `LISTING_MENU_ACCURACY` | as named (map to app-store codes) |

**Brand, trust, competition, supply**
| Code | Include when |
|---|---|
| `RAPIDO_BRAND_NEGATIVE_SPILLOVER` | explicitly transfers distrust from Rapido to Ownly ("Rapido DNA") — H7 |
| `LEGITIMACY_REASSURANCE`, `BRAND_ASSOCIATION_QUESTION`, `PROPOSITION_RECALL_NO_HIDDEN_COSTS`, `LOW_AWARENESS`, `NEGATIVE_REVIEWS_AWARENESS` | brand/awareness signals — H7 |
| `ASTROTURF_SUSPICION` | accuses posters of being paid by Ownly or by incumbents — a signal that the community distrusts comparisons in both directions |
| `INCUMBENT_DISTRUST`, `INCUMBENT_SUPPORT_BAD`, `INCUMBENT_LOYALTY`, `INCUMBENT_SAME_PROBLEMS`, `INCUMBENT_FEE_DISTRUST` | incumbent-side attitudes |
| `TOING_VS_OWNLY`, `COMPETITOR_ALTERNATIVE_SUGGESTED` | Swiggy Toing / Swish / ONDC as alternatives |
| `RIDER_EARNINGS_CONCERN` | doubts captain earnings under flat fee — supply risk (H9) |
| `CITY_EXPANSION_PRICE_RISE_EXPECTED` | expects prices to rise after entering new cities (H9) |
| `RAPIDO_PARCEL_SUBSTITUTE` | uses Rapido parcel + direct restaurant order as a DIY alternative |
| `HISTORICAL_PRICE_CONVERGENCE`, `TRIAL_CURIOSITY`, `GENERAL_SUPPORT_FOR_OWNLY`, `RAPIDO_APP_INTEGRATION` | as named |

**De-duplication rules applied to Reddit**
- Verbatim cross-posts of the same text in other threads are coded `relevant = 0` with a note naming the kept item.
- Follow-up comments where the text makes clear it is the same author/incident as an earlier item carry `[SAME_INCIDENT:<item_id>]` in `coding_note`; frequency tables count the incident once. RSS gives no author field, so this is inferred from content and flagged as such.

---

## 4. Other fields (identical to app-store codebook)

- **`severity` 1–4**, worst issue in the item: 1 cosmetic/request; 2 inconvenience, no failed order or money at risk; 3 failed/incorrect order or money at risk; 4 safety/hygiene/dietary breach, fraud-like conduct, or money described as lost after contacting support. Blank for praise/narrative.
- **`order_stage`**: discovery_onboarding, browse_menu, pricing_checkout, payment, dispatch_eta, delivery_handoff, food_quality_accuracy, post_order_support_refund, app_account, **NA_business_commentary** (social-only value).
- **`sentiment`** (no star ratings on social): `pos` / `neg` / `mixed` (both an explicit positive and an explicit negative about Ownly) / `neutral` (informational or question).
- **`switching_trigger_flag`**: 1 if the item states a reason to move to or away from Ownly; direction in `switching_trigger_text` (`to_ownly:` / `away_from_ownly:`).
- **`churn_signal`**: 1 only for an explicit stop/uninstall/never-again statement.
- **`repeat_use_signal`**: 1 if evidence of more than one completed order or ongoing use; inference noted in `coding_note`.
- **`city_mentioned`**: only when a city/locality is explicitly named as the author's context.
- **Comment fields** (`price_value_comment` etc.) are **coder summaries, not quotes**; single-quoted fragments inside them are verbatim.
- **`evidence_label`**: CONSUMER-GENERATED (personal experience/opinion), COMPANY CLAIM (Ownly/Rapido staff or execs), MEDIA REPORT (media pages/journalists relaying facts or claims), INTERPRETATION (commentator's own analysis).
- **`author_type`** (in raw file): consumer, restaurant_owner_or_staff, delivery_captain, ownly_rapido_employee_or_exec, competitor_employee, investor_analyst_media, marketer_agency, unknown; Reddit defaults to `consumer_unverified` unless text shows otherwise.

---

## 5. Mapping to app-store codebook (for stacking datasets)

| Social code | App-store code (B1) | Mapping |
|---|---|---|
| NON_DELIVERY | NOT_DELIVERED_OR_FALSE_DELIVERED | equivalent |
| LATE_DELIVERY | LATE_DELIVERY_ETA_BREACH | equivalent |
| RIDER_CONDUCT | RIDER_CONDUCT_OR_UNREACHABLE | equivalent |
| MISSING_WRONG_ITEMS | MISSING_OR_WRONG_ITEMS | equivalent |
| FOOD_QUALITY | FOOD_QUALITY_HYGIENE | equivalent |
| SUPPORT_UNRESPONSIVE | SUPPORT_UNRESPONSIVE_OR_SCRIPTED | equivalent |
| SUPPORT_SLOW | SUPPORT_UNRESPONSIVE_OR_SCRIPTED | narrower (roll up) |
| REFUND_ISSUE | REFUND_DELAY_OR_DENIAL | equivalent |
| TRUST_LOSS_SCAM_FRAMING | TRUST_LOSS_SCAM_FRAMING | identical |
| EARLY_LAUNCH_TRUST_RISK | EARLY_GOOD_THEN_DECLINE | related, not equivalent (social = argument; app = lived sequence) |
| NO_HIDDEN_FEES_POSITIVE | NO_HIDDEN_FEES_POSITIVE | identical |
| PRICE_SAVINGS_OBSERVED | LOWER_PRICE_VALUE_POSITIVE | narrower (requires own-order comparison) |
| ASSORTMENT_LIMITED | ASSORTMENT_MORE_RESTAURANTS | equivalent |
| CITY_AVAILABILITY_QUESTION | CITY_EXPANSION_REQUEST | equivalent |
| DISCOVERY_UX_BASIC | APP_CHECKOUT_BUG / APP_UX | partial (UX, not bug) |
| INCUMBENT_CHEAPER_AFTER_OFFERS, USER_BILL_COMPARISON, FUTURE_FEE_CREEP_EXPECTED, RAPIDO_RIDE_SPILLOVER_NEGATIVE, INCUMBENT_BETTER_RECOVERY, RESTAURANT_PREP_GOVERNANCE_GAP, AGGREGATOR_MARKUP_WORKAROUND | — | social-only; no app-store equivalent |
| All Group E narrative codes | — | social-only; never stacked with app reviews |

---

## 6. Required human validation

1. Two team members independently re-code all **experience items** (expected to be a small set) and a random 30% of narrative items, blind to this coding.
2. Cohen's κ on `primary_theme` (grouped to A–E if κ < 0.6) and on `severity`.
3. Open every URL for any row planned as a quote; replace retrieval-summary rows with verbatim text or drop them.
4. Set `human_verified = 1` after reconciliation; bump to v2.
