"""El registro de casos jugables.

Cada módulo hermano (``calafate.py``, ``huemul.py``, ...) define UN ``Caso``
como dato — ver ``caso_calafate.caso`` para el modelo y las reglas de
consistencia interna (un culpable, secretos sin ids repetidos). Acá los
juntamos en un solo diccionario, indexado por ``Caso.id``, que es lo que
consumen el CLI y el servidor web para armar el selector de casos.

⚠️ SPOILER: importar estos módulos y leer sus datos revela al culpable de
cada caso. Jugá antes de curiosear.
"""

from caso_calafate.caso import Caso
from caso_calafate.casos.andesita import CASO_ANDESITA
from caso_calafate.casos.calafate import CASO_CALAFATE
from caso_calafate.casos.chaltentres import CASO_CHALTEN_III
from caso_calafate.casos.esquel import CASO_ESQUEL
from caso_calafate.casos.huemul import CASO_HUEMUL
from caso_calafate.casos.nahuel import CASO_NAHUEL
from caso_calafate.casos.penitentes import CASO_PENITENTES
from caso_calafate.casos.piltriquitron import CASO_PILTRIQUITRON
from caso_calafate.casos.rionegro import CASO_RIO_NEGRO_I
from caso_calafate.casos.tromen import CASO_TROMEN
from caso_calafate.casos.viedma import CASO_VIEDMA

_TODOS = [
    CASO_CALAFATE,
    CASO_HUEMUL,
    CASO_PENITENTES,
    CASO_NAHUEL,
    CASO_CHALTEN_III,
    CASO_ANDESITA,
    CASO_TROMEN,
    CASO_RIO_NEGRO_I,
    CASO_ESQUEL,
    CASO_VIEDMA,
    CASO_PILTRIQUITRON,
]


def _armar_registro(casos: list[Caso]) -> dict[str, Caso]:
    """Indexa los casos por id y confirma que no haya dos con el mismo id."""
    registro: dict[str, Caso] = {}
    for caso in casos:
        if caso.id in registro:
            raise ValueError(f"hay dos casos con el id {caso.id!r}")
        registro[caso.id] = caso
    return registro


CASOS: dict[str, Caso] = _armar_registro(_TODOS)
