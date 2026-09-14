#!/usr/bin/env python3
"""
Ownly app-store review mining — reproducible collection + aggregation.
Agent B1, 2026-09-14. Standard library only (no pip installs needed).

USAGE
  python3 collect_and_code.py collect     # step 1: robots-compliant retrieval -> reviews_raw.csv, listing_stats.csv
  python3 collect_and_code.py aggregate   # step 3: reads reviews_coded.csv -> analysis_tables.md

STEP 2 (not in this script): thematic coding. The first pass was done by an AI coder
(Claude, labelled coder=ai_first_pass) using codebook.md, then must be human-verified
on reviews_validation_sample.csv. Coding is deliberately NOT automated with keywords only,
because keyword matching misreads sarcasm, negation and mixed reviews.

ACCESS POLICY (see methodology.md)
  * Only URLs whose paths are ALLOWED by the site's robots.txt are requested:
      - https://play.google.com/store/apps/details?id=...   (allowed; "/_" batchexecute API is disallowed -> NOT used)
      - https://apps.apple.com/in/app/<slug>/id<ID>?see-all=reviews  (allowed; /api/*, /v1/* disallowed -> NOT used)
      - itunes.apple.com /*/rss/* customer-review feed is DISALLOWED by robots.txt -> NOT used
  * No login, no tokens, no pagination APIs, >=4 s between requests, <40 requests per run.
  * Reviewer names / avatars / profile links are never written to disk.
"""
import csv, hashlib, json, re, sys, time, urllib.request, datetime, collections, os

HERE = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (academic research; low-volume; contact via university)"
ACCESS_DATE = datetime.date.today().isoformat()
SLEEP = 4

APPS = {
    # key: (platform, app_id, url_builder variants, food_filter)
    "ownly_play": ("google_play", "com.ownly.customer", False),
    "rapido_play": ("google_play", "com.rapido.passenger", True),
    "ownly_ios": ("apple_app_store", "6747476494", False),
    "rapido_ios": ("apple_app_store", "1198464606", True),
}
IOS_SLUG = {"6747476494": "ownly-food-delivery-app", "1198464606": "rapido-bike-taxi-auto-cabs"}
PLAY_LANGS = ["en_IN", "en", "hi", "te", "kn", "ta"]
IOS_PLATFORMS = ["iphone", "ipad"]

# Food-related filter for the main Rapido app (keep only reviews about food / Ownly).
FOOD_RE = re.compile(r"\b(ownly|food|restaurant|meal|biryani|dish|hotel food|order(ed)? food|delivery of food|swiggy|zomato)\b", re.I)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-IN,en;q=0.8"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode("utf-8", "ignore")


def rid(platform, native_id):
    # stable pseudonymous id; native store id is hashed so rows cannot be trivially linked to a profile
    return platform[:2].upper() + "_" + hashlib.sha1(f"{platform}:{native_id}".encode()).hexdigest()[:10]


# ---------------- Google Play ----------------
def parse_play(html):
    blocks = re.findall(r"AF_initDataCallback\(\{key: '(ds:\d+)', hash: '\d+', data:(.*?), sideChannel: \{\}\}\);</script>", html, re.S)
    reviews = []

    def walk(o):
        if isinstance(o, list):
            if (len(o) > 5 and isinstance(o[0], str) and isinstance(o[2], int) and 1 <= o[2] <= 5
                    and isinstance(o[4], str) and isinstance(o[5], list) and o[5] and isinstance(o[5][0], int)):
                reviews.append(o)
                return
            for x in o:
                walk(x)

    for _, d in blocks:
        try:
            walk(json.loads(d))
        except Exception:
            pass
    out = []
    for r in reviews:
        g = lambda i, default=None: r[i] if len(r) > i else default
        reply = g(7)
        out.append({
            "native_id": r[0],
            "review_date": datetime.datetime.utcfromtimestamp(r[5][0]).date().isoformat(),
            "star_rating": r[2],
            "review_text": r[4],
            "thumbs_up_count": g(6) if isinstance(g(6), int) else "",
            "app_version": g(10) if isinstance(g(10), str) else "",
            "developer_reply_present": int(bool(isinstance(reply, list) and len(reply) > 1 and reply[1])),
        })
    stats = {}
    m = re.search(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S)
    if m:
        try:
            ld = json.loads(m.group(1))
            ar = ld.get("aggregateRating", {})
            stats = {"rating_value": ar.get("ratingValue"), "rating_count": ar.get("ratingCount")}
        except Exception:
            pass
    inst = re.search(r'"([\d,]+\+)"', html)  # first "N+" string is the installs badge on details pages
    stats["installs_badge"] = inst.group(1) if inst else ""
    return out, stats


