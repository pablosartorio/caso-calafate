/* escritorio.js — todo lo que hay sobre la mesa, menos el monitor.
 *
 * Las fichas de los sospechosos, la libreta de pistas, el contador de
 * preguntas (palotes de a cinco, como en la pared de una celda), la máquina
 * de escribir y la orden de acusación.
 *
 * Este módulo NO habla con el servidor: cuando el jugador juega, emite
 * "jugada:interrogar" o "jugada:acusar" por el bus y main.js las manda por
 * el WebSocket. Mantener la capa visual sorda a la red es lo que después
 * permite testearla o reusarla sin tocar nada.
 */

import { avisar } from "./avisos.js";
import { reiniciarSintonia, sintonizar } from "./crt.js";
import { $, emitir, estado } from "./estado.js";
import { retratoPixel } from "./pixelart.js";
import { sonido } from "./sonido.js";

/* ── Armado inicial (una sola vez, cuando ya se conoce el caso) ──────────── */

export function prepararEscritorio() {
  prepararMaquina();
  prepararAcusacion();
  $("#boton-caso").addEventListener("click", () => emitir("abrir:briefing"));
  $("#boton-tablero").addEventListener("click", () => emitir("abrir:tablero"));
  $("#boton-diario").addEventListener("click", () => emitir("abrir:diario"));
}

function dibujarFichas() {
  const contenedor = $("#fichas");
  contenedor.innerHTML = "";
  for (const sospechoso of estado.caso.sospechosos) {
    const ficha = document.createElement("button");
    ficha.type = "button";
    ficha.className = "ficha";
    ficha.dataset.id = sospechoso.id;

    const foto = document.createElement("span");
    foto.className = "ficha-foto";
    foto.append(retratoPixel(sospechoso.id));

    const datos = document.createElement("span");
    datos.className = "ficha-datos";
    const nombre = document.createElement("span");
    nombre.className = "ficha-nombre";
    nombre.textContent = sospechoso.nombre;
    const cargo = document.createElement("span");
    cargo.className = "ficha-cargo";
    cargo.textContent = sospechoso.cargo;
    const coartada = document.createElement("span");
    coartada.className = "ficha-coartada";
    coartada.textContent = `“${sospechoso.coartada}”`;
    datos.append(nombre, cargo, coartada);

    const pin = document.createElement("span");
    pin.className = "ficha-pin";

    ficha.append(pin, foto, datos);
    ficha.addEventListener("click", () => elegirSospechoso(sospechoso));
    contenedor.append(ficha);
  }
}

export function elegirSospechoso(sospechoso) {
  if (estado.ocupado) return; // no se cambia de cámara con una pregunta en vuelo
  estado.seleccionado = sospechoso;
  for (const ficha of document.querySelectorAll(".ficha")) {
    ficha.classList.toggle("elegida", ficha.dataset.id === sospechoso.id);
  }
  sintonizar(sospechoso);
  actualizarMaquina();
  $("#entrada-pregunta").focus();
}

/* ── Cargar una partida (al entrar o retomar) ────────────────────────────── */

export function cargarPartida(detalle) {
  $("#nombre-partida").textContent = `«${detalle.nombre}»`;

  dibujarFichas(); // cada partida puede ser de un caso distinto: sospechosos propios
  reiniciarSintonia(); // cámara nueva, sin ráfaga de estática de entrada
  estado.seleccionado = null;

  dibujarLibreta(detalle.pistas);
  dibujarTally(detalle.preguntas_usadas);

  if (detalle.resultado) {
    cerrarEscritorio(detalle.resultado);
  } else {
    $("#maquina").hidden = false;
    $("#banda-cerrada").hidden = true;
    $("#boton-acusar").disabled = false;
    actualizarMaquina();
  }

  // Si venías interrogando a alguien, la cámara lo recuerda.
  const ultimo = estado.caso.sospechosos.find((s) => s.id === detalle.ultimo_sospechoso);
  if (ultimo) elegirSospechoso(ultimo);
  else sintonizar(null);
}

