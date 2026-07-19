/* pixelart.js — el puente entre pixelart.py y los <canvas> de la cámara.
 *
 * El servidor manda el arte COMO TEXTO (GET /api/retratos): una paleta
 * letra → color y cada retrato como base + capas de animación. Acá se pinta
 * cada capa pixel por pixel con fillRect, al tamaño real del arte (80×96);
 * el escalado grande lo hace CSS con image-rendering: pixelated.
 *
 * La jugada fina es la ANIMACIÓN: cada capa (párpado, boca cerrada, boca
 * abierta) va en su propio <canvas> apilado, con las MISMAS clases CSS que
 * traían los grupos de los SVG de retratos.js. Las reglas de base.css que
 * hacían parpadear y hablar a los SVG (.parpado, .boca-cerrada,
 * .boca-abierta, .hablando) animan estos canvas sin cambiar una línea.
 *
 * Si el arte pixel no llega (o el caso trae un sospechoso sin retrato), se
 * cae al retrato SVG de siempre: mejor la versión vieja que una cámara rota.
 */

import { api } from "./api.js";
import { delayParpadeo, retrato as retratoSVG } from "./retratos.js";

let DATOS = null; // {paleta, transparente, ancho, alto, retratos}

/** Pide el arte al servidor; sin él, retratoPixel() cae al SVG. */
export async function cargarRetratos() {
  try {
    DATOS = await api.retratos();
  } catch {
    DATOS = null;
  }
}

/** Pinta una grilla de texto en un canvas, un fillRect por pixel. */
function pintar(canvas, filas) {
  canvas.width = filas[0].length;
  canvas.height = filas.length;
  const contexto = canvas.getContext("2d");
  for (let y = 0; y < filas.length; y++) {
    for (let x = 0; x < filas[y].length; x++) {
      const letra = filas[y][x];
      if (letra === DATOS.transparente) continue;
      contexto.fillStyle = DATOS.paleta[letra];
      contexto.fillRect(x, y, 1, 1);
    }
  }
}

/** Una capa de animación: canvas chico, posicionado en porcentajes para que
 * acompañe al retrato a cualquier tamaño. */
function capa(nombre, datos) {
  const canvas = document.createElement("canvas");
  canvas.className = nombre.replaceAll("_", "-"); // boca_cerrada → boca-cerrada
  pintar(canvas, datos.filas);
  canvas.style.left = `${(datos.x / DATOS.ancho) * 100}%`;
  canvas.style.top = `${(datos.y / DATOS.alto) * 100}%`;
  canvas.style.width = `${(datos.filas[0].length / DATOS.ancho) * 100}%`;
  canvas.style.height = `${(datos.filas.length / DATOS.alto) * 100}%`;
  return canvas;
}

/** Devuelve el retrato pixel (un elemento) listo para enchufar en el feed. */
export function retratoPixel(id) {
  const retrato = DATOS?.retratos[id];
  if (!retrato) {
    // Sin arte pixel: el SVG de retratos.js (que además ya resuelve el caso
    // del sospechoso desconocido con su silueta anónima).
    const molde = document.createElement("template");
    molde.innerHTML = retratoSVG(id).trim();
    return molde.content.firstElementChild;
  }

  const marco = document.createElement("div");
  marco.className = `retrato retrato-pixel retrato-${id}`;
  marco.style.aspectRatio = `${DATOS.ancho} / ${DATOS.alto}`;
  marco.style.setProperty("--delay-parpadeo", delayParpadeo(id));

  const base = document.createElement("canvas");
  base.className = "capa-base";
  pintar(base, retrato.base);
  marco.append(base);
  for (const [nombre, datos] of Object.entries(retrato.capas)) {
    marco.append(capa(nombre, datos));
  }
  return marco;
}
