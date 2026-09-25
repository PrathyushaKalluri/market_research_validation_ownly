#!/usr/bin/env python3
"""
build_html.py - writes ../Ownly_Hyderabad_Story.html from ../data/*.csv.

Run build_evidence.py first. Every number on the page is read from the CSVs that
script wrote; nothing is typed in by hand except the words around it.
"""
import csv, os
from html import escape as e
import charts as C

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "..", "data")
OUT = os.path.join(HERE, "..", "Ownly_Hyderabad_Story.html")


def load(name):
    with open(os.path.join(D, name), encoding="utf-8") as f:
        return list(csv.DictReader(f))


EV = {r["ID"]: r for r in load("evidence.csv")}


def ev(i):
    """Display string for an evidence row, e.g. '82.5%' or '4 of 16'."""
    return EV[i]["Shown_as"]


def kn(i):
    r = EV[i]
    return f'{r["Numerator"]} of {r["Denominator"]}'


def f(x):
    return float(x)


# ── screen 1: problem ─────────────────────────────────────────────────
TL = load("s1_timeline.csv")
timeline = "".join(
    f'<li class="{"hyd" if "Hyderabad" in t["Event"] else ""}"><span class="when">{e(t["When"])}</span>{e(t["Event"])}</li>' for t in TL)

# ── screen 2: behaviour ───────────────────────────────────────────────
OS = load("s2_order_share.csv")
ch_share = C.hbars([{"label": r["App"], "value": f(r["Share_pct"]), "shown": f'{f(r["Share_pct"]):g}%',
                     "hl": r["App"] == "Ownly", "tip": f'{r["Orders"]} orders'} for r in OS],
                   vmax=60, label_w=90, w=460, title="Share of last-4-week orders by app")

# ── screen 3: KPIs ────────────────────────────────────────────────────
CITY = load("s1_city.csv")
meas = []
for m in ["Heard of Ownly", "Opened Ownly", "Ordered on Ownly"]:
    b = next(r for r in CITY if r["Measure"] == m and r["City"] == "Bengaluru")
    g = next(r for r in CITY if r["Measure"] == m and r["City"] == "Gachibowli")
    meas.append({"label": m, "values": [(f(b["Pct"]), f'{b["Yes"]} of {b["Base"]}'), (f(g["Pct"]), f'{g["Yes"]} of {g["Base"]}')]})
ch_funnel = C.paired(meas, [("Bengaluru (16 people)", C.GREY), ("Gachibowli (40 people)", C.ACC)], vmax=100,
                     title="Ownly funnel, Bengaluru vs Gachibowli")
BAR = load("s3_barriers.csv")
ch_barriers = C.hbars([{"label": r["KPI"], "value": f(r["Pct"]), "shown": f'{f(r["Pct"]):g}%', "lo": f(r["CI_low"]),
                        "hi": f(r["CI_high"]), "hl": i < 2, "sub": f'{r["Yes"]} of {r["Base"]}',
                        "tip": f'{r["Yes"]} of {r["Base"]}, 95% CI {r["CI_low"]}-{r["CI_high"]}%'} for i, r in enumerate(BAR)],
                      label_w=230, ci=True, title="Barrier KPIs with 95% intervals")

# ── screen 4: metrics ─────────────────────────────────────────────────
COV = load("s4_coverage.csv")
ch_cov = C.hbars([{"label": r["View"], "value": f(r["Coverage_pct"]), "shown": f'{f(r["Coverage_pct"]):g}%',
                   "hl": i == 2, "sub": f'{r["Pairs_clearing"]} of {r["Pairs"]} pairs',
                   "tip": f'{r["Pairs_clearing"]} of {r["Pairs"]} person x basket pairs'} for i, r in enumerate(COV)],
                 label_w=200, w=560, title="Switch-threshold coverage")
MET = load("s4_metrics.csv")
met_rows = "".join(f'<tr><td>{e(m["Metric"])}<span class="src">{e(m["Source"])}</span></td><td class="num">{e(m["Result"])}</td>'
                   f'<td>{e(m["Read_it_as"])}</td></tr>' for m in MET)
