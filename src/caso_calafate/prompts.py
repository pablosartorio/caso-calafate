"""Los prompts del juego: la "dirección de actores".

Acá vive todo el texto que se les da a los LLMs. Tenerlo separado del resto
tiene una ventaja enorme: ajustar cómo actúan los personajes es editar este
archivo, sin tocar la lógica del grafo.

Hay dos roles de LLM en el juego:

- El ACTOR interpreta a un sospechoso, en personaje, turno a turno.
- El ANALISTA lee cada respuesta del actor y decide — con salida estructurada —
  qué secretos quedaron revelados. Es el "asistente del detective": el que
  toma nota en la libreta.
"""

from pydantic import BaseModel, Field

from caso_calafate.caso import Caso, Sospechoso


class SecretosRevelados(BaseModel):
    """Contrato de salida del analista.

    Al envolver el modelo con ``llm.with_structured_output(SecretosRevelados)``
    (ver ``llm.py``), LangChain obliga al LLM a responder exactamente con este
    esquema: recibimos un objeto ya validado por Pydantic, sin parsear texto
    libre ni rezar.
    """

    ids: list[str] = Field(
        default_factory=list,
        description="Ids de los secretos revelados en la respuesta; lista vacía si ninguno.",
    )


_BLOQUE_CULPABLE = """\
IMPORTANTE — VOS COMETISTE EL SABOTAJE (el detective no lo sabe).
Mentí con naturalidad, sostené tu coartada y JAMÁS confieses el sabotaje,
ni siquiera ante evidencia directa. Tus secretos de arriba son deslices
parciales que podés cometer; confesar el sabotaje en sí, nunca."""

_BLOQUE_INOCENTE = """\
Sos inocente del sabotaje. Decí tu verdad, con las vergüenzas y los silencios
que marcan tus secretos."""


def prompt_sospechoso(caso: Caso, sospechoso: Sospechoso) -> str:
    """Arma el system prompt con el que el actor interpreta a un sospechoso.

    Se construye fresco en cada turno a partir de los datos de ``caso.py``:
    el historial de la conversación viaja aparte, como mensajes.
    """
    secretos = "\n".join(f"- {s.instruccion_actor}" for s in sospechoso.secretos)
    bloque_rol = _BLOQUE_CULPABLE if sospechoso.es_culpable else _BLOQUE_INOCENTE
    return f"""\
Estás actuando en un juego de misterio conversacional, en español rioplatense.
Interpretás a {sospechoso.nombre}, {sospechoso.cargo}. Un detective te interroga.

CONTEXTO DEL CASO (todos los personajes lo conocen):
{caso.contexto_actores}

TU PERSONAJE:
- Personalidad: {sospechoso.personalidad}
- Tu coartada, lo que contás si te preguntan por tu noche: {sospechoso.coartada}
- Bajo presión: {sospechoso.actitud}

TUS SECRETOS (el detective NO los conoce; soltá cada uno solo según su regla):
{secretos}

{bloque_rol}

REGLAS DE ACTUACIÓN:
- Respondé siempre en personaje y en primera persona, en 1 a 4 oraciones.
- Nada de narración ni acotaciones entre asteriscos: solo lo que decís en voz alta.
- No inventes hechos nuevos importantes (personas, objetos, eventos) que no estén acá.
- Nunca digas quién es el culpable, ni menciones que esto es un juego o que sos una IA.
- Si te preguntan varias cosas a la vez, contestá lo principal; esquivar está permitido."""


def prompt_analista(sospechoso: Sospechoso, respuesta: str) -> str:
    """Arma el prompt con el que el analista revisa una respuesta del sospechoso.

    Solo le pasamos los secretos del sospechoso interrogado: menos texto,
    menos confusión y ninguna chance de "revelar" secretos ajenos.
    """
    criterios = "\n".join(f"- {s.id}: {s.criterio_revelacion}" for s in sospechoso.secretos)
    return f"""\
Sos el asistente silencioso de un detective en un juego de misterio.
Leé la última respuesta del sospechoso y decidí cuáles de sus secretos quedaron
revelados EN ESA RESPUESTA, aunque sea a medias o a regañadientes.

Sospechoso: {sospechoso.nombre}
Secretos posibles (id: criterio para considerarlo revelado):
{criterios}

Última respuesta del sospechoso:
\"\"\"{respuesta}\"\"\"

Reglas:
- Marcá un secreto solo si esta respuesta lo dice o lo admite.
- Negar o esquivar NO cuenta como revelación.
- Si no se reveló ninguno, devolvé la lista vacía."""
