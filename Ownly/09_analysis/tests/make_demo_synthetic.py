"""Create DEMO_SYNTHETIC fixtures for testing the pipeline — NEVER real data.

Every file name contains DEMO_SYNTHETIC; everything is written ONLY to the session scratchpad
(default below). The script refuses any output directory inside the project folder.

usage: python tests/make_demo_synthetic.py [--out DIR]
then:  bash tests/run_demo_test.sh
"""
from __future__ import annotations

import argparse
import os
import sys
import uuid
from datetime import datetime, timedelta
from pathlib import Path

os.environ["OWNLY_DEMO_MODE"] = "1"
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import config as C  # noqa: E402
import make_form_column_map as mfm  # noqa: E402
import utils_survey as us  # noqa: E402
from tests.demo_survey_gen import gen_city  # noqa: E402

DEFAULT_OUT = Path("/private/tmp/claude-501/-Users-klprathyusha-Sem-3-Project/90a9dd4b-778d-4cbd-b419-3747da65abb9/scratchpad/demo_synthetic")


def safe_write(df: pd.DataFrame, path: Path):
    path = Path(path)
    if "DEMO_SYNTHETIC" not in path.name:
        raise SystemExit(f"refusing: synthetic file name must contain DEMO_SYNTHETIC: {path}")
    try:
        path.resolve().relative_to(C.PROJECT_ROOT.resolve())
        raise SystemExit(f"refusing to write synthetic data inside the project: {path}")
    except ValueError:
        pass
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"wrote {path} ({len(df)} rows)")


def audit_fixture(g):
    rows, n = [], 0
    slots = ["lunch_peak", "dinner_peak", "off_peak", "weekend_dinner", "late_night"]
    for day in range(4):
        for slot_i, slot in enumerate(slots):
            for dp in ("DP1", "DP2", "DP3"):
                for r in range(1, 21):
                    base = g.uniform(180, 350)
                    t0 = datetime(2026, 9, 17 + day, 12 + slot_i * 2, 0) + timedelta(minutes=int(g.integers(0, 30)))
                    for plat in ("swiggy", "zomato", "ownly"):
                        n += 1
                        listed = "n" if (plat == "ownly" and r > 15) else "y"
                        menu = round(base * (1.0 if plat == "ownly" else g.uniform(1.0, 1.15)))
                        pack, pf = (0, 0) if plat == "ownly" else (15, 15)
                        deliv = 30 if plat == "ownly" else int(g.choice([25, 30, 40]))
                        disc = 0 if plat == "ownly" else int(g.choice([0, 20, 40]))
                        tax = round(0.05 * menu)
                        final = menu + pack + pf + deliv + tax - disc
                        eta = int(g.integers(28, 40)) + (5 if plat == "ownly" else 0)
                        rows.append({"audit_id": f"A{n:06d}", "capture_ts": (t0 + timedelta(minutes=int(g.integers(0, 6)))).isoformat(),
                                     "day_of_week": t0.strftime("%a"), "slot": slot, "auditor_id": "AUD1", "drop_point_id": dp,
                                     "platform": plat, "account_state": "existing", "subscription_active": "n",
                                     "restaurant_id": f"R{r:02d}", "restaurant_name": f"Demo Restaurant {r}",
                                     "restaurant_listed": listed, "restaurant_open": "y" if g.random() > .05 else "n",
                                     "distance_km_shown": round(g.uniform(1, 6), 1), "basket_id": "B1", "item_list": "demo item",
                                     "item_match_quality": "exact", "menu_subtotal": menu, "offline_subtotal_verified": "",
                                     "offline_price_source": "unverified", "packaging_fee": pack, "platform_fee": pf,
                                     "delivery_fee": deliv, "small_cart_fee": 0, "surge_rain_fee": 0, "other_fees": 0,
                                     "taxes_gst": tax, "discount_amount": disc, "discount_type": "auto_offer" if disc else "none",
                                     "subscription_saving_shown": 0, "final_payable": final, "eta_min_shown": eta,
                                     "eta_max_shown": eta + 5, "promo_banner_text": "", "screenshot_file": "",
                                     "test_order_placed": "n", "actual_delivery_min": "", "order_accurate": "NA", "notes": "DEMO_SYNTHETIC"})
    return pd.DataFrame(rows)


def fakedoor_fixture(g):
    rows = []
    p_cta = {"A": .12, "B": .16, "C": .10}
    for i in range(900):
        v = "ABC"[i % 3]
        vid, sid = str(uuid.uuid4()), str(uuid.uuid4())
        t0 = datetime(2026, 9, 18) + timedelta(minutes=int(g.integers(0, 14 * 1440)))
        src = g.choice(["whatsapp", "linkedin", "instagram"])
        qa = g.random() < .02

        def ev(name, ms, payload="{}"):
            rows.append({"experiment_id": "hyd_vp_fakedoor_v1", "page_version": "DEMO_SYNTHETIC", "variant_id": v,
                         "variant_key": v, "anon_visitor_id": vid, "anon_session_id": sid, "event_name": name,
                         "ts": (t0 + timedelta(milliseconds=ms)).isoformat(), "time_since_load_ms": ms,
                         "utm_source": src, "utm_medium": "community", "utm_campaign": "demo", "utm_content": "",
                         "referrer_domain": "", "device_type": "mobile", "is_qa": qa, "is_bot_suspect": False,
                         "payload": payload})
        ev("page_view", 0)
        if g.random() < .7:
            ev("vp_view", 3000)
        if g.random() < .5:
            ev("scroll_50", 6000)
        if g.random() < p_cta[v]:
            ms = int(g.integers(4000, 40000))
            ev("cta_click", ms)
            ev("disclosure_view", ms + 200)
            if g.random() < .35:
                ev("secondary_intent", ms + 20000, '{"action":"bill_calc"}')
            if g.random() < .5:
                ev("mini_survey_submit", ms + 40000, '{"seg_occupation":"student","locality":"gachibowli","orders_4wk":"4-7"}')
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    out = Path(ap.parse_args().out)
    g = np.random.default_rng(C.SEED)
    fmap = mfm.build()
    safe_write(fmap, out / "form_column_map_DEMO_SYNTHETIC.csv")
    dic = pd.read_csv(C.DICT_FILE, dtype=str).fillna("")
    design = us.load_design()
    for city, versions, n in (("hyd", ["V1", "V2", "V3", "V4"], 60), ("blr", ["B1", "B2"], 70)):
        for v in versions:
            df = gen_city(city, [v], n, fmap, dic, design, g)
            safe_write(df, out / "data" / "raw" / f"{city}_survey_{v.lower()}_raw_DEMO_SYNTHETIC.csv")
    safe_write(audit_fixture(g), out / "audit_obs_DEMO_SYNTHETIC.csv")
    safe_write(fakedoor_fixture(g), out / "events_DEMO_SYNTHETIC.csv")


if __name__ == "__main__":
    main()
