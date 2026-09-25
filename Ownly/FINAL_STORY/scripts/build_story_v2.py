"""
build_story_v2.py - builds Ownly_Story_v2.html, the 7-minute presentation.

Standard library only, like the other scripts here. Every chart is SVG written
by Python: no chart library, no CDN, no external request. Figures are read from
the CSVs in FINAL_STORY/data/ and final_dashboard/data/ wherever one exists, so
a number on screen cannot drift from its source.

Twelve slides, one screen each, keyboard paged.
Run:  python3 scripts/build_story_v2.py
"""
import csv
import os
import statistics as st
from collections import defaultdict
from html import escape as e

HERE = os.path.dirname(os.path.abspath(__file__))
STORY = os.path.dirname(HERE)
ROOT = os.path.dirname(STORY)
OUT = os.path.join(STORY, "Ownly_Story_v2.html")
N_SLIDES = 12

# ---------------------------------------------------------------- palette
# Same tokens as final_dashboard/index.html so the deck and the dashboard read
# as one piece of work. Light only: this is projected, never viewed in dark mode.
INK, MUTED, RULE = "#443533", "#8C7F78", "#D5C9B4"
BLUE, BLUE_LT, CORAL, TAN, GREEN = "#2F6094", "#7FA0C0", "#EF7259", "#C9B79A", "#3F7A5E"


