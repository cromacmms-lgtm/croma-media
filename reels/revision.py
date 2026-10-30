#!/usr/bin/env python3
"""Arma la página de revisión del calendario (reels + historias) en una carpeta lista para publicar.
Uso: python3 reels/revision.py <carpeta_previews> <carpeta_salida>"""
import os, sys, json, glob, html as H, re, shutil, subprocess
from datetime import datetime
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import plan
from PIL import Image

PREV, OUT = sys.argv[1], sys.argv[2]
os.makedirs(os.path.join(OUT, 'v'), exist_ok=True)
os.makedirs(os.path.join(OUT, 'h'), exist_ok=True)
DIAS = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
MESES = ['', 'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
FORMATO = {'adivinanza': 'Adivinanza', 'checklist': 'Checklist', 'linea': 'Línea de tiempo', 'equipo': 'Equipo animado',
           'mito': 'Mito o realidad', 'filas': 'Comparativo', 'telefono': 'Interfaz CROMA', 'formula': 'Fórmula animada',
           'matriz': 'Matriz', 'texto': 'Texto'}

extra = [
    dict(slug='2026-10-30-reel-bomba3', fecha='2026-10-30T10:05:00', titulo_reel='Cuando el jefe pregunta qué pasó con la bomba 3',
         formato='Humor de planta', estado='Programado',
         caption=json.load(open(os.path.join(ROOT, 'content/2026-10-30-reel-bomba3.json')))['caption'], tema='bomba3'),
    dict(slug='2026-11-04-reel-bomba-centrifuga', fecha='2026-11-03T10:05:00', titulo_reel='Bomba centrífuga: por dónde puede fallar',
         formato='Equipo animado', estado='Programado · pasó del miércoles 4 al martes 3',
         caption=json.load(open(os.path.join(ROOT, 'content/2026-11-04-reel-bomba-centrifuga.json')))['caption'], tema='bomba-centrifuga'),
]
items = []
for e in extra:
    items.append(dict(e, src=os.path.join(ROOT, 'media', e['slug'], 'reel.mp4')))
for r in plan.REELS:
    tipos = [s['tipo'] for s in r['escenas'] if s['tipo'] != 'texto']
    tema = r['slug'][11:]
    items.append(dict(slug=r['slug'], fecha=r['fecha'], titulo_reel=r['titulo_reel'], formato=FORMATO.get(tipos[0], 'Reel') if tipos else 'Reel',
                      estado='Programado', caption=r['caption'], tema=tema, src=os.path.join(PREV, r['slug'] + '-preview.mp4')))
items.sort(key=lambda x: x['fecha'])

# historias por día
hist = {}
for f in sorted(glob.glob(os.path.join(ROOT, 'content', '*-historia-*-*.json'))):
    sp = json.load(open(f))
    if not re.search(r'-(anuncio|tip|pregunta)$', sp['slug']):
        continue
    d = sp['date'][:10]
    hist.setdefault(d, []).append(sp)


def small_video(src, dst):
    if src.endswith('-preview.mp4') and os.path.exists(src):
        shutil.copy(src, dst)
    else:
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-vf', 'scale=540:960', '-c:v', 'libx264', '-crf', '30',
                        '-preset', 'veryfast', '-c:a', 'aac', '-b:a', '96k', '-movflags', '+faststart', dst], check=True)


def fecha_txt(iso):
    d = datetime.fromisoformat(iso)
    return d, f'{DIAS[d.weekday()].capitalize()} {d.day} de {MESES[d.month]}'


def esc(s):
    return H.escape(s).replace('\n', '<br>')


