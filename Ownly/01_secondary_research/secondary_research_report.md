# Secondary Market & Competitive Research — Ownly Hyderabad (Gachibowli) Market-Transfer Study

**Workstream:** Agent A — Secondary Market & Competitive Research
**Access date for all sources:** 2026-09-14
**Companion files:** `evidence_table.csv` (68 rows, every claim with URL, dates, exact wording, verification status), `market_price_anchors.md` (fee/price/ETA anchors for survey and choice-experiment design)
**Supersedes where stated:** root files `16_ownly_secondary_research_findings.md` and `17_ownly_hyderabad_restaurant_onboarding_targets.md` (dated 2026-09-03). See Section 13 for explicit corrections.

---

## 0. How to read this report

**Evidence labels (used on every claim):**

| Label | Meaning in this report |
|---|---|
| **FACT** | Verified by ≥2 genuinely independent sources, a primary document, or a stable reference work |
| **COMPANY CLAIM** | Published by Ownly/Rapido/Swiggy/Zomato themselves, or a company statement relayed by media |
| **MEDIA REPORT** | Journalist reporting, often based on unnamed sources or a single upstream report |
| **CONSUMER-GENERATED** | Individual user posts, bills, reviews |
| **HYPOTHESIS** | A testable proposition for primary research |
| **INTERPRETATION** | Our reading of evidence; not stated by any source |
| **ASSUMPTION** | Something we take as given for design purposes, flagged for checking |
| **UNKNOWN** | Searched for, not found |

`[E##]` = row in `evidence_table.csv`.

**Method limits you should know about.**
- Several major outlets (Business Standard, Deccan Herald, MediaNama) returned HTTP 403 to automated fetching. For those rows the exact wording comes from the search-engine index, and they are marked `unverified` or `partially`. A human should open those links before the claim goes on a slide.
- Google Play would not render. The Apple App Store listing did.
- Syndicated stories were traced back to their source where possible. **Several stories that look like independent confirmations are really one report copied many times** (Section 13).
- Review mining, Reddit and LinkedIn belong to Agent B. We only used consumer-generated items here when they came through media or showed up on a store listing.

---

## 1. Headline findings (read first)

1. **Hyderabad status is now a COMPANY CLAIM, but the launch date is UNKNOWN.** Ownly's own site says *"Ownly is now in Hyderabad"* [E22]. A 2026-07-23 report expected launches in the five cities "over the next two to three weeks" [E10], which suggests mid-to-late August 2026. **We found no independent, dated media report of the Hyderabad launch in 12+ searches.** The Hyderabad page names no localities, and **Gachibowli is not mentioned** [E22]. The team has to check in the app whether Gachibowli addresses can be served.
2. **The Hyderabad proposition is narrower than "no fees."** The page promises no platform fees, no packaging fees and no surge charges [E23]. **It says nothing about a delivery fee.** Bengaluru reporting says ~₹30 + GST [E13], but the App Store description says "Free delivery" [E28]. A launch-week Bengaluru bill showed no delivery fee at all [E29], and a vendor blog calls the fee "distance-based" [E31]. **The real delivery fee in Gachibowli is UNKNOWN and is the most important thing for the competitor audit to record.**
3. **The Bengaluru traction numbers are weaker than the 16_ file suggested.** "50,000 orders/day, ~10% share" [E19] comes from **one upstream Moneycontrol report** that other outlets copied. It is not independently verified. Ownly's own site gives different figures: 22,000 restaurants and 42 lakh orders [E24]. Other reports say 20,000 [E18] or 25,000 restaurants. Classify these as MEDIA REPORT and COMPANY CLAIM, not FACT.
4. **The incumbent fee stack is real and documented, but the numbers are national.** Platform fee is ₹17.58 incl. GST on both Swiggy and Zomato since March 2026 [E33–E35]. Delivery charges carry 18% GST since 2025-09-22 [E36]. Subscribers now pay rain surcharges [E38]. One Bengaluru bill added **₹72 of non-food charges to a ₹119 item** on Zomato [E29]. **We found no Hyderabad-specific fee figures.**
5. **Ownly is not the only "affordable" challenger.** Swiggy's budget app **Toing** reportedly has 33M weekly active users [E45]. It targets "students and young professionals living alone," which is exactly this study's segment [E46]. No source lists Hyderabad as a Toing city (UNKNOWN). **Flipkart** is piloting food delivery in Bengaluru [E50–E51]. **INTERPRETATION:** the claim "the only low-price option" may already be out of date in some cities.
6. **Part of the Bengaluru tailwind may not transfer.** Ownly's Bengaluru rise overlapped with open restaurant revolt against incumbents: boycott threats, commission-cap demands, an NRAI case at the CCI [E48–E49]. Inc42 explicitly tied that pushback to Ownly's opening [E16]. **We found no equivalent 2026 restaurant protest in Hyderabad.** (HYPOTHESIS for H9: supply-side goodwill may be weaker in Hyderabad.)
7. **Hyderabad context is biryani-heavy and has less rain than Bengaluru.** Swiggy reports 1.75 crore biryani orders in Hyderabad in 2025 [E57]. Five of the twelve dishes on Ownly's Hyderabad price page are biryanis [E26]. Average annual rainfall is 859.6 mm in Hyderabad versus 1,077.8 mm in Bengaluru [E60–E61]. **INTERPRETATION:** whether Ownly carries biryani anchor restaurants may matter more for assortment (H10) than in Bengaluru. Rain-surge pain may be less salient (H1/H3 HYPOTHESIS).

