"""CROMA — generador de piezas para redes.

Uso:
    python3 engine/croma.py content/<archivo>.json [...]
Lee cada especificación JSON, arma una página HTML por slide con el sistema de diseño de CROMA
y la renderiza a JPG (1080×1350 publicaciones, 1080×1920 historias) en media/<slug>/NN.jpg.

Texto enriquecido en cualquier campo: **palabra** = color de acento.
"""
import html, json, os, re, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENG = os.path.join(ROOT, 'engine')

THEMES = {
    'claro':   dict(bg='#ffffff', grid='#e6dcf9', gridop=.6, ink='#2a1458', muted='#5e5378', acc='#7c4ddb', eti='#7c4ddb',
                    ring='#bda8e3', logo='croma-logo-color.png', iso='croma-isotipo-violeta.png', ico='#512974',
                    card='#f7f3ff', cardbd='#ddd2f2', pill='#512974', pillink='#ffffff', bar='#ddd2f2', baron='#7c4ddb'),
    'suave':   dict(bg='#f7f3ff', grid='#e6dcf9', gridop=.75, ink='#2a1458', muted='#5e5378', acc='#7c4ddb', eti='#7c4ddb',
                    ring='#bda8e3', logo='croma-logo-color.png', iso='croma-isotipo-violeta.png', ico='#512974',
                    card='#ffffff', cardbd='#ddd2f2', pill='#512974', pillink='#ffffff', bar='#ddd2f2', baron='#7c4ddb'),
    'violeta': dict(bg='#512974', grid='rgba(189,168,227,.16)', gridop=1, ink='#ffffff', muted='#ece5fa', acc='#bda8e3', eti='#bda8e3',
                    ring='rgba(189,168,227,.20)', logo='croma-logo-blanco.png', iso='croma-isotipo-blanco.png', ico='#bda8e3',
                    card='#2a1458', cardbd='#2a1458', pill='#ffffff', pillink='#512974', bar='rgba(189,168,227,.30)', baron='#ffffff'),
    'noche':   dict(bg='#120f1e', grid='rgba(189,168,227,.10)', gridop=1, ink='#f7f3ff', muted='#c4bbd9', acc='#bda8e3', eti='#bda8e3',
                    ring='#2e2350', logo='croma-logo-fondo-oscuro.png', iso='croma-isotipo-blanco.png', ico='#bda8e3',
                    card='#221a38', cardbd='#3a2f5c', pill='#bda8e3', pillink='#2a1458', bar='#3a2f5c', baron='#bda8e3'),
}

