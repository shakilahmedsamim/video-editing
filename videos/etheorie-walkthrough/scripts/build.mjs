// Build the Apple-style screen walkthrough from steps.json + vo.json.
// One sub-composition per segment (intro, events, chapter cards, steps, outro), crossfaded by XF seconds.
// Usage: node scripts/build.mjs   (after scripts/voice.py)
import fs from "node:fs";

const cfg = JSON.parse(fs.readFileSync("steps.json", "utf8"));
const vo = JSON.parse(fs.readFileSync("vo.json", "utf8"));
const W = 1568, H = 734;                 // screenshot size
const CX = 120, CY = 128, CW = 1680;     // card position / width on the 1920x1080 frame
const S = CW / W, CH = Math.round(H * S);
const XF = 0.5, VO_AT = 0.5;
const r3 = (n) => +(+n).toFixed(3);
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;");
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));

for (const s of cfg.segments) {
  const all = [s.title, s.subtitle, s.action, s.show, s.say, ...(s.crumb || []), ...(s.chips || [])].filter(Boolean).join(" ");
  if (/[–—"'“”()[\]{}]/.test(all.replace(/(\w)'(\w)/g, "$1$2"))) throw new Error(`text rule broken in ${s.id}: ${all}`);
}

// camera framing a rect: returns {x, y, scale} for a transform-origin 0 0 camera in screenshot units
function frame(r, zmax = 1.9, zforce) {
  const [x1, y1, x2, y2] = r, w = x2 - x1, h = y2 - y1;
  const z = zforce || clamp(Math.min((0.78 * W) / w, (0.78 * H) / h), 1, zmax);
  const cx = (x1 + x2) / 2, cy = (y1 + y2) / 2;
  return { x: r3(clamp(W / 2 - z * cx, W - z * W, 0)), y: r3(clamp(H / 2 - z * cy, H - z * H, 0)), scale: r3(z) };
}

const CURSOR = `<svg viewBox="0 0 24 34" width="24" height="34"><path d="M2 2 L2 26 L8 20.2 L12.4 30 L16.6 28.1 L12.2 18.6 L20.2 18.6 Z" fill="#111" stroke="#fff" stroke-width="1.8" stroke-linejoin="round"/></svg>`;
const sfx = [];
const slots = [];
let t = 0;

function stepScene(s, id) {
  const P = id;
  let html = "", js = "", tt = 0.85;
  const crumb = s.crumb.map((c, i) => `<span class="${i === s.crumb.length - 1 ? "cur" : ""}">${esc(c)}</span>`).join('<span class="sep">›</span>');
  // click outlines + ripples
  s.clicks.forEach((c, i) => {
    if (c.box) {
      const [a, b, x2, y2] = c.box;
      html += `<div id="${P}-ob${i}" class="obox" style="left:${a - 4}px;top:${b - 4}px;width:${x2 - a + 8}px;height:${y2 - b + 8}px"></div>`;
    }
    html += `<div id="${P}-rp${i}" class="ripple" style="left:${c.x - 34}px;top:${c.y - 34}px"></div>`;
  });
  s.highlights.forEach((h, i) => {
    const [a, b, x2, y2] = h.r, pad = 6;
    html += `<div id="${P}-sp${i}" class="spot" style="left:${a - pad}px;top:${b - pad}px;width:${x2 - a + 2 * pad}px;height:${y2 - b + 2 * pad}px"></div>`;
  });
  if (s.clicks.length) html += `<div id="${P}-cur" class="cursor">${CURSOR}</div>`;

  if (!s.scroll) js += `tl.fromTo("#${P}-cam", { x: 0, y: 0, scale: 1 }, { x: 0, y: 0, scale: 1, duration: 0.01 }, 0);\n`;
  if (s.scroll) {
    js += `tl.fromTo("#${P}-cam", { x: 0, y: 110, scale: 1 }, { x: 0, y: 0, scale: 1, duration: 1.4, ease: "power2.inOut" }, 0.5);\n`;
    tt = 2.1;
  }
  if (s.clicks.length) {
    let px = W * 0.56, py = H * 0.86;
    js += `tl.fromTo("#${P}-cur", { x: ${px - 2}, y: ${py - 2}, opacity: 0 }, { x: ${px - 2}, y: ${py - 2}, opacity: 1, duration: 0.35 }, 0.45);\n`;
    s.clicks.forEach((c, i) => {
      js += `tl.to("#${P}-cur", { x: ${c.x - 2}, y: ${c.y - 2}, duration: 1.1, ease: "power2.inOut" }, ${r3(tt)});\n`;
      const at = tt + 1.1;
      if (!c.hover) {
        js += `tl.to("#${P}-cur", { scale: 0.86, duration: 0.09, yoyo: true, repeat: 1, ease: "power1.inOut", transformOrigin: "2px 2px" }, ${r3(at)});\n`;
        js += `tl.fromTo("#${P}-rp${i}", { scale: 0.2, opacity: 0.55 }, { scale: 1.6, opacity: 0, duration: 0.7, ease: "power2.out" }, ${r3(at)});\n`;
        sfx.push({ name: "tick", t: r3(t + at), gain: 0.5 });
      }
      if (c.box) {
        js += `tl.fromTo("#${P}-ob${i}", { opacity: 0 }, { opacity: 1, duration: 0.25 }, ${r3(at + 0.05)});\n`;
        js += `tl.to("#${P}-ob${i}", { opacity: 0, duration: 0.3 }, ${r3(at + 1.1)});\n`;
      }
      tt = at + 0.45;
    });
    tt += 0.5;
    js += `tl.to("#${P}-cur", { opacity: 0, duration: 0.3 }, ${r3(tt - 0.2)});\n`;
  }
  // highlights: camera move, spotlight crossfade, optional pan
  let prevSpot = null;
  s.highlights.forEach((h, i) => {
    const moveCam = !h.short || i === 0;
    if (h.pan) {
      const z = 1.45, viewH = H / z;
      const top = [h.r[0], h.r[1] - 10, h.r[2], h.r[1] - 10 + viewH];
      const f1 = frame(top, 3, z);
      const f2 = { ...f1, y: r3(clamp(H / 2 - z * (h.r[3] - viewH / 2), H - z * H, 0)) };
      js += `tl.to("#${P}-cam", { x: ${f1.x}, y: ${f1.y}, scale: ${f1.scale}, duration: 1.1, ease: "power2.inOut" }, ${r3(tt)});\n`;
      if (prevSpot !== null) js += `tl.to("#${P}-sp${prevSpot}", { opacity: 0, duration: 0.35 }, ${r3(tt + 0.2)});\n`;
      js += `tl.fromTo("#${P}-sp${i}", { opacity: 0 }, { opacity: 1, duration: 0.45 }, ${r3(tt + 0.5)});\n`;
      js += `tl.to("#${P}-cam", { y: ${f2.y}, duration: 2.6, ease: "sine.inOut" }, ${r3(tt + 1.5)});\n`;
      tt += 1.5 + 2.6 + 0.6;
    } else {
      if (moveCam) {
        const f = frame(h.r);
        js += `tl.to("#${P}-cam", { x: ${f.x}, y: ${f.y}, scale: ${f.scale}, duration: 1.1, ease: "power2.inOut" }, ${r3(tt)});\n`;
      }
      if (prevSpot !== null) js += `tl.to("#${P}-sp${prevSpot}", { opacity: 0, duration: 0.35 }, ${r3(tt + 0.1)});\n`;
      js += `tl.fromTo("#${P}-sp${i}", { opacity: 0 }, { opacity: 1, duration: 0.45 }, ${r3(tt + (moveCam ? 0.5 : 0.15))});\n`;
      tt += (moveCam ? 1.1 : 0.4) + (h.short ? 0.7 : 1.5);
    }
    prevSpot = i;
  });
  const end = tt + 0.8;
  const need = vo[s.id] ? VO_AT + vo[s.id] + 0.9 : 0;
  const D = r3(Math.max(end, need, 6));
  const body = `
      <div id="${P}-w" class="wrap">
        <div class="topbar"><div class="badge">Step ${s.step}</div><div class="crumb">${crumb}</div></div>
        <div class="card"><div class="scale"><div id="${P}-cam" class="cam">
          <img class="shot" src="assets/shots/${s.shot}" alt="">
          ${html}
        </div></div></div>
        <div class="cap"><div class="act">${esc(s.action)}</div><div class="show">Show your client: ${esc(s.show)}</div></div>
      </div>`;
  return { D, body, js };
}

function cardScene(s, P) {
  let body = "", js = "", D = 6;
  const say = vo[s.id] || 0;
  if (s.type === "intro") {
    body = `<div id="${P}-w" class="wrap center"><div class="ttl" id="${P}-t">${esc(s.title)}</div><div class="sub" id="${P}-s">${esc(s.subtitle)}</div>
      <div class="chips">${s.chips.map((c, i) => `<div class="chip" id="${P}-c${i}"><b>${i + 1}</b>${esc(c)}</div>`).join("")}</div></div>`;
    js += `tl.fromTo("#${P}-t", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.9, ease: "power3.out" }, 0.3);\n`;
    js += `tl.fromTo("#${P}-s", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.8, ease: "power3.out" }, 0.8);\n`;
    s.chips.forEach((_, i) => { js += `tl.fromTo("#${P}-c${i}", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, ${r3(1.8 + i * 0.55)});\n`; });
    D = Math.max(VO_AT + say + 1.6, 1.8 + 6 * 0.55 + 2);
  } else if (s.type === "events") {
    body = `<div id="${P}-w" class="wrap center"><div class="ttl small" id="${P}-t">${esc(s.title)}</div><div class="groups">` +
      s.groups.map((g, gi) => `<div class="grp" id="${P}-g${gi}"><div class="gname">${esc(g.name)}</div><div class="pills">${g.items.map((it, k) => `<span class="pill" id="${P}-p${gi}-${k}">${esc(it)}</span>`).join("")}</div></div>`).join("") + `</div></div>`;
    js += `tl.fromTo("#${P}-t", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.8, ease: "power3.out" }, 0.3);\n`;
    let k0 = 0.9;
    s.groups.forEach((g, gi) => {
      js += `tl.fromTo("#${P}-g${gi} .gname", { opacity: 0 }, { opacity: 1, duration: 0.4 }, ${r3(k0)});\n`;
      g.items.forEach((_, k) => { js += `tl.fromTo("#${P}-p${gi}-${k}", { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.35, ease: "power2.out" }, ${r3(k0 + 0.2 + k * 0.12)});\n`; });
      k0 += 0.4 + g.items.length * 0.12 + 0.4;
    });
    D = Math.max(VO_AT + say + 2.2, k0 + 2);
  } else if (s.type === "chapter") {
    body = `<div id="${P}-w" class="wrap center"><div class="chn" id="${P}-n">Chapter ${s.num}</div><div class="ttl" id="${P}-t">${esc(s.title)}</div><div class="sub" id="${P}-u">${esc(s.url)}</div></div>`;
    js += `tl.fromTo("#${P}-n", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }, 0.3);\n`;
    js += `tl.fromTo("#${P}-t", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.8, ease: "power3.out" }, 0.45);\n`;
    js += `tl.fromTo("#${P}-u", { opacity: 0 }, { opacity: 1, duration: 0.6 }, 0.9);\n`;
    D = 2.7;
  } else if (s.type === "outro") {
    body = `<div id="${P}-w" class="wrap center"><div class="ttl" id="${P}-t">${esc(s.title)}</div><div class="rows">` +
      s.rows.map(([a, b], i) => `<div class="row" id="${P}-r${i}"><span class="ck"><svg viewBox="0 0 20 20" width="20" height="20"><path d="M4.5 10.5 L8.5 14.2 L15.5 6.5" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg></span><b>${esc(a)}:</b><span class="rv">${esc(b)}</span></div>`).join("") + `</div></div>`;
    js += `tl.fromTo("#${P}-t", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.8, ease: "power3.out" }, 0.3);\n`;
    s.rows.forEach((_, i) => { js += `tl.fromTo("#${P}-r${i}", { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.out" }, ${r3(1.1 + i * 0.6)});\n`; });
    D = Math.max(VO_AT + say + 3.0, 1.1 + 6 * 0.6 + 3);
  }
  return { D: r3(D), body, js };
}

cfg.segments.forEach((s, i) => {
  const P = s.id;
  const { D, body, js } = s.type === "step" ? stepScene(s, P) : cardScene(s, P);
  const last = i === cfg.segments.length - 1;
  const fade = `tl.fromTo("#${P}-w", { opacity: 0 }, { opacity: 1, duration: ${XF}, ease: "power1.inOut" }, 0);\n` +
    (last ? "" : `tl.to("#${P}-w", { opacity: 0, duration: ${XF}, ease: "power1.inOut" }, ${r3(D - XF)});\n`);
  fs.writeFileSync(`compositions/${P}.html`, `<!doctype html>
<html>
  <head><meta charset="UTF-8" /></head>
  <body>
    <template>
      <style>#root { position: absolute; inset: 0; }</style>
      <div id="root" data-composition-id="${P}" data-width="1920" data-height="1080">${body}
      </div>
      <script>
        (function () {
          const tl = gsap.timeline({ paused: true });
${(fade + js).split("\n").filter(Boolean).map((l) => "          " + l).join("\n")}
          window.__timelines["${P}"] = tl;
        })();
      </script>
    </template>
  </body>
</html>
`);
  slots.push({ id: P, start: r3(t), dur: D, vo: vo[s.id] ? r3(t + VO_AT) : null, voDur: vo[s.id] });
  t = t + D - XF;
});
const TOTAL = r3(t + XF);
fs.writeFileSync("sfx.json", JSON.stringify({ total: TOTAL, events: sfx }, null, 2));
fs.writeFileSync("timings.json", JSON.stringify({ total: TOTAL, slots }, null, 2));

const slotHtml = slots.map((s, i) => `      <div id="slot-${s.id}" data-composition-id="${s.id}" data-composition-src="compositions/${s.id}.html" data-start="${s.start}" data-duration="${s.dur}" data-track-index="${1 + (i % 2)}" data-width="1920" data-height="1080"></div>`).join("\n");
const voHtml = slots.filter((s) => s.vo !== null).map((s) => `      <audio id="vo-${s.id}" src="assets/audio/vo/${s.id}.wav" data-start="${s.vo}" data-duration="${s.voDur}" data-track-index="10" data-volume="1"></audio>`).join("\n");
fs.writeFileSync("index.html", `<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="assets/gsap.min.js"></script>
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1920px; height: 1080px; overflow: hidden; background: #f5f5f7; }
      #root { position: relative; width: 100%; height: 100%; overflow: hidden; background: #f5f5f7; color: #1d1d1f;
        font-family: Inter, sans-serif; -webkit-font-smoothing: antialiased; }
      [data-composition-id="root"] > div[data-composition-src] { position: absolute; inset: 0; }
      .wrap { position: absolute; inset: 0; }
      .topbar { position: absolute; left: ${CX}px; top: 50px; height: 50px; display: flex; align-items: center; gap: 18px; }
      .badge { height: 44px; padding: 0 20px; border-radius: 22px; background: #0071e3; color: #fff; font-size: 20px; font-weight: 600;
        display: flex; align-items: center; letter-spacing: 0.01em; }
      .crumb { font-size: 22px; color: #6e6e73; font-weight: 500; display: flex; align-items: center; gap: 12px; white-space: nowrap; }
      .crumb .sep { color: #a1a1a6; font-size: 24px; }
      .crumb .cur { color: #1d1d1f; font-weight: 600; }
      .card { position: absolute; left: ${CX}px; top: ${CY}px; width: ${CW}px; height: ${CH}px; border-radius: 18px; overflow: hidden; background: #fff;
        box-shadow: 0 30px 80px rgba(0,0,0,0.12), 0 4px 14px rgba(0,0,0,0.06); }
      .scale { position: absolute; left: 0; top: 0; width: ${W}px; height: ${H}px; transform: scale(${r3(S)}); transform-origin: 0 0; }
      .cam { position: absolute; left: 0; top: 0; width: ${W}px; height: ${H}px; transform-origin: 0 0; }
      .shot { position: absolute; left: 0; top: 0; width: ${W}px; height: ${H}px; display: block; }
      .spot { position: absolute; border-radius: 10px; border: 3px solid #0071e3; box-shadow: 0 0 0 4000px rgba(0,0,0,0.6); opacity: 0; }
      .obox { position: absolute; border-radius: 9px; border: 3px solid #0071e3; box-shadow: 0 0 0 4px rgba(0,113,227,0.18); opacity: 0; }
      .ripple { position: absolute; width: 68px; height: 68px; border-radius: 50%; background: rgba(0,113,227,0.35); border: 2px solid rgba(0,113,227,0.6); opacity: 0; }
      .cursor { position: absolute; left: 0; top: 0; width: 24px; height: 34px; filter: drop-shadow(0 2px 3px rgba(0,0,0,0.35)); }
      .cap { position: absolute; left: ${CX}px; top: ${CY + CH + 26}px; width: ${CW}px; }
      .act { font-size: 36px; font-weight: 700; letter-spacing: -0.015em; color: #1d1d1f; }
      .show { margin-top: 6px; font-size: 25px; font-weight: 500; color: #6e6e73; }
      .center { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
      .ttl { font-size: 92px; font-weight: 700; letter-spacing: -0.035em; }
      .ttl.small { font-size: 60px; margin-bottom: 40px; }
      .sub { margin-top: 18px; font-size: 34px; color: #6e6e73; font-weight: 500; }
      .chn { font-size: 26px; font-weight: 600; color: #0071e3; margin-bottom: 16px; }
      .chips { margin-top: 64px; display: flex; gap: 18px; flex-wrap: wrap; justify-content: center; width: 1500px; }
      .chip { height: 64px; padding: 0 28px 0 12px; border-radius: 32px; background: #fff; box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        display: flex; align-items: center; gap: 14px; font-size: 25px; font-weight: 600; }
      .chip b { width: 40px; height: 40px; border-radius: 20px; background: #0071e3; color: #fff; display: flex; align-items: center; justify-content: center; font-size: 20px; }
      .groups { display: flex; gap: 40px; align-items: flex-start; }
      .grp { width: 500px; text-align: left; }
      .gname { font-size: 28px; font-weight: 700; margin-bottom: 20px; }
      .pills { display: flex; flex-wrap: wrap; gap: 12px; }
      .pill { height: 50px; padding: 0 22px; border-radius: 25px; background: #fff; box-shadow: 0 6px 18px rgba(0,0,0,0.07); font-size: 22px; font-weight: 500;
        display: inline-flex; align-items: center; }
      .rows { margin-top: 50px; display: flex; flex-direction: column; gap: 16px; width: 1180px; }
      .row { height: 76px; padding: 0 30px; border-radius: 20px; background: #fff; box-shadow: 0 8px 24px rgba(0,0,0,0.07); display: flex; align-items: center;
        gap: 16px; font-size: 27px; text-align: left; }
      .row b { font-weight: 700; } .row .rv { color: #6e6e73; font-weight: 500; }
      .ck { width: 36px; height: 36px; border-radius: 18px; background: #0071e3; display: flex; align-items: center; justify-content: center; flex: none; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="root" data-width="1920" data-height="1080" data-duration="${TOTAL}">
${slotHtml}
${voHtml}
      <audio id="bgm" src="assets/audio/music.wav" data-start="0" data-duration="${TOTAL}" data-track-index="11" data-volume="0.06"></audio>
      <audio id="sfx" src="assets/audio/sfx.wav" data-start="0" data-duration="${TOTAL}" data-track-index="12" data-volume="0.35"></audio>
    </div>
    <script>
      window.__timelines["root"] = gsap.timeline({ paused: true });
    </script>
  </body>
</html>
`);
console.log(`${slots.length} segments, ${sfx.length} clicks, total ${TOTAL}s (${(TOTAL / 60).toFixed(2)} min)`);
