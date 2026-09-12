"""Tests unitarios de los nodos, llamados a mano (sin grafo).

Un nodo es una función ``estado → dict de actualizaciones``: para testearlo
alcanza con armar el estado en un diccionario y mirar qué devuelve. Ni LangGraph
ni checkpointer — eso se prueba aparte, en ``test_grafo.py``.
"""

import pytest
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableLambda

from caso_calafate.nodos import decidir_accion, nodo_acusar, nodo_analizar, nodo_cerrar_turno
from caso_calafate.prompts import SecretosRevelados

# ── decidir_accion (el ruteo de entrada) ─────────────────────────────────────


def test_decidir_accion_devuelve_la_accion_pedida():
    assert decidir_accion({"accion": "interrogar"}) == "interrogar"
    assert decidir_accion({"accion": "acusar"}) == "acusar"


def test_decidir_accion_explota_con_una_accion_desconocida():
    with pytest.raises(ValueError, match="acción desconocida"):
        decidir_accion({"accion": "bailar"})
    with pytest.raises(ValueError, match="acción desconocida"):
        decidir_accion({})  # sin acción tampoco vale


# ── nodo_cerrar_turno ────────────────────────────────────────────────────────


def test_cerrar_turno_cuenta_desde_cero():
    assert nodo_cerrar_turno({}) == {"preguntas_usadas": 1}


def test_cerrar_turno_incrementa_lo_que_habia():
    assert nodo_cerrar_turno({"preguntas_usadas": 3}) == {"preguntas_usadas": 4}


# ── nodo_analizar (el filtro sobre lo que dice el LLM analista) ──────────────


def test_analizar_filtra_ids_alucinados_y_duplicados(caso_asado, analista_fijo):
    """El analista devuelve basura mezclada: un id válido repetido, uno inexistente
    y uno de OTRO sospechoso. Solo debe sobrevivir el válido, una sola vez."""
    analista = analista_fijo(["vio_al_perro", "inventado", "vio_al_perro", "huellas_patio"])
    actualizacion = nodo_analizar(
        {"sospechoso_actual": "michi", "respuesta": "Vi a Moro en la mesa."},
        caso=caso_asado,
        analista=analista,
    )
    # "huellas_patio" es un secreto de Moro: interrogando a Michi no puede salir.
    assert actualizacion["pistas_nuevas"] == ["vio_al_perro"]
    assert actualizacion["pistas_descubiertas"] == ["vio_al_perro"]


def test_analizar_no_repite_pistas_ya_descubiertas(caso_asado, analista_fijo):
    analista = analista_fijo(["vio_al_perro"])
    actualizacion = nodo_analizar(
        {
            "sospechoso_actual": "michi",
            "respuesta": "Ya te lo dije: vi a Moro.",
            "pistas_descubiertas": ["vio_al_perro"],
        },
        caso=caso_asado,
        analista=analista,
    )
    assert actualizacion["pistas_nuevas"] == []


def test_analizar_con_analista_mudo_no_revela_nada(caso_asado, analista_fijo):
    actualizacion = nodo_analizar(
        {"sospechoso_actual": "moro", "respuesta": "Guau."},
        caso=caso_asado,
        analista=analista_fijo([]),
    )
    assert actualizacion == {"pistas_nuevas": [], "pistas_descubiertas": []}


def test_analizar_no_deja_escapar_la_excepcion_si_el_analista_explota(caso_asado):
    """Si el LLM analista se cuelga o tira cualquier excepción, el nodo no
    puede propagarla: el turno ya le preguntó al sospechoso y tiene que
    contar igual (ver nodo_cerrar_turno, que corre después sin condición)."""

    def _analista_roto(_mensajes):
        raise RuntimeError("timeout de ollama")

    actualizacion = nodo_analizar(
        {"sospechoso_actual": "michi", "respuesta": "Vi al perro llevarse el asado."},
        caso=caso_asado,
        analista=RunnableLambda(_analista_roto),
    )
    assert actualizacion == {"pistas_nuevas": []}


# ── nodo_acusar ──────────────────────────────────────────────────────────────


def test_acusar_al_culpable_es_victoria(caso_asado):
    actualizacion = nodo_acusar({"sospechoso_actual": "moro"}, caso=caso_asado)
    assert actualizacion["resultado"] == "victoria"
    assert "Moro" in actualizacion["respuesta"]


def test_acusar_a_un_inocente_es_derrota(caso_asado):
    actualizacion = nodo_acusar({"sospechoso_actual": "michi"}, caso=caso_asado)
    assert actualizacion["resultado"] == "derrota"
    assert "inocente" in actualizacion["respuesta"]


def test_acusar_a_un_inocente_con_reaccion_propia_usa_ese_texto(caso_asado):
    """``reaccion_acusacion_fallida`` reemplaza el mensaje genérico de derrota
    cuando el caso la definió para ese sospechoso."""
    caso_con_reaccion = caso_asado.model_copy(deep=True)
    michi = caso_con_reaccion.sospechoso("michi")
    michi.reaccion_acusacion_fallida = "Michi bosteza y se va, sin dignarse a responder."

    actualizacion = nodo_acusar({"sospechoso_actual": "michi"}, caso=caso_con_reaccion)
    assert actualizacion["resultado"] == "derrota"
    assert actualizacion["respuesta"] == "Michi bosteza y se va, sin dignarse a responder."


def test_acusar_a_alguien_inexistente_explota(caso_asado):
    with pytest.raises(ValueError, match="no existe"):
        nodo_acusar({"sospechoso_actual": "fantasma"}, caso=caso_asado)


def test_el_veredicto_usa_las_palabras_del_caso(caso_asado):
    """El motor no sabe qué se investiga: el texto del veredicto lo pone el
    caso (``delito`` y ``culpable_alias``). Antes decía «sabotaje» siempre,
    jugaras el caso que jugaras."""
    victoria = nodo_acusar({"sospechoso_actual": "moro"}, caso=caso_asado)
    assert caso_asado.delito in victoria["respuesta"]
    assert "sabotaje" not in victoria["respuesta"]

    derrota = nodo_acusar({"sospechoso_actual": "michi"}, caso=caso_asado)
    assert f"El verdadero {caso_asado.culpable_alias}" in derrota["respuesta"]
    assert "saboteador" not in derrota["respuesta"]


def test_el_analista_recibe_instrucciones_como_system(caso_asado):
    """El encuadre del prompt no es cosmético: es la diferencia entre detectar
    la pista y comérsela.

    Medido contra qwen2.5:7b sobre una respuesta que cumplía el criterio: como
    string suelto salía 2 de 8 veces; como SystemMessage + HumanMessage, 4 de
    4. Este test congela el encuadre para que nadie lo "simplifique" sin
    saber lo que cuesta.
    """
    recibido = {}

    def espia(entrada):
        recibido["entrada"] = entrada
        return SecretosRevelados(ids=[])

    nodo_analizar(
        {"sospechoso_actual": "michi", "respuesta": "Vi al perro llevarse el asado."},
        caso=caso_asado,
        analista=RunnableLambda(espia),
    )

    entrada = recibido["entrada"]
    assert isinstance(entrada, list), "el analista tiene que recibir mensajes, no un string"
    assert [type(m) for m in entrada] == [SystemMessage, HumanMessage]
    # Las reglas y los criterios viajan como instrucciones del sistema.
    assert "criterio" in entrada[0].content or "revelado" in entrada[0].content
    assert entrada[0].content.count("vio_al_perro") == 1
