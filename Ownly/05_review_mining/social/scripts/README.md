# Reproducing the social dataset (Agent B2, 2026-09-14)

Python 3 standard library only. Run from this folder.

1. **Collect Reddit** (public RSS, no login; ~12 s spacing, 429 back-off): `mkdir -p rss && python3 rss_v2.py` then `python3 rss_followup.py`.
   `rss_v2.py` expects `rss/search_results.json` from the first exploratory run; if absent, create it as `{"threads": {}}`.
   Results will differ from 2026-09-14 because Reddit content and search ranking change. The original raw RSS cache is **not** kept in the project because it contains Reddit usernames.
2. **LinkedIn / X / forum items** were captured manually from logged-out public pages → `manual_items.json` (URLs + excerpts + `verbatim_status`).
3. **Coding (AI first pass):** `codes_reddit*.py` merge hand-coded rows into `codes.json` (LinkedIn/X/forum codes are already in `codes.json`). Order: `codes_reddit.py`, then `_b2` … `_b12`, then `_fu`.
4. **Build:** `python3 build_social.py` → writes `../social_raw.csv`, `../social_coded.csv`, `../search_log.csv`. It decodes LinkedIn/X post dates from their IDs and redacts phone numbers, personal emails, Reddit usernames and named private individuals.
5. Before using any row: human validation per `../codebook_social.md` §6.

Note: `build_social.py` reads inputs relative to its own folder (`SCR`) and writes to the absolute project path in `OUT` — edit `OUT` if the project folder moves.
