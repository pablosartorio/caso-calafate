/* preferencias.js — dos preferencias chicas de accesibilidad/gusto visual,
 * persistidas en localStorage con el mismo patrón que ya usa sonido.js para
 * la radio: una clave, un getter, y quien las pinta decide cómo mostrarlas.
 *
 * 1. FILTRO_MONITOR — qué filtro CSS lleva la cámara del CRT:
 *      "fosforo" (verde, el look de siempre) → "ambar" (monocromático,
 *      cámaras de seguridad viejas) → "color" (sin filtro, los colores DB32
 *      reales del pixel art) → vuelve a "fosforo".
 * 2. MOTION_CRT — si la "nieve" y el parpadeo del monitor van a intensidad
 *    completa ("normal") o atenuada ("suave"). Es MÁS FINO que
 *    prefers-reduced-motion: reduce (que apaga TODA animación); esto solo
 *    calma el ruido del CRT y deja el resto del juego (parpadeo de ojos,
 *    boca al hablar, cursor) tal cual.
 */

const CLAVE_FILTRO = "calafate-filtro-monitor";
const CLAVE_MOTION = "calafate-motion-crt";

export const FILTROS_MONITOR = ["fosforo", "ambar", "color"];

const ETIQUETAS_FILTRO = {
  fosforo: "fósforo",
  ambar: "ámbar",
  color: "color",
};

export function filtroMonitor() {
  const guardado = localStorage.getItem(CLAVE_FILTRO);
  return FILTROS_MONITOR.includes(guardado) ? guardado : "fosforo";
}

export function etiquetaFiltro(filtro) {
  return ETIQUETAS_FILTRO[filtro] ?? filtro;
}

export function siguienteFiltroMonitor() {
  const actual = FILTROS_MONITOR.indexOf(filtroMonitor());
  const proximo = FILTROS_MONITOR[(actual + 1) % FILTROS_MONITOR.length];
  localStorage.setItem(CLAVE_FILTRO, proximo);
  return proximo;
}

export function motionCrtSuave() {
  return localStorage.getItem(CLAVE_MOTION) === "suave";
}

export function alternarMotionCrt() {
  const nuevo = motionCrtSuave() ? "normal" : "suave";
  localStorage.setItem(CLAVE_MOTION, nuevo);
  return nuevo === "suave";
}

/** Aplica ambas preferencias guardadas al <body> (se llama al arrancar). */
export function aplicarPreferenciasVisuales() {
  document.body.dataset.filtroMonitor = filtroMonitor();
  document.body.classList.toggle("motion-crt-suave", motionCrtSuave());
}
