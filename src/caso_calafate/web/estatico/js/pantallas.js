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
import { retratoPixel } from "./pixelart.js";
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

  // Una partida cuyo caso ya no está en el registro no se puede abrir, pero
  // sí incinerar: se muestra marcada en vez de desaparecer del archivo.
  const huerfana = partida.caso_disponible === false;

  const carpeta = document.createElement("button");
  carpeta.type = "button";
  carpeta.className = `expediente-carpeta${huerfana ? " expediente-huerfano" : ""}`;
  carpeta.disabled = huerfana;
  if (huerfana) carpeta.title = "el caso de este expediente ya no está disponible";
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

  const motor = document.createElement("span");
  motor.className = "expediente-motor";
  if (!huerfana) {
    const apagado = partida.motor_disponible === false;
    motor.textContent = `${apagado ? "⚠" : "🧠"} ${partida.motor_etiqueta ?? ""}`;
    if (apagado) {
      motor.classList.add("expediente-motor-caido");
      motor.title = partida.motor_motivo ?? "";
    }
  }

  const stats = document.createElement("span");
  stats.className = "expediente-stats";
  const maximo = partida.preguntas_usadas + partida.preguntas_restantes;
  stats.textContent = huerfana
    ? "el caso de este expediente ya no existe"
    : `🔎 ${partida.pistas_descubiertas}/${partida.total_secretos} pistas · ` +
      `❓ ${partida.preguntas_usadas}/${maximo} preguntas`;

  const sello = document.createElement("span");
  const estadoDelCaso = huerfana
    ? "ILEGIBLE"
    : { victoria: "RESUELTO", derrota: "FALLIDO" }[partida.resultado];
  sello.className = `sello expediente-sello ${
    { RESUELTO: "sello-verde", FALLIDO: "sello-rojo", ILEGIBLE: "sello-rojo" }[estadoDelCaso] ??
    "sello-ambar"
  }`;
  sello.textContent = estadoDelCaso ?? "ABIERTO";

  carpeta.append(nombre, caso, fecha, motor, stats, sello);
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
  $("#motor-elegido").addEventListener("change", mostrarDetalleDelMotor);

  formulario.addEventListener("submit", async (evento) => {
    evento.preventDefault();
    const nombre = formulario.nombre.value.trim();
    const modeloId = $("#motor-elegido").value;
    if (!nombre || !casoElegido || !modeloId) return;
    try {
      const partida = await api.crearPartida(nombre, casoElegido.id, modeloId);
      velo.close();
      location.hash = `#/partida/${partida.id}`;
    } catch {
      avisar("no pude abrir el expediente", { tipo: "error" });
    }
  });
}

export function abrirSelectorDeCasos({ casoId } = {}) {
  const lista = $("#casos-lista");
  lista.innerHTML = "";
  const tarjetas = new Map();
  for (const caso of estado.casosDisponibles) {
    const tarjeta = tarjetaDeCaso(caso);
    tarjetas.set(caso.id, tarjeta);
    lista.append(tarjeta);
  }
  poblarMotores();
  mostrarPasoElegirCaso();
  $("#velo-casos").showModal();
  // Deep link a la carátula de un caso puntual: salta el paso 1.
  if (casoId) tarjetas.get(casoId)?.querySelector("button")?.click();
}

/* Los motores que hoy no andan NO se esconden: van deshabilitados y con el
 * motivo escrito en la opción. Es la única pista que tiene el jugador de que
 * existe un Gemini esperando una API key, o un modelo a un `ollama pull` de
 * distancia. */
function poblarMotores() {
  const select = $("#motor-elegido");
  select.innerHTML = "";
  for (const motor of estado.motoresDisponibles) {
    const opcion = document.createElement("option");
    opcion.value = motor.id;
    opcion.disabled = !motor.disponible;
    opcion.textContent = motor.disponible ? motor.etiqueta : `${motor.etiqueta} — ${motor.motivo}`;
    select.append(opcion);
  }
  const sugerido = estado.motoresDisponibles.find(
    (m) => m.id === estado.motorSugerido && m.disponible,
  );
  const primero = estado.motoresDisponibles.find((m) => m.disponible);
  select.value = (sugerido ?? primero)?.id ?? "";
  mostrarDetalleDelMotor();
}

function mostrarDetalleDelMotor() {
  const elegido = estado.motoresDisponibles.find((m) => m.id === $("#motor-elegido").value);
  $("#motor-detalle").textContent = elegido?.detalle ?? "";
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

  // El documento es DE ESTE caso: el membrete y el título salen de sus datos,
  // no del HTML — si no, todo expediente parecería del Centro Espacial.
  const caso = estado.caso;
  if (caso) {
    $("#briefing-membrete").textContent = `${caso.sede.toUpperCase()}\nDIVISIÓN SEGURIDAD — ${caso.ciudad.toUpperCase()}`;
    $("#briefing-titulo").textContent = caso.titulo;
  }

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
  const velo = $("#velo-diario");
  if (velo.open) return; // ya está abierto: showModal() de nuevo tiraría error
  const caso = estado.caso;
  const gano = veredicto.resultado === "victoria";
  const acusado = caso.sospechosos.find((s) => s.id === veredicto.acusado);
  const nombre = acusado?.nombre ?? "el acusado";
  const cargo = acusado?.cargo ?? "";

  // Toda la tapa habla del caso que se jugó: ciudad, sede, hecho y el mote
  // que la prensa le puso al culpable salen de los datos del caso.
  $("#diario-ciudad").textContent = caso.ciudad.toUpperCase();

  $("#diario-titular").textContent = gano
    ? `¡CASO RESUELTO EN ${caso.ciudad.toUpperCase()}!`
    : `EL ${caso.culpable_alias.toUpperCase()} SIGUE LIBRE`;

  $("#diario-bajada").textContent = gano
    ? `${nombre}, ${cargo}, confesó ${caso.delito}. El expediente se cierra.`
    : `La acusación contra ${nombre}, ${cargo}, se desarmó en minutos. ` +
      `${caso.sede}, en crisis.`;

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

  // La foto de tapa es el retrato del acusado: sirve para cualquier caso, a
  // diferencia del dibujo del satélite que estaba antes acá.
  $("#diario-foto").replaceChildren(retratoPixel(veredicto.acusado));
  $("#diario-epigrafe").textContent = gano
    ? `${nombre}, ${cargo}, tras la confesión.`
    : `${nombre}, ${cargo}: la acusación no prosperó.`;

  sonido.veredicto(veredicto.resultado);
  velo.showModal();
}

export function prepararDiario() {
  $("#boton-diario-escritorio").addEventListener("click", () => $("#velo-diario").close());
  // El link "volver al archivo" navega por hash; el velo se cierra solo.
  $("#velo-diario a[href='#/archivo']").addEventListener("click", () => {
    $("#velo-diario").close();
  });
}
