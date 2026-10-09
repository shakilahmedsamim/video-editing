# Generates index.html (1080x1350, cream "screenshot proof" style). Run: python3 build.py
A,B,C,D=0.866,0.38,-0.866,0.38
OX,OY=262,590
W,H=260,120
N=13
def P(x,y,dy=0): return (A*x+C*y+OX, B*x+D*y+OY+dy)
def poly(pts): return " ".join(f"{x:.1f},{y:.1f}" for x,y in pts)
corners=[(0,0),(W,0),(W,H),(0,H)]
layers=""
for i in range(N,0,-1):
    dy=i*8.5
    layers+=f'<polygon points="{poly([P(x,y,dy) for x,y in corners])}" fill="{"#2C7A52" if i%2 else "#358A5E"}"/>\n'
    layers+=f'<polyline points="{poly([P(0,H,dy-1.2),P(W,H,dy-1.2),P(W,0,dy-1.2)])}" fill="none" stroke="#A6E3BE" stroke-width="1.2" opacity=".6"/>\n'
top_m=f"matrix({A},{B},{C},{D},{OX},{OY})"
def flame(x,y,h,rot=0):
    w=h*0.42
    return f'''<g transform="translate({x:.1f},{y:.1f}) rotate({rot})">
<path d="M0 0C{-w} {-h*0.25} {-w*0.7} {-h*0.62} 0 {-h}C{w*0.15} {-h*0.68} {w*0.95} {-h*0.5} {w*0.62} {-h*0.12}C{w*0.5} {-h*0.02} {w*0.25} 0 0 0Z" fill="url(#fo)"/>
<path d="M{w*0.05:.1f} -2C{-w*0.45} {-h*0.2} {-w*0.25} {-h*0.48} {w*0.05} {-h*0.66}C{w*0.2} {-h*0.42} {w*0.6} {-h*0.3} {w*0.32} {-h*0.08}C{w*0.25} -2 {w*0.12} -2 {w*0.05} -2Z" fill="#FFD25A"/>
</g>'''
flames=""
for t,h,r in [(0.10,58,-8),(0.24,44,6),(0.40,30,10),(0.58,22,4)]:
    x,y=P(W*t*0.75,0); flames+=flame(x,y+2,h,r)
for t,h,r in [(0.18,48,-14),(0.38,34,-6),(0.62,24,-10)]:
    x,y=P(0,H*t*0.8); flames+=flame(x+2,y+1,h,r)
x,y=P(14,10); flames+=flame(x,y+4,84,-2)
burn="M0 0L104 0L96 10L84 7L76 18L62 14L56 28L44 24L40 38L30 34L24 48L14 46L10 62L0 70Z"
gx,gy=P(10,10)
stack=f'''<svg class="abs" style="left:24px;top:500px" width="342" height="450" viewBox="130 380 380 500">
<defs><linearGradient id="fo" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#F2412C"/><stop offset=".55" stop-color="#FF7F2A"/><stop offset="1" stop-color="#FFB13B"/></linearGradient>
<radialGradient id="sh"><stop offset="0" stop-color="#3A2E14" stop-opacity=".28"/><stop offset="1" stop-color="#3A2E14" stop-opacity="0"/></radialGradient><filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="10"/></filter></defs>
<ellipse cx="320" cy="850" rx="200" ry="18" fill="url(#sh)"/>
{layers}
<polygon points="{poly([P(x,y) for x,y in corners])}" fill="#4DAA77"/>
<g transform="{top_m}">
 <rect x="10" y="10" width="{W-20}" height="{H-20}" rx="6" fill="none" stroke="#2F7D55" stroke-width="3"/>
 <rect x="20" y="20" width="{W-40}" height="{H-40}" rx="4" fill="none" stroke="#A6E3BE" stroke-width="1.4" opacity=".8"/>
 <ellipse cx="{W/2}" cy="{H/2}" rx="34" ry="34" fill="#3E9668" stroke="#2F7D55" stroke-width="3"/>
 <text x="{W/2}" y="{H/2+14}" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="40" fill="#1E5C3C">$</text>
 <circle cx="{W-38}" cy="{H-34}" r="9" fill="none" stroke="#2F7D55" stroke-width="3"/>
 <path d="{burn}" fill="#2A1A10"/><path d="{burn}" fill="none" stroke="#FF7F2A" stroke-width="3.5" stroke-linejoin="round"/>
 <rect x="168" y="-1" width="26" height="{H+2}" fill="#F1E9D2"/>
</g>
<polygon points="{poly([P(168,H),P(194,H),P(194,H,N*8.5),P(168,H,N*8.5)])}" fill="#D9CFB3"/>
<ellipse cx="{gx:.0f}" cy="{gy-24:.0f}" rx="80" ry="54" fill="#FF8A2B" opacity=".28" filter="url(#blur)"/>
{flames}
<g fill="#FF8A2B"><circle cx="232" cy="470" r="4"/><circle cx="282" cy="452" r="3"/><circle cx="214" cy="430" r="2.5"/><circle cx="306" cy="500" r="3.5"/><circle cx="196" cy="508" r="3"/></g>
<g fill="none" stroke="#8A8676" stroke-width="5" stroke-linecap="round" opacity=".35"><path d="M250 440c-18-24 18-40 0-64"/><path d="M290 470c-10-18 14-30 2-48"/></g>
</svg>'''