cards = ''
for it in items:
    d, ftxt = fecha_txt(it['fecha'])
    vname = f'v/{it["slug"]}.mp4'
    small_video(it['src'], os.path.join(OUT, vname))
    poster = f'v/{it["slug"]}.jpg'
    Image.open(os.path.join(ROOT, 'media', it['slug'], 'portada.jpg')).convert('RGB').resize((360, 640)).save(os.path.join(OUT, poster), quality=78)
    hs = ''
    for sp in sorted(hist.get(it['fecha'][:10], []), key=lambda x: x['date']):
        img = f'h/{sp["slug"]}.jpg'
        Image.open(os.path.join(ROOT, 'media', sp['slug'], '01.jpg')).convert('RGB').resize((360, 640)).save(os.path.join(OUT, img), quality=80)
        kind = 'Anuncio del reel' if sp['slug'].endswith('anuncio') else ('Pregunta' if sp['slug'].endswith('pregunta') else 'Tip')
        hs += (f'<figure class="story"><img src="{img}" alt="Historia: {H.escape(re.sub(r"[*]", "", sp["story"]["title"]))}" loading="lazy" width="360" height="640">'
               f'<figcaption><span class="t">{sp["date"][11:16]}</span> {kind}</figcaption></figure>')
    est = it['estado']
    estc = 'new' if est == 'Nuevo' else 'set'
    cards += f'''
<article class="entry" id="{it['tema']}">
  <div class="when"><span class="dow">{ftxt.split(' ')[0]}</span><span class="day">{d.day}</span><span class="mon">{MESES[d.month][:3]}</span></div>
  <div class="reel"><video src="{vname}" poster="{poster}" controls playsinline preload="none" width="270" height="480"></video></div>
  <div class="info">
    <div class="meta"><span class="time">{ftxt} · 10:05</span><span class="chip fmt">{H.escape(it['formato'])}</span><span class="chip {estc}">{H.escape(est)}</span></div>
    <h2>{H.escape(it['titulo_reel'])}</h2>
    <details><summary>Texto del posteo</summary><p class="cap">{esc(it['caption'])}</p></details>
    <div class="stories">{hs}</div>
  </div>
</article>'''

