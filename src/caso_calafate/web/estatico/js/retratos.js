/* retratos.js — los tres sospechosos, dibujados a mano en SVG.
 *
 * Estilo "foto de expediente": busto de frente, fondo con líneas de altura
 * como en las fotos policiales, formas planas. Los colores base son neutros
 * a propósito: cada contexto los procesa con filtros CSS — sepia en las
 * fichas y polaroids, fósforo verde dentro del monitor CRT.
 *
 * Detalles vivos (las clases las anima base.css):
 *   .parpado       → el párpado que parpadea cada tanto
 *   .boca-cerrada / .boca-abierta → alternan cuando el retrato tiene la
 *                    clase "hablando" (mientras streamea su respuesta)
 *
 * Nada de <defs> ni ids internos: estos SVG se inyectan varias veces en la
 * misma página y los ids duplicados romperían las referencias.
 */

// El fondo compartido: pared con líneas de altura y una sombra en el piso.
const FONDO = `
  <rect width="200" height="240" fill="#cfc3a6"/>
  <g stroke="#5c4c34" stroke-opacity="0.16" stroke-width="1">
    <line x1="0" y1="34"  x2="200" y2="34"/>
    <line x1="0" y1="59"  x2="200" y2="59"/>
    <line x1="0" y1="84"  x2="200" y2="84"/>
    <line x1="0" y1="109" x2="200" y2="109"/>
    <line x1="0" y1="134" x2="200" y2="134"/>
    <line x1="0" y1="159" x2="200" y2="159"/>
    <line x1="0" y1="184" x2="200" y2="184"/>
    <line x1="0" y1="209" x2="200" y2="209"/>
  </g>
  <ellipse cx="100" cy="238" rx="74" ry="10" fill="#3a2f1e" opacity="0.22"/>`;

// Ojos genéricos: blanco + iris + pupila + brillo, y el párpado que parpadea.
function ojos(colorPiel, colorIris, separacion = 15, mirada = 0) {
  const izq = 100 - separacion;
  const der = 100 + separacion;
  return `
  <g class="ojos">
    <ellipse cx="${izq}" cy="100" rx="7.5" ry="4.6" fill="#efe9db"/>
    <ellipse cx="${der}" cy="100" rx="7.5" ry="4.6" fill="#efe9db"/>
    <circle cx="${izq + mirada}" cy="100.5" r="3.1" fill="${colorIris}"/>
    <circle cx="${der + mirada}" cy="100.5" r="3.1" fill="${colorIris}"/>
    <circle cx="${izq + mirada}" cy="100.5" r="1.4" fill="#17100a"/>
    <circle cx="${der + mirada}" cy="100.5" r="1.4" fill="#17100a"/>
    <circle cx="${izq + mirada - 1}" cy="99.3" r="0.8" fill="#fffdf4"/>
    <circle cx="${der + mirada - 1}" cy="99.3" r="0.8" fill="#fffdf4"/>
    <g class="parpado">
      <rect x="${izq - 8}" y="94.5" width="16" height="10" rx="4" fill="${colorPiel}"/>
      <rect x="${der - 8}" y="94.5" width="16" height="10" rx="4" fill="${colorPiel}"/>
    </g>
  </g>`;
}

