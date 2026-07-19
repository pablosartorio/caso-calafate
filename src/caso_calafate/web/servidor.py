"""El servidor web del juego: el mismo grafo que el CLI, servido por HTTP.

Este módulo es el gemelo de ``cli.py``: otra "piel" sobre el mismo motor.
La división de responsabilidades calca la de la terminal:

- Los comandos informativos del CLI (``/caso``, ``/pistas``, ``/sospechosos``)
  acá son endpoints **REST**: leen estado con ``aget_state()``, no invocan
  el grafo.
- Las jugadas (``interrogar`` / ``acusar``) van por **WebSocket**: son las
  únicas que invocan el grafo, y el socket permite streamear cada token de la
  respuesta del sospechoso al browser, como hace la terminal con
  ``stream_mode="messages"``.

Dos decisiones de diseño para mirar de cerca:

1. **DTOs anti-spoiler.** El browser es territorio del jugador: cualquier
   respuesta HTTP se puede inspeccionar con F12. Por eso los modelos de salida
   (``SospechosoDTO``, ``CasoDTO``) declaran EXPLÍCITAMENTE qué campos viajan
   — y ``es_culpable``, los secretos y el epílogo no están. El epílogo recién
   sale del servidor cuando la partida termina.

2. **Inyección de dependencias, otra vez.** ``crear_app()`` recibe el registro
   de casos, actor y analista igual que ``construir_grafo()``. Los tests le
   enchufan modelos falsos y una base en memoria, y prueban TODO el protocolo
   web sin API key (ver ``tests/test_web.py``).

3. **Multi-caso.** El servidor sirve TODOS los casos del registro a la vez
   (un grafo por caso, ver el ``lifespan``); cada partida elige su caso al
   crearse (``NuevaPartida.caso_id``) y queda atada a él para siempre.
"""

import os
from contextlib import asynccontextmanager
from pathlib import Path

import aiosqlite
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langchain_core.runnables import Runnable
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from pydantic import BaseModel, Field

from caso_calafate.caso import Caso
from caso_calafate.casos import CASOS
from caso_calafate.grafo import construir_grafo
from caso_calafate.llm import crear_motores, texto_de
from caso_calafate.fondo import exportar_fondo
from caso_calafate.pixelart import exportar_retratos
from caso_calafate.web.partidas import RegistroPartidas

ESTATICO = Path(__file__).parent / "estatico"


# ── DTOs: el contrato con el browser ─────────────────────────────────────────
# FastAPI usa estos modelos para FILTRAR la respuesta: aunque el handler
# devuelva un objeto con más campos, al browser solo llega lo declarado acá.


class SospechosoDTO(BaseModel):
    """Lo que el jugador puede saber de un sospechoso. Ni un campo más."""

    id: str
    nombre: str
    cargo: str
    coartada: str
    color: str


class CasoDTO(BaseModel):
    id: str
    titulo: str
    briefing: str
    max_preguntas: int
    total_secretos: int
    motor: str  # para que el frontend avise si se juega en modo fake
    sospechosos: list[SospechosoDTO]


class CasoResumenDTO(BaseModel):
    """La tarjeta del selector de casos: sin briefing ni sospechosos — nada
    que spoilee antes de aceptar el caso."""

    id: str
    titulo: str
    gancho: str
    cantidad_sospechosos: int
    max_preguntas: int


class CasosDTO(BaseModel):
    motor: str  # para que el frontend avise si se juega en modo fake
    casos: list[CasoResumenDTO]


class NuevaPartida(BaseModel):
    nombre: str = Field(min_length=1, max_length=60)
    caso_id: str


class Posicion(BaseModel):
    x: float
    y: float


class TableroDTO(BaseModel):
    """El estado visual del corcho: dónde quedó cada nota y qué une cada hilo.

    Es cosmética pura del frontend — el servidor lo guarda y lo devuelve sin
    interpretarlo — pero tiparlo evita que un PUT malformado ensucie la base.
    """

    notas: dict[str, Posicion] = {}
    fotos: dict[str, Posicion] = {}
    conexiones: list[tuple[str, str]] = []


