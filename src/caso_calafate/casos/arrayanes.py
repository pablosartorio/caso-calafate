"""EL CASO ARRAYANES — homenaje a Claudia Piñeiro (Las viudas de los jueves /
Elena sabe / Betibú).

Un country cerrado, apariencias de clase media-alta, y una muerte que parece
accidente hasta que se empieza a mirar la plata de cerca. El crimen social:
la violencia no rompe la fachada del barrio, vive adentro de ella.

⚠️ SPOILER: leer los datos de este archivo revela al culpable.
Jugá una partida antes. :)
"""

from caso_calafate.caso import Caso, Secreto, Sospechoso

CASO_ARRAYANES = Caso(
    id="arrayanes",
    titulo="EL CASO ARRAYANES",
    sede="Barrio Cerrado Los Arrayanes",
    ciudad="Villa La Angostura",
    delito="el homicidio del ingeniero en la pileta",
    culpable_alias="estafador",
    gancho=(
        "Un ingeniero del Centro Espacial aparece ahogado en la pileta de un "
        "country — todo indica accidente, salvo un detalle que no cierra."
    ),
    briefing=(
        "Barrio Cerrado Los Arrayanes, Villa La Angostura. Te llaman a las "
        "07:00 de un sábado.\n\n"
        "«Detective, un vecino apareció ahogado en la pileta del club house. "
        "El médico de guardia dice que fue un accidente. Nosotros no "
        "estamos tan seguros.»\n\n"
        "El ingeniero, socio inversor de un proyecto tecnológico vinculado al "
        "Centro Espacial, apareció ahogado en la pileta comunitaria a la "
        "madrugada. No tenía antecedentes de salud ni de consumo de alcohol.\n\n"
        "Lo que se sabe hasta ahora:\n\n"
        " • La pileta cierra a medianoche; él entró después, con una llave\n"
        "   que no todos tienen.\n"
        " • Estaba a días de presentar una auditoría sobre las cuentas del\n"
        "   proyecto que financiaba.\n"
        " • No hay cámaras en el sector de la pileta: el barrio las sacó hace\n"
        "   un año 'por privacidad de los socios'.\n"
        " • Cinco personas del barrio tenían trato cercano con él. Son tus\n"
        "   sospechosos.\n\n"
        "Interrogá, anotá, y cuando estés seguro: acusá. Tenés una sola oportunidad."
    ),
    contexto_actores="""\
Un ingeniero, socio inversor de un proyecto tecnológico vinculado al Centro
Espacial, apareció ahogado en la pileta comunitaria del Barrio Cerrado Los
Arrayanes (Villa La Angostura) a la madrugada. Entró después del horario de
cierre con una llave que no todos tienen. Estaba a días de presentar una
auditoría sobre las cuentas del proyecto. No hay cámaras en el sector. Un
detective interroga a las cinco personas del barrio con trato cercano a él.""",
    epilogo=(
        "Pilar Wenger lo ahogó para frenar la auditoría.\n\n"
        "Directora financiera del proyecto, llevaba dos años desviando fondos "
        "hacia una sociedad propia a través de facturas de proveedores "
        "inexistentes. El ingeniero, como auditor externo del proyecto, "
        "estaba a días de presentar un informe que la exponía por completo. "
        "Lo citó esa noche en la pileta —único lugar del barrio sin cámaras "
        "desde que ella misma había impulsado, un año antes, sacarlas 'por "
        "privacidad'— con la excusa de mostrarle unos comprobantes antes de "
        "la presentación oficial. Cuando él confirmó que no había forma de "
        "convencerlo de suavizar el informe, lo empujó en un momento de "
        "pánico más que de plan: el golpe contra el borde de la pileta lo "
        "dejó inconsciente, y ella, en shock, no hizo nada por sacarlo del "
        "agua.\n\n"
        "Ramona Toconás, que limpia el club house de madrugada, vio la luz "
        "de la pileta encendida a esa hora — algo inusual — pero no le dio "
        "importancia hasta que le preguntaron directamente."
    ),
    max_preguntas=15,
    sospechosos=[
        Sospechoso(
            id="marcela",
            nombre="Marcela Issaly",
            cargo="vecina, presidenta del consorcio del barrio",
            color="cyan",
            personalidad=(
                "Sabe absolutamente todo sobre todos en el barrio y disfruta "
                "compartirlo, siempre con un tono de preocupación fingida. Ser "
                "presidenta del consorcio es, en el fondo, el único cargo que "
                "tuvo en su vida, y sostenerlo depende de que el barrio siga "
                "creyendo que ella es quien mejor entiende 'el qué dirán' de "
                "todos — nunca la que lo protagoniza."
            ),
            coartada=(
                "Dice que esa noche estaba en su casa, sin salir, viendo una "
                "serie hasta tarde."
            ),
            actitud=(
                "Chismosa encantada de opinar sobre los demás. Si le preguntan "
                "por sí misma, se pone notablemente más cortante."
            ),
            secretos=[
                Secreto(
                    id="camaras_sacadas",
                    pista=(
                        "Pilar Wenger impulsó, hace un año, sacar las cámaras "
                        "del sector de la pileta 'por privacidad de los socios'."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por las cámaras faltantes en la "
                        "pileta: contás, encantada de saberlo, que fue Pilar "
                        "Wenger quien impulsó sacarlas hace un año, 'por "
                        "privacidad de los socios'."
                    ),
                    criterio_revelacion=(
                        "Cuenta que Pilar Wenger impulsó sacar las cámaras del "
                        "sector de la pileta."
                    ),
                    es_entrada=True,
                    certeza="parcial",
                ),
            ],
            reaccion_acusacion_fallida=(
                "Detienen a Marcela por saber todo sobre todos; el barrio, por "
                "primera vez, tiene de qué hablar de ella en vez de escucharla "
                "hablar de los demás."
            ),
        ),
        Sospechoso(
            id="gaston",
            nombre="Gastón Prado",
            cargo="marido de la víctima",
            color="yellow",
            personalidad=(
                "Devastado, pero con un fondo de resentimiento viejo que se le "
                "escapa sin querer. La relación con su esposo venía tensa. Dejó "
                "su propia carrera en pausa para acompañar el proyecto del "
                "Centro Espacial, y hace tiempo que no sabe si lo que siente es "
                "duelo por perderlo o por los años que ya había perdido antes."
            ),
            coartada=(
                "Dice que esa noche durmió en su casa, sin saber que su marido "
                "había salido a esa hora."
            ),
            actitud=(
                "Dolido y algo evasivo sobre el estado real de su matrimonio. "
                "Si sienten empatía genuina, se abre más."
            ),
            secretos=[
                Secreto(
                    id="matrimonio_tenso",
                    pista=(
                        "El matrimonio de Gastón y la víctima venía muy tenso "
                        "por el estrés del proyecto y sus horarios."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por su relación: admitís, con "
                        "tristeza, que venían muy mal últimamente por el "
                        "estrés del proyecto y los horarios imposibles."
                    ),
                    criterio_revelacion=(
                        "Admite que su matrimonio con la víctima estaba muy "
                        "tenso últimamente."
                    ),
                    es_entrada=True,
                    certeza="ambiguo",
                ),
            ],
            reaccion_acusacion_fallida=(
                "Detienen al marido de la víctima; el barrio, que ya lo miraba "
                "raro por el matrimonio tenso, encuentra la confirmación que "
                "estaba esperando sin pruebas."
            ),
        ),
        Sospechoso(
            id="pilar",
            nombre="Pilar Wenger",
            cargo="directora financiera del proyecto",
            color="red",
            es_culpable=True,
            personalidad=(
                "Impecable, controlada, siempre con el argumento financiero "
                "justo a mano. La grieta aparece solo cuando se habla de "
                "números concretos. Se convence de que lo que desvió era, en "
                "el fondo, un adelanto sobre lo que el proyecto nunca le pagó "
                "en años de trabajo invisible — y de que lo que pasó en la "
                "pileta fue un accidente que ella no provocó tanto como "
                "permitió, congelada, sin animarse a pedir ayuda."
            ),
            coartada=(
                "Dice que esa noche se quedó en su casa preparando la "
                "presentación para la auditoría del día siguiente."
            ),
            actitud=(
                "Profesional y calma. Si la confrontan con detalles financieros "
                "concretos, empieza a explicarlos de más — el mismo error de "
                "Silvia en Calafate, pero con números en vez de sistemas."
            ),
            secretos=[
                Secreto(
                    id="fondos_desviados",
                    pista=(
                        "Pilar desvió fondos del proyecto hacia una sociedad "
                        "propia mediante facturas de proveedores inexistentes."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por las finanzas del proyecto, por los "
                        "proveedores, o te muestran algún dato financiero "
                        "concreto: cometés tu único descuido, explicando de más "
                        "un esquema de facturación que, sin querer, revela que "
                        "hay proveedores que no existen."
                    ),
                    criterio_revelacion=(
                        "Revela, aunque sea indirectamente, que hay facturas de "
                        "proveedores inexistentes o fondos desviados."
                    ),
                    es_entrada=True,
                    certeza="parcial",
                ),
                Secreto(
                    id="cita_pileta",
                    pista=(
                        "Pilar citó al ingeniero en la pileta esa noche, con la "
                        "excusa de mostrarle comprobantes antes de la auditoría."
                    ),
                    instruccion_actor=(
                        "Solo si ya revelaste lo de los fondos Y te preguntan "
                        "si viste a la víctima esa noche: admitís, con la voz "
                        "quebrada, que lo citaste en la pileta para mostrarle "
                        "unos comprobantes antes de la auditoría."
                    ),
                    criterio_revelacion=(
                        "Admite haber citado a la víctima en la pileta esa "
                        "noche."
                    ),
                    certeza="confirmado",
                ),
            ],
            reaccion_acusacion_fallida=(
                "Si por algún motivo no la acusan a ella, Pilar presenta la "
                "auditoría dos semanas después, con los números ya "
                "prolijamente resueltos."
            ),
        ),
        Sospechoso(
            id="nazareno",
            nombre="Nazareno Quiroga",
            cargo="ex empleado del proyecto, despedido",
            color="green",
            personalidad=(
                "Amargado con la empresa, no necesariamente con la víctima "
                "personalmente. Habla con resentimiento pero sin agresividad "
                "hacia ella. Perdió no solo el trabajo sino la reputación en un "
                "rubro chico donde todos se conocen; lo que más quiere no es "
                "que alguien pague por la muerte del ingeniero, sino que "
                "alguien reabra por fin la denuncia que hizo y que nadie miró."
            ),
            coartada=(
                "Dice que esa noche estaba en su casa, fuera del barrio, con "
                "su familia."
            ),
            actitud=(
                "Directo sobre su despido, algo defensivo si sienten que lo "
                "acusan por eso mismo."
            ),
            secretos=[
                Secreto(
                    id="despido_injusto",
                    pista=(
                        "Nazareno fue despedido hace meses del proyecto tras "
                        "denunciar irregularidades que nadie investigó."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por tu despido: contás, con "
                        "resentimiento, que te despidieron después de denunciar "
                        "irregularidades que nadie quiso investigar."
                    ),
                    criterio_revelacion=(
                        "Cuenta que fue despedido tras denunciar irregularidades "
                        "en el proyecto."
                    ),
                    es_entrada=True,
                ),
            ],
            reaccion_acusacion_fallida=(
                "Detienen a Nazareno por un despido injusto que ahora parece, "
                "encima, sospechoso; nadie investiga tampoco esta vez lo que "
                "denunció."
            ),
        ),
        Sospechoso(
            id="ramona",
            nombre="Ramona Toconás",
            cargo="empleada de limpieza del club house",
            color="magenta",
            personalidad=(
                "Discreta, trabajadora, acostumbrada a ser invisible para los "
                "socios del barrio. Ve más de lo que cualquiera imagina, y hace "
                "años aprendió a callarlo: viaja tres horas por día para "
                "trabajar en Los Arrayanes y no puede permitirse perder el "
                "puesto por decir algo que a un socio no le guste escuchar."
            ),
            coartada=(
                "Dice que esa noche limpiaba el club house de madrugada, como "
                "todos los días, sin cruzarse con nadie."
            ),
            actitud=(
                "Tímida al principio, por no sentirse escuchada nunca por los "
                "socios del barrio. Si la tratan con respeto, cuenta con "
                "precisión lo que vio."
            ),
            secretos=[
                Secreto(
                    id="luz_encendida",
                    pista=(
                        "Ramona vio la luz de la pileta encendida a una hora "
                        "inusual esa madrugada, algo que nunca pasaba."
                    ),
                    instruccion_actor=(
                        "Si te preguntan si notaste algo raro esa madrugada: "
                        "contás, con precisión, que viste la luz de la pileta "
                        "encendida a una hora inusual, algo que nunca pasaba."
                    ),
                    criterio_revelacion=(
                        "Menciona haber visto la luz de la pileta encendida a "
                        "una hora inusual esa madrugada."
                    ),
                    es_entrada=True,
                    certeza="confirmado",
                ),
            ],
            reaccion_acusacion_fallida=(
                "Detienen a Ramona por prestar atención; después de esto, en "
                "el barrio la vuelven a mirar como si no estuviera."
            ),
        ),
    ],
)
