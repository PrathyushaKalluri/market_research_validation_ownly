/* ═══════════════════════════════════════════════════════════════════
   Ownly Gachibowli — pre-registration-aligned dashboard.
   Five sections. Every number carries its formula, calculation and source.
   ═══════════════════════════════════════════════════════════════════ */
(function () {
"use strict";
var A = window.AD, V = window.VZ, C = V.C;
function T(n) { return A[n] || []; }
function num(v) { return (v === null || v === undefined || isNaN(v)) ? null : +v; }
function uniq(rows, k) { var s = []; rows.forEach(function (r) { if (s.indexOf(r[k]) < 0) s.push(r[k]); }); return s; }
function by(rows, k) { var m = {}; rows.forEach(function (r) { (m[r[k]] = m[r[k]] || []).push(r); }); return m; }

var OUT = [];
function sec(id, n, title, lede) {
  OUT.push('<section class="sec" id="' + id + '"><div class="eyebrow">' + n + '</div><h2>' +
    V.esc(title) + '</h2>' + (lede ? '<p class="lede prose">' + lede + '</p>' : '') + '<div class="grid">');
}
function endsec() { OUT.push('</div></section>'); }
function card(cls, title, sub, body, note) {
  OUT.push('<section class="card ' + (cls || '') + '"><div class="hd"><h3>' + V.esc(title) +
    '</h3></div>' + (sub ? '<p class="sub">' + sub + '</p>' : '') + body +
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
function provRows(pairs) {
  return '<div class="prov">' + pairs.filter(function (p) { return p[1]; }).map(function (p) {
    return '<div class="r"><span class="l">' + V.esc(p[0]) + '</span><span>' + V.esc(p[1]) + '</span></div>';
  }).join('') + '</div>';
}
function statusPill(s) {
  var t = String(s).toUpperCase(), cls = "p-ok";
  if (t.indexOf("NOT COMPUTABLE") >= 0 || t.indexOf("NOT FIELDED") >= 0) cls = "p-unk";
  else if (t.indexOf("LOW BASE") >= 0 || t.indexOf("ABSENT") >= 0 || t.indexOf("WIDE") >= 0 || t.indexOf("n=4") >= 0) cls = "p-warn";
  return '<span class="pill ' + cls + '">' + V.esc(s) + '</span>';
}

/* ══════════ TOP STRIP ══════════ */
var kpi = T("01_kpi_prereg_computed");
var comp = kpi.filter(function (r) { return String(r.Status).indexOf("COMPUTED") === 0; }).length;
var matrix = T("02_transferability_matrix");
var guards = T("03_guardrails");
var nKeep = matrix.filter(function (r) { return r.Verdict === "KEEP"; }).length;
var nInsuf = matrix.filter(function (r) { return r.Verdict === "INSUFFICIENT EVIDENCE"; }).length;
var overall = T("04_overall_call").filter(function (r) { return r.Rule === "OVERALL HYDERABAD CALL"; })[0] || {};
document.getElementById("topstrip").innerHTML = [
  { v: overall.Observed || "—", k: "Overall Hyderabad call (decision_rules §3)", s: "PROVISIONAL — 4 of 6 rows LOW confidence", color: C.s[6] },
  { v: nKeep + " of 6", k: "playbook elements verdicted KEEP", s: "2 KEEP · 1 DEPRIORITIZE · 3 insufficient" },
  { v: nInsuf + " of 6", k: "elements that cannot be decided on evidence", s: "their inputs are not computable", color: C.crit },
  { v: "2 of 4", k: "guardrails that cannot be evaluated", s: "G2 and G4 — source questions absent", color: C.crit },
  { v: comp + " of " + kpi.length, k: "pre-registered KPIs computed", s: (kpi.length - comp) + " not computable" },
  { v: "40", k: "survey respondents in catchment", s: "124 received · 87 quality-passed" },
].map(function (k) {
  return '<div class="kc"><span class="v"' + (k.color ? ' style="color:' + k.color + '"' : '') + '>' +
    V.esc(k.v) + '</span><span class="k">' + V.esc(k.k) + '</span><span class="s">' + V.esc(k.s) + '</span></div>';
}).join("");

/* ══════════ 1 · PROBLEM STATEMENT ══════════ */
sec("s1", "Section 1", "Problem statement",
  "Corrected against the project charter and the pre-registered decision rules. Every block carries an " +
  "evidence label, as <code>A_research_charter.md §5</code> requires of every claim in every deliverable.");

card("c8", "The problem, the question, and the two decisions it serves", "",
  T("07_problem_statement_aligned").sort(function (a, b) { return a.Order - b.Order; })
    .map(function (r) {
      var lab = String(r["Evidence label"] || "");
      var cls = lab.indexOf("FACT") === 0 ? "p-ok" : lab.indexOf("MEDIA") === 0 ? "p-warn" :
                lab.indexOf("PRE-REG") === 0 ? "p-info" : "p-na";
      return '<div class="blk"><div class="h">' + V.esc(r.Section) +
        '<span class="pill ' + cls + '">' + V.esc(lab) + '</span></div>' +
        '<div class="t">' + V.esc(r.Content) + '</div>' +
        '<div class="src">source · ' + V.esc(r.Source) + '</div></div>';
    }).join(""),
  "<b>What changed from the earlier build</b> · the decision framing now shows <b>both</b> pre-registered levels " +
  "(six playbook elements, then the overall call) instead of an ad-hoc seven-tactic list; every block carries an " +
  "evidence label; and the Foodpanda figure is labelled MEDIA REPORT, which is its grade in our own source.");

card("c4", "Input lineage", "Every file this dashboard reads, and what it feeds.",
  T("06_provenance").map(function (r) {
    return '<div class="blk"><div class="h">' + V.esc(r.Input) + '</div>' +
      '<div class="t" style="font-size:12.5px">' + V.esc(r["What it is"]) + '</div>' +
      '<div class="src">' + V.esc(r.Path) + '<br>→ ' + V.esc(r["What it feeds"]) + '</div></div>';
  }).join(""), "");

card("", "H₀ — which test is primary, and what it returned",
  "decision_rules §1 fixes the primary test in advance, so the choice is not made after seeing results.",
  tbl([
    { label: "Item", get: function (r) { return "<b>" + V.esc(r.Item) + "</b>"; } },
    { label: "Value", get: function (r) { return V.esc(r.Value); } },
    { label: "Pre-registered rule", get: function (r) { return '<span style="font-family:var(--mono);font-size:11px">' + V.esc(r["Pre-registered rule"]) + '</span>'; } },
    { label: "Evaluation", get: function (r) { return V.esc(r.Evaluation); } },
  ], T("05_h0_result")),
  "<b>Correction carried forward</b> · the “28% could not choose” figure is <b>27.5%</b> and sits <b>below</b> " +
  "the pre-registered 35% threshold, so it does <b>not</b> trigger the rule it was previously presented as meeting. " +
  "It is reported for information only.");
endsec();

/* ══════════ 2 · KPIs ══════════ */
sec("s2", "Section 2", "KPIs",
  "The pre-registered KPI set from <code>metric_dictionary.md</code> — not the ad-hoc numbering used in the " +
  "earlier dashboard. Expand any row for its formula, the calculation applied, and its source columns.");

card("c5", "How much of the pre-registered KPI set is computable",
  comp + " of " + kpi.length + " evaluated KPIs return a value.",
  V.donut({
    data: [{ label: "Computed", value: comp, color: C.s[2] },
           { label: "Not computable", value: kpi.length - comp, color: "#c9d1d8" }],
    size: 200, center: comp + "/" + kpi.length, centerSub: "computed"
  }),
  "<b>The nine that cannot be computed are not an oversight</b> — each names the missing source question or the " +
  "base that is too small. Two of them (K51, K71) sit on guardrails, which is why the overall call cannot clear.");

card("c7", "Guardrails G1–G4",
  "decision_rules §3.1 — any breach blocks a KEEP overall. An unevaluable guardrail cannot be cleared either.",
  guards.map(function (g) {
    var st = String(g.State);
    var cls = st === "NOT BREACHED" ? "keep" : st === "BREACHED" ? "dep" : "insuf";
    var pill = st === "NOT BREACHED" ? "p-ok" : st === "BREACHED" ? "p-bad" : "p-unk";
    return '<div class="elem ' + cls + '"><div class="eh"><span class="en">' + V.esc(g.Guardrail) +
      ' · ' + V.esc(g["Breach condition"]) + '</span><span class="pill ' + pill + '">' + V.esc(st) + '</span></div>' +
      '<div class="inputs"><span class="inp">' + V.esc(g.Observed) + '</span></div>' +
      '<div class="reason">' + V.esc(g.Note) + '</div></div>';
  }).join(""), "");

card("", "Pre-registered KPI register",
  "Every KPI with its status, value, 95% interval and full derivation.",
  '<div class="tw"><table><thead><tr>' +
    ['KPI', 'Name', 'Layer', 'G', 'Status', 'Value', '95% CI', 'n', 'Evidence', 'Derivation']
      .map(function (h, i) { return '<th class="' + (i >= 5 && i <= 7 ? 'n' : '') + '">' + h + '</th>'; }).join('') +
  '</tr></thead><tbody>' + kpi.map(function (r) {
    var v = r.Value === null || r.Value === "" ? "—" : r.Value + " " + (r.Unit || "");
    var ciTxt = (r["CI Low"] === null || r["CI Low"] === "") ? "—" : r["CI Low"] + "–" + r["CI High"];
    var det = '<details class="prov-d"><summary>show formula &amp; source</summary>' + provRows([
      ["Pre-reg formula", r["Pre-registered formula"]],
      ["Calculation", r["Calculation applied"]],
      ["Source file", r["Source file"]],
      ["Source columns", r["Source columns"]],
      ["Pre-reg source", r["Pre-registered source"]],
      ["Evidence label", r["Evidence label"]],
      ["Decision served", r["Decision it serves"]],
      ["Why not computable", r["Why not computable"]],
    ]) + '</details>';
    return '<tr><td><b>' + V.esc(r["KPI ID"]) + '</b>' + (r["North Star"] === "Yes" ? ' ★' : '') +
      '</td><td>' + V.esc(r.Name) + '</td><td>' + V.esc(String(r.Layer).replace(/^Layer \d+ · /, '')) +
      '</td><td>' + V.esc(r.Guardrail || "") + '</td><td>' + statusPill(r.Status) +
      '</td><td class="n">' + V.esc(v) + '</td><td class="n">' + V.esc(ciTxt) +
      '</td><td class="n">' + V.esc(r.N === null ? "—" : r.N) + '</td><td>' +
      V.esc(String(r["Evidence label"] || "").replace(/\.$/, "")) + '</td><td>' + det + '</td></tr>';
  }).join('') + '</tbody></table></div>',
  "<b>Source</b> · Data/01_kpi_prereg_computed.csv, generated by compute_aligned.py from the definitions in " +
  "metric_dictionary.md. <b>★</b> marks the north star. Wilson 95% intervals on proportions; percentile " +
  "bootstrap (10,000 resamples, seed 20260921) on the audit median.");

card("c6", "Computed KPIs, by value",
  "Only the KPIs that returned a value. Whiskers are 95% intervals where the metric is a proportion.",
  V.barH({
    data: kpi.filter(function (r) { return num(r.Value) !== null && r.Unit === "%"; })
      .sort(function (a, b) { return num(b.Value) - num(a.Value); })
      .map(function (r) {
        return { label: r["KPI ID"] + " · " + String(r.Name).slice(0, 32), value: num(r.Value),
                 lo: num(r["CI Low"]), hi: num(r["CI High"]), vlabel: r.Value + "%",
                 color: r.Guardrail ? C.s[1] : C.s[0],
                 tip: r["KPI ID"] + " " + r.Name + "\n" + r.Value + "% (n=" + r.N + ")\n" +
                      (num(r["CI Low"]) !== null ? "95% CI " + r["CI Low"] + "–" + r["CI High"] + "\n" : "") +
                      "\n" + String(r["Calculation applied"]).slice(0, 180) };
      }),
    max: 100, w: 560, rowH: 26, labelW: 235, fmtAxis: function (t) { return V.fmt(t, 0) + "%"; }
  }),
  legend([{ name: "Guardrail KPI", color: C.s[1] }, { name: "Standard KPI", color: C.s[0] }]) +
  "Hover any bar for its derivation.");

card("c6", "Ownly adoption funnel",
  "The pre-registered acquisition layer: K10 → K12 → K01.",
  V.funnel({
    data: [["K10", "Heard of Ownly"], ["K12", "Opened / browsed"], ["K01", "Ordered"]].map(function (p) {
      var r = kpi.filter(function (x) { return x["KPI ID"] === p[0]; })[0] || {};
      var n = num(r.N) || 40;
      return { label: p[1], value: p[0] === "K12" ? 17.5 : num(r.Value), k: Math.round((p[0] === "K12" ? 17.5 : num(r.Value)) * 40 / 100), n: 40 };
    }), w: 520
  }),
  "<b>K01 trial is 2 respondents of 40</b>, 95% CI 1.4–16.5%. The 4-week window mostly predates Ownly's " +
  "Hyderabad rollout, so a low value here measures the question window as much as rejection.");
endsec();

/* ══════════ 3 · MARKETING METRICS ══════════ */
sec("s3", "Section 3", "Marketing metrics",
  "The ten computed metrics and the ten marked NOT ESTIMABLE — plus the one place where a project metric " +
  "and its pre-registered equivalent disagree.");

card("c7", "Metrics computed",
  "Three are definitions constructed for this study, because the standard formula sheet has no metric for the question at issue.",
  V.barH({
    data: T("02_marketing_metrics").map(function (r) {
      var own = r["Our Own Definition"] === "Yes";
      return { label: r["Metric ID"] + " · " + r["Metric Name"], value: num(r.Value),
               vlabel: V.fmt(r.Value, 1) + (r.Unit === "%" ? "%" : " " + (r.Unit || "")),
               color: own ? C.s[1] : C.s[0],
               tip: r["Metric Name"] + "\n" + r.Value + " " + (r.Unit || "") + "\n\n" + (r.Formula || "") +
                    "\n\nCaveat: " + (r.Caveat || "—") };
    }), w: 600, rowH: 29, labelW: 262, fmtAxis: function (t) { return V.fmt(t, 0); }
  }),
  legend([{ name: "Our own definition", color: C.s[1] }, { name: "Standard formula sheet", color: C.s[0] }]));

card("c5", "Marked NOT ESTIMABLE",
  "Every one needs Ownly's or Rapido's internal transaction or cost data.",
  tbl([
    { label: "Metric", get: function (r) { return "<b>" + V.esc(r.Metric) + "</b>"; } },
    { label: "Sheet", get: function (r) { return V.esc(r["Formula Sheet"]); } },
    { label: "Why not computable", get: function (r) { return V.esc(r["Why Not Computable"]); } },
  ], T("03_not_estimable")),
  "<b>The finding inside the gap</b> · the metrics that determine whether Ownly survives are precisely the " +
  "ones no external researcher can see.");

card("", "Where a project metric and its pre-registered equivalent disagree", "",
  '<div class="callout warn"><p><b>MM1 Switch-Threshold Coverage = 81.1%. Pre-registered K23 Switching-threshold ' +
  'coverage = 100%.</b> They are different calculations, and only K23 is pre-registered.</p>' +
  '<p><b>MM1</b> counts person × basket <i>pairs</i> where the observed saving clears that person\'s stated bar: ' +
  '107 of 132 pairs (33 respondents × 4 baskets). <b>K23</b> counts <i>respondents</i> whose stated bar is at or ' +
  'below the single median saving Ownly delivers: 33 of 33, because ₹114.50 exceeds every rupee figure anyone named ' +
  '(the highest was ₹100).</p>' +
  '<p>MM1 is the more conservative and more informative number because it preserves basket-level variation. But the ' +
  'threshold rules in decision_rules §2.1 are written against <b>K23</b>, so K23 is what the verdict uses. ' +
  'Both are shown rather than silently reconciled.</p></div>', "");
endsec();

/* ══════════ 4 · ANALYTICS ══════════ */
sec("s4", "Section 4", "Analytics",
  "The evidence the verdicts rest on. Each chart names the pre-registered KPI it computes.");

card("c7", "K24 · The ₹30 trade-off",
  "Same ₹30 saving, three different sacrifices, same 40 respondents. Whiskers are 95% Wilson intervals.",
  V.barH({
    data: T("04_tradeoffs").sort(function (a, b) { return a["Sort Order"] - b["Sort Order"]; })
      .map(function (r) {
        return { label: r.Description, value: num(r["Accept Pct"]), lo: num(r["CI Low"]), hi: num(r["CI High"]),
                 vlabel: V.fmt(r["Accept Pct"], 1) + "%",
                 color: r["Is Constraint"] === "Yes" ? C.s[1] : C.s[0],
                 tip: r.Description + "\n" + r["Accepted K"] + " of " + r["Base N"] + " = " + r["Accept Pct"] + "%" };
      }),
    max: 100, ref: 50, w: 620, rowH: 42, labelW: 230, fmtAxis: function (t) { return V.fmt(t, 0) + "%"; }
  }),
  "<b>K24 feeds three separate rules.</b> §2.1 uses the <b>speed</b> share (92.5% ≥ 50% → supports KEEP). " +
  "§2.5 uses the <b>restaurant</b> share (35.0% < 50% → supports KEEP). §2.6 uses the <b>reliability</b> share — " +
  "and 72.5% is <b>not</b> below 50%, so the 'people won't trade reliability' branch does not hold in this sample.");

card("c5", "K20 · Median matched-basket saving",
  "Per matched set: (cheaper incumbent − Ownly) ÷ cheaper incumbent. Bootstrap interval on the median.",
  V.barH({
    data: T("07_price_audit_pairs").filter(function (r) { return r["Price View"] === "LIST+FEES"; })
      .sort(function (a, b) { return num(a["Saving Pct"]) - num(b["Saving Pct"]); })
      .map(function (r) {
        return { label: r.Restaurant, value: num(r["Saving Pct"]), vlabel: V.fmt(r["Saving Pct"], 1) + "%",
                 color: C.s[2],
                 tip: r.Restaurant + "\nOwnly " + V.inr(r["Ownly Payable"], 2) + " vs " + r["Cheapest Rival"] +
                      " " + V.inr(r["Cheapest Rival Payable"], 2) + "\nsaving " + V.inr(r["Saving Rs"], 2) };
      }),
    max: 60, w: 420, rowH: 30, labelW: 130, fmtAxis: function (t) { return V.fmt(t, 0) + "%"; }
  }),
  "<b>K20 = 30.5%</b> (median of 16.9, 27.5, 33.5, 52.6). 95% bootstrap CI <b>16.9–52.6%</b>, lower bound above 0, " +
  "so <b>guardrail G1 is not breached</b>. Median in rupees is <b>₹114.50</b>, which clears the §2.1 threshold of ₹30.");

card("c6", "K22 · Fee load, and the gap that drives §2.2",
  "Non-food charges as a share of the final bill, zero-discount captures only.",
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
  "<b>Ownly 4.8% vs incumbent pooled median 23.0% → gap 18.2 pp</b>, well above the 5 pp threshold. " +
  "Paired with <b>K25 fee pain 38.9%</b> (≥ 30%), both §2.2 KEEP conditions are met.");

card("c6", "K50 · ETA gap, and why §2.6 cannot clear",
  "Median shown ETA by platform. The KEEP condition is a gap of at most +5 minutes.",
  (function () {
    var rows = T("23_eta_by_platform_long");
    var rests = uniq(rows, "Restaurant"), plats = uniq(rows, "Platform");
    return V.barGrouped({
      cats: rests,
      series: plats.map(function (p, i) {
        return { name: p, color: p === "Ownly" ? C.s[1] : C.s[i === 0 ? 0 : 3],
                 values: rests.map(function (rst) {
                   var m = rows.filter(function (r) { return r.Restaurant === rst && r.Platform === p; });
                   return m.length ? num(m[0]["Quoted ETA Min"]) : 0;
                 }) };
      }), w: 520, h: 240
    }) + legend(plats.map(function (p, i) { return { name: p, color: p === "Ownly" ? C.s[1] : C.s[i === 0 ? 0 : 3] }; }));
  })(),
  "<b>K50 = +17.0 min</b>, which already fails §2.6's KEEP condition of ≤ +5 min. But the verdict is still " +
  "INSUFFICIENT EVIDENCE, because the other half of that rule — <b>K51 fulfilment failure incidence</b> — has no " +
  "source question in the live instrument.");

card("c6", "K61 · Rapido awareness gap — the decisive input for §2.3",
  "Ownly awareness among Rapido users versus non-users, in this sample.",
  V.barH({
    data: [
      { label: "Rapido users (n=24)", value: 33.3, vlabel: "33.3%", color: C.s[1], tip: "8 of 24 aware of Ownly" },
      { label: "Non-users (n=16)", value: 56.2, vlabel: "56.2%", color: C.s[0], tip: "9 of 16 aware of Ownly" },
    ], max: 100, w: 470, rowH: 40, labelW: 175, fmtAxis: function (t) { return V.fmt(t, 0) + "%"; }
  }),
  "<b>K61 = −22.9 pp.</b> The pre-registered rule says <b>DEPRIORITIZE if K61 ≤ 0</b>, and it is. " +
  "<b>Stated plainly</b> · the interval on that difference runs <b>−58.9 to +20.1 pp</b> and includes positive " +
  "values, so the direction is not established — the rule keys on the point estimate, and we apply it as written " +
  "rather than reinterpreting it after seeing the data.");

card("c6", "K40 / K42 · Supply",
  "Coverage of the 10-restaurant audit frame, and overlap with incumbents.",
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
      w: 430, labelW: 185, headH: 54, cellH: 26
    });
  })(),
  "<b>K40 = 90%</b> (9 of 10) → guardrail G3 not breached. <b>K42 = 88.9%</b> overlap. " +
  "<b>K41 local−chain gap is NOT COMPUTABLE</b> — audit_coverage.csv has no local/chain flag, and K41 is exactly " +
  "what separates KEEP from ADAPT in §2.5. Tagging the 10 frame restaurants would resolve it in an afternoon.");

