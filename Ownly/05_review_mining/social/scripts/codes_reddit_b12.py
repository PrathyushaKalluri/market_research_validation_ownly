"""Reddit coding batch 12 (AI first pass)."""
import json, os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "codes_reddit_b2.py")).read().split("# ---- RD-1vq18l9")[0])
# RD-1vn73gn
T = "RD-1vn73gn"
C(T, 1, "pos", "USER_BILL_COMPARISON;PRICE_SAVINGS_OBSERVED;FULL_SWITCH_TO_OWNLY", stage="pricing_checkout", hyp="H2;H12",
  sw="to_ownly: 'switching to Ownly and delete Swiggy'", price="same restaurant, same food: Swiggy ₹367; dish price alone ₹100 higher on Swiggy", note="2026-08-13")
C(T+"-p3idt64", 0, "neg", "FUTURE_FEE_CREEP_EXPECTED", hyp="H2")
X(T+"-p3f1ux7", note="automoderator")
# RD-1w6qgm0
T = "RD-1w6qgm0"; S = "[SAME_INCIDENT:RD-1w6qgm0] "
C(T, 1, "neg", "SUPPORT_UNRESPONSIVE;RESTAURANT_PLATFORM_BLAME_LOOP", sev=3, stage="post_order_support_refund", hyp="H4;H12",
  support="restaurant manager said no complaint was received from the app", note="2026-09-04 (r/Ownly); support screenshot not retrievable")
C(T+"-p7p24l5", 0, "neg", "REFUND_POLICY_RESTRICTIVE", stage="post_order_support_refund", hyp="H4", note="Claims users get banned from refunds after a few — unverified")
C(T+"-p7p2neh", 1, "neutral", "COMPENSATION_PARTIAL_OFFERED", sev=3, stage="post_order_support_refund", hyp="H4", note=S+"was offered half the money earlier")
# RD-1sko63h — r/Ownly is merchant-run
C("RD-1sko63h", 0, "neutral", "MERCHANT_ISSUES_COMMUNITY", hyp="H10", author="restaurant_owner_or_staff", note="r/Ownly created by a cloud-kitchen co-owner 'to understand Ownly more closely and resolve the issues we're facing' (2026-04-13) — unofficial")
C("RD-1sko63h-ougezcb", 0, "neutral", "FEE_TRANSPARENCY_QUESTION", hyp="H8", note="Asks for breakdown of (restaurant) charges")
# RD-1vo68qd — cloud kitchen owner promo
T = "RD-1vo68qd"
C(T, 0, "pos", "RESTAURANT_MULTI_PLATFORM_LISTING", hyp="H10", author="restaurant_owner_or_staff", city="Bengaluru", note="Cloud kitchen (C.V. Raman Nagar) lists on Ownly, Swiggy and Zomato; promo post 2026-08-14")
C(T+"-p3nf2wm", 0, "pos", "RESTAURANT_PRICES_LOWER_ON_OWNLY", stage="pricing_checkout", hyp="H2", ev="COMPANY CLAIM", author="restaurant_owner_or_staff",
  price="'We have kept our prices there much much lower than Swiggy/ Zomato'", note="Seller's own claim (labelled COMPANY CLAIM = seller claim); shows lower Ownly price is a restaurant choice, not guaranteed")
C(T+"-p3te3tx", 0, "neutral", "SERVICE_RADIUS_LIMIT;NUTRITION_INFO_REQUEST", stage="browse_menu", hyp="H10", note="~15 km away — too far")
C(T+"-p3n4vfh", 0, "neutral", "SERVICE_RADIUS_LIMIT", stage="browse_menu", hyp="H10", note="'Very far from my pg' — PG resident wants a nearer branch")
C(T+"-p3o0k5t", 0, "neutral", "RESTAURANT_MULTI_PLATFORM_LISTING", hyp="H10", author="restaurant_owner_or_staff")
X(T+"-p3n6ayi",T+"-p3nehoo",T+"-p3n0ofo",T+"-p3n195p",T+"-p3n1wpf",T+"-p3nepw8",T+"-p3nza09",T+"-p3ta77h",T+"-p3tfing",T+"-p3n46xb",T+"-p3ndy01",T+"-p3nedqc",T+"-p3na67e",T+"-p3nf732",T+"-p3na6r4",T+"-p3nefvh",T+"-p3s8d6p",T+"-p3nk182",T+"-p3o0m9s",T+"-p3o8m8n",T+"-p3ozsuv",T+"-p3p14q5",T+"-p3pmoah",T+"-p3rzctf", note="well-wishes / menu questions / order confirmations without platform — no Ownly content")
# RD-1vu5s4x — 'Finally moved away from Swiggy'
T = "RD-1vu5s4x"
C(T, 1, "pos", "USER_BILL_COMPARISON;PRICE_SAVINGS_OBSERVED;FULL_SWITCH_TO_OWNLY;SUBSCRIPTION_NOT_ENOUGH", stage="pricing_checkout", hyp="H2;H12",
  sw="to_ownly: 'Finally moved away from Swiggy'", price="'Even with the Swiggy Card discount + Swiggy One it still is off by ~120-150 rupees'", note="2026-08-21; screenshots not retrievable")
