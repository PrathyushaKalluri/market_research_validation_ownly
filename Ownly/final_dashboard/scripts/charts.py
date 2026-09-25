"""
charts.py — hand-rolled inline SVG chart primitives.

Deliberately not a plotting library: no library chrome, no default palettes, no
notebook styling. Classic print-BI conventions - hairline rules, tabular figures,
direct labelling, no legends where a label will do.
"""
from html import escape

CREAM = "#F2EBDD"
CORAL = "#EF7259"
BLUE = "#2F6094"
DARK = "#443533"
RULE = "#D5C9B4"
MUTED = "#8C7F78"
PANEL = "#FBF8F1"
GRID = "#E5DBC8"

PLATFORM = {"ownly": CORAL, "swiggy": BLUE, "zomato": DARK,
            "Ownly": CORAL, "Swiggy": BLUE, "Zomato": DARK}


def _t(x, y, s, cls="lbl", anchor="start", size=None, color=None, weight=None):
    st = []
    if size:
        st.append(f"font-size:{size}px")
    if color:
        st.append(f"fill:{color}")
    if weight:
        st.append(f"font-weight:{weight}")
    style = f' style="{";".join(st)}"' if st else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" '
            f'text-anchor="{anchor}"{style}>{escape(str(s))}</text>')


def _svg(w, h, body, cls="chart"):
    return (f'<svg class="{cls}" viewBox="0 0 {w} {h}" width="100%" '
            f'preserveAspectRatio="xMinYMin meet" role="img">{body}</svg>')


def hbar(rows, w=560, rowh=34, maxval=None, unit="%", pad_l=210, pad_r=64,
         color=None, note_key="note", show_ci=True):
    """rows: [{label, value, ci_lo?, ci_hi?, note?, color?}]"""
    h = len(rows) * rowh + 26
    mx = maxval or max([r["value"] for r in rows] + [1])
    mx = mx * 1.08
    plot_w = w - pad_l - pad_r
    b = [f'<rect x="0" y="0" width="{w}" height="{h}" fill="none"/>']
    for i, r in enumerate(rows):
        y = i * rowh + 12
        bw = max(0, r["value"] / mx * plot_w)
        c = r.get("color") or color or BLUE
        b.append(f'<rect x="{pad_l}" y="{y}" width="{bw:.1f}" height="{rowh-16}" fill="{c}"/>')
        b.append(_t(pad_l - 10, y + rowh - 22, r["label"], anchor="end", size=12.5, color=DARK))
        val = f'{r["value"]:.0f}{unit}' if unit == "%" else f'{r["value"]:,.0f}'
        b.append(_t(pad_l + bw + 7, y + rowh - 22, val, size=12.5, weight=600, color=DARK))
        if show_ci and r.get("ci_lo") is not None:
            x1 = pad_l + r["ci_lo"] / mx * plot_w
            x2 = pad_l + r["ci_hi"] / mx * plot_w
            ym = y + (rowh - 16) / 2
            b.append(f'<line x1="{x1:.1f}" y1="{ym:.1f}" x2="{x2:.1f}" y2="{ym:.1f}" '
                     f'stroke="{DARK}" stroke-width="1" opacity=".55"/>')
            for xx in (x1, x2):
                b.append(f'<line x1="{xx:.1f}" y1="{ym-3.5:.1f}" x2="{xx:.1f}" y2="{ym+3.5:.1f}" '
                         f'stroke="{DARK}" stroke-width="1" opacity=".55"/>')
        if r.get(note_key):
            b.append(_t(pad_l + bw + 7, y + rowh - 9, r[note_key], size=10, color=MUTED))
    b.append(f'<line x1="{pad_l}" y1="6" x2="{pad_l}" y2="{h-8}" stroke="{RULE}" stroke-width="1"/>')
    return _svg(w, h, "".join(b))


