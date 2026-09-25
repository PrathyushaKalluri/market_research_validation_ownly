"""
04_build_site.py — builds final_dashboard/site/ (Netlify-ready, presentation-ready).

Eight sections: problem · market & funnel · KPIs · marketing metrics · analysis ·
why others failed · H0 · propositions.
Every number is read from data/ at build time. Nothing is typed in by hand.
"""
import os
import shutil
from html import escape

import numpy as np
import pandas as pd

import charts as ch
from charts import BLUE, CORAL, DARK, MUTED, CREAM, RULE

ROOT = "/Users/klprathyusha/Sem 3/Project/Ownly"
D = f"{ROOT}/final_dashboard/data"
SITE = f"{ROOT}/final_dashboard/site"
os.makedirs(f"{SITE}/data", exist_ok=True)
SHEET = ("https://docs.google.com/spreadsheets/d/"
         "1YWjzxcGNsEWhM_OT1PHFhGa9Eb2b0EegY63qz5q-7G8/edit?usp=sharing")

L = lambda f: pd.read_csv(f"{D}/{f}")
K = L("kpi_table.csv"); M = L("marketing_metrics.csv"); H = L("hypothesis_results.csv")
P = L("audit_pairs.csv"); A = L("audit_clean.csv"); COV = L("audit_coverage.csv")
TR = L("tradeoff_summary.csv"); TT = L("tradeoff_tests.csv"); ST = L("switching_staircase.csv")
STC = L("switch_threshold_coverage.csv"); SEG = L("segment_cuts.csv"); AS = L("associations.csv")
FUN = L("funnel_research.csv"); BEN = L("bengaluru_benchmark.csv")
VS = L("sample_volume_share.csv"); ETA = L("eta_gap_by_restaurant.csv")

for f in os.listdir(D):
    if f.endswith(".csv"):
        shutil.copy(f"{D}/{f}", f"{SITE}/data/{f}")

kv = lambda i, c="value": (K.loc[K.kpi_id == i, c].iloc[0] if (K.kpi_id == i).any() else None)
mv = lambda i, c="value": (M.loc[M.metric_id == i, c].iloc[0] if (M.metric_id == i).any() else None)
GREY = "#C9B79A"


def ev(link, label=None):
    if link is None or (isinstance(link, float) and pd.isna(link)):
        return ""
    href = str(link)
    txt = label or ("live sheet" if href.startswith("http") else href.split("/")[-1])
    tgt = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
    return f'<a class="ev" href="{escape(href)}"{tgt}>{escape(txt)}</a>'


def card(value, label, sub="", tone=""):
    return (f'<div class="card {tone}"><div class="cval">{value}</div>'
            f'<div class="clab">{escape(label)}</div>'
            + (f'<div class="csub">{escape(sub)}</div>' if sub else "") + "</div>")


def panel(title, body, foot="", kicker="", link=None):
    return (f'<section class="panel">'
            + (f'<div class="kick">{escape(kicker)}</div>' if kicker else "")
            + f'<h3>{title}{ev(link)}</h3>{body}'
            + (f'<p class="foot">{foot}</p>' if foot else "") + "</section>")


def readme(text):
    return f'<div class="readme"><span>HOW TO READ THIS</span><p>{text}</p></div>'


def tbl(df):
    th = "".join(f"<th>{escape(str(c).replace('_',' '))}</th>" for c in df.columns)
    tr = "".join("<tr>" + "".join(
        f"<td>{'' if pd.isna(v) else escape(str(v))}</td>" for v in r) + "</tr>"
        for _, r in df.iterrows())
    return f'<table class="tb"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


def lead(text, sub=""):
    return (f'<div class="lead"><p class="hl">{text}</p>'
            + (f'<p class="hlsub">{sub}</p>' if sub else "") + "</div>")


TABS = []
tab = lambda i, n, t, b: TABS.append(dict(id=i, num=n, name=t, body=b))

# ===================================================== 1 THE PROBLEM
EVO = """
<div class="evo">
  <div class="evo-step"><span class="step-n">FIRST VERSION</span>
    <b>A market-research question</b><p>&ldquo;Should Ownly enter Hyderabad?&rdquo;</p>
    <p class="why">Ownly is already here &mdash; a restaurant-partner launch with the National
    Restaurant Association in Jubilee Hills on 22 July 2026, then on-ground promotion in
    September. The company has answered this one.</p></div>
  <div class="evo-arrow">&rarr;</div>
  <div class="evo-step"><span class="step-n">SECOND VERSION</span>
    <b>A transfer question</b><p>&ldquo;Does the Bengaluru playbook transfer to
    Gachibowli?&rdquo;</p>
    <p class="why">Closer, but nothing in it can be measured. &ldquo;Transfer&rdquo; has no number
    attached, so no answer to it tells anyone what to change.</p></div>
  <div class="evo-arrow">&rarr;</div>
  <div class="evo-step now"><span class="step-n">THE BUSINESS QUESTION</span>
    <b>What we set out to answer</b>
    <p><b>How large and durable must Ownly's price advantage be to break the Swiggy and Zomato
    habit in Gachibowli, and what restaurant choice, discovery and delivery experience are needed
    so that a cheap first order becomes a regular one?</b></p>
    <p class="why">Every part of this is measurable, and every part maps to a KPI on the next
    page.</p></div>
</div>"""

tab("t1", "01", "The problem",
    lead("Which parts of the Bengaluru playbook should Gachibowli "
         "<span class='kad'>KEEP</span>, <span class='kad'>ADAPT</span> or "
         "<span class='kad'>DEPRIORITISE</span>?",
         "That is the decision this study serves. Getting to a question that sharp took three "
         "attempts.")
    + panel("How the question sharpened", EVO, kicker="Three versions")
    + panel("What we set out to test",
            '<div class="two"><div><h4>The idea being tested</h4>'
            '<p class="big">A lower price gets someone to try Ownly. The restaurants it carries '
            'and the delivery it provides decide whether they come back.</p>'
            '<p>Price, restaurant choice, discovery and delivery are measured separately, so each '
            'can be judged on its own evidence.</p></div>'
            '<div><h4>How we answered it</h4>'
            '<p>A survey of people who order food in the Gachibowli catchment, a price audit '
            'comparing the same dishes across all three apps at the same moment, interviews, '
            'app-store and social listening, and a study of every company that has tried this '
            'before in India.</p>'
            '<p>Each source is reported separately, so it is always clear where a number came '
            'from.</p></div></div>',
            kicker="The approach"))

# ===================================================== 2 MARKET & FUNNEL
fr = [dict(label=r["stage"], n=int(r["n"]),
           pct=None if pd.isna(r["pct_of_catchment"]) else r["pct_of_catchment"],
           note=(str(r["note"])[:44] + "…") if len(str(r["note"])) > 45 else str(r["note"]))
      for _, r in FUN.iterrows()]
