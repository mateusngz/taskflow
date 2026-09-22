"""
Sistema de undo/redo usando duas pilhas (encadeadas).

Estrategia: antes de qualquer acao alterar o estado das colunas do
Kanban, guardamos uma "foto" (snapshot) do estado anterior na pilha de
undo. Desfazer = tirar a foto anterior da pilha e restaurar; a foto do
estado em que estavamos vai para a pilha de redo, pra poder refazer.

E uma simplificacao do conceito de "comando reversivel": em vez de
guardar como desfazer cada tipo de acao separadamente, guardamos o
estado completo antes da acao. Continua usando o TAD Pilha (LIFO) como
pede o roteiro.
"""

from .pilha import PilhaEncadeada


class GerenciadorUndoRedo:
    def __init__(self):
        self._pilha_undo = PilhaEncadeada()
        self._pilha_redo = PilhaEncadeada()

    def registrar_estado_anterior(self, snapshot) -> None:
        """Chamado ANTES de aplicar uma acao, passando o estado atual
        (antes da mudanca). Uma acao nova invalida o historico de redo."""
        self._pilha_undo.empilhar(snapshot)
        self._pilha_redo = PilhaEncadeada()

    def pode_desfazer(self) -> bool:
        return not self._pilha_undo.vazia()

    def pode_refazer(self) -> bool:
        return not self._pilha_redo.vazia()

    def desfazer(self, estado_atual):
        """Retorna o snapshot anterior (ou None se nao ha o que desfazer).
        `estado_atual` e empilhado em redo, para permitir refazer depois.
        """
        if not self.pode_desfazer():
            return None
        anterior = self._pilha_undo.desempilhar()
        self._pilha_redo.empilhar(estado_atual)
        return anterior

    def refazer(self, estado_atual):
        """Retorna o proximo snapshot (ou None se nao ha o que refazer)."""
        if not self.pode_refazer():
            return None
        proximo = self._pilha_redo.desempilhar()
        self._pilha_undo.empilhar(estado_atual)
        return proximo
