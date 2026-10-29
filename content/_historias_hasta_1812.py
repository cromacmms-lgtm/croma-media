#!/usr/bin/env python3
"""Genera las especificaciones de las historias del 30/10 al 17/12: dos por día de reel
(18:05 anuncia el reel, 18:10 tip, pregunta o marca)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
DM = 'Respondé por DM'

def nuevo(t, sub, icon, theme='violeta'):
    return dict(theme=theme, icon=icon, eti='Nuevo reel', title=t, sub=sub)

def preg(t, opts, theme='noche'):
    return dict(theme=theme, kind='question', eti='Pregunta rápida', title=t, size=88, options=opts, cta=DM, ring=False)

def tip(eti, t, sub, icon=None, theme='suave'):
    d = dict(theme=theme, eti=eti, title=t, sub=sub)
    if icon:
        d['icon'] = icon
    return d

DIAS = [
 ('2026-10-30', 'bomba3',
  nuevo('Cuando el jefe pregunta **qué pasó con la bomba 3.**', '¿Te pasó? Está en el perfil.', 'mensaje'),
  preg('¿Dónde queda **el historial de tus equipos?**', ['En un sistema', 'En planillas', 'En el grupo de WhatsApp', 'En la memoria de alguien'])),
 ('2026-11-03', 'bomba-centrifuga',
  nuevo('Bomba centrífuga: **por dónde puede fallar.**', 'Rodamientos, sello mecánico e impulsor. En el perfil.', 'gota', 'noche'),
  tip('Tip de mantenimiento', 'Una fuga por el sello mecánico **no se corrige ajustando.**',
      'Indica desgaste o daño de las caras del sello: se reemplaza. Lo que se ajusta es la empaquetadura.', 'gota')),
 ('2026-11-05', 'adivinanza-compresor',
  nuevo('¿Qué falla es? **Compresor de tornillo.**', '¿La adivinás? Está en el perfil.', 'termometro'),
  preg('¿Cada cuánto limpiás **el enfriador del compresor?**', ['Cada mes', 'Cada 3 meses', 'Cuando levanta temperatura', 'Nunca lo vimos'])),
 ('2026-11-10', 'tarjeta-roja',
  nuevo('Una falla que no puede esperar **y una línea que no se detiene.**', 'Para eso está la tarjeta roja. En el perfil.', 'alerta', 'noche'),
  tip('En CROMA', 'La tarjeta roja **se carga desde el QR del equipo.**', 'Con foto, daño y causa. Después el planner la aprueba y la convierte en correctiva.', 'qr', 'claro')),
 ('2026-11-12', 'parada',
  nuevo('La parada de enero **se planifica en noviembre.**', 'Antes, durante y después. En el perfil.', 'calendario'),
  preg('¿Tu planta hace **parada en verano?**', ['Sí, en enero', 'Sí, en febrero', 'No hacemos parada', 'Depende del año'])),
 ('2026-11-17', 'motor-electrico',
  nuevo('Motor eléctrico: **por dónde puede fallar.**', 'Rodamientos, bobinado, ventilación y bornes. En el perfil.', 'rayo', 'noche'),
  tip('Tip de mantenimiento', 'Tapa del ventilador sucia, **motor más caliente.**',
      'Limpiar aletas y tapa en la ronda es de las tareas más simples y que más vida le dan al motor.', 'termometro')),
 ('2026-11-19', 'mito-grasa',
  nuevo('Mito o realidad: **más grasa es mejor.**', 'La respuesta, en el perfil.', 'gota'),
  preg('¿Quién define **cuánta grasa lleva cada rodamiento?**', ['El fabricante', 'El técnico, a ojo', 'El plan de lubricación', 'Nadie lo tiene definido'])),
 ('2026-11-24', 'tres-estrategias',
  nuevo('Correctivo, preventivo **y predictivo.**', 'El mismo equipo, tres resultados. En el perfil.', 'engranaje', 'noche'),
  tip('Del piso de planta', 'El mejor plan **combina las tres.**',
      'Predictivo en lo crítico, preventivo en lo importante y correctivo planificado en lo que puede esperar.', None, 'claro')),
 ('2026-11-26', 'cosechadora',
  nuevo('Cosecha fina: **4 controles a la cosechadora.**', 'Pasáselo a quien maneja la máquina. En el perfil.', 'tractor'),
  tip('Agro', 'Registrá las **horas de motor.**', 'Así sabés cuándo toca cada servicio, aunque cambie el operador.', 'reloj')),
 ('2026-12-01', 'cinco-porques',
  nuevo('Los 5 porqués **de una falla.**', 'Del sello que falla a la causa raíz. En el perfil.', 'lupa', 'noche'),
  preg('¿Cuántas veces cambiaste **el mismo repuesto este año?**', ['Una', 'Dos o tres', 'Más de tres', 'Perdí la cuenta'])),
 ('2026-12-03', 'adivinanza-reductor',
  nuevo('¿Qué falla es? **Reductor de velocidad.**', '¿La adivinás? Está en el perfil.', 'engranaje'),
  tip('Tip de mantenimiento', 'Un nivel de aceite que baja **es una falla avisando.**',
      'Mancha debajo del eje y nivel que baja: revisá el retén antes de que se dañen engranajes y rodamientos.', 'gota', 'claro')),
 ('2026-12-08', 'calor-verano',
  nuevo('4 equipos que **sufren el calor.**', 'Qué revisar antes del verano. En el perfil.', 'termometro', 'noche'),
  preg('¿Qué equipo **sufre más el calor en tu planta?**', ['Compresores', 'Motores eléctricos', 'Tableros eléctricos', 'Equipos de frío'])),
 ('2026-12-10', 'mtbf-mttr',
  nuevo('MTBF y MTTR **con un ejemplo.**', 'Dos números que te dicen si tu mantenimiento mejora. En el perfil.', 'grafico'),
  tip('La base', 'Sin registros, **no hay indicadores.**', 'Cada falla con su hora de inicio y de fin: con eso ya podés calcular los dos.', 'grafico')),
 ('2026-12-15', 'criticidad',
  nuevo('¿Qué equipo **atiendo primero?**', 'Análisis de criticidad, en el perfil.', 'alerta', 'noche'),
  preg('¿Tenés tus equipos **clasificados por criticidad?**', ['Sí, todos', 'Solo los principales', 'Todavía no', 'Queremos empezar'])),
 ('2026-12-17', 'vacaciones',
  nuevo('El mantenimiento **no se toma vacaciones.**', 'Dejá enero programado. En el perfil.', 'calendario'),
  dict(theme='noche', eti='Hablemos', title='En 2027, **tu mantenimiento en orden.**', sub='Te mostramos CROMA con tus equipos.', contacts=True)),
]

out = []
for fecha, tema, s1, s2 in DIAS:
    for hora, k, st in [('18:05', 'anuncio', s1), ('18:10', 'tip' if s2.get('kind') != 'question' else 'pregunta', s2)]:
        slug = f'{fecha}-historia-{tema}-{k}'
        spec = dict(slug=slug, format='story', date=f'{fecha}T{hora}:00', story=st)
        json.dump(spec, open(os.path.join(HERE, slug + '.json'), 'w'), ensure_ascii=False, indent=1)
        out.append(slug)
print(len(out))
