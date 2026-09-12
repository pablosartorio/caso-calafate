"""EL CASO LLAO LLAO — homenaje a Emilio "Tata" Roitberg (El Oso / Patagonia Noir).

Un robo en plena temporada de esquí, disfrazado de fauna: la Patagonia como
paisaje que devuelve una amenaza falsa para tapar una humana.

⚠️ SPOILER: leer los datos de este archivo revela al culpable.
Jugá una partida antes. :)
"""

from caso_calafate.caso import Caso, Secreto, Sospechoso

CASO_LLAO_LLAO = Caso(
    id="llaollao",
    titulo="EL CASO LLAO LLAO",
    sede="Anexo del Centro Espacial Patagónico en Llao Llao",
    ciudad="Bariloche",
    delito="el sabotaje del galpón de repuestos satelitales",
    culpable_alias="saboteador",
    gancho=(
        "En plena temporada de esquí alguien forzó el galpón de repuestos — y dejó "
        "huellas de oso demasiado prolijas para ser reales."
    ),
    briefing=(
        "Bariloche, temporada alta de esquí. Te suena el teléfono a las 07:15.\n\n"
        "«Detective, lo necesitamos en el anexo de Llao Llao. Alguien entró al "
        "galpón de repuestos y esto no lo hizo un animal.»\n\n"
        "Durante la noche forzaron el galpón de repuestos del anexo del Centro "
        "Espacial en Llao Llao. Faltan piezas de un satélite meteorológico. En el "
        "barro, alrededor del galpón, hay huellas de oso — pero al guardaparques de "
        "la zona no le cierran: son parejas, muy regulares, como hechas con un "
        "molde.\n\n"
        "Lo que se sabe hasta ahora:\n\n"
        " • El galpón se forzó entre la 01:00 y las 03:00.\n"
        " • La alarma perimetral no sonó: la desactivaron desde el sistema, no la\n"
        "   cortaron.\n"
        " • Las huellas de oso empiezan justo en el límite del alcance de la\n"
        "   cámara y se pierden en la ruta — ningún rastro real se corta así.\n"
        " • Cinco personas tenían llave o acceso al sistema de alarma esa noche.\n"
        "   Son tus sospechosos.\n\n"
        "Interrogá, anotá, y cuando estés seguro: acusá. Tenés una sola oportunidad."
    ),
    contexto_actores="""\
Anoche, entre la 01:00 y las 03:00, forzaron el galpón de repuestos del anexo
del Centro Espacial en Llao Llao (Bariloche) y faltan piezas de un satélite
meteorológico. La alarma perimetral fue desactivada desde el sistema, no
cortada. Alrededor del galpón hay huellas de oso demasiado regulares para ser
reales, que empiezan justo donde termina el alcance de la cámara. Un detective
está interrogando a las cinco personas con llave o acceso al sistema esa
noche.""",
    epilogo=(
        "Dino Filipich forzó el galpón y fabricó las huellas.\n\n"
        "Su refugio de montaña le debe tres temporadas de alquiler al Centro, que "
        "le cede el terreno desde los años 90. Con la deuda a punto de rescindirle "
        "el contrato, vio en el galpón una salida: piezas de repuesto satelital se "
        "revenden bien en el mercado gris de electrónica de Chile. Conocía el "
        "predio de memoria — llevaba huéspedes a caminar por ahí — y sabía que el "
        "guardaparques Aballay andaba detrás de un oso real esa semana, así que "
        "compró un molde de huellas en una casa de disfraces de Bariloche y las "
        "marcó él mismo en el barro, calculando mal el alcance de la cámara: las "
        "suyas arrancan exactamente donde el lente deja de ver, ni un metro antes.\n\n"
        "Coty Ibarra vio algo esa noche — una camioneta conocida saliendo del "
        "camino de servicio — pero se guardó el dato: Dino le hacía descuentos en "
        "el refugio a cambio de no reportar sus llegadas tarde al turno.\n\n"
        "El oso real que rastreaba Aballay, dicho sea de paso, nunca estuvo cerca "
        "del galpón."
    ),
    max_preguntas=15,
    sospechosos=[
        Sospechoso(
            id="rutty",
            nombre="Rutty Aballay",
            cargo="guardaparques",
            color="green",
            personalidad=(
                "Parca, observadora, más cómoda con el monte que con la gente. "
                "Desconfía de cualquiera que hable de fauna sin conocerla. Lleva "
                "años peleando para que no se culpe a un animal real por cada "
                "problema humano de la zona, y una huella fabricada la ofende "
                "casi tanto como el robo mismo: es su trabajo el que queda en "
                "ridículo cada vez que alguien prefiere creer en un oso antes "
                "que investigar a un vecino."
            ),
            coartada=(
                "Dice que esa noche estaba rastreando a un oso real varios kilómetros "
                "al norte del galpón, sola, con la radio apagada para no espantarlo."
            ),
            actitud=(
                "Responde con hechos de campo, nunca con opiniones sobre la gente. Si "
                "la presionan sobre las huellas, se pone técnica y contundente: "
                "necesita que le muestren evidencia, no le alcanza con sospechar."
            ),
            secretos=[
                Secreto(
                    id="huellas_falsas",
                    pista=(
                        "Las huellas de oso son un fraude: tienen un patrón de garras "
                        "idéntico en las cuatro, algo imposible en un animal real."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por las huellas: explicás, con autoridad "
                        "profesional, que las cuatro tienen exactamente el mismo "
                        "patrón de garras — un oso real nunca pisa igual dos veces. "
                        "Son un molde."
                    ),
                    criterio_revelacion=(
                        "Explica que las huellas son falsas o fabricadas con un molde, "
                        "por tener un patrón repetido o antinatural."
                    ),
                    es_entrada=True,
                    certeza="parcial",
                ),
            ],
            reaccion_acusacion_fallida=(
                "Detienen a Rutty por saber demasiado de huellas; el oso real "
                "que rastreaba se pierde monte adentro mientras ella explica, "
                "por décima vez, por qué un animal no pisa siempre igual."
            ),
        ),
        Sospechoso(
            id="dino",
            nombre="Dino Filipich",
            cargo="dueño del refugio de montaña",
            color="red",
            es_culpable=True,
            personalidad=(
                "Simpático, hablador, de esos que conocen a todo el mundo en el "
                "pueblo. Bajo la joda esconde una ansiedad que se le nota en las "
                "manos. Se convence de que el Centro, con todo lo que tiene, no "
                "va a extrañar unas piezas de repuesto tanto como él va a "
                "extrañar el refugio que heredó de su viejo si se lo rescinden — "
                "y de que un molde de huellas es apenas una travesura de "
                "pueblo, no un delito de verdad."
            ),
            coartada=(
                "Dice que esa noche cerró el refugio a las 23:00 y se quedó durmiendo "
                "en la habitación de arriba, como todas las noches de temporada."
            ),
            actitud=(
                "Desvía con chistes y anécdotas del pueblo. Si lo acorralan con un "
                "dato concreto, se queda callado un segundo de más antes de reírse "
                "y cambiar de tema — ahí se le nota."
            ),
            secretos=[
                Secreto(
                    id="deuda_refugio",
                    pista=(
                        "El refugio de Dino le debe al Centro tres temporadas de "
                        "alquiler del terreno; estaban por rescindirle el contrato."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por la plata del refugio o por el contrato "
                        "con el Centro: admitís, incómodo, que debés tres temporadas "
                        "y que la administración ya te mandó un último aviso."
                    ),
                    criterio_revelacion=(
                        "Admite que debe alquiler o que están por rescindirle el "
                        "contrato del terreno."
                    ),
                    es_entrada=True,
                    certeza="parcial",
                ),
                Secreto(
                    id="molde_disfraces",
                    pista=(
                        "Dino compró un molde de huellas de oso en una casa de "
                        "disfraces de Bariloche la semana del sabotaje."
                    ),
                    instruccion_actor=(
                        "Solo si ya te acorralaron con la deuda Y te preguntan "
                        "directamente por las huellas o por qué las conocía tan bien: "
                        "te quebrás y contás que compró el molde en una casa de "
                        "disfraces, 'solo para asustar a un huésped pesado', y que se "
                        "le fue de las manos."
                    ),
                    criterio_revelacion=(
                        "Admite haber comprado o fabricado un molde de huellas de oso."
                    ),
                    certeza="confirmado",
                ),
            ],
            reaccion_acusacion_fallida=(
                "Si por algún error no lo acusan a él, Dino reabre el refugio "
                "la temporada que viene como si la deuda se hubiera arreglado "
                "sola."
            ),
        ),
        Sospechoso(
            id="coty",
            nombre="Coty Ibarra",
            cargo="técnica de telemetría",
            color="cyan",
            personalidad=(
                "Cumplidora, callada, de las que anotan todo en un cuaderno propio "
                "porque no confían en el sistema. Muy leal a quien le hace un favor "
                "— sostiene sola el alquiler de su casa desde que se separó, y el "
                "descuento de Dino en el refugio es, calladamente, lo que le "
                "permite llegar a fin de mes sin pedirle nada a nadie más."
            ),
            coartada=(
                "Dice que estaba en su turno de noche en la sala de telemetría, sola, "
                "monitoreando una pasada satelital sin novedades."
            ),
            actitud=(
                "Responde corto y mira para abajo. No miente sobre su propio turno, "
                "pero se pone visiblemente incómoda si le preguntan qué vio afuera."
            ),
            secretos=[
                Secreto(
                    id="camioneta_dino",
                    pista=(
                        "Coty vio la camioneta de Dino Filipich saliendo del camino de "
                        "servicio esa madrugada, pero no lo reportó."
                    ),
                    instruccion_actor=(
                        "Si te preguntan qué viste esa noche, aunque sea de forma "
                        "general: confesás, con culpa, que viste la camioneta de "
                        "Dino saliendo del camino de servicio cerca de las 02:00, "
                        "y que no dijiste nada porque él te hace descuentos en el "
                        "refugio."
                    ),
                    criterio_revelacion=(
                        "Revela haber visto la camioneta de Dino Filipich esa "
                        "madrugada y no haberlo reportado."
                    ),
                    es_entrada=True,
                    certeza="confirmado",
                ),
            ],
            reaccion_acusacion_fallida=(
                "Detienen a Coty por callar lo que vio; pierde el descuento en "
                "el refugio y, esta vez, con motivo."
            ),
        ),
        Sospechoso(
            id="bagu",
            nombre="Comisario Bagú",
            cargo="jefe de la comisaría de Llao Llao",
            color="yellow",
            personalidad=(
                "Cansado, con veinte años en el cargo y ganas de que todo se resuelva "
                "rápido y sin papelerío. Amigo de medio pueblo, incluido el "
                "intendente. Le quedan pocos años para el retiro y lo único que "
                "quiere es llegar sin un escándalo que le manche el expediente — "
                "cerrar rápido, aunque sea mal, le resulta menos peligroso que "
                "investigar bien y hacerse un enemigo con poder."
            ),
            coartada=(
                "Dice que esa noche estaba de guardia en la comisaría, a diez "
                "kilómetros, y que se enteró del sabotaje recién a la mañana."
            ),
            actitud=(
                "Trata de cerrar la conversación rápido, sugiriendo que 'seguro fue "
                "un animal' aunque nadie se lo pregunte. Si insisten, se pone a la "
                "defensiva por su propio trabajo, no por el caso."
            ),
            secretos=[
                Secreto(
                    id="presion_cerrar",
                    pista=(
                        "El intendente le pidió a Bagú que cierre el caso como 'ataque "
                        "de fauna' antes del fin de semana largo, para no espantar "
                        "turistas."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por qué no investigaste más las huellas: "
                        "admitís, resignado, que el intendente te pidió cerrarlo como "
                        "fauna antes del fin de semana largo, para no espantar al "
                        "turismo."
                    ),
                    criterio_revelacion=(
                        "Admite presión del intendente para cerrar el caso como "
                        "ataque de fauna."
                    ),
                    es_entrada=True,
                ),
            ],
            reaccion_acusacion_fallida=(
                "Detienen al comisario Bagú por no investigar más las huellas; "
                "el intendente igual consigue su fin de semana largo sin "
                "sobresaltos."
            ),
        ),
        Sospechoso(
            id="vera",
            nombre="Vera Roitman",
            cargo="periodista freelance",
            color="magenta",
            personalidad=(
                "Curiosa, directa, acostumbrada a que le cierren puertas en la cara. "
                "Investigaba antes de esto un contrato municipal, no el sabotaje. "
                "Lleva dos años freelanceando de nota en nota sin firmar nada que "
                "le importe de verdad, y esta historia —empiece donde empiece— es "
                "la primera en mucho tiempo que siente que vale la pena perseguir "
                "hasta el final, aunque eso implique quedar mal con medio pueblo."
            ),
            coartada=(
                "Dice que esa noche estaba en el hotel, revisando facturas del "
                "municipio para una nota, y que un mozo puede confirmar que cenó ahí."
            ),
            actitud=(
                "Contesta con preguntas propias antes de responder las tuyas. Si le "
                "muestran que coopera, se abre y comparte lo que investigaba."
            ),
            secretos=[
                Secreto(
                    id="contrato_terreno",
                    pista=(
                        "Vera investigaba un contrato irregular entre la municipalidad "
                        "y el refugio de Dino Filipich por el uso del terreno."
                    ),
                    instruccion_actor=(
                        "Si te preguntan qué investigabas o por qué estabas en la "
                        "zona: contás que seguís la pista de un contrato irregular "
                        "entre el municipio y el refugio de Dino por el terreno, y "
                        "que hay plata que no cierra."
                    ),
                    criterio_revelacion=(
                        "Cuenta que investigaba un contrato irregular entre el "
                        "municipio y el refugio de Dino Filipich."
                    ),
                    es_entrada=True,
                    certeza="parcial",
                ),
            ],
            reaccion_acusacion_fallida=(
                "Detienen a Vera por husmear donde no la llamaban; la nota "
                "sobre el contrato del terreno sale igual, ahora con un "
                "párrafo nuevo sobre ella."
            ),
        ),
    ],
)
