"""
Exemplo de recursividade pedido no Módulo 1: uma tarefa pode ter
subtarefas, que por sua vez podem ter suas próprias subtarefas.
Este módulo monta e imprime essa árvore recursivamente.
"""


def imprimir_arvore(tarefa: dict, nivel: int = 0) -> None:
    """Imprime uma tarefa e suas subtarefas com indentação por nível.

    `tarefa` é um dicionário no formato:
        {"titulo": "...", "subtarefas": [ {...}, {...} ]}
    """
    prefixo = "  " * nivel + ("- " if nivel > 0 else "")
    print(f"{prefixo}{tarefa['titulo']}")

    for sub in tarefa.get("subtarefas", []):
        imprimir_arvore(sub, nivel + 1)


if __name__ == "__main__":
    exemplo = {
        "titulo": "Preparar apresentação",
        "subtarefas": [
            {"titulo": "Montar slides", "subtarefas": []},
            {
                "titulo": "Testar demo",
                "subtarefas": [
                    {"titulo": "Rodar em máquina limpa", "subtarefas": []},
                ],
            },
        ],
    }
    imprimir_arvore(exemplo)
