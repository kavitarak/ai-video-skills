---
name: casefile-documentary-reel
description: "Make a vertical case-file documentary explainer reel on any topic: aged notebook paper, Anton headlines, red-ink underlines/circles, stamps, torn cards, typewriter documents, counters, built with HyperFrames."
---

# Case-file documentary reel

A 9:16 explainer that tells one surprising true story as if you were flipping through an
investigator's case file: every beat is a "page" of aged notebook paper with a mono header
("THE LAW · FIG. 5.2"), one big condensed headline, and one piece of red-ink evidence being
drawn on it (underline, circle, strike, stamp, counter, bar, typed document). Hindi voiceover
carries the story; the screen shows the short English evidence phrase for each beat.

The look only works if every number is true. The format promises *documents*, so a wrong
figure or an invented letter reads as a lie. Research first, cite sources, and never fake a
real person's letter, signature, or a newspaper front page — show the real fact as a ledger,
a chart, or a quoted line with its source instead.

## 0. Talk to the user (Hindi/Hinglish if they write that way)
Ask only what you can't decide: target length (default 60–90 s; the reference was 170 s),
and whether they will send a voiceover. Then work.

## 1. Research → story
1. Search the web for the topic. Collect 8–15 hard facts: dates, money then vs now, counts,
   names, the one rule/decision/person that changed everything, and what's at stake next.
   Keep source + date for each. Prefer primary/official sources.
2. Shape it into this arc (one beat ≈ 3–6 s, one fact per beat):

| Beat | Purpose | Typical device |
|---|---|---|
| Cold open | Shocking "then" number with the year | stamp `2001` + torn card `$33 A DAY`, rupee conversion |
| Contrast | Then vs now | bar chart, red smaller bar, counter |
| Hook | "One man / one line / one rule did this" | torn card headline, underline |
| Problem | Why it was hard | icon tiles, item list being crossed out, calendar/pill grid |
| Setting | Where it hurt | sepia photo plate + torn caption card |
| Protagonist | Who acted, when | date stamp, polaroid with red name tag (only with a real photo the user gives) |
| Turning point | The offer / decision | typed ledger or quote, underline the key number |
| Mechanism | How it was possible | `X = Y` definition page, marker highlight, strike old → new, flowchart tiles |
| Consequence | Scale of impact | big counter, "x became y", bar chart of prices dropping |
| Twist | What changed later / what's at risk | stamp a later year over old text, strikes in a law page, `REFUSED` stamp |
| Close | Open question | `WILL ONE LINE BE ENOUGH?` with a red `?` |

3. Write the **Hindi voiceover script** as short spoken lines (5–12 words each), and next to
   each line the **on-screen English phrase** (2–6 words, uppercase). Screen text never
   repeats the whole sentence — it is the evidence label. Show the script to the user.

## 2. Voiceover — pick the route that exists
This machine may have no TTS. Check, don't assume:
- **User recording (best):** they record the script (phone, or any TTS app such as CapCut
  text-to-speech / ElevenLabs) and attach it. Transcribe it for word timings (below) and time
  every beat to the line it illustrates.
- **TTS available:** if `npx hyperframes media-use resolve --doctor` reports a working TTS
  provider (HeyGen sign-in or Gemini key), generate the Hindi narration through media-use.
- **No voice:** build a text-led cut. Time each beat by reading speed: 0.6 s + 0.3 s per
  on-screen word, minimum 3 s, and tell the user they can lay the voice over later.