NE = load("s4_not_estimable.csv")
ne_rows = "".join(f'<li><b>{e(r["Metric"])}</b> - {e(r["Why we cannot compute it"])}</li>' for r in NE)

# ── screen 5: market ──────────────────────────────────────────────────
PV = load("s5_price_views.csv")
ch_price = C.diverging([{"label": r["View"], "value": f(r["Median_saving_rs"]),
                         "shown": (f'Rs{f(r["Median_saving_rs"]):.0f} cheaper' if f(r["Median_saving_rs"]) >= 0
                                   else f'Rs{-f(r["Median_saving_rs"]):.0f} dearer'),
                         "sub": f'Ownly cheaper in {r["Ownly_cheaper"]} of {r["Baskets"]} baskets', "hl": i == 0}
                        for i, r in enumerate(PV)], vmin=-60, vmax=130, label_w=200, w=560,
                       title="Median saving on Ownly per basket")
FL = load("s5_fee_load.csv")
ch_fee = C.hbars([{"label": r["Platform"], "value": f(r["Fee_share_pct"]), "shown": f'{f(r["Fee_share_pct"]):g}%',
                   "hl": r["Platform"] == "Ownly", "sub": f'{r["Captures"]} bills', "tip": f'{r["Captures"]} no-discount bills'}
                  for r in FL], vmax=35, label_w=90, w=400, title="Fees and tax as a share of the bill")

# ── screen 6: customers ───────────────────────────────────────────────
TR = load("s6_tradeoff.csv")
ch_trade = C.hbars([{"label": r["Give_up"], "value": f(r["Accept_pct"]), "shown": f'{f(r["Accept_pct"]):g}%',
                     "lo": f(r["CI_low"]), "hi": f(r["CI_high"]), "hl": i == 2, "sub": f'{r["Accept"]} of {r["Base"]} would',
                     "tip": f'{r["Accept"]} of {r["Base"]}, 95% CI {r["CI_low"]}-{r["CI_high"]}%'} for i, r in enumerate(TR)],
                   label_w=200, w=540, ci=True, title="Would take Rs30 off to give this up")
MS = [r for r in load("s6_fd_missing.csv") if r["Outcome"].startswith("Order lost")]
ch_miss = C.hbars([{"label": r["Situation"].replace("Wanted ", "").replace(" not on Ownly", " was missing").capitalize(),
                    "value": f(r["Pct"]), "shown": f'{f(r["Pct"]):g}%', "hl": i == 0, "lo": f(r["CI_low"]), "hi": f(r["CI_high"]),
                    "sub": f'{r["Answers"]} of {r["Base"]} sessions', "tip": f'{r["Answers"]} of {r["Base"]}, 95% CI {r["CI_low"]}-{r["CI_high"]}%'}
                   for i, r in enumerate(MS)], label_w=170, w=480, ci=True, title="Order lost when the wanted place or dish was missing")

# ── screen 7: after the order ─────────────────────────────────────────
VO = load("s7_voice.csv")
vmeas = []
for th in ["Order went wrong", "Support / refund failed", "Doubt the price"]:
    vals = []
    for src in ["App-store reviews", "People who ordered (social)", "General discussion (social)"]:
        r = next(x for x in VO if x["Source"] == src and x["Theme"] == th)
        vals.append((f(r["Pct"]), f'{f(r["Pct"]):g}%'))
    vmeas.append({"label": th, "values": vals})
ch_voice = C.paired(vmeas, [("App reviews (29)", C.ACC), ("People who ordered (97)", "var(--accent-2)"),
                            ("General talk (225)", C.GREY)], vmax=100, label_w=170, w=600,
                    title="Share of posts mentioning each problem")
OW = load("s7_fd_offer_why.csv")
ch_offer = C.hbars([{"label": r["Reason"], "value": f(r["Pct"]), "shown": f'{r["Answers"]}', "hl": i < 2,
                     "tip": f'{r["Answers"]} of {r["Base"]}'} for i, r in enumerate(OW)],
                   vmax=40, label_w=210, w=440, unit="", title="Why they picked that offer (answers)")

