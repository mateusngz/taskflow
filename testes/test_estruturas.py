"""
Testes dos Módulos 3, 4 e 5.
"""

import unittest

from modulo3_listas.lista_dupla import ListaDuplamenteEncadeada
from modulo4_pilhas.pilha import PilhaEncadeada
from modulo5_filas.fila_array import FilaArrayCircular
from modulo5_filas.fila_prioridade import FilaPrioridade


class TestListaDupla(unittest.TestCase):
    def setUp(self):
        self.lista = ListaDuplamenteEncadeada()
        self.lista.inserir({"id": 1, "titulo": "A"})
        self.lista.inserir({"id": 2, "titulo": "B"})
        self.lista.inserir({"id": 3, "titulo": "C"})

    def test_percorrer_ordem(self):
        ids = [t["id"] for t in self.lista.percorrer()]
        self.assertEqual(ids, [1, 2, 3])

    def test_percorrer_reverso(self):
        ids = [t["id"] for t in self.lista.percorrer(reverso=True)]
        self.assertEqual(ids, [3, 2, 1])

    def test_buscar_existente(self):
        self.assertEqual(self.lista.buscar(2)["titulo"], "B")

    def test_buscar_inexistente(self):
        self.assertIsNone(self.lista.buscar(99))

    def test_remover(self):
        removido = self.lista.remover(2)
        self.assertEqual(removido["id"], 2)
        ids = [t["id"] for t in self.lista.percorrer()]
        self.assertEqual(ids, [1, 3])

    def test_mover(self):
        self.lista.mover(1, 2)  # move o id=1 para a última posição
        ids = [t["id"] for t in self.lista.percorrer()]
        self.assertEqual(ids, [2, 3, 1])


class TestPilhaEncadeada(unittest.TestCase):
    def test_empilhar_e_desempilhar_ordem_lifo(self):
        pilha = PilhaEncadeada()
        pilha.empilhar("A")
        pilha.empilhar("B")
        pilha.empilhar("C")
        self.assertEqual(pilha.desempilhar(), "C")
        self.assertEqual(pilha.desempilhar(), "B")
        self.assertEqual(pilha.desempilhar(), "A")
        self.assertTrue(pilha.vazia())

    def test_desempilhar_vazia_retorna_none(self):
        pilha = PilhaEncadeada()
        self.assertIsNone(pilha.desempilhar())


class TestFilaArrayCircular(unittest.TestCase):
    def test_fifo(self):
        fila = FilaArrayCircular(capacidade=3)
        fila.enfileirar("A")
        fila.enfileirar("B")
        self.assertEqual(fila.desenfileirar(), "A")
        fila.enfileirar("C")
        fila.enfileirar("D")  # usa o espaço que "deu a volta"
        self.assertEqual(fila.desenfileirar(), "B")
        self.assertEqual(fila.desenfileirar(), "C")
        self.assertEqual(fila.desenfileirar(), "D")
        self.assertTrue(fila.vazia())

    def test_fila_cheia_recusa_novo_item(self):
        fila = FilaArrayCircular(capacidade=1)
        self.assertTrue(fila.enfileirar("A"))
        self.assertFalse(fila.enfileirar("B"))


class TestFilaPrioridade(unittest.TestCase):
    def test_ordem_por_urgencia(self):
        fp = FilaPrioridade()
        fp.enfileirar({"id": 1}, "baixa")
        fp.enfileirar({"id": 2}, "alta")
        fp.enfileirar({"id": 3}, "media")

        ordem = [fp.desenfileirar()["id"] for _ in range(3)]
        self.assertEqual(ordem, [2, 3, 1])


if __name__ == "__main__":
    unittest.main()
