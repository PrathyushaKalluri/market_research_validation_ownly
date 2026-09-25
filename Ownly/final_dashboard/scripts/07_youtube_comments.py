"""
07_youtube_comments.py — code retrieved YouTube comments into theme families.

Source: 05_review_mining/youtube/*_comments.json (verbatim comments retrieved from the
YouTube InnerTube API). Evidence label: CONSUMER-GENERATED.

These are self-selected viewers of two explainer videos about Rapido/Ownly. Counts are
SHARES OF CODED COMMENTS MENTIONING A THEME - never order failure rates, never population
incidence, and never Gachibowli-specific unless the comment says so.
"""
import json
import os
import re

import pandas as pd

ROOT = "/Users/klprathyusha/Sem 3/Project/Ownly"
YT = f"{ROOT}/05_review_mining/youtube"
D = f"{ROOT}/final_dashboard/data"

VIDEOS = {
    "h6PJ_QB4CiQ": ("Can Rapido's \"Ownly\" beat Zomato-Swiggy?", "2026-03-28", "post-launch"),
    "2EI51Z7WQ3o": ("Rapido's Genius Strategy to Beat Zomato and Swiggy", "2025-06-17", "pre-launch"),
}

# keyword -> theme family. Deliberately conservative: a comment must say the thing.
RULES = {
    "PRICE_DOUBT": [r"\bwon'?t last", r"once they (build|get|have)", r"another (zomato|swiggy)",
                    r"\b0% today", r"increase.{0,20}(later|price|fee|commission)",
                    r"burn(ing)? (investor|vc|cash)", r"same as (zomato|swiggy)",
                    r"loot", r"after.{0,15}monopoly", r"raise.{0,15}price", r"hike"],
    "PRICE_ADVANTAGE": [r"cheap(er)?\b", r"low(er)? price", r"no platform fee", r"save[sd]? (money|\d)",
                        r"afford", r"transparent pricing", r"no hidden"],
    "RIDER_ECONOMICS": [r"\brider", r"\bdriver", r"captain", r"delivery (boy|partner|agent)",
                        r"earn(ing)?s?\b", r"per (order|hour|delivery) pay", r"gig worker"],
    "REGULATION": [r"\bban\b", r"regulat", r"government", r"licen[cs]e", r"court", r"legal",
                   r"bike ?taxi.{0,20}(ban|illegal)", r"karnataka"],
    "ONDC_PRECEDENT": [r"\bondc\b", r"open network"],
    "ZERO_COMMISSION": [r"commission", r"restaurant.{0,20}(margin|profit|side)", r"\bnrai\b",
                        r"subscription model", r"saas"],
    "COMPETITORS": [r"\btoing\b", r"\bswish\b", r"magicpin", r"eatclub", r"\bgrab\b", r"box8",
                    r"eatsure", r"blinkit", r"zepto"],
    "ASSORTMENT": [r"restaurant.{0,25}(less|few|limited|not (there|available|listed)|need)",
                   r"(less|few|limited).{0,15}restaurant", r"not available in", r"my city",
                   r"coverage", r"outlets"],
    "SPEED_ETA": [r"\beta\b", r"delivery time", r"\bslow(er)?\b", r"late", r"\bfast(er)?\b",
                  r"\d+ ?min"],
    "RELIABILITY": [r"don'?t deliver", r"cancel", r"wrong order", r"missing", r"not delivered",
                    r"bad experience", r"worst service"],
    "SUPPORT_REFUND": [r"refund", r"customer (care|support|service)", r"complain", r"no recourse",
                       r"resolution"],
    "TRUST_QUALITY": [r"hygien", r"quality", r"stale", r"fresh", r"food safety"],
    "WORD_OF_MOUTH": [r"friend", r"told me", r"recommend", r"heard about", r"word of mouth",
                      r"influencer", r"trust", r"referr"],
    "DISINTERMEDIATION": [r"call(ing)? (the )?(shop|restaurant|hotel)", r"order direct",
                          r"directly from", r"uninstall", r"cook at home", r"stopped ordering"],
    "CREATOR_CREDIBILITY": [r"sponsor", r"paid promo", r"\bpr\b", r"biased", r"shill"],
}

FIRSTHAND = [r"\bi (use|used|tried|ordered|order)\b", r"\bmy (order|experience)\b",
             r"i have (used|tried|ordered)", r"i'?ve (used|tried|ordered)"]

rows = []
for vid, (title, pub, phase) in VIDEOS.items():
    path = f"{YT}/{vid}_comments.json"
    if not os.path.exists(path):
        continue
    data = json.load(open(path))
    for c in data["comments"]:
        txt = (c.get("text") or "").strip()
        if not txt:
            continue
        low = txt.lower()
        themes = [fam for fam, pats in RULES.items()
                  if any(re.search(p, low) for p in pats)]
        # likes arrive as strings ('731', '', or '1.2K')
        raw = str(c.get("likes") or "").strip().replace(",", "")
        if raw.upper().endswith("K"):
            likes = int(float(raw[:-1]) * 1000)
        else:
            likes = int(raw) if raw.isdigit() else 0
        rows.append({
            "video_id": vid, "video_title": title, "published_video": pub, "phase": phase,
            "comment_id": c.get("id"), "author": c.get("author"), "published": c.get("published"),
            "likes": likes, "text": txt, "themes": ";".join(themes),
            "n_themes": len(themes),
            "first_hand_claim": int(any(re.search(p, low) for p in FIRSTHAND)),
            "mentions_ownly": int(bool(re.search(r"\bownly\b", low))),
            "evidence_type": "CONSUMER-GENERATED",
        })

C = pd.DataFrame(rows)
# drop the pinned creator/self-promo comment (contains the channel's own download links)
C = C[~C["text"].str.contains(r"finanjo\.com|notion\.site", case=False, na=False)]
C.to_csv(f"{D}/youtube_comments_coded.csv", index=False)

# theme summary
n_coded = int((C["n_themes"] > 0).sum())
summ = []
for fam in RULES:
    k = int(C["themes"].str.contains(fam, na=False).sum())
    kl = int(C[C["themes"].str.contains(fam, na=False)]["likes"].sum())
    summ.append({"theme_family": fam, "comments": k,
                 "share_of_coded_pct": round(k / n_coded * 100, 1) if n_coded else 0,
                 "total_likes_on_those_comments": kl})
S = pd.DataFrame(summ).sort_values("comments", ascending=False)
S["base_n_coded"] = n_coded
S["base_n_retrieved"] = len(C)
S["measure_definition"] = ("share of coded comments mentioning this theme - NOT a failure rate, "
                           "NOT population incidence")
S.to_csv(f"{D}/youtube_theme_summary.csv", index=False)

fh = C[(C["first_hand_claim"] == 1) & (C["mentions_ownly"] == 1)]
fh.to_csv(f"{D}/youtube_firsthand_ownly.csv", index=False)

print(f"videos: {len(VIDEOS)} | comments retrieved: {len(C)} | with >=1 theme: {n_coded}")
print(f"first-hand Ownly-use claims: {len(fh)}")
print()
print(S[["theme_family", "comments", "share_of_coded_pct", "total_likes_on_those_comments"]]
      .to_string(index=False))
print("\n--- highest-engagement comments (excl. pinned) ---")
for _, r in C.nlargest(6, "likes").iterrows():
    print(f'  [{r.likes:>4} likes] {r.text[:150].replace(chr(10)," ")}')
print("\n--- first-hand Ownly claims ---")
for _, r in fh.iterrows():
    print(f'  [{r.likes:>3}] {r.text[:190].replace(chr(10)," ")}')