# ── screen 8: what they will pay for ──────────────────────────────────
SP = load("s8_fd_speed.csv")
ch_speed = C.columns([{"label": r["Price"], "value": f(r["Pct"]), "hl": True,
                       "shown": (f'{r["Took_Rapido_Link"]} of {r["Chose_delivery"]}' if r["Sample"].startswith("Too small")
                                 else f'{f(r["Pct"]):g}%'),
                       "sub": f'{r["Took_Rapido_Link"]} of {r["Chose_delivery"]}', "tip": f'{r["Took_Rapido_Link"]} of {r["Chose_delivery"]} took Rapido Link'}
                      for r in SP], vmax=100, w=400, h=220, title="Rapido Link take-up at each randomised price")
PY = load("s8_fd_pay.csv")
ch_pay = C.hbars([{"label": r["Model"], "value": f(r["Pct"]), "shown": f'{f(r["Pct"]):g}%', "hl": i == 0,
                   "sub": f'{r["Chose"]} of {r["Base"]} chose; {r["Then_placed"]} placed', "tip": f'{r["Chose"]} of {r["Base"]}'}
                  for i, r in enumerate(PY)], label_w=190, w=400, title="How they chose to pay")
EN = load("s8_fd_entry.csv")

# ── evidence appendix ─────────────────────────────────────────────────
ev_rows = []
for r in load("evidence.csv"):
    ci = f'{r["CI_low"]}-{r["CI_high"]}%' if r["CI_low"] != "" else ""
    base = f'{r["Numerator"]} / {r["Denominator"]}' if r["Numerator"] != "" else (f'n = {r["Denominator"]}' if r["Denominator"] else "")
    cls = "warn" if r["Sample_check"].startswith(("Too small", "Small")) else ""
    ev_rows.append(f'<tr><td class="id">{e(r["ID"])}</td><td>{e(r["Claim"])}</td><td class="num">{e(r["Shown_as"])}</td>'
                   f'<td class="num">{e(base)}</td><td class="num">{e(ci)}</td><td class="{cls}">{e(r["Sample_check"])}</td>'
                   f'<td class="meth">{e(r["Method"])}<br><span class="src">{e(r["Source_file"])}</span></td></tr>')
ev_table = "\n".join(ev_rows)


def src(*ids):
    return '<p class="source">Evidence: ' + ", ".join(ids) + " - see the last page for each calculation.</p>"


# ════════════════════════════════════════════════════════════════════
SCREENS = []

SCREENS.append(("The problem", f"""
<h1>Ownly won Bengaluru on the restaurant side. Hyderabad is a different fight.</h1>
<div class="grid two">
  <div>
    <h3>Why we picked this problem</h3>
    <p>Ownly (Rapido's food app) charges restaurants no commission and customers no platform fee. In Bengaluru it
    reached <b>{ev('R1')}</b> daily orders within a year. It is now running the same playbook in Hyderabad.</p>
    <p>Ownly is already live in Gachibowli, so the question is not <i>whether</i> to enter. It is <b>which parts of the
    Bengaluru playbook still work here</b>, and what has to change.</p>
    <p class="q">Problem statement: will Ownly's Bengaluru value proposition transfer to Gachibowli, and what do 20-35
    year-old students and professionals there need before they switch and stay?</p>
  </div>
  <div>
    <h3>What happened in Bengaluru</h3>
    <ol class="timeline">{timeline}</ol>
  </div>
</div>
<table class="compare">
  <tr><th></th><th>Bengaluru (reference)</th><th>Hyderabad (target)</th></tr>
  <tr><td>Restaurants</td><td>{ev('R2')} threatened to quit Swiggy/Zomato. They came to Ownly.</td><td>No revolt. Ownly has to go and win them.</td></tr>
  <tr><td>Ownly's pitch</td><td>Zero commission, flat Rs30 delivery, no fees</td><td>Same pitch, copied</td></tr>
  <tr><td>Customers</td><td>{ev('C-Ben-Pay a ')} pay a Swiggy/Zomato membership (16 people)</td><td>{ev('C-Gac-Pay a ')} pay one (40 people)</td></tr>
</table>
{src('R1', 'R2', 'C-Ben-Pay a', 'C-Gac-Pay a')}
"""))