---

## 2. Ownly timeline

| Date | Event | Label | Evidence |
|---|---|---|---|
| 2025-06 | Pre-launch reporting of a restaurant fee model (₹25 for orders ≤₹400, ₹50 above) and an analyst expectation of 8–15% commission | MEDIA REPORT (superseded) | [E07], [E08] |
| 2025-08-13 | Pilot in BTM Layout, HSR Layout and Koramangala (Bengaluru), run through subsidiary Ctrlx Technologies | MEDIA REPORT → FACT (consistent across many reports) | [E01], [E02] |
| 2025-11 | Magicpin partnership reported (from 16_; not re-verified in this pass) | MEDIA REPORT | 16_ file |
| 2026-03-03 | Citywide Bengaluru launch as standalone app ("mid-March" in one report) | FACT | [E09] |
| 2026-03-26 | ~5,000 orders/day; ~20,000 restaurants | MEDIA REPORT | [E12] |
| 2026-05-15 | Rapido raises $240M at $3B valuation (Prosus-led) | MEDIA REPORT (TechCrunch) | [E54] |
| 2026-07 | ~40,000 orders/day, ~7% share (Bengaluru) | MEDIA REPORT (single upstream) | [E19] |
| 2026-07-23 | Report: 5-city rollout (incl. Hyderabad) to follow "over the next two to three weeks" | MEDIA REPORT (unnamed sources) | [E10] |
| 2026-07-28 | Ownly integrated into the main Rapido app | MEDIA REPORT | [E18] |
| 2026-07-30 | NRAI MoU signed; "nearly 10%" share claimed | MEDIA REPORT / COMPANY CLAIM | [E16], [E17] |
| 2026-08-21 | 50,000+ orders/day, ~10% share of Bengaluru | MEDIA REPORT (single upstream) | [E19] |
| **Unknown (by 2026-09-14)** | **"Ownly is now in Hyderabad"** | **COMPANY CLAIM, undated** | [E22] |

---

## 3. Ownly evidence table (rows requested in the brief)

