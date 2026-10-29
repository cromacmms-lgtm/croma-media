"""Reels programados del 5/11 al 17/12 (martes y jueves a las 10:05).
Ritmo: unos 4 segundos por bloque de texto. Nomenclatura correcta: falla, avería, síntoma, fuga, fuera de servicio."""

CTA = 'Escribinos por DM o a soporte@cromacmms.com'

REELS = [
# ------------------------------------------------------------------ jue 5/11
dict(slug='2026-11-05-adivinanza-compresor', fecha='2026-11-05T10:05:00', seed=1, portada=6.5,
  titulo_reel='¿Qué falla es? Compresor de tornillo',
  eti='Adivinanza de mantenimiento', titulo=['¿Qué falla es?', 'Compresor de tornillo'], titulo_px=80,
  nota='Caso ilustrativo',
  escenas=[
    dict(tipo='adivinanza', dur=11,
      equipo=dict(icon='compresor', code='COMP-01', name='Compresor de tornillo'),
      sintomas=[('termometro', 'La temperatura de descarga sube día a día'),
                ('check', 'El nivel de aceite está bien'),
                ('alerta', 'El enfriador está cubierto de polvo')],
      opciones=['Falta de aceite', 'Enfriador obstruido', 'Válvula de admisión trabada'], correcta=1,
      explica='El polvo no deja disipar el calor. Si sigue así, el compresor **se detiene por alta temperatura.**'),
    dict(tipo='texto', dur=5, eti='Cómo se previene', titulo=['Limpieza del enfriador', 'con frecuencia fija.'], px=72,
      icon='calendario', lines=['Una tarea corta de preventivo,', '**con su frecuencia en CROMA.**'],
      sub='Por ejemplo, cada 30 días, o antes si el ambiente tiene mucho polvo.'),
  ],
  cierre=dict(texto='¿La adivinaste?\n**Contalo en los comentarios.**'),
  caption=('¿Qué falla es?\n\nCompresor de tornillo: la temperatura de descarga sube día a día, el nivel de aceite está bien '
           'y el enfriador está cubierto de polvo.\n\nRespuesta: enfriador obstruido. El polvo no deja disipar el calor y, si sigue '
           'así, el compresor se detiene por alta temperatura.\n\nSe previene con una limpieza del enfriador con frecuencia fija, '
           'más seguida si el ambiente tiene mucho polvo.\n\n¿La adivinaste? Contalo en los comentarios.\n\nCaso ilustrativo.\n\n'
           '#airecomprimido #compresores #mantenimientoindustrial #mantenimientopreventivo #CMMS #Córdoba')),
# ------------------------------------------------------------------ mar 10/11
dict(slug='2026-11-10-tres-cosas', fecha='2026-11-10T10:05:00', seed=2, portada=7.5,
  titulo_reel='¿Tu software de mantenimiento hace estas 3 cosas?',
  eti='Software de mantenimiento', titulo=['¿El tuyo hace', 'estas 3 cosas?'],
  nota='Interfaz ilustrativa · datos de ejemplo',
  escenas=[
    dict(tipo='checklist', dur=12, items=[
      ('qr', 'Código QR en cada equipo', 'Lo escaneás y ves su historial y sus órdenes de trabajo.'),
      ('camara', 'Falla reportada con foto', 'Desde el celular, en el momento y en el lugar.'),
      ('campana', 'Avisos automáticos', 'El preventivo avisa antes de vencer.')]),
    dict(tipo='telefono', dur=12, eti='En CROMA', titulo=['Así funciona', 'en la planta.'], pantallas=[
      dict(eti='COMP-01', titulo='Escaneás el equipo', filas=[dict(tipo='qr'),
           dict(titulo='Compresor de tornillo', sub='Sala de máquinas', chip='En servicio', chipc='ok', icon='compresor')]),
      dict(eti='NUEVO AVISO', titulo='Reportás la falla con foto', filas=[dict(tipo='foto', icon='gota'),
           dict(titulo='Pérdida de aceite', sub='COMP-01 · hace un momento', chip='Nuevo', chipc='warn', icon='alerta')]),
      dict(eti='AVISOS', titulo='Y nada queda en el olvido', filas=[
           dict(tipo='aviso', texto='El preventivo de COMP-01 vence mañana', icon='reloj', c='#f0b240'),
           dict(tipo='aviso', texto='Nuevo aviso de falla en COMP-01', icon='alerta', c='#f07070'),
           dict(tipo='aviso', texto='OT-0421 finalizada · COMP-01 en servicio', icon='check', c='#4fc795')]),
    ]),
  ],
  cierre=dict(texto='¿Cuántas tiene\n**el tuyo?**'),
  caption=('¿Tu software de mantenimiento hace estas 3 cosas?\n\n1. Código QR en cada equipo: lo escaneás y ves su historial y sus '
           'órdenes de trabajo.\n2. Falla reportada con foto, desde el celular, en el momento y en el lugar.\n3. Avisos automáticos: '
           'el preventivo avisa antes de vencer.\n\nEn CROMA las tres vienen de base.\n\n¿Cuántas tiene el tuyo? Contanos en los '
           'comentarios.\n\nInterfaz ilustrativa, datos de ejemplo.\n\n#mantenimiento #CMMS #softwaredemantenimiento '
           '#mantenimientoindustrial #industria #Córdoba')),
# ------------------------------------------------------------------ jue 12/11
dict(slug='2026-11-12-parada-de-planta', fecha='2026-11-12T10:05:00', seed=3, portada=6,
  titulo_reel='La parada de planta de enero se planifica en noviembre',
  eti='Parada de planta', titulo=['La de enero se', 'planifica en noviembre.'], titulo_px=72,
  escenas=[
    dict(tipo='linea', dur=15, etapas=[
      ('checklist', 'Noviembre', 'Lista de pendientes, priorizada por criticidad'),
      ('caja', 'Diciembre', 'Repuestos comprados y contratistas confirmados'),
      ('alerta', 'Enero · parada', 'Bloqueo y etiquetado, un responsable por trabajo'),
      ('check', 'Arranque', 'Pruebas, registro de lo hecho y plan actualizado')]),
    dict(tipo='texto', dur=5, eti='Con CROMA', titulo=['Cada trabajo,', 'con responsable y fecha.'], px=72,
      icon='calendario', lines=['Cargá cada trabajo de la parada', '**con su responsable y su fecha.**'],
      sub='Al terminar, queda el historial de lo que se hizo.'),
  ],
  cierre=dict(texto='La parada sale bien\nantes de empezar.\n**Planificala hoy.**'),
  caption=('La parada de planta de enero se planifica en noviembre.\n\nNoviembre: lista de pendientes, priorizada por criticidad.\n'
           'Diciembre: repuestos comprados y contratistas confirmados.\nEnero: bloqueo y etiquetado en cada equipo, un responsable por '
           'trabajo.\nArranque: pruebas, registro de lo que se hizo y plan de mantenimiento actualizado.\n\nSi la lista se arma en '
           'diciembre, faltan repuestos, contratistas y tiempo.\n\nGuardalo y compartilo con quien coordina la parada.\n\n'
           f'¿Querés ordenarla con tiempo? {CTA}\n\n#paradadeplanta #mantenimientoindustrial #planificación #seguridadindustrial #CMMS #Córdoba')),
# ------------------------------------------------------------------ mar 17/11
dict(slug='2026-11-17-motor-electrico', fecha='2026-11-17T10:05:00', seed=4, portada=6,
  titulo_reel='Motor eléctrico: por dónde puede fallar',
  eti='Motor eléctrico', titulo=['Por dónde puede', 'fallar.'],
  nota='Ilustración y frecuencias de ejemplo',
  escenas=[
    dict(tipo='equipo', dur=20.3, svg='motor', pasos=[
      dict(texto='Un motor trifásico funcionando.\nCada parte tiene su forma de fallar.'),
      dict(resaltar=['hl_rod'], vibra=True, panel=dict(comp='Rodamientos', falla='Desgaste o falta de lubricación',
           sintoma='Vibración y temperatura por encima de lo normal', detecta='Análisis de vibraciones y termografía')),
      dict(resaltar=['hl_bob'], panel=dict(comp='Bobinado', falla='Pérdida de aislación',
           sintoma='Recalentamiento y disparo de protecciones', detecta='Medición de resistencia de aislación')),
      dict(resaltar=['hl_vent'], panel=dict(comp='Ventilación', falla='Tapa del ventilador y aletas obstruidas',
           sintoma='Temperatura de carcasa elevada', detecta='Limpieza e inspección visual en la ronda')),
      dict(resaltar=['hl_bor'], panel=dict(comp='Caja de bornes', falla='Conexiones flojas',
           sintoma='Punto caliente en los bornes', detecta='Termografía')),
    ]),
    dict(tipo='frecuencias', dur=5.5, eti='Inspecciones predictivas', titulo=['Cada una con', 'su frecuencia.'],
      encabezado='Programadas en **CROMA**', filas=[('grafico', 'Análisis de vibraciones', 'Cada 30 días'),
        ('termometro', 'Termografía', 'Cada 90 días'), ('rayo', 'Resistencia de aislación', 'Cada 6 meses'),
        ('checklist', 'Ronda de limpieza', 'Semanal')],
      pie='Las frecuencias se definen según la criticidad del motor.'),
  ],
  cierre=dict(texto='Tu motor avisa\nantes de fallar.\n**Medilo a tiempo.**'),
  caption=('Motor eléctrico: por dónde puede fallar.\n\nRodamientos: desgaste o falta de lubricación. Síntoma: vibración y temperatura '
           'por encima de lo normal. Se detecta con análisis de vibraciones y termografía.\n\nBobinado: pérdida de aislación. Síntoma: '
           'recalentamiento y disparo de protecciones. Se detecta midiendo la resistencia de aislación.\n\nVentilación: tapa del '
           'ventilador y aletas obstruidas. Síntoma: temperatura de carcasa elevada. Se previene con limpieza en la ronda.\n\nCaja de '
           'bornes: conexiones flojas. Síntoma: punto caliente. Se detecta con termografía.\n\nCada inspección con su frecuencia, '
           'según la criticidad del motor, programada en CROMA.\n\nIlustración y frecuencias de ejemplo.\n\n'
           '#motoreseléctricos #mantenimientopredictivo #termografía #mantenimientoindustrial #CMMS #Córdoba')),
# ------------------------------------------------------------------ jue 19/11
dict(slug='2026-11-19-mito-grasa', fecha='2026-11-19T10:05:00', seed=5, portada=5,
  titulo_reel='Mito o realidad: más grasa es mejor',
  eti='Mito o realidad', titulo=['Lubricación de', 'rodamientos'],
  escenas=[
    dict(tipo='mito', dur=14, frase='Al rodamiento, cuanta más grasa, mejor.', veredicto='mito', puntos=[
      ('termometro', 'El exceso de grasa aumenta la fricción y la **temperatura del rodamiento.**'),
      ('alerta', 'Puede dañar el **sello** y, en un motor, llegar al **bobinado.**'),
      ('reloj', 'La **cantidad y la frecuencia** de relubricación las define el fabricante para cada rodamiento.')]),
    dict(tipo='texto', dur=5, eti='La lubricación', titulo=['también se', 'planifica.'], icon='gota',
      lines=['Cada punto de engrase con', '**su cantidad y su frecuencia,**', 'programado en CROMA.']),
  ],
  cierre=dict(texto='Ni de más ni de menos.\n**Lo que indica el fabricante.**'),
  caption=('Mito o realidad: al rodamiento, cuanta más grasa, mejor.\n\nMito. El exceso de grasa aumenta la fricción y la temperatura '
           'del rodamiento, puede dañar el sello y, en un motor eléctrico, llegar al bobinado.\n\nLa cantidad y la frecuencia de '
           'relubricación las define el fabricante para cada rodamiento, según su tamaño, velocidad y condiciones de trabajo.\n\n'
           'Cada punto de engrase con su cantidad y su frecuencia, programado en CROMA.\n\nGuardalo para la próxima ronda de '
           'lubricación.\n\n#lubricación #rodamientos #mantenimientoindustrial #confiabilidad #CMMS #Córdoba')),
# ------------------------------------------------------------------ mar 24/11
dict(slug='2026-11-24-tres-estrategias', fecha='2026-11-24T10:05:00', seed=6, portada=12,
  titulo_reel='Correctivo, preventivo y predictivo en el mismo equipo',
  eti='Mismo equipo, tres estrategias', titulo=['Correctivo, preventivo', 'y predictivo.'], titulo_px=70,
  escenas=[
    dict(tipo='texto', dur=4.5, icon='reductor', lines=['Un motorreductor de', '**una cinta transportadora.**'],
      sub='Su rodamiento empieza a desgastarse.'),
    dict(tipo='filas', dur=14, filas=[
      dict(nombre='Correctivo', color='red', cuando='Cuando falla', texto='La cinta se detiene en plena producción y el repuesto se compra de urgencia.'),
      dict(nombre='Preventivo', color='amber', cuando='Cada X horas o días', texto='El rodamiento se cambia en fecha, aunque todavía le quede vida útil.'),
      dict(nombre='Predictivo', color='green', cuando='Según la condición', texto='La vibración avisa el desgaste y el cambio se planifica en la parada.', destacar=True)]),
    dict(tipo='texto', dur=5, eti='La clave', titulo=['Combinarlas según', 'la criticidad.'], px=76,
      icon='engranaje', lines=['Cada equipo con su estrategia,', '**y todas programadas en CROMA.**']),
  ],
  cierre=dict(texto='No hay una sola estrategia.\n**Hay un plan.**'),
  caption=('Correctivo, preventivo y predictivo en el mismo equipo: el motorreductor de una cinta transportadora.\n\nCorrectivo: '
           'se interviene cuando falla. La cinta se detiene en plena producción y el repuesto se compra de urgencia.\n\nPreventivo: '
           'el rodamiento se cambia en fecha, aunque todavía le quede vida útil.\n\nPredictivo: la vibración avisa el desgaste y el '
           'cambio se planifica en la parada.\n\nNo se trata de elegir una: cada equipo lleva la estrategia que corresponde según su '
           'criticidad, y todas se programan en CROMA.\n\n#mantenimientopredictivo #mantenimientopreventivo #confiabilidad '
           '#mantenimientoindustrial #CMMS #Córdoba')),
# ------------------------------------------------------------------ jue 26/11
dict(slug='2026-11-26-cosechadora', fecha='2026-11-26T10:05:00', seed=7, portada=9,
  titulo_reel='Cosecha fina: 4 controles a la cosechadora',
  eti='Agro · cosecha fina', titulo=['4 controles a', 'la cosechadora.'],
  escenas=[
    dict(tipo='checklist', dur=15, encabezado='Antes de entrar al lote:', items=[
      ('cuchilla', 'Plataforma de corte', 'Cuchillas, puntones y molinete en condiciones.'),
      ('correa', 'Correas y cadenas', 'Tensión, desgaste y alineación de poleas.'),
      ('termometro', 'Refrigeración y filtros', 'Radiador y tamiz limpios, filtro de aire al día.'),
      ('llama', 'Prevención de incendios', 'Motor y escape sin residuos, matafuegos cargados.')]),
    dict(tipo='texto', dur=5, eti='El consejo', titulo=['Registrá las', 'horas de motor.'], icon='reloj',
      lines=['Así sabés cuándo toca cada servicio,', '**aunque cambie el operador.**']),
  ],
  cierre=dict(texto='Revisala antes\n**de entrar al lote.**'),
  caption=('Cosecha fina: 4 controles a la cosechadora antes de entrar al lote.\n\n1. Plataforma de corte: cuchillas, puntones y '
           'molinete en condiciones.\n2. Correas y cadenas: tensión, desgaste y alineación de poleas.\n3. Refrigeración y filtros: '
           'radiador y tamiz limpios, filtro de aire al día.\n4. Prevención de incendios: motor y escape sin residuos, matafuegos '
           'cargados.\n\nY registrá las horas de motor: así sabés cuándo toca cada servicio, aunque cambie el operador.\n\nPasáselo a '
           'tu contratista o a quien maneja la máquina.\n\n#agro #cosechafina #maquinariaagrícola #mantenimiento #campo #Córdoba')),
# ------------------------------------------------------------------ mar 1/12
dict(slug='2026-12-01-recorrido-ot', fecha='2026-12-01T10:05:00', seed=8, portada=9.5,
  titulo_reel='Una orden de trabajo, del aviso al cierre',
  eti='Una orden de trabajo', titulo=['Del aviso', 'al cierre.'],
  nota='Interfaz ilustrativa · datos de ejemplo',
  escenas=[
    dict(tipo='telefono', dur=17, pantallas=[
      dict(eti='PASO 1 · AVISO', titulo='El operador escanea el equipo', filas=[dict(tipo='qr'),
           dict(titulo='BOM-03 · Bomba de agua', sub='Planta de tratamiento', chip='En servicio', chipc='ok', icon='bomba')]),
      dict(eti='PASO 2 · FALLA', titulo='Reporta la falla con foto', filas=[dict(tipo='foto', icon='gota'),
           dict(titulo='Fuga por el sello mecánico', sub='BOM-03 · hace un momento', chip='Nuevo', chipc='warn', icon='alerta')]),
      dict(eti='PASO 3 · ORDEN', titulo='El planner genera la orden de trabajo', filas=[
           dict(titulo='OT-0418 · Correctivo', sub='Prioridad alta · BOM-03', chip='Asignada', chipc='info', icon='checklist'),
           dict(titulo='Técnico asignado', sub='Turno mañana', icon='persona'),
           dict(tipo='aviso', texto='Te asignaron la OT-0418', icon='campana', c='#6f9cf0')]),
      dict(eti='PASO 4 · CIERRE', titulo='Se cierra y queda en el historial', filas=[
           dict(titulo='Cambio de sello mecánico', sub='2,5 h · turno mañana', chip='Finalizada', chipc='ok', icon='llave'),
           dict(titulo='Historial de BOM-03', sub='3 intervenciones este año', icon='grafico'),
           dict(titulo='BOM-03', sub='Bomba de agua', chip='En servicio', chipc='ok', icon='bomba')]),
    ]),
    dict(tipo='texto', dur=5, eti='Así funciona', titulo=['Nadie pregunta', 'qué pasó.'], icon='checklist',
      lines=['Cada paso queda registrado', '**en el equipo, con fecha y responsable.**']),
  ],
  cierre=dict(texto='Del aviso al cierre,\n**todo en un lugar.**'),
  caption=('Una orden de trabajo, del aviso al cierre.\n\n1. El operador escanea el código QR de la bomba.\n2. Reporta la falla con '
           'foto: fuga por el sello mecánico.\n3. El planner genera la orden de trabajo y la asigna al técnico del turno.\n4. Se cierra '
           'con lo que se hizo y queda en el historial del equipo.\n\nCada paso registrado, con fecha y responsable. Nadie tiene que '
           f'preguntar qué pasó.\n\n¿Querés verlo con tus equipos? {CTA}\n\nInterfaz ilustrativa, datos de ejemplo.\n\n'
           '#mantenimiento #CMMS #órdenesdetrabajo #mantenimientoindustrial #softwaredemantenimiento #Córdoba')),
# ------------------------------------------------------------------ jue 3/12
dict(slug='2026-12-03-adivinanza-reductor', fecha='2026-12-03T10:05:00', seed=9, portada=6.5,
  titulo_reel='¿Qué falla es? Reductor de velocidad',
  eti='Adivinanza de mantenimiento', titulo=['¿Qué falla es?', 'Reductor de velocidad'], titulo_px=78,
  nota='Caso ilustrativo',
  escenas=[
    dict(tipo='adivinanza', dur=11,
      equipo=dict(icon='reductor', code='RED-02', name='Reductor de la cinta 2'),
      sintomas=[('gota', 'Mancha de aceite debajo del eje de salida'),
                ('alerta', 'El nivel de aceite baja semana a semana'),
                ('termometro', 'Temperatura de carcasa normal')],
      opciones=['Retén del eje de salida desgastado', 'Engranajes desgastados', 'Exceso de carga'], correcta=0,
      explica='El retén ya no sella y el aceite se pierde por el eje. Con nivel bajo, **se dañan engranajes y rodamientos.**'),
    dict(tipo='texto', dur=5, eti='Cómo se detecta a tiempo', titulo=['Ronda visual y', 'control de nivel.'], px=78,
      icon='checklist', lines=['Una inspección corta con frecuencia fija,', '**programada en CROMA.**'],
      sub='Por ejemplo, control de nivel semanal.'),
  ],
  cierre=dict(texto='¿La adivinaste?\n**Contalo en los comentarios.**'),
  caption=('¿Qué falla es?\n\nReductor de velocidad: mancha de aceite debajo del eje de salida, el nivel baja semana a semana y la '
           'temperatura de carcasa es normal.\n\nRespuesta: retén del eje de salida desgastado. El retén ya no sella y el aceite se '
           'pierde por el eje. Si el nivel sigue bajando, se dañan engranajes y rodamientos.\n\nSe detecta a tiempo con ronda visual y '
           'control de nivel con frecuencia fija.\n\n¿La adivinaste? Contalo en los comentarios.\n\nCaso ilustrativo.\n\n'
           '#reductores #lubricación #mantenimientoindustrial #mantenimientopreventivo #CMMS #Córdoba')),
# ------------------------------------------------------------------ mar 8/12
dict(slug='2026-12-08-pileta-hotel', fecha='2026-12-08T10:05:00', seed=10, portada=9,
  titulo_reel='Temporada en las sierras: la pileta antes de enero',
  eti='Hoteles y complejos', titulo=['La pileta,', 'antes de enero.'],
  escenas=[
    dict(tipo='checklist', dur=15, encabezado='Antes de la temporada:', items=[
      ('bomba', 'Bomba de recirculación', 'Sin fuga por el sello, sin vibración ni temperatura anormal.'),
      ('filtro', 'Filtro', 'Retrolavado y estado del medio filtrante.'),
      ('gota', 'Tratamiento del agua', 'Equipo de cloración funcionando y calibrado.'),
      ('escudo', 'Seguridad', 'Rejillas de succión y tablero eléctrico en condiciones.')]),
    dict(tipo='texto', dur=5, eti='En plena temporada', titulo=['Un técnico tarda', 'más en llegar.'], px=78,
      icon='calendario', lines=['Por eso conviene dejar', '**el preventivo programado en CROMA**', 'antes de que llegue la gente.']),
  ],
  cierre=dict(texto='En enero,\nla pileta no espera.\n**Revisala hoy.**'),
  caption=('Temporada en las sierras: la pileta, antes de enero.\n\n1. Bomba de recirculación: sin fuga por el sello, sin vibración ni '
           'temperatura anormal.\n2. Filtro: retrolavado y estado del medio filtrante.\n3. Tratamiento del agua: equipo de cloración '
           'funcionando y calibrado.\n4. Seguridad: rejillas de succión y tablero eléctrico en condiciones.\n\nEn plena temporada, un '
           'técnico o un repuesto tardan más en llegar. Una pileta fuera de servicio en enero son reclamos.\n\nCompartilo con quien se '
           'encarga del mantenimiento del hotel o complejo.\n\n#hotelería #turismoCórdoba #cabañas #piletas #mantenimiento #temporada')),
# ------------------------------------------------------------------ jue 10/12
dict(slug='2026-12-10-mtbf-mttr', fecha='2026-12-10T10:05:00', seed=11, portada=7,
  titulo_reel='MTBF y MTTR con un ejemplo',
  eti='Indicadores', titulo=['MTBF y MTTR', 'con un ejemplo.'],
  nota='Ejemplo ilustrativo',
  escenas=[
    dict(tipo='formula', dur=9.5, nombre='MTBF', num='Horas de funcionamiento', den='Cantidad de fallas',
      lee='Cada cuánto falla un equipo. **Cuanto más alto, mejor.**',
      ejemplo=dict(texto='Un compresor trabajó 600 h en el mes y tuvo 3 fallas.', calc='600 h ÷ 3', valor=200, unidad='h')),
    dict(tipo='formula', dur=9.5, nombre='MTTR', num='Horas de reparación', den='Cantidad de reparaciones',
      lee='Cuánto tarda en volver a estar en servicio. **Cuanto más bajo, mejor.**',
      ejemplo=dict(texto='Las 3 reparaciones llevaron 2 h, 4 h y 3 h.', calc='9 h ÷ 3', valor=3, unidad='h')),
    dict(tipo='texto', dur=5, eti='La base', titulo=['Sin registros,', 'no hay indicadores.'], px=76, icon='grafico',
      lines=['Cada falla con su hora de inicio y fin,', '**y CROMA calcula MTBF y MTTR por equipo.**']),
  ],
  cierre=dict(texto='Lo que no se mide,\n**no se mejora.**'),
  caption=('MTBF y MTTR, con un ejemplo.\n\nMTBF (tiempo medio entre fallas): horas de funcionamiento ÷ cantidad de fallas. Un '
           'compresor que trabajó 600 h y tuvo 3 fallas tiene un MTBF de 200 h. Cuanto más alto, mejor.\n\nMTTR (tiempo medio de '
           'reparación): horas de reparación ÷ cantidad de reparaciones. Si las 3 reparaciones llevaron 2 h, 4 h y 3 h, el MTTR es de '
           '3 h. Cuanto más bajo, mejor.\n\nLa base de los dos: registrar cada falla con su hora de inicio y fin. Con eso, CROMA calcula MTBF y MTTR por equipo.\n\nEjemplo '
           'ilustrativo.\n\n#MTBF #MTTR #indicadores #confiabilidad #mantenimientoindustrial #CMMS')),
# ------------------------------------------------------------------ mar 15/12
dict(slug='2026-12-15-criticidad', fecha='2026-12-15T10:05:00', seed=12, portada=9,
  titulo_reel='¿Qué equipo atiendo primero? Análisis de criticidad',
  eti='Análisis de criticidad', titulo=['¿Qué equipo', 'atiendo primero?'],
  nota='Ejemplo ilustrativo',
  escenas=[
    dict(tipo='texto', dur=4.5, icon='alerta', lines=['Tres equipos fallan el mismo día.', '**¿Por cuál empezás?**']),
    dict(tipo='matriz', dur=11, equipos=[
      dict(nombre='Aire de oficina', icon='copo', f=1, c=0),
      dict(nombre='Bomba de agua', icon='bomba', f=1, c=1),
      dict(nombre='Compresor de aire', icon='compresor', f=2, c=2)],
      nota='Frecuencia de falla × consecuencia:\n**el compresor va primero.**'),
    dict(tipo='texto', dur=5, eti='La criticidad', titulo=['ordena las', 'prioridades.'], icon='escudo',
      lines=['En CROMA, cada equipo lleva', '**su criticidad A, B o C,**', 'y con eso se ordenan las prioridades.']),
  ],
  cierre=dict(texto='No todo es urgente.\n**Lo crítico, sí.**'),
  caption=('¿Qué equipo atiendo primero?\n\nEl análisis de criticidad cruza la frecuencia de falla con la consecuencia de la falla: '
           'producción, seguridad, calidad y costo.\n\nEn el ejemplo, el compresor de aire falla seguido y, si se detiene, frena toda la '
           'planta: va primero. La bomba de agua viene después. El aire acondicionado de la oficina puede esperar.\n\nLa criticidad '
           'ordena las prioridades y define la estrategia y la frecuencia de cada plan de mantenimiento. En CROMA, cada equipo lleva su criticidad A, B o C.\n\nEjemplo ilustrativo.\n\n'
           '#criticidad #confiabilidad #mantenimientoindustrial #gestióndeactivos #CMMS #Córdoba')),
# ------------------------------------------------------------------ jue 17/12
dict(slug='2026-12-17-vacaciones', fecha='2026-12-17T10:05:00', seed=13, portada=6,
  titulo_reel='Vacaciones de verano: el mantenimiento no se toma vacaciones',
  eti='Vacaciones de verano', titulo=['El mantenimiento', 'no se toma vacaciones.'], titulo_px=74,
  nota='Interfaz ilustrativa · datos de ejemplo',
  escenas=[
    dict(tipo='telefono', dur=13, pantallas=[
      dict(eti='ENERO', titulo='Preventivos programados', filas=[
           dict(titulo='COMP-01 · Cambio de filtros', sub='05/01 · turno mañana', chip='Programada', chipc='info', icon='compresor'),
           dict(titulo='CAL-01 · Inspección de caldera', sub='12/01', chip='Programada', chipc='info', icon='llama'),
           dict(titulo='BOM-03 · Análisis de vibraciones', sub='19/01', chip='Programada', chipc='info', icon='bomba')]),
      dict(eti='AVISOS', titulo='Nada queda en el olvido', filas=[
           dict(tipo='aviso', texto='El preventivo de COMP-01 vence mañana', icon='reloj', c='#f0b240'),
           dict(tipo='aviso', texto='OT-0503 asignada al turno mañana', icon='campana', c='#6f9cf0')]),
      dict(eti='A LA VUELTA', titulo='Todo registrado', filas=[
           dict(titulo='12 órdenes cerradas en enero', icon='checklist', chip='Finalizadas', chipc='ok'),
           dict(titulo='Historial de cada equipo', sub='Quién, qué y cuándo', icon='grafico')]),
    ]),
    dict(tipo='texto', dur=5, eti='Antes de irte', titulo=['Dejá enero', 'programado.'], icon='calendario',
      lines=['Con los preventivos cargados,', '**la planta sigue en orden aunque no estés.**']),
  ],
  cierre=dict(texto='Felices fiestas.\n**Nos vemos en 2027.**'),
  caption=('El mantenimiento no se toma vacaciones.\n\nAntes de irte, dejá enero programado: preventivos con fecha y responsable, '
           'avisos automáticos para que nada quede en el olvido y, a la vuelta, todo registrado en el historial de cada equipo.\n\n'
           'Gracias por acompañarnos este año. Felices fiestas, nos vemos en 2027.\n\nInterfaz ilustrativa, datos de ejemplo.\n\n'
           '#mantenimiento #CMMS #planificación #mantenimientopreventivo #industria #Córdoba')),
]
