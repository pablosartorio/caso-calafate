"""Acá se arma el grafo de LangGraph. El dibujo completo:

                    ┌─→ interrogar ─→ analizar ─→ cerrar_turno ─┐
    START ─(¿accion?)┤                                           ├─→ END
                    └─→ acusar ─────────────────────────────────┘

Cada turno del juego es UNA invocación del grafo: el CLI pasa la jugada
(``accion`` + datos) y el grafo la procesa de punta a punta. La partida entera
vive en el checkpointer: como compilamos con ``MemorySaver`` y el CLI siempre
invoca con el mismo ``thread_id``, LangGraph recupera el estado del turno
anterior y le mezcla la jugada nueva. Distintos ``thread_id`` = partidas
paralelas independientes (hay un test que lo demuestra).
"""

from functools import partial

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.runnables import Runnable
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from caso_calafate.caso import Caso
from caso_calafate.estado import EstadoJuego
from caso_calafate.nodos import (
    decidir_accion,
    nodo_acusar,
    nodo_analizar,
    nodo_cerrar_turno,
    nodo_interrogar,
)


def construir_grafo(
    caso: Caso,
    actor: BaseChatModel,
    analista: Runnable,
    checkpointer: BaseCheckpointSaver | None = None,
) -> CompiledStateGraph:
    """Construye y compila el grafo del juego.

    Args:
        caso: los datos del misterio (sospechosos, secretos, reglas).
        actor: chat model que interpreta a los sospechosos.
        analista: runnable que recibe un prompt y devuelve ``SecretosRevelados``.
        checkpointer: dónde persistir el estado entre turnos. Por defecto,
            en memoria (la partida dura lo que dura el proceso).

    Pasar ``actor`` y ``analista`` desde afuera — en vez de crearlos acá — es
    inyección de dependencias: los tests enchufan modelos falsos y el juego
    completo corre sin API key (ver ``tests/test_grafo.py``).
    """
    grafo = StateGraph(EstadoJuego)

    # partial() fija los argumentos extra de cada nodo; LangGraph solo va a
    # llamarlos con el estado, que es el único argumento que queda libre.
    grafo.add_node("interrogar", partial(nodo_interrogar, caso=caso, actor=actor))
    grafo.add_node("analizar", partial(nodo_analizar, caso=caso, analista=analista))
    grafo.add_node("cerrar_turno", nodo_cerrar_turno)
    grafo.add_node("acusar", partial(nodo_acusar, caso=caso))

    # Arista condicional de entrada: decidir_accion mira el estado y devuelve
    # una clave del mapa; el mapa dice a qué nodo saltar.
    grafo.add_conditional_edges(
        START,
        decidir_accion,
        {"interrogar": "interrogar", "acusar": "acusar"},
    )

    # La rama del interrogatorio es una tubería fija de tres pasos.
    grafo.add_edge("interrogar", "analizar")
    grafo.add_edge("analizar", "cerrar_turno")
    grafo.add_edge("cerrar_turno", END)

    # La acusación termina la partida en un solo paso.
    grafo.add_edge("acusar", END)

    return grafo.compile(checkpointer=checkpointer or MemorySaver())