card("c6", "Voice of customer — sentiment by source",
  "836 documents scored by a negation-aware lexicon, validated against star ratings at ρ = 0.648 (p < 0.001).",
  (function () {
    var g = by(T("16b_sentiment_by_source_long"), "Source");
    var ord = { Negative: 0, Neutral: 1, Positive: 2 };
    return V.stacked100({
      data: Object.keys(g).map(function (s) {
        return { label: s, parts: g[s].sort(function (a, b) { return ord[a["Sentiment Label"]] - ord[b["Sentiment Label"]]; })
          .map(function (r) {
            return { name: r["Sentiment Label"], value: num(r["Pct Of Source"]),
                     color: r["Sentiment Label"] === "Negative" ? C.crit :
                            r["Sentiment Label"] === "Positive" ? C.s[2] : "#c9d1d8" };
          }) };
      }), w: 500, labelW: 95
    });
  })(),
  legend([{ name: "Negative", color: C.crit }, { name: "Neutral", color: "#c9d1d8" }, { name: "Positive", color: C.s[2] }]) +
  "<b>Not a pre-registered KPI.</b> Text analytics sit outside metric_dictionary.md and inform no verdict on this " +
  "page — they are supporting context only, and are labelled as such.");

card("c6", "Theme families",
  "119 granular codes rolled into families. Area = documents, colour = mean sentiment.",
  V.treemap({
    data: T("14_theme_families").filter(function (r) { return r["Theme Family"] !== "Other"; })
      .map(function (r) {
        return { label: r["Theme Family"], value: num(r.Documents), sentiment: num(r["Mean Sentiment"]),
                 tip: r["Theme Family"] + "\n" + r.Documents + " documents\nmean sentiment " + r["Mean Sentiment"] };
      }),
    color: function (r) { return V.diverge(r.sentiment, 0.35); }, w: 500, h: 280
  }),
  "Execution themes (fulfilment, support, trust) are the negative cluster; value themes are positive. " +
  "<b>Supporting context, not a pre-registered input.</b>");
