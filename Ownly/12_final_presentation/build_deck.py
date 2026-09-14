#!/usr/bin/env python3
"""Build the DRAFT final deck (17 Sep submission).

Slides built from evidence already collected are filled in. Slides that need the 3-day survey/audit are clearly
marked TO FILL. No survey or audit numbers are invented.

Requires: python-pptx, matplotlib.
Run:      python build_deck.py   (writes Ownly_Gachibowli_deck_DRAFT.pptx and charts/*.png next to this file)
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

HERE = os.path.dirname(os.path.abspath(__file__))
CH = os.path.join(HERE, "charts")
os.makedirs(CH, exist_ok=True)

# ---- palette (dataviz reference instance, light mode) ----
INK, INK2, MUTED, GRID, AXIS = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
SURFACE = "#fcfcfb"
BLUE_DARK, BLUE_LIGHT, BLUE = "#1c5cab", "#86b6ef", "#2a78d6"

plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
                     "axes.edgecolor": AXIS, "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": INK2,
                     "figure.facecolor": SURFACE, "axes.facecolor": SURFACE})


def chart_social_families():
    # Source: 05_review_mining/social/social_analysis.md §2.3 (108 de-duplicated first-hand incidents; one incident can sit in several families)
    fam = [("Fulfilment failure", 46, 38), ("Support / refund failure", 29, 27), ("Price win", 19, 1),
           ("Price non-win", 18, 1), ("App / payment friction", 13, 4), ("Assortment / coverage", 8, 2),
           ("Support recovered well", 7, 1), ("Reliable experience praised", 7, 0)]
    fam.sort(key=lambda x: x[1])
    labels = [f[0] for f in fam]
    sev = [f[2] for f in fam]
    low = [f[1] - f[2] for f in fam]
    fig, ax = plt.subplots(figsize=(9, 4.6), dpi=200)
    y = range(len(fam))
    ax.barh(y, sev, color=BLUE_DARK, height=0.62, label="Severity 3–4 (failed order, money at risk, safety)", edgecolor=SURFACE, linewidth=2)
    ax.barh(y, low, left=sev, color=BLUE_LIGHT, height=0.62, label="Lower severity / not rated", edgecolor=SURFACE, linewidth=2)
    for i, f in enumerate(fam):
        ax.text(f[1] + 0.8, i, str(f[1]), va="center", color=INK2, fontsize=9)
    ax.set_yticks(list(y))
    ax.set_yticklabels(labels, fontsize=10)
    ax.xaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.set_xlabel("Incidents (n = 108 first-hand Ownly experiences; a post can fall in several families)", fontsize=9, color=MUTED)
    ax.legend(loc="lower right", frameon=False, fontsize=8.5, labelcolor=INK2)
    ax.set_title("In public posts, failures after ordering outnumber price wins", loc="left", fontsize=13, color=INK, pad=12)
    fig.text(0.01, 0.005, "Source: Reddit/LinkedIn/X, Bengaluru, Jan–Sep 2026; AI first-pass coding, human validation pending. Self-selected — not prevalence.", fontsize=7.5, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    p = os.path.join(CH, "social_theme_families.png")
    fig.savefig(p)
    plt.close(fig)
    return p


def chart_appstore_themes():
    # Source: 05_review_mining/app_stores/analysis_tables.md (n = 37 reviews; a review can carry several themes)
    th = [("Support unresponsive / scripted", 21), ("Refund delayed or denied", 16), ("Cancelled by platform/restaurant", 11),
          ("Late delivery", 10), ("Rider conduct / unreachable", 9), ("Trust loss / 'scam' framing", 8),
          ("Not delivered / falsely delivered", 7), ("Lower price / value (positive)", 4), ("No hidden fees (positive)", 3)]
    th.sort(key=lambda x: x[1])
    fig, ax = plt.subplots(figsize=(9, 4.6), dpi=200)
    y = range(len(th))
    ax.barh(y, [t[1] for t in th], color=BLUE, height=0.62)
    for i, t in enumerate(th):
        ax.text(t[1] + 0.3, i, str(t[1]), va="center", color=INK2, fontsize=9)
    ax.set_yticks(list(y))
    ax.set_yticklabels([t[0] for t in th], fontsize=10)
    ax.xaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
    ax.set_xlabel("Reviews mentioning the theme (n = 37 visible Play Store + App Store reviews)", fontsize=9, color=MUTED)
    ax.set_title("App reviews point the same way: support and refunds dominate complaints", loc="left", fontsize=13, color=INK, pad=12)
    fig.text(0.01, 0.005, "Listing averages are 4.48 stars (Play, 44,485 ratings) and 4.5 stars (iOS, 10,466); visible reviews skew negative. Not prevalence.", fontsize=7.5, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    p = os.path.join(CH, "appstore_themes.png")
    fig.savefig(p)
    plt.close(fig)
    return p


# ---------------- deck helpers ----------------
prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]
DARK = RGBColor(0x0b, 0x0b, 0x0b)
GREY = RGBColor(0x52, 0x51, 0x4e)
ACCENT = RGBColor(0x1c, 0x5c, 0xab)
AMBER = RGBColor(0x9a, 0x5b, 0x00)


def textbox(slide, x, y, w, h, text, size=14, bold=False, color=DARK, align=PP_ALIGN.LEFT):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    lines = text if isinstance(text, list) else [text]
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.alignment = align
        p.font.size = Pt(size)
        p.font.name = "Arial"
        p.font.bold = bold
        p.font.color.rgb = color
        p.space_after = Pt(6)
    return tb


def header(slide, title, kicker=None, draft=True):
    if kicker:
        textbox(slide, 0.6, 0.35, 12, 0.4, kicker.upper(), 11, True, ACCENT)
    textbox(slide, 0.6, 0.65, 12.1, 1.0, title, 26, True)
    if draft:
        textbox(slide, 10.4, 7.0, 2.8, 0.35, "DRAFT — 14 Sep 2026", 9, False, GREY, PP_ALIGN.RIGHT)


def table(slide, x, y, w, rows, col_w=None, size=11):
    nr, nc = len(rows), len(rows[0])
    shp = slide.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(w), Inches(0.4 * nr))
    t = shp.table
    for j in range(nc):
        if col_w:
            t.columns[j].width = Inches(col_w[j])
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            c = t.cell(i, j)
            c.text = str(v)
            for p in c.text_frame.paragraphs:
                p.font.size = Pt(size)
                p.font.name = "Arial"
                p.font.bold = (i == 0)
                p.font.color.rgb = DARK
    return t


def placeholder(slide, y, lines):
    box = slide.shapes.add_shape(1, Inches(0.6), Inches(y), Inches(12.1), Inches(0.45 + 0.34 * len(lines)))
    box.fill.solid()
    box.fill.fore_color.rgb = RGBColor(0xfd, 0xf6, 0xe7)
    box.line.color.rgb = RGBColor(0xe0, 0xb8, 0x6a)
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "TO FILL AFTER DATA COLLECTION (15–16 Sep) — do not present until real numbers are in"
    p.font.size = Pt(12)
    p.font.name = "Arial"
    p.font.bold = True
    p.font.color.rgb = AMBER
    for l in lines:
        q = tf.add_paragraph()
        q.text = "• " + l
        q.font.size = Pt(12)
        q.font.name = "Arial"
        q.font.color.rgb = DARK


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


# ---------------- slides ----------------
# 1
s = prs.slides.add_slide(BLANK)
textbox(s, 0.8, 2.0, 11.5, 1.5, "Does Ownly's Bengaluru proposition transfer to Gachibowli?", 34, True)
textbox(s, 0.8, 3.4, 11.5, 1.2, ["Early market-fit validation among 20–30-year-old students and working professionals",
                                  "[Team names] · [Course] · 17 September 2026"], 16, False, GREY)
textbox(s, 0.8, 5.4, 11.5, 0.8, "One-line answer: [TO FILL on 17 Sep — SCALE / ADAPT / TARGET SELECTIVELY, with confidence level]", 14, True, AMBER)

# 2
s = prs.slides.add_slide(BLANK)
header(s, "A proposition that works in one city is not proof it works in the next", "Why this question")
textbox(s, 0.6, 1.8, 6.0, 4.8, [
    "Starbucks Australia (analogy only): it closed about three-quarters of its Australian stores in 2008 after overestimating its differentiation and expanding too fast into an established local coffee culture (Patterson, Scott & Uncles, 2010).",
    "Ownly (Rapido's food-delivery app) grew fast in Bengaluru with a zero-commission, low-fee proposition, and now says it is live in Hyderabad.",
    "Our question: are the conditions behind Bengaluru's traction present in Gachibowli — for whom, and at what trade-offs?"], 15)
table(s, 7.0, 1.9, 5.7, [["Decision options"], ["SCALE — proposition transfers as is"], ["ADAPT — need exists, but price or experience must change"],
                        ["TARGET SELECTIVELY — works for one segment"], ["RETHINK — need or switching potential absent"]], [5.7], 13)
notes(s, "Starbucks Australia lesson sourced in 01_secondary_research/secondary_research_report.md §12. Use as analogy only.")

# 3
s = prs.slides.add_slide(BLANK)
header(s, "Several widely repeated Ownly 'facts' are unverified or contradicted", "What is claimed vs what is verified")
table(s, 0.6, 1.7, 12.1, [
    ["Claim", "What we found", "Evidence label"],
    ["50,000 orders/day, ~10% Bengaluru share", "Traces to a single upstream media report copied by others", "MEDIA REPORT (single source)"],
    ["₹30 flat delivery fee", "Contradicted: App Store says 'Free delivery'; users report ₹0/₹15; a blog says distance-based", "CONTESTED"],
    ["~15% cheaper than Swiggy/Zomato", "Pilot-era (Aug 2025) positioning, not a measured saving", "COMPANY CLAIM"],
    ["20,000 / 22,000 / 25,000 restaurants", "Sources disagree; the company's own site says 22,000", "COMPANY CLAIM / MEDIA"],
    ["Ownly is live in Hyderabad", "Ownly's site says so; no dated independent report; posts suggest launch late Aug – ~11 Sep 2026", "COMPANY CLAIM + INTERPRETATION"],
    ["Incumbent fees", "Platform fee ₹17.58 incl. GST (Swiggy & Zomato, national, Mar 2026); 18% GST on delivery", "MEDIA REPORT (national, not Hyderabad)"],
    ["New affordability rival", "Swiggy's budget app Toing targets students/young professionals; Hyderabad availability unknown", "MEDIA REPORT"],
], [3.3, 6.2, 2.6], 11)
notes(s, "Full evidence table with URLs and dates: 01_secondary_research/evidence_table.csv (68 claims).")

# 3b — segments
s = prs.slides.add_slide(BLANK)
header(s, "Ownly pitches local eateries and first-time online orderers, but showcases popular regional chains", "Who Ownly targets (secondary research)")
table(s, 0.6, 1.65, 6.0, [
    ["Restaurants", "Evidence (label)"],
    ["Stated target: local/regional eateries incumbents 'aren't built for'", "CEO interview, Jul 2026 (COMPANY CLAIM, verified)"],
    ["~70,000 unlisted Bengaluru outlets: thaali places, tiffin centres, dhabas; 15% of onboarded were new to delivery", "Inc42, 25 Mar 2026 (MEDIA REPORT, verified)"],
    ["Pilot rules: ≥4 'Meals for One' under ₹150; dine-in prices; no packaging fee", "Storyboard18, Aug 2025 (MEDIA REPORT, verified)"],
    ["Showcase partners are well-known regional chains: Empire, Vidyarthi Bhavan (BLR); Paradise, Bawarchi, Cream Stone (HYD)", "Press release; ownly.food/hyd (COMPANY CLAIM)"],
    ["KFC & McDonald's (via magicpin) went offline in May 2026", "Financial Express (MEDIA REPORT, snippet)"],
], [3.4, 2.6], 10)
table(s, 6.9, 1.65, 5.8, [
    ["Customers", "Evidence (label)"],
    ["Price-sensitive diners; 'affordability is the biggest deterrent'", "CEO interview (COMPANY CLAIM, verified)"],
    ["Rapido riders who have never ordered food online; goal of 100M online orderers", "Company statements (COMPANY CLAIM)"],
    ["Everyday low prices, not coupons; 'pay for Food + Delivery'", "Launch coverage, Instagram (COMPANY CLAIM)"],
    ["No stated age or occupation target; no data on actual users", "UNKNOWN"],
    ["Analysts group budget apps with 'students and younger users'; say Toing leads", "JP Morgan via Storyboard18 (MEDIA REPORT, no metrics)"],
], [3.2, 2.6], 10)
textbox(s, 0.6, 6.05, 12.1, 0.9, ["So what (INTERPRETATION): our 20–30 Gachibowli users fit Ownly's price point, but most already use Swiggy/Zomato. For Ownly they are a switching segment, not the first-time orderers it says it is chasing. The audit therefore samples showcase chains, local budget eateries and national QSRs."], 12, False, GREY)
notes(s, "Sources and verification status: 01_secondary_research/ownly_restaurant_and_user_segments.md and ownly_segments_evidence.csv.")

# 4
s = prs.slides.add_slide(BLANK)
header(s, "What we could collect in 3 days, ethically, with ₹900", "Method")
table(s, 0.6, 1.7, 12.1, [
    ["Evidence", "Size", "What it answers", "Limits"],
    ["Secondary research", "68 sourced claims", "Claims vs facts; market context", "Mostly national/Bengaluru"],
    ["Public customer voice (app stores, Reddit, LinkedIn, X)", "37 reviews + 524 posts (108 first-hand)", "Bengaluru benchmark: what drives use and churn", "Self-selected; not prevalence"],
    ["Competitor price audit, Gachibowli", "[n] captures, [n] matched comparisons", "Is Ownly actually cheaper at checkout, after coupons?", "Team accounts; 3 slots"],
    ["Test orders", "3 orders (₹900)", "Promised vs actual delivery time, fees charged", "Anecdotal"],
    ["Short survey (7 min)", "[n] valid, 20–30, Gachibowli area", "Fee pain, switching threshold, trade-offs, Ownly funnel", "Convenience sample"],
    ["Short interviews", "[n] (students / professionals)", "Why behind the numbers", "Not prevalence"],
], [3.6, 2.9, 3.5, 2.1], 11)
textbox(s, 0.6, 5.7, 12.1, 1.2, ["All activities approved by [instructor] on [date]. No incentives, no deception, no personal identifiers stored.",
                                  "Dropped for time/ethics: Bengaluru survey, fake-door landing page, full choice experiment (designs retained as next-phase appendix)."], 12, False, GREY)

# 5
s = prs.slides.add_slide(BLANK)
header(s, "Bengaluru benchmark: price attracts, but failures after ordering drive the loudest complaints", "Public customer voice")
s.shapes.add_picture(chart_social_families(), Inches(0.5), Inches(1.65), width=Inches(7.4))
textbox(s, 8.1, 1.8, 4.7, 5.0, [
    "Price is praised before ordering; harm happens after dispatch (non-delivery, rider issues, support).",
    "Savings are contested: all 6 user-posted bill comparisons favour Ownly, but 18 posts say coupons/card offers erased the gap.",
    "37 posts expect prices or fees to rise later ('enjoy while it lasts').",
    "Payment gaps noticed: no cash on delivery, no meal cards (Pluxee).",
    "Label: CONSUMER-GENERATED signals — they tell us what to measure, not how common it is."], 13)

# 6
s = prs.slides.add_slide(BLANK)
header(s, "App-store reviews independently show the same failure pattern", "Public customer voice")
s.shapes.add_picture(chart_appstore_themes(), Inches(0.5), Inches(1.65), width=Inches(7.4))
textbox(s, 8.1, 1.8, 4.7, 5.0, [
    "Two independent public sources converge: support, refunds, cancellations and lateness.",
    "Positive reviews praise price and 'no hidden fees'.",
    "Caution: only 37 reviews were accessible within the stores' crawling rules, and they skew negative versus the 4.5★ averages.",
    "Implication to test in Gachibowli: does reliability outweigh a ₹30 saving? (slide 9)"], 13)

# 7
s = prs.slides.add_slide(BLANK)
header(s, "[Insight title after audit] — Is Ownly cheaper at checkout in Gachibowli?", "Market reality: competitor price audit")
placeholder(s, 1.8, ["Price per basket (median final payable) per app — from audit_report.md",
                     "Median gap Ownly − Swiggy and Ownly − Zomato with 95% CI: (a) without coupons, (b) after coupons",
                     "Win rate (Ownly cheapest, tie ≤ ₹5) and fee share of bill per app",
                     "Coverage: share of 10 popular restaurants listed & open on Ownly; ETA gap (minutes)",
                     "Test orders: promised vs actual delivery time; fee actually charged (n = 3, anecdotal)",
                     "Chart: dot-plot of gaps per restaurant with median line; title states the finding only if CI excludes 0"])

# 8
s = prs.slides.add_slide(BLANK)
header(s, "[Insight title after survey] — How painful are fees, and what saving makes people switch?", "Gachibowli survey")
placeholder(s, 1.8, ["Price Pain Index median (0–100) with CI; % whose checkout charges made them reconsider (H1.1); cart abandonment (H1.4)",
                     "Top-3 frustrations: price/fee vs late/cancel (H1.2) — sorted bar with n",
                     "Required saving to switch (median ₹) vs audit median saving (H2.3) — the key economic test",
                     "Transparency: simple vs itemised bill at equal ₹245 (H2.2)",
                     "Students vs working professionals side by side (only if each n ≥ 20; else note 'directional')"])

# 9
s = prs.slides.add_slide(BLANK)
header(s, "[Insight title after survey] — What will people give up for ₹30 less?", "Trade-offs")
placeholder(s, 1.8, ["% choosing ₹30 cheaper but 15 min slower (H3)",
                     "% choosing ₹30 cheaper but late 3 in 10 vs 1 in 10 (H4)",
                     "% choosing ₹30 cheaper but only a few usual restaurants (H5)",
                     "Rule: '₹30 buys the compromise' only if the CI lower bound > 50% (stated, hypothetical preference)",
                     "Max acceptable dinner ETA (median); delivery-fee acceptance curve from the max-fee question (H8)"])

# 10
s = prs.slides.add_slide(BLANK)
header(s, "[Insight title after survey] — Ownly's early funnel in Gachibowli", "Adoption & course KPIs")
placeholder(s, 1.8, ["Aided awareness → tried → repeat (≥2 orders in 4 weeks) with n at each step; aware→tried conversion (say–do gap)",
                     "Penetration share = tried ÷ delivery users; brand development index students vs professionals",
                     "Share of requirements & heavy-usage index → market-share decomposition (only if ≥10 Ownly triers)",
                     "Trial intent before vs after revealing 'Ownly by Rapido' (brand effect, within-subject)",
                     "Top reasons for not trying (incl. payment method not accepted)"])

# 11
s = prs.slides.add_slide(BLANK)
header(s, "Bengaluru assumption → Gachibowli evidence → does it transfer?", "Market-transfer test")
table(s, 0.6, 1.7, 12.1, [
    ["Bengaluru assumption", "Bengaluru evidence (public, labelled)", "Gachibowli evidence", "Verdict"],
    ["Lower total price triggers trial", "6/6 user bill comparisons favour Ownly; 18 posts report no win after coupons (CONSUMER-GENERATED)", "[Audit gap after coupons; required saving]", "[TRANSFERABLE / ADAPT / NOT / UNKNOWN]"],
    ["Delivery fee is acceptable", "Fee contested (₹0 / ₹15 / ₹30)", "[Observed fee; % accepting that fee]", "[ ]"],
    ["Reliability good enough to repeat", "46 fulfilment + 29 support/refund failures in first-hand posts", "[Trade-off H4; test orders; Ownly users' on-time rating]", "[ ]"],
    ["Restaurant coverage sufficient", "'Limited restaurants' 8 incidents", "[Audit coverage; % needing most usual restaurants]", "[ ]"],
    ["Rapido brand builds trust", "Two-sided mentions", "[Intent before vs after reveal]", "[ ]"],
    ["Users switch easily (multi-home)", "'Just keep switching' posts; coupons pull users back", "[% using ≥2 apps; memberships]", "[ ]"],
], [2.6, 3.9, 3.6, 2.0], 11)
textbox(s, 0.6, 6.4, 12, 0.5, "Verdict rules (pre-registered): TRANSFERABLE = need present and not weaker; ADAPT = need present but a condition is worse; NOT = need absent; UNKNOWN = not enough data.", 11, False, GREY)

# 12
s = prs.slides.add_slide(BLANK)
header(s, "Recommendation", "Decision")
textbox(s, 0.6, 1.7, 12, 0.6, "Working position going into data collection (HYPOTHESIS, to be confirmed or rejected by slides 7–11):", 14, True, AMBER)
textbox(s, 0.6, 2.3, 12, 2.0, [
    "ADAPT rather than copy Bengaluru: lead with a fair total price you can rely on, not 'cheapest'.",
    "Guardrail before scaling: support and refund resolution; delivery-time parity at dinner peak.",
    "Start with small, frequent solo orders from students and young professionals; add payment options (COD / meal cards).",
    "Don't compete on coupons against Swiggy/Zomato."], 15)
placeholder(s, 4.6, ["Final recommendation (SCALE / ADAPT / TARGET SELECTIVELY / RETHINK) with confidence level and the evidence that decided it",
                     "What would change our mind; next experiment (the full 5-week design in the appendix)"])

# 13 limitations
s = prs.slides.add_slide(BLANK)
header(s, "Limitations and next research", "Honesty slide")
textbox(s, 0.6, 1.8, 12, 5, [
    "3-day window, convenience sample around Gachibowli — results describe our respondents, not Hyderabad.",
    "No Bengaluru survey: the Bengaluru benchmark relies on self-selected public posts and reviews.",
    "Survey trade-offs and intent are stated preferences; the price audit reflects the team's own accounts and 3 time slots.",
    "Scenario KPIs (growth rate, contribution per order, CLV) use media figures and assumptions, not company data.",
    "Next phase (designed, in appendix): 220-person Hyderabad survey with a choice experiment and randomised brand test; 150-person Bengaluru Ownly-user survey; 2-week audit; 16 interviews; value-proposition landing-page test."], 15)

# 14 appendix: scenario KPIs
s = prs.slides.add_slide(BLANK)
header(s, "Appendix: course KPIs we can compute now (scenarios, clearly labelled)", "Appendix A")
table(s, 0.6, 1.7, 12.1, [
    ["KPI (course formula)", "Calculation", "Result", "Label"],
    ["Compound monthly growth (CAGR)", "(50,000 ÷ 5,000)^(1/5) − 1, Bengaluru daily orders Mar→Aug 2026", "≈ 58.5% per month", "MEDIA REPORT inputs"],
    ["Contribution per order", "Delivery fee − rider payout − ₹5 other; fee ₹0–30 vs payout ₹30–60", "−₹65 to −₹5 per order (positive only if payout < fee − ₹5)", "ASSUMPTION scenario"],
    ["Break-even volume", "Fixed costs ÷ contribution per order", "Not reachable while contribution ≤ 0", "ASSUMPTION scenario"],
    ["Customer lifetime value", "Margin × r ÷ (1 + d − r), d = 1%/month", "₹50 margin: ₹73 at 60% retention vs ₹409 at 90%", "ASSUMPTION scenario"],
], [2.8, 4.9, 2.6, 1.8], 11)
textbox(s, 0.6, 5.0, 12, 1.5, ["Takeaway (INTERPRETATION): retention multiplies value far more than margin, so reliability that keeps users is worth more than deeper discounts.",
                                "Full working: 09_analysis/short_plan/scenario_kpis.md"], 13, False, GREY)

# 15 appendix: CSV toolkit
s = prs.slides.add_slide(BLANK)
header(s, "Appendix: digital-funnel KPIs (practice dataset, not Ownly data)", "Appendix B")
textbox(s, 0.6, 1.7, 12, 2.2, [
    "Marketing Metrics 1000 Records.csv: generic 2024–25 USD campaign data (8 channels). Formulas check out (CTR, conversion rate, ROAS, CPA reproduce in 1000/1000 rows).",
    "Data-quality flag: conversions exceed qualified leads in 325/1000 rows; near-identical ROAS across channels suggests synthetic data.",
    "How these KPIs would apply to Ownly's Gachibowli launch: CTR and conversion rate of launch ads; CPA (= average acquisition cost) compared with CLV (Appendix A).",
    "Applied to our own survey recruitment: completes ÷ starts by channel; cost per valid response = ₹0."], 13)

out = os.path.join(HERE, "Ownly_Gachibowli_deck_DRAFT.pptx")
prs.save(out)
print("saved", out)
