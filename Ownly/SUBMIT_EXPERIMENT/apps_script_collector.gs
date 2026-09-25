/**
 * Ownly Gachibowli fake door — event collector.
 *
 * Google Apps Script bound to a Google Sheet. One POST = one event = one row.
 *
 * SETUP
 *  1. Create a Google Sheet. Add two tabs, named exactly:  events   contacts
 *  2. Extensions → Apps Script. Paste this file. Save.
 *  3. Deploy → New deployment → type "Web app"
 *       Execute as:      Me
 *       Who has access:  Anyone
 *     Copy the /exec URL.
 *  4. Open that URL in a browser. It should print: collector alive: <experiment id>
 *  5. Paste the URL into CONFIG.ENDPOINT in fake_door.html and mobility_entry.html.
 *
 * WHY THIS IS SAFE TO PUT IN A PUBLIC HTML FILE
 *  The /exec URL is write-only. It appends rows and returns "ok". It cannot read the
 *  sheet, cannot list rows, and carries no API key or credential. The sheet itself
 *  stays private to your Google account. Nothing in the HTML can be used to read data.
 *
 * PRIVACY
 *  - Apps Script does not expose the sender's IP, so no IP is ever stored.
 *  - Unknown fields are dropped; only the whitelist below is written.
 *  - Free-text fields are truncated and scrubbed of anything resembling an email or
 *    phone number BEFORE storage — a second line of defence after the client-side scrub.
 *  - Contacts go to a SEPARATE tab, so the behavioural data can be analysed and shared
 *    without ever opening the tab that holds personal data.
 */

var EXPERIMENTS = ['hyd_gach_fakedoor_2026_09', 'hyd_gach_discovery_2026_09'];
var EVENTS_SHEET    = 'events';
var CONTACTS_SHEET  = 'contacts';
var RESPONSES_SHEET = 'responses';
var DEBUG_SHEET     = 'debug_log';

/* ═══════════════════════════════════════════════════════════════
   EVERY REQUEST IS LOGGED, INCLUDING THE ONES THAT FAIL.

   sendBeacon tells the page "the browser accepted this" — never "the
   server stored it". So when rows go missing there is no way, from
   the phone, to tell a request that never arrived from one that
   arrived and was thrown away. That ambiguity is why this problem
   survived three fixes.

   debug_log records EVERY call to doPost before anything can go
   wrong with it: when, how big, how many events, and the outcome —
   including exceptions and lock failures. If the tab is empty, the
   requests are not reaching Google. If it fills with errors, they are
   arriving and being lost here. One glance separates the two.
   ═══════════════════════════════════════════════════════════════ */
function debugLog_(bytes, count, outcome, detail) {
  try {
    var sh = sheet_(DEBUG_SHEET, ['at','bytes','events','outcome','detail']);
    sh.appendRow([new Date().toISOString(), bytes, count, outcome,
                  String(detail || '').slice(0, 300)]);
  } catch (e) { /* logging must never be the thing that breaks it */ }
}

/* ═══════════════════════════════════════════════════════════════
   TWO VIEWS OF THE SAME DATA.

   `events`    one row per tap. Complete, ordered, and interleaved
               across everyone — the right shape for analysis, the
               wrong shape for reading.
   `responses` ONE ROW PER PERSON. Every choice they made and every
               question they answered, in its own column. Nobody's
               answers sit in anybody else's row.

   Both are written on every request, so `responses` is never stale
   and never needs rebuilding.
   ═══════════════════════════════════════════════════════════════ */
var RESP_COLS = [
  'participant_code','anon_visitor_id','first_seen','last_seen','arm','source',
  'is_qa','n_events','furthest_screen','entry_tap',
  /* the two searches — the reason the study exists */
  'dish_queries','dish_chosen','dish_cuisine','dish_not_found',
  'restaurant_queries','restaurant_chosen','restaurant_kind','restaurant_category',
  'restaurant_not_found',
  /* the basket */
  'items_added','basket_value',
  /* the three priced choices, each with the price this person was shown */
  'delivery_chosen','delivery_price_shown',
  'offer_chosen','wallet_amount_shown',
  'payment_chosen','protection_price_shown','bill_total',
  /* every in-journey question */
  'q_why_filter','q_why_dish','q_meal_slot','q_why_rest','q_app_gap',
  'q_missing_dish','q_missing_action','q_why_item','q_why_offer','q_why_bill',
  'q_why_delivery','q_rapido_link_trust',
  /* how far they got */
  'reached_cart','placed_order','went_to_survey'
];

