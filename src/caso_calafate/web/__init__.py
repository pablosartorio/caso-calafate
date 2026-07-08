"""La interfaz web del juego: el escritorio del detective, en el browser.

El paquete tiene tres piezas:

- ``servidor.py`` — la app FastAPI: REST para consultar, WebSocket para jugar.
- ``partidas.py`` — el registro de partidas guardadas (metadatos + tablero).
- ``estatico/``  — el frontend: HTML, CSS y JavaScript artesanales, sin
  frameworks ni build step, servidos por el mismo proceso.

El motor (``grafo.py`` y compañía) no se tocó para nada: esta es exactamente
la "otra piel" que promete el docstring de ``cli.py``.
"""

from caso_calafate.web.servidor import crear_app, main

__all__ = ["crear_app", "main"]
