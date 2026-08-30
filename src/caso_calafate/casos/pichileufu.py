"""EL CASO PICHILEUFÚ — homenaje a Rodolfo Walsh (Variaciones en rojo /
Operación Masacre).

El registro técnico dice "avería". Alguien murió. El tono acá es de denuncia
periodística, no de enigma: la pregunta no es solo quién encubrió, sino cómo
una institución entera se acomoda para que la verdad no le cueste nada a
quien manda.

⚠️ SPOILER: leer los datos de este archivo revela al culpable.
Jugá una partida antes. :)
"""

from caso_calafate.caso import Caso, Secreto, Sospechoso

CASO_PICHILEUFU = Caso(
    id="pichileufu",
    titulo="EL CASO PICHILEUFÚ",
    sede="Central Nuclear Pichileufú",
    ciudad="Bariloche",
    delito="el encubrimiento del accidente nuclear",
    culpable_alias="encubridor",
    gancho=(
        "El parte oficial dice 'avería técnica sin heridos'. Un operario está "
        "muerto, y el informe interno que lo prueba desapareció."
    ),
    briefing=(
        "Central Nuclear Pichileufú. Te llaman a las 23:00, fuera de horario: "
        "algo no cierra en un parte que ya se había cerrado.\n\n"
        "«Detective, el parte oficial dice 'avería técnica, sin heridos'. Pero "
        "un operario murió esa noche, y el informe interno que lo documenta "
        "no aparece en ningún lado.»\n\n"
        "Hace una semana, durante un mantenimiento de rutina, un operario "
        "murió por exposición a una falla que el parte oficial nunca "
        "mencionó. El informe técnico interno, que sí registraba lo ocurrido, "
        "fue retirado del sistema esa misma noche.\n\n"
        "Lo que se sabe hasta ahora:\n\n"
        " • El parte oficial se redactó y se firmó antes de que terminara el\n"
        "   turno, algo inusual para un incidente de esa gravedad.\n"
        " • El informe interno existió: dos personas lo vieron antes de que\n"
        "   desapareciera del sistema.\n"
        " • La familia del operario recibió una indemnización rápida, con la\n"
        "   condición de no hacer declaraciones.\n"
        " • Cinco personas tuvieron acceso al informe antes de que se\n"
        "   borrara. Son tus sospechosos.\n\n"
        "Interrogá, anotá, y cuando estés seguro: acusá. Tenés una sola oportunidad."
    ),
    contexto_actores="""\
Hace una semana, durante un mantenimiento de rutina en la Central Nuclear
Pichileufú (Bariloche), un operario murió por exposición a una falla que el
parte oficial nunca mencionó ("avería técnica, sin heridos"). El informe
técnico interno que sí registraba lo ocurrido fue retirado del sistema esa
misma noche. La familia del operario recibió una indemnización rápida a
cambio de no declarar. Un detective interroga a las cinco personas que
tuvieron acceso al informe antes de que desapareciera.""",
    epilogo=(
        "El interventor Palavecino ordenó borrar el informe.\n\n"
        "Enviado desde Buenos Aires meses atrás para 'poner en orden' la "
        "Central antes de una auditoría internacional, sabía que un "
        "accidente con muerte documentado hundía cualquier posibilidad de "
        "renovar el financiamiento externo del que dependía su propia "
        "gestión. La noche del accidente, presionó al gerente Aldo Brizuela "
        "para que redactara y firmara un parte oficial minimizado antes de "
        "que terminara el turno, y él mismo ordenó, por teléfono, que el "
        "informe técnico interno se retirara del sistema 'para revisión', sin "
        "que nadie volviera a verlo. Gestionó también la indemnización "
        "rápida a la familia, presentándola como generosidad institucional.\n\n"
        "La Dra. Renata Ostrowski, que redactó el informe técnico original, "
        "guardó una copia en un disco personal — no por valentía, al "
        "principio, sino por simple costumbre de archivo. Tardó una semana en "
        "decidir si esa copia era algo que le correspondía mostrar, o algo "
        "que era más seguro callar."
    ),
    max_preguntas=15,
    sospechosos=[
        Sospechoso(
            id="brizuela",
            nombre="Aldo Brizuela",
            cargo="gerente de la Central",
            color="yellow",
            personalidad=(
                "Cansado, atrapado entre la lealtad institucional y una culpa "
                "que no sabe bien dónde poner. Elige mucho las palabras."
            ),
            coartada=(
                "Dice que redactó el parte oficial esa misma noche, 'con la "
                "información que tenía en ese momento', y que después no supo "
                "más del informe interno."
            ),
            actitud=(
                "Defensivo con matices legales al principio. Si le muestran que "
                "entienden la presión que tuvo, se ablanda y admite más de lo "
                "que planeaba."
            ),
            secretos=[
                Secreto(
                    id="parte_apurado",
                    pista=(
                        "Aldo firmó el parte oficial minimizado antes de que "
                        "terminara el turno, algo inusual para un incidente de "
                        "esa gravedad."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por qué el parte se firmó tan rápido: "
                        "admitís, incómodo, que fue inusualmente apurado para un "
                        "incidente así, pero decís que 'órdenes de arriba' te "
                        "apuraron."
                    ),
                    criterio_revelacion=(
                        "Admite que el parte oficial se firmó de forma inusualmente "
                        "apurada, por presión de instancias superiores."
                    ),
                ),
                Secreto(
                    id="presion_palavecino",
                    pista=(
                        "El interventor Palavecino presionó personalmente a Aldo "
                        "para que firmara el parte minimizado esa misma noche."
                    ),
                    instruccion_actor=(
                        "Solo si ya admitiste que te apuraron Y te preguntan "
                        "quién exactamente: nombrás, con evidente alivio de "
                        "sacárselo de encima, al interventor Palavecino."
                    ),
                    criterio_revelacion=(
                        "Nombra al interventor Palavecino como quien lo presionó "
                        "para firmar el parte."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="renata",
            nombre="Dra. Renata Ostrowski",
            cargo="física, autora del informe técnico interno",
            color="cyan",
            personalidad=(
                "Metódica, guardó silencio por miedo pero nunca dejó de pensar "
                "en el operario muerto. Responde con precisión técnica cuando "
                "puede evitar mirar el costado humano."
            ),
            coartada=(
                "Dice que redactó el informe técnico esa misma noche, con todos "
                "los detalles del accidente, y que lo subió al sistema como "
                "corresponde."
            ),
            actitud=(
                "Cauta, calcula cada respuesta. Si sienten que confían en ella "
                "y no la presionan de más, termina soltando lo que más le pesa."
            ),
            secretos=[
                Secreto(
                    id="copia_personal",
                    pista=(
                        "Renata guardó una copia personal del informe técnico "
                        "antes de que se borrara del sistema institucional."
                    ),
                    instruccion_actor=(
                        "Solo si te ganás su confianza (varias preguntas "
                        "amables, sin presionar) y te preguntan si guardó algo "
                        "del informe: admite, en voz baja, que tiene una copia "
                        "personal en un disco propio."
                    ),
                    criterio_revelacion=(
                        "Admite tener una copia personal del informe técnico "
                        "original."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="numa",
            nombre="Numa Lezcano",
            cargo="delegado gremial",
            color="red",
            personalidad=(
                "Firme, acostumbrado a pelear cada reclamo laboral. Desconfía "
                "profundamente de cualquier explicación oficial."
            ),
            coartada=(
                "Dice que se enteró del accidente recién al día siguiente, como "
                "todo el personal, por el parte oficial minimizado."
            ),
            actitud=(
                "Directo y combativo. Si sienten que están de su lado buscando "
                "la verdad, coopera sin vueltas."
            ),
            secretos=[
                Secreto(
                    id="indemnizacion_condicionada",
                    pista=(
                        "La familia del operario recibió una indemnización "
                        "rápida a cambio de firmar que no harían declaraciones "
                        "públicas."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por la familia del operario o por una "
                        "indemnización: contás, indignado, que recibieron plata "
                        "rápido a cambio de firmar que no iban a declarar "
                        "públicamente."
                    ),
                    criterio_revelacion=(
                        "Cuenta que la familia del operario recibió una "
                        "indemnización condicionada a no hacer declaraciones."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="ceferino",
            nombre="Ceferino Aguer",
            cargo="periodista freelance",
            color="green",
            personalidad=(
                "Insistente, acostumbrado a que le cierren puertas y a "
                "conseguir igual lo que busca. Anota todo en una libreta propia."
            ),
            coartada=(
                "Dice que esa noche estaba afuera de la Central, esperando "
                "alguna declaración oficial que nunca llegó."
            ),
            actitud=(
                "Coopera con gusto si sienten que comparten el mismo objetivo: "
                "que la verdad salga a la luz."
            ),
            secretos=[
                Secreto(
                    id="fuente_interna",
                    pista=(
                        "Ceferino tiene una fuente dentro de la Central que le "
                        "confirmó, extraoficialmente, que hubo una muerte."
                    ),
                    instruccion_actor=(
                        "Si te preguntan cómo supiste del accidente antes que "
                        "nadie: contás, protegiendo el nombre, que tenés una "
                        "fuente dentro de la Central que te confirmó "
                        "extraoficialmente que hubo una muerte."
                    ),
                    criterio_revelacion=(
                        "Cuenta que tiene una fuente interna que le confirmó la "
                        "muerte del operario."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="palavecino",
            nombre="Interventor Palavecino",
            cargo="interventor enviado desde Buenos Aires",
            color="magenta",
            es_culpable=True,
            personalidad=(
                "Frío, corporativo, habla en términos de 'gestión' y "
                "'auditoría' incluso cuando se le pregunta por una muerte."
            ),
            coartada=(
                "Dice que esa noche estaba redactando el informe de gestión "
                "para la auditoría internacional, ajeno a los detalles "
                "operativos del incidente."
            ),
            actitud=(
                "Cordial y evasivo con lenguaje corporativo. Si lo confrontan "
                "con algo concreto, se pone frío y empieza a hablar de "
                "'procedimientos', nunca de personas."
            ),
            secretos=[
                Secreto(
                    id="auditoria_en_juego",
                    pista=(
                        "Palavecino necesitaba que la Central pasara una "
                        "auditoría internacional sin incidentes documentados, o "
                        "perdía el financiamiento que sostenía su gestión."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por la auditoría internacional: "
                        "admitís, con lenguaje corporativo, que la Central "
                        "necesitaba pasarla sin incidentes documentados o se "
                        "perdía financiamiento clave."
                    ),
                    criterio_revelacion=(
                        "Admite que la auditoría internacional necesitaba que no "
                        "hubiera incidentes documentados."
                    ),
                ),
                Secreto(
                    id="orden_borrado",
                    pista=(
                        "Palavecino ordenó por teléfono que el informe técnico "
                        "interno se retirara del sistema 'para revisión'."
                    ),
                    instruccion_actor=(
                        "Solo si ya admitiste lo de la auditoría Y te preguntan "
                        "directamente si vos ordenaste retirar el informe: "
                        "admitís, con frialdad corporativa, que ordenaste "
                        "retirarlo 'para revisión', sin admitir que fuera un "
                        "encubrimiento."
                    ),
                    criterio_revelacion=(
                        "Admite haber ordenado retirar el informe técnico del "
                        "sistema."
                    ),
                ),
            ],
        ),
    ],
)
