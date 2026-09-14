"""Build 05_review_mining/social/ datasets from collected items.
Inputs (scratchpad): manual_items.json (LinkedIn/X/forum), rss/state.json (Reddit RSS), codes.json (hand coding keyed by item_id).
Outputs (project): social_raw.csv, social_coded.csv, search_log.csv
Reproducible: python3 build_social.py  (stdlib only)
"""
import json, csv, re, datetime as dt, os
SCR = os.path.dirname(os.path.abspath(__file__))
OUT = "/Users/klprathyusha/Sem 3/Project/05_review_mining/social"
ACCESS = "2026-09-14"
TODAY = dt.date(2026, 9, 14)

def li_date(s):   # LinkedIn activity id: top 41 bits = unix ms
    return dt.datetime.utcfromtimestamp((int(s) >> 22) / 1000).date()
def x_date(s):    # X/Twitter snowflake
    return dt.datetime.utcfromtimestamp(((int(s) >> 22) + 1288834974657) / 1000).date()
PHONE = re.compile(r"(?<!\d)(?:\+?91[\s-]?)?[6-9]\d{9}(?!\d)")
EMAIL = re.compile(r"\b[\w.+-]+@(?!ownly\.food\b)[\w-]+\.[\w.]+\b")
import hashlib
SALT = "ownly-b2-2026"
NAME_HASHES = {'78174996a3d1da42', 'b42e38eab351079f', '2489d6f97f507352', '21fc2f742d91813b'}  # salted SHA-256 (16 hex) of lower-cased names of private individuals found in complaint text; plaintext not stored
def _redact_names(t):
    toks = t.split(" "); out = []; i = 0
    h = lambda x: hashlib.sha256((SALT + x.lower().strip('.,!?:;()\"')).encode()).hexdigest()[:16]
    while i < len(toks):
        if i + 1 < len(toks) and h(toks[i] + " " + toks[i + 1]) in NAME_HASHES:
            out.append("[name redacted]"); i += 2; continue
        out.append("[name redacted]" if h(toks[i]) in NAME_HASHES else toks[i]); i += 1
    return " ".join(out)
RUSER = re.compile(r"\bu/[A-Za-z0-9_-]+")  # Reddit usernames
def redact(t):
    return RUSER.sub("u/[redacted]", _redact_names(EMAIL.sub("[email redacted]", PHONE.sub("[phone redacted]", t))))
def words(t, n=60):
    t = redact(t)
    w = t.split()
    return " ".join(w[:n]) + (" …" if len(w) > n else "")

raw = []
manual = json.load(open(os.path.join(SCR, "manual_items.json")))
by_id = {m["item_id"]: m for m in manual}
for m in manual:
    basis = m["date_basis"]
    if basis == "linkedin_activity_id":
        d, q = li_date(m["snowflake"]).isoformat(), "exact_from_id"
    elif basis == "linkedin_activity_id_parent":
        d, q = li_date(m["snowflake"]).isoformat(), "parent_post_date"
    elif basis == "x_status_id":
        d, q = x_date(m["snowflake"]).isoformat(), "exact_from_id"
    elif basis in ("page_date", "stated_in_text"):
        d, q = m["date"], basis
    elif basis == "relative_age":
        d, q = (TODAY - dt.timedelta(days=m["rel_days"])).isoformat(), "approx_relative_age"
    else:  # parent_date_approx
        p = by_id.get(m["parent"], {})
        d = li_date(p["snowflake"]).isoformat() if p.get("snowflake") else ""
        q = "comment_date_unknown_parent_date_used"
    raw.append(dict(item_id=m["item_id"], platform=m["platform"], community=m["community"], item_kind=m["item_kind"],
        parent_item_id=m["parent"], url=m["url"], post_date=d, date_quality=q, access_date=ACCESS,
        author_type=m["author_type"], engagement=m["engagement"], text_excerpt=words(m["text"]),
        verbatim_status=m["verbatim"], city_mentioned=m["city"], collection_note=m.get("note", "")))

