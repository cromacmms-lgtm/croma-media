"""Ilustraciones de equipos para el motor de reels (960 x 480, línea lavanda).
Los ids hl_* son resaltes que el plan prende en cada paso. data-rot / data-flow / data-slide animan piezas."""
LV, WH = '#bda8e3', '#ece5fa'


def motor():
    fins = ''.join(f'<line x1="{x}" y1="138" x2="{x}" y2="362"/>' for x in range(190, 250, 16)) + \
           ''.join(f'<line x1="{x}" y1="138" x2="{x}" y2="362"/>' for x in range(546, 620, 16))
    coils = ''.join(f'<path d="M{x},188 q14,62 0,124" />' for x in range(282, 520, 26))
    blades = ''.join(f'<path d="M0,0 L-6,-62 Q10,-58 12,-8 Z" transform="rotate({k*45})" fill="rgba(189,168,227,.35)"/>' for k in range(8))
    stripes = ''.join(f'<line x1="{x}" y1="228" x2="{x-16}" y2="272"/>' for x in range(660, 900, 24))
    return f'''<svg width="960" height="480" viewBox="0 0 960 480" style="position:absolute;left:0;top:0">
 <defs><clipPath id="shc"><rect x="690" y="230" width="190" height="40" rx="6"/></clipPath>
  <clipPath id="fanc"><rect x="74" y="146" width="86" height="208" rx="22"/></clipPath></defs>
 <g fill="none" stroke="{LV}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round">
  <rect x="100" y="410" width="780" height="24" rx="6" fill="rgba(189,168,227,.14)"/>
  <rect x="210" y="372" width="70" height="38" rx="4"/><rect x="520" y="372" width="70" height="38" rx="4"/>
  <rect x="150" y="120" width="490" height="260" rx="44" fill="rgba(189,168,227,.12)"/>
  <g stroke="rgba(189,168,227,.5)" stroke-width="3">{fins}</g>
  <rect x="262" y="172" width="276" height="156" rx="22" fill="rgba(18,15,30,.45)" stroke="rgba(236,229,250,.55)"/>
  <g stroke="#e8b27a" stroke-width="5" opacity=".9">{coils}</g>
  <rect x="320" y="66" width="150" height="58" rx="10" fill="rgba(189,168,227,.14)"/>
  <circle cx="358" cy="95" r="8"/><circle cx="395" cy="95" r="8"/><circle cx="432" cy="95" r="8"/>
  <rect x="640" y="158" width="52" height="184" rx="14" fill="rgba(189,168,227,.12)"/>
  <rect x="690" y="230" width="190" height="40" rx="6" fill="rgba(189,168,227,.10)"/>
  <g clip-path="url(#shc)" stroke="rgba(236,229,250,.6)" stroke-width="4"><g data-slide="120,24">{stripes}</g></g>
  <rect x="74" y="146" width="86" height="208" rx="22" fill="rgba(189,168,227,.10)"/>
  <g clip-path="url(#fanc)"><g data-rot="117,250,600" stroke="{WH}" stroke-width="2.5">{blades}<circle r="10" fill="{WH}"/></g></g>
  <circle cx="176" cy="250" r="16" stroke="{WH}"/><circle cx="666" cy="250" r="16" stroke="{WH}"/>
 </g>
 <g font-family="Sora" font-size="22" fill="#c4bbd9" text-anchor="middle" data-a="0.5" data-b="3.6" data-fx="fade">
  <text x="117" y="470">Ventilador</text><text x="400" y="52">Caja de bornes</text><text x="400" y="470">Estator y bobinado</text><text x="785" y="470">Eje lado acople</text>
 </g>
 <g fill="none" stroke="#f07070" stroke-width="5">
  <g id="hl_rod" opacity="0"><circle cx="176" cy="250" r="30"/><circle cx="666" cy="250" r="30"/></g>
  <rect id="hl_bob" x="252" y="162" width="296" height="176" rx="28" opacity="0"/>
  <rect id="hl_vent" x="64" y="136" width="106" height="228" rx="28" opacity="0"/>
  <rect id="hl_bor" x="308" y="54" width="174" height="82" rx="16" opacity="0"/>
 </g>
</svg>'''