Transcribing a recording when Hugging Face is blocked: the Whisper-small CTranslate2 model is
mirrored on npm in four parts.
```bash
mkdir -p ~/models/dl && cd ~/models/dl
for i in 0 1 2 3; do npm pack @skillninja/shortmovie-telop-model-p$i --silent; done
for f in *.tgz; do mkdir -p x/${f%.tgz}; tar -xzf $f -C x/${f%.tgz}; done
mkdir -p ../whisper-small && cp x/*p0*/package/{tokenizer.json,vocabulary.json,config.json,preprocessor_config.json} ../whisper-small/
cat x/*p0*/package/model.bin.part0 x/*p1*/package/model.bin.part1 x/*p2*/package/model.bin.part2 x/*p3*/package/model.bin.part3 > ../whisper-small/model.bin
pip install --break-system-packages -q faster-whisper
```
Load audio yourself (16 kHz mono wav → numpy) and pass the array to
`WhisperModel(...).transcribe(audio, language="hi", word_timestamps=True)`; passing a path can
fail on PyAV version mismatches.

## 3. Build the project
If `hyperframes` isn't on PATH, install it first (`npm i -g hyperframes`, or run every command
below as `npx hyperframes …`). Rendering needs Chrome: if it complains, set
`HYPERFRAMES_BROWSER_PATH` to an installed Chrome/Chromium (Linux: `/usr/bin/google-chrome`, macOS:
`/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`, Windows:
`C:\Program Files\Google\Chrome\Application\chrome.exe`).
```bash
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1
hyperframes init <slug> --non-interactive --skip-skills --resolution portrait --example blank
cd <slug> && mkdir -p assets/fonts assets/vendor assets/sfx assets/img assets/voice compositions
```
Offline-safe assets (the CDN and Google Fonts are often unreachable):
- GSAP: `npm pack gsap@3.15.0`, copy `package/dist/gsap.min.js` to `assets/vendor/`. Never
  leave the jsdelivr `<script>`; the render fails without network.
- Fonts: `npm pack @fontsource/anton @fontsource/special-elite`, copy
  `files/anton-latin-400-normal.woff2` → `assets/fonts/anton.woff2` and
  `files/special-elite-latin-400-normal.woff2` → `assets/fonts/special-elite.woff2`.
  Space Mono is bundled with HyperFrames.
- SFX: copy from the HyperFrames skills checkout (`skills/media-use/audio/assets/sfx/`):
  `impact-bass-2` (stamp), `typing` (typed document), `key-press` (counter), `whoosh` /
  `whoosh-short` (page change, strikes), `pop` / `click-soft` (cards, ticks), `riser` (build
  into the turning point). If HyperFrames isn't cloned, `git clone --depth 1
  https://github.com/heygen-com/hyperframes` (GitHub is reachable).
- Photos: the reference uses sepia archive stills (pharmacy shelves, a hospital ward, a
  factory). Use images the user supplies; never put a real public figure's photo in from the
  web. Without photos, stay on paper pages — the style holds up without them.

Write the two kit files below verbatim into `assets/`, then one sub-composition per beat.

