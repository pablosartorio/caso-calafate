/* main.js — el director de orquesta.
 *
 * Es el único módulo que conoce a todos los demás. Sus tres trabajos:
 *
 * 1. ARRANCAR: pedir el caso, armar el escritorio, enganchar el audio.
 * 2. RUTEAR: el hash de la URL decide la pantalla (#/archivo o
 *    #/partida/<id>) — la URL ES el estado de navegación, así el F5 y el
 *    botón de atrás funcionan gratis.
 * 3. TRADUCIR: las jugadas que emite la interfaz van al WebSocket, y los
 *    mensajes del WebSocket vuelven a la interfaz. Todo el protocolo con el
 *    servidor pasa por acá, en un solo lugar.
 */

import { api, conectarPartida } from "./api.js";
import { avisar } from "./avisos.js";
import * as crt from "./crt.js";
import * as escritorio from "./escritorio.js";
import { $, escuchar, estado } from "./estado.js";
import {
  mostrarArchivo,
  mostrarBriefing,
  mostrarDiario,
  prepararDiario,
  prepararSelectorDeCasos,
} from "./pantallas.js";
import { cargarFondo } from "./fondo.js";
import { cargarRetratos } from "./pixelart.js";
import { radioEncendida, sonido } from "./sonido.js";
import { abrirTablero, prepararTablero } from "./tablero.js";

let conexion = null;        // el WebSocket de la partida abierta
let veredictoActual = null; // el veredicto recibido, para releer el diario

/* ── Arranque ────────────────────────────────────────────────────────────── */

async function arrancar() {
  try {
    const { motor, casos } = await api.casos();
    estado.motor = motor;
    estado.casosDisponibles = casos;
  } catch {
    avisar("no pude hablar con el servidor — ¿está corriendo detective-web?", {
      tipo: "error",
      duracion: 60000,
    });
    return;
  }

  if (estado.motor === "fake") $("#aviso-fake").hidden = false;

  // El arte pixel de la cámara y el fondo de escena; si fallan, el CRT cae
  // a los retratos SVG y el archivo cae a su fondo de gradientes de siempre.
  await Promise.all([cargarRetratos(), cargarFondo()]);

  crt.iniciarCRT();
  escritorio.prepararEscritorio();
  prepararTablero();
  prepararDiario();
  prepararSelectorDeCasos();
  prepararRadio();

  // El audio recién puede nacer con un gesto del usuario (política de
  // autoplay de los browsers): el primer click o tecla lo despierta.
  const despertarAudio = () => sonido.activar();
  window.addEventListener("pointerdown", despertarAudio, { once: true });
  window.addEventListener("keydown", despertarAudio, { once: true });

  conectarBus();
  window.addEventListener("hashchange", rutear);
  await rutear();
}

function prepararRadio() {
  const boton = $("#boton-radio");
  const pintar = () => {
    boton.setAttribute("aria-pressed", String(radioEncendida()));
    $("#radio-estado").textContent = radioEncendida() ? "encendida" : "apagada";
  };
  pintar();
  boton.addEventListener("click", () => {
    sonido.radio(!radioEncendida());
    pintar();
  });
}

/* ── El bus: la interfaz emite, main traduce ─────────────────────────────── */

function conectarBus() {
  escuchar("jugada:interrogar", (jugada) => {
    // Espejo local de la conversación (para re-sintonizar sin ir al server).
    (estado.conversaciones[jugada.sospechoso] ??= []).push({
      quien: "detective",
      texto: jugada.pregunta,
    });
    crt.preguntar(jugada.pregunta);
    enviarOAvisar({ tipo: "interrogar", ...jugada });
  });

  escuchar("jugada:acusar", (jugada) => {
    enviarOAvisar({ tipo: "acusar", ...jugada });
  });

  escuchar("abrir:briefing", () => mostrarBriefing(estado.caso.briefing));
  escuchar("abrir:tablero", abrirTablero);
  escuchar("abrir:diario", () => {
    if (veredictoActual) mostrarDiario(veredictoActual);
  });
}

function enviarOAvisar(jugada) {
  if (conexion?.enviar(jugada)) return;
  avisar("no hay señal con la central — la jugada no salió", { tipo: "error" });
  estado.ocupado = false;
  escritorio.actualizarMaquina();
}

/* ── Los mensajes del servidor ───────────────────────────────────────────── */

