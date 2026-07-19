/* tablero.js — el corcho: notas, polaroids, chinchetas e hilo rojo.
 *
 * El clásico tablero de detective, interactivo:
 *
 * - cada pista descubierta es una NOTA que se puede arrastrar
 * - cada sospechoso es una POLAROID fijada con chincheta
 * - tocás una chincheta y después otra → se tiende un HILO rojo entre ambas
 * - tocás un hilo → se corta
 *
 * Tres técnicas para mirar de cerca:
 * 1. El drag usa Pointer Events con setPointerCapture: un solo par de
 *    manejadores sirve para mouse, touch y lápiz, sin librerías.
 * 2. Las posiciones se guardan en PORCENTAJE del corcho, no en píxeles: el
 *    tablero sobrevive a cualquier tamaño de ventana.
 * 3. Los hilos son <path> de SVG con una curva cuadrática cuyo punto de
 *    control cuelga hacia abajo: la comba de un hilo real.
 *
 * Todo (posiciones + conexiones) se persiste con PUT /api/partidas/…/tablero,
 * con un debounce para no bombardear al servidor mientras arrastrás.
 */

import { api } from "./api.js";
import { avisar } from "./avisos.js";
import { $, estado } from "./estado.js";
import { retratoPixel } from "./pixelart.js";

let conectando = null;   // data-clave de la chincheta de origen, si hay hilo pendiente
let timerGuardado = null;

export function prepararTablero() {
  const velo = $("#velo-tablero");
  $("#boton-tablero-cerrar").addEventListener("click", () => velo.close());
  velo.addEventListener("close", () => {
    cancelarConexion();
    guardarYa(); // que no se pierda el último movimiento
  });

  // Click en el corcho pelado = cancelar el hilo pendiente.
  $("#corcho").addEventListener("click", (evento) => {
    if (evento.target.id === "corcho") cancelarConexion();
  });
  $("#corcho").addEventListener("pointermove", (evento) => {
    if (conectando) dibujarHiloPendiente(evento);
  });

  window.addEventListener("resize", () => {
    if (velo.open) dibujarHilos();
  });
}

export function abrirTablero() {
  armarPiezas();
  $("#velo-tablero").showModal();
  dibujarHilos();
}

/* ── Armar el corcho a partir del estado ─────────────────────────────────── */

function armarPiezas() {
  const corcho = $("#corcho");
  // Borrón y cuenta nueva (menos el SVG de hilos, que es fijo).
  for (const pieza of corcho.querySelectorAll(".nota, .polaroid, .tablero-vacio")) {
    pieza.remove();
  }

  const tablero = estado.tablero;

  // Las polaroids de los sospechosos, siempre presentes.
  estado.caso.sospechosos.forEach((sospechoso, indice) => {
    const clave = `foto-${sospechoso.id}`;
    tablero.fotos[sospechoso.id] ??= { x: 14 + indice * 27, y: 7 };
    const pieza = document.createElement("figure");
    pieza.className = "polaroid";
    pieza.append(retratoPixel(sospechoso.id));
    const nombre = document.createElement("figcaption");
    nombre.textContent = sospechoso.nombre.split(" ")[0];
    pieza.append(nombre);
    montarPieza(pieza, clave, tablero.fotos[sospechoso.id]);
  });

  // Una nota por pista descubierta; las nuevas caen en una grilla con mugre.
  estado.pistas.forEach((pista, indice) => {
    tablero.notas[pista.id] ??= {
      x: 8 + (indice % 4) * 23 + (barajar(pista.id) % 5),
      y: 36 + Math.floor(indice / 4) * 24 + (barajar(pista.id + "y") % 6),
    };
    const pieza = document.createElement("div");
    pieza.className = "nota";
    pieza.textContent = pista.pista;
    montarPieza(pieza, pista.id, tablero.notas[pista.id]);
  });

  if (estado.pistas.length === 0) {
    const cartel = document.createElement("p");
    cartel.className = "tablero-vacio";
    cartel.textContent = "el corcho espera evidencia — volvé cuando alguien suelte algo…";
    corcho.append(cartel);
  }
}

function montarPieza(pieza, clave, posicion) {
  pieza.dataset.clave = clave;
  pieza.style.left = `${posicion.x}%`;
  pieza.style.top = `${posicion.y}%`;
  pieza.style.setProperty("--rot", `${(barajar(clave) % 9) - 4}deg`);

  const chincheta = document.createElement("button");
  chincheta.type = "button";
  chincheta.className = "chincheta";
  chincheta.title = "tender un hilo";
  chincheta.addEventListener("click", (evento) => {
    evento.stopPropagation();
    tocarChincheta(clave, chincheta);
  });
  pieza.append(chincheta);

  hacerArrastrable(pieza, clave);
  $("#corcho").append(pieza);
}

/** Un hash bobo pero determinista: misma pieza, misma inclinación siempre. */
function barajar(texto) {
  let suma = 0;
  for (const letra of texto) suma = (suma * 31 + letra.codePointAt(0)) % 1000;
  return suma;
}

/* ── Arrastrar (Pointer Events) ──────────────────────────────────────────── */