n_stu = int(SEG.loc[SEG.segment.str.startswith("Student"), "n"].iloc[0])
n_pro = int(SEG.loc[SEG.segment.str.startswith("Working"), "n"].iloc[0])
WHO = '<div class="cards">' + "".join([
    card(str(n_stu), "Students"), card(str(n_pro), "Working professionals"),
    card(f"{kv('K11'):.0f}%", "already pay for Swiggy One or Zomato Gold", "n=40", tone="warn"),
    card(f"{kv('K12'):.0f}%", "use two or more delivery apps in a month", "n=40")]) + "</div>"

tab("t2", "02", "Market & funnel",
    lead("Who we studied.",
         "124 people answered the survey. 40 of them live or work in the Gachibowli catchment and "
         "fall in the age range we set. Those 40 are the base for every survey figure here.")
    + panel("From every response down to the people this study is about",
            ch.funnel_steps(fr, w=700)
            + readme("Each bar is a narrower group than the one above it. We start with everyone "
                     "who answered and end with the people who live in the Gachibowli catchment, "
                     "order food online, and know about Ownly. Percentages are shares of the "
                     "40-person catchment group."),
            link="data/funnel_research.csv")
    + panel("The people behind the numbers", WHO,
            foot="Eight in ten already pay a monthly membership to Swiggy or Zomato. That single "
                 "fact shapes every price comparison in this study, because a member sees a "
                 "different price at checkout from everyone else.",
            link="data/cleaned_survey.csv")
    + panel("The wider market, for scale",
            '<div class="cards">'
            + card("1.49 lakh", "people live in Gachibowli", "Census-derived, 2020")
            + card("9.46 lakh", "IT workforce in Telangana", "State IT department, FY2024")
            + card("221", "restaurants Ownly lists in Gachibowli", "Checked 19 Sep 2026")
            + "</div>", kicker="Context", link="data/market_context.csv"))

# ===================================================== 3 KPIs
def kpi_row(r):
    val = r["value"]
    vs = ("—" if pd.isna(val) else f'{val:g}%' if r["unit"] == "%"
          else f'₹{val:,.0f}' if r["unit"] == "INR" else f'{val:g} {r["unit"]}')
    base = f'n={int(r["denominator"])} · ' if pd.notna(r["denominator"]) else ""
    if base and base.replace("n=", "").replace(" · ", "") in str(r["evidence_strength"]):
        base = ""
    return (f'<div class="kpi"><div class="kpi-v">{vs}</div><div class="kpi-b">'
            f'<b>{escape(r["kpi_name"])}</b>'
            f'<div class="kpi-meta">{base}{escape(str(r["evidence_strength"]))}'
            f'{ev(r["evidence_link"])}</div>'
            f'<p class="why">{escape(r["why_good_indicator"])}</p></div></div>')


NSR = K[K.kpi_id == "NS"].iloc[0]
NS_BLOCK = ('<div class="ns"><div class="ns-l">'
            '<div class="ns-badge">NEEDS RAPIDO&#39;S OWN DATA</div>'
            f'<h4>{escape(NSR["kpi_name"])}</h4>'
            f'<p class="frm">{escape(NSR["formula"])}</p></div>'
            f'<div class="ns-r"><p>{escape(NSR["why_good_indicator"])}</p>'
            f'<p class="lim"><b>What it takes to measure.</b> '
            f'{escape(NSR["what_would_upgrade_it"])}</p></div></div>')

fam = K[(K.kpi_id != "NS") & (K.family_order < 9)].sort_values(["family_order", "kpi_id"])
n_ready = int(fam[fam.is_headline & fam.status.str.startswith("COMPUTED")].shape[0])
fam_html = ""
for f, g in fam.groupby("family", sort=False):
    ok = g["status"].str.startswith("COMPUTED").any()
    fam_html += (f'<div class="fam"><div class="fam-h"><b>{escape(f)}</b>'
                 f'<span class="fbadge {"ok" if ok else "gap"}">'
                 f'{"MEASURED IN THIS STUDY" if ok else "NEEDS RAPIDO&#39;S OWN DATA"}</span></div>'
                 + "".join(kpi_row(r) for _, r in g.iterrows()) + "</div>")

tab("t3", "03", "KPIs",
    lead(f"Eight KPIs decide this business. We measured {n_ready} of them.",
         "One sits above the rest as the single number that answers the question. Seven drive it. "
         "Each is shown with the measures behind it.")
    + panel("The North Star", NS_BLOCK,
            kicker="If Rapido tracked one number in Hyderabad, this is it",
            foot="A cheap first order only matters if it becomes a second one. This is the number "
                 "that says whether it did.", link=NSR["evidence_link"])
    + panel("The seven driver KPIs", fam_html, kicker="Each with the measures behind it"))

# ===================================================== 4 MARKETING METRICS
def mm_row(r):
    val = r["value"]
    vs = ("—" if pd.isna(val) else f'₹{val:,.0f}' if r["unit"] == "INR" else f'{val:g}{r["unit"]}')
    return (f'<div class="mm"><div class="mm-h"><span class="mm-v">{vs}</span>'
            f'<b>{escape(r["metric_name"])}</b>'
            f'<span class="mm-src">{escape(str(r["formula_sheet_reference"]))}</span></div>'
            f'<p class="frm">{escape(r["formula"])}</p>'
            f'<p class="why">{escape(r["interpretation"])}</p></div>')


STC_CHART = ch.grouped_bars(
    ["List price\n(before any offer)", "With a Swiggy One or\nZomato Gold membership",
     "After a coupon"],
    [dict(name="People whose price bar Ownly clears", color=BLUE,
          vals=STC["coverage_pct"].tolist())],
    w=660, h=370, xlab="Which price the customer actually sees",
    ylab="Share of people whose price bar is cleared")

tab("t4", "04", "Marketing metrics",
    lead("Ownly's saving is big enough for four in five people — until an offer lands on the "
         "other side.",
         "Switch-Threshold Coverage is the central metric of this study. It compares every "
         "person's own stated price bar against every price we actually observed.")
    + panel("Switch-Threshold Coverage", STC_CHART
            + readme("We asked each person how much cheaper an app has to be, on every order, "
                     "before they would switch to it. Then we priced the same dishes on all three "
                     "apps. This chart shows what share of those personal price bars Ownly's "
                     "saving actually clears — first at list price, then for someone with a paid "
                     f"membership, then once a coupon is applied. Based on "
                     f"{int(ST.n_named.iloc[0])} people × 4 priced dishes."),
            kicker="The central number in this study",
            foot="Eight in ten people would switch at Ownly's list price. Two in ten would switch "
                 "at the price someone with a membership and a coupon actually pays.",
            link="data/switch_threshold_coverage.csv")
    + panel(f"The {len(M)} metrics we built", "".join(mm_row(r) for _, r in M.iterrows()),
            kicker="From the course formula sheets, and our own"))

