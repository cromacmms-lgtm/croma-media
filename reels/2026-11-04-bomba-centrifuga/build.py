#!/usr/bin/env python3
"""Reel: bomba centrífuga funcionando, por dónde puede fallar y cómo se detecta (ilustración y frecuencias de ejemplo)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'engine'))
import croma  # noqa: E402
I = dict(croma.ICONS)


def ic(name, size=28, color='currentColor', sw=1.8):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{I[name]}</svg>')


F = '../../engine/fonts/'
L = '../../engine/logos/'
LV, WH = '#bda8e3', '#ece5fa'

# ---------- ilustración de la bomba (coordenadas de la tarjeta, 960 x 480) ----------
fins = ''.join(f'<line x1="{x}" y1="222" x2="{x}" y2="358" />' for x in range(146, 360, 22))
vanes = ''.join(
    f'<path d="M0,0 C 18,-22 44,-30 62,-24" transform="rotate({k*60})" />' for k in range(6))
pump = f'''
<svg id="pump" width="960" height="480" viewBox="0 0 960 480" style="position:absolute;left:0;top:0">
 <defs>
  <clipPath id="cpl"><rect x="384" y="272" width="82" height="36" rx="6"/></clipPath>
  <clipPath id="sucl"><rect x="842" y="244" width="118" height="52"/></clipPath>
  <clipPath id="disl"><rect x="770" y="0" width="52" height="130"/></clipPath>
 </defs>
 <g fill="none" stroke="{LV}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round">
  <!-- base -->
  <rect x="70" y="384" width="820" height="26" rx="6" fill="rgba(189,168,227,.14)"/>
  <!-- motor -->
  <rect x="78" y="232" width="40" height="116" rx="14" fill="rgba(189,168,227,.10)"/>
  <rect x="112" y="210" width="270" height="160" rx="28" fill="rgba(189,168,227,.12)"/>
  <g stroke="rgba(189,168,227,.55)" stroke-width="3">{fins}</g>
  <rect x="206" y="170" width="84" height="42" rx="8" fill="rgba(189,168,227,.12)"/>
  <rect x="140" y="368" width="40" height="16" rx="3"/><rect x="314" y="368" width="40" height="16" rx="3"/>
  <!-- acople -->
  <rect x="380" y="268" width="90" height="44" rx="8" fill="rgba(189,168,227,.10)"/>
  <g clip-path="url(#cpl)" stroke="rgba(236,229,250,.7)" stroke-width="5"><g id="spin">{''.join(f'<line x1="{x}" y1="270" x2="{x-14}" y2="312"/>' for x in range(370, 500, 20))}</g></g>
  <!-- soporte de rodamientos -->
  <g id="brg"><rect x="470" y="246" width="150" height="88" rx="14" fill="rgba(189,168,227,.12)"/>
   <rect x="482" y="334" width="126" height="50" rx="6"/>
   <circle id="b1c" cx="500" cy="290" r="18" stroke="{WH}"/><circle id="b2c" cx="590" cy="290" r="18" stroke="{WH}"/></g>
  <!-- sello -->
  <rect id="seal" x="620" y="262" width="26" height="56" rx="5" fill="rgba(189,168,227,.18)"/>
  <!-- voluta, impulsor y bridas -->
  <circle cx="740" cy="270" r="112" fill="rgba(189,168,227,.10)"/>
  <rect x="770" y="118" width="52" height="62" fill="rgba(18,15,30,.0)"/>
  <line x1="760" y1="118" x2="832" y2="118" stroke-width="6"/>
  <rect x="846" y="244" width="16" height="52"/>
  <line x1="862" y1="234" x2="862" y2="306" stroke-width="6"/>
  <circle cx="740" cy="270" r="66" stroke="rgba(236,229,250,.5)" fill="rgba(18,15,30,.35)"/>
  <g id="imp" transform="translate(740,270)" stroke="{WH}" stroke-width="4">{vanes}<circle r="12" fill="{WH}"/></g>
  <rect x="700" y="378" width="80" height="8" rx="3"/>
 </g>
 <!-- tuberías y flujo -->
 <g fill="none" stroke="{LV}" stroke-width="4">
  <rect x="770" y="-10" width="52" height="128" fill="rgba(189,168,227,.10)"/>
  <rect x="862" y="244" width="110" height="52" fill="rgba(189,168,227,.10)"/>
 </g>
 <g clip-path="url(#sucl)"><line id="fs" x1="1000" y1="270" x2="840" y2="270" stroke="{WH}" stroke-width="6" stroke-dasharray="18 22" stroke-linecap="round"/></g>
 <g clip-path="url(#disl)"><line id="fd" x1="796" y1="140" x2="796" y2="-10" stroke="{WH}" stroke-width="6" stroke-dasharray="18 22" stroke-linecap="round"/></g>
 <!-- resaltes de cada falla -->
 <rect id="hl0" x="458" y="236" width="174" height="108" rx="20" fill="none" stroke="#f07070" stroke-width="5" opacity="0"/>
 <rect id="hl1" x="610" y="250" width="46" height="80" rx="12" fill="none" stroke="#f07070" stroke-width="5" opacity="0"/>
 <circle id="hl2" cx="740" cy="270" r="84" fill="none" stroke="#f07070" stroke-width="5" opacity="0"/>
 <g id="drops">{''.join(f'<circle id="dp{k}" cx="633" cy="320" r="10" fill="#6f9cf0" opacity="0"/>' for k in range(4))}</g>
 <g id="bubs">{''.join(f'<circle id="bb{k}" cx="740" cy="270" r="6" fill="none" stroke="#fff" stroke-width="2.5" opacity="0"/>' for k in range(10))}</g>
 <g id="heat" opacity="0"><circle cx="545" cy="214" r="26" fill="#3d1717" stroke="#f07070" stroke-width="3"/>
  <g transform="translate(531,200) scale(1.15)" fill="none" stroke="#f7a8a8" stroke-width="2" stroke-linecap="round">{I['termometro']}</g></g>
 <!-- etiquetas del inicio -->
 <g id="labs" font-family="Sora" font-size="22" fill="#c4bbd9" text-anchor="middle">
  <text x="246" y="446">Motor</text><text x="425" y="250">Acople</text><text x="545" y="446">Rodamientos</text><text x="740" y="446">Voluta e impulsor</text>
 </g>
 <!-- checks del final -->
 {''.join(f'<g id="ok{k}" opacity="0"><circle cx="{x}" cy="{y}" r="22" fill="#10301f" stroke="#4fc795" stroke-width="3"/><path d="M{x-9},{y} l6,7 l12,-14" fill="none" stroke="#8fe0bb" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></g>' for k,(x,y) in enumerate([(545,214),(633,226),(740,140)]))}
</svg>'''

scenes = [
    ('01', 'Rodamientos', 'Desgaste de rodamientos', 'Vibración y temperatura por encima de lo normal', 'Análisis de vibraciones y termografía'),
    ('02', 'Sello mecánico', 'Desgaste de las caras del sello', 'Fuga por el sello', 'Inspección visual en cada ronda'),
    ('03', 'Impulsor', 'Cavitación', 'Caída de caudal y de presión, vibración', 'Control de la presión de succión'),
]
panels = ''
for i, (n, comp, falla, sint, det) in enumerate(scenes):
    panels += f'''<div class="pan" id="pn{i}">
  <div class="ph"><b>{n}</b>{comp}</div>
  <div class="pr"><span>Falla</span><p>{falla}</p></div>
  <div class="pr"><span>Síntoma</span><p>{sint}</p></div>
  <div class="pr"><span>Se detecta con</span><p>{det}</p></div></div>'''
freq = [('grafico', 'Análisis de vibraciones', 'Cada 30 días'), ('termometro', 'Termografía', 'Cada 90 días'), ('checklist', 'Ronda de inspección visual', 'Diaria')]
panels += '<div class="pan" id="pn3"><div class="ph" style="gap:14px">Con su frecuencia, en <span style="color:#bda8e3">CROMA</span></div>' + ''.join(
    f'<div class="fr" id="fr{k}"><div class="fi">{ic(n, 34, LV, 1.9)}</div><p>{t}</p><div class="fc">{fq}</div></div>' for k, (n, t, fq) in enumerate(freq)) + \
    '<div class="fn">Frecuencias de ejemplo · se definen según la criticidad del equipo</div></div>'

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
#card{{position:absolute;left:60px;top:500px;width:960px;height:960px;border-radius:48px;overflow:hidden}}
.pan{{position:absolute;left:36px;right:36px;top:500px;height:420px;border-radius:32px;background:rgba(18,15,30,.30);border:1.5px solid rgba(255,255,255,.14);padding:30px 34px}}
.ph{{display:flex;align-items:center;gap:16px;font:700 44px/1 Sora;color:#fff;margin-bottom:22px}}
.ph b{{font:500 26px/1 JBM,monospace;color:#2a1458;background:#bda8e3;padding:9px 12px;border-radius:12px}}
.pr{{display:flex;gap:18px;align-items:baseline;padding:14px 0;border-top:1.5px solid rgba(255,255,255,.10)}}
.pr span{{flex:none;width:250px;font:500 22px/30px JBM,monospace;color:#bda8e3;text-transform:uppercase;letter-spacing:.06em}}
.pr p{{font:600 31px/40px Sora;color:#fff}}
.fr{{display:flex;align-items:center;gap:20px;height:84px;margin-top:14px;padding:0 20px;border-radius:20px;background:rgba(189,168,227,.10);border:1.5px solid rgba(189,168,227,.25)}}
.fi{{width:54px;height:54px;border-radius:15px;background:rgba(189,168,227,.14);display:grid;place-items:center;flex:none}}
.fr p{{flex:1;font:600 29px/34px Sora;color:#fff}}
.fc{{flex:none;padding:10px 16px;border-radius:14px;background:#1b2645;color:#a9c4f7;font:600 22px/1 Sora}}
.fn{{margin-top:16px;font:500 19px/26px JBM,monospace;color:rgba(189,168,227,.8)}}
.cap{{position:absolute;left:60px;right:60px;top:1500px;text-align:center;font:700 56px/66px Sora;letter-spacing:-.02em;color:#fff}}
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

<div class="eti" id="h0" style="top:236px">Bomba centrífuga</div>
<div class="ttl" id="h1" style="top:290px">Por dónde puede</div>
<div class="ttl" id="h2" style="top:384px;color:#bda8e3">fallar.</div>
<div class="ttl" id="h1b" style="top:290px;opacity:0">Se detectan con</div>
<div class="ttl" id="h2b" style="top:388px;color:#bda8e3;opacity:0;font-size:70px">inspecciones predictivas.</div>

<div id="card" class="glass">
  <div id="pwrap" style="position:absolute;left:0;top:10px;width:960px;height:480px">{pump}</div>
  <div class="pan" id="pn_intro" style="display:flex;align-items:center;justify-content:center;text-align:center;font:600 40px/52px Sora;color:#fff">Funcionando normal.<br>Pero cada componente<br>tiene su forma de fallar.</div>
  {panels}
</div>

<div class="endl ttl" id="f1" style="top:640px">Tu bomba avisa<br>antes de fallar.<br><span style="color:#bda8e3">Medila a tiempo.</span></div>
<img class="abs" id="flogo" src="{L}croma-logo-blanco.png" style="left:330px;top:1040px;width:420px">
<div class="endl" id="f2" style="top:1190px;font:500 32px/40px JBM,monospace;color:#bda8e3">@cromacmms</div>

<script>
const DURATION = 21.0;
const $ = id => document.getElementById(id);
const cl = (v,a=0,b=1) => Math.min(b, Math.max(a, v));
const P = (t,a,b) => cl((t-a)/(b-a));
const io = x => x<.5 ? 4*x*x*x : 1-Math.pow(-2*x+2,3)/2;
const oc = x => 1-Math.pow(1-x,3);
const ob = x => {{const c1=1.7,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2);}};
const L = (a,b,x) => a+(b-a)*x;
const S = [2.6, 6.6, 10.6, 14.6];   // inicio de rodamientos, sello, impulsor, predictivas
const END = 18.6;
function pane(el, t, a, b){{ const pin=oc(P(t,a,a+.4)), pout=io(P(t,b-.3,b)); el.style.opacity=pin*(1-pout); el.style.transform=`translateY(${{(1-pin)*30 - pout*20}}px)`; }}

function render(t){{
  $('b1').style.transform=`translate(${{-180+Math.sin(t*.35)*60}}px, ${{420+Math.cos(t*.3)*50}}px)`;
  $('b2').style.transform=`translate(${{380+Math.cos(t*.25)*70}}px, ${{1050+Math.sin(t*.28)*60}}px)`;
  $('b3').style.transform=`translate(${{560+Math.sin(t*.4+1)*80}}px, ${{620+Math.cos(t*.33)*60}}px)`;
  const rm=io(P(t,END-.6,END+.2));
  $('ring').style.transform=`translate(${{L(-320,780,rm)+Math.sin(t*.2)*14}}px, ${{L(560,120,rm)}}px) rotate(${{t*6}}deg)`;
  $('disc').style.transform=`translate(${{-170+Math.cos(t*.3)*12}}px, ${{1660+Math.sin(t*.25)*14}}px)`;

  const hout=io(P(t,END-.6,END-.1));
  const sw=io(P(t,S[3]-.3,S[3]+.1)), swin=oc(P(t,S[3],S[3]+.45));
  [['h0',0,1],['h1',0,1-sw],['h2',.1,1-sw]].forEach(([id,a,k])=>{{ const p=oc(P(t,a,a+.35)); const el=$(id); el.style.opacity=p*(1-hout)*k; el.style.transform=`translateY(${{(1-p)*30 - hout*50 - sw*30}}px)`; }});
  [['h1b',0],['h2b',.1]].forEach(([id,a])=>{{ const p=oc(P(t,S[3]+a,S[3]+a+.45)); const el=$(id); el.style.opacity=p*(1-hout); el.style.transform=`translateY(${{(1-p)*30 - hout*50}}px)`; }});
  const cin=oc(P(t,0.1,0.7)), cout=io(P(t,END-.6,END-.1));
  $('card').style.opacity=cin*(1-cout); $('card').style.transform=`translateY(${{(1-cin)*120 - cout*60}}px) scale(${{L(.95,1,cin)*L(1,.95,cout)}})`;

  // bomba funcionando
  const run = t < S[2] ? 1 : (t < S[3] ? .55 : 1);           // en cavitación baja el caudal
  $('imp').setAttribute('transform', `translate(740,270) rotate(${{t*540}})`);
  $('spin').setAttribute('transform', `translate(${{(t*160)%20}},0)`);
  $('fs').style.strokeDashoffset = -(t*220*run);  $('fd').style.strokeDashoffset = -(t*220*run);
  // vibración en la falla de rodamientos y en cavitación
  const vib = (P(t,S[0]+.4,S[0]+.7)*(1-P(t,S[1]-.3,S[1]))) + .6*(P(t,S[2]+.4,S[2]+.7)*(1-P(t,S[3]-.3,S[3])));
  $('pwrap').style.transform = `translate(${{Math.sin(t*95)*3.5*vib}}px, ${{Math.cos(t*120)*2.5*vib}}px)`;
  $('labs').setAttribute('opacity', oc(P(t,0.6,1.1))*(1-io(P(t,S[0]-.2,S[0]+.2))));

  // resaltes
  for(let i=0;i<3;i++){{ const on = P(t,S[i]+.2,S[i]+.45)*(1-P(t,S[i+1]-.3,S[i+1])); const pulse=.6+.4*Math.sin(t*9);
    $('hl'+i).setAttribute('opacity', on*pulse); }}
  const hb = P(t,S[0]+.2,S[0]+.45)*(1-P(t,S[1]-.3,S[1]));
  ['b1c','b2c'].forEach(id=>$(id).setAttribute('stroke', hb>0.5 ? '#f07070' : '#ece5fa'));
  $('heat').setAttribute('opacity', oc(P(t,S[0]+.9,S[0]+1.2))*(1-P(t,S[1]-.3,S[1])));
  // gotas de la fuga
  for(let k=0;k<4;k++){{ const on = t>S[1]+.6 && t<S[2]-.2; const ph = ((t - S[1] - .6 + k*.35) % 1.4)/1.4;
    const d=$('dp'+k); d.setAttribute('cy', 322 + ph*58); d.setAttribute('opacity', on && t>S[1]+.6+k*.35 ? (1-ph)*.95 : 0); }}
  // burbujas de cavitación
  for(let k=0;k<10;k++){{ const on = t>S[2]+.6 && t<S[3]-.2; const ph = ((t*1.6 + k*.137) % 1); const ang = k*36 + t*120;
    const r = 18 + ph*44; const b=$('bb'+k); b.setAttribute('cx', 740 + Math.cos(ang*Math.PI/180)*r); b.setAttribute('cy', 270 + Math.sin(ang*Math.PI/180)*r);
    b.setAttribute('r', 3 + 5*Math.sin(ph*Math.PI)); b.setAttribute('opacity', on ? Math.sin(ph*Math.PI) : 0); }}
  // checks de las predictivas
  for(let k=0;k<3;k++){{ const p=ob(P(t,S[3]+.3+k*.25,S[3]+.65+k*.25)); const g=$('ok'+k); g.setAttribute('opacity', P(t,S[3]+.3+k*.25,S[3]+.4+k*.25)); }}

  // paneles
  pane($('pn_intro'), t, 0.5, S[0]);
  for(let i=0;i<3;i++) pane($('pn'+i), t, S[i], S[i+1]);
  pane($('pn3'), t, S[3], END-.1);
  for(let k=0;k<3;k++){{ const p=oc(P(t,S[3]+.3+k*.25,S[3]+.7+k*.25)); const r=$('fr'+k); r.style.opacity=p; r.style.transform=`translateX(${{(1-p)*40}}px)`; }}

  const f1=oc(P(t,END,END+.55)); $('f1').style.opacity=f1; $('f1').style.transform=`translateY(${{(1-f1)*40}}px)`;
  const lg=oc(P(t,END+.6,END+1.1)); $('flogo').style.opacity=lg; $('flogo').style.transform=`translateY(${{(1-lg)*24}}px)`;
  $('f2').style.opacity=oc(P(t,END+.9,END+1.3));
}}
render(0);
</script></body></html>'''

open(os.path.join(HERE, 'index.html'), 'w').write(html)
print('ok')
