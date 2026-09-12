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
                "posada. El forastero la trataba distinto a como la trata el "
                "pueblo hace años — con una atención de otro lado que la "
                "halagó bastante más de lo que está dispuesta a admitir, "
                "aunque nunca cruzó ninguna línea real; lo que de verdad "
                "quiere es sacar la posada de los números ajustados de "
                "siempre, con o sin esa atención de por medio."
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
                    es_entrada=True,
                    certeza="parcial",
                ),
            ],
            reaccion_acusacion_fallida=(
                "Detienen a Delfina por un negocio que nunca llegó a cerrarse; "
                "la posada, con ella presa, se queda sin nadie que lleve las "
                "cuentas."
            ),
        ),
        Sospechoso(
            id="rogelio",
            nombre="Rogelio Aguirre",
            cargo="marido de Delfina, changarín",
            color="yellow",
            personalidad=(
                "Celoso, orgulloso, le cuesta que su mujer maneje la parte "
                "económica de la posada sin consultarle. Se crió viendo a su "
                "padre perder todo por no bajar nunca la cabeza, y jura que a "
                "él no le va a pasar lo mismo — aunque esa promesa lo vuelve "
                "más susceptible, no menos, cada vez que alguien con plata le "
                "presta a Delfina la atención que él siente que no le puede dar."
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
                    es_entrada=True,
                    certeza="ambiguo",
                ),
            ],
            reaccion_acusacion_fallida=(
                "Detienen a Rogelio por celos que él mismo reconoce "
                "exagerados; Delfina se queda sola con la posada y con la "
                "sospecha de medio pueblo encima."
            ),
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
                "algo se le escapa de control. Se convence de que en Jacobacci "
                "las cosas siempre se arreglaron así y que lo que pasó esa "
                "noche fue apenas un exceso de una costumbre vieja, no un "
                "crimen — la misma lógica que usa hace años para cobrar "
                "'protección' sin sentir que roba."
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
                        "Si te preguntan cómo se manejan los negocios en el "
                        "pueblo, o directamente por 'protección' o pagos "
                        "irregulares: admitís, amenazante, que 'acá las cosas se "
                        "arreglan así hace años', sin llamarlo delito."
                    ),
                    criterio_revelacion=(
                        "Admite cobrar 'protección' a comerciantes del pueblo "
                        "desde hace años."
                    ),
                    es_entrada=True,
                    certeza="parcial",
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
                    certeza="confirmado",
                ),
            ],
            reaccion_acusacion_fallida=(
                "Si por algún motivo no lo acusan a él, el comisario Frutos "
                "sigue de recorrida por el pueblo, cobrando lo de siempre "
                "como si nada."
            ),
        ),
        Sospechoso(
            id="hernan",
            nombre="Hernán Bracamonte",
            cargo="socio técnico del forastero",
            color="green",
            personalidad=(
                "Ansioso, dependía del acuerdo con el forastero para su propio "
                "futuro laboral en el proyecto de radar. Ya perdió un proyecto "
                "parecido en otra estación, por falta de fondos, y no está "
                "dispuesto a volver a mudarse de pueblo en pueblo detrás de un "
                "trabajo que se le escapa cada vez que está por asentarse."
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
                    es_entrada=True,
                ),
            ],
            reaccion_acusacion_fallida=(
                "Detienen a Hernán por depender demasiado de un acuerdo que ya "
                "no existe; el proyecto de radar se frena igual, con o sin él "
                "preso."
            ),
        ),
        Sospechoso(
            id="yolanda",
            nombre="Yolanda Currás",
            cargo="empleada administrativa de la Estación",
            color="magenta",
            personalidad=(
                "Discreta, acostumbrada a mirar para otro lado por conveniencia "
                "propia. No es mala persona, pero elige bien sus batallas: cría "
                "sola a sus hijos con un sueldo administrativo que no le "
                "alcanzaría si tuviera que pagar cada multa de tránsito que "
                "Frutos le 'perdona' desde hace años, y no está dispuesta a "
                "arriesgar eso por una verdad que no le trae nada a cambio."
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
                        "Si te preguntan qué viste esa noche cerca de la "
                        "posada, aunque sea de forma general: confesás, con "
                        "miedo, que viste la camioneta del comisario Frutos "
                        "cerca de la posada, y que no dijiste nada porque te "
                        "'perdona' las multas de tránsito hace años."
                    ),
                    criterio_revelacion=(
                        "Admite haber visto la camioneta del comisario Frutos "
                        "cerca de la posada esa noche."
                    ),
                    es_entrada=True,
                    certeza="confirmado",
                ),
            ],
            reaccion_acusacion_fallida=(
                "Detienen a Yolanda por haber visto una camioneta; a la "
                "familia, esta vez, ya no se le perdona ninguna multa."
            ),
        ),
    ],
)
