"""Tests del servidor web, con los mismos fakes que el resto de la suite.

La gracia es la misma de siempre: como ``crear_app`` recibe caso, actor y
analista por parámetro, acá se prueba el protocolo COMPLETO — REST, WebSocket,
streaming, partidas guardadas — sin API key, sin red y sin browser. El
``TestClient`` de FastAPI habla HTTP y WebSocket contra la app en memoria.
"""

from contextlib import ExitStack

import pytest
from fastapi.testclient import TestClient
from langchain_core.language_models.fake_chat_models import FakeListChatModel
from starlette.websockets import WebSocketDisconnect

from caso_calafate.llm import MOTOR_FAKE
from caso_calafate.web import crear_app
from caso_calafate.web.servidor import MAX_PREGUNTA


@pytest.fixture
def crear_cliente(caso_asado, motores_fake):
    """Fábrica de clientes de prueba: cada test elige qué "detecta" el analista.

    El TestClient se usa como context manager para que dispare el lifespan de
    la app (ahí se abre la base SQLite en memoria); el ExitStack los cierra
    todos al final del test.
    """
    with ExitStack() as pila:

        def _crear(ids: list[str] | None = None) -> TestClient:
            app = crear_app({caso_asado.id: caso_asado}, motores_fake(ids))
            return pila.enter_context(TestClient(app))

        yield _crear


@pytest.fixture
def cliente(crear_cliente) -> TestClient:
    """Cliente estándar: el analista siempre cree ver la pista de Michi."""
    return crear_cliente(["vio_al_perro"])


def _nueva_partida(
    cliente: TestClient,
    nombre: str = "expediente de prueba",
    caso_id: str = "asado",
    modelo_id: str = MOTOR_FAKE,
) -> str:
    respuesta = cliente.post(
        "/api/partidas", json={"nombre": nombre, "caso_id": caso_id, "modelo_id": modelo_id}
    )
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


def test_el_selector_de_casos_no_spoilea(cliente, caso_asado):
    """/api/casos es la tarjeta del selector: ni briefing, ni sospechosos, ni
    nada que huela a spoiler — el browser es territorio enemigo."""
    respuesta = cliente.get("/api/casos")
    crudo = respuesta.text  # el JSON tal cual lo vería el jugador con F12

    assert respuesta.status_code == 200
    prohibidos = (
        '"es_culpable"',
        '"secretos"',
        '"instruccion_actor"',
        '"epilogo"',
        '"briefing"',
        '"sospechosos"',
        "Fue Moro",
    )
    for prohibido in prohibidos:
        assert prohibido not in crudo

    datos = respuesta.json()
    assert [c["id"] for c in datos["casos"]] == ["asado"]
    assert datos["casos"][0]["titulo"] == caso_asado.titulo
    assert datos["casos"][0]["gancho"] == caso_asado.gancho
    assert datos["casos"][0]["cantidad_sospechosos"] == 2
    assert datos["casos"][0]["max_preguntas"] == 5


def test_el_caso_embebido_en_la_partida_no_spoilea(cliente, caso_asado):
    """El detalle de una partida trae el caso COMPLETO (briefing, sospechosos)
    para que el frontend no necesite un fetch aparte — pero sigue sin
    culpables, secretos ni epílogo hasta que la partida cierra."""
    id_ = _nueva_partida(cliente)
    respuesta = cliente.get(f"/api/partidas/{id_}")
    crudo = respuesta.text

    assert respuesta.status_code == 200
    prohibidos = ('"es_culpable"', '"secretos"', '"instruccion_actor"', '"epilogo"', "Fue Moro")
    for prohibido in prohibidos:
        assert prohibido not in crudo

    caso = respuesta.json()["caso"]
    assert caso["id"] == "asado"
    assert caso["titulo"] == caso_asado.titulo
    assert caso["max_preguntas"] == 5
    assert caso["total_secretos"] == 2
    # El orden se baraja por partida, así que se compara el conjunto.
    assert {s["id"] for s in caso["sospechosos"]} == {"moro", "michi"}
    coartadas = {s["id"]: s["coartada"] for s in caso["sospechosos"]}
    assert coartadas["moro"] == "Dice que dormía en la cucha."


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
    assert partidas[0]["caso_id"] == "asado"
    assert partidas[0]["caso_titulo"] == "¿QUIÉN SE COMIÓ EL ASADO?"
    assert partidas[0]["preguntas_usadas"] == 0
    assert partidas[0]["preguntas_restantes"] == 5
    assert partidas[0]["resultado"] is None

    assert cliente.delete(f"/api/partidas/{id_}").status_code == 204
    assert cliente.get("/api/partidas").json() == []
    assert cliente.delete(f"/api/partidas/{id_}").status_code == 404