# ── La app ───────────────────────────────────────────────────────────────────


def crear_app(
    casos: dict[str, Caso],
    actor: BaseChatModel,
    analista: Runnable,
    ruta_db: str = ":memory:",
    motor: str = "",
) -> FastAPI:
    """Arma la aplicación FastAPI con un grafo por caso, el registro y las rutas.

    ``casos`` es el registro completo (id → Caso, ver ``caso_calafate.casos``):
    cada partida elige SU caso al crearse y queda atada a él para siempre — el
    servidor sirve todos los casos a la vez, no uno solo.

    ``ruta_db`` apunta al archivo SQLite que comparte el checkpointer de los
    grafos y el registro de partidas; ``:memory:`` (el default, pensado para
    tests) dura lo que dura el proceso.
    """

    @asynccontextmanager
    async def vida(app: FastAPI):
        # La conexión se abre acá (contexto async) y no en import-time: el
        # lifespan de FastAPI es el lugar para recursos con apertura y cierre.
        conexion = await aiosqlite.connect(ruta_db)
        app.state.registro = RegistroPartidas(conexion)
        await app.state.registro.preparar()
        checkpointer = AsyncSqliteSaver(conexion)
        # Un grafo por caso, mismo checkpointer: cada partida solo invoca el
        # grafo de SU caso_id, así que no hay cruce de estado entre casos.
        app.state.grafos = {
            id_: construir_grafo(c, actor, analista, checkpointer=checkpointer)
            for id_, c in casos.items()
        }
        yield
        await conexion.close()

    app = FastAPI(title="El Caso Calafate", lifespan=vida)

    def _config(partida_id: str) -> dict:
        """El thread_id del checkpointer ES el id de la partida: mismo truco
        que el CLI, pero ahora con una partida por expediente en vez de una
        por proceso."""
        return {"configurable": {"thread_id": partida_id}}

    async def _estado_de(partida_id: str, caso_id: str) -> dict:
        return (await app.state.grafos[caso_id].aget_state(_config(partida_id))).values

    def _caso_dto(caso: Caso) -> CasoDTO:
        return CasoDTO(
            id=caso.id,
            titulo=caso.titulo,
            briefing=caso.briefing,
            max_preguntas=caso.max_preguntas,
            total_secretos=caso.total_secretos(),
            motor=motor,
            sospechosos=[SospechosoDTO(**s.model_dump()) for s in caso.sospechosos],
        )

    # ── REST: lo informativo (nada de esto invoca el grafo) ─────────────────

    @app.get("/api/casos")
    def api_casos() -> CasosDTO:
        """El selector de casos: título y gancho de cada uno, sin spoilers
        (nada de briefing completo, sospechosos ni epílogo todavía)."""
        return CasosDTO(
            motor=motor,
            casos=[
                CasoResumenDTO(
                    id=c.id,
                    titulo=c.titulo,
                    gancho=c.gancho,
                    cantidad_sospechosos=len(c.sospechosos),
                    max_preguntas=c.max_preguntas,
                )
                for c in casos.values()
            ],
        )

    @app.get("/api/retratos")
    def api_retratos() -> dict:
        """El arte pixel de la cámara del CRT: paleta DB32 + capas, como texto.

        Acá no hay nada que filtrar — el arte es cosmética pública — así que
        viaja tal cual sale de ``pixelart.exportar_retratos()``."""
        return exportar_retratos()

    @app.get("/api/fondo")
    def api_fondo() -> dict:
        """El fondo de escena del archivo de expedientes, como texto (ver
        ``fondo.py``). Misma cosmética pública que ``/api/retratos``: nada
        que filtrar."""
        return exportar_fondo()

    @app.get("/api/partidas")
    async def api_partidas(request: Request) -> list[dict]:
        """El archivo de casos: cada partida con un resumen de su estado."""
        partidas = await request.app.state.registro.listar()
        resultado = []
        for p in partidas:
            caso = casos[p["caso_id"]]
            estado = await _estado_de(p["id"], p["caso_id"])
            resultado.append({**p, "caso_titulo": caso.titulo, **_resumen(estado, caso)})
        return resultado

    @app.post("/api/partidas", status_code=201)
    async def api_crear_partida(datos: NuevaPartida, request: Request) -> dict:
        nombre = datos.nombre.strip()
        if not nombre:
            raise HTTPException(422, "la partida necesita un nombre")
        if datos.caso_id not in casos:
            raise HTTPException(422, f"no existe el caso {datos.caso_id!r}")
        return await request.app.state.registro.crear(nombre, datos.caso_id)

    @app.delete("/api/partidas/{partida_id}", status_code=204)
    async def api_borrar_partida(partida_id: str, request: Request) -> None:
        partida = await request.app.state.registro.obtener(partida_id)
        if partida is None:
            raise HTTPException(404, "no existe esa partida")
        await request.app.state.registro.borrar(partida_id)
        # El registro borró los metadatos; los checkpoints los borra el grafo
        # de SU caso (cada caso tiene el suyo, ver el lifespan).
        await app.state.grafos[partida["caso_id"]].checkpointer.adelete_thread(partida_id)

    @app.get("/api/partidas/{partida_id}")
    async def api_detalle_partida(partida_id: str, request: Request) -> dict:
        """Todo lo que el frontend necesita para retomar una partida:
        el caso completo, el resumen, la libreta, las conversaciones y el
        tablero."""
        partida = await request.app.state.registro.obtener(partida_id)
        if partida is None:
            raise HTTPException(404, "no existe esa partida")

        caso = casos[partida["caso_id"]]
        estado = await _estado_de(partida_id, partida["caso_id"])
        detalle = {
            **partida,
            "caso": _caso_dto(caso),
            **_resumen(estado, caso),
            "pistas": _pistas_descubiertas(estado, caso),
            "conversaciones": _serializar_conversaciones(estado.get("conversaciones", {})),
            "ultimo_sospechoso": estado.get("sospechoso_actual"),
        }
        if estado.get("resultado"):
            # Recién acá — con la partida cerrada — el epílogo cruza el cable.
            detalle["veredicto"] = _veredicto(estado, caso)
        return detalle

    @app.put("/api/partidas/{partida_id}/tablero", status_code=204)
    async def api_guardar_tablero(
        partida_id: str, tablero: TableroDTO, request: Request
    ) -> None:
        guardado = await request.app.state.registro.guardar_tablero(
            partida_id, tablero.model_dump()
        )
        if not guardado:
            raise HTTPException(404, "no existe esa partida")

    # ── WebSocket: las jugadas (lo único que invoca el grafo) ───────────────

    @app.websocket("/ws/partidas/{partida_id}")
    async def ws_partida(websocket: WebSocket, partida_id: str) -> None:
        """Un socket por partida abierta en el browser.

        Protocolo (JSON por mensaje):

          cliente → ``{"tipo": "interrogar", "sospechoso": id, "pregunta": str}``
                    ``{"tipo": "acusar", "sospechoso": id}``
          servidor → ``comienzo`` · ``fragmento``* · ``turno``   (interrogar)
                     ``veredicto``                               (acusar)
                     ``error``                                   (jugada inválida)

        El turno completo viaja al final en ``turno.respuesta`` aunque ya haya
        salido por fragmentos: el streaming es mejora progresiva, no la fuente
        de verdad — si un modelo no streamea, el juego funciona igual.
        """
        partida = await websocket.app.state.registro.obtener(partida_id)
        if partida is None:
            # 4404: código de aplicación (la franja 4000-4999 es libre en WS).
            await websocket.close(code=4404)
            return
        await websocket.accept()
        caso_id = partida["caso_id"]

        try:
            while True:
                jugada = await websocket.receive_json()
                match jugada.get("tipo"):
                    case "interrogar":
                        await _jugada_interrogar(websocket, partida_id, caso_id, jugada)
                    case "acusar":
                        await _jugada_acusar(websocket, partida_id, caso_id, jugada)
                    case desconocido:
                        await _error(websocket, f"no conozco la jugada {desconocido!r}")
        except WebSocketDisconnect:
            pass  # el jugador cerró la pestaña; la partida queda en la base

    async def _jugada_interrogar(
        websocket: WebSocket, partida_id: str, caso_id: str, jugada: dict
    ) -> None:
        caso = casos[caso_id]
        grafo = app.state.grafos[caso_id]
        estado = await _estado_de(partida_id, caso_id)
        sospechoso = caso.buscar_sospechoso(jugada.get("sospechoso", ""))
        pregunta = (jugada.get("pregunta") or "").strip()

        if estado.get("resultado"):
            return await _error(websocket, "el caso ya está cerrado")
        if caso.max_preguntas - estado.get("preguntas_usadas", 0) <= 0:
            return await _error(websocket, "no quedan preguntas: es hora de acusar")
        if sospechoso is None:
            return await _error(websocket, "no conozco a ese sospechoso")
        if not pregunta:
            return await _error(websocket, "la pregunta está vacía")

        await websocket.send_json({"tipo": "comienzo", "sospechoso": sospechoso.id})

        entrada = {
            "accion": "interrogar",
            "sospechoso_actual": sospechoso.id,
            "pregunta": pregunta,
        }
        try:
            # El mismo stream_mode="messages" del CLI: cada token que genera
            # cualquier LLM interno llega con metadata de QUÉ nodo lo produjo.
            # Filtramos "interrogar" para transmitir solo la voz del sospechoso
            # (el analista trabaja en silencio).
            async for pedazo, metadata in grafo.astream(
                entrada, _config(partida_id), stream_mode="messages"
            ):
                if metadata.get("langgraph_node") == "interrogar":
                    texto = texto_de(pedazo)
                    if texto:
                        await websocket.send_json({"tipo": "fragmento", "texto": texto})
        except WebSocketDisconnect:
            raise
        except Exception as error:  # LLM caído, timeout, etc.: el juego avisa y sigue
            return await _error(websocket, f"el interrogatorio se cortó: {error}")

        estado = await _estado_de(partida_id, caso_id)
        await websocket.send_json(
            {
                "tipo": "turno",
                "sospechoso": sospechoso.id,
                "respuesta": estado.get("respuesta", ""),
                "pistas_nuevas": [
                    {"id": s.id, "pista": s.pista}
                    for id_ in estado.get("pistas_nuevas", [])
                    if (s := caso.secreto(id_)) is not None
                ],
                **_resumen(estado, caso),
            }
        )

    async def _jugada_acusar(
        websocket: WebSocket, partida_id: str, caso_id: str, jugada: dict
    ) -> None:
        caso = casos[caso_id]
        grafo = app.state.grafos[caso_id]
        estado = await _estado_de(partida_id, caso_id)
        sospechoso = caso.buscar_sospechoso(jugada.get("sospechoso", ""))

        if estado.get("resultado"):
            return await _error(websocket, "el caso ya está cerrado")
        if sospechoso is None:
            return await _error(websocket, "no conozco a ese sospechoso")

        # La acusación no streamea (es la rama corta y determinista del
        # grafo), así que alcanza con un ainvoke.
        estado = await grafo.ainvoke(
            {"accion": "acusar", "sospechoso_actual": sospechoso.id},
            _config(partida_id),
        )
        await websocket.send_json({"tipo": "veredicto", **_veredicto(estado, caso)})

    async def _error(websocket: WebSocket, mensaje: str) -> None:
        await websocket.send_json({"tipo": "error", "mensaje": mensaje})

    # ── Traducciones estado → JSON (compartidas por REST y WebSocket) ────────

    def _resumen(estado: dict, caso: Caso) -> dict:
        usadas = estado.get("preguntas_usadas", 0)
        return {
            "preguntas_usadas": usadas,
            "preguntas_restantes": caso.max_preguntas - usadas,
            "pistas_descubiertas": len(estado.get("pistas_descubiertas", [])),
            "total_secretos": caso.total_secretos(),
            "resultado": estado.get("resultado"),
        }

    def _pistas_descubiertas(estado: dict, caso: Caso) -> list[dict]:
        return [
            {"id": s.id, "pista": s.pista}
            for id_ in estado.get("pistas_descubiertas", [])
            if (s := caso.secreto(id_)) is not None
        ]

    def _serializar_conversaciones(conversaciones: dict) -> dict:
        """De mensajes de LangChain a JSON neutro: el browser no tiene por qué
        saber qué es un HumanMessage."""
        return {
            sospechoso_id: [
                {
                    "quien": "detective" if isinstance(m, HumanMessage) else "sospechoso",
                    "texto": texto_de(m),
                }
                for m in mensajes
            ]
            for sospechoso_id, mensajes in conversaciones.items()
        }

    def _veredicto(estado: dict, caso: Caso) -> dict:
        encontradas = len(estado.get("pistas_descubiertas", []))
        return {
            "resultado": estado["resultado"],
            "texto": estado.get("respuesta", ""),
            "acusado": estado.get("sospechoso_actual"),
            "epilogo": caso.epilogo,
            "calificacion": _calificacion(estado["resultado"], encontradas, caso.total_secretos()),
            "pistas_descubiertas": encontradas,
            "total_secretos": caso.total_secretos(),
            "preguntas_usadas": estado.get("preguntas_usadas", 0),
        }

    # El frontend: archivos estáticos servidos por el mismo proceso. Montado
    # al final para que /api y /ws (declarados antes) tengan prioridad.
    app.mount("/", StaticFiles(directory=ESTATICO, html=True), name="estatico")

    return app


