# Setting up storage — every step, in order

**Read this once before you start, then follow it top to bottom.** Nothing here needs any coding.
You will copy one file into a Google Sheet, press a few buttons, and paste one link back.

**Time:** about 15 minutes.
**You need:** a Google account, and this folder open on your computer.

When you are finished, every tap and every search from every participant lands in a spreadsheet
automatically, and you never have to remember to download anything.

---

## What you are building

```
   participant's phone                  your Google account
  ┌────────────────────┐              ┌──────────────────────┐
  │  fake_door.html    │  ──POST──►   │  Apps Script         │
  │  (you send them    │              │  (the collector)     │
  │   the link)        │              │         │            │
  └────────────────────┘              │         ▼            │
                                      │  Google Sheet        │
                                      │  one row per tap     │
                                      └──────────────────────┘
```

Two files in this folder do the work:

| File | What it is | What you do with it |
|---|---|---|
| **`apps_script_collector.gs`** | The collector code | Copy-paste it into Google |
| **`fake_door.html`** | The prototype | Paste two links into the top of it |

---

# PART 1 · Create the Sheet and paste the collector

### Step 1 — Make a blank Google Sheet

1. Go to **[sheets.new](https://sheets.new)** — this creates a new blank spreadsheet.
2. Click **"Untitled spreadsheet"** at the top left and name it:
   ```
   Ownly Fake Door Responses
   ```
3. Leave the tab at the bottom called `Sheet1` exactly as it is. **Do not rename or delete it.**
   The script creates its own tabs and ignores this one.

### Step 2 — Open the script editor

In that same Sheet, from the menu bar:

**Extensions** → **Apps Script**

A new browser tab opens, titled *Untitled project*, showing a code editor with a few lines in it
that look like this:

```javascript
function myFunction() {

}
```

### Step 3 — Delete what is there and paste ours

1. Click anywhere inside that code area.
2. Select everything: **Ctrl+A** (Windows) or **Cmd+A** (Mac).
3. Press **Delete**. The editor should now be completely empty.
4. Now open **`apps_script_collector.gs`** from this folder in any text editor (or in VS Code).
5. Select all of it and copy it.
6. Click back into the empty Google editor and paste.

You should now see, near the top:

```javascript
var EXPERIMENTS = ['hyd_gach_fakedoor_2026_09', 'hyd_gach_discovery_2026_09'];
```

If you see that line, the paste worked.

### Step 4 — Name and save the project

1. Click **"Untitled project"** at the top left.
2. Type `Ownly Collector` and click **Rename**.
3. Press **Ctrl+S** / **Cmd+S** to save. A small "Saved" toast appears.

### Step 5 — Create the tabs

At the top of the editor there is a dropdown that currently says a function name, next to a
**▷ Run** button.

1. Open that dropdown and choose **`setupSheets`**.
2. Click **▷ Run**.

**Google will now ask for permission. This is expected — it is your own script asking to write to
your own spreadsheet.** Click through it:

- *"Authorization required"* → **Review permissions**
- Choose your Google account
- You will see **"Google hasn't verified this app"** — this is normal for a script you just wrote
  yourself. Click **Advanced** (small link, bottom left), then **Go to Ownly Collector (unsafe)**.
- Click **Allow**.

The run finishes and the Execution log at the bottom says something like
`Tabs ready: events, contacts`.

3. Switch back to your spreadsheet tab and check. There are now **two new tabs at the bottom**:
   **`events`** and **`contacts`**, each with a header row.

> **If you do not see the tabs:** you probably clicked Run before choosing `setupSheets` in the
> dropdown. Choose it and Run again.

---

# PART 2 · Publish the collector and get its link

### Step 6 — Deploy it as a web app

Back in the Apps Script tab:

1. Top right, click the blue **Deploy** button → **New deployment**.
2. Next to **"Select type"** there is a small **gear icon** ⚙. Click it and choose **Web app**.
3. Fill the form exactly like this:

   | Field | What to put |
   |---|---|
   | Description | `collector v1` |
   | Execute as | **Me (your@email)** | 
   | Who has access | **Anyone** |

   **"Anyone" is required and it is safe.** It lets a phone send a row *in*. It does **not** let
   anyone read your spreadsheet — see the note at the end of this file.

4. Click **Deploy**.
5. Copy the **Web app URL**. It ends in **`/exec`** and looks like:

   ```
   https://script.google.com/macros/s/AKfycbx.....................mA/exec
   ```

   **Paste it somewhere safe for a minute** — a notes app, or just leave the tab open.

> ⚠ **Take the URL ending in `/exec`, not `/dev`.** The `/dev` one only works while you are
> logged in, so it will fail on a participant's phone.

### Step 7 — Check the link is alive

1. Open a **new browser tab** and paste that `/exec` URL into the address bar. Press Enter.
2. You should see this plain text:

   ```
   collector alive: hyd_gach_fakedoor_2026_09, hyd_gach_discovery_2026_09
   ```

**If you see that, the collector works.** If you see an error page, go back to Step 6 and check
"Who has access" is set to **Anyone**.

---

# PART 3 · Make the survey and its QR

### Step 8 — Create the Google Form

1. Go to **[forms.new](https://forms.new)**.
2. Name it something a participant will recognise, e.g. `How Gachibowli orders food`.
3. Add your questions.
4. **Settings** (top tab) → turn **"Collect email addresses"** to **Off**, so it stays anonymous.
5. Click **Send** (top right) → click the **🔗 link icon** → tick **Shorten URL** → **Copy**.

   You now have a link like:
   ```
   https://forms.gle/AbCdEfGhJkLmNpQr7
   ```

> The prototype builds the QR code from whatever link you paste, on the spot. You do **not** need
> to generate a QR anywhere else — and it works with no internet, because the QR is drawn inside
> the page.

---

# PART 4 · Put the two links into the prototype

### Step 9 — Open the prototype

Open **`fake_door.html`** from this folder in a text editor (VS Code, TextEdit, Notepad — anything).

Press **Ctrl+F** / **Cmd+F** and search for:

```
ENDPOINT
```

You will land on this block, near the top of the `<script>` section:

```javascript
var CONFIG = {
  EXPERIMENT_ID: "hyd_gach_fakedoor_2026_09",
  PAGE_VERSION: "2026-09-23.v5",
  ENDPOINT: "",
  /* Paste your Google Form link here. Leave empty and the survey step is
     hidden entirely — no dead button, no broken QR. See STORAGE_SETUP.md. */
  SURVEY_URL: "",
  ARMS: ["discount", "restaurants"]
};
```

### Step 10 — Paste both links

Change **only** the two empty pairs of quotes:

```javascript
var CONFIG = {
  EXPERIMENT_ID: "hyd_gach_fakedoor_2026_09",
  PAGE_VERSION: "2026-09-23.v5",
  ENDPOINT: "https://script.google.com/macros/s/AKfycbx.....................mA/exec",
  /* Paste your Google Form link here. ... */
  SURVEY_URL: "https://forms.gle/AbCdEfGhJkLmNpQr7",
  ARMS: ["discount", "restaurants"]
};
```

**Rules:**
- Keep the **quotes** around each link.
- Keep the **comma** at the end of each line.
- Do not change anything else in that block.

Save the file.

### Step 11 — Do the same for the second prototype

Open **`mobility_entry.html`** in the same folder, search for `ENDPOINT`, and paste the **same
`/exec` link** there. Save.

*(That file is the separate discovery mock. If you are not running that part, skip this step.)*

---

# PART 5 · Test it before anyone real uses it

**Do not skip this.** It is the only thing that proves the whole chain works, and it takes two
minutes.

### Step 12 — Walk through it once as a test

1. Open `fake_door.html` in your browser, but add `?qa=1` to the end of the address:

   ```
   file:///.../SUBMIT_EXPERIMENT/fake_door.html?qa=1
   ```

   A black bar appears at the bottom. That is the facilitator panel — it only shows with `?qa=1`.

2. Check the black bar says **`endpoint=on`**. If it says `endpoint=OFF`, the link in Step 10 did
   not save properly.

3. Now **go all the way through**: search a dish, pick a place, add an item, choose delivery, apply
   an offer, choose how to pay, tap **Place Order**, then **Yes — I'll answer a few more questions**.

4. Check the **QR code appears** on that last screen, and point your phone camera at it. Your
   Google Form should open on the phone.

### Step 13 — Confirm the rows arrived

1. Go back to your **Google Sheet**.
2. Click the **`events`** tab.
3. **Refresh the page** (Ctrl+R / Cmd+R).

You should see **dozens of rows**, one per action, with columns like `event_name`, `ts_iso`,
`payload_json`.

✅ **If the rows are there, you are done. The setup works.**

### Step 14 — Delete the test rows

Your test run is marked `is_qa = TRUE`, and the analysis script drops those automatically — so you
*can* leave them. But it is tidier to remove them:

1. In the `events` tab, click the row number of the first data row (row 2).
2. Scroll to the bottom, hold **Shift**, click the last row number.
3. Right-click → **Delete rows**.

**Never delete row 1** — that is the header.

---

# Running it with real participants

**Give them the link without any parameters:**

```
fake_door.html
```

Not `?qa=1`. Anything with `qa=1` or `variant=` in the address is marked as a test and is thrown
away at analysis time.

| To do this | Use this address |
|---|---|
| A real participant | `fake_door.html` |
| Preview one arm yourself | `fake_door.html?variant=restaurants&qa=1` |
| Test a specific delivery price | `fake_door.html?qa=1&rl=35` |
| Record where they came from | `fake_door.html?source=whatsapp` |

---

# Getting the data out for analysis

When fieldwork is done:

1. Open the Sheet → **`events`** tab.
2. **File** → **Download** → **Comma Separated Values (.csv)**.
3. Save it into this folder as `events.csv`.
4. Open a terminal in this folder and run:

   ```bash
   python3 analyse_results.py events.csv
   ```

That prints the funnel, the search types, the zero-result gaps, the three willingness-to-pay curves
and every in-journey answer.

To see what the output looks like before you have any real data:

```bash
python3 analyse_results.py --demo
```

*(That runs on fabricated numbers and says so loudly at the top. Never mix it with real results.)*

---

# If you change the collector code later

**This catches everyone out.** Editing the script does **not** update the live link. You must:

**Deploy** → **Manage deployments** → click the **✏️ pencil** → under *Version* choose
**New version** → **Deploy**

The `/exec` URL stays the same. If you skip this, your edits do nothing and the collector silently
keeps running the old code.

---

# Troubleshooting

| What you see | What it means | Fix |
|---|---|---|
| QA bar says `endpoint=OFF` | The link did not save into `CONFIG.ENDPOINT` | Redo Step 10 — check the quotes and comma |
| The `/exec` URL shows an error page | Access is not set to "Anyone" | Step 6, redeploy |
| No rows in `events`, no errors | You are probably looking at the `/dev` URL | Use the one ending `/exec` |
| Rows appear but say `rejected: event_name` | The collector is older than the prototype | Redeploy as **New version** (above) |
| QR does not appear | `SURVEY_URL` is empty | Step 10 |
| QR appears but says FACILITATOR… | Same — the link is missing | Step 10 |
| Red bar: *storage blocked* | The phone is in private browsing | Use a normal window |
| Nothing at all happens on tap | The file was saved mid-edit and broke | Reopen the archived copy and redo Step 10 |

---

# What is stored, and what is not

**Stored:** every screen reached, every tap, every search string, every answer, timings, the
randomly assigned prices, and a random ID per device.

**Never stored:** name, phone number, email, address, location, IP, or any payment detail — the
prototype never asks for any of them, and there is no field in it that could.

Free text is scrubbed of anything resembling an email or a phone number **twice** — once in the
browser before it is sent, and again in the collector before it is written.

**Why "Anyone" access is safe.** The `/exec` link is write-only. It accepts a row and replies `ok`.
It cannot read the Sheet, cannot list rows, and carries no password or key. The Sheet itself stays
private to your Google account. There is nothing in the HTML that could be used to read your data.

**The participant's deletion code.** The last screen shows an 8-character code. If someone asks you
to delete their answers, search the `anon_visitor_id` column in the `events` tab for a value
starting with those 8 characters (lowercase) and delete those rows.
