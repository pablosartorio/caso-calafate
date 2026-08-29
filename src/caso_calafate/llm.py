"""Fábrica de modelos de lenguaje: el catálogo de motores y cómo se instancian.

Todo lo que depende de QUÉ LLM se usa vive en este archivo. El resto del
código habla con "un actor" y "un analista" sin saber si detrás hay un modelo
local de Ollama o un fake para tests.

El juego es **local**: los motores corren en tu Ollama, no cuestan nada y no
necesitan API key. Cada partida elige SU motor al crearse, igual que elige su
caso: por eso acá hay un CATÁLOGO (``MOTORES``) y no un único modelo global.

El id de cada motor es el string "proveedor:modelo" que entiende
``init_chat_model`` de LangChain: una sola función que instancia el chat model
del proveedor que sea, sin que nuestro código importe nada específico de
Ollama. Ojo con los dos puntos: ``init_chat_model`` parte el string una sola
vez (``split(":", maxsplit=1)``), así que
``ollama:qwen2.5:7b`` se lee como proveedor ``ollama`` + modelo ``qwen2.5:7b``.
"""

import itertools
import os
from dataclasses import dataclass

from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.runnables import Runnable, RunnableLambda

from caso_calafate.prompts import SecretosRevelados

MOTOR_FAKE = "fake"


@dataclass(frozen=True)
class Motor:
    """Una entrada del catálogo: un modelo que el jugador puede elegir."""

    id: str  # "ollama:qwen2.5:7b" — lo que entiende init_chat_model
    etiqueta: str  # "Qwen 2.5 7B" — lo que ve el jugador
    proveedor: str  # "ollama" | "fake"
    detalle: str  # una línea de contexto para el selector
    modelo: str = ""  # el nombre suelto, sin el prefijo del proveedor
    metodo_estructurado: str | None = None  # ver la nota de abajo

    @property
    def es_local(self) -> bool:
        return self.proveedor == "ollama"


# El orden de este dict ES el orden del selector, en el CLI y en la web.
#
# Sobre ``metodo_estructurado``: el "analista" del juego es el modelo envuelto
# con ``with_structured_output``, y no todos los modelos lo resuelven igual.
# Si alguno se porta mal con el formato de las pistas, se le pide otro método
# acá y no en el nodo.
MOTORES: dict[str, Motor] = {
    motor.id: motor
    for motor in [
        Motor(
            id="ollama:qwen2.5:7b",
            etiqueta="Qwen 2.5 7B",
            proveedor="ollama",
            modelo="qwen2.5:7b",
            detalle="local y gratis — el más parejo de los tres",
        ),
        Motor(
            id="ollama:llama3.1:8b",
            etiqueta="Llama 3.1 8B",
            proveedor="ollama",
            modelo="llama3.1:8b",
            detalle="local y gratis — más lento, otra voz",
        ),
        Motor(
            id="ollama:llama3.2:1b",
            etiqueta="Llama 3.2 1B",
            proveedor="ollama",
            modelo="llama3.2:1b",
            detalle="local y gratis — rapidísimo, actuación rústica",
        ),
        Motor(
            id=MOTOR_FAKE,
            etiqueta="Sin LLM (modo fake)",
            proveedor="fake",
            detalle="respuestas enlatadas y pistas que se revelan solas",
        ),
    ]
}

MOTOR_POR_DEFECTO = "ollama:qwen2.5:7b"


def motor_sugerido() -> str:
    """El motor que viene preseleccionado en el selector.

    Sale de ``DETECTIVE_MODEL`` si está en el ``.env`` y es un id conocido; si
    no, del default. Ya no es "el motor del juego" como antes: ahora es apenas
    una sugerencia, porque cada partida elige el suyo.
    """
    elegido = os.environ.get("DETECTIVE_MODEL", "").strip()
    return elegido if elegido in MOTORES else MOTOR_POR_DEFECTO


async def relevar_motores() -> dict[str, str | None]:
    """Qué motores se pueden usar ahora mismo, y por qué no los que no.

    Devuelve id → motivo, donde ``None`` significa "listo para jugar". Se
    releva en runtime y no al importar el módulo, porque las condiciones
    cambian solas: prendés ``ollama serve``, bajás un modelo con ``ollama
    pull``. Mostrar el motivo (en vez de esconder el motor) es a propósito: es
    la mitad de la ayuda que necesita quien recién arranca.
    """
    modelos_locales = await _modelos_de_ollama()
    estado: dict[str, str | None] = {}
    for id_, motor in MOTORES.items():
        estado[id_] = _motivo_de_indisponibilidad(motor, modelos_locales)
    return estado