function hacerArrastrable(pieza, clave) {
  let corrimiento = null; // distancia del click a la esquina de la pieza

  pieza.addEventListener("pointerdown", (evento) => {
    if (evento.target.classList.contains("chincheta")) return; // eso es un hilo
    pieza.setPointerCapture(evento.pointerId);
    const caja = pieza.getBoundingClientRect();
    corrimiento = { x: evento.clientX - caja.left, y: evento.clientY - caja.top };
    pieza.classList.add("arrastrando");
  });

  pieza.addEventListener("pointermove", (evento) => {
    if (!corrimiento) return;
    const corcho = $("#corcho").getBoundingClientRect();
    const x = ((evento.clientX - corrimiento.x - corcho.left) / corcho.width) * 100;
    const y = ((evento.clientY - corrimiento.y - corcho.top) / corcho.height) * 100;
    const posicion = {
      x: Math.min(92, Math.max(0.5, x)),
      y: Math.min(86, Math.max(1, y)),
    };
    pieza.style.left = `${posicion.x}%`;
    pieza.style.top = `${posicion.y}%`;
    guardarPosicion(clave, posicion);
    dibujarHilos(); // los hilos siguen a la pieza en vivo
  });

  const soltar = () => {
    if (!corrimiento) return;
    corrimiento = null;
    pieza.classList.remove("arrastrando");
    guardarConCalma();
  };
  pieza.addEventListener("pointerup", soltar);
  pieza.addEventListener("pointercancel", soltar);
}

function guardarPosicion(clave, posicion) {
  if (clave.startsWith("foto-")) {
    estado.tablero.fotos[clave.slice(5)] = posicion;
  } else {
    estado.tablero.notas[clave] = posicion;
  }
}

/* ── Los hilos ───────────────────────────────────────────────────────────── */

function tocarChincheta(clave, boton) {
  if (!conectando) {
    conectando = clave;
    boton.classList.add("conectando");
    return;
  }
  if (conectando !== clave) {
    const nueva = [conectando, clave];
    const yaExiste = estado.tablero.conexiones.some(
      ([a, b]) => (a === nueva[0] && b === nueva[1]) || (a === nueva[1] && b === nueva[0])
    );
    if (!yaExiste) {
      estado.tablero.conexiones.push(nueva);
      guardarConCalma();
    }
  }
  cancelarConexion();
  dibujarHilos();
}

function cancelarConexion() {
  conectando = null;
  $(".chincheta.conectando")?.classList.remove("conectando");
  $("#hilos .hilo-pendiente")?.remove();
}

function puntoDeChincheta(clave) {
  const pieza = $(`[data-clave="${clave}"]`);
  if (!pieza) return null;
  // offsetLeft/Top son relativos al corcho (position: absolute adentro suyo).
  return { x: pieza.offsetLeft + pieza.offsetWidth / 2, y: pieza.offsetTop };
}

function curvaDeHilo(a, b) {
  // El punto de control cuelga bajo el punto medio: cuanto más largo el
  // hilo, más comba — como un hilo de verdad, que no está tenso.
  const medioX = (a.x + b.x) / 2;
  const medioY = (a.y + b.y) / 2 + Math.hypot(b.x - a.x, b.y - a.y) * 0.12 + 12;
  return `M ${a.x} ${a.y} Q ${medioX} ${medioY} ${b.x} ${b.y}`;
}

function dibujarHilos() {
  const svg = $("#hilos");
  svg.innerHTML = "";
  estado.tablero.conexiones.forEach((conexion, indice) => {
    const [claveA, claveB] = conexion;
    const a = puntoDeChincheta(claveA);
    const b = puntoDeChincheta(claveB);
    if (!a || !b) return; // una punta apunta a algo que ya no está
    const hilo = document.createElementNS("http://www.w3.org/2000/svg", "path");
    hilo.setAttribute("class", "hilo");
    hilo.setAttribute("d", curvaDeHilo(a, b));
    hilo.addEventListener("click", () => {
      estado.tablero.conexiones.splice(indice, 1);
      dibujarHilos();
      guardarConCalma();
    });
    svg.append(hilo);
  });
}

function dibujarHiloPendiente(evento) {
  const origen = puntoDeChincheta(conectando);
  if (!origen) return;
  const corcho = $("#corcho").getBoundingClientRect();
  const destino = { x: evento.clientX - corcho.left, y: evento.clientY - corcho.top };
  let pendiente = $("#hilos .hilo-pendiente");
  if (!pendiente) {
    pendiente = document.createElementNS("http://www.w3.org/2000/svg", "path");
    pendiente.setAttribute("class", "hilo-pendiente");
    $("#hilos").append(pendiente);
  }
  pendiente.setAttribute("d", curvaDeHilo(origen, destino));
}

/* ── Persistencia con calma ──────────────────────────────────────────────── */

function guardarConCalma() {
  clearTimeout(timerGuardado);
  timerGuardado = setTimeout(guardarYa, 700);
}

function guardarYa() {
  clearTimeout(timerGuardado);
  timerGuardado = null;
  if (!estado.partidaId || !estado.tablero) return;
  api.guardarTablero(estado.partidaId, estado.tablero).catch(() => {
    avisar("no pude guardar el tablero — se reintenta en el próximo movimiento", {
      tipo: "error",
    });
  });
}