def paired_tradeoff(rows, w=660, rowh=64):
    """rows: [{label, cheap_pct, prem_pct, cheap_txt, prem_txt, n}] - 100% stacked pair."""
    h = len(rows) * rowh + 34
    pad_l, pad_r = 186, 20
    pw = w - pad_l - pad_r
    b = []
    b.append(_t(pad_l, 12, "CHOSE THE ₹30 CHEAPER OPTION", cls="axlab", size=9.5, color=MUTED, weight=600))
    b.append(_t(pad_l + pw, 12, "PAID ₹30 TO KEEP IT", cls="axlab", anchor="end", size=9.5,
               color=MUTED, weight=600))
    for i, r in enumerate(rows):
        y = i * rowh + 26
        cw = r["cheap_pct"] / 100 * pw
        b.append(f'<rect x="{pad_l}" y="{y}" width="{cw:.1f}" height="26" fill="{CORAL}"/>')
        b.append(f'<rect x="{pad_l+cw:.1f}" y="{y}" width="{pw-cw:.1f}" height="26" fill="{BLUE}"/>')
        b.append(_t(pad_l - 10, y + 17, r["label"], anchor="end", size=13, color=DARK, weight=600))
        if cw > 42:
            b.append(_t(pad_l + 8, y + 17.5, f'{r["cheap_pct"]:.0f}%', size=12.5,
                        color="#FFF", weight=700))
        if pw - cw > 42:
            b.append(_t(pad_l + pw - 8, y + 17.5, f'{r["prem_pct"]:.0f}%', anchor="end",
                        size=12.5, color="#FFF", weight=700))
        b.append(_t(pad_l, y + 40, r["cheap_txt"], size=10.5, color=MUTED))
        b.append(_t(pad_l + pw, y + 40, r["prem_txt"], anchor="end", size=10.5, color=MUTED))
    b.append(f'<line x1="{pad_l+pw/2:.1f}" y1="20" x2="{pad_l+pw/2:.1f}" y2="{h-16}" '
             f'stroke="{DARK}" stroke-width="1" stroke-dasharray="3 3" opacity=".45"/>')
    return _svg(w, h, "".join(b))


def scatter(points, w=600, h=380, xlab="", ylab="", pad=58, quadrant=None, xfmt="₹{:,.0f}"):
    """points: [{x,y,label,color,platform}]"""
    xs = [p["x"] for p in points]
    ys = [p["y"] for p in points]
    x0, x1 = min(xs) * .88, max(xs) * 1.08
    y0, y1 = 0, max(ys) * 1.22
    pw, ph = w - pad - 24, h - pad - 30

    def px(v):
        return pad + (v - x0) / (x1 - x0) * pw

    def py(v):
        return h - pad + 6 - (v - y0) / (y1 - y0) * ph

    b = []
    for gv in range(0, int(y1) + 10, 10):
        if gv > y1:
            break
        b.append(f'<line x1="{pad}" y1="{py(gv):.1f}" x2="{pad+pw}" y2="{py(gv):.1f}" '
                 f'stroke="{GRID}" stroke-width="1"/>')
        b.append(_t(pad - 8, py(gv) + 3.5, gv, anchor="end", size=10.5, color=MUTED))
    if quadrant:
        qx, qy = px(quadrant[0]), py(quadrant[1])
        b.append(f'<line x1="{qx:.1f}" y1="{py(y1):.1f}" x2="{qx:.1f}" y2="{h-pad+6:.1f}" '
                 f'stroke="{DARK}" stroke-width="1" stroke-dasharray="4 3" opacity=".5"/>')
        b.append(f'<line x1="{pad}" y1="{qy:.1f}" x2="{pad+pw}" y2="{qy:.1f}" '
                 f'stroke="{DARK}" stroke-width="1" stroke-dasharray="4 3" opacity=".5"/>')
        b.append(_t(pad + 6, py(y1) + 14, "CHEAPER · SLOWER", size=9.5, color=MUTED, weight=600))
        b.append(_t(pad + pw - 4, py(y1) + 14, "DEARER · SLOWER", anchor="end", size=9.5,
                    color=MUTED, weight=600))
    for p in points:
        c = p.get("color") or PLATFORM.get(p.get("platform", ""), BLUE)
        b.append(f'<circle cx="{px(p["x"]):.1f}" cy="{py(p["y"]):.1f}" r="6" fill="{c}" '
                 f'fill-opacity=".9"/>')
        if p.get("label"):
            b.append(_t(px(p["x"]), py(p["y"]) - 11, p["label"], anchor="middle", size=10,
                        color=DARK))
    b.append(f'<line x1="{pad}" y1="{h-pad+6:.1f}" x2="{pad+pw}" y2="{h-pad+6:.1f}" '
             f'stroke="{DARK}" stroke-width="1"/>')
    for v in [x0 + (x1 - x0) * f for f in (0, .25, .5, .75, 1)]:
        b.append(_t(px(v), h - pad + 24, xfmt.format(v), anchor="middle", size=10.5, color=MUTED))
    b.append(_t(pad + pw / 2, h - 6, xlab, anchor="middle", size=10.5, color=MUTED, weight=600))
    b.append(f'<text x="14" y="{pad+ph/2:.1f}" class="lbl" text-anchor="middle" '
             f'transform="rotate(-90 14 {pad+ph/2:.1f})" style="font-size:10.5px;'
             f'fill:{MUTED};font-weight:600">{escape(ylab)}</text>')
    return _svg(w, h, "".join(b))


