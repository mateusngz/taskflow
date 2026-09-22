"""
TAD Lista - versão com array (tamanho fixo, simulando array estático).
"""


class ListaArray:
    def __init__(self, capacidade: int):
        self._dados = [None] * capacidade
        self._quantidade = 0

    def inserir(self, tarefa: dict, posicao: int = None) -> bool:
        if self._quantidade >= self._capacidade:
            return False  # array cheio

        if posicao is None or posicao >= self._quantidade:
            posicao = self._quantidade

        # desloca os elementos a partir de `posicao` uma casa pra frente
        for i in range(self._quantidade, posicao, -1):
            self._dados[i] = self._dados[i - 1]

        self._dados[posicao] = tarefa
        self._quantidade += 1
        return True

    def remover(self, id_tarefa: int) -> bool:
        indice = None
        for i in range(self._quantidade):
            if self._dados[i]["id"] == id_tarefa:
                indice = i
                break
        if indice is None:
            return False

        # desloca os elementos seguintes uma posição pra trás
        for i in range(indice, self._quantidade - 1):
            self._dados[i] = self._dados[i + 1]

        self._dados[self._quantidade - 1] = None
        self._quantidade -= 1
        return True

    def buscar(self, id_tarefa: int) -> dict | None:
        for tarefa in self._dados[: self._quantidade]:
            if tarefa["id"] == id_tarefa:
                return tarefa
        return None

    def mover(self, id_tarefa: int, nova_posicao: int) -> bool:
        tarefa = self.buscar(id_tarefa)
        if tarefa is None:
            return False
        self.remover(id_tarefa)
        return self.inserir(tarefa, nova_posicao)

    def percorrer(self) -> list:
        return [t for t in self._dados[: self._quantidade]]
