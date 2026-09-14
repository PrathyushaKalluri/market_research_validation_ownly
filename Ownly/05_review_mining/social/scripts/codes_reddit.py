"""Hand coding (AI first pass) of Reddit items, merged into codes.json. Keyed by stable ids RD-<thread>[-<comment>].
primary_theme = first listed theme. Items coded relevant=0 are banter/off-topic/no Ownly content."""
import json, os
SCR = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(SCR, "codes.json")
codes = json.load(open(P))
def C(i, fh, sent, themes, sev="", stage="NA_business_commentary", hyp="", ev="CONSUMER-GENERATED", sw="", churn=0, rep=0,
      price="", eta="", assort="", support="", trust="", note="", author=None, city=None):
    t = themes.split(";")
    d = dict(relevant=1, first_hand_ownly_use=fh, sentiment=sent, themes=themes, primary_theme=t[0], severity=sev, order_stage=stage,
             switching_trigger_flag=1 if sw else 0, switching_trigger_text=sw, churn_signal=churn, repeat_use_signal=rep,
             price_value_comment=price, delivery_eta_comment=eta, assortment_comment=assort, support_comment=support,
             trust_safety_quality_comment=trust, hypotheses_linked=hyp, evidence_label=ev, coding_note=note)
    if author: d["author_type"] = author
    if city: d["city_mentioned"] = city
    codes[i] = d
def X(*ids, note="banter/off-topic; no Ownly-relevant content"):
    for i in ids:
        codes[i] = dict(relevant=0, first_hand_ownly_use=0, sentiment="", themes="", primary_theme="", severity="", order_stage="",
                        switching_trigger_flag=0, switching_trigger_text="", churn_signal=0, repeat_use_signal=0, price_value_comment="",
                        delivery_eta_comment="", assortment_comment="", support_comment="", trust_safety_quality_comment="",
                        hypotheses_linked="", evidence_label="", coding_note=note)

# ---- RD-1vp2t3m  r/Zomato  2026-08-15  "Swiggy vs Ownly vs Zomato pricing" (image post) ----
T = "RD-1vp2t3m"
C(T, 1, "neutral", "USER_BILL_COMPARISON", stage="pricing_checkout", hyp="H1;H2", note="Image-only post; screenshots not retrievable via RSS. Commenter p3z47ie says OP's screenshots showed ~450 on Zomato/Swiggy vs ~300 on Ownly — direction taken from that reply, not verified", city="Bengaluru")
C(T+"-p3u6lpb", 0, "neutral", "TOING_VS_OWNLY", hyp="H2", note="Sees Swiggy Toing as Ownly's real competitor")
C(T+"-p3u7qii", 0, "neg", "TOING_VS_OWNLY;INCUMBENT_DISTRUST", hyp="H2;H9", trust="believes Toing exists only to kill Ownly then be shut", note="Profanity — do not quote")
C(T+"-p3u9630", 0, "neutral", "COMPETITOR_CONTEXT", hyp="H2", note="Flipkart entry mentioned")
C(T+"-p3z1ik8", 0, "pos", "TOING_VS_OWNLY", stage="pricing_checkout", hyp="H2", price="says Toing cannot match Ownly pricing; Toing 'price match' feature often fails", note="Implies Toing use; Ownly use not stated")
C(T+"-p3zdjt9", 0, "neg", "TOING_VS_OWNLY;INCUMBENT_DISTRUST", hyp="H2", note="Negative Toing experience (feature removed); competitor evidence")
C(T+"-p3uq8ca", 0, "neutral", "TOING_VS_OWNLY", hyp="H2", note="UI of Ownly resembles Toing")
C(T+"-p3wb68m", 0, "neg", "FUTURE_FEE_CREEP_EXPECTED", hyp="H2;H7", price="'once they have market share they will spike up'")
C(T+"-p3woziw", 0, "neg", "DELIVERY_PRICE_LEVEL_TOO_HIGH", hyp="H1", price="₹300–400 for idli/dosa seen as absurd regardless of app")
C(T+"-p3wfvo8", 0, "neutral", "SUSTAINABILITY_SKEPTICISM", hyp="H2")
C(T+"-p3z47ie", 1, "mixed", "ACCEPTS_WAIT_FOR_SAVINGS;PRICE_SAVINGS_OBSERVED;LATE_DELIVERY;RIDER_MULTI_APP_OBSERVED;FUTURE_FEE_CREEP_EXPECTED", sev=2, stage="dispatch_eta", hyp="H2;H3;H9;H12",
  sw="to_ownly: ~₹300 vs ~₹450 (incl. first-order extra discount); accepts +10–15 min wait to save ~₹150", rep=1,
  price="Ownly ~300 vs Zomato/Swiggy ~450 with an extra Ownly discount on first order", eta="slower than Swiggy/Zomato by ~10–15 min; 'don't mind waiting'",
  note="Most direct price–ETA trade-off statement in dataset (H3). Tried twice. Rider bill said 'rapido', no uniform")