def waterfall(items, w=560, h=250, pad_l=46, unit="₹"):
    """items: [{label, value, kind: base|add|sub|total}]"""
    run, pts, mx = 0, [], 0
    for it in items:
        if it["kind"] == "total":
            pts.append((it["label"], 0, it["value"], "total"))
            mx = max(mx, it["value"])
        else:
            s = run
            run += it["value"]
            pts.append((it["label"], min(s, run), abs(it["value"]), it["kind"]))
            mx = max(mx, run, s)
    mx *= 1.16
    pw = w - pad_l - 16
    bw = pw / len(pts) * .62
    step = pw / len(pts)
    ph = h - 74

    def py(v):
        return 20 + ph - v / mx * ph

    b = []
    for i, (lab, base, val, kind) in enumerate(pts):
        x = pad_l + i * step + (step - bw) / 2
        c = {"base": BLUE, "add": MUTED, "sub": CORAL, "total": DARK}[kind]
        y = py(base + val)
        hh = max(1.5, val / mx * ph)
        b.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{hh:.1f}" fill="{c}"/>')
        b.append(_t(x + bw / 2, y - 6, f'{unit}{val:,.0f}', anchor="middle", size=10.5,
                    color=DARK, weight=600))
        for j, part in enumerate(lab.split("\n")):
            b.append(_t(x + bw / 2, 20 + ph + 15 + j * 11, part, anchor="middle", size=9.8,
                        color=MUTED))
    b.append(f'<line x1="{pad_l}" y1="{20+ph:.1f}" x2="{w-16}" y2="{20+ph:.1f}" '
             f'stroke="{DARK}" stroke-width="1"/>')
    return _svg(w, h, "".join(b))


def funnel(stages, w=540, rowh=52):
    """stages: [{label, k, n, pct}]"""
    h = len(stages) * rowh + 16
    pad_l = 176
    pw = w - pad_l - 72
    b = []
    for i, s in enumerate(stages):
        y = i * rowh + 10
        bw = max(2, s["pct"] / 100 * pw)
        b.append(f'<rect x="{pad_l}" y="{y}" width="{bw:.1f}" height="30" fill="{BLUE}" '
                 f'fill-opacity="{1 - i*0.17:.2f}"/>')
        b.append(_t(pad_l - 10, y + 20, s["label"], anchor="end", size=12.5, color=DARK, weight=600))
        b.append(_t(pad_l + bw + 8, y + 15, f'{s["pct"]:.0f}%', size=13, color=DARK, weight=700))
        b.append(_t(pad_l + bw + 8, y + 27, f'{s["k"]}/{s["n"]}', size=10, color=MUTED))
        if i:
            drop = stages[i - 1]["pct"] - s["pct"]
            if drop > 0:
                b.append(_t(pad_l - 10, y + 34, f'−{drop:.0f}pp', anchor="end", size=9.5,
                            color=CORAL, weight=600))
    return _svg(w, h, "".join(b))


def matrix(rows, cols, cells, w=760, cellh=34, pad_l=230, pad_r=56):
    """cells: {(row,col): status}"""
    STY = {"SUPPORTS": (BLUE, "#FFF"), "CONTRADICTS": (CORAL, "#FFF"),
           "MIXED": ("#C9B79A", DARK), "NO EVIDENCE": ("#EDE4D3", MUTED)}
    cw = (w - pad_l - pad_r) / len(cols)
    h = len(rows) * cellh + 68
    b = []
    for j, c in enumerate(cols):
        x = pad_l + j * cw + cw / 2
        b.append(f'<text x="{x:.1f}" y="52" class="lbl" text-anchor="start" '
                 f'transform="rotate(-40 {x:.1f} 52)" style="font-size:10px;fill:{MUTED};'
                 f'font-weight:600">{escape(c)}</text>')
    for i, r in enumerate(rows):
        y = 62 + i * cellh
        b.append(_t(pad_l - 10, y + cellh / 2 + 4, r, anchor="end", size=11.5, color=DARK))
        for j, c in enumerate(cols):
            st = cells.get((r, c), "NO EVIDENCE")
            bg, fg = STY.get(st, STY["NO EVIDENCE"])
            x = pad_l + j * cw
            b.append(f'<rect x="{x:.1f}" y="{y}" width="{cw-3:.1f}" height="{cellh-4}" fill="{bg}"/>')
            sym = {"SUPPORTS": "●", "CONTRADICTS": "▲", "MIXED": "◐", "NO EVIDENCE": "·"}[st]
            b.append(_t(x + (cw - 3) / 2, y + cellh / 2 + 4, sym, anchor="middle", size=12, color=fg))
    return _svg(w, h, "".join(b))


