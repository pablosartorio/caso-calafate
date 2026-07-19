"""Tests del fondo de escena: mismo espíritu que test_pixelart.py — el
validador ya corre al importar, esto lo deja por escrito con nombre propio."""

from caso_calafate.fondo import ALTO_FONDO, ANCHO_FONDO, FONDO, exportar_fondo
from caso_calafate.pixelart import PALETA


def test_el_fondo_mide_lo_que_declara_y_no_tiene_huecos():
    assert len(FONDO) == ALTO_FONDO, "faltan filas"
    assert all(len(fila) == ANCHO_FONDO for fila in FONDO), "filas disparejas"
    assert all(set(fila) <= set(PALETA) for fila in FONDO), "color fuera de paleta"


def test_el_export_para_la_web_es_el_mismo_arte():
    paquete = exportar_fondo()
    assert paquete["paleta"] == PALETA
    assert paquete["filas"] is FONDO  # sin copias: una sola fuente
    assert (paquete["ancho"], paquete["alto"]) == (ANCHO_FONDO, ALTO_FONDO)