const RETRATOS = {
  /* ── Marta Iriarte — ingeniera jefa: seca, angular, lentes rectos ──────── */
  marta: `
  ${FONDO}
  <!-- campera técnica de cuello alto -->
  <path d="M30,240 C34,196 60,174 100,171 C140,174 166,196 170,240 Z" fill="#45525c"/>
  <path d="M30,240 C33,204 48,186 70,178 L74,240 Z" fill="#3a464f"/>
  <path d="M170,240 C167,204 152,186 130,178 L126,240 Z" fill="#3a464f"/>
  <line x1="100" y1="184" x2="100" y2="240" stroke="#2c353c" stroke-width="3"/>
  <rect x="129" y="204" width="5" height="17" rx="1.5" fill="#ded6c4"/>
  <rect x="129" y="202" width="5" height="4" rx="1.5" fill="#8f867a"/>
  <!-- cuello -->
  <path d="M87,138 L113,138 L112,176 L88,176 Z" fill="#a97f61"/>
  <path d="M84,166 L100,176 L88,189 L74,177 Z" fill="#37424b"/>
  <path d="M116,166 L100,176 L112,189 L126,177 Z" fill="#37424b"/>
  <!-- orejas y cara -->
  <ellipse cx="66" cy="102" rx="6" ry="10" fill="#c99f7f"/>
  <ellipse cx="134" cy="102" rx="6" ry="10" fill="#c99f7f"/>
  <path d="M68,96 C68,58 81,44 100,44 C119,44 132,58 132,96
           C132,120 121,144 100,150 C79,144 68,120 68,96 Z" fill="#c99f7f"/>
  <path d="M88,143 C93,150 107,150 112,143 L112,152 C104,157 96,157 88,152 Z"
        fill="#a97f61" opacity="0.55"/>
  <!-- pelo: carré corto con canas -->
  <path d="M64,98 C62,52 82,36 100,36 C118,36 138,52 136,98 L129,98
           C129,72 119,57 100,57 C81,57 71,72 71,98 Z" fill="#6a5f58"/>
  <path d="M64,98 L71,98 C71,116 73,130 79,141 L67,136 C63,124 63,110 64,98 Z" fill="#6a5f58"/>
  <path d="M136,98 L129,98 C129,116 127,130 121,141 L133,136 C137,124 137,110 136,98 Z" fill="#6a5f58"/>
  <path d="M88,40 C96,38 104,38 112,41 L110,46 C103,43 96,43 90,45 Z" fill="#a29a92"/>
  <path d="M67,116 C66,124 67,130 69,135 L72,133 C70,128 69,122 69,116 Z" fill="#9d948c"/>
  <!-- cejas firmes, casi enojadas -->
  <path d="M76,89 L94,86.5" stroke="#4a3f37" stroke-width="3" stroke-linecap="round"/>
  <path d="M124,89 L106,86.5" stroke="#4a3f37" stroke-width="3" stroke-linecap="round"/>
  ${ojos("#c99f7f", "#4c3a2c", 15, -0.8)}
  <!-- lentes rectangulares -->
  <g fill="none" stroke="#2f2a24" stroke-width="2">
    <rect x="75" y="93" width="19" height="12" rx="2"/>
    <rect x="106" y="93" width="19" height="12" rx="2"/>
    <line x1="94" y1="98" x2="106" y2="98"/>
    <line x1="75" y1="97" x2="67" y2="95"/>
    <line x1="125" y1="97" x2="133" y2="95"/>
  </g>
  <!-- nariz y boca firme -->
  <path d="M100,102 L98,117 Q100,120 104,118" fill="none" stroke="#a97f61" stroke-width="2"
        stroke-linecap="round"/>
  <path class="boca-cerrada" d="M89,133 Q100,130 111,133" fill="none" stroke="#7e5a48"
        stroke-width="2.5" stroke-linecap="round"/>
  <ellipse class="boca-abierta" cx="100" cy="133.5" rx="6.5" ry="3.8" fill="#5b3a30"/>
  <path d="M84,124 Q86,127 89,127" fill="none" stroke="#a97f61" stroke-width="1.4" opacity="0.7"/>
  <path d="M116,124 Q114,127 111,127" fill="none" stroke="#a97f61" stroke-width="1.4" opacity="0.7"/>`,

  /* ── Julián Funes — técnico junior: joven, despeinado, cara de susto ───── */
  julian: `
  ${FONDO}
  <!-- buzo con capucha -->
  <path d="M30,240 C34,198 62,176 100,173 C138,176 166,198 170,240 Z" fill="#4d5560"/>
  <path d="M64,186 C70,176 84,170 100,170 C116,170 130,176 136,186
           C126,180 112,177 100,177 C88,177 74,180 64,186 Z" fill="#3e454e"/>
  <!-- chaleco reflectivo -->
  <path d="M50,240 C52,202 64,184 84,177 L92,189 L86,240 Z" fill="#d9992f"/>
  <path d="M150,240 C148,202 136,184 116,177 L108,189 L114,240 Z" fill="#d9992f"/>
  <rect x="55" y="208" width="29" height="8" fill="#e9e4d8" opacity="0.9" transform="rotate(4 69 212)"/>
  <rect x="116" y="208" width="29" height="8" fill="#e9e4d8" opacity="0.9" transform="rotate(-4 131 212)"/>
  <!-- credencial colgando torcida -->
  <path d="M86,176 L98,214" stroke="#b3392e" stroke-width="5" fill="none"/>
  <path d="M114,176 L102,214" stroke="#b3392e" stroke-width="5" fill="none"/>
  <rect x="92" y="212" width="17" height="21" rx="2" fill="#eae4d4" transform="rotate(-6 100 222)"/>
  <rect x="95" y="216" width="7" height="7" rx="1" fill="#8f867a" transform="rotate(-6 100 222)"/>
  <!-- cuello -->
  <path d="M88,140 L112,140 L111,177 L89,177 Z" fill="#b28565"/>
  <!-- orejas y cara redonda -->
  <ellipse cx="66" cy="104" rx="6.5" ry="10" fill="#d4a781"/>
  <ellipse cx="134" cy="104" rx="6.5" ry="10" fill="#d4a781"/>
  <path d="M68,98 C68,60 82,46 100,46 C118,46 132,60 132,98
           C132,124 120,147 100,152 C80,147 68,124 68,98 Z" fill="#d4a781"/>
  <path d="M88,145 C93,152 107,152 112,145 L112,154 C104,159 96,159 88,154 Z"
        fill="#b28565" opacity="0.5"/>
  <!-- rulos -->
  <g fill="#322821">
    <circle cx="72" cy="62" r="13"/>
    <circle cx="86" cy="50" r="14"/>
    <circle cx="102" cy="46" r="14"/>
    <circle cx="118" cy="51" r="13"/>
    <circle cx="130" cy="64" r="11"/>
    <circle cx="79" cy="52" r="10"/>
    <circle cx="94" cy="58" r="10"/>
    <circle cx="111" cy="57" r="10"/>
    <circle cx="124" cy="57" r="9"/>
    <circle cx="68" cy="74" r="8"/>
    <circle cx="132" cy="76" r="7"/>
  </g>
  <!-- cejas levantadas de preocupación -->
  <path d="M77,88 Q85,81 94,84" fill="none" stroke="#3d3128" stroke-width="2.8" stroke-linecap="round"/>
  <path d="M123,88 Q115,81 106,84" fill="none" stroke="#3d3128" stroke-width="2.8" stroke-linecap="round"/>
  ${ojos("#d4a781", "#54412f", 15, 0)}
  <!-- pecas -->
  <g fill="#a5764f" opacity="0.65">
    <circle cx="80" cy="115" r="1.1"/><circle cx="86" cy="118" r="1.1"/>
    <circle cx="83" cy="112" r="1"/><circle cx="120" cy="115" r="1.1"/>
    <circle cx="114" cy="118" r="1.1"/><circle cx="117" cy="112" r="1"/>
  </g>
  <!-- nariz y boca nerviosa -->
  <path d="M100,103 L99,118 Q101,121 105,119" fill="none" stroke="#b28565" stroke-width="2"
        stroke-linecap="round"/>
  <path class="boca-cerrada" d="M90,134 Q95,136.5 100,134.5 Q106,132.5 110,135.5" fill="none"
        stroke="#8a5c48" stroke-width="2.5" stroke-linecap="round"/>
  <ellipse class="boca-abierta" cx="100" cy="135" rx="6" ry="4.4" fill="#664033"/>
  <!-- gota de transpiración, pobre pibe -->
  <path d="M137,88 C139,92 140,95 138,97 C136,99 133,97 134,93 C134.5,91 136,89 137,88 Z"
        fill="#bcd8e0" opacity="0.85"/>`,

  /* ── Silvia Roldán — Calidad y Seguridad: rodete impecable, media sonrisa ─ */
  silvia: `
  ${FONDO}
  <!-- rodete detrás de la cabeza -->
  <circle cx="100" cy="40" r="14" fill="#241c16"/>
  <path d="M89,34 Q100,26 111,34" fill="none" stroke="#4a3a2c" stroke-width="2" opacity="0.7"/>
  <!-- buzo azul de Calidad (el detalle que Julián vio de lejos…) -->
  <path d="M30,240 C34,196 60,174 100,171 C140,174 166,196 170,240 Z" fill="#2f6390"/>
  <path d="M30,240 C33,206 46,188 66,180 L70,240 Z" fill="#275378"/>
  <path d="M170,240 C167,206 154,188 134,180 L130,240 Z" fill="#275378"/>
  <path d="M86,166 L100,174 L114,166 L114,178 L100,186 L86,178 Z" fill="#244d70"/>
  <line x1="100" y1="186" x2="100" y2="240" stroke="#1d405e" stroke-width="3"/>
  <circle cx="100" cy="196" r="2.4" fill="#c8d4de"/>
  <rect x="122" y="200" width="34" height="14" rx="2" fill="#dde4ea"/>
  <text x="139" y="210" text-anchor="middle" font-family="inherit" font-size="7"
        fill="#2f4459" letter-spacing="0.5">CALIDAD</text>
  <!-- cuello -->
  <path d="M88,138 L112,138 L111,174 L89,174 Z" fill="#a67e5f"/>
  <!-- orejas con perlitas -->
  <ellipse cx="66" cy="102" rx="6" ry="10" fill="#c69d7d"/>
  <ellipse cx="134" cy="102" rx="6" ry="10" fill="#c69d7d"/>
  <circle cx="65" cy="112" r="2.6" fill="#efe7dc"/>
  <circle cx="135" cy="112" r="2.6" fill="#efe7dc"/>
  <!-- cara ovalada y serena -->
  <path d="M69,96 C69,58 82,44 100,44 C118,44 131,58 131,96
           C131,121 120,144 100,149 C80,144 69,121 69,96 Z" fill="#c69d7d"/>
  <path d="M89,142 C94,149 106,149 111,142 L111,151 C103,156 97,156 89,151 Z"
        fill="#a67e5f" opacity="0.5"/>
  <!-- pelo tirante con raya al medio -->
  <path d="M66,100 C64,52 84,38 100,38 C116,38 136,52 134,100 L128,100
           C128,72 118,58 100,58 C82,58 72,72 72,100 Z" fill="#241c16"/>
  <path d="M100,39 L100,57" stroke="#0f0b08" stroke-width="1.6"/>
  <path d="M72,64 Q78,52 88,47" fill="none" stroke="#4a3a2c" stroke-width="1.6" opacity="0.8"/>
  <path d="M128,64 Q122,52 112,47" fill="none" stroke="#4a3a2c" stroke-width="1.6" opacity="0.8"/>
  <!-- cejas prolijas -->
  <path d="M77,88 Q85,84.5 93,87" fill="none" stroke="#3a2c20" stroke-width="2.6" stroke-linecap="round"/>
  <path d="M123,88 Q115,84.5 107,87" fill="none" stroke="#3a2c20" stroke-width="2.6" stroke-linecap="round"/>
  ${ojos("#c69d7d", "#45362a", 15, 0)}
  <!-- nariz y media sonrisa de manual -->
  <path d="M100,102 L99,116 Q101,119 104.5,117.5" fill="none" stroke="#a67e5f" stroke-width="2"
        stroke-linecap="round"/>
  <path class="boca-cerrada" d="M89,131 Q100,137 111,131" fill="none" stroke="#8a5744"
        stroke-width="2.5" stroke-linecap="round"/>
  <ellipse class="boca-abierta" cx="100" cy="133" rx="6.5" ry="4" fill="#5f3c31"/>`,
};

/** Devuelve el SVG completo (string) del retrato pedido. */
export function retrato(id) {
  const cuerpo = RETRATOS[id];
  if (!cuerpo) {
    // Un caso escrito por el jugador puede tener sospechosos sin retrato:
    // silueta anónima antes que romper la pantalla.
    return `<svg class="retrato" viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg"
      role="img" aria-label="sin retrato">${FONDO}
      <path d="M30,240 C34,198 62,176 100,173 C138,176 166,198 170,240 Z" fill="#4a4438"/>
      <circle cx="100" cy="98" r="34" fill="#5c5344"/>
      <text x="100" y="112" text-anchor="middle" font-size="40" fill="#cfc3a6">?</text>
    </svg>`;
  }
  // El delay del parpadeo varía por sospechoso para que no pestañeen en coro.
  const delay = { marta: "0s", julian: "1.4s", silvia: "2.6s" }[id] ?? "0s";
  return `<svg class="retrato retrato-${id}" viewBox="0 0 200 240"
    xmlns="http://www.w3.org/2000/svg" role="img" aria-label="retrato"
    style="--delay-parpadeo:${delay}">${cuerpo}</svg>`;
}
