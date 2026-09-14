"""Build 08_clean_data/master_data_dictionary.csv reproducibly from the canonical sources.

Sources: 03_hyderabad_survey/survey_variable_dictionary.csv (survey), DERIVED (below, mirrors
04_derive_metrics.py / 02_quality_flags.py), 10_dashboard/schema/*.csv (mart headers),
06_competitor_audit/audit_schema.csv, 07_fake_door/event_schema.md fields, coded review/interview headers.
Re-run whenever any source changes:  python make_master_dictionary.py
"""
from __future__ import annotations

import csv
from pathlib import Path

import config as C

P = C.PROJECT_ROOT
COLS = ["dataset", "variable_name", "label", "type", "allowed_values", "missing_codes", "source_file",
        "produced_by_script", "derived_formula", "hypothesis_linked"]

DERIVED = [  # variable, type, formula, hypotheses, script
    ("seg_occupation", "categorical", "seg_occupation_raw 1,2→student; 3→working_professional; 4→working_student; 5→other", "H6", "04"),
    ("seg_freq", "categorical", "scr_orders_4wk 1→occasional (1–3); 2→regular (4–7); 3,4→frequent (8+)", "H1.6;H6.4", "04"),
    ("blr_pilot_area", "binary", "city=blr and scr_area in (1 Koramangala, 2 HSR, 3 BTM)", "H9", "04"),
    ("own_aware_unaided", "binary", "human-coded mention of Ownly in beh_unaided_apps; regex first pass own_aware_unaided_auto until coded", "H7;H11.3", "04"),
    ("beh_platform_count", "integer", "number of options selected in beh_platforms_used_4wk", "H9.4", "04"),
    ("beh_multihome", "binary", "beh_platform_count >= 2", "H9.4;SRI", "04"),
    ("multihome5", "integer", "5 if beh_platform_count >= 2 else 1 (SRI component)", "SRI", "04"),
    ("beh_any_subscription", "binary", "Swiggy One or Zomato Gold or another membership selected", "H9.4;AS14", "04"),
    ("high_offer_dependency", "binary", "beh_offer_dependency in (3,4); 98→missing", "H1.5", "04"),
    ("ppi", "0-100", "((mean of pain_fee_reconsider_freq, pain_bill_unreasonable_freq, pain_menu_markup_belief[98→NA], beh_abandon_price_freq) − 1)/4×100; ≥3 items", "H1;H6.1;H9.2", "04"),
    ("sri", "0-100", "mean(r(bt_trial_intent), r(multihome5), r(6 − dec_habit_lock)), r(x)=(x−1)/4×100; all 3 required", "H1.7;D2", "04"),
    ("sri_no_intent", "0-100", "mean(r(multihome5), r(6 − dec_habit_lock)) — robustness / city comparison", "H1.7;H9", "04"),
    ("rss", "0-100", "% of price_vs_reliability DCE tasks where the more reliable AND pricier alternative was chosen; ≥2 tasks; Hyderabad only", "H4.1;H4.3", "04"),
    ("adi", "0-100", "(exp_fav_restaurant_needed − 1)/4×100", "H10.1", "04"),
    ("adi_high", "binary", "adi >= 75", "H10.1;D4", "04"),
    ("dec_switch_threshold_inr", "₹", "beh_switch_savings_required if code in (10,20,30,50,75,100)", "H2.3;D2", "04"),
    ("dec_switch_no_amount", "binary", "beh_switch_savings_required = 0 ('no amount') — never coded as ∞ or ₹0", "H2.3", "04"),
    ("dec_switch_dk", "binary", "beh_switch_savings_required = 98", "H2.3", "04"),
    ("exp_eta_max_lunch_min", "minutes", "exp_eta_max_lunch; 98→missing; 75 = 'more than 60'", "H3.2;H3.3", "04"),
    ("exp_eta_max_dinner_min", "minutes", "exp_eta_max_dinner; 98→missing", "H3.2;H3.3;D4", "04"),
    ("fee_reconsider_ge3", "binary", "pain_fee_reconsider_freq >= 3", "H1.1;D1", "04"),
    ("abandon_price_ge2", "binary", "beh_abandon_price_freq >= 2", "H1.4;D1", "04"),
    ("markup_top2", "binary", "pain_menu_markup_belief in (4,5); 98→missing", "H1.3", "04"),
    ("price_set", "binary", "any of first 4 price options selected in pain_top_frustrations", "H1.2", "04"),
    ("reliability_set", "binary", "'late delivery' or 'cancelled orders' selected in pain_top_frustrations", "H1.2", "04"),
    ("pain_incident_any_3m", "binary", "any pain_incidents_3m option except 'none of these'", "H4.3", "04"),
    ("bt_t2b / bt_topbox", "binary", "bt_trial_intent >= 4 / = 5 (first exposure, both arms)", "H2.5;H7.1;H11", "04"),
    ("br_t2b / br_topbox", "binary", "br_trial_intent >= 4 / = 5 (post-reveal, blind arms)", "H7.4", "04"),
    ("rapido_exp_group", "categorical", "dem_rapido_ride_use=0→none; dem_rapido_ride_experience 1-2 negative, 3 neutral, 4-5 positive", "H7.3", "04"),
    ("own_aware_any", "binary", "own_aware_aided in (1,2) OR own_aware_unaided = 1", "H7;H11.3", "04"),
    ("aware_2wk_plus", "binary", "own_aware_duration in (2,3,4)", "H11.3;D5", "04"),
    ("own_tried_bin", "binary", "own_tried = 2", "H11.3;H12", "04"),
    ("own_repeat", "binary", "own_orders_4wk >= 2 among tried", "H12;D5", "04"),
    ("own_lapsed", "binary", "own_orders_4wk = 0 among tried", "H12.2;H12.4", "04"),
    ("own_status", "categorical", "user_repeat / user_single / lapsed / tried_unknown / aware_not_tried / unaware / not_asked", "H9;H12", "04"),
    ("tenure_band", "categorical", "own_first_order_month 1-2→le_1m; 3→2_3m; 4-5→gt_3m", "H9 maturity", "04"),
    ("on_time_most", "binary", "own_reliability_rating in (4,5)", "D4", "04"),
    ("unresolved_issue", "binary", "own_support_issue_resolved in (0,3); 9→missing", "H12.2", "04"),
    ("offer_trigger", "binary", "own_first_trial_trigger = 1", "H12.4", "04"),
    ("wtp_start", "₹", "20 for V1/V4/B1; 40 for V2/V3/B2", "H8", "01"),
    ("wtp_max_fee", "₹", "highest fee answered Yes on the reconstructed staircase path; NA if rejects all or path incomplete", "H8.1;H6.2", "04"),
    ("wtp_censored_top", "binary", "Yes at ₹60", "H8", "04"),
    ("wtp_rejects_all", "binary", "No at ₹0 — reported separately, never coded ₹0", "H8", "04"),
    ("wtp_status / wtp_path", "text", "ok / incomplete / not_answered / no_start; fees visited in order", "H8", "04"),
    ("bill_s1_simple_chosen", "binary", "bill_s1 mapped by version order; 'no real difference' → NA (bill_s1_indifferent=1)", "H2.2", "04"),
    ("bill_s2_nodiscount_chosen", "binary", "bill_s2 mapped by version order; indifferent → NA", "H2.4", "04"),
    ("bill_s3_newapp_chosen / bill_s4_newapp_chosen", "binary", "bill_s3/bill_s4 mapped by version order", "H2;H3", "04"),
    ("meta_brand_arm / meta_dce_block", "categorical", "from meta_form_version (V1,V2 blind; V3,V4 branded; blocks V1,V3=1, V2,V4=2; Bengaluru none)", "H7;H2-H5", "01"),
    ("meta_duration_sec", "seconds", "meta_submit_ts (IST) − meta_start_ts (epoch ms → IST)", "QC", "01"),
    ("EX01_screen_fail … EX09_outside_target_after_recode", "flag", "'' / borderline / hard — rules in 08_clean_data/cleaning_protocol.md §3", "QC", "02"),
    ("exclusion_reason / exclusion_flags_all / EX_borderline", "text", "first hard (or adjudicated-exclude) flag by precedence; all flags; kept borderline", "QC", "03"),
    ("FLAG_no_token / FLAG_no_duration / FLAG_iiith / FLAG_choice_left_right / FLAG_dominance_fail / FLAG_wtp_nonmonotone / FLAG_wtp_orphan_conflict",
     "binary", "sensitivity flags (never exclusion on their own)", "QC", "02"),
    ("w_match_hyd", "weight", "Bengaluru post-stratification weight to Hyderabad seg_occupation × seg_freq (2×2 collapse if a cell n<10); Hyderabad = 1", "H9", "09"),
]
TABLE_SCRIPT = {"fact_survey_respondent": "04 (+09 weights)", "fact_dce_long": "04", "fact_wtp_long": "04",
                "fact_bill_choice_long": "04", "fact_model_dce": "07", "fact_model_coefs": "07/08",
                "fact_reviews": "11", "fact_interview_segments": "manual coding (04_interviews)", "fact_audit_obs": "10",
                "fact_audit_pairs": "10", "fact_fakedoor_events": "12", "agg_fakedoor_variant": "12",
                "dim_hypothesis": "06", "fact_evidence_matrix": "manual (11_insights)", "fact_scorecard": "13",
                "dim_chart": "manual (10_dashboard)", "bridge_insight_hypothesis": "manual (11_insights)"}


