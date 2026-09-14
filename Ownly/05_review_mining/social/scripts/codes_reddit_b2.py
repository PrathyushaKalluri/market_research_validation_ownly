"""Reddit coding batch 2 (AI first pass). Reuses C()/X() helpers from codes_reddit.py conventions."""
import json, os
SCR = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(SCR, "codes.json")
codes = json.load(open(P))
def C(i, fh, sent, themes, sev="", stage="NA_business_commentary", hyp="", ev="CONSUMER-GENERATED", sw="", churn=0, rep=0,
      price="", eta="", assort="", support="", trust="", note="", author=None, city=None):
    t = themes.split(";")
    d = dict(relevant=1, first_hand_ownly_use=fh, sentiment=sent, themes=themes, primary_theme=t[0], severity=sev, order_stage=stage,
             switching_trigger_flag=1 if sw else 0, switching_trigger_text=sw, churn_signal=churn, repeat_use_signal=rep,
             price_value_comment=price, delivery_eta_comment=eta, assortment_comment=assort, support_comment=support,
             trust_safety_quality_comment=trust, hypotheses_linked=hyp, evidence_label=ev, coding_note=note)
    if author: d["author_type"] = author
    if city: d["city_mentioned"] = city
    codes[i] = d
def X(*ids, note="banter/off-topic; no Ownly-relevant content"):
    for i in ids:
        codes[i] = dict(relevant=0, first_hand_ownly_use=0, sentiment="", themes="", primary_theme="", severity="", order_stage="",
                        switching_trigger_flag=0, switching_trigger_text="", churn_signal=0, repeat_use_signal=0, price_value_comment="",
                        delivery_eta_comment="", assortment_comment="", support_comment="", trust_safety_quality_comment="",
                        hypotheses_linked="", evidence_label="", coding_note=note)

# ---- RD-1vq18l9  r/Zomato  2026-08-16  "Zomato and ownly price difference. 80% more" ----
T = "RD-1vq18l9"
C(T, 1, "pos", "USER_BILL_COMPARISON;PRICE_SAVINGS_OBSERVED", stage="pricing_checkout", hyp="H1;H2", sw="to_ownly: ₹220 vs ₹392 same place same items",
  price="'₹392 on Zomato vs ₹220 on Ownly'; '₹220 is not even an offer price'", note="Screenshots not retrievable; single basket; restaurant unnamed")