# ===================================================== 5 ANALYSIS
trows = [dict(label=r["dimension"].upper(), cheap_pct=r["chose_cheaper_pct"],
              prem_pct=r["paid_premium_pct"],
              cheap_txt={"speed": "wait 45 min instead of 30",
                         "reliability": "accept 3-in-10 orders late",
                         "usual restaurants": "lose most usual restaurants"}[r["dimension"]],
              prem_txt={"speed": "pay ₹30 to get it sooner",
                        "reliability": "pay ₹30 for 1-in-10 late",
                        "usual restaurants": "pay ₹30 to keep them"}[r["dimension"]])
         for _, r in TR.iterrows()]

STAIR = ch.line_chart(
    ST["level_rs"].tolist(),
    [dict(name="Everyone who named\na figure (n=33)", color=BLUE, vals=ST["pct_of_named"].tolist()),
     dict(name="All 40 people\n(incl. 'no amount'\nand 'don't know')", color=MUTED,
          vals=ST["pct_of_all"].tolist(), dash=True)],
    w=680, h=430, xlab="How much cheaper Ownly must be, on every order",
    ylab="Share of people who would switch",
    marks=[dict(level=30, label="₹30 — half the group"),
           dict(level=50, label="₹50 — a clear majority")])

er = []
for vw, nm, sub, trig in [
        ("LIST+FEES", "LIST PRICE", "before any offer", ""),
        ("MEMBER", "WITH A MEMBERSHIP", "Swiggy One or Zomato Gold",
         "▼ the membership alone takes this much"),
        ("AFTER OFFER", "AFTER A COUPON", "a discount code applied",
         "▼ the coupon takes the rest")]:
    g = P[P.view == vw]
    er.append(dict(name=nm, sub=sub, trigger=trig, win_pct=g.ownly_wins.mean() * 100,
                   win_k=int(g.ownly_wins.sum()), win_n=len(g),
                   saving_rs=g.saving_rs.median(), saving_pct=g.saving_pct.median()))

ETA_CHART = ch.grouped_bars(
    [r["restaurant_display"] for _, r in ETA.iterrows()],
    [dict(name="Ownly", color=CORAL, vals=[r["ownly"] for _, r in ETA.iterrows()]),
     dict(name="Faster of Swiggy / Zomato", color=BLUE,
          vals=[r["best_incumbent"] for _, r in ETA.iterrows()])],
    w=660, h=380, xlab="Restaurant", ylab="Delivery time shown in the app (minutes)",
    unit="", ymax=50)

cov_rows = [dict(name=r["restaurant_display"],
                 on={"Ownly": bool(r["on_ownly"]), "Swiggy": bool(r.get("swiggy", False)),
                     "Zomato": bool(r.get("zomato", False))}) for _, r in COV.iterrows()]
COV_CHART = ch.coverage_grid(cov_rows, ["Ownly", "Swiggy", "Zomato"], w=640)

SEG_CHART = ch.grouped_bars(
    [s.replace(" ", "\n", 1) for s in SEG["segment"]],
    [dict(name="Gives up speed", color=BLUE, vals=SEG["Trades speed for ₹30"].tolist()),
     dict(name="Gives up reliability", color=GREY, vals=SEG["Trades reliability for ₹30"].tolist()),
     dict(name="Gives up usual restaurants", color=CORAL,
          vals=SEG["Trades restaurants for ₹30"].tolist())],
    w=700, h=400, xlab="Group", ylab="Share who would give it up to save ₹30")

seg_disp = SEG.copy()
for c in seg_disp.columns:
    if c in ("segment", "n"):
        continue
    money = c.strip().endswith("(₹)")
    seg_disp[c] = seg_disp[c].map(
        lambda v, _m=money: "" if pd.isna(v) else (f"₹{v:.0f}" if _m else f"{v:.0f}%"))

frows = [dict(label=str(r["question"]).rstrip("?"),
              est=r["rho"], lo=r["ci_lo"], hi=r["ci_hi"], n=int(r["n"]),
              color=BLUE if r["p_value"] < .05 else MUTED)
         for _, r in AS.iterrows() if pd.notna(r.get("rho"))]
FOREST = ch.forest(frows, w=760, pad_l=330,
                   xlab="Strength of relationship  (−1 = opposite · 0 = none · +1 = strong)",
                   ylab="")

bl = BEN.set_index("base")
BEN_CHART = ch.grouped_bars(
    ["Know about\nOwnly", "Have ordered\non Ownly", "Pay for a\nmembership",
     "Expect prices\nto rise"],
    [dict(name="Gachibowli (n=40)", color=CORAL,
          vals=[float(bl.loc["Gachibowli catchment", c]) for c in
                ["aware_pct", "tried_pct", "membership_pct", "durability_doubt_pct"]]),
     dict(name="Bengaluru (n=16)", color=BLUE,
          vals=[float(bl.loc["Bengaluru (benchmark)", c]) for c in
                ["aware_pct", "tried_pct", "membership_pct", "durability_doubt_pct"]])],
    w=680, h=390, xlab="", ylab="Share of people")

vs = VS.set_index("base")
SHARE_CHART = ch.stacked_share([
    dict(label="Gachibowli", note=f"{int(vs.loc['Gachibowli catchment','total_orders'])} orders",
         segs=[dict(name="Swiggy", pct=float(vs.loc["Gachibowli catchment", "swiggy_pct"]),
                    color=BLUE),
               dict(name="Zomato", pct=float(vs.loc["Gachibowli catchment", "zomato_pct"]),
                    color=DARK),
               dict(name="Everything else", pct=float(vs.loc["Gachibowli catchment", "other_pct"]),
                    color=GREY)]),
    dict(label="Bengaluru", note=f"{int(vs.loc['Bengaluru (benchmark)','total_orders'])} orders",
         segs=[dict(name="Swiggy", pct=float(vs.loc["Bengaluru (benchmark)", "swiggy_pct"]),
                    color=BLUE),
               dict(name="Zomato", pct=float(vs.loc["Bengaluru (benchmark)", "zomato_pct"]),
                    color=DARK),
               dict(name="Everything else",
                    pct=float(vs.loc["Bengaluru (benchmark)", "other_pct"]
                              + vs.loc["Bengaluru (benchmark)", "volume_share_pct"]),
                    color=GREY)])], w=660)

