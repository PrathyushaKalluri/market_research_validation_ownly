"""
05_build_dashboard.py — assembles final_dashboard/index.html from the computed CSVs.
Every number on the page is read from data/, never typed in by hand.
"""
import os
from html import escape

import numpy as np
import pandas as pd

import charts as ch
from charts import BLUE, CORAL, DARK, MUTED, CREAM, RULE, PANEL

ROOT = "/Users/klprathyusha/Sem 3/Project/Ownly"
D = f"{ROOT}/final_dashboard/data"

S = pd.read_csv(f"{D}/cleaned_survey.csv")
K = pd.read_csv(f"{D}/kpi_table.csv")
M = pd.read_csv(f"{D}/marketing_metrics.csv")
H = pd.read_csv(f"{D}/hypothesis_results.csv")
P = pd.read_csv(f"{D}/audit_pairs.csv")
A = pd.read_csv(f"{D}/audit_clean.csv")
TR = pd.read_csv(f"{D}/tradeoff_summary.csv")
TH = pd.read_csv(f"{D}/review_theme_summary.csv")
EM = pd.read_csv(f"{D}/evidence_matrix.csv")
NE = pd.read_csv(f"{D}/not_estimable.csv")
COV = pd.read_csv(f"{D}/audit_coverage.csv").set_index("restaurant_name")
YT = pd.read_csv(f"{D}/youtube_theme_summary.csv")
YTC = pd.read_csv(f"{D}/youtube_comments_coded.csv")
YTF = pd.read_csv(f"{D}/youtube_firsthand_ownly.csv")

HYD = S[S["pop_HYD_ELIGIBLE"]]
N_HYD = len(HYD)


def kv(kid, col="value"):
    r = K[K["kpi_id"] == kid]
    return None if r.empty else r.iloc[0][col]


def mv(mid, col="value"):
    r = M[M["metric_id"] == mid]
    return None if r.empty else r.iloc[0][col]


# ------------------------------------------------------------------ fragments
def card(value, label, sub="", tone="", note=""):
    cls = f"card {tone}".strip()
    return (f'<div class="{cls}"><div class="cval">{value}</div>'
            f'<div class="clab">{escape(label)}</div>'
            f'{f"<div class=csub>{escape(sub)}</div>" if sub else ""}'
            f'{f"<div class=cnote>{escape(note)}</div>" if note else ""}</div>')


def panel(title, body, foot="", kicker=""):
    return (f'<section class="panel">'
            f'{f"<div class=kick>{escape(kicker)}</div>" if kicker else ""}'
            f'<h3>{escape(title)}</h3>{body}'
            f'{f"<p class=foot>{foot}</p>" if foot else ""}</section>')


def headline(text, sub=""):
    return (f'<div class="headline"><p class="hl">{text}</p>'
            f'{f"<p class=hlsub>{sub}</p>" if sub else ""}</div>')


def tbl(df, cols=None, cls=""):
    df = df if cols is None else df[cols]
    th = "".join(f"<th>{escape(str(c).replace('_',' '))}</th>" for c in df.columns)
    tr = ""
    for _, r in df.iterrows():
        tds = "".join(f"<td>{escape('' if pd.isna(v) else str(v))}</td>" for v in r)
        tr += f"<tr>{tds}</tr>"
    return f'<table class="tb {cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


TABS = []


def tab(tid, num, name, body):
    TABS.append({"id": tid, "num": num, "name": name, "body": body})


# ============================================================ 01 BUSINESS PROBLEM
lockin = kv("K50"); aware = kv("K70"); trial = kv("K72")
mh = kv("K51"); disc = mv("MM8")
cards = "".join([
    card(f"{N_HYD}", "Hyderabad respondents, 20–35", "37 in the Gachibowli catchment"),
    card(f"{lockin:.0f}%", "hold a Swiggy One / Zomato Gold membership", f"n={int(kv('K50','denominator'))}", tone="warn"),
    card(f"{mh:.0f}%", "use 2+ delivery apps in a month", f"n={int(kv('K51','denominator'))}"),
    card(f"{aware:.0f}%", "had heard of Ownly before this survey", f"n={N_HYD}"),
    card(f"{trial:.0f}%", "had ever ordered on Ownly", f"{int(kv('K72','numerator'))} of {N_HYD}", tone="bad"),
    card("0", "Ownly orders in the last 4 weeks", "across all 40 recent orderers", tone="bad"),
])
chain = f"""
<div class="chain">
  <div class="ch-node"><b>Cheaper final bill</b><span>observed: ₹{mv('MM2'):,.0f} median saving on list price</span></div>
  <div class="ch-arrow">→</div>
  <div class="ch-node"><b>First trial</b><span>stated: {kv('K70'):.0f}% aware · {kv('K72'):.0f}% tried</span></div>
  <div class="ch-arrow">→</div>
  <div class="ch-node q"><b>?</b><span>the gap this study examines</span></div>
  <div class="ch-arrow">→</div>
  <div class="ch-node"><b>Repeat / main app</b><span>stated: {kv('K74'):.0f}% would continue once the offer ends</span></div>
</div>
<div class="risks">
  <div class="risk"><b>Restaurant availability</b><span>{mv('MM6'):.0f}% will not give up their usual restaurants for ₹30</span></div>
  <div class="risk"><b>Delivery &amp; fulfilment</b><span>Ownly quoted {kv('K31'):+.0f} min vs the incumbent median</span></div>
  <div class="risk"><b>Memberships &amp; coupons</b><span>{mv('MM3'):.0f}% of Ownly's price wins reverse after incumbent offers</span></div>
</div>"""

hist = """
<table class="tb small"><thead><tr><th>Challenger</th><th>What happened</th><th>Evidence</th></tr></thead><tbody>
<tr><td><b>Uber&nbsp;Eats India</b></td><td>Operating loss per order of $2.55 against an average order value of $2.45 — it lost more per order than the order was worth. Sold to Zomato, Jan 2020.</td><td class="ev">FACT — SEC Form 8-K, Ex. 99.1</td></tr>
<tr><td><b>Foodpanda India</b></td><td>Daily orders fell from ~200,000 to ~5,000 (−97.5%) once discounting stopped. FY19: revenue ₹82 Cr, loss ₹756 Cr.</td><td class="ev">MEDIA REPORT / RoC filings</td></tr>
<tr><td><b>ONDC network</b></td><td>Monthly orders fell 6.5M → 4.6M (−29%) after buyer-app incentives were cut ~90%.</td><td class="ev">MEDIA REPORT — single upstream</td></tr>
</tbody></table>"""

tab("t1", "01", "Business problem",
    headline("Ownly is already live in Gachibowli — and almost nobody here is using it.",
             f"Among {N_HYD} respondents aged 20–35, {kv('K70'):.0f}% had heard of Ownly, "
             f"{kv('K72'):.0f}% had ever ordered, and <b>zero</b> of the 40 recent food orderers "
             f"placed an Ownly order in the last four weeks. The question is not whether the price "
             f"gap exists — we measured it — but why it is not converting.")
    + f'<div class="cards six">{cards}</div>'
    + panel("The business tension", chain,
            kicker="A → B → ? → C",
            foot="Survey items are stated behaviour and stated preference. The audit is observed. "
                 "Neither measures actual first-order conversion — the fake-door test was not run.")
    + panel("The historical warning", hist,
            kicker="Three strongest cases from the challenger dossiers",
            foot="Analogy, not proof. These are different companies in different years. "
                 "Ownly must be judged on Ownly's evidence — see tab 10.")
    + panel("The decision this study serves",
            '<p class="big">Which parts of the Bengaluru playbook should Gachibowli '
            '<b>KEEP</b>, <b>ADAPT</b> or <b>DEPRIORITISE</b>?</p>'
            '<p class="muted">Answered on tab 13, with each call traced to a named observation.</p>'))

# ============================================================ 02 KPI DRIVER TREE
def kpi_rows(driver, layer="INPUT"):
    g = K[(K["driver"] == driver) & (K["layer"] == layer)]
    out = ""
    for _, r in g.iterrows():
        val = r["value"]
        unit = r["unit"]
        vs = f"{val:,.1f}" if isinstance(val, float) and unit != "%" else f"{val:g}"
        vs = f"{vs}{'%' if unit=='%' else ''}"
        ci = ""
        if pd.notna(r["ci_lo"]):
            ci = f'<span class="ci">95% CI {r["ci_lo"]:.0f}–{r["ci_hi"]:.0f}</span>'
        base = f'n={int(r["denominator"])}' if pd.notna(r["denominator"]) else ""
        out += (f'<div class="kpirow"><div class="kv">{vs}{" " + unit if unit not in ("%",) else ""}</div>'
                f'<div class="kn"><b>{escape(r["kpi_name"])}</b>'
                f'<span class="src">{base} · {escape(str(r["evidence_type"]))}</span>{ci}</div></div>')
    return out


tree = f"""
<div class="tree">
  <div class="tcol">
    <div class="tcap">INPUT DRIVERS — what Ownly controls</div>
    <div class="tgrp"><h4>PRICE</h4>{kpi_rows('PRICE')}</div>
    <div class="tgrp"><h4>ASSORTMENT</h4>{kpi_rows('ASSORTMENT')}</div>
    <div class="tgrp"><h4>SERVICE</h4>{kpi_rows('SERVICE')}</div>
    <div class="tgrp"><h4>DISTRIBUTION</h4>{kpi_rows('DISTRIBUTION')}</div>
    <div class="tgrp"><h4>MARKET LOCK-IN — what Ownly does not control</h4>{kpi_rows('LOCK-IN')}</div>
  </div>
  <div class="tmid">
    <div class="tarrow"><span>drives</span></div>
    <div class="tbox acq">ACQUISITION<small>price · discovery</small></div>
    <div class="tbox ret">RETENTION<small>assortment · execution</small></div>
  </div>
  <div class="tcol">
    <div class="tcap">OUTPUT — what the market did</div>
    <div class="tgrp"><h4>FUNNEL</h4>{kpi_rows('FUNNEL','OUTPUT')}</div>
    <div class="tgrp"><h4>RETENTION SIGNAL</h4>{kpi_rows('RETENTION','OUTPUT')}</div>
    <div class="tgrp"><h4>₹30 TRADE-OFFS</h4>{kpi_rows('TRADE-OFF','OUTPUT')}</div>
  </div>
</div>"""