/** El turno terminó bien: actualizar contadores y devolver la máquina. */
export function turnoCerrado(turno) {
  dibujarTally(turno.preguntas_usadas);
  estado.ocupado = false;
  actualizarMaquina();
  if (turno.preguntas_restantes === 3) {
    avisar("Quedan tres preguntas. El directorio empieza a ponerse nervioso.", {
      titulo: "MEMO INTERNO",
    });
  }
}

/** El caso se cerró: la máquina se retira, queda el sello del resultado. */
export function cerrarEscritorio(resultado) {
  $("#maquina").hidden = true;
  const banda = $("#banda-cerrada");
  banda.hidden = false;
  const texto = $("#banda-cerrada-texto");
  texto.textContent = resultado === "victoria" ? "CASO CERRADO — RESUELTO" : "CASO CERRADO — FALLIDO";
  texto.className = resultado;
  $("#boton-acusar").disabled = true;
}

/* ── La libreta ──────────────────────────────────────────────────────────── */

function dibujarLibreta(pistas) {
  const lista = $("#lista-pistas");
  lista.innerHTML = "";
  for (const pista of pistas) anotarPista(pista, { recien: false });
  actualizarCuentaPistas(pistas.length);
}

export function pistaNueva(pista, total) {
  sonido.pista();
  avisar(pista.pista, { tipo: "pista", titulo: "🔎 NUEVA PISTA", duracion: 7000 });
  anotarPista(pista, { recien: true });
  actualizarCuentaPistas(total);
}

function anotarPista(pista, { recien }) {
  $("#libreta-vacia").hidden = true;
  const renglon = document.createElement("li");
  renglon.textContent = pista.pista;
  renglon.dataset.id = pista.id;
  if (recien) renglon.classList.add("pista-recien");
  $("#lista-pistas").append(renglon);
  if (recien) renglon.scrollIntoView({ block: "nearest", behavior: "smooth" });
}

function actualizarCuentaPistas(descubiertas) {
  $("#cuenta-pistas").textContent = `${descubiertas}/${estado.caso.total_secretos}`;
}

/* ── El tally de preguntas ───────────────────────────────────────────────── */

function dibujarTally(usadas) {
  const tally = $("#tally");
  tally.innerHTML = "";
  const titulo = document.createElement("span");
  titulo.className = "tally-titulo";
  titulo.textContent = "PREGUNTAS";
  tally.append(titulo);
  for (let i = 1; i <= estado.caso.max_preguntas; i++) {
    const palote = document.createElement("span");
    palote.className = "palote" + (i % 5 === 0 ? " palote-cruz" : "");
    if (i <= usadas) palote.classList.add("usado");
    tally.append(palote);
  }
  tally.setAttribute("aria-label", `${usadas} de ${estado.caso.max_preguntas} preguntas usadas`);
}

/* ── La máquina de escribir ──────────────────────────────────────────────── */

function prepararMaquina() {
  const entrada = $("#entrada-pregunta");

  entrada.addEventListener("keydown", (evento) => {
    if (evento.key.length === 1) sonido.tecla(); // solo teclas que imprimen
  });

  $("#maquina").addEventListener("submit", (evento) => {
    evento.preventDefault();
    const pregunta = entrada.value.trim();
    if (!pregunta || !estado.seleccionado || estado.ocupado) return;

    sonido.retorno();
    const maquina = $("#maquina");
    maquina.classList.add("disparada");
    setTimeout(() => maquina.classList.remove("disparada"), 350);

    entrada.value = "";
    estado.ocupado = true;
    actualizarMaquina();
    emitir("jugada:interrogar", {
      sospechoso: estado.seleccionado.id,
      pregunta,
    });
  });
}

