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

  /* ── Rocío — analista/jefa de Calidad: rodete tirante, blazer, precisión cansada ─ */
  rocio: `
  ${FONDO}
  <!-- blazer prolijo de QA -->
  <path d="M30,240 C34,198 60,176 100,173 C140,176 166,198 170,240 Z" fill="#3c5048"/>
  <path d="M30,240 C33,206 46,188 66,180 L70,240 Z" fill="#31423c"/>
  <path d="M170,240 C167,206 154,188 134,180 L130,240 Z" fill="#31423c"/>
  <path d="M86,168 L100,176 L114,168 L114,180 L100,188 L86,180 Z" fill="#e9e4d8"/>
  <rect x="96" y="188" width="8" height="30" fill="#8a6b45"/>
  <!-- cuello -->
  <path d="M88,140 L112,140 L111,176 L89,176 Z" fill="#9c7657"/>
  <!-- orejas y cara -->
  <ellipse cx="66" cy="102" rx="6" ry="10" fill="#c69d7d"/>
  <ellipse cx="134" cy="102" rx="6" ry="10" fill="#c69d7d"/>
  <path d="M69,96 C69,58 82,44 100,44 C118,44 131,58 131,96 C131,121 120,144 100,149 C80,144 69,121 69,96 Z" fill="#c69d7d"/>
  <path d="M89,142 C94,149 106,149 111,142 L111,151 C103,156 97,156 89,151 Z" fill="#9c7657" opacity="0.5"/>
  <!-- pelo: rodete tirante bajo -->
  <path d="M66,100 C64,54 84,40 100,40 C116,40 136,54 134,100 L128,100 C128,74 118,59 100,59 C82,59 72,74 72,100 Z" fill="#3a2f28"/>
  <circle cx="100" cy="188" r="11" fill="#3a2f28"/>
  <path d="M100,41 L100,58" stroke="#241c16" stroke-width="1.4"/>
  <!-- cejas rectas, firmes -->
  <path d="M77,88 L93,86" stroke="#2e2620" stroke-width="2.6" stroke-linecap="round"/>
  <path d="M123,88 L107,86" stroke="#2e2620" stroke-width="2.6" stroke-linecap="round"/>
  ${ojos("#c69d7d", "#4c3a2c", 15, 0)}
  <!-- nariz y boca fina, cansada -->
  <path d="M100,102 L99,116 Q101,119 104,117.5" fill="none" stroke="#9c7657" stroke-width="2"
        stroke-linecap="round"/>
  <path class="boca-cerrada" d="M90,132 L110,132" fill="none" stroke="#7e5a48" stroke-width="2.5"
        stroke-linecap="round"/>
  <ellipse class="boca-abierta" cx="100" cy="132.5" rx="6" ry="3.5" fill="#5b3a30"/>`,

  /* ── Facundo — técnico de ensayos, turno noche: joven, nervioso, ojeroso ──── */
  facundo: `
  ${FONDO}
  <!-- overol de planta, turno noche -->
  <path d="M30,240 C34,198 60,176 100,173 C140,176 166,198 170,240 Z" fill="#4a5568"/>
  <path d="M30,240 C33,206 46,188 66,180 L70,240 Z" fill="#3c4757"/>
  <path d="M170,240 C167,206 154,188 134,180 L130,240 Z" fill="#3c4757"/>
  <rect x="88" y="196" width="24" height="16" rx="2" fill="#8a94a3"/>
  <!-- cuello -->
  <path d="M88,140 L112,140 L111,177 L89,177 Z" fill="#c99a72"/>
  <!-- orejas y cara redonda -->
  <ellipse cx="66" cy="104" rx="6.5" ry="10" fill="#d4a781"/>
  <ellipse cx="134" cy="104" rx="6.5" ry="10" fill="#d4a781"/>
  <path d="M68,98 C68,60 82,46 100,46 C118,46 132,60 132,98 C132,124 120,147 100,152 C80,147 68,124 68,98 Z" fill="#d4a781"/>
  <path d="M88,145 C93,152 107,152 112,145 L112,154 C104,159 96,159 88,154 Z" fill="#c99a72" opacity="0.5"/>
  <!-- pelo corto despeinado -->
  <path d="M69,90 C67,58 82,44 100,44 C118,44 133,58 131,90 C126,82 118,86 118,78 C112,86 104,82 100,76
           C96,82 88,86 82,78 C82,86 74,82 69,90 Z" fill="#2e2419"/>
  <!-- cejas levantadas, ojeras de turno noche -->
  <path d="M77,87 Q85,81 94,84" fill="none" stroke="#241c16" stroke-width="2.6" stroke-linecap="round"/>
  <path d="M123,87 Q115,81 106,84" fill="none" stroke="#241c16" stroke-width="2.6" stroke-linecap="round"/>
  <path d="M78,110 Q85,112 91,110" fill="none" stroke="#a5764f" stroke-width="1.4" opacity="0.4"/>
  <path d="M122,110 Q115,112 109,110" fill="none" stroke="#a5764f" stroke-width="1.4" opacity="0.4"/>
  ${ojos("#d4a781", "#54412f", 15, 0)}
  <!-- nariz y boca nerviosa -->
  <path d="M100,103 L99,118 Q101,121 105,119" fill="none" stroke="#c99a72" stroke-width="2"
        stroke-linecap="round"/>
  <path class="boca-cerrada" d="M90,134 Q100,131 110,134" fill="none" stroke="#8a5c48" stroke-width="2.5"
        stroke-linecap="round"/>
  <ellipse class="boca-abierta" cx="100" cy="134.5" rx="6" ry="4" fill="#664033"/>`,

  /* ── Hernán — gerente/jefe de proyecto: calmo, calculador, traje y anteojos ── */
  hernan: `
  ${FONDO}
  <!-- traje gerencial -->
  <path d="M30,240 C34,196 60,174 100,171 C140,174 166,196 170,240 Z" fill="#3a3f4a"/>
  <path d="M30,240 C33,204 48,186 70,178 L74,240 Z" fill="#2e323b"/>
  <path d="M170,240 C167,204 152,186 130,178 L126,240 Z" fill="#2e323b"/>
  <path d="M88,178 L100,220 L112,178 Z" fill="#8f2f2f"/>
  <path d="M86,175 L100,184 L114,175 L114,182 L100,190 L86,182 Z" fill="#e9e4d8"/>
  <!-- cuello -->
  <path d="M87,138 L113,138 L112,176 L88,176 Z" fill="#b98561"/>
  <!-- orejas y cara -->
  <ellipse cx="66" cy="102" rx="6" ry="10" fill="#c1906a"/>
  <ellipse cx="134" cy="102" rx="6" ry="10" fill="#c1906a"/>
  <path d="M68,96 C68,58 81,44 100,44 C119,44 132,58 132,96 C132,120 121,144 100,150 C79,144 68,120 68,96 Z" fill="#c1906a"/>
  <path d="M88,143 C93,150 107,150 112,143 L112,152 C104,157 96,157 88,152 Z" fill="#b98561" opacity="0.55"/>
  <!-- pelo canoso, prolijo, entradas -->
  <path d="M67,92 C66,54 82,38 100,38 C118,38 134,54 133,92 C127,80 130,64 118,56 C122,64 116,68 108,62
           C110,70 100,66 100,58 C100,66 90,70 92,62 C84,68 78,64 82,56 C70,64 73,80 67,92 Z" fill="#8a7a6a"/>
  <!-- cejas firmes, media sonrisa calculadora -->
  <path d="M76,89 L94,87" stroke="#5a4f42" stroke-width="2.8" stroke-linecap="round"/>
  <path d="M124,89 L106,87" stroke="#5a4f42" stroke-width="2.8" stroke-linecap="round"/>
  ${ojos("#c1906a", "#4c3a2c", 15, 0)}
  <g fill="none" stroke="#2f2a24" stroke-width="2">
    <circle cx="85" cy="99" r="11"/>
    <circle cx="115" cy="99" r="11"/>
    <line x1="96" y1="99" x2="104" y2="99"/>
    <line x1="74" y1="97" x2="67" y2="95"/>
    <line x1="126" y1="97" x2="133" y2="95"/>
  </g>
  <!-- nariz y boca, media sonrisa profesional -->
  <path d="M100,102 L98,117 Q100,120 104,118" fill="none" stroke="#b98561" stroke-width="2"
        stroke-linecap="round"/>
  <path class="boca-cerrada" d="M89,132 Q100,136 111,132" fill="none" stroke="#7e5a48" stroke-width="2.5"
        stroke-linecap="round"/>
  <ellipse class="boca-abierta" cx="100" cy="133" rx="6.5" ry="3.8" fill="#5b3a30"/>`,

  /* ── Tomás — ingeniero de control, meticuloso pero blando para el conflicto ── */
  tomas: `
  ${FONDO}
  <!-- camisa de oficina técnica -->
  <path d="M30,240 C34,198 60,176 100,173 C140,176 166,198 170,240 Z" fill="#8f9199"/>
  <path d="M30,240 C33,206 46,188 66,180 L70,240 Z" fill="#797b83"/>
  <path d="M170,240 C167,206 154,188 134,180 L130,240 Z" fill="#797b83"/>
  <path d="M86,175 L100,184 L114,175 L114,182 L100,190 L86,182 Z" fill="#e9e4d8"/>
  <!-- cuello -->
  <path d="M88,140 L112,140 L111,177 L89,177 Z" fill="#c9a37f"/>
  <!-- orejas y cara -->
  <ellipse cx="66" cy="104" rx="6" ry="10" fill="#c9a37f"/>
  <ellipse cx="134" cy="104" rx="6" ry="10" fill="#c9a37f"/>
  <path d="M68,98 C68,60 82,46 100,46 C118,46 132,60 132,98 C132,123 120,146 100,151 C80,146 68,123 68,98 Z" fill="#c9a37f"/>
  <path d="M88,144 C93,151 107,151 112,144 L112,153 C104,158 96,158 88,153 Z" fill="#a9835f" opacity="0.5"/>
  <!-- pelo corto con raya al costado -->
  <path d="M68,94 C67,56 82,42 100,42 C118,42 133,56 132,94 L126,94 C126,68 116,55 100,55 C84,55 74,68 74,94 Z" fill="#4a3c2e"/>
  <path d="M74,58 L92,50" stroke="#2f251b" stroke-width="1.4" opacity="0.7"/>
  <!-- cejas inseguras, un poco caídas -->
  <path d="M77,89 Q86,87 94,89.5" fill="none" stroke="#3a2f24" stroke-width="2.6" stroke-linecap="round"/>
  <path d="M123,89 Q114,87 106,89.5" fill="none" stroke="#3a2f24" stroke-width="2.6" stroke-linecap="round"/>
  ${ojos("#c9a37f", "#3a2b1f", 15, 0)}
  <!-- mostacho prolijo -->
  <path d="M90,121 Q100,126 110,121 Q100,124 100,123 Q100,124 90,121 Z" fill="#3a2f24"/>
  <!-- nariz y boca -->
  <path d="M100,102 L99,117 Q101,120 104,118.5" fill="none" stroke="#a9835f" stroke-width="2"
        stroke-linecap="round"/>
  <path class="boca-cerrada" d="M91,133 Q100,131 109,133" fill="none" stroke="#8a5c48" stroke-width="2.5"
        stroke-linecap="round"/>
  <ellipse class="boca-abierta" cx="100" cy="133.5" rx="6" ry="3.8" fill="#664033"/>`,

  /* ── Nahuel — ingeniero/técnico junior: ansioso, perfeccionista, anteojos ──── */
  nahuel: `
  ${FONDO}
  <!-- buzo con capucha, informático -->
  <path d="M30,240 C34,198 62,176 100,173 C138,176 166,198 170,240 Z" fill="#5a4f6b"/>
  <path d="M64,186 C70,176 84,170 100,170 C116,170 130,176 136,186
           C126,180 112,177 100,177 C88,177 74,180 64,186 Z" fill="#463c58"/>
  <!-- cuello -->
  <path d="M88,140 L112,140 L111,177 L89,177 Z" fill="#d0a67d"/>
  <!-- orejas y cara redonda -->
  <ellipse cx="66" cy="104" rx="6.5" ry="10" fill="#d8b28c"/>
  <ellipse cx="134" cy="104" rx="6.5" ry="10" fill="#d8b28c"/>
  <path d="M68,98 C68,60 82,46 100,46 C118,46 132,60 132,98 C132,124 120,147 100,152 C80,147 68,124 68,98 Z" fill="#d8b28c"/>
  <path d="M88,145 C93,152 107,152 112,145 L112,154 C104,159 96,159 88,154 Z" fill="#b78c63" opacity="0.5"/>
  <!-- pelo rulado desprolijo -->
  <g fill="#2b2118">
    <circle cx="74" cy="64" r="11"/><circle cx="88" cy="52" r="12"/><circle cx="104" cy="48" r="12"/>
    <circle cx="119" cy="53" r="11"/><circle cx="129" cy="66" r="9"/><circle cx="96" cy="55" r="9"/><circle cx="111" cy="54" r="9"/>
  </g>
  <!-- cejas muy levantadas, ansioso -->
  <path d="M76,86 Q85,78 95,82" fill="none" stroke="#241c16" stroke-width="2.6" stroke-linecap="round"/>
  <path d="M124,86 Q115,78 105,82" fill="none" stroke="#241c16" stroke-width="2.6" stroke-linecap="round"/>
  ${ojos("#d8b28c", "#45362a", 15, 0)}
  <g fill="none" stroke="#5c5348" stroke-width="1.8">
    <rect x="75" y="93" width="19" height="12" rx="5"/>
    <rect x="106" y="93" width="19" height="12" rx="5"/>
    <line x1="94" y1="98" x2="106" y2="98"/>
  </g>
  <!-- nariz y boca tensa -->
  <path d="M100,103 L99,118 Q101,121 105,119" fill="none" stroke="#b78c63" stroke-width="2"
        stroke-linecap="round"/>
  <path class="boca-cerrada" d="M91,135 Q100,132.5 109,135" fill="none" stroke="#8a5c48" stroke-width="2.5"
        stroke-linecap="round"/>
  <ellipse class="boca-abierta" cx="100" cy="135.5" rx="6" ry="4.2" fill="#664033"/>`,

  /* ── Marisa — jefa de Metrología/Radioterapia: rodete, guardapolvo, ansiosa ── */
  marisa: `
  ${FONDO}
  <!-- guardapolvo de laboratorio -->
  <path d="M30,240 C34,198 60,176 100,173 C140,176 166,198 170,240 Z" fill="#e2ded2"/>
  <path d="M30,240 C33,206 46,188 66,180 L70,240 Z" fill="#c9c4b6"/>
  <path d="M170,240 C167,206 154,188 134,180 L130,240 Z" fill="#c9c4b6"/>
  <line x1="100" y1="186" x2="100" y2="240" stroke="#b3ada0" stroke-width="2"/>
  <!-- cuello -->
  <path d="M88,138 L112,138 L111,176 L89,176 Z" fill="#c69d7d"/>
  <!-- orejas y cara -->
  <ellipse cx="66" cy="102" rx="6" ry="10" fill="#c69d7d"/>
  <ellipse cx="134" cy="102" rx="6" ry="10" fill="#c69d7d"/>
  <path d="M69,96 C69,58 82,44 100,44 C118,44 131,58 131,96 C131,121 120,144 100,149 C80,144 69,121 69,96 Z" fill="#c69d7d"/>
  <path d="M89,142 C94,149 106,149 111,142 L111,151 C103,156 97,156 89,151 Z" fill="#a67e5f" opacity="0.5"/>
  <!-- pelo en rodete tirante -->
  <path d="M67,100 C65,54 83,39 100,39 C117,39 135,54 133,100 L127,100 C127,73 117,58 100,58 C83,58 73,73 73,100 Z" fill="#4a3c2e"/>
  <circle cx="100" cy="35" r="10" fill="#4a3c2e"/>
  <!-- cejas tensas -->
  <path d="M77,88 Q85,84 93,87" fill="none" stroke="#3a2f24" stroke-width="2.6" stroke-linecap="round"/>
  <path d="M123,88 Q115,84 107,87" fill="none" stroke="#3a2f24" stroke-width="2.6" stroke-linecap="round"/>
  ${ojos("#c69d7d", "#45362a", 15, 0)}
  <g fill="none" stroke="#403830" stroke-width="1.8">
    <rect x="76" y="93" width="18" height="11" rx="4"/>
    <rect x="106" y="93" width="18" height="11" rx="4"/>
    <line x1="94" y1="98" x2="106" y2="98"/>
  </g>
  <!-- nariz y boca fina, precisa -->
  <path d="M100,102 L99,116 Q101,119 104,117.5" fill="none" stroke="#a67e5f" stroke-width="2"
        stroke-linecap="round"/>
  <path class="boca-cerrada" d="M90,132 Q100,130 110,132" fill="none" stroke="#8a5744" stroke-width="2.5"
        stroke-linecap="round"/>
  <ellipse class="boca-abierta" cx="100" cy="132.5" rx="6" ry="3.6" fill="#5f3c31"/>`,

  /* ── Braian — técnico de service, vendedor nato, simpático ─────────────────── */
  braian: `
  ${FONDO}
  <!-- polo con parche de la empresa -->
  <path d="M30,240 C34,198 60,176 100,173 C140,176 166,198 170,240 Z" fill="#c94f3d"/>
  <path d="M30,240 C33,206 46,188 66,180 L70,240 Z" fill="#a83f30"/>
  <path d="M170,240 C167,206 154,188 134,180 L130,240 Z" fill="#a83f30"/>
  <rect x="118" y="196" width="20" height="14" rx="2" fill="#eae4d4"/>
  <!-- cuello -->
  <path d="M88,140 L112,140 L111,177 L89,177 Z" fill="#c9a37f"/>
  <!-- orejas y cara -->
  <ellipse cx="66" cy="104" rx="6" ry="10" fill="#c9a37f"/>
  <ellipse cx="134" cy="104" rx="6" ry="10" fill="#c9a37f"/>
  <path d="M68,98 C68,60 82,46 100,46 C118,46 132,60 132,98 C132,124 120,147 100,152 C80,147 68,124 68,98 Z" fill="#c9a37f"/>
  <path d="M88,145 C93,152 107,152 112,145 L112,154 C104,159 96,159 88,154 Z" fill="#a9835f" opacity="0.5"/>
  <!-- pelo con gel, peinado hacia atrás -->
  <path d="M69,92 C68,56 83,42 100,42 C117,42 132,56 131,92 C129,78 122,68 112,64 C118,72 114,78 106,72
           C108,80 100,76 100,68 C100,76 92,80 94,72 C86,78 82,72 88,64 C78,68 71,78 69,92 Z" fill="#241c16"/>
  <!-- cejas relajadas, sonrisa comercial -->
  <path d="M77,87 Q85,84 94,86.5" fill="none" stroke="#241c16" stroke-width="2.6" stroke-linecap="round"/>
  <path d="M123,87 Q115,84 106,86.5" fill="none" stroke="#241c16" stroke-width="2.6" stroke-linecap="round"/>
  ${ojos("#c9a37f", "#4c3a2c", 15, 0)}
  <!-- nariz y sonrisota -->
  <path d="M100,102 L99,117 Q101,120 104,118.5" fill="none" stroke="#a9835f" stroke-width="2"
        stroke-linecap="round"/>
  <path class="boca-cerrada" d="M88,131 Q100,140 112,131" fill="none" stroke="#7e5a48" stroke-width="2.5"
        stroke-linecap="round"/>
  <ellipse class="boca-abierta" cx="100" cy="134" rx="7" ry="4.4" fill="#5b3a30"/>`,

  /* ── Ricardo — veterano, calmo, mostacho, jefe de turno/compras ─────────────── */
  ricardo: `
  ${FONDO}
  <!-- coverall de sala de control, veterano -->
  <path d="M30,240 C34,196 60,174 100,171 C140,174 166,196 170,240 Z" fill="#4d5560"/>
  <path d="M30,240 C33,204 48,186 70,178 L74,240 Z" fill="#3e454e"/>
  <path d="M170,240 C167,204 152,186 130,178 L126,240 Z" fill="#3e454e"/>
  <rect x="86" y="196" width="28" height="10" rx="2" fill="#8f867a"/>
  <!-- cuello -->
  <path d="M87,138 L113,138 L112,176 L88,176 Z" fill="#b3835f"/>
  <!-- orejas y cara curtida -->
  <ellipse cx="65" cy="102" rx="6.5" ry="10.5" fill="#bb8862"/>
  <ellipse cx="135" cy="102" rx="6.5" ry="10.5" fill="#bb8862"/>
  <path d="M67,96 C67,57 81,43 100,43 C119,43 133,57 133,96 C133,121 121,145 100,151 C79,145 67,121 67,96 Z" fill="#bb8862"/>
  <path d="M88,144 C93,151 107,151 112,144 L112,153 C104,158 96,158 88,153 Z" fill="#96683f" opacity="0.55"/>
  <!-- pelo cano, prolijo hacia atrás -->
  <path d="M65,88 C64,52 81,37 100,37 C119,37 136,52 135,88 C131,72 121,60 100,60 C79,60 69,72 65,88 Z" fill="#a8a099"/>
  <!-- cejas gruesas, calma -->
  <path d="M75,88 L94,86" stroke="#8a827a" stroke-width="3" stroke-linecap="round"/>
  <path d="M125,88 L106,86" stroke="#8a827a" stroke-width="3" stroke-linecap="round"/>
  ${ojos("#bb8862", "#4c3a2c", 15, 0)}
  <!-- mostacho tupido -->
  <path d="M87,120 Q100,128 113,120 Q100,127 100,125 Q100,127 87,120 Z" fill="#8a827a"/>
  <!-- nariz recia y boca serena -->
  <path d="M100,101 L97,118 Q100,121 105,119" fill="none" stroke="#96683f" stroke-width="2.2"
        stroke-linecap="round"/>
  <path class="boca-cerrada" d="M90,133 L110,133" fill="none" stroke="#7e5a48" stroke-width="2.5"
        stroke-linecap="round"/>
  <ellipse class="boca-abierta" cx="100" cy="133.5" rx="6.5" ry="3.8" fill="#5b3a30"/>`,

  /* ── Nadia — operadora de guardia: meticulosa, nerviosa, trenza ─────────────── */
  nadia: `
  ${FONDO}
  <!-- uniforme de sala de control -->
  <path d="M30,240 C34,198 60,176 100,173 C140,176 166,198 170,240 Z" fill="#345066"/>
  <path d="M30,240 C33,206 46,188 66,180 L70,240 Z" fill="#2a4152"/>
  <path d="M170,240 C167,206 154,188 134,180 L130,240 Z" fill="#2a4152"/>
  <path d="M86,175 L100,184 L114,175 L114,182 L100,190 L86,182 Z" fill="#dde4ea"/>
  <!-- cuello -->
  <path d="M88,140 L112,140 L111,177 L89,177 Z" fill="#c9a37f"/>
  <!-- orejas y cara -->
  <ellipse cx="66" cy="104" rx="6" ry="10" fill="#cf9e78"/>
  <ellipse cx="134" cy="104" rx="6" ry="10" fill="#cf9e78"/>
  <path d="M68,98 C68,60 82,46 100,46 C118,46 132,60 132,98 C132,123 120,146 100,151 C80,146 68,123 68,98 Z" fill="#cf9e78"/>
  <path d="M88,144 C93,151 107,151 112,144 L112,153 C104,158 96,158 88,153 Z" fill="#a9835f" opacity="0.5"/>
  <!-- pelo en trenza -->
  <path d="M68,94 C67,56 82,42 100,42 C118,42 133,56 132,94 L126,94 C126,68 116,55 100,55 C84,55 74,68 74,94 Z" fill="#2e2419"/>
  <path d="M126,90 Q134,110 128,132 Q136,110 130,88 Z" fill="#2e2419"/>
  <circle cx="130" cy="110" r="1.6" fill="#1a1512"/><circle cx="129" cy="122" r="1.6" fill="#1a1512"/>
  <!-- cejas ansiosas -->
  <path d="M77,88 Q85,82 95,85" fill="none" stroke="#241c16" stroke-width="2.6" stroke-linecap="round"/>
  <path d="M123,88 Q115,82 105,85" fill="none" stroke="#241c16" stroke-width="2.6" stroke-linecap="round"/>
  ${ojos("#cf9e78", "#3a2b1f", 15, 0)}
  <!-- nariz y boca -->
  <path d="M100,103 L99,117 Q101,120 104,118.5" fill="none" stroke="#a9835f" stroke-width="2"
        stroke-linecap="round"/>
  <path class="boca-cerrada" d="M91,133 Q100,131 109,133.5" fill="none" stroke="#8a5c48" stroke-width="2.5"
        stroke-linecap="round"/>
  <ellipse class="boca-abierta" cx="100" cy="134" rx="6" ry="4" fill="#664033"/>`,

  /* ── Gustavo — técnico de instrumentación, callado, de pocas palabras ───────── */
  gustavo: `
  ${FONDO}
  <!-- camisa de leñador, técnico de instrumentación -->
  <path d="M30,240 C34,198 60,176 100,173 C140,176 166,198 170,240 Z" fill="#7a4234"/>
  <path d="M30,240 C33,206 46,188 66,180 L70,240 Z" fill="#63352a"/>
  <path d="M170,240 C167,206 154,188 134,180 L130,240 Z" fill="#63352a"/>
  <path d="M50,200 L150,200 M55,220 L145,220" stroke="#4a2a20" stroke-width="3" opacity="0.5"/>
  <!-- cuello -->
  <path d="M88,140 L112,140 L111,177 L89,177 Z" fill="#b3835f"/>
  <!-- orejas y cara -->
  <ellipse cx="66" cy="102" rx="6.5" ry="10.5" fill="#bb8862"/>
  <ellipse cx="134" cy="102" rx="6.5" ry="10.5" fill="#bb8862"/>
  <path d="M67,96 C67,57 81,43 100,43 C119,43 133,57 133,96 C133,121 121,145 100,151 C79,145 67,121 67,96 Z" fill="#bb8862"/>
  <path d="M88,144 C93,151 107,151 112,144 L112,153 C104,158 96,158 88,153 Z" fill="#96683f" opacity="0.55"/>
  <!-- pelo canoso ralo -->
  <path d="M70,86 C72,58 84,44 100,44 C116,44 128,58 130,86 C122,74 114,68 100,68 C86,68 78,74 70,86 Z" fill="#9a9088"/>
  <!-- cejas gruesas, silencioso -->
  <path d="M76,88 L94,87" stroke="#8a827a" stroke-width="2.8" stroke-linecap="round"/>
  <path d="M124,88 L106,87" stroke="#8a827a" stroke-width="2.8" stroke-linecap="round"/>
  ${ojos("#bb8862", "#5c4632", 15, 0)}
  <g fill="none" stroke="#403830" stroke-width="1.8">
    <rect x="76" y="93" width="18" height="11" rx="3"/>
    <rect x="106" y="93" width="18" height="11" rx="3"/>
    <line x1="94" y1="98" x2="106" y2="98"/>
  </g>
  <!-- nariz y boca cerrada -->
  <path d="M100,101 L98,118 Q100,121 105,119" fill="none" stroke="#96683f" stroke-width="2.2"
        stroke-linecap="round"/>
  <path class="boca-cerrada" d="M91,132 L109,132" fill="none" stroke="#7e5a48" stroke-width="2.5"
        stroke-linecap="round"/>
  <ellipse class="boca-abierta" cx="100" cy="132.5" rx="6" ry="3.6" fill="#5b3a30"/>`,

  /* ── César — técnico operador del acelerador: nervioso, habla de más ────────── */
  cesar: `
  ${FONDO}
  <!-- uniforme de acelerador, tipo ambo -->
  <path d="M30,240 C34,198 60,176 100,173 C140,176 166,198 170,240 Z" fill="#4d7a7a"/>
  <path d="M30,240 C33,206 46,188 66,180 L70,240 Z" fill="#3d6363"/>
  <path d="M170,240 C167,206 154,188 134,180 L130,240 Z" fill="#3d6363"/>
  <path d="M86,175 L100,184 L114,175 L114,182 L100,190 L86,182 Z" fill="#e9e4d8"/>
  <!-- cuello -->
  <path d="M88,140 L112,140 L111,177 L89,177 Z" fill="#c9a37f"/>
  <!-- orejas y cara -->
  <ellipse cx="66" cy="104" rx="6" ry="10" fill="#d0a67d"/>
  <ellipse cx="134" cy="104" rx="6" ry="10" fill="#d0a67d"/>
  <path d="M68,98 C68,60 82,46 100,46 C118,46 132,60 132,98 C132,123 120,146 100,151 C80,146 68,123 68,98 Z" fill="#d0a67d"/>
  <path d="M88,144 C93,151 107,151 112,144 L112,153 C104,158 96,158 88,153 Z" fill="#ab8058" opacity="0.5"/>
  <!-- pelo corto prolijo -->
  <path d="M69,92 C68,56 83,42 100,42 C117,42 132,56 131,92 L125,92 C125,66 115,53 100,53 C85,53 75,66 75,92 Z" fill="#3a2f24"/>
  <!-- cejas nerviosas, sube y baja -->
  <path d="M77,88 Q86,83 95,86" fill="none" stroke="#241c16" stroke-width="2.6" stroke-linecap="round"/>
  <path d="M123,88 Q114,83 105,86" fill="none" stroke="#241c16" stroke-width="2.6" stroke-linecap="round"/>
  ${ojos("#d0a67d", "#4c3a2c", 15, 0)}
  <!-- nariz y sonrisa nerviosa -->
  <path d="M100,103 L99,117 Q101,120 104,118.5" fill="none" stroke="#ab8058" stroke-width="2"
        stroke-linecap="round"/>
  <path class="boca-cerrada" d="M89,133 Q100,137 111,133" fill="none" stroke="#8a5c48" stroke-width="2.5"
        stroke-linecap="round"/>
  <ellipse class="boca-abierta" cx="100" cy="134.5" rx="6.5" ry="4.2" fill="#664033"/>`,

  /* ── Ariel — físico médico: metódico, monótono, sin expresión ───────────────── */
  ariel: `
  ${FONDO}
  <!-- guardapolvo de físico médico -->
  <path d="M30,240 C34,198 60,176 100,173 C140,176 166,198 170,240 Z" fill="#e2ded2"/>
  <path d="M30,240 C33,206 46,188 66,180 L70,240 Z" fill="#c9c4b6"/>
  <path d="M170,240 C167,206 154,188 134,180 L130,240 Z" fill="#c9c4b6"/>
  <line x1="100" y1="186" x2="100" y2="240" stroke="#b3ada0" stroke-width="2"/>
  <!-- cuello -->
  <path d="M88,140 L112,140 L111,176 L89,176 Z" fill="#b3835f"/>
  <!-- orejas y cara angulosa -->
  <ellipse cx="66" cy="102" rx="6" ry="10" fill="#bb8862"/>
  <ellipse cx="134" cy="102" rx="6" ry="10" fill="#bb8862"/>
  <path d="M68,96 C68,58 81,44 100,44 C119,44 132,58 132,96 C132,120 121,144 100,150 C79,144 68,120 68,96 Z" fill="#bb8862"/>
  <path d="M88,143 C93,150 107,150 112,143 L112,152 C104,157 96,157 88,152 Z" fill="#96683f" opacity="0.55"/>
  <!-- pelo corto muy prolijo -->
  <path d="M68,94 C67,54 82,40 100,40 C118,40 133,54 132,94 L126,94 C126,68 116,56 100,56 C84,56 74,68 74,94 Z" fill="#2e2419"/>
  <!-- cejas rectas, sin expresión -->
  <path d="M77,88 L94,87" stroke="#241c16" stroke-width="2.4" stroke-linecap="round"/>
  <path d="M123,88 L106,87" stroke="#241c16" stroke-width="2.4" stroke-linecap="round"/>
  ${ojos("#bb8862", "#3a2b1f", 15, 0)}
  <g fill="none" stroke="#2f2a24" stroke-width="2">
    <rect x="75" y="93" width="19" height="12" rx="2"/>
    <rect x="106" y="93" width="19" height="12" rx="2"/>
    <line x1="94" y1="98" x2="106" y2="98"/>
  </g>
  <!-- nariz y boca plana -->
  <path d="M100,102 L98,117 Q100,120 104,118" fill="none" stroke="#96683f" stroke-width="2"
        stroke-linecap="round"/>
  <path class="boca-cerrada" d="M90,132.5 L110,132.5" fill="none" stroke="#7e5a48" stroke-width="2.5"
        stroke-linecap="round"/>
  <ellipse class="boca-abierta" cx="100" cy="133" rx="6" ry="3.6" fill="#5b3a30"/>`,

  /* ── Marcela — ingeniera, brillante y perfeccionista, insegura fuera de lo técnico ─ */
  marcela: `
  ${FONDO}
  <!-- blazer de ingeniera -->
  <path d="M30,240 C34,198 60,176 100,173 C140,176 166,198 170,240 Z" fill="#4a3f5c"/>
  <path d="M30,240 C33,206 46,188 66,180 L70,240 Z" fill="#3c334c"/>
  <path d="M170,240 C167,206 154,188 134,180 L130,240 Z" fill="#3c334c"/>
  <path d="M86,168 L100,176 L114,168 L114,180 L100,188 L86,180 Z" fill="#e9e4d8"/>
  <!-- cuello -->
  <path d="M88,138 L112,138 L111,176 L89,176 Z" fill="#c9a37f"/>
  <!-- orejas y cara -->
  <ellipse cx="66" cy="102" rx="6" ry="10" fill="#c9a37f"/>
  <ellipse cx="134" cy="102" rx="6" ry="10" fill="#c9a37f"/>
  <path d="M69,96 C69,58 82,44 100,44 C118,44 131,58 131,96 C131,121 120,144 100,149 C80,144 69,121 69,96 Z" fill="#c9a37f"/>
  <path d="M89,142 C94,149 106,149 111,142 L111,151 C103,156 97,156 89,151 Z" fill="#a9835f" opacity="0.5"/>
  <!-- pelo suelto ondulado -->
  <path d="M66,102 C63,54 82,38 100,38 C118,38 137,54 134,102 C130,86 132,64 118,54 C124,68 118,78 108,68
           C112,80 100,74 100,60 C100,74 88,80 92,68 C82,78 76,68 82,54 C68,64 70,86 66,102 Z" fill="#3a2f24"/>
  <!-- cejas tensas, insegura -->
  <path d="M77,88 Q85,83 94,86" fill="none" stroke="#241c16" stroke-width="2.6" stroke-linecap="round"/>
  <path d="M123,88 Q115,83 106,86" fill="none" stroke="#241c16" stroke-width="2.6" stroke-linecap="round"/>
  ${ojos("#c9a37f", "#4c3a2c", 15, 0)}
  <!-- nariz y boca fina, tensa -->
  <path d="M100,102 L99,116 Q101,119 104,117.5" fill="none" stroke="#a9835f" stroke-width="2"
        stroke-linecap="round"/>
  <path class="boca-cerrada" d="M91,132 Q100,130 109,132" fill="none" stroke="#8a5744" stroke-width="2.5"
        stroke-linecap="round"/>
  <ellipse class="boca-abierta" cx="100" cy="132.5" rx="6" ry="3.6" fill="#5f3c31"/>`,

  /* ── Diego — técnico de sistemas, informal, gorra al revés, chistoso ────────── */
  diego: `
  ${FONDO}
  <!-- buzo informal -->
  <path d="M30,240 C34,198 62,176 100,173 C138,176 166,198 170,240 Z" fill="#5a6b4d"/>
  <path d="M64,186 C70,176 84,170 100,170 C116,170 130,176 136,186
           C126,180 112,177 100,177 C88,177 74,180 64,186 Z" fill="#485840"/>
  <!-- cuello -->
  <path d="M88,140 L112,140 L111,177 L89,177 Z" fill="#c69875"/>
  <!-- orejas y cara redonda -->
  <ellipse cx="66" cy="104" rx="6.5" ry="10" fill="#cf9e78"/>
  <ellipse cx="134" cy="104" rx="6.5" ry="10" fill="#cf9e78"/>
  <path d="M68,98 C68,60 82,46 100,46 C118,46 132,60 132,98 C132,124 120,147 100,152 C80,147 68,124 68,98 Z" fill="#cf9e78"/>
  <path d="M88,145 C93,152 107,152 112,145 L112,154 C104,159 96,159 88,154 Z" fill="#a9835f" opacity="0.5"/>
  <!-- gorra al revés -->
  <path d="M70,68 C70,50 83,40 100,40 C117,40 130,50 130,68 L130,80 L70,80 Z" fill="#8f2f2f"/>
  <path d="M118,74 L138,84 L118,86 Z" fill="#7a2626"/>
  <!-- cejas relajadas, sonrisa pícara -->
  <path d="M77,90 Q85,88 94,90.5" fill="none" stroke="#241c16" stroke-width="2.6" stroke-linecap="round"/>
  <path d="M123,90 Q115,88 106,90.5" fill="none" stroke="#241c16" stroke-width="2.6" stroke-linecap="round"/>
  ${ojos("#cf9e78", "#54412f", 15, 0.6)}
  <!-- nariz y sonrisa ladeada -->
  <path d="M100,103 L99,118 Q101,121 105,119" fill="none" stroke="#a9835f" stroke-width="2"
        stroke-linecap="round"/>
  <path class="boca-cerrada" d="M89,133 Q101,138 112,132" fill="none" stroke="#8a5c48" stroke-width="2.5"
        stroke-linecap="round"/>
  <ellipse class="boca-abierta" cx="101" cy="134.5" rx="6.5" ry="4.2" fill="#664033"/>`,

  /* ── Andrea — gestión de configuración: prolija, memoriosa, archiva todo ────── */
  andrea: `
  ${FONDO}
  <!-- cárdigan prolijo -->
  <path d="M30,240 C34,198 60,176 100,173 C140,176 166,198 170,240 Z" fill="#6b5a48"/>
  <path d="M30,240 C33,206 46,188 66,180 L70,240 Z" fill="#584a3a"/>
  <path d="M170,240 C167,206 154,188 134,180 L130,240 Z" fill="#584a3a"/>
  <line x1="100" y1="180" x2="100" y2="240" stroke="#453a2d" stroke-width="2"/>
  <circle cx="100" cy="196" r="2" fill="#eae4d4"/><circle cx="100" cy="214" r="2" fill="#eae4d4"/>
  <!-- cuello -->
  <path d="M88,138 L112,138 L111,176 L89,176 Z" fill="#c69d7d"/>
  <!-- orejas y cara -->
  <ellipse cx="66" cy="102" rx="6" ry="10" fill="#c69d7d"/>
  <ellipse cx="134" cy="102" rx="6" ry="10" fill="#c69d7d"/>
  <path d="M69,96 C69,58 82,44 100,44 C118,44 131,58 131,96 C131,121 120,144 100,149 C80,144 69,121 69,96 Z" fill="#c69d7d"/>
  <path d="M89,142 C94,149 106,149 111,142 L111,151 C103,156 97,156 89,151 Z" fill="#a67e5f" opacity="0.5"/>
  <!-- pelo en rodete muy tirante -->
  <path d="M67,100 C65,54 83,39 100,39 C117,39 135,54 133,100 L127,100 C127,73 117,58 100,58 C83,58 73,73 73,100 Z" fill="#55483c"/>
  <circle cx="100" cy="34" r="9" fill="#55483c"/>
  <!-- cejas rectas -->
  <path d="M77,88 L93,86.5" stroke="#3a2f24" stroke-width="2.6" stroke-linecap="round"/>
  <path d="M123,88 L107,86.5" stroke="#3a2f24" stroke-width="2.6" stroke-linecap="round"/>
  ${ojos("#c69d7d", "#45362a", 15, 0)}
  <g fill="none" stroke="#403830" stroke-width="1.8">
    <rect x="76" y="93" width="18" height="11" rx="2"/>
    <rect x="106" y="93" width="18" height="11" rx="2"/>
    <line x1="94" y1="98" x2="106" y2="98"/>
  </g>
  <!-- nariz y boca precisa -->
  <path d="M100,102 L99,116 Q101,119 104,117.5" fill="none" stroke="#a67e5f" stroke-width="2"
        stroke-linecap="round"/>
  <path class="boca-cerrada" d="M91,132 L109,132" fill="none" stroke="#8a5744" stroke-width="2.5"
        stroke-linecap="round"/>
  <ellipse class="boca-abierta" cx="100" cy="132.5" rx="6" ry="3.6" fill="#5f3c31"/>`,

  /* ── Claudia — ensayista/operadora de consola, turno noche, insegura ────────── */
  claudia: `
  ${FONDO}
  <!-- uniforme de consola nocturna -->
  <path d="M30,240 C34,198 60,176 100,173 C140,176 166,198 170,240 Z" fill="#3d4a5c"/>
  <path d="M30,240 C33,206 46,188 66,180 L70,240 Z" fill="#313c4a"/>
  <path d="M170,240 C167,206 154,188 134,180 L130,240 Z" fill="#313c4a"/>
  <path d="M86,175 L100,184 L114,175 L114,182 L100,190 L86,182 Z" fill="#dde4ea"/>
  <!-- cuello -->
  <path d="M88,140 L112,140 L111,177 L89,177 Z" fill="#c9a37f"/>
  <!-- orejas y cara -->
  <ellipse cx="66" cy="104" rx="6" ry="10" fill="#cf9e78"/>
  <ellipse cx="134" cy="104" rx="6" ry="10" fill="#cf9e78"/>
  <path d="M68,98 C68,60 82,46 100,46 C118,46 132,60 132,98 C132,123 120,146 100,151 C80,146 68,123 68,98 Z" fill="#cf9e78"/>
  <path d="M88,144 C93,151 107,151 112,144 L112,153 C104,158 96,158 88,153 Z" fill="#a9835f" opacity="0.5"/>
  <!-- pelo en cola de caballo -->
  <path d="M68,94 C67,56 82,42 100,42 C118,42 133,56 132,94 L126,94 C126,68 116,55 100,55 C84,55 74,68 74,94 Z" fill="#3a2f24"/>
  <path d="M127,88 Q138,104 132,126" fill="none" stroke="#3a2f24" stroke-width="7" stroke-linecap="round"/>
  <!-- ojeras de turno noche -->
  <path d="M79,110 Q86,113 92,110" fill="none" stroke="#7a5638" stroke-width="1.6" opacity="0.5"/>
  <path d="M121,110 Q114,113 108,110" fill="none" stroke="#7a5638" stroke-width="1.6" opacity="0.5"/>
  <!-- cejas inseguras -->
  <path d="M77,89 Q85,84 95,87" fill="none" stroke="#241c16" stroke-width="2.6" stroke-linecap="round"/>
  <path d="M123,89 Q115,84 105,87" fill="none" stroke="#241c16" stroke-width="2.6" stroke-linecap="round"/>
  ${ojos("#cf9e78", "#3a2b1f", 15, 0)}
  <!-- nariz y boca -->
  <path d="M100,103 L99,117 Q101,120 104,118.5" fill="none" stroke="#a9835f" stroke-width="2"
        stroke-linecap="round"/>
  <path class="boca-cerrada" d="M91,133 Q100,131 109,133.5" fill="none" stroke="#8a5c48" stroke-width="2.5"
        stroke-linecap="round"/>
  <ellipse class="boca-abierta" cx="100" cy="134" rx="6" ry="4" fill="#664033"/>`,

  /* ── Ovidio — técnico veterano de antena/RF: gruñón, mostacho, canoso ───────── */
  ovidio: `
  ${FONDO}
  <!-- camisa de trabajo curtida -->
  <path d="M30,240 C34,196 60,174 100,171 C140,174 166,196 170,240 Z" fill="#5c6b52"/>
  <path d="M30,240 C33,204 48,186 70,178 L74,240 Z" fill="#4a5642"/>
  <path d="M170,240 C167,204 152,186 130,178 L126,240 Z" fill="#4a5642"/>
  <!-- cuello -->
  <path d="M87,138 L113,138 L112,176 L88,176 Z" fill="#ad7a54"/>
  <!-- orejas grandes y cara curtida -->
  <ellipse cx="65" cy="103" rx="7" ry="11" fill="#b98661"/>
  <ellipse cx="135" cy="103" rx="7" ry="11" fill="#b98661"/>
  <path d="M67,97 C67,58 81,44 100,44 C119,44 133,58 133,97 C133,122 121,146 100,152 C79,146 67,122 67,97 Z" fill="#b98661"/>
  <path d="M88,145 C93,152 107,152 112,145 L112,154 C104,159 96,159 88,154 Z" fill="#96683f" opacity="0.55"/>
  <!-- surcos de la edad -->
  <path d="M78,112 Q85,115 91,112" fill="none" stroke="#8a5c38" stroke-width="1.2" opacity="0.5"/>
  <path d="M122,112 Q115,115 109,112" fill="none" stroke="#8a5c38" stroke-width="1.2" opacity="0.5"/>
  <!-- pelo cano ralo -->
  <path d="M71,84 C74,56 85,42 100,42 C115,42 126,56 129,84 C120,72 112,66 100,66 C88,66 80,72 71,84 Z" fill="#c9c2b8"/>
  <!-- cejas gruesas, mal genio contenido -->
  <path d="M75,89 L93,86" stroke="#a29a92" stroke-width="3" stroke-linecap="round"/>
  <path d="M125,89 L107,86" stroke="#a29a92" stroke-width="3" stroke-linecap="round"/>
  ${ojos("#b98661", "#4c3a2c", 15, 0)}
  <!-- mostacho canoso, tupido -->
  <path d="M86,120 Q100,130 114,120 Q100,128 100,126 Q100,128 86,120 Z" fill="#a29a92"/>
  <!-- nariz recia y boca inexpresiva -->
  <path d="M100,101 L97,119 Q100,122 105,119.5" fill="none" stroke="#96683f" stroke-width="2.2"
        stroke-linecap="round"/>
  <path class="boca-cerrada" d="M91,134 L109,134" fill="none" stroke="#7e5a48" stroke-width="2.5"
        stroke-linecap="round"/>
  <ellipse class="boca-abierta" cx="100" cy="134.5" rx="6" ry="3.6" fill="#5b3a30"/>`,

  /* ── Valeria — jefa de proyecto: exigida al límite, a la defensiva ──────────── */
  valeria: `
  ${FONDO}
  <!-- blazer de jefa de proyecto -->
  <path d="M30,240 C34,198 60,176 100,173 C140,176 166,198 170,240 Z" fill="#5c3f4a"/>
  <path d="M30,240 C33,206 46,188 66,180 L70,240 Z" fill="#4a333c"/>
  <path d="M170,240 C167,206 154,188 134,180 L130,240 Z" fill="#4a333c"/>
  <path d="M86,168 L100,176 L114,168 L114,180 L100,188 L86,180 Z" fill="#e9e4d8"/>
  <!-- cuello -->
  <path d="M88,138 L112,138 L111,176 L89,176 Z" fill="#c9a37f"/>
  <!-- orejas y cara -->
  <ellipse cx="66" cy="102" rx="6" ry="10" fill="#c9a37f"/>
  <ellipse cx="134" cy="102" rx="6" ry="10" fill="#c9a37f"/>
  <path d="M69,96 C69,58 82,44 100,44 C118,44 131,58 131,96 C131,121 120,144 100,149 C80,144 69,121 69,96 Z" fill="#c9a37f"/>
  <path d="M89,142 C94,149 106,149 111,142 L111,151 C103,156 97,156 89,151 Z" fill="#a9835f" opacity="0.5"/>
  <!-- pelo lacio, corto ejecutivo -->
  <path d="M65,100 C63,54 83,38 100,38 C117,38 137,54 135,100 L129,100 C129,72 118,57 100,57 C82,57 71,72 71,100 Z" fill="#241c16"/>
  <path d="M65,100 L71,100 C71,114 73,124 78,132 L68,128 C64,118 64,110 65,100 Z" fill="#241c16"/>
  <path d="M135,100 L129,100 C129,114 127,124 122,132 L132,128 C136,118 136,110 135,100 Z" fill="#241c16"/>
  <!-- cejas a la defensiva -->
  <path d="M76,88 Q85,84 95,87.5" fill="none" stroke="#241c16" stroke-width="2.8" stroke-linecap="round"/>
  <path d="M124,88 Q115,84 105,87.5" fill="none" stroke="#241c16" stroke-width="2.8" stroke-linecap="round"/>
  ${ojos("#c9a37f", "#2f2419", 15, 0)}
  <!-- nariz y boca firme -->
  <path d="M100,102 L99,116 Q101,119 104,117.5" fill="none" stroke="#a9835f" stroke-width="2"
        stroke-linecap="round"/>
  <path class="boca-cerrada" d="M89,132 Q100,129.5 111,132" fill="none" stroke="#8a5744" stroke-width="2.5"
        stroke-linecap="round"/>
  <ellipse class="boca-abierta" cx="100" cy="132.5" rx="6.5" ry="3.8" fill="#5f3c31"/>`,

  /* ── Walter — operador de guardia, primer año, muy nervioso ─────────────────── */
  walter: `
  ${FONDO}
  <!-- uniforme de guardia -->
  <path d="M30,240 C34,198 60,176 100,173 C140,176 166,198 170,240 Z" fill="#4a5245"/>
  <path d="M30,240 C33,206 46,188 66,180 L70,240 Z" fill="#3c4438"/>
  <path d="M170,240 C167,206 154,188 134,180 L130,240 Z" fill="#3c4438"/>
  <rect x="88" y="196" width="24" height="16" rx="2" fill="#d9992f"/>
  <!-- cuello -->
  <path d="M88,140 L112,140 L111,177 L89,177 Z" fill="#d0a67d"/>
  <!-- orejas y cara joven, redonda -->
  <ellipse cx="66" cy="104" rx="6.5" ry="10" fill="#d8b28c"/>
  <ellipse cx="134" cy="104" rx="6.5" ry="10" fill="#d8b28c"/>
  <path d="M68,98 C68,60 82,46 100,46 C118,46 132,60 132,98 C132,124 120,147 100,152 C80,147 68,124 68,98 Z" fill="#d8b28c"/>
  <path d="M88,145 C93,152 107,152 112,145 L112,154 C104,159 96,159 88,154 Z" fill="#b78c63" opacity="0.5"/>
  <!-- pelo corto -->
  <path d="M69,92 C68,56 83,42 100,42 C117,42 132,56 131,92 L125,92 C125,66 115,53 100,53 C85,53 75,66 75,92 Z" fill="#2e2419"/>
  <!-- cejas muy arriba, terror contenido -->
  <path d="M76,85 Q85,76 96,81" fill="none" stroke="#241c16" stroke-width="2.6" stroke-linecap="round"/>
  <path d="M124,85 Q115,76 104,81" fill="none" stroke="#241c16" stroke-width="2.6" stroke-linecap="round"/>
  ${ojos("#d8b28c", "#54412f", 16, 0)}
  <!-- gota de sudor, pobre pibe -->
  <path d="M137,88 C139,92 140,95 138,97 C136,99 133,97 134,93 C134.5,91 136,89 137,88 Z"
        fill="#bcd8e0" opacity="0.85"/>
  <!-- nariz y boca tensa -->
  <path d="M100,103 L99,118 Q101,121 105,119" fill="none" stroke="#b78c63" stroke-width="2"
        stroke-linecap="round"/>
  <path class="boca-cerrada" d="M90,135 Q100,133 110,135.5" fill="none" stroke="#8a5c48" stroke-width="2.5"
        stroke-linecap="round"/>
  <ellipse class="boca-abierta" cx="100" cy="135.5" rx="6" ry="4.4" fill="#664033"/>`,

  /* ── Nora — jefa de Administración de Contratos: controlada, persuasiva ─────── */
  nora: `
  ${FONDO}
  <!-- blazer ejecutivo -->
  <path d="M30,240 C34,198 60,176 100,173 C140,176 166,198 170,240 Z" fill="#38424a"/>
  <path d="M30,240 C33,206 46,188 66,180 L70,240 Z" fill="#2d353b"/>
  <path d="M170,240 C167,206 154,188 134,180 L130,240 Z" fill="#2d353b"/>
  <path d="M86,168 L100,176 L114,168 L114,180 L100,188 L86,180 Z" fill="#e9e4d8"/>
  <circle cx="100" cy="184" r="2.4" fill="#c8a45a"/>
  <!-- cuello -->
  <path d="M88,138 L112,138 L111,176 L89,176 Z" fill="#c1906a"/>
  <!-- orejas y cara -->
  <ellipse cx="66" cy="102" rx="6" ry="10" fill="#c1906a"/>
  <ellipse cx="134" cy="102" rx="6" ry="10" fill="#c1906a"/>
  <path d="M68,96 C68,58 81,44 100,44 C119,44 132,58 132,96 C132,120 121,144 100,150 C79,144 68,120 68,96 Z" fill="#c1906a"/>
  <path d="M88,143 C93,150 107,150 112,143 L112,152 C104,157 96,157 88,152 Z" fill="#96683f" opacity="0.5"/>
  <!-- pelo bob prolijo hasta el mentón -->
  <path d="M64,98 C62,52 82,36 100,36 C118,36 138,52 136,98 L129,98 C129,72 119,57 100,57 C81,57 71,72 71,98 Z" fill="#4a3c2e"/>
  <path d="M64,98 L71,98 C71,112 72,122 75,130 L66,128 C63,118 63,108 64,98 Z" fill="#4a3c2e"/>
  <path d="M136,98 L129,98 C129,112 128,122 125,130 L134,128 C137,118 137,108 136,98 Z" fill="#4a3c2e"/>
  <!-- cejas controladas -->
  <path d="M76,88 L94,87" stroke="#3a2f24" stroke-width="2.6" stroke-linecap="round"/>
  <path d="M124,88 L106,87" stroke="#3a2f24" stroke-width="2.6" stroke-linecap="round"/>
  ${ojos("#c1906a", "#45362a", 15, 0)}
  <!-- nariz y sonrisa contenida -->
  <path d="M100,102 L98,117 Q100,120 104,118" fill="none" stroke="#96683f" stroke-width="2"
        stroke-linecap="round"/>
  <path class="boca-cerrada" d="M90,131 Q100,134.5 110,131" fill="none" stroke="#7e5a48" stroke-width="2.5"
        stroke-linecap="round"/>
  <ellipse class="boca-abierta" cx="100" cy="132.5" rx="6" ry="3.6" fill="#5b3a30"/>`,

  /* ── Marcelo — gerente de proyecto: campechano, cansado, culposo ────────────── */
  marcelo: `
  ${FONDO}
  <!-- camisa con corbata floja -->
  <path d="M30,240 C34,196 60,174 100,171 C140,174 166,196 170,240 Z" fill="#8f9199"/>
  <path d="M30,240 C33,204 48,186 70,178 L74,240 Z" fill="#797b83"/>
  <path d="M170,240 C167,204 152,186 130,178 L126,240 Z" fill="#797b83"/>
  <path d="M92,178 L100,215 L108,178 Z" fill="#4a5568"/>
  <path d="M86,175 L100,184 L114,175 L114,182 L100,190 L86,182 Z" fill="#e9e4d8"/>
  <!-- cuello -->
  <path d="M87,138 L113,138 L112,176 L88,176 Z" fill="#b3835f"/>
  <!-- orejas y cara cansada -->
  <ellipse cx="66" cy="102" rx="6" ry="10" fill="#bb8862"/>
  <ellipse cx="134" cy="102" rx="6" ry="10" fill="#bb8862"/>
  <path d="M68,96 C68,58 81,44 100,44 C119,44 132,58 132,96 C132,120 121,144 100,150 C79,144 68,120 68,96 Z" fill="#bb8862"/>
  <path d="M88,143 C93,150 107,150 112,143 L112,152 C104,157 96,157 88,152 Z" fill="#96683f" opacity="0.55"/>
  <!-- bolsas bajo los ojos -->
  <path d="M78,111 Q86,114 92,111" fill="none" stroke="#7a5638" stroke-width="1.6" opacity="0.5"/>
  <path d="M122,111 Q114,114 108,111" fill="none" stroke="#7a5638" stroke-width="1.6" opacity="0.5"/>
  <!-- pelo canoso, entradas marcadas -->
  <path d="M69,90 C68,54 82,40 100,40 C118,40 132,54 131,90 C125,76 128,62 116,56 C120,66 112,70 106,64
           C108,72 100,68 100,60 C100,68 92,72 94,64 C88,70 80,66 84,56 C72,62 75,76 69,90 Z" fill="#9a9088"/>
  <!-- cejas caídas, culpa -->
  <path d="M77,90 Q85,88 93,90.5" fill="none" stroke="#5a4f42" stroke-width="2.6" stroke-linecap="round"/>
  <path d="M123,90 Q115,88 107,90.5" fill="none" stroke="#5a4f42" stroke-width="2.6" stroke-linecap="round"/>
  ${ojos("#bb8862", "#4c3a2c", 15, 0)}
  <!-- nariz y boca caída -->
  <path d="M100,102 L98,117 Q100,120 104,118" fill="none" stroke="#96683f" stroke-width="2"
        stroke-linecap="round"/>
  <path class="boca-cerrada" d="M90,134 Q100,131 110,134" fill="none" stroke="#7e5a48" stroke-width="2.5"
        stroke-linecap="round"/>
  <ellipse class="boca-abierta" cx="100" cy="134.5" rx="6.5" ry="3.8" fill="#5b3a30"/>`,
};

/** El delay del parpadeo varía por sospechoso (determinístico, según el id)
 * para que ningún par pestañee en coro. Se comparte con pixelart.js. */
export function delayParpadeo(id) {
  let hash = 0;
  for (const caracter of id) hash = (hash * 31 + caracter.charCodeAt(0)) % 30;
  return `${(hash / 10).toFixed(1)}s`;
}

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
  return `<svg class="retrato retrato-${id}" viewBox="0 0 200 240"
    xmlns="http://www.w3.org/2000/svg" role="img" aria-label="retrato"
    style="--delay-parpadeo:${delayParpadeo(id)}">${cuerpo}</svg>`;
}
