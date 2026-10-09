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
stack=f'''<svg class="abs" style="left:44px;top:304px;z-index:5" width="190" height="250" viewBox="130 380 380 500">
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
h1{{left:0;right:0;top:52px;text-align:center;font-weight:800;font-size:74px;line-height:1.1;letter-spacing:-2px}}
h1 .o{{color:var(--or)}}
/* laptop */
.lap{{position:absolute;left:50px;top:548px;width:980px;height:552px;background:#fff;border-radius:18px;overflow:hidden;box-shadow:0 0 0 1px #E3DCCD,0 30px 60px rgba(60,50,20,.16)}}
.chrome{{height:46px;background:#EEF0F3;display:flex;align-items:center;gap:14px;padding:0 16px;border-bottom:1px solid #DDE0E5;font-family:Inter,sans-serif}}
.lights{{display:flex;gap:7px}}.lights i{{width:12px;height:12px;border-radius:50%}}
.url{{flex:1;height:30px;border-radius:15px;background:#fff;display:flex;align-items:center;gap:8px;padding:0 14px;font-size:14px;color:#555}}
.tiles{{left:262px;top:358px;display:flex;gap:16px}}
.tile{{width:96px;height:96px;border-radius:22px;background:#fff;box-shadow:0 1px 0 #e7e1d4,0 10px 24px rgba(60,50,20,.08);display:flex;align-items:center;justify-content:center}}
.scr{{width:805px;height:420px;transform:scale(1.2);transform-origin:0 0;background:#fff;border-radius:8px;overflow:hidden;font-family:Inter,sans-serif;color:#1C1E21;position:relative}}
.cam{{position:absolute;left:50%;top:5px;width:6px;height:6px;margin-left:-3px;border-radius:50%;background:#3A3F4B}}
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
.app-top{{height:34px;display:flex;align-items:center;gap:10px;padding:0 14px;border-bottom:1px solid #E8EAEE;font-size:12.5px}}
.ham{{display:flex;flex-direction:column;gap:2.5px}} .ham i{{width:12px;height:1.8px;background:#6B7280;border-radius:1px}}
.logo{{width:16px;height:16px;border-radius:5px;background:conic-gradient(#3B6FE0 0 50%,#F2552C 0 75%,#22C55E 0)}}
.app-top b{{font-weight:700;color:#1C1E21}}
.srch{{margin-left:18px;flex:1;height:22px;border-radius:11px;background:#F1F3F5;color:#9AA1AC;font-size:11px;display:flex;align-items:center;padding-left:12px}}
.tb-ic{{width:16px;height:16px;border-radius:50%;border:1.6px solid #9AA1AC}}
.av{{width:22px;height:22px;border-radius:50%;background:#20280F;color:#fff;font-size:9.5px;font-weight:700;display:flex;align-items:center;justify-content:center}}
.app-body{{display:flex;height:386px}}
.nav{{width:42px;border-right:1px solid #ECEEF1;background:#FAFBFC;display:flex;flex-direction:column;align-items:center;gap:16px;padding-top:14px}}
.nav i{{width:16px;height:16px;border-radius:4px;background:#DDE1E7}} .nav i.on{{background:#3B6FE0}}
.cnt{{flex:1;padding:10px 16px 0;position:relative}}
.crumb{{font-size:10.5px;color:#8A919C}} .crumb span{{margin:0 4px}}
.ttl{{display:flex;justify-content:space-between;align-items:center;margin-top:3px}}
.ttl b{{font-size:16px;font-weight:700}}
.dt{{display:flex;align-items:center;gap:6px;font-size:10.5px;font-weight:600;color:#444;border:1px solid #D8DCE2;border-radius:6px;padding:4px 8px}}
.kp{{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:9px}}
.k{{border:1px solid #ECEEF1;border-radius:8px;padding:7px 9px}}
.k.cost{{border-color:#F6B9C1;background:#FFF7F8}}
.k s{{text-decoration:none;display:block;font-size:9.5px;letter-spacing:.5px;text-transform:uppercase;color:#8A919C;font-weight:600}}
.k b{{display:block;font-size:18px;font-weight:700;margin-top:1px;font-variant-numeric:tabular-nums}}
.kr{{display:flex;align-items:center;justify-content:space-between;margin-top:2px}}
.k em{{font-style:normal;font-size:9.5px;font-weight:700;padding:1px 6px;border-radius:10px}}
.ch{{margin-top:9px;border:1px solid #ECEEF1;border-radius:8px;height:176px;position:relative;overflow:hidden}}
.ch svg{{position:absolute;left:2px;top:24px}}
.lg{{position:absolute;left:10px;right:10px;top:7px;display:flex;gap:14px;font-size:10px;font-weight:600;color:#6B7280}}
.lg span{{display:flex;align-items:center;gap:5px}} .lg i{{width:12px;height:2.5px;border-radius:2px}}
.lg .gr{{margin-left:auto;border:1px solid #E0E3E8;border-radius:5px;padding:1px 6px}}
.tip{{position:absolute;right:44px;top:92px;background:#1C1E21;color:#fff;border-radius:7px;padding:7px 10px;font-size:10px;line-height:1.55;box-shadow:0 6px 14px rgba(0,0,0,.18)}}
.tip s{{text-decoration:none;color:#AEB4BE;display:block;font-size:9.5px}}
.tip div{{display:flex;align-items:center;gap:6px}} .tip i{{width:7px;height:7px;border-radius:50%}} .tip b{{margin-left:12px;margin-left:auto;padding-left:14px}}
.tb{{width:100%;border-collapse:collapse;margin-top:8px;font-size:10.5px}}
.tb th{{text-align:left;font-size:9px;letter-spacing:.5px;text-transform:uppercase;color:#8A919C;font-weight:600;padding:4px 6px;border-bottom:1px solid #ECEEF1}}
.tb td{{padding:5px 6px;border-bottom:1px solid #F3F4F6;font-weight:500;font-variant-numeric:tabular-nums}}
.tb td.z{{color:#C81E33;font-weight:700}}
.dot{{display:inline-block;width:6px;height:6px;border-radius:50%;background:#22C55E;margin-right:6px;vertical-align:1px}}
.up{{background:#FFE7EA;color:#C81E33}} .flat{{background:#EEF0F3;color:#6B7280}}
.chart{{position:absolute;left:18px;right:18px;top:142px;bottom:16px;border:1px solid #ECEEF1;border-radius:10px}}
.lg{{position:absolute;left:14px;top:10px;display:flex;gap:16px;font-size:12px;font-weight:600;color:#6B7280}}
.lg span{{display:flex;align-items:center;gap:6px}} .lg i{{width:14px;height:3px;border-radius:2px}}
/* cards */
.cards{{left:60px;right:60px;top:1124px;display:grid;grid-template-columns:1fr 1fr;gap:22px}}
.c{{background:#fff;border-radius:22px;padding:18px 24px;display:flex;gap:18px;align-items:center;box-shadow:0 1px 0 #e7e1d4,0 12px 28px rgba(60,50,20,.08);border-left:6px solid}}
.c.r{{border-color:var(--red)}} .c.g{{border-color:var(--ok)}}
.c .ic{{flex:none;width:58px;height:58px;border-radius:50%;display:flex;align-items:center;justify-content:center}}
.c.r .ic{{background:var(--red)}} .c.g .ic{{background:var(--ok)}}
.c .t{{font-size:20px;color:var(--mut);font-weight:600;line-height:1.2}}
.c .v{{display:block;font-size:31px;font-weight:800;margin-top:4px;line-height:1.15}}
.c.r .v{{color:var(--redt)}} .c.g .v{{color:var(--okt)}}
.foot{{left:0;right:0;top:1262px;text-align:center;font-size:26px;font-weight:500;color:#45473C}}
.foot b{{font-weight:700;color:var(--ink);position:relative}}
.foot b svg{{position:absolute;left:-4px;bottom:-12px}}
</style></head><body>

<h1 class="abs">Your ads aren't<br>wasting money.<br>Your <span class="o">tracking</span> is. 🔥</h1>

<div class="abs tiles">
 <div class="tile"><svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="#20280F" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 3l14 7-6 2-2 6z"/><path d="M14 14l5 5"/></svg></div>
 <div class="tile"><svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="20" height="12" rx="2" fill="#4DAA77" stroke="#2F7D55" stroke-width="1.5"/><circle cx="12" cy="12" r="3" fill="#3E9668" stroke="#2F7D55" stroke-width="1.4"/><path d="M5 9v6M19 9v6" stroke="#2F7D55" stroke-width="1.4"/></svg></div>
 <div class="tile"><svg width="44" height="44" viewBox="0 0 24 24"><path d="M12 2c1 4 6 6 6 12a6 6 0 0 1-12 0c0-3 1.5-4.5 3-6 0 2 1 3 2 3-1-3 0-6 1-9z" fill="#FF7F2A"/><path d="M12 12c.5 2 3 3 3 5.5a3 3 0 0 1-6 0c0-1.5 1-2.5 1.8-3.2.1 1 .6 1.5 1.2 1.7-.4-1.4-.4-2.8 0-4z" fill="#FFD25A"/></svg></div>
 <div class="tile"><svg width="46" height="46" viewBox="0 0 24 24" fill="none" stroke="#E5323F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 20.5h18"/><path d="M4 16l5-5 4 3 7-8"/><path d="M15 6h5v5"/></svg></div>
 <div class="tile"><svg width="46" height="46" viewBox="0 0 24 24" fill="none" stroke="#20280F" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.6-3.6 3.2-5.5 6.5-5.5s5.9 1.9 6.5 5.5"/><path d="M16.5 9.5l4.5 4.5M21 9.5L16.5 14" stroke="#E5323F" stroke-width="2.2"/></svg></div>
</div>
<svg class="abs" style="left:822px;top:392px" width="170" height="150" viewBox="0 0 170 150" fill="none" stroke="#20280F" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M10 14c60 0 116 30 130 116"/><path d="M122 114l18 18 10-22"/></svg>
<div class="abs lap"><div class="chrome"><div class="lights"><i style="background:#FF5F57"></i><i style="background:#FEBC2E"></i><i style="background:#28C840"></i></div><div class="url"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#666" stroke-width="2.4"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg>https://ads.example.com/campaigns/overview</div></div><div class="scr">
 <div class="app-top"><span class="ham"><i></i><i></i><i></i></span><span class="logo"></span><b>Ads Manager</b><span class="srch">Search campaigns, reports...</span><span class="tb-ic"></span><span class="tb-ic"></span><span class="av">SA</span></div>
 <div class="app-body">
  <div class="nav"><i class="on"></i><i></i><i></i><i></i><i></i><i></i></div>
  <div class="cnt">
   <div class="crumb">All campaigns <span>›</span> Lead gen <span>›</span> Overview</div>
   <div class="ttl"><b>Campaign performance</b><span class="dt"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#555" stroke-width="2.4"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>Sep 1 - Sep 30, 2026 ▾</span></div>
   <div class="kp">
    <div class="k cost"><s>Cost</s><b>$18,420</b><div class="kr"><em class="up">▲ 64%</em><svg width="56" height="20" viewBox="0 0 56 20"><path d="M0.0 18.2 L7.0 17.3 L14.0 16.4 L21.0 14.6 L28.0 13.7 L35.0 11.0 L42.0 9.2 L49.0 6.5 L56.0 2.0" fill="none" stroke="#FF4D5E" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></div></div>
    <div class="k"><s>Clicks</s><b>9,812</b><div class="kr"><em class="up">▲ 41%</em><svg width="56" height="20" viewBox="0 0 56 20"><path d="M0.0 16.4 L7.0 15.5 L14.0 14.6 L21.0 12.8 L28.0 11.9 L35.0 10.1 L42.0 9.2 L49.0 7.4 L56.0 4.7" fill="none" stroke="#6B7280" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></div></div>
    <div class="k"><s>Avg. CPC</s><b>$1.88</b><div class="kr"><em class="up">▲ 16%</em><svg width="56" height="20" viewBox="0 0 56 20"><path d="M0.0 14.6 L7.0 13.7 L14.0 12.8 L21.0 13.2 L28.0 11.9 L35.0 11.0 L42.0 10.1 L49.0 9.2 L56.0 8.3" fill="none" stroke="#6B7280" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></div></div>
    <div class="k"><s>Paying customers</s><b>3</b><div class="kr"><em class="flat">0%</em><svg width="56" height="20" viewBox="0 0 56 20"><path d="M0.0 19.1 L7.0 19.1 L14.0 18.2 L21.0 19.1 L28.0 19.1 L35.0 18.2 L42.0 19.1 L49.0 19.1 L56.0 18.2" fill="none" stroke="#9AA1AC" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></div></div>
   </div>
   <div class="ch">
    <div class="lg"><span><i style="background:#FF4D5E"></i>Cost</span><span><i style="background:#9AA1AC"></i>Paying customers</span><span class="gr">Daily ▾</span></div>
    <svg width="728" height="164" viewBox="0 0 728 164" font-family="Inter" font-size="9.5" fill="#9AA1AC">
     <defs><linearGradient id="ar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF4D5E" stop-opacity=".26"/><stop offset="1" stop-color="#FF4D5E" stop-opacity="0"/></linearGradient></defs>
     <g stroke-width="1"><path d="M42 132.0H714" stroke="#EEF0F3"/><text x="35" y="135.5" text-anchor="end">$0</text><path d="M42 91.3H714" stroke="#EEF0F3"/><text x="35" y="94.8" text-anchor="end">$500</text><path d="M42 50.7H714" stroke="#EEF0F3"/><text x="35" y="54.2" text-anchor="end">$1K</text><path d="M42 10.0H714" stroke="#EEF0F3"/><text x="35" y="13.5" text-anchor="end">$1.5K</text></g><text x="42.0" y="147.0" text-anchor="start">Sep 1</text><text x="204.2" y="147.0" text-anchor="middle">Sep 8</text><text x="366.4" y="147.0" text-anchor="middle">Sep 15</text><text x="528.6" y="147.0" text-anchor="middle">Sep 22</text><text x="714.0" y="147.0" text-anchor="end">Sep 30</text>
     <path d="M42.0 106.8 L65.2 105.2 L88.3 107.6 L111.5 102.7 L134.7 101.1 L157.9 103.5 L181.0 97.8 L204.2 95.4 L227.4 97.0 L250.6 93.8 L273.7 89.7 L296.9 91.3 L320.1 86.5 L343.2 84.0 L366.4 82.4 L389.6 84.8 L412.8 79.1 L435.9 75.1 L459.1 75.9 L482.3 70.2 L505.4 66.9 L528.6 68.6 L551.8 62.9 L575.0 58.8 L598.1 55.5 L621.3 57.2 L644.5 49.9 L667.7 44.2 L690.8 38.5 L714.0 31.1 L714.0 132.0 L42.0 132.0 Z" fill="url(#ar)"/>
     <path d="M42.0 106.8 L65.2 105.2 L88.3 107.6 L111.5 102.7 L134.7 101.1 L157.9 103.5 L181.0 97.8 L204.2 95.4 L227.4 97.0 L250.6 93.8 L273.7 89.7 L296.9 91.3 L320.1 86.5 L343.2 84.0 L366.4 82.4 L389.6 84.8 L412.8 79.1 L435.9 75.1 L459.1 75.9 L482.3 70.2 L505.4 66.9 L528.6 68.6 L551.8 62.9 L575.0 58.8 L598.1 55.5 L621.3 57.2 L644.5 49.9 L667.7 44.2 L690.8 38.5 L714.0 31.1" fill="none" stroke="#FF4D5E" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"/>
     <path d="M42.0 132.0 L65.2 132.0 L88.3 132.0 L111.5 132.0 L134.7 132.0 L157.9 132.0 L181.0 132.0 L204.2 132.0 L227.4 132.0 L250.6 132.0 L273.7 132.0 L296.9 128.3 L320.1 132.0 L343.2 132.0 L366.4 132.0 L389.6 132.0 L412.8 132.0 L435.9 132.0 L459.1 132.0 L482.3 132.0 L505.4 132.0 L528.6 132.0 L551.8 128.3 L575.0 132.0 L598.1 132.0 L621.3 132.0 L644.5 132.0 L667.7 128.3 L690.8 132.0 L714.0 132.0" fill="none" stroke="#9AA1AC" stroke-width="2" stroke-dasharray="4 4" stroke-linejoin="round"/>
     <path d="M714.0 31.1V132.0" stroke="#C9CED6" stroke-dasharray="3 3"/>
     <circle cx="714.0" cy="31.1" r="7" fill="#FF4D5E" opacity=".2"/><circle cx="714.0" cy="31.1" r="3.8" fill="#fff" stroke="#FF4D5E" stroke-width="2.2"/>
    </svg>
    <div class="tip"><s>Sep 30, 2026</s><div><i style="background:#FF4D5E"></i>Cost<b>$1,240</b></div><div><i style="background:#9AA1AC"></i>Paying customers<b>0</b></div></div>
   </div>
   <table class="tb">
    <tr><th>Campaign</th><th>Status</th><th>Cost</th><th>Clicks</th><th>Paying cust.</th></tr>
    <tr><td><i class="dot"></i>Search - Generic</td><td>Learning limited</td><td>$9,860</td><td>5,102</td><td class="z">1</td></tr>
    <tr><td><i class="dot"></i>Performance Max</td><td>Eligible</td><td>$6,140</td><td>3,488</td><td class="z">2</td></tr>
    <tr><td><i class="dot"></i>Search - Brand</td><td>Eligible</td><td>$2,420</td><td>1,222</td><td class="z">0</td></tr>
   </table>
  </div>
 </div>
 <svg class="abs" style="left:0;top:0" width="805" height="420" fill="none" stroke="#E5323F" stroke-linecap="round" stroke-width="3">
  <path d="M44 134C38 100 100 86 150 87C214 88 256 104 254 130C252 160 210 174 152 172C92 170 38 158 42 130C43 120 52 112 66 108"/>
 </svg>
</div></div>
{stack}

<div class="abs cards">
 <div class="c r"><div class="ic"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 3l14 7-6 2-2 6z"/><path d="M14 14l5 5"/></svg></div><div class="t">Google sees:<span class="v">clicks</span></div></div>
 <div class="c g"><div class="ic"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#0B3D24" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.6-3.6 3.2-5.5 6.5-5.5s5.9 1.9 6.5 5.5"/><path d="M15.5 11.5l2 2 4-4.5"/></svg></div><div class="t">Google should see:<span class="v">paying customers</span></div></div>
</div>

<div class="abs foot">Bad tracking shows up as a <b>higher cost per customer.<svg width="330" height="18" viewBox="0 0 330 18" fill="none"><path d="M4 11C90 4 210 4 326 9" stroke="#F2552C" stroke-width="4" stroke-linecap="round"/></svg></b></div>
</body></html>'''
open("index.html","w").write(html)
