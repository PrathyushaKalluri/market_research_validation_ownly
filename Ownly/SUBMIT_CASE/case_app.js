/* ═══════════════════════════════════════════════════════════════════
   Ownly case-study dashboard.
   Five sections: the case, KPIs, marketing metrics, analysis, solutions.
   Every case-study claim is tested against data here.
   ═══════════════════════════════════════════════════════════════════ */
(function () {
"use strict";
var S = window.CS, V = window.VZ, C = V.C;
var BLR = "#eb6834", HYD = "#2a78d6";
function T(n) { return S[n] || []; }
function num(v) { return (v === null || v === undefined || isNaN(v)) ? null : +v; }
function uniq(rows, k) { var o = []; rows.forEach(function (r) { if (o.indexOf(r[k]) < 0) o.push(r[k]); }); return o; }
function by(rows, k) { var m = {}; rows.forEach(function (r) { (m[r[k]] = m[r[k]] || []).push(r); }); return m; }
function pick(rows, k, v) { return rows.filter(function (r) { return r[k] === v; }); }

var OUT = [];
function sec(id, n, title, lede) {
  OUT.push('<section class="sec" id="' + id + '"><div class="eyebrow">' + n + '</div><h2>' +
    V.esc(title) + '</h2>' + (lede ? '<p class="lede prose">' + lede + '</p>' : '') + '<div class="grid">');
}
function endsec() { OUT.push('</div></section>'); }
function bT() { return '<span class="badge b-tab">Tableau</span>'; }
function bP() { return '<span class="badge b-py">Python only</span>'; }
function card(cls, title, badge, sub, body, note) {
  OUT.push('<section class="card ' + (cls || '') + '"><div class="hd"><h3>' + V.esc(title) + '</h3>' +
    (badge || '') + '</div>' + (sub ? '<p class="sub">' + sub + '</p>' : '') + body +
    (note ? '<div class="note">' + note + '</div>' : '') + '</section>');
}
function legend(items) {
  return '<div class="legend">' + items.map(function (i) {
    return '<span><i class="sw" style="background:' + i.color + '"></i>' + V.esc(i.name) + '</span>';
  }).join('') + '</div>';
}
function tbl(cols, rows) {
  return '<div class="tw"><table><thead><tr>' +
    cols.map(function (c) { return '<th class="' + (c.n ? 'n' : '') + '">' + V.esc(c.label) + '</th>'; }).join('') +
    '</tr></thead><tbody>' + rows.map(function (r) {
      return '<tr>' + cols.map(function (c) {
        var v = c.get(r);
        return '<td class="' + (c.n ? 'n' : '') + '">' + (v === null || v === undefined || v === '' ? '—' : v) + '</td>';
      }).join('') + '</tr>';
    }).join('') + '</tbody></table></div>';
}

/* ─── helpers to read the KPI table ─── */
var KP = {}; T("16_kpis").forEach(function (r) { KP[r.KPI] = r; });
function kv(name) { var r = KP[name]; return r ? num(r.Value) : null; }

/* ══════════ TOP ══════════ */
document.getElementById("topstrip").innerHTML = [
  { v: "232", k: "posts in Swiggy/Zomato communities in Aug 2026 — the boycott month", s: "vs 0–7 in every prior month", color: BLR },
  { v: "1,000+", k: "Bengaluru restaurants threatened to delist", s: "up to 21,000 statewide expected", color: BLR },
  { v: "35%", k: "of Hyderabad will give up their usual restaurants for ₹30", s: "92.5% will give up speed", color: C.crit },
  { v: V.pct(kv("Catalogue overlap")), k: "of Ownly's restaurants are already on a rival", s: "+17 min slower" },
  { v: V.pct(kv("Membership lock-in")), k: "of Hyderabad already pay for a rival membership", s: "it cancels the saving" },
  { v: V.pct(kv("Trial rate")), k: "have ordered on Ownly in Gachibowli", s: "2 of 40 — directional only" },
].map(function (k) {
  return '<div class="kc"><span class="v"' + (k.color ? ' style="color:' + k.color + '"' : '') + '>' +
    V.esc(k.v) + '</span><span class="k">' + V.esc(k.k) + '</span><span class="s">' + V.esc(k.s) + '</span></div>';
}).join("");

/* ══════════════════ 1 · THE CASE ══════════════════ */
sec("s1", "Section 1", "The case",
  "Ownly grew fast in Bengaluru and is copying the playbook into Hyderabad. This section tests <i>why</i> " +
  "Bengaluru worked — because if the reason doesn't travel, neither does the playbook.");

OUT.push('<section class="card"><div class="callout key">' +
  '<p><b>The problem.</b> Ownly went from a three-area pilot (Aug 2025) to 50,000+ daily orders and ~10% of ' +
  'Bengaluru (Aug 2026). But in July 2026 <b>1,000+ Bengaluru restaurants threatened to quit Swiggy and Zomato</b> ' +
  'over commissions and arbitrary deductions, with up to 21,000 statewide expected to join. Ownly signed an ' +
  'agreement with the national restaurant association in that same window. <b>Restaurants were already looking ' +
  'for a way out — Ownly walked through a door someone else had opened.</b></p>' +
  '<p>Hyderabad has no such revolt. There, Ownly sells <b>89% the same restaurants, ~17 minutes slower</b>, into ' +
  'a market where <b>82.5% already pay for a rival membership</b> — and where the one thing people refuse to give ' +
  'up for ₹30 is <b>their usual restaurants</b>. The problem is not the price. It is a supply-side win being ' +
  'carried into a demand-side fight.</p></div></section>');

card("c7", "The conversation exploded in the boycott month", bT(),
  "Social posts per month by audience. The Aug 2026 spike is the restaurant revolt, visible in the communities of the apps being boycotted.",
  (function () {
    var rows = T("03_social_timeline_by_audience");
    var months = uniq(rows, "Month").sort();
    var auds = ["Bengaluru local", "Incumbent app community", "Professional / LinkedIn"];
    var cols = [BLR, C.s[7], C.s[4]];
    return V.lineChart({
      x: months.map(function (m) { return String(m).slice(2); }),
      series: auds.map(function (a, i) {
        return { name: a, color: cols[i], area: i === 1,
                 values: months.map(function (m) {
                   var f = rows.filter(function (r) { return r.Month === m && r.Audience === a; });
                   return f.length ? num(f[0].Documents) : 0;
                 }) };
      }), w: 620, h: 260, fmtTip: function (v) { return V.fmt(v, 0) + " posts"; }
    });
  })(),
  legend([{ name: "Bengaluru local subreddits", color: BLR }, { name: "r/Zomato + r/swiggy", color: C.s[7] }, { name: "LinkedIn", color: C.s[4] }]) +
  "<b>Read the orange line</b> · Bengaluru-local chatter starts at the <b>March 2026 citywide launch</b> and holds. " +
  "<b>Read the red area</b> · posts in the incumbent apps' own communities go from <b>0–7 a month to 232 in Aug 2026</b> — " +
  "the month of the 15 Aug delisting deadline. <b>Source</b> · 524 social posts, community field.");

card("c5", "What actually happened, month by month", bT(),
  "Ownly's moves and the restaurants' moves on one timeline.",
  '<div>' + T("01_bengaluru_event_register").map(function (e) {
    var cls = e.Actor === "Ownly" ? "own" : e.Actor === "Restaurants" ? "rest" : "";
    return '<div class="evt ' + cls + '"><span class="m">' + V.esc(e.Month) + '</span>' +
      '<span class="e"><b>' + V.esc(e.Event) + '</b><br>' + V.esc(e.Detail) + '</span></div>';
  }).join('') + '</div>',
  "<b>Blue = Ownly's move. Orange = restaurants' move.</b> All MEDIA REPORT grade. " +
  "<b>The last row matters</b> · no reporting was found after the 1 Sep 2026 deadline, so whether the boycott " +
  "executed, was called off, or was settled is <b>UNKNOWN</b>.");

card("c6", "What the restaurants were actually angry about", bT(),
  "The six demands, verbatim. Note that only one is about the commission rate.",
  tbl([
    { label: "Demand (verbatim)", get: function (r) { return V.esc(r["Demand (verbatim)"]); } },
    { label: "Grievance", get: function (r) { return '<span class="pill p-blr">' + V.esc(r["Grievance type"]) + "</span>"; } },
  ], T("02_boycott_demands")),
  "<b>This is why zero commission landed so well.</b> The complaints were about money being taken automatically, " +
  "discounts imposed without consent, and no itemised statement — and Ownly's offer (no commission, no ad fees, " +
  "no forced promotions) answered nearly all of them at once.");

card("c6", "Bengaluru vs Hyderabad — the same questions, two cities", bT(),
  "From our own survey: n = 16 in Bengaluru, n = 40 in the Gachibowli catchment.",
  (function () {
    var rows = T("09_city_comparison").filter(function (r) { return r.Metric !== "Median saving needed to switch (Rs)"; });
    var mets = uniq(rows, "Metric");
    return V.lollipop({
      data: mets.map(function (m) {
        var b = pick(rows, "Metric", m).filter(function (r) { return r.City === "Bengaluru"; })[0] || {};
        var h = pick(rows, "Metric", m).filter(function (r) { return String(r.City).indexOf("Gachibowli") === 0; })[0] || {};
        return { label: m, a: num(b.Value) || 0, b: num(h.Value) || 0,
                 vlabel: (num(h.Value) - num(b.Value) > 0 ? "+" : "") + V.fmt(num(h.Value) - num(b.Value), 0) + " pp" };
      }),
      w: 540, labelW: 235, nameA: "Bengaluru", nameB: "Gachibowli",
      colorA: BLR, colorB: HYD, max: 100, fmtAxis: function (t) { return V.fmt(t, 0) + "%"; }
    });
  })(),
  legend([{ name: "Bengaluru (n=16)", color: BLR }, { name: "Gachibowli (n=40)", color: HYD }]) +
  "<b>Awareness 75% → 42.5% and trial 25% → 5%</b> — expected, Ownly is weeks old in Hyderabad. " +
  "<b>Membership lock-in is identical (81% vs 82.5%)</b>, so that barrier travels. " +
  "<b>The Bengaluru switching bar is higher</b> (₹50 vs ₹30), which makes Hyderabad look <i>easier</i> on price — " +
  "and it still isn't working, which is the point.");
endsec();

/* ══════════════════ 2 · KPIs ══════════════════ */
sec("s2", "Section 2", "KPIs",
  "The numbers the case study rests on. Every proportion carries a 95% Wilson interval.");

card("c7", "Funnel and market conditions", bT(),
  "Share of the 40 Gachibowli respondents. Whiskers are 95% confidence intervals.",
  V.barH({
    data: ["Awareness", "Browse rate", "Trial rate", "Membership lock-in", "Multi-homing",
           "Rapido usage", "Rapido food discovery", "Price-durability doubt", "Post-offer repeat intent"]
      .map(function (k) {
        var r = KP[k]; if (!r) return null;
        return { label: k, value: num(r.Value), lo: num(r["CI low"]), hi: num(r["CI high"]),
                 vlabel: V.fmt(r.Value, 1) + "%",
                 color: (k === "Membership lock-in" || k === "Price-durability doubt") ? C.crit :
                        (k === "Multi-homing" ? C.s[2] : C.s[0]),
                 tip: k + "\n" + r["Question it answers"] + "\n" + r.Base + " = " + r.Value + "%\n95% CI " +
                      r["CI low"] + "–" + r["CI high"] + "\n\n" + r["Why it matters"] };
      }).filter(Boolean),
    max: 100, w: 620, rowH: 30, labelW: 200, fmtAxis: function (t) { return V.fmt(t, 0) + "%"; }
  }),
  legend([{ name: "Barrier", color: C.crit }, { name: "Opportunity", color: C.s[2] }, { name: "Funnel", color: C.s[0] }]) +
  "Hover any bar for the question it answers and why it matters. <b>Source</b> · Data/16_kpis.csv");

card("c5", "The adoption funnel", bT(),
  "Awareness → browse → order, in the catchment.",
  V.funnel({
    data: [["Awareness", "Heard of Ownly"], ["Browse rate", "Opened it"], ["Trial rate", "Ordered"]]
      .map(function (p) {
        var r = KP[p[0]];
        return { label: p[1], value: num(r.Value), k: parseInt(String(r.Base).split(" ")[0], 10), n: 40 };
      }), w: 460
  }),
  "<b>The last step is 2 people.</b> Interval 1.4–16.5%. The 4-week window also mostly predates Ownly's " +
  "Hyderabad rollout, so a low number here measures the question window as much as rejection.");

card("c6", "Supply and service KPIs", bT(),
  "From the price audit, not the survey.",
  tbl([
    { label: "KPI", get: function (r) { return "<b>" + V.esc(r.KPI) + "</b>"; } },
    { label: "Answers", get: function (r) { return V.esc(r["Question it answers"]); } },
    { label: "Value", n: 1, get: function (r) { return "<b>" + V.fmt(r.Value, 1) + " " + V.esc(r.Unit) + "</b>"; } },
    { label: "Base", get: function (r) { return V.esc(r.Base); } },
    { label: "Why it matters", get: function (r) { return V.esc(r["Why it matters"]); } },
  ], T("16_kpis").filter(function (r) { return r.Source === "Audit"; })),
  "");

card("c6", "The switching bar vs what Ownly delivers", bT(),
  "People said they need a median ₹30 saving every time. Ownly delivers ₹114.50 on list price.",
  V.bullet({ label: "Median saving delivered (list price + fees)", value: 114.5, max: 140, target: 30,
             color: C.s[2], vlabel: "₹114.50", w: 520,
             bands: [{ from: 0, to: 30, color: C.crit }] }) +
  V.bullet({ label: "Median saving once a rival membership applies", value: 77.59, max: 140, target: 30,
             color: C.s[2], vlabel: "₹77.59", w: 520,
             bands: [{ from: 0, to: 30, color: C.crit }] }) +
  V.bullet({ label: "Median saving after one rival coupon", value: 0, max: 140, target: 30,
             color: C.crit, vlabel: "−₹28.07", w: 520,
             bands: [{ from: 0, to: 30, color: C.crit }] }),
  "<b>Black line = ₹30</b>, the bar people said they need. <b>Red band = below the bar.</b> " +
  "After a routine rival coupon the saving goes <b>negative</b> — Ownly becomes the more expensive app.");
endsec();

/* ══════════════════ 3 · MARKETING METRICS ══════════════════ */
sec("s3", "Section 3", "Marketing metrics",
  "Ten metrics computed from our own evidence, and ten more we refused to invent.");

card("c7", "Computed metrics", bT(),
  "Three are definitions we built ourselves, because the standard formula sheet has no metric for the question at issue.",
  V.barH({
    data: T("17_marketing_metrics").map(function (r) {
      return { label: r.ID + " · " + r.Metric, value: num(r.Value),
               vlabel: V.fmt(r.Value, 1) + (r.Unit === "%" ? "%" : " " + (r.Unit || "")),
               color: r["Our own definition"] === "Yes" ? C.s[1] : C.s[0],
               tip: r.Metric + "\n" + r.Value + " " + (r.Unit || "") + "\n\n" + (r.Formula || "") +
                    "\n\nCaveat: " + (r.Caveat || "—") };
    }), w: 600, rowH: 29, labelW: 258, fmtAxis: function (t) { return V.fmt(t, 0); }
  }),
  legend([{ name: "Our own definition", color: C.s[1] }, { name: "Standard formula sheet", color: C.s[0] }]) +
  "<b>Switch-Threshold Coverage (MM1)</b> is the central one: it asks “is the saving big enough <i>for these " +
  "particular people</i>”, not merely “is Ownly cheaper”. Hover any bar for its formula and caveat.");

card("c5", "Marked NOT ESTIMABLE", bT(),
  "Each needs Ownly's or Rapido's internal data. None is guessed.",
  tbl([
    { label: "Metric", get: function (r) { return "<b>" + V.esc(r.Metric) + "</b>"; } },
    { label: "Why not computable", get: function (r) { return V.esc(r["Why not computable"]); } },
  ], T("18_not_estimable")),
  "<b>The finding inside the gap</b> · retention, CLV, CAC and contribution margin are exactly the metrics " +
  "that decide whether Ownly survives — and no external researcher can see any of them.");
endsec();

/* ══════════════════ 4 · ANALYSIS ══════════════════ */
sec("s4", "Section 4", "Analysis",
  "Each claim in the case study, tested. Sentiment and topic modelling are marked " +
  "<span class='badge b-py'>Python only</span> because Tableau cannot compute them — it can draw them once " +
  "the values exist as columns.");

/* — claim register — */
card("", "Claim check — does the case study survive its own data?", bT(),
  "Every substantive claim, its evidence, and whether it holds.",
  (function () {
    var claims = [
      ["Bengaluru restaurants were in open revolt in mid-2026", "HOLDS",
       "1,000+ restaurants threatened delisting from 15 Aug 2026; up to 21,000 statewide expected. Six documented demands.",
       "Media reports, Jul–Aug 2026 (Business Today, Storyboard18, Inc42, News18)"],
      ["The revolt coincided with Ownly's scale-up", "HOLDS",
       "Ownly signed the NRAI MoU in Aug 2026, went live in the main Rapido app in Jul 2026, and moved from 40,000 to 50,000+ daily orders across Jul–Aug 2026.",
       "Ownly event register"],
      ["The conversation spiked in that month", "HOLDS",
       "Posts in r/Zomato and r/swiggy went from 0–7 a month to 232 in Aug 2026 — a 33× jump on the prior peak.",
       "524 social posts, community + date fields"],
      ["…but the spike was volume, not anger, among consumers", "IMPORTANT NUANCE",
       "Mean sentiment barely moves by audience: Bengaluru local −0.03, incumbent communities −0.02. The revolt was a restaurant-side event; consumer tone did not shift with it.",
       "Sentiment model over 836 documents"],
      ["Hyderabad has no equivalent revolt", "NOT DISPROVEN — but this is an absence of evidence",
       "No comparable Hyderabad restaurant action was found in the secondary research, and only 4 of 524 social posts mention Hyderabad at all. Absence of reporting is not proof of absence.",
       "Secondary research + social city field"],
      ["Hyderabad users won't give up their restaurants for ₹30", "HOLDS — strongly",
       "92.5% would wait 15 min longer and 72.5% would accept a late order, but only 35% would give up their usual restaurants. 24 people accepted a delay but refused to lose restaurants; exactly 1 did the opposite.",
       "Survey n=40, paired design, McNemar exact p = 1.5×10⁻⁶"],
      ["Ownly sells the same restaurants, slower", "HOLDS",
       "88.9% of Ownly's audited restaurants are also on a rival. Quoted ETA gap +17 min, flat across all four restaurants.",
       "Price audit, 10-restaurant frame"],
      ["The saving is real but invisible to most", "HOLDS",
       "Cheapest in 4 of 4 baskets, median saving ₹114.50, fee load 4.8% vs 23%. But 82.5% hold a membership, and after one rival coupon the median saving is −₹28.07.",
       "Price audit × survey"],
      ["Rapido is not bringing people in", "HOLDS",
       "60% use Rapido, but only 5 of 33 answering had noticed food inside it. Rapido users were also less aware of Ownly than non-users (33% vs 56%), though that difference is not statistically established.",
       "Survey n=40"],
      ["People leave after repeated failures, not price", "SUPPORTED, NOT PROVEN",
       "App-store reviews: 72% mention a failed delivery, 79% support or refunds. First-hand social posts mention failure 49.5% of the time vs 18.9% in general discussion. The mechanism comes from interviews, which carry no prevalence figure.",
       "37 reviews, 524 social posts, 1 documented interview"],
    ];
    return claims.map(function (c) {
      var cls = c[1].indexOf("HOLDS") === 0 ? "" : (c[1].indexOf("NOT DISPROVEN") === 0 || c[1].indexOf("SUPPORTED") === 0 ? "partial" : "partial");
      var pill = c[1].indexOf("HOLDS") === 0 ? "p-ok" : "p-warn";
      return '<div class="claim ' + cls + '"><div class="ch"><span class="ct">' + V.esc(c[0]) +
        '</span><span class="pill ' + pill + '">' + V.esc(c[1]) + '</span></div>' +
        '<div class="ce">' + V.esc(c[2]) + '</div><div class="cs">evidence · ' + V.esc(c[3]) + '</div></div>';
    }).join("");
  })(),
  "<b>Two claims are deliberately not marked as proven.</b> That Hyderabad has no restaurant revolt is an " +
  "<i>absence of reporting</i>, not a verified fact. And the retention mechanism rests on one documented " +
  "interview, so it is supported by convergence rather than measured.");

/* — the ₹30 trade-off — */
card("c7", "The ₹30 trade-off — the finding the whole case rests on", bT(),
  "Same ₹30 saving offered three times; only the thing given up changed. Same 40 people each time.",
  V.barH({
    data: T("10_tradeoff").sort(function (a, b) { return a["Sort order"] - b["Sort order"]; })
      .map(function (r) {
        return { label: r["Give up"], value: num(r["Accept %"]), lo: num(r["CI low"]), hi: num(r["CI high"]),
                 vlabel: V.fmt(r["Accept %"], 1) + "%",
                 color: r["Is the constraint"] === "Yes" ? BLR : C.s[0],
                 tip: r["Give up"] + "\n" + r.Accepted + " of " + r.Base + " accepted ₹30\n95% CI " +
                      r["CI low"] + "–" + r["CI high"] + "\n" + r["Refused %"] + "% refused" };
      }),
    max: 100, ref: 50, w: 620, rowH: 44, labelW: 230, fmtAxis: function (t) { return V.fmt(t, 0) + "%"; }
  }),
  "<b>Dashed line is a coin flip.</b> Only the restaurants row falls below it. " +
  "<b>McNemar exact test, paired: p = 1.5 × 10⁻⁶.</b> 24 people accepted a delay but refused to lose their " +
  "restaurants; exactly 1 did the reverse. A split that lopsided happens by chance about once in 670,000 times.");

card("c5", "Where the price advantage goes", bT(),
  "Share of person × restaurant pairs where the saving clears that person's own stated bar.",
  V.waterfall({
    data: [{ label: "List price", value: 81.1 }, { label: "Membership effect", value: -25.0 },
           { label: "Coupon effect", value: -28.8 }, { label: "After coupon", total: true }],
    w: 420, h: 270, fmtAxis: function (t) { return V.fmt(t, 0) + "%"; }
  }),
  "<b>81% → 56% → 27%.</b> The advantage Ownly controls is real; the one customers experience often isn't.");

card("c6", "Same food, three apps, same 20 minutes", bT(),
  "Matched baskets at one Gachibowli address, 16 Sep 2026, before any coupon.",
  (function () {
    var rows = T("11_price_audit");
    return V.barGrouped({
      cats: rows.map(function (r) { return r.Restaurant; }),
      series: [
        { name: "Ownly", color: C.s[2], values: rows.map(function (r) { return num(r["Ownly payable"]); }) },
        { name: "Cheapest rival", color: BLR, values: rows.map(function (r) { return num(r["Cheapest rival payable"]); }) },
      ], w: 520, h: 250
    });
  })(),
  legend([{ name: "Ownly", color: C.s[2] }, { name: "Cheapest rival", color: BLR }]) +
  "<b>Cheapest in 4 of 4.</b> But note the ETA column in the data: Ownly is slower on every one. " +
  "<b>Limitation</b> · n = 4 baskets, one address, one slot.");

card("c6", "Why the saving exists: fees, not food", bT(),
  "Non-food charges as a share of the bill, zero-discount captures only.",
  V.barH({
    data: T("13_fee_load").map(function (r) {
      return { label: r.Platform, value: num(r["Median fee load %"]), vlabel: V.fmt(r["Median fee load %"], 1) + "%",
               color: r.Platform === "Ownly" ? C.s[2] : BLR,
               tip: r.Platform + ": " + r["Median fee load %"] + "% of the bill is fees and tax (" + r.Captures + " captures)" };
    }), max: 35, w: 460, rowH: 36, labelW: 95, fmtAxis: function (t) { return V.fmt(t, 0) + "%"; }
  }),
  "<b>This is the durable half of the advantage.</b> A discount is funded and can be withdrawn; a fee that is " +
  "never charged needs no funding. It is also the one thing rivals cannot copy without giving up revenue.");

/* — PYTHON-ONLY BLOCK — */
card("c6", "Sentiment by audience — and why the revolt isn't visible here", bP(),
  "836 documents scored by a negation-aware lexicon. Higher bar = more positive.",
  (function () {
    var rows = T("04_sentiment_by_audience").slice().sort(function (a, b) { return num(a["Mean sentiment"]) - num(b["Mean sentiment"]); });
    return V.barH({
      data: rows.map(function (r) {
        var m = num(r["Mean sentiment"]);
        return { label: r.Audience + " (" + r.Documents + ")", value: m + 0.5, vlabel: V.fmt(m, 3),
                 color: m < -0.2 ? C.crit : m < 0 ? C.s[3] : C.s[2],
                 tip: r.Audience + "\n" + r.Documents + " documents\nmean " + m +
                      "\n" + r.Negative + " negative / " + r.Neutral + " neutral / " + r.Positive + " positive" };
      }),
      max: 1, ref: 0.5, w: 500, rowH: 32, labelW: 210,
      fmtAxis: function (t) { return V.fmt(t - 0.5, 1); }
    });
  })(),
  "<b>Dashed line is neutral.</b> The honest finding: consumer sentiment is <b>flat</b> across audiences " +
  "(−0.02 to −0.10). Only <b>app-store reviewers</b> are sharply negative (−0.42), and they are the most " +
  "self-selected group in the study. <b>So the Bengaluru revolt shows up as volume and vocabulary, not as " +
  "consumer anger</b> — which fits, because it was a restaurant-side dispute.");

card("c6", "What each audience actually talks about", bP(),
  "Distinctive vocabulary by TF-IDF — terms frequent in one group but rare across the whole corpus.",
  (function () {
    var rows = T("07_topic_terms").filter(function (r) { return r.Split === "By audience"; });
    var groups = ["Bengaluru local", "Incumbent app community", "Professional / LinkedIn"];
    return groups.map(function (g) {
      var t = rows.filter(function (r) { return r.Group === g; }).slice(0, 8);
      if (!t.length) return "";
      return '<div style="margin-bottom:10px"><div style="font-size:12px;font-weight:600;color:var(--ink);margin-bottom:5px">' +
        V.esc(g) + '</div><div style="display:flex;flex-wrap:wrap;gap:5px">' +
        t.map(function (x) {
          return '<span class="pill p-info" data-tip="' + V.esc(x.Term + ' — TF-IDF ' + x["TF-IDF"] + ', in ' + x["Document frequency"] + ' documents') + '">' + V.esc(x.Term) + '</span>';
        }).join("") + '</div></div>';
    }).join("");
  })(),
  "<b>The split is the finding.</b> Incumbent-app communities talk in <b>competitive and fee language</b> " +
  "(toing, pricing, fee, fees, bengaluru, city). Bengaluru locals talk in <b>usage language</b> " +
  "(ordering, cheaper, ordered, refund). <b>Tableau cannot compute TF-IDF</b> — Python does, and Tableau can " +
  "then chart the scores.");

card("c6", "Before and after the Bengaluru launch", bP(),
  "The YouTube corpus carries a phase flag: 199 pre-launch comments, 76 post-launch.",
  (function () {
    var ph = T("05_youtube_phase");
    return V.barGrouped({
      cats: ph.map(function (r) { return r.Phase; }),
      series: [
        { name: "Negative", color: C.crit, values: ph.map(function (r) { return 100 * num(r.Negative) / num(r.Comments); }) },
        { name: "Positive", color: C.s[2], values: ph.map(function (r) { return 100 * num(r.Positive) / num(r.Comments); }) },
      ], w: 420, h: 220
    });
  })(),
  legend([{ name: "Negative %", color: C.crit }, { name: "Positive %", color: C.s[2] }]) +
  "Mean sentiment moves from <b>−0.041 pre-launch to +0.011 post-launch</b> — a small improvement, not a " +
  "swing. <b>Do not over-read it</b>: the two phases come from two different videos with different audiences, " +
  "so this is not a clean before/after.");

card("c6", "What changed in the vocabulary after launch", bP(),
  "Top TF-IDF terms, pre-launch vs post-launch YouTube comments.",
  (function () {
    var rows = T("07_topic_terms").filter(function (r) { return r.Split === "By YouTube phase"; });
    return ["pre-launch", "post-launch"].map(function (g) {
      var t = rows.filter(function (r) { return r.Group === g; }).slice(0, 8);
      return '<div style="margin-bottom:10px"><div style="font-size:12px;font-weight:600;color:var(--ink);margin-bottom:5px">' +
        V.esc(g) + '</div><div style="display:flex;flex-wrap:wrap;gap:5px">' +
        t.map(function (x) { return '<span class="pill ' + (g === "pre-launch" ? "p-na" : "p-info") + '">' + V.esc(x.Term) + '</span>'; }).join("") +
        '</div></div>';
    }).join("");
  })(),
  "<b>Before launch</b> the talk is speculative and business-model framed (confident, business, zerodha, ondc). " +
  "<b>After launch</b> it turns operational and competitive (commissions, riders, menu, toing). " +
  "The conversation moved from “will this work?” to “how does it work, and who pays?”");

card("c6", "The people who actually ordered say something different", bT(),
  "Share of coded items mentioning each theme, by who is speaking.",
  (function () {
    var rows = T("15_theme_by_base");
    var bases = uniq(rows, "Base");
    var themes = ["Fulfilment Fail", "Support Refund", "Price Doubt", "Price Advantage"];
    return V.barGrouped({
      cats: themes,
      series: bases.slice(0, 2).map(function (b, i) {
        return { name: b, color: i === 0 ? C.s[0] : BLR,
                 values: themes.map(function (t) {
                   var f = rows.filter(function (r) { return r.Base === b && r.Theme === t; });
                   return f.length ? num(f[0]["Share of coded items %"]) : 0;
                 }) };
      }), w: 520, h: 240
    }) + legend(bases.slice(0, 2).map(function (b, i) { return { name: b, color: i === 0 ? C.s[0] : BLR }; }));
  })(),
  "<b>People who describe their own order mention a failure 49.5% of the time; people just discussing Ownly, " +
  "18.9%.</b> The closer you get to a real order, the worse it sounds. <b>Caution</b> · public posts are " +
  "self-selected — dissatisfied people post more. The <i>gap between the two</i> carries the information, not the level.");

card("c5", "App-store ratings", bT(),
  "37 reviews. The shape is the finding, not the average.",
  V.barH({
    data: T("14_review_stars").slice().sort(function (a, b) { return b["Star rating"] - a["Star rating"]; })
      .map(function (r) {
        return { label: r["Star rating"] + " ★", value: num(r.Reviews), vlabel: r.Reviews,
                 color: r["Low rating"] === "Yes" ? C.crit : C.s[2],
                 tip: r["Star rating"] + "-star: " + r.Reviews + " of 37" };
      }),
    w: 380, rowH: 28, labelW: 56, fmtAxis: function (t) { return V.fmt(t, 0); }
  }),
  "<b>26 of 37 are 1-star</b>, and the complaints are about delivery and refunds, not price.");

card("c7", "Restaurant-side voice — reported at its real size", bP(),
  "Every post in the corpus written by a restaurant owner or staff member. There are seven.",
  '<div>' + T("08_restaurant_voice").map(function (r) {
    return '<div class="verb"><div class="meta">' +
      '<span class="pill ' + (r["Sentiment label"] === "negative" ? "p-bad" : r["Sentiment label"] === "positive" ? "p-ok" : "p-na") + '">' +
      V.esc(r["Sentiment label"]) + " " + V.fmt(r["Sentiment score"], 2) + '</span>' +
      '<span>' + V.esc(r.Month) + '</span><span>' + V.esc(r.Community) + '</span></div>' +
      '<div class="txt">' + V.esc(r.Verbatim) + '</div></div>';
  }).join('') + '</div>',
  "<b>This is not a finding and must not be presented as one.</b> Seven posts cannot support a sentiment " +
  "claim about restaurant owners. They are shown because the case study asserts restaurants were angry, and " +
  "honesty requires showing that <b>our own social corpus does not evidence that</b> — the revolt is documented " +
  "in media reports, not in our text. One post does capture the fear directly: " +
  "<i>“this wont last long. either they will up fees or shut down.”</i>");
endsec();

/* ══════════════════ 5 · SOLUTIONS ══════════════════ */
sec("s5", "Section 5", "Solutions",
  "What Ownly should keep, adapt and deprioritise — each tied to the number behind it.");

card("", "Keep · Adapt · Deprioritise", bT(),
  "The Bengaluru playbook, element by element.",
  (function () {
    var rows = T("20_keep_adapt_deprioritise");
    var ord = { KEEP: 1, ADAPT: 2, DEPRIORITISE: 3 };
    return rows.slice().sort(function (a, b) { return ord[a.Call] - ord[b.Call]; }).map(function (r) {
      var cls = r.Call === "KEEP" ? "" : r.Call === "ADAPT" ? "partial" : "no";
      var pill = r.Call === "KEEP" ? "p-ok" : r.Call === "ADAPT" ? "p-warn" : "p-bad";
      return '<div class="claim ' + cls + '"><div class="ch"><span class="ct">' + V.esc(r["Playbook element"]) +
        '</span><span class="pill ' + pill + '">' + V.esc(r.Call) + '</span></div>' +
        '<div class="ce">' + V.esc(r.Why) + '</div>' +
        '<div class="cs">evidence · ' + V.esc(r.Evidence) + '  (' + V.esc(r.Source) + ')</div></div>';
    }).join("");
  })(), "");

card("", "The six solutions", bT(),
  "Same structure as the case study, each with the evidence that drives it.",
  tbl([
    { label: "#", n: 1, get: function (r) { return r["#"]; } },
    { label: "Solution", get: function (r) { return "<b>" + V.esc(r.Solution) + "</b>"; } },
    { label: "What to do", get: function (r) { return V.esc(r["What to do"]); } },
    { label: "Evidence", get: function (r) { return V.esc(r.Evidence); } },
    { label: "From", get: function (r) { return '<span class="pill p-na">' + V.esc(r["Evidence source"]) + "</span>"; } },
  ], T("19_solutions")), "");

OUT.push('<section class="card"><div class="callout key">' +
  '<p><b>Full solution.</b> Ownly\'s Bengaluru win was mostly a <b>restaurant</b> win, not a customer win — ' +
  'restaurants were furious with Swiggy and Zomato and needed somewhere to go, and Ownly offered zero commission ' +
  'at exactly the right moment. That door is not open in Hyderabad.</p>' +
  '<p>So in Hyderabad: <b>keep</b> the two things that genuinely belong to Ownly — zero commission and a bill with ' +
  'no hidden fees. <b>Stop leading with the price comparison</b>, because 82.5% of the city holds a membership that ' +
  'erases it and one rival coupon makes Ownly the dearer app. <b>Fix the restaurant list first</b> — it is the only ' +
  'thing people refused to trade, and Ownly currently offers 89% the same restaurants, 17 minutes slower. ' +
  'Then fix <b>delivery reliability</b>, because reviews and interviews agree that failed orders are what make ' +
  'people leave. Treat <b>discounts as the last lever, not the first</b>: only 25% say they would stay once the ' +
  'offer ends, which is precisely how Foodpanda went from 200,000 daily orders to 5,000.</p>' +
  '<p style="font-size:14.5px"><b>In one line: don\'t buy the first order — earn the second one, by stocking the ' +
  'restaurants people actually want and delivering them properly.</b></p></div></section>');

card("", "What we could not check, stated plainly", bT(), "",
  tbl([
    { label: "Open question", get: function (r) { return "<b>" + V.esc(r[0]) + "</b>"; } },
    { label: "Why it is open", get: function (r) { return V.esc(r[1]); } },
  ], [
    ["Whether Ownly is growing in Hyderabad", "Ownly publishes no Hyderabad numbers, and no dated media report of the Hyderabad launch was found in 12+ searches."],
    ["Whether the Bengaluru boycott actually happened", "No reporting found after the 1 Sep 2026 deadline. It may have executed, been called off, or been settled."],
    ["How often Ownly orders really fail", "No test orders were placed. Review complaints come from people who chose to complain, so they overstate failure."],
    ["Whether Ownly makes or loses money per order", "No company in this industry publishes it. The ₹30-in/₹56-out gap uses Swiggy's disclosed rider cost, not Ownly's."],
    ["Anything about repeat behaviour", "Only 2 of 40 respondents had ever ordered on Ownly, so all retention figures are stated intent, not observed behaviour."],
    ["Whether Hyderabad restaurants are unhappy with incumbents", "We found no evidence either way. Absence of reporting is not proof of absence."],
  ]), "");
endsec();

/* ══════════ RENDER ══════════ */
document.getElementById("main").innerHTML = OUT.join("");
V.initTooltip();
(function () {
  var links = Array.prototype.slice.call(document.querySelectorAll("#nav a"));
  var secs = links.map(function (a) { return document.querySelector(a.getAttribute("href")); });
  var t = false;
  function upd() {
    t = false; var best = 0;
    for (var i = 0; i < secs.length; i++) if (secs[i] && secs[i].getBoundingClientRect().top < 140) best = i;
    links.forEach(function (a, k) { a.classList.toggle("on", k === best); });
  }
  window.addEventListener("scroll", function () { if (!t) { t = true; window.requestAnimationFrame(upd); } }, { passive: true });
  upd();
})();
})();
