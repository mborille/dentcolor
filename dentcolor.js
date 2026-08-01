/**
 * dentcolor — colorimetria para odontologia restauradora.
 *
 * Porte JavaScript da implementação de referência do CIEDE2000 (CIE 142:2001)
 * e das conversões CIELAB <-> sRGB. Numericamente equivalente à versão Python
 * do mesmo pacote (concordância verificada abaixo de 1e-9 em dE00).
 *
 * ESCOPO: esta biblioteca fornece MÉTODO, não DADOS. Não acompanha tabela de
 * coordenadas L*a*b* de nenhuma escala de cor comercial.
 *
 * Autor: Marcelo Barboza Borille (CRO-RS 14520)
 * DOI: 10.6084/m9.figshare.33087674
 * Licença: MIT
 */

export const VERSION = "1.0.0";

/** Ponto branco D65, observador padrão 2 graus (CIE 1931), escala Y = 100. */
export const D65_2DEG = [95.047, 100.0, 108.883];

const EPSILON = 216 / 24389; // (6/29)^3
const KAPPA = 24389 / 27; // (29/3)^3

=========================================================
BLOCO PARA SUBSTITUIR NO dentcolor.js  (linhas ~24 a 32)
=========================================================

Onde está:

  /**
   * Limiar de perceptibilidade 50:50 em odontologia, em unidades de dE00.
   * FONTE A VERIFICAR ANTES DE PUBLICAR: Paravina et al., "Color difference
   * thresholds in dentistry", J Esthet Restor Dent, 2015.
   */
  export const PERCEPTIBILITY_THRESHOLD = 0.8;

  /** Limiar de aceitabilidade 50:50 em odontologia. Mesma ressalva de fonte. */
  export const ACCEPTABILITY_THRESHOLD = 1.8;

Colocar:

  /**
   * Limiares visuais 50:50 em odontologia, em unidades de dE00.
   *
   * Fonte: Paravina RD, Ghinea R, Herrera LJ, Bona AD, Igiel C, Linninger M,
   * Sakai M, Takahashi H, Tashkandi E, Perez MdelM. Color difference
   * thresholds in dentistry. J Esthet Restor Dent. 2015;27 Suppl 1:S1-9.
   * doi:10.1111/jerd.12149 - PMID 25886208
   *
   * Determinados para ceramica monocromatica em cabine de visualizacao.
   * Sao referencia de controle de qualidade, nao criterio clinico automatico:
   * o estudo relata diferenca significativa entre grupos de observadores.
   */
  export const PERCEPTIBILITY_THRESHOLD = 0.8;
  export const ACCEPTABILITY_THRESHOLD = 1.8;


=========================================================
EQUIVALENTE PARA O dentcolor.py
=========================================================

  # Limiares visuais 50:50 em odontologia, em unidades de dE00.
  #
  # Fonte: Paravina RD, Ghinea R, Herrera LJ, Bona AD, Igiel C, Linninger M,
  # Sakai M, Takahashi H, Tashkandi E, Perez MdelM. Color difference
  # thresholds in dentistry. J Esthet Restor Dent. 2015;27 Suppl 1:S1-9.
  # doi:10.1111/jerd.12149 - PMID 25886208
  #
  # Determinados para ceramica monocromatica em cabine de visualizacao.
  # Sao referencia de controle de qualidade, nao criterio clinico automatico:
  # o estudo relata diferenca significativa entre grupos de observadores.
  PERCEPTIBILITY_THRESHOLD = 0.8
  ACCEPTABILITY_THRESHOLD = 1.8


=========================================================
OBSERVACAO
=========================================================

Confira o texto exato que esta hoje no dentcolor.py antes de substituir.
Eu vi o cabecalho do .js na sua tela, mas nao vi o do .py, entao o bloco
acima e o equivalente em sintaxe Python, nao uma copia do que esta la.

Mensagem de commit sugerida para os dois arquivos:

  Substituir nota "fonte a verificar" pela citacao completa de Paravina 2015

const rad = (d) => (d * Math.PI) / 180;
const deg = (r) => (r * 180) / Math.PI;