def erosion(steps, w=560, rowh=86):
    """Three-stage erosion of a price advantage.
    steps: [{name, sub, win_pct, win_k, win_n, saving_rs, saving_pct}]"""
    h = len(steps) * rowh + 30
    pad_l = 158
    bar_w = w - pad_l - 128
    b = []
    b.append(_t(pad_l, 13, "OWNLY CHEAPEST IN…", size=9.5, color=MUTED, weight=600))
    b.append(_t(w - 8, 13, "MEDIAN SAVING", anchor="end", size=9.5, color=MUTED, weight=600))
    for i, s in enumerate(steps):
        y = i * rowh + 26
        frac = max(0.0, s["win_pct"] / 100)
        bw = bar_w * frac
        c = BLUE if s["saving_rs"] > 20 else (CORAL if s["saving_rs"] < 0 else "#C9B79A")
        b.append(_t(pad_l - 12, y + 16, s["name"], anchor="end", size=12.5, color=DARK, weight=700))
        b.append(_t(pad_l - 12, y + 30, s["sub"], anchor="end", size=9.8, color=MUTED))
        b.append(f'<rect x="{pad_l}" y="{y}" width="{bar_w}" height="26" fill="#EDE4D3"/>')
        if bw > 0:
            b.append(f'<rect x="{pad_l}" y="{y}" width="{bw:.1f}" height="26" fill="{c}"/>')
        b.append(_t(pad_l + 8, y + 17.5, f'{s["win_k"]} of {s["win_n"]} baskets',
                    size=11.5, color="#FFF" if bw > 120 else DARK, weight=700))
        sv = ("−₹" + f'{abs(s["saving_rs"]):,.0f}') if s["saving_rs"] < 0 else f'₹{s["saving_rs"]:,.0f}'
        b.append(_t(w - 8, y + 14, sv, anchor="end", size=17, color=c, weight=700))
        b.append(_t(w - 8, y + 28, f'{s["saving_pct"]:+.1f}%', anchor="end", size=10.5, color=MUTED))
        if i < len(steps) - 1:
            b.append(f'<line x1="{pad_l}" y1="{y+rowh-22:.1f}" x2="{w-8}" y2="{y+rowh-22:.1f}" '
                     f'stroke="{RULE}" stroke-width="1"/>')
            b.append(_t(pad_l, y + rowh - 9, steps[i + 1].get("trigger", ""), size=9.8,
                        color=CORAL, weight=600))
    return _svg(w, h, "".join(b))


def step_curve(points, w=560, h=300, xlab="", ylab=""):
    """points: [(x_label, cumulative_pct)] - cumulative switching curve."""
    pad_l, pad_b = 46, 46
    pw, ph = w - pad_l - 22, h - pad_b - 28
    n = len(points)
    b = []
    for gv in (0, 25, 50, 75, 100):
        y = 20 + ph - gv / 100 * ph
        b.append(f'<line x1="{pad_l}" y1="{y:.1f}" x2="{pad_l+pw}" y2="{y:.1f}" '
                 f'stroke="{GRID}" stroke-width="1"/>')
        b.append(_t(pad_l - 8, y + 3.5, f'{gv}%', anchor="end", size=10.5, color=MUTED))
    step = pw / max(1, n - 1)
    pts = []
    for i, (lab, v) in enumerate(points):
        x = pad_l + i * step
        y = 20 + ph - v / 100 * ph
        pts.append((x, y))
        b.append(_t(x, 20 + ph + 17, lab, anchor="middle", size=10.5, color=MUTED))
    poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    b.append(f'<polyline points="{poly}" fill="none" stroke="{BLUE}" stroke-width="2.4"/>')
    for i, (x, y) in enumerate(pts):
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{BLUE}"/>')
        b.append(_t(x, y - 9, f'{points[i][1]:.0f}', anchor="middle", size=10, color=DARK,
                    weight=600))
    b.append(f'<line x1="{pad_l}" y1="{20+ph:.1f}" x2="{pad_l+pw}" y2="{20+ph:.1f}" '
             f'stroke="{DARK}" stroke-width="1"/>')
    b.append(_t(pad_l + pw / 2, h - 6, xlab, anchor="middle", size=10.5, color=MUTED, weight=600))
    return _svg(w, h, "".join(b)), pts, (pad_l, pw, ph)


