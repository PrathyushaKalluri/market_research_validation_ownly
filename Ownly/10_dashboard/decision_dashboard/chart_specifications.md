# Chart Specifications

Format: **ID · chart · KPI · encoding · base · interpretation rule**. Colours:
- Hyderabad blue, Bengaluru orange
- Service P amber, Service Q violet
- Ownly aqua, other apps in greys

Status colours (good/warn/critical) are used only for verdicts, always with a text label.

## Page 1 · Executive Decision Cockpit
| ID | Chart | KPI | Encoding | Base | Read |
|---|---|---|---|---|---|
| 1.1 | H₀ banner | K13 / K14 | Primary test named (fake door or survey per D3); effect, CI, p, verdict pill | Visitors per arm / Hyderabad decided | decision_rules §1 |
| 1.2 | Overall call chip | §3 rules | REPLICATE / ADAPT / LOCALIZE / INSUFFICIENT EVIDENCE + PROVISIONAL flag | — | decision_rules §3 |
| 1.3 | KPI cards (9) | K00 north star, K10, K01, K13, K20, K32, K33, K40, K50 | Value, CI, n, evidence label, Bengaluru comparator | Per KPI | Guardrail cards turn red on breach |
| 1.4 | Transferability Matrix | 6 rows × (Bengaluru evidence, Hyderabad evidence, KPI, confidence, verdict) | Table with verdict chips | — | decision_rules §2 |

## Page 2 · Bengaluru Playbook
| 2.1 | Strategy timeline | external | Dated milestones, colour by type (launch / model / funding / competitor) | — | Context |
| 2.2 | Reported orders/day | K90 | Dot + line, only sourced points (Mar 5k, Jul 40k, Aug 50k) | — | Always labelled external |
| 2.3 | Fee-model strip | external | Periods × restaurant side / customer side | — | Never mix periods |
| 2.4 | Bengaluru user benchmark | K62, K17, K31, K36 (Bengaluru filter) | Ranked bars | Bengaluru respondents | Benchmark for Hyderabad |
| 2.5 | Claims vs evidence | external + ours | Claim · source · our test · status | — | Unverified claims marked |

## Page 3 · Hyderabad Market
| 3.1 | Profile | occupation, member, A1 | 100% stacked bars | Hyderabad eligible | — |
| 3.2 | Order frequency | S4 total | Histogram (0, 1–2, 3–5, 6–10, 11+) | Recent orderers | — |
| 3.3 | Share of orders by app | K92 | 100% stack, Ownly aqua | Orders | — |
| 3.4 | Funnel | K10, K11, K12, trier, K30 | Horizontal funnel, Hyderabad vs Bengaluru | Eligible | Where the biggest drop is |
| 3.5 | ₹30 trade-offs | K24 | Grouped bars, 50% line | Answered | >50% = price wins |
| 3.6 | Triers vs non-triers | K24, K25, member | Paired bars | Hyderabad | — |

## Page 4 · First vs Second Order
| 4.1 | First-order drivers (left) | K17, K16, K24 speed, K72 | Ranked bars | Stage bases | — |
| 4.2 | Second-order drivers (right) | K36, K24 reliability, K52, K34 | Ranked bars + gap bar | Triers | — |
| 4.3 | Acquisition → retention funnel | K10 → K01 → K30 → K00 | Step bars | Eligible | — |
| 4.4 | Hypothesis check | decision_rules §4 | 3 conditions ✓/✕/? | — | Never stated as fact |

## Page 5 · Is Ownly Actually Cheaper?
| 5.1 | Matched-basket waterfall | K22 components | Median menu → +fees → −discount → final, per platform | Matched sets | — |
| 5.2 | Saving per set | K20 | Dot plot sorted, 0 line, ₹5 tie band | Sets | Dots left of 0 = Ownly dearer |
| 5.3 | Tiles | K20, K21, K22, K50 | Value + CI + k/n | Sets | — |
| 5.4 | Saving vs ETA gap | K20 × K50 | Scatter, quadrant labels | Sets | Cheaper and slower quadrant = trade-off |
| 5.5 | Threshold vs saving | K23 | Threshold histogram + observed median line | Numeric thresholds | — |

## Page 6 · Can the Marketplace Deliver?
| 6.1 | Coverage matrix | K40, K41 | Restaurant × platform grid (✓/✕), chain/local tag | Frame (10) | — |
| 6.2 | Availability overlap | K42 | Stat + by slot | Captures | — |
| 6.3 | Failure incidence | K51 by failure type | Ranked bars | Ownly users | — |
| 6.4 | Review theme map | K53 | Ranked bars with a **"self-selected sample, not prevalence"** banner | 37 reviews / 123 first-hand posts | Issue discovery only |

## Page 7 · Rapido Distribution
| 7.1 | Rapido usage | K60 | 100% stack by frequency | Eligible | — |
| 7.2 | Awareness and trial: users vs non-users | K61 | Paired bars + pp gap + CI | Each group | Association only |
| 7.3 | Discovery source | K62 | Ranked bars | Aware | — |
| 7.4 | Fake-door by channel | utm_source | Table: visitors, CTA % | Visitors | Directional |

## Page 8 · Promotion
| 8.1 | Offer-triggered first order | K70 | Stat + stack | Users | — |
| 8.2 | Repeat by offer | K71 | Paired bars + gap | Users | — |
| 8.3 | Trial intent vs repeat without promo | K15 vs K32 | Paired bars, ½ line | Answered | Rule 2.4 |
| 8.4 | Segment split | K32, K71 by occupation | Grouped bars | Segments | TARGET TO SEGMENT rule |

## Page 9 · Segment Prioritization
| 9.1 | Segment matrix | K94-style frequency, K10, K01, K24 price-first, K32, K71, K33, K14 Q share | Table, raw values + n, **no composite score** | Segments | Read across rows |

## Page 10 · Final Decision
| 10.1 | KEEP / ADAPT / DROP cards | decision_rules §2 | Card per element: verdict, metric, qualitative note, confidence, source, implication | — | — |
| 10.2 | H₀ statement | K13/K14 | Reject / fail to reject + "means / does not mean" | — | — |
| 10.3 | Not calculable | Layer 10 | List | — | Honesty panel |
| 10.4 | Next validation | — | Checklist before citywide scale | — | — |
