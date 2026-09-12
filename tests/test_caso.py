"""Tests de los datos del caso y sus validaciones.

Dos grupos:

1. Que el MODELO de datos rechace casos mal armados (validadores de Pydantic).
2. Que EL CASO REAL cumpla las invariantes que el motor asume. Esto convierte
   errores de contenido ("me olvidé de marcar al culpable") en tests rojos,
   en vez de bugs a mitad de una partida.
"""

import pytest

from caso_calafate.caso import Caso, Secreto, Sospechoso, buscar_caso
from caso_calafate.casos import CASOS
from caso_calafate.casos.calafate import CASO_CALAFATE


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
        id="t",
        titulo="T",
        gancho="G",
        briefing="B",
        contexto_actores="C",
        epilogo="E",
        sede="S",
        ciudad="Ciudad",
        delito="el hecho",
        culpable_alias="responsable",
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


# ── El registro de casos ─────────────────────────────────────────────────────


def test_hay_al_menos_once_casos_y_ninguno_repite_id():
    assert len(CASOS) >= 11
    assert list(CASOS) == [c.id for c in CASOS.values()]  # la clave ES Caso.id


# ── Invariantes de CADA caso jugable ─────────────────────────────────────────
# Parametrizado sobre todo el registro: un caso nuevo queda auto-verificado
# (pistas suficientes, preguntas alcanzan, textos no vacíos, un solo culpable)
# sin escribir un test por caso.


@pytest.mark.parametrize("caso", CASOS.values(), ids=CASOS.keys())
def test_cada_caso_tiene_entre_tres_y_cinco_sospechosos_y_un_culpable(caso: Caso):
    # Los once casos originales tienen 3; los basados en cuentos policiales
    # argentinos (ver casos/llaollao.py y hermanos) piden 5.
    assert 3 <= len(caso.sospechosos) <= 5
    # culpable() explota si no hay ninguno; el validador ya garantizó que hay uno solo.
    assert caso.culpable().es_culpable


@pytest.mark.parametrize("caso", CASOS.values(), ids=CASOS.keys())
def test_cada_caso_es_justo(caso: Caso):
    """Reglas de jugabilidad: pistas suficientes y preguntas para encontrarlas."""
    assert caso.total_secretos() >= 5, "muy pocas pistas para deducir algo"
    assert caso.max_preguntas >= caso.total_secretos(), (
        "tiene que haber al menos tantas preguntas como pistas, "
        "o el caso es imposible de resolver completo"
    )
    for sospechoso in caso.sospechosos:
        assert sospechoso.secretos, f"{sospechoso.nombre} no tiene ningún secreto que revelar"


@pytest.mark.parametrize("caso", CASOS.values(), ids=CASOS.keys())
def test_los_textos_de_cada_caso_no_estan_vacios(caso: Caso):
    assert caso.titulo.strip()
    assert caso.gancho.strip()
    assert caso.briefing.strip()
    assert caso.contexto_actores.strip()
    assert caso.epilogo.strip()


# ── El vocabulario de cada caso ──────────────────────────────────────────────
# Los prompts, el veredicto y el diario arman frases con estos campos. Si un
# caso los escribe mal (un artículo de más, un alias en plural), las frases
# salen torcidas en la partida; acá salen en rojo.


@pytest.mark.parametrize("caso", CASOS.values(), ids=CASOS.keys())
def test_cada_caso_trae_su_vocabulario(caso: Caso):
    assert caso.sede.strip()
    assert caso.ciudad.strip()
    assert caso.delito.strip()
    assert caso.culpable_alias.strip()


@pytest.mark.parametrize("caso", CASOS.values(), ids=CASOS.keys())
def test_el_delito_encaja_en_las_frases_del_juego(caso: Caso):
    """``delito`` se usa como «cometiste ___» y «confesó ___»: necesita
    artículo y no puede empezar con mayúscula ni terminar en punto."""
    primera = caso.delito.split()[0]
    assert primera in ("el", "la", "los", "las"), f"«{caso.delito}» no arranca con artículo"
    assert not caso.delito.endswith("."), "el delito se incrusta en una frase, sin punto final"