| Item | What the evidence says | Label | Verification | Evidence |
|---|---|---|---|---|
| Launch history | Subsidiary Ctrlx Technologies; pilot Aug 2025; standalone app; later folded into Rapido app | MEDIA REPORT | Verified | E01, E02, E18 |
| Bengaluru pilot | BTM, HSR, Koramangala from mid-Aug 2025 | FACT | Verified | E01 |
| Full Bengaluru expansion | Citywide 2026-03-03 | FACT | Verified | E09 |
| Hyderabad availability/expansion | Company site: "Ownly is now in Hyderabad." Expected per July report. **No independent dated launch report; no localities listed; Gachibowli serviceability UNKNOWN** | COMPANY CLAIM | Unverified | E10, E11, E22 |
| Restaurant model | Zero commission; Rs 0 listing/subscription/marketing (one vendor-blog source for the full list) | MEDIA REPORT | Zero commission verified; "no subscription" partially | E16, E18, E31 |
| Commission structure | 0% for restaurants. Pilot-era "fixed fee per order" and pre-launch proposals appear superseded | MEDIA REPORT | Partially | E04, E06–E08 |
| Customer pricing proposition | Hyderabad: no platform, packaging or surge fees; "no inflated prices." Bengaluru: menu ≈ offline price + delivery fee. "~15% cheaper" is a pilot-era claim with no method | COMPANY CLAIM | Unverified | E03, E23, E28, E32 |
| Delivery fee | ~₹30 + GST (Bengaluru reports) vs "Free delivery" (App Store) vs no fee on one launch-week bill vs "distance-based" (blog). **Hyderabad fee not published** | CONTRADICTED | Contradicted | E13, E28, E29, E31 |
| Delivery model | Rapido's captain network; one report says a specialised fleet at first, with captains trained over time | MEDIA REPORT | Partially | E05, E16 |
| Rapido integration | Inside the main Rapido app from 2026-07-28 | MEDIA REPORT | Verified | E18 |
| Restaurant coverage | 20,000 (BT, Jul-2026), 22,000 (Ownly site), 25,000 (other media) — Bengaluru. **Hyderabad count UNKNOWN**; 8 Hyderabad brands named on the site | COMPANY CLAIM / MEDIA | Conflicting | E18, E24, E25 |
| Order claims | 5k/day (Mar) → 40k (Jul) → 50k (Aug), Bengaluru; site says "42 lakh and counting" | MEDIA REPORT / COMPANY CLAIM | Single upstream | E12, E19, E24 |
| Customer claims | "₹34 crore and counting" saved; "4.4 rating"; App Store 4.5 (~10K ratings) | COMPANY CLAIM | Unverified | E24, E28 |
| Competitor differences | Incumbents: platform fee ₹17.58, packaging fees, variable delivery fees, commissions 8–35% by various sources. Toing: budget menu, claims no platform/delivery/surge fee. Flipkart: 10–13% commission, Bengaluru pilot | MEDIA REPORT | Mixed | E33, E45–E51 |

---

## 4. Ownly value proposition and business model

**What is well supported**
- **Zero commission to restaurants.** FACT-level consistency across Business Today, Inc42 and others [E16, E18].
- **Ownly earns mainly from the customer delivery fee, not from restaurants.** MEDIA REPORT [E13, E19]. **INTERPRETATION:** revenue per order depends on the delivery fee. That is why "free delivery" claims and the true fee level matter so much for sustainability.

**What is contested**
- **The delivery fee.** It is described as "flat ~₹30 + GST" [E13], but also as "Free delivery" [E28], as absent on one bill [E29], and as "distance-based" [E31]. HYPOTHESIS: the fee varies by distance, promotion or time period. It has to be observed in the audit.
- **"No markup / offline prices."** This is a COMPANY CLAIM. The only independent-ish check is a single Bengaluru pizza order [E29–E30]. Ownly's Hyderabad page shows 12 dishes that are 7–41% cheaper than "other apps" [E26], but with no date, outlet or fee basis. **Treat these as a list of items to audit.**
- **ETA.** One consumer-review summary mentions a "25-minute ETA" promise and complaints about longer waits [E65]. We found no official ETA commitment. UNKNOWN.

