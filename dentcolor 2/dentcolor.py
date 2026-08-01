# -*- coding: utf-8 -*-
"""
dentcolor — colorimetria para odontologia restauradora.

Implementacao de referencia do CIEDE2000 (CIE 142:2001) e das conversoes
CIELAB <-> sRGB, com utilitarios de gamut e limiares perceptivos usados em
odontologia estetica.

ESCOPO: esta biblioteca fornece METODO, nao DADOS. Ela nao acompanha tabela
de coordenadas L*a*b* de nenhuma escala de cor comercial. Coordenadas de
escala devem ser medidas pelo proprio usuario, ou obtidas de fonte publicada
e citada, e carregadas conforme o esquema em schema/shade-table.schema.json.

Autor: Marcelo Barboza Borille (CRO-RS 14520)
DOI: 10.6084/m9.figshare.33087674
Licenca: MIT
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from typing import Iterable, Sequence

__version__ = "1.0.0"

__all__ = [
    "Lab",
    "ciede2000",
    "delta_e_cie76",
    "lab_to_xyz",
    "xyz_to_lab",
    "xyz_to_linear_srgb",
    "linear_srgb_to_xyz",
    "lab_to_srgb",
    "srgb_to_lab",
    "lab_to_hex",
    "hex_to_lab",
    "in_srgb_gamut",
    "PERCEPTIBILITY_THRESHOLD",
    "ACCEPTABILITY_THRESHOLD",
    "classify_difference",
    "load_shade_table",
    "nearest_shade",
]

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

#: Ponto branco D65, observador padrao 2 graus (CIE 1931), escala Y = 100.
D65_2DEG = (95.047, 100.000, 108.883)

#: Constantes da funcao de transferencia CIELAB (CIE 15:2004).
_EPSILON = 216.0 / 24389.0   # (6/29)^3
_KAPPA = 24389.0 / 27.0      # (29/3)^3

#: Limiar de perceptibilidade 50:50 em odontologia, em unidades de dE00.
#: FONTE A VERIFICAR ANTES DE PUBLICAR: Paravina et al., "Color difference
#: thresholds in dentistry", J Esthet Restor Dent, 2015. Confirme o valor e a
#: referencia completa no artigo original antes de citar.
PERCEPTIBILITY_THRESHOLD = 0.8

#: Limiar de aceitabilidade 50:50 em odontologia, em unidades de dE00.
#: MESMA RESSALVA DE FONTE acima.
ACCEPTABILITY_THRESHOLD = 1.8


@dataclass(frozen=True)
class Lab:
    """Cor em CIELAB. L em [0, 100]; a e b tipicamente em [-128, 127]."""

    L: float
    a: float
    b: float

    def as_tuple(self) -> tuple[float, float, float]:
        return (self.L, self.a, self.b)

    @property
    def chroma(self) -> float:
        """C*ab."""
        return math.hypot(self.a, self.b)

    @property
    def hue(self) -> float:
        """h_ab em graus, no intervalo [0, 360)."""
        if self.a == 0.0 and self.b == 0.0:
            return 0.0
        return math.degrees(math.atan2(self.b, self.a)) % 360.0


# ---------------------------------------------------------------------------
# Diferenca de cor
# ---------------------------------------------------------------------------

def ciede2000(
    lab1: Sequence[float] | Lab,
    lab2: Sequence[float] | Lab,
    kL: float = 1.0,
    kC: float = 1.0,
    kH: float = 1.0,
) -> float:
    """
    Diferenca de cor CIEDE2000 (dE00) entre duas cores CIELAB.

    Segue a formulacao de Sharma, Wu e Dalal (2005), incluindo o tratamento
    correto da descontinuidade de matiz em 0/360 graus e o caso croma zero.

    Parametros
    ----------
    lab1, lab2 : sequencia (L, a, b) ou Lab
    kL, kC, kH : fatores parametricos. O padrao 1:1:1 e o usado na maior
        parte da literatura odontologica.

    Retorna
    -------
    float : dE00, sempre >= 0. A funcao e simetrica.
    """
    L1, a1, b1 = lab1.as_tuple() if isinstance(lab1, Lab) else tuple(lab1)
    L2, a2, b2 = lab2.as_tuple() if isinstance(lab2, Lab) else tuple(lab2)

    C1 = math.hypot(a1, b1)
    C2 = math.hypot(a2, b2)
    C_bar = (C1 + C2) / 2.0
    C_bar7 = C_bar ** 7
    G = 0.5 * (1.0 - math.sqrt(C_bar7 / (C_bar7 + 25.0 ** 7)))

    a1p = (1.0 + G) * a1
    a2p = (1.0 + G) * a2
    C1p = math.hypot(a1p, b1)
    C2p = math.hypot(a2p, b2)

    h1p = 0.0 if (a1p == 0.0 and b1 == 0.0) else math.degrees(math.atan2(b1, a1p)) % 360.0
    h2p = 0.0 if (a2p == 0.0 and b2 == 0.0) else math.degrees(math.atan2(b2, a2p)) % 360.0

    dLp = L2 - L1
    dCp = C2p - C1p

    if C1p * C2p == 0.0:
        dhp = 0.0
    else:
        dhp = h2p - h1p
        if dhp > 180.0:
            dhp -= 360.0
        elif dhp < -180.0:
            dhp += 360.0
    dHp = 2.0 * math.sqrt(C1p * C2p) * math.sin(math.radians(dhp) / 2.0)

    L_bar_p = (L1 + L2) / 2.0
    C_bar_p = (C1p + C2p) / 2.0

    if C1p * C2p == 0.0:
        h_bar_p = h1p + h2p
    else:
        soma = h1p + h2p
        if abs(h1p - h2p) <= 180.0:
            h_bar_p = soma / 2.0
        elif soma < 360.0:
            h_bar_p = (soma + 360.0) / 2.0
        else:
            h_bar_p = (soma - 360.0) / 2.0

    T = (
        1.0
        - 0.17 * math.cos(math.radians(h_bar_p - 30.0))
        + 0.24 * math.cos(math.radians(2.0 * h_bar_p))
        + 0.32 * math.cos(math.radians(3.0 * h_bar_p + 6.0))
        - 0.20 * math.cos(math.radians(4.0 * h_bar_p - 63.0))
    )

    d_theta = 30.0 * math.exp(-(((h_bar_p - 275.0) / 25.0) ** 2))
    C_bar_p7 = C_bar_p ** 7
    R_C = 2.0 * math.sqrt(C_bar_p7 / (C_bar_p7 + 25.0 ** 7))

    S_L = 1.0 + (0.015 * (L_bar_p - 50.0) ** 2) / math.sqrt(20.0 + (L_bar_p - 50.0) ** 2)
    S_C = 1.0 + 0.045 * C_bar_p
    S_H = 1.0 + 0.015 * C_bar_p * T
    R_T = -math.sin(math.radians(2.0 * d_theta)) * R_C

    term_L = dLp / (kL * S_L)
    term_C = dCp / (kC * S_C)
    term_H = dHp / (kH * S_H)

    return math.sqrt(
        term_L * term_L + term_C * term_C + term_H * term_H + R_T * term_C * term_H
    )


def delta_e_cie76(lab1: Sequence[float] | Lab, lab2: Sequence[float] | Lab) -> float:
    """Diferenca euclidiana CIE76 (dEab). Incluida para comparacao historica."""
    L1, a1, b1 = lab1.as_tuple() if isinstance(lab1, Lab) else tuple(lab1)
    L2, a2, b2 = lab2.as_tuple() if isinstance(lab2, Lab) else tuple(lab2)
    return math.sqrt((L2 - L1) ** 2 + (a2 - a1) ** 2 + (b2 - b1) ** 2)


def classify_difference(de00: float) -> str:
    """
    Classifica um dE00 contra os limiares perceptivos.

    Retorna 'imperceptivel', 'perceptivel_aceitavel' ou 'inaceitavel'.
    Os limiares sao os definidos em PERCEPTIBILITY_THRESHOLD e
    ACCEPTABILITY_THRESHOLD; leia a ressalva de fonte junto das constantes.
    """
    if de00 < PERCEPTIBILITY_THRESHOLD:
        return "imperceptivel"
    if de00 <= ACCEPTABILITY_THRESHOLD:
        return "perceptivel_aceitavel"
    return "inaceitavel"


# ---------------------------------------------------------------------------
# Conversoes de espaco de cor
# ---------------------------------------------------------------------------

def lab_to_xyz(lab: Sequence[float] | Lab, white=D65_2DEG) -> tuple[float, float, float]:
    """CIELAB -> XYZ (escala 0..100)."""
    L, a, b = lab.as_tuple() if isinstance(lab, Lab) else tuple(lab)
    fy = (L + 16.0) / 116.0
    fx = fy + a / 500.0
    fz = fy - b / 200.0

    def finv(t: float) -> float:
        t3 = t ** 3
        return t3 if t3 > _EPSILON else (116.0 * t - 16.0) / _KAPPA

    xr = finv(fx)
    yr = (((L + 16.0) / 116.0) ** 3) if L > (_KAPPA * _EPSILON) else (L / _KAPPA)
    zr = finv(fz)
    Xw, Yw, Zw = white
    return (xr * Xw, yr * Yw, zr * Zw)


def xyz_to_lab(xyz: Sequence[float], white=D65_2DEG) -> Lab:
    """XYZ (escala 0..100) -> CIELAB."""
    X, Y, Z = xyz
    Xw, Yw, Zw = white
    xr, yr, zr = X / Xw, Y / Yw, Z / Zw

    def f(t: float) -> float:
        return t ** (1.0 / 3.0) if t > _EPSILON else (_KAPPA * t + 16.0) / 116.0

    fx, fy, fz = f(xr), f(yr), f(zr)
    return Lab(116.0 * fy - 16.0, 500.0 * (fx - fy), 200.0 * (fy - fz))


def xyz_to_linear_srgb(xyz: Sequence[float]) -> tuple[float, float, float]:
    """XYZ (0..100) -> sRGB linear (0..1, sem recorte)."""
    X, Y, Z = (v / 100.0 for v in xyz)
    r = 3.2404542 * X - 1.5371385 * Y - 0.4985314 * Z
    g = -0.9692660 * X + 1.8760108 * Y + 0.0415560 * Z
    b = 0.0556434 * X - 0.2040259 * Y + 1.0572252 * Z
    return (r, g, b)


def linear_srgb_to_xyz(rgb: Sequence[float]) -> tuple[float, float, float]:
    """sRGB linear (0..1) -> XYZ (0..100)."""
    r, g, b = rgb
    X = 0.4124564 * r + 0.3575761 * g + 0.1804375 * b
    Y = 0.2126729 * r + 0.7151522 * g + 0.0721750 * b
    Z = 0.0193339 * r + 0.1191920 * g + 0.9503041 * b
    return (X * 100.0, Y * 100.0, Z * 100.0)


def _encode_srgb(c: float) -> float:
    return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1.0 / 2.4)) - 0.055


def _decode_srgb(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def in_srgb_gamut(lab: Sequence[float] | Lab, tol: float = 1e-9) -> bool:
    """
    Informa se a cor cabe no gamut sRGB sem recorte.

    Relevante em odontologia: tons de dentina saturados e alguns tons
    clareados caem fora do sRGB, e o hex correspondente e uma aproximacao
    com perda. Verifique antes de publicar qualquer figura em tela.
    """
    return all(-tol <= v <= 1.0 + tol for v in xyz_to_linear_srgb(lab_to_xyz(lab)))


def lab_to_srgb(lab: Sequence[float] | Lab, clip: bool = True) -> tuple[int, int, int]:
    """CIELAB -> sRGB 8 bits. Com clip=True, recorta ao gamut."""
    lin = xyz_to_linear_srgb(lab_to_xyz(lab))
    out = []
    for v in lin:
        if clip:
            v = min(1.0, max(0.0, v))
        out.append(int(round(min(1.0, max(0.0, _encode_srgb(v))) * 255.0)))
    return tuple(out)  # type: ignore[return-value]


def srgb_to_lab(rgb: Sequence[int]) -> Lab:
    """sRGB 8 bits -> CIELAB."""
    lin = [_decode_srgb(v / 255.0) for v in rgb]
    return xyz_to_lab(linear_srgb_to_xyz(lin))


def lab_to_hex(lab: Sequence[float] | Lab, clip: bool = True) -> str:
    """CIELAB -> string hexadecimal '#RRGGBB' em maiusculas."""
    r, g, b = lab_to_srgb(lab, clip=clip)
    return f"#{r:02X}{g:02X}{b:02X}"


def hex_to_lab(value: str) -> Lab:
    """'#RRGGBB' ou 'RRGGBB' -> CIELAB."""
    h = value.strip().lstrip("#")
    if len(h) != 6:
        raise ValueError(f"hex invalido: {value!r}")
    return srgb_to_lab([int(h[i:i + 2], 16) for i in (0, 2, 4)])


# ---------------------------------------------------------------------------
# Tabelas de escala fornecidas pelo usuario
# ---------------------------------------------------------------------------

def load_shade_table(path: str) -> dict:
    """
    Carrega uma tabela de escala em JSON conforme schema/shade-table.schema.json.

    A biblioteca NAO acompanha tabela de nenhuma escala comercial. Meça a sua
    ou use fonte publicada e citada. O bloco 'provenance' do arquivo e
    obrigatorio: se ele nao estiver preenchido, a funcao avisa.
    """
    with open(path, "r", encoding="utf-8") as fh:
        table = json.load(fh)

    prov = table.get("provenance") or {}
    faltando = [k for k in ("status", "method", "instrument", "illuminant", "observer")
                if not prov.get(k)]
    if faltando:
        import warnings
        warnings.warn(
            "tabela de escala sem procedencia completa; campos ausentes: "
            + ", ".join(faltando)
            + ". Nao publique resultados derivados dela sem declarar isso.",
            stacklevel=2,
        )
    return table


def nearest_shade(
    target: Sequence[float] | Lab,
    table: dict,
    kL: float = 1.0,
    kC: float = 1.0,
    kH: float = 1.0,
) -> list[tuple[str, float]]:
    """
    Ordena os tons de uma tabela por dE00 crescente em relacao a cor alvo.

    Retorna lista de (nome_do_tom, dE00). O primeiro elemento e o mais proximo.
    """
    alvo = target.as_tuple() if isinstance(target, Lab) else tuple(target)
    resultado = []
    for tom in table.get("shades", []):
        lab = (tom["L"], tom["a"], tom["b"])
        resultado.append((tom["name"], ciede2000(alvo, lab, kL, kC, kH)))
    resultado.sort(key=lambda p: p[1])
    return resultado
