"""EL CASO ESQUEL — un patrón de calibración desviado en el Centro de Dosimetría Esquel.

⚠️ SPOILER: leer los datos de este archivo revela al culpable.
Jugá una partida antes. :)
"""

from caso_calafate.caso import Caso, Secreto, Sospechoso

CASO_ESQUEL = Caso(
    id="esquel",
    titulo="EL CASO ESQUEL",
    gancho=(
        "Un control de rutina destapó que el patrón que calibra la radioterapia "
        "de media Patagonia estaba mal — y alguien lo tapó."
    ),
    briefing=(
        "Esquel, Chubut. 07:15 de la mañana. Te despierta el teléfono.\n\n"
        "«Detective, necesitamos que venga al Centro de Dosimetría y Calibración. "
        "Encontramos algo que no puede esperar.»\n\n"
        "El Centro Esquel certifica los patrones de referencia con los que una "
        "docena de hospitales de la Patagonia calibran sus equipos de "
        "radioterapia. Ayer, durante un control cruzado de rutina, el "
        "laboratorio detectó que el patrón secundario — la cámara de "
        "ionización que se usa como referencia — estaba desviado casi un 3% "
        "respecto de lo que decía su certificado de calibración vigente, "
        "firmado hace cinco semanas.\n\n"
        "Lo que se sabe hasta ahora:\n\n"
        " • El certificado lo emitió el proveedor externo que hace el\n"
        "   mantenimiento y la recalibración periódica del patrón: Metrología\n"
        "   Austral S.R.L.\n"
        " • El instrumento de lectura guarda un registro interno de las\n"
        "   mediciones crudas que nadie puede editar a mano; ese registro no\n"
        "   coincide con los valores finales del certificado firmado.\n"
        " • Solo tres personas tuvieron el certificado en sus manos antes de\n"
        "   que quedara archivado como válido: el técnico que lo redactó y dos\n"
        "   personas del laboratorio.\n"
        " • Ya se avisó a los hospitales que habían calibrado con ese patrón\n"
        "   en las últimas cinco semanas: todos revisaron sus equipos a\n"
        "   tiempo. No hubo ningún paciente afectado.\n\n"
        "Interrogá, anotá, y cuando estés seguro: acusá. Tenés una sola oportunidad."
    ),
    contexto_actores="""\
Hace cinco semanas, el proveedor externo Metrología Austral S.R.L. hizo el
mantenimiento y la recalibración periódica del patrón secundario de
dosimetría del Centro Esquel, y entregó un certificado de calibración
conforme. Ayer, un control cruzado interno de rutina detectó que el patrón
estaba desviado casi un 3% respecto de lo que decía ese certificado. El
registro interno de mediciones crudas del instrumento no coincide con los
valores finales firmados. Tres personas tuvieron el certificado en sus manos
antes de que quedara archivado como válido: el técnico del proveedor externo
y dos integrantes del laboratorio. Los hospitales afectados ya revisaron sus
equipos; no hubo daño a ningún paciente. Un detective está interrogando a
las tres personas que tuvieron acceso al certificado.""",
    epilogo=(
        "Braian Coliqueo alteró el certificado de calibración del patrón "
        "secundario del Centro Esquel.\n\n"
        "Metrología Austral factura el service periódico como un paquete "
        "cerrado — limpieza, ajuste y la comparación cruzada de 24 horas "
        "contra la fuente de control — sea cual sea el tiempo que realmente "
        "insuma. Esa tarde Braian tenía otra visita agendada en Comodoro "
        "Rivadavia y no quiso perder el turno; decidió saltarse las 24 horas "
        "de estabilización con la fuente de control, el paso que menos se "
        "nota y el que más tiempo consume, confiado en que el patrón iba a "
        "seguir dentro de tolerancia como en cada visita anterior. No fue "
        "así: sin el ajuste fino de esa comparación, el patrón quedó "
        "desviado casi un 3%. En vez de avisar y volver, antes de irse editó "
        "el PDF del certificado para que mostrara el valor final que él "
        "sabía que tenía que dar — el que hubiera salido si hubiese "
        "completado el proceso — y lo firmó como conforme.\n\n"
        "Lo delató lo único que no pudo tocar: el electrómetro guarda un "
        "registro interno de cada lectura cruda, con hora y fecha, que no "
        "pasa por ningún informe editable. Ese registro se corta exactamente "
        "en el paso de la comparación cruzada, cinco horas antes de la hora "
        "de salida que el propio Braian anotó en su planilla de visita.\n\n"
        "Marisa había firmado la recepción del certificado confiando, como "
        "siempre, en la palabra del proveedor — apurada, además, por una "
        "novedad familiar que prefería no ventilar en el trabajo. Nahuel fue "
        "quien encontró la desviación en el control cruzado, y por miedo a "
        "haberse equivocado él mismo, se guardó el resultado dos días para "
        "repetir la medición antes de escalarlo — dos días que, a los ojos "
        "de cualquiera, también podían parecer sospechosos.\n\n"
        "Un ahorro de cinco horas que, tarde o temprano, el propio patrón se "
        "encargó de delatar."
    ),
    max_preguntas=15,
    sospechosos=[
        Sospechoso(
            id="marisa",
            nombre="Marisa Huenchul",
            cargo="jefa de Metrología y Aseguramiento de Calidad del Centro Esquel",
            color="bright_cyan",
            personalidad=(
                "Meticulosa, algo ansiosa, con vocación real de hacer las cosas "
                "bien. Habla con precisión técnica y le gusta citar el "
                "procedimiento correspondiente, pero se pone visiblemente "
                "incómoda con preguntas personales."
            ),
            coartada=(
                "Dice que esa tarde revisó y archivó el certificado de Metrología "
                "Austral como cualquier otro, sin nada fuera de lo normal, y que "
                "se fue del Centro a la hora de siempre."
            ),
            actitud=(
                "Responde con aplomo sobre cuestiones técnicas, pero si le "
                "preguntan por su rutina esa tarde puntual o por la relación del "
                "Centro con el proveedor, se pone tensa, da vueltas y evita "
                "mirar a los ojos antes de sincerarse."
            ),
            secretos=[
                Secreto(
                    id="marisa_apurada_padre",
                    pista=(
                        "Marisa se fue del laboratorio antes de lo habitual el día "
                        "que firmó el certificado, porque su padre había sido "
                        "internado esa misma mañana."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por tu coartada esa tarde, al principio "
                        "sos evasiva y decís que 'tenías cosas personales que "
                        "atender'; solo si insisten en qué cosas, o te marcan que "
                        "te fuiste antes de lo normal, contás, incómoda, que tu "
                        "padre había entrado de urgencia al hospital esa mañana y "
                        "vos estabas pendiente del teléfono, así que revisaste el "
                        "certificado más rápido de lo que hubieras querido."
                    ),
                    criterio_revelacion=(
                        "Admite que se fue temprano o revisó el certificado "
                        "apurada porque su padre estaba internado esa tarde."
                    ),
                ),
                Secreto(
                    id="marisa_contrato_renovacion",
                    pista=(
                        "El Centro está por renovar el contrato anual de service "
                        "con Metrología Austral, y Marisa fue quien empujó la "
                        "renovación pese a que el proveedor es más caro que otras "
                        "opciones de la región."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por la relación del Centro con el "
                        "proveedor, o por qué confiaron tanto en Braian: admitís "
                        "que empujaste la renovación del contrato con Metrología "
                        "Austral porque es la única empresa con turnos "
                        "disponibles en la región en menos de dos meses, y que "
                        "eso te volvió más blanda a la hora de cuestionar sus "
                        "tiempos de trabajo."
                    ),
                    criterio_revelacion=(
                        "Reconoce que impulsó la renovación del contrato con el "
                        "proveedor pese a las dudas, o que eso la volvió menos "
                        "exigente con los tiempos de trabajo del técnico."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="nahuel",
            nombre="Nahuel Epuyén",
            cargo="técnico de laboratorio, a cargo del control cruzado de patrones",
            color="bright_yellow",
            personalidad=(
                "Joven, prolijo, un poco inseguro de sus propias mediciones pese "
                "a ser bueno en lo suyo. Habla despacio, como pensando cada "
                "palabra, y se pone visiblemente nervioso si siente que dudan de "
                "su trabajo."
            ),
            coartada=(
                "Dice que detectó la desviación del patrón en el control cruzado "
                "de rutina de esta semana y que apenas la vio dio aviso a Marisa."
            ),
            actitud=(
                "Se pone nervioso fácil. Si le marcan inconsistencias en las "
                "fechas, o le preguntan directamente por su relación personal "
                "con Braian, titubea y termina confesando sus verdades chicas, "
                "casi aliviado de sacárselas de encima."
            ),
            secretos=[
                Secreto(
                    id="nahuel_demora_reporte",
                    pista=(
                        "Nahuel encontró la desviación del patrón dos días antes "
                        "de reportarla: repitió la medición en silencio porque "
                        "temía haberse equivocado él mismo."
                    ),
                    instruccion_actor=(
                        "Si te preguntan cuándo detectaste la desviación por "
                        "primera vez, al principio decís 'apenas la vi, la "
                        "reporté'. Pero si te muestran las fechas de los "
                        "registros de laboratorio o insisten en la línea de "
                        "tiempo, admitís, avergonzado, que la viste dos días "
                        "antes y repetiste la medición vos solo, en silencio, "
                        "porque pensabas que el error podía ser tuyo."
                    ),
                    criterio_revelacion=(
                        "Admite que detectó la desviación antes de reportarla y "
                        "que repitió la medición en silencio por miedo a "
                        "haberse equivocado él mismo."
                    ),
                ),
                Secreto(
                    id="nahuel_plata_braian",
                    pista=(
                        "Braian le debe plata a Nahuel por un arreglo personal "
                        "(le vendió una notebook usada) y todavía no se la pagó."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por tu relación con Braian, o si tenés "
                        "algo personal con él: al principio decís que 'lo "
                        "conocés de las visitas de service, nada más'. Si "
                        "insisten, o preguntan directamente por deudas o plata "
                        "de por medio, contás, medio incómodo, que le vendiste "
                        "una notebook usada hace unos meses y todavía te debe "
                        "una parte de la plata, y que eso te da bronca pero no "
                        "tiene nada que ver con el patrón."
                    ),
                    criterio_revelacion=(
                        "Menciona que Braian le debe dinero por una venta "
                        "personal (por ejemplo, una notebook) y que hay tensión "
                        "entre ellos por eso."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="braian",
            nombre="Braian Coliqueo",
            cargo="técnico de service de Metrología Austral S.R.L. (proveedor externo)",
            color="bright_red",
            es_culpable=True,
            personalidad=(
                "Vendedor nato, simpático, siempre con una broma o una excusa de "
                "agenda a mano. Habla con mucha jerga técnica tranquilizadora "
                "cuando se pone nervioso. Cuando lo acorralan, en vez de "
                "callarse, habla de más."
            ),
            coartada=(
                "Dice que estuvo en el Centro Esquel toda la jornada haciendo el "
                "service completo del patrón, que se fue pasadas las 18:00 rumbo "
                "a Comodoro Rivadavia para otra visita, y que el certificado que "
                "entregó refleja exactamente lo que midió."
            ),
            actitud=(
                "Si lo presionan en general, minimiza con chistes y cita "
                "cláusulas de su contrato de service. Si lo confrontan con datos "
                "técnicos concretos (tiempos, registros del electrómetro), se "
                "pone nervioso, habla de más para taparlo y recién ahí empieza a "
                "ceder terreno."
            ),
            secretos=[
                Secreto(
                    id="braian_service_recortado",
                    pista=(
                        "El paso de comparación cruzada con la fuente de control "
                        "(24 horas de estabilización) no se completó ese día, "
                        "aunque el certificado dice que sí."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por el procedimiento completo o por "
                        "cuánto tiempo estuvo cada etapa del service: minimizás, "
                        "usás jerga técnica tranquilizadora y evitás admitirlo "
                        "directamente. Pero si te presionan con los tiempos "
                        "exactos o con el registro del electrómetro, te trabás y "
                        "terminás admitiendo que salteaste el paso de las 24 "
                        "horas con la fuente de control."
                    ),
                    criterio_revelacion=(
                        "Admite que no completó el paso de comparación o "
                        "estabilización de 24 horas con la fuente de control."
                    ),
                ),
                Secreto(
                    id="braian_otro_cliente",
                    pista=(
                        "Braian tenía agendado otro cliente urgente en Comodoro "
                        "Rivadavia esa misma tarde y salió del Centro Esquel con "
                        "el tiempo justo."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por tu agenda esa tarde o por qué te "
                        "fuiste a esa hora: admitís, medio orgulloso, que tenías "
                        "otro cliente esperándote en Comodoro Rivadavia, que "
                        "cobrás por visita y no por hora, y que no ibas a perder "
                        "esa segunda visita por nada del mundo."
                    ),
                    criterio_revelacion=(
                        "Admite que tenía otro cliente o compromiso urgente que "
                        "lo apuraba esa tarde."
                    ),
                ),
                Secreto(
                    id="braian_certificado_alterado",
                    pista=(
                        "El valor final del certificado firmado no coincide con "
                        "la última lectura cruda guardada en el electrómetro: "
                        "alguien editó el documento después de la medición."
                    ),
                    instruccion_actor=(
                        "Nunca confesás espontáneamente. Si te confrontan "
                        "directamente con la discrepancia entre el registro del "
                        "electrómetro y el certificado firmado, te ponés a la "
                        "defensiva y decís que 'los valores finales incluyen "
                        "correcciones de firmware que el registro no muestra' "
                        "(una excusa técnica falsa). Solo si insisten mucho, o "
                        "te acusan directamente de haber editado el documento, "
                        "te quebrás y minimizás: decís que fue 'una diferencia de "
                        "nada', que igual el patrón iba a dar bien en la próxima "
                        "visita, y que no quisiste perder el contrato anual por "
                        "un ajuste que ibas a terminar la vez siguiente."
                    ),
                    criterio_revelacion=(
                        "Admite, aunque sea minimizando, haber modificado o "
                        "alterado el certificado para ocultar que el service "
                        "había quedado incompleto."
                    ),
                ),
            ],
        ),
    ],
)
