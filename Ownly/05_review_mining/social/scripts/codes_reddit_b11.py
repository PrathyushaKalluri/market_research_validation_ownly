"""Reddit coding batch 11 (AI first pass)."""
import json, os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "codes_reddit_b2.py")).read().split("# ---- RD-1vq18l9")[0])
# RD-1q7cvbt / RD-1q7cvyi — restaurant subscription question
C("RD-1q7cvbt", 0, "neutral", "FEE_MODEL_DESCRIPTION", hyp="H9", note="Asks whether Ownly's restaurant subscription model works (2026-01-08)")
C("RD-1q7cvbt-nyejjaz", 0, "neutral", "CITY_AVAILABILITY_QUESTION", hyp="H9", city="West Bengal", note="Replies to a customer comment not present in RSS")
X("RD-1q7cvyi", note="cross-post of RD-1q7cvbt")
# RD-1rme2x8 — electronic_city first-order cancellations
T = "RD-1rme2x8"; S = "[SAME_INCIDENT:RD-1rme2x8] "
C(T, 1, "neg", "PLATFORM_RESTAURANT_CANCELLATION;SUPPORT_UNRESPONSIVE;FIRST_ORDER_FAILURE", sev=3, stage="dispatch_eta", hyp="H4;H12", city="Bengaluru",
  sw="away_from_ownly (first-time user): two consecutive cancellations", support="support told user to reorder; second order also cancelled", note="2026-03-06, Electronic City, launch week")
C(T+"-o925ag6", 1, "neg", "LISTING_MENU_ACCURACY;PLATFORM_RESTAURANT_CANCELLATION", sev=3, stage="browse_menu", hyp="H4;H10", note="Advises checking the restaurant is open on Swiggy — Ownly shows restaurants not accepting orders")
C(T+"-o92gcb5", 1, "neutral", "SMALL_CART_CANCELLATION_SUSPECTED", stage="dispatch_eta", hyp="H8", note=S+"restaurant 300 m away and open; suspects small-cart cancellation")
X(T+"-ocrqm4d", note="same author as RD-1qcrc1f-ocrqfj6 (same day, cross-posted churn statement) — excluded")
X(T+"-oo7wae1", note="verbatim duplicate of RD-1qcrc1f-oo7vwmt — excluded")
C(T+"-oo7yi8v", 0, "neutral", "SMALL_CART_CANCELLATION_SUSPECTED", hyp="H8", note="Says restaurants sometimes cancel orders under ₹150 — tension with low-AOV value proposition")
C(T+"-o8yoszw", 0, "neg", "TRIAL_DETERRED_BY_NEGATIVE_POSTS", stage="discovery_onboarding", hyp="H7;H12", note="'not gonna use it then' — prospective user deterred by others' failures")
X(T+"-o8z08hs", T+"-o92gh0x", T+"-o96xcot", note="dish-ingredient (veg/non-veg kuska) side discussion")
# RD-1u4t85s — forced rating
T = "RD-1u4t85s"
C(T, 1, "neg", "FORCED_RATING_UX", sev=2, stage="app_account", hyp="H12", rep=1, note="Cannot skip restaurant-rating screen; 2–3 orders 'worked fine'")
C(T+"-orfgiva", 0, "neg", "CHURN_ADVOCACY", hyp="H12")
C(T+"-owaosy0", 1, "pos", "PRICE_SAVINGS_OBSERVED;NO_HIDDEN_FEES_POSITIVE;WELCOME_THIRD_COMPETITOR", stage="pricing_checkout", hyp="H1;H2", note="[SAME_INCIDENT:RD-1qcrc1f-owap5ff] same minute and wording — counted once")
C(T+"-orgbeey", 1, "mixed", "FORCED_RATING_UX;RELIABLE_EXPERIENCE_POSITIVE;COMPETITOR_CONTEXT", sev=1, stage="app_account", hyp="H4;H12", note="'it works and not the dump that magic pin has now become'")
C(T+"-orqjidr", 1, "pos", "TRADEOFF_ACCEPTED;FEE_LEVEL_OBSERVED", stage="pricing_checkout", hyp="H8", price="'no additional fees (minimal fees like +5 rupees)'", note="Jun 2026 fee observation (+₹5) — unverified")
X(T+"-orfo76h")
# RD-1v0w2lx — FIFA offer
C("RD-1v0w2lx", 1, "neutral", "PROMO_ORDER_CANCELLED;LAUNCH_PROMOTION_OBSERVED", sev=2, stage="dispatch_eta", hyp="H2;H12", price="'FIFA offer' — bunch of items for ₹60; order cancelled", note="2026-07-19: evidence Ownly runs deep promotional offers (not only everyday pricing)")
# RD-1vkoo9i — r/Zomato reaction to Ownly 'trolling' ad
T = "RD-1vkoo9i"
C(T, 0, "neutral", "COMPANY_MARKETING_OBSERVED", hyp="H7", note="Image of an Ownly ad mocking competitors' fees (2026-08-10); image not retrievable")
for cid in ("p2v20cd","p35yh8q","p2vs9q2","p2zbnhg","p3ea3bq","p383wbr"):
    C(T+"-"+cid, 0, "neg", "SUSTAINABILITY_SKEPTICISM", hyp="H2")
