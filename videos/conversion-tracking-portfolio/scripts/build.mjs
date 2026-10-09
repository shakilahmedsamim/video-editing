// Assemble index.html from timings.json and inject per-line cue times into each scene.
// Usage: node scripts/build.mjs   (run from the project root, after scripts/voice.py)
import fs from "node:fs";

const T = JSON.parse(fs.readFileSync("timings.json", "utf8"));
const W = 1920, H = 1080;
const TERMS = ["GA4", "Google Tag Manager", "Google Ads", "Enhanced Conversions", "Meta Pixel",
  "Conversions API", "server-side", "HubSpot", "CRM", "data layer", "deduplication", "consent",
  "evidence", "click ID", "Conversion Tracking", "Web Analytics"];
const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;");
const hi = (s) => {
  let out = esc(s);
  for (const t of TERMS) out = out.replace(new RegExp(`\\b(${t})\\b`, "g"), '<b class="cap-k">$1</b>');
  return out;
};

// 1) inject cues
for (const sc of T.scenes) {
  const f = `compositions/${sc.id}.html`;
  if (!fs.existsSync(f)) { console.warn("missing", f); continue; }
  const cues = sc.lines.map((l) => +l.start.toFixed(2));
  const src = fs.readFileSync(f, "utf8").replace(/\/\*CUES\*\/[^]*?\/\*END\*\//,
    `/*CUES*/${JSON.stringify({ c: cues, d: sc.duration })}/*END*/`);
  fs.writeFileSync(f, src);
}

// 2) index.html
const r2 = (n) => +n.toFixed(3);
const scenes = T.scenes.map((sc) => `      <div id="slot-${sc.id}" data-composition-id="${sc.id}" data-composition-src="compositions/${sc.id}.html"
        data-start="${r2(sc.start)}" data-duration="${r2(sc.duration)}" data-track-index="1"
        data-width="${W}" data-height="${H}"></div>`).join("\n");
let ci = 0;
const caps = T.scenes.flatMap((sc) => sc.lines.map((l) => {
  ci++;
  const end = l.gend + 0.15;
  return `      <div id="cap-${ci}" class="clip cap" data-start="${r2(l.gstart)}" data-duration="${r2(end - l.gstart)}" data-track-index="5"><span class="cap-t">${hi(l.text)}</span></div>`;
})).join("\n");

const html = `<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=${W}, height=${H}" />
    <script src="assets/gsap.min.js"></script>
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: ${W}px; height: ${H}px; overflow: hidden; background: #070c18; }
      :root {
        --bg: #0a1020; --panel: #101a2e; --panel2: #14203a; --line: #24324d;
        --text: #e8eef8; --muted: #8c9bb4; --dim: #7d8ba5;
        --blue: #4c8dff; --blue-soft: rgba(76, 141, 255, 0.14);
        --ok: #34d399; --warn: #f5a524; --bad: #f2555a;
      }
      #root {
        position: relative; width: 100%; height: 100%; overflow: hidden;
        background: var(--bg); color: var(--text);
        font-family: Inter, ui-sans-serif, system-ui, sans-serif;
      }
      [data-composition-id="root"] > div[data-composition-src] { position: absolute; inset: 0; }
      #bg-grid {
        position: absolute; inset: 0;
        background-image: linear-gradient(rgba(76,141,255,0.05) 1px, transparent 1px),
          linear-gradient(90deg, rgba(76,141,255,0.05) 1px, transparent 1px);
        background-size: 80px 80px;
      }
      #bg-glow {
        position: absolute; left: -10%; top: -30%; width: 120%; height: 120%;
        background: radial-gradient(ellipse at 50% 30%, rgba(76,141,255,0.13), transparent 60%);
      }
      /* shared scene vocabulary */
      .eyebrow { font-size: 22px; letter-spacing: 0.22em; text-transform: uppercase; color: var(--blue); font-weight: 600; }
      .card { background: var(--panel); border: 1px solid var(--line); border-radius: 20px; }
      .demo-tag { display: inline-block; font-size: 16px; letter-spacing: 0.14em; font-weight: 700; color: var(--warn);
        border: 1px solid rgba(245,165,36,0.5); border-radius: 8px; padding: 6px 12px; }
      .mono { font-family: "JetBrains Mono", monospace; }
      /* captions */
      .cap { position: absolute; left: 0; right: 0; bottom: 56px; display: flex; justify-content: center; }
      .cap-t { max-width: 1500px; text-align: center; font-size: 36px; line-height: 1.3; font-weight: 500;
        color: #f4f7fc; background: rgba(6, 10, 20, 0.78); border-radius: 14px; padding: 12px 28px; }
      .cap-k { color: #8db7ff; font-weight: 700; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="root" data-width="${W}" data-height="${H}" data-duration="${r2(T.total)}">
      <div id="bg" class="clip" data-start="0" data-duration="${r2(T.total)}" data-track-index="0"><div id="bg-glow"></div><div id="bg-grid"></div></div>
${scenes}
${caps}
      <audio id="vo" src="assets/audio/voice.wav" data-start="0" data-duration="${r2(T.total)}" data-track-index="10" data-volume="1"></audio>
      <audio id="bgm" src="assets/audio/music.wav" data-start="0" data-duration="${r2(T.total)}" data-track-index="11" data-volume="0.13"></audio>
    </div>
    <script>
      const tl = gsap.timeline({ paused: true });
      tl.fromTo("#bg-glow", { x: -60, y: 0 }, { x: 60, y: 30, duration: ${r2(T.total)}, ease: "none" }, 0);
      tl.fromTo("#bg-grid", { backgroundPosition: "0px 0px" }, { backgroundPosition: "80px 160px", duration: ${r2(T.total)}, ease: "none" }, 0);
      window.__timelines["root"] = tl;
    </script>
  </body>
</html>
`;
fs.writeFileSync("index.html", html);
console.log(`index.html: ${T.scenes.length} scenes, ${ci} captions, ${T.total}s`);