C(T+"-p41yzmn", 0, "neg", "FUTURE_FEE_CREEP_EXPECTED;SUSTAINABILITY_SKEPTICISM", hyp="H2;H7")
C(T+"-p4226ts", 0, "neutral", "FEE_MODEL_DESCRIPTION", hyp="H8", ev="INTERPRETATION", price="claims flat listing fee/subscription for restaurants and a per-km delivery fee", note="Per-km claim conflicts with '₹30 flat' reports — unverified")
C(T+"-p42pf3j", 0, "neutral", "SUSTAINABILITY_SKEPTICISM", hyp="H2")
C(T+"-p42qjgr", 0, "neutral", "FEE_MODEL_DESCRIPTION", hyp="H8", ev="INTERPRETATION", note="Guesses subscription plans like rider plans")
C(T+"-p47obms", 0, "neutral", "FEE_MODEL_DESCRIPTION", hyp="H8", ev="INTERPRETATION", note="Claims monthly restaurant listing fee — unverified")
C(T+"-p464h7b", 0, "neg", "SUSTAINABILITY_SKEPTICISM;FUTURE_FEE_CREEP_EXPECTED", hyp="H2", note="Cites incumbent 4–5% EBITDA/order — unverified")
C(T+"-p46axsf", 0, "neutral", "FEE_MODEL_DESCRIPTION;RAPIDO_ECOSYSTEM_ADVANTAGE", hyp="H8;H9", ev="INTERPRETATION", note="Claims delivery fee goes entirely to rider; revenue from restaurant+rider subscriptions — unverified")
C(T+"-p46l72e", 0, "pos", "RESTAURANT_ECONOMICS_POSITIVE;RAPIDO_ECOSYSTEM_ADVANTAGE", hyp="H2;H9", ev="INTERPRETATION", note="Relays '7 percent of blr' share")
C(T+"-p474rcv", 0, "pos", "SWITCH_DESPITE_TEMPORARY_PRICING", stage="pricing_checkout", hyp="H2;H12", sw="to_ownly: 'deliver at half the price. Even if it's temporary'")
C(T+"-p5fe5po", 0, "neutral", "NO_DISCOUNTS_ON_OWNLY", stage="pricing_checkout", hyp="H2", price="Ownly lacks Zomato/Swiggy-style discounts")
C(T+"-p420vqm", 0, "neutral", "INCUMBENT_CHEAPER_AFTER_OFFERS", stage="pricing_checkout", hyp="H2", price="Zomato had ₹120 off at same restaurant", note="First-hand Zomato experience, not Ownly")
C(T+"-p46pu29", 0, "neutral", "RESTAURANT_SETS_DISCOUNTS", hyp="H2", ev="INTERPRETATION", note="Says restaurants toggle discounts in platform console (claims to have seen it)")
C(T+"-p41xfda", 0, "neutral", "CITY_AVAILABILITY_QUESTION", stage="discovery_onboarding", hyp="H9", city="Pune")
C(T+"-p41yho2", 0, "neg", "SUSTAINABILITY_SKEPTICISM", hyp="H9", city="Pune")
C(T+"-p43q5jq", 0, "pos", "INCUMBENT_LOYALTY", hyp="H12", note="'Only over zomato anyday' — loyalty to incumbent")
C(T+"-p45pw2c", 0, "neutral", "LOW_PLATFORM_LOYALTY", hyp="H12", note="Advises app-hopping to whichever is cheapest")
C(T+"-p45ypr1", 0, "neutral", "CITY_AVAILABILITY_QUESTION", stage="discovery_onboarding", hyp="H9", city="Mumbai")
C(T+"-p467sfc", 0, "neutral", "SUSTAINABILITY_SKEPTICISM", hyp="H8")
C(T+"-p46udk0", 0, "neutral", "FREE_DELIVERY_PERCEPTION", stage="pricing_checkout", hyp="H8", note="Aug 2026: commenter perceives Ownly delivery as free — conflicts with '₹30 flat fee' reports; fee may vary by offer/area")
C(T+"-p46crht", 0, "neg", "INCUMBENT_SUPPORT_BAD;INCUMBENT_DISTRUST", stage="post_order_support_refund", hyp="H1;H4", support="Zomato support 'horrendous'; 'never get refunds'")
C(T+"-p47wj6j", 0, "neg", "INCUMBENT_SUPPORT_BAD", stage="post_order_support_refund", hyp="H4", support="Zomato support is a bot that says to email")
C(T+"-p46g974", 0, "neutral", "TRIAL_CURIOSITY", hyp="H4", note="Asks about Ownly service quality — reliability as the open question after price")
C(T+"-p46nfzv", 0, "neg", "PRICE_COMPARISON_DISPUTE", stage="pricing_checkout", hyp="H2", note="Claims the reverse can be shown for other restaurants — assertion, no data")
C(T+"-p471knv", 0, "neutral", "SEGMENTED_PLATFORM_USE", stage="pricing_checkout", hyp="H2;H8;H10", price="'For small orders ownly For large orders with credit card offers Swiggy'", note="Basket-size segmentation of platform choice — key for H2/H8")
C(T+"-p47k28x", 0, "neutral", "CITY_AVAILABILITY_QUESTION", stage="discovery_onboarding", hyp="H9")
C(T+"-p48izuo", 0, "pos", "TOING_VS_OWNLY", stage="pricing_checkout", hyp="H2", price="recommends Swiggy Toing: zero platform fee, lower than Zomato")
C(T+"-p4d4532", 0, "neutral", "TOING_VS_OWNLY;INCUMBENT_CHEAPER_AFTER_OFFERS", stage="pricing_checkout", hyp="H2", price="Swiggy final price after discount always cheaper than Toing", note="First-hand Toing/Swiggy comparison, not Ownly")
C(T+"-p49dpay", 0, "neutral", "NEGATIVE_REVIEWS_AWARENESS", stage="discovery_onboarding", hyp="H7;H12", trust="notices many negative app-store reviews about Ownly service")
C(T+"-p4a5f6l", 0, "neg", "FUTURE_FEE_CREEP_EXPECTED", hyp="H2", note="Hindi idiom 'chaar din ki chandni' = short-lived")
C(T+"-p4c42op", 0, "neutral", "HISTORICAL_PRICE_CONVERGENCE", hyp="H2", note="Recalls Zomato being much cheaper when new")
C(T+"-p4cbzrc", 1, "pos", "FULL_SWITCH_TO_OWNLY;PRICE_SAVINGS_OBSERVED", stage="pricing_checkout", hyp="H2;H12", rep=1, sw="to_ownly: 'completely moved to ownly'",
  price="at launch little difference as restaurants raised listing prices; now 'great'", note="Only explicit full-switch statement in Reddit batch 1–2")