# Reddit (public RSS feeds, no login)
st = json.load(open(os.path.join(SCR, "rss", "state.json")))
KEEP = re.compile(r"ownly|rapido|swiggy|zomato|deliver|order|price|fee|refund|support|restaurant|cheap|rider|captain|food", re.I)
ownly_thread = lambda t: bool(re.search(r"ownly", t, re.I))
threads = sorted(st["thread_data"].items(), key=lambda kv: kv[1]["items"][0]["date"] if kv[1]["items"] else "")
for n, (tid, td) in enumerate(threads, 1):
    if not td["items"]:
        continue
    focus = ownly_thread(td["title"] + " " + td["items"][0]["text"])
    sub = re.search(r"/r/([^/]+)/", td["url"]).group(1)
    post_id = f"RD-{tid}"  # stable: Reddit's own base36 thread id
    for k, it in enumerate(td["items"]):
        cid = it["id"].split("_")[-1] if it.get("id") else f"{k:02d}"  # stable: RSS entry id (t1_xxxx)
        is_post = k == 0
        txt = ((it["title"] + " — ") if is_post else "") + it["text"]
        txt = re.sub(r"submitted by /u/\S+|\[link\]|\[comments\]", "", txt).strip()
        if not is_post and (len(txt.split()) < 4 or (not focus and not re.search(r"ownly|rapido", txt, re.I))):
            continue
        if not is_post and txt.lower() in ("[deleted]", "[removed]"):
            continue
        raw.append(dict(item_id=post_id if is_post else f"{post_id}-{cid}", platform="reddit", community=f"r/{sub}",
            item_kind="post" if is_post else "comment", parent_item_id="" if is_post else post_id,
            url=td["url"] if is_post else it["link"].split("?")[0], post_date=it["date"][:10], date_quality="exact_rss",
            access_date=ACCESS, author_type="consumer_unverified", engagement="not exposed by RSS",
            text_excerpt=words(txt), verbatim_status="yes_truncated_60w", city_mentioned="",
            collection_note="thread focus: Ownly" if focus else "thread focus: broader Rapido/food-delivery"))

codes = json.load(open(os.path.join(SCR, "codes.json"))) if os.path.exists(os.path.join(SCR, "codes.json")) else {}
RAW_COLS = ["item_id","platform","community","item_kind","parent_item_id","url","post_date","date_quality","access_date",
            "author_type","engagement","text_excerpt","verbatim_status","city_mentioned","collection_note"]
CODE_COLS = ["relevant","first_hand_ownly_use","sentiment","themes","primary_theme","severity","order_stage","switching_trigger_flag","switching_trigger_text",
             "churn_signal","repeat_use_signal","price_value_comment","delivery_eta_comment","assortment_comment","support_comment",
             "trust_safety_quality_comment","hypotheses_linked","evidence_label","coding_note"]
os.makedirs(OUT, exist_ok=True)
for r in raw:  # coder overrides for author_type / city
    c = codes.get(r["item_id"], {})
    if c.get("author_type"): r["author_type"] = c["author_type"]
    if c.get("city_mentioned") is not None and c.get("city_mentioned") != "": r["city_mentioned"] = c["city_mentioned"]
with open(os.path.join(OUT, "social_raw.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, RAW_COLS); w.writeheader(); w.writerows(raw)
uncoded = []
with open(os.path.join(OUT, "social_coded.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, RAW_COLS + CODE_COLS + ["coder", "human_verified"]); w.writeheader()
    for r in raw:
        c = codes.get(r["item_id"])
        if c is None: uncoded.append(r["item_id"]); c = {}
        row = dict(r); row.update({k: c.get(k, "") for k in CODE_COLS}); row["coder"] = "ai_first_pass"; row["human_verified"] = ""
        w.writerow(row)

# search log
log = json.load(open(os.path.join(SCR, "search_log_manual.json")))
for u, code, n, rel, *ts in st["log"]:
    log.append(dict(date=ACCESS, tool="python urllib (Reddit public RSS)", query_or_url=u, results_count=n,
        relevant_count=rel, accessible="y" if code == "200" else "n", notes=f"HTTP {code}; 12s spacing, 429 back-off"))
with open(os.path.join(OUT, "search_log.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, ["date","tool","query_or_url","results_count","relevant_count","accessible","notes"]); w.writeheader(); w.writerows(log)
print(len(raw), "raw items;", sum(1 for r in raw if r["platform"] == "reddit"), "reddit;", len(uncoded), "uncoded:", uncoded[:200])
