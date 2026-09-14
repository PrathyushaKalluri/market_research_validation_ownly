"""Reddit coding batch 8 (AI first pass). Phone numbers / rider names in this thread are redacted by build_social.py."""
import json, os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "codes_reddit_b2.py")).read().split("# ---- RD-1vq18l9")[0])
T = "RD-1tmgwrf"; R = "Alleged repeat-offender rider (same phone number reported by several users) — unverified allegation; PII redacted. "
C(T, 1, "neg", "NON_DELIVERY;RIDER_CONDUCT;SUPPORT_UNRESPONSIVE;REFUND_ISSUE;LATE_NIGHT_RELIABILITY_RISK;TRUST_LOSS_SCAM_FRAMING", sev=4, stage="delivery_handoff", hyp="H3;H4;H12",
  sw="away_from_ownly: 'Refrain from ordering from ownly late night'", support="no refund, no escalation", trust="marked delivered; CCTV/neighbours show no rider; rider phone switched off",
  note="2026-05-24. Thread became a collection point: ≥12 further users report the same pattern through Sep 2026")
C(T+"-onmte5s", 0, "neutral", "COD_AS_TRUST_SAFEGUARD", stage="payment", hyp="H4;H9", note="Suggests COD/pay-on-delivery as protection (also suggests posting rider's number — not reproduced)")
C(T+"-onno8o8", 1, "neutral", "NO_CASH_ON_DELIVERY", sev=1, stage="payment", hyp="H9")
C(T+"-p2osu3v", 1, "neg", "NON_DELIVERY;RIDER_CONDUCT", sev=4, stage="delivery_handoff", hyp="H4", note=R+"2026-08-09")
C(T+"-p2p0x02", 1, "neg", "NON_DELIVERY", sev=3, stage="delivery_handoff", hyp="H4", note="Brief 'happened with me just now'")
C(T+"-onn8bjy", 1, "mixed", "NON_DELIVERY;SUPPORT_RECOVERY_POSITIVE", sev=2, stage="post_order_support_refund", hyp="H4;H12", support="'processed refund without much hassle'")
C(T+"-orfhkxt", 0, "neutral", "RIDER_VETTING_SUGGESTION", hyp="H9", note="Suggests security deposits from delivery partners")
C(T+"-opjoob7", 1, "neg", "NON_DELIVERY;RIDER_CONDUCT;SUPPORT_UNRESPONSIVE", sev=4, stage="delivery_handoff", hyp="H4;H12", support="'live agent never joins the chat'", note=R+"2026-06-03")
C(T+"-oq1lqwp", 1, "neg", "NON_DELIVERY;RIDER_CONDUCT", sev=4, stage="delivery_handoff", hyp="H4;H9", note=R+"2026-06-06 ('SAME NUMBER! SAME GUY!')")
C(T+"-oq1lhij", 1, "mixed", "NON_DELIVERY;SUPPORT_CLOSES_UNRESOLVED;SUPPORT_RECOVERY_AFTER_ESCALATION", sev=3, stage="post_order_support_refund", hyp="H4;H12",
  support="chats repeatedly closed as 'resolved'; refund only after threatening consumer court")
C(T+"-p0wks8m", 1, "neg", "PAYMENT_DEDUCTED_ORDER_FAILED;SUPPORT_UNRESPONSIVE", sev=3, stage="payment", hyp="H4;H9", support="support blamed customer's tab-switching", note="Twice: payment succeeded, order cancelled as 'payment failed' (2026-07-31)")
C(T+"-p0wogno", 0, "neutral", "SUPPORT_WORKAROUND", stage="post_order_support_refund", hyp="H4", note="Suggests credit-card chargeback")
C(T+"-p2p14i9", 1, "neg", "NON_DELIVERY;SUPPORT_CHANNEL_UNKNOWN", sev=3, stage="post_order_support_refund", hyp="H4", note="Asks for a support email/number — none known")
C(T+"-p31bwis", 1, "mixed", "LATE_DELIVERY;RIDER_CONDUCT", sev=3, stage="dispatch_eta", hyp="H3;H4", eta="due 2 h earlier; arrived after ~4 h; rider phone off", note="Platform assumed Ownly from thread context")
C(T+"-p4p288t", 1, "neg", "LATE_NIGHT_RELIABILITY_RISK;NON_DELIVERY;SUPPORT_UNRESPONSIVE", sev=3, stage="delivery_handoff", hyp="H3;H4", eta="ordered ~1:24 am; rider claimed delivered without coming near", note="2026-08-19")
C(T+"-p5ah0t7", 1, "mixed", "NON_DELIVERY;SUPPORT_RECOVERY_POSITIVE;LOW_AOV_ORDERING", sev=2, stage="post_order_support_refund", hyp="H4;H6", support="refund received; item only ₹68", note="Contrast with large-order refund disputes (RD-1w8qx26)")
C(T+"-p6913ng", 1, "neg", "ETA_DISPLAY_MISLEADING;CONTACT_DETAILS_WRONG;SUPPORT_BOT_NO_HUMAN;TRUST_LOSS_SCAM_FRAMING", sev=3, stage="dispatch_eta", hyp="H4;H12",
  eta="ETA frozen at 15 min", support="'a bot that never connects to a human'", note="Captain's and restaurant's numbers both wrong")
C(T+"-p6g6fcj", 1, "neg", "NON_DELIVERY;RIDER_CONDUCT", sev=3, stage="delivery_handoff", hyp="H4", note="Marked delivered while rider was a road away; rider didn't answer")
C(T+"-p75f38q", 1, "neg", "SUPPORT_CLOSES_UNRESOLVED;NON_DELIVERY", sev=4, stage="post_order_support_refund", hyp="H4;H12", support="support says 'delivery agent says order is delivered' and closes chat",
  note="[SAME_INCIDENT:RD-1vw5429-p75fa7u] same minute as two similar comments in other threads — counted once")
C(T+"-p9cp00m", 1, "mixed", "NON_DELIVERY;SUPPORT_RECOVERY_POSITIVE", sev=2, stage="post_order_support_refund", hyp="H4", support="got refund", note="2026-09-12 — issue still occurring two days before collection")
json.dump(codes, open(P, "w"), indent=1, ensure_ascii=False)
print(len(codes), "codes total;", sum(1 for k in codes if k.startswith("RD-")), "reddit")