for cid in ("p2v9oav","p2uyvyq","p36mkdo","p2vuq0z","p2z31qu","p2zhwu3","p2zj0iu","p2znga2","p35szbv","p35tssl","p36gipd","p36zfqf","p3ei8be"):
    C(T+"-"+cid, 0, "neg", "FUTURE_FEE_CREEP_EXPECTED", hyp="H2;H7")
for cid in ("p2veri2","p2vokxj","p2w2k6a","p2yyt00","p30nt1y","p2vx5b9","p38j20x"):
    C(T+"-"+cid, 0, "neutral", "HISTORICAL_PRICE_CONVERGENCE", hyp="H1;H2", note="Nostalgia for early Zomato/Swiggy/Uber Eats/Foodpanda discounts that later disappeared")
C(T+"-p2vy6iu", 0, "neutral", "HISTORICAL_PRICE_CONVERGENCE;DISCOUNT_DRIVEN_ORDERING", hyp="H1;H6", note="As interns renting, survived on 50%-off Zomato ('cooking would probably cost more') — price anchor for young renters")
C(T+"-p2zasin", 0, "neutral", "DISCOUNT_DRIVEN_ORDERING", hyp="H6", note="Whole class ordered when discounts appeared (student context)")
C(T+"-p386za1", 0, "pos", "GENERAL_SUPPORT_FOR_OWNLY", hyp="H7", note="Hinglish: critics complain whether Ownly gives benefits or charges fees")
C(T+"-p2uvrz2", 0, "neutral", "CITY_AVAILABILITY_QUESTION", hyp="H9", city="Bengaluru")
C(T+"-p2vs813", 1, "neutral", "CITY_AVAILABILITY_QUESTION", hyp="H9", note="'I just now ordered fried rice' — availability confirmation")
C(T+"-p2w6262", 0, "pos", "WELCOME_THIRD_COMPETITOR", hyp="H1")
C(T+"-p32sokv", 0, "neutral", "TRANSPARENT_DELIVERY_FEE_PREFERENCE;INCUMBENT_FEE_STACK_FRUSTRATION", stage="pricing_checkout", hyp="H1;H8", price="prefers higher delivery fee over 'utter nonsense' platform fee")
C(T+"-p2vhimd", 0, "neutral", "TOING_VS_OWNLY;COMPETITOR_FEE_CREEP_OBSERVED", stage="pricing_checkout", hyp="H2;H8", price="Toing advertised no delivery fee; now charged on every order", note="First-hand Toing use — incumbent value app already added fees")
C(T+"-p2vxpig", 0, "neutral", "TOING_VS_OWNLY", stage="pricing_checkout", hyp="H2", note="Toing gave ₹50 off for a screenshot of a cheaper cart elsewhere")
C(T+"-p2vz8sq", 0, "neg", "TOING_VS_OWNLY;FUTURE_FEE_CREEP_EXPECTED", hyp="H2")
C(T+"-p2w9pjy", 0, "neutral", "INCUMBENT_MARGIN_BELIEF", hyp="H1")
C(T+"-p2v5nmx", 0, "neutral", "TRIAL_CURIOSITY", hyp="H12")
C(T+"-p2v7q1a", 0, "neutral", "MULTI_HOMING_PRICE_COMPARISON;FUTURE_FEE_CREEP_EXPECTED", stage="pricing_checkout", hyp="H1;H12", price="Swiggy added platform+packaging fees; ordered on Zomato and saved ₹42; frequent orderer counts monthly savings")
C(T+"-p2wtl39", 0, "neutral", "LAUNCH_DISCOUNT_TEMPORARY", stage="pricing_checkout", hyp="H2", note="Claims advertised benefit 'Only applicable on first order' — unverified")
C(T+"-p2yropj", 0, "pos", "STAY_TRANSPARENT_DEMAND;SUBSCRIPTION_ACCEPTABLE;TRANSPARENT_DELIVERY_FEE_PREFERENCE", hyp="H2;H8",
  price="would accept subscriptions for frequent users; rejects inflate-then-discount offers", note="States the conditions under which future monetisation would be acceptable")
