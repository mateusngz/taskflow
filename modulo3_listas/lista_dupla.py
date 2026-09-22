"""
TAD Lista - versão duplamente encadeada.

Usada para mover tarefas entre colunas do Kanban ou reordenar
prioridade dentro de uma coluna (precisa andar para os dois lados).
"""


class NoDuplo:
    def __init__(self, dado: dict):
        self.dado = dado
        self.anterior: "NoDuplo | None" = None
        self.proximo: "NoDuplo | None" = None


class ListaDuplamenteEncadeada:
    def __init__(self):
        self._cabeca: NoDuplo | None = None
        self._cauda: NoDuplo | None = None
        self._quantidade = 0

    def inserir(self, tarefa: dict, posicao: int = None) -> None:
        novo = NoDuplo(tarefa)

        if self._cabeca is None:
            self._cabeca = novo
            self._cauda = novo
            self._quantidade += 1
            return

        if posicao is None or posicao >= self._quantidade:
            # insere no fim
            novo.anterior = self._cauda
            self._cauda.proximo = novo
            self._cauda = novo
            self._quantidade += 1
            return

        if posicao <= 0:
            # insere no início
            novo.proximo = self._cabeca
            self._cabeca.anterior = novo
            self._cabeca = novo
            self._quantidade += 1
            return

        # posição no meio: caminha até o nó que hoje ocupa essa posição
        atual = self._cabeca
        for _ in range(posicao):
            atual = atual.proximo

        anterior = atual.anterior
        novo.anterior = anterior
        novo.proximo = atual
        anterior.proximo = novo
        atual.anterior = novo
        self._quantidade += 1

    def remover(self, id_tarefa: int) -> dict | None:
        atual = self._cabeca
        while atual is not None:
            if atual.dado["id"] == id_tarefa:
                if atual.anterior is not None:
                    atual.anterior.proximo = atual.proximo
                else:
                    self._cabeca = atual.proximo

                if atual.proximo is not None:
                    atual.proximo.anterior = atual.anterior
                else:
                    self._cauda = atual.anterior

                self._quantidade -= 1
                return atual.dado
            atual = atual.proximo
        return None

    def buscar(self, id_tarefa: int) -> dict | None:
        atual = self._cabeca
        while atual is not None:
            if atual.dado["id"] == id_tarefa:
                return atual.dado
            atual = atual.proximo
        return None

    def mover(self, id_tarefa: int, nova_posicao: int) -> bool:
        tarefa = self.remover(id_tarefa)
        if tarefa is None:
            return False
        self.inserir(tarefa, nova_posicao)
        return True

    def percorrer(self, reverso: bool = False) -> list:
        resultado = []
        if not reverso:
            atual = self._cabeca
            while atual is not None:
                resultado.append(atual.dado)
                atual = atual.proximo
        else:
            atual = self._cauda
            while atual is not None:
                resultado.append(atual.dado)
                atual = atual.anterior
        return resultado

    def vazia(self) -> bool:
        return self._cabeca is None