### `assets/casefile.css`
```css
/* Case-file documentary kit — aged notebook paper, condensed headlines, red ink. */
@font-face { font-family: "Anton"; src: url("fonts/anton.woff2") format("woff2"); font-weight: 400; }
@font-face { font-family: "Special Elite"; src: url("fonts/special-elite.woff2") format("woff2"); font-weight: 400; }

:root {
  --paper: #d3bd8f;
  --paper-hi: #e8d7ad;
  --card: #e9ddbe;
  --ink: #2a2119;
  --ink-soft: #5b4c3c;
  --red: #a3291f;
  --marker: rgba(203, 132, 52, 0.85);
  --rule: rgba(80, 60, 40, 0.13);
  --display: "Anton", "League Gothic", "Oswald", sans-serif;
  --mono: "Space Mono", "IBM Plex Mono", monospace;
  --type: "Special Elite", "Space Mono", monospace;
}

/* ---------- persistent paper ---------- */
#paper { position: absolute; inset: 0; overflow: hidden; background:
    radial-gradient(ellipse 85% 70% at 50% 45%, var(--paper-hi) 0%, var(--paper) 60%, #b09468 100%); }
#paper .lines { position: absolute; inset: 0;
  background: repeating-linear-gradient(180deg, transparent 0 63px, var(--rule) 63px 65px); }
#paper .margin { position: absolute; top: 0; bottom: 0; left: 118px; width: 3px; background: rgba(179, 51, 43, 0.35); }
#paper .holes { position: absolute; top: 0; bottom: 0; left: 30px; width: 40px;
  background: radial-gradient(circle at 20px 50%, rgba(70, 52, 34, 0.45) 0 9px, transparent 10px) 0 0 / 40px 330px repeat-y; }
#paper .fold { position: absolute; top: 0; bottom: 0; left: 50%; width: 2px; background: linear-gradient(90deg, rgba(0,0,0,.06), rgba(255,255,255,.12)); }
#paper .corner { position: absolute; top: 0; right: 0; width: 70px; height: 70px;
  background: linear-gradient(225deg, #8f7f5d 0 49%, #efe4c8 50% 100%); box-shadow: -4px 4px 8px rgba(0,0,0,.18); }
#paper .grain { position: absolute; inset: -40px; opacity: 0.13; mix-blend-mode: multiply;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3' seed='7'/><feColorMatrix values='0 0 0 0 0.3  0 0 0 0 0.22  0 0 0 0 0.12  0 0 0 0.9 0'/></filter><rect width='240' height='240' filter='url(%23n)'/></svg>"); }
#paper .vig { position: absolute; inset: 0; background: radial-gradient(ellipse 80% 65% at 50% 48%, transparent 55%, rgba(60, 40, 20, 0.35) 100%); }

/* ---------- scene scaffolding ---------- */
.scene { position: absolute; inset: 0; }
.hdr { position: absolute; top: 200px; left: 150px; right: 90px; display: flex; justify-content: space-between; align-items: baseline;
  font-family: var(--mono); font-weight: 700; font-size: 28px; letter-spacing: 7px; color: var(--ink-soft); text-transform: uppercase;
  padding-bottom: 14px; border-bottom: 3px solid var(--ink); }
.hdr .fig { color: var(--red); letter-spacing: 3px; }
.stack { position: absolute; left: 150px; right: 90px; top: 300px; bottom: 360px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; gap: 26px; }
.kicker { font-family: var(--mono); font-weight: 700; font-size: 31px; letter-spacing: 9px; color: var(--ink-soft); text-transform: uppercase; }
.h1 { font-family: var(--display); font-size: 168px; line-height: 0.98; color: var(--ink); text-transform: uppercase; letter-spacing: 1px; }
.h2 { font-family: var(--display); font-size: 118px; line-height: 1.02; color: var(--ink); text-transform: uppercase; }
.h3 { font-family: var(--display); font-size: 80px; line-height: 1.05; color: var(--ink); text-transform: uppercase; }
.red { color: var(--red); }
.small { font-family: var(--mono); font-weight: 700; font-size: 30px; letter-spacing: 3px; color: var(--ink-soft); text-transform: uppercase; }
.num { font-family: var(--display); font-size: 270px; line-height: 0.95; color: var(--ink); font-variant-numeric: tabular-nums; }
.mark { position: relative; display: inline-block; padding: 0 12px; }
.mark > .hl { position: absolute; left: 0; right: 0; top: 14%; bottom: 8%; background: var(--marker); transform-origin: 0 50%; z-index: -1; }
.mark { isolation: isolate; }

/* torn paper card (edges are cut by cf.torn) */
.torn { position: relative; background: var(--card); padding: 34px 44px; filter: drop-shadow(0 14px 18px rgba(40, 25, 10, 0.35)); }
.torn::before { content: ""; position: absolute; inset: 0; background:
  linear-gradient(180deg, rgba(255,255,255,.25), rgba(0,0,0,.05)); pointer-events: none; }

/* rubber stamp */
.stamp { display: inline-block; font-family: var(--display); font-size: 170px; line-height: 1; color: var(--red); letter-spacing: 4px;
  padding: 10px 34px 16px; border: 9px double var(--red); border-radius: 10px; transform: rotate(-8deg); mix-blend-mode: multiply;
  -webkit-mask-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='m'><feTurbulence type='fractalNoise' baseFrequency='0.7' numOctaves='2' seed='3'/><feColorMatrix values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 -2.2 1.7'/></filter><rect width='300' height='300' filter='url(%23m)'/></svg>");
  mask-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='m'><feTurbulence type='fractalNoise' baseFrequency='0.7' numOctaves='2' seed='3'/><feColorMatrix values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 -2.2 1.7'/></filter><rect width='300' height='300' filter='url(%23m)'/></svg>"); }

/* typewritten letter */
.letter { position: absolute; left: 140px; right: 110px; background: #efe5c9; padding: 56px 56px 70px; transform: rotate(-1.5deg);
  box-shadow: 0 24px 40px rgba(40, 25, 10, 0.35); }
.letter .lt-head { display: flex; justify-content: space-between; font-family: var(--mono); font-size: 28px; letter-spacing: 3px; color: var(--ink-soft); }
.letter .lt-org { font-family: var(--display); font-size: 96px; color: var(--ink); margin-top: 26px; text-transform: uppercase; }
.letter .lt-sub { font-family: var(--mono); font-size: 28px; letter-spacing: 8px; color: var(--ink-soft); padding-bottom: 18px; border-bottom: 3px solid var(--ink); }
.letter .lt-body { font-family: var(--type); font-size: 44px; line-height: 1.55; color: var(--ink); margin-top: 30px; white-space: pre-wrap; }

/* photo plate: sepia archival still */
.plate { position: absolute; inset: 0; overflow: hidden; }
.plate img { width: 100%; height: 100%; object-fit: cover; filter: sepia(0.85) contrast(1.05) brightness(0.9) saturate(0.8); }
.plate::after { content: ""; position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 45%, transparent 45%, rgba(30, 18, 6, 0.55) 100%); }

/* bar chart */
.bars { position: relative; width: 100%; }
.bar-row { margin: 18px 0; }
.bar-lbl { font-family: var(--mono); font-weight: 700; font-size: 28px; letter-spacing: 4px; color: var(--ink-soft); text-align: left; margin-bottom: 8px; }
.bar { height: 64px; background: var(--ink); transform-origin: 0 50%; }
.bar.red { background: var(--red); }

/* icon tile (flowchart / steps) */
.tile { display: flex; align-items: center; justify-content: center; min-width: 120px; padding: 20px 28px; border: 5px solid var(--ink);
  font-family: var(--display); font-size: 52px; color: var(--ink); background: rgba(255, 250, 235, 0.35); text-transform: uppercase; }
.arrow { font-family: var(--display); font-size: 54px; color: var(--ink-soft); }

/* polaroid portrait */
.polaroid { background: #f2ead6; padding: 22px 22px 90px; box-shadow: 0 20px 34px rgba(40, 25, 10, 0.4); transform: rotate(-3deg); position: relative; }
.polaroid img { display: block; width: 640px; height: 700px; object-fit: cover; filter: sepia(0.9) contrast(1.1) grayscale(0.3); }
.polaroid .tag { position: absolute; left: 22px; bottom: 26px; background: var(--red); color: #fff; font-family: var(--display); font-size: 40px; padding: 4px 18px; }

/* ink overlays created by helpers */
.ink { position: absolute; pointer-events: none; overflow: visible; }
```