@pytest.mark.parametrize("caso", CASOS.values(), ids=CASOS.keys())
def test_el_alias_del_culpable_encaja_en_las_frases_del_juego(caso: Caso):
    """``culpable_alias`` se usa como «el ___ sigue libre»: sustantivo pelado,
    sin artículo adelante."""
    primera = caso.culpable_alias.split()[0]
    assert primera not in ("el", "la", "un", "una"), "el alias va sin artículo"
    assert caso.culpable_alias == caso.culpable_alias.lower(), "el alias va en minúscula"


def test_ningun_caso_hereda_el_vocabulario_del_calafate():
    """El bug que motivó estos campos: todo caso hablaba del sabotaje del
    CALAFATE-1, jugara lo que jugara."""
    for caso in CASOS.values():
        if caso.id == "calafate":
            continue
        assert "CALAFATE" not in caso.delito
        assert "sabotaje del satélite" not in caso.delito


# ── Búsqueda de casos (la usa el selector del CLI) ───────────────────────────


def test_buscar_caso_acepta_id_titulo_tildes_y_prefijos():
    catalogo = list(CASOS.values())
    assert buscar_caso(catalogo, "huemul").id == "huemul"
    assert buscar_caso(catalogo, "PILTRIQUITRÓN").id == "piltriquitron"  # con tilde, como la tabla
    assert buscar_caso(catalogo, "el caso huemul").id == "huemul"        # el título entero
    assert buscar_caso(catalogo, "río negro").id == "rio-negro-i"        # el título sin "el caso"
    assert buscar_caso(catalogo, "pilt").id == "piltriquitron"           # un prefijo del id


def test_buscar_caso_devuelve_none_si_no_hay_match():
    catalogo = list(CASOS.values())
    assert buscar_caso(catalogo, "el caso del asado") is None
    assert buscar_caso(catalogo, "   ") is None


# ── Campos nuevos: defaults y que no rompan los 22 casos reales ─────────────


def test_secreto_tiene_defaults_de_es_entrada_y_certeza():
    secreto = Secreto(id="s", pista="p", instruccion_actor="i", criterio_revelacion="c")
    assert secreto.es_entrada is False
    assert secreto.certeza is None


def test_sospechoso_tiene_default_de_reaccion_acusacion_fallida():
    assert _sospechoso_minimo("a", es_culpable=True).reaccion_acusacion_fallida is None


@pytest.mark.parametrize("caso", CASOS.values(), ids=CASOS.keys())
def test_los_22_casos_reales_siguen_validando_con_los_campos_nuevos(caso: Caso):
    """Los campos nuevos son opcionales: ningún caso existente los completa
    todavía, así que todos tienen que seguir en sus defaults."""
    for sospechoso in caso.sospechosos:
        assert sospechoso.reaccion_acusacion_fallida is None
        for secreto in sospechoso.secretos:
            assert secreto.es_entrada is False
            assert secreto.certeza is None


# ── Caso.secretos_no_revelados ───────────────────────────────────────────────


def test_secretos_no_revelados_excluye_los_descubiertos(caso_asado):
    todos = caso_asado.secretos_no_revelados([])
    assert {s.id for s in todos} == {"huellas_patio", "vio_al_perro"}

    faltantes = caso_asado.secretos_no_revelados(["vio_al_perro"])
    assert [s.id for s in faltantes] == ["huellas_patio"]


def test_secretos_no_revelados_vacio_cuando_ya_se_encontraron_todos(caso_asado):
    assert caso_asado.secretos_no_revelados(["huellas_patio", "vio_al_perro"]) == []


def test_secretos_no_revelados_ignora_ids_de_descubiertos_que_no_existen(caso_asado):
    """Un id que no corresponde a ningún secreto (alucinado, de otro caso) no
    debería hacer explotar nada ni filtrar de más."""
    faltantes = caso_asado.secretos_no_revelados(["inventado"])
    assert {s.id for s in faltantes} == {"huellas_patio", "vio_al_perro"}
