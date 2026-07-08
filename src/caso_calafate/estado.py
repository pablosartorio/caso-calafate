"""El estado compartido del grafo.

En LangGraph, el "estado" es un diccionario tipado que fluye por los nodos.
Cada nodo recibe el estado actual y devuelve SOLO las claves que quiere
actualizar; LangGraph mezcla esa actualización con el estado que ya había.

¿Cómo mezcla? Depende de cómo esté anotada cada clave:

- Por defecto: el valor nuevo REEMPLAZA al viejo.
- Si la clave está anotada con un "reducer" (una función), LangGraph llama
  ``reducer(valor_viejo, valor_nuevo)`` y guarda el resultado. Acá lo usamos
  para que las pistas se ACUMULEN entre turnos en lugar de pisarse.

Además, como el grafo se compila con un checkpointer (ver ``grafo.py``), este
estado PERSISTE entre invocaciones: cada turno del juego es un ``invoke()``
nuevo, pero la partida (pistas, conversaciones, preguntas usadas) sigue viva.
"""

from typing import Annotated, Literal, TypedDict

from langchain_core.messages import BaseMessage

# El tipo de jugada que el CLI le pide al grafo en cada turno.
Accion = Literal["interrogar", "acusar"]

# Cómo terminó la partida. Mientras sigue abierta, el estado no tiene resultado.
Resultado = Literal["victoria", "derrota"]


def acumular_pistas(previas: list[str], nuevas: list[str]) -> list[str]:
    """Reducer para ``pistas_descubiertas``: suma sin duplicar, conservando el orden.

    LangGraph la llama automáticamente cada vez que un nodo devuelve esa clave.
    """
    return previas + [p for p in nuevas if p not in previas]


class EstadoJuego(TypedDict, total=False):
    """Todo lo que el grafo sabe de la partida.

    ``total=False`` marca todas las claves como opcionales: en cada ``invoke()``
    el CLI pasa solo las claves de entrada del turno, y los nodos usan
    ``estado.get(...)`` con defaults para las que todavía no existen.
    """

    # ── Entrada del turno (la carga el CLI en cada invoke) ───────────────────
    accion: Accion
    sospechoso_actual: str  # id del sospechoso al que se interroga o acusa
    pregunta: str  # texto libre del jugador (solo para "interrogar")

    # ── Memoria de la partida (persiste entre turnos vía checkpointer) ──────
    conversaciones: dict[str, list[BaseMessage]]  # historial por sospechoso
    pistas_descubiertas: Annotated[list[str], acumular_pistas]  # ids de secretos
    preguntas_usadas: int
    resultado: Resultado | None

    # ── Salida del turno (para que el CLI la muestre) ────────────────────────
    respuesta: str  # lo que dijo el sospechoso, o el texto del veredicto
    pistas_nuevas: list[str]  # ids revelados en ESTE turno (para el cartel 🔎)
