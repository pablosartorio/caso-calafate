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
from caso_calafate.casos.arrayanes import CASO_ARRAYANES
from caso_calafate.casos.calafate import CASO_CALAFATE
from caso_calafate.casos.catedral import CASO_CATEDRAL
from caso_calafate.casos.chaltentres import CASO_CHALTEN_III
from caso_calafate.casos.epuyen import CASO_EPUYEN
from caso_calafate.casos.esquel import CASO_ESQUEL
from caso_calafate.casos.frias import CASO_FRIAS
from caso_calafate.casos.huemul import CASO_HUEMUL
from caso_calafate.casos.jacobacci import CASO_JACOBACCI
from caso_calafate.casos.llaollao import CASO_LLAO_LLAO
from caso_calafate.casos.mascardi import CASO_MASCARDI
from caso_calafate.casos.moreno import CASO_MORENO
from caso_calafate.casos.nahuel import CASO_NAHUEL
from caso_calafate.casos.penitentes import CASO_PENITENTES
from caso_calafate.casos.pichileufu import CASO_PICHILEUFU
from caso_calafate.casos.piltriquitron import CASO_PILTRIQUITRON
from caso_calafate.casos.rionegro import CASO_RIO_NEGRO_I
from caso_calafate.casos.roca import CASO_ROCA
from caso_calafate.casos.tromen import CASO_TROMEN
from caso_calafate.casos.tronador import CASO_TRONADOR
from caso_calafate.casos.viedma import CASO_VIEDMA

# Los once originales, más once nuevos basados en cuentos y novelas policiales
# argentinas (ver el docstring de cada archivo nuevo para el homenaje puntual).
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
    CASO_LLAO_LLAO,
    CASO_MASCARDI,
    CASO_ROCA,
    CASO_CATEDRAL,
    CASO_TRONADOR,
    CASO_FRIAS,
    CASO_PICHILEUFU,
    CASO_JACOBACCI,
    CASO_ARRAYANES,
    CASO_MORENO,
    CASO_EPUYEN,
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

# Los 10 casos con homenaje literario real, profundizados a fondo (personajes,
# secretos encadenados, veracidad revisada contra la obra que homenajean) y
# con pixel art propio — son los únicos que el selector de casos (CLI y web)
# le ofrece al jugador. Los otros 12 (el Calafate original y los casos de la
# primera tanda) NO se borraron ni se sacaron del registro: siguen en `CASOS`
# completo, jugables por id si alguien los pide a mano, y quedan disponibles
# para una futura ronda de profundización. Un caso nuevo se suma a este
# selector agregando su id acá, no editando `_TODOS`.
CASOS_VISIBLES: dict[str, Caso] = {
    id_: CASOS[id_]
    for id_ in (
        "mascardi",
        "roca",
        "llaollao",
        "arrayanes",
        "jacobacci",
        "moreno",
        "frias",
        "tronador",
        "epuyen",
        "pichileufu",
    )
}
