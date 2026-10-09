// Collect the SFX list (absolute seconds) from compositions/overlays.html into sfx.json for scripts/sfx.py.
import fs from "node:fs";
const src = fs.readFileSync("compositions/overlays.html", "utf8");
const list = eval(src.match(/\/\*SFX\*\/([^]*?)\/\*ENDSFX\*\//)[1]);
const total = JSON.parse(fs.readFileSync("timings.json", "utf8")).total;
const events = list.map(([name, t, gain]) => ({ name, t, gain: gain ?? 1 })).sort((a, b) => a.t - b.t);
fs.writeFileSync("sfx.json", JSON.stringify({ total, events }, null, 2));
console.log(`sfx.json: ${events.length} events`);