### `assets/casefile.js`
```js
/* Case-file documentary kit: deterministic GSAP helpers. Every helper takes the
   scene's own timeline `tl` and a time `t` local to that scene. No Math.random. */
(function () {
  const RED = "#a3291f";
  // seeded PRNG so torn edges / wobbles are identical on every render
  function rng(seed) { let s = seed >>> 0 || 1; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }
  const $ = (sel, root) => (typeof sel === "string" ? (root || document).querySelector(sel) : sel);

  // Cut a ragged paper edge into an element via clip-path.
  function torn(sel, seed = 1, depth = 10) {
    const el = $(sel); if (!el) return; const r = rng(seed); const pts = []; const n = 28;
    for (let i = 0; i <= n; i++) pts.push(`${(i / n) * 100}% ${r() * depth}px`);
    for (let i = 0; i <= n; i++) pts.push(`calc(100% - ${r() * depth}px) ${(i / n) * 100}%`);
    for (let i = n; i >= 0; i--) pts.push(`${(i / n) * 100}% calc(100% - ${r() * depth}px)`);
    for (let i = n; i >= 0; i--) pts.push(`${r() * depth}px ${(i / n) * 100}%`);
    el.style.clipPath = `polygon(${pts.join(",")})`;
  }

  // SVG ink drawn INSIDE the element in a 0..1000 x 0..100 box that stretches with it,
  // so marks stay aligned however fonts load or text changes. pathLength=1 lets the
  // draw-on tween run 1 -> 0 regardless of size.
  function ink(el, box, d, color, width) {
    const ns = "http://www.w3.org/2000/svg";
    if (getComputedStyle(el).position === "static") el.style.position = "relative";
    if (getComputedStyle(el).display === "inline") el.style.display = "inline-block";
    const svg = document.createElementNS(ns, "svg");
    svg.setAttribute("class", "ink"); svg.setAttribute("viewBox", "0 0 1000 100"); svg.setAttribute("preserveAspectRatio", "none");
    Object.assign(svg.style, box, { zIndex: 5 });
    const p = document.createElementNS(ns, "path");
    p.setAttribute("d", d); p.setAttribute("fill", "none"); p.setAttribute("stroke", color || RED);
    p.setAttribute("stroke-width", width || 7); p.setAttribute("vector-effect", "non-scaling-stroke");
    p.setAttribute("stroke-linecap", "round"); p.setAttribute("stroke-linejoin", "round"); p.setAttribute("pathLength", "1");
    p.style.strokeDasharray = "1"; p.style.strokeDashoffset = "1";
    svg.appendChild(p); el.appendChild(svg); return p;
  }

  // Hand-drawn wavy underline that draws itself.
  function underline(tl, sel, t, o = {}) {
    const el = $(sel); if (!el) return; const r = rng(o.seed || 5);
    let d = "M 5 50"; for (let x = 60; x <= 1000; x += 60) d += ` Q ${x - 30} ${50 + (r() * 70 - 25)} ${x} ${50 + (r() * 30 - 15)}`;
    const p = ink(el, { left: "0", right: "0", bottom: "-22px", height: "20px", width: "100%" }, d, o.color, o.width || 7);
    tl.to(p, { strokeDashoffset: 0, duration: o.dur || 0.45, ease: "power2.out" }, t);
  }

  // Hand-drawn loose ellipse around an element.
  function circle(tl, sel, t, o = {}) {
    const el = $(sel); if (!el) return; const pad = o.pad || 26;
    const d = "M 400 4 C 1060 0, 1040 96, 500 97 C -50 98, -40 6, 560 10";
    const p = ink(el, { left: -pad + "px", top: -pad * 0.6 + "px", width: `calc(100% + ${pad * 2}px)`, height: `calc(100% + ${pad * 1.2}px)` }, d, o.color, o.width || 6);
    tl.to(p, { strokeDashoffset: 0, duration: o.dur || 0.6, ease: "power1.inOut" }, t);
  }

  // Red strike-through that draws across text.
  function strike(tl, sel, t, o = {}) {
    const el = $(sel); if (!el) return;
    const p = ink(el, { left: "-8px", top: "0", width: "calc(100% + 16px)", height: "100%" }, "M 4 56 Q 500 44 996 52", o.color, o.width || 8);
    tl.to(p, { strokeDashoffset: 0, duration: o.dur || 0.35, ease: "power2.out" }, t);
    if (o.dim !== false) tl.to(el, { color: o.dimColor || "rgba(42,33,25,.55)", duration: 0.2, ease: "none" }, t + 0.1);
  }

  // Red X over an element (crossing out an item).
  function cross(tl, sel, t, o = {}) {
    const el = $(sel); if (!el) return; const box = { left: "-6px", top: "-6px", width: "calc(100% + 12px)", height: "calc(100% + 12px)" };
    const a = ink(el, box, "M 4 4 L 996 96", o.color, o.width || 7);
    const b = ink(el, box, "M 996 4 L 4 96", o.color, o.width || 7);
    tl.to(a, { strokeDashoffset: 0, duration: 0.14, ease: "power2.out" }, t);
    tl.to(b, { strokeDashoffset: 0, duration: 0.14, ease: "power2.out" }, t + 0.12);
  }

  // Marker highlight sweeping behind a .mark span (needs a child .hl).
  function marker(tl, sel, t, o = {}) {
    const hl = $(sel + " > .hl") || $(sel); if (!hl) return;
    tl.fromTo(hl, { scaleX: 0 }, { scaleX: 1, duration: o.dur || 0.35, ease: "power2.out" }, t);
  }

  // Rubber stamp slam.
  function stamp(tl, sel, t, o = {}) {
    const el = $(sel); if (!el) return; const rot = o.rotation == null ? -8 : o.rotation;
    tl.fromTo(el, { opacity: 0, scale: 2.4, rotation: rot - 10 }, { opacity: 1, scale: 1, rotation: rot, duration: 0.2, ease: "power4.in" }, t);
    tl.to(el, { scale: 1.04, duration: 0.06, ease: "power1.out", yoyo: true, repeat: 1 }, t + 0.2);
  }

  // Typewriter reveal: splits text into spans and reveals them at `cps` chars/sec.
  function type(tl, sel, t, o = {}) {
    const el = $(sel); if (!el) return 0; const cps = o.cps || 28; const text = el.textContent; el.textContent = "";
    const spans = [];
    for (const ch of text) { const s = document.createElement("span"); s.textContent = ch; s.style.opacity = "0"; el.appendChild(s); spans.push(s); }
    spans.forEach((s, i) => tl.set(s, { opacity: 1 }, t + i / cps));
    return text.length / cps; // duration, so callers can place the next beat
  }

  // Number counter. fmt: "en" (1,234,567) | "in" (12,34,567) | fn(n). Writes into a child
  // span so ink marks added to the same element survive. Lays out at the FINAL value.
  function count(tl, sel, t, from, to, dur, o = {}) {
    const el = $(sel); if (!el) return; const dec = o.decimals || 0;
    const fmt = typeof o.fmt === "function" ? o.fmt : (n) => n.toLocaleString(o.fmt === "in" ? "en-IN" : "en-US", { minimumFractionDigits: dec, maximumFractionDigits: dec });
    const pre = o.prefix || "", suf = o.suffix || "";
    const txt = document.createElement("span"); txt.className = "cnt"; el.textContent = ""; el.appendChild(txt);
    const show = (v) => { txt.textContent = pre + fmt(dec ? v : Math.round(v)) + suf; };
    const obj = { v: from }; show(from);
    tl.fromTo(obj, { v: from }, { v: to, duration: dur, ease: o.ease || "power2.out", onUpdate: () => show(obj.v) }, t);
  }

  // Bar grows from the left (scaleX 0 -> 1).
  function bar(tl, sel, t, o = {}) {
    tl.fromTo(sel, { scaleX: 0 }, { scaleX: o.to || 1, duration: o.dur || 0.6, ease: o.ease || "power3.out" }, t);
  }

  // Item lands: small drop with a settle (cards, tiles, notes).
  function land(tl, sel, t, o = {}) {
    tl.fromTo(sel, { opacity: 0, y: o.y == null ? -40 : o.y, rotation: o.from || 0 },
      { opacity: 1, y: 0, rotation: o.rotation || 0, duration: o.dur || 0.3, ease: "back.out(1.6)", stagger: o.stagger || 0 }, t);
  }

  // Slow archival push on a photo plate or the whole scene.
  function push(tl, sel, t, dur, o = {}) {
    tl.fromTo(sel, { scale: o.from || 1.0 }, { scale: o.to || 1.08, duration: dur, ease: "none", transformOrigin: o.origin || "50% 50%" }, t);
  }

  window.cf = { torn, underline, circle, strike, cross, marker, stamp, type, count, bar, land, push };
})();
```

