"""EL CASO MORENO — homenaje a Sergio Olguín (Verónica Rosenthal / La
fragilidad de los cuerpos).

Una periodista invitada empieza a tirar del hilo de un fraude que nadie le
pidió investigar, y termina destapando algo que la propia base prefería
mantener bajo el hielo.

⚠️ SPOILER: leer los datos de este archivo revela al culpable.
Jugá una partida antes. :)
"""

from caso_calafate.caso import Caso, Secreto, Sospechoso

CASO_MORENO = Caso(
    id="moreno",
    titulo="EL CASO MORENO",
    sede="Base de Monitoreo Glaciológico Perito Moreno",
    ciudad="El Calafate",
    delito="el fraude en los fondos de la base",
    culpable_alias="estafador",
    gancho=(
        "Una periodista invitada a cubrir el monitoreo satelital del glaciar "
        "empieza a notar que los números de la base no cierran."
    ),
    briefing=(
        "Base de Monitoreo Glaciológico Perito Moreno. Te llaman a la tarde, "
        "con la base en alerta.\n\n"
        "«Detective, una periodista que vino a cubrir el monitoreo satelital "
        "encontró algo en los registros de compras. Y alguien intentó "
        "borrarle las notas del cuaderno.»\n\n"
        "La periodista, invitada por el propio Centro Espacial para una nota "
        "sobre el uso de imágenes satelitales en el estudio del glaciar, "
        "empezó a cruzar facturas de mantenimiento con el estado real de los "
        "equipos, y algo no cerraba. Anoche, alguien entró a su cuarto y "
        "arrancó varias páginas de su cuaderno de notas.\n\n"
        "Lo que se sabe hasta ahora:\n\n"
        " • Las facturas de mantenimiento de los últimos dos años son mucho\n"
        "   más altas de lo que el estado de los equipos justifica.\n"
        " • Solo un puñado de personas maneja los contratos de mantenimiento\n"
        "   de la base.\n"
        " • El cuarto de la periodista no fue forzado: alguien tenía llave o\n"
        "   pasó desapercibido.\n"
        " • Cinco personas de la base tuvieron acceso a su cuarto o a los\n"
        "   contratos. Son tus sospechosos.\n\n"
        "Interrogá, anotá, y cuando estés seguro: acusá. Tenés una sola oportunidad."
    ),
    contexto_actores="""\
Una periodista invitada por el Centro Espacial a cubrir el monitoreo
satelital del glaciar, en la Base de Monitoreo Glaciológico Perito Moreno (El
Calafate), notó que las facturas de mantenimiento de los últimos dos años son
mucho más altas de lo que justifica el estado real de los equipos. Anoche
alguien entró a su cuarto, sin forzarlo, y arrancó páginas de su cuaderno de
notas. Un detective interroga a las cinco personas con acceso a su cuarto o a
los contratos de mantenimiento. La base queda a horas de cualquier ciudad,
rodeada de hielo y sin más compañía que el viento: para la prensa que la
visita es una postal de prestigio científico, puertas adentro esa misma
distancia es la que le permitió a alguien vaciar las cuentas de mantenimiento
durante dos años sin que nadie de afuera preguntara.""",
    epilogo=(
        "Franco Islas infló las facturas de mantenimiento durante dos años.\n\n"
        "Contratista privado a cargo del mantenimiento de los equipos de la "
        "base, facturaba repuestos y horas de trabajo que nunca se hacían, "
        "quedándose con la diferencia junto a un cómplice externo que nunca "
        "llegó a identificarse del todo. Cuando se enteró de que la "
        "periodista cruzaba facturas con el estado real del equipamiento, "
        "entró a su cuarto de madrugada — tenía una copia de todas las "
        "llaves de la base, por su trabajo — y arrancó las páginas del "
        "cuaderno donde ella había empezado a anotar las inconsistencias, "
        "esperando que pareciera un episodio menor y sin sentido, no un "
        "encubrimiento.\n\n"
        "Anselmo Duarte, jefe de base, había notado hacía meses que los "
        "números no cerraban del todo, pero prefirió no indagar: Franco era "
        "el único contratista dispuesto a trabajar en un lugar tan aislado, y "
        "reemplazarlo hubiera significado meses sin mantenimiento real."
    ),
    max_preguntas=15,
    sospechosos=[
        Sospechoso(
            id="julieta",
            nombre="Julieta Farhi",
            cargo="periodista invitada",
            color="cyan",
            personalidad=(
                "Curiosa hasta la obsesión, no suelta un dato raro aunque nadie "
                "más le preste atención. Acostumbrada a que la subestimen. "
                "Lleva años cubriendo notas de color que nadie recuerda al día "
                "siguiente y quiere, por una vez, una nota que importe; le "
                "aterra volver a Buenos Aires con la misma libreta vacía de "
                "siempre."
            ),
            coartada=(
                "No es sospechosa en el sentido clásico: es quien destapó el "
                "fraude, y cuenta con detalle todo lo que encontró."
            ),
            actitud=(
                "Colaborativa y precisa, encantada de compartir cada dato que "
                "cruzó en sus notas. La única que no tiene nada que ocultar."
            ),
            secretos=[
                Secreto(
                    id="facturas_infladas",
                    pista=(
                        "Las facturas de mantenimiento de los últimos dos años "
                        "son muchísimo más altas de lo que el estado real de los "
                        "equipos justifica."
                    ),
                    instruccion_actor=(
                        "Con cualquier pregunta abierta sobre qué encontraste, "
                        "por qué te llamaron o en qué estabas trabajando: "
                        "explicás, con entusiasmo periodístico, que las "
                        "facturas de mantenimiento de dos años son muchísimo "
                        "más altas de lo que el estado real de los equipos "
                        "justifica."
                    ),
                    criterio_revelacion=(
                        "Explica que las facturas de mantenimiento están "
                        "infladas respecto al estado real de los equipos."
                    ),
                    es_entrada=True,
                    certeza="parcial",
                ),
            ],
            reaccion_acusacion_fallida=(
                "«¿Yo? Yo solo hago preguntas, detective. Parece que a alguien "
                "más le van a tener que hacer unas cuantas más.»"
            ),
        ),
        Sospechoso(
            id="anselmo",
            nombre="Anselmo Duarte",
            cargo="jefe de la base",
            color="yellow",
            personalidad=(
                "Pragmático, agotado por la logística de mantener una base "
                "aislada funcionando. Elige sus batallas con cuidado. Lleva "
                "quince años lejos de su familia por esta base y le queda "
                "poco antes del retiro; teme que un escándalo de fraude bajo "
                "su gestión le arruine la salida, así que prioriza que todo "
                "siga funcionando por sobre hacer las preguntas incómodas."
            ),
            coartada=(
                "Dice que esa noche estaba en su oficina, revisando turnos "
                "para la semana, y no se cruzó con la periodista."
            ),
            actitud=(
                "Cordial pero cansado. Si le preguntan por qué no controló "
                "mejor las facturas, se pone incómodo y justifica la falta de "
                "opciones."
            ),
            secretos=[
                Secreto(
                    id="sospecha_previa",
                    pista=(
                        "Anselmo sospechaba hace meses que los números de "
                        "mantenimiento no cerraban del todo, pero no investigó."
                    ),
                    instruccion_actor=(
                        "Con cualquier pregunta abierta sobre las cuentas de "
                        "la base o sobre si notaste algo raro antes de esto: "
                        "admitís, incómodo, que sospechabas algo hace meses "
                        "pero no investigaste, porque Franco era el único "
                        "contratista dispuesto a venir hasta acá y te quedaban "
                        "pocos años para el retiro como para abrir ese frente."
                    ),
                    criterio_revelacion=(
                        "Admite haber sospechado antes de irregularidades en las "
                        "cuentas de mantenimiento."
                    ),
                    es_entrada=True,
                    certeza="parcial",
                ),
            ],
            reaccion_acusacion_fallida=(
                "«Yo cargué esta base quince años sin que se me cayera nada "
                "encima. No pienso cargar también con esto, detective.»"
            ),
        ),
        Sospechoso(
            id="franco",
            nombre="Franco Islas",
            cargo="contratista de mantenimiento",
            color="red",
            es_culpable=True,
            personalidad=(
                "Simpático y servicial en apariencia, el único dispuesto a "
                "trabajar en un lugar tan aislado. Conoce cada rincón de la "
                "base. Se convenció, con el tiempo, de que nadie más soportaría "
                "el frío, la distancia y los meses sin ver a su familia por lo "
                "que le pagan, y que 'inflar un poco' las facturas era apenas "
                "cobrarse el verdadero costo de estar acá — nunca lo piensa "
                "como robarle a nadie en particular, sino como cobrarse algo "
                "que la base de todos modos le debía."
            ),
            coartada=(
                "Dice que esa noche estaba revisando un generador en el otro "
                "extremo de la base, lejos de los dormitorios."
            ),
            actitud=(
                "Servicial y colaborador de entrada. Si lo confrontan con "
                "números concretos de facturación, se pone técnico y evasivo."
            ),
            secretos=[
                Secreto(
                    id="llaves_todas",
                    pista=(
                        "Franco tiene copia de todas las llaves de la base, "
                        "incluidos los dormitorios, por su trabajo de "
                        "mantenimiento."
                    ),
                    instruccion_actor=(
                        "Con cualquier pregunta abierta sobre tu acceso a la "
                        "base o a los dormitorios: admitís, sin darle mayor "
                        "importancia, que tenés copia de todas las llaves de "
                        "la base por tu trabajo."
                    ),
                    criterio_revelacion=(
                        "Admite tener copia de todas las llaves de la base, "
                        "incluidos los dormitorios."
                    ),
                    es_entrada=True,
                    certeza="parcial",
                ),
                Secreto(
                    id="cobros_inexistentes",
                    pista=(
                        "Franco facturó repuestos y horas de trabajo que nunca "
                        "se realizaron, quedándose con la diferencia."
                    ),
                    instruccion_actor=(
                        "Solo si ya admitiste lo de las llaves Y te muestran un "
                        "dato concreto de una factura específica: te quebrás y "
                        "admitís que facturaste repuestos y horas que nunca se "
                        "hicieron."
                    ),
                    criterio_revelacion=(
                        "Admite haber facturado repuestos u horas de trabajo "
                        "inexistentes."
                    ),
                    certeza="confirmado",
                ),
            ],
            reaccion_acusacion_fallida=(
                "«¿Yo? Con lo que me pagan por venir hasta acá, ya bastante "
                "hago con no cobrarles el doble, detective.»"
            ),
        ),
        Sospechoso(
            id="cielo",
            nombre="Cielo Manqueo",
            cargo="bióloga de la base",
            color="green",
            personalidad=(
                "Observadora, ajena a los conflictos administrativos, más "
                "interesada en el hielo que en las cuentas. Honesta casi hasta "
                "la ingenuidad. Perdió su beca de investigación en la "
                "universidad hace dos años y esta base es su única chance de "
                "seguir estudiando el glaciar antes de que el retroceso lo "
                "cambie para siempre; le preocupa más eso que cualquier "
                "chisme administrativo."
            ),
            coartada=(
                "Dice que esa noche estaba en el laboratorio, procesando "
                "muestras, y no se cruzó con nadie."
            ),
            actitud=(
                "Directa y sin nada que ocultar sobre sí misma, aunque nota "
                "detalles ajenos sin darles demasiada importancia."
            ),
            secretos=[
                Secreto(
                    id="franco_nocturno",
                    pista=(
                        "Cielo vio a Franco Islas merodeando cerca de los "
                        "dormitorios esa noche, algo que no era parte de su "
                        "rutina de trabajo."
                    ),
                    instruccion_actor=(
                        "Con cualquier pregunta abierta sobre esa noche o "
                        "sobre si viste a alguien fuera de lugar: contás, sin "
                        "darle mucha importancia en el momento, que viste a "
                        "Franco merodeando cerca de los dormitorios."
                    ),
                    criterio_revelacion=(
                        "Menciona haber visto a Franco Islas merodeando cerca "
                        "de los dormitorios esa noche."
                    ),
                    es_entrada=True,
                    certeza="parcial",
                ),
            ],
            reaccion_acusacion_fallida=(
                "«Yo solo cuento lo que veo. Si se equivocaron de persona, "
                "no fue por algo que yo dije.»"
            ),
        ),
        Sospechoso(
            id="rulo",
            nombre="Rulo Estévez",
            cargo="piloto del helicóptero de la base",
            color="magenta",
            personalidad=(
                "Relajado, el que más tiempo lleva en la base, conoce todas las "
                "rutinas y horarios de todos. Manda casi todo lo que gana a su "
                "familia en el norte, endeudada desde hace años; volar es lo "
                "único que sabe hacer y le aterra más perder la licencia por "
                "algún quilombo ajeno que cualquier otra cosa."
            ),
            coartada=(
                "Dice que esa noche estaba haciendo mantenimiento de rutina al "
                "helicóptero, en el hangar, hasta tarde."
            ),
            actitud=(
                "Colaborador y observador. Si le preguntan por rutinas o "
                "movimientos de otros, responde con precisión de quien lleva "
                "años prestando atención al detalle."
            ),
            secretos=[
                Secreto(
                    id="franco_conoce_llaves",
                    pista=(
                        "Rulo sabe, por haber trabajado con él, que Franco "
                        "Islas es el único que tiene copia de todas las llaves "
                        "de la base."
                    ),
                    instruccion_actor=(
                        "Con cualquier pregunta abierta sobre quién tiene "
                        "acceso a los distintos sectores de la base: contás, "
                        "con seguridad, que solo Franco Islas tiene copia de "
                        "todas las llaves, por su trabajo de mantenimiento."
                    ),
                    criterio_revelacion=(
                        "Cuenta que Franco Islas es el único con copia de "
                        "todas las llaves de la base."
                    ),
                    es_entrada=True,
                    certeza="parcial",
                ),
            ],
            reaccion_acusacion_fallida=(
                "«Yo vuelo el helicóptero, no las cuentas de la base. Se "
                "olvidaron de preguntarle a quien las maneja de verdad.»"
            ),
        ),
    ],
)