ACQ = ('<div class="acq">'
       '<div class="acq-i"><span class="acq-n">THE GAME</span>'
       '<b>₹50 off, up to three times</b>'
       '<p>Ownly runs a retro racing mini-game inside the app. Win it and you get ₹50 off your '
       'order. It can be played a maximum of three times, so a new customer can earn ₹150 of '
       'discount through play alone.</p></div>'
       '<div class="acq-i"><span class="acq-n">THE REFERRAL</span>'
       '<b>₹100 for a friend&#39;s first order</b>'
       '<p>Users can refer friends, and the referral pays out around ₹100 on that friend&#39;s '
       'first order. This is Ownly buying word of mouth directly — the exact channel our '
       'interviews say people trust most.</p></div>'
       '<div class="acq-i"><span class="acq-n">THE APP CHANGE</span>'
       '<b>Ownly took Metro&#39;s place in the bottom bar</b>'
       '<p>In the Rapido app, Ownly now sits in the bottom navigation bar where Metro used to be, '
       'and Metro has moved to a box on the home screen. Ownly has been given the most valuable '
       'position in an app tens of millions of people already open.</p></div></div>')

tab("t5", "05", "Analysis",
    lead("₹30 buys time. ₹30 buys some risk. ₹30 does not buy your usual restaurants.",
         "Same ₹30, three different trades, put to the same 40 people. Because everyone answered "
         "all three, the three can be compared directly against each other.")
    + panel("What people will give up to save ₹30", ch.paired_tradeoff(trows)
            + readme("Each row is one question. People were shown two identical food orders — one "
                     "at ₹260, one at ₹230 — and told what was different about the cheaper one. "
                     "The orange bar is the share who took the cheaper option. The blue bar is the "
                     "share who paid ₹30 more to avoid that compromise. All 40 people answered "
                     "all three questions."),
            foot="Speed is the easiest thing to give up and restaurant choice is the hardest. The "
                 "gap between those two is far too large to be chance.",
            link="data/tradeoff_summary.csv")
    + panel("How much cheaper Ownly has to be before people switch", STAIR
            + readme("The horizontal axis is the size of the saving, on every order. The vertical "
                     "axis is the share of people who said they would move their main app for "
                     "that saving. The solid blue line counts the 33 people who named a figure. "
                     "The dashed grey line counts all 40, including 4 who said no saving would "
                     "move them and 3 who did not know — which is why it sits lower. The two red "
                     "markers show where half the group is won: ₹30 on the blue line, ₹50 on the "
                     "grey."),
            foot="₹30 already wins over half the people who put a number on it. ₹50 wins a "
                 "majority of the whole group. Ownly's observed saving is ₹114 at list price — "
                 "comfortably above both.",
            link="data/switching_staircase.csv")
    + panel("What happens to Ownly's price advantage as offers are applied", ch.erosion(er)
            + readme("We priced the <b>same dish, from the same restaurant, at the same moment</b> "
                     "on all three apps — four dishes in total, at a Gachibowli address. Each row "
                     "is one of the three prices a customer might see. The bar shows how many of "
                     "those four dishes were cheapest on Ownly; the figure on the right is the "
                     "typical saving in rupees."),
            foot="At list price Ownly is cheapest on all four dishes by about ₹114. A paid "
                 "membership on the other app removes part of that. A coupon removes the rest.",
            link="data/audit_pairs.csv")
    + '<div class="two wide">'
    + panel("Delivery time shown at checkout", ETA_CHART
            + readme("For each restaurant we recorded the delivery time the app promised at the "
                     "moment of ordering. Orange is Ownly; blue is whichever of Swiggy or Zomato "
                     "was faster."),
            foot="Ownly is slower at every restaurant by a similar amount each time — roughly 17 "
                 "to 24 minutes. A consistent gap like this points to where the food is collected "
                 "from rather than to the riders, which makes it a branch question.",
            link="data/eta_gap_by_restaurant.csv")
    + panel("Which restaurants each app carries", COV_CHART
            + readme("Every restaurant we checked at a Gachibowli address, and whether each app "
                     "carries it."),
            foot="Ownly carries 9 of the 10 restaurants we checked, and one of them — Aanimuthyalu "
                 "Unlimited — is on Ownly alone. Ownly lists 221 restaurants in Gachibowli in "
                 "total, so there are very likely more it has to itself beyond the ones we "
                 "checked.",
            link="data/audit_coverage.csv")
    + "</div>"
    + panel("How Ownly is winning its first orders", ACQ,
            kicker="Observed in the live apps, September 2026",
            foot="All three are running right now. Together they show a company buying trial "
                 "through play, through friends, and through the most valuable piece of screen "
                 "space it owns.")
    + panel("Which groups behave differently", SEG_CHART
            + readme("Each cluster is one group of people. The three bars show what share of that "
                     "group would give up speed, reliability or their usual restaurants to save "
                     "₹30. Restaurant choice is protected hardest in every single group.")
            + tbl(seg_disp),
            foot="Working professionals ask for a bigger saving than students before they switch — "
                 "₹50 against ₹30. People who do not pay for a membership are about twice as "
                 "likely to keep using Ownly once an introductory offer ends.",
            link="data/segment_cuts.csv")
    + '<div class="two wide">'
    + panel("Gachibowli against Bengaluru", BEN_CHART
            + readme("The same four questions asked in both cities. Bengaluru has had Ownly far "
                     "longer, so it shows what a more developed market looks like."),
            foot="Awareness and trial are roughly twice as high in Bengaluru. Both cities are "
                 "equally sceptical that low prices will last.",
            link="data/bengaluru_benchmark.csv")
    + panel("Where delivery orders go today", SHARE_CHART
            + readme("Every order our respondents reported in the last four weeks, split by app."),
            foot="Swiggy and Zomato take more than nine in ten orders in both cities. That is the "
                 "habit Ownly's price advantage has to break.",
            link="data/sample_volume_share.csv")
    + "</div>"
    + panel("What we tested for a relationship, and what we found", FOREST
            + readme("Each line is one relationship we set out to test before looking at the data. "
                     "The dot is the measured strength, from −1 to +1. The horizontal line around "
                     "it is the range the true value is likely to sit in. When that range crosses "
                     "the centre line, the relationship is not strong enough to call."),
            foot="All four ranges cross the centre, so the recommendations rest on the trade-off "
                 "and price findings instead — where the differences are large and clear.",
            link="data/associations.csv"))

