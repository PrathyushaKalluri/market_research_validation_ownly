# Interview Screener — Google-Form-ready + phone script

**Version:** v2, 2026-09-14. Used for Hyderabad interviews (main) and the optional Bengaluru Ownly module (branch B).
**Principle:** the screener must not reveal the research focus (Ownly, price, fees). Brand questions are hidden among a list of several apps.

---

## PART A — Google Form (copy-paste)

**Form title:** Food Ordering Habits — Research Conversation Sign-up
**Form description:**
> We're a student research team studying how young people decide how and where to order food. This 2-minute form checks whether you fit the group we're speaking to. If you're selected, we'll contact you to schedule a 30–45 minute conversation. This research is independent and not conducted by or for any food-delivery, restaurant or ride-hailing company. Your answers are used only to select participants and are deleted after the project.

Settings: do **not** require Google sign-in. Collect email: **off** (contact is collected in Q14). Shuffle option order where marked [shuffle].

### Section 1 — Basic eligibility

**Q1. How old are you?** *(Short answer, response validation: Number, between 18 and 60)*
→ `scr_age`. **Disqualify if <20 or >30** (form still submits; flag in sheet).

**Q2. Which city do you currently live, study or work in most days?** *(Multiple choice)*
- Hyderabad
- Bengaluru
- Other
→ `scr_city`. Other → disqualify. Hyderabad → Section 2. Bengaluru → Section 2 (Bengaluru branch is flagged later by Q7).

**Q3. In the last 4 weeks, roughly how many times have YOU ordered food for delivery through any app or directly from a restaurant (not groceries)?** *(Multiple choice)*
- 0
- 1–3
- 4–7
- 8–15
- 16 or more
→ `scr_orders_4wk`. **0 → disqualify.** Derive `seg_freq`: 1–3 occasional, 4–7 regular, 8+ frequent.

### Section 2 — About you

**Q4. Which best describes you right now?** *(Multiple choice)*
- Full-time student (not working)
- Working full-time or part-time (not studying)
- Both studying and working
- Neither currently
→ `seg_occupation` = student / working_professional / working_student / other. **"Neither" → disqualify.**

**Q5. [If student or working_student] Where do you study?** *(Short answer)* → `scr_institution` (coded later; used for the IIIT-H cap).

**Q6. Where do you live most days?** *(Multiple choice)*
- College hostel
- PG
- Shared flat with friends/colleagues
- Living alone
- With family
- Other
→ `dem_living`.

**Q7. Which area do you live in, and which area do you study/work in? (e.g. "live Kondapur, work Financial District")** *(Short answer)*
→ `scr_locality_text` (coded to: Gachibowli, Financial District/Nanakramguda, HITEC City/Madhapur, Kondapur, Manikonda/Narsingi, Kukatpally, Other Hyderabad, Bengaluru-area). **Hyderabad respondents whose home and work/study are both outside the West Hyderabad corridor → hold as low priority (not disqualified).**

### Section 3 — Ordering

