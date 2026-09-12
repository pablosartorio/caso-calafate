# 🛰️ El Caso Calafate

Juego de misterio por interrogatorios en la terminal. Vos sos el detective;
tres sospechosos — interpretados por un LLM — esconden lo que pasó la noche en
que alguien saboteó el satélite CALAFATE-1 en Bariloche. Tenés 15 preguntas
para juntar pistas y una sola oportunidad de acusar.

Abajo del capó es un proyecto didáctico de **LangGraph + LangChain**: un grafo
con ruteo condicional, estado persistente con checkpointer, salida
estructurada y streaming, todo testeado sin gastar un token.

```
(12❓) Marta › ¿Perdiste tu tarjeta de acceso, no?

Marta Iriarte — Lo... sí. Perdí mi tarjeta el jueves. No lo reporté: perderla
es una falta grave, ¿entiende? Pero yo no entré a la sala limpia anoche.

╭─────────────────────────── 🔎 Nueva pista ───────────────────────────╮
│ La tarjeta que abrió la sala limpia a las 03:02 no la tenía Marta:   │
│ la perdió el jueves y no lo reportó.                                 │
╰──────────────────────────────────────────────────────────────────────╯
```

> ⚠️ **Spoiler**: los datos de `src/caso_calafate/casos/` revelan al culpable
> de cada caso. Jugá una partida antes de leer el código. :)

## Cómo jugar

