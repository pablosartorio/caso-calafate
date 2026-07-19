"""El registro de partidas: los metadatos que el checkpointer no guarda.

El ESTADO de cada partida (conversaciones, pistas, preguntas usadas) ya vive
en el checkpointer de LangGraph, indexado por ``thread_id`` — eso no cambia
al pasar del CLI a la web. Pero el checkpointer no sabe qué es una "partida":
no guarda nombres, ni fechas de creación, ni el corcho con hilos rojos del
tablero de evidencias (que es puro estado VISUAL, del frontend).

Este registro guarda esos metadatos en una tabla propia dentro de la MISMA
base SQLite que usa ``AsyncSqliteSaver``: un solo archivo ``partidas.sqlite``
con dos mundos adentro — las tablas de LangGraph y la nuestra.

La separación importa: si mañana el tablero cambia de formato, el estado del
juego ni se entera; y si el motor suma claves al estado, este registro
tampoco. Cada capa persiste lo suyo.
"""

import json
import uuid
from datetime import UTC, datetime

import aiosqlite


class RegistroPartidas:
    """CRUD mínimo de partidas sobre una conexión aiosqlite compartida.

    Recibe la conexión desde afuera (la misma que usa el checkpointer) en
    lugar de abrirla acá: inyección de dependencias otra vez, igual que los
    nodos reciben el LLM. Los tests le pasan una base en memoria.
    """

    def __init__(self, conexion: aiosqlite.Connection):
        self._conexion = conexion

    async def preparar(self) -> None:
        """Crea la tabla si no existe (y migra las que ya existían). Llamalo
        una vez al levantar la app."""
        await self._conexion.execute(
            """
            CREATE TABLE IF NOT EXISTS partidas (
                id      TEXT PRIMARY KEY,
                nombre  TEXT NOT NULL,
                creada  TEXT NOT NULL,
                tablero TEXT NOT NULL DEFAULT '{}',
                caso_id TEXT NOT NULL DEFAULT 'calafate'
            )
            """
        )
        # Migración liviana: un partidas.sqlite de antes de que existiera el
        # multi-caso tiene la tabla sin esta columna — CREATE TABLE IF NOT
        # EXISTS no la agrega sola. Las partidas viejas quedan como
        # 'calafate', que era el único caso que existía entonces.
        cursor = await self._conexion.execute("PRAGMA table_info(partidas)")
        columnas = {fila[1] for fila in await cursor.fetchall()}
        if "caso_id" not in columnas:
            await self._conexion.execute(
                "ALTER TABLE partidas ADD COLUMN caso_id TEXT NOT NULL DEFAULT 'calafate'"
            )
        await self._conexion.commit()

    async def crear(self, nombre: str, caso_id: str) -> dict:
        """Da de alta una partida y devuelve sus metadatos.

        El id es un uuid recortado: corto para viajar en URLs, único de sobra
        para una base local. Ese mismo id será el ``thread_id`` del grafo.
        """
        partida = {
            "id": uuid.uuid4().hex[:12],
            "nombre": nombre,
            "creada": datetime.now(UTC).isoformat(timespec="seconds"),
            "caso_id": caso_id,
        }
        await self._conexion.execute(
            "INSERT INTO partidas (id, nombre, creada, caso_id) VALUES (?, ?, ?, ?)",
            (partida["id"], partida["nombre"], partida["creada"], partida["caso_id"]),
        )
        await self._conexion.commit()
        return partida

    async def listar(self) -> list[dict]:
        """Todas las partidas, la más nueva primero."""
        cursor = await self._conexion.execute(
            "SELECT id, nombre, creada, caso_id FROM partidas ORDER BY creada DESC, id"
        )
        filas = await cursor.fetchall()
        return [{"id": f[0], "nombre": f[1], "creada": f[2], "caso_id": f[3]} for f in filas]

    async def obtener(self, id_: str) -> dict | None:
        """Una partida con su tablero deserializado, o None si no existe."""
        cursor = await self._conexion.execute(
            "SELECT id, nombre, creada, tablero, caso_id FROM partidas WHERE id = ?", (id_,)
        )
        fila = await cursor.fetchone()
        if fila is None:
            return None
        return {
            "id": fila[0],
            "nombre": fila[1],
            "creada": fila[2],
            "tablero": json.loads(fila[3]),
            "caso_id": fila[4],
        }

    async def borrar(self, id_: str) -> bool:
        """Elimina la partida del registro. Devuelve False si no existía.

        Ojo: esto borra los METADATOS. Los checkpoints del grafo los borra el
        servidor con ``checkpointer.adelete_thread`` — cada capa limpia lo suyo.
        """
        cursor = await self._conexion.execute("DELETE FROM partidas WHERE id = ?", (id_,))
        await self._conexion.commit()
        return cursor.rowcount > 0

    async def guardar_tablero(self, id_: str, tablero: dict) -> bool:
        """Persiste el estado visual del tablero (posiciones e hilos), como JSON."""
        cursor = await self._conexion.execute(
            "UPDATE partidas SET tablero = ? WHERE id = ?", (json.dumps(tablero), id_)
        )
        await self._conexion.commit()
        return cursor.rowcount > 0
