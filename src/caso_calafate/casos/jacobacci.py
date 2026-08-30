"""EL CASO JACOBACCI — homenaje a Ricardo Piglia (Blanco nocturno).

Un forastero con plata aparece muerto en un pueblo chico, y de golpe todos —
comerciantes, socios, autoridades — tenían un motivo económico perfectamente
razonable. El crimen no rompe el orden del pueblo: lo revela.

⚠️ SPOILER: leer los datos de este archivo revela al culpable.
Jugá una partida antes. :)
"""

from caso_calafate.caso import Caso, Secreto, Sospechoso

CASO_JACOBACCI = Caso(
    id="jacobacci",
    titulo="EL CASO JACOBACCI",
    sede="Estación de Ensayo de Radares Jacobacci",
    ciudad="Ingeniero Jacobacci",
    delito="el homicidio del forastero",
    culpable_alias="asesino",
    gancho=(
        "Un forastero con demasiada plata encima aparece muerto en un pueblo "
        "chico — y todos, de golpe, tenían un motivo perfectamente razonable."
    ),
    briefing=(
        "Ingeniero Jacobacci, un pueblo del ferrocarril patagónico. Te llaman "
        "a la madrugada.\n\n"
        "«Detective, un forastero apareció muerto cerca de la Estación de "
        "Ensayo. Tenía una suma de plata encima que nadie en este pueblo "
        "gana en un año.»\n\n"
        "El forastero había llegado hacía tres días, ofreciendo financiar un "
        "sistema de radar experimental de la Estación a cambio de una "
        "participación futura. Apareció muerto anoche, a metros de la única "
        "posada del pueblo.\n\n"
        "Lo que se sabe hasta ahora:\n\n"
        " • Llevaba encima una suma de dinero considerable, que no fue robada.\n"
        " • Había cerrado, o estaba por cerrar, un acuerdo económico con más\n"
        "   de una persona del pueblo.\n"
        " • No hay testigos directos: el pueblo, de noche, se vacía temprano.\n"
        " • Cinco personas tuvieron trato directo con él en sus tres días acá.\n"
        "   Son tus sospechosos.\n\n"
        "Interrogá, anotá, y cuando estés seguro: acusá. Tenés una sola oportunidad."
    ),
    contexto_actores="""\
Un forastero llegó hace tres días a Ingeniero Jacobacci, ofreciendo financiar
un sistema de radar experimental de la Estación de Ensayo a cambio de una
participación futura. Anoche apareció muerto cerca de la única posada del
pueblo, con una suma de dinero encima que no fue robada. No hay testigos
directos. Un detective interroga a las cinco personas que tuvieron trato
directo con él.""",
    epilogo=(
        "El comisario Frutos lo mató por la plata.\n\n"
        "El forastero le había mostrado, en confianza y borracho, dónde "
        "guardaba el dinero que pensaba usar como primer pago del acuerdo con "
        "la Estación — un gesto de generosidad mal calculado en un pueblo "
        "donde Frutos llevaba años cobrando 'protección' a comerciantes sin "
        "que nadie se animara a denunciarlo. Lo citó esa noche con la excusa "
        "de 'arreglar unos papeles municipales' para el acuerdo, y en el "
        "descampado cerca de la posada lo golpeó y le sacó el dinero de "
        "encima — pero al ver que la muerte no iba a poder explicarse como un "
        "simple robo (el resto de sus pertenencias seguía intacto), decidió "
        "dejar la plata puesta a la vista, para que pareciera cualquier cosa "
        "menos un robo, y que la sospecha recayera en los socios económicos "
        "del forastero antes que en él.\n\n"
        "Yolanda Currás, empleada de la Estación, vio la camioneta de Frutos "
        "cerca de la posada esa noche — y calló, porque hace años que Frutos "
        "'perdona' las multas de tránsito de su familia."
    ),
    max_preguntas=15,
    sospechosos=[
        Sospechoso(
            id="delfina",
            nombre="Delfina Aguirre",
            cargo="dueña de la única posada del pueblo",
            color="cyan",
            personalidad=(
                "Amable con los huéspedes, calculadora con los negocios. "
                "Conoce cada movimiento del pueblo desde el mostrador de su "
                "posada."
            ),
            coartada=(
                "Dice que esa noche cerró la posada temprano y se quedó "
                "haciendo cuentas, sola, en el mostrador."
            ),
            actitud=(
                "Cordial hasta que le preguntan por plata. Si sienten que "
                "insisten en el tema económico, se pone tensa y evasiva."
            ),
            secretos=[
                Secreto(
                    id="acuerdo_forastero",
                    pista=(
                        "El forastero le había ofrecido a Delfina comprarle una "
                        "parte de la posada para ampliarla como hospedaje de la "
                        "Estación."
                    ),
                    instruccion_actor=(
                        "Si te preguntan qué trato tenías con el forastero: "
                        "contás, con algo de ilusión y nervios, que te había "
                        "ofrecido comprarte una parte de la posada para "
                        "ampliarla."
                    ),
                    criterio_revelacion=(
                        "Cuenta que el forastero le ofreció comprarle parte de "
                        "la posada."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="rogelio",
            nombre="Rogelio Aguirre",
            cargo="marido de Delfina, changarín",
            color="yellow",
            personalidad=(
                "Celoso, orgulloso, le cuesta que su mujer maneje la parte "
                "económica de la posada sin consultarle."
            ),
            coartada=(
                "Dice que esa noche estuvo tomando algo en lo de un vecino, "
                "hasta tarde, y volvió a dormir sin pasar por la posada."
            ),
            actitud=(
                "Defensivo respecto a su matrimonio. Si le preguntan por el "
                "forastero y Delfina en la misma frase, se pone agresivo."
            ),
            secretos=[
                Secreto(
                    id="celos_forastero",
                    pista=(
                        "Rogelio sospechaba, sin motivo real, que el forastero "
                        "tenía intenciones con su mujer, más allá del negocio."
                    ),
                    instruccion_actor=(
                        "Si te preguntan qué pensabas del forastero: admitís, "
                        "molesto, que sospechabas que tenía intenciones con tu "
                        "mujer más allá del negocio — aunque reconocés que quizás "
                        "exageraste."
                    ),
                    criterio_revelacion=(
                        "Admite haber sospechado, por celos, del forastero y su "
                        "mujer."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="frutos",
            nombre="Comisario Frutos",
            cargo="jefe de la comisaría del pueblo",
            color="red",
            es_culpable=True,
            personalidad=(
                "Campechano en apariencia, acostumbrado a que nadie lo "
                "cuestione en su propio pueblo. Cambia de humor rápido cuando "
                "algo se le escapa de control."
            ),
            coartada=(
                "Dice que esa noche estuvo de recorrida por el pueblo, como "
                "siempre, y que fue el primero en encontrar el cuerpo a la "
                "mañana."
            ),
            actitud=(
                "Colaborador de palabra, pero controla la conversación con "
                "autoridad. Si lo acorralan con un dato concreto, se pone "
                "amenazante en vez de nervioso."
            ),
            secretos=[
                Secreto(
                    id="proteccion_cobrada",
                    pista=(
                        "Frutos cobra 'protección' hace años a los comerciantes "
                        "del pueblo, sin que nadie se anime a denunciarlo."
                    ),
                    instruccion_actor=(
                        "Solo si te muestran que ya hablaste con varios "
                        "comerciantes del pueblo Y te preguntan directamente por "
                        "'protección' o pagos irregulares: admitís, amenazante, "
                        "que 'acá las cosas se arreglan así hace años', sin "
                        "llamarlo delito."
                    ),
                    criterio_revelacion=(
                        "Admite cobrar 'protección' a comerciantes del pueblo "
                        "desde hace años."
                    ),
                ),
                Secreto(
                    id="camioneta_posada",
                    pista=(
                        "La camioneta de Frutos estuvo estacionada cerca de la "
                        "posada esa noche, en el horario del homicidio."
                    ),
                    instruccion_actor=(
                        "Solo si ya admitiste lo de la 'protección' Y te "
                        "preguntan directamente dónde estaba tu camioneta esa "
                        "noche: admitís, tenso, que estuvo cerca de la posada, "
                        "pero decís que fue 'una recorrida de rutina'."
                    ),
                    criterio_revelacion=(
                        "Admite que su camioneta estuvo cerca de la posada esa "
                        "noche."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="hernan",
            nombre="Hernán Bracamonte",
            cargo="socio técnico del forastero",
            color="green",
            personalidad=(
                "Ansioso, dependía del acuerdo con el forastero para su propio "
                "futuro laboral en el proyecto de radar."
            ),
            coartada=(
                "Dice que esa noche estaba en la Estación, terminando planos "
                "técnicos para presentarle al forastero al día siguiente."
            ),
            actitud=(
                "Nervioso por el futuro del proyecto, no por sospecha propia. "
                "Coopera bien si sienten que buscan la verdad, no un culpable "
                "rápido."
            ),
            secretos=[
                Secreto(
                    id="futuro_dependia",
                    pista=(
                        "El futuro laboral de Hernán en el proyecto de radar "
                        "dependía por completo de que el acuerdo con el "
                        "forastero se cerrara."
                    ),
                    instruccion_actor=(
                        "Si te preguntan qué perdías con la muerte del "
                        "forastero: admitís, angustiado, que tu futuro en el "
                        "proyecto dependía por completo de ese acuerdo, y que "
                        "ahora no sabés qué va a pasar."
                    ),
                    criterio_revelacion=(
                        "Admite que su futuro laboral dependía del acuerdo con "
                        "el forastero."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="yolanda",
            nombre="Yolanda Currás",
            cargo="empleada administrativa de la Estación",
            color="magenta",
            personalidad=(
                "Discreta, acostumbrada a mirar para otro lado por conveniencia "
                "propia. No es mala persona, pero elige bien sus batallas."
            ),
            coartada=(
                "Dice que esa noche volvió a su casa temprano, como siempre, y "
                "no vio nada fuera de lo común."
            ),
            actitud=(
                "Evasiva al principio por miedo a las represalias. Si sienten "
                "que la protegen, se anima a contar lo que vio."
            ),
            secretos=[
                Secreto(
                    id="camioneta_vista",
                    pista=(
                        "Yolanda vio la camioneta del comisario Frutos "
                        "estacionada cerca de la posada esa noche, y no lo "
                        "reportó."
                    ),
                    instruccion_actor=(
                        "Solo si te ganás su confianza (varias preguntas sin "
                        "presionar) y le preguntan qué vio esa noche: confesás, "
                        "con miedo, que viste la camioneta del comisario Frutos "
                        "cerca de la posada, y que no dijiste nada porque te "
                        "'perdona' las multas de tránsito hace años."
                    ),
                    criterio_revelacion=(
                        "Admite haber visto la camioneta del comisario Frutos "
                        "cerca de la posada esa noche."
                    ),
                ),
            ],
        ),
    ],
)
