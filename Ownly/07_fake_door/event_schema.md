# Event Schema & Tracking Taxonomy — `hyd_vp_fakedoor_v1`

Machine-readable version: `events_schema.json`. Collector: `apps_script_collector.gs`. Analysis: `analyze_fakedoor.py`.

## Funnel

```
VISITOR ─────────────► page_view
   │
VALUE PROPOSITION VIEW ► vp_view        (hero ≥60% visible for 3 s, OR scroll_50, OR cta_click)
   │                    scroll_50       (user scrolled to ≥50% of page; diagnostic)
CTA CLICK ────────────► cta_click       (payload: cta_position hero|bottom)
   │
RESEARCH DISCLOSURE ──► disclosure_view (shown immediately on every CTA click)
   │
HIGHER-INTENT ACTION ─► secondary_intent (bill comparison completed)   | secondary_skip
   │
OPTIONAL CONTEXT ─────► mini_survey_submit                              | mini_survey_skip
   │
REDIRECT ─────────────► survey_link_click (to main Hyderabad survey)
                        exit            (pagehide; dwell, max scroll, furthest step)
```

Ethics ordering note: the disclosure appears at the moment of the CTA click, *before* the higher-intent action, so nobody takes the effortful step believing a real service exists.

## Common fields (every event)

| Field | Type | Example | Notes |
|---|---|---|---|
| `experiment_id` | string | `hyd_vp_fakedoor_v1` | Constant |
| `page_version` | string | `2026-09-14.1` | Bump on any copy change; analyse versions separately |
| `variant_id` | A/B/C | `B` | Random, sticky per browser |
| `variant_key` | string | `B_transparent_bill` | Human-readable |
| `anon_visitor_id` | UUID v4 | `3f0c…` | `localStorage`; **unit of analysis** |
| `anon_session_id` | UUID v4 | `a91e…` | `sessionStorage` |
| `event_name` | enum | `cta_click` | See table below |
| `ts` | ISO-8601 UTC | `2026-09-17T14:03:22.117Z` | Client clock |
| `time_since_load_ms` | int | `8412` | Since page load |
| `utm_source` / `utm_medium` / `utm_campaign` / `utm_content` | string ≤ 80 | `whatsapp` / `community_group` / `hyd_vp_fakedoor_v1` / `pg_telecomnagar_01` | First touch in session |
| `referrer_domain` | string | `l.instagram.com` | Hostname only |
| `device_type` | enum | `mobile` | Coarse, from UA pattern; UA string not stored |
| `is_qa` | bool | `false` | True in review mode, with `?qa`, or `?v=` |
| `is_bot_suspect` | bool | `false` | `navigator.webdriver` or crawler UA |
| `payload` | object | `{}` | Event-specific, whitelisted keys only |

Collector adds `received_at` (server time) and stores `payload` as `payload_json`.

## Events

| Event | Fires when | Payload | Once per page load? |
|---|---|---|---|
| `page_view` | Script runs | `viewport_w` | Yes (review switch re-fires, QA only) |
| `vp_view` | Hero ≥ 60% visible for 3 s, or scroll ≥ 50%, or CTA click | `trigger` | Yes |
| `scroll_50` | User scroll reaches 50% of page height | `pct` | Yes |
| `cta_click` | Either CTA tapped | `cta_position` | No (first used in analysis) |
| `disclosure_view` | Disclosure screen shown | `from` | Yes |
| `secondary_intent` | Bill comparison submitted with valid amounts | `action`, `bill_food`, `bill_final`, `bill_gap_inr`, `bill_gap_pct` | No (last used) |
| `secondary_skip` | "Skip this" tapped | — | Yes |
| `mini_survey_submit` | "Send answers" tapped | `seg_occupation`, `locality`, `orders_4wk` (`no_answer` if blank) | Yes |
| `mini_survey_skip` | "Skip" tapped | — | Yes |
| `survey_link_click` | Main-survey button tapped (sent by beacon) | — | Yes |
| `exit` | `pagehide` (sent by beacon) | `dwell_ms`, `max_scroll_pct`, `furthest_step` | Yes |

## Derived visitor-level variables (built in `analyze_fakedoor.py`)

| Variable | Rule |
|---|---|
| `vp` | any `vp_view` or `cta_click` |
| `cta` | any `cta_click` |
| `secondary` | any `secondary_intent` |
| `mini` | any `mini_survey_submit` |
| `survey_click` | any `survey_link_click` |
| `bounce` | no `cta_click`, no `scroll_50`, and max exit `dwell_ms` < 10,000 |
| `time_to_cta` | min `time_since_load_ms` over `cta_click` |
| `source` | first event's `utm_source`, else `ref:<referrer_domain>`, else `(direct/none)` |
| `seg_occupation`, `locality` | last `mini_survey_submit`; `not_asked` if none |
| `seg_freq` | `orders_4wk`: `1_3`→occasional, `4_7`→regular, `8_plus`→frequent, `0`→none, else unknown |

## UTM convention

`utm_campaign=hyd_vp_fakedoor_v1` always. `utm_source ∈ {whatsapp, telegram, linkedin, instagram, qr_poster}`; `utm_medium ∈ {community_group, post, story, offline}`; `utm_content` = group/venue/account code logged in a channel register (code → description, admin permission date). Never put the variant in the URL.

Example: `https://<host>/?utm_source=whatsapp&utm_medium=community_group&utm_campaign=hyd_vp_fakedoor_v1&utm_content=pg_telecomnagar_01`

## Master data-dictionary rows (for `08_clean_data/master_data_dictionary`)

Dataset name: `fakedoor_events` (raw, event grain) → `fakedoor_visitors` (cleaned, visitor grain). Raw file lands in `08_clean_data/raw/fakedoor_events_raw.csv`; exclusions in `08_clean_data/excluded/fakedoor_exclusions.csv`; analysis outputs in `09_analysis/fakedoor/`.
