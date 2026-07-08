"""Tests de los datos del caso y sus validaciones.

Dos grupos:

1. Que el MODELO de datos rechace casos mal armados (validadores de Pydantic).
2. Que EL CASO REAL cumpla las invariantes que el motor asume. Esto convierte
   errores de contenido ("me olvidé de marcar al culpable") en tests rojos,
   en vez de bugs a mitad de una partida.
"""

import pytest

from caso_calafate.caso import CASO_CALAFATE, Caso, Secreto, Sospechoso


def _sospechoso_minimo(id_: str, es_culpable: bool = False, secretos=None) -> Sospechoso:
    """Helper para armar sospechosos descartables en los tests de validación."""
    return Sospechoso(
        id=id_,
        nombre=id_.capitalize(),
        cargo="cargo",
        personalidad="p",
        coartada="c",
        actitud="a",
        es_culpable=es_culpable,
        secretos=secretos or [],
    )


def _caso_con(sospechosos: list[Sospechoso]) -> Caso:
    return Caso(
        titulo="T",
        briefing="B",
        contexto_actores="C",
        epilogo="E",
        sospechosos=sospechosos,
    )


# ── Validadores del modelo ───────────────────────────────────────────────────


def test_un_caso_sin_culpable_no_se_puede_construir():
    with pytest.raises(ValueError, match="exactamente 1 culpable"):
        _caso_con([_sospechoso_minimo("a"), _sospechoso_minimo("b")])


def test_un_caso_con_dos_culpables_no_se_puede_construir():
    with pytest.raises(ValueError, match="exactamente 1 culpable"):
        _caso_con(
            [
                _sospechoso_minimo("a", es_culpable=True),
                _sospechoso_minimo("b", es_culpable=True),
            ]
        )


def test_ids_de_secretos_repetidos_no_se_permiten():
    secreto = Secreto(id="repetido", pista="p", instruccion_actor="i", criterio_revelacion="c")
    with pytest.raises(ValueError, match="repetidos"):
        _caso_con(
            [
                _sospechoso_minimo("a", es_culpable=True, secretos=[secreto]),
                _sospechoso_minimo("b", secretos=[secreto.model_copy()]),
            ]
        )


# ── Búsqueda de sospechosos ──────────────────────────────────────────────────


def test_buscar_sospechoso_ignora_mayusculas_y_acepta_prefijos(caso_asado):
    assert caso_asado.buscar_sospechoso("MICHI").id == "michi"
    assert caso_asado.buscar_sospechoso("mor").id == "moro"


def test_buscar_sospechoso_ignora_tildes():
    # "Julián" tiene tilde en el caso real; el jugador no debería sufrir por eso.
    assert CASO_CALAFATE.buscar_sospechoso("julian").id == "julian"
    assert CASO_CALAFATE.buscar_sospechoso("JULIÁN").id == "julian"


def test_buscar_sospechoso_devuelve_none_si_no_hay_match(caso_asado):
    assert caso_asado.buscar_sospechoso("nadie") is None
    assert caso_asado.buscar_sospechoso("") is None


# ── Invariantes del caso real ────────────────────────────────────────────────


def test_el_caso_real_tiene_tres_sospechosos_y_un_culpable():
    assert len(CASO_CALAFATE.sospechosos) == 3
    # culpable() explota si no hay ninguno; el validador ya garantizó que hay uno solo.
    assert CASO_CALAFATE.culpable().es_culpable


def test_el_caso_real_es_justo():
    """Reglas de jugabilidad: pistas suficientes y preguntas para encontrarlas."""
    assert CASO_CALAFATE.total_secretos() >= 5, "muy pocas pistas para deducir algo"
    assert CASO_CALAFATE.max_preguntas >= CASO_CALAFATE.total_secretos(), (
        "tiene que haber al menos tantas preguntas como pistas, "
        "o el caso es imposible de resolver completo"
    )
    for sospechoso in CASO_CALAFATE.sospechosos:
        assert sospechoso.secretos, f"{sospechoso.nombre} no tiene ningún secreto que revelar"


def test_los_textos_del_caso_real_no_estan_vacios():
    assert CASO_CALAFATE.briefing.strip()
    assert CASO_CALAFATE.contexto_actores.strip()
    assert CASO_CALAFATE.epilogo.strip()
