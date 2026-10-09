# Generates index.html (1080x1350). Run: python3 build.py
A,B,C,D=0.866,0.38,-0.866,0.38
OX,OY=262,590
W,H=260,120
def P(x,y,dy=0): return (A*x+C*y+OX, B*x+D*y+OY+dy)
def poly(pts): return " ".join(f"{x:.1f},{y:.1f}" for x,y in pts)
corners=[(0,0),(W,0),(W,H),(0,H)]
layers=""
N=13
for i in range(N,0,-1):
    dy=i*8.5
    fill="#2C7A52" if i%2 else "#358A5E"
    layers+=f'<polygon points="{poly([P(x,y,dy) for x,y in corners])}" fill="{fill}"/>\n'
    # paper edge highlight along the two front edges
    e=[P(0,H,dy-1.2),P(W,H,dy-1.2),P(W,0,dy-1.2)]
    layers+=f'<polyline points="{poly(e)}" fill="none" stroke="#8FD4AC" stroke-width="1.2" opacity=".55"/>\n'
# band around stack (paper strap) on front faces
band=""
bx0,bx1=110,150
for (x0,y0,x1,y1) in [(bx0,H,bx1,H)]:
    pass
top_m=f"matrix({A},{B},{C},{D},{OX},{OY})"
# flames along top-left & top-right edges near top corner
def flame(x,y,h,s=1,rot=0):
    w=h*0.42
    return f'''<g transform="translate({x:.1f},{y:.1f}) rotate({rot}) scale({s})">
<path d="M0 0C{-w} {-h*0.25} {-w*0.7} {-h*0.62} 0 {-h}C{w*0.15} {-h*0.68} {w*0.95} {-h*0.5} {w*0.62} {-h*0.12}C{w*0.5} {-h*0.02} {w*0.25} 0 0 0Z" fill="url(#fo)"/>
<path d="M{w*0.05:.1f} -2C{-w*0.45} {-h*0.2} {-w*0.25} {-h*0.48} {w*0.05} {-h*0.66}C{w*0.2} {-h*0.42} {w*0.6} {-h*0.3} {w*0.32} {-h*0.08}C{w*0.25} -2 {w*0.12} -2 {w*0.05} -2Z" fill="#FFD25A"/>
</g>'''
flames=""
for t,h,r in [(0.10,58,-8),(0.24,44,6),(0.40,30,10),(0.58,22,4)]:
    x,y=P(W*t*0.75,0); flames+=flame(x,y+2,h,1,r)
for t,h,r in [(0.18,48,-14),(0.38,34,-6),(0.62,24,-10)]:
    x,y=P(0,H*t*0.8); flames+=flame(x+2,y+1,h,1,r)
