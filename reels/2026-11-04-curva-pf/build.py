#!/usr/bin/env python3
"""Reel técnico: la curva P-F (curva conceptual)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
F = '../../engine/fonts/'
L = '../../engine/logos/'

# curva conceptual: condición del equipo en función del tiempo
def c(x):
    return 1 - 0.03 * x - 0.95 * x ** 4

OX, OY, W, H = 90, 70, 760, 330
def px(x): return OX + x * W
def py(v): return OY + (1 - v) * H

XS = [i / 200 for i in range(201)]
path = 'M' + ' L'.join(f'{px(x):.1f},{py(c(x)):.1f}' for x in XS)
import math
_seg = [math.hypot(px(XS[i+1])-px(XS[i]), py(c(XS[i+1]))-py(c(XS[i]))) for i in range(200)]
_cum = [0.0]
for d in _seg: _cum.append(_cum[-1]+d)
ARC = [round(v/_cum[-1], 4) for v in _cum]
XP, XF = 0.40, 0.935
pts = [(0.50, 'Ultrasonido'), (0.60, 'Vibraciones'), (0.68, 'Análisis de aceite'),
       (0.75, 'Termografía'), (0.82, 'Ruido audible'), (0.88, 'Calor al tacto')]
dots = ''.join(
    f'<g id="d{i}" opacity="0"><circle cx="{px(x):.1f}" cy="{py(c(x)):.1f}" r="19" fill="#2a1458" stroke="#bda8e3" stroke-width="3.5"/>'
    f'<text x="{px(x):.1f}" y="{py(c(x))+8:.1f}" text-anchor="middle" class="dn">{i+1}</text></g>' for i, (x, _) in enumerate(pts))
legend = ''.join(
    f'<div class="lg" id="l{i}" style="left:{40 + (i // 3) * 450}px;top:{560 + (i % 3) * 70}px"><b>{i+1}</b><span>{t}</span></div>'
    for i, (_, t) in enumerate(pts))
thr = py(0.25)
ticks = ''.join(f'<line id="k{j}" x1="{px(x):.1f}" x2="{px(x):.1f}" y1="{OY+H}" y2="{OY+H-26}" stroke="#bda8e3" stroke-width="5" stroke-linecap="round" opacity="0"/>'
                for j, x in enumerate([XP - (XF - XP) / 2, XP, (XP + XF) / 2, XF]))

html = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<style>
@font-face{{font-family:Sora;font-weight:400;src:url({F}sora-latin-400-normal.woff2)}}
@font-face{{font-family:Sora;font-weight:600;src:url({F}sora-latin-600-normal.woff2)}}
@font-face{{font-family:Sora;font-weight:700;src:url({F}sora-latin-700-normal.woff2)}}
@font-face{{font-family:Sora;font-weight:400;src:url({F}sora-latin-ext-400-normal.woff2);unicode-range:U+0100-024F}}
@font-face{{font-family:Sora;font-weight:600;src:url({F}sora-latin-ext-600-normal.woff2);unicode-range:U+0100-024F}}
@font-face{{font-family:Sora;font-weight:700;src:url({F}sora-latin-ext-700-normal.woff2);unicode-range:U+0100-024F}}
@font-face{{font-family:JBM;font-weight:500;src:url({F}jetbrains-mono-latin-500-normal.woff2)}}
*{{box-sizing:border-box;margin:0}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#120f1e;font-family:Sora,sans-serif;color:#f7f3ff}}
.abs{{position:absolute}}
#bg{{position:absolute;inset:0;overflow:hidden}}
.blob{{position:absolute;border-radius:50%;filter:blur(90px)}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(189,168,227,.07) 2px,transparent 2px),linear-gradient(90deg,rgba(189,168,227,.07) 2px,transparent 2px);background-size:80px 80px}}
.ring{{position:absolute;border-radius:50%;border:64px solid #bda8e3}}
.glass{{background:linear-gradient(140deg,rgba(255,255,255,.16),rgba(255,255,255,.05) 55%,rgba(255,255,255,.09));
  border:2px solid rgba(255,255,255,.24);box-shadow:0 50px 140px rgba(0,0,0,.55),inset 0 2px 0 rgba(255,255,255,.22);
  -webkit-backdrop-filter:blur(30px) saturate(160%);backdrop-filter:blur(30px) saturate(160%)}}
.eti{{position:absolute;left:0;right:0;text-align:center;font:500 32px/40px JBM,monospace;letter-spacing:.18em;color:#bda8e3;text-transform:uppercase}}
.ttl{{position:absolute;left:0;right:0;text-align:center;font:700 84px/94px Sora;letter-spacing:-.025em}}
#card{{position:absolute;left:60px;top:500px;width:960px;height:780px;border-radius:48px;overflow:hidden}}
svg text{{font-family:Sora}}
.ax{{font:400 22px Sora;fill:#c4bbd9}}
.dn{{font:700 21px Sora;fill:#fff}}
.big{{font:700 44px Sora;fill:#fff}}
.lg{{position:absolute;display:flex;align-items:center;gap:16px;font:600 30px/1 Sora;color:#fff}}
.lg b{{width:46px;height:46px;border-radius:50%;background:#2a1458;border:3px solid #bda8e3;display:grid;place-items:center;font:700 22px/1 Sora;flex:none}}
.chip{{position:absolute;padding:12px 18px;border-radius:16px;font:600 25px/1 Sora;white-space:nowrap}}
.cap{{position:absolute;left:60px;right:60px;top:1330px;text-align:center;font:700 60px/70px Sora;letter-spacing:-.02em;color:#fff}}
.cap em{{font-style:normal;color:#bda8e3}}
.endl{{position:absolute;left:0;right:0;text-align:center}}
</style></head><body>
<div id="bg">
  <div class="blob" id="b1" style="width:820px;height:820px;background:#7c4ddb;opacity:.55"></div>
  <div class="blob" id="b2" style="width:900px;height:900px;background:#512974;opacity:.85"></div>
  <div class="blob" id="b3" style="width:520px;height:520px;background:#bda8e3;opacity:.30"></div>
  <div class="grid"></div>
  <div class="ring" id="ring" style="width:560px;height:560px"></div>
  <div class="abs" id="disc" style="width:330px;height:330px;border-radius:50%;background:#7c4ddb"></div>
</div>

<div class="eti" id="h0" style="top:236px">Curva P-F</div>
<div class="ttl" id="h1" style="top:290px">Tu equipo avisa</div>
<div class="ttl" id="h2" style="top:384px;color:#bda8e3">antes de fallar.</div>

<div id="card" class="glass">
 <svg width="960" height="470" viewBox="0 0 960 470" style="position:absolute;left:0;top:10px">
  <g stroke="rgba(255,255,255,.10)" stroke-width="1.5">
   <line x1="{OX}" x2="{OX+W}" y1="{OY+H*0.25}" y2="{OY+H*0.25}"/><line x1="{OX}" x2="{OX+W}" y1="{OY+H*0.5}" y2="{OY+H*0.5}"/>
  </g>
  <line x1="{OX}" y1="{OY-10}" x2="{OX}" y2="{OY+H}" stroke="#c4bbd9" stroke-width="3"/>
  <line x1="{OX}" y1="{OY+H}" x2="{OX+W+20}" y2="{OY+H}" stroke="#c4bbd9" stroke-width="3"/>
  <text class="ax" transform="translate({OX-26},{OY+H/2}) rotate(-90)" text-anchor="middle">Condición del equipo</text>
  <text class="ax" x="{OX+W+20}" y="{OY+H+34}" text-anchor="end">Tiempo</text>
  <line id="thr" x1="{OX}" x2="{OX+W}" y1="{thr:.1f}" y2="{thr:.1f}" stroke="#f07070" stroke-width="3" stroke-dasharray="12 10" opacity="0"/>
  <path id="curve" d="{path}" fill="none" stroke="#bda8e3" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>
  {ticks}
  {dots}
  <g id="gP" opacity="0"><circle cx="{px(XP):.1f}" cy="{py(c(XP)):.1f}" r="16" fill="#fff"/><text class="big" x="{px(XP):.1f}" y="{py(c(XP))-28:.1f}" text-anchor="middle">P</text></g>
  <g id="gF" opacity="0"><circle cx="{px(XF):.1f}" cy="{py(c(XF)):.1f}" r="16" fill="#f07070"/><text class="big" x="{px(XF)+34:.1f}" y="{py(c(XF))+14:.1f}" text-anchor="start" style="fill:#f7a8a8">F</text></g>
  <g id="gB" opacity="0">
   <line x1="{px(XP):.1f}" x2="{px(XF):.1f}" y1="{OY+H+56}" y2="{OY+H+56}" stroke="#fff" stroke-width="4"/>
   <line x1="{px(XP):.1f}" x2="{px(XP):.1f}" y1="{OY+H+44}" y2="{OY+H+68}" stroke="#fff" stroke-width="4"/>
   <line x1="{px(XF):.1f}" x2="{px(XF):.1f}" y1="{OY+H+44}" y2="{OY+H+68}" stroke="#fff" stroke-width="4"/>
  </g>
 </svg>
 <div class="chip" id="cP" style="left:{px(XP)-70:.0f}px;top:{py(c(XP))+10+54:.0f}px;background:#fff;color:#2a1458">Falla potencial</div>
 <div class="chip" id="cF" style="left:{px(XF)-262:.0f}px;top:{py(c(XF))+10+26:.0f}px;background:#3d1717;color:#f7a8a8;border:2px solid rgba(240,112,112,.5)">Falla funcional</div>
 <div class="chip" id="cB" style="left:{(px(XP)+px(XF))/2-118:.0f}px;top:{OY+H+10+66:.0f}px;background:rgba(189,168,227,.22);color:#fff;border:2px solid rgba(189,168,227,.5)">Intervalo P-F</div>
 {legend}
</div>

<div class="cap" id="cA"><em>Punto P:</em> la falla ya<br>empezó, pero no se ve.</div>
<div class="cap" id="cB2">Primero la detecta un<br>instrumento. <em>Al final, tu mano.</em></div>
<div class="cap" id="cC"><em>Intervalo P-F:</em> tu margen<br>para planificar.</div>
<div class="cap" id="cD">Inspeccioná, como mínimo,<br>cada <em>medio intervalo P-F.</em></div>

<div class="endl ttl" id="f1" style="top:640px">Detectar a tiempo<br>es <span style="color:#bda8e3">planificar.</span><br>Tarde, es <span style="color:#bda8e3">correr.</span></div>
<img class="abs" id="flogo" src="{L}croma-logo-blanco.png" style="left:330px;top:1040px;width:420px">
<div class="endl" id="f2" style="top:1190px;font:500 32px/40px JBM,monospace;color:#bda8e3">@cromacmms</div>

<script>
const DURATION = 13.5;
const $ = id => document.getElementById(id);
const cl = (v,a=0,b=1) => Math.min(b, Math.max(a, v));
const P = (t,a,b) => cl((t-a)/(b-a));
const io = x => x<.5 ? 4*x*x*x : 1-Math.pow(-2*x+2,3)/2;
const oc = x => 1-Math.pow(1-x,3);
const ob = x => {{const c1=1.7,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2);}};
const L = (a,b,x) => a+(b-a)*x;
function vis(el, t, a, b, d=0.4, dy=40){{ const pin=oc(P(t,a,a+d)), pout=io(P(t,b,b+d*.8));
  el.style.opacity = pin*(1-pout); el.style.transform=`translateY(${{(1-pin)*dy - pout*dy*.6}}px)`; }}
function pop(el, t, a){{ const k=ob(P(t,a,a+.35)); el.style.opacity=P(t,a,a+.08); el.style.transform=`scale(${{Math.max(0,k)}})`; el.style.transformOrigin='center'; el.style.transformBox='fill-box'; }}
// avance de la curva en x (0..1) según el tiempo
const XP={XP}, XF={XF}, PTS={[x for x,_ in pts]}, ARC={ARC};
function arc(x){{ const f=x*200, i=Math.min(199,Math.floor(f)); return L(ARC[i],ARC[i+1],f-i); }}
function xAt(t){{ if(t<0.7) return 0; if(t<2.4) return L(0, XP, io(P(t,0.7,2.4))); if(t<6.9) return L(XP, XF, P(t,2.6,6.9)); return L(XF, 1, P(t,6.9,7.3)); }}
function tAt(x){{ return 2.6 + (x-XP)/(XF-XP)*(6.9-2.6); }}

function render(t){{
  $('b1').style.transform=`translate(${{-180+Math.sin(t*.35)*60}}px, ${{420+Math.cos(t*.3)*50}}px)`;
  $('b2').style.transform=`translate(${{380+Math.cos(t*.25)*70}}px, ${{1050+Math.sin(t*.28)*60}}px)`;
  $('b3').style.transform=`translate(${{560+Math.sin(t*.4+1)*80}}px, ${{620+Math.cos(t*.33)*60}}px)`;
  $('ring').style.transform=`translate(${{780+Math.sin(t*.2)*14}}px, ${{L(690,120,io(P(t,10.6,11.4)))}}px) rotate(${{t*6}}deg)`;
  $('disc').style.transform=`translate(${{-170+Math.cos(t*.3)*12}}px, ${{1580+Math.sin(t*.25)*14}}px)`;

  const hout=io(P(t,10.6,11.1));
  [['h0',0],['h1',0],['h2',.12]].forEach(([id,a])=>{{ const p=oc(P(t,a,a+.35)); const el=$(id); el.style.opacity=p*(1-hout); el.style.transform=`translateY(${{(1-p)*30 - hout*50}}px)`; }});
  const cin=oc(P(t,0.2,0.8)), cout=io(P(t,10.6,11.1));
  $('card').style.opacity=cin*(1-cout); $('card').style.transform=`translateY(${{(1-cin)*120 - cout*60}}px) scale(${{L(.95,1,cin)*L(1,.95,cout)}})`;

  // curva: la longitud dibujada es aproximadamente proporcional a x (la curva se alarga al final)
  const x=xAt(t); $('curve').style.strokeDashoffset = 1 - arc(x);
  $('thr').setAttribute('opacity', 0.9*oc(P(t,2.8,3.4)));
  pop($('gP'), t, 2.4); const cp=oc(P(t,2.5,2.85)); $('cP').style.opacity=cp; $('cP').style.transform=`translateY(${{(1-cp)*16}}px)`;
  PTS.forEach((px,i)=>{{ const a=tAt(px); pop($('d'+i), t, a); const l=oc(P(t,a,a+.35)); $('l'+i).style.opacity=l; $('l'+i).style.transform=`translateX(${{(1-l)*30}}px)`; }});
  pop($('gF'), t, 6.9); const cf=oc(P(t,7.0,7.35)); $('cF').style.opacity=cf; $('cF').style.transform=`translateY(${{(1-cf)*16}}px)`;
  const br=oc(P(t,7.5,7.95)); $('gB').setAttribute('opacity', br); $('cB').style.opacity=br; $('cB').style.transform=`translateY(${{(1-br)*14}}px)`;
  for(let j=0;j<4;j++){{ const k=oc(P(t,9.1+j*.18,9.35+j*.18)); $('k'+j).setAttribute('opacity', k); }}

  vis($('cA'), t, 0.9, 3.3); vis($('cB2'), t, 3.5, 7.3); vis($('cC'), t, 7.5, 9.0); vis($('cD'), t, 9.1, 10.6);

  const f1=oc(P(t,11.1,11.65)); $('f1').style.opacity=f1; $('f1').style.transform=`translateY(${{(1-f1)*40}}px)`;
  const lg=oc(P(t,11.7,12.2)); $('flogo').style.opacity=lg; $('flogo').style.transform=`translateY(${{(1-lg)*24}}px)`;
  $('f2').style.opacity=oc(P(t,12.0,12.4));
}}
render(0);
</script></body></html>'''

open(os.path.join(HERE, 'index.html'), 'w').write(html)
print('ok')
