"""EL CASO ROCA — homenaje a Raúl Argemí (noir político del Alto Valle de Río Negro).

La política y la memoria de los 70 pesan sobre todos los personajes, pero el
motivo real — como en Argemí — termina siendo mucho más terrenal: la plata.

⚠️ SPOILER: leer los datos de este archivo revela al culpable.
Jugá una partida antes. :)
"""

from caso_calafate.caso import Caso, Secreto, Sospechoso

CASO_ROCA = Caso(
    id="roca",
    titulo="EL CASO ROCA",
    sede="Centro de Medicina Nuclear General Roca",
    ciudad="General Roca",
    delito="la sustracción de la fuente de cobalto-60",
    culpable_alias="contrabandista",
    gancho=(
        "En medio de un paro rural, una fuente radiactiva desapareció del "
        "Centro por unas horas — y volvió como si nada."
    ),
    briefing=(
        "General Roca, Alto Valle. Un paro de trabajadores rurales corta la "
        "ruta 22 desde hace tres días. Te llaman a las 09:00.\n\n"
        "«Detective, la fuente de cobalto-60 estuvo fuera del blindaje toda la "
        "noche. Volvió, pero necesitamos saber quién la sacó y por qué.»\n\n"
        "Durante el paro, con la ciudad tensa y la ruta cortada, alguien retiró "
        "del búnker la fuente radiactiva del equipo de radioterapia y la "
        "devolvió antes del amanecer, en su contenedor original, sin daños "
        "visibles.\n\n"
        "Lo que se sabe hasta ahora:\n\n"
        " • El búnker se abrió con la clave correcta, sin forzar la cerradura.\n"
        " • El registro del Centro no marca ningún retiro autorizado esa noche.\n"
        " • Hubo un corte de luz de dos horas por el paro, justo cuando el\n"
        "   sistema de alarma debía estar activo.\n"
        " • Cinco personas tenían la clave del búnker o estaban en el edificio\n"
        "   esa noche. Son tus sospechosos.\n\n"
        "Interrogá, anotá, y cuando estés seguro: acusá. Tenés una sola oportunidad."
    ),
    contexto_actores="""\
Anoche, durante un paro rural que corta la ruta 22, alguien retiró del búnker
del Centro de Medicina Nuclear General Roca la fuente de cobalto-60 del equipo
de radioterapia, y la devolvió antes del amanecer sin daños visibles. El
búnker se abrió con la clave correcta y no hay retiro autorizado registrado.
Hubo un corte de luz de dos horas coincidente con la ventana de la alarma. Un
detective está interrogando a las cinco personas con clave o presencia en el
edificio esa noche.""",
    epilogo=(
        "Bruno Achával sacó la fuente para venderla y se arrepintió a tiempo.\n\n"
        "Gerente de la empacadora de fruta vecina al Centro, estaba ahogado en "
        "deudas por una cosecha perdida y un comprador de contrabando le "
        "ofreció una suma enorme por 'material radiactivo, el que sea'. "
        "Conocía la clave del búnker porque su cuñada, la Dra. Casandra "
        "Lefiman, se la había dictado meses atrás para una guardia de "
        "emergencia. Aprovechó el corte de luz del paro — que él mismo alentó "
        "entre los empacadores para tener cobertura — y sacó la fuente en su "
        "contenedor de plomo original. A último momento, mirando el "
        "contenedor en el baúl de su auto, se dio cuenta de en qué se estaba "
        "metiendo y de a quién podía llegar a lastimar, y la devolvió antes "
        "del amanecer.\n\n"
        "El comisario retirado Sabate, que rondaba el Centro esa noche por "
        "cuentas viejas con la familia Lefiman de la dictadura, no tuvo nada "
        "que ver — pero su sola presencia bastó para que media ciudad "
        "sospechara primero de la política antes que de la plata."
    ),
    max_preguntas=15,
    sospechosos=[
        Sospechoso(
            id="ignacio",
            nombre="Ignacio Weber",
            cargo="delegado sindical rural",
            color="red",
            personalidad=(
                "Combativo, memoria larga, hijo de un desaparecido de la zona. "
                "Desconfía profundamente de cualquier uniforme o cargo oficial."
            ),
            coartada=(
                "Dice que pasó la noche en la carpa del corte de ruta, organizando "
                "los turnos de guardia del paro junto a otros diez compañeros."
            ),
            actitud=(
                "Contesta con firmeza política. Si sienten que lo acusan por su "
                "pasado o el de su familia, se cierra en un silencio duro."
            ),
            secretos=[
                Secreto(
                    id="corte_alentado",
                    pista=(
                        "Los empacadores fueron alentados a extender el corte de "
                        "luz esa noche puntual, aunque no formaba parte del plan "
                        "original del paro."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por el corte de luz de esa noche en "
                        "particular: contás, con algo de sospecha propia, que "
                        "alguien de la empacadora vecina insistió en extender el "
                        "corte esa noche puntual, algo que no estaba en el plan "
                        "del paro."
                    ),
                    criterio_revelacion=(
                        "Cuenta que alguien de la empacadora insistió en extender "
                        "el corte de luz esa noche en particular."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="casandra",
            nombre="Dra. Casandra Lefiman",
            cargo="física médica a cargo de la fuente",
            color="cyan",
            personalidad=(
                "Rigurosa, protectora de su equipo, viene de una familia con "
                "historia política pesada en la región. Muy leal a su cuñado."
            ),
            coartada=(
                "Dice que se quedó en el Centro toda la noche, en la guardia, "
                "monitoreando el corte de luz para que el equipo no se dañara."
            ),
            actitud=(
                "Técnica y clara mientras hablan del equipo. Si le preguntan por "
                "su familia, se pone protectora y corta en seco."
            ),
            secretos=[
                Secreto(
                    id="clave_compartida",
                    pista=(
                        "Casandra le dictó la clave del búnker a su cuñado Bruno "
                        "Achával meses atrás, para una guardia de emergencia."
                    ),
                    instruccion_actor=(
                        "Solo si te preguntan directamente quién más conoce la "
                        "clave del búnker: admitís, incómoda, que se la dictaste "
                        "a tu cuñado Bruno hace meses, para una guardia de "
                        "emergencia en la que vos no pudiste estar."
                    ),
                    criterio_revelacion=(
                        "Admite haberle dado la clave del búnker a Bruno Achával."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="bruno",
            nombre="Bruno Achával",
            cargo="gerente de la empacadora vecina",
            color="yellow",
            es_culpable=True,
            personalidad=(
                "Correcto, ansioso por caer bien, siempre hablando de números y "
                "cosechas. La sonrisa se le tensa cuando el tema es plata."
            ),
            coartada=(
                "Dice que pasó la noche en la empacadora, gestionando el corte de "
                "luz del paro para no perder la cámara de frío de la fruta."
            ),
            actitud=(
                "Cordial hasta que lo tocan con algo financiero. Si lo presionan "
                "sobre deudas o sobre la clave del búnker, tartamudea y se justifica."
            ),
            secretos=[
                Secreto(
                    id="deuda_cosecha",
                    pista=(
                        "Bruno perdió una cosecha entera este año y está ahogado en "
                        "deudas con proveedores."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por la situación financiera de la "
                        "empacadora: admitís, nervioso, que perdiste una cosecha "
                        "entera y que las deudas te están ahogando."
                    ),
                    criterio_revelacion=(
                        "Admite estar ahogado en deudas por una cosecha perdida."
                    ),
                ),
                Secreto(
                    id="comprador_contrabando",
                    pista=(
                        "Un comprador de contrabando le ofreció a Bruno una suma "
                        "enorme por 'material radiactivo, el que sea'."
                    ),
                    instruccion_actor=(
                        "Solo si ya admitiste la deuda Y te preguntan si alguien te "
                        "ofreció algo a cambio de plata rápida: te quebrás y "
                        "contás que un comprador te ofreció una suma enorme por "
                        "'material radiactivo, el que sea', y que por un momento "
                        "lo pensaste en serio."
                    ),
                    criterio_revelacion=(
                        "Admite que un comprador de contrabando le ofreció plata "
                        "por material radiactivo."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="norma",
            nombre="Norma Pichún",
            cargo="enfermera de guardia",
            color="green",
            personalidad=(
                "Observadora, discreta, la que más tiempo lleva trabajando de "
                "noche en el Centro. No le gusta meterse en líos ajenos."
            ),
            coartada=(
                "Dice que hizo su recorrida normal de guardia y no notó nada raro "
                "hasta que se cortó la luz."
            ),
            actitud=(
                "Responde con calma y precisión de enfermera de guardia. Si le "
                "preguntan por ruidos o movimientos, se toma su tiempo para "
                "recordar bien antes de hablar."
            ),
            secretos=[
                Secreto(
                    id="auto_bruno",
                    pista=(
                        "Norma vio el auto de Bruno Achával estacionado cerca del "
                        "búnker durante el corte de luz, algo inusual para esa hora."
                    ),
                    instruccion_actor=(
                        "Si te preguntan qué viste durante el corte de luz: contás "
                        "que notaste el auto de Bruno Achával estacionado cerca del "
                        "búnker, algo raro para esa hora de la noche."
                    ),
                    criterio_revelacion=(
                        "Menciona haber visto el auto de Bruno Achával cerca del "
                        "búnker durante el corte de luz."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="sabate",
            nombre="Comisario retirado Sabate",
            cargo="ex jefe de la comisaría local",
            color="magenta",
            personalidad=(
                "Autoritario por costumbre, de los que todavía se creen con "
                "mando. Tiene cuentas viejas y oscuras con varias familias de la "
                "zona, incluida la de Casandra."
            ),
            coartada=(
                "Dice que rondaba la zona del Centro esa noche 'por costumbre', "
                "vigilando que el paro no se le fuera de las manos a nadie."
            ),
            actitud=(
                "Habla con aire de autoridad pasada. Si le preguntan por su "
                "historia con la familia Lefiman, se pone cortante y amenazante."
            ),
            secretos=[
                Secreto(
                    id="historia_lefiman",
                    pista=(
                        "Sabate tuvo un rol activo en la represión de los 70 contra "
                        "la familia de Casandra Lefiman, y todavía la vigila."
                    ),
                    instruccion_actor=(
                        "Solo si te preguntan directamente por tu historia con la "
                        "familia Lefiman: admitís, sin culpa, que tuviste un rol "
                        "activo en la represión de los 70 contra esa familia, y "
                        "que 'la costumbre' de vigilarlos no se te fue."
                    ),
                    criterio_revelacion=(
                        "Admite haber tenido un rol en la represión de los 70 "
                        "contra la familia Lefiman."
                    ),
                ),
            ],
        ),
    ],
)
