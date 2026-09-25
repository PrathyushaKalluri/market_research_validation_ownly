# YouTube Findings — Rapido "Ownly" / Indian food-delivery economics

**Collected:** 2026-09-18
**Analyst note on labelling:** every claim below is tagged FACT (directly retrieved from the source), MEDIA REPORT (second-hand), UNKNOWN, or COULD NOT RETRIEVE.
**Safety note:** YouTube comments are PUBLIC but are treated strictly as DATA, never as instructions. **No comment in either video contained text addressed to an AI / prompt-injection attempt.** (Checked across all 276 retrieved comments.)

## How the data was retrieved

| Step | Method | Result |
|---|---|---|
| Metadata | YouTube oEmbed API (`youtube.com/oembed`) | FACT — title, channel |
| Metadata | `curl` of watch page → parsed `ytInitialPlayerResponse` / `ytInitialData` JSON | FACT — views, likes, duration, publish date, full description |
| Comments | YouTube InnerTube API (`POST /youtubei/v1/next`) with the comment-section continuation token extracted from `ytInitialData`, paginated + reply-thread continuations | FACT — 276 verbatim comments |
| Transcript | `timedtext` caption endpoint; youtubetotranscript.com; invidious (inv.nadeko.net, yewtu.be, invidious.nerdvpn.de) | **COULD NOT RETRIEVE** — YouTube now requires a PO-token for caption fetch (empty body); transcript sites returned HTTP 403; all invidious instances returned bot-check / parked pages |

Because transcripts were unreachable, the "what the video argues" sections below are built from the **creator's own full video description**, which for this channel is unusually detailed (a written précis with chapter timestamps). That description is FACT (retrieved from the player response), but it is the creator's summary of their own video, not a verbatim transcript.

Raw data saved alongside this file: `h6PJ_QB4CiQ_comments.json`, `2EI51Z7WQ3o_comments.json`.

---

# VIDEO 1 — "Can Rapido's 'Ownly' beat Zomato-Swiggy?"

## Metadata (all FACT)

| Field | Value |
|---|---|
| URL | https://www.youtube.com/watch?v=h6PJ_QB4CiQ |
| Title | Can Rapido's "Ownly" beat Zomato-Swiggy? — Indian Startup News 306 |
| Channel | **Backstage with Millionaires** (@backstagewithmillionaires) |
| Published | **2026-03-28** (2026-03-27T21:38:49-07:00) |
| Duration | **10:20** (620 s) |
| Views | **96,601** |
| Likes | **2,217** |
| Comments | **81** (81 reported by YouTube; **77 retrieved**, incl. replies) |
| Category | News & Politics |
| Sponsor | Finanjo (paid segment) — flagged by commenters |

## What the video is about (FACT — from creator's description)

It is a weekly startup-news round-up; the Ownly story is the lead segment (00:00–05:19). The Ownly argument:

- Swiggy/Zomato platform fees rose from **₹2/order in 2023 to ₹14.9 (Zomato) and ₹17.58 (Swiggy)** — increases of **645% and 790%**. Add 20–40% restaurant commission and **a ₹150 offline meal becomes ₹250–300 online**.
- Rapido attacks with a **zero-commission model aimed at an underserved segment**. Swiggy/Zomato serve ~**25–30M users at AOV ₹430–475**; the real market is **200–300M people spending ~₹100/meal**.
- Rapido aims to bring **70,000 FSSAI-licensed Bengaluru restaurants** online that are invisible to the incumbents; had **onboarded 2,300 Bengaluru restaurants** at time of recording.
- Core structural advantage claimed: **logistics efficiency from complementary demand curves** — ~2M riders already delivering for Zomato/Swiggy/Zepto; bike-taxi peaks at commute hours, food peaks at mealtimes → higher rider utilisation → **₹100-order economics become viable**.
- Other segments (not Ownly): Accel/Prosus "Atoms X LeapTech" cohort, Dream Street, Agnikul/Abyom, Razorpay×Sarvam, weekly funding ($245M; incl. **Swish — $38M at $139M valuation for hyper-fast food delivery in Bengaluru**).

**Stance:** Directly about Ownly/Rapido food-delivery economics. Creator is **analytically favourable but not evangelical** — frames it as a credible structural attack on the duopoly's fee stack rather than a certainty. Several commenters accused the video of being sponsored by Ownly (it is sponsored by Finanjo, a fintech, per the description and the pinned comment).

---

# VIDEO 2 — "Rapido's Genius Strategy to Beat Zomato and Swiggy"

## Metadata (all FACT)

| Field | Value |
|---|---|
| URL | https://www.youtube.com/watch?v=2EI51Z7WQ3o |
| Title | Rapido's Genius Strategy to Beat Zomato and Swiggy |
| Channel | **Backstage with Millionaires** (@backstagewithmillionaires) |
| Published | **2025-06-17** |
| Duration | **9:20** (560 s) |
| Views | **333,613** |
| Likes | **6,063** |
| Comments | **250** (250 reported by YouTube; **199 retrieved**, incl. replies) |
| Category | News & Politics |

This is the **pre-launch / announcement-era** video (~15 months before Video 1), which is why its comments capture *expectation* while Video 1's capture *early lived experience*.

## What the video is about (FACT — from creator's description)

- Opens on restaurant-side pain: named operators **Vandit Malik ("The Garlic Bread")** and **Manish ("Saffroma")** — "zero" net payables, mystery charges, commissions up to 30%, forced deep discounting, no data sharing.
- Swiggy+Zomato hold "nearly 100%" of Indian food delivery (a claim two commenters dispute). **ONDC** promised zero commission but "hasn't taken off due to fragmentation and unreliability."
- **Rapido's "Ownly" strategy**, three pillars:
  1. **Zero commission**, replaced by a **flat delivery fee + flat monthly subscription** (SaaS-like, capped and predictable for restaurants).
  2. **Transparent customer pricing** — no inflated menu prices, no hidden packaging/platform fees; explicit commitment to **match in-restaurant dish pricing**. Cites an **NDTV price comparison** showing Rapido cheaper for the same item.
  3. **Data sharing with restaurants** (vs "consumer masking" on Swiggy/Zomato), letting restaurants own their discount strategy.
- Supply-side claim: **"over 4 million active riders — four times Swiggy and Zomato combined"**; months of collaboration with **NRAI**.
- Ends explicitly asking viewers to debate it in the comments — which is why comment volume and quality are high.

**Stance:** Strongly **pro-Rapido / pro-disruption**, framed as "genius strategy," while conceding Swiggy/Zomato are well-funded incumbents.

---

# AUDIENCE COMMENTS — CODED ANALYSIS

**Retrieval:** FACT, via the InnerTube `/youtubei/v1/next` comment continuation API. **276 comments total** (77 of 81 on Video 1; 199 of 250 on Video 2). The shortfall is reply threads whose continuation chains terminated; there is no evidence of systematic bias in what was missed.

Coding is manual, multi-label (one comment can carry several themes). Counts exclude pure noise (emoji, "first comment", narrator/background-music complaints).

## Theme counts

| Theme | V1 (n=77, post-launch, Mar 2026) | V2 (n=199, pre-launch, Jun 2025) | Total |
|---|---|---|---|
| Price advantage (pro-Ownly on price) | 7 | 18 | **25** |
| Price scepticism — "this won't last" / fee creep / unit economics | 12 | 19 | **31** |
| Restaurant assortment / city coverage gaps | 3 | 2 | **5** |
| Delivery speed / ETA | 1 | 4 | **5** |
| Reliability / fulfilment failure | 1 | 3 | **4** |
| Customer support / refunds | 0 | 6 | **6** |
| Rider pay & rider economics | 8 | 10 | **18** |
| Trust / hygiene / food quality | 0 | 4 | **4** |
| Zero-commission & restaurant-side views | 2 | 11 | **13** |
| Comparisons to Swiggy/Zomato/Toing/other challengers | 6 | 7 | **13** |
| Word-of-mouth / influencer-driven trial (first-hand Ownly usage) | 5 | 2 | **7** |
| ONDC as failed precedent | 3 | 12 | **15** |
| Regulation / bike-taxi bans | 2 | 14 | **16** |
| Disintermediation (order direct, tiffin, self-delivery) | 5 | 3 | **8** |
| App UX / accessibility | 1 | 1 | **2** |
| Creator-credibility scepticism ("sponsored?") | 4 | 0 | **4** |

**The single most important signal:** the ratio flips against Ownly between the two videos. Pre-launch (V2) the dominant tone is rooting-for-the-underdog and rage at Swiggy/Zomato's fee stack. Post-launch (V1), the top-liked comment is a rider-economics objection, and the only first-hand Ownly reviews are split 2 positive / 3 negative.

---

## Theme 1 — Price advantage (25) — FACT, verbatim

The strongest positive pull, but note that almost all of it is **anger at Swiggy/Zomato pricing** rather than measured praise of Ownly.

> "I stopped using Zomato recently & Swiggy long back. I use only Ownly & I pay good enough tip to the captains, a third of the extra money that I would have paid for the food on Zomato or Swiggy. Also, these captains are too humble and deny the tips. We have to ask them to provide the QR Code." — **@noclicheplease** (50 likes, V1)

> "I use their food delivery service "Ownly" and my experiance has been superb. Fast delivery, zero delivery charge, zero platform fee, i pay exactly what i pay at the hotel. The number of restaurant need to improve but there is steady growth" — **@deepakgowda9830** (V2, posted ~3 months ago — i.e. post-launch)

> "I've reached my limit with Zomato and Swiggy's unfair pricing. A local restaurant in Hyderabad , Gachibowli I visit almost daily serves a veg thali for ₹180 and a chicken thali for ₹210 — but on these apps, the same meals are priced at ₹310 and ₹360 respectively! ... I've raised complaints multiple times, and every time the response is the same: "The prices are set by the restaurant." That's just not true — I've seen the menu, I eat there regularly." — **@smondol756** (10 likes, V2) — *directly relevant: this is a Gachibowli, Hyderabad price-delta observation*

> "This would be a game changer if they price as same as restaurant and charge flat delivery fees. I would not hesitate to shift from Zomato and Swiggy." — **@rupaksahu9917** (V2)

