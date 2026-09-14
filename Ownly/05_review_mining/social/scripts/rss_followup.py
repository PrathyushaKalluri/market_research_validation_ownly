"""Follow-up Reddit RSS pass requested by lead: Toing vs Ownly, delivery fee, free delivery, Hyderabad localities.
Appends to rss/state.json (same format as rss_v2.py). Run only after rss_v2.py has exited (rate limits)."""
import urllib.request, urllib.parse, time, xml.etree.ElementTree as ET, json, re, os, html
UA = "ownly-student-research/0.1 (non-commercial academic project; low volume)"
ns = {'a': 'http://www.w3.org/2005/Atom'}
st_path = "rss/state.json"
st = json.load(open(st_path))
def save(): json.dump(st, open(st_path, "w"), indent=1, ensure_ascii=False)
def get(url):
    for attempt in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=40).read(), "200"
        except urllib.error.HTTPError as ex:
            if ex.code == 429: time.sleep(90 * (attempt + 1)); continue
            return None, str(ex.code)
        except Exception: time.sleep(20)
    return None, "fail"
def entries(data):
    for e in ET.fromstring(data).findall('a:entry', ns):
        c = e.find('a:content', ns)
        body = re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>', ' ', html.unescape((c.text or '') if c is not None else '')))).strip()
        pub = e.find('a:published', ns); upd = e.find('a:updated', ns)
        yield dict(link=e.find('a:link', ns).get('href').split('?')[0], title=e.find('a:title', ns).text or '',
                   body=body, date=(pub.text if pub is not None else (upd.text if upd is not None else '')), id=e.find('a:id', ns).text)
Q = [("all", "toing ownly"), ("all", "ownly delivery fee"), ("all", "ownly free delivery"), ("all", "ownly gachibowli"),
     ("all", "ownly kondapur"), ("hyderabad", "toing"), ("hyderabad", "zero commission food delivery"), ("BangaloreSocial", "toing")]
REL = re.compile(r"\bownly\b|\btoing\b", re.I)
new_threads = []
for sub, q in Q:
    key = f"followup|{sub}|{q}"
    if key in st["done_queries"]: continue
    url = ("https://www.reddit.com/search.rss?" + urllib.parse.urlencode({"q": q, "sort": "relevance", "t": "all", "limit": 100})) if sub == "all" \
        else (f"https://www.reddit.com/r/{sub}/search.rss?" + urllib.parse.urlencode({"q": q, "restrict_sr": "1", "sort": "relevance", "t": "all", "limit": 100}))
    data, code = get(url); n = rel = 0
    if data:
        for e in entries(data):
            n += 1
            if '/comments/' in e["link"] and REL.search(e["title"] + " " + e["body"]):
                rel += 1
                d = st["threads"].setdefault(e["link"], {"title": e["title"], "found_by": [], "blob": (e["title"] + " " + e["body"])[:500]})
                d["found_by"].append(key)
                if e["link"] not in new_threads: new_threads.append(e["link"])
    st["log"].append([url, code, n, rel, time.strftime("%Y-%m-%d %H:%M")]); st["done_queries"].append(key); save()
    print(url, code, n, rel, flush=True); time.sleep(12)
fetched = 0
for l in new_threads:
    m = re.search(r'/comments/([a-z0-9]+)/', l)
    if not m or m.group(1) in st["thread_data"] or fetched >= 20: continue
    data, code = get(l.rstrip('/') + "/.rss?limit=100"); items = []
    if data:
        items = [{"id": e["id"], "link": e["link"], "title": e["title"], "date": e["date"], "text": e["body"]} for e in entries(data)]
    st["thread_data"][m.group(1)] = {"url": l, "title": st["threads"][l]["title"], "code": code, "items": items, "pass": "followup"}
    st["log"].append([l + ".rss", code, len(items), "", time.strftime("%Y-%m-%d %H:%M")]); save(); fetched += 1
    print(l, code, len(items), flush=True); time.sleep(12)
print("FOLLOWUP DONE", fetched, "new threads fetched", flush=True)