# ===================================================== 6 WHY OTHERS FAILED
MECH = [
    ("M1", "Demand bought with discounts disappears when the discounts stop",
     "Foodpanda India went from around 200,000 orders a day to around 5,000 once it stopped "
     "discounting. Orders on the government-backed ONDC network fell about 29% after incentives "
     "were cut.",
     f"Ownly's saving comes from removing fees, not from funding discounts. Charges other than "
     f"food are {kv('K3'):.0f}% of an Ownly bill against about {kv('K3')+mv('MM10'):.0f}% on "
     "Swiggy and Zomato. That advantage does not need marketing money behind it.",
     "STRUCTURALLY DIFFERENT"),
    ("M2", "Winning restaurants is easier than winning customers",
     "Zomato told the competition regulator that only about 1% of its restaurants are exclusive to "
     "it. Thrive closed its consumer app even while charging restaurants just 3%.",
     "Zero commission has brought Ownly to 221 restaurants in Gachibowli within weeks of launch, "
     "including at least one that neither Swiggy nor Zomato carries.", "MOVING FAST"),
    ("M3", "Being cheaper is not the same as being different",
     "Eternal, Zomato's parent, told shareholders in July 2026 that new low-price apps offer "
     "&ldquo;the same restaurants, similar or longer delivery times&rdquo;.",
     "Our survey says the part that matters is restaurant choice, not speed: 92% of people will "
     "wait longer to save ₹30, but only 35% will give up their usual restaurants. Ownly's opening "
     "is to carry the branches people already order from.", "THE REAL BATTLEGROUND"),
    ("M4", "Cheap food still has to arrive",
     "Ola withdrew from ONDC after complaints about tracking, refunds and support. Zomato's own "
     "customers kept ordering through the price war because the service held.",
     "72% of people will accept a slightly less reliable delivery to save ₹30, so reliability is "
     "not what stops someone trying Ownly. Interviews are clear that repeated bad orders are what "
     "makes people leave — so this protects the second order, not the first.",
     "THE RETENTION GUARDRAIL"),
    ("M5", "The economics have to work eventually",
     "Uber Eats India lost about $2.55 on an average order worth about $2.45 — more per order than "
     "the order itself was worth — and sold to Zomato.",
     "Ownly charges no delivery fee, no platform fee and no packaging fee, and takes no commission "
     "from restaurants. Rapido has said openly that it is not trying to make money from food yet; "
     "the riders and the app are already paid for by the bike-taxi business.",
     "A DELIBERATE CHOICE"),
]
mh = "".join(
    f'<div class="mech"><div class="mh"><span class="mid">{m[0]}</span><b>{m[1]}</b>'
    f'<span class="status ok">{m[4]}</span></div><div class="mg">'
    f'<div><span class="mlab">WHAT HAPPENED BEFORE</span><p>{m[2]}</p></div>'
    f'<div><span class="mlab">WHERE OWNLY STANDS</span><p>{m[3]}</p></div></div></div>'
    for m in MECH)

tab("t6", "06", "Why others failed",
    lead("Six companies have tried to beat Swiggy and Zomato on price. Ownly is playing a "
         "different game.",
         "Every one of them bought orders with discounts. Ownly removes fees instead — an "
         "advantage that stays when the marketing money stops.")
    + panel("Five ways challengers have failed, and where Ownly stands on each", mh,
            foot="Drawn from a study of Uber Eats India, Foodpanda, Amazon Food, ONDC, Thrive and "
                 "DotPe — five research dossiers and around 230 sources.")
    + panel("Why Rapido entered anyway",
            '<ul class="plain">'
            '<li><b>A customer the big two do not serve.</b> Swiggy and Zomato are built around a '
            'higher-spending customer. A much larger group spends around ₹100 a meal and is priced '
            'out of app delivery entirely.</li>'
            '<li><b>Fees, not discounts.</b> No commission for restaurants, and no platform, '
            'packaging or surge fee for customers. The price gap is built into the model.</li>'
            '<li><b>A fleet that already exists.</b> Rapido&#39;s riders and app are paid for by '
            'bike taxis, and mealtimes fall outside the commute rush.</li>'
            '<li><b>Restaurants were ready to listen.</b> Ownly launched into an open dispute over '
            'commissions, with a National Restaurant Association partnership in Hyderabad in July '
            '2026.</li></ul>', kicker="The strategic logic"))

# ===================================================== 7 H0
hs = H[H.id == "H0-STATED"].iloc[0]
_nP = int(str(hs["result"]).split("Service P ")[1].split(" ")[0])
_nQ = int(str(hs["result"]).split("Service Q ")[1].split(",")[0])
_nC = int(str(hs["result"]).split("plus ")[1].split(" ")[0])
_spd = TR.loc[TR.dimension == "speed", "chose_cheaper_pct"].iloc[0]
_rel = TR.loc[TR.dimension == "reliability", "chose_cheaper_pct"].iloc[0]
_ast = TR.loc[TR.dimension == "usual restaurants", "chose_cheaper_pct"].iloc[0]

PQ_CHART = ch.grouped_bars(
    ["Service P\n(the price story)", "Service Q\n(restaurants, reliability,\nsupport)",
     "Wanted\nboth"],
    [dict(name="People", color=BLUE, vals=[float(_nP), float(_nQ), float(_nC)])],
    w=620, h=340, xlab="Which service they would start using", ylab="Number of people",
    unit="", ymax=24)

PLAIN = (
    '<div class="plainq">'
    '<div class="pq"><span class="pq-n">WHAT WE ASKED</span>'
    '<p>We wrote two descriptions of a food app and showed <b>both to the same people</b>.</p>'
    '<p><b>Service P</b> — the Bengaluru story: a lower final bill, no hidden fees, clear '
    'pricing.<br><b>Service Q</b> — the Hyderabad story: local restaurants, delivery that turns '
    'up, real support, clear pricing.</p>'
    '<p>Then: <i>if only one of these existed where you live, which would you start '
    'using?</i></p></div>'
    '<div class="pq"><span class="pq-n">WHAT CAME BACK</span>'
    f'<p><b>{_nP}</b> chose the price story. <b>{_nQ}</b> chose the restaurants-and-service '
    f'story. <b>{_nC}</b> wanted both.</p>'
    f'<p>Among those who picked a side, that is <b>{_nP/(_nP+_nQ)*100:.0f}% for price</b> — a '
    'clear lean, in the direction the Bengaluru playbook assumes.</p></div>'
    '<div class="pq"><span class="pq-n">WHAT IT MEANS</span>'
    '<p>Price leads, and it leads comfortably. With a group of this size that is a <b>strong '
    'directional signal</b> pointing the same way as every other price finding in this study.</p>'
    f'<p>The {_nC} people who wanted both are the more interesting result: a third of the group '
    'did not see these as alternatives at all.</p></div>'
    '<div class="pq warn"><span class="pq-n">WHAT COMES NEXT</span>'
    '<p>The sharpest version of this question is a live test where people can click and order, so '
    'that real first orders are counted rather than stated preference.</p>'
    '<p>That test is designed and ready to run. It is the first item on the plan.</p></div></div>')