def heat(rows, cols, cells, w=520, cellh=40, pad_l=140):
    """cells: {(row,col): (text, level 0..3)}"""
    LV = ["#EDE4D3", "#C9D5E2", "#7FA0C0", BLUE]
    cw = (w - pad_l) / len(cols)
    h = len(rows) * cellh + 40
    b = []
    for j, c in enumerate(cols):
        b.append(_t(pad_l + j * cw + cw / 2, 22, c, anchor="middle", size=11, color=MUTED,
                    weight=600))
    for i, r in enumerate(rows):
        y = 32 + i * cellh
        b.append(_t(pad_l - 10, y + cellh / 2 + 4, r, anchor="end", size=11.5, color=DARK))
        for j, c in enumerate(cols):
            txt, lv = cells.get((r, c), ("–", 0))
            x = pad_l + j * cw
            b.append(f'<rect x="{x:.1f}" y="{y}" width="{cw-3:.1f}" height="{cellh-4}" fill="{LV[lv]}"/>')
            b.append(_t(x + (cw - 3) / 2, y + cellh / 2 + 4.5, txt, anchor="middle", size=11.5,
                        color="#FFF" if lv >= 2 else DARK, weight=600))
    return _svg(w, h, "".join(b))


def staircase(levels, series, w=620, h=330, xlab="", note=""):
    """levels: [10,20,...]; series: [{name,color,vals:[...],dash?}] cumulative % lines."""
    pad_l, pad_b, pad_t = 52, 56, 26
    pw, ph = w - pad_l - 118, h - pad_b - pad_t
    b = []
    for gv in (0, 25, 50, 75, 100):
        y = pad_t + ph - gv / 100 * ph
        b.append(f'<line x1="{pad_l}" y1="{y:.1f}" x2="{pad_l+pw}" y2="{y:.1f}" '
                 f'stroke="{GRID}" stroke-width="1"/>')
        b.append(_t(pad_l - 8, y + 3.5, f'{gv}%', anchor="end", size=10.5, color=MUTED))
    y50 = pad_t + ph - 50 / 100 * ph
    b.append(f'<line x1="{pad_l}" y1="{y50:.1f}" x2="{pad_l+pw}" y2="{y50:.1f}" '
             f'stroke="{DARK}" stroke-width="1" stroke-dasharray="4 3" opacity=".55"/>')
    step = pw / max(1, len(levels) - 1)
    for i, lv in enumerate(levels):
        x = pad_l + i * step
        b.append(_t(x, pad_t + ph + 18, f'₹{lv}', anchor="middle", size=11, color=DARK))
    for s in series:
        pts = [(pad_l + i * step, pad_t + ph - v / 100 * ph) for i, v in enumerate(s["vals"])]
        poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        dash = ' stroke-dasharray="5 4"' if s.get("dash") else ""
        b.append(f'<polyline points="{poly}" fill="none" stroke="{s["color"]}" '
                 f'stroke-width="2.4"{dash}/>')
        for (x, y), v in zip(pts, s["vals"]):
            b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.8" fill="{s["color"]}"/>')
        lx, ly = pts[-1]
        b.append(_t(lx + 9, ly + 4, s["name"], size=10.5, color=s["color"], weight=600))
    b.append(f'<line x1="{pad_l}" y1="{pad_t+ph:.1f}" x2="{pad_l+pw}" y2="{pad_t+ph:.1f}" '
             f'stroke="{DARK}" stroke-width="1"/>')
    b.append(_t(pad_l + pw / 2, h - 8, xlab, anchor="middle", size=10.5, color=MUTED, weight=600))
    if note:
        b.append(_t(pad_l, 14, note, size=10, color=MUTED))
    return _svg(w, h, "".join(b))


def funnel_steps(rows, w=600, rowh=46):
    """rows: [{label,n,pct,note,drop}] — vertical funnel with step retention."""
    h = len(rows) * rowh + 18
    pad_l, pad_r = 250, 120
    pw = w - pad_l - pad_r
    mx = max(r["n"] for r in rows)
    b = []
    for i, r in enumerate(rows):
        y = i * rowh + 10
        bw = max(3, r["n"] / mx * pw)
        b.append(f'<rect x="{pad_l}" y="{y}" width="{bw:.1f}" height="26" fill="{BLUE}" '
                 f'fill-opacity="{max(.35, 1 - i*0.1):.2f}"/>')
        b.append(_t(pad_l - 10, y + 13, r["label"], anchor="end", size=11.5, color=DARK,
                    weight=600))
        if r.get("note"):
            b.append(_t(pad_l - 10, y + 25, r["note"], anchor="end", size=9.3, color=MUTED))
        b.append(_t(pad_l + bw + 8, y + 12, f'{r["n"]}', size=14, color=DARK, weight=700))
        if r.get("pct") is not None:
            b.append(_t(pad_l + bw + 8, y + 24, f'{r["pct"]:.0f}% of catchment', size=9.5,
                        color=MUTED))
        if i and r.get("drop") is not None:
            b.append(_t(pad_l + bw + 62, y + 12, f'−{r["drop"]:.0f}%', size=10, color=CORAL,
                        weight=600))
    return _svg(w, h, "".join(b))


