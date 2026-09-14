/**
 * OPTIONAL alternative to link_randomizer.html: counter-based (block) randomisation.
 *
 * Why use it: pure random assignment can drift (e.g. 58/42) at n≈200. This version
 * cycles through a shuffled permutation of the versions, so counts never differ by
 * more than one full cycle. Use it if the daily balance check in
 * randomization_and_versions.md §5 shows imbalance beyond 55/45.
 *
 * Deploy: script.google.com → New project → paste → set FORMS below →
 * Deploy → New deployment → Web app → Execute as: Me; Who has access: Anyone.
 * Share the /exec URL (append ?utm_source=...&city=blr as needed).
 *
 * Apps Script web apps cannot send an HTTP 302, so we return a tiny HTML page
 * that navigates the top window.
 */

var FORMS = {
  hyd: [
    { version: 'V1', url: 'FORM_URL_V1', entry: { version: 'ENTRY_ID_V1_VERSION', token: 'ENTRY_ID_V1_TOKEN', start: 'ENTRY_ID_V1_START', source: 'ENTRY_ID_V1_SOURCE', campaign: 'ENTRY_ID_V1_CAMPAIGN' } },
    { version: 'V2', url: 'FORM_URL_V2', entry: { version: 'ENTRY_ID_V2_VERSION', token: 'ENTRY_ID_V2_TOKEN', start: 'ENTRY_ID_V2_START', source: 'ENTRY_ID_V2_SOURCE', campaign: 'ENTRY_ID_V2_CAMPAIGN' } },
    { version: 'V3', url: 'FORM_URL_V3', entry: { version: 'ENTRY_ID_V3_VERSION', token: 'ENTRY_ID_V3_TOKEN', start: 'ENTRY_ID_V3_START', source: 'ENTRY_ID_V3_SOURCE', campaign: 'ENTRY_ID_V3_CAMPAIGN' } },
    { version: 'V4', url: 'FORM_URL_V4', entry: { version: 'ENTRY_ID_V4_VERSION', token: 'ENTRY_ID_V4_TOKEN', start: 'ENTRY_ID_V4_START', source: 'ENTRY_ID_V4_SOURCE', campaign: 'ENTRY_ID_V4_CAMPAIGN' } }
  ],
  blr: [
    { version: 'B1', url: 'FORM_URL_B1', entry: { version: 'ENTRY_ID_B1_VERSION', token: 'ENTRY_ID_B1_TOKEN', start: 'ENTRY_ID_B1_START', source: 'ENTRY_ID_B1_SOURCE', campaign: 'ENTRY_ID_B1_CAMPAIGN' } },
    { version: 'B2', url: 'FORM_URL_B2', entry: { version: 'ENTRY_ID_B2_VERSION', token: 'ENTRY_ID_B2_TOKEN', start: 'ENTRY_ID_B2_START', source: 'ENTRY_ID_B2_SOURCE', campaign: 'ENTRY_ID_B2_CAMPAIGN' } }
  ]
};

function doGet(e) {
  var p = (e && e.parameter) || {};
  var city = p.city === 'blr' ? 'blr' : 'hyd';
  var pool = FORMS[city];
  var chosen = nextVersion_(city, pool);

  var source = clean_(p.utm_source, 'direct');
  var campaign = clean_(p.utm_campaign, 'none');

  var qs = [
    'usp=pp_url',
    chosen.entry.version + '=' + encodeURIComponent(chosen.version),
    chosen.entry.token + '=' + encodeURIComponent(Utilities.getUuid()),
    chosen.entry.start + '=' + encodeURIComponent(String(Date.now())),
    chosen.entry.source + '=' + encodeURIComponent(source),
    chosen.entry.campaign + '=' + encodeURIComponent(campaign)
  ].join('&');
  var target = chosen.url + '?' + qs;

  var html = '<!doctype html><meta name="robots" content="noindex">' +
    '<p style="font-family:sans-serif">Opening the survey… ' +
    '<a href="' + target + '" target="_top">Tap here if it does not open.</a></p>' +
    '<script>window.top.location.replace(' + JSON.stringify(target) + ');</script>';
  return HtmlService.createHtmlOutput(html)
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

/** Cycles through a freshly shuffled permutation of the pool; thread-safe via LockService. */
function nextVersion_(city, pool) {
  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var props = PropertiesService.getScriptProperties();
    var key = 'queue_' + city;
    var queue = JSON.parse(props.getProperty(key) || '[]');
    if (queue.length === 0) {
      queue = pool.map(function (_, i) { return i; });
      for (var i = queue.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var t = queue[i]; queue[i] = queue[j]; queue[j] = t;
      }
    }
    var idx = queue.shift();
    props.setProperty(key, JSON.stringify(queue));
    return pool[idx];
  } finally {
    lock.releaseLock();
  }
}

function clean_(s, fallback) {
  if (!s) return fallback;
  var c = String(s).replace(/[^A-Za-z0-9_\-.]/g, '').slice(0, 60);
  return c || fallback;
}