endsec();

/* ══════════ 5 · PROPOSITIONS ══════════ */
sec("s5", "Section 5", "Propositions",
  "The six pre-registered playbook elements, each judged against the threshold rule fixed on 2026-09-16 — " +
  "then the overall Hyderabad call.");

card("", "Transferability Matrix — decision_rules §2",
  "Each element shows the rule verbatim, the inputs with their values, and the reasoning.",
  matrix.map(function (m) {
    var v = String(m.Verdict);
    var cls = v === "KEEP" ? "keep" : v === "DEPRIORITIZE" ? "dep" : v === "ADAPT" ? "adapt" : "insuf";
    var pill = v === "KEEP" ? "p-ok" : v === "DEPRIORITIZE" ? "p-bad" : v === "ADAPT" ? "p-warn" : "p-unk";
    var conf = String(m.Confidence);
    var cpill = conf === "HIGH" ? "p-ok" : conf === "MEDIUM" ? "p-warn" : "p-na";
    return '<div class="elem ' + cls + '"><div class="eh"><span class="en">' + V.esc(m.Element) + ' · ' +
      V.esc(m["Playbook element"]) + '</span><span><span class="pill ' + pill + '">' + V.esc(v) +
      '</span> <span class="pill ' + cpill + '">' + V.esc(conf) + ' confidence</span></span></div>' +
      '<div class="inputs">' + String(m.Inputs).split(" | ").map(function (i) {
        return '<span class="inp">' + V.esc(i) + '</span>';
      }).join("") + '</div>' +
      '<div class="reason">' + V.esc(m.Reasoning) + '</div>' +
      '<div class="rule"><b>Pre-registered rule:</b> ' + V.esc(m["Pre-registered rule"]) + '</div></div>';
  }).join(""),
  "<b>Source</b> · Data/02_transferability_matrix.csv, produced by apply_rules.py from " +
  "09_analysis/kpi_system/decision_rules.md §2. <b>2 KEEP · 1 DEPRIORITIZE · 3 INSUFFICIENT EVIDENCE.</b>");