C(T+"-p3z5k7n", 1, "neutral", "RIDER_MULTI_APP_OBSERVED", stage="delivery_handoff", hyp="H9", note="Rider wore Ownly helmet with Swiggy bag — shared rider supply with incumbents (observation, not verified)")
C(T+"-p3z5tlv", 0, "neutral", "RIDER_MULTI_APP_OBSERVED", hyp="H9", ev="INTERPRETATION")
C(T+"-p3wc86d", 0, "neutral", "CITY_AVAILABILITY_QUESTION", stage="discovery_onboarding", hyp="H9", city="Bengaluru")
C(T+"-p3z5bd9", 0, "neutral", "CITY_AVAILABILITY_QUESTION", stage="discovery_onboarding", hyp="H9", city="Bengaluru", note="2026-08-16: commenter believes Ownly is Bengaluru-only")
C(T+"-p3xdxl1", 0, "pos", "GENERAL_SUPPORT_FOR_OWNLY", hyp="H7")
C(T+"-p3z0kqj", 1, "neg", "MEAL_CARD_PAYMENT_GAP", sev=2, stage="payment", hyp="H6;H9;H12", note="Ownly does not accept meal cards / Pluxee — relevant to salaried professionals using employer meal benefits")
C(T+"-p47hzt0", 0, "neutral", "MEAL_CARD_PAYMENT_GAP", stage="payment", hyp="H6")
C(T+"-p3z7ulc", 0, "neutral", "MULTI_HOMING_PRICE_COMPARISON", stage="pricing_checkout", hyp="H1;H12", price="'always compare all 3'; best deal rotates between Zomato and Swiggy")
C(T+"-p3zl1ol", 1, "neg", "LATE_DELIVERY;ETA_DISPLAY_MISLEADING;SUPPORT_UNRESPONSIVE;RESTAURANT_PLATFORM_BLAME_LOOP", sev=3, stage="dispatch_eta", hyp="H4;H9;H12",
  sw="away_from_ownly: 1-hour non-arrival while app showed 11 min; support slow; escalated by email next day",
  eta="app showed 11 mins; order not arrived after 1 hour", support="support slow/unresponsive; restaurant redirected to Ownly")
C(T+"-p3zl4ah", 1, "neutral", "WTP_FOR_RELIABILITY", hyp="H4;H8", sw="away_from_ownly: 'convinced to pay a bit more but get things or resolution in time'",
  note="Reply in same sub-thread as p3zl1ol; RSS gives no authorship so same-author is assumed, not verified. Key H4 statement: paying more for reliability/resolution")
