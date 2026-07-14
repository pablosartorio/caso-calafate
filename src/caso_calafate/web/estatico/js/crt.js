/* crt.js — el monitor: la cámara de la sala de interrogatorios.
 *
 * Acá está la pieza más fina del frontend: el REVELADO. El servidor manda
 * fragmentos de texto a la velocidad a la que el LLM los genera, pero
 * mostrarlos tal cual queda a los saltos (los tokens llegan en ráfagas).
 * En cambio, los fragmentos se acumulan en una cola y un timer los revela
 * a ritmo de teletipo, parejo. Dos relojes desacoplados: el de la red y el
 * de la pantalla.
 *
 * Regla de oro del streaming (espejo de la del servidor): los fragmentos son
 * mejora progresiva. La respuesta COMPLETA llega al final en el mensaje
 * "turno", y este módulo la reconcilia con lo que mostró — si un modelo no
 * streamea, el texto aparece igual.
 */

import { $, estado } from "./estado.js";
import { retratoPixel } from "./pixelart.js";
import { sonido } from "./sonido.js";

const VELOCIDAD = 30;      // milisegundos entre tandas de caracteres
const POR_TANDA = 2;       // caracteres por tanda (≈ 65 por segundo)

let cola = "";             // texto que llegó y todavía no se mostró
let nodoTexto = null;      // el nodo de texto de la respuesta en curso
let cursor = null;         // el bloquecito verde que titila
let timer = null;
let cierreDelTurno = null; // {respuesta, alTerminar} — llega con "turno"
let tictac = 0;            // para el tic de teletipo cada tantas letras

export function iniciarCRT() {
  // Click en la transcripción = "no tengo paciencia": revelar todo ya.
  $("#transcripcion").addEventListener("click", revelarTodo);
}

/* ── Sintonizar: elegir a quién se ve en la cámara ───────────────────────── */

let camaraAnterior = null; // para saber si esto es un CAMBIO de cámara

/** Al entrar a una partida no hubo cámara previa: que no meta estática. */
export function reiniciarSintonia() {
  camaraAnterior = null;
}

export function sintonizar(sospechoso) {
  const sinSenal = $("#crt-sin-senal");

  // El golpe de nieve solo si se está CAMBIANDO de cámara: se ve la
  // estática pelada 300 ms y después queda el estado final (feed o la
  // leyenda de SIN SEÑAL). Al cargar la página, nada de ruido gratuito.
  const hayCambio = camaraAnterior !== (sospechoso?.id ?? null);
  camaraAnterior = sospechoso?.id ?? null;
  if (hayCambio && camaraAnterior !== null) {
    sonido.estatica();
    sinSenal.classList.add("solo-nieve");
    sinSenal.hidden = false;
    setTimeout(() => {
      sinSenal.classList.remove("solo-nieve");
      sinSenal.hidden = Boolean(sospechoso);
    }, 300);
  } else {
    sinSenal.hidden = Boolean(sospechoso);
  }

  if (!sospechoso) {
    $("#crt-feed").innerHTML = "";
    $("#crt-sujeto").textContent = "SUJETO: —";
    return;
  }

  $("#crt-feed").replaceChildren(retratoPixel(sospechoso.id));

  const [nombre, ...resto] = sospechoso.nombre.split(" ");
  const apellido = resto.length ? resto.join(" ") : nombre;
  $("#crt-sujeto").textContent =
    `SUJETO: ${apellido.toUpperCase()}, ${nombre[0]}. — ${sospechoso.cargo.toUpperCase()}`;

  // Al cambiar de cámara se repone la charla que ya hubo con esa persona.
  const transcripcion = $("#transcripcion");
  transcripcion.innerHTML = "";
  for (const mensaje of estado.conversaciones[sospechoso.id] ?? []) {
    agregarLinea(mensaje.quien === "detective" ? "detective" : "sospechoso", mensaje.texto);
  }
  transcripcion.scrollTop = transcripcion.scrollHeight;
}

/* ── El flujo de un turno ────────────────────────────────────────────────── */

/** La pregunta del detective aparece al instante (la tipeaste vos). */
export function preguntar(texto) {
  agregarLinea("detective", texto);
}

