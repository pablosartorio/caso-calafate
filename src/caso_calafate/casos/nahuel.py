"""EL CASO NAHUEL — una dosis mal calibrada y un registro que no debía existir,
en el Centro Nahuel de Medicina Nuclear y Radioterapia.

⚠️ SPOILER: leer los datos de este archivo revela al culpable.
Jugá una partida antes. :)
"""

from caso_calafate.caso import Caso, Secreto, Sospechoso

CASO_NAHUEL = Caso(
    id="nahuel",
    titulo="EL CASO NAHUEL",
    gancho=(
        "Un paciente recibió más dosis de la indicada, y alguien se encargó "
        "de que nadie supiera cuándo empezó el error."
    ),
    briefing=(
        "Neuquén, 08:15 de la mañana. Te suena el teléfono.\n\n"
        "«Detective, necesitamos que venga al Centro Nahuel. Ya. Antes de que "
        "esto llegue a la prensa.»\n\n"
        "El Centro Nahuel de Medicina Nuclear y Radioterapia atiende pacientes "
        "oncológicos de toda la Línea Sur y buena parte del Alto Valle. Ayer, el "
        "control mensual de dosimetría in vivo — la verificación que compara la "
        "dosis prescripta con la que el equipo realmente entregó — detectó que, "
        "dos semanas atrás, el acelerador lineal le había entregado a un "
        "paciente casi un 9% más de dosis de la indicada en una de sus "
        "sesiones. El paciente está bien: la desviación se detectó a tiempo y "
        "el tratamiento se corrigió sin secuelas. Lo que no está tan bien es lo "
        "que encontraron después, revisando papeles.\n\n"
        "Lo que se sabe hasta ahora:\n\n"
        " • La desviación coincide con la semana en que se hizo la calibración\n"
        "   de rutina del equipo — la única explicación razonable para un error\n"
        "   así de sistemático y sostenido en varias sesiones.\n"
        " • Al ir a revisar el registro de esa calibración en el sistema de\n"
        "   gestión de calidad, faltaban las mediciones originales: en su lugar\n"
        "   hay una entrada que coincide, número por número, con la calibración\n"
        "   de la semana anterior.\n"
        " • Solo tres personas tienen acceso a ese sistema: la jefa del\n"
        "   Servicio de Radioterapia, el técnico operador del acelerador y el\n"
        "   físico médico responsable de la calibración.\n"
        " • Nadie reportó ningún desperfecto del equipo esa semana.\n\n"
        "Interrogá, anotá, y cuando estés seguro: acusá. Tenés una sola oportunidad."
    ),
    contexto_actores="""\
Hace dos semanas, en el Centro Nahuel de Medicina Nuclear y Radioterapia
(Neuquén), el acelerador lineal usado para tratamientos oncológicos entregó
una dosis casi 9% mayor a la prescripta en una sesión de un paciente. La
desviación se detectó a tiempo en el control mensual de dosimetría in vivo y
no tuvo consecuencias clínicas. Al revisar el registro de calibración semanal
del equipo correspondiente a esa semana, se encontró que las mediciones
originales no están: fueron reemplazadas por una entrada idéntica a la
calibración de la semana anterior. Solo la jefa del Servicio de Radioterapia,
el técnico operador del acelerador y el físico médico responsable de la
calibración tienen acceso al sistema de gestión de calidad donde se guarda ese
registro. Un detective está interrogando a los tres.""",
    epilogo=(
        "El físico médico Ariel Bracamonte fue quien alteró el registro de "
        "calibración.\n\n"
        "Esa semana tenía que viajar a Buenos Aires por un trámite personal "
        "urgente — la renovación de su matrícula profesional, con turno fijo e "
        "improrrogable — y decidió hacer la calibración de rutina del "
        "acelerador solo, sin esperar a que la jefa de servicio consiguiera a "
        "alguien para el doble chequeo que exige el protocolo. Se apuró, usó "
        "una tabla de corrección por temperatura y presión que no era la "
        "vigente esa semana, y nadie lo notó, porque se suponía que nadie más "
        "tenía que revisar esa calibración hasta la siguiente.\n\n"
        "Diez días después, el control mensual de dosimetría in vivo mostró la "
        "desviación. Cuando la jefa de servicio le pidió el registro de esa "
        "semana para entender qué había pasado, Ariel entró al sistema de "
        "gestión de calidad, borró las mediciones reales y las reemplazó por "
        "una copia exacta de la calibración de la semana anterior — la que sí "
        "estaba bien. Después redactó un ticket al soporte técnico del "
        "fabricante sugiriendo una posible falla de firmware del equipo, para "
        "que la sospecha recayera en la máquina y no en él. Tenía pánico de "
        "perder la matrícula por un error humano que, encima, había cometido "
        "saltándose un protocolo que él mismo había ayudado a redactar.\n\n"
        "Lo que Ariel no tuvo en cuenta — o prefirió no acordarse — es que el "
        "acelerador manda automáticamente una copia de cada calibración a un "
        "servidor de telemetría del fabricante, pensado para diagnóstico "
        "remoto del equipo y no como registro oficial del centro. Esa copia, "
        "con el timestamp original intacto, todavía tenía los números reales: "
        "los mismos que él había borrado del sistema local.\n\n"
        "Un físico impecable en el papel, hundido por una copia de seguridad "
        "que ni siquiera sabía que estaba mirando."
    ),
    max_preguntas=15,
    sospechosos=[
        Sospechoso(
            id="marisa",
            nombre="Marisa Quintriqueo",
            cargo="jefa del Servicio de Radioterapia",
            color="bright_cyan",
            personalidad=(
                "Seria, precisa, acostumbrada a defender su servicio de recortes "
                "de presupuesto. Habla en términos clínicos y protocolares. No "
                "le gusta que se cuestione la gestión del servicio, y menos "
                "todavía que se cuestione al personal a su cargo delante suyo."
            ),
            coartada=(
                "Dice que la semana del incidente estuvo de licencia, asistiendo "
                "a un congreso de oncología en Buenos Aires."
            ),
            actitud=(
                "Si la presionan sobre la gestión del servicio, defiende su "
                "trabajo citando protocolos y recursos insuficientes. Pero si le "
                "marcan que algo no cierra con su coartada, o le preguntan con "
                "insistencia dónde estuvo realmente esos días, se pone incómoda "
                "y evasiva antes de admitir la verdad."
            ),
            secretos=[
                Secreto(
                    id="pedido_segundo_fisico",
                    pista=(
                        "Marisa había pedido, meses atrás, contratar un segundo "
                        "físico médico para poder cumplir siempre el protocolo "
                        "de doble chequeo en la calibración semanal. Gerencia se "
                        "lo negó por presupuesto."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por el protocolo de doble chequeo, por "
                        "la carga de trabajo del físico, o por pedidos de "
                        "personal que hayas hecho: contás, con amargura "
                        "contenida, que hace meses pediste por escrito un "
                        "segundo físico médico para que la calibración semanal "
                        "se hiciera siempre con el doble chequeo que marca el "
                        "protocolo, y que gerencia lo rechazó por costos."
                    ),
                    criterio_revelacion=(
                        "Menciona que pidió o reclamó la incorporación de un "
                        "segundo físico médico para el doble chequeo de "
                        "calibración, y que fue rechazado por presupuesto o "
                        "gerencia."
                    ),
                ),
                Secreto(
                    id="licencia_no_fue_congreso",
                    pista=(
                        "Marisa no estuvo en el congreso que dice: pidió esos "
                        "días porque su madre tuvo una internación corta, y no "
                        "lo blanqueó para no parecer ausente del servicio en un "
                        "momento delicado."
                    ),
                    instruccion_actor=(
                        "Al principio sostenés que estuviste en el congreso de "
                        "oncología en Buenos Aires. Solo si te marcan una "
                        "inconsistencia (que no hay registro de tu inscripción, "
                        "que nadie te vio ahí) o te preguntan directamente y con "
                        "insistencia dónde estuviste esos días: confesás, "
                        "incómoda, que en realidad pediste esos días porque tu "
                        "madre tuvo una internación corta, y que no quisiste que "
                        "se supiera para no dar la imagen de que abandonaste el "
                        "servicio en un momento así."
                    ),
                    criterio_revelacion=(
                        "Admite que no estuvo en el congreso y que en realidad "
                        "se ausentó por un problema de salud familiar (su "
                        "madre), que ocultó para no parecer negligente."
                    ),
                ),
                Secreto(
                    id="llamado_atencion_previo",
                    pista=(
                        "Marisa ya le había llamado la atención, meses atrás, al "
                        "físico Ariel Bracamonte por calibrar equipos solo, sin "
                        "el doble chequeo, aunque nunca hizo un reporte formal."
                    ),
                    instruccion_actor=(
                        "Si te preguntan si alguna vez tuviste algún problema de "
                        "desempeño con el equipo, o específicamente con el "
                        "físico Ariel: contás, cuidándote de no acusarlo "
                        "directamente, que meses atrás notaste que a veces él "
                        "calibraba solo cuando no había con quién hacer el "
                        "doble chequeo, se lo remarcaste verbalmente, y él te "
                        "aseguró que no iba a volver a pasar. No hiciste ningún "
                        "reporte formal sobre eso."
                    ),
                    criterio_revelacion=(
                        "Cuenta que ya había advertido o llamado la atención al "
                        "físico médico por calibrar equipos sin el doble "
                        "chequeo, sin haber hecho un reporte formal."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="cesar",
            nombre="César Huenchumil",
            cargo="técnico operador del acelerador lineal (turno tarde)",
            color="bright_yellow",
            personalidad=(
                "Treinta y dos años, buen técnico, mal manejo de los nervios. "
                "Habla de más cuando está ansioso y se contradice solo. Le cae "
                "bien todo el mundo y no quiere meter a nadie en problemas, lo "
                "cual lo hace peor mintiendo."
            ),
            coartada=(
                "Dice que esa semana estuvo todo el turno tarde operando el "
                "equipo con los pacientes agendados y que no tocó nada del "
                "sistema de calibración."
            ),
            actitud=(
                "Cuanto más lo presionan, más se enreda. Si le marcan una "
                "contradicción o le insisten sobre algo puntual (el checklist, "
                "si vio a alguien fuera de horario), se quiebra rápido y "
                "confiesa sus verdades chicas, aclarando todo el tiempo que él "
                "no hizo nada malo."
            ),
            secretos=[
                Secreto(
                    id="vio_fisico_solo_de_noche",
                    pista=(
                        "César vio al físico Ariel Bracamonte solo en la sala de "
                        "control una noche de esa semana, con el sistema de "
                        "calidad abierto, fuera del horario habitual."
                    ),
                    instruccion_actor=(
                        "Solo si te preguntan si viste algo raro esa semana, o "
                        "específicamente si viste al físico fuera de horario: "
                        "contás, dudando si corresponde 'acusarlo', que una "
                        "noche volviste al Centro a buscar algo que te habías "
                        "olvidado y viste a Ariel solo en la sala de control, "
                        "con la notebook del sistema de calidad abierta, a una "
                        "hora en que no había turno. En el momento no le diste "
                        "importancia, pensaste que se estaba poniendo al día "
                        "con algo atrasado."
                    ),
                    criterio_revelacion=(
                        "Cuenta haber visto al físico médico solo en la sala de "
                        "control, con el sistema de gestión de calidad abierto, "
                        "fuera del horario habitual, esa misma semana."
                    ),
                ),
                Secreto(
                    id="checklist_incompleto",
                    pista=(
                        "César no completó el checklist diario de verificación "
                        "del acelerador un día de esa semana porque llegó tarde, "
                        "y le pidió a un compañero que lo firmara igual."
                    ),
                    instruccion_actor=(
                        "Al principio negás cualquier problema con tus "
                        "controles diarios. Si te presionan sobre si siempre "
                        "cumplís el checklist matutino de arranque, o te marcan "
                        "que falta tu firma en algún registro de esa semana: "
                        "confesás, angustiado, que un día llegaste tarde, te "
                        "salteaste el checklist de la mañana y le pediste a un "
                        "compañero que lo firmara para no meterte en "
                        "problemas."
                    ),
                    criterio_revelacion=(
                        "Admite que un día no completó (o hizo firmar sin "
                        "completar) el checklist diario de verificación del "
                        "acelerador."
                    ),
                ),
                Secreto(
                    id="reto_previo_ariel",
                    pista=(
                        "Ariel le hizo a César un comentario despectivo delante "
                        "de otros compañeros, diciendo que 'los técnicos no "
                        "entienden de física'. Quedó tensión entre los dos."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por tu relación con el físico Ariel, o "
                        "si hay mal clima en el equipo de trabajo: contás, un "
                        "poco resentido, que Ariel te cargó feo delante de "
                        "otros compañeros diciendo que 'los técnicos no "
                        "entienden de física', después de que le preguntaste "
                        "algo sobre la calibración. Desde entonces la relación "
                        "quedó tensa."
                    ),
                    criterio_revelacion=(
                        "Cuenta que tuvo un cruce o recibió un comentario "
                        "despectivo del físico médico que generó tensión entre "
                        "ambos."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="ariel",
            nombre="Ariel Bracamonte",
            cargo="físico médico responsable de calibración de equipos",
            color="bright_magenta",
            es_culpable=True,
            personalidad=(
                "Metódico, calmo, hincha con los tecnicismos. Contesta como si "
                "estuviera citando un manual del fabricante. Nunca levanta la "
                "voz, lo cual a veces resulta más inquietante que si gritara."
            ),
            coartada=(
                "Dice que esa semana hizo la calibración de rutina del "
                "acelerador como siempre, según el protocolo vigente, y que si "
                "hay algo raro en el registro tiene que ser un problema del "
                "software de gestión de calidad."
            ),
            actitud=(
                "Nunca pierde la calma. Ante cualquier evidencia, la 'explica' "
                "con tecnicismos y desvía la sospecha hacia el software o hacia "
                "una posible falla de sincronización del equipo. Jamás confiesa "
                "espontáneamente; solo se pone especialmente técnico y preciso "
                "-casi nervioso- cuando tocan el registro de calibración o la "
                "posibilidad de que exista algún respaldo externo de esos "
                "datos."
            ),
            secretos=[
                Secreto(
                    id="respaldo_remoto_telemetria",
                    pista=(
                        "El acelerador envía automáticamente una copia de cada "
                        "calibración a un servidor de telemetría del "
                        "fabricante, independiente del registro local del "
                        "centro. Ariel no lo mencionó."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por respaldos, copias, o si existe "
                        "algún otro lugar donde quede registrada la "
                        "calibración además del sistema local: cometés tu único "
                        "desliz, explicando con demasiado detalle técnico que "
                        "el equipo manda telemetría en forma automática a un "
                        "servidor del fabricante... y recién ahí notás que "
                        "dijiste de más, e intentás minimizarlo aclarando que "
                        "'eso es solo para diagnóstico del equipo, no un "
                        "registro oficial'."
                    ),
                    criterio_revelacion=(
                        "Revela que existe un respaldo o telemetría remota del "
                        "fabricante que conserva los datos originales de "
                        "calibración, independiente del sistema local."
                    ),
                ),
                Secreto(
                    id="calibro_solo_sin_doble_chequeo",
                    pista=(
                        "Esa semana Ariel hizo la calibración solo, sin el "
                        "doble chequeo que exige el protocolo, porque tenía "
                        "apuro por un trámite personal."
                    ),
                    instruccion_actor=(
                        "Si te preguntan directamente si hiciste la calibración "
                        "de esa semana con el doble chequeo del protocolo, o "
                        "por qué la hiciste solo: al principio decís que 'se "
                        "hizo como siempre'. Solo si insisten con el protocolo, "
                        "o te marcan que no hay registro de un segundo físico "
                        "esa semana: admitís, minimizando, que ese día tenías "
                        "apuro por un trámite personal y decidiste hacerla "
                        "solo, porque 'ya la había hecho cien veces'."
                    ),
                    criterio_revelacion=(
                        "Admite que hizo la calibración de esa semana sin el "
                        "doble chequeo del protocolo, estando solo."
                    ),
                ),
                Secreto(
                    id="alteracion_registro",
                    pista=(
                        "Después de enterarse, por el control cruzado, de que "
                        "la dosis había salido mal, Ariel entró al sistema de "
                        "gestión de calidad y reemplazó los valores de esa "
                        "semana por los de la semana anterior, para que "
                        "pareciera una calibración normal."
                    ),
                    instruccion_actor=(
                        "Nunca confesás esto espontáneamente. Solo si te "
                        "confrontan con la existencia del respaldo remoto de "
                        "telemetría (o con que los valores del registro local "
                        "no coinciden con ningún otro registro) Y además te "
                        "preguntan directamente si vos modificaste o borraste "
                        "el registro: ahí, recién, se te cae la calma. Admitís, "
                        "a media voz, que reemplazaste los datos de esa semana "
                        "por los de la semana anterior porque entraste en "
                        "pánico, con miedo a perder la matrícula por un error "
                        "que sabías que era tuyo."
                    ),
                    criterio_revelacion=(
                        "Confiesa haber alterado o reemplazado el registro de "
                        "calibración de esa semana para ocultar el error real."
                    ),
                ),
            ],
        ),
    ],
)
