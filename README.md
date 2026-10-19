# CROMA — medios para redes

Este repositorio guarda las piezas que se publican en el Instagram de CROMA (@cromacmms) y el generador que las produce. Todo lo que hay acá es público: solo contenido que se va a publicar.

## Cómo funciona

1. Cada pieza se describe en `content/<fecha>-<tema>.json`: formato (`carousel`, `story`, `reel`), fecha y hora, texto del posteo y slides.
2. `python3 engine/croma.py content/<archivo>.json` arma las slides con el sistema de diseño de CROMA y las guarda en `media/<slug>/NN.jpg` (publicaciones 1080×1350, historias 1080×1920). Necesita Node con `playwright` (`npm i playwright`) y un Chromium; si hay uno preinstalado, se usa solo.
3. Se suben a `main` y Metricool las toma desde `https://raw.githubusercontent.com/cromacmms-lgtm/croma-media/<sha-del-commit>/media/<slug>/NN.jpg` (con el SHA del commit, no `main`, para que nunca tome una versión vieja en caché). Si se corrige una pieza ya programada, hay que actualizar la publicación en Metricool: guarda su propia copia al programar. Metricool cambia el id de una publicación cada vez que se actualiza; el uuid se mantiene.
4. Se programan en Metricool (marca `cromacmms`, id 7520428, zona `America/Buenos_Aires`) con publicación automática. `calendario.json` registra qué está programado.

## Ritmo

- Una publicación cada 4 días, a las 10:05 (pico de audiencia según Metricool).
- Una historia cada 2 días, a las 18:05.
- La historia del día de una publicación la anuncia ("Nuevo post").

## Reglas de contenido

- **Público:** pymes industriales de Córdoba (agroindustria, alimentos, metalmecánica), hoteles y complejos de las sierras, constructoras y agro. Al dueño, al jefe de mantenimiento y al técnico.
- **Tono:** profesional pero cercano, técnico sin ser frío, con orgullo de piso de planta. Español rioplatense con voseo ("guardalo", "escribinos").
- **Nomenclatura correcta:** "detención", "falla", "fuera de servicio", "detención no planificada". Nunca "se para" ni "paró". "Equipo" en lugar de "máquina" cuando se habla en general.
- **No mostrar el producto por dentro:** nada de pantallas, funciones, flujos ni KPIs del software. El contenido es educativo (tips, indicadores, checklists, costos) y de marca. El producto se muestra en la demo.
- **Sin datos inventados:** si un número es un ejemplo, se dice "ejemplo ilustrativo". Coma decimal y punto de miles.
- **Llamada a la acción:** DM a @cromacmms o cromacmms@gmail.com.
- Sin emojis decorativos ni signos de exclamación dobles.

## Pilares de contenido

1. **Qué mejora en una empresa con un software de mantenimiento** (sin mostrar el producto): comparaciones sin sistema / con software en organización, planificación, trazabilidad, comunicación, seguridad, vida útil de los equipos y decisiones. El foco es la mejora de la empresa, no "cuánto se gana". Inspirarse en cómo comunican los mejores CMMS del mundo (MaintainX, UpKeep, Limble, Fracttal): datos concretos con fuente, comparaciones claras, tono directo.
2. **Tips técnicos útiles** por rubro y temporada.
3. **Marca:** quiénes somos, del piso de planta, frases propias. Sin fotos de personas: solo la marca.

Datos externos solo con fuente citada en la slide y en el texto (por ejemplo, Siemens, *The True Cost of Downtime 2024*: las 500 empresas más grandes pierden el equivalente al 11 % de sus ingresos por detenciones no planificadas; 27 h por planta grande por mes).

**No repetir:** el enfoque "tu mantenimiento sigue en papel" y las "5 señales" ya se usaron; no volver a ese ángulo.

## Plantillas (`engine/croma.py`)

- `cover`, `brand`: portadas (fondos `claro`, `suave`, `violeta`, `noche`; decorado `ring` o `icon`).
- `text`: título, párrafos y una caja destacada opcional.
- `items`: de 1 a 4 ítems con número, ícono, título y texto.
- `formula`: indicador = numerador / denominador.
- `example`: dos resultados con su cálculo.
- `compare`: dos columnas.
- `cta`: cierre con contacto.
- Historias: `statement` y `question` (con opciones A–D y "Respondé por DM").

`**texto**` pinta una palabra con el color de acento. Los íconos disponibles están en `ICONS`.

## Temas por rubro y temporada (para las próximas tandas)

- Hotelería: preparación de temporada (oct–dic), cierre de temporada (mar–abr).
- Agro: cosecha fina (nov–dic) y gruesa (mar–jun); siembra.
- Industria: indicadores (MTTR, MTBF, disponibilidad, OEE), lubricación, aire comprimido, calderas, auditorías y registros.
- Construcción: equipos en obra, mantenimiento por horas de uso, vehículos.
- Marca: quiénes somos, del piso de planta, frases.
