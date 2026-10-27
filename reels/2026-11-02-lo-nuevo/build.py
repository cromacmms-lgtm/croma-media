#!/usr/bin/env python3
"""Reel "¿Tu software de mantenimiento hace estas 5 cosas?" (tendencias del rubro, imágenes ilustrativas)."""
import os, sys, random
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'engine'))
import croma  # noqa: E402

I = dict(croma.ICONS)
I['campana'] = '<path d="M6 16.5V11a6 6 0 0 1 12 0v5.5l1.8 1.8H4.2z"/><path d="M10 20.5a2 2 0 0 0 4 0"/>'
I['mic'] = '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5.5 11a6.5 6.5 0 0 0 13 0"/><path d="M12 17.5V21"/>'
I['camara'] = '<path d="M4 8h3l1.6-2.5h6.8L17 8h3v11H4z"/><circle cx="12" cy="13.2" r="3.6"/>'
I['chispa'] = '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 15.5l.7 2 2 .7-2 .7-.7 2-.7-2-2-.7 2-.7z"/>'


def ic(name, size=28, color='currentColor', sw=1.8):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{I[name]}</svg>')


F = '../../engine/fonts/'
L = '../../engine/logos/'

# QR ilustrativo (patrón decorativo, no codifica nada)
random.seed(3)
Nq, cell = 25, 14
qr = []
def finder(x0, y0):
    for y in range(7):
        for x in range(7):
            if x in (0, 6) or y in (0, 6) or (2 <= x <= 4 and 2 <= y <= 4):
                qr.append((x0 + x, y0 + y))
for (fx, fy) in [(0, 0), (Nq - 7, 0), (0, Nq - 7)]:
    finder(fx, fy)
for y in range(Nq):
    for x in range(Nq):
        inf = (x < 8 and y < 8) or (x >= Nq - 8 and y < 8) or (x < 8 and y >= Nq - 8)
        if not inf and random.random() < 0.48:
            qr.append((x, y))
qr_svg = ''.join(f'<rect x="{x*cell}" y="{y*cell}" width="{cell}" height="{cell}"/>' for x, y in qr)

items = [
    ('Código QR en cada equipo', 'Lo escaneás y ves su historial al instante.'),
    ('Fallas reportadas con foto', 'Desde el celular, en el momento y en el lugar.'),
    ('Carga por voz', 'El técnico habla y el sistema lo escribe.'),
    ('Avisos automáticos', 'El preventivo te avisa antes de vencer.'),
    ('IA que sugiere causas', 'Según el historial de fallas de tu planta.'),
]
caps = ''.join(
    f'<div class="it" id="it{i}"><div class="num">0{i+1}</div><div class="itt">{t}</div><div class="its">{s}</div></div>'
    for i, (t, s) in enumerate(items))
segs = ''.join(f'<div class="seg"><b id="sg{i}"></b></div>' for i in range(5))

wave = ''.join(f'<i id="w{k}"></i>' for k in range(32))

