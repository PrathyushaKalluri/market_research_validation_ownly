# Design & motion reference pack

Compiled 26 Sep 2026. URLs HTTP-checked, library versions from the live npm registry.

## 0. The decisions

- **Stack: GSAP 3.15.0 UMD (gsap + ScrollTrigger + Flip) + IntersectionObserver for video + native
  `animation-timeline: view()` behind `@supports`.** Lenis 1.3.26 optional with a kill switch.
  GSAP is the only option with real **pinning**, and every plugin has been free since April 2025.
- **No ES-module CDN imports.** They fail on `file://`, and so does `fetch()` of local JSON. Inline the
  data as `<script type="application/json">` or always serve over `python3 -m http.server`.
- **The pattern that carries a 12-screen research story is not fancy:** one sticky chart + captions
  scrolling past it, each caption setting the chart to state *N*. Everything else is garnish.
- **Budget the "wow" to three moments**, not twelve: the hero scroll-scrub, the scattered→sorted photo
  sort (screen 09), and one count-up wall.
- **Vendor the libraries locally before presenting.** Venue Wi-Fi is the number one cause of a dead demo.

## 1. References worth stealing from

**Structure (data journalism)**
| Site | Steal |
|---|---|
| pudding.cool/2017/03/film-dialogue | The canonical sticky-chart + scrolling-captions template. Same marks re-sorted per caption. **Use for screens 05–08.** |
| pudding.cool/2025/11/democracy | Progressive highlighting: don't draw a new chart, dim everything and light the subset. Click-a-dot-for-a-quote — how to surface our verbatims. |
| pudding.cool/2018/08/pockets | Photographs treated as measured data: identical crop, identical frame, one caption line. **Directly applicable to our 8 firsthand screenshots.** |
| pudding.cool/2026/02/womens-sizing | Grids of small comparative charts with 2-word labels — the model for screen 10. |
| nytimes.com/interactive/2018/03/19/upshot/race-class-white-and-black-men.html | Dots that flow and sort into bins: curved paths, random stagger, **bin labels fade in only after the dots land**. |
| ig.ft.com/coronavirus-chart | One chart, whole screen, annotation *is* the headline. Use for the fake-door conversion result. |
| reuters.com/graphics | Two-column sticky/step layout, and how it collapses to one column with the graphic sticky at top. Copy the breakpoint behaviour. |
| nytimes.com/projects/2012/snow-fall | Chapter title cards: full bleed, one oversized line, nothing else. Use as act dividers. Note how little motion it has. |

**Craft (award sites)** — lusion.co (easing: nothing linear, nothing bouncy) · basement.studio (14px label → 120px display in one viewport) · obys.agency (one hot accent on neutral ground — our coral on cream) · cuberto.com (section entry cascade: headline mask 0.0s → rule 0.15s → body 0.3s → visual 0.4s) · igloo.inc (pacing only, not the WebGL).

**Information architecture** — press.stripe.com (warm paper ground done well; ~62–68ch measure) · a16zcrypto.com/state-of-crypto (sticky section index + downloadable PDF) · bain.com/insights/topics/technology-report (**numbered exhibits — "Figure 3:" costs nothing and makes research look rigorous**) · apple.com/airpods-pro (one claim per screen, number as hero).

**Galleries:** godly.website · awwwards.com/websites/scrolling · thefwa.com · siteinspire.com

## 2. Techniques — when, and the failure mode

| Technique | Use for | Failure mode | Guardrail |
|---|---|---|---|
| **Pinned section** | The 2–4 scenes where one visual persists across several claims | Pins measure layout at creation; late fonts/images offset every pin. Ancestor `overflow:hidden`/`transform` breaks `position:fixed` | `document.fonts.ready` + `window.load` → `ScrollTrigger.refresh()`. Explicit image dimensions. **Max 3 pins.** |
| **Scroll-scrub** | Where the audience should feel they drive the change | Scrubbing layout properties stutters on a projector; scrubbed text is unreadable | Transform/opacity only. `scrub: 0.5–1`, never `true` |
| **Step-triggered chart states** | **80% of our story** — highest value per hour | Scrolling back leaves the chart in the wrong state | One idempotent `renderChart(state)` called from `onEnter` **and** `onEnterBack` |
| **Horizontal panels** | Exactly one sequential thing (the order journey) | Trackpad users jump the track; doubles responsive work; desyncs from narration | Allowed once. Never for a chart |
| **Scatter → sorted grid** | Screen 09 — it enacts our methodology | DOM reparenting inside a pin invalidates measurements; >60 items drops to 15fps; random rotation looks like Pinterest | **Never move the DOM.** Author the final grid, store scatter offsets, animate `x/y/rotation → 0`. Cap ±12°, cap ~36 items, labels last |
| **Count-ups** | 3–6 headline figures max | Digit width shoves layout; counting everything means nothing matters | `tabular-nums` + fixed min-width, 1.2–1.6s, `once:true`, `toLocaleString('en-IN')` |
| **SVG draw-on** | One or two paths | 12 series becomes spaghetti | Axis exists before the line arrives |
| **Masked reveals** | Headlines only — cheapest professional tell | `clip-path` is costlier than a wrapper; masked text is invisible without JS | `overflow:hidden` wrapper + `translateY`; visible state is the default |

