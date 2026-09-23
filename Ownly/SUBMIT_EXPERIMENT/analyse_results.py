#!/usr/bin/env python3
"""
Ownly fake door — analysis.

Reads exported event CSVs (from the facilitator downloads or the Google Sheet),
drops QA and bot sessions, deduplicates by participant, and computes the funnel,
the primary metric and the pre-registered comparisons from EXPERIMENT_DESIGN.md.

Statistics implemented from scratch (no numpy/scipy on this machine):
  * Fisher's exact test, two-sided
  * Wilson score interval for a single proportion
  * Newcombe-Wilson hybrid score interval for a DIFFERENCE of proportions

Usage:
    python3 analyse_results.py events1.csv events2.csv ...
    python3 analyse_results.py --demo          # runs on fabricated data, clearly marked
"""

import csv, json, math, statistics, sys
from collections import defaultdict, Counter

# ─────────────────────────── statistics ───────────────────────────

def wilson(k, n, z=1.959963985):
    """Wilson score interval for one proportion. Returns (point, lo, hi) in %."""
    if n == 0:
        return (None, None, None)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (100 * p, 100 * max(0.0, c - h), 100 * min(1.0, c + h))


def newcombe_diff(k1, n1, k2, n2, z=1.959963985):
    """
    Newcombe-Wilson hybrid score interval for (p1 - p2).

    Preferred over the Wald interval because it keeps sensible coverage when a
    rate is near 0 or 1 and when n is small — exactly our situation.
    """
    if n1 == 0 or n2 == 0:
        return (None, None, None)

    def bounds(k, n):
        p = k / n
        d = 1 + z * z / n
        c = (p + z * z / (2 * n)) / d
        h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
        return max(0.0, c - h), min(1.0, c + h)

    l1, u1 = bounds(k1, n1)
    l2, u2 = bounds(k2, n2)
    p1, p2 = k1 / n1, k2 / n2
    diff = p1 - p2
    lo = diff - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)
    hi = diff + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)
    return (100 * diff, 100 * lo, 100 * hi)


def fisher_exact(a, b, c, d):
    """Two-sided Fisher exact test on [[a,b],[c,d]]. Returns p."""
    n = a + b + c + d
    if n == 0:
        return None
    C = math.comb

    def pr(A):
        B, Cc, D = (a + b) - A, (a + c) - A, d - (a - A)
        if B < 0 or Cc < 0 or D < 0:
            return 0.0
        return C(a + b, A) * C(c + d, Cc) / C(n, a + c)

    obs = pr(a)
    total = 0.0
    for A in range(0, min(a + b, a + c) + 1):
        p = pr(A)
        if p <= obs + 1e-12:
            total += p
    return min(1.0, total)


# ─────────────────────────── loading ───────────────────────────

FUNNEL = [
    ("landing_page_view",       "Saw the app"),
    ("first_meaningful_tap",    "Tapped something"),
    ("dish_search_view",        "Reached the search"),
    ("searched",                "Searched — dish or place"),
    ("chose",                   "Chose a dish or a place"),
    ("menu_view",               "Opened a menu"),
    ("item_added",              "Put something in the cart"),
    ("delivery_screen_view",    "Reached the delivery step"),
    ("cart_view",               "Opened the cart"),
    ("offer_applied",           "Applied an offer"),
    ("bill_option_chosen",      "Chose how to pay"),
    ("place_order_click",       "Tapped Place Order"),
    ("research_disclosure_view","Saw the debrief"),
]

# Human labels for the in-journey micro-question answers.
LABELS = {
    "why_offer": {"now_certain": "Money off now", "more_later": "More money later", "adds_up": "10% adds up", "wont_return": "Might not order again", "distrust_future": "Don't trust the later one"},
    "why_filter": {"cheapest": "Cheapest", "quickest": "Quickest", "trustable": "Food I trust", "browsing": "Just looking"},
    "why_dish": {"craving": "Craving it", "default": "My usual", "time_of_day": "Time of day", "sharing": "For more than one", "safe": "Safest choice"},
    "why_rest": {"only_place": "Only place that makes it right", "consistent": "It's consistent", "value": "Best value", "fastest": "Fastest / nearest", "habit": "Habit"},
    "app_gap": {"yes_easy": "Yes, it's on my app", "yes_costly": "Yes, but expensive there", "no": "NO — not on my app", "dont_know": "Never checked"},
    "missing_dish": {"other_dish": "Something else here", "other_app": "My usual app", "find_place": "Find a place that makes it", "not_order": "Would not order", "rarely_want": "Only wanted it today"},
    "missing_action": {"other_place": "Another place here", "other_app": "My usual app", "other_food": "Something else here", "not_order": "Would not order"},
    "why_item": {"came_for_it": "What I came for", "bestseller": "Marked bestseller", "price": "Price / discount", "picture": "It looked good", "portion": "Portion looked right"},
    "why_bill": {"cheapest_now": "Cheapest today", "order_often": "Plan pays off", "no_third_sub": "Not a third subscription", "want_cover": "Want the cover", "doubt_refund": "Doubt the refund", "new_app": "Won't commit yet"},
    "why_delivery": {"worth_it": "Sooner is worth it", "not_worth": "Not worth paying", "rider_idea": "Liked the passing rider", "hungry_now": "Want it now", "risk": "Faster felt riskier"},
    "rapido_link_trust": {"nothing": "Nothing", "food_safety": "Sealed and warm", "detour": "Passenger first", "no_tracking": "Tracking", "late_anyway": "Late anyway"},
    "meal_slot": {"breakfast": "Breakfast", "lunch": "Lunch", "evening": "Evening", "dinner": "Dinner", "late_night": "Late night"},
}
QUESTION_TITLES = {
    "why_offer":        "Why that offer?  (asked at the cart, where it is worth real money)",
    "why_filter":       "You filtered by X — what were you hoping to find?",
    "why_item":         "Why that menu item and not another?",
    "why_bill":         "Why that pricing model?",
    "why_delivery":     "Why that delivery option?",
    "rapido_link_trust":"What would worry you about a passing Rapido captain bringing your food?",
    "why_dish":       "Why that dish, right now?",
    "why_rest":       "Why that place for it?",
    "app_gap":        "Can you get that place on the app you use most today?",
    "missing_dish":   "The DISH you wanted is not here — what would you do?",
    "missing_action": "The PLACE you wanted is not here — what would you do?",
    "miss_most":      "Of the places you picked, which would you miss most?",
    "meal_slot":      "When do you usually order it?",
}


