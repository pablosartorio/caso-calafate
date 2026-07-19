"""EL CASO PILTRIQUITRÓN — una modificación no autorizada al sistema de parada
de emergencia del reactor, durante la puesta en marcha de la Central Piltriquitrón.

⚠️ SPOILER: leer los datos de este archivo revela al culpable.
Jugá una partida antes. :)
"""

from caso_calafate.caso import Caso, Secreto, Sospechoso

CASO_PILTRIQUITRON = Caso(
    id="piltriquitron",
    titulo="EL CASO PILTRIQUITRÓN",
    gancho=(
        "En la puesta en marcha de un reactor, alguien tocó el sistema de "
        "parada de emergencia — y después movió papeles para que pareciera "
        "el error de otro."
    ),
    briefing=(
        "El Bolsón, 07:15 de la mañana. Te levanta una llamada de la propia central.\n\n"
        "«Detective, necesitamos que venga. Tenemos un problema de ingeniería que "
        "puede ser mucho más que un problema de ingeniería.»\n\n"
        "En la Central Piltriquitrón, a los pies del cerro, el equipo de puesta en "
        "marcha estaba corriendo la prueba de tiempo de caída de barras del sistema "
        "de parada rápida del reactor — la última función de seguridad que se valida "
        "antes de la primera criticidad. El resultado no cerró. Al revisar, "
        "apareció algo peor que un número fuera de rango: alguien había reemplazado "
        "un módulo de la lógica de disparo por otro que nunca pasó por el Comité de "
        "Control de Cambios de Ingeniería. Nadie firmó ese cambio. O alguien lo firmó "
        "y después se ocupó de que no quedara ningún rastro.\n\n"
        "Lo que se sabe hasta ahora:\n\n"
        " • La prueba de tiempo de caída de barras, el jueves a la tarde, dio un\n"
        "   valor fuera de rango.\n"
        " • Al revisar el módulo físico instalado, el número de parte no coincide\n"
        "   con el del diseño aprobado.\n"
        " • En el sistema de gestión documental, la Solicitud de Modificación de\n"
        "   Ingeniería correspondiente aparece incompleta — falta el campo de\n"
        "   aprobación — y el registro fue editado dos días después de conocerse\n"
        "   la anomalía.\n"
        " • Tres personas del equipo de ingeniería y gerencia de proyecto tenían\n"
        "   acceso a esa documentación. Son tus sospechosos.\n\n"
        "Interrogá, anotá, y cuando estés seguro: acusá. Tenés una sola oportunidad."
    ),
    contexto_actores="""\
En la Central Piltriquitrón, durante la puesta en marcha en frío del reactor, la
prueba de tiempo de caída de barras del sistema de parada rápida dio un resultado
fuera de rango. Al revisar, se descubrió que el módulo de lógica de disparo
instalado no es el que figura en el diseño aprobado, sino un reemplazo que nunca
pasó por el Comité de Control de Cambios de Ingeniería. La Solicitud de
Modificación de Ingeniería correspondiente aparece incompleta y fue editada dos
días después de conocerse la anomalía. Un detective está interrogando al personal
de ingeniería y gerencia de proyecto con acceso a esa documentación.""",
    epilogo=(
        "Hernán Bracamonte, gerente de proyecto de Piltriquitrón, autorizó el reemplazo.\n\n"
        "Seis semanas antes de la prueba, el proveedor que debía entregar la tarjeta "
        "de votación 2-de-3 de la lógica de disparo avisó que no iba a llegar a "
        "tiempo — un problema de producción propio, nada que ver con la central. El "
        "hito de «prueba en frío» tenía una cláusula de penalidad económica dura, y "
        "Bracamonte no estaba dispuesto a explicarle al directorio un atraso por una "
        "tarjeta electrónica. Encontró un módulo de otro fabricante que, en el "
        "papel, cumplía la misma función, y le dijo a Tomás Lizarraga que lo "
        "instalara: que él se encargaba del trámite de ingeniería después, que no "
        "perdieran el hito por un formulario. Nunca lo llevó al Comité de Control de "
        "Cambios. Ni la calificación sísmica del módulo nuevo ni el análisis de "
        "compatibilidad se completaron. Confiaba en que, con el tiempo de respuesta "
        "dentro de rango, nadie iba a mirar dos veces el número de parte.\n\n"
        "No fue así. Cuando la prueba de tiempo de caída de barras dio fuera de "
        "rango y Tomás —con el estómago revuelto por haber instalado él mismo el "
        "reemplazo— pidió revisar el expediente, Bracamonte entró al sistema de "
        "gestión documental con su propio usuario y trató de completar "
        "retroactivamente la Solicitud de Modificación de Ingeniería, dejando el "
        "campo de «propuesto por» a nombre de un ingeniero júnior que ni siquiera "
        "estaba afectado al proyecto esa semana. No contó con que el sistema guarda "
        "el log de auditoría de cada edición, con usuario y hora, y que Andrea "
        "Kessler —a cargo de la configuración documental— lo revisa como parte de "
        "su rutina.\n\n"
        "Una cláusula de penalidad, un módulo «equivalente» y un expediente "
        "retocado dos días tarde: el intento de que pareciera el error de un "
        "ingeniero de menor rango terminó siendo, justamente, la prueba que lo "
        "señaló a él."
    ),
    max_preguntas=15,
    sospechosos=[
        Sospechoso(
            id="hernan",
            nombre="Hernán Bracamonte",
            cargo="gerente de proyecto de la Central Piltriquitrón",
            color="bright_blue",
            es_culpable=True,
            personalidad=(
                "Cordial, mide cada palabra, acostumbrado a manejar reuniones de "
                "directorio y a que le crean. Nunca levanta la voz ni pierde la "
                "sonrisa profesional. Habla en plural («decidimos», «el equipo "
                "resolvió») cuando le conviene diluir responsabilidades."
            ),
            coartada=(
                "Dice que esa tarde estuvo en su oficina cerrando el informe de "
                "avance mensual para el directorio, y que se retiró temprano, antes "
                "de las 18:00."
            ),
            actitud=(
                "Mientras la charla gira en torno a cronogramas y plazos, es dueño "
                "de la conversación y contesta con soltura. Pero si lo llevan a "
                "terreno técnico específico —el módulo, el expediente, el log de "
                "auditoría— se pone rígido, elige mucho las palabras y busca "
                "desviar la charla hacia «eso pregúntenselo a los ingenieros»."
            ),
            secretos=[
                Secreto(
                    id="presion_cronograma",
                    pista=(
                        "El contrato de la puesta en marcha de Piltriquitrón tiene "
                        "una cláusula de penalidad económica fuerte por cada semana "
                        "de atraso del hito de «prueba en frío», y Bracamonte la "
                        "tenía muy presente."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por el cronograma, por el hito de prueba "
                        "en frío o por presiones comerciales del proyecto: admitís, "
                        "sin darle mucha importancia al principio, que había una "
                        "cláusula de penalidad importante en el contrato y que "
                        "estabas muy encima de esa fecha. Enseguida minimizás "
                        "diciendo que «eso es gerencia de proyecto normal, no "
                        "cambia nada de lo técnico»."
                    ),
                    criterio_revelacion=(
                        "Menciona la cláusula de penalidad contractual por atraso "
                        "del hito de puesta en marcha, o reconoce que estaba bajo "
                        "fuerte presión de cronograma."
                    ),
                ),
                Secreto(
                    id="detalle_tecnico_de_mas",
                    pista=(
                        "Bracamonte conoce detalles técnicos específicos del módulo "
                        "de reemplazo —marca, motivo del cambio, hasta la falta de "
                        "calificación sísmica— que un gerente de proyecto no "
                        "debería manejar de memoria."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por el módulo de reemplazo o el proveedor "
                        "alternativo: en algún momento te explayás de más, dando "
                        "detalles técnicos específicos (marca, por qué «es "
                        "equivalente», qué le faltaba certificar) que un gerente no "
                        "manejaría sin haber estado metido en la decisión. Recién "
                        "después te corregís y aclarás que «eso se lo explicaron "
                        "los ingenieros, yo repito lo que me dijeron»."
                    ),
                    criterio_revelacion=(
                        "Da detalles técnicos específicos del módulo de reemplazo "
                        "(marca, certificación faltante, motivo puntual del cambio) "
                        "que exceden lo que un gerente de proyecto sabría de "
                        "memoria sin haber participado de la decisión técnica."
                    ),
                ),
                Secreto(
                    id="acceso_al_expediente",
                    pista=(
                        "El log de auditoría del sistema de gestión documental "
                        "muestra que la Solicitud de Modificación de Ingeniería fue "
                        "accedida y editada con las credenciales del gerente de "
                        "proyecto, dos días después de conocerse la anomalía."
                    ),
                    instruccion_actor=(
                        "Solo si te confrontan directamente con el registro de "
                        "auditoría, o te dicen que tu usuario editó el expediente "
                        "esos días: te ponés tenso y ensayás una explicación poco "
                        "convincente —que alguien pudo usar tu computadora, que no "
                        "te acordás bien de haber entrado al sistema documental esa "
                        "semana— sin llegar nunca a confesar del todo."
                    ),
                    criterio_revelacion=(
                        "Al ser confrontado con el log de auditoría, no logra dar "
                        "una explicación convincente de por qué su usuario editó el "
                        "expediente, o admite haber entrado al sistema documental "
                        "esos días sin recordar bien por qué."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="tomas",
            nombre="Tomás Lizarraga",
            cargo="ingeniero de control y protecciones, diseño de la lógica de disparo",
            color="bright_yellow",
            personalidad=(
                "Treinta y pocos años, meticuloso hasta la obsesión con los "
                "números, pero blando para el conflicto humano. Habla con "
                "precisión técnica de manual y se traba apenas la charla pasa de "
                "las máquinas a las decisiones de la gente."
            ),
            coartada=(
                "Dice que estuvo en sala de control toda la tarde del jueves, "
                "corriendo la prueba de tiempo de caída de barras junto con el "
                "resto del equipo de puesta en marcha."
            ),
            actitud=(
                "Responde rápido y seguro sobre lo técnico. Si lo empujan hacia "
                "el terreno de «quién decidió qué», se pone visiblemente "
                "incómodo, hace silencios largos, y si insisten se quiebra y "
                "termina contando más de lo que había planeado."
            ),
            secretos=[
                Secreto(
                    id="orden_verbal",
                    pista=(
                        "Tomás instaló el módulo de reemplazo por orden verbal "
                        "directa del gerente de proyecto, quien le dijo que él se "
                        "encargaba después del trámite de ingeniería."
                    ),
                    instruccion_actor=(
                        "Al principio decís que el cambio «vino de arriba, con la "
                        "documentación en trámite», sin dar nombres. Solo si te "
                        "preguntan directamente QUIÉN te dio la orden de instalar "
                        "el módulo de reemplazo, o insisten en que expliques por "
                        "qué avanzaste sin la Solicitud de Modificación de "
                        "Ingeniería aprobada: contás, incómodo, que fue el propio "
                        "Hernán Bracamonte quien te lo pidió personalmente, y que "
                        "te aseguró que él se ocupaba del papeleo."
                    ),
                    criterio_revelacion=(
                        "Dice que fue el gerente de proyecto (Bracamonte) quien le "
                        "ordenó instalar el módulo de reemplazo antes de tener la "
                        "aprobación formal de ingeniería."
                    ),
                ),
                Secreto(
                    id="objecion_ignorada",
                    pista=(
                        "Tomás había mandado un mail interno advirtiendo que el "
                        "módulo de reemplazo no tenía la calificación sísmica "
                        "completa. El mail nunca se giró al Comité de Control de "
                        "Cambios."
                    ),
                    instruccion_actor=(
                        "Si te preguntan si vos tenías dudas sobre el módulo, o si "
                        "alguna vez objetaste el reemplazo: admitís, con bronca "
                        "contenida, que mandaste un mail interno señalando que "
                        "faltaba la calificación sísmica del módulo nuevo, pero "
                        "que nunca tuvo respuesta formal y que no insististe "
                        "porque no querías quedar pegado con el gerente."
                    ),
                    criterio_revelacion=(
                        "Cuenta que había advertido, por mail o formalmente, sobre "
                        "la falta de calificación sísmica del módulo de reemplazo, "
                        "y que esa advertencia nunca se procesó."
                    ),
                ),
                Secreto(
                    id="checklist_apurado",
                    pista=(
                        "Tomás firmó el checklist de verificación de instalación "
                        "del módulo de reemplazo sin completar la prueba de "
                        "aislación exigida por el procedimiento, para cerrar la "
                        "tarea antes de una fecha límite que había puesto el "
                        "gerente."
                    ),
                    instruccion_actor=(
                        "Solo si te marcan una inconsistencia entre el checklist "
                        "firmado y lo que realmente se probó, o te preguntan "
                        "directamente si completaste todas las pruebas de "
                        "instalación: confesás, avergonzado, que firmaste el "
                        "checklist sin correr la prueba de aislación completa "
                        "porque Bracamonte quería cerrar la tarea esa misma tarde."
                    ),
                    criterio_revelacion=(
                        "Admite que firmó el checklist de verificación de "
                        "instalación sin completar alguna prueba requerida (por "
                        "ejemplo la de aislación), por presión de tiempo."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="andrea",
            nombre="Andrea Kessler",
            cargo="responsable de gestión de configuración y documentación de ingeniería",
            color="bright_magenta",
            personalidad=(
                "Prolija, memoriosa, de las que archivan todo por las dudas. "
                "Habla con precisión de auditora —fechas, horas, nombres de "
                "archivo— y se pone incómoda cuando tiene que opinar sobre "
                "personas en vez de datos."
            ),
            coartada=(
                "Dice que pasó toda la tarde del jueves y el viernes en su "
                "escritorio, revisando el expediente de la modificación apenas se "
                "enteró de la anomalía en la prueba."
            ),
            actitud=(
                "Es la más colaborativa de los tres al principio, casi ansiosa "
                "por mostrar el log de auditoría. Pero si le preguntan por qué "
                "tardó en reportarlo, o por su relación con Bracamonte, se cierra "
                "y mide mucho lo que dice."
            ),
            secretos=[
                Secreto(
                    id="log_auditoria_gerente",
                    pista=(
                        "El log de auditoría del sistema documental muestra que la "
                        "Solicitud de Modificación de Ingeniería fue editada con "
                        "el usuario del gerente de proyecto, dos días después de "
                        "conocerse la anomalía en la prueba."
                    ),
                    instruccion_actor=(
                        "Sos la más dispuesta a hablar de esto: si te preguntan "
                        "por el expediente, por quién lo editó o por el log de "
                        "auditoría, mostrás sin reparos que el sistema registra "
                        "que se accedió y editó con el usuario de Hernán "
                        "Bracamonte el día después de la prueba fallida."
                    ),
                    criterio_revelacion=(
                        "Dice que el log de auditoría muestra que el expediente "
                        "fue editado con el usuario del gerente de proyecto "
                        "(Bracamonte)."
                    ),
                ),
                Secreto(
                    id="tardanza_en_reportar",
                    pista=(
                        "Andrea encontró la inconsistencia en el expediente un día "
                        "antes de reportarla formalmente: se guardó la sospecha "
                        "una jornada completa antes de avisar."
                    ),
                    instruccion_actor=(
                        "Solo si te preguntan por qué tardaste en dar aviso, o "
                        "notás que te cuestionan por haber demorado el reporte: "
                        "admitís, incómoda, que encontraste la irregularidad un "
                        "día antes de avisar porque necesitabas estar segura antes "
                        "de acusar a alguien tan arriba en la jerarquía."
                    ),
                    criterio_revelacion=(
                        "Admite que detectó la irregularidad en el expediente y "
                        "esperó un día o más antes de reportarla formalmente."
                    ),
                ),
                Secreto(
                    id="conflicto_previo_gerente",
                    pista=(
                        "Meses atrás Andrea había elevado una observación de "
                        "auditoría sobre otro expediente incompleto de "
                        "Bracamonte, y él la frenó diciéndole que no hiciera una "
                        "montaña de un trámite. Quedó una tensión no resuelta "
                        "entre los dos."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por tu relación con el gerente, o si "
                        "tuviste roces con él antes de este caso: contás, con "
                        "cuidado de no sonar vengativa, que meses atrás señalaste "
                        "otra irregularidad documental de Bracamonte y que él la "
                        "minimizó, y que desde entonces la relación quedó tirante."
                    ),
                    criterio_revelacion=(
                        "Cuenta que tuvo un conflicto previo con el gerente de "
                        "proyecto por otra observación de auditoría que él "
                        "minimizó o desestimó."
                    ),
                ),
            ],
        ),
    ],
)