C(T+"-p2yvz60", 1, "neg", "OWNLY_FEES_OBSERVED", sev=2, stage="pricing_checkout", hyp="H2;H8", price="'charged me gst and platform fee...abt 40 rs extra'", note="Reply under the Ownly ad; platform not named explicitly — AMBIGUOUS")
C(T+"-p2zsfyq", 1, "neg", "PORTION_SMALLER_THAN_EXPECTED", sev=2, stage="food_quality_accuracy", hyp="H4", note="Smaller portion from a burrito chain")
C(T+"-p2zzs8n", 1, "neg", "PAYMENT_DEDUCTED_ORDER_FAILED;TRUST_LOSS_SCAM_FRAMING", sev=3, stage="payment", hyp="H4;H7")
C(T+"-p302tfa", 0, "neg", "SUBSCRIPTION_STILL_FEES;INCUMBENT_FEE_STACK_FRUSTRATION", stage="pricing_checkout", hyp="H1", note="Zomato Gold member still charged platform fee")
C(T+"-p308quz", 1, "neg", "INCUMBENT_CHEAPER_AFTER_OFFERS", stage="pricing_checkout", hyp="H2", price="'Zomato still ends up cheaper than ownly'")
C(T+"-p30cdmr", 1, "neg", "OWNLY_PRICIER_OBSERVED;TOING_VS_OWNLY", stage="pricing_checkout", hyp="H2", price="Ownly prices above restaurant prices at 'a few specific places'; 'Toing is actually the only legit one'")
C(T+"-p310aq0", 0, "neutral", "FEES_VARY_BY_CITY_BELIEF", hyp="H9", note="'This might vary from city to city' — platform ambiguous")
C(T+"-p31xtqr", 1, "pos", "CLEAN_APP_NO_UPSELL", hyp="H12", note="'Love the UI; very minimal' (contrast with 'slow and glitchy' reports)")
C(T+"-p33kcgv", 0, "neg", "OWNLY_FEES_OBSERVED", stage="pricing_checkout", hyp="H2;H8", note="'They do have platform fee & restaurant packaging fees' — platform AMBIGUOUS")
C(T+"-p33nevq", 0, "neutral", "CITY_AVAILABILITY_QUESTION", hyp="H9", city="Delhi")
C(T+"-p36jp7u", 0, "pos", "SWITCH_DESPITE_TEMPORARY_PRICING", hyp="H12")
C(T+"-p36kc9g", 0, "neutral", "TRANSPARENT_DELIVERY_FEE_PREFERENCE;SUSTAINABILITY_SKEPTICISM", stage="pricing_checkout", hyp="H2;H8",
  price="'I'd much rather see a flat platform fee that is clearly labelled'")
C(T+"-p37z1cu", 0, "neg", "RAPIDO_BRAND_NEGATIVE_SPILLOVER;FUTURE_FEE_CREEP_EXPECTED", hyp="H7",
  trust="expects Rapido playbook: raise prices slowly, tipping, pay more to get a delivery partner assigned")
C(T+"-p3913em", 0, "pos", "GENERAL_SUPPORT_FOR_OWNLY", hyp="H7")
C(T+"-p3aaig4", 0, "neg", "SWIGGY_OWNERSHIP_ASSOCIATION;FUTURE_FEE_CREEP_EXPECTED", hyp="H7", note="Hinglish: 'it's Swiggy's child after all' — associates Ownly/Rapido with Swiggy's (former) stake")
C(T+"-p3l6wvy", 0, "neutral", "LOW_AWARENESS", hyp="H7", note="'What platform is this?'")
X(T+"-p2wdkae", T+"-p2wo951", T+"-p2woj77", T+"-p2ws5dj", T+"-p2vuuiw", T+"-p330oms", T+"-p33pfcw", T+"-p33u7ba", T+"-p376jva", T+"-p3es98p", T+"-p303vba", note="wordplay/meme/image-only/one-line nostalgia")
json.dump(codes, open(P, "w"), indent=1, ensure_ascii=False)
print(len(codes), "codes total;", sum(1 for k in codes if k.startswith("RD-")), "reddit")
