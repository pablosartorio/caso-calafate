/* avisos.js — los papelitos volantes de arriba a la derecha.
 *
 * Un solo tipo de notificación para todo el juego: un papel con chincheta.
 * Las pistas usan letra manuscrita, los errores tinta roja. El contenido
 * SIEMPRE entra por textContent — nunca innerHTML — porque puede venir de
 * un LLM o del jugador, y esta capa no confía en nadie.
 */

import { $ } from "./estado.js";

export function avisar(texto, { tipo = "", titulo = "", duracion = 5200 } = {}) {
  const aviso = document.createElement("div");
  aviso.className = `aviso ${tipo ? `aviso-${tipo}` : ""}`;

  if (titulo) {
    const cabeza = document.createElement("span");
    cabeza.className = "aviso-titulo";
    cabeza.textContent = titulo;
    aviso.append(cabeza);
  }
  aviso.append(document.createTextNode(texto));

  $("#avisos").append(aviso);
  setTimeout(() => {
    aviso.classList.add("aviso-saliendo");
    aviso.addEventListener("animationend", () => aviso.remove(), { once: true });
  }, duracion);
}
