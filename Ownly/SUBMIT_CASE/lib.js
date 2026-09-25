/* ═══════════════════════════════════════════════════════════════════
   Ownly BI — charting library.
   Hand-rolled SVG. No external dependencies, works from file://.
   Every chart returns an SVG string; tooltips work by data-tip delegation.
   ═══════════════════════════════════════════════════════════════════ */
(function (global) {
"use strict";

/* ---------- palette (CVD-validated categorical order) ---------- */
var C = {
  s: ["#2a78d6","#eb6834","#1baf7a","#eda100","#e87ba4","#008300","#4a3aa7","#e34948"],
  seq: ["#cde2fb","#9ec5f4","#6da7ec","#3987e5","#2a78d6","#1c5cab","#104281","#0d366b"],
  good:"#0ca30c", goodInk:"#006300", warn:"#fab219", warnInk:"#8a5d00", crit:"#d03b3b",
  ink:"#10151a", ink2:"#48535e", muted:"#7b8590", grid:"#e6eaee", axis:"#c3cad1",
  surface:"#ffffff", neutral:"#eef1f4"
};

/* ---------- formatting ---------- */
function fmt(v, d) { if (v === null || v === undefined || isNaN(v)) return "—"; return Number(v).toFixed(d === undefined ? 1 : d); }
function pct(v, d) { return fmt(v, d === undefined ? 1 : d) + "%"; }
function inr(v, d) { if (v === null || v === undefined || isNaN(v)) return "—"; var s = Number(v) < 0 ? "−" : ""; return s + "₹" + Math.abs(Number(v)).toLocaleString("en-IN", {minimumFractionDigits: d||0, maximumFractionDigits: d||0}); }
function cnt(v) { if (v === null || v === undefined || isNaN(v)) return "—"; return Number(v).toLocaleString("en-IN"); }
function esc(s) { return String(s === null || s === undefined ? "" : s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;"); }
function tip(s) { return 'data-tip="' + esc(s) + '"'; }

/* ---------- scales ---------- */
function niceMax(v) {
  if (v <= 0) return 1;
  var e = Math.pow(10, Math.floor(Math.log10(v))), f = v / e;
  var n = f <= 1 ? 1 : f <= 2 ? 2 : f <= 2.5 ? 2.5 : f <= 5 ? 5 : 10;
  return n * e;
}
function ticks(min, max, n) {
  n = n || 5; var out = [], step = (max - min) / n;
  for (var i = 0; i <= n; i++) out.push(min + i * step);
  return out;
}

/* ---------- diverging colour for sentiment / correlation ---------- */
function diverge(v, max) {
  max = max || 1; var t = Math.max(-1, Math.min(1, v / max));
  if (Math.abs(t) < 0.04) return "#eceff2";
  var a = Math.abs(t);
  var c1 = t > 0 ? [26,175,122] : [208,59,59];
  var mix = function (x) { return Math.round(236 + (x - 236) * Math.min(1, 0.25 + a * 0.9)); };
  return "rgb(" + mix(c1[0]) + "," + mix(c1[1]) + "," + mix(c1[2]) + ")";
}
function seqColor(t) { // t in 0..1
  var i = Math.max(0, Math.min(C.seq.length - 1, Math.round(t * (C.seq.length - 1))));
  return C.seq[i];
}

/* ═══════════════════════════════════════════════════════════════════
   CHARTS
   ═══════════════════════════════════════════════════════════════════ */

/* 1 ── horizontal bar, optional CI whiskers and value labels */
function barH(opts) {
  var d = opts.data, W = opts.w || 640, rowH = opts.rowH || 34, pad = opts.labelW || 190;
  var H = d.length * rowH + 30;
  var max = opts.max || niceMax(Math.max.apply(null, d.map(function (r) { return Math.max(r.value || 0, r.hi || 0); })));
  var x = function (v) { return pad + (v / max) * (W - pad - 60); };
  var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" class="chart">';
  ticks(0, max, 4).forEach(function (t) {
    s += '<line x1="' + x(t) + '" y1="6" x2="' + x(t) + '" y2="' + (H - 24) + '" stroke="' + C.grid + '"/>';
    s += '<text x="' + x(t) + '" y="' + (H - 8) + '" text-anchor="middle" class="ax">' + (opts.fmtAxis ? opts.fmtAxis(t) : fmt(t, 0)) + '</text>';
  });
  if (opts.ref !== undefined) {
    s += '<line x1="' + x(opts.ref) + '" y1="2" x2="' + x(opts.ref) + '" y2="' + (H - 24) + '" stroke="' + C.muted + '" stroke-dasharray="4 4"/>';
  }
  d.forEach(function (r, i) {
    var y = 10 + i * rowH, bh = Math.min(20, rowH - 12);
    var col = r.color || C.s[0];
    s += '<text x="0" y="' + (y + bh / 2 + 4) + '" class="lbl">' + esc(r.label) + '</text>';
    s += '<rect x="' + pad + '" y="' + y + '" width="' + Math.max(1, x(r.value) - pad) + '" height="' + bh + '" rx="3" fill="' + col + '" ' + tip(r.tip || (r.label + ": " + fmt(r.value))) + '/>';
    if (r.lo !== undefined && r.hi !== undefined) {
      s += '<line x1="' + x(r.lo) + '" y1="' + (y + bh / 2) + '" x2="' + x(r.hi) + '" y2="' + (y + bh / 2) + '" stroke="' + C.ink2 + '" stroke-width="1.5"/>';
      s += '<line x1="' + x(r.lo) + '" y1="' + (y + 3) + '" x2="' + x(r.lo) + '" y2="' + (y + bh - 3) + '" stroke="' + C.ink2 + '" stroke-width="1.5"/>';
      s += '<line x1="' + x(r.hi) + '" y1="' + (y + 3) + '" x2="' + x(r.hi) + '" y2="' + (y + bh - 3) + '" stroke="' + C.ink2 + '" stroke-width="1.5"/>';
    }
    var lx = Math.max(x(r.value), x(r.hi === undefined ? r.value : r.hi)) + 8;
    s += '<text x="' + lx + '" y="' + (y + bh / 2 + 4) + '" class="val">' + (r.vlabel !== undefined ? esc(r.vlabel) : fmt(r.value)) + '</text>';
  });
  return s + "</svg>";
}

/* 2 ── grouped bar (vertical) */
function barGrouped(opts) {
  var cats = opts.cats, series = opts.series, W = opts.w || 640, H = opts.h || 260;
  var L = 46, B = 46, T = 12, R = 10;
  var max = opts.max || niceMax(Math.max.apply(null, series.reduce(function (a, s) { return a.concat(s.values); }, [])));
  var bw = (W - L - R) / cats.length, gw = bw * 0.72 / series.length;
  var y = function (v) { return T + (1 - v / max) * (H - T - B); };
  var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" class="chart">';
  ticks(0, max, 4).forEach(function (t) {
    s += '<line x1="' + L + '" y1="' + y(t) + '" x2="' + (W - R) + '" y2="' + y(t) + '" stroke="' + C.grid + '"/>';
    s += '<text x="' + (L - 8) + '" y="' + (y(t) + 4) + '" text-anchor="end" class="ax">' + fmt(t, 0) + '</text>';
  });
  cats.forEach(function (c, i) {
    var x0 = L + i * bw + bw * 0.14;
    series.forEach(function (ser, j) {
      var v = ser.values[i], h = Math.max(1, (H - T - B) - (y(v) - T));
      s += '<rect x="' + (x0 + j * gw) + '" y="' + y(v) + '" width="' + (gw - 2) + '" height="' + h + '" rx="3" fill="' + (ser.color || C.s[j]) + '" ' + tip(c + " · " + ser.name + ": " + fmt(v)) + '/>';
    });
    s += '<text x="' + (L + i * bw + bw / 2) + '" y="' + (H - B + 16) + '" text-anchor="middle" class="ax">' + esc(c) + '</text>';
  });
  return s + "</svg>";
}

/* 3 ── 100% stacked bar (horizontal rows) */
function stacked100(opts) {
  var rows = opts.data, W = opts.w || 640, rowH = 40, pad = opts.labelW || 120;
  var H = rows.length * rowH + 26;
  var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" class="chart">';
  rows.forEach(function (r, i) {
    var y = 10 + i * rowH, tot = r.parts.reduce(function (a, p) { return a + p.value; }, 0) || 1, x = pad;
    s += '<text x="0" y="' + (y + 18) + '" class="lbl">' + esc(r.label) + '</text>';
    r.parts.forEach(function (p, j) {
      var w = (p.value / tot) * (W - pad - 10);
      if (w <= 0) return;
      s += '<rect x="' + x + '" y="' + y + '" width="' + Math.max(0, w - 2) + '" height="22" rx="2" fill="' + (p.color || C.s[j]) + '" ' + tip(r.label + " · " + p.name + ": " + fmt(p.value, 1) + "%") + '/>';
      if (w > 42) s += '<text x="' + (x + w / 2 - 1) + '" y="' + (y + 15) + '" text-anchor="middle" class="inbar">' + fmt(p.value, 0) + '%</text>';
      x += w;
    });
  });
  return s + "</svg>";
}

/* 4 ── waterfall */
function waterfall(opts) {
  var d = opts.data, W = opts.w || 640, H = opts.h || 300, L = 54, B = 58, T = 16, R = 12;
  var run = 0, pts = [], min = 0, max = 0;
  d.forEach(function (r) {
    if (r.total) { pts.push({ label: r.label, from: 0, to: run, total: true, value: run }); }
    else { pts.push({ label: r.label, from: run, to: run + r.value, value: r.value }); run += r.value; }
    min = Math.min(min, run); max = Math.max(max, run);
  });
  max = niceMax(max * 1.08); min = min < 0 ? -niceMax(-min * 1.15) : 0;
  var y = function (v) { return T + (1 - (v - min) / (max - min)) * (H - T - B); };
  var bw = (W - L - R) / pts.length;
  var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" class="chart">';
  ticks(min, max, 5).forEach(function (t) {
    s += '<line x1="' + L + '" y1="' + y(t) + '" x2="' + (W - R) + '" y2="' + y(t) + '" stroke="' + C.grid + '"/>';
    s += '<text x="' + (L - 8) + '" y="' + (y(t) + 4) + '" text-anchor="end" class="ax">' + (opts.fmtAxis ? opts.fmtAxis(t) : fmt(t, 0)) + '</text>';
  });
  if (min < 0) s += '<line x1="' + L + '" y1="' + y(0) + '" x2="' + (W - R) + '" y2="' + y(0) + '" stroke="' + C.axis + '" stroke-width="1.5"/>';
  pts.forEach(function (p, i) {
    var x0 = L + i * bw + bw * 0.18, w = bw * 0.64;
    var yt = y(Math.max(p.from, p.to)), yb = y(Math.min(p.from, p.to));
    var col = p.total ? C.s[0] : (p.value >= 0 ? C.good : C.crit);
    s += '<rect x="' + x0 + '" y="' + yt + '" width="' + w + '" height="' + Math.max(2, yb - yt) + '" rx="3" fill="' + col + '" ' + tip(p.label + ": " + (opts.fmtAxis ? opts.fmtAxis(p.value) : fmt(p.value))) + '/>';
    if (i < pts.length - 1) s += '<line x1="' + (x0 + w) + '" y1="' + y(p.to) + '" x2="' + (x0 + bw) + '" y2="' + y(p.to) + '" stroke="' + C.axis + '" stroke-dasharray="3 3"/>';
    s += '<text x="' + (x0 + w / 2) + '" y="' + (yt - 6) + '" text-anchor="middle" class="val">' + (opts.fmtAxis ? opts.fmtAxis(p.total ? p.value : p.value) : fmt(p.value)) + '</text>';
    var words = String(p.label).split(" ");
    var line1 = words.slice(0, 2).join(" "), line2 = words.slice(2).join(" ");
    s += '<text x="' + (x0 + w / 2) + '" y="' + (H - B + 16) + '" text-anchor="middle" class="ax">' + esc(line1) + '</text>';
    if (line2) s += '<text x="' + (x0 + w / 2) + '" y="' + (H - B + 29) + '" text-anchor="middle" class="ax">' + esc(line2) + '</text>';
  });
  return s + "</svg>";
}

/* 5 ── funnel */
function funnel(opts) {
  var d = opts.data, W = opts.w || 560, stepH = 56, H = d.length * stepH + 18;
  var max = d[0].value || 1;
  var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" class="chart">';
  d.forEach(function (r, i) {
    var w = Math.max(6, (r.value / max) * (W - 200)), x0 = 150, y = 10 + i * stepH;
    s += '<text x="0" y="' + (y + 22) + '" class="lbl">' + esc(r.label) + '</text>';
    s += '<rect x="' + x0 + '" y="' + y + '" width="' + w + '" height="30" rx="4" fill="' + seqColor(1 - i / Math.max(1, d.length - 1) * 0.65) + '" ' + tip(r.label + ": " + fmt(r.value, 1) + "% (" + r.k + " of " + r.n + ")") + '/>';
    s += '<text x="' + (x0 + w + 10) + '" y="' + (y + 21) + '" class="val">' + fmt(r.value, 1) + '%</text>';
    s += '<text x="' + (x0 + w + 62) + '" y="' + (y + 21) + '" class="ax">' + r.k + " of " + r.n + '</text>';
    if (i > 0) {
      var drop = d[i - 1].value ? (100 * (1 - r.value / d[i - 1].value)) : 0;
      s += '<text x="' + x0 + '" y="' + (y - 5) + '" class="ax" fill="' + C.crit + '">↓ ' + fmt(drop, 0) + '% drop</text>';
    }
  });
  return s + "</svg>";
}

/* 6 ── line / area, multi-series, optional dashed tail */
function lineChart(opts) {
  var xs = opts.x, series = opts.series, W = opts.w || 680, H = opts.h || 250;
  var L = 48, B = 42, T = 14, R = 14;
  var all = series.reduce(function (a, s) { return a.concat(s.values.filter(function (v) { return v !== null; })); }, []);
  var max = opts.max !== undefined ? opts.max : niceMax(Math.max.apply(null, all));
  var min = opts.min !== undefined ? opts.min : Math.min(0, Math.min.apply(null, all));
  var px = function (i) { return L + (xs.length === 1 ? 0.5 : i / (xs.length - 1)) * (W - L - R); };
  var py = function (v) { return T + (1 - (v - min) / (max - min || 1)) * (H - T - B); };
  var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" class="chart">';
  ticks(min, max, 4).forEach(function (t) {
    s += '<line x1="' + L + '" y1="' + py(t) + '" x2="' + (W - R) + '" y2="' + py(t) + '" stroke="' + C.grid + '"/>';
    s += '<text x="' + (L - 8) + '" y="' + (py(t) + 4) + '" text-anchor="end" class="ax">' + (opts.fmtAxis ? opts.fmtAxis(t) : fmt(t, 0)) + '</text>';
  });
  if (min < 0) s += '<line x1="' + L + '" y1="' + py(0) + '" x2="' + (W - R) + '" y2="' + py(0) + '" stroke="' + C.axis + '"/>';
  var every = Math.max(1, Math.ceil(xs.length / 9));
  xs.forEach(function (lx, i) {
    if (i % every === 0 || i === xs.length - 1)
      s += '<text x="' + px(i) + '" y="' + (H - B + 18) + '" text-anchor="middle" class="ax">' + esc(lx) + '</text>';
  });
  series.forEach(function (ser, si) {
    var col = ser.color || C.s[si], dpath = "", apath = "", started = false;
    ser.values.forEach(function (v, i) {
      if (v === null || v === undefined) return;
      dpath += (started ? "L" : "M") + px(i) + " " + py(v);
      apath += (started ? "L" : "M" + px(i) + " " + py(min) + "L") + px(i) + " " + py(v);
      started = true;
    });
    if (ser.area && started) s += '<path d="' + apath + 'L' + px(ser.values.length - 1) + ' ' + py(min) + 'Z" fill="' + col + '" opacity="0.12"/>';
    s += '<path d="' + dpath + '" fill="none" stroke="' + col + '" stroke-width="2" stroke-linejoin="round"' + (ser.dashed ? ' stroke-dasharray="5 4"' : '') + '/>';
    if (ser.dots !== false) ser.values.forEach(function (v, i) {
      if (v === null || v === undefined) return;
      s += '<circle cx="' + px(i) + '" cy="' + py(v) + '" r="3.6" fill="' + col + '" stroke="#fff" stroke-width="1.4" ' + tip(xs[i] + " · " + ser.name + ": " + (opts.fmtTip ? opts.fmtTip(v) : fmt(v, 2))) + '/>';
    });
  });
  return s + "</svg>";
}

/* 7 ── scatter with optional fitted line and size channel */
function scatter(opts) {
  var d = opts.data, W = opts.w || 620, H = opts.h || 300, L = 54, B = 46, T = 14, R = 16;
  var xmax = opts.xmax || niceMax(Math.max.apply(null, d.map(function (p) { return p.x; })));
  var xmin = opts.xmin !== undefined ? opts.xmin : 0;
  var ymax = opts.ymax || niceMax(Math.max.apply(null, d.map(function (p) { return p.y; })));
  var ymin = opts.ymin !== undefined ? opts.ymin : 0;
  var px = function (v) { return L + (v - xmin) / (xmax - xmin || 1) * (W - L - R); };
  var py = function (v) { return T + (1 - (v - ymin) / (ymax - ymin || 1)) * (H - T - B); };
  var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" class="chart">';
  ticks(ymin, ymax, 4).forEach(function (t) {
    s += '<line x1="' + L + '" y1="' + py(t) + '" x2="' + (W - R) + '" y2="' + py(t) + '" stroke="' + C.grid + '"/>';
    s += '<text x="' + (L - 8) + '" y="' + (py(t) + 4) + '" text-anchor="end" class="ax">' + (opts.fmtY ? opts.fmtY(t) : fmt(t, 0)) + '</text>';
  });
  ticks(xmin, xmax, 5).forEach(function (t) {
    s += '<text x="' + px(t) + '" y="' + (H - B + 18) + '" text-anchor="middle" class="ax">' + (opts.fmtX ? opts.fmtX(t) : fmt(t, 0)) + '</text>';
  });
  if (opts.line) {
    var dp = "";
    opts.line.forEach(function (p, i) { dp += (i ? "L" : "M") + px(p.x) + " " + py(p.y); });
    s += '<path d="' + dp + '" fill="none" stroke="' + (opts.lineColor || C.s[1]) + '" stroke-width="2"' + (opts.lineDashed ? ' stroke-dasharray="5 4"' : '') + '/>';
  }
  d.forEach(function (p, i) {
    var r = p.r || 6;
    s += '<circle cx="' + px(p.x) + '" cy="' + py(p.y) + '" r="' + r + '" fill="' + (p.color || C.s[0]) + '" fill-opacity="0.78" stroke="#fff" stroke-width="1.4" ' + tip(p.tip || (fmt(p.x) + ", " + fmt(p.y))) + '/>';
    if (p.label) s += '<text x="' + px(p.x) + '" y="' + (py(p.y) - r - 5) + '" text-anchor="middle" class="ax">' + esc(p.label) + '</text>';
  });
  if (opts.xlab) s += '<text x="' + ((L + W - R) / 2) + '" y="' + (H - 4) + '" text-anchor="middle" class="axlab">' + esc(opts.xlab) + '</text>';
  if (opts.ylab) s += '<text transform="translate(12,' + ((T + H - B) / 2) + ') rotate(-90)" text-anchor="middle" class="axlab">' + esc(opts.ylab) + '</text>';
  return s + "</svg>";
}

/* 8 ── heatmap (matrix) */
function heatmap(opts) {
  var rows = opts.rows, cols = opts.cols, get = opts.get, W = opts.w || 700;
  var L = opts.labelW || 160, T = opts.headH || 74;
  var cw = (W - L - 8) / cols.length, ch = opts.cellH || 30;
  var H = T + rows.length * ch + 10;
  var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" class="chart">';
  cols.forEach(function (c, j) {
    s += '<text transform="translate(' + (L + j * cw + cw / 2) + ',' + (T - 8) + ') rotate(-38)" text-anchor="start" class="ax">' + esc(c) + '</text>';
  });
  rows.forEach(function (r, i) {
    s += '<text x="0" y="' + (T + i * ch + ch / 2 + 4) + '" class="lbl">' + esc(String(r).length > 30 ? String(r).slice(0, 29) + "…" : r) + '</text>';
    cols.forEach(function (c, j) {
      var v = get(r, c);
      var fill = v === null || v === undefined ? C.neutral : (opts.color ? opts.color(v) : diverge(v.v !== undefined ? v.v : v, opts.max));
      var lab = v === null || v === undefined ? "" : (opts.label ? opts.label(v) : fmt(v, 2));
      s += '<rect x="' + (L + j * cw) + '" y="' + (T + i * ch) + '" width="' + (cw - 2) + '" height="' + (ch - 2) + '" rx="2" fill="' + fill + '" ' + tip((opts.tip ? opts.tip(r, c, v) : r + " × " + c + ": " + lab)) + '/>';
      if (lab && cw > 40) s += '<text x="' + (L + j * cw + cw / 2 - 1) + '" y="' + (T + i * ch + ch / 2 + 3) + '" text-anchor="middle" class="cell">' + esc(lab) + '</text>';
    });
  });
  return s + "</svg>";
}

/* 9 ── treemap (squarified-ish slice/dice) */
function treemap(opts) {
  var d = opts.data.slice().sort(function (a, b) { return b.value - a.value; });
  var W = opts.w || 640, H = opts.h || 300;
  var total = d.reduce(function (a, r) { return a + r.value; }, 0) || 1;
  var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" class="chart">';
  var x = 0, y = 0, w = W, h = H, i = 0;
  while (i < d.length) {
    var horiz = w >= h;
    var remaining = d.slice(i).reduce(function (a, r) { return a + r.value; }, 0) || 1;
    var rowCount = Math.max(1, Math.min(d.length - i, Math.round(Math.sqrt(d.length - i))));
    var row = d.slice(i, i + rowCount);
    var rowVal = row.reduce(function (a, r) { return a + r.value; }, 0);
    var band = (horiz ? w : h) * (rowVal / remaining);
    var off = 0;
    row.forEach(function (r, k) {
      var frac = r.value / (rowVal || 1);
      var cx, cy, cw, chh;
      if (horiz) { cw = band; chh = h * frac; cx = x; cy = y + off; off += chh; }
      else { cw = w * frac; chh = band; cx = x + off; cy = y; off += cw; }
      var col = opts.color ? opts.color(r) : seqColor(0.25 + 0.7 * (r.value / d[0].value));
      s += '<rect x="' + cx + '" y="' + cy + '" width="' + Math.max(0, cw - 2) + '" height="' + Math.max(0, chh - 2) + '" rx="3" fill="' + col + '" ' + tip(r.tip || (r.label + ": " + cnt(r.value))) + '/>';
      if (cw > 66 && chh > 28) {
        s += '<text x="' + (cx + 8) + '" y="' + (cy + 19) + '" class="tmlab">' + esc(String(r.label).length > 20 ? String(r.label).slice(0, 19) + "…" : r.label) + '</text>';
        if (chh > 42) s += '<text x="' + (cx + 8) + '" y="' + (cy + 36) + '" class="tmval">' + cnt(r.value) + '</text>';
      }
    });
    if (horiz) { x += band; w -= band; } else { y += band; h -= band; }
    i += rowCount;
  }
  return s + "</svg>";
}

/* 10 ── box plot (horizontal, multiple) */
function boxplot(opts) {
  var d = opts.data, W = opts.w || 620, rowH = 54, pad = opts.labelW || 150;
  var H = d.length * rowH + 30;
  var all = d.reduce(function (a, r) { return a.concat([r.box.min, r.box.max]).concat(r.box.outliers || []); }, []);
  var max = opts.max || niceMax(Math.max.apply(null, all));
  var x = function (v) { return pad + (v / max) * (W - pad - 30); };
  var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" class="chart">';
  ticks(0, max, 5).forEach(function (t) {
    s += '<line x1="' + x(t) + '" y1="6" x2="' + x(t) + '" y2="' + (H - 24) + '" stroke="' + C.grid + '"/>';
    s += '<text x="' + x(t) + '" y="' + (H - 8) + '" text-anchor="middle" class="ax">' + (opts.fmtAxis ? opts.fmtAxis(t) : fmt(t, 0)) + '</text>';
  });
  d.forEach(function (r, i) {
    var b = r.box, y = 14 + i * rowH, cy = y + 14, col = r.color || C.s[0];
    s += '<text x="0" y="' + (cy + 4) + '" class="lbl">' + esc(r.label) + '</text>';
    s += '<line x1="' + x(b.min) + '" y1="' + cy + '" x2="' + x(b.q1) + '" y2="' + cy + '" stroke="' + C.ink2 + '"/>';
    s += '<line x1="' + x(b.q3) + '" y1="' + cy + '" x2="' + x(b.max) + '" y2="' + cy + '" stroke="' + C.ink2 + '"/>';
    s += '<line x1="' + x(b.min) + '" y1="' + (cy - 7) + '" x2="' + x(b.min) + '" y2="' + (cy + 7) + '" stroke="' + C.ink2 + '"/>';
    s += '<line x1="' + x(b.max) + '" y1="' + (cy - 7) + '" x2="' + x(b.max) + '" y2="' + (cy + 7) + '" stroke="' + C.ink2 + '"/>';
    s += '<rect x="' + x(b.q1) + '" y="' + (cy - 12) + '" width="' + Math.max(2, x(b.q3) - x(b.q1)) + '" height="24" rx="3" fill="' + col + '" fill-opacity="0.32" stroke="' + col + '" ' + tip(r.label + " — min " + fmt(b.min, 0) + " · Q1 " + fmt(b.q1, 0) + " · median " + fmt(b.med, 0) + " · Q3 " + fmt(b.q3, 0) + " · max " + fmt(b.max, 0) + " (n=" + b.n + ")") + '/>';
    s += '<line x1="' + x(b.med) + '" y1="' + (cy - 12) + '" x2="' + x(b.med) + '" y2="' + (cy + 12) + '" stroke="' + col + '" stroke-width="2.5"/>';
    (b.outliers || []).forEach(function (o) {
      s += '<circle cx="' + x(o) + '" cy="' + cy + '" r="3.2" fill="none" stroke="' + C.crit + '" stroke-width="1.4" ' + tip("Outlier: " + fmt(o, 0)) + '/>';
    });
    s += '<text x="' + (x(b.med)) + '" y="' + (cy + 26) + '" text-anchor="middle" class="ax">med ' + (opts.fmtAxis ? opts.fmtAxis(b.med) : fmt(b.med, 0)) + '</text>';
  });
  return s + "</svg>";
}

/* 11 ── histogram */
function histogram(opts) {
  var vals = opts.values.filter(function (v) { return v !== null && !isNaN(v); });
  var W = opts.w || 620, H = opts.h || 230, L = 44, B = 40, T = 12, R = 12;
  if (!vals.length) return '<svg viewBox="0 0 10 10"></svg>';
  var lo = opts.min !== undefined ? opts.min : Math.min.apply(null, vals);
  var hi = opts.max !== undefined ? opts.max : Math.max.apply(null, vals);
  var nb = opts.bins || 10, bw = (hi - lo) / nb || 1;
  var bins = new Array(nb).fill(0);
  vals.forEach(function (v) { var i = Math.min(nb - 1, Math.max(0, Math.floor((v - lo) / bw))); bins[i]++; });
  var maxc = niceMax(Math.max.apply(null, bins));
  var y = function (c) { return T + (1 - c / maxc) * (H - T - B); };
  var cw = (W - L - R) / nb;
  var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" class="chart">';
  ticks(0, maxc, 4).forEach(function (t) {
    s += '<line x1="' + L + '" y1="' + y(t) + '" x2="' + (W - R) + '" y2="' + y(t) + '" stroke="' + C.grid + '"/>';
    s += '<text x="' + (L - 8) + '" y="' + (y(t) + 4) + '" text-anchor="end" class="ax">' + fmt(t, 0) + '</text>';
  });
  bins.forEach(function (c, i) {
    var x0 = L + i * cw;
    if (c > 0) s += '<rect x="' + (x0 + 1) + '" y="' + y(c) + '" width="' + (cw - 3) + '" height="' + Math.max(1, (H - T - B) - (y(c) - T)) + '" rx="2" fill="' + (opts.color || C.s[0]) + '" ' + tip((opts.fmtAxis ? opts.fmtAxis(lo + i * bw) : fmt(lo + i * bw, 0)) + " – " + (opts.fmtAxis ? opts.fmtAxis(lo + (i + 1) * bw) : fmt(lo + (i + 1) * bw, 0)) + ": " + c) + '/>';
    if (i % Math.ceil(nb / 6) === 0) s += '<text x="' + x0 + '" y="' + (H - B + 17) + '" text-anchor="middle" class="ax">' + (opts.fmtAxis ? opts.fmtAxis(lo + i * bw) : fmt(lo + i * bw, 0)) + '</text>';
  });
  return s + "</svg>";
}

/* 12 ── donut */
function donut(opts) {
  var d = opts.data, S = opts.size || 210, r = S / 2 - 6, ri = r * 0.6, cx = S / 2, cy = S / 2;
  var total = d.reduce(function (a, x) { return a + x.value; }, 0) || 1, a0 = -Math.PI / 2;
  var s = '<svg viewBox="0 0 ' + S + ' ' + S + '" class="chart">';
  d.forEach(function (x, i) {
    var a1 = a0 + (x.value / total) * Math.PI * 2, large = (a1 - a0) > Math.PI ? 1 : 0;
    var p = ["M", cx + r * Math.cos(a0), cy + r * Math.sin(a0),
             "A", r, r, 0, large, 1, cx + r * Math.cos(a1), cy + r * Math.sin(a1),
             "L", cx + ri * Math.cos(a1), cy + ri * Math.sin(a1),
             "A", ri, ri, 0, large, 0, cx + ri * Math.cos(a0), cy + ri * Math.sin(a0), "Z"].join(" ");
    s += '<path d="' + p + '" fill="' + (x.color || C.s[i]) + '" ' + tip(x.label + ": " + fmt(100 * x.value / total, 1) + "% (" + cnt(x.value) + ")") + '/>';
    a0 = a1;
  });
  if (opts.center) {
    s += '<text x="' + cx + '" y="' + (cy - 2) + '" text-anchor="middle" class="donutv">' + esc(opts.center) + '</text>';
    if (opts.centerSub) s += '<text x="' + cx + '" y="' + (cy + 16) + '" text-anchor="middle" class="ax">' + esc(opts.centerSub) + '</text>';
  }
  return s + "</svg>";
}

/* 13 ── slope chart (two points per series) */
function slope(opts) {
  var d = opts.data, W = opts.w || 460, H = opts.h || 300, T = 28, B = 34, L = 130, R = 130;
  var all = d.reduce(function (a, r) { return a.concat([r.left, r.right]); }, []);
  var max = niceMax(Math.max.apply(null, all)), min = 0;
  var y = function (v) { return T + (1 - (v - min) / (max - min)) * (H - T - B); };
  var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" class="chart">';
  s += '<text x="' + L + '" y="14" text-anchor="middle" class="axlab">' + esc(opts.leftLabel) + '</text>';
  s += '<text x="' + (W - R) + '" y="14" text-anchor="middle" class="axlab">' + esc(opts.rightLabel) + '</text>';
  s += '<line x1="' + L + '" y1="' + T + '" x2="' + L + '" y2="' + (H - B) + '" stroke="' + C.grid + '"/>';
  s += '<line x1="' + (W - R) + '" y1="' + T + '" x2="' + (W - R) + '" y2="' + (H - B) + '" stroke="' + C.grid + '"/>';
  d.forEach(function (r, i) {
    var col = r.color || C.s[i % C.s.length];
    s += '<line x1="' + L + '" y1="' + y(r.left) + '" x2="' + (W - R) + '" y2="' + y(r.right) + '" stroke="' + col + '" stroke-width="2" ' + tip(r.label + ": " + fmt(r.left, 1) + " → " + fmt(r.right, 1)) + '/>';
    s += '<circle cx="' + L + '" cy="' + y(r.left) + '" r="4.5" fill="' + col + '" stroke="#fff" stroke-width="1.4"/>';
    s += '<circle cx="' + (W - R) + '" cy="' + y(r.right) + '" r="4.5" fill="' + col + '" stroke="#fff" stroke-width="1.4"/>';
    s += '<text x="' + (L - 9) + '" y="' + (y(r.left) + 4) + '" text-anchor="end" class="ax">' + esc(r.label) + ' ' + fmt(r.left, 0) + '</text>';
    s += '<text x="' + (W - R + 9) + '" y="' + (y(r.right) + 4) + '" class="ax">' + fmt(r.right, 0) + '</text>';
  });
  return s + "</svg>";
}

/* 14 ── tornado (sensitivity) */
function tornado(opts) {
  var d = opts.data, W = opts.w || 640, rowH = 40, pad = opts.labelW || 210;
  var H = d.length * rowH + 30;
  var lo = Math.min.apply(null, d.map(function (r) { return Math.min(r.low, r.high); }));
  var hi = Math.max.apply(null, d.map(function (r) { return Math.max(r.low, r.high); }));
  var span = Math.max(Math.abs(lo), Math.abs(hi)) * 1.1 || 1;
  var x = function (v) { return pad + ((v + span) / (2 * span)) * (W - pad - 20); };
  var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" class="chart">';
  s += '<line x1="' + x(0) + '" y1="4" x2="' + x(0) + '" y2="' + (H - 24) + '" stroke="' + C.axis + '" stroke-width="1.5"/>';
  [-span, -span / 2, 0, span / 2, span].forEach(function (t) {
    s += '<text x="' + x(t) + '" y="' + (H - 8) + '" text-anchor="middle" class="ax">' + (opts.fmtAxis ? opts.fmtAxis(t) : fmt(t, 0)) + '</text>';
  });
  d.forEach(function (r, i) {
    var y = 10 + i * rowH, a = x(Math.min(r.low, r.high)), b = x(Math.max(r.low, r.high));
    s += '<text x="0" y="' + (y + 16) + '" class="lbl">' + esc(r.lever) + '</text>';
    s += '<rect x="' + a + '" y="' + y + '" width="' + Math.max(2, b - a) + '" height="22" rx="3" fill="' + (r.color || C.s[0]) + '" fill-opacity="0.85" ' + tip(r.lever + ": " + (opts.fmtAxis ? opts.fmtAxis(r.low) : fmt(r.low)) + " → " + (opts.fmtAxis ? opts.fmtAxis(r.high) : fmt(r.high)) + "  (range tested " + r.lo_val + "–" + r.hi_val + ")") + '/>';
  });
  return s + "</svg>";
}

/* 15 ── lollipop / dot plot */
function lollipop(opts) {
  var d = opts.data, W = opts.w || 620, rowH = 30, pad = opts.labelW || 190;
  var H = d.length * rowH + 28;
  var vals = d.reduce(function (a, r) { return a.concat([r.a, r.b]); }, []);
  var max = opts.max || niceMax(Math.max.apply(null, vals));
  var x = function (v) { return pad + (v / max) * (W - pad - 40); };
  var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" class="chart">';
  ticks(0, max, 4).forEach(function (t) {
    s += '<line x1="' + x(t) + '" y1="4" x2="' + x(t) + '" y2="' + (H - 22) + '" stroke="' + C.grid + '"/>';
    s += '<text x="' + x(t) + '" y="' + (H - 6) + '" text-anchor="middle" class="ax">' + (opts.fmtAxis ? opts.fmtAxis(t) : fmt(t, 0)) + '</text>';
  });
  d.forEach(function (r, i) {
    var y = 14 + i * rowH;
    s += '<text x="0" y="' + (y + 4) + '" class="lbl">' + esc(r.label) + '</text>';
    s += '<line x1="' + x(r.a) + '" y1="' + y + '" x2="' + x(r.b) + '" y2="' + y + '" stroke="' + C.axis + '" stroke-width="2"/>';
    s += '<circle cx="' + x(r.a) + '" cy="' + y + '" r="5.5" fill="' + (opts.colorA || C.s[0]) + '" ' + tip(r.label + " · " + (opts.nameA || "A") + ": " + fmt(r.a, 1)) + '/>';
    s += '<circle cx="' + x(r.b) + '" cy="' + y + '" r="5.5" fill="' + (opts.colorB || C.s[1]) + '" ' + tip(r.label + " · " + (opts.nameB || "B") + ": " + fmt(r.b, 1)) + '/>';
    s += '<text x="' + (Math.max(x(r.a), x(r.b)) + 10) + '" y="' + (y + 4) + '" class="val">' + (r.vlabel || ("+" + fmt(Math.abs(r.b - r.a), 0))) + '</text>';
  });
  return s + "</svg>";
}

/* 16 ── bullet / gauge */
function bullet(opts) {
  var W = opts.w || 300, H = 54, L = 0, R = 46;
  var max = opts.max || 100, v = opts.value, t = opts.target;
  var x = function (q) { return L + (q / max) * (W - L - R); };
  var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" class="chart">';
  s += '<rect x="0" y="16" width="' + (W - R) + '" height="20" rx="3" fill="' + C.neutral + '"/>';
  (opts.bands || []).forEach(function (b) {
    s += '<rect x="' + x(b.from) + '" y="16" width="' + (x(b.to) - x(b.from)) + '" height="20" fill="' + b.color + '" opacity="0.22"/>';
  });
  s += '<rect x="0" y="21" width="' + x(v) + '" height="10" rx="2" fill="' + (opts.color || C.s[0]) + '" ' + tip((opts.label || "") + ": " + fmt(v, 1)) + '/>';
  if (t !== undefined) s += '<line x1="' + x(t) + '" y1="13" x2="' + x(t) + '" y2="39" stroke="' + C.ink + '" stroke-width="2.5" ' + tip("Target: " + fmt(t, 1)) + '/>';
  s += '<text x="' + (W - R + 8) + '" y="' + 31 + '" class="val">' + (opts.vlabel || fmt(v, 1)) + '</text>';
  if (opts.label) s += '<text x="0" y="10" class="ax">' + esc(opts.label) + '</text>';
  return s + "</svg>";
}

/* ---------- tooltip wiring ---------- */
function initTooltip() {
  var el = document.createElement("div");
  el.className = "tooltip"; el.hidden = true;
  document.body.appendChild(el);
  document.addEventListener("mouseover", function (e) {
    var t = e.target.closest ? e.target.closest("[data-tip]") : null;
    if (!t) return;
    el.textContent = t.getAttribute("data-tip");
    el.hidden = false;
  });
  document.addEventListener("mousemove", function (e) {
    if (el.hidden) return;
    var w = el.offsetWidth, h = el.offsetHeight;
    var x = e.clientX + 14, y = e.clientY + 16;
    if (x + w > window.innerWidth - 10) x = e.clientX - w - 14;
    if (y + h > window.innerHeight - 10) y = e.clientY - h - 14;
    el.style.left = x + "px"; el.style.top = y + "px";
  });
  document.addEventListener("mouseout", function (e) {
    var t = e.target.closest ? e.target.closest("[data-tip]") : null;
    if (t) el.hidden = true;
  });
}

global.VZ = {
  C: C, fmt: fmt, pct: pct, inr: inr, cnt: cnt, esc: esc, tip: tip,
  niceMax: niceMax, diverge: diverge, seqColor: seqColor,
  barH: barH, barGrouped: barGrouped, stacked100: stacked100, waterfall: waterfall,
  funnel: funnel, lineChart: lineChart, scatter: scatter, heatmap: heatmap,
  treemap: treemap, boxplot: boxplot, histogram: histogram, donut: donut,
  slope: slope, tornado: tornado, lollipop: lollipop, bullet: bullet,
  initTooltip: initTooltip
};
})(window);
