"""
TAD Tarefa - versão com armazenamento estático.

Simula um array de tamanho fixo pré-alocado: a capacidade máxima de
tarefas é definida na criação e não pode crescer depois.
"""


class TarefasEstatico:
    def __init__(self, capacidade: int):
        self._capacidade = capacidade
        self._dados = [None] * capacidade  # espaço pré-alocado
        self._quantidade = 0

    def criar(self, id_: int, titulo: str, prazo: str, prioridade: str) -> bool:
        """Adiciona uma tarefa no primeiro espaço livre.

        Retorna False se não houver espaço (array cheio) — isso é o
        comportamento que queremos evidenciar na comparação com a
        versão dinâmica.
        """
        if self._quantidade >= self._capacidade:
            return False  # TODO: decidir e documentar o que fazer aqui

        self._dados[self._quantidade] = {
            "id": id_,
            "titulo": titulo,
            "prazo": prazo,
            "prioridade": prioridade,
            "status": "a_fazer",
        }
        self._quantidade += 1
        return True

    def buscar_por_id(self, id_: int) -> dict | None:
        for tarefa in self._dados[: self._quantidade]:
            if tarefa["id"] == id_:
                return tarefa
        return None

    def marcar_concluida(self, id_: int) -> bool:
        tarefa = self.buscar_por_id(id_)
        if tarefa is None:
            return False
        tarefa["status"] = "concluido"
        return True

    def listar(self) -> list:
        return [t for t in self._dados[: self._quantidade]]


if __name__ == "__main__":
    tarefas = TarefasEstatico(capacidade=3)
    tarefas.criar(1, "Estudar para prova", "2026-09-01", "alta")
    print(tarefas.listar())
