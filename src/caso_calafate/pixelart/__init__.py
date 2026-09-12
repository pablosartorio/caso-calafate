"""El arte pixel de la cámara del CRT: retratos VGA como datos, no como PNGs.

Cada retrato es texto donde un caracter es un pixel: la letra elige un color
de la PALETA y el punto es transparente. Editar el arte es editar strings —
sin programa de dibujo, y el diff de git muestra qué pixel cambió. Es el
mismo truco que usa el juego hermano (cripta-arrayan, ``sprites.py``), pero
en 80×96 y con la paleta DB32 (DawnBringer 32): 32 colores pensados para el
look "VGA de los 90", con rampas de piel y de gris que permiten sombrear.

El frontend pide todo por ``GET /api/retratos`` y pinta cada capa en su
propio <canvas> apilado, con las MISMAS clases CSS que animaban los SVG de
``retratos.js`` — el parpadeo y la charla ya estaban resueltos en base.css
y no se tocaron. Las fichas y el corcho siguen usando los retratos SVG: la
cámara de seguridad es digital y pixelada; la polaroid es una foto.

Este paquete está partido en:

    ``_nucleo``   → la paleta, las medidas del lienzo y el validador
    ``calafate``  → los retratos del caso Calafate (marta, julian, silvia)

Un caso nuevo suma su propio módulo (``pixelart/<caso>.py``) con un dict
``RETRATOS_<CASO>`` y se combina acá abajo — agregar un retrato es crear o
editar un archivo chico, nunca tocar un monolito.
"""

from caso_calafate.pixelart._nucleo import (
    ALTO,
    ANCHO,
    CAPAS_DE_ANIMACION,
    PALETA,
    TRANSPARENTE,
)
from caso_calafate.pixelart._nucleo import exportar_retratos as _exportar_retratos
from caso_calafate.pixelart._nucleo import validar_retratos as _validar_retratos
from caso_calafate.pixelart.arrayanes import RETRATOS_ARRAYANES
from caso_calafate.pixelart.calafate import RETRATOS_CALAFATE
from caso_calafate.pixelart.epuyen import RETRATOS_EPUYEN
from caso_calafate.pixelart.frias import RETRATOS_FRIAS
from caso_calafate.pixelart.jacobacci import RETRATOS_JACOBACCI
from caso_calafate.pixelart.llaollao import RETRATOS_LLAOLLAO
from caso_calafate.pixelart.mascardi import RETRATOS_MASCARDI
from caso_calafate.pixelart.moreno import RETRATOS_MORENO
from caso_calafate.pixelart.pichileufu import RETRATOS_PICHILEUFU
from caso_calafate.pixelart.roca import RETRATOS_ROCA
from caso_calafate.pixelart.tronador import RETRATOS_TRONADOR

# ── Los retratos combinados ──────────────────────────────────────────────────
# Cada módulo de caso aporta su dict; acá se mergean en el único RETRATOS que
# consumen cli.py y web/servidor.py. Un caso nuevo se suma con una línea más.
#
# ⚠️ OJO — este dict es GLOBAL por id de sospechoso, no por caso: si dos casos
# reutilizan el mismo id, el segundo dict pisa al primero acá abajo y uno de
# los dos sospechosos queda con el retrato del OTRO personaje. Pasó con
# "perla" (mascardi/frías) y "ceferino" (epuyen/pichileufu) al agregar la
# ronda de pixel art de 2026-09; se resolvió renombrando el id en frías
# ("perla" → "anzoategui") y en pichileufú ("ceferino" → "aguer") — no es un
# bug de este archivo, sino de que ``casos/*.py`` no garantiza ids únicos
# entre casos (el fallback SVG de ``retratos.js`` tiene el mismo problema de
# fondo). Si en el futuro un caso nuevo reintroduce una colisión, el fix es
# el mismo: renombrar el id en el archivo del caso más nuevo.

RETRATOS: dict[str, dict] = {
    **RETRATOS_CALAFATE,
    **RETRATOS_MASCARDI,
    **RETRATOS_ROCA,
    **RETRATOS_LLAOLLAO,
    **RETRATOS_ARRAYANES,
    **RETRATOS_JACOBACCI,
    **RETRATOS_MORENO,
    **RETRATOS_FRIAS,
    **RETRATOS_TRONADOR,
    **RETRATOS_EPUYEN,
    **RETRATOS_PICHILEUFU,
}

_validar_retratos(RETRATOS)


# ── Export para la web ───────────────────────────────────────────────────────


def exportar_retratos() -> dict:
    """El paquete que viaja por ``GET /api/retratos``: paleta + capas, tal cual.

    La web no recibe imágenes: recibe estos mismos strings y pinta cada capa
    pixel por pixel en su <canvas> (ver ``estatico/js/pixelart.js``)."""
    return _exportar_retratos(RETRATOS)


__all__ = [
    "PALETA",
    "TRANSPARENTE",
    "ANCHO",
    "ALTO",
    "CAPAS_DE_ANIMACION",
    "RETRATOS",
    "exportar_retratos",
]
