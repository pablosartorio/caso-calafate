"""EL CASO VIEDMA — un hito de pago cobrado con datos truchos en la Estación de Radar Costero.

⚠️ SPOILER: leer los datos de este archivo revela al culpable.
Jugá una partida antes. :)
"""

from caso_calafate.caso import Caso, Secreto, Sospechoso

CASO_VIEDMA = Caso(
    id="viedma",
    titulo="EL CASO VIEDMA",
    gancho=(
        "Un hito de pago se cobró con un número que el radar nunca alcanzó "
        "— y alguien lo escondió mal."
    ),
    # Los párrafos van en una sola línea lógica (concatenación implícita de
    # strings): rich los envuelve al ancho de la terminal. Los saltos duros
    # quedan solo donde son intencionales (la lista de viñetas).
    briefing=(
        "Viedma, martes a media mañana. Te llama Auditoría Interna.\n\n"
        "«Detective, tenemos un problema con el radar. No es un choque ni un "
        "cortocircuito — esto es peor.»\n\n"
        "Hace tres semanas, el equipo de proyecto de la Estación de Radar Costero "
        "Viedma —contrato con el Estado provincial para vigilancia marítima y "
        "meteorológica— presentó el Informe de Aceptación en Sitio del Hito 3, "
        "certificando que el radar alcanzaba 60 km de alcance de detección sobre "
        "el blanco de referencia, tal como exige la especificación técnica del "
        "contrato. Con ese informe aprobado, el cliente liberó un pago "
        "equivalente al 40% del contrato restante.\n\n"
        "Un control cruzado de rutina, comparando el informe final contra los "
        "registros crudos del propio radar guardados en el servidor, encontró "
        "que el alcance medido esa noche fue de 54,3 km —seis kilómetros por "
        "debajo de la especificación— y que la tabla de resultados del informe "
        "fue editada después de terminada la medición.\n\n"
        "Lo que se sabe hasta ahora:\n\n"
        " • El ensayo de aceptación se corrió la noche del jueves 25/6,\n"
        "   entre las 22:00 y la 01:00.\n"
        " • Los logs crudos del radar (no editables desde la consola operativa) registran\n"
        "   un alcance máximo de 54,3 km esa noche.\n"
        " • El informe final entregado al cliente reporta 60,8 km, y los metadatos del\n"
        "   archivo PDF muestran que fue guardado por última vez a las 03:40 de esa\n"
        "   madrugada, tres horas después de terminado el ensayo.\n"
        " • Tres personas del equipo de proyecto tuvieron acceso al informe y a los\n"
        "   datos crudos esa noche. Son tus sospechosos.\n\n"
        "Interrogá, anotá, y cuando estés seguro: acusá. Tenés una sola oportunidad."
    ),
    contexto_actores="""\
La noche del jueves 25 de junio se corrió el ensayo de aceptación en sitio del
Hito 3 del contrato de la Estación de Radar Costero Viedma, entre las 22:00 y
la 01:00. Los registros crudos del radar marcan un alcance máximo de 54,3 km
sobre el blanco de referencia, por debajo del mínimo contractual de 60 km. El
informe final entregado al cliente, sin embargo, certifica 60,8 km de
alcance, y sus metadatos muestran que el archivo fue guardado por última vez
a las 03:40 de esa madrugada. Con ese informe aprobado, el cliente liberó un
pago equivalente al 40% del contrato restante. Un detective está
interrogando a las tres personas del equipo de proyecto que tuvieron acceso
al informe y a los datos crudos esa noche.""",
    epilogo=(
        "Nora Bulacio alteró el informe de aceptación.\n\n"
        "Dos semanas antes del ensayo, Dirección le había avisado que su área "
        "—Administración de Contratos y Proyecto— iba a sufrir un recorte del 30% "
        "en el presupuesto del año próximo si el Hito 3 no se certificaba a "
        "tiempo: sin ese pago, la empresa prefería tercerizar la gestión "
        "administrativa antes que sostener un equipo completo esperando papeles. "
        "Para Nora, que había armado ese equipo a pulso durante años, la amenaza "
        "era personal.\n\n"
        "La noche del ensayo, cuando Tomás le mandó el informe preliminar con el "
        "número real —54,3 km, por debajo de la especificación— Nora no avisó a "
        "nadie. Se quedó sola en la oficina, abrió el archivo con su usuario (el "
        "único con permisos de edición sobre la versión final antes del envío al "
        "cliente) y cambió la tabla de resultados: 54,3 pasó a ser 60,8. Guardó "
        "el archivo a las 03:40 y lo subió al portal del cliente esa misma "
        "mañana, convencida de que iba a poder ajustar el radar de verdad —una "
        "actualización de firmware, una recalibración de antena— antes de que a "
        "alguien se le ocurriera pedir los logs crudos.\n\n"
        "Se olvidó de un detalle: el gráfico de la página 12 del informe, el que "
        "muestra la curva de detección en función de la distancia, no lo dibujó "
        "ella a mano. Es una exportación automática del mismo software que "
        "genera los logs crudos, pegada como imagen. La tabla decía 60,8 km. El "
        "gráfico, técnicamente inalterado, seguía mostrando la curva cortada en "
        "54 km. Nadie lo notó durante tres semanas —hasta que Auditoría, "
        "buscando otra cosa, puso los dos números uno al lado del otro."
    ),
    max_preguntas=15,
    sospechosos=[
        Sospechoso(
            id="tomas",
            nombre="Tomás Aguirre",
            cargo="ingeniero de RF, responsable del ensayo",
            color="bright_cyan",
            personalidad=(
                "Obsesivo con el detalle, callado, más cómodo con un osciloscopio que "
                "con un jefe. Habla en jerga técnica incluso cuando no hace falta. Se "
                "pone tenso si sienten que dudan de la calidad de su medición."
            ),
            coartada=(
                "Dice que corrió el ensayo, armó el informe preliminar y se retiró "
                "poco después de mandarlo, sin quedarse a controlar el envío final."
            ),
            actitud=(
                "Colaborativo con los datos técnicos, tajante cuando se trata de números. "
                "Si le preguntan por su horario esa noche se pone incómodo, como si "
                "irse temprano fuera una falta, antes de admitirlo."
            ),
            secretos=[
                Secreto(
                    id="dato_real_54km",
                    pista=(
                        "El ensayo real del jueves dio un alcance máximo de 54,3 km, "
                        "no los 60,8 km que figuran en el informe final."
                    ),
                    instruccion_actor=(
                        "Solo si te preguntan directamente por el resultado real del "
                        "ensayo o por los datos crudos: confirmás, con seguridad "
                        "técnica, que el alcance medido esa noche fue 54,3 km, bien "
                        "por debajo del mínimo contractual de 60 km. Sos categórico: "
                        "los logs no mienten."
                    ),
                    criterio_revelacion=(
                        "Confirma que el resultado real del ensayo fue 54,3 km (o un "
                        "número claramente por debajo de 60 km), no lo que figura en "
                        "el informe final entregado al cliente."
                    ),
                ),
                Secreto(
                    id="aviso_a_nora",
                    pista=(
                        "Tomás le avisó por escrito a Nora Bulacio, esa misma noche, "
                        "que el número no alcanzaba la especificación, antes de irse."
                    ),
                    instruccion_actor=(
                        "Si te preguntan qué hiciste con el resultado, a quién se lo "
                        "reportaste, o qué pasó después del ensayo: contás que le "
                        "mandaste el informe preliminar con el número real a Nora por "
                        "mail interno cerca de la 01:30, y que te fuiste confiando en "
                        "que ella iba a escalar el problema. No acusás a nadie, solo "
                        "contás el hecho."
                    ),
                    criterio_revelacion=(
                        "Cuenta que le reportó el resultado real del ensayo a Nora "
                        "Bulacio esa misma noche, antes de retirarse."
                    ),
                ),
                Secreto(
                    id="salida_temprana",
                    pista=(
                        "Tomás no se quedó controlando el envío del informe: se fue "
                        "del predio a la 01:40, apenas mandó el archivo preliminar, "
                        "para llegar a un cumpleaños."
                    ),
                    instruccion_actor=(
                        "Si te preguntan qué hiciste después de mandar el informe, o "
                        "si te quedaste hasta tarde esa noche: al principio decís "
                        "vagamente que 'te quedaste un rato más', pero si insisten "
                        "admitís, con algo de vergüenza porque suena poco profesional, "
                        "que te fuiste a la 01:40 a un cumpleaños de un amigo y que no "
                        "volviste a mirar el informe hasta el lunes."
                    ),
                    criterio_revelacion=(
                        "Admite que se retiró del predio poco después de enviar el "
                        "informe preliminar (cerca de la 01:40) y no volvió a "
                        "revisarlo esa noche."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="nora",
            nombre="Nora Bulacio",
            cargo="jefa de Administración de Contratos y Proyecto",
            color="bright_magenta",
            es_culpable=True,
            personalidad=(
                "Controlada, persuasiva, siempre en modo gestión de equipo. Habla en "
                "términos de procesos y de 'proteger a su gente'. Nunca levanta la "
                "voz, pero nunca cede terreno tampoco."
            ),
            coartada=(
                "Dice que se quedó cerrando la documentación administrativa hasta "
                "eso de las 02:00 y se fue derecho a su casa; nadie puede confirmar "
                "la hora exacta porque se fue sola."
            ),
            actitud=(
                "Colaborativa y hasta cálida al principio, se victimiza defendiendo a "
                "su equipo. Si le muestran los metadatos del archivo o le preguntan "
                "por los permisos de edición, se enfría y desvía la conversación "
                "hacia Tomás o hacia 'problemas del software'. Jamás confiesa."
            ),
            secretos=[
                Secreto(
                    id="recorte_presupuesto",
                    pista=(
                        "Dos semanas antes del ensayo, Dirección le había advertido a "
                        "Nora que su área iba a sufrir un recorte del 30% si el "
                        "Hito 3 no se certificaba a tiempo."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por la situación de tu área, el presupuesto, "
                        "o si sentís presión por los tiempos del contrato: contás, con "
                        "cierta amargura contenida, que Dirección amenazó con recortar "
                        "un 30% de tu equipo de Administración de Contratos si el "
                        "Hito 3 no se cobraba a tiempo. Lo presentás como una "
                        "injusticia hacia tu gente, nunca como excusa para nada."
                    ),
                    criterio_revelacion=(
                        "Revela que su área enfrentaba un recorte presupuestario o de "
                        "personal si el pago del Hito 3 no se certificaba a tiempo."
                    ),
                ),
                Secreto(
                    id="edicion_0340",
                    pista=(
                        "El informe final fue guardado por última vez a las 03:40 con "
                        "el usuario de Nora, tres horas después de terminado el "
                        "ensayo."
                    ),
                    instruccion_actor=(
                        "Si te confrontan directamente con los metadatos del archivo "
                        "(que se guardó a las 03:40 con tu usuario): primero intentás "
                        "minimizarlo, decís que 'debe haber sido un ajuste de formato "
                        "menor, un typo'. Si insisten en qué cambiaste, te volvés vaga "
                        "y repetís que no te acordás el detalle, pero JAMÁS decís "
                        "explícitamente que cambiaste el número del alcance."
                    ),
                    criterio_revelacion=(
                        "Admite, aunque sea minimizándolo como 'un ajuste menor', que "
                        "ella guardó o modificó el archivo del informe a esa hora de "
                        "la madrugada."
                    ),
                ),
                Secreto(
                    id="acceso_exclusivo",
                    pista=(
                        "Solo Nora tiene permisos para editar la versión final del "
                        "informe antes de subirla al portal del cliente; ni Tomás ni "
                        "Marcelo pueden tocar esa versión."
                    ),
                    instruccion_actor=(
                        "Si te preguntan quién tiene permisos de edición sobre el "
                        "informe final, o quién más pudo haber cambiado el archivo: "
                        "explicás, con tono profesional, que por procedimiento solo el "
                        "área de Administración de Contratos —es decir, vos— tiene "
                        "permisos de edición sobre la versión final antes de subirla "
                        "al portal del cliente. Lo decís como un dato de proceso, no "
                        "como una confesión."
                    ),
                    criterio_revelacion=(
                        "Confirma que ella es la única con permisos de edición sobre "
                        "la versión final del informe antes del envío al cliente."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="marcelo",
            nombre="Marcelo Andrada",
            cargo="gerente de proyecto",
            color="bright_yellow",
            personalidad=(
                "Campechano, cansado, con demasiados proyectos encima. Tiende a "
                "delegar y confiar en su gente más de lo que debería. Se pone culposo "
                "cuando siente que falló como responsable último de algo."
            ),
            coartada=(
                "Dice que esa noche no estaba en la base: se fue a las 18:00 y firmó "
                "el informe recién el viernes a la mañana, por mail, desde su casa."
            ),
            actitud=(
                "Colaborativo y algo nervioso. Si lo presionan sobre cómo revisó el "
                "informe antes de firmarlo, se pone incómodo y termina admitiendo que "
                "confió demasiado en lo que le mandó Nora."
            ),
            secretos=[
                Secreto(
                    id="firma_sin_revisar",
                    pista=(
                        "Marcelo firmó el informe de aceptación sin comparar la tabla "
                        "de resultados contra los logs crudos del ensayo: confió en "
                        "el resumen que le mandó Nora."
                    ),
                    instruccion_actor=(
                        "Si te preguntan cómo revisaste el informe antes de firmarlo, "
                        "o si lo cruzaste con los datos crudos del radar: admitís, "
                        "incómodo, que no llegaste a cruzar la tabla final con los "
                        "logs crudos —confiaste en el resumen que te mandó Nora esa "
                        "madrugada— porque tenías otros tres proyectos encima esa "
                        "semana."
                    ),
                    criterio_revelacion=(
                        "Admite que firmó o aprobó el informe sin verificar "
                        "personalmente los datos crudos, confiando en el resumen de "
                        "Nora."
                    ),
                ),
                Secreto(
                    id="senial_de_alarma",
                    pista=(
                        "Unos días después de firmar, a Marcelo le llamó la atención "
                        "que el gráfico de la página 12 no coincidiera del todo con "
                        "la tabla de resultados, pero no le dio importancia."
                    ),
                    instruccion_actor=(
                        "Solo si te preguntan si notaste algo raro en el informe "
                        "después de firmarlo, o si volviste a mirarlo: contás, con "
                        "algo de culpa, que unos días después te pareció que el "
                        "gráfico de la página 12 no cerraba del todo con el número de "
                        "la tabla, pero lo atribuiste a un problema de escala del eje "
                        "y no volviste a mirarlo. No lo mencionás espontáneamente."
                    ),
                    criterio_revelacion=(
                        "Cuenta que notó una inconsistencia entre el gráfico y la "
                        "tabla del informe después de firmarlo, pero no la investigó."
                    ),
                ),
                Secreto(
                    id="salida_temprana_hija",
                    pista=(
                        "Marcelo le dijo a su equipo que se quedaba hasta tarde esa "
                        "noche, pero en realidad se fue a las 18:00 a buscar a su "
                        "hija y no volvió a la base."
                    ),
                    instruccion_actor=(
                        "Si te preguntan si estuviste en la base esa noche, o "
                        "remarcan que dijiste que 'te quedabas hasta tarde': admitís, "
                        "un poco avergonzado de haber quedado mal, que en realidad te "
                        "fuiste a las 18:00 a buscar a tu hija a un acto escolar y no "
                        "volviste; le dijiste a tu equipo que 'te quedabas' para no "
                        "dar explicaciones personales."
                    ),
                    criterio_revelacion=(
                        "Admite que se retiró de la base a las 18:00 esa tarde y no "
                        "volvió, contradiciendo lo que había dicho inicialmente."
                    ),
                ),
            ],
        ),
    ],
)