C(T+"-p4zcoce", 0, "neg", "FUTURE_FEE_CREEP_EXPECTED", hyp="H2")
C(T+"-p4zgxnr", 0, "neutral", "LOW_PLATFORM_LOYALTY", hyp="H12", note="Will switch again when Ownly raises prices")
C(T+"-p52p0z4", 1, "neg", "PRICE_PARITY_OBSERVED;LOCATION_DEPENDENT_PRICING", stage="pricing_checkout", hyp="H2", price="'In our area, already most shops have same price between Swiggy and Ownly'")
C(T+"-p599njy", 0, "pos", "RAPIDO_BRAND_POSITIVE_SPILLOVER", hyp="H7", trust="'rapido seems to do ok without excessive charges'")
C(T+"-p59d8y8", 0, "neutral", "REGULATORY_RISK_BIKE_TAXI", hyp="H9", note="Bike-taxi bans / gig-worker pay as risk to rider supply")
C(T+"-p5rnqx2", 0, "neutral", "LOW_PLATFORM_LOYALTY", hyp="H12", note="'Just keep switching… some new startup will keep coming to remove stupid fees for 18 months'")
C(T+"-p62k7j9", 0, "neutral", "FEE_MODEL_DESCRIPTION", hyp="H8", ev="INTERPRETATION")
C(T+"-p4zcdy4", 0, "neutral", "OWNLY_SUBSCRIPTION_QUESTION", hyp="H8")
C(T+"-p4zgv23", 1, "neutral", "NO_OWNLY_SUBSCRIPTION", hyp="H8", note="New user (Aug 2026): no Ownly subscription exists")
C(T+"-p56mt6x", 0, "neutral", "NO_OWNLY_SUBSCRIPTION", hyp="H8")
C(T+"-p66sylu", 0, "neutral", "SUBSCRIPTION_ACCEPTABLE", hyp="H8", price="suggests ₹200/month subscription instead of per-order fees", note="Single suggested WTP anchor for a subscription")
for cid in ("p4zhy2t","p56qlri","p57cjho","p59elnn"):
    C(T+"-"+cid, 0, "neutral", "TOING_VS_OWNLY", hyp="H2", note="Toing and Ownly UI/prices similar; Toing owned by Swiggy")
C(T+"-p59rwj3", 0, "pos", "TOING_VS_OWNLY;GENERAL_SUPPORT_FOR_OWNLY", hyp="H2;H7", note="Will avoid Swiggy/Toing while Ownly 'stays reasonable'")
C(T+"-p5348vu", 0, "neg", "TOING_VS_OWNLY;COMPETITOR_FEE_CREEP_OBSERVED", hyp="H2", note="'Swiggy started toing with same narrative but eventually the prices turned out to be same'")
for cid,city in (("p4zetnp",None),("p4zip4j",None),("p50f6sz","Bengaluru"),("p50tn37","Mumbai"),("p559zyo","Delhi"),("p5d1v3x","Mumbai"),("p5kse45",None),("p5l01ge",None),("p5mggao","Delhi"),("p5rh1mv","tier-2 city")):
    C(T+"-"+cid, 0, "neutral", "CITY_AVAILABILITY_QUESTION", stage="discovery_onboarding", hyp="H9", city=city)