**Pilot-era fee proposals** [E06–E08] (restaurant-paid delivery, ₹25/₹50 per order, 8–15% commission) should **not** be described as Ownly's current model.

---

## 5. Rapido ecosystem advantage

| Asset | Evidence | Label | Transfer to Hyderabad? |
|---|---|---|---|
| App distribution | Ownly inside the Rapido app since 2026-07-28 [E18]; Rapido ~74M monthly users (Jan–Feb 2026, national) [E15] | MEDIA REPORT | **Likely transferable.** City-level Rapido user base in Hyderabad is UNKNOWN |
| Rider network in Hyderabad | "5.4 lakh active captains", "9.1 lakh daily rides" [E55] | COMPANY CLAIM (low-tier outlet) | **Presence yes; spare food-delivery capacity UNKNOWN** |
| Capital | $240M at $3B (May 2026) [E54] | MEDIA REPORT (TechCrunch) | Transferable |
| Demand data from past Swiggy deliveries | [E05] | MEDIA REPORT | Unclear |
| Restaurant relationships | NRAI MoU (national) [E17]; Magicpin partnership (16_/17_) | MEDIA REPORT | **Partially.** Hyderabad onboarding depth UNKNOWN |
| Entity registered in Telangana | CIN `U47912TS2025PTC198828`, 500081 address [E27] | COMPANY-published identifier; INTERPRETATION of the "TS" code | Does not prove operations — confirm on MCA |

**H7 brand-effect caution (INTERPRETATION):** secondary data cannot tell us whether "by Rapido" raises or lowers trust in food delivery. We found no source on consumer perception of Rapido as a food brand. **UNKNOWN. Needs the brand-blind/brand-reveal survey test.**

**Scale figures conflict** [E66]: 400+ vs 500+ vs 600 cities; 1M vs 9M captains. Don't use a single Rapido scale number without noting the conflict.

---

## 6. Indian food-delivery market and incumbents

| Metric | Value | Label | Evidence |
|---|---|---|---|
| Duopoly share | Eternal (Zomato) ">58%" food-delivery GOV share, Q1FY27 | MEDIA REPORT | E43 |
| Zomato FD NOV Q1FY27 | ₹10,769 cr, +20% YoY; adj. EBITDA 5.6% | MEDIA REPORT (from filings) | E42, E67 |
| Swiggy FD GOV Q1FY27 | ₹9,490 cr, +17.4% YoY; adj. EBITDA 3.1%; 19.2M MTU | MEDIA REPORT | E42, E44 |
| National daily orders | Zomato 2.5M+, Swiggy 2–2.2M | MEDIA REPORT | E20 |
| Bengaluru daily orders | 500k–600k (estimate) | MEDIA REPORT | E19 |
| **Hyderabad daily orders / share / TAM** | **UNKNOWN** | — | — |
| **Platform AOV (national or city)** | **UNKNOWN** (not in any fetched source) | — | — |

**Current customer fee stack on incumbents (national unless stated)**

| Fee | Current evidence | Label | Evidence |
|---|---|---|---|
| Platform fee | ₹17.58 incl. GST (Swiggy); ₹14.90 + GST = ₹17.58 (Zomato), March 2026. Swiggy's 4th hike in 7 months | MEDIA REPORT (verified) | E33–E35 |
| Delivery fee | "₹25–60" without membership (blog, low confidence); ₹19 "delivery partner fee" on one Bengaluru Zomato bill | MEDIA / CONSUMER | E41, E29 |
| GST on delivery | 18% since 2025-09-22 | FACT-level | E36 |
| Packaging | ₹25 on one Bengaluru Zomato bill; restaurant-set | CONSUMER-GENERATED | E29 |
| Rain surcharge | Subscribers lost exemption (May 2025); amount "₹15–35" **unverified** | MEDIA REPORT | E38, E39 |
| Small-cart / long-distance fee | **UNKNOWN** (not found as documented line items) | — | — |
| Donation add-on | ₹3 Feeding India (Zomato bill) | CONSUMER-GENERATED | E29 |
| Swiggy One / Zomato Gold | ₹99/month, free delivery above ₹199 within 7 km — **2024 source, stale**; 2026 blog prices conflict | MEDIA REPORT (stale) | E40 |