/**
 * Diferença de cor CIEDE2000 entre duas cores CIELAB.
 * @param {number[]} lab1 [L, a, b]
 * @param {number[]} lab2 [L, a, b]
 * @param {number} [kL=1] @param {number} [kC=1] @param {number} [kH=1]
 * @returns {number} dE00, sempre >= 0. Simétrica.
 */
export function ciede2000(lab1, lab2, kL = 1, kC = 1, kH = 1) {
  const [L1, a1, b1] = lab1;
  const [L2, a2, b2] = lab2;

  const C1 = Math.hypot(a1, b1);
  const C2 = Math.hypot(a2, b2);
  const Cbar = (C1 + C2) / 2;
  const Cbar7 = Math.pow(Cbar, 7);
  const G = 0.5 * (1 - Math.sqrt(Cbar7 / (Cbar7 + Math.pow(25, 7))));

  const a1p = (1 + G) * a1;
  const a2p = (1 + G) * a2;
  const C1p = Math.hypot(a1p, b1);
  const C2p = Math.hypot(a2p, b2);

  const h1p = a1p === 0 && b1 === 0 ? 0 : ((deg(Math.atan2(b1, a1p)) % 360) + 360) % 360;
  const h2p = a2p === 0 && b2 === 0 ? 0 : ((deg(Math.atan2(b2, a2p)) % 360) + 360) % 360;

  const dLp = L2 - L1;
  const dCp = C2p - C1p;

  let dhp = 0;
  if (C1p * C2p !== 0) {
    dhp = h2p - h1p;
    if (dhp > 180) dhp -= 360;
    else if (dhp < -180) dhp += 360;
  }
  const dHp = 2 * Math.sqrt(C1p * C2p) * Math.sin(rad(dhp) / 2);

  const LbarP = (L1 + L2) / 2;
  const CbarP = (C1p + C2p) / 2;

  let hbarP;
  if (C1p * C2p === 0) {
    hbarP = h1p + h2p;
  } else {
    const soma = h1p + h2p;
    if (Math.abs(h1p - h2p) <= 180) hbarP = soma / 2;
    else if (soma < 360) hbarP = (soma + 360) / 2;
    else hbarP = (soma - 360) / 2;
  }

  const T =
    1 -
    0.17 * Math.cos(rad(hbarP - 30)) +
    0.24 * Math.cos(rad(2 * hbarP)) +
    0.32 * Math.cos(rad(3 * hbarP + 6)) -
    0.2 * Math.cos(rad(4 * hbarP - 63));

  const dTheta = 30 * Math.exp(-Math.pow((hbarP - 275) / 25, 2));
  const CbarP7 = Math.pow(CbarP, 7);
  const RC = 2 * Math.sqrt(CbarP7 / (CbarP7 + Math.pow(25, 7)));

  const SL = 1 + (0.015 * Math.pow(LbarP - 50, 2)) / Math.sqrt(20 + Math.pow(LbarP - 50, 2));
  const SC = 1 + 0.045 * CbarP;
  const SH = 1 + 0.015 * CbarP * T;
  const RT = -Math.sin(rad(2 * dTheta)) * RC;

  const tL = dLp / (kL * SL);
  const tC = dCp / (kC * SC);
  const tH = dHp / (kH * SH);

  return Math.sqrt(tL * tL + tC * tC + tH * tH + RT * tC * tH);
}

/** Diferença euclidiana CIE76 (dEab). Incluída para comparação histórica. */
export function deltaECIE76(lab1, lab2) {
  return Math.hypot(lab2[0] - lab1[0], lab2[1] - lab1[1], lab2[2] - lab1[2]);
}

/** Classifica um dE00 contra os limiares perceptivos. */
export function classifyDifference(de00) {
  if (de00 < PERCEPTIBILITY_THRESHOLD) return "imperceptivel";
  if (de00 <= ACCEPTABILITY_THRESHOLD) return "perceptivel_aceitavel";
  return "inaceitavel";
}

