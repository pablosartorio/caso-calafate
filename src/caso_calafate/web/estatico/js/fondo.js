/* fondo.js — el puente entre fondo.py y el fondo del archivo de expedientes.
 *
 * El servidor manda la escena COMO TEXTO (GET /api/fondo): paleta + una
 * grilla de caracteres, igual que pixelart.js con los retratos. Acá se pinta
 * una sola vez en un <canvas> descartable, se vuelca a data URL con
 * toDataURL(), y esa URL queda en la variable CSS --fondo-escena — así el
 * "cover" y el resto del recorte lo sigue resolviendo CSS de siempre, sin
 * que ningún otro módulo tenga que saber que el fondo es pixel art.
 *
 * Si el pedido falla, la variable simplemente no se define y el CSS cae al
 * fondo de gradientes de toda la vida (ver pantallas.css).
 */

import { api } from "./api.js";

export async function cargarFondo() {
  let datos;
  try {
    datos = await api.fondo();
  } catch {
    return;
  }

  const canvas = document.createElement("canvas");
  canvas.width = datos.ancho;
  canvas.height = datos.alto;
  const contexto = canvas.getContext("2d");
  for (let y = 0; y < datos.filas.length; y++) {
    const fila = datos.filas[y];
    for (let x = 0; x < fila.length; x++) {
      contexto.fillStyle = datos.paleta[fila[x]];
      contexto.fillRect(x, y, 1, 1);
    }
  }

  document.documentElement.style.setProperty(
    "--fondo-escena",
    `url(${canvas.toDataURL("image/png")})`
  );
}
