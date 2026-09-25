#!/usr/bin/env python3
"""
Shared text-analytics library: negation-aware sentiment lexicon and TF-IDF.

Lifted unchanged from SUBMIT_BI/build_data.py, where the lexicon was validated
against app-store star ratings: Spearman rho = 0.648, n = 37, p < 0.001, and
monotonic from 1 star (-0.66) to 5 stars (+0.34). The lexicon was written blind
to the star ratings, so that check is genuinely out-of-sample.
"""
import math, re
from collections import Counter, defaultdict

# ════════════════════════════════════════════════════════════════════
# SENTIMENT — domain lexicon, negation-aware
# ════════════════════════════════════════════════════════════════════

POS = {
 "good":1,"great":2,"excellent":2,"amazing":2,"awesome":2,"love":2,"loved":2,"best":2,
 "nice":1,"happy":1.5,"cheap":1,"cheaper":1,"affordable":1.5,"reasonable":1,"fast":1.5,
 "quick":1.5,"quickly":1.5,"fresh":1.5,"hot":1,"tasty":1.5,"delicious":2,"smooth":1.5,
 "easy":1,"helpful":1.5,"support":0.5,"refund":0.5,"genuine":1.5,"transparent":2,
 "honest":1.5,"save":1.5,"saving":1.5,"saved":1.5,"discount":1,"free":1,"zero":0.5,
 "recommend":2,"recommended":2,"better":1.5,"improve":0.5,"improved":1.5,"perfect":2,
 "satisfied":2,"reliable":1.5,"working":1,"works":1,"worth":1.5,"superb":2,"thanks":1,
 "convenient":1.5,"sustainable":1,"support":0.5,"welcome":1,"win":1.5,"benefit":1.5,
}
NEG = {
 "bad":-1.5,"worst":-2.5,"terrible":-2.5,"awful":-2.5,"horrible":-2.5,"pathetic":-2.5,
 "poor":-1.5,"hate":-2,"scam":-2.5,"fraud":-2.5,"cheat":-2.5,"cheating":-2.5,"fake":-2,
 "late":-1.5,"delay":-1.5,"delayed":-1.5,"slow":-1.5,"waiting":-1,"wait":-0.8,
 "cancel":-1.5,"cancelled":-1.8,"cancellation":-1.5,"missing":-2,"wrong":-1.8,
 "cold":-1.5,"stale":-2,"spoiled":-2,"rotten":-2.5,"disgusting":-2.5,
 "expensive":-1.5,"costly":-1.5,"overpriced":-2,"charge":-0.5,"charges":-0.8,"fee":-0.5,
 "fees":-0.8,"hidden":-1.5,"surge":-1,"increase":-0.8,"increased":-1,"rise":-0.8,
 "never":-1,"nothing":-0.8,"nobody":-1,"useless":-2,"waste":-2,"wasted":-2,
 "refuse":-1.5,"refused":-1.5,"complaint":-1.5,"issue":-1,"issues":-1.2,"problem":-1.2,
 "problems":-1.5,"error":-1.2,"bug":-1.2,"crash":-1.5,"stuck":-1.5,"failed":-1.8,
 "fail":-1.5,"unavailable":-1.2,"unprofessional":-2,"rude":-2,"ignore":-1.5,
 "ignored":-1.8,"disappointed":-2,"disappointing":-2,"frustrating":-2,"annoying":-1.5,
 "loss":-1.2,"lose":-1.2,"losing":-1.2,"burn":-1,"unsustainable":-1.5,"doubt":-1,
 "risky":-1.2,"exploit":-2,"exploitation":-2,"underpaid":-2,"struggle":-1.5,
}
NEGATORS = {"not","no","never","dont","don't","doesnt","doesn't","didnt","didn't",
            "cant","can't","wont","won't","isnt","isn't","without","hardly","nor"}
INTENS = {"very":1.5,"really":1.4,"extremely":1.8,"totally":1.5,"absolutely":1.7,
          "completely":1.6,"so":1.3,"too":1.3,"highly":1.4,"super":1.4}

TOKEN = re.compile(r"[a-z']+")

def sentiment(text):
    """Return (score in [-1,1], label). Lexicon + negation + intensifiers."""
    if not text: return 0.0, "neutral"
    toks = TOKEN.findall(text.lower())
    if not toks: return 0.0, "neutral"
    total, hits = 0.0, 0
    for i, t in enumerate(toks):
        w = POS.get(t, 0) or NEG.get(t, 0)
        if w == 0: continue
        mult = 1.0
        for k in (1, 2):
            if i-k >= 0:
                prev = toks[i-k]
                if prev in NEGATORS: mult *= -0.85
                elif prev in INTENS and k == 1: mult *= INTENS[prev]
        total += w*mult; hits += 1
    if hits == 0: return 0.0, "neutral"
    raw = total/math.sqrt(hits)          # dampen long-text accumulation
    score = max(-1.0, min(1.0, raw/3.0))
    label = "positive" if score > 0.12 else ("negative" if score < -0.12 else "neutral")
    return round(score, 3), label

STOP = set("""a an the and or but if then than that this these those is are was were be been being am
of to in on at by for with from as it its it's i you he she they we me my our your their them his her
not no do does did doing done have has had having will would can could should may might must shall
so such very too also just only more most much many other some any each every all both few own same
there here what which who whom when where why how about into over under again further once now then
get got go going one two three s t re ve ll d m ain don didn doesn isn aren wasn weren won t
they're you're we're i'm i've don't can't won't it's he's she's that's there's what's let's
food order orders app apps delivery deliver delivered swiggy zomato ownly rapido rs inr
""".split())

def tfidf_terms(docs, top=14, min_df=2):
    """Top distinctive terms by mean TF-IDF. `docs` is a list of strings."""
    tok_docs = []
    for d in docs:
        ts = [t for t in TOKEN.findall((d or "").lower()) if len(t) > 2 and t not in STOP]
        tok_docs.append(ts)
    N = len(tok_docs)
    if N == 0: return []
    df = Counter()
    for ts in tok_docs: df.update(set(ts))
    scores = defaultdict(float)
    for ts in tok_docs:
        if not ts: continue
        tf = Counter(ts); L = len(ts)
        for t, c in tf.items():
            if df[t] < min_df: continue
            scores[t] += (c/L) * math.log(N/(1+df[t]) + 1)
    out = sorted(scores.items(), key=lambda kv: -kv[1])[:top]
    return [{"term": t, "score": round(s, 4), "df": df[t]} for t, s in out]