def truthy(v):
    return str(v).strip().lower() in ("true", "1", "yes")


def load(paths):
    rows = []
    for p in paths:
        with open(p, encoding="utf-8", errors="replace") as f:
            for r in csv.DictReader(f):
                rows.append(r)
    return rows


def participants(rows):
    """
    Collapse events to one record per participant.

    Exclusions, applied in this order and reported:
      1. is_qa            facilitator previews
      2. is_bot_suspect   automation
      3. no landing_page_view  never reached the manipulated screen
    """
    dropped = Counter()
    by_pid = defaultdict(lambda: {"events": set(), "arm": None, "source": None, "payloads": []})

    for r in rows:
        if truthy(r.get("is_qa")):
            dropped["qa"] += 1
            continue
        if truthy(r.get("is_bot_suspect")):
            dropped["bot"] += 1
            continue
        pid = r.get("anon_visitor_id")
        if not pid:
            dropped["no_id"] += 1
            continue
        rec = by_pid[pid]
        rec["events"].add(r.get("event_name"))
        rec["arm"] = rec["arm"] or r.get("variant_id")
        rec["source"] = rec["source"] or r.get("source")
        try:
            pl = json.loads(r.get("payload_json") or "{}")
        except Exception:
            pl = {}
        rec["payloads"].append((r.get("event_name"), pl))

    # A participant who taps a restaurant card on the home screen has chosen a
    # place WITHOUT ever reaching the place search, so `restaurant_search_selected`
    # never fires for them. Without this synthetic step the place-first route
    # disappears from the funnel entirely.
    for rec in by_pid.values():
        if rec["events"] & {"dish_search_started", "restaurant_search_started"}:
            rec["events"].add("searched")
        if rec["events"] & {"dish_selected", "restaurant_search_selected", "restaurant_card_click"}:
            rec["events"].add("chose")

    keep = {}
    for pid, rec in by_pid.items():
        if "landing_page_view" not in rec["events"]:
            dropped["never_saw_proposition"] += 1
            continue
        keep[pid] = rec
    return keep, dropped


def micro(rec, q_id):
    """The answer this participant gave to one in-journey question, or None."""
    for name, pl in rec["payloads"]:
        if name == "micro_answer" and pl.get("q_id") == q_id:
            return pl.get("answer")
    return None


def qualified(rec):
    """
    PRIMARY METRIC — a named restaurant request.

    Returns (made_request, gap_qualified).

    `gap_qualified` is the stronger form: they submitted a request AND said, at
    the moment they picked the place, that they cannot get it on the app they
    use today. That is an assortment gap named by the person who has it, which
    is the thing this study exists to find. It replaces the old
    is_current_customer flag, which came from a question the v3 journey removed.
    """
    made = any(name == "restaurant_request_submitted" and str(pl.get("restaurant_name", "")).strip()
               for name, pl in rec["payloads"])
    return made, (made and micro(rec, "app_gap") in ("no", "yes_costly"))


# ─────────────────────────── report ───────────────────────────