ICONS = json.load(open(os.path.join(ENG, 'icons-base.json')))
ICONS.update({
    'check': '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    'x': '<path d="M6.5 6.5l11 11M17.5 6.5l-11 11"/>',
    'flecha': '<path d="M5 12h14M13 6l6 6-6 6"/>',
    'celular': '<rect x="6.5" y="2.5" width="11" height="19" rx="2.5"/><path d="M10.5 18.5h3"/>',
    'mensaje': '<path d="M4 5.5h16a1.5 1.5 0 0 1 1.5 1.5v9a1.5 1.5 0 0 1-1.5 1.5H10l-4.5 3.5V17.5H4A1.5 1.5 0 0 1 2.5 16V7A1.5 1.5 0 0 1 4 5.5z"/><path d="M7.5 10.5h9M7.5 13.5h6"/>',
    'mail': '<rect x="2.5" y="5" width="19" height="14" rx="2"/><path d="M3 6.5l9 6.5 9-6.5"/>',
    'pileta': '<path d="M2 14c2 0 2-1.5 4-1.5s2 1.5 4 1.5 2-1.5 4-1.5 2 1.5 4 1.5 2-1.5 4-1.5"/><path d="M2 18.5c2 0 2-1.5 4-1.5s2 1.5 4 1.5 2-1.5 4-1.5 2 1.5 4 1.5 2-1.5 4-1.5"/><path d="M8 11V5.5a2 2 0 0 1 4 0M14 11V5.5a2 2 0 0 1 4 0M8 8h4M14 8h4"/>',
    'llama': '<path d="M12 2.5c.8 3 4.5 5 4.5 10a4.5 4.5 0 0 1-9 0c0-2.2 1-3.8 2.2-5 .1 2.2 1 3.3 2.3 3.3 0-3.2-1-5.6 0-8.3z"/><path d="M10.5 17a1.5 1.5 0 0 0 3 0c0-1.3-1.5-2.2-1.5-3.5-.8.8-1.5 2-1.5 3.5z"/>',
    'copo': '<path d="M12 2.5v19M3.8 7.25l16.4 9.5M20.2 7.25 3.8 16.75"/><path d="M9.5 4 12 6.5 14.5 4M9.5 20 12 17.5 14.5 20M4.2 10.3l3.4-.9-.9-3.4M19.8 13.7l-3.4.9.9 3.4M4.2 13.7l3.4.9-.9 3.4M19.8 10.3l-3.4-.9.9-3.4"/>',
    'rayo': '<path d="M13 2.5 4.5 13.5h6.5l-1 8 8.5-11h-6.5z"/>',
    'gota': '<path d="M12 3c3 4 6 7.3 6 11a6 6 0 0 1-12 0c0-3.7 3-7 6-11z"/><path d="M9 14.5a3 3 0 0 0 3 3"/>',
    'escudo': '<path d="M12 3l7 2.8v5.4c0 4.8-3 8.3-7 9.8-4-1.5-7-5-7-9.8V5.8z"/><path d="M9 12l2 2 4-4"/>',
    'filtro': '<path d="M3.5 4.5h17l-6.5 7.5v6l-4 2v-8z"/>',
    'correa': '<circle cx="7" cy="12" r="4"/><circle cx="17.5" cy="12" r="2.5"/><path d="M7 8l10.5 1.5M7 16l10.5-1.5"/><circle cx="7" cy="12" r="1"/>',
    'termometro': '<path d="M14 14.5V5a2 2 0 0 0-4 0v9.5a4 4 0 1 0 4 0z"/><path d="M12 9v8"/>',
    'generador': '<rect x="2.5" y="6" width="19" height="12" rx="2"/><path d="M12.8 8.5 9.8 12.6h3l-.9 3.4 3.3-4.6h-3.2z"/><path d="M6 18v2M18 18v2"/>',
    'cuchilla': '<path d="M3 13.5l3-4 3 4 3-4 3 4 3-4 3 4"/><path d="M3 17.5h18"/>',
    'moneda': '<circle cx="12" cy="12" r="9"/><path d="M14.6 9.6c-.5-1-1.5-1.6-2.6-1.6-1.4 0-2.5.8-2.5 2s1 1.6 2.5 2 2.5.9 2.5 2.1-1.1 2-2.5 2c-1.1 0-2.2-.6-2.7-1.6M12 6.5V8M12 16v1.5"/>',
    'persona': '<circle cx="12" cy="7.5" r="3.5"/><path d="M5 20.5v-1a5 5 0 0 1 5-5h4a5 5 0 0 1 5 5v1"/>',
    'camion': '<path d="M2.5 6.5h11v10h-11zM13.5 10h4.5l3.5 3.5v3h-8"/><circle cx="6.5" cy="17.5" r="2"/><circle cx="17" cy="17.5" r="2"/>',
    'carrito': '<path d="M2.5 3.5h2.5l2.4 11.5h11l2.1-8H6.2"/><circle cx="9.5" cy="19" r="1.5"/><circle cx="17" cy="19" r="1.5"/>',
    'libro': '<path d="M4 4.5h6a2 2 0 0 1 2 2v13a2 2 0 0 0-2-2H4zM20 4.5h-6a2 2 0 0 0-2 2v13a2 2 0 0 1 2-2h6z"/>',
    'caja': '<path d="M3.5 7.5 12 3l8.5 4.5v9L12 21l-8.5-4.5z"/><path d="M3.5 7.5 12 12l8.5-4.5M12 12v9"/>',
    'lupa': '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/>',
    'tendencia': '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
})

def ico(name, color, size, sw=1.75, extra=''):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" {extra}>{ICONS[name]}</svg>')

def rt(s, acc):
    """Texto enriquecido: escapa y pinta **acento**. Admite saltos con \\n."""
    s = html.escape(s)
    s = re.sub(r'\*\*(.+?)\*\*', lambda m: f'<span style="color:{acc}">{m.group(1)}</span>', s)
    return s.replace('\n', '<br>')