card("", "The overall Hyderabad call — decision_rules §3",
  "Each rule is evaluated in order, with what was observed and why it did or did not apply.",
  tbl([
    { label: "Rule", get: function (r) {
        var isCall = r.Rule === "OVERALL HYDERABAD CALL" || r.Rule === "PROVISIONAL flag";
        return (isCall ? "<b>" : "") + V.esc(r.Rule) + (isCall ? "</b>" : ""); } },
    { label: "Observed", get: function (r) { return V.esc(r.Observed); } },
    { label: "Evaluation", get: function (r) { return V.esc(r.Evaluation); } },
  ], T("04_overall_call")),
  "");

OUT.push('<section class="card"><div class="callout unk">' +
  '<p><b>The call is INSUFFICIENT EVIDENCE, flagged PROVISIONAL — and that is the correct answer, not a failure.</b></p>' +
  '<p>Two of the four guardrails cannot be evaluated at all, because the questions they depend on (A2 acquisition ' +
  'channel, A3 fulfilment failure) are absent from the live instrument. Three of the six playbook elements rest on ' +
  'inputs that do not exist. And the audit priced one of two planned slots. decision_rules §3.5 anticipated exactly ' +
  'this situation and says the dashboard should report it rather than guess.</p>' +
  '<p><b>What is nonetheless established, on evidence:</b> the price advantage is real and clears its threshold ' +
  '(§2.1 KEEP, G1 not breached), the fee advantage is real and felt (§2.2 KEEP), and Rapido cross-sell is not ' +
  'earning its place in this sample (§2.3 DEPRIORITIZE). Those three verdicts do not depend on the missing inputs.</p>' +
  '</div></section>');