# ---------------- Apple App Store (web page, not RSS) ----------------
def parse_ios(html):
    out, stats = [], {}
    for s in re.findall(r'<script[^>]*type="application/(?:ld\+)?json"[^>]*>(.*?)</script>', html, re.S):
        try:
            d = json.loads(s)
        except Exception:
            continue
        found = []

        def w(o):
            if isinstance(o, dict):
                if o.get("$kind") == "Review":
                    found.append(o)
                if o.get("@type") == "SoftwareApplication" and "aggregateRating" in o:
                    stats.update({"rating_value": o["aggregateRating"].get("ratingValue"),
                                  "rating_count": o["aggregateRating"].get("reviewCount")})
                for v in o.values():
                    w(v)
            elif isinstance(o, list):
                for v in o:
                    w(v)

        w(d)
        for r in found:
            text = (r.get("title") or "").strip()
            body = (r.get("contents") or "").strip()
            out.append({
                "native_id": r.get("id"),
                "review_date": (r.get("date") or "")[:10],
                "star_rating": r.get("rating"),
                "review_text": (text + " — " + body) if text else body,
                "thumbs_up_count": "",
                "app_version": "",
                "developer_reply_present": int(bool(r.get("response"))),
            })
    return out, stats


def collect():
    rows, seen, log, stats_rows = [], set(), [], []
    for key, (platform, app_id, food_filter) in APPS.items():
        if platform == "google_play":
            urls = [f"https://play.google.com/store/apps/details?id={app_id}&hl={hl}&gl=IN" for hl in PLAY_LANGS]
            parser = parse_play
        else:
            urls = [f"https://apps.apple.com/in/app/{IOS_SLUG[app_id]}/id{app_id}?see-all=reviews&platform={p}" for p in IOS_PLATFORMS]
            parser = parse_ios
        for url in urls:
            try:
                html = fetch(url)
                revs, stats = parser(html)
            except Exception as e:
                log.append((key, url, "ERROR " + repr(e), 0, 0))
                time.sleep(SLEEP)
                continue
            new = 0
            for r in revs:
                k = (platform, r["native_id"])
                if k in seen:
                    continue
                if food_filter and not FOOD_RE.search(r["review_text"] or ""):
                    continue
                seen.add(k)
                new += 1
                rows.append({
                    "review_id": rid(platform, r["native_id"]),
                    "platform_source": platform,
                    "app_id": app_id,
                    "app_context": "ownly_standalone" if not food_filter else "rapido_main_app_food_mention",
                    "app_version": r["app_version"],
                    "review_date": r["review_date"],
                    "star_rating": r["star_rating"],
                    "review_text": (r["review_text"] or "").replace("\r", " ").strip(),
                    "thumbs_up_count": r["thumbs_up_count"],
                    "developer_reply_present": r["developer_reply_present"],
                    "source_url": url,
                    "retrieved_at": ACCESS_DATE,
                })
            log.append((key, url, "ok", len(revs), new))
            if stats:
                stats_rows.append({"app_key": key, "platform": platform, "app_id": app_id, "url": url, **stats, "retrieved_at": ACCESS_DATE})
            time.sleep(SLEEP)
    fields = ["review_id", "platform_source", "app_id", "app_context", "app_version", "review_date", "star_rating",
              "review_text", "thumbs_up_count", "developer_reply_present", "source_url", "retrieved_at"]
    rows.sort(key=lambda r: (r["platform_source"], r["review_date"]), reverse=True)
    with open(os.path.join(HERE, "reviews_raw.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    with open(os.path.join(HERE, "retrieval_log.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["app_key", "url", "status", "reviews_on_page", "new_unique_kept"])
        w.writerows(log)
    # keep one stats row per app (first successful page)
    first = {}
    for s in stats_rows:
        first.setdefault(s["app_key"], s)
    with open(os.path.join(HERE, "listing_stats.csv"), "w", newline="", encoding="utf-8") as f:
        keys = ["app_key", "platform", "app_id", "url", "rating_value", "rating_count", "installs_badge", "retrieved_at"]
        w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        w.writeheader()
        w.writerows(first.values())
    for l in log:
        print(*l, sep=" | ")
    print("unique reviews kept:", len(rows))


# ---------------- Aggregation (after coding) ----------------
def aggregate():
    path = os.path.join(HERE, "reviews_coded.csv")
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    n = len(rows)
    L = []
    P = L.append
    P(f"# Aggregation tables (auto-generated by collect_and_code.py aggregate)\n\nn = {n} coded reviews\n")

    def table(title, counter, total, extra=None):
        P(f"\n## {title}\n\n| value | n | % |" + (" " + extra[0] + " |" if extra else ""))
        P("|---|---|---|" + ("---|" if extra else ""))
        for k, v in counter.most_common():
            P(f"| {k} | {v} | {100*v/total:.0f}% |" + (f" {extra[1](k)} |" if extra else ""))

    table("By source", collections.Counter(r["platform_source"] + " / " + r["app_context"] for r in rows), n)
    table("By star rating", collections.Counter(r["star_rating"] for r in rows), n)
    table("By month", collections.Counter(r["review_date"][:7] for r in rows), n)
    table("Sentiment", collections.Counter(r["sentiment"] for r in rows), n)
    table("City mentioned", collections.Counter(r["city_mentioned"] for r in rows), n)

    theme_n, theme_sev = collections.Counter(), collections.defaultdict(list)
    for r in rows:
        for t in [t.strip() for t in r["themes"].split(";") if t.strip()]:
            theme_n[t] += 1
            if r["severity"]:
                theme_sev[t].append(int(r["severity"]))
    P("\n## Theme frequency x severity (a review can carry several themes)\n")
    P("| theme | n reviews | % of reviews | mean severity (1-4) | n severity>=3 | priority = n x mean severity |")
    P("|---|---|---|---|---|---|")
    for t, v in sorted(theme_n.items(), key=lambda kv: -kv[1] * (sum(theme_sev[kv[0]]) / max(1, len(theme_sev[kv[0]])))):
        s = theme_sev[t]
        ms = sum(s) / len(s) if s else 0
        P(f"| {t} | {v} | {100*v/n:.0f}% | {ms:.2f} | {sum(1 for x in s if x >= 3)} | {v*ms:.1f} |")

    P("\n## Order stage x sentiment (heat table, counts)\n")
    sents = ["neg", "mixed", "neutral", "pos"]
    P("| order_stage | " + " | ".join(sents) + " | total |")
    P("|---|" + "---|" * (len(sents) + 1))
    st = collections.defaultdict(collections.Counter)
    for r in rows:
        st[r["order_stage"]][r["sentiment"]] += 1
    for k in sorted(st, key=lambda k: -sum(st[k].values())):
        P(f"| {k} | " + " | ".join(str(st[k][s]) for s in sents) + f" | {sum(st[k].values())} |")

    P("\n## Theme share among low (1-2 star) vs high (4-5 star) reviews\n")
    lo = [r for r in rows if r["star_rating"] in ("1", "2")]
    hi = [r for r in rows if r["star_rating"] in ("4", "5")]
    P(f"low n = {len(lo)}, high n = {len(hi)}\n\n| theme | % of 1-2 star | % of 4-5 star |\n|---|---|---|")
    for t, _ in theme_n.most_common():
        a = sum(1 for r in lo if t in r["themes"].split(";"))
        b = sum(1 for r in hi if t in r["themes"].split(";"))
        P(f"| {t} | {100*a/max(1,len(lo)):.0f}% ({a}) | {100*b/max(1,len(hi)):.0f}% ({b}) |")

    flags = ["switching_trigger_flag", "churn_signal", "repeat_use_signal"]
    P("\n## Behavioural signals\n\n| flag | n=1 | % |\n|---|---|---|")
    for fl in flags:
        c = sum(1 for r in rows if r.get(fl) == "1")
        P(f"| {fl} | {c} | {100*c/n:.0f}% |")
    open(os.path.join(HERE, "analysis_tables.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    {"collect": collect, "aggregate": aggregate}[sys.argv[1] if len(sys.argv) > 1 else "collect"]()