def _calificacion(resultado: str, encontradas: int, total: int) -> str:
    """El remate según cómo se jugó — gemelo en texto plano del que muestra
    el CLI con markup de rich (``cli._calificacion``)."""
    if resultado != "victoria":
        return "🪦 El culpable sigue suelto. El CALAFATE-2 va a necesitar otro detective."
    if encontradas >= total * 0.8:
        return "🏆 Detective de leyenda: resolviste el caso con la evidencia en la mano."
    if encontradas >= total * 0.4:
        return "🕵️ Buen ojo, detective. Un par de pistas más y era de manual."
    return "🍀 Acertaste... con más instinto que evidencia. La suerte también cuenta."


# ── Punto de entrada del comando ``detective-web`` ───────────────────────────


def main() -> None:
    """Levanta el servidor con el caso real y el motor del ``.env``."""
    load_dotenv()

    try:
        actor, analista, nombre_motor = crear_motores()
    except Exception as error:  # API key ausente, proveedor mal escrito, etc.
        print(f"No pude inicializar el modelo de lenguaje: {error}")
        print("Revisá tu .env — las opciones de DETECTIVE_MODEL están en el README.")
        return

    ruta_db = os.environ.get("DETECTIVE_DB", "partidas.sqlite")
    puerto = int(os.environ.get("DETECTIVE_WEB_PORT", "8765"))
    app = crear_app(CASOS, actor, analista, ruta_db=ruta_db, motor=nombre_motor)

    print(f"🛰️  El Caso Calafate — http://127.0.0.1:{puerto}")
    print(f"    motor: {nombre_motor} · partidas en {ruta_db} · {len(CASOS)} casos disponibles")
    if nombre_motor == "fake":
        print("    ⚠ modo fake: respuestas enlatadas, pistas que se revelan solas")
    uvicorn.run(app, host="127.0.0.1", port=puerto, log_level="warning")