def test_las_partidas_necesitan_nombre(cliente):
    vacio = cliente.post(
        "/api/partidas", json={"nombre": "   ", "caso_id": "asado", "modelo_id": MOTOR_FAKE}
    )
    assert vacio.status_code == 422
    sin_nombre = {"caso_id": "asado", "modelo_id": MOTOR_FAKE}
    assert cliente.post("/api/partidas", json=sin_nombre).status_code == 422


def test_las_partidas_necesitan_un_caso_que_exista(cliente):
    respuesta = cliente.post(
        "/api/partidas", json={"nombre": "x", "caso_id": "no-existe", "modelo_id": MOTOR_FAKE}
    )
    assert respuesta.status_code == 422


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


# ── El arte pixel de la cámara ───────────────────────────────────────────────


def test_los_retratos_pixel_viajan_por_rest(cliente):
    """El arte es fijo del juego (los tres de Calafate): aunque esta app corra
    el caso del asado, el endpoint sirve el mismo paquete — para sospechosos
    sin retrato pixel el frontend cae al SVG, así que no rompe nada."""
    respuesta = cliente.get("/api/retratos")
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert set(datos) == {"paleta", "transparente", "ancho", "alto", "retratos"}
    assert set(datos["retratos"]) == {"marta", "julian", "silvia"}


# ── El vocabulario del caso viaja al frontend ────────────────────────────────


def test_el_detalle_trae_el_vocabulario_del_caso(cliente, caso_asado):
    """El briefing, la orden de acusación y el diario hablan del hecho REAL:
    para eso necesitan estos campos. No spoilean — describen el hecho, no al
    autor — pero igual el test de arriba vigila que nada más se cuele."""
    id_ = _nueva_partida(cliente)
    caso = cliente.get(f"/api/partidas/{id_}").json()["caso"]

    assert caso["sede"] == caso_asado.sede
    assert caso["ciudad"] == caso_asado.ciudad
    assert caso["delito"] == caso_asado.delito
    assert caso["culpable_alias"] == caso_asado.culpable_alias


def test_el_veredicto_no_habla_del_caso_calafate(cliente):
    """Regresión: la calificación decía «el CALAFATE-2 va a necesitar otro
    detective» en todos los casos."""
    id_ = _nueva_partida(cliente)
    with cliente.websocket_connect(f"/ws/partidas/{id_}") as ws:
        ws.send_json({"tipo": "acusar", "sospechoso": "michi"})
        veredicto = ws.receive_json()

    assert "CALAFATE" not in veredicto["calificacion"]
    assert "chorro de asados" in veredicto["calificacion"]  # el alias del caso de juguete
    assert "saboteador" not in veredicto["texto"]


# ── El socket no se cae con lo que le manden ─────────────────────────────────


@pytest.mark.parametrize(
    "payload", ['"hola"', "[1, 2, 3]", "null", "42", "no soy json", ""], ids=repr
)
def test_el_socket_contesta_error_ante_un_mensaje_ilegible(cliente, payload):
    """El browser es territorio del jugador: un mensaje roto tiene que
    devolver un error, no matar la conexión de la partida."""
    id_ = _nueva_partida(cliente)

    with cliente.websocket_connect(f"/ws/partidas/{id_}") as ws:
        ws.send_text(payload)
        mensaje = ws.receive_json()
        assert mensaje["tipo"] == "error"

        # Y la partida sigue jugable después del papelón.
        _, turno = _interrogar(ws, "michi", "¿Qué viste anoche?")
        assert turno["preguntas_usadas"] == 1