vis0 = f'''<div class="vis" id="v0">
  <div class="tagq glass2"><svg width="{Nq*cell}" height="{Nq*cell}" viewBox="0 0 {Nq*cell} {Nq*cell}" fill="#120f1e">{qr_svg}</svg>
   <div class="code" style="margin-top:18px;color:#2a1458;font-size:26px">BOM-03 · Bomba de agua</div></div>
  <div id="scan"></div>
  <div class="okchip" id="ok0">{ic('check', 30, '#8fe0bb', 2.6)}<span>Historial abierto</span></div>
</div>'''
vis1 = f'''<div class="vis" id="v1">
  <div id="vf"><i class="br tl"></i><i class="br tr"></i><i class="br bl"></i><i class="br bm"></i>
    <div id="vfin">{ic('gota', 150, 'rgba(189,168,227,.8)', 1.4)}<div style="font:500 24px/1 JBM,monospace;color:#c4bbd9;margin-top:18px">BOM-03</div></div>
  </div>
  <div id="flash"></div>
  <div class="otc glass2" id="otc"><div class="thumb">{ic('gota', 44, '#bda8e3', 1.6)}</div>
    <div><div class="code">Nuevo aviso de falla</div><div style="font:600 30px/38px Sora;color:#fff">Pérdida de agua · BOM-03</div><div style="font:400 22px/30px Sora;color:#c4bbd9">1 foto · hace un momento</div></div></div>
</div>'''
vis2 = f'''<div class="vis" id="v2">
  <div id="micr"></div><div id="mic">{ic('mic', 96, '#fff', 1.8)}</div>
  <div class="wave">{wave}</div>
  <div class="trans glass2"><span id="tr"></span><span class="caret" id="trc"></span></div>
</div>'''
nots = [('reloj', 'El preventivo de COMP-01 vence mañana', '#f0b240'),
        ('check', 'OT-0418 finalizada · BOM-03 en servicio', '#4fc795'),
        ('alerta', 'Quedan 2 sellos mecánicos en stock', '#f07070')]
vis3 = '<div class="vis" id="v3">' + ''.join(
    f'<div class="nt glass2" id="nt{i}"><div class="nti" style="background:{c}26;border-color:{c}66">{ic(n, 40, c, 2)}</div>'
    f'<div><div class="ntt">Mantenimiento · ahora</div><div class="ntb">{t}</div></div></div>' for i, (n, t, c) in enumerate(nots)) + '</div>'