C(T+"-p3zncna", 0, "neutral", "INCUMBENT_SAME_PROBLEMS", hyp="H4", note="Says Swiggy/Zomato have same failures")
C(T+"-p3zl7d0", 0, "neg", "FUTURE_FEE_CREEP_EXPECTED", hyp="H2;H7", note="Hinglish, vulgar: expects exploitation after IPO — do not quote")
C(T+"-p40c2ff", 0, "neutral", "TRANSPARENT_DELIVERY_FEE_PREFERENCE;INCUMBENT_PRICE_OBSTACLE", stage="pricing_checkout", hyp="H1;H2;H8",
  price="wants an explicit delivery fee instead of 'free delivery' with inflated menu prices")
C(T+"-p41fyke", 0, "neg", "INCUMBENT_FEE_OPACITY", stage="pricing_checkout", hyp="H1", price="Swiggy bundles 'GST and other charges'; prefers Zomato's itemised platform fee")
C(T+"-p47v3kg", 0, "neutral", "INCUMBENT_CHEAPER_CONDITIONAL", stage="pricing_checkout", hyp="H2", price="for small minimum orders Zomato may be best")
C(T+"-p4kknmn", 0, "neutral", "COMPETITOR_CONTEXT", hyp="H2", note="ONDC/Digihaat")
C(T+"-p6l12ro", 0, "neutral", "LAUNCH_DISCOUNT_TEMPORARY", stage="pricing_checkout", hyp="H2;H12", note="Parent comment not identifiable in RSS; likely refers to an introductory Ownly discount 'only for first 3 orders' — unverified")
C(T+"-p3zfi23", 0, "neg", "FUTURE_FEE_CREEP_EXPECTED;CITY_EXPANSION_PRICE_RISE_EXPECTED", hyp="H2;H9", city="Bengaluru",
  price="expects prices to rise to parity in new cities 'apart from the first few weeks'", note="Directly relevant to Hyderabad transfer (H9)")
C(T+"-p45k2my", 0, "neg", "SUSTAINABILITY_SKEPTICISM", hyp="H9", note="Relays an X claim of ₹150–170 cash burn per order and ₹1,700–2,000 cr to reach 5% share — unverified second-hand figures; do not cite as fact")
X(T+"-p3z0e57", T+"-p3z1jxl", T+"-p3z3dn1", T+"-p3z99ov", note="off-topic (screenshot doxxing banter / restaurant opinion)")

# ---- RD-1qcrc1f  r/BangaloreSocial  2026-01-14  "Anyone using Ownly (Rapido's food delivery)" ----
T = "RD-1qcrc1f"
C(T, 1, "pos", "PRICE_SAVINGS_OBSERVED;MULTI_HOMING_ASSORTMENT;FUTURE_FEE_CREEP_EXPECTED", stage="pricing_checkout", hyp="H2;H10;H12", rep=1,
  price="'always so in awe of how cheap the final pricing is'", assort="keeps Swiggy for some exclusive restaurants", note="3 months on/off use alongside Swiggy", city="Bengaluru")
C(T+"-nzkcrwd", 0, "neutral", "LOW_AWARENESS", stage="discovery_onboarding", hyp="H7")
C(T+"-nzkgt0d", 0, "pos", "SERVICE_AREA_LIMITED", stage="discovery_onboarding", hyp="H9", city="Bengaluru", note="Jan 2026: only some areas of Bangalore")
C(T+"-ocrqahg", 0, "neg", "ASTROTURF_SUSPICION", hyp="H7", trust="suspects positive posts are Ownly marketing")
C(T+"-nzkr1nx", 0, "neutral", "TRIAL_CURIOSITY", stage="browse_menu", hyp="H10", assort="asks about menu before trying")
C(T+"-nzkv72b", 1, "mixed", "ASSORTMENT_LIMITED;PRICE_SAVINGS_OBSERVED", stage="browse_menu", hyp="H2;H10", price="'Pricing is where it's killer'", assort="'Great but not extensive'")
C(T+"-nzketdz", 0, "neutral", "TRIAL_CURIOSITY", stage="pricing_checkout", hyp="H2")
C(T+"-nzkh0ra", 1, "pos", "PRICE_SAVINGS_OBSERVED;LOW_AOV_ORDERING", stage="pricing_checkout", hyp="H2;H8", price="order as low as ₹40 → ₹45 final after delivery", note="Jan 2026 pilot-era fee; not current")
C(T+"-p0wrhum", 1, "neutral", "PRICE_PARITY_OBSERVED", stage="pricing_checkout", hyp="H2", price="'almost same price if no card discount in Swiggy'", note="2026-07-31; screenshots not retrievable; direction of comparison ambiguous — AMBIGUOUS")
C(T+"-ocrqfj6", 1, "neg", "APP_UX_SLOW_GLITCHY;RIDER_UNTRAINED;ASTROTURF_SUSPICION", sev=2, stage="app_account", hyp="H9;H12", churn=1, rep=1,
  sw="away_from_ownly: slow glitchy app; confused riders", trust="suspects supporters are marketing team", note="Used 2 weeks; 'going to delete my account'")
