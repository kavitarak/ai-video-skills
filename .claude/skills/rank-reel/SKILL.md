---
name: rank-reel
description: "Hindi countdown-ranking reel (Top 10 -> No.1) with neo-brutalist colour cards, counters, demo panels, Devanagari word captions and comment/DM outro in HyperFrames; topic mode or edit the user's own video."
---

# Rank reel (countdown style)

The reference reel ("18 लाख GitHub stars — top 10 Claude Code skills") works because it is a
**countdown with proof**: every item is a bright card with one hard number that counts up,
a one-line Hindi hook, and a tiny demo showing what the thing does. Pace ≈ 4.5 s per item,
captions build word by word, the top bar shows progress so viewers stay for No.1, and the end
converts: "Comment SKILLS" typed into a comment box + a DM card being sent "to the friend
who still…". Always use the user's own brand in the top bar, never the reference creator's.

Everything in it must be true — the numbers are the hook. Pull live numbers (GitHub API,
official sites) and say where they came from.

## 0. Pick the mode (ask only if unclear)
- **Topic mode**: user gives a topic ("top 5 AI tools", "best free APIs"). You research, rank,
  script, build. No footage.
- **Own-video mode** (`mode: "split"`): user sends their talking-head video. Their video plays in
  a framed window under the cards; their own audio is the voice; captions come from their speech;
  a card appears when they reach each point.
Ask about the brand once if unknown (name + logo letter for the top bar). The examples below use
the brand **kavi.onlines**, letter **K**; always replace it with the user's own brand.

## 1. Research and rank (topic mode)
- Find a real, comparable metric for every item (GitHub stars, users, downloads, price…). For
  GitHub, the API is reachable even when the web isn't:
  `curl -s "https://api.github.com/repos/<owner>/<repo>"` → `stargazers_count`, or
  `https://api.github.com/search/repositories?q=<query>&sort=stars&order=desc`.
- Rank by that metric, descending to No.1 at the end. Keep the source and date of each number.
- Intro total = sum of the items (Indian commas, e.g. `24,93,821`) and the teaser = No.1's
  value in lakh/k ("5.6 लाख").

## 2. Script (Hindi, Devanagari, English tech words kept in Latin)
One short line per beat, in the reference rhythm:
- Intro: `"<total in लाख> <metric>। ये हैं <topic> के top <N>।"`
- Items: `"<Number in English>. <name> — <what it does in ≤7 words>।"` (e.g. "Eight. Caveman. कम बोलो, कम tokens।")
- No.1: `"और number one: <name>। <one-line payoff>।"`
- Outro: `"पूरी list चाहिए? Comment करो <KEYWORD>, और उस दोस्त को भेजो जो अभी भी <pain>।"`
Mark 1–2 words per line to highlight: `r` = red box (numbers, the hook word), `b` = black box
(the payoff phrase). Show the script to the user.

**Voice.** No TTS may be reachable here (check `npx hyperframes media-use resolve --doctor`).
If none: build a text-led cut (captions carry it) and give the user the script to record; when
they send the recording, transcribe it (below) and rebuild with real word timings + `vo`.
Voice cloning isn't available offline — say so plainly if asked.

## 3. Own-video mode: transcribe and place cards
1. Copy the user's video; extract 16 kHz mono wav; transcribe with word timestamps
   (Whisper-small via npm when Hugging Face is blocked):
```bash
mkdir -p ~/models/dl && cd ~/models/dl
for i in 0 1 2 3; do npm pack @skillninja/shortmovie-telop-model-p$i --silent; done
for f in *.tgz; do mkdir -p x/${f%.tgz}; tar -xzf $f -C x/${f%.tgz}; done
mkdir -p ../whisper-small && cp x/*p0*/package/{tokenizer.json,vocabulary.json,config.json,preprocessor_config.json} ../whisper-small/
cat x/*p0*/package/model.bin.part0 x/*p1*/package/model.bin.part1 x/*p2*/package/model.bin.part2 x/*p3*/package/model.bin.part3 > ../whisper-small/model.bin
pip install --break-system-packages -q faster-whisper
```
   Pass a numpy array (not a path) to `WhisperModel(...).transcribe(audio, language="hi", word_timestamps=True)`.
