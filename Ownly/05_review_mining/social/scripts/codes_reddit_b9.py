"""Reddit coding batch 9 (AI first pass)."""
import json, os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "codes_reddit_b2.py")).read().split("# ---- RD-1vq18l9")[0])
C("RD-1vj71um", 1, "neg", "SUPPORT_UNRESPONSIVE;GENERAL_SERVICE_COMPLAINT", sev=2, stage="post_order_support_refund", hyp="H4;H12",
  support="'horrible customer support'", note="r/Ownly (unofficial community sub), 2026-08-08; no detail")
C("RD-1vbqoq9", 0, "neutral", "LAUNCH_CLAIM_RELAY", hyp="H9", ev="MEDIA REPORT", author="investor_analyst_media",
  note="Relays ~7% Bengaluru share, >40,000 daily orders, ~25,000 restaurants; post itself says share 'not independently confirmed by Rapido'; 'preparing for expansion beyond Bengaluru' (2026-07-31)")
json.dump(codes, open(P, "w"), indent=1, ensure_ascii=False)
print(len(codes), "codes total;", sum(1 for k in codes if k.startswith("RD-")), "reddit")