function manejadoresDePartida() {
  return {
    comienzo: () => crt.comienzoRespuesta(),

    fragmento: (mensaje) => crt.fragmento(mensaje.texto),

    turno: (mensaje) => {
      (estado.conversaciones[mensaje.sospechoso] ??= []).push({
        quien: "sospechoso",
        texto: mensaje.respuesta,
      });
      crt.ponerEnHora(mensaje.preguntas_usadas);

      // Primero se termina de revelar el texto; recién ahí caen las pistas
      // (una por una) y se libera la máquina. El orden es dramaturgia.
      crt.finTurno(mensaje.respuesta, () => {
        mensaje.pistas_nuevas.forEach((pista, indice) => {
          estado.pistas.push(pista);
          const total = estado.pistas.length;
          setTimeout(() => escritorio.pistaNueva(pista, total), indice * 650);
        });
        escritorio.turnoCerrado(mensaje);
      });
    },

    veredicto: (mensaje) => {
      veredictoActual = mensaje;
      escritorio.acusacionResuelta(mensaje);
      setTimeout(() => mostrarDiario(mensaje), 400);
    },

    error: (mensaje) => {
      avisar(mensaje.mensaje, { tipo: "error", titulo: "LA CENTRAL RESPONDE" });
      if (crt.hayTransmision()) crt.fallo();
      estado.ocupado = false;
      escritorio.actualizarMaquina();
    },
  };
}

function avisarPorLaSenal(cambio) {
  if (cambio === "reintentando") {
    avisar("se cortó la señal con la central — reintentando…", { tipo: "error" });
  } else if (cambio === "recuperada") {
    avisar("señal recuperada", { titulo: "LA CENTRAL" });
  } else if (cambio === "perdida") {
    avisar("no hay caso: la central no responde. Recargá la página.", {
      tipo: "error",
      duracion: 60000,
    });
  }
}

/* ── Ruteo por hash ──────────────────────────────────────────────────────── */

async function rutear() {
  // Si el hash cambió con un overlay abierto (botón "atrás" del browser,
  // por ejemplo), ese velo ya no corresponde a lo que se va a mostrar.
  for (const velo of document.querySelectorAll("dialog[open]")) velo.close();

  const partidaId = location.hash.match(/^#\/partida\/([a-z0-9]+)/)?.[1];
  if (partidaId) {
    await abrirPartida(partidaId);
  } else {
    cerrarPartida();
    mostrarSeccion("archivo");
    await mostrarArchivo();
  }
}

function mostrarSeccion(nombre) {
  $("#pantalla-archivo").hidden = nombre !== "archivo";
  $("#pantalla-escritorio").hidden = nombre !== "escritorio";
  document.body.dataset.pantalla = nombre;
}

async function abrirPartida(partidaId) {
  if (estado.partidaId === partidaId) return; // el hash se re-disparó, nada que hacer
  cerrarPartida();

  let detalle;
  try {
    detalle = await api.detalle(partidaId);
  } catch (error) {
    avisar(
      error.status === 404 ? "ese expediente no existe (¿lo incineraste?)" : error.message,
      { tipo: "error" }
    );
    location.hash = "#/archivo";
    return;
  }

  estado.partidaId = partidaId;
  estado.detalle = detalle;
  estado.caso = detalle.caso;
  estado.conversaciones = detalle.conversaciones ?? {};
  estado.pistas = detalle.pistas ?? [];
  estado.tablero = normalizarTablero(detalle.tablero);
  estado.ocupado = false;
  veredictoActual = detalle.veredicto ?? null;

  document.title = `🛰️ ${estado.caso.titulo}`;
  mostrarSeccion("escritorio");
  escritorio.cargarPartida(detalle);
  crt.ponerEnHora(detalle.preguntas_usadas);

  conexion = conectarPartida(partidaId, manejadoresDePartida(), avisarPorLaSenal);

  // Partida recién estrenada: el briefing se presenta solo, tipeándose.
  const estrenando =
    !detalle.resultado && detalle.preguntas_usadas === 0 && estado.pistas.length === 0;
  if (estrenando) mostrarBriefing(estado.caso.briefing, { tipear: true });

  // ?abrir=tablero|diario|acusar — links directos a las vistas del caso.
  const abrir = new URLSearchParams(location.search).get("abrir");
  if (abrir === "tablero") abrirTablero();
  else if (abrir === "diario" && veredictoActual) mostrarDiario(veredictoActual);
  else if (abrir === "acusar" && !detalle.resultado) $("#boton-acusar").click();
}

function cerrarPartida() {
  conexion?.cerrar();
  conexion = null;
  estado.partidaId = null;
  estado.detalle = null;
  estado.caso = null;
  veredictoActual = null;
  document.title = "🛰️ El Caso Calafate";
}

/** El tablero guardado puede venir vacío o de una versión vieja: se sanea. */
function normalizarTablero(tablero) {
  return {
    notas: tablero?.notas ?? {},
    fotos: tablero?.fotos ?? {},
    conexiones: tablero?.conexiones ?? [],
  };
}

arrancar();
