"""
TAD Pilha (LIFO).

TODO: implementar as duas versões pedidas no roteiro:
- PilhaArray: usando uma lista Python como array de tamanho fixo
- PilhaEncadeada: usando nós ligados (parecido com lista_encadeada.py)

Comece pela versão que achar mais simples e depois compare no relatório.
"""


class PilhaArray:
    def __init__(self, capacidade: int):
        self._dados = [None] * capacidade
        self._topo_idx = -1  # -1 = pilha vazia

    def empilhar(self, item) -> bool:
        if self._topo_idx + 1 >= len(self._dados):
            return False  # pilha cheia
        self._topo_idx += 1
        self._dados[self._topo_idx] = item
        return True

    def desempilhar(self):
        if self.vazia():
            return None
        item = self._dados[self._topo_idx]
        self._dados[self._topo_idx] = None
        self._topo_idx -= 1
        return item

    def topo(self):
        if self.vazia():
            return None
        return self._dados[self._topo_idx]

    def vazia(self) -> bool:
        return self._topo_idx == -1


class PilhaEncadeada:
    class _No:
        def __init__(self, dado):
            self.dado = dado
            self.proximo = None

    def __init__(self):
        self._topo: "PilhaEncadeada._No | None" = None

    def empilhar(self, item) -> None:
        novo = PilhaEncadeada._No(item)
        novo.proximo = self._topo
        self._topo = novo

    def desempilhar(self):
        if self.vazia():
            return None
        item = self._topo.dado
        self._topo = self._topo.proximo
        return item

    def topo(self):
        if self.vazia():
            return None
        return self._topo.dado

    def vazia(self) -> bool:
        return self._topo is None
