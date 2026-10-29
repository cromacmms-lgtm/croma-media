#!/usr/bin/env python3
"""Motor de reels de CROMA.

Cada reel se describe en reels/plan.py como una lista de escenas (gancho, adivinanza, mito, checklist,
filas, línea de tiempo, fórmula, matriz, equipo, teléfono, cierre). El motor arma reels/<slug>/index.html
con una función render(t) declarativa (cada elemento tiene su momento de entrada y salida) y la música
original con los cortes de cada escena.

Uso: python3 reels/motor.py <slug> [<slug> ...]
"""
import os, sys, re, json, html as H
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'engine'))
sys.path.insert(0, HERE)
import croma  # noqa: E402

I = dict(croma.ICONS)
I['campana'] = '<path d="M6 16.5V11a6 6 0 0 1 12 0v5.5l1.8 1.8H4.2z"/><path d="M10 20.5a2 2 0 0 0 4 0"/>'
I['casa'] = '<path d="M3.5 11 12 4l8.5 7"/><path d="M5.5 9.5V20h13V9.5"/><path d="M10 20v-5h4v5"/>'
I['camara'] = '<path d="M4 8h3l1.6-2.5h6.8L17 8h3v11H4z"/><circle cx="12" cy="13.2" r="3.6"/>'
I['play'] = '<path d="M8 5.5v13l10-6.5z"/>'
I['motor'] = '<rect x="3" y="7" width="13" height="10" rx="2"/><path d="M16 12h5M6 7V5h5v2M6 10v4M9 10v4M12 10v4"/>'
I['bomba'] = '<circle cx="14" cy="13" r="6"/><path d="M14 7V3h4M20 13h2M3 12h5M3 15h5"/><circle cx="14" cy="13" r="2"/>'
I['compresor'] = '<rect x="3" y="9" width="12" height="9" rx="2"/><path d="M15 12h3a3 3 0 0 1 3 3v3M7 9V6h4v3M6 18v2M12 18v2"/>'
I['reductor'] = '<rect x="6" y="5" width="12" height="14" rx="2"/><path d="M2 9h4M18 15h4M10 9h4M10 13h4"/>'
I['cosechadora'] = '<path d="M3 15h10l2-5h4l2 5v2H3z"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/><path d="M3 15V9h5v6"/>'

F = '../../engine/fonts/'
LG = '../../engine/logos/'
LV = '#bda8e3'


def ic(name, size=28, color='currentColor', sw=1.8):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{I[name]}</svg>')


