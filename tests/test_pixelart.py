"""Tests del arte pixel: el contrato entre los datos y la cámara del CRT.

Mismo espíritu que los tests de sprites del juego hermano (cripta-arrayan):
el contrato es por NOMBRE — cada sospechoso del caso real tiene un retrato
con su mismo id — y si un retrato pierde una fila o le aparece una letra
fuera de la paleta, explota acá un test con nombre y apellido, no la cámara
en plena partida. El validador ya corre al importar; estos tests lo dejan
por escrito.
"""

from caso_calafate.casos import CASOS
from caso_calafate.casos.calafate import CASO_CALAFATE
from caso_calafate.pixelart import (
    ALTO,
    ANCHO,
    CAPAS_DE_ANIMACION,
    PALETA,
    RETRATOS,
    TRANSPARENTE,
    exportar_retratos,
)

# Los casos que YA tienen arte pixel propio (los demás siguen con el
# fallback SVG de ``retratos.js`` — no rompen nada, solo no tienen pixel art
# todavía). Un caso nuevo se suma a esta lista cuando se le agrega su
# ``pixelart/<caso>.py``.
CASOS_CON_PIXEL_ART = [
    "calafate", "mascardi", "roca", "llaollao", "arrayanes", "jacobacci",
    "moreno", "frias", "tronador", "epuyen", "pichileufu",
]


def test_cada_sospechoso_del_caso_calafate_tiene_retrato():
    """La clave del retrato ES el id del sospechoso: la convención que evita
    mantener un mapeo aparte, vigilada acá."""
    assert set(RETRATOS) >= {s.id for s in CASO_CALAFATE.sospechosos}


def test_cada_sospechoso_de_los_casos_con_pixel_art_tiene_retrato():
    """Ronda de arte de 10 casos nuevos: por cada uno, sus cinco sospechosos
    tienen que estar en RETRATOS. (``RETRATOS`` es global por id — ver el
    comentario en ``pixelart/__init__.py`` sobre qué hacer si un caso nuevo
    reintroduce una colisión de ids entre casos distintos.)"""
    for caso_id in CASOS_CON_PIXEL_ART:
        ids_sospechosos = {s.id for s in CASOS[caso_id].sospechosos}
        faltantes = ids_sospechosos - set(RETRATOS)
        assert not faltantes, f"{caso_id}: sin retrato para {faltantes}"


def test_las_bases_son_opacas_y_del_tamano_de_la_camara():
    """La base es la foto quieta: 80×96, sin huecos y solo colores DB32."""
    for nombre, retrato in RETRATOS.items():
        base = retrato["base"]
        assert len(base) == ALTO, f"{nombre}: faltan filas"
        assert all(len(fila) == ANCHO for fila in base), f"{nombre}: filas disparejas"
        assert all(TRANSPARENTE not in fila for fila in base), f"{nombre}: huecos en la base"
        assert all(set(fila) <= set(PALETA) for fila in base), f"{nombre}: color desconocido"


def test_las_capas_de_animacion_estan_y_entran_en_el_retrato():
    """Sin párpado o sin bocas no hay parpadeo ni charla: las tres capas son
    obligatorias, y su recorte tiene que caer adentro de la base."""
    for nombre, retrato in RETRATOS.items():
        assert set(retrato["capas"]) == set(CAPAS_DE_ANIMACION), f"{nombre}: capas incompletas"
        for capa, datos in retrato["capas"].items():
            filas = datos["filas"]
            assert filas, f"{nombre}/{capa}: capa vacía"
            assert len({len(f) for f in filas}) == 1, f"{nombre}/{capa}: filas disparejas"
            assert datos["x"] + len(filas[0]) <= ANCHO, f"{nombre}/{capa}: se sale a lo ancho"
            assert datos["y"] + len(filas) <= ALTO, f"{nombre}/{capa}: se sale a lo alto"
            colores = set("".join(filas))
            assert colores <= set(PALETA) | {TRANSPARENTE}, f"{nombre}/{capa}: color desconocido"


def test_el_export_para_la_web_es_el_mismo_arte():
    paquete = exportar_retratos()
    assert paquete["paleta"] == PALETA
    assert paquete["retratos"] is RETRATOS  # sin copias: una sola fuente
    assert paquete["transparente"] == TRANSPARENTE
    assert (paquete["ancho"], paquete["alto"]) == (ANCHO, ALTO)
