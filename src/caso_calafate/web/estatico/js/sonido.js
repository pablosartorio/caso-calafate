/* sonido.js — todo el audio del juego, sintetizado con Web Audio.
 *
 * No hay UN SOLO archivo de audio: la lluvia es ruido blanco filtrado, el
 * zumbido del monitor son dos senoidales graves, las teclas son ráfagas de
 * ruido con un filtro pasabanda, la campanita de las pistas es una campana
 * FM de dos parciales. Sintetizar tiene dos gracias: pesa cero bytes y se
 * puede afinar cada sonido con un número.
 *
 * Reglas de la casa:
 * - El AudioContext se crea recién en el primer gesto del usuario (los
 *   browsers bloquean el audio antes de eso — política de autoplay).
 * - El ambiente (lluvia + viento + zumbido) vive en su propio bus con la
 *   radio del escritorio como perilla; los efectos van por otro bus y suenan
 *   siempre. La preferencia queda en localStorage.
 */

const PREFERENCIA = "calafate-radio";

let ctx = null;
let busAmbiente = null; // lluvia, viento, zumbido — lo apaga la radio
let busEfectos = null;  // teclas, sellos, campanitas — suena siempre
let ruido = null;       // buffer de ruido blanco, compartido por todo

/** Primer gesto del usuario: acá nace el contexto y arranca el ambiente. */
function activar() {
  if (ctx) {
    if (ctx.state === "suspended") ctx.resume();
    return;
  }
  ctx = new AudioContext();

  const maestro = ctx.createGain();
  maestro.gain.value = 0.9;
  maestro.connect(ctx.destination);

  busAmbiente = ctx.createGain();
  busAmbiente.gain.value = 0;
  busAmbiente.connect(maestro);

  busEfectos = ctx.createGain();
  busEfectos.gain.value = 0.8;
  busEfectos.connect(maestro);

  // 2 segundos de ruido blanco; con loop=true alcanza para siempre.
  ruido = ctx.createBuffer(1, ctx.sampleRate * 2, ctx.sampleRate);
  const datos = ruido.getChannelData(0);
  for (let i = 0; i < datos.length; i++) datos[i] = Math.random() * 2 - 1;

  encenderAmbiente();
  if (radioEncendida()) subirAmbiente();
}

/* ── El ambiente: lluvia patagónica, viento y zumbido de CRT ─────────────── */

function fuenteDeRuido() {
  const fuente = ctx.createBufferSource();
  fuente.buffer = ruido;
  fuente.loop = true;
  fuente.start();
  return fuente;
}

function encenderAmbiente() {
  // Lluvia: ruido pasado por un pasabajos, con la frecuencia de corte
  // ondulando despacio para que "respire" como una lluvia de verdad.
  const lluvia = ctx.createBiquadFilter();
  lluvia.type = "lowpass";
  lluvia.frequency.value = 750;
  const vaivenLluvia = ctx.createOscillator();
  vaivenLluvia.frequency.value = 0.07;
  const cuantoVaiven = ctx.createGain();
  cuantoVaiven.gain.value = 180;
  vaivenLluvia.connect(cuantoVaiven).connect(lluvia.frequency);
  vaivenLluvia.start();
  const ganLluvia = ctx.createGain();
  ganLluvia.gain.value = 0.055;
  fuenteDeRuido().connect(lluvia).connect(ganLluvia).connect(busAmbiente);

  // Viento: una banda angosta de ruido que sube y baja cada ~9 segundos.
  const viento = ctx.createBiquadFilter();
  viento.type = "bandpass";
  viento.frequency.value = 280;
  viento.Q.value = 1.6;
  const ganViento = ctx.createGain();
  ganViento.gain.value = 0.02;
  const vaivenViento = ctx.createOscillator();
  vaivenViento.frequency.value = 0.11;
  const cuantoViento = ctx.createGain();
  cuantoViento.gain.value = 0.014;
  vaivenViento.connect(cuantoViento).connect(ganViento.gain);
  vaivenViento.start();
  fuenteDeRuido().connect(viento).connect(ganViento).connect(busAmbiente);

  // Zumbido del monitor: 50 Hz y su armónico (acá la red eléctrica es de 50).
  for (const [frecuencia, volumen] of [[50, 0.014], [100, 0.006]]) {
    const osc = ctx.createOscillator();
    osc.frequency.value = frecuencia;
    const gan = ctx.createGain();
    gan.gain.value = volumen;
    osc.connect(gan).connect(busAmbiente);
    osc.start();
  }
}

function subirAmbiente() {
  busAmbiente.gain.cancelScheduledValues(ctx.currentTime);
  busAmbiente.gain.linearRampToValueAtTime(0.7, ctx.currentTime + 1.4);
}

