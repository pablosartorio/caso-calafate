"""EL CASO TROMEN — sabotaje a la antena del radar 3D, la noche antes de la demo militar.

⚠️ SPOILER: leer los datos de este archivo revela al culpable.
Jugá una partida antes. :)
"""

from caso_calafate.caso import Caso, Secreto, Sospechoso

CASO_TROMEN = Caso(
    id="tromen",
    titulo="EL CASO TROMEN",
    gancho=(
        "A horas de la demo para las Fuerzas Armadas, alguien dejó el radar "
        "más nuevo del país mirando para cualquier lado."
    ),
    briefing=(
        "Zapala, 05:40 de la mañana. Te suena el teléfono en el hotel.\n\n"
        "«Detective, tiene que venir al predio del radar. Ya.»\n\n"
        "En doce horas iba a hacer el primer vuelo de prueba en vivo, delante de "
        "la comitiva de las Fuerzas Armadas, la demostración más importante en la "
        "historia del Sistema Tromen: el radar 3D de vigilancia aérea que la "
        "planta viene desarrollando hace cuatro años. Esta madrugada alguien "
        "entró al predio del radar y dañó el mecanismo de rotación de la "
        "antena. La demo, como mínimo, queda cancelada por semanas.\n\n"
        "Lo que se sabe hasta ahora:\n\n"
        " • Según el primer peritaje, el daño se produjo entre la 01:00 y las 02:00.\n"
        " • La tranquera de servicio del predio del radar registra UNA apertura\n"
        "   en la madrugada, a las 01:15, con el código genérico de mantenimiento\n"
        "   — ese código no identifica a la persona que lo usa.\n"
        " • Sobre el motor de acimut (el que hace girar la antena) se encontraron\n"
        "   marcas de una herramienta específica: una llave dinamométrica que\n"
        "   solo usa el equipo de antena y RF.\n"
        " • Esa noche había tres personas con acceso al predio. Son tus sospechosos.\n\n"
        "Interrogá, anotá, y cuando estés seguro: acusá. Tenés una sola oportunidad."
    ),
    contexto_actores="""\
Esta madrugada, entre la 01:00 y las 02:00, alguien dañó el mecanismo de
rotación de la antena del radar 3D del Sistema Tromen, en el predio del radar
de la planta (cerca de Zapala, Neuquén), horas antes de la demostración en
vivo para una comitiva de las Fuerzas Armadas. La tranquera de servicio del
predio registra una única apertura de madrugada, a la 01:15, con el código
genérico de mantenimiento, que no identifica a quien lo usó. Sobre el motor de
acimut se hallaron marcas de una llave dinamométrica del tipo que solo usa el
equipo de antena y RF. Un detective está interrogando al personal que tenía
acceso al predio esa noche.""",
    epilogo=(
        "Ovidio Melinao saboteó el mecanismo de rotación de la antena.\n\n"
        "Hace un año pidió ser el primer jefe de proyecto del Sistema Tromen — "
        "treinta años de oficio, cada antena de la planta armada con sus propias "
        "manos — y la gerencia le dio el puesto a Valeria Anchorena, una "
        "ingeniera de treinta y dos años recién llegada de otra planta. Se lo "
        "tomó como un insulto que nunca dijo en voz alta, pero que masticó cada "
        "día que vio a Valeria armar el cronograma de la demo.\n\n"
        "La noche anterior retiró del pañol la llave dinamométrica de su kit a "
        "las 20:30, con la excusa de «una revisión pendiente», y a la 01:15 "
        "volvió solo al predio del radar pidiendo el código genérico de la "
        "tranquera de servicio — sin registrar, como exige el protocolo "
        "nocturno, a un segundo técnico. Sabía exactamente qué tornillo aflojar "
        "en el motor de acimut para frenar la rotación sin que se notara a "
        "simple vista: lo suficiente para que la antena fallara delante de la "
        "comitiva y dejara mal parada, específicamente, a la jefa de proyecto "
        "que le había ganado el ascenso. No calculó que el juego del motor sin "
        "ese tornillo iba a forzar el reductor entero: lo que planeó como un "
        "traspié vergonzoso terminó siendo semanas de reparación.\n\n"
        "Walter, el operador de guardia, vio la camioneta de mantenimiento "
        "estacionada junto a la tranquera esa madrugada y no le dio importancia "
        "— los de mantenimiento entran y salen todo el tiempo. Valeria, "
        "mientras tanto, no estaba donde dijo que estaba: se había ido temprano "
        "a ver a su pareja en el pueblo, algo que ocultó por vergüenza y por "
        "conflicto de interés, no porque tuviera nada que ver con el sabotaje.\n\n"
        "Un plan de vieja escuela — delatado por una llave que se olvidó de devolver."
    ),
    max_preguntas=15,
    sospechosos=[
        Sospechoso(
            id="ovidio",
            nombre="Ovidio Melinao",
            cargo="técnico principal de antena y RF",
            color="bright_red",
            es_culpable=True,
            personalidad=(
                "Treinta años en el predio, se conoce cada tuerca del sistema de "
                "memoria. Habla poco y despacio, con desdén contenido hacia «los "
                "que llegaron con el diploma bajo el brazo». Orgulloso de su "
                "oficio, mal genio bien guardado."
            ),
            coartada=(
                "Dice que se fue del predio a las 22:00, como todos los días, y se "
                "quedó solo en su casa del pueblo viendo tele hasta dormirse."
            ),
            actitud=(
                "Si lo presionan sobre su trabajo se pone técnico y desdeñoso, casi "
                "aburrido. Pero si le preguntan por el ascenso, por Valeria, o por "
                "sus herramientas, se cierra, contesta cortante y tarda en mirar a "
                "los ojos antes de aflojar."
            ),
            secretos=[
                Secreto(
                    id="llave_dinamometrica_faltante",
                    pista=(
                        "El kit de herramientas asignado a Ovidio tiene una llave "
                        "dinamométrica sin devolver esa noche: el registro de pañol "
                        "la marca retirada a las 20:30 y nunca reingresada."
                    ),
                    instruccion_actor=(
                        "Solo si te preguntan directamente por tus herramientas, "
                        "por el pañol o por la llave dinamométrica: admitís, "
                        "incómodo, que la retiraste a las 20:30 para «una revisión "
                        "pendiente» y que después te olvidaste de devolverla, como "
                        "pasa siempre. Insistís en que eso no prueba nada."
                    ),
                    criterio_revelacion=(
                        "Admite haber retirado la llave dinamométrica del pañol esa "
                        "noche y no haberla devuelto, o reconoce que la herramienta "
                        "usada en el motor es del tipo que él maneja."
                    ),
                ),
                Secreto(
                    id="acceso_solo_sin_pareja",
                    pista=(
                        "El protocolo exige que de noche nadie entre solo al predio "
                        "del radar; Ovidio pidió el código de la tranquera de "
                        "servicio para una «calibración de rutina» sin registrar un "
                        "segundo técnico, algo prohibido."
                    ),
                    instruccion_actor=(
                        "Si te preguntan si volviste al predio esa noche, o por qué "
                        "pediste el código de la tranquera sin avisarle a nadie: "
                        "reconocés, a regañadientes, que volviste solo cerca de la "
                        "01:15 para una calibración menor que «no ameritaba "
                        "despertar a nadie más», aunque el protocolo de noche pide "
                        "ir de a dos."
                    ),
                    criterio_revelacion=(
                        "Reconoce que volvió solo al predio del radar durante la "
                        "madrugada, o que pidió el acceso sin un segundo técnico "
                        "pese a que el protocolo lo exige."
                    ),
                ),
                Secreto(
                    id="resentimiento_ascenso",
                    pista=(
                        "Ovidio pidió ser jefe de proyecto del Sistema Tromen hace "
                        "un año; el puesto se lo dieron a Valeria Anchorena, más "
                        "joven y venida de otra planta. Nunca lo digirió."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por Valeria, por el proyecto, o por si "
                        "esperabas un ascenso: no podés disimular la amargura. "
                        "Contás que vos pediste ser jefe de proyecto hace un año, "
                        "que treinta años de oficio «no valieron nada» porque se "
                        "lo dieron a alguien de afuera, más joven, «que nunca tocó "
                        "una antena». Aclarás que igual eso no tiene nada que ver "
                        "con lo que pasó."
                    ),
                    criterio_revelacion=(
                        "Cuenta que fue candidato o esperaba ser jefe de proyecto "
                        "y que el puesto se lo dieron a Valeria, mostrando "
                        "resentimiento por el ascenso."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="valeria",
            nombre="Valeria Anchorena",
            cargo="jefa de proyecto del Sistema Tromen",
            color="bright_cyan",
            personalidad=(
                "Treinta y dos años, ingeniera. La trajeron de otra planta hace "
                "seis meses para encabezar el proyecto más grande de su carrera. "
                "Se exige al límite, habla rápido, se pone a la defensiva si "
                "siente que dudan de una autoridad recién estrenada."
            ),
            coartada=(
                "Dice que se quedó en la oficina de proyecto revisando el "
                "cronograma de la demo hasta la 01:30, y después se fue directo a "
                "dormir al alojamiento de planta."
            ),
            actitud=(
                "Si la presionan sobre su gestión se pone firme y cita el "
                "cronograma. Pero si le preguntan por el horario exacto en que se "
                "fue, o por su relación con Ovidio, se pone tensa, tarda en "
                "contestar y termina sincerándose."
            ),
            secretos=[
                Secreto(
                    id="salida_antes_de_lo_dicho",
                    pista=(
                        "Valeria no se quedó hasta la 01:30 como dijo: salió del "
                        "predio poco después de las 23:00 y no volvió hasta pasadas "
                        "las 06:00, cuando ya se había dado la alarma."
                    ),
                    instruccion_actor=(
                        "Solo si te preguntan por tu horario exacto de salida, o si "
                        "notan que no hay registro tuyo en el predio después de las "
                        "23:00: admitís, incómoda, que en realidad te fuiste bastante "
                        "antes de lo que dijiste primero, cerca de las 23:00, y que "
                        "volviste recién con la alarma. No es delito, pero te da "
                        "vergüenza porque «la jefa de proyecto debería haberse "
                        "quedado»."
                    ),
                    criterio_revelacion=(
                        "Admite que en realidad se retiró del predio antes de lo "
                        "que había declarado (cerca de las 23:00) y no cerca de la "
                        "01:30."
                    ),
                ),
                Secreto(
                    id="donde_estuvo_realmente",
                    pista=(
                        "Esas horas de la madrugada las pasó en el pueblo, con su "
                        "pareja, de quien nadie en la planta sabe todavía porque "
                        "trabaja para una empresa competidora del proyecto."
                    ),
                    instruccion_actor=(
                        "Solo si insisten en dónde estuviste exactamente esas horas "
                        "que faltan, después de que ya admitiste que te fuiste "
                        "antes: contás, muy incómoda y pidiendo discreción, que "
                        "estuviste con tu pareja, que trabaja para una empresa "
                        "competidora, y que no lo blanqueaste en la planta por el "
                        "conflicto de interés. Jurás que no tiene nada que ver con "
                        "el sabotaje."
                    ),
                    criterio_revelacion=(
                        "Revela que pasó esas horas con su pareja, que trabaja "
                        "para una empresa competidora, y que ocultó la relación "
                        "por conflicto de interés."
                    ),
                ),
                Secreto(
                    id="advertencia_de_ovidio",
                    pista=(
                        "Cuatro días antes, delante de otro técnico, Ovidio le dijo "
                        "a Valeria que «esta demo se les puede complicar más de lo "
                        "que piensan» — algo que en su momento pareció una crítica "
                        "técnica más."
                    ),
                    instruccion_actor=(
                        "Si te preguntan si notaste tensión con el personal, o "
                        "específicamente con Ovidio, o si alguien te advirtió antes "
                        "de la demo: contás que días atrás Ovidio te dijo, medio en "
                        "broma medio en serio, que «la demo se les podía complicar "
                        "más de lo que pensaban». En su momento lo tomaste como la "
                        "crítica de alguien golpeado por no haber sido ascendido, "
                        "no como una amenaza."
                    ),
                    criterio_revelacion=(
                        "Menciona que Ovidio le hizo un comentario o advertencia "
                        "días antes sobre que la demostración «se les podía "
                        "complicar», vinculado a su resentimiento por no haber "
                        "sido ascendido."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="walter",
            nombre="Walter Currumil",
            cargo="operador de guardia, sala de control del predio Tromen",
            color="bright_yellow",
            personalidad=(
                "Veintitrés años, primer año en la planta. Nervioso, atropellado, "
                "quiere caer bien y habla de más cuando se pone ansioso. Buen pibe."
            ),
            coartada=(
                "Dice que estuvo toda la noche en la sala de control monitoreando "
                "las pantallas y que no vio entrar ni salir a nadie por la "
                "tranquera principal."
            ),
            actitud=(
                "Cuanto más lo presionan, más se enreda y se contradice. Si le "
                "marcan una inconsistencia horaria o un registro que falta, se "
                "quiebra rápido y confiesa, pidiendo que no lo echen."
            ),
            secretos=[
                Secreto(
                    id="ronda_no_hecha",
                    pista=(
                        "El protocolo exige una ronda visual al predio del radar "
                        "cada hora; Walter no hizo la ronda de la 01:00 porque se "
                        "quedó mirando un partido en el celular."
                    ),
                    instruccion_actor=(
                        "Al principio negás cualquier falla («hice todo como "
                        "corresponde»). Si te presionan sobre las rondas, los "
                        "horarios, o notan que falta un registro: confesás, con "
                        "culpa, que la ronda de la 01:00 no la hiciste porque te "
                        "quedaste viendo un partido de fútbol en el celular, y que "
                        "fue la única que te salteaste en toda la noche."
                    ),
                    criterio_revelacion=(
                        "Admite que no realizó la ronda de vigilancia programada "
                        "(la de la 01:00) porque estaba distraído con el celular."
                    ),
                ),
                Secreto(
                    id="camioneta_estacionada",
                    pista=(
                        "Cerca de la 01:10, desde la ventana de la sala de "
                        "control, Walter vio la camioneta de mantenimiento "
                        "estacionada junto a la tranquera de servicio del predio "
                        "del radar, con las balizas apagadas."
                    ),
                    instruccion_actor=(
                        "Solo si te preguntan si viste algo raro esa noche, o "
                        "específicamente si viste vehículos o movimiento cerca de "
                        "la tranquera de servicio: contás que, de pasada, viste la "
                        "camioneta de mantenimiento estacionada ahí cerca de la "
                        "01:10, con las balizas apagadas, pero que no le diste "
                        "importancia porque «los de mantenimiento entran y salen "
                        "todo el tiempo»."
                    ),
                    criterio_revelacion=(
                        "Menciona haber visto la camioneta de mantenimiento "
                        "estacionada junto a la tranquera de servicio cerca de la "
                        "01:10."
                    ),
                ),
            ],
        ),
    ],
)