FONTS = ''.join(
    f'@font-face{{font-family:Sora;font-weight:{w};src:url(file://{ENG}/fonts/sora-latin-{w}-normal.woff2)}}'
    f'@font-face{{font-family:Sora;font-weight:{w};src:url(file://{ENG}/fonts/sora-latin-ext-{w}-normal.woff2);unicode-range:U+0100-024F}}'
    for w in (400, 600, 700)) + f'@font-face{{font-family:JBM;font-weight:500;src:url(file://{ENG}/fonts/jetbrains-mono-latin-500-normal.woff2)}}'

def page(t, W, H, body, deco=''):
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{FONTS}
html,body{{margin:0;width:{W}px;height:{H}px;overflow:hidden}}*{{box-sizing:border-box}}
.root{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:{t['bg']};color:{t['ink']};font-family:Sora,sans-serif}}
.plano{{position:absolute;inset:0;opacity:{t['gridop']};background-image:linear-gradient({t['grid']} 2px,transparent 2px),linear-gradient(90deg,{t['grid']} 2px,transparent 2px);background-size:80px 80px;background-position:-1px -1px}}
.anillo{{position:absolute;border-radius:50%;-webkit-mask:linear-gradient(#000 0 calc(50% - 15px),transparent 0 calc(50% + 15px),#000 0);mask:linear-gradient(#000 0 calc(50% - 15px),transparent 0 calc(50% + 15px),#000 0)}}
.eti{{font:600 26px/34px Sora;letter-spacing:.14em;text-transform:uppercase;color:{t['eti']};margin:0}}
.mono{{font:500 28px/36px JBM,monospace;letter-spacing:.04em}}
p,h1,h2,h3{{margin:0}}
</style></head><body><div class="root"><div class="plano"></div>{deco}{body}</div></body></html>'''

def ring(t, size, pos, border=104):
    return f'<div class="anillo" style="width:{size}px;height:{size}px;{pos};border:{border}px solid {t["ring"]}"></div>'

def bigicon(t, name, size, pos, op=1, sw=1.1):
    return f'<div style="position:absolute;{pos};opacity:{op}">{ico(name, t["ring"], size, sw)}</div>'

def header(t, n, total, cover=False):
    logo = (f'<img src="file://{ENG}/logos/{t["logo"]}" style="width:250px;display:block">' if cover
            else f'<img src="file://{ENG}/logos/{t["iso"]}" style="width:62px;height:62px;display:block">')
    bars = ''.join(f'<i style="display:block;height:8px;border-radius:4px;width:{64 if i == n else 26}px;background:{t["baron"] if i == n else t["bar"]}"></i>'
                   for i in range(1, total + 1))
    return (f'<div style="position:absolute;left:80px;right:80px;top:80px;height:64px;display:flex;justify-content:space-between;align-items:center">'
            f'{logo}<div style="display:flex;align-items:center;gap:22px"><div style="display:flex;gap:8px">{bars}</div>'
            f'<span class="mono" style="color:{t["muted"]}">{n:02d}/{total:02d}</span></div></div>')

def footer(t, last=False):
    right = '' if last else f'<span style="display:flex;align-items:center;gap:10px;font:600 26px/36px Sora;color:{t["acc"]}">Deslizá {ico("flecha", t["acc"], 34)}</span>'
    return (f'<div style="position:absolute;left:80px;right:80px;bottom:72px;display:flex;justify-content:space-between;align-items:center">'
            f'<span class="mono" style="font-size:24px;color:{t["muted"]}">@cromacmms</span>{right}</div>')

# ---------------------------------------------------------------- plantillas de publicación (1080×1350)
W, H = 1080, 1350

def tpl_cover(s, t, n, N):
    deco = ''
    d = s.get('deco', 'ring')
    if d == 'ring':
        deco = ring(t, 820, 'top:-260px;right:-330px')
    elif d == 'icon':
        deco = bigicon(t, s['icon'], 540, 'right:-110px;top:150px', .55 if t['bg'] in ('#ffffff', '#f7f3ff') else 1, 1.0)
    chips = ''.join(f'<span style="display:inline-flex;align-items:center;gap:12px;height:64px;padding:0 28px 0 22px;border-radius:999px;background:{t["card"]};'
                    f'box-shadow:inset 0 0 0 2px {t["cardbd"]};font:600 26px/1 Sora;color:{t["ink"]}">{ico(c[1], t["ico"], 30)}{html.escape(c[0])}</span>'
                    for c in s.get('chips', []))
    body = (header(t, n, N, cover=True) +
            f'<div style="position:absolute;left:80px;right:80px;bottom:168px">'
            f'<p class="eti">{rt(s["eti"], t["acc"])}</p>'
            f'<h1 style="margin-top:26px;font:700 {s.get("size", 104)}px/{s.get("lh", 1.0)} Sora;letter-spacing:-.025em;max-width:{s.get("maxw", 900)}px">{rt(s["title"], t["acc"])}</h1>'
            + (f'<p style="margin-top:34px;font:400 40px/54px Sora;color:{t["muted"]};max-width:840px">{rt(s["sub"], t["acc"])}</p>' if s.get('sub') else '')
            + (f'<div style="display:flex;gap:16px;flex-wrap:wrap;margin-top:44px">{chips}</div>' if chips else '') +
            '</div>' + footer(t))
    return page(t, W, H, body, deco)

def tpl_brand(s, t, n, N):
    deco = ring(t, 900, 'bottom:-330px;right:-360px')
    body = (f'<div style="position:absolute;left:80px;right:80px;top:80px;display:flex;justify-content:flex-end"><span class="mono" style="color:{t["muted"]}">{n:02d}/{N:02d}</span></div>'
            f'<div style="position:absolute;left:80px;right:80px;top:380px">'
            f'<p class="eti">{rt(s["eti"], t["acc"])}</p>'
            f'<img src="file://{ENG}/logos/{t["logo"]}" style="width:820px;display:block;margin-top:40px">'
            f'<p style="margin-top:56px;font:700 64px/72px Sora;letter-spacing:-.01em;max-width:860px">{rt(s["title"], t["acc"])}</p>'
            f'<p style="margin-top:28px;font:400 36px/50px Sora;color:{t["muted"]};max-width:800px">{rt(s.get("sub", ""), t["acc"])}</p></div>' + footer(t))
    return page(t, W, H, body, deco)

def tpl_text(s, t, n, N):
    box = ''
    if s.get('box'):
        b = s['box']
        box = (f'<div style="margin-top:56px;background:{t["card"]};box-shadow:inset 0 0 0 2px {t["cardbd"]};border-radius:32px;padding:44px 48px;display:flex;gap:28px;align-items:flex-start">'
               f'{ico(b.get("icon", "check"), t["ico"], 64, 1.6)}<div><p class="eti" style="margin-bottom:12px">{rt(b.get("eti", ""), t["acc"])}</p>'
               f'<p style="font:600 34px/48px Sora">{rt(b["text"], t["acc"])}</p></div></div>')
    deco = bigicon(t, s['icon'], 480, 'right:-90px;bottom:110px', .9, 1.0) if s.get('icon') else ''
    paras = ''.join(f'<p style="margin-top:28px;font:400 36px/52px Sora;color:{t["muted"]};max-width:880px">{rt(p, t["acc"])}</p>' for p in s.get('body', []))
    body = (header(t, n, N) + f'<div style="position:absolute;left:80px;right:80px;top:170px;bottom:150px;display:flex;flex-direction:column;justify-content:center">'
            f'<p class="eti">{rt(s["eti"], t["acc"])}</p>'
            f'<h2 style="margin-top:24px;font:700 {s.get("size", 80)}px/{s.get("lh", 1.05)} Sora;letter-spacing:-.015em;max-width:{s.get("maxw", 880)}px">{rt(s["title"], t["acc"])}</h2>'
            f'{paras}{box}</div>' + footer(t, n == N))
    return page(t, W, H, body, deco)

def tpl_items(s, t, n, N):
    items = s['items']
    rows = ''
    for i, it in enumerate(items):
        sep = f'border-top:2px solid {t["cardbd"]};' if i else ''
        num = f'<span class="mono" style="color:{t["acc"]};font-size:30px;width:64px;flex:none;padding-top:10px">{html.escape(it.get("num", ""))}</span>' if it.get('num') else ''
        rows += (f'<div style="display:flex;gap:28px;align-items:flex-start;padding:{s.get("pad", 44)}px 0;{sep}">{num}'
                 f'<div style="width:96px;height:96px;flex:none;border-radius:28px;background:{t["card"]};box-shadow:inset 0 0 0 2px {t["cardbd"]};display:grid;place-items:center">{ico(it["icon"], t["ico"], 56, 1.6)}</div>'
                 f'<div><p style="font:700 40px/50px Sora">{rt(it["title"], t["acc"])}</p>'
                 + (f'<p style="margin-top:10px;font:400 30px/44px Sora;color:{t["muted"]}">{rt(it["text"], t["acc"])}</p>' if it.get('text') else '') + '</div></div>')
    body = (header(t, n, N) + f'<div style="position:absolute;left:80px;right:80px;top:170px;bottom:150px;display:flex;flex-direction:column;justify-content:center">'
            f'<p class="eti">{rt(s["eti"], t["acc"])}</p>'
            + (f'<h2 style="margin:22px 0 18px;font:700 {s.get("size", 64)}px/1.08 Sora;letter-spacing:-.01em;max-width:900px">{rt(s["title"], t["acc"])}</h2>' if s.get('title') else '<div style="height:18px"></div>')
            + rows + '</div>' + footer(t, n == N))
    return page(t, W, H, body)

def tpl_formula(s, t, n, N):
    good = s.get('good')
    goodhtml = (f'<div style="display:inline-flex;align-items:center;gap:14px;margin-top:40px;height:64px;padding:0 28px;border-radius:999px;background:{t["pill"]};color:{t["pillink"]};font:600 28px/1 Sora">'
                f'{ico("tendencia" if good == "alto" else "check", t["pillink"], 30, 2)}{html.escape(s["goodtext"])}</div>') if good else ''
    body = (header(t, n, N) + f'<div style="position:absolute;left:80px;right:80px;top:170px;bottom:150px;display:flex;flex-direction:column;justify-content:center">'
            f'<p class="eti">{rt(s["eti"], t["acc"])}</p>'
            f'<h2 style="margin-top:22px;font:700 76px/1.05 Sora;letter-spacing:-.015em">{rt(s["title"], t["acc"])}</h2>'
            f'<p style="margin-top:22px;font:400 36px/50px Sora;color:{t["muted"]};max-width:880px">{rt(s["lead"], t["acc"])}</p>'
            f'<div style="margin-top:56px;background:{t["card"]};box-shadow:inset 0 0 0 2px {t["cardbd"]};border-radius:32px;padding:52px 56px;display:flex;align-items:center;gap:36px">'
            f'<span style="font:700 72px/1 Sora;letter-spacing:-.02em;color:{t["acc"]}">{html.escape(s["name"])}</span><span style="font:400 64px/1 Sora;color:{t["muted"]}">=</span>'
            f'<div style="flex:1;text-align:center"><p style="font:600 34px/44px Sora">{rt(s["num"], t["acc"])}</p>'
            f'<div style="height:4px;background:{t["ink"]};margin:18px 0;border-radius:2px"></div><p style="font:600 34px/44px Sora">{rt(s["den"], t["acc"])}</p></div></div>'
            f'{goodhtml}</div>' + footer(t, n == N))
    return page(t, W, H, body)

def tpl_example(s, t, n, N):
    rows = ''.join(
        f'<div style="flex:1;background:{t["card"]};box-shadow:inset 0 0 0 2px {t["cardbd"]};border-radius:32px;padding:40px 40px 44px">'
        f'<p class="eti" style="color:{t["muted"]}">{rt(r["label"], t["acc"])}</p>'
        f'<p class="mono" style="margin-top:18px;font-size:30px;color:{t["muted"]}">{html.escape(r["calc"])}</p>'
        f'<p style="margin-top:14px;font:700 120px/1 Sora;letter-spacing:-.04em;color:{t["ink"]}">{html.escape(r["value"])}<span style="font-size:52px;color:{t["acc"]};margin-left:10px">{html.escape(r.get("unit", ""))}</span></p></div>'
        for r in s['results'])
    body = (header(t, n, N) + f'<div style="position:absolute;left:80px;right:80px;top:170px;bottom:150px;display:flex;flex-direction:column;justify-content:center">'
            f'<p class="eti">{rt(s["eti"], t["acc"])}</p>'
            f'<h2 style="margin-top:22px;font:700 {s.get("size", 64)}px/1.1 Sora;letter-spacing:-.01em;max-width:900px">{rt(s["title"], t["acc"])}</h2>'
            f'<p style="margin-top:24px;font:400 34px/50px Sora;color:{t["muted"]};max-width:900px">{rt(s["lead"], t["acc"])}</p>'
            f'<div style="display:flex;gap:24px;margin-top:52px">{rows}</div>'
            + (f'<p style="margin-top:36px;font:400 28px/40px Sora;color:{t["muted"]}">{rt(s["note"], t["acc"])}</p>' if s.get('note') else '')
            + '</div>' + footer(t, n == N))
    return page(t, W, H, body)

def tpl_compare(s, t, n, N):
    def col(c, hi):
        bg = t['pill'] if hi else t['card']
        ink = t['pillink'] if hi else t['ink']
        sub = t['pillink'] if hi else t['muted']
        lis = ''.join(f'<li style="display:flex;gap:16px;align-items:flex-start;font:400 30px/42px Sora;color:{sub}">'
                      f'{ico(c.get("mark", "check"), ink, 36, 2)}<span>{rt(x, ink)}</span></li>' for x in c['list'])
        return (f'<div style="flex:1;background:{bg};box-shadow:inset 0 0 0 2px {t["cardbd"] if not hi else bg};border-radius:32px;padding:44px 40px">'
                f'{ico(c["icon"], ink, 64, 1.6)}<p style="margin-top:22px;font:700 44px/52px Sora;color:{ink}">{html.escape(c["name"])}</p>'
                f'<ul style="list-style:none;margin:26px 0 0;padding:0;display:flex;flex-direction:column;gap:22px">{lis}</ul></div>')
    body = (header(t, n, N) + f'<div style="position:absolute;left:80px;right:80px;top:170px;bottom:150px;display:flex;flex-direction:column;justify-content:center">'
            f'<p class="eti">{rt(s["eti"], t["acc"])}</p>'
            f'<h2 style="margin-top:22px;font:700 64px/1.1 Sora;letter-spacing:-.01em;max-width:900px">{rt(s["title"], t["acc"])}</h2>'
            f'<div style="display:flex;gap:24px;margin-top:48px">{col(s["a"], False)}{col(s["b"], True)}</div></div>' + footer(t, n == N))
    return page(t, W, H, body)

def tpl_cta(s, t, n, N):
    deco = ring(t, 860, 'bottom:-300px;right:-360px')
    contacts = (f'<div style="display:flex;flex-direction:column;gap:22px;margin-top:52px">'
                f'<div style="display:flex;align-items:center;gap:20px;font:600 36px/1 Sora">{ico("mensaje", t["acc"], 48, 1.7)}DM a @cromacmms</div>'
                f'<div style="display:flex;align-items:center;gap:20px;font:600 36px/1 Sora">{ico("mail", t["acc"], 48, 1.7)}cromacmms@gmail.com</div></div>')
    save = (f'<div style="display:inline-flex;align-items:center;gap:16px;margin-top:56px;height:96px;padding:0 44px;border-radius:999px;background:{t["pill"]};color:{t["pillink"]};font:700 36px/1 Sora">'
            f'{ico(s.get("pillicon", "libro"), t["pillink"], 40, 2)}{html.escape(s["pill"])}</div>') if s.get('pill') else ''
    body = (f'<div style="position:absolute;left:80px;right:80px;top:80px;display:flex;justify-content:flex-end"><span class="mono" style="color:{t["muted"]}">{n:02d}/{N:02d}</span></div>'
            f'<div style="position:absolute;left:80px;right:80px;top:250px">'
            f'<p class="eti">{rt(s["eti"], t["acc"])}</p>'
            f'<h2 style="margin-top:24px;font:700 {s.get("size", 84)}px/1.04 Sora;letter-spacing:-.02em;max-width:900px">{rt(s["title"], t["acc"])}</h2>'
            + (f'<p style="margin-top:30px;font:400 36px/52px Sora;color:{t["muted"]};max-width:860px">{rt(s["body"], t["acc"])}</p>' if s.get('body') else '')
            + save + contacts + '</div>'
            f'<img src="file://{ENG}/logos/{t["logo"]}" style="position:absolute;left:80px;bottom:80px;width:300px">')
    return page(t, W, H, body, deco)

# ---------------------------------------------------------------- historias (1080×1920)
SW, SH = 1080, 1920

def story_frame(t, inner, deco=''):
    foot = f'<img src="file://{ENG}/logos/{t["logo"]}" style="position:absolute;left:72px;bottom:360px;width:260px">'
    return page(t, SW, SH, f'<div style="position:absolute;left:72px;right:72px;top:260px;bottom:500px;display:flex;flex-direction:column;justify-content:center">{inner}</div>{foot}', deco)

def tpl_story(s, t):
    kind = s.get('kind', 'statement')
    deco = ring(t, 900, 'top:-260px;right:-380px') if s.get('ring', True) else ''
    inner = f'<div style="margin-bottom:56px">{ico(s["icon"], t["acc"], 150, 1.5)}</div>' if s.get('icon') else ''
    inner += f'<p class="eti" style="font-size:30px;line-height:40px">{rt(s["eti"], t["acc"])}</p>'
    inner += f'<h1 style="margin-top:30px;font:700 {s.get("size", 100)}px/1.04 Sora;letter-spacing:-.02em">{rt(s["title"], t["acc"])}</h1>'
    if s.get('sub'):
        inner += f'<p style="margin-top:36px;font:400 44px/60px Sora;color:{t["muted"]}">{rt(s["sub"], t["acc"])}</p>'
    if kind == 'question':
        opts = ''.join(f'<div style="display:flex;align-items:center;gap:22px;height:104px;padding:0 36px;border-radius:28px;background:{t["card"]};box-shadow:inset 0 0 0 2px {t["cardbd"]};font:600 40px/1 Sora">'
                       f'<span class="mono" style="font-size:32px;color:{t["acc"]}">{chr(65 + i)}</span>{html.escape(o)}</div>' for i, o in enumerate(s['options']))
        inner += f'<div style="display:flex;flex-direction:column;gap:20px;margin-top:56px">{opts}</div>'
    if s.get('cta'):
        inner += (f'<div style="align-self:flex-start;display:inline-flex;align-items:center;gap:18px;margin-top:60px;height:104px;padding:0 48px;border-radius:999px;background:{t["pill"]};color:{t["pillink"]};font:700 40px/1 Sora">'
                  f'{ico(s.get("ctaicon", "mensaje"), t["pillink"], 44, 2)}{html.escape(s["cta"])}</div>')
    if s.get('contacts'):
        inner += (f'<div style="display:flex;flex-direction:column;gap:28px;margin-top:64px">'
                  f'<div style="display:flex;align-items:center;gap:22px;font:600 44px/1 Sora">{ico("mensaje", t["acc"], 56, 1.7)}DM a @cromacmms</div>'
                  f'<div style="display:flex;align-items:center;gap:22px;font:600 44px/1 Sora">{ico("mail", t["acc"], 56, 1.7)}cromacmms@gmail.com</div></div>')
    return story_frame(t, inner, deco)

TPL = dict(cover=tpl_cover, brand=tpl_brand, text=tpl_text, items=tpl_items, formula=tpl_formula,
           example=tpl_example, compare=tpl_compare, cta=tpl_cta)

def build(spec_path, outdir_root=os.path.join(ROOT, 'media')):
    spec = json.load(open(spec_path))
    slug = spec['slug']
    out = os.path.join(outdir_root, slug)
    os.makedirs(out, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix='croma-')
    jobs = []
    if spec['format'] == 'story':
        pages = [(tpl_story(spec['story'], THEMES[spec['story'].get('theme', 'violeta')]), SW, SH)]
    else:
        N = len(spec['slides'])
        pages = [(TPL[s['tpl']](s, THEMES[s.get('theme', 'claro')], i + 1, N), W, H) for i, s in enumerate(spec['slides'])]
    for i, (h, w, hh) in enumerate(pages, 1):
        hp = os.path.join(tmp, f'{i:02d}.html')
        open(hp, 'w').write(h)
        jobs.append({'html': hp, 'out': os.path.join(out, f'{i:02d}.jpg'), 'w': w, 'h': hh})
    jp = os.path.join(tmp, 'jobs.json')
    json.dump(jobs, open(jp, 'w'))
    subprocess.run(['node', os.path.join(ENG, 'render.js'), jp], check=True)
    return [j['out'] for j in jobs]

if __name__ == '__main__':
    for p in sys.argv[1:]:
        for o in build(p):
            print(o)
