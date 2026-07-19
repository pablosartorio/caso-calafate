/* api.js — la única puerta al servidor.
 *
 * Dos canales, calcados del diseño del backend (ver web/servidor.py):
 *
 * - REST con fetch() para todo lo informativo: el caso, el archivo de
 *   partidas, el detalle para retomar, el tablero.
 * - Un WebSocket por partida para las jugadas: por ahí bajan los fragmentos
 *   de la respuesta del sospechoso a medida que el LLM los genera.
 *
 * El resto del frontend no sabe qué es fetch ni WebSocket: usa `api.*` y
 * `conectarPartida()`.
 */

async function traerJSON(url, opciones = {}) {
  const respuesta = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...opciones,
  });
  if (!respuesta.ok) {
    let detalle = "";
    try {
      detalle = (await respuesta.json()).detail ?? "";
    } catch {
      /* sin cuerpo JSON: alcanza con el status */
    }
    const error = new Error(detalle || `el servidor respondió ${respuesta.status}`);
    error.status = respuesta.status;
    throw error;
  }
  return respuesta.status === 204 ? null : respuesta.json();
}

export const api = {
  casos: () => traerJSON("/api/casos"),
  retratos: () => traerJSON("/api/retratos"),
  partidas: () => traerJSON("/api/partidas"),
  crearPartida: (nombre, casoId) =>
    traerJSON("/api/partidas", {
      method: "POST",
      body: JSON.stringify({ nombre, caso_id: casoId }),
    }),
  borrarPartida: (id) => traerJSON(`/api/partidas/${id}`, { method: "DELETE" }),
  detalle: (id) => traerJSON(`/api/partidas/${id}`),
  guardarTablero: (id, tablero) =>
    traerJSON(`/api/partidas/${id}/tablero`, {
      method: "PUT",
      body: JSON.stringify(tablero),
    }),
};

/**
 * Abre el WebSocket de una partida y devuelve un manijita para hablarle.
 *
 * `manejadores` es un objeto {tipo → función}: cada mensaje del servidor trae
 * un campo "tipo" (comienzo, fragmento, turno, veredicto, error) y acá se
 * despacha al manejador que corresponda — el mismo patrón que usa el servidor
 * con las jugadas del cliente.
 *
 * Si la conexión se cae sin que nadie la haya cerrado a propósito, reintenta
 * hasta tres veces con espera creciente y avisa por `alCambiarSenal`.
 */
export function conectarPartida(partidaId, manejadores, alCambiarSenal = () => {}) {
  const protocolo = location.protocol === "https:" ? "wss" : "ws";
  const url = `${protocolo}://${location.host}/ws/partidas/${partidaId}`;

  let ws = null;
  let intentos = 0;
  let cerradaAProposito = false;

  function abrir() {
    ws = new WebSocket(url);

    ws.addEventListener("open", () => {
      if (intentos > 0) alCambiarSenal("recuperada");
      intentos = 0;
    });

    ws.addEventListener("message", (evento) => {
      const mensaje = JSON.parse(evento.data);
      const manejador = manejadores[mensaje.tipo];
      if (manejador) manejador(mensaje);
      else console.warn("mensaje sin manejador:", mensaje);
    });

    ws.addEventListener("close", (evento) => {
      if (cerradaAProposito || evento.code === 4404) return;
      if (intentos < 3) {
        intentos += 1;
        alCambiarSenal("reintentando");
        setTimeout(abrir, 700 * 2 ** intentos);
      } else {
        alCambiarSenal("perdida");
      }
    });
  }

  abrir();

  return {
    enviar(jugada) {
      if (ws?.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify(jugada));
        return true;
      }
      return false;
    },
    cerrar() {
      cerradaAProposito = true;
      ws?.close();
    },
  };
}
