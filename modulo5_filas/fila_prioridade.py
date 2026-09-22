"""
Fila de prioridade simples: tarefas mais urgentes saem primeiro,
independente da ordem de chegada.
"""


class FilaPrioridade:
    _ORDEM = {"alta": 0, "media": 1, "baixa": 2}

    def __init__(self):
        self._itens = []  # cada item: (urgencia, tarefa)

    def enfileirar(self, tarefa: dict, urgencia: str) -> None:
        # inserção mantendo a lista sempre ordenada por urgência.
        # Isso deixa enfileirar O(n) mas desenfileirar O(1) — escolha
        # razoável aqui porque a lista de avisos é lida com mais
        # frequência do que é alterada.
        peso = self._ORDEM.get(urgencia, len(self._ORDEM))
        indice_insercao = len(self._itens)
        for i, (peso_existente, _) in enumerate(self._itens):
            if peso < peso_existente:
                indice_insercao = i
                break
        self._itens.insert(indice_insercao, (peso, tarefa))

    def desenfileirar(self):
        if self.vazia():
            return None
        _, tarefa = self._itens.pop(0)
        return tarefa

    def vazia(self) -> bool:
        return len(self._itens) == 0
