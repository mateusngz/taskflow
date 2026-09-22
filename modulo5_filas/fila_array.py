"""
TAD Fila (FIFO) - versão com array circular.

Array circular evita ter que deslocar todos os elementos ao
desenfileirar: em vez disso, os índices de frente e fim "dão a volta"
quando chegam ao fim do array.
"""


class FilaArrayCircular:
    def __init__(self, capacidade: int):
        self._dados = [None] * capacidade
        self._capacidade = capacidade
        self._frente_idx = 0
        self._quantidade = 0

    def enfileirar(self, item) -> bool:
        if self._quantidade >= self._capacidade:
            return False  # fila cheia
        posicao_livre = (self._frente_idx + self._quantidade) % self._capacidade
        self._dados[posicao_livre] = item
        self._quantidade += 1
        return True

    def desenfileirar(self):
        if self.vazia():
            return None
        item = self._dados[self._frente_idx]
        self._dados[self._frente_idx] = None
        self._frente_idx = (self._frente_idx + 1) % self._capacidade
        self._quantidade -= 1
        return item

    def frente(self):
        if self.vazia():
            return None
        return self._dados[self._frente_idx]

    def vazia(self) -> bool:
        return self._quantidade == 0