C(T+"-ocrvht0", 1, "mixed", "APP_UX_SLOW_GLITCHY;RIDER_MULTI_APP_OBSERVED;LOW_AWARENESS", sev=2, stage="app_account", hyp="H7;H9", note="Riders 'okaish'; use Swiggy/Zomato packaging; 'no one seems to know about them'")
C(T+"-o6kcml5", 1, "neg", "RIDER_CONDUCT;SUPPORT_SLOW;PLATFORM_RESTAURANT_CANCELLATION;TRUST_LOSS_SCAM_FRAMING", sev=3, stage="delivery_handoff", hyp="H4;H9;H12",
  sw="away_from_ownly: 'avoid it'", eta="over an hour then cancelled", support="10–15 min per support response", note="Feb 2026; first rider drove away")
C(T+"-p2huep3", 0, "neutral", "INCUMBENT_SAME_PROBLEMS", hyp="H4")
C(T+"-oo7vwmt", 1, "neg", "NON_DELIVERY;NO_CASH_ON_DELIVERY", sev=3, stage="delivery_handoff", hyp="H4;H9", note="Marked delivered but not received; no pay-on-delivery")
C(T+"-oome4g5", 1, "neg", "TRUST_LOSS_SCAM_FRAMING", sev=4, stage="post_order_support_refund", hyp="H7;H12", trust="claims ₹3k lost ('scammed for 3k')", note="No detail; unverified allegation")
C(T+"-owap5ff", 1, "pos", "ACCEPTS_HASSLE_FOR_SAVINGS;PRICE_SAVINGS_OBSERVED;NO_HIDDEN_FEES_POSITIVE", stage="pricing_checkout", hyp="H2;H4;H12", rep=1,
  sw="to_ownly: 'I'll discount that for the money I am saving'", price="'Very cheap, and no extra charges'", note="Tolerates 'little hassle' for savings — H4 counter-evidence to reliability-first")

# ---- RD-1nk2ror  r/ShareBazarIndia  2025-09-18  pilot commentary ----
T = "RD-1nk2ror"
C(T, 0, "pos", "LAUNCH_CLAIM_RELAY;FEE_MODEL_DESCRIPTION;RAPIDO_ECOSYSTEM_ADVANTAGE", hyp="H2;H7", ev="MEDIA REPORT", author="investor_analyst_media",
  price="relays 'effective order values 17–49% cheaper'; flat restaurant fee, zero user delivery charge (pilot)", note="Figures unsourced in post (likely brokerage/media research)")
