# Deploy it, share it, and watch the numbers come in

**Follow this top to bottom. No coding.** About 30 minutes end to end.

Do **`STORAGE_SETUP.md` first** — this guide assumes your Apps Script collector already works and
you have the `/exec` URL.

---

## The shape of it

```
   a participant's phone                     your Google account              you
  ┌──────────────────────────┐            ┌─────────────────────┐       ┌──────────────┐
  │  your-site.netlify.app   │ ─ POST ─►  │  Apps Script        │       │ metrics.html │
  │  (index.html)            │            │        ↓            │  ◄──  │  on YOUR     │
  │  every tap, every search │            │  Google Sheet       │  read │  laptop      │
  └──────────────────────────┘            └─────────────────────┘  key  └──────────────┘
```

**Three files do the work:**

| File | Where it lives | Who sees it |
|---|---|---|
| `deploy/index.html` | Netlify, public | Participants |
| `apps_script_collector.gs` | Google, private | Nobody — it just writes |
| `metrics.html` | **Your laptop only** | You |

---

# PART A · Put the prototype on the internet

### A1 — Check the deploy folder is ready

In this folder there is a subfolder called **`deploy`**. It contains **only** what a participant
should ever receive:

```
deploy/
  index.html          ← the prototype (a copy of fake_door.html)
  mobility_entry.html ← the separate discovery mock
  _headers            ← security headers
  robots.txt          ← keeps it out of Google search
```

**Everything else stays off the internet** — the design document, the archives, the analysis script,
the collector source and `metrics.html`. Do not upload the whole folder.

> ⚠ **If you changed `fake_door.html` after reading this, re-copy it:**
> ```bash
> cp fake_door.html deploy/index.html
> ```
> `deploy/index.html` is a **copy**, not a link. Editing `fake_door.html` does not update it.

### A2 — Confirm your two links are already in it

Open `deploy/index.html`, press **Ctrl+F** / **Cmd+F**, search for `ENDPOINT`. You should see both
filled in:

```javascript
  ENDPOINT: "https://script.google.com/macros/s/AKfyc.../exec",
  SURVEY_URL: "https://docs.google.com/forms/d/e/1FAIpQLSeFWZ.../viewform",
```

If either is still `""`, go back to `STORAGE_SETUP.md` Step 10, then re-copy as above.

### A3 — Create the Netlify site (drag and drop)