vis4 = f'''<div class="vis" id="v4">
  <div class="aic glass2" id="aic">
    <div class="code">BOM-03 · Pérdida de agua</div>
    <div style="display:flex;align-items:center;gap:14px;margin-top:22px">{ic('chispa', 44, '#bda8e3', 1.8)}<span style="font:600 30px/1 Sora;color:#fff">Posibles causas</span></div>
    <div class="sug" id="s0"><b>Sello mecánico</b><span>3 fallas parecidas en el año</span></div>
    <div class="sug" id="s1"><b>Junta de la carcasa</b><span>1 falla parecida</span></div>
    <div class="sug" id="s2"><b>Revisar alineación</b><span>Último preventivo: 02/10</span></div>
  </div>
</div>'''

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
.glass2{{background:linear-gradient(150deg,rgba(255,255,255,.13),rgba(255,255,255,.05));border:1.5px solid rgba(255,255,255,.18);box-shadow:0 24px 60px rgba(0,0,0,.35),inset 0 1px 0 rgba(255,255,255,.15)}}
.eti{{position:absolute;left:0;right:0;text-align:center;font:500 32px/40px JBM,monospace;letter-spacing:.18em;color:#bda8e3;text-transform:uppercase}}
.ttl{{font:700 96px/104px Sora;letter-spacing:-.03em}}
.code{{font:500 24px/30px JBM,monospace;letter-spacing:.05em;color:#bda8e3}}
#hook{{position:absolute;left:70px;right:70px;top:640px;text-align:center}}
#prog{{position:absolute;left:120px;right:120px;top:300px;display:flex;gap:14px}}
.seg{{flex:1;height:8px;border-radius:4px;background:rgba(255,255,255,.14);overflow:hidden}}
.seg b{{display:block;height:100%;width:0;background:#bda8e3;border-radius:4px}}
#card{{position:absolute;left:110px;top:380px;width:860px;height:760px;border-radius:52px;overflow:hidden}}
.vis{{position:absolute;inset:0}}
.it{{position:absolute;left:70px;right:70px;top:1190px;text-align:center}}
.num{{font:500 30px/40px JBM,monospace;letter-spacing:.14em;color:#bda8e3}}
.itt{{font:700 70px/80px Sora;letter-spacing:-.02em;color:#fff;margin-top:8px}}
.its{{font:400 36px/48px Sora;color:#d9ccf2;margin-top:16px}}
/* 1 qr */
.tagq{{position:absolute;left:190px;top:110px;width:480px;height:520px;border-radius:36px;background:#f7f3ff;display:flex;flex-direction:column;align-items:center;justify-content:center}}
#scan{{position:absolute;left:170px;width:520px;height:8px;border-radius:4px;background:#7c4ddb;box-shadow:0 0 40px 10px rgba(124,77,219,.7)}}
.okchip{{position:absolute;left:250px;top:640px;width:360px;height:76px;border-radius:24px;background:#10301f;border:2px solid rgba(79,199,149,.5);display:flex;align-items:center;justify-content:center;gap:14px;font:600 28px/1 Sora;color:#8fe0bb}}
/* 2 foto */
#vf{{position:absolute;left:150px;top:80px;width:560px;height:440px;border-radius:30px;background:rgba(18,15,30,.35)}}
.br{{position:absolute;width:70px;height:70px;border:6px solid #fff}}
.br.tl{{left:-3px;top:-3px;border-right:0;border-bottom:0;border-radius:30px 0 0 0}}
.br.tr{{right:-3px;top:-3px;border-left:0;border-bottom:0;border-radius:0 30px 0 0}}
.br.bl{{left:-3px;bottom:-3px;border-right:0;border-top:0;border-radius:0 0 0 30px}}
.br.bm{{right:-3px;bottom:-3px;border-left:0;border-top:0;border-radius:0 0 30px 0}}
#vfin{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center}}
#flash{{position:absolute;inset:0;background:#fff;opacity:0}}
.otc{{position:absolute;left:60px;right:60px;top:560px;height:150px;border-radius:30px;display:flex;align-items:center;gap:24px;padding:0 28px}}
.thumb{{width:100px;height:100px;border-radius:22px;background:linear-gradient(135deg,#512974,#7c4ddb);display:grid;place-items:center;flex:none}}
/* 3 voz */
#mic{{position:absolute;left:350px;top:110px;width:160px;height:160px;border-radius:50%;background:#7c4ddb;display:grid;place-items:center}}
#micr{{position:absolute;left:350px;top:110px;width:160px;height:160px;border-radius:50%;border:4px solid #bda8e3}}
.wave{{position:absolute;left:150px;right:150px;top:320px;height:140px;display:flex;align-items:center;justify-content:center;gap:8px}}
.wave i{{display:block;width:10px;border-radius:5px;background:#bda8e3}}
.trans{{position:absolute;left:60px;right:60px;top:500px;min-height:180px;border-radius:30px;padding:30px 34px;font:600 34px/46px Sora;color:#fff}}
.caret{{display:inline-block;width:4px;height:40px;background:#bda8e3;margin-left:4px;vertical-align:-6px}}
/* 4 avisos */
.nt{{position:absolute;left:60px;right:60px;height:150px;border-radius:34px;display:flex;align-items:center;gap:26px;padding:0 30px}}
.nti{{width:86px;height:86px;border-radius:24px;border:2px solid;display:grid;place-items:center;flex:none}}
.ntt{{font:500 21px/26px JBM,monospace;color:#c4bbd9;letter-spacing:.04em}}
.ntb{{font:600 31px/40px Sora;color:#fff;margin-top:6px}}
/* 5 ia */
.aic{{position:absolute;left:60px;right:60px;top:70px;bottom:70px;border-radius:36px;padding:40px}}
.sug{{margin-top:22px;height:118px;border-radius:24px;background:rgba(189,168,227,.12);border:1.5px solid rgba(189,168,227,.3);display:flex;flex-direction:column;justify-content:center;padding:0 28px}}
.sug b{{font:600 32px/40px Sora;color:#fff}} .sug span{{font:400 23px/30px Sora;color:#c4bbd9}}
#note{{position:absolute;left:0;right:0;top:1150px;text-align:center;font:500 22px/30px JBM,monospace;letter-spacing:.06em;color:rgba(189,168,227,.75)}}
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

<div id="hook"><div class="eti" style="position:relative;margin-bottom:30px" id="h0">Software de mantenimiento</div>
  <div class="ttl" id="h1">¿El tuyo hace</div><div class="ttl" id="h2" style="color:#bda8e3">estas 5 cosas?</div></div>

<div id="prog">{segs}</div>
<div id="card" class="glass">{vis0}{vis1}{vis2}{vis3}{vis4}</div>
<div id="note">Imágenes ilustrativas</div>
{caps}

<div class="endl ttl" id="f1" style="top:640px">¿Cuántas<br>tiene <span style="color:#bda8e3">el tuyo?</span></div>
<div class="endl" id="f2" style="top:900px;font:400 40px/52px Sora;color:#d9ccf2">Contanos en los comentarios.</div>
<img class="abs" id="flogo" src="{L}croma-logo-blanco.png" style="left:330px;top:1060px;width:420px">
<div class="endl" id="f3" style="top:1210px;font:500 32px/40px JBM,monospace;color:#bda8e3">@cromacmms</div>

<script>
const DURATION = 16.0;
const $ = id => document.getElementById(id);
const cl = (v,a=0,b=1) => Math.min(b, Math.max(a, v));
const P = (t,a,b) => cl((t-a)/(b-a));
const io = x => x<.5 ? 4*x*x*x : 1-Math.pow(-2*x+2,3)/2;
const oc = x => 1-Math.pow(1-x,3);
const ob = x => {{const c1=1.6,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2);}};
const L = (a,b,x) => a+(b-a)*x;
const S0 = 2.0, D = 2.2;          // cada ítem dura D segundos desde S0
const TXT = 'Compresor 1: cambié el filtro de aire. Quedó en servicio.';
function fade(el, p, dy=40){{ el.style.opacity=p; el.style.transform=`translateY(${{(1-p)*dy}}px)`; }}

function render(t){{
  $('b1').style.transform=`translate(${{-180+Math.sin(t*.35)*60}}px, ${{420+Math.cos(t*.3)*50}}px)`;
  $('b2').style.transform=`translate(${{380+Math.cos(t*.25)*70}}px, ${{1050+Math.sin(t*.28)*60}}px)`;
  $('b3').style.transform=`translate(${{560+Math.sin(t*.4+1)*80}}px, ${{620+Math.cos(t*.33)*60}}px)`;
  $('ring').style.transform=`translate(${{740+Math.sin(t*.2)*14}}px, ${{140}}px) rotate(${{t*6}}deg)`;
  $('disc').style.transform=`translate(${{-170+Math.cos(t*.3)*12}}px, ${{1580+Math.sin(t*.25)*14}}px)`;

  // gancho
  const hout=io(P(t,1.7,2.05));
  [['h0',0],['h1',.08],['h2',.22]].forEach(([id,a])=>{{ const p=oc(P(t,a,a+.5)); const el=$(id); el.style.opacity=p*(1-hout); el.style.transform=`translateY(${{(1-p)*50 - hout*80}}px) scale(${{L(1,.96,hout)}})`; }});

  // tarjeta, progreso y textos
  const END = S0 + 5*D;
  const cin=oc(P(t,S0-.15,S0+.35)), cout=io(P(t,END-.1,END+.35));
  $('card').style.opacity=cin*(1-cout); $('card').style.transform=`translateY(${{(1-cin)*120 - cout*80}}px) scale(${{L(.94,1,cin)*L(1,.94,cout)}})`;
  $('prog').style.opacity=cin*(1-cout); $('note').style.opacity=cin*(1-cout)*.9;
  for(let i=0;i<5;i++){{
    const a=S0+i*D, b=a+D;
    $('sg'+i).style.width = (P(t,a,b)*100)+'%';
    const pin=oc(P(t,a+.05,a+.45)), pout=io(P(t,b-.25,b));
    const last = i===4; const po = last ? io(P(t,END-.1,END+.3)) : pout;
    const it=$('it'+i); it.style.opacity=pin*(1-po); it.style.transform=`translateY(${{(1-pin)*40 - po*30}}px)`;
    const v=$('v'+i); const vin=oc(P(t,a,a+.35)), vout=io(P(t,b-.2,b)); v.style.opacity = vin*(last?1:(1-vout)); v.style.transform=`translateX(${{(1-vin)*80 - (last?0:vout*80)}}px)`;
  }}
  // 1: QR
  {{ const a=S0; const sp=P(t,a+.3,a+1.3); $('scan').style.top = (L(110,620,io(sp)))+'px'; $('scan').style.opacity = (sp>0 && sp<1)?1:0;
     const k=ob(P(t,a+1.3,a+1.6)); $('ok0').style.opacity=P(t,a+1.3,a+1.4); $('ok0').style.transform=`scale(${{Math.max(0,k)}})`; }}
  // 2: foto
  {{ const a=S0+D; const fl=P(t,a+.55,a+.6)*(1-P(t,a+.6,a+.95)); $('flash').style.opacity=fl*.85;
     const z=io(P(t,a+.2,a+.55)); $('vf').style.transform=`scale(${{L(1.06,1,z)}})`;
     const k=ob(P(t,a+.9,a+1.3)); const o=$('otc'); o.style.opacity=P(t,a+.9,a+1.0); o.style.transform=`translateY(${{(1-Math.min(1,k))*60}}px) scale(${{L(.9,1,Math.min(1.05,k))}})`; }}
  // 3: voz
  {{ const a=S0+2*D; const r=((t-a)%0.9)/0.9; const on = t>a && t<a+D; $('micr').style.transform=`scale(${{1+r*.7}})`; $('micr').style.opacity= on ? (1-r)*.8 : 0;
     for(let k=0;k<32;k++){{ const h = on ? 18 + 100*Math.abs(Math.sin(t*7.3 + k*0.7) * Math.sin(t*3.1 + k*1.3)) * (0.4+0.6*Math.sin(k/31*Math.PI)) : 18; $('w'+k).style.height=h+'px'; }}
     const n=Math.floor(P(t,a+.35,a+1.75)*TXT.length+0.0001); $('tr').textContent=TXT.slice(0,n); $('trc').style.opacity = Math.floor(t*4)%2===0 ? 1:0; }}
  // 4: avisos
  {{ const a=S0+3*D; for(let i=0;i<3;i++){{ const k=ob(P(t,a+.2+i*.4,a+.6+i*.4)); const el=$('nt'+i);
     el.style.top = (L(-180, 90 + i*190, Math.min(1,k)))+'px'; el.style.opacity=P(t,a+.2+i*.4,a+.35+i*.4); el.style.transform=`scale(${{L(.92,1,Math.min(1,k))}})`; }} }}
  // 5: IA
  {{ const a=S0+4*D; for(let i=0;i<3;i++){{ const p=oc(P(t,a+.4+i*.3,a+.8+i*.3)); const el=$('s'+i); el.style.opacity=p; el.style.transform=`translateX(${{(1-p)*50}}px)`; }}
     const g=io(P(t,a+1.4,a+1.7)); $('s0').style.borderColor=`rgba(189,168,227,${{.3+.6*g}})`; $('s0').style.boxShadow=`0 0 ${{40*g}}px rgba(189,168,227,${{.4*g}})`; }}

  // cierre
  const f1=oc(P(t,END+.3,END+.85)); fade($('f1'), f1);
  fade($('f2'), oc(P(t,END+.65,END+1.1)), 24);
  const lg=oc(P(t,END+1.0,END+1.5)); fade($('flogo'), lg, 24);
  fade($('f3'), oc(P(t,END+1.3,END+1.7)), 14);
}}
render(0);
</script></body></html>'''

open(os.path.join(HERE, 'index.html'), 'w').write(html)
print('ok')