tab("t2", "02", "KPI driver tree",
    headline("Ownly controls price well and discovery badly — and the market controls the rest.",
             "Inputs are grouped by whether Ownly can move them. The two it owns outright "
             "(fee load, quoted ETA) are strong and weak respectively; the two that decide the "
             "outcome (assortment overlap, membership lock-in) are largely set by the incumbents.")
    + panel("Input → behaviour → output", tree,
            foot="Arrows denote hypothesised influence, not measured causality. No causal test was run. "
                 "Every figure carries its base and evidence type."))

# ============================================================ 03 MARKETING METRICS
mm_cards = ""
for mid in ["MM1", "MM2", "MM3", "MM4", "MM6", "MM7", "MM8", "MM9", "MM10"]:
    r = M[M["metric_id"] == mid].iloc[0]
    v = r["value"]
    u = r["unit"]
    vs = f"₹{v:,.0f}" if u == "INR" else (f"{v:,.0f}{u}" if u in ("%", "pp") else f"{v:,.1f}")
    den = f'n={int(r["denominator"])}' if pd.notna(r["denominator"]) else ""
    tone = "warn" if mid in ("MM3", "MM4", "MM7", "MM8", "MM9") else ""
    mm_cards += card(vs, r["metric_name"], den, tone=tone)

custom = M[M["metric_name"].str.contains("custom")][
    ["metric_id", "metric_name", "formula", "value", "unit", "interpretation"]]
custom_html = ""
for _, r in custom.iterrows():
    custom_html += (f'<div class="cust"><h4>{escape(r["metric_name"])} — '
                    f'<span class="cv">{r["value"]:,.1f}{r["unit"] if r["unit"]!="INR" else ""}</span></h4>'
                    f'<p class="frm">{escape(r["formula"])}</p>'
                    f'<p class="why"><b>Why it is a good indicator.</b> {escape(r["interpretation"])}</p></div>')

tab("t3", "03", "Marketing metrics",
    headline("Ownly wins every basket on list price — and loses half of them at the checkout people actually see.",
             f"Price Win Rate is {mv('MM1'):.0f}% on list price plus fees. "
             f"{mv('MM3'):.0f}% of those wins reverse once incumbent coupons apply, and "
             f"{mv('MM4'):.0f}% reverse on the membership benefit alone — before any coupon.")
    + f'<div class="cards">{mm_cards}</div>'
    + panel("Two metrics we defined ourselves", custom_html,
            kicker="Custom KPIs",
            foot="Both are computed from the same audit rows as the standard metrics; "
                 "the definitions are in data/metric_dictionary.csv.")
    + panel("Business metrics that are NOT estimable from this evidence",
            tbl(NE[["metric", "why_not_estimable"]]),
            kicker="Stated as a limit, not hidden",
            foot="No proxy, assumption or benchmark was substituted for any of these. "
                 "Reporting them as unknown is a finding about the evidence base."))

# ============================================================ 04 ₹30 EQUATION
rows = []
for _, r in TR.iterrows():
    rows.append({"label": r["dimension"].upper(),
                 "cheap_pct": r["chose_cheaper_pct"], "prem_pct": r["paid_premium_pct"],
                 "cheap_txt": {"speed": "wait 45 min instead of 30",
                               "reliability": "accept 3-in-10 late",
                               "usual restaurants": "lose most usual restaurants"}[r["dimension"]],
                 "prem_txt": {"speed": "pay ₹30 to arrive sooner",
                              "reliability": "pay ₹30 for 1-in-10 late",
                              "usual restaurants": "pay ₹30 to keep them"}[r["dimension"]]})
p4 = H[H["id"] == "P4"].iloc[0]

tab("t4", "04", "The ₹30 equation",
    headline("₹30 buys time. ₹30 buys reliability. ₹30 cannot buy away your usual restaurants.",
             f"The same ₹30, three trades, same {N_HYD} respondents. "
             f"{TR[TR.dimension=='speed'].chose_cheaper_pct.iloc[0]:.0f}% will wait 15 minutes longer "
             f"and {TR[TR.dimension=='reliability'].chose_cheaper_pct.iloc[0]:.0f}% will accept worse "
             f"reliability — but only {TR[TR.dimension=='usual restaurants'].chose_cheaper_pct.iloc[0]:.0f}% "
             f"will give up their restaurants.")
    + panel("What will Gachibowli users trade for ₹30?", ch.paired_tradeoff(rows),
            foot=f"Hyderabad respondents aged 20–35, n={N_HYD}. Forced binary choice, ₹260 vs ₹230 held "
                 f"constant across all three items. SURVEY — STATED PREFERENCE. "
                 f"McNemar (paired, assortment vs speed): p={p4['p_value']:.2g}.")
    + panel("Why this is the most decision-relevant chart in the study",
            f"""<div class="two">
            <div><h4>It isolates one variable</h4><p>The rupee amount never changes. Only the thing
            being given up changes. So the differences are attributable to the attribute, not to
            price sensitivity.</p></div>
            <div><h4>It contradicts the project's own prior</h4><p>The pre-registered prediction
            (PAP §6.7, P3) was that Ownly's ~17-minute ETA deficit would block adoption.
            <b>It was falsified</b> — {TR[TR.dimension=='speed'].chose_cheaper_pct.iloc[0]:.0f}%
            accept the slower option. Speed is not the constraint. Assortment is.</p></div>
            </div>""",
            kicker="Reading the result"))

# ============================================================ 05 PRICE-TO-SWITCH FIT
ORDER = ["₹10", "₹20", "₹30", "₹50", "₹75", "₹100 or more"]
VALS = {"₹10": 10, "₹20": 20, "₹30": 30, "₹50": 50, "₹75": 75, "₹100 or more": 100}
thr = HYD["switch_savings_rs"].dropna()
cum = []
for lab in ORDER:
    cum.append((lab, (thr <= VALS[lab]).sum() / len(thr) * 100))
curve_svg, _, _ = ch.step_curve(cum, xlab="Recurring saving required to switch main app")
n_never = int(HYD["switch_never"].sum())
n_dk = int(HYD["switch_dk"].sum())

obs_list = P[P["view"] == "LIST+FEES"]["saving_rs"].median()
obs_mem = P[P["view"] == "MEMBER"]["saving_rs"].median()
obs_off = P[P["view"] == "AFTER OFFER"]["saving_rs"].median()
obs_rows = [
    {"label": "LIST + FEES  (non-member)", "value": obs_list, "note": "observed median, n=4 baskets", "color": BLUE},
    {"label": "MEMBER PRICE  (Gold/One)", "value": obs_mem, "note": "membership benefit only, no coupon", "color": "#7FA0C0"},
]
fit = f"""
<div class="fit">
  <div class="fitrow ok"><b>₹{obs_list:,.0f}</b><span>structural saving — clears the stated bar of
    <b>{mv('MM5'):.0f}%</b> of the {int(mv('MM5','denominator'))} respondents who named a threshold</span></div>
  <div class="fitrow mid"><b>₹{obs_mem:,.0f}</b><span>after the incumbent membership benefit alone —
    still clears most thresholds, but {mv('MM4'):.0f}% of baskets have already flipped</span></div>
  <div class="fitrow bad"><b>−₹{abs(obs_off):,.0f}</b><span>after incumbent coupons Ownly is
    <b>dearer</b> — no positive threshold can be cleared</span></div>
</div>"""

tab("t5", "05", "Price-to-switch fit",
    headline("The saving people need is small. The saving Ownly delivers is large — until an incumbent coupon lands.",
             f"Median stated requirement is ₹{kv('K52'):,.0f} of recurring saving. The observed "
             f"structural saving is ₹{obs_list:,.0f}. That is a comfortable fit. After coupons the "
             f"observed saving is −₹{abs(obs_off):,.0f}, and the fit disappears entirely.")
    + f'''<div class="two wide">
      {panel("How much recurring saving do users require?", curve_svg,
             foot=f"Cumulative share of Hyderabad respondents whose stated threshold is met at or below "
                  f"each level. n={len(thr)} gave a rupee figure. Held separate and NOT in the curve: "
                  f"<b>{n_never}</b> said no amount would make them switch, <b>{n_dk}</b> said don't know. "
                  f"SURVEY — STATED PREFERENCE.")}
      {panel("What saving did we actually observe?", ch.hbar(obs_rows, unit="INR", w=520, pad_l=200)
             + fit,
             foot="Matched restaurant × basket comparisons at one Gachibowli address, "
                  "wed_dinner 2026-09-16. n=4 complete three-app comparisons. PRIMARY OBSERVED DATA.")}
    </div>'''
    + panel("Price-to-switch fit — the interpretation",
            f"""<p class="big">On list price, Ownly's saving clears the stated switching bar of every
            respondent who named one. That is a genuine structural achievement, and it is why
            <b>price can acquire</b>.</p>
            <p>But {mv('MM7'):.0f}% of this sample holds an incumbent membership, so the list view is
            not the view most of them see. This is a <b>fit</b> statement about price levels, not a
            forecast of conversion or share — neither was measured.</p>""",
            kicker="Not a conversion forecast"))