/** El estado de la máquina depende de tres cosas: selección, turno y tiempo. */
export function actualizarMaquina() {
  const entrada = $("#entrada-pregunta");
  const tecla = $("#tecla-enviar");
  const quien = $("#maquina-quien");
  const restantes = restantesActuales();

  const cartel = $("#maquina-restantes");
  cartel.textContent = `(${restantes}❓)`;
  cartel.classList.toggle("pocas", restantes <= 3);

  if (estado.ocupado) {
    entrada.disabled = true;
    tecla.disabled = true;
    entrada.placeholder = "el sospechoso está hablando…";
    return;
  }
  if (restantes <= 0) {
    entrada.disabled = true;
    tecla.disabled = true;
    quien.textContent = "se acabó el tiempo";
    entrada.placeholder = "el directorio exige un nombre: estampá la acusación";
    return;
  }
  if (!estado.seleccionado) {
    entrada.disabled = true;
    tecla.disabled = true;
    quien.textContent = "elegí a quién interrogar";
    entrada.placeholder = "tocá la ficha de un sospechoso para empezar";
    return;
  }
  entrada.disabled = false;
  tecla.disabled = false;
  quien.textContent = estado.seleccionado.nombre.split(" ")[0];
  entrada.placeholder = `escribile tu pregunta a ${estado.seleccionado.nombre.split(" ")[0]}…`;
}

function restantesActuales() {
  const usadas = document.querySelectorAll("#tally .palote.usado").length;
  return estado.caso.max_preguntas - usadas;
}

/* ── La orden de acusación ───────────────────────────────────────────────── */

let acusado = null;

function prepararAcusacion() {
  const velo = $("#velo-acusacion");

  $("#boton-acusar").addEventListener("click", () => {
    if ($("#boton-acusar").disabled) return;
    acusado = null;
    dibujarFilasDeAcusacion();
    $("#boton-acusacion-confirmar").disabled = true;
    $("#sello-golpe").hidden = true;
    velo.showModal();
  });

  $("#boton-acusacion-cancelar").addEventListener("click", () => velo.close());

  $("#boton-acusacion-confirmar").addEventListener("click", () => {
    if (!acusado) return;
    // El sellazo: sonido, animación, y recién después viaja la jugada.
    sonido.sello();
    const sello = $("#sello-golpe");
    sello.hidden = false;
    sello.classList.add("golpeando");
    $("#boton-acusacion-confirmar").disabled = true;
    $("#boton-acusacion-cancelar").disabled = true;
    setTimeout(() => {
      sello.classList.remove("golpeando");
      emitir("jugada:acusar", { sospechoso: acusado.id });
    }, 750);
  });

  velo.addEventListener("close", () => {
    $("#boton-acusacion-cancelar").disabled = false;
  });
}

function dibujarFilasDeAcusacion() {
  const lista = $("#acusacion-lista");
  lista.innerHTML = "";
  for (const sospechoso of estado.caso.sospechosos) {
    const fila = document.createElement("button");
    fila.type = "button";
    fila.className = "acusado-fila";

    const foto = document.createElement("span");
    foto.className = "acusado-foto";
    foto.append(retratoPixel(sospechoso.id));

    const datos = document.createElement("span");
    const nombre = document.createElement("span");
    nombre.className = "acusado-nombre";
    nombre.textContent = sospechoso.nombre;
    const cargo = document.createElement("span");
    cargo.className = "acusado-cargo";
    cargo.textContent = ` — ${sospechoso.cargo}`;
    datos.append(nombre, cargo);

    const marca = document.createElement("span");
    marca.className = "acusado-marca";
    marca.textContent = "✗";

    fila.append(foto, datos, marca);
    fila.addEventListener("click", () => {
      acusado = sospechoso;
      for (const otra of lista.children) otra.classList.remove("seleccionada");
      fila.classList.add("seleccionada");
      $("#boton-acusacion-confirmar").disabled = false;
    });
    lista.append(fila);
  }
}

/** main.js llama acá cuando llega el veredicto: cerrar la orden y el caso. */
export function acusacionResuelta(veredicto) {
  $("#velo-acusacion").close();
  cerrarEscritorio(veredicto.resultado);
  dibujarTally(veredicto.preguntas_usadas);
}
