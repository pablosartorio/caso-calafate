"""Los nodos del grafo: cada uno es una función ``estado → actualización parcial``.

Un nodo de LangGraph recibe el estado completo y devuelve un diccionario con
SOLO las claves que quiere actualizar (LangGraph mezcla el resto solo — ver
``estado.py``). Esa forma tan simple es lo que hace a los nodos fáciles de
testear: se los llama a mano con un dict armado en el test y se mira qué
devuelven, sin levantar ningún grafo.

Los nodos que necesitan un LLM lo reciben como argumento extra (``actor``,
``analista``) en lugar de crearlo adentro. Eso se llama inyección de
dependencias, y es lo que permite que los tests enchufen modelos falsos:
``grafo.py`` fija esos argumentos con ``functools.partial`` al armar el grafo.
"""

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import Runnable

from caso_calafate.caso import Caso
from caso_calafate.estado import Accion, EstadoJuego
from caso_calafate.llm import texto_de
from caso_calafate.prompts import SecretosRevelados, prompt_analista, prompt_sospechoso


def decidir_accion(estado: EstadoJuego) -> Accion:
    """Función de ruteo de la arista condicional de entrada.

    No es un nodo: no modifica el estado. Solo mira la acción pedida y devuelve
    el nombre del nodo al que hay que ir. LangGraph la usa como "guardabarrera"
    en START (ver el mapa de rutas en ``grafo.py``).
    """
    accion = estado.get("accion")
    if accion not in ("interrogar", "acusar"):
        raise ValueError(f"acción desconocida: {accion!r} (esperaba 'interrogar' o 'acusar')")
    return accion


def nodo_interrogar(estado: EstadoJuego, *, caso: Caso, actor: BaseChatModel) -> dict:
    """Le hace la pregunta del jugador al sospechoso (una llamada al LLM actor).

    Arma los mensajes como [system del personaje] + historial + [pregunta nueva],
    y guarda el par pregunta/respuesta en el historial de ESE sospechoso, para
    que en el próximo turno el personaje recuerde la charla.
    """
    sospechoso = caso.sospechoso(estado["sospechoso_actual"])
    if sospechoso is None:
        raise ValueError(f"no existe el sospechoso {estado['sospechoso_actual']!r}")

    historial = estado.get("conversaciones", {}).get(sospechoso.id, [])
    pregunta = HumanMessage(estado["pregunta"])
    mensajes = [SystemMessage(prompt_sospechoso(caso, sospechoso)), *historial, pregunta]

    respuesta = actor.invoke(mensajes)

    conversaciones = dict(estado.get("conversaciones", {}))
    conversaciones[sospechoso.id] = [*historial, pregunta, respuesta]
    return {"conversaciones": conversaciones, "respuesta": texto_de(respuesta)}


def nodo_analizar(estado: EstadoJuego, *, caso: Caso, analista: Runnable) -> dict:
    """Revisa la respuesta del sospechoso y anota los secretos que reveló.

    El analista devuelve un ``SecretosRevelados`` (salida estructurada), pero
    igual filtramos lo que dice: un LLM puede alucinar un id inexistente o
    repetir uno ya descubierto, y el estado del juego tiene que quedar sano.

    Fijate que devolvemos ``pistas_descubiertas`` con SOLO las nuevas: el
    reducer ``acumular_pistas`` (ver ``estado.py``) se encarga de sumarlas a
    las que ya había.
    """
    sospechoso = caso.sospechoso(estado["sospechoso_actual"])
    if sospechoso is None or not sospechoso.secretos:
        return {"pistas_nuevas": []}

    veredicto: SecretosRevelados = analista.invoke(
        prompt_analista(sospechoso, estado.get("respuesta", ""))
    )

    validos = {s.id for s in sospechoso.secretos}
    ya_descubiertas = set(estado.get("pistas_descubiertas", []))
    nuevas = [
        id_
        for id_ in dict.fromkeys(veredicto.ids)  # dict.fromkeys: dedup conservando orden
        if id_ in validos and id_ not in ya_descubiertas
    ]
    return {"pistas_nuevas": nuevas, "pistas_descubiertas": nuevas}


def nodo_cerrar_turno(estado: EstadoJuego) -> dict:
    """Contabiliza la pregunta gastada.

    Nodo 100 % determinista, sin LLM: los más baratos de testear y los que más
    conviene mantener separados de los nodos "con magia".
    """
    return {"preguntas_usadas": estado.get("preguntas_usadas", 0) + 1}


def nodo_acusar(estado: EstadoJuego, *, caso: Caso) -> dict:
    """Resuelve la acusación final y cierra la partida.

    Pura lógica de juego: comparar al acusado con el culpable del caso.
    """
    acusado = caso.sospechoso(estado["sospechoso_actual"])
    if acusado is None:
        raise ValueError(f"no existe el sospechoso {estado['sospechoso_actual']!r}")

    if acusado.es_culpable:
        resultado = "victoria"
        veredicto = (
            f"Acusás a {acusado.nombre}, {acusado.cargo}. La evidencia encaja: "
            f"tras un largo silencio, {acusado.nombre} confiesa el sabotaje. Caso cerrado."
        )
    else:
        resultado = "derrota"
        veredicto = (
            f"Acusás a {acusado.nombre}, {acusado.cargo}... y la acusación se desarma "
            f"en minutos: {acusado.nombre} era inocente. El verdadero saboteador queda libre."
        )
    return {"resultado": resultado, "respuesta": veredicto, "pistas_nuevas": []}