**Overrated, skip:** scroll-scrubbed image sequences (the Apple effect — 20–60MB, zero analytical content, dies on a mirrored projector), WebGL heroes, custom cursors (invisible from row 5), per-character scrambles on every heading, parallax on everything, full-page scroll-snapping (fights the presenter).

## 3. Boot code

```html
<script src="vendor/gsap.min.js"></script>
<script src="vendor/ScrollTrigger.min.js"></script>
<script src="vendor/Flip.min.js"></script>
<!-- CDN equivalents: https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/{gsap,ScrollTrigger,Flip}.min.js -->
```

```js
gsap.registerPlugin(ScrollTrigger, Flip);
const REDUCE   = matchMedia('(prefers-reduced-motion: reduce)').matches;
const NOSMOOTH = new URLSearchParams(location.search).has('nosmooth');  // presenter kill switch

if (!REDUCE && !NOSMOOTH) {                       // Lenis is the first thing to cut if the room stutters
  const lenis = new Lenis({ duration: 1.1, lerp: 0.12, smoothWheel: true, autoRaf: false });
  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add(t => lenis.raf(t * 1000));
  gsap.ticker.lagSmoothing(0);
  document.querySelectorAll('a[href^="#"]').forEach(a =>
    a.addEventListener('click', e => { e.preventDefault(); lenis.scrollTo(a.getAttribute('href')); }));
}

// The two most important lines in the file
window.addEventListener('load', () => ScrollTrigger.refresh());
document.fonts.ready.then(() => ScrollTrigger.refresh());
```

**Pin + scrub, with responsive and reduced-motion in one construct:**
```js
gsap.matchMedia().add({ isDesktop:'(min-width: 900px)', reduce:'(prefers-reduced-motion: reduce)' }, ctx => {
  if (!ctx.conditions.isDesktop || ctx.conditions.reduce) return;   // mobile + reduced get the static layout
  gsap.timeline({ scrollTrigger:{ trigger:'#scene-funnel', start:'top top', end:'+=2200',
      pin:true, scrub:0.6, anticipatePin:1, invalidateOnRefresh:true }})
    .from('.funnel__step',  { scaleY:0, transformOrigin:'50% 100%', stagger:0.25, ease:'none' })
    .from('.funnel__label', { autoAlpha:0, stagger:0.25, ease:'none' }, 0.1);
});
```

**Chart reveal on enter:**
```js
gsap.utils.toArray('.chart').forEach(chart => {
  const bars = chart.querySelectorAll('[data-bar]');
  gsap.set(bars, { scaleX:0, transformOrigin:'0% 50%' });
  ScrollTrigger.create({ trigger:chart, start:'top 75%', once:true,
    onEnter:() => gsap.to(bars,{ scaleX:1, duration:0.9, ease:'power3.out', stagger:0.06 }) });
});
```
```css
svg [data-bar]{ transform-box: fill-box; transform-origin: 0% 50%; }
```

**Count-up (Indian digit grouping):**
```js
const nf = d => new Intl.NumberFormat('en-IN',{minimumFractionDigits:d,maximumFractionDigits:d});
document.querySelectorAll('[data-count]').forEach(el => {
  const end = parseFloat(el.dataset.count), fmt = nf(parseInt(el.dataset.decimals||'0',10));
  el.textContent = fmt.format(REDUCE ? end : 0);
  if (REDUCE) return;
  const o = { v:0 };
  ScrollTrigger.create({ trigger:el, start:'top 85%', once:true,
    onEnter:() => gsap.to(o,{ v:end, duration:1.4, ease:'power2.out',
      onUpdate:() => { el.textContent = fmt.format(o.v); } }) });
});
```

**Scatter → sorted (no-reflow version — use this one):** author the cards already inside their bins, then
```js
const scatter = cards.map(() => ({ x:gsap.utils.random(-380,380,1), y:gsap.utils.random(-260,260,1), r:gsap.utils.random(-12,12,1) }));
cards.forEach((c,i) => gsap.set(c,{ x:scatter[i].x, y:scatter[i].y, rotation:scatter[i].r }));
gsap.set(labels,{ autoAlpha:0, y:8 });
ScrollTrigger.create({ trigger:'.sorter', start:'top top', end:'+=1400', pin:true,
  onEnter:() => {
    gsap.to(cards, { x:0, y:0, rotation:0, duration:1.0, ease:'power3.inOut', stagger:{ each:0.035, from:'random' }});
    gsap.to(labels,{ autoAlpha:1, y:0, duration:0.5, delay:0.85, stagger:0.08 });   // labels land last
  }});
```