Requisitos: [`uv`](https://docs.astral.sh/uv/). Nada más — uv se encarga de
Python y de las dependencias.

```bash
uv sync
cp .env.example .env   # elegí el motor LLM acá (ver opciones abajo)
uv run detective
```

El juego es **local**: los modelos corren en tu Ollama, no cuestan nada y no
necesitan ninguna API key. El motor se elige **al empezar cada partida**, en el
CLI y en la web, así que no hace falta editar nada para probar otro. El
catálogo vive en `llm.py` (`MOTORES`) y el selector muestra también los que hoy
no andan, con el motivo — `ollama serve` apagado, un modelo sin bajar — así que
la tabla de motores funciona además como ayuda de instalación.

| Motor | Qué necesita | Cómo se juega |
|---|---|---|
| `ollama:qwen2.5:7b` | `ollama serve` corriendo y `ollama pull qwen2.5:7b` | El default: el más parejo de los tres. |
| `ollama:llama3.1:8b` | ídem, con `ollama pull llama3.1:8b` | Más lento, otra voz. |
| `ollama:llama3.2:1b` | ídem, con `ollama pull llama3.2:1b` | Rapidísimo y el más flojo actuando. |
| `fake` | Nada | Sin LLM: respuestas enlatadas y pistas que se revelan solas. Para probar la mecánica y para los tests. |

`DETECTIVE_MODEL` en el `.env` ya no es "el motor del juego": es apenas **el
que viene preseleccionado** en el selector.

### Comandos dentro del juego

| Comando | Qué hace |
|---|---|
| `/sospechosos` | Quiénes son y qué dicen haber hecho esa noche |
| `/hablar <nombre>` | Elegir a quién interrogar (acepta prefijos: `/hablar mar`) |
| *escribir texto* | Hacerle una pregunta al sospechoso elegido (gasta 1 de las 15) |
| `/pistas` | Tu libreta de pistas descubiertas |
| `/caso` | Releer el briefing |
| `/acusar <nombre>` | Señalar al culpable — cierra la partida, **una sola oportunidad** |
| `/salir` | Abandonar el caso |

## La interfaz web: el escritorio del detective

El mismo motor, otra piel — tal como promete el docstring de `cli.py`:

```bash
uv run detective-web    # y abrí http://127.0.0.1:8765
```

Sos el detective frente a tu escritorio: el interrogatorio se ve por un
monitor CRT (la cámara de la sala), las pistas caen en una libreta
manuscrita, hay un tablero de corcho donde conectás la evidencia con hilo
rojo, la acusación se estampa con un sello, y el veredicto sale en la tapa
del diario del día siguiente. Con lluvia patagónica de fondo — todo el sonido
está sintetizado con Web Audio, no hay un solo archivo de audio.

Qué mirar del lado técnico:

- **El motor no cambió.** `web/servidor.py` es el gemelo de `cli.py`: REST
  para lo informativo (como `/pistas` o `/caso`, lee estado con
  `aget_state()`) y un WebSocket por partida para las jugadas, que streamea
  los tokens del actor al browser con el mismo `stream_mode="messages"`.
- **Partidas guardadas.** `SqliteSaver` (bueno, su versión async) reemplaza a
  `MemorySaver`: cada expediente es un `thread_id` en `partidas.sqlite`, y se
  retoma desde el archivo de casos. El registro de nombres y el tablero viven
  en una tabla propia dentro del mismo archivo (`web/partidas.py`).
- **DTOs anti-spoiler.** El browser es territorio del jugador (F12 mediante):
  los modelos de respuesta filtran `es_culpable`, los secretos y el epílogo,
  que recién viaja cuando la partida se cierra. Hay un test que lo garantiza.
- **Frontend artesanal.** HTML/CSS/JS sin frameworks ni build step, servido
  por el mismo proceso. Los retratos son SVG dibujados a mano, las texturas
  (madera, papel, corcho, nieve del CRT) son gradientes + `feTurbulence`, y
  el revelado tipo teletipo desacopla el reloj de la red del de la pantalla
  (`estatico/js/crt.js`).

## Cómo funciona

Cada turno del juego es **una invocación del grafo**. El CLI arma la jugada
(`interrogar` o `acusar`), el grafo la procesa y el checkpointer guarda la
partida para el turno siguiente:

```mermaid
graph LR
    START((START)) -->|accion = interrogar| I[interrogar 🎭]
    START -->|accion = acusar| A[acusar ⚖️]
    I --> AN[analizar 🔎]
    AN --> C[cerrar_turno ⏱️]
    C --> FIN((END))
    A --> FIN
```

- **interrogar** — el LLM *actor* responde en personaje, con el historial de
  ese sospechoso y un system prompt armado desde los datos del caso.
- **analizar** — un segundo rol de LLM, el *analista*, lee la respuesta y
  decide con **salida estructurada** (un modelo Pydantic) qué secretos se
  revelaron. El nodo filtra alucinaciones y repetidos.
- **cerrar_turno** — descuenta la pregunta. Determinista, sin LLM.
- **acusar** — compara acusado vs. culpable y cierra la partida.

### Mapa del código (en orden de lectura sugerido)

| Archivo | Qué es | Concepto que muestra |
|---|---|---|
| `caso.py` | El MODELO del misterio: sospechosos, secretos, vocabulario | Pydantic con validadores (`model_validator`); separar contenido de motor |
| `casos/` | Los casos jugables, uno por archivo, en un registro por id | Datos como módulos; agregar un caso es agregar un archivo |
| `estado.py` | El estado tipado que fluye por el grafo | `TypedDict` como estado de LangGraph; **reducers** (`Annotated[..., acumular_pistas]`) |
| `prompts.py` | La "dirección de actores": prompts de actor y analista | El contrato de salida estructurada (`SecretosRevelados`) |
| `nodos.py` | Las funciones `estado → actualización` | Nodos testeables; inyección de dependencias; validar lo que dice el LLM |
| `grafo.py` | Ensambla y compila el grafo | `StateGraph`, `add_conditional_edges`, **checkpointer** (`MemorySaver` + `thread_id`) |
| `llm.py` | El catálogo de motores y su fábrica | `init_chat_model` multi-proveedor; `with_structured_output` (y su `method`); relevar disponibilidad en runtime |
| `cli.py` | La capa visual (rich) | **Streaming** con `stream_mode="messages"`; leer estado con `get_state()` |
| `web/servidor.py` | La otra capa visual: FastAPI | REST + WebSocket; DTOs anti-spoiler; `astream` y `aget_state`; cache de grafos por `(caso, motor)` |
| `web/partidas.py` | Registro de partidas guardadas | Convivir con el checkpointer en la misma SQLite; migraciones livianas con `PRAGMA table_info` |
| `pixelart/` | Los retratos VGA como texto, con capas de animación, un módulo por caso | El arte como dato: se versiona y se valida al importar; agregar un caso nuevo es agregar un archivo |
| `web/estatico/` | El frontend (HTML/CSS/JS a mano) | Streaming por WS; revelado teletipo; texturas con CSS; Web Audio |
| `tests/` | 263 tests que corren en ~3 s | Testear apps LLM **sin LLM**: fakes, caso de juguete, `TestClient` con WebSocket |

## Tests

```bash
uv run pytest        # 263 tests, sin API key, sin red
uv run ruff check .  # lint
```

GitHub Actions (`.github/workflows/ci.yml`) corre ambos comandos en cada push
y PR — no hace falta acordarse de correrlos a mano antes de mergear.

La idea clave: el grafo recibe el actor y el analista **por parámetro**
(inyección de dependencias), así que los tests enchufan modelos falsos de
LangChain y prueban la lógica completa — ruteo, checkpointer, acumulación de
pistas, veredictos — en milisegundos. Además usan un caso de juguete propio
(«¿Quién se comió el asado?»), de modo que editar El Caso Calafate no rompe
ningún test del motor.

## Ideas para extender (ejercicios)

De más fácil a más difícil:

1. ~~**Escribí tu propio caso.**~~ Ya hay 22 en el registro (`casos/`), pero
   el selector de casos (CLI y web) solo ofrece los 10 profundizados a fondo
   —inspirados en cuentos y novelas policiales argentinos reales, con
   personajes complejos y retrato pixel art propio—: `mascardi`, `roca`,
   `llaollao`, `arrayanes`, `jacobacci`, `moreno`, `frias`, `tronador`,
   `epuyen`, `pichileufu`. Los otros 12 (el Calafate original y la primera
   tanda) siguen en el registro completo (`CASOS` en `casos/__init__.py`) sin
   profundizar todavía, y una partida vieja de alguno se puede seguir
   retomando — simplemente no aparecen en el alta de expediente nueva
   (`CASOS_VISIBLES`). Copiá el archivo de un caso, cambiale los datos, y si
   querés que aparezca en el selector sumalo también a `CASOS_VISIBLES`. Los
   validadores te avisan si te olvidás del culpable, y los tests de
   `test_caso.py` corren solos sobre el caso nuevo.
2. **Pistas falsas.** Agregale a `Secreto` un campo `es_pista_falsa` y que la
   libreta las marque distinto cuando se descubre la verdad.
3. **Careo.** Un comando `/carear <a> <b>` donde un sospechoso reacciona a lo
   que dijo otro (necesita pasar fragmentos de una conversación a otra).
4. **Motores de nube.** `init_chat_model` acepta `google_genai:` y `groq:` sin
   tocar el motor: alcanza con instalar el paquete de integración y agregar una
   línea a `MOTORES` — el servidor, el CLI y el frontend ni se enteran. Ojo con
   el analista: `with_structured_output` sobre Groq usa `tool_choice` forzado
   por defecto y no todos los modelos gratis lo respetan; para esos hay que
   pedirle `method="json_schema"` (para eso está `Motor.metodo_estructurado`).
4. ~~**Partidas guardadas.**~~ Resuelto en la interfaz web (`web/partidas.py` +
   `AsyncSqliteSaver`). Queda para el CLI: agregá `--partida <nombre>` usando
   el mismo `thread_id` contra la misma base.
5. ~~**Interfaz web.**~~ ¡Hecha! (`web/`). Para seguirla: un **modo
   espectador** — otra pestaña abierta en la misma partida que mire el
   interrogatorio en vivo (el `thread_id` ya lo permite; falta que el server
   reparta los fragmentos a más de un socket).