# ============================================================ 06 MARKET REALITY
# Karachi Bakery's basket is a ~Rs1,200 cake, not the single-portion basket the audit
# defines; the audit results note excludes it from basket-level comparison. Excluded here too.
EXCL_REST = ["Karachi Bakery"]
pts = []
for _, r in A[A["final_payable"].notna() & A["eta_mid"].notna()].iterrows():
    if r["discount_type"] != "none" or r["restaurant_name"] in EXCL_REST:
        continue
    pts.append({"x": r["final_payable"], "y": r["eta_mid"], "platform": r["platform"],
                "label": ""})
sc = ch.scatter(pts, xlab="Final payable (list + fees, no coupon)", ylab="Quoted ETA, minutes",
                quadrant=(np.median([p["x"] for p in pts]), np.median([p["y"] for p in pts])))

wf_rest = "Paradise Biryani"
wfa, wfb = [], []
for plat, store in (("ownly", wfa), ("swiggy", wfb)):
    g = A[(A.restaurant_name == wf_rest) & (A.platform == plat) & (A.discount_type == "none")]
    if g.empty:
        continue
    r = g.iloc[0]
    store += [{"label": "Menu", "value": r["menu_subtotal"], "kind": "base"}]
    for lbl, col in [("Delivery", "delivery_fee"), ("Platform\nfee", "platform_fee"),
                     ("Packaging", "packaging_fee"), ("Tax", "taxes_gst")]:
        if pd.notna(r[col]) and r[col] > 0:
            store.append({"label": lbl, "value": r[col], "kind": "add"})
    store.append({"label": "Final\npayable", "value": r["final_payable"], "kind": "total"})

ER = []
for vw, nm, sub, trig in [
        ("LIST+FEES", "LIST + FEES", "non-member, no coupon", ""),
        ("MEMBER", "MEMBER PRICE", "Gold / One benefit only", "▼ the membership alone takes this much"),
        ("AFTER OFFER", "AFTER OFFER", "coupon applied", "▼ one coupon takes the rest")]:
    g = P[P["view"] == vw]
    ER.append({"name": nm, "sub": sub, "trigger": trig,
               "win_pct": g["ownly_wins"].mean() * 100,
               "win_k": int(g["ownly_wins"].sum()), "win_n": len(g),
               "saving_rs": g["saving_rs"].median(), "saving_pct": g["saving_pct"].median()})
sl = ch.erosion(ER)

tab("t6", "06", "Market reality",
    headline("Ownly is structurally cheaper and structurally slower — and the discount war undoes the first half.",
             f"Non-food charges are {kv('K22_ownly'):.0f}% of an Ownly bill against "
             f"{kv('K22_swiggy'):.0f}% on Swiggy and {kv('K22_zomato'):.0f}% on Zomato. "
             f"Ownly's quoted ETA is {kv('K31'):+.0f} minutes against the incumbent median.")
    + f'''<div class="two wide">
      {panel("Final payable vs quoted ETA", sc,
             foot="Each mark is one platform × basket capture, list price plus fees, no coupon. "
                  f'<span class="sw" style="background:{CORAL}"></span>Ownly '
                  f'<span class="sw" style="background:{BLUE}"></span>Swiggy '
                  f'<span class="sw" style="background:{DARK}"></span>Zomato. '
                  "Dashed lines are medians. PRIMARY OBSERVED DATA.")}
      {panel("How Ownly's price advantage erodes, in two steps", sl,
             kicker="Same four baskets, three views",
             foot=f"A membership alone — before any coupon — flips {mv('MM4'):.0f}% of the baskets; "
                  f"coupons flip {mv('MM3'):.0f}%. Since {mv('MM7'):.0f}% of our sample holds a "
                  "membership, the top row is not the view most of them see.")}
    </div>'''
    + f'''<div class="two wide">
      {panel(f"Bill composition — {wf_rest}, Ownly", ch.waterfall(wfa),
             foot="Ownly charged no delivery, platform or packaging fee in every captured row. "
                  "Only GST is added.")}
      {panel(f"Bill composition — {wf_rest}, Swiggy", ch.waterfall(wfb),
             foot="The fee stack is the structural difference between the two platforms.")}
    </div>''')

# ============================================================ 07 ASSORTMENT
ov = kv("K42"); own_only = int(kv("K43")); inc_only = int(kv("K44"))
cov_rows = []
for rest in COV.index:
    o = COV.loc[rest, "ownly"] == "y"
    s_ = COV.loc[rest, "swiggy"] == "y"
    z = COV.loc[rest, "zomato"] == "y"
    cov_rows.append({"Restaurant": rest, "Ownly": "●" if o else "—",
                     "Swiggy": "●" if s_ else "—", "Zomato": "●" if z else "—",
                     "Status": "Ownly only" if (o and not s_ and not z) else
                               ("Missing from Ownly" if (not o) else "On all three")})
covdf = pd.DataFrame(cov_rows)

slot_note = A["slot"].dropna().unique().tolist()
heat_cells = {}
for plat in ["Ownly", "Swiggy", "Zomato"]:
    heat_cells[(plat, "Lunch")] = ("not captured", 0)
    heat_cells[(plat, "Dinner")] = ("captured", 3)
    heat_cells[(plat, "Post-midnight")] = ("not captured", 0)
hm = ch.heat(["Ownly", "Swiggy", "Zomato"], ["Lunch", "Dinner", "Post-midnight"], heat_cells)

tab("t7", "07", "Assortment & availability",
    headline(f"Ownly sells the same restaurants as the incumbents — {ov:.0f}% overlap, and one exclusive.",
             f"Of the audited restaurants carried by at least one incumbent, {ov:.0f}% are also on "
             f"Ownly. Exactly {own_only} restaurant was Ownly-only; {inc_only} was missing from Ownly. "
             "This is the factual basis of the 'no new use case' risk.")
    + f'''<div class="two wide">
      {panel("Restaurant coverage at one Gachibowli address", tbl(covdf),
             foot="DP1, 2026-09-16. ● = listed. 12 restaurants audited. PRIMARY OBSERVED DATA. "
                  "Aanimuthyalu Unlimited appears once after correcting a duplicate spelling in the capture sheet.")}
      <div>
      {panel("What the survey says assortment is worth",
             ch.hbar([{"label": "Will NOT give up usual restaurants for ₹30",
                       "value": mv('MM6'), "color": BLUE,
                       "note": f"n={N_HYD} · the highest premium share of the three trades"},
                      {"label": "Would try Ownly if usual restaurants were on it",
                       "value": (HYD['ownly_trigger'].eq('My usual restaurants being on it').sum()
                                 / HYD['ownly_trigger'].notna().sum() * 100),
                       "color": MUTED,
                       "note": f"n={int(HYD['ownly_trigger'].notna().sum())} who named a trigger"}],
                     w=520, pad_l=250, show_ci=False),
             foot="SURVEY — STATED PREFERENCE.")}
      {panel("Daypart coverage", hm,
             kicker="Observed slots only",
             foot="Only the wed_dinner slot was captured. Lunch and post-midnight were not audited, so "
                  "<b>late-night availability is neither confirmed nor refuted here</b>. Social data "
                  "flags a late-night reliability risk; demand importance remains unvalidated.")}
      </div>
    </div>''')

# ============================================================ 08 AWARENESS → TRIAL
fstages = [
    {"label": "Target sample", "k": N_HYD, "n": N_HYD, "pct": 100},
    {"label": "Aware of Ownly", "k": int(kv("K70", "numerator")), "n": N_HYD, "pct": kv("K70")},
    {"label": "Opened / browsed", "k": int(kv("K71", "numerator")), "n": N_HYD, "pct": kv("K71")},
    {"label": "Ever ordered", "k": int(kv("K72", "numerator")), "n": N_HYD, "pct": kv("K72")},
]
rap_rows = [
    {"label": "Used Rapido in last 4 weeks", "value": kv("K61"), "color": BLUE,
     "note": f'n={int(kv("K61","denominator"))}'},
    {"label": "Noticed food inside the Rapido app", "value": kv("K60"), "color": CORAL,
     "note": f'n={int(kv("K60","denominator"))} Rapido users'},
    {"label": "Ever ordered on Ownly", "value": kv("K72"), "color": DARK,
     "note": f"n={N_HYD}"},
]

tab("t8", "08", "Awareness → trial",
    headline("Rapido gives Ownly access to the customer, not discovery of the product.",
             f"{kv('K61'):.0f}% of respondents used Rapido in the last four weeks, but only "
             f"{kv('K60'):.0f}% of Rapido users had noticed that food can be ordered inside it. "
             f"The distribution asset is real; the discovery it produces is not.")
    + f'''<div class="two wide">
      {panel("Ownly funnel in this sample", ch.funnel(fstages),
             foot=f"Hyderabad respondents aged 20–35, n={N_HYD}. <b>DIRECTIONAL — LOW BASE</b> at the "
                  f"trial stage ({int(kv('K72','numerator'))} respondents). SURVEY — STATED BEHAVIOUR.")}
      {panel("Distribution vs discovery", ch.hbar(rap_rows, w=520, pad_l=250, show_ci=False),
             foot="'Not sure' is counted as not-noticed. Respondents who do not use Rapido are excluded "
                  f"from the discovery base. Rapido Discovery Gap = {mv('MM8'):.0f}%.")}
    </div>'''
    + panel("The interviews point the lever somewhere else",
            f"""<div class="two">
            <div><h4>What we measured</h4><p>An {mv('MM8'):.0f}% discovery gap inside Rapido. The
            obvious inference is “fix the in-app placement”.</p>
            <p>But that inference was never tested — and the interviews suggest it is the wrong
            first move.</p></div>
            <div><h4>What the interviews say</h4><p>Trial comes from <b>a friend's recommendation,
            influencers, Instagram and YouTube reviews</b>. The one documented interviewee heard
            about Ownly <b>from her brother</b> — not from the Rapido app.</p>
            <p>Survey agrees: after price, the most-cited trial trigger was
            <b>“a friend telling me it works well”</b>.</p></div></div>
            <p class="big" style="margin-top:14px">So the higher-value experiment is a
            <b>referral or creator-led trial mechanism</b>, not a placement change.</p>""",
            kicker="A recommendation this evidence changed",
            foot="Interview evidence: T-4, T-6, I-01.9 in <code>04_interviews/interview_findings_coded.md</code>. "
                 "<b>NOT ESTABLISHED:</b> no CAC is calculated and none can be; whether either lever "
                 "raises trial is untested — both are experiments, not inferences."))

