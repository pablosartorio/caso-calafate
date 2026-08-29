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

import random
import unicodedata
from collections.abc import Iterable

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

    # ── El vocabulario del caso ──────────────────────────────────────────────
    # Los prompts, el veredicto y la interfaz hablan del hecho concreto que se
    # investiga. Sin estos campos, el motor tendría que inventarse una palabra
    # ("el sabotaje") que solo es cierta en algunos casos: acá cada caso pone
    # la suya. Nada de esto spoilea — describe el HECHO, nunca a su autor.
    sede: str = Field(description="El organismo donde pasa todo, ej. 'Centro Espacial Patagónico'")
    ciudad: str = Field(description="Dónde queda la sede, ej. 'Bariloche'")
    delito: str = Field(
        description="El hecho a resolver, con artículo y sin nombrar al culpable: encaja en "
        "«cometiste ___» y «confesó ___», ej. 'el sabotaje del satélite CALAFATE-1'"
    )
    culpable_alias: str = Field(
        description="Cómo le dice la prensa al culpable sin nombre: un sustantivo masculino "
        "singular SIN artículo, que encaje en «el ___ sigue libre», ej. 'saboteador'"
    )
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

    def sospechosos_para(self, semilla: str) -> list[Sospechoso]:
        """Los sospechosos en un orden barajado, propio de cada partida.

        El orden en que están escritos en el archivo del caso terminó siendo
        una pista involuntaria: en los once casos, el culpable casi nunca es
        el del medio. Un jugador que lo nota descarta uno sin preguntar nada.

        La semilla es el id de la partida, así que el orden es distinto entre
        partidas pero SIEMPRE el mismo dentro de una: si cambiara en cada
        request, las fichas del escritorio se reordenarían solas al recargar.

        Ojo: esto solo cambia cómo se MUESTRAN. Buscar por nombre, resolver
        la acusación y contar secretos no dependen del orden.
        """
        barajados = list(self.sospechosos)
        random.Random(semilla).shuffle(barajados)
        return barajados


def buscar_caso(catalogo: Iterable[Caso], texto: str) -> Caso | None:
    """Búsqueda tolerante de un caso: gemela de ``Caso.buscar_sospechoso``.

    Acepta el id o el título, sin tildes ni mayúsculas y por prefijo, así el
    jugador puede tipear «piltriquitrón» (como lo ve escrito en la tabla) y
    no solo el slug pelado «piltriquitron».
    """
    consulta = _normalizar(texto)
    if not consulta:
        return None
    for caso in catalogo:
        # Los títulos arrancan todos con "EL CASO ...", así que se prueba
        # también sin ese prefijo: "río negro" tiene que encontrar el suyo.
        titulo = _normalizar(caso.titulo)
        nombre = titulo.removeprefix("el caso ").strip()
        if consulta == _normalizar(caso.id) or titulo.startswith(consulta):
            return caso
        if nombre.startswith(consulta):
            return caso
    # Segunda vuelta, más laxa: un prefijo del id ("pilt" encuentra el caso).
    return next((c for c in catalogo if _normalizar(c.id).startswith(consulta)), None)