x,y=P(14,10); flames+=flame(x,y+4,80,1,-2)
burn_flat="M0 0L104 0L96 10L84 7L76 18L62 14L56 28L44 24L40 38L30 34L24 48L14 46L10 62L0 70Z"
html=f'''<!doctype html>
<html><head><meta charset="utf-8"><title>Tracking Burns Money</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{{--bg:#0B1426;--card:#111D35;--line:#22324F;--w:#FFFFFF;--g:#C3CCDC;--dim:#8592AB;--red:#FF4D5E;--ok:#22E584}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1080px;height:1350px;overflow:hidden}}
body{{font-family:Poppins,sans-serif;color:var(--w);position:relative;background:radial-gradient(620px 420px at 42% 50%,rgba(255,120,60,.10),transparent 70%),radial-gradient(900px 600px at 50% 0%,#12203B,transparent 70%),var(--bg)}}
.abs{{position:absolute}}
h1{{left:72px;right:72px;top:84px;font-weight:800;letter-spacing:-.4px}}
h1 .l1{{display:block;font-size:56px;line-height:1.15}}
h1 .l2{{display:block;font-size:92px;line-height:1.1;letter-spacing:-1.2px;margin-top:4px}}
h1 .u{{position:relative;display:inline-block}}
h1 .u svg{{position:absolute;left:-6px;bottom:-10px}}
.cards{{left:72px;right:72px;top:1004px;display:grid;grid-template-columns:1fr 1fr;gap:24px}}
.c{{border-radius:22px;padding:26px 28px;background:var(--card);border:1.5px solid var(--line);display:flex;gap:18px;align-items:center}}
.c .ic{{flex:none;width:64px;height:64px;border-radius:18px;display:flex;align-items:center;justify-content:center}}
.c.r{{border-color:rgba(255,77,94,.55);background:linear-gradient(180deg,rgba(255,77,94,.10),rgba(255,77,94,.03)),var(--card)}}
.c.r .ic{{background:rgba(255,77,94,.16)}}
.c.k{{border-color:rgba(34,229,132,.6);background:linear-gradient(180deg,rgba(34,229,132,.10),rgba(34,229,132,.03)),var(--card);box-shadow:0 0 40px rgba(34,229,132,.10)}}
.c.k .ic{{background:rgba(34,229,132,.16)}}
.c .t{{font-size:20px;color:var(--g);font-weight:500;line-height:1.25}}
.c .v{{display:block;font-size:30px;font-weight:800;line-height:1.2;margin-top:2px}}
.c.r .v{{color:var(--red)}} .c.k .v{{color:var(--ok)}}
.foot{{left:72px;right:72px;top:1238px;font-size:26px;font-weight:500;color:#E6EBF3;display:flex;align-items:center;gap:14px}}
.foot i{{flex:none;width:36px;height:4px;border-radius:2px;background:var(--red)}}
</style></head><body>
<h1 class="abs"><span class="l1">Your ads aren't wasting money.</span><span class="l2">Your <span class="u">tracking<svg width="380" height="22" viewBox="0 0 370 22" fill="none"><path d="M4 14C90 6 230 4 366 10" stroke="#FF4D5E" stroke-width="6" stroke-linecap="round"/></svg></span> is.</span></h1>

<svg class="abs" style="left:0;top:34px" width="1080" height="1350" viewBox="0 0 1080 1350">
<defs>
 <linearGradient id="fo" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#FF4D2E"/><stop offset=".55" stop-color="#FF8A2B"/><stop offset="1" stop-color="#FFB13B"/></linearGradient>
 <linearGradient id="area" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF4D5E" stop-opacity=".38"/><stop offset="1" stop-color="#FF4D5E" stop-opacity="0"/></linearGradient>
 <linearGradient id="scr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#152442"/><stop offset="1" stop-color="#101C34"/></linearGradient>
 <linearGradient id="base" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3A4A68"/><stop offset="1" stop-color="#26334D"/></linearGradient>
 <radialGradient id="glow"><stop offset="0" stop-color="#FF8A2B" stop-opacity=".55"/><stop offset="1" stop-color="#FF8A2B" stop-opacity="0"/></radialGradient>
 <filter id="blur"><feGaussianBlur stdDeviation="6"/></filter>
</defs>

<!-- ground shadow -->
<ellipse cx="560" cy="872" rx="470" ry="26" fill="#050A15" opacity=".7"/>

<!-- ===== laptop ===== -->
<g>
 <rect x="498" y="478" width="512" height="340" rx="18" fill="#2A3753"/>
 <rect x="512" y="492" width="484" height="312" rx="8" fill="url(#scr)"/>
 <!-- top bar -->
 <rect x="512" y="492" width="484" height="30" rx="8" fill="#1A2A4A"/><rect x="512" y="510" width="484" height="12" fill="#1A2A4A"/>
 <circle cx="530" cy="507" r="4" fill="#FF5F57"/><circle cx="544" cy="507" r="4" fill="#FEBC2E"/><circle cx="558" cy="507" r="4" fill="#28C840"/>
 <rect x="600" y="500" width="250" height="14" rx="7" fill="#24365A"/>
 <!-- sidebar -->
 <rect x="512" y="522" width="52" height="282" fill="#13213D"/>
 <rect x="527" y="540" width="22" height="22" rx="6" fill="#3B6FE0"/>
 <rect x="527" y="576" width="22" height="22" rx="6" fill="#24365A"/><rect x="527" y="612" width="22" height="22" rx="6" fill="#24365A"/><rect x="527" y="648" width="22" height="22" rx="6" fill="#24365A"/>
 <!-- kpi tiles -->
 <g>
  <rect x="580" y="538" width="128" height="62" rx="10" fill="#1A2A4A"/>
  <rect x="594" y="552" width="48" height="8" rx="4" fill="#3A4D72"/><rect x="594" y="570" width="78" height="16" rx="5" fill="#C9D3E6"/>
  <rect x="720" y="538" width="128" height="62" rx="10" fill="#1A2A4A"/>
  <rect x="734" y="552" width="48" height="8" rx="4" fill="#3A4D72"/><rect x="734" y="570" width="60" height="16" rx="5" fill="#C9D3E6"/>
  <rect x="860" y="538" width="122" height="62" rx="10" fill="rgba(255,77,94,.14)" stroke="#FF4D5E" stroke-opacity=".6"/>
  <rect x="874" y="552" width="44" height="8" rx="4" fill="#FF8B96" opacity=".7"/><rect x="874" y="570" width="58" height="16" rx="5" fill="#FF4D5E"/>
  <path d="M948 584l10-12 10 12M958 573v16" stroke="#FF4D5E" stroke-width="3.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
 </g>
 <!-- chart -->
 <rect x="580" y="614" width="402" height="176" rx="10" fill="#132240"/>
 <g stroke="#22324F" stroke-width="1.2"><path d="M596 650H966M596 690H966M596 730H966M596 770H966"/></g>
 <path d="M600 768L640 760L676 752L712 742L748 734L784 712L820 704L856 682L892 666L928 642L960 628V778H600Z" fill="url(#area)"/>
 <path d="M600 768L640 760L676 752L712 742L748 734L784 712L820 704L856 682L892 666L928 642L960 628" fill="none" stroke="#FF4D5E" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
 <path d="M600 772L960 768" stroke="#7E8BA6" stroke-width="2.5" stroke-dasharray="6 7" stroke-linecap="round" opacity=".7"/>
 <circle cx="960" cy="628" r="14" fill="#FF4D5E" opacity=".22"/><circle cx="960" cy="628" r="6" fill="#FF4D5E"/>
 <!-- base -->
 <path d="M470 818H1038L1056 846C1058 852 1054 856 1046 856H462C454 856 450 852 452 846Z" fill="url(#base)"/>
 <rect x="700" y="818" width="108" height="8" rx="4" fill="#1B263D"/>
</g>

<!-- ===== money stack ===== -->
<circle cx="{P(30,20)[0]:.0f}" cy="{P(30,20)[1]-30:.0f}" r="150" fill="url(#glow)"/>
<g>
{layers}
<polygon points="{poly([P(x,y) for x,y in corners])}" fill="#4DAA77"/>
<g transform="{top_m}">
 <rect x="10" y="10" width="{W-20}" height="{H-20}" rx="6" fill="none" stroke="#2F7D55" stroke-width="3"/>
 <rect x="20" y="20" width="{W-40}" height="{H-40}" rx="4" fill="none" stroke="#8FD4AC" stroke-width="1.4" opacity=".7"/>
 <ellipse cx="{W/2}" cy="{H/2}" rx="34" ry="34" fill="#3E9668" stroke="#2F7D55" stroke-width="3"/>
 <text x="{W/2}" y="{H/2+14}" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="40" fill="#1E5C3C">$</text>
 <circle cx="{W-38}" cy="{H-34}" r="9" fill="none" stroke="#2F7D55" stroke-width="3"/>
 <!-- charred corner -->
 <path d="{burn_flat}" fill="#1B1410"/>
 <path d="{burn_flat}" fill="none" stroke="#FF8A2B" stroke-width="3.5" stroke-linejoin="round"/>
</g>
<!-- strap -->
<g transform="{top_m}"><rect x="168" y="-1" width="26" height="{H+2}" fill="#E9E1C9"/></g>
<polygon points="{poly([P(168,H),P(194,H),P(194,H,N*8.5),P(168,H,N*8.5)])}" fill="#CFC6AC"/>
</g>
<!-- glow behind flames -->
<ellipse cx="{P(10,10)[0]:.0f}" cy="{P(10,10)[1]-20:.0f}" rx="90" ry="60" fill="#FF7A2F" opacity=".35" filter="url(#blur)"/>
{flames}
<!-- embers -->
<g fill="#FFB13B"><circle cx="232" cy="470" r="3.5"/><circle cx="282" cy="452" r="2.5"/><circle cx="214" cy="430" r="2"/><circle cx="306" cy="500" r="3"/><circle cx="196" cy="508" r="2.5" fill="#FF8A2B"/></g>
<!-- smoke -->
<g fill="none" stroke="#8592AB" stroke-width="5" stroke-linecap="round" opacity=".28">
 <path d="M250 440c-18-24 18-40 0-64s14-44 4-62"/><path d="M290 470c-10-18 14-30 2-48"/>
</g>
<!-- loose half-burnt bill -->
<g transform="translate(404 404) rotate(-18)">
 <rect x="0" y="0" width="110" height="52" rx="5" fill="#4DAA77"/>
 <rect x="6" y="6" width="98" height="40" rx="3" fill="none" stroke="#2F7D55" stroke-width="2"/>
 <circle cx="55" cy="26" r="13" fill="#3E9668" stroke="#2F7D55" stroke-width="2"/>
 <text x="55" y="33" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="18" fill="#1E5C3C">$</text>
 <path d="M84 0H110V52H90L96 44L86 38L94 28L84 20L92 10Z" fill="#1B1410"/>
 <path d="M84 0L92 10L84 20L94 28L86 38L96 44L90 52" fill="none" stroke="#FF8A2B" stroke-width="2.5" stroke-linejoin="round"/>
</g>
</svg>

<div class="abs cards">
 <div class="c r"><div class="ic"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#FF4D5E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 3l14 7-6 2-2 6z"/><path d="M14 14l5 5"/></svg></div><div class="t">Google sees:<span class="v">clicks</span></div></div>
 <div class="c k"><div class="ic"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#22E584" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.6-3.6 3.2-5.5 6.5-5.5s5.9 1.9 6.5 5.5"/><path d="M15.5 11.5l2 2 4-4.5"/></svg></div><div class="t">Google should see:<span class="v">paying customers</span></div></div>
</div>
<div class="abs foot"><i></i>Bad tracking shows up as a higher cost per customer.</div>
</body></html>'''
open("index.html","w").write(html)