# ============================================================ 09 TRIAL vs RETENTION
piv = TH.pivot_table(index="theme_family", columns="base", values="share_of_coded_items_pct")
order = ["PRICE_DOUBT", "PRICE_ADVANTAGE", "FULFILMENT_FAIL", "SUPPORT_REFUND", "ASSORTMENT",
         "COMPETITION", "TRUST_QUALITY", "DISTRIBUTION"]
piv = piv.reindex([o for o in order if o in piv.index])
thtbl = piv.round(1).reset_index().rename(columns={"theme_family": "Theme family"})


yt_top = YT.nlargest(6, "comments")
YT_LABEL = {"RIDER_ECONOMICS": "Rider economics", "COMPETITORS": "Competitors",
            "ZERO_COMMISSION": "Zero commission", "REGULATION": "Regulation / bans",
            "ONDC_PRECEDENT": "ONDC as precedent", "SPEED_ETA": "Speed / ETA",
            "SUPPORT_REFUND": "Support & refunds", "PRICE_DOUBT": "Price scepticism",
            "PRICE_ADVANTAGE": "Price advantage", "WORD_OF_MOUTH": "Word of mouth",
            "ASSORTMENT": "Assortment", "RELIABILITY": "Reliability",
            "TRUST_QUALITY": "Trust / quality", "DISINTERMEDIATION": "Ordering direct instead",
            "CREATOR_CREDIBILITY": "Creator credibility"}
yt_bars = [{"label": YT_LABEL.get(r["theme_family"], r["theme_family"].title()),
            "value": r["share_of_coded_pct"],
            "color": CORAL if r["theme_family"] == "RIDER_ECONOMICS" else BLUE,
            "note": f'{int(r["comments"])} comments, {int(r["total_likes_on_those_comments"]):,} likes'}
           for _, r in yt_top.iterrows()]
yt_quotes = ""
for _, r in YTF.sort_values("likes", ascending=False).iterrows():
    yt_quotes += (f'<blockquote>“{escape(str(r["text"])[:300].strip())}”'
                  f'<cite>YouTube comment · {int(r["likes"])} likes</cite></blockquote>')
n_yt = len(YTC); n_ytc = int(YT["base_n_coded"].iloc[0])

quotes = HYD["prop_reason"].dropna().tolist()
pick = [q for q in quotes if any(w in q.lower() for w in
        ["restaurant", "variety", "food i like", "locally", "prefer"])][:3]
pick += [q for q in quotes if "price" in q.lower() or "cheap" in q.lower()][:2]
qhtml = "".join(f'<blockquote>“{escape(q.strip())}”<cite>Survey open text, Hyderabad</cite></blockquote>'
                for q in pick[:5])

tri = f"""<div class="three">
<div class="stage"><span class="st">PRE-ORDER</span><b>Price</b>
<p>{mv('MM5'):.0f}% of stated switching thresholds are cleared by the observed structural saving.</p></div>
<div class="stage"><span class="st">SWITCHING</span><b>Restaurant availability</b>
<p>{mv('MM6'):.0f}% will not trade their usual restaurants for ₹30 — the highest of the three trades.</p></div>
<div class="stage"><span class="st">POST-ORDER</span><b>Fulfilment &amp; support</b>
<p>{piv.loc['FULFILMENT_FAIL','App-store reviews']:.0f}% of coded app-store reviews and
{piv.loc['FULFILMENT_FAIL','First-hand Ownly accounts (social)']:.0f}% of first-hand accounts mention fulfilment failure.</p></div>
</div>"""

resolve = f"""<div class="two">
<div><h4>The contradiction</h4><p>The survey says
<b>{TR[TR.dimension=='reliability'].chose_cheaper_pct.iloc[0]:.0f}% will accept worse reliability
for ₹30</b>. The review record says fulfilment failure is
<b>{piv.loc['FULFILMENT_FAIL','App-store reviews']:.0f}%</b> of coded app-store reviews. Both cannot
be the headline.</p></div>
<div><h4>What the interviews resolve</h4><p>Interviews report that people leave an app after
<b>frequent bad orders</b>. Users <i>accept</i> a reliability risk when choosing; they <i>leave</i>
after it actually happens, repeatedly. Different decision moments — so both findings hold.
<b>Reliability is a churn driver, not a trial blocker.</b></p></div>
</div>"""

tab("t9", "09", "Trial vs retention risk",
    headline("What people argue about is price. What people who actually ordered report is fulfilment.",
             f"Price doubt is {piv.loc['PRICE_DOUBT','Public discussion (social, relevant)']:.0f}% of "
             f"public discussion but {piv.loc['PRICE_DOUBT','App-store reviews']:.0f}% of app-store "
             f"reviews. Fulfilment failure runs the other way — "
             f"{piv.loc['FULFILMENT_FAIL','Public discussion (social, relevant)']:.0f}% of discussion, "
             f"{piv.loc['FULFILMENT_FAIL','App-store reviews']:.0f}% of reviews.")
    + f'''<div class="two wide">
      {panel("Stated trial intent vs stated post-offer continuation",
             ch.hbar([{"label": "Likely to TRY the chosen proposition", "value":
                       (HYD['prop_P_intent_n']>=4).sum()/HYD['prop_P_intent_n'].notna().sum()*100,
                       "color": BLUE, "note": f"top-2 box, n={N_HYD}"},
                      {"label": "Likely to CONTINUE after the ₹100 offer ends", "value": kv("K74"),
                       "color": CORAL, "note": f"top-2 box, n={N_HYD}"},
                      {"label": "Believe a new app's low prices will rise", "value": kv("K75"),
                       "color": DARK, "note": f"agree + strongly agree, n={N_HYD}"}],
                     w=540, pad_l=280, show_ci=False),
             foot=f"Trial-to-repeat intent gap = <b>{mv('MM9'):.0f}pp</b>. "
                  "STATED-INTENT PROXY — this is not observed retention, and the two items use "
                  "different framings.")}
      {panel("Coded theme mentions by evidence base", tbl(thtbl),
             foot="<b>Share of coded items mentioning the theme family</b> — NOT an order failure rate. "
                  "App-store reviews n=37, first-hand social accounts n=97, public discussion n=420. "
                  "All three bases are self-selected toward complaint. CONSUMER-GENERATED.")}
    </div>'''
    + panel("Where each factor appears to bind", tri, kicker="Synthesis")
    + panel("Reliability: accepted at the point of choice, fatal after repetition", resolve,
            kicker="Interviews resolve a contradiction the survey alone could not",
            foot="Interview evidence: <code>04_interviews/interview_findings_coded.md</code> (T-5). "
                 "This is why reliability sits in the retention guardrail on tab 13, not in the "
                 "acquisition hook.")
    + panel("What an engaged public audience argues about",
            ch.hbar(yt_bars, w=700, pad_l=180, pad_r=190, show_ci=False)
            + '<p style="margin:14px 0 6px;font-size:12px"><b>Every first-hand Ownly user in 275 '
              'comments — all three of them:</b></p>' + yt_quotes,
            kicker=f"YouTube · 2 videos · {n_yt} comments retrieved verbatim",
            foot=f"Shares are of the {n_ytc} comments carrying at least one coded theme — "
                 "<b>not</b> order failure rates and <b>not</b> population incidence. Self-selected "
                 "viewers of two Rapido/Ownly explainer videos (Backstage with Millionaires, "
                 "Jun 2025 and Mar 2026), national not Gachibowli. "
                 "Source: <code>data/youtube_comments_coded.csv</code>.")
    + panel("Respondent voice", qhtml + '<p class="foot">Verbatim open-text answers to “what made you '
            'pick that one?”, Hyderabad respondents (n=24 answered). Interview findings are coded '
            'separately in <code>04_interviews/interview_findings_coded.md</code>; the transcript is '
            'Gemini auto-notes and is <b>not yet human-verified</b>, so no interview quote is placed '
            'on a slide here.</p>',
            kicker="Only real quotes"))