**Auto-play on section entry (screen 08's walkthrough):**
```js
const mediaIO = new IntersectionObserver(es => es.forEach(e => {
  const v = e.target; if (e.isIntersecting) { const p = v.play(); if (p) p.catch(()=>{}); } else v.pause();
}), { threshold:0.35, rootMargin:'0px 0px -10% 0px' });
document.querySelectorAll('video[data-autoplay]').forEach(v => {
  v.muted = true; v.playsInline = true;                  // required for autoplay
  if (REDUCE) { v.removeAttribute('loop'); return; }      // leave the poster frame
  mediaIO.observe(v);
});
```

**Free native reveals (off main thread), behind a feature query:**
```css
@supports (animation-timeline: view()) { @media (prefers-reduced-motion: no-preference) {
  .reveal { animation: reveal-up linear both; animation-timeline: view(); animation-range: entry 10% cover 35%; }
}}
```

## 4. Typography, grid, palette

**Recommended pairing — "editorial heat":** display **Instrument Serif** (incl. italic, for verbatim
pull-quotes) · UI **Inter Tight** · data **JetBrains Mono**.
```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter+Tight:wght@400..700&family=JetBrains+Mono:wght@400..700&display=swap">
```
Alternates: **Archivo** variable (`wdth 62–125`) + IBM Plex Mono — one family, fewest bytes, most disciplined;
or Bricolage Grotesque + DM Sans + Geist Mono — friendlier, reads younger.

**Fluid scale** (utopia.fyi), `--step--2` … `--step-6`; body `--step-0` at `clamp(1rem, 0.93rem + 0.36vw, 1.2rem)`,
scene headline `--step-5`, stat hero `--step-6` at `clamp(3.82rem, 2.57rem + 6.23vw, 7.24rem)`.
**The jump from a `--step--1` label to a `--step-6` stat inside one viewport is what makes it look designed.**
Max 3 sizes per screen. `line-height:0.94` and `letter-spacing:-0.02em` on display; `max-width:62ch` on body.

**Grid:** `min-height:100svh` (not `vh` — mobile chrome), 12 columns, `gap: clamp(16px,2.4vw,32px)`,
page margin `clamp(20px,6vw,112px)`, chart well `1 / span 8`, caption rail `10 / span 3`, both full width under 900px.
**Spacing:** a 4px rhythm — `4 8 12 16 24 32 48 64 96 128 192`. Within a block 12–24; between blocks 48–64; between scenes 96–192. Never a bare `margin-top: 37px`.

**Palette note that matters for charts:** a mono-red palette cannot encode more than one series.
ink `#1A1614` · cream `#FBF4EC` · paper `#FFFFFF` · coral `#FF4438` (fills, accents) ·
brick `#B3261E` (**text** on cream — pure coral fails contrast below ~20px) · deep teal `#0F6E6B`
(competitor/baseline series) · warm grey `#A79C92` (context, inactive). Never encode a third category in a lighter red.

## 5. What kills these sites in a room

1. **Vendor everything** into `/vendor/` and `/fonts/` the day before. Venue Wi-Fi is the single most common failure.
2. **Self-host fonts**, `font-display: swap`, max 2 display weights + 1 variable body + 1 mono. A font flash on a projected slide is the most visible amateur tell.
3. **`ScrollTrigger.refresh()` after `load` and after `fonts.ready`** — fixes ~90% of "my pins are offset".
4. **Explicit `width`/`height` on every image**, `loading="lazy"` below the second scene. Re-encode the firsthand screenshots to WebP ~1400px.
5. **Budget:** first scene ≤ 1.5MB, whole site ≤ 12MB, checked on throttled Fast 4G.
6. **Animate transform and opacity only.** Never `filter: blur()` — catastrophic on integrated GPUs.
7. **Projectors mirror at 30Hz, often 1280×720.** Test at that size, at 125% zoom, **on battery** (GPUs throttle).
8. **`prefers-reduced-motion` must give a complete page**, not a broken one. The un-animated state is the visible state, so a JS failure degrades gracefully.
9. **Never scroll-jack.** Space/PageDown/arrows must page the document. Ship `?nosmooth=1`.
10. **Video:** H.264, ≤1600px, ≤3MB, `muted playsinline loop preload="metadata"` + poster, paused off-screen. Prefer a 4s loop or animated SVG over a 30s video.
11. **Record a 90-second screen capture of the full scroll** and keep the MP4 on the presenting machine. If the browser dies you narrate over the video. Ten minutes of work, only insurance that always works.

**Pre-flight, 24h before:** Lighthouse ≥90 on Fast 4G · no layout shift on font swap · pins correct after hard reload with cache disabled · reduced-motion on → page still complete · 1280×720 at 125% zoom · **Wi-Fi off → site still loads** · keyboard PageDown works · backup MP4 on the desktop.
