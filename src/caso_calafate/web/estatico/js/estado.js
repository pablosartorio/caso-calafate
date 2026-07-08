/* estado.js — el estado compartido del frontend, más un canal de avisos.
 *
 * La versión artesanal de lo que en un framework sería un store: un objeto
 * plano que cualquier módulo puede leer, y un mini bus de eventos para que
 * los módulos se avisen cosas sin importarse entre sí (main.js escucha las
 * jugadas que emite escritorio.js, por ejemplo — así no hay imports
 * circulares).
 *
 * Ojo con el paralelismo: este estado es la COPIA VISUAL de la partida. La
 * verdad vive en el checkpointer del servidor; acá solo se refleja lo que
 * llega por REST y WebSocket.
 */

export const estado = {
  caso: null,           // lo que devuelve GET /api/caso (título, sospechosos…)
  partidaId: null,      // la partida abierta en pantalla
  detalle: null,        // lo que devolvió GET /api/partidas/<id> al entrar
  conversaciones: {},   // historial por sospechoso, actualizado en vivo
  pistas: [],           // las pistas descubiertas [{id, pista}], en orden
  seleccionado: null,   // el sospechoso frente a la cámara (objeto del caso)
  ocupado: false,       // hay una pregunta en vuelo: la máquina se traba
  tablero: null,        // notas / fotos / conexiones del corcho
};

const escuchas = new Map();

/** Suscribe una función a un evento del bus. */
export function escuchar(evento, funcion) {
  if (!escuchas.has(evento)) escuchas.set(evento, []);
  escuchas.get(evento).push(funcion);
}

/** Emite un evento con datos; los que escuchan, reaccionan. */
export function emitir(evento, datos) {
  for (const funcion of escuchas.get(evento) ?? []) funcion(datos);
}

/** Atajo para document.querySelector, porque se usa en todos lados. */
export const $ = (selector) => document.querySelector(selector);