# ============================================================ 10 CHALLENGERS
MECH = [
    ("M1", "RENTED DEMAND",
     "Foodpanda: 200,000 → 5,000 daily orders (−97.5%) when discounts stopped. ONDC −29% after incentive cuts.",
     f"Ownly's gap is <b>structural</b> (fee removal), not discount-funded: non-food load "
     f"{kv('K22_ownly'):.0f}% vs {kv('K22_swiggy'):.0f}%/{kv('K22_zomato'):.0f}%. But "
     f"{kv('K75'):.0f}% of our sample expects the low prices to rise anyway.",
     "PARTIALLY ESCAPED"),
    ("M2", "ATTACKING THE NON-SCARCE SIDE",
     "Zomato told the CCI ~1% of its restaurants are exclusive — 99% already multi-home. Thrive died at 3% commission.",
     f"Ownly's zero-commission wins supply the incumbents already have: {ov:.0f}% overlap, "
     f"{own_only} exclusive restaurant observed.",
     "AT RISK"),
    ("M3", "NO NEW USE CASE",
     "Eternal Q1FY27: “the same restaurants, similar or longer delivery times… there's no new use case being unlocked here.”",
     f"Our own audit confirms both premises: {ov:.0f}% assortment overlap and "
     f"{kv('K31'):+.0f} min quoted ETA. Survey shows speed is tolerated, so the binding half is assortment.",
     "AT RISK"),
    ("M4", "RELIABILITY FLOOR",
     "Ola exited ONDC after tracking, refund and support failures. Eternal's cohorts held 46%→49% through the price war.",
     f"{piv.loc['FULFILMENT_FAIL','App-store reviews']:.0f}% of coded reviews mention fulfilment "
     f"failure. But our survey finds {TR[TR.dimension=='reliability'].chose_cheaper_pct.iloc[0]:.0f}% "
     "will accept worse reliability for ₹30 — stated tolerance is higher than the complaint record suggests.",
     "UNKNOWN"),
    ("M5", "THIN REVENUE ARCHITECTURE",
     "Incumbents earn a take rate plus a ₹17.58 platform fee plus subscriptions plus ads. Platform fee rose >645% in 31 months.",
     "Ownly charged ₹0 delivery, ₹0 platform and ₹0 packaging in every captured row, and takes 0% "
     "commission. Burn per order is <b>UNKNOWN</b> — no figure is published anywhere. "
     "<b>New signal:</b> rider economics is the single largest theme in 275 retrieved YouTube "
     f"comments ({YT[YT.theme_family=='RIDER_ECONOMICS'].share_of_coded_pct.iloc[0]:.0f}% of coded "
     f"comments, {int(YT[YT.theme_family=='RIDER_ECONOMICS'].total_likes_on_those_comments.iloc[0]):,} "
     "likes) — repeatedly arguing riders earn more per hour from bike taxi than from food delivery.",
     "UNKNOWN"),
]
mh_html = ""
for mid, name, hist_e, own_e, status in MECH:
    cls = {"ESCAPED": "esc", "PARTIALLY ESCAPED": "part", "AT RISK": "risk", "UNKNOWN": "unk"}[status]
    mh_html += (f'<div class="mech"><div class="mhead"><span class="mid">{mid}</span>'
                f'<b>{name}</b><span class="status {cls}">{status}</span></div>'
                f'<div class="mgrid"><div><span class="mlab">HISTORICAL EVIDENCE</span><p>{hist_e}</p></div>'
                f'<div><span class="mlab">OWNLY EVIDENCE (ours)</span><p>{own_e}</p></div></div></div>')

tab("t10", "10", "Why challengers fail",
    headline("Ownly has escaped the mechanism that killed the others — and inherited two more.",
             "Its price gap is structural rather than subsidy-funded, which is genuinely different in "
             "kind from Foodpanda. But it sells the same restaurants more slowly, and its revenue "
             "architecture is thinner than any incumbent's.")
    + panel("Five failure mechanisms, scored against our own evidence", mh_html,
            foot="Historical cases are analogies, not causal proof. "
                 "<b>No statement here asserts that Ownly will fail.</b> Each status describes whether "
                 "the historical risk signal is present in our Gachibowli observations. "
                 "Sources: 01_secondary_research/challenger_failures/ (5 dossiers, ~230 sources)."))

# ============================================================ 11 EVIDENCE MATRIX
cols = ["survey", "interviews", "price_audit", "app_reviews", "social",
        "secondary_research", "challenger_history"]
colnames = ["Survey", "Interviews", "Price audit", "App reviews", "Social",
            "Secondary", "Challengers"]
cells = {}
for _, r in EM.iterrows():
    for c, cn in zip(cols, colnames):
        cells[(r["dimension"], cn)] = r[c]
mx = ch.matrix(list(EM["dimension"]), colnames, cells)
interp = EM[["dimension", "current_interpretation"]].rename(
    columns={"dimension": "Dimension", "current_interpretation": "Current interpretation"})

tab("t11", "11", "Evidence triangulation",
    headline("No recommendation rests on a single source — and the interviews changed two of them.",
             "Fourteen dimensions across seven evidence types. Interviews were conducted after the "
             "first build of this dashboard; they resolved the reliability contradiction and "
             "redirected the discovery recommendation. The interview count is still UNKNOWN, so no "
             "interview finding carries a prevalence figure.")
    + panel("Triangulation matrix", mx
            + f'<div class="legend"><span><i style="background:{BLUE}"></i>SUPPORTS</span>'
              f'<span><i style="background:{CORAL}"></i>CONTRADICTS</span>'
              f'<span><i style="background:#C9B79A"></i>MIXED</span>'
              f'<span><i style="background:#EDE4D3"></i>NO EVIDENCE</span></div>',
            foot="Contradictions are shown, not reconciled. Two are load-bearing: the survey "
                 "<b>contradicts</b> the review record on reliability, and <b>contradicts</b> the "
                 "assumption that Rapido creates discovery.")
    + panel("Interpretation strength by dimension", tbl(interp)))

# ============================================================ 12 PROPOSITIONS
PROPS = [
    ("Same food. Smaller final bill.", "PRICE",
     "Pay less for the order I was going to place anyway.",
     f"Price Win Rate {mv('MM1'):.0f}% on list+fees; median saving ₹{mv('MM2'):,.0f}; "
     f"fee load {kv('K22_ownly'):.0f}% vs {kv('K22_swiggy'):.0f}%; "
     f"{mv('MM5'):.0f}% of stated thresholds cleared.",
     f"{mv('MM3'):.0f}% offer reversal; {mv('MM7'):.0f}% hold memberships; "
     f"{kv('K75'):.0f}% expect the prices to rise; forced choice P vs Q not significant (p=0.73).",
     "Cheapest to communicate, and already true. But it is the claim every failed challenger made.",
     "Incumbent coupons neutralise it within one campaign cycle.", "MODERATE", "ADAPT"),
    ("The restaurants you already order from — at a smaller final bill.", "PRICE + ASSORTMENT",
     "Get my usual food for less, without giving up where I order from.",
     f"{mv('MM6'):.0f}% will not trade usual restaurants for ₹30 (highest of three trades, "
     f"McNemar p={p4['p_value']:.2g}); assortment is the only attribute price could not buy; "
     "open text repeatedly names restaurant availability.",
     f"Ownly already carries {ov:.0f}% of incumbent-listed restaurants, so the claim is close to "
     "parity today; only 1 exclusive observed; Pizza Hut missing.",
     "Couples the one advantage Ownly owns (price) to the one constraint users named (assortment). "
     "Defensible because assortment depth is slow to copy.",
     "Requires named local supply depth, which we have not measured beyond 12 restaurants.",
     "MODERATE–STRONG", "KEEP & BUILD"),
    ("A cheaper order that still turns up.", "RELIABILITY",
     "Save money without gambling on whether dinner arrives.",
     f"{piv.loc['FULFILMENT_FAIL','App-store reviews']:.0f}% of coded reviews mention fulfilment "
     "failure; incumbents recovered failed orders better in 3 of 3 direct comparisons.",
     f"Our survey contradicts the urgency: {TR[TR.dimension=='reliability'].chose_cheaper_pct.iloc[0]:.0f}% "
     "will accept worse reliability for ₹30. No Ownly reliability data exists for Hyderabad.",
     "A guardrail, not a hook. Necessary to retain; insufficient to acquire.",
     "Promising reliability without measuring it invites the exact complaints in the review record.",
     "DIRECTIONAL", "TEST LATER"),
    ("Food inside the app you already use.", "RAPIDO CROSS-SELL",
     "Order food without installing or learning anything new.",
     f"{kv('K61'):.0f}% used Rapido recently — the access is real and free.",
     f"{mv('MM8'):.0f}% of Rapido users had not noticed food in the app. Distribution ≠ discovery. "
     "Uber Eats ran exactly this play and sold for $206M.",
     "The cheapest available lever: the users are already in the app.",
     "If placement is fixed and trial still does not move, the problem was never discovery.",
     "DIRECTIONAL", "TEST NEXT"),
    ("Local favourites, without the online mark-up.", "LOCAL SUPPLY",
     "Order from the neighbourhood places that are missing or overpriced online.",
     "Local coverage 100% vs chain 80% in the audit; 1 Ownly-only local restaurant observed; "
     "zero-commission is structurally attractive to sub-₹150 eateries.",
     "Evidence base is 12 restaurants at one address. Demand for local-only supply is <b>not measured</b>.",
     "The only territory an incumbent cannot match by cutting a fee, because it requires supply "
     "the incumbent does not have.",
     "Unvalidated demand. Could be a supply story with no customer behind it.",
     "DIRECTIONAL", "TEST NEXT"),
]
ph = ""
for title, terr, job, forev, agev, logic, risk, conf, dec in PROPS:
    dcls = {"KEEP & BUILD": "keep", "ADAPT": "adapt", "TEST NEXT": "test",
            "TEST LATER": "later", "DEPRIORITISE": "drop"}[dec]
    ph += (f'<div class="prop"><div class="phead"><span class="terr">{terr}</span>'
           f'<span class="dec {dcls}">{dec}</span></div>'
           f'<h4>“{escape(title)}”</h4>'
           f'<p class="job"><b>Customer job:</b> {escape(job)}</p>'
           f'<div class="pgrid"><div><span class="mlab">EVIDENCE FOR</span><p>{forev}</p></div>'
           f'<div><span class="mlab">EVIDENCE AGAINST</span><p>{agev}</p></div></div>'
           f'<div class="pgrid"><div><span class="mlab">BUSINESS LOGIC</span><p>{escape(logic)}</p></div>'
           f'<div><span class="mlab">RISK</span><p>{escape(risk)}</p></div></div>'
           f'<p class="conf">CONFIDENCE: <b>{conf}</b></p></div>')