function bajarAmbiente() {
  busAmbiente.gain.cancelScheduledValues(ctx.currentTime);
  busAmbiente.gain.linearRampToValueAtTime(0, ctx.currentTime + 0.4);
}

/* ── Piezas chicas para armar efectos ────────────────────────────────────── */

/** Ráfaga de ruido filtrado: la base de teclas, estática y golpes. */
function rafaga({ tipo = "bandpass", frecuencia = 2000, q = 1, dur = 0.05, vol = 0.1 }) {
  const fuente = fuenteDeRuido();
  const filtro = ctx.createBiquadFilter();
  filtro.type = tipo;
  filtro.frequency.value = frecuencia;
  filtro.Q.value = q;
  const gan = ctx.createGain();
  gan.gain.setValueAtTime(vol, ctx.currentTime);
  gan.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + dur);
  fuente.connect(filtro).connect(gan).connect(busEfectos);
  fuente.stop(ctx.currentTime + dur + 0.05);
}

/** Una campana simple: senoidal con caída exponencial (y un parcial arriba). */
function campana(frecuencia, { dur = 0.9, vol = 0.06, retardo = 0 } = {}) {
  const cuando = ctx.currentTime + retardo;
  for (const [multiplo, peso] of [[1, 1], [2.76, 0.35]]) {
    const osc = ctx.createOscillator();
    osc.frequency.value = frecuencia * multiplo;
    const gan = ctx.createGain();
    gan.gain.setValueAtTime(vol * peso, cuando);
    gan.gain.exponentialRampToValueAtTime(0.0001, cuando + dur);
    osc.connect(gan).connect(busEfectos);
    osc.start(cuando);
    osc.stop(cuando + dur + 0.05);
  }
}

/* ── La API que usa el resto del juego ───────────────────────────────────── */

export const sonido = {
  activar,

  /** La radio del escritorio: prende/apaga el ambiente y recuerda el gusto. */
  radio(encender) {
    localStorage.setItem(PREFERENCIA, encender ? "1" : "0");
    if (!ctx) return;
    if (encender) subirAmbiente();
    else bajarAmbiente();
  },

  /** Una tecla de la máquina: ruido corto, cada golpe apenas distinto. */
  tecla() {
    if (!ctx) return;
    rafaga({ frecuencia: 2300 + Math.random() * 1600, q: 2, dur: 0.03, vol: 0.07 });
  },

  /** Enter: golpe seco + campanita + el carro que vuelve. */
  retorno() {
    if (!ctx) return;
    rafaga({ frecuencia: 1400, q: 1.2, dur: 0.05, vol: 0.14 });
    campana(1319, { dur: 0.5, vol: 0.05, retardo: 0.05 });
    rafaga({ tipo: "lowpass", frecuencia: 350, dur: 0.22, vol: 0.08 });
  },

  /** El tic del teletipo mientras el sospechoso "escribe" en el CRT. */
  teletipo() {
    if (!ctx) return;
    rafaga({ frecuencia: 1750, q: 6, dur: 0.015, vol: 0.02 });
  },

  /** Estática al sintonizar otra cámara. */
  estatica() {
    if (!ctx) return;
    rafaga({ tipo: "highpass", frecuencia: 900, dur: 0.32, vol: 0.09 });
  },

  /** ¡Pista nueva!: dos notas de campana y un roce de papel. */
  pista() {
    if (!ctx) return;
    campana(587, { vol: 0.055 });
    campana(880, { vol: 0.05, retardo: 0.13 });
    rafaga({ frecuencia: 3200, q: 0.8, dur: 0.12, vol: 0.03 });
  },

  /** El sello contra el papel: un golpe grave con cuerpo. */
  sello() {
    if (!ctx) return;
    const osc = ctx.createOscillator();
    osc.frequency.setValueAtTime(150, ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(48, ctx.currentTime + 0.12);
    const gan = ctx.createGain();
    gan.gain.setValueAtTime(0.5, ctx.currentTime);
    gan.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.18);
    osc.connect(gan).connect(busEfectos);
    osc.start();
    osc.stop(ctx.currentTime + 0.25);
    rafaga({ tipo: "lowpass", frecuencia: 900, dur: 0.06, vol: 0.2 });
  },

  /** El acorde del final: mayor si ganaste, un lamento grave si no. */
  veredicto(resultado) {
    if (!ctx) return;
    if (resultado === "victoria") {
      [523, 659, 784, 1047].forEach((nota, i) =>
        campana(nota, { dur: 1.6, vol: 0.05, retardo: i * 0.16 })
      );
    } else {
      campana(220, { dur: 2.4, vol: 0.07 });
      campana(262, { dur: 2.4, vol: 0.05, retardo: 0.3 });
    }
  },
};

/** ¿La radio quedó prendida la última vez? (si nunca se tocó: prendida) */
export function radioEncendida() {
  return localStorage.getItem(PREFERENCIA) !== "0";
}
