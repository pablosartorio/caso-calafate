"""EL CASO CHALTÉN III — datos de configuración alterados en el satélite CHALTÉN-III.

⚠️ SPOILER: leer los datos de este archivo revela al culpable.
Jugá una partida antes. :)
"""

from caso_calafate.caso import Caso, Secreto, Sospechoso

CASO_CHALTEN_III = Caso(
    id="chalten-iii",
    titulo="EL CASO CHALTÉN III",
    gancho=(
        "A cuatro días de un ensayo crítico, alguien maquilló los números para "
        "que el satélite pasara un examen que no debía pasar."
    ),
    # Los párrafos van en una sola línea lógica (concatenación implícita de
    # strings): rich los envuelve al ancho de la terminal. Los saltos duros
    # quedan solo donde son intencionales (la lista de viñetas).
    briefing=(
        "San Carlos de Bariloche, jueves, 20:15. Te suena el teléfono.\n\n"
        "«Detective, necesitamos que venga al Centro. Tenemos un problema con el "
        "CHALTÉN-III y no es un problema de fierros.»\n\n"
        "A cuatro días de arrancar el ensayo térmico de vacío del satélite de "
        "comunicaciones CHALTÉN-III — geoestacionario, la etapa de calificación "
        "más dura antes de integrarlo a la plataforma — control de configuración "
        "detectó algo que no debería estar ahí: los datos de configuración "
        "cargados en el software de vuelo de la carga útil de comunicaciones no "
        "coinciden con los que figuran como aprobados en el repositorio del "
        "proyecto.\n\n"
        "Si nadie lo llegaba a notar, el ensayo iba a arrancar el lunes con "
        "datos que no son los que el satélite va a llevar en órbita. Y "
        "CHALTÉN-III hubiera acreditado una etapa de calificación entera con un "
        "defecto adentro, sin que nadie se enterara.\n\n"
        "Lo que se sabe hasta ahora:\n\n"
        " • El repositorio registra un commit sin ticket de cambio asociado,\n"
        "   cargado el martes a las 23:40 desde una cuenta válida — no hubo\n"
        "   intrusión, alguien con acceso legítimo lo hizo.\n"
        " • El commit modifica seis parámetros de calibración de la tabla de\n"
        "   frecuencias que usa la carga útil de comunicaciones.\n"
        " • Solo tres personas tuvieron permisos de escritura sobre ese\n"
        "   repositorio esa semana: la jefa de integración de software, un\n"
        "   técnico de control de configuración, y el ingeniero de software\n"
        "   junior a cargo de esa parte del código.\n"
        " • Los tres estaban trabajando esa semana con acceso remoto habilitado\n"
        "   al banco de ensayos.\n\n"
        "Interrogá, anotá, y cuando estés seguro: acusá. Tenés una sola oportunidad."
    ),
    contexto_actores="""\
A cuatro días del ensayo térmico de vacío del satélite de comunicaciones
CHALTÉN-III, control de configuración detectó que los datos de configuración
cargados en el software de vuelo de la carga útil no coinciden con los
aprobados en el repositorio del proyecto: hay un commit del martes a las
23:40, sin ticket de cambio asociado, que modifica seis parámetros de
calibración de la tabla de frecuencias. Solo tres personas tuvieron acceso de
escritura al repositorio esa semana. Un detective está interrogando a las
tres.""",
    epilogo=(
        "Nahuel Bravo alteró la configuración del CHALTÉN-III.\n\n"
        "Meses atrás, durante el desarrollo del software de vuelo de la carga "
        "útil de comunicaciones, escribió la rutina que interpola la tabla de "
        "compensación térmica del sintetizador de frecuencia — el módulo que "
        "ajusta la ganancia según la temperatura de operación. Tiene un error: "
        "en los extremos del rango térmico, calcula mal la compensación. Nadie "
        "lo vio porque la revisión de ese módulo la firmó él mismo, apurado, "
        "sin pedir una segunda mirada.\n\n"
        "El error durmió tranquilo durante meses, hasta que el cronograma lo "
        "alcanzó: el ensayo térmico de vacío iba a llevar la carga útil "
        "exactamente a esos extremos de temperatura donde su rutina fallaba. "
        "Si el ensayo corría con los datos reales, el defecto iba a aparecer, "
        "documentado, delante de todo el comité de calificación — y con él, la "
        "pregunta de quién había escrito ese código y por qué nadie lo había "
        "atrapado antes.\n\n"
        "Nahuel entró en pánico. Es su primer proyecto grande desde que se "
        "recibió; le aterraba decepcionar a Rocío, quien tres semanas antes ya "
        "lo había sancionado por otro error menor, y todavía más le aterraba "
        "que lo apartaran del equipo. No pensó en sabotear nada ni en dañar el "
        "satélite: pensó que si conseguía tiempo, podía arreglar el bug real "
        "en silencio antes de que el ensayo lo delatara. El martes a las "
        "23:40, con su propia cuenta y sin abrir ningún ticket de cambio, "
        "entró al repositorio de configuración y modificó los valores de "
        "calibración de entrada de la tabla de frecuencias — no el código con "
        "el error, sino los datos que ese código iba a procesar — de modo que, "
        "al pasar por su rutina defectuosa, el resultado final igual cayera "
        "dentro de norma. Un parche sobre un parche: maquilló la entrada para "
        "que la salida mintiera bien.\n\n"
        "Lo que no calculó fue el control de configuración. Tomás, siguiendo "
        "el procedimiento al pie de la letra por primera vez en semanas — "
        "todavía con culpa por la auditoría que había apurado dos semanas "
        "antes —, corrió la verificación completa de checksums antes de "
        "habilitar el banco de ensayos y encontró un commit sin ticket, "
        "cargado de madrugada, que no coincidía con ningún cambio aprobado. "
        "Alcanzó para frenar todo antes de que el CHALTÉN-III entrara a la "
        "cámara térmica con una mentira adentro.\n\n"
        "Un intento de ganar tiempo — arruinado por la planilla que, esta vez, "
        "alguien completó entera."
    ),
    max_preguntas=15,
    sospechosos=[
        Sospechoso(
            id="rocio",
            nombre="Rocío Aitken",
            cargo="jefa de integración de software (carga útil de comunicaciones)",
            color="bright_cyan",
            personalidad=(
                "Cincuenta y pico, quince años en el área. Metódica, exigente, "
                "protectora de su equipo aunque no lo demuestre. Contesta con "
                "procedimientos y cronogramas antes que con opiniones."
            ),
            coartada=(
                "Dice que se quedó hasta las 22:00 el martes cerrando el plan de "
                "ensayo y se fue derecho a su casa; su marido puede confirmar la "
                "hora en que llegó."
            ),
            actitud=(
                "Profesional y cortante al principio. Si le preguntan por el "
                "desempeño de su equipo o por accesos fuera de horario se pone "
                "incómoda y evasiva antes de contestar con más detalle del que "
                "planeaba."
            ),
            secretos=[
                Secreto(
                    id="sancion_nahuel",
                    pista=(
                        "Hace tres semanas Rocío le hizo a Nahuel un llamado de "
                        "atención formal por un error de código encontrado en una "
                        "revisión — quedó asentado en su legajo."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por el desempeño de Nahuel, por su legajo, "
                        "o por conflictos recientes en el equipo: contás, incómoda, "
                        "que hace tres semanas encontraste un error en una revisión "
                        "de su código y tuviste que hacerle un llamado de atención "
                        "formal. Aclarás que fue un tema menor y que no volviste a "
                        "tener problemas con él, aunque notaste que quedó muy "
                        "afectado."
                    ),
                    criterio_revelacion=(
                        "Cuenta que le hizo a Nahuel un llamado de atención o "
                        "sanción formal por un error de código encontrado en "
                        "revisión."
                    ),
                ),
                Secreto(
                    id="acceso_remoto_nocturno",
                    pista=(
                        "Rocío accedió al repositorio de configuración de forma "
                        "remota, de madrugada, dos veces esa semana — dice que fue "
                        "para adelantar el cronograma del ensayo, no para tocar el "
                        "código de la carga útil."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por los registros de acceso remoto al "
                        "repositorio a su nombre, o por qué estuvo conectada de "
                        "madrugada: admitís, un poco fastidiada porque parece que "
                        "te sospechan a vos, que entraste dos veces de madrugada "
                        "esa semana para terminar de armar el cronograma detallado "
                        "del ensayo — no tocaste una línea de la configuración de "
                        "la carga útil, y podés mostrar los archivos que sí "
                        "modificaste si hace falta."
                    ),
                    criterio_revelacion=(
                        "Admite haber accedido remotamente al repositorio de "
                        "madrugada esa semana, aclarando que fue para el "
                        "cronograma del ensayo y no para modificar la "
                        "configuración de la carga útil."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="tomas",
            nombre="Tomás Bracamonte",
            cargo="técnico de control de configuración",
            color="bright_yellow",
            personalidad=(
                "Treinta años. Prolijo con las planillas pero inseguro cuando lo "
                "cuestionan; se pone nervioso y habla de más si siente que dudan "
                "de su trabajo."
            ),
            coartada=(
                "Dice que esa semana cumplió su horario normal de oficina y que "
                "el martes a la noche estaba en su casa cenando con su pareja."
            ),
            actitud=(
                "Se pone tenso cuando le preguntan por auditorías o controles "
                "anteriores; si le marcan alguna inconsistencia, se derrumba "
                "rápido y confiesa sus propios descuidos, pidiendo que no lo "
                "hagan quedar mal frente a Rocío."
            ),
            secretos=[
                Secreto(
                    id="auditoria_apurada",
                    pista=(
                        "Dos semanas atrás Tomás cerró una auditoría de control de "
                        "configuración sin verificar los checksums de una entrega "
                        "completa — la dio por buena para no atrasar el "
                        "cronograma."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por auditorías anteriores del "
                        "repositorio, por cómo funciona el control de "
                        "configuración, o si hay antecedentes de descuidos: "
                        "confesás, avergonzado, que dos semanas atrás cerraste una "
                        "auditoría sin correr la verificación completa de "
                        "checksums de una entrega, porque venías atrasado y "
                        "confiaste en que estaba todo bien. Aclarás que fue la "
                        "única vez y que por eso ahora revisás todo el doble."
                    ),
                    criterio_revelacion=(
                        "Admite haber cerrado una auditoría de configuración sin "
                        "verificar completamente los checksums de una entrega "
                        "anterior."
                    ),
                ),
                Secreto(
                    id="nahuel_solo_de_noche",
                    pista=(
                        "Tomás vio a Nahuel trabajando solo en el banco de "
                        "pruebas de software una noche esa semana, sin el segundo "
                        "operador que exige el procedimiento — no lo reportó."
                    ),
                    instruccion_actor=(
                        "Solo si te preguntan si viste a alguien en el banco de "
                        "pruebas fuera de horario, o si notaste algo raro en el "
                        "comportamiento de tus compañeros esa semana: contás, con "
                        "culpa, que una noche viste a Nahuel trabajando solo en "
                        "el banco de software, sin el segundo operador que pide "
                        "el procedimiento. No lo reportaste porque pensaste que "
                        "era una excepción de una noche y no quisiste hacerle un "
                        "lío por eso."
                    ),
                    criterio_revelacion=(
                        "Cuenta que vio a Nahuel trabajando solo en el banco de "
                        "pruebas de software sin el segundo operador requerido, y "
                        "que no lo reportó."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="nahuel",
            nombre="Nahuel Bravo",
            cargo="ingeniero de software junior (carga útil de comunicaciones)",
            color="bright_magenta",
            es_culpable=True,
            personalidad=(
                "Veintipocos años, becario que quedó efectivizado hace poco. "
                "Ansioso, perfeccionista, habla rápido cuando está incómodo y se "
                "disculpa por todo. Al principio parece el más colaborador de "
                "los tres."
            ),
            coartada=(
                "Dice que esa semana se quedó trabajando solo hasta tarde varias "
                "noches, puliendo detalles del software antes del ensayo, "
                "porque quería que todo saliera perfecto."
            ),
            actitud=(
                "Colabora de más al principio, ansioso por caer bien. Si lo "
                "presionan con preguntas técnicas puntuales — el commit, los "
                "valores de calibración, la rutina que escribió — se pone "
                "rígido, tarda en responder y termina quebrándose."
            ),
            secretos=[
                Secreto(
                    id="bug_original",
                    pista=(
                        "Meses atrás Nahuel escribió la rutina que interpola la "
                        "tabla de compensación térmica del sintetizador de "
                        "frecuencia; tiene un error que, en los extremos de "
                        "temperatura, calcula mal la ganancia. Nunca fue "
                        "detectado en las revisiones."
                    ),
                    instruccion_actor=(
                        "Si te preguntan específicamente por la rutina de "
                        "interpolación térmica, por quién escribió ese módulo, o "
                        "si hubo errores de diseño en el software que vos "
                        "programaste: admitís, con la voz quebrada, que fuiste "
                        "vos quien escribió esa rutina hace meses, que tiene un "
                        "error en el cálculo de ganancia en los extremos de "
                        "temperatura, y que nadie lo detectó porque vos mismo "
                        "hiciste la revisión de tu propio código y no dijiste "
                        "nada."
                    ),
                    criterio_revelacion=(
                        "Admite haber escrito la rutina con el error de cálculo "
                        "de ganancia en los extremos de temperatura, y que nunca "
                        "fue detectado porque revisó su propio código."
                    ),
                ),
                Secreto(
                    id="alteracion_config",
                    pista=(
                        "El martes a las 23:40, Nahuel cargó al repositorio "
                        "nuevos valores de calibración de la tabla de "
                        "frecuencias, sin ticket de cambio, para que el ensayo "
                        "diera resultados dentro de norma pese al error de su "
                        "código."
                    ),
                    instruccion_actor=(
                        "Solo si ya reconociste el error de tu código "
                        "(bug_original) Y te preguntan directamente por el "
                        "commit del martes a la noche o por los valores de "
                        "calibración modificados: confesás, derrumbado, que esa "
                        "noche entraste al repositorio y cambiaste los valores "
                        "de calibración de entrada para que, al pasar por tu "
                        "rutina con el error, el resultado igual diera dentro de "
                        "norma en el ensayo. No falseaste el ensayo por maldad: "
                        "pensabas arreglar el bug real apenas terminara el "
                        "ensayo, antes de que alguien lo notara."
                    ),
                    criterio_revelacion=(
                        "Confiesa haber modificado los valores de calibración de "
                        "la tabla de frecuencias esa noche, sin ticket de cambio, "
                        "para que el ensayo diera un resultado válido pese al "
                        "error real de su código."
                    ),
                ),
                Secreto(
                    id="miedo_primer_proyecto",
                    pista=(
                        "CHALTÉN-III es el primer proyecto grande de Nahuel "
                        "desde que terminó la carrera; tenía terror de que lo "
                        "aparten del equipo o de decepcionar a Rocío si se sabía "
                        "que su código tenía un error."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por qué nunca reportó el error, por qué "
                        "no pidió ayuda, o qué sintió cuando se dio cuenta del "
                        "problema: explicás, con mucha angustia, que CHALTÉN-III "
                        "es tu primer proyecto grande, que le tenías terror a "
                        "decepcionar a Rocío o a que te sacaran del equipo, y que "
                        "por eso decidiste tratar de arreglarlo solo y en "
                        "silencio en vez de avisar."
                    ),
                    criterio_revelacion=(
                        "Explica que tenía miedo de ser apartado del proyecto o "
                        "de decepcionar a su jefa, y que por eso decidió intentar "
                        "resolver el problema en silencio en vez de reportarlo."
                    ),
                ),
            ],
        ),
    ],
)
