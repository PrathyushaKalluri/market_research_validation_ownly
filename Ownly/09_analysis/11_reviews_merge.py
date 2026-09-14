"""Step 11: merge coded app-store reviews + social items into fact_reviews (one row per item x theme).

App reviews and social posts are CONSUMER-GENERATED, self-selected signals: they are used for
issue discovery and severity, never for prevalence claims. Quotes are truncated to 25 words.
Outputs: MART_DIR/fact_reviews.csv, OUT_ROOT/review_theme_summary.csv, review_summary_metrics.csv
"""
from __future__ import annotations

import re

import numpy as np
import pandas as pd

import config as C
import utils_io as io

RELIABILITY_RE = re.compile(r"LATE|ETA|CANCEL|REFUND|SUPPORT|NOT_DELIVERED|FALSE_DELIVER|RELIAB|MISSING|WRONG", re.I)


def excerpt(t, n=25):
    words = str(t).split()
    return " ".join(words[:n]) + (" …" if len(words) > n else "") if words else ""


def harmonise(df, family):
    if family == "app_store":
        base = pd.DataFrame({"item_id": df.review_id, "source": df.platform_source, "url": df.get("source_url"),
                             "item_date": df.review_date, "access_date": df.get("retrieved_at"),
                             "app_version": df.get("app_version"), "star_rating": df.star_rating,
                             "author_type": "consumer", "quote_excerpt": df.review_text.map(excerpt),
                             "evidence_type": "CONSUMER-GENERATED"})
    else:
        if "relevant" in df:
            df = df[df.relevant.astype(str).str.lower().isin(["1", "true", "yes", "y"])]
        base = pd.DataFrame({"item_id": df.item_id, "source": df.platform, "url": df.url, "item_date": df.post_date,
                             "access_date": df.access_date, "app_version": np.nan, "star_rating": np.nan,
                             "author_type": df.author_type, "quote_excerpt": df.text_excerpt.map(excerpt),
                             "evidence_type": df.get("evidence_label", "CONSUMER-GENERATED")})
    for src, dst in [("city_mentioned", "city_mentioned"), ("sentiment", "sentiment"), ("order_stage", "order_stage"),
                     ("severity", "severity"), ("switching_trigger_flag", "switching_trigger"),
                     ("churn_signal", "churn_signal"), ("repeat_use_signal", "repeat_signal"),
                     ("price_value_comment", "price_value_comment"), ("delivery_eta_comment", "eta_comment"),
                     ("assortment_comment", "assortment_comment"), ("support_comment", "support_comment"),
                     ("trust_safety_quality_comment", "trust_quality_comment"), ("coder", "coder_id"),
                     ("human_verified", "human_reviewed"), ("themes", "themes"), ("primary_theme", "primary_theme")]:
        base[dst] = df[src].values if src in df else np.nan
    base["source_family"] = family
    return base


def main():
    parts = []
    for path, fam in [(C.REVIEWS_APP_FILE, "app_store"), (C.REVIEWS_SOCIAL_FILE, "social")]:
        if path.exists():
            parts.append(harmonise(pd.read_csv(path), fam))
    if not parts:
        print("  no coded review files — skipping")
        return
    items = pd.concat(parts, ignore_index=True)
    items["severity"] = pd.to_numeric(items.severity, errors="coerce")
    rows = []
    for _, r in items.iterrows():
        themes = [t.strip() for t in str(r.themes).replace("|", ";").split(";") if t.strip() and t.strip() != "nan"]
        themes = sorted(themes, key=lambda t: 0 if t == r.primary_theme else 1) or ["UNCODED"]
        for rank, t in enumerate(themes, start=1):
            rows.append({**r.drop(["themes", "primary_theme"]).to_dict(), "theme_code": t, "theme_rank": rank,
                         "coder_confidence": np.nan})
    fact = io.stamp(pd.DataFrame(rows))
    fact["data_status"] = "REAL_CONSUMER_GENERATED"          # reviews are real public data, not survey data
    io.write_csv(fact, C.MART_DIR / "fact_reviews.csv")

    summ = []
    for (fam, theme), g in fact.groupby(["source_family", "theme_code"]):
        n_items = items[items.source_family == fam].item_id.nunique()
        summ.append({"source_family": fam, "theme_code": theme, "n_items": g.item_id.nunique(),
                     "share_of_items": g.item_id.nunique() / n_items, "mean_severity": g.severity.mean(),
                     "n_severity_ge3": int((g.severity >= 3).sum()),
                     "priority_n_x_severity": g.item_id.nunique() * g.severity.mean()})
    io.write_csv(pd.DataFrame(summ).sort_values("priority_n_x_severity", ascending=False), C.OUT_ROOT / "review_theme_summary.csv")

    items["reliability_theme"] = items.themes.astype(str).str.contains(RELIABILITY_RE)
    w = items.severity.fillna(2) / 4
    share = float((items.reliability_theme * w).sum() / len(items))
    score = float(np.clip((0.50 - share) / (0.50 - 0.10) * 100, 0, 100))
    io.write_csv(pd.DataFrame([{"metric": "review_reliability_share_severity_weighted", "value": share, "n": len(items),
                                "note": "NOT a prevalence estimate; self-selected reviews"},
                               {"metric": "review_reliability_score", "value": score, "n": len(items),
                                "note": "anchors: 50% share -> 0, 10% -> 100"}]),
                 C.OUT_ROOT / "review_summary_metrics.csv")


if __name__ == "__main__":
    main()