n_reels, n_hist = len(items), sum(len(v) for v in hist.values())
page = f'''<title>Calendario CROMA</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=JetBrains+Mono:wght@500&display=swap">
<style>
/* Lista cronológica: cada fecha es una fila con el reel, su texto y las dos historias del día. */
:root{{--bg:#f7f3ff;--surface:#ffffff;--ink:#2a1458;--muted:#5e5378;--line:#ddd2f2;--accent:#7c4ddb;--brand:#512974;--tint:#ede4fe;
  --ok-bg:#e1f4ea;--ok-ink:#12623f;--info-bg:#e7eefb;--info-ink:#1f4a99;
  --display:'Sora',system-ui,sans-serif;--body:'Sora',system-ui,sans-serif;--mono:'JetBrains Mono',ui-monospace,monospace}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#120f1e;--surface:#1b1530;--ink:#f7f3ff;--muted:#c4bbd9;--line:#3a2f5c;--accent:#bda8e3;--brand:#bda8e3;--tint:#2e2350;
  --ok-bg:#10301f;--ok-ink:#8fe0bb;--info-bg:#1b2645;--info-ink:#a9c4f7;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#120f1e;--surface:#1b1530;--ink:#f7f3ff;--muted:#c4bbd9;--line:#3a2f5c;--accent:#bda8e3;--brand:#bda8e3;--tint:#2e2350;
  --ok-bg:#10301f;--ok-ink:#8fe0bb;--info-bg:#1b2645;--info-ink:#a9c4f7;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--ink);font:400 16px/1.55 var(--body);margin:0}}
.wrap{{max-width:1080px;margin:0 auto;padding-block:40px 80px;padding-left:max(16px, env(safe-area-inset-left, 0px));padding-right:max(16px, env(safe-area-inset-right, 0px))}}
header{{display:grid;gap:14px;margin-bottom:34px}}
.eyebrow{{font:500 13px/1 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--accent)}}
h1{{font:700 clamp(30px,5vw,46px)/1.08 var(--display);letter-spacing:-.02em;margin:0;text-wrap:balance}}
.lead{{color:var(--muted);max-width:64ch;margin:0}}
.facts{{display:flex;flex-wrap:wrap;gap:10px;margin-top:6px}}
.fact{{font:600 14px/1 var(--body);padding:10px 14px;border-radius:12px;background:var(--tint);color:var(--ink);font-variant-numeric:tabular-nums}}
.entry{{display:grid;grid-template-columns:84px 270px minmax(0,1fr);gap:24px;padding:26px 0;border-top:1px solid var(--line);align-items:start}}
.when{{display:grid;justify-items:center;gap:2px;padding-top:4px}}
.dow{{font:500 12px/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}}
.day{{font:700 44px/1 var(--display);color:var(--brand);font-variant-numeric:tabular-nums}}
.mon{{font:600 14px/1 var(--body);color:var(--muted)}}
.reel video{{display:block;width:270px;max-width:100%;aspect-ratio:9/16;height:auto;border-radius:18px;background:#120f1e}}
.info{{min-width:0;display:grid;gap:12px}}
.meta{{display:flex;flex-wrap:wrap;gap:8px;align-items:center}}
.time{{font:500 13px/1 var(--mono);color:var(--muted);margin-right:4px}}
.chip{{font:600 12.5px/1 var(--body);padding:7px 10px;border-radius:9px;background:var(--tint);color:var(--ink)}}
.chip.new{{background:var(--info-bg);color:var(--info-ink)}} .chip.set{{background:var(--ok-bg);color:var(--ok-ink)}}
h2{{font:700 22px/1.25 var(--display);margin:0;text-wrap:balance}}
details{{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:12px 16px}}
summary{{cursor:pointer;font:600 14px/1.4 var(--body);color:var(--accent)}}
summary:focus-visible,video:focus-visible{{outline:2px solid var(--accent);outline-offset:3px}}
.cap{{margin:12px 0 4px;color:var(--ink);font-size:14.5px;line-height:1.6;max-width:65ch}}
.stories{{display:flex;flex-wrap:wrap;gap:14px}}
.story{{margin:0;display:grid;gap:6px;width:150px}}
.story img{{width:150px;height:auto;aspect-ratio:9/16;border-radius:12px;border:1px solid var(--line);display:block}}
figcaption{{font:500 12.5px/1.3 var(--body);color:var(--muted)}}
figcaption .t{{font:500 12.5px/1 var(--mono);color:var(--ink)}}
footer{{margin-top:30px;padding-top:20px;border-top:1px solid var(--line);color:var(--muted);font-size:14px}}
@media (max-width:760px){{.entry{{grid-template-columns:64px minmax(0,1fr);gap:16px}} .reel{{grid-column:2}} .info{{grid-column:1 / -1}} .day{{font-size:36px}}}}
@media (prefers-reduced-motion:reduce){{*{{scroll-behavior:auto}}}}
</style>
<div class="wrap">
<header>
  <span class="eyebrow">Instagram @cromacmms · 30 de octubre al 18 de diciembre</span>
  <h1>Lo que sale hasta el 18 de diciembre</h1>
  <p class="lead">Reels los martes y jueves a las 10:05, y esos mismos días dos historias: a las 18:05 la que anuncia el reel y a las 18:10 un tip o una pregunta. Tocá cada reel para verlo y abrí "Texto del posteo" para leer lo que va abajo.</p>
  <div class="facts"><span class="fact">{n_reels} reels</span><span class="fact">{n_hist} historias</span><span class="fact">Todo programado con publicación automática</span><span class="fact">Cada pieza también en tu Google Calendar</span></div>
</header>
{cards}
<footer>Los videos de esta página están en calidad reducida para que carguen rápido; en Instagram salen en 1080 × 1920. Las interfaces y los datos que aparecen son ilustrativos.</footer>
</div>'''
open(os.path.join(OUT, 'index.html'), 'w').write(page)
print('ok', n_reels, n_hist)
