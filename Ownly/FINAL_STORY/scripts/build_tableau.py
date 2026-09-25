#!/usr/bin/env python3
"""
build_tableau.py - writes ../Ownly_Hyderabad_Story.twbx (a Tableau Story, one story point per screen).

Uses the same ../data/*.csv as the HTML page, copied to ../tableau/Data with two helper
columns added where a chart needs them:  Highlight (Yes/No, drives the accent colour)
and Sort (keeps bars in story order instead of alphabetical).

The XML follows what Tableau Desktop 2026.2 writes itself (checked against the
bundled "World Indicators" sample): worksheets -> dashboards -> one storyboard.
"""
import csv, hashlib, os, shutil, zipfile
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "data")
TAB = os.path.join(HERE, "..", "tableau")
DATA = os.path.join(TAB, "Data")
OUT_TWB = os.path.join(TAB, "Ownly_Hyderabad_Story.twb")
OUT_TWBX = os.path.join(HERE, "..", "Ownly_Hyderabad_Story.twbx")
ACCENT, MUTED, ACCENT2, NEG = "#2a78d6", "#cfccc4", "#86b6ef", "#e34948"


def esc(s):
    return escape(str(s), quote=True)


def uid(seed):
    h = hashlib.md5(seed.encode()).hexdigest().upper()
    return "%s-%s-%s-%s-%s" % (h[:8], h[8:12], h[12:16], h[16:20], h[20:32])


