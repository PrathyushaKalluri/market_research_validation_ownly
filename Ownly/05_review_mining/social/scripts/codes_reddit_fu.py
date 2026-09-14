"""Reddit coding — follow-up pass threads (AI first pass)."""
import json, os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "codes_reddit_b2.py")).read().split("# ---- RD-1vq18l9")[0])
C("RD-1w9qa1f", 0, "pos", "REFERRAL_OFFER_OBSERVED;LAUNCH_PROMOTION_OBSERVED;PROPOSITION_RECALL_NO_HIDDEN_COSTS", stage="pricing_checkout", hyp="H2;H12",
  price="referral copy: 'get upto ₹100 off on your first order'; 'No surge fee. No platform fee. No packaging charges.'",
  note="2026-09-07 referral-code post (poster benefits from referrals) — evidence of current acquisition offer and messaging, NOT an organic review")
X("RD-1w9qa1f-p8c5ytu", note="subreddit bot safety notice")
C("RD-1w0k0bk", 0, "neg", "RESTAURANT_PUSHBACK_OFFLINE_PRICE_MATCHING;COMPETITOR_CONTEXT;TOING_VS_OWNLY", hyp="H9;H10", author="restaurant_owner_or_staff",
  note="r/hyderabad, 2026-08-28: restaurant owner says Swiggy Toing cut its listed prices 'drastically without consent', disputes Toing's 'offline prices', cannot delist. About Toing, not Ownly — but shows Hyderabad supply-side friction for offline-price-matching models. City from subreddit context (not stated in text)")
json.dump(codes, open(P, "w"), indent=1, ensure_ascii=False)
print(len(codes), "codes total;", sum(1 for k in codes if k.startswith("RD-")), "reddit")