def report(rows, is_demo=False):
    if is_demo:
        print("=" * 72)
        print("  DUMMY DATA — FABRICATED FOR ILLUSTRATION. NOT A FINDING.")
        print("  Delete this output before entering any real result.")
        print("=" * 72 + "\n")

    keep, dropped = participants(rows)
    print(f"Participants analysed : {len(keep)}")
    if dropped:
        print("Excluded events/records:", dict(dropped))
    print()

    arms = sorted({r["arm"] for r in keep.values() if r["arm"]})
    if not arms:
        print("No arm labels found — nothing to compare."); return

    # ── funnel ──
    print("FUNNEL (participants reaching each step)")
    print(f"{'Step':<34}" + "".join(f"{a:>16}" for a in arms))
    print("-" * (34 + 16 * len(arms)))
    prev = {}
    for ev, label in FUNNEL:
        cells = []
        for a in arms:
            sub = [r for r in keep.values() if r["arm"] == a]
            k = sum(1 for r in sub if ev in r["events"])
            n = len(sub)
            pt, lo, hi = wilson(k, n)
            cells.append(f"{k}/{n} ({pt:.0f}%)" if pt is not None else "—")
        print(f"{label:<34}" + "".join(f"{c:>16}" for c in cells))
    print()

    # ── primary ──
    print("PRIMARY METRIC — Restaurant Request Rate (named restaurant submitted)")
    counts = {}
    for a in arms:
        sub = [r for r in keep.values() if r["arm"] == a]
        k = sum(1 for r in sub if qualified(r)[0])
        counts[a] = (k, len(sub))
        pt, lo, hi = wilson(k, len(sub))
        print(f"  {a:<14} {k}/{len(sub)} = {pt:5.1f}%   95% CI {lo:5.1f}–{hi:.1f}")
    print()
    print("  Of those, the GAP-QUALIFIED form — requested a place they said they")
    print("  cannot get, or can only get expensively, on the app they use today:")
    for a in arms:
        sub = [r for r in keep.values() if r["arm"] == a]
        g = sum(1 for r in sub if qualified(r)[1])
        pt, lo, hi = wilson(g, len(sub))
        print(f"  {a:<14} {g}/{len(sub)} = {pt:5.1f}%   95% CI {lo:5.1f}–{hi:.1f}")
    print()

    if len(arms) == 2:
        a1, a2 = arms
        k1, n1 = counts[a1]
        k2, n2 = counts[a2]
        diff, lo, hi = newcombe_diff(k1, n1, k2, n2)
        p = fisher_exact(k1, n1 - k1, k2, n2 - k2)
        print(f"COMPARISON  {a1} vs {a2}")
        print(f"  Absolute difference : {diff:+.1f} pp")
        print(f"  95% CI (Newcombe)   : {lo:+.1f} to {hi:+.1f} pp")
        print(f"  Fisher exact p      : {p:.4f}")
        if k2 > 0 and (k2 / n2) >= 0.10:
            print(f"  Relative uplift     : {((k1/n1)/(k2/n2) - 1) * 100:+.0f}%")
        else:
            print("  Relative uplift     : not reported (baseline below 10% — unstable)")
        print()
        print("  DECISION RULES (EXPERIMENT_DESIGN.md §11)")
        if diff is not None:
            if abs(diff) < 10:
                print("   → R2: within ±10 pp. No directional separation at this size.")
                print("     Do not choose between the framings on this evidence. Escalate to n ≥ 200.")
            elif diff >= 15:
                print(f"   → R1: {a1} leads by ≥15 pp. Directional support for prioritising it.")
            elif diff <= -15:
                print(f"   → R1/R3: {a2} leads by ≥15 pp.")
            else:
                print("   → Between 10 and 15 pp: suggestive, below the pre-set threshold. Treat as R2.")
        print()

    # ── H5: click vs qualified ──
    print("H5 — does a tap overstate interest?")
    print("  (a tap costs nothing; naming a place you actually use costs recall and effort)")
    for a in arms:
        sub = [r for r in keep.values() if r["arm"] == a]
        taps = sum(1 for r in sub if "first_meaningful_tap" in r["events"])
        reqs = sum(1 for r in sub if qualified(r)[0])
        ratio = (reqs / taps) if taps else None
        flag = "  <- R4: taps are curiosity, not intent" if ratio is not None and ratio < 0.35 else ""
        print(f"  {a:<14} tap -> request = {reqs}/{taps} = "
              + (f"{ratio:.2f}{flag}" if ratio is not None else "—"))
    print()

    # ── the artifact ──
    print("REQUESTED RESTAURANTS (the operational output — valuable regardless of H1)")
    names = Counter()
    for r in keep.values():
        for ev, pl in r["payloads"]:
            if ev == "restaurant_request_submitted":
                for nm in str(pl.get("restaurant_name", "")).split("|"):
                    nm = nm.strip()
                    if nm:
                        names[nm] += 1
    if names:
        for nm, c in names.most_common(20):
            share = 100 * c / len(keep)
            flag = "   ← R8: requested by ≥20% — onboard first" if share >= 20 else ""
            print(f"  {c:>3}  ({share:4.1f}%)  {nm}{flag}")
    else:
        print("  none recorded")
    print()
    # ── what people searched for ──
    # ══ the two search streams — the reason this study exists ══
    print("=" * 72)
    print("WHAT KIND OF FOOD, AND WHAT KIND OF PLACE")
    print("=" * 72)
    cuisine, restkind, restcat = Counter(), Counter(), Counter()
    first_box = Counter()
    for r in keep.values():
        for ev, pl in r["payloads"]:
            if ev == "dish_selected" and pl.get("category"):
                cuisine[pl["category"]] += 1
            if ev == "restaurant_search_selected":
                if pl.get("rest_kind"):
                    restkind[pl["rest_kind"]] += 1
                if pl.get("category"):
                    restcat[pl["category"]] += 1
            if ev == "first_meaningful_tap" and pl.get("tap_kind"):
                first_box[pl["tap_kind"]] += 1
    def block(title, c, note=""):
        tot = sum(c.values())
        print(f"\n{title}   (n = {tot})")
        if not tot:
            print("  none recorded"); return
        for k, v in c.most_common():
            pt, lo, hi = wilson(v, tot)
            print(f"  {v:>3}  {pt:>5.1f}%  [{lo:.0f}–{hi:.0f}]  {k}")
        if note:
            print("  " + note)
    block("CUISINE TYPE SEARCHED FOR", cuisine)
    block("RESTAURANT TYPE CHOSEN", restkind,
          "→ local vs chain is the case study's central question, read off behaviour.")
    block("RESTAURANT CATEGORY CHOSEN", restcat)
    # ── every query typed, including the abandoned ones ──
    qd, qr, zerod, zeror = Counter(), Counter(), Counter(), Counter()
    for r in keep.values():
        for ev, pl in r["payloads"]:
            if ev != "search_query":
                continue
            q = str(pl.get("query", "")).strip().lower()
            if not q:
                continue
            n0 = str(pl.get("results_count", "")).strip() in ("0", "0.0")
            if pl.get("source_screen") == "dish":
                qd[q] += 1
                if n0:
                    zerod[q] += 1
            else:
                qr[q] += 1
                if n0:
                    zeror[q] += 1

    print("\nEVERY QUERY TYPED   (logged on pause, so abandoned searches survive)")
    for title, c in [("in the DISH box", qd), ("in the RESTAURANT box", qr)]:
        print(f"\n  {title} — {sum(c.values())} queries, {len(c)} distinct")
        for k, v in c.most_common(15):
            print(f"    {v:>3}  {k}")
        if not c:
            print("    none recorded")

    print("\n" + "=" * 72)
    print("SEARCHES THAT FOUND NOTHING — the demand we cannot serve")
    print("=" * 72)
    for title, c, tot in [("DISHES we do not have", zerod, sum(qd.values())),
                          ("PLACES we do not have", zeror, sum(qr.values()))]:
        print(f"\n  {title} — {sum(c.values())} of {tot} queries returned zero")
        for k, v in c.most_common(20):
            print(f"    {v:>3}  {k}")
        if not c:
            print("    none")
    print("\n  → These two lists are the operational output of the whole study. A dish")
    print("    nobody can find is a MENU problem; a place nobody can find is an")
    print("    ONBOARDING problem. `missing_dish` and `missing_action` say which of")
    print("    them actually costs an order and which just costs a choice.")
    print("  → Cross-check every name against Ownly's live Gachibowli catalogue before")
    print("    acting: a zero result here may mean we did not stock it in the prototype,")
    print("    not that Ownly does not have it.")
    print()

    block("WHICH BOX THEY REACHED FOR FIRST", first_box,
          "→ `restaurant_search` = place-first thinking; `dish`/`search` = dish-first.\n"
          "    This decides what the home screen should lead with.")
    print()

    print("DISH SEARCHES  (nothing in the survey ever asked what people want to EAT)")
    dq, dsel = Counter(), Counter()
    rq = Counter()
    for r in keep.values():
        for ev, pl in r["payloads"]:
            if ev == "dish_selected":
                if pl.get("dish"): dsel[str(pl["dish"]).strip().lower()] += 1
                if pl.get("query"): dq[str(pl["query"]).strip().lower()] += 1
            if ev in ("restaurant_search_selected", "restaurant_request_submitted"):
                q = pl.get("query") or pl.get("restaurant_query")
                if q: rq[str(q).strip().lower()] += 1
    if dsel:
        print("  dish chosen:")
        for k, c in dsel.most_common(12): print(f"    {c:>3}  {k}")
    if dq:
        print("  raw dish queries typed:")
        for k, c in dq.most_common(12): print(f"    {c:>3}  {k}")
    if rq:
        print("  raw restaurant queries typed:")
        for k, c in rq.most_common(12): print(f"    {c:>3}  {k}")
    if not (dsel or dq or rq): print("  none recorded")
    print()

    # ── off-frame requests: the supply gap, named by the people who want it ──
    print("DISHES ASKED FOR THAT WE DO NOT LIST")
    md = Counter()
    n_md = 0
    for r in keep.values():
        had = False
        for ev, pl in r["payloads"]:
            if ev == "dish_added_custom" and str(pl.get("dish", "")).strip():
                md[str(pl["dish"]).strip()] += 1
                had = True
        if had:
            n_md += 1
    if md:
        pt, lo, hi = wilson(n_md, len(keep))
        print(f"  {n_md} of {len(keep)} participants ({pt:.1f}%, 95% CI {lo:.1f}-{hi:.1f}) "
              f"asked for a dish we do not list")
        for k, v in md.most_common(20):
            print(f"    {v:>3}  {k}")
    else:
        print("  none recorded")
    print()

    print("PLACES REQUESTED THAT ARE NOT IN OUR AUDIT FRAME")
    print("  (the audit found 88.9% catalogue overlap — these are the other 11%)")
    custom = Counter()
    n_with_custom = 0
    for r in keep.values():
        had = False
        for ev, pl in r["payloads"]:
            if ev == "restaurant_added_custom":
                nm = str(pl.get("restaurant_name", "")).strip()
                if nm:
                    custom[nm] += 1; had = True
        if had:
            n_with_custom += 1
    if custom:
        pt, lo, hi = wilson(n_with_custom, len(keep))
        print(f"  {n_with_custom} of {len(keep)} participants ({pt:.1f}%, 95% CI {lo:.1f}-{hi:.1f}) "
              f"named at least one place we do not stock")
        for nm, c in custom.most_common(20):
            print(f"    {c:>3}  {nm}")
        print("  → Cross-check each against Ownly's live Gachibowli catalogue before acting (rule R7).")
    else:
        print("  none recorded — every request came from the shown list")
    print()

    # ── the within-subject revealed preference ──
    print("FIRST MEANINGFUL TAP  (offer pull vs assortment pull, WITHIN each person)")
    ft = Counter()
    for r in keep.values():
        for ev, pl in r["payloads"]:
            if ev == "first_meaningful_tap":
                ft[pl.get("tap_kind", "?")] += 1
                break
    tot = sum(ft.values())
    if tot:
        for k, c in ft.most_common():
            print(f"    {k:<14} {c:>3}  ({100*c/tot:4.1f}%)")
        print("    This does not depend on the between-arms comparison, so it is the")
        print("    one contrast this sample size can actually speak to.")
    else:
        print("    none recorded")
    print()

    # ══════════════════════════════════════════════════════════════════
    #  THE CHECKOUT — the two choices nothing else in the project tests
    # ══════════════════════════════════════════════════════════════════
    print("=" * 72)
    print("CHECKOUT: HOW PEOPLE WANT TO BE CHARGED, AND HOW DELIVERED")
    print("=" * 72)

    BILL_LABEL = {
        "per_order":  "Pay per order · ₹15 a time        (cheapest today)",
        "membership": "Ownly Plus · ₹99/month            (a THIRD subscription)",
        "protected":  "Order Protection · price randomised (buys a refund guarantee)",
    }
    DEL_LABEL = {
        "standard":    "Standard · 42 min · free",
        "rapido_link": "Rapido Link · 25 min · paid  (17 min saved, price randomised per person)",
    }

    def final_choice(rec, ev_name, key):
        """The LAST option a participant settled on, not the first one they tried."""
        val = None
        for name, pl in rec["payloads"]:
            if name == ev_name and pl.get(key):
                val = pl[key]
        return val

    OFFER_LABEL = {
        "flat100": "₹100 off this order              (cash NOW, certain)",
        "wallet":  "₹X into Ownly Money, next order  (MORE cash, one order away)",
        "recur10": "10% off every order for 30 days  (recurring, self-applying)",
    }

    for title, ev_name, key, labels in [
        ("OFFER APPLIED", "offer_applied", "offer", OFFER_LABEL),
        ("PRICING MODEL CHOSEN", "bill_option_chosen", "bill_id", BILL_LABEL),
        ("DELIVERY OPTION CHOSEN", "delivery_option_chosen", "delivery_id", DEL_LABEL),
    ]:
        c = Counter()
        for r in keep.values():
            v = final_choice(r, ev_name, key)
            if v:
                c[v] += 1
        n = sum(c.values())
        print(f"\n{title}   (n = {n} who made a choice)")
        if not n:
            print("  none recorded")
            continue
        for v, k in c.most_common():
            pt, lo, hi = wilson(k, n)
            print(f"  {k:>3}  {pt:5.1f}%  [{lo:.0f}–{hi:.0f}]  {labels.get(v, v)}")
        if ev_name == "offer_applied":
            print("  → All three sit against the participant's OWN basket with their real rupee")
            print("    value on screen, so this is a priced choice, not a stated preference.")
            print("  → All three are offer types Indian delivery apps actually run, and none")
            print("    asks the participant to remember anything or predict their own future.")
            print("    NO COUPON TOUCHES DELIVERY, so this cannot cancel the delivery decision.")
            # did they explain the offer they actually kept?
            mism = 0
            for r in keep.values():
                final = final_choice(r, "offer_applied", "offer")
                why = None
                for n2, pl in r["payloads"]:
                    if n2 == "micro_answer" and pl.get("q_id") == "why_offer":
                        why = pl.get("detail")
                if final and why and final != why:
                    mism += 1
            if mism:
                print(f"  → CAUTION: {mism} participant(s) explained one offer then switched to")
                print("    another. `why_offer` fires on the FIRST application, so for those")
                print("    people the reason and the final choice describe different offers.")
                print("    Exclude them from the why_offer read, or report both.")
        if ev_name == "bill_option_chosen":
            print("  → This is a WITHIN-SUBJECT choice: everyone who reached the cart answered it,")
            print("    so unlike the between-arms contrast it is not destroyed by n = 40.")
            print("  → `[AUDIT]` Ownly charged ZERO on 8 of 8 captures; fee load 5.2% vs an")
            print("    incumbent median of 23.4%. This asks what people accept instead.")
            print("  → `protected` is the one nothing has ever priced. `[GACH]` Q26 put a quick")
            print("    refund promise 2nd (6 of 23) behind price (8) and at 3x a first-order")
            print("    discount (2). `[PUBLIC]` refund delay/denial is in 43% of 37 reviews at")
            print("    mean severity 3.31 — the highest-severity theme in the corpus. Its price")
            print("    is RANDOMISED, so see the curve below rather than this single rate.")
            print("  → `membership` asks whether there is room for a THIRD subscription:")
            print("    `[GACH]` 82.5% (33/40) already hold Swiggy One and/or Zomato Gold, and")
            print("    a membership alone flips 1 of 4 audited baskets away from Ownly.")
        if ev_name == "delivery_option_chosen":
            rl = c.get("rapido_link", 0)
            if n:
                pt, lo, hi = wilson(rl, n)
                print(f"  → RAPIDO LINK TAKE-UP: {rl}/{n} = {pt:.1f}% (95% CI {lo:.1f}–{hi:.1f})")
                print("    Standard is free at 42 min; Rapido Link saves 17 min for a price that")
                print("    was RANDOMISED per participant. The take-up rate at each price is the")
                print("    demand curve below — a single take-up number here means nothing on its own.")

    # ── the demand curve for 17 minutes ──
    by_price = defaultdict(lambda: [0, 0])          # price -> [took_fast, n]
    for r in keep.values():
        price = None
        for name, pl in r["payloads"]:
            if pl.get("rl_price"):
                price = int(pl["rl_price"])
        if price is None:
            continue
        final = final_choice(r, "delivery_option_chosen", "delivery_id") or "standard"
        by_price[price][1] += 1
        if final == "rapido_link":
            by_price[price][0] += 1
    if by_price:
        print("\nWILLINGNESS TO PAY FOR 17 MINUTES   (price randomised between participants)")
        print(f"  {'price':>7} {'took it':>9} {'rate':>7}   {'95% CI':>12}")
        for price in sorted(by_price):
            k, n = by_price[price]
            pt, lo, hi = wilson(k, n)
            bar = "█" * int(round((pt or 0) / 6))
            print(f"  {'₹'+str(price):>7} {str(k)+'/'+str(n):>9} {pt:>6.1f}%   {lo:>5.0f}–{hi:<5.0f} {bar}")
        print("  → Fit the take-up rate against price to get the value of 17 minutes to this")
        print("    sample. `[GACH]` the survey's `tradeoff_eta` found 92.5% would WAIT 15 min")
        print("    longer to save ₹30. If take-up here stays high at ₹30+, the two measures")
        print("    disagree — and the behavioural one was the one that cost something.")
        ns = [n for _, n in by_price.values()]
        if ns and min(ns) < 8:
            print(f"  ⚠ Thinnest price cell is n={min(ns)}. Report the curve as directional only.")

    # ── at what amount does money later beat ₹100 now? ──
    by_wallet = defaultdict(lambda: [0, 0])
    for r in keep.values():
        amt = None
        for name, pl in r["payloads"]:
            if pl.get("wallet_amt"):
                amt = int(pl["wallet_amt"])
        if amt is None:
            continue
        final = final_choice(r, "offer_applied", "offer")
        if not final:
            continue
        by_wallet[amt][1] += 1
        if final == "wallet":
            by_wallet[amt][0] += 1
    if by_wallet:
        print("\nWHEN DOES MONEY LATER BEAT ₹100 NOW?   (wallet amount randomised)")
        print("  ₹100 off today is the fixed comparator in every arm.")
        print(f"  {'wallet':>8} {'chose it':>10} {'rate':>7}   {'95% CI':>12}")
        for amt in sorted(by_wallet):
            k, n = by_wallet[amt]
            pt, lo, hi = wilson(k, n)
            bar = "█" * int(round((pt or 0) / 6))
            print(f"  {'₹'+str(amt):>8} {str(k)+'/'+str(n):>10} {pt:>6.1f}%   {lo:>5.0f}–{hi:<5.0f} {bar}")
        print("  → The amount where this crosses 50% is what one order of delay costs Ownly.")
        print("    If nothing in this range beats ₹100 now, the app has to buy every order")
        print("    outright — which is `[GACH]` the 25% who said they would stay after an")
        print("    intro offer ended, priced in rupees instead of stated on a 5-point scale.")
        ns = [n for _, n in by_wallet.values()]
        if ns and min(ns) < 8:
            print(f"  ⚠ Thinnest cell is n={min(ns)}. Directional only.")

    # ── what is a refund guarantee worth? ──
    by_prot = defaultdict(lambda: [0, 0])
    for r in keep.values():
        price = None
        for name, pl in r["payloads"]:
            if pl.get("protect_price"):
                price = int(pl["protect_price"])
        if price is None:
            continue
        final = final_choice(r, "bill_option_chosen", "bill_id")
        if not final:
            continue
        by_prot[price][1] += 1
        if final == "protected":
            by_prot[price][0] += 1
    if by_prot:
        print("\nWHAT IS A REFUND GUARANTEE WORTH?   (cover price randomised)")
        print(f"  {'cover':>7} {'bought it':>11} {'rate':>7}   {'95% CI':>12}")
        for price in sorted(by_prot):
            k, n = by_prot[price]
            pt, lo, hi = wilson(k, n)
            bar = "█" * int(round((pt or 0) / 6))
            print(f"  {'₹'+str(price):>7} {str(k)+'/'+str(n):>11} {pt:>6.1f}%   {lo:>5.0f}–{hi:<5.0f} {bar}")
        print("  → `[GACH]` a refund promise is the #2 STATED reason people would try Ownly.")
        print("    This is the first time anyone has been asked to pay for it. If take-up")
        print("    collapses at every price, the stated preference is cheap talk. If it holds,")
        print("    reliability cover is a product — and `why_bill` says whether the people who")
        print("    decline do so because their orders arrive fine, or because they do not")
        print("    believe the refund would ever arrive.")
        ns = [n for _, n in by_prot.values()]
        if ns and min(ns) < 8:
            print(f"  ⚠ Thinnest cell is n={min(ns)}. Directional only.")

    # how much the pricing choice was actually worth to them
    deltas = []
    for r in keep.values():
        tot = None
        for name, pl in r["payloads"]:
            if name == "place_order_click" and pl.get("bill_total"):
                tot = pl["bill_total"]
        if tot:
            deltas.append(float(tot))
    if deltas:
        print(f"\nBASKET AT CHECKOUT   n = {len(deltas)}")
        print(f"  median bill  {statistics.median(deltas):.0f}   "
              f"range {min(deltas):.0f}–{max(deltas):.0f}")

    # did they even engage with the choice, or just take the default?
    touched = sum(1 for r in keep.values()
                  if any(n2 == "bill_option_chosen" for n2, _ in r["payloads"]))
    reached = sum(1 for r in keep.values() if "cart_view" in r["events"])
    if reached:
        pt, lo, hi = wilson(touched, reached)
        print(f"\nENGAGEMENT WITH THE PRICING CHOICE")
        print(f"  {touched}/{reached} = {pt:.1f}% (95% CI {lo:.1f}–{hi:.1f}) of people who reached the")
        print("  cart actively changed the pricing model rather than leaving the default.")
        print("  A LOW number here does not mean the default is preferred — it means the")
        print("  choice was not salient, and that is a finding about the screen, not about")
        print("  pricing. Report it before reporting the split above.")
    print()

    # ══════════════════════════════════════════════════════════════════
    #  THE IN-JOURNEY QUESTIONS
    #  Each was asked one tap after the choice it is about, naming that
    #  choice. Nothing here duplicates the survey, the interviews or the
    #  review mining — see EXPERIMENT_DESIGN §13.
    # ══════════════════════════════════════════════════════════════════
    print("=" * 72)
    print("IN-JOURNEY QUESTIONS — asked at the moment of each choice")
    print("=" * 72)

    ans = defaultdict(Counter)
    speed = defaultdict(list)
    for r in keep.values():
        for ev, pl in r["payloads"]:
            if ev != "micro_answer":
                continue
            q = pl.get("q_id")
            if not q:
                continue
            ans[q][pl.get("answer", "?")] += 1
            try:
                speed[q].append(int(pl.get("ms_to_answer") or 0))
            except (TypeError, ValueError):
                pass

    if not ans:
        print("  no answers recorded\n")
    for q in ("why_filter", "why_dish", "why_rest", "app_gap", "missing_action", "why_item",
              "why_offer", "why_bill", "why_delivery", "rapido_link_trust",
              "miss_most", "meal_slot"):
        if q not in ans:
            continue
        c = ans[q]
        tot = sum(c.values())
        answered = tot - c.get("skipped", 0)
        print(f"\n{QUESTION_TITLES.get(q, q)}")
        print(f"  asked {tot}, answered {answered}"
              + (f", median {statistics.median(speed[q])/1000:.1f}s to answer" if speed.get(q) else ""))
        for v, n in c.most_common():
            lab = LABELS.get(q, {}).get(v, v)
            pct = 100 * n / answered if answered and v != "skipped" else None
            pt, lo, hi = wilson(n, answered) if (answered and v != "skipped") else (None, None, None)
            bar = "█" * int(round((pct or 0) / 4))
            line = f"    {n:>3}  " + (f"{pct:5.1f}%" if pct is not None else "   —  ") + f"  {lab}"
            if pt is not None:
                line += f"   [{lo:.0f}–{hi:.0f}]"
            print(line + ("  " + bar if bar else ""))

        # question-specific readings
        if q == "why_offer" and answered:
            durable = c.get("lasts", 0) + c.get("distrust_future", 0)
            print(f"    → {durable}/{answered} answered in terms of whether the offer LASTS.")
            print("      `[GACH]` 87.5% of the surveyed 40 expect a new app's prices to rise.")
            print("      This is the first time that doubt has been measured against real money.")
        if q == "app_gap" and answered:
            gap = c.get("no", 0) + c.get("yes_costly", 0)
            pt, lo, hi = wilson(gap, answered)
            print(f"    → ASSORTMENT GAP RATE: {gap}/{answered} = {pt:.1f}% "
                  f"(95% CI {lo:.1f}–{hi:.1f}) could not get that place on their current app,")
            print("      or could only get it expensively. This is the number the case study's")
            print("      assortment argument stands or falls on.")
        if q == "missing_action" and answered:
            stay = c.get("other_place", 0) + c.get("other_food", 0)
            leave = c.get("other_app", 0) + c.get("not_order", 0)
            pt, lo, hi = wilson(leave, answered)
            print(f"    → ORDER LOST when a wanted place is missing: {leave}/{answered} = {pt:.1f}% "
                  f"(95% CI {lo:.1f}–{hi:.1f})")
            print(f"    → substituted within the app instead:        {stay}/{answered}")
            print("      This is the only measure in the whole project that prices a missing")
            print("      restaurant. Treat it as directional at this sample size.")
        if q == "miss_most":
            print("    → the single place each person would least give up. Onboarding order.")

    print()

    # ── how the dish and the place combine ──
    print("DISH → PLACE PAIRS  (what people want, and where they want it from)")
    pairs = Counter()
    for r in keep.values():
        dish = place = None
        for ev, pl in r["payloads"]:
            if ev == "dish_selected" and pl.get("dish"):
                dish = str(pl["dish"]).strip().lower()
            if ev in ("restaurant_search_selected", "restaurant_card_click") and pl.get("restaurant_name"):
                place = place or str(pl["restaurant_name"]).strip()
        if dish and place:
            pairs[(dish, place)] += 1
    if pairs:
        for (d, pl_), n in pairs.most_common(20):
            print(f"    {n:>3}  {d}  →  {pl_}")
    else:
        print("    none recorded")
    print()

    print("NOTE: segment comparisons are NOT produced here. At n≈40 each segment cell is ~10,")
    print("      which EXPERIMENT_DESIGN.md §12 forbids interpreting. Report composition only.")


