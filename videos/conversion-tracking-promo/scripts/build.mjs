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
  if (off) sfx.push({ name: "whoosh", t: r3(start), gain: 1 });
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
        .cl-in { max-width: 1520px; text-align: center; font-family: Montserrat, sans-serif; font-size: 38px; font-weight: 700;
          line-height: 1.5; color: #fff; background: rgba(36, 14, 46, 0.62); border-radius: 18px; padding: 10px 26px; }
        .cw { display: inline-block; padding: 0 6px; margin: 0 -3px; border-radius: 10px; }
      </style>
      <div id="root" data-composition-id="captions" data-width="${W}" data-height="${H}">
${capHtml}      </div>
      <script>
        (function () {
          const tl = gsap.timeline({ paused: true });
          function hl(sel, a, b) {
            tl.fromTo(sel, { backgroundColor: "rgba(244,165,28,0)", color: "#ffffff" },
              { backgroundColor: "rgba(244,165,28,1)", color: "#2a0f35", duration: 0.08 }, a);
            tl.to(sel, { backgroundColor: "rgba(244,165,28,0)", color: "#ffffff", duration: 0.08 }, Math.max(a + 0.1, b - 0.02));
          }
${capJs}          window.__timelines["captions"] = tl;
        })();
      </script>
    </template>
  </body>
</html>
`);

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
      html, body { width: ${W}px; height: ${H}px; overflow: hidden; background: #b4519e; }
      :root {
        --magenta: #b4519e; --orange: #f4a51c; --lime: #b6d334; --plum: #3a1648; --cream: #f7f1ea;
        --ink: #2a0f35; --white: #ffffff; --ok: #1fa971; --bad: #e23d5b;
      }
      #root { position: relative; width: 100%; height: 100%; overflow: hidden; background: var(--magenta);
        font-family: Montserrat, sans-serif; color: var(--white); }
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
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="root" data-width="${W}" data-height="${H}" data-duration="${r3(T.total)}">
${slotHtml}
      <div id="slot-captions" data-composition-id="captions" data-composition-src="compositions/captions.html"
        data-track-kind="captions" data-start="0" data-duration="${r3(T.total)}" data-track-index="5" data-width="${W}" data-height="${H}"></div>
      <audio id="vo" src="assets/audio/voice.wav" data-start="0" data-duration="${r3(T.total)}" data-track-index="10" data-volume="1"></audio>
      <audio id="bgm" src="assets/audio/music.wav" data-start="0" data-duration="${r3(T.total)}" data-track-index="11" data-volume="0.16"></audio>
      <audio id="sfx" src="assets/audio/sfx.wav" data-start="0" data-duration="${r3(T.total)}" data-track-index="12" data-volume="0.3"></audio>
    </div>
    <script>
      window.__timelines["root"] = gsap.timeline({ paused: true });
    </script>
  </body>
</html>
`);
console.log(`index.html: ${slots.length} scenes, ${lines.length} caption lines, ${sfx.length} sfx, ${T.total}s`);
