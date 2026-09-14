"""Reddit coding batch 6 (AI first pass)."""
import json, os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "codes_reddit_b2.py")).read().split("# ---- RD-1vq18l9")[0])
T = "RD-1vspuva"
C(T, 1, "neg", "RIDER_COORDINATION_FAILURE;SUPPORT_SLOW;SUPPORT_UNRESPONSIVE;LATE_DELIVERY", sev=3, stage="dispatch_eta", hyp="H3;H4;H12",
  eta="initial ETA already 1 hour; rider never went to restaurant; >1 h elapsed", support="~20 min to first response; agent left without helping",
  note="2026-08-19 7:44 pm order; post has an 'Update' that RSS truncates — final outcome unknown")
C(T+"-p4ooll8", 1, "neg", "LATE_NIGHT_RELIABILITY_RISK;RIDER_CONDUCT;SUPPORT_SLOW", sev=3, stage="delivery_handoff", hyp="H3;H4;H12", rep=1,
  support="waited >1 h for bot to assign an agent; ~20 min per reply", trust="rider marks picked up and 'takes off with your order'",
  note="Says it happens 'only when you order late at night' — time-of-day reliability pattern (single user)")
C(T+"-p4rcb95", 1, "neg", "SUPPORT_UNRESPONSIVE;INCUMBENT_BETTER_EXPERIENCE", sev=3, hyp="H4;H12", churn=1,
  sw="away_from_ownly: one order, worse than Zomato/Swiggy; deleted account ('for the first time')")
C(T+"-p4spy3n", 0, "neg", "SUPPORT_UNRESPONSIVE", stage="post_order_support_refund", hyp="H4", support="'If something goes south you are on your own on Ownly'")
json.dump(codes, open(P, "w"), indent=1, ensure_ascii=False)
print(len(codes), "codes total;", sum(1 for k in codes if k.startswith("RD-")), "reddit")
