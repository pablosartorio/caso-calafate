"""Tests de integración del grafo completo, con modelos falsos.

Acá se prueba lo que los tests unitarios no pueden: que los nodos estén bien
CONECTADOS, que el ruteo condicional funcione y que el checkpointer haga
persistir la partida entre invocaciones. Como actor y analista se inyectan
(ver ``construir_grafo``), todo corre sin API key.
"""

from caso_calafate.grafo import construir_grafo


def _config(partida: str = "test") -> dict:
    """Config de LangGraph: el thread_id identifica la partida en el checkpointer."""
    return {"configurable": {"thread_id": partida}}


def _jugada_interrogar(sospechoso: str, pregunta: str) -> dict:
    return {"accion": "interrogar", "sospechoso_actual": sospechoso, "pregunta": pregunta}


# ── La rama del interrogatorio, de punta a punta ─────────────────────────────


def test_un_turno_de_interrogatorio_completo(caso_asado, actor_loro, analista_fijo):
    grafo = construir_grafo(caso_asado, actor_loro, analista_fijo(["vio_al_perro"]))

    estado = grafo.invoke(_jugada_interrogar("michi", "¿Qué viste anoche?"), _config())

    assert estado["respuesta"] == "Yo no fui."  # la primera respuesta del actor falso
    assert estado["pistas_nuevas"] == ["vio_al_perro"]
    assert estado["pistas_descubiertas"] == ["vio_al_perro"]
    assert estado["preguntas_usadas"] == 1
    # El historial guarda el par pregunta/respuesta de este turno.
    assert len(estado["conversaciones"]["michi"]) == 2


def test_el_checkpointer_recuerda_la_partida_entre_turnos(caso_asado, actor_loro, analista_fijo):
    """Cada turno es un invoke() nuevo, pero con el mismo thread_id la partida sigue."""
    grafo = construir_grafo(caso_asado, actor_loro, analista_fijo([]))
    config = _config("partida-larga")

    grafo.invoke(_jugada_interrogar("michi", "¿Dónde estabas?"), config)
    estado = grafo.invoke(_jugada_interrogar("michi", "¿Y no viste nada?"), config)

    assert estado["preguntas_usadas"] == 2
    assert len(estado["conversaciones"]["michi"]) == 4  # dos pares pregunta/respuesta


def test_cada_sospechoso_tiene_su_propia_conversacion(caso_asado, actor_loro, analista_fijo):
    grafo = construir_grafo(caso_asado, actor_loro, analista_fijo([]))
    config = _config()

    grafo.invoke(_jugada_interrogar("michi", "¿Qué viste?"), config)
    estado = grafo.invoke(_jugada_interrogar("moro", "¿Fuiste vos?"), config)

    assert len(estado["conversaciones"]["michi"]) == 2
    assert len(estado["conversaciones"]["moro"]) == 2


def test_partidas_con_distinto_thread_id_no_se_mezclan(caso_asado, actor_loro, analista_fijo):
    grafo = construir_grafo(caso_asado, actor_loro, analista_fijo([]))

    grafo.invoke(_jugada_interrogar("michi", "¿Qué viste?"), _config("partida-a"))
    estado_b = grafo.invoke(_jugada_interrogar("moro", "¿Fuiste vos?"), _config("partida-b"))

    assert estado_b["preguntas_usadas"] == 1  # la partida B no heredó el turno de la A
    assert "michi" not in estado_b["conversaciones"]


def test_las_pistas_se_acumulan_sin_duplicarse(caso_asado, actor_loro, analista_fijo):
    """El analista insiste con la misma pista dos turnos seguidos: el estado
    la guarda una sola vez, y el segundo turno no la anuncia como nueva."""
    grafo = construir_grafo(caso_asado, actor_loro, analista_fijo(["vio_al_perro"]))
    config = _config()

    grafo.invoke(_jugada_interrogar("michi", "¿Qué viste?"), config)
    estado = grafo.invoke(_jugada_interrogar("michi", "¿Segura que eso viste?"), config)

    assert estado["pistas_descubiertas"] == ["vio_al_perro"]
    assert estado["pistas_nuevas"] == []


# ── La rama de la acusación ──────────────────────────────────────────────────


def test_acusar_al_culpable_gana_la_partida(caso_asado, actor_loro, analista_fijo):
    grafo = construir_grafo(caso_asado, actor_loro, analista_fijo([]))

    estado = grafo.invoke({"accion": "acusar", "sospechoso_actual": "moro"}, _config())

    assert estado["resultado"] == "victoria"


def test_acusar_a_un_inocente_pierde_la_partida(caso_asado, actor_loro, analista_fijo):
    grafo = construir_grafo(caso_asado, actor_loro, analista_fijo([]))

    estado = grafo.invoke({"accion": "acusar", "sospechoso_actual": "michi"}, _config())

    assert estado["resultado"] == "derrota"


def test_acusar_no_gasta_preguntas(caso_asado, actor_loro, analista_fijo):
    """La acusación va por la rama corta del grafo: no pasa por cerrar_turno."""
    grafo = construir_grafo(caso_asado, actor_loro, analista_fijo([]))
    config = _config()

    grafo.invoke(_jugada_interrogar("michi", "¿Qué viste?"), config)
    estado = grafo.invoke({"accion": "acusar", "sospechoso_actual": "moro"}, config)

    assert estado["preguntas_usadas"] == 1  # solo la pregunta, la acusación no cuenta