C(T+"-nev20nr", 0, "pos", "WELCOME_THIRD_COMPETITOR;INCUMBENT_DISTRUST", hyp="H1")
C(T+"-nf7kcb2", 0, "neg", "RIDER_EARNINGS_CONCERN", hyp="H9", note="Doubts captain economics (~₹25 for 10 km on E20 petrol) — supply-side risk")
C(T+"-nfi8jqw", 0, "neg", "RIDER_EARNINGS_CONCERN", hyp="H9")
C(T+"-nfok3th", 0, "neutral", "RIDER_EARNINGS_CONCERN;FEE_MODEL_DESCRIPTION", hyp="H8;H9", note="Questions non-distance-based delivery fee")

# ---- RD-1vpxbyr  r/BangaloreSocial  2026-08-16  "Ownly vs Zomato !!!" ----
T = "RD-1vpxbyr"
C(T, 1, "neg", "USER_BILL_COMPARISON;PRICE_COMPARISON_DISPUTE", stage="pricing_checkout", hyp="H2", city="Bengaluru",
  note="Screenshot not retrievable. Post says 'same restaurant same dish… platforms are scamming'; replies dispute which app was cheaper (Imperio half/quarter plate) — direction AMBIGUOUS")
C(T+"-p40z6fw", 1, "pos", "PRICE_SAVINGS_OBSERVED", stage="pricing_checkout", hyp="H2", price="Ownly ~30% cheaper than Zomato for this user")
C(T+"-p40ymz4", 0, "neutral", "TRIAL_CURIOSITY", hyp="H12")
C(T+"-p40z0hq", 1, "neg", "OWNLY_PRICIER_OBSERVED", stage="pricing_checkout", hyp="H2", price="'half plate at 60rs higher than Zomato' (Imperio)", note="Contradicts H2 for a specific listing")
C(T+"-p41atep", 1, "mixed", "INCUMBENT_CHEAPER_AFTER_OFFERS;PRICE_SAVINGS_OBSERVED;MULTI_HOMING_PRICE_COMPARISON;INCUMBENT_DEFENSIVE_DISCOUNTING", stage="pricing_checkout", hyp="H2;H12", rep=1,
  price="2 weeks, ≥1 order/day, ≥2 restaurants checked: pre-coupon Zomato never lower; Zomato coupons made totals equal or ₹15–20 below Ownly",
  note="Most systematic user comparison found. Reads Zomato coupons as temporary defensive tactic")
C(T+"-p41g7mi", 1, "neg", "OWNLY_PRICIER_OBSERVED;PRICE_COMPARISON_DISPUTE", stage="pricing_checkout", hyp="H2", note="Disputes p41atep with a screenshot (item size mismatch 'quarter' vs half) — shows item-matching problems in comparisons")
C(T+"-p4k7g8h", 0, "neutral", "PRICE_COMPARISON_DISPUTE", stage="pricing_checkout", hyp="H2", note="AMBIGUOUS which platform")
C(T+"-p4n9d1n", 1, "neg", "MISSING_WRONG_ITEMS;RIDER_CONDUCT;TRUST_LOSS_SCAM_FRAMING;LARGE_ORDER_TRUST_RISK", sev=4, stage="delivery_handoff", hyp="H4;H6;H10;H12",
  sw="away_from_ownly: 'if ur ordering for more items don't trust ownly'", trust="rider allegedly left with half the order")
C(T+"-p4scllw", 1, "neg", "SUPPORT_UNRESPONSIVE;MISSING_WRONG_ITEMS", sev=4, stage="post_order_support_refund", hyp="H4;H12", support="reported; 'haven't taken any action'; 'practically non existent'", note="Same incident as p4n9d1n (assumed same author)")
C(T+"-p56oj1w", 0, "neutral", "ASTROTURF_SUSPICION", stage="pricing_checkout", hyp="H2;H7", price="asserts Zomato prices are higher", note="Suspects post is paid by Zomato")
X(T+"-p40zdqb", T+"-p419axy", T+"-p4rs5jk", T+"-p56on51")

json.dump(codes, open(P, "w"), indent=1, ensure_ascii=False)
print(len(codes), "codes total;", sum(1 for k in codes if k.startswith("RD-")), "reddit")
