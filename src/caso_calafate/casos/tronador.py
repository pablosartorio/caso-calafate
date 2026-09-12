"""EL CASO TRONADOR — homenaje a Borges & Bioy Casares (Seis problemas para
don Isidro Parodi, firmado H. Bustos Domecq).

El propio mecanismo del juego — interrogar sin moverse del escritorio — es el
mismo truco de Parodi: un detective confinado que resuelve todo de oído. Acá
lo llevamos al extremo con una cuarentena sanitaria, y con personajes tan
grandilocuentes que se delatan por el simple gusto de escucharse hablar.

⚠️ SPOILER: leer los datos de este archivo revela al culpable.
Jugá una partida antes. :)
"""

from caso_calafate.caso import Caso, Secreto, Sospechoso

CASO_TRONADOR = Caso(
    id="tronador",
    titulo="EL CASO TRONADOR",
    sede="Centro Espacial Patagónico",
    ciudad="Bariloche",
    delito="el robo durante la cuarentena",
    culpable_alias="ladrón",
    gancho=(
        "Cinco personas encerradas por una cuarentena sanitaria, un robo en la "
        "sala común, y nadie que pudiera haber entrado ni salido."
    ),
    briefing=(
        "Centro Espacial Patagónico, módulo de aislamiento sanitario. Un brote "
        "de gripe obligó a poner en cuarentena a cinco personas hace tres "
        "días. Te llaman a las 10:00, por teléfono: no podés entrar al módulo.\n\n"
        "«Detective, dentro del módulo desapareció una caja fuerte con "
        "documentación reservada. Las cinco personas ahí adentro son, a la "
        "vez, todos los sospechosos y todos los únicos testigos posibles.»\n\n"
        "Vas a tener que resolver esto sin pisar el lugar de los hechos: solo "
        "podés hablarles por videollamada, uno por uno.\n\n"
        "Lo que se sabe hasta ahora:\n\n"
        " • La caja fuerte estaba en la sala común del módulo hasta la\n"
        "   medianoche.\n"
        " • Nadie entró ni salió del módulo: la cuarentena es real y está\n"
        "   controlada desde afuera.\n"
        " • La caja apareció vacía, escondida en un conducto de ventilación,\n"
        "   a la mañana siguiente.\n"
        " • Las cinco personas en cuarentena son tus sospechosos.\n\n"
        "Interrogá, anotá, y cuando estés seguro: acusá. Tenés una sola oportunidad."
    ),
    contexto_actores="""\
Hace tres días, un brote de gripe puso en cuarentena a cinco personas en el
módulo de aislamiento del Centro Espacial Patagónico (Bariloche). Anoche
desapareció una caja fuerte con documentación reservada de la sala común;
apareció vacía a la mañana, escondida en un conducto de ventilación. Nadie
entró ni salió del módulo: los cinco en cuarentena son los únicos que pudieron
hacerlo. Un detective los interroga por videollamada, sin poder ingresar al
módulo.""",
    epilogo=(
        "El suboficial Pochettino robó la caja para encubrir su propio error.\n\n"
        "Meses atrás, investigando una denuncia menor, había 'resuelto' el "
        "caso culpando al empleado equivocado — un error que constaba, con "
        "pelos y señales, en la documentación reservada de esa misma caja "
        "fuerte. Al enterarse de que un ascenso suyo dependía de que esa "
        "documentación se revisara pronto, decidió que la única salida era "
        "que el contenido 'desapareciera'. Vació la caja de noche, mientras "
        "los demás dormían, y escondió los papeles en su propio bolso — no en "
        "el conducto de ventilación, donde puso solo la caja vacía como señuelo "
        "para simular un robo externo imposible dentro de una cuarentena "
        "cerrada.\n\n"
        "La Sra. Higinia Bulacio, que no duerme bien y escucha todo desde su "
        "camastro, oyó el crujido metálico de la caja esa noche pero no le "
        "dio importancia hasta que se lo preguntaron directamente — y hasta "
        "entonces, prefirió seguir contando, con lujo de detalle, sus propias "
        "teorías sobre todos los demás."
    ),
    max_preguntas=15,
    sospechosos=[
        Sospechoso(
            id="wernicke",
            nombre="Dr. Aurelio Wernicke",
            cargo="director teórico del Centro",
            color="cyan",
            personalidad=(
                "Solemne, incapaz de responder una pregunta simple sin antes "
                "explicar tres conceptos que nadie pidió. Se cree el más lúcido "
                "del módulo. Cultiva un castellano de gala, sembrado de "
                "latinismos y subordinadas, convencido de que la llaneza es "
                "cosa de espíritus menores; en el fondo teme haberse "
                "convertido, para el resto del Centro, en una reliquia "
                "elocuente a la que se escucha por cortesía y ya no por "
                "autoridad real."
            ),
            coartada=(
                "Dice que pasó la noche leyendo, como todas las noches de "
                "cuarentena, 'ajeno por completo a las minucias materiales del "
                "edificio'."
            ),
            actitud=(
                "Responde con largos rodeos teóricos antes de llegar al punto. Si "
                "lo apuran, se ofende por la falta de paciencia intelectual del "
                "interrogador."
            ),
            secretos=[
                Secreto(
                    id="conducto_conocido",
                    pista=(
                        "El Dr. Wernicke diseñó, hace años, el plano de ventilación "
                        "del módulo — conoce el conducto donde apareció la caja "
                        "mejor que nadie."
                    ),
                    instruccion_actor=(
                        "Con cualquier pregunta abierta sobre el módulo, sus "
                        "planos o el conducto de ventilación: explicás, con "
                        "orgullo académico y demasiado detalle, que vos mismo "
                        "diseñaste ese plano hace años, aunque aclarás que eso "
                        "'no prueba absolutamente nada'."
                    ),
                    criterio_revelacion=(
                        "Revela que diseñó o conoce en detalle el plano del "
                        "conducto de ventilación del módulo."
                    ),
                    es_entrada=True,
                    certeza="ambiguo",
                ),
            ],
            reaccion_acusacion_fallida=(
                "«Permítanme señalar, con la ecuanimidad que me caracteriza, "
                "que acaban de confundir la elocuencia con la culpa: error ya "
                "cometido, si mal no recuerdo, por los primeros exégetas de "
                "Aristóteles.»"
            ),
        ),
        Sospechoso(
            id="higinia",
            nombre="Sra. Higinia Bulacio",
            cargo="administrativa, huésped ocasional del módulo",
            color="yellow",
            personalidad=(
                "Metiche declarada, encantada de opinar sobre la vida de los "
                "otros cuatro. Duerme mal y por eso 'lo escucha todo'. Adorna "
                "cada anécdota con una prosa tan barroca como innecesaria, "
                "quizás porque toda la vida sintió que nadie la tomaba del "
                "todo en serio; ser, por una vez, la única testigo auditiva "
                "de algo importante le sabe a revancha tardía."
            ),
            coartada=(
                "Dice que no durmió casi nada esa noche, como de costumbre, y que "
                "puede dar fe de casi todos los movimientos ajenos, menos los "
                "propios."
            ),
            actitud=(
                "Chismosa y dispuesta a teorizar sobre cualquiera, menos sobre sí "
                "misma. Si le preguntan algo puntual sobre ruidos, se toma su "
                "tiempo para lucirse con el relato."
            ),
            secretos=[
                Secreto(
                    id="crujido_metalico",
                    pista=(
                        "Higinia escuchó un crujido metálico esa noche, similar al "
                        "de una caja fuerte al abrirse, pero no le dio importancia."
                    ),
                    instruccion_actor=(
                        "Con cualquier pregunta abierta sobre esa noche o sobre "
                        "si escuchaste algo raro: contás, con lujo de detalle, "
                        "que escuchaste un crujido metálico, 'como de bisagra "
                        "vieja', pero que no le diste importancia en el "
                        "momento."
                    ),
                    criterio_revelacion=(
                        "Cuenta que escuchó un crujido metálico esa noche similar "
                        "al de la caja fuerte."
                    ),
                    es_entrada=True,
                    certeza="parcial",
                ),
            ],
            reaccion_acusacion_fallida=(
                "«Yo, detective, lo dije desde el principio con la elocuencia "
                "que Dios me dio: el crujido metálico no mentía. Ustedes sí "
                "se equivocaron, y con qué convicción.»"
            ),
        ),
        Sospechoso(
            id="osman",
            nombre="Osmán Correa",
            cargo="técnico que se cree poeta",
            color="green",
            personalidad=(
                "Dramático, convierte cada respuesta en un pequeño discurso. "
                "Le encanta la idea de ser sospechoso de algo, por primera vez en "
                "su vida gris de técnico. Sueña, en secreto, con que esta "
                "cuarentena sea la anécdota que por fin lo saque del anonimato "
                "del taller: ser leído, aunque sea como sospechoso de una nota "
                "policial, le parece mejor que seguir siendo el técnico "
                "invisible de siempre."
            ),
            coartada=(
                "Dice que pasó la noche escribiendo versos sobre el encierro, "
                "'una cuarentena es, ante todo, materia poética'."
            ),
            actitud=(
                "Teatral y ansioso por que sus respuestas suenen memorables. Si "
                "lo interrumpen, se ofende como artista incomprendido."
            ),
            secretos=[
                Secreto(
                    id="rencor_ascenso",
                    pista=(
                        "Osmán fue pasado por alto para un ascenso hace un año, "
                        "en favor de alguien con menos antigüedad."
                    ),
                    instruccion_actor=(
                        "Con cualquier pregunta abierta sobre tu trabajo, tu "
                        "historia en el Centro o si tenés algún resentimiento: "
                        "contás, con dramatismo, que hace un año te pasaron por "
                        "alto para un ascenso, 'la mediocridad, una vez más, "
                        "premiada por sobre el mérito'."
                    ),
                    criterio_revelacion=(
                        "Cuenta que fue pasado por alto para un ascenso hace un "
                        "año."
                    ),
                    es_entrada=True,
                    certeza="parcial",
                ),
            ],
            reaccion_acusacion_fallida=(
                "«Qué ironía, detective: por fin alguien me presta atención, "
                "y es para acusarme de algo que no hice. La poesía, ya lo "
                "sabía, siempre fue más justa que la ley.»"
            ),
        ),
        Sospechoso(
            id="pochettino",
            nombre="Suboficial Pochettino",
            cargo="seguridad interna del Centro",
            color="red",
            es_culpable=True,
            personalidad=(
                "Autoritario, impaciente con lo que considera 'teorías raras' de "
                "los demás. Convencido de que su instinto policial nunca falla. "
                "Se convenció de que retirar la caja no fue robar sino corregir, "
                "en privado, un error que de otro modo iba a arruinarle una "
                "carrera entera por una decisión que en su momento le pareció "
                "correcta: para él, la Central le debe más de lo que él le sacó."
            ),
            coartada=(
                "Dice que hizo su ronda de control dentro del módulo y se "
                "durmió temprano, 'como corresponde a quien cumple su horario'."
            ),
            actitud=(
                "Desestima cualquier hipótesis ajena con desdén profesional. Si "
                "lo confrontan con un error suyo del pasado, se pone agresivo y "
                "defensivo."
            ),
            secretos=[
                Secreto(
                    id="ascenso_pendiente",
                    pista=(
                        "Pochettino tiene un ascenso pendiente que depende de que "
                        "se revise pronto cierta documentación reservada."
                    ),
                    instruccion_actor=(
                        "Con cualquier pregunta abierta sobre tu ascenso, tu "
                        "carrera o por qué te importa esa documentación: "
                        "admitís, a regañadientes, que tenés un ascenso "
                        "pendiente atado a que esos papeles se revisen pronto."
                    ),
                    criterio_revelacion=(
                        "Admite tener un ascenso pendiente ligado a la revisión "
                        "de la documentación de la caja."
                    ),
                    es_entrada=True,
                    certeza="parcial",
                ),
                Secreto(
                    id="error_viejo",
                    pista=(
                        "Hace meses, Pochettino 'resolvió' mal una denuncia y "
                        "culpó al empleado equivocado — el error consta en esa "
                        "misma documentación."
                    ),
                    instruccion_actor=(
                        "Solo si ya admitiste lo del ascenso Y te preguntan qué "
                        "hay exactamente en esa documentación que te preocupa: "
                        "confesás, furioso pero acorralado, que hace meses "
                        "resolviste mal una denuncia y culpaste al empleado "
                        "equivocado, y que eso queda registrado ahí."
                    ),
                    criterio_revelacion=(
                        "Admite haber resuelto mal una denuncia anterior y "
                        "culpado al empleado equivocado."
                    ),
                    certeza="confirmado",
                ),
            ],
            reaccion_acusacion_fallida=(
                "Si por algún motivo no lo acusan a él, el suboficial "
                "Pochettino sigue al mando de la seguridad del módulo, y ya "
                "empezó a cerrar el caso puertas adentro como 'incidente sin "
                "explicación', antes de que alguien vuelva a mirar esa "
                "documentación."
            ),
        ),
        Sospechoso(
            id="delia",
            nombre="Delia Roget",
            cargo="actriz, invitada de honor de una charla suspendida",
            color="magenta",
            personalidad=(
                "Extravagante, acostumbrada a ser el centro de cualquier salón. "
                "Trata la cuarentena como un papel más que debe interpretar con "
                "dignidad. Le teme, más que a cualquier crimen, a la idea de "
                "envejecer sin público: esta cuarentena, para ella, es apenas "
                "otro escenario reducido donde sigue necesitando que la miren."
            ),
            coartada=(
                "Dice que pasó la noche ensayando un monólogo en voz baja para "
                "no molestar a los demás, y que por eso está segura de haber "
                "estado despierta hasta tarde."
            ),
            actitud=(
                "Teatral y encantadora, pero atenta: es la que más detalles "
                "sueltos nota de los demás, aunque los cuenta como anécdotas de "
                "salón."
            ),
            secretos=[
                Secreto(
                    id="pochettino_inquieto",
                    pista=(
                        "Delia notó a Pochettino visiblemente inquieto la tarde "
                        "anterior al robo, algo impropio de él."
                    ),
                    instruccion_actor=(
                        "Con cualquier pregunta abierta sobre el ambiente esa "
                        "tarde o si notaste algo raro en alguien: contás, con "
                        "tono de anécdota de salón, que Pochettino estaba "
                        "visiblemente inquieto, 'algo impropio de un hombre de "
                        "su temple'."
                    ),
                    criterio_revelacion=(
                        "Menciona haber notado a Pochettino inquieto la tarde "
                        "anterior al robo."
                    ),
                    es_entrada=True,
                    certeza="parcial",
                ),
            ],
            reaccion_acusacion_fallida=(
                "«Qué escena, detective, pero mal dirigida: aplaudieron a la "
                "persona equivocada. La verdadera protagonista de este cuento "
                "sigue libre.»"
            ),
        ),
    ],
)