2. Build caption groups straight from the words (3–6 words per group, break at pauses > 0.35 s
   or sentence ends; `t0` = first word start − 0.05, `t1` = next group's `t0`). Fix obvious
   mis-hearings of names/brands by hand; show the user the caption text if unsure.
3. Find where they start each point (the spoken number or the item's name) → that's the item's
   `start`; its `dur` runs to the next item. Before the first item, set a `headline` card
   (title of the video). Look at a frame of their video to set `video_focus` (CSS
   object-position) so faces aren't cropped by the window.

## 4. Build
Set up once per session:
```bash
npm i -g hyperframes 2>/dev/null || true          # or use npx hyperframes …
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 HYPERFRAMES_BROWSER_PATH=/usr/bin/google-chrome   # set to your own Chrome/Chromium path
mkdir -p ~/rankreel/kit/fonts && cd /tmp && npm pack gsap@3.15.0 @fontsource/inter @fontsource/noto-sans-devanagari @fontsource/jetbrains-mono --silent
for f in *.tgz; do mkdir -p x_${f%.tgz}; tar -xzf $f -C x_${f%.tgz}; done
cp x_gsap-*/package/dist/gsap.min.js ~/rankreel/kit/
cp x_fontsource-inter-*/package/files/inter-latin-900-normal.woff2 ~/rankreel/kit/fonts/inter-900.woff2
cp x_fontsource-inter-*/package/files/inter-latin-700-normal.woff2 ~/rankreel/kit/fonts/inter-700.woff2
cp x_fontsource-noto-sans-devanagari-*/package/files/noto-sans-devanagari-devanagari-800-normal.woff2 ~/rankreel/kit/fonts/deva-800.woff2
cp x_fontsource-noto-sans-devanagari-*/package/files/noto-sans-devanagari-latin-800-normal.woff2 ~/rankreel/kit/fonts/deva-latin-800.woff2
cp x_fontsource-jetbrains-mono-*/package/files/jetbrains-mono-latin-700-normal.woff2 ~/rankreel/kit/fonts/mono-700.woff2
test -d ~/hyperframes || git clone --depth 1 https://github.com/heygen-com/hyperframes ~/hyperframes   # for SFX
```
Write the three files below verbatim (`~/rankreel/kit/rankreel.css`, `~/rankreel/kit/rankreel.js`,
`~/rankreel/build.py`), then write a spec script like the example and run it. The builder writes
a complete HyperFrames project; copy `package.json`/`hyperframes.json` from any
`hyperframes init` project next to it (or run `hyperframes init <slug> --non-interactive
--skip-skills --resolution portrait --example blank` first and build into that folder).

Demo panel types (pick the one that *shows* the item's job): `chips` (a flow: Plan→Test→Code,
lights up in order) · `chat` (session bubbles, last one green ✓) · `compare` (red "Without · 180
lines" vs dark "With · lean" bars) · `tags` (official feature tags under a header) · `tiles`
(3–5 traits, last one highlighted) · `stat` (a number counting to a result). Colours: one
saturated colour per item, never repeated in a reel (yellow #f2b63c, green #2fb37b, magenta
#d94fd0, orange #ec6f2d, pink #e66ab3, mint #bfe3d6, coral #e2685a, lime #8fe33d, violet #a98bf5,
blue #4d8af0).

### `kit/rankreel.css`
```css
/* Rank-reel kit — cream canvas, neo-brutalist colour cards, Hindi word captions. */
@font-face { font-family: "RR Inter"; src: url("fonts/inter-900.woff2") format("woff2"); font-weight: 900; }
@font-face { font-family: "RR Inter"; src: url("fonts/inter-700.woff2") format("woff2"); font-weight: 700; }
@font-face { font-family: "RR Deva"; src: url("fonts/deva-800.woff2") format("woff2"); font-weight: 800; unicode-range: U+0900-097F, U+1CD0-1CF9, U+200C-200D, U+20A8, U+20B9, U+25CC, U+A830-A839, U+A8E0-A8FF; }
@font-face { font-family: "RR Deva"; src: url("fonts/deva-latin-800.woff2") format("woff2"); font-weight: 800; unicode-range: U+0000-00FF, U+2000-206F; }
@font-face { font-family: "RR Mono"; src: url("fonts/mono-700.woff2") format("woff2"); font-weight: 700; }

:root {
  --bg: #f1ebe5; --ink: #141414; --muted: #7a726b; --white: #ffffff; --red: #e8331f;
  --sans: "RR Inter", "Inter", sans-serif; --mono: "RR Mono", "JetBrains Mono", monospace; --cap: "RR Deva", "RR Inter", sans-serif;
}

/* ---------- canvas ---------- */
#canvas { position: absolute; inset: 0; overflow: hidden; background: var(--bg); }
#canvas .blob1 { position: absolute; width: 900px; height: 900px; right: -260px; top: -320px; border-radius: 50%;
  background: radial-gradient(circle, rgba(246, 196, 176, .85) 0%, rgba(246, 196, 176, 0) 70%); }
#canvas .blob2 { position: absolute; width: 900px; height: 900px; left: -380px; top: -260px; border-radius: 50%;
  background: radial-gradient(circle, rgba(244, 214, 222, .7) 0%, rgba(244, 214, 222, 0) 70%); }
#canvas .blob3 { position: absolute; width: 1200px; height: 900px; left: -60px; bottom: -420px; border-radius: 50%;
  background: radial-gradient(circle, rgba(230, 226, 222, .9) 0%, rgba(230, 226, 222, 0) 70%); }

/* ---------- top bar (persistent) ---------- */
#topbar { position: absolute; left: 60px; right: 60px; top: 112px; height: 72px; display: flex; align-items: center; justify-content: space-between; z-index: 6; }
#brand { display: flex; align-items: center; gap: 18px; font-family: var(--sans); font-weight: 900; font-size: 40px; color: var(--ink); letter-spacing: -1px; }
#brand .logo { width: 66px; height: 66px; border-radius: 16px; background: var(--red); color: #fff; display: flex; align-items: center; justify-content: center;
  font-size: 42px; font-weight: 900; box-shadow: 0 6px 14px rgba(232, 51, 31, .35); }
.pill-label { font-family: var(--mono); font-weight: 700; font-size: 26px; letter-spacing: 4px; color: var(--ink); text-transform: uppercase;
  background: rgba(255, 255, 255, .7); padding: 12px 24px; border-radius: 40px; white-space: nowrap; }
#segs { position: absolute; left: 60px; right: 60px; top: 214px; display: flex; gap: 12px; z-index: 6; }
#segs .seg { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 8px; }
#segs .bar { width: 100%; height: 12px; border-radius: 8px; background: rgba(20, 20, 20, .1); overflow: hidden; position: relative; }
#segs .fill { position: absolute; inset: 0; border-radius: 8px; transform: scaleX(0); transform-origin: 0 50%; }
#segs .n { font-family: var(--mono); font-weight: 700; font-size: 24px; color: var(--muted); }

/* ---------- rank card ---------- */
.rcard { position: absolute; left: 60px; right: 60px; top: 290px; height: 690px; border: 6px solid var(--ink); border-radius: 36px;
  box-shadow: 14px 14px 0 var(--ink); padding: 40px 48px; overflow: hidden; }
.rcard .k { font-family: var(--mono); font-weight: 700; font-size: 26px; letter-spacing: 2px; color: rgba(20, 20, 20, .62); }
.rcard .no { display: inline-block; margin-top: 16px; background: var(--ink); color: #fff; font-family: var(--mono); font-weight: 700; font-size: 28px; padding: 6px 14px; border-radius: 6px; }
.rcard .title { font-family: var(--sans); font-weight: 900; font-size: 104px; line-height: 1.02; letter-spacing: -4px; color: var(--ink); margin-top: 10px; white-space: nowrap; }
.rcard .repo { display: inline-flex; align-items: center; gap: 10px; background: var(--ink); color: #fff; font-family: var(--mono); font-weight: 700; font-size: 26px; padding: 6px 14px; border-radius: 6px; margin-top: 8px; }
.rcard .repo svg { width: 26px; height: 26px; fill: #fff; }
.rcard .lbl { font-family: var(--mono); font-weight: 700; font-size: 26px; letter-spacing: 2px; color: rgba(20, 20, 20, .62); margin-top: 30px; }
.rcard .big { font-family: var(--sans); font-weight: 900; font-size: 184px; line-height: 0.95; letter-spacing: -9px; color: var(--ink); margin-top: 4px; font-variant-numeric: tabular-nums; }
.rcard .track { position: relative; height: 16px; background: rgba(20, 20, 20, .16); border-radius: 10px; margin-top: 22px; overflow: hidden; }
.rcard .track .fill { position: absolute; inset: 0; background: var(--ink); border-radius: 10px; transform: scaleX(0); transform-origin: 0 50%; }
.rcard .tag { font-family: var(--sans); font-weight: 700; font-size: 34px; color: var(--ink); margin-top: 18px; }
.rcard .px { position: absolute; right: 26px; top: 22px; display: grid; grid-template-columns: repeat(9, 18px); grid-auto-rows: 18px; gap: 4px; }
.rcard .px i { display: block; background: var(--ink); border-radius: 2px; }

/* ---------- demo panel ---------- */
.panel { position: absolute; left: 60px; right: 60px; top: 1020px; height: 370px; background: #fff; border-radius: 34px;
  box-shadow: 0 18px 40px rgba(60, 40, 30, .12); padding: 40px 44px; overflow: hidden; }
.panel .ph { font-family: var(--mono); font-weight: 700; font-size: 24px; letter-spacing: 4px; color: #b7aea6; text-transform: uppercase; }
.chip { display: inline-flex; align-items: center; justify-content: center; font-family: var(--sans); font-weight: 700; font-size: 38px; color: var(--ink);
  padding: 22px 34px; border-radius: 22px; border: 4px solid var(--ink); background: #fff; }
.arr { font-family: var(--sans); font-weight: 900; font-size: 40px; color: #b7aea6; }
.bubble { display: inline-block; font-family: var(--sans); font-weight: 700; font-size: 34px; color: var(--ink); background: #f3eee9; border-radius: 20px; padding: 16px 24px; }
.bubble.ok { background: #e3f6e6; color: #1f8a3b; }
.cbar { height: 86px; border-radius: 14px; display: flex; align-items: center; padding: 0 26px; font-family: var(--sans); font-weight: 900; font-size: 36px; color: #fff; transform-origin: 0 50%; white-space: nowrap; }
.tagx { display: inline-block; font-family: var(--sans); font-weight: 700; font-size: 32px; color: #b0412e; background: #fbe9e4; border-radius: 16px; padding: 12px 22px; }
.tile { display: flex; align-items: center; justify-content: center; text-align: center; font-family: var(--sans); font-weight: 700; font-size: 32px; color: var(--ink);
  border: 4px solid var(--ink); border-radius: 18px; height: 160px; padding: 0 12px; }
.stat { font-family: var(--sans); font-weight: 900; font-size: 150px; letter-spacing: -6px; line-height: 1; color: var(--ink); }

/* ---------- captions ---------- */
.cap { position: absolute; left: 70px; right: 70px; top: 1428px; text-align: center; font-family: var(--cap); font-weight: 800; font-size: 58px; line-height: 1.35; color: var(--ink); }
.cap .w { display: inline-block; margin: 0 0.12em; }
.cap .r { background: var(--red); color: #fff; border-radius: 10px; padding: 0 14px; }
.cap .b { background: var(--ink); color: #fff; border-radius: 10px; padding: 0 14px; }

/* ---------- own-video mode: footage window ---------- */
.footage { position: absolute; left: 60px; right: 60px; overflow: hidden; border: 6px solid var(--ink); border-radius: 36px; box-shadow: 14px 14px 0 var(--ink); background: #000; }
.footage video { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }

/* ---------- intro / outro ---------- */
.total { position: absolute; left: 0; right: 0; top: 330px; text-align: center; font-family: var(--sans); font-weight: 900; font-size: 236px; letter-spacing: -11px; color: var(--ink); font-variant-numeric: tabular-nums; }
.total-l { position: absolute; left: 0; right: 0; top: 590px; text-align: center; font-family: var(--sans); font-weight: 900; font-size: 50px; color: var(--ink); }
.toplbl { position: absolute; left: 0; right: 0; top: 290px; text-align: center; font-family: var(--mono); font-weight: 700; font-size: 24px; letter-spacing: 6px; color: #b7aea6; text-transform: uppercase; }
.mini { position: absolute; width: 640px; height: 400px; border: 6px solid var(--ink); border-radius: 30px; box-shadow: 10px 10px 0 var(--ink); padding: 30px 36px; }
.mini .t { font-family: var(--sans); font-weight: 900; font-size: 64px; letter-spacing: -2px; color: var(--ink); }
.mini .v { font-family: var(--sans); font-weight: 900; font-size: 120px; letter-spacing: -5px; color: var(--ink); margin-top: 10px; }
.mini .q { position: absolute; right: 34px; top: 22px; font-family: var(--sans); font-weight: 900; font-size: 70px; color: var(--ink); }
.mini .blur { filter: blur(14px); }
.inputbar { position: absolute; left: 60px; right: 60px; top: 300px; height: 150px; background: #fff; border-radius: 32px; box-shadow: 0 18px 40px rgba(60, 40, 30, .12);
  display: flex; align-items: center; padding: 0 30px; gap: 26px; }
.inputbar .av { width: 74px; height: 74px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #ff7a5c, #e8331f); flex: none; }
.inputbar .field { flex: 1; height: 96px; border-radius: 24px; background: #f4f0ec; display: flex; align-items: center; padding: 0 30px; font-family: var(--sans); font-weight: 900; font-size: 54px; color: var(--ink); }
.inputbar .send { width: 96px; height: 96px; border-radius: 24px; background: var(--red); display: flex; align-items: center; justify-content: center; flex: none; }
.caret { display: inline-block; width: 5px; height: 58px; background: var(--ink); margin-left: 6px; }
.dm { position: absolute; left: 60px; right: 60px; top: 490px; height: 300px; background: #fff; border-radius: 32px; box-shadow: 0 18px 40px rgba(60, 40, 30, .12); padding: 34px 40px; }
.dm .lbl { font-family: var(--mono); font-weight: 700; font-size: 24px; letter-spacing: 4px; color: #b7aea6; }
.dm .row { display: flex; align-items: center; gap: 22px; margin-top: 18px; }
.dm .face { width: 78px; height: 78px; border-radius: 50%; background: #f1e3d6; display: flex; align-items: center; justify-content: center; font-family: var(--sans); font-weight: 900; font-size: 36px; color: var(--ink); flex: none; }
.dm .msg { font-family: var(--sans); font-weight: 900; font-size: 44px; line-height: 1.15; color: var(--ink); flex: 1; }
.dm .ig { width: 64px; height: 64px; flex: none; }
.dm .btn { position: relative; display: inline-flex; align-items: center; margin-top: 22px; height: 64px; padding: 0 30px; border-radius: 34px; font-family: var(--sans); font-weight: 900; font-size: 32px; color: #fff; background: var(--ink); }
.dm .btn .sent { position: absolute; inset: 0; border-radius: 34px; background: #23a047; display: flex; align-items: center; justify-content: center; opacity: 0; }
.biglogo { position: absolute; left: 50%; top: 900px; width: 200px; height: 200px; margin-left: -100px; border-radius: 48px; background: var(--red); color: #fff;
  display: flex; align-items: center; justify-content: center; font-family: var(--sans); font-weight: 900; font-size: 120px; box-shadow: 0 24px 50px rgba(232, 51, 31, .35); }
```

### `kit/rankreel.js`
```js
/* Rank-reel kit: deterministic GSAP helpers. Each takes the scene's own timeline `tl`
   and a time local to that scene. No Math.random, no Date. */
(function () {
  const $ = (s) => (typeof s === "string" ? document.querySelector(s) : s);
  function rng(seed) { let s = seed >>> 0 || 1; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }

  // Pixel/dither corner on a card (seeded so it's identical every render).
  function pixels(sel, seed) {
    const host = $(sel); if (!host) return; const r = rng(seed || 3);
    for (let row = 0; row < 7; row++) for (let col = 0; col < 9; col++) {
      const i = document.createElement("i");
      const density = (col / 8) * 0.9 + (1 - row / 6) * 0.45 - 0.35;
      i.style.opacity = r() < density ? (r() < 0.5 ? "1" : "0.55") : "0";
      host.appendChild(i);
    }
  }

  // Counter. fmt: "k" (101.8k), "in" (18,33,463), "en" (1,833,463), or fn.
  function count(tl, sel, t, from, to, dur, o = {}) {
    const el = $(sel); if (!el) return; const dec = o.decimals == null ? (o.fmt === "k" ? 1 : 0) : o.decimals;
    const f = typeof o.fmt === "function" ? o.fmt
      : o.fmt === "k" ? (n) => n.toFixed(dec) + "k"
      : (n) => Number(n.toFixed(dec)).toLocaleString(o.fmt === "en" ? "en-US" : "en-IN", { minimumFractionDigits: dec, maximumFractionDigits: dec });
    const obj = { v: from }; el.textContent = (o.prefix || "") + f(from) + (o.suffix || "");
    tl.fromTo(obj, { v: from }, { v: to, duration: dur, ease: o.ease || "power3.out",
      onUpdate: () => { el.textContent = (o.prefix || "") + f(obj.v) + (o.suffix || ""); } }, t);
  }

  // Card arrives: rises from below with a little overshoot.
  function cardIn(tl, sel, t) {
    tl.fromTo(sel, { y: 140, scale: 0.94, rotation: 2, opacity: 0 }, { y: 0, scale: 1, rotation: 0, opacity: 1, duration: 0.42, ease: "back.out(1.4)" }, t);
  }
  // Pop for chips/tiles/tags (accepts array of selectors, staggered).
  function pop(tl, sels, t, o = {}) {
    tl.fromTo(sels, { scale: 0.6, opacity: 0, y: 16 }, { scale: 1, opacity: 1, y: 0, duration: o.dur || 0.26, ease: "back.out(2)", stagger: o.stagger || 0.12 }, t);
  }
  // Progress bar / horizontal fill.
  function fill(tl, sel, t, to, dur) { tl.fromTo(sel, { scaleX: 0 }, { scaleX: to == null ? 1 : to, duration: dur || 0.9, ease: "power3.out" }, t); }
  // Typing into a field (reveals characters).
  function typeIn(tl, sel, t, cps) {
    const el = $(sel); if (!el) return 0; const txt = el.textContent; el.textContent = ""; const c = cps || 9;
    [...txt].forEach((ch, i) => { const s = document.createElement("span"); s.textContent = ch; s.style.opacity = "0"; el.appendChild(s); tl.set(s, { opacity: 1 }, t + i / c); });
    return txt.length / c;
  }

  window.rr = { pixels, count, cardIn, pop, fill, typeIn };
})();
```

### `build.py`
```python
"""Rank-reel builder. build(spec, out_dir) writes a HyperFrames project.

spec = {
  "brand": {"name": "kavi.onlines", "letter": "K"},
  "mode": "topic" | "split",            # split = user's own video in a window under the cards
  "video": "/path/talking.mp4",         # split mode only (its audio is kept)
  "vo": "/path/vo.wav" | None,          # topic mode voiceover (optional)
  "intro": {"label": "TOP 10 COMBINED · GITHUB", "total": 1833463, "unit": "stars", "fmt": "in",
            "teaser": "3 लाख", "dur": 5.5},
  "items": [ {"rank": 10, "slug": "CLAUDE-MEM", "title": "claude-mem", "kicker": "Claude Code skill",
              "repo": "thedotmack/claude-mem", "label": "GitHub stars", "value": 101.8, "fmt": "k",
              "bar": 0.34, "tag": "Remembers every past session", "color": "#f2b63c",
              "demo": {"type": "chips", "items": ["Plan","Test","Code"]}, "dur": 4.6, "start": None} ],
  "outro": {"label": "FREE LIST", "keyword": "SKILLS", "dm": "Wo dost jo Claude bina skills ke chala raha hai", "dur": 7},
  "captions": [ {"t0": 0.2, "t1": 2.4, "words": [["18", 0.2, "r"], ["लाख", 0.5, "r"], ["GitHub", 0.9], ["stars।", 1.3]]} ],
}
Demo types: chips{items, active?} · chat{lines:[[text, ok?]]} · compare{rows:[[label, frac, color]], head} ·
tags{head, items} · tiles{items} · stat{from,to,label}
"""
import html as H, json, os, shutil

KIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kit")
SFX = os.path.expanduser("~/hyperframes/skills/media-use/audio/assets/sfx")
SFX_LEN = {"pop": 0.72, "whoosh-short": 0.57, "click-soft": 0.36, "key-press": 0.43, "whoosh": 0.57, "typing": 1.54, "sparkle": 1.5}
GH = '<svg viewBox="0 0 16 16"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38v-1.33c-2.23.48-2.7-1.07-2.7-1.07-.36-.92-.89-1.17-.89-1.17-.73-.5.06-.49.06-.49.8.06 1.23.83 1.23.83.72 1.22 1.88.87 2.34.66.07-.52.28-.87.51-1.07-1.78-.2-3.65-.89-3.65-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82a7.6 7.6 0 0 1 4 0c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48v2.2c0 .21.15.46.55.38A8 8 0 0 0 16 8c0-4.42-3.58-8-8-8Z"/></svg>'
STAR = '<svg viewBox="0 0 24 24" style="width:1em;height:1em;vertical-align:-0.12em"><path fill="#f7c325" d="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7L12 17.3 5.8 20.9l1.6-7L2 9.2l7.1-.6z"/></svg>'
SEND = '<svg viewBox="0 0 24 24" width="48" height="48"><path fill="#fff" d="M3 11.5 21 3l-8.5 18-2.2-7.3z"/></svg>'
IG = '<svg viewBox="0 0 24 24" class="ig"><defs><linearGradient id="igg" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#feda75"/><stop offset=".5" stop-color="#d62976"/><stop offset="1" stop-color="#4f5bd5"/></linearGradient></defs><rect x="2" y="2" width="20" height="20" rx="6" fill="none" stroke="url(#igg)" stroke-width="2.2"/><circle cx="12" cy="12" r="4.6" fill="none" stroke="url(#igg)" stroke-width="2.2"/><circle cx="17.6" cy="6.4" r="1.4" fill="#d62976"/></svg>'
e = H.escape


def _demo(i, d):
    t = d["type"]; js = []
    if t == "chips":
        parts = []
        for k, c in enumerate(d["items"]):
            if k: parts.append(f'<span id="{i}-ar{k}" class="arr">→</span>')
            parts.append(f'<span id="{i}-c{k}" class="chip">{e(c)}</span>')
        ids = [f'"#{i}-c{k}"' for k in range(len(d["items"]))]
        allids = []
        for k in range(len(d["items"])):
            if k: allids.append(f'"#{i}-ar{k}"')
            allids.append(f'"#{i}-c{k}"')
        html = f'<div class="ph">{e(d.get("head", "workflow"))}</div><div style="display:flex;align-items:center;gap:18px;margin-top:70px;justify-content:center">{"".join(parts)}</div>'
        js.append(f'rr.pop(tl, [{", ".join(allids)}], 0.9, {{ stagger: 0.12 }});')
        col = d.get("color", "#4d8af0")
        for k, s in enumerate(ids):
            js.append(f'tl.to({s}, {{ backgroundColor: "{col}", color: "#fff", duration: 0.18, ease: "power2.out" }}, {1.8 + k * 0.45:.2f});')
    elif t == "chat":
        rows = []
        for k, ln in enumerate(d["lines"]):
            txt, ok = (ln + [False])[:2] if isinstance(ln, list) else (ln, False)
            rows.append(f'<div style="margin-top:{18 if k else 26}px"><span id="{i}-b{k}" class="bubble{" ok" if ok else ""}">{e(txt)}{" ✓" if ok else ""}</span></div>')
        html = f'<div class="ph">{e(d.get("head", "session"))}</div>{"".join(rows)}'
        js.append(f'rr.pop(tl, [{", ".join(f"""\"#{i}-b{k}\"""" for k in range(len(d["lines"])))}], 0.9, {{ stagger: 0.55 }});')
    elif t == "compare":
        rows = []
        for k, (lbl, frac, colr) in enumerate(d["rows"]):
            rows.append(f'<div id="{i}-r{k}" class="cbar" style="background:{colr};width:{int(frac * 100)}%;margin-top:{26 if k else 30}px">{e(lbl)}</div>')
        html = f'<div class="ph">{e(d.get("head", "compare"))}</div>{"".join(rows)}'
        for k in range(len(d["rows"])):
            js.append(f'rr.fill(tl, "#{i}-r{k}", {0.9 + k * 0.5:.2f}, 1, 0.6);')
    elif t == "tags":
        tg = "".join(f'<span id="{i}-g{k}" class="tagx">{e(x)}</span>' for k, x in enumerate(d["items"]))
        html = f'<div style="display:flex;align-items:center;gap:22px"><div class="logo" style="width:90px;height:90px;border-radius:22px;background:#fff;box-shadow:0 8px 20px rgba(0,0,0,.12);display:flex;align-items:center;justify-content:center;font-size:56px;color:#e8331f">✳</div><div style="font-family:var(--sans);font-weight:900;font-size:44px">{e(d.get("head", ""))}</div></div><div style="display:flex;flex-wrap:wrap;gap:16px;margin-top:34px">{tg}</div>'
        js.append(f'rr.pop(tl, [{", ".join(f"""\"#{i}-g{k}\"""" for k in range(len(d["items"])))}], 0.9, {{ stagger: 0.12 }});')
    elif t == "tiles":
        n = len(d["items"])
        tl_ = "".join(f'<div id="{i}-t{k}" class="tile" style="background:{d.get("color", "#d9cffc")}{"" if k < n - 1 else "; filter: saturate(1.6)"}">{e(x)}</div>' for k, x in enumerate(d["items"]))
        html = f'<div class="ph">{e(d.get("head", ""))}</div><div style="display:grid;grid-template-columns:repeat({n},1fr);gap:16px;margin-top:50px">{tl_}</div>'
        js.append(f'rr.pop(tl, [{", ".join(f"""\"#{i}-t{k}\"""" for k in range(n))}], 0.9, {{ stagger: 0.14 }});')
    elif t == "stat":
        html = f'<div class="ph">{e(d.get("head", ""))}</div><div style="display:flex;align-items:flex-end;justify-content:space-between;margin-top:40px"><div style="font-family:var(--sans);font-weight:700;font-size:36px;max-width:440px;color:#7a726b">{e(d.get("label", ""))}</div><div id="{i}-st" class="stat" style="color:{d.get("color", "#141414")}">0</div></div>'
        js.append(f'rr.count(tl, "#{i}-st", 0.9, {d["from"]}, {d["to"]}, 1.4, {{ fmt: "en" }});')
    else:
        raise ValueError(t)
    return html, "\n    ".join(js)


def _item_scene(i, it, n_total, idx, split):
    seed = (it["rank"] * 7 + 3)
    demo_html, demo_js = ("", "")
    if not split and it.get("demo"):
        demo_html, demo_js = _demo(i, it["demo"])
    big = it["value"]
    pill = f'#{it["rank"]:02d} · {it["slug"]} · {idx:02d} / {n_total:02d}'
    title_size = 104 if len(it["title"]) <= 14 else max(64, int(104 * 14 / len(it["title"])))
    if split: title_size = min(title_size, 84)
    card_style = f'background:{it["color"]};' + ("height:560px; top:300px; padding:34px 44px;" if split else "")
    html = f'''<div class="pill-label" id="{i}-pl" style="position:absolute; right:60px; top:122px; z-index:7{"; font-size:%dpx; letter-spacing:2px" % max(18, int(26 * 24 / len(pill))) if len(pill) > 24 else ""}">{e(pill)}</div>
    <div id="{i}-card" class="rcard" style="{card_style}">
      <div class="px" id="{i}-px"></div>
      <div class="k">{e(it.get("kicker", ""))}</div>
      <div class="no">No.{it["rank"]:02d}</div>
      <div class="title" style="font-size:{title_size}px">{e(it["title"])}</div>
      {f'<div class="repo">{GH}{e(it["repo"])}</div>' if it.get("repo") else ''}
      <div class="lbl">★ {e(it.get("label", ""))}</div>
      <div class="big" id="{i}-big"{' style="font-size:140px; letter-spacing:-6px"' if split else ''}>0</div>
      <div class="track"><div class="fill" id="{i}-bar"></div></div>
      <div class="tag">{e(it.get("tag", ""))}</div>
    </div>
    {f'<div class="panel" id="{i}-panel">{demo_html}</div>' if demo_html else ''}'''
    js = f'''rr.pixels("#{i}-px", {seed});
    rr.cardIn(tl, "#{i}-card", 0);
    rr.count(tl, "#{i}-big", 0.25, 0, {big}, 1.3, {{ fmt: "{it.get("fmt", "k")}" }});
    rr.fill(tl, "#{i}-bar", 0.35, {it.get("bar", 0.5)}, 1.2);
    {f'tl.fromTo("#{i}-panel", {{ y: 80, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }}, 0.5);' if demo_html else ''}
    {demo_js}'''
    sfx = [("whoosh-short", 0.0, 0.35), ("key-press", 0.3, 0.3), ("key-press", 0.8, 0.25)]
    if demo_html:
        sfx.append(("pop", 0.9, 0.3))
    return html, js, sfx


def _headline_scene(i, it):
    html = f'''<div class="pill-label" style="position:absolute; right:60px; top:122px; z-index:7">{e(it.get("pill", "NEW"))}</div>
    <div id="{i}-card" class="rcard" style="background:{it.get("color", "#141414")}; height:560px; top:300px; padding:40px 48px">
      <div class="px" id="{i}-px"></div>
      <div class="k" style="color:rgba(255,255,255,.7)">{e(it.get("kicker", ""))}</div>
      <div class="title" style="color:#fff; white-space:normal; font-size:{it.get("size", 96)}px; line-height:1.0; margin-top:24px">{it["title"]}</div>
      <div class="tag" style="color:rgba(255,255,255,.85); margin-top:26px">{e(it.get("sub", ""))}</div>
    </div>'''
    js = f'''rr.pixels("#{i}-px", 11);
    rr.cardIn(tl, "#{i}-card", 0.05);'''
    return html, js, [("whoosh", 0.0, 0.35)]


def _intro_scene(i, it, items):
    cols = [x["color"] for x in items][:7]
    minis = []
    for k, c in enumerate(cols):
        inner = f'<div class="t">{e(items[k]["title"])}</div><div class="v">{items[k]["value"]}{"k" if items[k].get("fmt", "k") == "k" else ""}</div>' if k == len(cols) - 1 else ""
        minis.append(f'<div class="mini" id="{i}-m{k}" style="left:220px; top:780px; background:{c}">{inner}</div>')
    top = items[-1]
    html = f'''<div class="pill-label" style="position:absolute; right:60px; top:122px; z-index:7">{e(it.get("pill", "TOP LIST"))} · 01 / {len(items) + 2:02d}</div>
    <div class="toplbl">{e(it.get("label", ""))}</div>
    <div class="total" id="{i}-tot" style="font-size:{min(236, int(1780 / max(1, len(f"{it['total']:,}"))))}px">0</div>
    <div class="total-l">{STAR} {e(it.get("unit", "stars"))}</div>
    {"".join(minis)}
    <div class="mini" id="{i}-mys" style="left:220px; top:760px; background:{top["color"]}">
      <div style="font-family:var(--mono);font-weight:700;font-size:26px">No.01</div>
      <div class="t blur">{e(top["title"])}</div><div class="q">?</div>
      <div class="v" style="font-family:var(--cap)">{e(it.get("teaser", ""))} {STAR}</div>
    </div>'''
    n = len(cols)
    js = [f'rr.count(tl, "#{i}-tot", 0.1, {int(it["total"] * 0.25)}, {it["total"]}, 1.6, {{ fmt: "{it.get("fmt", "in")}" }});']
    for k in range(n):
        rot = (k - n / 2) * 4
        js.append(f'tl.fromTo("#{i}-m{k}", {{ opacity: 0, y: 200, rotation: 0 }}, {{ opacity: 1, y: {-k * 14}, x: {k * 10}, rotation: {rot:.1f}, duration: 0.35, ease: "back.out(1.5)" }}, {1.0 + k * 0.08:.2f});')
    js.append(f'tl.to([{", ".join(f"""\"#{i}-m{k}\"""" for k in range(n))}], {{ x: (k) => (k % 2 ? 60 : -60), rotation: (k) => (k % 2 ? 8 : -8), duration: 0.25, ease: "power2.inOut", yoyo: true, repeat: 1, stagger: 0.03 }}, 2.0);')
    js.append(f'tl.to([{", ".join(f"""\"#{i}-m{k}\"""" for k in range(n))}], {{ opacity: 0, y: 260, duration: 0.3, ease: "power2.in", stagger: 0.02 }}, 2.9);')
    js.append(f'tl.fromTo("#{i}-mys", {{ opacity: 0, scale: 0.6, rotation: -6 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.4, ease: "back.out(1.8)" }}, 3.2);')
    return html, "\n    ".join(js), [("whoosh", 1.0, 0.4), ("pop", 3.2, 0.45)]


def _outro_scene(i, it, n_total):
    html = f'''<div class="pill-label" style="position:absolute; right:60px; top:122px; z-index:7">{e(it.get("label", "FREE LIST"))} · {n_total:02d} / {n_total:02d}</div>
    <div class="inputbar" id="{i}-in"><div class="av"></div><div class="field"><span id="{i}-kw">{e(it["keyword"])}</span><span class="caret" id="{i}-car"></span></div><div class="send">{SEND}</div></div>
    <div class="dm" id="{i}-dm"><div class="lbl">SEND TO</div>
      <div class="row"><div class="face">{e(it.get("face", "D"))}</div><div class="msg">{e(it["dm"])}</div>{IG}</div>
      <div class="btn" id="{i}-btn">Send ➤<div class="sent" id="{i}-sent">Sent ✓</div></div></div>
    <div class="biglogo" id="{i}-logo">{e(it.get("letter", "K"))}</div>'''
    js = f'''tl.fromTo("#{i}-in", {{ y: 60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }}, 0.1);
    const d = rr.typeIn(tl, "#{i}-kw", 0.8, 8);
    tl.to("#{i}-car", {{ opacity: 0, duration: 0.01, yoyo: true, repeat: 15, repeatDelay: 0.24, ease: "none" }}, 0.4);
    tl.fromTo("#{i}-dm", {{ y: 60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "back.out(1.4)" }}, 1.0 + d);
    tl.to("#{i}-sent", {{ opacity: 1, duration: 0.15, ease: "none" }}, 2.4 + d);
    tl.fromTo("#{i}-logo", {{ scale: 0, rotation: -20 }}, {{ scale: 1, rotation: 0, duration: 0.45, ease: "back.out(2)" }}, 2.9 + d);'''
    return html, js, [("typing", 0.8, 0.45), ("click-soft", 2.4 + len(it["keyword"]) / 8, 0.6), ("sparkle", 2.9 + len(it["keyword"]) / 8, 0.4)]


def _captions(groups, onvideo):
    out, js = [], []
    style = ' style="top:1440px; color:#fff; text-shadow:0 4px 14px rgba(0,0,0,.85), 0 0 3px rgba(0,0,0,.9)"' if onvideo else ""
    for g, grp in enumerate(groups):
        ws = []
        for k, w in enumerate(grp["words"]):
            txt, t = w[0], w[1]; cls = w[2] if len(w) > 2 else ""
            ws.append(f'<span class="w{(" " + cls) if cls else ""}" id="cw{g}-{k}">{e(txt)}</span>')
            js.append(f'tl.fromTo("#cw{g}-{k}", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.12, ease: "power2.out" }}, {t:.2f});')
        dur = round(grp["t1"] - grp["t0"], 2)
        out.append(f'<div id="cg{g}" class="clip cap" data-start="{grp["t0"]:.2f}" data-duration="{dur}" data-track-index="{g % 2 + 1}"{style}>{" ".join(ws)}</div>')
    return "\n    ".join(out), "\n    ".join(js)


def build(spec, out):
    split = spec.get("mode") == "split"
    os.makedirs(out + "/compositions", exist_ok=True); os.makedirs(out + "/assets/fonts", exist_ok=True); os.makedirs(out + "/assets/sfx", exist_ok=True)
    for f in ("rankreel.css", "rankreel.js", "gsap.min.js"):
        shutil.copy(f"{KIT}/{f}", f"{out}/assets/{f}")
    for f in os.listdir(f"{KIT}/fonts"):
        shutil.copy(f"{KIT}/fonts/{f}", f"{out}/assets/fonts/{f}")
    items = spec["items"]; n_total = len(items) + 2
    scenes = []  # (id, html, js, sfx, start, dur)
    t = 0.0
    if split and spec.get("headline"):
        h, j, s = _headline_scene("head", spec["headline"])
        first = items[0].get("start") or 0
        if first > 0.3:
            scenes.append(("head", h, j, s, 0.0, round(first, 3)))
    if spec.get("intro") and not split:
        h, j, s = _intro_scene("intro", {**spec["intro"]}, items)
        d = spec["intro"].get("dur", 5.5); scenes.append(("intro", h, j, s, t, d)); t += d
    for k, it in enumerate(items):
        h, j, s = _item_scene(f"i{k}", it, n_total, k + 2, split)
        st = it.get("start") if it.get("start") is not None else t
        d = it.get("dur", 4.6)
        st = round(st, 3); scenes.append((f"i{k}", h, j, s, st, d)); t = round(st + d, 3)
    if spec.get("outro") and not split:
        o = {**spec["outro"], "letter": spec["brand"]["letter"]}
        h, j, s = _outro_scene("outro", o, n_total)
        d = spec["outro"].get("dur", 7.0); scenes.append(("outro", h, j, s, round(t, 3), d)); t = round(t + d, 3)
    total = round(spec.get("total") or t, 2)
    # fix durations so scenes don't overlap
    fixed = []
    for k, sc in enumerate(scenes):
        nxt = scenes[k + 1][4] if k + 1 < len(scenes) else total
        fixed.append((*sc[:5], round(min(sc[5], nxt - sc[4]) if k + 1 < len(scenes) else total - sc[4], 3)))
    scenes = fixed
    mounts, auds, used = [], [], set()
    for sid, h, j, s, st, d in scenes:
        open(f"{out}/compositions/{sid}.html", "w").write(f'''<template>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    {h}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {j}
    window.__timelines["{sid}"] = tl;
  </script>
</template>
''')
        mounts.append(f'      <div id="{sid}" class="clip" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{st}" data-duration="{d}" data-track-index="{2 + len(mounts) % 2}" data-width="1080" data-height="1920" style="z-index:4"></div>')
        for n, (fx, tt, vol) in enumerate(s):
            if tt >= d: continue
            used.add(fx)
            auds.append(f'    <audio id="{sid}-fx{n}" class="clip" src="assets/sfx/{fx}.mp3" data-start="{round(st + tt, 3)}" data-duration="{SFX_LEN[fx]}" data-track-index="{20 + len(auds) % 6}" data-volume="{vol}"></audio>')
    for fx in used:
        shutil.copy(f"{SFX}/{fx}.mp3", f"{out}/assets/sfx/{fx}.mp3")
    # progress segments
    segs = "".join(f'<div class="seg"><div class="bar"><div class="fill" id="sf{k}" style="background:{it["color"]}"></div></div><div class="n">{it["rank"]}</div></div>' for k, it in enumerate(items))
    seg_js = []
    for k, sc in enumerate([x for x in scenes if x[0].startswith("i")]):
        seg_js.append(f'tl.fromTo("#sf{k}", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.35, ease: "power2.out" }}, {sc[4] + 0.1:.2f});')
    # captions
    cap_html, cap_js = _captions(spec.get("captions", []), split)
    open(f"{out}/compositions/captions.html", "w").write(f'''<template>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
    {cap_html}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {cap_js}
    window.__timelines["captions"] = tl;
  </script>
</template>
''')
    media = ""
    if split:
        shutil.copy(spec["video"], f"{out}/assets/footage.mp4")
        media = f'''      <div class="footage" style="top:{spec.get("video_top", 930)}px; height:{1890 - spec.get("video_top", 930) - 260}px; z-index:3">
        <video id="a-roll" class="clip" src="assets/footage.mp4" style="object-position:{spec.get("video_focus", "50% 40%")}" playsinline data-has-audio="true" data-start="0" data-duration="{total}" data-track-index="0"></video>
      </div>'''
    elif spec.get("vo"):
        shutil.copy(spec["vo"], f"{out}/assets/vo.wav")
        auds.insert(0, f'    <audio id="vo" class="clip" src="assets/vo.wav" data-start="0" data-duration="{total}" data-track-index="9" data-volume="1"></audio>')
    b = spec["brand"]
    open(f"{out}/index.html", "w").write(f'''<!doctype html>
<html lang="hi" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <link rel="stylesheet" href="assets/rankreel.css" />
    <script src="assets/gsap.min.js"></script>
    <script src="assets/rankreel.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #f1ebe5; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="1080" data-height="1920">
      <div id="canvas"><div class="blob1"></div><div class="blob2"></div><div class="blob3"></div></div>
      <div id="topbar"><div id="brand"><div class="logo">{e(b["letter"])}</div>{e(b["name"])}</div></div>
      <div id="segs">{segs}</div>
{media}
{chr(10).join(mounts)}
      <div id="caps" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{total}" data-track-index="8" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:9"></div>
{chr(10).join(auds)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {chr(10).join("      " + x for x in seg_js).strip()}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
''')
    return dict(total=total, scenes=[(s[0], s[4], s[5]) for s in scenes])


def captions_from_lines(lines, starts, durs, hl=None):
    """Text-led captions: one caption group per script line, words revealed at reading pace
    across the scene. hl = {word: 'r'|'b'} highlight map."""
    hl = hl or {}; groups = []
    for line, st, d in zip(lines, starts, durs):
        words = line.split()
        if not words: continue
        if len(words) <= 6:
            chunks = [words]
        else:  # split after sentence punctuation nearest the middle
            mid = len(words) / 2
            cuts = [k + 1 for k, w in enumerate(words[:-1]) if w[-1] in "।,.?!:—" or w == "—"]
            cut = min(cuts, key=lambda c: abs(c - mid)) if cuts else len(words) // 2
            chunks = [words[:cut], words[cut:]]
        span = d - 0.3; per_chunk = span / len(chunks); t0 = st + 0.15
        for ch in chunks:
            step = min(0.32, (per_chunk - 0.4) / max(1, len(ch)))
            ws = [[w, round(t0 + k * step, 2)] + ([hl[w.strip("।,.?!")]] if w.strip("।,.?!") in hl else []) for k, w in enumerate(ch)]
            groups.append({"t0": round(t0, 2), "t1": round(t0 + per_chunk - 0.05, 2), "words": ws})
            t0 += per_chunk
    return groups
```

### Example spec (topic mode — the tested GitHub top-5 reel)
```python
import os, sys; sys.path.insert(0, os.path.expanduser("~/rankreel"))
from build import build, captions_from_lines
items = [
 dict(rank=5, slug="REA", title="rea", kicker="GitHub repo", repo="morluto/rea", label="GitHub stars", value=443.1, bar=443.1/561, tag="Reverse engineer anything with agents", color="#ec6f2d",
      demo=dict(type="chips", head="how it works", items=["App", "Agents", "Source"], color="#141414")),
 dict(rank=4, slug="FREECODECAMP", title="freeCodeCamp", kicker="GitHub repo", repo="freeCodeCamp/freeCodeCamp", label="GitHub stars", value=458.8, bar=458.8/561, tag="Learn to code — free", color="#2fb37b",
      demo=dict(type="tags", head="Free curriculum", items=["HTML", "CSS", "JavaScript", "Python", "Math"])),
 dict(rank=3, slug="PUBLIC-APIS", title="public-apis", kicker="GitHub repo", repo="public-apis/public-apis", label="GitHub stars", value=497.2, bar=497.2/561, tag="A collective list of free APIs", color="#e66ab3",
      demo=dict(type="chat", head="request", lines=[["GET /weather?city=Raipur"], ["200 OK · free", True]])),
 dict(rank=2, slug="AWESOME", title="awesome", kicker="GitHub repo", repo="sindresorhus/awesome", label="GitHub stars", value=533.7, bar=533.7/561, tag="Awesome lists about every topic", color="#f2b63c",
      demo=dict(type="tiles", head="lists for", items=["Python", "React", "Security", "Design"], color="#fbe7b5")),
 dict(rank=1, slug="BUILD-YOUR-OWN-X", title="build-your-own-x", kicker="GitHub repo", repo="codecrafters-io/build-your-own-x", label="GitHub stars", value=561.0, bar=1.0, tag="Recreate the tech you use, from scratch", color="#4d8af0", dur=5.2,
      demo=dict(type="chips", head="build your own", items=["Git", "Docker", "Redis"], color="#4d8af0")),
]
spec = dict(brand=dict(name="kavi.onlines", letter="K"), mode="topic",
  intro=dict(pill="GITHUB STARS", label="TOP 5 COMBINED · GITHUB", total=2493821, unit="stars", fmt="in", teaser="5.6 लाख", dur=5.5),
  items=items, outro=dict(label="FREE LIST", keyword="REPOS", dm="Wo dost jo abhi bhi tutorials mein atka hai", face="D", dur=7.0))
lines = ["25 लाख GitHub stars। ये हैं GitHub के top 5 repos।",
 "Five. rea — agents से app को reverse engineer करो।",
 "Four. freeCodeCamp — free में coding सीखो।",
 "Three. public-apis — free APIs की पूरी list।",
 "Two. awesome — हर topic की awesome lists।",
 "और number one: build-your-own-x। Git, Docker — खुद बनाओ।",
 "पूरी list चाहिए? Comment करो REPOS, और उस दोस्त को भेजो।"]
r0 = build(spec, "/tmp/_probe_rr")  # first pass only to get scene timing
starts = [s[1] for s in r0["scenes"]]; durs = [s[2] for s in r0["scenes"]]
spec["captions"] = captions_from_lines(lines, starts, durs, hl={"25": "r", "लाख": "r", "free": "b", "one:": "r", "REPOS": "r", "खुद": "b", "बनाओ।": "b"})
print(build(spec, os.path.expanduser("~/rankreel/out/topic-github")))
```
For own-video mode use `mode="split"`, `video=<path>`, `total=<video length>`, `video_top=900`,
`video_focus="50% 35%"`, a `headline=dict(pill, kicker, title, sub, color)`, items with `start`
and `dur` from the transcript, no `intro`/`outro`, and captions from the transcript words.

## 5. Check → look → render
```bash
cd <project> && hyperframes lint && hyperframes check     # timeline_track_too_dense on captions and blob overflow warnings are expected
hyperframes snapshot --at <one time per scene, ~3 s into each>   # READ the contact sheet
hyperframes render --fps 30 --quality delivery -o renders/<slug>.mp4   # run in background; ~1.5 min per 35 s
```
Look for: totals or titles running off the edges (shorten or let the builder's auto-size work),
card taglines clipped, the top pill colliding with the brand, captions splitting mid-sentence,
faces cropped in own-video mode (adjust `video_focus`/`video_top`), and any number that differs
from your sources. Probe the MP4 and look at frames from the file before sending.

## 6. Deliver
Send the MP4. In the user's language: one line on what it covers, the sources (with dates) for
every number, the script if they still need to record it, and the offer to swap items, colours
or the CTA keyword.