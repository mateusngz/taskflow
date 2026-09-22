"""
TAD Tarefa - versão com armazenamento dinâmico.

Cada tarefa é um objeto criado sob demanda, sem limite de quantidade
pré-definido (equivalente conceitual a alocação dinâmica com
malloc/free em C, aqui feita via objetos e garbage collector).
"""


class Tarefa:
    def __init__(self, id_: int, titulo: str, prazo: str, prioridade: str):
        self.id = id_
        self.titulo = titulo
        self.prazo = prazo
        self.prioridade = prioridade
        self.status = "a_fazer"

    def marcar_concluida(self) -> None:
        self.status = "concluido"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "titulo": self.titulo,
            "prazo": self.prazo,
            "prioridade": self.prioridade,
            "status": self.status,
        }


class TarefasDinamico:
    def __init__(self):
        self._tarefas: list[Tarefa] = []

    def criar(self, id_: int, titulo: str, prazo: str, prioridade: str) -> Tarefa:
        nova = Tarefa(id_, titulo, prazo, prioridade)
        self._tarefas.append(nova)
        return nova

    def buscar_por_id(self, id_: int) -> Tarefa | None:
        for tarefa in self._tarefas:
            if tarefa.id == id_:
                return tarefa
        return None

    def marcar_concluida(self, id_: int) -> bool:
        tarefa = self.buscar_por_id(id_)
        if tarefa is None:
            return False
        tarefa.marcar_concluida()
        return True

    def listar(self) -> list:
        return [t.to_dict() for t in self._tarefas]


if __name__ == "__main__":
    tarefas = TarefasDinamico()
    tarefas.criar(1, "Estudar para prova", "2026-09-01", "alta")
    print(tarefas.listar())
