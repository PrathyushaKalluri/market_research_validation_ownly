# B. Assumption Map

**Version:** 2026-09-14. Every assumption below is **unvalidated** until the linked test runs.

**How to read this map:**
- **Importance:** how badly the Gachibowli strategy fails if the assumption is false (H/M/L).
- **Current evidence:** what we know today, before primary research.
- **Quadrant:**
  - **TEST FIRST** = high importance + weak or no evidence
  - **MONITOR** = high importance + moderate evidence
  - **PARK** = low importance

## 1. The implicit "Bengaluru playbook" being transferred

> Young urban users pay noticeably more than menu price on incumbent apps → a zero-commission model lets restaurants list at near-menu prices with a flat delivery fee → total checkout is visibly lower → users try Ownly (helped by Rapido app distribution and brand familiarity) → the experience (ETA, reliability, selection, support) is "good enough" → users repeat → Ownly takes share.

Every arrow in that chain is an assumption. The map below breaks the chain into testable links.

## 2. Assumption register

| ID | Assumption | Source of assumption | Label | Importance | Current evidence (pre-fieldwork) | Quadrant | Test (hypothesis → instrument) | Kill / weaken criterion |
|---|---|---|---|---|---|---|---|---|
| AS1 | Gachibowli 20–30s experience frequent, salient pain from fees and total checkout price | Bengaluru narrative; media | HYPOTHESIS | H | Weak: media anecdotes, no Hyderabad data | TEST FIRST | H1.1–H1.4 → Hyderabad survey pain items; interviews | Fee-reconsider frequency CI entirely below 50% "sometimes+" |
| AS2 | Price/fee pain is a bigger switching lever than reliability or assortment pain | Ownly positioning | HYPOTHESIS | H | None | TEST FIRST | H1.2, H4.1, H5.1 → pain ranking, choice tasks | Reliability or assortment trade-off value > achievable savings |
| AS3 | Ownly's total checkout is actually lower than Swiggy/Zomato in Gachibowli for comparable baskets | Company claim ("~15% cheaper", single source) | COMPANY CLAIM | H | Unverified in Hyderabad | TEST FIRST | H2 → **competitor audit** | Ownly matched-pair median gap CI includes 0 or favours incumbents; win rate < 50% |
| AS4 | The savings are large enough, relative to what users need, to trigger switching | Team inference | ASSUMPTION | H | None | TEST FIRST | H2.3 → required savings (survey) vs observed savings (audit) | Median required savings > audit median savings for target segment |
| AS5 | Users value transparency (fewer line items) beyond the lower total | Ownly messaging | HYPOTHESIS | M | None | TEST FIRST | H2.2 → bill comparison at equal totals | Preference for simple bill ≈ 50% (CI includes 50%) |
| AS6 | Users tolerate somewhat longer ETA for savings | Bengaluru narrative | HYPOTHESIS | H | None | TEST FIRST | H3 → choice tasks, ETA expectations | Implied value of 10 min > ₹30 for majority segment |
| AS7 | Ownly's reliability (lateness, cancellations) is comparable to incumbents | Company positioning | UNKNOWN | H | Unknown; reviews may signal (Agent B) | TEST FIRST | H4, H12 → reviews, Hyderabad Ownly users, optional test orders | Reliability is top severity theme and top churn reason |
| AS8 | Users won't give up reliability for price | Behavioural-science prior | HYPOTHESIS | H | None | TEST FIRST | H4.1 → price-vs-reliability tasks (RSS) | Opposite of AS7 risk: if RSS is low, reliability is less of a guardrail |
| AS9 | Ownly's Gachibowli restaurant coverage is sufficient for the restaurants users actually order from | Zero-commission onboarding thesis; channel partners (v1 file 17) | ASSUMPTION | H | Unknown for Hyderabad | TEST FIRST | H10 → audit coverage + ADI + "couldn't find restaurant" | Coverage of frame < ADI-implied need among ≥40% of users |
| AS10 | Ownly's delivery fee is acceptable | Company claim / media | COMPANY CLAIM (contested) | H | **Fee itself is contested** (`01_secondary_research`): media report "~₹30 + GST" (Bengaluru); App Store says "Free delivery"; a launch-week bill showed ₹0; a vendor blog says "distance-based"; the Hyderabad page claims no platform/packaging/surge fee but publishes no delivery fee. Acceptance untested. | TEST FIRST | Audit (actual fee in Gachibowli) → H8.1 fee ladder | Acceptance at the audit-observed fee CI entirely < 50% |
| AS11 | The Rapido brand increases trust and trial | Distribution thesis | HYPOTHESIS | M | Mixed priors: ride-hailing brand ≠ food trust; possible negative spillover (cancellations) | TEST FIRST | H7 → randomised brand arms | Branded arm trust/intent not higher, or lower |
| AS12 | Rapido app distribution drives awareness in Hyderabad as in Bengaluru | Media/company | COMPANY CLAIM | M | Integration reported; Hyderabad awareness unknown | MONITOR | H9, H11.3 → unaided/aided awareness, acquisition source | Low aided awareness among Rapido ride users |
| AS13 | Gachibowli users multi-home, so trial is low-friction | Team inference | HYPOTHESIS | M | None | TEST FIRST | H9.4 → platforms used, subscriptions, habit lock | Majority single-homers with active subscription |
| AS14 | Incumbent subscriptions (Swiggy One, Zomato Gold) don't neutralise Ownly's fee advantage | Team inference | ASSUMPTION | H | Unknown | TEST FIRST | Audit with subscription on/off; subscription penetration | Subscriber checkout ≤ Ownly checkout in most matched pairs |
| AS15 | Discount-driven users will value "everyday low price" over coupons | Ownly model | ASSUMPTION | M | None; high offer dependency could falsify | TEST FIRST | H1.5, H2.4 → offer dependency, discount-framing scenario | Majority prefer the discount-framed bill at equal or higher total |
| AS16 | Students are more price-sensitive; professionals value time and reliability more | Common prior | HYPOTHESIS | M | None | TEST FIRST | H6 | No meaningful difference, or the reverse |
| AS17 | Students are a commercially viable first segment (frequency × basket) | Team inference | ASSUMPTION | M | None | TEST FIRST | H6.4 → frequency, AOV, occasions | Low AOV × low frequency, or campus delivery-access constraints |
| AS18 | Pain and switching drivers seen in Bengaluru exist at similar strength in Hyderabad | Transfer premise | HYPOTHESIS | H | None | TEST FIRST | H9.1–H9.2 → matched city comparison | Hyderabad PPI or SRI materially lower (beyond −10 pts) |
| AS19 | Bengaluru frictions (from reviews and churn) won't be more damaging in Hyderabad | Transfer premise | HYPOTHESIS | H | None | TEST FIRST | H9.3 → expectations, coverage, reviews by city | Hyderabad ETA expectations stricter and coverage thinner |
| AS20 | Early Hyderabad users will repeat after launch offers end | Growth thesis | UNKNOWN | H | None | TEST FIRST | H12 → Hyderabad Ownly users; interviews | Low repeat among tried users; "offer-only" trial reasons |
| AS21 | Stated interest converts into action | Survey default | ASSUMPTION | H | Known intention–behaviour gap in literature | TEST FIRST | H11 → fake door; aware→tried gap | Aware→tried conversion far below stated intent |
| AS22 | Restaurants in Hyderabad keep menu prices near dine-in on Ownly | Company claim | COMPANY CLAIM | M | Unverified | MONITOR | Audit with verified offline prices where possible | Ownly menu subtotal ≈ incumbent menu subtotal |
| AS24 | Users believe Ownly's low prices will last (so it's worth switching habits) | Implicit in everyday-low-price model | ASSUMPTION | H | **Contradicting signal:** 37 social items (Bengaluru, self-selected) expect prices/fees to rise; two cite Swiggy Toing later adding fees (`05_review_mining/social/social_analysis.md`) | TEST FIRST | Interviews (probe added), `bt_concern` open-text coding, H12.4 lapse reasons | Price-durability scepticism recurs in ≥3 interviews across ≥2 segments, or appears among the top-3 coded concerns |
| AS25 | Payment options don't block adoption | Not considered in v1 | ASSUMPTION | M | **Contradicting signal:** social posts report no meal-card (e.g. Pluxee) and no cash-on-delivery support; this may matter for salaried professionals | TEST FIRST | Option added to not-tried/barrier lists; interviews | "Payment method not accepted" among the top-3 barriers for any segment |
| AS23 | Gachibowli is a representative test bed for Hyderabad | Team framing | ASSUMPTION | L (for this study) | IT/student-dense micro-market; likely not representative | PARK (declare as limitation) | None — scope boundary | — |