---

## 7. Challengers and substitutes

| Player | Proposition | Scale / status | Hyderabad? | Evidence |
|---|---|---|---|---|
| **Swiggy Toing** | Budget meals, items from ₹49; claims no platform/delivery/surge fee (another report says ₹12 platform fee); separate app with Swiggy login | 33M weekly active users (CLSA), "nearly 50 cities" | **UNKNOWN** (not in any listed city set) | E45–E47 |
| **Flipkart (Minutes / "Eat In")** | Lower commissions for restaurants: 10% or 12–13% (sources disagree); ONDC | Bengaluru pilot, Aug–Sep 2026 | No timeline found | E50, E51 |
| **Magicpin / ONDC** | Discovery + delivery via ONDC | 150k orders/day (Sept 2024, stale); FY24 revenue ₹879.6 cr, loss ₹107.3 cr | Hyderabad merchant network claimed in 17_ (not re-verified) | E52, E53 |
| **Zomato budget formats** | "Everyday" home-style meals (2023–; reported wind-down) | Unclear in 2026 | UNKNOWN | search only; not tabled |
| **Swiggy Bolt** | ~10-minute food delivery | Hyderabad had "second-highest" Bolt orders (2025) | Yes | E58 |

**INTERPRETATION for H2/H5/H9:** "Cheaper than Swiggy/Zomato" is no longer a unique claim nationally. Swiggy may answer Ownly with Toing in any city it chooses. In the Hyderabad audit, add Toing (if it's available in Gachibowli) as a comparison platform.

---

## 8. Incumbent responses to Ownly and restaurant-side economics

- **Commission levels** vary by source: "8–28%" (Bengaluru association) [E48]; "25–35%" (Inc42) [E16]; "16–30%" (Business Standard) [E51]; "30–40% per order once you stack commission, advertising and other charges" (Inc42) [E50]. The spread reflects different definitions (base commission vs effective take rate). **Cite as a range, with its definition.**
- **Restaurant payout example:** a ₹400 dish with packaging nets about ₹220 to the restaurant [E48] (association figure, an interested party). **INTERPRETATION:** this is the mechanism behind the "menu-price inflation" hypothesis (H1). Restaurants may raise app menu prices to protect margin, but no source here measures the actual online-vs-offline markup in Hyderabad. **UNKNOWN until audited.**
- **Incumbent response:** 16_ reported incumbents offering "better commercial terms" (Aug 2026, unquantified). In this pass we found CEO-level talks with Bengaluru restaurant associations, a boycott deferred to Aug 31 [E49], and a Zomato assurance that concerns would be addressed "by September." Outcome UNKNOWN.
- **Consumer-side response:** Toing's scale-up [E45] is the most material competitive move found. Whether it was a response to Ownly is **not stated by any source**, so we don't claim it.

---

## 9. Independent evidence on Ownly pricing vs incumbents

| Evidence | Finding | Limits | Evidence |
|---|---|---|---|
| Viral Bengaluru user bill (Mar 2026) | ₹119 pizza: Ownly ~₹125; Swiggy ~₹180 (after ₹50 discount); Zomato ₹191.37 | n=1, launch week, possible promo, OTP failure reported | E29, E30 |
| Ownly Hyderabad page | 12 dishes, Ownly 7–41% below "other apps" | Company claim; no date, outlet or fee basis | E26 |
| "~15% lower" | Pilot-era positioning | No method | E03 |
| Price-comparison tools (e.g., BuyHatke Food Compare) | Exist for Swiggy/Zomato/Ownly | Not analysed; usable as an audit aid only | search only |

**No journalist-run, multi-restaurant, multi-time basket comparison was found, and none exists for Hyderabad.** That gap is exactly why the team's competitor basket audit (06_competitor_audit) is essential.

---

## 10. Competitor comparison matrix (customer-facing, as of 2026-09-14)

| Dimension | Ownly (Hyderabad) | Swiggy | Zomato | Toing | Flipkart food |
|---|---|---|---|---|---|
| Platform fee | None claimed [E23] | ₹17.58 incl. GST [E33] | ₹14.90 + GST [E33] | Claimed none / ₹12 reported (conflict) [E46–E47] | UNKNOWN |
| Packaging fee | None claimed [E23] | Restaurant-set (UNKNOWN typical) | ₹25 on one bill [E29] | UNKNOWN | UNKNOWN |
| Delivery fee | **UNKNOWN in Hyderabad**; ~₹30+GST reported in Bengaluru; "Free delivery" on App Store [E13, E28] | Variable; ₹25–60 (low-conf.) [E41] | Variable; ₹19 on one bill [E29] | Claimed none [E46] | UNKNOWN |
| Surge / rain | None claimed [E23] | Yes, incl. subscribers [E38] | Yes, incl. subscribers [E38] | Claimed none [E46] | UNKNOWN |
| Menu prices | Claimed near-offline [E28] | Commission-influenced (INTERPRETATION) | Same | Budget-curated | UNKNOWN |
| Subscription | None found | Swiggy One (price must be re-captured) [E40] | Gold (price must be re-captured) [E40] | None found | UNKNOWN |
| Restaurant commission | 0% [E18] | 8–35% by source [E16, E48] | Same | UNKNOWN | 10–13% [E50–E51] |
| Fast-delivery tier | None found | Bolt (~10 min) [E58] | UNKNOWN in 2026 | UNKNOWN | Minutes fleet [E50] |
| Gachibowli coverage | **UNKNOWN** | Yes (listing pages exist) | Yes (listing pages exist) | **UNKNOWN** | No |

---

## 11. Bengaluru vs Hyderabad / Gachibowli context

| Dimension | Bengaluru | Hyderabad / Gachibowli | Label | Transfer implication |
|---|---|---|---|---|
| City population (Census 2011) | 8,443,675 [E61] | 6,809,970 [E60]; Gachibowli 149,264 (2020) [E59] | FACT (dated) | Scale is comparable; Gachibowli is a micro-market |
| Ownly traction | 50k/day, ~10% (media) [E19] | Company says live; **no metrics** [E22] | MEDIA / COMPANY | Nothing to compare yet. Hyderabad evidence must come from primary research |
| Ownly localities | Pilot areas documented [E01] | **Not published**; Gachibowli not mentioned [E22] | UNKNOWN | Check serviceability in-app first |
| Restaurant–platform climate | Open revolt: boycott threats, 22% cap demand, NRAI CCI case [E48–E49] | **No 2026 protest found** | MEDIA REPORT / UNKNOWN | HYPOTHESIS: weaker supply-side tailwind (H9) |
| Restaurant listing gap | >1 lakh FSSAI vs <30k on big platforms (unverified) [E14] | UNKNOWN | — | Don't assume the same "invisible restaurants" pool |
| Signature food | UNKNOWN (not collected) | 1.75 cr biryani orders on Swiggy, 2025; >18% of India's [E57–E58] | COMPANY CLAIM (Swiggy) | Biryani anchors (Paradise, Bawarchi) matter for assortment (H10) |
| Fast-delivery habit | UNKNOWN | 2nd-highest Swiggy Bolt orders (2025) [E58] | COMPANY CLAIM | HYPOTHESIS: higher ETA expectations weaken a slower/cheaper trade-off (H3) |
| Rainfall | 1,077.8 mm/yr; wettest Sept [E61] | 859.6 mm/yr; monsoon Jun–Oct [E60] | FACT | HYPOTHESIS: rain-surge pain less frequent in Hyderabad (H1) |
| IT workforce | Not collected | ~9.46 lakh (Telangana, FY2024) [E62] | MEDIA REPORT | Gachibowli = Financial District / IT hub [E59] |
| Students near target area | Not collected | University of Hyderabad, IIIT-H, MANUU, TISS off-campus [E59]; ISB not in fetched text | FACT (Wikipedia) | Student segment is physically dense near Gachibowli |
| Rapido rider base | UNKNOWN (city-level) | 5.4 lakh captains (company claim) [E55] | COMPANY CLAIM | Presence ≠ food capacity |
| Budget competitor (Toing) | Not in listed cities | Not in listed cities | UNKNOWN | Audit whether available |
| Flipkart food | Pilot [E50] | None | MEDIA REPORT | Less crowded in Hyderabad for now |
| Price levels / rents / cost of living | Not reliably sourced | 16_'s "30–40% lower rent" still unsourced | UNKNOWN | Don't use |

---

## 12. Starbucks Australia — analytical analogy only

**Sourced lesson.** Starbucks closed about three-quarters of its Australian stores in mid-2008. A peer-reviewed case analysis says the chain **"overestimated points of differentiation and perceived value of supplementary services," "expanded too quickly and forced themselves upon an unwilling public,"** entered late into a competitive market with an established local coffee culture, let service standards slip, and had an unsustainable business model (Patterson, Scott & Uncles, 2010, *Australasian Marketing Journal* 18(1):41–47) [E63]. Widely repeated figures: 61 of 87 stores closed, ~$105M in losses over the first seven years [E64] (MEDIA REPORT, not checked against filings).

**General lesson (INTERPRETATION):** a proposition that works in one market doesn't carry over automatically. Local jobs-to-be-done, habits, competitive alternatives and willingness to pay all have to be validated.

**Where the analogy is useful for Ownly, and where it isn't (INTERPRETATION):**
- *Useful:* the risk of **overestimating the differentiator**. For Ownly that is "no platform/packaging fees" in a market where incumbents discount heavily and Toing-style budget options exist. There is also the risk of **scaling before the local job is confirmed**, e.g., Hyderabad's biryani-anchor and fast-delivery expectations.
- *Not a match:* Ownly is not importing a foreign culture. It is entering a habit (app food delivery) that already exists, with a price or structure difference. Don't claim "Ownly = Starbucks."

---

## 13. Corrections to root files 16_ and 17_ (dated 2026-09-03)

| # | Earlier claim | Correction | Evidence |
|---|---|---|---|
| C1 | Hyderabad is a "next quarter" target, not live | **Stale.** Ownly's site now says "Ownly is now in Hyderabad." The launch date is still UNKNOWN and not independently reported. Frame the study as early market-fit validation | E10, E22 |
| C2 | 50,000/day and 10% share "verified — consistent across 2 independent sources" | **Downgrade.** Both trace to one Moneycontrol report. Classify as MEDIA REPORT (single upstream), not verified | E19, E21 |
| C3 | "₹30 + GST flat delivery fee — Verified across 3 independent sources" | **Downgrade to contested.** App Store says "Free delivery," one bill showed no delivery fee, a blog says "distance-based," and the Hyderabad page states no delivery fee | E13, E28, E29, E31 |
| C4 | Restaurant count 20k vs 25k | Add the **company's own figure of 22,000** (site). Still unresolved; cite as a range with sources | E18, E24 |
| C5 | Rapido "$2.3 billion valuation," "6M+ daily rides, 500+ cities, 1M+ captains" | Valuation now **$3B (May 2026)**. Scale figures conflict across sources; flag rather than cite one | E54, E66 |
| C6 | "~15% below competitor platforms" | Traced to **pilot-era (Aug 2025) positioning**. Not a measured Bengaluru or Hyderabad saving | E03 |
| C7 | 17_: Paradise and Bawarchi as anchor *candidates* | Ownly's Hyderabad page **already names Paradise Biryani and Bawarchi** (plus Vivaha Bhojanambu, Harley's, 100N, Punjabi Affair, Bakelore, Cream Stone). Shah Ghouse and Cafe Bahar are not shown on the page — absence from a marketing page ≠ absence from the app | E25 |
| C8 | 16_ competitor section lists Flipkart as the main new challenger | Add **Swiggy Toing** (33M WAU, budget positioning aimed at students and young professionals) as the most material affordability competitor | E45, E46 |
| C9 | 16_ says Swiggy/Zomato offered "better commercial terms" | Still unquantified. New context: boycott deferral, CEO talks, 22% cap demand. Outcome UNKNOWN | E48, E49 |
| C10 | 17_: Magicpin 70,500-merchant Hyderabad network; NRAI 250-member Hyderabad chapter | **Not re-verified in this pass.** Keep as MEDIA REPORT until reopened | — |
| C11 | Implicit: Rapido is Bengaluru-only as an Ownly entity | The Ownly entity (CTRLX) shows a **Telangana CIN and a Hyderabad 500081 address**. Confirm on MCA; it does not prove operations | E27 |

