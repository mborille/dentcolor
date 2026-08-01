# -*- coding: utf-8 -*-
"""
Suite de testes do dentcolor.

Roda com: python3 -m pytest tests/ -v
Ou direto:  python3 tests/test_dentcolor.py

A validacao externa contra colour-science so roda se o pacote estiver
instalado (pip install colour-science). Sem ele, os demais testes rodam
normalmente.
"""
import math
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dentcolor import (  # noqa: E402
    Lab,
    ciede2000,
    delta_e_cie76,
    classify_difference,
    lab_to_xyz,
    xyz_to_lab,
    lab_to_srgb,
    srgb_to_lab,
    lab_to_hex,
    hex_to_lab,
    in_srgb_gamut,
)

try:
    import numpy as np
    import colour
    TEM_COLOUR = True
except ImportError:
    TEM_COLOUR = False


class TestCIEDE2000(unittest.TestCase):
    """Propriedades matematicas exigidas pela CIE 142:2001."""

    def test_identidade(self):
        for lab in [(50, 0, 0), (0, 0, 0), (100, 0, 0), (73.5, 1.5, 14.3), (60, -40, 30)]:
            self.assertAlmostEqual(ciede2000(lab, lab), 0.0, places=12)

    def test_simetria(self):
        random.seed(42)
        for _ in range(20000):
            p = (random.uniform(0, 100), random.uniform(-100, 100), random.uniform(-100, 100))
            q = (random.uniform(0, 100), random.uniform(-100, 100), random.uniform(-100, 100))
            self.assertAlmostEqual(ciede2000(p, q), ciede2000(q, p), places=12)

    def test_nao_negativo(self):
        random.seed(7)
        for _ in range(20000):
            p = (random.uniform(0, 100), random.uniform(-128, 127), random.uniform(-128, 127))
            q = (random.uniform(0, 100), random.uniform(-128, 127), random.uniform(-128, 127))
            self.assertGreaterEqual(ciede2000(p, q), 0.0)

    def test_croma_zero(self):
        """Par acromatico nao pode gerar NaN nem divisao por zero."""
        d = ciede2000((50, 0, 0), (60, 0, 0))
        self.assertFalse(math.isnan(d))
        self.assertGreater(d, 0)

    def test_descontinuidade_de_matiz(self):
        """Continuidade ao cruzar 0/360 graus em h'."""
        base = (50, 0.0001, 2.5)
        antes = ciede2000(base, (50, -0.0001, 2.5))
        self.assertLess(antes, 0.05)

    def test_aceita_dataclass(self):
        a = Lab(50, 2.6772, -79.7751)
        b = Lab(50, 0, -82.7485)
        self.assertAlmostEqual(ciede2000(a, b), ciede2000(a.as_tuple(), b.as_tuple()), places=12)

    def test_conjunto_oficial_sharma(self):
        """
        Conformidade contra o conjunto de teste de Sharma, Wu e Dalal (2005).

        O arquivo NAO acompanha este pacote: baixe a tabela de 34 pares do
        material suplementar do artigo e salve em tests/sharma2005.csv com as
        colunas L1,a1,b1,L2,a2,b2,dE00. Sem o arquivo, este teste e pulado e
        a validacao numerica fica por conta de test_contra_colour_science.

        Esta separacao e proposital: o pacote nao redistribui dado de
        terceiro nem afirma conformidade que o usuario nao possa reproduzir.
        """
        caminho = os.path.join(os.path.dirname(__file__), "sharma2005.csv")
        if not os.path.exists(caminho):
            self.skipTest("tests/sharma2005.csv ausente; veja o docstring")

        import csv
        with open(caminho, newline="", encoding="utf-8") as fh:
            linhas = list(csv.DictReader(fh))
        self.assertGreater(len(linhas), 0, "csv vazio")
        for i, r in enumerate(linhas, 1):
            lab1 = (float(r["L1"]), float(r["a1"]), float(r["b1"]))
            lab2 = (float(r["L2"]), float(r["a2"]), float(r["b2"]))
            with self.subTest(par=i):
                self.assertAlmostEqual(ciede2000(lab1, lab2), float(r["dE00"]), places=4)

    def test_regressao_interna(self):
        """
        Valores de regressao desta implementacao.

        ATENCAO ao que estes numeros sao e ao que nao sao: foram gerados por
        esta biblioteca e conferidos contra colour-science 0.4.7, com
        concordancia melhor que 1e-12. Servem para detectar regressao entre
        versoes do pacote. NAO sao transcricao de tabela publicada, e nao
        devem ser citados como tal.
        """
        casos = [
            ((50.0, 2.6772, -79.7751), (50.0, 0.0, -82.7485), 2.0425),
            ((50.0, 0.0, 0.0), (50.0, -1.0, 2.0), 2.3669),
            ((50.0, 2.49, -0.001), (50.0, -2.49, 0.0009), 7.1792),
            ((50.0, 2.49, -0.001), (50.0, -2.49, 0.0011), 7.2195),
            ((50.0, 2.5, 0.0), (50.0, 0.0, -2.5), 4.3065),
            ((50.0, 2.5, 0.0), (73.0, 25.0, -18.0), 27.1492),
            ((60.2574, -34.0099, 36.2677), (60.4626, -34.1751, 39.4387), 1.2644),
            ((22.7233, 20.0904, -46.694), (23.0331, 14.973, -42.5619), 2.0373),
            ((90.8027, -2.0831, 1.441), (91.1528, -1.6435, 0.0447), 1.4441),
            ((2.0776, 0.0795, -1.135), (0.9033, -0.0636, -0.5514), 0.9082),
        ]
        for lab1, lab2, esperado in casos:
            with self.subTest(lab1=lab1, lab2=lab2):
                self.assertAlmostEqual(ciede2000(lab1, lab2), esperado, places=4)

    @unittest.skipUnless(TEM_COLOUR, "colour-science nao instalado")
    def test_contra_colour_science(self):
        random.seed(20260725)
        pior = 0.0
        for _ in range(50000):
            p = (random.uniform(0, 100), random.uniform(-128, 127), random.uniform(-128, 127))
            q = (random.uniform(0, 100), random.uniform(-128, 127), random.uniform(-128, 127))
            ref = float(colour.difference.delta_E_CIE2000(np.array(p), np.array(q)))
            pior = max(pior, abs(ciede2000(p, q) - ref))
        self.assertLess(pior, 1e-9, f"discrepancia maxima {pior:.3e}")