def read(path):
    with open(os.path.join(ROOT, path), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def truthy(v):
    return str(v).strip().lower() in ("true", "1", "yes")


# ================================================================ chart kit
def _svg(w, h, body, label):
    return (f'<svg class="chart" viewBox="0 0 {w} {h}" role="img" aria-label="{e(label)}" '
            f'preserveAspectRatio="xMinYMin meet" xmlns="http://www.w3.org/2000/svg">{body}</svg>')


def _bar(x, y, w, h, fill):
    """Square at the baseline, rounded at the data end."""
    if w <= 0:
        return ""
    r = min(4, h / 2, w)
    return (f'<path d="M{x},{y} h{w - r} a{r},{r} 0 0 1 {r},{r} v{h - 2 * r} '
            f'a{r},{r} 0 0 1 -{r},{r} h-{w - r} z" fill="{fill}"/>')


def _vbar(x, base, w, h, fill):
    if h <= 0:
        return ""
    r = min(4, w / 2, h)
    return (f'<path d="M{x},{base} v-{h - r} a{r},{r} 0 0 1 {r},-{r} h{w - 2 * r} '
            f'a{r},{r} 0 0 1 {r},{r} v{h - r} z" fill="{fill}"/>')


def hbars(items, vmax=100, label_w=200, w=620, row=44, bar_h=18, ci=False, title=""):
    """items: label, value, shown, [sub], [hl], [lo, hi]. One series, emphasis
    colouring: the bar that carries the point is blue, the rest are tan."""
    plot = w - label_w - 66
    h = row * len(items) + 10
    out = []
    for i, it in enumerate(items):
        y = i * row + 6
        bw = max(0, plot * it["value"] / vmax)
        fill = it.get("fill") or (BLUE if it.get("hl") else TAN)
        out.append(f'<text x="{label_w - 14}" y="{y + bar_h - 4}" text-anchor="end" class="rl">{e(it["label"])}</text>')
        if it.get("sub"):
            out.append(f'<text x="{label_w - 14}" y="{y + bar_h + 12}" text-anchor="end" class="sl">{e(it["sub"])}</text>')
        out.append(f'<g><title>{e(it["label"])}: {e(it.get("shown", ""))}</title>'
                   f'<rect x="{label_w}" y="{y - 4}" width="{plot + 60}" height="{row - 6}" fill="transparent"/>'
                   + _bar(label_w, y, bw, bar_h, fill) + "</g>")
        if ci and it.get("lo") is not None:
            x1, x2 = label_w + plot * it["lo"] / vmax, label_w + plot * it["hi"] / vmax
            cy = y + bar_h + 6
            out.append(f'<path d="M{x1:.1f},{cy} H{x2:.1f} M{x1:.1f},{cy - 3} v6 M{x2:.1f},{cy - 3} v6" '
                       f'stroke="{MUTED}" stroke-width="1" fill="none" opacity=".75"/>')
        out.append(f'<text x="{label_w + bw + 10:.1f}" y="{y + bar_h - 4}" class="vl">{e(it.get("shown", ""))}</text>')
    out.append(f'<line x1="{label_w}" y1="0" x2="{label_w}" y2="{h}" stroke="{RULE}" stroke-width="1"/>')
    return _svg(w, h, "".join(out), title)


def grouped(items, series, vmax=100, label_w=190, w=620, row=52, bar_h=15, title=""):
    """Two bars per row. series = [(name, colour), (name, colour)]; each item
    carries a[], shown_a, b, shown_b."""
    plot = w - label_w - 66
    top = 26
    h = top + row * len(items) + 8
    out = []
    for i, (name, col) in enumerate(series):
        lx = label_w + i * 200
        out.append(f'<rect x="{lx}" y="4" width="11" height="11" rx="2" fill="{col}"/>'
                   f'<text x="{lx + 17}" y="14" class="lg">{e(name)}</text>')
    for i, it in enumerate(items):
        y = top + row * i + 4
        out.append(f'<text x="{label_w - 14}" y="{y + bar_h - 3}" text-anchor="end" class="rl">{e(it["label"])}</text>')
        if it.get("sub"):
            out.append(f'<text x="{label_w - 14}" y="{y + bar_h + 13}" text-anchor="end" class="sl">{e(it["sub"])}</text>')
        for j, key in enumerate(("a", "b")):
            bw = max(0, plot * it[key] / vmax)
            yy = y + j * (bar_h + 4)
            out.append(f'<g><title>{e(series[j][0])}: {e(it["shown_" + key])}</title>'
                       + _bar(label_w, yy, bw, bar_h, series[j][1]) + "</g>")
            out.append(f'<text x="{label_w + bw + 9:.1f}" y="{yy + bar_h - 3}" class="vl'
                       f'{" lt" if j else ""}">{e(it["shown_" + key])}</text>')
    out.append(f'<line x1="{label_w}" y1="{top - 6}" x2="{label_w}" y2="{h}" stroke="{RULE}" stroke-width="1"/>')
    return _svg(w, h, "".join(out), title)


def dumbbell(rows, vmax, series_a, series_b, label_w=168, w=620, row_h=66, title=""):
    """One row per measure, two dots joined by a rule. Series A is the subject
    (dark), series B the comparison (light). Values are direct-labelled."""
    plot = w - label_w - 56
    top = 36
    h = top + row_h * len(rows) + 32
    x = lambda v: label_w + plot * v / vmax
    out = []
    for i, (name, fill) in enumerate(((series_b, BLUE_LT), (series_a, BLUE))):
        lx = label_w + i * 206
        out.append(f'<circle cx="{lx + 6}" cy="10" r="6" fill="{fill}"/>'
                   f'<text x="{lx + 20}" y="14" class="lg">{e(name)}</text>')
    for g in range(0, int(vmax) + 1, 20):
        gx = x(g)
        out.append(f'<line x1="{gx:.1f}" y1="{top - 8}" x2="{gx:.1f}" y2="{h - 24}" stroke="{RULE}" stroke-width="1"/>'
                   f'<text x="{gx:.1f}" y="{h - 8}" class="ax" text-anchor="middle">{g}%</text>')
    for i, r in enumerate(rows):
        cy = top + row_h * i + row_h / 2 - 6
        xa, xb = x(r["a"]), x(r["b"])
        out.append(f'<text x="{label_w - 16}" y="{cy + 5}" class="rl" text-anchor="end">{e(r["label"])}</text>')
        out.append(f'<line x1="{min(xa, xb):.1f}" y1="{cy}" x2="{max(xa, xb):.1f}" y2="{cy}" stroke="{TAN}" stroke-width="3"/>')
        out.append(f'<g><title>{e(series_b)}: {e(r["b_note"])}</title><circle cx="{xb:.1f}" cy="{cy}" r="8" fill="{BLUE_LT}"/></g>')
        out.append(f'<g><title>{e(series_a)}: {e(r["a_note"])}</title><circle cx="{xa:.1f}" cy="{cy}" r="8" fill="{BLUE}"/></g>')
        out.append(f'<text x="{xa - 14:.1f}" y="{cy + 5}" class="vl" text-anchor="end">{r["a"]:g}%</text>')
        out.append(f'<text x="{xb + 14:.1f}" y="{cy + 5}" class="vl lt">{r["b"]:g}%</text>')
        out.append(f'<text x="{label_w - 16}" y="{cy + 21}" class="sl" text-anchor="end">{e(r["sub"])}</text>')
    return _svg(w, h, "".join(out), title)


def columns(items, vmax, w=440, h=236, title=""):
    """Vertical columns: used for the price ladder, where the x axis is money."""
    left, base, top = 40, h - 42, 24
    span = (w - left - 18) / len(items)
    bw = min(58, span - 18)
    out = [f'<line x1="{left - 6}" y1="{base}" x2="{w - 10}" y2="{base}" stroke="{RULE}" stroke-width="1"/>']
    for i, it in enumerate(items):
        x = left + span * i + (span - bw) / 2
        bh = (base - top) * it["value"] / vmax
        out.append(f'<g><title>{e(it["label"])}: {e(it["shown"])}</title>'
                   + _vbar(x, base, bw, bh, it.get("fill", BLUE)) + "</g>")
        out.append(f'<text x="{x + bw / 2:.1f}" y="{base - bh - 8:.1f}" class="vl" text-anchor="middle">{e(it["shown"])}</text>')
        out.append(f'<text x="{x + bw / 2:.1f}" y="{base + 16}" class="rl" text-anchor="middle">{e(it["label"])}</text>')
        out.append(f'<text x="{x + bw / 2:.1f}" y="{base + 30}" class="sl" text-anchor="middle">{e(it["sub"])}</text>')
    return _svg(w, h, "".join(out), title)


def staircase(points, w=430, h=232, title=""):
    """Cumulative share that would switch at each rupee level."""
    left, right, base, top = 44, w - 14, h - 34, 20
    xs = [left + (right - left) * i / (len(points) - 1) for i in range(len(points))]
    ys = [base - (base - top) * p["pct"] / 100 for p in points]
    out = []
    for g in (0, 25, 50, 75, 100):
        gy = base - (base - top) * g / 100
        out.append(f'<line x1="{left}" y1="{gy:.1f}" x2="{right}" y2="{gy:.1f}" stroke="{RULE}" stroke-width="1"/>'
                   f'<text x="{left - 8}" y="{gy + 4:.1f}" class="ax" text-anchor="end">{g}%</text>')
    d = " ".join(f'{"M" if i == 0 else "L"}{x:.1f},{y:.1f}' for i, (x, y) in enumerate(zip(xs, ys)))
    out.append(f'<path d="{d}" fill="none" stroke="{BLUE}" stroke-width="2"/>')
    for i, p in enumerate(points):
        hl = p.get("hl")
        out.append(f'<g><title>{e(p["label"])}: {e(p["shown"])}</title>'
                   f'<circle cx="{xs[i]:.1f}" cy="{ys[i]:.1f}" r="{6 if hl else 4.5}" fill="{CORAL if hl else BLUE}" '
                   f'stroke="#FBF8F1" stroke-width="2"/></g>')
        out.append(f'<text x="{xs[i]:.1f}" y="{base + 16}" class="sl" text-anchor="middle">{e(p["label"])}</text>')
        if hl:
            out.append(f'<text x="{xs[i]:.1f}" y="{ys[i] - 12:.1f}" class="vl hl" text-anchor="middle">{e(p["shown"])}</text>')
    return _svg(w, h, "".join(out), title)


def waterfall(items, w=470, h=250, title=""):
    """Money left on the table at each checkout stage. One negative bar."""
    left, base, top = 44, h - 46, 26
    span = (w - left - 16) / len(items)
    bw = min(66, span - 22)
    vmax = max(abs(i["value"]) for i in items)
    zero = base - 46  # room for the negative bar below the baseline
    out = [f'<line x1="{left - 8}" y1="{zero}" x2="{w - 10}" y2="{zero}" stroke="{INK}" stroke-width="1"/>']
    for i, it in enumerate(items):
        x = left + span * i + (span - bw) / 2
        bh = (zero - top) * abs(it["value"]) / vmax
        if it["value"] >= 0:
            out.append(_vbar(x, zero, bw, bh, BLUE))
            ly = zero - bh - 8
        else:
            r = min(4, bw / 2)
            bh = min(bh, base - zero - 14)
            out.append(f'<path d="M{x},{zero} v{bh - r} a{r},{r} 0 0 0 {r},{r} h{bw - 2 * r} '
                       f'a{r},{r} 0 0 0 {r},-{r} v-{bh - r} z" fill="{CORAL}"/>')
            ly = zero + bh + 15
        out.append(f'<text x="{x + bw / 2:.1f}" y="{ly:.1f}" class="vl{" neg" if it["value"] < 0 else ""}" '
                   f'text-anchor="middle">{e(it["shown"])}</text>')
        out.append(f'<text x="{x + bw / 2:.1f}" y="{base + 14}" class="rl" text-anchor="middle">{e(it["label"])}</text>')
        out.append(f'<text x="{x + bw / 2:.1f}" y="{base + 28}" class="sl" text-anchor="middle">{e(it["sub"])}</text>')
    return _svg(w, h, "".join(out), title)


# ================================================================ html kit
def tiles(items, cls=""):
    t = []
    for it in items:
        col = it.get("tone", "")
        t.append(f'<div class="tile"><div class="tv {col}">{it["v"]}</div>'
                 f'<div class="tl2">{e(it["label"])}</div><div class="ts">{e(it.get("sub", ""))}</div></div>')
    return f'<div class="tiles {cls}">{"".join(t)}</div>'


def fig(caption, body, cap=None, cls=""):
    c = f'<p class="cap">{cap}</p>' if cap else ""
    return f'<figure class="{cls}"><figcaption>{e(caption)}</figcaption>{body}{c}</figure>'


def slide(n, kick, h1, lede, body, foot="Ownly · Gachibowli"):
    l = f'<p class="lede">{lede}</p>' if lede else ""
    return (f'<section id="s{n}"><p class="kick">{n:02d} · {e(kick)}</p><h1>{h1}</h1>{l}{body}'
            f'<footer class="pg"><span>{e(foot)}</span><span>{n} / {N_SLIDES}</span></footer></section>')


# ================================================================ slides
def s1_problem():
    city = read("FINAL_STORY/data/s1_city.csv")
    tl = read("FINAL_STORY/data/s1_timeline.csv")

    def pct(measure, city_name):
        r = next(x for x in city if x["Measure"] == measure and x["City"] == city_name)
        return float(r["Pct"]), f'{r["Yes"]} of {r["Base"]}'

    rows = []
    for measure, label in (("Heard of Ownly", "Heard of Ownly"),
                           ("Opened Ownly", "Opened the app"),
                           ("Ordered on Ownly", "Ordered on it")):
        a, a_note = pct(measure, "Gachibowli")
        b, b_note = pct(measure, "Bengaluru")
        rows.append({"label": label, "a": a, "b": b, "a_note": a_note, "b_note": b_note,
                     "sub": f"{a_note} here · {b_note} there"})

    li = "".join(f'<li{" class=hyd" if "Hyderabad" in t["Event"] else ""}>'
                 f'<span class="when">{e(t["When"])}</span><span class="what">{e(t["Event"])}</span></li>' for t in tl)

    body = f"""
  <div class="two">
    {fig("How Ownly won Bengaluru", f'<ol class="tl">{li}</ol>')}
    {fig("The same app, two cities",
         dumbbell(rows, 80, "Gachibowli catchment (40)", "Bengaluru (16)", title="Ownly funnel in two cities"),
         "Our survey, Sep 2026. Bengaluru is 16 people — direction, not size.")}
  </div>
  {tiles([
      {"v": "1,000+", "label": "restaurants threatened to quit Swiggy and Zomato in Bengaluru",
       "sub": "Nothing like it has happened in Hyderabad"},
      {"v": "221", "label": "restaurants already listed on Ownly at our Gachibowli address",
       "sub": "Supply is here. Demand is the question"},
      {"v": "0 of 326", "label": "orders our respondents placed in four weeks were on Ownly",
       "sub": "Swiggy 178 · Zomato 120 · other 28", "tone": "bad"}])}"""
    return slide(1, "The problem", "Will Ownly's Bengaluru playbook work in Gachibowli?",
                 "Ownly is already live here, so the question is not whether to enter. It is "
                 "<b>which parts of the playbook still work</b> — and what has to change first.", body)


def s2_bengaluru():
    """Bengaluru is the control group: same app, 18 months ahead."""
    R = read("final_dashboard/data/survey_all_rows_with_flags.csv")
    blr = [r for r in R if "Bengaluru" in r["city"] and truthy(r["age_eligible"])]
    hyd = [r for r in R if truthy(r["age_eligible"]) and truthy(r["in_catchment"])]

    def top2(rows, col, vals):
        a = [r for r in rows if r[col]]
        k = sum(1 for r in a if r[col] in vals)
        return 100 * k / len(a), f"{k} of {len(a)}"

    def food(rows):
        u = [r for r in rows if r["rapido_food_seen"] and r["rapido_food_seen"] != "I don't use the Rapido app"]
        k = sum(1 for r in u if r["rapido_food_seen"] == "Yes")
        return 100 * k / len(u), f"{k} of {len(u)}"

    def trade(rows, col):
        a = [r for r in rows if r[col] != ""]
        k = sum(1 for r in a if truthy(r[col]))
        return 100 * k / len(a), f"{k} of {len(a)}"

    items = []
    for label, sub, fb, fh in (
            ("Expect prices to rise", "agree or strongly agree", top2(blr, "durability_doubt", {"Agree", "Strongly agree"}), top2(hyd, "durability_doubt", {"Agree", "Strongly agree"})),
            ("Would stay after the offer", "definitely or probably", top2(blr, "repeat_no_promo", {"Definitely", "Probably"}), top2(hyd, "repeat_no_promo", {"Definitely", "Probably"})),
            ("Noticed food in Rapido", "Rapido users only", food(blr), food(hyd)),
            ("Give up usual restaurants", "for ₹30 off", trade(blr, "rest_chose_cheap"), trade(hyd, "rest_chose_cheap"))):
        items.append({"label": label, "sub": sub, "a": fh[0], "b": fb[0],
                      "shown_a": f"{fh[0]:.0f}%", "shown_b": f"{fb[0]:.0f}%"})

    chart = grouped(items, [("Gachibowli (40)", BLUE), ("Bengaluru (16)", BLUE_LT)], label_w=204,
                    title="What changes with 18 months of exposure, and what does not")

    cards = "".join(f'<div class="card"><div class="ch">{e(h)}</div><div class="cb">{e(b)}</div></div>'
                    for h, b in (("Offers ended", "2 of the 4 order less now because the discounts stopped"),
                                 ("Late or failed deliveries", "1 stopped after orders went wrong"),
                                 ("Went back to the membership", "1 returned to Swiggy One / Zomato Gold"),
                                 ("Would not miss it", "3 of 4 said they'd be “not disappointed” if Ownly vanished")))

    body = f"""
  <div class="two">
    {fig("The four Bengaluru users who tried it", f'<div class="cards2">{cards}</div>',
         "Four people — counts, not rates. Asked what would bring them back: more offers (2), "
         "faster delivery (1), a bigger price gap (1). None said the product.")}
    {fig("Bengaluru versus Gachibowli", chart,
         "Exposure lifts repeat intent and Rapido discovery. It does not buy belief in the price.")}
  </div>
  {tiles([
      {"v": "2.1%", "label": "of Bengaluru orders in four weeks were on Ownly", "sub": "3 of 146 orders, 18 months in", "tone": "bad"},
      {"v": "₹50", "label": "median saving a Bengaluru user needs to switch main app", "sub": "₹30 in Gachibowli — Hyderabad is cheaper to win"},
      {"v": "4 of 6", "label": "who knew Ownly but never opened it said “just haven't got around to it”",
       "sub": "Inertia, not rejection"}])}"""
    return slide(2, "The control group", "Bengaluru is what Gachibowli looks like in 18 months.",
                 "Same app, restaurant problem already solved. <b>Awareness converted. Ordering did not.</b>", body)


def s3_kpis():
    rows = [r for r in read("final_dashboard/data/kpi_table.csv") if truthy(r["is_headline"])]
    instrument = {
        "NS": "Ownly transaction logs", "K1a": "Price audit · 4 matched baskets",
        "K13": "Survey · 33 named a figure", "K4": "Price audit · 10-restaurant frame",
        "K7": "Price audit · 39 ETA captures", "K9": "Survey · 33 Rapido users",
        "K18": "Survey · 40 respondents", "K23": "Ownly per-order economics",
    }
    why = {
        "NS": "Repeat orders are the only proof the model works. Only Rapido can see them.",
        "K1a": "Does Ownly actually cost less at the checkout, basket by basket?",
        "K13": "The price of a switch. Below it, nothing moves.",
        "K4": "A missing restaurant is the biggest reason an order is lost.",
        "K7": "Seventeen minutes slower is what the cheaper bill costs you.",
        "K9": "Rapido is the one channel rivals cannot copy. Is anyone seeing it?",
        "K18": "Trial is easy to buy. This is whether it survives the offer ending.",
        "K23": "Whether a repeat order makes money, which decides if any of this scales.",
    }
    cards = []
    for r in rows:
        done = "NOT COMPUTABLE" not in r["status"]
        val = f'{r["value"]}<span class="u">{e(r["unit"])}</span>' if done else "—"
        fam = r["family"].split("·")[-1].strip()
        cards.append(
            f'<div class="kpi{"" if done else " off"}">'
            f'<div class="kv">{val}</div>'
            f'<div class="kn">{e(fam)}</div>'
            f'<div class="km">{e(instrument.get(r["kpi_id"], ""))}</div>'
            f'<div class="kw">{e(why.get(r["kpi_id"], ""))}</div>'
            f'<div class="kb">{"MEASURED" if done else "NEEDS RAPIDO DATA"}</div></div>')

    body = f"""
  <div class="kpigrid">{"".join(cards)}</div>
  {tiles([
      {"v": "6 of 8", "label": "KPI families we could measure with outside-in evidence",
       "sub": "Price, switching price, coverage, delivery gap, Rapido discovery, repeat intent"},
      {"v": "2", "label": "need Ownly's own transaction data and cost per order",
       "sub": "Retained orders per user, and margin per repeat order", "tone": "warn"},
      {"v": "10", "label": "marketing metrics built on top of them",
       "sub": "Led by switch-threshold coverage: 81% → 56% → 27%"}])}"""
    return slide(3, "The KPI system", "Eight things decide this business. We could measure six.",
                 "One north-star and seven drivers. <b>Each one names the instrument that produced it</b> — "
                 "and the two we cannot compute are stated, not hidden.", body)


def s4_evidence():
    funnel = [
        {"label": "Responses received", "value": 124, "shown": "124", "sub": "16–19 Sep 2026", "hl": True},
        {"label": "Hyderabad branch", "value": 78, "shown": "78", "sub": "20 Bengaluru · 26 other cities"},
        {"label": "Passed the age screen", "value": 52, "shown": "52", "sub": "20–35 only"},
        {"label": "Gachibowli catchment", "value": 40, "shown": "40", "sub": "34 in Gachibowli itself", "hl": True},
    ]
    inst = [
        {"v": "124", "label": "survey responses", "sub": "51 from Gachibowli · 62 from the catchment"},
        {"v": "70", "label": "fake-door sessions on a working app", "sub": "34 direct · 36 from inside a ride app"},
        {"v": "79", "label": "price captures at one address", "sub": "4 matched three-app baskets"},
        {"v": "836", "label": "reviews, posts and comments coded", "sub": "37 app-store · 524 social · 275 YouTube"},
        {"v": "1", "label": "order we placed and complained about ourselves", "sub": "Receipt, chat and photos kept"},
        {"v": "1", "label": "documented interview transcript", "sub": "Used for mechanism, never for a percentage", "tone": "warn"},
    ]
    body = f"""
  <div class="two">
    {fig("Who we actually asked", hbars(funnel, vmax=124, label_w=186, w=600, row=72, bar_h=26, title="Survey funnel"),
         "Kondapur and Madhapur were options on the form. <b>Nobody picked either.</b>")}
    {fig("Six instruments, and what each produced", tiles(inst, "six"),
         "Every figure in this deck carries its instrument and its base. "
         "Small bases are labelled as direction, not size.")}
  </div>"""
    return slide(4, "The evidence", "Six instruments. Every number carries its base.",
                 "We could not buy data, so we built it: a survey, a price audit at one address, "
                 "<b>a working fake app</b>, coded public reviews, and an order we placed ourselves.", body)


def s5_price():
    pairs = read("final_dashboard/data/audit_pairs.csv")
    cov = read("final_dashboard/data/switch_threshold_coverage.csv")
    by_view = defaultdict(list)
    for p in pairs:
        by_view[p["view"]].append(p)

    wf, names = [], (("LIST+FEES", "Menu price + fees", "what the app first shows"),
                     ("MEMBER", "After their membership", "Swiggy One / Zomato Gold"),
                     ("AFTER OFFER", "After their coupon", "the bill people actually pay"))
    for key, label, sub in names:
        v = by_view[key]
        med = st.median([float(x["saving_rs"]) for x in v])
        wins = sum(1 for x in v if truthy(x["ownly_wins"]))
        wf.append({"label": label, "sub": f"wins {wins} of {len(v)} baskets", "value": med,
                   "shown": f'{"−" if med < 0 else ""}₹{abs(med):.0f}'})

    cv = [{"label": lbl, "value": float(r["coverage_pct"]), "shown": f'{float(r["coverage_pct"]):.0f}%',
           "sub": f'{r["pairs_clearing"]} of {r["pairs_total"]} pairs', "hl": lbl == "Menu price + fees",
           "fill": CORAL if lbl == "After their coupon" else None}
          for (key, lbl, _), r in zip(names, cov)]

    body = f"""
  <div class="two">
    {fig("What Ownly saves you, per basket", waterfall(wf, w=520, title="Median saving by price view"),
         "Four matched baskets, one Gachibowli address, 16 Sep 2026. Directional — four baskets, not a market.")}
    {fig("Share of people whose switching price is met",
         hbars(cv, label_w=182, w=600, row=48, title="Switch-threshold coverage"),
         "33 people's stated switching price × 4 real baskets = 132 pairs.")}
  </div>
  {tiles([
      {"v": "5.2%", "label": "of an Ownly bill is fees and tax", "sub": "Incumbent median 23.4% — structural, needs no subsidy"},
      {"v": "4 of 4", "label": "baskets Ownly wins before anyone's coupon", "sub": "Median ₹114.50 cheaper"},
      {"v": "−₹28", "label": "Ownly is dearer once a rival coupon lands", "sub": "The advantage is real, and it is erasable", "tone": "bad"}])}"""
    return slide(5, "Price", "Ownly is genuinely cheaper — until the checkout people actually see.",
                 "The saving is <b>structural</b>, not bought with discounts. That is the strength. "
                 "It is also <b>one coupon deep</b>.", body)


def s6_thirty():
    td = read("final_dashboard/data/tradeoff_summary.csv")
    stair = read("final_dashboard/data/switching_staircase.csv")
    labels = {"speed": ("Wait 15 minutes longer", "45 min instead of 30"),
              "reliability": ("Accept 3-in-10 late", "instead of 1-in-10"),
              "usual restaurants": ("Give up usual restaurants", "keep only a few of them")}
    items = []
    for r in td:
        lab, sub = labels[r["dimension"]]
        pct = float(r["chose_cheaper_pct"])
        items.append({"label": lab, "sub": sub, "value": pct, "shown": f"{pct:.1f}%",
                      "lo": float(r["ci_lo"]), "hi": float(r["ci_hi"]),
                      "hl": r["dimension"] != "usual restaurants",
                      "fill": CORAL if r["dimension"] == "usual restaurants" else None})

    pts = [{"label": f'₹{r["level_rs"]}', "pct": float(r["pct_of_named"]),
            "shown": f'{float(r["pct_of_named"]):.0f}% by ₹{r["level_rs"]}',
            "hl": r["level_rs"] == "30"} for r in stair]

    body = f"""
  <div class="two">
    {fig("What they would give up for ₹30 off", hbars(items, label_w=194, w=600, row=74, bar_h=26, ci=True,
                                                       title="Trade-offs at ₹30"),
         "40 people, forced binary choices, 95% intervals. The gap is not noise: "
         "24 accepted the wait but refused to lose restaurants; 1 did the reverse.")}
    {fig("How much cheaper, every time, to switch main app", staircase(pts, title="Switching staircase"),
         "33 people named a figure; 4 said no amount would move them, 3 didn't know.")}
  </div>
  {tiles([
      {"v": "₹30", "label": "median saving needed to change main app", "sub": "Half are reachable at ₹30 or less"},
      {"v": "82.5%", "label": "already pay for Swiggy One or Zomato Gold", "sub": "33 of 40 · 19 pay for both", "tone": "warn"},
      {"v": "35%", "label": "would give up their usual restaurants for ₹30", "sub": "The one thing price does not buy", "tone": "bad"}])}"""
    return slide(6, "The ₹30 equation", "Price buys speed and patience. It does not buy their restaurants.",
                 "Same ₹30, three different answers. <b>The order of these three numbers is the strategy.</b>", body)


def s7_fakedoor():
    fn = read("FINAL_STORY/data/s8_fd_funnel.csv")
    entry = read("FINAL_STORY/data/s8_fd_entry.csv")
    steps = ["Opened Ownly", "Picked a dish or place", "Added food to cart", "Chose how to pay", "Pressed Place order"]
    d = {(r["Channel"], r["Step"]): r for r in fn}
    items = []
    for s in steps:
        a, b = d[("Direct link", s)], d[("Inside Rapido", s)]
        items.append({"label": s, "a": float(a["Pct"]), "b": float(b["Pct"]),
                      "shown_a": f'{a["Sessions"]} of {a["Base"]}', "shown_b": f'{b["Sessions"]} of {b["Base"]}'})
    funnel = grouped(items, [("Direct link", BLUE), ("Inside a ride app", BLUE_LT)],
                     label_w=176, w=600, row=62, bar_h=18, title="Fake-door funnel by entry point")

    ent = [{"label": r["Entry_point"].replace("Ad after the ride ends", "Ad after the ride"),
            "value": float(r["Pct"]), "shown": f'{float(r["Pct"]):.0f}%',
            "sub": f'{r["Placed"]} of {r["Sessions"]} sessions', "hl": "Food tab" in r["Entry_point"]}
           for r in entry if int(r["Sessions"]) >= 5]

    body = f"""
  <div class="two">
    {fig("70 sessions on an app that could not take an order", funnel,
         "Real restaurant names, invented prices, no payment screen, no confirmation. "
         "“Placed” means they pressed the button.")}
    {fig("Where they came in from", hbars(ent, label_w=176, w=560, row=72, bar_h=26, title="Orders placed by entry point"),
         "Small groups — direction only. An ad interrupts; a tab is a decision already made.")}
  </div>
  {tiles([
      {"v": "16 of 30", "label": "went back to their usual app when the place they wanted was missing",
       "sub": "The single biggest leak we found", "tone": "bad"},
      {"v": "62.5%", "label": "chose a restaurant because “it's always good” or “they make it best”",
       "sub": "Only 12.5% chose on price"},
      {"v": "91.7%", "label": "entering from inside the ride app browsed something", "sub": "But only 36.1% finished — 47.1% direct"}])}"""
    return slide(7, "The fake door", "We built a working app and watched 70 people use it.",
                 "Not a landing page: eight screens, real menus, a delivery choice, a cart, "
                 "randomised prices. <b>Choices, not opinions.</b>", body)


def s8_paid():
    sp = read("FINAL_STORY/data/s8_fd_speed.csv")
    pay = read("FINAL_STORY/data/s8_fd_pay.csv")
    ladder = [{"label": f'₹{r["Price_rs"]}', "value": float(r["Pct"]), "shown": f'{float(r["Pct"]):.0f}%',
               "sub": f'{r["Took_Rapido_Link"]} of {r["Chose_delivery"]}',
               "fill": CORAL if r["Price_rs"] == "49" else BLUE} for r in sp]

    names = {"Pay Rs15 per order": ("Pay ₹15 per order", "a small visible fee"),
             "Order Protection (Rs15 + cover)": ("Order Protection", "₹15 + refund cover ₹9–39"),
             "Ownly Plus Rs99/month": ("Ownly Plus ₹99/month", "a third subscription")}
    pitems = []
    for r in pay:
        lab, sub = names[r["Model"]]
        chose, placed, base = int(r["Chose"]), int(r["Then_placed"]), int(r["Base"])
        pitems.append({"label": lab, "sub": sub, "a": 100 * chose / base, "b": 100 * placed / base,
                       "shown_a": f"{chose} of {base} chose", "shown_b": f"{placed} then placed"})
    pchart = grouped(pitems, [("Chose it", BLUE), ("Then placed the order", BLUE_LT)],
                     label_w=184, w=590, row=50, title="How they chose to pay")

    body = f"""
  <div class="two">
    {fig("Paying to skip 17 minutes", columns(ladder, 70, w=430, title="Rapido Link take-up by randomised price"),
         "Each person saw one random price. Take-up <b>rose</b> as the price rose — "
         "every group under 15 people, so read the shape, not the levels.")}
    {fig("Which way of paying they picked", pchart,
         "42 people reached this screen. All three options carried the same delivery fee.")}
  </div>
  {tiles([
      {"v": "45.5%", "label": "paid ₹15–₹49 for faster delivery", "sub": "20 of 44 — while 92.5% said they would wait for ₹30", "tone": "bad"},
      {"v": "62%", "label": "chose a ₹15 per-order fee, and 81% of them placed the order", "sub": "A visible small fee is tolerated"},
      {"v": "3 of 8", "label": "who chose the ₹99 membership actually placed an order", "sub": "A third subscription is not wanted", "tone": "warn"}])}"""
    return slide(8, "What they paid for", "They said they would wait. Then they paid not to.",
                 "The clearest gap in the study between <b>what people say</b> and "
                 "<b>what they do when a button is in front of them</b>.", body)


def s9_verdicts():
    V = [("Confirmed", "They won't give up their restaurants",
          "Survey: only 35% would, for ₹30",
          "Missing place → 16 of 30 went back to their usual app. 62.5% picked a restaurant on trust, 12.5% on price."),
         ("Confirmed", "Nobody believes the prices will last",
          "Survey: 87.5% expect them to rise",
          "53% picked cash-now because “I may not order again” or “I don't trust later offers”. Only 35% took the wallet."),
         ("Confirmed", "Failed orders and refunds drive people away",
          "Reviews: 72% and 79%",
          "“I want a refund if it goes wrong” was the top reason behind payment choices. 8 of 42 bought refund cover at ₹9–39."),
         ("Confirmed", "Rapido brings attention, not orders",
          "Survey: 5 of 33 noticed food in Rapido",
          "From inside the ride app: 33 of 36 browsed, 13 of 36 finished. Ad 4 of 16; food tab 8 of 14."),
         ("Contradicted", "Don't spend on speed",
          "Survey: 92.5% would wait 15 min for ₹30",
          "45.5% paid ₹15–49 to save 17 minutes, and take-up rose with price: 25% → 33% → 54% → 64%."),
         ("New nuance", "No fees is the thing to keep",
          "Our own assumption going in",
          "62% chose ₹15 per order and 81% of them placed. Only 8 of 42 took ₹99/month, and 3 of those placed.")]
    tone = {"Confirmed": "ok", "Contradicted": "bad", "New nuance": "warn"}
    cards = "".join(
        f'<div class="vcard {tone[v]}"><div class="vb">{e(v)}</div><div class="vt">{e(t)}</div>'
        f'<div class="vs">{e(s)}</div><div class="ve">{e(ev)}</div></div>' for v, t, s, ev in V)
    body = f'<div class="vgrid">{cards}</div>'
    return slide(9, "Claims vs evidence", "Six things we believed. The app tested all six.",
                 "Survey and desk research made the claims. <b>The fake door made people choose.</b> "
                 "Four held, one broke, one changed shape.", body)


def s10_firsthand():
    img = "images/firsthand"
    shots = [(f"{img}/02_order_receipt_lapinoz_23sep.png", "₹765 paid · 23 Sep"),
             (f"{img}/01_complaint_small_pizza.png", "“I ordered a 22cm slice”"),
             (f"{img}/05_support_chat_closed_no_resolution.png", "Chat closed, unresolved"),
             (f"{img}/07_field_team_delivery_handover.png", "The handover, Gachibowli")]
    strip = "".join(f'<figure class="shot"><img src="{s}" alt="{e(c)}" loading="lazy"><figcaption>{e(c)}</figcaption></figure>'
                    for s, c in shots)
    steps = [("21:54", "We report the wrong item, with a photo", ""),
             ("22:20", "First human reply", "26 minutes later"),
             ("22:27", "25% refund offered on that one item", ""),
             ("22:29", "“Since we haven't heard from you, we'll close this chat”", "closed in 2 minutes", True),
             ("22:37", "We reopen and ask for the refund we were offered", ""),
             ("22:55", "Refund confirmed", "61 minutes after the complaint")]
    tl = "".join(f'<li{" class=hyd" if len(x) > 3 else ""}><span class="when">{e(x[0])}</span>'
                 f'<span class="what">{e(x[1])}{f" — {e(x[2])}" if x[2] else ""}</span></li>' for x in steps)

    body = f"""
  <div class="two wide">
    {fig("We ordered on Ownly ourselves", f'<div class="shots">{strip}</div>',
         "23 September 2026, La Pino'z via Ownly, delivered to Gachibowli. Food arrived cold, "
         "cutlery missing, and the pizza was a fraction of the size ordered.")}
    {fig("What support did about it", f'<ol class="tl">{tl}</ol>',
         "One order, one complaint. It is not a rate — it is the experience behind the 79%.")}
  </div>
  {tiles([
      {"v": "79%", "label": "of Ownly app-store reviews mention support or refund failure",
       "sub": "29 coded reviews · 70% of all reviews are 1-star", "tone": "bad"},
      {"v": "26 min", "label": "before a human replied to us", "sub": "The chat then closed itself in 2 minutes", "tone": "warn"},
      {"v": "1 star", "label": "we rated the support experience", "sub": "Refund received. Experience not repaired"}])}"""
    return slide(10, "First-hand", "We ordered it, it went wrong, and we watched how they fixed it.",
                 "The reviews said orders fail and refunds are a fight. "
                 "<b>So we bought one and found out.</b>", body)


def s11_ui():
    proto = "images/prototype"
    shots = [(f"{proto}/home_discount.png", "Home screen A — discounts first"),
             (f"{proto}/home_restaurants.png", "Home screen B — your regulars first")]
    strip = "".join(f'<figure class="shot tall"><img src="{s}" alt="{e(c)}" loading="lazy"><figcaption>{e(c)}</figcaption></figure>'
                    for s, c in shots)
    recs = [("Lead with the places they already order from",
             "A missing restaurant lost 16 of 30 orders. Put regulars on the home screen, and add “Not here yet? Tell us the place.”"),
            ("Sell the delivery choice, and answer the worry",
             "45.5% paid ₹15–49 for 17 minutes. 11 of 34 worried the captain drops a passenger first — say “no passenger on board”."),
            ("Show the bill, then offer cover — not a membership",
             "₹0 platform, ₹0 packaging lines make the 5.2% fee load visible. Add refund cover at ₹19. Drop the ₹99 plan.")]
    rl = "".join(f'<li><b>{e(h)}</b><span>{e(b)}</span></li>' for h, b in recs)
    body = f"""
  <div class="two">
    {fig("The app we built to test it", f'<div class="shots">{strip}</div>',
         "Both home screens ran live. The arm comparison itself is not reportable — "
         "phones were shared, so the split was 58 to 12.")}
    {fig("Three changes the sessions argue for", f'<ol class="recs">{rl}</ol>',
         "Each one is a change to a screen, not a slogan.")}
  </div>"""
    return slide(11, "Product", "Three screen changes, straight out of the sessions.",
                 "Everything here was chosen by someone in the fake door, not by us in a meeting.", body)


def s12_strategy():
    rows = [("KEEP", "keep", "Zero commission and no platform fee",
             "Fees are 5.2% of an Ownly bill against a 23.4% incumbent median. Structural — it needs no subsidy to stay true."),
            ("ADAPT", "adapt", "Go deep on local restaurants, not wide",
             "A missing place lost 53.3% of fake-door orders, and only 35% would trade their restaurants for ₹30."),
            ("ADD", "add", "Paid fast delivery through Rapido",
             "45.5% paid ₹15–49 for 17 minutes, take-up rising with price. It also uses the one asset rivals cannot copy."),
            ("ADD", "add", "Same-day refund cover, ₹9–39",
             "Refund failure appears in 79% of app reviews, was the top reason behind payment choices — and we lived it ourselves."),
            ("DROP", "drop", "Big first-order discounts and a ₹99 membership",
             "Only 25% would stay after the offer; 3 of the 8 who chose the membership placed an order. Bengaluru's triers left when the offers ended.")]
    tr = "".join(f'<tr><td><span class="dec {c}">{e(d)}</span></td><td class="w">{e(w)}</td><td>{e(b)}</td></tr>'
                 for d, c, w, b in rows)
    body = f"""
  <table class="calls"><tbody>{tr}</tbody></table>
  {tiles([
      {"v": "Second orders", "label": "the number that decides this, and only Rapido can see it",
       "sub": "Repeat orders per user, 30 days after the first"},
      {"v": "Order failure", "label": "the number that will undo the price advantage",
       "sub": "Late, missing and wrong orders per 100 — plus time to a resolved refund"},
      {"v": "₹30 → ₹0", "label": "what a rival coupon does to the whole argument",
       "sub": "Watch coverage, not list price: 81% → 56% → 27%", "tone": "warn"}])}"""
    return slide(12, "So what", "Don't buy the first order. Earn the second one.",
                 "Price gets attention, and Ownly already has the cheaper bill. "
                 "<b>Nothing in our evidence says anyone comes back.</b>", body)


# ================================================================ shell
CSS = """
*,*::before,*::after{box-sizing:border-box}
html{scroll-snap-type:y proximity;-webkit-text-size-adjust:100%}
body{margin:0;background:#F2EBDD;color:#443533;font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
     font-variant-numeric:tabular-nums;color-scheme:light}
section{min-height:100vh;max-width:1260px;margin:0 auto;padding:30px 52px 18px;scroll-snap-align:start;
        display:flex;flex-direction:column;gap:14px}
h1{font:400 clamp(26px,3vw,40px)/1.08 Georgia,"Times New Roman",serif;margin:0;letter-spacing:-.01em;max-width:28ch}
.kick{margin:0;font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:#EF7259}
.lede{margin:0;max-width:86ch;font-size:15px;color:#5E504B}
.lede b{font-weight:600;color:#443533}

.two{display:grid;grid-template-columns:.86fr 1.14fr;gap:18px;align-items:stretch;flex:1;min-height:0}
.two.wide{grid-template-columns:1.15fr .85fr}
figure{margin:0;background:#FBF8F1;border:1px solid #D5C9B4;padding:14px 18px 12px;display:flex;flex-direction:column}
figcaption{font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:#8C7F78;margin-bottom:10px}
.cap{margin:9px 0 0;font-size:11.5px;color:#8C7F78;border-top:1px solid #EDE4D3;padding-top:7px}
.cap b{color:#443533;font-weight:600}

/* timeline */
.tl{list-style:none;margin:auto 0;padding:0 0 0 18px;border-left:2px solid #E5DBC8}
.tl li{position:relative;padding:0 0 12px 14px}
.tl li:last-child{padding-bottom:0}
.tl li::before{content:"";position:absolute;left:-25px;top:5px;width:10px;height:10px;border-radius:50%;
               background:#F2EBDD;border:2px solid #C9B79A}
.tl li.hyd::before{background:#EF7259;border-color:#EF7259}
.tl .when{display:block;font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:#8C7F78}
.tl .what{display:block;font-size:13.5px}
.tl li.hyd .what{font-weight:600}

/* charts */
svg.chart{display:block;width:100%;height:auto;margin-block:auto}
.chart .rl{font-size:12.5px;fill:#443533;font-weight:600}
.chart .sl{font-size:10.5px;fill:#8C7F78}
.chart .vl{font:400 14px Georgia,serif;fill:#2F6094}
.chart .vl.lt{fill:#7FA0C0}
.chart .vl.neg,.chart .vl.hl{fill:#EF7259}
.chart .ax{font-size:10px;fill:#8C7F78}
.chart .lg{font-size:11px;fill:#5E504B}

/* stat tiles: the 1px gap over a rule-coloured bed is the divider */
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:1px;background:#D5C9B4;border:1px solid #D5C9B4;flex:none;margin-top:auto}
.tiles.six{grid-template-columns:repeat(2,1fr);margin-block:auto}
.tile{background:#FBF8F1;padding:11px 15px}
.tv{font:400 25px/1.05 Georgia,"Times New Roman",serif;color:#2F6094}
.tv.bad{color:#EF7259}.tv.warn{color:#B4552F}
.tl2{margin-top:5px;font-size:12.5px;max-width:36ch}
.ts{margin-top:3px;font-size:10.5px;color:#8C7F78}

/* kpi grid */
.kpigrid{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:#D5C9B4;border:1px solid #D5C9B4;flex:1}
.kpi{background:#FBF8F1;padding:14px 16px;display:flex;flex-direction:column;gap:4px}
.kpi.off{background:#F4EFE4}
.kv{font:400 30px/1 Georgia,serif;color:#2F6094}
.kpi.off .kv{color:#8C7F78}
.kv .u{font-size:13px;margin-left:3px;color:#8C7F78}
.kn{font-size:13px;font-weight:600;line-height:1.3}
.km{font-size:10.5px;color:#8C7F78}
.kw{font-size:11.5px;color:#5E504B;margin-top:4px}
.kb{margin-top:auto;font-size:9px;letter-spacing:.12em;color:#2F6094}
.kpi.off .kb{color:#B4552F}

/* bengaluru cards */
.cards2{display:grid;gap:1px;margin-block:auto;background:#D5C9B4;border:1px solid #D5C9B4}
.card{background:#FBF8F1;padding:10px 13px}
.ch{font-size:13px;font-weight:600}
.cb{font-size:11.5px;color:#5E504B;margin-top:2px}

/* verdicts */
.vgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:#D5C9B4;border:1px solid #D5C9B4;flex:1}
.vcard{background:#FBF8F1;padding:14px 16px;display:flex;flex-direction:column;gap:6px}
.vb{align-self:flex-start;font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;padding:2px 8px;color:#fff;background:#2F6094}
.vcard.bad .vb{background:#EF7259}.vcard.warn .vb{background:#B4552F}
.vt{font:400 19px/1.15 Georgia,serif}
.vs{font-size:11px;color:#8C7F78}
.ve{font-size:12.5px;color:#443533;border-top:1px solid #EDE4D3;padding-top:7px;margin-top:auto}

/* photos */
.shots{display:flex;gap:10px;margin-block:auto}
.shot{padding:0;border:0;background:none;flex:1;min-width:0}
.shot img{width:100%;height:248px;object-fit:cover;object-position:top;border:1px solid #D5C9B4;background:#fff}
.shot.tall img{height:312px;object-position:top}
.shot figcaption{margin:6px 0 0;font-size:10.5px;letter-spacing:.04em;text-transform:none}

/* recommendations */
.recs{margin:auto 0;padding-left:20px;display:flex;flex-direction:column;gap:12px}
.recs li b{display:block;font-size:14px}
.recs li span{display:block;font-size:12.5px;color:#5E504B;margin-top:2px}

/* strategy table */
.calls{border-collapse:collapse;width:100%;margin-block:auto}
.calls td{border-bottom:1px solid #EDE4D3;padding:11px 12px 11px 0;vertical-align:top;font-size:12.5px;color:#5E504B}
.calls td.w{font-size:14px;font-weight:600;color:#443533;width:30%}
.calls td:first-child{width:104px}
.dec{display:inline-block;font-size:9.5px;letter-spacing:.12em;padding:2px 8px;color:#fff;background:#2F6094}
.dec.adapt{background:#C9B79A;color:#443533}.dec.add{background:#3F7A5E}.dec.drop{background:#EF7259}

.pg{display:flex;justify-content:space-between;flex:none;font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;
    color:#8C7F78;border-top:1px solid #D5C9B4;padding-top:8px;margin-top:auto}

@media (max-width:900px){
  section{padding:24px 18px 16px}
  .two,.two.wide{grid-template-columns:1fr}
  .kpigrid,.vgrid{grid-template-columns:1fr 1fr}
}
@media print{
  @page{size:A4 landscape;margin:8mm}
  html{scroll-snap-type:none}
  section{min-height:auto;page-break-after:always;padding:0 0 10px}
}
"""

JS = """
// Arrow keys / space page through the slides. ?shot=N renders one slide alone.
(function(){
  var s=[].slice.call(document.querySelectorAll('section'));
  var q=new URLSearchParams(location.search).get('shot');
  if(q){s.forEach(function(x,i){if(i!=q-1)x.remove();});return;}
  addEventListener('keydown',function(ev){
    var k=ev.key,d=(k==='ArrowRight'||k==='ArrowDown'||k===' ')?1:(k==='ArrowLeft'||k==='ArrowUp')?-1:0;
    if(!d)return; ev.preventDefault();
    var y=scrollY,n=s.filter(function(x){return d>0?x.offsetTop>y+8:x.offsetTop<y-8;});
    var t=d>0?n[0]:n[n.length-1]; if(t)scrollTo({top:t.offsetTop,behavior:'smooth'});
  });
})();
"""


def build():
    slides = [s1_problem(), s2_bengaluru(), s3_kpis(), s4_evidence(), s5_price(), s6_thirty(),
              s7_fakedoor(), s8_paid(), s9_verdicts(), s10_firsthand(), s11_ui(), s12_strategy()]
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ownly in Gachibowli</title>
<style>{CSS}</style>
</head>
<body>
{"".join(slides)}
<script>{JS}</script>
</body>
</html>"""
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"wrote {OUT} ({len(html):,} bytes, {len(slides)} slides)")


if __name__ == "__main__":
    build()