def header(path):
    with open(path, newline="", encoding="utf-8") as f:
        return next(csv.reader(f), [])


def main():
    rows = []
    with open(C.DICT_FILE, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            names = [r["variable_name"]]
            if r["variable_name"].startswith("dce_t1"):
                names = [f"dce_t{i}" for i in range(1, 7)]
            elif r["variable_name"].startswith("wtp_start"):
                names = [f"wtp_accept_{fee}" for fee in C.WTP_FEES]
            for n in names:
                if r["response_type"] in ("text_block",):
                    continue
                note = "one 0/1 column per option: <var>__<option_slug>; plus __n_selected, __other_text" if r["response_type"].startswith("checkboxes") else ""
                rows.append({"dataset": "survey_harmonised (both cities; city column)", "variable_name": n,
                             "label": r["question_text"][:160], "type": r["response_type"], "allowed_values": r["values_codes"],
                             "missing_codes": "blank = not shown/skipped; 98/99 = DK/NA where listed",
                             "source_file": "03_hyderabad_survey/survey_variable_dictionary.csv",
                             "produced_by_script": "09_analysis/01_ingest_and_harmonise.py",
                             "derived_formula": "; ".join(x for x in (r["derived_formula"], note) if x),
                             "hypothesis_linked": r["hypothesis_linked"]})
    for var, typ, formula, hyp, script in DERIVED:
        rows.append({"dataset": "survey_derived (survey_respondent_full)", "variable_name": var, "label": "", "type": typ,
                     "allowed_values": "", "missing_codes": "NA when inputs missing (see formula)",
                     "source_file": "09_analysis/M_pre_analysis_plan.md §4", "produced_by_script": f"09_analysis/{script}_*.py",
                     "derived_formula": formula, "hypothesis_linked": hyp})
    for p in sorted((P / "10_dashboard" / "schema").glob("*.csv")):
        for col in header(p):
            rows.append({"dataset": f"mart:{p.stem}", "variable_name": col, "label": "see 10_dashboard/dataset_schema.md",
                         "type": "", "allowed_values": "", "missing_codes": "", "source_file": f"10_dashboard/schema/{p.name}",
                         "produced_by_script": TABLE_SCRIPT.get(p.stem, ""), "derived_formula": "", "hypothesis_linked": ""})
    extra = [("audit_raw", P / "06_competitor_audit" / "audit_schema.csv", "manual field capture (06_competitor_audit/audit_field_sheet.md)",
              "06_competitor_audit/audit_data_dictionary.md"),
             ("reviews_app_store_coded", P / "05_review_mining" / "app_stores" / "reviews_coded.csv", "05_review_mining/app_stores/collect_and_code.py + AI first pass", "05_review_mining/app_stores/codebook.md"),
             ("social_coded", P / "05_review_mining" / "social" / "social_coded.csv", "05_review_mining/social (AI first pass)", "05_review_mining/social/codebook_social.md"),
             ("interview_coded_segments", P / "04_interviews" / "coded_segments_template.csv", "manual + AI first pass (human reviewed)", "04_interviews/coding_framework.md")]
    for ds, path, script, doc in extra:
        if path.exists():
            for col in header(path):
                rows.append({"dataset": ds, "variable_name": col, "label": f"see {doc}", "type": "", "allowed_values": "",
                             "missing_codes": "", "source_file": str(path.relative_to(P)), "produced_by_script": script,
                             "derived_formula": "", "hypothesis_linked": ""})
    for col in ["experiment_id", "page_version", "variant_id", "variant_key", "anon_visitor_id", "anon_session_id", "event_name",
                "ts", "time_since_load_ms", "utm_source", "utm_medium", "utm_campaign", "utm_content", "referrer_domain",
                "device_type", "is_qa", "is_bot_suspect", "payload"]:
        rows.append({"dataset": "fakedoor_events_raw", "variable_name": col, "label": "see 07_fake_door/event_schema.md",
                     "type": "", "allowed_values": "", "missing_codes": "", "source_file": "07_fake_door/events_schema.json",
                     "produced_by_script": "07_fake_door/apps_script_collector.gs", "derived_formula": "", "hypothesis_linked": "H11"})
    out = P / "08_clean_data" / "master_data_dictionary.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {out} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