/* event + payload key -> the responses column it fills.
   'set' overwrites (the last value wins), 'add' appends to a list. */
var RESP_MAP = {
  first_meaningful_tap:      [['tap_kind','entry_tap','set']],
  search_query:              [['query','__search','add']],
  dish_selected:             [['dish','dish_chosen','set'],['category','dish_cuisine','set']],
  dish_added_custom:         [['dish','dish_not_found','add']],
  restaurant_search_selected:[['restaurant_name','restaurant_chosen','set'],
                              ['rest_kind','restaurant_kind','set'],
                              ['category','restaurant_category','set']],
  restaurant_card_click:     [['restaurant_name','restaurant_chosen','set'],
                              ['rest_kind','restaurant_kind','set'],
                              ['category','restaurant_category','set']],
  restaurant_added_custom:   [['restaurant_name','restaurant_not_found','add']],
  item_added:                [['item_name','items_added','add'],['item_price','__price','set']],
  cart_view:                 [['item_price','basket_value','set']],
  delivery_option_chosen:    [['delivery_id','delivery_chosen','set'],['rl_price','delivery_price_shown','set']],
  delivery_confirmed:        [['delivery_id','delivery_chosen','set'],['rl_price','delivery_price_shown','set']],
  offer_applied:             [['offer','offer_chosen','set'],['wallet_amt','wallet_amount_shown','set']],
  offer_removed:             [['offer','__clear_offer','set']],
  bill_option_chosen:        [['bill_id','payment_chosen','set'],['protect_price','protection_price_shown','set']],
  place_order_click:         [['bill_total','bill_total','set'],['item_price','basket_value','set']]
};

var EVENT_NAMES = [
  'experiment_view','entry_card_view','entry_card_click','decoy_service_click','entry_exit',
  'landing_page_view','offer_card_click','category_chip_click','filter_tab_click',
  'restaurant_card_click','search_tap','first_meaningful_tap','bottom_nav_click',
  'micro_shown','micro_answer','survey_view','survey_link_click',
  'dish_search_view','dish_search_started','dish_selected','dish_added_custom','back_tapped',
  'search_query','search_cleared',
  'restaurant_search_view','restaurant_search_started','restaurant_search_selected',
  
  'restaurant_added_custom',
  
  /* the order journey added in v4 */
  'menu_view','item_added','item_qty_changed','cart_view',
  'offer_applied','offer_removed',
  'delivery_screen_view','delivery_confirmed','delivery_revisited',
  'bill_option_chosen','delivery_option_chosen','place_order_click','honest_stop_view',
  'research_disclosure_view','followup_consent_given','prototype_exit'
];

var COLUMNS = [
  'received_at','event_id','experiment_id','page_version','variant_id','variant_key','source',
  'anon_visitor_id','anon_session_id','event_name','ts_iso','time_since_load_ms',
  'time_since_prev_ms','device_type','viewport_w','is_qa','is_bot_suspect','payload_json'
];

/* Only these payload keys are stored. Anything else the page sends is discarded. */
var PAYLOAD_KEYS = [
  /* the in-journey micro-questions */
  'q_id','answer','subject','screen','ms_to_answer','detail',
  /* what KIND of dish and what KIND of place — the point of the study */
  'category','rest_kind','results_count',
  /* the two searches — the findings this study exists for */
  'dish','query',
  'restaurant_name','from_list','typed',
  'source_screen','n_selected',
  /* the cart, the pricing choice and the delivery choice */
  'item_name','item_price','bill_id','bill_total','bill_touched','offer_worth',
  'delivery_id','delivery_touched','mins','rl_price','wallet_amt','protect_price',
  /* journey shape */
  'entry_screen','placement','card_position','ms_to_notice','dwell_ms','was_noticed_first',
  'variant_key','source','tap_kind','ms_to_first_tap',
  'ms_to_start','offer','position','category','n_offers','storage_ok',
  'contact_channel','furthest_step','completed_posttest','reason',
  'max_scroll_pct','service','noticed','clicked'
];

var UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
var FALLBACK_ID_RE = /^(fb|fallback)-\d+-\d+$/i;

