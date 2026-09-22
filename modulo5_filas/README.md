# Módulo 5 — Filas

## O que este módulo entrega

- `fila_lembretes.py` — fila FIFO simples: tarefas que vencem hoje entram
  na fila de avisos, na ordem em que foram detectadas.
- `fila_prioridade.py` — fila de prioridade: tarefas urgentes furam a
  fila e saem primeiro, independente da ordem de chegada.

## TAD Fila

| Operação | Descrição |
|---|---|
| `enfileirar(item)` | adiciona no fim |
| `desenfileirar()` | remove e retorna o item da frente |
| `frente()` | consulta sem remover |
| `vazia()` | True se não há elementos |

## Aplicação: simulação de lembretes

Simula o momento em que o app "varre" as tarefas e gera avisos: tarefas
com prazo vencendo entram na fila (FIFO) ou na fila de prioridade
(ordenada por urgência, calculada com `calcular_urgencia` do Módulo 1).

## TODO

- [ ] Implementar `fila_array.py` (array circular, como o roteiro pede)
- [ ] Implementar `fila_encadeada.py`
- [ ] Implementar `fila_prioridade.py`
- [ ] Relatório: complexidade de cada operação, e por que array circular
      evita o desperdício de um array comum ao desenfileirar