## 3. Priority view (the 2×2)

```
                      EVIDENCE TODAY
                 weak / none        moderate / strong
IMPORTANCE  H   ┌────────────────────┬──────────────────┐
                │ TEST FIRST          │ MONITOR          │
                │ AS1 AS2 AS3 AS4 AS6 │ AS12 AS22        │
                │ AS7 AS8 AS9 AS10*   │                  │
                │ AS14 AS18 AS19 AS20 │                  │
                │ AS21                │                  │
            M   │ AS5 AS11 AS13 AS15  │                  │
                │ AS16 AS17           │                  │
            L   │ PARK: AS23          │                  │
                └────────────────────┴──────────────────┘
 * AS10: the fee level is reported; acceptance is untested.
```

## 4. The three riskiest assumptions (fieldwork must answer these first)

1. **AS3 + AS4: the price advantage is real and big enough.** If the audit shows no consistent advantage, or advantages smaller than the switching threshold, the core proposition does not transfer. That holds no matter what survey appeal scores say.
2. **AS7 + AS9: experience is acceptable.** Lower price has little value if dinner is late or the user's restaurants are missing. This is the non-negotiable guardrail family.
3. **AS20 + AS21: early trial becomes repeat behaviour.** Launch-period trial in Hyderabad may be offer-driven. Repeat and aware→tried evidence decides whether to scale or adapt.