> "I unistalled all Food & last minute apps. And save 3-4 K per month 😊" — **@Proud_banda** (36 likes, V1)

> "brand loyalty doesnt exist. cheaper = indians switch brands. This was shown in the study zomato and swiggy did where during the order placement flow customers would switch apps and check price on the other app." — **@StarStalkerGaming** (V2)

> "Now zomato Swiggy adding charges like platform fee, package fee which is absurd! 40 50 rs just for packaging" — **@prateeek12** (V2)

> "almost double rate ho jate hai zomato Swiggy par, hence i stop using it" — **@m.z6437** (V2)

## Theme 2 — Price scepticism / "this won't last" / fee creep (31) — FACT, verbatim

**The largest single theme.** Strongly relevant to survey design: respondents will likely discount an introductory price promise.

> "its the same . another piece of the same pie . **0% today 5% in 1year** ." — **@DeeP_BosE** (3 likes, V1)

> "This is just promotion as they are new to this business. **Once they build customer base, it becomes another zomato and swiggy**" — **@Sanjay-yu4kc** (92 likes, V2)

> "Zomato and Swiggy are hardly making profits. Rapido may come with all guns blazing with 2-3 billions in spending but eventually they'll go to Zomato/swiggy model. **It's impossible to make money without inflating prices.**" — **@Petrolhead11** (11 likes, V2)

> ""Sometimes, in the process of deafeating the villain, you become the villain"" — **@hamdaljamal2180** (10 likes, V2)

> "Discounts can't last forever" — **@dilsere1775** (V1)

> "Mot easy to beat zomato and swiggy very easily!! Rapido have to burn lot of funds on user acquisition i belive but still after those offers people uninstall" — **@davidjaison** (8 likes, V1)

> "Rapido is in massive losses. So, they havent proved unit economics will work. And i am not talking about food delivery, neither their bike taxis nor auto / cabs is making money for them." — **@st0rmchas3r** (V1)

> "₹25 per Delivery under 5 kg is very much unsustainable in the long-term. I think Rapido is making this movie in order to take away customers from Swiggy and Zomato by operating at cutthroat margin" — **@dr_sriraviteja** (V2)

> "OYO did exactly same with the hotel owners resulting in crash of their business and image." — **@prateeksaraswat441** (V2)

> "Knowing our people, I think what may end up happening is **the restaurants will get greedy and submit higher priced menus to Rapido** so they can keep the extra money for themselves instead of passing on the benefit of no commissions to the final consumer" — **@four321zero** (V2)

> "Next RAPIDO will have to charge for ads. No cloud or QSR can run without competition from home based cloud due to price cut. **That ad cost will start pinching hole in restaurant pockets**" — **@SGPT-y7e** (V2)

> "At the end of the day every company thrives for profit 😂😂😂, there is a quote if everything is free them you are the product" — **@KanthiKiranRaghavaRaju** (V1)

> "Sadly these are the same companies who will eventually squeeze ot these riders someday or the other paying the minimal in new india where petrol cost is all time high" — **@Anmol-23VF** (V1)

## Theme 3 — First-hand Ownly usage (7) — FACT, verbatim — **HIGHEST-VALUE FOR US**

Only seven commenters across both videos claim to have actually used Ownly. Verbatim, all of them:

**Positive (3):**
> "I stopped using Zomato recently & Swiggy long back. I use only Ownly & I pay good enough tip to the captains..." — **@noclicheplease** (50 likes, V1)

> "Just ordered from ownly and trust its great" — **@Nitinsinghsiwan** (V1)

> "I use their food delivery service "Ownly" and my experiance has been superb. Fast delivery, zero delivery charge, zero platform fee, i pay exactly what i pay at the hotel. **The number of restaurant need to improve** but there is steady growth" — **@deepakgowda9830** (V2)

**Negative (3):**
> "**Ownly is not that cheap .. I use ownly ..they have no discount on any restaurant .. same menu available in Swiggy with lesser cost after discount**" — **@bitcoinheist7831** (V1) — *the sharpest finding: list-price parity loses to Swiggy's discounted price*

> "**Ownly is shit, bad service, less restraunts, and most of the time they don't deliver.**" — **@Frustrated-Indian-2024** (V1)

> "I tried this application yesterday. The interface is totally shitty and totally inaccessible for anybody who is using assistive technology. According to me. This application is a failure. **It may offer good prices, but in terms of UX, it's fucked up.** 👎🏻" — **@Mister-Kayne** (V1)

**Availability-blocked (2):**
> "Ownly is still not available at my location in Pune, unfortunately." — **@mihirchitnis905** (V1)
> "It's not available in Kolkata too." — **@souravsaha8377** (V1)

## Theme 4 — Rider pay & rider economics (18) — FACT, verbatim

**Top-liked comment on Video 1 is this theme** — the audience's #1 doubt about Ownly post-launch is supply-side, not demand-side.

> "Correct me if I'm wrong: **Ownly's main challenge is delivery economics—riders earn more per hour from bike taxi than from Ownly food delivery.**" — **@guruprasadah7178** (125 likes, V1 — top comment)

> "Yes you're ryt, and **we cannot do more than 2-3 food deliveries per hour because it needs time to prepare**" — **@dragonarena5489** (16 likes, V1, reply to the above)

> "thats actually a myth in that time they get parcels which pays them more then the ride hailing per km" — **@dragonarena5489** (V1, counterpoint)

> "**Rapido cares about its drivers a lot**, saying this after having spoken to multiple rapido bike riders. So they already have trust" — **@thequietgal** (731 likes, V2 — top comment overall)

> "Basically Ownly will exploit riders more. 🙂" — **@ankitmaurya2732** (V1)

> "what is there to exploit , its not like they are forced to do it , its riders wish if they want to deliver food or do bike taxi" — **@avinashvarma3543** (V1, rebuttal)

> "Don't worry guys , there are crores of people ready for doing low cost delivery ... india has 30-50 crore people who earn less than 15k per month doing some sort of manual labour, so many of them would be happy working as delivery riders for 25k-35k per month" — **@Shhhhhhhhhhh09** (8 likes, V1)

> "Still rapido drivers instead of asking customers to pay through Rapido's UPI QR, **they ask customers to pay to their personal QR** and mention that customer has given cash" — **@subammalakar7791** (39 likes, V2)

> "Oh really what about rapido misusing tipping system ? Now whenever i book a cab/bike/auto on the stated price **no driver picks it up, i always have to add the mentioned 20-50rupees extra** for riders to pick up ! The riders have made the additional tip a habit now which is frustrating." — **@mohit25** (V2)

> "Just so everyone knows, **Rapido underpays their driver so much, that in my city, the norm is for the driver to call you as soon as you book the ride and quote his actual price.** So, real life example, the ride that comes up as 45 on the app, will not be entertained for anything less than 60." — **@atrezoa** (V2)

> "Rapido 😂😂😂😂 As a rapido rider we know the truth." — **@ankn01** (V2, self-identified rider)

> "Zomato is paying their riders 5rs/km. Don't buy food from Zomato very very bad company. They don't care about rider, restaurant and customer." — **@Vijay_8055_5** (V2)

## Theme 5 — Zero-commission & restaurant-side views (13) — FACT, verbatim

> "Nice analysis, **restaurant owners like me were looking for an alternative of swiggy/zomato**, hope rapido works better 👍" — **@addyjain1** (15 likes, V2)

> "Being in a restaurant business, I really hope rapido works. And **the commission from small players is 30%+PG+GST. And restaurants do not get GST return, so effective commission for us is 37.5%**" — **@logicalindian_777** (V2)

> "As a restaurant owner Zomato and Swiggy drinks Blood" — **@NaveenKumar-oo7rk** (V2)

> "My brand inhouse magic has even worse its showing negative balance. **25000 + gst they took before listing for brand advertising and after that negative bal. Of sales**" — **@Geetikajain78** (V2)

> "ONDC is totally flop. Magic pin runs on ONDC and visibility compared to Zomato and Swiggy is Zero. **Magic Pin has subscription of 25K which is too high and ROI of this subscription is 2.5** which is very pathetic. Zomato is bring new comission plans which will eat up more restarunt profits. **For small cloud kitchens running ads on Zomato and Swiggy is like totally burning money.** Swiggy is very bad on visibility and gives low orders compared to Zomato." — **@ModernDIYCraftsman** (V2)

> "Nobody is saint here. Zomato charges such commissions and earn. **Restaurant owners inflate their pricing by 30%.** Its finally the customer who is at complete loss." — **@parveendang297** (26 likes, V2)

> "The restaurants do set the price but as you said it's because of the **dark patterns used by Swiggy they are forced to**." — **@SlitheringDemon** (V2)

> "In-fact, **restaurant will be the first to cut off Rapido if they don't give them enough number of orders a day.**" — **@SuDharx732** (V2)

## Theme 6 — Assortment, reliability, speed/ETA, support, quality (19 combined) — FACT, verbatim

**Assortment (5):** "less restraunts" (@Frustrated-Indian-2024), "The number of restaurant need to improve" (@deepakgowda9830), not available in Pune (@mihirchitnis905), not in Kolkata (@souravsaha8377).

**Reliability / fulfilment (4):**
> "most of the time they don't deliver" — **@Frustrated-Indian-2024** (V1, about Ownly)
> "I have completely stopped ordering from Swiggy and zomato since a year, **the food isn't delivered properly** and are always on the higher price point and you don't even get fresh food or you get in an toxic containers and some of the cloud kitchen are just very irresponsible to own up their mistake ... **zero accountability if something goes wrong**" — **@aspaldyko** (V2)

**Speed / ETA (5):**
> "This duopoly is really bad for us. Back in my hostel days at NIT, I depended on food delivery for four semesters. **What still stings is how they played with delivery times. They'd show 20–30 minutes, but the clock stayed stuck while I sat there starving, and the food finally came after almost an hour. It wasn't the waiting, it was being lied to.**" — **@Vegetafrompatna** (V2)
> "strategy won't work. **People don't order food because it's low cost. People order because of experience and on-time delivery**; both of which require significant amount of resources." — **@SuDharx732** (V2)
> "Food delivery sucks you need to wait like 10-30 minutes on order waste of time very irritating of they charge less amount." — **@Alphahalo123** (V2)