/** Mensaje "comienzo": el sospechoso va a hablar — línea nueva y cursor. */
export function comienzoRespuesta() {
  const linea = agregarLinea("sospechoso", "");
  nodoTexto = linea.firstChild;
  cursor = document.createElement("span");
  cursor.className = "cursor-crt";
  linea.append(cursor);
  $("#crt-feed .retrato")?.classList.add("hablando");
}

/** Mensaje "fragmento": texto nuevo a la cola del teletipo. */
export function fragmento(texto) {
  cola += texto;
  if (!timer) timer = setInterval(revelarUnPoco, VELOCIDAD);
}

/** Mensaje "turno": el servidor cerró el turno; reconciliar y avisar. */
export function finTurno(respuestaCompleta, alTerminar) {
  cierreDelTurno = { respuesta: respuestaCompleta, alTerminar };
  if (!timer) terminarRevelado(); // no había nada streameado (o ya terminó)
}

/** ¿Hay una respuesta a medio revelar? (main lo usa ante un error) */
export function hayTransmision() {
  return cursor !== null;
}

/** Corte de luz: el interrogatorio falló a mitad de camino. */
export function fallo() {
  detenerTimer();
  cola = "";
  cierreDelTurno = null;
  quitarCursor();
  agregarLinea("sistema", "— TRANSMISIÓN INTERRUMPIDA —");
}

/* ── El teletipo ─────────────────────────────────────────────────────────── */

function revelarUnPoco() {
  if (!cola) {
    detenerTimer();
    if (cierreDelTurno) terminarRevelado();
    return;
  }
  if (nodoTexto) {
    nodoTexto.textContent += cola.slice(0, POR_TANDA);
    if ((tictac = (tictac + 1) % 5) === 0) sonido.teletipo();
  }
  cola = cola.slice(POR_TANDA);
  desplazarSiHaceFalta();
}

function revelarTodo() {
  if (!cola && !cierreDelTurno) return;
  if (nodoTexto) nodoTexto.textContent += cola;
  cola = "";
  detenerTimer();
  if (cierreDelTurno) terminarRevelado();
  desplazarSiHaceFalta();
}

function terminarRevelado() {
  const { respuesta, alTerminar } = cierreDelTurno;
  cierreDelTurno = null;

  // La reconciliación: lo que quedó en pantalla debe ser la respuesta
  // completa, sin importar qué tan bien haya streameado el modelo.
  if (nodoTexto && respuesta && nodoTexto.textContent !== respuesta) {
    nodoTexto.textContent = respuesta;
  }
  nodoTexto = null;
  quitarCursor();
  $("#crt-feed .retrato")?.classList.remove("hablando");
  desplazarSiHaceFalta();
  alTerminar?.();
}

function detenerTimer() {
  clearInterval(timer);
  timer = null;
}

function quitarCursor() {
  cursor?.remove();
  cursor = null;
}

/* ── Piecitas ────────────────────────────────────────────────────────────── */

function agregarLinea(tipo, texto) {
  const linea = document.createElement("div");
  linea.className = `linea linea-${tipo}`;
  linea.append(document.createTextNode(texto)); // textContent: acá habla un LLM
  $("#transcripcion").append(linea);
  desplazarSiHaceFalta();
  return linea;
}

function desplazarSiHaceFalta() {
  const caja = $("#transcripcion");
  // Solo si el lector ya estaba mirando el final; si subió a releer, no se
  // le mueve el piso.
  if (caja.scrollHeight - caja.scrollTop - caja.clientHeight < 160) {
    caja.scrollTop = caja.scrollHeight;
  }
}

/** El reloj del caso: empezó 06:50; cada pregunta se lleva 13 minutos. */
export function ponerEnHora(preguntasUsadas) {
  const minutos = 6 * 60 + 50 + preguntasUsadas * 13;
  const hh = String(Math.floor(minutos / 60) % 24).padStart(2, "0");
  const mm = String(minutos % 60).padStart(2, "0");
  $("#crt-reloj").textContent = `${hh}:${mm}`;
}