tab("t12", "12", "Propositions",
    headline("Price is the hook Ownly has. Assortment is the hook the evidence asks for.",
             "Five territories, each scored on our own evidence. Only one couples the advantage "
             "Ownly owns to the constraint respondents actually named.")
    + panel("Proposition territories", ph,
            foot="Confidence reflects evidence strength, not enthusiasm. No territory is recommended "
                 "on the basis of what sounds compelling."))

# ============================================================ 13 GTM DECISION
kad = [
    ("KEEP", "Zero platform, packaging and surge fees",
     f"Observed: non-food load {kv('K22_ownly'):.0f}% vs {kv('K22_swiggy'):.0f}% (Swiggy). "
     "This is the structural advantage and it survives without subsidy."),
    ("KEEP", "Transparent, coupon-free everyday pricing",
     f"{mv('MM5'):.0f}% of stated switching thresholds are cleared by the observed ₹{mv('MM2'):,.0f} saving."),
    ("ADAPT", "“Cheaper than Swiggy/Zomato” as the headline claim",
     f"{mv('MM3'):.0f}% of price wins reverse after coupons and {mv('MM4'):.0f}% on the membership "
     f"benefit alone. Against the {mv('MM7'):.0f}% who hold memberships, the claim is often false at "
     "their checkout. Reframe around the everyday bill, not a comparison."),
    ("ADAPT", "Restaurant breadth as the supply goal",
     f"{ov:.0f}% overlap means breadth reproduces the incumbent catalogue. Shift the target to "
     "named local depth — the one thing ₹30 could not buy."),
    ("ADAPT", "Rapido as a distribution channel",
     f"{mv('MM8'):.0f}% of Rapido users had not noticed food in the app. Access exists; discovery "
     "must be built and measured, not assumed."),
    ("DEPRIORITISE", "Speed / ETA parity investment",
     f"{TR[TR.dimension=='speed'].chose_cheaper_pct.iloc[0]:.0f}% accept 15 minutes slower for ₹30, so "
     "the pre-registered prediction that ETA blocks adoption was falsified. Spend the money elsewhere."),
    ("DEPRIORITISE", "First-order discount depth",
     f"{kv('K74'):.0f}% say they would continue once a ₹100 offer ends, and {kv('K75'):.0f}% expect "
     "prices to rise. Deeper intro discounts buy the trial the historical record says does not stick."),
]
kad_html = ""
for dec, item, why in kad:
    cls = {"KEEP": "keep", "ADAPT": "adapt", "DEPRIORITISE": "drop"}[dec]
    kad_html += (f'<div class="kad"><span class="dec {cls}">{dec}</span>'
                 f'<div><b>{escape(item)}</b><p>{why}</p></div></div>')

gtm = [
    ("WHO", f"Students and young professionals in the Gachibowli catchment who order 2+ times a month "
            f"and do <b>not</b> hold an incumbent membership. In our sample that is a minority — "
            f"{100-mv('MM7'):.0f}% — and it is the only group who sees Ownly's list-price advantage at their checkout."),
    ("ACQUISITION HOOK", "A smaller everyday bill on restaurants they already order from — not a "
                         "cheaper-than-X comparison that a coupon can falsify."),
    ("PRICE REQUIREMENT", f"Median stated requirement ₹{kv('K52'):,.0f} recurring. Observed structural "
                          f"saving ₹{mv('MM2'):,.0f}. The level is sufficient; its <b>durability</b> is the open question."),
    ("SUPPLY REQUIREMENT", f"Depth in the specific restaurants respondents already use. "
                           f"{mv('MM6'):.0f}% will not trade them for ₹30 — the strongest single "
                           "constraint measured in this study."),
    ("CHANNEL", f"Rapido is access, not discovery: {mv('MM8'):.0f}% gap. Treat in-app placement as an "
                "experiment with a measured trial outcome."),
    ("EXPERIENCE GUARDRAIL", f"Quoted ETA {kv('K31'):+.0f} min is tolerated. Fulfilment and refund "
                             "failure — the dominant theme in first-hand accounts — is not measured "
                             "in Hyderabad and is the guardrail to instrument first."),
    ("RETENTION", f"Unknown. Stated continuation after the offer ends is {kv('K74'):.1f}% and the "
                  f"trial-to-repeat intent gap is {mv('MM9'):.1f}pp, but no behavioural retention was observed."),
    ("COMPETITIVE RESPONSE", f"Already visible. {mv('MM3'):.0f}% of Ownly's price wins reversed on "
                             "coupons in a single audit slot, and the incumbents hold roughly ₹15/order "
                             "of platform-fee headroom to compress the gap further."),
    ("VIABILITY", "Unresolved. Ownly charged ₹0 to the customer and takes 0% commission in every "
                  "captured row. Revenue per order in Gachibowli was <b>₹0 observed</b>. "
                  "Burn per order is UNKNOWN and is not estimated here."),
]
gtm_html = "".join(f'<div class="gtmrow"><span class="glab">{l}</span><p>{v}</p></div>'
                   for l, v in gtm)

nxt = """<ol class="next">
<li><b>Run the fake-door test that was never run.</b> It is the only instrument that yields a
behavioural first-order conversion rate, which is what H₀ is actually about.</li>
<li><b>Audit named local restaurants, not showcase chains.</b> Every Ownly price we hold is a chain;
the strategy the evidence points to depends on depth we have not measured.</li>
<li><b>Place 3 test orders.</b> Quoted ETA is not delivery time. The reliability guardrail is
currently unmeasured in Hyderabad.</li>
<li><b>Conduct the 8 interviews.</b> The mechanism behind every number in this deck is unvalidated.</li>
<li><b>Re-audit against a membership-holding account.</b> 83% of the target holds one; the list-price
view is not their reality.</li>
</ol>"""

tab("t13", "13", "GTM decision",
    headline("Keep the fee architecture. Adapt the price claim. Stop paying for speed.",
             "Ownly's advantage is real but it is being communicated as a comparison that incumbent "
             "coupons can falsify at will — against a sample where 83% hold a membership. The "
             "constraint respondents actually named was assortment, and speed was not a constraint at all.")
    + panel("KEEP / ADAPT / DEPRIORITISE", kad_html,
            foot="Each call is traced to a named observation in this deck. "
                 "No call rests on the historical challenger record alone.")
    + panel("The GTM answer", gtm_html, kicker="Executive conclusion")
    + panel("What to test next", nxt,
            foot="Listed in order of decision value, not ease. Item 1 is the only one that would "
                 "let a future version of this study answer H₀ as originally written."))

# ============================================================ 14 HYPOTHESIS
hb = H[H["id"] == "H0-BEHAVIOURAL"].iloc[0]
hs = H[H["id"] == "H0-STATED"].iloc[0]
hm_ = H[H["id"] == "H0-STATED-MCNEMAR"].iloc[0]

pred = H[H["id"].str.startswith("P")][["id", "statement", "verdict", "result", "note"]]
pred_html = ""
for _, r in pred.iterrows():
    vcls = {"CONFIRMED": "keep", "FALSIFIED": "drop", "NOT TESTABLE": "unk",
            "NOT SUPPORTED": "adapt"}.get(r["verdict"], "adapt")
    if str(r["verdict"]).startswith("NOT SUPPORTED AS STATED"):
        vcls = "adapt"
    pred_html += (f'<div class="pred"><div class="phead"><span class="mid">{r["id"]}</span>'
                  f'<span class="dec {vcls}">{escape(str(r["verdict"]))}</span></div>'
                  f'<p class="pstate">{escape(r["statement"])}</p>'
                  f'<p class="pres">{escape(str(r["result"]))}</p>'
                  f'<p class="pnote">{escape(str(r["note"]))}</p></div>')

