"""EL CASO MASCARDI — homenaje a Cristian Perfumo (thrillers patagónicos de atracos).

Un golpe coordinado, no un ladrón solitario: la Patagonia como escenario de
operación, con cómplices que se reparten roles como en un asalto de película.

⚠️ SPOILER: leer los datos de este archivo revela al culpable.
Jugá una partida antes. :)
"""

from caso_calafate.caso import Caso, Secreto, Sospechoso

CASO_MASCARDI = Caso(
    id="mascardi",
    titulo="EL CASO MASCARDI",
    sede="Estación de Radares del Lago Mascardi",
    ciudad="Bariloche",
    delito="el robo del prototipo de radar portátil",
    culpable_alias="ladrón",
    gancho=(
        "En medio de un temporal, un golpe coordinado se llevó el prototipo — "
        "esto no lo hizo un saboteador solo."
    ),
    briefing=(
        "Lago Mascardi, después de un temporal de tres días. Te llaman a las "
        "08:00.\n\n"
        "«Detective, el prototipo de radar portátil no está. Y esto no fue un "
        "descuido.»\n\n"
        "Durante la última noche del temporal — con las lanchas de auxilio "
        "ocupadas en otra emergencia y la posada llena de técnicos varados — "
        "alguien sacó el prototipo de radar portátil del depósito de la "
        "estación y lo cruzó al otro lado del lago.\n\n"
        "Lo que se sabe hasta ahora:\n\n"
        " • El depósito se abrió con una llave real, sin forzar nada.\n"
        " • Se usó una lancha esa noche, pese a la alerta de navegación.\n"
        " • El sistema de guardia registró un corte de cámaras de exactamente\n"
        "   nueve minutos — el tiempo justo para sacar el cajón.\n"
        " • Cinco personas estaban en la zona esa noche. Son tus sospechosos.\n\n"
        "Interrogá, anotá, y cuando estés seguro: acusá. Tenés una sola oportunidad."
    ),
    contexto_actores="""\
Anoche, durante un temporal, desapareció el prototipo de radar portátil del
depósito de la Estación de Radares del Lago Mascardi (Bariloche). El depósito
se abrió con llave, sin forzar nada, y alguien cruzó el lago en lancha pese a
la alerta de navegación. Las cámaras se cortaron nueve minutos, justo lo
necesario para sacar el cajón. Un detective está interrogando a las cinco
personas que estaban en la zona esa noche.""",
    epilogo=(
        "Ezequiel Farías organizó el golpe desde adentro.\n\n"
        "Como jefe de seguridad tenía llave del depósito y control sobre las "
        "cámaras: cortarlas nueve minutos y volver a encenderlas era apenas "
        "tocar un interruptor que solo él podía tocar sin que sonara una "
        "alarma. Endeudado con un socio de Neuquén que ya le había puesto un "
        "plazo, armó el golpe con tres roles: el 'Colorado' Andrada cruzó el "
        "lago en lancha con el prototipo, Baltasar Oyarzún prestó su galpón de "
        "pesca en la otra orilla como punto de entrega sin preguntar qué "
        "guardaba, y el propio Ezequiel se aseguró de ser 'el primero en "
        "notar' el robo a la mañana, gritando más que nadie para despejar toda "
        "sospecha de sí mismo.\n\n"
        "Melina Suárez, que trabajaba de noche en el prototipo, fue la única "
        "que notó que el corte de cámaras coincidía exacto con la ventana de "
        "acceso — pero calló un tiempo, todavía dolida por su separación de "
        "Ezequiel, sin saber bien si de verdad quería involucrarse.\n\n"
        "Perla Domínguez, en su posada, no vio nada raro: esa noche, como "
        "todas las de temporal, tenía la casa llena y no daba abasto."
    ),
    max_preguntas=15,
    sospechosos=[
        Sospechoso(
            id="baltasar",
            nombre="Baltasar Oyarzún",
            cargo="guía de pesca",
            color="green",
            personalidad=(
                "Relajado, de pocas palabras, acostumbrado a que la gente de la "
                "estación lo trate como parte del paisaje, no como testigo. Lo que "
                "más lo desvela no es la deuda en sí, sino que alguien de Neuquén "
                "se aparezca por el lago a cobrársela delante de los técnicos que "
                "sí lo tratan con respeto."
            ),
            coartada=(
                "Dice que esa noche cerró su galpón de pesca temprano por el "
                "temporal y se quedó adentro tomando mate, solo."
            ),
            actitud=(
                "Responde sin apuro, casi displicente. Si le muestran algo concreto "
                "sobre su galpón, se pone tenso de golpe y empieza a medir cada "
                "palabra."
            ),
            secretos=[
                Secreto(
                    id="deuda_juego",
                    pista=(
                        "Baltasar tiene deudas de juego con gente de Neuquén, la "
                        "misma plaza donde Ezequiel Farías tiene un socio."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por tus deudas, por gente de Neuquén, o en "
                        "general si tenés problemas de plata: admitís, incómodo, "
                        "que debés dinero de juego a gente de Neuquén, pero jurás "
                        "que no tiene nada que ver con esto."
                    ),
                    criterio_revelacion=(
                        "Admite tener deudas de juego vinculadas a gente de Neuquén."
                    ),
                    es_entrada=True,
                    certeza="ambiguo",
                ),
            ],
            reaccion_acusacion_fallida=(
                "La crónica de Bariloche titula «Detienen a guía de pesca por "
                "error»: sueltan a Baltasar dos días después, sin una disculpa "
                "formal, y sigue debiéndole la misma plata a la misma gente de "
                "Neuquén."
            ),
        ),
        Sospechoso(
            id="melina",
            nombre="Melina Suárez",
            cargo="ingeniera del prototipo de radar",
            color="cyan",
            personalidad=(
                "Meticulosa, todavía dolida por una separación reciente. Contesta "
                "con precisión técnica hasta que la pregunta se pone personal. Lo "
                "que la frena no es lealtad a Ezequiel — eso ya se terminó — sino "
                "el miedo a que el rencor le esté nublando el juicio y esté "
                "acusando a alguien solo por despecho."
            ),
            coartada=(
                "Dice que se quedó trabajando hasta tarde en el laboratorio y se "
                "fue a dormir a su cuarto en la estación, sola, cerca de la 01:00."
            ),
            actitud=(
                "Firme con los datos técnicos. Si le preguntan por Ezequiel, su "
                "ex, se cierra en banda y cambia de tema con brusquedad."
            ),
            secretos=[
                Secreto(
                    id="corte_coincide",
                    pista=(
                        "El corte de cámaras de nueve minutos coincidió exactamente "
                        "con la única ventana en que el depósito quedó sin vigilancia."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por el corte de cámaras, por cómo alguien "
                        "pudo entrar sin ser visto, o en general qué pasó esa noche "
                        "en el depósito: explicás, con precisión técnica, que el "
                        "corte duró justo nueve minutos y coincidió exacto con la "
                        "única ventana sin vigilancia — 'como si alguien supiera el "
                        "horario exacto'."
                    ),
                    criterio_revelacion=(
                        "Explica que el corte de cámaras coincidió exactamente con "
                        "la ventana sin vigilancia del depósito."
                    ),
                    es_entrada=True,
                    certeza="parcial",
                ),
                Secreto(
                    id="sospecha_ezequiel",
                    pista=(
                        "Melina sospechó de entrada que fue Ezequiel — el único "
                        "con acceso real para cortar las cámaras sin que saltara "
                        "una alarma — pero calló, insegura de si el rencor le "
                        "nublaba el juicio."
                    ),
                    instruccion_actor=(
                        "Solo si ya contaste lo del corte de cámaras Y te "
                        "preguntan por qué no sospechaste antes de alguien en "
                        "particular: admitís, incómoda, que pensaste enseguida en "
                        "Ezequiel — el único con acceso real para cortarlas sin "
                        "que saltara una alarma — pero no dijiste nada, insegura "
                        "de si el rencor por la separación te estaba nublando el "
                        "juicio."
                    ),
                    criterio_revelacion=(
                        "Admite haber sospechado específicamente de Ezequiel "
                        "Farías por su acceso a las cámaras, y que calló por "
                        "dudas personales."
                    ),
                    certeza="confirmado",
                ),
            ],
            reaccion_acusacion_fallida=(
                "Detienen a Melina un fin de semana entero mientras el prototipo "
                "sigue del otro lado del lago; cuando la largan, pide que la "
                "saquen de la causa y no vuelve a hablar del tema."
            ),
        ),
        Sospechoso(
            id="andrada",
            nombre="'Colorado' Andrada",
            cargo="lanchero de la estación",
            color="red",
            personalidad=(
                "Bromista, popular entre los técnicos, de esos que hacen un favor "
                "sin preguntar demasiado. Se pone serio solo cuando lo acusan. Ser "
                "'el que resuelve' es lo único que tiene en la estación, y sabe "
                "que haber prestado la lancha sin preguntar lo puede dejar del "
                "lado equivocado la primera vez que alguien necesite pruebas y no "
                "favores."
            ),
            coartada=(
                "Dice que esa noche amarró bien las lanchas por el temporal y se "
                "fue a dormir a su casa en el pueblo, como cualquier noche mala."
            ),
            actitud=(
                "Minimiza todo con humor. Si le marcan una contradicción concreta "
                "sobre el estado de las lanchas, se pone nervioso y empieza a "
                "justificarse de más."
            ),
            secretos=[
                Secreto(
                    id="lancha_usada",
                    pista=(
                        "Una de las lanchas amaneció con combustible gastado y ramas "
                        "de la otra orilla enredadas en el motor — se usó esa noche."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por las lanchas esa noche, o te muestran "
                        "el dato del combustible gastado o las ramas en el motor: "
                        "admitís, nervioso, que una lancha se usó esa noche, pero "
                        "decís que vos no fuiste — que Ezequiel te pidió las "
                        "llaves 'para revisar algo' y no volviste a preguntar."
                    ),
                    criterio_revelacion=(
                        "Admite que se usó una lancha esa noche y que Ezequiel "
                        "Farías le pidió las llaves."
                    ),
                    es_entrada=True,
                    certeza="confirmado",
                ),
            ],
            reaccion_acusacion_fallida=(
                "El 'Colorado' pasa una noche en la comisaría por prestar una "
                "lancha; lo sueltan sin cargos, pero deja de hacerle favores a "
                "cualquiera sin preguntar primero."
            ),
        ),
        Sospechoso(
            id="perla",
            nombre="Perla Domínguez",
            cargo="dueña de la posada de técnicos",
            color="yellow",
            personalidad=(
                "Charlatana, orgullosa de conocer a todos sus huéspedes por nombre. "
                "Le encanta opinar de la vida ajena, sin mala intención. La posada "
                "es lo único que le quedó después de quedarse viuda joven, y "
                "llenarla de historia ajena es, en el fondo, su manera de no "
                "quedarse sola con las propias."
            ),
            coartada=(
                "Dice que esa noche la posada estaba llena por el temporal y no "
                "paró de atender huéspedes hasta pasada la medianoche."
            ),
            actitud=(
                "Habla de más sobre todos menos sobre sí misma. Cuanto más la "
                "dejan hablar, más detalles sueltos aparecen sin que se los pidan."
            ),
            secretos=[
                Secreto(
                    id="ezequiel_endeudado",
                    pista=(
                        "Ezequiel Farías le comentó a Perla, tomando algo, que tenía "
                        "un socio de Neuquén 'presionándolo feo' por plata."
                    ),
                    instruccion_actor=(
                        "Si te preguntan si notaste algo raro en Ezequiel, o "
                        "directamente qué se comenta de él por la posada: contás, "
                        "como quien no quiere la cosa, que hace poco te comentó que "
                        "tenía un socio de Neuquén presionándolo feo por plata."
                    ),
                    criterio_revelacion=(
                        "Cuenta que Ezequiel Farías tenía problemas de plata con un "
                        "socio de Neuquén."
                    ),
                    es_entrada=True,
                    certeza="parcial",
                ),
            ],
            reaccion_acusacion_fallida=(
                "Detienen a Perla mientras la posada se vacía de huéspedes "
                "asustados; jura, dolida, que ella solo repite lo que escucha, "
                "nunca lo que hace."
            ),
        ),
        Sospechoso(
            id="ezequiel",
            nombre="Ezequiel Farías",
            cargo="jefe de seguridad de la estación",
            color="magenta",
            es_culpable=True,
            personalidad=(
                "Eficiente, siempre el primero en dar la alarma y ofrecerse a "
                "ayudar. Controla la conversación con tono de mando. Se convence "
                "de que no le está robando a nadie de la estación, solo "
                "resolviendo un problema que la estación jamás lo hubiera "
                "ayudado a resolver — y que gritar más fuerte que nadie a la "
                "mañana no es actuar, es simplemente hacer bien el trabajo que "
                "ya venía haciendo."
            ),
            coartada=(
                "Dice que hizo su ronda nocturna normal y que fue él mismo quien "
                "notó el robo a la mañana y dio aviso de inmediato."
            ),
            actitud=(
                "Colaborador en apariencia, redirige la sospecha hacia cualquier "
                "otro con calma profesional. Si lo acorralan con evidencia técnica "
                "sobre las cámaras, se pone frío y evasivo de golpe."
            ),
            secretos=[
                Secreto(
                    id="socio_neuquen",
                    pista=(
                        "Ezequiel debe una suma importante a un socio de Neuquén, "
                        "que ya le había puesto un plazo límite para pagar."
                    ),
                    instruccion_actor=(
                        "Con cualquier pregunta abierta sobre esa noche o sobre "
                        "vos: admitís, tenso, que le debés plata a un socio de "
                        "Neuquén y que te puso un plazo. Negás que tenga que ver "
                        "con el robo."
                    ),
                    criterio_revelacion=(
                        "Admite tener una deuda con un socio de Neuquén y un plazo "
                        "de pago."
                    ),
                    es_entrada=True,
                    certeza="parcial",
                ),
                Secreto(
                    id="llaves_lancha",
                    pista=(
                        "Ezequiel le pidió las llaves de una lancha al 'Colorado' "
                        "Andrada esa misma noche, 'para revisar algo'."
                    ),
                    instruccion_actor=(
                        "Solo si ya admitiste la deuda Y te preguntan por las "
                        "llaves de la lancha o por Andrada: caés, cada vez más "
                        "frío, en que le pediste las llaves esa noche 'para "
                        "revisar el amarre', sin dar más detalles."
                    ),
                    criterio_revelacion=(
                        "Admite haberle pedido las llaves de una lancha a Andrada "
                        "esa misma noche."
                    ),
                    certeza="confirmado",
                ),
            ],
            reaccion_acusacion_fallida=(
                "Si por algún error no lo acusan, Ezequiel sigue de jefe de "
                "seguridad, dando notas a la prensa como el hombre que más se "
                "indignó con el robo."
            ),
        ),
    ],
)