def dotplot(rows, w=620, rowh=30, pad_l=230, unit="%", xmax=100):
    """rows: [{label, points:[{name,value,color}]}] — segment comparison dot plot."""
    h = len(rows) * rowh + 34
    pw = w - pad_l - 70
    b = []
    for gv in (0, 25, 50, 75, 100):
        if gv > xmax:
            break
        x = pad_l + gv / xmax * pw
        b.append(f'<line x1="{x:.1f}" y1="18" x2="{x:.1f}" y2="{h-16}" stroke="{GRID}" '
                 f'stroke-width="1"/>')
        b.append(_t(x, 12, f'{gv}{unit}', anchor="middle", size=9.5, color=MUTED))
    for i, r in enumerate(rows):
        y = 30 + i * rowh
        b.append(_t(pad_l - 12, y + 4, r["label"], anchor="end", size=11.5, color=DARK))
        vals = [p["value"] for p in r["points"] if p["value"] is not None]
        if len(vals) > 1:
            x1 = pad_l + min(vals) / xmax * pw
            x2 = pad_l + max(vals) / xmax * pw
            b.append(f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y:.1f}" '
                     f'stroke="{RULE}" stroke-width="2"/>')
        for p in r["points"]:
            if p["value"] is None:
                continue
            x = pad_l + p["value"] / xmax * pw
            b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" fill="{p["color"]}"/>')
    return _svg(w, h, "".join(b))


def bullet(rows, w=600, rowh=40, pad_l=250, unit=""):
    """rows: [{label, value, target, vmax, color, note}] — value vs a reference marker."""
    h = len(rows) * rowh + 14
    pw = w - pad_l - 96
    b = []
    for i, r in enumerate(rows):
        y = i * rowh + 10
        vmax = r.get("vmax") or max(r["value"], r.get("target") or 0) * 1.25 or 1
        bw = max(2, min(1, r["value"] / vmax) * pw)
        b.append(f'<rect x="{pad_l}" y="{y+5}" width="{pw}" height="16" fill="#EDE4D3"/>')
        b.append(f'<rect x="{pad_l}" y="{y+5}" width="{bw:.1f}" height="16" '
                 f'fill="{r.get("color", BLUE)}"/>')
        if r.get("target") is not None:
            tx = pad_l + min(1, r["target"] / vmax) * pw
            b.append(f'<line x1="{tx:.1f}" y1="{y}" x2="{tx:.1f}" y2="{y+26}" stroke="{DARK}" '
                     f'stroke-width="2"/>')
        b.append(_t(pad_l - 10, y + 16, r["label"], anchor="end", size=11.5, color=DARK,
                    weight=600))
        b.append(_t(pad_l + pw + 8, y + 17, f'{r["value"]:,.0f}{unit}', size=12.5, color=DARK,
                    weight=700))
        if r.get("note"):
            b.append(_t(pad_l - 10, y + 27, r["note"], anchor="end", size=9.3, color=MUTED))
    return _svg(w, h, "".join(b))


def axes(b, pad_l, pad_t, pw, ph, xlab, ylab, w, h):
    """Shared axis furniture: named x and y axes."""
    b.append(f'<line x1="{pad_l}" y1="{pad_t+ph:.1f}" x2="{pad_l+pw}" y2="{pad_t+ph:.1f}" '
             f'stroke="{DARK}" stroke-width="1.2"/>')
    b.append(f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t+ph:.1f}" '
             f'stroke="{DARK}" stroke-width="1.2"/>')
    b.append(_t(pad_l + pw / 2, h - 6, xlab, anchor="middle", size=11, color=DARK, weight=700))
    b.append(f'<text x="15" y="{pad_t+ph/2:.1f}" text-anchor="middle" '
             f'transform="rotate(-90 15 {pad_t+ph/2:.1f})" '
             f'style="font-size:11px;fill:{DARK};font-weight:700">{escape(ylab)}</text>')