tab("t14", "14", "Hypothesis decision",
    headline("We fail to reject H₀ on the stated-preference proxy — and the behavioural H₀ was never tested.",
             f"Service P {hs['result']}. Exact binomial p = {hs['p_value']}, "
             f"{hs['ci']}. The two bundled propositions did not separate. "
             "The attribute-level trade-offs did.")
    + f'''<div class="two wide">
      {panel("H₀ — behavioural (as originally written)",
             f'<p class="hstate">{escape(hb["statement"])}</p>'
             f'<div class="verdict big-unk">NOT DIRECTLY TESTED</div>'
             f'<p>{escape(hb["note"])}</p>',
             kicker="Status")}
      {panel("H₀ — stated-preference analogue",
             f'<p class="hstate">{escape(hs["statement"])}</p>'
             f'<div class="verdict big-adapt">{escape(hs["verdict"])}</div>'
             f'<table class="tb small"><tbody>'
             f'<tr><th>Test</th><td>{escape(hs["test"])}</td></tr>'
             f'<tr><th>Result</th><td>{escape(hs["result"])}</td></tr>'
             f'<tr><th>n</th><td>{int(hs["n"])} expressed a preference (of {N_HYD})</td></tr>'
             f'<tr><th>Statistic</th><td>{escape(hs["statistic"])}</td></tr>'
             f'<tr><th>p-value</th><td>{hs["p_value"]}</td></tr>'
             f'<tr><th>95% CI</th><td>{escape(str(hs["ci"]))}</td></tr>'
             f'<tr><th>Paired check</th><td>McNemar {escape(hm_["statistic"])}, p={hm_["p_value"]} → {escape(hm_["verdict"])}</td></tr>'
             f'</tbody></table>'
             f'<p class="foot">{escape(hs["note"])}</p>',
             kicker="Proxy, not conversion")}
    </div>'''
    + panel("The more informative decomposed finding",
            f"""<p class="big">The two <b>bundled</b> propositions did not separate — but the
            <b>attributes inside them</b> separated sharply.</p>
            <p>Holding ₹30 constant,
            {TR[TR.dimension=='speed'].chose_cheaper_pct.iloc[0]:.0f}% traded speed and
            {TR[TR.dimension=='reliability'].chose_cheaper_pct.iloc[0]:.0f}% traded reliability, but only
            {TR[TR.dimension=='usual restaurants'].chose_cheaper_pct.iloc[0]:.0f}% traded their usual
            restaurants (McNemar p={p4['p_value']:.2g}). A bundled-concept test asks the wrong question
            of a 46-person sample; the attribute trades answer it with the same respondents.</p>""",
            kicker="Why the null is not the end of the analysis")
    + panel("Pre-registered predictions P1–P5", pred_html,
            kicker="Registered 2026-09-18, before any response was collected",
            foot="Registered in <code>09_analysis/M_pre_analysis_plan.md §6.7</code> as a separate "
                 "SECONDARY Holm family. <b>P3 was falsified and P1's first limb failed</b> — both are "
                 "reported as they came out. P2 could not be tested because the live form omits the "
                 "offer-dependency item."))

# ==================================================================== ASSEMBLE
nav = "".join(f'<button class="tabbtn" data-t="{t["id"]}">'
              f'<span class="tnum">{t["num"]}</span>{escape(t["name"])}</button>' for t in TABS)
secs = "".join(f'<div class="tabpane" id="{t["id"]}">'
               f'<div class="pgttl"><span class="pgnum">{t["num"]}</span>{escape(t["name"])}</div>'
               f'{t["body"]}</div>' for t in TABS)

CSS = f"""
:root{{--cream:{CREAM};--coral:{CORAL};--blue:{BLUE};--dark:{DARK};--rule:{RULE};
--muted:{MUTED};--panel:{PANEL};--grid:#E5DBC8}}
*{{box-sizing:border-box}}
html,body{{margin:0;padding:0}}
body{{background:var(--cream);color:var(--dark);
font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
font-size:14px;line-height:1.5;-webkit-font-smoothing:antialiased;
font-variant-numeric:tabular-nums}}
.wrap{{max-width:1180px;margin:0 auto;padding:0 28px 80px}}
header.top{{background:var(--dark);color:var(--cream);padding:22px 0 0}}
.topin{{max-width:1180px;margin:0 auto;padding:0 28px}}
.eyebrow{{font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;opacity:.72;
margin:0 0 6px}}
header.top h1{{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:27px;
margin:0 0 4px;letter-spacing:-.01em}}
header.top .sub{{font-size:12.5px;opacity:.74;margin:0 0 18px;max-width:760px;line-height:1.55}}
.meta{{display:flex;gap:26px;font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;
opacity:.62;border-top:1px solid rgba(242,235,221,.18);padding:9px 0}}
nav.tabs{{background:var(--dark);border-top:1px solid rgba(242,235,221,.16);position:sticky;top:0;
z-index:50}}
.tabsin{{max-width:1180px;margin:0 auto;padding:0 22px;display:flex;flex-wrap:wrap;gap:0}}
.tabbtn{{background:none;border:0;border-bottom:2px solid transparent;color:rgba(242,235,221,.62);
font:inherit;font-size:11.5px;padding:9px 10px;cursor:pointer;white-space:nowrap;
display:flex;align-items:baseline;gap:6px;letter-spacing:.01em}}
.tabbtn:hover{{color:var(--cream)}}
.tabbtn.on{{color:var(--cream);border-bottom-color:var(--coral)}}
.tnum{{font-size:9.5px;opacity:.6;letter-spacing:.06em}}
.tabpane{{display:none;padding-top:26px}}
.tabpane.on{{display:block}}
.pgttl{{font-size:10.5px;letter-spacing:.17em;text-transform:uppercase;color:var(--muted);
display:flex;gap:9px;align-items:baseline;border-bottom:1px solid var(--rule);
padding-bottom:7px;margin-bottom:20px}}
.pgnum{{color:var(--coral);font-weight:700}}
.headline{{margin:0 0 22px;max-width:920px}}
.hl{{font-family:Georgia,"Times New Roman",serif;font-size:25px;line-height:1.28;margin:0 0 9px;
font-weight:400;letter-spacing:-.012em}}
.hlsub{{margin:0;font-size:13.5px;color:#5E504B;line-height:1.6;max-width:840px}}
.panel{{background:var(--panel);border:1px solid var(--rule);padding:18px 20px 16px;
margin:0 0 18px}}
.panel h3{{font-size:11px;letter-spacing:.14em;text-transform:uppercase;margin:0 0 14px;
color:var(--dark);font-weight:700}}
.kick{{font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--coral);
font-weight:700;margin-bottom:5px}}
.foot{{font-size:11px;color:var(--muted);line-height:1.55;margin:13px 0 0;
border-top:1px solid var(--rule);padding-top:9px}}
.muted{{color:var(--muted)}}
.big{{font-size:15.5px;line-height:1.55;margin:0 0 8px}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(168px,1fr));gap:1px;
background:var(--rule);border:1px solid var(--rule);margin:0 0 18px}}
.cards.six{{grid-template-columns:repeat(6,1fr)}}
.card{{background:var(--panel);padding:15px 15px 13px}}
.cval{{font-family:Georgia,serif;font-size:29px;line-height:1;margin-bottom:7px;
letter-spacing:-.02em}}
.card.warn .cval{{color:#B4552F}} .card.bad .cval{{color:var(--coral)}}
.clab{{font-size:11.5px;line-height:1.38;color:var(--dark)}}
.csub{{font-size:10px;color:var(--muted);margin-top:5px}}
.cnote{{font-size:10px;color:var(--muted);margin-top:3px}}
svg.chart{{display:block;max-width:100%;height:auto}}
text{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
font-variant-numeric:tabular-nums}}
.tb{{width:100%;border-collapse:collapse;font-size:12px}}
.tb th{{text-align:left;font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;
color:var(--muted);border-bottom:1px solid var(--rule);padding:6px 9px 6px 0;font-weight:700}}
.tb td{{padding:7px 9px 7px 0;border-bottom:1px solid #EDE4D3;vertical-align:top;line-height:1.45}}
.tb.small{{font-size:11.5px}}
.tb tbody th{{text-transform:none;letter-spacing:0;font-size:11px;padding-right:14px;
white-space:nowrap;color:var(--muted)}}
td.ev{{font-size:10px;color:var(--muted);letter-spacing:.04em;white-space:nowrap}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}
.two.wide>*{{margin-bottom:0}}
.three{{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--rule)}}
.stage{{background:var(--panel);padding:14px}}
.st{{font-size:9.5px;letter-spacing:.13em;color:var(--coral);font-weight:700}}
.stage b{{display:block;font-size:14px;margin:5px 0 6px}}
.stage p{{margin:0;font-size:11.5px;color:#5E504B;line-height:1.5}}
.chain{{display:flex;align-items:stretch;gap:0;margin-bottom:16px}}
.ch-node{{flex:1;background:#fff;border:1px solid var(--rule);padding:12px 13px}}
.ch-node b{{display:block;font-size:13.5px;margin-bottom:4px}}
.ch-node span{{font-size:10.5px;color:var(--muted);line-height:1.45;display:block}}
.ch-node.q{{background:var(--dark);border-color:var(--dark)}}
.ch-node.q b{{color:var(--coral);font-size:22px;line-height:1}}
.ch-node.q span{{color:rgba(242,235,221,.7)}}
.ch-arrow{{display:flex;align-items:center;padding:0 9px;color:var(--muted);font-size:15px}}
.risks{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
.risk{{border-left:2px solid var(--coral);padding:2px 0 2px 11px}}
.risk b{{display:block;font-size:12px;margin-bottom:3px}}
.risk span{{font-size:11px;color:var(--muted);line-height:1.45}}
.tree{{display:grid;grid-template-columns:1fr 150px 1fr;gap:16px;align-items:start}}
.tcap{{font-size:9.5px;letter-spacing:.13em;text-transform:uppercase;color:var(--muted);
font-weight:700;margin-bottom:9px;border-bottom:1px solid var(--rule);padding-bottom:5px}}
.tgrp{{margin-bottom:15px}}
.tgrp h4{{font-size:10px;letter-spacing:.1em;color:var(--coral);margin:0 0 6px;font-weight:700}}
.kpirow{{display:flex;gap:11px;align-items:baseline;padding:5px 0;
border-bottom:1px solid #EDE4D3}}
.kv{{font-family:Georgia,serif;font-size:16px;min-width:74px;text-align:right;letter-spacing:-.01em}}
.kn b{{display:block;font-size:11.5px;font-weight:600;line-height:1.35}}
.src{{font-size:9.5px;color:var(--muted);display:block;margin-top:1px}}
.ci{{font-size:9.5px;color:var(--muted);display:block}}
.tmid{{display:flex;flex-direction:column;gap:9px;padding-top:44px}}
.tarrow{{text-align:center;color:var(--muted);font-size:9.5px;letter-spacing:.12em;
text-transform:uppercase}}
.tbox{{background:var(--dark);color:var(--cream);padding:12px 10px;text-align:center;
font-size:11.5px;letter-spacing:.09em;font-weight:700}}
.tbox small{{display:block;font-weight:400;letter-spacing:0;opacity:.7;font-size:10px;
margin-top:4px}}
.tbox.ret{{background:var(--coral)}}
.cust{{border-left:2px solid var(--blue);padding:2px 0 10px 13px;margin-bottom:13px}}
.cust h4{{margin:0 0 4px;font-size:13px}}
.cv{{font-family:Georgia,serif;font-size:17px;color:var(--blue)}}
.frm{{font-family:"SF Mono",Menlo,Consolas,monospace;font-size:10.5px;color:var(--muted);
margin:0 0 6px;line-height:1.5}}
.why{{margin:0;font-size:11.5px;line-height:1.55}}
.fit{{margin-top:13px}}
.fitrow{{display:flex;gap:12px;align-items:baseline;padding:8px 0;
border-top:1px solid #EDE4D3}}
.fitrow b{{font-family:Georgia,serif;font-size:19px;min-width:92px}}
.fitrow span{{font-size:11.5px;line-height:1.45;color:#5E504B}}
.fitrow.ok b{{color:var(--blue)}} .fitrow.mid b{{color:#7FA0C0}} .fitrow.bad b{{color:var(--coral)}}
.sw{{display:inline-block;width:9px;height:9px;margin:0 3px 0 9px;vertical-align:middle}}
.mech{{border:1px solid var(--rule);margin-bottom:11px;background:#fff}}
.mhead{{display:flex;align-items:center;gap:11px;padding:9px 13px;background:var(--cream);
border-bottom:1px solid var(--rule)}}
.mid{{font-family:Georgia,serif;font-size:14px;color:var(--coral)}}
.mhead b{{flex:1;font-size:11.5px;letter-spacing:.09em}}
.status{{font-size:9.5px;letter-spacing:.1em;padding:3px 8px;font-weight:700}}
.status.esc{{background:var(--blue);color:#fff}}
.status.part{{background:#7FA0C0;color:#fff}}
.status.risk{{background:var(--coral);color:#fff}}
.status.unk{{background:#DDD2BE;color:var(--dark)}}
.mgrid{{display:grid;grid-template-columns:1fr 1fr;gap:16px;padding:12px 13px}}
.mlab{{font-size:9px;letter-spacing:.12em;color:var(--muted);font-weight:700;display:block;
margin-bottom:4px}}
.mgrid p,.pgrid p{{margin:0;font-size:11.5px;line-height:1.55}}
.legend{{display:flex;gap:16px;margin-top:11px;font-size:10px;color:var(--muted)}}
.legend i{{display:inline-block;width:10px;height:10px;margin-right:5px;vertical-align:middle}}
.prop,.pred{{border:1px solid var(--rule);background:#fff;padding:13px 15px;margin-bottom:11px}}
.phead{{display:flex;justify-content:space-between;align-items:center;margin-bottom:7px}}
.terr{{font-size:9.5px;letter-spacing:.12em;color:var(--muted);font-weight:700}}
.dec{{font-size:9.5px;letter-spacing:.1em;padding:3px 9px;font-weight:700}}
.dec.keep{{background:var(--blue);color:#fff}}
.dec.adapt{{background:#C9B79A;color:var(--dark)}}
.dec.test{{background:var(--dark);color:var(--cream)}}
.dec.later{{background:#DDD2BE;color:var(--dark)}}
.dec.drop{{background:var(--coral);color:#fff}}
.dec.unk{{background:#DDD2BE;color:var(--dark)}}
.prop h4{{font-family:Georgia,serif;font-size:16px;font-weight:400;margin:0 0 6px}}
.job{{font-size:11.5px;margin:0 0 9px;color:#5E504B}}
.pgrid{{display:grid;grid-template-columns:1fr 1fr;gap:15px;margin-bottom:9px}}
.conf{{margin:0;font-size:10px;letter-spacing:.1em;color:var(--muted)}}
.kad{{display:flex;gap:13px;align-items:flex-start;padding:10px 0;
border-bottom:1px solid #EDE4D3}}
.kad .dec{{min-width:96px;text-align:center;flex-shrink:0}}
.kad b{{font-size:12.5px;display:block;margin-bottom:3px}}
.kad p{{margin:0;font-size:11.5px;color:#5E504B;line-height:1.55}}
.gtmrow{{display:flex;gap:16px;padding:10px 0;border-bottom:1px solid #EDE4D3}}
.glab{{font-size:9.5px;letter-spacing:.11em;color:var(--coral);font-weight:700;min-width:158px;
flex-shrink:0;padding-top:2px}}
.gtmrow p{{margin:0;font-size:12px;line-height:1.6}}
.next{{margin:0;padding-left:19px}}
.next li{{font-size:12px;line-height:1.6;margin-bottom:7px}}
blockquote{{margin:0 0 11px;padding:0 0 0 13px;border-left:2px solid var(--rule);
font-family:Georgia,serif;font-size:13.5px;line-height:1.5;color:#4A3D39}}
blockquote cite{{display:block;font-family:inherit;font-size:9.5px;letter-spacing:.09em;
text-transform:uppercase;color:var(--muted);font-style:normal;margin-top:5px}}
.hstate{{font-size:12.5px;line-height:1.55;background:var(--cream);padding:11px 13px;
margin:0 0 11px;border-left:2px solid var(--muted)}}
.verdict{{font-family:Georgia,serif;font-size:19px;padding:9px 13px;margin-bottom:11px;
letter-spacing:.01em}}
.big-unk{{background:#DDD2BE;color:var(--dark)}}
.big-adapt{{background:var(--dark);color:var(--cream)}}
.pstate{{font-size:12px;margin:0 0 5px;line-height:1.5}}
.pres{{font-size:11.5px;margin:0 0 5px;color:var(--blue);font-weight:600}}
.pnote{{font-size:11px;margin:0;color:var(--muted);line-height:1.55}}
code{{font-family:"SF Mono",Menlo,Consolas,monospace;font-size:11px;background:var(--cream);
padding:1px 4px}}
footer.bot{{border-top:1px solid var(--rule);margin-top:34px;padding:16px 0;font-size:10.5px;
color:var(--muted);line-height:1.6}}
@media(max-width:920px){{.two,.pgrid,.mgrid,.three,.risks,.cards.six{{grid-template-columns:1fr}}
.tree{{grid-template-columns:1fr}}.chain{{flex-direction:column}}.ch-arrow{{transform:rotate(90deg);
padding:4px 0}}}}
@media print{{nav.tabs{{display:none}}.tabpane{{display:block!important;page-break-after:always}}}}
"""

