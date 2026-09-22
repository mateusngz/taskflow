"""
Funções utilitárias para lidar com datas de prazo de tarefas.
"""

from datetime import date, datetime


def parse_data(texto: str) -> date:
    """Converte uma string 'AAAA-MM-DD' em um objeto date.

    Levanta ValueError se o formato for inválido.
    """
    return datetime.strptime(texto, "%Y-%m-%d").date()


def dias_ate_prazo(prazo: date, hoje: date = None) -> int:
    """Retorna quantos dias faltam até o prazo.

    Um valor negativo indica que o prazo já passou (dias em atraso).
    """
    if hoje is None:
        hoje = date.today()
    return (prazo - hoje).days


if __name__ == "__main__":
    # exemplo rápido de uso
    prazo = parse_data("2026-09-01")
    print(f"Prazo: {prazo} | dias restantes: {dias_ate_prazo(prazo)}")
