"""Tests del servidor web, con los mismos fakes que el resto de la suite.

La gracia es la misma de siempre: como ``crear_app`` recibe caso, actor y
analista por parámetro, acá se prueba el protocolo COMPLETO — REST, WebSocket,
streaming, partidas guardadas — sin API key, sin red y sin browser. El
``TestClient`` de FastAPI habla HTTP y WebSocket contra la app en memoria.
"""

from contextlib import ExitStack

import pytest
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from caso_calafate.web import crear_app


@pytest.fixture
def crear_cliente(caso_asado, actor_loro, analista_fijo):
    """Fábrica de clientes de prueba: cada test elige qué "detecta" el analista.

    El TestClient se usa como context manager para que dispare el lifespan de
    la app (ahí se abre la base SQLite en memoria); el ExitStack los cierra
    todos al final del test.
    """
    with ExitStack() as pila:

        def _crear(ids: list[str] | None = None) -> TestClient:
            app = crear_app(caso_asado, actor_loro, analista_fijo(ids or []))
            return pila.enter_context(TestClient(app))

        yield _crear


@pytest.fixture
def cliente(crear_cliente) -> TestClient:
    """Cliente estándar: el analista siempre cree ver la pista de Michi."""
    return crear_cliente(["vio_al_perro"])


def _nueva_partida(cliente: TestClient, nombre: str = "expediente de prueba") -> str:
    respuesta = cliente.post("/api/partidas", json={"nombre": nombre})
    assert respuesta.status_code == 201
    return respuesta.json()["id"]


def _interrogar(ws, sospechoso: str, pregunta: str) -> tuple[str, dict]:
    """Juega un turno completo por el socket y devuelve (texto_streameado, turno)."""
    ws.send_json({"tipo": "interrogar", "sospechoso": sospechoso, "pregunta": pregunta})
    fragmentos: list[str] = []
    while True:
        mensaje = ws.receive_json()
        match mensaje["tipo"]:
            case "comienzo":
                continue
            case "fragmento":
                fragmentos.append(mensaje["texto"])
            case "turno":
                return "".join(fragmentos), mensaje
            case "error":
                raise AssertionError(f"jugada rechazada: {mensaje['mensaje']}")


# ── El contrato anti-spoiler ─────────────────────────────────────────────────


def test_el_caso_viaja_sin_spoilers(cliente, caso_asado):
    """Lo que devuelve /api/caso es exactamente lo que el jugador puede ver:
    nada de culpables, secretos ni epílogo — el browser es territorio enemigo."""
    respuesta = cliente.get("/api/caso")
    crudo = respuesta.text  # el JSON tal cual lo vería el jugador con F12

    assert respuesta.status_code == 200
    # Las claves van con comillas para buscar el CAMPO JSON exacto (el campo
    # legítimo "total_secretos" contiene el substring "secretos", por ejemplo).
    prohibidos = ('"es_culpable"', '"secretos"', '"instruccion_actor"', '"epilogo"', "Fue Moro")
    for prohibido in prohibidos:
        assert prohibido not in crudo

    datos = respuesta.json()
    assert datos["titulo"] == caso_asado.titulo
    assert datos["max_preguntas"] == 5
    assert datos["total_secretos"] == 2
    assert [s["id"] for s in datos["sospechosos"]] == ["moro", "michi"]
    assert datos["sospechosos"][0]["coartada"] == "Dice que dormía en la cucha."


def test_el_detalle_de_una_partida_abierta_tampoco_spoilea(cliente):
    id_ = _nueva_partida(cliente)
    respuesta = cliente.get(f"/api/partidas/{id_}")

    assert respuesta.status_code == 200
    assert "veredicto" not in respuesta.json()
    assert "Fue Moro" not in respuesta.text  # el epílogo no viaja hasta el cierre


# ── El archivo de casos (REST) ───────────────────────────────────────────────


def test_crear_listar_y_borrar_partidas(cliente):
    id_ = _nueva_partida(cliente, "caso del asado frío")

    partidas = cliente.get("/api/partidas").json()
    assert len(partidas) == 1
    assert partidas[0]["nombre"] == "caso del asado frío"
    assert partidas[0]["preguntas_usadas"] == 0
    assert partidas[0]["preguntas_restantes"] == 5
    assert partidas[0]["resultado"] is None

    assert cliente.delete(f"/api/partidas/{id_}").status_code == 204
    assert cliente.get("/api/partidas").json() == []
    assert cliente.delete(f"/api/partidas/{id_}").status_code == 404


def test_las_partidas_necesitan_nombre(cliente):
    assert cliente.post("/api/partidas", json={"nombre": "   "}).status_code == 422
    assert cliente.post("/api/partidas", json={}).status_code == 422


# ── Las jugadas (WebSocket) ──────────────────────────────────────────────────


def test_interrogar_streamea_y_cierra_el_turno(cliente):
    id_ = _nueva_partida(cliente)

    with cliente.websocket_connect(f"/ws/partidas/{id_}") as ws:
        texto, turno = _interrogar(ws, "michi", "¿Qué viste anoche?")

    # La respuesta completa viaja en el mensaje final aunque ya haya salido
    # por fragmentos: el streaming es mejora progresiva, no fuente de verdad.
    assert turno["respuesta"] == "Yo no fui."
    assert texto == turno["respuesta"]
    assert turno["preguntas_usadas"] == 1
    assert turno["preguntas_restantes"] == 4
    assert turno["pistas_nuevas"] == [
        {"id": "vio_al_perro", "pista": "Michi vio a Moro rondando la mesa antes de la siesta."}
    ]


