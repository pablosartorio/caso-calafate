"""EL CASO FRÍAS — homenaje a Jorge Luis Borges (La muerte y la brújula).

Una serie de incidentes cuyas fechas y ubicaciones dibujan, en el mapa del
predio, un patrón geométrico perfecto. El patrón no es una pista: es una
trampa tendida para atraer a alguien a un punto exacto.

⚠️ SPOILER: leer los datos de este archivo revela al culpable.
Jugá una partida antes. :)
"""

from caso_calafate.caso import Caso, Secreto, Sospechoso

CASO_FRIAS = Caso(
    id="frias",
    titulo="EL CASO FRÍAS",
    sede="Estación de Rastreo Satelital Lago Frías",
    ciudad="Bariloche",
    delito="la serie de sabotajes con patrón",
    culpable_alias="estratega",
    gancho=(
        "Tres incidentes, tres fechas, tres puntos del predio — y sobre el "
        "mapa, dibujan un triángulo perfecto que apunta a un cuarto punto."
    ),
    briefing=(
        "Estación de Rastreo Satelital, Lago Frías. Te llaman a la mañana "
        "después del tercer incidente.\n\n"
        "«Detective, no son sabotajes sueltos. Marcamos las fechas y las "
        "ubicaciones en el mapa del predio y forman una figura. Y la figura "
        "no está completa.»\n\n"
        "En dos semanas hubo tres incidentes menores — un cable cortado, una "
        "antena desalineada, un archivo borrado — en tres puntos distintos "
        "del predio, cada uno en la madrugada de un día par. Marcados en el "
        "mapa, los tres puntos forman un triángulo casi perfecto. Extendiendo "
        "sus líneas, hay un cuarto punto exacto donde debería pasar algo "
        "esta noche: la sala de control principal.\n\n"
        "Lo que se sabe hasta ahora:\n\n"
        " • Los tres incidentes previos fueron menores, casi simbólicos.\n"
        " • Cada uno coincidió con el turno de una persona distinta.\n"
        " • Alguien, adentro, conoce el patrón tan bien como para haberlo\n"
        "   trazado él mismo.\n"
        " • El patrón no parece pensado solo para señalar un lugar: parece\n"
        "   pensado para asegurarse de que alguien viniera a investigar\n"
        "   justo esta noche, a ese cuarto punto.\n"
        " • Cinco personas tienen acceso a los tres puntos marcados. Son tus\n"
        "   sospechosos.\n\n"
        "Interrogá, anotá, y cuando estés seguro: acusá. Tenés una sola oportunidad."
    ),
    contexto_actores="""\
En dos semanas hubo tres incidentes menores en la Estación de Rastreo
Satelital del Lago Frías (Bariloche), cada uno en un punto distinto del predio
y en la madrugada de un día par. Marcados en el mapa, los tres puntos forman
un triángulo casi perfecto que, extendido, señala un cuarto punto exacto: la
sala de control principal, esta noche. Un detective interroga a las cinco
personas con acceso a los tres puntos marcados.""",
    epilogo=(
        "Yago Scharrer trazó el patrón para exponer a Martín Kreiman.\n\n"
        "Matemático obsesivo, llevaba años convencido de que Kreiman le había "
        "robado la autoría real de un método de rastreo que ambos habían "
        "desarrollado juntos años atrás, y que la Estación solo reconocía a "
        "Kreiman. No tenía pruebas que alguien fuera a creerle si las "
        "presentaba directamente — así que decidió construir una prueba que "
        "nadie pudiera ignorar: un patrón geométrico tan preciso que "
        "obligara a que un detective apareciera. Provocó él mismo los tres "
        "incidentes menores, cronometrados con precisión para dibujar el "
        "triángulo, calculando el día exacto en que un investigador serio "
        "terminaría marcando el cuarto punto — la sala de control — y se "
        "presentaría ahí esa noche en particular. No le bastaba con que el "
        "patrón señalara un lugar: necesitaba atraer al detective hasta ese "
        "lugar, como testigo obligado, para dejarle ahí mismo, a la vista, "
        "las pruebas reales del plagio de Kreiman, disfrazadas de "
        "'hallazgo' del cuarto incidente.\n\n"
        "El cabo Ezcurra, que creyó en el patrón desde el primer día, no "
        "estaba tan equivocado: el patrón era real. Solo se equivocó en "
        "pensar que apuntaba a la próxima víctima, y no a su autor."
    ),
    max_preguntas=15,
    sospechosos=[
        Sospechoso(
            id="yago",
            nombre="Yago Scharrer",
            cargo="matemático de la Estación",
            color="cyan",
            es_culpable=True,
            personalidad=(
                "Frío, preciso, incapaz de dejar pasar un error de cálculo ajeno "
                "sin corregirlo en voz alta. Habla de números como quien habla de "
                "justicia. Se convenció de que un cálculo bien hecho es una forma "
                "superior de verdad, y que armar el patrón no fue sabotear nada: "
                "fue, para él, la única demostración que Kreiman no podría "
                "desacreditar con un cargo o un apellido. No se piensa como "
                "alguien que dañó la Estación, sino como el único ahí adentro "
                "dispuesto a pagar el precio de que se supiera la verdad."
            ),
            coartada=(
                "Dice que pasó cada una de las tres noches trabajando solo en su "
                "oficina, en un proyecto que no quiere detallar todavía."
            ),
            actitud=(
                "Explica el patrón geométrico con un entusiasmo casi orgulloso, "
                "como si fuera un problema elegante y no un crimen. Si le "
                "preguntan por Kreiman, se pone tenso y frío de golpe."
            ),
            secretos=[
                Secreto(
                    id="metodo_robado",
                    pista=(
                        "Yago está convencido de que Martín Kreiman se atribuyó "
                        "un método de rastreo que ambos desarrollaron juntos años "
                        "atrás."
                    ),
                    instruccion_actor=(
                        "Con cualquier pregunta abierta sobre Kreiman o sobre "
                        "tu trabajo en la Estación: contás, con amargura "
                        "contenida, que Kreiman se atribuyó un método que "
                        "desarrollaron juntos, y que la Estación solo lo reconoce "
                        "a él."
                    ),
                    criterio_revelacion=(
                        "Cuenta que cree que Martín Kreiman se atribuyó un "
                        "método que desarrollaron juntos."
                    ),
                    es_entrada=True,
                    certeza="parcial",
                ),
                Secreto(
                    id="patron_propio",
                    pista=(
                        "Yago calculó personalmente, hace semanas, el triángulo "
                        "geométrico que forman los tres incidentes."
                    ),
                    instruccion_actor=(
                        "Solo si ya te habló del conflicto con Kreiman Y le "
                        "preguntan directamente si él trazó el patrón: admite, "
                        "con una calma inquietante, que sí, que calculó el "
                        "triángulo hace semanas — 'la geometría no miente, "
                        "aunque las personas sí'."
                    ),
                    criterio_revelacion=(
                        "Admite haber calculado o trazado él mismo el patrón "
                        "geométrico de los incidentes."
                    ),
                    certeza="confirmado",
                ),
            ],
            reaccion_acusacion_fallida=(
                "«La geometría no miente. Ustedes, en cambio, acaban de "
                "demostrar que sí se equivocan.»"
            ),
        ),
        Sospechoso(
            id="dahlia",
            nombre="Dahlia Reinoso",
            cargo="jefa de seguridad de la Estación",
            color="yellow",
            personalidad=(
                "Escéptica por oficio, desconfía de las explicaciones demasiado "
                "elegantes. Prefiere la evidencia aburrida a la teoría vistosa. "
                "Hace años, en otro destino, avaló una hipótesis vistosa que "
                "resultó falsa y le costó un ascenso; desde entonces no vuelve a "
                "confiar en ninguna teoría hasta que no la desarma con sus "
                "propias manos, y teme, en el fondo, que esta vez el patrón sea "
                "real y ella no lo vea a tiempo otra vez."
            ),
            coartada=(
                "Dice que estuvo de guardia normal las tres noches, sin ver nada "
                "que le llamara la atención en su momento."
            ),
            actitud=(
                "Responde con pragmatismo y cierto fastidio hacia la idea del "
                "patrón. Si le muestran el mapa, lo analiza en serio, sin "
                "prejuicio."
            ),
            secretos=[
                Secreto(
                    id="descarta_patron",
                    pista=(
                        "Dahlia cree que el 'patrón' es una coincidencia y que "
                        "alguien lo está usando para distraer de un motivo más "
                        "simple."
                    ),
                    instruccion_actor=(
                        "Con cualquier pregunta abierta sobre el caso o sobre "
                        "el patrón geométrico: decís, con escepticismo "
                        "profesional, que puede ser una coincidencia forzada "
                        "por alguien que quiere hacer parecer esto más "
                        "complicado de lo que es."
                    ),
                    criterio_revelacion=(
                        "Expresa que sospecha que el patrón es artificial, hecho "
                        "a propósito para distraer."
                    ),
                    es_entrada=True,
                    certeza="ambiguo",
                ),
            ],
            reaccion_acusacion_fallida=(
                "«Se los dije: la teoría más vistosa casi nunca es la "
                "correcta. Deberían haber escuchado a la aburrida.»"
            ),
        ),
        Sospechoso(
            id="ezcurra",
            nombre="Cabo Ezcurra",
            cargo="seguridad de turno",
            color="green",
            personalidad=(
                "Crédulo, entusiasta, el primero en creer en la teoría del "
                "patrón geométrico. Se toma la investigación como algo personal. "
                "Es el más joven de guardia y los veteranos lo tratan como un "
                "pibe que todavía no se ganó el respeto del uniforme; sueña con "
                "ser el que resuelve el caso él solo, aunque eso signifique "
                "creer un poco demasiado rápido en la primera teoría elegante "
                "que aparece."
            ),
            coartada=(
                "Dice que estuvo en su puesto las tres noches y que fue él quien "
                "notó primero que las fechas coincidían con días pares."
            ),
            actitud=(
                "Entusiasmado con cualquier avance en la teoría del patrón. Si "
                "le muestran que se equivoca en algo, se pone dócil y "
                "colaborador, nunca defensivo."
            ),
            secretos=[
                Secreto(
                    id="cuarto_punto",
                    pista=(
                        "Ezcurra fue el primero en calcular que el cuarto punto "
                        "del patrón caía exactamente en la sala de control "
                        "principal."
                    ),
                    instruccion_actor=(
                        "Con cualquier pregunta abierta sobre el patrón o "
                        "sobre cómo diste con el cuarto punto: contás, con "
                        "orgullo, que fuiste vos mismo, extendiendo las líneas "
                        "del triángulo sobre el mapa del predio."
                    ),
                    criterio_revelacion=(
                        "Cuenta que él mismo calculó que el cuarto punto del "
                        "patrón caía en la sala de control."
                    ),
                    es_entrada=True,
                    certeza="parcial",
                ),
            ],
            reaccion_acusacion_fallida=(
                "«¡Yo tenía razón con el patrón! Lo del cuarto punto no falló. "
                "Ustedes sí, con el nombre.»"
            ),
        ),
        Sospechoso(
            id="martin",
            nombre="Martín Kreiman",
            cargo="jefe del área de rastreo",
            color="red",
            personalidad=(
                "Seguro de sí, algo distante, acostumbrado a que le reconozcan "
                "logros ajenos sin que nadie se lo cuestione. Bajo esa "
                "seguridad hay temor genuino de no dar la talla: la dirección "
                "espera de él resultados que, sospecha en privado, en parte le "
                "debe al trabajo de Yago — y prefiere no examinarlo demasiado "
                "de cerca antes que confirmar sus propias dudas."
            ),
            coartada=(
                "Dice que estuvo de viaje en Buenos Aires durante los primeros "
                "dos incidentes, y en la Estación pero sin salir de su oficina "
                "durante el tercero."
            ),
            actitud=(
                "Cordial y algo condescendiente. Si le preguntan por Yago o por "
                "el método de rastreo, se pone incómodo y minimiza el tema."
            ),
            secretos=[
                Secreto(
                    id="conflicto_yago",
                    pista=(
                        "Martín sabe que Yago Scharrer lo acusa, en privado, de "
                        "haberse atribuido un método que desarrollaron juntos."
                    ),
                    instruccion_actor=(
                        "Con cualquier pregunta abierta sobre Yago o sobre el "
                        "método de rastreo: admitís, incómodo, que sabés que "
                        "te acusa en privado de atribuirte un método que "
                        "hicieron juntos, pero decís que 'la autoría se decide "
                        "con papeles, no con quejas'."
                    ),
                    criterio_revelacion=(
                        "Admite conocer la acusación de Yago Scharrer sobre la "
                        "autoría del método."
                    ),
                    es_entrada=True,
                    certeza="parcial",
                ),
            ],
            reaccion_acusacion_fallida=(
                "«La autoría se decide con papeles, dije. Y los papeles, "
                "visto lo visto, tampoco eran míos para acusar a nadie.»"
            ),
        ),
        Sospechoso(
            id="perla",
            nombre="Perla Anzoátegui",
            cargo="archivista de la Estación",
            color="magenta",
            personalidad=(
                "Metódica, guarda cada mapa y cada plano del predio como un "
                "tesoro personal. Le cuesta admitir cuando algo se le escapó. "
                "Lleva más de veinte años catalogando a mano cada rincón de la "
                "Estación, orgullosa de ser la única que conoce el predio real "
                "y no el que figura en los planos oficiales; le pesa no "
                "haberse preguntado, en su momento, por qué alguien quería "
                "justamente ese mapa con tanto detalle."
            ),
            coartada=(
                "Dice que estuvo en el archivo las tres noches, catalogando "
                "planos viejos, y que no vio a nadie fuera de hora."
            ),
            actitud=(
                "Cuidadosa con los datos, algo posesiva con sus archivos. Si "
                "le preguntan quién pidió mapas del predio últimamente, "
                "recuerda con precisión de archivista."
            ),
            secretos=[
                Secreto(
                    id="mapa_pedido",
                    pista=(
                        "Yago Scharrer le pidió a Perla, hace un mes, una copia "
                        "detallada del mapa del predio 'para un cálculo "
                        "personal'."
                    ),
                    instruccion_actor=(
                        "Si te preguntan si alguien pidió mapas del predio "
                        "últimamente: contás, con tu precisión habitual, que "
                        "Yago te pidió una copia detallada hace un mes, para "
                        "'un cálculo personal' que no quiso explicar."
                    ),
                    criterio_revelacion=(
                        "Cuenta que Yago Scharrer le pidió una copia detallada "
                        "del mapa del predio hace un mes."
                    ),
                    es_entrada=True,
                    certeza="parcial",
                ),
            ],
            reaccion_acusacion_fallida=(
                "«Yo archivo lo que me piden, detective. Si alguien usó un "
                "mapa mío para algo turbio, la culpa es de quien lo usó, no "
                "de quien lo guardó.»"
            ),
        ),
    ],
)
