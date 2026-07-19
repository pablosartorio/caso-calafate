"""EL CASO PENITENTES — filtración de las especificaciones del radar Centinela-3D.

⚠️ SPOILER: leer los datos de este archivo revela al culpable.
Jugá una partida antes. :)
"""

from caso_calafate.caso import Caso, Secreto, Sospechoso

CASO_PENITENTES = Caso(
    id="penitentes",
    titulo="EL CASO PENITENTES",
    gancho=(
        "A 72 horas de la demo para las Fuerzas Armadas, alguien vendió "
        "los planos del radar por afuera."
    ),
    briefing=(
        "San Carlos de Bariloche, lunes 07:15. Te suena el teléfono en pleno desayuno.\n\n"
        "«Detective, tenemos un quilombo serio en la Planta Los Penitentes. Mejor "
        "venga.»\n\n"
        "A 72 horas de la demostración del nuevo radar 3D de vigilancia aérea "
        "Centinela-3D ante una comisión de las Fuerzas Armadas, el área de "
        "Seguridad Informática detectó que alguien accedió a la carpeta de "
        "especificaciones técnicas confidenciales del proyecto durante el fin "
        "de semana — y las copió a un pendrive que no figura en el inventario "
        "serializado de la planta.\n\n"
        "Lo que se sabe hasta ahora:\n\n"
        " • El acceso a la carpeta ocurrió el sábado a las 23:14.\n"
        " • El sistema de alerta de dispositivos externos (el que debería haber\n"
        "   bloqueado ese pendrive) estuvo desactivado entre las 22:00 y la 01:00\n"
        "   de esa misma noche.\n"
        " • El registro marca que el acceso a la carpeta se hizo con las\n"
        "   credenciales de Marcela Suárez, la ingeniera a cargo del diseño del\n"
        "   Centinela-3D.\n"
        " • Esa noche había guardia de mantenimiento de sistemas en la planta;\n"
        "   nadie más figura en los registros de acceso físico al edificio.\n"
        " • Tres personas tenían acceso a esa carpeta o a esos sistemas ese fin\n"
        "   de semana. Son tus sospechosos.\n\n"
        "Interrogá, anotá, y cuando estés seguro: acusá. Tenés una sola oportunidad."
    ),
    contexto_actores="""\
El sábado a las 23:14, alguien accedió a la carpeta de especificaciones técnicas
confidenciales del radar Centinela-3D en la Planta Los Penitentes y las copió a
un pendrive que no figura en el inventario serializado de la planta. El sistema
de alerta de dispositivos externos estuvo desactivado entre las 22:00 y la 01:00
de esa noche. El acceso a la carpeta quedó registrado con las credenciales de
Marcela Suárez, ingeniera a cargo del proyecto. Un detective está interrogando
al personal que tenía acceso a esa carpeta o a esos sistemas ese fin de semana.""",
    epilogo=(
        "Ricardo Bianchi vendió los planos del Centinela-3D.\n\n"
        "Hacía meses que acumulaba deudas de juego — carreras, alguna apuesta "
        "online, un fin de semana catastrófico en un casino de Neuquén que no le "
        "contó ni a la mujer. Un contacto que se presentó como «representante "
        "comercial» de un comprador extranjero le ofreció una cifra que cubría "
        "todo, a cambio de las especificaciones técnicas completas del radar "
        "antes de la demo a las Fuerzas Armadas: cuanto antes, mejor precio.\n\n"
        "Como jefe de Compras y Vinculación con Contratistas, Ricardo tenía "
        "motivos legítimos para pedir especificaciones a Ingeniería —armar "
        "pliegos, cotizar con proveedores— pero no acceso directo a la carpeta "
        "confidencial del proyecto. Se lo resolvió Marcela sin saberlo: semanas "
        "atrás, apurada por cerrar un pliego, le había compartido su usuario y "
        "contraseña «por esa única vez» para que él mismo bajara un archivo, y "
        "nunca cambió la clave después.\n\n"
        "El sábado a la tarde le pidió un favor a Diego, el técnico de sistemas "
        "de guardia: que desactivara un rato el sistema de alerta de "
        "dispositivos externos porque iba a «probar un pendrive nuevo del área "
        "de inventario» y los falsos positivos lo tenían al horno. Diego, sin "
        "ver nada raro en el pedido de un jefe de área con el que se llevaba "
        "bien, lo desactivó de 22:00 a 01:00. Ricardo entró por la puerta de "
        "servicio del depósito —a la que tiene acceso habitual por su función— "
        "a las 22:40, se sentó en una terminal de Ingeniería con el usuario de "
        "Marcela, copió la carpeta completa de especificaciones a un pendrive "
        "que no era de los seriados de la planta, y se fue antes de la una. "
        "Diego lo cruzó de lejos al volver de una ronda por la sala de "
        "servidores, con el uniforme gris de Compras y Logística puesto — "
        "pensó que estaba haciendo un inventario nocturno y no le dio más "
        "vueltas.\n\n"
        "Lo entregó un detalle de guardapolvo: desde hace dos años, todos los "
        "dispositivos externos autorizados en la planta llevan una etiqueta "
        "serializada — un procedimiento que, como jefe de Compras, Ricardo "
        "conocía mejor que nadie porque era él quien lo auditaba. Y sin embargo "
        "usó un pendrive sin etiquetar. La urgencia de pagar la deuda antes del "
        "lunes le ganó al único control que él mismo debería haber hecho "
        "cumplir.\n\n"
        "Un plan bien armado — quebrado por su propia rutina de auditor."
    ),
    max_preguntas=15,
    sospechosos=[
        Sospechoso(
            id="marcela",
            nombre="Marcela Suárez",
            cargo="ingeniera a cargo del diseño del Centinela-3D",
            color="bright_cyan",
            personalidad=(
                "Brillante, perfeccionista, algo insegura fuera de lo técnico. El "
                "proyecto es su bebé desde hace tres años y lo defiende como tal. Se "
                "pone tensa y correctora si siente que dudan de su criterio "
                "profesional; se ablanda y confiesa con culpa genuina cuando el tema "
                "es un error propio, no técnico."
            ),
            coartada=(
                "Dice que pasó todo el fin de semana en su casa, en San Carlos de "
                "Bariloche, terminando la presentación para la demo, y que no volvió "
                "a pisar la planta desde el viernes a la tarde."
            ),
            actitud=(
                "Al principio se pone a la defensiva profesional («este proyecto lo "
                "controlo yo, no me vengan con que se filtró algo por mi culpa»). Si "
                "le preguntan puntual por su usuario, su contraseña, o cómo pudo "
                "alguien acceder a la carpeta con sus credenciales sin que ella "
                "estuviera, se pone visiblemente incómoda y termina confesando."
            ),
            secretos=[
                Secreto(
                    id="contrasena_compartida",
                    pista=(
                        "El acceso del sábado a la noche se hizo con el usuario y la "
                        "contraseña de Marcela — pero ella nunca la cambió después de "
                        "compartirla hace unas semanas."
                    ),
                    instruccion_actor=(
                        "Al principio negás que alguien pueda haber usado tu clave "
                        "(«¿cómo van a haber entrado con mi usuario? Yo estuve en "
                        "casa todo el finde, no sé nada»). Solo si te preguntan "
                        "directamente por tu contraseña, tu usuario, o cómo pudo "
                        "alguien acceder con tus credenciales sin que estuvieras: "
                        "confesás, con mucha vergüenza porque va contra el "
                        "reglamento de seguridad informática, que hace unas semanas "
                        "—apurada por cerrar un pliego de un proveedor— le "
                        "compartiste tu usuario y contraseña a Ricardo Bianchi «por "
                        "esa única vez», para que él mismo bajara un archivo, y que "
                        "nunca cambiaste la clave después."
                    ),
                    criterio_revelacion=(
                        "Admite que compartió su usuario o contraseña con Ricardo "
                        "(u otra persona) en algún momento y que nunca la cambió."
                    ),
                ),
                Secreto(
                    id="sospechas_ricardo",
                    pista=(
                        "En las últimas semanas, Marcela notó a Ricardo Bianchi "
                        "insistente con preguntas sobre quién podía acceder a la "
                        "carpeta del Centinela-3D, y escuchó rumores de que andaba "
                        "mal de plata."
                    ),
                    instruccion_actor=(
                        "Si te preguntan si notaste algo raro en algún compañero, o "
                        "específicamente por Ricardo: contás, dudando si vale la "
                        "pena mencionarlo, que en las últimas semanas Ricardo te "
                        "hizo un par de preguntas que en su momento te parecieron "
                        "normales —quién tenía acceso a la carpeta del proyecto, si "
                        "había forma de bajar los archivos sin loguearse como "
                        "Ingeniería— y que también escuchaste un comentario de "
                        "pasillo de que andaba mal de plata, algo de carreras o "
                        "apuestas. En su momento no le diste importancia."
                    ),
                    criterio_revelacion=(
                        "Menciona que Ricardo preguntó sobre accesos a la carpeta "
                        "del proyecto, o que tenía problemas de dinero o de juego."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="diego",
            nombre="Diego Correa",
            cargo="técnico de sistemas, de guardia el fin de semana",
            color="bright_green",
            personalidad=(
                "Dicharachero, informal, un poco perezoso pero no mala persona. "
                "Confía en la palabra de los jefes de área y no cuestiona pedidos "
                "que le parecen razonables. Trata de minimizar todo con chistes; "
                "tartamudea y se pone serio de golpe cuando lo acorralan."
            ),
            coartada=(
                "Dice que estuvo toda la noche haciendo la ronda de mantenimiento de "
                "sistemas y monitoreo, sin ninguna novedad."
            ),
            actitud=(
                "Al principio minimiza («todo tranqui, no pasó nada raro en mi "
                "guardia»). Si le muestran una contradicción en los registros —por "
                "ejemplo que el sistema de alerta estuvo apagado— o le preguntan "
                "directo por eso, se quiebra rápido y confiesa, con miedo a perder "
                "el trabajo."
            ),
            secretos=[
                Secreto(
                    id="alerta_desactivada",
                    pista=(
                        "El sistema de alerta de dispositivos externos estuvo "
                        "apagado de 22:00 a 01:00 esa noche por pedido de Ricardo "
                        "Bianchi, que dijo que iba a «probar un pendrive nuevo de "
                        "inventario»."
                    ),
                    instruccion_actor=(
                        "Al principio decís que no tocaste ningún sistema de "
                        "seguridad esa noche. Si te muestran el registro de que la "
                        "alerta de dispositivos externos estuvo apagada, o te "
                        "preguntan directamente por eso: confesás, nervioso, que "
                        "Ricardo Bianchi te pidió el favor esa tarde, que dijo que "
                        "iba a probar un pendrive nuevo del área de inventario y "
                        "que los falsos positivos lo tenían al horno, y que vos, "
                        "como no viste nada raro en el pedido de un jefe de área, "
                        "la desactivaste de 22 a 1 y después la reactivaste vos "
                        "mismo sin avisar a nadie porque no querías quedar pegado a "
                        "un quilombo."
                    ),
                    criterio_revelacion=(
                        "Admite haber desactivado el sistema de alerta de "
                        "dispositivos externos esa noche, y que fue a pedido de "
                        "Ricardo Bianchi."
                    ),
                ),
                Secreto(
                    id="vio_uniforme_compras",
                    pista=(
                        "Cerca de las 22:40, Diego vio de lejos a alguien entrando "
                        "por la puerta de servicio del depósito con el uniforme "
                        "gris de Compras y Logística, y asumió que era un "
                        "inventario nocturno de rutina."
                    ),
                    instruccion_actor=(
                        "Solo si te preguntan si viste a alguien esa noche, o qué "
                        "viste en tu ronda: contás que cerca de las 22:40, volviendo "
                        "de la sala de servidores, viste de lejos a alguien entrar "
                        "por la puerta de servicio del depósito con el uniforme "
                        "gris de Compras y Logística puesto. No le viste la cara, "
                        "pensaste que era un inventario nocturno de rutina y "
                        "seguiste con lo tuyo."
                    ),
                    criterio_revelacion=(
                        "Menciona haber visto a alguien con el uniforme o ropa de "
                        "Compras y Logística entrando por la puerta de depósito esa "
                        "noche."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="ricardo",
            nombre="Ricardo Bianchi",
            cargo="jefe de Compras y Vinculación con Contratistas",
            color="bright_red",
            es_culpable=True,
            personalidad=(
                "Cordial, sociable, buen vendedor de sí mismo — el tipo de tipo que "
                "se acuerda del cumpleaños de todos. Maneja gente mejor que "
                "planillas. Cuando lo acorralan pierde la sonrisa comercial y se "
                "pone frío y calculador, desviando la conversación con la habilidad "
                "de quien negocia contratos para vivir."
            ),
            coartada=(
                "Dice que se fue el viernes a la tarde y pasó todo el fin de semana "
                "en Bariloche con la familia, sin pisar la planta ni una vez."
            ),
            actitud=(
                "Nunca pierde la calma de entrada. Si lo confrontan con evidencia "
                "concreta, primero la minimiza o la explica con excusas técnicas "
                "(«esos lectores de tarjeta fallan seguido»), y si eso no alcanza, "
                "desvía la sospecha hacia otros («la clave era de Marcela, ¿no? "
                "Yo qué sé qué hizo con ella»). Jamás confiesa espontáneamente, pero "
                "cede terreno, dato por dato, cuando lo aprietan con algo puntual."
            ),
            secretos=[
                Secreto(
                    id="acceso_deposito",
                    pista=(
                        "El registro de acceso físico muestra la tarjeta de Ricardo "
                        "Bianchi entrando por la puerta de servicio del depósito a "
                        "las 22:40 del sábado — la misma noche que dice haber "
                        "estado en su casa."
                    ),
                    instruccion_actor=(
                        "Si te preguntan directamente por tu tarjeta de acceso o el "
                        "registro de esa noche, o te marcan que hay una entrada "
                        "tuya al depósito: primero intentás minimizar («habrá un "
                        "error en el sistema, esos lectores fallan seguido»). Si "
                        "insisten con el dato concreto, admitís —incómodo— que sí, "
                        "pasaste por la planta el sábado a la noche, pero decís que "
                        "fue solo un momento para buscar unos papeles del área de "
                        "Compras que te habías olvidado, y que no tiene nada que "
                        "ver con lo del radar."
                    ),
                    criterio_revelacion=(
                        "Admite que estuvo físicamente en la planta (por la puerta "
                        "de depósito) el sábado a la noche, aunque sea minimizando "
                        "el motivo."
                    ),
                ),
                Secreto(
                    id="deudas_juego",
                    pista=(
                        "Ricardo Bianchi tiene deudas de juego importantes —"
                        "carreras, apuestas online, algún casino— que viene "
                        "arrastrando desde hace meses."
                    ),
                    instruccion_actor=(
                        "Nunca lo contás espontáneamente. Solo si te preguntan "
                        "directo por tus finanzas, por deudas, o si te mencionan "
                        "rumores de que jugás o apostás: admitís, incómodo pero "
                        "minimizando, que sí, tenés algunas deudas de juego —"
                        "carreras, alguna apuesta online— pero insistís en que "
                        "«no es nada que no pueda manejar» y que no tiene relación "
                        "con la planta."
                    ),
                    criterio_revelacion=(
                        "Admite tener deudas de juego (apuestas, carreras, casino) "
                        "o problemas financieros serios."
                    ),
                ),
                Secreto(
                    id="pedido_a_diego",
                    pista=(
                        "Ricardo le pidió a Diego, el fin de semana, que "
                        "desactivara el sistema de alerta de dispositivos externos "
                        "con la excusa de «probar un pendrive nuevo de inventario»."
                    ),
                    instruccion_actor=(
                        "Solo si te confrontan con que el sistema de alerta estuvo "
                        "apagado esa noche, o con que Diego ya contó que se lo "
                        "pediste vos: al principio lo negás o decís que no te "
                        "acordás bien. Si insisten con el dato concreto (que Diego "
                        "ya lo admitió, o que el registro lo muestra), reconocés, "
                        "ya sin poder desviar más, que sí le pediste el favor a "
                        "Diego con la excusa de un pendrive de inventario, pero "
                        "seguís sosteniendo que no fue para nada relacionado con el "
                        "robo de los planos."
                    ),
                    criterio_revelacion=(
                        "Admite haberle pedido a Diego que desactivara el sistema "
                        "de alerta de dispositivos externos esa noche."
                    ),
                ),
            ],
        ),
    ],
)
