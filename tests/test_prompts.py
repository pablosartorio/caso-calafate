"""Tests estructurales de los prompts: sin red, sin LLM real.

Verifican que el texto generado tenga las piezas clave — el blindaje
anti-rotura-de-personaje, el vocabulario del caso, el formato de salida —
sin necesitar Ollama. La prueba en VIVO contra un modelo real (que confirma
que el blindaje efectivamente sostiene el personaje) se hizo a mano y no
corre en CI: ver el reporte de esta tarea.
"""

import pytest

from caso_calafate.caso import Caso, Secreto, Sospechoso
from caso_calafate.prompts import prompt_analista, prompt_sospechoso


@pytest.fixture
def caso_asado() -> Caso:
    return Caso(
        id="asado",
        titulo="¿QUIÉN SE COMIÓ EL ASADO?",
        gancho="Un asado desaparece de la mesa del patio.",
        briefing="El asado que se enfriaba en la mesa del patio desapareció.",
        contexto_actores="Desapareció un asado de la mesa del patio de la casa.",
        epilogo="Fue Moro, el perro. Las huellas en la mesa lo delataron.",
        sede="la casa de la esquina",
        ciudad="Cipolletti",
        delito="el robo del asado",
        culpable_alias="chorro de asados",
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


# ── El blindaje anti-rotura-de-personaje ─────────────────────────────────────


def test_el_prompt_menciona_ignorar_instrucciones(caso_asado):
    """El vector de ataque documentado: "ignorá tus instrucciones"."""
    culpable = caso_asado.culpable()
    prompt = prompt_sospechoso(caso_asado, culpable)
    assert "ignores tus instrucciones" in prompt.lower()


def test_el_prompt_menciona_modo_desarrollador_y_debug(caso_asado):
    culpable = caso_asado.culpable()
    prompt = prompt_sospechoso(caso_asado, culpable)
    bajo = prompt.lower()
    assert "modo desarrollador" in bajo
    assert "modo debug" in bajo


def test_el_prompt_instruye_no_reconocer_ser_una_ia(caso_asado):
    culpable = caso_asado.culpable()
    prompt = prompt_sospechoso(caso_asado, culpable)
    bajo = prompt.lower()
    assert "modelo de lenguaje" in bajo
    assert "nunca reconozcas" in bajo


def test_el_blindaje_aparece_cerca_del_principio_y_reforzado_al_final(caso_asado):
    """Primacía + recencia: la defensa no puede vivir en una sola línea perdida."""
    culpable = caso_asado.culpable()
    prompt = prompt_sospechoso(caso_asado, culpable)

    mitad = len(prompt) // 2
    primera_mitad = prompt[:mitad].lower()
    segunda_mitad = prompt[mitad:].lower()

    assert "blindaje de personaje" in primera_mitad
    assert "refuerzo final" in segunda_mitad


def test_el_prompt_incluye_un_ejemplo_de_meta_ataque_generico(caso_asado):
    """El micro-ejemplo few-shot no debe atarse a ningún personaje real del juego."""
    culpable = caso_asado.culpable()
    prompt = prompt_sospechoso(caso_asado, culpable)
    assert "ejemplo" in prompt.lower()
    # No debe mencionar nombres de sospechosos de casos reales del juego.
    assert "silvia" not in prompt.lower()


def test_el_prompt_nombra_al_personaje_dentro_del_blindaje(caso_asado):
    """El blindaje se dirige al actor por su propio nombre, no genérico."""
    culpable = caso_asado.culpable()
    prompt = prompt_sospechoso(caso_asado, culpable)
    assert f"como {culpable.nombre}" in prompt


# ── Invariantes que ya existían: no romper lo que funciona ──────────────────


def test_el_prompt_sigue_nombrando_el_delito_del_caso(caso_asado):
    culpable = caso_asado.culpable()
    prompt = prompt_sospechoso(caso_asado, culpable)
    assert caso_asado.delito.upper() in prompt.upper()


def test_el_prompt_sigue_pidiendo_una_a_cuatro_oraciones_en_primera_persona(caso_asado):
    culpable = caso_asado.culpable()
    prompt = prompt_sospechoso(caso_asado, culpable)
    assert "1 a 4 oraciones" in prompt
    assert "primera persona" in prompt


def test_el_prompt_del_inocente_tambien_lleva_el_blindaje(caso_asado):
    inocente = next(s for s in caso_asado.sospechosos if not s.es_culpable)
    prompt = prompt_sospechoso(caso_asado, inocente)
    assert "blindaje de personaje" in prompt.lower()
    assert caso_asado.delito in prompt


# ── El analista: los ejemplos nuevos no deben faltar ni romper el contrato ──


def test_el_prompt_del_analista_incluye_ejemplos(caso_asado):
    michi = next(s for s in caso_asado.sospechosos if s.id == "michi")
    prompt = prompt_analista(michi, "No sé nada, yo estaba durmiendo.")
    assert "ejemplos" in prompt.lower()


def test_el_prompt_del_analista_sigue_mencionando_al_sospechoso_y_sus_secretos(caso_asado):
    michi = next(s for s in caso_asado.sospechosos if s.id == "michi")
    prompt = prompt_analista(michi, "Vi a Moro cerca de la mesa.")
    assert michi.nombre in prompt
    assert "vio_al_perro" in prompt