C(T+"-p4dejfk", 0, "neg", "MENU_MARKUP_INCUMBENT;AGGREGATOR_MARKUP_WORKAROUND", stage="pricing_checkout", hyp="H1", price="item ₹550 dine-in/direct via Rapido vs ₹650 on Zomato before delivery charge", note="Self-reported offline price — unverified")
C(T+"-p4fdfta", 0, "neutral", "SUSTAINABILITY_SKEPTICISM", hyp="H2")
C(T+"-p4lnink", 0, "neutral", "RESTAURANT_SETS_PRICES", hyp="H1", ev="INTERPRETATION", note="Defends Zomato: restaurants list prices, 15–20% cut")
X(T+"-p42i3qq", note="about Zomato VIP feature; no Ownly content")
X(T+"-p45vwya", T+"-p46d3to", T+"-p46piwf", T+"-p47fza1", T+"-p48akxt")
X(T+"-p4f9640", note="moderator removal notice")

# ---- RD-1nclyuy  r/swiggy  2025-09-09  "Anyone tried Rapido's food delivery (Ownly)?" ----
T = "RD-1nclyuy"
C(T, 1, "mixed", "ASSORTMENT_LIMITED;SERVICE_AREA_LIMITED;DISCOVERY_UX_BASIC;PRICE_SAVINGS_OBSERVED", sev=1, stage="browse_menu", hyp="H2;H9;H10", city="Bengaluru",
  assort="'very few restaurants listed'", price="pricing 'caught my attention' (text truncated)", note="Pilot (HSR, Koramangala), Sep 2025")