# ── Partidas huérfanas: su caso ya no está en el registro ────────────────────


@pytest.fixture
def partida_huerfana(tmp_path, caso_asado, motores_fake):
    """Crea una partida de un caso que después desaparece del registro.

    Pasa de verdad: alcanza con renombrar un caso o sacarlo de ``casos/``.
    Antes, una sola partida así tiraba abajo TODO el archivo (500 en
    /api/partidas) y ni siquiera se la podía borrar.
    """
    ruta = str(tmp_path / "partidas.sqlite")
    otro = caso_asado.model_copy(
        update={"id": "milanesa", "titulo": "¿QUIÉN SE COMIÓ LA MILANESA?"}
    )
    registro_completo = {caso_asado.id: caso_asado, otro.id: otro}

    with TestClient(crear_app(registro_completo, motores_fake(), ruta_db=ruta)) as c:
        id_ = _nueva_partida(c, "la milanesa", caso_id="milanesa")

    # La misma base, pero ahora el caso "milanesa" ya no existe.
    app = crear_app({caso_asado.id: caso_asado}, motores_fake(), ruta_db=ruta)
    with TestClient(app) as cliente_sin_el_caso:
        yield cliente_sin_el_caso, id_


def test_una_partida_huerfana_no_tumba_el_archivo(partida_huerfana):
    cliente, id_ = partida_huerfana
    respuesta = cliente.get("/api/partidas")

    assert respuesta.status_code == 200
    partidas = respuesta.json()
    assert [p["id"] for p in partidas] == [id_]
    assert partidas[0]["caso_disponible"] is False
    assert partidas[0]["caso_titulo"] == "— expediente ilegible —"


def test_una_partida_huerfana_no_se_puede_abrir_pero_avisa(partida_huerfana):
    cliente, id_ = partida_huerfana
    respuesta = cliente.get(f"/api/partidas/{id_}")

    assert respuesta.status_code == 410
    assert "milanesa" in respuesta.json()["detail"]


def test_el_socket_rechaza_una_partida_huerfana(partida_huerfana):
    cliente, id_ = partida_huerfana
    with pytest.raises(WebSocketDisconnect) as excinfo:
        with cliente.websocket_connect(f"/ws/partidas/{id_}"):
            pass
    assert excinfo.value.code == 4404


def test_una_partida_huerfana_se_puede_incinerar(partida_huerfana):
    """Lo importante: que el jugador pueda limpiar el archivo."""
    cliente, id_ = partida_huerfana
    assert cliente.delete(f"/api/partidas/{id_}").status_code == 204
    assert cliente.get("/api/partidas").json() == []


# ── El selector de motores ───────────────────────────────────────────────────


def test_el_catalogo_de_motores_viaja_con_el_motivo_de_los_que_no_estan(cliente):
    """El desplegable necesita saber qué NO se puede usar, y por qué.

    Acá la app se armó con un solo motor inyectado, así que el catálogo tiene
    exactamente ese: los tests no dependen de si hay ollama prendido ni de qué
    API keys tenga el entorno.
    """
    motores = cliente.get("/api/casos").json()["motores"]

    assert [m["id"] for m in motores] == [MOTOR_FAKE]
    assert motores[0]["disponible"] is True
    assert motores[0]["motivo"] is None
    assert motores[0]["etiqueta"]  # el jugador ve un nombre, no un id crudo


def test_las_partidas_necesitan_un_motor_disponible(cliente):
    """Elegir un motor que no está tiene que fallar en el alta y no a mitad
    del primer interrogatorio."""
    respuesta = cliente.post(
        "/api/partidas",
        json={"nombre": "x", "caso_id": "asado", "modelo_id": "groq:openai/gpt-oss-120b"},
    )
    assert respuesta.status_code == 422
    assert "no está disponible" in respuesta.json()["detail"]

    sin_motor = cliente.post("/api/partidas", json={"nombre": "x", "caso_id": "asado"})
    assert sin_motor.status_code == 422


