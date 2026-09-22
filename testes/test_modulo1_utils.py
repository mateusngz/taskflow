"""
Testes do Módulo 1. Rode com:
    python3 -m unittest discover testes
"""

import unittest
from datetime import date

from modulo1_utils.datas import parse_data, dias_ate_prazo
from modulo1_utils.prioridade import calcular_urgencia


class TestDatas(unittest.TestCase):
    def test_parse_data_valida(self):
        self.assertEqual(parse_data("2026-09-01"), date(2026, 9, 1))

    def test_dias_ate_prazo(self):
        hoje = date(2026, 8, 25)
        prazo = date(2026, 9, 1)
        self.assertEqual(dias_ate_prazo(prazo, hoje), 7)

    def test_prazo_atrasado_e_negativo(self):
        hoje = date(2026, 8, 25)
        prazo = date(2026, 8, 20)
        self.assertEqual(dias_ate_prazo(prazo, hoje), -5)


class TestPrioridade(unittest.TestCase):
    def test_prazo_proximo_forca_alta(self):
        hoje = date(2026, 8, 25)
        prazo = date(2026, 8, 26)  # amanhã
        self.assertEqual(calcular_urgencia(prazo, "baixa", hoje), "alta")

    def test_prazo_distante_mantem_prioridade_declarada(self):
        hoje = date(2026, 8, 25)
        prazo = date(2026, 9, 20)
        self.assertEqual(calcular_urgencia(prazo, "media", hoje), "media")

    def test_prioridade_invalida_levanta_erro(self):
        with self.assertRaises(ValueError):
            calcular_urgencia(date(2026, 9, 1), "urgentissima")


if __name__ == "__main__":
    unittest.main()
