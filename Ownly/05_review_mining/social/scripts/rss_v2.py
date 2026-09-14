import urllib.request, urllib.parse, time, xml.etree.ElementTree as ET, json, re, os, html
UA="ownly-student-research/0.1 (non-commercial academic project; low volume)"
ns={'a':'http://www.w3.org/2005/Atom'}
FOOD=re.compile(r'food|deliver|order|restaurant|swiggy|zomato|meal|biryani',re.I)
def relevant(t): return bool(re.search(r'\bownly\b',t,re.I)) or (bool(re.search(r'rapido',t,re.I)) and bool(FOOD.search(t)))
st_path="rss/state.json"
st=json.load(open(st_path)) if os.path.exists(st_path) else {"log":[],"threads":{},"done_queries":[],"thread_data":{}}
old=json.load(open("rss/search_results.json"))
for l,v in old["threads"].items(): st["threads"].setdefault(l.split('?')[0],{"title":v["title"],"found_by":v["found_by"],"blob":v["title"]})
def save(): json.dump(st,open(st_path,"w"),indent=1,ensure_ascii=False)
def get(url):
    for attempt in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":UA}),timeout=40).read(),"200"
        except urllib.error.HTTPError as ex:
            if ex.code==429: time.sleep(90*(attempt+1)); continue
            return None,str(ex.code)
        except Exception as ex: time.sleep(20)
    return None,"fail"
Q=[("all","ownly rapido"),("all","rapido food delivery"),("all","ownly swiggy"),("all","ownly zomato"),("all","ownly hyderabad"),("hyderabad","ownly"),("hyderabad","rapido food"),("bangalore","ownly"),("BangaloreSocial","ownly"),("Zomato","ownly"),("swiggy","ownly"),("india","ownly"),("indianstartups","ownly"),("IndiaInvestments","ownly"),("Chennai","ownly"),("Ownly","")]
for sub,q in Q:
    key=f"{sub}|{q}"
    if key in st["done_queries"]: continue
    if sub=="all": url="https://www.reddit.com/search.rss?"+urllib.parse.urlencode({"q":q,"sort":"relevance","t":"all","limit":100})
    elif q=="": url=f"https://www.reddit.com/r/{sub}/new.rss?limit=100"
    else: url=f"https://www.reddit.com/r/{sub}/search.rss?"+urllib.parse.urlencode({"q":q,"restrict_sr":"1","sort":"relevance","t":"all","limit":100})
    data,code=get(url); n=rel=0
    if data:
        for e in ET.fromstring(data).findall('a:entry',ns):
            l=e.find('a:link',ns).get('href').split('?')[0]; t=e.find('a:title',ns).text or ''
            c=e.find('a:content',ns); body=html.unescape(re.sub('<[^>]+>',' ',html.unescape((c.text or '') if c is not None else '')))
            n+=1
            if '/comments/' in l and (sub=="Ownly" or relevant(t+' '+body)):
                rel+=1; d=st["threads"].setdefault(l,{"title":t,"found_by":[],"blob":(t+' '+body)[:500]}); d["found_by"].append(key)
    st["log"].append([url,code,n,rel,time.strftime("%Y-%m-%d %H:%M")]); st["done_queries"].append(key); save(); print(url,code,n,rel,flush=True); time.sleep(12)
EXSUB=re.compile(r"/r/(AutoNewspaper|TIMESINDIAauto|IndiaReferral|sundaysarthak|MaharashtraTalks|southindia_|Indiajobs|IndianWorkers|TradeSphereX|wierdJobIdeasIndia|degoogle|CreditCardIndia)/",re.I)
EXTITLE=re.compile(r"intern|referral code|non.?veg|Modi Govt|interview with Ownly|rented EV|extract ₹48|credit card gurus",re.I)
cands=[l for l,v in st["threads"].items() if (relevant(v.get("blob",v["title"])) or "Ownly|" in ' '.join(v["found_by"])) and not EXSUB.search(l) and not EXTITLE.search(v["title"])]
cands.sort(key=lambda l:(not re.search('ownly',st["threads"][l]["title"],re.I), -len(st["threads"][l]["found_by"])))
print(len(st["threads"]),"threads;",len(cands),"candidates",flush=True)
for l in cands[:45]:
    m=re.search(r'/comments/([a-z0-9]+)/',l)
    if not m or m.group(1) in st["thread_data"]: continue
    data,code=get(l.rstrip('/')+"/.rss?limit=100"); items=[]
    if data:
        for e in ET.fromstring(data).findall('a:entry',ns):
            c=e.find('a:content',ns); txt=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',html.unescape(c.text or '')))).strip() if c is not None else ''
            pub=e.find('a:published',ns); upd=e.find('a:updated',ns)
            items.append({"id":e.find('a:id',ns).text,"link":e.find('a:link',ns).get('href'),"title":e.find('a:title',ns).text,"date":(pub.text if pub is not None else (upd.text if upd is not None else '')),"text":txt})
    st["thread_data"][m.group(1)]={"url":l,"title":st["threads"][l]["title"],"code":code,"items":items}
    st["log"].append([l+".rss",code,len(items),"",time.strftime("%Y-%m-%d %H:%M")]); save(); print(l,code,len(items),flush=True); time.sleep(12)
print("DONE",len(st["thread_data"]),flush=True)
