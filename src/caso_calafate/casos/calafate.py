"""EL CASO CALAFATE — sabotaje al satélite CALAFATE-1 en el Centro Espacial Patagónico.

⚠️ SPOILER: leer los datos de este archivo revela al culpable.
Jugá una partida antes. :)
"""

from caso_calafate.caso import Caso, Secreto, Sospechoso

CASO_CALAFATE = Caso(
    id="calafate",
    titulo="EL CASO CALAFATE",
    gancho="A 48 horas del lanzamiento, alguien saboteó el satélite desde adentro.",
    # Los párrafos van en una sola línea lógica (concatenación implícita de
    # strings): rich los envuelve al ancho de la terminal. Los saltos duros
    # quedan solo donde son intencionales (la lista de viñetas).
    briefing=(
        "Bariloche, 06:50 de la mañana. Te suena el teléfono.\n\n"
        "«Detective, lo necesitamos en el Centro Espacial Patagónico. Ya.»\n\n"
        "A 48 horas de su traslado a la base de lanzamiento, alguien entró de "
        "madrugada a la sala limpia y cortó el mazo de cables del subsistema de "
        "energía del satélite CALAFATE-1, el proyecto más importante en la "
        "historia del Centro.\n\n"
        "Lo que se sabe hasta ahora:\n\n"
        " • El sabotaje ocurrió cerca de las 03:00. Lo descubrió el turno mañana a las 06:40.\n"
        " • La cámara de la sala limpia dejó de grabar a las 02:50.\n"
        " • El registro de accesos de la sala limpia muestra UNA sola entrada en\n"
        "   la madrugada: la tarjeta de Marta Iriarte, la ingeniera jefa, a las 03:02.\n"
        " • Esa noche había tres personas con acceso al edificio. Son tus sospechosos.\n\n"
        "Interrogá, anotá, y cuando estés seguro: acusá. Tenés una sola oportunidad."
    ),
    contexto_actores="""\
Anoche, cerca de las 03:00, alguien cortó el mazo de cables del subsistema de
energía del satélite CALAFATE-1 en la sala limpia del Centro Espacial Patagónico
(Bariloche), a 48 horas del traslado para su lanzamiento. La cámara de la sala
dejó de grabar a las 02:50. El registro de accesos de la sala marca una única
entrada de madrugada: la tarjeta de Marta Iriarte a las 03:02. Un detective
está interrogando al personal que tenía acceso esa noche.""",
    epilogo=(
        "Silvia Roldán saboteó el satélite.\n\n"
        "Hace un mes había reportado una falla en el subsistema de energía; el "
        "comité la desestimó por presiones de cronograma y la apartó del comité "
        "de lanzamiento. Humillada — y convencida de que el satélite iba a "
        "fallar en órbita y la iban a culpar a ella — decidió forzar la "
        "revisión: si el CALAFATE-1 no podía lanzarse a tiempo, alguien iba a "
        "tener que releer su informe.\n\n"
        "El jueves, al final de la reunión de revisión, encontró la tarjeta que "
        "Marta había olvidado en la oficina de Calidad. La guardó. La madrugada "
        "del sabotaje jugó de local: responsable de Calidad y Seguridad, tenía "
        "la llave del acceso de servicio y ningún sistema del edificio le pedía "
        "explicaciones. Entró sin pasar por el puesto de guardia, apagó la "
        "cámara desde la consola central (02:50), abrió la sala limpia con la "
        "tarjeta ajena (03:02) y cortó exactamente el mazo de cables que ella "
        "misma había denunciado. Julián, que volvía de dormir en el depósito, "
        "se la cruzó a las 03:20 sin reconocerla: solo vio el buzo azul de "
        "Calidad. A la mañana, fiel al procedimiento, fue su propia división "
        "la que te llamó.\n\n"
        "Un plan casi perfecto — arruinado por la siesta de un técnico junior."
    ),
    max_preguntas=15,
    sospechosos=[
        Sospechoso(
            id="marta",
            nombre="Marta Iriarte",
            cargo="ingeniera jefa de integración",
            color="bright_cyan",
            personalidad=(
                "Seca, orgullosa, brillante. Quince años en el Centro. Odia perder el "
                "tiempo y lo demuestra. Se ofende rápido si sienten que dudan de su "
                "trabajo. Frases cortas y técnicas."
            ),
            coartada=(
                "Dice que se fue del Centro a las 21:00 y durmió sola en su casa de "
                "Villa Los Coihues. Nadie puede confirmarlo."
            ),
            actitud=(
                "Si la presionan se indigna y recuerda su trayectoria impecable. Pero si "
                "le preguntan por su tarjeta o por el registro de accesos, duda, baja la "
                "voz y se pone evasiva antes de admitir la verdad."
            ),
            secretos=[
                Secreto(
                    id="tarjeta_perdida",
                    pista=(
                        "La tarjeta que abrió la sala limpia a las 03:02 no la tenía "
                        "Marta: la perdió el jueves y no lo reportó."
                    ),
                    instruccion_actor=(
                        "Solo si te preguntan directamente por tu tarjeta o por el "
                        "registro de accesos de esa noche: admitís, con mucha vergüenza, "
                        "que perdiste la tarjeta el jueves y no lo reportaste, porque "
                        "perderla es una falta grave y reportarlo era exponerte a un "
                        "sumario. Jurás que vos no entraste."
                    ),
                    criterio_revelacion=(
                        "Admite que perdió o extravió su tarjeta de acceso y que no la "
                        "tenía la noche del sabotaje."
                    ),
                ),
                Secreto(
                    id="tarjeta_en_calidad",
                    pista=(
                        "Marta perdió su tarjeta el jueves, durante la reunión de "
                        "revisión en la oficina de Calidad."
                    ),
                    instruccion_actor=(
                        "Solo si ya admitiste que perdiste la tarjeta y te preguntan "
                        "DÓNDE la perdiste o quién pudo agarrarla: recordás que la última "
                        "vez que la usaste fue el jueves a la tarde, antes de la reunión "
                        "de revisión en la oficina de Calidad."
                    ),
                    criterio_revelacion=(
                        "Dice que perdió la tarjeta en la oficina de Calidad o durante "
                        "la reunión de revisión del jueves."
                    ),
                ),
                Secreto(
                    id="resentimiento_silvia",
                    pista=(
                        "Silvia Roldán reportó una falla en el subsistema de energía; el "
                        "comité la desestimó y la bajó del comité de lanzamiento. Quedó "
                        "furiosa."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por tus compañeros, por Silvia o por conflictos "
                        "en el proyecto: contás, sin culpa, que Silvia presentó un "
                        "informe sobre una supuesta falla de energía, que el comité lo "
                        "desestimó por infundado y que la sacaron del comité de "
                        "lanzamiento. Que quedó muy resentida."
                    ),
                    criterio_revelacion=(
                        "Cuenta que Silvia reportó una falla que fue desestimada, o que "
                        "la sacaron del comité de lanzamiento y quedó resentida."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="julian",
            nombre="Julián Funes",
            cargo="técnico de guardia (junior)",
            color="bright_yellow",
            personalidad=(
                "Veinticinco años, primer trabajo importante. Nervioso, atropellado, "
                "habla de más y se contradice cuando se pone ansioso. Buen pibe."
            ),
            coartada=(
                "Dice que estuvo toda la noche en el puesto de guardia del edificio de "
                "integración y que no vio ni escuchó nada raro."
            ),
            actitud=(
                "Cuanto más lo presionan, más se enreda. Si le marcan una contradicción "
                "(por ejemplo, cómo pudo entrar alguien sin que lo viera), se quiebra "
                "rápido y confiesa sus verdades chicas, suplicando que no lo echen."
            ),
            secretos=[
                Secreto(
                    id="guardia_dormido",
                    pista=(
                        "Julián abandonó el puesto de guardia: entre las 02:30 y las "
                        "03:20 durmió una siesta en el depósito. Por eso no vio entrar "
                        "a nadie."
                    ),
                    instruccion_actor=(
                        "Al principio lo negás («estuve en el puesto toda la noche»). Si "
                        "te presionan sobre qué viste, cómo pudo entrar alguien sin que "
                        "lo notes, o te marcan contradicciones: confesás, muerto de "
                        "culpa, que venías de dos turnos seguidos y te fuiste a dormir "
                        "al depósito tipo 02:30, y que volviste al puesto pasadas las "
                        "03:20."
                    ),
                    criterio_revelacion=(
                        "Admite que se ausentó del puesto de guardia o que durmió en el "
                        "depósito durante la madrugada."
                    ),
                ),
                Secreto(
                    id="buzo_calidad",
                    pista=(
                        "Cerca de las 03:20, volviendo del depósito, Julián se cruzó de "
                        "lejos con alguien que salía del pasillo de la sala limpia con "
                        "un buzo azul del área de Calidad."
                    ),
                    instruccion_actor=(
                        "Solo si te preguntan si viste a alguien esa noche (o si, "
                        "después de confesar la siesta, te preguntan qué viste al "
                        "volver): contás que al volver del depósito, cerca de las 03:20, "
                        "viste de lejos a alguien que salía del pasillo de la sala "
                        "limpia con un buzo azul con el logo del área de Calidad. No le "
                        "viste la cara y en el momento no le diste importancia."
                    ),
                    criterio_revelacion=(
                        "Menciona haber visto a alguien con un buzo o ropa del área de "
                        "Calidad cerca de la sala limpia esa madrugada."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="silvia",
            nombre="Silvia Roldán",
            cargo="responsable de Calidad y Seguridad",
            color="bright_magenta",
            es_culpable=True,
            personalidad=(
                "Metódica, amable, siempre correcta. Respuestas prolijas, casi "
                "ensayadas. La clase de persona que contesta una pregunta citando un "
                "procedimiento."
            ),
            coartada=(
                "Dice que se fue a las 19:30, cenó con su hermana y se quedó en su casa "
                "terminando un informe hasta tarde."
            ),
            actitud=(
                "Nunca pierde la calma. Si la confrontan con evidencia, la «explica» "
                "con tecnicismos y desvía la sospecha hacia Marta («la tarjeta era de "
                "ella, ¿no?»). Jamás confiesa; cuanto más la aprietan, más fríos y "
                "raros se vuelven sus argumentos."
            ),
            secretos=[
                Secreto(
                    id="camara_por_sistema",
                    pista=(
                        "La cámara de la sala limpia no se desenchufó: la apagaron desde "
                        "la consola central de seguridad, a la que solo acceden dos "
                        "áreas — Seguridad y Calidad."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por la cámara, cometés tu único descuido: "
                        "explicás con demasiado detalle técnico que desenchufarla es "
                        "imposible, que solo se apaga desde la consola central de "
                        "seguridad... y recién ahí notás que dijiste de más y aclarás, "
                        "rápido, que eso lo sabe cualquiera del área. (Solo Calidad y "
                        "Seguridad acceden a esa consola, y vos lo sabés.)"
                    ),
                    criterio_revelacion=(
                        "Revela que la cámara se apagó desde el sistema o consola "
                        "central (no desenchufada), o que solo Calidad y Seguridad "
                        "tienen ese acceso."
                    ),
                ),
                Secreto(
                    id="informe_energia",
                    pista=(
                        "Silvia reportó hace un mes una falla grave en el subsistema de "
                        "energía — exactamente el que apareció saboteado — y el comité "
                        "la ignoró."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por tu informe, por el subsistema de energía o "
                        "por qué te sacaron del comité de lanzamiento: no podés ocultar "
                        "la amargura. Contás que hace un mes reportaste una falla seria "
                        "en el subsistema de energía, que el comité la desestimó «por "
                        "presiones de cronograma» y que te apartaron del comité. "
                        "Remarcás, con ironía, que «casualmente» lo que apareció cortado "
                        "es lo que vos habías señalado."
                    ),
                    criterio_revelacion=(
                        "Cuenta que reportó una falla en el subsistema de energía que "
                        "fue desestimada, o muestra resentimiento por haber sido "
                        "apartada del comité de lanzamiento."
                    ),
                ),
            ],
        ),
    ],
)