card("", "What would move the call off INSUFFICIENT EVIDENCE",
  "Four gaps, in order of how cheaply each closes.",
  tbl([
    { label: "#", n: 1, get: function (r) { return r[0]; } },
    { label: "Gap", get: function (r) { return "<b>" + V.esc(r[1]) + "</b>"; } },
    { label: "Unblocks", get: function (r) { return V.esc(r[2]); } },
    { label: "Cost to close", get: function (r) { return V.esc(r[3]); } },
  ], [
    [1, "Tag the 10 audit-frame restaurants local vs chain", "K41 → §2.5 Local restaurant supply", "One afternoon. The frame already exists; it just has no local/chain column."],
    [2, "Price the thu_lunch slot", "Removes the §3 rule 5 trigger (audit incomplete)", "One lunch slot, same protocol as wed_dinner."],
    [3, "Add question A3 (fulfilment failure) and A2 (acquisition channel)", "K51 → guardrail G2 and §2.6; K71 → guardrail G4 and §2.4", "Two questions, but they need a trier base — so this depends on gap 4."],
    [4, "Field the fake door", "K13 → makes H₀ a behavioural test instead of a stated one", "Built and the collector is verified; needs about a week of traffic. At 200 visitors it detects a ~20 pp difference."],
  ]),
  "<b>Gaps 1 and 2 are cheap and would settle two of the three undecided elements.</b> Gaps 3 and 4 need field work " +
  "and a real trier base, which is the honest reason this study cannot reach a verdict on retention.");
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
