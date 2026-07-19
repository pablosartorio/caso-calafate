/* pantallas.js — lo que rodea al escritorio:
 *
 * · el ARCHIVO: la estantería de expedientes (crear, retomar, incinerar)
 * · el SELECTOR DE CASOS: qué misterio investigar, al abrir un expediente
 * · el BRIEFING: el documento del caso, tipeado a máquina
 * · el DIARIO: la tapa del día siguiente, con el veredicto
 */

import { api } from "./api.js";
import { avisar } from "./avisos.js";
import { $, estado } from "./estado.js";
import { sonido } from "./sonido.js";

/* ── El archivo de casos ─────────────────────────────────────────────────── */

export async function mostrarArchivo() {
  const estantes = $("#estantes");
  estantes.innerHTML = "";

  let partidas;
  try {
    partidas = await api.partidas();
  } catch {
    avisar("no pude leer el archivo — ¿el servidor sigue vivo?", { tipo: "error" });
    return;
  }

  for (const partida of partidas) estantes.append(tarjetaDeExpediente(partida));
  estantes.append(tarjetaDeNuevoExpediente());
}

function tarjetaDeExpediente(partida) {
  const item = document.createElement("li");
  item.className = "expediente";

  const carpeta = document.createElement("button");
  carpeta.type = "button";
  carpeta.className = "expediente-carpeta";
  carpeta.addEventListener("click", () => {
    location.hash = `#/partida/${partida.id}`;
  });

  const nombre = document.createElement("span");
  nombre.className = "expediente-nombre";
  nombre.textContent = partida.nombre;

  const caso = document.createElement("span");
  caso.className = "expediente-caso";
  caso.textContent = partida.caso_titulo ?? "";

  const fecha = document.createElement("span");
  fecha.className = "expediente-fecha";
  fecha.textContent = `abierto el ${new Date(partida.creada).toLocaleDateString("es-AR", {
    day: "numeric",
    month: "long",
  })}`;

  const stats = document.createElement("span");
  stats.className = "expediente-stats";
  const maximo = partida.preguntas_usadas + partida.preguntas_restantes;
  stats.textContent =
    `🔎 ${partida.pistas_descubiertas}/${partida.total_secretos} pistas · ` +
    `❓ ${partida.preguntas_usadas}/${maximo} preguntas`;

  const sello = document.createElement("span");
  const estadoDelCaso = { victoria: "RESUELTO", derrota: "FALLIDO" }[partida.resultado];
  sello.className = `sello expediente-sello ${
    { RESUELTO: "sello-verde", FALLIDO: "sello-rojo" }[estadoDelCaso] ?? "sello-ambar"
  }`;
  sello.textContent = estadoDelCaso ?? "ABIERTO";

  carpeta.append(nombre, caso, fecha, stats, sello);
  item.append(carpeta, botonDeIncinerar(partida, item));
  return item;
}

/** Borrar con confirmación en dos toques: ✕ → "¿incinerar?" → adiós. */
function botonDeIncinerar(partida, item) {
  const boton = document.createElement("button");
  boton.type = "button";
  boton.className = "expediente-borrar";
  boton.textContent = "✕";
  boton.title = "incinerar expediente";

  let confirmando = false;
  boton.addEventListener("click", async () => {
    if (!confirmando) {
      confirmando = true;
      boton.textContent = "¿incinerar?";
      boton.classList.add("confirmando");
      setTimeout(() => {
        confirmando = false;
        boton.textContent = "✕";
        boton.classList.remove("confirmando");
      }, 2600);
      return;
    }
    try {
      await api.borrarPartida(partida.id);
      item.remove();
    } catch {
      avisar("no pude incinerar el expediente", { tipo: "error" });
    }
  });
  return boton;
}

function tarjetaDeNuevoExpediente() {
  const item = document.createElement("li");

  const boton = document.createElement("button");
  boton.type = "button";
  boton.className = "expediente-nueva";
  boton.innerHTML = `<span class="mas">+</span><span class="texto">NUEVO EXPEDIENTE</span>`;
  boton.addEventListener("click", abrirSelectorDeCasos);

  item.append(boton);
  return item;
}

/* ── El selector de casos: overlay de alta de expediente ─────────────────── *
 * Dos pasos en el mismo <dialog>: elegir el caso (tarjetas) y después
 * nombrar el expediente — igual de espíritu que el resto de los velos
 * (briefing, acusación, tablero), solo que este tiene un paso previo. */

let casoElegido = null;