class TestConversoes(unittest.TestCase):

    def test_roundtrip_lab_xyz(self):
        random.seed(1)
        for _ in range(10000):
            lab = (random.uniform(0, 100), random.uniform(-100, 100), random.uniform(-100, 100))
            volta = xyz_to_lab(lab_to_xyz(lab)).as_tuple()
            for x, y in zip(lab, volta):
                self.assertAlmostEqual(x, y, places=9)

    def test_roundtrip_hex(self):
        random.seed(2)
        for _ in range(5000):
            rgb = [random.randint(0, 255) for _ in range(3)]
            h = f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"
            self.assertEqual(lab_to_hex(hex_to_lab(h)), h)

    def test_branco_e_preto(self):
        self.assertEqual(lab_to_hex((100, 0, 0)), "#FFFFFF")
        self.assertEqual(lab_to_hex((0, 0, 0)), "#000000")

    def test_cinza_neutro(self):
        """Cinza sRGB tem a e b proximos de zero em D65."""
        lab = srgb_to_lab([128, 128, 128])
        self.assertAlmostEqual(lab.a, 0.0, places=4)
        self.assertAlmostEqual(lab.b, 0.0, places=4)

    def test_gamut(self):
        self.assertTrue(in_srgb_gamut((50, 0, 0)))
        self.assertFalse(in_srgb_gamut((50, 120, -120)))

    def test_hex_invalido(self):
        for ruim in ["#12345", "xyzxyz", "", "#GGGGGG"]:
            with self.assertRaises(ValueError):
                hex_to_lab(ruim)


class TestLimiares(unittest.TestCase):

    def test_classificacao(self):
        self.assertEqual(classify_difference(0.4), "imperceptivel")
        self.assertEqual(classify_difference(1.2), "perceptivel_aceitavel")
        self.assertEqual(classify_difference(3.0), "inaceitavel")


class TestCIE76(unittest.TestCase):

    def test_euclidiana(self):
        self.assertAlmostEqual(delta_e_cie76((50, 0, 0), (50, 3, 4)), 5.0, places=12)


if __name__ == "__main__":
    unittest.main(verbosity=2)
