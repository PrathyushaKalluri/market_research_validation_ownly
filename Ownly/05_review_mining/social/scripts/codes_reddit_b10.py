"""Reddit coding batch 10 (AI first pass)."""
import json, os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "codes_reddit_b2.py")).read().split("# ---- RD-1vq18l9")[0])
C("RD-1p6erff", 0, "neutral", "MERCHANT_ONBOARDING_QUESTION", hyp="H10", author="restaurant_owner_or_staff", note="Asks how to use Ownly Merchant app (2025-11-25) — restaurant-side, context only")
X("RD-1p6errn", note="empty post (title only)")
C("RD-1o842dl", 0, "neutral", "COMPETITOR_CONTEXT;TOING_VS_OWNLY", hyp="H2", ev="MEDIA REPORT", author="investor_analyst_media", note="Eternal CEO: Zomato app itself can serve value-seeking users; 'We don't need another app' (2025-10-16)")
C("RD-1o842dl-nl9p5an", 0, "neg", "SUSTAINABILITY_SKEPTICISM;INCUMBENT_FREE_DELIVERY_SUBSCRIPTION", hyp="H2;H8", price="criticises Zomato Gold free delivery on ₹99 orders; predicts Toing and Ownly shut down on losses")
C("RD-1qyeu24", 0, "neutral", "PLANNED_SPEND_SHIFT_FROM_INCUMBENT;CARD_CASHBACK_OPTIMISATION", stage="payment", hyp="H2;H12",
  sw="to_ownly (planned): moving food/grocery spend from Swiggy to FirstClub, Swish and Ownly", note="2026-02-07; asks if a 10% cashback card applies — shows card offers matter in platform choice")
X("RD-1qyeu24-o432xm1", "RD-1qyeu24-oe05ivl", note="credit-card MCC/cashback mechanics; no Ownly experience")
json.dump(codes, open(P, "w"), indent=1, ensure_ascii=False)
print(len(codes), "codes total;", sum(1 for k in codes if k.startswith("RD-")), "reddit")
