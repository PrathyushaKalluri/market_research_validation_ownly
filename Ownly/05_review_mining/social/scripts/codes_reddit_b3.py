"""Reddit coding batch 3 (AI first pass)."""
import json, os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "codes_reddit_b2.py")).read().split("# ---- RD-1vq18l9")[0])
T = "RD-1v8r1w7"
C(T, 0, "neutral", "LAUNCH_CLAIM_RELAY;RAPIDO_APP_INTEGRATION", hyp="H7", ev="MEDIA REPORT", author="investor_analyst_media", note="News-relay subreddit post (2026-07-28): Ownly integrated into main Rapido app in Bengaluru")
T = "RD-1nclzlx"
X(T, note="verbatim cross-post of RD-1nclyuy (same author, same text) — excluded from counts")
X(T+"-ndcbc4d", note="survey/research solicitation by an academic researcher; no Ownly experience")
C(T+"-nddnreu", 0, "neutral", "PRICE_AS_SWITCH_TRIGGER;MULTI_HOMING_PRICE_COMPARISON", hyp="H1;H2", sw="to_ownly (conditional): 'Pricing is a big factor for a switch!'", note="Uses both Swiggy and Zomato")
C(T+"-ntzggfd", 1, "neg", "RESTAURANT_CAPTURES_SAVINGS;NO_DISCOUNTS_ON_OWNLY;INCUMBENT_CHEAPER_AFTER_OFFERS", sev=2, stage="pricing_checkout", hyp="H2",
  sw="away_from_ownly: same menu prices as incumbents but no discounts — 'Completely useless'",
  price="restaurants list 'almost the same exorbitant prices' as Swiggy/Zomato, which then discount; Ownly doesn't", note="Dec 2025. Mechanism: zero commission benefits restaurant margin, not customer price")
C(T+"-nzb4quo", 0, "neg", "RESTAURANT_CAPTURES_SAVINGS", stage="pricing_checkout", hyp="H2", price="'No point of flat fee if restaurants prices are same as on other platforms'")
X(T+"-o6kcxtm", note="third cross-post of RD-1qcrc1f-o6kcml5; author states they 'commented on other posts as well' — confirms de-duplication; excluded from counts")
json.dump(codes, open(P, "w"), indent=1, ensure_ascii=False)
print(len(codes), "codes total;", sum(1 for k in codes if k.startswith("RD-")), "reddit")
