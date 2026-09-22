"""
Funções para calcular a urgência de uma tarefa a partir do prazo
e da prioridade declarada pelo usuário.
"""

from datetime import date
from .datas import dias_ate_prazo


NIVEIS = ("baixa", "media", "alta")


def calcular_urgencia(prazo: date, prioridade: str, hoje: date = None) -> str:
    """Combina prazo e prioridade declarada em um nível final de urgência.

    Regra simples:
    - prazo já vencido ou faltando 1 dia -> sempre 'alta'
    - prioridade declarada 'alta' -> mantém 'alta'
    - caso contrário, usa a prioridade declarada
    """
    if prioridade not in NIVEIS:
        raise ValueError(f"prioridade inválida: {prioridade}")

    restantes = dias_ate_prazo(prazo, hoje)

    if restantes <= 1:
        return "alta"
    return prioridade


if __name__ == "__main__":
    from .datas import parse_data

    p = parse_data("2026-08-26")
    print(calcular_urgencia(p, "baixa"))  # prazo amanhã -> 'alta'
