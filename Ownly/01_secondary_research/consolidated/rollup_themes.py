#!/usr/bin/env python3
"""Theme-family rollup over the two coded datasets. Reproduces the exhibit in
consolidated_evidence_pack.md Section 1. Stdlib only. Run from the project root."""
import csv, collections, re, sys

FAM = {
 'PRICE_ADVANTAGE': ['PRICE_SAVINGS_OBSERVED','USER_BILL_COMPARISON','LOWER_PRICE_VALUE_POSITIVE',
                     'NO_HIDDEN_FEES_POSITIVE','FEE_MODEL_DESCRIPTION','CHEAPER'],
 'PRICE_DOUBT':     ['FUTURE_FEE_CREEP_EXPECTED','SUSTAINABILITY_SKEPTICISM','HISTORICAL_PRICE_CONVERGENCE',
                     'INCUMBENT_CHEAPER_AFTER_OFFERS','MENU_PRICE_INFLATION_ON_OWNLY','AGGREGATOR_MARKUP_WORKAROUND'],
 'FULFILMENT_FAIL': ['NON_DELIVERY','NOT_DELIVERED_OR_FALSE_DELIVERED','LATE_DELIVERY','LATE_DELIVERY_ETA_BREACH',
                     'PLATFORM_RESTAURANT_CANCELLATION','CANCELLATION','MISSING_OR_WRONG_ITEMS','CANCELLATION_BLOCKED'],
 'SUPPORT_REFUND':  ['SUPPORT_UNRESPONSIVE','SUPPORT_UNRESPONSIVE_OR_SCRIPTED','REFUND',
                     'PAYMENT_DEDUCTED_ORDER_FAILED','REFUND_DELAY'],
 'ASSORTMENT':      ['CITY_AVAILABILITY_QUESTION','RESTAURANT_UNAVAILABLE','LISTING_MENU_ACCURACY','ASSORTMENT'],
 'COMPETITION':     ['TOING_VS_OWNLY','COMPETITOR_CONTEXT','LOW_PLATFORM_LOYALTY'],
 'DISTRIBUTION':    ['RAPIDO_ECOSYSTEM_ADVANTAGE','TRIAL_CURIOSITY','LAUNCH_CLAIM_RELAY'],
 'TRUST_QUALITY':   ['FOOD_QUALITY_HYGIENE','DIETARY_VEG_TRUST','RIDER_CONDUCT_OR_UNREACHABLE','ASTROTURF_SUSPICION'],
}
RMAP = {c: f for f, cs in FAM.items() for c in cs}

def load(p):
    with open(p, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def split(v):
    return [t.strip().upper() for t in re.split(r'[;|,]', v or '') if t.strip()]

def rollup(rows, first_hand_only=False):
    c, base = collections.Counter(), 0
    for r in rows:
        if first_hand_only and (r.get('first_hand_ownly_use') or '') != '1':
            continue
        codes = split(r.get('themes', '')) or split(r.get('primary_theme', ''))
        fams = {RMAP[x] for x in codes if x in RMAP}
        for f in fams:
            c[f] += 1
        if fams:
            base += 1
    return c, base

def show(title, c, base):
    print(f"\n{title}  (base n={base})")
    for k, v in c.most_common():
        print(f"  {v:4d}  {100*v/base:5.1f}%  {k}")

if __name__ == '__main__':
    soc = load('05_review_mining/social/social_coded.csv')
    rev = load('05_review_mining/app_stores/reviews_coded.csv')
    show('SOCIAL — all discussion', *rollup(soc))
    show('SOCIAL — first-hand Ownly use only', *rollup(soc, True))
    show('APP-STORE REVIEWS', *rollup(rev))
