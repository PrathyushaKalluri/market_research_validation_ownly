# Convert an existing v6 form into v7

**Time:** about 35 minutes plus a 10-minute test. Building v7 from scratch takes about 30 minutes.
Keep this file and `Survey_v7_Google_Form_Build_Guide.md` open side by side. The v7 guide has the
copy-paste boxes; this guide says **where** each one goes.

---

## Step 0 · Convert, or build fresh?

| Your situation | Do this |
|---|---|
| **Real responses have already come in on v6** | **Don't convert.** Deleting a section deletes its responses too. Leave v6 alone, close it, and build v7 as a new form (count v6 as wave 1) |
| The v6 link **has already been shared** (in groups, posters or QR codes), but no real responses yet | **Convert.** The link stays the same |
| The link hasn't been shared yet | **Either works.** A fresh form is slightly quicker and leaves no leftover settings behind. Converting saves nothing |

Before you start: **Responses tab → ⋮ → Delete all responses** (test responses only), then
**Responses → ⋮ → Unlink form**. The old sheet keeps columns for deleted questions, so you'll link a new one at the end.

> **Rules for the whole conversion**
> 1. **Identify sections by title, never by number.** Numbers shift after every delete.
> 2. Branches that pointed at deleted sections quietly reset. **Don't fix branches until Step 6**, where you set them all at once.
> 3. **Merge with above** (⋮ on a section header) joins a section to the one above it. The lower section's
>    **title and description disappear**, but its questions stay.

---

## Step 1 · Delete 20 whole sections (5 min)

On each section header: **⋮ → Delete section**. Work **from the bottom up**.

| Delete | Sections |
|---|---|
| The whole Other-city path | `Other city · Ownly users` · `Other city · About Ownly` · `Other city · Ownly` · `Other city · Your last order` · `Other city · Your orders` · `Other city · About you` · `Other city · Your city` |
| The whole Bengaluru path | `Bengaluru · Ownly users` · `Bengaluru · A bit more about Ownly (2)` · `Bengaluru · A bit more about Ownly` · `Bengaluru · About Ownly` · `Bengaluru · Ownly` · `Bengaluru · Two services` · `Bengaluru · Quick choices` · `Bengaluru · Your last order` · `Bengaluru · Your orders` · `Bengaluru · About you` · `Bengaluru · Your area` |
| Two Hyderabad pages | `Hyderabad · A bit more about Ownly (2)` · `Hyderabad · About Ownly` |

✅ **Checkpoint: 12 sections**, in this order: *(title card)* · Hyd Your area · Hyd About you · Hyd Your orders ·
Hyd Your last order · Hyd Quick choices · Hyd Two services · Hyd Ownly · Hyd A bit more about Ownly ·
Hyd Ownly users · Last question · Thank you!

---

## Step 2 · Merge 3 pairs of sections (2 min)

**⋮ → Merge with above** on each of these:

