"""El modelo de datos de un caso: sospechosos, secretos y pistas.

Este módulo es puro MODELO más validación: acá no hay LLMs, grafos, ni el
contenido de ningún caso puntual. Los casos jugables (uno por archivo) viven
en el paquete ``caso_calafate.casos`` — separar los datos del juego de la
lógica del motor tiene dos ventajas:

1. Se puede testear cada mitad por su lado (mirá ``tests/test_caso.py``).
2. Escribir un caso nuevo es escribir datos, sin tocar el motor.

Modelamos con Pydantic (y no con dataclasses) porque valida los datos al
construirlos — un caso mal armado explota al importar el módulo, no en el
medio de una partida — y porque es la misma librería que LangChain usa para
"structured output", así que la vas a ver por todo el proyecto.
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

    id: str = Field(description="Slug único del caso, ej. 'calafate'. Clave del registro y la DB")
    titulo: str
    gancho: str = Field(
        description="Una línea de enganche SIN spoilers para la tarjeta del selector de casos"
    )
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