Helper contract — every helper takes the scene's own `tl` and a time local to the scene:
`cf.torn(sel, seed)` ragged card edge · `cf.stamp(tl, sel, t, {rotation})` ·
`cf.underline(tl, sel, t)` · `cf.circle(tl, sel, t, {pad})` · `cf.strike(tl, sel, t)` ·
`cf.cross(tl, sel, t)` · `cf.marker(tl, ".mark-id", t)` (element needs a child `<span class="hl">`) ·
`d = cf.type(tl, sel, t, {cps})` returns its duration · `cf.count(tl, sel, t, from, to, dur, {decimals, fmt:"in"|"en", prefix, suffix})` ·
`cf.bar(tl, sel, t, {to, dur})` · `cf.land(tl, sel|[sels], t, {y, rotation, stagger})` ·
`cf.push(tl, sel, t, dur, {to})` for photo plates. Ink marks are drawn inside the element and
stretch with it, so call them after `type`/`count` on the same element and they stay aligned.

### Root `index.html`
Head loads `assets/casefile.css`, `assets/vendor/gsap.min.js`, `assets/casefile.js` (in that
order). Body: one `#stage` holding the persistent paper and every scene mount, then the
`<audio>` clips (voice first, then SFX).
```html
<div id="root" data-composition-id="main" data-start="0" data-duration="TOTAL" data-width="1080" data-height="1920">
  <div id="stage" style="position:absolute; inset:0; transform-origin:50% 45%">
    <div id="paper"><div class="lines"></div><div class="margin"></div><div class="holes"></div><div class="fold"></div><div class="corner"></div><div class="grain"></div><div class="vig"></div></div>
    <div id="s1" class="clip" data-composition-id="s1" data-composition-src="compositions/s1.html" data-start="0" data-duration="5.8" data-track-index="1" data-width="1080" data-height="1920"></div>
    <!-- s2, s3 … each starting where the previous ends (hard cuts, like the reference) -->
  </div>
  <audio id="vo" class="clip" src="assets/voice/vo.wav" data-start="0" data-duration="TOTAL" data-track-index="9" data-volume="1"></audio>
  <audio id="sfx-stamp1" class="clip" src="assets/sfx/impact-bass-2.mp3" data-start="0.15" data-duration="1.2" data-track-index="10" data-volume="0.45"></audio>
</div>
<script>
  const tl = gsap.timeline({ paused: true });
  // slow archival drift inside each scene, hard reset on every cut
  [0, 5.8 /*, …scene starts */].forEach((t, k, a) => {
    const end = k + 1 < a.length ? a[k + 1] : TOTAL;
    tl.fromTo("#stage", { scale: 1 }, { scale: 1.035, duration: end - t, ease: "none", immediateRender: k === 0 }, t);
  });
  window.__timelines["main"] = tl;
</script>
```

