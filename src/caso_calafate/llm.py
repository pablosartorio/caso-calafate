"""Fábrica de modelos de lenguaje.

Todo lo que depende de QUÉ LLM se usa vive en este archivo. El resto del
código habla con "un actor" y "un analista" sin saber si detrás hay Claude,
un modelo local de Ollama o un fake para tests.

El motor se elige con la variable de entorno ``DETECTIVE_MODEL``:

- ``anthropic:claude-opus-4-8``  → Claude vía API (necesita ANTHROPIC_API_KEY).
- ``ollama:llama3.2``            → modelo local gratis (necesita ``ollama serve``).
- ``fake``                       → sin ningún LLM; respuestas enlatadas para
                                   probar la mecánica del juego y los tests.

El formato "proveedor:modelo" es el que entiende ``init_chat_model`` de
LangChain: una sola función que instancia el chat model del proveedor que sea,
sin que nuestro código importe nada específico de Anthropic ni de Ollama.
"""

import itertools
import os

from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.runnables import Runnable, RunnableLambda

from caso_calafate.prompts import SecretosRevelados

MODELO_POR_DEFECTO = "anthropic:claude-opus-4-8"


def crear_motores(nombre: str | None = None) -> tuple[BaseChatModel, Runnable, str]:
    """Crea el par de modelos que usa el juego.

    Devuelve ``(actor, analista, nombre_del_motor)``:

    - ``actor``: el chat model que interpreta a los sospechosos.
    - ``analista``: el mismo modelo envuelto con ``with_structured_output``,
      así que su ``invoke()`` devuelve un ``SecretosRevelados`` validado.

    Nota: no fijamos ``temperature`` a propósito. Los modelos Claude recientes
    (Opus 4.7 en adelante) directamente rechazan los parámetros de sampling,
    y los defaults de cada proveedor andan bien para este juego.
    """
    nombre = nombre or os.environ.get("DETECTIVE_MODEL", MODELO_POR_DEFECTO)
    if nombre == "fake":
        actor, analista = _motores_fake()
        return actor, analista, nombre

    modelo = init_chat_model(nombre)
    analista = modelo.with_structured_output(SecretosRevelados)
    return modelo, analista, nombre


def _motores_fake() -> tuple[BaseChatModel, Runnable]:
    """Modelos falsos para jugar sin API.

    El actor recita respuestas enlatadas (en loop infinito, gracias a
    ``itertools.cycle``) y el analista "revela" todos los secretos que existan
    en el caso. Puede devolver ids de sospechosos que no son el interrogado:
    no importa, porque ``nodo_analizar`` filtra los que no corresponden — otra
    ventaja de validar en el nodo en vez de confiar en el modelo.
    """
    # Import local para evitar un ciclo: caso.py no importa nada del paquete,
    # pero llm.py sí es importado por módulos que caso.py no debe conocer.
    from caso_calafate.caso import CASO_CALAFATE

    respuestas = itertools.cycle(
        [
            AIMessage("Mirá, detective... esa noche yo no vi nada raro. Nada."),
            AIMessage("¿Me está acusando? Pregúntele a los demás: alguno miente."),
            AIMessage("No tengo nada que ocultar. Bueno... casi nada."),
        ]
    )
    actor = GenericFakeChatModel(messages=respuestas)

    todos_los_ids = [s.id for sospechoso in CASO_CALAFATE.sospechosos for s in sospechoso.secretos]
    analista = RunnableLambda(lambda _prompt: SecretosRevelados(ids=todos_los_ids))
    return actor, analista


def texto_de(mensaje: BaseMessage) -> str:
    """Extrae el texto plano de un mensaje (o chunk de streaming) de LangChain.

    ``mensaje.content`` puede ser un string o una lista de bloques — Anthropic,
    por ejemplo, a veces devuelve ``[{"type": "text", "text": ...}]``. Acá
    normalizamos los dos casos para que el resto del código no se entere.
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
