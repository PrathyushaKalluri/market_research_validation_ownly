"""
charts.py - small SVG chart helpers for the story page. Standard library only.

Every chart is one series in one colour: the bar that carries the point is the
accent, the rest are grey. Colours come from CSS variables so the page can
switch light/dark without touching the SVG.
"""
from html import escape as e

ACC, GREY, NEG = "var(--accent)", "var(--bar-muted)", "var(--neg)"
INK, INK2, RULE = "var(--ink)", "var(--ink-2)", "var(--rule)"


def _svg(w, h, body, label):
    return (f'<svg class="chart" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{e(label)}" '
            f'xmlns="http://www.w3.org/2000/svg">{body}</svg>')


def _bar(x, y, w, h, fill):
    """Horizontal bar, square at the baseline, rounded at the data end."""
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


def hbars(items, vmax=100, label_w=210, w=620, row=40, bar_h=16, unit="%", ci=False, title=""):
    """items: dicts with label, value, [shown], [hl], [sub], [lo, hi]."""
    plot = w - label_w - 70
    h = row * len(items) + 8
    out = []
    for i, it in enumerate(items):
        y = i * row + 6
        v = it["value"]
        bw = max(0, plot * v / vmax)
        fill = ACC if it.get("hl") else GREY
        out.append(f'<text x="{label_w - 12}" y="{y + bar_h - 3}" text-anchor="end" class="lbl">{e(it["label"])}</text>')
        if it.get("sub"):
            out.append(f'<text x="{label_w - 12}" y="{y + bar_h + 12}" text-anchor="end" class="sub">{e(it["sub"])}</text>')
        out.append(f'<g><title>{e(it["label"])}: {e(it.get("tip", it.get("shown", "")))}</title>'
                   f'<rect x="{label_w}" y="{y - 4}" width="{plot + 60}" height="{row - 6}" fill="transparent"/>'
                   + _bar(label_w, y, bw, bar_h, fill) + '</g>')
        if ci and it.get("lo") is not None:
            x1, x2 = label_w + plot * it["lo"] / vmax, label_w + plot * it["hi"] / vmax
            cy = y + bar_h + 5
            out.append(f'<path d="M{x1:.1f},{cy} H{x2:.1f} M{x1:.1f},{cy - 3} v6 M{x2:.1f},{cy - 3} v6" '
                       f'stroke="{INK2}" stroke-width="1" fill="none" opacity=".7"/>')
        tx = label_w + bw + 8
        out.append(f'<text x="{tx:.1f}" y="{y + bar_h - 3}" class="val{" strong" if it.get("hl") else ""}">'
                   f'{e(it.get("shown", f"{v:g}{unit}"))}</text>')
    out.append(f'<line x1="{label_w}" y1="0" x2="{label_w}" y2="{h}" stroke="{RULE}" stroke-width="1"/>')
    return _svg(w, h, "".join(out), title)


def diverging(items, vmin, vmax, label_w=210, w=620, row=40, bar_h=16, title=""):
    """Bars either side of zero. Negative bars use the negative colour."""
    plot = w - label_w - 80
    zx = label_w + plot * (-vmin) / (vmax - vmin)
    h = row * len(items) + 8
    out = []
    for i, it in enumerate(items):
        y = i * row + 6
        v = it["value"]
        bw = plot * abs(v) / (vmax - vmin)
        out.append(f'<text x="{label_w - 12}" y="{y + bar_h - 3}" text-anchor="end" class="lbl">{e(it["label"])}</text>')
        if it.get("sub"):
            out.append(f'<text x="{label_w - 12}" y="{y + bar_h + 12}" text-anchor="end" class="sub">{e(it["sub"])}</text>')
        if v >= 0:
            out.append(f'<g><title>{e(it["label"])}: {e(it["shown"])}</title>' + _bar(zx, y, bw, bar_h, ACC if it.get("hl") else GREY) + '</g>')
            out.append(f'<text x="{zx + bw + 8:.1f}" y="{y + bar_h - 3}" class="val">{e(it["shown"])}</text>')
        else:
            r = min(4, bar_h / 2, bw)
            out.append(f'<g><title>{e(it["label"])}: {e(it["shown"])}</title>'
                       f'<path d="M{zx},{y} h-{bw - r} a{r},{r} 0 0 0 -{r},{r} v{bar_h - 2 * r} a{r},{r} 0 0 0 {r},{r} h{bw - r} z" fill="{NEG}"/></g>')
            out.append(f'<text x="{zx + 8:.1f}" y="{y + bar_h - 3}" class="val strong">{e(it["shown"])}</text>')
    out.append(f'<line x1="{zx:.1f}" y1="0" x2="{zx:.1f}" y2="{h}" stroke="{INK2}" stroke-width="1"/>')
    return _svg(w, h, "".join(out), title)


def paired(measures, series, vmax=100, label_w=170, w=620, bar_h=12, gap=4, title=""):
    """Two series per measure (e.g. Bengaluru vs Gachibowli). series = [(name, fill_var)]."""
    plot = w - label_w - 90
    group = len(series) * (bar_h + gap) + 18
    h = group * len(measures) + 26
    out = []
    lx = label_w
    for name, fill in series:           # legend
        out.append(f'<rect x="{lx}" y="2" width="10" height="10" rx="2" fill="{fill}"/>'
                   f'<text x="{lx + 15}" y="11" class="sub">{e(name)}</text>')
        lx += 15 + 6.2 * len(name) + 20
    for gi, m in enumerate(measures):
        y0 = 26 + gi * group
        out.append(f'<text x="{label_w - 12}" y="{y0 + bar_h + 2}" text-anchor="end" class="lbl">{e(m["label"])}</text>')
        for si, (name, fill) in enumerate(series):
            y = y0 + si * (bar_h + gap)
            v, shown = m["values"][si]
            bw = plot * v / vmax
            out.append(f'<g><title>{e(m["label"])} - {e(name)}: {e(shown)}</title>' + _bar(label_w, y, bw, bar_h, fill) + '</g>')
            out.append(f'<text x="{label_w + bw + 6:.1f}" y="{y + bar_h - 2}" class="val small">{e(shown)}</text>')
    out.append(f'<line x1="{label_w}" y1="20" x2="{label_w}" y2="{h}" stroke="{RULE}" stroke-width="1"/>')
    return _svg(w, h, "".join(out), title)


def columns(items, vmax=100, w=420, h=230, title=""):
    """Vertical bars (ordered categories such as price points). items: label, value, shown, sub, hl."""
    base = h - 44
    n = len(items)
    slot = (w - 20) / n
    bw = min(46, slot * 0.5)
    out = [f'<line x1="10" y1="{base}" x2="{w - 10}" y2="{base}" stroke="{RULE}" stroke-width="1"/>']
    for i, it in enumerate(items):
        cx = 10 + slot * i + slot / 2
        bh = (base - 24) * it["value"] / vmax
        out.append(f'<g><title>{e(it["label"])}: {e(it["tip"])}</title>' +
                   _vbar(cx - bw / 2, base, bw, bh, ACC if it.get("hl") else GREY) + '</g>')
        out.append(f'<text x="{cx:.1f}" y="{base - bh - 7:.1f}" text-anchor="middle" class="val">{e(it["shown"])}</text>')
        out.append(f'<text x="{cx:.1f}" y="{base + 17}" text-anchor="middle" class="lbl">{e(it["label"])}</text>')
        out.append(f'<text x="{cx:.1f}" y="{base + 33}" text-anchor="middle" class="sub">{e(it["sub"])}</text>')
    return _svg(w, h, "".join(out), title)
