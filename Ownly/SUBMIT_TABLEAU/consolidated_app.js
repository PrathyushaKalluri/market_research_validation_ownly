/* ═══════════════════════════════════════════════════════════════════
   Ownly Gachibowli — consolidated dashboard.
   Renders every Tableau worksheet plus the Python-only analyses,
   from the same ./Data CSVs the .twbx is built on.
   ═══════════════════════════════════════════════════════════════════ */
(function () {
"use strict";
var D = window.CD, V = window.VZ, C = V.C;

/* ---------- data helpers ---------- */
function T(name) { return D[name] || []; }
function where(name, fn) { return T(name).filter(fn); }
function num(v) { return (v === null || v === undefined || isNaN(v)) ? null : +v; }
function sum(rows, k) { return rows.reduce(function (a, r) { return a + (num(r[k]) || 0); }, 0); }
function uniq(rows, k) { var s = []; rows.forEach(function (r) { if (s.indexOf(r[k]) < 0) s.push(r[k]); }); return s; }
function by(rows, k) {
  var m = {}; rows.forEach(function (r) { (m[r[k]] = m[r[k]] || []).push(r); }); return m;
}

/* ---------- card builders ---------- */
var OUT = [];
function sec(id, n, title, lede) {
  OUT.push('<section class="sec" id="' + id + '"><div class="eyebrow">' + n + '</div>' +
           '<h2>' + V.esc(title) + '</h2>' +
           (lede ? '<p class="lede prose">' + lede + '</p>' : '') + '<div class="grid">');
}
function endsec() { OUT.push('</div></section>'); }

/* badge: where this visual lives */
function bTab(sheet) { return '<span class="badge b-tab">Tableau ' + V.esc(sheet) + '</span>'; }
function bPy() { return '<span class="badge b-py">Python only</span>'; }
function bBoth(sheet) { return '<span class="badge b-both">Tableau ' + V.esc(sheet) + ' · Python-computed</span>'; }

function card(cls, title, badge, sub, body, note) {
  OUT.push('<section class="card ' + (cls || '') + '">' +
    '<div class="hd"><h3>' + V.esc(title) + '</h3>' + (badge || '') + '</div>' +
    (sub ? '<p class="sub">' + sub + '</p>' : '') + body +
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
function kstrip(items, el) {
  var h = items.map(function (k) {
    return '<div class="kc"><span class="v"' + (k.color ? ' style="color:' + k.color + '"' : '') + '>' +
      k.v + '</span><span class="k">' + V.esc(k.k) + '</span>' +
      (k.s ? '<span class="s">' + V.esc(k.s) + '</span>' : '') + '</div>';
  }).join('');
  if (el) document.getElementById(el).innerHTML = h;
  return '<div class="kstrip" style="margin-top:0">' + h + '</div>';
}

/* ═══════════════════ TOP STRIP ═══════════════════ */
var kpi = T("01_kpi_summary");
var notComp = kpi.filter(function (r) { return r["Not Computable"] === "Yes"; }).length;
kstrip([
  { v: "40", k: "survey respondents in catchment", s: "124 received" },
  { v: "836", k: "public documents analysed", s: "16 months, 3 sources" },
  { v: "₹114.50", k: "median saving Ownly delivers", s: "4 of 4 matched baskets" },
  { v: "35.0%", k: "will give up usual restaurants for ₹30", s: "the binding constraint", color: C.crit },
  { v: "−₹26.01", k: "contribution per order at reported economics", s: "₹30 revenue − ₹56.01 rider", color: C.crit },
  { v: notComp + " of " + kpi.length, k: "KPIs marked NOT COMPUTABLE", s: "reason stated for each" },
], "topstrip");

/* ═══════════════════ 1 · PROBLEM STATEMENT ═══════════════════ */
sec("s1", "Section 1", "Problem statement",
  "Why the obvious question — <i>will anyone try it?</i> — is the wrong one, and what we set out to answer instead.");

card("c7", "Business problem", bTab("1.1"),
  "The decision this study serves, stated in full.",
  '<div class="prose">' + T("39_problem_statement")
    .sort(function (a, b) { return a.Order - b.Order; })
    .map(function (r) {
      return '<div class="blk"><div class="h">' + V.esc(r.Section) + '</div><div class="t">' + V.esc(r.Content) + '</div></div>';
    }).join('') + '</div>',
  "<b>Source</b> · 39_problem_statement.csv");

card("c5", "Research funnel", bTab("1.2"),
  "How 124 responses became an analysis base of 40. Nothing was deleted — excluded rows carry flags.",
  (function () {
    var f = where("10_funnels", function (r) { return r.Funnel === "Research sample"; })
      .sort(function (a, b) { return a["Stage Order"] - b["Stage Order"]; });
    var top = f.length ? f[0].N : 1;
    return V.funnel({ data: f.map(function (r) {
      return { label: r.Stage, value: 100 * r.N / top, k: r.N, n: top };
    }), w: 470 });
  })(),
  "<b>Source</b> · 10_funnels.csv. The study is about one catchment; a larger n of the wrong people would be worse, not better.");

card("", "Analytics applied, and where each layer runs", bTab("1.3"),
  "Every technique used in this study, what computed it, and the honest confidence on each.",
  tbl([
    { label: "Layer", get: function (r) { return "<b>" + V.esc(r["Analytics Layer"]) + "</b>"; } },
    { label: "Technique", get: function (r) { return V.esc(r.Technique); } },
    { label: "Applied to", get: function (r) { return V.esc(r["Applied To"]); } },
    { label: "Computed in", get: function (r) {
        var p = r["Computed In"] === "Python" ? "b-py" : "b-tab";
        return '<span class="badge ' + p + '">' + V.esc(r["Computed In"]) + "</span>"; } },
    { label: "Drawn in Tableau", get: function (r) { return V.esc(r["Drawn In Tableau"]); } },
    { label: "Confidence", get: function (r) { return V.esc(r.Confidence); } },
  ], T("37_analytics_layers")),
  "<b>The split that matters</b> · Tableau draws every chart in this study natively. It cannot <i>compute</i> logistic fits, sentiment, TF-IDF or exact tests — Python does those and stores the result as a column.");
endsec();

/* ═══════════════════ 2 · KPIs ═══════════════════ */
sec("s2", "Section 2", "KPIs",
  "One north star, seven drivers, and an honest column for what cannot be measured from outside the company.");

card("c7", "Headline KPIs", bBoth("2.1"),
  "The KPIs flagged as headline, with 95% Wilson confidence intervals where the metric is a proportion.",
  (function () {
    var h = kpi.filter(function (r) { return r["Is Headline"] === "Yes" && num(r.Value) !== null; });
    return V.barH({
      data: h.map(function (r) {
        return { label: r["KPI Name"], value: num(r.Value),
                 lo: num(r["CI Low"]), hi: num(r["CI High"]),
                 vlabel: V.fmt(r.Value, 1) + (r.Unit === "%" ? "%" : ""),
                 color: C.s[0],
                 tip: r["KPI Name"] + "\n" + r.Value + " " + (r.Unit || "") +
                      (num(r["CI Low"]) !== null ? "\n95% CI " + r["CI Low"] + "–" + r["CI High"] : "") +
                      "\nBase: " + (r.Base || "—") };
      }),
      w: 640, rowH: 34, labelW: 250, fmtAxis: function (t) { return V.fmt(t, 0); }
    });
  })(),
  "<b>Wilson intervals are Python-computed</b> and stored as columns, so Tableau draws them as reference bands. <b>Source</b> · 01_kpi_summary.csv");

card("c5", "KPI coverage — what we can and cannot measure", bTab("2.2"),
  "Of " + kpi.length + " specified KPIs, " + notComp + " require Ownly's or Rapido's internal data.",
  V.donut({
    data: [
      { label: "Computed", value: kpi.length - notComp, color: C.s[2] },
      { label: "Not computable", value: notComp, color: "#c9d1d8" },
    ], size: 200, center: (kpi.length - notComp) + "/" + kpi.length, centerSub: "computed"
  }) +
  V.barH({
    data: (function () {
      var g = by(kpi, "Layer");
      return Object.keys(g).map(function (k) {
        var nc = g[k].filter(function (r) { return r["Not Computable"] === "Yes"; }).length;
        return { label: k + " (" + g[k].length + ")", value: g[k].length - nc, vlabel: (g[k].length - nc) + " computed",
                 color: C.s[2], tip: k + ": " + (g[k].length - nc) + " computed, " + nc + " not computable" };
      });
    })(), w: 400, rowH: 26, labelW: 150, fmtAxis: function (t) { return V.fmt(t, 0); }
  }),
  "<b>Not a gap in the research</b> — retention, CLV, CAC and contribution margin cannot be seen from outside the company by anyone.");

card("c6", "Adoption funnel", bBoth("2.3"),
  "Share of the 40 catchment respondents. Intervals widen sharply as the base shrinks.",
  (function () {
    var f = where("10_funnels", function (r) { return r.Funnel === "Ownly adoption"; })
      .sort(function (a, b) { return a["Stage Order"] - b["Stage Order"]; });
    return V.funnel({ data: f.map(function (r) {
      return { label: r.Stage, value: num(r.Pct), k: r.N, n: 40 };
    }), w: 520 });
  })(),
  "<b>Read the last row carefully</b> · trial is 2 respondents of 40, 95% CI 1.4–16.5%. The 4-week window mostly predates Ownly's Hyderabad rollout.");

card("c6", "North star and guardrail", bPy(),
  "The two metrics that decide whether this business works — neither is computable from outside.",
  tbl([
    { label: "KPI", get: function (r) { return "<b>" + V.esc(r["KPI Name"]) + "</b>"; } },
    { label: "Layer", get: function (r) { return V.esc(r.Layer); } },
    { label: "Status", get: function (r) { return '<span class="pill p-na">' + V.esc(r.Status) + "</span>"; } },
    { label: "Why", get: function (r) { return V.esc(String(r.Limitation || "").slice(0, 180)); } },
  ], kpi.filter(function (r) { return r.Layer === "NORTH STAR" || r.Layer === "GUARDRAIL"; })),
  "<b>Uber Eats India lost $2.55 per order against a $2.45 order value</b> — it lost more per order than the order was worth. Any repeat rate is meaningless without the guardrail.");

card("", "Full KPI register", bTab("2.4"),
  "All " + kpi.length + " KPIs with formula, base, evidence grade and limitation.",
  tbl([
    { label: "ID", get: function (r) { return r["KPI ID"]; } },
    { label: "KPI", get: function (r) { return "<b>" + V.esc(r["KPI Name"]) + "</b>"; } },
    { label: "Layer", get: function (r) { return V.esc(r.Layer); } },
    { label: "Driver", get: function (r) { return V.esc(r.Driver); } },
    { label: "Value", n: 1, get: function (r) { return num(r.Value) === null ? "—" : V.fmt(r.Value, 1) + (r.Unit === "%" ? "%" : ""); } },
    { label: "95% CI", n: 1, get: function (r) { return num(r["CI Low"]) === null ? "—" : r["CI Low"] + "–" + r["CI High"]; } },
    { label: "Status", get: function (r) {
        var cls = r["Not Computable"] === "Yes" ? "p-na" : "p-ok";
        return '<span class="pill ' + cls + '">' + V.esc(r.Status) + "</span>"; } },
    { label: "Evidence", get: function (r) { return V.esc(r["Evidence Type"]); } },
  ], kpi),
  "<b>Source</b> · 01_kpi_summary.csv");
endsec();

/* ═══════════════════ 3 · MARKETING METRICS ═══════════════════ */
sec("s3", "Section 3", "Marketing metrics",
  "Ten metrics computed from our own evidence. Ten more listed with a reason rather than filled in with a plausible-looking number.");

card("c7", "Metrics computed", bTab("3.1"),
  "Three are definitions we constructed, because the standard formula sheet has no metric for the question actually at issue.",
  V.barH({
    data: T("02_marketing_metrics").map(function (r) {
      var own = r["Our Own Definition"] === "Yes";
      return { label: r["Metric ID"] + " · " + r["Metric Name"], value: num(r.Value),
               vlabel: V.fmt(r.Value, 1) + (r.Unit === "%" ? "%" : " " + (r.Unit || "")),
               color: own ? C.s[1] : C.s[0],
               tip: r["Metric Name"] + "\n" + r.Value + " " + (r.Unit || "") + "\n\n" +
                    (r.Formula || "") + "\n\nCaveat: " + (r.Caveat || "—") };
    }), w: 620, rowH: 30, labelW: 265, fmtAxis: function (t) { return V.fmt(t, 0); }
  }),
  legend([{ name: "Our own definition", color: C.s[1] }, { name: "Standard formula sheet", color: C.s[0] }]) +
  "<b>MM1 Switch-Threshold Coverage</b> is the study's central number: it answers “is the saving big enough <i>for these people</i>”, not merely “is Ownly cheaper”. Hover any bar for its formula and caveat.");

card("c5", "Marked NOT ESTIMABLE", bTab("3.2"),
  "Every one requires Ownly's or Rapido's internal transaction or cost data.",
  tbl([
    { label: "Metric", get: function (r) { return "<b>" + V.esc(r.Metric) + "</b>"; } },
    { label: "Sheet", get: function (r) { return V.esc(r["Formula Sheet"]); } },
    { label: "Why not computable", get: function (r) { return V.esc(r["Why Not Computable"]); } },
  ], T("03_not_estimable")),
  "<b>The finding inside the gap</b> · the metrics that determine whether Ownly survives are precisely the ones no external researcher can see.");
endsec();

/* ═══════════════════ 4 · ANALYTICS ═══════════════════ */
sec("s4", "Section 4", "Analytics",
  "Descriptive, diagnostic, predictive and text analytics — the evidence behind every recommendation in section 5.");

/* — 4a trade-off — */
card("c7", "The ₹30 trade-off", bBoth("4.1"),
  "Same ₹30 saving, three different sacrifices, same 40 respondents. Whiskers are 95% Wilson intervals.",
  V.barH({
    data: T("04_tradeoffs").sort(function (a, b) { return a["Sort Order"] - b["Sort Order"]; })
      .map(function (r) {
        return { label: r.Description, value: num(r["Accept Pct"]),
                 lo: num(r["CI Low"]), hi: num(r["CI High"]),
                 vlabel: V.fmt(r["Accept Pct"], 1) + "%",
                 color: r["Is Constraint"] === "Yes" ? C.s[1] : C.s[0],
                 tip: r.Description + "\n" + r["Accepted K"] + " of " + r["Base N"] +
                      " = " + r["Accept Pct"] + "%\n95% CI " + r["CI Low"] + "–" + r["CI High"] };
      }),
    max: 100, ref: 50, w: 640, rowH: 44, labelW: 235,
    fmtAxis: function (t) { return V.fmt(t, 0) + "%"; }
  }),
  "<b>Dashed line = a coin flip.</b> Only the restaurants row falls below it. " + legend([{ name: "Not a constraint", color: C.s[0] }, { name: "The binding constraint", color: C.s[1] }]));

card("c5", "Is that gap real? — McNemar exact", bBoth("4.2"),
  "Paired test: considers only respondents who switched their answer between two scenarios.",
  tbl([
    { label: "Comparison", get: function (r) { return "<b>" + V.esc(r.Comparison) + "</b>"; } },
    { label: "A not B", n: 1, get: function (r) { return r["Discordant A Only"]; } },
    { label: "B not A", n: 1, get: function (r) { return r["Discordant B Only"]; } },
    { label: "p", n: 1, get: function (r) { return num(r["P Value"]) < 0.001 ? Number(r["P Value"]).toExponential(1) : V.fmt(r["P Value"], 4); } },
    { label: "Result", get: function (r) {
        return '<span class="pill ' + (r["Significant at 0.05"] === "Yes" ? "p-bad" : "p-na") + '">' +
          (r["Significant at 0.05"] === "Yes" ? "Reject H₀" : "Fail to reject") + "</span>"; } },
  ], T("05_tradeoff_tests")),
  "<b>24 to 1.</b> A split that lopsided happens by chance about once in 670,000 times. <b>Tableau cannot compute an exact test</b> — Python did, and the p-values are stored as columns. <b>Honest caveat</b> · the third row (p = 0.021) would not survive a strict multiple-comparison correction.");

/* — 4b price — */
card("c6", "Where the price advantage goes", bTab("4.3"),
  "Share of person × restaurant pairs where Ownly's saving clears that person's own stated switching bar.",
  V.waterfall({
    data: [
      { label: "List price", value: 81.1 },
      { label: "Membership effect", value: -25.0 },
      { label: "Coupon effect", value: -28.8 },
      { label: "After coupon", total: true },
    ], w: 480, h: 280, fmtAxis: function (t) { return V.fmt(t, 0) + "%"; }
  }),
  "<b>Source</b> · 09_price_erosion.csv · 132 pairs (33 respondents naming a figure × 4 baskets). After a rival coupon the median saving is <b>−₹28.07</b> — Ownly is dearer.");

card("c6", "Matched basket comparison", bTab("4.4"),
  "Identical items, same address, same 20-minute window, 16 Sep 2026. No coupon on either side.",
  (function () {
    var rows = where("07b_price_by_platform_long", function (r) { return r["Price View"] === "LIST+FEES"; });
    var rests = uniq(rows, "Restaurant");
    var plats = uniq(rows, "Platform");
    return V.barGrouped({
      cats: rests,
      series: plats.map(function (p, i) {
        return { name: p, color: p === "Ownly" ? C.s[2] : C.s[i === 0 ? 1 : 3],
                 values: rests.map(function (rst) {
                   var m = rows.filter(function (r) { return r.Restaurant === rst && r.Platform === p; });
                   return m.length ? num(m[0]["Final Payable Rs"]) : 0;
                 }) };
      }), w: 520, h: 250
    }) + legend(plats.map(function (p, i) {
      return { name: p, color: p === "Ownly" ? C.s[2] : C.s[i === 0 ? 1 : 3] };
    }));
  })(),
  "<b>Ownly was cheapest in 4 of 4.</b> Median saving ₹114.50 (30.5%). <b>Limitation</b> · one address, one dinner slot, n = 4.");

card("c6", "Bill composition — where the money goes", bTab("4.5"),
  "Median share of the final bill by component, zero-discount captures only.",
  (function () {
    var g = by(T("08_bill_composition_long"), "Platform");
    return V.stacked100({
      data: Object.keys(g).map(function (p) {
        return { label: p, parts: g[p].map(function (r, i) {
          return { name: r.Component, value: num(r["Pct Of Bill"]),
                   color: r["Component Group"] === "Food" ? C.s[2] : C.s[[1, 3, 0, 4, 7][i % 5]] };
        }) };
      }), w: 520, labelW: 80
    });
  })(),
  legend([{ name: "Food", color: C.s[2] }, { name: "Fees & tax", color: C.s[1] }]) +
  "<b>The structural point</b> · Ownly's advantage is mostly <i>not</i> a lower menu price — it is fees it does not charge. A discount can be withdrawn; a fee never charged cannot.");

card("c6", "Delivery time by restaurant", bTab("4.16"),
  "Quoted ETA midpoint at checkout.",
  (function () {
    var rows = T("23_eta_by_platform_long");
    var rests = uniq(rows, "Restaurant"), plats = uniq(rows, "Platform");
    return V.barGrouped({
      cats: rests,
      series: plats.map(function (p, i) {
        return { name: p, color: p === "Ownly" ? C.s[2] : C.s[i === 0 ? 1 : 3],
                 values: rests.map(function (rst) {
                   var m = rows.filter(function (r) { return r.Restaurant === rst && r.Platform === p; });
                   return m.length ? num(m[0]["Quoted ETA Min"]) : 0;
                 }) };
      }), w: 520, h: 240
    }) + legend(plats.map(function (p, i) {
      return { name: p, color: p === "Ownly" ? C.s[2] : C.s[i === 0 ? 1 : 3] };
    }));
  })(),
  "The penalty is <b>flat across unrelated brands</b> (+17.5 to +24 min) — the signature of fulfilling from a more distant outlet. <b>Mechanism inferred, not shown</b>: outlet distances were not recorded.");

card("", "Every matched basket, all three price views", bPy(),
  "The full audit result. 'Ownly wins' means its final payable was lowest.",
  tbl([
    { label: "Restaurant", get: function (r) { return "<b>" + V.esc(r.Restaurant) + "</b>"; } },
    { label: "View", get: function (r) { return V.esc(r["Price View"]); } },
    { label: "Ownly", n: 1, get: function (r) { return V.inr(r["Ownly Payable"], 2); } },
    { label: "Cheapest rival", n: 1, get: function (r) { return V.inr(r["Cheapest Rival Payable"], 2); } },
    { label: "Rival", get: function (r) { return V.esc(r["Cheapest Rival"]); } },
    { label: "Saving", n: 1, get: function (r) { return V.inr(r["Saving Rs"], 2); } },
    { label: "Saving %", n: 1, get: function (r) { return V.fmt(r["Saving Pct"], 1) + "%"; } },
    { label: "ETA gap", n: 1, get: function (r) { return "+" + V.fmt(r["ETA Gap Min"], 0) + " min"; } },
    { label: "Result", get: function (r) {
        return '<span class="pill ' + (r["Ownly Wins"] === "Yes" ? "p-ok" : "p-bad") + '">' +
          (r["Ownly Wins"] === "Yes" ? "Ownly wins" : "Ownly loses") + "</span>"; } },
  ], T("07_price_audit_pairs")),
  "<b>Source</b> · 07_price_audit_pairs.csv. The Ownly account was new (carrying an intro offer); the incumbent accounts were subscribed.");

/* — 4c predictive — */
card("c7", "Predicted adoption at any recurring saving", bBoth("4.6"),
  "Logistic curve fitted to six observed staircase points. Solid inside the observed range, dashed beyond it.",
  (function () {
    var rows = T("11_demand_curve");
    var obs = rows.filter(function (r) { return r.Series === "Observed"; });
    var fit = rows.filter(function (r) { return r.Series === "Fitted logistic"; })
                  .sort(function (a, b) { return a["Saving Rs"] - b["Saving Rs"]; });
    var mk = rows.filter(function (r) { return String(r.Series).indexOf("Observed saving") === 0; });
    var maxObs = Math.max.apply(null, obs.map(function (r) { return num(r["Saving Rs"]); }));
    return V.scatter({
      data: obs.map(function (r) {
        return { x: num(r["Saving Rs"]), y: num(r["Pct Would Switch"]), r: 7, color: C.s[1],
                 tip: "Observed: ₹" + r["Saving Rs"] + " → " + r["Pct Would Switch"] + "% cumulative" };
      }).concat(mk.map(function (r) {
        return { x: num(r["Saving Rs"]), y: num(r["Pct Would Switch"]), r: 8, color: C.s[2],
                 tip: String(r.Series).replace("Observed saving at checkout: ", "") +
                      "\nObserved saving ₹" + r["Saving Rs"] + "\nPredicted adoption " + r["Pct Would Switch"] + "%" };
      })),
      line: fit.filter(function (r) { return num(r["Saving Rs"]) <= maxObs; })
               .map(function (r) { return { x: num(r["Saving Rs"]), y: num(r["Pct Would Switch"]) }; }),
      lineColor: C.s[0],
      w: 620, h: 290, xmin: 0, xmax: 200, ymin: 0, ymax: 100,
      xlab: "Recurring saving per order (₹)", ylab: "Cumulative % who would switch",
      fmtX: function (t) { return "₹" + V.fmt(t, 0); }, fmtY: function (t) { return V.fmt(t, 0) + "%"; }
    });
  })(),
  legend([{ name: "Observed staircase point", color: C.s[1] }, { name: "Fitted logistic", color: C.s[0] }, { name: "Observed saving at each checkout view", color: C.s[2] }]) +
  (function () {
    var f = {}; T("11b_demand_curve_fit").forEach(function (r) { f[r.Parameter] = r.Value; });
    return "<b>Fit</b> · logit(p) = " + f["b0 (intercept)"] + " + " + f["b1 (slope)"] +
      "·saving · <b>R² = " + f["R squared"] + "</b>. <b>Method</b> · Gabor-Granger price response. " +
      "<b>Tableau has no logistic trend line</b> — Python fitted it and the fitted values are a column. " +
      "<b>Base</b> · " + f["Base n"] + " respondents who named a figure; " + f["Excluded - no amount"] +
      " said no amount would move them. <b>Anything above ₹" + f["Max observed saving"] + " is extrapolation.</b>";
  })());

card("c5", "Who is most likely to switch?", bBoth("4.15"),
  "Lift = subgroup rate ÷ overall rate, for “will give up usual restaurants for ₹30”.",
  (function () {
    var rows = where("27_switcher_profiling", function (r) {
      return String(r.Target).indexOf("usual restaurants") >= 0;
    }).sort(function (a, b) { return b.Lift - a.Lift; }).slice(0, 9);
    var base = rows.length ? num(rows[0]["Base Pct"]) : 0;
    return V.barH({
      data: rows.map(function (r) {
        return { label: r.Feature, value: num(r.Pct), lo: num(r["CI Low"]), hi: num(r["CI High"]),
                 vlabel: V.fmt(r.Lift, 2) + "×",
                 color: num(r.Lift) >= 1.25 ? C.s[2] : (num(r.Lift) <= 0.75 ? C.crit : C.s[0]),
                 tip: r.Feature + "\n" + r.K + " of " + r.N + " = " + r.Pct + "%\nlift " + r.Lift +
                      "×\n95% CI " + r["CI Low"] + "–" + r["CI High"] };
      }),
      max: 100, ref: base, w: 460, rowH: 30, labelW: 180,
      fmtAxis: function (t) { return V.fmt(t, 0) + "%"; }
    });
  })(),
  "<b>EXPLORATORY ONLY.</b> n = 40 — subgroup cells are small and every interval is wide. Not a fitted classifier, no out-of-sample validation. Dashed line = overall base rate.");

card("c7", "Profiling significance tests", bPy(),
  "Fisher exact on each 2×2 contrast. Reported rather than suppressed.",
  tbl([
    { label: "Outcome", get: function (r) { return V.esc(r.Target); } },
    { label: "Feature", get: function (r) { return "<b>" + V.esc(r.Feature) + "</b>"; } },
    { label: "In yes/no", n: 1, get: function (r) { return r["In Yes"] + " / " + r["In No"]; } },
    { label: "Out yes/no", n: 1, get: function (r) { return r["Out Yes"] + " / " + r["Out No"]; } },
    { label: "p", n: 1, get: function (r) { return V.fmt(r["Fisher P"], 3); } },
    { label: "Verdict", get: function (r) {
        return '<span class="pill ' + (r.Detectable === "Yes" ? "p-ok" : "p-na") + '">' +
          (r.Detectable === "Yes" ? "Significant" : "Not detectable") + "</span>"; } },
  ], T("27b_profiling_tests")),
  "<b>This is the honest limit of a 40-person sample</b> — we can measure the headline rate precisely enough to act on, but not the subgroup differences.");

card("c5", "Relationships between survey variables", bPy(),
  "Spearman rank correlation. Blue positive, red negative, pale = no relationship.",
  (function () {
    var cells = T("26_correlations_long");
    var vars = uniq(cells, "Variable A");
    return V.heatmap({
      rows: vars, cols: vars,
      get: function (a, b) {
        var f = cells.filter(function (r) {
          return (r["Variable A"] === a && r["Variable B"] === b) ||
                 (r["Variable A"] === b && r["Variable B"] === a);
        });
        return f.length ? num(f[0]["Spearman Rho"]) : null;
      },
      label: function (v) { return V.fmt(v, 2); },
      tip: function (a, b, v) {
        var f = cells.filter(function (r) {
          return (r["Variable A"] === a && r["Variable B"] === b) ||
                 (r["Variable A"] === b && r["Variable B"] === a);
        });
        return a + " × " + b + (f.length ? "\nρ = " + f[0]["Spearman Rho"] + "\np = " + f[0]["P Value"] + " (n=" + f[0].N + ")" : "");
      },
      w: 560, labelW: 150, headH: 90, cellH: 27
    });
  })(),
  "<b>At n = 40 only strong relationships are detectable.</b> Every off-diagonal cell here is weak and none reaches significance — reported as a null result, not suppressed.");

card("c7", "Formally tested associations", bPy(),
  "The four relationships specified in the pre-analysis plan.",
  tbl([
    { label: "Question", get: function (r) { return "<b>" + V.esc(r.Question) + "</b>"; } },
    { label: "n", n: 1, get: function (r) { return r.N; } },
    { label: "ρ", n: 1, get: function (r) { return V.fmt(r["Spearman Rho"], 3); } },
    { label: "p", n: 1, get: function (r) { return V.fmt(r["P Value"], 3); } },
    { label: "95% CI", n: 1, get: function (r) { return V.fmt(r["CI Low"], 2) + " – " + V.fmt(r["CI High"], 2); } },
    { label: "Verdict", get: function (r) { return '<span class="pill p-na">' + V.esc(r.Verdict) + "</span>"; } },
  ], T("26b_associations")),
  "All four fail to reach significance. At n = 40 this means <b>the sample cannot detect a relationship</b>, not that none exists.");

/* — 4d text analytics — */
card("c5", "Does the sentiment model actually work?", bBoth("4.10"),
  "Validation: mean lexicon score against the star rating the reviewer chose. Independent signals.",
  V.barH({
    data: T("17_sentiment_validation").sort(function (a, b) { return a["Star Rating"] - b["Star Rating"]; })
      .map(function (r) {
        var m = num(r["Mean Sentiment Score"]);
        return { label: r["Star Rating"] + " ★  (n=" + r.Reviews + ")", value: m + 1,
                 vlabel: V.fmt(m, 2), color: m < 0 ? C.crit : C.s[2],
                 tip: r["Star Rating"] + "-star reviews (n=" + r.Reviews + ")\nmean sentiment " + m };
      }),
    max: 2, ref: 1, w: 430, rowH: 32, labelW: 135,
    fmtAxis: function (t) { return V.fmt(t - 1, 1); }
  }),
  (function () {
    var s = {}; T("17b_sentiment_validation_stat").forEach(function (r) { s[r.Statistic] = r.Value; });
    return "<b>Spearman ρ = " + s["Spearman rho"] + ", n = " + s.n + ", p < 0.001.</b> " +
      "The lexicon was written blind to the star ratings, so this is a genuine out-of-sample check. " +
      "Monotonic from 1★ to 5★. <b>Tableau has no NLP</b> — Python scored all 836 documents.";
  })());

card("c7", "Sentiment by source", bTab("4.7"),
  "The people who have actually ordered are far more negative than the people commenting.",
  (function () {
    var g = by(T("16b_sentiment_by_source_long"), "Source");
    var order = { Negative: 0, Neutral: 1, Positive: 2 };
    return V.stacked100({
      data: Object.keys(g).map(function (s) {
        return { label: s + " (" + sum(g[s], "Documents") + ")",
                 parts: g[s].sort(function (a, b) { return order[a["Sentiment Label"]] - order[b["Sentiment Label"]]; })
                   .map(function (r) {
                     return { name: r["Sentiment Label"], value: num(r["Pct Of Source"]),
                              color: r["Sentiment Label"] === "Negative" ? C.crit :
                                     r["Sentiment Label"] === "Positive" ? C.s[2] : "#c9d1d8" };
                   }) };
      }), w: 600, labelW: 140
    });
  })(),
  legend([{ name: "Negative", color: C.crit }, { name: "Neutral", color: "#c9d1d8" }, { name: "Positive", color: C.s[2] }]) +
  "<b>Mean score</b> · app store −0.42, YouTube −0.03, social −0.02. <b>Caution</b> · public posts are self-selected and dissatisfied users post far more readily. The <i>difference between sources</i> carries the information, not the level.");

card("c7", "Volume and sentiment over 16 months", bBoth("4.8"),
  "Monthly document count against mean sentiment, through Ownly's launch period.",
  (function () {
    var t = T("15_text_trend_monthly").sort(function (a, b) { return a.Month < b.Month ? -1 : 1; });
    return V.lineChart({
      x: t.map(function (r) { return String(r.Month).slice(2); }),
      series: [{ name: "Documents", color: C.s[0], area: true, values: t.map(function (r) { return num(r.Documents); }) }],
      w: 600, h: 180, fmtTip: function (v) { return V.fmt(v, 0) + " documents"; }
    }) + V.lineChart({
      x: t.map(function (r) { return String(r.Month).slice(2); }),
      series: [{ name: "Mean sentiment", color: C.s[1], values: t.map(function (r) { return num(r["Mean Sentiment"]); }) }],
      w: 600, h: 150, min: -0.5, max: 0.5,
      fmtAxis: function (v) { return V.fmt(v, 2); }, fmtTip: function (v) { return V.fmt(v, 3); }
    });
  })(),
  legend([{ name: "Document volume", color: C.s[0] }, { name: "Mean sentiment", color: C.s[1] }]) +
  "<b>Volume spikes in 2026-08</b> (331 of 836 documents) around the Hyderabad push. Sentiment runs slightly negative throughout and does <b>not</b> improve as volume rises.");

card("c5", "Sentiment mix by month", bPy(),
  "The same 16 months as a 100% stacked share — does the mix shift, not just the level?",
  (function () {
    var g = by(T("15b_text_trend_long"), "Month");
    var order = { Negative: 0, Neutral: 1, Positive: 2 };
    return V.stacked100({
      data: Object.keys(g).sort().map(function (m) {
        return { label: String(m).slice(2), parts: g[m].sort(function (a, b) {
          return order[a["Sentiment Label"]] - order[b["Sentiment Label"]]; })
          .map(function (r) {
            return { name: r["Sentiment Label"], value: num(r["Pct Of Month"]),
                     color: r["Sentiment Label"] === "Negative" ? C.crit :
                            r["Sentiment Label"] === "Positive" ? C.s[2] : "#c9d1d8" };
          }) };
      }), w: 440, labelW: 52
    });
  })(),
  "Months with very few documents produce unstable shares — read the early months with care.");

card("c5", "What the market talks about", bTab("4.9"),
  "119 granular codes rolled into families by keyword rule. Area = documents, colour = sentiment.",
  V.treemap({
    data: T("14_theme_families").filter(function (r) { return r["Theme Family"] !== "Other"; })
      .map(function (r) {
        return { label: r["Theme Family"], value: num(r.Documents), sentiment: num(r["Mean Sentiment"]),
                 tip: r["Theme Family"] + "\n" + r.Documents + " documents\nmean sentiment " + r["Mean Sentiment"] };
      }),
    color: function (r) { return V.diverge(r.sentiment, 0.35); },
    w: 440, h: 290
  }),
  "<b>Red = negative, green = positive.</b> Execution themes are the negative ones; value themes are the positive ones.");

card("c7", "Theme volume against theme sentiment", bPy(),
  "Bottom-right is the danger zone: talked about a lot, and talked about badly.",
  V.scatter({
    data: T("14_theme_families").filter(function (r) { return r["Theme Family"] !== "Other"; })
      .map(function (r) {
        var s = num(r["Mean Sentiment"]), n = num(r.Documents);
        return { x: n, y: s, r: 6 + Math.sqrt(n) * 0.85,
                 color: s < -0.15 ? C.crit : (s > 0.05 ? C.s[2] : C.s[3]),
                 label: r["Theme Family"].length > 16 ? r["Theme Family"].slice(0, 15) + "…" : r["Theme Family"],
                 tip: r["Theme Family"] + "\n" + n + " documents\nmean sentiment " + s };
      }),
    w: 600, h: 290, ymin: -0.45, ymax: 0.25, xmin: 0,
    xlab: "Documents mentioning the theme", ylab: "Mean sentiment",
    fmtY: function (t) { return V.fmt(t, 2); }
  }),
  "<b>Fulfilment failure</b>, <b>Support &amp; refunds</b> and <b>Trust</b> are the negative cluster — all execution, none of them price. <b>Price — advantage</b> is the largest theme and is mildly positive.");

card("c6", "Distinctive vocabulary", bBoth("4.11"),
  "Top terms by mean TF-IDF across all 836 documents, stopwords and brand names removed.",
  V.barH({
    data: where("18_tfidf_terms", function (r) { return r.Scope === "Overall"; })
      .sort(function (a, b) { return a.Rank - b.Rank; }).slice(0, 14)
      .map(function (r, i) {
        return { label: r.Term, value: num(r["TFIDF Score"]), vlabel: V.fmt(num(r["TFIDF Score"]) * 100, 1),
                 color: V.seqColor(0.35 + 0.6 * (1 - i / 14)),
                 tip: '"' + r.Term + '" — TF-IDF ' + r["TFIDF Score"] + ", appears in " + r["Document Frequency"] + " documents" };
      }),
    w: 500, rowH: 24, labelW: 130, fmtAxis: function (t) { return V.fmt(t * 100, 0); }
  }),
  "TF-IDF favours terms frequent in some documents but rare across the corpus — what makes a document <i>distinctive</i>, not merely common. <b>Tableau cannot compute TF-IDF</b>.");

card("c6", "Which themes co-occur", bPy(),
  "Pairs of themes appearing in the same document — how arguments bundle.",
  V.barH({
    data: T("19_theme_cooccurrence").slice(0, 12).map(function (r) {
      var a = r["Theme A"], b = r["Theme B"];
      return { label: (a.length > 15 ? a.slice(0, 14) + "…" : a) + " + " + (b.length > 15 ? b.slice(0, 14) + "…" : b),
               value: num(r.Documents), vlabel: r.Documents, color: C.s[0],
               tip: a + " + " + b + ": " + r.Documents + " documents" };
    }),
    w: 520, rowH: 24, labelW: 245, fmtAxis: function (t) { return V.fmt(t, 0); }
  }),
  "<b>Source</b> · co-occurrence within the theme codes assigned to each document.");

card("", "Most-engaged verbatims", bPy(),
  "Ranked by likes/reactions. Engagement is published by YouTube and a few social posts only.",
  '<div>' + T("20_verbatims").slice(0, 12).map(function (v) {
    var lab = v["Sentiment Label"];
    return '<div class="verb"><div class="meta">' +
      '<span class="pill ' + (lab === "negative" ? "p-bad" : lab === "positive" ? "p-ok" : "p-na") + '">' +
      V.esc(lab) + " " + V.fmt(v["Sentiment Score"], 2) + '</span>' +
      '<span>' + V.esc(v.Source) + '</span>' + (v.Month ? '<span>' + V.esc(v.Month) + '</span>' : '') +
      (num(v.Engagement) ? '<span>♥ ' + V.cnt(v.Engagement) + '</span>' : '') +
      (num(v["Star Rating"]) ? '<span>' + v["Star Rating"] + '★</span>' : '') +
      (v.Themes ? '<span>' + V.esc(String(v.Themes).split(";").slice(0, 3).join(" · ")) + '</span>' : '') +
      '</div><div class="txt">' + V.esc(v.Verbatim) + '</div></div>';
  }).join('') + '</div>',
  "<b>Warning</b> · 471 of 524 social items return “not exposed by RSS” for engagement, so engagement-weighted views are YouTube-dominated and are not a full-corpus measure.");

/* — 4e competitive / method — */
card("c7", "Evidence triangulation", bTab("4.12"),
  "Which sources speak to which question. A claim resting on one column is weaker than one resting on four.",
  (function () {
    var rows = T("34_evidence_matrix_long");
    var dims = uniq(rows, "Dimension"), srcs = uniq(rows, "Evidence Source");
    var COL = { Strong: "#7fc39b", Moderate: "#bfe0cf", Directional: "#f5e3b8", Present: "#e4ecf3", Contradicted: "#eda6a6" };
    return V.heatmap({
      rows: dims, cols: srcs,
      get: function (d, s) {
        var f = rows.filter(function (r) { return r.Dimension === d && r["Evidence Source"] === s; });
        return f.length ? f[0] : null;
      },
      color: function (v) { return COL[v.Strength] || "#eceff2"; },
      label: function (v) { return String(v.Strength).slice(0, 3); },
      tip: function (d, s, v) { return d + "\n" + s + ": " + v.Strength + "\n\n" + v.Assessment; },
      w: 620, labelW: 210, headH: 96, cellH: 26
    }) + legend(Object.keys(COL).map(function (k) { return { name: k, color: COL[k] }; }));
  })(),
  "<b>Source</b> · 34_evidence_matrix_long.csv. Hover any cell for the full assessment.");

card("c5", "Gachibowli against Bengaluru", bTab("4.13"),
  "The same six metrics measured in both cities. Bengaluru is where the playbook was written.",
  (function () {
    var rows = T("24_city_benchmark_long");
    var metrics = uniq(rows, "Metric");
    var blr = "Bengaluru (benchmark)", hyd = "Gachibowli catchment";
    return V.slope({
      data: metrics.map(function (m, i) {
        var l = rows.filter(function (r) { return r.Metric === m && r["City Base"] === blr; });
        var rr = rows.filter(function (r) { return r.Metric === m && r["City Base"] === hyd; });
        return { label: m, left: l.length ? num(l[0].Value) : 0, right: rr.length ? num(rr[0].Value) : 0,
                 color: C.s[i % C.s.length] };
      }),
      leftLabel: "Bengaluru (n=16)", rightLabel: "Gachibowli (n=40)", w: 450, h: 300
    });
  })(),
  "<b>Awareness and trial are far lower in Hyderabad</b> — expected, Ownly is weeks old there. <b>Membership lock-in is the same</b> in both, so the barrier travels. <b>Caution</b> · the Bengaluru base is n = 16.");

card("c5", "Restaurant availability across platforms", bTab("4.14"),
  "The 10-restaurant audit frame.",
  (function () {
    var rows = T("22_coverage_long");
    var rests = uniq(rows, "Restaurant"), plats = uniq(rows, "Platform");
    return V.heatmap({
      rows: rests, cols: plats,
      get: function (a, b) {
        var f = rows.filter(function (r) { return r.Restaurant === a && r.Platform === b; });
        return f.length ? num(f[0]["Listed Flag"]) : null;
      },
      color: function (v) { return v ? "#bfe6cf" : "#eceff2"; },
      label: function (v) { return v ? "●" : "—"; },
      tip: function (a, b, v) { return a + " on " + b + ": " + (v ? "listed" : "not listed"); },
      w: 420, labelW: 180, headH: 54, cellH: 27
    });
  })(),
  "<b>Selection caveat</b> · the frame was built from Ownly's showcase page plus incumbent chains, so it <b>selects for restaurants present everywhere</b> and cannot detect exclusives. Ownly lists 221 restaurants at this address; we priced 10.");

card("c4", "App-store rating distribution", bTab("4.17"),
  "37 reviews retrieved. The shape, not the mean, is the finding.",
  V.barH({
    data: T("21_review_stars").sort(function (a, b) { return b["Star Rating"] - a["Star Rating"]; })
      .map(function (r) {
        return { label: r["Star Rating"] + " ★", value: num(r.Reviews), vlabel: r.Reviews,
                 color: r["Is Low Rating"] === "Yes" ? C.crit : C.s[2],
                 tip: r["Star Rating"] + "-star: " + r.Reviews + " of 37 reviews" };
      }),
    w: 380, rowH: 28, labelW: 56, fmtAxis: function (t) { return V.fmt(t, 0); }
  }),
  "<b>Bottom-heavy</b> — 26 of 37 at 1★. The most self-selected source in the study. Not an order failure rate.");

card("c8", "Segment scorecard", bTab("4.18"),
  "Six cuts of the catchment across the metrics that drive the decision.",
  (function () {
    var rows = T("28_segment_cuts_long");
    var segs = uniq(rows, "Segment"), mets = uniq(rows, "Metric");
    return V.heatmap({
      rows: segs, cols: mets,
      get: function (s, m) {
        var f = rows.filter(function (r) { return r.Segment === s && r.Metric === m; });
        return f.length ? num(f[0].Value) : null;
      },
      color: function (v) { return V.seqColor(Math.min(1, v / 100)); },
      label: function (v) { return V.fmt(v, 0); },
      tip: function (s, m, v) { return s + "\n" + m + ": " + v; },
      w: 660, labelW: 180, headH: 108, cellH: 27
    });
  })(),
  "<b>Interpret with care</b> · the working-professional cell is n = 7. Directional only.");

card("c4", "Trade-off by segment", bPy(),
  "Does the ₹30 result hold within subgroups? Fisher exact p on each contrast.",
  tbl([
    { label: "Dimension", get: function (r) { return V.esc(r.Dimension); } },
    { label: "Segment", get: function (r) { return "<b>" + V.esc(r.Segment) + "</b>"; } },
    { label: "n", n: 1, get: function (r) { return r.N; } },
    { label: "Accept", n: 1, get: function (r) { return V.fmt(r["Accept Pct"], 1) + "%"; } },
    { label: "p", n: 1, get: function (r) { return V.fmt(r["Fisher P"], 3); } },
  ], T("28b_segment_tradeoffs")),
  "Every contrast is <b>underpowered</b>.");

card("c7", "Hypothesis register", bPy(),
  "Every test specified in the pre-analysis plan, including the ones that found nothing.",
  tbl([
    { label: "Hypothesis", get: function (r) { return "<b>" + V.esc(String(r.Statement || "").slice(0, 130)) + "</b>"; } },
    { label: "Test", get: function (r) { return V.esc(r.Test); } },
    { label: "n", n: 1, get: function (r) { return r.N; } },
    { label: "p", n: 1, get: function (r) { return r["P Value"] === null ? "—" : r["P Value"]; } },
    { label: "Verdict", get: function (r) {
        var v = String(r.Verdict);
        var cls = v.indexOf("FAIL") >= 0 ? "p-na" : v.indexOf("NOT") >= 0 ? "p-warn" : "p-ok";
        return '<span class="pill ' + cls + '">' + V.esc(v) + "</span>"; } },
  ], T("35_hypotheses")),
  "<b>Pre-registration</b> · plan frozen at 09_analysis/PAP_frozen_2026-09-21.md with a provenance block separating git-dated sections from later additions whose pre-data status rests on the project log alone.");

card("c5", "Data-quality register", bPy(),
  "Anomalies found during cleaning and exactly how each was handled.",
  tbl([
    { label: "Anomaly", get: function (r) { return "<b>" + V.esc(r.Anomaly) + "</b>"; } },
    { label: "How it was handled", get: function (r) { return V.esc(r["How It Was Handled"]); } },
  ], T("36_data_quality")),
  "");
endsec();

/* ═══════════════════ 5 · PROPOSITIONS ═══════════════════ */
sec("s5", "Section 5", "Propositions",
  "The Bengaluru playbook, tactic by tactic — and the economic constraint underneath all of it.");

card("", "KEEP / ADAPT / DEPRIORITISE", bTab("5.1"),
  "Each call anchored to a single measured number.",
  tbl([
    { label: "Bengaluru tactic", get: function (r) { return "<b>" + V.esc(r["Bengaluru Tactic"]) + "</b>"; } },
    { label: "Call", get: function (r) {
        var c = r.Call, cls = c === "KEEP" ? "p-ok" : c === "ADAPT" ? "p-warn" : "p-bad";
        return '<span class="pill ' + cls + '">' + V.esc(c) + "</span>"; } },
    { label: "Evidence", get: function (r) { return V.esc(r.Evidence); } },
    { label: "Key metric", get: function (r) { return V.esc(r["Key Metric"]); } },
    { label: "Value", n: 1, get: function (r) { return "<b>" + V.esc(r["Key Value"]) + "</b>"; } },
  ], T("38_propositions").sort(function (a, b) { return a["Call Order"] - b["Call Order"]; })),
  "");

OUT.push('<section class="card"><div class="callout"><p><b>If you remember one sentence.</b> ' +
  'Ownly\'s price advantage is real and durable, but it is aimed at the one thing this market will ' +
  'not trade — and it is invisible to the 82.5% who already pay for a membership. ' +
  '<b>Fix the restaurant list before spending another rupee on the discount.</b></p></div></section>');

card("c6", "Contribution per order — the sign problem", bTab("5.2"),
  "Contribution = revenue per order − rider payout, at three rider-cost assumptions.",
  (function () {
    var rows = T("31_breakeven_grid_long");
    var scen = uniq(rows, "Rider Cost Scenario");
    var revs = uniq(rows, "Revenue Per Order Rs").sort(function (a, b) { return a - b; });
    return V.lineChart({
      x: revs.map(function (r) { return "₹" + r; }),
      series: scen.map(function (s, i) {
        return { name: s, color: C.s[[2, 0, 1][i] || i],
                 values: revs.map(function (rv) {
                   var f = rows.filter(function (r) { return r["Rider Cost Scenario"] === s && num(r["Revenue Per Order Rs"]) === rv; });
                   return f.length ? num(f[0]["Contribution Per Order Rs"]) : null;
                 }) };
      }),
      w: 520, h: 250, min: -70, max: 45,
      fmtAxis: function (t) { return "₹" + V.fmt(t, 0); }, fmtTip: function (v) { return V.inr(v, 2); }
    }) + legend(scen.map(function (s, i) { return { name: s, color: C.s[[2, 0, 1][i] || i] }; }));
  })(),
  (function () {
    var b = {}; T("31b_breakeven_summary").forEach(function (r) { b[r.Item] = r.Value; });
    return "<b>Ownly's only reported revenue figure is ₹" + b["Revenue per order (reported)"] +
      " per order.</b> At the industry rider payout that is <b>" + V.inr(b["Contribution per order"], 2) +
      " per order</b> before marketing, support or overhead. Break-even revenue is <b>" +
      V.inr(b["Break-even revenue per order"], 2) + "</b>, an uplift of <b>" + b["Uplift needed pct"] + "%</b>.";
  })());

card("c6", "Which lever moves the outcome most?", bTab("5.3"),
  "Monthly contribution swing when each lever is moved across a plausible range, others held at base.",
  V.tornado({
    data: T("32_lever_sensitivity").sort(function (a, b) { return b.Swing - a.Swing; })
      .map(function (r) {
        return { lever: r.Lever, low: num(r["Low Outcome"]), high: num(r["High Outcome"]),
                 lo_val: r["Range Low"], hi_val: r["Range High"],
                 color: r["Lever Type"] === "Can change the sign" ? C.s[2] : C.s[0] };
      }),
    w: 520, labelW: 205, fmtAxis: function (t) { return "₹" + V.fmt(t / 1000, 0) + "k"; }
  }),
  legend([{ name: "Volume lever — moves contribution the WRONG way while it is negative", color: C.s[0] },
          { name: "Can change the sign", color: C.s[2] }]) +
  "<b>Read this carefully.</b> While contribution per order is negative, growth makes losses larger, not smaller. Only the revenue and cost levers can change the sign. This is the mechanism that ended Uber Eats India.");

card("c6", "Why challengers have failed before", bTab("5.4"),
  "Five mechanisms from the historical record, scored against our own evidence.",
  tbl([
    { label: "Failure mechanism", get: function (r) { return "<b>" + V.esc(r["Failure Mechanism"]) + "</b>"; } },
    { label: "Ownly", get: function (r) {
        var s = r["Ownly Status"], cls = s === "Escaped" ? "p-ok" : s === "At risk" ? "p-warn" : "p-bad";
        return '<span class="pill ' + cls + '">' + V.esc(s) + "</span>"; } },
    { label: "Our evidence", get: function (r) { return V.esc(r["Our Evidence"]); } },
  ], T("25_challenger_failure_modes").sort(function (a, b) { return a["Status Order"] - b["Status Order"]; })),
  "<b>Source</b> · 01_secondary_research/challenger_failures/ — Foodpanda, Uber Eats India, Amazon Food, Dunzo, ONDC, magicpin, Thrive, DotPe, Toing, Zepto Café.");

card("c6", "Unit-economics benchmarks and their provenance", bPy(),
  "Only figures that are FACT-grade and common across the domain were adopted.",
  tbl([
    { label: "Metric", get: function (r) { return "<b>" + V.esc(r.Metric) + "</b>"; } },
    { label: "Value", n: 1, get: function (r) {
        var u = r.Unit;
        return u === "₹" ? V.inr(r.Value, 2) : u === "$" ? "$" + V.fmt(r.Value, 2) : V.fmt(r.Value, 1) + " " + u; } },
    { label: "Grade", get: function (r) {
        var g = String(r["Evidence Grade"]);
        var cls = g.indexOf("FACT") === 0 ? "p-ok" : g.indexOf("CALC") === 0 ? "p-info" : "p-warn";
        return '<span class="pill ' + cls + '">' + V.esc(g) + "</span>"; } },
    { label: "Entity", get: function (r) { return V.esc(r.Entity) + '<br><span style="color:var(--muted)">' + V.esc(r.Series) + "</span>"; } },
    { label: "Source", get: function (r) { return V.esc(r.Source); } },
  ], T("30_econ_benchmarks")),
  "<b>Deliberately excluded</b> · CAC. Our own secondary research concludes there is <b>no credible, dated, primary-sourced CAC figure for Indian food delivery in the public domain</b> — neither DRHP discloses it. Advertising &amp; sales promotion per order is used as the named defensible proxy instead.");

OUT.push('<section class="card"><div class="callout warn"><p><b>What this economics layer is not.</b> ' +
  'It is a contribution model, not a P&amp;L — fixed costs, technology, support and overhead are excluded ' +
  'entirely, so true break-even is strictly worse than shown. Ownly\'s ₹30 revenue per order is ' +
  'MEDIA-reported and contested across three outlets, and our own Gachibowli audit observed <b>₹0</b> ' +
  'charged to the customer, which would make contribution worse, not better. ₹56.01 is Swiggy\'s FY24 ' +
  'disclosed rider payout used as a domain-wide proxy; Ownly\'s own delivery cost is not disclosed by anyone.' +
  '</p></div></section>');
endsec();

/* ═══════════════════ RENDER ═══════════════════ */
document.getElementById("main").innerHTML = OUT.join("");
V.initTooltip();

/* nav highlighting */
(function () {
  var links = Array.prototype.slice.call(document.querySelectorAll("#nav a"));
  var secs = links.map(function (a) { return document.querySelector(a.getAttribute("href")); });
  var ticking = false;
  function upd() {
    ticking = false;
    var best = 0;
    for (var i = 0; i < secs.length; i++) if (secs[i] && secs[i].getBoundingClientRect().top < 140) best = i;
    links.forEach(function (a, k) { a.classList.toggle("on", k === best); });
  }
  window.addEventListener("scroll", function () {
    if (!ticking) { ticking = true; window.requestAnimationFrame(upd); }
  }, { passive: true });
  upd();
})();
})();
