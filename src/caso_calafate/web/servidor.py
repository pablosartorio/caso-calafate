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
   de casos y el de motores igual que ``construir_grafo()`` recibe los suyos.
   Los tests le enchufan modelos falsos y una base en memoria, y prueban TODO
   el protocolo web sin API key (ver ``tests/test_web.py``).

3. **Multi-caso y multi-motor.** El servidor sirve TODOS los casos y todos los
   modelos usables a la vez; cada partida elige los suyos al crearse
   (``NuevaPartida.caso_id`` y ``modelo_id``) y queda atada a ellos para
   siempre. Los grafos se compilan por par ``(caso, motor)`` al primer uso
   (ver ``_grafo_de``).
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
from caso_calafate.llm import (
    MOTOR_FAKE,
    MOTORES,
    crear_motores,
    motor_sugerido,
    relevar_motores,
    texto_de,
)
from caso_calafate.pixelart import exportar_retratos
from caso_calafate.web.partidas import RegistroPartidas

ESTATICO = Path(__file__).parent / "estatico"

# El tope de una pregunta, en caracteres. El mismo número está en el
# ``maxlength`` del input (``estatico/index.html``), pero ese es cosmético: el
# browser es territorio del jugador y por el socket entra lo que quiera. Sin
# este chequeo, un pegado de 20.000 caracteres viaja entero al LLM — plata y
# latencia sin techo en los motores de nube, y el socket se cae de keepalive
# esperando la respuesta.
MAX_PREGUNTA = 280


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
    motor: str  # el motor de ESTA partida, no el del servidor
    sospechosos: list[SospechosoDTO]
    # El vocabulario del caso: con esto el briefing, la orden de acusación y
    # el diario hablan del hecho REAL en vez de repetir el del caso original.
    # Describe el hecho, nunca a su autor, así que no spoilea nada.
    sede: str
    ciudad: str
    delito: str
    culpable_alias: str


class CasoResumenDTO(BaseModel):
    """La tarjeta del selector de casos: sin briefing ni sospechosos — nada
    que spoilee antes de aceptar el caso."""

    id: str
    titulo: str
    gancho: str
    cantidad_sospechosos: int
    max_preguntas: int


class MotorDTO(BaseModel):
    """Una opción del selector de motores, con su estado real.

    ``motivo`` es la mitad útil: un motor que no se puede usar se muestra
    igual, deshabilitado y diciendo QUÉ le falta (prender ollama, bajar el
    modelo, poner una API key). Esconderlo dejaría al jugador sin saber que
    existe ni cómo habilitarlo.
    """

    id: str
    etiqueta: str
    detalle: str
    disponible: bool
    motivo: str | None = None


class CasosDTO(BaseModel):
    casos: list[CasoResumenDTO]
    motores: list[MotorDTO]
    motor_sugerido: str


