#!/usr/bin/env python3
"""Arma index.html del reel "Así se va a ver CROMA" (interfaz ilustrativa, datos de ejemplo)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'engine'))
import croma  # noqa: E402

I = dict(croma.ICONS)
I['casa'] = '<path d="M3.5 11 12 4l8.5 7"/><path d="M5.5 9.5V20h13V9.5"/><path d="M10 20v-5h4v5"/>'
I['campana'] = '<path d="M6 16.5V11a6 6 0 0 1 12 0v5.5l1.8 1.8H4.2z"/><path d="M10 20.5a2 2 0 0 0 4 0"/>'


def ic(name, size=28, color='currentColor', sw=1.8):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{I[name]}</svg>')


F = '../../engine/fonts/'
L = '../../engine/logos/'

nav = [('casa', 'Inicio'), ('engranaje', 'Equipos'), ('checklist', 'Órdenes'),
       ('calendario', 'Calendario'), ('grafico', 'Indicadores')]
nav_html = ''.join(
    f'<div class="nav" style="top:{120 + i*68}px">{ic(n, 30)}<span>{t}</span></div>' for i, (n, t) in enumerate(nav))

# ---------- Vista A: inicio ----------
kpis = [
    ('Disponibilidad', 'k1', '96,4', ' %', '<span class="up">+1,2 pts</span> vs. septiembre'),
    ('OT abiertas', 'k2', '12', '', '<i class="dot" style="background:#f0b240"></i>3 en proceso'),
    ('MTTR', 'k3', '2,1', ' h', '<span class="up">−0,4 h</span> vs. septiembre'),
    ('Preventivos al día', 'k4', '94', ' %', '<div class="bar"><b id="k4bar"></b></div>'),
]
kpi_html = ''
for i, (lab, kid, val, unit, foot) in enumerate(kpis):
    x = 270 + i * (285 + 22)
    kpi_html += (f'<div class="card kpi a-in" id="ka{i}" style="left:{x}px;top:236px;width:285px;height:172px">'
                 f'<div class="lab">{lab}</div><div class="val"><span id="{kid}">{val}</span><small>{unit}</small></div>'
                 f'<div class="foot">{foot}</div></div>')

pts = [38, 41, 33, 29, 31, 24, 19, 16]
cw, ch, ox, oy = 650, 270, 40, 120
xs = [ox + i * cw / (len(pts) - 1) for i in range(len(pts))]
ys = [oy + ch - (p / 45) * ch for p in pts]
line = ' '.join(f'{x:.1f},{y:.1f}' for x, y in zip(xs, ys))
area = f'M{xs[0]:.1f},{oy+ch} ' + ' '.join(f'L{x:.1f},{y:.1f}' for x, y in zip(xs, ys)) + f' L{xs[-1]:.1f},{oy+ch} Z'
grid = ''.join(f'<line x1="{ox}" x2="{ox+cw}" y1="{oy + ch*k/3:.1f}" y2="{oy + ch*k/3:.1f}" />' for k in range(4))
chart_html = f'''
<div class="card a-in" id="ka4" style="left:270px;top:430px;width:730px;height:532px">
  <div class="ct">Horas de detención no planificada</div><div class="cs">Últimas 8 semanas</div>
  <svg width="730" height="470" style="position:absolute;left:0;top:60px" viewBox="0 0 730 470">
    <defs><linearGradient id="ag" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#bda8e3" stop-opacity=".45"/><stop offset="1" stop-color="#bda8e3" stop-opacity="0"/></linearGradient></defs>
    <g stroke="rgba(255,255,255,.10)" stroke-width="1.5">{grid}</g>
    <path id="carea" d="{area}" fill="url(#ag)" opacity="0"/>
    <polyline id="cline" points="{line}" fill="none" stroke="#bda8e3" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>
    <circle id="cdot" cx="{xs[-1]:.1f}" cy="{ys[-1]:.1f}" r="11" fill="#fff" stroke="#7c4ddb" stroke-width="5" opacity="0"/>
    <text x="{ox}" y="{oy+ch+44}" class="axis">Hace 8 semanas</text>
    <text x="{ox+cw}" y="{oy+ch+44}" class="axis" text-anchor="end">Esta semana</text>
  </svg>
  <div class="tag" id="ctag" style="left:{xs[-1]-58:.0f}px;top:{ys[-1]-12:.0f}px">16 h</div>
</div>'''

prev = [('engranaje', 'COMP-01', 'Compresor de aire', 'Hoy', 'warn'),
        ('llama', 'CAL-01', 'Caldera', 'Mañana', 'info'),
        ('gota', 'BOM-03', 'Bomba de agua', 'Jue 30', 'info'),
        ('caja', 'LIN-02', 'Envasadora', 'Vie 31', 'info')]
rows = ''.join(
    f'<div class="row" id="pr{i}" style="top:{96 + i*104}px"><div class="ib">{ic(n, 30, "#bda8e3")}</div>'
    f'<div class="rt"><div class="code">{c}</div><div class="rn">{t}</div></div><div class="chip {k}">{d}</div></div>'
    for i, (n, c, t, d, k) in enumerate(prev))
list_html = (f'<div class="card a-in" id="ka5" style="left:1022px;top:430px;width:454px;height:532px">'
             f'<div class="ct">Próximos preventivos</div>{rows}</div>')

view_a = f'''<div class="view" id="vA">
<div class="h1">Resumen de hoy</div><div class="h2">Martes 28 de octubre · Planta 1</div>
{kpi_html}{chart_html}{list_html}</div>'''

# ---------- Vista B: equipos ----------
eq = [('engranaje', 'COMP-01', 'Compresor de aire', 'Sala de máquinas', 'En servicio', 'ok', 98),
      ('gota', 'BOM-03', 'Bomba de agua', 'Planta de tratamiento', 'En falla', 'bad', 71),
      ('llama', 'CAL-01', 'Caldera', 'Servicios', 'En servicio', 'ok', 95),
      ('caja', 'LIN-02', 'Envasadora', 'Línea 2', 'Preventivo hoy', 'warn', 92),
      ('generador', 'GEN-01', 'Generador', 'Exterior', 'En servicio', 'ok', 99),
      ('camion', 'MON-01', 'Montacargas', 'Depósito', 'Fuera de servicio', 'off', 64)]
cards = ''
for i, (n, c, t, a, s, k, d) in enumerate(eq):
    x = 270 + (i % 3) * (387 + 22)
    y = 300 + (i // 3) * (320 + 22)
    cards += (f'<div class="card eq b-in {"hot" if c=="BOM-03" else ""}" id="eb{i}" style="left:{x}px;top:{y}px;width:387px;height:320px">'
              f'<div class="ib big">{ic(n, 38, "#bda8e3")}</div><div class="pill {k}"><i></i>{s}</div>'
              f'<div class="code" style="position:absolute;left:28px;top:118px">{c}</div>'
              f'<div class="en">{t}</div><div class="ea">{a}</div>'
              f'<div class="disp"><span>Disponibilidad</span><b>{d} %</b></div><div class="bar eqbar"><b style="width:{d}%"></b></div></div>')
chips = [('Todos', '48', ''), ('En servicio', '44', 'ok'), ('En falla', '2', 'bad'), ('Fuera de servicio', '2', 'off')]
chip_html = '<div class="chips b-in" id="ebc">' + ''.join(
    f'<div class="fchip {"on" if i==0 else ""}">{"<i class=%s></i>" % k if k else ""}{t} <b>{v}</b></div>'
    for i, (t, v, k) in enumerate(chips)) + '</div>'
view_b = f'''<div class="view" id="vB">
<div class="h1">Equipos</div><div class="h2">48 equipos · Planta 1</div>
{chip_html}{cards}</div>'''

# ---------- Vista C: indicadores ----------
ck = [('MTBF', '312', ' h', '<span class="up">+8 %</span> vs. septiembre'),
      ('Cumplimiento del preventivo', '94', ' %', '<span class="up">+6 pts</span> vs. septiembre'),
      ('OT cerradas', '86', '', 'en octubre')]
ck_html = ''
for i, (lab, val, unit, foot) in enumerate(ck):
    x = 270 + i * (387 + 22)
    ck_html += (f'<div class="card kpi c-in" id="kc{i}" style="left:{x}px;top:236px;width:387px;height:150px">'
                f'<div class="lab">{lab}</div><div class="val" style="top:52px"><span id="kcv{i}">{val}</span><small>{unit}</small></div>'
                f'<div class="foot">{foot}</div></div>')
R = 150
circ = 2 * 3.14159265 * R
donut = f'''
<div class="card c-in" id="kc3" style="left:270px;top:408px;width:470px;height:554px">
 <div class="ct">Tipo de trabajo</div><div class="cs">Octubre</div>
 <svg width="380" height="380" viewBox="0 0 380 380" style="position:absolute;left:45px;top:110px">
  <circle cx="190" cy="190" r="{R}" fill="none" stroke="rgba(255,255,255,.08)" stroke-width="46"/>
  <circle id="dPrev" cx="190" cy="190" r="{R}" fill="none" stroke="#bda8e3" stroke-width="46" stroke-dasharray="0 {circ:.1f}" transform="rotate(-90 190 190)"/>
  <circle id="dCorr" cx="190" cy="190" r="{R}" fill="none" stroke="#7c4ddb" stroke-width="46" stroke-dasharray="0 {circ:.1f}" transform="rotate(-90 190 190)"/>
 </svg>
 <div class="dc"><b id="dpct">68 %</b><span>preventivo</span></div>
 <div class="leg" style="top:494px"><i style="background:#bda8e3"></i>Preventivo 68 %<i style="background:#7c4ddb;margin-left:26px"></i>Correctivo 32 %</div>
</div>'''
bars = [14, 18, 17, 21, 19, 23]
bw, gap, bx0, base, bh = 70, 36, 60, 430, 300
bar_html = ''
for i, v in enumerate(bars):
    x = bx0 + i * (bw + gap)
    h = v / 25 * bh
    col = '#7c4ddb' if i == len(bars) - 1 else 'rgba(189,168,227,.75)'
    bar_html += (f'<div class="vb" id="vb{i}" style="left:{x}px;top:{base-h:.0f}px;width:{bw}px;height:{h:.0f}px;background:{col}"></div>'
                 f'<div class="vbl" style="left:{x}px;top:{base+16}px;width:{bw}px">S{i+1}</div>')
bar_html += f'<div class="tag" id="vbt" style="left:{bx0 + 5*(bw+gap) - 6}px;top:{base - 23/25*bh - 64:.0f}px">23 OT</div>'
barcard = (f'<div class="card c-in" id="kc4" style="left:762px;top:408px;width:714px;height:554px">'
           f'<div class="ct">OT cerradas por semana</div><div class="cs">Últimas 6 semanas</div>'
           f'<div style="position:absolute;left:0;top:60px;width:714px;height:494px">{bar_html}</div></div>')
view_c = f'''<div class="view" id="vC">
<div class="h1">Indicadores</div><div class="h2">Octubre · Planta 1</div>
{ck_html}{donut}{barcard}</div>'''

html = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<style>
@font-face{{font-family:Sora;font-weight:400;src:url({F}sora-latin-400-normal.woff2)}}
@font-face{{font-family:Sora;font-weight:600;src:url({F}sora-latin-600-normal.woff2)}}
@font-face{{font-family:Sora;font-weight:700;src:url({F}sora-latin-700-normal.woff2)}}
@font-face{{font-family:Sora;font-weight:400;src:url({F}sora-latin-ext-400-normal.woff2);unicode-range:U+0100-024F,U+2212}}
@font-face{{font-family:Sora;font-weight:600;src:url({F}sora-latin-ext-600-normal.woff2);unicode-range:U+0100-024F,U+2212}}
@font-face{{font-family:Sora;font-weight:700;src:url({F}sora-latin-ext-700-normal.woff2);unicode-range:U+0100-024F,U+2212}}
@font-face{{font-family:JBM;font-weight:500;src:url({F}jetbrains-mono-latin-500-normal.woff2)}}
*{{box-sizing:border-box;margin:0}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#120f1e;font-family:Sora,sans-serif;color:#f7f3ff}}
.abs{{position:absolute}}
#bg{{position:absolute;inset:0;overflow:hidden}}
.blob{{position:absolute;border-radius:50%;filter:blur(90px)}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(189,168,227,.07) 2px,transparent 2px),linear-gradient(90deg,rgba(189,168,227,.07) 2px,transparent 2px);background-size:80px 80px}}
.ring{{position:absolute;border-radius:50%;border:64px solid #bda8e3}}
.hd{{position:absolute;left:0;right:0;text-align:center}}
.eti{{font:500 30px/40px JBM,monospace;letter-spacing:.18em;color:#bda8e3;text-transform:uppercase}}
.ttl{{font:700 92px/100px Sora;letter-spacing:-.025em}}
#screen{{position:absolute;left:24px;top:610px;width:1032px;height:688px;border-radius:30px;overflow:hidden;
  background:linear-gradient(140deg,rgba(255,255,255,.16),rgba(255,255,255,.05) 55%,rgba(255,255,255,.09));
  border:2px solid rgba(255,255,255,.24);box-shadow:0 50px 140px rgba(0,0,0,.55),inset 0 2px 0 rgba(255,255,255,.22);
  -webkit-backdrop-filter:blur(30px) saturate(160%);backdrop-filter:blur(30px) saturate(160%);transform-origin:50% 50%}}
#ui{{position:absolute;left:0;top:0;width:1500px;height:1000px;transform:scale(.688);transform-origin:0 0}}
.top{{position:absolute;left:0;top:0;width:1500px;height:96px;border-bottom:1.5px solid rgba(255,255,255,.12)}}
.side{{position:absolute;left:0;top:96px;width:250px;height:904px;border-right:1.5px solid rgba(255,255,255,.12)}}
.nav{{position:absolute;left:18px;width:214px;height:54px;display:flex;align-items:center;gap:14px;padding-left:18px;font:400 21px/1 Sora;color:#c4bbd9;z-index:2}}
.nav svg{{flex:none}}
#pill{{position:absolute;left:18px;width:214px;height:54px;border-radius:16px;background:rgba(189,168,227,.20);border:1.5px solid rgba(189,168,227,.35)}}
.srch{{position:absolute;left:420px;top:24px;width:560px;height:48px;border-radius:24px;background:rgba(255,255,255,.08);border:1.5px solid rgba(255,255,255,.12);display:flex;align-items:center;gap:12px;padding-left:20px;font:400 19px/1 Sora;color:#a99fc4}}
.view{{position:absolute;inset:0}}
.h1{{position:absolute;left:270px;top:124px;font:700 40px/48px Sora;color:#fff}}
.h2{{position:absolute;left:270px;top:178px;font:400 21px/28px Sora;color:#c4bbd9}}
.card{{position:absolute;border-radius:24px;background:linear-gradient(150deg,rgba(255,255,255,.11),rgba(255,255,255,.04));border:1.5px solid rgba(255,255,255,.14);box-shadow:inset 0 1px 0 rgba(255,255,255,.12)}}
.kpi .lab{{position:absolute;left:26px;top:24px;font:400 20px/24px Sora;color:#c4bbd9}}
.kpi .val{{position:absolute;left:26px;top:60px;font:700 56px/60px Sora;color:#fff;letter-spacing:-.02em}}
.kpi .val small{{font-size:28px;font-weight:600;color:#ece5fa;margin-left:2px}}
.kpi .foot{{position:absolute;left:26px;right:26px;bottom:22px;font:400 17px/22px Sora;color:#c4bbd9;display:flex;align-items:center;gap:8px}}
.up{{color:#4fc795;font-weight:600}}
.dot{{display:inline-block;width:12px;height:12px;border-radius:50%}}
.bar{{position:relative;width:100%;height:10px;border-radius:5px;background:rgba(255,255,255,.12);overflow:hidden}}
.bar b{{position:absolute;left:0;top:0;bottom:0;border-radius:5px;background:#bda8e3}}
.ct{{position:absolute;left:28px;top:24px;font:600 24px/30px Sora;color:#fff}}
.cs{{position:absolute;left:28px;top:58px;font:400 18px/24px Sora;color:#a99fc4}}
.axis{{font:400 17px Sora;fill:#a99fc4}}
.tag{{position:absolute;padding:8px 14px;border-radius:12px;background:#fff;color:#2a1458;font:700 20px/1 Sora;box-shadow:0 10px 30px rgba(0,0,0,.3)}}
.row{{position:absolute;left:20px;right:20px;height:88px;border-radius:18px;background:rgba(255,255,255,.05);display:flex;align-items:center;gap:16px;padding:0 16px}}
.ib{{width:54px;height:54px;border-radius:15px;background:rgba(189,168,227,.14);border:1.5px solid rgba(189,168,227,.25);display:grid;place-items:center;flex:none}}
.ib.big{{position:absolute;left:26px;top:26px;width:70px;height:70px;border-radius:19px}}
.rt{{flex:1;min-width:0}}
.code{{font:500 17px/22px JBM,monospace;letter-spacing:.06em;color:#bda8e3}}
.rn{{font:600 21px/28px Sora;color:#fff}}
.chip{{padding:9px 14px;border-radius:12px;font:600 17px/1 Sora;flex:none}}
.chip.warn{{background:#3a2a0c;color:#f7cf7f}}
.chip.info{{background:#1b2645;color:#a9c4f7}}
.eq .en{{position:absolute;left:28px;top:146px;font:600 28px/36px Sora;color:#fff}}
.eq .ea{{position:absolute;left:28px;top:186px;font:400 19px/24px Sora;color:#c4bbd9}}
.eq .disp{{position:absolute;left:28px;right:28px;top:236px;display:flex;justify-content:space-between;font:400 17px/22px Sora;color:#c4bbd9}}
.eq .disp b{{color:#fff;font-weight:600}}
.eqbar{{position:absolute;left:28px;right:28px;top:270px;width:auto}}
.pill{{position:absolute;right:22px;top:30px;display:flex;align-items:center;gap:9px;padding:9px 14px;border-radius:14px;font:600 17px/1 Sora}}
.pill i,.fchip i{{display:inline-block;width:11px;height:11px;border-radius:50%}}
.pill.ok{{background:#10301f;color:#8fe0bb}} .pill.ok i,.fchip i.ok{{background:#4fc795}}
.pill.bad{{background:#3d1717;color:#f7a8a8}} .pill.bad i,.fchip i.bad{{background:#f07070}}
.pill.warn{{background:#3a2a0c;color:#f7cf7f}} .pill.warn i{{background:#f0b240}}
.pill.off{{background:#2e2350;color:#c4bbd9}} .pill.off i,.fchip i.off{{background:#8f84ad}}
.chips{{position:absolute;left:270px;top:236px;display:flex;gap:12px}}
.fchip{{display:flex;align-items:center;gap:9px;padding:12px 18px;border-radius:15px;background:rgba(255,255,255,.06);border:1.5px solid rgba(255,255,255,.12);font:400 18px/1 Sora;color:#c4bbd9}}
.fchip b{{color:#fff;font-weight:600}}
.fchip.on{{background:rgba(189,168,227,.22);border-color:rgba(189,168,227,.4);color:#fff}}
.dc{{position:absolute;left:45px;top:110px;width:380px;height:380px;display:flex;flex-direction:column;align-items:center;justify-content:center}}
.dc b{{font:700 60px/64px Sora;color:#fff}} .dc span{{font:400 20px/26px Sora;color:#c4bbd9}}
.leg{{position:absolute;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:10px;font:400 18px/1 Sora;color:#ece5fa}}
.leg i{{display:inline-block;width:14px;height:14px;border-radius:4px}}
.vb{{position:absolute;border-radius:12px 12px 4px 4px;transform-origin:50% 100%}}
.vbl{{position:absolute;text-align:center;font:400 17px/1 Sora;color:#a99fc4}}
#cursor{{position:absolute;left:0;top:0;width:44px;height:44px;z-index:20;filter:drop-shadow(0 6px 10px rgba(0,0,0,.45))}}
#ripple{{position:absolute;width:90px;height:90px;margin:-45px 0 0 -45px;border-radius:50%;border:4px solid #fff;z-index:19;opacity:0}}
.cap{{position:absolute;left:60px;right:60px;top:1386px;text-align:center;font:700 62px/72px Sora;letter-spacing:-.02em;color:#fff}}
.cap em{{font-style:normal;color:#bda8e3}}
#note{{position:absolute;left:0;right:0;top:1320px;text-align:center;font:500 22px/30px JBM,monospace;letter-spacing:.06em;color:rgba(189,168,227,.75)}}
#end{{position:absolute;left:0;right:0;top:0;height:1920px}}
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

<div class="hd eti" id="h0" style="top:286px">Nueva interfaz</div>
<div class="hd ttl" id="h1" style="top:342px">Así se va a ver</div>
<div class="hd ttl" id="h2" style="top:444px;color:#bda8e3">CROMA.</div>

<div id="screen"><div id="ui">
  <div class="top">
    <img src="{L}croma-logo-blanco.png" style="position:absolute;left:36px;top:30px;height:36px">
    <div class="srch">{ic('lupa', 24, '#a99fc4')}Buscar equipo u orden de trabajo</div>
    <div class="fchip" style="position:absolute;left:1150px;top:24px;padding:13px 18px">{ic('edificio', 22, '#bda8e3')}Planta 1</div>
    <div style="position:absolute;left:1322px;top:30px">{ic('campana', 34, '#ece5fa')}<i style="position:absolute;right:2px;top:2px;width:12px;height:12px;border-radius:50%;background:#f07070"></i></div>
    <div style="position:absolute;left:1392px;top:22px;width:52px;height:52px;border-radius:50%;background:rgba(189,168,227,.25);border:1.5px solid rgba(189,168,227,.45);display:grid;place-items:center">{ic('persona', 28, '#fff')}</div>
  </div>
  <div class="side"></div>
  <div id="pill"></div>
  {nav_html}
  {view_a}{view_b}{view_c}
  <div id="ripple"></div>
  <svg id="cursor" viewBox="0 0 24 24"><path d="M4 2.5 L4 19.5 L8.6 15.4 L11.6 22 L14.6 20.6 L11.7 14.2 L18 14.2 Z" fill="#fff" stroke="#120f1e" stroke-width="1.4" stroke-linejoin="round"/></svg>
</div></div>

<div id="note">Interfaz ilustrativa · datos de ejemplo</div>
<div class="cap" id="capA">Simple para<br>el <em>técnico.</em></div>
<div class="cap" id="capB">Clara para el <em>jefe<br>de mantenimiento.</em></div>
<div class="cap" id="capC">Con los números<br>que <em>el dueño necesita.</em></div>

<div id="end">
  <img class="abs" id="elogo" src="{L}croma-logo-blanco.png" style="left:290px;top:760px;width:500px">
  <div class="endl ttl" id="e1" style="top:990px">Nueva interfaz.</div>
  <div class="endl ttl" id="e2" style="top:1096px;color:#bda8e3">Muy pronto.</div>
  <div class="endl eti" id="e3" style="top:1260px;letter-spacing:.08em;text-transform:none">@cromacmms</div>
</div>

<script>
const DURATION = 15.0;
const $ = id => document.getElementById(id);
const cl = (v,a=0,b=1) => Math.min(b, Math.max(a, v));
const P = (t,a,b) => cl((t-a)/(b-a));
const io = x => x<.5 ? 4*x*x*x : 1-Math.pow(-2*x+2,3)/2;
const oc = x => 1-Math.pow(1-x,3);
const ob = x => {{const c1=1.4,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2);}};
const L = (a,b,x) => a+(b-a)*x;
function rise(el, t, a, d=0.6, dy=40){{ const p=oc(P(t,a,a+d)); el.style.opacity=p; el.style.transform=`translateY(${{(1-p)*dy}}px)`; return p; }}
function vis(el, t, a, b, d=0.45, dy=36){{ // aparece en a, se va en b
  const pin=oc(P(t,a,a+d)), pout=io(P(t,b,b+d*.8)); el.style.opacity = pin*(1-pout);
  el.style.transform=`translateY(${{(1-pin)*dy - pout*dy*.6}}px)`; }}
function fmt(v, dec){{ return v.toFixed(dec).replace('.',','); }}

// cursor: [t, x, y] en coordenadas de la interfaz (1500x1000)
const CK = [[0,1640,760],[1.3,1640,760],[2.3,700,330],[3.1,760,330],[3.7,940,700],[4.15,124,188],[4.6,124,188],
            [5.6,600,560],[6.3,872,470],[7.5,880,474],[8.05,124,392],[8.5,124,392],[9.3,500,700],[10.1,520,690],[10.8,1230,560],[11.6,1260,560]];
function cur(t){{ for(let i=0;i<CK.length-1;i++){{ const [t0,x0,y0]=CK[i],[t1,x1,y1]=CK[i+1];
   if(t<=t1){{ const p=io(P(t,t0,t1)); return [L(x0,x1,p),L(y0,y1,p)]; }} }} const l=CK[CK.length-1]; return [l[1],l[2]]; }}
const CLICKS=[4.35,8.3];
const NAVY=[120,188,256,324,392];

function render(t){{
  // fondo
  $('b1').style.transform=`translate(${{-180+Math.sin(t*.35)*60}}px, ${{420+Math.cos(t*.3)*50}}px)`;
  $('b2').style.transform=`translate(${{380+Math.cos(t*.25)*70}}px, ${{1050+Math.sin(t*.28)*60}}px)`;
  $('b3').style.transform=`translate(${{560+Math.sin(t*.4+1)*80}}px, ${{620+Math.cos(t*.33)*60}}px)`;
  const rm=io(P(t,11.2,12.2)); $('ring').style.transform=`translate(${{L(720,800,rm)+Math.sin(t*.2)*14}}px, ${{L(480,40,rm)}}px) rotate(${{t*6}}deg)`;
  $('disc').style.transform=`translate(${{-90+Math.cos(t*.3)*12}}px, ${{L(1160,1420,rm)+Math.sin(t*.25)*14}}px)`;

  // encabezado
  const hout = io(P(t,11.2,11.8));
  [['h0',0.0],['h1',0.12],['h2',0.28]].forEach(([id,a])=>{{ const p=oc(P(t,a,a+.6)); const el=$(id);
    el.style.opacity=p*(1-hout); el.style.transform=`translateY(${{(1-p)*44 - hout*60}}px)`; }});

  // pantalla: entrada, cámara y salida
  const pin = oc(P(t,0.25,1.25)), pout = io(P(t,11.1,11.9));
  let sc = L(.9,1,pin) * L(1,.82,pout), ty = (1-pin)*160 - pout*120;
  // empuje suave + zoom a la tarjeta en falla
  const z = io(P(t,6.2,6.9)) * (1-io(P(t,7.6,8.2)));
  sc *= 1 + .03*P(t,1.2,4.3) + .08*z;
  const tx = -70*z; ty -= 10*z;
  const s=$('screen'); s.style.opacity = pin*(1-pout); s.style.transform=`translate(${{tx}}px, ${{ty}}px) scale(${{sc}})`;
  $('note').style.opacity = oc(P(t,1.2,1.8))*(1-io(P(t,11.0,11.5)))*(1-z);

  // menú lateral
  let py = NAVY[0];
  py = L(py, NAVY[1], io(P(t,4.35,4.65))); py = L(py, NAVY[4], io(P(t,8.3,8.6)));
  $('pill').style.top = py+'px';
  document.querySelectorAll('.nav').forEach((n,i)=>{{ const on = Math.abs(NAVY[i]-py)<20; n.style.color = on?'#fff':'#c4bbd9'; n.style.fontWeight = on?600:400; }});

  // vistas
  const vA = 1-io(P(t,4.4,4.7)), vB = io(P(t,4.45,4.75))*(1-io(P(t,8.35,8.65))), vC = io(P(t,8.4,8.7));
  $('vA').style.opacity=vA; $('vB').style.opacity=vB; $('vC').style.opacity=vC;
  $('vA').style.transform=`translateY(${{(1-vA)*-14}}px)`; $('vB').style.transform=`translateY(${{(1-io(P(t,4.45,4.75)))*20}}px)`; $('vC').style.transform=`translateY(${{(1-vC)*20}}px)`;

  // A: tarjetas, números, gráfico, lista
  for(let i=0;i<6;i++){{ const el=$('ka'+i); const p=oc(P(t,0.75+i*.12,1.35+i*.12)); el.style.opacity=p; el.style.transform=`translateY(${{(1-p)*30}}px)`; }}
  const k=oc(P(t,1.0,2.4));
  $('k1').textContent=fmt(L(80,96.4,k),1); $('k2').textContent=Math.round(L(0,12,k)); $('k3').textContent=fmt(L(4.5,2.1,k),1); $('k4').textContent=Math.round(L(0,94,k));
  $('k4bar').style.width = (94*k)+'%';
  const hov = io(P(t,2.2,2.5))*(1-io(P(t,3.0,3.3)));
  $('ka1').style.transform=`translateY(${{-8*hov}}px)`; $('ka1').style.borderColor=`rgba(189,168,227,${{.14+.5*hov}})`;
  const lp = io(P(t,1.5,3.2)); $('cline').style.strokeDashoffset = 1-lp; $('carea').style.opacity = oc(P(t,2.4,3.3));
  const dp = ob(P(t,3.1,3.5)); $('cdot').setAttribute('opacity', P(t,3.1,3.2)); $('cdot').setAttribute('r', 11*dp);
  const tg=$('ctag'); const tp=oc(P(t,3.25,3.6)); tg.style.opacity=tp; tg.style.transform=`translate(0, ${{-50 - (1-tp)*14}}px)`;
  for(let i=0;i<4;i++){{ const el=$('pr'+i); const p=oc(P(t,1.6+i*.14,2.1+i*.14)); el.style.opacity=p; el.style.transform=`translateX(${{(1-p)*36}}px)`; }}

  // B: equipos
  const bc=oc(P(t,4.6,5.1)); $('ebc').style.opacity=bc; $('ebc').style.transform=`translateY(${{(1-bc)*20}}px)`;
  for(let i=0;i<6;i++){{ const el=$('eb'+i); const p=oc(P(t,4.65+i*.09,5.25+i*.09)); el.style.opacity=p; el.style.transform=`translateY(${{(1-p)*34}}px) scale(${{L(.96,1,p)}})`; }}
  const hb = io(P(t,6.2,6.5))*(1-io(P(t,7.8,8.1)));
  const hot=$('eb1'); hot.style.transform=`translateY(${{-10*hb}}px) scale(${{1+.03*hb}})`;
  hot.style.borderColor=`rgba(240,112,112,${{.14+.7*hb}})`; hot.style.boxShadow=`0 0 ${{60*hb}}px rgba(240,112,112,${{.35*hb}}), inset 0 1px 0 rgba(255,255,255,.12)`;

  // C: indicadores
  for(let i=0;i<5;i++){{ const el=$('kc'+i); const p=oc(P(t,8.6+i*.1,9.2+i*.1)); el.style.opacity=p; el.style.transform=`translateY(${{(1-p)*30}}px)`; }}
  const kc=oc(P(t,8.8,10.0)); $('kcv0').textContent=Math.round(L(200,312,kc)); $('kcv1').textContent=Math.round(L(60,94,kc)); $('kcv2').textContent=Math.round(L(0,86,kc));
  const C={circ:.1f}; const d1=io(P(t,9.0,10.1));
  const prev=.68*C*d1, corr=.32*C*io(P(t,9.6,10.6));
  $('dPrev').setAttribute('stroke-dasharray', `${{prev}} ${{C}}`);
  $('dCorr').setAttribute('stroke-dasharray', `${{corr}} ${{C}}`); $('dCorr').setAttribute('stroke-dashoffset', `${{-.68*C}}`);
  $('dpct').textContent = Math.round(68*d1)+' %';
  for(let i=0;i<6;i++){{ const p=ob(P(t,9.2+i*.1,9.75+i*.1)); $('vb'+i).style.transform=`scaleY(${{Math.max(0,p)}})`; }}
  const vt=oc(P(t,10.0,10.4)); $('vbt').style.opacity=vt; $('vbt').style.transform=`translateY(${{(1-vt)*12}}px)`;

  // cursor y clic
  const [cx,cy]=cur(t); const cu=$('cursor');
  const pr=CLICKS.reduce((m,c)=>Math.max(m, cl(1-Math.abs(t-c)/.12)),0); cu.style.transform=`translate(${{cx}}px, ${{cy}}px) scale(${{1-.15*pr}})`;
  cu.style.opacity = 1-io(P(t,11.0,11.4));
  let rp=0, rx=0, ry=0; CLICKS.forEach(c=>{{ const p=P(t,c,c+.5); if(t>=c && t<=c+.5){{ rp=p; [rx,ry]=cur(c); }} }});
  const rpl=$('ripple'); rpl.style.left=(rx+8)+'px'; rpl.style.top=(ry+8)+'px'; rpl.style.opacity = rp>0 ? (1-rp)*.9 : 0; rpl.style.transform=`scale(${{.3+rp*1.1}})`;

  // textos de abajo
  vis($('capA'), t, 1.15, 4.3); vis($('capB'), t, 4.75, 8.15); vis($('capC'), t, 8.75, 11.0);

  // cierre
  const lg=oc(P(t,11.8,12.5)); const el=$('elogo'); el.style.opacity=lg; el.style.transform=`translateY(${{(1-lg)*30}}px) scale(${{L(.92,1,lg)}})`;
  rise($('e1'), t, 12.25); rise($('e2'), t, 12.5); rise($('e3'), t, 12.9, .5, 20);
}}
render(0);
</script></body></html>'''

open(os.path.join(HERE, 'index.html'), 'w').write(html)
print('ok')