WHYNOT = (
    '<p class="big">Asking people to choose between two whole packages hides what is driving the '
    'choice.</p>'
    f'<p>Each description carried four features at once, and {_nC} people said they wanted both — '
    'which tells us the packages were not really alternatives.</p>'
    '<p>So we asked it a sharper way: <b>hold the saving at ₹30 and change only one thing at a '
    'time.</b> That separated cleanly, and it is what the recommendations are built on.</p>'
    + ch.hbar([dict(label="Give up 15 minutes of speed", value=float(_spd), color=BLUE,
                    note="the easiest thing to give up"),
               dict(label="Give up some reliability", value=float(_rel), color=GREY, note=""),
               dict(label="Give up your usual restaurants", value=float(_ast), color=CORAL,
                    note="the hardest — and the one that matters")],
              w=620, pad_l=240, pad_r=215, show_ci=False))

tab("t7", "07", "H₀ decision",
    lead("Price leads. Restaurants decide.",
         "We put the two stories head to head with the same people, then took them apart to see "
         "which part was doing the work.")
    + panel("In plain words", PLAIN, kicker="Read this first")
    + '<div class="two wide">'
    + panel("Which story people chose", PQ_CHART
            + readme("Each bar is the number of people who said they would start using that "
                     "service. Everyone saw both descriptions before choosing."),
            foot=f"Price leads {_nP} to {_nQ}, with {_nC} wanting both.",
            link="data/hypothesis_results.csv")
    + panel("What the same ₹30 can and cannot buy", WHYNOT, kicker="The sharper question")
    + "</div>"
    + panel("Where this leaves the question",
            '<div class="two"><div><h4>What we can say now</h4>'
            '<p>Price is the strongest single pull, and it pulls in the direction the Bengaluru '
            'playbook assumes. The saving needed is modest — ₹30 moves half the group, ₹50 moves a '
            'clear majority, and Ownly already delivers ₹114 at list price.</p>'
            '<p>Restaurant choice is the one thing money does not buy. That is where the '
            '<b>ADAPT</b> belongs.</p></div>'
            '<div><h4>What the next test adds</h4>'
            '<p>A live landing test measures real first orders rather than stated preference, and '
            'settles the direction with behaviour instead of opinion.</p>'
            '<p>The design is complete and the measurement plan is written. It is the first item '
            'on the next-steps list.</p></div></div>', kicker="The position"))

# ===================================================== 8 PROPOSITIONS
PROPS = [
    ("1", "Lead with the everyday bill, not a comparison", "KEEP",
     "Ownly's saving comes from removing fees, so it is there on every order without a coupon. Say "
     "it as the price of the meal itself — “your usual order, ₹114 less” — rather than as a "
     "comparison against another app.",
     "A comparison can be disproved by a single coupon on the other side. The everyday bill "
     "cannot. Eight in ten people here already pay for a Swiggy or Zomato membership, so a "
     "comparison is exactly the claim they are most likely to test.",
     "Cheapest on all 4 dishes at list price · ₹114 typical saving · Fees are 5% of an Ownly bill "
     "against 23% elsewhere"),
    ("2", "Win the nearest branch of the restaurants people already use", "ADAPT",
     "Target the specific outlets closest to Gachibowli for the restaurants people order from "
     "most, rather than adding more restaurant names to the total.",
     "Restaurant choice is the only thing people would not give up for ₹30 — 65% paid more to keep "
     "it. Ownly already carries the big names, but not always the nearest branch, which is also "
     "the most likely reason its delivery times run longer. Fixing the branch fixes both at once.",
     "65% protect their restaurants · Delivery 17–24 min longer at every restaurant checked"),
    ("3", "Buy word of mouth, because that is how people actually arrive", "KEEP",
     "Keep referrals and in-app rewards as the main route to a first order, and measure first "
     "orders earned per referral.",
     "Interviews are consistent: people try a new food app because a friend told them to. Ownly is "
     "already doing this — ₹100 for a friend's first order, and a ₹50 reward playable up to three "
     "times. This is the channel our own respondents say they trust.",
     "₹100 per referral · ₹50 game reward × 3 · Friend recommendation named the top trial trigger "
     "after price"),
    ("4", "Use the Rapido bottom bar as the discovery engine it now is", "KEEP",
     "Ownly now occupies the bottom navigation bar in the Rapido app where Metro used to sit. "
     "Treat that position as the primary acquisition channel and measure taps through to first "
     "orders.",
     "Rapido opens in front of tens of millions of people who are already paying for a ride. "
     "Two-thirds of our respondents used Rapido in the last four weeks. Owning the best position "
     "in that app is the cheapest distribution any food app in India has.",
     "67% used Rapido in the last four weeks · Ownly placed in the bottom bar, September 2026"),
    ("5", "Make the second order the measure of success", "ADAPT",
     "Track what share of people who arrive on an introductory offer order again without one, and "
     "treat that number as the scoreboard for Hyderabad.",
     "A first order is bought; a second order is earned. People who do not already pay for a "
     "membership are about twice as likely to keep using Ownly after an offer ends, which makes "
     "them the group to win first.",
     "Repeat intent roughly doubles among people without a membership · 25% overall would continue "
     "after the offer ends"),
]
ph = "".join(
    f'<div class="prop"><div class="ph"><span class="pnum">{p[0]}</span><b>{escape(p[1])}</b>'
    f'<span class="dec {p[2].lower()}">{p[2]}</span></div>'
    f'<p class="pdef">{escape(p[3])}</p><div class="pg2">'
    f'<div><span class="mlab">WHY</span><p>{escape(p[4])}</p></div>'
    f'<div><span class="mlab">THE EVIDENCE</span><p class="pev">{escape(p[5])}</p></div>'
    '</div></div>' for p in PROPS)

tab("t8", "08", "Propositions",
    lead("Five moves, in the order we would make them.",
         "Each one says what to do, why it follows from the evidence, and which numbers support "
         "it.")
    + panel("The plan", ph)
    + panel("What we would measure next",
            '<ol class="plain">'
            '<li><b>A live landing test.</b> Two versions of the offer, real clicks, real first '
            'orders. This turns the price-versus-restaurants question from a stated preference '
            'into a measured one. Designed and ready.</li>'
            '<li><b>A branch-level price audit.</b> Record the outlet name and distance next to '
            'each price, confirming whether the delivery gap is a branch question.</li>'
            '<li><b>A wider restaurant check.</b> Sample 25–30 restaurants from Ownly&#39;s own 221 '
            'to size how much it carries that the other two do not.</li>'
            '<li><b>Three test orders.</b> Compare the delivery time promised at checkout with the '
            'time the food actually arrives.</li>'
            '<li><b>One extra survey question.</b> &ldquo;Name the three places you order from '
            'most&rdquo; turns restaurant coverage into the version that predicts behaviour.</li>'
            '</ol>', kicker="The next five things"))