def _motivo_de_indisponibilidad(motor: Motor, modelos_locales: set[str] | None) -> str | None:
    if motor.proveedor == "fake":
        return None

    if modelos_locales is None:
        return "ollama serve no está corriendo"
    if motor.modelo not in modelos_locales:
        return f"falta bajarlo: ollama pull {motor.modelo}"
    return None


async def _modelos_de_ollama() -> set[str] | None:
    """Los modelos bajados en el Ollama local, o None si el servidor no está.

    Distinguir "no hay servidor" de "no está ese modelo" importa: son dos
    problemas con dos soluciones distintas (``ollama serve`` vs ``ollama
    pull``), y el selector muestra cuál de las dos te toca.
    """
    try:
        import ollama

        respuesta = await ollama.AsyncClient().list()
    except Exception:  # servidor apagado, timeout, versión rara del cliente
        return None

    nombres = set()
    for modelo in respuesta.models:
        nombre = modelo.model or ""
        nombres.add(nombre)
        # Ollama devuelve "qwen2.5:7b" pero también acepta "qwen2.5" a secas
        # cuando el tag es "latest".
        if nombre.endswith(":latest"):
            nombres.add(nombre.removesuffix(":latest"))
    return nombres


def crear_motores(nombre: str | None = None) -> tuple[BaseChatModel, Runnable, str]:
    """Crea el par de modelos que usa una partida.

    Devuelve ``(actor, analista, id_del_motor)``:

    - ``actor``: el chat model que interpreta a los sospechosos.
    - ``analista``: el mismo modelo envuelto con ``with_structured_output``,
      así que su ``invoke()`` devuelve un ``SecretosRevelados`` validado.

    Nota: no fijamos ``temperature`` a propósito. Los defaults de cada
    proveedor andan bien para este juego, y algunos modelos directamente
    rechazan los parámetros de sampling.
    """
    nombre = nombre or motor_sugerido()
    if nombre == MOTOR_FAKE:
        actor, analista = _motores_fake()
        return actor, analista, nombre

    motor = MOTORES.get(nombre)
    modelo = init_chat_model(nombre)
    extras = {}
    if motor is not None and motor.metodo_estructurado:
        extras["method"] = motor.metodo_estructurado
    analista = modelo.with_structured_output(SecretosRevelados, **extras)
    return modelo, analista, nombre


def _motores_fake() -> tuple[BaseChatModel, Runnable]:
    """Modelos falsos para jugar sin API.

    El actor recita respuestas enlatadas (en loop infinito, gracias a
    ``itertools.cycle``) y el analista "revela" todos los secretos que existan
    en CUALQUIER caso del registro. Puede devolver ids que no son del
    sospechoso interrogado (ni siquiera del caso que se está jugando): no
    importa, porque ``nodo_analizar`` filtra los que no corresponden — otra
    ventaja de validar en el nodo en vez de confiar en el modelo. Eso es lo
    que permite que este fake sirva para CUALQUIER caso sin conocerlo.
    """
    # Import local para evitar un ciclo: caso.py no importa nada del paquete,
    # pero llm.py sí es importado por módulos que caso.py no debe conocer.
    from caso_calafate.casos import CASOS

    respuestas = itertools.cycle(
        [
            AIMessage("Mirá, detective... esa noche yo no vi nada raro. Nada."),
            AIMessage("¿Me está acusando? Pregúntele a los demás: alguno miente."),
            AIMessage("No tengo nada que ocultar. Bueno... casi nada."),
        ]
    )
    actor = GenericFakeChatModel(messages=respuestas)

    todos_los_ids = [
        secreto.id
        for caso in CASOS.values()
        for sospechoso in caso.sospechosos
        for secreto in sospechoso.secretos
    ]
    analista = RunnableLambda(lambda _prompt: SecretosRevelados(ids=todos_los_ids))
    return actor, analista


def texto_de(mensaje: BaseMessage) -> str:
    """Extrae el texto plano de un mensaje (o chunk de streaming) de LangChain.

    ``mensaje.content`` puede ser un string o una lista de bloques — según el
    proveedor y el modelo, a veces llega ``[{"type": "text", "text": ...}]``.
    Acá normalizamos los dos casos para que el resto del código no se entere.
    """
    contenido = mensaje.content
    if isinstance(contenido, str):
        return contenido
    partes = []
    for bloque in contenido:
        if isinstance(bloque, dict):
            partes.append(bloque.get("text", ""))
        else:
            partes.append(str(bloque))
    return "".join(partes)
