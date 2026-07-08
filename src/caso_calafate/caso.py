"""Definición del caso: sospechosos, secretos y pistas.

Este módulo es puro CONTENIDO más validación: acá no hay LLMs ni grafos.
Separar los datos del juego de la lógica del motor tiene dos ventajas:

1. Se puede testear cada mitad por su lado (mirá ``tests/test_caso.py``).
2. Escribir un caso nuevo es escribir datos, sin tocar el motor.

Modelamos con Pydantic (y no con dataclasses) porque valida los datos al
construirlos — un caso mal armado explota al importar el módulo, no en el
medio de una partida — y porque es la misma librería que LangChain usa para
"structured output", así que la vas a ver por todo el proyecto.

⚠️ SPOILER: leer los datos de este archivo revela al culpable.
Jugá una partida antes. :)
"""

import unicodedata

from pydantic import BaseModel, Field, model_validator


def _normalizar(texto: str) -> str:
    """Minúsculas y sin tildes, para comparar nombres sin sufrir ("Julián" == "julian")."""
    descompuesto = unicodedata.normalize("NFD", texto)
    sin_tildes = "".join(c for c in descompuesto if unicodedata.category(c) != "Mn")
    return sin_tildes.lower().strip()


class Secreto(BaseModel):
    """Algo que un sospechoso sabe y puede soltar si le preguntan bien.

    Cada secreto se describe tres veces, una por "audiencia":

    - ``instruccion_actor``: para el LLM que actúa al sospechoso
      (cuándo y cómo soltar el secreto).
    - ``criterio_revelacion``: para el LLM analista, que decide si la
      respuesta del sospechoso efectivamente lo reveló.
    - ``pista``: lo que ve el jugador en su libreta cuando se revela.
    """

    id: str = Field(description="Identificador único, ej. 'tarjeta_perdida'")
    pista: str = Field(description="Texto que ve el jugador en /pistas")
    instruccion_actor: str = Field(description="Regla de actuación para el LLM sospechoso")
    criterio_revelacion: str = Field(description="Criterio que evalúa el LLM analista")


class Sospechoso(BaseModel):
    """Un personaje interrogable. Todo lo que define su actuación vive acá."""

    id: str = Field(description="Slug corto, ej. 'marta'")
    nombre: str
    cargo: str
    personalidad: str = Field(description="Cómo habla y reacciona en general")
    coartada: str = Field(description="Lo que DICE que hizo esa noche (sea verdad o mentira)")
    actitud: str = Field(description="Cómo responde cuando lo presionan")
    es_culpable: bool = False
    secretos: list[Secreto] = Field(default_factory=list)
    color: str = Field(default="white", description="Color de rich para el CLI")


class Caso(BaseModel):
    """El caso completo: ambientación, sospechosos y reglas de la partida."""

    titulo: str
    briefing: str = Field(description="Lo que se le cuenta al jugador al arrancar")
    contexto_actores: str = Field(description="Resumen de los hechos que todo personaje conoce")
    epilogo: str = Field(description="La verdad completa; se muestra al terminar la partida")
    max_preguntas: int = Field(default=15, ge=1)
    sospechosos: list[Sospechoso]

    @model_validator(mode="after")
    def _validar_consistencia(self) -> "Caso":
        """Un caso jugable necesita exactamente un culpable y secretos sin ids repetidos."""
        culpables = [s for s in self.sospechosos if s.es_culpable]
        if len(culpables) != 1:
            raise ValueError(f"el caso necesita exactamente 1 culpable, hay {len(culpables)}")
        ids = [secreto.id for s in self.sospechosos for secreto in s.secretos]
        if len(ids) != len(set(ids)):
            raise ValueError("hay ids de secretos repetidos entre los sospechosos")
        return self

    # ── Helpers de consulta (los usan los nodos del grafo y el CLI) ──────────

    def sospechoso(self, id_: str) -> Sospechoso | None:
        """Busca un sospechoso por su id exacto."""
        return next((s for s in self.sospechosos if s.id == id_), None)

    def buscar_sospechoso(self, texto: str) -> Sospechoso | None:
        """Búsqueda tolerante para el CLI: por id o por nombre, sin tildes ni mayúsculas.

        Acepta prefijos ("mar" encuentra a Marta), así el jugador no tiene que
        tipear nombres completos.
        """
        consulta = _normalizar(texto)
        if not consulta:
            return None
        for s in self.sospechosos:
            if consulta == s.id or _normalizar(s.nombre).startswith(consulta):
                return s
        return None

    def secreto(self, id_: str) -> Secreto | None:
        """Busca un secreto por id, entre todos los sospechosos."""
        for s in self.sospechosos:
            for secreto in s.secretos:
                if secreto.id == id_:
                    return secreto
        return None

    def total_secretos(self) -> int:
        return sum(len(s.secretos) for s in self.sospechosos)

    def culpable(self) -> Sospechoso:
        return next(s for s in self.sospechosos if s.es_culpable)


