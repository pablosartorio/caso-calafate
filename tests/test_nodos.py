"""Tests unitarios de los nodos, llamados a mano (sin grafo).

Un nodo es una función ``estado → dict de actualizaciones``: para testearlo
alcanza con armar el estado en un diccionario y mirar qué devuelve. Ni LangGraph
ni checkpointer — eso se prueba aparte, en ``test_grafo.py``.
"""

import pytest

from caso_calafate.nodos import decidir_accion, nodo_acusar, nodo_analizar, nodo_cerrar_turno

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


# ── nodo_acusar ──────────────────────────────────────────────────────────────


def test_acusar_al_culpable_es_victoria(caso_asado):
    actualizacion = nodo_acusar({"sospechoso_actual": "moro"}, caso=caso_asado)
    assert actualizacion["resultado"] == "victoria"
    assert "Moro" in actualizacion["respuesta"]


def test_acusar_a_un_inocente_es_derrota(caso_asado):
    actualizacion = nodo_acusar({"sospechoso_actual": "michi"}, caso=caso_asado)
    assert actualizacion["resultado"] == "derrota"
    assert "inocente" in actualizacion["respuesta"]


def test_acusar_a_alguien_inexistente_explota(caso_asado):
    with pytest.raises(ValueError, match="no existe"):
        nodo_acusar({"sospechoso_actual": "fantasma"}, caso=caso_asado)
