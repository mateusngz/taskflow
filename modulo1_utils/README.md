# Módulo 1 — Modularização

## O que este módulo entrega

Biblioteca de funções utilitárias usadas pelo resto do projeto, separadas
por responsabilidade (um arquivo por assunto, nada de tudo em um `main`).

- `datas.py` — parsing e comparação de datas de prazo (strings tipo
  `"2026-08-30"` viram objetos `date`, cálculo de "dias até o prazo").
- `prioridade.py` — cálculo de nível de urgência de uma tarefa a partir do
  prazo e da prioridade declarada.
- `arvore_subtarefas.py` — exemplo de recursividade: monta e imprime uma
  árvore de subtarefas aninhadas (uma tarefa pode ter subtarefas, que podem
  ter subtarefas).

## Interface pública

| Função | Parâmetros | Retorno |
|---|---|---|
| `parse_data(texto)` | string `"AAAA-MM-DD"` | objeto `date` |
| `dias_ate_prazo(prazo)` | objeto `date` | inteiro (dias restantes, negativo se atrasado) |
| `calcular_urgencia(prazo, prioridade)` | `date`, string | string (`baixa`/`media`/`alta`) |
| `imprimir_arvore(tarefa, nivel=0)` | dict aninhado | (efeito colateral: imprime no terminal) |

## Complexidade

- `parse_data` / `dias_ate_prazo` / `calcular_urgencia`: O(1) — operações
  aritméticas simples sobre datas.
- `imprimir_arvore`: O(n), onde n é o número total de subtarefas na árvore
  (visita cada nó exatamente uma vez).

## Decisões de projeto

- Optamos por Python puro (sem bibliotecas externas de data) para manter o
  módulo simples de auditar e sem dependências.
