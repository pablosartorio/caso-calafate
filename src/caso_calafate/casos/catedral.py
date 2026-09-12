"""EL CASO CATEDRAL — homenaje a María Brandán Aráoz (Detectives en Bariloche).

Tono más liviano que el resto: un campamento juvenil, un "fantasma" de cerro y
una rivalidad de pasantes. Nadie se juega la vida, pero alguien sí se juega el
puesto.

⚠️ SPOILER: leer los datos de este archivo revela al culpable.
Jugá una partida antes. :)
"""

from caso_calafate.caso import Caso, Secreto, Sospechoso

CASO_CATEDRAL = Caso(
    id="catedral",
    titulo="EL CASO CATEDRAL",
    sede="Campamento de Observación Astronómica Cerro Catedral",
    ciudad="Bariloche",
    delito="la desaparición de la bitácora del telescopio",
    culpable_alias="farsante",
    gancho=(
        "En el campamento juvenil de observación, un 'fantasma' anda suelto en "
        "el cerro — y la bitácora del telescopio desapareció con él."
    ),
    briefing=(
        "Cerro Catedral, campamento de verano de observación astronómica. Te "
        "llaman a las 08:30, la directora está furiosa.\n\n"
        "«Detective, la bitácora del telescopio no aparece. Y los pasantes "
        "dicen que anoche vieron 'algo' en el cerro. Necesito que esto no se "
        "nos vaya de las manos.»\n\n"
        "Anoche, durante el turno de observación, alguien sacó del domo la "
        "bitácora con meses de registros — y esa misma noche, dos pasantes "
        "juran haber visto una figura pálida moviéndose entre las rocas.\n\n"
        "Lo que se sabe hasta ahora:\n\n"
        " • La bitácora estaba en el domo hasta las 23:00, la última vez que\n"
        "   alguien la anotó.\n"
        " • El 'fantasma' apareció recién después de esa hora, y solo lo vieron\n"
        "   quienes estaban lejos del domo.\n"
        " • No hay ninguna otra salida del cerro esa noche: quien se la llevó\n"
        "   sigue en el campamento.\n"
        " • Cinco personas estaban despiertas esa noche. Son tus sospechosos.\n\n"
        "Interrogá, anotá, y cuando estés seguro: acusá. Tenés una sola oportunidad."
    ),
    contexto_actores="""\
Anoche, en el Campamento de Observación Astronómica del Cerro Catedral
(Bariloche), desapareció del domo la bitácora del telescopio, con meses de
registros. La misma noche, después de las 23:00, dos pasantes dicen haber
visto una figura pálida en las rocas, lejos del domo. No hay otra salida del
cerro: quien se llevó la bitácora sigue en el campamento. Un detective está
interrogando a las cinco personas que estaban despiertas esa noche.""",
    epilogo=(
        "Facu Roldán inventó al fantasma para hundir a Antonella.\n\n"
        "Los dos competían por la única beca de pasantía fija que el Centro "
        "ofrecía a fin de temporada, y Facu sabía que Antonella, hija del "
        "director, llevaba semanas atrasada con la bitácora por estar "
        "ayudando a su papá con otra tarea. Pensó que si la bitácora "
        "'desaparecía' del todo, la culparían a ella por descuido. Se cubrió "
        "con una sábana blanca del depósito de containers y se paseó lejos "
        "del domo para que dos pasantes lo vieran de lejos y corrieran la voz "
        "del 'fantasma' — así nadie prestaría atención a quién entraba y "
        "salía del domo en ese rato. Escondió la bitácora en su propia carpa, "
        "entre las cosas de trekking, pensando devolverla 'encontrada' unos "
        "días después para quedar como el héroe.\n\n"
        "Tobías Reyes, que fue el primero en 'encontrar' pistas del fantasma "
        "a la mañana, no tuvo nada que ver — solo quería ser el centro de la "
        "anécdota del verano, como todos los años."
    ),
    max_preguntas=15,
    sospechosos=[
        Sospechoso(
            id="facu",
            nombre="Facu Roldán",
            cargo="pasante de observación",
            color="red",
            es_culpable=True,
            personalidad=(
                "Aplicado, competitivo, siempre el primero en levantar la mano "
                "para tareas visibles. Le cuesta disimular cuando algo le importa."
            ),
            coartada=(
                "Dice que esa noche estuvo en su carpa temprano, agotado después "
                "del turno de observación, y no se movió hasta la mañana."
            ),
            actitud=(
                "Colaborador y ansioso por ayudar a 'resolver' el misterio del "
                "fantasma. Si le preguntan por la beca o por Antonella, se pone "
                "raro y cambia de tema rápido."
            ),
            secretos=[
                Secreto(
                    id="beca_en_juego",
                    pista=(
                        "Facu y Antonella compiten por la única pasantía fija que "
                        "ofrece el Centro a fin de temporada."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por tu relación con Antonella o por la "
                        "pasantía: admitís, con algo de incomodidad, que los dos "
                        "compiten por la única beca fija de fin de temporada."
                    ),
                    criterio_revelacion=(
                        "Admite que compite con Antonella por la única pasantía "
                        "fija del Centro."
                    ),
                    es_entrada=True,
                ),
                Secreto(
                    id="sabana_containers",
                    pista=(
                        "Del depósito de containers falta una sábana blanca — la "
                        "misma que alguien pudo usar para simular un fantasma."
                    ),
                    instruccion_actor=(
                        "Solo si ya admitiste lo de la beca Y te preguntan "
                        "directamente por el depósito de containers o por sábanas "
                        "blancas: te ponés visiblemente nervioso y decís que 'no "
                        "sabés de qué hablan', sin poder sostenerles la mirada."
                    ),
                    criterio_revelacion=(
                        "Se pone nervioso o evasivo al preguntarle específicamente "
                        "por la sábana blanca faltante del depósito."
                    ),
                ),
            ],
            reaccion_acusacion_fallida=(
                "A Facu lo sueltan entre risas nerviosas del campamento entero: "
                "la beca sigue en juego, y el fantasma del cerro, libre."
            ),
        ),
        Sospechoso(
            id="antonella",
            nombre="Antonella Vidal",
            cargo="pasante de observación, hija del director",
            color="cyan",
            personalidad=(
                "Inteligente, un poco a la defensiva por ser 'la hija del jefe'. "
                "Sabe más de lo que cuenta porque no quiere parecer favorecida."
            ),
            coartada=(
                "Dice que esa noche ayudaba a su papá con un informe atrasado en "
                "la oficina, hasta pasada la medianoche."
            ),
            actitud=(
                "Cortante al principio, por miedo a que la acusen de aprovechada. "
                "Si sienten que la escuchan en serio, se relaja y cuenta más."
            ),
            secretos=[
                Secreto(
                    id="bitacora_atrasada",
                    pista=(
                        "Antonella llevaba semanas atrasada con la bitácora por "
                        "estar ayudando a su padre con otra tarea del Centro."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por el estado de la bitácora antes de "
                        "desaparecer: admitís, avergonzada, que llevabas semanas "
                        "atrasada porque estabas ayudando a tu papá con otro "
                        "informe."
                    ),
                    criterio_revelacion=(
                        "Admite que llevaba semanas atrasada con la bitácora del "
                        "telescopio."
                    ),
                    es_entrada=True,
                ),
            ],
            reaccion_acusacion_fallida=(
                "Antonella queda liberada, aunque la directora le sigue diciendo "
                "que ponerse al día con la bitácora no es opcional."
            ),
        ),
        Sospechoso(
            id="colo",
            nombre="'Colo' Benítez",
            cargo="guía de trekking del campamento",
            color="yellow",
            personalidad=(
                "Bromista profesional, le encanta asustar turistas con leyendas "
                "del cerro. Toma todo con humor, incluso las acusaciones."
            ),
            coartada=(
                "Dice que esa noche se quedó tomando mate con dos pasantes junto "
                "al fogón, contando historias, hasta tarde."
            ),
            actitud=(
                "Divertido y exagerado al contar la leyenda del fantasma. Si le "
                "preguntan en serio, admite enseguida que exagera todo por oficio."
            ),
            secretos=[
                Secreto(
                    id="leyenda_vieja",
                    pista=(
                        "La leyenda del 'fantasma del cerro' que corrió esa noche "
                        "es casi calcada de una que el Colo cuenta hace años en "
                        "sus excursiones."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por el origen de la leyenda del "
                        "fantasma: reconocés, divertido, que es casi calcada de "
                        "una que vos mismo contás hace años en tus excursiones — "
                        "'cualquiera pudo copiarla'."
                    ),
                    criterio_revelacion=(
                        "Reconoce que la leyenda del fantasma se parece a una que "
                        "él mismo cuenta hace años."
                    ),
                    es_entrada=True,
                ),
            ],
            reaccion_acusacion_fallida=(
                "Al Colo lo sueltan entre carcajadas propias: se toma la "
                "acusación como el mejor material nuevo para sus excursiones."
            ),
        ),
        Sospechoso(
            id="marisol",
            nombre="Marisol Andueza",
            cargo="pasante nueva",
            color="green",
            personalidad=(
                "Insegura, consciente de ser la última en llegar al grupo. "
                "Sospecha que todos sospechan de ella primero, y tiene razón."
            ),
            coartada=(
                "Dice que esa noche se quedó despierta sola, estudiando el manual "
                "del telescopio porque todavía no se lo sabe de memoria."
            ),
            actitud=(
                "A la defensiva desde el primer momento, anticipándose a la "
                "sospecha. Si la tratan con paciencia, se relaja y coopera bien."
            ),
            secretos=[
                Secreto(
                    id="vio_a_facu",
                    pista=(
                        "Marisol vio a Facu Roldán salir de su carpa después de "
                        "medianoche, aunque él dijo que se había acostado temprano."
                    ),
                    instruccion_actor=(
                        "Si te preguntan si viste a alguien despierto esa noche: "
                        "contás, dudando al principio por miedo a equivocarte, que "
                        "viste a Facu salir de su carpa después de medianoche."
                    ),
                    criterio_revelacion=(
                        "Menciona haber visto a Facu Roldán salir de su carpa "
                        "después de medianoche."
                    ),
                    es_entrada=True,
                ),
            ],
            reaccion_acusacion_fallida=(
                "Marisol queda liberada, aliviada de que por una vez la duda no "
                "haya recaído del todo en ella."
            ),
        ),
        Sospechoso(
            id="tobias",
            nombre="Tobías Reyes",
            cargo="pasante de observación",
            color="magenta",
            personalidad=(
                "Efusivo, ama ser el centro de atención de cualquier anécdota. "
                "Cuenta la historia del fantasma como si fuera la propia."
            ),
            coartada=(
                "Dice que fue el primero en levantarse a la mañana y el primero "
                "en notar las 'pruebas' del fantasma cerca del domo."
            ),
            actitud=(
                "Encantado de repetir su versión de los hechos una y otra vez, "
                "cada vez con más detalle. Le gusta el protagonismo del misterio."
            ),
            secretos=[
                Secreto(
                    id="pruebas_fabricadas",
                    pista=(
                        "Las 'pruebas' del fantasma que Tobías mostró a la mañana "
                        "— unas marcas en la tierra — las hizo él mismo con un palo, "
                        "para alargar la anécdota."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por las marcas o 'pruebas' del fantasma "
                        "que mostraste a la mañana, o cualquier pregunta abierta "
                        "que te dé pie a contar la anécdota con detalle (te "
                        "encanta): confesás, avergonzado, que las hiciste vos "
                        "mismo con un palo para que la historia durara más, sin "
                        "pensar que complicaría la investigación real."
                    ),
                    criterio_revelacion=(
                        "Admite haber fabricado él mismo las marcas o pruebas del "
                        "fantasma."
                    ),
                    es_entrada=True,
                ),
            ],
            reaccion_acusacion_fallida=(
                "A Tobías lo sueltan sin cargos, aunque ahora la anécdota del "
                "verano incluye, para su deleite, haber sido sospechoso."
            ),
        ),
    ],
)