def read(name):
    with open(os.path.join(SRC, name), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write(name, header, rows):
    with open(os.path.join(DATA, name), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


# ── 1. Tableau-ready copies of the chart tables ───────────────────────
if os.path.isdir(TAB):
    shutil.rmtree(TAB)
os.makedirs(DATA)
EV = {r["ID"]: r for r in read("evidence.csv")}


def hl_copy(src, dst, label_col, hl_fn, keep=None, extra=None):
    rows = read(src)
    if keep:
        rows = [r for r in rows if keep(r)]
    hdr = list(rows[0].keys())
    out_hdr = [h for h in hdr if h != "Sort"] + ["Highlight", "Sort"] + (list(extra[0]) if extra else [])
    out = []
    for i, r in enumerate(rows):
        line = [r[h] for h in hdr if h != "Sort"] + ["Yes" if hl_fn(r, i) else "No", i]
        if extra:
            line += extra[1](r)
        out.append(line)
    write(dst, out_hdr, out)


hl_copy("s2_order_share.csv", "t_order_share.csv", "App", lambda r, i: r["App"] == "Ownly")
hl_copy("s1_city.csv", "t_city.csv", "Measure", lambda r, i: r["City"] == "Gachibowli",
        keep=lambda r: r["Measure"] != "Pay a rival membership", extra=(["Label"], lambda r: [f'{r["Yes"]} of {r["Base"]}']))
hl_copy("s3_barriers.csv", "t_barriers.csv", "KPI", lambda r, i: i < 2, extra=(["Label"], lambda r: [f'{float(r["Pct"]):g}%  ({r["Yes"]} of {r["Base"]})']))
hl_copy("s4_coverage.csv", "t_coverage.csv", "View", lambda r, i: i == 2, extra=(["Label"], lambda r: [f'{float(r["Coverage_pct"]):g}%  ({r["Pairs_clearing"]} of {r["Pairs"]} pairs)']))
hl_copy("s5_price_views.csv", "t_price.csv", "View", lambda r, i: i == 0,
        extra=(["Label", "Direction"], lambda r: [(f'Rs{float(r["Median_saving_rs"]):.0f} cheaper' if float(r["Median_saving_rs"]) >= 0
                                                   else f'Rs{-float(r["Median_saving_rs"]):.0f} dearer') + f'  ({r["Ownly_cheaper"]} of {r["Baskets"]} baskets)',
                                                  "Ownly cheaper" if float(r["Median_saving_rs"]) >= 0 else "Ownly dearer"]))
hl_copy("s5_fee_load.csv", "t_fee.csv", "Platform", lambda r, i: r["Platform"] == "Ownly",
        extra=(["Label"], lambda r: [f'{float(r["Fee_share_pct"]):g}%  ({r["Captures"]} bills)']))
hl_copy("s6_tradeoff.csv", "t_tradeoff.csv", "Give_up", lambda r, i: i == 2,
        extra=(["Label"], lambda r: [f'{float(r["Accept_pct"]):g}%  ({r["Accept"]} of {r["Base"]})']))
hl_copy("s6_fd_missing.csv", "t_missing.csv", "Situation", lambda r, i: i == 0, keep=lambda r: r["Outcome"].startswith("Order lost"),
        extra=(["Label"], lambda r: [f'{float(r["Pct"]):g}%  ({r["Answers"]} of {r["Base"]})']))
hl_copy("s7_voice.csv", "t_voice.csv", "Theme", lambda r, i: r["Source"] == "App-store reviews",
        keep=lambda r: r["Theme"] in ("Order went wrong", "Support / refund failed", "Doubt the price"))
hl_copy("s7_fd_offer_why.csv", "t_offer_why.csv", "Reason", lambda r, i: i < 2)
hl_copy("s8_fd_speed.csv", "t_speed.csv", "Price", lambda r, i: True,
        extra=(["Label"], lambda r: [f'{r["Took_Rapido_Link"]} of {r["Chose_delivery"]}']))
hl_copy("s8_fd_pay.csv", "t_pay.csv", "Model", lambda r, i: i == 0,
        extra=(["Label"], lambda r: [f'{float(r["Pct"]):g}%  ({r["Chose"]} of {r["Base"]}; {r["Then_placed"]} placed)']))
ev_rows = read("evidence.csv")
write("t_evidence.csv", ["Row", "ID", "Screen", "Claim", "Shown_as", "k_of_n", "CI", "Sample_check", "Method", "Source_file"],
      [[i, r["ID"], r["Screen"], r["Claim"], r["Shown_as"],
        f'{r["Numerator"]} / {r["Denominator"]}' if r["Numerator"] else (f'n = {r["Denominator"]}' if r["Denominator"] else "-"),
        f'{r["CI_low"]}-{r["CI_high"]}%' if r["CI_low"] else "-", r["Sample_check"], r["Method"], r["Source_file"]]
       for i, r in enumerate(ev_rows)])


# ── 2. XML pieces ─────────────────────────────────────────────────────
def sniff(path):
    with open(path, encoding="utf-8") as f:
        rd = csv.reader(f)
        hdr = next(rd)
        rows = list(rd)
    types = []
    for i, _ in enumerate(hdr):
        vals = [r[i] for r in rows if i < len(r) and r[i] != ""]
        kind = "integer"
        for v in vals:
            try:
                if float(v) != int(float(v)):
                    kind = "real"
            except ValueError:
                kind = "string"
                break
        types.append(kind if vals else "string")
    return hdr, types


DS = {}  # ds name -> (file, hdr, types)


def datasource(name, filename, caption, palette=None):
    hdr, types = sniff(os.path.join(DATA, filename))
    DS[name] = (filename, hdr, dict(zip(hdr, types)))
    base = filename[:-4]
    cols = "\n".join(f"            <column datatype='{t}' name='{esc(h)}' ordinal='{i}' />" for i, (h, t) in enumerate(zip(hdr, types)))
    remote = {"string": 129, "integer": 20, "real": 5}
    agg = {"string": "Count", "integer": "Sum", "real": "Sum"}
    oid = f"[{base}.csv_{uid(base).replace('-', '')}]"
    recs = [f"""        <metadata-record class='capability'>
          <remote-name /><remote-type>0</remote-type><parent-name>[{esc(base)}.csv]</parent-name><remote-alias />
          <aggregation>Count</aggregation><contains-null>true</contains-null>
          <attributes>
            <attribute datatype='string' name='character-set'>&quot;UTF-8&quot;</attribute>
            <attribute datatype='string' name='collation'>&quot;en_GB&quot;</attribute>
            <attribute datatype='string' name='field-delimiter'>&quot;,&quot;</attribute>
            <attribute datatype='string' name='header-row'>&quot;true&quot;</attribute>
            <attribute datatype='string' name='locale'>&quot;en_IN&quot;</attribute>
            <attribute datatype='string' name='single-char'>&quot;&quot;</attribute>
          </attributes>
        </metadata-record>"""]
    for i, (h, t) in enumerate(zip(hdr, types)):
        recs.append(f"""        <metadata-record class='column'>
          <remote-name>{esc(h)}</remote-name><remote-type>{remote[t]}</remote-type><local-name>[{esc(h)}]</local-name>
          <parent-name>[{esc(base)}.csv]</parent-name><remote-alias>{esc(h)}</remote-alias><ordinal>{i}</ordinal>
          <local-type>{t}</local-type><aggregation>{agg[t]}</aggregation><contains-null>true</contains-null>
          <object-id>{esc(oid)}</object-id>
        </metadata-record>""")
    meta = "\n".join(
        f"    <column datatype='{t}' name='[{esc(h)}]' role='{'measure' if t != 'string' else 'dimension'}' "
        f"type='{'quantitative' if t != 'string' else 'nominal'}' />" for h, t in zip(hdr, types))
    style = ""
    if palette:
        field, mapping = palette
        maps = "".join(f"<map to='{c}'><bucket>&quot;{esc(v)}&quot;</bucket></map>" for v, c in mapping.items())
        style = (f"\n    <style>\n      <style-rule element='mark'>\n        <encoding attr='color' field='[none:{esc(field)}:nk]' "
                 f"type='palette'>{maps}</encoding>\n      </style-rule>\n    </style>")
    tok = name.split(".", 1)[1]
    return f"""  <datasource caption='{esc(caption)}' inline='true' name='{name}' version='18.1'>
    <connection class='federated'>
      <named-connections>
        <named-connection caption='{esc(base)}' name='textscan.{tok}'>
          <connection class='textscan' directory='Data' filename='{esc(filename)}' password='' server='' />
        </named-connection>
      </named-connections>
      <relation connection='textscan.{tok}' name='{esc(filename)}' table='[{esc(base)}#csv]' type='table'>
        <columns character-set='UTF-8' header='yes' locale='en_IN' separator=','>
{cols}
        </columns>
      </relation>
      <metadata-records>
{chr(10).join(recs)}
      </metadata-records>
    </connection>
{meta}{style}
  </datasource>"""


def inst(f, t):
    return f"[sum:{f}:qk]" if t != "string" else f"[none:{f}:nk]"


SHEETS = []


def sheet(name, ds, rows=(), cols=(), mark="Bar", color=None, label=None, filters=None, sort=None, title=None, fontsize=12):
    _, hdr, T = DS[ds]
    used = list(rows) + list(cols) + [x for x in (color, label) if x] + [f for f, _ in (filters or [])] + ([sort] if sort else [])
    deps, seen = [], set()
    for fld in used:
        if fld in seen:
            continue
        seen.add(fld)
        t = T[fld]
        deps.append(f"        <column datatype='{t}' name='[{esc(fld)}]' role='{'measure' if t != 'string' else 'dimension'}' "
                    f"type='{'quantitative' if t != 'string' else 'nominal'}' />")
        deps.append(f"        <column-instance column='[{esc(fld)}]' derivation='{'Sum' if t != 'string' else 'None'}' "
                    f"name='{esc(inst(fld, t))}' pivot='key' type='{'quantitative' if t != 'string' else 'nominal'}' />")
    srt = ""
    if sort:
        first_dim = next(f for f in list(rows) + list(cols) if T[f] == "string")
        srt = (f"        <computed-sort column='[{ds}].{esc(inst(first_dim, 'string'))}' direction='ASC' "
               f"using='[{ds}].{esc(inst(sort, T[sort]))}' />\n")
    flt = ""
    for fld, vals in (filters or []):
        members = "".join(f"<groupfilter function='member' level='{esc(inst(fld, 'string'))}' member='&quot;{esc(v)}&quot;' />" for v in vals)
        flt += (f"        <filter class='categorical' column='[{ds}].{esc(inst(fld, 'string'))}'>\n"
                f"          <groupfilter function='union' user:ui-domain='relevant' user:ui-enumeration='inclusive' "
                f"user:ui-marker='enumerate'>{members}</groupfilter>\n        </filter>\n")
    enc = ""
    if color:
        enc += f"            <color column='[{ds}].{esc(inst(color, T[color]))}' />\n"
    if label:
        enc += f"            <text column='[{ds}].{esc(inst(label, T[label]))}' />\n"
    shelf = lambda fs: " / ".join(f"[{ds}].{esc(inst(f, T[f]))}" for f in fs)
    ttl = (f"    <layout-options>\n      <title>\n        <formatted-text>\n          <run fontsize='{fontsize}'>{esc(title)}</run>\n"
           f"        </formatted-text>\n      </title>\n    </layout-options>\n") if title else ""
    SHEETS.append((name, f"""  <worksheet name='{esc(name)}'>
{ttl}    <table>
      <view>
        <datasources>
          <datasource caption='{esc(ds)}' name='{ds}' />
        </datasources>
        <datasource-dependencies datasource='{ds}'>
{chr(10).join(deps)}
        </datasource-dependencies>
{srt}{flt}        <aggregation value='true' />
      </view>
      <style>
        <style-rule element='worksheet'>
          <format attr='font-family' value='Tableau Book' />
        </style-rule>
        <style-rule element='gridline'>
          <format attr='line-visibility' value='off' />
        </style-rule>
      </style>
      <panes>
        <pane selection-relaxation-option='selection-relaxation-allow'>
          <view><breakdown value='auto' /></view>
          <mark class='{mark}' />
{('          <encodings>' + chr(10) + enc + '          </encodings>' + chr(10)) if enc else ''}          <style>
            <style-rule element='mark'>
              <format attr='mark-labels-show' value='true' />
              <format attr='size' value='0.6' />
            </style-rule>
          </style>
        </pane>
      </panes>
      <rows>{shelf(rows)}</rows>
      <cols>{shelf(cols)}</cols>
    </table>
    <simple-id uuid='{{{uid("ws:" + name)}}}' />
  </worksheet>"""))


def text_zone(zid, x, y, w, h, runs):
    """runs: list of (text, fontsize, bold, colour)."""
    body = "".join(
        f"<run{' bold=' + chr(39) + 'true' + chr(39) if b else ''} fontcolor='{c}' fontname='Tableau Book' fontsize='{fs}'>"
        f"{esc(t).replace(chr(10), '&#10;')}</run>" for t, fs, b, c in runs)
    return (f"        <zone h='{h}' id='{zid}' type-v2='text' w='{w}' x='{x}' y='{y}'>\n"
            f"          <formatted-text>{body}</formatted-text>\n"
            f"          <zone-style><format attr='margin' value='8' /></zone-style>\n        </zone>\n")


def sheet_zone(zid, name, x, y, w, h):
    return (f"        <zone h='{h}' id='{zid}' name='{esc(name)}' w='{w}' x='{x}' y='{y}'>"
            f"<zone-style><format attr='margin' value='6' /></zone-style></zone>\n")


DASHES = []
W, H = 1300, 640


def dashboard(name, headline, blocks, note):
    """blocks: list of ('sheet', name) or ('text', [runs]) laid out left to right."""
    z, zid = [], 10
    z.append(text_zone(zid, 0, 0, 100000, 15000, [(name.split(" ", 1)[1].upper() + "\n", 10, True, "#2a78d6"),
                                                   (headline, 19, False, "#1b1a18")]))
    zid += 1
    n = len(blocks)
    widths = [100000 // n] * n
    x = 0
    for (kind, val), wd in zip(blocks, widths):
        if kind == "sheet":
            z.append(sheet_zone(zid, val, x, 15000, wd, 71000))
        else:
            z.append(text_zone(zid, x, 15000, wd, 71000, val))
        x += wd
        zid += 1
    z.append(text_zone(zid, 0, 86000, 100000, 14000, [(note, 10, False, "#5b5953")]))
    DASHES.append((name, [v for k, v in blocks if k == "sheet"], f"""  <dashboard enable-sort-zone-taborder='true' name='{esc(name)}'>
    <style />
    <size maxheight='{H}' maxwidth='{W}' minheight='{H}' minwidth='{W}' sizing-mode='fixed' />
    <zones>
      <zone h='100000' id='1' type-v2='layout-basic' w='100000' x='0' y='0'>
{''.join(z)}      </zone>
    </zones>
    <simple-id uuid='{{{uid("db:" + name)}}}' />
  </dashboard>"""))


def facts(items):
    """items: list of (big, small) -> runs for a text zone."""
    runs = []
    for big, small in items:
        runs += [(big + "\n", 22, False, "#1b1a18"), (small + "\n\n", 11, False, "#5b5953")]
    return runs


def ev(i):
    return EV[i]["Shown_as"]


def kn(i):
    return f'{EV[i]["Numerator"]} of {EV[i]["Denominator"]}'


# ── 3. Datasources and sheets ─────────────────────────────────────────
HL = ("Highlight", {"Yes": ACCENT, "No": MUTED})
ds_xml = [
    datasource("federated.order", "t_order_share.csv", "Order share", HL),
    datasource("federated.city", "t_city.csv", "City funnel", ("City", {"Gachibowli": ACCENT, "Bengaluru": MUTED})),
    datasource("federated.barrier", "t_barriers.csv", "Barrier KPIs", HL),
    datasource("federated.cover", "t_coverage.csv", "Switch-threshold coverage", HL),
    datasource("federated.price", "t_price.csv", "Price audit", ("Direction", {"Ownly cheaper": ACCENT, "Ownly dearer": NEG})),
    datasource("federated.fee", "t_fee.csv", "Fee load", HL),
    datasource("federated.trade", "t_tradeoff.csv", "Rs30 trade-offs", HL),
    datasource("federated.miss", "t_missing.csv", "Fake door - missing", HL),
    datasource("federated.voice", "t_voice.csv", "Reviews and social",
               ("Source", {"App-store reviews": ACCENT, "People who ordered (social)": ACCENT2, "General discussion (social)": MUTED})),
    datasource("federated.offer", "t_offer_why.csv", "Fake door - offer reasons", HL),
    datasource("federated.speed", "t_speed.csv", "Fake door - Rapido Link", HL),
    datasource("federated.pay", "t_pay.csv", "Fake door - payment", HL),
    datasource("federated.evid", "t_evidence.csv", "Evidence"),
]

sheet("Order share", "federated.order", rows=["App"], cols=["Share_pct"], color="Highlight", label="Share_pct", sort="Sort",
      title="Share of last-4-week orders (%)")
sheet("City funnel", "federated.city", rows=["Measure", "City"], cols=["Pct"], color="City", label="Label", sort="Sort",
      title="Ownly funnel: Bengaluru (16 people) vs Gachibowli (40 people)")
sheet("Barrier KPIs", "federated.barrier", rows=["KPI"], cols=["Pct"], color="Highlight", label="Label", sort="Sort",
      title="Barrier KPIs (% of people)")
sheet("Coverage", "federated.cover", rows=["View"], cols=["Coverage_pct"], color="Highlight", label="Label", sort="Sort",
      title="Switch-threshold coverage (% of person x basket pairs)")
sheet("Price audit", "federated.price", rows=["View"], cols=["Median_saving_rs"], color="Direction", label="Label", sort="Sort",
      title="Median saving on Ownly per basket (Rs), 4 baskets")
sheet("Fee load", "federated.fee", rows=["Platform"], cols=["Fee_share_pct"], color="Highlight", label="Label", sort="Sort",
      title="Fees + tax as % of the bill")
sheet("Trade-offs", "federated.trade", rows=["Give_up"], cols=["Accept_pct"], color="Highlight", label="Label", sort="Sort",
      title="Would take Rs30 off to give this up (%)")
sheet("Missing place", "federated.miss", rows=["Situation"], cols=["Pct"], color="Highlight", label="Label", sort="Sort",
      title="Fake door: order lost when it wasn't on Ownly (%)")
sheet("Voice", "federated.voice", rows=["Theme", "Source"], cols=["Pct"], color="Source", label="Pct", sort="Sort",
      title="Share of posts mentioning each problem (%)")
sheet("Offer reasons", "federated.offer", rows=["Reason"], cols=["Answers"], color="Highlight", label="Answers", sort="Sort",
      title="Fake door: why they picked their offer (answers)")
sheet("Rapido Link", "federated.speed", rows=["Pct"], cols=["Price"], color="Highlight", label="Label", sort="Sort",
      title="Took Rapido Link at each random price (%)")
sheet("Payment", "federated.pay", rows=["Model"], cols=["Pct"], color="Highlight", label="Label", sort="Sort",
      title="How they chose to pay (%)")
sheet("Evidence table", "federated.evid", rows=["ID", "Claim", "Shown_as", "k_of_n", "CI", "Sample_check"], cols=[],
      mark="Text", label="Source_file", sort="Row", title="Every number, how it was calculated, and whether the sample is big enough", fontsize=11)

# ── 4. Dashboards, in story order ─────────────────────────────────────
dashboard("01 The problem", "Ownly won Bengaluru on the restaurant side. Hyderabad is a different fight.", [
    ("text", [("WHY WE PICKED THIS PROBLEM\n", 10, True, "#5b5953"),
              (f"Ownly charges restaurants no commission and customers no platform fee. In Bengaluru it reached {ev('R1')} daily orders "
               "within a year and is now copying that playbook into Hyderabad, where it is already live.\n\n", 13, False, "#1b1a18"),
              ("Problem statement: will Ownly's Bengaluru value proposition transfer to Gachibowli, and what do 20-35 year-old "
               "students and professionals there need before they switch and stay?", 14, True, "#1b1a18")]),
    ("text", [("BENGALURU vs HYDERABAD\n", 10, True, "#5b5953"),
              (f"Restaurants:  Bengaluru - {ev('R2')} threatened to quit Swiggy/Zomato and came to Ownly.  Hyderabad - no revolt.\n\n", 13, False, "#1b1a18"),
              ("Pitch:  zero commission, flat Rs30 delivery, no fees - copied as-is.\n\n", 13, False, "#1b1a18"),
              (f"Customers:  {ev('C-Ben-Pay a ')} pay a rival membership in Bengaluru (16 people); {ev('C-Gac-Pay a ')} in Gachibowli (40 people).\n\n", 13, False, "#1b1a18"),
              ("Aug 2025 pilot  >  Mar 2026 citywide, ~20,000 restaurants  >  Jul 2026 restaurant revolt  >  Aug 2026 50,000+ orders/day  >  Sep 2026 live in Gachibowli", 11, False, "#5b5953")]),
], "Evidence: R1, R2, C-Ben-Pay a, C-Gac-Pay a (Evidence page).")

dashboard("02 Hyderabad users", "Gachibowli orders on Swiggy and Zomato, and most people pay both.", [
    ("sheet", "Order share"),
    ("text", facts([(ev("B1"), f"pay Swiggy One or Zomato Gold ({kn('B1')})"), (ev("B2"), f"pay for both ({kn('B2')})"),
                    (ev("B3"), f"use two or more apps ({kn('B3')})"), (ev("B5"), f"said the extra charges were too much ({kn('B5')})"),
                    (f"Rs{float(EV['B8']['Value']):.0f}", f"median saving needed to switch ({EV['B8']['Denominator']} people)")])),
], f"40 people in the Gachibowli catchment, {ev('B6')} students, {ev('B7')} aged 20-24. Ownly has been live for weeks, so 0% of orders is a starting point.  Evidence: B1-B8.")

dashboard("03 Our KPIs", "We tracked a funnel and the four things that block it. People have heard of Ownly, but hardly anyone orders.", [
    ("sheet", "City funnel"), ("sheet", "Barrier KPIs"),
], f"Why these KPIs: the funnel shows whether the playbook is working; the barriers show what would stop it here. Bengaluru is 16 people - direction only. "
   f"Rapido users were less aware of Ownly than non-users ({kn('K8')} vs {kn('K9')}).  Evidence: K1-K9.")

dashboard("04 Marketing metrics", "Ownly's saving is big enough for most people, until a rival membership or coupon is applied.", [
    ("sheet", "Coverage"),
    ("text", [("FORMULA-SHEET METRICS\n", 10, True, "#5b5953"),
              (f"Unit (volume) share: 0% of {EV['B4-Ownly']['Method'].split(';')[1].strip()} - a floor, Ownly is weeks old\n", 12, False, "#1b1a18"),
              (f"Penetration share: {kn('MM2')} ({ev('MM2')})\n\n", 12, False, "#1b1a18"),
              ("NOT COMPUTABLE, AND WHY\n", 10, True, "#5b5953"),
              ("Retention, CLV, CAC, YoY growth, revenue share - need Ownly's own customer, spend and revenue data, or a prior period.", 12, False, "#1b1a18")]),
], "Coverage = person x basket pairs where Ownly's real saving is at least what that person said they need to switch.  Evidence: MM1-0, MM1-1, MM1-2, MM2.")

dashboard("05 Analysis - market", "Ownly is cheaper on the menu, but it is the same restaurants, slower. Every price-led challenger before it failed.", [
    ("sheet", "Price audit"), ("sheet", "Fee load"),
    ("text", facts([(kn("A-ovl"), "Ownly restaurants in our audit are also on Swiggy or Zomato"),
                    (f"+{float(EV['A-eta']['Value']):.0f} min", f"longer quoted wait ({EV['A-eta']['Denominator']} captures)"),
                    (ev("R9"), "earlier price-led challengers failed or shrank; Foodpanda ~200,000 to ~5,000 orders a day")])),
], "\"There's no new use case being unlocked here.\" - Zomato founder, Jul 2026.  Ownly's saving comes from removing fees, not paying for discounts.  Evidence: A-*, R5, R7, R9.")

dashboard("06 Analysis - customers", "People will trade speed and reliability for Rs30, but not their restaurants. In the fake door a missing place lost the order about half the time.", [
    ("sheet", "Trade-offs"), ("sheet", "Missing place"),
], f"McNemar exact p = {EV['T4']['Value']}. When choosing a restaurant, {ev('F3-Trust ')} said trust/loyalty and {ev('F3-Good p')} said price. "
   f"What gets people to TRY is price ({kn(chr(84)+'5-Seeing it' + chr(39))}) and a refund promise ({kn('T5-A promise ')}).  Evidence: T1-T5, F3, F4.")

dashboard("07 Analysis - trust", "The problem gets louder the closer people get to a real order. People don't trust the price, or the order, to hold.", [
    ("sheet", "Voice"), ("sheet", "Offer reasons"),
], f"Share of posts mentioning a theme, not a failure rate. App reviews = 29 coded posts (small). {ev('F11')} took cash now because they may not return or don't trust later offers; "
   f"only {ev('F10')} took Ownly Money. Interviews: people leave after repeated bad orders.  Evidence: V-*, F10, F11.")

dashboard("08 Analysis - fake door", "The fake door showed what people will pay for: speed through Rapido and a small fee. Not another membership.", [
    ("sheet", "Rapido Link"), ("sheet", "Payment"),
    ("text", facts([(kn("F7"), "worry the captain will drop a passenger first"),
                    (kn("F2-bottom_nav"), "who came in from Rapido's food tab placed an order"),
                    (kn("F2-ride_complete_ad"), "who came from the after-ride ad did")])),
], f"{float(EV['F0']['Value']):.0f} live fake-door sessions; no money changed hands. {ev('F6')} paid for Rapido Link overall ({kn('F6')}) while the survey said {ev('T1')} would wait.  Evidence: F0-F9.")

dashboard("09 Propositions", "Don't buy the first order. Earn the second one.", [
    ("text", [("KEEP   ", 12, True, ACCENT), ("Zero commission; no platform, packaging or surge fees.  ", 13, True, "#1b1a18"),
              (f"Fees {ev('A-fee-ownly').split(' ')[0]} of an Ownly bill vs {ev('A-fee-zomato')}-{ev('A-fee-swiggy').split(' ')[0]} on rivals.\n\n", 12, False, "#5b5953"),
              ("ADAPT   ", 12, True, "#b07800"), ("Stop saying 'cheaper than Swiggy/Zomato' - show people their own bill.  ", 13, True, "#1b1a18"),
              (f"After a rival coupon the saving clears only {ev('MM1-2')} of cases.\n\n", 12, False, "#5b5953"),
              ("ADAPT   ", 12, True, "#b07800"), ("Go deep on local restaurants people refuse to give up.  ", 13, True, "#1b1a18"),
              (f"Only {ev('T3')} would give them up; a missing place lost {ev('F4-not_he')} of fake-door orders.\n\n", 12, False, "#5b5953"),
              ("ADD   ", 12, True, "#138a5f"), ("Rapido Link: paid fast delivery, no passenger on board.  ", 13, True, "#1b1a18"),
              (f"{ev('F6')} paid Rs15-49 for it. Replaces 'don't spend on speed'.\n\n", 12, False, "#5b5953"),
              ("ADD   ", 12, True, "#138a5f"), ("Same-day refund cover as a Rs9-39 option.  ", 13, True, "#1b1a18"),
              (f"Refund failure is in {ev('V-App-st-Suppor')} of app reviews.\n\n", 12, False, "#5b5953"),
              ("DEPRIORITISE   ", 12, True, "#8a877f"), ("Big first-order discounts, and a third membership.  ", 13, True, "#1b1a18"),
              (f"Only {ev('K7')} would stay after the offer; {kn('F8p-membership')} Ownly Plus choosers placed an order.", 12, False, "#5b5953")]),
], "Watch two numbers monthly: second orders after the offer ends, and orders that go wrong. If second orders don't come, stop the discounts rather than doubling them.")

dashboard("10 UI recommendations", "Three screens that put the findings into the app.", [
    ("text", [("1. HOME LEADS WITH RESTAURANTS\n", 11, True, ACCENT),
              ("Search your usual place first; 'Your regulars on Ownly'. If a place is missing, ask for it - a missing place becomes an onboarding list, not a lost order.", 13, False, "#1b1a18")]),
    ("text", [("2. SELL SPEED AS A CHOICE\n", 11, True, ACCENT),
              ("Standard 42 min free, or Rapido Link 25 min for a fee - 'No passenger on board. Tracking from pickup.' answers the top worry on the option itself.", 13, False, "#1b1a18")]),
    ("text", [("3. SHOW THE BILL, NOT A COMPARISON\n", 11, True, ACCENT),
              ("Every line visible, fees read Rs0, no 'cheaper than Swiggy' claim a coupon can disprove. Order Protection: late, cold or wrong - full refund the same day.", 13, False, "#1b1a18")]),
], "Phone mock-ups of these three screens are on page 10 of the HTML version (Ownly_Hyderabad_Story.html).")

dashboard("11 Evidence", "Evidence: every number, how it was calculated, and whether the sample is big enough.", [
    ("sheet", "Evidence table"),
], "OK = 30+; Small = 10-29 (direction); Too small = under 10 (count only). 95% Wilson intervals. 'Not a sample' = cited media/filings. "
   "Fake door: 25 test rows and 1 duplicate removed; home-screen A/B dropped (arm fixed per phone: 58 vs 12).")

CAPTIONS = [
    "The problem", "Hyderabad users", "Our KPIs", "Marketing metrics", "Market & competitors", "Customers",
    "Trust", "Fake door", "Propositions", "UI", "Evidence"]

points = "\n".join(f"                  <story-point caption='{esc(c)}' captured-sheet='{esc(d[0])}' id='{i}' />"
                   for i, (c, d) in enumerate(zip(CAPTIONS, DASHES), 1))
story = f"""  <dashboard name='Ownly in Hyderabad' type='storyboard'>
    <layout-options>
      <title>
        <formatted-text>
          <run>Ownly in Hyderabad: will the Bengaluru playbook transfer?</run>
        </formatted-text>
      </title>
    </layout-options>
    <style />
    <size maxheight='{H + 150}' maxwidth='{W}' minheight='{H + 150}' minwidth='{W}' sizing-mode='fixed' />
    <zones>
      <zone h='100000' id='2' type-v2='layout-basic' w='100000' x='0' y='0'>
        <zone h='100000' id='1' param='vert' removable='false' type-v2='layout-flow' w='100000' x='0' y='0'>
          <zone h='4453' id='3' type-v2='title' w='100000' x='0' y='0' />
          <zone fixed-size='80' h='11000' id='4' is-fixed='true' paired-zone-id='5' removable='false' type-v2='flipboard-nav' w='100000' x='0' y='4453' />
          <zone h='84547' id='5' paired-zone-id='4' removable='false' type-v2='flipboard' w='100000' x='0' y='15453'>
            <flipboard active-id='1' nav-type='caption' show-nav-arrows='true'>
              <story-points>
{points}
              </story-points>
            </flipboard>
          </zone>
        </zone>
      </zone>
    </zones>
    <simple-id uuid='{{{uid("story")}}}' />
  </dashboard>"""

# ── 5. Windows and assembly ───────────────────────────────────────────
wins = []
for name, _ in SHEETS:
    wins.append(f"""    <window class='worksheet' hidden='true' name='{esc(name)}'>
      <cards>
        <edge name='left'><strip size='160'><card type='pages' /><card type='filters' /><card type='marks' /></strip></edge>
        <edge name='top'><strip size='2147483647'><card type='columns' /></strip><strip size='2147483647'><card type='rows' /></strip><strip size='31'><card type='title' /></strip></edge>
      </cards>
      <simple-id uuid='{{{uid("win:" + name)}}}' />
    </window>""")
for name, sheets_in, _ in DASHES:
    vps = "".join(f"<viewpoint name='{esc(s)}'><zoom type='entire-view' /></viewpoint>" for s in sheets_in)
    wins.append(f"""    <window class='dashboard' hidden='true' name='{esc(name)}'>
      <viewpoints>{vps}</viewpoints>
      <active id='-1' />
      <simple-id uuid='{{{uid("dwin:" + name)}}}' />
    </window>""")
wins.append(f"""    <window class='dashboard' maximized='true' name='Ownly in Hyderabad'>
      <viewpoints />
      <active id='-1' />
      <simple-id uuid='{{{uid("swin")}}}' />
    </window>""")

xml = f"""<?xml version='1.0' encoding='utf-8' ?>
<workbook original-version='18.1' source-build='2026.2.1 (20262.26.0708.1337)' source-platform='mac' version='18.1' xmlns:user='http://www.tableausoftware.com/xml/user'>
  <document-format-change-manifest>
    <AccessibleZoneTabOrder />
    <AnimationOnByDefault />
    <AutoCreateAndUpdateDSDPhoneLayouts />
    <MarkAnimation />
    <ObjectModelEncapsulateLegacy />
    <ObjectModelTableType />
    <SchemaViewerObjectModel />
    <SetMembershipControl />
    <SheetIdentifierTracking />
    <SortTagCleanup />
    <WindowsPersistSimpleIdentifiers />
  </document-format-change-manifest>
  <preferences>
    <preference name='ui.encoding.shelf.height' value='24' />
    <preference name='ui.shelf.height' value='26' />
  </preferences>
  <datasources>
{chr(10).join(ds_xml)}
  </datasources>
  <worksheets>
{chr(10).join(x for _, x in SHEETS)}
  </worksheets>
  <dashboards>
{chr(10).join(x for _, _, x in DASHES)}
{story}
  </dashboards>
  <windows source-height='30'>
{chr(10).join(wins)}
  </windows>
</workbook>
"""
with open(OUT_TWB, "w", encoding="utf-8") as f:
    f.write(xml)
with zipfile.ZipFile(OUT_TWBX, "w", zipfile.ZIP_DEFLATED) as z:
    z.write(OUT_TWB, os.path.basename(OUT_TWB))
    for fn in sorted({v[0] for v in DS.values()}):
        z.write(os.path.join(DATA, fn), "Data/" + fn)
print("wrote", OUT_TWBX, f"- {len(DS)} datasources, {len(SHEETS)} sheets, {len(DASHES)} dashboards, 1 story")