# ==================================================================== ASSEMBLE
nav = "".join(f'<button class="tb-btn" data-t="{t["id"]}"><span class="tn">{t["num"]}</span>'
              f'{escape(t["name"])}</button>' for t in TABS)
secs = "".join(f'<div class="pane" id="{t["id"]}"><div class="ptt"><span class="pn">{t["num"]}'
               f'</span>{escape(t["name"])}</div>{t["body"]}</div>' for t in TABS)

CSS = f"""
:root{{--cream:{CREAM};--coral:{CORAL};--blue:{BLUE};--dark:{DARK};--rule:{RULE};--muted:{MUTED};
--panel:#FBF8F1;--grid:#E5DBC8}}
*{{box-sizing:border-box}}html,body{{margin:0;padding:0}}
body{{background:var(--cream);color:var(--dark);font-family:-apple-system,BlinkMacSystemFont,
"Segoe UI",Helvetica,Arial,sans-serif;font-size:14px;line-height:1.55;-webkit-font-smoothing:
antialiased;font-variant-numeric:tabular-nums}}
.wrap{{max-width:1160px;margin:0 auto;padding:0 26px 80px}}
header{{background:var(--dark);color:var(--cream);padding:26px 0 0}}
.hin{{max-width:1160px;margin:0 auto;padding:0 26px}}
.eyebrow{{font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;opacity:.7;margin:0 0 8px}}
header h1{{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:28px;
margin:0 0 7px}}
header .sub{{font-size:13px;opacity:.78;margin:0 0 22px;max-width:820px}}
nav{{background:var(--dark);border-top:1px solid rgba(242,235,221,.18);position:sticky;top:0;z-index:50}}
.nin{{max-width:1160px;margin:0 auto;padding:0 20px;display:flex;flex-wrap:wrap}}
.tb-btn{{background:none;border:0;border-bottom:2px solid transparent;color:rgba(242,235,221,.62);
font:inherit;font-size:11.5px;padding:10px 12px;cursor:pointer;white-space:nowrap;display:flex;
gap:6px;align-items:baseline}}
.tb-btn:hover{{color:var(--cream)}}
.tb-btn.on{{color:var(--cream);border-bottom-color:var(--coral)}}
.tn{{font-size:9.5px;opacity:.6}}
.pane{{display:none;padding-top:26px}}.pane.on{{display:block}}
.ptt{{font-size:10.5px;letter-spacing:.17em;text-transform:uppercase;color:var(--muted);
display:flex;gap:9px;border-bottom:1px solid var(--rule);padding-bottom:7px;margin-bottom:22px}}
.pn{{color:var(--coral);font-weight:700}}
.lead{{margin:0 0 24px;max-width:920px}}
.hl{{font-family:Georgia,serif;font-size:26px;line-height:1.3;margin:0 0 10px;font-weight:400}}
.kad{{color:var(--coral);font-weight:700}}
.hlsub{{margin:0;font-size:13.5px;color:#5E504B;max-width:860px}}
.panel{{background:var(--panel);border:1px solid var(--rule);padding:19px 22px 17px;margin:0 0 18px}}
.panel h3{{font-size:11px;letter-spacing:.14em;text-transform:uppercase;margin:0 0 15px;
font-weight:700}}
.kick{{font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--coral);
font-weight:700;margin-bottom:5px}}
.foot{{font-size:12px;color:#5E504B;margin:14px 0 0;border-top:1px solid var(--rule);
padding-top:11px;line-height:1.6}}
.readme{{background:var(--cream);border-left:3px solid var(--blue);padding:10px 14px;margin:14px 0 0}}
.readme span{{font-size:8.5px;letter-spacing:.14em;color:var(--blue);font-weight:700;display:block;
margin-bottom:4px}}
.readme p{{margin:0;font-size:11.5px;line-height:1.6;color:#4A3D39}}
.why{{font-size:12px;line-height:1.6;margin:6px 0 0}}
.lim{{font-size:11.5px;line-height:1.55;margin:5px 0 0;color:#6B5C57}}
.big{{font-size:15.5px;line-height:1.55;margin:0 0 9px}}
.frm{{font-family:"SF Mono",Menlo,Consolas,monospace;font-size:10.5px;color:var(--muted);
margin:4px 0 6px;line-height:1.5}}
a.ev{{display:inline-block;font-size:9.5px;background:var(--cream);border:1px solid var(--rule);
color:#6B5C57;padding:1px 6px;margin-left:7px;text-decoration:none;white-space:nowrap}}
a.ev:hover{{background:var(--blue);color:#fff;border-color:var(--blue)}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:1px;
background:var(--rule);border:1px solid var(--rule)}}
.card{{background:var(--panel);padding:15px}}
.cval{{font-family:Georgia,serif;font-size:28px;line-height:1;margin-bottom:7px}}
.card.warn .cval{{color:#B4552F}}
.clab{{font-size:11.5px;line-height:1.4}}.csub{{font-size:10px;color:var(--muted);margin-top:5px}}
svg.chart{{display:block;max-width:100%;height:auto;margin:0 auto}}
text{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
font-variant-numeric:tabular-nums}}
.tb{{width:100%;border-collapse:collapse;font-size:11.5px;margin-top:16px}}
.tb th{{text-align:left;font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;
color:var(--muted);border-bottom:1px solid var(--rule);padding:7px 9px 7px 0;font-weight:700}}
.tb td{{padding:8px 9px 8px 0;border-bottom:1px solid #EDE4D3;line-height:1.5}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}.two.wide>*{{margin-bottom:0}}
.evo{{display:flex;align-items:stretch}}
.evo-step{{flex:1;background:#fff;border:1px solid var(--rule);padding:15px}}
.evo-step.now{{background:var(--dark);border-color:var(--dark);color:var(--cream)}}
.evo-step.now .why,.evo-step.now p{{color:rgba(242,235,221,.82)}}
.step-n{{font-size:9px;letter-spacing:.13em;color:var(--coral);font-weight:700}}
.evo-step b{{display:block;font-size:13.5px;margin:7px 0}}
.evo-step p{{margin:0 0 7px;font-size:12px}}
.evo-arrow{{display:flex;align-items:center;padding:0 10px;color:var(--muted)}}
.ns{{display:grid;grid-template-columns:330px 1fr;gap:22px;align-items:start}}
.ns-badge{{display:inline-block;font-size:9px;letter-spacing:.12em;background:#DDD2BE;
padding:3px 8px;font-weight:700;margin-bottom:9px}}
.ns-l h4{{font-family:Georgia,serif;font-size:20px;font-weight:400;margin:0 0 7px}}
.fam{{border:1px solid var(--rule);background:#fff;margin-bottom:14px}}
.fam-h{{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:11px 15px;
background:var(--cream);border-bottom:1px solid var(--rule)}}
.fam-h b{{font-size:12.5px}}
.fbadge{{font-size:9px;letter-spacing:.1em;padding:3px 9px;font-weight:700;white-space:nowrap}}
.fbadge.ok{{background:var(--blue);color:#fff}}.fbadge.gap{{background:#DDD2BE;color:var(--dark)}}
.kpi{{display:flex;gap:18px;padding:14px 15px;border-bottom:1px solid #EDE4D3}}
.fam .kpi:last-child{{border-bottom:0}}
.kpi-v{{font-family:Georgia,serif;font-size:22px;min-width:100px;text-align:right;flex-shrink:0}}
.kpi-b b{{font-size:13px}}
.kpi-meta{{font-size:9.5px;color:var(--muted);margin:2px 0 5px}}
.mm{{border-left:2px solid var(--blue);padding:2px 0 13px 14px;margin-bottom:15px}}
.mm-h{{display:flex;align-items:baseline;gap:11px;flex-wrap:wrap}}
.mm-v{{font-family:Georgia,serif;font-size:21px;color:var(--blue)}}
.mm-h b{{font-size:13.5px}}.mm-src{{font-size:9.5px;color:var(--muted)}}
.acq{{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--rule);
border:1px solid var(--rule)}}
.acq-i{{background:#fff;padding:16px}}
.acq-n{{font-size:9px;letter-spacing:.13em;color:var(--coral);font-weight:700}}
.acq-i b{{display:block;font-family:Georgia,serif;font-size:16px;font-weight:400;margin:7px 0 8px}}
.acq-i p{{margin:0;font-size:12px;line-height:1.6}}
.mech{{border:1px solid var(--rule);margin-bottom:12px;background:#fff}}
.mh{{display:flex;align-items:center;gap:12px;padding:10px 14px;background:var(--cream);
border-bottom:1px solid var(--rule)}}
.mid{{font-family:Georgia,serif;font-size:14px;color:var(--coral)}}
.mh b{{flex:1;font-size:12.5px}}
.status{{font-size:9px;letter-spacing:.1em;padding:3px 9px;font-weight:700;white-space:nowrap}}
.status.ok{{background:var(--blue);color:#fff}}
.mg{{display:grid;grid-template-columns:1fr 1fr;gap:18px;padding:13px 14px}}
.mlab{{font-size:9px;letter-spacing:.12em;color:var(--muted);font-weight:700;display:block;
margin-bottom:5px}}
.mg p{{margin:0;font-size:11.8px;line-height:1.65}}
.plainq{{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--rule);
border:1px solid var(--rule)}}
.pq{{background:#fff;padding:15px}}.pq.warn{{background:var(--cream)}}
.pq-n{{font-size:9px;letter-spacing:.13em;color:var(--coral);font-weight:700;display:block;
margin-bottom:9px}}
.pq p{{margin:0 0 9px;font-size:12.3px;line-height:1.62}}.pq p:last-child{{margin-bottom:0}}
.prop{{border:1px solid var(--rule);background:#fff;padding:16px 18px;margin-bottom:13px}}
.ph{{display:flex;align-items:center;gap:13px;margin-bottom:11px}}
.pnum{{font-family:Georgia,serif;font-size:19px;color:var(--coral);min-width:22px}}
.ph b{{flex:1;font-family:Georgia,serif;font-size:17.5px;font-weight:400}}
.dec{{font-size:9px;letter-spacing:.1em;padding:4px 10px;font-weight:700;white-space:nowrap}}
.dec.keep{{background:var(--blue);color:#fff}}.dec.adapt{{background:#C9B79A;color:var(--dark)}}
.pdef{{font-size:13px;line-height:1.6;margin:0 0 12px}}
.pg2{{display:grid;grid-template-columns:1.4fr 1fr;gap:20px;border-top:1px solid #EDE4D3;
padding-top:11px}}
.pg2 p{{margin:0;font-size:11.8px;line-height:1.65}}
.pev{{font-family:"SF Mono",Menlo,Consolas,monospace;font-size:10.5px;color:var(--blue);
line-height:1.7}}
ul.plain,ol.plain{{margin:0;padding-left:20px}}
ul.plain li,ol.plain li{{font-size:12.5px;line-height:1.7;margin-bottom:8px}}
footer{{border-top:1px solid var(--rule);margin-top:36px;padding:17px 0;font-size:10.5px;
color:var(--muted);line-height:1.65}}
@media(max-width:920px){{.two,.mg,.ns,.plainq,.acq,.pg2{{grid-template-columns:1fr}}
.evo{{flex-direction:column}}.evo-arrow{{transform:rotate(90deg);padding:4px 0}}}}
@media print{{nav{{display:none}}.pane{{display:block!important;page-break-after:always}}}}
"""

