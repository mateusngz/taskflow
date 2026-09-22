# Módulo 4 — Pilhas

## O que este módulo entrega

Pilha de **undo/redo**: toda ação do usuário (criar, editar, mover ou
excluir uma tarefa) gera um "comando" que é empilhado. Desfazer = pop da
pilha de undo + push na pilha de redo (e vice-versa).

## TAD Pilha

| Operação | Descrição |
|---|---|
| `empilhar(item)` | adiciona no topo — O(1) |
| `desempilhar()` | remove e retorna o topo — O(1) |
| `topo()` | consulta o topo sem remover — O(1) |
| `vazia()` | True se não há elementos |

## Aplicação prática: undo/redo

- `PilhaAcoes` guarda comandos, cada um sabendo como se desfazer
  (ex.: `{"tipo": "criar", "id": 3}` desfeito = remover a tarefa 3).
- Duas pilhas: `pilha_undo` e `pilha_redo`.
- Ao executar uma ação nova: empilha em `undo`, **limpa** `redo` (uma
  ação nova invalida o "refazer" anterior — decisão de projeto a
  documentar no relatório).

## TODO

- [ ] Implementar `pilha.py` (com array e com lista encadeada, para
      comparar como pede o roteiro)
- [ ] Implementar `undo_redo.py` usando a pilha
- [ ] Relatório: complexidade de cada operação nas duas versões