class NuevaPartida(BaseModel):
    nombre: str = Field(min_length=1, max_length=60)
    caso_id: str
    modelo_id: str


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
    motores: dict[str, tuple[BaseChatModel, Runnable]] | None = None,
    *,
    ruta_db: str = ":memory:",
) -> FastAPI:
    """Arma la aplicación FastAPI con el registro, los motores y las rutas.

    ``casos`` es el registro completo (id → Caso, ver ``caso_calafate.casos``):
    cada partida elige SU caso al crearse y queda atada a él para siempre — el
    servidor sirve todos los casos a la vez, no uno solo.

    ``motores`` es el registro paralelo de modelos (id → actor, analista) y
    funciona igual: cada partida elige el suyo al crearse. Si es ``None`` (el
    caso real), el ``lifespan`` releva qué motores se pueden usar y los
    instancia solo a esos. Los tests le pasan uno falso y se saltan el
    relevamiento entero — misma inyección de dependencias que ``casos``.

    ``ruta_db`` apunta al archivo SQLite que comparte el checkpointer de los
    grafos y el registro de partidas; ``:memory:`` (el default, pensado para
    tests) dura lo que dura el proceso. Va como keyword-only a propósito: un
    tercer argumento posicional de más terminaba siendo la ruta de la base, y
    SQLite creaba tan campante un archivo con el ``repr`` del objeto en el
    nombre en vez de fallar.
    """

    @asynccontextmanager
    async def vida(app: FastAPI):
        # La conexión se abre acá (contexto async) y no en import-time: el
        # lifespan de FastAPI es el lugar para recursos con apertura y cierre.
        conexion = await aiosqlite.connect(ruta_db)
        app.state.registro = RegistroPartidas(conexion)
        await app.state.registro.preparar()
        checkpointer = AsyncSqliteSaver(conexion)
        # AsyncSqliteSaver crea sus tablas de forma perezosa, en la primera
        # lectura o escritura de estado. Acá se las pide de una: si no,
        # ``adelete_thread`` (que NO llama a setup) explota con "no such table"
        # en una base donde todavía nadie jugó un turno.
        await checkpointer.setup()
        # El checkpointer aparte: los checkpoints se indexan por thread_id, no
        # por caso, así que para borrarlos no hace falta saber de qué caso era
        # la partida (importa para las partidas huérfanas, ver _caso_de).
        app.state.checkpointer = checkpointer
        app.state.motores, app.state.motivos = await _preparar_motores()
        # Un grafo por (caso, motor), compilado al primer uso y no acá: con 11
        # casos y 8 motores el producto cartesiano son 88 grafos que casi
        # nadie va a jugar. Compilar es barato pero no gratis, y la mayoría
        # sería basura. El checkpointer es el mismo para todos: los
        # checkpoints se indexan por thread_id (= id de partida), así que
        # tampoco acá hay cruce de estado.
        app.state.grafos = {}
        yield
        await conexion.close()

    async def _preparar_motores() -> tuple[dict, dict]:
        """Los motores usables y el motivo de los que no, al arrancar.

        Un motor que no arranca NO tumba el servidor: se anota el motivo y el
        selector lo muestra deshabilitado. Que falte una API key no puede
        impedirte jugar en local.
        """
        if motores is not None:  # inyectados (tests): no hay nada que relevar
            return dict(motores), dict.fromkeys(motores, None)

        motivos = await relevar_motores()
        listos = {}
        for id_, motivo in motivos.items():
            if motivo is not None:
                continue
            try:
                actor, analista, _ = crear_motores(id_)
            except Exception as error:  # paquete faltante, key inválida, etc.
                motivos[id_] = f"no pude inicializarlo: {error}"
                continue
            listos[id_] = (actor, analista)
        return listos, motivos

    app = FastAPI(title="El Caso Calafate", lifespan=vida)

    def _config(partida_id: str) -> dict:
        """El thread_id del checkpointer ES el id de la partida: mismo truco
        que el CLI, pero ahora con una partida por expediente en vez de una
        por proceso."""
        return {"configurable": {"thread_id": partida_id}}

    def _grafo_de(caso_id: str, modelo_id: str):
        """El grafo de esta partida, compilado la primera vez que se pide.

        Si el motor con el que se creó la partida ya no está disponible
        (apagaste ollama, sacaste una API key), igual hace falta un grafo para
        LEER el estado — y leer no invoca al LLM. Para eso cae al motor fake,
        que siempre está. Jugar, en cambio, se bloquea antes de llegar acá.
        """
        if modelo_id not in app.state.motores:
            modelo_id = MOTOR_FAKE
        clave = (caso_id, modelo_id)
        if clave not in app.state.grafos:
            actor, analista = app.state.motores[modelo_id]
            app.state.grafos[clave] = construir_grafo(
                casos[caso_id], actor, analista, checkpointer=app.state.checkpointer
            )
        return app.state.grafos[clave]

    async def _estado_de(partida: dict) -> dict:
        """El estado del grafo de una partida. Recibe la partida entera porque
        el grafo depende de dos cosas suyas: el caso y el motor."""
        grafo = _grafo_de(partida["caso_id"], partida["modelo_id"])
        return (await grafo.aget_state(_config(partida["id"]))).values

    def _caso_de(partida: dict) -> Caso | None:
        """El caso de una partida guardada, o None si ya no existe.

        Una partida vieja puede apuntar a un caso que se renombró o se sacó
        del registro. Eso no puede tumbar el archivo entero: la partida queda
        HUÉRFANA — se lista marcada y se puede incinerar, pero no abrir.
        """
        return casos.get(partida["caso_id"])

    def _estado_del_motor(modelo_id: str) -> dict:
        """Cómo está el motor de una partida guardada, para que el frontend
        avise antes de que el jugador escriba una pregunta al vacío."""
        motor = MOTORES.get(modelo_id)
        return {
            "motor_etiqueta": motor.etiqueta if motor else modelo_id,
            "motor_disponible": modelo_id in app.state.motores,
            "motor_motivo": app.state.motivos.get(modelo_id, "ese motor ya no está en el catálogo"),
        }

    def _caso_dto(caso: Caso, partida: dict) -> CasoDTO:
        motor = partida["modelo_id"]
        return CasoDTO(
            id=caso.id,
            titulo=caso.titulo,
            briefing=caso.briefing,
            max_preguntas=caso.max_preguntas,
            total_secretos=caso.total_secretos(),
            motor=motor,
            # Barajados por partida: el orden del archivo delataba al culpable.
            sospechosos=[
                SospechosoDTO(**s.model_dump())
                for s in caso.sospechosos_para(partida["id"])
            ],
            sede=caso.sede,
            ciudad=caso.ciudad,
            delito=caso.delito,
            culpable_alias=caso.culpable_alias,
        )

    # ── REST: lo informativo (nada de esto invoca el grafo) ─────────────────

    @app.get("/api/casos")
    def api_casos() -> CasosDTO:
        """El alta de expediente: qué casos hay y con qué motor se pueden jugar.

        De los casos, título y gancho nomás — nada de briefing completo,
        sospechosos ni epílogo todavía. De los motores, todo el catálogo:
        también los que hoy no andan, con el motivo."""
        return CasosDTO(
            motor_sugerido=motor_sugerido(),
            motores=[
                MotorDTO(
                    id=id_,
                    etiqueta=MOTORES[id_].etiqueta,
                    detalle=MOTORES[id_].detalle,
                    disponible=motivo is None,
                    motivo=motivo,
                )
                for id_, motivo in app.state.motivos.items()
                if id_ in MOTORES
            ],
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

    @app.get("/api/partidas")
    async def api_partidas(request: Request) -> list[dict]:
        """El archivo de casos: cada partida con un resumen de su estado."""
        partidas = await request.app.state.registro.listar()
        resultado = []
        for p in partidas:
            caso = _caso_de(p)
            if caso is None:
                resultado.append({**p, **_resumen_huerfana()})
                continue
            estado = await _estado_de(p)
            resultado.append(
                {
                    **p,
                    "caso_titulo": caso.titulo,
                    "caso_disponible": True,
                    **_estado_del_motor(p["modelo_id"]),
                    **_resumen(estado, caso),
                }
            )
        return resultado

    @app.post("/api/partidas", status_code=201)
    async def api_crear_partida(datos: NuevaPartida, request: Request) -> dict:
        nombre = datos.nombre.strip()
        if not nombre:
            raise HTTPException(422, "la partida necesita un nombre")
        if datos.caso_id not in casos:
            raise HTTPException(422, f"no existe el caso {datos.caso_id!r}")
        # El motor se valida contra los que de verdad andan, no contra el
        # catálogo entero: elegir uno sin API key desde el browser tiene que
        # fallar acá y no a mitad del primer interrogatorio.
        if datos.modelo_id not in app.state.motores:
            motivo = app.state.motivos.get(datos.modelo_id, "no existe")
            raise HTTPException(422, f"el motor {datos.modelo_id!r} no está disponible: {motivo}")
        return await request.app.state.registro.crear(nombre, datos.caso_id, datos.modelo_id)

    @app.delete("/api/partidas/{partida_id}", status_code=204)
    async def api_borrar_partida(partida_id: str, request: Request) -> None:
        partida = await request.app.state.registro.obtener(partida_id)
        if partida is None:
            raise HTTPException(404, "no existe esa partida")
        await request.app.state.registro.borrar(partida_id)
        # El registro borró los metadatos; los checkpoints los borra el
        # checkpointer, que indexa por thread_id: así una partida huérfana
        # (con un caso_id que ya no existe) también se puede incinerar.
        await app.state.checkpointer.adelete_thread(partida_id)

    @app.get("/api/partidas/{partida_id}")
    async def api_detalle_partida(partida_id: str, request: Request) -> dict:
        """Todo lo que el frontend necesita para retomar una partida:
        el caso completo, el resumen, la libreta, las conversaciones y el
        tablero."""
        partida = await request.app.state.registro.obtener(partida_id)
        if partida is None:
            raise HTTPException(404, "no existe esa partida")

        caso = _caso_de(partida)
        if caso is None:
            raise HTTPException(
                410, f"el caso {partida['caso_id']!r} de este expediente ya no está disponible"
            )
        estado = await _estado_de(partida)
        detalle = {
            **partida,
            **_estado_del_motor(partida["modelo_id"]),
            "caso": _caso_dto(caso, partida),
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
                     ``error``                                   (jugada rechazada
                                                                  o ilegible)

        El turno completo viaja al final en ``turno.respuesta`` aunque ya haya
        salido por fragmentos: el streaming es mejora progresiva, no la fuente
        de verdad — si un modelo no streamea, el juego funciona igual.
        """
        partida = await websocket.app.state.registro.obtener(partida_id)
        # 4404: código de aplicación (la franja 4000-4999 es libre en WS). Vale
        # tanto para la partida que no existe como para la huérfana: en las dos
        # no hay nada que jugar, y el browser no debe reintentar.
        if partida is None or _caso_de(partida) is None:
            await websocket.close(code=4404)
            return
        await websocket.accept()
        # 4409: el caso existe y la partida también, pero su motor hoy no
        # anda. Cerramos con un código distinto del 4404 para que el browser
        # sepa que esto SÍ se arregla (prendiendo ollama, poniendo la key) y
        # pueda decir cuál de las dos cosas.
        if partida["modelo_id"] not in app.state.motores:
            await _error(websocket, _estado_del_motor(partida["modelo_id"])["motor_motivo"])
            await websocket.close(code=4409)
            return

        try:
            while True:
                # Lo que llega por el socket lo escribe el browser: puede ser
                # cualquier cosa. Un JSON roto (o uno que no sea un objeto) se
                # contesta con un error, no tumba la conexión.
                try:
                    jugada = await websocket.receive_json()
                except ValueError:
                    await _error(websocket, "no entendí el mensaje: esperaba JSON")
                    continue
                if not isinstance(jugada, dict):
                    await _error(websocket, "la jugada tiene que ser un objeto JSON")
                    continue
                match jugada.get("tipo"):
                    case "interrogar":
                        await _jugada_interrogar(websocket, partida, jugada)
                    case "acusar":
                        await _jugada_acusar(websocket, partida, jugada)
                    case desconocido:
                        await _error(websocket, f"no conozco la jugada {desconocido!r}")
        except WebSocketDisconnect:
            pass  # el jugador cerró la pestaña; la partida queda en la base

    async def _jugada_interrogar(websocket: WebSocket, partida: dict, jugada: dict) -> None:
        partida_id = partida["id"]
        caso = casos[partida["caso_id"]]
        grafo = _grafo_de(partida["caso_id"], partida["modelo_id"])
        estado = await _estado_de(partida)
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
        if len(pregunta) > MAX_PREGUNTA:
            return await _error(
                websocket, f"la pregunta no puede pasar los {MAX_PREGUNTA} caracteres"
            )

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

        estado = await _estado_de(partida)
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

    async def _jugada_acusar(websocket: WebSocket, partida: dict, jugada: dict) -> None:
        partida_id = partida["id"]
        caso = casos[partida["caso_id"]]
        grafo = _grafo_de(partida["caso_id"], partida["modelo_id"])
        estado = await _estado_de(partida)
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
        """Avisa de una jugada rechazada, sin romperse si ya no hay a quién avisarle.

        El aviso de error suele ser lo ÚLTIMO que pasa en un socket agonizante:
        si el LLM tardó tanto que se cayó el keepalive, uvicorn ya cerró la
        conexión y este ``send_json`` levanta un ``RuntimeError`` que sube por
        todo el stack y tapa el error verdadero en el log. El motivo real vale
        más que el aviso que ya nadie va a leer.
        """
        try:
            await websocket.send_json({"tipo": "error", "mensaje": mensaje})
        except (RuntimeError, WebSocketDisconnect):
            print(f"[ws] no pude avisar del error (socket cerrado): {mensaje}")

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

    def _resumen_huerfana() -> dict:
        """El resumen de una partida cuyo caso ya no existe: sin números que
        inventar, y marcada para que el archivo la muestre como ilegible."""
        return {
            "caso_titulo": "— expediente ilegible —",
            "caso_disponible": False,
            "preguntas_usadas": 0,
            "preguntas_restantes": 0,
            "pistas_descubiertas": 0,
            "total_secretos": 0,
            "resultado": None,
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
            "calificacion": _calificacion(
                estado["resultado"], encontradas, caso.total_secretos(), caso.culpable_alias
            ),
            "pistas_descubiertas": encontradas,
            "total_secretos": caso.total_secretos(),
            "preguntas_usadas": estado.get("preguntas_usadas", 0),
        }

    # El frontend: archivos estáticos servidos por el mismo proceso. Montado
    # al final para que /api y /ws (declarados antes) tengan prioridad.
    app.mount("/", StaticFiles(directory=ESTATICO, html=True), name="estatico")

    return app


def _calificacion(resultado: str, encontradas: int, total: int, alias: str) -> str:
    """El remate según cómo se jugó — gemelo en texto plano del que muestra
    el CLI con markup de rich (``cli._calificacion``)."""
    if resultado != "victoria":
        return f"🪦 El {alias} sigue suelto. Alguien va a tener que reabrir el expediente."
    if encontradas >= total * 0.8:
        return "🏆 Detective de leyenda: resolviste el caso con la evidencia en la mano."
    if encontradas >= total * 0.4:
        return "🕵️ Buen ojo, detective. Un par de pistas más y era de manual."
    return "🍀 Acertaste... con más instinto que evidencia. La suerte también cuenta."


# ── Punto de entrada del comando ``detective-web`` ───────────────────────────


def main() -> None:
    """Levanta el servidor con todos los casos y todos los motores usables.

    A diferencia del CLI, acá no se elige nada por adelantado: el relevamiento
    de motores pasa dentro del ``lifespan`` y cada jugador elige el suyo al
    abrir un expediente. Que falte una API key o esté apagado ollama no impide
    arrancar — se ve reflejado en el selector.
    """
    load_dotenv()

    ruta_db = os.environ.get("DETECTIVE_DB", "partidas.sqlite")
    puerto = int(os.environ.get("DETECTIVE_WEB_PORT", "8765"))
    app = crear_app(CASOS, ruta_db=ruta_db)

    print(f"🛰️  El Caso Calafate — http://127.0.0.1:{puerto}")
    print(f"    partidas en {ruta_db} · {len(CASOS)} casos · {len(MOTORES)} motores en el catálogo")
    print(f"    motor sugerido: {motor_sugerido()} (cada partida elige el suyo)")
    uvicorn.run(app, host="127.0.0.1", port=puerto, log_level="warning")