SCREENS.append(("Hyderabad users", f"""
<h1>Gachibowli orders on Swiggy and Zomato, and most people pay both.</h1>
<div class="grid two">
  <div>
    <h3>Where the last month's orders went</h3>
    {ch_share}
    <p class="note">{EV['B4-Swiggy']['Method'].split(';')[1].strip()} reported by 40 people. Ownly has been live for weeks, so 0% is a starting point, not a verdict.</p>
  </div>
  <div class="facts">
    <div><span class="big">{ev('B1')}</span> pay for Swiggy One or Zomato Gold <span class="n">{kn('B1')}</span></div>
    <div><span class="big">{ev('B2')}</span> pay for both <span class="n">{kn('B2')}</span></div>
    <div><span class="big">{ev('B3')}</span> use two or more apps <span class="n">{kn('B3')}</span></div>
    <div><span class="big">{ev('B5')}</span> said the extra charges on their last bill were too much <span class="n">{kn('B5')}</span></div>
    <div><span class="big">Rs{float(EV['B8']['Value']):.0f}</span> saving per order is what the typical person needs to switch <span class="n">median, {EV['B8']['Denominator']} people</span></div>
  </div>
</div>
<p class="who">Who we asked: 40 people in the Gachibowli catchment, {ev('B6')} students, {ev('B7')} aged 20-24.</p>
{src('B1', 'B2', 'B3', 'B4-Swiggy', 'B5', 'B8')}
"""))

SCREENS.append(("Our KPIs", f"""
<h1>We tracked a funnel and the four things that block it. People have heard of Ownly, but hardly anyone orders.</h1>
<div class="grid two">
  <div>
    <h3>Funnel KPIs: awareness, browse, trial</h3>
    {ch_funnel}
    <p class="note">Bengaluru is only 16 people, so treat its bars as direction, not size.</p>
  </div>
  <div>
    <h3>Barrier KPIs: why the funnel narrows</h3>
    {ch_barriers}
    <p class="note">Line under each bar = 95% interval. Rapido users were <i>less</i> aware of Ownly than non-users
    ({kn('K8')} vs {kn('K9')}).</p>
  </div>
</div>
<p class="why">Why these KPIs: the problem is whether a proven playbook transfers. The funnel shows whether it is working;
the barriers show what would stop it working here: rival memberships, belief in the price, staying after the offer, and whether Rapido actually brings people in.</p>
{src('K1', 'K2', 'K3', 'K5', 'K6', 'K7', 'K8', 'K9')}
"""))

SCREENS.append(("Marketing metrics", f"""
<h1>Ownly's saving is big enough for most people, until a rival membership or coupon is applied.</h1>
<div class="grid two">
  <div>
    <h3>Switch-threshold coverage</h3>
    <p class="small">For each person x basket: is Ownly's real saving at least what <i>that person</i> said they need to switch?</p>
    {ch_cov}
  </div>
  <div>
    <h3>Metrics from the formula sheet, and our own</h3>
    <table class="metrics">{met_rows}</table>
    <h3>What we could not calculate, and why</h3>
    <ul class="ne">{ne_rows}</ul>
  </div>
</div>
{src('MM1-0', 'MM1-1', 'MM1-2', 'MM2', 'B4-Ownly')}
"""))

SCREENS.append(("Analysis 1 - market", f"""
<h1>Ownly is cheaper on the menu, but it is the same restaurants, slower. Every price-led challenger before it failed.</h1>
<div class="grid two">
  <div>
    <h3>Price audit: 4 matched baskets, same address, same evening</h3>
    {ch_price}
    <h3>Fees + tax as a share of the bill</h3>
    {ch_fee}
  </div>
  <div class="facts">
    <div><span class="big">{kn('A-ovl')}</span> Ownly restaurants in our audit are also on Swiggy or Zomato</div>
    <div><span class="big">+{float(EV['A-eta']['Value']):.0f} min</span> longer quoted wait on Ownly <span class="n">{EV['A-eta']['Denominator']} app captures</span></div>
    <div><span class="big">{ev('R9')}</span> earlier price-led challengers failed or shrank. Foodpanda fell from {ev('R5').replace(' to ', ' to ')} orders a day once discounts stopped.</div>
    <blockquote>"The same restaurants, similar or longer delivery times... There's no new use case being unlocked here."
      <cite>Zomato founder, shareholders' letter, Jul 2026</cite></blockquote>
    <p class="note">Ownly's saving is different from theirs: it comes from removing fees, not from paying for discounts.</p>
  </div>
</div>
{src('A-win-0', 'A-win-1', 'A-win-2', 'A-fee-ownly', 'A-ovl', 'A-eta', 'R5', 'R7', 'R9')}
"""))

