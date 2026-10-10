// Assemble the "color-block promo" video from timings.json.
//  - injects per-line cue times into each compositions/<scene>.html  (/*CUES*/{...}/*END*/)
//  - overlaps scenes by WIPE seconds so each new scene circle-wipes over the previous one
//  - writes compositions/captions.html (one line at a time, active word highlighted)
//  - collects SFX cues declared in each scene (/*SFX*/[...]/*ENDSFX*/) into sfx.json
//  - writes index.html
// Usage: node scripts/build.mjs   (run from the project root, after scripts/voice.py)
import fs from "node:fs";

const T = JSON.parse(fs.readFileSync("timings.json", "utf8"));
const W = 1920, H = 1080, WIPE = 0.6;
const r3 = (n) => +(+n).toFixed(3);
const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;");

const sfx = [];
const slots = T.scenes.map((sc, i) => {
  const off = i === 0 ? 0 : WIPE;
  const start = sc.start - off, dur = sc.duration + off;
  const cues = sc.lines.map((l) => r3(l.start + off));
  const f = `compositions/${sc.id}.html`;
  if (!fs.existsSync(f)) throw new Error(`missing ${f}`);
  let src = fs.readFileSync(f, "utf8").replace(/\/\*CUES\*\/[^]*?\/\*END\*\//,
    `/*CUES*/${JSON.stringify({ c: cues, d: r3(dur), w: off })}/*END*/`);
  fs.writeFileSync(f, src);
  // scene-declared sound effects: [["pop", "c[1]+0.2"], ...] evaluated in scene-local time
  const m = src.match(/\/\*SFX\*\/([^]*?)\/\*ENDSFX\*\//);
  if (m) {
    const list = eval(m[1]);
    const c = cues, D = dur; // eslint-disable-line no-unused-vars
    for (const [name, expr, gain] of list) {
      const t = typeof expr === "number" ? expr : eval(expr);
      sfx.push({ name, t: r3(start + t), gain: gain ?? 1 });
    }
  }
  if (off) sfx.push({ name: "whoosh", t: r3(start), gain: 0.6 });
  return { id: sc.id, start: r3(start), dur: r3(dur), track: 1 + (i % 2) };
});
sfx.sort((a, b) => a.t - b.t);
fs.writeFileSync("sfx.json", JSON.stringify({ total: T.total, events: sfx }, null, 2));

// ---- captions sub-composition: words timed proportionally to their length inside each line
const lines = T.scenes.flatMap((sc) => sc.lines.map((l) => ({ ...l })));
let capHtml = "", capJs = "";
lines.forEach((l, li) => {
  const words = l.text.split(/\s+/);
  const weights = words.map((w) => w.replace(/[^\w']/g, "").length + 2);
  const sum = weights.reduce((a, b) => a + b, 0);
  const span = l.gend - l.gstart;
  let acc = l.gstart;
  const spans = words.map((w, wi) => {
    const t0 = acc; acc += (weights[wi] / sum) * span;
    capJs += `    hl("#cw-${li}-${wi}", ${r3(t0)}, ${r3(acc)});\n`;
    return `<span id="cw-${li}-${wi}" class="cw">${esc(w)}</span>`;
  }).join(" ");
  capHtml += `        <div id="cl-${li}" class="clip cl" data-start="${r3(l.gstart)}" data-duration="${r3(l.gend - l.gstart + 0.2)}" data-track-index="1"><div class="cl-in">${spans}</div></div>\n`;
});
fs.writeFileSync("compositions/captions.html", `<!doctype html>
<html>
  <head><meta charset="UTF-8" /></head>
  <body>
    <template>
      <style>
        #root { position: absolute; inset: 0; pointer-events: none; }
        .cl { position: absolute; left: 0; right: 0; bottom: 64px; display: flex; justify-content: center; }
        .cl-in { max-width: 1520px; text-align: center; font-family: Inter, sans-serif; font-size: 34px; font-weight: 600;
          line-height: 1.5; color: #e9eefb; background: rgba(4, 8, 18, 0.62); border: 1px solid rgba(255,255,255,0.08); border-radius: 18px; padding: 10px 26px; }
        .cw { display: inline-block; padding: 0 6px; margin: 0 -3px; border-radius: 10px; }
      </style>
      <div id="root" data-composition-id="captions" data-width="${W}" data-height="${H}">
${capHtml}      </div>
      <script>
        (function () {
          const tl = gsap.timeline({ paused: true });
          function hl(sel, a, b) {
            tl.fromTo(sel, { backgroundColor: "rgba(76,141,255,0)", color: "#e9eefb" },
              { backgroundColor: "rgba(76,141,255,1)", color: "#ffffff", duration: 0.08 }, a);
            tl.to(sel, { backgroundColor: "rgba(76,141,255,0)", color: "#e9eefb", duration: 0.08 }, Math.max(a + 0.1, b - 0.02));
          }
${capJs}          window.__timelines["captions"] = tl;
        })();
      </script>
    </template>
  </body>
</html>
`);

// ---- deterministic particle field
let seed = 7; const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
const particles = Array.from({ length: 70 }, () => { const z = rnd(); const sz = (1 + z * 3).toFixed(1);
  return `<i class="pt" style="left:${(rnd() * 2040).toFixed(0)}px;top:${(rnd() * 1200).toFixed(0)}px;width:${sz}px;height:${sz}px;opacity:0.3"></i>`; }).join("");

// ---- index.html
const slotHtml = slots.map((s) => `      <div id="slot-${s.id}" data-composition-id="${s.id}" data-composition-src="compositions/${s.id}.html"
        data-start="${s.start}" data-duration="${s.dur}" data-track-index="${s.track}" data-width="${W}" data-height="${H}"></div>`).join("\n");
fs.writeFileSync("index.html", `<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=${W}, height=${H}" />
    <script src="assets/gsap.min.js"></script>
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: ${W}px; height: ${H}px; overflow: hidden; background: #05080f; }
      :root {
        --bg: #05080f; --bg2: #0a1222; --text: #eef2fb; --muted: #8e9ab3; --dim: #5d6a85;
        --blue: #4c8dff; --cyan: #5ee0ff; --ok: #34d399; --warn: #fbbf24; --bad: #f2555a; --white: #ffffff;
      }
      #root { position: relative; width: 100%; height: 100%; overflow: hidden; background: radial-gradient(ellipse at 50% 35%, #0d1a33 0%, #05080f 70%);
        font-family: Inter, sans-serif; color: var(--text); }
      [data-composition-id="root"] > div[data-composition-src] { position: absolute; inset: 0; }
      /* shared scene vocabulary */
      .wipe { position: absolute; inset: 0; overflow: hidden; }
      .fill { position: absolute; inset: 0; }
      .big { font-weight: 800; letter-spacing: -0.035em; line-height: 0.98; }
      .glass { background: rgba(255, 255, 255, 0.16); border: 1.5px solid rgba(255, 255, 255, 0.35); border-radius: 22px;
        box-shadow: 0 30px 60px rgba(42, 15, 53, 0.22); }
      .paper { background: #ffffff; color: var(--ink); border-radius: 22px; box-shadow: 0 30px 70px rgba(42, 15, 53, 0.25); }
      .pill { display: inline-flex; align-items: center; border-radius: 999px; font-weight: 700; }
      .ast { position: absolute; width: 56px; height: 56px; }
      .ast i { position: absolute; left: 22px; top: 0; width: 12px; height: 56px; border-radius: 6px; background: currentColor; }
      .ast i:nth-child(2) { transform: rotate(60deg); } .ast i:nth-child(3) { transform: rotate(-60deg); }
      .mono { font-family: "JetBrains Mono", monospace; }
      .demo { position: absolute; font-size: 17px; letter-spacing: 0.14em; font-weight: 800; padding: 7px 14px; border-radius: 8px;
        background: rgba(42, 15, 53, 0.78); color: #ffd27a; }
      .gl { background: linear-gradient(160deg, rgba(255,255,255,0.09), rgba(255,255,255,0.03)); border: 1px solid rgba(255,255,255,0.12);
        border-radius: 20px; box-shadow: 0 30px 80px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.08); }
      .kick { font-size: 20px; font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase; color: var(--blue); }
      .hd { font-weight: 800; letter-spacing: -0.035em; line-height: 1.02; }
      .grad { background: linear-gradient(90deg, #ffffff, #9cc0ff); -webkit-background-clip: text; background-clip: text; color: transparent; }
      #pt { position: absolute; inset: -60px; }
      .pt { position: absolute; border-radius: 50%; background: #9cc0ff; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="root" data-width="${W}" data-height="${H}" data-duration="${r3(T.total)}">
      <div id="bgl" class="clip" data-start="0" data-duration="${r3(T.total)}" data-track-index="0"><div id="pt">${particles}</div></div>
${slotHtml}
      <div id="slot-captions" data-composition-id="captions" data-composition-src="compositions/captions.html"
        data-track-kind="captions" data-start="0" data-duration="${r3(T.total)}" data-track-index="5" data-width="${W}" data-height="${H}"></div>
      <audio id="vo" src="assets/audio/voice.wav" data-start="0" data-duration="${r3(T.total)}" data-track-index="10" data-volume="1"></audio>
      <audio id="bgm" src="assets/audio/music.wav" data-start="0" data-duration="${r3(T.total)}" data-track-index="11" data-volume="0.14"></audio>
      <audio id="sfx" src="assets/audio/sfx.wav" data-start="0" data-duration="${r3(T.total)}" data-track-index="12" data-volume="0.3"></audio>
    </div>
    <script>
      const tl = gsap.timeline({ paused: true });
      tl.fromTo("#pt", { x: 0, y: 0 }, { x: -50, y: -30, duration: ${r3(T.total)}, ease: "none" }, 0);
      tl.fromTo("#pt .pt", { opacity: 0.15 }, { opacity: 0.55, duration: 2.2, yoyo: true, repeat: ${Math.ceil(T.total / 2.2)}, stagger: { each: 0.07, from: "random" }, ease: "sine.inOut" }, 0);
      window.__timelines["root"] = tl;
    </script>
  </body>
</html>
`);
console.log(`index.html: ${slots.length} scenes, ${lines.length} caption lines, ${sfx.length} sfx, ${T.total}s`);