# ═════════════════════════════════════════════════════════════════════════════
# EL CASO CALAFATE
# ═════════════════════════════════════════════════════════════════════════════

CASO_CALAFATE = Caso(
    titulo="EL CASO CALAFATE",
    # Los párrafos van en una sola línea lógica (concatenación implícita de
    # strings): rich los envuelve al ancho de la terminal. Los saltos duros
    # quedan solo donde son intencionales (la lista de viñetas).
    briefing=(
        "Bariloche, 06:50 de la mañana. Te suena el teléfono.\n\n"
        "«Detective, lo necesitamos en el Centro Espacial Patagónico. Ya.»\n\n"
        "A 48 horas de su traslado a la base de lanzamiento, alguien entró de "
        "madrugada a la sala limpia y cortó el mazo de cables del subsistema de "
        "energía del satélite CALAFATE-1, el proyecto más importante en la "
        "historia del Centro.\n\n"
        "Lo que se sabe hasta ahora:\n\n"
        " • El sabotaje ocurrió cerca de las 03:00. Lo descubrió el turno mañana a las 06:40.\n"
        " • La cámara de la sala limpia dejó de grabar a las 02:50.\n"
        " • El registro de accesos muestra UNA sola entrada en la madrugada:\n"
        "   la tarjeta de Marta Iriarte, la ingeniera jefa, a las 03:02.\n"
        " • Esa noche había tres personas con acceso al edificio. Son tus sospechosos.\n\n"
        "Interrogá, anotá, y cuando estés seguro: acusá. Tenés una sola oportunidad."
    ),
    contexto_actores="""\
Anoche, cerca de las 03:00, alguien cortó el mazo de cables del subsistema de
energía del satélite CALAFATE-1 en la sala limpia del Centro Espacial Patagónico
(Bariloche), a 48 horas del traslado para su lanzamiento. La cámara de la sala
dejó de grabar a las 02:50. El registro de accesos marca una única entrada de
madrugada: la tarjeta de Marta Iriarte a las 03:02. Un detective está
interrogando al personal que tenía acceso esa noche.""",
    epilogo=(
        "Silvia Roldán saboteó el satélite.\n\n"
        "Hace un mes había reportado una falla en el subsistema de energía; el "
        "comité la desestimó por presiones de cronograma y la apartó del comité "
        "de lanzamiento. Humillada — y convencida de que el satélite iba a "
        "fallar en órbita y la iban a culpar a ella — decidió forzar la "
        "revisión: si el CALAFATE-1 no podía lanzarse a tiempo, alguien iba a "
        "tener que releer su informe.\n\n"
        "El jueves, al final de la reunión de revisión, encontró la tarjeta que "
        "Marta había olvidado en la oficina de Calidad. La guardó. La madrugada "
        "del sabotaje apagó la cámara desde la consola central (02:50), entró a "
        "la sala limpia con la tarjeta ajena (03:02) y cortó exactamente el mazo "
        "de cables que ella misma había denunciado. Julián, que volvía de dormir "
        "en el depósito, se la cruzó a las 03:20 sin reconocerla: solo vio el "
        "buzo azul de Calidad.\n\n"
        "Un plan casi perfecto — arruinado por la siesta de un técnico junior."
    ),
    max_preguntas=15,
    sospechosos=[
        Sospechoso(
            id="marta",
            nombre="Marta Iriarte",
            cargo="ingeniera jefa de integración",
            color="bright_cyan",
            personalidad=(
                "Seca, orgullosa, brillante. Quince años en el Centro. Odia perder el "
                "tiempo y lo demuestra. Se ofende rápido si sienten que dudan de su "
                "trabajo. Frases cortas y técnicas."
            ),
            coartada=(
                "Dice que se fue del Centro a las 21:00 y durmió sola en su casa de "
                "Villa Los Coihues. Nadie puede confirmarlo."
            ),
            actitud=(
                "Si la presionan se indigna y recuerda su trayectoria impecable. Pero si "
                "le preguntan por su tarjeta o por el registro de accesos, duda, baja la "
                "voz y se pone evasiva antes de admitir la verdad."
            ),
            secretos=[
                Secreto(
                    id="tarjeta_perdida",
                    pista=(
                        "La tarjeta que abrió la sala limpia a las 03:02 no la tenía "
                        "Marta: la perdió el jueves y no lo reportó."
                    ),
                    instruccion_actor=(
                        "Solo si te preguntan directamente por tu tarjeta o por el "
                        "registro de accesos de esa noche: admitís, con mucha vergüenza, "
                        "que perdiste la tarjeta el jueves y no lo reportaste, porque "
                        "reportarla es una falta grave. Jurás que vos no entraste."
                    ),
                    criterio_revelacion=(
                        "Admite que perdió o extravió su tarjeta de acceso y que no la "
                        "tenía la noche del sabotaje."
                    ),
                ),
                Secreto(
                    id="tarjeta_en_calidad",
                    pista=(
                        "Marta perdió su tarjeta el jueves, durante la reunión de "
                        "revisión en la oficina de Calidad."
                    ),
                    instruccion_actor=(
                        "Solo si ya admitiste que perdiste la tarjeta y te preguntan "
                        "DÓNDE la perdiste o quién pudo agarrarla: recordás que la última "
                        "vez que la usaste fue el jueves a la tarde, antes de la reunión "
                        "de revisión en la oficina de Calidad."
                    ),
                    criterio_revelacion=(
                        "Dice que perdió la tarjeta en la oficina de Calidad o durante "
                        "la reunión de revisión del jueves."
                    ),
                ),
                Secreto(
                    id="resentimiento_silvia",
                    pista=(
                        "Silvia Roldán reportó una falla en el subsistema de energía; el "
                        "comité la desestimó y la bajó del comité de lanzamiento. Quedó "
                        "furiosa."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por tus compañeros, por Silvia o por conflictos "
                        "en el proyecto: contás, sin culpa, que Silvia presentó un "
                        "informe sobre una supuesta falla de energía, que el comité lo "
                        "desestimó por infundado y que la sacaron del comité de "
                        "lanzamiento. Que quedó muy resentida."
                    ),
                    criterio_revelacion=(
                        "Cuenta que Silvia reportó una falla que fue desestimada, o que "
                        "la sacaron del comité de lanzamiento y quedó resentida."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="julian",
            nombre="Julián Funes",
            cargo="técnico de guardia (junior)",
            color="bright_yellow",
            personalidad=(
                "Veinticinco años, primer trabajo importante. Nervioso, atropellado, "
                "habla de más y se contradice cuando se pone ansioso. Buen pibe."
            ),
            coartada=(
                "Dice que estuvo toda la noche en el puesto de guardia del edificio de "
                "integración y que no vio ni escuchó nada raro."
            ),
            actitud=(
                "Cuanto más lo presionan, más se enreda. Si le marcan una contradicción "
                "(por ejemplo, cómo pudo entrar alguien sin que lo viera), se quiebra "
                "rápido y confiesa sus verdades chicas, suplicando que no lo echen."
            ),
            secretos=[
                Secreto(
                    id="guardia_dormido",
                    pista=(
                        "Julián abandonó el puesto de guardia: entre las 02:30 y las "
                        "03:20 durmió una siesta en el depósito. Por eso no vio entrar "
                        "a nadie."
                    ),
                    instruccion_actor=(
                        "Al principio lo negás («estuve en el puesto toda la noche»). Si "
                        "te presionan sobre qué viste, cómo pudo entrar alguien sin que "
                        "lo notes, o te marcan contradicciones: confesás, muerto de "
                        "culpa, que venías de dos turnos seguidos y te fuiste a dormir "
                        "al depósito tipo 02:30, y que volviste al puesto pasadas las "
                        "03:20."
                    ),
                    criterio_revelacion=(
                        "Admite que se ausentó del puesto de guardia o que durmió en el "
                        "depósito durante la madrugada."
                    ),
                ),
                Secreto(
                    id="buzo_calidad",
                    pista=(
                        "Cerca de las 03:20, volviendo del depósito, Julián se cruzó de "
                        "lejos con alguien que salía del pasillo de la sala limpia con "
                        "un buzo azul del área de Calidad."
                    ),
                    instruccion_actor=(
                        "Solo si te preguntan si viste a alguien esa noche (o si, "
                        "después de confesar la siesta, te preguntan qué viste al "
                        "volver): contás que al volver del depósito, cerca de las 03:20, "
                        "viste de lejos a alguien que salía del pasillo de la sala "
                        "limpia con un buzo azul con el logo del área de Calidad. No le "
                        "viste la cara y en el momento no le diste importancia."
                    ),
                    criterio_revelacion=(
                        "Menciona haber visto a alguien con un buzo o ropa del área de "
                        "Calidad cerca de la sala limpia esa madrugada."
                    ),
                ),
            ],
        ),
        Sospechoso(
            id="silvia",
            nombre="Silvia Roldán",
            cargo="responsable de Calidad y Seguridad",
            color="bright_magenta",
            es_culpable=True,
            personalidad=(
                "Metódica, amable, siempre correcta. Respuestas prolijas, casi "
                "ensayadas. La clase de persona que contesta una pregunta citando un "
                "procedimiento."
            ),
            coartada=(
                "Dice que se fue a las 19:30, cenó con su hermana y se quedó en su casa "
                "terminando un informe hasta tarde."
            ),
            actitud=(
                "Nunca pierde la calma. Si la confrontan con evidencia, la «explica» "
                "con tecnicismos y desvía la sospecha hacia Marta («la tarjeta era de "
                "ella, ¿no?»). Jamás confiesa; cuanto más la aprietan, más fríos y "
                "raros se vuelven sus argumentos."
            ),
            secretos=[
                Secreto(
                    id="camara_por_sistema",
                    pista=(
                        "La cámara de la sala limpia no se desenchufó: la apagaron desde "
                        "la consola central de seguridad, a la que solo acceden dos "
                        "áreas — Seguridad y Calidad."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por la cámara, cometés tu único descuido: "
                        "explicás con demasiado detalle técnico que desenchufarla es "
                        "imposible, que solo se apaga desde la consola central de "
                        "seguridad... y recién ahí notás que dijiste de más y aclarás, "
                        "rápido, que eso lo sabe cualquiera del área. (Solo Calidad y "
                        "Seguridad acceden a esa consola, y vos lo sabés.)"
                    ),
                    criterio_revelacion=(
                        "Revela que la cámara se apagó desde el sistema o consola "
                        "central (no desenchufada), o que solo Calidad y Seguridad "
                        "tienen ese acceso."
                    ),
                ),
                Secreto(
                    id="informe_energia",
                    pista=(
                        "Silvia reportó hace un mes una falla grave en el subsistema de "
                        "energía — exactamente el que apareció saboteado — y el comité "
                        "la ignoró."
                    ),
                    instruccion_actor=(
                        "Si te preguntan por tu informe, por el subsistema de energía o "
                        "por qué te sacaron del comité de lanzamiento: no podés ocultar "
                        "la amargura. Contás que hace un mes reportaste una falla seria "
                        "en el subsistema de energía, que el comité la desestimó «por "
                        "presiones de cronograma» y que te apartaron del comité. "
                        "Remarcás, con ironía, que «casualmente» lo que apareció cortado "
                        "es lo que vos habías señalado."
                    ),
                    criterio_revelacion=(
                        "Cuenta que reportó una falla en el subsistema de energía que "
                        "fue desestimada, o muestra resentimiento por haber sido "
                        "apartada del comité de lanzamiento."
                    ),
                ),
            ],
        ),
    ],
)