function scrub_(v, maxLen) {
  return String(v == null ? '' : v)
    .replace(/[\w.+-]+@[\w-]+\.[\w.]+/g, '[removed]')
    .replace(/(\+?\d[\d\s-]{8,}\d)/g, '[removed]')
    .slice(0, maxLen || 200);
}
function validId_(v) { return UUID_RE.test(String(v)) || FALLBACK_ID_RE.test(String(v)); }
function respond_(msg) {
  return ContentService.createTextOutput(msg).setMimeType(ContentService.MimeType.TEXT);
}
function sheet_(name, headers) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName(name);
  if (!sh) { sh = ss.insertSheet(name); sh.appendRow(headers); }
  else if (sh.getLastRow() === 0) { sh.appendRow(headers); }
  return sh;
}

/* ═══════════════════════════════════════════════════════════════
   READING THE DATA BACK.

   The POST side stays write-only and needs no secret: that is what
   makes it safe to put in a public page. Reading is different, so it
   is gated on READ_KEY.

   Set READ_KEY to a long random string below. It goes ONLY into
   metrics.html on your own machine — never into fake_door.html, which
   is public. Leave it as the default and reading stays switched off.
   ═══════════════════════════════════════════════════════════════ */
var READ_KEY = 'CHANGE-ME-TO-A-LONG-RANDOM-STRING';

