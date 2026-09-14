"""Reddit coding batch 7 (AI first pass)."""
import json, os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "codes_reddit_b2.py")).read().split("# ---- RD-1vq18l9")[0])
T = "RD-1vs9ut4"; S = "[SAME_INCIDENT:RD-1vs9ut4] "
C(T, 1, "neg", "MENU_PRICE_INFLATION_ON_OWNLY;SLOGAN_THROWN_BACK;TOING_VS_OWNLY;MARKUP_TOLERANCE_STATED", sev=2, stage="pricing_checkout", hyp="H1;H2;H7",
  price="2 idlis ₹40 in store vs ₹68 on Ownly; would accept ₹50–55; A2B lists 2 idlis at ₹55 on Toing", trust="says Ownly's no-inflation / 'price match' branding is broken",
  note="2026-08-19. Self-reported in-store price (unverified). Stated markup tolerance ≈25–38% over in-store — single user, useful anchor for survey wording")
C(T+"-p4k7qew", 0, "neutral", "RESTAURANT_SETS_PRICES;PRICE_ONLY_USP", hyp="H2", ev="INTERPRETATION", note="'This is their only usp. The app is crap otherwise.'")
for cid in ("p4jp1tw", "p4k6ozg", "p4krvlk"):
    C(T+"-"+cid, 1, "neg", "MENU_PRICE_INFLATION_ON_OWNLY", stage="pricing_checkout", hyp="H2", note="Brief corroboration ('noticed the same') — low information")
C(T+"-p4onxs8", 0, "neutral", "SERVICE_AREA_EXPANSION_OBSERVED;OFFLINE_ALTERNATIVE", stage="discovery_onboarding", hyp="H9", note="Neighbour notes Ownly newly serves their area; suggests visiting the restaurant instead")
C(T+"-p4k4ib5", 0, "neg", "MISLEADING_ADVERTISING_CONCERN;TRANSPARENT_DELIVERY_FEE_PREFERENCE", stage="pricing_checkout", hyp="H2;H7;H8", price="prefers flat per-km delivery rates over claiming restaurant price match")
C(T+"-p4kl9av", 1, "neg", "MENU_PRICE_INFLATION_ON_OWNLY;TRANSPARENT_DELIVERY_FEE_PREFERENCE;RIDER_EARNINGS_CONCERN", stage="pricing_checkout", hyp="H2;H8",
  price="worked example: '95 + 15(delivery) = 110 total For a 57 rs dish'", note="Implies a ₹15 delivery fee on this order (Aug 2026) — conflicts with 'free' and '₹30 flat' reports; unverified")
C(T+"-p4kvnxv", 0, "neg", "HIDDEN_COMMISSION_IN_MENU_PRICE;TRANSPARENT_DELIVERY_FEE_PREFERENCE;SLOGAN_THROWN_BACK", stage="pricing_checkout", hyp="H1;H2",
  price="wants platform costs shown as fees rather than hidden in food price — 'That's the hidden charge which is what Ownly claimed to remove'")
C(T+"-p4ll7gi", 1, "neutral", "PRICE_MATCH_CLAIM_VIOLATED;MARKUP_TOLERANCE_STATED", stage="pricing_checkout", hyp="H2;H7", price="would pay ₹75 for 2 idlis; ₹68 'far cheaper than few other restaurants'; objects to 'price match' promotion; packaging folded into item price; GST separate", note=S)
C(T+"-p4qrquq", 0, "neutral", "RIDER_EARNINGS_CONCERN;SUSTAINABILITY_SKEPTICISM", hyp="H8;H9", note="Questions ₹30 for 4–5 km / 40 min")
C(T+"-p4rh94j", 1, "neutral", "MISLEADING_ADVERTISING_CONCERN;TRANSPARENT_DELIVERY_FEE_PREFERENCE", hyp="H7;H8", note=S+"'charge a reasonable amount for packing and delivery but they should not be added to the product cost'")
C(T+"-p4s1lnl", 0, "neutral", "COST_OF_CONVENIENCE_ACCEPTED", hyp="H1", note="Compares app costs with petrol/time of going out")
C(T+"-p4t7kxq", 0, "neutral", "TRANSPARENT_DELIVERY_FEE_PREFERENCE", hyp="H2")
C(T+"-p4t8cid", 0, "neutral", "ANCHORING_DISCOUNT_PREFERENCE;RESTAURANT_SETS_PRICES", hyp="H2", ev="INTERPRETATION",
  note="Claims Indian buyers prefer '₹1000 with 20% off' over a straight ₹800 — a discount-framing hypothesis worth testing in the bill-comparison experiment")
C(T+"-p5est5i", 0, "neutral", "FEE_MODEL_DESCRIPTION", hyp="H8", ev="INTERPRETATION", note="Flat monthly restaurant subscription (belief)")
C(T+"-p5et377", 0, "neutral", "FREE_DELIVERY_PERCEPTION;NO_HIDDEN_FEES_POSITIVE", stage="pricing_checkout", hyp="H8", note="'no platform fee/ packing charge/ delivery fee' — conflicts with p4kl9av's ₹15 delivery")
C(T+"-p75exe7", 1, "neg", "WTP_FOR_RELIABILITY;NON_DELIVERY;SUPPORT_UNRESPONSIVE", sev=4, stage="post_order_support_refund", hyp="H4;H8;H12",
  sw="away_from_ownly: 'willing to pay extra if I can get faster resolution'", support="'customer support is horrible'",
  note="[SAME_INCIDENT:RD-1vw5429-p75fa7u] same minute, same complaint in another thread; kept for the added WTP statement, counted once")
X(T+"-p4kuk6x", T+"-p4luwns")
json.dump(codes, open(P, "w"), indent=1, ensure_ascii=False)
print(len(codes), "codes total;", sum(1 for k in codes if k.startswith("RD-")), "reddit")
