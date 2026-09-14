/**
 * Fake-door event collector — hyd_vp_fakedoor_v1
 * Google Apps Script bound to a Google Sheet. Deploy as Web app:
 *   Execute as: Me   |   Who has access: Anyone
 * Receives one JSON event per POST (text/plain body) from prototype/index.html
 * and appends one row to the "events" sheet. Stores NO personal data:
 * Apps Script does not expose the sender's IP, and unknown fields are dropped.
 */

var SHEET_NAME = 'events';
var EXPERIMENT_ID = 'hyd_vp_fakedoor_v1';

var COLUMNS = [
  'received_at', 'experiment_id', 'page_version', 'variant_id', 'variant_key',
  'anon_visitor_id', 'anon_session_id', 'event_name', 'ts', 'time_since_load_ms',
  'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'referrer_domain',
  'device_type', 'is_qa', 'is_bot_suspect', 'payload_json'
];

var EVENT_NAMES = ['page_view', 'vp_view', 'scroll_50', 'cta_click', 'disclosure_view',
  'secondary_intent', 'secondary_skip', 'mini_survey_submit', 'mini_survey_skip',
  'survey_link_click', 'exit'];

// Whitelist of payload keys. Anything else is discarded before storage.
var PAYLOAD_KEYS = ['viewport_w', 'review_switch', 'trigger', 'pct', 'cta_position', 'from',
  'action', 'bill_food', 'bill_final', 'bill_gap_inr', 'bill_gap_pct',
  'seg_occupation', 'locality', 'orders_4wk', 'dwell_ms', 'max_scroll_pct', 'furthest_step'];

var UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

function doPost(e) {
  var lock = LockService.getScriptLock();
  try {
    var raw = (e && e.postData && e.postData.contents) ? e.postData.contents : '';
    if (!raw || raw.length > 5000) return respond_('rejected: empty or too large');
    var ev = JSON.parse(raw);

    if (ev.experiment_id !== EXPERIMENT_ID) return respond_('rejected: experiment_id');
    if (['A', 'B', 'C'].indexOf(ev.variant_id) === -1) return respond_('rejected: variant_id');
    if (EVENT_NAMES.indexOf(ev.event_name) === -1) return respond_('rejected: event_name');
    if (!UUID_RE.test(String(ev.anon_visitor_id)) || !UUID_RE.test(String(ev.anon_session_id))) return respond_('rejected: ids');

    var payload = {};
    var p = ev.payload || {};
    PAYLOAD_KEYS.forEach(function (k) {
      if (Object.prototype.hasOwnProperty.call(p, k)) {
        var v = p[k];
        payload[k] = (typeof v === 'string') ? v.slice(0, 60) : v;
      }
    });

    var row = COLUMNS.map(function (c) {
      if (c === 'received_at') return new Date().toISOString();
      if (c === 'payload_json') return JSON.stringify(payload);
      var v = ev[c];
      if (v === undefined || v === null) return '';
      return (typeof v === 'string') ? v.slice(0, 80) : v;
    });

    lock.waitLock(10000);
    var sheet = getSheet_();
    sheet.appendRow(row);
    return respond_('ok');
  } catch (err) {
    return respond_('error: ' + err);
  } finally {
    try { lock.releaseLock(); } catch (x) {}
  }
}

function doGet() {
  return respond_('collector alive: ' + EXPERIMENT_ID);
}

function getSheet_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
  }
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(COLUMNS);
    sheet.setFrozenRows(1);
  }
  return sheet;
}

function respond_(msg) {
  return ContentService.createTextOutput(msg).setMimeType(ContentService.MimeType.TEXT);
}

/** Run once from the editor to create the header row before launch. */
function setup() {
  getSheet_();
}