def md(s):
    """**texto** -> acento lavanda; \n -> salto de línea."""
    s = H.escape(s, quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<em>\1</em>', s)
    return s.replace('\n', '<br>')


def A(a, b=None, fx='rise', extra=''):
    """Atributos de animación declarativa."""
    bb = '' if b is None else f' data-b="{b:.3f}"'
    return f'data-a="{a:.3f}"{bb} data-fx="{fx}" {extra}'


# ---------------------------------------------------------------- plantillas de escena
# Cada plantilla recibe (s, t0, t1) y devuelve el HTML del contenido de la tarjeta.
# s: dict de la escena, t0/t1: inicio y fin absolutos de la escena.

def sc_texto(s, t0, t1):
    icon = s.get('icon')
    h = f'<div class="col center" style="gap:34px;padding:0 60px">'
    if icon:
        h += f'<div class="bigic" {A(t0+.15, t1-.25, "pop")}>{ic(icon, 120, LV, 1.5)}</div>'
    for i, ln in enumerate(s['lines']):
        h += f'<div class="tx1" {A(t0+.3+i*.45, t1-.25)}>{md(ln)}</div>'
    if s.get('sub'):
        h += f'<div class="tx2" {A(t0+.5+len(s["lines"])*.45, t1-.25)}>{md(s["sub"])}</div>'
    return h + '</div>'


def sc_adivinanza(s, t0, t1):
    """Pregunta con equipo y síntomas, opciones, cuenta y respuesta."""
    d = t1 - t0
    tq, to, tr = t0 + .2, t0 + d * .38, t0 + d * .62     # síntomas, opciones, respuesta
    eq = s['equipo']
    h = (f'<div class="quiz"><div class="qeq" {A(tq, t1-.25)}><div class="ib">{ic(eq["icon"], 46, LV, 1.7)}</div>'
         f'<div><div class="code">{H.escape(eq["code"])}</div><div class="qn">{H.escape(eq["name"])}</div></div></div>')
    h += '<div class="qs">'
    for i, x in enumerate(s['sintomas']):
        h += f'<div class="qsi" {A(tq+.4+i*.5, t1-.25, "left")}>{ic(x[0], 34, "#f7cf7f", 2)}<span>{md(x[1])}</span></div>'
    h += '</div><div class="qq" ' + A(to-.3, t1-.25) + '>¿Qué falla es?</div><div class="qo">'
    for i, o in enumerate(s['opciones']):
        ok = i == s['correcta']
        h += (f'<div class="opt" {A(to+i*.25, t1-.25, "left")} data-ans="{tr:.3f}" data-ok="{1 if ok else 0}">'
              f'<b>{"ABC"[i]}</b><span>{md(o)}</span><i class="mark">{ic("check" if ok else "x", 34, "#fff", 2.6)}</i></div>')
    h += '</div>'
    h += f'<div class="qx" {A(tr+.5, t1-.25)}>{md(s["explica"])}</div></div>'
    return h


def sc_mito(s, t0, t1):
    real = s.get('veredicto', 'mito') == 'realidad'
    h = (f'<div class="col" style="padding:60px 54px;gap:30px">'
         f'<div class="mq" {A(t0+.15, t1-.25)}>“{md(s["frase"])}”</div>'
         f'<div class="stamp {"ok" if real else "bad"}" {A(t0+1.2, t1-.25, "stamp")}>{"REALIDAD" if real else "MITO"}</div>')
    stp = (t1 - t0 - 2.4) / max(1, len(s['puntos']))
    for i, p in enumerate(s['puntos']):
        h += f'<div class="mp" {A(t0+2.0+i*stp, t1-.25, "left")}>{ic(p[0], 40, LV, 1.9)}<span>{md(p[1])}</span></div>'
    return h + '</div>'


def sc_checklist(s, t0, t1):
    n = len(s['items'])
    step = (t1 - t0 - .8) / n
    h = f'<div class="col" style="padding:50px 44px;gap:22px">'
    if s.get('encabezado'):
        h += f'<div class="ct1" {A(t0+.1, t1-.25)}>{md(s["encabezado"])}</div>'
    for i, it in enumerate(s['items']):
        a = t0 + .4 + i * step
        h += (f'<div class="ck" {A(a, t1-.25, "left")}><div class="ckn">{i+1:02d}</div><div class="ib">{ic(it[0], 40, LV, 1.8)}</div>'
              f'<div><div class="ckt">{md(it[1])}</div><div class="cks">{md(it[2])}</div></div>'
              f'<div class="ckm" {A(a+.6, t1-.25, "pop")}>{ic("check", 30, "#8fe0bb", 2.6)}</div></div>')
    return h + '</div>'


def sc_filas(s, t0, t1):
    """Filas comparativas (por ejemplo correctivo / preventivo / predictivo)."""
    n = len(s['filas'])
    step = (t1 - t0 - .6) / n
    h = f'<div class="col" style="padding:46px 40px;gap:24px">'
    if s.get('encabezado'):
        h += f'<div class="ct1" {A(t0+.1, t1-.25)}>{md(s["encabezado"])}</div>'
    for i, f in enumerate(s['filas']):
        a = t0 + .35 + i * step
        hot = ' hot' if f.get('destacar') else ''
        h += (f'<div class="fl{hot}" {A(a, t1-.25, "left")} {"data-hot=%.3f" % (t1-1.2) if f.get("destacar") else ""}>'
              f'<div class="flh"><span class="tag {f.get("color","")}">{md(f["nombre"])}</span><span class="flc">{md(f.get("cuando",""))}</span></div>'
              f'<div class="flb">{md(f["texto"])}</div></div>')
    return h + '</div>'


def sc_linea(s, t0, t1):
    n = len(s['etapas'])
    step = (t1 - t0 - .6) / n
    h = f'<div class="tl"><div class="tlbar" {A(t0+.1, t1-.25, "grow")} data-d="{t1-t0-.8:.3f}"></div>'
    for i, e in enumerate(s['etapas']):
        a = t0 + .3 + i * step
        h += (f'<div class="tle" {A(a, t1-.25, "left")}><div class="tld">{ic(e[0], 34, "#2a1458", 2)}</div>'
              f'<div><div class="tlm">{md(e[1])}</div><div class="tlt">{md(e[2])}</div></div></div>')
    return h + '</div>'


def sc_formula(s, t0, t1):
    d = t1 - t0
    h = (f'<div class="col center" style="gap:26px;padding:40px">'
         f'<div class="fx" {A(t0+.1, t1-.25)}><div class="fxn">{md(s["nombre"])}</div><div class="fxe">=</div>'
         f'<div class="fxf"><div class="fxu">{md(s["num"])}</div><div class="fxl"></div><div class="fxd">{md(s["den"])}</div></div></div>'
         f'<div class="tx2" {A(t0+.9, t1-.25)}>{md(s["lee"])}</div>')
    if s.get('ejemplo'):
        e = s['ejemplo']
        h += (f'<div class="fe" {A(t0+d*.45, t1-.25)}><div class="fet">{md(e["texto"])}</div>'
              f'<div class="fer"><span>{md(e["calc"])}</span><b><i class="count" data-a="{t0+d*.45+.4:.3f}" data-d="1.0" data-from="0" '
              f'data-to="{e["valor"]}" data-dec="{e.get("dec",0)}">{e["valor"]}</i> {md(e["unidad"])}</b></div></div>')
    return h + '</div>'


def sc_matriz(s, t0, t1):
    """Matriz de criticidad 3x3 con equipos ubicados."""
    cols = ['#1d4a3a', '#3a3a1a', '#4a2418']
    cells = ''
    for r in range(3):
        for c in range(3):
            lvl = r + c        # 0..4
            color = ['rgba(79,199,149,.28)', 'rgba(127,196,207,.22)', 'rgba(240,178,64,.25)', 'rgba(240,140,90,.30)', 'rgba(240,112,112,.38)'][lvl]
            cells += f'<div class="mc" style="left:{c*230}px;top:{(2-r)*170}px;background:{color}"></div>'
    h = (f'<div class="mx" {A(t0+.1, t1-.25, "fade")}><div class="mxg">{cells}'
         f'<div class="mxy">Consecuencia de la falla →</div><div class="mxx">Frecuencia de falla →</div>')
    for i, e in enumerate(s['equipos']):
        x, y = e['f'] * 230 + 115, (2 - e['c']) * 170 + 85
        h += (f'<div class="mdot" {A(t0+.9+i*.55, t1-.25, "pop")} style="left:{x-34}px;top:{y-34}px">{ic(e["icon"], 36, "#fff", 2)}</div>'
              f'<div class="mlab" {A(t0+1.0+i*.55, t1-.25)} style="left:{x-120}px;top:{y+38}px">{md(e["nombre"])}</div>')
    h += '</div>'
    if s.get('nota'):
        h += f'<div class="mxn" {A(t0+1.2+len(s["equipos"])*.55, t1-.25)}>{md(s["nota"])}</div>'
    return h + '</div>'


def sc_telefono(s, t0, t1):
    """Pantallas de la app (ilustrativas) dentro de un teléfono de vidrio."""
    scr = s['pantallas']
    step = (t1 - t0) / len(scr)
    h = f'<div class="ph glass2" {A(t0, t1-.25, "rise")}><div class="phn"></div>'
    for i, p in enumerate(scr):
        a, b = t0 + i * step, t0 + (i + 1) * step
        h += f'<div class="scr" {A(a+.05, b-.15 if i < len(scr)-1 else t1-.25, "right")}>'
        h += f'<div class="scrh"><div class="code">{H.escape(p.get("eti",""))}</div><div class="scrt">{md(p["titulo"])}</div></div>'
        for j, r in enumerate(p['filas']):
            ra = a + .35 + j * .35
            k = r.get('tipo', 'fila')
            if k == 'qr':
                h += f'<div class="sqr" {A(ra, None, "pop")}>{qr_svg(15, 15)}<div class="sqrs" data-scan="{ra+.2:.3f}"></div></div>'
            elif k == 'foto':
                h += f'<div class="sph" {A(ra, None, "pop")}>{ic(r.get("icon","gota"), 90, LV, 1.4)}<div class="flash" data-flash="{ra+.4:.3f}"></div></div>'
            elif k == 'aviso':
                h += (f'<div class="sav" {A(ra, None, "left")}><div class="ib" style="background:{r.get("c","#f0b240")}26">{ic(r.get("icon","campana"), 34, r.get("c","#f0b240"), 2)}</div>'
                      f'<div><div class="code" style="font-size:18px">{H.escape(r.get("de","CROMA · ahora"))}</div><div class="savt">{md(r["texto"])}</div></div></div>')
            else:
                chip = f'<span class="chip {r.get("chipc","")}">{md(r["chip"])}</span>' if r.get('chip') else ''
                h += (f'<div class="srow" {A(ra, None, "left")}><div class="ib">{ic(r.get("icon","engranaje"), 30, LV, 1.8)}</div>'
                      f'<div class="srt"><div class="srn">{md(r["titulo"])}</div>{"<div class=srs>"+md(r["sub"])+"</div>" if r.get("sub") else ""}</div>{chip}</div>')
        h += '</div>'
    return h + '</div>'


def qr_svg(n=15, cell=14):
    import random
    rnd = random.Random(5)
    q = []
    def fnd(x0, y0):
        for y in range(5):
            for x in range(5):
                if x in (0, 4) or y in (0, 4) or (x == 2 and y == 2):
                    q.append((x0 + x, y0 + y))
    for fx, fy in [(0, 0), (n - 5, 0), (0, n - 5)]:
        fnd(fx, fy)
    for y in range(n):
        for x in range(n):
            inf = (x < 6 and y < 6) or (x >= n - 6 and y < 6) or (x < 6 and y >= n - 6)
            if not inf and rnd.random() < .5:
                q.append((x, y))
    return (f'<svg width="{n*cell}" height="{n*cell}" viewBox="0 0 {n*cell} {n*cell}" fill="#120f1e">'
            + ''.join(f'<rect x="{x*cell}" y="{y*cell}" width="{cell}" height="{cell}"/>' for x, y in q) + '</svg>')


def sc_equipo(s, t0, t1):
    """Ilustración de un equipo (reels/equipos.py) con pasos que resaltan componentes y un panel de falla."""
    import equipos
    svg = getattr(equipos, s['svg'])()
    steps = s['pasos']
    n = len(steps)
    step = (t1 - t0 - .3) / n
    h = f'<div class="eqw" {A(t0, t1-.25, "fade")} data-vib=\'{json.dumps([[t0+i*step+.3, t0+(i+1)*step-.2] for i,p in enumerate(steps) if p.get("vibra")])}\'>{svg}</div>'
    for i, p in enumerate(steps):
        a, b = t0 + .2 + i * step, t0 + .2 + (i + 1) * step
        last = i == n - 1
        for hid in p.get('resaltar', []):
            h += f'<i class="hlref" data-id="{hid}" data-a="{a+.2:.3f}" data-b="{b-.25:.3f}"></i>'
        h += f'<div class="pan" {A(a, (t1-.25) if last else b-.25)}>'
        if p.get('panel'):
            pp = p['panel']
            h += f'<div class="pnh"><b>{i+1:02d}</b>{md(pp["comp"])}</div>'
            for lab, txt in [('Falla', pp.get('falla')), ('Síntoma', pp.get('sintoma')), ('Se detecta con', pp.get('detecta'))]:
                if txt:
                    h += f'<div class="pr"><span>{lab}</span><p>{md(txt)}</p></div>'
        elif p.get('texto'):
            h += f'<div class="pnt">{md(p["texto"])}</div>'
        h += '</div>'
    return h


def sc_frecuencias(s, t0, t1):
    n = len(s['filas'])
    h = f'<div class="col" style="padding:50px 44px;gap:20px">'
    if s.get('encabezado'):
        h += f'<div class="ct1" {A(t0+.1, t1-.25)}>{md(s["encabezado"])}</div>'
    for i, (icn, name, fq) in enumerate(s['filas']):
        h += (f'<div class="ck" {A(t0+.5+i*.45, t1-.25, "left")}><div class="ib">{ic(icn, 40, LV, 1.8)}</div>'
              f'<div class="ckt" style="flex:1">{md(name)}</div><span class="chip info" style="font-size:22px;padding:11px 16px">{md(fq)}</span></div>')
    if s.get('pie'):
        h += f'<div class="tx2" style="margin-top:14px;text-align:center" {A(t0+.8+n*.45, t1-.25)}>{md(s["pie"])}</div>'
    return h + '</div>'


SCENES = dict(frecuencias=sc_frecuencias, texto=sc_texto, adivinanza=sc_adivinanza, mito=sc_mito, checklist=sc_checklist, filas=sc_filas,
              linea=sc_linea, formula=sc_formula, matriz=sc_matriz, telefono=sc_telefono, equipo=sc_equipo)

CSS = open(os.path.join(HERE, 'motor.css')).read()
JS = open(os.path.join(HERE, 'motor.js')).read()


def build(r):
    slug = r['slug']
    out = os.path.join(HERE, slug)
    os.makedirs(out, exist_ok=True)
    # tiempos
    t = 0.0
    tl = []
    for s in r['escenas']:
        tl.append((t, t + s['dur']))
        t += s['dur']
    END = t
    DUR = END + r.get('cierre_dur', 2.6)
    # encabezados: uno por cambio de texto
    heads, cur = [], None
    for (a, b), s in zip(tl, r['escenas']):
        key = (s.get('eti', r.get('eti', '')), tuple(s.get('titulo', r.get('titulo', ['', '']))), s.get('px', r.get('titulo_px')))
        if cur and cur['key'] == key:
            cur['b'] = b
        else:
            cur = dict(key=key, a=a, b=b)
            heads.append(cur)
    hh = ''
    for i, hd in enumerate(heads):
        eti, (l1, l2), px = hd['key']
        b = hd['b'] - .2 if i < len(heads) - 1 else END - .1
        small = ' style="font-size:%dpx;line-height:%dpx"' % (px, int(px * 1.12)) if px else ''
        hh += (f'<div class="eti" {A(max(0, hd["a"]), b, "rise", "data-in=.35")}>{H.escape(eti)}</div>'
               f'<div class="ttl l1"{small} {A(max(0, hd["a"]), b, "rise", "data-in=.35")}>{md(l1)}</div>'
               f'<div class="ttl l2"{small} {A(max(0, hd["a"])+.1, b, "rise", "data-in=.35")}>{md(l2)}</div>')
    # escenas
    body = ''
    for (a, b), s in zip(tl, r['escenas']):
        body += f'<div class="scene">{SCENES[s["tipo"]](s, a, b)}</div>'
    note = r.get('nota')
    note_html = f'<div id="note" {A(.6, END-.3, "fade")}>{H.escape(note)}</div>' if note else ''
    cl = r['cierre']
    end = (f'<div class="endl ttl" id="endt" {A(END+.05, None)} style="top:640px">{md(cl["texto"])}</div>'
           f'<img class="abs" id="endlogo" {A(END+.6, None)} src="{LG}croma-logo-blanco.png" style="left:330px;top:1040px;width:420px">'
           f'<div class="endl handle" id="endh" {A(END+.9, None, "fade")} style="top:1190px">@cromacmms</div>')
    page = (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{CSS.replace("@F@", F)}</style></head><body>'
            '<div id="bg"><div class="blob" id="b1"></div><div class="blob" id="b2"></div><div class="blob" id="b3"></div>'
            '<div class="grid"></div><div class="ring" id="ring"></div><div class="abs" id="disc"></div></div>'
            f'{hh}<div id="card" class="glass" {A(.1, END-.15, "card")}>{body}</div>{note_html}{end}'
            f'<script>const DURATION={DUR:.2f}, END={END:.2f};\n{JS}</script></body></html>')
    open(os.path.join(out, 'index.html'), 'w').write(page)
    # música: cortes en cada escena
    cues = [a for a, _ in tl]
    json.dump(dict(dur=DUR, end=END, cues=cues, seed=r.get('seed', 7), key=r.get('tono', 0), bpm=r.get('bpm', 120)),
              open(os.path.join(out, 'musica.json'), 'w'))
    return out, DUR


if __name__ == '__main__':
    import plan
    want = sys.argv[1:]
    for r in plan.REELS:
        if not want or r['slug'] in want:
            o, d = build(r)
            print('ok', r['slug'], f'{d:.1f}s')
