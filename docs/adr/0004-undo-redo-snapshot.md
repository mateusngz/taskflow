# 0004 — Undo/redo por snapshot de estado

## Contexto

O Módulo 4 pede uma aplicação prática de pilha, e undo/redo foi a
escolhida. Existem duas formas comuns de implementar isso: guardar
"comandos reversíveis" (cada ação sabe como desfazer a si mesma) ou
guardar uma cópia do estado inteiro antes de cada ação.

## Decisão

Usar a estratégia de **snapshot de estado**: antes de qualquer ação
alterar as colunas, uma cópia completa do estado atual das três colunas
é empilhada em `GerenciadorUndoRedo` (que usa `PilhaEncadeada` por
baixo). Desfazer = tirar a cópia anterior da pilha e restaurar; refazer
funciona de forma simétrica com uma segunda pilha.

## Consequências

- Mais simples de implementar e de garantir correto do que escrever uma
  função de "desfazer" separada para cada tipo de ação (criar, mover,
  concluir) — reduz risco de bugs no undo de uma ação específica.
- Continua usando o TAD Pilha (LIFO) como o roteiro pede, só que
  guardando estados em vez de comandos.
- Tem um custo de memória maior: cada ação guarda uma cópia inteira das
  colunas, não só a diferença. Para o tamanho de dados de uma lista de
  tarefas pessoal, esse custo é desprezível na prática.
- Uma ação nova sempre limpa a pilha de redo (comportamento padrão da
  maioria dos editores de texto: fazer algo novo depois de desfazer
  invalida o "refazer" anterior).