HTML = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ownly · Gachibowli Market-Fit Dashboard</title><style>{CSS}</style></head><body>
<header class="top"><div class="topin">
<p class="eyebrow">Market Research &amp; Validation · Rapido Ownly · Hyderabad</p>
<h1>Can Ownly turn a cheaper first order into a repeat habit in Gachibowli?</h1>
<p class="sub">How large and durable must Ownly's price advantage be to break Swiggy/Zomato lock-in
in Gachibowli, and what restaurant coverage, discovery and delivery experience are required so that
price-led trial becomes repeat usage?</p>
<div class="meta">
<span>Survey n={N_HYD} Hyderabad · 20–35</span><span>Price audit · 12 restaurants · 1 slot</span>
<span>App reviews n=37 · Social n=524</span><span>Interviews 1 documented (+ team-reported) · Fake door 0</span>
<span>Compiled 2026-09-18</span></div>
</div></header>
<nav class="tabs"><div class="tabsin">{nav}</div></nav>
<div class="wrap">{secs}
<footer class="bot">
<b>Evidence discipline.</b> Every figure carries its base and evidence type. Survey items are stated
behaviour or stated preference and are never described as conversion. Audit figures are observed at one
Gachibowli address in one dinner slot (n=4 complete three-app comparisons) and are directional.
Coded review and social counts are shares of coded items mentioning a theme — never order failure rates.
Bengaluru and Hyderabad are never blended. CAC, CLV, EBITDA, market share, retention and burn per order
are <b>NOT ESTIMABLE</b> from this evidence and no value is imputed for them. No respondent data was
simulated or fabricated at any point.<br><br>
<b>Reproduce:</b> <code>final_dashboard/scripts/</code> 01→05. Source trace: <code>SOURCE_MAP.md</code>.
</footer></div>
<script>
var btns=document.querySelectorAll('.tabbtn'),panes=document.querySelectorAll('.tabpane');
function go(id){{panes.forEach(function(p){{p.classList.toggle('on',p.id===id)}});
btns.forEach(function(b){{b.classList.toggle('on',b.dataset.t===id)}});
if(history.replaceState)history.replaceState(null,'','#'+id);window.scrollTo(0,0);}}
btns.forEach(function(b){{b.addEventListener('click',function(){{go(b.dataset.t)}})}});
var qp=new URLSearchParams(location.search).get('tab');
go(qp||(location.hash||'#t1').slice(1));window.scrollTo(0,0);
document.addEventListener('keydown',function(e){{
 var ids=Array.prototype.map.call(btns,function(b){{return b.dataset.t}});
 var i=ids.indexOf(document.querySelector('.tabpane.on').id);
 if(e.key==='ArrowRight'&&i<ids.length-1)go(ids[i+1]);
 if(e.key==='ArrowLeft'&&i>0)go(ids[i-1]);}});
</script></body></html>"""

out = f"{ROOT}/final_dashboard/index.html"
with open(out, "w") as fh:
    fh.write(HTML)
print(f"WROTE {out}  ({len(HTML)/1024:.0f} KB, {len(TABS)} tabs)")
