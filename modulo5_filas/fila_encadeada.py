"""
TAD Fila (FIFO) - versão com lista encadeada.
"""


class FilaEncadeada:
    class _No:
        def __init__(self, dado):
            self.dado = dado
            self.proximo = None

    def __init__(self):
        self._frente = None
        self._fim = None

    def enfileirar(self, item) -> None:
        novo = FilaEncadeada._No(item)
        if self._fim is None:
            self._frente = novo
            self._fim = novo
        else:
            self._fim.proximo = novo
            self._fim = novo

    def desenfileirar(self):
        if self.vazia():
            return None
        item = self._frente.dado
        self._frente = self._frente.proximo
        if self._frente is None:
            self._fim = None
        return item

    def frente(self):
        if self.vazia():
            return None
        return self._frente.dado

    def vazia(self) -> bool:
        return self._frente is None