C(T+"-p50728x", 0, "neutral", "CITY_AVAILABILITY_QUESTION;HYDERABAD_NOT_YET_AVAILABLE", stage="discovery_onboarding", hyp="H9", city="Hyderabad", note="2026-08-21: 'Not available in Hyderabad!' — dates Hyderabad launch after this")
C(T+"-p5j6tvy", 0, "pos", "HYDERABAD_DEMAND_SIGNAL;INCUMBENT_FATIGUE", stage="discovery_onboarding", hyp="H1;H9", city="Hyderabad", note="2026-08-24: 'Can't wait for it to come to Hyderabad. Tired of zomato monopoly' — only Hyderabad consumer-demand item found")
C(T+"-p5kk204", 0, "neutral", "RAPIDO_ECOSYSTEM_ADVANTAGE;EXPANSION_SPECULATION", hyp="H9", ev="INTERPRETATION", city="Hyderabad", note="Speculates scale-up to Hyderabad/Pune, not Mumbai; riders already multi-app")
for cid in ("p55t75p","p68mmmf","p4zzboz","p5uvs0c","p68pcfe"):
    C(T+"-"+cid, 0, "neg", "FUTURE_FEE_CREEP_EXPECTED", hyp="H2")
for cid in ("p5eu5j6","p5832p9"):
    C(T+"-"+cid, 0, "pos", "SWITCH_DESPITE_TEMPORARY_PRICING", hyp="H12")
C(T+"-p4zlg8f", 1, "neutral", "PRICE_PARITY_OBSERVED;INCUMBENT_CHEAPER_AFTER_OFFERS", stage="pricing_checkout", hyp="H2", price="after discount Zomato was ₹0.41 cheaper than Ownly — effectively parity")
C(T+"-p4zjvh9", 0, "neg", "INCUMBENT_DISTRUST", hyp="H1")
for cid in ("p503hbv","p56v4n0","p5qt6op"):
    C(T+"-"+cid, 0, "neutral", "COST_OF_CONVENIENCE_ACCEPTED", hyp="H1")
C(T+"-p4zqore", 0, "neutral", "MEAL_CARD_PAYMENT_GAP", stage="payment", hyp="H6;H9", sw="to_ownly (conditional): 'implement pluxee card payment then I would order'", note="Conditional trial barrier for salaried users with meal cards")
C(T+"-p506sie", 0, "pos", "GENERAL_SUPPORT_FOR_OWNLY", hyp="H7")
C(T+"-p50b7qt", 1, "mixed", "NON_DELIVERY;LATE_DELIVERY;SUPPORT_RECOVERY_POSITIVE", sev=2, stage="delivery_handoff", hyp="H4", support="'customer support was responsive and refunded'", note="Marked delivered mid-way after 1 h wait (biryani)")
C(T+"-p552cl0", 1, "pos", "SUPPORT_RECOVERY_POSITIVE;ORDER_CONCURRENCY_TIP", stage="post_order_support_refund", hyp="H4", support="support calls on cancellation; full refund initiated immediately")
C(T+"-p55fh79", 0, "neutral", "INCUMBENT_CHEAPER_CONDITIONAL", stage="pricing_checkout", hyp="H2", note="Splitting orders with 60% off might make Swiggy cheaper")
C(T+"-p55u3l2", 1, "neg", "ORDER_BATCHING_STALE_FOOD;LATE_DELIVERY;FOOD_QUALITY", sev=3, stage="dispatch_eta", hyp="H3;H4", eta="rider picks '4-5 orders at once' and roams; delivered after ~1 hour; stale food",
  note="Mechanism hypothesis linking low delivery cost to batching and slower, colder delivery (single user)")
C(T+"-p56gury", 0, "neg", "SUPPORT_UNRESPONSIVE;TOING_VS_OWNLY", hyp="H4", note="'Cs sucks. Toing is better'")
C(T+"-p58hft8", 0, "neutral", "INCUMBENT_FOOD_SAFETY_INCIDENT;HOME_COOKING_ALTERNATIVE", hyp="H1", note="Stopped Swiggy/Zomato after a cockroach; cooks at home")
for cid in ("p58m0ut","p5rq0k4"):
    C(T+"-"+cid, 0, "neutral", "ASTROTURF_SUSPICION", hyp="H7")