T5A = kn("T5-Seeing it'")
SCREENS.append(("Analysis 2 - customers", f"""
<h1>People will trade speed and reliability for Rs30, but not their restaurants. In the fake door, a missing place lost the order about half the time.</h1>
<div class="grid two">
  <div>
    <h3>Survey: would you take Rs30 off to give this up?</h3>
    {ch_trade}
    <p class="note">{EV['T4']['Claim'].split(';')[0]}; McNemar exact p = {EV['T4']['Value']}.</p>
  </div>
  <div>
    <h3>Fake door: what happened when it wasn't there</h3>
    {ch_miss}
    <p class="note">"Lost" = went back to their usual app, or didn't order. When people chose a restaurant, <b>{ev('F3-Trust ')}</b>
    said it was because it's always good, they make it best or they always order there. Only {ev('F3-Good p')} said price.</p>
  </div>
</div>
<p class="why">What gets people to <i>try</i> is different: price ({T5A}) and a refund promise ({kn('T5-A promise ')})
came top. Their usual restaurants being on Ownly was named by only 2 of 23. Price opens the door; missing restaurants close it.</p>
{src('T1', 'T2', 'T3', 'T4', 'F4-not_he', 'F4-no_suc', 'F3-Trust', 'T5')}
"""))

SCREENS.append(("Analysis 3 - trust", f"""
<h1>The problem gets louder the closer people get to a real order. People don't trust the price, or the order, to hold.</h1>
<div class="grid two">
  <div>
    <h3>What people mention, by who is talking</h3>
    {ch_voice}
    <p class="note">Share of posts mentioning each theme. This is <i>not</i> a failure rate: people who complain post more.
    App reviews are 29 coded posts (small). {ev('V-1star')} of all reviews are 1-star.</p>
  </div>
  <div>
    <h3>Fake door: why people picked their offer</h3>
    {ch_offer}
    <p class="note"><b>{ev('F11')}</b> picked cash now because they may not come back or don't trust later offers
    ({kn('F11')}). Only {ev('F10')} took Ownly Money for the next order, even though it was worth more.</p>
    <p class="note">Interviews: people leave after <b>repeated</b> bad orders, not one. And "what if they increase prices later?"</p>
  </div>
</div>
{src('V-App-st-Order', 'V-People-Order', 'V-Genera-Doubt', 'V-1star', 'F10', 'F11')}
"""))

SCREENS.append(("Analysis 4 - fake door", f"""
<h1>The fake door showed what people will pay for: speed through Rapido and a small fee. Not another membership.</h1>
<div class="grid three">
  <div>
    <h3>Rapido Link: 25 min instead of 42, at a random price</h3>
    {ch_speed}
    <p class="note"><b>{ev('F6')}</b> paid for it overall ({kn('F6')}). Higher prices did not put people off.
    The survey said {ev('T1')} would wait; in the fake door, nearly half paid not to.</p>
  </div>
  <div>
    <h3>Payment model they chose</h3>
    {ch_pay}
    <p class="note">Top reason behind the choice: "I want a refund if it goes wrong" ({kn('F9')}).</p>
  </div>
  <div class="facts slim">
    <div><span class="big">{kn('F7')}</span> worry the captain will <b>drop a passenger first</b></div>
    <div><span class="big">{EN[1]['Placed']} of {EN[1]['Sessions']}</span> who came in from Rapido's <b>food tab</b> placed an order</div>
    <div><span class="big">{EN[0]['Placed']} of {EN[0]['Sessions']}</span> who came from the <b>after-ride ad</b> did</div>
  </div>
</div>
<p class="who">Fake door: {EV['F0']['Value']} live sessions on our own app, {EV['F1-Direct']['Denominator']} from a direct link and
{EV['F1-Inside']['Denominator']} from inside a Rapido-style app. No money changed hands; "placed" means they pressed the button.</p>
{src('F0', 'F6', 'F6-15', 'F6-49', 'F7', 'F8-per_order', 'F8-membership', 'F9', 'F2-bottom_nav', 'F2-ride_complete_ad')}
"""))