html=f'''<!doctype html>
<html><head><meta charset="utf-8"><title>Tracking Burns Money</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&family=Caveat:wght@700&display=swap" rel="stylesheet">
<style>
:root{{--bg:#F4F0E7;--ink:#20280F;--mut:#6B6B60;--or:#F2552C;--red:#FF4D5E;--redt:#D7263D;--ok:#22E584;--okt:#11924F}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1080px;height:1350px;overflow:hidden}}
body{{font-family:Poppins,sans-serif;color:var(--ink);position:relative;
 background:radial-gradient(700px 260px at 50% 104%,rgba(242,85,44,.20),transparent 70%),radial-gradient(900px 500px at 50% 0%,#FBF8F1,transparent 70%),var(--bg)}}
.abs{{position:absolute}}
.hand{{font-family:Caveat,cursive}}
h1{{left:0;right:0;top:76px;text-align:center;font-weight:800;font-size:78px;line-height:1.1;letter-spacing:-2px}}
h1 .o{{color:var(--or)}}
/* laptop */
.lap{{left:316px;top:400px;width:712px;height:492px;background:#1E222B;border-radius:22px;padding:16px;box-shadow:0 30px 60px rgba(60,50,20,.18)}}
.scr{{width:100%;height:100%;background:#fff;border-radius:8px;overflow:hidden;font-family:Inter,sans-serif;color:#1C1E21;position:relative}}
.cam{{position:absolute;left:50%;top:6px;width:6px;height:6px;margin-left:-3px;border-radius:50%;background:#3A3F4B}}
.base{{left:282px;top:890px;width:780px;height:30px;border-radius:0 0 22px 22px;background:linear-gradient(#D9D6CD,#BDB9AE);box-shadow:0 18px 30px rgba(60,50,20,.16)}}
.base i{{position:absolute;left:50%;top:0;width:120px;height:9px;margin-left:-60px;background:#ABA799;border-radius:0 0 8px 8px}}
.top{{height:44px;border-bottom:1px solid #ECEEF1;display:flex;align-items:center;justify-content:space-between;padding:0 18px}}
.top b{{font-size:16px;font-weight:700}}
.btn{{font-size:12px;font-weight:600;color:#555;border:1px solid #D8DCE2;border-radius:7px;padding:5px 10px}}
.kpis{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;padding:14px 18px 0}}
.k{{border:1px solid #ECEEF1;border-radius:10px;padding:10px 12px}}
.k s{{text-decoration:none;display:block;font-size:11px;letter-spacing:.6px;text-transform:uppercase;color:#8A919C;font-weight:600}}
.k b{{display:flex;align-items:baseline;gap:8px;font-size:22px;font-weight:700;margin-top:2px}}
.k em{{font-style:normal;font-size:12px;font-weight:700;padding:2px 7px;border-radius:12px}}
.up{{background:#FFE7EA;color:#C81E33}} .flat{{background:#EEF0F3;color:#6B7280}}
.chart{{position:absolute;left:18px;right:18px;top:142px;bottom:16px;border:1px solid #ECEEF1;border-radius:10px}}
.lg{{position:absolute;left:14px;top:10px;display:flex;gap:16px;font-size:12px;font-weight:600;color:#6B7280}}
.lg span{{display:flex;align-items:center;gap:6px}} .lg i{{width:14px;height:3px;border-radius:2px}}
/* cards */
.cards{{left:60px;right:60px;top:990px;display:grid;grid-template-columns:1fr 1fr;gap:22px}}
.c{{background:#fff;border-radius:22px;padding:24px 26px;display:flex;gap:18px;align-items:center;box-shadow:0 1px 0 #e7e1d4,0 12px 28px rgba(60,50,20,.08);border-left:6px solid}}
.c.r{{border-color:var(--red)}} .c.g{{border-color:var(--ok)}}
.c .ic{{flex:none;width:58px;height:58px;border-radius:50%;display:flex;align-items:center;justify-content:center}}
.c.r .ic{{background:var(--red)}} .c.g .ic{{background:var(--ok)}}
.c .t{{font-size:20px;color:var(--mut);font-weight:600;line-height:1.2}}
.c .v{{display:block;font-size:31px;font-weight:800;margin-top:4px;line-height:1.15}}
.c.r .v{{color:var(--redt)}} .c.g .v{{color:var(--okt)}}
.foot{{left:0;right:0;top:1186px;text-align:center;font-size:26px;font-weight:500;color:#45473C}}
.foot b{{font-weight:700;color:var(--ink);position:relative}}
.foot b svg{{position:absolute;left:-4px;bottom:-12px}}
</style></head><body>

<h1 class="abs">Your ads aren't<br>wasting money.<br>Your <span class="o">tracking</span> is. 🔥</h1>

<div class="abs lap"><div class="scr"><span class="cam"></span>
 <div class="top"><b>Campaign performance</b><span class="btn">Last 30 days ▾</span></div>
 <div class="kpis">
  <div class="k" style="border-color:#F6B9C1;background:#FFF7F8"><s>Cost</s><b>$18,420 <em class="up">▲ 64%</em></b></div>
  <div class="k"><s>Clicks</s><b>9,812 <em class="up">▲ 41%</em></b></div>
  <div class="k"><s>Paying customers</s><b>3 <em class="flat">0%</em></b></div>
 </div>
 <div class="chart">
  <div class="lg"><span><i style="background:#FF4D5E"></i>Cost</span><span><i style="background:#9AA1AC"></i>Paying customers</span></div>
  <svg class="abs" style="left:0;top:0" width="100%" height="100%" viewBox="0 0 676 262" preserveAspectRatio="none" fill="none">
   <defs><linearGradient id="ar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF4D5E" stop-opacity=".28"/><stop offset="1" stop-color="#FF4D5E" stop-opacity="0"/></linearGradient></defs>
   <g stroke="#F0F1F3" stroke-width="1.2"><path d="M14 80H662M14 130H662M14 180H662M14 230H662"/></g>
   <path d="M20 228L80 222L140 214L200 206L260 196L320 180L380 170L440 148L500 132L560 104L620 76L650 62V238H20Z" fill="url(#ar)"/>
   <path d="M20 228L80 222L140 214L200 206L260 196L320 180L380 170L440 148L500 132L560 104L620 76L650 62" stroke="#FF4D5E" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke"/>
   <path d="M20 232L650 230" stroke="#9AA1AC" stroke-width="2.5" stroke-dasharray="6 7" stroke-linecap="round" vector-effect="non-scaling-stroke"/>
   
  </svg>
 </div>
 <!-- hand circle around Cost -->
 <svg class="abs" style="left:0;top:0" width="680" height="420" fill="none" stroke="#E5323F" stroke-linecap="round" stroke-width="4">
  <path d="M14 92C8 60 70 44 130 46c66 2 112 18 110 46-2 30-56 46-120 44C54 134 6 120 10 90c2-16 20-30 48-36"/>
 </svg>
</div></div>
<div class="abs base"><i></i></div>
{stack}

<div class="abs cards">
 <div class="c r"><div class="ic"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 3l14 7-6 2-2 6z"/><path d="M14 14l5 5"/></svg></div><div class="t">Google sees:<span class="v">clicks</span></div></div>
 <div class="c g"><div class="ic"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#0B3D24" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.6-3.6 3.2-5.5 6.5-5.5s5.9 1.9 6.5 5.5"/><path d="M15.5 11.5l2 2 4-4.5"/></svg></div><div class="t">Google should see:<span class="v">paying customers</span></div></div>
</div>

<div class="abs foot">Bad tracking shows up as a <b>higher cost per customer.<svg width="330" height="18" viewBox="0 0 330 18" fill="none"><path d="M4 11C90 4 210 4 326 9" stroke="#F2552C" stroke-width="4" stroke-linecap="round"/></svg></b></div>
</body></html>'''
open("index.html","w").write(html)
