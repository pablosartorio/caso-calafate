"""EL CASO HUEMUL — una parada automática de seguridad en el reactor de
investigación Huemul, y un registro de turno que alguien reescribió después.

⚠️ SPOILER: leer los datos de este archivo revela al culpable.
Jugá una partida antes. :)
"""

from caso_calafate.caso import Caso, Secreto, Sospechoso

CASO_HUEMUL = Caso(
    id="huemul",
    titulo="EL CASO HUEMUL",
    gancho=(
        "A la 01:47 de la madrugada el reactor Huemul se frenó solo, como "
        "tenía que hacer. Lo raro es lo que alguien escribió después."
    ),
    briefing=(
        "Bariloche, 06:45 de la mañana. Te suena el teléfono.\n\n"
        "«Detective, tenemos un problema en el Complejo Atómico Huemul. Nadie "
        "se lastimó, pero necesitamos que venga.»\n\n"
        "Anoche, durante un ensayo nocturno programado del reactor de "
        "investigación Huemul, el sistema de refrigeración tuvo una anomalía "
        "térmica que activó la parada automática de seguridad. No hubo "
        "heridos, no hubo fuga, no hubo daño en el núcleo: el reactor hizo "
        "exactamente lo que tenía que hacer. El problema apareció después, "
        "cuando el ingeniero de turno de la mañana revisó el registro "
        "digital de turno y encontró que alguien lo había alterado horas "
        "antes de que él llegara.\n\n"
        "Lo que se sabe hasta ahora:\n\n"
        " • El ensayo empezó a las 23:30: arranque a baja potencia para\n"
        "   probar un elemento combustible instrumentado nuevo.\n"
        " • A la 01:47 la temperatura de salida del núcleo tocó el punto de\n"
        "   disparo y el reactor se detuvo solo, como marca el procedimiento.\n"
        " • El registro digital de turno tiene un tramo de seis minutos —\n"
        "   entre la 01:41 y la 01:47 — que fue sobreescrito: el valor de\n"
        "   apertura de una válvula del circuito secundario aparece\n"
        "   \"corregido\" después del hecho.\n"
        " • Esa madrugada había tres personas con acceso al sistema de\n"
        "   control y registro. Son tus sospechosos.\n\n"
        "Interrogá, anotá, y cuando estés seguro: acusá. Tenés una sola oportunidad."
    ),
    contexto_actores="""\
Anoche, durante un ensayo nocturno programado del reactor de investigación
Huemul (arranque a baja potencia para probar un elemento combustible
instrumentado nuevo), el sistema de refrigeración tuvo una anomalía térmica:
la temperatura de salida del núcleo tocó el punto de disparo a la 01:47 y el
reactor se detuvo automáticamente por seguridad, sin heridos ni fuga de
material. A la mañana, el ingeniero de turno del día encontró que el registro
digital de turno había sido alterado: falta un tramo de seis minutos
(01:41-01:47) y el valor de apertura de una válvula del circuito secundario
fue modificado después del hecho. Un detective está interrogando al personal
que tuvo acceso al sistema de control y registro esa madrugada.""",
    epilogo=(
        "Ricardo Aballay causó la anomalía y después alteró el registro para taparla.\n\n"
        "A las 23:30 arrancó el ensayo programado: probar, a baja potencia, un "
        "elemento combustible instrumentado nuevo. El cronograma era ajustado "
        "— el reactor debía quedar frío y disponible antes de las 07:00 para "
        "una inspección regulatoria que el propio Ricardo había pedido "
        "adelantar, para no perder otro día de parada. Cerca de la 01:40, con "
        "el rebalanceo de caudal del circuito secundario demorado, tomó un "
        "atajo que había hecho mil veces sin problema: cerró manualmente una "
        "válvula para acelerar la secuencia, sin esperar la verificación "
        "automática que exige el procedimiento. Esta vez el rebalanceo no "
        "fue parejo: la temperatura de salida del núcleo subió más rápido de "
        "lo previsto y, a la 01:47, tocó el punto de disparo. El reactor hizo "
        "lo que tenía que hacer — se frenó solo, sin daño, sin fuga, sin "
        "heridos.\n\n"
        "El problema, para Ricardo, no fue el scram: fue lo que el scram iba "
        "a dejar escrito. Con 22 años de legajo limpio y a dos años de "
        "jubilarse, sabía que un disparo por maniobra manual fuera de "
        "procedimiento significaba, como mínimo, un sumario, y probablemente "
        "la pérdida de su habilitación de operador senior antes de poder "
        "retirarse con ella. Entre la 01:50 y las 02:00, con la sala de "
        "control ya tranquila y Nadia todavía recomponiéndose de la parada, "
        "entró al registro digital de turno y reescribió el tramo de las "
        "01:41 a las 01:47: cambió el valor registrado de apertura de la "
        "válvula para que pareciera una operación automática normal, y dejó "
        "que el disparo se leyera como causado por una lectura errónea del "
        "sensor de temperatura de salida del núcleo.\n\n"
        "Fue un error de cálculo: el sensor que eligió para cargarle la "
        "culpa era, casualmente, uno que Gustavo Enz —el técnico de "
        "instrumentación— había calibrado y probado esa misma mañana, sin "
        "encontrarle nada raro. Cuando el ingeniero de turno del día cruzó "
        "esa calibración con el relato oficial del «sensor fallado», la "
        "historia dejó de cerrar.\n\n"
        "Un operador que evitó un incidente real, y que casi provoca uno "
        "peor tratando de borrar que había sido él quien lo causó."
    ),
    max_preguntas=15,
    sospechosos=[
        Sospechoso(
            id="ricardo",
            nombre="Ricardo Aballay",
            cargo="jefe de turno de operación",
            color="bright_blue",
            es_culpable=True,
            personalidad=(
                "Veterano con 22 años en el reactor, orgulloso de un legajo sin "
                "un solo incidente. Habla con la calma de quien ha visto de "
                "todo, cita el procedimiento de memoria y trata a los más "
                "jóvenes con una mezcla de afecto y autoridad. Nunca levanta "
                "la voz. Hasta que lo acorralan."
            ),
            coartada=(
                "Dice que el ensayo se hizo al pie de la letra del "
                "procedimiento y que la parada automática fue, lisa y "
                "llanamente, un fallo de instrumentación: el sensor de "
                "temperatura de salida dio una lectura errónea."
            ),
            actitud=(
                "Tranquilo y técnico al principio, casi paternal. Si lo "
                "presionan en general, se aferra a la explicación del sensor y "
                "a su historial impecable. Pero si lo confrontan con algo "
                "puntual —el tramo editado del registro, el timing de la "
                "válvula, o el estado real del sensor— se pone rígido, repite "
                "la misma frase dos veces y, si insisten, se quiebra."
            ),
            secretos=[
                Secreto(
                    id="maniobra_manual",
                    pista=(
                        "Cerca de la 01:40, Ricardo cerró manualmente una "
                        "válvula de caudal del circuito secundario sin "
                        "completar la secuencia de verificación que exige el "
                        "procedimiento del ensayo."
                    ),
                    instruccion_actor=(
                        "Al principio negás cualquier maniobra fuera de "
                        "procedimiento («todo se hizo como corresponde»). "
                        "Solo si te preguntan puntualmente por la válvula del "
                        "circuito secundario, por qué el rebalanceo de caudal "
                        "no siguió la secuencia normal, o por lo que hiciste "
                        "vos mismo esa madrugada entre la 01:30 y la 01:47: "
                        "admitís, incómodo, que cerraste la válvula a mano "
                        "para adelantar la secuencia, algo que habías hecho "
                        "antes sin problema."
                    ),
                    criterio_revelacion=(
                        "Admite que operó manualmente una válvula del "
                        "circuito secundario fuera de la secuencia del "
                        "procedimiento, sin esperar la verificación automática."
                    ),
                ),
                Secreto(
                    id="bitacora_editada",
                    pista=(
                        "El tramo del registro de turno entre la 01:41 y la "
                        "01:47 fue reescrito después del hecho: fue Ricardo "
                        "quien entró al sistema, poco después de la parada, y "
                        "cambió el valor de apertura de la válvula registrado."
                    ),
                    instruccion_actor=(
                        "Este es el secreto que más te cuesta soltar. Jamás lo "
                        "mencionás espontáneamente. Solo si te confrontan con "
                        "algo concreto sobre el registro editado —que el "
                        "sistema marca quién y cuándo lo modificó, que el "
                        "tramo de las 01:41 a las 01:47 fue sobreescrito, o "
                        "una contradicción directa entre tu maniobra manual y "
                        "lo que dice la bitácora oficial— te quebrás y "
                        "confesás que entraste al registro después de la "
                        "parada y cambiaste el valor de la válvula para que "
                        "pareciera una operación automática."
                    ),
                    criterio_revelacion=(
                        "Confiesa haber alterado o \"corregido\" el registro "
                        "digital de turno esa madrugada, específicamente el "
                        "valor de apertura de la válvula."
                    ),
                ),
                Secreto(
                    id="miedo_habilitacion",
                    pista=(
                        "Ricardo está a dos años de jubilarse. Un disparo "
                        "atribuido a una maniobra manual fuera de "
                        "procedimiento le habría costado, como mínimo, un "
                        "sumario, y probablemente la pérdida de su "
                        "habilitación de operador senior."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por qué alguien haría algo así, por "
                        "tu situación laboral, por tu jubilación, o "
                        "directamente por qué editarías un registro: bajás la "
                        "guardia y confesás, con la voz quebrada, el miedo a "
                        "perder tu habilitación después de 22 años de legajo "
                        "limpio, a dos años de retirarte."
                    ),
                    criterio_revelacion=(
                        "Menciona el miedo a perder su habilitación u "
                        "operador senior, o a arruinar su carrera justo antes "
                        "de jubilarse."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="nadia",
            nombre="Nadia Chapare",
            cargo="operadora de guardia",
            color="bright_green",
            personalidad=(
                "Treinta y dos años, cinco en la sala de control, meticulosa "
                "hasta la obsesión con los checklists. Habla rápido cuando "
                "está nerviosa y se disculpa por cosas que no hizo. Le tiene "
                "un respeto casi reverencial a Ricardo, lo que le complica "
                "decir que vio algo raro de su parte."
            ),
            coartada=(
                "Dice que estuvo toda la madrugada en la consola, "
                "registrando parámetros como corresponde, y que la parada "
                "fue una sorpresa total: «el sistema hizo lo que tenía que "
                "hacer»."
            ),
            actitud=(
                "A la defensiva enseguida, tartamudea si siente que la "
                "acusan. Si le marcan una contradicción puntual —un hueco en "
                "el registro de horarios, algo que no dijo antes— se "
                "derrumba rápido y confiesa, aliviada de sacárselo de encima."
            ),
            secretos=[
                Secreto(
                    id="aviso_omitido",
                    pista=(
                        "Nadia vio subir la temperatura de salida del núcleo "
                        "minutos antes del disparo y no dijo nada, porque no "
                        "quiso cuestionar a Ricardo delante de todos."
                    ),
                    instruccion_actor=(
                        "Solo si te preguntan directamente si notaste algo "
                        "raro antes de la parada, o si viste subir la "
                        "temperatura antes del disparo: confesás, avergonzada, "
                        "que sí, viste la tendencia subir en la consola unos "
                        "minutos antes, pero no dijiste nada porque no "
                        "quisiste cuestionar a tu jefe de turno delante de "
                        "todos."
                    ),
                    criterio_revelacion=(
                        "Admite haber notado el aumento de temperatura antes "
                        "del disparo y no haberlo alertado por no querer "
                        "confrontar a Ricardo."
                    ),
                ),
                Secreto(
                    id="salio_de_sala",
                    pista=(
                        "Nadia se ausentó unos minutos de la sala de control "
                        "durante el ensayo —fue al baño—, algo que el "
                        "procedimiento prohíbe expresamente durante una "
                        "prueba activa."
                    ),
                    instruccion_actor=(
                        "Al principio negás haberte movido de tu puesto "
                        "(«estuve en la consola toda la noche»). Si te "
                        "presionan sobre si estuviste todo el tiempo ahí, o "
                        "te marcan un hueco en el registro de horarios: "
                        "confesás que saliste un par de minutos al baño, y "
                        "jurás que no tiene nada que ver con lo que pasó "
                        "después."
                    ),
                    criterio_revelacion=(
                        "Admite haberse ausentado brevemente de la sala de "
                        "control durante el ensayo."
                    ),
                ),
                Secreto(
                    id="roce_previo",
                    pista=(
                        "Meses atrás, Nadia ya había reportado que Ricardo se "
                        "saltaba pasos de un checklist en otro ensayo; el "
                        "reporte quedó informal y sin consecuencias."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por tu relación con Ricardo, o si "
                        "alguna vez viste algo irregular de su parte antes de "
                        "esta noche: contás, incómoda, que meses atrás ya le "
                        "habías marcado que se saltaba pasos del checklist en "
                        "otro ensayo, y que nadie le dio seguimiento formal al "
                        "reporte."
                    ),
                    criterio_revelacion=(
                        "Cuenta que había reportado antes que Ricardo se "
                        "saltaba procedimientos y que no hubo consecuencias."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="gustavo",
            nombre="Gustavo Enz",
            cargo="técnico de instrumentación y control (guardia pasiva)",
            color="bright_yellow",
            personalidad=(
                "Cincuenta y pico, de pocas palabras, más cómodo hablando de "
                "sensores que de personas. Meticuloso con los números, "
                "incómodo con las preguntas que no tienen una respuesta "
                "técnica. Tiene sus propias costumbres de andar por casa que "
                "preferiría no explicar."
            ),
            coartada=(
                "Dice que esa noche estaba en su casa, de guardia pasiva, y "
                "que lo único que hizo fue una revisión remota corta cuando "
                "lo llamaron por la lectura de temperatura."
            ),
            actitud=(
                "Parco y evasivo con lo personal, pero no puede evitar "
                "ponerse técnico y preciso apenas le tocan un tema de "
                "instrumentos —ahí suelta más de lo que quiere. Si le "
                "insisten con sospecha sobre por qué le incomoda hablar de "
                "\"editar registros\" en general, termina confesando su "
                "propia manía menor."
            ),
            secretos=[
                Secreto(
                    id="acceso_remoto",
                    pista=(
                        "Gustavo se conectó remotamente al sistema de control "
                        "y registro esa madrugada, a las 02:10, usando sus "
                        "credenciales de mantenimiento."
                    ),
                    instruccion_actor=(
                        "Al principio decís que no tocaste nada esa noche, "
                        "que dormías en tu casa. Solo si te preguntan "
                        "directamente por accesos remotos, o por qué tus "
                        "credenciales aparecen en el sistema esa madrugada: "
                        "admitís que te llamaron a las 02:10 para revisar a "
                        "distancia una lectura de temperatura, y que entraste "
                        "al sistema con tu usuario un par de minutos."
                    ),
                    criterio_revelacion=(
                        "Admite haberse conectado remotamente al sistema de "
                        "registro o control esa madrugada."
                    ),
                ),
                Secreto(
                    id="sensor_no_fallo",
                    pista=(
                        "El sensor de temperatura señalado como responsable "
                        "de la anomalía fue calibrado y probado por Gustavo "
                        "esa misma mañana: funciona perfecto, sin ninguna "
                        "falla."
                    ),
                    instruccion_actor=(
                        "Solo si te preguntan específicamente por el estado "
                        "del sensor de temperatura de salida del núcleo, o si "
                        "confirmás la explicación oficial del \"fallo de "
                        "instrumentación\": contás, con extrañeza técnica, "
                        "que lo revisaste y calibraste vos mismo esa mañana y "
                        "que no tiene ninguna falla, que es rarísimo que "
                        "hayan dicho eso."
                    ),
                    criterio_revelacion=(
                        "Revela que el sensor señalado como fallado fue "
                        "probado o calibrado y no presenta ninguna falla."
                    ),
                ),
                Secreto(
                    id="historial_ediciones",
                    pista=(
                        "Gustavo tiene la costumbre de corregir con fecha "
                        "retroactiva pequeños registros de calibración cuando "
                        "se olvida de cargarlos a tiempo: una práctica menor, "
                        "pero fuera de norma."
                    ),
                    instruccion_actor=(
                        "Si te preguntan, con insistencia o sospecha, por qué "
                        "te pone tan nervioso el tema de \"editar registros\" "
                        "en general, o si alguna vez modificaste una fecha en "
                        "el sistema: confesás, incómodo, que a veces cargás "
                        "calibraciones con fecha retroactiva cuando se te "
                        "pasa el momento, una mala costumbre que no tiene "
                        "nada que ver con lo de esa noche."
                    ),
                    criterio_revelacion=(
                        "Admite haber alterado fechas o registros de "
                        "calibración en otras ocasiones, como una práctica "
                        "menor no relacionada con el incidente de esa noche."
                    ),
                ),
            ],
        ),
    ],
)