export function prepararSelectorDeCasos() {
  const velo = $("#velo-casos");
  const formulario = $("#form-nombrar-expediente");

  $("#boton-casos-cancelar").addEventListener("click", () => velo.close());
  $("#boton-casos-volver").addEventListener("click", mostrarPasoElegirCaso);

  formulario.addEventListener("submit", async (evento) => {
    evento.preventDefault();
    const nombre = formulario.nombre.value.trim();
    if (!nombre || !casoElegido) return;
    try {
      const partida = await api.crearPartida(nombre, casoElegido.id);
      velo.close();
      location.hash = `#/partida/${partida.id}`;
    } catch {
      avisar("no pude abrir el expediente", { tipo: "error" });
    }
  });
}

function abrirSelectorDeCasos() {
  const lista = $("#casos-lista");
  lista.innerHTML = "";
  for (const caso of estado.casosDisponibles) lista.append(tarjetaDeCaso(caso));
  mostrarPasoElegirCaso();
  $("#velo-casos").showModal();
}

function mostrarPasoElegirCaso() {
  $("#casos-paso-elegir").hidden = false;
  $("#form-nombrar-expediente").hidden = true;
  casoElegido = null;
}

function tarjetaDeCaso(caso) {
  const li = document.createElement("li");
  const boton = document.createElement("button");
  boton.type = "button";
  boton.className = "caso-tarjeta";

  const titulo = document.createElement("span");
  titulo.className = "caso-tarjeta-titulo";
  titulo.textContent = caso.titulo;

  const gancho = document.createElement("span");
  gancho.className = "caso-tarjeta-gancho";
  gancho.textContent = caso.gancho;

  const stats = document.createElement("span");
  stats.className = "caso-tarjeta-stats";
  stats.textContent = `🕵️ ${caso.cantidad_sospechosos} sospechosos · ❓ ${caso.max_preguntas} preguntas`;

  boton.append(titulo, gancho, stats);
  boton.addEventListener("click", () => {
    casoElegido = caso;
    $("#casos-caso-elegido").textContent = caso.titulo;
    $("#casos-paso-elegir").hidden = true;

    const formulario = $("#form-nombrar-expediente");
    formulario.hidden = false;
    formulario.nombre.value = "";
    formulario.nombre.focus();
  });

  li.append(boton);
  return li;
}

/* ── El briefing tipeado ─────────────────────────────────────────────────── */

let timerTipeo = null;

export function mostrarBriefing(texto, { tipear = false, alAceptar = null } = {}) {
  const velo = $("#velo-briefing");
  const cuerpo = $("#texto-briefing");
  const saltar = $("#boton-briefing-saltar");
  const aceptar = $("#boton-briefing-aceptar");

  clearInterval(timerTipeo);
  aceptar.textContent = tipear ? "ACEPTAR EL CASO →" : "VOLVER AL ESCRITORIO →";

  if (!tipear) {
    cuerpo.textContent = texto;
    saltar.hidden = true;
  } else {
    // El informe se tipea solo, como salido del télex de la División.
    cuerpo.textContent = "";
    saltar.hidden = false;
    let cursor = 0;
    timerTipeo = setInterval(() => {
      cursor += 3;
      cuerpo.textContent = texto.slice(0, cursor);
      if (cursor % 12 === 0) sonido.teletipo();
      if (cursor >= texto.length) {
        clearInterval(timerTipeo);
        saltar.hidden = true;
      }
    }, 24);
  }

  saltar.onclick = () => {
    clearInterval(timerTipeo);
    cuerpo.textContent = texto;
    saltar.hidden = true;
  };
  aceptar.onclick = () => velo.close();
  velo.addEventListener("close", () => {
    clearInterval(timerTipeo);
    cuerpo.textContent = texto; // que quede completo si lo cerraron con Esc
    alAceptar?.();
  }, { once: true });

  velo.showModal();
}

/* ── El diario del día siguiente ─────────────────────────────────────────── */

