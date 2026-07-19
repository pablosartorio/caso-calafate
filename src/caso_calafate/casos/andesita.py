"""EL CASO ANDESITA — un informe de control de calidad alterado en la Planta Andesita.

⚠️ SPOILER: leer los datos de este archivo revela al culpable.
Jugá una partida antes. :)
"""

from caso_calafate.caso import Caso, Secreto, Sospechoso

CASO_ANDESITA = Caso(
    id="andesita",
    titulo="EL CASO ANDESITA",
    gancho=(
        "Un lote de elementos combustibles salió aprobado del laboratorio — "
        "pero los datos crudos cuentan otra historia."
    ),
    # Los párrafos van en una sola línea lógica (concatenación implícita de
    # strings): rich los envuelve al ancho de la terminal. Los saltos duros
    # quedan solo donde son intencionales (la lista de viñetas).
    briefing=(
        "Bariloche, 07:15 de la mañana. Te suena el teléfono en medio del desayuno.\n\n"
        "«Detective, necesitamos que venga a la Planta Andesita. Es un tema... "
        "delicado.»\n\n"
        "En la Planta Andesita se fabrican y ensayan elementos combustibles "
        "nucleares. Hace una semana, el Lote EC-114 —treinta y dos elementos "
        "combustibles destinados a la Central Huemul— salió del laboratorio de "
        "ensayos con el sello de «aprobado, sin observaciones». Ayer, durante "
        "una auditoría de rutina previa al despacho, alguien pidió el archivo "
        "crudo del ensayo de hermeticidad y radiografiado de soldaduras... y no "
        "coincidía con el informe firmado.\n\n"
        "Lo que se sabe hasta ahora:\n\n"
        " • El ensayo se corrió el jueves de la semana pasada, turno noche, y\n"
        "   terminó cerca de la 01:00.\n"
        " • El registro crudo del equipo radiográfico marca tres elementos como\n"
        "   «rechazado — posible falta de fusión en la soldadura de cierre»,\n"
        "   con el timestamp de esa madrugada.\n"
        " • El informe final, cargado al sistema (LIMS) el viernes a la mañana,\n"
        "   dice que los treinta y dos elementos «cumplen norma, sin\n"
        "   observaciones» — y lleva la firma de aprobación del laboratorio.\n"
        " • Solo tres personas tenían permisos de escritura en el LIMS esa\n"
        "   semana. Son tus sospechosos.\n\n"
        "Interrogá, anotá, y cuando estés seguro: acusá. Tenés una sola oportunidad."
    ),
    contexto_actores="""\
La semana pasada se ensayó el Lote EC-114 (32 elementos combustibles para la
Central Huemul) en el laboratorio de ensayos de la Planta Andesita. El ensayo
de hermeticidad y radiografiado de las soldaduras de cierre se corrió el
jueves, turno noche, y terminó cerca de la 01:00. El registro crudo del
equipo marca tres elementos como rechazados por posible falta de fusión en la
soldadura. El viernes a la mañana se cargó al sistema de gestión de ensayos
(LIMS) el informe final, que aprueba los 32 elementos sin observaciones y
lleva la firma del laboratorio. La discrepancia se descubrió ayer, durante
una auditoría previa al despacho del lote. Solo tres personas tenían permisos
de escritura en el LIMS esa semana; un detective está interrogando a las
tres.""",
    epilogo=(
        "Hernán Bracamonte, jefe del Laboratorio de Ensayos, alteró el informe "
        "del Lote EC-114.\n\n"
        "Hacía tres meses que la Central Huemul amenazaba con aplicar la multa "
        "por atraso —una cláusula que le podía costar el presupuesto del área "
        "entero— si el lote no salía esa semana. Cuando el jueves a la noche el "
        "radiografiado marcó tres elementos con posible falta de fusión en la "
        "soldadura de cierre, Hernán supo lo que significaba: un reensayo "
        "completo, con elementos de reemplazo fabricados de cero, implicaba "
        "como mínimo seis semanas más. No tenía ese tiempo.\n\n"
        "El viernes a primera hora, antes de que Control de Calidad final "
        "revisara el paquete de ensayos, entró solo al laboratorio, abrió el "
        "archivo crudo del radiografiado con su propio usuario del LIMS, "
        "reemplazó los tres registros «rechazado» por valores dentro de norma "
        "y firmó el informe consolidado él mismo, saltándose la doble firma "
        "que exige el procedimiento «por practicidad, para no atrasar más el "
        "trámite». Se dijo a sí mismo que más adelante iba a pedir un reensayo "
        "silencioso de esos tres elementos, con calma, sin que nadie lo "
        "notara — un reensayo que nunca llegó a pedir.\n\n"
        "Lo delató algo que no controlaba: el equipo radiográfico graba cada "
        "lectura con un sello de integridad que no se puede editar sin dejar "
        "rastro, y guarda automáticamente una copia espejo en un servidor que "
        "administra Sistemas —al que Hernán ni sabía que tenía acceso otra "
        "área—. La auditoría de rutina comparó esa copia espejo con el informe "
        "firmado y las fechas y los valores no coincidían.\n\n"
        "Facundo, el técnico que corrió el ensayo, se había ido a la 01:15 "
        "convencido de que su trabajo terminaba con avisarle al jefe por "
        "teléfono: nunca imaginó que alguien iba a tocar sus números después. "
        "Y Rocío, que semanas atrás había pedido el traslado a otra planta, "
        "cansada de la presión de cronograma de Hernán, terminó siendo, sin "
        "quererlo, la que destapó todo: fue ella quien pidió la copia espejo "
        "para la auditoría — la misma semana en que le había llamado la "
        "atención lo insistente que él se ponía con que el informe «ya estaba "
        "cerrado»."
    ),
    max_preguntas=15,
    sospechosos=[
        Sospechoso(
            id="rocio",
            nombre="Rocío Painemal",
            cargo="analista de Aseguramiento de Calidad",
            color="bright_cyan",
            personalidad=(
                "Meticulosa, directa, algo cansada del clima laboral del último "
                "año. Responde con precisión casi notarial, como si supiera que "
                "todo lo que diga puede terminar en un informe. No se le tiembla "
                "la voz, pero tampoco regala nada de más."
            ),
            coartada=(
                "Dice que el fin de semana en que se cargó el informe final "
                "estuvo de franco en Piedra del Águila, con su familia, y que no "
                "tocó el sistema hasta el lunes."
            ),
            actitud=(
                "Responde con calma y prolijidad, casi dictando un acta. Si la "
                "contradicen con un dato concreto —un registro, un horario— no "
                "se pone nerviosa, pero corrige el relato con precisión, y ahí "
                "aparece lo que se había guardado."
            ),
            secretos=[
                Secreto(
                    id="visita_viernes",
                    pista=(
                        "Rocío no estuvo todo el fin de semana en Piedra del "
                        "Águila: pasó por la planta el viernes a la mañana, un "
                        "rato, antes de irse de franco."
                    ),
                    instruccion_actor=(
                        "Solo si te preguntan puntualmente si estuviste en la "
                        "planta el viernes, o te muestran algún registro de esa "
                        "mañana: aclarás, sin darle mayor importancia, que "
                        "pasaste un rato por tu oficina el viernes temprano "
                        "para dejar armada una carpeta antes de irte de franco, "
                        "pero que no entraste al LIMS ni tocaste ningún informe "
                        "de ensayos."
                    ),
                    criterio_revelacion=(
                        "Admite que estuvo en la planta el viernes a la mañana "
                        "(aunque sea brevemente), contradiciendo la versión de "
                        "que pasó todo el fin de semana afuera."
                    ),
                ),
                Secreto(
                    id="pedido_traslado",
                    pista=(
                        "Rocío había pedido, semanas atrás, el traslado a otra "
                        "planta del grupo: la relación con Hernán, su jefe "
                        "directo, venía tensa por las presiones de cronograma."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por tu relación con Hernán o por si "
                        "pensaste en irte del área: contás, sin vueltas, que "
                        "pediste el traslado hace unas semanas porque la "
                        "presión constante de plazos te tenía harta, y que la "
                        "relación con Hernán venía tensa. Aclarás que eso no "
                        "tiene nada que ver con lo que encontraste en la "
                        "auditoría."
                    ),
                    criterio_revelacion=(
                        "Cuenta que pidió un traslado a otra planta o que su "
                        "relación laboral con Hernán estaba tensa por las "
                        "presiones de cronograma."
                    ),
                ),
                Secreto(
                    id="hernan_nervioso",
                    pista=(
                        "Días antes de la auditoría, Rocío notó a Hernán "
                        "insistiendo, más de lo normal, en que el paquete de "
                        "ensayos del Lote EC-114 «ya estaba cerrado y no hacía "
                        "falta revisarlo de nuevo»."
                    ),
                    instruccion_actor=(
                        "Si te preguntan si notaste algo raro en el "
                        "comportamiento de Hernán esa semana: contás que sí, "
                        "que insistió varias veces en que el informe del Lote "
                        "EC-114 «estaba cerrado» y que no hacía falta que nadie "
                        "lo revisara de nuevo, algo que en ese momento te "
                        "pareció apuro nomás, pero que en retrospectiva te hizo "
                        "ruido."
                    ),
                    criterio_revelacion=(
                        "Cuenta que notó a Hernán insistiendo en que no había "
                        "que revisar de nuevo el informe del Lote EC-114, o que "
                        "actuó con apuro o nerviosismo inusual esa semana."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="facundo",
            nombre="Facundo Yulán",
            cargo="técnico de ensayos no destructivos (turno noche)",
            color="bright_yellow",
            personalidad=(
                "Joven, cumplidor, un poco inseguro de su lugar en la planta. "
                "Habla con respeto casi excesivo hacia sus superiores. Se pone "
                "nervioso si siente que algo puede volverse en su contra, "
                "aunque no tenga nada que ver."
            ),
            coartada=(
                "Dice que corrió el ensayo del Lote EC-114 el jueves a la "
                "noche, cargó los datos crudos al sistema como corresponde, y "
                "se retiró del laboratorio a las 00:30 sin volver a tocar nada."
            ),
            actitud=(
                "Colaborador por naturaleza, pero se guarda cosas por miedo a "
                "quedar pegado o a perjudicar a alguien. Si notan que se "
                "contradice o dudás en su relato, con algo de presión suelta lo "
                "que vio o hizo."
            ),
            secretos=[
                Secreto(
                    id="observacion_verbal",
                    pista=(
                        "Facundo avisó verbalmente a Hernán, esa misma noche "
                        "por teléfono, que el radiografiado había marcado tres "
                        "elementos como rechazados — antes de irse del "
                        "laboratorio."
                    ),
                    instruccion_actor=(
                        "Si te preguntan qué hiciste apenas viste la lectura "
                        "anómala, o si avisaste a alguien esa noche: contás que "
                        "llamaste a Hernán, tu jefe, para avisarle del "
                        "resultado antes de irte, porque el procedimiento dice "
                        "que las observaciones críticas hay que reportarlas de "
                        "inmediato. Él te dijo que «lo iba a revisar él mismo a "
                        "la mañana» y que vos podías cerrar turno tranquilo."
                    ),
                    criterio_revelacion=(
                        "Cuenta que llamó o avisó a Hernán (el jefe) por "
                        "teléfono esa misma noche sobre los elementos "
                        "rechazados, antes de retirarse."
                    ),
                ),
                Secreto(
                    id="no_volvio_a_ver_datos",
                    pista=(
                        "Facundo nunca volvió a abrir el archivo del ensayo "
                        "después de cargarlo esa noche: se enteró de que el "
                        "informe decía «aprobado» recién cuando se lo mostró el "
                        "auditor, días después."
                    ),
                    instruccion_actor=(
                        "Si notan que estás nervioso o te preguntan si sabías "
                        "que el informe final decía otra cosa: admitís, "
                        "genuinamente sorprendido y un poco dolido, que vos "
                        "cargaste los datos crudos tal cual salieron del "
                        "equipo, que no volviste a tocar el archivo, y que te "
                        "enteraste de que el informe decía «aprobado sin "
                        "observaciones» recién cuando el auditor te lo mostró — "
                        "y que no entendés cómo pasó."
                    ),
                    criterio_revelacion=(
                        "Afirma que él cargó los datos originales sin "
                        "modificarlos y que se enteró del cambio en el informe "
                        "final recién después, por el auditor."
                    ),
                ),
                Secreto(
                    id="salida_tardia",
                    pista=(
                        "El registro de accesos marca que Facundo salió del "
                        "laboratorio a la 01:15, no a las 00:30 como dijo "
                        "primero."
                    ),
                    instruccion_actor=(
                        "Al principio decís que te fuiste a las 00:30. Si te "
                        "muestran el registro de accesos o te marcan la "
                        "diferencia de horario: admitís, un poco avergonzado, "
                        "que te quedaste hasta la 01:15 repasando la "
                        "calibración del equipo dos veces porque te habían "
                        "llamado la atención antes por un error de carga de "
                        "datos, y no querías que pasara de nuevo. No le "
                        "dijiste la hora exacta a nadie porque no querías "
                        "parecer inseguro."
                    ),
                    criterio_revelacion=(
                        "Admite que en realidad se retiró más tarde de lo que "
                        "dijo primero (cerca de la 01:15), por haber repasado "
                        "la calibración del equipo."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="hernan",
            nombre="Hernán Bracamonte",
            cargo="jefe del Laboratorio de Ensayos",
            color="bright_magenta",
            es_culpable=True,
            personalidad=(
                "Gerencial, calculador, de los que dicen que «los números no "
                "mienten» pero maneja los números a su favor. Vocabulario "
                "técnico y de gestión, cita cronogramas y cláusulas "
                "contractuales como si fueran escritura sagrada. Bajo presión "
                "se pone paternalista y trata de explicarte «cómo funciona "
                "realmente» la industria."
            ),
            coartada=(
                "Dice que el jueves se fue del laboratorio a las 20:00, se "
                "llevó una carpeta de informes a su casa, y no volvió a entrar "
                "al sistema hasta el lunes siguiente."
            ),
            actitud=(
                "Si lo presionan con generalidades, se pone didáctico y desvía "
                "hacia la presión comercial del cliente. Pero si le muestran el "
                "registro de accesos al LIMS o le preguntan puntualmente por la "
                "noche del jueves a viernes, se pone rígido, mide cada "
                "palabra, y termina quebrándose si insisten con la copia "
                "espejo del ensayo."
            ),
            secretos=[
                Secreto(
                    id="login_viernes_temprano",
                    pista=(
                        "El usuario de Hernán Bracamonte quedó registrado en el "
                        "LIMS el viernes a las 06:40 de la mañana, antes de que "
                        "llegara nadie más al laboratorio — y antes de la hora "
                        "en que dice haber vuelto a tocar el sistema."
                    ),
                    instruccion_actor=(
                        "Solo si te preguntan directamente por tu ingreso al "
                        "LIMS el viernes a la mañana o por el registro de "
                        "accesos de esa semana: admitís, incómodo, que entraste "
                        "solo al laboratorio el viernes bien temprano, antes de "
                        "que llegara nadie, «para adelantar papeleo». Negás "
                        "cualquier otra cosa mientras puedas."
                    ),
                    criterio_revelacion=(
                        "Admite que ingresó al LIMS o al laboratorio el "
                        "viernes muy temprano en la mañana, antes de que "
                        "llegara el resto del personal."
                    ),
                ),
                Secreto(
                    id="presion_cliente",
                    pista=(
                        "La Central Huemul venía amenazando con aplicar la "
                        "cláusula de multa por atraso si el Lote EC-114 no "
                        "salía esa semana; Hernán manejaba directamente esa "
                        "correspondencia."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por plazos, por el cliente o por la "
                        "presión de cronograma: contás, con algo de "
                        "indignación defensiva, que la Central Huemul "
                        "amenazaba con una multa contractual muy fuerte si el "
                        "lote se atrasaba, que vos eras quien recibía esos "
                        "mails, y que «nadie entiende la presión que es "
                        "sostener un cronograma así»."
                    ),
                    criterio_revelacion=(
                        "Menciona la amenaza de multa o penalidad del cliente "
                        "(Central Huemul) por atraso en la entrega del lote, y "
                        "que él manejaba esa presión directamente."
                    ),
                ),
                Secreto(
                    id="reensayo_evitado",
                    pista=(
                        "Un reensayo completo de los elementos observados "
                        "hubiera demorado, según los propios cálculos de "
                        "Hernán, al menos seis semanas — tiempo que el "
                        "cronograma no tenía."
                    ),
                    instruccion_actor=(
                        "Solo si te acusan directamente de haber alterado el "
                        "informe, o te preguntan por qué no se hizo un "
                        "reensayo cuando el radiografiado marcó una "
                        "observación: te quebrás. Confesás que sabías que un "
                        "reensayo completo tomaba mínimo seis semanas, que no "
                        "tenías ese margen, y que pensabas «arreglarlo "
                        "después» con un reensayo silencioso que nunca "
                        "llegaste a hacer."
                    ),
                    criterio_revelacion=(
                        "Confiesa haber alterado o reemplazado los resultados "
                        "del informe para evitar un reensayo que iba a demorar "
                        "semanas, con la intención de corregirlo después."
                    ),
                ),
            ],
        ),
    ],
)