/** CIELAB -> XYZ (escala 0..100). */
export function labToXyz([L, a, b], white = D65_2DEG) {
  const fy = (L + 16) / 116;
  const fx = fy + a / 500;
  const fz = fy - b / 200;
  const finv = (t) => {
    const t3 = t * t * t;
    return t3 > EPSILON ? t3 : (116 * t - 16) / KAPPA;
  };
  const xr = finv(fx);
  const yr = L > KAPPA * EPSILON ? Math.pow((L + 16) / 116, 3) : L / KAPPA;
  const zr = finv(fz);
  return [xr * white[0], yr * white[1], zr * white[2]];
}

/** XYZ (escala 0..100) -> CIELAB. */
export function xyzToLab([X, Y, Z], white = D65_2DEG) {
  const xr = X / white[0];
  const yr = Y / white[1];
  const zr = Z / white[2];
  const f = (t) => (t > EPSILON ? Math.cbrt(t) : (KAPPA * t + 16) / 116);
  const fx = f(xr);
  const fy = f(yr);
  const fz = f(zr);
  return [116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)];
}

/** XYZ (0..100) -> sRGB linear (0..1, sem recorte). */
export function xyzToLinearSrgb([X, Y, Z]) {
  const x = X / 100;
  const y = Y / 100;
  const z = Z / 100;
  return [
    3.2404542 * x - 1.5371385 * y - 0.4985314 * z,
    -0.969266 * x + 1.8760108 * y + 0.041556 * z,
    0.0556434 * x - 0.2040259 * y + 1.0572252 * z,
  ];
}

/** sRGB linear (0..1) -> XYZ (0..100). */
export function linearSrgbToXyz([r, g, b]) {
  return [
    (0.4124564 * r + 0.3575761 * g + 0.1804375 * b) * 100,
    (0.2126729 * r + 0.7151522 * g + 0.072175 * b) * 100,
    (0.0193339 * r + 0.119192 * g + 0.9503041 * b) * 100,
  ];
}

const encodeSrgb = (c) => (c <= 0.0031308 ? 12.92 * c : 1.055 * Math.pow(c, 1 / 2.4) - 0.055);
const decodeSrgb = (c) => (c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4));

/**
 * Informa se a cor cabe no gamut sRGB sem recorte.
 * Tons de dentina saturados e alguns tons clareados caem fora do sRGB.
 */
export function inSrgbGamut(lab, tol = 1e-9) {
  return xyzToLinearSrgb(labToXyz(lab)).every((v) => v >= -tol && v <= 1 + tol);
}

/** CIELAB -> sRGB 8 bits. */
export function labToSrgb(lab, clip = true) {
  return xyzToLinearSrgb(labToXyz(lab)).map((v) => {
    const x = clip ? Math.min(1, Math.max(0, v)) : v;
    return Math.round(Math.min(1, Math.max(0, encodeSrgb(x))) * 255);
  });
}

/** sRGB 8 bits -> CIELAB. */
export function srgbToLab(rgb) {
  return xyzToLab(linearSrgbToXyz(rgb.map((v) => decodeSrgb(v / 255))));
}

/** CIELAB -> '#RRGGBB' em maiúsculas. */
export function labToHex(lab, clip = true) {
  return (
    "#" +
    labToSrgb(lab, clip)
      .map((v) => v.toString(16).toUpperCase().padStart(2, "0"))
      .join("")
  );
}

/** '#RRGGBB' ou 'RRGGBB' -> CIELAB. */
export function hexToLab(value) {
  const h = value.trim().replace(/^#/, "");
  if (!/^[0-9a-fA-F]{6}$/.test(h)) throw new Error(`hex invalido: ${value}`);
  return srgbToLab([0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16)));
}

/**
 * Ordena os tons de uma tabela por dE00 crescente em relação à cor alvo.
 * @param {number[]} target [L, a, b]
 * @param {{shades: {name: string, L: number, a: number, b: number}[]}} table
 * @returns {{name: string, de00: number}[]}
 */
export function nearestShade(target, table, kL = 1, kC = 1, kH = 1) {
  return (table.shades || [])
    .map((s) => ({ name: s.name, de00: ciede2000(target, [s.L, s.a, s.b], kL, kC, kH) }))
    .sort((x, y) => x.de00 - y.de00);
}