| Merge this section… | …into | Lost when merged (that's intended) |
|---|---|---|
| `Hyderabad · About you` | `Hyderabad · Your area` | its title |
| `Hyderabad · Your last order` | `Hyderabad · Your orders` | "Now just your most recent order." |
| `Hyderabad · Two services` | `Hyderabad · Quick choices` | the Service P / Q text. You add the new version back in Step 4 |

> **If "Merge with above" isn't in your ⋮ menu:** drag each question (the ⠿ handle at the top of the card)
> up into the section above, then delete the empty section.

✅ **Checkpoint: 9 sections.** That's the final count for v7.

---

## Step 3 · Title card, form description and settings (2 min)

**Form title:** paste the v7 title (it says **4-minute**, not 6-minute).
**Form description:** replace it with the v7 description.

**The city question on the title card becomes the age question.** Branching is already switched on, so keep it on:
- Question text → `How old are you?`
- Delete the 3 options and paste the 4 v7 age options (`Under 20` · `20–25` · `26–30` · `Over 30`)

---

## Step 4 · Edit the remaining sections, top to bottom (20 min)

Legend: 🗑 delete · ✏️ change · ➕ add · ✔ leave as it is

### Section 2 (was "Hyderabad · Your area" + "About you") → **About you**

| | Question | Action |
|---|---|---|
| ✏️ | Section title | → `About you` |
| ✏️ | Which area? | Change the type to **Dropdown** · text → `Where do you live, study or work on most days?` · delete all options and paste the **13 v7 options** |
| 🗑 | How old are you? | Delete it (it now lives on the title card) |
| ✏️ | Which best describes you right now? | Delete the 6 options and paste the 4 v7 options |
| ✏️ | Which food delivery memberships… | Change the type from **Checkboxes to Multiple choice** · text → `Do you have a paid food delivery membership right now?` · ⋮ → untick **Description** · replace the options with `Swiggy One` · `Zomato Gold` · `Both` · `Neither` |
| ✔ | In the last 4 weeks, did you order food online… | Keep it. **It must stay the last question** on the page |

### Section 3 (was "Your orders" + "Your last order") → **Your recent orders**

| | Question | Action |
|---|---|---|
| ✏️ | Section title / description | Title → `Your recent orders` · delete the description |
| 🗑 | Swiggy / Zomato / Ownly / Any other way: how many orders… | Delete all 4 |
| ➕ | **Q6 Orders per app (grid)** | Add it at the **top** of the section. Copy it from the v7 guide: type **Multiple choice grid**, 4 rows, 4 columns, **Require a response in each row** ON |
| 🗑 | Which app did you use for your most recent… | Delete it |
| ✏️ | What was the total amount you paid for it? | Text → `Your most recent order: what was the total amount you paid?` (the description and validation stay) |
| 🗑 | How many people was that order for? | Delete it |
| ✏️ | Thinking about that amount: did it feel fair… | Text → `Did that amount feel fair for what you got?` · last option → `I didn't really check` |

### Section 4 (was "Quick choices" + "Two services") → **A few quick choices**

| | Question | Action |
|---|---|---|
| ✏️ | Section title / description | Title → `A few quick choices` · description → paste the v7 one |
| ✔ | Same restaurant, same food. Which would you choose? | Keep it as it is |
| ✏️ | Same restaurant, same food, same delivery time… | Replace both options with the v7 ones (`late in about 1 of every 10 orders` / `3 of every 10`) |
| ✏️ | Same food price level and delivery time… | Text → `Same delivery time. Which would you choose?` (options unchanged) |
| 🗑 | Think of a typical order… how much lower… | Delete it |
| ➕ | **Text block "Two services"** | Click the restaurants trade-off question, then **Tt** in the toolbar. Paste the v7 title and description (Service Q now has **3 bullets** and no "Hyderabad") |
| 🗑 | If SERVICE P were available… | Delete it |
| 🗑 | And if SERVICE Q were available… | Delete it |
| ✔ | If only one of them existed… | Keep it. Check **Shuffle option order** is still ON |
| ✔ | In one line, what made you pick that one? | Keep it (optional) |
| 🗑 | Imagine you tried the one you picked… ₹100 off… | Delete it |
| 🗑 | How much do you agree: "A new app's low prices…" | Delete it |

✅ The page should read: 3 trade-offs → Two services text → forced choice → why.

### Section 5 · "Hyderabad · Ownly" → **Ownly**

| | Question | Action |
|---|---|---|
| ✏️ | Section title | → `Ownly` |
| ✏️ | Ownly is a food delivery app by Rapido… | Text → the v7 wording (`(the bike-taxi app)`). The 4 options stay as they are |

### Section 6 · "Hyderabad · A bit more about Ownly" → **What's holding you back**

| | Question | Action |
|---|---|---|
| ✏️ | Section title | → `What's holding you back` |
| 🗑 | Where did you first hear about Ownly? | Delete it |
| ✏️ | What's the MAIN reason you haven't opened it? | Text → `What's the MAIN reason you haven't ordered on Ownly?` · replace the 7 options with the **6 v7 options** |

### Section 7 · "Hyderabad · Ownly users" → **Ownly users**

| | Question | Action |
|---|---|---|
| ✏️ | Section title / description | Title → `Ownly users` · description → paste the v7 one |
| 🗑 | Where did you first hear about Ownly? | Delete it |
| 🗑 | Where have you ordered on Ownly? | Delete it |
| ✏️ | When did you place your FIRST Ownly order? | Replace the 2 options with the 3 v7 options |
| ✏️ | How many Ownly orders… 4 weeks BEFORE… | Change the type from **Short answer to Multiple choice** (this removes the number validation, which is fine) · ⋮ → untick **Description** · paste the options `0` · `1–2` · `3–5` · `6+` |
| ✏️ | Think of your most recent Ownly order. If Ownly didn't exist… | Text → the v7 wording (`what would you have done instead?`) · replace the 6 options with the 5 v7 options |
| ✔ | How would you feel if you could no longer use Ownly? | Keep it as it is |
| ✏️ | What ONE change would make you order more on Ownly? | Replace the 7 options with the 5 v7 options |

### Sections 8 and 9 · Last question / Thank you!
✔ Leave both as they are.

---

## Step 5 · Search for leftovers (2 min)

In the editor, press **Ctrl/Cmd + F** and search for each of these. **None should appear:**
`Hyderabad ·` · `Bengaluru ·` · `SERVICE P were` · `Swiggy: how many` · `first hear` · `Tick all` · `Option 1` · `Copy of`

(`Hyderabad ·` and `Bengaluru ·` **will** appear inside the location dropdown's options. That's correct.
They should not appear in any **section title**.)

---

## Step 6 · Set every branch (5 min)

Set these by **section name**, even the ones that already look right:

| Where | Setting |
|---|---|
| Title card: How old are you? | Under 20 → **Thank you!** · 20–25 → **About you** · 26–30 → **About you** · Over 30 → **Thank you!** |
| About you: ordered in last 4 weeks? | Yes → **Your recent orders** · No → **A few quick choices** |
| Ownly: Before today… | Hadn't heard → **Last question** · Heard, never opened → **What's holding you back** · Opened, didn't order → **What's holding you back** · Ordered → **Ownly users** |
| After *Your recent orders* | → A few quick choices |
| After *A few quick choices* | → Ownly |
| After *What's holding you back* | → **Last question** |
| After *Ownly users* | → **Last question** |
| After *Last question* | → **Submit form** |

---

## Step 7 · Finish (10 min)

1. **Responses → Link to Sheets → Create a new spreadsheet** → name it `Ownly Survey v7 responses`.
2. Run the **5 test paths** in Part 5 of the v7 guide, on a phone as well as a laptop.
3. Delete the test responses from the form **and** the new sheet.
4. Update the sharing messages: **"6 minutes" → "4 minutes"**.

✅ **Final check:** 9 sections · 21 questions in total (19 required, plus the optional "why" and the WhatsApp number) ·
1 grid · 1 dropdown · 1 text block · 3 branching questions.
