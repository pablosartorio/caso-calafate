"""Fixtures compartidas por todos los tests.

La idea central: los tests NUNCA llaman a un LLM real. Usan:

- Un caso de juguete («¿Quién se comió el asado?») independiente del caso
  real — si mañana editás El Caso Calafate, estos tests no se enteran.
- ``FakeListChatModel`` de LangChain como actor: devuelve respuestas fijas.
- Un analista falso hecho con ``RunnableLambda``: devuelve el
  ``SecretosRevelados`` que el test quiera.

Con eso, los tests corren en milisegundos, sin API key y sin internet.
"""

import pytest
from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_core.runnables import RunnableLambda

from caso_calafate.caso import Caso, Secreto, Sospechoso
from caso_calafate.prompts import SecretosRevelados


@pytest.fixture
def caso_asado() -> Caso:
    """Un caso mínimo de dos sospechosos para testear el motor."""
    return Caso(
        titulo="¿QUIÉN SE COMIÓ EL ASADO?",
        briefing="El asado que se enfriaba en la mesa del patio desapareció.",
        contexto_actores="Desapareció un asado de la mesa del patio de la casa.",
        epilogo="Fue Moro, el perro. Las huellas en la mesa lo delataron.",
        max_preguntas=5,
        sospechosos=[
            Sospechoso(
                id="moro",
                nombre="Moro",
                cargo="perro de la casa",
                personalidad="ansioso y glotón",
                coartada="Dice que dormía en la cucha.",
                actitud="se hace el distraído",
                es_culpable=True,
                secretos=[
                    Secreto(
                        id="huellas_patio",
                        pista="Hay huellas de pata sobre la mesa del patio.",
                        instruccion_actor="Si te preguntan por la mesa, admitís que te subiste.",
                        criterio_revelacion="Admite que se subió a la mesa.",
                    )
                ],
            ),
            Sospechoso(
                id="michi",
                nombre="Michi",
                cargo="gata de la casa",
                personalidad="indiferente",
                coartada="Dice que tomaba sol en el techo.",
                actitud="desprecio absoluto",
                secretos=[
                    Secreto(
                        id="vio_al_perro",
                        pista="Michi vio a Moro rondando la mesa antes de la siesta.",
                        instruccion_actor="Si te preguntan qué viste, contás lo de Moro.",
                        criterio_revelacion="Dice que vio a Moro cerca de la mesa.",
                    )
                ],
            ),
        ],
    )


@pytest.fixture
def actor_loro() -> FakeListChatModel:
    """Actor falso: repite respuestas enlatadas en orden (y vuelve a empezar)."""
    return FakeListChatModel(
        responses=["Yo no fui.", "Estaba en otra parte.", "No vi nada, lo juro."]
    )


@pytest.fixture
def analista_fijo():
    """Fábrica de analistas falsos: ``analista_fijo(["id1"])`` siempre revela esos ids.

    Patrón "factory as fixture" de pytest: la fixture devuelve una función,
    y cada test la llama con los ids que necesita para su escenario.
    """

    def _crear(ids: list[str]) -> RunnableLambda:
        return RunnableLambda(lambda _prompt: SecretosRevelados(ids=list(ids)))

    return _crear
