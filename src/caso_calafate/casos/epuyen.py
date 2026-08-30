"""EL CASO EPUYÉN — homenaje a Guillermo Saccomanno (Cámara Gesell).

Un pueblo turístico patagónico, fuera de temporada, en un silencio que no es
inocente: todos saben algo y nadie lo dice primero, porque decirlo primero
tiene un costo social que nadie quiere pagar.

⚠️ SPOILER: leer los datos de este archivo revela al culpable.
Jugá una partida antes. :)
"""

from caso_calafate.caso import Caso, Secreto, Sospechoso

CASO_EPUYEN = Caso(
    id="epuyen",
    titulo="EL CASO EPUYÉN",
    sede="Centro de Radioterapia Epuyén",
    ciudad="Epuyén",
    delito="el encubrimiento de la negligencia médica",
    culpable_alias="encubridor",
    gancho=(
        "Temporada baja en un pueblo turístico patagónico: una muerte "
        "evitable, y un silencio que el pueblo entero parece haber acordado."
    ),
    briefing=(
        "Epuyén, temporada baja. Te llaman a un pueblo que en esta época del "
        "año casi no tiene turistas ni ruido.\n\n"
        "«Detective, un paciente murió acá hace dos semanas por una dosis mal "
        "calculada. El Centro lo llamó 'complicación imprevista'. Nadie en "
        "el pueblo quiere hablar del tema.»\n\n"
        "Un paciente de radioterapia murió por una dosis mal calculada del "
        "equipo. El informe interno original, que documentaba el error real, "
        "fue reemplazado por uno que hablaba de una 'complicación clínica "
        "imprevista'.\n\n"
        "Lo que se sabe hasta ahora:\n\n"
        " • El error de cálculo quedó registrado en el sistema del equipo\n"
        "   antes de ser corregido en el informe final.\n"
        " • La familia del paciente no hizo reclamos: recibió una atención\n"
        "   médica gratuita de por vida para otro familiar enfermo.\n"
        " • En un pueblo tan chico, casi todos saben algo, pero nadie fue el\n"
        "   primero en decirlo.\n"
        " • Cinco personas del pueblo y del Centro tienen alguna pieza del\n"
        "   silencio. Son tus sospechosos.\n\n"
        "Interrogá, anotá, y cuando estés seguro: acusá. Tenés una sola oportunidad."
    ),
    contexto_actores="""\
Hace dos semanas, un paciente del Centro de Radioterapia Epuyén murió por una
dosis mal calculada del equipo. El informe interno original fue reemplazado
por uno que habla de una "complicación clínica imprevista". La familia del
paciente no reclamó: recibió atención médica gratuita de por vida para otro
familiar enfermo. En un pueblo chico, casi todos saben algo pero nadie lo dijo
primero. Un detective interroga a las cinco personas del pueblo y del Centro
con alguna pieza del silencio.""",
    epilogo=(
        "La Dra. Ainhoa Pallares encubrió su propio error de cálculo.\n\n"
        "Directora del Centro, fue ella misma quien calculó mal la dosis del "
        "equipo esa tarde, distraída por un problema personal que no viene "
        "al caso. Al ver el resultado, en vez de reportar el error tal cual "
        "había ocurrido, redactó un informe alternativo que hablaba de una "
        "'complicación clínica imprevista', invisible a cualquier auditoría "
        "externa. Gestionó personalmente, y con genuina culpa, que la familia "
        "recibiera atención médica gratuita de por vida para un familiar "
        "enfermo — no como soborno calculado, sino como la única reparación "
        "que se sintió capaz de ofrecer sin confesar. El resto del pueblo no "
        "encubrió un crimen: encubrió a una médica que, en un lugar tan "
        "chico, es la única que atiende a la mitad de los vecinos, y nadie "
        "quiso ser quien la dejara sin trabajo.\n\n"
        "Braian Melivilu, familiar del paciente muerto, es el único que "
        "nunca aceptó del todo el silencio — solo que no encontró, en dos "
        "semanas, con quién hablarlo antes de que llegaras vos."
    ),
    max_preguntas=15,
    sospechosos=[
        Sospechoso(
            id="norberto",
            nombre="Norberto Achával",
            cargo="intendente de Epuyén",
            color="cyan",
            personalidad=(
                "Pragmático, preocupado por la imagen del pueblo más que por "
                "cualquier otra cosa. Fuera de temporada, cualquier escándalo "
                "le parece una amenaza existencial."
            ),
            coartada=(
                "Dice que se enteró del error recién por rumores, como todo el "
                "pueblo, y que nunca vio ningún informe oficial."
            ),
            actitud=(
                "Cordial pero evasivo, siempre pensando en el turismo del año "
                "que viene. Si sienten que insisten, se pone nervioso por la "
                "reputación del pueblo, no por el caso en sí."
            ),
            secretos=[
                Secreto(
                    id="miedo_reputacion",
                    pista=(
                        "Norberto teme que un escándalo médico hunda la "
                        "temporada turística del pueblo del año próximo."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por qué el pueblo no habla del tema: "
                        "admitís, con preocupación política, que temés que un "
                        "escándalo así hunda la temporada turística del año "
                        "que viene."
                    ),
                    criterio_revelacion=(
                        "Admite temer que un escándalo médico afecte el turismo "
                        "del pueblo."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="ainhoa",
            nombre="Dra. Ainhoa Pallares",
            cargo="directora del Centro de Radioterapia",
            color="red",
            es_culpable=True,
            personalidad=(
                "Querida en el pueblo, agotada, cargando una culpa que no "
                "termina de procesar. Responde con calidez profesional que se "
                "quiebra un poco cada vez que el tema se acerca demasiado."
            ),
            coartada=(
                "Dice que el día del incidente hizo su trabajo normal, y que el "
                "informe que se presentó fue el que ella misma redactó."
            ),
            actitud=(
                "Cálida y colaboradora en general, la única del pueblo que no "
                "esquiva el tema por completo — pero se pone visiblemente "
                "afectada si le preguntan por el cálculo de dosis en concreto."
            ),
            secretos=[
                Secreto(
                    id="calculo_propio",
                    pista=(
                        "Fue la propia Dra. Pallares quien calculó mal la dosis "
                        "esa tarde, distraída por un problema personal."
                    ),
                    instruccion_actor=(
                        "Solo si te preguntan directamente quién calculó la "
                        "dosis ese día: admitís, con la voz quebrada, que "
                        "fuiste vos misma, distraída por un problema personal "
                        "que preferís no detallar."
                    ),
                    criterio_revelacion=(
                        "Admite haber calculado ella misma la dosis que causó "
                        "la muerte del paciente."
                    ),
                ),
                Secreto(
                    id="informe_reemplazado",
                    pista=(
                        "Ainhoa redactó personalmente el informe alternativo "
                        "que reemplazó al original, hablando de una "
                        "'complicación clínica imprevista'."
                    ),
                    instruccion_actor=(
                        "Solo si ya admitiste el error de cálculo Y te "
                        "preguntan quién redactó el informe final: admitís, "
                        "resignada, que lo redactaste vos misma, y que no fue "
                        "un accidente que dijera 'complicación imprevista' en "
                        "vez de la verdad."
                    ),
                    criterio_revelacion=(
                        "Admite haber redactado ella misma el informe "
                        "alternativo que encubrió el error real."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="braian",
            nombre="Braian Melivilu",
            cargo="familiar del paciente fallecido",
            color="yellow",
            personalidad=(
                "Dolido, desconfiado del silencio del pueblo, pero atrapado "
                "por la ayuda médica que su familia todavía necesita del "
                "Centro."
            ),
            coartada=(
                "No es sospechoso en el sentido clásico: es quien más quiere "
                "que la verdad salga, aunque le cueste hablar de eso."
            ),
            actitud=(
                "Dolido y contenido al principio. Si sienten que de verdad "
                "buscan la verdad y no solo un culpable rápido, se abre por "
                "completo."
            ),
            secretos=[
                Secreto(
                    id="atencion_gratuita",
                    pista=(
                        "La familia de Braian recibió atención médica gratuita "
                        "de por vida para otro familiar enfermo, poco después "
                        "de la muerte."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por qué tu familia no reclamó "
                        "legalmente: contás, con dolor y algo de vergüenza, que "
                        "el Centro les ofreció atención médica gratuita de por "
                        "vida para otro familiar enfermo, y que no supieron "
                        "decir que no."
                    ),
                    criterio_revelacion=(
                        "Cuenta que su familia recibió atención médica gratuita "
                        "de por vida a cambio de no reclamar."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="ceferino",
            nombre="Padre Ceferino",
            cargo="cura párroco de Epuyén",
            color="green",
            personalidad=(
                "Reservado por naturaleza y por oficio, escucha mucho más de "
                "lo que alguna vez repite. Cree en la reparación privada antes "
                "que en el escándalo público."
            ),
            coartada=(
                "No estuvo presente en ningún hecho concreto: su rol es haber "
                "acompañado a la familia después de la muerte."
            ),
            actitud=(
                "Calmo y cuidadoso con lo que cuenta, protegiendo la "
                "confianza de sus feligreses. Si sienten respeto por eso, "
                "comparte lo que puede sin romper esa confianza."
            ),
            secretos=[
                Secreto(
                    id="acompano_acuerdo",
                    pista=(
                        "El Padre Ceferino ayudó a mediar el acuerdo entre la "
                        "Dra. Pallares y la familia del paciente."
                    ),
                    instruccion_actor=(
                        "Si te preguntan si sabías del acuerdo entre el "
                        "Centro y la familia: admitís, con cuidado, que "
                        "ayudaste a mediarlo, porque creíste que era mejor "
                        "para la familia que un juicio largo."
                    ),
                    criterio_revelacion=(
                        "Admite haber mediado el acuerdo entre la Dra. "
                        "Pallares y la familia del paciente."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="xime",
            nombre="Xime Calfunao",
            cargo="recepcionista del Centro de Radioterapia",
            color="magenta",
            personalidad=(
                "Joven, todavía no curtida en los silencios del pueblo. Sabe "
                "más de lo que le corresponde por estar siempre en el "
                "mostrador."
            ),
            coartada=(
                "Dice que ese día trabajó su turno normal, sin ver nada fuera "
                "de lo común hasta que el clima del Centro cambió de golpe."
            ),
            actitud=(
                "Nerviosa por ser la más joven y la más nueva. Si sienten que "
                "la tratan con paciencia, termina contando lo que escuchó sin "
                "querer."
            ),
            secretos=[
                Secreto(
                    id="informe_original_visto",
                    pista=(
                        "Xime alcanzó a ver, un instante, el informe original "
                        "antes de que la Dra. Pallares lo reemplazara."
                    ),
                    instruccion_actor=(
                        "Solo si te ganás su confianza (varias preguntas con "
                        "paciencia) y le preguntan si vio algún informe: "
                        "confesás, nerviosa, que alcanzaste a ver el informe "
                        "original un instante antes de que la Dra. Pallares lo "
                        "reemplazara."
                    ),
                    criterio_revelacion=(
                        "Admite haber visto el informe original antes de que "
                        "fuera reemplazado."
                    ),
                ),
            ],
        ),
    ],
)