X(T+"-nda2voc", note="subreddit automoderator message")
C(T+"-nddymv2", 0, "neg", "MENU_MARKUP_EXPECTED_ON_OWNLY", hyp="H2", note="Expects restaurants to overprice on Ownly anyway")
C(T+"-nddzh25", 0, "neutral", "EARLY_LAUNCH_TRUST_RISK", hyp="H4;H12", note="Speculative, not experience")
C(T+"-ndlcips", 0, "neutral", "INCUMBENT_BLAMED_FOR_MARKUP", hyp="H1")
C(T+"-ndm2od8", 0, "neg", "MENU_MARKUP_EXPECTED_ON_OWNLY", hyp="H2")
C(T+"-ndgfhsw", 1, "neg", "SERVICE_AREA_LIMITED", sev=2, stage="discovery_onboarding", hyp="H9", note="Could not add address — not serviceable")
C(T+"-nqpoc6l", 1, "neg", "SERVICE_AREA_LIMITED;APP_ACCESS_ISSUE", sev=2, stage="app_account", hyp="H9")
C(T+"-ocdb1nb", 0, "neutral", "SERVICE_AREA_LIMITED", stage="discovery_onboarding", hyp="H9")
C(T+"-nu17sk9", 0, "pos", "LEGITIMACY_REASSURANCE", hyp="H7", trust="reassures CTRLX is a registered Rapido subsidiary")
X(T+"-o6kcdaz", note="same incident as RD-1qcrc1f-o6kcml5 (same minute, same details) — excluded from counts to avoid double counting")
X(T+"-o6kchdh", note="verbatim duplicate cross-post of RD-1qcrc1f-o6kcml5 — excluded from counts")
X(T+"-o7nrj28", note="asks for proof; no content")
C(T+"-o8exnna", 0, "neutral", "ASTROTURF_SUSPICION", hyp="H7", note="Says the negative poster repeats the same comment on all threads, suspects Swiggy agent")
C(T+"-p6qxdxd", 0, "neutral", "ASTROTURF_SUSPICION", hyp="H7")
C(T+"-ocrpw8j", 1, "neg", "DELIVERY_PROBLEMS_RECURRING;APP_UX_SLOW_GLITCHY;SUPPORT_UNRESPONSIVE", sev=3, stage="dispatch_eta", hyp="H4;H12", rep=1, support="complained ~5 times, no fixes")
X(T+"-ocrq382", note="verbatim duplicate cross-post of RD-1qcrc1f-ocrqfj6 — excluded from counts")
C(T+"-ocwxxxt", 1, "pos", "SIMPLE_PRICING_POSITIVE;ASSORTMENT_LIMITED;NO_HIDDEN_FEES_POSITIVE", stage="pricing_checkout", hyp="H2;H5;H10", sw="to_ownly: fewer restaurants accepted for 'normal pricing'",
  price="'normal pricing, I like it. No pricing mess swiggy zomato create'", assort="'Less restaurants' — accepted", note="Accepts smaller assortment for simple pricing (H5/H10)")
C(T+"-od40bi7", 0, "neutral", "CITY_AVAILABILITY_QUESTION", stage="discovery_onboarding", hyp="H9")
C(T+"-odj5wgc", 1, "neg", "LISTING_MENU_ACCURACY;PLATFORM_RESTAURANT_CANCELLATION;SUPPORT_UNRESPONSIVE", sev=4, stage="post_order_support_refund", hyp="H4;H9;H12",
  eta="rider called after an hour: shop closed", support="cannot reach customer care, shop or rider", trust="'that cash is gone'")
C(T+"-odnsfqk", 1, "neg", "NON_DELIVERY", sev=3, stage="delivery_handoff", hyp="H4", sw="away_from_ownly: 'please don't use it'", note="Delivered to wrong location")
C(T+"-oe3k4qv", 1, "neg", "NON_DELIVERY;FALLBACK_TO_INCUMBENT;RIDER_COORDINATION_FAILURE", sev=3, stage="delivery_handoff", hyp="H4;H9;H12",
  sw="away_from_ownly: ends up ordering on Swiggy/Zomato anyway", note="'no idea what is going on with their delivery partners'")
C(T+"-og3ay3d", 1, "neg", "PLATFORM_RESTAURANT_CANCELLATION;ASSORTMENT_LIMITED;APP_UX_SLOW_GLITCHY;PRICE_SAVINGS_OBSERVED", sev=3, stage="dispatch_eta", hyp="H2;H4;H10;H12", rep=1,
  sw="away_from_ownly: two last-minute cancellations despite lower prices", price="'prices are comparitively lesser'", assort="'very few restaurant options'", note="Tried twice; both cancelled at the end while app showed rider at restaurant")
C(T+"-oganv2f", 0, "neg", "NO_CASH_ON_DELIVERY", sev=1, stage="payment", hyp="H9")
C(T+"-ojuxr45", 1, "neg", "MISSING_WRONG_ITEMS;REFUND_ISSUE;TRUST_LOSS_SCAM_FRAMING", sev=4, stage="food_quality_accuracy", hyp="H4;H12", rep=1,
  trust="ordered regular rice bowl, got mini 'each time'; no refund", note="Screenshot of support not retrievable")
