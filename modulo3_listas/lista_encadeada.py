"""
TAD Lista - versão com encadeamento simples.
"""


class No:
    def __init__(self, dado: dict):
        self.dado = dado
        self.proximo: "No | None" = None


class ListaEncadeada:
    def __init__(self):
        self._cabeca: No | None = None
        self._quantidade = 0

    def inserir(self, tarefa: dict, posicao: int = None) -> None:
        novo = No(tarefa)

        if self._cabeca is None or posicao == 0:
            novo.proximo = self._cabeca
            self._cabeca = novo
            self._quantidade += 1
            return

        atual = self._cabeca
        indice = 0
        while atual.proximo is not None and (posicao is None or indice < posicao - 1):
            atual = atual.proximo
            indice += 1

        novo.proximo = atual.proximo
        atual.proximo = novo
        self._quantidade += 1

    def remover(self, id_tarefa: int) -> bool:
        anterior = None
        atual = self._cabeca

        while atual is not None:
            if atual.dado["id"] == id_tarefa:
                if anterior is None:
                    self._cabeca = atual.proximo
                else:
                    anterior.proximo = atual.proximo
                self._quantidade -= 1
                return True
            anterior = atual
            atual = atual.proximo

        return False

    def buscar(self, id_tarefa: int) -> dict | None:
        atual = self._cabeca
        while atual is not None:
            if atual.dado["id"] == id_tarefa:
                return atual.dado
            atual = atual.proximo
        return None

    def mover(self, id_tarefa: int, nova_posicao: int) -> bool:
        tarefa = self.buscar(id_tarefa)
        if tarefa is None:
            return False
        self.remover(id_tarefa)
        self.inserir(tarefa, nova_posicao)
        return True

    def percorrer(self) -> list:
        resultado = []
        atual = self._cabeca
        while atual is not None:
            resultado.append(atual.dado)
            atual = atual.proximo
        return resultado