def test_cada_partida_juega_con_su_propio_motor(caso_asado, actor_loro, analista_fijo):
    """Dos partidas, dos motores, dos voces: el grafo de una no pisa al de la otra.

    Es la prueba de que ``_grafo_de`` cachea por ``(caso, motor)`` y no solo
    por caso, que era el bug fácil de este refactor.
    """
    otro_actor = FakeListChatModel(responses=["Hablo distinto porque soy otro modelo."])
    motores = {
        MOTOR_FAKE: (actor_loro, analista_fijo([])),
        "otro": (otro_actor, analista_fijo([])),
    }

    with TestClient(crear_app({caso_asado.id: caso_asado}, motores)) as cliente:
        id_fake = _nueva_partida(cliente, "con el loro", modelo_id=MOTOR_FAKE)
        id_otro = _nueva_partida(cliente, "con el otro", modelo_id="otro")

        with cliente.websocket_connect(f"/ws/partidas/{id_fake}") as ws:
            _, turno_fake = _interrogar(ws, "michi", "¿dónde estabas?")
        with cliente.websocket_connect(f"/ws/partidas/{id_otro}") as ws:
            _, turno_otro = _interrogar(ws, "michi", "¿dónde estabas?")

    assert turno_fake["respuesta"] == "Yo no fui."
    assert turno_otro["respuesta"] == "Hablo distinto porque soy otro modelo."


def test_una_partida_con_el_motor_caido_se_lee_pero_no_se_juega(
    tmp_path, caso_asado, motores_fake
):
    """El gemelo del caso huérfano, pero del lado del motor.

    Apagaste ollama o sacaste una API key: el expediente tiene que seguir
    abriéndose (leer estado no invoca al LLM) y el socket tiene que decir qué
    le falta, en vez de tirar un 500.
    """
    ruta = str(tmp_path / "partidas.sqlite")
    motores_de_mas = {**motores_fake(), "ollama:qwen2.5:7b": motores_fake()[MOTOR_FAKE]}

    with TestClient(crear_app({caso_asado.id: caso_asado}, motores_de_mas, ruta_db=ruta)) as c:
        id_ = _nueva_partida(c, "con qwen", modelo_id="ollama:qwen2.5:7b")

    # La misma base, pero ahora ese motor ya no está disponible.
    with TestClient(crear_app({caso_asado.id: caso_asado}, motores_fake(), ruta_db=ruta)) as c:
        listado = c.get("/api/partidas").json()
        assert listado[0]["motor_disponible"] is False
        assert c.get(f"/api/partidas/{id_}").status_code == 200

        with pytest.raises(WebSocketDisconnect) as excinfo:
            with c.websocket_connect(f"/ws/partidas/{id_}") as ws:
                ws.receive_json()  # el error explicativo
                ws.receive_json()  # y recién ahí el cierre
        assert excinfo.value.code == 4409


@pytest.mark.anyio
async def test_una_base_vieja_se_migra_sin_perder_partidas(tmp_path):
    """Una base de antes del selector de motores no puede quedar ilegible.

    Se arma a mano la tabla como era (sin ``modelo_id``), se corre
    ``preparar()`` y la partida vieja tiene que seguir ahí, con el motor por
    defecto en vez de un NULL.
    """
    import aiosqlite

    from caso_calafate.llm import MOTOR_POR_DEFECTO
    from caso_calafate.web.partidas import RegistroPartidas

    ruta = str(tmp_path / "vieja.sqlite")
    conexion = await aiosqlite.connect(ruta)
    await conexion.execute(
        "CREATE TABLE partidas (id TEXT PRIMARY KEY, nombre TEXT NOT NULL, "
        "creada TEXT NOT NULL, tablero TEXT NOT NULL DEFAULT '{}', "
        "caso_id TEXT NOT NULL DEFAULT 'calafate')"
    )
    await conexion.execute(
        "INSERT INTO partidas (id, nombre, creada) VALUES ('vieja', 'de antes', '2026-01-01')"
    )
    await conexion.commit()

    registro = RegistroPartidas(conexion)
    await registro.preparar()

    partida = await registro.obtener("vieja")
    assert partida["nombre"] == "de antes"
    assert partida["caso_id"] == "calafate"
    assert partida["modelo_id"] == MOTOR_POR_DEFECTO
    await conexion.close()