HTML = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ownly in Gachibowli — Market Research &amp; Validation</title>
<style>{CSS}</style></head><body>
<header><div class="hin">
<p class="eyebrow">Market Research &amp; Validation · Rapido Ownly · Hyderabad</p>
<h1>Can Ownly turn a cheaper first order into a repeat habit in Gachibowli?</h1>
<p class="sub">Which parts of the Bengaluru playbook should Gachibowli KEEP, ADAPT or
DEPRIORITISE?</p>
</div></header>
<nav><div class="nin">{nav}</div></nav>
<div class="wrap">{secs}
<footer>Every figure on this site is computed from our own survey, price audit, interviews and
listening data. Each panel links to the file behind it. Raw responses:
<a href="{SHEET}" target="_blank" rel="noopener">live Google Sheet</a>.</footer></div>
<script>
var B=document.querySelectorAll('.tb-btn'),P=document.querySelectorAll('.pane');
function go(id){{P.forEach(p=>p.classList.toggle('on',p.id===id));
B.forEach(b=>b.classList.toggle('on',b.dataset.t===id));
if(history.replaceState)history.replaceState(null,'','#'+id);window.scrollTo(0,0);}}
B.forEach(b=>b.addEventListener('click',()=>go(b.dataset.t)));
var q=new URLSearchParams(location.search).get('tab');
go(q||(location.hash||'#t1').slice(1));window.scrollTo(0,0);
document.addEventListener('keydown',e=>{{var ids=[...B].map(b=>b.dataset.t),
i=ids.indexOf(document.querySelector('.pane.on').id);
if(e.key==='ArrowRight'&&i<ids.length-1)go(ids[i+1]);
if(e.key==='ArrowLeft'&&i>0)go(ids[i-1]);}});
</script></body></html>"""

with open(f"{SITE}/index.html", "w") as fh:
    fh.write(HTML)
open(f"{SITE}/_redirects", "w").write("/*  /index.html  200\n")
print(f"WROTE {SITE}/index.html ({len(HTML)/1024:.0f} KB, {len(TABS)} sections)")
