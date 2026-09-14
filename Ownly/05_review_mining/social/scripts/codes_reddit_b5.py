"""Reddit coding batch 5 (AI first pass). [SAME_INCIDENT:<id>] in coding_note = same author/incident as that item; count once."""
import json, os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "codes_reddit_b2.py")).read().split("# ---- RD-1vq18l9")[0])
T = "RD-1w8qx26"; S = "[SAME_INCIDENT:RD-1w8qx26] "
C(T, 1, "neg", "RELIABILITY_OVER_PRICE;INCUMBENT_BETTER_RECOVERY;LARGE_ORDER_TRUST_RISK;FREE_DELIVERY_PERCEPTION", sev=4, stage="food_quality_accuracy", hyp="H4;H6;H8;H12",
  sw="away_from_ownly: 'Not worth the no delivery prices and no platform fee'; Swiggy service 'a million times better'", city="Bengaluru",
  note="2026-09-06, ~₹2k order. Poster perceives Ownly as having no delivery fee")
C(T+"-p84qr61", 0, "neg", "RAPIDO_BRAND_NEGATIVE_SPILLOVER", hyp="H7", trust="'they have Rapido DNA. Don't expect any help from any of the rapido's ventures'", note="Explicit negative brand transfer from Rapido to Ownly")
C(T+"-p84pggr", 1, "neg", "PLATFORM_RESTAURANT_CANCELLATION;REFUND_ISSUE", sev=4, stage="post_order_support_refund", hyp="H4;H12", support="app shows refund, not received (₹1.2k, Wendy's)")
C(T+"-p85h050", 1, "neg", "PLATFORM_RESTAURANT_CANCELLATION;REFUND_ISSUE", sev=4, stage="post_order_support_refund", hyp="H4;H12", support="cancelled, no refund")
X(T+"-p85h0v2", note="exact duplicate of p85h050 — excluded")
C(T+"-p84t718", 0, "neutral", "COMPETITOR_ALTERNATIVE_SUGGESTED;TOING_VS_OWNLY", hyp="H2", note="Suggests Swiggy Toing or Swish instead")
C(T+"-p850abw", 1, "neg", "LATE_DELIVERY;TRACKING_OPACITY;SUPPORT_UNRESPONSIVE", sev=3, stage="dispatch_eta", hyp="H4;H12", churn=1,
  sw="away_from_ownly: first order took ~1.5 h; deleted account", eta="rider picked up 'in his own time'; no tracking after pickup; ~1.5 h delay", support="'useless'")
C(T+"-p84nen4", 0, "neg", "CHURN_ADVOCACY;SUPPORT_UNRESPONSIVE", hyp="H12", note="Urges others to delete account")
C(T+"-p84o65a", 1, "neg", "REFUND_ISSUE", sev=4, stage="post_order_support_refund", hyp="H12", churn=1, trust="~₹3k refunds held", note=S+"'never ordering again'")
C(T+"-p84occw", 0, "neutral", "SUPPORT_WORKAROUND", stage="post_order_support_refund", hyp="H4", note="Suggests emailing a company social-media address")
C(T+"-p84o2tn", 1, "neg", "MISSING_WRONG_ITEMS;FOOD_QUALITY;SUPPORT_UNRESPONSIVE;COMPENSATION_REVERSED", sev=4, stage="food_quality_accuracy", hyp="H4;H12",
  support="no phone line; slow replies; offered 50% then withdrew", trust="'less than half the items'; food 'looked like it was already eaten'", note=S)
C(T+"-p84wc0o", 0, "pos", "ASTROTURF_SUSPICION;INCUMBENT_DISTRUST", hyp="H1;H7", note="'These guys are looting us and we now have an alternative' (re incumbents)")
C(T+"-p85079n", 1, "neutral", "RELIABILITY_OVER_PRICE", hyp="H4", note=S+"'cheaper prices isn't always a good thing'")
C(T+"-p85x98w", 0, "pos", "TOLERATE_CHALLENGER_HICCUPS;INCUMBENT_FEE_DISTRUST", hyp="H4;H12", note="Argues users should accept 'a few initial hiccups' to keep a low-fee challenger alive — counter-view to reliability-first")
C(T+"-p85z4gw", 1, "neg", "WTP_FOR_RELIABILITY;INCUMBENT_BETTER_RECOVERY", hyp="H4;H8", price="accepts Swiggy charging '20-30rs extra every order' for proper service and delivery", note=S+"Quantified reliability premium (₹20–30/order) — single user")
C(T+"-p87i3s5", 0, "pos", "INCUMBENT_FEE_STACK_FRUSTRATION", stage="pricing_checkout", hyp="H1", price="lists incumbent fees (platform, packing, rain, peak hour, etc.) and 'double the pricing per item'", note="Satirical fee list; claims of 'double' unverified")
C(T+"-p87jkgc", 0, "pos", "TOLERATE_CHALLENGER_HICCUPS", hyp="H12", note="Bounce scooter analogy: users fail to support good startups")
C(T+"-p87mjar", 1, "neg", "TRUST_LOSS_SCAM_FRAMING;REFUND_ISSUE", sev=4, hyp="H7;H12", note=S+"refund/voucher refused")
C(T+"-p87mci1", 1, "neg", "PRICE_PARITY_OBSERVED;DELIVERY_PROBLEMS_RECURRING", stage="pricing_checkout", hyp="H2;H12", rep=1,
  price="'compared prices with ownly and Swiggy it's not that different. The only extra charges of delivery packaging and platform fee aren't there'", note=S+"3 orders, all bad. Savings = fees only, not menu prices")
X(T+"-p87o0bk", T+"-p87xlls", T+"-p87y9m4", note="argumentative/personal banter; no new content")
C(T+"-p87tpto", 1, "neg", "PLATFORM_FAULT_ATTRIBUTION", hyp="H4;H12", note=S+"3 orders from 3 different restaurants — blames platform, not restaurants")
C(T+"-p85e0wi", 0, "neutral", "INCUMBENT_SAME_PROBLEMS", hyp="H4")
C(T+"-p86x8k1", 1, "pos", "RELIABLE_EXPERIENCE_POSITIVE", hyp="H4;H12", rep=1, note="10–12 orders in 2 weeks, no issues; new customer")
C(T+"-p87mqyk", 1, "neutral", "LOCATION_DEPENDENT_RELIABILITY", hyp="H4;H9", note=S+"speculates failures depend on location")
C(T+"-p87ne60", 1, "pos", "RELIABLE_EXPERIENCE_POSITIVE;LOCATION_DEPENDENT_RELIABILITY", hyp="H4;H9", city="Bengaluru", note="HSR Layout; orders from same 2 'standard places'")
C(T+"-p8b3uuc", 1, "neg", "NO_CASH_ON_DELIVERY", sev=1, stage="payment", hyp="H9", note="COD not offered at their location")
C(T+"-p854g39", 1, "pos", "RELIABLE_EXPERIENCE_POSITIVE;SUPPORT_RECOVERY_POSITIVE;LARGE_ORDER_TRUST_RISK", stage="post_order_support_refund", hyp="H4;H6;H12", rep=1,
  support="'quick customer service as well as refund immediately'", note="All orders under ₹1,000; speculates policies differ above ₹1,000")
X(T+"-p84we6r", T+"-p84ngom")
json.dump(codes, open(P, "w"), indent=1, ensure_ascii=False)
print(len(codes), "codes total;", sum(1 for k in codes if k.startswith("RD-")), "reddit")