def line_chart(levels, series, w=660, h=400, xlab="", ylab="", marks=None, xfmt="₹{}"):
    """Cumulative line chart with named axes and optional annotated markers."""
    pad_l, pad_t, pad_b = 74, 34, 76
    pw, ph = w - pad_l - 150, h - pad_t - pad_b
    b = []
    for gv in (0, 25, 50, 75, 100):
        y = pad_t + ph - gv / 100 * ph
        b.append(f'<line x1="{pad_l}" y1="{y:.1f}" x2="{pad_l+pw}" y2="{y:.1f}" '
                 f'stroke="{GRID}" stroke-width="1"/>')
        b.append(_t(pad_l - 10, y + 4, f'{gv}%', anchor="end", size=11, color=MUTED))
    step = pw / max(1, len(levels) - 1)
    for i, lv in enumerate(levels):
        x = pad_l + i * step
        b.append(_t(x, pad_t + ph + 20, xfmt.format(lv), anchor="middle", size=11.5, color=DARK))
    for mi, m in enumerate(marks or []):
        i = levels.index(m["level"])
        x = pad_l + i * step
        b.append(f'<line x1="{x:.1f}" y1="{pad_t}" x2="{x:.1f}" y2="{pad_t+ph:.1f}" '
                 f'stroke="{CORAL}" stroke-width="1.5" stroke-dasharray="4 3"/>')
        ly = pad_t + 12 + mi * 15          # stagger so labels never collide
        b.append(f'<rect x="{x+4:.1f}" y="{ly-10:.1f}" width="{len(m["label"])*5.9+8:.0f}" '
                 f'height="14" fill="{PANEL}" opacity=".92"/>')
        b.append(_t(x + 8, ly, m["label"], size=10.5, color=CORAL, weight=700))
    for s in series:
        pts = [(pad_l + i * step, pad_t + ph - v / 100 * ph) for i, v in enumerate(s["vals"])]
        poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        dash = ' stroke-dasharray="6 4"' if s.get("dash") else ""
        b.append(f'<polyline points="{poly}" fill="none" stroke="{s["color"]}" '
                 f'stroke-width="2.6"{dash}/>')
        for (x, y), v in zip(pts, s["vals"]):
            b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.2" fill="{s["color"]}"/>')
            b.append(_t(x, y - 11, f'{v:.0f}', anchor="middle", size=10, color=s["color"],
                        weight=700))
        lx, ly = pts[-1]
        for j, part in enumerate(s["name"].split("\n")):
            b.append(_t(lx + 11, ly + 4 + j * 12, part, size=10.5, color=s["color"], weight=600))
    axes(b, pad_l, pad_t, pw, ph, xlab, ylab, w, h)
    return _svg(w, h, "".join(b))


def grouped_bars(cats, series, w=660, h=380, xlab="", ylab="", unit="%", ymax=100):
    """Clustered bars: cats on x, one bar per series."""
    pad_l, pad_t, pad_b = 66, 44, 74
    pw, ph = w - pad_l - 24, h - pad_t - pad_b
    b = []
    for gv in range(0, int(ymax) + 1, 25):
        y = pad_t + ph - gv / ymax * ph
        b.append(f'<line x1="{pad_l}" y1="{y:.1f}" x2="{pad_l+pw}" y2="{y:.1f}" '
                 f'stroke="{GRID}" stroke-width="1"/>')
        b.append(_t(pad_l - 9, y + 4, f'{gv}{unit}', anchor="end", size=10.5, color=MUTED))
    gw = pw / len(cats)
    bw = gw * 0.72 / len(series)
    for i, c in enumerate(cats):
        gx = pad_l + i * gw
        for j, s in enumerate(series):
            v = s["vals"][i]
            if v is None:
                continue
            x = gx + gw * 0.14 + j * bw
            hh = max(1.5, v / ymax * ph)
            y = pad_t + ph - hh
            b.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw-3:.1f}" height="{hh:.1f}" '
                     f'fill="{s["color"]}"/>')
            b.append(_t(x + (bw - 3) / 2, y - 5, f'{v:.0f}', anchor="middle", size=9.8,
                        color=DARK, weight=700))
        for k, part in enumerate(str(c).split("\n")):
            b.append(_t(gx + gw / 2, pad_t + ph + 18 + k * 12, part, anchor="middle", size=10.5,
                        color=DARK))
    lx = pad_l
    for s in series:
        b.append(f'<rect x="{lx}" y="14" width="11" height="11" fill="{s["color"]}"/>')
        b.append(_t(lx + 16, 23.5, s["name"], size=10.5, color=DARK))
        lx += 22 + len(s["name"]) * 6.2
    axes(b, pad_l, pad_t, pw, ph, xlab, ylab, w, h)
    return _svg(w, h, "".join(b))