### A scene (`compositions/s1.html`) — the pattern every beat follows
```html
<template>
  <div id="root" data-composition-id="s1" data-width="1080" data-height="1920">
    <div id="s1-scene" class="scene">
    <div class="hdr"><span>India · 2016</span><span class="fig">Fig. 1</span></div>
    <div class="stack">
      <div id="s1-stamp" class="stamp">2016</div>
      <div id="s1-card" class="torn" style="width: 840px; margin-top: 30px;">
        <div class="kicker" style="text-align:left">To send ₹10 online</div>
        <div class="h2" style="text-align:left; margin-top: 10px;">You needed</div>
        <div class="list" style="margin-top: 26px; display:flex; flex-direction:column; gap: 18px; align-items:flex-start;">
          <span id="s1-i1" class="h3">Account number</span>
          <span id="s1-i2" class="h3">IFSC code</span>
          <span id="s1-i3" class="h3">Bank login</span>
          <span id="s1-i4" class="h3">And patience</span>
        </div>
      </div>
    </div>
    </div>
  </div>
  <script>
    const tl = gsap.timeline({ paused: true });
    cf.torn("#s1-card", 11, 12);
    cf.stamp(tl, "#s1-stamp", 0.15);
    cf.land(tl, "#s1-card", 0.55, { rotation: -1.5, from: -4 });
    ["#s1-i1","#s1-i2","#s1-i3","#s1-i4"].forEach((s,k) => tl.fromTo(s, {opacity:0, x:-20}, {opacity:1, x:0, duration:0.22, ease:"power2.out"}, 1.2 + k*0.45));
    ["#s1-i1","#s1-i2","#s1-i3"].forEach((s,k) => cf.strike(tl, s, 3.6 + k*0.32));
    cf.circle(tl, "#s1-i4", 4.7, { pad: 18 });

    window.__timelines["s1"] = tl;
  </script>
</template>
```
Layout rules that keep it looking like the reference:
- Header (`.hdr`) on content pages: left = section label, right = `FIG. n` in red. Skip it on
  photo plates and the closing question.
