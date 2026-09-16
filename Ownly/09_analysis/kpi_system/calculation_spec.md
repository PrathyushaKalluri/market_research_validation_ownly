# Calculation Spec

**Version:** 1.0 · 2026-09-16. This spec is the contract between raw files and dashboard numbers. The dashboard
(`10_dashboard/decision_dashboard/ownly_decision_dashboard.html`) implements it in the browser; `09_analysis/` Python
may re-implement it. The two must agree.

## 1. Inputs

| Dataset | File | Grain | Load rule |
|---|---|---|---|
| Survey | Google Forms CSV export (`08_clean_data/raw/survey_v6_raw.csv`) | 1 row = 1 respondent | Headers matched by the phrases in §2; duplicate city-path columns are coalesced (first non-empty) |
| Audit | `audit_captures` CSV (audit-lite columns) | 1 row = 1 platform × restaurant × basket × slot | `platform` lowercased: `ownly` / `swiggy` / `zomato` / `toing` |
| Frame | `restaurant_frame` CSV | 1 row = 1 restaurant | `on_*` = yes/y/1/true → true |
| Fake door | Collector sheet export (`received_at … payload_json`) | 1 row = 1 event | Exclude `is_qa = true` and `is_bot_suspect = true` |

**Never edit raw files.** Cleaning happens in code.

## 2. Survey field matching (lower-cased, curly quotes normalised)

| Field | Header contains | Coding |
|---|---|---|
| city | `which city do you live` | Hyderabad / Bengaluru / Other |
| age | `how old are you` | eligible = starts with "2" (20–22, 23–25, 26–28, 29–30) |
| area | `which area?` | raw |
| occ | `best describes you` | Student (UG or PG) / Working / Both / Other |
| member | `memberships do you have right now` | member if it includes Swiggy One, Zomato Gold or Another; none if it starts with None; else unsure |
| rapido (A1) | `how often did you use rapido` | 0 Never, 1 1–3 times, 2 weekly, 3 several times a week; user = ≥1 |
| ordered | `order food online for delivery at least once` | Yes → true |
| cS, cZ, cO, cX | `swiggy: how many` · `zomato: how many` · `ownly (rapido` · `any other way` | number, blank → 0 |
| amount | `total amount you paid` | number |
| fair | `did it feel fair for what you got` | raw option |
| t1, t2, t3 | `same restaurant, same food. which` · `same restaurant, same food, same delivery time` · `same food price level` | 1 if the answer contains "230", else 0 |
| thresh | `make a different app your main one` | raw; ₹ value for numeric options (₹100 or more → 100) |
| tryP, tryQ | `if service p were available` · `and if service q were available` | 1–5 |
| choice | `if only one of them existed` | P / Q / N |
| keep | `once that offer ended` | 1–5 |
| status | `before today, which of these is true` | unaware / heard / opened / ordered (Other city: "I'd heard of it" → heard) |
| trigger, heard, whyNot, stopped | `would most make you try` · `first hear about ownly` · `reason you haven't opened` · `stopped you from ordering` | raw |
| first | `first ownly order` (not `use a discount`) | recent if it starts "In the last 4 weeks", else earlier |
| offer (A2) | `first ownly order use a discount` | yes (either Yes option) / no / unknown |
| prior | `4 weeks before the last 4 weeks` | number, blank → 0 for users |
| cf, disap, change, less | `if ownly didn't exist` · `no longer use ownly` · `one change would make you order more` · `less than you used to` | raw |
| fail (A3) | `has any of these happened` | any = ticked anything except "None of these"; blank → null |

**Ordering of matches:** check the `offer` phrase before `first`, because both headers contain "FIRST Ownly order".

## 3. Derived respondent flags

```
aware       = status in {heard, opened, ordered}
trier       = status == ordered
own8        = cO + prior                       # Ownly orders in the last 8 weeks
repeater    = trier AND own8 >= 2
nsm_member  = eligible AND ordered AND cO >= 1 AND own8 >= 2
frequent    = (cS + cZ + cO + cX) >= 6
price_first = (t1 + t2 + t3) >= 2
basket_high = amount >= median(amount within city)
```

## 4. Audit derivations

```
fees        = packaging_fee + platform_fee + delivery_fee + small_cart_fee + surge_rain_fee   (blank → 0)
eta_mid     = (eta_min_shown + eta_max_shown) / 2
matched set = slot + restaurant_name + basket_id where ownly AND ≥1 of swiggy/zomato have final_payable
comparator  = the incumbent with the lower final_payable in the set
saving_rs   = comparator.final_payable − ownly.final_payable
saving_pct  = saving_rs / comparator.final_payable
win         = saving_rs > 5 ; tie = |saving_rs| ≤ 5 ; loss = saving_rs < −5
eta_gap     = ownly.eta_mid − comparator.eta_mid
fee_load    = fees / final_payable
coverage    = frame on_ownly true / frame rows
overlap     = captures (restaurant_listed & restaurant_open on ownly) / captures listed & open on ≥1 incumbent (same set)
```

## 5. Fake-door derivations

```
visitor     = unique anon_visitor_id with page_view (per variant_id; a visitor's first variant is sticky)
cta         = visitor has any cta_click
secondary   = visitor has any secondary_intent
conv_arm    = cta visitors / visitors
lift_pp     = conv_B − conv_A ; lift_rel = conv_B / conv_A − 1
SRM check   = binomial test of visitors A vs B against 50/50; flag if p < 0.01
primary?    = total visitors ≥ 80 AND each arm ≥ 30   (D3)
```

## 6. Statistics

| Situation | Method | Output |
|---|---|---|
| Single proportion | Wilson score 95% | p, [lo, hi], k/n |
| Proportion vs 50% | Exact two-sided binomial | p-value |
| Two independent proportions | Fisher exact if any expected cell < 5, else two-proportion z; Newcombe (hybrid Wilson) CI on the difference | pp difference, CI, p, **relative lift** |
| Paired binary | McNemar exact (binomial on discordant pairs) | p |
| Medians (₹, %, minutes) | Bootstrap: 10,000 resamples, seed 20260914, **resampling restaurants** for the audit | median, percentile CI |
| Ratio of sums (share of requirements) | Bootstrap over respondents | ratio, CI |
| Categorical × categorical | Chi-square (Fisher if sparse), Cramér's V | V, p |

**Minimum bases:** n < 10 → hide the value and show "n < 10". n < 30 → show it with a "low base" flag and don't apply a
verdict. Audit n is always shown as k/n.

**Multiplicity:** only K13/K14 is confirmatory (H₀). Everything else is descriptive or exploratory; no p-value is reported
without an effect size.

**No statistical theatre:** no logistic regression unless ≥ 10 events per predictor; no composite attractiveness score.

## 7. Reproducibility
- The dashboard shows the file name and load time; demo data is visibly labelled on every page.
- Constants: bootstrap seed 20260914; tie ₹5; practical floors of 10pp and ₹10 (charter); D3 fake-door thresholds 80 and 30.