def forest(rows, w=660, h=None, xlab="", ylab="", lo=-1, hi=1, pad_l=300):
    """Effect size with confidence interval, one row per test."""
    rowh = 46
    h = h or len(rows) * rowh + 100
    pad_t = 40
    pw, ph = w - pad_l - 60, len(rows) * rowh
    b = []
    for gv in [lo, lo / 2, 0, hi / 2, hi]:
        x = pad_l + (gv - lo) / (hi - lo) * pw
        b.append(f'<line x1="{x:.1f}" y1="{pad_t-8}" x2="{x:.1f}" y2="{pad_t+ph:.1f}" '
                 f'stroke="{GRID if gv else DARK}" stroke-width="{1 if gv else 1.4}"/>')
        b.append(_t(x, pad_t + ph + 20, f'{gv:g}', anchor="middle", size=10.5, color=MUTED))
    b.append(_t(pad_l + (0 - lo) / (hi - lo) * pw, pad_t - 14, "no relationship",
               anchor="middle", size=10, color=DARK, weight=600))
    for i, r in enumerate(rows):
        y = pad_t + i * rowh + rowh / 2
        x = pad_l + (r["est"] - lo) / (hi - lo) * pw
        x1 = pad_l + (r["lo"] - lo) / (hi - lo) * pw
        x2 = pad_l + (r["hi"] - lo) / (hi - lo) * pw
        b.append(f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y:.1f}" stroke="{MUTED}" '
                 f'stroke-width="2"/>')
        for xx in (x1, x2):
            b.append(f'<line x1="{xx:.1f}" y1="{y-4:.1f}" x2="{xx:.1f}" y2="{y+4:.1f}" '
                     f'stroke="{MUTED}" stroke-width="2"/>')
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" fill="{r.get("color", BLUE)}"/>')
        for k, part in enumerate(r["label"].split("\n")):
            b.append(_t(pad_l - 14, y + 4 - 6 * (len(r["label"].split("\n")) - 1) + k * 12,
                        part, anchor="end", size=11, color=DARK))
        b.append(_t(pad_l + pw + 8, y + 4, f'n={r["n"]}', size=10, color=MUTED))
    axes(b, pad_l, pad_t, pw, ph, xlab, ylab, w, h)
    return _svg(w, h, "".join(b))


def coverage_grid(rows, plats, w=620, cellh=34, pad_l=230):
    """Restaurant x platform availability grid."""
    cw = (w - pad_l - 30) / len(plats)
    h = len(rows) * cellh + 58
    b = []
    for j, p in enumerate(plats):
        b.append(_t(pad_l + j * cw + cw / 2, 26, p, anchor="middle", size=11.5, color=DARK,
                    weight=700))
    for i, r in enumerate(rows):
        y = 40 + i * cellh
        b.append(_t(pad_l - 12, y + cellh / 2 + 4, r["name"], anchor="end", size=11.5, color=DARK))
        for j, p in enumerate(plats):
            x = pad_l + j * cw
            on = r["on"].get(p, False)
            col = BLUE if on else "#EDE4D3"          # one colour for present, one for absent
            b.append(f'<rect x="{x+4:.1f}" y="{y+3}" width="{cw-10:.1f}" height="{cellh-9}" '
                     f'fill="{col}"/>')
            b.append(_t(x + cw / 2, y + cellh / 2 + 4.5, "carries it" if on else "not listed",
                        anchor="middle", size=10.5, color="#FFF" if on else MUTED, weight=600))
    return _svg(w, h, "".join(b))


def stacked_share(rows, w=620, rowh=54, pad_l=200):
    """100% stacked horizontal bar, one row per base."""
    h = len(rows) * rowh + 40
    pw = w - pad_l - 30
    b = []
    for i, r in enumerate(rows):
        y = i * rowh + 26
        x = pad_l
        for seg in r["segs"]:
            sw = seg["pct"] / 100 * pw
            b.append(f'<rect x="{x:.1f}" y="{y}" width="{sw:.1f}" height="28" '
                     f'fill="{seg["color"]}"/>')
            if sw > 40:
                b.append(_t(x + sw / 2, y + 18, f'{seg["pct"]:.0f}%', anchor="middle", size=11,
                            color="#FFF", weight=700))
            x += sw
        b.append(_t(pad_l - 12, y + 13, r["label"], anchor="end", size=12, color=DARK, weight=600))
        b.append(_t(pad_l - 12, y + 26, r["note"], anchor="end", size=9.5, color=MUTED))
    lx = pad_l
    for seg in rows[0]["segs"]:
        b.append(f'<rect x="{lx}" y="4" width="11" height="11" fill="{seg["color"]}"/>')
        b.append(_t(lx + 16, 13.5, seg["name"], size=10.5, color=DARK))
        lx += 24 + len(seg["name"]) * 6.4
    return _svg(w, h, "".join(b))