def test_acusar_cierra_la_partida_y_recien_ahi_viaja_el_epilogo(cliente, caso_asado):
    id_ = _nueva_partida(cliente)

    with cliente.websocket_connect(f"/ws/partidas/{id_}") as ws:
        ws.send_json({"tipo": "acusar", "sospechoso": "moro"})
        veredicto = ws.receive_json()

        assert veredicto["tipo"] == "veredicto"
        assert veredicto["resultado"] == "victoria"
        assert veredicto["acusado"] == "moro"
        assert veredicto["epilogo"] == caso_asado.epilogo
        assert "instinto" in veredicto["calificacion"]  # ganó sin ninguna pista

        # Con el caso cerrado, no se puede seguir interrogando.
        ws.send_json({"tipo": "interrogar", "sospechoso": "michi", "pregunta": "¿y ahora?"})
        rechazo = ws.receive_json()
        assert rechazo["tipo"] == "error"
        assert "cerrado" in rechazo["mensaje"]

    detalle = cliente.get(f"/api/partidas/{id_}").json()
    assert detalle["resultado"] == "victoria"
    assert detalle["veredicto"]["epilogo"] == caso_asado.epilogo


def test_acusar_a_un_inocente_tambien_cierra(cliente):
    id_ = _nueva_partida(cliente)

    with cliente.websocket_connect(f"/ws/partidas/{id_}") as ws:
        ws.send_json({"tipo": "acusar", "sospechoso": "michi"})
        veredicto = ws.receive_json()

    assert veredicto["resultado"] == "derrota"
    assert "suelto" in veredicto["calificacion"]


def test_jugadas_invalidas_devuelven_error(cliente):
    id_ = _nueva_partida(cliente)

    with cliente.websocket_connect(f"/ws/partidas/{id_}") as ws:
        casos = [
            ({"tipo": "interrogar", "sospechoso": "nadie", "pregunta": "hola"}, "sospechoso"),
            ({"tipo": "interrogar", "sospechoso": "michi", "pregunta": "   "}, "vacía"),
            ({"tipo": "bailar"}, "bailar"),
        ]
        for jugada, palabra in casos:
            ws.send_json(jugada)
            mensaje = ws.receive_json()
            assert mensaje["tipo"] == "error"
            assert palabra in mensaje["mensaje"]


def test_sin_preguntas_restantes_solo_queda_acusar(cliente):
    id_ = _nueva_partida(cliente)

    with cliente.websocket_connect(f"/ws/partidas/{id_}") as ws:
        for numero in range(5):  # el caso de juguete da 5 preguntas
            _interrogar(ws, "michi", f"pregunta {numero}")

        ws.send_json({"tipo": "interrogar", "sospechoso": "michi", "pregunta": "¿una más?"})
        mensaje = ws.receive_json()
        assert mensaje["tipo"] == "error"
        assert "acusar" in mensaje["mensaje"]


def test_el_socket_rechaza_partidas_inexistentes(cliente):
    with pytest.raises(WebSocketDisconnect) as excinfo:
        with cliente.websocket_connect("/ws/partidas/no-existe"):
            pass
    assert excinfo.value.code == 4404


# ── Retomar partidas: el checkpointer visto desde la web ─────────────────────


def test_el_detalle_trae_todo_para_retomar_la_partida(cliente):
    id_ = _nueva_partida(cliente)

    with cliente.websocket_connect(f"/ws/partidas/{id_}") as ws:
        _interrogar(ws, "michi", "¿Qué viste?")
        _interrogar(ws, "moro", "¿Fuiste vos?")

    detalle = cliente.get(f"/api/partidas/{id_}").json()
    assert detalle["preguntas_usadas"] == 2
    assert detalle["ultimo_sospechoso"] == "moro"
    assert [p["id"] for p in detalle["pistas"]] == ["vio_al_perro"]

    charla = detalle["conversaciones"]["michi"]
    assert [m["quien"] for m in charla] == ["detective", "sospechoso"]
    assert charla[0]["texto"] == "¿Qué viste?"
    assert charla[1]["texto"] == "Yo no fui."


def test_partidas_paralelas_no_se_mezclan(cliente):
    id_a = _nueva_partida(cliente, "partida a")
    id_b = _nueva_partida(cliente, "partida b")

    with cliente.websocket_connect(f"/ws/partidas/{id_a}") as ws:
        _interrogar(ws, "michi", "¿Qué viste?")

    detalle_b = cliente.get(f"/api/partidas/{id_b}").json()
    assert detalle_b["preguntas_usadas"] == 0
    assert detalle_b["conversaciones"] == {}


# ── El tablero de evidencias ─────────────────────────────────────────────────


def test_el_tablero_se_guarda_y_se_recupera(cliente):
    id_ = _nueva_partida(cliente)
    tablero = {
        "notas": {"vio_al_perro": {"x": 12.5, "y": 40.0}},
        "fotos": {"moro": {"x": 80.0, "y": 15.0}},
        "conexiones": [["vio_al_perro", "moro"]],
    }

    assert cliente.put(f"/api/partidas/{id_}/tablero", json=tablero).status_code == 204
    assert cliente.get(f"/api/partidas/{id_}").json()["tablero"] == tablero

    assert cliente.put("/api/partidas/no-existe/tablero", json=tablero).status_code == 404


def test_el_tablero_malformado_se_rechaza(cliente):
    id_ = _nueva_partida(cliente)
    respuesta = cliente.put(
        f"/api/partidas/{id_}/tablero",
        json={"notas": {"x": "no soy una posición"}},
    )
    assert respuesta.status_code == 422