C(T+"-onzmqoc", 1, "neg", "MISSING_WRONG_ITEMS;REFUND_ISSUE", sev=4, stage="post_order_support_refund", hyp="H4;H12", support="wrong order declared 'not refundable'", trust="'wasted 400rs'")
X(T+"-oo7vq9m", note="verbatim duplicate cross-post of RD-1qcrc1f-oo7vwmt — excluded from counts")
C(T+"-ouh03z1", 1, "neg", "RIDER_CONDUCT;NON_DELIVERY", sev=3, stage="delivery_handoff", hyp="H4;H9", note="'Driver ran away with my order' (screenshot not retrievable)")
C(T+"-our2y87", 1, "mixed", "ASSORTMENT_LIMITED;PRICE_SAVINGS_OBSERVED", stage="browse_menu", hyp="H2;H10", city="Bengaluru",
  price="'Reasonable Fares (Not fully affordable) still way better than all apps'", assort="'Limited Options'", note="North Bengaluru, Jun 2026")

# ---- RD-1szs0vx  r/BangaloreSocial  2026-04-30  Meghana biryani price ----
T = "RD-1szs0vx"
C(T, 1, "neg", "MENU_PRICE_INFLATION_ON_OWNLY;SLOGAN_THROWN_BACK;TRUST_LOSS_SCAM_FRAMING", sev=2, stage="pricing_checkout", hyp="H2;H7",
  price="alleges Ownly raised MRP of Meghana chicken biryani then applied a discount", trust="says this breaks 'zero inflated menu price' tagline",
  note="Replies dispute it (MRP set by restaurant; portions differ offline). Allegation unverified — the kind of 'strike-through MRP' practice the competitor audit should record")
C(T+"-oj4chb0", 0, "neg", "TRUST_LOSS_SCAM_FRAMING", hyp="H7", note="Hindi: 'loot and loot more'")
C(T+"-ojfkmah", 0, "pos", "PRICE_SAVINGS_OBSERVED;PORTION_SIZE_DIFFERS_OFFLINE", stage="pricing_checkout", hyp="H2", price="'Ownly is indeed cheaper'; says Meghana prices same across channels but offline quantity differs")
C(T+"-ojgqrge", 0, "neutral", "PORTION_SIZE_DIFFERS_OFFLINE", hyp="H2")
C(T+"-ojgvwc4", 0, "neutral", "PORTION_SIZE_DIFFERS_OFFLINE", hyp="H2", note="Claims offline portion ~half of delivery — relevant to 'offline price' comparisons in audit")
C(T+"-oj48n4f", 0, "neutral", "CHECKOUT_PRICE_FOCUS", stage="pricing_checkout", hyp="H2", note="'Check price on checkout'")
C(T+"-oj4bqtm", 0, "neg", "EARLY_LAUNCH_TRUST_RISK;MENU_PRICE_INFLATION_ON_OWNLY", hyp="H7;H12", trust="'first impression is last impression'; inflated MRP + discount seen as unfair")
C(T+"-oj4ilm4", 0, "neutral", "RESTAURANT_SETS_PRICES", hyp="H2", ev="INTERPRETATION", note="Says restaurants set one MRP for all apps; asked an owner")
C(T+"-oj5idup", 0, "neutral", "AGGREGATOR_MARKUP_WORKAROUND;RAPIDO_PARCEL_SUBSTITUTE", stage="pricing_checkout", hyp="H1;H7", price="call restaurant + book Rapido parcel 'will atleast save you 300-400 rs'")
C(T+"-oj723wi", 0, "neutral", "AGGREGATOR_MARKUP_WORKAROUND", hyp="H8", note="Workaround worthwhile only for large (>4 items) orders")
C(T+"-oj9noze", 0, "neutral", "AGGREGATOR_MARKUP_WORKAROUND", hyp="H1", note="Orders by phone from regular restaurant; free delivery above ₹1k")
X(T+"-oj4f7ce", T+"-ojb1i2n", T+"-oj4g63v", T+"-oj4h4u0", T+"-oj4hivx", T+"-oj4hrc0", T+"-oj99fqc", note="biryani recommendation banter")

json.dump(codes, open(P, "w"), indent=1, ensure_ascii=False)
print(len(codes), "codes total;", sum(1 for k in codes if k.startswith("RD-")), "reddit")