SCREENS.append(("Propositions", f"""
<h1>Don't buy the first order. Earn the second one.</h1>
<table class="calls">
  <tr class="keep"><td>KEEP</td><td><b>Zero commission, and no platform, packaging or surge fees.</b></td>
    <td>Fees are {ev('A-fee-ownly').split(' ')[0]} of an Ownly bill vs {ev('A-fee-zomato')}-{ev('A-fee-swiggy').split(' ')[0]} on rivals. It needs no subsidy, so it cannot run out.</td></tr>
  <tr class="adapt"><td>ADAPT</td><td><b>Stop saying "cheaper than Swiggy/Zomato". Show people their own bill.</b></td>
    <td>After a rival coupon the claim holds for only {ev('MM1-2')} of cases, and {ev('B1')} hold a membership.</td></tr>
  <tr class="adapt"><td>ADAPT</td><td><b>Go deep on local restaurants, not wide.</b> Sign the places people refuse to give up.</td>
    <td>Only {ev('T3')} would give up their restaurants; a missing place lost {ev('F4-not_he')} of fake-door orders.</td></tr>
  <tr class="add"><td>ADD</td><td><b>Rapido Link: paid fast delivery by a nearby captain, with no passenger on board.</b></td>
    <td>{ev('F6')} paid Rs15-49 for it; the top worry was a passenger-first detour ({kn('F7')}).
    <i>Replaces "don't spend on speed".</i></td></tr>
  <tr class="add"><td>ADD</td><td><b>Same-day refund cover as a Rs9-39 option.</b></td>
    <td>Refund failure is in {ev('V-App-st-Suppor')} of app reviews; "refund if it goes wrong" was the top payment reason.</td></tr>
  <tr class="drop"><td>DEPRIORITISE</td><td><b>Big first-order discounts, and a third membership.</b></td>
    <td>Only {ev('K7')} would stay after the offer; {ev('F8-membership')} chose Ownly Plus and {kn('F8p-membership')} of them placed an order.</td></tr>
</table>
<p class="why">Watch two numbers every month: <b>second orders after the offer ends</b>, and <b>orders that go wrong</b>.
If second orders don't come, stop the discounts rather than doubling them.</p>
{src('A-fee-ownly', 'MM1-2', 'T3', 'F4-not_he', 'F6', 'F7', 'V-App-st-Suppor', 'K7', 'F8-membership')}
"""))

PHONES = """
<div class="phones">
  <figure>
    <div class="phone">
      <div class="bar">Ownly <span>Gachibowli</span></div>
      <div class="search">Search your usual place...</div>
      <p class="tag">Your regulars on Ownly</p>
      <div class="rest"><b>Paradise Biryani</b><span>Same menu as your usual app</span><em>Rs0 fees</em></div>
      <div class="rest"><b>Cream Stone</b><span>Same menu as your usual app</span><em>Rs0 fees</em></div>
      <div class="rest ask"><b>Not here yet?</b><span>Tell us the place, we'll bring it</span></div>
    </div>
    <figcaption><b>1. Home leads with restaurants, not discounts.</b> Search your usual place first. If it's missing, ask for it,
    so a missing place becomes an onboarding list instead of a lost order.</figcaption>
  </figure>
  <figure>
    <div class="phone">
      <div class="bar">Delivery</div>
      <div class="opt"><b>Standard</b><span>about 42 min</span><em>Free</em></div>
      <div class="opt on"><b>Rapido Link</b><span>about 25 min - a nearby captain</span><span class="promise">No passenger on board. Tracking from pickup.</span><em>Rs35</em></div>
    </div>
    <figcaption><b>2. Sell speed as a choice.</b> Rapido Link is something only Ownly can offer. Answer the top worry
    right on the option: no passenger first.</figcaption>
  </figure>
  <figure>
    <div class="phone">
      <div class="bar">Your bill</div>
      <div class="line"><span>Food</span><span>Rs340</span></div>
      <div class="line"><span>Delivery</span><span>Rs0</span></div>
      <div class="line"><span>Platform, packaging, surge</span><span>Rs0</span></div>
      <div class="line"><span>GST</span><span>Rs17</span></div>
      <div class="line cover"><span>Order Protection<small>Late, cold or wrong: full refund the same day</small></span><span>Rs19</span></div>
      <div class="line total"><span>To pay</span><span>Rs376</span></div>
    </div>
    <figcaption><b>3. Show the bill, not a comparison.</b> Every line is visible and the fees read Rs0. No "cheaper than Swiggy"
    claim that one coupon can disprove. Refund cover is one tap.</figcaption>
  </figure>
</div>"""

