#!/usr/bin/env python3
"""Reel "Cuando el jefe pregunta qué pasó con la bomba 3": sin sistema vs. con software (situación y datos de ejemplo)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'engine'))
import croma  # noqa: E402

I = dict(croma.ICONS)
I['campana'] = '<path d="M6 16.5V11a6 6 0 0 1 12 0v5.5l1.8 1.8H4.2z"/><path d="M10 20.5a2 2 0 0 0 4 0"/>'
I['play'] = '<path d="M8 5.5v13l10-6.5z"/>'
I['imagen'] = '<rect x="3" y="4.5" width="18" height="15" rx="2.5"/><circle cx="9" cy="10" r="1.8"/><path d="m4 18 5.5-5 4 3.5 3-2.5L21 17"/>'


def ic(name, size=28, color='currentColor', sw=1.8):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{I[name]}</svg>')


F = '../../engine/fonts/'
L = '../../engine/logos/'

# ---------- chat del grupo (situación ilustrativa) ----------
ROLES = {'S': ('Supervisor', '#bda8e3'), 'N': ('Turno noche', '#f0b240'), 'T': ('Técnico 2', '#6f9cf0'),
         'M': ('Turno mañana', '#4fc795'), 'U': ('Técnico 1', '#f07070')}
msgs = [
    ('S', '¿Alguien sabe qué le hicieron a la bomba 3?'),
    ('N', 'Yo no la toqué'),
    ('T', 'Creo que el martes le cambiaron algo'),
    ('T', '[img]IMG_2041.jpg'),
    ('T', 'Ah no, esa es la bomba 2'),
    ('S', '¿Cuál es la 3? ¿La de atrás?'),
    ('M', '[audio]2:47'),
    ('U', 'Preguntale al que estaba de vacaciones'),
    ('S', 'Está de vacaciones'),
    ('T', 'El repuesto lo pidió alguien, no sé quién'),
    ('U', 'Hay una planilla en la compu de la oficina'),
    ('S', '¿Qué compu?'),
    ('T', 'La que no anda'),
    ('N', '¿La bomba 3 no era la que cambiaron de lugar?'),
    ('S', '...'),
]
chat = ''
y = 24
for i, (r, txt) in enumerate(msgs):
    name, col = ROLES[r]
    if txt.startswith('[img]'):
        body = (f'<div class="att">{ic("imagen", 40, "#bda8e3")}<span>{txt[5:]}</span></div>')
        h = 150
    elif txt.startswith('[audio]'):
        wave = ''.join(f'<i style="height:{8 + (k*37 % 26)}px"></i>' for k in range(26))
        body = f'<div class="aud">{ic("play", 26, "#fff", 2)}<div class="wv">{wave}</div><span>{txt[7:]}</span></div>'
        h = 132
    else:
        body = f'<div class="tx">{txt}</div>'
        h = 112 if len(txt) < 26 else 150
    chat += (f'<div class="msg" style="top:{y}px"><div class="av" style="background:{col}">{name[0]}</div>'
             f'<div class="bub"><div class="who" style="color:{col}">{name}</div>{body}</div></div>')
    y += h + 18
CHAT_H = y

# ---------- historial del equipo (datos de ejemplo) ----------
hist = [
    ('14/10', 'Correctivo', 'Pérdida por el sello mecánico', 'Cambio de sello · 2,5 h · OT-0418', 'Finalizada', 'ok'),
    ('02/10', 'Preventivo', 'Inspección mensual', 'Sin novedades · 0,5 h · OT-0391', 'Finalizada', 'ok'),
    ('18/09', 'Correctivo', 'Ruido en el rodamiento lado acople', 'Cambio de rodamiento · 3 h · OT-0350', 'Finalizada', 'ok'),
    ('04/11', 'Preventivo', 'Alineación y engrase', 'Programado · responsable: turno mañana', 'Programada', 'info'),
]
rows = ''
for i, (d, k, tt, sub, st, cls) in enumerate(hist):
    rows += (f'<div class="hrow" id="h{i}" style="top:{326 + i*146}px"><div class="hd8">{d}</div>'
             f'<div class="hb"><div class="hk {"corr" if k=="Correctivo" else "prev"}">{k}</div><div class="ht">{tt}</div><div class="hs">{sub}</div></div>'
             f'<div class="st {cls}"><i></i>{st}</div></div>')

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
.cap{{position:absolute;left:60px;right:60px;text-align:center;font:700 64px/74px Sora;letter-spacing:-.02em;color:#fff}}
.cap em{{font-style:normal;color:#bda8e3}}
/* notificación */
#notif{{position:absolute;left:90px;width:900px;height:170px;top:560px;border-radius:40px;display:flex;align-items:center;gap:28px;padding:0 36px}}
#notif .ico{{width:96px;height:96px;border-radius:26px;background:#7c4ddb;display:grid;place-items:center;flex:none}}
#notif .n1{{font:600 26px/32px Sora;color:#c4bbd9;display:flex;justify-content:space-between;width:680px}}
#notif .n2{{font:700 38px/48px Sora;color:#fff;margin-top:8px}}
/* teléfono */
#phone{{position:absolute;left:250px;top:330px;width:580px;height:1010px;border-radius:64px;overflow:hidden}}
#phone .bar{{position:absolute;left:0;right:0;top:0;height:150px;border-bottom:1.5px solid rgba(255,255,255,.14);display:flex;align-items:center;gap:20px;padding:40px 30px 0}}
#phone .gav{{width:66px;height:66px;border-radius:50%;background:rgba(189,168,227,.25);border:1.5px solid rgba(189,168,227,.5);display:grid;place-items:center;flex:none}}
#phone .gt{{font:600 28px/34px Sora;color:#fff}} #phone .gs{{font:400 20px/26px Sora;color:#c4bbd9}}
#vp{{position:absolute;left:0;right:0;top:152px;bottom:0;overflow:hidden}}
#chat{{position:absolute;left:0;right:0;top:0;height:{CHAT_H}px}}
.msg{{position:absolute;left:22px;right:22px;display:flex;gap:14px;align-items:flex-start}}
.av{{width:50px;height:50px;border-radius:50%;flex:none;display:grid;place-items:center;font:700 22px/1 Sora;color:#2a1458;margin-top:6px}}
.bub{{max-width:440px;padding:14px 20px 16px;border-radius:8px 26px 26px 26px;background:rgba(255,255,255,.10);border:1.5px solid rgba(255,255,255,.12)}}
.who{{font:600 19px/24px Sora;margin-bottom:4px}}
.tx{{font:400 25px/34px Sora;color:#fff}}
.att{{display:flex;align-items:center;gap:14px;width:330px;height:84px;border-radius:16px;background:rgba(189,168,227,.14);padding:0 18px;font:500 20px/1 JBM,monospace;color:#ece5fa}}
.aud{{display:flex;align-items:center;gap:14px;width:360px;height:60px}}
.aud .wv{{flex:1;display:flex;align-items:center;gap:4px}} .aud .wv i{{display:block;width:5px;border-radius:3px;background:#bda8e3}}
.aud span{{font:500 20px/1 JBM,monospace;color:#c4bbd9}}
.timer{{position:absolute;display:flex;align-items:center;gap:12px;padding:16px 24px;border-radius:22px;font:600 34px/1 JBM,monospace}}
#t1{{left:690px;top:258px;background:#3d1717;color:#f7a8a8;border:2px solid rgba(240,112,112,.5)}}
#t2{{left:690px;top:258px;background:#10301f;color:#8fe0bb;border:2px solid rgba(79,199,149,.5)}}
/* panel con software */
#panel{{position:absolute;left:60px;top:330px;width:960px;height:932px;border-radius:44px;overflow:hidden}}
.srch{{position:absolute;left:36px;right:36px;top:36px;height:84px;border-radius:24px;background:rgba(255,255,255,.08);border:1.5px solid rgba(255,255,255,.16);display:flex;align-items:center;gap:18px;padding-left:28px;font:500 32px/1 JBM,monospace;color:#fff}}
.caret{{display:inline-block;width:3px;height:38px;background:#bda8e3;margin-left:2px}}
#eqh{{position:absolute;left:36px;right:36px;top:146px;height:156px;border-radius:28px;background:linear-gradient(150deg,rgba(255,255,255,.11),rgba(255,255,255,.04));border:1.5px solid rgba(255,255,255,.14);padding:28px}}
.ib{{width:84px;height:84px;border-radius:22px;background:rgba(189,168,227,.14);border:1.5px solid rgba(189,168,227,.25);display:grid;place-items:center;position:absolute;left:28px;top:28px}}
.code{{font:500 22px/28px JBM,monospace;letter-spacing:.06em;color:#bda8e3}}
.st{{display:flex;align-items:center;gap:10px;padding:11px 16px;border-radius:15px;font:600 20px/1 Sora;flex:none}}
.st i{{display:inline-block;width:12px;height:12px;border-radius:50%}}
.st.ok{{background:#10301f;color:#8fe0bb}} .st.ok i{{background:#4fc795}}
.st.info{{background:#1b2645;color:#a9c4f7}} .st.info i{{background:#6f9cf0}}
.mini{{position:absolute;top:126px;display:flex;flex-direction:column;gap:4px}}
.mini span{{font:400 18px/22px Sora;color:#c4bbd9}} .mini b{{font:700 30px/34px Sora;color:#fff}}
.htitle{{position:absolute;left:40px;top:358px;font:600 26px/32px Sora;color:#fff;display:none}}
.hrow{{position:absolute;left:36px;right:36px;height:130px;border-radius:24px;background:rgba(255,255,255,.06);border:1.5px solid rgba(255,255,255,.12);display:flex;align-items:center;gap:22px;padding:0 22px}}
.hd8{{font:600 24px/1 JBM,monospace;color:#bda8e3;width:92px;flex:none}}
.hb{{flex:1;min-width:0}}
.hk{{display:inline-block;font:600 16px/1 Sora;padding:6px 10px;border-radius:8px;margin-bottom:6px}}
.hk.corr{{background:rgba(240,112,112,.18);color:#f7a8a8}} .hk.prev{{background:rgba(189,168,227,.18);color:#d9ccf2}}
.ht{{font:600 27px/34px Sora;color:#fff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.hs{{font:400 20px/28px Sora;color:#c4bbd9;white-space:nowrap}}
#note{{position:absolute;left:0;right:0;top:1300px;text-align:center;font:500 22px/30px JBM,monospace;letter-spacing:.06em;color:rgba(189,168,227,.75)}}
.endl{{position:absolute;left:0;right:0;text-align:center}}
.ttl{{font:700 84px/96px Sora;letter-spacing:-.025em}}
</style></head><body>
<div id="bg">
  <div class="blob" id="b1" style="width:820px;height:820px;background:#7c4ddb;opacity:.55"></div>
  <div class="blob" id="b2" style="width:900px;height:900px;background:#512974;opacity:.85"></div>
  <div class="blob" id="b3" style="width:520px;height:520px;background:#bda8e3;opacity:.30"></div>
  <div class="grid"></div>
  <div class="ring" id="ring" style="width:560px;height:560px"></div>
  <div class="abs" id="disc" style="width:330px;height:330px;border-radius:50%;background:#7c4ddb"></div>
</div>

<!-- 1: la pregunta -->
<div id="notif" class="glass">
  <div class="ico">{ic('campana', 52, '#fff', 2)}</div>
  <div><div class="n1"><span>Jefe de planta</span><span>ahora</span></div><div class="n2">¿Qué pasó con la bomba 3?</div></div>
</div>
<div class="cap" id="c1" style="top:820px">Cuando el jefe<br>pregunta qué pasó<br>con la <em>bomba 3…</em></div>

<!-- 2: sin sistema -->
<div class="eti" id="e2" style="top:250px;text-align:left;left:250px">Sin sistema</div>
<div class="timer" id="t1">{ic('reloj', 36, '#f7a8a8', 2.2)}<span id="t1v">00:00</span></div>
<div id="phone" class="glass">
  <div class="bar"><div class="gav">{ic('llave', 34, '#fff')}</div><div><div class="gt">Mantenimiento</div><div class="gs">Grupo · 23 participantes</div></div></div>
  <div id="vp"><div id="chat">{chat}</div></div>
</div>
<div class="cap" id="c2" style="top:1400px"><em>Sin sistema:</em> 20 minutos<br>buscando en el grupo.</div>

<!-- 3: con software -->
<div class="eti" id="e3" style="top:250px;text-align:left;left:60px">Con software</div>
<div class="timer" id="t2">{ic('reloj', 36, '#8fe0bb', 2.2)}<span id="t2v">0 s</span></div>
<div id="panel" class="glass">
  <div class="srch">{ic('lupa', 34, '#c4bbd9')}<span id="q"></span><span class="caret" id="caret"></span></div>
  <div id="eqh">
    <div class="ib">{ic('gota', 44, '#bda8e3')}</div>
    <div style="position:absolute;left:136px;top:30px"><div class="code">BOM-03</div><div style="font:600 34px/42px Sora;color:#fff">Bomba de agua</div><div style="font:400 21px/28px Sora;color:#c4bbd9">Planta de tratamiento</div></div>
    <div class="st ok" style="position:absolute;right:28px;top:30px"><i></i>En servicio</div>
    <div class="mini" style="left:600px;top:96px;display:none"></div>
  </div>
  {rows}
</div>
<div id="note">Interfaz ilustrativa · datos de ejemplo</div>
<div class="cap" id="c3" style="top:1400px"><em>Con software:</em> la<br>respuesta en 3 segundos.</div>

<!-- 4: cierre -->
<div class="endl ttl" id="f1" style="top:640px">Que la información<br>no dependa de<br><span style="color:#bda8e3">quién se acuerda.</span></div>
<img class="abs" id="flogo" src="{L}croma-logo-blanco.png" style="left:330px;top:1040px;width:420px">
<div class="endl" id="f2" style="top:1190px;font:500 32px/40px JBM,monospace;color:#bda8e3">@cromacmms</div>

<script>
const DURATION = 15.0;
const $ = id => document.getElementById(id);
const cl = (v,a=0,b=1) => Math.min(b, Math.max(a, v));
const P = (t,a,b) => cl((t-a)/(b-a));
const io = x => x<.5 ? 4*x*x*x : 1-Math.pow(-2*x+2,3)/2;
const oc = x => 1-Math.pow(1-x,3);
const ob = x => {{const c1=1.5,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2);}};
const L = (a,b,x) => a+(b-a)*x;
function vis(el, t, a, b, d=0.45, dy=40){{ const pin=oc(P(t,a,a+d)), pout=io(P(t,b,b+d*.8));
  el.style.opacity = pin*(1-pout); el.style.transform=`translateY(${{(1-pin)*dy - pout*dy*.6}}px)`; }}
const CHAT_H = {CHAT_H}, VP = 1010-152;
const Q = 'BOM-03';

function render(t){{
  $('b1').style.transform=`translate(${{-180+Math.sin(t*.35)*60}}px, ${{420+Math.cos(t*.3)*50}}px)`;
  $('b2').style.transform=`translate(${{380+Math.cos(t*.25)*70}}px, ${{1050+Math.sin(t*.28)*60}}px)`;
  $('b3').style.transform=`translate(${{560+Math.sin(t*.4+1)*80}}px, ${{620+Math.cos(t*.33)*60}}px)`;
  const rm=io(P(t,12.0,12.8));
  $('ring').style.transform=`translate(${{L(700,800,rm)+Math.sin(t*.2)*14}}px, ${{L(160,60,rm)}}px) rotate(${{t*6}}deg)`;
  $('disc').style.transform=`translate(${{-170+Math.cos(t*.3)*12}}px, ${{1580+Math.sin(t*.25)*14}}px)`;

  // 1: notificación + gancho
  const n=$('notif'); const nin=ob(P(t,0.0,0.55)), nout=io(P(t,2.35,2.75));
  n.style.opacity = P(t,0,.2)*(1-nout); n.style.transform=`translateY(${{(1-nin)*-120 - nout*200}}px) scale(${{L(.94,1,nin)}})`;
  vis($('c1'), t, 0.25, 2.35, .5, 50);

  // 2: sin sistema
  const pin=oc(P(t,2.55,3.15)), pout=io(P(t,7.75,8.2));
  const ph=$('phone'); ph.style.opacity=pin*(1-pout); ph.style.transform=`translate(${{-pout*700}}px, ${{(1-pin)*140}}px) scale(${{L(.92,1,pin)}}) rotate(${{-pout*8}}deg)`;
  vis($('e2'), t, 2.6, 7.75, .4, 20);
  const sp = Math.pow(P(t,3.0,7.6), 1.8);
  $('chat').style.transform=`translateY(${{-sp*(CHAT_H-VP+40)}}px)`;
  const t1=$('t1'); vis(t1, t, 2.8, 7.75, .4, 20);
  const secs = Math.round(Math.pow(P(t,3.0,7.5),1.6)*(20*60+14));
  $('t1v').textContent = String(Math.floor(secs/60)).padStart(2,'0')+':'+String(secs%60).padStart(2,'0')+(t>3.0?' min':'');
  const shake = t>7.3 && t<7.75 ? Math.sin(t*90)*4 : 0; t1.style.marginLeft = shake+'px';
  vis($('c2'), t, 3.2, 7.75, .45, 40);

  // 3: con software
  const qin=oc(P(t,8.0,8.6)), qout=io(P(t,12.0,12.45));
  const pa=$('panel'); pa.style.opacity=qin*(1-qout); pa.style.transform=`translate(${{(1-qin)*600}}px, ${{-qout*60}}px) scale(${{L(1,.94,qout)}})`;
  vis($('e3'), t, 8.1, 12.0, .4, 20);
  const typed = Math.floor(P(t,8.55,9.05)*Q.length+0.0001); $('q').textContent = Q.slice(0, typed);
  $('caret').style.opacity = (t<9.3 && Math.floor(t*4)%2===0) || (t>=8.55 && t<9.1) ? 1 : 0;
  const eh=oc(P(t,9.15,9.55)); $('eqh').style.opacity=eh; $('eqh').style.transform=`translateY(${{(1-eh)*30}}px)`;
  for(let i=0;i<4;i++){{ const p=oc(P(t,9.35+i*.12,9.8+i*.12)); const r=$('h'+i); r.style.opacity=p; r.style.transform=`translateY(${{(1-p)*30}}px)`; }}
  const hl = io(P(t,10.3,10.6));
  $('h0').style.borderColor=`rgba(189,168,227,${{.12+.6*hl}})`; $('h0').style.background=`rgba(189,168,227,${{.06+.12*hl}})`;
  $('h0').style.boxShadow=`0 0 ${{50*hl}}px rgba(189,168,227,${{.35*hl}})`;
  const t2=$('t2'); vis(t2, t, 8.2, 12.0, .4, 20);
  $('t2v').textContent = Math.min(3, Math.floor(P(t,8.55,9.6)*3+0.0001)) + ' s';
  const pop = ob(P(t,9.6,9.9)); t2.style.scale = t>9.6 && t<9.9 ? L(1.12,1,pop) : 1;
  $('note').style.opacity = oc(P(t,9.2,9.6))*(1-io(P(t,11.9,12.3)));
  vis($('c3'), t, 8.7, 12.0, .45, 40);

  // 4: cierre
  const f1=oc(P(t,12.55,13.15)); $('f1').style.opacity=f1; $('f1').style.transform=`translateY(${{(1-f1)*40}}px)`;
  const lg=oc(P(t,13.2,13.7)); $('flogo').style.opacity=lg; $('flogo').style.transform=`translateY(${{(1-lg)*24}}px)`;
  const f2=oc(P(t,13.5,13.9)); $('f2').style.opacity=f2;
}}
render(0);
</script></body></html>'''

open(os.path.join(HERE, 'index.html'), 'w').write(html)
print('ok', CHAT_H)
