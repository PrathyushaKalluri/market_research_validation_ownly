"""Reddit coding batch 4 (AI first pass)."""
import json, os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "codes_reddit_b2.py")).read().split("# ---- RD-1vq18l9")[0])
T = "RD-1vw5429"
C(T, 1, "neg", "RELIABILITY_OVER_PRICE;RIDER_CONDUCT;NON_DELIVERY;REFUND_ISSUE", sev=3, stage="delivery_handoff", hyp="H4;H12",
  sw="away_from_ownly: 'They can't compete on reliability with swiggy and zomato. The lower price is not worth it'",
  support="refund fight 'painful'; refund initiated but 7 days", trust="rider took order from restaurant and left",
  note="2026-08-23. Clearest explicit reliability-over-price judgement in dataset (H4)")
C(T+"-p5e3vp2", 1, "pos", "FULL_SWITCH_TO_OWNLY", hyp="H12", rep=1, sw="to_ownly: 'i use only ownly and it's good for what it serves'")
C(T+"-p5e3mm2", 0, "neutral", "BRAND_ASSOCIATION_QUESTION", stage="discovery_onboarding", hyp="H7", note="Asks whether it's the Rapido app — Rapido link used as identifier")
C(T+"-p5e3vcm", 0, "neutral", "PROPOSITION_RECALL_NO_HIDDEN_COSTS", stage="discovery_onboarding", hyp="H7", note="Identifies Ownly by its 'no hidden costs' claim — proposition recall (possibly sarcastic)")
C(T+"-p5e5kxh", 1, "pos", "INCUMBENT_SAME_PROBLEMS;RELIABLE_EXPERIENCE_POSITIVE", hyp="H4;H12", rep=1, note="'Ordered plenty of times but no issues so far'; rider-ran-away happened once on Swiggy")
C(T+"-p5ed620", 1, "mixed", "OPERATIONS_UNDERSTAFFED;INCUMBENT_FEE_DISTRUST", sev=2, hyp="H1;H4", ev="CONSUMER-GENERATED",
  trust="attributes failures to lean ops team; says incumbents 'loot us with all fake charges'", note="Bad experience unspecified; cause is commenter's interpretation")
C(T+"-p75fa7u", 1, "neg", "NON_DELIVERY;SUPPORT_UNRESPONSIVE", sev=4, stage="post_order_support_refund", hyp="H4;H12", support="support closed chat without resolution (screenshots claimed)", note="2026-09-01; marked delivered, not received")
C(T+"-p7gdp5b", 0, "neutral", "COMPETITOR_CONTEXT", hyp="H9", note="Analogy to magicpin delivery problems")
json.dump(codes, open(P, "w"), indent=1, ensure_ascii=False)
print(len(codes), "codes total;", sum(1 for k in codes if k.startswith("RD-")), "reddit")