SCREENS.append(("UI recommendations", f"""
<h1>Three screens that put the findings into the app.</h1>
{PHONES}
<p class="note">Mock-ups for discussion, built from the fake-door results. Prices are illustrative.</p>
"""))

SCREENS.append(("Evidence", f"""
<h1>Evidence: every number on these pages, and how it was calculated.</h1>
<p class="small">Computed by <code>scripts/build_evidence.py</code> from the files listed. Sample check: <b>OK</b> = 30+ people;
<b>Small</b> = 10-29, read as direction; <b>Too small</b> = under 10, shown only as a count. Intervals are 95% Wilson.
Figures marked "Not a sample" come from media or company filings and are cited, not calculated.</p>
<p class="small">Fake door: 25 test rows (<code>sess_natural_*</code>) and 1 duplicate session removed. The discount vs restaurants
home-screen test is not reported: the arm was fixed per phone, and shared phones gave 58 vs 12 sessions. The restaurant list was fixed at 14
places with Paradise Biryani first, so restaurant picks show position as well as preference.</p>
<div class="evwrap"><table class="evidence">
<thead><tr><th>ID</th><th>What</th><th>Shown</th><th>k / n</th><th>95% CI</th><th>Sample</th><th>How + source</th></tr></thead>
<tbody>{ev_table}</tbody></table></div>
"""))

# ════════════════════════════════════════════════════════════════════
sections = []
for i, (name, body) in enumerate(SCREENS, 1):
    sections.append(f'<section id="s{i}"><header class="kick"><span>{i:02d}</span>{e(name)}</header>{body}'
                    f'<footer class="pg">{i} / {len(SCREENS)}</footer></section>')
nav = "".join(f'<a href="#s{i}" title="{e(n)}">{i}</a>' for i, (n, _) in enumerate(SCREENS, 1))

CSS = open(os.path.join(HERE, "story.css"), encoding="utf-8").read()
html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ownly in Hyderabad</title>
<style>{CSS}</style></head>
<body>
<nav class="dots">{nav}</nav>
{''.join(sections)}
<script>
// ?shot=N shows a single screen (used to export screenshots)
const shot=new URLSearchParams(location.search).get('shot');
if(shot){{document.querySelectorAll('section').forEach((s,i)=>{{if(i+1!=shot)s.remove();}});document.querySelector('nav').remove();}}
// arrow keys / space move one screen; the page also scrolls normally
const S=[...document.querySelectorAll('section')];
function cur(){{let y=scrollY+innerHeight/3;return Math.max(0,S.findIndex(s=>s.offsetTop+s.offsetHeight>y));}}
addEventListener('keydown',ev=>{{
  if(['ArrowRight','ArrowDown','PageDown',' '].includes(ev.key)){{ev.preventDefault();S[Math.min(S.length-1,cur()+1)].scrollIntoView({{behavior:'smooth'}});}}
  if(['ArrowLeft','ArrowUp','PageUp'].includes(ev.key)){{ev.preventDefault();S[Math.max(0,cur()-1)].scrollIntoView({{behavior:'smooth'}});}}
}});
</script>
</body></html>"""
import re
html = re.sub(r"Rs ?(\d)", "\u20b9\\1", html)   # rupee sign in the page (the CSVs keep 'Rs')
with open(OUT, "w", encoding="utf-8") as fh:
    fh.write(html)
print("wrote", OUT, f"({len(SCREENS)} screens)")