def demo_rows():
    """Fabricated events so the whole v4 pipeline can be exercised before real data exists."""
    import random
    random.seed(20260922)
    DISHES = ["chicken biryani", "mutton biryani", "dosa", "pizza", "ice cream",
              "haleem", "paneer butter masala", "burger"]
    PLACES = ["Paradise Biryani", "Bawarchi", "Shah Ghouse", "Mehfil",
              "Cream Stone", "Murgan Tiffins", "Vivaha Bhojanambu", "Karachi Bakery"]
    OFFFRAME = ["Chutneys", "Ulavacharu", "Pista House", "Subbayya Gari Hotel",
                "Rayalaseema Ruchulu"]
    ITEMS = [("Chicken Dum Biryani", 280), ("Mutton Biryani", 360), ("Masala Dosa", 120),
             ("Margherita", 199), ("Death by Chocolate", 190), ("Paneer Butter Masala", 260)]
    rows = []
    plan = {"discount": (20, .60, .45, .55), "restaurants": (20, .65, .55, .30)}
    for arm, (n, explore_p, cart_p, offer_first_p) in plan.items():
        for i in range(n):
            pid = f"{arm}-{i:03d}-0000-0000-000000000000"

            def ev(name, payload=None):
                rows.append({"anon_visitor_id": pid, "variant_id": arm, "source": "demo",
                             "event_name": name, "is_qa": "false", "is_bot_suspect": "false",
                             "payload_json": json.dumps(payload or {})})

            def micro_ev(q, a, sub=""):
                ev("micro_shown", {"q_id": q, "subject": sub})
                ev("micro_answer", {"q_id": q, "answer": a, "subject": sub,
                                    "ms_to_answer": random.randint(1400, 9000)})

            ev("landing_page_view")
            kind = "offer" if random.random() < offer_first_p else random.choice(
                ["restaurant", "category", "filter", "search"])
            ev("first_meaningful_tap", {"tap_kind": kind, "ms_to_first_tap": random.randint(900, 9000)})

            if kind == "offer":
                ev("offer_card_click", {"offer": "d_flat100", "position": 0})
            if kind == "filter":
                f = random.choice(["offers", "fast", "rated"])
                ev("filter_tab_click", {"detail": f})
                micro_ev("why_filter", random.choice(
                    ["cheapest", "cheapest", "quickest", "trustable", "browsing"]), f)

            if random.random() >= explore_p:
                continue

            dish = random.choice(DISHES)
            ev("dish_search_view", {"tap_kind": kind})
            ev("dish_search_started")
            for q in random.sample(["pulihora", "gongura mutton", "ragi sangati", "punugulu",
                                    "bobbatlu", "sakinalu", "biryani", "shawarma"],
                                   random.randint(1, 2)):
                ev("search_query", {"query": q, "results_count": 0 if len(q) > 8 else 3,
                                    "source_screen": "dish"})
                if len(q) > 8 and random.random() < .55:
                    ev("dish_added_custom", {"dish": q, "from_list": False,
                                             "source_screen": "search", "query": q})
                    micro_ev("missing_dish", random.choice(
                        ["other_app", "other_app", "other_dish", "find_place",
                         "not_order", "rarely_want"]), q)
            CU = {"chicken biryani":"Biryani","mutton biryani":"Biryani","dosa":"South Indian",
                  "pizza":"Pizza","ice cream":"Desserts","haleem":"Biryani",
                  "paneer butter masala":"North Indian","burger":"Fast food"}
            ev("dish_selected", {"dish": dish, "query": dish[:5], "typed": True,
                                 "category": CU[dish], "source_screen": "search"})
            micro_ev("why_dish", random.choice(
                ["craving", "default", "default", "time_of_day", "sharing", "safe"]), dish)
            micro_ev("meal_slot", random.choice(
                ["lunch", "dinner", "dinner", "late_night", "evening", "breakfast"]), dish)

            ev("restaurant_search_view", {"dish": dish})
            for q in random.sample(["meghana foods", "chutneys", "ulavacharu", "bawarchi",
                                    "pista house", "subbayya"], random.randint(1, 2)):
                ev("search_query", {"query": q, "results_count": 0 if q not in ("bawarchi",) else 1,
                                    "source_screen": "restaurant"})
            off_frame = random.random() < 0.28
            place = random.choice(OFFFRAME if off_frame else PLACES)
            CHAIN = {"Domino's", "Pizza Hut", "KFC"}
            ev("restaurant_search_selected",
               {"restaurant_name": place, "query": place.split()[0].lower(),
                "dish": dish, "from_list": not off_frame,
                "rest_kind": "chain" if place in CHAIN else "local",
                "category": "Biryani", "source_screen": "search"})
            if off_frame:
                ev("restaurant_added_custom",
                   {"restaurant_name": place, "from_list": False,
                    "source_screen": "restaurant_search", "dish": dish})
                micro_ev("missing_action", random.choice(
                    ["other_app", "other_app", "other_place", "other_food", "not_order"]), place)
                continue
            micro_ev("why_rest", random.choice(
                ["only_place", "consistent", "consistent", "value", "fastest", "habit"]), place)
            micro_ev("app_gap", random.choice(
                ["yes_easy", "yes_easy", "yes_costly", "no", "no", "dont_know"]), place)

            ev("menu_view", {"restaurant_name": place, "dish": dish})
            if random.random() >= cart_p / explore_p:
                continue

            subtotal = 0
            for _ in range(random.randint(1, 3)):
                nm, pr = random.choice(ITEMS)
                subtotal += pr
                ev("item_added", {"item_name": nm, "item_price": pr, "restaurant_name": place})
            micro_ev("why_item", random.choice(
                ["came_for_it", "came_for_it", "bestseller", "price", "picture", "portion"]), nm)
            ev("cart_view", {"restaurant_name": place, "n_selected": 2, "item_price": subtotal})

            # the offer choice — priced against their own basket
            off = ""
            if random.random() < 0.85:
                wamt = random.choice([120, 150, 200, 250])
                # deferred money wins more often as the amount rises
                p_wallet = {120: .10, 150: .22, 200: .38, 250: .52}[wamt]
                roll = random.random()
                off = "wallet" if roll < p_wallet else ("recur10" if roll < p_wallet + .28 else "flat100")
                worth = {"flat100": 100, "recur10": round(subtotal * .10), "wallet": 0}[off]
                ev("offer_applied", {"offer": off, "offer_worth": worth,
                                     "wallet_amt": wamt,
                                     "bill_total": subtotal + 60 - worth,
                                     "item_price": subtotal})
                micro_ev("why_offer", {
                    "flat100": random.choice(["now_certain", "now_certain", "wont_return",
                                              "distrust_future"]),
                    "recur10": "adds_up",
                    "wallet": "more_later"}[off], off)

            # delivery comes first, at a price randomised per participant
            rl = random.choice([15, 25, 35, 49])
            ev("delivery_screen_view", {"restaurant_name": place, "rl_price": rl})
            dly = "standard"
            # take-up falls as the price rises — a real demand curve
            if random.random() < {15: .78, 25: .62, 35: .44, 49: .24}[rl]:
                dly = "rapido_link"
            ev("delivery_option_chosen", {"delivery_id": dly, "mins": 25 if dly == "rapido_link" else 42,
                                          "rl_price": rl})
            micro_ev("why_delivery", random.choice(
                ["worth_it", "hungry_now", "rider_idea", "not_worth", "risk"]), dly)
            if dly == "rapido_link":
                micro_ev("rapido_link_trust", random.choice(
                    ["nothing", "food_safety", "food_safety", "detour", "no_tracking", "late_anyway"]))
            ev("delivery_confirmed", {"delivery_id": dly, "rl_price": rl})

            bill = "per_order"
            if random.random() < 0.80:
                bill = random.choice(["per_order", "per_order", "per_order",
                                      "protected", "protected", "membership"])
                pprice = random.choice([9, 19, 29, 39])
                if bill == "protected" and random.random() > {9: .80, 19: .55, 29: .34, 39: .16}[pprice]:
                    bill = "per_order"
                ev("bill_option_chosen", {"bill_id": bill, "bill_total": subtotal + 60,
                                          "delivery_id": dly, "item_price": subtotal,
                                          "protect_price": pprice})
                micro_ev("why_bill", {
                    "per_order": random.choice(["cheapest_now", "cheapest_now", "new_app",
                                                "no_third_sub", "doubt_refund"]),
                    "membership": random.choice(["order_often", "cheapest_now"]),
                    "protected": random.choice(["want_cover", "want_cover", "cheapest_now"]),
                }[bill], bill)

            ev("place_order_click", {"bill_id": bill, "delivery_id": dly, "offer": off,
                                     "bill_total": subtotal + 60, "item_price": subtotal,
                                     "restaurant_name": place, "dish": dish})
            ev("honest_stop_view", {"furthest_step": "cart"})
            ev("research_disclosure_view")

            if random.random() < 0.4:
                ev("followup_consent_given", {"contact_channel": "in_person"})
    return rows


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--demo" in sys.argv or not args:
        report(demo_rows(), is_demo=True)
    else:
        report(load(args))