---

## 14. UNKNOWN / evidence gaps (and how to close them)

| Gap | Why it matters | How to close |
|---|---|---|
| Hyderabad launch date and launch localities | "Early market fit" framing; Gachibowli serviceability | In-app check at 3–5 Gachibowli addresses; ask Ownly/Rapido PR; look for dated social posts (Agent B) |
| Ownly's actual delivery fee in Gachibowli (and whether it varies by distance, time or promo) | Core of H2/H8; the ₹-savings calculation | **Competitor audit**: screenshot the checkout at lunch, dinner and weekend |
| Ownly restaurant count and coverage in Gachibowli | H5/H10 assortment threshold | Audit: count serviceable restaurants from a fixed address per platform |
| Incumbent delivery, packaging, small-cart and long-distance fees in Hyderabad | H1 fee pain; choice-experiment levels | Audit (national figures here are placeholders) |
| Online vs verified offline menu prices in Hyderabad | H1 "menu inflation" | Audit with in-store menu photos/receipts only; never assume |
| ETAs (Ownly vs incumbents) in Gachibowli | H3 | Audit: record quoted ETA and actual delivery time on real orders if budget allows |
| AOV for 20–30-year-olds / by platform | Survey ranges, WTP anchors | Survey question on the last order's total; no secondary figure found |
| Hyderabad food-delivery TAM, daily orders, platform shares | Context only | Probably not public; don't estimate without flagged assumptions |
| Toing / Flipkart availability in Hyderabad | Competitive set | In-app check |
| Rapido brand perception as a food brand | H7 | Brand-blind → brand-reveal survey module |
| Ownly reliability/support performance | H4/H12 | Review mining (Agent B); Bengaluru survey |
| Current Swiggy One / Zomato Gold prices and terms | H1, H8 | Capture in-app on audit day |
| Whether the Bengaluru boycott ended or restaurants shifted to Ownly | H9 transfer of supply tailwind | Follow-up search after 2026-09 |
| ISB location/enrolment; student hostel/PG counts near Gachibowli | Sampling frame | Institutional websites |

---

## 15. Hand-offs to other workstreams

- **Competitor audit (06):** audit the 12 dishes on Ownly's Hyderabad page [E26] on Ownly, Swiggy, Zomato (and Toing if available). Use the itemised bill template from [E29] as the column schema: item, packaging, delivery, platform, donation, taxes, discount, total.
- **Survey design (Agent C):** Ownly's Hyderabad message is "no platform, packaging or surge fees," not "no fees." The brand-blind concept should describe the fee **structure** neutrally. Don't state a savings % (none is verified).
- **Review mining (Agent B):** ETA-promise complaints, "delivered but not received," refund delays [E28, E65]; look for any dated Hyderabad-launch posts.
- **Fake-door copy:** don't use "15% cheaper" or the company's dish comparisons as factual claims.
