"""El núcleo del arte pixel: la paleta DB32, las medidas del lienzo y el
validador de contrato.

Este módulo no conoce ningún retrato en particular — los retratos viven en
un módulo por caso (ver ``pixelart/calafate.py``) y se combinan en
``pixelart/__init__.py``, que es quien corre el validador sobre el diccionario
final. Separar el núcleo así permite que agregar un caso nuevo sea agregar un
archivo chico, sin tocar la paleta ni el validador.
"""

# ── La paleta (DB32) ─────────────────────────────────────────────────────────
# Letra → hex, nemotécnicas en lo posible: k=negro (key), v=violeta nocturno,
# m=morado vino, M=marrón oscuro, B=marrón (Brown), o=naranja, t=tostado,
# F=piel (Flesh), y=amarillo, L=lima, g=verde (green), E=esmeralda, d=verde
# oscuro (dark), O=oliva, Z=pizarra, z=azul noche, A=azul mar, a=azul,
# C=celeste, c=cian, e=escarcha, w=blanco (white), S=plata (Silver),
# s=gris piedra, G=gris (Gray), h=humo, p=púrpura, r=rojo, R=rosado,
# P=rosa (Pink), n=oliva claro, u=ocre. El punto: transparente.

PALETA: dict[str, str] = {
    "k": "#000000", "v": "#222034", "m": "#45283c", "M": "#663931",
    "B": "#8f563b", "o": "#df7126", "t": "#d9a066", "F": "#eec39a",
    "y": "#fbf236", "L": "#99e550", "g": "#6abe30", "E": "#37946e",
    "d": "#4b692f", "O": "#524b24", "Z": "#323c39", "z": "#3f3f74",
    "A": "#306082", "a": "#5b6ee1", "C": "#639bff", "c": "#5fcde4",
    "e": "#cbdbfc", "w": "#ffffff", "S": "#9badb7", "s": "#847e87",
    "G": "#696a6a", "h": "#595652", "p": "#76428a", "r": "#ac3232",
    "R": "#d95763", "P": "#d77bba", "n": "#8f974a", "u": "#8a6f30",
}

TRANSPARENTE = "."

ANCHO, ALTO = 80, 96  # tamaño de la base; las capas son recortes posicionados

CAPAS_DE_ANIMACION = ("parpado", "boca_cerrada", "boca_abierta")


def validar_retratos(retratos: dict[str, dict]) -> None:
    """Control de calidad del arte, al importar: un retrato torcido explota
    acá con nombre y apellido, no como un pixel corrido en plena partida."""
    validos = set(PALETA) | {TRANSPARENTE}
    for nombre, retrato in retratos.items():
        base = retrato["base"]
        if len(base) != ALTO or {len(f) for f in base} != {ANCHO}:
            raise ValueError(f"la base de {nombre!r} no mide {ANCHO}×{ALTO}")
        for numero, fila in enumerate(base):
            if TRANSPARENTE in fila:
                raise ValueError(f"la base de {nombre!r} tiene huecos (fila {numero})")
            if intrusos := set(fila) - validos:
                raise ValueError(f"la base de {nombre!r}, fila {numero}: chars {intrusos!r}")
        if faltan := set(CAPAS_DE_ANIMACION) - set(retrato["capas"]):
            raise ValueError(f"a {nombre!r} le faltan capas: {faltan}")
        for capa, datos in retrato["capas"].items():
            filas = datos["filas"]
            anchos = {len(f) for f in filas}
            if len(anchos) != 1:
                raise ValueError(f"{nombre!r}/{capa}: filas de anchos distintos: {anchos}")
            if intrusos := set("".join(filas)) - validos:
                raise ValueError(f"{nombre!r}/{capa}: chars {intrusos!r}")
            if datos["x"] + anchos.pop() > ANCHO or datos["y"] + len(filas) > ALTO:
                raise ValueError(f"{nombre!r}/{capa}: la capa se sale del retrato")


def exportar_retratos(retratos: dict[str, dict]) -> dict:
    """El paquete que viaja por ``GET /api/retratos``: paleta + capas, tal cual.

    La web no recibe imágenes: recibe estos mismos strings y pinta cada capa
    pixel por pixel en su <canvas> (ver ``estatico/js/pixelart.js``)."""
    return {
        "paleta": PALETA,
        "transparente": TRANSPARENTE,
        "ancho": ANCHO,
        "alto": ALTO,
        "retratos": retratos,
    }