C(T+"-p59xrhk", 1, "pos", "PRICE_SAVINGS_OBSERVED", stage="pricing_checkout", hyp="H2", note="'I noticed this too. Ownly is amazing as of now.'")
C(T+"-p5gszsr", 1, "mixed", "PRICE_CREEP_AFTER_REPEAT_ORDERS;PRICE_SAVINGS_OBSERVED", stage="pricing_checkout", hyp="H2;H12", rep=1,
  price="after a week of use, item prices appeared to rise 'after repeated orders' (Ownly or restaurants); still 'far better than paying Rain GST on tomato'", note="Perceived, unverified; worth tracking in the repeated-audit design")
C(T+"-p5rr6ja", 0, "neutral", "COMPETITOR_ALTERNATIVE_SUGGESTED;TOING_VS_OWNLY", hyp="H2", note="Suggests Toing or Directoo (any nearby rider)")
C(T+"-p5y9bly", 0, "neutral", "AGGREGATOR_MARKUP_WORKAROUND", hyp="H1", note="Call restaurant / send Porter")
C(T+"-p62n7n5", 0, "neutral", "AGGREGATOR_MARKUP_WORKAROUND", hyp="H1", note="Orders by phone and picks up")
C(T+"-p6a3nog", 0, "neg", "INCUMBENT_SUPPORT_BAD;INCUMBENT_CHURN_AFTER_SUPPORT_FAILURE", stage="post_order_support_refund", hyp="H1;H4", note="Stopped using Swiggy after an unresolved missing/wrong-item complaint — incumbents also lose users on support")
C(T+"-p4zg9sb", 0, "neutral", "SUSTAINABILITY_SKEPTICISM;MERCHANT_WANTS_OWNLY", hyp="H9;H10", author="restaurant_owner_or_staff", city="Mumbai", note="Cloud-kitchen owner in Mumbai keen for Ownly to arrive, doubts durability")
C(T+"-p4zgrk2", 0, "neutral", "LOW_PLATFORM_LOYALTY", hyp="H12")
C(T+"-p4zh3u5", 0, "neutral", "SUSTAINABILITY_SKEPTICISM", hyp="H2", note="Expects ad monetisation later")
C(T+"-p4zxw8p", 0, "neutral", "FEE_MODEL_DESCRIPTION", hyp="H8", ev="INTERPRETATION")
C(T+"-p581m04", 0, "neutral", "DELIVERY_PRICE_LEVEL_TOO_HIGH", hyp="H1", price="₹115 coffee vs ₹25 at a tapri; ₹60 dosa outlet — '3-5x' via delivery")
C(T+"-p5jqx54", 0, "neg", "DELIVERY_PRICE_LEVEL_TOO_HIGH", hyp="H1", price="'125 for dosa is insane'")
X(T+"-p4ymflh", note="automoderator")
X(T+"-p59e7rt",T+"-p5aaqp0",T+"-p5rt5cs",T+"-p5vhb5w",T+"-p5ru0h0",T+"-p5qo3yp",T+"-p5utc9o",T+"-p5v6now",T+"-p5sq0oj",T+"-p6a8xub",T+"-p4zh71k",T+"-p4zigp7",T+"-p4zij4m",T+"-p5y65y9",T+"-p603566",T+"-p675id2",T+"-p5fz8da", note="side debate (bike-taxi bans, dosa/curry, Toing ownership correction) / banter")
# RD-1k2w5wi — living-alone expenses (pre-Ownly; Rapido as transport)
C("RD-1k2w5wi", 0, "neutral", "DAILY_FOOD_BUDGET_ANCHOR", hyp="H1;H6", city="Bengaluru", note="2025-04-19, 22-year-old living in shared house: food ~₹8,000/month (₹65 + ₹100 + ₹100/day); Rapido used for transport, not food — context for young-professional budgets, not Ownly evidence")
C("RD-1k2w5wi-moeofj8", 0, "neutral", "DAILY_FOOD_BUDGET_ANCHOR", hyp="H6", city="Chennai", note="24-year-old IT worker: food ₹8–10k/month; Rapido as transport")
json.dump(codes, open(P, "w"), indent=1, ensure_ascii=False)
print(len(codes), "codes total;", sum(1 for k in codes if k.startswith("RD-")), "reddit")