- `.stack` centres one idea between the header and the lower caption-safe area. One headline
  per page; supporting text is `.kicker` (above) or `.small` (below).
- Red is for the single word that matters (`THREE.`, `EVERY DAY.`, `$0.20`, `?`). The orange
  marker is for definitions. Never colour two things red on one page.
- Ink (underline/circle/strike/stamp) lands 0.4–0.8 s *after* its text, timed to the spoken
  word. That beat-after-the-word rhythm is the style.
- Torn cards for quotes and captions over photos; `.letter` only for a real document or a
  ledger of facts with a source line — never a fabricated letter from a real organisation.
- Photo plate scene: `<div class="plate"><img src="assets/img/x.jpg"></div>` + `cf.push`
  over the scene length + a torn caption card in the lower third.
- Keep all text between y≈190 and y≈1560 so Instagram's UI doesn't cover it.

## 4. Sound
Voice at 1.0. Set each SFX `data-duration` to the file's real length (ffprobe it). SFX under the voice at 0.35–0.6: stamp on every stamp slam, typing under typed text,
key-press under counters, whoosh-short on strikes, a soft whoosh on section changes, riser
into the turning point. If the user has a music bed, add it at 0.12–0.18 with
`data-fade-in`/`data-fade-out`; otherwise tell them to add a low ambient track in CapCut.

## 5. Check → look → render
```bash
hyperframes lint && hyperframes check          # must pass; timeline_track_too_dense and contrast on deliberately dimmed struck-through text are expected
hyperframes snapshot --at <mid-point of every scene>   # then READ the contact sheet
HYPERFRAMES_BROWSER_PATH=/usr/bin/google-chrome hyperframes render --fps 30 --quality delivery -o renders/<slug>.mp4
```
In the snapshots look for: ink marks offset from their words, text past the margins, two
lines of headline where one was intended, empty lower halves (raise font sizes or move the
stack), and any number that differs from your research notes. Renders run several minutes;
run them in the background. Afterwards probe the MP4 (duration, audio stream) and look at a
few frames from the actual file before sending it.

## 6. Deliver
Send the MP4, then in the user's language: one line on what the video covers, the sources
used for the numbers, and the voiceover script if they haven't recorded it yet. Offer to swap
any line or number.