1. Go to **[app.netlify.com/drop](https://app.netlify.com/drop)**.
2. Sign up / log in — GitHub, Google or email all work, free tier is plenty.
3. **Drag the `deploy` folder** onto the drop zone. Drag the *folder itself*, not its contents.
4. Wait about 20 seconds. Netlify gives you a URL like:

   ```
   https://cheerful-marzipan-a1b2c3.netlify.app
   ```

**That is your live prototype.** Open it — the app should load.

### A4 — Give it a name people will not be suspicious of

1. **Site configuration** → **Change site name**.
2. Pick something plain, e.g. `gachibowli-food-study`.

   ```
   https://gachibowli-food-study.netlify.app
   ```

Avoid anything with "ownly", "rapido", "fake" or "test" in it. A URL that looks like a real company
misleads people; a URL that says "fake" changes how they behave. Neutral is correct.

### A5 — Test the live site before anyone else sees it

Open the live URL **on your phone**, on mobile data (not wifi), and go all the way through:

search a dish → pick a place → add an item → choose delivery → apply an offer → choose how to pay →
**Place Order** → **I'm open to answering a few more questions** → the QR appears.

Then open your **Google Sheet** → `events` tab → refresh. **Rows should be there.**

✅ If rows arrived from your phone on mobile data, the whole chain works.

> **Nothing arrived?** Add `?qa=1` to the live URL and look at the black bar at the bottom. It shows
> `sent=` and `queued=`. If `queued` keeps climbing and `sent` stays at 0, the `ENDPOINT` is wrong —
> redo `STORAGE_SETUP.md` Steps 6–10 and re-copy to `deploy/`.

### A6 — Updating the site later

Any time you change the prototype:

```bash
cp fake_door.html deploy/index.html
```

Then **Deploys** → drag the `deploy` folder onto the page again. The URL stays the same.

---

# PART B · Turn on the metrics feed

The collector is write-only by default — that is what makes it safe to put in a public page. To
read the data back into a dashboard you switch reading on with a key that only you hold.

### B1 — Invent a read key

Any long random string. For example:

```
ownly-gachi-7Kq2mR8vXtL4
```

Write it down. It is a password.

### B2 — Put it in the Apps Script

1. Open your Sheet → **Extensions** → **Apps Script**.
2. **Ctrl+F** / **Cmd+F** for `READ_KEY`. You will find:

   ```javascript
   var READ_KEY = 'CHANGE-ME-TO-A-LONG-RANDOM-STRING';
   ```

3. Replace the text between the quotes with your key:

   ```javascript
   var READ_KEY = 'ownly-gachi-7Kq2mR8vXtL4';
   ```

4. **Ctrl+S** / **Cmd+S** to save.

### B3 — Redeploy — this step is the one everyone forgets

**Saving does not update the live URL.**

**Deploy** → **Manage deployments** → click the **✏️ pencil** → under *Version* choose
**New version** → **Deploy**.

The `/exec` URL does not change.

### B4 — Never put this key in the prototype

`READ_KEY` goes in **two places only**: the Apps Script, and the metrics page on your own laptop.

It must **never** appear in `fake_door.html` or `deploy/index.html`. Those are public. Anyone with
the read key can download every response.

---

# PART C · Watch the numbers

### C1 — Open the dashboard

Open **`metrics.html`** from this folder **on your own computer**. Just double-click it — no server,
no internet needed for the page itself.

**Do not upload `metrics.html` to Netlify.** Keep it local.

### C2 — Connect it

At the top there are two boxes:

| Box | What to paste |
|---|---|
| First | Your `/exec` URL (same one as `ENDPOINT`) |
| Second | Your `READ_KEY` from B1 |

Click **Load**.

They are saved **in your browser only**, never in any file. **Forget** clears them.

### C3 — If Load does not work, use the CSV instead

Google sometimes blocks a browser reading Apps Script directly. It is not worth fighting:

1. Google Sheet → **`events`** tab → **File** → **Download** → **Comma Separated Values (.csv)**.
2. Drag that file onto the dashed box in `metrics.html`.

Identical dashboard, no network at all. Repeat whenever you want fresh numbers.

### C4 — What you get

| Section | What it shows |
|---|---|
| **Four tiles** | Participants · how many carried a basket to checkout · median basket · how many hit a dead search |
| **Funnel** | Every step with its share and confidence interval — the biggest drop is where to look |
| **Three demand curves** | Paying to save 17 min · money later vs ₹100 now · paying for a refund guarantee. Each price was randomised per participant, so these are curves, not single numbers |
| **What kind of food / place** | Cuisine searched for · **local vs chain** · which search box they reached for first |
| **Searches that found nothing** | The dish list and the place list. **This is the operational output** |
| **Every question** | Each in-journey question with its distribution |

Every chart has a **Show as a table** toggle underneath, and the page follows your system light/dark
setting with a manual override.

Test rows (`?qa=1`) and bot traffic are excluded automatically, and the header tells you how many
were dropped.

### C5 — The deeper statistics

The dashboard is for watching. For the write-up use the Python script, which does the exact tests
(Wilson intervals, Fisher exact, Newcombe differences, the decision rules):

```bash
python3 analyse_results.py events.csv
```

---

# PART D · Sharing it and getting responses

### D1 — What to send

Send the **plain URL**, nothing appended:

```
https://gachibowli-food-study.netlify.app
```

**Never send a link with `?qa=1` or `?variant=`.** Those mark the session as a test and the data is
thrown away.

### D2 — Track where people came from

Add `?source=` and the dashboard can split by channel:

| Channel | Link to send |
|---|---|
| WhatsApp | `...netlify.app/?source=whatsapp` |
| Instagram | `...netlify.app/?source=instagram` |
| In person | `...netlify.app/?source=inperson` |
| Campus group | `...netlify.app/?source=campus` |

Everything else is recorded identically; only the label changes.

### D3 — What to say when you share it

Do not explain what is being measured — that changes what people do. This is enough:

> Doing a short study on how people in Gachibowli order food. Takes about 5 minutes on your phone,
> nothing to sign up for, no payment details. It tells you at the end what it was for.
> [link]

**Do not say:** "help me test my app", "tell me if you'd use this", "pretend to order something".
Each of those tells people what answer you want.

### D4 — Your own testing links

| Purpose | Link |
|---|---|
| Real participant | `.../` |
| See the facilitator bar | `.../?qa=1` |
| Force the discount arm | `.../?variant=discount&qa=1` |
| Force the assortment arm | `.../?variant=restaurants&qa=1` |
| Force a delivery price | `.../?qa=1&rl=35` |
| Force a wallet amount | `.../?qa=1&w=200` |
| Force a protection price | `.../?qa=1&p=19` |

### D5 — How many people you need

The design is written for about **40**. Below roughly 30 the demand curves have cells of 5 or fewer
and the dashboard will say so with an orange "directional only" tag. Take that seriously — it means
the shape is suggestive and the number is not.

---

# What gets recorded

Everything a participant does, as it happens:

| | |
|---|---|
| **Every screen** | reached, and in what order |
| **Every tap** | offers, filters, categories, restaurant cards, bottom nav, back buttons |
| **Every search** | both boxes, **including abandoned ones** — logged on a pause, with how many results it found |
| **Every choice** | dish, place, menu item, quantity, delivery, offer, payment model |
| **Every answer** | all twelve in-journey questions, plus how long each took |
| **The randomised prices** | so take-up can be read as a curve |
| **Timings** | time to first tap, time on each step, total session |

**Never recorded:** name, phone, email, address, location, IP, or any payment detail. The prototype
has no field that could collect them. Free text is scrubbed of anything resembling an email or phone
number twice — in the browser, and again in the collector.

**If the network drops**, events queue in the phone's own storage and are re-sent when signal
returns, when the tab regains focus, and every 15 seconds. A participant who walks through a dead
spot still delivers a complete session.

---

# Troubleshooting

| What you see | Fix |
|---|---|
| Site loads but no rows in the Sheet | `ENDPOINT` missing from `deploy/index.html` — re-copy from `fake_door.html` |
| QA bar shows `queued` climbing, `sent=0` | Wrong `/exec` URL, or the deployment was never updated to a New version |
| Dashboard: "That read key was rejected" | `READ_KEY` in the script does not match what you typed, or you skipped **B3** |
| Dashboard: "Reading is off" | `READ_KEY` is still the default placeholder |
| Dashboard cannot reach the endpoint | Use the CSV drop instead (**C3**) — same result |
| QR does not appear at the end | `SURVEY_URL` missing from `deploy/index.html` |
| Netlify shows a file list, not the app | You dragged the *contents*; drag the `deploy` **folder** |
| Changes not showing on the live site | You edited `fake_door.html` but did not re-copy to `deploy/` |
| Rows say `rejected: event_name` | Collector is older than the prototype — redeploy as **New version** |

---

# Before you send it to anyone

- [ ] `deploy/index.html` has both `ENDPOINT` and `SURVEY_URL` filled in
- [ ] Walked the whole thing on a phone, on mobile data
- [ ] Rows appeared in the `events` tab
- [ ] The QR opened the survey when scanned
- [ ] `READ_KEY` set, and **redeployed as a New version**
- [ ] `metrics.html` loads and shows your test run
- [ ] Test rows deleted from the Sheet
- [ ] Site name has no "ownly", "rapido", "fake" or "test" in it
- [ ] `metrics.html`, the archives and the design doc are **not** in `deploy/`