**Q8. Which of these have you used to order food in the last 3 months? (Select all)** *(Checkboxes) [shuffle]*
- Swiggy
- Zomato
- Magicpin
- Ownly (by Rapido)
- EatSure
- Directly from a restaurant (call/WhatsApp/restaurant's own app)
- ONDC-based app (e.g. via Paytm/PhonePe Pincode)
- Other
- None of these
→ `scr_platforms_3m` (multi). Ownly is hidden among 8 options.

**Q9. Which ONE did you use most in the last 4 weeks?** *(Multiple choice, same list, [shuffle])* → `scr_platform_primary`.

**Q10. Do you currently have any of these memberships? (Select all)** *(Checkboxes)*
- Swiggy One / One Lite
- Zomato Gold
- Other food-app membership
- None
- Not sure
→ `scr_subscriptions`.

**Q11. [Only if Ownly ticked in Q8] Roughly when did you last order through Ownly?** *(Multiple choice)*
- In the last 4 weeks
- 1–3 months ago
- More than 3 months ago
- I've installed/opened it but never ordered
→ `scr_ownly_status` = current / lapsed / lapsed_old / aware_no_order (not ticked → `not_used`).
**Q11b. [Only if Ownly ticked] In which city did you order through Ownly?** Hyderabad / Bengaluru / Both / Other → `scr_ownly_city`.

### Section 4 — Final checks

**Q12. Do you or any close family member currently work for any of the following? (Select all)** *(Checkboxes)*
- A food-delivery or quick-commerce company
- A ride-hailing company
- A restaurant, cloud kitchen or food brand
- A market research or advertising agency
- None of these
→ `scr_conflict`. **Any except "None" → disqualify.**

**Q13. Have you taken part in an interview or focus group about food ordering apps in the last 6 months?** Yes / No → `scr_prior_research`. **Yes → disqualify.**

**Q14. If selected, how should we reach you? (Name or nickname + WhatsApp number or email)** *(Short answer)* → stored in the **recruitment sheet only**, never copied into transcripts or the analysis files.

**Q15. Preferred format:** In person near Gachibowli / Video call / Either → `scr_mode_pref`.
**Q16. When are you usually free? (Select all):** Weekday lunch / Weekday evening / Weekend → `scr_availability`.

**Confirmation message:** "Thanks! If you fit the group we're currently speaking to, we'll message you within 3 days. If not, we won't contact you again, and your details will be deleted at the end of the project."

---

## PART B — Selection rules (applied in the response sheet)

| Rule | Logic |
|---|---|
| Eligible | age 20–30 AND city ∈ {Hyderabad, Bengaluru} AND orders_4wk ≥ 1 AND occupation ≠ other AND conflict = None AND prior_research = No |
| Hyderabad main pool | eligible AND city = Hyderabad |
| Bengaluru module pool | eligible AND city = Bengaluru AND Ownly ticked AND ownly_city ∈ {Bengaluru, Both} |
| Ownly-user overlay | ownly_status ∈ {current, lapsed} AND ownly_city includes Hyderabad |
| Heavy-loyalist overlay | seg_freq = frequent AND (subscriptions include Swiggy One/Zomato Gold OR only 1 platform ticked in Q8 excluding "Directly") |
| Unaware-of-Ownly overlay | Ownly not ticked in Q8. Awareness itself is checked in the interview, because not ticking ≠ unaware. |
| Priority | Fill empty quota cells first. Within a cell, prefer non-IIIT-H students (until the cap) and spread workplace clusters. |

Sheet formula example (Google Sheets, eligibility flag in a helper column):
`=AND(B2>=20,B2<=30,OR(C2="Hyderabad",C2="Bengaluru"),D2<>"0",E2<>"Neither currently",L2="None of these",M2="No")`

---

## PART C — Phone / WhatsApp-call confirmation script (2–3 min, before booking)

> "Hi [name], this is [interviewer] from the student research team. You filled our food-ordering research form. Thanks! I just need to confirm a couple of details before booking. Is now OK for 2 minutes?"

1. "Just to confirm, you're [age] and you [live/study/work] around [area]?" (confirm Q1, Q7)
2. "Roughly how many times did you order food delivery in the last 4 weeks? Think of this week and the three before." (re-check Q3; **if the answer falls in a different band, use the phone answer and note the change**)
3. "Do you mainly study, mainly work, or both?" (Q4)
4. "Do you or anyone in your close family work at a delivery app, ride-hailing company, restaurant, or a market-research/ad agency?" (Q12. If yes → politely end.)
5. "The conversation is about 30–45 minutes, about how you actually order food. There are no right or wrong answers, and we're not selling anything. We'd like to audio-record for note accuracy, but only with your permission, and you can say no. [Incentive: ₹__ voucher.] Does [slot A / slot B] work?"
6. "Optional: during the chat we might ask you to open your food app's order history and walk us through a recent order. That's completely optional, and you can hide anything personal. Is that OK in principle?" (record `show_me_ok`)

**If ineligible:** "Thank you so much for your time. For this round we're speaking with a slightly different group, so we won't need to schedule. Your details will be deleted."

**Do NOT say:** "We're researching Ownly / Rapido", "cheaper food delivery", "hidden fees", "a new app". If asked "Is this for a company?": "No, it's an independent university project about food-ordering habits. We'll explain more at the end of the conversation."
