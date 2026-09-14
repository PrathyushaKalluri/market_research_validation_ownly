# Methodology — App-Store Review Collection (Agent B1)

**Access date:** 2026-09-14. **Script:** `collect_and_code.py` (Python 3 standard library only; no third-party packages or venv needed).
**Outputs:** `reviews_raw.csv`, `retrieval_log.csv`, `listing_stats.csv`, `reviews_coded.csv`, `reviews_validation_sample.csv`, `analysis_tables.md`, `analysis.md`, `codebook.md`.

## 1. Apps identified

| Store | App | ID | Verified by |
|---|---|---|---|
| Google Play | Ownly By Rapido: Food Delivery | `com.ownly.customer` | Page title on the fetched details page |
| Apple App Store (IN) | Ownly: Food Delivery App (seller: Ctrlx Technologies Private Limited) | `6747476494` | Product page |
| Google Play | Rapido: Bike-Taxi, Auto & Cabs | `com.rapido.passenger` | Page title. Only food/Ownly-related reviews are kept |
| Apple App Store (IN) | Rapido: Bike-Taxi, Auto & Cabs | `1198464606` | Product page. Only food/Ownly-related reviews are kept |

One exploratory call to the iTunes Search API (`itunes.apple.com/search`) was made to find the iOS IDs, before its robots.txt had been read. That path is **disallowed** by robots.txt (`Disallow: /search*`), so the script does not use it. The IDs were then confirmed on the allowed product pages.

## 2. Access rules applied (robots.txt read on 2026-09-14)

| Source | Endpoint | robots.txt status | Used? |
|---|---|---|---|
| Google Play | `/store/apps/details?id=…` (public details page) | Allowed | **Yes** |
| Google Play | `/_/PlayStoreUi/data/batchexecute` (the paginated review API that `google-play-scraper` relies on) | **Disallowed** (`Disallow: /_`) | **No** |
| Apple | `apps.apple.com/in/app/<slug>/id<ID>?see-all=reviews` | Allowed | **Yes** |
| Apple | `apps.apple.com /api/*`, `/v1/*`; `amp-api` (needs a bearer token) | Disallowed or token-gated | **No** |
| Apple | `itunes.apple.com/in/rss/customerreviews/…/json` (public RSS, up to ~500 recent reviews) | **Disallowed** (`Disallow: /*/rss/*`) | **No** — see §4 |

**Other safeguards:**
- No login, cookies, tokens, captcha handling or pagination APIs.
- 4-second delay between requests; 16 requests per run.
- Reviewer names, avatars and profile links are dropped at parse time and never written to disk.
- `review_id` is a salted-free SHA-1 prefix of the store's native review id. It is stable, but not a profile link.

**Variants requested to widen coverage without pagination:**
- Play: `hl` = en_IN, en, hi, te, kn, ta, all with `gl=IN`.
- iOS: platform = iphone, ipad.

Results were deduplicated on (store, native review id).

**Food filter (Rapido main app only):** a case-insensitive regex for ownly, food, restaurant, meal, biryani, dish, swiggy, zomato and similar terms.

## 3. What was retrieved (see `retrieval_log.csv`)

| Source | Reviews rendered per page | Unique kept |
|---|---|---|
| Ownly Play, en_IN | 20 | 20 |
| Ownly Play, en | 20 | 0 (duplicates) |
| Ownly Play, hi / te / kn / ta | 1 / 0 / 4 / 1 | 6 |
| Rapido Play, 6 language variants | 20 each | 1 (the only food-related review) |
| Ownly iOS, iphone / ipad | 20 page elements = 10 unique reviews | 10 |
| Rapido iOS, iphone / ipad | 20 each | 0 food-related |
| **Total** | | **37** |

**Listing-level context** (`listing_stats.csv`, a FACT as displayed by the store on 2026-09-14):

| Store | Rating | Ratings count | Installs |
|---|---|---|---|
| Ownly Play | 4.48★ | 44,485 | 1,000,000+ |
| Ownly iOS | 4.5★ | 10,466 | — |

## 4. Limitations and decisions the lead or team must take

1. **The sample is tiny (n = 37) and not a random sample of reviews.** Store pages render a "most relevant/helpful" selection. In this sample 70% are 1★, while the listing averages are 4.48★ and 4.5★. The rendered selection is therefore heavily skewed toward long negative reviews.
   - Theme percentages describe **this sample of visible reviews only**. They do not describe Ownly's customer base.
2. **The RSS decision is open.** Apple's customer-reviews RSS feed is a long-standing public Apple feed, but itunes.apple.com robots.txt disallows `/*/rss/*`. Following the brief's "do not circumvent robots restrictions" rule, it was **not used**.
   - One test request was made before robots.txt was checked. That response (50 reviews) was deleted unused.
   - If the team or instructor decide Apple's RSS feed is an intended public interface, it would add up to ~500 recent iOS reviews. That would be a documented change of policy, not a silent one.
3. **Google Play depth is limited** to what the public details page renders (~20 reviews). The paginated review API is robots-disallowed.
   - **Recommended manual supplement (compliant):** 1–2 team members open the Play Store app on a phone, sort Ownly reviews by *Most recent*, and hand-log 150–300 reviews into a copy of `reviews_raw.csv`.
   - Log fields: date, stars, text, no names; set `platform_source = google_play_manual`.
   - Then apply `codebook.md`. This is human reading, not scraping.
4. **No review names a city** (Bengaluru or Hyderabad). City-level transfer analysis (H9) is therefore not possible from this source.
   - Restaurant names that appear (e.g., India Sweet House, Nandhana Palace) are not used to infer location.
5. **The time trend around the Hyderabad launch cannot be estimated.** There are too few reviews per month, and the page selection is relevance-ranked, not chronological.
6. **Coding is an AI first pass** and needs human double-coding (`codebook.md` §5).
7. The script re-fetches live pages, so a re-run on a later date will return a different selection. `reviews_raw.csv` is the frozen 2026-09-14 snapshot used for analysis.

## 5. Re-running

```bash
python3 collect_and_code.py collect     # overwrites reviews_raw.csv, retrieval_log.csv, listing_stats.csv (iOS stats row was appended manually from the product page JSON: ratingValue 4.5, reviewCount 10466)
# (human/AI coding step -> reviews_coded.csv, using codebook.md)
python3 collect_and_code.py aggregate   # regenerates analysis_tables.md from reviews_coded.csv
```