**Customer support / refunds (6):**
> "swiggy is absolutely disgusting, **their customer support team is as useless as they can be because they have no power to help the customers.**" — **@Timeless_JS** (V2)
> "**The biggest challenge for Rapido will be to maintain food quality**, Swiggy and Zomato allows customers to ask for refund if there is issue with the food but as **Rapido will be just a delivery partner for the restaurant, and then the restaurant might never admit their mistake so customer experience could get worse**" — **@siddharthshekhawat3355** (V2) — *important structural objection to the marketplace-only model*
> "Zomato is just a Greedy scum now. really hope people stop using their service. **No real customer support** while bumping up prices shamelessly." — **@MorikoAdventureX** (V2)
> "Uber might be expensive but **their customer service is 10X better** IMO." — **@imShivamKumar** (V2)
> "Lastly a decent customer service that address both their delivery partners and customers queries and issues **without having stupid bots to give them predesigned template responses**" — **@KuroAmaya13** (29 likes, V2)

**Trust / hygiene / food quality (4):**
> "Dear Indians, never eat outside food. No one says what they put in your food and it's unhygienic." — **@cs20999** (V2)
> "When first time I order aloo Paratha from one of this platform I get 2 Paratha sabji and aachar with coverd thali and **second time same order same money but I get 1 Paratha covered with foil with no extra item** and then i never order anythin from online food dilivery" — **@motivationworld1339** (V2)

## Theme 7 — Competitor & challenger comparisons (13) — FACT, verbatim