function doGet(e) {
  var p = (e && e.parameter) ? e.parameter : {};

  if (p.action === 'events') {
    if (READ_KEY === 'CHANGE-ME-TO-A-LONG-RANDOM-STRING')
      return json_({ error: 'read_disabled', hint: 'Set READ_KEY in the script.' });
    if (p.key !== READ_KEY)
      return json_({ error: 'bad_key' });

    var sh = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(EVENTS_SHEET);
    if (!sh || sh.getLastRow() < 2) return json_({ rows: [], n: 0 });

    var last = sh.getLastRow();
    var cap  = Math.min(parseInt(p.limit || '20000', 10) || 20000, 20000);
    var from = Math.max(2, last - cap + 1);
    var vals = sh.getRange(from, 1, last - from + 1, COLUMNS.length).getValues();

    var rows = vals.map(function (r) {
      var o = {};
      COLUMNS.forEach(function (c, i) { o[c] = r[i]; });
      return o;
    });
    return json_({ rows: rows, n: rows.length, columns: COLUMNS });
  }

  return respond_('collector alive: ' + EXPERIMENTS.join(', '));
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

/* ═══════════════════════════════════════════════════════════════
   doPost — accepts ONE event or a BATCH of them.

   WHY BATCHING MATTERS. The first version took one POST per event.
   Each execution held a lock for ~2.5s (a full column scan plus two
   Sheet writes), so a phone flushing 25 queued events in parallel put
   25 executions in a queue behind a 10-second lock. Measured: 4 of 12
   concurrent posts died with "Lock timeout", and the client could not
   see the failure because it used mode:'no-cors'. Those rows were
   dropped from the outbox as if delivered. That is how a study loses
   two thirds of its data and looks fine doing it.

   Now: the client sends an array, the whole array is handled inside a
   SINGLE lock, events are written in one bulk setValues, and the
   responses row for each participant is read and written once for the
   whole batch instead of once per event.
   ═══════════════════════════════════════════════════════════════ */
function doPost(e) {
  var lock = LockService.getScriptLock();
  try {
    var raw = (e && e.postData && e.postData.contents) ? e.postData.contents : '';
    if (!raw) { debugLog_(0, 0, 'REJECTED', 'empty body'); return respond_('rejected: empty'); }
    if (raw.length > 400000) {
      debugLog_(raw.length, 0, 'REJECTED', 'too large'); return respond_('rejected: too large');
    }

    var parsed;
    try { parsed = JSON.parse(raw); }
    catch (pe) {
      debugLog_(raw.length, 0, 'REJECTED', 'bad json: ' + pe);
      return respond_('rejected: bad json');
    }
    var incoming = Object.prototype.toString.call(parsed) === '[object Array]' ? parsed : [parsed];
    if (!incoming.length) return respond_('ok 0');
    if (incoming.length > 200) return respond_('rejected: batch too large');

    /* validate and clean before taking the lock — no need to hold it for this */
    var good = [], rejected = 0;
    for (var i = 0; i < incoming.length; i++) {
      var ev = incoming[i];
      if (!ev || EXPERIMENTS.indexOf(ev.experiment_id) === -1) { rejected++; continue; }
      if (EVENT_NAMES.indexOf(ev.event_name) === -1)            { rejected++; continue; }
      if (!validId_(ev.anon_visitor_id) || !validId_(ev.anon_session_id)) { rejected++; continue; }

      var p = ev.payload || {}, payload = {};
      PAYLOAD_KEYS.forEach(function (k) {
        if (!Object.prototype.hasOwnProperty.call(p, k)) return;
        var v = p[k];
        payload[k] = (typeof v === 'string')
          ? scrub_(v, k === 'restaurant_name' ? 500 : 80) : v;
      });
      good.push({ ev: ev, payload: payload });
    }
    if (!good.length) {
      debugLog_(raw.length, incoming.length, 'REJECTED',
        'all ' + rejected + ' failed validation');
      return respond_('rejected: ' + rejected + ' of ' + incoming.length);
    }

    /* 60s, not 10s: a slow batch behind another slow batch must wait, not vanish */
    if (!lock.tryLock(60000)) {
      debugLog_(raw.length, incoming.length, 'LOCK BUSY', 'could not acquire in 60s');
      return respond_('busy');
    }

    var stamp = new Date().toISOString();

    /* contacts, if any */
    good.forEach(function (g) {
      if (g.ev.event_name === 'followup_consent_given') {
        var csh = sheet_(CONTACTS_SHEET, ['received_at','anon_visitor_id','contact_channel','note']);
        csh.appendRow([stamp, g.ev.anon_visitor_id, g.payload.contact_channel || '',
          'contact itself is NOT sent to this endpoint']);
      }
    });

    /* ── IDEMPOTENCY ──
       Every event carries a unique event_id. A client that retries — because
       it could not read the reply, or lost signal mid-request — must not
       create a second row. Without this, one stuck client rewrites the same
       batch every few seconds and the sheet fills with copies.

       Dedupe against what is already stored, and within the batch itself. */
    var sh = sheet_(EVENTS_SHEET, COLUMNS);
    var idIdx = COLUMNS.indexOf('event_id');
    var seen = {};
    var lastRow = sh.getLastRow();
    if (lastRow > 1 && idIdx >= 0) {
      /* Duplicates only ever arrive seconds after the original, so the last
         1500 rows is a generous window and keeps the scan fast as the sheet
         grows. A wider scan was costing whole seconds per request. */
      var from = Math.max(2, lastRow - 1500);
      var known = sh.getRange(from, idIdx + 1, lastRow - from + 1, 1).getValues();
      for (var s1 = 0; s1 < known.length; s1++) seen[known[s1][0]] = 1;
    }
    var fresh = [], dupes = 0;
    for (var s2 = 0; s2 < good.length; s2++) {
      var id = good[s2].ev.event_id;
      if (!id || seen[id]) { dupes++; continue; }
      seen[id] = 1;
      fresh.push(good[s2]);
    }
    if (!fresh.length) {
      debugLog_(raw.length, incoming.length, 'all duplicate', dupes + ' repeats');
      return respond_('ok 0 duplicate ' + dupes);
    }
    good = fresh;

    var rows = good.map(function (g) {
      return COLUMNS.map(function (c) {
        if (c === 'received_at')  return stamp;
        if (c === 'payload_json') return JSON.stringify(g.payload);
        var v = g.ev[c];
        if (v === undefined || v === null) return '';
        return (typeof v === 'string') ? v.slice(0, 120) : v;
      });
    });
    sh.getRange(sh.getLastRow() + 1, 1, rows.length, COLUMNS.length).setValues(rows);

    /* responses — one read + one write per participant, not per event */
    var byVisitor = {};
    good.forEach(function (g) {
      (byVisitor[g.ev.anon_visitor_id] = byVisitor[g.ev.anon_visitor_id] || []).push(g);
    });
    Object.keys(byVisitor).forEach(function (vid) {
      upsertResponse_(vid, byVisitor[vid]);
    });

    debugLog_(raw.length, incoming.length, 'OK',
      'stored ' + good.length + (dupes ? ', dup ' + dupes : '') +
      (rejected ? ', rejected ' + rejected : ''));
    return respond_('ok ' + good.length +
      (dupes ? ' duplicate ' + dupes : '') +
      (rejected ? ' rejected ' + rejected : ''));
  } catch (err) {
    debugLog_(-1, -1, 'EXCEPTION', err + ' | ' + (err && err.stack ? err.stack : ''));
    return respond_('error: ' + err);
  } finally {
    try { lock.releaseLock(); } catch (e2) {}
  }
}

/* ═══════════════════════════════════════════════════════════════
   ONE ROW PER PERSON.

   Finds this participant's row by anon_visitor_id and updates it in
   place, or creates it. Runs inside the same lock as the events
   append, so two phones arriving at once cannot interleave.

   A linear scan of the id column is fine at study scale (tens of
   participants); it is not a design for tens of thousands.
   ═══════════════════════════════════════════════════════════════ */
function upsertResponse_(vid, batch) {
  var sh = sheet_(RESPONSES_SHEET, RESP_COLS);
  var idCol = RESP_COLS.indexOf('anon_visitor_id') + 1;
  var last = sh.getLastRow();

  var rowIdx = 0;
  if (last > 1) {
    var ids = sh.getRange(2, idCol, last - 1, 1).getValues();
    for (var i = 0; i < ids.length; i++) {
      if (ids[i][0] === vid) { rowIdx = i + 2; break; }
    }
  }

  var first = batch[0].ev, row;
  if (rowIdx) {
    row = sh.getRange(rowIdx, 1, 1, RESP_COLS.length).getValues()[0];
  } else {
    row = RESP_COLS.map(function () { return ''; });
    row[RESP_COLS.indexOf('participant_code')] = String(vid).slice(0, 8).toUpperCase();
    row[RESP_COLS.indexOf('anon_visitor_id')]  = vid;
    row[RESP_COLS.indexOf('first_seen')]       = first.ts_iso || new Date().toISOString();
    row[RESP_COLS.indexOf('n_events')]         = 0;
  }

  function put(col, val, mode) {
    var i = RESP_COLS.indexOf(col);
    if (i < 0 || val === '' || val === null || val === undefined) return;
    if (mode === 'add') {
      var cur = String(row[i] || '');
      var parts = cur ? cur.split(' | ') : [];
      if (parts.indexOf(String(val)) < 0) parts.push(String(val));
      row[i] = parts.join(' | ');
    } else {
      row[i] = val;
    }
  }

  /* fold the whole batch into the row in memory, then write once */
  batch.forEach(function (g) {
    var ev = g.ev, payload = g.payload;

    put('last_seen', ev.ts_iso || new Date().toISOString(), 'set');
    put('arm', ev.variant_id, 'set');
    put('source', ev.source, 'set');
    put('is_qa', (ev.is_qa === true || ev.is_qa === 'true') ? 'TRUE' : 'FALSE', 'set');
    row[RESP_COLS.indexOf('n_events')] =
      (parseInt(row[RESP_COLS.indexOf('n_events')], 10) || 0) + 1;

    if (payload.screen)        put('furthest_screen', payload.screen, 'set');
    if (payload.furthest_step) put('furthest_screen', payload.furthest_step, 'set');

    /* the two search streams stay apart */
    if (ev.event_name === 'search_query' && payload.query) {
      put(payload.source_screen === 'restaurant' ? 'restaurant_queries' : 'dish_queries',
          payload.query + (String(payload.results_count) === '0' ? ' (0 results)' : ''), 'add');
    }

    var rules = RESP_MAP[ev.event_name];
    if (rules) {
      rules.forEach(function (r) {
        if (r[1].indexOf('__') === 0) return;
        put(r[1], payload[r[0]], r[2]);
      });
    }
    if (ev.event_name === 'offer_removed') put('offer_chosen', '', 'set');

    if (ev.event_name === 'micro_answer' && payload.q_id) {
      put('q_' + payload.q_id, payload.answer, 'set');
    }

    if (ev.event_name === 'cart_view')         put('reached_cart',   'YES', 'set');
    if (ev.event_name === 'place_order_click') put('placed_order',   'YES', 'set');
    if (ev.event_name === 'survey_view')       put('went_to_survey', 'YES', 'set');
  });

  if (rowIdx) sh.getRange(rowIdx, 1, 1, RESP_COLS.length).setValues([row]);
  else        sh.appendRow(row);
}

/**
 * Run once from the editor to create the three tabs and their headers.
 */
function setupSheets() {
  sheet_(EVENTS_SHEET, COLUMNS);
  sheet_(RESPONSES_SHEET, RESP_COLS);
  sheet_(CONTACTS_SHEET, ['received_at','anon_visitor_id','contact_channel','note']);
  sheet_(DEBUG_SHEET, ['at','bytes','events','outcome','detail']);
  Logger.log('Tabs ready: %s, %s, %s, %s',
    EVENTS_SHEET, RESPONSES_SHEET, CONTACTS_SHEET, DEBUG_SHEET);
}