def test_el_socket_rechaza_una_pregunta_gigante(cliente):
    """El `maxlength` del input es cosmético: por el socket entra lo que sea.

    Sin tope del lado del servidor, un pegado de 20.000 caracteres viajaba
    entero al LLM (plata y latencia sin techo en los motores de nube) y el
    socket se caía de keepalive esperando la respuesta.
    """
    id_ = _nueva_partida(cliente)

    with cliente.websocket_connect(f"/ws/partidas/{id_}") as ws:
        ws.send_json({"tipo": "interrogar", "sospechoso": "michi", "pregunta": "a" * 20_000})
        mensaje = ws.receive_json()
        assert mensaje["tipo"] == "error"
        assert str(MAX_PREGUNTA) in mensaje["mensaje"]

        # Una pregunta rechazada no gasta turno, y la partida sigue jugable.
        _, turno = _interrogar(ws, "michi", "¿Qué viste anoche?")
        assert turno["preguntas_usadas"] == 1


def test_una_pregunta_justo_en_el_tope_pasa(cliente):
    """El límite es inclusivo: 280 entra, 281 no."""
    id_ = _nueva_partida(cliente)

    with cliente.websocket_connect(f"/ws/partidas/{id_}") as ws:
        _, turno = _interrogar(ws, "michi", "¿" + "a" * (MAX_PREGUNTA - 2) + "?")
        assert turno["preguntas_usadas"] == 1

        larga = {"tipo": "interrogar", "sospechoso": "michi", "pregunta": "a" * (MAX_PREGUNTA + 1)}
        ws.send_json(larga)
        assert ws.receive_json()["tipo"] == "error"


def test_si_el_llm_explota_el_socket_avisa_y_sigue_vivo(caso_asado, analista_fijo):
    """Un LLM caído (timeout, 429, API key vencida) no puede tumbar la partida.

    El `except Exception` del interrogatorio avisa por el socket; lo que se
    prueba acá es que ese aviso llega y que la conexión aguanta para el
    siguiente intento.
    """

    class ActorRoto(FakeListChatModel):
        # Hay que romper los dos caminos: el servidor interroga con
        # ``astream``, que entra por ``_stream``, no por ``_call``.
        def _call(self, *args, **kwargs):
            raise RuntimeError("429 rate limit")

        def _stream(self, *args, **kwargs):
            raise RuntimeError("429 rate limit")

    motores = {MOTOR_FAKE: (ActorRoto(responses=["nunca llega"]), analista_fijo([]))}
    with TestClient(crear_app({caso_asado.id: caso_asado}, motores)) as cliente:
        id_ = _nueva_partida(cliente)
        with cliente.websocket_connect(f"/ws/partidas/{id_}") as ws:
            ws.send_json({"tipo": "interrogar", "sospechoso": "michi", "pregunta": "¿y?"})
            # Se corta en el primer mensaje terminal: si el fake no explotara,
            # llegaría un "turno" y el test falla en vez de colgarse esperando.
            while (m := ws.receive_json())["tipo"] in ("comienzo", "fragmento"):
                pass
            assert m["tipo"] == "error", f"esperaba un error, llegó {m['tipo']}"
            assert "429" in m["mensaje"]

            # El socket sigue abierto: una jugada mal formada se contesta igual.
            ws.send_json({"tipo": "bailar"})
            assert ws.receive_json()["tipo"] == "error"


def test_el_orden_de_los_sospechosos_es_estable_dentro_de_la_partida(cliente):
    """Se baraja por partida, no por request.

    El orden del archivo del caso delataba al culpable (casi nunca era el del
    medio), así que ahora cada partida tiene el suyo. Pero tiene que ser
    SIEMPRE el mismo dentro de una: si cambiara en cada request, las fichas
    del escritorio se reordenarían solas al recargar la página.
    """
    id_ = _nueva_partida(cliente)

    ordenes = {
        tuple(s["id"] for s in cliente.get(f"/api/partidas/{id_}").json()["caso"]["sospechosos"])
        for _ in range(4)
    }
    assert len(ordenes) == 1, f"el orden cambió entre requests: {ordenes}"