export function mostrarDiario(veredicto) {
  const gano = veredicto.resultado === "victoria";
  const acusado = estado.caso.sospechosos.find((s) => s.id === veredicto.acusado);
  const nombre = acusado?.nombre ?? "el acusado";
  const cargo = acusado?.cargo ?? "";

  $("#diario-titular").textContent = gano
    ? "¡CASO RESUELTO EN EL CENTRO ESPACIAL!"
    : "EL SABOTEADOR SIGUE LIBRE";

  $("#diario-bajada").textContent = gano
    ? `${nombre}, ${cargo}, confesó el sabotaje del CALAFATE-1. El lanzamiento vuelve a tener fecha.`
    : `La acusación contra ${nombre}, ${cargo}, se desarmó en minutos. El Centro, en crisis.`;

  // El cuerpo de la nota: el veredicto y, recién acá, la verdad completa.
  // Con victoria hubo confesión y el diario puede contarlo todo; con derrota
  // el titular dice que el saboteador sigue libre, así que la verdad va
  // detrás de una raya: es una confidencia al detective, no una primicia.
  const cuerpo = gano
    ? `${veredicto.texto}\n\n${veredicto.epilogo}`
    : `${veredicto.texto}\n\n— Lo que EL CORDILLERANO nunca llegó a publicar —\n\n` +
      veredicto.epilogo;
  $("#diario-cuerpo").textContent = cuerpo;

  $("#diario-stats").textContent =
    `PISTAS: ${veredicto.pistas_descubiertas}/${veredicto.total_secretos}\n` +
    `PREGUNTAS: ${veredicto.preguntas_usadas}/${estado.caso.max_preguntas}`;
  $("#diario-calificacion").textContent = veredicto.calificacion;

  $("#diario-foto").innerHTML = FOTO_SATELITE;

  sonido.veredicto(veredicto.resultado);
  $("#velo-diario").showModal();
}

export function prepararDiario() {
  $("#boton-diario-escritorio").addEventListener("click", () => $("#velo-diario").close());
  // El link "volver al archivo" navega por hash; el velo se cierra solo.
  $("#velo-diario a[href='#/archivo']").addEventListener("click", () => {
    $("#velo-diario").close();
  });
}

/* La foto del diario: el CALAFATE-1 en la sala limpia, la mañana del
   hallazgo (el mazo de cables colgando, cortado — lo que arrancó todo esto). */
const FOTO_SATELITE = `
<svg viewBox="0 0 240 160" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="el satélite CALAFATE-1">
  <rect width="240" height="160" fill="#d6d0c0"/>
  <rect y="118" width="240" height="42" fill="#b9b2a0"/>
  <line x1="0" y1="118" x2="240" y2="118" stroke="#8f8875" stroke-width="1.5"/>
  <!-- panel solar izquierdo -->
  <g stroke="#3c4652" stroke-width="1.5">
    <rect x="22" y="52" width="62" height="34" fill="#5e6d7c"/>
    <line x1="43" y1="52" x2="43" y2="86"/><line x1="63" y1="52" x2="63" y2="86"/>
    <line x1="22" y1="69" x2="84" y2="69"/>
    <line x1="84" y1="69" x2="98" y2="69"/>
  </g>
  <!-- panel solar derecho -->
  <g stroke="#3c4652" stroke-width="1.5">
    <rect x="156" y="52" width="62" height="34" fill="#5e6d7c"/>
    <line x1="177" y1="52" x2="177" y2="86"/><line x1="197" y1="52" x2="197" y2="86"/>
    <line x1="156" y1="69" x2="218" y2="69"/>
    <line x1="142" y1="69" x2="156" y2="69"/>
  </g>
  <!-- cuerpo -->
  <rect x="98" y="42" width="44" height="56" fill="#8a8578" stroke="#3a352c" stroke-width="2"/>
  <rect x="98" y="84" width="44" height="14" fill="#a8925c" stroke="#3a352c" stroke-width="1.5"/>
  <rect x="104" y="50" width="32" height="10" fill="#6f6a5e"/>
  <circle cx="120" cy="72" r="7" fill="#6f6a5e" stroke="#3a352c" stroke-width="1.5"/>
  <!-- antena -->
  <line x1="120" y1="42" x2="120" y2="26" stroke="#3a352c" stroke-width="2"/>
  <ellipse cx="120" cy="24" rx="10" ry="4" fill="none" stroke="#3a352c" stroke-width="2"/>
  <!-- el mazo de cables cortado, colgando -->
  <path d="M112,98 C110,108 112,114 108,120" fill="none" stroke="#77362a" stroke-width="3"/>
  <path d="M116,98 C116,106 114,112 113,117" fill="none" stroke="#8a5c30" stroke-width="2.5"/>
  <g stroke="#4a2018" stroke-width="1.5">
    <line x1="106" y1="120" x2="104" y2="124"/>
    <line x1="108" y1="120" x2="108" y2="125"/>
    <line x1="110" y1="120" x2="112" y2="124"/>
  </g>
  <!-- el soporte en la sala limpia -->
  <g stroke="#5c564a" stroke-width="3">
    <line x1="104" y1="98" x2="96" y2="130"/>
    <line x1="136" y1="98" x2="144" y2="130"/>
  </g>
  <circle cx="96" cy="133" r="4" fill="#5c564a"/>
  <circle cx="144" cy="133" r="4" fill="#5c564a"/>
</svg>`;
