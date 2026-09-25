/* ═══════════════════════════════════════════════════════════════════
   Ownly BI Workbook — application.
   Seven worksheets, global cross-filtering, live scenario model.
   ═══════════════════════════════════════════════════════════════════ */
(function () {
"use strict";
var B = window.BI, V = window.VZ, C = V.C;
var $ = function (s) { return document.querySelector(s); };

/* ---------- filter state ---------- */
var F = { occ: "", mem: "", multi: "", rap: "", aware: "" };
var TAB = "exec";

function rows() {
  return B.rows.filter(function (r) {
    if (F.occ && r.occ !== F.occ) return false;
    if (F.mem !== "" && r.member !== (F.mem === "1")) return false;
    if (F.multi !== "" && r.multi !== (F.multi === "1")) return false;
    if (F.rap !== "" && r.rapido !== (F.rap === "1")) return false;
    if (F.aware !== "" && r.aware !== (F.aware === "1")) return false;
    return true;
  });
}
function filtered() { return Object.keys(F).some(function (k) { return F[k] !== ""; }); }

/* ---------- stats in JS (mirror of the Python) ---------- */
function wilson(k, n) {
  if (!n) return { k: 0, n: 0, pct: 0, lo: 0, hi: 0 };
  var z = 1.959963985, p = k / n, d = 1 + z * z / n;
  var c = (p + z * z / (2 * n)) / d;
  var h = z * Math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d;
  return { k: k, n: n, pct: +(100 * p).toFixed(1), lo: +(100 * Math.max(0, c - h)).toFixed(1), hi: +(100 * Math.min(1, c + h)).toFixed(1) };
}
function share(rs, pred) {
  var elig = rs.filter(function (r) { return pred(r) !== null; });
  return wilson(elig.filter(pred).length, elig.length);
}
function med(xs) {
  var s = xs.filter(function (v) { return v !== null && v !== undefined && !isNaN(v); }).sort(function (a, b) { return a - b; });
  if (!s.length) return null;
  return s.length % 2 ? s[(s.length - 1) / 2] : (s[s.length / 2 - 1] + s[s.length / 2]) / 2;
}
function boxOf(xs) {
  var s = xs.filter(function (v) { return v !== null && v !== undefined && !isNaN(v); }).sort(function (a, b) { return a - b; });
  if (!s.length) return null;
  var q = function (p) { var i = (s.length - 1) * p, lo = Math.floor(i), hi = Math.ceil(i); return lo === hi ? s[lo] : s[lo] + (s[hi] - s[lo]) * (i - lo); };
  var q1 = q(.25), q3 = q(.75), iqr = q3 - q1;
  var inl = s.filter(function (v) { return v >= q1 - 1.5 * iqr && v <= q3 + 1.5 * iqr; });
  return { min: inl.length ? inl[0] : s[0], q1: q1, med: q(.5), q3: q3,
           max: inl.length ? inl[inl.length - 1] : s[s.length - 1],
           outliers: s.filter(function (v) { return v < q1 - 1.5 * iqr || v > q3 + 1.5 * iqr; }), n: s.length };
}
function logistic(x) { var f = B.demand_curve.fit; return 1 / (1 + Math.exp(-(f.b0 + f.b1 * x))); }

/* ---------- small builders ---------- */
function card(cls, title, sub, body, note) {
  return '<section class="card ' + (cls || "") + '"><h3>' + V.esc(title) + '</h3>' +
    (sub ? '<p class="sub">' + sub + '</p>' : "") + body +
    (note ? '<div class="note">' + note + '</div>' : "") + '</section>';
}
function legend(items) {
  return '<div class="legend">' + items.map(function (i) {
    return '<span><i class="sw" style="background:' + i.color + '"></i>' + V.esc(i.name) + '</span>';
  }).join("") + '</div>';
}
function tableOf(cols, data, opts) {
  opts = opts || {};
  var h = '<div class="tw"><table><thead><tr>' + cols.map(function (c) {
    return '<th class="' + (c.n ? "n" : "") + '">' + V.esc(c.label) + '</th>';
  }).join("") + '</tr></thead><tbody>' + data.map(function (r) {
    return '<tr>' + cols.map(function (c) {
      return '<td class="' + (c.n ? "n" : "") + '">' + (c.get(r) === null || c.get(r) === undefined ? "—" : c.get(r)) + '</td>';
    }).join("") + '</tr>';
  }).join("") + '</tbody></table></div>';
  return h;
}
function srcNote() {
  return filtered()
    ? '<b>Filter active</b> — survey-based charts reflect the ' + rows().length + ' selected respondents. Audit, text and benchmark charts are not respondent-level and do not filter.'
    : '';
}

/* ═══════════════════════════════════════════════════════════════════
   WORKSHEET 1 — EXECUTIVE
   ═══════════════════════════════════════════════════════════════════ */
function exec() {
  var rs = rows();
  var spd = share(rs, function (r) { return r.eta_cheap; });
  var rel = share(rs, function (r) { return r.rel_cheap; });
  var rst = share(rs, function (r) { return r.rest_cheap; });
  var mem = share(rs, function (r) { return r.member; });
  var dbt = share(rs, function (r) { return (r.doubt_n || 0) >= 4; });
  var rpt = share(rs, function (r) { return (r.repeat_n || 0) >= 4; });

  kpis([
    { v: V.pct(rst.pct, 1), k: "will give up usual restaurants for ₹30", s: rst.k + " of " + rst.n + " · CI " + rst.lo + "–" + rst.hi, color: C.crit },
    { v: V.inr(114.5), k: "median saving Ownly delivers", s: "4 of 4 matched baskets" },
    { v: V.pct(mem.pct, 1), k: "hold an incumbent membership", s: mem.k + " of " + mem.n },
    { v: V.inr(B.breakeven.contrib_per_order, 2), k: "contribution per order at reported economics", s: "₹30 revenue − ₹56.01 rider", color: C.crit },
    { v: "27.3%", k: "of switching bar still cleared after a rival coupon", s: "down from 81.1%", color: C.crit },
    { v: B.text_meta.n.toLocaleString(), k: "public documents analysed", s: "16 months, 3 sources" },
  ]);

  var g = "";

  g += card("h7", "What Gachibowli will trade for ₹30",
    "Same ₹30 saving, three different sacrifices, same respondents. Whiskers are 95% Wilson intervals.",
    V.barH({
      data: [
        { label: "Wait 15 minutes longer", value: spd.pct, lo: spd.lo, hi: spd.hi, vlabel: V.pct(spd.pct), color: C.s[0], tip: "Accepts a 15-min delay to save ₹30 — " + spd.k + " of " + spd.n },
        { label: "Accept 3-in-10 late, not 1-in-10", value: rel.pct, lo: rel.lo, hi: rel.hi, vlabel: V.pct(rel.pct), color: C.s[0], tip: "Accepts worse reliability — " + rel.k + " of " + rel.n },
        { label: "Give up usual restaurants", value: rst.pct, lo: rst.lo, hi: rst.hi, vlabel: V.pct(rst.pct), color: C.s[1], tip: "Gives up their restaurants — " + rst.k + " of " + rst.n },
      ], max: 100, ref: 50, w: 660, rowH: 46, labelW: 210, fmtAxis: function (t) { return V.fmt(t, 0) + "%"; }
    }),
    "<b>McNemar exact, paired</b> · restaurants vs speed p = 1.5×10⁻⁶ (24 switched one way, 1 the other) · restaurants vs reliability p = 0.0026. " + srcNote());

  g += card("h5", "Where the price advantage goes",
    "Share of person × restaurant pairs where Ownly's saving clears that person's own stated switching bar.",
    V.waterfall({
      data: [
        { label: "List price", value: 81.1 },
        { label: "Membership effect", value: -25.0 },
        { label: "Coupon effect", value: -28.8 },
        { label: "After coupon", total: true },
      ], w: 420, h: 280, fmtAxis: function (t) { return V.fmt(t, 0) + "%"; }
    }),
    "<b>Source</b> · switch_threshold_coverage.csv · 132 pairs (33 respondents naming a figure × 4 baskets). After a rival coupon the median saving is <b>−₹28.07</b> — Ownly is dearer.");

  g += card("h6", "Adoption funnel in this catchment",
    "Self-reported. Intervals widen sharply as the base shrinks.",
    V.funnel({
      data: [
        { label: "Heard of Ownly", value: share(rs, function (r) { return r.aware; }).pct, k: rs.filter(function (r) { return r.aware; }).length, n: rs.length },
        { label: "Opened / browsed", value: share(rs, function (r) { return r.opened; }).pct, k: rs.filter(function (r) { return r.opened; }).length, n: rs.length },
        { label: "Ordered", value: share(rs, function (r) { return r.ordered; }).pct, k: rs.filter(function (r) { return r.ordered; }).length, n: rs.length },
      ], w: 560
    }),
    "<b>Caution</b> · the trial base is 2 respondents unfiltered (CI 1.4–16.5%). The 4-week window mostly predates Ownly's Hyderabad rollout.");

  g += card("h6", "Belief in the proposition",
    "Top-2-box agreement. The price story only works if it is believed.",
    V.barH({
      data: [
        { label: "Expect prices to rise later", value: dbt.pct, lo: dbt.lo, hi: dbt.hi, vlabel: V.pct(dbt.pct), color: C.crit },
        { label: "Would stay after the offer ends", value: rpt.pct, lo: rpt.lo, hi: rpt.hi, vlabel: V.pct(rpt.pct), color: C.s[2] },
      ], max: 100, w: 520, rowH: 46, labelW: 200, fmtAxis: function (t) { return V.fmt(t, 0) + "%"; }
    }),
    "<b>Trial-to-repeat intent gap</b> · 52.5 pp (MM9). Foodpanda fell from ~200k to ~5k daily orders when discounting stopped.");

  g += card("", "The recommendation — Bengaluru playbook, tactic by tactic",
    "Each call is anchored to a single measured number.",
    tableOf([
      { label: "Bengaluru tactic", get: function (r) { return "<b>" + r[0] + "</b>"; } },
      { label: "Call", get: function (r) { return '<span class="pill ' + r[1] + '">' + r[2] + "</span>"; } },
      { label: "Evidence", get: function (r) { return r[3]; } },
    ], [
      ["No platform / packaging / surge fee", "p-ok", "Keep", "Fee load <b>5.2%</b> vs incumbent median <b>23.4%</b> (K3). Structural — needs no subsidy."],
      ["\"Total you see is total you pay\"", "p-ok", "Keep", "Cheapest in <b>4 of 4</b> baskets; median saving <b>₹114.50</b> against a stated ₹30 bar."],
      ["Headline \"cheaper than Swiggy & Zomato\"", "p-warn", "Adapt", "<b>82.5%</b> hold a membership; after one coupon Ownly is <b>₹28 dearer</b>. The claim is falsifiable."],
      ["Stock the same big chains", "p-warn", "Adapt", "<b>88.9%</b> catalogue overlap, <b>+17 min</b> slower. Only <b>35%</b> will give up their restaurants."],
      ["Rapido placement as growth channel", "p-warn", "Adapt", "Only <b>5 of 33</b> answering had noticed food inside Rapido — an <b>84.8%</b> discovery gap."],
      ["₹100 off the first order", "p-bad", "Deprioritise", "<b>25%</b> post-offer repeat intent; <b>87.5%</b> expect prices to rise. Rented demand."],
      ["Spend to match delivery speed", "p-bad", "Deprioritise", "<b>92.5%</b> accept 15 min slower. Our own pre-registered prediction P3 was falsified."],
    ]),
    "");

  g += card("", "The economic constraint underneath all of it", "",
    '<div class="callout bad"><p><b>' + V.esc(B.breakeven.headline) + '</b></p><p>' + V.esc(B.breakeven.consequence) + '</p></div>',
    "Full sourcing and caveats on the <b>Predictive &amp; Scenarios</b> worksheet.");

  return g;
}

/* ═══════════════════════════════════════════════════════════════════
   WORKSHEET 2 — PRICE & VALUE
   ═══════════════════════════════════════════════════════════════════ */
function price() {
  var lf = B.pairs.filter(function (p) { return p.view === "LIST+FEES"; });
  kpis([
    { v: "4 of 4", k: "baskets Ownly wins on list price", s: "K1a — 100%" },
    { v: "3 of 4", k: "wins once a membership applies", s: "K1b — 75%" },
    { v: "2 of 4", k: "wins after a rival coupon", s: "K1c — 50%", color: C.crit },
    { v: V.inr(114.5), k: "median saving, list + fees", s: "K2" },
    { v: "5.2%", k: "Ownly fee load", s: "vs 23.4% incumbent median" },
    { v: "+17 min", k: "median quoted ETA gap", s: "flat across all 4 restaurants" },
  ]);

  var g = "";

  g += card("h6", "Matched basket comparison — list price + fees",
    "Same items, same Gachibowli address, same 20-minute window, 16 Sep 2026. No coupon on either side.",
    V.barGrouped({
      cats: lf.map(function (p) { return p.restaurant; }),
      series: [
        { name: "Ownly", color: C.s[2], values: lf.map(function (p) { return p.ownly; }) },
        { name: "Cheapest rival", color: C.s[1], values: lf.map(function (p) { return p.rival; }) },
      ], w: 580, h: 260
    }),
    legend([{ name: "Ownly", color: C.s[2] }, { name: "Cheapest incumbent", color: C.s[1] }]) +
    "<b>Limitation</b> · n = 4 baskets, one address, one dinner slot. Directional, not a price index.");

  g += card("h6", "Where the money goes — bill composition",
    "Median share of the final bill by component, zero-discount captures only.",
    V.stacked100({
      data: B.fee_decomp.map(function (f) {
        return {
          label: f.platform.charAt(0).toUpperCase() + f.platform.slice(1),
          parts: f.parts.filter(function (p) { return p.pct > 0; }).map(function (p, i) {
            return { name: p.part, value: p.pct, color: p.part === "Food" ? C.s[2] : C.s[[1, 3, 0, 4, 7, 5][i % 6]] };
          })
        };
      }), w: 560, labelW: 80
    }),
    legend([{ name: "Food", color: C.s[2] }, { name: "Fees & tax", color: C.s[1] }]) +
    "<b>The structural point</b> · Ownly's advantage is mostly <i>not</i> a lower menu price — it is fees it does not charge. A discount can be withdrawn; a fee that is never charged cannot.");

  g += card("h6", "Price versus speed — the trade being offered",
    "Each point is one restaurant on one platform. Down-and-right is cheaper but slower.",
    V.scatter({
      data: B.pairs.filter(function (p) { return p.view === "LIST+FEES"; }).reduce(function (a, p) {
        a.push({ x: p.ownly_eta, y: p.ownly, r: 7, color: C.s[2], label: p.restaurant, tip: "Ownly · " + p.restaurant + " — " + V.inr(p.ownly) + ", " + p.ownly_eta + " min" });
        a.push({ x: p.rival_eta, y: p.rival, r: 7, color: C.s[1], tip: p.rival_name + " · " + p.restaurant + " — " + V.inr(p.rival) + ", " + p.rival_eta + " min" });
        return a;
      }, []),
      w: 560, h: 290, xlab: "Quoted delivery time (min)", ylab: "Final payable (₹)",
      fmtY: function (t) { return "₹" + V.fmt(t, 0); }
    }),
    legend([{ name: "Ownly", color: C.s[2] }, { name: "Incumbent", color: C.s[1] }]) +
    "Ownly sits lower (cheaper) and further right (slower) on every restaurant. The survey says the market accepts that trade: <b>92.5%</b> take cheaper-and-slower.");

  g += card("h6", "Saving delivered vs saving demanded",
    "The bar is what the audit observed; the marker is the median switching bar respondents stated.",
    B.erosion.map(function (e) {
      return V.bullet({
        label: e.view + " — " + V.pct(e.pct) + " of pairs clear the bar",
        value: Math.max(0, e.median_saving), max: 130, target: 30,
        color: e.median_saving < 30 ? C.crit : C.s[2],
        vlabel: V.inr(e.median_saving), w: 520,
        bands: [{ from: 0, to: 30, color: C.crit }]
      });
    }).join(""),
    "<b>Black line</b> = ₹30, the median recurring saving respondents said they need. <b>Red band</b> = below the bar. After a coupon the median saving is <b>negative</b>.");

  g += card("h6", "Delivery time by restaurant",
    "Quoted ETA midpoint at checkout, Ownly against the fastest incumbent.",
    V.lollipop({
      data: B.eta_gap.map(function (e) {
        return { label: e.restaurant, a: e.best, b: e.ownly, vlabel: "+" + V.fmt(e.gap, 0) + " min" };
      }),
      w: 540, labelW: 140, nameA: "Fastest incumbent", nameB: "Ownly",
      colorA: C.s[1], colorB: C.s[2], fmtAxis: function (t) { return V.fmt(t, 0) + "m"; }
    }),
    legend([{ name: "Fastest incumbent", color: C.s[1] }, { name: "Ownly", color: C.s[2] }]) +
    "The penalty is <b>flat across unrelated brands</b> (+17.5 to +24 min) — the signature of fulfilling from a more distant outlet, not of rider or batching noise. Mechanism inferred, not shown: outlet distances were not recorded.");

  g += card("h6", "Basket size distribution",
    "What respondents last spent, and how many orders they place.",
    V.boxplot({
      data: [
        { label: "Last bill (₹)", box: boxOf(rows().map(function (r) { return r.last_amount; })) || { min: 0, q1: 0, med: 0, q3: 0, max: 0, outliers: [], n: 0 }, color: C.s[0] },
        { label: "Saving required (₹)", box: boxOf(rows().map(function (r) { return r.switch_rs; })) || { min: 0, q1: 0, med: 0, q3: 0, max: 0, outliers: [], n: 0 }, color: C.s[3] },
      ], w: 560, labelW: 150, fmtAxis: function (t) { return "₹" + V.fmt(t, 0); }
    }),
    "Box = interquartile range, line = median, circles = Tukey outliers. " + srcNote());

  g += card("", "Every matched basket, all three price views",
    "The full audit result. 'Wins' means Ownly's final payable was lowest.",
    tableOf([
      { label: "Restaurant", get: function (r) { return "<b>" + r.restaurant + "</b>"; } },
      { label: "View", get: function (r) { return r.view; } },
      { label: "Ownly", n: 1, get: function (r) { return V.inr(r.ownly, 2); } },
      { label: "Cheapest rival", n: 1, get: function (r) { return V.inr(r.rival, 2); } },
      { label: "Rival", get: function (r) { return r.rival_name; } },
      { label: "Saving", n: 1, get: function (r) { return V.inr(r.saving, 2); } },
      { label: "Saving %", n: 1, get: function (r) { return V.fmt(r.saving_pct, 1) + "%"; } },
      { label: "Result", get: function (r) { return '<span class="pill ' + (r.wins ? "p-ok" : "p-bad") + '">' + (r.wins ? "Ownly wins" : "Ownly loses") + "</span>"; } },
    ], B.pairs),
    "<b>Source</b> · audit_pairs.csv. The Ownly account was new (carrying an intro offer); the incumbent accounts were subscribed.");

  return g;
}

/* ═══════════════════════════════════════════════════════════════════
   WORKSHEET 3 — DEMAND & SEGMENTS
   ═══════════════════════════════════════════════════════════════════ */
function demand() {
  var rs = rows();
  var mm = med(rs.map(function (r) { return r.switch_rs; }));
  kpis([
    { v: rs.length + " of " + B.rows.length, k: "respondents in current selection", s: filtered() ? "filter active" : "no filter" },
    { v: mm === null ? "—" : V.inr(mm), k: "median saving required to switch", s: "K13" },
    { v: V.pct(share(rs, function (r) { return r.member; }).pct), k: "hold a membership", s: "K11" },
    { v: V.pct(share(rs, function (r) { return r.multi; }).pct), k: "multi-home across apps", s: "K12" },
    { v: V.fmt(med(rs.map(function (r) { return r.orders_4wk; })), 0), k: "median orders per 4 weeks", s: "self-reported" },
    { v: V.inr(med(rs.map(function (r) { return r.last_amount; }))), k: "median last bill", s: "self-reported" },
  ]);

  var g = "";

  g += card("h7", "The switching staircase — cumulative willingness",
    "Share of respondents who would switch at or below each recurring saving. This is a demand curve.",
    V.lineChart({
      x: [10, 20, 30, 50, 75, 100].map(function (v) { return "₹" + v; }),
      series: [{ name: "Cumulative % willing to switch", color: C.s[0], area: true,
                 values: B.demand_curve.observed.map(function (p) { return p.y; }) }],
      w: 620, h: 250, max: 100, fmtAxis: function (t) { return V.fmt(t, 0) + "%"; },
      fmtTip: function (v) { return V.fmt(v, 1) + "%"; }
    }),
    "<b>Source</b> · switching_staircase.csv · base = " + B.demand_curve.n_named + " respondents who named a rupee figure. " +
    B.demand_curve.excluded_never + " said no amount would move them and " + B.demand_curve.excluded_dk + " did not know — both held out rather than coded as zero. Fitted model on the Predictive worksheet.");

  g += card("h5", "Trade-off by segment",
    "Does the ₹30 result hold within subgroups? Fisher exact p on each contrast.",
    tableOf([
      { label: "Dimension", get: function (r) { return r.dim; } },
      { label: "Segment", get: function (r) { return "<b>" + r.seg + "</b>"; } },
      { label: "n", n: 1, get: function (r) { return r.n; } },
      { label: "Accept", n: 1, get: function (r) { return V.pct(r.pct); } },
      { label: "95% CI", n: 1, get: function (r) { return r.lo + "–" + r.hi; } },
      { label: "p", n: 1, get: function (r) { return r.p === null ? "—" : V.fmt(r.p, 3); } },
    ], B.segment_tradeoffs),
    "Every contrast is <b>underpowered</b>: the working-professional cell is n = 7. Directional only.");

  g += card("h6", "Segment scorecard",
    "Six cuts of the catchment across the metrics that drive the decision.",
    tableOf([
      { label: "Segment", get: function (r) { return "<b>" + r.segment + "</b>"; } },
      { label: "n", n: 1, get: function (r) { return r.n; } },
      { label: "Trades speed", n: 1, get: function (r) { return r["Trades speed for ₹30"] + "%"; } },
      { label: "Trades restaurants", n: 1, get: function (r) { return r["Trades restaurants for ₹30"] + "%"; } },
      { label: "Saving req.", n: 1, get: function (r) { return "₹" + r["Median saving required (₹)"]; } },
      { label: "Post-offer repeat", n: 1, get: function (r) { return r["Post-offer repeat intent (top-2 %)"] + "%"; } },
      { label: "Price doubt", n: 1, get: function (r) { return r["Price-durability doubt (top-2 %)"] + "%"; } },
    ], B.segment_cuts),
    "<b>Source</b> · segment_cuts.csv, computed on the full catchment (not affected by the sidebar filter).");

  g += card("h6", "How much saving do people demand?",
    "Distribution of the stated recurring saving needed to change main app.",
    V.histogram({
      values: rs.map(function (r) { return r.switch_rs; }).filter(function (v) { return v !== null; }),
      bins: 8, min: 0, max: 120, w: 520, h: 230, color: C.s[3],
      fmtAxis: function (t) { return "₹" + V.fmt(t, 0); }
    }),
    "Excludes the respondents who said <b>no amount</b> would move them and those who did not know. " + srcNote());

  g += card("h6", "Where orders go today",
    "Total self-reported orders in the last 4 weeks, by platform, within the selection.",
    V.donut({
      data: (function () {
        var p = { Swiggy: 0, Zomato: 0, Ownly: 0, Other: 0 };
        rs.forEach(function (r) { p.Swiggy += r.n_swiggy || 0; p.Zomato += r.n_zomato || 0; p.Ownly += r.n_ownly || 0; p.Other += r.n_other || 0; });
        return [{ label: "Swiggy", value: p.Swiggy, color: C.s[1] }, { label: "Zomato", value: p.Zomato, color: C.s[7] },
                { label: "Other", value: p.Other, color: C.s[4] }, { label: "Ownly", value: p.Ownly, color: C.s[2] }];
      })(),
      size: 210, center: (function () { var t = 0; rs.forEach(function (r) { t += (r.orders_4wk || 0); }); return V.cnt(t); })(), centerSub: "orders / 4 wk"
    }),
    "<b>MM4 Sample Volume Share</b> · Ownly's share of orders inside this sample is <b>0.0%</b> — the only respondents reporting Ownly orders had contradictory answers and were excluded.");

  g += card("h6", "Relationships between the survey variables",
    "Spearman rank correlation. Blue = positive, red = negative, pale = no relationship.",
    V.heatmap({
      rows: B.corr.vars, cols: B.corr.vars,
      get: function (r, c) {
        var f = B.corr.cells.find(function (x) { return (x.a === r && x.b === c) || (x.a === c && x.b === r); });
        return f ? f.rho : null;
      },
      label: function (v) { return V.fmt(v, 2); },
      tip: function (r, c, v) {
        var f = B.corr.cells.find(function (x) { return (x.a === r && x.b === c) || (x.a === c && x.b === r); });
        return r + " × " + c + "\nρ = " + (f ? f.rho : "—") + (f && f.p !== null ? "\np = " + V.fmt(f.p, 3) + " (n=" + f.n + ")" : "");
      },
      w: 640, labelW: 168, headH: 88, cellH: 30
    }),
    "<b>Read with care</b> · at n = 40 only strong relationships are detectable. Every off-diagonal cell here is weak and none reaches significance — reported as a null result, not suppressed.");

  g += card("", "Formally tested associations",
    "The four relationships specified in the pre-analysis plan.",
    tableOf([
      { label: "Question", get: function (r) { return "<b>" + r.q + "</b>"; } },
      { label: "n", n: 1, get: function (r) { return r.n; } },
      { label: "ρ", n: 1, get: function (r) { return V.fmt(r.rho, 3); } },
      { label: "p", n: 1, get: function (r) { return V.fmt(r.p, 3); } },
      { label: "95% CI", n: 1, get: function (r) { return V.fmt(r.lo, 2) + " – " + V.fmt(r.hi, 2); } },
      { label: "Verdict", get: function (r) { return '<span class="pill p-na">' + r.verdict + "</span>"; } },
    ], B.associations),
    "All four fail to reach significance. At n = 40 this means <b>the sample cannot detect a relationship</b>, not that none exists.");

  return g;
}

/* ═══════════════════════════════════════════════════════════════════
   WORKSHEET 4 — VOICE OF CUSTOMER  (text analytics)
   ═══════════════════════════════════════════════════════════════════ */
function voc() {
  var sv = B.sentiment_vs_star;
  kpis([
    { v: V.cnt(B.text_meta.n), k: "documents scored", s: "524 social · 275 YouTube · 37 app store" },
    { v: B.text_trend.length + " mo", k: "of dated coverage", s: B.text_trend[0].month + " → " + B.text_trend[B.text_trend.length - 1].month },
    { v: V.fmt(sv.spearman.rho, 2), k: "sentiment vs star rating (ρ)", s: "p < 0.001 — lexicon validated", color: C.good },
    { v: "−0.42", k: "mean sentiment, app store", s: "vs −0.02 social", color: C.crit },
    { v: "26 of 37", k: "app-store reviews are 1-star", s: "70%", color: C.crit },
    { v: B.theme_families.length, k: "theme families from 119 codes", s: "rule-based rollup" },
  ]);

  var g = "";

  g += card("h5", "Does the sentiment model actually work?",
    "Validation: mean lexicon score against the star rating the reviewer chose. These are independent signals.",
    V.barH({
      data: sv.by_star.map(function (r) {
        return { label: r.star + " star  (n=" + r.n + ")", value: r.mean + 1, vlabel: V.fmt(r.mean, 2),
                 color: r.mean < 0 ? C.crit : C.s[2], tip: r.star + "-star reviews: mean sentiment " + V.fmt(r.mean, 3) };
      }),
      max: 2, ref: 1, w: 420, rowH: 34, labelW: 130,
      fmtAxis: function (t) { return V.fmt(t - 1, 1); }
    }),
    "<b>Spearman ρ = " + V.fmt(sv.spearman.rho, 3) + ", n = " + sv.spearman.n + ", p < 0.001.</b> The lexicon was written blind to the star ratings, so this is a genuine out-of-sample check. Monotonic from 1★ (−0.66) to 5★ (+0.34).");

  g += card("h7", "Sentiment by source",
    "The people who have actually ordered are far more negative than the people commenting.",
    V.stacked100({
      data: B.sentiment_by_source.map(function (r) {
        return { label: r.src + " (" + r.n + ")", parts: [
          { name: "Negative", value: 100 * r.negative / r.n, color: C.crit },
          { name: "Neutral", value: 100 * r.neutral / r.n, color: "#c9d1d8" },
          { name: "Positive", value: 100 * r.positive / r.n, color: C.s[2] },
        ] };
      }), w: 600, labelW: 130
    }),
    legend([{ name: "Negative", color: C.crit }, { name: "Neutral", color: "#c9d1d8" }, { name: "Positive", color: C.s[2] }]) +
    "<b>Mean score</b> · app store −0.42, YouTube −0.03, social −0.02. <b>Caution</b> · public posts are self-selected and dissatisfied users post far more readily. The <i>difference between sources</i> carries the information, not the level.");

  g += card("h7", "Volume and sentiment over 16 months",
    "Monthly document count against mean sentiment. Ownly's Hyderabad activity begins mid-2026.",
    V.lineChart({
      x: B.text_trend.map(function (t) { return t.month.slice(2); }),
      series: [
        { name: "Documents", color: C.s[0], area: true, values: B.text_trend.map(function (t) { return t.n; }) },
      ], w: 620, h: 190, fmtTip: function (v) { return V.fmt(v, 0) + " documents"; }
    }) +
    V.lineChart({
      x: B.text_trend.map(function (t) { return t.month.slice(2); }),
      series: [{ name: "Mean sentiment", color: C.s[1], values: B.text_trend.map(function (t) { return t.mean; }) }],
      w: 620, h: 150, min: -0.5, max: 0.5, fmtAxis: function (t) { return V.fmt(t, 2); },
      fmtTip: function (v) { return V.fmt(v, 3); }
    }),
    legend([{ name: "Document volume", color: C.s[0] }, { name: "Mean sentiment", color: C.s[1] }]) +
    "<b>Volume spikes in 2026-08</b> (331 of 836 documents) around the Hyderabad push. Sentiment runs slightly negative throughout and does <b>not</b> improve as volume rises.");

  g += card("h5", "What the market talks about",
    "119 granular codes rolled into families by keyword rule. Area = number of documents.",
    V.treemap({
      data: B.theme_families.filter(function (f) { return f.family !== "Other"; }).map(function (f) {
        return { label: f.family, value: f.n, tip: f.family + "\n" + f.n + " documents\nmean sentiment " + V.fmt(f.sentiment, 2),
                 sentiment: f.sentiment };
      }),
      color: function (r) { return V.diverge(r.sentiment, 0.35); },
      w: 470, h: 300
    }),
    "<b>Colour = sentiment</b> (red negative, green positive). Execution themes are the negative ones; value themes are the positive ones.");

  g += card("h7", "Theme volume against theme sentiment",
    "Bottom-right is the danger zone: talked about a lot, and talked about badly.",
    V.scatter({
      data: B.theme_families.filter(function (f) { return f.family !== "Other"; }).map(function (f) {
        return { x: f.n, y: f.sentiment, r: 6 + Math.sqrt(f.n) * 0.9,
                 color: f.sentiment < -0.15 ? C.crit : (f.sentiment > 0.05 ? C.s[2] : C.s[3]),
                 label: f.family.length > 16 ? f.family.slice(0, 15) + "…" : f.family,
                 tip: f.family + "\n" + f.n + " documents\nmean sentiment " + V.fmt(f.sentiment, 3) };
      }),
      w: 600, h: 300, ymin: -0.45, ymax: 0.25, xmin: 0,
      xlab: "Documents mentioning the theme", ylab: "Mean sentiment",
      fmtY: function (t) { return V.fmt(t, 2); }
    }),
    "<b>Fulfilment failure</b> (−0.33), <b>Support &amp; refunds</b> (−0.27) and <b>Trust</b> (−0.25) are the negative cluster — all execution, none of them price. <b>Price — advantage</b> is the largest theme and is mildly positive.");

  g += card("h6", "Distinctive vocabulary",
    "Top terms by mean TF-IDF across all 836 documents, after removing stopwords and the brand names themselves.",
    V.barH({
      data: B.terms_overall.slice(0, 14).map(function (t, i) {
        return { label: t.term, value: t.score, vlabel: V.fmt(t.score * 100, 1),
                 color: V.seqColor(0.35 + 0.6 * (1 - i / 14)),
                 tip: '"' + t.term + '" — TF-IDF ' + V.fmt(t.score, 4) + ", appears in " + t.df + " documents" };
      }),
      w: 520, rowH: 25, labelW: 130, fmtAxis: function (t) { return V.fmt(t * 100, 0); }
    }),
    "TF-IDF favours terms that are frequent in some documents but rare across the corpus — i.e. what makes a document <i>distinctive</i>, not merely common.");

  g += card("h6", "Which themes co-occur",
    "Pairs of themes appearing in the same document. Reveals how arguments bundle.",
    V.barH({
      data: B.cooccur.slice(0, 12).map(function (c) {
        return { label: (c.a.length > 16 ? c.a.slice(0, 15) + "…" : c.a) + " + " + (c.b.length > 16 ? c.b.slice(0, 15) + "…" : c.b),
                 value: c.n, vlabel: c.n, color: C.s[0], tip: c.a + " + " + c.b + ": " + c.n + " documents" };
      }),
      w: 540, rowH: 25, labelW: 250, fmtAxis: function (t) { return V.fmt(t, 0); }
    }),
    "<b>Source</b> · co-occurrence within the theme codes assigned to each document.");

  g += card("", "Most-engaged verbatims",
    "Ranked by likes/reactions. Engagement is published by YouTube and a few social posts only — " +
    B.engagement_note.available_n + " of " + B.engagement_note.total_n + " documents.",
    '<div>' + B.verbatims.slice(0, 14).map(function (v) {
      return '<div class="verb"><div class="meta">' +
        '<span class="pill ' + (v.label === "negative" ? "p-bad" : v.label === "positive" ? "p-ok" : "p-na") + '">' + v.label + " " + V.fmt(v.score, 2) + '</span>' +
        '<span>' + V.esc(v.src) + '</span>' + (v.date ? '<span>' + v.date + '</span>' : "") +
        (v.eng ? '<span>♥ ' + V.cnt(v.eng) + '</span>' : "") +
        (v.star ? '<span>' + v.star + '★</span>' : "") +
        (v.themes.length ? '<span>' + V.esc(v.themes.slice(0, 3).join(" · ")) + '</span>' : "") +
        '</div><div class="txt">' + V.esc(v.text) + '</div></div>';
    }).join("") + '</div>',
    "<b>Warning</b> · " + V.esc(B.engagement_note.warning));

  return g;
}

/* ═══════════════════════════════════════════════════════════════════
   WORKSHEET 5 — COMPETITIVE POSITION
   ═══════════════════════════════════════════════════════════════════ */
function compete() {
  var bl = B.blr_vs_hyd;
  kpis([
    { v: "88.9%", k: "of Ownly's catalogue is also on a rival", s: "K5 — 8 of 9" },
    { v: "90.0%", k: "audit-frame coverage", s: "K4 — 9 of 10" },
    { v: "221", k: "restaurants Ownly lists at this address", s: "we sampled 10" },
    { v: "1", k: "Ownly-exclusive restaurant observed", s: "and 1 missing from Ownly" },
    { v: "42.5%", k: "awareness in Gachibowli", s: "vs 75.0% in Bengaluru" },
    { v: "5.0%", k: "trial in Gachibowli", s: "vs 25.0% in Bengaluru" },
  ]);

  var g = "";

  g += card("h6", "Restaurant availability across platforms",
    "The 10-restaurant audit frame. Green = listed, grey = not listed.",
    V.heatmap({
      rows: B.coverage.map(function (r) { return r.restaurant_display; }),
      cols: ["ownly", "swiggy", "zomato"],
      get: function (r, c) {
        var row = B.coverage.find(function (x) { return x.restaurant_display === r; });
        var v = (row[c] || "").toString().toLowerCase();
        return v === "y" || v === "true" ? 1 : 0;
      },
      color: function (v) { return v ? "#bfe6cf" : "#eceff2"; },
      label: function (v) { return v ? "●" : "—"; },
      tip: function (r, c, v) { return r + " on " + c + ": " + (v ? "listed" : "not listed"); },
      w: 470, labelW: 190, headH: 56, cellH: 28
    }),
    "<b>Selection caveat</b> · the frame was built from Ownly's own showcase page plus incumbent chains, so it <b>selects for restaurants present everywhere</b> and cannot detect exclusives. Ownly lists 221 restaurants at this address; we priced 10.");

  g += card("h6", "Gachibowli against the Bengaluru benchmark",
    "The same six metrics measured in both cities. Bengaluru is where the playbook was written.",
    V.slope({
      data: [
        { label: "Awareness", left: +bl[1].aware_pct, right: +bl[0].aware_pct, color: C.s[0] },
        { label: "Trial", left: +bl[1].tried_pct, right: +bl[0].tried_pct, color: C.s[1] },
        { label: "Membership", left: +bl[1].membership_pct, right: +bl[0].membership_pct, color: C.s[2] },
        { label: "Multi-homing", left: +bl[1].multihoming_pct, right: +bl[0].multihoming_pct, color: C.s[3] },
        { label: "Price doubt", left: +bl[1].durability_doubt_pct, right: +bl[0].durability_doubt_pct, color: C.s[7] },
      ],
      leftLabel: "Bengaluru (n=16)", rightLabel: "Gachibowli (n=40)", w: 470, h: 290
    }),
    "<b>Awareness and trial are far lower in Hyderabad</b> — expected, since Ownly is weeks old there. <b>Membership lock-in is the same</b> in both (81% vs 83%), so the barrier travels. <b>The Bengaluru switching bar is higher</b> (₹50 vs ₹30). <b>Caution</b> · the Bengaluru base is n = 16.");

  g += card("h6", "Where challengers have failed before",
    "Five mechanisms from the historical record, scored against our own evidence.",
    tableOf([
      { label: "Failure mechanism", get: function (r) { return "<b>" + r[0] + "</b>"; } },
      { label: "Ownly", get: function (r) { return '<span class="pill ' + r[1] + '">' + r[2] + "</span>"; } },
      { label: "Our evidence", get: function (r) { return r[3]; } },
    ], [
      ["Rented demand — price funded by subsidy", "p-ok", "Escaped", "Ownly's saving is structural: fee load 5.2% vs 23.4%. It does not require funding to persist."],
      ["No new use case — same catalogue", "p-bad", "Exposed", "88.9% catalogue overlap. Same restaurants, +17 min slower. This is what killed Amazon Food."],
      ["Attacking a side that was not scarce", "p-bad", "Exposed", "Restaurants already multi-home on every platform. Zero-commission buys supply that was never constrained."],
      ["Thin unit economics", "p-bad", "Exposed", "₹30 revenue against ₹56.01 industry rider payout = −₹26.01 per order before any overhead."],
      ["Distribution assumed to convert", "p-warn", "At risk", "Uber Eats had the same amortised-fleet logic. Only 5 of 33 noticed food inside Rapido."],
    ]),
    "<b>Source</b> · 01_secondary_research/challenger_failures/ — Foodpanda, Uber Eats India, Amazon Food, Dunzo, ONDC, magicpin, Thrive, DotPe, Toing, Zepto Café.");

  g += card("h6", "App-store rating distribution",
    "37 reviews retrieved. The shape, not the mean, is the finding.",
    V.barH({
      data: B.stars.slice().sort(function (a, b) { return b.star - a.star; }).map(function (s) {
        return { label: s.star + " ★", value: s.n, vlabel: s.n,
                 color: s.star <= 2 ? C.crit : s.star === 3 ? C.s[3] : C.s[2],
                 tip: s.star + "-star: " + s.n + " of 37 reviews" };
      }),
      w: 460, rowH: 30, labelW: 60, fmtAxis: function (t) { return V.fmt(t, 0); }
    }),
    "<b>Strongly bimodal and bottom-heavy</b> — 26 of 37 at 1★. App-store reviews are the most self-selected source in the study: people review after something goes wrong. Not an order failure rate.");

  g += card("", "Market context",
    "Scale figures, and what each one can and cannot be used for.",
    tableOf([
      { label: "Item", get: function (r) { return "<b>" + r.item + "</b>"; } },
      { label: "Value", n: 1, get: function (r) { return V.cnt(+r.value); } },
      { label: "Source", get: function (r) { return r.source; } },
      { label: "Evidence type", get: function (r) { return '<span class="pill p-na">' + r.evidence_type + "</span>"; } },
      { label: "Use", get: function (r) { return r.use; } },
    ], B.market_context),
    "None of these is a market size. Value share, relative share and BDI/CDI are all marked NOT ESTIMABLE — see the Method worksheet.");

  return g;
}

/* ═══════════════════════════════════════════════════════════════════
   WORKSHEET 6 — PREDICTIVE & SCENARIOS
   ═══════════════════════════════════════════════════════════════════ */
var SC = null;
function predict() {
  var dc = B.demand_curve, be = B.breakeven;
  if (!SC) SC = {
    saving: 115, coverage: 35, discovery: 15, rev: B.econ_defaults.rev_per_order,
    rider: B.econ_defaults.rider_cost, cac: B.econ_defaults.cac,
    share: B.econ_defaults.target_share_pct, opm: B.econ_defaults.orders_per_user_month
  };

  kpis([
    { v: V.fmt(dc.fit.r2, 3), k: "R² of the fitted demand curve", s: "6 observed points", color: C.good },
    { v: V.pct(100 * logistic(30)), k: "predicted switching at a ₹30 saving", s: "the stated median bar" },
    { v: V.pct(100 * logistic(114.5)), k: "predicted at the ₹114.50 observed saving", s: "extrapolated beyond ₹100", color: C.warn },
    { v: V.inr(be.contrib_per_order, 2), k: "contribution per order", s: "₹30 revenue − ₹56.01 rider", color: C.crit },
    { v: V.inr(be.breakeven_rev, 2), k: "revenue per order needed to break even", s: "+" + be.uplift_needed_pct + "% on reported", color: C.crit },
    { v: "16 yrs", k: "category time to EBITDA break-even", s: "Eternal, the only one to get there" },
  ]);

  var g = "";

  /* ---- demand curve ---- */
  g += card("h7", "Predicted adoption at any recurring saving",
    "Logistic model fitted to the six observed staircase points. Solid inside the observed range, dashed beyond it.",
    V.scatter({
      data: dc.observed.map(function (p) {
        return { x: p.x, y: p.y, r: 7, color: C.s[1], tip: "Observed: ₹" + p.x + " → " + V.fmt(p.y, 1) + "% cumulative" };
      }).concat(dc.markers.map(function (m) {
        return { x: m.x, y: m.y, r: 8, color: C.s[2], label: m.label.split(" ")[0],
                 tip: m.label + "\nObserved saving ₹" + V.fmt(m.x, 2) + "\nPredicted adoption " + V.fmt(m.y, 1) + "%" };
      })),
      line: dc.curve.filter(function (p) { return p.x <= dc.max_observed_x; }),
      lineColor: C.s[0],
      w: 620, h: 300, xmin: 0, xmax: 200, ymin: 0, ymax: 100,
      xlab: "Recurring saving per order (₹)", ylab: "Cumulative % who would switch",
      fmtX: function (t) { return "₹" + V.fmt(t, 0); }, fmtY: function (t) { return V.fmt(t, 0) + "%"; }
    }),
    legend([{ name: "Observed staircase point", color: C.s[1] }, { name: "Fitted logistic", color: C.s[0] }, { name: "Observed saving at each checkout view", color: C.s[2] }]) +
    "<b>Fit</b> · logit(p) = " + dc.fit.b0 + " + " + dc.fit.b1 + "·saving · R² = " + dc.fit.r2 + ". " +
    "<b>Method</b> · Gabor-Granger style price-response, the standard technique for this question. " +
    "<b>Extrapolation warning</b> · " + V.esc(dc.extrapolation_warning) + " " +
    "<b>Base</b> · " + dc.n_named + " respondents who named a figure; " + dc.excluded_never + " said no amount would move them.");

  /* ---- profiling ---- */
  var pt = B.profiling.targets[0];
  g += card("h5", "Who is most likely to switch?",
    "Lift = subgroup rate ÷ overall rate for “" + pt.target + "”. Base rate " + V.pct(pt.base_pct) + ".",
    V.barH({
      data: pt.rows.slice(0, 9).map(function (r) {
        return { label: r.feature, value: r.pct, lo: r.lo, hi: r.hi,
                 vlabel: V.fmt(r.lift, 2) + "×",
                 color: r.lift >= 1.25 ? C.s[2] : (r.lift <= 0.75 ? C.crit : C.s[0]),
                 tip: r.feature + "\n" + r.k + " of " + r.n + " = " + V.fmt(r.pct, 1) + "%\nlift " + V.fmt(r.lift, 2) + "×\n95% CI " + r.lo + "–" + r.hi };
      }),
      max: 100, ref: pt.base_pct, w: 460, rowH: 32, labelW: 175,
      fmtAxis: function (t) { return V.fmt(t, 0) + "%"; }
    }),
    "<b>EXPLORATORY ONLY.</b> " + V.esc(B.profiling.note) + " Dashed line = overall base rate.");

  g += card("h7", "Profiling significance tests",
    "Fisher exact on each 2×2 contrast. None survives at n = 40 — reported rather than suppressed.",
    tableOf([
      { label: "Outcome", get: function (r) { return r.target; } },
      { label: "Feature", get: function (r) { return "<b>" + r.feature + "</b>"; } },
      { label: "In-group yes/no", n: 1, get: function (r) { return r.a + " / " + r.b; } },
      { label: "Out-group yes/no", n: 1, get: function (r) { return r.c + " / " + r.d; } },
      { label: "p", n: 1, get: function (r) { return r.p === null ? "—" : V.fmt(r.p, 3); } },
      { label: "Verdict", get: function (r) { return '<span class="pill ' + (r.p !== null && r.p < 0.05 ? "p-ok" : "p-na") + '">' + (r.p !== null && r.p < 0.05 ? "Significant" : "Not detectable") + "</span>"; } },
    ], B.profiling.tests),
    "This is the honest limit of a 40-person sample: we can measure the headline rate precisely enough to act on, but not the subgroup differences.");

  /* ---- break-even ---- */
  g += card("h6", "Contribution per order — the sign problem",
    "Contribution = revenue per order − rider payout, at three rider-cost assumptions.",
    V.lineChart({
      x: B.breakeven_grid.map(function (r) { return "₹" + r.rev; }),
      series: [
        { name: "Rider ₹45", color: C.s[2], values: B.breakeven_grid.map(function (r) { return r.contrib_at_45; }) },
        { name: "Rider ₹56.01 (industry)", color: C.s[0], values: B.breakeven_grid.map(function (r) { return r.contrib; }) },
        { name: "Rider ₹65", color: C.s[1], values: B.breakeven_grid.map(function (r) { return r.contrib_at_65; }) },
      ],
      w: 560, h: 260, min: -70, max: 45,
      fmtAxis: function (t) { return "₹" + V.fmt(t, 0); }, fmtTip: function (v) { return V.inr(v, 2); }
    }),
    legend([{ name: "Rider ₹45", color: C.s[2] }, { name: "Rider ₹56.01 (Swiggy FY24, FACT)", color: C.s[0] }, { name: "Rider ₹65", color: C.s[1] }]) +
    "<b>Ownly's only reported revenue figure is ₹30 per order.</b> At the industry rider payout that is <b>−₹26.01 per order</b> before marketing, support or overhead. Break-even revenue is <b>₹56.01</b>, an uplift of <b>" + be.uplift_needed_pct + "%</b>.");

  g += card("h6", "Which lever moves the outcome most?",
    "Monthly contribution swing when each lever is moved across a plausible range, others held at base.",
    V.tornado({
      data: B.tornado.map(function (t) {
        return { lever: t.lever, low: t.low, high: t.high, lo_val: t.lo_val, hi_val: t.hi_val,
                 color: (t.lever.indexOf("Revenue") >= 0 || t.lever.indexOf("Rider") >= 0) ? C.s[2] : C.s[0] };
      }),
      w: 560, labelW: 215, fmtAxis: function (t) { return "₹" + V.fmt(t / 1000, 0) + "k"; }
    }),
    legend([{ name: "Volume levers — move contribution the WRONG way while it is negative", color: C.s[0] }, { name: "Levers that can change the sign", color: C.s[2] }]) +
    "<b>Read this carefully.</b> " + V.esc(be.consequence));

  /* ---- scenario simulator ---- */
  g += card("", "Scenario simulator",
    "Every observed number in this workbook is fixed. These are <b>your</b> assumptions — change them and the model recomputes live.",
    scenarioUI(),
    "<b>Model</b> · users = catchment population × target share × P(switch | saving) × discovery × assortment fit. " +
    "Contribution = orders × (revenue − rider cost). <b>Excluded</b> · fixed costs, technology, support, overhead — so real break-even is strictly worse than shown. " +
    "<b>P(switch) comes from the fitted demand curve above.</b>");

  /* ---- benchmarks ---- */
  g += card("", "Unit-economics benchmarks used, and their provenance",
    "Only figures that are FACT-grade and common across the domain were adopted. Each is graded and sourced.",
    tableOf([
      { label: "Metric", get: function (r) { return "<b>" + r.metric + "</b>"; } },
      { label: "Value", n: 1, get: function (r) { return r.unit === "₹" ? V.inr(r.value, 2) : (r.unit === "$" ? "$" + V.fmt(r.value, 2) : V.fmt(r.value, 1) + " " + r.unit); } },
      { label: "Grade", get: function (r) { return '<span class="pill ' + (r.grade.indexOf("FACT") === 0 ? "p-ok" : r.grade.indexOf("CALC") === 0 ? "p-info" : "p-warn") + '">' + r.grade + "</span>"; } },
      { label: "Entity & series", get: function (r) { return r.entity + "<br><span style=\"color:var(--muted)\">" + r.series + "</span>"; } },
      { label: "Source", get: function (r) { return r.source; } },
      { label: "Why domain-wide", get: function (r) { return r.why_domain_wide; } },
    ], B.econ_benchmarks),
    "<b>Deliberately excluded</b> · CAC. Our own secondary research concludes there is <b>no credible, dated, primary-sourced CAC figure for Indian food delivery in the public domain</b> — neither DRHP discloses it. Advertising &amp; sales promotion per order is used as the named defensible proxy instead.");

  g += card("", "What this model is not", "",
    '<div class="callout warn"><p><b>Caveats carried forward from the sources:</b></p>' +
    B.breakeven.caveats.map(function (c) { return "<p>• " + V.esc(c) + "</p>"; }).join("") + '</div>', "");

  return g;
}

function scenarioUI() {
  var defs = [
    { k: "saving", label: "Recurring saving held", min: 0, max: 200, step: 5, unit: "₹" },
    { k: "coverage", label: "Usual-restaurant coverage", min: 10, max: 100, step: 5, unit: "%" },
    { k: "discovery", label: "Discovery rate", min: 5, max: 90, step: 5, unit: "%" },
    { k: "rev", label: "Revenue per order", min: 0, max: 120, step: 1, unit: "₹" },
    { k: "rider", label: "Rider cost per order", min: 20, max: 90, step: 1, unit: "₹" },
    { k: "cac", label: "Acquisition cost per user", min: 0, max: 200, step: 5, unit: "₹" },
    { k: "share", label: "Target share of catchment", min: 1, max: 30, step: 1, unit: "%" },
    { k: "opm", label: "Orders per user per month", min: 1, max: 12, step: 1, unit: "" },
  ];
  var h = '<div class="sliders">' + defs.map(function (d) {
    return '<div class="slider"><label for="sc-' + d.k + '">' + V.esc(d.label) +
      '<b id="scv-' + d.k + '">' + (d.unit === "₹" ? "₹" : "") + SC[d.k] + (d.unit === "%" ? "%" : "") + '</b></label>' +
      '<input type="range" id="sc-' + d.k + '" data-k="' + d.k + '" min="' + d.min + '" max="' + d.max + '" step="' + d.step + '" value="' + SC[d.k] + '">' +
      '<div class="rng"><span>' + (d.unit === "₹" ? "₹" : "") + d.min + '</span><span>' + (d.unit === "₹" ? "₹" : "") + d.max + (d.unit === "%" ? "%" : "") + '</span></div></div>';
  }).join("") + '</div><div id="sc-out"></div>';
  return h;
}

function scenarioCompute() {
  var pop = B.econ_defaults.catchment_pop;
  var adopt = logistic(SC.saving);
  var users = pop * (SC.share / 100) * adopt * (SC.discovery / 100) * (SC.coverage / 100);
  var orders = users * SC.opm;
  var cpo = SC.rev - SC.rider;
  var monthly = orders * cpo;
  var cacTotal = users * SC.cac;
  var payback = cpo > 0 ? (SC.cac / cpo) / SC.opm : null;
  return { adopt: adopt, users: users, orders: orders, cpo: cpo, monthly: monthly, cacTotal: cacTotal, payback: payback };
}

function scenarioRender() {
  var r = scenarioCompute(), el = document.getElementById("sc-out");
  if (!el) return;
  var neg = r.cpo < 0;
  el.innerHTML =
    '<div class="outs">' +
    out(V.pct(100 * r.adopt), "would switch at this saving", null) +
    out(V.cnt(Math.round(r.users)), "reachable users in catchment", null) +
    out(V.cnt(Math.round(r.orders)), "orders per month", null) +
    out(V.inr(r.cpo, 2), "contribution per order", neg ? C.crit : C.good) +
    out(V.inr(Math.round(r.monthly)), "monthly contribution", r.monthly < 0 ? C.crit : C.good) +
    out(r.payback === null ? "Never" : V.fmt(r.payback, 1) + " mo", "CAC payback", r.payback === null ? C.crit : C.good) +
    '</div>' +
    (neg
      ? '<div class="callout bad"><p><b>Contribution per order is negative (' + V.inr(r.cpo, 2) + ').</b> Every additional order increases the loss, so growth levers — discovery, coverage, saving held — make monthly contribution <b>worse</b>. Raise revenue per order above ' + V.inr(SC.rider, 2) + ', or lower rider cost below ' + V.inr(SC.rev, 2) + ', before spending anything on growth.</p></div>'
      : '<div class="callout"><p><b>Contribution per order is positive (' + V.inr(r.cpo, 2) + ').</b> Growth levers now compound: each additional order adds contribution, and acquisition pays back in ' + V.fmt(r.payback, 1) + ' months at the current CAC assumption.</p></div>');
}
function out(v, k, color) {
  return '<div class="out"><span class="v"' + (color ? ' style="color:' + color + '"' : "") + '>' + v + '</span><span class="k">' + V.esc(k) + '</span></div>';
}

/* ═══════════════════════════════════════════════════════════════════
   WORKSHEET 7 — METHOD & EVIDENCE
   ═══════════════════════════════════════════════════════════════════ */
function method() {
  kpis([
    { v: V.cnt(B.meta.n_received), k: "survey responses received", s: B.meta.n_clean + " passed quality checks" },
    { v: B.meta.n_catchment, k: "in the Gachibowli catchment", s: "the analysis base" },
    { v: B.meta.n_audit_captures, k: "price captures", s: "across 3 platforms" },
    { v: V.cnt(B.meta.n_text), k: "public documents coded", s: "3 independent sources" },
    { v: "9", k: "formal hypothesis tests", s: "3 reject · 5 null · 1 not testable" },
    { v: "19", k: "metrics marked NOT ESTIMABLE", s: "9 KPIs + 10 marketing metrics" },
  ]);

  var g = "";

  g += card("h7", "Evidence triangulation",
    "Which sources speak to which question. A claim resting on one column is weaker than one resting on four.",
    V.heatmap({
      rows: B.evidence_matrix.map(function (r) { return r.dimension; }),
      cols: ["survey", "interviews", "price_audit", "app_reviews", "social", "secondary_research", "challenger_history"],
      get: function (r, c) {
        var row = B.evidence_matrix.find(function (x) { return x.dimension === r; });
        var v = (row[c] || "").trim();
        return v === "" || v === "—" ? null : v;
      },
      color: function (v) {
        var s = String(v).toUpperCase();
        if (s.indexOf("STRONG") >= 0) return "#7fc39b";
        if (s.indexOf("MODERATE") >= 0) return "#bfe0cf";
        if (s.indexOf("CONTRADICT") >= 0) return "#eda6a6";
        if (s.indexOf("WEAK") >= 0 || s.indexOf("DIRECTIONAL") >= 0) return "#f5e3b8";
        return "#e4ecf3";
      },
      label: function (v) { return String(v).slice(0, 3); },
      tip: function (r, c, v) { return r + "\n" + c.replace(/_/g, " ") + ": " + v; },
      w: 700, labelW: 232, headH: 96, cellH: 28
    }),
    legend([{ name: "Strong", color: "#7fc39b" }, { name: "Moderate", color: "#bfe0cf" }, { name: "Directional / weak", color: "#f5e3b8" }, { name: "Contradicted", color: "#eda6a6" }, { name: "Present", color: "#e4ecf3" }]) +
    "<b>Source</b> · evidence_matrix.csv. Hover any cell for the full assessment.");

  g += card("h5", "Research funnel",
    "How 124 responses became an analysis base of 40. Nothing was deleted — excluded rows carry flags.",
    V.funnel({
      data: B.funnel_research.slice(0, 4).map(function (s, i) {
        return { label: s.stage, value: 100 * s.n / B.funnel_research[0].n, k: s.n, n: B.funnel_research[0].n };
      }), w: 430
    }),
    "The study is about one catchment. A larger n of the wrong people would be worse, not better.");

  g += card("", "Hypothesis register",
    "Every test specified in the pre-analysis plan, including the five that found nothing.",
    tableOf([
      { label: "Hypothesis", get: function (r) { return "<b>" + String(r.statement || "").slice(0, 150) + "</b>"; } },
      { label: "Test", get: function (r) { return r.test; } },
      { label: "n", n: 1, get: function (r) { return r.n; } },
      { label: "p", n: 1, get: function (r) { return r.p_value || "—"; } },
      { label: "Verdict", get: function (r) { return '<span class="pill ' + (String(r.verdict).indexOf("FAIL") >= 0 ? "p-na" : String(r.verdict).indexOf("NOT") >= 0 ? "p-warn" : "p-ok") + '">' + r.verdict + "</span>"; } },
    ], B.hypotheses),
    "<b>Pre-registration</b> · plan frozen at 09_analysis/PAP_frozen_2026-09-21.md with a provenance block separating git-dated sections (committed 2026-09-14, before the instrument went live) from later additions whose pre-data status rests on the project log alone.");

  g += card("h6", "Marketing metrics computed",
    "Ten metrics. Three are definitions we constructed because the standard formula sheet had no metric for the question.",
    tableOf([
      { label: "ID", get: function (r) { return r.metric_id; } },
      { label: "Metric", get: function (r) { return "<b>" + r.metric_name + "</b>"; } },
      { label: "Value", n: 1, get: function (r) { return r.value + (r.unit === "%" ? "%" : " " + r.unit); } },
      { label: "Basis", get: function (r) { return r.formula_sheet_reference; } },
    ], B.marketing_metrics),
    "<b>MM1 Switch-Threshold Coverage</b> is the study's central number: it answers “is the saving big enough <i>for these people</i>”, not merely “is Ownly cheaper”.");

  g += card("h6", "Marked NOT ESTIMABLE",
    "Listed with a reason instead of filled in with a plausible-looking number.",
    tableOf([
      { label: "Metric", get: function (r) { return "<b>" + r.metric + "</b>"; } },
      { label: "Sheet", get: function (r) { return r.formula_sheet; } },
      { label: "Why not computable", get: function (r) { return r.why_not_computable; } },
    ], B.not_estimable),
    "<b>The finding inside the gap</b> · the metrics that determine whether Ownly survives — retention, CLV, CAC, contribution margin, market share — are precisely the ones no external researcher can see.");

  g += card("", "Data-quality register",
    "Anomalies found during cleaning and exactly how each was handled.",
    tableOf([
      { label: "Anomaly", get: function (r) { return "<b>" + r.anomaly + "</b>"; } },
      { label: "What we found", get: function (r) { return r.what_we_found; } },
      { label: "How it was handled", get: function (r) { return r.how_it_was_handled; } },
    ], B.anomalies),
    "");

  g += card("", "Analytics applied, and the honest confidence on each",
    "",
    tableOf([
      { label: "Layer", get: function (r) { return "<b>" + r[0] + "</b>"; } },
      { label: "Technique", get: function (r) { return r[1]; } },
      { label: "Applied to", get: function (r) { return r[2]; } },
      { label: "Confidence", get: function (r) { return '<span class="pill ' + r[3] + '">' + r[4] + "</span>"; } },
    ], [
      ["Descriptive", "Proportions with Wilson intervals, funnels, distributions, box plots, share-of-wallet", "Survey n=40, audit, 836 documents", "p-ok", "High"],
      ["Diagnostic", "McNemar exact (paired), Fisher exact, Spearman correlation, waterfall decomposition, fee-load attribution", "Survey, audit", "p-ok", "High on the headline; null elsewhere"],
      ["Predictive", "Logistic price-response curve (Gabor-Granger), R² = " + B.demand_curve.fit.r2, "6 staircase points", "p-ok", "Good in range, extrapolated above ₹100"],
      ["Predictive", "Switcher profiling by lift + Fisher tests", "Survey n=40", "p-warn", "Exploratory — underpowered"],
      ["Predictive", "Sentiment and volume trend across 16 months", "836 dated documents", "p-info", "Descriptive trend; no forecast claimed"],
      ["Prescriptive", "Scenario simulator, tornado sensitivity, break-even solve", "Fitted curve + FACT-grade benchmarks", "p-info", "Assumption-driven, user-adjustable"],
      ["Text / cognitive", "Lexicon sentiment, negation-aware; validated ρ = " + B.sentiment_vs_star.spearman.rho + " vs stars", "836 documents", "p-ok", "Validated against an independent label"],
      ["Text / cognitive", "TF-IDF term salience, theme roll-up, co-occurrence", "836 documents, 119 codes", "p-info", "Light topic modelling"],
    ]),
    "<b>Not attempted, and why</b> · time-series forecasting (no transactional history), classification with train/test split (n = 40 cannot support it), market-share modelling (no market-size denominator exists). Claiming any of these would have been decoration, not analysis.");

  return g;
}

/* ═══════════════════════════════════════════════════════════════════
   SHELL
   ═══════════════════════════════════════════════════════════════════ */
var TABS = [
  { id: "exec",    name: "Executive overview", title: "Executive overview",
    sub: "The decision, the evidence behind it, and the constraint underneath it.", fn: exec },
  { id: "price",   name: "Price & value", title: "Price & value",
    sub: "What Ownly actually charges, how the advantage is built, and where it erodes.", fn: price },
  { id: "demand",  name: "Demand & segments", title: "Demand & segments",
    sub: "What the catchment will trade, what it demands to switch, and how subgroups differ.", fn: demand },
  { id: "voc",     name: "Voice of customer", title: "Voice of customer",
    sub: "836 documents across 16 months — sentiment, themes, vocabulary and verbatims.", fn: voc },
  { id: "compete", name: "Competitive position", title: "Competitive position",
    sub: "Assortment overlap, the Bengaluru benchmark, and the challenger failure record.", fn: compete },
  { id: "predict", name: "Predictive & scenarios", title: "Predictive & scenarios",
    sub: "A fitted demand curve, switcher profiling, break-even economics and a live scenario model.", fn: predict },
  { id: "method",  name: "Method & evidence", title: "Method & evidence",
    sub: "Triangulation, the hypothesis register, what was not estimable, and the confidence on every technique.", fn: method },
];

function kpis(list) {
  document.getElementById("kstrip").innerHTML = list.map(function (k) {
    return '<div class="kcard' + (k.na ? " na" : "") + '"><span class="v"' + (k.color ? ' style="color:' + k.color + '"' : "") + '>' +
      k.v + '</span><span class="k">' + V.esc(k.k) + '</span>' + (k.s ? '<span class="s">' + V.esc(k.s) + '</span>' : "") + '</div>';
  }).join("");
}

function render() {
  var t = TABS.find(function (x) { return x.id === TAB; });
  $("#t-title").textContent = t.title;
  $("#t-sub").textContent = t.sub;
  document.getElementById("grid").innerHTML = t.fn();
  Array.prototype.forEach.call(document.querySelectorAll("#nav a"), function (a) {
    a.classList.toggle("on", a.dataset.id === TAB);
  });
  var rs = rows();
  $("#fstat").innerHTML = "<b>" + rs.length + "</b> of " + B.rows.length + " respondents selected" +
    (filtered() ? "<br>Filter is active." : "<br>No filter applied.");
  if (TAB === "predict") {
    scenarioRender();
    Array.prototype.forEach.call(document.querySelectorAll("#sc-out, .slider input"), function () {});
    Array.prototype.forEach.call(document.querySelectorAll(".slider input[type=range]"), function (inp) {
      inp.addEventListener("input", function () {
        var k = inp.dataset.k; SC[k] = +inp.value;
        var lab = document.getElementById("scv-" + k);
        if (lab) lab.textContent = (k === "saving" || k === "rev" || k === "rider" || k === "cac" ? "₹" : "") + inp.value + (k === "coverage" || k === "discovery" || k === "share" ? "%" : "");
        scenarioRender();
      });
    });
  }
  wireSorting();
  document.getElementById("main").scrollTop = 0;
}

/* Click a column header to sort that table — numeric-aware, toggles direction. */
function wireSorting() {
  Array.prototype.forEach.call(document.querySelectorAll(".card table"), function (tbl) {
    var ths = tbl.querySelectorAll("thead th");
    Array.prototype.forEach.call(ths, function (th, idx) {
      th.addEventListener("click", function () {
        var body = tbl.querySelector("tbody");
        var trs = Array.prototype.slice.call(body.querySelectorAll("tr"));
        var dir = th.dataset.dir === "asc" ? -1 : 1;
        Array.prototype.forEach.call(ths, function (o) { delete o.dataset.dir; o.textContent = o.textContent.replace(/ [▲▼]$/, ""); });
        th.dataset.dir = dir === 1 ? "asc" : "desc";
        th.textContent = th.textContent.replace(/ [▲▼]$/, "") + (dir === 1 ? " ▲" : " ▼");
        var key = function (tr) {
          var td = tr.children[idx];
          if (!td) return "";
          var t = (td.textContent || "").trim();
          var n = parseFloat(t.replace(/[₹,%×\s]/g, "").replace(/−/g, "-"));
          return isNaN(n) ? t.toLowerCase() : n;
        };
        trs.sort(function (a, b) {
          var ka = key(a), kb = key(b);
          if (typeof ka === "number" && typeof kb === "number") return (ka - kb) * dir;
          return String(ka) < String(kb) ? -dir : String(ka) > String(kb) ? dir : 0;
        });
        trs.forEach(function (tr) { body.appendChild(tr); });
      });
    });
  });
}

function init() {
  document.getElementById("built").textContent = "built " + B.meta.built;
  document.getElementById("nav").innerHTML = TABS.map(function (t, i) {
    return '<a href="#' + t.id + '" data-id="' + t.id + '"><span class="ic">' + (i + 1) + '</span>' + V.esc(t.name) + '</a>';
  }).join("");
  document.getElementById("nav").addEventListener("click", function (e) {
    var a = e.target.closest("a"); if (!a) return;
    e.preventDefault(); TAB = a.dataset.id; location.hash = TAB; render();
  });
  [["#f-occ", "occ"], ["#f-mem", "mem"], ["#f-multi", "multi"], ["#f-rap", "rap"], ["#f-aware", "aware"]].forEach(function (p) {
    $(p[0]).addEventListener("change", function () { F[p[1]] = this.value; render(); });
  });
  $("#freset").addEventListener("click", function () {
    F = { occ: "", mem: "", multi: "", rap: "", aware: "" };
    ["#f-occ", "#f-mem", "#f-multi", "#f-rap", "#f-aware"].forEach(function (s) { $(s).value = ""; });
    render();
  });
  var h = (location.hash || "").replace("#", "");
  if (TABS.some(function (t) { return t.id === h; })) TAB = h;
  V.initTooltip();
  render();
}

if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
else init();
})();