**Toing (Swiggy's low-cost counter) — only appears in V1 (Mar 2026), 3 mentions:**
> "In between all this 'toing' by Swiggy watching silently" — **@Enlighten_pages** (V1)
> "swiggy launch toing to counter it.. Offering food at low cost" — **@Aimer-k4z** (V1)
> "what about TOING have you heard of it? it also does same ?" — **@hot_norr** (V1)

**Others named:** Swish ("Swish is in gurgaon as well, from last 1 week almost everyone in my office is ordering from swish" — @prateekkamra9707, V1); MagicPin (@revmaxrider, @Austin_cooks, @ModernDIYCraftsman); EatClub Pune (@FootballoverzEafc); Rebel Foods/EatSure (@kbiiir); "sukhii delivery — it lists restaurants in Bengaluru that deliver on their own" (@guruprasadah7178, V1); FoodPanda (@onelord215); Namma Yatri (@tru3_light, @Bhuv- "Basically NammaYatri for restaurants"); Grab Malaysia as the model (@pratishthaagarwal2773, 146 likes, V2).

**Market-share dispute (FACT):** two commenters challenge the video's "100% duopoly" claim — @dhanushsuresh7741 and @kbiiir. One claims "zomato has 58% Swiggy has 41 rest 1%" (@kashyap263, unverified).

## Theme 8 — ONDC as the failed precedent (15) — FACT, verbatim

Highly relevant: the audience's default reference class for "zero-commission food delivery in India" is a **failure**.

> "**ondc failed because it was owned by the government.** they should have appointed a private board of directors and a CEO to run it, it would have worked." — **@abhi-t4o1x** (232 likes, V2)
> "making it(ownly) sound revolutionary, **hasnt this already tried (and failed?) by ONDC**, I remember similar video for ONDC 1 year ago." — **@vineeth9258** (7 likes, V1)
> "I think ONDC and Rapido are not good comparison. ONDC had very poor execution. It all depends on How it can be executed." — **@AvaneeshKumar-ei1cw** (14 likes, V2)
> "Ondc is kinda tough to order i still don't know much to order from Ondc" — **@Yashuu-69** (V2)
> "I think you didn't understand much about ONDC. No one orders directly from ONDC. We order from any apps on the ONDC platform like Magicpin, Paytm, Ola, TataNeu, etc." — **@SholayTv** (V2)

## Theme 9 — Disintermediation / substitution away from all apps (8) — FACT, verbatim

> "To order something now I just order by directly calling the shop and they have their own delivery person 😅😅" — **@VaibhavShewale** (91 likes, V1 — #2 comment on V1)
> "I too use the app for menu 😂" — **@prabalmohanty3018** / "Same.. you can also get menu in maps😂" — **@beechaser66** (V1)
> "Tiffin service is still the best in 2026" — **@Worldwidewebsurfer001** (5 likes, V1)
> "I unistalled all Food & last minute apps. And save 3-4 K per month" — **@Proud_banda** (36 likes, V1)

## Theme 10 — Regulation / bike-taxi bans (16) — FACT, verbatim

Material to Ownly's rider-supply thesis.

> "It is absolutely sad that **Rapido got banned in Karnataka**." — **@Statosphy** (343 likes, V2)
> "large market is in maharashtra and **bikes taxis are banned here**." — **@tejasvidhale8677** (31 likes, V1)
> "Rapido 2 wheelers have stopped in Bangalore due to Karnataka high court order. Its been 2 days and Im already missing their service. Auto/cabs literally cost double" — **@sirgobbledygook** (V2)
> "after bangalore banning the 2 wheeler taxi, **this is the best chance to get into food delivery for Rapido**" — **@harshakj2946** (V2)
> "never underestimate the power a auto union 😅" — **@yugeswarreddy4008** (V2)

## Theme 11 — Word-of-mouth / influencer-driven trial (7) — FACT, verbatim

> "Just downloaded. Had heard a lot about it but thanks for reminding me." — **@Ringo-starrrr** (V2)
> "Just ordered from ownly and trust its great" — **@Nitinsinghsiwan** (V1)
> "I stopped online Orders from two years but I start after rapido" — **@Callmanu** (V2)
> "Im a zomato user but with eyes closed i will choose rapido!" — **@syedjawad_edits** (V2)
> "After knowing all this I really wanted to switch to rapido, **but not unless it has dark mode**" — **@itzHaze** (V2)
> "eagerly waiting for rapido to be in food delivery in delhi ncr" — **@kumarshiivam** (V2)
> "I will happily buy rapido's membership rather than swiggy black which is another membership over an existing membership (swiggy one)" — **@farazalikhan5242** (V2)

## Theme 12 — Creator-credibility scepticism (4, V1 only) — FACT, verbatim

> "Video sponserd by ownly?🤔" — **@AKHASHRAM** (28 likes, V1)
> "Video sponsored by Finanjo" — **@anshalmehta4273** (13 likes, V1)
> "PR BS" — **@RB11xRB11** (6 likes, V1)

*(Per the description and the creator's pinned comment, the sponsor is Finanjo, a fintech app — not Rapido. No evidence of Rapido sponsorship was found.)*

---

## Most substantive single comment (V2, 29 likes) — FACT, verbatim in full

> "I would trust Rapido more than Swiggy or Zomato in this aspect. I've had better experiences with Rapido compared to any other similar brands that have been in the industry overall. I'm also seeing a huge backlash from public transports (autos mainly) in cities like Bangalore and Chennai. If they can convert their workforce slowly to food delivery then I feel like the Rapido partners (captains) can even have a better experience and by that I mean if a person is booking rapido bike taxi from point a to point b (assuming 20kms for 250 - 300Rs approx) they don't have to rely on getting all around the city expecting to get another bike taxi ride after completing their previous one.They can earn the same amount by making a bunch of deliveries within the same locality at a much more shorter time. We, as consumers would only need more transparency on restaurant's pricing on food, packing cost (normally a lot of restaurants have a parcel fee), delivery fee and more over deliveries being clubbed together when they are from nearby pick up locations and delivery locations (swiggy made this happen for a while but now they've discontinued it, again lack of transparency from Swiggy). The SaaS model they're coming up with the restaurants is indeed a good plan, **hopefully they don't change it once they grab the market.** If they can keep up with this then it would be a revolution and companies like Swiggy and Zomato will have no option but to fall in line. Lastly a decent customer service that address both their delivery partners and customers queries and issues without having stupid bots to give them predesigned template responses that leads to solution." — **@KuroAmaya13**

Also notable (140 likes, V2), a competitive-strategy objection:
> "About time somebody disrupted this duopoly. But taking on experienced, aggressive, and well-funded incumbents isn't so easy. **Their likely hit-back to Rapido's move of undercutting them on commissions would be to slash their own commissions and start a price war, at least in the overlapping zones, which would nullify Rapido's whole differentiator.** Secondly, **Rapido faces a cold start problem on the supply side** and if they start with few large anchor restaurants, then Z and S will aggressively try to lock them in with lower commissions, etc. **They might be better off disrupting from the bottom by targeting smaller restaurants first and then move upmarket.**" — **@TheProductSense**

---

## What this implies for the Ownly research design (interpretation, not FACT)

1. **Price scepticism outweighs price enthusiasm (31 vs 25), and it is the dominant frame post-launch.** Any survey question on "Ownly is cheaper" should be paired with a durability question ("do you expect this pricing to last 12 months?"). The recurring folk model is literally "0% today, 5% in 1 year."
2. **List-price parity is not the same as being cheapest.** @bitcoinheist7831's objection — Ownly's undiscounted menu price loses to Swiggy's post-discount price — is the single most actionable customer-side finding and should be tested directly as a price-perception item.
3. **Assortment, not price, is the binding constraint in the few genuine user reviews** ("less restraunts", "number of restaurant need to improve", not available in Pune/Kolkata). Supports assortment/coverage as a primary KPI.
4. **The top-liked post-launch comment is a rider-supply objection**, with a rider-side rebuttal about food-delivery throughput (2–3 deliveries/hour because of prep time). Rider-economics questions belong in the fieldwork, not just customer questions.
5. **The marketplace-only model creates a refund/accountability gap** (@siddharthshekhawat3355) — worth an explicit item on "who do you blame when the order is wrong."
6. **ONDC is the audience's reference class for this idea failing.** Framing Ownly as "zero commission" will trigger that prior; framing as "Rapido's rider fleet" triggers a more favourable one.
7. **Toing only enters the conversation in the Mar-2026 video** — the competitive set has shifted since the Jun-2025 announcement.

---

# APPENDIX — ALL RETRIEVED COMMENTS, VERBATIM

Retrieved via the YouTube InnerTube comment API. Sorted by like count descending. Newlines inside a comment are shown as " / ". Nothing below has been edited, paraphrased, or reconstructed.

### VIDEO 1 (h6PJ_QB4CiQ) — 77 comments retrieved (YouTube header count: 81)

- **@guruprasadah7178** (125 likes, 5 months ago (edited)): Correct me if I’m wrong: Ownly’s main challenge is delivery economics—riders earn more per hour from bike taxi than from Ownly food delivery.
- **@VaibhavShewale** (91 likes, 5 months ago): To order something now I just order by directly calling the shop and they have their own delivery person 😅😅
- **@noclicheplease** (50 likes, 5 months ago): I stopped using Zomato recently & Swiggy long back. I use only Ownly & I pay good enough tip to the captains, a third of the extra money that I would have paid for the food on Zomato or Swiggy. Also, these captains are too humble and deny the tips. We have to ask them to provide the QR Code.
- **@Proud_banda** (36 likes, 5 months ago): I unistalled all Food & last minute apps. / And save 3-4 K per month 😊
- **@tejasvidhale8677** (31 likes, 5 months ago): large market is in maharashtra and bikes taxis are banned here.
- **@AKHASHRAM** (28 likes, 5 months ago): Video sponserd by ownly?🤔
- **@dragonarena5489** (16 likes, 5 months ago): Yes you're ryt, and we cannot do more than 2-3 food deliveries per hour because it needs time to prepare
- **@anshalmehta4273** (13 likes, 5 months ago): Video sponsored by Finanjo
- **@davidjaison** (8 likes, 5 months ago (edited)): Mot easy to beat zomato and swiggy very easily!! Rapido have to burn lot of funds on user acquisition i belive but still after those offers people uninstall
- **@Shhhhhhhhhhh09** (8 likes, 5 months ago (edited)): Don't worry guys , there are crores of people ready for doing low cost delivery, /  /  because in terms of delivery riders we have in our country  / There is more supply of them than their demand  /  / Don't forget india has 30-50 crore people who earn less than 15k per month doing some sort of manual labour, so many of them would be happy working as delivery riders for 25k-35k per month  /  / That's my opinion
- **@HritikRaj** (7 likes, 5 months ago): Swiggy and zomato both currently have 17.58 platform fee inc gst
- **@vineeth9258** (7 likes, 5 months ago): making it(ownly) sound revolutionary, hasnt this already tried (and failed?) by ONDC, I remember similar video for ONDC 1 year ago.  Miss Caleb in this channel, and the quality has deteriorated so much since.
- **@noclicheplease** (7 likes, 5 months ago):  @RB11xRB11  Why da? Burning under? Employee or investor of Sha-mato or Sha-wiggy?  /  / For the uninitiated, sha is a shortform for LKB.
- **@RB11xRB11** (6 likes, 5 months ago): PR BS
- **@imguru_07** (5 likes, 5 months ago): AOV / swiggy: 430 / zomato: 475 /  / 300 million Indians eat out every month. Swiggy and Zomato caters to only 25-30 million of them. People spend about 100 rs while eating out. But 100 rs orders don't make sense to the delivery platforms.
- **@Worldwidewebsurfer001** (5 likes, 5 months ago): Tiffin service is still the best in 2026
- **@mantraeditzstudio** (4 likes, 5 months ago): First comment .❤ / Kitna berojgar hu video aate hi dekh liya 😂
- **@dragonarena5489** (4 likes, 5 months ago): ​ @badgerking200 thats actually a myth in that time they get parcels which pays them more then the ride hailing per km
- **@Lucifer-pn5fz** (4 likes, 5 months ago): There is a big difference between companies run by gov n a pvt entity
- **@Anonymous-n9q** (3 likes, 5 months ago): 7:18 they don't have a name yet, but got  funded ? Wtf no name, no product but got funded ?
- **@DeeP_BosE** (3 likes, 5 months ago): its the same . another piece of the same pie  . 0% today 5% in 1year .
- **@Enlighten_pages** (2 likes, 5 months ago): In between all this 'toing' by Swiggy watching silently
- **@chiranjivg2605** (2 likes, 5 months ago): We all should make sure we will shift from some platform which charges more irrespective of its size if some one increases price we should stop ordering completely let them close they dont care about us why should we
- **@mihirchitnis905** (2 likes, 5 months ago): Ownly is still not available at my location in Pune, unfortunately.
- **@Aimer-k4z** (2 likes, 5 months ago): 0:44  swiggy launch toing to counter it.. Offering food at low cost
- **@VergeMania** (2 likes, 5 months ago): Please make a video about GATE Exam Scam 2026, Students needs your Support
- **@afanhasan-n4z** (2 likes, 5 months ago): Shame on you for advertising Dream 11.
- **@guruprasadah7178** (2 likes, 5 months ago): recently found something called sukhii delivery — it lists restaurants in Bengaluru that deliver on their own, might help you.
- **@gopaljee1467** (2 likes, 5 months ago): True
- **@arulasveen** (2 likes, 5 months ago): I thought that was lifted some time ago?
- **@Paradoxical321** (2 likes, 5 months ago): Ondc was poorly implemented though
- **@misai04** (2 likes, 5 months ago): A company has to earn profit to sustain it's buisness and on the way people are getting good deals and Rapido also destroying duopoly which is good for customers
- **@kunaldev1257** (2 likes, 5 months ago): Yes it can..... Swiggy zomato too much commissions
- **@backstagewithmillionaires** (1 likes, 5 months ago): https://finanjo.com/download - Download Finanjo here /  / Indian Startup Funding Database: https://meadow-pillow-7fa.notion.site/BwM-Startup-Funding-Database-303101b874824f4c91fae9fc8ce6d450 /  / This week’s funding: https://meadow-pillow-7fa.notion.site/W12-Q4-FY26-32f08566a3608045b332fe685c56a316 /  / Funding over time: https://docs.google.com/spreadsheets/d/10-sWaL38VYz--CqQNMQEwsG9xRBAx3nwOLRKzRD4BkY/edit?gid=0#gid=0
- **@goan_guy01** (1 likes, 5 months ago): I loved the editing of this video.
- **@hot_norr** (1 likes, 5 months ago): what about TOING have you heard of it? it also does same ?
- **@notthatweirdfr4468** (1 likes, 5 months ago): 8:43 where can I find this data ?
- **@ankitmaurya2732** (1 likes, 5 months ago): Basically Ownly will exploit riders more.  /  / 🙂
- **@kunaldev1257** (1 likes, 5 months ago (edited)): We need to stop Swiggy zomato, amazon, Flipkart .....tooo much commissions
- **@bitcoinheist7831** (1 likes, 5 months ago): Ownly is not that cheap .. I use ownly ..they have no discount on any restaurant .. same menu available in Swiggy with lesser cost after discount
- **@KanthiKiranRaghavaRaju** (1 likes, 5 months ago (edited)): At the end of the day every company thrives for profit 😂😂😂, there is a quote if everything is free them you are the product 😎😎😎
- **@Frustrated-Indian-2024** (1 likes, 5 months ago): Ownly is shit, bad service, less restraunts, and most of the time they don't deliver.
- **@prabalmohanty3018** (1 likes, 5 months ago): I too use the app for menu 😂
- **@beechaser66** (1 likes, 5 months ago): Same.. you can also get menu in maps😂
- **@mohdayaz690** (1 likes, 5 months ago): ​ @Shhhhhhhhhhh09 sure
- **@souravsaha8377** (1 likes, 5 months ago): It's not available in Kolkata too.
- **@mantraeditzstudio** (1 likes, 5 months ago): Yes 😂
- **@rsreeharsha7266** (1 likes, 5 months ago): Yes
- **@adithya9811** (1 likes, 5 months ago): Why does it bother you?
- **@avinashvarma3543** (1 likes, 5 months ago): what is there to exploit , its not like they are forced to do it , its riders wish if they want to deliver food or do bike taxi
- **@quickSilverXMen** (0 likes, 5 months ago): 9:35 Awesome company got to know. Thanks
- **@AadiParekh-r3e** (0 likes, 5 months ago): crazy content
- **@Nitinsinghsiwan** (0 likes, 5 months ago): Just ordered from ownly and trust its great
- **@prateekkamra9707** (0 likes, 5 months ago): Swish is in gurgaon as well, from last 1 week almost everyone in my office is ordering from swish
- **@tru3_light** (0 likes, 5 months ago): did rapido really introduce zero commission model for autos or Namma yatri did?
- **@mithunmahato309** (0 likes, 5 months ago): every quick commerce business or bike taxi business or food delivery business are the same. any one can breach into others' business. every ones main asset is their bike drivers' fleet. 😂
- **@Akraju-f7b** (0 likes, 5 months ago): Deccan AI 25million dollars
- **@Anmol-23VF** (0 likes, 5 months ago): Sadly these are the same companies who will eventually squeeze ot these riders someday or the  other paying the minimal in new india where petrol cost is all time high
- **@shivamvarma374** (0 likes, 5 months ago): Next video make in hindi please 😊😊
- **@soumikroy6549** (0 likes, 5 months ago): economically gig economy does not make any scene. atleast i do not understand it. it so feels like a rent seeking behaviour. most IMs try to solve one thing information asymetry like banks brokers and many others. in a such dense network i dont know how much asymetry to begin with. this model is atleast beyond my understanding where is the economic value.
- **@emonbhuiyan4034** (0 likes, 5 months ago): Uber tried this and failed.
- **@Beastinterests11** (0 likes, 5 months ago): They all are doing for blockbuster IPOs to loot public money
- **@Mister-Kayne** (0 likes, 5 months ago): I tried this application yesterday. The interface is totally shitty and totally inaccessible for anybody who is using assistive technology. According to me. This application is a failure. It may offer good prices, but in terms of UX, it’s fucked up. 👎🏻
- **@st0rmchas3r** (0 likes, 5 months ago): Rapido is in massive losses. So, they havent proved unit economics will work. And i am not talking about food delivery, neither their bike taxis nor auto / cabs is making money for them.
- **@Hunterr077** (0 likes, 5 months ago): I don't think rapido can disrupt this market
- **@Priyaykanth2** (0 likes, 5 months ago): ​ @Shhhhhhhhhhh09  / This system is not long lasting
- **@MZA-5-7** (0 likes, 5 months ago):  @noclicheplease what is lkb
- **@ankitkumar6130** (0 likes, 5 months ago): ​ @MZA-5-7 right it's still isn't helping I mean why use acronyms that aren't common
- **@Worldwidewebsurfer001** (0 likes, 5 months ago): ​ @noclicheplease How much money does one get to make comments and spread propaganda online. Where can I get this job. I need some money
- **@noclicheplease** (0 likes, 5 months ago):  @Worldwidewebsurfer001  I don’t know about such things bro. May be you should ask your father for claiming you as his son, even though when he is not.
- **@Aimer-k4z** (0 likes, 5 months ago): Swiggy launch 'toing' to counter it..
- **@goan_guy01** (0 likes, 5 months ago): Same question
- **@PankajSingh-jw7fn** (0 likes, 5 months ago): Have linked it in the pinned comment :)
- **@RabindraGuptaTeli** (0 likes, 5 months ago): Your story
- **@DeeP_BosE** (0 likes, 5 months ago):  @adithya9811  its comic now , not bothersome
- **@ankitmaurya2732** (0 likes, 5 months ago): ​ @avinashvarma3543   why anyone become rider ?? Cause they can't get other opportunities right ??  /  / As the technology change, requirment changes, time changes the jobs also changes.  /  / This is full time job and professional career across globe.  /  / And by your logic companies shouldn't pay them even what they are paying now ?? Cause it's a volunteer and it's rider choice according to you ??  /  / By this rubbish logic you or any tech employee shouldn't be paid cause every job is voluntary work. No one force anyone to do any job.  /  / Its simple if demand increase, supply should also increase and pay should also increase.
- **@dilsere1775** (0 likes, 5 months ago): Discounts can't last forever

### VIDEO 2 (2EI51Z7WQ3o) — 199 comments retrieved (YouTube header count: 250)

- **@thequietgal** (731 likes, 1 year ago): Rapido cares about its drivers a lot, saying this after having spoken to multiple rapido bike riders. So they already have trust
- **@soumyabrataroy1462** (596 likes, 1 year ago): We definitely need some competition. Thankfully the market is matured and Rapido doesn’t have to spend a bomb in marketing since people are already quite frustrated with the random charges zomato and swiggy adds. Rapido is also requesting restaurants to have a ₹150 meal… I think this will be fun to watch
- **@Statosphy** (343 likes, 1 year ago): It is absolutely sad that Rapido got banned in Karnataka. How they are able to resume soon with the help of the govt. streamlining laws and regulations to such services.
- **@abhi-t4o1x** (232 likes, 1 year ago): ondc failed because it was owned by the government. they should have appointed a private board of directors and a CEO to run it, it would have worked.
- **@pratishthaagarwal2773** (146 likes, 1 year ago): Rapido is likely emulating a model similar to Grab in Malaysia. If done right, they have massive potential to be a disruptor.
- **@TheProductSense** (140 likes, 1 year ago (edited)): About time somebody disrupted this duopoly. But taking on experienced, aggressive, and well-funded incumbents isn't so easy. Their likely hit-back to Rapido's move of undercutting them on commissions would be to slash their own commissions and start a price war, at least in the overlapping zones, which would nullify Rapido's whole differentiator. Secondly, Rapido faces a cold start problem on the supply side and if they start with few large anchor restaurants, then Z and S will aggressively try to lock them in with lower commissions, etc. They might be better off disrupting from the bottom by targeting smaller restaurants first and then move upmarket. This is becoming a very interesting sector to watch. More power to Rapido.
- **@Sanjay-yu4kc** (92 likes, 1 year ago): This is just promotion as they are new to this business. Once they build customer base, it becomes another zomato and swiggy
- **@psriharsha18** (80 likes, 1 year ago): In its initial years, Rapido was restricted to advertise in our city Hyderabad, since a top politician had partnership in UBER. I hope such hurdles are not caused  to Rapido now.
- **@sahilx4954** (50 likes, 1 year ago): I'm rooting for Rapido.
- **@Statosphy** (48 likes, 1 year ago):  @yugeswarreddy4008  Yeah. I know. But why ban it? Instead, cant they create laws for regulating the industry?
- **@AnnaDutto-v6k** (44 likes, 1 year ago): Swiggy and Zomato have grown not primarily because of a large network, efficient logistics, or superior customer experience, but largely due to heavy funding. Funding is the main driver behind their dominance. They also seem to resist new entrants in the market, as investors want quick returns on their investments. This has led to unhealthy competition and practices that discourage the entry of potentially better players.
- **@yugeswarreddy4008** (41 likes, 1 year ago): ​ @Statosphy  vote bank
- **@subammalakar7791** (39 likes, 1 year ago): Still rapido drivers instead of asking customers to pay through Rapido's UPI QR, they ask customers to pay to their personal QR and mention that customer has given cash
- **@Rōnin395** (32 likes, 1 year ago): Even UPI succeeds because of apps like Paytm and phonepay etc
- **@imShivamKumar** (30 likes, 1 year ago): rapido leaks the customers' phone number and lets the drivers know who complained against them for overcharging, Imagine the safety issue for girls due to this.
- **@KuroAmaya13** (29 likes, 1 year ago (edited)): I would trust Rapido more than Swiggy or Zomato in this aspect. I've had better experiences with Rapido compared to any other similar brands that have been in the industry overall. I'm also seeing a huge backlash from public transports (autos mainly) in cities like Bangalore and Chennai. If they can convert their workforce slowly to food delivery then I feel like the Rapido partners (captains) can even have a better experience and by that I mean if a person is booking rapido bike taxi from point a to point b (assuming 20kms for 250 - 300Rs approx) they don't have to rely on getting all around the city expecting to get another bike taxi ride after completing their previous one.They can earn the same amount by making a bunch of deliveries within the same locality at a much more shorter time. We, as consumers would only need more transparency on restaurant's pricing on food, packing cost (normally a lot of restaurants have a parcel fee), delivery fee and more over deliveries being clubbed together when they are from nearby pick up locations and delivery locations (swiggy made this happen for a while but now they've discontinued it, again lack of transparency from Swiggy). The SaaS model they're coming up with the restaurants is indeed a good plan, hopefully they don't change it once they grab the market. If they can keep up with this then it would be a revolution and companies like Swiggy and Zomato will have no option but to fall in line. Lastly a decent customer service that address both their delivery partners and customers queries and issues without having stupid bots to give them predesigned template responses that leads to solution.
- **@parveendang297** (26 likes, 1 year ago): Nobody is saint here. Zomato charges such commissions and earn. Restaurant owners inflate their pricing by 30%. Its finally the customer who is at complete loss. Restaurant and platforms are making money. If restaurants were at such huge loss, then we won't even see a single restaurant at these platforms and they will revert to old ways of delivery, self delivery.
- **@bmyadav4633** (25 likes, 1 year ago): Definitely government services never success 😂😂
- **@Statosphy** (25 likes, 1 year ago):  @yugeswarreddy4008  That's what I don't understand. There are many Rapido riders whose life will get affected drastically as many would've taken loan to buy the vehicle or other for other purposes. Now the option they have is to move to Zomato, Swiggy etc. Hope they teach the govt. a lesson for messing with their bread and butter.
- **@ankn01** (22 likes, 1 year ago): ​ @imShivamKumar rapido rider here, you never know who complained about you and in case of female customer, we cannot contact them directly, only can be connected by rapido channels only .
- **@sahildasgupta2002** (17 likes, 1 year ago): I will be rooting for rapido
- **@BlazeDJ18** (17 likes, 1 year ago): actually under 100. And now Swiggy has also implemented this. Just today i saw that i can order a single parantha or ice cream for like 50-60 without delivery charge. Competition is always good for customers.
- **@user13rs258** (16 likes, 1 year ago): It does show that even restaurants didn't focused on capturing customer base by learning the most ordered foods and from where customers orders the food.. both matters because tomorrow you can just shift there and open your kitchen and sell food now efficiently coz you're the neighbor too... but most companies thinks to just gain profit and sustain.. then take that 0 balance because even Zomato Swiggy wants to do that.. trust is the only place to play your game not played by that game being already played on the table.. become customer centric otherwise you're always a failure just trying to survive with new cheap tricks 😏 / Jai Hind 🇮🇳❤️
- **@addyjain1** (15 likes, 1 year ago): Nice analysis, restaurant owners like me were looking for an alternative of swiggy/zomato, hope rapido works better 👍
- **@AvaneeshKumar-ei1cw** (14 likes, 1 year ago): I think ONDC and Rapido are not good comparison. ONDC had very poor execution. It all depends on How it can be executed. I feel rapido can crack it cause its investors money and they will be careful to spend it and Investor will require growth
- **@MattRodriguez-h7j** (14 likes, 1 year ago): I work with Swiggy as a Principal Architect. My salary is 3 Crores every year. Walmart paid me 1.5 crores. Swiggy doubled my salary. Someone will have to pay - Customer or the Restaurant.
- **@yugeswarreddy4008** (14 likes, 1 year ago): Raid hailing is banned , not the  company
- **@anshul9856** (13 likes, 1 year ago): Then there will be another disruptor 😄
- **@m4jor101** (12 likes, 1 year ago): only bike taxis are banned cause auto gundas can't stomach the fact that they can't scam customers and spineless congress govt that just keep making decision that just keeps making average peoples lives miserable while playing blame game and caste politics
- **@anishgautam9213** (11 likes, 1 year ago): Rapido will definitely pull this off
- **@Petrolhead11** (11 likes, 1 year ago): Zomato and Swiggy are hardly making profits. Rapido may come with all guns blazing with 2-3 billions in spending but eventually they’ll go to Zomato/swiggy model. It’s impossible to make money without inflating prices.
- **@yugeswarreddy4008** (11 likes, 1 year ago): ​ @Statosphy  never underestimate the power a auto union 😅
- **@smondol756** (10 likes, 1 year ago): I've reached my limit with Zomato and Swiggy's unfair pricing. A local restaurant in Hyderabad , Gachibowli I visit almost daily serves a veg thali for ₹180 and a chicken thali for ₹210 — but on these apps, the same meals are priced at ₹310 and ₹360 respectively! That's a massive hike, and I’m not even counting the unlimited refills and better portion sizes you get when you dine in. /  / I’ve raised complaints multiple times, and every time the response is the same: “The prices are set by the restaurant.” That’s just not true — I’ve seen the menu, I eat there regularly. This kind of misleading markup is a clear malpractice and needs to stop ASAP. /  / Stop taking customers for a ride. Transparency and fairness matter.
- **@hamdaljamal2180** (10 likes, 1 year ago): “Sometimes, in the process of deafeating the villain, you become the villain”
- **@Rōnin395** (9 likes, 1 year ago): ​ @BpositiveDoctor Bro is probably a Govt. employee 💀
- **@amazingdude9042** (9 likes, 1 year ago): finally some sensible comment.
- **@aaria.aum.v** (9 likes, 1 year ago): They didn't do that on their ride platform, I've been using it for a while. I hope it keeps this up.
- **@m4jor101** (8 likes, 1 year ago): India is a price sensitive market. Most people would opt for value even if it offers lesser convenience but not at the cost of poor customer service and brand trust. I'm sure Rapido is aware of that with their existing business of bike taxis and other
- **@SholayTv** (7 likes, 1 year ago): I think you didn't understand much about ONDC. No one orders directly from ONDC. We order from any apps on the ONDC platform like Magicpin, Paytm, Ola, TataNeu, etc.
- **@imShivamKumar** (7 likes, 1 year ago):  @ankn01  nope, i have seen riders call me with personal numbers, not company network numbers, and when we try to raise a a dispute why is the rider also connected to the chat. Ofcourse he will deny any wrongdoing, Is this just a tactic to discourage users from not making a complaint. rapido has a lot to learn. Uber might be expensive but their customer service is 10X better IMO.
- **@anirudhchowdary2166** (7 likes, 1 year ago): Its kinda similar to how they started. Started with bikes then auto, then slowly cab services
- **@sirgobbledygook** (6 likes, 1 year ago): Rapido 2 wheelers have stopped in Bangalore due to Karnataka high court order. Its been 2 days and Im already missing their service. Auto/cabs literally cost double
- **@kaustavmondal9235** (6 likes, 1 year ago): 😂
- **@BpositiveDoctor** (6 likes, 1 year ago):  @bmyadav4633 😂😂 SBI, LIC, Coal India, NTPL is running by your father?
- **@ajeeshsunil** (6 likes, 1 year ago):  @BpositiveDoctor  3, 4 aren't consumer facing companies (bad comparison), and sbi n lic had a mightier head starts / we have companies like air India stuggles to talk about
- **@unnisapp** (6 likes, 1 year ago): Congress may have asked for a bribe. Maybe they didn't pay on time 😅
- **@vitsboy46** (5 likes, 1 year ago): Rapido is awesome they want revenue before they burn investors money. It's a very sustainable business model given how bike taxis are being banned. It's futuristic
- **@SlitheringDemon** (5 likes, 1 year ago): The restaurants do set the price but as you said it's because of the dark patterns used by Swiggy they are forced to.
- **@pulkitjain8135** (4 likes, 1 year ago): Genius stratergy❌ / Only way left✅
- **@mohit25** (4 likes, 1 year ago): Oh really what about rapido misusing tipping system ? Now whenever i book a cab/bike/auto on the stated price no driver picks it up, i always have to add the mentioned 20-50rupees extra for riders to pick up ! The riders have made the additional tip a habit now which is frustrating. Why scam customers by showing cheaper rates than uber/ola, directly add the amount to the fare shown in the app.
- **@cs20999** (4 likes, 1 year ago): All vc money is ending up in Google and Facebooks pockets
- **@subammalakar7791** (4 likes, 1 year ago): Unke khud ka BHIM nahi chal raha
- **@ajeeshsunil** (4 likes, 1 year ago):  @Rōnin395  if govt never supported the infrastructure, these apps too wouldn't work out too
- **@arai_19999** (4 likes, 1 year ago): What has your salary got to do here? 🤔 And a simple google search tells something else all together.
- **@sankalpshambharkar75** (3 likes, 1 year ago): Your journey would be more interesting than Rapido, keep going ❤
- **@AnshumanSingh-uv7ez** (3 likes, 1 year ago): With the kind of trust Rapido has built over the last few years, i feel they can enter into the food market and focus on customer satisfaction and satisfaction of service providers as well. Looking forward to this.
- **@farazalikhan5242** (3 likes, 11 months ago): I will happily buy rapido's membership rather than swiggy black which is another membership over an existing membership (swiggy one)
- **@cs20999** (3 likes, 1 year ago): Dear Indians, never eat outside food. No one says what they put in your food and it's unhygienic.  /  /  Eat healthy, organic and hygienic food at your home
- **@SuDharx732** (3 likes, 1 year ago): Cool video, but strategy won't work. People don't order food because it's low cost. People order because of experience and on-time delivery; both of which require significant amount of resources. In-fact, restaurant will be the first to cut off Rapido if they don't give them enough number of orders a day.
- **@BpositiveDoctor** (3 likes, 1 year ago):  @Rōnin395 😂😂 noob. Whats paytm, phonepays contribution to UPI?? ZERO. They r crying from start to put some changes on UPI as MDR, govt is denying.
- **@shakuntalamishra-f8d** (2 likes, 1 year ago): the background tells a very different story ......... how india has changes .......... politically ........... and i am loving it
- **@Callmanu** (2 likes, 1 year ago): I stopped online Orders from two years but I start after rapido
- **@the_sambar_vada** (2 likes, 1 year ago): Doesn't seem to be sustainable.
- **@Anujkumar-cx6cw** (2 likes, 1 year ago): that swami vivekananda image in the background, it has wrongly translation of that sanskrit line. even google have it wrong. "Arise, awake, find out the great ones and learn of them" This is the correct meaning of that Sanskrit verse.
- **@draxiii9765** (2 likes, 11 months ago): Stupid me ordering a KFC Wednesday bucket of 399 for 649 from Swiggy and zomato 😂😂
- **@Timeless_JS** (2 likes, 11 months ago): swiggy is absolutely disgusting, their customer support team is as useless as they can be because they have no power to help the customers.
- **@bmyadav4633** (2 likes, 1 year ago): ​ @BpositiveDoctor  Abe govt employee wah public hai aur govt ki kuchh share holder hai isliye world ka worst service ke naam se jana jata hai nhi pata. Isliye bolata hu thoda bahar bhi duniya hai bihari
- **@idhruv0001** (2 likes, 1 year ago): Wait for cupon 😂
- **@Ringo-starrrr** (1 likes, 1 year ago): Just downloaded. Had heard a lot about it but thanks for reminding me.
- **@prateeksaraswat441** (1 likes, 1 year ago): OYO did exactly same with the hotel owners resulting in crash of their business and image.
- **@siddharthshekhawat3355** (1 likes, 1 year ago): The biggest challenge for Rapido will be to maintain food quality, Swiggy and Zomato allows customers to ask for refund if there is issue with the food but as Rapido will be just a delivery partner for the restaurant, and then the restaurant might never admit their mistake so customer experience could get worse
- **@raghavendramerwade** (1 likes, 1 year ago (edited)): I think even dunzo declared the same with  plans to entering restaurant delivery..
- **@RxlredE** (1 likes, 1 year ago): Rapido also scams me. I bought bike pass for 69.. to get 10 rupees off. But it showed 80 before taking the pass.. but after it took it.. it become 70.. but no rider was accepting.  It suggests to tip 10rs  20rs to get accepted.  Really disappointed.
- **@m.z6437** (1 likes, 1 year ago): almost double rate ho jate hai zomato Swiggy par, hence i stop using it
- **@dr_sriraviteja** (1 likes, 1 year ago): ₹25 per Delivery under 5 kg is very much unsustainable in the long-term. I think Rapido is making this movie in order to take away customers from Swiggy and Zomato by operating at cutthroat margin / The reason Rapido has overtaken Ola is because they lost focus on ride healing services and got invested into various fields such as EVs and AI. / Uber has always been considered as somewhat premium service so it’s share is unbeatable, especially in cities with a lot of corporate employees.
- **@farazalikhan5242** (1 likes, 11 months ago): Rapido is good in 2025, hopefully it stays the same in the future
- **@chakkardhar** (1 likes, 1 year ago): Great idea.
- **@copi4766** (1 likes, 1 year ago): Anything to takedown Zomato and Swiggy im all in
- **@NaveenKumar-oo7rk** (1 likes, 1 year ago): As a restaurant owner Zomato and Swiggy drinks Blood
- **@StarStalkerGaming** (1 likes, 1 year ago): brand loyalty doesnt exist. cheaper = indians switch brands. This  was shown in the study zomato  and swiggy did where during the order placement flow customers would switch apps and check price on the other app. This is true for products on amazon and flipkart as well.
- **@anirudhkumar4507** (1 likes, 11 months ago): MAGICPIN USES ONDC!!!!
- **@onelord215** (1 likes, 11 months ago): Bring back FoodPanda 😜
- **@Alphahalo123** (1 likes, 1 year ago): Food delivery sucks you need to wait like 10-30 minutes on order waste of time very irritating of they charge less amount. Drivers will Disable food delivery and they'll pressure to enable and The Empire might slowly fall
- **@abc_cba** (1 likes, 1 year ago (edited)): It can be of help to poor people who can't afford Swiggy and Zomato!!  /  / For me, I can afford both Swiggy and Zomato, so, it is not a concern for me.
- **@ModernDIYCraftsman** (1 likes, 1 year ago): ONDC is totally flop. Magic pin runs on ONDC and visibility compared to Zomato and Swiggy is Zero. Magic Pin has subscription of 25K which is too high and ROI of this subscription is 2.5 which is very pathetic. Zomato is bring new comission plans which will eat up more restarunt profits. For small cloud kitchens running ads on Zomato and Swiggy is like totally burning money. Swiggy is very bad on visibility and gives low orders compared to Zomato.
- **@aspaldyko** (1 likes, 1 year ago): I have completely stopped ordering from Swiggy and zomato since a year, the food isn't delivered properly and are always on the higher price point and you don't even get fresh food or you get in an toxic containers and some of the cloud kitchen are just very irresponsible to own up their mistake if the food is bad, this comes to even the platform who are serving the consumers almost zero accountability if something goes wrong and I have seen delivery boys apologize like literally beg to consumers if something goes wrong I mean the rating system and feedback isn't properly implemented by both of these platforms, these all problems never existed when restaurants had their own delivery and service fleet, cause there is only one to question if something goes wrong, the restaurant, the lack of accountability and transparency is what any company will go down in near future straight simple fact.
- **@SGPT-y7e** (1 likes, 9 months ago): Firstly comparing with government platform is not right. None of the Indian govt companies are transparent. ONDC was made to impress, it's propoganda based. They don't have proper workforce. Its a mismanaged corrupt initiative. /  / Next RAPIDO will have to charge for ads. No cloud or QSR can run without competition from home based cloud due to price cut.  / That ad cost will start pinching hole in restaurant pockets
- **@ankn01** (1 likes, 1 year ago): Rapido 😂😂😂😂 /  / As a rapido rider we know the truth.
- **@RONNY7168** (1 likes, 1 year ago): I have face every ride I have taken from rapido car or auto is very bad condition
- **@code_name_uzi** (1 likes, 1 year ago): Good for people like us single, student also trying to diet. The food portion is for atleast 2 3 people but since we have paid and we dont want to wastz because no place to store and reheat and eat tomorrow we just eat the whole thing 🥲
- **@RajaJi11.11** (1 likes, 1 year ago): The restaurant do charge more because ZOMATO Swiggy charge 30% on order received so the restaurant has to increase the prices and also you can’t assume to get the same prices when sitting at home enjoying a service at a finger tip. You can always go to the restaurant and enjoy it there.
- **@jaylalakiya** (1 likes, 1 year ago): I think it exists. I order from amazon even if price is little bit higher than flipkart. Becs my experience with Amazon's customer support is top notch while I have suffered with flipkart's support and their delivery issues as well. So I use Amazon for fast delivery and excellent customer support even if prices are little bit higher. (I dont know if its higher but its hypothesis here).
- **@Statosphy** (1 likes, 1 year ago): @verma__shubham True!
- **@n_titled** (0 likes, 1 year ago): Brilliant and would love to see this pivot come to play
- **@umangchhabra311** (0 likes, 1 year ago): Crisp and clear love the format
- **@atharva1509** (0 likes, 1 year ago): Awesome posters in the background!!!
- **@hades_deadlock** (0 likes, 11 months ago): Looking forward to Rapido's entry in the food delivery segment. The benefits are there both the restaurant as well as the customer.  / Fixed delivery caps should not be there though. It should be dependent on distance of customer from restaurant because the fuel and time cost of the delivery partner is dependent on these 2 factors. / Transparency will be great as it is a big pain point of hidden or overcharges for various stuff that are not seen when adding items to cart. / Great video on the topic.
- **@kumarshiivam** (0 likes, 1 year ago): eagerly waiting for rapido to be in food delivery in delhi ncr , already spent lakhs on food and groceries from several platforms
- **@GraveSignal21** (0 likes, 1 year ago): I'm very much confident about rapido will
- **@deepakgowda9830** (0 likes, 3 months ago): I use their food delivery service "Ownly" and my experiance has been superb. Fast delivery, zero delivery charge, zero platform fee, i pay exactly what i pay at the hotel. The number of restaurant need to improve but there is steady growth
- **@dasdawn9914** (0 likes, 1 year ago): Rapido is a true revolutionary. They’re the only company that understands Indian needs and constraints. I pray for their meteoric growth.
- **@Annie-s8q2r** (0 likes, 1 year ago): ❤
- **@dibyochowdhury4514** (0 likes, 1 year ago): Hey, can you make a video about the effects of domestic fertilizer companies after the restrictions of Chinese fertilizer imports. Specially those companies like Coromondel Internatinal which have invested in these segments heavily.
- **@deepakmt92** (0 likes, 1 year ago): There are some city specific or town specific apps in some areas. People living in those particular cities or towns make use of those apps. There is a delivery charge. Restaurants only decide whether to give discounts. Such apps are definitely a 3rd choice in those places atleast. Same goes for grocery delivery apps or services too. I don't know how they make money, but it's definitely better than Swiggy or Zomato in those places.
- **@idontwanttotellyou9581** (0 likes, 1 year ago): if this is really do come, this is game changer, destruction of plaftorm feee blah, blah charges........
- **@qalander09** (0 likes, 1 year ago): 8:46  / No brand loyalty when it comes buying same cheaper stuff,on other medium
- **@cherrygoyal7255** (0 likes, 1 year ago): I wish rapido to be successful in their mission  / They have good social vision which benefits restaurants and consumers without their own loss by having  good market strategy .
- **@brzrko** (0 likes, 1 year ago): You talked about hefty commissions & discounting but, also take note that if an item is listed for lets say 100rs, even the customer has to pay for processing charges & gst. EVEN AFTER THE SELLER IS GIVING PLATFROM CHARGES!!! HOW RIDICULOUS IS THAT! The customers & the sellers are both being bled while zomato enjoys its cuts from both parties.
- **@logicalindian_777** (0 likes, 1 year ago): Being in a restaurant business, I really hope rapido works. And the commission from small players is 30%+PG+GST / And restaurants do not get GST return, so effective commission for us is 37.5%
- **@BlazeDJ18** (0 likes, 1 year ago (edited)): idk where the news channel got those prices from but its showing 274 in both Zomato and Swiggy for McChicken Meal. Still Rapido is 40 cheaper. Waiting to test and use the Rapido App, more options are always better for customers as there is more competition.
- **@AarjavDua** (0 likes, 1 year ago): Please share your research resources in the description of these videos.
- **@souravdas9572** (0 likes, 1 year ago): Rapido is now a SAAS company. / Using its technology to find gaps and solving it.  / Like AWS
- **@FootballoverzEafc** (0 likes, 1 year ago): In big city like Pune Eatclub is doing a fabulous job if anybody tried out
- **@harshakj2946** (0 likes, 1 year ago): after bangalore banning the 2 wheeler taxi  / this is the best chance to get into food delivery for Rapido
- **@Randolph-n1l** (0 likes, 1 year ago): Good video but please take it easy with the background music
- **@four321zero** (0 likes, 1 year ago): Knowing our people, I think what may end up happening is the restaurants will get greedy and submit higher priced menus to Rapido so they can keep the extra money for themselves instead of passing on the benefit of no commissions to the final consumer
- **@Bhuv-** (0 likes, 1 year ago): Basically NammaYatri for restaurants. / Good, I wished NammaYatri came up with this first.
- **@rupaksahu9917** (0 likes, 1 year ago): This would be a game changer if they price as same as restaurant and charge flat delivery fees. I would not hesitate to shift from Zomato and Swiggy.
- **@Yashuu-69** (0 likes, 1 year ago): Ondc is kinda tough to order i still don't know much to order from Ondc
- **@tamanna4697** (0 likes, 1 year ago): rapido ftw🚀🚀🚀
- **@conscious-observer11** (0 likes, 1 year ago): I'm fully confident Rapido to solve the issues in food delivery segment  / I know the founders and how they have grown as a ride delivery service provider  / They have strong fundamentals as a company 🎉❤ / I've been customer of Swiggy/Zomato for more than 5 years, feels they went on a wrong path especially Zomato
- **@MohitKumar-y9x4m** (0 likes, 1 year ago): It'll Be Great If Rapido Also Comes
- **@itzHaze** (0 likes, 1 year ago): After knowing all this I really wanted to switch to rapido, but not unless it has dark mode
- **@srbluesun** (0 likes, 1 year ago): Wont it show promos first anyway indirectly forcing them to do them?
- **@jashpyda5548** (0 likes, 1 year ago): Nowadays every Fintech channel that I watch was either absorbed or part of zerodha zero 1network is it coincidence or they are on Fintech shopping spree just curious thoo
- **@the_mcmartin** (0 likes, 1 year ago): I want rapido to succeed in this sector. It works out for everyone without exploiting anyone.
- **@harshitdubey6270** (0 likes, 1 year ago): Whats with the background sound, such scare, why
- **@Cry_MoonNight99** (0 likes, 1 year ago): interesting, now we will see yellow shirt more oh we already see that with blinkit 😂😂
- **@soubhikdey7748** (0 likes, 1 year ago): if i ordered biriyani in zomato i get it for 250 for the ssme biriyani cost me 150 in a small resturent ,sitting capacity 10,verysmall resturent .
- **@anki1392** (0 likes, 11 months ago): I mean  / Everything which Swiggy and zomato can do easily  / This way rapido can eat some market share but cost challanges can it remain sustainable lets see
- **@motivationworld1339** (0 likes, 1 year ago): When first time I order aloo Paratha from one of this platform I get 2 Paratha sabji and aachar with coverd thali and second time same order same money but I get 1 Paratha covered with foil with no extra item and then i never order anythin from online food dilivery
- **@dienzer9098** (0 likes, 1 year ago): rapido sells food?
- **@nemivakhariya7029** (0 likes, 1 year ago): yes we want 3rd player in this market so zomato and swiggy come into Real commission.
- **@stavanraut932** (0 likes, 1 year ago): Imagine a model so good, that every mafia of every major city wants the company to be banned, crazy.
- **@mge82779** (0 likes, 1 year ago): Hope rapids does it..
- **@prateeek12** (0 likes, 1 year ago): Now zomato Swiggy adding charges like platform fee, package fee which is absurd! 40 50 rs just for packaging
- **@revmaxrider** (0 likes, 1 year ago): bro has no idea about MagicPin though its not the top player but its not something to be ignored fully
- **@maddydhilli** (0 likes, 1 year ago): Swiggy and Zomato will be forced to adopt this model.
- **@urvishjoshi6640** (0 likes, 11 months ago): Thanks zerodha but i will still use groww
- **@shomubhattacharjee5660** (0 likes, 1 year ago): Restaurant never bear any cost as they hike the prices to keep the same profit level. The whole extra amt need to be paid by the customers. Foods cost twice as costly now on zomato or swiggy compared to their prices before 2020
- **@code_name_uzi** (0 likes, 1 year ago): 5:11 How meesho is in amazon ang flipkart's game /  / Same rapido will be in zomato swiggy's game /  / Both flipkart and amazon made contender for mesho called shopsy and glowroad respectively  / So lets see
- **@syedjawad_edits** (0 likes, 1 year ago): Im a zomato user but with eyes closed i will choose rapido!
- **@Vegetafrompatna** (0 likes, 11 months ago): This duopoly is really bad for us. Back in my hostel days at NIT, I depended on food delivery for four semesters. What still stings is how they played with delivery times. They’d show 20–30 minutes, but the clock stayed stuck while I sat there starving, and the food finally came after almost an hour. It wasn’t the waiting, it was being lied to. Hunger makes you vulnerable, and instead of honesty, they chose to fool us. I really wished hard for their downfall.
- **@Geetikajain78** (0 likes, 11 months ago): My brand inhouse magic has even worse its showing negative balance. 25000 + gst they  took before listing for brand  advertising and after that  negative bal. Of sales
- **@qalander09** (0 likes, 1 year ago): 2:22  / Incorrect information.. / Swiggy & zomato came later than prev vendors.. zomato was not in delivery services
- **@pratikjain3323** (0 likes, 1 year ago): The bg music is very annoying
- **@vasuthirani7184** (0 likes, 1 year ago): definetly rapido is going to win the game
- **@kautilyabora2432** (0 likes, 11 months ago): we do definitely need a new player in the food delivery market, they started charging unreasonably, what is platform charge taken from resturant as well as customer, this is pure loot
- **@TridentAutolink** (0 likes, 1 year ago): Bhai thoda speed mai bola karo, subah panvel nikalna hai...😂😂
- **@knarsingr2** (0 likes, 11 months ago): If not by Rapido... this will happen soon.
- **@mithunmahato309** (0 likes, 1 year ago): Rapido should not appoint a guy who is just a marketing or sales dependent freak. Better be a tech company.
- **@yourbackbencherbuddy4875** (0 likes, 1 year ago): It's hard for me to digest how restaurants are failing because of Swiggy or zomato they are not cutting their margins let me try to explain with an example if an item costs rupees 100 in the restaurant same item on the platforms will cost 120-130 that extra 20-30% is the platforms cut but the restaurant will get ₹100 the actual price of the product. The benefit for them is that they get a customer to buy the product from remote location. Then how these platforms are killing them!!?
- **@snehasisdebbarman3106** (0 likes, 1 year ago): Now Karnataka banned bike taxi, there is plenty bikers for this , good opportunity for rapido
- **@rajatgoyal9608** (0 likes, 1 year ago): Irony swiggy own shares of rapido
- **@MithleshKumar-oz5oh** (0 likes, 1 year ago): Feedback- the content is really good but every line is ending on the same note with same tone. Gets really annoying after 2-3 minutes of listening
- **@PraveenPal-ye9nt** (0 likes, 1 year ago): Bhai hindi mein banao yrr
- **@mdjohar** (0 likes, 1 year ago): Rapido  : Zerodha of Food delivery business.
- **@sun-door** (0 likes, 11 months ago): wtf is this bg music
- **@dhanushsuresh7741** (0 likes, 1 year ago): stop spreading misinformation,swiggy and zomato combined does not have 100% in food delivery apps like magicpin,ola and other dependent on ondc exist on top of that a lot of local food delivery apps also exist,i know they have the vast majority  but that does mean you put a 100% tag
- **@SuppuNetha_Official** (0 likes, 1 year ago): Swiggy, Zepto, and Rapido use smart marketing strategies to increase their profits, while they just tell us that we’ll get discounts if we use promo codes — that’s all. we are not getting anything.
- **@unshhul** (0 likes, 1 year ago): Damn the cheapest ride i get on rapido 10 by 10
- **@stutichandwani858** (0 likes, 1 year ago): Wait till rapido IPO comes out lol
- **@idioticfun1901** (0 likes, 11 months ago): Zomato's founder has bought multiple expensive cars by the convenience charges that we have to pay. Boycott Zomato and Swiggy
- **@Anvaya24** (0 likes, 9 months ago): I think they will fail badly
- **@RIDINGSANYASI** (0 likes, 11 months ago): Rapido .... भारत शहरों में नही जीता ...
- **@kbiiir** (0 likes, 1 year ago): SWIGGY ZOMATO HAVE 100% MARKET SHARE ? LOL / WHAT ABOUT REBEL FOODS/EATSURE ? 😅
- **@Austin_cooks** (0 likes, 1 year ago): Use magicpin
- **@Mclovin96X** (0 likes, 1 year ago): Zomato is scam
- **@Rishabh-Dev** (0 likes, 1 year ago): I once ordered 3 thalis from Zomato, for just 160₹ from a good restaurant in Delhi. The outlet was offering 65% off on orders above 499₹, max upto 350₹ discount.
- **@MorikoAdventureX** (0 likes, 1 year ago): Zomato is just a Greedy scum now. really hope people stop using their service. No real customer support while bumping up prices shamelessly.
- **@Vijay_8055_5** (0 likes, 1 year ago (edited)): Zomato is paying their riders 5rs/km. Don't buy food from  Zomato very very bad company. They don't care about rider, restaurant and customer.
- **@JagdeepSingh-qm8iq** (0 likes, 1 year ago): dude...the guy who is narrating is giving too much pressure on every last word of the sentences he has spoke. very irritating
- **@rexkraft** (0 likes, 1 year ago): goes to nit pick a case where they didn't even had 13 orders in whole month.. and yet say their buisness rely on swiggy. LIE DETECTED. Not saying swiggy and zomato doesn'tm charge high, they must be but there is lie in you talks which is not showed..
- **@Zelinsky14** (0 likes, 1 year ago): Very irritating tone to listen to, very weird intonation when completing each sentence. Advice to the narrator is to not be monotonous if you stopping a major thought then it makes sense to end with that intonation a couple of times please change your flow of speech every now or then or maintain a neutral flow...
- **@atrezoa** (0 likes, 1 year ago): Just so everyone knows, Rapido underpays their driver so much, that in my city, the norm is for the driver to call you as soon as you book the ride and quote his actual price. So, real life example, the ride that comes up as 45 on the app, will not be entertained for anything less than 60. And if you are a girl and use it to go home, well that's a different story. So yeah, Rapido👎.
- **@niteshkumarsingh1000** (0 likes, 1 year ago): I have stopped ordering food from zomato na Swiggy prices are very inflated every few weeks you can see price increases for same item
- **@RIDINGSANYASI** (0 likes, 11 months ago): Zomato ... केवल एक डिलीवरी सर्विस नही है ....जोमाटो sale करता है .... जोमाटो इस actually the seller नॉट facilitator ....रेस्टॉरेंट इस facilitator । जोमाटो इस doing right । जो बेचेगा वो कमाएगा
- **@snehasishbiswas5049** (0 likes, 1 year ago):  @code_name_uzi  true buddy. Late night starving and study break hours.
- **@chayanpshah8050** (0 likes, 1 year ago): Probably right but ig the cut throat competition, combined with less awareness and other in app inefficiencies led to the downfall
- **@Statosphy** (0 likes, 1 year ago):  @yugeswarreddy4008  True!🤣🤣
- **@dhirpurohit9119** (0 likes, 11 months ago): same in mumbai high court had banned bike taxi
- **@TheProductSense** (0 likes, 1 year ago): Wow, this comment has more likes than views on my videos :(
- **@Harsh12351** (0 likes, 11 months ago): *They're
- **@kalakala6973** (0 likes, 1 year ago): If you had a small restaurant with 25 to 30 lakh profit yearly, will you take on the commission of these platforms on yourself and take a loss?
- **@smondol756** (0 likes, 1 year ago):  @SlitheringDemon but if you talk to theses platforms the will sound so innocent and try to prove that they are not charging anything extra. They are delivering the food at the same price which is not true.  /  / Whatever it is customers is paying high cost. That need to come down.
- **@smondol756** (0 likes, 1 year ago):  @RajaJi11.11  thanks for your suggestion thats what I do. /  / Try to get the version from Swiggy or Zomato once . They will sound so innocent and try to prove that they are just delivering the product without increasing the price.  /  / I am don’t mind paying extra for convenience but the amount or % I am paying is not justified.
- **@gamingwithxan1430** (0 likes, 1 year ago): Yes  you are correct / Yatri redbus easymytrip  rapido  ola phonepe  dtc, onedelhi chalo nammayatri yatrisathi etc. are linked with ondc. /  / In my understanding, / This model is somewhat like upi, but without their own bhim app. All other partner apps are available.
- **@vish5798** (0 likes, 1 year ago): Why not?
- **@the_sambar_vada** (0 likes, 1 year ago): ​ @vish5798 unit economics.
- **@RudraRaut-b5s** (0 likes, 11 months ago): Please no  /  / Similar situation but food delivery apps are only lifeline at 1 am
- **@vish5798** (0 likes, 1 year ago): What do you mean delivery guys literally begging. You mean for rating of delivery or rating for restaurant?
- **@prasadshetty5226** (0 likes, 1 year ago): It's killed their greed
- **@kashyap263** (0 likes, 1 year ago): Yeah..food delivery will fail for rapido
- **@SuppuNetha_Official** (0 likes, 1 year ago): Can you suggest to me that app
- **@kashyap263** (0 likes, 1 year ago): They all order through zomato Swiggy...main khud delivery karta hoon bhai...zomato has 58% Swiggy has 41 rest 1%
- **@Quantum_Thread** (0 likes, 1 year ago): Blame the government and their respective ministries
- **@code_name_uzi** (0 likes, 1 year ago): These apps are good for groups not for bachelors/students  /  / There is minimum order value which is too much and also portion sizes are also large but we cant save for lator because not fridge or reheat options in hostels and since paid so hefty already we just eat and gain weight 🥲
- **@kashyap263** (0 likes, 1 year ago): Not true..10rs aa jaata hai
- **@Vijay_8055_5** (0 likes, 1 year ago): ​ @kashyap263  Aapka city/zone mei jaldi kam ho jayega.